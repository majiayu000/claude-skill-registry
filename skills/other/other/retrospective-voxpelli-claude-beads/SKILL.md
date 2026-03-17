---
name: retrospective
description: "Run a sprint retrospective for this project. Use when the user says 'retrospective', 'retro', 'sprint review', 'close out the sprint', 'what went well', or wants to generate a RETRO-NN.md file. Reads UPSTREAM-*.md files, recent git history, and conversation context to pre-populate the retrospective."
user-invocable: true
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - Grep
  - Bash
  - Skill
  - mcp__basic-memory__search_notes
  - mcp__basic-memory__read_note
  - mcp__basic-memory__write_note
  - mcp__basic-memory__edit_note
  - mcp__basic-memory__schema_validate
  - mcp__basic-memory__schema_diff
  - mcp__basic-memory__schema_infer
---

# Sprint Retrospective

Generate a sprint retrospective for this project. If the project `CLAUDE.md` has
a Sprint retrospectives section with a template, use it; otherwise use the
template below.

## Context

Retrospective files are named `RETRO-NN.md` in the project root. Each covers one
sprint's worth of work.

## Workflow

### 1. Determine sprint number

```bash
ls RETRO-*.md | sort -V | tail -1
```

Extract the highest sprint number and increment by 1.

### 2. Gather context

Run these in parallel:

**Recent commits since last retro:**

```bash
# Anchor to the commit that created/last modified the previous RETRO file.
# Edge cases that both result in full-history range (correct for Sprint 1):
#   1. No prior RETRO-*.md files exist yet
#   2. RETRO files are gitignored — git log -- RETRO-*.md returns empty
# In both cases the inner git log returns empty, making the range "..HEAD"
# which shows all commits — the right behavior for a first retrospective.
git log --oneline "$(git log -1 --format=%H -- RETRO-*.md)"..HEAD --no-merges
```

**Current upstream status:**

- Glob for all `UPSTREAM-*.md` files and read them
- Count open items per file and per section

**Recent conversation context:**

- Review the current session for friction, workarounds, discoveries, and
  decisions made during development

**Test and coverage status:**

Check `package.json` scripts for a test command. Try in order:

1. `npm test` (if a `test` script exists)
2. `npm run test:node` (if a `test:node` script exists)
3. `npm run test` (if a `test` script exists under another variant)

Run the first that exists and show the last 5 lines of output.

### 3. Draft the retrospective

Create `RETRO-{N}.md` using this template:

```markdown
## Sprint {N} Retrospective — {YYYY-MM-DD}

### What went well

- ...

### What could improve

- ...

### Upstream observations

<!-- Review recent work — anything to add to UPSTREAM-*.md files? -->

- ...

### Lessons learned

- ...
```

**Section guidelines:**

- **What went well** — concrete wins: bugs caught, patterns established, clean
  commits, test improvements. Reference specific files/commits. Focus on process
  and engineering quality, not just features shipped.
- **What could improve** — honest assessment of friction, false starts, wasted
  effort. Not a blame list — focus on systemic issues and what would prevent
  recurrence.
- **Upstream observations** — summarize current state of all UPSTREAM files.
  Log any NEW friction discovered in the session to the appropriate UPSTREAM
  file using `/upstream-tracker` (workflow 1). Note trends across packages.
  Flag stale items (>3 months old).
- **Lessons learned** — reusable insights. Each should be a principle that
  future sessions can apply, not a one-off fact. Format: **Bold principle** —
  supporting evidence from this sprint.

### 4. Check for trend review

If this is every 4th sprint (Sprint 4, 8, 12, ...), also perform a trend review:

**UPSTREAM files:** Review all `UPSTREAM-*.md` files — identify common trends,
evaluate whether open items are still valid, delete non-vendor files with no
remaining entries.

**Beads health:** Run `bd stats` and review issue hygiene:

- Stale `in_progress` issues (claimed but not worked in 2+ sprints)
- Completed work that was never closed (`bd list --status in_progress`)
- Blocked issues whose blockers have been resolved (`bd blocked`)
- Issues that should be compacted (`bd compact` for old closed issues)

**Basic Memory graph health** (via Basic Memory MCP tools):

1. Run the knowledge-gardener agent for automated audit (orphans, schema, stale notes, duplicates)
2. Validate both schemas: call `mcp__basic-memory__schema_validate` with `note_type="npm_package"` and again with `note_type="engineering"`
3. Call `mcp__basic-memory__schema_diff` on both types to detect drift (new observation categories in use but not in schema, or schema fields rarely used)
4. If notes cluster around a new unschemaed `type`, call `mcp__basic-memory__schema_infer` and consider creating a new schema
5. Verify all notes have: frontmatter `type` and `tags`, `## Observations`, `## Relations`
6. Flag notes missing any layer; fix or create beads issues

