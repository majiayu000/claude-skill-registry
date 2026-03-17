---
name: simulate-elite-experts
description: |
  Simulate high-stakes reasoning by modeling how top experts in the relevant domain would think, disagree, and converge on a decision.
  Use when users ask to role-play strongest minds, compare elite viewpoints, or ask: what would be a good group of people to explore X, and what would they say.
  Trigger for prompts like "think like world-class experts", "simulate top domain specialists", "role-play strongest domain people", and "use four-lens dialogue".
---

# Simulate Elite Experts

## Applicability Pre-Check (Gate 0)

Before running the full framework, evaluate 3 dimensions to decide whether this tool is appropriate:

1. **Complexity**: Does the problem involve multiple stakeholders, competing constraints, or non-obvious tradeoffs?
   - Yes (score 1) → proceed.
   - No (score 0) → consider skipping; a direct answer may suffice.

2. **Reversibility**: Is the decision hard to reverse once made?
   - Hard to reverse (score 1) → proceed; structured deliberation is valuable.
   - Easy to reverse (score 0) → consider skipping; low-cost decisions rarely need multi-lens analysis.

3. **Information ambiguity**: Is there significant uncertainty about facts, outcomes, or stakeholder preferences?
   - High ambiguity (score 1) → proceed; the framework surfaces hidden assumptions.
   - Low ambiguity (score 0) → consider skipping; the answer may already be clear.

**Decision rule**:
- Total >= 2 → use the full framework.
- Total = 1 → offer the user a choice between `micro` (lightweight) and full framework.
- Total = 0 → recommend skipping; inform the user this question is better answered directly.

If the user explicitly requests the framework regardless of score, proceed but note the pre-check result.

## When NOT to Use This Framework

Do not use (or actively recommend against using) this framework for:
- **Simple factual queries**: "What is the capital of France?" — no perspectives needed.
- **Single-correct-answer problems**: "Fix this syntax error" — no tradeoff to explore.
- **Urgent time-critical decisions**: When seconds matter, structured deliberation adds harmful delay.
- **Trivial reversible choices**: Low-stakes decisions where the cost of being wrong is negligible.
- **Pure emotional support**: When the user needs empathy, not analysis.

If the user's question falls into these categories, briefly explain why and offer a direct answer instead.

## Core Principle

Treat the model as a viewpoint simulator, not as one stable persona.
Use a fixed four-lens dialogue to answer two core questions:
1) What would be a good group of people to explore X?
2) What would they say?

## Fixed Four-Lens Composition (Hard Constraint)

For `classic`, `lean`, and `deep` profiles, always use exactly four roles:
1. Real Person A (specific real person)
2. Real Person B (specific real person)
3. Domain Expert Archetype (abstract role)
4. Omniscient Agent Archetype (abstract role)

For `micro` profile, use exactly two roles:
1. Real Person A (specific real person)
2. Domain Expert Archetype (abstract role)

Mandatory rules:
- Real Person roles must be concrete, real, named people (not fictional).
- Domain Expert Archetype must be an abstract domain expert role.
- Omniscient Agent Archetype (when present) must be an abstract omniscient intelligence role.
- Role counts and round counts must match the active profile.
- Do not replace this structure with generic "Expert A/B/C" panels.

## Real-Person Selection Criteria (Hard Constraint)

For Real Person A and Real Person B, satisfy all criteria:
- Domain relevance: each person must have direct, public work related to the current problem.
- Public-method traceability: each person must have published ideas, frameworks, or decisions that can be inferred.
- Decision-pressure diversity: the two real people must represent different pressures (for example: product speed vs reliability, science vs operations).
- Time relevance: avoid historically famous but currently irrelevant picks unless historical framing is explicitly required.

For each real person, include:
- Selection rationale in one sentence.
- 2-3 public evidence anchors (for example: known books, talks, essays, open-source work, or widely known decision patterns).

Do not pick real people only for fame value.
Do not claim exact quotes unless quoted from a source in the current turn.

## Inference Confidence Annotation

For every statement attributed to a real person (Real Person A/B), append an inline confidence tag:
- `[confidence: high]` — the viewpoint closely follows the person's published framework, methods, or repeated public positions.
- `[confidence: medium]` — the viewpoint is a reasonable extrapolation from the person's known work, but not directly stated by them.
- `[confidence: low]` — the viewpoint is speculative; the person has not publicly addressed this specific topic.

Rules:
- Confidence tags are mandatory for Real Person A/B in every dialogue round.
- Confidence tags are not required for abstract roles (Domain Expert Archetype, Omniscient Agent Archetype).
- If a real person's confidence drops to `low` in a round, briefly note why (e.g., "topic outside their published scope").

## Real-Person Scoring Matrix (Guardrail)

Before finalizing Real Person A/B, score candidates with this matrix.

Per-person dimensions:
- Domain relevance (0-2)
- Public-method traceability (0-2)
- Time relevance (0-2)

