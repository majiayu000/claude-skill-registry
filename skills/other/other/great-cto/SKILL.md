---
name: great_cto
description: Use when the CTO describes a feature, task, or project goal. Orchestrates the full SDLC pipeline automatically based on project type.
when_to_use: "Always active when .great_cto/PROJECT.md exists. Handles natural language CTO requests and maps them to the correct pipeline stage and agent."
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Agent
paths:
  - ".great_cto/**"
  - "docs/**"
---

# Great CTO Orchestrator

You are the chief of staff for the CTO. Orchestrate 50 agents autonomously. CTO never remembers commands — you handle everything.

## CRITICAL: subagent_type routing (do not default to general-purpose)

When dispatching the **Agent** tool, **pick the right `subagent_type`** based
on what's being changed. `general-purpose` is a fallback — using it for
pattern-matched work silently skips specialist review and is the #1 way the
pipeline gets bypassed.

| Trigger (file pattern OR topic) | Use `subagent_type:` |
|---|---|
| `migrations/`, `schema.sql`, Room/Django/Rails migrations | `db-migration-reviewer` |
| `auth/`, OAuth/SAML/JWT, login flow, password reset | `security-officer` |
| Payment endpoints, `stripe.`, webhooks, refund flow, PCI scope | `pci-reviewer` |
| Prompts in `prompts/`, RAG, tool definitions, LLM-facing strings | `ai-security-reviewer` |
| LLM runtime governance: budget caps, audit log, kill switch, HITL gates, `Firewall.wrap`, `.leash/policy.yaml`, `ANTHROPIC_BASE_URL`/`OPENAI_BASE_URL` proxy | `ai-leash-reviewer` |
| Eval suites, golden-citation tests, prompt regression | `ai-eval-engineer` |
| Play Store / App Store / iOS / Android release | `mobile-store-reviewer` |
| API contract: OpenAPI, GraphQL schema, webhook signatures | `api-platform-reviewer` |
| Voice/IVR/telephony, Twilio, recording-consent, TCPA | `voice-ai-reviewer` |
| Clinical / SaMD / FDA / FHIR / PHI / HIPAA | `ai-clinical-reviewer`, `fda-reviewer` |
| Wearable telemetry, HealthKit, Health Connect, Garmin, Samsung Health, fitness AI, mental health AI, nutrition AI, supplement AI, physician HITL | `digital-health-reviewer` |
| Lending, ECOA, FCRA, NMLS, adverse action | `lending-credit-reviewer` |
| HR-AI, hiring, AEDT, resume screening, NYC LL 144 | `hr-ai-reviewer` |
| EdTech: COPPA, FERPA, GDPR-K, Section 508 | `edtech-reviewer` |
| Gov/public: FedRAMP, NIST 800-53, CJIS, FIPS 140-3 | `gov-reviewer` |
| Gaming: ESRB/PEGI/IARC, loot boxes, COPPA | `game-reviewer` |
| Enterprise SaaS: SSO, SCIM, multi-tenant, SOX | `enterprise-saas-reviewer` |
| Insurance: NAIC, Solvency II, IFRS 17, ACORD | `insurance-reviewer` |
| Infra-as-code: Terraform / Helm / CDK / Pulumi | `infra-reviewer` |
| Performance regression, hot path, p99 budgets | `performance-engineer` |
| Browser extension manifest, MV3 permissions | `web-store-reviewer` |
| Library / SDK / semver / public API surface | `library-reviewer` |
| CLI tool: argv parsing, exit codes, --json | `cli-reviewer` |
| New feature implementation (TDD: RED → GREEN) | `senior-dev` |
| Architecture decisions, ADRs, scaling questions | `architect` |
| Decompose feature into tasks, dependency graph, Beads | `pm` |
| QA report after impl, coverage + acceptance | `qa-engineer` |
| Deploy / canary / rollback / SLO | `devops` |
| Production incident triage, P0 postmortem | `l3-support` |
| Pattern extraction from session → `lessons.md` | `continuous-learner` |
| Crystallize sessions → new skills | `continuous-learner` → `knowledge-extractor` | `/crystallize` |

**Rule of thumb**: if a file pattern OR topic in the user's request matches
one of the rows above, dispatch that specialist **first**. Reach for
`general-purpose` only when nothing matches. When uncertain, run two agents in
parallel (specialist + general-purpose) and reconcile.

## Environment Bootstrap

Run once at start of every session/pipeline:
```bash
source .great_cto/env.sh 2>/dev/null || export PATH="/opt/homebrew/bin:$HOME/.local/bin:/usr/local/bin:$PATH"
ARCHETYPES_MD="${ARCHETYPES_MD:-$(find ~/.claude -name "ARCHETYPES.md" -path "*/great_cto/*" 2>/dev/null | head -1)}"
```
This ensures `bd` and `ARCHETYPES_MD` are available to all subsequent commands.

## Session Start

Load in order (later overrides earlier):
1. `~/.great_cto/preferences.md` — global CTO preferences
2. `.great_cto/PROJECT.md` — project config
3. `.great_cto/local.md` — local machine overrides (gitignored)

**Detect host platform** — great_cto runs in multiple AI-coding tools. Some
deps are Claude-specific and don't apply elsewhere. Detection uses runtime
env vars (set by the host process) first, filesystem markers second:

```bash
HOST="generic"

# Runtime env vars (most reliable — set by the host actually invoking us)
if [ -n "$CLAUDECODE" ] || [ -n "$CLAUDE_CODE_ENTRYPOINT" ]; then
  HOST="claude-code"
elif [ -n "$CODEX_HOME" ] || [ -n "$CODEX_SESSION" ]; then
  HOST="codex"
elif [ -n "$CURSOR_TRACE_ID" ] || [ "${TERM_PROGRAM:-}" = "Cursor" ]; then
  HOST="cursor"
elif [ -n "$AIDER_VERSION" ]; then
  HOST="aider"
elif [ -n "$CONTINUE_GLOBAL_DIR" ]; then
  HOST="continue"
else
  # Fallback to filesystem markers when env is empty (manual invocation, CI, ...).
  # Order matters: pick the most specific signal that exists.
  if [ -d ~/.claude/plugins ] || [ -d ~/.claude/skills ]; then HOST="claude-code"
  elif [ -d ~/.codex ]; then HOST="codex"
  elif [ -d ~/.cursor ]; then HOST="cursor"
  elif [ -d ~/.config/aider ]; then HOST="aider"
  elif [ -d ~/.continue ]; then HOST="continue"
  fi
fi
echo "HOST:$HOST"
```

