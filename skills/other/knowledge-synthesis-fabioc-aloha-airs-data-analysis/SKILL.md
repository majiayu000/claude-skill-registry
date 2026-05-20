---
name: "knowledge-synthesis"
description: "Cross-project pattern recognition — abstract, generalize, connect, store at the highest true level"
applyTo: "**/*knowledge*,**/*insight*,**/*pattern*,**/*global*"
---

# Knowledge Synthesis Skill

> Extract the reusable from the specific. Store at the highest level that remains true.

## The Synthesis Process

### 1. Abstract — Strip project-specific details

| Before (project-specific) | After (abstracted) |
| ------------------------- | ------------------ |
| "In Alex extension, synapses.json breaks when files are renamed" | "Connection metadata breaks when target files are renamed" |
| "We migrated knowledge files to skills/" | "When reorganizing knowledge files, update all internal references" |
| "Alex's dream runs brain-qa.ps1" | "Automated health checks should run validation scripts" |

**Test**: Would this insight help someone who's never seen this project?

### 2. Generalize — Find the abstraction level

| Level | Example | Store As |
| ----- | ------- | -------- |
| Project-specific | "Alex uses synapses.json" | Don't store globally |
| Technology-specific | "JSON schema files break silently on rename" | GI-* insight |
| Architecture pattern | "Self-referencing metadata needs rename-aware tooling" | GK-* pattern |
| Universal principle | "Metadata that references other files is fragile by nature" | GK-* (high value) |

**Store at the highest level that remains true.** If generalizing makes it wrong, stay specific.

### 3. Connect — Link to existing knowledge

Before creating new knowledge, check: does this extend an existing pattern?

| Signal | Action |
| ------ | ------ |
| "We solved this before in project X" | Extend existing GK-* with new example |
| "This is the third time I've seen this" | Promote from insight (GI-*) to pattern (GK-*) |
| "This contradicts what we knew" | Update existing pattern, note the exception |
| "This is entirely new" | Create new GI-* insight, observe before promoting |

### 4. Store — Right format, right location

| Type | Prefix | Criteria | Location |
| ---- | ------ | -------- | -------- |
| Pattern | GK-* | Proven in 2+ projects, abstracted, actionable | `patterns/` |
| Insight | GI-* | Single observation, timestamped, may not generalize | `insights/` |

**Quality bar**: 10 great patterns > 100 mediocre notes.

## Pattern Triggers

| Signal During Work | Synthesis Opportunity |
| ------------------ | --------------------- |
| "We did this before" | Recurring solution → pattern candidate |
| Same bug in different context | Missing knowledge → capture the fix pattern |
| "This works everywhere" | Universal principle → high-value pattern |
| "I wish I'd known this earlier" | Onboarding knowledge → insight worth capturing |
| "This is not obvious" | Non-obvious insight → capture the *why* |

## Promotion Checklist (Insight → Pattern)

Before promoting a GI-* insight to GK-* pattern:

- [ ] Abstracted from original project context
- [ ] Named with clear, searchable slug
- [ ] Tagged with relevant categories
- [ ] Connected to existing patterns (if related)
- [ ] Includes at least one concrete example
- [ ] The generalization is still *true* (not over-abstracted)

## Anti-Patterns

| Don't | Why | Do Instead |
| ----- | --- | ---------- |
| Store every learning | Creates noise, reduces signal | Filter for non-obvious insights |
| Copy-paste project specifics | Not reusable outside original context | Abstract first |
| Create near-duplicates | Fragments knowledge | Extend existing patterns |
| Over-generalize | "Always do X" is usually wrong | Include scope and exceptions |
| Skip examples | Abstract knowledge is hard to apply | Include 1-2 concrete examples |

## Synthesis During Meditation

Phase 2 of meditation is the natural synthesis point:

1. Review session insights (Phase 1 output)
2. For each insight: Abstract → check if existing pattern covers it → extend or create
3. Connect new entries via synapses to related skills
4. Verify the global knowledge index is updated

## Synapses

See [synapses.json](synapses.json) for connections.
