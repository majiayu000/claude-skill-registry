---
name: list-todos
description: Analyze and prioritize TODO items from TODOS.md. Use when planning work or deciding what to implement next.
allowed-tools: Read, Glob, Grep, AskUserQuestion, Edit
---

Analyze the TODO items in TODOS.md and produce a prioritized list with implementation guidance.

## Prerequisites

Before starting:
- Confirm `TODOS.md` exists in the current working directory. If it does not exist, **STOP** and ask the user where their project TODOs live.

## Process

Copy this checklist and track progress:

```
List TODOs Progress:
- [ ] Step 1: Read TODOS.md
- [ ] Step 2: Read project context (optional)
- [ ] Step 3: Extract TODO items
- [ ] Step 4: Analyze each item
- [ ] Step 5: Sort by priority score
- [ ] Step 6: Output prioritized list
- [ ] Step 7: Interactive Q&A (if items need clarification)
- [ ] Step 8: Update TODOS.md with clarifications
```

1. **Read TODOS.md** from the project root
2. **Read project context (optional)** — Look for context files in this order of preference:
   - VISION.md (if exists, use for project alignment)
   - PRODUCT_SPEC.md (fallback if no VISION.md)
   - TECHNICAL_SPEC.md, AGENTS.md, EXECUTION_PLAN.md (additional context if they exist)
   - If none exist, proceed without project context — analyze based on TODO content alone
3. **Extract TODO items** — Parse all actionable items from TODOS.md
4. **Analyze each item** using the framework below
5. **Sort by priority score** (highest first), break ties by value to project
6. **Output the prioritized list**

## Analysis Framework

For each TODO item, evaluate:

### Ranking Factors

| Factor | Low | Medium | High |
|--------|-----|--------|------|
| **Requirements Clarity** | One-liner with no context, unclear intent | Some details but gaps remain | Detailed spec with acceptance criteria |
| **Ease of Implementation** | Can't assess without clearer requirements | Moderate effort, approach is clear | Straightforward, clear path |
| **Value to Project** (weighted 2×) | Can't assess without clearer requirements | Useful improvement | Core functionality, high impact |

**Assessing Value to Project:**
- If VISION.md or PRODUCT_SPEC.md exists, evaluate how strongly the item aligns with the stated vision and goals
- If no context files exist, assess value based on the TODO item's own description and apparent impact
- Items that directly advance the core vision/goals score higher than tangential improvements
- Consider both immediate utility and strategic alignment

### Critical Rule: Do NOT Infer

**If requirements clarity is LOW, do NOT attempt to infer what the item means.**

- Do NOT guess the implementation approach
- Do NOT assume what problem it solves
- Set Ease and Value to "Cannot assess"
- Focus Open Questions on understanding the basic intent

A one-liner TODO like "Add feature X" with no additional context = LOW clarity, regardless of how obvious it might seem.

### Priority Score Calculation

```
Priority = ((Clarity + Ease + (Value × 2)) / 4 × 10) × Personal Multiplier
```

Where each factor is scored 1-3 (Low=1, Medium=2, High=3). Value is weighted 2× because alignment with project goals is the strongest signal for prioritization.

**Personal Priority Multiplier:**
- Look for `[priority: N]` inline in the TODO item (e.g., `[priority: 1.5]`)
- Valid range: 0.5 to 2.0
- If not specified, default to 1.0
- Examples:
  - `[priority: 2]` — User considers this twice as important
  - `[priority: 0.5]` — User considers this half as important
  - `[priority: 1.5]` — User considers this 50% more important

**If Clarity is LOW, cap the Priority Score at 3/10 maximum** (applied before multiplier).

Adjust score based on:
- **Boost (+1-2):** Blocks other work, security-related, frequently requested
- **Reduce (-1-2):** Speculative, already has workaround, external dependency

## Output Format

### For items with HIGH or MEDIUM requirements clarity:

```markdown
## {N}. {TODO Title}

**Priority Score:** {N}/10 {if multiplier != 1.0: "(base {base}/10 × {multiplier})"}
**Ranking Factors:**
- Requirements Clarity: {Medium|High} — {one sentence explanation}
- Ease of Implementation: {Low|Medium|High} — {one sentence explanation}
- Value to Project: {Low|Medium|High} — {one sentence explanation}
{if multiplier != 1.0: "- Personal Priority: ×{multiplier}"}

**Implementation Notes:**
{2-4 sentences on how to implement: key files to modify, approach, dependencies, estimated scope}

**Open Questions:**
- {Question that would improve requirements clarity}
- {Another question, if applicable}

**Suggested Next Action:** {See rules below}
```

