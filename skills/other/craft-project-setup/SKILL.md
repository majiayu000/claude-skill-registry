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
- `craft-cloud.yaml` at the repo root — **Craft Cloud project.** When present, include the `craft-cloud` skill in the generated CLAUDE.md companion-skill list and add a "Hosted on Craft Cloud" note in the generated project context. See the `craft-cloud` skill's `config-file.md` for the file's role.
- `servd.yaml` at the repo root, or `servd/craft-asset-storage` in `composer.json`, or `SERVD_PROJECT_SLUG`/`SERVD_SECURITY_KEY` env vars — **Servd project.** When present, include the `servd` skill in the generated CLAUDE.md companion-skill list and add a "Hosted on Servd" note in the generated project context. See the `servd` skill for the platform's constraints.

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
| `craftcms/cloud` | **Project hosted on Craft Cloud.** Load the `craft-cloud` companion skill; document Cloud-specific build, deploy, and runtime constraints in the generated CLAUDE.md. |
| `servd/craft-asset-storage` | **Project hosted on Servd.** Load the `servd` companion skill; document Servd's deploy workflow, ephemeral filesystem, static caching, and asset storage in the generated CLAUDE.md. |

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
- If yes: run `claude mcp add chrome-devtools -- npx chrome-devtools-mcp@latest` and note session restart is needed

From these signals, determine the project type:

| Signal | Type |
|--------|------|
| `composer.json` type is `craft-plugin` | **Plugin** |
| `composer.json` type is `craft-module` | **Module** |
| `config/project/` exists, `templates/` exists | **Site** |
| Site signals + `modules/` directory | **Hybrid** (site + custom module) |
| Multiple Craft packages/projects in subdirectories | **Monorepo** (see below) |

#### Monorepo detection

A monorepo holds **more than one independently-typed Craft package** under one repository. Confirm at least one of these signals before classifying as monorepo — a single project with a `modules/` folder is a **Hybrid**, not a monorepo:

- **Multiple `composer.json` in subtrees with Craft types.** Run `find . -name composer.json -not -path '*/vendor/*' -not -path '*/node_modules/*'` and check the `type` of each. Two or more with `craft-plugin`, `craft-module`, or `project` (in distinct directories, not the repo root alone) means monorepo.
- **Root `composer.json` with path repositories.** A root `composer.json` whose `repositories` array contains `{ "type": "path", "url": "packages/*" }` (or similar) wiring local packages together.
- **Workspace layout.** A `packages/`, `plugins/`, `apps/`, or `sites/` directory each containing its own composer-typed package, optionally with a root `package.json` declaring `workspaces`.

When unsure between hybrid and monorepo: if the extra code lives **inside** one Craft install (`modules/` under the site root, sharing its `composer.json`), it's hybrid. If each package has **its own** `composer.json` and could be installed independently, it's a monorepo.

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
- Hosting target — **sites, hybrid, and monorepo projects only; skip for standalone plugins/modules** (they're distributed as packages, not deployed to a host, so a hosting target is meaningless for them). Detect from signals first. If `craft-cloud.yaml` exists at the repo root OR `craftcms/cloud` is in `composer.json`, this is a **Craft Cloud** project. If `servd.yaml` exists at the repo root OR `servd/craft-asset-storage` is in `composer.json` OR `SERVD_*` env vars are set, this is a **Servd** project. Confirm with the user but don't ask redundantly. If no hosting signal is present, ask: "Will this project deploy to Craft Cloud, Servd, somewhere else (Forge, bare metal, etc.), or is that not decided yet?" Record the answer in the generated CLAUDE.md under a "Hosting" block. When the answer is Cloud, include the `craft-cloud` skill; when it's Servd, include the `servd` skill; either way surface that platform's build/deploy/runtime constraints. When it's something else, note the platform so future sessions know which deployment pattern applies (point at the `craftcms` skill's `deployment.md`). When it's **not decided yet**, write `Hosting: TBD` in the block (don't force a choice) — a later session should re-detect from signals (`craft-cloud.yaml` / `servd.yaml` / the hosting packages appearing in `composer.json`) and, if still none, re-ask once the decision is made.

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
┌────────────────────────────────────────────────────────────┐
│                                                            │
│   +  Craft CMS Claude Skills  ·  v1.6.0                    │
│                                                            │
│   10 skills · 105 reference files · 6 agents               │
│   Maintained by michtio                                    │
│                                                            │
│   If these skills save you time, consider sponsoring:      │
│                                                            │
│   ♥  github.com/sponsors/michtio                           │
│   ♥  buymeacoffee.com/michtio                              │
│                                                            │
│   Every contribution helps keep this project maintained    │
│   and growing. Thank you for using these skills.           │
│                                                            │
└────────────────────────────────────────────────────────────┘
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

