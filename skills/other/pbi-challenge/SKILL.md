---
name: pbi-challenge
version: 1.0.0
description: '[Code Quality] AI-assisted Dev BA PIC review of PBI drafts. Generates challenge prompts, flags gaps, provides actionable feedback for BA drafter revision.'
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting.

> **Evidence Gate:** MANDATORY IMPORTANT MUST — every claim requires `file:line` proof or traced evidence with confidence percentage (>80% to act).

## Quick Summary

**Goal:** Help Dev BA PIC review BA drafters' PBI drafts by generating specific, actionable challenge prompts. AI provides analysis; human makes the decision.

**Key distinction:** Collaborative review tool (drafter → reviewer flow), NOT self-review (use `/refine-review` for AI self-review).

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

### Frontend/UI Context (if applicable)

When this task involves frontend or UI changes, **MUST READ** `.claude/skills/shared/ui-system-context.md` and the following docs:

- Component patterns: `docs/project-reference/frontend-patterns-reference.md`
- Styling/BEM guide: `docs/project-reference/scss-styling-guide.md`
- Design system tokens: `docs/project-reference/design-system/README.md`

## Workflow

1. **Locate PBI draft** — Find BA drafters' draft PBI in `team-artifacts/pbis/` or path provided by user
2. **Load protocols** — Read these 3 protocols:
    - `.claude/skills/shared/ba-team-decision-model-protocol.md` (decision model, veto scope)
    - `.claude/skills/shared/refinement-dor-checklist-protocol.md` (DoR criteria)
    - `.claude/skills/shared/cross-cutting-quality-concerns-protocol.md` (authorization, seed data, migration)
3. **Load domain context** — Auto-detect module from PBI content, load:
    - `docs/project-reference/domain-entities-reference.md` (entity definitions)
    - Relevant feature docs from `docs/business-features/{App}/`
    - Existing business rules (BR-{MOD}-XXX) from feature docs
4. **Technical Feasibility Analysis:**
    - Can described features be built with the project's architecture?
    - Any domain entity conflicts? (cross-reference entity definitions)
    - Any cross-service implications? (message bus events, shared data between services)
    - Estimated complexity alignment (does scope match story points?)
5. **AC Quality Analysis:**
    - Vagueness detector: flag "should", "might", "TBD", "etc.", "various", "appropriate"
    - Coverage check: happy path + edge case + error case + authorization scenario
    - Missing scenarios: suggest specific additions based on feature type
6. **Cross-Cutting Concerns Check:**
    - Authorization section present and complete? (roles × CRUD matrix)
    - Seed data requirements addressed? (or explicit "N/A")
    - Data migration implications? (schema changes)
    - Performance considerations? (list/grid/export features)
    - **UI Layout section present?** If PBI involves UI: must have `## UI Layout` per `ui-wireframe-protocol.md` with wireframe + components (with tiers) + states + design tokens. If backend-only: explicit "N/A". Flag missing UI visualization as a gap.
7. **Generate Challenge Prompts** — Output specific, actionable questions:
    - NOT vague: "needs work" or "improve AC"
    - SPECIFIC: "AC #2 says 'user can filter results' — which filters exactly? Suggest: status, date range, priority"
8. **Provide AI Verdict** — APPROVE / REQUEST_REVISION / ESCALATE_TO_LEAD
9. **AskUserQuestion** — Dev BA PIC reviews AI analysis and makes final human decision

## Output

```markdown
## PBI Challenge Review

**PBI:** {PBI filename}
**Reviewer:** Dev BA PIC
**Date:** {date}
**Module:** {detected module code}

### Technical Feasibility

**Status:** FEASIBLE | CONCERNS | INFEASIBLE
{Analysis with evidence — cite domain entities, service boundaries, architecture constraints}

### AC Quality

**Status:** GOOD | NEEDS_REVISION | POOR

| AC # | Issue            | Suggested Fix             |
| ---- | ---------------- | ------------------------- |
| {#}  | {specific issue} | {specific fix suggestion} |

### Cross-Cutting Concerns

| Concern        | Status    | Issue    |
| -------------- | --------- | -------- |
| Authorization  | ✅/❌     | {detail} |
| Seed Data      | ✅/❌/N/A | {detail} |
| Data Migration | ✅/❌/N/A | {detail} |
| Performance    | ✅/❌/N/A | {detail} |

### Challenge Prompts for BA Drafters

1. {Specific actionable question with suggested answer}
2. {Specific actionable question with suggested answer}
3. {Specific actionable question with suggested answer}

### AI Verdict

**{APPROVE | REQUEST_REVISION | ESCALATE_TO_LEAD}**
**Reason:** {evidence-based justification}
**Confidence:** {X%} — {what was verified vs. what needs more investigation}

### Decision Record

**Dev BA PIC Decision:** {filled after human review via AskUserQuestion}
**Vote:** {approve / request-revision / escalate}
**Conditions:** {if any}
```

## Key Rules

- **AI provides ANALYSIS, human makes DECISION** — Never auto-approve or auto-reject
- **Challenge prompts must be specific** — Include suggested answers, not just questions
- **Domain context required** — Always load entity reference + feature docs before analysis
- **Technical veto scope** — Dev BA PIC CAN veto: architecture feasibility, dependency correctness, cross-service impact, performance, security. CANNOT veto: UI/UX design, visual design, business value (see `ba-team-decision-model-protocol.md` §2)
- **Evidence-based** — Every concern raised must cite source (protocol section, entity definition, feature doc)
- **Constructive tone** — Focus on improving the PBI, not criticizing the drafters

---

## Next Steps

**MANDATORY IMPORTANT MUST** after completing this skill, use `AskUserQuestion` to recommend:

- **"/dor-gate (Recommended)"** — If APPROVE: validate DoR before grooming
- **"/refine"** — If REQUEST_REVISION: BA drafters revise, then re-run `/pbi-challenge`
- **"Escalate to Engineering Manager"** — If ESCALATE_TO_LEAD: document concern for technical consultation
- **"Skip, continue manually"** — user decides

## Closing Reminders

**MANDATORY IMPORTANT MUST** break work into small todo tasks using `TaskCreate` BEFORE starting.
**MANDATORY IMPORTANT MUST** validate decisions with user via `AskUserQuestion` — never auto-decide.
**MANDATORY IMPORTANT MUST** add a final review todo task to verify work quality.
