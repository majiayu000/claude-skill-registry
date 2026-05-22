---
name: ast-grep
description: ast-grep rule writing and usage best practices. This skill should be used when writing, reviewing, or debugging ast-grep rules for code search, linting, and transformation. Triggers on tasks involving YAML rules, pattern syntax, meta variables, constraints, or code rewriting.
---

# ast-grep Community Best Practices

Comprehensive best practices guide for ast-grep rule writing and usage, maintained by the ast-grep community. Contains 46 rules across 8 categories, prioritized by impact to guide automated rule generation and code transformation.

## When to Apply

Reference these guidelines when:
- Writing new ast-grep rules for linting or search
- Debugging patterns that don't match expected code
- Optimizing rule performance for large codebases
- Setting up ast-grep projects with proper organization
- Reviewing ast-grep rules for correctness and maintainability

## General Workflow

Follow this workflow when creating ast-grep rules for code search:

### Step 1: Understand the Query

Clarify what you want to find:
- Target programming language
- Edge cases to handle
- What to include vs exclude

### Step 2: Create Example Code

Write a sample code snippet representing the desired match pattern.

### Step 3: Write the ast-grep Rule

Choose the right approach:
- Use `pattern` for simple structures
- Use `kind` with `has`/`inside` for complex structures
- Combine with `all`, `any`, or `not` for compound queries
- **Always use `stopBy: end` for relational rules** (`inside`, `has`) to ensure complete search

### Step 4: Test the Rule

```bash
# Inspect AST structure
ast-grep run --pattern '[code]' --lang [language] --debug-query=ast

# Test inline rule
echo "[code]" | ast-grep scan --inline-rules "[rule]" --stdin

# Test from file
ast-grep scan --rule [file.yml] [path]
```

### Step 5: Search the Codebase

Deploy the validated rule:
```bash
# Search with pattern (simple matches)
ast-grep run --pattern '[pattern]' --lang [language] [path]

# Search with rule file (complex queries)
ast-grep scan --rule [file.yml] [path]

# Apply fixes interactively
ast-grep scan --rule [file.yml] --interactive [path]
```

### Quick Tips

1. **Always use `stopBy: end`** - Ensures complete subtree traversal for relational rules
2. **Start simple, add complexity** - Begin with patterns, progress to kinds, then relational rules
3. **Debug with AST inspection** - Use `--debug-query=ast` to verify structure matching
4. **Escape in inline rules** - Use `\$VAR` or single quotes for shell commands
5. **Test in playground first** - Use https://ast-grep.github.io/playground.html for rapid iteration

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Pattern Correctness | CRITICAL | `pattern-` |
| 2 | Meta Variable Usage | CRITICAL | `meta-` |
| 3 | Rule Composition | HIGH | `compose-` |
| 4 | Constraint Design | HIGH | `const-` |
| 5 | Rewrite Correctness | MEDIUM-HIGH | `rewrite-` |
| 6 | Project Organization | MEDIUM | `org-` |
| 7 | Performance Optimization | MEDIUM | `perf-` |
| 8 | Testing & Debugging | LOW-MEDIUM | `test-` |

## Quick Reference

### 1. Pattern Correctness (CRITICAL)

- [`pattern-valid-syntax`](references/pattern-valid-syntax.md) - Use valid parseable code as patterns
- [`pattern-language-aware`](references/pattern-language-aware.md) - Account for language-specific syntax differences
- [`pattern-context-selector`](references/pattern-context-selector.md) - Use context and selector for code fragments
- [`pattern-avoid-comments-strings`](references/pattern-avoid-comments-strings.md) - Avoid matching inside comments and strings
- [`pattern-strictness-levels`](references/pattern-strictness-levels.md) - Configure pattern strictness appropriately
- [`pattern-kind-vs-pattern`](references/pattern-kind-vs-pattern.md) - Choose kind or pattern based on specificity needs
- [`pattern-debug-ast`](references/pattern-debug-ast.md) - Use debug query to inspect AST structure
- [`pattern-nthchild-matching`](references/pattern-nthchild-matching.md) - Use nthChild for index-based positional matching
- [`pattern-range-matching`](references/pattern-range-matching.md) - Use range for character position matching

### 2. Meta Variable Usage (CRITICAL)

- [`meta-naming-convention`](references/meta-naming-convention.md) - Follow meta variable naming conventions
- [`meta-single-node`](references/meta-single-node.md) - Match single AST nodes with meta variables
- [`meta-reuse-binding`](references/meta-reuse-binding.md) - Reuse meta variables to enforce equality
- [`meta-underscore-noncapture`](references/meta-underscore-noncapture.md) - Use underscore prefix for non-capturing matches
- [`meta-named-vs-unnamed`](references/meta-named-vs-unnamed.md) - Use double dollar for unnamed node matching
- [`meta-multi-match-lazy`](references/meta-multi-match-lazy.md) - Understand multi-match variables are lazy

