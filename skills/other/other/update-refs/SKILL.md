---
name: update-refs
description: Update naming and documentation references across the Claude Pilot codebase. Use when renaming features, updating descriptions, changing terminology, or ensuring consistency after modifying commands, skills, or workflows. Triggers on "update references", "rename X to Y across codebase", "sync documentation", or "update all mentions of X".
version: 1.1.0
---

# Update References

Ensure naming and documentation consistency across all codebase locations.

## Checklist

When updating terminology, feature names, descriptions, or counts, check ALL locations:

### 1. User-Facing Messages

| Location | What to Check |
|----------|---------------|
| `launcher/banner.py` | Welcome banner text, feature descriptions |
| `launcher/cli.py` | Pilot CLI help text and messages |
| `installer/cli.py` | Installer CLI help text, prompts |
| `installer/steps/finalize.py` | Post-install instructions |
| `installer/ui.py` | UI banner and status messages |

### 2. Documentation & Website

| Location | What to Check |
|----------|---------------|
| `README.md` | Feature descriptions, usage examples, counts (rules, hooks, skills, commands) |
| `docs/site/index.html` | SEO meta tags, page title, structured data |
| `docs/site/src/pages/Index.tsx` | SEO description, structured data counts |
| `docs/site/src/components/HeroSection.tsx` | Stats bar counts (rules, hooks, skills, LSPs, MCP) |
| `docs/site/src/components/WhatsInside.tsx` | Feature cards, descriptions, item counts |
| `docs/site/src/components/DeepDiveSection.tsx` | Under the Hood subtitle counts, hooks pipeline, rules categories |
| `docs/site/src/components/WorkflowSteps.tsx` | /spec workflow details, All Commands grid |
| `docs/site/src/components/ComparisonSection.tsx` | Before & After comparison table |
| `docs/site/src/components/PricingSection.tsx` | Standard plan feature counts, value proposition |
| `docs/site/src/components/InstallSection.tsx` | Installation instructions |
| `docs/site/src/components/Footer.tsx` | Footer links |
| `docs/site/src/components/NavBar.tsx` | Navigation links |

### 3. Package & Install

| Location | What to Check |
|----------|---------------|
| `pyproject.toml` | Package name, description, metadata |
| `install.sh` | Shell installer script messages |
| `launcher/__init__.py` | Package docstring |

### 4. Claude Configuration (Plugin Source)

| Location | What to Check |
|----------|---------------|
| `pilot/commands/*.md` | Command descriptions in frontmatter (`spec`, `sync`, `vault`, `learn`, plus internal phases) |
| `pilot/skills/*/SKILL.md` | Skill descriptions in frontmatter |
| `pilot/rules/*.md` | Standard rules content |
| `pilot/hooks/hooks.json` | Hook configuration and event triggers |
| `pilot/hooks/*.py` | Hook script messages and logic |
| `pilot/agents/*.md` | Sub-agent definitions (plan-verifier, spec-verifier) |
| `pilot/settings.json` | LSP server configuration |
| `pilot/modes/*.json` | Language mode definitions |

### 5. Project-Level Claude Config

| Location | What to Check |
|----------|---------------|
| `.claude/rules/*.md` | Project-specific rules (git-commits.md, project.md) |
| `.claude/skills/*/SKILL.md` | Project-specific skills (lsp-cleaner, pr-review, update-refs) |

## No Hardcoded Counts

**Do NOT add specific counts (e.g., "22 rules", "7 hooks", "14 skills") to user-facing text.**

The project deliberately avoids quantity-focused messaging. Use qualitative descriptions instead:

| ❌ Don't | ✅ Do |
|----------|-------|
| "22 rules loaded every session" | "Production-tested rules loaded every session" |
| "7 hooks auto-lint on every edit" | "Hooks auto-lint, format, type-check on every edit" |
| "14 coding skills" | "Coding skills activated dynamically" |
| "5 MCP servers + 3 LSP servers" | "MCP servers + language servers pre-configured" |
| "2,900+ lines of best practices" | "Production-tested best practices" |

**Why:** Quality over quantity. Counts become stale and create maintenance burden across many files. The value is in what the system does, not how many components it has.

## Workflow

1. **Search first** - Use Grep to find all occurrences:
   ```
   Grep pattern="old term" glob="*.{md,py,tsx,json,ts}"
   ```

2. **Update systematically** - Work through checklist above, section by section

3. **Verify consistency** - Search again to confirm no misses:
   ```
   Grep pattern="old term" glob="*.{md,py,tsx,json,ts}"
   ```

4. **Build website** - Verify site compiles after changes:
   ```bash
   cd docs/site && npm run build
   ```

## Common Updates

| Change Type | Key Locations |
|-------------|---------------|
| Command rename/add | pilot/commands/*.md, README.md, WorkflowSteps.tsx, WhatsInside.tsx, counts table |
| Skill rename | pilot/skills/*/SKILL.md, README.md, WhatsInside.tsx, DeepDiveSection.tsx |
| Rule add/remove | pilot/rules/*.md, README.md, all count locations (see table above) |
| Hook change | pilot/hooks/hooks.json, pilot/hooks/*.py, DeepDiveSection.tsx, README.md |
| Feature description | launcher/banner.py, README.md, site components, Index.tsx structured data |
| Workflow change | pilot/commands/*.md, pilot/rules/*.md, README.md, WorkflowSteps.tsx |
| Package rename | pyproject.toml, install.sh, launcher/__init__.py, README.md |
| Installer message | installer/*.py, installer/steps/*.py |
| Terminology change | Search all locations in checklist above — grep for old term, replace everywhere |
