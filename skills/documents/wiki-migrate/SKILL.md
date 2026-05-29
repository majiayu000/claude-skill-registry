---
name: wiki-migrate
description: Migrate legacy wikis (phases/tasks in .plans/) to the new structure (workstreams/specs in docs/). Proposes a full migration plan, gets approval, then executes.
---

# Wiki Migration

Migrate legacy Obsidian wikis from phases/tasks structure to workstreams/specs structure.

## When to Use

- User has existing wiki in `.plans/` or other legacy location
- User wants to migrate to new `docs/` workstreams/specs structure
- User mentions "migrate wiki", "update wiki structure", "convert wiki"

## Migration Process

### Phase 1: Discovery & Analysis

1. **Find existing wiki:**
   ```
   Check: .plans/*/, docs/, wiki/
   Look for: README.md, CLAUDE.md, phases/, tasks/
   ```

2. **Analyze structure:**
   - Count phases, tasks, research files
   - Identify sub-wikis (nested structures with their own CLAUDE.md)
   - Map dependencies between files
   - Check for fragmentation (duplicate content)

3. **Identify workstreams:**
   - Group tasks by functional area (not by phase number)
   - Each major feature area = one workstream
   - Sub-wikis often map 1:1 to workstreams

### Phase 2: Propose Migration Plan

Present a complete migration plan to the user:

```markdown
## Migration Plan: [Project Name]

### Source
- Location: `.plans/refresh-browser/`
- Files: 112 markdown files
- Structure: 9 phases, 45 tasks, 3 sub-wikis

### Proposed Workstreams

| # | Workstream | Source | Files |
|---|------------|--------|-------|
| 01 | core-bridge | phases/00, 01, 05 | 12 |
| 02 | tabs-sidebar | phases/03 | 8 |
| 03 | devtools | research/devtools/ | 15 |
| 04 | context-menu | research/context-menu-bridge/ | 18 |

### File Transformations

| Old Path | New Path | Transform |
|----------|----------|-----------|
| phases/03-sidebar.md | workstreams/02-tabs-sidebar/README.md | Split into overview |
| tasks/3.1-tab-model.md | workstreams/02-tabs-sidebar/2.1-tab-model.md | Add behavior/ADR sections |

### Link Updates
- 234 wiki-links to update
- 12 cross-references between workstreams

### Risks
- [Any identified issues]

**Approve this plan? (y/n)**
```

### Phase 3: Execute Migration

After approval:

1. **Create new structure:**
   ```bash
   mkdir -p docs/workstreams/01-name
   mkdir -p docs/reference
   mkdir -p docs/research
   ```

2. **Transform files:**
   - Copy content to new location
   - Add missing sections (Behavior, Decisions, Integration)
   - Convert task format to spec format
   - Preserve ADR content where it exists

3. **Update wiki-links:**
   - Find all `[[old/path]]` references
   - Replace with `[[new/path]]`
   - Update relative paths

4. **Consolidate sub-wikis:**
   - Move sub-wiki content into workstream folders
   - Merge duplicate CLAUDE.md rules into workstream CLAUDE.md
   - Deduplicate any conflicting specs

5. **Create index files:**
   - Generate root README.md with workstream table
   - Generate workstream README.md with spec tables

6. **Generate/update CLAUDE.md with wiki operations:**
   - Preserve existing project-specific rules
   - Add wiki operations section (see template below)

### Phase 4: Validation

1. **Check for broken links:**
   ```bash
   grep -r '\[\[' docs/ | grep -v ']]'  # Unclosed links
   # Check each [[link]] resolves to a file
   ```

2. **Verify no content loss:**
   - Compare file counts
   - Spot-check key files

3. **Report results:**
   ```markdown
   ## Migration Complete

   - Migrated: 112 files → 89 specs
   - Consolidated: 3 sub-wikis → 3 workstreams
   - Updated: 234 wiki-links
   - Broken links: 0

   ### Next Steps
   - Review [[workstreams/01-name/README]]
   - Delete old `.plans/` directory when satisfied
   ```

## Spec Transformation Template

When converting a task file to a spec file:

**From (task):**
```markdown
# Task 3.1: Tab Model

**Phase:** 3 - Sidebar
**Commit:** `feat(tabs): implement tab model`

## Overview
Implement the tab data model...

## Steps
1. Create TabModel class
2. Add serialization

## Success Criteria
- [ ] Tabs persist across restart
```

**To (spec):**
```markdown
# 2.1 Tab Model

> **Workstream:** [[../README|02-Tabs-Sidebar]]

## Behavior

### Contract
- **Input:** Tab creation request (url, title)
- **Output:** Tab object with unique ID
- **Preconditions:** Browser window exists
- **Postconditions:** Tab persisted to storage

### Scenarios
- When tab created → assign unique ID, add to tab strip
- When browser closes → serialize all tabs to storage
- When browser opens → restore tabs from storage

## Decisions

### ADR-1: Tab Storage Format
- **Status:** Accepted
- **Context:** Need to persist tabs across restarts
- **Decision:** JSON file in user data directory
- **Consequences:** Human-readable, easy to debug
- **Alternatives:** SQLite (rejected: overkill for tab list)

## Integration

### Dependencies
- [[../01-core-bridge/1.1-storage|Storage Service]]

### Consumers
- [[2.2-tab-strip|Tab Strip UI]]
- [[../03-devtools/3.1-panel|DevTools Panel]]
```

## CLAUDE.md Wiki Operations Template

Add this section to the project's CLAUDE.md after migrating:

```markdown
## Wiki Operations

This documentation lives in an Obsidian vault (`docs/`). Follow these patterns.

### Progressive Disclosure

**Don't load everything.** Navigate in layers:

1. **Start at workstream README** - `workstreams/##-name/README.md`
   - Understand scope and current status
   - See which specs exist
   - Check dependencies

2. **Read specific specs as needed** - `workstreams/##-name/#.#-spec.md`
   - Load only the spec you're implementing
   - Check "Integration" section for related specs

3. **Dive into reference docs for deep context** - `reference/` or `workstreams/##-name/reference/`

4. **Check research for background** - `research/topic/`

### Spec File Format

```markdown
# #.# Spec Title

[← Back to Workstream](README.md)

## Behavior
What the component does (contract, files to create/modify)

## Decisions
**Assumptions:** numbered list with implications if wrong
**Failure modes:** table with Detection/Recovery
**Open questions:** %% [ ] items %%

## Integration
Dependencies, APIs, build integration

## Success Criteria
- [ ] Testable outcomes
```

### Updating Specs During Implementation

**Before:** Read Assumptions and Failure Modes
**During:** Mark open questions resolved, note discoveries
**After:** Update Success Criteria, update README status

### Link Format

| Target | Format |
|--------|--------|
| Same directory | `[text](filename.md)` |
| Parent | `[text](../README.md)` |
| Subdirectory | `[text](reference/file.md)` |
| Cross-workstream | `[text](../06-name/README.md)` |

### When to Create New Docs

| Situation | Action |
|-----------|--------|
| New feature area | Create new workstream |
| New task in workstream | Create numbered spec |
| Deep technical topic | Add to `reference/` |
| Research question | Use Oracle, save to `research/` |
```

## Best Practices

1. **Preserve history** - Keep old wiki until migration verified
2. **One approval** - Show full plan, don't interrupt during execution
3. **Transform, don't just move** - Add missing spec sections
4. **Consolidate fragmentation** - Merge duplicate sub-wikis
5. **Validate links** - Every `[[link]]` must resolve
6. **Include wiki operations** - CLAUDE.md must explain how to use the wiki
