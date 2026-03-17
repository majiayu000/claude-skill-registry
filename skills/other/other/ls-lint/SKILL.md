---
disable-model-invocation: false
name: ls-lint
user-invocable: false
description: This skill should be used when the user asks to "configure ls-lint", "set up filename linting", "enforce naming conventions", "create .ls-lint.yml", "lint file names", "lint directory names", "file naming rules", "directory structure linting", or mentions ls-lint, directory naming rules, or filename conventions.
---

# ls-lint v2.3

> **Version Notice:** This skill documents **ls-lint v2.3** specifically. Before proceeding, verify the installed version matches:
>
> ```bash
> ls-lint --version
> # or
> npx @ls-lint/ls-lint --version
> ```
>
> If a different version is installed, **stop and consult the official documentation** for that version at https://ls-lint.org or the GitHub repository at https://github.com/loeffel-io/ls-lint. Configuration syntax and available rules may differ between versions.

An extremely fast directory and filename linter that enforces naming conventions across project filesystems.

**Official Resources:**

- **GitHub**: https://github.com/loeffel-io/ls-lint
- **Documentation**: https://ls-lint.org/2.3/getting-started/introduction.html

**Key features:**

- Processes thousands of files in milliseconds
- Minimal configuration via `.ls-lint.yml`
- Cross-platform: Windows, macOS, Linux
- Full Unicode support
- Minimal dependencies (go-yaml, doublestar)

## Installation

```bash
# NPM (recommended)
npm install -D @ls-lint/ls-lint

# NPX (no install)
npx @ls-lint/ls-lint

# Homebrew (macOS/Linux)
brew install ls-lint

# Direct download (Linux amd64)
curl -sL -o ls-lint https://github.com/loeffel-io/ls-lint/releases/download/v2.3.1/ls-lint-linux-amd64
chmod +x ls-lint
```

## Configuration Basics

Create `.ls-lint.yml` in the project root with two main sections:

```yaml
ls:
  # Rules for directories and file extensions
  .js: kebab-case
  .ts: kebab-case

ignore:
  # Paths to exclude from linting
  - .git
  - node_modules
```

### Running ls-lint

```bash
# Run with default config (.ls-lint.yml)
npx @ls-lint/ls-lint

# Custom config path
ls-lint --config path/to/.ls-lint.yml

# Custom working directory
ls-lint --workdir /path/to/project
```

## Built-in Rules

Six naming convention rules are available:

| Rule                   | Description                                | Example          |
| ---------------------- | ------------------------------------------ | ---------------- |
| `lowercase`            | All lowercase letters, ignores non-letters | `readme`, `test` |
| `camelCase`            | camelCase, letters and digits only         | `myFile`         |
| `PascalCase`           | PascalCase, letters and digits only        | `MyComponent`    |
| `snake_case`           | Lowercase with underscores                 | `my_file`        |
| `SCREAMING_SNAKE_CASE` | Uppercase with underscores                 | `MY_CONSTANT`    |
| `kebab-case`           | Lowercase with hyphens                     | `my-file`        |

### Combining Rules

Use the pipe operator `|` to allow multiple conventions:

```yaml
ls:
  .ts: camelCase | PascalCase   # Either is valid
  .js: kebab-case | snake_case
```

## Extensions & Sub-extensions

### Standard Extensions

Apply rules to specific file types:

```yaml
ls:
  .js: kebab-case
  .ts: kebab-case
  .json: kebab-case
  .md: SCREAMING_SNAKE_CASE   # README.md, CHANGELOG.md
```

### Sub-extensions

Handle compound extensions like `.d.ts`, `.test.js`, `.module.css`:

```yaml
ls:
  .d.ts: kebab-case           # Type definition files
  .test.ts: kebab-case        # Test files
  .module.css: kebab-case     # CSS modules
  .config.js: kebab-case      # Config files
```

### Wildcard Extension

Match all extensions with `.*`:

```yaml
ls:
  .*: kebab-case              # All files must be kebab-case
```

### Directory Naming

Use `.dir` to enforce directory name conventions:

```yaml
ls:
  .dir: kebab-case            # All directories must be kebab-case
```

