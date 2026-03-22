---
name: dev-create-pr
description: Analyze the working tree, stage relevant changes, create a branch if needed, commit, and open a pull request
argument-hint: "[--all] [branch-name]"
disable-model-invocation: false
---

Examine all uncommitted changes, identify what belongs to the current task,
prompt the user about anything ambiguous, create a branch (if on `main`),
commit with a descriptive message, and open a pull request.

**When to use this skill:**

- New or updated lessons under `lessons/`
- Library code, skills, CI, config, scripts, tests
- Mixed infrastructure work
- Bug fixes, refactors, or tooling changes

## Arguments

- `--all` (optional): Include all uncommitted changes without prompting.
  Skips the relevance check in Phase 2. Use when you know every change in the
  tree belongs to the same task.
- `branch-name` (optional): Explicit branch name to use. If omitted, the
  skill infers one from the changes (see Phase 3).

## Workflow

Work through each phase **in order**.

---

### Phase 1 — Survey the working tree

Gather a complete picture of what has changed.

Run these commands in parallel:

```bash
git status --short
git diff --stat
git diff --cached --stat
git branch --show-current
git log --oneline -5
```

**If there are no changes** (status and both diffs are empty):

- Report "Nothing to commit — working tree is clean." and stop.

**Collect:**

- The current branch name
- List of modified tracked files (staged and unstaged)
- List of untracked files
- List of deleted files
- Recent commit history (for context)

---

### Phase 2 — Classify changes by relevance

**Goal:** Every file in the commit must belong to the same logical unit of
work. Unrelated changes must not silently slip in, and must not be silently
excluded.

**If `--all` was passed**, skip this phase — stage everything and go to
Phase 3.

#### 2a. Identify the task

Determine what the current work is about by examining:

1. **The current branch name** — e.g. `lesson-30-new-topic` or `fix-checkbox-click`
   tells you the scope.
2. **Already-staged files** (`git diff --cached`) — these are the most explicit
   signal of intent.
3. **Recent commits on this branch** (if not on `main`) — shows what has been
   committed so far for this task.
4. **File clustering** — files in the same directory or module likely belong
   together.

Formulate a one-line description of the task, e.g.:
"Add UI Lesson 11 — Widget ID System" or "Fix checkbox click detection".

#### 2b. Classify each changed file

For every modified, added, deleted, or untracked file, assign one of:

| Classification | Meaning |
|---|---|
| **Relevant** | Clearly part of the current task |
| **Unclear** | Could belong to this task or could be unrelated |
| **Unrelated** | Clearly not part of the current task |

**Heuristics for classification:**

- Files in the same directory as staged changes → likely **Relevant**
- Files in a completely different module → likely **Unrelated**
- Build artifacts, compiled shaders, `.o` files → **Unrelated** (and likely
  gitignored already)
- Root-level project files (`CMakeLists.txt`, `README.md`, `PLAN.md`) → check
  if the changes reference the current task; if so **Relevant**, otherwise
  **Unclear**
- `.claude/skills/` files → **Relevant** if the skill matches the task topic
- Test files for the module being changed → **Relevant**

#### 2c. Handle each classification

**Relevant files:** Stage them. No prompt needed.

**Unclear files:** Present each to the user with context and ask:

```text
This file changed but may not belong to the current task:

  M  common/ui/forge_ui.h  (+12 -3)

  Diff summary: Added forge_ui_widget_id() declaration

Include in this PR?
```

Use AskUserQuestion with options:

- "Include" — stage the file
- "Exclude" — leave it unstaged (it stays in the working tree for a future commit)
- "View diff" — show the full diff for this file, then re-ask

**Unrelated files:** Present them as a group and confirm exclusion:

```text
These files appear unrelated to the current task and will NOT be included:

  ?? build/CMakeCache.txt          (build artifact)
  M  lessons/gpu/05-mipmaps/main.c (different lesson)
  ?? .DS_Store                      (OS file)

Proceed without these files?
```

Use AskUserQuestion with options:

- "Proceed" — leave them out
- "Let me pick" — switch to per-file prompting for this group

**CRITICAL — never silently exclude.** If a file has real code changes (not
build artifacts or OS junk), the user must be told it is being left out. The
purpose of this skill is to prevent both accidental inclusions AND accidental
omissions.

---

### Phase 3 — Create a branch (if needed)

**If already on a feature branch** (not `main`), skip to Phase 4.

**If on `main`:**

1. Ensure `main` is up to date:

   ```bash
   git pull origin main
   ```

2. Derive a branch name from the changes. Use the task description from
   Phase 2 to generate a kebab-case name:

   | Task description | Branch name |
   |---|---|
   | Add UI Lesson 11 — Widget ID System | `ui-lesson-11-widget-id` |
   | Fix checkbox click detection | `fix-checkbox-click` |
   | Add dev-create-pr skill | `add-dev-create-pr-skill` |
   | Update math library with cross product | `math-cross-product` |

   If the user provided a `branch-name` argument, use that instead.

3. Create and switch to the branch:

   ```bash
   git checkout -b <branch-name>
   ```

---

### Phase 4 — Stage, review, and local review

> **MANDATORY: Run `/dev-local-review` before committing.** No exceptions.
> Do NOT proceed to Phase 5 until the local review passes with zero findings.

1. **Stage all relevant files** (those classified as Relevant in Phase 2, plus
   any Unclear files the user chose to include):

   ```bash
   git add <file1> <file2> ...
   ```

   Stage files by explicit name — never use `git add -A` or `git add .`.

