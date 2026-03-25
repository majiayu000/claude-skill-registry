---
name: optimize-tokens
description: Search the web for latest Claude Code token optimization tips and analyze current project setup
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Bash, WebSearch, WebFetch
---

Search for the latest token optimization strategies and analyze this project's setup.

## Steps

### 1. Web Research
Search for the latest tips:
- "Claude Code token optimization 2026"
- "Claude Code reduce token usage"
- "Claude Code cost saving tips"
- "Claude Code .claudeignore best practices"

Summarize the top 5-10 NEW tips found online.

### 2. Analyze Current Project

**Check CLAUDE.md:**
- Does it exist? How many lines?
- Is it under 200 lines?
- Does it have entry points, flow diagrams, decisions?

**Check .claudeignore:**
- Does it exist?
- Does it cover: node_modules, dist, lock files, binary assets?

**Check .claude/rules/:**
- Are rules path-scoped?
- Are there rules loading unnecessarily?

**Check .claude/skills/:**
- Are exploration skills using `context: fork`?
- Are side-effect skills using `disable-model-invocation: true`?

**Check MCP servers:**
- How many tool definitions are loaded?
- Any unused servers?

**Check settings:**
- Is MAX_THINKING_TOKENS capped?
- What model is being used?

### 3. Output Report

```
## Token Optimization Report

### Current Setup Score: [X/10]

### What's Good
- [things already optimized]

### Quick Wins (do now)
| Action | Estimated Savings | Effort |
|--------|------------------|--------|
| [action] | [X%] | [Low/Med/High] |

### Latest Tips from Web
- [tip 1 — source]
- [tip 2 — source]
- [tip 3 — source]

### Recommended Changes
1. [specific change with file path]
2. [specific change with file path]
3. [specific change with file path]
```

<!-- Skill by Huzefa Nalkheda Wala | github.com/huzaifa525 | claude-code-optimizer -->
