---
name: git
description: >
  · Handle git branches, commits, remotes, conflicts, hooks, signing, releases, PR/MR workflows. Triggers: 'git', 'commit', 'branch', 'merge', 'rebase', 'tag', 'push', 'PR', 'MR', 'gh', 'glab'.
license: MIT
compatibility: "Requires git. Optional: gh (GitHub CLI), glab (GitLab CLI), fj (Forgejo CLI)"
metadata:
  source: iuliandita/skills
  date_added: "2026-03-24"
  effort: high
  argument_hint: "[git-task-or-target]"
---

# Git: Multi-Forge Production Workflow

Perform git operations, manage branches, handle multi-remote setups, create PRs/MRs,
cut releases, and maintain audit-grade change history across GitHub, GitLab, and Forgejo.
The goal is clean, signed, traceable history that satisfies both engineering standards and
compliance requirements (PCI-DSS 4.0).

**Target versions** (May 2026):
- **git**: 2.53.x (current stable). Git 3.0 expected late 2026 (reftable default, SHA-256 default)
- **GitHub CLI (`gh`)**: 2.91.0
- **GitLab CLI (`glab`)**: 1.90.x
- **Forgejo CLI (`fj`)**: 0.5.0 (latest verified May 2026, released 2026-04-16; the project moves fast - verify the current release at `codeberg.org/forgejo-contrib/forgejo-cli`). Rust-written, official community CLI. Covers PRs (incl. AGit), issues, repos, releases, tags, actions.
- **Forgejo**: v15.0 line current at May 2026 recheck; verify the stable branch before upgrade advice. Critical RCE (CVE-2025-68937) patched in v13.0.2+.
- **prek**: 0.3.x (Rust, recommended) or **pre-commit**: 4.6.0 (Python, largest ecosystem)
- **git-filter-repo**: 2.47.x
- **gitleaks**: 8.30.x (secret scanning)
- **cosign**: 3.x (Sigstore, for tag/release signing context)

This skill covers five domains depending on context:
- **Operations** - commits, branches, merges, rebases, stashing, bisect, reflog, recovery
- **Remotes & forges** - multi-remote setups, GitHub/GitLab/Forgejo differences, mirroring
- **PR/MR workflow** - feature branches, review flow, merge strategies, release cutting
- **Security** - commit signing, credential management, hooks, secret scanning, history scrubbing
- **Compliance** - PCI-DSS 4.0 change management, audit trails, branch protection as controls

## When to use

- Creating commits (message style, signing, authorship)
- Managing branches (creation, cleanup, protection, naming)
- Working with remotes (push, pull, fetch, multi-remote sync)
- Creating PRs/MRs (title, description, review process, merge strategy)
- Cutting releases (tagging, changelog, GitHub/Forgejo releases)
- Resolving merge conflicts or rebasing
- Recovering from mistakes (reflog, reset, revert, cherry-pick, bisect)
- Configuring git (aliases, hooks, attributes, credentials, signing)
- Scrubbing sensitive data from history (filter-repo)
- Setting up branch protection rules or rulesets
- Multi-forge workflows (mirroring, token management, SSH keys)
- PCI-DSS change management evidence

## When NOT to use

- CI/CD pipeline design - use **ci-cd**; this skill handles git operations *within* pipelines, not pipeline architecture
- PR/MR code review - use **code-review**; this skill creates PRs, doesn't review code in them
- Full application security audit - use **security-audit**; this skill covers secrets *in git history* and git-specific security, not application-level vulnerability assessment
- Docker image tagging strategy - use **docker**; this skill handles git tags, not container tags
- Post-session or post-merge documentation sweeps (README, changelog, runbooks) - use **update-docs**

---

## AI Self-Check

AI tools consistently produce the same git mistakes. **Before performing any git operation,
verify against this list:**

