---
name: ast-grep
description: Effective code search, analysis, and refactoring using ast-grep (sg). Use this skill for precise AST-based code modifications, structural search, and linting.
---

# ast-grep (sg)

ast-grep is a fast and polyglot tool for code searching, linting, and rewriting based on Abstract Syntax Trees (AST). It excels at structural search and replace where regex fails.

## When to use

- **Structural Search**: Finding code based on structure (e.g., "all function calls to `foo` with 2 arguments") regardless of whitespace.
- **Refactoring**: Renaming variables, changing function signatures, or transforming code patterns safely.
- **Linting**: Creating custom rules to enforce code style or best practices.
- **Code Analysis**: Extracting information from codebases.

## Quick Start

### CLI Basics

```bash
# Search (pattern must be in single quotes)
ast-grep -p '$A + $B' --lang ts

# Rewrite (dry run)
ast-grep -p '$A != null' --rewrite '$A' --lang ts

# Interactive Rewrite
ast-grep -p 'var $A = $B' --rewrite 'const $A = $B' --interactive
```

### Pattern Syntax
- **Meta-variables**: `$VAR` matches any single node.
- **Multi-meta-variables**: `$$$ARGS` matches zero or more nodes (list of items).
- **Wildcard**: `$_` matches any node (non-capturing).
- **Anonymous**: `$$` matches any list of nodes (non-capturing).

See [Pattern Syntax](references/pattern-syntax.md) for details.

## Core Concepts

Understanding **Named vs Unnamed nodes** and **Matching Strictness** is crucial for precise patterns.

- **Named Nodes**: `identifier`, `function_definition` (matched by `$VAR`).
- **Unnamed Nodes**: `(`, `)`, `;` (skipped by default in `smart` mode).
- **Strictness**: Control matching precision (`smart`, `cst`, `ast`, `relaxed`, `signature`).

See [Core Concepts](references/core-concepts.md) for details.

## Rule Configuration (YAML)

For complex tasks, use YAML configuration files.

```yaml
id: no-console-log
language: TypeScript
rule:
  pattern: console.log($$$ARGS)
  inside:
    kind: function_declaration
    stopBy: end
fix: '' # Remove the log
```

See [Rule Configuration](references/rule-config.md) for details.

## Advanced Rewriting

ast-grep supports complex transformations (regex replace, case conversion) and rewriters for sub-node transformation.

See [Rewriting & Transformations](references/rewriting.md) for details.

## Project Setup & Testing

For larger projects, organize rules and tests using `sgconfig.yml`.

- **Scaffold**: `ast-grep new project`
- **Config**: `sgconfig.yml` defines rule and test directories.
- **Testing**: Define `valid` and `invalid` cases to ensure rule accuracy.

See [Project Setup & Testing](references/project-setup.md) for details.

## Utility Rules

Reuse logic with local or global utility rules. Enables recursive matching.

```yaml
utils:
  is-literal:
    any: [{kind: string}, {kind: number}]
rule:
  matches: is-literal
```

See [Utility Rules](references/utility-rules.md) for details.

## Configuration Reference

Full reference for YAML fields (`id`, `severity`, `files`, `ignores`) and supported languages.

See [Configuration Reference](references/yaml-reference.md) for details.

## CLI Reference

Common commands: `scan`, `run`, `new`, `test`, `lsp`.

See [CLI Reference](references/cli.md) for details.
