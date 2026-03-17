---
name: jscodeshift
description: jscodeshift codemod development best practices from Facebook/Meta. This skill should be used when writing, reviewing, or debugging jscodeshift codemods. Triggers on tasks involving AST transformation, code migration, automated refactoring, or codemod development.
---

# Facebook/Meta jscodeshift Best Practices

Comprehensive best practices guide for jscodeshift codemod development, designed for AI agents and LLMs. Contains 40 rules across 8 categories, prioritized by impact from critical (parser configuration, AST traversal) to incremental (advanced patterns). Each rule includes detailed explanations, real-world examples, and specific impact metrics.

## When to Apply

Reference these guidelines when:
- Writing new jscodeshift codemods for code migrations
- Debugging transform failures or unexpected behavior
- Optimizing codemod performance on large codebases
- Reviewing codemod code for correctness
- Testing codemods for edge cases and regressions

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Parser Configuration | CRITICAL | `parser-` |
| 2 | AST Traversal Patterns | CRITICAL | `traverse-` |
| 3 | Node Filtering | HIGH | `filter-` |
| 4 | AST Transformation | HIGH | `transform-` |
| 5 | Code Generation | MEDIUM | `codegen-` |
| 6 | Testing Strategies | MEDIUM | `test-` |
| 7 | Runner Optimization | LOW-MEDIUM | `runner-` |
| 8 | Advanced Patterns | LOW | `advanced-` |

## Quick Reference

### 1. Parser Configuration (CRITICAL)

- [`parser-typescript-config`](references/parser-typescript-config.md) - Use correct parser for TypeScript files
- [`parser-flow-annotation`](references/parser-flow-annotation.md) - Use Flow parser for Flow-typed code
- [`parser-babel5-compat`](references/parser-babel5-compat.md) - Avoid default babel5compat for modern syntax
- [`parser-export-declaration`](references/parser-export-declaration.md) - Export parser from transform module
- [`parser-astexplorer-match`](references/parser-astexplorer-match.md) - Match AST Explorer parser to jscodeshift parser

### 2. AST Traversal Patterns (CRITICAL)

- [`traverse-find-specific-type`](references/traverse-find-specific-type.md) - Use specific node types in find() calls
- [`traverse-two-pass-pattern`](references/traverse-two-pass-pattern.md) - Use two-pass pattern for complex transforms
- [`traverse-early-return`](references/traverse-early-return.md) - Return early when no transformation needed
- [`traverse-find-filter-pattern`](references/traverse-find-filter-pattern.md) - Use find() with filter object over filter() chain
- [`traverse-closest-scope`](references/traverse-closest-scope.md) - Use closestScope() for scope-aware transforms
- [`traverse-avoid-repeated-find`](references/traverse-avoid-repeated-find.md) - Avoid repeated find() calls for same node type

### 3. Node Filtering (HIGH)

- [`filter-path-parent-check`](references/filter-path-parent-check.md) - Check parent path before transformation
- [`filter-import-binding`](references/filter-import-binding.md) - Track import bindings for accurate usage detection
- [`filter-nullish-checks`](references/filter-nullish-checks.md) - Add nullish checks before property access
- [`filter-jsx-context`](references/filter-jsx-context.md) - Distinguish JSX context from regular JavaScript
- [`filter-computed-properties`](references/filter-computed-properties.md) - Handle computed property keys in filters

### 4. AST Transformation (HIGH)

- [`transform-builder-api`](references/transform-builder-api.md) - Use builder API for creating AST nodes
- [`transform-replacewith-callback`](references/transform-replacewith-callback.md) - Use replaceWith callback for context-aware transforms
- [`transform-insert-import`](references/transform-insert-import.md) - Insert imports at correct position
- [`transform-preserve-comments`](references/transform-preserve-comments.md) - Preserve comments when replacing nodes
- [`transform-renameto`](references/transform-renameto.md) - Use renameTo for variable renaming
- [`transform-remove-unused-imports`](references/transform-remove-unused-imports.md) - Remove unused imports after transformation

### 5. Code Generation (MEDIUM)

- [`codegen-tosource-options`](references/codegen-tosource-options.md) - Configure toSource() for consistent formatting
- [`codegen-preserve-style`](references/codegen-preserve-style.md) - Preserve original code style with recast
- [`codegen-template-literals`](references/codegen-template-literals.md) - Use template literals for complex node creation
- [`codegen-print-width`](references/codegen-print-width.md) - Set appropriate print width for long lines

### 6. Testing Strategies (MEDIUM)

- [`test-inline-snapshots`](references/test-inline-snapshots.md) - Use defineInlineTest for input/output verification
- [`test-negative-cases`](references/test-negative-cases.md) - Write negative test cases first
- [`test-dry-run-exploration`](references/test-dry-run-exploration.md) - Use dry run mode for codebase exploration
- [`test-fixture-files`](references/test-fixture-files.md) - Use fixture files for complex test cases
- [`test-parse-errors`](references/test-parse-errors.md) - Test for parse error handling

### 7. Runner Optimization (LOW-MEDIUM)

- [`runner-parallel-workers`](references/runner-parallel-workers.md) - Configure worker count for optimal parallelization
- [`runner-ignore-patterns`](references/runner-ignore-patterns.md) - Use ignore patterns to skip non-source files
- [`runner-extensions-filter`](references/runner-extensions-filter.md) - Filter files by extension
- [`runner-batch-processing`](references/runner-batch-processing.md) - Process large codebases in batches
- [`runner-verbose-output`](references/runner-verbose-output.md) - Use verbose output for debugging transforms

### 8. Advanced Patterns (LOW)

- [`advanced-compose-transforms`](references/advanced-compose-transforms.md) - Compose multiple transforms into pipelines
- [`advanced-scope-analysis`](references/advanced-scope-analysis.md) - Use scope analysis for safe variable transforms
- [`advanced-multi-file-state`](references/advanced-multi-file-state.md) - Share state across files with options
- [`advanced-custom-collections`](references/advanced-custom-collections.md) - Create custom collection methods

## How to Use

Read individual reference files for detailed explanations and code examples:

- [Section definitions](references/_sections.md) - Category structure and impact levels
- [Rule template](assets/templates/_template.md) - Template for adding new rules

## Full Compiled Document

For a single comprehensive document containing all rules, see [AGENTS.md](AGENTS.md).

## Reference Files

| File | Description |
|------|-------------|
| [AGENTS.md](AGENTS.md) | Complete compiled guide with all rules |
| [references/_sections.md](references/_sections.md) | Category definitions and ordering |
| [assets/templates/_template.md](assets/templates/_template.md) | Template for new rules |
| [metadata.json](metadata.json) | Version and reference information |
