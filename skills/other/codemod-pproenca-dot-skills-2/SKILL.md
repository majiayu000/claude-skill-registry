---
name: codemod
description: Codemod (JSSG, ast-grep, workflows) best practices for writing efficient, safe, and maintainable code transformations. This skill should be used when writing, reviewing, or debugging codemods, AST transformations, or automated refactoring tools. Triggers on tasks involving codemod, ast-grep, JSSG, code transformation, or automated migration.
---

# Codemod Best Practices

Comprehensive best practices guide for Codemod (JSSG, ast-grep, workflows), designed for AI agents and LLMs. Contains 48 rules across 11 categories, prioritized by impact to guide automated refactoring and code generation.

## When to Apply

Reference these guidelines when:
- Writing new codemods with JSSG or ast-grep
- Designing workflow configurations for migrations
- Debugging pattern matching or AST traversal issues
- Reviewing codemod code for performance and safety
- Setting up test fixtures for transform validation

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | AST Understanding | CRITICAL | `ast-` |
| 2 | Pattern Efficiency | CRITICAL | `pattern-` |
| 3 | Parsing Strategy | CRITICAL | `parse-` |
| 4 | Node Traversal | HIGH | `traverse-` |
| 5 | Semantic Analysis | HIGH | `semantic-` |
| 6 | Edit Operations | MEDIUM-HIGH | `edit-` |
| 7 | Workflow Design | MEDIUM-HIGH | `workflow-` |
| 8 | Testing Strategy | MEDIUM | `test-` |
| 9 | State Management | MEDIUM | `state-` |
| 10 | Security and Capabilities | LOW-MEDIUM | `security-` |
| 11 | Package Structure | LOW | `pkg-` |

## Quick Reference

### 1. AST Understanding (CRITICAL)

- [`ast-explore-before-writing`](references/ast-explore-before-writing.md) - Use AST Explorer before writing patterns
- [`ast-understand-named-vs-anonymous`](references/ast-understand-named-vs-anonymous.md) - Understand named vs anonymous nodes
- [`ast-use-kind-for-precision`](references/ast-use-kind-for-precision.md) - Use kind constraint for precision
- [`ast-field-access-for-structure`](references/ast-field-access-for-structure.md) - Use field access for structural queries
- [`ast-check-null-before-access`](references/ast-check-null-before-access.md) - Check null before property access

### 2. Pattern Efficiency (CRITICAL)

- [`pattern-use-meta-variables`](references/pattern-use-meta-variables.md) - Use meta variables for flexible matching
- [`pattern-avoid-overly-generic`](references/pattern-avoid-overly-generic.md) - Avoid overly generic patterns
- [`pattern-combine-with-rules`](references/pattern-combine-with-rules.md) - Combine patterns with rule operators
- [`pattern-use-constraints`](references/pattern-use-constraints.md) - Use constraints for reusable matching logic
- [`pattern-use-relational-patterns`](references/pattern-use-relational-patterns.md) - Use relational patterns for context
- [`pattern-ensure-idempotency`](references/pattern-ensure-idempotency.md) - Ensure patterns are idempotent

### 3. Parsing Strategy (CRITICAL)

- [`parse-select-correct-parser`](references/parse-select-correct-parser.md) - Select the correct parser for file type
- [`parse-handle-embedded-languages`](references/parse-handle-embedded-languages.md) - Handle embedded languages with parseAsync
- [`parse-provide-pattern-context`](references/parse-provide-pattern-context.md) - Provide context for ambiguous patterns
- [`parse-early-return-non-applicable`](references/parse-early-return-non-applicable.md) - Early return for non-applicable files

### 4. Node Traversal (HIGH)

- [`traverse-use-find-vs-findall`](references/traverse-use-find-vs-findall.md) - Use find() for single match, findAll() for multiple
- [`traverse-single-pass-collection`](references/traverse-single-pass-collection.md) - Collect multiple patterns in single traversal
- [`traverse-use-stopby-for-depth`](references/traverse-use-stopby-for-depth.md) - Use stopBy to control traversal depth
- [`traverse-use-siblings-efficiently`](references/traverse-use-siblings-efficiently.md) - Use sibling navigation efficiently
- [`traverse-cache-repeated-lookups`](references/traverse-cache-repeated-lookups.md) - Cache repeated node lookups

