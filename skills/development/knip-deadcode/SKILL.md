---
name: knip-deadcode-best-practices
description: Knip dead code detection best practices for JavaScript and TypeScript projects. Use when configuring Knip, analyzing unused code, setting up CI integration, or cleaning up codebases. Triggers on knip.json, dead code, unused exports, unused dependencies, bundle optimization.
---

# Community Knip Dead Code Detection Best Practices

Comprehensive guide for detecting and removing dead code in JavaScript and TypeScript projects using Knip. Contains 43 rules across 8 categories, prioritized by impact to guide configuration, CI integration, and cleanup workflows.

## When to Apply

Reference these guidelines when:
- Configuring Knip for a new project or monorepo
- Investigating false positives or false negatives
- Setting up CI pipelines to prevent dead code regressions
- Using auto-fix to clean up unused code
- Optimizing Knip performance for large codebases

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Configuration Foundations | CRITICAL | `config-` |
| 2 | Entry Point Strategy | CRITICAL | `entry-` |
| 3 | Workspace & Monorepo | HIGH | `workspace-` |
| 4 | Dependency Analysis | HIGH | `deps-` |
| 5 | Export Detection | MEDIUM-HIGH | `exports-` |
| 6 | CI Integration | MEDIUM | `ci-` |
| 7 | Auto-Fix Workflow | MEDIUM | `fix-` |
| 8 | Performance Optimization | LOW-MEDIUM | `perf-` |

## Quick Reference

### 1. Configuration Foundations (CRITICAL)

- [`config-avoid-broad-ignore`](references/config-avoid-broad-ignore.md) - Avoid broad ignore patterns
- [`config-configure-path-aliases`](references/config-configure-path-aliases.md) - Configure path aliases in Knip
- [`config-enable-plugins-explicitly`](references/config-enable-plugins-explicitly.md) - Enable framework plugins explicitly
- [`config-run-without-config`](references/config-run-without-config.md) - Run without config first for baseline
- [`config-separate-entry-project`](references/config-separate-entry-project.md) - Separate entry files from project files
- [`config-use-json-schema`](references/config-use-json-schema.md) - Use JSON schema for configuration validation
- [`config-use-negation-patterns`](references/config-use-negation-patterns.md) - Use negation patterns for exclusions
- [`config-use-production-mode`](references/config-use-production-mode.md) - Use production mode for shipping code analysis

### 2. Entry Point Strategy (CRITICAL)

- [`entry-add-dynamic-imports`](references/entry-add-dynamic-imports.md) - Add dynamic import targets as entry points
- [`entry-exclude-test-files`](references/entry-exclude-test-files.md) - Exclude test files from production entries
- [`entry-include-all-entry-points`](references/entry-include-all-entry-points.md) - Include all application entry points
- [`entry-include-bin-scripts`](references/entry-include-bin-scripts.md) - Include binary scripts as entry points
- [`entry-use-compilers`](references/entry-use-compilers.md) - Use compilers for non-standard file types
- [`entry-use-plugin-entries`](references/entry-use-plugin-entries.md) - Use plugin entry points for frameworks
- [`entry-verify-with-debug`](references/entry-verify-with-debug.md) - Verify entry points with debug mode

### 3. Workspace & Monorepo (HIGH)

- [`workspace-configure-root-workspace`](references/workspace-configure-root-workspace.md) - Configure root workspace explicitly
- [`workspace-ignore-specific`](references/workspace-ignore-specific.md) - Ignore specific workspaces when needed
- [`workspace-isolate-for-strict`](references/workspace-isolate-for-strict.md) - Isolate workspaces for strict dependency checking
- [`workspace-list-cross-deps`](references/workspace-list-cross-deps.md) - List cross-workspace dependencies explicitly
- [`workspace-per-workspace-plugins`](references/workspace-per-workspace-plugins.md) - Configure plugins per workspace
- [`workspace-use-workspace-globs`](references/workspace-use-workspace-globs.md) - Use workspace globs for consistent configuration

