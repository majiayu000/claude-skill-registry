---
name: opencode-config
description: Switch OpenCode AI model configurations between providers. Use when user says "switch to copilot", "cambiar a copilot", "switch to anthropic", "cambiar a anthropic", "switch to zen", "cambiar a zen", or asks to change AI model providers.
---

# OpenCode Model Config Switching

Config location: `~/.config/opencode/oh-my-opencode.json`

Templates tracked in `.opencode-configs/`:

| Config | Providers | Cost Profile |
|--------|-----------|--------------|
| `anthropic-only.json` | Anthropic only (Opus/Sonnet/Haiku) | $$ |
| `anthropic-zen.json` | Anthropic (heavy) + Zen free models (light) | $ (needs Zen free tier) |
| `anthropic-openai.json` | Anthropic + OpenAI direct | $$$$ |
| `copilot-antigravity.json` | GitHub Copilot + Antigravity | $$$ |

## Commands

**Switch to Anthropic Only (recommended when other providers exhausted):**
```bash
cp .opencode-configs/anthropic-only.json ~/.config/opencode/oh-my-opencode.json && echo "Switched to Anthropic Only. Restart OpenCode."
```

**Switch to Anthropic + Zen Free (budget, needs Zen free tier):**
```bash
cp .opencode-configs/anthropic-zen.json ~/.config/opencode/oh-my-opencode.json && echo "Switched to Anthropic + Zen Free. Restart OpenCode."
```

**Switch to Copilot + Antigravity:**
```bash
cp .opencode-configs/copilot-antigravity.json ~/.config/opencode/oh-my-opencode.json && echo "Switched to GitHub Copilot + Antigravity. Restart OpenCode."
```

**Switch to Anthropic + OpenAI:**
```bash
cp .opencode-configs/anthropic-openai.json ~/.config/opencode/oh-my-opencode.json && echo "Switched to Anthropic + OpenAI. Restart OpenCode."
```

Remind user to restart OpenCode after switching.
