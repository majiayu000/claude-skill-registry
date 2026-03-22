---
name: commit
description: Conventional commit message formatting. Use when creating git commits to ensure messages follow the project's conventional commit style with proper type, scope, and description.
compatibility: Designed for Claude Code
metadata:
  author: oxc-react-compiler
  version: "1.0"
---

# Conventional Commits

## Format

```
<type>(<scope>): <description>
                                        ← blank line
<body>
```

- **type**: required, lowercase
- **scope**: optional, in parentheses, lowercase
- **description**: required, lowercase start, imperative mood, no period
- **body**: optional, separated by blank line, free-form with bullet lists

## Types

| Type       | When to use                                             |
| ---------- | ------------------------------------------------------- |
| `feat`     | New compiler pass, HIR type, lint rule, or feature      |
| `fix`      | Bug fix                                                 |
| `chore`    | Tooling, config, deps, no production code change        |
| `docs`     | Documentation only                                      |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `deps`     | Dependency additions or updates                         |
| `test`     | Adding or updating tests                                |
| `ci`       | CI/CD pipeline changes                                  |
| `perf`     | Performance improvement                                 |
| `style`    | Formatting, whitespace (no logic change)                |

## Scope

Derive from the primary area of change:

- **HIR**: `hir`, `build-hir`, `environment`, `globals`, `object-shape`
- **SSA**: `ssa`
- **Optimization**: `optimization`, `const-prop`, `dce`, `inline-iife`
- **Inference**: `inference`, `infer-types`, `mutation-analysis`, `aliasing`
- **Reactive Scopes**: `reactive-scopes`, `scope-inference`, `scope-alignment`, `codegen`
- **Validation**: `validation`, `hooks`, `refs`, `effects`
- **Pipeline**: `pipeline`, `program`, `options`
- **Lint**: `lint`, `lint-rules`
- **NAPI/Plugin**: `napi`, `vite-plugin`
- **Utils**: `disjoint-set`, `utils`
- Omit scope for broad cross-cutting changes

## Rules

1. Use imperative mood: "add feature" not "added feature" or "adds feature"
2. Keep the first line under 72 characters
3. Start description lowercase
4. No trailing period
5. One commit per logical change — don't mix unrelated changes

## Examples

### One-liners (small, focused changes)

```
feat(hir): add InstructionValue enum with 40 variants
fix(ssa): handle redundant phi elimination for loop headers
chore(deps): update oxc crates to 0.50
feat(validation): implement validate_hooks_usage pass
```

### With body (multi-file or multi-step changes)

```
feat(inference): implement infer_mutation_aliasing_effects pass

- Build abstract heap model with pointer graph and ValueKind per value
- Fixpoint iteration to propagate effects through aliases
- Compute candidate effects based on instruction kind and operand types
- Record final AliasingEffect annotations on each instruction
```

```
feat(reactive-scopes): implement scope inference and alignment

- DisjointSet-based scope grouping in infer_reactive_scope_variables
- Align scopes to block boundaries
- Merge overlapping scopes with shared reactive operands
- Build reactive scope terminals for codegen
```

```
feat(build-hir): implement OXC AST to HIR lowering

- Walk oxc_ast Statement/Expression nodes
- Flatten nested expressions into temporaries with Places
- Convert control flow to explicit BasicBlock edges
- Handle JSX, hooks, destructuring, and closures
```

### Body style guidelines

- Use bullet lists (`-`) for discrete changes
- Use prose paragraphs for narrative summaries of larger features
- Group related bullets under subheadings when mixing concerns (e.g. "Fixes:")
- Keep body lines under 72 characters