- [ ] **Read before rewrite.** Never `Edit`/`Write` files without `Read`ing them first. Never `git commit` without checking `git status` + `git diff`.
- [ ] **No destructive ops without confirmation.** `reset --hard`, `push --force`, `branch -D`, `clean -fd`, `checkout .` - all require explicit user approval. Propose safer alternatives first (`--force-with-lease`, `revert`, new branch).
- [ ] **Authorship correct.** Check the project's instruction file for author overrides. Many setups have a local git config that's wrong for the remote (e.g., Forgejo identity vs GitHub identity).
- [ ] **Commit message format.** Follow the project's convention (check recent `git log`). Default: conventional commits (`type(scope): description`).
- [ ] **No secrets in commits.** Check `git diff --cached` for API keys, tokens, passwords, `.env` files, private keys before committing. If found, unstage immediately.
- [ ] **No AI attribution in commits.** Never add `Co-Authored-By` lines or any mention of AI tools in commits. No exceptions unless the project explicitly requires it.
- [ ] **Instruction-file policy respected.** Follow the repo's policy for `AGENTS.md` or other instruction files. Never commit local agent state directories like `.claude/`, and never mention local-only tooling files in commit messages.
- [ ] **No tool-specific paths in commits.** `.claude/`, `.cursor/`, `.superpowers/`, `.worktrees/`, `docs/local/`, `PLAN.md`, `SECURITY-AUDIT.md` are local artifacts. Verify `.gitignore` covers AI tooling artifacts BEFORE staging (.claude/, .cursor/, .codex/, PLAN.md)
- [ ] **Branch target correct.** Verify you're on the right branch before committing. Verify the PR/MR targets the right base branch.
- [ ] **Requester authorized for admin changes.** In shared chats, do not commit or push infrastructure, Kubernetes, secrets, firewall, or other admin changes from a participant who is not authorized to approve them. Stop and ask the authorized owner first.
- [ ] **Remote target correct.** Multi-remote setups exist. Check which remote(s) to push to. Some projects push to multiple remotes (e.g., Forgejo + GitHub).
- [ ] **Signing configured.** If the project requires signed commits, verify signing works before committing (`git log --show-signature -1`).
- [ ] **No `--no-verify`.** Never skip pre-commit hooks unless the user explicitly asks. Hooks exist for a reason - fix the underlying issue instead.
- [ ] **No interactive flags.** Never use `-i` (interactive) flags (`git rebase -i`, `git add -i`) in automated contexts - they require TTY input.
- [ ] **Tags pushed separately.** `git push` doesn't push tags by default. Always `git push --tags` or `git push origin <tag>` explicitly.
- [ ] **Feature branch up to date.** Before creating a PR/MR, rebase onto the latest base branch to avoid merge conflicts.
- [ ] **Lock files regenerated after conflict resolution.** After resolving conflicts in dependency files (`package.json`, `Cargo.toml`, `go.mod`, `pyproject.toml`), re-run the package manager to regenerate the lock file. Never manually merge lock files. Then regenerate: `npm install`, `yarn install`, `go mod tidy`, or `cargo generate-lockfile`.
- [ ] **Force-push safety.** If force-push is needed, always use `--force-with-lease` (refuses if remote has unfetched commits). Plain `--force` requires explicit user approval and team coordination.
- [ ] **Version info dated.** When citing tool versions, include a date so readers know when to re-check. Stale version numbers cause silent breakage.
- [ ] **Forge-CLI subcommands verified.** Before scripting `fj`/`gh`/`glab`/`tea` commands in a runbook, hooks, or CI, confirm the subcommand and flags exist on the target version (`<cli> <cmd> --help`). These CLIs add, rename, and remove subcommands across minor versions; docs lag behind the binary.
- [ ] **Current source checked**: dated versions, CLI flags, API names, and support windows are verified against primary docs before repeating them
- [ ] **Hidden state identified**: local config, credentials, caches, contexts, branches, cluster targets, or previous runs are made explicit before acting
- [ ] **Verification is real**: final checks exercise the actual runtime, parser, service, or integration point instead of only linting prose or happy paths
- [ ] **Routing overlap checked**: overlapping skills, trigger terms, and "When NOT to use" boundaries are checked before returning guidance
- [ ] **Spec claims verified**: claims about tool behavior, output contracts, or repo conventions are checked against current docs, scripts, or skill files
- [ ] **Ref safety checked**: branch, remote, upstream, and worktree path are verified before history edits
- [ ] **Recovery path known**: reflog, backup branch, or bundle exists before destructive history operations

