---
name: shape
description: Bridge WHAT (intent) to HOW (implementation). Use when spec is clear but approach is not. Triggers on "shape this", "how should I build", "implementation approach".
---

Decide HOW before building. Shape works dimension by dimension — each aspect that needs a HOW decision gets expert-informed choices the user selects from. This prevents collapsing multi-faceted decisions into a single recommendation.

For tasks with 1 dimension and an obvious approach, collapse to Step 1 → Step 5.

## Presentation

These rules govern HOW shape communicates across all steps.

- **Minto pyramid via AskUserQuestion** — Label = recommendation (conclusion first). Description = one-line tradeoff (always visible). Detail panel = structured plain text in AskUserQuestion's monospace preview box — short lines (~50 chars), ALL CAPS for section headers, dashes for bullets, ASCII tables for structure. No markdown formatting (renders as literal text, not rich text). The choice prompt IS the presentation — no text walls before it.
- **Batch independent choices** — Non-conflicting dimensions go into a single AskUserQuestion (up to 4 questions per call). Only separate dimensions where one choice constrains another.
- **Techniques are internal** — Apply reasoning techniques in your thinking. Present the insights they produce in plain language. Never name techniques (inversion, Musashi, obstacle-as-path, etc.) in user-facing output.
- **Infer, state, ask only if ambiguous** — Classify domain type, reversibility, and expert selection yourself. State your classification as a brief line. Only prompt via AskUserQuestion when genuinely unclear.
- **Brief scannable output** — Bullets over paragraphs. Findings in 1-2 lines each. No text walls between prompts.

## Workflow

### Step 1: Extract