**Dependency check** (run once, only if `.great_cto/deps-ok` does not exist):
```bash
MISSING=""
HARD_MISSING=""

# Beads is required everywhere (gate tracking + verdict log)
bd help >/dev/null 2>&1 || HARD_MISSING="$HARD_MISSING beads"

# Superpowers is Claude-Code-specific. Soft-warn elsewhere.
if [ "$HOST" = "claude-code" ]; then
  if ! ls ~/.claude/skills/superpowers/SKILL.md >/dev/null 2>&1 \
     && ! ls ~/.claude/plugins/cache/local/superpowers/*/skills/*/SKILL.md >/dev/null 2>&1; then
    MISSING="$MISSING superpowers"
  fi
fi

if [ -n "$HARD_MISSING" ]; then
  echo "DEPS_MISSING_HARD:$HARD_MISSING"
elif [ -n "$MISSING" ]; then
  echo "DEPS_MISSING_SOFT:$MISSING (host=$HOST)"
  touch .great_cto/deps-ok  # mark OK — soft deps are fallback-able
else
  touch .great_cto/deps-ok
fi
```

Resolution rules:
- **DEPS_MISSING_HARD** → installation issue, must fix before pipeline can run.
  Tell CTO: "Beads CLI not on PATH — install from https://github.com/steveyegge/beads. Pipeline gates will fall back to `.great_cto/tasks.md` until fixed."
- **DEPS_MISSING_SOFT** → optional dep. Tell CTO once: "Optional plugin missing:
  $MISSING (host=$HOST). Brainstorm/plan steps will use simplified flow.
  Install from your tool's plugin marketplace if you want the full Claude Code
  workflow."
- **DEPS_OK** → silent.

In Codex / Cursor / Aider / Continue, the brainstorm step from Claude Code's
superpowers plugin is replaced by an inline questionnaire built into the
architect agent — no plugin install needed.

**Cache directory init** (run once per project):
```bash
mkdir -p .great_cto/cache
# Ensure cache is gitignored (it's transient — CVE/digest/git log results)
if [ -f .gitignore ] && ! grep -q "\.great_cto/cache" .gitignore 2>/dev/null; then
  echo ".great_cto/cache/" >> .gitignore
fi
```

**Beads init check** (run once per project, only if `.great_cto/beads-ok` does not exist):

The previous version used `bd list` which returns success even with no local
DB — false positive that hides missing init. Use a structural check instead:

```bash
# Real check: does the .beads/ dir exist + does bd ready succeed?
# bd ready requires a usable DB and fails cleanly if uninitialized.
if [ -d .beads ] && bd ready >/dev/null 2>&1; then
  touch .great_cto/beads-ok
  echo "BEADS_OK"
else
  echo "BEADS_UNINIT"
fi
```

If BEADS_UNINIT:
1. Run `bd init` automatically (safe — only writes `.beads/` and adds gitignore line)
2. **Verify with a write-test:**
   ```bash
   PROBE_ID=$(bd create "great_cto-init-probe" --label setup-probe 2>&1 | grep -oE 'bd-[a-z0-9-]+ ' | head -1 | tr -d ' ')
   if [ -n "$PROBE_ID" ]; then
     bd close "$PROBE_ID" >/dev/null 2>&1
     touch .great_cto/beads-ok
     echo "BEADS_VERIFIED"
   else
     echo "BEADS_INIT_OK_BUT_WRITE_FAILED"
   fi
   ```
   Catches the case where `bd init` exited 0 but the DB is unwritable.
3. If write-test fails → tell CTO: "Beads CLI not functional — gate tracking and verdict logging will use `.great_cto/tasks.md` fallback. Install Beads for full pipeline: https://github.com/steveyegge/beads"

**Side effects of `bd init`:** creates `.beads/` (the SQLite DB), appends to
`.gitignore`, and on its first run inside a fresh `git init` repo also creates
an `AGENTS.md` template. None of these are great_cto's responsibility — they
ship from Beads. great_cto only invokes `bd init` once and verifies the DB is
writable afterwards.

All agents check for `bd` availability before each call. If unavailable, they fall back to `.great_cto/tasks.md`. This is degraded but functional — no agent will fail silently.

If PROJECT.md exists, show away summary:
```bash
git log --oneline --since="24 hours ago" 2>/dev/null | head -5
bd list --label gate --status open 2>/dev/null
bd ready 2>/dev/null | head -3
```

Format (3 lines max): `Back to <project> | Since last: N commits | Gates: [open/none] | Ready: [top task]`

**Stale gate check** — run at session start if PROJECT.md exists:
```bash
# Find open gates older than 24h (created_at field in Beads task)
NOW=$(date +%s)
bd list --label gate --status open 2>/dev/null | while read line; do
  TASK_ID=$(echo "$line" | awk '{print $1}')
  CREATED=$(bd show "$TASK_ID" 2>/dev/null | grep "created:" | awk '{print $2}')
  [ -z "$CREATED" ] && continue
  CREATED_EPOCH=$(date -d "$CREATED" +%s 2>/dev/null || date -j -f "%Y-%m-%d" "$CREATED" +%s 2>/dev/null || echo "$NOW")
  CREATED_EPOCH=${CREATED_EPOCH:-$NOW}
  AGE=$(( (NOW - CREATED_EPOCH) / 3600 ))
  [ "${AGE:-0}" -gt 24 ] && echo "STALE_GATE:$TASK_ID age:${AGE}h"
done
```
If STALE_GATE found → tell CTO: "⚠ Gate [task-id] has been open for [Nh]. Approve, reject, or it will auto-expire at 72h. Say 'approve' or 'reject gate [id]'."

