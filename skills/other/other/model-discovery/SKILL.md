---
name: model-discovery
description: "Fetch current model names from AI providers (Anthropic, OpenAI, Gemini, Ollama), classify them into tiers (fast/default/heavy), and detect new models. Use when needing up-to-date model IDs for API calls or when other skills reference model names."
---

# Model Discovery Skill

Fetch the most recent model names from AI providers using their APIs. Includes tier classification (fast/default/heavy) for routing decisions and automatic detection of new models.

## Variables

| Variable | Default | Description |
|----------|---------|-------------|
| CACHE_TTL_HOURS | 24 | How long to cache model lists before refreshing |
| ENABLED_ANTHROPIC | true | Fetch Claude models from Anthropic API |
| ENABLED_OPENAI | true | Fetch GPT models from OpenAI API |
| ENABLED_GEMINI | true | Fetch Gemini models from Google API |
| ENABLED_OLLAMA | true | Fetch local models from Ollama |
| OLLAMA_HOST | http://localhost:11434 | Ollama API endpoint |
| AUTO_CLASSIFY | true | Auto-classify new models using pattern matching |

## Instructions

**MANDATORY** - Follow the Workflow steps below in order. Do not skip steps.

- Before referencing model names in any skill, check if fresh data exists
- Use tier mappings to select appropriate models (fast for speed, heavy for capability)
- Check for new models periodically and classify them

## Red Flags - STOP and Reconsider

If you're about to:
- Hardcode a model version like `gpt-5.2` or `claude-sonnet-4-5`
- Use model names from memory without checking current availability
- Call APIs without checking if API keys are configured
- Skip new model classification when prompted

**STOP** -> Read the appropriate cookbook file -> Use the fetch script

## Workflow

### Fetching Models

1. [ ] Determine which provider(s) you need models from
2. [ ] Check if cached model list exists: `cache/models.json`
3. [ ] If cache is fresh (< CACHE_TTL_HOURS old), use cached data
4. [ ] If stale/missing, run: `uv run python scripts/fetch_models.py --force`
5. [ ] **CHECKPOINT**: Verify no API errors in output
6. [ ] Use the model IDs as needed

### Checking for New Models

1. [ ] Run: `uv run python scripts/check_new_models.py --json`
2. [ ] If new models found, review the output
3. [ ] For auto-classification: `uv run python scripts/check_new_models.py --auto`
4. [ ] For interactive classification: `uv run python scripts/check_new_models.py`
5. [ ] **CHECKPOINT**: All models assigned to tiers (fast/default/heavy)

### Getting Tier Recommendations

1. [ ] Read: `config/model_tiers.json` for current tier mappings
2. [ ] Use the appropriate model for task complexity:
   - **fast**: Simple tasks, high throughput, cost-sensitive
   - **default**: General purpose, balanced
   - **heavy**: Complex reasoning, research, difficult tasks

## Model Tier Reference

### Anthropic Claude

| Tier | Model | CLI Name |
|------|-------|----------|
| fast | claude-haiku-4-5 | haiku |
| default | claude-sonnet-4-5 | sonnet |
| heavy | claude-opus-4-5 | opus |

### OpenAI

| Tier | Model | Notes |
|------|-------|-------|
| fast | gpt-5.2-mini | Speed optimized |
| default | gpt-5.2 | Balanced flagship |
| heavy | gpt-5.2-pro | Maximum capability |

**Codex (for coding)**:
| Tier | Model |
|------|-------|
| fast | gpt-5.2-codex-mini |
| default | gpt-5.2-codex |
| heavy | gpt-5.2-codex-max |

### Google Gemini

| Tier | Model | Context |
|------|-------|---------|
| fast | gemini-3-flash-lite | See API output |
| default | gemini-3-pro | See API output |
| heavy | gemini-3-deep-think | See API output |

### Ollama (Local)

| Tier | Suggested Model | Notes |
|------|-----------------|-------|
| fast | phi3.5:latest | Small; fast |
| default | llama3.2:latest | Balanced |
| heavy | llama3.3:70b | Large; requires GPU |