Parse the intent brief (or user's spec). Identify:
- Goal and constraints
- Shaping dimensions — aspects needing HOW decisions (architecture, data model, API design, testing, deployment, etc.)

Search the codebase for existing patterns, conventions, and prior art. Then search beyond — GitHub repos, web results, documentation — for how others have solved this. Prior art search is a distinct step from codebase grep.

Summarize research internally. Present only what's relevant to shaping dimensions — 5-10 brief bullets, not architecture reports. The user needs to know what exists and what constrains the HOW, not a tour of the entire codebase.

**Dichotomy of control** — Ask via AskUserQuestion: what's actually within the user's control? Scope the shaping to match their timeline and accountability. Work that depends on other teams, external approvals, or infrastructure they can't change should be documented as externalities, not shaped as if the user can decide them.

Run the entry audit internally — do not output to user:
- [ ] Spec drives behavior? (not extracted from existing code — extracting spec from implementation codifies bugs)
- [ ] Constraints are declarative? (invariants and valid outcome spaces, not procedural instructions)
- [ ] Verification criteria defined? ("How will I know this is right?" is a design question, not a testing question)
- [ ] Scope within user's control? (externalities identified and separated)

Only surface failures via AskUserQuestion. If all checks pass, proceed silently. A spec that can't be verified isn't a spec.

Present findings and proposed dimensions as brief scannable bullets.

### Step 2: Scope

Infer the domain type — high-stakes (security, financial, compliance) or exploratory (prototypes, spikes). State your classification as a brief line. High-stakes domains get deeper analysis per dimension. Exploratory domains get lighter treatment. Only ask via AskUserQuestion if genuinely ambiguous.

Present dimensions to the user via AskUserQuestion (multiSelect): "Which aspects matter for this task?"

Not every task needs every dimension shaped. A CSS fix needs zero. A new API endpoint might need architecture + data model + testing. The user decides.

Infer reversibility per scoped dimension: Type 2 (reversible — move fast) or Type 1 (irreversible — deep analysis). State classifications as a brief line. Only ask if ambiguous. This sets the depth of shaping per dimension.

### Step 3: Shape loop

For each scoped dimension:

1. **Consult experts** — Invoke the consult skill via the Skill tool for expert perspectives on this dimension. Frame the prompt so consult produces distinct approaches, not a single recommendation:

   `Skill: hope:consult, args: "Panel: For [dimension] in [context], what are 2-3 distinct approaches? Surface where experts disagree — I need choices with tradeoffs, not consensus."`

   Take consult's output and reshape it into AskUserQuestion choices (see step 3 below). State who was consulted in a brief line.

2. **Reason through** — Apply relevant techniques internally based on domain type and dimension. These are your reasoning toolkit — use them, present the insights they produce in plain language:
   - Search for prior art and existing libraries — every library not written is ~1000 bugs avoided. Burden of proof is on building, not using. (always)
   - Identify failure modes, make broken states unrepresentable — what remains is the solution space. (high-stakes or irreversible dimensions)
   - Question complexity cost — can this be deleted instead of built? Is this earning its complexity? (always)
   - Ask how constraints improve the design, not just limit it. (when constraints feel blocking)
   - Check that broken states can't be expressed in types — if they can, the design is incomplete. (high-stakes domains)
   - Check that failure paths are first-class typed values, not escape hatches that break composition. (API and data dimensions)
   - Check that structure follows user journeys, not technical layers. (architecture dimensions)

3. **Present choices** — Use AskUserQuestion with detail panels. Each option:
   - Label: the approach name, mark recommended with "(Recommended)"
   - Description: one-line tradeoff
   - Detail panel (monospace preview): what you'd build, why the expert favors it (grounded in their work), what you gain and pay, when it shines vs. breaks — plain text, short lines, ALL CAPS headers
   - Always include an "Explore further" option

Batch non-conflicting dimensions into a single AskUserQuestion. Separate dimensions where one choice constrains another.

If "Explore further," regenerate choices with deeper analysis. If user reframes the dimension itself, restart expert selection. User can add new dimensions mid-loop if experts surface something unconsidered.

### Step 4: Integrate

After all dimensions are resolved:

**Cross-dimension tension check** — Two good individual choices can conflict when combined.

**Pre-mortem** — Distinct from per-dimension failure analysis. Imagine the shaped solution shipped and failed six months later. Why? This catches adoption, timing, political, and integration failures that per-dimension analysis misses. Consider at minimum: will users discover this feature? Can it be used without a mouse? What happens during concurrent operations (e.g., user interacts while system is streaming)? What's the maintenance burden when adjacent code changes?

**Second-order effects** — For each dimension choice, explicitly ask: "what does this prevent us from doing in 6-12 months?" List the closed-off futures as visible text. This analysis is not optional — every choice closes doors. The question is whether those doors matter.

Present tensions, pre-mortem risks, and second-order effects as one AskUserQuestion with detail panels showing each scenario. Include:
- **Lock it in** — proceed to emit
- **Revisit a dimension** — return to shape loop for a specific aspect
- **Explore further** — deeper analysis before deciding

If after genuine analysis there are truly no tensions, no risks, and no closed-off futures worth surfacing — state that briefly and proceed to Step 5.

### Step 5: Emit

Run the exit audit internally — do not output to user:
- [ ] Shape discovered, not imposed? (emerged from constraints, not justified backwards from a solution)
- [ ] Laws → Transformations → Compositions order? (axioms first, then structure-preserving transforms, then context-varying compositions)
- [ ] Inversion of control applied? (data drives computation, composition drives architecture, properties drive correctness)
- [ ] Fits in one head? (one person can hold the entire shape in working memory — hard gate, not preference)

Only surface failures. If all checks pass, proceed silently.

Compress the shape to one sentence explaining why it exists — the semantic checksum. If you can't, the shape isn't clear yet. Revise before emitting.

Produce the shape document:
- **Approach** — The concrete how per dimension, with rationale
- **Codebase findings** — What exists, what the approach builds on
- **Resolved tensions** — Where perspectives disagreed and how the user resolved it
- **Risks** — What could go wrong, especially irreversible changes
- **First step** — One atomic action that produces a visible artifact

## Boundaries

Shape surfaces expert-informed choices; user owns architecture. Expert options are advice, not prescriptions. When uncertain about risk, bias toward more human involvement. When interpretations diverge, present options — never pick for the user.
