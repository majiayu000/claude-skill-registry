---
name: audit
description: Full-sweep quality audit of .claude/ config — cross-references, permissions, inventory drift, model tiers, docs freshness, and upgrade proposals. Reports by severity; auto-fixes at the requested level — 'fix high' (critical+high), 'fix medium' (critical+high+medium), 'fix all' (all findings including low); 'upgrade' applies docs-sourced improvements with correctness verification and calibrate A/B testing for capability changes.
argument-hint: '[agents|skills] [fix [high|medium|all]] | upgrade'
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Agent, TaskCreate, TaskUpdate, WebFetch
---

<objective>

Run a full-sweep quality audit of the `.claude/` configuration: every agent file, every skill file, settings.json, and hooks. Spawns `self-mentor` for per-file analysis, then aggregates findings system-wide to catch issues that only surface across files — infinite loops, inventory drift, missing permissions, and cross-file interoperability breaks. Reports all findings and auto-fixes at the requested level: `fix high` (critical+high only), `fix medium` (critical+high+medium, default fix level), or `fix all` (all findings including low).

</objective>

<inputs>

- **$ARGUMENTS**: optional
  - No argument: full sweep, report only — lists all findings, no changes made (default)
  - `fix high` — fix `critical` and `high` findings; `medium` and `low` reported only
  - `fix medium` — fix `critical`, `high`, and `medium` findings; `low` reported only
  - `fix all` — fix all findings including `low`
  - `fix` (no level) — alias for `fix medium` (backward compatible)
  - `agents` — restrict sweep to agent files only, report only
  - `skills` — restrict sweep to skill files only, report only
  - Scope and fix level can be combined: `agents fix medium`, `skills fix all` — scope always precedes `fix`
  - `upgrade` — fetch latest Claude Code docs, filter new features by genuine value, then apply: **config** changes (apply + correctness check), **capability** changes (calibrate before → apply → calibrate after → accept if Δrecall ≥ 0 and ΔF1 ≥ 0). Skip to **Mode: upgrade**.

</inputs>

<workflow>

**Task tracking**: per CLAUDE.md, create tasks (TaskCreate) for each major phase and mark status live so the user can see progress in real time:

- Phase 1: setup + collect (Pre-flight + Steps 1–2) → mark in_progress when starting, completed when file list is ready
- Phase 2: per-file audit (Step 3) → mark in_progress when agents launch, completed when all reports received
- Phase 3: system-wide checks (Step 4) → mark in_progress when checks start, completed when all checks done
- Phase 4: aggregate + fix (Steps 5–9) → mark in_progress, then completed when fixes land
- Phase 5: final report (Step 10) → mark in_progress, then completed before output
- On loop retry or scope change → create a new task; do not reuse the completed task

Surface progress to the user at natural milestones: after system-wide checks ("✓ Checks 1-11 complete, N findings so far — spawning per-file audits"), after agent reports ("Agent reports received — N medium, N low findings"), and before each fix batch ("Fixing N medium findings in parallel").

## Pre-flight checks

```bash
RED='\033[1;31m'; YEL='\033[1;33m'; GRN='\033[0;32m'; NC='\033[0m'

# From _shared/preflight-helpers.md — TTL 4 hours, keyed per binary
preflight_ok()  { local f=".claude/state/preflight/$1.ok"; [ -f "$f" ] && [ $(( $(date +%s) - $(cat "$f") )) -lt 14400 ]; }
preflight_pass(){ mkdir -p .claude/state/preflight; date +%s > ".claude/state/preflight/$1.ok"; }

# .claude/ directory must exist (not cached — filesystem state)
if [ ! -d ".claude" ]; then
  printf "${RED}! BREAKING${NC}: .claude/ directory not found — nothing to audit\n"
  exit 1
fi

# jq availability — Check 6 depends on it
if preflight_ok jq; then
  JQ_AVAILABLE=true
elif command -v jq &>/dev/null; then
  preflight_pass jq; JQ_AVAILABLE=true
else
  printf "${YEL}⚠ MISSING${NC}: jq not found — Check 6 (permissions-guide drift) will be skipped\n"
  JQ_AVAILABLE=false
fi

# git availability — used in path portability check and baseline context
if ! preflight_ok git && ! command -v git &>/dev/null; then
  printf "${YEL}⚠ MISSING${NC}: git not found — path portability check may miss repo-root references\n"
else
  preflight_ok git || preflight_pass git
fi
```

If `.claude/` is missing, abort immediately. Missing `jq` is a warning — the audit continues with Check 6 skipped.

## Step 1: Run pre-commit (if configured)

```bash
# Check whether pre-commit is installed and a config exists
if (preflight_ok pre-commit || { command -v pre-commit &>/dev/null && preflight_pass pre-commit; }) \
    && [ -f .pre-commit-config.yaml ]; then
  pre-commit run --all-files
fi
```

Any files auto-corrected by pre-commit hooks (formatters, linters, whitespace fixers) are now clean before the structural audit begins. Note which files were modified — include them in the audit scope even if they were not originally targeted.

If pre-commit is not configured, skip this step silently.

## Step 2: Collect all config files

Enumerate everything in scope using built-in tools:

- **Agents**: Glob tool, pattern `agents/*.md`, path `.claude/`
- **Skills**: Glob tool, pattern `skills/*/SKILL.md`, path `.claude/`
- **Settings**: Read tool on `.claude/settings.json`
- **Hooks**: Glob tool, pattern `hooks/*`, path `.claude/`

Record the full file list — this becomes the audit scope for Steps 3–4. Cross-reference checks in Step 3 depend on this inventory being current. If MEMORY.md has not been updated since the last agent or skill was added or removed, run a live disk scan now rather than relying on the cached roster. Stale inventory is the primary cause of false-negative cross-reference findings.

## Step 3: Per-file audit via self-mentor

**Context management** — with 12+ agents and 14+ skills, accumulating full self-mentor responses in context causes overflow before aggregation. Use file-based findings to keep the main context lean.

