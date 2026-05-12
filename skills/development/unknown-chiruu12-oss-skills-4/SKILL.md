---
name: oss-setup-dev-env
description: |
  Set up a complete development environment for an unfamiliar OSS repo. Handles
  dependency installation, building, running tests, and configuring dev tooling.
  Use when cloning a new OSS repo and setting up for development, when the repo's
  setup instructions don't work, or when you need to debug environment issues.
  Not for setting up your own project — this is for getting someone else's repo running.
---

# Setup Dev Env

Get an unfamiliar repo building, running, and testing on your machine. Setup instructions are often outdated or assume knowledge you don't have. This skill systematically works through the actual requirements — not just what the README says.

## Purpose

The #1 reason contributors abandon their first OSS contribution isn't the code — it's the setup. Outdated README instructions, missing system dependencies, version mismatches, and Docker configurations that assume Linux all stop contributors cold. This skill teaches you to read the repo's actual build system, identify real requirements, and get a working development environment — even when the README is wrong.

## When to Use

- Cloning an OSS repo for the first time and setting up to develop
- The repo's setup instructions didn't work
- You need to debug why tests pass in CI but fail locally
- Setting up a repo that uses tools/build systems you're unfamiliar with
- **NOT** for setting up your own project
- **NOT** for CI debugging — use `oss-debug-ci` for that

## Prerequisites

- Repo forked and cloned
- Basic familiarity with your OS's package manager (brew, apt, etc.)
- `gh` CLI authenticated (to check CI configuration for hints)

## Process

### 1. Read the setup instructions (but don't trust them)

Start with the official instructions, but verify as you go.

```bash
# Find setup documentation
cat README.md | head -100
cat CONTRIBUTING.md docs/DEVELOPMENT.md docs/setup.md INSTALL.md 2>/dev/null | head -100

# Check when setup docs were last updated vs when code was last changed
git log --oneline -1 -- README.md CONTRIBUTING.md docs/DEVELOPMENT.md 2>/dev/null
git log --oneline -1 -- .
```

If the setup docs are 6+ months older than the latest code changes, they may be stale. Continue reading them, but verify each step against the actual build configuration.

### 2. Identify the build system and requirements

Read the actual build configuration — this is the source of truth, not the README.

```bash
# Language and package manager detection
ls package.json pnpm-lock.yaml yarn.lock package-lock.json 2>/dev/null  # Node.js
ls pyproject.toml setup.py setup.cfg requirements*.txt Pipfile 2>/dev/null  # Python
ls go.mod go.sum 2>/dev/null  # Go
ls Cargo.toml Cargo.lock 2>/dev/null  # Rust
ls Gemfile Gemfile.lock 2>/dev/null  # Ruby
ls pom.xml build.gradle build.gradle.kts 2>/dev/null  # Java/Kotlin
ls Makefile CMakeLists.txt 2>/dev/null  # Native/C/C++

# Version requirements
cat .node-version .nvmrc .python-version .ruby-version .tool-versions .mise.toml 2>/dev/null
cat package.json 2>/dev/null | grep -A 2 '"engines"'
cat pyproject.toml 2>/dev/null | grep -A 2 "python"
cat go.mod 2>/dev/null | head -3
cat rust-toolchain.toml rust-toolchain 2>/dev/null

# Docker-based development?
ls Dockerfile docker-compose.yml docker-compose.yaml .devcontainer/ 2>/dev/null

# System dependency hints
cat Makefile 2>/dev/null | head -50
cat Brewfile 2>/dev/null
```

Document:
- **Runtime**: what language, what version?
- **Package manager**: npm/pnpm/yarn? pip/uv/poetry? cargo?
- **System deps**: databases, native libraries, tools?
- **Docker**: is development Docker-based or Docker-optional?

### 3. Check CI for the real environment

CI configuration reveals what actually works — it's tested on every commit.

```bash
# Read the CI configuration
cat .github/workflows/ci.yml .github/workflows/test.yml 2>/dev/null

# What versions does CI use?
grep -A 3 "node-version\|python-version\|go-version\|rust-version" .github/workflows/*.yml 2>/dev/null

# What setup steps does CI run?
grep -A 5 "run:" .github/workflows/ci.yml 2>/dev/null | head -40

# What services does CI use? (databases, caches, etc.)
grep -A 10 "services:" .github/workflows/ci.yml 2>/dev/null
```

If the README says "use Node 18" but CI uses Node 22, use Node 22.

### 4. Install dependencies

Follow the build system, not the README.

```bash
# Node.js (detect the right package manager)
# Check for lockfiles to determine which manager
ls pnpm-lock.yaml 2>/dev/null && echo "Use: pnpm install"
ls yarn.lock 2>/dev/null && echo "Use: yarn install"
ls package-lock.json 2>/dev/null && echo "Use: npm install"

# Python
ls pyproject.toml 2>/dev/null && echo "Check: uv, pip, or poetry"
ls requirements.txt 2>/dev/null && echo "Use: pip install -r requirements.txt"

# Go
ls go.mod 2>/dev/null && echo "Use: go mod download"

# Rust
ls Cargo.toml 2>/dev/null && echo "Use: cargo build"
```

**Common failure points**:
- Wrong runtime version → use version manager (nvm, pyenv, rustup)
- Missing native dependencies → check Makefile, CI, or issue tracker for hints
- Network issues → check if the repo uses private registries
- Lockfile conflicts → use the exact package manager version CI uses

### 5. Build and run