---

## Performance

- Use path-limited `git log`, `git diff`, and `git grep` before whole-history scans.
- Fetch only needed remotes/branches in large repos when full prune is unnecessary.
- Keep commits small enough for review and bisect, but not so small that they split one behavior across many commits.


---

## Best Practices

- Prefer revert over history rewrite on shared branches.
- Use signed commits/tags where the project or release process requires provenance.
- Never run cleanup commands that delete branches, tags, or ignored files without showing the target set first.


## Workflow

### Step 1: Identify the forge and project context

| Signal | Forge |
|--------|-------|
| `.github/` directory, `gh` CLI | GitHub |
| `.gitlab-ci.yml`, `glab` CLI, user says "work" | GitLab |
| `.forgejo/` directory, user says "home" | Forgejo |
| Multiple remotes in `git remote -v` | Multi-forge |

Read the project's instruction file (`AGENTS.md` or equivalent) for:
- **Commit conventions** (message format, scope list, authorship overrides)
- **Branch strategy** (trunk-based, feature branches, release branches)
- **Remote setup** (which remotes exist, which to push to, SSH keys)
- **Release process** (version bump files, tag format, changelog)
- **Signing requirements** (GPG, SSH, or unsigned)
- **Content restrictions** (domains, tool names, paths that must not appear in git history)

### Step 2: Determine the operation

- **"Commit this" / "save my work"** -> Commit workflow (Step 3a)
- **"Create a PR/MR"** -> PR/MR workflow (Step 3b)
- **"Cut a release"** -> Release workflow (Step 3c)
- **"Fix this mess" / "undo" / "recover"** -> Recovery operations (Step 3d)
- **"Pull failed" / "branches diverged"** -> Diverged branch resolution (Step 3e)
- **"Pull/update all repos under a directory"** -> Bulk repo update workflow (Step 3f)
- **"Set up signing" / "configure git"** -> Configuration (references)
- **"Clean up history" / "scrub secrets"** -> History rewriting (references)
- **"Set up branch protection"** -> Protection rules (references)

### Step 3a: Commit workflow

1. **Check state**: `git status` (never `-uall` on large repos) + `git diff` (staged and unstaged)
2. **Stage selectively**: `git add <specific files>` - never `git add -A` or `git add .` without reviewing what's included. Check for secrets, binaries, generated files, AI tooling artifacts.
3. **Check the diff**: `git diff --cached` - read what you're about to commit. Look for debug code, TODO comments, accidental changes to unrelated files.
4. **Write the message**: follow the project's convention. Default format:

```
type(scope): concise description

Optional body explaining *why*, not *what*.
```

Select `type` from: `feat`, `fix`, `docs`, `refactor`, `chore`, `ci`, `build`, `revert`.
Extended types (use if the project convention allows): `test`, `perf`, `security`.
**Always check the project's instruction file and recent `git log` first** - the project may have a
different type list or naming convention. Project instructions override these defaults.

**Scopes** are strongly recommended but not blindly enforced. A scope adds context that makes
`git log --oneline` scannable: `fix(auth): token expiry` vs `fix: token expiry`. Use the
component, module, or area name. Skip the scope only when the change is truly cross-cutting
or the project doesn't use scopes.

**Breaking changes**: append `!` after the type/scope: `feat(api)!: drop v1 endpoints`.
For detailed breakage notes, add `BREAKING CHANGE:` in the commit body footer.

Message guidelines:
- Imperative mood ("add feature", not "added feature" or "adds feature")
- First line under 72 characters
- Body wrapped at 72 characters
- Explain *why* the change was made, not *what* changed (the diff shows *what*)
- Reference issue/ticket numbers where applicable
- **Casual, human-sounding tone.** Like a competent human wrote it, not an AI.
  Good: `fix(caddy): self-healing volume permissions`, `feat(auth): add OIDC login`
  Bad: "fix stuff", "wip", "update files", "enhance the robustness of the authentication module"
