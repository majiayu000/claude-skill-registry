---
name: wp-project-triage
description: "Use when you need to quickly understand a WordPress repository: detect project type (plugin/theme/block theme/WP core/full site), available tooling (Composer, npm, @wordpress/scripts), test frameworks (PHPUnit, Playwright, wp-env), and version hints."
compatibility: "Targets WordPress 6.9+ (PHP 8.0+). Filesystem-based agent with bash + node."
---

# WP Project Triage

## When to use

Use this skill to quickly understand what kind of WordPress repo you're in and what commands/conventions to follow before making changes.

## Inputs required

- Repo root (current working directory)

## Procedure

### 1) Detect project kind

```bash
# Plugin detection
if grep -l "Plugin Name:" *.php 2>/dev/null; then
  echo "KIND: plugin"
fi

# Theme detection
if [ -f "style.css" ] && grep -q "Theme Name:" style.css; then
  if [ -f "theme.json" ] && [ -d "templates" ]; then
    echo "KIND: block-theme"
  else
    echo "KIND: classic-theme"
  fi
fi

# WP Core detection
if [ -d "wp-includes" ] && [ -d "wp-admin" ]; then
  echo "KIND: wp-core"
fi

# Full site detection
if [ -d "wp-content" ]; then
  echo "KIND: full-site"
fi
```

### 2) Detect tooling

```bash
# PHP/Composer
[ -f "composer.json" ] && echo "TOOLING: composer"
[ -d "vendor" ] && echo "TOOLING: composer-installed"

# Node/npm
[ -f "package.json" ] && echo "TOOLING: npm"
[ -d "node_modules" ] && echo "TOOLING: npm-installed"

# WordPress Scripts
grep -q "@wordpress/scripts" package.json 2>/dev/null && echo "TOOLING: wp-scripts"

# Build config
[ -f "webpack.config.js" ] && echo "TOOLING: webpack"
[ -f "vite.config.js" ] && echo "TOOLING: vite"
```

### 3) Detect testing

```bash
# PHPUnit
[ -f "phpunit.xml" ] || [ -f "phpunit.xml.dist" ] && echo "TESTS: phpunit"

# Playwright
grep -q "playwright" package.json 2>/dev/null && echo "TESTS: playwright"

# wp-env
[ -f ".wp-env.json" ] && echo "TESTS: wp-env"

# Jest
grep -q "jest" package.json 2>/dev/null && echo "TESTS: jest"
```

### 4) Detect version hints

```bash
# PHP version from composer.json
grep -o '"php":\s*"[^"]*"' composer.json 2>/dev/null

# WordPress version from readme.txt
grep -i "Requires at least:" readme.txt 2>/dev/null
grep -i "Tested up to:" readme.txt 2>/dev/null

# Node version
[ -f ".nvmrc" ] && cat .nvmrc
[ -f ".node-version" ] && cat .node-version
```

### 5) Build triage report

Compile findings into structured output:

```
PROJECT TRIAGE
==============
Kind: [plugin|classic-theme|block-theme|wp-core|full-site]

Tooling:
- PHP: [composer version or none]
- Node: [npm/yarn, version if detected]
- Build: [wp-scripts|webpack|vite|none]

Tests:
- PHP: [phpunit|pest|none]
- E2E: [playwright|cypress|none]
- Unit: [jest|none]

Versions:
- PHP Required: X.X+
- WP Required: X.X+
- WP Tested: X.X
```

## Verification

- JSON should parse correctly
- Re-run after changes that affect structure (adding theme.json, block.json, build config)

## Failure modes / debugging

- If reports `unknown`, check whether repo root is correct
- If scanning is slow, add ignore directories (.git, node_modules, vendor)

## Use triage output to

- Select appropriate domain skills
- Choose build/test commands
- Set version compatibility expectations
- Apply correct coding standards