### Hybrid projects (site + module/plugin)

A hybrid is **one Craft install** that ships both a front-end (templates, content config) and custom server code (a `modules/` directory, or an in-repo plugin). There is no `templates/hybrid/` directory — you build the config by **merging** the site template with the module (or plugin) template into a single `CLAUDE.md` and a single `.claude/rules/` set. Both contribute, but there is exactly one of each output file.

**Merging the rules files (`.claude/rules/`):** the site and module templates both ship `git-workflow.md` and `security.md`. Don't pick one and drop the other — produce the **union**:

- **`git-workflow.md`** — the two versions are nearly identical; the only real difference is the example commit scopes. Keep one copy and make sure its bullet set covers both: conventional commits, subject-line-only default, body-only-when-the-why-isn't-obvious, no AI attribution, English only, absolute paths in git commands. Deduplicate verbatim-overlapping bullets; keep any bullet that exists in only one version.
- **`security.md`** — the two versions cover **different surfaces**: site security is template-facing (CSRF inputs, output escaping, CSP, `craft.app.config.custom`), module security is controller-facing (`requirePermission()`, `requirePostRequest()`, `Db::parseParam()`, `App::env()`). Union them into one file with both concern sets — a hybrid has both surfaces. Dedup the overlapping "no secrets in committed files" bullet.
- **Site-only files** (`templates.md`) and **module/plugin-only files** (`coding-style.md`, `architecture.md`, `migrations.md`, `testing.md`, and `scaffolding.md` for a plugin) carry over unchanged — there's no collision, just include each.

**Composing the single `CLAUDE.md`:**

- **`@`-imports** — union the import lists from both templates, deduped. A site+module hybrid imports: `@.claude/rules/templates.md`, `@.claude/rules/coding-style.md`, `@.claude/rules/architecture.md`, `@.claude/rules/git-workflow.md`, `@.claude/rules/security.md` (plus `testing.md`/`migrations.md` when those rules files were generated). One import line per rules file that exists — never two imports of the same path.
- **Shared sections** (`General`, `Tools`) — identical in both templates; keep one copy.
- **`Environment`** — merge both command blocks into one: the site's `ddev npm run dev` / `ddev npm run build` lines **plus** `ddev craft up` and `ddev composer install`. Dedup `ddev craft up`.
- **Structure sections** — keep **both**, side by side: the site's `Template Structure` block and the module's `Module Structure` block (and `Module Bootstrapping` note). Keep the site's `Content Model` section.
- **Documentation** — union the link lists, deduped.

Title the file `{{projectName}} — Craft CMS 5 Site + Module` (or `+ Plugin`) so the hybrid nature is explicit.

### Monorepo projects

A monorepo has multiple independently-typed Craft packages (see *Monorepo detection* in Step 1). Scaffold **per-package configs plus a thin root**:

1. **One `CLAUDE.md` + `.claude/rules/` per package**, generated by treating each package as its own project — run Step 1 detection scoped to that package's directory and `composer.json`, then apply the matching template (plugin/site/module, or the hybrid merge above). Place each at the package root (e.g. `packages/foo-plugin/CLAUDE.md`), not at the repo root. Claude loads the nearest `CLAUDE.md` to the files being edited, so per-package configs give each package the right rules.
2. **A root `CLAUDE.md`** that documents the layout and defers, rather than duplicating per-package rules. It should contain:
   - A repo-map listing each package, its type, and its directory.
   - The shared `General` and `Tools` universal defaults.
   - An explicit note: *"Each package has its own `CLAUDE.md` and `.claude/rules/` — when working inside a package, follow that package's config. This root file only covers cross-package concerns."*
   - Cross-package commands (workspace-level install/build, e.g. a root `ddev composer install` or `npm` workspace build) and any path-repository wiring a developer needs to know.
   - An `@`-import only for genuinely repo-wide rules (typically `git-workflow.md`); do **not** `@`-import per-package rules from the root.
