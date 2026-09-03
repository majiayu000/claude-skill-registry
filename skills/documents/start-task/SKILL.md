---
name: start-task
description: "Bootstrap a task into a synced feature branch — one shot, zero confirmations. Detects the source from the args: GitHub issue ('#100', 'issue 100', 'gh issue 100', or bare '100'), Jira key ('PROJ-42'), or a local spec file path; ad-hoc conversation otherwise. Fetches the task, derives {type}/{number}/{slug}, syncs the default branch, creates and pushes the branch, and writes specs/context/<id>.md. Use only when the user explicitly asks to start a task or create a work branch — never trigger automatically."
model: inherit
color: cyan
---

# Start-Task

Turn a task reference into a synced feature branch named
`{type}/{number}/{slug}` plus a context file at `specs/context/<id>.md`.
Zero confirmations on the happy path: detect → fetch → derive → execute → report.

## 1. Detect the source (no bash)

Match the args in this order:

1. **Jira** — `[A-Z]+-\d+` (e.g. `PROJ-42`)
2. **GitHub issue** — a numeric token, stripping any of `github`, `gh`, `issue`, `issues`, `#`
3. **Local spec** — a path ending in `.md`, `.txt`, `.yaml`, `.yml`, or `.json`; reject any path containing `..`
4. **Ad-hoc** — nothing matched: ask once (a single question) for the task type, title, and identifier, then skip to step 3

## 2. Fetch (1 bash call)

**GitHub:**

```bash
gh issue view <ISSUE_NUM> --json title,labels --jq '{title: .title, labels: [.labels[].name]}'
```

**Jira:** `which acli && acli jira issue view <KEY>` — extract summary, type, key.
If `acli` is missing, hard-stop: the developer chose Jira; do not degrade to ad-hoc.

**Local spec:** read the file; extract title and scope. The identifier is the
developer-provided one or the filename stem.

On any fetch failure, hard-stop and print the error verbatim — no retries, no
paraphrasing, no follow-up questions.

## 3. Derive TYPE and SLUG (no bash)

**TYPE** — from GitHub labels (first match wins) or from the task's nature:

| Signal | TYPE |
|---|---|
| `bug`, `fix`, `hotfix` | `fix` |
| `enhancement`, `feature` | `feat` |
| `refactor` | `refactor` |
| `docs`, `documentation` | `docs` |
| `test`, `tests` | `test` |
| `ci`, `github-actions` | `ci` |
| `chore`, `deps`, `dependencies` | `chore` |
| _(no match)_ | `feat` |

**SLUG** — from the title: lower-case; drop articles, prepositions, and helper
verbs; keep the core action verb + object nouns; 2–4 words; hyphenated; only
`[a-z0-9-]`.

Examples: "Add user authentication to the login form" → `add-user-auth`;
"Fix null pointer in payment processing flow" → `fix-null-pointer-payment`.

## 4. Execute

**GitHub** (1 bash call) — the script syncs the default branch, creates the
branch, writes **and commits** the context file on it, then pushes:

```bash
bash {base_directory}/gh-start-task.sh <ISSUE_NUM> <TYPE> <SLUG>
```

Non-zero exit → hard-stop, print stderr verbatim. It fails on a dirty working
tree by design — never stash or discard for the developer.

**Jira / local / ad-hoc** — do the same steps manually:

```bash
git status --porcelain            # any output → hard-stop: uncommitted changes
git fetch origin <default> && git checkout <default> && git pull origin <default>
git checkout -b <TYPE>/<ID>/<SLUG> && git push -u origin <TYPE>/<ID>/<SLUG>
```

If the branch already exists locally, switch to it instead of creating it.
Then write `specs/context/<ID>.md` with: identifier, title, type, source,
relevant details (description, acceptance criteria), and today's date. If the
file exists, update it in place — don't overwrite wholesale.

## 5. Report (no bash)

```
Branch: <TYPE>/<ID>/<SLUG>
Task:   <ID> — <TITLE>
Context: specs/context/<ID>.md

Next:
  /plan-requirements   — capture WHAT and WHY
  /plan-architecture   — design the solution
  /implement           — start coding
```

## You Must NOT

- Ask for confirmation on the happy path — ad-hoc's single intake question is the only interactive moment
- Stash, discard, or commit the developer's pre-existing uncommitted changes — hard-stop instead (the GitHub script committing the context file *it just generated* is the one sanctioned exception)
- Push to `main`/`master`, or use `--force` on any push
- Paraphrase errors — print them verbatim so the developer gets the exact actionable message
- Fall back to ad-hoc when a chosen CLI tool is missing — fail clearly
- Trigger automatically — this skill is opt-in