2. **Run quality checks on staged content:**

   - If any `.md` files are staged, lint only those files:

     ```bash
     git diff --cached --name-only -- '*.md' \
       | xargs -r npx markdownlint-cli2
     ```

     If errors are found in staged files, fix them, re-stage, and re-check.
     Never bypass lint rules.

   - If any `scripts/*.py` or `pipeline/*.py` files are staged, lint only those files:

     ```bash
     git diff --cached --name-only -z -- 'scripts/*.py' 'pipeline/*.py' 'tests/pipeline/*.py' \
       | xargs -0 -r uv run ruff check
     git diff --cached --name-only -z -- 'scripts/*.py' 'pipeline/*.py' 'tests/pipeline/*.py' \
       | xargs -0 -r uv run ruff format --check
     ```

     Fix issues if found.

   - If any Python files are staged (`scripts/`, `pipeline/`, or `tests/pipeline/`),
     run Pyright type checking:

     ```bash
     STAGED_PY=$(git diff --cached --name-only -- '*.py')
     [ -n "$STAGED_PY" ] && uv run pyright
     ```

     Fix issues if found.

3. **Show the final staging summary:**

   ```bash
   git diff --cached --stat
   ```

   Report the file count and total lines changed.

4. **Run `/dev-local-review`.**

   This is a mandatory gate. Run the local review skill and fix any findings
   it reports. Do NOT proceed to Phase 5 until it completes with zero findings.
   This catches problems before they reach the PR and burn a GitHub review
   round.

---

### Phase 5 — Compose the commit message

Analyze the staged diff to write a descriptive commit message.

```bash
git diff --cached
```

**Commit message format:**

```text
<type>: <short summary under 70 chars>

<body — what changed and why, wrapped at 72 chars>

Files changed:
- path/to/file.c — brief description of change
- path/to/other.h — brief description of change

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
```

**Type prefixes:**

| Prefix | When to use |
|---|---|
| `Add` | New feature, lesson, skill, or file |
| `Fix` | Bug fix |
| `Update` | Enhancement to existing functionality |
| `Refactor` | Code restructuring without behavior change |
| `Docs` | Documentation-only changes |
| `Chore` | Build, CI, config, or tooling changes |

**Rules for the message:**

- The summary line describes the *what* concisely
- The body explains the *why* — what motivated the change, what problem it
  solves, what the user will see differently
- List every changed file with a brief note (helps reviewers)
- Do not pad the message with filler — be direct
- If the changes span multiple concerns, note that honestly rather than
  forcing a single narrative

**Present the message to the user** before committing. Allow them to edit it.

---

### Phase 6 — Commit and push

0. **Block secrets before commit:**

   Scan staged file names for `.env` files or credential patterns. If any
   are found, refuse to proceed:

   ```bash
   # Block .env files
   git diff --cached --name-only \
     | grep -E '(^|/)\.env(\.|$)' && {
       echo "Refusing to commit .env files. Unstage them first."
       exit 1
     }

   # Block credential and key files
   if git diff --cached --name-only \
     | grep -Eq '(^|/)(credentials\.json|[^/]+\.pem|[^/]+\.key)$'; then
     echo "Refusing to commit credential/key files. Unstage them first."
     exit 1
   fi
   ```

1. **Commit:**

   ```bash
   git commit -m "$(cat <<'EOF'
   <commit message from Phase 5>
   EOF
   )"
   ```

2. **Push with upstream tracking:**

   ```bash
   git push -u origin <branch-name>
   ```

3. **Verify the push succeeded.** If it fails (e.g. network error, permission
   denied), report the error and stop.

---

### Phase 7 — Create the pull request

1. **Compose the PR title and body.**

   - **Title:** Same as the commit summary line (under 70 chars).
   - **Body:** Structured description derived from the commit message.

2. **Create the PR:**

   ```bash
   gh pr create --title "<title>" --body "$(cat <<'EOF'
   ## Summary
   <2-4 bullet points describing what changed and why>

   ## Changes
   <bulleted list of files with descriptions>

   ## Test plan
   - [ ] <relevant verification steps>

   🤖 Generated with [Claude Code](https://claude.com/claude-code)
   EOF
   )"
   ```

3. **Report the PR URL** to the user.

---

## Error handling

- **No changes to commit:** Report and stop — do not create an empty commit.
- **Branch already exists:** If the inferred branch name already exists,
  append a numeric suffix (`-2`, `-3`) or ask the user for a name.
- **Push rejected:** If the remote rejects the push (e.g. branch exists
  remotely with different history), report the error. Do not force-push.
- **`gh` CLI not authenticated:** Provide setup instructions
  (`gh auth login`) and stop.
- **Markdown lint fails:** Fix the issues — never bypass. See Phase 4.
- **Merge conflicts:** Should not happen on a fresh branch from `main`, but
  if they do, report and stop.

## Safety guarantees

- **Never uses `git add -A` or `git add .`** — always stages files by name.
- **Never silently ignores changed files** — every non-trivial change is
  either staged or explicitly acknowledged by the user as excluded.
- **Never silently includes unrelated changes** — unclear files are always
  prompted.
- **Never force-pushes.**
- **Never commits secrets or `.env` files** — if detected in the staged set,
  block the commit and exit so the user can unstage them.
- **Never bypasses quality checks** — lint must pass before commit.
- **Always shows the commit message** for user approval before committing.
