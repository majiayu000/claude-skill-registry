---
name: archive-issue
description: "Retire a closed issue's working artifacts out of specs/ into the GitHub wiki. Use only when the user asks to archive a finished issue, empty out specs/ for a done task, or move an issue's requirements/architecture/tasks/review/QA docs to the wiki."
model: inherit
color: gold
---

# Archive Issue

Once an issue closes, GitHub is the source of truth for its scope — but its requirements,
architecture, code-review, and QA docs under `specs/` still hold reasoning worth keeping. This
skill retires them out of `specs/` straight into the GitHub wiki. **Nothing archived is ever
committed to the main repo** — the wiki is the only place this content lives.

This skill resolves everything from the issue number alone via `gh issue view` plus the
artifact naming contract (`REQ-<N>-<slug>.md` / `ARCH-<N>-<slug>.md` / `TASKS-<N>-<slug>.md` /
`QA-<N>-<slug>.md` / `QA-RESULTS-<N>-<slug>.md` and the `> **Issue:** #N` metadata row) that
`plan-requirements`, `plan-architecture`, `generate-tasks`, `plan-qa`, and `execute-qa` write. There is no separate anchor file — GitHub already holds the title,
URL, and state.

**Declared dependency:** matching review reports to this issue reads the `Target` metadata
row defined in `review/report-template.md:8`. If that row's format ever changes, review
discovery here breaks — see Step 2's failure behavior for what happens when it does.

## Step 0 — Ensure the local wiki clone is current

Work happens in a local working clone of the wiki repo, conventionally at `.wiki/` in the main
repo root:

- If `.wiki/` doesn't exist: `git clone <repo>.wiki.git .wiki`. If the clone fails because the
  wiki was never initialized on GitHub, **stop** and tell the developer to create the first
  wiki page in the GitHub UI (a repo's wiki doesn't exist as a cloneable git remote until at
  least one page has been saved there) — do not attempt to create the wiki repo yourself.
- If it exists: `git -C .wiki pull --ff-only` before making any changes, so you're not
  archiving on top of a stale copy.
- Verify `.wiki/` is listed in `.gitignore`; if it isn't, add it — this clone must never enter
  the main repo's history.
- If `.wiki/Home.md` and `.wiki/_Sidebar.md` don't exist yet (first archive ever in this repo),
  they're bootstrapped in Step 5, not here.

All of Steps 3–5 write into this clone, not into the main repo.

## Step 1 — Resolve the issue, confirm closed

Take the issue number from the user (`/archive-issue 70`, or "archive issue 70"). If it isn't
purely numeric, **stop** — this skill is GitHub-only; a Jira key or other tracker ID has no
wiki page shape to produce here.

`gh issue view <N> --json title,url,state,closedAt` gives the title, URL, state, and close
date. If the state is not `CLOSED`, **stop and say so** — this is a retirement step, not a
drafting one; open-issue artifacts stay in `specs/` where the active pipeline expects them.
Make no changes to `specs/` or `.wiki/`.

## Step 2 — Discover the source artifacts

Resolve each source for issue `<N>` using this fallback order — **never** report "nothing to
archive" while files for `<N>` remain unmatched under `specs/`:

| Source | How it's found |
|---|---|
| `specs/context/<N>.md` | direct path |
| `specs/requirements/REQ-<N>-*.md` | glob first; if it misses, grep `specs/requirements/*.md` for a `> **Issue:** #<N>` row (covers artifacts written before the naming contract landed); if still nothing, check for an un-prefixed `REQ-<slug>.md` whose slug matches a `{type}/<N>/{slug}` branch found in `git for-each-ref --format='%(refname:short)' refs/heads refs/remotes`, or — when that branch was already deleted, the usual case for an old issue — the slugified issue title from Step 1 |
| `specs/architecture/ARCH-<N>-*.md` | same three-tier fallback as REQ |
| `specs/tasks/TASKS-<N>-*.md` | same three-tier fallback as REQ (the TASKS file shares the `<N>-<slug>` stem with ARCH; ARCH's `> **Tasks:**` header row names it explicitly when present) |
| `specs/reviews/CODE-REVIEW-PIPELINE-<N>-*.md` | glob — the filename already carries `<N>` because it derives from the ARCH filename (`review/SKILL.md`'s pipeline-mode save step) |
| `specs/reviews/CODE-REVIEW-{PR,BRANCH,STAGED,DIFF}-*.md` | read **every** file's `Target` row (`review/report-template.md:8`) and match it to issue `<N>` — never by assuming a PR number equals the issue number, and never by directory. Branch-mode: `Target` is a branch name — match if it is `{type}/<N>/{slug}`. PR-mode: `Target` is a PR URL — resolve its head branch (`gh pr view <PR#> --json headRefName`) and match that the same way. Staged/diff-mode reports carry no branch reference and can only be attributed if the report content otherwise names issue `<N>` explicitly |
| `specs/qa/QA-<N>-*.md` | same three-tier fallback as REQ (glob → `> **Issue:** #<N>` header row → slug match). A `QA-PR-<number>.md` fallback (general-mode plan with no issue) attributes like a PR-mode review report: resolve the PR's head branch via `gh pr view <number> --json headRefName` and match `{type}/<N>/{slug}` |
| `specs/qa/QA-RESULTS-<N>-*.md` | shares its plan's stem with a `RESULTS` infix (`QA-21-billing.md` → `QA-RESULTS-21-billing.md`) — attribute it exactly as its plan resolved; a results file whose plan is unattributed stays unattributed too |

Most issues (bugs, chores, small enhancements) never had a REQ/ARCH/review doc — only archive
what actually exists. Don't invent placeholder pages for missing docs, and don't rename
anything — only the directory changes (`specs/requirements/` → `issue-NNN/`), never the
filename.

**Failure mode: loud, not blocking.** When a file under `specs/` cannot be attributed to `<N>`
by any tier above — a `Target` row absent, malformed, or naming a different issue's branch —
do **not** stop and do **not** silently skip it. Archive everything you *can* resolve, then end
your report with a prominent unresolved block:

```
⚠  2 file(s) under specs/ could not be attributed to issue #35 and were NOT archived:
     specs/reviews/CODE-REVIEW-PR-41.md   — Target row absent
     specs/reviews/CODE-REVIEW-BRANCH-x.md — Target 'feat/12/other' ≠ issue #35
   These remain in the repo. Attribute them manually or re-run after fixing the Target row.
```

Unresolved files stay exactly where they are and are **excluded from Step 6's `git rm`** — a
file that was never archived must never be deleted. This is why discovery failure is
non-fatal: partial archival is safe precisely because removal is scoped to what Step 4 actually
wrote.

## Step 3 — Write the hub page

`.wiki/issue-NNN.md` (zero-padded to 3 digits). The metadata line is mandatory:

```
**PR(s):** #NN[, #MM…] · **Closed:** YYYY-MM-DD · [GitHub issue #N](url)
```

- No PR found for this issue (branch-mode review, or no review at all) → `**PR(s):** —
  (branch review)` or `**PR(s):** —` respectively; never omit the field.
- Multiple PRs against the same issue → list all of them, comma-separated.

Below the metadata line: a paragraph of what shipped (pull from the issue body's Summary —
don't re-derive it), a bullet list linking each sub-page that exists, and a one-line Outcome
pulled from the acceptance criteria or review verdict.

**Link sub-pages by bare basename, never full path.** Write `[Label](CODE-REVIEW-PR-63)`, not
`[Label](issue-NNN/CODE-REVIEW-PR-63.md)` — even though the file lives at
`issue-NNN/CODE-REVIEW-PR-63.md`. GitHub's wiki renders a `.md`-suffixed link as a raw-file
link instead of a wiki-page link, which silently breaks navigation. Drop both the `issue-NNN/`
directory prefix and the `.md` extension; the directory nesting is only for organizing the
wiki's git tree.

## Step 4 — Write the sub-pages

Carry the REQ/ARCH/TASKS/review/QA content over largely as-is — these are already well-formed
docs; don't rewrite them, just relocate them into `.wiki/issue-NNN/` **under their original
filenames** and drop anything that's now stale (e.g. a REQ doc's "next step: run
`/plan-architecture`" footer no longer applies once archived). Only for documents that
actually exist — never invent a placeholder, never rename one that does exist.

## Step 5 — Update the index

Both `.wiki/Home.md` and `.wiki/_Sidebar.md` are a single flat list, ascending by issue
number — no grouping model:

- Create both files with a one-line header if this is the first archived issue overall.
- Insert this issue's entry in ascending issue-number order among the existing entries — find
  the correct position, don't just append.
- If the issue was archived before (a partial or interrupted prior run), **locate and update**
  its existing entry rather than appending a duplicate.

## Step 6 — Retire the sources from the main repo

`git rm`, in the **main repo** (not `.wiki/`): `specs/context/<N>.md`, whichever of
`specs/requirements/`/`specs/architecture/`/`specs/tasks/`/`specs/qa/` were mirrored, and every review
report Step 2 successfully attributed — **excluding** anything named in the unresolved
block. Commit this separately from the wiki push in Step 7 — they're two different repos
with two different histories.

This commit lands on whatever branch the main repo is currently on — normally the default
branch, since archival runs post-merge. **Tell the developer it is unpushed** and let them
decide how it reaches the remote: a protected default branch needs a PR, an unprotected one
just needs a push. Never push the main repo yourself; Step 7's confirmation covers the wiki
only.

## Step 7 — Commit and push the wiki, with confirmation

Inside `.wiki/`: `git -C .wiki pull --ff-only` immediately before committing (not only back in
Step 0 — time has passed), then `git add`, commit (batch multiple issues archived in one pass
into one commit if convenient). **Confirm with the user before pushing** — this publishes to
shared external state, same as any other push, even though the commit itself is harmless to
make locally.

If the push is rejected (another lane pushed to the wiki first): `git -C .wiki pull --rebase`,
then retry the push **once**. Never run a second `--ff-only` here — with a local commit
present, fast-forward is impossible on diverged histories. If the rebase itself conflicts
(e.g. two lanes both edited `Home.md`), **stop and surface the conflict** rather than resolving
it silently.

Report what moved where (source path → wiki page) so the developer can review before/after the
push.

## Re-running

Archiving the same issue twice is safe: the hub and sub-pages simply overwrite, `git rm` is
re-attempted (a no-op if already removed), and the index entry is located-and-updated rather
than appended a second time.

## You Must NOT

- Support non-GitHub issue trackers — the wiki target is GitHub-specific.
- Rename any archived file — only its directory changes.
- Create placeholder sub-pages for documents that don't exist.
- Add a bundled script — this skill's work is markdown authoring.
- Delete any file that was not successfully archived.
- Push to the wiki without explicit developer confirmation.
