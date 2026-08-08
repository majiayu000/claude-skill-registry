---
name: dev-git-workflow
description: Team Git patterns for branching, PRs, commits, and code review. Use when choosing a branching model or hardening repo collaboration.
---

# Git Workflow (Modern Team Collaboration)

Use modern Git collaboration patterns: GitHub Flow for continuous deploy, trunk-based for scale, Conventional Commits for automation, stacked diffs for large features.

Use this skill to choose a branching model, standardize PR discipline, enforce commit conventions, and harden repository settings for safe collaboration.

## Quick Start

1. Identify constraints (team size, release cadence, CI maturity, compliance).
2. Choose a branching strategy using the decision tree.
3. Apply the baseline repo settings (branch protection, approvals, checks, merge strategy).
4. Use the relevant reference doc for implementation details.
5. If asked "best practice in 2026", verify via web search using `data/sources.json` as a starting source list.

## Quick Reference

| Task | Tool/Command | When to Use | Reference |
|------|-------------|-------------|-----------|
| Create feature branch | `git switch -c feat/name main` | Start new work | [Branching Strategies](references/branching-strategies.md) |
| Create feature worktree | `git worktree add .worktrees/feature -b feature/name` | Isolate one feature per agent/branch | [AI Agent Worktrees](references/ai-agent-worktrees.md) |
| Squash WIP commits | `git rebase -i HEAD~3` | Clean up before PR | [Interactive Rebase](references/interactive-rebase-guide.md) |
| Conventional commit | `git commit -m "feat: add feature"` | All commits | [Commit Conventions](references/commit-conventions.md) |
| Force push safely | `git push --force-with-lease` | After rebase | [Common Mistakes](references/common-mistakes.md) |
| Resolve conflicts | `git mergetool` | Merge conflicts | [Conflict Resolution](references/conflict-resolution.md) |
| Create stacked PRs | `gt create stack-name` (Graphite) | Large features | [Stacked Diffs](references/stacked-diffs-guide.md) |
| Auto-generate changelog | `npx standard-version` | Before release | [Release Management](references/release-management.md) |
| Run quality gates | GitHub Actions / GitLab CI | Every PR | [Automated Quality Gates](references/automated-quality-gates.md) |


## AI Agent Feature Loop

**[AI Agent Worktrees Reference](references/ai-agent-worktrees.md)** — Full guide to worktree isolation for Claude Code, Codex, Aider, and other AI coding agents.

```mermaid
flowchart LR
    A[Plan] --> B[Create worktree<br>per agent/feature]
    B --> C[Verify .gitignore<br>+ install deps]
    C --> D[Agent works<br>scoped commits]
    D --> E[Quality gates]
    E -->|pass| F[PR + merge]
    E -->|fail| D
    F --> G[Cleanup worktree<br>+ delete branch]

    style D fill:#fff3cd,stroke:#d4a017
    style F fill:#d4edda,stroke:#28a745
```

For AI-assisted engineering, prefer this default loop:

1. Create one worktree per feature branch (`git worktree add .worktrees/<feature> -b feature/<name>`).
2. Verify the worktree directory is in `.gitignore` (`git check-ignore -q .worktrees`).
3. Install dependencies and verify clean test baseline before starting work.
4. Implement scoped changes only for that feature.
5. Run repository quality gate(s) before PR.
6. Open one focused PR to the integration branch.
7. After merge, clean up: `git worktree remove` + `git branch -d`.

**Parallel agents:** One worktree per agent, disjoint file ownership, orchestrator merges from main. See [AI Agent Worktrees](references/ai-agent-worktrees.md) for setup, safety patterns, and cleanup.

If repository scripts exist (for example `scripts/git/feature-workflow.sh`), use them to enforce this loop.

## Local Safety Preflight (Before Checkout/Merge/Commit)

Use this quick sequence to avoid common local Git blockers during agent-driven work.

