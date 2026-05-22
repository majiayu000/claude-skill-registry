---
name: git-hygiene
description: How to track our work through commits, pull-requests, and pushes. Maintain proper git hygiene in our chaotic, multi-agent environment through atomic commits, with the option to have code reviewed by AI agents with PRs.
---

# Git Hygiene

## Rules

- link associated **Linear** issues (e.g., `XY-123`) when committing (when present)
- keep local work on `main`; use PR branches only for review/delivery when asked
  - I am a one man team, working too fast to deal with endless PRs and branches
- prefer **atomic commits**: only committing your work, listing paths explicitly and checking the code for changes from other agents
  - prefer **explicit paths** (or `git add -p`) over `git add .`
  - quote paths containing brackets/parentheses so the shell doesn't treat them as globs/subshells.
- do not let a dirty working tree block progress
  - commit only staged changes (your files); ignore other dirty files
  - never stage/commit someone else’s changes “just to clean things up”
  - avoid operations that require a clean working tree (rebases, non-ff merges) unless explicitly needed
- commit by default
  - Do **not** push or open PRs unless the user explicitly asks for it
- do **not** run destructive git ops (`git reset --hard`, force pushes, etc.) unless explicitly instructed
- Before deleting files (or using deletion to "fix" tests/lint), stop and ask
- never discard file content you didn't author (e.g., `git restore <path>`, `git checkout -- <path>`) unless explicitly instructed
- `git restore --staged ...` is allowed for staging hygiene (it does not discard working tree changes)
- always double-check `git status` before and after each commit

## Dirty Working Tree (Multi-Agent Reality)

Goal: keep shipping without stepping on other agents.

- You can always commit your work while other files are dirty: stage only your paths, then commit.
- Prefer fetch-only “sync” (`git fetch origin --prune`). It never touches the working tree.
- Avoid rebasing and avoid merging `origin/main` into a dirty working tree unless explicitly required (e.g., GitHub shows unavoidable conflicts / branch protection requires up-to-date).

## Remote Sync (origin/main)

Default: stay productive. Fetch for awareness. Only “integrate” when necessary.

- Always safe: `git fetch origin --prune`
- Avoid `git pull` by default (it bakes in merge/rebase behavior that’s easy to forget).
  - If you ever run `git pull` and it blocks/conflicts: do not stash or commit random work “to unblock”. Stop and ask Ian for input.
- Prefer merge commits on PR merge (see **Commit + PR Workflow**) so local commits keep their SHAs.

1. **Refresh your view of remote**
   - `git fetch origin --prune`
2. **Check divergence**
   - `git rev-list --left-right --count origin/main...HEAD`
   - Output is `<behind> <ahead>` (how many commits you are behind/ahead of `origin/main`)
3. **Pick the safe action**
   - `behind>0` and `ahead=0`: optional fast-forward (only if the working tree is clean)
     - `git merge --ff-only origin/main`
   - `behind=0` and `ahead>0`: you’re ahead locally; OK to keep committing locally
   - `behind>0` and `ahead>0`: you have local commits *and* `origin/main` moved
     - default: do nothing; keep committing your work; publish via PR branch when asked
     - avoid rebasing local `main` (rewrites history) unless explicitly instructed

## Modes

- **Commit-only (default):** create atomic commits locally.
- **Commit + PR (only when explicitly requested):** create atomic commits, push to a `pr/...` branch, open PR, optionally trigger AI review, and (optionally) merge.

## Commit Messages

Use a conventional prefix, then a concise summary. If a Linear issue exists, include it consistently.

- prefixes: `feat:`, `fix:`, `refactor:`, `docs:`, `chore:`, `agents:`
- preferred issue format: append in parentheses: `... (XY-123)`

## Staging Cookbook

Keep these moves in muscle memory:

- stage interactively: `git add -p`
- stage explicit paths: `git add path/to/file.ts path/to/other.ts`
- unstage (keep edits): `git restore --staged path/to/file.ts`
- amend last commit (local only): `git commit --amend`
- inspect staged-only scope: `git diff --staged --name-only`

### Commit Workflow (DEFAULT)

1. **Snapshot state + sanity-check scope**
   - `git status -sb`
   - `git diff`
   - `git diff --staged`
   - `git diff --staged --name-only`
   - `git diff --name-only` (optional; useful to spot other-agent edits you should ignore)
   - `git log -5 --oneline`
2. **Refresh remote view (cheap)**
   - `git fetch origin --prune`
3. **Propose a commit plan**
   - Group changes by issue or intent & suggest commit titles (see **Commit Messages** above)
   - Call out anything ambiguous and ask before proceeding
4. **Execute commits one by one**
   - Stage minimally (`git add -p` or explicit paths)
   - Avoid `git add .` unless the user explicitly asks for a "one big commit"
   - Run the smallest relevant verification (tests / lint / build)
   - Write a clear message; include linked issue IDs when applicable (Linear/GitHub)
5. **Final check**
   - Confirm your intended changes are committed (or explain what remains dirty)
   - Summarize what each commit contains + any follow-ups

## Commit + PR Workflow (WHEN REQUESTED)

1. Do the **Commit** workflow above first
2. **Fetch before publishing**
   - `git fetch origin --prune`
   - `git rev-list --left-right --count origin/main...HEAD`
   - If you are `behind>0` and `ahead=0` and the working tree is clean: optionally fast-forward (`git merge --ff-only origin/main`)
   - Otherwise: do not block; proceed to publish PR branch
3. **Push to a PR branch (without switching branches)**
   - Branch naming: `pr/<short-description>`
   - `git push origin HEAD:pr/<short-description>`
4. **Create PR**: prefer non-interactive creation and self-assigning:
   - `gh pr create --head pr/<short-description> --base main --assignee @me --fill`
5. **Review loop**: set a 5 minute timeout and then check the PR’s GitHub comments for AI code-review agent feedback (automatically triggered on PR creation)
   - if straightforward/clear, do yourself and commit/push; if unclear/opinionated, ask for feedback
   - repeat **review loop** until satisfactory (check-in if repeated issues)
6. **Merge**: once everything looks good, provide a summary and ask for merge approval
   - prefer merge commits to avoid rewriting commit SHAs (keeps local `main` compatible with `origin/main`):
     - `gh pr merge --merge --delete-branch`
   - if blocked (required reviews/checks), leave a handoff with PR number + what's missing

## Rebase Safety

If rebasing is required, avoid interactive editor prompts:

- prefer scoping to a single command (avoid persistent shell env changes):
  - `GIT_EDITOR=: GIT_SEQUENCE_EDITOR=: git rebase origin/main`
- (or use `--no-edit` when safe)