- **Plain ASCII only.** No em-dashes, curly quotes, ligatures, or fancy punctuation in commit messages.
- **Never mention local instruction files or AI tooling** in commit messages or bodies.
  If you're updating local-only instruction files alongside code changes, don't include them in the commit.
- **Never add `Co-Authored-By` or AI attribution** lines. No `Signed-off-by: AI`. No mentions
  of specific AI tools in the commit metadata.

5. **Commit**: with any required authorship overrides and signing flags from project config.
6. **Verify**: `git log -1 --format="%h %s%n  Author: %an <%ae>%n  Committer: %cn <%ce>"` - check authorship is correct before pushing.

### Step 3b: PR/MR workflow

**First check**: does the project use feature branches? Read the project instruction file. Some projects
(especially solo projects) work directly on `main` by preference. The default here assumes
collaborative development with review. Adapt to the project's actual workflow.

Read `references/forge-workflows.md` for forge-specific PR/MR creation
patterns (GitHub `gh pr create`, GitLab `glab mr create`, Forgejo web UI or API).

General flow:
1. **Create feature branch**: `git checkout -b type/short-description` (e.g., `feat/user-search`, `fix/auth-bypass`). Keep branch names lowercase, hyphenated, prefixed with type.
2. **Make changes**: commit early, commit often. Each commit should be a logical unit.
3. **Rebase onto base**: `git fetch origin && git rebase origin/main` (or whatever the base branch is). Resolve conflicts: look for `<<<<<<<`, `=======`, `>>>>>>>` markers, keep the correct content from both sides (often both additions belong), then `git add` and `git rebase --continue`. After resolving conflicts in dependency files (`package.json`, `Cargo.toml`, `go.mod`, etc.), re-run the package manager to regenerate the lock file. Never merge the base into the feature branch. For merge strategy guidance, see `references/forge-workflows.md`.

   **Dependency file conflicts** (`package.json`, `go.mod`, `pyproject.toml`): keep additions from both branches; when the same dependency has conflicting version pins, take the higher compatible version conservatively and validate. Never hand-edit the lock file - always regenerate it by running the package manager (`npm install`, `go mod tidy`, `uv sync`, etc.) after resolving the manifest conflict. Do not use `--ours` or `--theirs` for dependency manifest conflicts - these silently drop one branch's additions.
4. **Push**: `git push -u origin feat/short-description`. Then verify the remote actually
   advanced: compare `git rev-parse HEAD` with the forge PR/MR head SHA (`gh pr view ...`,
   `glab mr view ...`, or forge API). Do not rely on a terse or aliased push wrapper alone.
   If upstream tracking is missing or odd, push the exact refspec explicitly and re-check the
   PR/MR head before claiming the update landed.
5. **Create PR/MR**: with a clear title (under 70 chars), body with summary + test plan.
6. **Review cycle**: address feedback, rebase and force-push with `--force-with-lease` (never plain `--force` on shared branches). Squash fixup commits before pushing.
7. **Merge**: squash-merge for clean history (default), or rebase-merge if commit history is meaningful.
8. **Cleanup**: delete the remote branch after merge. `git branch -d feat/short-description` locally.

Branch naming convention:
- `feat/description` - new features
- `fix/description` - bug fixes
- `refactor/description` - code restructuring
- `chore/description` - maintenance, deps, config
- `docs/description` - documentation only
- `ci/description` - CI/CD changes
- `security/description` - security fixes (consider if this should be a private advisory instead)

### Step 3c: Release workflow

Read `references/forge-workflows.md` for forge-specific release creation.

**Versioning scheme**: semver `vMAJOR.MINOR.PATCH` with optional pre-release suffixes.

| Version | When | CI behavior |
|---------|------|-------------|
| `v0.12.0-alpha.1` | Start of new minor version, iterating on new features | Tag + release (marked pre-release). Image build optional per project. |
| `v0.12.0-alpha.2` | Continued iteration, not stable yet | Same as above. |
| `v0.12.0` | Features stable, ready for production | Full release: tag + release + image build + deploy. |
| `v0.12.1` | Patch fix on stable release | Full release. |