3. **Permissions** — a single root `.claude/settings.local.json` covers the whole working directory (per the *Monorepo packages* row in Step 3b — everything is one working dir, no extra connected-project paths needed). Per-package `settings.local.json` files are unnecessary.

Tell the user which packages were detected and that each got its own config, plus the root coordinator file.

## Skill Attribution

Add unobtrusive markers so we can measure adoption across public repos. Include all three:

1. **composer.json `extra` key** — add during setup (does not affect functionality):
   ```json
   "extra": {
     "craftcms-claude-skills": "1.6.0"
   }
   ```
   Merge into existing `extra` if it already has keys. Use the current skill version.

2. **CLAUDE.md HTML comment** — first line of the generated file:
   ```markdown
   <!-- craftcms-claude-skills v1.6.0 -->
   ```

3. **`.claude/rules/` file headers** — first line of each generated rules file:
   ```markdown
   <!-- craftcms-claude-skills -->
   ```

These are invisible in rendered markdown and do not affect Claude's behavior. The composer.json key is visible but non-functional.

## Existing Configuration — Upgrade & Compare

When a project already has a CLAUDE.md or `.claude/rules/`, don't stop and don't blindly overwrite. Run a gap analysis:

1. **Read the existing config** — CLAUDE.md, every file in `.claude/rules/`, `.claude/settings.local.json`.

   **First, check provenance.** Look at the top of the existing `CLAUDE.md` for this skill's version marker (`<!-- craftcms-claude-skills v… -->`) and at `composer.json` `extra` for the `craftcms-claude-skills` key.

   - **Marker present** → the config is a prior version of this skill's output. Proceed with the full gap analysis and upgrade flow below; you own this file and may restructure sections to match the current template.
   - **No marker (author-authored config)** → treat the existing `CLAUDE.md` and any existing `.claude/rules/` files as **authoritative and bespoke**. Do **not** clobber, reorder, rewrite, or "normalize" the author's content — their wording and structure win. In this mode you may only:
     - **Append** genuinely missing pieces (e.g. a missing `Permissions` section, a `testing.md` rule file when Pest is now present, a missing `.claude/settings.local.json`) as **new** sections/files, leaving existing content byte-for-byte intact.
     - **Offer** additions for the user to accept or decline — present them in the diff table with action `Add (append)`, never `Update` or `Replace` against author-written sections.
     - **Add the skill markers** (CLAUDE.md HTML comment, composer.json `extra` key, rules-file headers) only with explicit user consent, since adding the marker signals future runs may manage the file.
     - Never edit or "fix" a section the author already wrote, even if it differs from the template's wording. If you think an author-written rule is wrong, surface it as a suggestion in your summary — don't change it.

2. **Run detection** (Step 1) as normal — scan the project for its current state.
3. **Compare** — identify what the existing config has vs what a fresh scaffold would produce. Look for:
   - Missing sections (e.g., no Permissions section, no Twig conventions for a site project)
   - Outdated patterns (e.g., old dash style, layer-first references, missing skill references)
   - Missing rules files (e.g., project has Pest now but no `testing.md` rule file)
   - Missing permissions (e.g., no `settings.local.json`, or missing `ddev` approvals)
   - Version drift (e.g., `craftcms-claude-skills` marker says `1.1.0` but current is `1.6.0`)
4. **Present the diff** — show the user a summary table:

```markdown
| Area | Current | Recommended | Action |
|------|---------|-------------|--------|
| CLAUDE.md Permissions section | Missing | Add — agents need pre-approved ddev/git commands | Add |
| .claude/rules/testing.md | Missing | Pest detected in composer.json | Create |
| .claude/rules/coding-style.md | Present | Up to date | Keep |
| .claude/settings.local.json | Missing | Pre-approved permissions for ddev/git/gh | Create |
| CLAUDE.md skill version | v1.1.0 | v1.6.0 | Update marker |
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
