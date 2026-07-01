---
name: brainstorm
description: Explore vague or ambitious ideas into a right-sized requirements-only plan. Use when the user wants to brainstorm, think through scope, decide what to build, or needs collaborative product framing before planning — not for a decisive verdict on whether to adopt or switch to a specific external technology, library, or platform.
metadata:
  short-description: Collaborative requirements framing → requirements-only odin-plan/v1 artifact
---

# Brainstorm a Feature or Improvement

`Op: extend` — every brainstorm artifact is a load-bearing addition to the repo's decision record.

Brainstorming answers **WHAT** to build through collaborative dialogue. It precedes `/plan`, which enriches the same artifact with **HOW**.

The durable output is a **requirements-only plan** under `docs/plans/`. Write it with `artifact_contract: odin-plan/v1`, `artifact_readiness: requirements-only`, and `source: brainstorm` so planning does not invent product behavior, scope boundaries, or success criteria.

This skill does not implement code. It explores, clarifies, and documents decisions for later planning or execution.

## Core Principles

1. **Assess scope first** — match ceremony to the size and ambiguity of the work.
2. **Be a thinking partner** — suggest alternatives, challenge assumptions, and explore what-ifs instead of only extracting requirements.
3. **Resolve product decisions here** — user-facing behavior, scope boundaries, and success criteria belong in this workflow. Detailed implementation belongs in planning.
4. **Keep implementation out by default** — do not include libraries, schemas, endpoints, file layouts, or code-level design unless the brainstorm itself is inherently technical or architectural.
5. **Right-size the artifact** — simple work gets a compact requirements-only plan or brief alignment. Larger work gets a fuller plan. Do not add ceremony that does not help planning.
6. **Apply YAGNI to carrying cost, not coding effort** — prefer the simplest approach that delivers meaningful value. Avoid speculative complexity, but low-cost polish or delight is worth including when its ongoing cost is small.

## Interaction Rules

These rules apply to every brainstorm, including the universal (non-software) flow routed to `references/universal-brainstorming.md`.

1. **Ask one question at a time** — one per turn, even when sub-questions feel related.
2. **Prefer single-select multiple choice** — use it when choosing one direction, one priority, or one next step.
3. **Use multi-select rarely and intentionally** — only for compatible sets such as goals, constraints, non-goals, or success criteria that can all coexist.
4. **Default to the platform's blocking question tool** — use `AskUserQuestion` in Claude Code (call `ToolSearch` with `select:AskUserQuestion` first if its schema is not loaded), `request_user_input` in Codex, `ask_question` in Antigravity CLI (`agy`), `ask_user` in Pi. Fall back to numbered options in chat only when no blocking tool exists or the call errors — not because a schema load is required. Never silently skip the question. **Exception — visual-probe gate:** on an inherently visual topic, the first shape/behavior/state/layout/flow/diagram decision must be preceded by the separate text-vs-visual offer before it is raised. See Phase 1.3.
5. **Use an open-ended question only when the question is genuinely open** — drop the blocking tool when the answer is inherently narrative, when options would steer a diagnostic answer, or when you cannot write 3-4 genuinely distinct, plausibly-correct options without padding.
6. **Open-ended questions must be specific enough to elicit a substantive answer** — give the user something concrete to anchor on. Good: *"What is the most concrete thing someone's already done about this — paid for it, built a workaround, quit a tool over it?"* Too thin: *"What's your take?"*

## Output Guidance

- **Keep outputs concise** — short sections, brief bullets, only enough detail to support the next decision.
- **Repo-relative paths** — when referencing files, use paths relative to the repo root, never absolute paths.

## Model Tiers

Sub-agent dispatch is tiered by task shape, never hardcoded to a model name:

- **Extraction tier** — the grounding scout: retrieval and quoting work. Use the cheapest capable model when the harness exposes a known override.
- **Generation tier** — the claim verifier: evidence-driven mechanical verification. Use the mid-tier model when a known override exists.
- **Ceiling tier** — the dialogue itself runs in the main conversation; nothing is dispatched for it.

**Degradation rule.** When per-agent model selection is unavailable, dispatch on the inherited model and control cost through read budgets and output caps.

## Feature Description

<feature_description> #$ARGUMENTS </feature_description>

