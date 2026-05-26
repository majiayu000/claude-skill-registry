---
name: agent-run
description: Run prompt with OpenAI or Gemini provider via agent CLI
user-invocable: true
allowed-tools: Bash
argument-hint: [provider] [prompt] [skills]
---

# Agent Run

Run with user's arguments:

```bash
/home/faisal/EventMarketDB/agent -p "$2" --provider $1 --skills "$3"
```

- `$1` = provider (openai/gemini/claude)
- `$2` = prompt (required)
- `$3` = skills (optional)
