---
name: investigate
description: "Use when user asks 'what is X', 'how does X work', 'find out about', 'analyze', 'explain the code', or needs quick codebase investigation. Returns findings directly in conversation without saving files. Prefer this over Explore agent."
disable-model-invocation: false
context: fork
allowed-tools: Read, Glob, Grep, Bash, WebSearch, WebFetch
---

# /investigate

This skill performs rapid, documentation-driven codebase investigation and reports findings directly.

## Pre-fetched Context

- **Llmdoc exists:** !`test -d llmdoc && echo "llmdoc initialized" || echo "No llmdoc directory"`
- **Llmdoc index:** !`cat llmdoc/index.md 2>/dev/null | head -100 || echo "No index"`
- **Doc structure:** !`find llmdoc -name "*.md" 2>/dev/null | head -50`
- **Project structure:** !`ls -la 2>/dev/null | head -20`

## Investigation Protocol

### Phase 1: Documentation First

Before touching any source code, you MUST:

1. Check if `llmdoc/` exists (see pre-fetched context above).
2. If exists, read relevant documents in this order:
   - `llmdoc/index.md` - navigation and overview
   - `llmdoc/overview/*.md` - project context
   - `llmdoc/architecture/*.md` - system design
   - `llmdoc/guides/*.md` - workflows
   - `llmdoc/reference/*.md` - conventions

### Phase 2: Code Investigation

Only after exhausting documentation, investigate source code:

1. Use `Glob` to find relevant files.
2. Use `Grep` to search for patterns.
3. Use `Read` to examine specific files.

### Phase 3: Report

Output a concise report with this structure:

```markdown
#### Code Sections
- `path/to/file.ext:line~line` (SymbolName): Brief description

#### Report

**Conclusions:**
> Key findings...

**Relations:**
> File/module relationships...

**Result:**
> Direct answer to the question...
```

## Key Practices

- **Stateless**: Output directly, do not write files.
- **Concise**: Report under 150 lines.
- **No Code Blocks**: Reference code with `path/file.ext` format, not paste.
- **Objective**: State facts only, no subjective judgments.
