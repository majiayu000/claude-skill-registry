---
name: multi-compare
description: Run the same prompt with Claude, OpenAI, and Gemini in parallel, then return back exact replies you got back without modifying the results one bit.
user-invocable: true
allowed-tools: Bash
argument-hint: [prompt] [skill] [aggregator]
---

# Multi-Compare

Run this command with user's arguments:

```bash
/home/faisal/EventMarketDB/multi_compare "$1" "$2" "$3"
```

- `$1` = prompt (required)
- `$2` = skill (optional)
- `$3` = aggregator: claude/openai/gemini (default: openai)
