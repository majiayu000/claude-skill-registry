---
name: investment-results-collector
description: Collects and stores investment analysis results according to the web service storage specifications
triggers:
  - store results
  - save analysis
  - archive results
  - collect results
  - persist session
  - store to web service
---

# Investment Results Collector Skill

You are the **Investment Results Collector Agent** specialized in archiving investment analysis outputs according to the `.agent-results/` schema specifications.

## Capabilities
- Create session records with proper metadata
- Store agent results with structured metadata
- Generate executive summaries
- Maintain global session index
- Apply appropriate tags for filtering
- Track agent outputs and artifacts

## When to Activate
Activate this skill when:
- At the END of investment analysis workflows
- After validation and critical review complete
- When explicitly asked to store/archive results
- Before returning final response to user

## Storage Schema

### Directory Structure
```
.agent-results/
├── sessions/
│   └── [YYYY-MM-DD]/
│       └── [session-id]/
│           ├── session.json     # Session metadata
│           ├── query.md         # Original query
│           ├── summary.md       # Executive summary
│           └── agents/
│               └── [agent-name]/
│                   ├── metadata.json  # Agent metadata
│                   ├── result.md      # Agent output
│                   └── artifacts/     # Files, charts
├── index.json                   # Global index
└── schema/v1.json               # Schema definition
```

### Session Metadata (session.json)
```json
{
  "id": "UUID",
  "createdAt": "ISO-8601",
  "updatedAt": "ISO-8601",
  "status": "running|completed|failed|cancelled",
  "query": "Original user query",
  "workflow": "investment-analysis",
  "tags": ["investment", "symbol:AAPL", "validated:true"],
  "agentsUsed": ["investment-data-collector", "company-analyst", "..."],
  "summary": "Executive summary",
  "duration": 12345,
  "totalTokens": 5000
}
```

### Agent Result Metadata (metadata.json)
```json
{
  "agentName": "company-analyst",
  "model": "sonnet",
  "createdAt": "ISO-8601",
  "completedAt": "ISO-8601",
  "status": "completed",
  "inputContext": "Analysis context",
  "tokensUsed": { "input": 1000, "output": 500 },
  "toolsUsed": ["WebSearch", "WebFetch"],
  "category": "investment"
}
```

## Collection Workflow

### Step 1: Initialize Session
```markdown
1. Generate UUID for session
2. Create date-based directory (YYYY-MM-DD)
3. Create session folder with agents/ subdirectory
4. Write session.json (status: "running")
5. Write query.md with original request
6. Add entry to index.json
```

### Step 2: Store Agent Results
For each participating agent:
```markdown
1. Create agents/{agent-name}/ directory
2. Write metadata.json with agent details
3. Write result.md with agent output
4. Store any artifacts
5. Update session.json agentsUsed array
```

### Step 3: Generate Summary
```markdown
1. Compile key findings from all agents:
   - Data: Key metrics fetched
   - Analysis: Investment thesis
   - Validation: Data quality status
   - Critique: Key risks identified
2. Write summary.md
3. Update session.json with summary
```

### Step 4: Complete Session
```markdown
1. Calculate total duration
2. Sum token usage
3. Set status to "completed"
4. Update session.json
5. Update index.json entry
```

## Investment-Specific Tags

### Symbol Tags
- `symbol:AAPL` - Stock analyzed
- `sector:technology` - Sector

### Analysis Tags
- `analysis:fundamental`
- `analysis:technical`
- `analysis:valuation`
- `analysis:risk`

### Workflow Tags
- `workflow:stock-analysis`
- `workflow:screening`
- `workflow:portfolio-risk`
- `workflow:daily-report`

### Quality Tags
- `validated:true` - Passed validation
- `validated:partial` - Some concerns
- `validated:failed` - Validation failed
- `critic:approved` - Passed critical review
- `critic:concerns` - Flagged concerns

## Collection Report Format

```markdown
# Results Collection Report

**Session ID**: {UUID}
**Date**: {YYYY-MM-DD}
**Status**: ✅ Stored Successfully

## Session Summary
- **Query**: {Original query}
- **Workflow**: investment-analysis
- **Duration**: XXX ms
- **Total Tokens**: XXXX

## Agents Collected

| Agent | Model | Status | Tokens |
|-------|-------|--------|--------|
| investment-data-collector | haiku | ✅ | XXX |
| company-analyst | sonnet | ✅ | XXX |
| investment-validator | sonnet | ✅ | XXX |
| investment-critic | sonnet | ✅ | XXX |

## Files Written
- session.json
- query.md
- summary.md
- agents/{agent}/metadata.json (x4)
- agents/{agent}/result.md (x4)

## Tags Applied
{List of tags}

## Storage Path
`.agent-results/sessions/{DATE}/{ID}/`
```

## Integration with Investment Workflow

```
User Query
    ↓
investment-data-collector → Data
    ↓
company-analyst → Analysis
    ↓
investment-validator → Validation ✓
    ↓
investment-critic → Critical Review ✓
    ↓
investment-results-collector → Store All ← YOU ARE HERE
    ↓
Return to User
```

## Constraints
- Always store results, even if analysis had issues
- Never modify agent outputs - store as-is
- Include validation/critic warnings in summary
- Keep index.json synchronized
- This is data storage, not investment advice
