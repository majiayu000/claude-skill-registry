---
name: briefing-format
description: Standard structure and style for sales call briefings including templates for full briefings and quick-reference cheat sheets. Triggers when generating or formatting prospect briefings.
---

# Briefing Format

## Overview

This skill defines the standard structure for sales call prep briefings. It ensures consistent, scannable output that salespeople can quickly review before calls.

## Usage

The briefing-writer sub-agent references this skill when:
- Generating full prospect briefings
- Creating quick-reference cheat sheets
- Formatting research into actionable content

## Briefing Structure

### Per-Prospect Section

```markdown
**[PRIORITY INDICATOR] Company Name** (Call Time) [Status Icon]
*Priority reason in italics*

- **What they do:** One-line company description
- **Recent news:** Key development (date)
- **Key person:** Name (Title)—relevant background note
- **Pain point signal:** Specific signal with source
- **Your angle:** Recommended positioning
- **Opening line:** Suggested conversation starter in quotes
```

### Priority Indicators

| Symbol | Meaning |
|--------|---------|
| ⭐ | High priority - strong signals |
| 🔄 | Follow-up from previous conversation |
| 🆕 | New prospect - full research done |
| ⚠️ | Needs attention - action overdue |

### For Follow-ups, Add

```markdown
- **Last conversation:** Date—spoke with Name (Role)
- **What happened:** Brief summary
- **Objection raised:** Key concern
- **What resonated:** What worked
- **Status:** Current state
```

## Quick-Reference Cheat Sheet

One-liner format for at-a-glance review:

```markdown
| Time | Company | Key Person | One-Liner | Priority |
|------|---------|------------|-----------|----------|
| 10am | Acme Mfg | Tom (Proc) | Follow up Q3 timeline | 🔄 |
| 11am | Brightside | James (COO) | Blue Cross growth angle | 🆕 |
```

## Writing Guidelines

### Opening Lines

Good opening lines:
- Reference something specific (news, post, mutual connection)
- Ask a question (invites dialogue)
- Show you did homework (builds credibility)

Examples:
- "Congrats on the Series C—saw you're expanding to Europe. How's the team handling the growth?"
- "I saw your post about tool sprawl—that resonates with a lot of our customers."
- "Last time you mentioned evaluating options in Q3. Is that still the timeline?"

Avoid:
- Generic "How are you?"
- Immediately pitching
- Factually incorrect statements

### Angle Recommendations

Be specific about positioning:
- ✅ "Position as force multiplier for scaling ops team"
- ❌ "They might be interested in our product"

### Tone

- Concise (scannable in 30 seconds)
- Actionable (clear next steps)
- Confident but not presumptuous

## Resources

- `resources/briefing-template.md` - Full briefing template
- `resources/quick-reference-template.md` - Cheat sheet template

## Scripts

- `scripts/briefing-formatter.py` - Generate formatted briefings
