---
name: local-development
description: Complete guide for local agent development using kubani CLI, unified configuration, MCP integration, and seamless iteration. Includes the Nexus local runner for testing prompts and activities against live cluster services without building a container.
---

# Local Development Guide

This is the comprehensive guide for developing Kubani agents locally with cluster services.

---

## Nexus Agent: Local Iterative Testing (Primary Workflow)

The fastest way to iterate on Nexus Agent changes — prompts, activity logic, or mission configuration — is the **Nexus Local Runner** (`scripts/nexus_local_runner.py`). It directly invokes the Temporal activity functions as plain async functions against the live `*.almckay.io` cluster services. No container build, no Temporal worker, no cluster deployment needed.

### One-Time Setup

```bash
# 1. Copy the environment template
cp .env.nexus-local .env.nexus-local.override

# 2. Fill in secrets from the cluster
# NEXUS_DATABASE_URL:
kubectl get secret nexus-config -n nexus -o jsonpath='{.data.nexus-database-url}' | base64 -d

# REDIS_URL:
kubectl get secret nexus-config -n nexus -o jsonpath='{.data.redis-url}' | base64 -d

# QDRANT_API_KEY, NEO4J_PASSWORD: get from 1Password vault

# 3. Validate setup
python scripts/nexus_local_runner.py health   # check all *.almckay.io services
python scripts/nexus_local_runner.py check    # validate env vars
```

The `.env.nexus-local.override` file is gitignored. Never commit it.

### Runner Commands

| Command | What it does |
|---------|-------------|
| `health` | HTTP health check against all cluster service endpoints |
| `check` | Validate required env vars are set and non-placeholder |
| `turn <message>` | Run a single reactive agent turn (hits live LLM + MCP) |
| `mission --goal <...>` | Run a single proactive mission turn |
| `watch --goal <...>` | Re-run a mission on every file save (hot-reload for prompts) |

### Iterating on a Reactive Turn (AGENT_SYSTEM_PROMPT)

```bash
# 1. Edit the prompt in kubani/nexus/orchestrator/activities.py
# 2. Run immediately — no restart needed
python scripts/nexus_local_runner.py turn "What pods are unhealthy in the nexus namespace?"

# Use --log-level DEBUG to see every tool call and LLM token
python scripts/nexus_local_runner.py --log-level DEBUG turn "Summarise cluster health"
```

### Iterating on a Mission Turn (MISSION_SYSTEM_PROMPT)

```bash
# Run with the conservative nexus policy (memory + skills + fetch)
python scripts/nexus_local_runner.py mission \
    --goal "Check all pods in the nexus namespace and report failures" \
    --policy nexus \
    --max-tool-calls 10

# Run with the nexus-proactive policy (adds kubernetes + discord + temporal)
python scripts/nexus_local_runner.py mission \
    --goal "Check cluster health and send a Discord alert if any pods are failing" \
    --policy nexus-proactive \
    --max-tool-calls 20
```

### Watch Mode (Fastest Prompt Iteration)

```bash
# Watches activities.py — re-runs the mission every time you save the file
python scripts/nexus_local_runner.py watch \
    --goal "Summarise the top 3 stories from Hacker News" \
    --watch-path kubani/nexus/orchestrator/activities.py

# Watch a different file (e.g., mission model)
python scripts/nexus_local_runner.py watch \
    --goal "Check cluster health" \
    --watch-path kubani/nexus/missions/activities.py
```

### JSON Output (for scripting)

```bash
# All commands support --json for machine-readable output
python scripts/nexus_local_runner.py --json mission \
    --goal "Check cluster health" | jq '.should_notify'
```

### How It Works

The runner patches `temporalio.activity.heartbeat` to be a no-op, then directly `await`s the activity functions. Because all activities are pure async functions that accept and return serializable dicts, they work identically outside a Temporal worker. The LLM, MCP servers, and databases are all reached via the `*.almckay.io` ingress URLs configured in `.env.nexus-local`.

---

## General Kubani Agents: kubani CLI

For non-Nexus agents (syndicates, k8s-monitor, etc.), use the `kubani` CLI.

### Quick Start

```bash
# Install kubani CLI
uv pip install -e .

# Initialize configuration
kubani init

# Run agent locally with cluster services
kubani local-run --agent k8s-monitor --temporal cluster --output console

# Run with hot-reload for rapid iteration
kubani local-run --agent k8s-monitor --hot-reload
```

