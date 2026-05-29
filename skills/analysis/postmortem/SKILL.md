---
name: postmortem
description: |
  POSTMORTEM
---

---
description: Create blameless postmortem from the incident we just resolved
argument-hint: [optional: additional context or specific focus]
---

# POSTMORTEM

Generate a blameless postmortem from this conversation.

You just helped resolve an incident. The investigation context, hypotheses, evidence, and fix are all in this conversation (and likely in an INCIDENT.md file).

## Output Structure

Write a postmortem with:
- **Summary**: One paragraph - what happened, impact, resolution
- **Timeline**: Key events in UTC (use conversation timestamps if available)
- **Root Cause**: The actual underlying cause (not symptoms)
- **5 Whys**: Dig to systemic factors
- **What Went Well**: Recognition of good practices during response
- **What Went Wrong**: Honest assessment without blame
- **Follow-up Actions**: Concrete items with clear ownership

## Philosophy

- **Blameless**: Focus on systems, processes, and tools - not people
- **Honest**: Don't minimize or exaggerate
- **Actionable**: Every lesson should have a concrete follow-up

If INCIDENT.md exists, update its postmortem section. Otherwise create POSTMORTEM-{timestamp}.md.

Optional focus: **$ARGUMENTS**
