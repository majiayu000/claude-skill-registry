---
name: atomic-issues-prs
description: "Publish a change-set as atomic GitHub issues/PRs — one issue/PR per logical change, never bundled. Use when the user says \"open a PR per change\", \"atomic PRs\", \"push issues and prs atomically\", \"individual PR for each change\", or wants a change-set delivered as separate PRs/issues. Asks per run which objects to create (PR-only vs issue+linked-PR). Detects whether the canonical repo is directly pushable via `gh`; if not, pushes branches to the fork and opens PRs targeting upstream with `--head <fork-owner>:<branch>`. Requires `gh` auth; refuses force-push and direct push to protected branches without explicit authorization."
metadata:
  short-description: Atomic one-PR-per-change publisher with fork fallback
---

# Atomic Issues and PRs

Publish a change-set as atomic GitHub objects: one issue/PR per logical change, never bundled.
The layer above atomic-commit-and-push — it opens the PRs (and optionally issues) that skill never touches.

## Phase 0 — Preflight & canonical-repo resolution

Run `gh auth status`. If unauthenticated, stop and ask the user to run `gh auth login`.

Resolve the canonical (upstream) slug **explicitly before any permission check** — `gh repo view`'s
default inspects the *current* repo, which is the fork in a fork clone.

- Read remotes: `git remote -v`. Pick the contribution target: `upstream` if present, else `origin`.
- Detect a fork relationship: `gh repo view <slug> --json nameWithOwner,parent,defaultBranchRef`.
  A non-null `parent` means `<slug>` is itself a fork, so the canonical slug is `parent.nameWithOwner`.
- Query permission on the canonical slug: `gh repo view <canonical-slug> --json viewerPermission`.
  `viewerPermission` ∈ {ADMIN, MAINTAIN, WRITE} ⇒ **direct mode**; otherwise ⇒ **fork mode**.
- Record the canonical default base branch from `defaultBranchRef`.

## Phase 1 — Decompose & commit atomically

Group working-tree changes into atomic units by mechanism/file boundary — one concern per unit.
Never bundle unrelated changes.

Commit the **whole** set into N atomic commits first, running the repo-native type-checker and linter
before each commit. This is the patch-isolation mechanism: each unit becomes one self-contained commit,
so per-unit branches come from **cherry-pick** — never from re-staging a dirty tree, which would let
later units swallow earlier diffs. Present the unit→commit list to the user.

## Phase 2 — Choose objects (ask the user)

Ask what to create per unit:

- **PR-only** — one branch + one PR per unit.
- **Issue + linked PR** — a tracking issue per unit, plus a PR whose body says `Closes #N`.

One answer applies to the run; honor a per-unit override if the user volunteers one.

## Phase 3 — Resolve push URL (once)

Push by **URL**, never by remote name — this avoids undefined targets (a canonical slug from `parent`
has no local remote) and remote-name collisions / local-config mutation. With `gh` authenticated, the
git credential helper authorizes HTTPS pushes.

- **Direct mode**: push URL = `https://github.com/<canonical-slug>`.
- **Fork mode**: fork owner = authenticated login (`gh api user --jq .login`); fork slug = `<login>/<repo>`.
  If the fork does not exist, create it (`gh repo fork <canonical-slug> --clone=false`) — ask the user
  first, it is a write action. Push URL = `https://github.com/<fork-slug>`.

## Phase 4 — Per-unit publish loop

Default contract: **units are independent** — each branches off the canonical base and merges alone.
Determine dependency order in Phase 1; if no unit depends on another, every PR bases on `<default>`.
For each unit, in dependency order:

1. `git branch <branch> <parent-ref>` then `git cherry-pick <unit-commit>` onto it.
   - **Independent unit**: `<parent-ref>` = `<canonical-default-base>`; PR bases on `<default>`.
   - **Dependent unit (direct mode only)**: `<parent-ref>` = the prerequisite unit's already-pushed
     branch; PR bases on that branch (a stacked PR). Cherry-pick only this unit's commit — the
     prerequisite is already present via the parent branch, so no prerequisite is lost.
   - **Dependent unit in fork mode**: cross-fork stacking can't be expressed (a fork PR's base must be a
     branch in the canonical repo, not the fork). Stop and ask the user to land the prerequisite PR
     first, then re-run for the dependent unit — do not silently flatten it onto `<default>`.
2. `git push <push-url> <branch>:refs/heads/<branch>` (same form both modes — only the URL differs).
3. If issues were chosen: `gh issue create --repo <canonical-slug> --title "<summary>" --body-file <tmp>` → capture `#N`.
4. `gh pr create --repo <canonical-slug>` — direct mode: `--base <parent-ref> --head <branch>`;
   fork mode: `--base <default> --head <fork-owner>:<branch>`. Include `Closes #N` in the body when an issue was filed.
5. Emit the issue/PR URLs; move to the next unit.

## Constraints (hard)

- Never `--force` or `--force-with-lease` without explicit user authorization.
- Never push directly to protected branches (`main`, `master`, `release/*`) — branches only.
- One GitHub object per logical change; bundling is refused.
- Creating a fork is a write action — ask the user before `gh repo fork`.
