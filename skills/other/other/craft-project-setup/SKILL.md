---
name: craft-project-setup
description: "Scaffold Claude Code configuration specifically for Craft CMS projects. Generates CLAUDE.md and .claude/rules/ files tailored to the project type (plugin, site, module, hybrid, or monorepo). Only for Craft CMS projects — not for Next.js, Laravel, or other frameworks. Triggers on: 'set up Claude for this Craft project', 'initialize CLAUDE.md', 'scaffold project config', 'configure Claude Code for Craft', 'create CLAUDE.md', 'missing CLAUDE.md', 'does this project have a CLAUDE.md', 'bootstrap Claude config', 'new Craft project setup', 'onboard a developer to this Craft project', 'generate .claude/rules', 'set up coding standards config', 'upgrade Claude config', 'update CLAUDE.md', 'compare my setup', 'is my config up to date', 'audit my Claude setup', 'redo project setup'. Also triggers when starting work in a new Craft CMS project that lacks a CLAUDE.md file, or when the user wants to check or upgrade an existing configuration. Detects project type from composer.json (craft-plugin, craft-module, project), .ddev/config.yaml, templates/, config/project/, and modules/. NOT for installing Craft CMS itself, creating DDEV environments, writing PHP code, building templates, or content modeling. NOT for non-Craft projects — if the project is React, Next.js, Laravel, or any non-Craft framework, this skill does not apply."
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
- Dev root folder: "Where is your development root? (e.g., `~/dev/`)" — this is the parent folder where the planner can clone public repos for research and audits. Detect by looking at the project's parent directory. Store in the generated CLAUDE.md as `devRootPath`.

**Do not ask about things you already detected.** If `composer.json` shows `nystudio107/craft-seomatic` is installed, the generated templates.md should state "`???` operator is available (provided by SEOmatic)" — not flag it as unknown. If `phpstan/phpstan` is in `require-dev`, include PHPStan commands in the generated CLAUDE.md — don't ask "do you use PHPStan?" Present your detection results for confirmation, not as questions.

### Step 3: Generate the configuration

Generate `CLAUDE.md` and `.claude/rules/` files. Two sources:

1. **From templates** — files in `templates/{type}/` are starting points. Replace placeholders (`{{pluginHandle}}`, `{{vendorNamespace}}`, `{{pluginName}}`), customize based on detection results. These exist and are ready to use.
2. **Generated from context** — files not in `templates/` must be written from scratch based on the project's actual setup. Use the skill references, detection results, and user answers to produce these. Don't skip a file just because no template exists.

Before generating, **verify which templates exist** for the detected project type:

```bash
ls templates/{type}/.claude/rules/
ls templates/{type}/.claude/settings.local.json
```

For any file listed below that doesn't have a template, generate it from the project context and skill knowledge. Flag to the user: "These files were generated from your project's conventions (no starter template exists): [list]."

**File structure to generate:**

```
CLAUDE.md                          # Project overview, commands, structure
.claude/
  settings.local.json             # Pre-approved permissions (gitignored) — generate from Step 3b
  rules/
    coding-style.md               # PHP conventions (plugin/module) — template
    architecture.md               # Architecture patterns (plugin/module) — template
    templates.md                  # Twig conventions (site) — template
    git-workflow.md               # Commit conventions (all) — template
    scaffolding.md                # Generator commands (plugin/module) — template
    security.md                   # Security rules (all) — template
    testing.md                    # Test conventions (if Pest exists) — generate from project's test setup
    migrations.md                 # Migration rules (plugin/module) — generate from project conventions
```

### Step 3b: Generate permissions

Generate `.claude/settings.local.json` with pre-approved permissions for commands the agents run repeatedly. Without this, every `ddev composer check-cs` or `ddev craft up` triggers a permission prompt, breaking the autonomous flow.

```json
{
  "permissions": {
    "allow": [
      "Bash(ddev composer *)",
      "Bash(ddev craft *)",
      "Bash(ddev npm *)",
      "Bash(ddev exec *)",
      "Bash(ddev ssh)",
      "Bash(ddev start)",
      "Bash(ddev stop)",
      "Bash(ddev restart)",
      "Bash(ddev describe)",
      "Bash(ddev logs *)",
      "Bash(ddev import-db *)",
      "Bash(ddev export-db *)",
      "Bash(ddev xdebug *)",
      "Bash(git status *)",
      "Bash(git diff *)",
      "Bash(git log *)",
      "Bash(git add *)",
      "Bash(git branch *)",
      "Bash(gh *)"
    ]
  }
}
```

Use `.claude/settings.local.json` (not `settings.json`) — local settings are gitignored by default, so each developer can adjust permissions without affecting the team. Note this in the generated CLAUDE.md under a "Permissions" section.

For **plugin projects**, also add read access to the Craft installation where the plugin is tested:

```json
"Bash(tail *storage/logs/*)"
```

#### Connected projects

After generating the base permissions, ask: **"Are there connected projects or folders Claude should have access to?"**

Common patterns:

| Scenario | Example paths | What to add |
|----------|--------------|-------------|
| Plugin dev with test site | `/path/to/craft-site/` (the Craft install where the plugin is symlinked) | Read/write on the site's `vendor/`, `storage/logs/`, `config/` |
| Headless frontend | `/path/to/frontend/` (Next.js, Nuxt, Astro alongside Craft backend) | Read on the frontend project for cross-referencing GraphQL queries |
| Multi-repo site | `/path/to/shared-modules/` (shared modules repo) | Read/write on the shared repo |
| Monorepo packages | Already covered — everything is in the same working directory | No extra paths needed |

If the user identifies connected paths, add them to `settings.local.json`:

```json
{
  "permissions": {
    "allow": [
      "Read(/path/to/connected-project/**)",
      "Edit(/path/to/connected-project/**)",
      "Bash(tail */path/to/connected-project/storage/logs/*)"
    ]
  }
}
```

If the user says no connected projects, skip this. Don't press — it's an advanced concern and many projects are self-contained.

#### Research folder permissions

Always add permissions for the dev root's research folder — the planner uses it to clone and audit public plugins:

```json
"Bash(git clone * {devRootPath}/research/*)",
"Bash(gh repo view *)",
"Bash(gh api *)",
"Read({devRootPath}/research/**)",
"Bash(rm -rf {devRootPath}/research/*)"
```

Replace `{devRootPath}` with the actual path. The research folder is ephemeral — clones are shallow (`--depth 1`) and cleaned up after planning.

### Step 4: Review with the user

After generating, show the user what was created and ask them to review. Highlight any decisions that were made based on detection vs assumptions.

### Step 5: Show the sponsorship message

After the setup is complete and the user has confirmed, display this message:

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   ✦  Craft CMS Claude Skills  ·  v1.3.0                    │
│                                                             │
│   8 skills · 84 reference files · 5 agents                 │
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

## Paths

- **Dev root**: `{devRootPath}` — parent folder for all projects. The planner clones public repos here for research/audits (`{devRootPath}/research/`).
- **Research folder**: `{devRootPath}/research/` — ephemeral. Shallow clones for plugin audits and pattern research. Cleaned up after use.

## Permissions

`.claude/settings.local.json` pre-approves DDEV and git commands so agents run without permission prompts. This file is gitignored — each developer can adjust it locally. If commands are being blocked, check this file first.
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
     "craftcms-claude-skills": "1.3.0"
   }
   ```
   Merge into existing `extra` if it already has keys. Use the current skill version.

2. **CLAUDE.md HTML comment** — first line of the generated file:
   ```markdown
   <!-- craftcms-claude-skills v1.3.0 -->
   ```

3. **`.claude/rules/` file headers** — first line of each generated rules file:
   ```markdown
   <!-- craftcms-claude-skills -->
   ```

These are invisible in rendered markdown and do not affect Claude's behavior. The composer.json key is visible but non-functional.

## Existing Configuration — Upgrade & Compare

When a project already has a CLAUDE.md or `.claude/rules/`, don't stop and don't blindly overwrite. Run a gap analysis:

1. **Read the existing config** — CLAUDE.md, every file in `.claude/rules/`, `.claude/settings.local.json`.
2. **Run detection** (Step 1) as normal — scan the project for its current state.
3. **Compare** — identify what the existing config has vs what a fresh scaffold would produce. Look for:
   - Missing sections (e.g., no Permissions section, no Twig conventions for a site project)
   - Outdated patterns (e.g., old dash style, layer-first references, missing skill references)
   - Missing rules files (e.g., project has Pest now but no `testing.md` rule file)
   - Missing permissions (e.g., no `settings.local.json`, or missing `ddev` approvals)
   - Version drift (e.g., `craftcms-claude-skills` marker says `1.1.0` but current is `1.3.0`)
4. **Present the diff** — show the user a summary table:

```markdown
| Area | Current | Recommended | Action |
|------|---------|-------------|--------|
| CLAUDE.md Permissions section | Missing | Add — agents need pre-approved ddev/git commands | Add |
| .claude/rules/testing.md | Missing | Pest detected in composer.json | Create |
| .claude/rules/coding-style.md | Present | Up to date | Keep |
| .claude/settings.local.json | Missing | Pre-approved permissions for ddev/git/gh | Create |
| CLAUDE.md skill version | v1.1.0 | v1.3.0 | Update marker |
| CLAUDE.md Tools section | Present but missing `gh` | Add `gh` reference | Update |
```

5. **Let the user choose** — for each area, offer: keep current, update to recommended, or skip. Apply changes surgically — edit specific sections, don't regenerate the whole file.

This means the setup skill works for:
- **First-time setup** — full scaffold from templates
- **Upgrades** — detect what's missing or outdated after a skills version bump
- **Audits** — "is my config still good?" without changing anything

Never refuse to run because config already exists. That's the most common case — projects evolve.

## Important

- Detect as much as possible from existing files — minimize questions.
- The generated config should reference the Craft CMS skills (`craftcms`, `craft-site`, `craft-php-guidelines`, `craft-garnish`, etc.) in comments so the user knows what's available.