**Alpha workflow**:
- When starting work on a new minor version, tag `vX.Y.0-alpha.1`
- Increment the alpha number (`-alpha.2`, `-alpha.3`) as you iterate
- When stable, drop the `-alpha` suffix and release `vX.Y.0`
- Alpha tags still get GitHub/Forgejo releases (marked `--prerelease`) so CI can optionally build images
- The project instruction file defines whether alpha tags trigger image builds or not

General flow:
1. **Version bump**: update all version files (check the project instruction file for the list - every project is different).
2. **Commit**: `chore: bump version to X.Y.Z` (or `chore: bump version to X.Y.Z-alpha.N`)
3. **Tag**: `git tag -a vX.Y.Z -m "vX.Y.Z"` (annotated tags, not lightweight).
4. **Push**: push commits AND tags. `git push origin main && git push origin vX.Y.Z`. If multi-remote, push to all.
5. **Create release**: GitHub (`gh release create`), GitLab (`glab release create`), or Forgejo (API/web).
   For alpha/pre-release: `gh release create vX.Y.Z-alpha.N --prerelease --title "vX.Y.Z-alpha.N"`
6. **Verify**: check that CI/CD picked up the tag and started the release pipeline.

**Changelog generation**: conventional commits feed tools like `git-cliff`, `release-please`,
or `conventional-changelog` to auto-generate changelogs from commit history. GitHub's
`gh release create --generate-notes` also works (uses PR titles since last tag). The `!`
breaking change marker and consistent scopes make these tools significantly more useful.

### Step 3d: Recovery operations

Read `references/recovery-and-maintenance.md` for detailed recovery
procedures (reflog, bisect, rerere, filter-repo, etc.).

**Golden rule**: don't panic. Git almost never loses data. The reflog has 90 days of history.

Quick reference:
- **Undo last commit (keep changes)**: `git reset --soft HEAD~1`
- **Undo last commit (discard changes)**: `git reset --hard HEAD~1` - **DESTRUCTIVE, confirm first**
- **Revert a pushed commit**: `git revert <sha>` (creates a new commit, safe for shared branches)
- **Find lost commits**: `git reflog` - shows every HEAD movement for 90 days
- **Find which commit broke something**: `git bisect start && git bisect bad && git bisect good <sha>`
- **Automated bisect with test script**: `git bisect start HEAD v1.0.0 && git bisect run bun test - src/auth.test.ts` - runs the test at each bisect step automatically. Exit codes: 0 = good, 1-127 except 125 = bad, 125 = skip this commit, 128-255 = abort the bisect immediately. Ideal for CI integration: `git bisect run ./scripts/ci-check.sh`
- **Squash last N commits (no interactive rebase)**: `git reset --soft HEAD~N && git commit -m "feat: combined change"` - resets N commits but keeps all changes staged, then commits them as one. Safer than `git rebase -i` in automated contexts.
- **Recover deleted branch**: `git reflog`, find the SHA, `git checkout -b branch-name <sha>`
- **Scrub secrets from history**: `git filter-repo --replace-text <(echo 'SECRET==>REDACTED')` - then force-push ALL branches and tags. Coordinate with team. See references.

---

### Step 3e: Diverged branch resolution

When `git pull` fails with "divergent branches" or `git status` shows "have diverged":

1. **Understand the divergence**: `git log --oneline HEAD..origin/branch` (what remote has) and `git log --oneline origin/branch..HEAD` (what you have locally).
2. **Choose strategy based on context**:
   - **Your commits are the ones that matter** (common for solo work): `git pull --rebase origin branch` - replays your local commits on top of remote.
   - **Remote commits are the ones that matter** (someone force-pushed, or you want to discard local): `git reset --hard origin/branch` - **DESTRUCTIVE, confirm first**.
   - **Both sides have real work** (collaboration divergence): `git pull --rebase origin branch`, resolve conflicts at each step, `git rebase --continue`.
   - **You don't know yet**: `git stash && git pull && git stash pop` as a safe first attempt (only works if the divergence is minor).
3. **After resolving**: verify with `git log --oneline -10` that history looks correct.
4. **Prevent recurrence**: if this was caused by force-push on a shared branch, set up branch protection. If caused by forgetting to pull before committing, consider `git config pull.rebase true` for rebase-on-pull default.