Set up the run directory once before spawning any agents:

```bash
RUN_DIR="/tmp/audit-$(date +%s)"
mkdir -p "$RUN_DIR"
echo "Run dir: $RUN_DIR"
```

Spawn one **self-mentor** agent per file (or batch into groups of up to 10 for efficiency). The spawn prompt for each agent must:

1. Include the content from `.claude/skills/audit/templates/self-mentor-prompt.md`
2. Include the disk inventory from Step 2 (agent/skill list for cross-reference validation)
3. End with:

> "Write your FULL findings (all severity levels, Confidence block) to `<RUN_DIR>/<file-basename>.md` using the Write tool — where `<file-basename>` is the filename only (e.g. `oss-maintainer.md`, `audit-SKILL.md`). Then return to the caller ONLY a one-line summary: `<filename>: N critical, N high, N medium, N low [confidence 0.N]` — nothing else in your response."

Replace `<RUN_DIR>` with the actual directory path and `<file-basename>` with just the filename.

After all spawns complete, you will have a list of short summaries in context. Use these to identify which files have findings. The full content is in the run directory files.

## Step 4: System-wide checks

Beyond per-file analysis, run cross-file checks that self-mentor cannot do alone:

Run the following checks. For file-listing steps use Glob; for content-search steps use Grep. Bash is only needed for the pipeline comparisons and the `printf`/`jq` blocks below.

**Check 1 — Inventory drift (MEMORY.md vs disk)**
Use Glob (`agents/*.md`, path `.claude/`) to list agent files; extract basenames and sort, then write to `/tmp/agents_disk.txt` via Bash:

```bash
ls .claude/agents/*.md 2>/dev/null | xargs -n1 basename 2>/dev/null | sed 's/\.md$//' | sort > /tmp/agents_disk.txt || true
```

Read the `- Agents:` and `- Skills:` roster lines from the MEMORY.md content injected in the conversation context (available as auto-memory at session start). Do not attempt to Grep a file path — the MEMORY.md is not stored under `.claude/` but in Claude Code's auto-memory system. Repeat with Glob (`skills/*/`, path `.claude/`) for skills on disk — write to `/tmp/skills_disk.txt`.

**Check 2 — README vs disk**
Use Grep tool (pattern `^\| \*\*`, file `README.md`, output mode `content`) to extract agent/skill table rows.

**Check 3 — settings.json permissions**
Use Grep tool (pattern `gh |python -m|ruff|mypy|pytest`, glob `skills/*/SKILL.md`, path `.claude/`, output mode `content`) to collect bash commands used in skills.

**Check 4 — Orphaned follow-up references**
Use Grep tool (pattern `` `/[a-z-]*` ``, glob `skills/*/SKILL.md`, path `.claude/`, output mode `content`) to find skill-name references; compare against disk inventory.

**Check 5 — Hardcoded user paths**
Use Grep tool (pattern `/Users/|/home/`, glob `{agents/*.md,skills/*/SKILL.md}`, path `.claude/`, output mode `content`) to flag non-portable paths in agent and skill files. Then run a second Grep directly on `.claude/settings.json` with the same pattern to catch absolute hook paths in the settings file.

**Important**: run this check on every file regardless of whether critical or high findings were already found — path portability issues are orthogonal to other severity classes and must not be deprioritized due to presence of more serious findings in the same file.

**Check 6 — permissions-guide.md drift** — every allow entry must appear in the guide, and vice versa

```bash
RED='\033[1;31m'; YEL='\033[1;33m'; GRN='\033[0;32m'; NC='\033[0m'
if [ "${JQ_AVAILABLE:-false}" = "false" ] || ! command -v jq &>/dev/null; then
  printf "${YEL}⚠ SKIPPED${NC}: Check 6 — jq not available\n"
elif [ ! -f ".claude/settings.json" ]; then
  printf "${YEL}⚠ SKIPPED${NC}: Check 6 — .claude/settings.json not found\n"
elif [ ! -f ".claude/permissions-guide.md" ]; then
  printf "${YEL}⚠ SKIPPED${NC}: Check 6 — .claude/permissions-guide.md not found\n"
else
  # Allow entries missing from guide
  jq -r '.permissions.allow[]' .claude/settings.json 2>/dev/null | \
  while IFS= read -r perm; do
    grep -qF "\`$perm\`" .claude/permissions-guide.md 2>/dev/null \
      || printf "${YEL}⚠ MISSING from guide${NC}: %s\n" "$perm"
  done

  # Guide entries orphaned (not in allow list)
  grep '^| `' .claude/permissions-guide.md 2>/dev/null | awk -F'`' '{print $2}' | \
  while IFS= read -r perm; do
    jq -e --arg p "$perm" '(.permissions.allow // []) + (.permissions.deny // []) | contains([$p])' .claude/settings.json > /dev/null 2>&1 \
      || printf "${YEL}⚠ ORPHANED in guide${NC}: %s\n" "$perm"
  done
fi
```

**Check 6b — Permission safety audit** — every `allow` entry must be non-destructive, reversible, and local-only

Read `.claude/settings.json` using the Read tool and extract the `permissions.allow` list. For each entry, use model reasoning to evaluate it against three criteria:

- **Non-destructive**: does not permanently delete or overwrite data (no `rm -rf`, `git push --force`, `DROP TABLE`)
- **Reversible**: effect can be undone without data loss (local file edits, test runs, read-only queries)
- **Local-only**: does not affect systems outside the working directory or send data to external services

Flag destructive patterns as **critical** (auto-approved destructive commands are always a breaking safety failure). Flag external-state mutations as **high** and raise to user — some (e.g., `gh release create`) may be intentional but must be explicitly acknowledged.

**Check 7 — Skill frontmatter conflicts** — `context:fork + disable-model-invocation:true` is a broken combination: a forked skill has no model to coordinate agents or synthesize results.

