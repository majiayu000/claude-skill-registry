---
name: adr
description: |
  Create and manage Architecture Decision Records (ADRs) with standardized workflow.
  Handles numbering, formatting, indexing automatically.

  TRIGGER when: User wants to create an ADR ("create adr", "record decision", "document architecture decision"), list ADRs, show a specific ADR, or validate ADR format.

  DO NOT TRIGGER when: User is just asking about existing ADRs conceptually, viewing ADR documentation, or discussing decisions without creating/modifying ADRs.
version: "1.0.0"
argument-hint: "create <title> | list | show <number> | validate <number>"
allowed-tools: Read, Glob, Grep, Write, Edit
disable-model-invocation: false
user-invocable: true
---

# ADR Management Skill

## Purpose

Standardized workflow for creating and managing Architecture Decision Records (ADRs).

**Why This Skill Exists**:
- ✅ Ensures consistent ADR formatting across the project
- ✅ Automates mechanical tasks (numbering, indexing, metadata)
- ✅ Reduces human error (duplicate numbers, missing index updates)
- ✅ Makes ADR creation discoverable and easy

---

## Usage

```bash
/adr create "<title>"       # Create new ADR with auto-assigned number
/adr list                   # List all ADRs with status
/adr show <number>          # Show ADR summary
/adr validate <number>      # Validate ADR completeness (optional)
```

---

## Commands

### 1. Create ADR

**Command**: `/adr create "Title of Decision"`

**What It Does**:
1. **Auto-assign number**: Scans `docs/ADRs/` to find next sequential number
2. **Create file**: `docs/ADRs/{number}-{kebab-case-title}.md`
3. **Fill from template**: Uses `docs/ADRs/TEMPLATE.md` as base
4. **Auto-fill metadata**:
   - Number: `ADR-{number}`
   - Date: Today's date (YYYY-MM-DD)
   - Author: Claude Sonnet 4.5
   - Status: Proposed
5. **Update index**: Add entry to `docs/ADRs/README.md` table
6. **Return**: File path + next steps for user

**Example**:
```bash
User: /adr create "Use Zustand Vanilla Stores"

AI Response:
✅ Created ADR-010: docs/ADRs/010-use-zustand-vanilla-stores.md
✅ Updated index in docs/ADRs/README.md
✅ Updated checklist in docs/ADRs/CHECKLIST.md ⭐

Next steps:
1. Fill in Context section (why this decision?)
2. Document Decision details
3. List at least 2 Alternatives Considered
4. Add Consequences (positive + negative)
5. Change Status to "Accepted" when ready
```

**Workflow**:
1. Find next ADR number (scan `docs/ADRs/[0-9]*.md`)
2. Convert title to kebab-case: "Use Zustand Vanilla Stores" → "use-zustand-vanilla-stores"
3. Read `docs/ADRs/TEMPLATE.md`
4. Replace placeholders:
   - `ADR-NNN` → `ADR-010`
   - `[Short Title]` → User's title
   - `YYYY-MM-DD` → Today's date
   - `{{AUTHOR_NAME}}` → Claude Sonnet 4.5
   - `[Proposed]` → Proposed (default status)
5. Write to `docs/ADRs/{number}-{kebab-title}.md`
6. Update `docs/ADRs/README.md` index table:
   - Add new row: `| [010](./010-use-zustand-vanilla-stores.md) | Use Zustand Vanilla Stores | Proposed | 2026-03-04 |`
   - Update total count
   - Update last updated date
7. Update `docs/ADRs/CHECKLIST.md` table ⭐ NEW:
   - Add new row to "Current ADRs" table
   - Update total count and status breakdown
   - Update "Last Updated" timestamp
   - Identify related Pillars (if mentioned in ADR)
   - Mark "Code Updated" as ✅ when Status = Accepted
8. Present file path and next steps to user

---

### 2. List ADRs

**Command**: `/adr list`

**What It Does**:
- Lists all ADRs with number, title, and status
- Sorted by number (ascending)
- Color-coded by status:
  - ✅ Accepted (green)
  - 📋 Proposed (yellow)
  - ⚠️ Deprecated (orange)
  - 🔄 Superseded (gray)

