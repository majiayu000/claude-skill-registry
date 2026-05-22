---
name: ops-chutes
description: >
  Manage Chutes.ai resources, tracking subscription quota and account balance.
  Integrates with scheduler to pause operations when quota is reached.
triggers:
  - check chutes
  - chutes usage
  - chutes budget
  - chutes status
  - chutes models
  - list chutes models
  - what models are on chutes
  - chutes model list
  - is model X ready?
  - wait for chutes reset
  - can I run X calls?
  - check chutes health
  - chutes api check
metadata:
  short-description: Chutes.ai API management and Quota tracking
---

# Ops Chutes Skill

Manage Chutes.ai resources and monitor subscription quota and account balance.

## Triggers

- "Check chutes status" -> `status`
- "How much chutes budget left?" -> `usage`
- "Is chutes working?" -> `sanity [model]`

## Commands

```bash
# Check model status (hot/cold/down)
./run.sh status

# Check Subscription Quota and Remaining Balance
./run.sh usage [--chute-id <id>] [--json]

# Explore all available models (filterable)
# Flags: --query (name), --owner (sglang/vllm), --modality (text/image), --feature (reasoning/tools), --json
./run.sh models [--query <search>] [--owner <owner>] [--modality <modality>] [--feature <feature>] [--json]

# Check model health (HOT/COLD/DOWN)
./run.sh model-health <model_id>

# Run sanity check (Inference via Qwen/Qwen2.5-72B-Instruct)
./run.sh sanity [model_name]

# Check budget (exit 1 if Quota exhausted OR Balance < CHUTES_MIN_BALANCE)
./run.sh budget-check

# Wait until quota resets (7PM ET)
./run.sh wait-for-reset [--timeout <seconds>]

# Verify if a batch of calls is feasible (exit 1 if not)
./run.sh can-complete <num_calls>
```

## Environment Variables

| Variable             | Description                               |
| -------------------- | ----------------------------------------- |
| `CHUTES_API_TOKEN`   | API Token (standard)                      |
| `CHUTES_API_KEY`     | API Key (alternative naming)              |
| `CHUTES_MIN_BALANCE` | Minimum balance threshold (default: 0.05) |

## Concurrency & Rate Limiting

> [!WARNING]
> **Concurrecy Limit**: Chutes.ai can only handle **5-6 concurrent connections** per token.
> If this limit is exceeded, the API will return a 429 Rate Limit error and typically impose a **90-second pause** before resuming.
