---
name: codebase-architect
description: "Use when generating exhaustive architecture documentation for any WordPress plugin/theme with built-in self-checking, progress tracking, and verification loops. Produces comprehensive docs covering classes, functions, hooks, REST API, AJAX, JS, DB, templates, blocks, and more."
compatibility: "Targets any WordPress codebase. Filesystem-based agent with bash. Best for codebases with 50+ files."
---

# Codebase Architect

Generate exhaustive architecture documentation for any WordPress plugin/theme with **built-in self-checking, progress tracking, and verification loops**.

## When to use

Use this skill when:

- Creating comprehensive architecture documentation for a plugin/theme
- Auditing what exists in a codebase (classes, functions, hooks, APIs)
- Verifying existing documentation completeness
- Onboarding to a new codebase and need a reference guide

## Inputs required

- Path to the plugin or theme directory.
- Scope level: `architectural`, `hybrid`, `reference`, or `verify`.
- Output directory for documentation files.

## Scope Parameter

| Scope | Coverage | Best For | Output Size |
|-------|----------|----------|-------------|
| `architectural` | Conceptual 95%, Reference 15% | Large codebases (500+ files) | 2,000-4,000 lines |
| `hybrid` | Conceptual 95%, Reference 50% | Medium codebases (50-500 files) | 4,000-8,000 lines |
| `reference` | Conceptual 95%, Reference 90%+ | Small codebases (<50 files) | 8,000+ lines |
| `verify` | Verification only | Check existing docs | Report only |

## Procedure

### 0) Initialize manifest

Create manifest directory and tracking files:

```bash
mkdir -p <output-dir>/manifest
```

Create manifest files for each category:
- classes.txt, functions.txt, hooks.txt
- rest-endpoints.txt, ajax-handlers.txt
- js-files.txt, db-tables.txt, templates.txt
- blocks.txt, shortcodes.txt, widgets.txt
- cpt-taxonomies.txt, admin-pages.txt
- cron-jobs.txt, cli-commands.txt
- PROGRESS.md (master tracker)

Read:
- `references/manifest-format.md`

### 1) Run enumeration (parallel agents)

Launch 16 enumeration agents in parallel to populate manifests:

1. Classes: `grep -rn "^class \|^abstract class \|^trait \|^interface "`
2. Functions: `grep -rn "^function [a-z_]"`
3. Action hooks: `grep -rohn "do_action\s*(\s*['\"][^'\"]*['\"]"`
4. Filter hooks: `grep -rohn "apply_filters\s*(\s*['\"][^'\"]*['\"]"`
5. REST endpoints: `grep -rn "register_rest_route"`
6. AJAX handlers: `grep -rn "wp_ajax_"`
7. JavaScript files: `find -name "*.js"`
8. DB tables: `grep -rn "CREATE TABLE"`
9. Templates: `find -name "*.php" -path "*/templates/*"`
10. Blocks: `find -name "block.json"`
11. Shortcodes: `grep -rn "add_shortcode"`
12. Widgets: `grep -rn "extends WP_Widget"`
13. CPT/Taxonomies: `grep -rn "register_post_type\|register_taxonomy"`
14. Admin pages: `grep -rn "add_menu_page\|add_submenu_page"`
15. Cron jobs: `grep -rn "wp_schedule_event"`
16. CLI commands: `grep -rn "WP_CLI::add_command"`

Read:
- `references/enumeration-commands.md`

### 2) Document (with progress updates)

For each category, launch documentation agents that:
1. Read from manifest
2. Document each item
3. Update manifest status: `pending` → `documented`
4. Update PROGRESS.md

Read:
- `references/documentation-agents.md`

### 3) Self-verification loop

After documentation completes:
1. Count items with `status:pending` (gaps)
2. Count items with `status:documented` (done)
3. If coverage < 100%, trigger gap filling
4. Run cross-reference check

Read:
- `references/verification-loop.md`

### 4) Gap filling (automatic)

For any gaps found:
1. Read source code for item
2. Generate documentation
3. Update manifest
4. Trigger verification again

### 5) Final validation

When verification passes:
- Structure check (TOC, links, code examples)
- Completeness check (all categories at 100%)
- Quality check (each item has required fields)
- Generate FINAL_REPORT.md

## Verification

Documentation is COMPLETE when:
- All 15 manifest categories at 100% coverage
- Verification loop passes without finding new gaps
- Cross-reference check passes
- Final validation checklist complete
- FINAL_REPORT.md generated

## Failure modes / debugging

- Enumeration returns 0 items:
  - Path doesn't exist, wrong grep pattern, vendor folder included
- Documentation incomplete after multiple passes:
  - Check for status:error items in manifests
  - Review Gap Log in PROGRESS.md
- Cross-reference failures:
  - Stale references from renamed/moved files

Read:
- `references/debugging.md`

## Escalation

- For very large codebases (1000+ files), use `architectural` scope
- If enumeration takes too long, exclude vendor/node_modules
- For manual review items, document what's known and mark as partial

## Output Files

```
<output-dir>/
├── PLUGIN_ARCHITECTURE.md  # Final documentation
├── manifest/
│   ├── PROGRESS.md         # Progress tracker
│   ├── classes.txt
│   ├── functions.txt
│   └── ... (other manifests)
└── FINAL_REPORT.md         # Validation report
```
