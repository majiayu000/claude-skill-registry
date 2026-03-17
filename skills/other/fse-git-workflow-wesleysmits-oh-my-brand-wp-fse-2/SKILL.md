---
name: fse-git-workflow
description: Guide for committing to Oh My Brand! using Conventional Commits, Husky hooks, and linting. Use this when making commits, pushing to remote, or fixing pre-commit linting failures.
metadata:
  author: Wesley Smits
  version: "1.0.0"
---

# FSE Git Workflow

Git workflows, Conventional Commits, Husky pre-commit hooks, and CI/CD for the Oh My Brand! FSE theme.

---

## When to Use

- Making commits to the repository
- Creating feature branches
- Fixing pre-commit linting failures
- Understanding CI/CD pipeline requirements
- Creating pull requests
- Releasing new versions

---

## Reference Files

| File | Purpose |
|------|---------|
| [ci.yml](references/ci.yml) | GitHub Actions CI workflow |
| [PULL_REQUEST_TEMPLATE.md](references/PULL_REQUEST_TEMPLATE.md) | PR template |

---

## Development Workflow

### Initial Setup

```bash
# Clone and install
git clone git@github.com:WesleySmits/oh-my-brand-wp-fse.git
cd oh-my-brand-wp-fse
pnpm install && composer install
pnpm run prepare

# Verify
pnpm run lint && pnpm test && composer test
```

### Daily Flow

```bash
# 1. Start from main
git checkout main && git pull origin main

# 2. Create feature branch
git checkout -b feature/gallery-lightbox

# 3. Develop with watch mode
pnpm run watch

# 4. Lint and test before commit
pnpm run lint:fix && pnpm test && composer test

# 5. Commit (triggers hooks)
git commit -m "feat(gallery): Add lightbox functionality"

# 6. Push and create PR
git push -u origin feature/gallery-lightbox
```

---

## Environment Commands

| Command | Purpose |
|---------|---------|
| `pnpm run build` | Production build |
| `pnpm run watch` | Development watch mode |
| `pnpm run lint` | Run all linters |
| `pnpm run lint:fix` | Fix linting issues |
| `pnpm test` | Run JS/TS tests |
| `pnpm run test:e2e` | Run E2E tests |
| `composer test` | Run PHP tests |
| `composer lint:fix` | Fix PHP issues |

---

## Conventional Commits

### Format

```
<type>(<scope>): <subject>

[optional body]

[optional footer(s)]
```

### Commit Types

| Type | Description | Example |
|------|-------------|---------|
| `feat` | New feature | `feat(gallery): Add zoom functionality` |
| `fix` | Bug fix | `fix(faq): Resolve accordion collapse issue` |
| `docs` | Documentation only | `docs(readme): Update installation steps` |
| `style` | Formatting, CSS (no logic) | `style(css): Fix BEM class indentation` |
| `refactor` | Code refactoring | `refactor(carousel): Simplify state` |
| `perf` | Performance improvement | `perf(images): Implement lazy loading` |
| `test` | Adding/updating tests | `test(gallery): Add navigation tests` |
| `build` | Build system or deps | `build(vite): Upgrade to version 6.1` |
| `ci` | CI configuration | `ci(github): Add e2e job` |
| `chore` | Maintenance tasks | `chore(deps): Update dependencies` |

### Scopes

| Scope | Use For |
|-------|---------|
| `blocks` | Block-related changes |
| `gallery`, `faq`, `hero`, etc. | Specific block |
| `theme` | Theme configuration |
| `assets` | CSS/JS assets |
| `deps` | Dependencies |
| `ci` | CI/CD |

### Subject Rules

| Rule | Requirement |
|------|-------------|
| Case | Sentence case (capitalize first letter) |
| Empty | Subject cannot be empty |
| Full stop | No period at the end |
| Max length | Header max 100 characters |

---

## Branch Naming

### Format

```
<type>/<description>
```

| Type | Use For | Example |
|------|---------|---------|
| `feature/` | New features | `feature/gallery-lightbox` |
| `fix/` | Bug fixes | `fix/carousel-navigation` |
| `docs/` | Documentation | `docs/update-readme` |
| `refactor/` | Code refactoring | `refactor/optimize-helpers` |
| `test/` | Test additions | `test/add-faq-tests` |
| `chore/` | Maintenance | `chore/update-dependencies` |

---