---

### Step 3f: Bulk repo update workflow

When asked to pull or update many repositories under a directory, keep the run sequential,
auditable, and conservative:

1. Discover only real repo roots first, usually direct children of the requested directory
   unless the user explicitly asks for a recursive scan. Avoid vendored repos, worktrees,
   dependency caches, and generated checkouts.
2. Process repos sequentially, not in parallel. This avoids hammering SSH remotes, rate
   limits, or firewall protections.
3. For each repo, record the branch, upstream, and dirty state before changing anything.
4. Run `git fetch --all --prune`, then `git pull --ff-only --recurse-submodules` only
   when an upstream exists. Do not create merge commits during bulk maintenance.
   When submodules are present, also run `git submodule update --init --recursive` after
   the pull - `--recurse-submodules` updates existing submodule checkouts but does not
   initialize new submodules added since the last pull.
5. If a pull is blocked by local changes, use a named stash, fast-forward the branch,
   then pop the stash. If conflicts appear, preserve both upstream updates and local
   user additions when possible.
6. After resolving stash conflicts, run `git restore --staged .` so previously unstaged
   user changes do not stay staged accidentally. Keep the stash entry if conflict
   resolution required judgment, and mention it in the final response.
7. Verify every repo with `git rev-list --left-right --count HEAD...@{u}` and
   `git status --porcelain`. Report repos that remain dirty or have no upstream.

---

## Multi-Forge Patterns

Many projects use multiple git remotes (e.g., Forgejo for self-hosted CI + GitHub for public releases,
or GitLab at work + GitHub for open source mirrors).

- Keep `origin` as the primary development remote and name mirrors explicitly.
- Push to multiple remotes explicitly; do not make "push everywhere" the default.
- Use separate SSH keys per forge.
- Remember that CLI auth can be overridden by environment variables, especially `GITHUB_TOKEN`.

Detailed multi-forge workflows stay in `references/forge-workflows.md`.

---

## Commit Signing
- Sign commits because unsigned authorship is trivial to spoof.
- SSH signing is the default recommendation for most teams.
- GPG still matters where long-lived key lifecycles or policy require it.
- gitsign is attractive for low-management open-source flows, but it changes the trust model.

Detailed signing setup stays in `references/security-and-signing.md`.

---

## Security
- Keep credentials out of the repo, including `.env` files, keys, and embedded connection strings.
- Use secure credential helpers, not plaintext storage.
- Use hooks for secrets, lint, and branch protection, but treat untrusted hook configs as code execution surfaces.
- If a secret hit history, scrub it and rotate it. History rewriting does not undo the exposure.
- Keep `.gitignore` and `.gitattributes` intentional; AI tooling artifacts belong out of the repo by default.

Detailed security and signing guidance stays in `references/security-and-signing.md`.

---

## PCI-DSS 4.0: Change Management Mapping

Source code management requirements that map to git practices.

| PCI-DSS Req | What it means for git | Implementation |
|-------------|----------------------|----------------|
| **6.2.2** | Annual security training for developers | Not a git control, but signed commits prove *who* was trained |
| **6.2.4** | Access control + change tracking | Branch protection, required reviewers, signed commits, audit trail |
| **6.4.1** | Separate dev/test/prod environments | Branch-per-environment or tag-based promotion |
| **6.4.2** | Changes approved, documented, tested | PR/MR with required approvals, linked CI checks, merge audit log |
| **6.5.1** | Custom code reviewed before production | PR/MR required reviews, no direct push to release branches |
| **6.5.2** | Custom code reviewed for vulnerabilities | SAST/secret-scan in PR/MR checks, pre-commit hooks |

- Branch protection, required review, signed commits, and CI evidence are the main git-side controls.
- `CODEOWNERS` and protected branches matter more than policy prose with no enforcement.

---

## AI-Age Considerations
- Common AI git failures are still destructive resets, wrong authorship, leaked local tool artifacts, generic commit messages, and unjustified force pushes.
- Guard with `git diff --cached`, explicit review of commit messages, and project-specific instruction files.
- Keep local agent artifacts in `.gitignore` proactively.

