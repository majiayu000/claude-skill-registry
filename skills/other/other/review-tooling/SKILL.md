---
name: review-tooling
description: "Detect what dev tooling infrastructure a project has and flag gaps across linters, formatters, pre-commit hooks, test runners, and CI/CD pipelines. Returns structured findings without applying changes. Use when the user asks to \"review tooling\", \"check project tooling\", \"what tooling is missing\", \"review dev infrastructure\", or \"tooling audit\"."
---

# Review Tooling

Detect dev tooling infrastructure and flag gaps. Analysis only. Does not install or configure tools.

## Scope

Tooling review always operates at the project level since config files live at the project root. Scope parameters (diff commands, file lists) are accepted but ignored.

When called standalone, use the git repository root as the project root (fall back to the current working directory if not in a git repo).

## Step 1: Detect Tooling

Search for config files in the project root and subdirectories (exclude vendored directories like `node_modules/`, `vendor/`, `.build/`). Classify findings into five categories:

### Linters

| Config file pattern | Tool |
|---|---|
| `.eslintrc*`, `eslint.config.*` | ESLint |
| `biome.json`, `biome.jsonc` | Biome (linter + formatter) |
| `deno.json`, `deno.jsonc` with `lint` config | Deno lint |
| `.swiftlint.yml` | SwiftLint |
| `ruff.toml`, `[tool.ruff]` in `pyproject.toml` | Ruff |
| `.pylintrc`, `pylintrc` | Pylint |
| `.flake8`, `[flake8]` in `setup.cfg` | Flake8 |
| `.rubocop.yml` | RuboCop |
| `.golangci.yml`, `.golangci.yaml` | golangci-lint |
| `clippy.toml`, `.clippy.toml` | Clippy |
| `ktlint*`, `.editorconfig` with `ktlint` | ktlint |

### Formatters

| Config file pattern | Tool |
|---|---|
| `.prettierrc*`, `prettier.config.*` | Prettier |
| `biome.json`, `biome.jsonc` | Biome (linter + formatter) |
| `deno.json`, `deno.jsonc` with `fmt` config | Deno fmt |
| `.swift-format`, `.swiftformat` | swift-format / SwiftFormat |
| `[tool.black]` in `pyproject.toml`, `pyproject.toml` with `[tool.ruff.format]` | Black / Ruff formatter |
| `rustfmt.toml`, `.rustfmt.toml` | rustfmt |
| `gofmt` / `goimports` (check CI config or `Makefile` for usage) | gofmt |
| `.clang-format` | ClangFormat |

### Pre-commit Hooks

| Config file pattern | Tool |
|---|---|
| `.husky/` directory | Husky |
| `.lintstagedrc*`, `lint-staged` key in `package.json` | lint-staged |
| `.pre-commit-config.yaml` | pre-commit framework |
| `.git/hooks/pre-commit` (non-sample) | Custom git hook |
| `.lefthook.yml`, `lefthook.yml` | Lefthook |

### Test Runners

| Config file pattern | Tool |
|---|---|
| `jest.config.*`, `jest` key in `package.json` | Jest |
| `vitest.config.*` | Vitest |
| `pytest.ini`, `[tool.pytest]` in `pyproject.toml`, `conftest.py` | pytest |
| `Package.swift` with test targets, `*Tests/` directories | Swift Testing / XCTest |
| `_test.go` files | Go testing |
| `Cargo.toml` with `[dev-dependencies]`, `tests/` directory | Rust tests |
| `.rspec`, `spec/` directory | RSpec |
| `phpunit.xml*` | PHPUnit |

### CI/CD Pipelines

| Config file pattern | Tool |
|---|---|
| `.github/workflows/*.yml` | GitHub Actions |
| `.gitlab-ci.yml` | GitLab CI |
| `Jenkinsfile` | Jenkins |
| `.circleci/config.yml` | CircleCI |
| `bitbucket-pipelines.yml` | Bitbucket Pipelines |
| `.travis.yml` | Travis CI |
| `azure-pipelines.yml` | Azure Pipelines |

These tables are not exhaustive. If the project uses a tool not listed here, detect it by recognizing its config files.

## Step 2: Identify the Project Ecosystem

Determine the primary language(s) and ecosystem from config files and source code. This informs which tooling gaps are relevant. A Go project without Prettier is not a gap. A Node.js project without a linter is.

| Signal | Ecosystem |
|---|---|
| `package.json` | Node.js / JavaScript / TypeScript |
| `Package.swift`, `*.xcodeproj` | Swift / Apple |
| `pyproject.toml`, `setup.py`, `requirements.txt` | Python |
| `go.mod` | Go |
| `Cargo.toml` | Rust |
| `Gemfile` | Ruby |
| `pom.xml`, `build.gradle*` | Java / Kotlin |
| `deno.json`, `deno.jsonc` | Deno |

## Step 3: Analyze Gaps

For each category, assess whether the project has adequate tooling for its ecosystem:

- **Present and configured** — tool detected with config file
- **Partially configured** — tool detected but config appears minimal or default
- **Missing** — no tool detected for a category where one is standard for the ecosystem

When assessing pre-commit hooks, also check whether detected linters and formatters are wired into the hooks. A project with ESLint and Prettier but no pre-commit hook means formatting issues can slip into commits.

When assessing CI/CD, check whether the pipeline runs tests and linters. A CI config that only builds but never tests is a gap.

## Output Format

Return findings as a numbered list. For each finding:

```
### [P<N>] <title (imperative, <=80 chars)>

**Category:** <Linters | Formatters | Pre-commit Hooks | Test Runners | CI/CD>

<one paragraph: what is missing or misconfigured and why it matters for this project>
```

After all findings, add:

```
## Tooling Summary

| Category | Status | Tool(s) |
|---|---|---|
| Linters | <Present/Partial/Missing> | <detected tools or "—"> |
| Formatters | <Present/Partial/Missing> | <detected tools or "—"> |
| Pre-commit Hooks | <Present/Partial/Missing> | <detected tools or "—"> |
| Test Runners | <Present/Partial/Missing> | <detected tools or "—"> |
| CI/CD | <Present/Partial/Missing> | <detected tools or "—"> |

## Overall Verdict

**Tooling:** <well-equipped | gaps found>

<1-3 sentence summary>
```

If all categories are adequately covered, report that and highlight what the project does well.

## Priority Levels

- **P0** — No test runner detected for a project with source code
- **P1** — No linter for the primary language, or CI/CD pipeline exists but skips tests
- **P2** — No formatter, no pre-commit hooks, or linter/formatter not wired into hooks
- **P3** — No CI/CD pipeline, or minor config gaps
