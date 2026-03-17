---
name: council
description: 'Multi-model consensus council. Spawns parallel judges with configurable perspectives. Modes: validate, brainstorm, research. Triggers: "council", "get consensus", "multi-model review", "multi-perspective review", "council validate", "council brainstorm", "council research".'
context: fork
metadata:
  tier: judgment
  dependencies:
    - standards   # optional - loaded for code validation context
  replaces: judge
---

# /council — Multi-Model Consensus Council

Spawn parallel judges with different perspectives, consolidate into consensus. Works for any task — validation, research, brainstorming.

## Quick Start

```bash
/council --quick validate recent                               # fast inline check
/council validate this plan                                    # validation (2 agents)
/council brainstorm caching approaches                         # brainstorm
/council validate the implementation                          # validation (critique triggers map here)
/council research kubernetes upgrade strategies                # research
/council research the CI/CD pipeline bottlenecks               # research (analyze triggers map here)
/council --preset=security-audit validate the auth system      # preset personas
/council --deep --explorers=3 research upgrade automation      # deep + explorers
/council --debate validate the auth system                # adversarial 2-round review
/council --deep --debate validate the migration plan      # thorough + debate
/council                                                       # infers from context
```

Council works independently — no RPI workflow, no ratchet chain, no `ao` CLI required. Zero setup beyond initial install.

## Modes

| Mode | Agents | Execution Backend | Use Case |
|------|--------|-------------------|----------|
| `--quick` | 0 (inline) | Self | Fast single-agent check, no spawning |
| default | 2 | Runtime-native (Codex sub-agents preferred; Claude teams fallback) | Independent judges (no perspective labels) |
| `--deep` | 3 | Runtime-native | Thorough review |
| `--mixed` | 3+3 | Runtime-native + Codex CLI | Cross-vendor consensus |
| `--debate` | 2+ | Runtime-native | Adversarial refinement (2 rounds) |

```bash
/council --quick validate recent   # inline single-agent check, no spawning
/council recent                    # 2 runtime-native judges
/council --deep recent             # 3 runtime-native judges
/council --mixed recent            # runtime-native + Codex CLI
```

### Spawn Backend (MANDATORY)

Council requires a runtime that can **spawn parallel subagents** and (for `--debate`) **send messages between agents**. Use whatever multi-agent primitives your runtime provides. If no multi-agent capability is detected, fall back to `--quick` (inline single-agent).

**Required capabilities:**
- **Spawn subagent** — create a parallel agent with a prompt (required for all modes except `--quick`)
- **Agent messaging** — send a message to a specific agent (required for `--debate`)

Skills describe WHAT to do, not WHICH tool to call. See `skills/shared/SKILL.md` for the capability contract.

**After detecting your backend, read the matching reference for concrete spawn/wait/message/cleanup examples:**
- Claude feature contract → `skills/shared/references/claude-code-latest-features.md`
- Claude Native Teams → `skills/shared/references/backend-claude-teams.md`
- Codex Sub-Agents / CLI → `skills/shared/references/backend-codex-subagents.md`
- Background Tasks → `skills/shared/references/backend-background-tasks.md`
- Inline (`--quick`) → `skills/shared/references/backend-inline.md`

See also `references/cli-spawning.md` for council-specific spawning flow (phases, timeouts, output collection).

## When to Use `--debate`

Use `--debate` for high-stakes or ambiguous reviews where judges are likely to disagree:
- Security audits, architecture decisions, migration plans
- Reviews where multiple valid perspectives exist
- Cases where a missed finding has real consequences

Skip `--debate` for routine validation where consensus is expected. Debate adds R2 latency (judges stay alive and process a second round via backend messaging).

**Incompatibilities:**
- `--quick` and `--debate` cannot be combined. `--quick` runs inline with no spawning; `--debate` requires multi-agent rounds. If both are passed, exit with error: "Error: --quick and --debate are incompatible."
- `--debate` is only supported with validate mode. Brainstorm and research do not produce PASS/WARN/FAIL verdicts. If combined, exit with error: "Error: --debate is only supported with validate mode."

