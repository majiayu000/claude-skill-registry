---
name: wordpress-router
description: "Use at the start of WordPress tasks to classify the repo type (plugin, theme, block theme, WP core, full site) and route to the correct workflow/skill (blocks, theme.json, REST API, WP-CLI, performance, security, testing)."
compatibility: "Targets WordPress 6.9+ (PHP 8.0+). Filesystem-based agent with bash + node."
---

# WordPress Router

## When to use

Use this skill at the start of most WordPress tasks to:

- Identify what kind of WordPress codebase this is (plugin vs theme vs block theme vs WP core checkout vs full site)
- Pick the right workflow and guardrails
- Delegate to the most relevant domain skill(s)

## Inputs required

- Repo root (current working directory)
- User's intent (what they want changed) and any constraints (WP version targets, release requirements)

## Procedure

### 1) Detect project type

Run quick detection checks:

```bash
# Check for plugin indicators
ls -la | grep -E "^-.*\.php$" | head -3
grep -l "Plugin Name:" *.php 2>/dev/null

# Check for theme indicators
ls style.css 2>/dev/null && head -20 style.css

# Check for block theme indicators
ls theme.json 2>/dev/null
ls -d templates/ parts/ 2>/dev/null

# Check for WP core
ls wp-includes/ wp-admin/ 2>/dev/null

# Check for full site
ls wp-content/ 2>/dev/null
```

### 2) Classify the project

| Indicators | Type | Primary Skill |
|------------|------|---------------|
| `Plugin Name:` in PHP header | Plugin | `wp-plugin-development` |
| `style.css` with `Theme Name:` | Classic Theme | `wp-theme-development` |
| `theme.json` + `templates/` | Block Theme | `wp-block-themes` |
| `block.json` files | Has Blocks | `wp-gutenberg-blocks` |
| `wp-includes/` + `wp-admin/` | WP Core | Core development workflow |
| `wp-content/` present | Full Site | Multiple skills as needed |

### 3) Route to domain workflow

Based on user intent + repo kind:

| Intent | Route To |
|--------|----------|
| Create/modify Gutenberg blocks | `wp-gutenberg-blocks` |
| Block theme work (theme.json, templates) | `wp-block-themes` |
| Add interactivity (data-wp-* directives) | `wp-interactivity-api` |
| Plugin architecture, hooks, Settings API | `wp-plugin-development` |
| Performance profiling/optimization | `wp-performance-review` |
| Security audit | `wp-security-review` |
| WP-CLI operations | `wp-wpcli-and-ops` |
| Testing in isolation | `wp-playground` |

### 4) Apply guardrails

Before making changes:

- Confirm any version constraints if unclear
- Prefer the repo's existing tooling and conventions
- Check for existing tests/lint configs

## Verification

- Re-run detection if you create or restructure significant files
- Run the repo's lint/test/build commands if available

## Failure modes / debugging

- If detection is unclear, inspect:
  - Root `composer.json`, `package.json`
  - `style.css`, `block.json`, `theme.json`
  - `wp-content/` structure
- If repo is huge, narrow scanning scope

## Escalation

If routing is ambiguous, ask:
> "Is this intended to be a WordPress plugin, a theme (classic/block), or a full site repo?"