**Example Output**:
```
Architecture Decision Records (9 total):

✅ ADR-001: Layer First Architecture (Accepted, 2026-02-26)
✅ ADR-002: Data Schema Design (Accepted, 2026-02-26)
✅ ADR-003: Migration Strategy (Accepted, 2026-03-01)
✅ ADR-004: Development Workflow Quality Gates (Accepted, 2026-03-01)
✅ ADR-005: Identity Model (Accepted, 2026-03-01)
✅ ADR-006: Monorepo Structure (Accepted, 2026-03-01)
✅ ADR-007: AWS Amplify Deployment (Accepted, 2026-03-01)
✅ ADR-008: shadcn/ui Design System (Accepted, 2026-03-02)
✅ ADR-009: Zustand Vanilla Store Pattern (Accepted, 2026-03-04)

Status breakdown:
- Accepted: 9
- Proposed: 0
- Deprecated: 0
- Superseded: 0
```

**Implementation**:
1. Scan `docs/ADRs/[0-9]*.md` files
2. Read first 30 lines of each file to extract:
   - Title (from `# ADR-NNN: Title`)
   - Status (from `## Status` section)
   - Date (from `## Date` section)
3. Sort by number
4. Format output with status icons

---

### 3. Show ADR

**Command**: `/adr show <number>`

**What It Does**:
- Displays summary of specific ADR
- Shows: Title, Status, Date, Context, Decision (first paragraph)
- Links to full file

**Example**:
```bash
User: /adr show 009

AI Response:
# ADR-009: Zustand Vanilla Store Pattern

**Status**: Accepted
**Date**: 2026-03-04

## Context
Buffer adopts Clean Architecture with Headless pattern. Services need to
access stores, but services are not React components and cannot use hooks.

## Decision
Adopt Zustand Vanilla Store Pattern for all application stores.
- Use createStore() from zustand/vanilla
- Export vanilla store instance
- Provide getter actions for Service layer

## Consequences
✅ Services can access stores
✅ Stores testable without React
❌ Extra step for React components
❌ Deviates from standard tutorials

📄 Full document: docs/ADRs/009-zustand-vanilla-store-pattern.md
```

**Implementation**:
1. Find file: `docs/ADRs/{number}-*.md`
2. Read file content
3. Extract key sections:
   - Title, Status, Date
   - Context (first 200 chars)
   - Decision (first paragraph)
   - Consequences (positive + negative top 2)
4. Format as summary
5. Include link to full file

---

### 4. Validate ADR (Optional)

**Command**: `/adr validate <number>`

**What It Does**:
- Checks if ADR is complete and ready for "Accepted" status
- Validates required sections
- Checks quality criteria

**Validation Checks**:
- [ ] Context section is not empty (>50 chars)
- [ ] Decision section has implementation details
- [ ] At least 2 alternatives considered
- [ ] Consequences section has both positive AND negative
- [ ] References section exists
- [ ] Status matches content completeness

**Example Output**:
```bash
User: /adr validate 009

AI Response:
Validating ADR-009: Zustand Vanilla Store Pattern...

✅ Context: Complete (500 chars)
✅ Decision: Complete with code examples
✅ Alternatives: 4 options documented
✅ Consequences: Balanced (6 positive, 4 negative)
✅ References: 5 links provided
✅ Status: "Accepted" (appropriate for completeness)

Overall: READY ✅

This ADR is complete and ready for team review.
```

**Implementation**:
1. Read ADR file
2. Parse sections:
   - Context length
   - Decision has code blocks?
   - Count alternatives (look for "### Alternative")
   - Count consequences (✅ and ❌ lines)
   - References section exists?
3. Check status matches completeness:
   - If incomplete → should be "Proposed"
   - If complete → can be "Accepted"
4. Return validation report

---

## Automation Details

### Auto-Numbering Logic

```bash
# Find next ADR number
ls docs/ADRs/[0-9]*.md | sort -V | tail -1
# Output: docs/ADRs/009-zustand-vanilla-store-pattern.md
# Extract: 009
# Next: 010
```

### Kebab-Case Conversion

```
"Use Zustand Vanilla Stores" →
lowercase → "use zustand vanilla stores" →
replace spaces → "use-zustand-vanilla-stores"
```

### Index Update

When creating ADR-010:
1. Read `docs/ADRs/README.md`
2. Find `## ADR Index` section
3. Find last row in table
4. Insert new row:
   ```markdown
   | [010](./010-title.md) | Title | Proposed | 2026-03-04 |
   ```
5. Update `**Total ADRs**: 10`
6. Update `**Last Updated**: 2026-03-04`
7. Write back to file

### CHECKLIST Update ⭐ NEW

When creating ADR-010:
1. Read `docs/ADRs/CHECKLIST.md`
2. Find `## Current ADRs (Auto-Updated)` table
3. Add new row:
   ```markdown
   | [010](./010-title.md) | Title | Proposed | - | ⏳ |
   ```