### Suggested Next Action Rules

The "Suggested Next Action" field must follow these rules:

- **"Ready to implement"** — ONLY when the item has an explicit `[ready]` tag in TODOS.md. Never infer readiness from clarity or detail alone. The user must explicitly mark items as ready.
- **"Needs clarification"** — When requirements clarity is LOW, or significant open questions remain
- **"Needs research"** — When the approach is unclear and investigation is needed before implementation
- **"Consider deferring"** — When explicitly marked DEFERRED, has low value, or user has deprioritized (low multiplier)
- **"Consider removing"** — When the item appears obsolete, superseded, or no longer relevant

### For items with LOW requirements clarity:

```markdown
## {N}. {TODO Title}

**Priority Score:** {N}/10 (capped due to unclear requirements{if multiplier != 1.0: ", ×{multiplier} applied"})
**Ranking Factors:**
- Requirements Clarity: **Low** — {explain what's missing: no context, unclear intent, etc.}
- Ease of Implementation: Cannot assess
- Value to Project: Cannot assess
{if multiplier != 1.0: "- Personal Priority: ×{multiplier}"}

**What I understand:** {Brief statement of what little is clear, or "Only the title"}

**What I don't understand:**
- {Specific gap in understanding}
- {Another gap}

**Questions to clarify before proceeding:**
1. {Fundamental question about intent/purpose}
2. {Question about scope}
3. {Question about expected behavior}

**Suggested Next Action:** Clarify requirements first
```

### Summary section:

```markdown
# TODOS Analysis

**Generated:** {date}
**Items Analyzed:** {count}
**Project:** {project name from specs, or directory name}

---

{Individual item analyses, sorted by priority score}

---

## Summary

| Priority | Item | Score | Multiplier | Next Action |
|----------|------|-------|------------|-------------|
| 1 | {title} | {N}/10 | {×N or —} | {action} |
| 2 | {title} | {N}/10 | {×N or —} | {action} |
| ... | ... | ... | ... | ... |

**Ready to implement ([ready] tagged):** {count}
**Needs clarification:** {count}
**Consider deferring:** {count}
```

## Error Handling

**If TODOS.md doesn't exist:**
- Report: "No TODOS.md found in project root."
- Offer to create one with the standard template
- Suggest using `/add-todo` to add the first item

**If TODOS.md is empty or contains no TODO items:**
- Report: "TODOS.md exists but contains no actionable items"
- Show the file's current content (if any)
- Suggest using `/add-todo` to add items

**If TODOS.md uses non-standard format:**
- Attempt to parse what exists
- Report items that couldn't be parsed
- Show: "X items parsed, Y items skipped (non-standard format)"
- Offer to reformat to standard format

**If context files (VISION.md, etc.) can't be read:**
- Continue without that context
- Note in output: "Project context limited (VISION.md not found)"
- Score Value based on TODO content alone

**If priority tag has invalid value:**
- Use default multiplier (1.0)
- Report: "Invalid priority multiplier '{value}' ignored, using 1.0"
- Valid range reminder: 0.5 to 2.0

**If Edit tool fails during Q&A updates:**
- Report the edit failure
- Output the clarifications to terminal so they're not lost
- Suggest manually adding to TODOS.md

## Notes

- Skip items that are clearly completed (checked boxes)
- Group related items if they should be tackled together
- Consider project phase — items relevant to current phase score higher

---

## Review Your Output

After completing the analysis, verify:
- TODO count matches the number of items written to TODOS.md
- Priority assignments are justified by the criteria used
- No TODO items from the codebase were missed or duplicated

## Interactive Q&A Phase

After displaying the prioritized list and summary, use `AskUserQuestion` to offer the user an interactive session to clarify requirements. **All user interactions in this phase MUST use the `AskUserQuestion` tool** — never ask questions via plain text output.

See [QA_WORKFLOW.md](QA_WORKFLOW.md) for the detailed Q&A workflow:
1. Choose action (Clarify an item / Done)
2. Select item to clarify
3. Summarize current state
4. Ask open questions one at a time
5. Update TODOS.md with clarifications
6. Summarize understanding
7. Check implementation readiness
8. Continue or exit
