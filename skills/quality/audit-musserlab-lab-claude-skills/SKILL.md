---
name: audit
description: Periodic project health check - cross-check docs, prune conventions, find drift. Use when project documentation feels stale, before milestones, or when CLAUDE.md is getting long.
user-invocable: true
---

# Project Audit

When the user invokes `/audit`, perform a thorough health check of project documentation and conventions. This is a periodic maintenance task — not needed every session, but valuable before milestones, after intensive work periods, or when things feel out of sync.

---

## 0. Detect Project Type

Check the project's `.claude/CLAUDE.md` for a `project-type:` field:

- **`data-science`** — Full audit including all steps
- **`general`** (or no field found) — Skip steps marked **[Data Science only]**

---

## 1. Cross-Check CLAUDE.md Against Planning Documents

The main project CLAUDE.md should not maintain script or file lists that duplicate planning documents. Check for staleness:

1. Read the Project Document Registry in the project CLAUDE.md
2. For each registered planning document, read it and compare against the main CLAUDE.md:
   - Are any scripts referenced in CLAUDE.md marked as legacy/inactive in planning docs?
   - Does CLAUDE.md have stale lists that duplicate planning doc tables?
3. For stale/duplicated lists, propose:
   - **Replace** with a pointer to the planning document (preferred — avoids future drift)
   - **Update** to match (only if a summary is genuinely useful in CLAUDE.md)

---

## 2. Planning Document Health

For each registered planning document, check internal health:

1. **Uncollapsed completed phases** — Are there completed phases with detailed content (>10 lines) that should be collapsed to 3-5 line summaries? Report line counts per phase.
2. **Stale "Next Session" sections** — Does a "Next Session" or "Open Tasks" section contain items that appear to have been done already (based on status tables or completed phases)?
3. **Status table accuracy** — Are phases marked "Not started" that have actually been worked on, or "In progress" for work that's clearly complete?
4. **Overall size** — Report line count and KB for each planning doc. Flag any over 300 lines as candidates for collapsing.

---

## 3. Check for Unregistered Documents and Scripts

### Documents

Scan `.claude/` for `.md` files not listed in the Project Document Registry. Propose adding any missing ones to the appropriate category table.

### Scripts

Check if any scripts in `scripts/` are not tracked in any planning document. For untracked scripts that relate to ongoing work, suggest either:
- Adding them to an existing planning document
- Creating a new planning document with `/new-plan`

### Data files [Data Science only]

Check if any significant data files were created but not added to the Canonical Data Files Registry.

---

## 4. Script Lifecycle Status [Data Science only]

For projects using the script organization conventions:

1. **Missing status fields**: Check `.qmd` scripts for missing `status:` YAML frontmatter
2. **Status/reality mismatch**: Flag scripts marked `finalized` that have been modified since their last commit, or `development` scripts that appear complete
3. **Planning doc sync**: Verify YAML frontmatter status matches the relevant planning document's tracking table

---

## 5. Prune Self-Evident Conventions

Review existing convention entries in the project's `.claude/CLAUDE.md`. For each, ask: **Is this now self-evident from the codebase?**

A convention is self-evident when:
- The pattern is consistently established across the project's files
- Claude would infer it from reading any few files
- Removing the entry wouldn't cause Claude to do the wrong thing

Propose removing redundant entries. Show which entries would be pruned and why.

**Be conservative** — only prune conventions that are truly obvious from the code. When in doubt, keep the entry.

---

## 6. Project CLAUDE.md Size Check

Report the current size of the project CLAUDE.md (line count, approximate KB). If it's growing large (>300 lines), suggest:
- Moving detailed sections into planning documents
- Extracting complex conventions into skills
- Replacing inline tables with pointers to planning docs

---

## 7. User-Level Health Check

Quick checks on user-level configuration (lightweight — skip silently if everything is fine):

1. **MEMORY.md size** — Check `~/.claude/projects/*/memory/MEMORY.md` for the current project. If over 200 lines, flag for pruning.
2. **User CLAUDE.md size** — Check `~/.claude/CLAUDE.md` line count. If over 150 lines, suggest extracting content into skills.
3. **Skills scan** — For each skill in `~/.claude/skills/`:
   - **Path drift**: Grep for absolute user paths (e.g., `/Users/<username>/`) that should be `~/`. This is the most common skill issue — paths leak in during in-session edits.
   - **Lab repo sync**: Compare each personal skill against the lab skills repo (if one exists). Flag files that differ. Path differences (absolute vs `~/`) count as sync issues.
   - **Description accuracy**: Read the `description:` frontmatter — does it still match the skill's actual scope? Flag overly broad or narrow triggers.
   - **Stale references**: Spot-check any file paths, column names, or package names mentioned in skills against the current project state. Only check references relevant to the current project.
   - Report only actual issues found. Skip this step's output entirely if all skills are healthy.

---

## 8. Summary

Report findings organized as:
- **Issues found** — things that need fixing (stale references, unregistered files, uncollapsed phases, etc.)
- **Suggestions** — optional improvements (convention pruning, size reduction)
- **All clear** — areas that checked out fine

Ask the user which findings they'd like to act on before making any changes.