```bash
# Find the build command
cat package.json 2>/dev/null | grep -A 10 '"scripts"' | head -15
cat Makefile 2>/dev/null | grep -E "^[a-zA-Z].*:" | head -10
cat pyproject.toml 2>/dev/null | grep -A 10 '\[tool\.' | head -15

# Common build commands
# npm run build / pnpm build / yarn build
# make build / make all
# cargo build
# go build ./...
# python -m build
```

Verify the build succeeds. If it fails, read the error carefully — most build failures are missing dependencies or version mismatches, not code issues.

### 6. Run the tests

This is the real proof that your environment works.

```bash
# Find the test command
cat package.json 2>/dev/null | grep "test"
cat Makefile 2>/dev/null | grep -E "^test.*:"
cat pyproject.toml 2>/dev/null | grep -A 5 '\[tool.pytest'

# Run tests
# npm test / pnpm test / yarn test
# make test
# pytest
# cargo test
# go test ./...
```

If tests fail:
- Compare against CI — do these tests pass there?
- Check for required services (database, Redis, etc.)
- Check for environment variables (`.env.example`, `.env.test`)
- Check for test-specific setup scripts

```bash
# Check for test environment setup
cat .env.example .env.test .env.sample 2>/dev/null
ls scripts/setup-test* test/setup* 2>/dev/null
```

### 7. Set up dev tooling

Match the repo's development workflow.

```bash
# Linting/formatting
cat package.json 2>/dev/null | grep -E "lint|format|prettier|eslint"
ls .eslintrc* .prettierrc* .editorconfig biome.json 2>/dev/null
cat Makefile 2>/dev/null | grep -E "^lint|^format|^check"

# Pre-commit hooks
ls .husky/ .pre-commit-config.yaml 2>/dev/null
cat .pre-commit-config.yaml 2>/dev/null | head -20

# Run the linter to verify your setup
# npm run lint / pnpm lint
# make lint
# cargo clippy
```

### 8. IDE hints (optional)

Check if the repo provides IDE-specific configuration.

```bash
# VS Code / Cursor / Windsurf
ls .vscode/ 2>/dev/null && echo "VS Code config found"
cat .vscode/settings.json 2>/dev/null | head -20
cat .vscode/extensions.json 2>/dev/null

# JetBrains (IntelliJ, PyCharm, WebStorm, etc.)
ls .idea/ 2>/dev/null && echo "JetBrains config found"

# Editor-agnostic config
cat .editorconfig 2>/dev/null

# Debug launch configs
cat .vscode/launch.json 2>/dev/null | head -30
ls .run/ 2>/dev/null  # JetBrains run configurations
```

If the repo provides IDE config:
- **VS Code**: Open the repo in VS Code and install recommended extensions from `.vscode/extensions.json`
- **JetBrains**: Open with the appropriate IDE; `.idea/` configs will be picked up automatically
- **Cursor/Windsurf**: These use VS Code configs — `.vscode/` settings apply
- **Neovim**: Check for `.nvim.lua`, `.neoconf.json`, or LSP settings in the repo

If no IDE config exists, that's fine — the repo works from the command line.

### 9. Thinking gate — verify the environment

> "Before moving on to contribution work:
> 1. Can you build the project? (What's the build command?)
> 2. Do all tests pass? (What's the test command?)
> 3. Does the linter pass? (What's the lint command?)
> 4. If this is a web app / CLI / library — can you actually run it? (What's the run command?)"

If any answer is no, debug it now. A broken environment will waste time during contribution.

## Related Skills

- **Previous step**: ← `oss-prep-to-contribute` — this skill expands on prep step 7
- **If env differs from CI**: → `oss-debug-ci` — diagnose environment mismatches
- **If unfamiliar tools**: → `oss-learn-stack` — learn the build system from the repo
- **Next step**: → `oss-contribute` — start working on the issue

## Common Rationalizations

| Shortcut | Why It Fails |
|----------|-------------|
| "I'll just follow the README exactly" | READMEs go stale. The CI configuration is the source of truth for what actually works. Read both, trust CI when they disagree. |
| "Tests are failing but I'll start coding anyway" | If tests fail before your changes, you can't tell if your changes broke them. Fix the environment first. |
| "I'll skip the linter, I'll fix formatting later" | The linter often catches real issues (unused imports, type errors). Running it now avoids CI failures later. |
| "Docker is too heavy, I'll set up natively" | If the repo's dev workflow is Docker-based, fighting it wastes time. Use Docker when the repo expects it. |
| "I don't need to check CI, the README should be enough" | CI runs on every commit. README gets updated when someone remembers. CI is the single source of truth for environment setup. |

## Red Flags

- Tests fail and user wants to start coding anyway — the environment isn't ready
- User is installing a different runtime version than CI uses — version mismatch will cause problems
- README says "easy setup" but 5+ system dependencies are needed — prepare for a long setup
- User skips running the full test suite — partial verification is no verification
- Docker setup requires Linux-specific features on macOS — expect workarounds

## Verification Checklist

- [ ] Build system identified (language, package manager, version) (step 2)
- [ ] CI configuration read and compared with README (step 3)
- [ ] Dependencies installed using the correct package manager (step 4)
- [ ] Build succeeds (step 5)
- [ ] Full test suite passes (step 6)
- [ ] Linter/formatter runs and passes (step 7)
- [ ] User can build, test, lint, and run the project (step 9)

## Anti-patterns

- **DO NOT** follow the README blindly — cross-reference with CI configuration
- **DO NOT** skip running the full test suite — partial tests give false confidence
- **DO NOT** fight the repo's build system — if they use Docker, use Docker; if they use pnpm, use pnpm
- **DO NOT** install dependencies globally — use the repo's version manager (nvm, pyenv, etc.)
- **DO NOT** modify the repo's config to fit your setup — your setup should match the repo's expectations