### 5. Semantic Analysis (HIGH)

- [`semantic-use-file-scope-first`](references/semantic-use-file-scope-first.md) - Use file scope semantic analysis first
- [`semantic-check-null-results`](references/semantic-check-null-results.md) - Handle null semantic analysis results
- [`semantic-verify-file-ownership`](references/semantic-verify-file-ownership.md) - Verify file ownership before cross-file edits
- [`semantic-cache-cross-file-results`](references/semantic-cache-cross-file-results.md) - Cache semantic analysis results

### 6. Edit Operations (MEDIUM-HIGH)

- [`edit-batch-before-commit`](references/edit-batch-before-commit.md) - Batch edits before committing
- [`edit-preserve-formatting`](references/edit-preserve-formatting.md) - Preserve surrounding formatting in edits
- [`edit-handle-overlapping-ranges`](references/edit-handle-overlapping-ranges.md) - Handle overlapping edit ranges
- [`edit-use-flatmap-for-conditional`](references/edit-use-flatmap-for-conditional.md) - Use flatMap for conditional edits
- [`edit-add-imports-correctly`](references/edit-add-imports-correctly.md) - Add imports at correct position

### 7. Workflow Design (MEDIUM-HIGH)

- [`workflow-order-nodes-by-dependency`](references/workflow-order-nodes-by-dependency.md) - Order nodes by dependency
- [`workflow-use-matrix-for-parallelism`](references/workflow-use-matrix-for-parallelism.md) - Use matrix strategy for parallelism
- [`workflow-use-manual-gates`](references/workflow-use-manual-gates.md) - Use manual gates for critical steps
- [`workflow-validate-before-run`](references/workflow-validate-before-run.md) - Validate workflows before running
- [`workflow-use-conditional-steps`](references/workflow-use-conditional-steps.md) - Use conditional steps for dynamic workflows

### 8. Testing Strategy (MEDIUM)

- [`test-use-fixture-pairs`](references/test-use-fixture-pairs.md) - Use input/expected fixture pairs
- [`test-cover-edge-cases`](references/test-cover-edge-cases.md) - Cover edge cases in test fixtures
- [`test-use-strictness-levels`](references/test-use-strictness-levels.md) - Choose appropriate test strictness level
- [`test-update-fixtures-intentionally`](references/test-update-fixtures-intentionally.md) - Update test fixtures intentionally
- [`test-run-on-subset-first`](references/test-run-on-subset-first.md) - Test on file subset before full run

### 9. State Management (MEDIUM)

- [`state-use-for-resumability`](references/state-use-for-resumability.md) - Use state for resumable migrations
- [`state-make-transforms-idempotent`](references/state-make-transforms-idempotent.md) - Make transforms idempotent for safe reruns
- [`state-log-progress-for-observability`](references/state-log-progress-for-observability.md) - Log progress for long-running migrations

### 10. Security and Capabilities (LOW-MEDIUM)

- [`security-minimize-capabilities`](references/security-minimize-capabilities.md) - Minimize requested capabilities
- [`security-validate-external-inputs`](references/security-validate-external-inputs.md) - Validate external inputs before use
- [`security-review-before-running-third-party`](references/security-review-before-running-third-party.md) - Review third-party codemods before running

### 11. Package Structure (LOW)

- [`pkg-use-semantic-versioning`](references/pkg-use-semantic-versioning.md) - Use semantic versioning for packages
- [`pkg-write-descriptive-metadata`](references/pkg-write-descriptive-metadata.md) - Write descriptive package metadata
- [`pkg-organize-by-convention`](references/pkg-organize-by-convention.md) - Organize package by convention

## How to Use

Read individual reference files for detailed explanations and code examples:

- [Section definitions](references/_sections.md) - Category structure and impact levels
- [Rule template](assets/templates/_template.md) - Template for adding new rules

## Full Compiled Document

For a complete guide with all rules expanded, see [AGENTS.md](AGENTS.md).