**Basic Memory notes (project-independent knowledge base):** Basic Memory is a
cross-project knowledge store — notes there must be written from a general
engineering perspective, not referencing project-specific file paths, table names,
or project structure. Vendor package names (e.g., `@scope/vendor-package`) are
fine since they're real npm packages. Mentioning this project by name is okay
when genuinely relevant — just don't make notes only useful within this project.
Call `mcp__basic-memory__search_notes` and:

- Update notes that have been superseded by new learnings this sprint
- Remove notes that are too project-specific — generalize or delete
- Check for duplicate notes across directories and merge them
- Verify tags are consistent and discoverable

### 5. Create beads issues from findings

Review the "What could improve" and "Lessons learned" sections for actionable
items that aren't already tracked. Create beads issues for each:

```bash
bd create "..." -t bug|task|feature|chore -p N --description "..."
```

(`-t` = type; `-p` = priority: 0=critical, 1=high, 2=medium, 3=low, 4=backlog)

Include code quality issues, process improvements, and any findings that need
follow-up work. Skip items that are purely observational or already have open
issues.

### 6. Knowledge gap audit

Run `/knowledge-gaps` (if vp-knowledge is installed):

`/knowledge-gaps` scans all package manifests in the project (npm, Rust crates,
Go modules, PHP Composer, Python PyPI, Ruby gems) and tool manifests (Brewfile,
GitHub Actions workflows, Dockerfile, VSCode extensions). It cross-references
each dependency against Basic Memory notes to identify undocumented packages and
tools.

Steps:

1. Run `/knowledge-gaps` — it handles all manifest types automatically. If
   vp-knowledge is not installed, skip this step and note in the retrospective
   under "What could improve" that knowledge gap coverage was not audited.
2. Include Tier 1 gaps in the retrospective under "What could improve"
3. Create beads issues for the top 3 undocumented packages or tools

### 7. Write project-independent learnings to Basic Memory

Basic Memory is a **cross-project knowledge base** — it persists across all
repositories and sessions. Notes written here must be generalizable engineering
knowledge, not project-specific implementation details. Ask: "Would this note help
me on a completely different project using the same technology?" If yes, write it.
If it only makes sense in the context of this codebase, it belongs in `MEMORY.md`
or the project `CLAUDE.md` instead.

For each learning, search first, then create or update:

- If no matching note exists: call `mcp__basic-memory__write_note` to create it
- If a note exists with new content: call `mcp__basic-memory__read_note` first
  to get exact content, then call `mcp__basic-memory__edit_note` with
  `find_replace` or `replace_section` — never call `write_note` on an existing
  note (it requires `overwrite=True` and risks replacing the full note content)

Organize by engineering domain:

| Directory | Topics |
|-----------|--------|
| `engineering/fastify/` | Plugin patterns, lifecycle, error handling |
| `engineering/frontend/` | Web components, CSS, dark mode, SSR, a11y |
| `engineering/database/` | Query patterns, migrations, PostgreSQL |
| `engineering/testing/` | Test conventions, infrastructure, coverage |
| `engineering/tooling/` | Linter config, build pipelines, knip |
| `engineering/agents/` | Orchestration, workflow, quality gates |

**Guidelines:**

- Only write notes for patterns confirmed this sprint — not speculative
- Use concrete code examples, not abstract principles
- Tag notes for discoverability
- **No project-specific internals** — replace project file paths with generic
  descriptions (e.g., "route handler file" not "lib/routes/settings.js"),
  omit table names, and describe patterns in terms of the technology, not
  the application. Referencing vendor packages by npm name (e.g.,
  `@scope/vendor-package`) is fine — they're real published packages.
  Mentioning this project by name is okay when genuinely relevant — just
  don't make the note only useful within this project.
- **Division of labor with upstream-tracker.** This step writes `engineering/*`
  notes (patterns, conventions, lessons learned). For upstream friction about
  specific packages or tools, use `/upstream-tracker` workflow 6 (Promote to
  Basic Memory) instead — it writes to the `## Upstream Friction` section of
  entity notes (`npm/*`, `brew/*`, etc.), avoiding duplication. For packages
  not yet in Basic Memory, suggest `/package-intel` or `/tool-intel` for
  enrichment first.

### 8. Suggest documentation updates

After writing the retro, suggest updates to:

- Project `CLAUDE.md` — new conventions, gotchas, or commands discovered
- `MEMORY.md` — stable patterns confirmed across sprints
- `README.md` — if project structure or commands changed

Present suggestions to the user for approval before editing.
