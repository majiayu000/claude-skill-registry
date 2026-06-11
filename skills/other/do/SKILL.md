---
name: do
description: "Classify user requests and route to the correct agent + skill. Primary entry point for all delegated work."
user-invocable: true
argument-hint: "<request>"
allowed-tools:
  - Read
  - Bash
  - Grep
  - Glob
  - Skill
  - Task
routing:
  triggers:
    - "route task"
    - "classify request"
    - "which agent"
    - "delegate to skill"
    - "smart router"
  category: meta-tooling
---

# /do - Smart Router

/do is a **ROUTER**, not a worker. Classify requests, select the right agent + skill, dispatch. All execution goes to agents.

**Main thread:** (1) Classify, (2) Select agent+skill, (3) Dispatch, (4) Evaluate, (5) Re-route if needed, (6) Report.

Catching yourself reading source code, writing code, or analyzing — pause and route to an agent.

---

## The Completeness Standard

Do the whole thing — with tests and documentation.

- The answer is the finished product, not a plan. Plans organize execution; they don't replace it.
- Prefer the permanent solve and real fix over a workaround.
- If an agent returns partial work, route a follow-up to finish it.
- Search before building. Test before shipping.
- Decompose complexity into agent-sized tasks.

**The standard:** the result reads as "that's done," not "that's a start." Inject into agent prompts for Simple+ work.

Confidence in handling a task directly is a signal to route: direct handling skips domain knowledge, methodology, and references.

---

## Output Discipline

Every word the router prints and every dispatched agent prompt follows the **Dense-Complete Writing standard** (quoted verbatim in the Phase 4 injection). Full rules: `skills/shared-patterns/dense-complete-writing.md`.

**User sees:** phase banners, routing decision banner, brief post-agent summary (what changed, not how).
**Internal only:** routing JSON, classification reasoning, enhancement stacking (unless Verbose Routing ON).

---

## Instructions

### Phase Banners (MANDATORY)

Every phase MUST display a banner BEFORE executing: `/do > Phase N: PHASE_NAME — description...`

After Phase 2, display the full routing decision banner (`===` block). Both required: phase banners show *where*, the routing banner *what was decided*.

---

### Phase 1: CLASSIFY

**Goal**: Determine request complexity and whether routing is needed.

Read and follow the repository CLAUDE.md first — its conventions affect agent and skill selection.

| Complexity | Agent | Skill | Direct Action |
|------------|-------|-------|---------------|
| Trivial | No | No | **ONLY reading a file the user named by exact path** |
| Simple | **Yes** | Yes | Route to agent |
| Medium | **Required** | **Required** | Route to agent |
| Complex | Required (2+) | Required (2+) | Route to agent |

**Delegation is mandatory.** Everything beyond reading a user-named file is Simple+ and MUST route — without reasoning about whether you could handle it directly. When uncertain, classify UP.

**Progressive Depth**: For ambiguous complexity, start shallow; let the agent escalate. See `references/progressive-depth.md`.

**Common misclassifications** (NOT Trivial — route them): evaluating repos/URLs, opinions/recommendations, git operations, codebase questions (`explore-pipeline`), retro lookups (`retro`), comparisons.

**Maximize skill/agent/pipeline usage.** If one exists, USE IT.

**Named-pattern + escalation guide:** for which workflow pattern fits, the failure modes a workflow fights, and the "does this really need more compute?" cost gate, load `skills/workflow/references/workflow-patterns.md`.

**Check for parallel patterns FIRST**: 2+ independent failures or 3+ subtasks → `dispatching-parallel-agents`; broad research → `research-coordinator-engineer`; multi-agent coordination → `project-coordinator-engineer`; plan + "execute" → `subagent-driven-development`; new feature → `feature-lifecycle` (check `.feature/`; if present, run `feature-state.py status`). On 2+ independent items, dispatch all in parallel in one message.

**Optional: Force Direct** — OFF by default; applies only on explicit request.

**Creation Request Detection** (MANDATORY scan before Gate):

Creation signals:
- Verbs: "create", "scaffold", "build", "add new", "new [component]", "implement new"
- Targets: agent, skill, pipeline, hook, feature, plugin, workflow, voice profile
- Implicit: "I need a [component]", "build me a [component]"

