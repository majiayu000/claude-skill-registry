---
name: doc-workflow
description: "Use when user asks about 'documentation workflow', 'how to document', 'doc system', 'what is llmdoc', 'how does llmdoc work', or needs guidance on the documentation system."
disable-model-invocation: false
allowed-tools: Read, Glob, AskUserQuestion
---

# /doc-workflow

This skill provides guidance on the llmdoc documentation system and available documentation workflows.

## Pre-fetched Context

- **Llmdoc status:** !`test -d llmdoc && echo "INITIALIZED" || echo "NOT_INITIALIZED"`
- **Doc count:** !`find llmdoc -name "*.md" 2>/dev/null | wc -l`
- **Doc index:** !`cat llmdoc/index.md 2>/dev/null | head -30`

## Workflow Guide

### If llmdoc is NOT initialized:

Recommend running `/tr:initDoc` to initialize the documentation system.

Explain the benefits:
- Documentation-driven development
- LLM-optimized retrieval maps
- Consistent project understanding

### If llmdoc IS initialized:

Explain the available workflows:

| Task | Command/Skill | Description |
|------|--------------|-------------|
| Read docs | `/read-doc` | Quick project understanding |
| Update docs | `/update-doc` | Sync docs after code changes |
| Investigate | `/investigate` | Doc-first codebase research |
| Initialize | `/tr:initDoc` | One-time setup (already done) |

### llmdoc Structure

```
llmdoc/
├── index.md          # Navigation hub
├── overview/         # "What is this project?"
├── architecture/     # "How does it work?" (LLM Retrieval Map)
├── guides/           # "How do I do X?"
└── reference/        # "What are the specifics?"
```

## Actions

1. Check the pre-fetched context to determine llmdoc status.
2. Based on user's question, provide relevant guidance.
3. If user wants to perform an action, guide them to the appropriate skill/command.
