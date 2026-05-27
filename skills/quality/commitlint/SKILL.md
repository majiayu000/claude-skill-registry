---
name: commitlint
description: When setting up commit message validation for a project. When project has commitlint.config.js or .commitlintrc files. When configuring CI/CD to enforce commit format. When extracting commit rules for LLM prompt generation. When debugging commit message rejection errors.
---

# Commitlint

Validate commit messages against Conventional Commits format using commitlint configuration and rules.

## When to Use This Skill

Use this skill when:

- Setting up commitlint for a repository
- Configuring commitlint rules and shareable configurations
- Integrating commitlint with pre-commit hooks or CI/CD pipelines
- Extracting rules from commitlint config to generate LLM prompts for commit message generation
- Validating commit messages programmatically
- Troubleshooting commitlint configuration or validation errors
- Understanding commitlint rule syntax and severity levels
- Detecting commitlint configuration files in a repository

## Core Capabilities

### Configuration Detection

Commitlint uses cosmiconfig to find configuration files in this priority order:

**Dedicated config files:**

```text
.commitlintrc
.commitlintrc.json
.commitlintrc.yaml
.commitlintrc.yml
.commitlintrc.js
.commitlintrc.cjs
.commitlintrc.mjs
.commitlintrc.ts
.commitlintrc.cts
commitlint.config.js
commitlint.config.cjs
commitlint.config.mjs
commitlint.config.ts
commitlint.config.cts
```

**Package files:**

- `package.json` with `commitlint` field
- `package.yaml` (PNPM) with `commitlint` field

### Configuration Formats

**JavaScript ES Modules (Recommended):**

```javascript
// commitlint.config.js or commitlint.config.mjs
export default {
  extends: ['@commitlint/config-conventional'],
};
```

**TypeScript:**

```typescript
// commitlint.config.ts
import type { UserConfig } from '@commitlint/types';
import { RuleConfigSeverity } from '@commitlint/types';

const config: UserConfig = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [RuleConfigSeverity.Error, 'always', ['feat', 'fix', 'docs']],
  },
};

export default config;
```

**JSON:**

```json
{
  "extends": ["@commitlint/config-conventional"]
}
```

**YAML:**

```yaml
extends:
  - "@commitlint/config-conventional"
```

### Rule Configuration

Rules are configured as arrays: `[level, applicability, value]`

**Severity Levels:**

| Level | Meaning  | TypeScript Enum               |
| ----- | -------- | ----------------------------- |
| 0     | Disabled | `RuleConfigSeverity.Disabled` |
| 1     | Warning  | `RuleConfigSeverity.Warning`  |
| 2     | Error    | `RuleConfigSeverity.Error`    |

**Applicability:**

- `'always'` - Rule must match
- `'never'` - Rule must not match

**Example rules:**

```javascript
rules: {
  // Error if type is not in enum
  'type-enum': [2, 'always', ['feat', 'fix', 'docs', 'style', 'refactor', 'perf', 'test', 'build', 'ci', 'chore', 'revert']],

  // Error if type is empty
  'type-empty': [2, 'never'],

  // Error if subject is empty
  'subject-empty': [2, 'never'],

  // Error if header exceeds 100 chars
  'header-max-length': [2, 'always', 100],

  // Error if subject ends with period
  'subject-full-stop': [2, 'never', '.'],

  // Warning if body doesn't have leading blank line
  'body-leading-blank': [1, 'always'],
}
```

## Common Configurations

### @commitlint/config-conventional

The most widely used shareable configuration. Default error-level rules:

