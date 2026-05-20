---
name: handoff
version: 1.0.0
description: '[Process] Create structured handoff record between roles. Use when transitioning work between PO/BA/Dev/QA.'
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI MUST ask user whether to skip.

**Prerequisites:** **MUST READ** `.claude/skills/shared/understand-code-first-protocol.md` before executing.

## Quick Summary

**Goal:** Create a structured handoff record documenting what's ready, what's outstanding, and context for the receiving role.

**Workflow:**

1. **Summarize** — What was completed by the sending role
2. **Artifacts** — List deliverables (PBI, stories, designs, code, tests)
3. **Outstanding** — Known issues, open questions, risks
4. **Context** — Key decisions made, rationale, assumptions
5. **Next Steps** — What the receiving role should do first

**Key Rules:**

- Handoff must include artifact references (file paths, PBI IDs)
- Flag any blockers or dependencies
- Include contact/escalation info if applicable

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

## Handoff Types

| From         | To                   | Key Artifacts                                         |
| ------------ | -------------------- | ----------------------------------------------------- |
| PO → BA      | Idea, PBI draft      | Problem statement, business value, constraints        |
| BA → Dev     | Refined PBI, stories | Acceptance criteria, wireframes, dependencies         |
| Dev → QA     | Code, unit tests     | Test data, deployment steps, known limitations        |
| QA → PO      | Test results         | Coverage report, defect list, sign-off recommendation |
| Design → Dev | Design spec          | Component inventory, tokens, states, interactions     |

## Output Format

```
## Handoff Record

**From:** [Role]
**To:** [Role]
**Date:** {date}
**Feature/PBI:** [Reference]

### Completed Work
- [Item with artifact reference]

### Artifacts
| Artifact | Location | Status |
|----------|----------|--------|

### Outstanding Items
- [Open question/risk with owner]

### Context & Decisions
- [Key decision + rationale]

### Next Steps for [Receiving Role]
1. [First action]
2. [Second action]

### Blockers
- [Any blocking items]
```

## IMPORTANT Task Planning Notes (MUST FOLLOW)

- Always plan and break work into many small todo tasks using `TaskCreate`
- Always add a final review todo task to verify work quality and identify fixes/enhancements

---

## Workflow Recommendation

> **IMPORTANT MUST:** If you are NOT already in a workflow, use `AskUserQuestion` to ask the user:
>
> 1. **Activate `dev-qa-handoff` workflow** (Recommended) — handoff → test-spec
> 2. **Execute `/handoff` directly** — run this skill standalone