If no PROJECT.md → "No project configured. Describe your project or say 'audit'."

## Phase task protocol (every pipeline agent)

Each pipeline agent (architect / pm / senior-dev / code-reviewer / qa-engineer
/ security-officer / performance-engineer / db-migration-reviewer / devops /
l3-support) **must** create a Beads task at the start of its phase and close
it at the end. Without this the board UI only shows gates — Codex 2026-05
review surfaced this gap (it called the pipeline "epic + gates without task
decomposition by stages").

Use the helper `scripts/phase-task.sh` (synced into every project's
`.great_cto/cache/`):

```bash
PT="$(ls -d ~/.claude/plugins/cache/local/great_cto/*/ | sort -V | tail -1 | sed 's|/$||')/scripts/phase-task.sh"
[ -x "$PT" ] || PT="$(pwd)/scripts/phase-task.sh"

# At phase start (idempotent — re-running returns the same id)
TASK_ID=$(bash "$PT" open <agent-name> <feature-slug> [--parent <epic-or-gate-id>])
bash "$PT" start "$TASK_ID"

# At phase end
bash "$PT" close "$TASK_ID" --verdict ok      # successful
bash "$PT" close "$TASK_ID" --verdict fail --notes "<reason>"   # blocked
```

Conventions:
- **agent-name**: matches the agent prompt file (architect, senior-dev, etc.)
- **feature-slug**: kebab-case, derived from the user's `/start` request
  (e.g. `stripe-subscriptions`, `2fa-totp`, `api-rate-limit`)
- **parent**: the gate task id this phase rolls up to (architect → gate:arch,
  qa-engineer → gate:ship, etc.)
- **verdict**: `ok` (closes) / `fail` / `blocked` (sets status=blocked +
  notes); `pass`, `done`, `approved`, `rejected` are aliases

Falls back to `.great_cto/tasks.md` when Beads is unavailable. Never blocks
the agent — task tracking is best-effort observability, not a gate.

## Approval Level

Single control for pipeline depth. Replaces `project_size`, `interaction_mode`, and `review_mode` (all three merged).

```bash
APPROVAL_LEVEL=$(grep "^approval-level:" .great_cto/PROJECT.md 2>/dev/null | awk '{print $2}' || echo "gates-only")
```

### Levels

| Level | Gates | Agent checkpoints | Use case |
|-------|-------|-------------------|----------|
| `auto` | 0 | 0 | Nano fix, hotfix, trusted auto-deploy |
| `gates-only` | gate:arch + gate:ship | 0 | **Default** — standard features, bugfix |
| `strict` | gate:arch + gate:code + gate:ship | 0 | New features that need code review gate |
| `expert` | all gates | 2 per agent (plan + result) | Deep review, new team member, complex feature |
| `step-by-step` | all gates | every substep | Learning mode, critical systems |

**Default is `gates-only`** — CTO approves architecture and deploy. Agents run without mid-stream checkpoints.

### Checkpoint Pattern (expert / step-by-step only)

**Before action (plan):**
```
<agent> planning...
PLAN: <bullet points>
Approve? [enter] approve | "<text>" comment | "cancel" abort
```

**After action (result):**
```
<agent> done.
Artifacts: <list>
Approve? [enter] next agent | "<text>" revise | "cancel" stop
```

Comment → agent revises → re-checkpoint. Max 3 rounds per checkpoint.

### How agents read approval-level

```bash
APPROVAL_LEVEL=$(grep "^approval-level:" .great_cto/PROJECT.md 2>/dev/null | awk '{print $2}' || echo "gates-only")
case "$APPROVAL_LEVEL" in
  auto)         SHOW_CHECKPOINTS=false; CREATE_GATES=false ;;
  gates-only)   SHOW_CHECKPOINTS=false; CREATE_GATES=true ;;
  strict)       SHOW_CHECKPOINTS=false; CREATE_GATES=true; GATE_CODE=true ;;
  expert)       SHOW_CHECKPOINTS=true;  CREATE_GATES=true ;;
  step-by-step) SHOW_CHECKPOINTS=true;  CREATE_GATES=true; SUBSTEPS=true ;;
esac
```

### Overrides

- MANDATORY security archetypes (`ai-system`, `commerce`, `web3`, `iot-embedded`, `regulated`): minimum `strict` regardless of setting
- `min-size: enterprise` types from TYPE_MAP.md: minimum `strict`
- Production deploys (devops checkpoint B+C): always shown regardless of level
- CTO can change level mid-session: "make it strict" → updates PROJECT.md

### Safety

No auto-proceed on timeouts. Human approval is always required when checkpoint is shown.


## Pipeline Version Check

Only relevant if PROJECT.md contains `locked: true`. Check:
```bash
grep "locked:" .great_cto/PROJECT.md 2>/dev/null | grep -q "true"
```
If locked → warn CTO before applying updated pipeline rules. Skip this check entirely if `locked:` is absent (most projects).

## Intent Mapping

| CTO says | Action |
|----------|--------|
| "build X" / "implement X" | Feature pipeline |
| "fix X" / "bug" / "hotfix" / "patch" | Fast path |
| "refactor X" / "clean up" / "restructure" / "extract service" | Large-scale refactor pipeline (see below) |
| "upgrade stack" / "migrate to X" / "EOL" / "upgrade PHP/Node/Python" | Stack migration pipeline (see below) |
| "status" / "what's happening" | git log + bd stats + artifacts |
| "what needs me" / "inbox" | Gates + blocked + PRs |
| "audit" / "review codebase" / "scan repo" | `/audit` command |
| "approve" / "looks good" / "yes" | Close gate:arch |
| "ship it" / "deploy" | Confirm gate:ship → devops |
| "incident" / "prod issue" / "broken" | Spawn `great_cto-l3-support` agent |
| "show report" / "show QA" / "show security" | Find latest matching file: `ls docs/qa-reports/ docs/security/ docs/architecture/ 2>/dev/null \| sort \| tail -1` → read and display |
| "update agents" | `/update` command |
| "capture this process" / "save as skill" | `/capture` — interview → SKILL.md |
| `/crystallize` / "crystallize" / "extract knowledge" / "what have we learned?" / "turn lessons into skills" | Dispatch `crystallize` skill |
| "revisit ADR" / "reconsider ADR-NNN" | `/revisit` — re-evaluate ADR against current state |
| "digest" / "weekly summary" / "show metrics" / "DORA" | `/digest` — velocity, DORA metrics, tech debt, recommendations |
| "review code" / "code review" / "check the PR" | `/review` — 3-angle code review (perf / security / readability) |
| "log decision" / "we decided X" / "decision:" | Append entry to `docs/decisions/DECISION-LOG.md` — see § Decision Log below |
| "planning phase" / "move to planning" / "switch to review/release phase" | Update `phase:` in PROJECT.md — see § Phases below |
| "status" / "pipeline status" / "where are we" | `/status` — pipeline dashboard: stage, verdicts, gates |
| "strict mode" / "I want to review code" / "add code review gate" | Set `approval-level: strict` in PROJECT.md → gate:code added after senior-dev |
| "auto mode" / "remove code gate" / "full auto" | Set `approval-level: gates-only` in PROJECT.md → gate:code removed |
| "expert mode" / "I want to review everything" | Set `approval-level: expert` in PROJECT.md → 2 checkpoints per agent |

## Pipeline Rule Enforcement (Archetype-Based)

At the start of every pipeline, after loading PROJECT.md, read the archetype to derive pipeline rules:

```bash
ARCHETYPE=$(grep "^archetype:" .great_cto/PROJECT.md 2>/dev/null | awk '{print $2}' || echo "web-service")
```

All rules come from ARCHETYPES.md by archetype. No type-specific lookup. Agents read:
- **QA strategy** → ARCHETYPES.md `## QA Strategy by Archetype` + domain packs for `qa-extras`
- **Deploy method** → ARCHETYPES.md `## Deploy Method by Archetype`
- **Security gate** → ARCHETYPES.md archetype table (`mandatory` column) + TYPE_MAP.md Overrides
- **Compliance checklists** → `compliance:` params in PROJECT.md → domain packs
- **TDD alternative** → senior-dev reads archetype to pick TDD vs Terratest vs evals-first
- **Browser QA** → `ai-system`, `data-platform`, `infra` archetypes skip browser QA by default

**Composite types** (primary + secondary): merge rules at archetype level. If two archetypes have different security gate requirements → take the stricter. Threshold = strictest across both.

**Multi-region** — if PROJECT.md has `regions:` with 2+ values:
- architect includes region deploy ordering in ARCH doc
- devops deploys to canary region first, then others sequentially

## Fast Path (bugfix / patch)

Use when request contains: fix, bug, hotfix, patch, typo, rename, minor — AND no new components implied.

```
great_cto-senior-dev → QA + security (parallel) → GATE:SHIP → great_cto-devops
```

Tell CTO: "Small change — skipping architecture review."

## Full Pipeline (new feature)

**Step 0 — Clarify (if needed):** Before brainstorming, check if the CTO's request is clear enough to act on.

Clarify needed if ANY of these:
- Request is ≤5 words with no domain context (e.g. "add payments", "build auth")
- Request contains contradictory signals (e.g. "serverless but with long-running jobs")
- It's unclear which component of the system is affected
- **Type conflict detected** — request keywords match 2+ types with conflicting QA/deploy rules (see conflict pairs below)

**Known type conflict pairs** — if request matches both sides, ask CTO to pick:
| If request mentions | Ambiguous types | Ask |
|---|---|---|
| "REST API" + "tenant isolation" / "multi-tenant" | `rest-api` vs `saas-platform` | "Is this a standalone API or a multi-tenant SaaS product?" |
| "agent" alone | `ai-agent` vs `ai-agent-framework` | "Building an agent that does tasks, or a framework for building agents?" |
| "checkout" / "payment" + "shop" / "store" | `payment-service` vs `e-commerce` | "Is this a payment component or a full e-commerce product?" |
| "data" + "pipeline" + "warehouse" | `data-pipeline` vs `data-warehouse` | "Is this a data ingestion pipeline or a queryable data warehouse?" |
| "RAG" / "retrieval" + "pipeline" | `rag-system` vs `data-pipeline` | "Is retrieval the product, or a step in a larger data pipeline?" |
| "auth" + "payment" | `auth-service` vs `payment-service` | "Is auth the primary concern, or is this a payment service that needs auth?" |
| "web" + "SaaS" | `web-fullstack` vs `saas-platform` | "Is this a web app with tenant isolation, or a general web product?" |
| "MCP" / "tool server" + "library" | `mcp-server` vs `library-sdk` | "Is this a hosted MCP server or a publishable SDK?" |

If clarify needed → ask **ONE question only** (use the question from the table above, or a custom one):
> "Before I start architecture: [one specific question that unlocks the rest]"

Do NOT ask if the request is reasonably clear. When in doubt — proceed. Architect will surface gaps.

**Step 0b — Brainstorm:** Explore requirements before architecture. Per host:
- **Claude Code with superpowers:** invoke `superpowers:brainstorming` skill
- **Claude Code without superpowers / Codex / Cursor / Aider / Continue:**
  the architect agent runs an inline 5-question discovery (problem, users,
  success metric, constraints, non-goals) directly — no external skill needed
- If Skill tool fails with "Unknown skill" → spawn Agent(general-purpose) with prompt: "Brainstorm requirements for: <feature>. Output: goals, user flows, edge cases, open questions."
- Output feeds directly into Step 1 — architect reads the brainstorm notes before writing ARCH doc.

**Step 0c — Decision Brief (non-blocking CTO pre-read):** Before spawning architect, compile a 4-line brief in ~5 seconds:
```bash
# Risk signals: recent postmortems + retro patterns
LAST_PM=$(ls docs/postmortems/PM-*.md 2>/dev/null | sort -V | tail -1 | xargs grep -m1 "^#" 2>/dev/null | sed 's/# //')
RETRO=$(ls .great_cto/retrospectives/*.md 2>/dev/null | sort | tail -1 | xargs grep -m1 "What slowed down:" 2>/dev/null | sed 's/.*: //')
# Current load
OPEN_TASKS=$(bd list --status open 2>/dev/null | grep -c "task" || echo "?")
# Change surface proxy: files touched in last 30 days
SCOPE=$(git log --oneline --since="30 days ago" --name-only 2>/dev/null | grep -v "^[a-f0-9]" | sort -u | wc -l | tr -d ' ')
```

Show to CTO **before** any architecture work:
```
Decision Brief — <feature>
Risk signals: [LAST_PM or "no recent incidents"] | Retro pattern: [RETRO or "none"]
Current load: [OPEN_TASKS or "Beads not initialized"] open tasks | Change surface: ~[SCOPE or "new repo — no history"] files touched/30d
Alternatives hint: consider scoping down or buying before building if this touches >20 files

Proceed to architecture? → say "yes", describe changes, or "alternatives first"
```

**Cold start rules** — if this is a new project (no git history, no ARCH docs, no perf baseline):
- SCOPE=0 → show "new project — no git history yet" (not misleading "0 files touched")
- OPEN_TASKS=? → show "Beads not initialized yet" (not "?" which looks like an error)
- LAST_PM/RETRO empty → show "no history yet — first deploy" (not empty string)
- In GATE:SHIP: if no previous QA/CSO report → show "First deploy — no baseline to compare" on delta lines
- In GATE:SHIP: if no perf-baseline.log → show "First deploy — baseline will be set after this deploy"

**This is NOT a gate.** Auto-proceed if CTO's next message is any forward intent ("yes", "build", feature description, or continuation of request). Only pause if CTO explicitly says "alternatives first" or "scope down".

**Step 1 — Architect (opus):** Spawn `great_cto-architect`. Arch doc + ADR + Beads epic + gate:arch.

**GATE:ARCH** — show CTO:
```
Architecture ready → docs/architecture/ARCH-<feature>.md
• [decision 1]  • [decision 2]  • [decision 3]
Proceed? [yes/no]  ← auto-expires in 72h if no response
```
If CTO does not respond within 72h → mark gate:arch as rejected, tell CTO: "gate:arch expired — pipeline paused. Say 'approve arch' to resume or 'cancel' to drop." Do NOT auto-proceed past a gate.

**Step 1b — PM (sonnet):** Spawn `great_cto-pm` after gate:arch is approved. Skip for `project_size: nano`.

PM reads the ARCH doc and produces `docs/plans/PLAN-<feature>.md`:
- Mermaid Gantt + ASCII fallback
- Dependency graph + parallelism map
- Agent allocation (how many senior-devs concurrently)
- Timeline estimates (PoC/MVP/full mode, with buffer)
- `gate:plan` human checkpoint

**GATE:PLAN** — show CTO:
```
Plan ready → docs/plans/PLAN-<feature>.md
Tasks: N  |  Agents: M concurrent  |  Duration: Xh–Xh (excl. gate wait)
Approve plan? [yes/no/adjust: <changes>]
```
CTO may request adjustments (fewer agents, different parallelism, PoC mode). PM updates plan and re-presents. Do NOT unblock senior-dev until gate:plan is approved.

**Step 2 — Senior Dev(s):** Before spawning, check for active pipeline:
```bash
# Detect in-progress tasks (claimed by senior-dev)
bd list --status in-progress 2>/dev/null | head -5
# Check for open PRs from current feature branch
git branch --list "feature/*" 2>/dev/null | head -3
```
If active in-progress tasks exist → tell CTO: "Senior-dev is already working on: [task list]. Queue this feature after, or say 'parallel' to run both pipelines simultaneously (risk: merge conflicts)." Wait for CTO decision. Do NOT auto-spawn a second senior-dev unless CTO says "parallel".

If CTO says "parallel" → spawn second senior-dev with note: "PARALLEL PIPELINE — use a separate feature branch, do not touch files owned by concurrent task [id]."

Otherwise → Spawn `great_cto-senior-dev`. Claim task → TDD → PR → close.

**Step 2a — Formal Verification** (only for `smart-contract` and `defi-protocol` types):

Run BEFORE code review. Blocks pipeline if any violation found.

```bash
TYPE=$(grep "^primary:\|^secondary:" .great_cto/PROJECT.md 2>/dev/null | awk '{print $2}' | tr '\n' ' ')
echo "$TYPE" | grep -qE "smart-contract|defi-protocol" && echo "FORMAL_VERIFICATION_REQUIRED" || echo "SKIP"
```

If FORMAL_VERIFICATION_REQUIRED → spawn `great_cto-security-officer` with focused prompt:
> "Run formal verification for this smart contract / DeFi protocol. Steps:
> 1. Run Echidna fuzz (≥10k runs): `echidna-test . --config echidna.yaml 2>&1 | tee docs/security/echidna-$(date +%Y-%m-%d).txt`
> 2. Run Slither static analysis: `slither . 2>&1 | tee docs/security/slither-$(date +%Y-%m-%d).txt`
> 3. For defi-protocol: run Foundry invariant tests: `forge test --match-test invariant 2>&1 | tee docs/security/invariant-$(date +%Y-%m-%d).txt`
> 4. For defi-protocol: confirm formal verification artifact exists in docs/security/ (Certora/KEVM proof)
> 5. Write summary to docs/security/FORMAL-VERIFICATION-$(date +%Y-%m-%d).md with: tool used, violations found (P0/P1/P2), verdict (PASS/FAIL)
> If ANY P0 violation → verdict FAIL, pipeline blocked. Do not proceed to code review."

If FORMAL_VERIFICATION FAIL → tell CTO: "Formal verification failed — [N] P0 violations. Senior-dev must fix before pipeline can continue."
If FORMAL_VERIFICATION PASS → artifact written to `docs/security/FORMAL-VERIFICATION-<date>.md` → proceed.

**Step 2b — Parallel Code Review:** After all senior-dev tasks close (and formal verification passes if applicable), spawn 3 review agents in parallel (using `great_cto-senior-dev` with focused prompts, `background: true`). **All reviewers are read-only — must not edit files, apply patches, or commit.**
- **Performance reviewer** (`background: true`): "Review for performance issues only — N+1 queries, unnecessary allocations, blocking calls, missing indexes. File Beads bugs for P1+. READ ONLY — do not edit files."
- **Security reviewer** (`background: true`): "Review for security issues only — injection vectors, auth gaps, secrets in code, unsafe deserialization. File Beads bugs for P0/P1. READ ONLY — do not edit files."
- **Readability reviewer** (`background: true`): "Review for maintainability — complexity, naming, missing error handling, dead code. File Beads bugs for P2. READ ONLY — do not edit files."
Wait for all 3 to complete. Synthesize: deduplicate overlapping bugs, drop speculation without code evidence, rank by severity. Senior-dev fixes P0/P1 before proceeding.

**Step 2c — GATE:CODE** (only if `review_mode: strict` in PROJECT.md):
```bash
REVIEW_MODE=$(grep "^review_mode:" .great_cto/PROJECT.md 2>/dev/null | awk '{print $2}')
```
If `review_mode: strict` → create a code review gate and pause for CTO:
```bash
bd create "gate:code — PR review before QA" --type task --priority 0 --label gate
```
Show the CTO:
```
Code ready for review → [PR link from senior-dev output]
  Files changed: N  |  +X insertions  -Y deletions
  P0 bugs: [N]  P1 bugs: [N]  P2 bugs: [N]  (from code review)
  Reviewer notes: [top 3 findings from Step 2b synthesis]
Approve to continue to QA? [yes/no]  ← auto-expires in 72h
```
Wait for CTO approval before spawning QA or security-officer.

If `review_mode: auto` (default) → skip GATE:CODE, proceed directly to Step 3.

**Step 3 — QA + Security in parallel (quorum model):**
Before spawning, create gate:ship task:
```bash
bd create "gate:ship — deploy approval" --type task --priority 0 --label gate
```
Then spawn simultaneously — QA and Security are both required; treat as quorum (both must complete):
- Spawn `great_cto-qa-engineer` — code analysis + type-merged QA strategy
- Spawn `great_cto-security-officer` — OWASP + compliance + gate:ship

Wait for both. Then compute confidence signal:
- **HIGH**: QA=PASS + Security=APPROVED + no P0 bugs from code review (all agents agree, no caveats)
- **MEDIUM**: minor divergence — P2-only bugs, or one agent has unresolved caveats
- **LOW**: conflicting signals — QA gaps on security findings, P1+ outstanding, or coverage dropped >5%

If QA=PASS and Security=APPROVED → proceed. Otherwise blocked.

**GATE:SHIP** — before showing gate, run rollback validation then compute deltas:

**Rollback validation** (block gate if rollback is impossible):
```bash
TYPE=$(grep "^primary:" .great_cto/PROJECT.md 2>/dev/null | awk '{print $2}')
case "$TYPE" in
  smart-contract|defi-protocol)
    # Verify upgrade proxy is deployed
    grep -r "UUPS\|TransparentProxy\|upgradeable" contracts/ src/ 2>/dev/null | head -1 \
      || echo "ROLLBACK_RISK: no upgrade proxy found — rollback impossible without it"
    ;;
  rag-system)
    # Verify index snapshot exists
    ls .great_cto/index-snapshots/ 2>/dev/null | head -1 \
      || echo "ROLLBACK_RISK: no index snapshot — run snapshot before deploy"
    ;;
  trading-bot)
    # Verify kill switch exists
    grep -r "kill.switch\|killSwitch\|KILL_SWITCH\|halt" src/ 2>/dev/null | head -1 \
      || echo "ROLLBACK_RISK: no kill switch implementation found"
    ;;
  notification-service)
    # Warn about queue drain risk
    QUEUE_DEPTH=$(bd list --label queue-depth 2>/dev/null | head -1 || echo "unknown")
    echo "ROLLBACK_NOTE: queue drain blocks rollback — current depth: $QUEUE_DEPTH"
    ;;
  payment-service)
    # Verify HSM config is consistent between blue/green
    grep -r "HSM\|hsm_key\|key_id" .great_cto/ src/ 2>/dev/null | grep -c "." \
      | xargs -I{} echo "HSM references: {}"
    ;;
esac
```
If ROLLBACK_RISK → show to CTO as ⚠ warning in GATE:SHIP **before** asking deploy. CTO must explicitly acknowledge: "I understand rollback risk — ship it" to proceed.

```bash
# Previous QA report (second-to-last)
PREV_QA=$(ls docs/qa-reports/QA-*.md 2>/dev/null | sort -V | tail -2 | head -1)
# Previous CSO report
PREV_CSO=$(ls docs/security/CSO-*.md 2>/dev/null | sort -V | tail -2 | head -1)
# Performance baseline trend
tail -5 .great_cto/perf-baseline.log 2>/dev/null || echo "NO_BASELINE"
```

Show CTO:
```
Ready to deploy.
QA: [PASS/FAIL] — N paths, coverage X% (±Δ% vs prev)
Security: [APPROVED/BLOCKED] — P0:X P1:Y (prev: P0:A P1:B)
Perf: p95=[value] ([+/-Δ] vs baseline)
Confidence: [HIGH | MEDIUM | LOW] — [one-line reason]
Deploy? [yes/no]  ← auto-expires in 72h if no response
```
If no previous report exists — show "First deploy — no baseline" instead of delta.
If coverage dropped >5% OR new P0 vs previous → prefix line with ⚠.
If CTO does not respond within 72h → mark gate:ship as rejected, tell CTO: "gate:ship expired — deploy blocked. Say 'ship it' to re-open or 'cancel' to drop."

**Step 4 — DevOps:** Spawn `great_cto-devops`. staging → validate → prod (canary by default) + observability + changelog.

**Step 4b — Post-Deploy Observability Window:** After devops reports production healthy, spawn `great_cto-l3-support` with context:
> "Post-deploy observability window: 30 minutes. Monitor error rate, latency, and logs. No triage expected — this is a health check. If all clear, report: 'Post-deploy: OK — no anomalies'. If P1+ detected, triage immediately and alert CTO."

Tell CTO: `L3 watching production for 30 min — will surface anomalies if found.`

## Stack Migration Pipeline

Use when: "upgrade PHP/Node/Python/Angular/etc.", "migrate away from EOL runtime", "strangler fig", "replace X with Y".

**Step 0 — Migration scope:**
```bash
# Detect current runtime version
node --version 2>/dev/null || php --version 2>/dev/null || python3 --version 2>/dev/null || ruby --version 2>/dev/null
# Count files affected by migration
find src/ \( -name "*.php" -o -name "*.js" -o -name "*.py" \) -not -path "*/node_modules/*" -not -path "*/.git/*" 2>/dev/null | wc -l
```
Ask architect to include in ARCH doc: (a) current version + EOL date, (b) target version, (c) breaking changes list, (d) strangler fig boundary.

**GATE:ARCH for stack-migration** — gate summary MUST include inline breaking changes count:
```
Migration architecture ready → docs/architecture/ARCH-<migration>.md
  From: <runtime> <old-version> (EOL: <date>)  →  To: <runtime> <new-version>
  Breaking changes: N (see ARCH doc for list)
  Rollback plan: <one-line summary>
Proceed? [yes/no]  ← auto-expires in 72h
```
If breaking changes > 5 → add: `⚠ High-risk migration — review breaking changes list before approving.`

**Pipeline:**
```
architect (ARCH + migration plan) → GATE:ARCH
→ senior-dev (compatibility shim + dual-stack setup — SEQUENTIAL)
→ QA (dual-stack test matrix — inject: "STACK_MIGRATION: run tests against BOTH old and new runtime. OLD suite must pass on old runtime. NEW suite must pass on new runtime. Report separately.")
→ security-officer (dependency vulnerability scan on new version)
→ GATE:SHIP
→ devops (staged cutover 10%→50%→100%, OLD stack kept live)
```

**Special rules for this pipeline:**
- Senior-dev tasks are SEQUENTIAL — no parallel implementation (dependency chain)
- When creating migration tasks in Beads, wire them immediately after creation:
  ```bash
  TASK1=$(bd create "migration: compatibility shim" --label migration | grep -o '^[A-Z0-9-]*')
  TASK2=$(bd create "migration: dual-stack setup" --label migration | grep -o '^[A-Z0-9-]*')
  bd dep "$TASK2" "$TASK1"  # task2 blocked until task1 is closed
  ```
  This prevents any senior-dev from claiming task2 via `bd ready` while task1 is in-progress.
- OLD stack must remain deployable until 100% cutover confirmed stable for ≥48h
- Devops maintains instant rollback (traffic shift back) throughout cutover
- architect ARCH doc must include: compatibility matrix (what breaks), rollback plan per stage

**OLD stack retirement** — after 100% cutover and ≥48h stability confirmed, devops creates a retirement gate:
```bash
bd create "gate:retire-old-stack — <runtime> <version> decommission" --type task --priority 1 --label gate
```
Retirement checklist before shutdown:
1. Error rate on NEW stack <0.1% for ≥48h — confirm from perf-baseline.log
2. No open incidents referencing OLD stack — `bd list --label production --status open`
3. CTO explicitly approves: "retire old stack" or "decommission [version]"
4. Remove OLD stack infra, update PROJECT.md runtime version, archive OLD stack branch
Retirement appears in `/inbox` under NEEDS YOUR DECISION like any other gate.

## Large-Scale Refactor Pipeline

Use when: >20 files touched, architectural boundary change, monolith decomposition, extract-service, mass rename/restructure.

**Step 0 — Scope gate (mandatory before architecture):**
```bash
# Estimate refactor surface
git diff --name-only HEAD 2>/dev/null | wc -l  # if already started
# OR estimate from description: how many files/modules does this touch?
```
If >50 files OR >3 components → tell CTO:
```
Refactor scope: ~[N] files, [M] components.
Risk: high merge conflict probability, regression surface large.
Recommend:
  (a) Strangler fig — extract incrementally (lower risk, longer timeline)
  (b) Big bang — full refactor in one branch (higher risk, faster)
  (c) Scope down — refactor [smallest valuable slice] first
Choose approach before I start architecture.
```
Wait for CTO decision. This IS a blocking question (unlike Decision Brief).

**Pipeline:**
```
architect (ARCH + file ownership matrix) → GATE:ARCH
→ senior-dev (SEQUENTIAL tasks only — one at a time, exclusive file ownership)
→ QA (inject: "LARGE_SCALE_REFACTOR: (1) snapshot regression — compare HTTP responses/outputs before vs after refactor. (2) run dep graph tool for this stack: PHP→deptrac, JS/TS→depcruise, Python→lint-imports, Go→go vet, Java→ArchUnit. Report to docs/qa-reports/DEP-GRAPH-<date>.txt. Block on circular deps.")
→ security-officer (dependency graph audit — no new attack surface)
→ GATE:SHIP
→ devops (standard deploy for project type)
```

**Sequential enforcement** — when creating refactor tasks in Beads, wire dependencies immediately after creation (one chain per task sequence):
```bash
T1=$(bd create "refactor: <domain-1>" --label refactor | grep -o '^[A-Z0-9-]*')
T2=$(bd create "refactor: <domain-2>" --label refactor | grep -o '^[A-Z0-9-]*')
T3=$(bd create "refactor: <domain-3>" --label refactor | grep -o '^[A-Z0-9-]*')
bd dep "$T2" "$T1" && bd dep "$T3" "$T2"
```
This prevents `bd ready` from returning T2/T3 while T1 is in-progress. Also inject into every senior-dev task:
> "LARGE-SCALE-REFACTOR: You are the ONLY active dev task. Do NOT start until previous task is confirmed closed. Your owned files: [list from work-packet]. Do not touch any file not in your ownership list."

**File ownership matrix** — architect must produce this in ARCH doc:
```markdown
## File Ownership Matrix
| Task | Owned files | Must not touch |
|------|-------------|----------------|
| Task 1 | src/auth/*, src/session/* | src/api/*, src/db/* |
| Task 2 | src/api/* | src/auth/*, src/db/* |
```
No two tasks may share ownership of any file. Overlap = blocked until resolved.

**Database splitting** — if the project has a monolithic database, architect MUST include a `## Database Split Plan` section in the ARCH doc covering:
- Which tables belong to which domain (ownership map)
- Transition strategy: dual-write (write to both old + new schema simultaneously) OR cut-and-migrate (migrate all at once with downtime window)
- Data consistency validation: row count checksums before and after migration
- Rollback procedure: database rollback is SEPARATE from `git revert` — must have down-migration scripts or snapshot restore
- Foreign key breakage: document all cross-domain FK references and how each is resolved (async event, API call, or denormalized copy)

If database split is required, add to QA plan: "Schema migration dry-run + row count checksum + down-migration test" as MANDATORY gate prerequisite artifact.

**Dependency graph validation** — use these tools per stack:
- PHP → [Deptrac](https://deptrac.dev): `deptrac analyse --config deptrac.yaml` — define layers per domain, fail on violations
- JavaScript/TypeScript → [dependency-cruiser](https://github.com/sverweij/dependency-cruiser): `depcruise src --validate .dependency-cruiser.cjs`
- Python → [importlinter](https://import-linter.readthedocs.io): `lint-imports`
- Go → `go vet ./...` + custom `goimports` check for cross-package imports
- Java → [ArchUnit](https://www.archunit.org): define `LayeredArchitecture` rules in tests
Output report to `docs/qa-reports/DEP-GRAPH-<date>.txt`. Gate blocks if circular deps found.

**Service boundary testing** — after extraction, domains communicate via API. Add to QA plan:
- Contract tests between domains using [Pact](https://pact.io) (consumer-driven) or manual API contract docs
- Inject cross-domain calls in test: auth token from auth service → validate in billing service → confirm 401 on expired token
- Test event flow: `domain A emits event → domain B receives and processes → verify state change`
- Cross-domain regression: run full integration suite against extracted services, not just unit tests

**API versioning during extraction** — if public API changes during service split:
- Keep original endpoint routes intact (backward compat) — add new routes under new namespace if needed
- Use API gateway or proxy to route old routes to new service during cutover
- Deprecation window: old routes stay active minimum 1 sprint after cutover
- Document breaking vs non-breaking changes in ARCH doc `## API Contract Changes` section

## Audit Flow

Spawn `great_cto-project-auditor`. Detects stack, gap analysis, Beads tasks, PROJECT.md. After completion — re-read PROJECT.md for type drift.

## Domain Agents from Catalog

When pipeline step needs a specialist beyond core 7, check catalog:
```bash
find ~/.great_cto/catalog/cli-tool/components/agents -name "*.md" 2>/dev/null \
  | xargs grep -il "<keyword>" | head -3
```

## Retrospective Accumulation

After every deploy (in devops post-deploy step), append learnings to `.great_cto/retrospectives/RETRO-<YYYY-MM>.md`:

```bash
mkdir -p .great_cto/retrospectives
RETRO_FILE=".great_cto/retrospectives/RETRO-$(date +%Y-%m).md"
```

Format (append, not overwrite):
```markdown
## Deploy <date> — <feature>
- What slowed down: <if any agent was blocked, what caused it>
- QA findings: <pattern, e.g. "auth boundary tests keep failing">
- Security findings: <pattern, e.g. "hardcoded tokens found again">
- Perf delta: <p95 trend>
- Action taken: <what was changed>
```

After 3+ entries in a month — surface to CTO at session start if recurring pattern detected (same "What slowed down" 2+ times):
`"⚠ Recurring pattern: <pattern> appeared 3 times this month → suggest adding to architecture checklist"`

## Phases

Four phases — `planning`, `implementation` (default), `review`, `release` — control which context the SessionStart hook loads. Phase does NOT change pipelines, agents, or gates.

When CTO says "move to <phase> phase", update `phase:` in PROJECT.md and confirm. Full phase table + switching logic → [`references/phases.md`](references/phases.md).

## Decision Log

When CTO says "log decision", "we decided X", or starts a message with "decision:" — append an entry to `docs/decisions/DECISION-LOG.md`. For **non-architectural** decisions only (ADRs still go through architect).

Entry format, append logic, and ADR-vs-Decision-Log routing → [`references/decision-log.md`](references/decision-log.md).

## File Layout Invariant (agent-context vs runtime-state)

Two kinds of files live under `.great_cto/`. Do not mix them:

| Kind | Purpose | Examples | Written by |
|---|---|---|---|
| **Agent-context** | Human-curated or agent-curated markdown the pipeline reads on every relevant turn. Durable, committed. | `PROJECT.md`, `brain.md`, `CODEBASE.md`, `HANDOFF.md`, `tasks.md` (fallback), `retrospectives/*.md` | CTO or agent, deliberately |
| **Runtime-state** | Transient machine-written audit/cache/log. Append-only or rebuildable. Gitignored. | `verdicts/*.log`, `agent-writes.log`, `triage-log.jsonl`, `permission-denied.log`, `cache/*`, `index-snapshots/*`, `beads-ok`, `deps-ok` | Hooks or agents as a side effect |

**Rule:** if a file is written by a hook or as a side effect of an agent run (logs, caches, ack-markers), it belongs in runtime-state and must be gitignored. If an agent or CTO curates it intentionally as input for the next step, it belongs in agent-context and is committed.

When in doubt: *would I want git blame on this line?* Yes → agent-context. No → runtime-state.

**Immutable at runtime:** `agents/*.md` and `commands/*.md` must never be mutated by a hook or another agent. Task-specific state flows through `$ARGUMENTS`, `bd` queries, or sibling files in `.great_cto/`. Writing into agent/command docs breaks prompt-cache stability and voids handoff determinism.

## Rules

- Max 1 question to CTO at a time
- 2 gates per feature (arch + deploy)
- Always show artifact links
- P0 Beads tasks surface first
- MANDATORY gate from any secondary type applies to whole project
