---
description: Trunk Based Development workflow - all development on main branch with small frequent commits, minimal branching, and continuous integration. Covers when branches are justified (exceptional cases only), commit patterns, feature flag usage for incomplete work, environment branch rules (deployment only), and AI agent default behavior (assume main). Essential for understanding repository git workflow and preventing unnecessary branch proliferation
---

# Trunk Based Development Skill

## Purpose

This Skill provides comprehensive guidance on **Trunk Based Development (TBD)** - the git workflow used throughout this repository where all development happens on the `main` branch with small, frequent commits.

**When to use this Skill:**

- Planning git workflow for new features
- Deciding whether to create a branch
- Understanding when branches are justified
- Managing incomplete work using feature flags
- Navigating environment branches (deployment only)
- Creating plans with git workflow specifications
- Implementing AI agent default behaviors

## Core Concepts

### What is Trunk Based Development?

**Trunk Based Development (TBD)** is a git workflow where:

- **All development happens on `main` branch** (the "trunk")
- **Small, frequent commits** pushed directly to `main`
- **Minimal branching** - branches are exceptional, not standard
- **Short-lived feature branches** (if used) - < 1 day, merge quickly
- **Feature flags** for incomplete work (not branches)
- **Continuous integration** enabled by frequent merges

### Why TBD?

**Benefits**:

- **Reduced merge conflicts**: Small commits integrate continuously
- **Faster feedback**: Changes visible immediately
- **Simpler workflow**: No complex branching strategies
- **Better collaboration**: Everyone works on latest code
- **Easier rollback**: Small commits easier to revert than large branches

**Tradeoffs**:

- **Requires discipline**: Commits must be small and safe
- **Needs feature flags**: Hide incomplete work behind flags
- **Depends on CI/CD**: Automated tests prevent breakage
- **Cultural shift**: Teams used to long-lived branches must adapt

## The 99% Rule: Work on Main

### Default Behavior

**99% of work happens on `main` branch directly.**

**Standard workflow**:

```bash
# 1. Ensure you're on main
git checkout main
git pull origin main

# 2. Make changes
# (edit files)

# 3. Commit frequently
git add [files]
git commit -m "feat(component): add feature X"

# 4. Push to main
git push origin main

# 5. Repeat steps 2-4 for each small change
```

**AI agents assume `main` by default** unless explicitly told otherwise.

### When Main is Default

Use `main` branch for:

- **Feature development** - Build features incrementally with commits to `main`
- **Bug fixes** - Fix and push directly to `main`
- **Refactoring** - Small, safe refactors committed to `main`
- **Documentation** - Write docs, commit to `main`
- **Configuration changes** - Update config, push to `main`
- **Dependency updates** - Upgrade packages, test, push to `main`

**Key principle**: If work is safe to integrate frequently, do it on `main`.

## The 1% Exception: When to Branch

### Justified Branch Scenarios

Branches are **exceptional** and require **explicit justification**. Create branch ONLY for:

**1. Experimental Work (High Risk)**

- **Definition**: Unproven ideas, may be abandoned
- **Duration**: Days to weeks (not months)
- **Example**: Exploring new framework, prototyping radical redesign
- **Justification**: "Testing viability before committing to main"

**2. External Contributions**

- **Definition**: Pull requests from external contributors
- **Duration**: Until review complete
- **Example**: Open source PR from community member
- **Justification**: "External contributor cannot push to main"

**3. Compliance/Audit Requirements**

- **Definition**: Regulatory need for branch-based approval
- **Duration**: Until approval granted
- **Example**: Financial system change requiring dual approval
- **Justification**: "Compliance requires formal branch review"

**4. Parallel Maintenance Versions**

- **Definition**: Supporting multiple major versions simultaneously
- **Duration**: Ongoing (release branches)
- **Example**: Supporting v1.x while developing v2.x
- **Justification**: "Backporting fixes to v1.x users"

### Branch Justification Template

When creating branch, document justification:

```yaml
git-workflow: "Branch: [branch-name]"
branch-justification: |
  **Category**: [Experimental | External | Compliance | Parallel Versions]
  **Reason**: [Specific justification for why main won't work]
  **Duration**: [Expected branch lifespan]
  **Merge Strategy**: [How and when to merge back to main]
```

### ❌ NOT Justified Branch Scenarios

These do **NOT** justify branches (use `main` instead):

- **"Feature in progress"** → Use feature flags on `main`
- **"Needs review before merge"** → Use pair programming or quick reviews on `main`
- **"Might break things"** → Use automated tests on `main`
- **"Working on it for a week"** → Break into smaller commits on `main`
- **"Multiple people on feature"** → Coordinate commits on `main`
- **"Want to keep it separate"** → Preference is not justification

**Key principle**: Branches are for structural necessity, not convenience.

## Feature Flags for Incomplete Work

### What are Feature Flags?