### kubani CLI Reference

| Command | Description |
|---------|-------------|
| `kubani init` | Initialize configuration |
| `kubani local-run` | Run agent locally |
| `kubani test` | Run tests |
| `kubani eval` | Run evaluations |
| `kubani ship` | Ship: test -> build -> deploy (preferred) |
| `kubani deploy` | Deploy to cluster (legacy, use `kubani ship` instead) |

### local-run Options

```bash
kubani local-run --agent <name> [options]

Options:
  --temporal [local|cluster]  Temporal mode (default: local)
  --output [console|discord|both]  Output mode (default: console)
  --hot-reload               Enable hot-reload on file changes
  --mock-services            Use mock services (no cluster needed)
  --tunnel                   Enable cluster service tunneling
```

---

## Configuration System

Configuration is loaded in order (later overrides earlier):

1. `config.default.yaml` — Base defaults (committed)
2. `config.{environment}.yaml` — Environment-specific (committed)
3. `config.local.yaml` — Local overrides (gitignored)
4. Environment variables with `KUBANI_` prefix

For Nexus specifically, `.env.nexus-local` and `.env.nexus-local.override` are used instead of `config.local.yaml`.

---

## Cluster Service URLs

All cluster services are reachable via the `*.almckay.io` ingress when connected to the cluster network (VPN/Tailscale).

| Service | URL |
|---------|-----|
| LLM (vLLM, Qwen3.5-9B-NVFP4) | `https://llm.almckay.io/v1` |
| LLM Fast (Qwen3-4B) | `https://llm-fast.almckay.io/v1` |
| Temporal UI | `https://temporal.almckay.io` |
| Temporal gRPC | `temporal.almckay.io:7233` |
| Nexus Gateway | `https://nexus.almckay.io` |
| Memory MCP | `https://mcp-gateway.almckay.io/memory` |
| Skills MCP | `https://skills-mcp.almckay.io` |
| Discord MCP | `https://discord-mcp.almckay.io` |
| Temporal MCP | `https://mcp-gateway.almckay.io/temporal` |
| Qdrant | `https://qdrant.almckay.io` |
| Grafana | `https://grafana.almckay.io` |
| Metadata API | `https://metadata.almckay.io` |

---

## Testing

```bash
# Run all tests
python -m pytest tests/ -v

# Run Nexus loop tests specifically
python -m pytest tests/test_nexus_loop_e2e.py tests/test_nexus_local_runner.py -v

# Run with coverage
python -m pytest tests/ --cov=kubani --cov-report=term-missing
```

---

## Deployment

Once local testing is complete, ship the component:

```bash
# Ship (test -> build -> push -> deploy -> verify)
kubani ship nexus-orchestrator

# Dry run (tests only, no build/deploy)
kubani ship nexus-orchestrator --dry-run

# Skip tests if already tested locally
kubani ship nexus-orchestrator --skip-test

# List all shippable components
kubani ship --list
```

---

## Troubleshooting

### Services unreachable

```bash
# Run health check to identify which services are down
python scripts/nexus_local_runner.py health

# Check VPN/Tailscale is connected
ping llm.almckay.io
```

### Secrets not set

```bash
# Run config check to identify missing or placeholder values
python scripts/nexus_local_runner.py check
```

### LLM errors

```bash
# Test LLM connectivity directly
curl -s https://llm.almckay.io/v1/models | jq '.data[].id'

# Try the fast model for quicker iteration
LLM_API_URL=https://llm-fast.almckay.io/v1 LLM_MODEL=Qwen3.5-9B-NVFP4 \
    python scripts/nexus_local_runner.py turn "Hello"
```

### MCP server errors

```bash
# Test a specific MCP server
curl -s https://skills-mcp.almckay.io/health

# Run with mock MCP (no MCP servers needed)
MCP_MEMORY_ENABLED=false MCP_SKILLS_ENABLED=false \
    python scripts/nexus_local_runner.py turn "Hello"
```

---

## See Also

- [Nexus Local Development ADR](../../plans/nexus/08-local-development.md)
- [Agent Evaluation](../agent-evaluation/SKILL.md)
- [Continuous Learning](../continuous-learning/SKILL.md)
- [Deployment](../deployment/SKILL.md)
- [MCP Servers](../mcp-servers/SKILL.md)
