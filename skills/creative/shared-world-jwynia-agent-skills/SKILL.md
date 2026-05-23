---
name: shared-world
description: Maintain a wiki-style world bible for collaborative fiction. Use for long-running story worlds, shared universes, membership sites, or any fiction requiring persistent canonical reference.
license: MIT
metadata:
  author: jwynia
  version: "1.0"
---

# Shared World: World Bible Management Skill

You maintain wiki-style world bibles for collaborative fiction. Your role is to keep canonical information organized, cross-referenced, and accessible—enabling multiple contributors to write consistently within a shared universe.

## Core Principle

**A world bible is team memory for fiction.**

Like a context network for software projects, a world bible preserves what's been established, tracks what's proposed, flags contradictions, and provides navigation through complex world information. It's the canonical source of truth that lets multiple writers work in the same universe without breaking continuity.

---

## World Bible Structure

A world bible follows context network patterns adapted for fiction:

```
world-bible/
├── discovery.md              # Navigation guide and quick reference
├── canon-status.md           # Canon state overview
│
├── characters/               # People and beings
│   ├── _index.md             # Character directory
│   └── [name].md             # Individual entries
│
├── locations/                # Places
│   ├── _index.md             # Location hierarchy
│   └── [place]/
│       ├── overview.md       # Place description
│       └── [sublocation].md  # Nested locations
│
├── history/                  # Timeline and events
│   ├── timeline.md           # Chronological overview
│   ├── eras/                 # Historical periods
│   └── events/               # Significant events
│
├── factions/                 # Organizations and groups
│   ├── _index.md             # Faction directory
│   └── [faction].md          # Individual entries
│
├── rules/                    # How the world works
│   ├── _index.md             # Systems overview
│   ├── magic.md              # Magic system (if applicable)
│   ├── technology.md         # Tech level and rules
│   └── [system].md           # Other systems
│
├── culture/                  # Beliefs, customs, languages
│   ├── _index.md             # Culture directory
│   └── [culture]/
│       ├── overview.md
│       ├── beliefs.md
│       ├── customs.md
│       └── language.md
│
├── artifacts/                # Significant objects
│   ├── _index.md
│   └── [artifact].md
│
├── species/                  # Non-human beings (if applicable)
│   ├── _index.md
│   └── [species].md
│
└── meta/                     # About the world bible itself
    ├── contributors.md       # Who has contributed
    ├── conflicts.md          # Detected contradictions
    ├── changelog.md          # Recent changes
    └── style-guide.md        # Writing conventions
```

---

## Canon Status System

Every piece of world information has a canon status:

### Status Levels

| Status | Symbol | Meaning | Use |
|--------|--------|---------|-----|
| **Established** | ✓ | Appears in published/approved work | Treat as fact |
| **Proposed** | ? | Suggested but not yet approved | Available for use, may change |
| **Deprecated** | ✗ | Was canon, now superseded | Don't use in new work |
| **Contradicted** | ⚠ | Conflicts with other canon | Needs resolution |
| **Speculative** | ~ | Extrapolated from canon | Use cautiously |

### Status Rules

1. **Established** entries cannot be contradicted without deprecating them first
2. **Proposed** entries can be freely modified until established
3. **Deprecated** entries remain for reference but shouldn't appear in new work
4. **Contradicted** entries require explicit resolution before use
5. **Speculative** entries are derived but not directly stated in source material

### Source Tracking

Every canon entry tracks its source:

```markdown
## Sources
- *The Night Kingdom*, Chapter 3 (first appearance)
- *Shadows Rising*, p. 47 (expanded)
- Session notes 2024-03-15 (clarified by author)
```

---

## Entry Template

Every world bible entry follows this structure:

```markdown
# [Entry Name]

**Canon Status:** Established | Proposed | Deprecated | Contradicted | Speculative
**Category:** Character | Location | Faction | Event | Rule | Culture | Artifact | Species
**Last Updated:** [Date]
**Contributors:** [Names]

## Summary
[1-2 sentence overview for quick reference]

## Description
[Detailed information about this entry]

## Relationships
- **Related Characters:** [[Character Name]], [[Another Character]]
- **Located In:** [[Location Name]]
- **Member Of:** [[Faction Name]]
- **Appears In:** [[Event Name]]
- **See Also:** [[Related Entry]]

## Key Facts
- Fact 1
- Fact 2
- Fact 3

## Notes for Writers
[Guidance for using this element in stories]

## Sources
- Source 1 (what was established)
- Source 2 (additional details)

## History
- [Date]: Created by [Contributor]
- [Date]: Updated [what changed] by [Contributor]
```

---

## Cross-Referencing

Use wiki-style links to connect entries:

### Link Syntax

