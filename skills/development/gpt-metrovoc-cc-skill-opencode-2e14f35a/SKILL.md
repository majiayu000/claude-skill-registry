---
name: gpt
description: "Use GPT-5.2 for long-running coding tasks: large refactors, feature implementation etc."
allowed-tools: Bash, Read
---

# GPT-5.2 (via ocw)

Long-context coding. Best for: large refactors, feature implementation.

## Prompt Guidelines

GPT strictly follows instructions. Provide as much **high-level design context** as possible:

- Architecture decisions, data flow, component responsibilities
- Constraints, edge cases, expected behaviors

**Avoid**:

- Contradictory requirements (GPT will struggle to reconcile conflicts)
- Code snippets — GPT writes code well on its own; use tokens for design info instead

## Create Session (with worktree for code edits)

```bash
ocw new gpt --worktree
```

Returns:

- Line 1: 6-char hash
- Line 2: worktree path (e.g., `/path/to/ocw-abc123`)

The worktree is an isolated git branch. Work there freely.

## Create Session (read-only, no worktree)

```bash
ocw new gpt
```

## Chat

```bash
ocw chat <hash> << 'EOF'
your prompt
EOF
```

## Chat with File

```bash
ocw chat <hash> -f /path/to/spec.md << 'EOF'
implement based on this
EOF
```

## Worktree Workflow

1. `ocw new gpt --worktree` → get hash + path
2. Work in worktree: `cd /path/to/ocw-{hash}`
3. Edit, commit, push as needed
4. When done: `git worktree remove /path/to/ocw-{hash}`

## List Sessions

```bash
ocw list
```
