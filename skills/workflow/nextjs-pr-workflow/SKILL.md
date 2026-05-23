---
name: nextjs-pr-workflow
description: Complete Next.js PR workflow using pr-creation-workflow, jira-git-integration, and linting-workflow frameworks
license: Apache-2.0
compatibility: opencode
metadata:
  audience: developers
  workflow: nextjs-pr
---

## What I do

I implement a complete Next.js PR creation workflow by extending framework skills:

1. **Identify Target Branch**: Determine which branch PR should merge into (configurable, not hardcoded)
2. **Run Next.js Quality Checks**: Execute `npm run lint`, `npm run build`, and `npm run test` using `linting-workflow` framework
3. **Identify Tracking**: Check for JIRA tickets or git issue references
4. **Create Pull Request**: Use `pr-creation-workflow` framework with `git-semantic-commits` for PR title formatting
5. **Add JIRA Comments**: Use `git-issue-updater` framework for consistent JIRA ticket updates

**Critical Requirement**: All tests MUST pass (`npm run test`) before PR creation. This is a blocking step.

## When to use me

Use this workflow when:
- Completing implementation of a PLAN.md file
- Finishing new feature implementation in Next.js apps
- Ready to create a PR after development is complete
- Need to ensure code quality before submitting changes
- Following the standard practice of linting, building, and testing before PR
- **All tests must pass** before PR can be created (blocking requirement)

**Frameworks Used**:
- `pr-creation-workflow`: For PR creation logic and quality checks
- `linting-workflow`: For Next.js linting (npm run lint)
- `jira-git-integration`: For JIRA ticket management and comments

## When to use me

Use this workflow when:
- Completing implementation of a PLAN.md file
- Finishing new feature implementation in Next.js apps
- Ready to create a PR after development is complete
- Need to ensure code quality before submitting changes
- Following the standard practice of linting and building before PR

## When to use me

Use this workflow when:
- Completing implementation of a PLAN.md file
- Finishing new feature implementation in Next.js apps
- Ready to create a PR after development is complete
- Need to ensure code quality before submitting changes
- Following the standard practice of linting and building before PR

## Prerequisites

- Next.js project with `npm run lint`, `npm run build`, and `npm run test` scripts
- Git repository initialized and on a feature branch
- Active Atlassian/JIRA account (if using JIRA integration)
- Write access to repository
- PLAN.md file with implementation details
- **All existing tests must pass** before using this workflow

## Steps

### Step 1: Check Project Structure

Verify this is a Next.js project and check for required scripts:
```bash
# Verify package.json exists and has required scripts
jq -r '.scripts.lint and .scripts.build and .scripts.test' package.json
```

**Required scripts**: `lint`, `build`, and `test`. If any script is missing, the workflow cannot proceed.

### Step 2: Identify Target Branch

Ask user which branch PR should merge into. Note: This is not necessarily `dev` - different projects use different conventions.

**Use**: Ask user or detect default from `git symbolic-ref`

### Step 3: Run Quality Checks via Linting Workflow

Use `linting-workflow` framework with JavaScript/TypeScript language detection:
- Framework: ESLint
- Package manager: npm/yarn/pnpm
- Run `npm run lint` (or `yarn lint` / `pnpm lint`)
- Apply auto-fix with `npm run lint -- --fix`
- Handle errors with re-running

### Step 3.5: Run Tests (BLOCKING STEP)

Before proceeding to PR creation, **all tests must pass**:
```bash
# Run test suite
npm run test

# Or with coverage
npm run test -- --coverage
```

**Behavior**:
- If tests pass: Continue to PR creation
- If tests fail: Do NOT create PR. User must fix failing tests first
- Error message: "Tests failed. Please fix test failures before creating PR. Run: npm run test"

**Test Requirements**:
- All unit tests must pass
- All integration tests must pass
- No skipped tests (unless documented)
- Coverage threshold (if configured) must be met

### Step 3.6: Update Coverage Badge in README

Use `coverage-readme-workflow` to update README with latest coverage:
- Run tests with coverage
- Extract coverage percentage
- Update coverage badge in README.md
- Ensure badge color reflects coverage level

This ensures PR includes updated coverage documentation.

**Coverage Update Command:**
```bash
# Run coverage workflow (delegated to coverage-readme-workflow)
opencode --agent coverage-readme-workflow "update coverage badge"
```

**Behavior**:
- If coverage badge exists: Update with new percentage
- If coverage badge doesn't exist: Add new badge and section
- Badge color reflects coverage level (>=80% green, 60-79% yellow, 40-59% orange, <40% red)

### Step 4: Identify Tracking System

Read PLAN.md for JIRA ticket references:
```bash
# Check for JIRA ticket
PLAN_JIRA=$(grep -oE "[A-Z]+-[0-9]+" PLAN.md | head -1)
```

### Step 5: Create Pull Request via PR Workflow

