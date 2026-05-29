---
name: reconcile
description: Audit a project against current plugin conventions and offer to update structure.
argument-hint: "[--apply] [--report]"
disable-model-invocation: true
---

Reconcile an existing fiction project with the current plugin conventions. This audits your project structure, identifies gaps or outdated patterns, and offers to scaffold missing sections.

Use this when:
- You've updated the fiction plugin and want to adopt new conventions
- You've been working on a project and want to ensure it follows best practices
- You're inheriting a project and want to understand what's missing

## What to Do

### 1. Find Project Root

Same as `/load` — look for README.md, chapters/, characters/ directories.

### 2. Audit Structure

Check for expected directories and files:

**Required:**
- [ ] `README.md` — Project overview
- [ ] `chapters/` — Chapter files

**Recommended:**
- [ ] `characters/` — Character documents
- [ ] `world/` — World/setting documents
- [ ] `craft/tone.md` — Voice guidance
- [ ] `themes.md` — Thematic content

**Build & Cover:**
- [ ] `builds/` — EPUB build outputs (date-organized)
- [ ] `covers/` — Cover artwork iterations
- [ ] `critiques/` — Critique outputs (date-organized)
- [ ] `synopses/` — Synopsis outputs (date-organized)
- [ ] `epub.css` — EPUB styling (if building)

### 3. Audit File Content

For each existing file, check for expected sections:

**README.md should have:**
- [ ] `## Anchored` — Immutable constraints (new convention)
- [ ] `## Key Decisions` — Tracked decisions
- [ ] `## Status` — Project status
- [ ] `## Chapters` — Chapter list

**Character files should have:**
- [ ] Want vs. Need
- [ ] Lie / Ghost / Flaw (for major characters)
- [ ] Voice notes

**For series projects, also check:**
- [ ] `series-architecture.md` with `## Anchored` section
- [ ] Book-level anchors that reference series anchors

### 4. Generate Report

Output a reconciliation report:

```markdown
## Reconciliation Report: [Project Name]

### Structure Status
- README.md exists
- chapters/ directory (X chapters)
- characters/ directory (X characters)
- craft/tone.md — missing
- themes.md exists
- builds/ — missing (create with `/fiction:build`)
- covers/ — missing (create for cover artwork)
- critiques/ — missing (create with `/fiction:critique`)
- synopses/ — missing (create with `/fiction:synopsis`)

### Content Audit

**README.md**
- Missing `## Anchored` section (new convention)
- Has `## Key Decisions`
- Has `## Status`

**Character: [Name]**
- Has Want/Need
- Missing Voice notes

[...continue for each file...]

### Recommendations

1. **High priority:** Add `## Anchored` section to README.md
2. **Medium priority:** Create craft/tone.md for voice consistency
3. **Low priority:** Add Voice notes to character files

### Would you like me to:
- [ ] Add missing sections to existing files (safe — adds, doesn't replace)
- [ ] Scaffold missing files from templates
- [ ] Both
```

### 5. Update progress.md

After auditing, update (or create) `progress.md` with:

```markdown
## Last Reconcile

**Date:** [Today's date]
**Plugin version:** [Current version if known]
**Issues found:** [Count]
**Issues resolved:** [Count of auto-fixed items]
```

Also update:
- Structure Audit checklist based on what exists
- Any chapter review entries if chapters were audited
- Notes section with summary of what was done

### 6. Apply Changes (If Requested)

If user approves:
- Add missing sections to existing files (append, don't overwrite)
- Create missing files from templates
- Update progress.md with resolved issues
- Report what was changed

**Important:** Never overwrite existing content. Only add missing sections.

## Arguments

```
/fiction:reconcile              # Reconcile project in current directory
/fiction:reconcile --apply      # Auto-apply safe changes without prompting
/fiction:reconcile --report     # Report only, don't offer changes
```

If arguments provided: $ARGUMENTS

## What This Checks

### New Conventions (v2+)
- `## Anchored` sections for immutable constraints
- Distinction between anchored and key decisions
- Cross-references between review tools

### Core Structure
- All expected directories exist
- Character files have complete information
- World files exist for settings mentioned in chapters
- Tone guide exists if project has specific voice

### Consistency
- Characters mentioned in chapters have character files
- Locations mentioned in chapters have world files
- Chapter numbering is sequential

## Notes

- Non-destructive by default — reports first, then asks
- Respects existing content — only adds, never replaces
- Works with both standalone and series projects
- Run periodically as the plugin evolves
