---
name: git-hooks
description: Central authority on git hook implementations, modern best practices, and tooling for .NET/C#, JavaScript/TypeScript, Python, and polyglot repositories. Covers framework selection (Husky.Net, lefthook, Husky, pre-commit), setup workflows, Conventional Commits, semantic versioning, secret scanning (gitleaks, TruffleHog), performance optimization, CI/CD integration, testing strategies, and team collaboration patterns. Adaptive to project scale from solo developers to enterprise teams. Use for setting up git hooks, configuring pre-commit/commit-msg/pre-push hooks, integrating dotnet format/dotnet test, ESLint/Prettier, Black/Ruff/mypy, commitlint, choosing between frameworks, optimizing hook performance, enforcing code quality, automating testing, and troubleshooting hook issues.
allowed-tools: Read, Bash, Glob, Grep
---

# Git Hooks

## Overview

This skill provides comprehensive guidance on modern git hook implementations across multiple ecosystems, with primary focus on .NET/C# and strong support for JavaScript/TypeScript and Python. It covers framework selection, setup workflows, performance optimization, security integration, testing strategies, and team collaboration patterns.

**Key capabilities:**

1. **Adaptive framework recommendations** based on ecosystem, scale, and requirements
2. **Complete lifecycle support** from tool selection → setup → configuration → testing → maintenance
3. **Performance-first approach** with parallel execution and incremental processing patterns
4. **Security by default** with mandatory secret scanning integration
5. **CI/CD integration** for defense-in-depth validation (local + remote)
6. **Real-world examples** with copy-paste ready configurations

## When to Use This Skill

Use this skill when you need to:

- **Set up git hooks** for a new or existing project
- **Choose a git hook framework** (Husky.Net vs lefthook vs Husky vs pre-commit)
- **Configure pre-commit hooks** for code formatting, linting, security scanning
- **Configure commit-msg hooks** for Conventional Commits validation
- **Configure pre-push hooks** for running tests or build validation
- **Integrate ecosystem tools** (dotnet format, ESLint/Prettier, Black/Ruff/mypy)
- **Enforce Conventional Commits** with commitlint
- **Scan for secrets** before commits (gitleaks, TruffleHog)
- **Optimize hook performance** (slow hooks blocking developers)
- **Test git hooks** (unit testing, integration testing)
- **Deploy hooks to a team** (automatic installation, CI/CD enforcement)
- **Troubleshoot hook issues** (activation problems, performance issues)
- **Handle monorepo** hook patterns

**Trigger scenarios:**

- "Set up git hooks for my .NET project"
- "How do I enforce code formatting before commits?"
- "Configure Conventional Commits validation"
- "My pre-commit hook is too slow"
- "Should I use Husky.Net or lefthook for C#?"
- "Integrate secret scanning with git hooks"

## Quick Start Decision Tree

### Which framework should I use?

**Answer these questions:**

1. **What's your primary ecosystem?**
   - **.NET/C# only** → Consider **Husky.Net** (native integration) or **lefthook** (performance)
   - **JavaScript/TypeScript only** → Use **Husky** + lint-staged + commitlint
   - **Python only** → Use **pre-commit** framework
   - **Multiple languages (polyglot)** → Use **lefthook** or **pre-commit**

2. **What's your team size/scale?**
   - **Solo developer or small team** → Any framework works; choose based on ecosystem
   - **Medium team (5-20)** → Prioritize ease of installation and CI/CD integration
   - **Large team/enterprise (20+)** → Prioritize performance (lefthook), standardization

3. **What's your performance requirement?**
   - **Speed is critical** → Use **lefthook** (parallel execution, Go-based)
   - **Speed is moderate concern** → Any framework with incremental processing
   - **Speed is not a concern** → Choose based on ecosystem familiarity

### Quick recommendations

| Ecosystem | Solo/Small Team | Medium Team | Large Team/Enterprise |
| --- | --- | --- | --- |
| **.NET/C#** | Husky.Net | Husky.Net or lefthook | lefthook |
| **JavaScript/TypeScript** | Husky + lint-staged | Husky + lint-staged | Husky + lint-staged or lefthook |
| **Python** | pre-commit | pre-commit | pre-commit or lefthook |
| **Polyglot** | lefthook or pre-commit | lefthook | lefthook |

## Framework Comparison at a Glance

| Feature | Husky.Net | lefthook | Husky (JS) | pre-commit |
| --- | --- | --- | --- | --- |
| **Performance** | Moderate | **Excellent** (parallel) | Good (with lint-staged) | Good |
| **Ecosystem** | .NET/C# | **Any** | JavaScript/TS | **Any** (Python primary) |
| **Config Format** | JSON (task-runner.json) | YAML | Shell scripts + package.json | YAML |
| **Parallel Execution** | ❌ No | ✅ Yes | ❌ No | Partial |
| **Learning Curve** | Low (.NET devs) | Moderate | Low (JS devs) | Low (Python devs) |
| **Monorepo Support** | Moderate | **Excellent** | Excellent | Good |

