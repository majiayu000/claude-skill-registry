---
model: claude-haiku-4-5-20251001
description: Create a Conventional Commits-compliant git commit — analyzes staged changes, drafts a message, and confirms before executing.
tools: Bash, Read
---

# /commit

Create a git commit following the **Conventional Commits** specification. Analyze staged changes, infer the best commit message, show it for confirmation, then execute.

## Invocation format

```
/commit [hint?]
```

- **No args** — analyze staged (or unstaged) changes and infer everything automatically.
- **With hint** — use the hint as extra context when generating the message (e.g., `/commit fixes the null-ref on startup`).

---

## Conventional Commits structure

Every commit message follows this shape:

```
<type>(<scope>): <subject>

[optional body]

[optional footer(s)]
```

### Type — required

| Type | When to use |
|---|---|
| `feat` | A new feature visible to users or callers of the module |
| `fix` | A bug fix |
| `docs` | Documentation only (comments, markdown, XML docs) |
| `test` | Adding or correcting tests — no production code changes |
| `refactor` | Code change that is neither a bug fix nor a new feature |
| `perf` | Performance improvement |
| `build` | Changes to build system, project files, Directory.Build.props, NuGet |
| `ci` | CI/CD pipeline changes (GitHub Actions, scripts) |
| `chore` | Maintenance tasks that don't fit elsewhere (dependency bumps, cleanup) |
| `style` | Formatting, whitespace — no logic change |

### Scope — optional but preferred

Use the module or layer affected. Keep it lowercase and short.

Examples: `sample-collection`, `test-orders`, `domain`, `infra`, `outbox`, `startup`

### Subject — required

- Imperative mood, present tense: **"add barcode command"** not "added" or "adds"
- No capital first letter
- No period at the end
- Max ~72 characters on the first line

### Body — optional

Use when the *why* is not obvious from the subject. Wrap at 100 characters.

### Footer — optional

| Footer key | Usage |
|---|---|
| `BREAKING CHANGE: <description>` | Any breaking API or contract change — triggers a major version bump |
| `Closes #<n>` / `Fixes #<n>` | Link to an issue |
| `Co-Authored-By: Name <email>` | Co-author attribution |

A commit with `BREAKING CHANGE:` in the footer (or a `!` after the type/scope) is a **breaking change**, regardless of type.

---

## Phase 1 — Understand what changed

Run these in parallel:

1. `git status --short` — see staged vs unstaged files
2. `git diff --staged` — full diff of what is staged
3. `git log --oneline -5` — recent commits (to match the project's style and scope vocabulary)

If **nothing is staged**, check `git diff --stat` (unstaged). If there are unstaged changes, tell the user what you found and ask:
- Should I stage everything (`git add -A`) and commit?
- Or should I stage specific files? (list them)

Do not stage or commit without confirmation when nothing is staged.

---

## Phase 2 — Analyze and draft

Using the diff:

1. **Identify the type** — is this new behaviour, a fix, docs, test-only, etc.?
2. **Identify the scope** — which module or layer is touched? Use the folder name as a guide (`SampleCollection` → `sample-collection`).
3. **Write the subject** — one concise imperative phrase describing *what* changed.
4. **Decide if a body is needed** — add one only if the *why* is non-obvious (e.g., a workaround, a deliberate design choice, a tricky fix).
5. **Check for breaking changes** — if any public interface, integration event contract, or module facade method signature changed incompatibly, add `BREAKING CHANGE:` to the footer.
6. **Add `Co-Authored-By`** — always append:
   ```
   Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
   ```

---

## Phase 3 — Show and confirm

Display the full proposed commit message in a code block, like this:

```
feat(sample-collection): add CreateBarcode command and handler

Implements step 5 of the collection workflow. The command carries
tubeType, barcodeValue, technicianId, and createdAt — all required
by CollectionRequest.CreateBarcode().

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```

Then ask the user:
> Commit with this message? (yes / edit / cancel)

- **yes** — proceed to Phase 4
- **edit** — ask what to change and regenerate; show again before committing
- **cancel** — stop; do not commit

---

## Phase 4 — Execute

Run the commit using a HEREDOC to preserve formatting exactly:

```bash
git commit -m "$(cat <<'EOF'
<full message here>
EOF
)"
```

After the commit succeeds, show the one-line output from `git log --oneline -1`.

If the pre-commit hook fails:
1. Read the hook output carefully.
2. Fix the reported issues.
3. Re-stage affected files.
4. Create a **new** commit — never use `--amend` unless the user explicitly asks for it.

---

## Rules — never violate

- **Never** use `git add -A` or `git add .` without explicit user approval.
- **Never** skip hooks (`--no-verify`).
- **Never** amend unless the user explicitly requests it.
- **Never** push; only commit.
- **Never** commit files that likely contain secrets (`.env`, `*credentials*`, `*secret*`). Warn the user instead.