1. Working tree cleanliness:
- `git status --porcelain`
- If non-empty, decide explicitly: commit, stash, or abort branch switch.

2. Lock/process check:
- If Git commands fail with `index.lock`, check running Git processes first:
  - `test -f .git/index.lock && ps aux | rg "[g]it"`
- Remove stale lock only after confirming no active Git process.

3. Branch switch guard:
- Do not `checkout`/`switch` when local changes would be overwritten.
- Commit/stash intentionally; avoid accidental context loss.

4. Merge conflict protocol:
- On conflict, stop new edits, resolve conflict file-by-file, rerun relevant tests, then complete merge commit.

5. Automation note:
- For recurring branch operations, prefer project scripts/worktrees over ad-hoc local branch juggling.


## Decision Tree: Choosing Branching Strategy

```text
Use this decision tree to select the optimal branching strategy for your team based on team size, release cadence, and CI/CD maturity.

Team characteristics -> What's your situation?
    ├─ Small team (1-5 devs) + Continuous deployment + High CI/CD maturity?
    │   └─ GitHub Flow (main + feature branches)
    │
    ├─ Medium team (5-15 devs) + Continuous deployment + High CI/CD maturity?
    │   └─ Trunk-Based Development (main + short-lived branches)
    │
    ├─ Large team (15+ devs) + Continuous deployment + Very high CI/CD maturity?
    │   └─ Trunk-Based + Feature Flags (progressive rollout)
    │
    ├─ Scheduled releases + Medium CI/CD maturity?
    │   └─ GitFlow (main + develop + release branches)
    │
    └─ Multiple versions + Low-Medium CI/CD maturity?
        └─ GitFlow (long-lived release branches)
```

## Navigation: Core Workflows

### Branching Strategies

**[Branching Strategies Comparison](references/branching-strategies.md)** - Comprehensive guide to choosing and implementing branching strategies

- GitHub Flow (recommended for modern teams): Simple, continuous deployment
- Trunk-Based Development (enterprise scale): Short-lived branches, daily merges
- GitFlow (structured releases): Scheduled releases, multiple versions
- Decision matrix: Team size, release cadence, CI/CD maturity
- Migration paths between strategies

### Pull Request Best Practices

**[PR Best Practices Guide](references/pr-best-practices.md)** - Effective code reviews and fast PR cycles

- PR size guidelines: keep PRs reviewable (often 200-400 LOC works well; split larger changes)
- Review categories: BLOCKER, WARNING, NITPICK
- Review etiquette: Collaborative feedback, code examples
- PR description templates: What, Why, How, Testing
- Data-driven insights on review efficiency

### Commit Conventions

**[Conventional Commits Standard](references/commit-conventions.md)** - Commit message formats and semantic versioning integration

- Conventional commit format: `type(scope): description`
- Commit types: feat, fix, BREAKING CHANGE, refactor, docs
- SemVer automation: Auto-bump versions from commits
- Changelog generation: Automated from commit history
- Tools: commitlint, semantic-release, standard-version

---

## Navigation: Advanced Techniques

### Stacked Diffs

**[Stacked Diffs Implementation](references/stacked-diffs-guide.md)** - Platform-specific workflows and team adoption

- What are stacked diffs: Break large features into reviewable chunks
- When to use: Features > 500 lines, complex refactoring
- GitLab native support: MR chains
- GitHub with Graphite: CLI-based stacking
- Benefits: 60% faster review cycles, better quality

### Interactive Rebase

**[Interactive Rebase & History Cleanup](references/interactive-rebase-guide.md)** - Maintain clean commit history

- Auto-squash workflow: `fixup!` and `squash!` commits
- Interactive rebase commands: pick, reword, edit, squash, fixup, drop
- Splitting commits: Break large commits into focused changes
- Reordering commits: Logical commit history
- Best practices: Never rebase public branches

### Conflict Resolution

