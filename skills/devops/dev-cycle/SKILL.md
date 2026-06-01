---
name: dev-cycle
description: >
  · Run dev workflow: branch, implement, lint/test, review, docs, PR, merge, release. Triggers: 'start working', 'kick off', 'wrap up', 'ship this', 'ready to ship'. Not for single git ops (use git).
license: MIT
compatibility: "Requires git. Optional forge CLIs by host: gh (GitHub), glab (GitLab), tea (Forgejo/Gitea). Bitbucket uses web UI or REST API. Bare git (no remote) works via format-patch/bundle. Delegates to git, testing, code-review, update-docs, and a brainstorming skill if installed."
metadata:
  source: iuliandita/skills
  date_added: "2026-04-14"
  effort: high
  argument_hint: "[start|finish] [description]"
---

# Dev Cycle: Start-to-Finish Workflow

Orchestrates a unit of work from branch creation to merge and release. Runs in
two modes that typically span different sessions:

- **Start mode**: pull latest, size-detect, create feature branch, brainstorm
  spec for large work or hand off to coding for small work.
- **Finish mode**: verify green, sync docs/versions, review, push, open PR,
  watch CI, merge, cut release when conventions exist.

Each mode delegates to purpose-built skills (`git`, `testing`, `code-review`,
`update-docs`, brainstorming skills) rather than reimplementing them. This
skill is the glue, not the engine.

## When to use

- User signals the start of a unit of work: "start working on X", "let's add Y",
  "kick off the Z refactor", "new feature branch for ..."
- User signals the end of a unit of work: "wrap this up", "ship this", "ready
  to merge", "finish and release", "close out", "finalize"
- Branch is clearly a feature branch and the user is about to stop touching code
- A PR is about to be opened, or CI just went green on one

## When NOT to use

- Heavyweight, planned milestones with phases and formal requirements - use a dedicated milestone/phase skill if your environment has one (e.g., the GSD family `gsd-new-milestone` / `gsd-plan-phase` / `gsd-execute-phase`). Skip this skill entirely for multi-week coordinated initiatives with stakeholders.
- Single git operations (just commit, just push, just cut a release) - use **git**
- Roadmap idea capture without starting code - use **roadmap**
- Pure brainstorming without any start-of-work intent - use a brainstorming skill directly
- Post-merge retrospective or documentation cleanup alone - use **update-docs**
- Full repo audits (security, bugs, slop) - use **full-review** or **deep-audit**

## Related Skills

- **git** - branch creation, commits, push, PR/MR. This skill calls git for the mechanical steps; git knows the forge conventions.
- **testing** - runs lint/type/unit/integration suites. Finish mode invokes it before review.
- **code-review** - final correctness pass before push. Finish mode invokes it after tests are green.
- **update-docs** - sweeps README/CHANGELOG/roadmap/instruction files for drift. Finish mode invokes it to close the doc-gap you've noticed.
- **docker** - when the unit of work touches `Dockerfile`, `docker-compose*.yml`, or container images. Finish mode's version-bump step updates image tags here.
- **kubernetes** - when the work touches K8s manifests, Kustomize overlays, or Helm charts. Version-bump step touches `Chart.yaml` and image references.
- **ci-cd** - when the change modifies pipeline config. The CI-watch step in finish mode depends on working pipelines; if CI itself changed, exercise caution.
- **roadmap** - if the repo has a gitignored ROADMAP.md, finish mode checks off shipped items.

**External dependencies (not in this collection):**
- `superpowers:brainstorming` (optional) - start mode uses it for large work if installed. Falls back to other brainstorming skills (e.g., `gsd-explore`), then inline Socratic questioning. See start.md Step A4 for the full fallback chain.

---

## AI Self-Check

Before declaring start-mode complete:

- [ ] Ran `git status` and `git pull --ff-only` (or equivalent) - working tree is clean and up to date
- [ ] New branch created from the base branch (not from another feature branch); branch name follows repo convention
- [ ] Size classification stated explicitly (small/medium/large) with the signals that drove it
- [ ] For large work: a spec file was produced, or a brainstorming skill was invoked and its output captured
- [ ] Handoff line told the user what skill(s) to reach for next (e.g., "this touches Postgres - use **databases** when modifying migrations")
- [ ] No code was written in start mode unless the task was explicitly small

Before declaring finish-mode complete:

