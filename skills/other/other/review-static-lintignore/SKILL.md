---
name: review-static-lintignore
description: Audit all lint-ignore suppressions for appropriateness and overuse
user-invocable: true
disable-model-invocation: true
---
Enter planning mode. Audit every `lint-ignore` suppression in the codebase — both the check definitions and the usage sites. Use parallelism where possible.

## What lint-ignore Is

Static analysis checks in `tests/check_batch_*.ps1` support inline suppression via `; lint-ignore: <tag>` comments in `.ahk` source files. When a check encounters a suppressed line, it skips it. This is the escape hatch for legitimate exceptions — but escape hatches can also become workarounds that silently disable the checks they're supposed to enforce.

## Three-Phase Audit

### Phase 1 — Inventory which checks have lint-ignore support

Scan `tests/check_batch_*.ps1` files for suppression tag definitions. For each one, document:
- The tag name (e.g., `lint-ignore: critical-leak`)
- Which check/sub-check it belongs to
- What the check is trying to enforce
- How many usage sites exist in `.ahk` files

### Phase 2 — Evaluate each suppression tag

For each lint-ignore tag, write **both sides**:

**Argument for keeping it:**
- What legitimate exception does this cover?
- Is the pattern genuinely safe in specific contexts that the checker can't distinguish?

**Argument for removing it:**
- Does the escape hatch undermine the check's purpose?
- Could the check be made smarter to handle the legitimate cases without a suppression?
- Has the tag accumulated so many uses that the check is effectively disabled?

### Phase 3 — Audit every usage site

Every lint-ignore is required to have a parenthetical reason: `; lint-ignore: tag (reason)`. This is enforced by the `lint_ignore_reason` sub-check in `check_batch_patterns.ps1`.

For each `; lint-ignore:` comment in `.ahk` source files:

1. **Read the surrounding code** — is this a genuine exception or a workaround?
2. **Verify the stated reason** — is the parenthetical reason still accurate given the current code? Reasons can become stale after refactoring.
3. **Classify**:
   - **Appropriate** — the code is genuinely an exception the checker can't handle
   - **Workaround** — the code should be fixed to not need suppression
   - **Stale** — the code was changed and the suppression is no longer needed (line no longer triggers the check)
   - **Improvable** — the check could be enhanced to handle this case without suppression

## Validation

For each finding:

1. **Cite evidence**: "I verified by reading `file.ahk` lines X–Y" with the actual suppressed code quoted, and "check defined at `check_batch_X.ps1` line Z" showing what the check enforces.
2. **Trace the safety argument**: For appropriate suppressions, explain why the suppressed code is actually safe despite triggering the check.
3. **Counter-argument**: For workaround findings, note what would break or become harder if the suppression were removed without fixing the code.

## Plan Format

**Section 1 — Suppression tag inventory:**

| Tag | Check File | Enforces | Usage Count |
|-----|-----------|----------|-------------|
| `critical-leak` | `check_batch_guards.ps1` | Critical "Off" before return | 14 |

**Section 2 — Tag-level evaluation:**

| Tag | Keep Argument | Remove Argument | Verdict |
|-----|--------------|----------------|---------|
| `critical-leak` | State machine returns inside outer Critical scope — checker can't see caller context | 14 uses may indicate the check needs scope awareness | Keep — but enhance check |

**Section 3 — Per-usage audit:**

| File | Line | Tag | Code | Classification | Action |
|------|------|-----|------|---------------|--------|
| `gui_state.ahk` | 130 | `critical-leak` | `return ; lint-ignore: critical-leak` | Appropriate — outer function holds Critical | None |
| `foo.ahk` | 55 | `dead-param` | `MyFunc(a, b) { ; lint-ignore: dead-param` | Workaround — param `b` could be removed | Remove suppression, remove param |

Order by action needed: workarounds and stale suppressions first, appropriate ones last.

Ignore any existing plans — create a fresh one.
