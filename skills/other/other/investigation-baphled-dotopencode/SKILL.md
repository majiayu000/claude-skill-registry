---
name: investigation
description: Systematic codebase investigation producing structured Obsidian documentation with DataviewJS auto-indexing
category: Workflow Orchestration
---

# Skill: investigation

## What I do

I conduct systematic codebase investigations using parallel agent exploration, synthesise findings into a structured set of Obsidian documents, and create auto-generated DataviewJS indexes for discovery and navigation. The output is a reproducible, searchable investigation record stored in the user's Obsidian vault.

## When to use me

- When conducting a discovery or audit of an application or codebase
- When asked to investigate, explore, or assess a project
- When producing structured findings for a codebase review
- When the user wants a documented record of a project investigation

---

## Investigation Workflow

### Phase 1: Plan
1. Identify project (name, language, entry point)
2. Identify vault (default: `/home/baphled/vaults/baphled/`)
3. Determine folder: `1. Projects/{Project}/Investigations/{YYYY-MM-DD}/`
4. Create todo list to track progress

### Phase 2: Explore (6 Parallel Agents)
Launch agents for: structure, architecture, debt, testing, CI/CD, documentation. Each returns metrics, file paths, and assessments.

### Phase 3: Synthesise Documents
Create 6 numbered documents:
- `00-Executive-Summary.md` — Good/Bad/Ugly, metrics, assessment
- `01-Architecture-Deep-Dive.md` — Layers, patterns, violations
- `02-Technical-Debt-Analysis.md` — Prioritised inventory
- `03-Testing-Strategy.md` — Coverage, gaps, patterns
- `04-CI-CD-Assessment.md` — Pipeline evaluation
- `05-Recommendations.md` — Action plan

### Phase 4: Create Auto-Generated Indexes
- **Project-level**: `Investigations.md` with DataviewJS auto-discovery
- **Dated page**: `{YYYY-MM-DD}.md` listing all documents

### Phase 5: Store in Memory
Create memory entities for key findings.

---

## Document Conventions

**Frontmatter**: Include title, date, type (discovery/investigation), project, status, created/modified timestamps.

**Cross-linking**: Use relative wikilinks (e.g., `[[01-Architecture-Deep-Dive]]`), not project-prefixed.

**Tags**: Add `#investigation #project-slug #YYYY-MM-DD #discovery` at bottom.

**Numbering**: `00-05` with kebab-case names (Executive-Summary, Architecture-Deep-Dive, etc.)

---

## DataviewJS Rules

- **ALWAYS** use `dv.table(headers, rows)` for tables
- **NEVER** use `dv.paragraph()` with markdown table strings
- Project-level index: auto-discover dated folders, render status grid
- Dated page: list all documents with status

---

## Folder Structure

```
1. Projects/{Project}/
  Investigations.md                 ← DataviewJS auto-index
  Investigations/{YYYY-MM-DD}.md    ← Dated page
  Investigations/{YYYY-MM-DD}/
    00-Executive-Summary.md
    01-Architecture-Deep-Dive.md
    02-Technical-Debt-Analysis.md
    03-Testing-Strategy.md
    04-CI-CD-Assessment.md
    05-Recommendations.md
```

---

## Anti-patterns to avoid

- ❌ Hardcoding data in indexes — use DataviewJS auto-discovery
- ❌ Using `dv.paragraph()` for tables — use `dv.table(headers, rows)`
- ❌ Prefixing wikilinks with project name — keep relative
- ❌ Running agents sequentially — launch all 6 in parallel
- ❌ Skipping memory storage — store findings as entities
- ❌ Manual index files — must be auto-generated
- ❌ Forgetting frontmatter — required on all documents
- ❌ Mixing assessment with raw data — Executive Summary assesses only

---

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Workflow-Orchestration/Investigation.md`

## Related skills

- `research` - General research methodology (investigation is a specialised form)
- `obsidian-structure` - PARA structure conventions for the vault
- `obsidian-dataview-expert` - DataviewJS queries and dashboards
- `memory-keeper` - Storing discoveries in the knowledge graph
- `parallel-execution` - Running exploration agents concurrently
- `note-taking` - General note creation conventions