**[Conflict Resolution Techniques](references/conflict-resolution.md)** - Merge strategies and conflict handling

- Resolution strategies: `--ours`, `--theirs`, manual merge
- Rebase vs merge: When to use each
- Merge tool setup: VS Code, Meld, custom tools
- Conflict markers: Understanding `<<<<<<<`, `=======`, `>>>>>>>`
- Prevention strategies: Frequent rebasing, small PRs

---

## Navigation: Automation & Quality

### Automated Quality Gates

**[Automated Quality Gates](references/automated-quality-gates.md)** - CI/CD pipelines and quality enforcement

- Essential gates: Tests, coverage, linting, security scans
- Advanced gates: Performance benchmarks, bundle size, a11y checks
- GitHub Actions workflows: Complete PR checks pipeline
- GitLab CI pipelines: MR quality gates
- Pre-commit hooks: Husky + lint-staged setup
- Quality metrics thresholds: Coverage 80%, complexity < 10

### Validation Checklists

**[Validation Checklists](references/validation-checklists.md)** - Pre-PR, pre-merge, pre-release checklists

- Before creating PR: Code quality, commit hygiene, testing
- Before merging PR: Review process, CI/CD checks, final verification
- Before releasing: Pre-release testing, version management, documentation
- Post-deployment: Immediate verification, monitoring, tasks
- Hotfix checklist: Critical bug fast-track process

### Release Management

**[Release Management](references/release-management.md)** - Versioning and deployment workflows

- Semantic versioning: MAJOR.MINOR.PATCH
- Manual release workflow: GitFlow release branches
- Automated releases: semantic-release automation
- Hotfix workflow: Emergency patches
- Changelog generation: Keep a Changelog format
- Release checklists: Pre-release, release day, post-release

---

## Navigation: AI Agent Workflows

### AI Agent Worktrees

**[AI Agent Worktrees](references/ai-agent-worktrees.md)** - Worktree isolation patterns for AI coding agents

- When to use worktrees with agents (decision table)
- Directory conventions (`.worktrees/`, global paths, `.gitignore`)
- Agent-specific patterns: Claude Code, Codex, Aider, Copilot Workspace
- Parallel agent execution: one worktree per agent, disjoint file ownership
- Safety: lock contention, conflict detection, cross-agent file guards
- Cleanup lifecycle: removal, pruning, batch cleanup scripts

---

## Navigation: Learning & Troubleshooting

### Monorepo Workflows

**[Monorepo Workflows](references/monorepo-workflows.md)** - Git patterns for monorepo repositories

- Trunk-based branching for monorepos
- Sparse checkout and partial clone
- Affected-only CI (Nx, Turborepo, Bazel)
- CODEOWNERS per package/directory
- Monorepo vs polyrepo decision table

### Git Hooks Automation

**[Git Hooks Automation](references/git-hooks-automation.md)** - Pre-commit, commit-msg, pre-push hooks

- Husky v9+ and lefthook setup
- lint-staged and commitlint integration
- Custom hooks (gitleaks, file size limits, branch naming)
- Team distribution strategies

### Git Bisect Debugging

**[Git Bisect Debugging](references/git-bisect-debugging.md)** - Regression hunting with git bisect

- Manual and automated bisect workflows
- Writing bisect test scripts
- Handling merge commits, log and replay

### Common Mistakes

**[Common Mistakes & Fixes](references/common-mistakes.md)** - Learn from common pitfalls

- Large unfocused PRs -> Split into stacked diffs
- Vague commit messages -> Use conventional commits
- Rewriting public history -> Never rebase main
- Ignoring review comments -> Address all feedback
- Committing secrets -> Use environment variables
- Force push dangers -> Use `--force-with-lease`

## Decision Tables

### When to Use Each Branching Strategy