If the feature description above is empty, ask: "What would you like to explore? Please describe the feature, problem, or improvement you're thinking about." Do not proceed until you have one.

## Execution Flow

### Phase 0: Resume, Assess, and Route

#### 0.0 Resolve Output Mode

Determine `OUTPUT_FORMAT` before any other phase fires. Output mode is **exclusive** — the plan is written as markdown (`.md`) OR HTML (`.html`), never both. Precedence: in-prompt request > user-stated preference > default (`md`), with a hard pipeline-mode override.

1. **In-prompt request.** Reason over the prompt for a request about *this document's* output format, expressed as `output:` shorthand or plain language. On an explicit format, match case-insensitively to `md`/`html`, and ignore the `output:` token when reading the rest of the prompt as the feature description. Distinguish a format request from format as subject matter: "explore an HTML export feature" is the work, not a doc-format request.
   - `output:` alone → fall through.
   - `output:<unknown>` → drop the token, fall through, and emit a one-line note after final resolution: `Ignored unknown output: '<value>' — using <resolved_format> instead.`
2. **User-stated preference.** Honor an output-format preference already in context (earlier in session, memory, or active instructions) over config.
3. **Default.** `OUTPUT_FORMAT=md`.
4. **Pipeline override.** When invoked from a `disable-model-invocation` context, force `OUTPUT_FORMAT=md` regardless of steps 1-3. Later steps parse markdown reliably.

**Load rendering references only at Phase 3.** Read `references/markdown-rendering.md` for `md` or `references/html-rendering.md` for `html` when composing the doc. Loading them now would carry 200+ lines through the entire dialogue.

#### 0.1 Resume Existing Work When Appropriate

If the user references an existing brainstorm topic or document, or there is an obvious recent matching plan in `docs/plans/` with `artifact_contract: odin-plan/v1`, `artifact_readiness: requirements-only`, and `source: brainstorm`:

- Read the document.
- Confirm: "Found an existing requirements-only plan for [topic]. Continue from this, or start fresh?"
- If resuming, summarize state briefly, continue from existing decisions and outstanding questions, and update the existing document instead of creating a duplicate.
- Resume preserves the existing artifact's format, except pipeline mode, which forces `md`.

#### 0.1b Classify Task Domain

Classify whether this is a software task: does it involve building, modifying, or architecting software?

- **Software** — continue to Phase 0.2.
- **Non-software brainstorming** — route to `references/universal-brainstorming.md`; it replaces Phases 0.2-4. The Core Principles and Interaction Rules still apply.
- **Neither** — respond directly for quick-help, factual, or single-step requests.

**Verdict-shape carve-out.** A request weighing whether to **adopt / switch to / replace** a *named external technology, library, pattern, platform, or architecture* is software. Classify it as software so the 0.1c gate can catch it.

#### 0.1c Route a Verdict Question to `/pov`

A brainstorm scopes **what to build** once a direction is chosen. Deciding **whether to adopt, switch to, or replace** a *specific external candidate* judged against this project is `/pov`'s job.

The verdict shape — all three hold:

- a **named external candidate** (one specific thing, or a bounded set the user already named);
- a **whether-to-commit intent** (adopt / switch to / migrate to / replace with / revisit);
- judged **against this project**, not a neutral explainer.

Open-ended design or scoping stays here. The whether-to-commit trigger separates verdict from exploration.

When the shape matches, offer — do not silently switch. Use the blocking question tool with one simple choice:

- **Yes** → invoke `/pov` with the candidate(s), framed intent, and links.
- **No** → stay here; the brainstorm continues.

Name `/pov` by what it does (project-grounded verdict), never as internal machinery. On accept, invoke `/pov` via the platform's skill-invocation primitive, passing the crisp frame. Do not merely tell the user to type `/pov`.

The same offer applies whenever the dialogue later clarifies into the verdict shape.

#### 0.2 Assess Whether Brainstorming Is Needed

**Clear requirements indicators:** specific acceptance criteria, referenced existing patterns, exact expected behavior, constrained scope.

If requirements are already clear, keep the interaction brief. Confirm understanding and present concise next-step options. Skip Phase 1.1 and 1.2; go straight to Phase 1.3 or Phase 2.5 in announce-mode, then Phase 3.

#### 0.3 Assess Scope