| Rule | Configuration | Pass Example | Fail Example |
| --- | --- | --- | --- |
| `type-enum` | `['build', 'chore', 'ci', 'docs', 'feat', 'fix', 'perf', 'refactor', 'revert', 'style', 'test']` | `fix: message` | `foo: message` |
| `type-case` | `'lowerCase'` | `fix: message` | `FIX: message` |
| `type-empty` | `never` | `fix: message` | `: message` |
| `subject-case` | `never` + `['sentence-case', 'start-case', 'pascal-case', 'upper-case']` | `fix: some message` | `fix: Some Message` |
| `subject-empty` | `never` | `fix: message` | `fix:` |
| `subject-full-stop` | `never`, `'.'` | `fix: message` | `fix: message.` |
| `header-max-length` | `100` | Short header | Header > 100 chars |
| `body-leading-blank` | `always` (warning) | Blank line before body | No blank line |
| `body-max-line-length` | `100` | Lines <= 100 chars | Line > 100 chars |
| `footer-leading-blank` | `always` (warning) | Blank line before footer | No blank line |
| `footer-max-line-length` | `100` | Lines <= 100 chars | Line > 100 chars |

### Complete Configuration Schema

```javascript
// commitlint.config.js
export default {
  // Extend shareable configs (resolved via node resolution)
  extends: ['@commitlint/config-conventional'],

  // Parser preset for parsing commit messages
  parserPreset: 'conventional-changelog-atom',

  // Output formatter
  formatter: '@commitlint/format',

  // Custom rules (override inherited rules)
  rules: {
    'type-enum': [2, 'always', ['feat', 'fix', 'docs', 'style', 'refactor', 'test', 'chore']],
  },

  // Functions that return true to ignore specific commits
  // Merged with default ignores (merge commits, reverts, semver tags)
  ignores: [(commit) => commit.includes('WIP')],

  // Whether to use default ignore patterns
  // Default patterns: 'Merge pull request', 'Revert X', 'v1.2.3', etc.
  defaultIgnores: true,

  // Custom help URL shown on failure
  helpUrl: 'https://example.com/commit-guidelines',

  // Prompt configuration (for @commitlint/cz-commitlint)
  prompt: {
    messages: {},
    questions: {
      type: {
        description: 'Select the type of change:',
      },
    },
  },
};
```

## CLI Usage

### Installation

```bash
# npm
npm install -D @commitlint/cli @commitlint/config-conventional

# yarn
yarn add -D @commitlint/cli @commitlint/config-conventional

# pnpm
pnpm add -D @commitlint/cli @commitlint/config-conventional
```

### Common Commands

```bash
# Lint the last commit
npx commitlint --last

# Lint a range of commits
npx commitlint --from HEAD~5

# Lint from a specific commit
npx commitlint --from abc1234

# Lint message from stdin
echo "feat: add feature" | npx commitlint

# Lint message from file
npx commitlint < .git/COMMIT_EDITMSG

# Lint with edit flag (reads .git/COMMIT_EDITMSG)
npx commitlint --edit

# Lint with custom config path
npx commitlint --config ./custom-commitlint.config.js

# Print resolved config
npx commitlint --print-config

# Strict mode (warnings become exit code 2)
npx commitlint --last --strict
```

### Exit Codes

| Code | Meaning                            |
| ---- | ---------------------------------- |
| 0    | Success (no errors)                |
| 1    | Lint errors found                  |
| 2    | Warnings found (strict mode only)  |
| 3    | Errors found (strict mode)         |
| 9    | Config file missing (with -g flag) |

## Rule Reference

### Type Rules

| Rule              | Condition                             | Default Applicability    |
| ----------------- | ------------------------------------- | ------------------------ |
| `type-enum`       | `type` is found in value              | `always`                 |
| `type-case`       | `type` is in case `value`             | `always`, `'lower-case'` |
| `type-empty`      | `type` is empty                       | `never`                  |
| `type-max-length` | `type` has `value` or less characters | `always`, `Infinity`     |
| `type-min-length` | `type` has `value` or more characters | `always`, `0`            |

### Subject Rules

| Rule                       | Condition                                | Default Applicability |
| -------------------------- | ---------------------------------------- | --------------------- |
| `subject-case`             | `subject` is in case `value`             | `always`              |
| `subject-empty`            | `subject` is empty                       | `never`               |
| `subject-full-stop`        | `subject` ends with `value`              | `never`, `'.'`        |
| `subject-max-length`       | `subject` has `value` or less characters | `always`, `Infinity`  |
| `subject-min-length`       | `subject` has `value` or more characters | `always`, `0`         |
| `subject-exclamation-mark` | `subject` has exclamation before `:`     | `never`               |