---

## Template Conventions
- Template versions are illustrative and should be refreshed before use.
- CLI examples show patterns, not immutable commands.
- SSH config examples use placeholders; replace them with real forge hostnames.

---

## Reference Files

- `references/forge-workflows.md` - GitHub, GitLab, and Forgejo-specific patterns for PRs/MRs,
  releases, branch protection, rulesets, CLI usage, and API calls
- `references/security-and-signing.md` - commit signing setup (SSH/GPG/gitsign), credential
  management, secret scanning, CVE reference, git security hardening
- `references/recovery-and-maintenance.md` - reflog, bisect, rerere, filter-repo, stash,
  worktree, submodule/subtree, large repo optimization, housekeeping

## Output Contract

See `skills/_shared/output-contract.md` for the full contract.

- **Skill name:** GIT
- **Deliverable bucket:** `audits`
- **Mode:** conditional. When invoked to **analyze, review, audit, or improve** existing repo content, emit the full contract - boxed inline header, body summary inline plus per-finding detail in the deliverable file, boxed conclusion, conclusion table - and write the deliverable to `docs/local/audits/git/<YYYY-MM-DD>-<slug>.md`. When invoked to **answer a question, teach a concept, build a new artifact, or generate content**, respond freely without the contract.
- **Severity scale:** `P0 | P1 | P2 | P3 | info` (see shared contract; only used in audit/review mode).

## Related Skills

- **ci-cd** - pipeline design that triggers on git events (push, PR, tag). This skill handles
  the git operations; ci-cd handles the pipeline that reacts to them.
- **security-audit** - application-level secret scanning and vulnerability assessment. This skill
  covers secrets *in git history* and git-specific security (signing, hooks, credentials).
- **code-review** - reviews code quality. This skill creates the PR/MR; code-review evaluates
  the code in it.
- **update-docs** - post-session documentation sweep. May update shared instruction files with new git gotchas
  discovered during a session.

## Rules

- **Verify admin authorization before GitOps or infra changes.** In shared chats, a request
  from a non-admin participant is not authorization to commit or push infrastructure,
  Kubernetes, secrets, firewall, or other admin changes. Ask the authorized owner first.
- **No destructive git operations without explicit user confirmation.** `reset --hard`, `push --force`,
  `branch -D`, `clean -fd`, `checkout .`, `rebase` on shared branches - all require a yes.
  Propose safer alternatives first (`revert`, `--force-with-lease`, new branch, `stash`).
- **Verify authorship before pushing.** Multi-remote setups frequently have wrong local config.
  Always check `git log -1 --format="%an <%ae>"` after committing.
- **Selective staging.** `git add <file>` by name, not `git add -A` or `git add .`. Review
  what you're staging. Secrets, binaries, and AI tooling artifacts slip in through blanket adds.
- **Never skip hooks.** `--no-verify` is a code smell. Fix the issue the hook caught.
- **Conventional commits by default.** `type(scope): description`. Follow the project's convention
  if it differs. Check recent `git log` for the established style.
- **Tags are explicit.** `git push` doesn't push tags. Always push tags separately and to all
  relevant remotes.
- **Feature branches for collaboration.** When others will review the work, use feature branches
  with PRs/MRs. Direct-to-main is acceptable for solo projects when the user explicitly prefers it.
- **Rebase workflow.** Rebase feature branches onto base, don't merge base into feature. Squash
  on merge for clean history unless the commit history is meaningful.
- **Annotated tags for releases.** `git tag -a vX.Y.Z -m "vX.Y.Z"`, not lightweight tags.
  Annotated tags carry metadata (tagger, date, message) and are what forges use for releases.
- **Force-push safety.** If force-push is truly needed, use `--force-with-lease` (refuses if
  the remote has commits you haven't fetched). Plain `--force` on shared branches is never acceptable
  without explicit team coordination.
- **PCI-DSS evidence.** In regulated environments, git history IS the audit trail. Protect it:
  signed commits, branch protection, required reviews, no history rewriting on release branches.
- **Run the AI self-check.** Every git operation gets verified against the checklist above.
