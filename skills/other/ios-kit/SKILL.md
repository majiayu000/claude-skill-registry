---
name: ios-kit
description: Startup runbook for iOS projects. Establishes stack decisions, scaffolds the project, configures GitHub security, and confirms governing constraints.
---

## Purpose

Initialize a new iOS project with the standard stack, scaffolding, GitHub security, and constraints.

Input: `<app-name>` (optional, default: "App")

## Startup sequence (execute in order)

### 1. Confirm stack decisions

Execute `/ios-stack` to establish platform choices, architecture, environment model, and quality posture.

### 2. Scaffold the project

Execute `/ios-scaffold <app-name> [--github]` to create a buildable baseline with offline-first storage, push plumbing (stubbed), tooling, and CI.

Verify the scaffold passes all quality gates before proceeding (build, tests, lint, format).

### 3. Set up local Git hooks

Execute `/github-hooks --platform ios` to install Git hooks for pre-commit validation (SwiftLint, SwiftFormat, secrets), commit message enforcement, and pre-push tests.

### 4. Configure GitHub security (if --github was used)

Execute `/github-secure` to apply branch protection, Dependabot, CodeQL (Swift), CODEOWNERS, SECURITY.md, PR templates, and security workflows.

### 5. Verify constraints are active

Confirm these always-on skills are enabled:

- `ios-sec` — security policy
- `ios-nfr` — non-functional requirements
- `ios-std` — coding standards
- `ios-styleguide` — design/UX standards

## Quality workflows (invoke as needed)

- `/ios-unit-test` — run tests, report failures, fix with approval
- `/ios-code-review` — review against policies, fix with approval
- `/ios-design-review` — visual review of screens, fix with approval

## Additional workflows (invoke as needed)

- `/ios-add-feature` — scaffold new features
- `/ios-add-auth` — add authentication
- `/ios-deps` — dependency management
- `/ios-release` — App Store release preparation
- `/ios-teardown` — tear down project (reverse of `/ios-kit`)

## Ready state

After completing the startup sequence, the project is ready to develop when ALL of these pass:

- `xcodebuild build` succeeds with zero warnings
- `xcodebuild test` passes all tests
- `./scripts/lint.sh` reports zero violations
- `./scripts/format.sh` makes no changes
- Git hooks are installed and functional (pre-commit, commit-msg, pre-push)
- CI passes on first push (if --github)

If any gate fails, fix before proceeding to feature development.

## Output

After running this kit, confirm:

- Stack decisions applied
- Project scaffolded and building
- **Local Git hooks installed (pre-commit, commit-msg, pre-push)**
- **GitHub security configured (if --github)**
- Governing constraints active
- Quality workflows available
- **Ready state achieved (all gates passing)**