### Scope Rules

| Rule               | Condition                              | Default Applicability    |
| ------------------ | -------------------------------------- | ------------------------ |
| `scope-enum`       | `scope` is found in value              | `always`, `[]`           |
| `scope-case`       | `scope` is in case `value`             | `always`, `'lower-case'` |
| `scope-empty`      | `scope` is empty                       | `never`                  |
| `scope-max-length` | `scope` has `value` or less characters | `always`, `Infinity`     |
| `scope-min-length` | `scope` has `value` or more characters | `always`, `0`            |

### Header Rules

| Rule                | Condition                                   | Default Applicability    |
| ------------------- | ------------------------------------------- | ------------------------ |
| `header-case`       | `header` is in case `value`                 | `always`, `'lower-case'` |
| `header-full-stop`  | `header` ends with `value`                  | `never`, `'.'`           |
| `header-max-length` | `header` has `value` or less characters     | `always`, `72`           |
| `header-min-length` | `header` has `value` or more characters     | `always`, `0`            |
| `header-trim`       | `header` has no leading/trailing whitespace | `always`                 |

### Body Rules

| Rule                   | Condition                                                    | Default Applicability    |
| ---------------------- | ------------------------------------------------------------ | ------------------------ |
| `body-leading-blank`   | `body` begins with blank line                                | `always`                 |
| `body-empty`           | `body` is empty                                              | `never`                  |
| `body-max-length`      | `body` has `value` or less characters                        | `always`, `Infinity`     |
| `body-max-line-length` | `body` lines have `value` or less characters (URLs excluded) | `always`, `Infinity`     |
| `body-min-length`      | `body` has `value` or more characters                        | `always`, `0`            |
| `body-case`            | `body` is in case `value`                                    | `always`, `'lower-case'` |
| `body-full-stop`       | `body` ends with `value`                                     | `never`, `'.'`           |

### Footer Rules

| Rule                     | Condition                                      | Default Applicability |
| ------------------------ | ---------------------------------------------- | --------------------- |
| `footer-leading-blank`   | `footer` begins with blank line                | `always`              |
| `footer-empty`           | `footer` is empty                              | `never`               |
| `footer-max-length`      | `footer` has `value` or less characters        | `always`, `Infinity`  |
| `footer-max-line-length` | `footer` lines have `value` or less characters | `always`, `Infinity`  |
| `footer-min-length`      | `footer` has `value` or more characters        | `always`, `0`         |

### Case Values

For rules that check case (`*-case`):

```javascript
[
  'lower-case',    // lowercase
  'upper-case',    // UPPERCASE
  'camel-case',    // camelCase
  'kebab-case',    // kebab-case
  'pascal-case',   // PascalCase
  'sentence-case', // Sentence case
  'snake-case',    // snake_case
  'start-case',    // Start Case
]
```

## Programmatic Usage

### Load Configuration

```javascript
import load from '@commitlint/load';

async function getCommitlintConfig() {
  const config = await load();
  console.log(config.rules);
  return config;
}
```

### Validate Message

```javascript
import load from '@commitlint/load';
import lint from '@commitlint/lint';

async function validateMessage(message) {
  const config = await load();
  const result = await lint(message, config.rules);

  return {
    valid: result.valid,
    errors: result.errors,
    warnings: result.warnings,
  };
}
```

## LLM Integration Patterns

### Extract Rules for Prompt Generation

Generate LLM-friendly constraints from commitlint config:

