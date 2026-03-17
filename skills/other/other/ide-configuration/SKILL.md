---
name: ide-configuration
description: Configure Claude Code CLI, Cursor IDE, and VS Code with various AI models using official documentation only. Kimi K2.5, GLM, Anthropic setup guides.
---

# IDE Configuration

Configure Claude Code CLI and Cursor IDE with official model providers.

## Quick Setup

### Claude Code + Kimi K2.5 (Recommended)

```powershell
# Windows PowerShell
$env:ANTHROPIC_BASE_URL = "https://api.moonshot.cn/anthropic/"
$env:ANTHROPIC_API_KEY = "sk-your-moonshot-key"
claude
```

```bash
# macOS/Linux
export ANTHROPIC_BASE_URL=https://api.moonshot.cn/anthropic/
export ANTHROPIC_API_KEY=sk-your-moonshot-key
claude
```

### Cursor + Kimi K2.5

1. Settings > Models
2. Add custom model: `kimi-k2-turbo-preview`
3. Or use OpenRouter: `https://openrouter.ai/api/v1`

## Official Sources Only

**When configuring, ALWAYS verify with:**
- Moonshot: https://platform.moonshot.cn/docs
- Anthropic: https://docs.anthropic.com
- Cursor: https://docs.cursor.com

**Never use unverified third-party guides for configuration.**

## Model Selection Guide

| Need | Model | Provider |
|------|-------|----------|
| Speed | kimi-k2-turbo-preview | Moonshot |
| Reasoning | kimi-k2-thinking | Moonshot |
| Long context | kimi-k2-0905-preview | Moonshot |
| General | sonnet | Anthropic |
| Vision | glm-4.6v | Z.AI |

## Troubleshooting

| Issue | Check |
|-------|-------|
| 429 errors | Account balance/RPM limits |
| Model not found | Exact model name from official docs |
| Connection fail | API endpoint URL correctness |

See full guide: `docs/agent-instructions/setup-guides/model-configuration-faq.md`
