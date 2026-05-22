---
name: coderabbit-review
description: Use CodeRabbit CLI to receive external code review feedback and address identified issues. Invoke this skill when the user requests CodeRabbit review, or proactively after implementing significant code changes to get feedback and improve code quality.
compatibility: Requires coderabbit CLI, git, and access to the internet. The target directory must be a git repository.
license: Apache-2.0
---

# Coderabbit Review

## Workflow

1. After implementing code changes, request a review from CodeRabbit
2. Analyze the review results and understand the feedback
3. Fix the identified issues
4. Re-run the review if necessary to confirm fixes

## Command Reference

- `--prompt-only`: Show only AI agent prompts (implies --plain)
- `--plain`: Output in plain text format with human-friendly formatting
- `--type <type>`: Review type: all, committed, uncommitted (default: "all")
- `--base <branch>`: Base branch for comparison
- `--base-commit <commit>`: Base commit on current branch for comparison
- `--cwd <path>`: Working directory path (default: current directory)

## Command Selection

**Review all changes (default):**

```bash
coderabbit review --prompt-only
```

**Review uncommitted changes only:**

```bash
coderabbit review --prompt-only --type uncommitted
```

**Review committed changes only:**

```bash
coderabbit review --prompt-only --type committed
```

**Compare against base branch:**

```bash
coderabbit review --prompt-only --base <branch>
```

## Handling Review Feedback

When review feedback is received, address issues in the following priority order:

1. **Security issues** - Fix immediately
2. **Bugs/regressions** - High priority fixes
3. **Missing tests** - Add required test coverage
4. **Code quality** - Implement refactoring and improvements
5. **Style/conventions** - Align with project standards

## Verification

After addressing the feedback, re-run `coderabbit review --prompt-only` to confirm that the issues have been resolved.
