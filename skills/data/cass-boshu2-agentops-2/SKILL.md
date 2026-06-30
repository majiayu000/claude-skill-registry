---
name: cass
description: Mine past agent sessions for working prompts, decisions, and patterns. Use when "what did I ask?", "find that prompt", session archaeology, or agent history.
practices:
- pragmatic-programmer
skill_api_version: 1
user-invocable: false
hexagonal_role: supporting
metadata:
  tier: execution
  external_dependencies:
  - "cass binary (>=0.3.6 recommended; some commands require HEAD \u2014 see Version Pinning)"
  - jq (required for parsing --json output)
  - GNU coreutils 'timeout' (recommended; cass index can hang under contention)
  - ssh + rsync (optional; only for cross-machine `cass sources` workflows)
  - fastembed model bundle ~90MB (optional; only for --mode semantic / hybrid; install via `cass models install`)
---
# cass Session Search

## Table of Contents

- [The Goldmine Principle](#the-goldmine-principle)
- [THE EXACT PROMPT — Discovery Workflow](#the-exact-prompt--discovery-workflow)
- [Version Pinning Caveat](#version-pinning-caveat)
- [Two-Step Bootstrap (Replaces "ALWAYS first")](#two-step-bootstrap-replaces-always-first)
- [Stuck-Index & Recovery Decision Tree](#stuck-index--recovery-decision-tree)
- [Quick Reference](#quick-reference)
- [When to Use What](#when-to-use-what)
- [Critical Rules](#critical-rules)
- [Agent Harness Exclusion](#agent-harness-exclusion)
- [Search Modes](#search-modes)
- [Cross-Machine Search (Multi-Workstation Corpus)](#cross-machine-search-multi-workstation-corpus)
- [Anti-Patterns (Don't Do These)](#anti-patterns-dont-do-these)
- [Resume a Past Session in Its Native Harness](#resume-a-past-session-in-its-native-harness)
- [The Heuristics](#the-heuristics)
- [jq Essentials](#jq-essentials)
- [Hidden Power: Capabilities the Old Skill Missed](#hidden-power-capabilities-the-old-skill-missed)
- [Token & Cost Analytics (Bonus Use Case)](#token--cost-analytics-bonus-use-case)
- [Recovery Cheat Sheet (No-Permission Moves)](#recovery-cheat-sheet-no-permission-moves)
- [Reference Index](#reference-index)
- [Quick Search (Grep Recipes for References)](#quick-search-grep-recipes-for-references)
- [Scripts](#scripts)
- [Validation](#validation)

> **Core Insight:** Your repeated prompts are your best prompts. If you typed it 10+ times, it works. Mine your history.

## The Goldmine Principle

Your conversation history contains:
- **Refined prompts** — Every rephrase that worked better was captured
- **Working rituals** — Prompts repeated 10+ times ARE your methodology
- **Scope decisions** — "When did we decide NOT to do X?"
- **Recovery moments** — What you searched for after context loss = what mattered

**The insight:** Mining your past beats inventing new approaches.

---

## THE EXACT PROMPT — Discovery Workflow

```
1. Bootstrap: Check health, refresh index, get project overview
   cass status --json && cass index --json
   cass search "*" --workspace /data/projects/PROJECT --aggregate agent,date --limit 1 --json

2. Find prompts: Search for keywords, filter to user prompts (lines 1-3)
   cass search "KEYWORD" --workspace /data/projects/PROJECT --json --fields minimal --limit 50 \
     | jq '[.hits[] | select(.line_number <= 3)]'

3. Follow hits: View the actual content
   cass view /path/from/source_path.jsonl -n LINE -C 20

4. Expand context: See the full conversation flow
   cass expand /path/from/source_path.jsonl --line LINE --context 3

5. Discover related: Find the whole work cluster
   cass context /path/from/source_path.jsonl --json
```

### Why This Workflow Works

- **Aggregations first** — Know the terrain before diving in
- **`--fields minimal`** — 5x smaller output, preserves context window
- **`line_number <= 3`** — User prompts live at the top of sessions
- **Context clustering** — Work happens in clusters; one good hit → many related sessions

---

## Version Pinning Caveat

cass evolves quickly. The skill describes **HEAD behavior** (latest source in `/dp/coding_agent_session_search`). The released **v0.3.6 binary** lacks several features added since:

- `cass sources agents {list,exclude,include}` — added 2026-04-20 (commit `82d8d70e`)
- Tail-end writer-race tolerance for full rebuilds — fixed 2026-04-22 (commit `e06342f2`, bead `zz8ni`)
- Lexical generation manifests for federated installs (commits `2b7b86a1`, `683ccd03`, `cf76fe15`)
- Rebuild producer stall telemetry (commit `73a86604`)

When a flag/subcommand returns "unrecognized" or behaves differently than documented, run `cass --version` and check `git log -- src/lib.rs` for the relevant commit. Each affected section calls out which commit/version it depends on.

Probe what your installed binary actually supports:
```bash
cass capabilities --json | jq '{version: .crate_version, features, connectors}'
cass introspect --json   | jq '.commands[].name'
```

---

## Two-Step Bootstrap (Replaces "ALWAYS first")

**Three states matter — never conflate them.**

| State | What it means | What to do |
|-------|---------------|------------|
| `cass health` exit 0 | Sub-50ms preflight passed | Search immediately |
| `cass health` exit 1 + `index.stale=true` | Index is **usable but old** | Search now, refresh in background with a wall-clock cap: `( timeout 600 cass index --json &>/tmp/cass-bg.log </dev/null & )` (NEVER bare `&` — cass index can hang) |
| `cass status` returns `database.exists=false` OR `documents=0` | Truly **broken/uninitialized** | Run `cass doctor --fix --json`, then `cass index --full --json` |

**The trap:** Treating a stale index as broken triggers an unneeded full rebuild (8–25s cost) when an incremental refresh (1–3s) or even a stale-but-correct query would have worked.

```bash
# Robust two-step bootstrap that never blocks the user.
# IMPORTANT: every cass index call gets a wall-clock cap. cass index has been
# observed to hang indefinitely under contention — without `timeout`, the
# bootstrap itself becomes the symptom.
cass status --json | jq '{healthy, fresh: .index.fresh, stale: .index.stale, db: .database.exists, sem: .semantic.available}'

# Refresh policy: stale → bg refresh (capped); never block search
if [ "$(cass status --json | jq -r '.index.stale')" = "true" ]; then
  ( timeout 600 cass index --json >"/tmp/cass-index.$$.log" 2>&1 </dev/null & ) 2>/dev/null
fi
# Search even with stale index — results are still useful
cass search "KEYWORD" --workspace /path --json --fields minimal --limit 10
```

For the production-quality version of this logic (cap-on-every-call, broken-state escalation, exit-code semantics for hooks), use `scripts/recover.sh` — it implements the full decision tree with timeouts and per-PID logs.

`cass health` returning exit 1 on stale is a *deliberate* preflight signal for cron/CI. In an interactive agent loop, prefer `cass status --json` and decide.

---

## Stuck-Index & Recovery Decision Tree

Real-world bugs we've hit (all observed in mined sessions). Walk top-down — **first match wins**.

| Symptom | Likely cause | Autonomous fix (no user prompt needed) |
|---------|--------------|----------------------------------------|
| `cass index --json` streams `phase: indexing, current: 0, total: N` for >2 min | OPEN issue #196 in v0.3.6: incremental hangs after prior `--force-rebuild` | Kill the run, then `cass index --full --force-rebuild --json` (25s typical) |
| `cass status` shows `index.rebuilding=true` and `pid` is stale (>1h) | Crashed indexer left lock | `cass doctor --fix --json` (removes stale `.index.lock` automatically) |
| `cass search` returns 0 hits but the file plainly contains the term | Term lives in tool stdout/stderr (skipped at index time) | Fall back to `rg -n "TERM" /path/to/session.jsonl` |
| `cass search --workspace /X` returns 0; same query without `--workspace` works | Workspace string mismatch | `cass search "KEYWORD" --aggregate workspace --limit 1 --json` to discover the canonical path, then re-run |
| `vtable constructor failed: fts_messages` (older bug, fixed in 0.3.0+) | DB↔FTS schema drift after upgrade | `cass doctor --fix --json` rebuilds the Tantivy side from SQLite |
| `--limit 0 panic` | Earlier cass versions panicked on limit=0 | Always pass `--limit 1` (or `--limit 5`) for aggregations |
| Massive `core.NNNNN` files in cass project dir | Past indexer crash recorded a coredump | They're SAFE to leave; they don't affect search. Only delete with explicit user permission. |
| `cass models install` fails with WSAENOTCONN on Windows (closed #193) | Network blip during huggingface download | Retry once; if it persists, use `--mirror <URL>` to point at a different HF mirror, or `--from-file <DIR>` if you have the model cached locally. Then `cass models verify`. |
| `cass index` says "Index rebuild is already in progress" but nothing visible | Concurrent agent triggered a rebuild | Don't fight it — `cass status --json | jq '.rebuild'` shows `pid`/`phase`/`processed_conversations`. Wait ~60s, re-check. |
| `cass index --full --force-rebuild --json` runs for 200s+ then exits with `"index failed: updating last_indexed_at after index run ... database is busy"` | Concurrent-rebuild race in `persist_final_index_run_metadata`. **Fixed at HEAD (commit e06342f2, bead zz8ni); affects v0.3.6 and earlier.** | Verify the index data is good: `cass search "X" --limit 1 --json | jq '.total_matches'` — if non-zero, index is fine, just the freshness marker is missing. A subsequent `cass index --json` rewrites the marker once contention clears. Upgrade to >0.3.6 to get the log-and-swallow fix |
| `cass status` shows `unhealthy` indefinitely after a successful-looking rebuild | Same as above — timestamp marker never landed | Same fix: confirm searches return hits, then a single quiet `cass index --json` writes the marker. Upgrade past v0.3.6 for the proper fix |

**Never paper over by skipping cass and falling back to manual `find`/`grep`.** The autonomous fixes above resolve every real failure without user intervention. Asking the user to "rebuild your index" is the worst outcome — they have agents waiting.

---

## Quick Reference

```bash
# Health + refresh (ALWAYS first)
cass status --json && cass index --json

# Project overview: who did what, when?
cass search "*" --workspace /path --aggregate agent,date --limit 1 --json

# Find keyword, minimal output
cass search "KEYWORD" --workspace /path --json --fields minimal --limit 50

# Follow a hit
cass view /path.jsonl -n LINE -C 20        # Line-oriented
cass expand /path.jsonl --line LINE --context 3  # Message-oriented

# Find related sessions
cass context /path.jsonl --json

# Export for parsing
cass export /path.jsonl --format json --include-tools -o /tmp/out.json

# Inspect or change persistent agent-harness exclusions
cass sources agents list --json
cass sources agents exclude openclaw
cass sources agents exclude openclaw --keep-indexed-data
cass sources agents include openclaw
```

---

## When to Use What

| You Want | Use | Why |
|----------|-----|-----|
| Project overview | `--aggregate agent,date --limit 1` | Counts only, no content |
| Find prompts | `--fields minimal` + `jq select(.line_number <= 3)` | User prompts are lines 1-3 |
| Ritual detection | Count matches: >10 = ritual | Repeated = working |
| Full conversation | `cass expand --context 3` | Message boundaries preserved |
| Raw JSON parsing | `cass export --include-tools -o file.json` | Never pipe exports |
| Content not found | `rg "string" /path.jsonl` | cass skips tool outputs |
| Noisy harness flooding index | `cass sources agents exclude <agent>` | Persistently disable future indexing |

---

## Critical Rules

| Rule | Why | Consequence |
|------|-----|-------------|
| **`--limit 1` minimum** | `--limit 0` panics | Use 1 for aggregations |
| **`--fields minimal`** | Token efficiency | 5x smaller output |
| **Export to file** | Piping causes broken pipe panic | `-o /tmp/out.json` always |
| **Exact workspace paths** | Case-sensitive matching | Use `--aggregate workspace` to discover |
| **`--include-tools`** | Tool calls hidden by default | Required for full export |

---

## Agent Harness Exclusion

When a user tells you one agent harness is producing garbage, loops, or too much disk usage, handle that directly in `cass` instead of telling them it cannot be excluded.

```bash
# See current state
cass sources agents list --json

# Persistently stop indexing this harness in future scans/syncs/watch mode
cass sources agents exclude openclaw

# Keep already indexed data but block future indexing
cass sources agents exclude openclaw --keep-indexed-data

# Re-enable later
cass sources agents include openclaw
```

### What `exclude` actually does

- Writes the preference to `sources.toml`, so the setting survives future runs
- Prevents future indexing even if the source files still exist on disk
- By default, purges already archived local data for that harness and rebuilds lexical search so the exclusion also reclaims space

### When to use it

- A harness is spamming looped or low-value output
- A user wants `cass` to remember "ignore this source going forward"
- You need a reversible, agent-friendly way to reduce archive bloat without manually deleting source files

---

## Search Modes

| Mode | When | Example |
|------|------|---------|
| `lexical` (default) | Exact strings, filenames | `"AGENTS.md"`, `"--workspace"` |
| `semantic` | Conceptual, unknown wording | `"scope reduction discussions"` |
| `hybrid` | Broad exploration | `"architecture decisions"` |

**Default to lexical.** Only use semantic when you don't know exact wording.

### Enabling Semantic / Hybrid (one-time)

```bash
cass models status --json    # state: not_installed | installed | partial
cass models install          # downloads ~90MB MiniLM bundle from HuggingFace
cass index --semantic --build-hnsw --json   # builds vector + HNSW
cass search "QUERY" --mode hybrid --json    # then queries fall back to lexical if semantic missing
```

If the model is `not_installed`, `--mode hybrid` and `--mode semantic` **silently fall back to lexical** — no panic, no degraded experience. See [SEMANTIC_AND_HYBRID.md](references/SEMANTIC_AND_HYBRID.md).

---

## Cross-Machine Search (Multi-Workstation Corpus)

When the user has agents running on `css`, `csd`, `ts1`, `ts2`, etc., the cass corpus on each machine is **disjoint**. Three ways to reach across:

```bash
# Option A: One-shot remote query (no setup, slow per call)
ssh css 'cass search "KEYWORD" --json --fields minimal --limit 20' | jq '.hits'

# Option B: Configured sources (preferred — caches the remote sessions locally)
cass sources setup                                      # interactive wizard, auto-discovers from ~/.ssh/config
cass sources add ssh://user@css --name css --preset linux-defaults
cass sources sync --source css --json                   # rsyncs new sessions, then re-indexes
cass search "KEYWORD" --json                            # results now span all configured sources
cass sources list --json                                # see what's wired up

# Option C: Parallel fan-out (when speed matters more than dedup)
for h in css csd ts1 ts2; do
  ssh "$h" 'cass search "KEYWORD" --json --fields minimal --limit 10' > "/tmp/cass-$h.json" &
done
wait
jq -s '[.[] | .hits[]] | unique_by(.source_path + (.line_number|tostring))' /tmp/cass-*.json
```

`cass sources doctor` diagnoses connectivity. Configured-source results carry `origin_host` in their hit metadata — preserve it when reporting back to the user. Full reference: [REMOTE_SOURCES.md](references/REMOTE_SOURCES.md).

---

## Anti-Patterns (Don't Do These)

| Anti-pattern | Why it's wrong | Do instead |
|--------------|----------------|------------|
| Asking the user "should I rebuild the index?" | They have agents waiting; rebuild is safe and idempotent | Just run `cass doctor --fix --json` (preserves source data) |
| Running `cass index --full` whenever `status` says unhealthy | A 25s rebuild for a 30-min stale index is wasteful | Check `index.stale` separately from `database.exists`; prefer incremental |
| Running bare `cass` to "see what's there" | Launches blocking TUI in the agent's session | Always `--json` or `--robot`; never bare |
| Piping `cass export` into `head`/`jq` | Broken-pipe panic on large sessions | `cass export ... -o /tmp/x.json` first, then operate on the file |
| Treating subagent files as the same as parent sessions | Subagents are separate conversation logs with their own line-2 prompt | Filter by `select(.source_path \| contains("subagent"))` |
| Using `--limit 0` for "no limit" | Earlier cass panics; modern cass caps to RAM ceiling but rarely what you want | Use a real limit (`--limit 50`) or pagination via `--cursor` |
| Searching with `--workspace /X` and trusting 0 hits | Workspace strings are case-sensitive and trailing-slash-sensitive | When 0 hits but you expected some, re-run with `--aggregate workspace --limit 1` to discover the canonical key |
| Skipping `--fields minimal` on wide scans | Default `full` returns ~3KB per hit × 100 hits = 300KB context burn | Always pass `--fields minimal` for wide passes; upgrade to `summary`/`full` for the few you keep |
| Reading session file with `cat` to extract a prompt | Loads the full conversation into context | `cass view PATH -n LINE -C 5` (window) or `cass expand PATH --line LINE --context 3` (message-aware) |
| Re-indexing on every `cass search` | Wasteful; index is shared across processes | Index is shared. Only refresh when `cass status` says `stale` or `recommended_action` says so |

---

## Resume a Past Session in Its Native Harness

`cass resume` resolves a session path into the exact command its native CLI uses to continue the conversation — Claude Code, Codex, Gemini, OpenCode, pi_agent.

```bash
# Find a relevant past session
cass search "KEYWORD" --json --fields minimal --limit 5 \
  | jq -r '.hits[0].source_path' > /tmp/sess.path

# Print the resume command without executing
cass resume "$(cat /tmp/sess.path)" --shell

# Or replace the current process with the resumed agent
cass resume "$(cat /tmp/sess.path)" --exec
```

**Pitfall:** Subagent files (`subagents/agent-*.jsonl`) are **not resumable** by design — they're orchestrated by a parent. You'll get `session_id_not_found` with a hint to pass `--agent claude`. Resolve to the parent session via `cass context <path> --json` first. See [RESUME.md](references/RESUME.md).

---

## The Heuristics

| Signal | Meaning | Action |
|--------|---------|--------|
| `line_number` 1-3 | User prompts | Filter: `select(.line_number <= 3)` |
| `/subagents/` line 2 | THE extraction prompt | Copy-paste ready |
| `total_matches` > 10 | Ritual pattern | Document it, reuse it |
| 0 results + content exists | Workspace path mismatch | Use `--aggregate workspace` |

---

## jq Essentials

```bash
# User prompts only
| jq '[.hits[] | select(.line_number <= 3)]'

# Source paths for follow-up
| jq '.hits[].source_path' -r

# Aggregation buckets
| jq '.aggregations.agent.buckets'

# Count matches
| jq '.total_matches'

# Find repeated prompts (ritual detection)
| jq '[.hits[] | select(.line_number <= 3) | .title[0:80]] | group_by(.) | map({prompt: .[0], count: length}) | sort_by(-.count) | .[0:20]'
```

---

## Hidden Power: Capabilities the Old Skill Missed

| Command | What it gives you | When |
|---------|-------------------|------|
| `cass health` | <50ms exit-code-only preflight | Cron / hook gating |
| `cass index --watch --json` | Filesystem-watcher keeps index live; one cycle = `--watch-once /path` | Long-running orchestrator hosts |
| `cass index --idempotency-key K --json` | Cached identical-key responses for 24h | Retried CI runs |
| `cass index --semantic --build-hnsw` | O(log n) approximate vector search | After `cass models install` |
| `cass doctor --fix --json` | Auto-rebuilds index from DB; backs up corrupt DB to `.corrupt.<ts>` | Any time `status.healthy=false` |
| `cass resume PATH --shell` | Cross-harness resume command emitter | Continuing a past Codex/Claude/Gemini session |
| `cass sources setup` | Interactive ssh-config-aware multi-machine wizard | First time wiring a fleet |
| `cass sources sync --source NAME --json` | rsync remote sessions, then re-index | Periodic fleet refresh |
| `cass sources doctor --json` | Connectivity + path probe | Before relying on cross-machine results |
| `cass sources mappings ...` | Rewrite source paths to local equivalents | After moving a workspace |
| `cass sources agents {list,exclude,include}` | Persistent harness exclusion (writes `disabled_agents` in `~/.config/cass/sources.toml`) | When openclaw / a noisy connector floods the index |
| `cass models install / status / verify / remove` | Manage the MiniLM bundle (~90MB) | Enabling semantic search |
| `cass analytics tokens \| tools \| models` | Per-day/per-tool/per-model usage stats from indexed sessions | Cost reports, regression checks |
| `cass analytics rebuild --json` | Backfill rollup tables when coverage_pct is low | After bulk `import` or `sources sync` |
| `cass analytics validate --json` | Detect drift between raw rows and rollups | Sanity check before reporting numbers |
| `cass import chatgpt PATH` | Bring `conversations.json` exports from ChatGPT web into the corpus | Migrating off ChatGPT.com |
| `cass export-html PATH --password ...` | Encrypted, self-contained HTML conversation viewer | Sharing one session with a teammate |
| `cass pages encrypt ARCHIVE --with-recovery` | Encrypted searchable archive for static hosting | Publishing a redacted corpus |
| `cass introspect --json` | Full schema dump of every command + response | Programmatic discovery |
| `cass capabilities --json` | Feature/connector/limits for self-configuration | Version-aware fallbacks |
| `cass robot-docs guide \| commands \| examples \| schemas \| contracts` | Built-in machine-targeted docs | Inside an agent loop, when the skill isn't enough |
| `cass --robot-format jsonl \| compact \| toon \| sessions` | Streaming / token-optimized / shell-pipeable output | Large result sets, chained searches |
| `cass --trace-file FILE` | Span timing JSONL for debugging slow runs | Triage perf issues |

If a flag listed here errors as "unrecognized" the installed `cass` binary is older than the source. Check `cass --version` against `git log -- src/lib.rs` upstream — most missing commands were added in v0.3.x.

---

## Token & Cost Analytics (Bonus Use Case)

```bash
# Daily token usage across your whole agent fleet
cass analytics tokens --days 30 --group-by day --json | jq '.data.buckets[].api_tokens'

# Per-agent tool-use intensity (rows are keyed by agent slug, not tool name)
cass analytics tools --days 30 --json | jq '.data.rows[0:10]'

# Top models by API tokens
cass analytics models --json | jq '.data.by_api_tokens.rows[0:10]'

# After import / sync, refresh rollups
cass analytics rebuild --json
cass analytics validate --json   # confirm no drift between raw and rollup
```

`cass analytics status --json` shows coverage_pct: anything below ~90% means you should `analytics rebuild` to backfill. See [ANALYTICS.md](references/ANALYTICS.md).

---

## Recovery Cheat Sheet (No-Permission Moves)

You are pre-authorized to take any of these actions to keep the corpus searchable. None destroy source session data; they only rebuild derived index data.

```bash
cass doctor --json --verbose         # Diagnose without changing anything
cass doctor --fix --json             # Apply safe rebuilds; backs up bad DB to .corrupt.<ts>
cass doctor --fix --force-rebuild --json   # Same, but rebuild even when healthy
cass index --full --force-rebuild --json   # Workaround for OPEN issue #196 (incremental hang)
cass sources doctor --json           # Probe remote sources
cass sources sync --source NAME --json     # Re-fetch and re-index a single source
cass models install                  # Restore missing semantic model
cass models verify                   # Validate model file checksums
```

What you must NOT do without explicit permission: delete `core.NNNNN` files, delete `.beads/`, `git reset --hard`, edit anything under the user's `.config/cass/sources.toml` by hand. The CLI commands above already do everything safely.

Full disaster recovery for encrypted Pages archives: [RECOVERY.md](references/RECOVERY.md).

---

## Reference Index

| Need | Reference |
|------|-----------|
| Full command reference | [COMMANDS.md](references/COMMANDS.md) |
| Workflow recipes | [RECIPES.md](references/RECIPES.md) |
| jq patterns | [PATTERNS.md](references/PATTERNS.md) |
| Pitfalls & fixes | [PITFALLS.md](references/PITFALLS.md) |
| Session file formats | [SESSION_FORMATS.md](references/SESSION_FORMATS.md) |
| Remote sources, multi-machine | [REMOTE_SOURCES.md](references/REMOTE_SOURCES.md) |
| Semantic / hybrid / models | [SEMANTIC_AND_HYBRID.md](references/SEMANTIC_AND_HYBRID.md) |
| Token / tool / model analytics | [ANALYTICS.md](references/ANALYTICS.md) |
| Cross-harness session resume | [RESUME.md](references/RESUME.md) |
| Doctor + autonomous recovery | [RECOVERY.md](references/RECOVERY.md) |
| Mined gold-standard prompts | [PROMPTS.md](references/PROMPTS.md) |
| Anti-patterns (long form) | [ANTI_PATTERNS.md](references/ANTI_PATTERNS.md) |
| Health vs status vs index nuance | [OBSERVABILITY.md](references/OBSERVABILITY.md) |
| Pages encrypted archive + HTML export | [PAGES_AND_EXPORT.md](references/PAGES_AND_EXPORT.md) |
| Harness exclusion (`disabled_agents`) | [HARNESS_EXCLUSION.md](references/HARNESS_EXCLUSION.md) |
| Schema introspection contracts | [INTROSPECTION.md](references/INTROSPECTION.md) |

---

## Quick Search (Grep Recipes for References)

When the right reference isn't obvious from titles, grep the references directory directly — cheaper than loading whole files into context.

```bash
REFS=.claude/skills/cass/references

# Find any anti-pattern by symptom keyword
grep -ni "limit 0\|broken pipe\|workspace path\|stale" "$REFS"/ANTI_PATTERNS.md "$REFS"/PITFALLS.md

# Find the recipe / jq for a task
grep -niE "ritual|user prompt|aggregate|subagent|cluster|timeline" "$REFS"/RECIPES.md "$REFS"/PATTERNS.md

# Find a recovery recipe (issue numbers, error strings, fix names)
grep -niE "doctor|--force-rebuild|issue #196|last_indexed_at|database is busy|core\." "$REFS"/RECOVERY.md "$REFS"/OBSERVABILITY.md

# Find a flag, command, or response field
grep -niE "robot-format|--mode|--cursor|_meta|fallback_mode|hits_clamped" "$REFS"/COMMANDS.md "$REFS"/INTROSPECTION.md

# Find a real "what did I ask" prompt template you've used before
grep -ni "use cass\|find that\|session history\|what worked" "$REFS"/PROMPTS.md

# Find harness/connector slugs and exclusion behavior
grep -niE "openclaw|disabled_agents|sources agents" "$REFS"/HARNESS_EXCLUSION.md "$REFS"/REMOTE_SOURCES.md

# Find resume / cross-harness behavior
grep -niE "resume|--shell|--exec|subagent.*not resumable" "$REFS"/RESUME.md
```

These grep across the whole references directory in <50ms and surface a line+filename that you can then open with the Read tool — far cheaper than reading the whole reference.

---

## Scripts

Scripts live under `scripts/`. They contribute zero context tokens — they execute, never load. None of them mutate state without explicit confirmation.

| Script | Usage |
|--------|-------|
| `./scripts/quick_analysis.sh /path` | One-command project overview (status → aggregate agent/date → top prompts) |
| `./scripts/prompt_miner.py --workspace /path` | Find repeated prompts (ritual detection) |
| `./scripts/validate.sh` | Validate cass install + skill structure |
| `./scripts/recover.sh` | Autonomous recovery decision tree (READY → STALE_BUT_USABLE → BROKEN); safe by default. Use as a `PreToolUse` hook before `cass search`. Wraps every `cass index` call in `timeout` to dodge issue #196 hangs |
| `./scripts/multi_machine_search.sh "QUERY" [host…]` | Parallel fan-out across the fleet (defaults to css/csd/ts1/ts2); merges hits, dedups by source_path:line, sorts by score. Per-host `timeout` cap; safe re: shell-special query chars |

---

## Validation

```bash
# Quick health check
cass status --json | jq '.index.fresh'

# Should return: true
```

If `false`, run: `cass index --json`