## Task Types

| Type | Trigger Words | Perspective Focus |
|------|---------------|-------------------|
| **validate** | validate, check, review, assess, critique, feedback, improve | Is this correct? What's wrong? What could be better? |
| **brainstorm** | brainstorm, explore, options, approaches | What are the alternatives? Pros/cons? |
| **research** | research, investigate, deep dive, explore deeply, analyze, examine, evaluate, compare | What can we discover? What are the properties, trade-offs, and structure? |

Natural language works — the skill infers task type from your prompt.

---

## Architecture

### Context Budget Rule (CRITICAL)

Judges write ALL analysis to output files. Messages to the lead contain ONLY a
minimal completion signal: `{"type":"verdict","verdict":"...","confidence":"...","file":"..."}`.
The lead reads output files during consolidation. This prevents N judges from
exploding the lead's context window with N full reports via SendMessage.

**Consolidation runs inline as the lead** — no separate chairman agent. The lead
reads each judge's output file sequentially with the Read tool and synthesizes.

### Execution Flow

```
┌─────────────────────────────────────────────────────────────────┐
│  Phase 1: Build Packet (JSON)                                   │
│  - Task type (validate/brainstorm/research)                      │
│  - Target description                                           │
│  - Context (files, diffs, prior decisions)                      │
│  - Perspectives to assign                                       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Phase 1a: Select spawn backend                                  │
│  codex_subagents | claude_teams | background_fallback            │
│  Team lead = spawner (this agent)                                │
└─────────────────────────────────────────────────────────────────┘
                              │
            ┌─────────────────┴─────────────────┐
            ▼                                   ▼
┌───────────────────────┐           ┌───────────────────────┐
│  RUNTIME-NATIVE JUDGES│           │     CODEX AGENTS      │
│ (spawn_agent or teams)│           │  (Bash tool, parallel)│
│                       │           │  Agent 1 (independent │
│  Agent 1 (independent │           │    or with preset)    │
│    or with preset)    │           │  Agent 2              │
│  Agent 2              │           │  Agent 3              │
│  Agent 3 (--deep only)│           │  (--mixed only)       │
│  (--deep/--mixed only)│           │                       │
│                       │           │  Output: JSON + MD    │
│  Write files, then    │           │  Files: .agents/      │
│ wait()/SendMessage to │           │    council/codex-*    │
│ lead                  │           │                       │
│  Files: .agents/      │           └───────────────────────┘
│    council/claude-*   │                       │
└───────────────────────┘                       │
            │                                   │
            └─────────────────┬─────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Phase 2: Consolidation (Team Lead — inline, no extra agent)    │
│  - Receive MINIMAL completion signals (verdict + file path)     │
│  - Read each judge's output file with Read tool                 │
│  - If schema_version is missing from a judge's output, treat    │
│    as version 0 (backward compatibility)                        │
│  - Compute consensus verdict                                    │
│  - Identify shared findings                                     │
│  - Surface disagreements with attribution                       │
│  - Generate Markdown report for human                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Phase 3: Cleanup                                               │
│  - Cleanup backend resources (close_agent / TeamDelete / none)  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Output: Markdown Council Report                                │
│  - Consensus: PASS/WARN/FAIL                                    │
│  - Shared findings                                              │
│  - Disagreements (if any)                                       │
│  - Recommendations                                              │
└─────────────────────────────────────────────────────────────────┘
```

### Graceful Degradation

| Failure | Behavior |
|---------|----------|
| 1 of N agents times out | Proceed with N-1, note in report |
| All Codex CLI agents fail | Proceed with runtime-native judges only, note degradation |
| All agents fail | Return error, suggest retry |
| Codex CLI not installed | Skip Codex CLI judges, continue with runtime judges only (warn user) |
| No multi-agent capability | Fall back to `--quick` (inline single-agent review) |
| No agent messaging | `--debate` unavailable, single-round review only |
| Output dir missing | Create `.agents/council/` automatically |

Timeout: 120s per agent (configurable via `--timeout=N` in seconds).