## Git Hooks (Husky)

### Hook: pre-commit

Runs `lint-staged` on staged files:
- ESLint for `*.ts`, `*.js`, `*.tsx`, `*.jsx`
- Stylelint for `*.css`
- PHPCS for `*.php`
- Prettier for formatting

### Hook: commit-msg

Validates commit message format with commitlint.

### What Happens When You Commit

1. **pre-commit** runs lint-staged on staged files
2. **commit-msg** validates message format
3. ✅ All pass → Commit succeeds
4. ❌ Any fail → Commit aborted, fix errors and retry

### Reinstall Hooks

```bash
rm -rf .husky/_
pnpm run prepare
```

---

## Pre-Commit Checklist

- [ ] `pnpm run lint` passes
- [ ] `pnpm run lint:fix` applied
- [ ] `pnpm test` passes
- [ ] `composer test` passes
- [ ] Commit message follows Conventional Commits
- [ ] Branch is up-to-date with `main`

---

## Pull Request Process

1. **Push branch** to remote
2. **Create PR** on GitHub from feature branch to `main`
3. **Fill template** (see [PULL_REQUEST_TEMPLATE.md](references/PULL_REQUEST_TEMPLATE.md))
4. **CI runs** - all checks must pass
5. **Request review** from maintainer
6. **Squash merge** to main after approval

### PR Best Practices

| Practice | Description |
|----------|-------------|
| Small PRs | Keep changes focused |
| Descriptive titles | Use Conventional Commit format |
| Link issues | Reference related GitHub issues |
| Add screenshots | For visual changes |

---

## CI/CD Pipeline

### Pipeline Jobs

See [ci.yml](references/ci.yml) for the full workflow.

| Job | Purpose |
|-----|---------|
| `commitlint` | Validate commit messages |
| `lint-js` | ESLint + Stylelint |
| `lint-php` | PHPCS with WordPress standards |
| `test-unit-js` | Vitest with coverage |
| `test-unit-php` | PHPUnit |
| `test-e2e` | Playwright with wp-env |
| `build` | Production build verification |

### Required Status Checks

All checks must pass before merging:
- ✅ commitlint
- ✅ lint-js
- ✅ lint-php
- ✅ test-unit-js
- ✅ test-unit-php
- ✅ test-e2e
- ✅ build

---

## Release Process

### Semantic Versioning

```
MAJOR.MINOR.PATCH

MAJOR → Breaking changes
MINOR → New features (backward compatible)
PATCH → Bug fixes (backward compatible)
```

### Creating a Release

```bash
# 1. Ensure main is up to date
git checkout main && git pull origin main

# 2. Update version in: style.css, package.json, functions.php

# 3. Update CHANGELOG.md

# 4. Commit version bump
git commit -m "chore(release): Bump version to 1.2.0"

# 5. Create and push tag
git tag -a v1.2.0 -m "Release version 1.2.0"
git push origin main --tags

# 6. Create GitHub release
```

---

## Troubleshooting

### Commit Message Errors

**"type must be one of..."**
```bash
# ❌ Wrong
git commit -m "added new button block"

# ✅ Correct
git commit -m "feat(blocks): Add new button block"
```

**"subject must be sentence-case"**
```bash
# ❌ Wrong
git commit -m "feat(gallery): add lightbox"

# ✅ Correct
git commit -m "feat(gallery): Add lightbox"
```

### Lint Errors

```bash
# Fix all linting issues
pnpm run lint:fix

# Fix PHP issues
composer lint:fix

# Stage fixes and retry
git add . && git commit -m "feat(blocks): Add feature"
```

### Git Hook Issues

```bash
# Reinstall hooks
rm -rf .husky/_
pnpm run prepare
```

### Bypass Hooks (Emergency Only)

```bash
git commit -m "fix(urgent): Emergency fix" --no-verify
# Note: CI will still run all checks
```

---

## Related Skills

- [vitest-testing](../vitest-testing/SKILL.md) - JS testing
- [phpunit-testing](../phpunit-testing/SKILL.md) - PHP testing
- [playwright-testing](../playwright-testing/SKILL.md) - E2E testing

---

## References

- [Conventional Commits Specification](https://www.conventionalcommits.org/)
- [Commitlint Documentation](https://commitlint.js.org/)
- [Husky Documentation](https://typicode.github.io/husky/)
- [Semantic Versioning](https://semver.org/)
