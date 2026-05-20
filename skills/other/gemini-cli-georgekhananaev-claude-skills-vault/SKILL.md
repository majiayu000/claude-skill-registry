---
name: gemini-cli
description: Run Gemini CLI for AI queries. Use when user asks to "run/ask/use gemini", compare Claude vs Gemini, or delegate tasks to Gemini.
---

# Gemini CLI

Interact w/ Google's Gemini CLI locally. Run queries, get responses, compare outputs.

## Prerequisites

Gemini CLI must be installed & configured:

1. **Install:** https://github.com/google-gemini/gemini-cli
2. **Auth:** Run `gemini` & sign in w/ Google account
3. **Verify:** `gemini --version`

## When to Use

- User asks to "run/ask/use gemini"
- Compare Claude vs Gemini responses
- Get second AI opinion
- Delegate task to Gemini

## Usage

```bash
# One-shot query
gemini "Your prompt"

# Specific model
gemini -m gemini-3-pro-preview "prompt"

# JSON output
gemini -o json "prompt"

# YOLO mode (auto-approve)
gemini -y "prompt"

# File analysis
cat file.txt | gemini "Analyze this"
```

## Comparison Workflow

1. Provide Claude's response first
2. Run same query via Gemini CLI
3. Present both for comparison

## CLI Options

| Flag | Desc |
|------|------|
| `-m` | Model (gemini-3-pro) |
| `-o` | Output: text/json/stream-json |
| `-y` | Auto-approve (YOLO) |
| `-d` | Debug mode |
| `-s` | Sandbox mode |
| `-r` | Resume session |
| `-i` | Interactive after prompt |

## Best Practices

- Quote prompts w/ double quotes
- Use `-o json` for parsing
- Pipe files for context
- Specify model for specific capabilities