Use the feature description plus a light repo scan to classify:

- **Lightweight** — small, well-bounded, low ambiguity.
- **Standard** — normal feature or bounded refactor with some decisions.
- **Deep** — cross-cutting, strategic, or highly ambiguous.

If scope is unclear, ask one targeted question.

**Deep sub-mode: feature vs product.** For Deep scope, also classify:

- **Deep — feature** (default): existing product shape anchors decisions.
- **Deep — product**: the brainstorm must establish product shape.

Product-tier triggers additional Phase 1.2 questions and additional plan sections.

**Visual probe tripwire.** If the feature is inherently visual or spatial — drawing/canvas tools, UI layout, interaction states, charts, diagrams, animation, maps, timelines — read `references/visual-probes.md` now. The gate is pending; do not offer the visual path until the first concrete shape/behavior decision.

### Phase 1: Understand the Idea

#### 1.1 Existing Context Scan

Scan the repo before substantive brainstorming. Match depth to scope.

**Lightweight** — search for the topic, check for similar existing work, move on.

**Standard and Deep** — two passes:

*Constraint Check (inline)* — source the agnostic orientation from the shared repo-grounding profile cache instead of re-reading files every run. Set `SKILL_DIR` to this skill's directory and run:

```bash
SKILL_DIR="<absolute path of the directory containing the SKILL.md you just read>"
python3 "$SKILL_DIR/scripts/repo-profile-cache.py" get
```

On `HIT`, load the profile JSON and take `conventions.strategy` for strategy, `vocabulary` for concepts, and `conventions` for workflow/scope constraints. On `MISS`, dispatch a generic subagent with `references/agents/repo-profiler.md` to derive the profile, write its JSON to a file, then persist with `python3 "$SKILL_DIR/scripts/repo-profile-cache.py" put <file>`. On `NO-CACHE`, derive inline and skip `put`. The cache is an optimization, never a correctness dependency.

*Topic Scan (grounding scout)* — create a scratch dir at `/tmp/odin/brainstorm/<run-id>/`, then dispatch one extraction-tier subagent. Scout prompt:

> Gather grounding for a requirements brainstorm about **{topic}** in this repo. Search first with native file-search and content-search tools, then read targeted sections — budget ~20 reads, prefer ranges over whole files. Find: whether something similar exists, relevant artifacts (plans, specs, feature docs), adjacent examples, and the current state of anything the topic touches. Write a **grounding dossier** to `{scratch-dir}/grounding.md`: at most 150 lines of verbatim quotes and short snippets, each with a `file:line` pointer. Extraction only — quote what the repo says; do not interpret or propose. Return only a gist: 3-5 lines summarizing what the dossier holds, plus its absolute path.

Carry only the gist in the dialogue. Read the dossier on demand.

Two rules govern technical depth:

1. **Verify before claiming** — when the brainstorm touches checkable infrastructure, read the relevant source files to confirm. Any absence claim must be verified; if not, label it an unverified assumption.
2. **Defer design decisions to planning** — schemas, migrations, endpoints, deployment topology belong in planning, unless the brainstorm is itself about a technical or architectural decision.

**Slack context** (opt-in, Standard and Deep only) — never auto-dispatch. Route by condition:

- Tools available + user asked: read `references/agents/slack-researcher.md` and dispatch a generic subagent.
- Tools available + user did not ask: note: "Slack tools detected. Ask me to search Slack for organizational context at any point."
- No tools + user asked: note: "Slack context was requested but no Slack tools are available. Install and authenticate a Slack plugin to enable search."

#### 1.2 Product Pressure Test

Before generating approaches, scan the opening for rigor gaps. This is agent-internal analysis, not a user-facing checklist. Raise only scope-appropriate gaps as questions during Phase 1.3.

**Lightweight:**
- Is this solving the real user problem?
- Are we duplicating something that already covers this?
- Is there a clearly better framing with near-zero extra cost?

**Standard:**
- **Evidence gap** — asserts want/need but points to no observable action.
- **Specificity gap** — beneficiary is too abstract to design for.
- **Counterfactual gap** — no picture of what users do today or what changes if nothing ships.
- **Attachment gap** — treats a solution shape as the thing to build without examining smaller forms.