**📖 For detailed comparison:** See [references/framework-comparison.md](references/framework-comparison.md) for comprehensive feature analysis, pros/cons, and selection criteria.

## Core Capabilities

### 1. .NET/C# Workflows

**Quick Start:** Install Husky.Net (`dotnet tool install Husky`) or lefthook (`scoop install lefthook`), configure task-runner.json or lefthook.yml, and verify.

**Key patterns:**

- Use `${staged}` or `{staged_files}` for incremental processing
- Integrate dotnet format (pre-commit) and dotnet test (pre-push)
- Attach Husky.Net to .csproj for automatic team installation

**📖 For complete setup:** See [references/setup-workflows.md](references/setup-workflows.md#netc-workflows)

**Examples:**

- [examples/husky-net-dotnet-format.json](examples/husky-net-dotnet-format.json)
- [examples/lefthook-dotnet.yml](examples/lefthook-dotnet.yml)

---

### 2. JavaScript/TypeScript Workflows

**Quick Start:** Install dependencies (`npm install --save-dev husky lint-staged @commitlint/cli`), initialize Husky (`npx husky init`), configure lint-staged in package.json, and add hooks.

**Key patterns:**

- Use lint-staged for incremental processing (15x speedup)
- Integrate ESLint, Prettier, and commitlint
- Automatic installation via prepare script

**📖 For complete setup:** See [references/setup-workflows.md](references/setup-workflows.md#javascripttypescript-workflows)

**Examples:**

- [examples/husky-javascript-package.json](examples/husky-javascript-package.json)

---

### 3. Python Workflows

**Quick Start:** Install pre-commit (`pip install pre-commit`), create `.pre-commit-config.yaml` with Black/Ruff/mypy hooks, and run `pre-commit install`.

**Key patterns:**

- Use Ruff for 10-100x faster linting than Flake8/pylint
- Extensive plugin ecosystem (hundreds of pre-built hooks)
- Automatic environment management

**📖 For complete setup:** See [references/setup-workflows.md](references/setup-workflows.md#python-workflows)

**Examples:**

- [examples/pre-commit-python.yaml](examples/pre-commit-python.yaml)

---

### 4. Polyglot Workflows

For repositories with multiple languages, use **lefthook** (recommended for performance) or **pre-commit**.

**📖 For complete setup:** See [references/setup-workflows.md](references/setup-workflows.md#polyglot-workflows)

**Examples:**

- [examples/lefthook-polyglot.yml](examples/lefthook-polyglot.yml)

---

### 5. Conventional Commits & Semantic Versioning

**Tools:** commitlint (validation), commitizen (interactive prompts), semantic-release (automated versioning)

**Quick Start:** Install commitlint, configure rules, add commit-msg hook

**📖 For complete setup:** See [references/conventional-commits.md](references/conventional-commits.md)

**Examples:**

- [examples/commitlint.config.js](examples/commitlint.config.js)

---

### 6. Security & Secret Scanning

**Tools:** gitleaks (secret detection), TruffleHog (800+ secret types with API validation)

**Quick Start:** Install gitleaks/TruffleHog, add to pre-commit hooks, configure allowlist for false positives

**Best Practice:** Scan locally (pre-commit) AND in CI/CD (pull requests)

**📖 For complete setup:** See [references/secret-scanning.md](references/secret-scanning.md)

---

### 7. Performance Optimization

**Key strategies:**

1. **Incremental processing** - Only process staged files (15x speedup)
2. **Parallel execution** - Run hooks in parallel with lefthook (90% speedup)
3. **Fast tools** - Use Ruff (10-100x faster than Flake8/pylint)
4. **Caching** - ESLint --cache, dotnet --no-build

**📖 For detailed strategies:** See [references/performance-optimization.md](references/performance-optimization.md)

---

### 8. Testing & Validation

**Levels:**

- **Unit testing** - Test individual hook scripts
- **Integration testing** - Test complete workflow
- **CI/CD validation** - Run same checks locally and remotely (defense in depth)

**📖 For examples and patterns:** See [references/testing-strategies.md](references/testing-strategies.md)

---

### 9. Troubleshooting

**Common issues:**

- **Hooks not running** - Run framework install command, check core.hooksPath
- **Hooks too slow** - Use incremental processing, parallel execution, faster tools
- **Windows path issues** - Use quotes and forward slashes

**Migration strategies:** Gradual rollout (formatting → linting → commit validation → testing/security)

**📖 For complete troubleshooting:** See [references/troubleshooting.md](references/troubleshooting.md)

---

## Configuration Examples

**Complete examples are available in the `examples/` directory:**

- [examples/husky-net-dotnet-format.json](examples/husky-net-dotnet-format.json) - Husky.Net with dotnet format
- [examples/lefthook-dotnet.yml](examples/lefthook-dotnet.yml) - lefthook for .NET/C#
- [examples/husky-javascript-package.json](examples/husky-javascript-package.json) - Husky + lint-staged for JS/TS
- [examples/pre-commit-python.yaml](examples/pre-commit-python.yaml) - pre-commit for Python
- [examples/lefthook-polyglot.yml](examples/lefthook-polyglot.yml) - lefthook for polyglot repositories
- [examples/commitlint.config.js](examples/commitlint.config.js) - Conventional Commits configuration

---

## Migration & Adoption

### Gradual Rollout Strategy

#### Phase 1: Start with formatting (low risk)

- Add dotnet format / Prettier / Black
- Warning mode (don't block commits)
- Team feedback and adjustment

#### Phase 2: Add linting

- Add ESLint / Ruff / StyleCop
- Error mode (block commits)
- Fix existing violations

#### Phase 3: Add commit message validation

- Add commitlint
- Educate team on Conventional Commits
- Provide commitizen for assistance

#### Phase 4: Add testing and security

- Add dotnet test in pre-push
- Add gitleaks in pre-commit
- CI/CD enforcement

---

## Test Scenarios

### Scenario 1: Framework Selection for .NET Project

**User Query:** "I need to set up git hooks for my C# project with 15 developers"

**Expected Behavior:**

- Skill activates on keywords: "git hooks", "C#", ".NET"
- Provides Quick Start Decision Tree guiding to framework selection
- Considers team size (medium team)
- Recommends Husky.Net (native integration) or lefthook (performance)
- Links to framework comparison and setup workflows

---

### Scenario 2: Performance Optimization Request

**User Query:** "My pre-commit hook is taking 35 seconds and blocking developers from committing"

**Expected Behavior:**

- Skill activates on keywords: "pre-commit hook", "slow", "performance"
- Recognizes performance problem
- Provides immediate optimization strategies
- Links to performance-optimization.md for deep-dive

---

### Scenario 3: Framework Comparison Request

**User Query:** "Should I use Husky.Net or lefthook for our .NET team?"

**Expected Behavior:**

- Skill activates on framework names: "Husky.Net", "lefthook"
- Provides framework comparison matrix
- Asks relevant follow-up questions (team size, performance requirements)
- Guides decision based on context

---

### Scenario 4: Conventional Commits Implementation

**User Query:** "How do I enforce Conventional Commits in my JavaScript project?"

**Expected Behavior:**

- Skill activates on keywords: "Conventional Commits", "JavaScript", "enforce"
- Recognizes commit validation need
- Provides setup steps for commitlint
- Links to conventional-commits.md for complete guide

---

### Scenario 5: Secret Scanning Integration

**User Query:** "I want to prevent developers from accidentally committing secrets to our repository"

**Expected Behavior:**

- Skill activates on keywords: "secrets", "prevent", "commit"
- Recognizes security requirement
- Recommends gitleaks or TruffleHog
- Links to secret-scanning.md
- Mentions both local (pre-commit) and CI/CD enforcement

---

## References

**Official Documentation (access via MCP servers):**

- **Husky.Net:** <https://alirezanet.github.io/Husky.Net/>
- **lefthook:** <https://github.com/evilmartians/lefthook>
- **Husky (JS):** <https://typicode.github.io/husky/>
- **pre-commit:** <https://pre-commit.com/>
- **commitlint:** <https://commitlint.js.org/>

**Detailed references:**

- [references/framework-comparison.md](references/framework-comparison.md) - Framework comparison and selection criteria
- [references/setup-workflows.md](references/setup-workflows.md) - Setup workflows for all ecosystems
- [references/conventional-commits.md](references/conventional-commits.md) - Conventional Commits setup
- [references/secret-scanning.md](references/secret-scanning.md) - Secret scanning integration
- [references/performance-optimization.md](references/performance-optimization.md) - Performance strategies
- [references/testing-strategies.md](references/testing-strategies.md) - Testing and validation patterns
- [references/troubleshooting.md](references/troubleshooting.md) - Troubleshooting guide

## Version History

- **v1.0.0** (2025-12-26): Initial release

---

## Last Updated

**Date:** 2025-11-28
**Model:** claude-opus-4-5-20251101

**Research Sources:** Microsoft Learn MCP, Context7 MCP (Husky.Net, lefthook, Husky, pre-commit repositories), Perplexity MCP (2024-2025 best practices), Firecrawl MCP (official documentation sites), Ref MCP (commitlint, semantic-release).
