---
name: claude-config
description: Cheat sheet for Claude Code Router configuration and installation.
---

# Claude Code Router Configuration

Example configuration file for Claude Code Router:

```json
{
  "Providers": [
    {
      "name": "openrouter",
      "api_base_url": "https://gateway.ai.cloudflare.com/v1/0177dfd3fc04f0bb51d422b49f2dad20/jyasu-demo/openrouter/v1/chat/completions",
      "api_key": "?",
      "models": [
        "deepseek/deepseek-chat-v3-0324:free"
      ],
      "transformer": {
        "use": ["openrouter"]
      }
    },
    {
      "name": "gemini",
      "api_base_url": "https://gateway.ai.cloudflare.com/v1/0177dfd3fc04f0bb51d422b49f2dad20/jyasu-demo/google-ai-studio/v1/models/",
      "api_key": "?",
      "models": ["gemini-2.5-flash", "gemini-2.5-pro"],
      "transformer": {
        "use": ["gemini"]
      }
    },
      {
        "name": "gemini",
        "api_base_url": "https://generativelanguage.googleapis.com/v1beta/models/",
        "api_key": "?",
        "models": ["gemini-2.5-flash", "gemini-2.5-pro"],
        "transformer": {
          "use": ["gemini"]
        }
      },
      {
        "name": "gemini",
        "api_base_url": "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions",
        "api_key": "?",
        "models": ["gemini-2.5-flash", "gemini-2.5-pro"],
        "transformer": {
          "use": ["openapi"]
        }
      },
      {
        "name": "gemini",
        "api_base_url": "https://gateway.ai.cloudflare.com/v1/0177dfd3fc04f0bb51d422b49f2dad20/jyasu-demo/google-ai-studio/v1beta/openai/chat/completions",
        "api_key": "?",
        "models": ["gemini-2.5-flash", "gemini-2.5-pro"],
        "transformer": {
          "use": ["openapi"]
        }
      }
  ],
  "Router": {
    "default": "openrouter,deepseek/deepseek-chat-v3-0324:free",
    "background": "openrouter,deepseek/deepseek-chat-v3-0324:free",
    "think": "openrouter,deepseek/deepseek-chat-v3-0324:free",
    "longContext": "openrouter,deepseek/deepseek-chat-v3-0324:free",
    "longContextThreshold": 60000,
    "webSearch": "openrouter,deepseek/deepseek-chat-v3-0324:free"
  }
}
```

**Installation**
```bash
npm install -g @anthropic-ai/claude-code
npm install -g @musistudio/claude-code-router
mkdir ~/.claude-code-router
touch ~/.claude-code-router/config.json
git clone https://github.com/wshobson/agents .claude/agents/wshobson
git clone https://github.com/dl-ezo/claude-code-sub-agents  .claude/agents/dl-ezo
# https://github.com/ruvnet/claude-flow
```

Path to config file: `~/.claude-code-router/config.json`
