---
name: record-knowledge
description: >-
  Record tacit knowledge — quirks, pitfalls, dependencies, decisions, root causes — as tagged
  Markdown entries in `.claude/knowledge/entries/`. Use this skill whenever discoveries are made
  during work, when the user shares undocumented system behavior, or at plan completion to capture
  lessons learned. Also use when Claude Code makes a mistake pointed out by the user — record what
  happened, why it was wrong, and what to do next time.
license: MIT
allowed-tools: Read, Grep, Glob, Edit, Write
---

# Record Knowledge

## Goal
Capture tacit knowledge discovered during work and make it available for future sessions.

## When to Reference
- **New session start**: Search `.claude/knowledge/entries/` for active entries related to the current task before starting work
  - If an `overview` entry exists for the topic, read it first — load `detail` entries on demand to save context
- **Progress update**: Check if related entries need updating based on new discoveries
- Not needed when resuming a session (context is already preserved)

## When to Record
- Undocumented behavior, quirks, or pitfalls
- Hardware/service characteristics shared by the user
- Dependencies or coupled settings discovered during configuration
- Decision rationale (why a particular approach was chosen)
- Root causes and fixes found during troubleshooting
- **Claude Code's own mistakes and prevention measures** — errors pointed out by the user, incorrect output, tool misuse, etc. Record specifically: what happened, why it was wrong, and what to do next time. Tag with `#pitfall`
- **Environment-specific behavior** — when a discovery is tied to a specific PC, OS, network, or toolchain version (e.g., proxy issues at office, build differences between WSL and native Linux), include the environment details (hostname, OS, network type, etc.) in the entry body. Tag with `#environment-specific`. This aids retrospective fact-checking when the same user or team works across multiple environments

## Setup

Copy `assets/knowledge-CLAUDE.md` to `.claude/knowledge/CLAUDE.md`:

```bash
mkdir -p .claude/knowledge/entries
cp assets/knowledge-CLAUDE.md .claude/knowledge/CLAUDE.md
```

This creates the tag registry and search reference used by the skill.

## Recording Flow

1. Create `.claude/knowledge/entries/YYYY/MM/YYYYMMDD-HHMMSS-author-slug.md` with YAML frontmatter
2. For new discoveries without enough detail yet, write a temporary note in the working directory and convert to an entry later
3. Do NOT add links to subdirectory `CLAUDE.md` files — use tag search to find entries instead
4. Claude Code acts autonomously — create and edit entries without asking for user confirmation

## Entry Location
- `.claude/knowledge/entries/YYYY/MM/YYYYMMDD-HHMMSS-author-slug.md` — one file per entry, organized by year/month
- Timestamp prefix ensures chronological ordering and collision avoidance
- Author field uses your Git hosting platform account name (without `@`)
- Slug is descriptive kebab-case
- Example: `2026/03/20260302-143052-alice-docker-compose-port-conflict.md`
- Create `YYYY/MM/` subdirectory if it doesn't exist
- Legacy flat entries (directly under `entries/`) remain functional — migrate with `scripts/migrate-to-dated-dirs.py`

## Entry Format (YAML Frontmatter)
```markdown
---
title: <title>
author: "@<username>"
created: YYYY-MM-DD
status: draft | active | superseded | deprecated
type: knowledge | overview | detail | fragment | synthesis
confidence: low | mid | high
superseded_by: YYYY/MM/newer-entry-slug.md   # only when status: superseded
tags: "#tag1 #tag2 ..."
---

<body — concrete facts, procedures, code examples, etc.>

- ref: [display text](URL or relative path)
- see: [related entry title](YYYY/MM/slug.md) — relationship description
```

- Keep entries focused and under **100 KB** where possible. If approaching **1 MB**, split into multiple focused entries (one pitfall, one decision, one root cause per entry). Large entries degrade context loading precision in future sessions
- When creating an entry that exceeds **300 lines**, consider splitting it immediately using the split procedure below
- `type` is optional — defaults to `knowledge` if omitted

### Entry Types