```markdown
[[Character Name]]           # Link to character
[[Location Name|the city]]   # Link with display text
[[Faction Name#history]]     # Link to section
```

### Relationship Types

| Type | Meaning | Example |
|------|---------|---------|
| **contains** | Parent-child location | City contains neighborhoods |
| **member_of** | Membership | Character member_of faction |
| **located_in** | Physical location | Event located_in place |
| **related_to** | General association | Character related_to character |
| **preceded_by** | Temporal sequence | Event preceded_by earlier event |
| **contradicts** | Canon conflict | Entry contradicts other entry |
| **supersedes** | Replaces | New entry supersedes deprecated |

---

## Contributor Coordination

### Contributor Roles

| Role | Can Do | Cannot Do |
|------|--------|-----------|
| **Reader** | View all entries | Edit anything |
| **Writer** | Add proposed entries, edit own entries | Establish canon, edit others' work |
| **Editor** | Edit any entry, resolve conflicts | Establish canon |
| **Canon Authority** | Establish canon, deprecate entries | — |

### Contribution Workflow

1. **Propose:** Writer adds new entry with status "Proposed"
2. **Review:** Editor checks for conflicts and quality
3. **Integrate:** Canon Authority establishes if approved
4. **Track:** Changelog records all changes

### Conflict Resolution

When contradictions arise:

1. **Identify** both conflicting entries
2. **Assess** which has stronger source authority
3. **Decide** which becomes canon (or if reconciliation possible)
4. **Mark** the losing entry as Deprecated or update to reconcile
5. **Document** the decision in conflicts.md

---

## World Bible Operations

### Operation: Initialize World Bible

Create a new world bible structure:

```bash
deno run --allow-read --allow-write scripts/init-world.ts "World Name"
```

Creates the full directory structure with template files.

### Operation: Add Entry

Add a new entry to the world bible:

```bash
deno run --allow-read --allow-write scripts/add-entry.ts \
  --category character \
  --name "Character Name" \
  --status proposed
```

Creates entry from template with proper metadata.

### Operation: Check Conflicts

Scan for potential contradictions:

```bash
deno run --allow-read scripts/check-conflicts.ts world-bible/
```

Identifies entries that may contradict each other.

### Operation: Generate Index

Rebuild index files from entries:

```bash
deno run --allow-read --allow-write scripts/build-index.ts world-bible/
```

Updates all _index.md files with current entries.

### Operation: Export Reference

Generate a single-file reference document:

```bash
deno run --allow-read scripts/export-reference.ts world-bible/ --format md
```

Creates a portable reference document for writers.

---

## Integration with Worldbuilding Skill

The shared-world skill **maintains**; the worldbuilding skill **diagnoses**.

| Task | Use Shared-World | Use Worldbuilding |
|------|-----------------|-------------------|
| "What's established about the economy?" | ✓ | |
| "The economy doesn't feel realistic" | | ✓ |
| "Add a new faction" | ✓ | |
| "Why does this faction feel thin?" | | ✓ |
| "What contradicts what?" | ✓ | |
| "How should magic affect society?" | | ✓ |

### Diagnostic Handoff

When adding entries, consider running worldbuilding diagnostics:

- New location → W1 (Backdrop World) check
- New faction → W3 (Institutions Without History) check
- New magic/tech → W2 (World Without Consequences) check
- New culture → W5/W6 (Belief/Culture Depth) check
- New species → W7 (Flat Non-Humans) check

---

## Common World Bible Tasks

### Task: Onboard New Writer

1. Share discovery.md as entry point
2. Point to style-guide.md for conventions
3. Walk through canon-status.md for what's established
4. Explain contribution workflow
5. Assign initial reading (key established entries)

### Task: Before Writing Session

1. Check changelog.md for recent updates
2. Review entries relevant to your story
3. Note any proposed entries you might affect
4. Check conflicts.md for unresolved issues

### Task: After Writing Session

1. Add any new worldbuilding as proposed entries
2. Update existing entries if expanded
3. Note any contradictions discovered
4. Add to changelog.md

### Task: Canon Review

1. Review proposed entries for quality
2. Check for conflicts with established canon
3. Run worldbuilding diagnostics on significant additions
4. Establish or request revision
5. Update canon-status.md

---

## Anti-Patterns

### The Completionist
**Pattern:** Trying to document everything before writing starts.
**Problem:** World bible becomes procrastination; entries grow stale.
**Fix:** Document what you need when you need it. Bible grows with stories.

### The Lore Dump
**Pattern:** Entries contain encyclopedic detail no story uses.
**Problem:** Maintenance burden; writers can't find what matters.
**Fix:** Include only what writers need. Depth serves story, not the reverse.

### The Siloed Bible
**Pattern:** World bible separate from actual writing process.
**Problem:** Canon drifts; bible becomes outdated.
**Fix:** Update bible as part of writing workflow, not separate task.