## Path Patterns

### Global Rules

Rules at the top level apply project-wide:

```yaml
ls:
  .js: kebab-case             # Applies everywhere
  .ts: kebab-case

ignore:
  - node_modules
```

### Directory-Specific Rules

Override global rules for specific directories:

```yaml
ls:
  .js: kebab-case             # Global default

  components:                 # Override for components/
    .js: PascalCase

  src/models:                 # Override for src/models/
    .js: PascalCase
```

Directory rules apply to the specified directory and all its subdirectories.

### Glob Patterns

Use wildcards for flexible path matching:

```yaml
ls:
  # Single wildcard: matches one directory level
  packages/*/src:
    .ts: kebab-case

  # Double wildcard: matches any depth
  packages/**/components:
    .tsx: PascalCase
```

### Alternative Patterns

Use curly braces for multiple alternatives:

```yaml
ls:
  packages/*/{src,tests}:
    .ts: kebab-case

  src/{components,pages}:
    .tsx: PascalCase
```

## Advanced Rules

### Regex Patterns

For custom naming patterns, use regex with `regex:^pattern$` format:

```yaml
ls:
  # Files must start with uppercase letter
  .ts: regex:^[A-Z].*$

  # Allow files starting with underscore or letter
  .js: regex:^[_a-z][a-zA-Z0-9]*$
```

Combine regex with built-in rules:

```yaml
ls:
  .ts: PascalCase | regex:^index$   # PascalCase OR "index"
```

### Directory Substitution

Reference parent directory names in patterns:

```yaml
ls:
  # File must match parent directory name
  components/*/:
    .tsx: regex:^${0}$   # ${0} = parent directory name
```

### Exists Rule

Enforce file quantity constraints:

```yaml
ls:
  # Exactly one index file required
  src/:
    index.ts: exists:1

  # Between 1-5 test files allowed
  tests/:
    .test.ts: exists:1-5

  # No image files allowed
  src/:
    .png: exists:0
    .jpg: exists:0
```

Combine with naming rules:

```yaml
ls:
  .ts: kebab-case | exists:1   # Must be kebab-case AND exactly one
```

## Common Configurations

### JavaScript/TypeScript Project

```yaml
ls:
  .dir: kebab-case
  .js: kebab-case
  .ts: kebab-case
  .tsx: PascalCase           # React components
  .d.ts: kebab-case
  .json: kebab-case
  .md: SCREAMING_SNAKE_CASE

  src/components:
    .tsx: PascalCase

ignore:
  - .git
  - node_modules
  - dist
  - coverage
```

### Monorepo Pattern

```yaml
ls:
  .dir: kebab-case
  .*: kebab-case

  packages/*/src:
    .ts: kebab-case
    .tsx: PascalCase

  packages/*/{src,tests}:
    .dir: kebab-case

ignore:
  - .git
  - node_modules
  - "**/dist"
  - "**/coverage"
  - "**/build"
```

## GitHub Actions Integration

Basic workflow configuration:

```yaml
# .github/workflows/lint.yml
name: Lint
on: [push, pull_request]

jobs:
  ls-lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ls-lint/action@v2
```

### Action Configuration Options

```yaml
- uses: ls-lint/action@v2
  with:
    config: .ls-lint.yml          # Config file path
    workdir: .                    # Working directory
    error-output-format: text     # text or json
    warn: false                   # Output to stdout, exit 0
    debug: false                  # Enable debug output
```

## Troubleshooting

### Common Issues

**No files matched**: Verify path patterns match actual directory structure.

**Rule not applying**: Check for more specific rules that might override.

**Ignore not working**: Ensure ignore patterns use correct glob syntax.

### Debug Mode

Run with verbose output to diagnose issues:

```bash
ls-lint --debug
```

## External Resources

For features not covered in this skill, consult:

- **GitHub Repository**: https://github.com/loeffel-io/ls-lint
- **Official Documentation**: https://ls-lint.org/2.3/getting-started/introduction.html
- **GitHub Action**: https://github.com/ls-lint/action

The official documentation covers additional features like:

- Multiple configuration files
- Bazel integration
- Docker usage
- Complete regex syntax
