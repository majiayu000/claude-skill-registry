---
name: commit
description: "One-shot conventional commit; bundled scripts adaptively gather diff context, draft the message, and stage+commit — pass `ask` to confirm first or add a hint for the title. Use only when the user asks for a commit."
model: inherit
color: lightcoral
---

# Commit

Commit the current changes with a conventional message. Two bundled scripts own
every git inspection and mutation — run no other git commands.

**Arguments:** the optional word `ask` (confirm mode) and/or a message hint for
the title (e.g. `/commit ask fix null check in auth`). Without `ask`, resolve
all ambiguity yourself and pause for nothing.

## Steps

### 1. Gather

```bash
{base_directory}/gather.sh
```

Prints branch, extracted task number (`NONE` if none), status, sensitive files
(auto-excluded later), full diffstat, recent commits, and an adaptively sized
diff. Read it once — never re-run git to "see more"; the script already chose
what matters.

If it prints `NOTHING_TO_COMMIT`, say so and stop.

### 2. Draft

Compute every field silently from the blob:

- **Type** — `feat` (new functionality), `fix` (corrects behavior), `refactor`
  (restructure, no behavior change), `docs` (only `.md`), `test` (only tests),
  `chore` (config/deps/tooling), `style` (formatting), `ci` (CI config).
  Mixed signals → pick the dominant one.
- **Task number** — `TASK_NUMBER` from the blob. If `NONE`, omit the `(scope)`
  and the `Refs:` trailer entirely. Never invent one, never leave one blank.
- **Title** — imperative mood, total header ≤72 chars. Base on the hint if given.
- **Description** — 1–3 specific sentences: what changed and why.

Write it to a temp file **unique to this checkout** — parallel worktrees each run
their own `/commit`, and a shared fixed path races. Use
`/tmp/commit-msg-{task-number}.txt`; when `TASK_NUMBER` is `NONE`, use
`/tmp/commit-msg-{branch}.txt` with `/` replaced by `-`:

```bash
cat > /tmp/commit-msg-{task-number}.txt <<'EOF'
{type}({task-number}): {title}

{description}

Refs: {task-number}
EOF
```

### 3. Commit

**Default (no `ask`):** run immediately, with no narration between tool calls.

**With `ask`:** show the draft message and the status list, then ask
*"Commit this? (yes / edit / only <files> / cancel)"*. Apply any edit or file
selection, then run.

```bash
{base_directory}/commit.sh /tmp/commit-msg-{task-number}.txt [file ...]
```

No file args → stages everything. File args (ask mode) → stages only those.
Either way the script drops sensitive files and embedded git repositories
(nested worktrees, stray clones — real submodules are kept), then commits with
hooks running.

- Hook failure → report the script output and stop. No workarounds.
- `NOTHING_STAGED` → everything was excluded; report and stop.

## Report

≤3 lines: the commit header, anything excluded, confirmation that
it's committed. Do not re-print the message body.

## You Must NOT

- Run `git add` or `git commit` yourself — the scripts own all mutation.
- Use `--no-verify` or bypass hooks in any way.
- Push to remote or run tests — not this skill's job.
- Ask questions in default mode — `ask` is the only interactive path.