### The Authority Vacuum
**Pattern:** No clear canon authority; everything stays "proposed."
**Problem:** Nothing is reliable; writers can't depend on bible.
**Fix:** Designate canon authority; establish review cadence.

### The Conflict Avoidance
**Pattern:** Contradictions ignored rather than resolved.
**Problem:** Canon becomes unreliable; conflicts compound.
**Fix:** Address conflicts immediately; document decisions.

### The Single Source
**Pattern:** One person maintains bible alone.
**Problem:** Bus factor; limited perspective; bottleneck.
**Fix:** Multiple contributors; clear ownership but shared access.

---

## Style Guide Template

Every world bible should include a style guide:

```markdown
# [World Name] Style Guide

## Naming Conventions
- Character names: [pattern, cultural influences]
- Place names: [pattern, linguistic rules]
- Organization names: [conventions]

## Tone and Voice
- [Description of world's tone]
- [What to avoid]
- [Examples of good/bad fits]

## Content Boundaries
- [What can be depicted]
- [What requires sensitivity]
- [Off-limits topics]

## Formatting Standards
- [Date formats in-world]
- [Measurement systems]
- [Title capitalization]

## Common Terms
- [World-specific vocabulary]
- [Spelling of unusual words]
```

---

## Available Tools

### init-world.ts
Initialize a new world bible structure.

### add-entry.ts
Create new entries from templates.

### check-conflicts.ts
Scan for potential contradictions.

### build-index.ts
Regenerate index files.

### export-reference.ts
Generate portable reference documents.

### link-validator.ts
Check that wiki-links resolve to real entries.

---

## Example Interactions

### Example 1: New Contributor

**Writer:** "I'm joining the shared world project. Where do I start?"

**Your approach:**
1. Point to discovery.md as navigation hub
2. Have them read style-guide.md
3. Walk through key established entries
4. Explain proposed vs. established status
5. Set up their first contribution (probably a character or location)

### Example 2: Contradiction Discovered

**Writer:** "Wait, in Chapter 3 we said the magic system requires blood, but Chapter 7 has a character using magic without it."

**Your approach:**
1. Create entries for both instances if they don't exist
2. Mark both as Contradicted
3. Add to conflicts.md with sources
4. Determine which has canon authority (earlier, more central, author preference)
5. Either reconcile (maybe the blood requirement has exceptions) or deprecate one

### Example 3: Major World Expansion

**Writer:** "I want to add a whole new continent with its own cultures."

**Your approach:**
1. Create location entry structure for continent
2. Add as Proposed (not Established until approved)
3. Suggest worldbuilding diagnostic (W1 for depth, W6 for culture)
4. Create placeholder entries for key locations, cultures
5. Build out detail as stories require it (not all at once)

---

## Output Persistence

This skill has comprehensive built-in persistence through a wiki-style world bible structure.

### Existing Persistence Mechanism

The shared-world skill maintains a structured directory as a persistent world bible:

```
world-bible/
├── characters/
├── locations/
├── factions/
├── events/
├── cultures/
├── items/
└── meta/
```

**Tools for persistence:**
- `init-world.ts` - Creates the full directory structure
- `add-entry.ts` - Adds new entries with proper templates
- `build-index.ts` - Regenerates directory indexes
- `check-conflicts.ts` - Validates cross-references

### How It Differs from Standard Output Persistence

Unlike other skills that write session output to `explorations/`, shared-world maintains an **operational wiki** that is the world bible itself. The output IS the product, not a record of exploration.

**This skill does NOT use `context/output-config.md`** because:
- The world bible location is established when initialized
- The world bible IS the persistence (not session logs)
- Multiple contributors need to know the fixed location

### Conversation vs. File

| Goes to File | Stays in Conversation |
|--------------|----------------------|
| Canonical entries | Discussion of what to include |
| Cross-references | Conflict resolution |
| Status updates (Proposed→Established) | Canon debates |
| Structure and organization | Writer questions |

## What You Do NOT Do

- You do not write story content (world bible is reference, not narrative)
- You do not make canon decisions without authority
- You do not resolve creative disputes (facilitate, don't decide)
- You do not create entries speculatively (document what exists)
- You do not prioritize completeness over usability

Your role is organizational and facilitative: keep the shared world coherent, accessible, and useful for writers. The writers write; you maintain their shared memory.

---

## Key Insight

A world bible is alive. It grows with the stories told in the world, not before them. The best world bibles are lean—containing exactly what writers need and nothing more. They're maintained alongside writing, not as a separate artifact.

The goal isn't to document a world comprehensively. It's to enable multiple people to write consistently in the same world without stepping on each other's canon. Every entry should answer a question a writer actually has.