If ANY creation signal AND complexity Simple+: set `is_creation = true`; Phase 4 Step 0 is MANDATORY (write ADR before dispatching).

**Not creation**: debugging, reviewing, fixing, refactoring, explaining, auditing existing components. When ambiguous, check whether output is a NEW file.

**Gate**: Complexity classified. If creation detected, output `[CREATION REQUEST DETECTED]` before routing banner. Display banner (ALL classifications). Trivial: handle directly. Simple+: proceed to Phase 2.

---

### Phase 2: ROUTE

**Goal**: Select the correct agent + skill. Semantic intent routing is primary, and the orchestrator does it itself — read the manifest in-session, no routing sub-dispatch (self-route beat the Haiku hop +8.1 accuracy points, zero new safety misses; `scripts/routing-ab-results/self-route-v1/VERDICT.md`, PR #776). The pre-router is a safety-net, not a short-circuit — the fast path below is the one exception, and it only commits routes the safety-net would force anyway. Prefer FORCE-labeled entries when intent matches semantically.

**Contract: read for INTENT.** Read what the user MEANS; trigger keywords are hints, never gates. Plain or non-native-English phrasing routes as well as jargon ("send my commits to the server" routes like "git push"). Cost: one in-session manifest read (~34 KB) on requests that miss the fast path — measured, accepted (`scripts/routing-ab-results/self-route-v1/VERDICT.md`, Cost section).

**Fast path: high-confidence force-route (run FIRST, before Step 0)**

Resolve SDIR as in Step 0, then run:

```bash
python3 "$SDIR/pre-route.py" --request "{user_request}" --json-compact
```

If the result has `"confidence": "high"` AND `"match_type": "force_route"` AND the skill is `pr-workflow` or a security skill: dispatch that pair directly. Skip Step 0 (manifest read + self-route), Step 1.5 (weights read), and Step 1 (pre-route already ran). Everything else stays mandatory: the routing banner (Step 3), Step 2 skill overrides where compatible, Phase 3 enhancements, and ALL Phase 4 injections — stamp the `[do-route]` marker with `health=-`. Agent: pre-route's `agent` when non-null, else the domain agent implied by Phase 1 classification, else `general-purpose`.

**Equivalence**: Step 1(a) already overrides any semantic pick with exactly these high-confidence force-routes, so the full flow always lands on this same force-routed skill. The fast path changes cost (the ~34 KB manifest read skipped), not behavior. Guards already ran inside pre-route, so idiom false-positives ("push back", "fish out") never reach the fast path. Any other result — no match, medium/low confidence, non-force match, or a skill outside pr-workflow/security — falls through to Step 0 unchanged.

**Step 0: Semantic intent routing (PRIMARY — orchestrator self-route)**

Generate the manifest, then route directly off it in-session. No routing sub-dispatch: the orchestrator reads the manifest and applies the rules below itself. (Self-route-v1 blind A/B, n=99: PROMOTE — +8.1 accuracy points over the Haiku hop, zero new safety-bucket misses, stub-tier 9→12; it fixes the agent-attribution failure and deletes a dispatch round trip. `scripts/routing-ab-results/self-route-v1/VERDICT.md`.)

```bash
SDIR="${HOME}/.claude/scripts"; [ -d "$SDIR" ] || SDIR="${HOME}/.hermes/scripts"; [ -d "$SDIR" ] || SDIR="${HOME}/.factory/scripts"; [ -d "$SDIR" ] || SDIR="${HOME}/.codex/scripts"; [ -d "$SDIR" ] || SDIR="${HOME}/.reasonix/scripts"
python3 "$SDIR/routing-manifest.py"
```

Given the user request and the manifest of available agents, skills, and pipelines, select the BEST agent+skill combination, and optionally a pipeline. Hold the decision internally as JSON (never printed; the `[do-route]` marker in Phase 4 is its only external trace):

```
{
  "agent": "agent-name or null",
  "skill": "skill-name or null",
  "pipeline": "pipeline-name or null",
  "reasoning": "one sentence why",
  "confidence": "high/medium/low"
}
```

Apply ALL of the following rules when deciding:

```
SECTION-INTEGRITY RULE (HARD CONSTRAINT — never violate):
- The `agent` field MUST be a name listed in the `AGENTS:` section of the manifest, or null. Never put a skill name in `agent`.
- The `skill` field MUST be a name listed in the `SKILLS:` section of the manifest, or null. Never put an agent name in `skill`.
- The `pipeline` field MUST be a name listed in the `PIPELINES:` section of the manifest, or null.
- If no agent fits the request, return `"agent": null` — DO NOT promote a skill into the `agent` slot. The router will fall back to a default agent (e.g. `general-purpose`) and pair it with your chosen skill.
- Skills marked `FORCE (process)` are still skills, not agents. They go in the `skill` field only. Example: `zsh-shell-config` is a SKILL — if it matches, set `"skill": "zsh-shell-config"` and pick a separate agent (or null) for `agent`.

FORCE-ROUTE RULE: Entries marked "FORCE" in the manifest MUST be selected when their domain clearly matches the user's intent. However, FORCE matching is SEMANTIC, not keyword-based. Match on what the user MEANS, not individual words. Examples:
- "push my changes" → pr-workflow (FORCE) ✓ (user means git push)
- "push back on this design" → NOT pr-workflow (user means resist/argue)
- "configure my fish shell" → fish-shell-config (FORCE) ✓ (user means Fish shell)
- "fish for bugs" → NOT fish-shell-config (user means search for bugs)
- "quick fix to the login page" → quick (FORCE) ✓ (user wants a small edit)
- "quick overview of the architecture" → NOT quick (user wants exploration)

PIPELINE-SELECTION RULE: The `pipeline` field is OPTIONAL and most requests should return `null`. Return a pipeline name ONLY when BOTH conditions hold:
(1) the user's intent SEMANTICALLY matches a pipeline's `triggers` or `description` in the PIPELINES section of the manifest, AND
(2) the request genuinely benefits from a multi-phase flow (research + write, scope + gather + synthesize, multi-wave review) — not just a single skill task.
Match on MEANING, not keyword overlap. If a single agent+skill satisfies the request, return `null` for pipeline. Examples:
- "write an article in vexjoy voice about X" → pipeline: "voice-writer" ✓ (multi-phase voice content generation matches the voice-writer pipeline)
- "research X with artifacts and sources" → pipeline: "research-pipeline" ✓ (formal SCOPE → GATHER → SYNTHESIZE → VALIDATE → DELIVER flow)
- "comprehensive review of these 8 files" → pipeline: "comprehensive-review" ✓ (multi-wave per-package review across many files)
- "fix the typo on line 42 of foo.py" → pipeline: null (single trivial edit, no pipeline needed)
- "debug this failing test" → pipeline: null (one agent+skill handles it; pipeline only if user asks for systematic debugging artifacts)
- "review this 10-line function" → pipeline: null (single skill, no multi-wave review warranted)
When in doubt, return null. A pipeline pick must be defensible against the manifest's PIPELINES section.

Rules:
- Pick the most specific match. "Go tests" → golang-general-engineer + go-patterns, not general-purpose.
- Agent handles the domain. Skill handles the methodology. Pick both when possible.
- If the request implies a task verb (review, debug, refactor, test), prefer skills that match that verb.
- If nothing matches well, return all nulls with reasoning.
- Prefer entries whose description semantically matches the request, not just keyword overlap.
- For GENUINE git / version-control operations — actually pushing code, committing files to a repository, or opening/merging a pull request — ALWAYS select pr-workflow. Do NOT route metaphorical or non-version-control uses of these words (e.g. 'commit to a decision/plan', 'merge ideas in your head', 'push back on a proposal') to pr-workflow.
- Return a single skill name as a string, not an array. If multiple skills are needed, pick the primary one.
```

**Step 0b: Apply the routing decision**

Use `agent` and `skill` fields directly; if `confidence` is "low", verify against INDEX files. The routing JSON is internal — never printed.

**Dispatch-time section validator (MANDATORY before every `Agent(subagent_type=...)` call).** A skill name in the `agent` field makes the harness reject the dispatch (`Agent type 'X' not found`). Assert the `agent` field maps to a name in the manifest's `AGENTS:` section. Pseudocode:

```
agents_section = grep_section(manifest, "AGENTS:", "SKILLS:")
skills_section = grep_section(manifest, "SKILLS:", "PIPELINES:")
agent_names = [first_token(line) for line in agents_section]
skill_names = [first_token(line) for line in skills_section]

if route.agent and route.agent not in agent_names:
    if route.agent in skill_names:
        # Cross-section slip: a skill landed in the agent slot.
        route.skill = route.skill or route.agent  # promote to skill if empty
        route.agent = None                         # clear bad agent pick
    record_misroute(reason="agent-slot held skill name", value=route.agent)

if route.agent is None:
    route.agent = "general-purpose"  # safe fallback; pair with chosen skill
```

If Step 0 cannot produce a defensible agent+skill pair, fall back to `general-purpose` + verification-before-completion.

Route to the simplest agent+skill that satisfies the request. On `[cross-repo]` output, route to `.claude/agents/` local agents. Route all code changes to domain agents.

**Step 1.5: Health evaluation (shadow-only instrumentation)**

Runs AFTER the semantic pick (Step 0/0b), BEFORE the Step 1 safety-net.

Once per /do, read the routing weights and score the semantic pick. Resolve SDIR as in Step 0, then run:

```bash
python3 "$SDIR/learning-db.py" route-weights --json
```

Call `health_adjust(semantic_pick, alternates, weights, force_route_flags)` (`scripts/lib/route_policy.py`). It returns `{final_pick, action, reason}` with `action` in `keep | demote | tiebreak`. The `action` is the policy's WOULD-action only.

**Shadow-only: the policy's would-action is recorded for the signal check (scripts/route-signal-check.py); the route is never altered.** The semantic pick always dispatches. Activation is gated on the first recorded negative signal — see docs/route-loop-validation.md.

Policy thresholds (for reading the recorded would-action, not for changing the route):

- Would-demote floor: `confidence < 0.30 AND failure >= 3 AND n >= 5`, toward a healthier alternate.
- Would-tiebreak: semantic confidence `< 0.35` AND an evidenced (`n >= 5`) healthier alternate supplied.
- Force-route/security pairs are hard-exempt — always `keep`. Exemption is by SKILL name and accepts force_route_flags as bare skill names or full `agent:skill` pairs.
- Evidence gate: `n < 5` or no row => `keep`.

**Always log the evaluation** to the T3 event stream: set `health_at_decision` to the picked pair's `confidence` scalar (a float, or `null` when the pair has no weight row); `n` and `failure` are separate fields. The recorder writes all three from the marker onto the per-dispatch DECISION event in `<CLAUDE_LEARNING_DIR>/route-events.jsonl`. Every route is scored even though nothing changes.

Carry the gate inputs on the routing marker so the recorder snapshots them at decision time — confidence alone cannot reconstruct the demote floor; it needs `n` and `failure` too. Append format and example: Phase 4 Step 2.

**Step 1: Deterministic safety-net** (`pre-route.py` — runs AFTER the semantic decision, never short-circuits it)

Use its result ONLY as a guardrail. Reuse the fast-path gate's pre-route output when it ran this turn; otherwise resolve SDIR as in Step 0 and run:

```bash
python3 "$SDIR/pre-route.py" --request "{user_request}" --json-compact
```

- **(a) Safety-critical force-route override.** If pre-route returns `"confidence": "high"` with a `force_route` match for `pr-workflow` or a security skill and the semantic pick disagrees, override to the force-route: genuine "push", "commit", "create PR", "merge" and security work MUST hit quality gates (lint, tests, CI). Record `match_type`.
- **(b) Guards stay active.** Its phrase/unigram guards suppress false matches (e.g. "fish out", metaphorical commit/merge). A guarded request — and otherwise — stays with the Step 0 semantic decision.

**Step 2: Apply skill override** (task verb overrides default skill)

Common overrides: "review" → systematic-code-review, "debug" → systematic-debugging, "refactor" → systematic-refactoring, "TDD" → test-driven-development. Full override table in `INDEX files`.

**Step 3: Display routing decision** (MANDATORY — FIRST visible output, before any work)

```
===================================================================
 ROUTING: [brief summary]
===================================================================
 Selected:
   -> Agent: [name] - [why]
   -> Skill: [name] - [why]
   -> Pipeline: PHASE1 → PHASE2 → ... (if pipeline; phases from skills/workflow/references/pipeline-index.json)
   -> Extra Rigor: [add verification patterns for code/security/testing tasks when needed]
 Invoking...
===================================================================
```

For Trivial: show `Classification: Trivial - [reason]` and `Handling directly (no agent/skill)`.

**Optional: Dry Run Mode** — OFF by default; when enabled, show the routing decision without executing.
**Optional: Verbose Routing** — OFF by default; when enabled, explain why each alternative was rejected.

**Learning capture is automatic** via hooks (full table in the Learning Capture section after Phase 4; ADR `learn-step-to-hook`).

**Gate**: Agent+skill selected. Banner displayed. Proceed to Phase 3.

---

### Phase 3: ENHANCE

**Goal**: Stack skills based on request signals. Use retro knowledge if present.

| Signal in Request | Enhancement to Add |
|-------------------|-------------------|
| Any substantive work (code, design, plan) | Add retro knowledge only when it materially helps the task |
| "comprehensive" / "thorough" / "full" | Add parallel reviewers (security + business + quality) |
| "with tests" / "production ready" | Append test-driven-development + verification-before-completion |
| "research needed" / "investigate first" | Prepend research-coordinator-engineer |
| "review" with 5+ files | Use parallel-code-review (3 reviewers) |
| Diff-scope review detected (comprehensive/full review on a real diff) | Run `python3 scripts/right-size-review.py --base {base} --head {head}` (or `--files N --packages M`); dispatch the matching tier — Tier 1→parallel-code-review (3), Tier 2→12, Tier 3→17, Tier 4→full (27). Escalate one tier on any CRITICAL finding; no tier signal → full behavior. |
| Complex implementation | Offer subagent-driven-development |
| "local only" / "no push" / "keep it local" / "don't commit" / "stay local" | Inject `local-only` constraint (see `shared-patterns/local-only.md`). Prepend: "**LOCAL-ONLY MODE.** Do not push, commit, create PRs, or deploy. All work stays on disk. Read-only git is fine." |
| Voice profile skill selected (voice-vexjoy, voice-dragonball-z, voice-andy-nemmity, etc.) | Stack `voice-writer` (its 13-phase pipeline is required for all voice content); the voice-* skill loads as the profile in Phase 1 (LOAD). |
| Vague verb + ambiguous object + no concrete file/symbol named + multiple plausible interpretations | `planning` (interview mode) — load `depth-first-interview.md` |
| Objective with done-criteria / "keep going until X" / "loop until done" | Stack `objective-loop` (skills/meta/objective-loop) |

**Interview-mode heuristic.** Fires when: short request (<15 words), verb in `{build, design, make, fix, figure out, set up}`, object with no file/symbol/path qualifier, no acceptance criteria.

| Example | Match? | Why |
|---|---|---|
| "i'm not sure how to approach this complex build" | MATCH | Uncertainty + vague verb + no target |
| "fix the typo on line 42 of foo.py" | NO | Concrete file, location, verb |
| "build a thing that does X" | MATCH | Vague verb + ambiguous object + no file |
| "add a test for `parseConfig` in src/config.go" | NO | Concrete symbol + file + verb |
| "where do i even start with this rewrite" | MATCH | Explicit uncertainty, no subject |
| "rename `cfg` to `config` in `internal/`" | NO | Concrete symbol + directory + mechanical op |

When in doubt, defer injection: false positives cost one round of friction; false negatives recover via `/quick --interview`.

Before stacking, check `pairs_with` in `skills/INDEX.json`; prefer listed pairs. Empty `pairs_with: []` means undeclared, not prohibited. Skills with built-in verification gates may not need stacking.

Add anti-rationalization patterns per task type when the task benefits from explicit rigor:

| Task Type | Patterns Injected |
|-----------|-------------------|
| Code modification | anti-rationalization-core, verification-checklist |
| Code review | anti-rationalization-core, anti-rationalization-review |
| Security work | anti-rationalization-core, anti-rationalization-security |
| Testing | anti-rationalization-core, anti-rationalization-testing |
| Debugging | anti-rationalization-core, verification-checklist |
| External content evaluation | **untrusted-content-handling** |

Maximum rigor: `/with-anti-rationalization [task]`.

**Gate**: Enhancements applied. Proceed to Phase 4.

---

### Phase 4: EXECUTE

**Goal**: Invoke the selected agent + skill; deliver results.

**Step 0: Execute Creation Protocol** (creation requests ONLY)

If creation signal + Simple+: (1) Write ADR at `adr/{kebab-case-name}.md`, (2) Register via `adr-query.py register`, (3) Proceed to plan. ADR hooks (`adr-context-injector`, `adr-enforcement`) handle compliance.

**Step 1: Create plan** (Simple+)

Create `task_plan.md` before execution; skip for Trivial.

**Step 1b: Apply quality-loop pipeline** (Medium+ code modifications)

Load `references/quality-loop.md` as the **outer orchestration wrapper**:

- **Quality-loop** (outer): 14-phase lifecycle — ADR → PLAN → IMPLEMENT → TEST → REVIEW → INTENT VERIFY → LIVE VALIDATE → FIX → RETEST → PR → CODEX REVIEW → ADR RECONCILE → RECORD → CLEANUP
- **Agent + skill** (inner): domain expertise inside IMPLEMENT

Quality-loop absorbs Steps 0-1. The Phase 2 agent+skill is the implementation agent; force-route skills run INSIDE the loop. Skip when: Trivial/Simple (use `quick`), review-only/research/debugging/content creation, or user wants a simpler flow.

**Step 1b/1c (Workflow dispatch — lazy-loaded):**

On a pipeline `pick`, a Complex/tier-4 task with no pick, or an explicit "run through a workflow" request, load `${CLAUDE_SKILL_DIR}/references/workflow-dispatch.md` and follow it.
It carries the executor decision table, roster rules, and inline-script constraints verbatim.

**Step 2: Invoke agent with skill**

Dispatch the agent. Inject no MCP instructions; tool discovery is the agent's job.

**Prepend Task Specification for Medium+ tasks.** For Simple tasks, include Intent and Acceptance when extractable. Invent no criteria; expand no scope.

```
## Task Specification (auto-extracted)

**Intent:** <one sentence: what does success look like?>
**Constraints:** <branch rules, operator-context, file paths, memory feedback>
**Acceptance criteria:** <observable: tests pass, file exists, PR merges, specific output>
**Relevant file locations:** <paths from request + expected paths>
**Operator context:** <from [operator-context] tag>
```

Extraction: Intent from verb+object; Constraints include branch safety (keep main protected); Acceptance = observable outcomes. For creation, add "Implementation must match ADR `<kebab-case-name>`."

Four injections (verbatim): completeness and density standards on Simple+; reference-loading and base instructions on all dispatches.

**MANDATORY: Reference loading.** MUST include: "Before starting work, read your agent .md file to find the Reference Loading Table. Load EVERY reference file whose signal matches this task. Load greedily — if multiple signals match, load all matching references."

**MANDATORY: Completeness standard.** MUST include: "Deliver the finished product. Ship the complete thing."

**MANDATORY: Dense-Complete Writing standard.** MUST include: "Write to the Dense-Complete Writing standard — your structural guide for everything you do. It governs your output, code comments, any skill or reference files you write, AND every one of your thinking turns: (1) shortest accurate word; (2) cut every word that carries no instruction, rule, or decision; (3) plain English, not jargon; (4) concrete over abstract; (5) heavy qualifications in separate short sentences; (6) Completeness: treat content as fixed and wording as negotiable: carry every required point through the draft, then choose the shortest plain words that say those points exactly. Say everything the task needs and not one word more. Report what changed, not how. Full rules: `skills/shared-patterns/dense-complete-writing.md`."

**MANDATORY: Base instructions.** MUST include: "Before starting work, also load `agents/base-instructions.md` for universal operational rules."

**MANDATORY: Stamp the routing marker on every routed agent prompt.** Prepend verbatim: `[do-route] agent={agent} skill={skill} complexity={complexity}` (use `skill=-` when routing agent-only). It is the SOLE signal `routing-decision-recorder` uses to record a `routing` row, reading `agent`/`skill` straight from it. Dispatches without it (pr-review sub-agents, nested fan-out) are correctly excluded from route-health. Stamp each agent in a roster.

Append the Step 1.5 gate inputs to the same marker line so the recorder snapshots the route's decision-time health: ` health={confidence} n={n} fail={failure} action={keep|demote|tiebreak}`, plus ` alts={k1,k2}` when alternates were passed. When the picked pair has no weight row, append ` health=-` only (the recorder writes null). Example: `[do-route] agent=python-general-engineer skill=test-driven-development complexity=Medium health=0.72 n=6 fail=0 action=keep`.

**Token budget signal (optional, documented).** Read `orchestration.token_budget` from `.claude/settings.json` (default 500000 when absent). Subtract a rough estimate of tokens spent; prepend to each agent prompt: "~{remaining} tokens available for this task; prioritize accordingly." Advisory, not a hard cap. Read the key once per session.

```bash
TOKEN_BUDGET=$(python3 -c "import json,sys; print(json.load(open('.claude/settings.json')).get('orchestration',{}).get('token_budget',500000))" 2>/dev/null || echo 500000)
```

**Inject thinking directive.** Prepend verbatim, no framing:

| Complexity | Thinking Directive |
|---|---|
| Trivial | None (no agent) |
| Simple | "Prioritize responding quickly rather than thinking deeply. When in doubt, respond directly." |
| Medium | None (adaptive) |
| Complex | "Think carefully and step-by-step before responding; this problem is harder than it looks." |

**Category overrides** (regardless of complexity): `thinking:slow` for security work, API/schema design, migrations, 5+ file reviews, architectural decisions; `thinking:fast` for lookups, status checks, single-function renames/refactors. Hooks capture the thinking class from dispatch metadata; the router sets the directive but records nothing.

**Verb-based model dispatch for Complex tasks (3+ data sources).** Extraction verbs use parallel Haiku readers; analysis verbs a single Opus agent (extraction 38% cheaper, 23% faster — A/B tested).

| Task verb class | Dispatch mode |
|---|---|
| list, count, extract, inventory, search, check, find, grep | Parallel Haiku readers (one Agent `model: "haiku"` per data source) → Opus synthesizer |
| review, audit, assess, analyze, debug, investigate, evaluate | Single Opus agent (direct) |

Simple/Medium: dispatch directly.

Route to agents that create feature branches; for file modifications, include "commit your changes on the branch". For `isolation: "worktree"` agents, inject `worktree-agent` rules: "Verify CWD contains .claude/worktrees/. Create feature branch before edits. Skip task_plan.md. Stage specific files only."

Non-org repos: up to 3 `/pr-review` → fix iterations before PR creation. Org-gated repos (via `scripts/classify-repo.py`): require user confirmation before EACH git action.

**Step 3: Handle multi-part requests**

Detect: "first...then", "and also", numbered lists, semicolons. Sequential dependencies run in order; independent items launch multiple Task tools in one message. Max parallelism: 10.

**Step 4: Auto-Pipeline Fallback** (no match AND complexity >= Simple)

Invoke `auto-pipeline` for unmatched requests. If none matches — or when uncertain — **ROUTE ANYWAY** to the closest agent + verification-before-completion as safety net.

**Lazy-completion check (before declaring done).** When an agent returns a "done" claim on an enumerable objective ("all N", a file list, a count), compare claimed scope vs objective scope; if claimed < objective, reject the early "done" and re-dispatch the remainder. See `skills/meta/do/references/lazy-completion-detector.md`. On a re-dispatch from this check, report the route failure (see Learning Capture, "Report routing failures").

**Gate**: Agent invoked, results delivered. Learning capture runs automatically (see note below).

---

### Learning Capture (automatic — no router step)

Hooks capture everything automatically. The router records by hand exactly one case: orchestrator-reported route failures it observes directly (see "Report routing failures" below) — the single deliberate manual capture step, by ADR design. Everything else is hook-driven:

| Capture | Hook | Event |
|---------|------|-------|
| Routing decision row (`{agent}:{skill}`, `category=effectiveness`) | `routing-decision-recorder` | PostToolUse:Agent |
| Routing outcome - validate pending (decision-row exists, re-queue late rows) | `routing-outcome-recorder` | SubagentStop |
| Routing outcome - finalize (boost/decay) on the next user turn | `routing-outcome-finalizer` | UserPromptSubmit |
| Routing outcome - session-end fallback for autonomous runs | `session-learning-recorder` | Stop |
| Right-sizing tier feedback (when a `rightsizing:` banner is emitted) | `routing-decision-recorder` | PostToolUse:Agent |
| Tool errors and fixes | `error-learner` | PostToolUse |
| Review findings | `review-capture` | PostToolUse:Agent |

These feed the routing loop: `learning-db.py route-health` reads the decision rows (denominator) and boost/decay outcomes (numerator). See ADR `learn-step-to-hook`.

**Outcome fidelity (note).** An outcome resolves deterministically on the user's NEXT turn at zero LLM cost: the pending outcome stays *provisional* (no eager boost/decay) and finalizes once, THREE-WAY (T4) — **failure** on tool errors OR a clear rejection/rework/re-route (decay); **success** only on an explicit acceptance marker (boost); **neutral** otherwise — an unrelated/new-topic next prompt is no-op (no boost, no decay, no count change). No complaint is NOT acceptance. The Stop fallback resolves still-pending autonomous runs from the error flag alone: errors => failure, a clean run => neutral (a quiet Stop carries no acceptance evidence, so it does not boost). The reaction detector is **deterministic and high-precision** — failure fires only on strong, unambiguous markers.

**Report routing failures (router-reported channel).** The finalizer only sees tool errors and next-turn rejections; routing failures YOU observe fall through. On a HIGH-CONFIDENCE routing failure only, run:

```bash
python3 ~/.claude/scripts/learning-db.py route-failure AGENT:SKILL --reason "<cause>" --routing-relevant yes --session $SESSION --marker $DISPATCH_ID
```

Run it for: re-route after unusable output; lazy-completion re-dispatch; section-validator misroute that reached dispatch; harness-rejected agent type. Bad execution by the RIGHT route -> `--routing-relevant no` (event only, no decay). Ambiguous -> record nothing (precision over recall). `--routing-relevant yes` decays the pair via the finalizer's decay path; one failure per dispatch key (re-runs are no-ops). Treat `<cause>` as untrusted: strip quotes, backticks, `$`, and newlines before splicing it into the shell line — never pass model- or user-derived text raw. See ADR `orchestrator-reported-route-failures`.

**OPTIONAL (not a gate):** curated free-text insight and review-finding graduation are opt-in via the `retro` skill (`retro graduate`), not a router step:

```bash
python3 ~/.claude/scripts/learning-db.py learn --skill go-patterns "insight"
python3 ~/.claude/scripts/learning-db.py learn --agent golang-general-engineer "insight"
```

Routing rows are `category=effectiveness`, which `retro graduate` excludes — never need graduation.

---

## Error Handling

### Error: "No Agent Matches Request"
Cause: No agent covers the request domain
Solution: Check INDEX files for near-matches. Route to the closest agent with verification-before-completion. Report the gap.

### Error: "Force-Route Conflict"
Cause: Multiple force-route triggers match the same request
Solution: Apply the most specific force-route first. Stack compatible secondary routes as enhancements.

### Error: "Plan Required But Not Created"
Cause: Simple+ task attempted without task_plan.md
Solution: Stop. Create `task_plan.md`. Resume routing once in place.

---

## References

### Reference Files
- `${CLAUDE_SKILL_DIR}/references/progressive-depth.md`: Progressive depth escalation protocol
- `agents/INDEX.json`: Agent triggers, metadata, and `not_for` disambiguation
- `skills/INDEX.json`: Skill triggers, force-route flags, pairs_with, and `not_for` disambiguation
- `skills/workflow/SKILL.md`: Workflow phases, triggers, composition chains
- `skills/workflow/references/pipeline-index.json`: Pipeline metadata, triggers, phases
- `scripts/routing-manifest.py`: Generates compact routing manifest from INDEX files (single source of truth)