```python
def extract_rules_for_prompt(config: dict) -> str:
    """Extract commitlint rules into LLM-friendly format."""
    rules = config.get('rules', {})
    prompt_parts = []

    # Extract type-enum if present
    if 'type-enum' in rules:
        level, applicability, types = rules['type-enum']
        if level > 0 and applicability == 'always':
            prompt_parts.append(f"Allowed commit types: {', '.join(types)}")

    # Extract scope-enum if present
    if 'scope-enum' in rules:
        level, applicability, scopes = rules['scope-enum']
        if level > 0 and applicability == 'always' and scopes:
            prompt_parts.append(f"Allowed scopes: {', '.join(scopes)}")

    # Extract header-max-length
    if 'header-max-length' in rules:
        level, applicability, length = rules['header-max-length']
        if level > 0:
            prompt_parts.append(f"Header must be {length} characters or less")

    # Extract subject-case
    if 'subject-case' in rules:
        level, applicability, cases = rules['subject-case']
        if level > 0 and applicability == 'never':
            prompt_parts.append(f"Subject must NOT use: {', '.join(cases)}")

    return '\n'.join(prompt_parts)
```

### Validation Loop

```python
import subprocess

async def validate_with_commitlint(message: str, cwd: Path | None = None) -> tuple[bool, list[str]]:
    """
    Validate commit message with commitlint.

    Args:
        message: The commit message to validate
        cwd: Working directory (defaults to current directory)

    Returns:
        Tuple of (is_valid, error_messages)
    """
    result = subprocess.run(
        ['npx', 'commitlint'],
        input=message,
        capture_output=True,
        text=True,
        cwd=cwd,
    )

    if result.returncode == 0:
        return True, []

    # Parse errors from stderr
    errors = [line.strip() for line in result.stderr.split('\n') if line.strip()]
    return False, errors
```

**Validation loop pattern:**

1. LLM generates commit message based on diff and rules
2. Run commitlint on generated message
3. If validation fails, feed errors back to LLM with context
4. Retry (max 3 times by default)
5. Return final message (valid or best effort after retries)

## Common Issues

**Node v24 ESM issues:**

Use `.mjs` extension for ES modules config, or add `"type": "module"` to package.json

**Missing extends:**

Config without `extends` or `rules` fails with "Please add rules" error. Include at least one:

```javascript
export default {
  extends: ['@commitlint/config-conventional'],
};
```

**Empty config error:**

Config file must have at least `extends` or `rules` defined.

**Scope enum empty array:**

`scope-enum` with `[]` passes all scopes. Use specific array to restrict:

```javascript
rules: {
  'scope-enum': [2, 'always', ['api', 'ui', 'docs']],
}
```

**Subject case trap:**

`@commitlint/config-conventional` uses `never` with specific cases, meaning those cases are forbidden (not required):

```javascript
// This forbids sentence-case, start-case, pascal-case, upper-case
'subject-case': [2, 'never', ['sentence-case', 'start-case', 'pascal-case', 'upper-case']]
```

## Pre-commit Integration

For pre-commit hook integration with commitlint, activate the pre-commit skill:

```text
Skill(command: "pre-commit")
```

## Conventional Commits Reference

For Conventional Commits format specification and examples, activate the conventional-commits skill:

```text
Skill(command: "conventional-commits")
```

## References

### Official Documentation

- [Commitlint Official Site](https://commitlint.js.org/) (accessed 2025-01-15)
- [Configuration Reference](https://commitlint.js.org/reference/configuration.html) (accessed 2025-01-15)
- [Rules Reference](https://commitlint.js.org/reference/rules.html) (accessed 2025-01-15)
- [CLI Reference](https://commitlint.js.org/reference/cli.html) (accessed 2025-01-15)
- [Getting Started Guide](https://commitlint.js.org/guides/getting-started.html) (accessed 2025-01-15)
- [GitHub Repository](https://github.com/conventional-changelog/commitlint) (accessed 2025-01-15)

### Related Specifications

- [Conventional Commits](https://www.conventionalcommits.org/) - Commit message format specification
- [Cosmiconfig](https://github.com/cosmiconfig/cosmiconfig) - Configuration file discovery mechanism

### Source Attribution

This skill was created from reference documentation at `the commit-polish repository` (2025-12-01)