**Feature flags** (feature toggles) are runtime switches that enable/disable features without code changes.

**Purpose**: Hide incomplete work on `main` until ready for users.

### Basic Pattern

```javascript
// Define feature flag (in config or env vars)
const FEATURE_FLAGS = {
  newCheckout: false, // Feature under development
  betaAnalytics: true, // Feature in beta testing
};

// Use flag to conditionally enable feature
function renderCheckout() {
  if (FEATURE_FLAGS.newCheckout) {
    return <NewCheckoutFlow />; // New implementation
  } else {
    return <OldCheckoutFlow />; // Stable implementation
  }
}
```

### Feature Flag Lifecycle

**1. Development Phase** (flag = false):

- Commit new code to `main` with flag disabled
- Code deployed but not executed
- Safe to push incomplete work

**2. Testing Phase** (flag = true for testers):

- Enable flag for internal testing
- Users don't see changes yet
- Iterate based on feedback

**3. Release Phase** (flag = true for everyone):

- Enable flag for all users
- Feature now live
- Monitor for issues

**4. Cleanup Phase** (remove flag):

- After stability confirmed, remove flag and old code
- Simplify codebase
- One path remains

### Feature Flag Best Practices

**DO**:

- Use flags for multi-day features
- Keep flags simple (boolean toggles)
- Document flag purpose and timeline
- Remove flags after feature stable (don't accumulate)
- Test both paths (flag on and off)

**DON'T**:

- Use flags for trivial single-commit changes
- Create complex flag hierarchies
- Keep flags indefinitely (technical debt)
- Forget to test flag-disabled path
- Use flags as permanent configuration

## Environment Branches

### What are Environment Branches?

This repository has **environment-specific branches** for deployment:

- `prod-ayokoding-web` - Production deployment for ayokoding.com
- `prod-ose-platform-web` - Production deployment for oseplatform.com

### Critical Rules

**❌ NEVER commit directly to environment branches**

- Environment branches are **deployment targets**, not development branches
- Changes flow: `main` → CI/CD → environment branch (automated)
- Manual commits to environment branches break deployment pipeline

**✅ Only CI/CD writes to environment branches**

- Deployment automation merges from `main`
- Environment-specific configs applied during deployment
- Tags created on environment branches to track releases

**Workflow**:

```
Developer commits to main → CI/CD tests → CI/CD deploys to environment branch
```

### Environment Branch Naming

**Pattern**: `prod-[app-name]`

**Examples**:

- `prod-ayokoding-web`
- `prod-ose-platform-web`

**Rationale**: Clear, explicit, unambiguous naming prevents accidental commits.

## AI Agent Default Behavior

### Git Workflow in Plans

**Default assumption**: All plans use `main` branch unless explicitly specified otherwise.

**Plan frontmatter** (optional field):

```yaml
git-workflow: "Trunk Based Development (main branch)"
```

**If omitted**: Agents assume TBD on `main` by default.

**If branch specified**: Must include justification:

```yaml
git-workflow: "Branch: experimental-ui-redesign"
branch-justification: |
  **Category**: Experimental
  **Reason**: Testing radical UI redesign that may be abandoned
  **Duration**: 2 weeks exploration phase
  **Merge Strategy**: Merge to main if approved, discard if rejected
```

### Agent Behavior Rules

**When creating plans**:

- Plan-maker agent defaults to `main` branch
- Only suggests branch if user provides justification
- Validates branch justification against TBD criteria
- Warns if branch seems unnecessary

**When executing work**:

- Plan-executor agent works on `main` unless plan specifies branch
- Checks current branch before starting work
- Warns if accidentally on wrong branch
- Never creates branches without explicit instruction

**When validating code**:

- Checker agents validate against `main` branch expectations
- Flag unexpected branches in audit reports
- Recommend merging long-lived branches

## Common Patterns

### Pattern 1: Multi-Day Feature Development

**Scenario**: Feature takes 3 days to complete

**✅ Correct approach (TBD with feature flags)**:

```
Day 1:
- Add feature flag (disabled)
- Commit basic infrastructure to main
- Push to main

Day 2:
- Implement core logic (behind flag)
- Commit to main
- Push to main

Day 3:
- Complete feature (behind flag)
- Test internally with flag enabled
- Enable flag for all users
- Push to main
```

**❌ Wrong approach (long-lived branch)**:

```
Day 1-3:
- Create feature branch
- Accumulate changes
- Risk merge conflicts
- Delayed integration
```

### Pattern 2: Experimental Work

**Scenario**: Testing new framework (may be abandoned)

**✅ Correct approach (short-lived experimental branch)**:

```yaml
git-workflow: "Branch: experimental-graphql"
branch-justification: |
  **Category**: Experimental
  **Reason**: Evaluating GraphQL vs REST, may reject GraphQL
  **Duration**: 1 week evaluation
  **Merge Strategy**: Merge to main if adopted, delete if rejected
```

**Workflow**:

```bash
# Day 1-7: Experiment on branch
git checkout -b experimental-graphql
# (exploration work)

# Day 7: Decision made
# If adopting: Merge to main
git checkout main
git merge experimental-graphql
git push origin main
git branch -d experimental-graphql

# If rejecting: Delete branch
git branch -D experimental-graphql
```

### Pattern 3: External Contribution

**Scenario**: Open source contributor submits PR

**✅ Correct approach (PR branch from fork)**:

```
1. Contributor forks repo
2. Contributor creates branch in fork
3. Contributor opens PR to main
4. Maintainer reviews PR
5. Maintainer merges to main (if approved)
6. Contributor's branch deleted after merge
```

**Key**: Branch is in fork, not main repo. Main repo stays clean.

## Commit Patterns in TBD

### Small, Frequent Commits

**Target**: Multiple commits per day, each < 200 lines changed

**Rationale**: Small commits are:

- Easier to review
- Easier to revert
- Easier to understand in git history
- Lower risk of conflicts

**Example workflow**:

```bash
# Commit 1: Add data model
git add src/models/user.ts
git commit -m "feat(models): add User data model"
git push origin main

# Commit 2: Add repository interface
git add src/repositories/user-repository.ts
git commit -m "feat(repositories): add UserRepository interface"
git push origin main

# Commit 3: Add service layer
git add src/services/user-service.ts
git commit -m "feat(services): add UserService with CRUD operations"
git push origin main
```

**NOT**:

```bash
# Bad: One massive commit after 3 days
git add src/*
git commit -m "feat(user): add complete user management system"
git push origin main
```

### Atomic Commits

**Definition**: Each commit is a complete, working unit

**Rules**:

- ✅ Commit compiles and passes tests
- ✅ Commit includes related changes only
- ✅ Commit message describes change clearly
- ❌ Commit breaks build (fails tests)
- ❌ Commit mixes unrelated changes
- ❌ Commit message is vague

### Conventional Commits

This repository enforces Conventional Commits format:

```
<type>(<scope>): <description>

type: feat | fix | docs | style | refactor | test | chore
scope: component/module being changed
description: brief summary of change
```

**Examples**:

```bash
feat(auth): add JWT token validation
fix(api): handle null response from external service
docs(readme): update installation instructions
refactor(utils): simplify date formatting logic
test(user): add integration tests for user service
```

## Common Mistakes

### ❌ Mistake 1: Creating unnecessary branches

**Wrong thinking**: "I'll create a branch just to be safe"

**Right thinking**: "Can I use feature flags? If yes, work on main"

### ❌ Mistake 2: Long-lived branches (> 1 day)

**Wrong**: Branch open for weeks accumulating changes

**Right**: Short-lived experimental branches (< 1 week) or work on main

### ❌ Mistake 3: Treating environment branches as development branches

**Wrong**: `git commit` directly to `prod-ayokoding-web`

**Right**: Commit to `main`, let CI/CD deploy to environment branch

### ❌ Mistake 4: Large, infrequent commits

**Wrong**: One commit after 3 days with 1000 lines changed

**Right**: 10-15 small commits over 3 days, each < 200 lines

### ❌ Mistake 5: Committing broken code to main

**Wrong**: Push commits that fail tests "I'll fix it later"

**Right**: Every commit passes tests (use pre-push hooks)

## Best Practices

### TBD Checklist

Before pushing to `main`:

- [ ] Commit is small (< 200 lines changed)
- [ ] Commit is atomic (complete, working unit)
- [ ] Tests pass for this commit
- [ ] Commit message follows Conventional Commits
- [ ] Feature incomplete? Hidden behind feature flag
- [ ] No environment branch commits
- [ ] Working on latest `main` (pulled recently)

### When in Doubt

**Ask these questions**:

1. **Can I break this into smaller commits?** → If yes, do it
2. **Is this work experimental and high-risk?** → If no, use `main`
3. **Can I hide incomplete work with feature flag?** → If yes, use `main`
4. **Do I have a valid branch justification?** → If no, use `main`

**Default to `main` unless you have a compelling reason to branch.**

## References

**Primary Convention**: [Trunk Based Development Convention](../../../../governance/development/workflow/trunk-based-development.md)

**Related Conventions**:

- [Commit Message Convention](../../../../governance/development/workflow/commit-messages.md) - Conventional Commits format
- [Implementation Workflow](../../../../governance/development/workflow/implementation.md) - Development workflow stages
- [Plans Organization](../../../../governance/conventions/project/plans-organization.md) - Git workflow in plans

**Related Skills**:

- `plan__writing-gherkin-criteria` - Writing testable acceptance criteria for TBD workflow
- `wow__understanding-repository-architecture` - Understanding repository structure and principles

---

This Skill packages critical Trunk Based Development workflow knowledge for maintaining simple, effective git practices. For comprehensive details, consult the primary convention document.
