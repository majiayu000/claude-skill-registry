---
name: multi-model
description: Multi-model orchestration for ARIA. Activate when dispatching tasks to different LLM providers (OpenAI, local models, cloud providers) or when optimizing cost/latency tradeoffs.
---

# Multi-Model Orchestration

This skill enables ARIA to dispatch tasks to multiple LLM providers beyond Claude.

## Configuration Files

| File | Purpose |
|------|---------|
| `.claude/config/models.json` | Model registry and routing rules |
| `.claude/config/env.template` | API key template (copy to secure location) |
| `.claude/config/claude-code-router.template.json` | Router config for hybrid mode |
| `.claude/mcp-servers.json` | MCP server configurations |

## Multi-Model Modes

### Mode A: Full Replacement (Kimi K2 replaces Claude)
All Claude calls redirect to Kimi K2. Simplest setup.

### Mode B: Hybrid (Claude + Kimi K2 together) ⭐ Recommended
Use Claude as main orchestrator, Kimi K2 for subagents/background tasks.
Requires [claude-code-router](https://github.com/musistudio/claude-code-router).

### Mode C: Subagent-only
Keep Claude for everything, use Kimi K2 only when explicitly requested in Task prompts.

## Supported Providers

### Native Claude (via Task tool)
```python
# Built-in - no additional config needed
Task(subagent_type="general-purpose", model="opus", prompt="...")
Task(subagent_type="general-purpose", model="sonnet", prompt="...")
Task(subagent_type="general-purpose", model="haiku", prompt="...")
```

### External Models (via MCP or Bash)

#### 1. OpenAI (GPT-4, GPT-4o)
```bash
# Via aichat (configured in pixi.toml)
aichat -m openai:gpt-4-turbo "Your prompt here"

# Via direct API
curl https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "gpt-4-turbo", "messages": [{"role": "user", "content": "..."}]}'
```

#### 2. Local Models (Ollama)
```bash
# List available models
ollama list

# Run inference
ollama run llama3.2 "Your prompt here"

# Via API
curl http://localhost:11434/api/generate \
  -d '{"model": "llama3.2", "prompt": "..."}'
```

#### 3. LocalAI
```bash
# Start LocalAI server
localai run --models-path ./models

# Query (OpenAI-compatible API)
curl http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "llama3", "messages": [...]}'
```

#### 4. vLLM (High-throughput)
```bash
# Start vLLM server
python -m vllm.entrypoints.openai.api_server \
  --model mistralai/Mixtral-8x7B-Instruct-v0.1

# Query (OpenAI-compatible)
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "mistralai/Mixtral-8x7B-Instruct-v0.1", "messages": [...]}'
```

#### 5. Moonshot Kimi K2 (OpenAI-compatible)
```bash
# Using OpenAI SDK with Moonshot endpoint
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["MOONSHOT_API_KEY"],
    base_url="https://api.moonshot.ai/v1",
)

# Kimi K2 Instruct - best for agentic tasks
response = client.chat.completions.create(
    model="kimi-k2-instruct",
    messages=[{"role": "user", "content": "Analyze this codebase..."}],
    temperature=0.6,  # Recommended for K2
)

# Kimi K2 Thinking - step-by-step reasoning with tool use
response = client.chat.completions.create(
    model="kimi-k2-thinking",
    messages=[{"role": "user", "content": "Debug this complex issue..."}],
)
```

```bash
# Via curl (OpenAI-compatible)
curl https://api.moonshot.ai/v1/chat/completions \
  -H "Authorization: Bearer $MOONSHOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "kimi-k2-instruct",
    "messages": [{"role": "user", "content": "..."}],
    "temperature": 0.6
  }'

# Via aichat (if configured)
aichat -m moonshot:kimi-k2-instruct "Your prompt here"
```

#### 6. OpenRouter (Unified Gateway)
```bash
# Access Kimi K2 and 100+ models via single API
curl https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "moonshotai/kimi-k2",
    "messages": [{"role": "user", "content": "..."}]
  }'
```

## ARIA Multi-Model Dispatch Pattern

### Cost-Optimized Routing
```yaml
routing_strategy:
  # Use cheapest model that can handle the task
  simple_tasks:
    primary: claude.haiku      # Fast, cheap
    fallback: local.ollama     # Free, offline

  analysis_tasks:
    primary: claude.sonnet     # Balanced
    fallback: openai.gpt4      # Alternative

  complex_tasks:
    primary: claude.opus       # Best reasoning
    fallback: openai.gpt4      # Alternative
```

### Parallel Multi-Model Execution
```python
# Example: Get multiple perspectives on architecture decision
# Launch tasks to different models in parallel

# Claude perspective
Task(subagent_type="general-purpose", model="sonnet",
     prompt="Analyze this architecture from security standpoint...")

# OpenAI perspective (via Bash + aichat)
Bash(command='aichat -m openai:gpt-4 "Analyze this architecture..."')

# Local model (via Bash + ollama)
Bash(command='ollama run llama3.2 "Analyze this architecture..."')
```

### Consensus Pattern
```python
# Get agreement from multiple models before proceeding
models = ["claude.sonnet", "openai.gpt4", "local.llama3"]
responses = []

for model in models:
    response = query_model(model, prompt)
    responses.append(response)

# Require 2/3 agreement for critical decisions
consensus = check_consensus(responses, threshold=0.66)
```

## Hybrid Mode Setup (Claude + Kimi K2)

Use Claude as the main orchestrator and Kimi K2 for subagent/background tasks.

### 1. Install claude-code-router
```bash
npm install -g claude-code-router
```

### 2. Create Router Config
```bash
mkdir -p ~/.claude-code-router
cp .claude/config/claude-code-router.template.json ~/.claude-code-router/config.json
# Edit with your API keys
```

### 3. Router Configuration
```json
{
  "providers": [
    {
      "name": "anthropic",
      "api_base_url": "https://api.anthropic.com",
      "api_key": "$ANTHROPIC_API_KEY",
      "models": ["claude-opus-4-5-20251101", "claude-sonnet-4-20250514"]
    },
    {
      "name": "moonshot",
      "api_base_url": "https://api.moonshot.ai/anthropic",
      "api_key": "$MOONSHOT_API_KEY",
      "models": ["kimi-k2-thinking-turbo", "kimi-k2-instruct"]
    }
  ],
  "router": {
    "default": "anthropic,claude-sonnet-4-20250514",
    "think": "anthropic,claude-opus-4-5-20251101",
    "background": "moonshot,kimi-k2-thinking-turbo"
  }
}
```

### 4. Run with Hybrid Mode
```bash
# Activate router (sets ANTHROPIC_BASE_URL to local proxy)
ccr activate

# Run Claude Code - it will route to different models based on task
claude
```

### 5. Route Specific Subagents to Kimi K2
In Task prompts, add at the beginning:
```python
Task(subagent_type="general-purpose",
     prompt="""<CCR-SUBAGENT-MODEL>moonshot,kimi-k2-thinking</CCR-SUBAGENT-MODEL>

     Analyze this codebase for security vulnerabilities...""")
```

## Environment Setup

### 1. Copy API Key Template
```bash
# Option A: Project-local (gitignored)
cp .claude/config/env.template .claude/config/env

# Option B: User-global
cp .claude/config/env.template ~/.claude/env

# Edit with your actual API keys
```

### 2. Source Environment
```bash
# Add to ~/.bashrc or ~/.zshrc
ENV_FILE="${HOME}/.claude/env"
[ -f ".claude/config/env" ] && ENV_FILE=".claude/config/env"

if [ -f "$ENV_FILE" ]; then
  set -a
  source "$ENV_FILE"
  set +a
fi
```

### 3. Use Kimi K2 as Claude Replacement (Optional)
```bash
# Add to env file to use Kimi K2 instead of Claude:
export ANTHROPIC_BASE_URL=https://api.moonshot.ai/anthropic
export ANTHROPIC_AUTH_TOKEN=${MOONSHOT_API_KEY}
export ANTHROPIC_MODEL=kimi-k2-thinking-turbo
export ANTHROPIC_DEFAULT_OPUS_MODEL=kimi-k2-thinking-turbo
export ANTHROPIC_DEFAULT_SONNET_MODEL=kimi-k2-thinking-turbo
export ANTHROPIC_DEFAULT_HAIKU_MODEL=kimi-k2-thinking-turbo
export CLAUDE_CODE_SUBAGENT_MODEL=kimi-k2-thinking-turbo

# Then run Claude Code normally - it will use Kimi K2!
claude
```

### 4. Verify Configuration
```bash
# Check Claude
echo "Claude: ${ANTHROPIC_API_KEY:0:10}..."

# Check OpenAI
echo "OpenAI: ${OPENAI_API_KEY:0:10}..."

# Check Moonshot
echo "Moonshot: ${MOONSHOT_API_KEY:0:10}..."

# Check local models
ollama list
curl -s http://localhost:8080/v1/models | jq .  # LocalAI
```

## Model Selection Matrix

| Task Type | Recommended | Fallback | Reason |
|-----------|-------------|----------|--------|
| Orchestration | claude.opus | moonshot.kimi_k2 | Best reasoning |
| Agentic tasks | moonshot.kimi_k2 | claude.sonnet | 1T MoE, tool use optimized |
| Deep reasoning | moonshot.kimi_k2_thinking | claude.opus | Step-by-step with tools |
| Code review | claude.sonnet | moonshot.kimi_k2 | Code understanding |
| Coding tasks | moonshot.kimi_k2 | claude.sonnet | Strong coding benchmark |
| Documentation | claude.haiku | local.llama3 | Cost-effective |
| Vision/Images | openai.gpt4o | claude.sonnet | Multimodal |
| Private data | local.ollama | local.localai | Data stays local |
| High volume | local.vllm | local.localai | Throughput |
| Offline | local.ollama | - | No internet |

### Kimi K2 Specs
- **Architecture**: Mixture-of-Experts (MoE)
- **Total Parameters**: 1 trillion
- **Active Parameters**: 32 billion per forward pass
- **Strengths**: Agentic tasks, reasoning, coding
- **API**: OpenAI-compatible (https://api.moonshot.ai/v1)
- **Recommended temp**: 0.6

## Security Considerations

1. **Never commit API keys** - Use env files outside repo
2. **Rotate keys regularly** - Especially for production
3. **Use local models for sensitive data** - PII, proprietary code
4. **Audit model access** - Log which models see what data
5. **Rate limit external APIs** - Prevent cost overruns

## Troubleshooting

### Model not responding
```bash
# Check if service is running
curl -s http://localhost:11434/api/tags  # Ollama
curl -s http://localhost:8080/v1/models  # LocalAI

# Check API key
curl -s https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY" | jq .error
```

### Slow inference
```bash
# Use quantized models locally
ollama pull llama3.2:3b-instruct-q4_0  # Smaller, faster

# Or use vLLM for batching
python -m vllm.entrypoints.openai.api_server \
  --model meta-llama/Llama-3-8b-instruct \
  --tensor-parallel-size 2  # Multi-GPU
```

## Related Skills

- [AI Assistants](../ai-assistants/SKILL.md) - aichat, aider configuration
- [Inference](../inference/SKILL.md) - LocalAI, vLLM setup
- [Observability](../observability/SKILL.md) - Model metrics monitoring
