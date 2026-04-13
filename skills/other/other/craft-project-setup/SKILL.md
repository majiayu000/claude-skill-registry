---
name: craft-project-setup
description: "Scaffold Claude Code configuration for a Craft CMS project. Generates CLAUDE.md and .claude/rules/ tailored to the project type (plugin, site, module, or hybrid). Use when the user says 'set up Claude for this project', 'initialize CLAUDE.md', 'scaffold project config', 'configure Claude Code', 'set up this Craft project', or when starting work in a new Craft CMS project that has no CLAUDE.md. Also use when the user mentions 'project setup', 'bootstrap', or asks how to configure Claude Code for their Craft project."
---

# Craft CMS Project Setup

Scaffold Claude Code configuration for Craft CMS projects. Generates a `CLAUDE.md` and `.claude/rules/` directory tailored to the project type.

## Workflow

### Step 1: Detect the project

Read the project root to determine what exists. Check for:

- `.ddev/config.yaml` — DDEV project name, PHP version, database type
- `composer.json` — package type (`craft-plugin`, `craft-module`, or `project`), dependencies, scripts (check-cs, phpstan, pest)
- `src/` or `src/Plugin.php` — plugin source directory
- `templates/` — site templates
- `config/project/` — Craft project config (indicates a site)
- `config/general.php` — Craft general config
- `modules/` — custom modules

From these signals, determine the project type:

| Signal | Type |
|--------|------|
| `composer.json` type is `craft-plugin` | **Plugin** |
| `composer.json` type is `craft-module` | **Module** |
| `config/project/` exists, `templates/` exists | **Site** |
| Site signals + `modules/` directory | **Hybrid** (site + custom module) |

### Step 2: Ask clarifying questions

Confirm the detected type and gather project-specific details. Keep it short — 3-5 questions max.

**For plugins:**
- Plugin handle and vendor namespace (detect from `composer.json` if possible)
- Does it have custom element types?
- What Craft edition does it target? (Solo, Team, Pro)

**For sites:**
- CSS framework? (detect Tailwind version from `package.json` or `tailwind.config.*`)
- Are they using atomic design patterns? (detect `_atoms/`, `_molecules/` in templates)
- Any custom modules alongside the site?

**For all types:**
- Confirm detected tooling: ECS, PHPStan, Pest (from `composer.json` scripts)
- Git workflow: main branch name, PR-based workflow?

### Step 3: Generate the configuration

Generate `CLAUDE.md` and `.claude/rules/` files using the templates in `templates/` as a starting point. Customize based on the answers:

- Replace placeholders: `{{pluginHandle}}`, `{{vendorNamespace}}`, `{{pluginName}}`
- Include only relevant rules files for the project type
- Include only the tooling commands that actually exist in the project

**File structure to generate:**

```
CLAUDE.md                          # Project overview, commands, structure
.claude/
  rules/
    coding-style.md               # PHP conventions (plugin/module)
    architecture.md               # Architecture patterns (plugin/module)
    templates.md                  # Twig conventions (site)
    git-workflow.md               # Commit conventions (all)
    scaffolding.md                # Generator commands (plugin/module)
    security.md                   # Security rules (all)
    testing.md                    # Test conventions (if Pest exists)
    migrations.md                 # Migration rules (plugin/module)
```

### Step 4: Review with the user

After generating, show the user what was created and ask them to review. Highlight any decisions that were made based on detection vs assumptions.

## Universal Defaults

Every generated CLAUDE.md includes these rules regardless of project type. These are baseline expectations for professional Craft CMS work:

```markdown
## General

Be critical. We're equals — push back when something doesn't make sense.

Do not excessively use emojis.

Do not include AI attribution in commits, PR descriptions, PR comments, issue comments, or generated code. Many clients and enterprises remain skeptical of AI-generated work, so all output should be indistinguishable from human-authored work.

Do not include "Test plan" sections in PR descriptions.
```

```markdown
## Tools

Use `ddev` shorthand commands: `ddev composer`, `ddev craft`, `ddev npm`. Never run `php`, `composer`, or `npm` on the host — everything goes through DDEV.

Use `gh` for all GitHub operations — it's already authenticated.
```

## Template Files

The `templates/` directory contains starter files for each project type. Read the relevant templates and customize them based on detection results. Do not copy them verbatim — adapt to what actually exists in the project.

- `templates/plugin/` — Plugin development CLAUDE.md and rules
- `templates/site/` — Site development CLAUDE.md and rules
- `templates/module/` — Module development CLAUDE.md and rules

For hybrid projects (site + module), merge the site and module templates.

## Important

- Never overwrite an existing CLAUDE.md without asking. If one exists, offer to merge or replace.
- Never overwrite existing `.claude/rules/` files without asking.
- Detect as much as possible from existing files — minimize questions.
- The generated config should reference the Craft CMS skills (`craftcms`, `craft-site`, `craft-php-guidelines`, etc.) in comments so the user knows what's available.