Pair dimension:
- Decision-pressure diversity (0-2, pair-level only)

Passing rules:
- Real Person A score >= 5/6.
- Real Person B score >= 5/6.
- Pair diversity score >= 2/2.
- If any rule fails, rerun candidate selection and mark `low-confidence roster` if no better pair is available.

## Fallback Strategy (When Real-Person Selection Is Unclear)

Use this deterministic fallback order:
1. If user names real people, use them unless unsafe or clearly irrelevant.
2. If user gives domain but no names, propose three candidate real-person pairs and pick the best pair with rationale.
3. If confidence in pair quality is below 0.6, ask user to select one pair before continuing.
4. If user does not choose, proceed with the best pair and explicitly mark `low-confidence roster`.

Never replace Real Person A/B with fictional characters.
Never collapse to only abstract roles.

## Simulation Safety Rules

- For real people, clearly mark outputs as simulated viewpoints inferred from public work.
- Do not claim private access, private intent, or exact quotes.
- Keep analysis decision-oriented, falsifiable, and domain-specific.

## Rolling Uncertainty Tracker

Uncertainty tracking is not limited to the final ledger. Apply rolling updates:
- After Round 1: tag each initial position with its evidence basis (`fact`, `assumption`, or `speculation`).
- After Round 2: record any assumptions that were challenged and whether they survived cross-examination.
- After Round 3: note which revised positions introduced new assumptions or resolved old ones.
- The final Uncertainty Ledger (Section 8) consolidates the rolling tracker into a clean summary.

This ensures uncertainty is visible throughout the dialogue, not hidden until the end.

## Output Contract Guardrail (Hard Constraint)

Section and round counts depend on the active profile:
- `micro`: exactly 5 sections, 2 roles, 2 rounds (4 turns total).
- `lean`: exactly 7 sections, 4 roles, 4 rounds (same as classic, but turns compressed to 1-3 sentences).
- `classic`: exactly 7 sections, 4 roles, 4 rounds (16 turns total).
- `deep`: exactly 9 sections, 4 roles, 6 rounds (24 turns total).

Do not add extra top-level sections beyond the profile's contract.
Each dialogue round must contain one turn from each active role.

Preflight checklist (internal; do not output verbatim):
1. Role composition matches selected profile.
2. Real-person scoring matrix passes.
3. Evidence anchors are present for all real people.
4. Section count matches profile contract.
5. Each round has turns from all active roles.
6. Inference confidence tags are present for all real-person turns.

Postflight checklist (internal; do not output verbatim):
1. No fabricated direct quotes for real people.
2. Moderator synthesis includes recommendation, strongest alternative, preconditions, early warnings, and next actions.
3. Uncertainty ledger cleanly separates facts, assumptions, and speculation.

## Failure Modes and Recovery Actions

- FM1: Fame-first roster with weak relevance.
  - Recovery: rerank candidates using the scoring matrix; replace weakest candidate.
- FM2: Dialogue turns collapse into agreement too early.
  - Recovery: enforce at least one direct challenge per role in Round 2.
- FM3: Missing or malformed section structure.
  - Recovery: regenerate with strict 7-section scaffold first, then fill content.
- FM4: Actionability gap in synthesis.
  - Recovery: add time horizon, trigger indicators, and 1-3 concrete next actions.
- FM5: Speculation leakage.
  - Recovery: move uncertain claims to Uncertainty Ledger and add evidence-needed items.

## Controlled Execution Profiles (Structure-Preserving)

Profiles adjust depth and structure according to problem complexity.

- `micro`: 2 roles (1 real person + 1 domain expert archetype), 2 dialogue rounds (initial + final), 5 output sections. Use for medium-complexity problems or when pre-check score = 1.
- `lean`: 4 roles, 4 dialogue rounds, 7 sections (same structure as classic). Compress each turn to 1-3 sentences for low-token contexts.
- `classic` (default): 4 roles, 4 dialogue rounds, balanced detail and readability.
- `deep`: 4 roles, 6 dialogue rounds, 9 sections. Adds metrics, counterarguments, failure triggers, stress test, and contingency planning.

Variable round rules:
- Minimum 2 rounds for any profile (initial positions + final statements).
- Rounds 2 (cross-examination) and 3 (revised positions) may be added or removed based on profile.
- Maximum 6 rounds for `deep` profile: adds Round 5 (stress test with adversarial scenarios) and Round 6 (contingency planning).
- Each round always includes one turn from every active role.

Profile selection:
- If user specifies a profile, use it.
- If user does not specify, use `classic`.
- If applicability pre-check score = 1, suggest `micro` or `lean`.

### Micro Profile Output Sections

1. Good Group To Explore X (Two-Lens Roster)
2. Dialogue Round 1: Initial Positions
3. Dialogue Round 2: Final Statements
4. Moderator Synthesis
5. Uncertainty Ledger

