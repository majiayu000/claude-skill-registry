---
description: Load Brief business context into agent sessions
---

# Brief Context Skill

Automatically loads comprehensive business context from Brief MCP.

## When Invoked

Calls `mcp__brief__brief_get_onboarding_context` to retrieve:

### Product Context
- **Service definition**: What Brief does
- **Customers**: Who uses Brief
- **Competitive advantages**: Why Brief vs alternatives
- **Business model**: How Brief works

### Strategic Context
- **6-month goal**: Current strategic focus
- **Top metrics**: What we're measuring (3 key metrics)

### User Understanding
- **Top personas**: Primary user types with needs and pain points
- **Customer insights**: Recent themes and sentiment

### Current Work
- **Building**: What's actively in development
- **Committed**: What we're committed to delivering

### Velocity & Team
- **Release frequency**: How often we ship
- **Decision speed**: How quickly we make decisions
- **Technical sophistication**: Team's technical capabilities
- **Engineering team**: Team structure and focus areas

### Recent Decisions
- Last 10 architectural/business decisions with rationale

## Usage Pattern

```text
/onboard
→ Invokes brief-context skill
→ Agent now has full business context
→ Can reference when making decisions
→ Can call guard_approach to check against decisions
```

## Integration with Agents

All agents should have access to this context:
- **context-loader**: Calls this first
- **task-planner**: References for constraints, calls guard_approach before planning
- **implementation**: Checks decisions with guard_approach before architectural changes

## Fallback

If Brief MCP not available:
- Report: "Brief MCP not connected. Working with code context only."
- Suggest: "Run /brief to set up MCP server for business context."