Synthesis questions (agent weighs internally):
- Is there a nearby framing that creates more user value without more carrying cost?
- Given project state, user goal, and constraints, what is the highest-leverage move right now?

**Deep:** Standard lenses plus — is this a local patch, or does it move the broader system toward where it wants to be?

**Deep — product:** Deep plus durability gap, adjacent-product risk, and failure conditions. These feed Scope Boundaries and Dependencies / Assumptions in the plan.

#### 1.3 Collaborative Dialogue

Follow the Interaction Rules. Use the blocking question tool when available.

**Visual-probe gate.** If the Phase 0.3 tripwire fired, the **first** decision about shape, behavior, state, layout, flow, or a diagram must go through the text-vs-visual offer from `references/visual-probes.md` before it is raised in any form. The offer is its own prior question with two options: sketch rough options in a local browser, or describe them in chat. ASCII or text mockups inside another question do **not** satisfy the gate.

Guidelines:
- Ask what the user is already thinking before offering ideas.
- Start broad (problem, users, value) then narrow (constraints, exclusions, edge cases).
- Rigor probes fire before Phase 2 as separate open-ended probes, one per gap.
- Clarify the problem frame, validate assumptions, ask about success criteria.
- Make requirements concrete enough that planning will not need to invent behavior.
- Surface dependencies only when they materially affect scope.
- Resolve product decisions here; leave technical implementation choices for planning.
- Bring ideas, alternatives, and challenges instead of only interviewing.

**Before exiting Phase 1.3: integration check.** Combine what the user has said and surface any non-obvious consequence the dialogue has not probed. Probe it now.

**Exit condition:** continue until the idea is clear AND no integration-check questions are pending, OR the user explicitly wants to proceed.

### Phase 2: Explore Approaches

If multiple plausible directions remain, propose **2-3 concrete approaches**. Otherwise state the recommended direction directly.

Use at least one non-obvious angle — inversion, constraint removal, or analogy from another domain. Hold each to an anti-genericness test: if it would appear in a generic listicle, sharpen it against the grounding dossier or drop it.

Present approaches first, then evaluate. Let the user see all options before the recommendation.

When useful, include one deliberately higher-upside alternative as a challenger option alongside the baseline.

At product tier, alternatives differ on *what* is built, not *how*.

For each approach:
- Brief description (2-3 sentences)
- Pros and cons
- Key risks or unknowns
- When it is best suited

**Approach granularity: mechanism / product shape, not architecture.** Name mechanism-level distinctions and product-relevant trade-offs. Do NOT name implementation specifics — column names, table names, file paths, service classes, JSON shapes, exact method names. Those are `/plan`'s job.

After presenting all approaches, state the recommendation and explain why. Prefer simpler solutions when added complexity creates real carrying cost.

If relevant, call out whether the choice is: reuse an existing pattern, extend an existing capability, or build net new.

### Phase 2.5: Synthesis Summary

**STOP. Before composing the synthesis, read `references/synthesis-summary.md`.** The two-stage shape, four scoping synthesis sections, keep tests, and routing all live there.

Surface a scoping synthesis before Phase 3 writes the plan — the user's last chance to correct scope.

**Path A vs Path B:** gated by whether any blocking question fired AND the scope tier.

- **Path A** — no blocking questions fired AND tier is Lightweight: announce-mode. Emit "What we're building" prose only (1-3 sentences), then proceed to Phase 3 in the same turn. No confirmation question.
- **Path B** — at least one blocking question fired, OR tier is Standard / Deep: full tier-aware scoping synthesis with confirmation gate.

#### 2.6 Claim Verification (inside the Path B confirmation wait)

When the upcoming plan will assert checkable repo claims, dispatch one generation-tier verifier at the same moment the Path B confirmation goes up. Pass it the claim list and the grounding dossier path. It verifies each claim directly against the codebase — budget ~15 targeted reads — and returns per-claim verdicts: **confirmed** (with `file:line`), **refuted** (with contradicting evidence), or **unverifiable**.

Consume verdicts at Phase 3: correct refuted claims, label unverifiable ones as explicit assumptions.

Skip when Path A fires, when the doc makes no checkable claims, or on the non-software route.

### Phase 3: Capture the Requirements-Only Plan

Write or update a requirements-only plan only when the conversation produced durable decisions worth preserving — see `references/brainstorm-sections.md` "Decide whether a doc is warranted at all".

