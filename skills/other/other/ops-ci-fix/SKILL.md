---
name: ops-ci-fix
description: Run typecheck and lint scoped to changed packages, fix all errors iteratively, and commit a clean state. Execute inline until the writer-lock patch-return pilot lands. Terminal condition is all affected packages pass typecheck and lint with zero errors.
---

# ops-ci-fix — Typecheck + Lint Fix Loop

Use this skill to clear typecheck and lint errors from the monorepo. No plan file needed.

**Terminal condition:** All affected packages pass `pnpm --filter <pkg> typecheck` and `pnpm --filter <pkg> lint`.
Full-repo runs (`pnpm typecheck` / `pnpm lint`) only when the change is cross-cutting or a scoped run
fails with a non-localized error.
**Max iterations per phase:** 5. If errors are not decreasing after 5 attempts, stop and surface remaining errors to the operator.

---

## Claude: Execution Mode

Current active policy: execute this skill inline.

Why:
- the previous shared-checkout Codex path relied on the stale `codex exec -a never --sandbox workspace-write` contract
- that path still holds the writer lock for the full mutable agent session
- the replacement patch-return pilot is not validated yet

Writer-lock is still required for writes. Claude is non-interactive in this context so wrap each
git write command rather than opening a subshell:
```bash
bash scripts/agents/with-writer-lock.sh -- git add <file1> <file2> ...
bash scripts/agents/with-writer-lock.sh -- git commit -m "..."
```

Do not offload this skill to a shared-checkout mutable Codex session until the active build-offload protocol is reactivated by the patch-return pilot.

---

## Codex: Execution Procedure

> **Writer lock:** Claude holds the lock via `with-writer-lock.sh` before launching this session.
> Codex inherits the lock token as a child process. Do NOT run `with-writer-lock.sh` or
> `integrator-shell.sh` yourself — you already have the lock.

### Phase 1 — Typecheck

Determine which packages changed:
```bash
git diff --name-only HEAD | sed 's|/.*||' | sort -u
```

Run typecheck scoped to each changed package:
```bash
pnpm --filter <pkg> typecheck 2>&1 | tee /tmp/typecheck-out.txt; echo "EXIT:$?"
```

Fall back to full-repo only when a scoped run fails with a non-localized error (e.g. a shared type
package is broken and errors appear in many packages):
```bash
pnpm typecheck 2>&1 | tee /tmp/typecheck-out.txt; echo "EXIT:$?"
```

For each error line matching `path/to/file.ts(line,col): error TSxxxx: <message>`:
1. Read the file at the reported path and line.
2. Diagnose using the Error Playbook below.
3. Apply the fix.

Repeat until all affected packages exit 0. Stop after 5 iterations on the same error.

### Phase 2 — Lint

Run lint scoped to each changed package using the **package's own lint script** (not raw eslint):
```bash
pnpm --filter <pkg> lint 2>&1 | tee /tmp/lint-out.txt; echo "EXIT:$?"
```

For auto-fixable errors (e.g. `simple-import-sort`): first check how the package runs lint:
```bash
# Read the package's lint script to understand its eslint invocation:
cat apps/<pkg>/package.json | grep -A1 '"lint"'
# e.g. apps/prime uses ./scripts/lint-wrapper.sh
```

If the lint script passes arguments through, run it with `--fix`:
```bash
pnpm --filter <pkg> lint -- --fix <file1> <file2> ...
```

If it does not pass arguments through, read the wrapper script to find the underlying eslint command
and replicate it with `--fix` on the specific files. Do not run `pnpm --filter <pkg> exec eslint --fix`
blindly — the wrapper may set config paths or NODE_OPTIONS that differ from the raw invocation.

For remaining errors, apply manual fixes using the Error Playbook below.

Run `pnpm --filter <pkg> lint` after each fix round. Repeat until exit 0. Stop after 5 iterations on
the same error.

### Phase 3 — Commit

> Writer lock is already held (inherited from Claude's `with-writer-lock.sh` invocation).
> Plain git commands work here — do not re-wrap them.

Stage only the files you changed. Never use `git add -A` or `git add .`.

```bash
git add <file1> <file2> ...
git commit -m "fix(ci): resolve typecheck and lint errors

Co-Authored-By: Codex <noreply@openai.com>"
```

---

## Error Playbook

### TypeScript errors

| Pattern | Fix |
|---|---|
| `Property 'x' is missing … but required` on a schema input type | Check if the schema field has `.optional().default(…)`. If so, change `z.infer<typeof schema>` to `z.input<typeof schema>` for the input type. |
| Property missing at call site | Add the missing property, or make it optional in the type if semantically correct. |
| Type mismatch (`not assignable to`) | Trace the type chain. Fix at the narrowest point — prefer fixing the type definition over adding casts. |
| `Object is possibly 'undefined'` | Add a null-check or use optional chaining. Only use `!` when the call site has already guaranteed non-null. |

### Lint errors

| Rule | Auto-fixable? | Fix |
|---|---|---|
| `simple-import-sort/imports` | Yes | Run lint with `--fix` via the package script (see Phase 2) |
| `max-lines-per-function` | No | Extract helper functions/constants to module scope (outside the `describe` block or containing function). Do not split test cases across files. |
| `ds/require-disable-justification` | No | Add a ticket ID to the disable comment: `// eslint-disable-line ds/no-hardcoded-copy -- PRIME-001 reason` |
| `ds/no-raw-font` | No | If the flagged string is a font-family value: replace with a CSS variable from the design token system. If it is an i18n key or data value (false positive): fix `containsDisallowed()` in `packages/eslint-plugin-ds/src/rules/no-raw-font.ts` to use word-boundary matching (`\b<font>\b`), then rebuild with `pnpm --filter @acme/eslint-plugin-ds build`. |
| `ds/no-hardcoded-copy` | No | **Warnings only — do not fix unless the rule fires as an `error`.** |
| `react-hooks/exhaustive-deps` | No | **Warnings only — do not fix unless the rule fires as an `error`.** |

### Escalate — do not attempt to fix

- Errors in generated files (`*.gen.ts`, `dist/`, `.next/`)
- Errors requiring new package dependencies
- The same error recurring after 5 fix attempts
- Errors in >10 files sharing the same root cause (likely a shared type or config change — surface to operator)

---

## Output Summary (end of session)

Always end with:

```
## ops-ci-fix Result

Typecheck: PASS | FAIL (N errors remaining)
Lint: PASS | FAIL (N errors remaining)

Files changed:
- path/to/file.ts — reason

Escalated (not fixed):
- path/to/file.ts:line — error message — reason for escalation
```
