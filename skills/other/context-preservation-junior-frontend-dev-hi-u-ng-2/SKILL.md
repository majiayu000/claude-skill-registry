---
name: context-preservation
description: Generate structured handoff summaries between workflow phases.
  Use when transitioning between RQPIV phases.
---

# Context Preservation Skill

## Purpose
Maintain context continuity across phases and sessions.

## When to Use
- Transitioning between RQPIV phases
- Handing off between sub-agents
- Pausing work for later resumption
- Creating progress reports

## Templates

### Phase Handoff
Reference: [templates/handoff-template.md](templates/handoff-template.md)

Use when transitioning from one phase to another. Captures:
- Summary of completed work
- Key findings and decisions
- Artifacts created
- Recommendations for next phase

### Progress Summary
Reference: [templates/progress-summary.md](templates/progress-summary.md)

Use for tracking ongoing work:
- Completed tasks
- In-progress items
- Blocked items
- Next steps

### Session Resume
Reference: [templates/session-resume.md](templates/session-resume.md)

Use when resuming interrupted work:
- Last known state
- Files to reload
- Continue point

## Context Preservation Process

### At Phase Start
1. Read previous phase handoff
2. Load relevant artifacts
3. Note key constraints/decisions
4. Begin phase work

### During Phase
1. Update progress summary as work progresses
2. Document significant decisions
3. Note any blockers or issues

### At Phase End
1. Create comprehensive handoff
2. List all artifacts created
3. Provide recommendations
4. Clear next actions

## Artifact Naming Convention

```
{type}-{session}-{timestamp}.md
```

Examples:
- `handoff-auth-feature-20251215.md`
- `progress-auth-feature-20251215-1430.md`
- `session-resume-auth-feature.md`

## Storage Locations

| Artifact Type | Location |
|---------------|----------|
| Handoffs | `plans/sessions/{session}/` |
| Progress | `plans/sessions/{session}/` |
| Resume | `plans/sessions/{session}/` |

## Best Practices

### For Handoffs
- Be concise but complete
- Include file paths for referenced artifacts
- Highlight decisions that affect future phases
- Note any assumptions made

### For Progress
- Update frequently (after each significant action)
- Be honest about blockers
- Include time context

### For Resume
- Capture exact stopping point
- List files to re-read
- Include any temporary notes