| Requirement | GitHub Flow | Trunk-Based | GitFlow |
|-------------|-------------|-------------|---------|
| Continuous deployment | [OK] Best | [OK] Best | [FAIL] Poor |
| Scheduled releases | [WARNING] OK | [WARNING] OK | [OK] Best |
| Multiple versions | [FAIL] Poor | [FAIL] Poor | [OK] Best |
| Small team (< 5) | [OK] Best | [WARNING] OK | [FAIL] Overkill |
| Large team (> 15) | [WARNING] OK | [OK] Best | [WARNING] OK |
| Fast iteration | [OK] Best | [OK] Best | [FAIL] Poor |

### PR Size vs Review Time

| LOC | Review Time | Bug Detection | Recommendation |
|-----|-------------|---------------|----------------|
| < 50 | < 10 min | High | [OK] Ideal for hotfixes |
| 50-200 | 10-30 min | High | [OK] Ideal for features |
| 200-400 | 30-60 min | Medium-High | [OK] Acceptable |
| 400-1000 | 1-2 hours | Medium | [WARNING] Consider splitting |
| > 1000 | > 2 hours | Low | [FAIL] Always split |

## Do / Avoid

### GOOD: Do

- Keep PRs under 400 lines (200-400 optimal)
- Use conventional commit messages
- Rebase before opening PR (clean history)
- Require at least one approval before merge
- Run CI checks on every PR
- Use stacked diffs for large features (>500 LOC)
- Squash WIP commits before merge
- Use `--force-with-lease` (not `--force`)

### BAD: Avoid

- Long-lived feature branches (>3 days)
- Merging without review
- Rebasing public/shared branches
- Force pushing to main/master
- Committing secrets (even "temporarily")
- Large monolithic PRs (>1000 lines)
- Vague commit messages ("fix", "update")
- Skipping CI to merge faster

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| **Long-lived branches** | Merge conflicts, stale code | Trunk-based, short branches |
| **Unreviewed merges** | Bugs reach production | Branch protection rules |
| **Rebasing main** | History corruption | Never rebase public branches |
| **1000+ LOC PRs** | Poor review quality | Stacked diffs, split PRs |
| **"fix" commits** | Unclear history | Conventional commits |
| **No CI gates** | Broken main | Required status checks |
| **Secrets in history** | Security breach | Pre-commit hooks, gitleaks |

## Repository Baseline (Security + Reliability)

Set these repo defaults before scaling a team:

- **Branch protection**: require PRs to `main` (no direct pushes), require status checks, require up-to-date branch on merge.
- **Review gates**: require approvals; enforce CODEOWNERS for sensitive paths (auth, payments, infra, prod configs).
- **History policy**: pick merge strategy (squash vs merge commits) and make it consistent; document exceptions.
- **Signed changes**: require signed commits and signed tags for releases (team-specific key management).
- **Secret prevention**: local pre-commit + server-side secret scanning/push protection; rotate on incident.
- **Merge safety**: use merge queue (or equivalent) for busy repos to keep `main` green under high concurrency.
- **Cost control**: cache dependencies/builds; run heavy jobs conditionally; cap CI minutes for untrusted forks.

Template: [assets/pull-requests/pr-template.md](assets/pull-requests/pr-template.md)
Guide: [assets/template-git-workflow-guide.md](assets/template-git-workflow-guide.md)

## Security-Sensitive Changes

For security-related git operations, see [dev-git-commit-message/assets/template-security-commits.md](../dev-git-commit-message/assets/template-security-commits.md):

- Secrets detection with pre-commit hooks
- Handling accidental secret commits
- Security commit metadata (CVE, CVSS)
- Branch protection for security-sensitive code

## Optional: AI/Automation

> **Note**: AI tools assist but cannot replace human judgment for merge decisions.

- **PR summarization** - Generate description from commits
- **Change risk labeling** - Flag high-risk files (auth, payments)
- **Review suggestions** - Identify potential reviewers

### Bounded Claims

- AI summaries need human verification
- Risk labels are suggestions, not guarantees
- Merge decisions always require human approval