### Deep Profile Additional Rounds

- Round 5: Stress Test — each role describes the scenario where their recommendation fails catastrophically.
- Round 6: Contingency Planning — each role proposes a fallback plan triggered by Round 5 failure scenarios.

## Required Output Sections (By Profile)

### Classic (default) — 7 sections:
1. Good Group To Explore X (Four-Lens Roster)
2. Dialogue Round 1: Initial Positions
3. Dialogue Round 2: Cross-Examination
4. Dialogue Round 3: Revised Positions
5. Dialogue Round 4: Final Statements
6. Moderator Synthesis
7. Uncertainty Ledger

### Micro — 5 sections:
1. Good Group To Explore X (Two-Lens Roster)
2. Dialogue Round 1: Initial Positions
3. Dialogue Round 2: Final Statements
4. Moderator Synthesis
5. Uncertainty Ledger

### Deep — up to 9 sections:
1. Good Group To Explore X (Four-Lens Roster)
2. Dialogue Round 1: Initial Positions
3. Dialogue Round 2: Cross-Examination
4. Dialogue Round 3: Revised Positions
5. Dialogue Round 4: Final Statements
6. Dialogue Round 5: Stress Test
7. Dialogue Round 6: Contingency Planning
8. Moderator Synthesis
9. Uncertainty Ledger

Do not skip the Roster section or the Uncertainty Ledger in any profile.
Each dialogue round must contain one turn from each active role.

## Workflow

1. Define decision frame
- Restate question, success criteria, constraints, and time horizon.
- Declare assumptions when context is missing.

2. Build four-lens roster
- Select two real people with clear relevance to the problem.
- Explain why each role belongs in the group.
- Score Real Person A/B with the scoring matrix before finalizing.

3. Run multi-round dialogue
- Round 1: initial claims.
- Round 2: challenges and tradeoffs.
- Round 3: revised positions after challenge.
- Round 4: final stance and one concrete action.

4. Synthesize
- Merge strongest arguments into one recommendation.
- State why it beats the strongest alternative.
- Include preconditions, early warning indicators, and next actions.

5. Calibrate uncertainty
- Separate facts, assumptions, and speculation.
- List evidence needed for confidence upgrades.

6. Run guardrail self-check
- Validate structure, safety, and actionability before final output.

7. User interaction and post-use reflection
- After delivering the output, append the Post-Use Self-Check section.
- If the session is interactive, invite the user to mark which positions they agree/disagree with and why.

## User Interaction Guidance

The framework output should not be a passive report. Build in interaction touchpoints:

1. **Pre-dialogue check-in**: After presenting the roster (Section 1), pause and ask the user:
   - "Do these roles and people look right for your question? Would you swap anyone?"
   - If the user confirms, proceed. If the user suggests changes, adjust before running dialogue.

2. **Mid-dialogue checkpoint** (optional, for `deep` profile): After Round 2 (Cross-Examination), briefly ask:
   - "Any assumptions you think were missed in the cross-examination?"

3. **Post-output reflection**: After the Uncertainty Ledger, always append the Post-Use Self-Check.

These interaction points transform the output from "AI-generated report" to "collaborative thinking scaffold."

## Post-Use Self-Check

After the final section (Uncertainty Ledger), always append a self-check block to help the user actively process the output rather than passively accept it.

Template:
```
### Post-Use Self-Check
1. Before reading this analysis, what was your initial leaning?
2. After reading, has your position changed? If so, which argument was most persuasive?
3. Which assumption in the Uncertainty Ledger concerns you most?
4. What is one piece of evidence you could gather in the next 48 hours to reduce uncertainty?
5. If you had to decide right now, what would you choose and why?
```

Rules:
- This block is mandatory in all profiles (micro, lean, classic, deep).
- It appears after the Uncertainty Ledger, as a non-numbered appendix (not counted in the main section count).
- Keep it to exactly 5 questions. Do not expand or customize.

## Evaluation and Regression

Use:
- `references/eval-rubric.md` for scoring criteria.
- `references/eval-cases.md` for regression test prompts.
- `references/first-use-guide.md` for onboarding new users.
- `scripts/lint_response.ps1` for hard-gate structure checks on generated outputs.

When updating this skill:
- Run at least 5 cases from `eval-cases.md`.
- Ensure every case matches its profile's section and role count requirements.
- Track rubric score before/after edits and avoid regressions (new baseline: 0-20 scale).
- Record outcomes using a compact log: date, cases run, pass rate, avg score, fail reasons.

## Output Contract

- Use `references/output-templates.md` for English output.
- Use `references/output-templates-zh.md` for Chinese output.
- If user asks for brevity, keep all sections required by the active profile and compress each section to 1-3 bullets.
- If using `lean` profile, keep all required sections and all active role turns per round.
- If using `micro` profile, use the 5-section template with 2 roles.