- [ ] `$FORGE` detected from `git remote get-url origin` before any push/PR/merge step
- [ ] All lint/type/test suites green - output inspected, not inferred from "exit code 0". If no toolchain was detectable, user was asked explicitly (not silently skipped)
- [ ] `update-docs` ran over tracked AND gitignored context files (`CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `.claude/`, `.codex/`, `.opencode/`, `.planning/`); findings addressed or deferred with a note. Only tracked files were staged for commit; gitignored edits remain local
- [ ] Current version sourced from primary manifest (or user confirmation) before proposing bumps
- [ ] Version-bump sites checked: Dockerfile, K8s manifests, Helm Chart.yaml/values, package.json/pyproject.toml/Cargo.toml, CHANGELOG
- [ ] `git fetch --tags origin` run before release-signal detection (local-only tag check misses remote history)
- [ ] Release convention detected via 2+ independent signals before attempting a release
- [ ] `code-review` ran on the diff against base, not against HEAD alone
- [ ] PR/MR body includes summary + test plan; no AI attribution trailers
- [ ] CI watched to completion with forge-appropriate verification (e.g., `gh pr view --json statusCheckRollup`, `glab ci status`, manual confirmation for Bitbucket/bare) - not merged on "probably fine"
- [ ] For releases: tag matches the bumped version; CHANGELOG has a new section dated today; release-workflow watch used forge-appropriate exit-status flag (`gh run watch --exit-status` etc.)
- [ ] No `--no-verify`, no `--force-push`, no destructive reset - if blocked, fix the root cause
- [ ] **Current source checked**: dated versions, CLI flags, API names, and support windows are verified against primary docs before repeating them
- [ ] **Hidden state identified**: local config, credentials, caches, contexts, branches, cluster targets, or previous runs are made explicit before acting
- [ ] **Verification is real**: final checks exercise the actual runtime, parser, service, or integration point instead of only linting prose or happy paths
- [ ] **Routing overlap checked**: overlapping skills, trigger terms, and "When NOT to use" boundaries are checked before returning guidance
- [ ] **Spec claims verified**: claims about tool behavior, output contracts, or repo conventions are checked against current docs, scripts, or skill files
- [ ] **Dirty tree protected**: unrelated user changes are identified and left intact
- [ ] **Remote/branch target checked**: base branch, upstream, and PR target are verified before push, merge, or release

---

## Performance

- Run the narrowest meaningful checks (e.g., `--testPathPattern` or `go test ./pkg/...`) during iteration, then the full required gate (`lint + typecheck + test`) once before finishing. Running the full suite on every edit wastes minutes per cycle.
- Keep commits batch-sized by review concern - one logical change per commit - so bisect, revert, and blame stay useful on a branch with many commits.
- Invoke existing project scripts (`Makefile`, `justfile`, `scripts/`) instead of reconstructing ad hoc command sequences; those scripts encode project conventions that ad hoc commands silently skip.

## Best Practices

- Create the feature branch before any implementation edits; untracked local changes that predate the branch are easy to accidentally bundle into the wrong commit.
- Do not force-push, squash, or merge without explicit user intent - each has a different history rewrite consequence that's hard to undo after others have pulled.
- Put concrete verification evidence (test counts, lint output, CI run URL) in PRs and final summaries rather than vague "tests pass" claims; reviewers cannot approve what they cannot verify.


## Workflow

### Step 0: Detect mode

Pick the mode from user intent + repo state. Do not assume.

| Signal | Likely mode |
|--------|-------------|
| "start", "kick off", "new branch for", "let's build", no feature branch yet | **start** |
| "ship", "wrap up", "merge this", "release", "finalize", feature branch active with commits ahead of base | **finish** |
| Branch clean + no explicit signal | ask the user which mode |
| User ran the skill with `start` or `finish` as an argument | honor the argument |

If in doubt, determine the base branch first (`git symbolic-ref --quiet refs/remotes/origin/HEAD | sed 's|refs/remotes/origin/||'`), then:

```bash
git branch --show-current
git log --oneline @{u}.. 2>/dev/null || git log --oneline "$BASE_BRANCH"..HEAD
```

A feature branch with commits ahead of base strongly signals finish mode.

---

## Mode A: Start

Detailed steps live in `references/start.md`. Summary:

### Step A1: Verify clean state and pull

Run these, stopping on any failure:

```bash
git rev-parse --is-inside-work-tree  # must be inside a git repo
git status --porcelain               # must be empty; if not, stash or commit first
git fetch origin --prune
git checkout "$BASE_BRANCH"          # usually main or master
git pull --ff-only                   # refuse non-fast-forward
```

If `BASE_BRANCH` is unknown, read it from `git symbolic-ref refs/remotes/origin/HEAD` or ask the user. Never guess between `main` and `master` - wrong base means a botched branch.

### Step A2: Size-detect

Read `references/size-heuristics.md` for the full table. Fast path:

- **Small** (dive in): typo, rename, dep bump, single-file fix, <20 LOC estimated, user said "quick"/"tiny"
- **Large** (brainstorm): new feature, refactor, new dependency, public API change, multi-module, user said "properly" or "design"
- **Ambiguous**: ask 1-2 disambiguating questions; default to large if uncertain

State the classification and the signals: "Classifying this as **large** because it adds a new public endpoint and touches the auth module."

### Step A3: Create the feature branch

Delegate branch naming and creation to the **git** skill. If it isn't available, use the repo's convention (grep recent branches for pattern) or a sensible default like `type/short-description` (e.g., `feat/oauth-login`, `fix/token-refresh-race`).

```bash
git checkout -b "$BRANCH_NAME"
```

### Step A4: For large work, brainstorm or spec

Try skills in this order, stopping at the first that succeeds:

1. `superpowers:brainstorming` (the superpowers brainstorming skill)
2. Any other installed brainstorming skill (e.g., `brainstorm`, `brainstorming`, `gsd-explore`)
3. **Inline Socratic fallback** - ask the user these questions one at a time, then write a spec file:
   - What's the goal in one sentence?
   - What does success look like (measurable outcome)?
   - What's explicitly out of scope?
   - What are the hardest constraints (performance, compatibility, deadlines)?
   - What could go wrong or surprise us?
   - Any existing code/skills/patterns to reuse?

**Headless/non-interactive contexts** (Claude Code `--bare`, Codex `exec`, Cursor Automations) cannot prompt the user. If a brainstorming skill is unavailable AND the environment is non-interactive, write a minimal `SPEC.md` with Goal/Constraints/Risks populated from available context (issue body, branch name, git log), mark unknowns with `TODO:` so they're easy to find later, and continue to handoff. Do not block waiting for answers that can't come.

Write the spec to `SPEC.md` at the repo root (or `specs/<branch-name>.md` if the repo already has a `specs/` dir). Commit it as the first commit on the new branch so the start point is recorded. Spec file format in `references/start.md`.

### Step A5: Hand off

End start mode with a clear handoff:

- State the branch name
- State the classification
- Point the user at skills that fit the domain ("touches Dockerfile - use **docker** when editing", "adds K8s manifests - use **kubernetes**")
- Remind the user to invoke **dev-cycle** in finish mode when ready to ship

Do not continue into implementation - that's the user's next session.

---

## Mode B: Finish

Detailed steps live in `references/finish.md`. Summary:

### Step B1: Pre-close audit and forge detection

First, detect the forge - every later step (push, PR, CI watch, merge, release) dispatches on it. See `references/finish.md` Step B1 for the full detection block. Short version: read `git remote get-url origin`, pattern-match on host, set `$FORGE` to one of `github | gitlab | forgejo | bitbucket | unknown | bare`. Forgejo and Gitea share a CLI (`tea`) and are collapsed into the single value `forgejo`.

Then sanity-check the branch:

```bash
# Staged or modified files block closing. Untracked files are fine (not part of HEAD).
git diff --cached --stat; git diff --stat
git log --oneline "$BASE_BRANCH"..HEAD   # commits exist on this branch
git diff "$BASE_BRANCH"..HEAD --stat     # scope sanity check
```

If the branch has no commits or the diff is empty, stop - there's nothing to ship.

### Step B2: Run lint, type, and tests

Delegate to the **testing** skill with instruction "run lint, type checks, and tests; surface any failures".

If the testing skill isn't installed, detect the toolchain. Check in order - first match wins. If no language manifest matches, **continue** to task runners and custom scripts; don't give up:

- **Language manifests**: `package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `Gemfile`, `composer.json`, `pom.xml`, `build.gradle*`, `mix.exs`, `Package.swift`
- **Task runners**: `Makefile` with `lint`/`test`/`check` targets, `justfile`, `Taskfile.yml`
- **Custom scripts**: executable files in `scripts/` or `bin/` whose names match `lint|test|check|ci|validate|verify`
- **Documented commands**: grep `README.md` / `CONTRIBUTING.md` for script invocations

Full detection table and the quick-scan commands live in `references/finish.md`.

**If nothing detectable**: stop and ask the user how to verify. Do NOT silently skip - a finish-mode report with no verification run is a false green. Offer: (a) run a command they'll provide, (b) skip with explicit acknowledgement, (c) abort.

Inspect the actual output. "Exit 0" is not verification - tests that didn't run also return 0. Confirm the suite was exercised.

**If anything is red, stop.** Do not proceed. Fix the root cause (or ask the user to), then re-run. Never use `--no-verify` or skip failing tests.

### Step B3: Sync docs and versions

Docs and versions get left behind. Address in two parts:

**Part 1 - Delegate to `update-docs`** for README, CHANGELOG, roadmap, instruction files, companion-file drift. Invoke as a review-and-fix pass, not read-only.

**Important: refresh gitignored docs too**, not just tracked ones. Files like `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `.claude/`, `.codex/`, `.opencode/`, and private `.planning/` directories are commonly gitignored but are still primary context for the developer and for future AI sessions. Stale gitignored docs cause just as much confusion as stale tracked ones. Only the tracked subset gets staged for commit; gitignored updates stay local but still get made. Ask `update-docs` to sweep both sets.

**Part 2 - Version-bump sites**. First read the current version from the primary source (see `references/version-bump-sites.md` for the detection script - it checks `package.json`, `pyproject.toml`, `Cargo.toml`, then falls back to the latest semver tag). If no primary source exists, ask the user what the current version is before proceeding.

Then find and update version strings. Common sites:

- `Dockerfile` (LABEL version, image tags, default ARGs)
- `docker-compose*.yml` (image tags)
- `k8s/**/*.yaml` and `kustomize/**/*.yaml` (`image:` fields)
- `helm/**/Chart.yaml` (`version` and `appVersion`) and `values.yaml` (image tag)
- `package.json` (`version`)
- `pyproject.toml` (`version` under `[project]` or `[tool.poetry]`)
- `Cargo.toml` (`version`)
- `CHANGELOG.md` (new section with today's date)
- Version badges in `README.md`

Propose a diff. Do not silently edit. The user confirms the version bump scope.

**Part 3 - Tests reflect new version**. If tests reference version strings (snapshots, integration tests pulling images by tag, fixtures hardcoding versions), update them and rerun the suite.

### Step B4: Final code review

Delegate to the **code-review** skill with the diff scope: `BASE_BRANCH..HEAD`. The review covers the full change, not just the last commit.

If the review surfaces blocking issues, fix them and loop back to Step B2 (tests may now be affected).

### Step B5: Push and open PR

Delegate to the **git** skill - it handles forge routing. If unavailable, dispatch on `$FORGE` from Step B1. Full per-forge commands in `references/finish.md`.

| `$FORGE` | Push + PR |
|----------|-----------|
| `github` | `git push -u origin <branch>` + `gh pr create` |
| `gitlab` | same push + `glab mr create --target-branch` |
| `forgejo` | same push + `tea pulls create --base --head` |
| `bitbucket` | push + announce web-UI URL (no official CLI) |
| `unknown` (self-hosted) | push + announce branch URL; ask user what forge this is |
| `bare` (no remote) | `git format-patch` or `git bundle` - share file with reviewer |

No AI attribution trailers. No "Generated with Claude Code" lines. Strip them from any commit-helper template before committing.

### Step B6: Watch CI

Dispatch on `$FORGE`. Every tool has a watch trap - default exit code may not reflect failure.

| `$FORGE` | Command | Trap |
|----------|---------|------|
| `github` | `gh pr checks --watch --fail-fast` then verify via `gh pr view --json statusCheckRollup` | exits 0/1/8; treat anything non-zero as not-ready |
| `gitlab` | `glab ci status --live` then `glab mr view --output json` | `--live` doesn't always exit non-zero on failure; verify explicitly |
| `forgejo` | `tea pulls status <pr>` or `tea actions list` (varies by instance) | Actions API is newer; fall back to web UI if command missing |
| `bitbucket` | No CLI - watch web UI or poll Pipelines REST API | Manual confirmation before merge |
| `unknown` | Ask user which CI is wired (Jenkins, Drone, Woodpecker, Buildkite, Teamcity) and point them at the URL | Assume nothing |
| `bare` | No remote CI; rely on B2 local output | N/A |

If CI fails, fix the root cause - don't retry hoping for flakiness to resolve. If genuinely flaky (rerunning the identical commit passes), rerun and note it in the PR body.

### Step B7: Merge

Once CI is green, dispatch on `$FORGE`:

| `$FORGE` | Merge command | Delete-branch flag |
|----------|---------------|--------------------|
| `github` | `gh pr merge --squash` / `--rebase` / `--merge` | `--delete-branch` |
| `gitlab` | `glab mr merge --squash` / `--rebase` / (default = merge commit) | `--remove-source-branch` |
| `forgejo` | `tea pulls merge <pr> --style squash\|merge\|rebase\|rebase-merge` | Delete via web UI or follow-up `git push origin --delete <branch>` |
| `bitbucket` | Web UI or REST API with `"merge_strategy": "squash"` | `"close_source_branch": true` |
| `unknown`/`bare` | Local: `git merge --no-ff` (or `--ff-only` after rebase) on base, push, `git branch -d` | N/A |

Check the repo's merge convention before picking a style. If multiple are allowed, match recent merge history: `git log --merges --oneline "$BASE_BRANCH" | head -5`.

### Step B8: Release (conditional)

**First, `git fetch --tags origin` if a remote exists** - local-only tag checks miss remote release history and cause false-negative skips. Then:

**Auto-skip unless at least 2 independent release signals are present.** A single stale tag or lonely CHANGELOG is not a convention. Signal catalog and detection commands live in `references/finish.md` Step B8. Summary:

- Semver tags (`git tag -l 'v[0-9]*'` after `git fetch --tags`)
- CHANGELOG / CHANGES / HISTORY file
- Release workflow file (GitHub Actions, GitLab CI, Forgejo/Gitea Actions, Woodpecker, Drone)
- Forge-native release history (`gh`/`glab`/`tea` release list)
- Published package (non-private `package.json`, `[project]` in `pyproject.toml`, `[package]` in `Cargo.toml`)

**Hard skips**: `package.json` has `"private": true`, or `$FORGE=bare` with no local-tag-only intent (ask user).

If release-capable:

1. Determine bump type (breaking -> major, feature -> minor, fix -> patch). Ask if unclear.
2. Guard against existing tag via `git rev-parse --verify --quiet "refs/tags/v$NEW_VERSION"` (note: `git tag -l` always exits 0 so it cannot be used as a guard).
3. Tag the merge commit on `$BASE_BRANCH` and push.
4. Create a forge-native release object (`gh release create`, `glab release create`, `tea releases create`) - Bitbucket and bare have no platform release object; the tag itself IS the release.
5. Watch the release workflow with the forge-appropriate exit-status flag. **Every forge has a default-exit trap** (see Rule 6 and `references/finish.md` for per-forge commands).

Full procedures, extract-changelog function, and per-forge release-watch commands in `references/finish.md`.

---

## Concrete end-to-end finish on GitHub

Branch `feat/oauth-login` on a Node repo with `gh` available, Dockerfile, Helm chart, `"version": "1.4.2"` in `package.json`, CHANGELOG present, GitHub Actions release workflow.

```
B1  git remote get-url origin  -> github.com  -> FORGE=github, FORGE_CLI=gh
    git log main..HEAD          -> 6 commits; diff 340 lines across 12 files
B2  bun run lint && bun run typecheck && bun test  -> all green, 184 tests
B3  update-docs: README badges, CHANGELOG [1.5.0] section dated 2026-04-16
    Bump: package.json 1.4.2 -> 1.5.0, Dockerfile LABEL, helm/Chart.yaml appVersion, values.yaml image tag
B4  code-review on main..HEAD   -> 2 nits addressed, re-run tests green
B5  git push -u origin feat/oauth-login
    gh pr create --base main --title "feat(auth): OAuth login" --body-file .github/pr-body.md
B6  gh pr checks --watch --fail-fast     # then:
    gh pr view --json statusCheckRollup --jq '.statusCheckRollup[].conclusion' | grep -v SUCCESS && exit 1
B7  gh pr merge --squash --delete-branch
B8  git fetch --tags origin
    git rev-parse --verify --quiet refs/tags/v1.5.0 || git tag -a v1.5.0 -m "v1.5.0" && git push origin v1.5.0
    gh release create v1.5.0 --title v1.5.0 --notes-file <(extract_changelog 1.5.0)
    RUN_ID=$(gh run list --limit 1 --json databaseId --jq '.[0].databaseId')
    gh run watch "$RUN_ID" --exit-status
```

GitLab substitutes `glab mr create`, `glab ci status --live`, `glab mr merge --squash --remove-source-branch`, `glab release create`. Forgejo substitutes `tea pulls create`, `tea pulls merge --style squash`, `tea releases create`. Bitbucket and bare paths skip B5-B8 CLI steps and use web UI / `format-patch` respectively.

---

## Output Contract

See `skills/_shared/output-contract.md` for the full contract.

- **Skill name:** DEV-CYCLE
- **Deliverable bucket:** `audits`
- **Mode:** conditional. When invoked to **analyze, review, audit, or improve** existing repo content, emit the full contract - boxed inline header, body summary inline plus per-finding detail in the deliverable file, boxed conclusion, conclusion table - and write the deliverable to `docs/local/audits/dev-cycle/<YYYY-MM-DD>-<slug>.md`. When invoked to **answer a question, teach a concept, build a new artifact, or generate content**, respond freely without the contract.
- **Severity scale:** `P0 | P1 | P2 | P3 | info` (see shared contract; only used in audit/review mode).

## Rules

1. **Read before edit.** Always read files you're about to modify in the current session. No exceptions.
2. **Never force-push, never `--no-verify`, never skip failing tests.** If a hook or test is in the way, fix the underlying issue. Destructive shortcuts are a red flag, not a convenience.
3. **Delegate, don't reimplement.** `git`, `testing`, `code-review`, `update-docs`, and brainstorming skills know their domains better than this skill does. Call them.
4. **No AI attribution in git artifacts.** No `Co-Authored-By` trailers, no "Generated with Claude Code" lines, no robot emoji in commit messages, PR titles/bodies, or release notes. Strip from any commit-helper templates before committing.
5. **Confirm before release.** Release cutting is a forge-visible action. Announce the version, bump sites, and plan to the user; get explicit confirmation before pushing the tag.
6. **Inspect CI output, don't infer it.** Every forge's watch command has a default-exit trap: `gh run watch` exits 0 on workflow failure without `--exit-status`; `gh pr checks --watch` returns when done, not only when green; `glab ci status --live` prints but doesn't always exit non-zero on pipeline failure. After any watch, verify with an explicit status query (`gh pr view --json statusCheckRollup`, `glab ci status --output json`, or web-UI confirmation for forges without a CLI). Confirm every check actually passed.
7. **Release detection is conservative.** If no convention signals are present, skip. A missing `CHANGELOG.md` plus no tags means this isn't a release-cut situation - don't create one.
8. **Don't bundle unrelated work.** If mid-finish you notice a bug outside the branch's scope, file it (roadmap skill or an issue) - don't sneak it into the PR.
9. **Plain ASCII only.** No em-dashes, no `--` substitutes, no curly quotes, no decorative emoji. Functional status markers (`[OK]`, `[FAIL]`, severity emoji in reports from delegated skills) are fine.
10. **Mode boundaries are sacred.** Start mode ends with a handoff, not implementation. Finish mode starts with verification, not committing new code. Don't blur them.

## Reference Files

- `references/start.md` - detailed start-mode workflow, branch naming conventions, spec file template, brainstorming fallback chain (including headless-mode behavior)
- `references/finish.md` - detailed finish-mode workflow with per-forge commands (GitHub/GitLab/Forgejo/Gitea/Bitbucket) and bare-git paths (format-patch, bundle, local merge). Covers forge detection, toolchain detection with custom-script fallback, CI watch traps, release cutting, and rollback
- `references/size-heuristics.md` - complete size-classification table with concrete signals, edge cases, and the ambiguity-resolution questions
- `references/version-bump-sites.md` - grep patterns and locations for version strings across common ecosystems (Docker, K8s, Helm, package managers)