Use `pr-creation-workflow` framework with Next.js-specific configuration:
- Quality checks: `npm run lint`, `npm run build`, and `npm run test`
- **Test validation is MANDATORY** - PR cannot be created if tests fail
- Target branch: User-specified or detected
- Tracking: JIRA ticket or git issue
- Platform: GitHub PR (not GitLab)
- **Use git-semantic-commits for PR title formatting**: Follow Conventional Commits specification
  - Examples: `feat: add user authentication`, `fix(ui): resolve layout issue`, `docs: update API docs`
  - Include ticket reference: `feat: add login feature [IBIS-456]` or `fix(IBIS-456): resolve session timeout`
  - Use scope: `feat(api): add authentication`, `fix(ui): resolve layout issue`
  - Breaking changes: `feat!: breaking API change` or `feat(api)!: breaking change to authentication`
- PR body should include test results summary

### Step 6: Handle JIRA Integration via Git Issue Updater

Use `git-issue-updater` framework for:
- JIRA resource detection (cloud ID, projects)
- Adding comments with PR details (user, date, time, commit hash, files changed)
- Uploading images (if applicable)
- Consistent progress tracking across all JIRA tickets

### Step 7: Merge Confirmation

After PR creation, ask user to confirm merge target before proceeding.

## Example PLAN.md Integration

When your PLAN.md contains:
```markdown
# Plan: Add New Feature

## Overview
Implements a new feature for...

## JIRA Reference
IBIS-456: https://company.atlassian.net/browse/IBIS-456

## Implementation
...
```

This skill will:
1. Detect JIRA ticket `IBIS-456`
2. Run linting and build
3. Create PR with Conventional Commits format (e.g., `feat: add user component [IBIS-456]`)
4. Add comment to JIRA ticket IBIS-456 using git-issue-updater
5. Prompt for merge target

## Common Issues

### Linting Errors
- **Issue**: Many linting errors at once
- **Solution**: Run `npm run lint -- --fix` first, then manually fix remaining errors

### Build Failures
- **Type Errors**: Check TypeScript types and interfaces
- **Import Errors**: Verify all imports are correct and paths exist
- **Missing Dependencies**: Run `npm install` to ensure all dependencies are installed
- **Environment Variables**: Check `.env.local` or environment configuration

### JIRA Integration
- **Permission Denied**: Ensure your account has JIRA access and comment permissions
- **Cloud ID Not Found**: Use `atlassian_getAccessibleAtlassianResources` to locate it
- **Ticket Not Found**: Verify the ticket key exists and is accessible

### Git Issues
- **Branch Diverged**: Rebase with `git rebase <target-branch>` before PR creation
- **Wrong Target Branch**: Verify you're creating the PR against the correct branch (not always `dev`)
- **Unstaged Changes**: Ensure all changes are committed before PR
- **No gh CLI**: Install GitHub CLI: `https://cli.github.com/`

## Best Practices

- Always run linting, building, and testing before creating any PR
- **Never create a PR with failing tests** - this is a blocking requirement
- Keep PRs focused and small (ideally < 400 lines changed)
- **Use git-semantic-commits for PR title formatting** following Conventional Commits specification
- Write clear, descriptive PR titles: `feat: add user component [IBIS-456]` or `fix(IBIS-456): resolve session timeout`
- Include scope when relevant: `feat(api): add authentication`, `fix(ui): resolve layout issue`
- Use breaking change indicator: `feat!: breaking API change` or `feat(api)!: breaking change to authentication`
- Include quality check status in every PR (linting ✓, build ✓, test ✓)
- **Use git-issue-updater for JIRA ticket updates** with consistent format (user, date, time, PR details)
- Add JIRA comments immediately after PR creation for traceability
- Never skip the build or test steps - they catch production-breaking issues
- Commit linting, build, and test fixes separately for clarity
- Use semantic branch names (e.g., `feature/IBIS-456-add-component`)
- Review your own changes before submitting PR

## Troubleshooting Checklist

Before creating PR:
- [ ] `npm run lint` passes with no errors
- [ ] `npm run build` completes successfully
- [ ] `npm run test` passes with no failures (**BLOCKING**)
- [ ] All tests pass (unit, integration, e2e)
- [ ] No skipped tests (unless documented)
- [ ] Coverage badge updated in README.md
- [ ] All changes are committed and staged
- [ ] Target branch is identified (main, develop, staging, etc. - not necessarily `dev`)
- [ ] Branch is up to date with target branch
- [ ] PLAN.md is updated if implementation changed
- [ ] JIRA ticket or git issue reference is identified
- [ ] PR body includes all necessary documentation

## Related Skills

- **Next.js Specific**:
  - `nextjs-standard-setup`: For creating standardized Next.js 16 applications with proper component architecture
  - `nextjs-unit-test-creator`: For generating comprehensive unit tests for Next.js applications
- **Git Frameworks**:
  - `git-semantic-commits`: For semantic commit message formatting and PR title conventions
  - `git-issue-updater`: For consistent issue/ticket update functionality with user, date, time
- **JIRA Integration**:
  - `jira-git-workflow`: For creating JIRA tickets and initial PLAN.md setup
- **Quality Assurance**:
  - `linting-workflow`: For code quality checks (ESLint, Pylint, etc.)
  - `coverage-readme-workflow`: For updating README with coverage badges before PR creation
- **PR Workflows**:
  - `pr-creation-workflow`: For generic PR creation workflow
  - `git-pr-creator`: For creating Git pull requests with JIRA integration

