---
name: setting-up-oh-my-opencode
description: Use when installing or configuring oh-my-opencode plugin for OpenCode, or when Vertex AI models need to be configured for Claude/Gemini access
---

# Setting Up oh-my-opencode

Install and configure oh-my-opencode plugin with platform-appropriate model routing.

## Prerequisites

1. **OpenCode installed** via home-manager (from llm-agents.nix)
2. **Authentication configured:**
   - ChatGPT Plus: `opencode auth login` → OpenAI → headless
   - Vertex AI (macOS): `gcloud auth application-default login`

## Platform Subscription Summary

| Platform | Claude | OpenAI | Gemini | Copilot |
|----------|--------|--------|--------|---------|
| **devbox** | Max 20x (personal) | ChatGPT Plus | No | No |
| **macOS** | Vertex AI (work) | ChatGPT Plus | Vertex AI (work) | Yes (work) |

## Verify Vertex AI Access (macOS only)

Before installing, confirm Vertex AI credentials work:

```bash
# Check env vars
echo "GOOGLE_CLOUD_PROJECT: $GOOGLE_CLOUD_PROJECT"
echo "VERTEX_LOCATION: $VERTEX_LOCATION"

# Test model access
opencode models | grep google-vertex
opencode run --model google-vertex/gemini-2.5-flash "Say hello"
opencode run --model google-vertex-anthropic/claude-sonnet-4@20250514 "Say hello"
```

## Installation

### macOS (Vertex AI + ChatGPT + Copilot)

```bash
npx oh-my-opencode install --no-tui \
  --claude=yes \
  --openai=yes \
  --gemini=yes \
  --copilot=yes
```

### Devbox (Max 20x + ChatGPT)

```bash
npx oh-my-opencode install --no-tui \
  --claude=max20 \
  --openai=yes
```

## Post-Install: Configure Vertex AI Models (macOS)

The installer configures `anthropic/` and `google/` model names, but macOS should route through Vertex AI for work billing.

Edit `~/.config/opencode/oh-my-opencode.json`:

| Before | After |
|--------|-------|
| `anthropic/claude-opus-4-5` | `google-vertex-anthropic/claude-opus-4-5@20251101` |
| `anthropic/claude-sonnet-4-5` | `google-vertex-anthropic/claude-sonnet-4-5@20250929` |
| `anthropic/claude-haiku-4-5` | `google-vertex-anthropic/claude-haiku-4-5@20251001` |
| `google/gemini-3-flash` | `google-vertex/gemini-3-flash-preview` |
| `google/gemini-3-pro` | `google-vertex/gemini-3-pro-preview` |

Replace all occurrences in both `agents` and `categories` sections.

## Verification

```bash
# Check agent assignments
cat ~/.config/opencode/oh-my-opencode.json | jq '.agents.sisyphus, .agents.oracle'

# Test a Vertex AI model
opencode run --model google-vertex-anthropic/claude-opus-4-5@20251101 "Say 'Vertex AI working'"
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `opencode: command not found` | Run `home-manager switch` to install opencode |
| Vertex AI models not listed | Check `GOOGLE_CLOUD_PROJECT` and `gcloud auth application-default login` |
| "Permission denied" on Vertex | Verify IAM permissions in GCP console |