**Minimum quorum:** At least 1 agent must respond for a valid council. If 0 agents respond, return error.

### Pre-Flight Checks

1. **Multi-agent capability:** Detect whether runtime supports spawning parallel subagents. If not, degrade to `--quick`.
2. **Agent messaging:** Detect whether runtime supports agent-to-agent messaging. If not, disable `--debate`.
3. **Codex CLI judges (--mixed only):** Check `which codex`, test model availability, test `--output-schema` support. Downgrade mixed mode when unavailable.
4. **Agent count:** Verify `judges * (1 + explorers) <= MAX_AGENTS (12)`
5. **Output dir:** `mkdir -p .agents/council`

---

## Quick Mode (`--quick`)

Single-agent inline validation. No subprocess spawning, no Task tool, no Codex. The current agent performs a structured self-review using the same output schema as a full council.

**When to use:** Routine checks, mid-implementation sanity checks, pre-commit quick scan.

**Execution:** Gather context (files, diffs) -> perform structured self-review inline using the council output_schema (verdict, confidence, findings, recommendation) -> write report to `.agents/council/YYYY-MM-DD-quick-<target>.md` labeled as `Mode: quick (single-agent)`.

**Limitations:** No cross-perspective disagreement, no cross-vendor insights, lower confidence ceiling. Not suitable for security audits or architecture decisions.

---

## Packet Format (JSON)

The packet sent to each agent. **File contents are included inline** — agents receive the actual code/plan text in the packet, not just paths. This ensures both Claude and Codex agents can analyze without needing file access.

If `.agents/ao/environment.json` exists, include it in the context packet so judges can reason about available tools and environment state.

```json
{
  "council_packet": {
    "version": "1.0",
    "mode": "validate | brainstorm | research",
    "target": "Implementation of user authentication system",
    "context": {
      "files": [
        {
          "path": "src/auth/jwt.py",
          "content": "<file contents inlined here>"
        },
        {
          "path": "src/auth/middleware.py",
          "content": "<file contents inlined here>"
        }
      ],
      "diff": "git diff output if applicable",
      "spec": {
        "source": "bead na-0042 | plan doc | none",
        "content": "The spec/bead description text (optional — included when wrapper provides it)"
      },
      "prior_decisions": [
        "Using JWT, not sessions",
        "Refresh tokens required"
      ]
    },
    "perspective": "skeptic (only when --preset or --perspectives used)",
    "perspective_description": "What could go wrong? (only when --preset or --perspectives used)",
    "output_schema": {
      "verdict": "PASS | WARN | FAIL",
      "confidence": "HIGH | MEDIUM | LOW",
      "key_insight": "Single sentence summary",
      "findings": [
        {
          "severity": "critical | significant | minor",
          "category": "security | architecture | performance | style",
          "description": "What was found",
          "location": "file:line if applicable",
          "recommendation": "How to address",
          "fix": "Specific action to resolve this finding",
          "why": "Root cause or rationale",
          "ref": "File path, spec anchor, or doc reference"
        }
      ],
      "recommendation": "Concrete next step",
      "schema_version": 2
    }
  }
}
```

---

## Perspectives

> **Perspectives & Presets:** Use `Read` tool on `skills/council/references/personas.md` for persona definitions, preset configurations, and custom perspective details.

**Auto-Escalation:** When `--preset` or `--perspectives` specifies more perspectives than the current judge count, automatically escalate judge count to match. The `--count` flag overrides auto-escalation.

---

## Named Perspectives

Named perspectives assign each judge a specific viewpoint. Pass `--perspectives="a,b,c"` for free-form names, or `--perspectives-file=<path>` for YAML with focus descriptions:

```bash
/council --perspectives="security-auditor,performance-critic,simplicity-advocate" validate src/auth/
/council --perspectives-file=.agents/perspectives/api-review.yaml validate src/api/
```

**YAML format** for `--perspectives-file`:

```yaml
perspectives:
  - name: security-auditor
    focus: Find security vulnerabilities and trust boundary violations
  - name: performance-critic
    focus: Identify performance bottlenecks and scaling risks
```

