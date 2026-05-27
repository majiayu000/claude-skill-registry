---
name: design-challenger
description: Evaluate high-level protocol or system designs for overcomplication, then propose simpler, more structured alternatives with explicit trade-offs. Use when the user wants to challenge a system design, simplify an architecture, reduce protocol complexity, or compare design alternatives.
argument-hint: "<design description>"
allowed-tools:
  - Read
  - Glob
  - Grep
---

# Design Challenger

<goals>
## Goals

- Identify overcomplicated designs (too many moving parts, cross-file flow complexity, fragile invariants).
- Propose cleaner alternatives that reduce invariants, shorten flows, and consolidate responsibilities.
- Stay objective by grounding suggestions in project context, requirements, and assumptions.
- Allow bold redesigns (some recall is acceptable) while keeping trade-offs explicit.
- Avoid code-level refactors; focus on protocol/system-level design changes only.
</goals>

---

<process>
## Process

**TRIGGER:** User provides a high-level protocol or system design for evaluation.

1. Clarify the context briefly when needed: intended users, runtime constraints, compatibility needs, and failure modes.
2. If domain context is missing, consult references before proposing alternatives.
3. Map the current design at a high level: components, handoffs, invariants, and cross-file flow.
4. Identify the overcomplication drivers: unnecessary indirections, redundant layers, excessive configurability, or fragile sequencing.
5. Propose one or more simpler designs that meet the same requirements with fewer moving parts.
6. If major simplification requires removing a feature, make the case and note impact; consider modular or optional variants when removal is too costly.
7. Explicitly enumerate trade-offs for each alternative.
</process>

---

<references>
## References

Load only the minimum needed for the task.

- `references/context-questions.md`: use when the prompt lacks constraints.
- `references/complexity-smells.md`: use to spot overcomplication drivers.
- `references/simplification-tactics.md`: use to structure alternatives.
- `references/decision-matrix.md`: use when multiple options must be compared.
- `references/tradeoff-catalog.md`: use to enumerate trade-offs.
- `references/domain-context.md`: use only when domain context is missing.
</references>

---

<output_format>
## Output Format

Use the following format and keep it concrete and concise. Do not include code.

1) What is overcomplicated
- ...

2) Simpler alternative
- ...

3) Trade-offs
- ...
</output_format>

---

<guardrails>
## Guardrails

- Do not suggest code edits or function-level tweaks (e.g., no line-level or snippet changes).
- Avoid subjective preferences; justify improvements by reducing complexity, invariants, or moving parts.
- Do not propose changes that reduce security posture; simplifications should be neutral or positive for security.
- Feature removal is allowed only with clear justification (usage, risk, maintenance cost, compatibility impact).
- If requirements force complexity, say so and focus on the minimal simplifications that preserve constraints.
</guardrails>
