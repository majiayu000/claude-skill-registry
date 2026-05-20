---
name: nexus
description: Nexus conversational PI agent architecture, development, and deployment. Use when working on the Nexus orchestrator, gateway, or tools.
---

# Nexus Agent

Nexus is the conversational personal intelligence (PI) agent — a single agentic loop using the Strands Agent SDK, orchestrated by Temporal.

## Architecture

```
UI (WebSocket) → Nexus Gateway (FastAPI) → Temporal Signal
    → Orchestrator Workflow → run_agent_turn Activity
        → Strands Agent (think → act → observe loop)
            → Core Tools (read/write/edit/bash)
            → MCP Tools (memory, skills, fetch)
            → Custom Tools (web_search)
        → Response via Redis PubSub → Gateway → UI
```

### Key Differences from Syndicates

| Aspect | Syndicates | Nexus |
|--------|-----------|-------|
| Pattern | Multi-agent orchestration | Single agentic loop |
| SDK | Custom framework agents | Strands Agent SDK |
| Config | `kubani.framework.config` (YAML) | Environment variables |
| Workflow | Multiple specialized workflows | Entity workflow pattern |
| Interaction | Event-driven, autonomous | Conversational, user-initiated |

## Components

| Component | Location | Purpose |
|-----------|----------|---------|
| Orchestrator | `kubani/nexus/orchestrator/` | Temporal worker, activities, workflow |
| Gateway | `kubani/nexus/gateway/` | FastAPI, WebSocket, Discord bridge |
| Tools | `kubani/nexus/orchestrator/tools/` | Core and extra tool definitions |

### Entity Workflow Pattern

The orchestrator uses a long-running Temporal entity workflow:
- Receives messages via Temporal signals
- Processes each message in a `run_agent_turn` activity
- Uses `continue-as-new` after 100 iterations to prevent history growth
- Maintains conversation state across turns

### Key Files

- `activities.py` — `run_agent_turn()`: Creates Strands Agent, builds system prompt, executes agent loop
- `workflow.py` — Entity workflow with signal handling and continue-as-new
- `worker.py` — Temporal worker entry point
- `tools/core.py` — Core tools (file ops, bash, etc.)
- `tools/extra_tools.py` — MCP client tools (fetch, web_search)

## Local Development

```bash
# Setup
cd kubani/nexus/orchestrator
cp ../../nexus/.env.example .env  # Edit with credentials

# Run worker locally
source .env && python -m kubani.nexus.orchestrator.worker

# Run gateway (separate terminal)
cd kubani/nexus/gateway
source .env && python -m kubani.nexus.gateway.main
```

See `kubani/nexus/.env.example` for all required environment variables.

## Configuration

Nexus uses direct environment variables (NOT the kubani config system):

| Variable | Purpose |
|----------|---------|
| `TEMPORAL_HOST` | Temporal server address |
| `TEMPORAL_NAMESPACE` | Temporal namespace (usually `nexus`) |
| `NEXUS_DATABASE_URL` | PostgreSQL connection string |
| `REDIS_URL` | Redis for pub/sub and caching |
| `LLM_API_URL` | vLLM API endpoint |
| `QDRANT_URL` | Vector database |
| `MCP_MEMORY_URL` | Memory MCP server |
| `MCP_SKILLS_URL` | Skills MCP server |

## Building & Deploying

```bash
# Build container
earthly +nexus-orchestrator

# Smoke test
docker run --rm --env-file .env <image> python -c "from kubani.nexus.orchestrator.worker import *; print('OK')"

# Deploy via GitOps
# Update image tag in infrastructure/gitops/apps/nexus/orchestrator-deployment.yaml
# Commit and push (Flux auto-deploys)
```

## Testing Changes

1. **Prompt changes**: Edit `activities.py` system prompt, run worker locally, send test message via UI
2. **Tool changes**: Edit tools, run worker locally, test tool invocation
3. **Workflow changes**: Edit `workflow.py`, restart worker, verify signal handling
4. **Always follow the 4-stage workflow**: local test → integration → container build → deploy