**Flag priority:** `--perspectives`/`--perspectives-file` override `--preset` perspectives. `--count` always overrides judge count. Without `--count`, judge count auto-escalates to match perspective count.

See [references/personas.md](references/personas.md) for all built-in presets and their perspective definitions.

---

## Explorer Sub-Agents

> **Explorer Details:** Use `Read` tool on `skills/council/references/explorers.md` for explorer architecture, prompts, sub-question generation, and timeout configuration.

**Summary:** Judges can spawn explorer sub-agents (`--explorers=N`, max 5) for parallel deep-dive research. Total agents = `judges * (1 + explorers)`, capped at MAX_AGENTS=12.

---

## Debate Phase (`--debate`)

> **Debate Protocol:** Use `Read` tool on `skills/council/references/debate-protocol.md` for full debate execution flow, R1-to-R2 verdict injection, timeout handling, and cost analysis.

**Summary:** Two-round adversarial review. R1 produces independent verdicts. R2 sends other judges' verdicts via backend messaging (`send_input` or `SendMessage`) for steel-manning and revision. Only supported with validate mode.

---

## Agent Prompts

> **Agent Prompts:** Use `Read` tool on `skills/council/references/agent-prompts.md` for judge prompts (default and perspective-based), consolidation prompt, and debate R2 message template.

---

## Consensus Rules

| Condition | Verdict |
|-----------|---------|
| All PASS | PASS |
| Any FAIL | FAIL |
| Mixed PASS/WARN | WARN |
| All WARN | WARN |

Disagreement handling:
- If Claude says PASS and Codex says FAIL → DISAGREE (surface both)
- Severity-weighted: Security FAIL outweighs style WARN

**DISAGREE resolution:** When vendors disagree, the spawner presents both positions with reasoning and defers to the user. No automatic tie-breaking — cross-vendor disagreement is a signal worth human attention.

---

## Output Format

> **Report Templates:** Use `Read` tool on `skills/council/references/output-format.md` for full report templates (validate, brainstorm, research) and debate report additions (verdict shifts, convergence detection).

All reports write to `.agents/council/YYYY-MM-DD-<type>-<target>.md`.


---

## Configuration

### Partial Completion

