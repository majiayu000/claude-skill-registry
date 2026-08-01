---
name: idea-generation
description: 'Work with IdeaForge''s AI idea generation system. Triggers: generation
  flow, AI prompts, scoring system, duplicate detection, real-time logs, generation
  debugging. Pipeline: API → PromptBuilder → AI →'
---

---
name: idea-generation
description: Work with IdeaForge's AI idea generation system. Triggers: generation flow, AI prompts, scoring system, duplicate detection, real-time logs, generation debugging. Pipeline: API → PromptBuilder → AI → Parse → Dedupe → Save.
---

# Idea Generation

## Pipeline

```
POST /api/generation/generate
  → IdeaGenerationService
    → PromptBuilder (YAML configs)
    → callAI() (Claude/Gemini)
    → parseAIResponse()
    → EmbeddingService (duplicate check)
    → IdeaRepository (save)
    → GenerationLogger (SSE logs)
```

## API

```typescript
POST /api/generation/generate
{
  "framework": "pain-point",  // optional, random if not specified
  "domain": "Healthcare",      // optional
  "sessionId": "uuid"          // for log tracking
}
```

## AI Response Shape

```json
{
  "name": "Idea Name (max 60 chars)",
  "domain": "Domain → Subdomain",
  "problem": "...",
  "solution": "...",
  "quickSummary": "Elevator pitch",
  "concreteExample": {
    "currentState": "How users handle this today",
    "yourSolution": "How they'd use your product",
    "keyImprovement": "Quantifiable improvement"
  },
  "evaluation": {
    "problemSeverity": { "score": 8, "reasoning": "..." }
  },
  "tags": ["tag1", "tag2"]
}
```

## Scoring

- Per-criterion: 1-10 scale
- Weighted total: 0-100 scale
- Config: `evaluation-criteria.yaml`

## Duplicate Detection

1. **Exact**: Same domain + problem + solution
2. **Semantic**: Embedding similarity > 85%

## SSE Logs

Stages: `INIT` → `CONFIG_LOAD` → `PROMPT_BUILD` → `API_CALL` → `RESPONSE_PARSE` → `DUPLICATE_CHECK` → `DB_SAVE` → `COMPLETE`

Endpoint: `GET /api/logs/stream/{sessionId}`

## Key Files

| File | Purpose |
|------|---------|
| `services/ideaGenerationService.ts` | Orchestration |
| `services/promptBuilder.ts` | AI prompts |
| `services/configService.ts` | YAML configs |
| `lib/aiProvider.ts` | Claude/Gemini |