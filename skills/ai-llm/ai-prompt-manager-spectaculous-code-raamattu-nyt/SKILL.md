---
name: ai-prompt-manager
description: Expert assistant for managing AI prompts, features, and configuration in the KR92 Bible Voice AI system. Use when creating AI prompts, configuring AI features, managing prompt versions, setting up AI bindings, or working with AI pricing and models. Supports multiple vendors and models for feature flexibility.
---

# AI Prompt Manager

## Quick Start

### Core Workflow

1. **Create feature** → Define what AI capability is needed
2. **Create prompt template** → Write system/user prompts with `{{variables}}`
3. **Create prompt version** → Implement the template (allows versioning)
4. **Bind to environment** → Connect prompt to dev/stage/prod
5. **Configure provider** → Choose vendor and model
6. **Test via Admin panel** → Validate response and cost

For SQL patterns, see [sql-patterns.md](references/sql-patterns.md).

### Database Schema (Essentials)

| Table | Purpose |
|-------|---------|
| `ai_features` | Feature registry (key, description) |
| `ai_prompt_templates` | Prompt structure (task, name) |
| `ai_prompt_versions` | Prompt variants with `{{variables}}` |
| `ai_prompt_bindings` | Link prompt version to environment |
| `ai_feature_bindings` | Link feature to vendor/model/env |
| `ai_pricing` | Cost per vendor/model |
| `ai_usage_logs` | Track calls, tokens, cost per user |

Full schema: See `Docs/context/db-schema-short.md`.

## Prompt Design

### Variable Substitution

Use `{{variable}}` syntax for dynamic content:

```javascript
system_prompt: "You are a {{role}} assistant for Bible study."
user_prompt_template: "Analyze: {{verse_reference}}"

// At call time
await getPrompt('my_feature', {
  role: 'theological scholar',
  verse_reference: 'John 3:16'
}, 'prod');
```

### Output Schema

Define expected output structure to validate responses:

```json
{
  "type": "object",
  "properties": {
    "summary": {"type": "string"},
    "insights": {
      "type": "array",
      "items": {"type": "string"}
    },
    "references": {
      "type": "array",
      "items": {"type": "string"}
    }
  }
}
```

### Temperature & Tokens

- **Temperature**: 0.0–0.3 (factual), 0.4–0.7 (balanced), 0.8–1.0 (creative)
- **max_tokens**: Set based on expected output length
  - Verse lookup: ~50 tokens
  - Short analysis: ~200 tokens
  - Full commentary: ~1000+ tokens

See [providers.md](references/providers.md) for full guidance.

## Vendor & Model Configuration

Vendors: `lovable`, `openai`, `anthropic`, `openrouter`

Models are **vendor-specific and change over time**. Always:
1. Check current availability in the API docs
2. Test in dev environment first
3. Configure pricing in `ai_pricing` before promoting to prod

See [providers.md](references/providers.md) for selection strategy.

## Environment Strategy

1. **dev** – Test new prompts, experiment with vendors
2. **stage** – Validate cost estimates, pre-production testing
3. **prod** – Stable, cost-optimized features

Always follow: dev → stage → prod progression.

## Testing AI Features

1. Go to Admin panel → AI section → Testaus tab
2. Select feature
3. Input test variables
4. Review response, tokens, cost estimate
5. Iterate on prompt if needed

## Monorepo Integration

AI features work across workspace apps:

- **raamattu-nyt** (main Bible app) – Uses most AI features
- **widgetizer** (embed service) – Limited AI features
- **Edge Functions** – Orchestrate calls in `ai-orchestrator/`

All share same `bible_schema` database and configuration.

## Skills Handoff

- **Quota/plan limits** → See `subscription-system` skill
- **Cost optimization** → See `performance-auditor` skill
- **Edge Functions** → See `edge-function-generator` skill

## References

- [sql-patterns.md](references/sql-patterns.md) – Common SQL workflows
- [providers.md](references/providers.md) – Vendor/model selection and parameters
- `Docs/06-AI-ARCHITECTURE.md` – Full system design
- `Docs/context/db-schema-short.md` – Database schema details
- `Docs/context/supabase-map.md` – Edge Functions & access matrix
