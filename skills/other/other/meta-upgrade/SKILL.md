---
version: 2.0.0
name: meta-upgrade
description: >
  Upgrade installed workflow skills and templates from the agentic-workflow repo.
  Version-aware: compares semver versions, shows changelogs, warns about local
  adaptations. Use when the user says "upgrade the workflow", "update skills",
  "sync skills", "check for skill updates", or after pulling a new version of
  agentic-workflow.
disable-model-invocation: true
user-invocable: true
argument-hint: "[--all | --skills-only | --templates-only | --diff]"
---

# Upgrade — Sync Skills & Templates from agentic-workflow

Compares the installed workflow skills and templates against the source
agentic-workflow repo and offers selective upgrades.

## Step 1: Locate Source Repo

1. Read `workflow.json` in the current project root
2. Resolve `workflowRepo` path (e.g., `../agentic-workflow`)
3. If `workflow.json` doesn't exist or has no `workflowRepo`:
   - Ask the user for the path to the agentic-workflow repo
4. Verify the source repo exists and is accessible

## Step 2: Compare Skills (Version-Aware)

5. Read the source catalog: `<workflowRepo>/.claude/skills/meta-skill-catalog/catalog.json`
6. Read the local catalog: `.claude/skills/meta-skill-catalog/catalog.json`
7. For each skill in the source catalog, compare versions:

   **New skills** (in source but not local):
   - List them with name, category, description, and version
   - Mark as "Available to install"

   **Version comparison** (in both catalogs):
   - Compare `version` (source) vs `installed_version` (local)
   - Categorize by semver difference:
     - `up-to-date` — same version
     - `patch-available` — bug fixes, safe to auto-apply
     - `minor-available` — new features, review recommended
     - `major-available` — breaking changes, review required
   - Read the source skill's `CHANGELOG.md` and show entries between installed and current version

   **Ahead of source** (local `installed_version` > source `version`):
   - This means local modifications exist
   - Check `context/adaptations.md` for tracked adaptations
   - Warn: "This skill has local modifications. Run /meta-contribute-back before upgrading to preserve changes."

   **Local-only skills** (in local but not source):
   - These are project-specific skills — leave them untouched
   - List as "Project-specific (no upstream)"

## Step 3: Compare Templates

8. Resolve the docs repo path from `workflow.json`
9. Compare templates in `<workflowRepo>/templates/` against `<docsRepo>/templates/`
10. For each template:
    - **New**: Template exists in source but not in docs repo
    - **Updated**: Content differs between source and docs repo
    - **Unchanged**: Identical

## Step 4: Present Upgrade Report

11. Show the version-aware report:

```
### Workflow Upgrade Report

**Source:** <workflowRepo path>

#### Skills
| Skill | Installed | Current | Status |
|-------|-----------|---------|--------|
| meta-heartbeat | 1.0.0 | 1.1.0 | minor-available |
| doc-prd | 1.0.0 | 1.0.0 | up-to-date |
| dev-tdd-backend | 1.0.0 | 1.2.0 | minor-available (2 changes) |
| dev-verification-backend | 1.0.0 | 2.0.0 | major-available ⚠ |
| my-custom-skill | — | — | project-specific |

#### Changelog for Updated Skills

**dev-tdd-backend** (1.0.0 → 1.2.0):
- 1.2.0: Added Aspire integration test handling
- 1.1.0: Added event sourcing test patterns

**dev-verification-backend** (1.0.0 → 2.0.0):
- 2.0.0: BREAKING — Verification phases restructured
  ⚠ Review required before upgrading

#### Adaptation Warnings
⚠ dev-tdd-backend has 1 local adaptation (Aspire integration tests)
  Run /meta-contribute-back dev-tdd-backend before upgrading to preserve changes.
```

## Step 5: Apply Updates (After Approval)

12. Ask the user what to upgrade:
    - "Update all" — apply all updates and install new skills
    - "Update skills only" — skip templates
    - "Update templates only" — skip skills
    - "Let me pick" — interactive selection

13. For each approved update:

    **Skill updates:**
    - Back up the current SKILL.md to `SKILL.md.bak` (overwrite previous backup)
    - Copy the new SKILL.md from the source repo
    - Copy any new supporting files (references/, scripts/)
    - Update the local catalog entry
    - Update `installed_version` and `installed_date` in the local catalog entry

    **Skill installs (new):**
    - Create the skill directory
    - Copy SKILL.md and supporting files
    - Add to local catalog

    **Template updates:**
    - Copy the new template to the docs repo
    - Note: existing generated documents are NOT affected (only the template changes)

    **Template installs (new):**
    - Copy to docs repo templates directory
    - Create the output directory if it doesn't exist

14. Update the local catalog's `updated` date
    - Copy the skill's `CHANGELOG.md` from source (for local reference during future upgrades)

## Step 6: Post-Upgrade Verification

15. Run a quick check:
    - All installed skills have valid SKILL.md files
    - Catalog matches what's on disk
    - No orphaned skill directories
16. Report any issues found

## Step 7: Update Daily Memory

17. Log the upgrade in today's daily memory:
    - What was upgraded (skills, templates)
    - What was newly installed
    - What was skipped

## Flags

| Flag | Behavior |
|------|----------|
| `--all` | Update everything without prompting for selection |
| `--skills-only` | Only compare and update skills |
| `--templates-only` | Only compare and update templates |
| `--diff` | Show full content diffs for changed files |
| `--dry-run` | Show what would change without applying |

## Safety Rules

- **Never overwrite project-specific skills** (skills not in the source catalog)
- **Never modify context files** (SOUL.md, USER.md, MEMORY.md) — those are personal
- **Never modify workflow.json** — that's project-specific config
- **Never modify CLAUDE.md** — bootstrap handles that, not upgrade
- **Always back up before overwriting** (SKILL.md.bak)
- **Always show changes before applying** — no silent updates
