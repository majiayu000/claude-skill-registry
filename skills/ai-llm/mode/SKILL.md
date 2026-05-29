---
name: mode
description: Use when the user wants to change optimization aggressiveness, switch between aggressive/balanced/thorough modes, or adjust token-saving behavior.
disable-model-invocation: true
allowed-tools: Read, Write, Bash
argument-hint: "[aggressive|balanced|thorough]"
---

Switch optimization mode to: **$ARGUMENTS**

## Available Modes

### Aggressive Mode
**Goal:** Maximum token savings. Use for routine tasks, simple edits, well-understood codebases.

Rules:
- `MAX_THINKING_TOKENS=4000` — minimal thinking for simple operations
- Fork ALL exploration — never explore in main context
- Read ONLY the specific lines needed (always use offset/limit)
- Skip reading files you can infer from context
- Use Haiku for all subagent tasks
- Compact after every 5 tool calls
- Never read more than 50 lines from any file at once
- Prefer Grep → targeted Read over full file reads
- One-sentence responses unless the user asks for detail

### Balanced Mode (Default)
**Goal:** Good savings with reasonable context. Use for general development work.

Rules:
- `MAX_THINKING_TOKENS=10000` — standard thinking budget
- Fork exploration and review tasks
- Read full files when needed, but use offset/limit for large files
- Use Sonnet for most tasks, Opus for complex ones
- Compact after reading 10+ files
- Normal response length

### Thorough Mode
**Goal:** Maximum context and quality. Use for complex debugging, architecture decisions, security audits.

Rules:
- `MAX_THINKING_TOKENS=32000` — deep thinking for complex problems
- Read related files fully to understand context
- Use Opus for implementation, Sonnet for simple subagents
- Don't compact aggressively — keep context for cross-referencing
- Explore broadly before narrowing down
- Detailed explanations and reasoning in responses
- Run extra verification passes

## How to Apply

When the user invokes `/mode [name]`:

1. Acknowledge the mode switch
2. State the key behavior changes
3. Apply the rules for the rest of this session

Example response:
```
Switched to **aggressive** mode.
- Minimal thinking, maximum token savings
- All exploration forked to subagents
- Targeted file reads only
- Compact responses
```

If no argument given, show current mode and the three options.

## Mode Comparison

| Aspect | Aggressive | Balanced | Thorough |
|--------|-----------|----------|----------|
| Thinking budget | 4K | 10K | 32K |
| Exploration | Always forked | Fork when large | Direct when useful |
| File reading | Targeted lines | Full when needed | Full + related |
| Model selection | Haiku subagents | Sonnet default | Opus default |
| Response style | Terse | Normal | Detailed |
| Best for | Routine edits | General dev | Complex problems |

<!-- Skill by Huzefa Nalkheda Wala | github.com/huzaifa525 | claude-code-optimizer -->
