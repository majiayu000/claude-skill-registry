---
name: vendor-sync
description: "Pull latest upstream changes from vendor subtrees into this project. Use when the user says 'sync vendor', 'pull upstream', 'update subtrees', 'vendor pull', 'vendor sync', 'sync vendors', 'vendor changes', or wants to update any vendor package from its upstream repository. Also use when the user mentions a vendor package name followed by 'pull', 'sync', or 'update'."
argument-hint: "[package-name]"
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - mcp__basic-memory__search_notes
  - mcp__basic-memory__read_note
  - mcp__basic-memory__edit_note
---

# Vendor Sync

Pull latest upstream changes into one or more vendor subtrees, cross-reference
the diff against open upstream issue tracking entries, and re-link workspace
packages.

## Registry

Read the vendor subtree registry from `.claude/vendor-registry.json`. Each
entry has the shape:

```json
{ "prefix": "vendor/pkg", "remote": "remote-name", "branch": "branch-name", "package": "@scope/pkg-name" }
```

- **prefix** — the local `vendor/` directory used as the subtree prefix
- **remote** — the git remote alias configured in this repo
- **branch** — the upstream branch to pull from
- **package** — the npm package name; maps to `UPSTREAM-<name>.md` filename
  (slashes → `--`, drop leading `@`): e.g. `@voxpelli/pkg` → `UPSTREAM-voxpelli--pkg.md`

If `.claude/vendor-registry.json` does not exist, tell the user and stop. Do
not attempt to read the subtree table from any other source.

## Workflow

### 1. Determine scope

Read and parse `.claude/vendor-registry.json`. Then determine which subtrees
to pull:

- If the user names a specific package (by prefix directory, remote alias, or
  package name), pull only that entry
- Match casual names: "auth" → the entry whose remote or package contains
  "auth"; resolve ambiguity by asking
- If the user says "all" or does not specify, pull all entries

### 2. Check working tree

```bash
git status
```

Subtree pulls create merge commits; the working tree must be clean. If there
are uncommitted changes, warn the user and ask whether to proceed.

### 3. Pull each subtree

Before pulling, capture the current HEAD so later steps can diff accurately
even if conflict resolution adds extra commits:

```bash
PRE_PULL_HEAD=$(git rev-parse HEAD)
```

For each selected entry, run:

```bash
git subtree pull --prefix <prefix> <remote> <branch> --squash
```

Use the git remote alias from the registry, not a full URL. The `--squash`
flag collapses upstream history into a single merge commit.

If the pull reports "Already up to date", say so and skip the remaining steps
for that entry.

### 4. Resolve conflicts

First check whether any conflicts exist:

```bash
git diff --name-only --diff-filter=U
```

If the output is empty, no conflicts — skip to step 5. If conflicts exist, for
modify/delete conflicts (upstream deleted a file that was locally modified from
a previous squash pull), always accept the upstream version:

- Deletions: `git rm <file>`
- Content conflicts: `git checkout --theirs <file>`

Vendor directories must mirror upstream exactly.

### 5. Clean stale vendor node_modules

Remove any leftover `node_modules/` inside each pulled vendor directory before
running npm install. These are untracked artifacts from previous installs that
can poison npm workspace resolution:

```bash
rm -rf <prefix>/node_modules
```

Run this for every entry that was pulled.

### 6. Re-link workspaces

```bash
npm install
```

This updates workspace symlinks after subtree contents change.

### 7. Cross-reference changelog against UPSTREAM tracking files

For each pulled subtree that has a `CHANGELOG.md` (or `CHANGES.md`, `HISTORY.md`)
in its prefix directory, extract the changelog entries added by the pull:

```bash
git diff $PRE_PULL_HEAD -- <prefix>/CHANGELOG.md
```

Parse the added lines (those starting with `+`) to identify new changelog entries
(bug fixes, features, breaking changes). Compare each entry against the open items
in the corresponding `UPSTREAM-<package>.md` file. If a changelog entry clearly
addresses an open UPSTREAM item (matching keywords, issue references, or described
behavior), flag it as a candidate for auto-resolution with your confidence level:

- **High confidence** — changelog explicitly mentions the bug/feature by name or
  references the same upstream issue URL
- **Medium confidence** — changelog describes a fix/feature in the same area as
  the UPSTREAM entry but doesn't reference it directly
- **Low confidence** — only a vague topical match; mention but don't auto-resolve

For high-confidence matches, proceed to resolve the entry in step 8. For medium
confidence, note the match in the report and let the user decide. Skip low
confidence matches in the resolution step but mention them in the report.

If no changelog file exists in the pulled prefix, skip this step for that entry
and rely solely on the code diff cross-reference in step 8.

### 8. Cross-reference code diff against UPSTREAM tracking files

This is the primary resolution mechanism — do not defer this to the retro.

For each pulled subtree, capture the full sync diff scoped to the vendor
directory (not just the summary):

```bash
git show HEAD -- <prefix>
```

Read the corresponding `UPSTREAM-<package>.md` file (derived from the
registry `package` field). For each open entry in that file, check whether
the sync diff visibly addresses the issue (bug fixed, feature added, API
changed). If an entry appears resolved by the diff:

1. Delete the entry from the tracking file
2. For vendor files: if the section is now empty, restore the
   `_No entries yet._` placeholder
3. Note each deleted entry in your report

If no tracking file exists for a pulled package, skip this step for that entry.

### 8b. Annotate Basic Memory friction entries

For each entry auto-resolved in steps 7–8, check whether a corresponding
Basic Memory entity note exists with an `## Upstream Friction` section. If
Basic Memory MCP tools are available:

1. Call `mcp__basic-memory__search_notes` with the package name
2. If a note exists, call `mcp__basic-memory__read_note` to check for a
   matching friction entry
3. If found, call `mcp__basic-memory__edit_note` with `find_replace` to append
   `_(Resolved by vendor-sync YYYY-MM-DD)_` to the matching entry's line.
   Use `expected_replacements=1`. Always match against the note's exact text.
4. Annotation only — never delete entries, never move them to `### Resolved`.
   The upstream-tracker's workflow 6 handles pruning during its prune pass.

If Basic Memory tools are not available or no matching entry exists, skip
silently. This annotation step is best-effort — vendor-sync works identically
without it, and stale Basic Memory entries are caught by trend review.

### 9. Verify

Check `package.json` scripts and run the most comprehensive available
verification in order of preference:

1. `npm run check && npm test` — if both scripts exist
2. `npm run check` — if only `check` exists
3. `npm test` — if only `test` exists

Show the last 5 lines of output. If verification fails after a pull, report
the errors. The user may need to adapt app code to upstream API changes.

### 10. Report

Summarize the results:

- Which subtrees were pulled and whether there were changes
- Which UPSTREAM entries were resolved (deleted) and why
- Whether verification passed
- Any app-side implications from the upstream changes (API changes, new
  exports, behavioral differences visible in the diff)

## Error handling

- **Registry not found** — tell the user to create `.claude/vendor-registry.json`
  and point them to the format described above. Stop.
- **No changes** — if a pull reports "Already up to date", skip steps 4–8b for
  that entry and note it in the report.
- **npm install failures** — most commonly caused by stale `node_modules/`
  inside vendor directories (step 5). If install fails after cleaning those,
  check for peer dependency conflicts between vendor devDependencies and the
  root project.
- **Verification failures** — report errors. Do not attempt auto-fixes unless
  the failure is clearly a stale artifact (re-run npm install and retry once).
- **Subtree heuristics fail** — if `git subtree pull` errors because git cannot
  identify the subtree prefix correctly, use the explicit merge fallback:
  ```bash
  git fetch <remote> <branch>
  git merge -X subtree=<prefix> --squash <remote>/<branch>
  ```
  Then proceed from step 4 (conflict resolution) normally.
