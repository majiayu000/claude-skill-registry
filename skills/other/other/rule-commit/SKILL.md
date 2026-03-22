---
name: rule-commit
description: 'Rule mapping for commit'
---

# Rule commit

Apply this rule whenever work touches:
- `*`

All commits in this repository follow the [Conventional Commits](https://www.conventionalcommits.org/) specification. This enables automated changelog generation and makes the history easy to scan.

### Format

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

### Types

| Type       | When to use                                    |
|------------|------------------------------------------------|
| `feat`     | A new feature or capability                    |
| `fix`      | A bug fix                                      |
| `docs`     | Documentation-only changes                     |
| `style`    | Formatting, whitespace, semicolons (no logic)  |
| `refactor` | Code restructuring without behavior change     |
| `perf`     | Performance improvement                        |
| `test`     | Adding or updating tests                       |
| `chore`    | Build scripts, CI config, tooling              |
| `revert`   | Reverting a previous commit                    |

### Scopes

- **nx** - Nx workspace configuration, project.json, generators
- **rule** - Rule processor logic and related files
- **shared** - Shared libraries under `libs/shared/`
- **script** - Tooling scripts under `tools/`

### Examples

```
feat(rule): add vehicle definition validation
fix(shared): prevent racing of requests
refactor(nx): consolidate build targets
test(rule): add edge cases for weight threshold
chore(script): update create-rule template
```

### Interactive commit

Run `pnpm commit` to use the interactive prompt which enforces the format automatically.