### 4. Dependency Analysis (HIGH)

- [`deps-add-unlisted-deps`](references/deps-add-unlisted-deps.md) - Add unlisted dependencies to package.json
- [`deps-avoid-transitive-reliance`](references/deps-avoid-transitive-reliance.md) - Avoid relying on transitive dependencies
- [`deps-configure-plugin-deps`](references/deps-configure-plugin-deps.md) - Configure plugins for tool-specific dependencies
- [`deps-fix-files-first`](references/deps-fix-files-first.md) - Fix unused files before dependencies
- [`deps-ignore-conditional-deps`](references/deps-ignore-conditional-deps.md) - Ignore conditionally loaded dependencies
- [`deps-remove-obsolete-types`](references/deps-remove-obsolete-types.md) - Remove obsolete type definition packages

### 5. Export Detection (MEDIUM-HIGH)

- [`exports-check-class-members`](references/exports-check-class-members.md) - Check class members for unused code
- [`exports-enable-entry-exports`](references/exports-enable-entry-exports.md) - Enable entry export checking for private packages
- [`exports-handle-reexports`](references/exports-handle-reexports.md) - Handle re-exports in barrel files
- [`exports-ignore-same-file`](references/exports-ignore-same-file.md) - Ignore exports used in same file
- [`exports-tag-public-api`](references/exports-tag-public-api.md) - Tag public API exports with JSDoc
- [`exports-trace-usage`](references/exports-trace-usage.md) - Trace export usage before removal
- [`exports-use-include-libs`](references/exports-use-include-libs.md) - Use include libs for type-based consumption

### 6. CI Integration (MEDIUM)

- [`ci-add-to-pipeline`](references/ci-add-to-pipeline.md) - Add Knip to CI pipeline
- [`ci-separate-production-check`](references/ci-separate-production-check.md) - Separate production and default mode checks
- [`ci-use-cache`](references/ci-use-cache.md) - Enable cache for faster CI runs
- [`ci-use-max-issues`](references/ci-use-max-issues.md) - Use max issues for gradual adoption
- [`ci-use-reporters`](references/ci-use-reporters.md) - Use appropriate reporters for CI output
- [`ci-watch-mode-local`](references/ci-watch-mode-local.md) - Use watch mode for local development

### 7. Auto-Fix Workflow (MEDIUM)

- [`fix-allow-remove-files`](references/fix-allow-remove-files.md) - Explicitly allow file removal
- [`fix-format-after-fix`](references/fix-format-after-fix.md) - Format code after auto-fix
- [`fix-review-before-commit`](references/fix-review-before-commit.md) - Review auto-fix changes before commit
- [`fix-update-deps-after`](references/fix-update-deps-after.md) - Update package manager after dependency fix
- [`fix-use-fix-type`](references/fix-use-fix-type.md) - Use fix type for targeted cleanup

### 8. Performance Optimization (LOW-MEDIUM)

- [`perf-filter-issue-types`](references/perf-filter-issue-types.md) - Filter issue types for focused analysis
- [`perf-limit-output`](references/perf-limit-output.md) - Limit output for large codebases
- [`perf-profile-performance`](references/perf-profile-performance.md) - Profile performance for slow analysis
- [`perf-use-bun-runtime`](references/perf-use-bun-runtime.md) - Use Bun runtime for faster analysis
- [`perf-use-cache-flag`](references/perf-use-cache-flag.md) - Enable cache for repeated analysis
- [`perf-use-workspace-filter`](references/perf-use-workspace-filter.md) - Filter workspaces for faster monorepo analysis

## How to Use

Read individual reference files for detailed explanations and code examples:

- [Section definitions](references/_sections.md) - Category structure and impact levels
- [Rule template](assets/templates/_template.md) - Template for adding new rules

## Reference Files

| File | Description |
|------|-------------|
| [references/_sections.md](references/_sections.md) | Category definitions and ordering |
| [assets/templates/_template.md](assets/templates/_template.md) | Template for new rules |
| [metadata.json](metadata.json) | Version and reference information |
