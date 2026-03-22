---
name: memvault
description: "Production-ready long-term memory server for AI agents with Ebbinghaus decay and strength-weighted retrieval. Use when you need persistent memory across agent sessions, memory decay (forgetting curve), memory statistics, or multi-agent memory tracking. Triggers: long-term memory, remember, recall, memory decay, Ebbinghaus, agent memory, memvault. Requires Docker."
---

# MemVault — Long-term Memory for AI Agents

## Quick Start

```bash
# Install (one command — Docker handles everything)
bash scripts/install.sh

# Verify
memvault health
```

## Usage

```bash
# Store a memory
memvault memorize-text <user_id> "<message>" "[reply]"

# Retrieve memories (strength-weighted)
memvault retrieve <user_id> "<query>"

# Run daily decay (memories fade like human memory)
memvault decay <user_id>

# Check stats
memvault stats <user_id>
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/memorize` | Store conversation → extract facts/events/knowledge |
| POST | `/retrieve` | Strength-weighted vector search (`similarity × strength`) |
| POST | `/decay` | Ebbinghaus forgetting curve (run daily via cron) |
| GET | `/stats` | Memory distribution, access patterns, agent breakdown |
| GET | `/health` | Service health |

## How It Works

1. **Store**: Conversations → LLM extracts facts → embedded → stored in pgvector
2. **Retrieve**: Query embedded → cosine similarity × memory strength → ranked results
3. **Decay**: `strength = exp(-rate × days / (1 + damping × ln(1 + access_count)))`
4. **Access boost**: Each retrieval increments `access_count`, slowing decay

Fading memories (strength < 0.1) are excluded from search.

## Configuration

All via environment variables in `.env` (created by install script):

- `MEMVAULT_LLM_BASE_URL` — Default: Ollama local. Set to OpenAI/Groq/etc URL if preferred
- `MEMVAULT_LLM_MODEL` — Default: `qwen2.5:3b`
- `MEMVAULT_TRANSLATION` — Set `true` + `MEMVAULT_TRANSLATION_LANG` for auto-translation
- `MEMVAULT_PORT` — Default: `8002`

## Daily Cron Setup

Add Ebbinghaus decay to your agent's cron:

```
0 3 * * *  curl -s -X POST 'http://127.0.0.1:8002/decay?user_id=YOUR_USER_ID'
```

## TOOLS.md Snippet

```markdown
## MemVault 🧠
memvault memorize-text "<user_id>" "<content>" "<context>"
memvault retrieve "<user_id>" "<query>"
memvault decay <user_id>
memvault stats <user_id>
- API: 127.0.0.1:8002
```

## Multi-Agent Memory

Tag memories by source agent:

```bash
curl -X POST http://localhost:8002/memorize -H "Content-Type: application/json" \
  -d '{"conversation": [
    {"role": "metadata", "content": "{\"source_agent\": \"research-bot\"}"},
    {"role": "user", "content": "Found new papers on transformers"}
  ], "user_id": "team"}'
```

## Troubleshooting

- **"Connection refused"** → Run `docker compose -f ~/.openclaw/workspace/skills/memvault/docker-compose.yml up -d`
- **Slow memorize** → Normal, LLM extraction takes 5-15s per conversation
- **No results from retrieve** → Check `memvault stats` — if total=0, nothing stored yet
- **All memories fading** → Reduce decay_rate: `curl -X POST 'http://localhost:8002/decay?decay_rate=0.05'`
