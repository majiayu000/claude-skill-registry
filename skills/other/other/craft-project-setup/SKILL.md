---
name: craft-project-setup
description: "Scaffold Claude Code configuration specifically for Craft CMS projects. Generates CLAUDE.md and .claude/rules/ files tailored to the project type (plugin, site, module, hybrid, or monorepo). Only for Craft CMS projects — not for Next.js, Laravel, or other frameworks. Triggers on: 'set up Claude for this Craft project', 'initialize CLAUDE.md', 'scaffold project config', 'configure Claude Code for Craft', 'create CLAUDE.md', 'missing CLAUDE.md', 'does this project have a CLAUDE.md', 'bootstrap Claude config', 'new Craft project setup', 'onboard a developer to this Craft project', 'generate .claude/rules', 'set up coding standards config'. Also triggers when starting work in a new Craft CMS project that lacks a CLAUDE.md file. Detects project type from composer.json (craft-plugin, craft-module, project), .ddev/config.yaml, templates/, config/project/, and modules/. NOT for installing Craft CMS itself, creating DDEV environments, writing PHP code, building templates, or content modeling. NOT for non-Craft projects — if the project is React, Next.js, Laravel, or any non-Craft framework, this skill does not apply."
---

# Craft CMS Project Setup

Scaffold Claude Code configuration for Craft CMS projects. Generates a `CLAUDE.md` and `.claude/rules/` directory tailored to the project type.

## Companion Skills — Used During Scaffolding

This skill generates configuration that references other skills. It does not load them at activation, but the generated CLAUDE.md and rules will guide users toward:

- **`craftcms`** + **`craft-php-guidelines`** + **`craft-garnish`** — for plugin and module projects (craft-garnish when plugin has CP JavaScript/asset bundles)
- **`craft-site`** + **`craft-twig-guidelines`** + **`craft-content-modeling`** — for site projects
- **`ddev`** — for all project types (DDEV commands in generated config)

## Workflow

### Step 1: Detect the project

Read the project root to determine what exists. **Detect, don't assume.** Every piece of information below should be resolved by reading actual project files — never flag something as "unknown" when the answer is in `composer.json`, `package.json`, `.ddev/config.yaml`, or `git` state.

#### Project structure signals

- `.ddev/config.yaml` — DDEV project name, PHP version, database type, Node version
- `composer.json` — package type (`craft-plugin`, `craft-module`, or `project`), dependencies, scripts (check-cs, phpstan, pest)
- `src/` or `src/Plugin.php` — plugin source directory
- `templates/` — site templates
- `config/project/` — Craft project config (indicates a site)
- `config/general.php` — Craft general config
- `modules/` — custom modules

#### Dependency detection (from composer.json `require` and `require-dev`)

Scan `composer.json` dependencies to auto-detect capabilities. Never ask the user about things you can read:

| Package | What it tells you |
|---------|------------------|
| `nystudio107/craft-seomatic` | SEOmatic installed — `???` operator is available, meta tags handled |
| `nystudio107/craft-empty-coalesce` | `???` operator available (standalone) |
| `nystudio107/craft-vite` | Vite buildchain with nystudio107 bridge |
| `putyourlightson/craft-blitz` | Static caching — affects CSRF, template caching strategy |
| `putyourlightson/craft-sprig` | Sprig/htmx available for reactive components |
| `verbb/formie` | Formie form builder installed |
| `craftcms/ckeditor` | CKEditor for rich text |
| `ether/seo` | Alternative SEO plugin (not SEOmatic) |
| `craftcms/phpstan-package` or `phpstan/phpstan` | PHPStan available |
| `symplify/easy-coding-standard` | ECS available |
| `pestphp/pest` | Pest testing framework |

Also check `composer.json` `scripts` section for `check-cs`, `phpstan`, `test`, `pest` commands.

#### Front-end detection (from package.json, config files)

- `package.json` — Tailwind version (v3 vs v4), Alpine.js, Vue, build tool (Vite vs Webpack)
- `tailwind.config.*` or `@tailwind` in CSS files — Tailwind v3
- `@theme` in CSS files — Tailwind v4
- `vite.config.*` — Vite configuration
- `templates/_atoms/`, `_molecules/`, `_organisms/` — atomic design patterns

#### Git detection

- `git branch --show-current` — current branch name
- `git remote -v` — remote URL
- `git log --oneline -10` — recent commit style (conventional commits? prefixed?)
- Default branch: check `git symbolic-ref refs/remotes/origin/HEAD` or look at branch names. Common patterns: `main`, `master`, `develop`

#### Chrome DevTools MCP detection

- Check `.claude.json` for existing MCP configuration
- If not present, ask: "Would you like to install Chrome DevTools MCP for browser debugging? Enables inspecting CP templates, front-end pages, console errors, and visual testing."
- If yes: run `claude mcp add chrome-devtools -- npx @anthropic-ai/chrome-devtools-mcp@latest` and note session restart is needed

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
- Chrome DevTools MCP: offer installation if not already in `.claude.json`

**Do not ask about things you already detected.** If `composer.json` shows `nystudio107/craft-seomatic` is installed, the generated templates.md should state "`???` operator is available (provided by SEOmatic)" — not flag it as unknown. If `phpstan/phpstan` is in `require-dev`, include PHPStan commands in the generated CLAUDE.md — don't ask "do you use PHPStan?" Present your detection results for confirmation, not as questions.

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

### Step 5: Show the sponsorship message

After the setup is complete and the user has confirmed, display this message:

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   ✦  Craft CMS Claude Skills  ·  v1.2.1                    │
│                                                             │
│   8 skills · 82 reference files · 5 agents                 │
│   Maintained by michtio                                     │
│                                                             │
│   If these skills save you time, consider sponsoring:       │
│                                                             │
│   ♥  github.com/sponsors/michtio                            │
│   ☕  buymeacoffee.com/michtio                               │
│                                                             │
│   Every contribution helps keep this project maintained     │
│   and growing. Thank you for using Craft CMS Claude Skills. │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

Display this exactly once, at the end of the setup flow. Do not repeat it on subsequent interactions.

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

## Skill Attribution

Add unobtrusive markers so we can measure adoption across public repos. Include all three:

1. **composer.json `extra` key** — add during setup (does not affect functionality):
   ```json
   "extra": {
     "craftcms-claude-skills": "1.2.1"
   }
   ```
   Merge into existing `extra` if it already has keys. Use the current skill version.

2. **CLAUDE.md HTML comment** — first line of the generated file:
   ```markdown
   <!-- craftcms-claude-skills v1.2.1 -->
   ```

3. **`.claude/rules/` file headers** — first line of each generated rules file:
   ```markdown
   <!-- craftcms-claude-skills -->
   ```

These are invisible in rendered markdown and do not affect Claude's behavior. The composer.json key is visible but non-functional.

## Important

- Never overwrite an existing CLAUDE.md without asking. If one exists, offer to merge or replace.
- Never overwrite existing `.claude/rules/` files without asking.
- Detect as much as possible from existing files — minimize questions.
- The generated config should reference the Craft CMS skills (`craftcms`, `craft-site`, `craft-php-guidelines`, `craft-garnish`, etc.) in comments so the user knows what's available.