4. Update total counts: `**Total**: 10 ADRs`
5. Update status breakdown
6. When ADR Status changes to "Accepted":
   - Update "Code Updated" column: `⏳ → ✅`
   - Identify related Pillars by scanning ADR content for Pillar keywords
   - Update Pillar References section if new mappings found
7. Update `**Last Updated**: 2026-03-04`
8. Write back to file

**Pillar Detection Logic**:
- Scan ADR content for Pillar names (A, B, D, E, etc.)
- Check for pattern keywords:
  - "branded type", "nominal" → Pillar A
  - "schema validation", "zod" → Pillar B
  - "layer", "boundary", "import" → Pillar I
  - "headless", "hook" → Pillar L
  - "saga", "compensation" → Pillar M
  - "idempotent" → Pillar Q
  - "logging", "traceId" → Pillar R
- Add to Pillar References section in CHECKLIST

---

## Best Practices

### When to Create an ADR

**Create ADR when**:
- ✅ Making architectural decisions (layer structure, patterns)
- ✅ Choosing technologies (libraries, frameworks)
- ✅ Establishing coding standards (TypeScript strict mode)
- ✅ Defining processes (deployment, testing)
- ✅ Setting precedents (all stores use vanilla pattern)

**Don't create ADR for**:
- ❌ Implementation details within a module
- ❌ Temporary experiments
- ❌ Easily reversible choices
- ❌ Personal coding preferences (use linter)

### ADR Lifecycle

1. **Proposed**: Draft, under discussion
   - Create with `/adr create`
   - Fill in sections
   - Share with team for feedback

2. **Accepted**: Implemented and active
   - Update Status to "Accepted"
   - Reference in code comments
   - Enforce in code reviews

3. **Deprecated**: No longer recommended
   - Update Status to "Deprecated"
   - Add deprecation reason
   - Link to replacement (if any)

4. **Superseded**: Replaced by newer ADR
   - Update Status to "Superseded by ADR-XXX"
   - Link to new ADR
   - Keep for historical context

---

## Integration with Workflow

### Reference ADRs in Code

```typescript
// Following ADR-009: Zustand Vanilla Store Pattern
// All stores use createStore() from zustand/vanilla
import { createStore } from 'zustand/vanilla';

export const taskStore = createStore<TaskStore>()((set, get) => ({
  // Implementation per ADR-009
}));
```

### Link ADRs in PRs

When creating pull request:
```markdown
## Changes
- Refactored taskStore to vanilla pattern

## References
- Implements [ADR-009: Zustand Vanilla Store Pattern](../docs/ADRs/009-zustand-vanilla-store-pattern.md)
```

### Use ADRs in Code Review

Reviewer: "Why are we using `createStore()` instead of `create()`?"
Author: "See ADR-009 - Services need to access stores without React hooks."

---

## Quick Reference

### Create New ADR
```bash
/adr create "Your Decision Title"
```

### List All ADRs
```bash
/adr list
```

### View Specific ADR
```bash
/adr show 009
```

### Validate Before Accepting
```bash
/adr validate 009
```

---

## Related Documentation

- [ADR Template](../../docs/ADRs/TEMPLATE.md) - Template file
- [ADR README](../../docs/ADRs/README.md) - Complete guide
- [ADR Index](../../docs/ADRs/README.md#adr-index) - All ADRs

---

## Notes for Claude

When user invokes `/adr create`:

1. **Ask for confirmation** if title seems incomplete:
   - "Create ADR about 'store'?" → Ask: "Did you mean 'Zustand Store Pattern' or something more specific?"

2. **Suggest related ADRs** if similar topics exist:
   - Creating ADR about authentication → "Note: ADR-005 covers Identity Model. Is this different?"

3. **Check for typos** in common terms:
   - "vanila" → "Did you mean 'vanilla'?"
   - "Zustnd" → "Did you mean 'Zustand'?"

4. **Auto-fill common metadata**:
   - Author: "Claude Sonnet 4.5" (unless user specifies)
   - Date: Today's date (YYYY-MM-DD format)
   - Status: "Proposed" (can be changed later)

5. **Remind about required sections**:
   - "Created ADR-010. Remember to fill in:
     - Context (why this decision?)
     - Decision (what are we doing?)
     - At least 2 Alternatives
     - Consequences (both positive and negative)"

---

**Version:** 1.0.0
**Last Updated:** 2026-03-04
**Changelog:**
- v1.0.0 (2026-03-04): Initial release - ADR creation and management skill