## CLI Mappings (for spawn:agent skill)

| CLI Tool | Fast | Default | Heavy |
|----------|------|---------|-------|
| claude-code | haiku | sonnet | opus |
| codex-cli | gpt-5.2-codex-mini | gpt-5.2-codex | gpt-5.2-codex-max |
| gemini-cli | gemini-3-flash-lite | gemini-3-pro | gemini-3-deep-think |
| cursor-cli | gpt-5.2 | sonnet-4.5 | sonnet-4.5-thinking |
| opencode-cli | anthropic/claude-haiku-4-5 | anthropic/claude-sonnet-4-5 | anthropic/claude-opus-4-5 |
| copilot-cli | claude-sonnet-4.5 | claude-sonnet-4.5 | claude-sonnet-4.5 |

## Quick Reference

### Scripts

```bash
# Fetch all models (uses cache if fresh)
uv run python scripts/fetch_models.py

# Force refresh from APIs
uv run python scripts/fetch_models.py --force

# Fetch and check for new models
uv run python scripts/fetch_models.py --force --check-new

# Check for new unclassified models (JSON output for agents)
uv run python scripts/check_new_models.py --json

# Auto-classify new models using patterns
uv run python scripts/check_new_models.py --auto

# Interactive classification
uv run python scripts/check_new_models.py
```

### Config Files

| File | Purpose |
|------|---------|
| `config/model_tiers.json` | Static tier mappings and CLI model names |
| `config/known_models.json` | Registry of all classified models with timestamps |
| `cache/models.json` | Cached API responses |

### API Endpoints

| Provider | Endpoint | Auth |
|----------|----------|------|
| Anthropic | `GET /v1/models` | `x-api-key` header |
| OpenAI | `GET /v1/models` | Bearer token |
| Gemini | `GET /v1beta/models` | `?key=` param |
| Ollama | `GET /api/tags` | None |

## Output Examples

### Fetch Models Output

```json
{
  "fetched_at": "2025-12-17T05:53:25Z",
  "providers": {
    "anthropic": [{"id": "claude-opus-4-5", "name": "Claude Opus 4.5"}],
    "openai": [{"id": "gpt-5.2", "name": "gpt-5.2"}],
    "gemini": [{"id": "models/gemini-3-pro", "name": "Gemini 3 Pro"}],
    "ollama": [{"id": "phi3.5:latest", "name": "phi3.5:latest"}]
  }
}
```

### Check New Models Output (--json)

```json
{
  "timestamp": "2025-12-17T06:00:00Z",
  "has_new_models": true,
  "total_new": 2,
  "by_provider": {
    "openai": {
      "count": 2,
      "models": [
        {"id": "gpt-5.2-mini", "inferred_tier": "fast", "needs_classification": false},
        {"id": "gpt-5.2-pro", "inferred_tier": "heavy", "needs_classification": false}
      ]
    }
  }
}
```

## Integration

Other skills should reference this skill for model names:

```markdown
## Model Names

For current model names and tiers, use the `model-discovery` skill:
- Tiers: Read `config/model_tiers.json`
- Fresh data: Run `uv run python scripts/fetch_models.py`
- New models: Run `uv run python scripts/check_new_models.py --json`

**Do not hardcode model version numbers** - they become stale quickly.
```

## New Model Detection

When new models are detected:

1. The script will report them with suggested tiers based on naming patterns
2. Models matching these patterns are auto-classified:
   - **heavy**: `-pro`, `-opus`, `-max`, `thinking`, `deep-research`
   - **fast**: `-mini`, `-nano`, `-flash`, `-lite`, `-haiku`
   - **default**: Base model names without modifiers
3. Models not matching patterns require manual classification
4. Specialty models (TTS, audio, transcribe) are auto-excluded

### Agent Query for New Models

When checking for new models programmatically:

```bash
# Returns exit code 1 if new models need attention
uv run python scripts/check_new_models.py --json

# Example agent workflow
if ! uv run python scripts/check_new_models.py --json > /tmp/new_models.json 2>&1; then
    echo "New models detected - review /tmp/new_models.json"
fi
```