**Minimum quorum:** 1 agent. **Recommended:** 80% of judges. On timeout, proceed with remaining judges and note in report. On user cancellation, shutdown all judges and generate partial report with INCOMPLETE marker.

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `COUNCIL_TIMEOUT` | 120 | Agent timeout in seconds |
| `COUNCIL_CODEX_MODEL` | (user's default) | Override Codex model for --mixed. Omit `-m` flag to use the user's configured default. |
| `COUNCIL_CLAUDE_MODEL` | sonnet | Claude model for judges (sonnet default — use opus for high-stakes via `--profile=thorough`) |
| `COUNCIL_EXPLORER_MODEL` | sonnet | Model for explorer sub-agents |
| `COUNCIL_EXPLORER_TIMEOUT` | 60 | Explorer timeout in seconds |
| `COUNCIL_R2_TIMEOUT` | 90 | Maximum wait time for R2 debate completion after sending debate messages. Shorter than R1 since judges already have context. |

### Flags

| Flag | Description |
|------|-------------|
| `--deep` | 3 Claude agents instead of 2 |
| `--mixed` | Add 3 Codex agents |
| `--debate` | Enable adversarial debate round (2 rounds via backend messaging, same agents). Incompatible with `--quick`. |
| `--timeout=N` | Override timeout in seconds (default: 120) |
| `--perspectives="a,b,c"` | Custom perspective names (each name sets the judge's system prompt to adopt that viewpoint) |
| `--perspectives-file=<path>` | Load named perspectives from a YAML file (see Named Perspectives below) |
| `--preset=<name>` | Built-in persona preset (security-audit, architecture, research, ops, code-review, plan-review, doc-review, retrospective, product, developer-experience) |
| `--count=N` | Override agent count per vendor (e.g., `--count=4` = 4 Claude, or 4+4 with --mixed). Subject to MAX_AGENTS=12 cap. |
| `--explorers=N` | Explorer sub-agents per judge (default: 0, max: 5). Max effective value depends on judge count. Total agents capped at 12. |
| `--explorer-model=M` | Override explorer model (default: sonnet) |
| `--technique=<name>` | Brainstorm technique (scamper, six-hats, reverse). Case-insensitive. Only applicable to brainstorm mode — error if combined with validate/research. If omitted, unstructured brainstorm (current behavior). See `references/brainstorm-techniques.md`. |
| `--profile=<name>` | Model quality profile (thorough, balanced, fast). Error if unrecognized name. Overridden by `COUNCIL_CLAUDE_MODEL` env var (highest priority), then by explicit `--count`/`--deep`/`--mixed`. See `references/model-profiles.md`. |

---

## CLI Spawning Commands

> **CLI Spawning:** Use `Read` tool on `skills/council/references/cli-spawning.md` for team setup, Claude/Codex agent spawning, parallel execution, debate R2 commands, cleanup, and model selection.

---

## Examples

```bash
/council validate recent                                        # 2 judges, recent commits
/council --deep --preset=architecture research the auth system  # 3 judges with architecture personas
/council --mixed validate this plan                             # 3 Claude + 3 Codex
/council --deep --explorers=3 research upgrade patterns         # 12 agents (3 judges x 4)
/council --preset=security-audit --deep validate the API        # attacker, defender, compliance
/council --preset=doc-review validate README.md                  # 4 doc judges with named perspectives
/council brainstorm caching strategies for the API              # 2 judges explore options
/council --technique=scamper brainstorm API improvements               # structured SCAMPER brainstorm
/council --technique=six-hats brainstorm migration strategy            # parallel perspectives brainstorm
/council --profile=thorough validate the security architecture       # opus, 3 judges, 120s timeout
/council --profile=fast validate recent                               # haiku, 2 judges, 60s timeout
/council research Redis vs Memcached for session storage        # 2 judges assess trade-offs
/council validate the implementation plan in PLAN.md            # structured plan feedback
/council --preset=doc-review validate docs/ARCHITECTURE.md             # 4 doc review judges
/council --perspectives="security-auditor,perf-critic" validate src/   # named perspectives
/council --perspectives-file=.agents/perspectives/custom.yaml validate # perspectives from file
```

### Fast Single-Agent Validation

**User says:** `/council --quick validate recent`

**What happens:**
1. Agent gathers context (recent diffs, files) inline without spawning
2. Agent performs structured self-review using council output schema
3. Report written to `.agents/council/YYYY-MM-DD-quick-<target>.md` labeled `Mode: quick (single-agent)`

**Result:** Fast sanity check for routine validation (no cross-perspective insights or debate).

### Adversarial Debate Review

**User says:** `/council --debate validate the auth system`

**What happens:**
1. Agent spawns 2 judges (runtime-native backend) with independent perspectives
2. R1: Judges assess independently, write verdicts to `.agents/council/`
3. R2: Team lead sends other judges' verdicts via backend messaging
4. Judges revise positions based on cross-perspective evidence
5. Consolidation: Team lead computes consensus with convergence detection

**Result:** Two-round review with steel-manning and revision, useful for high-stakes decisions.

### Cross-Vendor Consensus with Explorers

**User says:** `/council --mixed --explorers=2 research Kubernetes upgrade strategies`

**What happens:**
1. Agent spawns 3 Claude judges + 3 Codex judges (6 total)
2. Each judge spawns 2 explorer sub-agents (6 x 3 = 18 total agents, exceeds MAX_AGENTS)
3. Agent auto-scales to 2 judges per vendor (4 x 3 = 12 agents at limit)
4. Explorers perform parallel deep-dives, return sub-findings to judges
5. Judges consolidate explorer findings with own research

**Result:** Cross-vendor research with deep exploration, capped at 12 total agents.

---

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| "Error: --quick and --debate are incompatible" | Both flags passed together | Use `--quick` for fast inline check OR `--debate` for multi-round review, not both |
| "Error: --debate is only supported with validate mode" | Debate flag used with brainstorm/research | Remove `--debate` or switch to validate mode — brainstorming/research have no PASS/FAIL verdicts |
| Council spawns fewer agents than expected | `--explorers=N` exceeds MAX_AGENTS (12) | Agent auto-scales judge count. Check report header for actual judge count. Reduce `--explorers` or use `--count` to manually set judges |
| Codex judges skipped in --mixed mode | Codex CLI not on PATH | Install Codex CLI (`brew install codex`). Model uses user's configured default — no specific model required. |
| No output files in `.agents/council/` | Permission error or disk full | Check directory permissions with `ls -ld .agents/council/`. Council auto-creates missing dirs. |
| Agent timeout after 120s | Slow file reads or network issues | Increase timeout with `--timeout=300` or check `COUNCIL_TIMEOUT` env var. Default: 120s. |

---

## Migration from /judge

`/council` replaces `/judge`. Migration:

| Old | New |
|-----|-----|
| `/judge recent` | `/council validate recent` |
| `/judge 2 opus` | `/council recent` (default) |
| `/judge 3 opus` | `/council --deep recent` |

The `/judge` skill is deprecated. Use `/council`.

---

## Multi-Agent Architecture

Council uses whatever multi-agent primitives your runtime provides. Each judge is a parallel subagent that writes output to a file and sends a minimal completion signal to the lead.

### Deliberation Protocol

The `--debate` flag implements the **deliberation protocol** pattern:
> Independent assessment → evidence exchange → position revision → convergence analysis

- **R1:** Spawn judges as parallel subagents. Each assesses independently, writes verdict to file, signals completion.
- **R2:** Lead sends other judges' verdict summaries to each judge via agent messaging. Judges revise and write R2 files.
- **Consolidation:** Lead reads all output files, computes consensus.
- **Cleanup:** Shut down judges via runtime's cleanup mechanism.

### Communication Rules

- **Judges → lead only.** Judges never message each other directly. This prevents anchoring.
- **Lead → judges.** Only the lead sends follow-ups (for debate R2).
- **No shared task mutation by judges.** Lead manages coordination state.

### Ralph Wiggum Compliance

Council maintains fresh-context isolation (Ralph Wiggum pattern) with one documented exception:

**`--debate` reuses judge context across R1 and R2.** This is intentional. Judges persist within a single atomic council invocation — they do NOT persist across separate council calls. The rationale:

- Judges benefit from their own R1 analytical context (reasoning chain, not just the verdict JSON) when evaluating other judges' positions in R2
- Re-spawning with only the verdict summary (~200 tokens) would lose the judge's working memory of WHY they reached their verdict
- The exception is bounded: max 2 rounds, within one invocation, with explicit cleanup

Without `--debate`, council is fully Ralph-compliant: each judge is a fresh spawn, executes once, writes output, and terminates.

### Degradation

If no multi-agent capability is detected, council falls back to `--quick` (inline single-agent review). If agent messaging is unavailable, `--debate` degrades to single-round review with a note in the report.

### Judge Naming

Convention: `council-YYYYMMDD-<target>` (e.g., `council-20260206-auth-system`).

Judge names: `judge-{N}` for independent judges (e.g., `judge-1`, `judge-2`), or `judge-{perspective}` when using presets/perspectives (e.g., `judge-error-paths`, `judge-feasibility`). Use the same logical names across both Codex and Claude backends.

---

## See Also

- `skills/vibe/SKILL.md` — Complexity + council for code validation (uses `--preset=code-review` when spec found)
- `skills/pre-mortem/SKILL.md` — Plan validation (uses `--preset=plan-review`, always 3 judges)
- `skills/post-mortem/SKILL.md` — Work wrap-up (uses `--preset=retrospective`, always 3 judges + retro)
- `skills/swarm/SKILL.md` — Multi-agent orchestration
- `skills/standards/SKILL.md` — Language-specific coding standards
- `skills/research/SKILL.md` — Codebase exploration (complementary to council research mode)
