---
name: contributing-guide
description: Эксперт CONTRIBUTING.md. Используй для open source guidelines, PR процессов и contributor onboarding.
---

# Contributing Guide Expert

Эксперт по документации для open source contributors.

## Структура CONTRIBUTING.md

```markdown
# Contributing to Project Name

Thank you for your interest in contributing! 🎉

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Pull Request Process](#pull-request-process)
- [Style Guide](#style-guide)
- [Community](#community)
```

## Quick Start Section

```markdown
## Quick Start

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/project-name.git
   cd project-name
   ```
3. Install dependencies:
   ```bash
   npm install
   ```
4. Create a branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
5. Make changes and test:
   ```bash
   npm test
   ```
6. Submit a PR!
```

## Development Environment

```markdown
## Development Setup

### Prerequisites
- Node.js 18+ ([download](https://nodejs.org))
- npm 8+ or yarn 1.22+
- Git 2.28+
- Docker (optional, for integration tests)

### Installation

```bash
# Clone repository
git clone https://github.com/org/project.git
cd project

# Install dependencies
npm install

# Copy environment file
cp .env.example .env

# Run setup script
npm run setup

# Verify installation
npm test
```

### Available Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server |
| `npm test` | Run all tests |
| `npm run test:watch` | Run tests in watch mode |
| `npm run lint` | Run ESLint |
| `npm run lint:fix` | Fix linting issues |
| `npm run typecheck` | Run TypeScript checks |
| `npm run build` | Build for production |
```

## Git Workflow

```markdown
## Git Workflow

### Branch Naming Convention

```
<type>/<short-description>
```

**Types:**
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation only
- `refactor/` - Code refactoring
- `test/` - Adding tests
- `chore/` - Maintenance tasks

**Examples:**
- `feature/user-authentication`
- `fix/login-redirect-loop`
- `docs/api-examples`

### Commit Messages

We follow [Conventional Commits](https://conventionalcommits.org):

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting (no code change)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance

**Examples:**
```
feat(auth): add OAuth2 support
fix(api): handle null response from server
docs(readme): update installation steps
```
```

## Pull Request Template

```markdown
## Pull Request Guidelines

### Before Submitting

- [ ] I have read the [Contributing Guide](CONTRIBUTING.md)
- [ ] My code follows the project's style guidelines
- [ ] I have performed a self-review
- [ ] I have added tests for my changes
- [ ] All new and existing tests pass
- [ ] I have updated documentation if needed
- [ ] My commits follow conventional commit format

### PR Template

```markdown
## Description
<!-- Describe your changes -->

## Type of Change
- [ ] Bug fix (non-breaking change)
- [ ] New feature (non-breaking change)
- [ ] Breaking change
- [ ] Documentation update

## How Has This Been Tested?
<!-- Describe test scenarios -->

## Screenshots (if applicable)
<!-- Add screenshots -->

## Checklist
- [ ] Tests pass
- [ ] Lint passes
- [ ] Documentation updated
```
```

## Issue Templates

### Bug Report

```markdown
---
name: Bug Report
about: Report a bug to help us improve
title: '[BUG] '
labels: bug
assignees: ''
---

## Bug Description
<!-- Clear description of the bug -->

## Steps to Reproduce
1. Go to '...'
2. Click on '...'
3. See error

## Expected Behavior
<!-- What should happen -->

## Actual Behavior
<!-- What actually happens -->

## Environment
- OS: [e.g., macOS 14.0]
- Node version: [e.g., 18.17.0]
- Project version: [e.g., 1.2.3]

## Screenshots
<!-- If applicable -->

## Additional Context
<!-- Any other information -->
```

### Feature Request

```markdown
---
name: Feature Request
about: Suggest a new feature
title: '[FEATURE] '
labels: enhancement
assignees: ''
---

## Problem Statement
<!-- What problem does this solve? -->

## Proposed Solution
<!-- How would you like it to work? -->

## Alternatives Considered
<!-- Other solutions you've considered -->

## Additional Context
<!-- Any other information -->
```

## Code Style Guide

```markdown
## Style Guide

### General Principles
- Write self-documenting code
- Prefer explicit over implicit
- Keep functions small and focused
- DRY (Don't Repeat Yourself)

### TypeScript/JavaScript

```typescript
// ✅ Good
function calculateTotalPrice(items: CartItem[]): number {
  return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
}

// ❌ Bad
function calc(i: any[]): any {
  let t = 0;
  for (let x of i) t += x.p * x.q;
  return t;
}
```

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Variables | camelCase | `userName` |
| Functions | camelCase | `getUserById` |
| Classes | PascalCase | `UserService` |
| Constants | UPPER_SNAKE | `MAX_RETRIES` |
| Files | kebab-case | `user-service.ts` |
| Interfaces | PascalCase + I prefix | `IUserService` |

### File Structure

```
src/
├── components/     # UI components
├── hooks/          # Custom React hooks
├── services/       # Business logic
├── utils/          # Helper functions
├── types/          # TypeScript types
└── __tests__/      # Test files
```
```

## Code Review Process

```markdown
## Code Review

### Review Checklist

**Functionality:**
- [ ] Code works as intended
- [ ] Edge cases handled
- [ ] Error handling adequate

**Code Quality:**
- [ ] Readable and maintainable
- [ ] No unnecessary complexity
- [ ] Follows project conventions

**Testing:**
- [ ] Adequate test coverage
- [ ] Tests are meaningful
- [ ] Edge cases tested

**Security:**
- [ ] No hardcoded secrets
- [ ] Input validation present
- [ ] No SQL injection risks

### Response Times
- First response: within 48 hours
- Follow-up reviews: within 24 hours
- Merge after approval: within 24 hours

### Approval Requirements
- 1 maintainer approval required
- All CI checks must pass
- No unresolved conversations
```

## Pre-commit Hooks

```json
// package.json
{
  "husky": {
    "hooks": {
      "pre-commit": "lint-staged",
      "commit-msg": "commitlint -E HUSKY_GIT_PARAMS"
    }
  },
  "lint-staged": {
    "*.{ts,tsx}": [
      "eslint --fix",
      "prettier --write"
    ],
    "*.{json,md}": [
      "prettier --write"
    ]
  }
}
```

## Recognition Program

```markdown
## Recognition

### Contributors
All contributors are added to our [CONTRIBUTORS.md](CONTRIBUTORS.md) file.

### Badges
| Badge | Criteria |
|-------|----------|
| 🥇 First Contribution | Merged first PR |
| 🔥 Frequent Contributor | 10+ merged PRs |
| 📚 Documentation Hero | 5+ docs PRs |
| 🐛 Bug Hunter | 5+ bug fixes |
| ⭐ Core Contributor | Significant impact |

### Rewards
- Stickers and swag for active contributors
- Shoutouts in release notes
- Conference ticket opportunities
- LinkedIn recommendations
```

## Community Guidelines

```markdown
## Community

### Communication Channels
- **Discord**: [Join our server](https://discord.gg/xxx)
- **GitHub Discussions**: For questions and ideas
- **Twitter**: [@project](https://twitter.com/project)

### Response Time Expectations
- Issues: 48 hours
- PRs: 72 hours
- Questions: 24-48 hours

### Getting Help
1. Check existing issues and discussions
2. Read the documentation
3. Ask in Discord #help channel
4. Create a GitHub Discussion

### Code of Conduct
We follow the [Contributor Covenant](https://contributor-covenant.org).
Be respectful, inclusive, and constructive.
```

## Лучшие практики

1. **Progressive disclosure** — от простого к сложному
2. **Clear examples** — реальные примеры кода
3. **Up-to-date** — обновляйте при изменениях
4. **Welcoming tone** — дружелюбный язык
5. **Multiple entry points** — для разных типов contributions
6. **Automated checks** — CI для валидации PR
