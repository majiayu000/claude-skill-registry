---
name: codex-claude-loop
description: Dual-AI engineering loop orchestrating Claude Code (planning/implementation) and Codex (validation/review). Use when (1) complex feature development requiring validation, (2) high-quality code with security/performance concerns, (3) large-scale refactoring, (4) user requests codex-claude loop or dual-AI review. Do NOT use for simple one-off fixes or prototypes.
requires:
  - codex-plugin:codex-cli
---

# Codex-Claude Engineering Loop

## Workflow Overview

```
Plan (Claude) → Validate (Codex) → Implement (Claude) → Review (Codex) → Fix → Re-validate → Done
```

| Role | Responsibility |
|------|----------------|
| **Claude** | Architecture, planning, code implementation (Edit/Write/Read) |
| **Codex** | Validation, code review, quality assurance |

## Environment Notice

> **Non-TTY environment**: See [codex-cli SKILL](../codex-cli/SKILL.md#-environment-notice) for CLI fundamentals.
> **Key rule**: Always use `codex exec` in Claude Code (not `codex`)

## Phase 0: Pre-flight Check

Before executing any Codex command:

1. **Create context directory**:
```bash
mkdir -p .codex-loop
```

2. **Check Git Repository Status**
```bash
git rev-parse --git-dir 2>/dev/null && echo "Git OK" || echo "Not a Git repo"
```

3. **If NOT in Git repository**, ask user via `AskUserQuestion`:
   - "This directory is not a Git repository. Codex requires Git by default."
   - Options:
     - "Initialize Git repository here (`git init`)"
     - "Use `--skip-git-repo-check` flag (bypass check)"
     - "Cancel operation"

4. **Apply user choice**:
```bash
# Option 1: Initialize Git
git init

# Option 2: Use skip flag
codex exec --skip-git-repo-check -s read-only "prompt"
```

5. **Ask user via `AskUserQuestion`**:
   - Model preference (gpt-5.2-codex, gpt-5.2, gpt-5.1-codex-max, gpt-5.1-codex-mini)
   - Reasoning effort level (low, medium, high, xhigh)

## Phase 1: Planning (Claude)

1. Create detailed implementation plan
2. Break down into clear steps
3. Document assumptions and risks
4. Save to `.codex-loop/plan.md`

## Phase 2: Plan Validation (Codex)

Execute with `timeout: 600000`:

```bash
codex exec -m MODEL -c model_reasoning_effort=LEVEL -s read-only \
  "Review this plan: $(cat .codex-loop/plan.md) Check: logic, edge cases, architecture, security"
```

Save result: `> .codex-loop/phase2_validation.md`

## Phase 3: Feedback Loop

If issues found in `.codex-loop/phase2_validation.md`:
1. Summarize Codex feedback to user
2. Ask via `AskUserQuestion`: "Revise and re-validate, or proceed?"
3. If revise → Update `.codex-loop/plan.md` → Repeat Phase 2

## Phase 4: Implementation (Claude)

1. Implement using Edit/Write/Read tools
2. Execute step-by-step with error handling
3. Save summary to `.codex-loop/implementation.md`

## Phase 5: Code Review (Codex)

Execute with `timeout: 600000`:

```bash
codex exec -m MODEL -s read-only \
  "Review: $(cat .codex-loop/plan.md) $(cat .codex-loop/implementation.md) Check: bugs, performance, security. Classify: Critical/Major/Minor/Info"
```

Save result: `> .codex-loop/phase5_review.md`

Claude response by severity:
- Critical → Fix immediately
- Architectural → Discuss with user
- Minor → Document and proceed

## Phase 6: Iteration

1. Apply fixes from `.codex-loop/phase5_review.md`
2. Significant changes → Re-validate with Codex
3. Use `codex exec resume` for session continuity
4. Loop until quality standards met

## Context Files

```
.codex-loop/
├── plan.md               # Implementation plan
├── phase2_validation.md  # Plan validation result
├── implementation.md     # Implementation summary
├── phase5_review.md      # Code review result
└── iterations.md         # Iteration history
```

## Quick Reference

**Always use `timeout: 600000` (10 min)** for all Codex commands.

> **Models, reasoning effort, options**: See [codex-cli SKILL](../codex-cli/SKILL.md)

## Error Handling

> **Full error reference**: See [codex-cli SKILL](../codex-cli/SKILL.md#error-handling)

**Error Recovery Flow**:
1. Non-zero exit → Stop and report error message
2. Summarize error via `AskUserQuestion`
3. Confirm with user before: architectural changes, multi-file mods, `--skip-git-repo-check`

## Timeout Configuration

| Task Type | Recommended Timeout | Claude Code Tool |
|-----------|---------------------|------------------|
| All Codex operations | **10 minutes** | `timeout: 600000` |

> **Approval modes**: See [codex-cli SKILL](../codex-cli/SKILL.md) - valid values: `untrusted`, `on-failure`, `on-request`, `never`

## Best Practices

- **Always use `codex exec`** in Claude Code environment (non-TTY)
- **Always create `.codex-loop/`** directory at start
- **Always save outputs** to context files for traceability
- **Always validate plans** before implementation
- **Never skip review** after changes
- **Default to `-s read-only`** for all reviews
- **Use `resume`** for session continuity
- **Check Git status** before first Codex command
- **Ask user permission** before using `--skip-git-repo-check`
- **Set 10-minute timeout** for all Codex exec commands (`timeout: 600000`)

## References

- **Codex CLI fundamentals**: See [codex-cli SKILL](../codex-cli/SKILL.md) (models, options, error handling)