```bash
RED='\033[1;31m'; YEL='\033[1;33m'; GRN='\033[0;32m'; CYN='\033[0;36m'; NC='\033[0m'
for f in .claude/skills/*/SKILL.md; do
  name=$(basename "$(dirname "$f")")
  if awk '/^---$/{c++} c<2' "$f" 2>/dev/null | grep -q 'context: fork' && \
     awk '/^---$/{c++} c<2' "$f" 2>/dev/null | grep -q 'disable-model-invocation: true'; then
    printf "${RED}! BREAKING${NC} skills/%s: context:fork + disable-model-invocation:true\n" "$name"
    printf "  ${RED}→${NC} forked skill has no model to coordinate agents or synthesize results\n"
    printf "  ${CYN}fix${NC}: remove disable-model-invocation:true (or remove context:fork if purely tool-only)\n"
  fi
done
```

Flag any drift between MEMORY.md, README.md, settings.json, and actual disk state. Flag any hardcoded `/Users/` or `/home/` paths — these should be `.claude/`, `~/`, or `$(git rev-parse --show-toplevel)/` style. Flag any permissions-guide.md entries not in the allow list (orphaned docs) or allow entries without a guide row (undocumented permissions).

**Check 8 — Model tier appropriateness**

Three capability tiers define the expected model assignment for each agent:

| Tier                | Profile                                                     | Current mapping     |
| ------------------- | ----------------------------------------------------------- | ------------------- |
| `plan-gated`        | Long-horizon reasoning, plan mode, governance               | `opusplan`          |
| `deep-reasoning`    | Complex implementation, multi-file code gen, judgment calls | `opus`              |
| `focused-execution` | Pattern matching, structured output, rule application       | `sonnet` or `haiku` |

Extract declared models with Bash:

```bash
printf "%-30s %s\n" "AGENT" "MODEL"
for f in .claude/agents/*.md; do
  name=$(basename "$f" .md)
  model=$(awk '/^---$/{c++; if(c==2)exit} c==1 && /^model:/{sub(/^model: /,""); print}' "$f")
  printf "%-30s %s\n" "$name" "${model:-(inherit)}"
done
```

Using model reasoning, classify each agent into a tier based on its `<role>`, `description`, and workflow body content. Cross-reference the classified tier against the declared model:

- `focused-execution` agent using `opus` or `opusplan` → **medium** (potential overkill — may increase latency and cost without quality gain)
- `deep-reasoning` agent using `sonnet` → **high** (likely underpowered for multi-file code gen or complex judgment)
- `plan-gated` agent using `sonnet` → **high** (plan mode requires strong long-horizon reasoning)
- `focused-execution` agent using `haiku` → **not a finding** — haiku is acceptable and economical for narrow/rule-based tasks

**Important**: CLAUDE.md's `## Agent Teams` section specifies models for team-mode spawn instructions to the lead — it is NOT a mandate for agent frontmatter. Frontmatter `model:` governs standalone use. Do NOT flag frontmatter models as violations because they differ from CLAUDE.md's team-mode model spec.

**Report only** — never auto-fix. Model assignments may be intentional trade-offs (e.g., cost sensitivity, latency constraints). Flag mismatches with rationale so the user can decide.

**Time-resilience note**: when new model tiers or model aliases arrive, update only the tier-to-model mapping table above. The tier classification heuristic (what each agent does) is model-agnostic.

### Tool efficiency

For each agent and skill, validate that declared tools match actual usage — no unnecessary permissions, no missing tools.

**Mechanical check** — for each skill, cross-reference `allowed-tools:` frontmatter against tool names referenced in the workflow body:

```bash
RED='\033[1;31m'; YEL='\033[1;33m'; GRN='\033[0;32m'; CYN='\033[0;36m'; NC='\033[0m'
for f in .claude/skills/*/SKILL.md; do
  name=$(basename "$(dirname "$f")")
  declared=$(awk '/^---$/{c++; if(c==2)exit} c==1 && /^allowed-tools:/{sub(/^allowed-tools: /,""); print}' "$f")
  body=$(awk '/^---$/{c++} c>=2{print}' "$f")
  for tool in Read Write Edit Bash Grep Glob TaskCreate TaskUpdate WebFetch WebSearch; do
    in_body=$(echo "$body" | grep -cw "$tool" || true)
    in_decl=$(echo "$declared" | grep -cw "$tool" || true)
    if [ "$in_body" -gt 0 ] && [ "$in_decl" -eq 0 ]; then
      printf "${YEL}⚠ MISSING tool${NC}: skills/%s references %s but not in allowed-tools\n" "$name" "$tool"
    fi
    if [ "$in_body" -eq 0 ] && [ "$in_decl" -gt 0 ]; then
      printf "${YEL}⚠ UNUSED tool${NC}:  skills/%s declares %s but workflow never references it\n" "$name" "$tool"
    fi
  done
done
```

**Semantic check** (model reasoning) — review each agent's `tools:` frontmatter against its declared domain and workflow:

- `WebFetch`/`WebSearch` declared for an agent whose domain has no web-research component → **medium** (unnecessary permission surface)
- `Write`/`Edit` declared for a read-only agent (e.g., `solution-architect`) but not used in practice → **medium**
- `Bash` absent for an agent whose domain involves running code (linting, Continuous Integration (CI) validation, performance profiling) → **high** (silent failure when workflow invokes shell commands)
- `Task` absent for an orchestrating agent that needs to spawn subagents → **high**
- `tools:` is `*` (wildcard) for a focused domain agent — prefer an explicit list → **low**

Report missing necessary tools as **high**; declared-but-unused tools as **medium**.

### Purpose overlap review

Read all agent/skill descriptions together and flag pairs where:

- Two agents have substantially overlapping domains (risk: users don't know which to pick)
- A skill's workflow duplicates logic already owned by an agent it could simply spawn
- An agent has grown so broad its scope is unclear (candidate for splitting)

### CLAUDE.md consistency

`.claude/CLAUDE.md` is the master governance file; agent and skill instructions must not contradict it.

Read `.claude/CLAUDE.md` and extract its governance directives (Workflow Orchestration, Task Management, Self-Setup Maintenance, Communication, Core Principles). For each agent and skill file, check whether any instruction contradicts or undermines a CLAUDE.md directive:

- **Direct contradiction**: file says the opposite of what CLAUDE.md mandates (e.g., "skip planning" vs "enter plan mode for non-trivial tasks")
- **Missing required behavior**: file performs an action governed by Self-Setup Maintenance rules but omits the required steps (e.g., modifies `.claude/` files without mentioning cross-reference updates)
- **Tone/style mismatch**: file's communication guidance conflicts with the Communication section (e.g., "apologize to the user" vs "flag early, not late")

Major contradictions → **high** severity, raised to user (CLAUDE.md takes precedence — the agent/skill needs updating, but the user decides how).
Minor drift (slightly different wording of the same idea, or missing but not contradicting) → **low**.

- **Direct contradiction** includes explicit instructions to skip a required behavior (e.g., "Do not create task tracking entries" contradicts the Task Management directive as directly as saying "never track tasks"). The test is whether a reasonable reader would interpret the instruction as overriding the CLAUDE.md mandate — if yes, it is high; if the file simply does not mention the behavior, it is low (omission).

Also audit CLAUDE.md itself for **scope creep** — content that is too specific to belong in a universal governance file:

- **Domain-specific output formats** (e.g., a structured findings template that only one skill uses) → **medium**: move to the relevant agent/skill file; CLAUDE.md governs all agents, so its Output Standards should be universal (Confidence block, Internal Quality Loop) not skill-specific.
- **Skill-specific rules or antipatterns** (e.g., review consolidation rules, release checklist items) → **medium**: these belong in the skill's own SKILL.md or checklist file, not in the master governance file.
- **Project-specific details that don't generalise** (specific tool versions, project-local paths, one-off workflow notes) → **low**: prefer agent instructions or MEMORY.md for project-local context; CLAUDE.md is synced to `~/.claude/` and must work across all projects without modification.

The test: would a reasonable reader expect this content to apply to every single agent in every project? If no → it doesn't belong in CLAUDE.md.

### Claude Code docs freshness

Spawn a **web-explorer** agent to fetch the current Claude Code documentation. Try the direct paths below; if they don't resolve, navigate from the Claude Code homepage (`code.claude.com`) to find the current schema pages.

**File-based handoff**: the web-explorer agent must write its full findings (validated fields, deprecated fields, new features, upgrade proposals with genuine-value assessment) to `$RUN_DIR/docs-freshness.md` using the Write tool. Return ONLY a summary line: `findings=N deprecated=N new_features=N confidence=0.N` — nothing else in the response.

- Hook event names, types, and schemas — `code.claude.com/docs/en/hooks`
- Agent frontmatter schema — `code.claude.com/docs/en/sub-agents`
- Skill frontmatter schema — `code.claude.com/docs/en/skills`

With the fetched docs, validate the local config:

**Hook validation** (`settings.json`):

- Every hook event name (e.g. `SubagentStart`) exists in the documented event list
- Every hook `type` is one of `command`, `http`, `prompt`, `agent`
- No deprecated top-level `decision:`/`reason:` fields in PreToolUse hooks
  (correct form is `hookSpecificOutput.permissionDecision`)

**Agent frontmatter validation** (`.claude/agents/*.md`):

- All frontmatter fields are in the documented schema
  (`name`, `description`, `tools`, `disallowedTools`, `model`, `permissionMode`,
  `maxTurns`, `skills`, `mcpServers`, `hooks`, `memory`, `background`, `isolation`,
  `color` — note: `color` is a Claude Code UI extension not in the public schema)
- `model` values are recognized short-names (`sonnet`, `opus`, `haiku`, `inherit`,
  or project-level aliases like `opusplan`)

**Skill frontmatter validation** (`.claude/skills/*/SKILL.md`):

- All frontmatter fields are in the documented schema
  (`name`, `description`, `argument-hint`, `disable-model-invocation`,
  `user-invocable`, `allowed-tools`, `model`, `context`, `agent`, `hooks`)

**Improvement opportunities** — collect documented features not yet in use:

- New hook events that could add value (e.g. `PreCompact`, `SessionEnd`, `Stop`)
- New agent frontmatter fields (e.g. `memory`, `isolation`, `maxTurns`, `background`)
- New skill frontmatter fields (e.g. `context: fork`, `model`, `hooks`)
- New settings keys (e.g. `sandbox`, `plansDirectory`, `alwaysThinkingEnabled`)

Findings classification:

- Deprecated/invalid hook event name or type in use → **high**
- Deprecated frontmatter field, deprecated settings key, unrecognized model ID → **medium**
- New documented feature not yet used → evaluate with genuine-value filter and add to **Upgrade Proposals** table (not a LOW finding)

**Upgrade Proposals** — for each new feature, apply the genuine-value filter before adding: "Does this solve a demonstrated problem in the current setup, or add measurable capability?" Omit features that add complexity without evidence of need. Classify passing candidates:

- **config**: settings, hooks, frontmatter metadata — low risk, verified by correctness check only
- **capability**: agent instructions, skill workflow changes — higher risk, requires calibrate A/B

Cap at 5 proposals per run; if more pass the filter, rank by expected impact and take the top 5.

| #                                                                         | Feature | Type | Target | Rationale | A/B plan |
| ------------------------------------------------------------------------- | ------- | ---- | ------ | --------- | -------- |
| (filled at runtime — omit table entirely if no proposals pass the filter) |         |      |        |           |          |

**Check 9 — Example value vs. token cost**

First, detect whether the project has local context files that reduce the need for generic examples:

```bash
for f in AGENTS.md CONTRIBUTING.md .claude/CLAUDE.md; do
  [ -f "$f" ] && printf "✓ found: %s\n" "$f"
done
```

Then scan agent and skill files for inline examples:

````bash
for f in .claude/agents/*.md .claude/skills/*/SKILL.md; do
  count=$(grep -cE '^```|^## Example|^### Example' "$f" 2>/dev/null || true)
  lines=$(wc -l < "$f" | tr -d ' ')
  [ "$count" -gt 0 ] && printf "%s: %d example blocks, %d total lines\n" "$f" "$count" "$lines"
done
````

Using model reasoning, evaluate each file's examples against two criteria:

1. **Necessity**: does the example demonstrate something that prose alone cannot — a nuanced judgment call, a non-obvious output format, a complex multi-step pattern? Or does it just restate the surrounding paragraph in code?
2. **Project fit**: if the project has `AGENTS.md` or `CONTRIBUTING.md`, project-specific examples in agent files compete with or duplicate that local context — flag as low-value unless the example is domain-specific to the agent's specialty.

Classify each example block:

- **High-value**: non-obvious pattern, nuanced judgment, or output-format spec that prose cannot convey → keep
- **Low-value**: restates prose, trivial, or superseded by project-local docs → **low** finding: suggest removing or replacing with a pointer to the local doc

Report per-file: `N examples total, K high-value, M low-value (est. ~X tokens wasted)`.

**Check 10 — Agent color drift (statusline COLOR_MAP vs frontmatter)**

Each agent declares a `color:` in its frontmatter. `hooks/statusline.js` maps those color names to ANSI codes via a `COLOR_MAP` object. If a color name is added to an agent but not to `COLOR_MAP`, the statusline silently falls back to no color. Verify alignment:

```bash
# Extract color: values declared in agent frontmatter
for f in .claude/agents/*.md; do
  name=$(basename "$f" .md)
  color=$(awk '/^---$/{c++; if(c==2)exit} c==1 && /^color:/{sub(/^color: */,""); print}' "$f")
  [ -n "$color" ] && printf "%s: %s\n" "$name" "$color"
done
```

Using model reasoning, cross-reference each extracted color name against the `COLOR_MAP` keys in `.claude/hooks/statusline.js`. Flag any mismatch:

- Color declared in agent frontmatter but **not a key in `COLOR_MAP`** → **medium** (agent will appear uncolored in statusline)
- Color in `COLOR_MAP` that is **not declared by any agent** → **low** (dead mapping, no functional impact)

Note: `COLOR_MAP` may intentionally include extra entries (future-proofing); flag only the agent-declared-but-missing case as actionable.

**Check 11 — Memory health (MEMORY.md noise accumulation)**

MEMORY.md has a 200-line truncation limit. Noise accumulates silently over time — duplicate rules, stale version pins, and absorbed feedback files all erode the budget without adding information. Run three sub-checks:

**11a — Duplicate with CLAUDE.md**: Read both MEMORY.md and CLAUDE.md. For each section in MEMORY.md, check whether the same rule or directive exists verbatim or near-verbatim in CLAUDE.md. Flag duplicates as **low** — one source of truth is enough; the MEMORY.md copy adds context-window cost with no benefit.

**11b — Stale version pins**: Scan MEMORY.md for lines containing pinned semver values (e.g. `v0.15.2`, `v1.19.1`) or "as of [month year]" staleness markers. Flag each as **low** — pinned versions age within weeks; the actionable rule (e.g. "always run `pre-commit autoupdate`") should survive, the specific version should not.

```bash
# Find lines with semver pins or "as of" staleness markers in MEMORY.md
MEMORY_FILE="$HOME/.claude/projects/$(git rev-parse --show-toplevel | sed 's|/|-|g')/memory/MEMORY.md"
if [ -f "$MEMORY_FILE" ]; then
  grep -nE '(v[0-9]+\.[0-9]+\.[0-9]+|as of [A-Z][a-z]+ 20[0-9]{2})' "$MEMORY_FILE" || echo "no stale pins found"
else
  printf "${YEL}⚠ SKIPPED${NC}: Check 11b — MEMORY.md not found at derived path: %s\n" "$MEMORY_FILE"
fi
```

**11c — Absorbed feedback files**: List all `feedback_*.md` files in the memory directory. For each, read its content and check whether the rule it documents is already present in MEMORY.md or in the relevant agent/skill file. If yes, flag as **low** (delete the feedback file — the lesson is absorbed).

```bash
MEMORY_DIR="$HOME/.claude/projects/$(git rev-parse --show-toplevel | sed 's|/|-|g')/memory"
if [ -d "$MEMORY_DIR" ]; then
  ls "$MEMORY_DIR"/feedback_*.md 2>/dev/null || echo "no feedback files"
else
  printf "${YEL}⚠ SKIPPED${NC}: Check 11c — memory dir not found: %s\n" "$MEMORY_DIR"
fi
```

All three sub-checks produce only **low** findings — auto-fixed under `/audit fix all`; reported only under `/audit fix` or lower. Fix action: remove the duplicate section, drop the version pin (keep the surrounding rule), delete the absorbed feedback file.

**Check 12 — Agent description routing alignment**

Three sub-checks, all using model reasoning over extracted agent descriptions. These are **report-only** — never auto-fix; descriptions are semantic and require human judgment.

First, extract all agent descriptions:

```bash
printf "%-25s %s\n" "AGENT" "DESCRIPTION"
for f in .claude/agents/*.md; do
  name=$(basename "$f" .md)
  desc=$(awk '/^---$/{c++; if(c==2)exit} c==1 && /^description:/{sub(/^description: /,""); print}' "$f")
  printf "%-25s %s\n" "$name" "$desc"
done
```

Apply model reasoning to the collected descriptions:

**12a — Overlap analysis**: For each pair of agents, assess domain overlap. Flag pairs where a reasonable orchestrator could confuse which agent to pick — i.e., given a task in the overlap zone, the descriptions alone do not disambiguate. Each ambiguous pair → **medium** finding.

**12b — NOT-for clause coverage**: For each high-overlap pair found in 12a, check whether at least one agent in the pair has a "NOT for" / "not for" / exclusion clause in its description that references the other or its domain. Missing disambiguation → **medium**.

**12c — Trigger phrase specificity**: For each agent, check whether the description's first clause states an exclusive domain not shared with any other agent. A vague opener that doesn't immediately distinguish this agent from its nearest neighbor → **low**.

Severity: 12a/12b = **medium**; 12c = **low**. Fix reference: run `/calibrate routing` to verify whether description overlap translates to actual routing confusion, then refine descriptions accordingly.

**Check 13 — Codex integration smoke-test**

Skip if codex is not installed (`command -v codex` returns non-zero).

```bash
RED='\033[1;31m'; GRN='\033[0;32m'; YEL='\033[1;33m'; NC='\033[0m'
if ! command -v codex &>/dev/null; then
  printf "${YEL}⚠ SKIPPED${NC}: Check 13 — codex not installed\n"
else
  SMOKE_FILE="/tmp/audit-codex-smoke-$$.py"
  SMOKE_OUT="/tmp/audit-codex-smoke-$$.out"
  # Run a trivial generation task: write a function that checks if n is prime
  codex exec "Write a Python function is_prime(n: int) -> bool that returns True if n is prime. Put it in $SMOKE_FILE. Include a quick sanity-check: assert is_prime(7) and not is_prime(4)." \
    --sandbox workspace-write 2>"$SMOKE_OUT"
  EXIT=$?
  if [ $EXIT -ne 0 ]; then
    printf "${RED}! BREAKING${NC}: Check 13 — codex exec exited with code %d\n" "$EXIT"
    printf "  stderr: %s\n" "$(tail -5 $SMOKE_OUT)"
  elif [ ! -f "$SMOKE_FILE" ]; then
    printf "${RED}! BREAKING${NC}: Check 13 — codex ran but produced no output file\n"
  else
    # Basic output review: file must contain 'def is_prime', at least 3 lines, no syntax error
    HAS_DEF=$(grep -c 'def is_prime' "$SMOKE_FILE" || true)
    LINES=$(wc -l < "$SMOKE_FILE" | tr -d ' ')
    python3 -m py_compile "$SMOKE_FILE" 2>"$SMOKE_OUT"
    SYNTAX=$?
    if [ "$HAS_DEF" -lt 1 ] || [ "$LINES" -lt 3 ] || [ "$SYNTAX" -ne 0 ]; then
      printf "${RED}! BREAKING${NC}: Check 13 — codex output failed review (def_found=%s lines=%s syntax_ok=%s)\n" \
        "$HAS_DEF" "$LINES" "$([ $SYNTAX -eq 0 ] && echo yes || echo no)"
      printf "  output: %s\n" "$(head -5 $SMOKE_FILE)"
    else
      printf "${GRN}✓ OK${NC}: Check 13 — codex integration live (generated %d-line function, syntax valid)\n" "$LINES"
    fi
  fi
  rm -f "$SMOKE_FILE" "$SMOKE_OUT"
fi
```

- Codex not installed → **skipped** (not a finding)
- Codex exits non-zero or produces no file → **critical** (integration broken; `/codex` skill will silently fail)
- Output file missing `def is_prime` or fails `py_compile` → **high** (codex running but producing invalid output)
- All checks pass → logged as `✓ OK`, no finding

## Step 5: Aggregate and classify findings

**Delegate aggregation to a consolidator agent** to avoid flooding the main context with all agent findings. Spawn a **self-mentor** consolidator agent with this prompt:

> "Read all finding files in `<RUN_DIR>/` (\*.md files from Steps 3–4, including `docs-freshness.md` if present). Apply the severity classification from `.claude/skills/audit/severity-table.md`. Antipatterns that indicate severity under-classification are also in that file. Group all findings by severity (critical, high, medium, low). Apply the one-finding-per-issue rule: when a single location has multiple distinct problems at different severities, emit one finding entry per problem. Write the aggregated severity table to `<RUN_DIR>/aggregate.md` using the Write tool. Return ONLY a one-line summary: `findings=N critical=N high=N medium=N low=N`"

Main context receives only that one-liner for the Step 7 report structure. Read `<RUN_DIR>/aggregate.md` only if you need to display specific finding details in Step 7.

## Step 6: Cross-validate critical findings

Read and follow the cross-validation protocol from `.claude/skills/_shared/cross-validation-protocol.md`.

**Skill-specific**: the verifier agent is always **self-mentor**.

## Step 7: Report findings

Output a structured audit report before fixing anything:

```
## Audit Report — .claude/ config

### Scope
- Agents audited: N
- Skills audited: N
- System-wide checks: inventory drift, README sync, permissions, infinite loops, hardcoded paths, CLAUDE.md consistency, docs freshness, permissions-guide drift, model tier appropriateness, agent color drift, memory health, agent routing alignment, codex integration smoke-test

### Findings by Severity

#### Critical (N)
| File | Line | Issue | Category |
|---|---|---|---|
| agents/foo.md | 42 | References `bar-agent` which does not exist on disk | broken cross-ref |

#### High (N)
...

#### Medium (N)
...

#### Low (N) — auto-fixed only with 'fix all'; otherwise reported only
...

### Summary
- Total findings: N (C critical, H high, M medium, L low)
- Auto-fix eligible: N per fix level — `fix high`: C+H | `fix medium`: C+H+M | `fix all`: C+H+M+L

### Upgrade Proposals (N — run `/audit upgrade` to apply)
| # | Feature | Type | Rationale |
|---|---------|------|-----------|
| 1 | ... | config | ... |

(omit this section entirely if no proposals passed the genuine-value filter)
```

If no fix level was passed, stop here and present the report.

## Step 8: Delegate fixes to subagents

Choose the fix agent based on file type:

- **`.claude/agents/*.md` and `.claude/skills/*/SKILL.md`** → spawn **self-mentor** — it has domain expertise in config quality and has `Write`/`Edit` tools
- **Code files** (`.py`, `.js`, `.ts`, etc.) → spawn **sw-engineer**

Spawn one agent per affected file, batching all findings for that file into a single subagent prompt. Issue **all spawns in a single response** for parallelism.

Each subagent prompt template: Read the fix prompt template from .claude/skills/audit/templates/fix-prompt.md and use it, filling in `<file path>` and the list of findings.

**Exceptions — handle inline without subagents (note in report):**

- **settings.json permission missing**: report only — structural JSON edits are risky to delegate
- **CLAUDE.md contradiction**: raise to user — do not auto-fix (CLAUDE.md takes precedence)
- **Dead loop**: flag for user review — requires human judgment on which link to break
- **Model tier mismatch**: report only — model assignments may be intentional for cost/latency trade-offs; user decides whether to adjust

After all subagents complete, collect their results and proceed to Step 9.

**Low findings** (nits): fix only when `fix all` was passed — otherwise collect in the final report for optional manual cleanup.

## Step 8b: Codex cross-file check

After all Step 8 fix agents complete and before self-mentor re-audit:

Read `.claude/skills/_shared/codex-prepass.md` and run the Codex pre-pass on the combined diff of all fixes.

Treat any findings as additional issues entering Step 9's re-audit scope. Skip if Step 8 touched only 1 file.

## Step 9: Re-audit modified files + confidence check

For every file changed in Step 8, spawn **self-mentor** again to confirm the fix resolved the finding and no new issues were introduced. Use the same file-based approach as Step 3 — write full re-audit findings to `<RUN_DIR>/<file-basename>-reaudit.md` and return only a one-line summary.

```bash
# Spot-check: confirm the previously broken reference no longer appears
grep -n "<broken-name>" <fixed-file>
```

**Confidence re-run**: parse each confidence score from the one-line summaries (Step 3) and re-audit summaries (Step 9). For any file where **Score < 0.7**:

1. Re-spawn self-mentor on that file with the specific gap from the `Gaps:` field addressed in the prompt (e.g., "pay special attention to async error paths — previous pass flagged this as a gap")
2. If confidence is still < 0.7 after one retry: flag to user with ⚠ and include the gap in the final report — do not silently drop it
3. Recurring low-confidence gaps (same gap on same file across multiple audit runs) → candidate for adding to self-mentor's `\<antipatterns_to_flag>` or the agent's own instructions

```bash
# Parse confidence scores from self-mentor outputs (regex on task result text)
# Score: 0.82  → extract 0.82
# Flag any < 0.7 for targeted re-run
```

If re-audit surfaces new issues, loop back to Step 8 for those findings only (max 2 re-audit cycles — escalate to user if still unresolved).

## Step 10: Final report

Output the complete audit summary:

```
## Audit Complete — .claude/ config

### Files Audited
- Agents: N | Skills: N | Settings: 1 | Hooks: N

### Findings
| Severity | Found | Fixed | Remaining |
|---|---|---|---|
| critical | N | N | 0 |
| high | N | N | 0 |
| medium | N | N | 0 |
| low | N | N (fix all only) | N |

### Fixes Applied
| File | Change |
|---|---|
| agents/foo.md | Replaced broken ref `old-agent` → `correct-agent` |

### Remaining (low/nits — auto-fixed only with 'fix all'; otherwise manual review optional)
- [low findings that were not auto-fixed]
- [any infinite loops flagged for user decision]

### Agent Confidence
| File | Score | Label | Gaps |
|------|-------|-------|------|
| agents/foo.md | 0.92 | high | — |
| skills/bar/SKILL.md | 0.64 | ⚠ low | no runtime data for bash validation |

Low-confidence files re-audited: N | Still uncertain after retry: N (see gaps above)

### Next Step
Run `/sync apply` to propagate clean config to ~/.claude/
```

## Mode: upgrade

**Trigger**: `/audit upgrade`

**Purpose**: Apply documented Claude Code improvements that passed the genuine-value filter. Config changes are applied and correctness-checked immediately. Capability changes are A/B tested via a mini calibrate pipeline — accepted only if Δrecall ≥ 0 and ΔF1 ≥ 0.

**Task tracking**: TaskCreate "Fetch upgrade proposals", "Apply config proposals", "A/B test capability proposals". Mark in_progress/completed throughout.

### Phase 1: Gate check

Before applying anything, verify the baseline is structurally sound:

```bash
# Check for the most likely breaking issue — frontmatter conflicts — without running the full audit
for f in .claude/agents/*.md .claude/skills/*/SKILL.md; do
  awk '/^---$/{c++} c<2' "$f" 2>/dev/null | grep -q 'context: fork' && \
  awk '/^---$/{c++} c<2' "$f" 2>/dev/null | grep -q 'disable-model-invocation: true' && \
  echo "BREAKING: $f — context:fork + disable-model-invocation:true"
done
```

If any critical or high issues are known from a recent `/audit` run, or the gate check above finds a BREAKING issue: stop and print "⚠ Resolve critical/high findings first (`/audit fix high`), then re-run `/audit upgrade`."

### Phase 2: Fetch and classify proposals

**Always spawn a fresh web-explorer** — do not use context from previous audit runs, cached docs, or memory. Every upgrade run must fetch live docs.

Run the **Claude Code docs freshness** check from Step 4 of the main audit workflow: spawn web-explorer, validate current config against latest docs, apply genuine-value filter, produce the Upgrade Proposals table. Cap at 5 total (max 3 capability, any number of config).

If no proposals pass the filter: print "✓ No upgrade proposals — current setup is current." and stop.

### Phase 3: Apply config proposals

Mark "Apply config proposals" in_progress. For each **config** proposal, in sequence:

1. Apply the change (Edit/Write tool)
2. Correctness check:
   ```bash
   # settings.json — JSON validity
   jq empty .claude/settings.json && echo "✓ valid JSON" || echo "✗ invalid JSON"
   # JS hook files — syntax check
   node --check .claude/hooks/*.js 2>&1 | grep -v '^$' || true
   ```
3. Accept (✓) if check passes; revert and mark rejected (✗) with reason if it fails

Mark "Apply config proposals" completed.

### Phase 4: A/B test capability proposals

Mark "A/B test capability proposals" in_progress. For each **capability** proposal (max 3), in sequence:

**Step a — Baseline calibration**: Read `.claude/skills/calibrate/templates/pipeline-prompt.md`. Spawn a `general-purpose` subagent using that template with the target agent name, domain, N=3, MODE=fast, AB_MODE=false. Capture `recall_before` and `f1_before` from the returned JSON.

**Step b — Apply change**: Edit the target agent file per the proposal spec.

**Step c — Post calibration**: Spawn the same pipeline subagent again with identical parameters. Capture `recall_after` and `f1_after`.

**Step d — Decision**:

- `Δrecall = recall_after − recall_before`
- `ΔF1 = f1_after − f1_before`
- **Accept** (✓) if Δrecall ≥ 0 AND ΔF1 ≥ 0 → keep the change
- **Revert** (✗) if either delta is negative → restore the file, record the deltas

Mark "A/B test capability proposals" completed.

### Phase 5: Report and sync

```
## Upgrade Complete — <date>

### Gate
[clean / issues found and stopped]

### Config Changes
| # | Feature | Target | Result | Notes |
|---|---------|--------|--------|-------|
| 1 | ... | hooks/task-log.js | ✓ accepted | jq valid |

### Capability Changes
| # | Feature | Target | Δrecall | ΔF1 | Result |
|---|---------|--------|---------|-----|--------|
| 1 | ... | agents/self-mentor.md | +0.04 | +0.02 | ✓ accepted |
| 2 | ... | agents/sw-engineer.md | −0.02 | +0.01 | ✗ reverted |

### Next Steps
- `/sync apply` — propagate accepted changes to ~/.claude/
- `/audit` — confirm clean baseline after upgrades
- Reverted items: run `/calibrate <agent> full` for deeper A/B signal (N=10 vs N=3 used here)
```

Run `/sync apply` automatically after all proposals are processed.

</workflow>

<notes>

- **`!` Breaking findings**: when a skill or agent is completely non-functional (check #7, broken cross-refs, invalid hook events), prefix the finding with `!` and state the impact + fix in one place — don't bury it as a table row. These surface as **`! BREAKING`** in bash output and as prominent callouts in the final report.
- **Terminal color conventions** (used in Step 4 bash output):
  - `RED` (`\033[1;31m`) — breaking/critical: `! BREAKING`, `ERROR`
  - `YELLOW` (`\033[1;33m`) — warnings/medium: `⚠ MISSING`, `⚠ ORPHANED`, `⚠ DIFFERS`
  - `GREEN` (`\033[0;32m`) — pass status: `✓ OK`, `✓ IDENTICAL`
  - `CYAN` (`\033[0;36m`) — source agent name or fix hint
- **Report before fix**: never silently mutate files — always present the findings report first (Step 7), then fix
- **settings.json is hands-off**: missing permissions are always reported, never auto-edited — structural JSON edits risk breaking Claude Code's config loading
- **Dead loops need human judgment**: a cycle in follow-up chains might be intentional (e.g., refactor → review → fix → refactor) — flag and explain, don't auto-remove
- **Max 2 re-audit cycles**: if fixes don't converge after 2 loops, surface the remaining issues to the user rather than spinning
- **Relationship to self-mentor**: `self-mentor` is a single-file reactive audit; `/audit` is the system-wide sweep that runs self-mentor at scale and adds cross-file checks
- `general-purpose` is a Claude Code built-in agent type (no `.claude/agents/general-purpose.md` file needed) — it provides a baseline Claude instance with access to all tools but no custom system prompt.
- **Paths must be portable**: `.claude/` for project-relative paths, `~/` or `$HOME/` for home paths — never a literal `/Users/` or `/home/` path; this rule applies to ALL config files including `settings.json`
- Pre-flight for `/sync` — run clean before `/sync apply`.
- **Bash error logging**: if a bash block in Pre-flight checks or Step 4 fails unexpectedly, append a JSONL line to `.claude/logs/audit-errors.jsonl` (`{"ts":"<ISO>","check":"<N>","error":"<message>"}`) for post-mortem — do not swallow errors silently.
- **Execution order tip**: Steps 1–2 and Step 4 bash checks are fast (seconds); Step 3 (self-mentor spawns) is expensive (seconds per file). For early signal on system-wide issues, run Steps 1–2 + Step 4 first, then spawn Step 3 agents in parallel with any Step 4 analysis that doesn't depend on per-file results.
- **Token cost**: Step 3 (self-mentor spawns) is the most expensive part of the audit. For a quick structural scan where you mainly need cross-reference and inventory validation, the system-wide checks in Step 4 are often sufficient on their own. Consider running `/audit agents` or `/audit skills` to scope the sweep, or skip Step 3 entirely for a fast pass when you already trust per-file quality.
- **Skill-creator complement**: For testing whether skill trigger descriptions fire correctly (trigger accuracy, A/B description testing), see the official skill-creator utility from Anthropic. `/audit` checks structural quality; `skill-creator` validates that the right skill is selected by Claude Code's dispatcher when the user types a command.
- Follow-up chains:
  - Audit clean → `/sync apply` to propagate verified config to `~/.claude/`
  - Audit found structural issues → review flagged files manually before syncing
  - Audit found many low items → run `/audit fix all` to auto-fix them, or run `/develop refactor` for a targeted cleanup pass
  - After fixing agent instructions (from audit findings) → `/calibrate <agent>` to verify the fix improved recall and confidence calibration
  - Audit Check 12 found description overlap → `/calibrate routing` to verify behavioral routing impact; update descriptions for confused pairs based on the routing report
  - Audit surfaced upgrade proposals → `/audit upgrade` to apply with correctness checks and calibrate A/B evidence for capability changes
  - `/audit upgrade` reverted a capability change → run `/calibrate <agent> full` for deeper signal (N=10 vs N=3 used in upgrade mode)

</notes>