### 3. Rule Composition (HIGH)

- [`compose-all-for-and-logic`](references/compose-all-for-and-logic.md) - Use all for AND logic between rules
- [`compose-any-for-or-logic`](references/compose-any-for-or-logic.md) - Use any for OR logic between rules
- [`compose-not-for-exclusion`](references/compose-not-for-exclusion.md) - Use not for exclusion patterns
- [`compose-inside-for-context`](references/compose-inside-for-context.md) - Use inside for contextual matching
- [`compose-has-for-children`](references/compose-has-for-children.md) - Use has for child node requirements
- [`compose-matches-for-reuse`](references/compose-matches-for-reuse.md) - Use matches for rule reusability
- [`compose-precedes-follows`](references/compose-precedes-follows.md) - Use precedes and follows for sequential positioning
- [`compose-field-targeting`](references/compose-field-targeting.md) - Use field to target specific sub-nodes

### 4. Constraint Design (HIGH)

- [`const-kind-filter`](references/const-kind-filter.md) - Use kind constraints to filter meta variables
- [`const-regex-filter`](references/const-regex-filter.md) - Use regex constraints for text patterns
- [`const-not-inside-not`](references/const-not-inside-not.md) - Avoid constraints inside not rules
- [`const-pattern-constraint`](references/const-pattern-constraint.md) - Use pattern constraints for structural filtering
- [`const-post-match-timing`](references/const-post-match-timing.md) - Understand constraints apply after matching

### 5. Rewrite Correctness (MEDIUM-HIGH)

- [`rewrite-preserve-semantics`](references/rewrite-preserve-semantics.md) - Preserve program semantics in rewrites
- [`rewrite-meta-variable-reference`](references/rewrite-meta-variable-reference.md) - Reference all necessary meta variables in fix
- [`rewrite-transform-operations`](references/rewrite-transform-operations.md) - Use transform for complex rewrites
- [`rewrite-test-before-deploy`](references/rewrite-test-before-deploy.md) - Test rewrites on representative code
- [`rewrite-syntax-validity`](references/rewrite-syntax-validity.md) - Ensure fix templates produce valid syntax

### 6. Project Organization (MEDIUM)

- [`org-project-structure`](references/org-project-structure.md) - Use standard project directory structure
- [`org-unique-rule-ids`](references/org-unique-rule-ids.md) - Use unique descriptive rule IDs
- [`org-severity-levels`](references/org-severity-levels.md) - Assign appropriate severity levels
- [`org-file-filtering`](references/org-file-filtering.md) - Use file filtering for targeted rules
- [`org-message-clarity`](references/org-message-clarity.md) - Write clear actionable messages

### 7. Performance Optimization (MEDIUM)

- [`perf-specific-patterns`](references/perf-specific-patterns.md) - Use specific patterns over generic ones
- [`perf-stopby-boundaries`](references/perf-stopby-boundaries.md) - Use stopBy to limit search depth
- [`perf-thread-parallelism`](references/perf-thread-parallelism.md) - Leverage parallel scanning with threads
- [`perf-avoid-regex-heavy`](references/perf-avoid-regex-heavy.md) - Avoid heavy regex in hot paths

### 8. Testing & Debugging (LOW-MEDIUM)

- [`test-valid-invalid-cases`](references/test-valid-invalid-cases.md) - Write both valid and invalid test cases
- [`test-snapshot-updates`](references/test-snapshot-updates.md) - Use snapshot testing for fix verification
- [`test-playground-first`](references/test-playground-first.md) - Test patterns in playground first
- [`test-edge-cases`](references/test-edge-cases.md) - Test edge cases and boundary conditions

## How to Use

Read individual reference files for detailed explanations and code examples:

- [Section definitions](references/_sections.md) - Category structure and impact levels
- [Rule template](assets/templates/_template.md) - Template for adding new rules

## Full Compiled Document

- [AGENTS.md](AGENTS.md) - Complete compiled guide with all rules

## Reference Files

| File | Description |
|------|-------------|
| [AGENTS.md](AGENTS.md) | Complete compiled guide with all rules |
| [references/_sections.md](references/_sections.md) | Category definitions and ordering |
| [assets/templates/_template.md](assets/templates/_template.md) | Template for new rules |
| [metadata.json](metadata.json) | Version and reference information |
