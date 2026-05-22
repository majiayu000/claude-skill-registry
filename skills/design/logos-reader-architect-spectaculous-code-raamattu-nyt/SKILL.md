---
name: logos-reader-architect
description: |
  Design-only architecture skill for Bible reading systems. Use when (1) designing verse reference data models, (2) planning reader component hierarchies, (3) architecting audio playback contracts, (4) designing embed/share URL schemes, (5) planning outlook/presentation systems, (6) analyzing network requests for duplicate elimination, (7) designing lean data fetching patterns. DESIGN ONLY - no code modifications, no refactoring, no database changes. Produces type definitions, component diagrams, design rationale, and network optimization plans.
---

# Logos Reader Architect

Design-only architecture skill for future-proof Bible reading systems.

## Constraints

**MUST NOT:**
- Modify existing code
- Refactor components
- Write production implementations
- Change database schemas
- Touch Supabase, RPCs, or Edge Functions

**MUST:**
- Design abstractions
- Define data models and contracts
- Name components clearly
- Explain relationships between parts
- Think ahead to embedding, sharing, and audio playback

## Design Tasks

Execute these in order when designing a Bible reader architecture:

### 1. Canonical Data Model

Design first-class types for:
- Verse reference (single verse, range)
- Ordered verse sets
- Optional labels/metadata
- Version handling (KR92, KJV, etc.)

```typescript
// Example structure - customize per requirements
type VerseRef = { book: string; chapter: number; verse: number }
type VerseRange = { start: VerseRef; end: VerseRef }
type VerseSet = { refs: (VerseRef | VerseRange)[]; version: string; label?: string }
```

### 2. Reader Component Taxonomy

Design hierarchy:
- `VerseRow` - single verse display
- `VerseGroup` - contiguous verses
- `VerseSetReader` - arbitrary verse collections
- `ChapterReader` - full chapter (specialization)

Clarify: compositional vs specialized, chapter-awareness boundaries.

### 3. Outlook Model (5-Tier Template System)

**Primary reference:** [Docs/context/reader-templates.md](../../../Docs/context/reader-templates.md)

Read `Docs/context/reader-templates.md` for complete template specifications including:
- Template hierarchy and breakpoints
- Visual differences (verse numbers, spacing, padding, font, actions)
- OutlookConfig type definition
- OUTLOOK_PRESETS values
- CSS mapping
- Key implementation files

**Design principles:**
- Independent of reader type
- Consistent across app, embed, widget
- Changes: layout, spacing, actions
- Preserves: semantics, verse identity

### 4. Audio Playback Contract

Design abstraction that:
- Operates on ordered verse lists (not chapters)
- Emits verse cue events
- Drives active verse highlighting
- Reusable by any reader component

```typescript
// Example interface
interface AudioController {
  play(verses: VerseRef[]): void
  onVerseCue: (ref: VerseRef) => void
  onComplete: () => void
}
```

### 5. Linking & Embedding Model

Design:
- URL encoding for verse sets
- Embed data delivery mechanism
- App vs external site differences

## Output Format

Produce:
1. **Conceptual overview** - Architecture summary
2. **Type definitions** - TypeScript-style
3. **Component diagram** - ASCII relationships
4. **Design rationale** - Why this scales
5. **Deferred items** - What's intentionally not designed

## Review Workflow

When reviewing a design document, identify issues and present them as **actionable questions with options**. This makes decisions faster and clearer.

### Question Format

For each issue found, use AskUserQuestion tool with 2-4 concrete options:

```
Issue: Audio segments keyed by rangeIndex break if ranges reorder.

Question: "How should audio segments be keyed?"
Options:
- "By book.chapter identity (Recommended)" - Survives reordering, more robust
- "Keep rangeIndex" - Simpler, reordering not expected
- "Defer decision" - Mark as TODO, decide later
```

### Review Categories

Group issues into these categories and present as multi-select or sequential questions:

**Architecture Decisions** - Coupling, extensibility, component boundaries
**API Surface** - What's exposed, what's internal, response shapes
**Edge Cases** - Errors, empty states, limits, overrides
**Missing States** - Loading, error, empty handling

### Final Confirmation

After collecting decisions, always ask:

```
"Update the design document with these decisions?"
Options:
- "Yes, update now"
- "Show me the changes first"
- "No, just note for later"
```

### Example Review Output

Instead of:
> "Line 56: rangeIndex ties audio directly to parsing order. If you reorder ranges, audio breaks. Consider keying by book.chapter identity instead."

Use AskUserQuestion:
> **Audio Segment Keying**
> rangeIndex ties audio to parsing order - reordering ranges breaks playback.
>
> Options:
> 1. "Key by book.chapter identity (Recommended)" - Survives reordering
> 2. "Keep rangeIndex" - Simpler if reorder never happens
> 3. "Add both keys" - rangeIndex for order, identity for lookup

## Network Optimization Analysis

When analyzing duplicate requests or designing lean data fetching:

1. **Capture network log** - Filter by domain, sort by timestamp
2. **Identify duplicates** - Same endpoint multiple times
3. **Trace call sites** - `grep -rn "functionName" src/`
4. **Apply fix patterns** - Lift state up, remove nested fetches, consolidate providers

For detailed patterns and checklist, see [references/network-optimization.md](references/network-optimization.md).

### Quick Diagnostic Questions

- Is the same data fetched by multiple hooks?
- Does a service function fetch data that React Query also manages?
- Are there provider wrappers whose context is never consumed?
- Do child components fetch data they already receive as props?

## Context Files

For project context, read from `Docs/context/`:
- `Docs/context/reader-templates.md` - **5-tier template system** (primary reference for outlook design)
- `Docs/context/db-schema-short.md` - Database tables (verses, chapters, audio)
- `Docs/context/supabase-map.md` - Edge Functions (embed, etc.)
- `Docs/context/packages-map.md` - Shared packages (shared-voice, etc.)

For reader-specific patterns, see [references/current-architecture.md](references/current-architecture.md).
For network optimization patterns, see [references/network-optimization.md](references/network-optimization.md).
