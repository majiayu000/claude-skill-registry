---
name: token-check
description: Analyze current session token usage and suggest optimizations
disable-model-invocation: true
allowed-tools: Bash
---

Analyze the current Claude Code session for token efficiency:

## Check These

1. **Context loaded**: What CLAUDE.md, rules, and skills are currently loaded?
2. **MCP servers**: How many tool definitions are in context?
3. **Conversation length**: How many turns deep are we?
4. **File reads**: Have we read the same file multiple times?

## Suggest

- Whether to `/compact` the conversation
- Whether to `/clear` and start fresh
- Which MCP servers to disable if unused
- Whether CLAUDE.md is too large
- Whether rules files should use path-scoping

## Output

```
Session Health Report
─────────────────────
Context usage: [estimate]
Conversation turns: [count]
Suggested action: [compact / clear / continue]
Optimization tips: [specific suggestions]
```

<!-- Skill by Huzefa Nalkheda Wala | claude-code-optimizer -->
