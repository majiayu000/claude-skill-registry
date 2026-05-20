---
name: note-organizer
description: This skill should be used when the user asks to "organize notes", "process notes", "structure my notes", mentions "[raw]" or "[organized]" tags, or needs systematic note processing and extraction of actionable items.
version: 2.0.0
---

# Note Organizer

Transform unstructured notes into organized, actionable format using tag-based workflow.

## When to Use

User mentions: "organize notes", "process notes", "[raw]" tag, or needs structured analysis of unstructured text (meetings, brainstorms, research).

## Workflow

1. **Identify raw notes**: Look for `[raw]` tag or unstructured text blocks
2. **Extract structure**: Analyze for topics, decisions, actions, questions, insights, references
3. **Apply tags**: `[raw]` → `[organized]`, plus content tags (`[decision]`, `[action]`, `[question]`, `[insight]`, `[blocker]`, `[risk]`)
4. **Generate output**: Use standard format (Summary → Topics → Decisions → Actions → Questions → Insights → Blockers/Risks → References → Next Steps)
5. **Suggest project link**: If notes relate to active project, tag `[project:name]` and suggest adding to `.projects/[name]/.context.md`
6. **Offer integration**: Suggest saving to daily log, updating project context, or creating todos

## Output Format

```markdown
[organized]
## Summary
[1-2 sentences]

## Decisions Made
- [decision] Description + rationale

## Actions Required
- [ ] [priority] [action] Task - Owner - Deadline

## Open Questions / Key Insights / Blockers & Risks / References
[Tagged appropriately]

## Next Steps
1-3 priorities
```

## Tag Reference

- States: `[raw]` → `[organized]`
- Content: `[decision]` `[action]` `[question]` `[insight]` `[reference]` `[blocker]` `[risk]`
- Priority: `[urgent]` `[high]` `[medium]` `[low]`

## Best Practices

- Preserve original meaning (don't invent info)
- Be specific (include rationale for decisions, owners/deadlines for actions)
- Flag uncertainties (`[decision?]`, `[unknown owner]`)
- Apply PII redaction when needed

See `GUIDE.md` for examples, detailed workflow, troubleshooting, and integration patterns.
