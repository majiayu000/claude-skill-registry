---
name: github-hooks
description: Set up local Git hooks for pre-commit validation (lint, format, tests, secrets). Integrates with mern-scaffold, nean-scaffold, and iOS projects.
argument-hint: "[--platform mern|nean|ios] [--no-secrets] [--no-tests]"
allowed-tools: Bash, Write, Read, Glob, Grep
---

## Purpose
Install local Git hooks to catch issues before commits reach the remote. Complements `github-secure` by shifting checks left.

**Designed to work with:** `/mern-scaffold`, `/mern-kit`, `/nean-scaffold`, `/nean-kit`, and iOS projects.

## Arguments
- `--platform <p>` — Target platform: `mern`, `nean`, or `ios` (auto-detected if not specified)
- `--no-secrets` — Skip secret scanning hook
- `--no-tests` — Skip pre-push test hook

## Platform detection
If `--platform` not specified:
- Detect `nx.json` → NEAN
- Detect `pnpm-workspace.yaml` or `turbo.json` → MERN
- Detect `project.yml` (XcodeGen) or `Package.swift` or `*.xcodeproj` → iOS

## What gets created

### MERN (using Husky + lint-staged + pnpm)
```
.husky/
├── pre-commit        # Lint + format staged files
├── commit-msg        # Validate commit message format
└── pre-push          # Run tests before push

.lintstagedrc.json    # Lint-staged configuration
.commitlintrc.json    # Commit message rules
.gitleaks.toml        # Secret scanning config
package.json          # Updated with husky + lint-staged + commitlint
```

### NEAN (using Husky + lint-staged + npm/Nx)
```
.husky/
├── pre-commit        # Lint + format staged files (via Nx)
├── commit-msg        # Validate commit message format
└── pre-push          # Run affected tests before push

.lintstagedrc.json    # Lint-staged configuration (Nx-aware)
.commitlintrc.json    # Commit message rules
.gitleaks.toml        # Secret scanning config
package.json          # Updated with husky + lint-staged + commitlint
```

### iOS (using git hooks directly)
```
.githooks/
├── pre-commit        # SwiftLint + SwiftFormat on staged files
├── commit-msg        # Validate commit message format
└── pre-push          # Run tests before push

scripts/
└── install-hooks.sh  # Hook installation script
```

## Hooks installed

### pre-commit
- Lint staged files (ESLint/SwiftLint)
- Format staged files (Prettier/SwiftFormat)
- Check for secrets (gitleaks)
- Block commits with errors

### commit-msg
- Enforce conventional commits format
- Validate message length
- Check for required prefixes

### pre-push
- Run test suite (NEAN: affected tests only for speed)
- Block push if tests fail
- Optional: run full build

## Workflow
1. Detect or specify platform
2. Install hook dependencies
3. Create hook scripts
4. Configure hook behavior
5. Verify hooks work with test commit

## Secret scanning
Uses `gitleaks` to detect:
- API keys
- Passwords
- Tokens
- Private keys
- Connection strings

## MERN integration notes

When used after `/mern-scaffold`:
- Detects existing pnpm workspace and turbo config
- Adds dependencies to root package.json
- Hooks run the same quality gates as CI (lint, format, test)
- Complements the existing ci.yml workflow

## NEAN integration notes

When used after `/nean-scaffold`:
- Detects existing Nx workspace (`nx.json`)
- Adds dependencies to root package.json (npm)
- Pre-commit runs `npx nx affected --target=lint` on staged files
- Pre-push runs `npx nx affected --target=test`
- Uses Nx's intelligent caching for faster hook execution
- Complements the existing ci.yml workflow

## iOS integration notes

When used after `/ios-scaffold`:
- Detects project.yml (XcodeGen), Package.swift, or *.xcodeproj
- Creates `.githooks/` directory with shell scripts
- Pre-commit runs SwiftLint + SwiftFormat on staged .swift files
- Pre-push runs xcodebuild test
- Includes `scripts/install-hooks.sh` for team onboarding
- Complements the existing ci.yml workflow

## Output
- Hooks installed
- Dependencies added
- Test commit instructions
- **Remind to run `/github-secure` for repository-level security**

## Reference
For hook configurations and customization, see `reference/github-hooks-reference.md`
