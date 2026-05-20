---
name: setup
description: Run Wayfinder Paths setup - install dependencies, create wallets, configure API key
metadata:
  tags: setup, onboarding, config
---

## When to use

Use this skill when:
- Setting up Wayfinder Paths for the first time
- Updating your API key
- Creating new wallets
- Troubleshooting configuration issues

## How to use

Run the setup script:

```bash
python3 scripts/setup.py
```

This will:
1. Ensure Python 3.12 and Poetry are installed
2. Install all dependencies
3. Prompt for your Wayfinder API key (get one at https://strategies.wayfinder.ai)
4. Create `config.json` from the template
5. Generate local development wallets
6. Configure the MCP server

### Options

- `--api-key KEY` - Provide API key non-interactively
- `--non-interactive` - Fail instead of prompting (for CI)

### After Setup

1. Enable the MCP server when Claude prompts

### Troubleshooting

If you see "api_key not set":
- Edit `config.json` and add your key under `system.api_key`
- Or re-run setup: `python3 scripts/setup.py`

Get your API key at: **https://strategies.wayfinder.ai**

## Rules

- [rules/api-key.md](rules/api-key.md) - API key configuration details