---

## Related Skills

- [Software Code Review](../software-code-review/SKILL.md) - Code review standards and techniques
- [Quality Debugging](../qa-debugging/SKILL.md) - Git bisect, debugging workflows
- [DevOps Platform Engineering](../ops-devops-platform/SKILL.md) - CI/CD pipelines, automation
- [Software Testing & Automation](../qa-testing-strategy/SKILL.md) - Test-driven development, coverage gates
- [Documentation Standards](../docs-codebase/SKILL.md) - Changelog formats, documentation workflows
- [Git Commit Message](../dev-git-commit-message/SKILL.md) - Commit message conventions, security commits

## Usage Notes

**For Claude Code**:

- Recommend GitHub Flow for most modern teams (simple, effective)
- Suggest stacked diffs for features > 500 lines
- Always validate commit messages against conventional commit format
- Check PR size - warn if > 400 lines, block if > 1000 lines
- Reference assets/ for copy-paste ready configurations
- Use references/ for deep-dive implementation guidance

**Progressive Disclosure**:

1. Start with Quick Reference for fast lookups
2. Use Decision Tree for choosing strategies
3. Navigate to specific resources for detailed implementation
4. Reference templates for production-ready configurations
5. Check validation checklists before PR/merge/release

---

## Quick Command Reference

**Common Operations**:

```bash
# Rebase feature branch
git fetch origin && git rebase origin/main

# Interactive rebase last 3 commits
git rebase -i HEAD~3

# Squash all commits in branch
git rebase -i $(git merge-base HEAD main)

# Force push safely
git push --force-with-lease origin feature-branch

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Cherry-pick specific commit
git cherry-pick abc123

# Stash changes
git stash push -m "WIP: implementing feature X"
git stash pop
```

**Conflict Resolution**:

```bash
# Pull latest with rebase
git pull --rebase origin main

# Use visual merge tool
git mergetool

# Accept their changes
git checkout --theirs <file>

# Accept your changes
git checkout --ours <file>
```

## Trend Awareness Protocol

IMPORTANT: When users ask recommendation questions about Git workflows, branching strategies, or collaboration tools, verify current trends via web search (and/or the links in `data/sources.json`) before answering.

### Trigger Conditions

- "What's the best Git workflow for [team size/use case]?"
- "What should I use for [branching/PR management]?"
- "What's the latest in Git collaboration?"
- "Current best practices for [branching/code review]?"
- "Is [GitFlow/Trunk-Based] still relevant in 2026?"
- "[GitHub Flow] vs [Trunk-Based] vs [GitFlow]?"
- "Best PR stacking tool?"

### Required Searches

1. Search: `"Git workflow best practices 2026"`
2. Search: `"[specific strategy] vs alternatives 2026"`
3. Search: `"Git collaboration trends January 2026"`
4. Search: `"[branching/PR tools] comparison 2026"`

### What to Report

After searching, provide:

- **Current landscape**: What Git workflows/tools are popular NOW
- **Emerging trends**: New collaboration patterns, tools, or practices gaining traction
- **Deprecated/declining**: Strategies/tools losing relevance or support
- **Recommendation**: Based on fresh data, not just static knowledge

### Example Topics (verify with fresh search)

- Branching strategies (Trunk-Based, GitHub Flow, GitFlow)
- PR stacking tools (Graphite, git-stack, Stacked PRs)
- Merge queue implementations (GitHub, GitLab)
- Code review platforms and automation
- Conventional commits and changelog tools
- Git hosting platform features (GitHub, GitLab, Bitbucket)
- AI-assisted Git workflows

## Fact-Checking

- Use web search/web fetch to verify current external facts, versions, pricing, deadlines, regulations, or platform behavior before final answers.
- Prefer primary sources; report source links and dates for volatile information.
- If web access is unavailable, state the limitation and mark guidance as unverified.
