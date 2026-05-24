---
name: CrewAI Development
description: Create CrewAI workflows as NestJS applications under apps/crewai/. FUTURE: Same pattern as LangGraph - NestJS app, same webhook pattern as n8n, receive same parameters, wrap as API agents. CRITICAL: Status webhook URL must read from environment variables.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# CrewAI Development Skill

**NOTE**: This is a FUTURE skill. CrewAI workflows will follow the same pattern as LangGraph when implemented.

## When to Use This Skill

Use this skill when:
- Planning CrewAI workflow architecture (FUTURE)
- Setting up CrewAI as a NestJS application (FUTURE)
- Configuring webhook status tracking for CrewAI (FUTURE)
- Wrapping CrewAI endpoints as API agents (FUTURE)

## Directory Structure (Future)

CrewAI applications will follow the same pattern as LangGraph:

```
apps/
├── api/              # Main NestJS API
├── n8n/              # N8N workflows
├── langgraph/        # LangGraph workflows
└── crewai/           # CrewAI workflows (FUTURE)
    ├── src/
    │   ├── main.ts
    │   ├── app.module.ts
    │   ├── crews/
    │   │   └── example-crew.ts
    │   └── controllers/
    │       └── crewai.controller.ts
    ├── package.json
    └── tsconfig.json
```

## Expected Pattern (When Implemented)

CrewAI workflows will:

1. **Be NestJS applications** under `apps/crewai/`
2. **Receive same parameters** as n8n/LangGraph:
   - `taskId`, `conversationId`, `userId`
   - `userMessage`, `statusWebhook`
   - `provider`, `model`
   - `stepName`, `sequence`, `totalSteps`
3. **Use same webhook pattern** for status tracking
4. **Wrap as API agents** with request/response transforms
5. **Follow A2A protocol** (health, agent card endpoints)

## Reference

See **LangGraph Development Skill** for the complete pattern that CrewAI will follow when implemented.

