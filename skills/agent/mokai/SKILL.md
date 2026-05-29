---
Done: false
today: false
follow up: false
this week: true
back burner: false
ASAP: false
type: Task
status:
relation:
description:
effort:
ai-assigned: true
ai-ignore: false
ai-ask: false
priority:
agent:
slash-command:
urgent: false
---
**Current problem**: 669-line agent with embedded knowledge
- Too token-heavy
- Not conversational
- Hard to maintain

**Proposed solution**: Break into slash commands
```
.claude/commands/mokai/
├── mokai-primer.md              # Loads all MOKAI context
├── mokai-strategy.md            # Strategic planning mode
├── mokai-compliance.md          # Tenders/IPP mode
├── mokai-finance.md            # Financial operations mode
├── mokai-operations.md         # Daily ops mode
├── mokai-status.md            # Daily status (existing)
├── mokai-weekly.md            # Weekly review (existing)
└── mokai-insights.md          # Deep analysis (existing)
```

**Benefits**:
- Lightweight (50-100 lines each vs 669)
- Conversational (context loads once, persists)
- Flexible (mix modes as needed)
- Maintainable (update one without touching others)
