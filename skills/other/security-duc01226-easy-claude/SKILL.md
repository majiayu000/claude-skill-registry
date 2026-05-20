---
name: security
version: 1.0.0
description: '[Code Quality] Perform security review on specified scope'
disable-model-invocation: false
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI MUST ask user whether to skip.

**Prerequisites:** **MUST READ** `.claude/skills/shared/evidence-based-reasoning-protocol.md` before executing.

- `docs/project-reference/domain-entities-reference.md` — Domain entity catalog, relationships, cross-service sync (read when task involves business entities/models)

> **External Memory:** For complex or lengthy work (research, analysis, scan, review), write intermediate findings and final results to a report file in `plans/reports/` — prevents context loss and serves as deliverable.

> **Evidence Gate:** MANDATORY IMPORTANT MUST — every claim, finding, and recommendation requires `file:line` proof or traced evidence with confidence percentage (>80% to act, <80% must verify first).

## Quick Summary

**Goal:** Perform security review against OWASP Top 10 and project authorization patterns.

**Workflow:**

1. **Scope** — Identify security-sensitive code areas
2. **Audit** — Review against OWASP categories and platform security patterns
3. **Report** — Document findings with severity and remediation

**Key Rules:**

- Analysis Mindset: systematic review, not guesswork
- Check both backend and frontend attack surfaces
- Use project authorization attributes and entity-level access expressions (see docs/project-reference/backend-patterns-reference.md)

<scope>$ARGUMENTS</scope>

## Analysis Mindset (NON-NEGOTIABLE)

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

- Do NOT assume code is secure at face value — verify by reading actual implementations
- Every vulnerability finding must include `file:line` evidence
- If you cannot prove a vulnerability with a code trace, state "potential risk, not confirmed"
- Question assumptions: "Is this actually exploitable?" → trace the input path to confirm
- Challenge completeness: "Are there other attack vectors?" → check all input boundaries
- No "looks secure" without proof — state what you verified and how

Activate `arch-security-review` skill and follow its workflow.

**CRITICAL**: Present your security findings. Wait for explicit user approval before implementing fixes.

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements

---

## Workflow Recommendation

> **IMPORTANT MUST:** If you are NOT already in a workflow, use `AskUserQuestion` to ask the user:
>
> 1. **Activate `quality-audit` workflow** (Recommended) — security → sre-review → test
> 2. **Execute `/security` directly** — run this skill standalone

---

## Next Steps

**MANDATORY IMPORTANT MUST** after completing this skill, use `AskUserQuestion` to recommend:

- **"/sre-review (Recommended)"** — Production readiness review
- **"/performance"** — Analyze performance next
- **"Skip, continue manually"** — user decides

## Closing Reminders

**MANDATORY IMPORTANT MUST** break work into small todo tasks using `TaskCreate` BEFORE starting.
**MANDATORY IMPORTANT MUST** validate decisions with user via `AskUserQuestion` — never auto-decide.
**MANDATORY IMPORTANT MUST** add a final review todo task to verify work quality.