| Type | Meaning | When to Use |
|------|---------|-------------|
| `knowledge` | Standalone verified fact (default) | Most entries — independent pieces of knowledge |
| `overview` | Topic entry point with summary and detail links | When 3+ detail entries exist for a topic |
| `detail` | Focused entry referenced from an overview | Deep-dive into a specific aspect of a topic |
| `fragment` | Isolated observation, not yet promoted | Quick notes that may become knowledge later |
| `synthesis` | Cross-cutting insight from multiple entries | Integrating patterns across entries (#27) |

### Overview Entries

Overview entries serve as **topic entry points** that reduce context consumption:

- Add `topic: <topic-name>` to frontmatter (lowercase kebab-case)
- Include a `## Detail Entries` section listing related detail entries via see links
- On session start, read the overview first; load detail entries on demand
- Consider creating an overview when 3+ entries share the same primary tag

```markdown
---
title: "Docker — Overview"
type: overview
topic: docker
status: active
tags: "#docker"
---

Summary of Docker-related knowledge.

## Detail Entries
- see: [Port conflict resolution](YYYY/MM/slug.md) — common port conflicts
- see: [Build cache pitfalls](YYYY/MM/slug.md) — cache invalidation issues
```

### Tag Guidelines
- Claude Code assigns tags autonomously for optimal searchability
- Naming: lowercase kebab-case with `#` prefix (e.g., `#docker`, `#typescript`, `#pitfall`)
- Add new tags freely as needed
- Check the tag registry in `.claude/knowledge/CLAUDE.md` before creating new tags to avoid duplicates

#### Similarity Check (on every entry creation)
Before assigning tags to a new entry, scan the tag registry for near-duplicates:
- **Singular/plural**: `#backup` vs `#backups` → use the existing form
- **Abbreviation/full**: `#k8s` vs `#kubernetes` → use the existing form
- **Synonym**: `#error` vs `#bug` → use the existing form
- **Substring overlap**: `#windows-service` vs `#win-service` → use the existing form
If a near-duplicate is found, reuse the existing tag. Do not create a new one.

### ref / see Link Format
- Use Markdown links for URLs and repo paths (clickable in your Git hosting platform's web UI)
  - External: `- ref: [title](https://example.com/...)`
  - In-repo: `- ref: [path](../../../relative-path)` (relative from `.claude/knowledge/entries/`)

### see Links (Synapse Formation Between Entries)
- Add `see:` links to related entries when creating or editing an entry
- Within `entries/`, use entries/-relative paths: `- see: [title](YYYY/MM/slug.md) — relationship`
- Describe the relationship briefly after `—` (e.g., "another port conflict", "prerequisite step")
- Relevance criteria:
  - **Sequential steps**: procedure step dependencies, workflow stages
  - **Same technology, different pitfalls**: multiple gotchas for one tool
  - **Prerequisite → application**: setup steps → usage caveats
  - **Design decision ↔ rationale**: architecture choice ↔ supporting evidence
- Bidirectional links by default (if A → B, add B → A too)
- When adding a new entry, update related existing entries with see links

## Status Definitions

| Status | Meaning | Claude Code Behavior |
|--------|---------|---------------------|
| `draft` | Unverified fragment | Reference with caution. Do not use as basis for decisions |
| `active` | Verified, current knowledge | Use as basis for decisions |
| `superseded` | Replaced by a newer entry | Do not reference; follow `superseded_by` link to the replacement |
| `deprecated` | Obsolete, no longer relevant | Do not reference; use only for historical context |

### Confidence Levels

| Level | Meaning | When to Use |
|-------|---------|-------------|
| `low` | Anecdotal or unverified | Observed once, not yet reproduced or confirmed |
| `mid` | Partially verified | Reproduced or confirmed in some contexts |
| `high` | Well-established fact | Verified multiple times, documented, or widely known |

- `confidence` is optional — omit if not applicable
- `draft` entries typically have `confidence: low`
- Promote `confidence` as knowledge is verified through use

### Correction Flow (superseded)

When an entry is found to be incorrect:
1. Set `status: superseded` and add `superseded_by: YYYY/MM/newer-entry-slug.md`
2. Create the replacement entry with a `- see:` link: `corrects [original title](YYYY/MM/original.md)`
3. Keep the original entry intact — it preserves why the incorrect belief was held, useful for retrospective learning
4. Do NOT delete or overwrite the original content

## Entry Granularity

**1 entry = 1 topic.** A topic is the smallest unit of knowledge that is useful on its own.

Splitting guidelines:
- 1 pitfall → 1 entry
- 1 design decision + rationale → 1 entry
- 1 root cause + fix → 1 entry
- Background shared by multiple entries → `type: fragment` or a referenced `synthesis` entry

When recording from a large context (e.g., session output):
1. Identify distinct topics within the context
2. Create 1 entry per topic
3. Link related entries with `- see:`

### Synthesis Entries

A `synthesis` entry distills patterns and principles from multiple related entries. It represents the author's internalized understanding, not just recorded facts.

```markdown
---
title: "My approach to NixOS system configuration"
type: synthesis
status: active
confidence: high
tags: "#nixos #system-config"
sources:
  - YYYY/MM/entry-a.md
  - YYYY/MM/entry-b.md
  - YYYY/MM/entry-c.md
---

Distilled understanding from experience.
Not just facts — the author's own perspective and principles.

- see: [entry-a](YYYY/MM/entry-a.md) — source
- see: [entry-b](YYYY/MM/entry-b.md) — source
```

- `sources:` lists the entries that were synthesized (entries/-relative paths)
- Synthesis entries do NOT replace source entries — sources remain `active`
- On session start, prefer `synthesis` over individual `knowledge` entries for the same topic (reduces context consumption)

## Amendment Rules
- Entries are **mutable** — edit in place (git tracks change history)
  - Adding info, corrections, supplementary examples → edit directly
  - Use `git log entries/<slug>.md` to review change history
- Use `deprecated` only when knowledge is genuinely obsolete
  - Example: service decommissioned, fundamental spec change, "should no longer be referenced"
- Use `superseded` when an entry is replaced by a corrected version (see Correction Flow above)

## Splitting Large Entries

When an entry exceeds 300 lines or approaches 100 KB, split it into an **index + sub-entries** structure:

### Split Structure
```
entries/YYYY/MM/
├── YYYYMMDD-HHMMSS-author-topic.md          ← Index (type: overview)
└── YYYYMMDD-HHMMSS-author-topic/
    ├── section-one.md                        ← Sub-entry (type: detail)
    ├── section-two.md                        ← Sub-entry (type: detail)
    └── section-three.md                      ← Sub-entry (type: detail)
```

### Split Procedure
1. Create a subdirectory next to the original entry with the same base name (without `.md`)
2. Move each major section (`## heading`) into its own file in the subdirectory
3. Convert the original entry into an index (`type: overview`) with:
   - Brief summary of the topic
   - `## Detail Entries` section with see links to each sub-entry
4. Each sub-entry gets its own frontmatter (`type: detail`, same tags as parent)
5. Sub-entries use simple filenames (no timestamp prefix needed — the parent directory provides context)

### When to Split
- Entry exceeds **300 lines** during creation → split immediately
- Existing entry grows past **300 lines** through edits → propose split
- `review-knowledge` reports an entry as oversized → split in fix mode

## Procedure
1. Extract knowledge from user input or work discoveries
2. Read the tag registry in `.claude/knowledge/CLAUDE.md`
3. Select tags — reuse existing tags; check for near-duplicates before creating any new tag
4. **Find related entries** (see link candidates) — run before writing so links are included from the start:
   a. **Tag search**: Grep `entries/` for each tag assigned in step 3 (e.g., `Grep pattern="#docker" path=".claude/knowledge/entries/"`)
   b. **Keyword search**: Grep for 2–3 distinctive terms from the title or body (tool names, error messages, config keys)
   c. **Narrow results**: Skip `deprecated` entries. From the remaining hits, read titles and tags to judge relevance using the criteria in "see Links (Synapse Formation Between Entries)"
   d. **Prepare links**: For each related entry, draft a `- see:` line with a brief relationship description
5. Create `.claude/knowledge/entries/YYYY/MM/YYYYMMDD-HHMMSS-author-slug.md` (or edit existing entry) — include the see links drafted in step 4
6. **Tag registry update (mandatory)**: If a new tag was created, add it to the tag registry in `.claude/knowledge/CLAUDE.md` **within the same operation** — do not defer this step. Use `scripts/regenerate-tag-registry.py --write` for bulk maintenance
7. **Add backlinks**: For each entry linked in step 4, edit that entry to add a reciprocal `- see:` link pointing back to the new entry
8. Briefly notify the user what was recorded and which entries were linked (no confirmation needed beforehand)