When a doc is warranted, compose it using:

- `references/brainstorm-sections.md` — section contract.
- The format-specific rendering reference for the resolved `OUTPUT_FORMAT`.

**Write tight.** Hold every section to the prose-economy discipline in `references/brainstorm-sections.md`.

Write to `docs/plans/YYYY-MM-DD-NNN-<type>-<topic>-plan.<md|html>`. Include `artifact_contract: odin-plan/v1`, `artifact_readiness: requirements-only`, and `source: brainstorm`. Title is `<Name> - Plan`. Keep the doc light and standalone-readable: a Goal Capsule and an ODIN spec outline. Do not emit a Goal Launch Block or Reader Index.

#### Vocabulary Capture

**Skip if `CONCEPTS.md` does not exist at repo root** — creation is owned by other skills.

Run this after the plan is written. Scan the dialogue and the ODIN spec outline for **resolved** domain terms — terms where the conversation pinned down a precise local meaning. For each: add if missing, refine if new precision surfaced, no action if consistent. Domain entities, named processes, and status concepts with project-specific meaning only — not file paths, class names, or implementation decisions.

### Phase 4: Handoff

Read `references/handoff.md` now — before presenting options. The option set, visibility conditions, per-selection dispatch instructions, and closing summary formats live there.

## Constitutional Rules

1. **Op-cell is `extend`.** every durable brainstorm artifact is an addition to the repo's decision record.
2. **Markdown is canonical; HTML is opt-in.** The plan is written as `md` OR `html`, never both.
3. **No implementation detail by default.** Libraries, schemas, endpoints, file layouts stay out unless the brainstorm is inherently technical.
4. **One question at a time.** No stacked questions.
5. **Repo-relative paths only.** Absolute paths break portability.
6. **If any rule here conflicts with `~/.claude/claude/system-prompt-baseline.md`, the baseline wins.**

## Validation Gates

| Gate | Pass Criteria | Blocking |
|---|---|---|
| Feature description captured | Non-empty feature description before Phase 1 | Yes |
| Verdict-shape routed | `/pov` offered when the input matches the verdict shape | No (user may decline) |
| Domain classified | Software / non-software / neither classified before Phase 1 | Yes |
| Scope tier assigned | Lightweight / Standard / Deep assigned before Phase 1.3 | Yes |
| Profile resolved | Cache hit, miss-derived, or NO-CACHE fallback handled | No |
| Grounding dossier written | Scout writes `{scratch}/grounding.md` when a scout runs | Yes (when scout dispatched) |
| Rigor gaps probed | every Phase 1.2 gap present has been asked before Phase 2 | Yes |
| Visual gate observed | First visual decision goes through text-vs-visual offer | Yes (when tripwire fired) |
| Synthesis read first | `references/synthesis-summary.md` read before Phase 2.5 | Yes |
| Doc warranted check | Decision to write or skip the plan is explicit per `brainstorm-sections.md` | Yes |
| Rendering reference read | `markdown-rendering.md` or `html-rendering.md` read before compose | Yes |
| Handoff read | `references/handoff.md` read before presenting Phase 4 options | Yes |

## Anti-patterns

- **Guessing the verdict shape.** Offer `/pov`; do not silently route.
- **Stacking questions.** One per turn.
- **Loading rendering references early.** Phase 3 only.
- **Writing implementation detail into the ODIN spec outline.** Defer to `/plan`.
- **Skipping the synthesis on substantive pre-loaded openings.** Tier guards Path A vs Path B.
- **Absolute paths in artifacts.** Always repo-relative.
- **Pasting the internal three-bucket draft verbatim.** The user sees only the compressed Stage 2 synthesis.

## See also / Disambiguation

- **vs `/pov`** — `/pov` returns a decisive, project-grounded verdict on a specific external candidate. Brainstorm scopes *what* to build once a direction is chosen.
- **vs `/ideate`** — `ideate` generates divergent candidate directions from an open field with reject-by-default critique. Brainstorm dialogues a single idea into scope.
- **vs `/plan`** — `/plan` turns clarified requirements into implementation units. Brainstorm produces the requirements-only input.
- **vs `/work`** — `/work` implements. Brainstorm does not write code.
