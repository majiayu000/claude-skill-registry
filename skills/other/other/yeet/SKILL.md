---
argument-hint: <create-pr|update-pr|create-issue|create-discussion> [options]
disable-model-invocation: false
name: yeet
user-invocable: true
description: This skill should be used when the user asks to "create a pull request", "create PR", "open PR", "update a pull request", "update PR", "create an issue", "file an issue", "create a GitHub issue", "create a Claude Code issue", "report a bug in Claude Code", "create a Codex issue", "report a bug in Codex CLI", "create a Sablier issue", "file an issue in sablier-labs", "create a discussion", "start a GitHub discussion", "yeet a PR", "yeet an issue", "yeet a discussion", or mentions GitHub contribution workflows.
---

# GitHub Contribution Workflows

Facilitate GitHub-based open source contribution workflows including pull requests, issues, and discussions. Emphasizes semantic analysis over mechanical operations — understand the intent and context of changes before generating titles, descriptions, or selecting templates. All generated content should be conversational and informal.

## Prerequisites

Verify GitHub CLI authentication before any workflow:

```bash
gh auth status
```

For pull request workflows, also verify:

- Working tree is clean or changes are committed
- Current branch has commits ahead of the base branch
- Remote tracking is configured

## Related Skills

For detailed GitHub CLI command syntax, flags, and patterns, activate the `cli-gh` skill.

## Workflows

Each workflow is fully documented in its reference file. Load the appropriate reference based on user intent.

| Workflow | Trigger | Reference |
|---|---|---|
| Create PR | "create PR", "open PR", "yeet a PR" | `references/create-pr.md` |
| Update PR | "update PR", "edit PR" | `references/update-pr.md` |
| Create Issue | "create issue", "file issue" (generic repo) | `references/create-issue.md` |
| Claude Code Issue | "Claude Code issue", "report bug in CC" | `references/issue-claude-code.md` |
| Codex CLI Issue | "Codex issue", "report bug in Codex" | `references/issue-codex-cli.md` |
| Sablier Issue | "Sablier issue", "sablier-labs issue" | `references/issue-sablier.md` |
| Biome Issue | "Biome issue", "biomejs issue" | `references/issue-biome.md` |
| Create Discussion | "create discussion", "start discussion" | `references/create-discussion.md` |

Shared patterns (auth validation, admonitions, HEREDOC syntax, semantic analysis, tone, platform normalization, error handling, file links) are in `references/commons.md`.
