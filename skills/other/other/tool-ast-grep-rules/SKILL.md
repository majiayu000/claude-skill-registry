---
name: tool-ast-grep-rules
description: 'Write AST-based code search and rewrite rules using ast-grep YAML. Create linting rules, code modernizations, and API migrations with auto-fix. Use when the user mentions ast-grep, tree-sitter patterns, code search rules, lint rules with YAML, AST matching, or code refactoring patterns.'
---

# ast-grep Rule Crafter

ast-grep uses tree-sitter to parse code into AST, enabling precise pattern matching. Rules are defined in YAML for linting, searching, and rewriting code.

## Quick Start

```yaml
id: no-console-log
language: JavaScript
rule:
  pattern: console.log($$$ARGS)
fix: logger.log($$$ARGS)
message: Replace console.log with logger
```

## Project Configuration

Project-level scanning requires an `sgconfig.yml` configuration file:

```yaml
# sgconfig.yml (project root)
ruleDirs:
  - rules          # Rule directory, recursively loads all .yml files
```

Typical project structure:

```
my-project/
├── sgconfig.yml
├── rules/
│   ├── no-console.yml
│   └── custom/
│       └── team-rules.yml
└── src/
```

Running project scan:

```bash
ast-grep scan              # Automatically finds sgconfig.yml
ast-grep scan --config path/to/sgconfig.yml  # Specify config
```

> **Note**: `ast-grep scan` command requires `sgconfig.yml`, while `ast-grep run -p` can be used standalone.

## Rule Workflow

### Lint Rule (Common)

Check only without fixing, used for CI/editor hints:

```yaml
# rules/no-console-log.yml
id: no-console-log
language: JavaScript
severity: warning
message: Avoid console.log in production code
rule:
  pattern: console.log($$$ARGS)
```

Verify:

```bash
ast-grep scan -r rules/no-console-log.yml src/
```

### Rewrite Rule (Optional)

Add `fix` when auto-fix is needed:

```yaml
id: no-console-log
language: JavaScript
severity: warning
message: Replace console.log with logger
rule:
  pattern: console.log($$$ARGS)
fix: logger.log($$$ARGS)
```

Apply fix:

```bash
ast-grep scan -r rules/no-console-log.yml --update-all src/
```

### Development Workflow

```
- [ ] 1. Explore pattern with CLI: ast-grep -p 'pattern' src/
- [ ] 2. Create rule file (.yml)
- [ ] 3. Verify: ast-grep scan -r rule.yml src/
- [ ] 4. If false positives → add constraints → re-verify
```

Debug AST structure:

```bash
ast-grep -p 'console.log($ARG)' --debug-query ast
```

## Essential Syntax

| Element | Syntax | Example |
|---------|--------|---------|
| Single node | `$VAR` | `console.log($MSG)` |
| Multiple nodes | `$$$ARGS` | `fn($$$ARGS)` |
| Same content | Use same name | `$A == $A` |
| Non-capturing | `$_VAR` | `$_FN($_FN)` |

## Core Rules Quick Reference

| Type | Purpose | Example |
|------|---------|---------|
| `pattern` | Match code structure | `pattern: if ($COND) {}` |
| `kind` | Match AST node type | `kind: function_declaration` |
| `all` | Match ALL conditions | `all: [pattern: X, kind: Y]` |
| `any` | Match ANY condition | `any: [pattern: var $A, pattern: let $A]` |
| `not` | Exclude matches | `not: {pattern: safe_call()}` |
| `has` | Must have child | `has: {kind: return_statement}` |
| `inside` | Must be in ancestor | `inside: {kind: class_body}` |

## Detailed References

**Complete syntax guide**: See [rule-syntax.md](rule-syntax.md)
- Atomic rules (pattern, kind, regex, nthChild, range)
- Composite rules (all, any, not, matches)
- Relational rules (has, inside, follows, precedes)
- Transform and fixConfig

**Language-specific patterns**: See [common-patterns.md](common-patterns.md)
- JavaScript/TypeScript examples
- Python examples
- Go and Rust examples

## Supported Languages

Bash, C, Cpp, CSharp, Css, Elixir, Go, Haskell, Hcl, Html, Java, JavaScript, Json, Kotlin, Lua, Nix, Php, Python, Ruby, Rust, Scala, Solidity, Swift, Tsx, TypeScript, Yaml
