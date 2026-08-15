---
name: lock-decision
description: This skill should be used when the user says "lock it", "go with that", "approved", "that's the standard", or explicitly establishes a project-wide pattern like "from now on all forms should use this approach". Formalizes approved decisions into locked standards that the system enforces going forward. Not needed for story-scoped decisions — only for project-wide patterns.
version: 1.2.0
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep"]
---

# Lock Decision Skill

You are the **commitment mechanism** of the Craft harness. When something is approved, you make it official — turning decisions into standards that the entire system respects.

## When This Activates

- User explicitly approves an option ("let's go with A", "yes, that one")
- User says "lock it", "that's the one", "approved"
- A design pattern needs to become a standard
- A technical approach should be enforced

## Orchestrator Context

The orchestrator may pass enriched args. Parse labeled fields if present:

- `DECISION_TYPE:` design/pattern/token/approach — routes to correct lock template
- `DECISION_SCOPE:` project-wide or story-scoped — determines where to write

**Fallback:** Most lock context comes from conversation. Args are supplementary.

## The Lock Process

### 1. Confirm Understanding

Before locking, verify:

```markdown
## Locking Decision

**Decision:** [Clear statement of what's being locked]

**Context:** [Why this decision was made]

**Applies to:** [Where this standard will be enforced]

Is this correct? Once locked, this becomes a project standard.
```

### 2. Execute the Lock

Depending on what's being locked:

#### Design Pattern → `locked.md`

```markdown
## [Pattern Name]

**Locked:** [Date]
**Context:** [Why this was approved]

### Specification

[Detailed description of the pattern]

### Implementation

```tsx
// Example code showing correct implementation
```

### Variations
- [Allowed variation 1]
- [Allowed variation 2]

### Not Allowed
- [Anti-pattern 1]
- [Anti-pattern 2]
```

#### Design Token → `tokens.yaml`

**When locking colors, typography, or spacing values, update `.craft/design/tokens.yaml`:**

When the file already exists, update it with targeted Edits on the specific keys - never a whole-file Write (the write-permission hook denies Write on an existing tokens.yaml; unnamed keys and their provenance comments must survive).

```yaml
colors:
  primary: "#6366F1"  # Locked: [Date] - [Context]
  surface: "#FAFAFA"

typography:
  font-sans: "Inter, -apple-system, sans-serif"

spacing:
  base: 8  # Locked: [Date]
```

**This file is the source of truth.** The implementer agent reads this when writing styles. Quality gates validate against it.

#### Technical Approach → Story file or `project.md`

```markdown
## Technical Decision: [Title]

**Locked:** [Date]
**Decision:** [What was decided]
**Rationale:** [Why this approach]
**Alternatives Considered:** [What we didn't choose and why]
```

### 3. Confirm the Lock

After writing the lock, output a brief confirmation and return silently to the caller:

> **Locked:** [Summary] → [File updated]

Do NOT output a large markdown block or ask "Ready to continue?" — the caller (story-new, creative-spark, etc.) owns the next step. Terminal text kills command chains.

## Lock Categories

Four lock types: **Design Decisions** (typed UI decisions with valid keys per type), **Pattern Locks** (UI patterns with spec, states, variants, usage rules), **Token Locks** (design values in tokens.yaml), and **Approach Locks** (technical decisions with rationale and implementation standard).

> **Lock templates:** Read `${CLAUDE_PLUGIN_ROOT}/skills/lock-decision/references/lock-templates.md` for detailed templates and examples for each lock type (design decisions with valid key tables, pattern locks, token locks, approach locks).

## Enforcement

Locked decisions are enforced via:

1. **Style hooks** — Grep for token violations on Write/Edit
2. **Adhoc Fit Check** - on the adhoc tweak path, the Fit Check's read of locked.md (plus its mid-pass pivot re-check) is the lock gate - no blocking hook checks locked.md compliance; the write-gate hook checks only write permission
3. **Code review** — Analyzer agents reference locked patterns
4. **Validation** — Validation enforces locked decisions during implementation

## Unlocking (Rare)

Locks can only be unlocked by explicit user request:

```markdown
## Unlock Request

**Pattern:** [What's being unlocked]
**Reason:** [Why the lock should be removed]
**Proposed Change:** [What will replace it]

⚠️ This will remove enforcement. Are you sure?

Options:
1. Unlock and replace with new standard
2. Unlock temporarily for this story only
3. Keep locked, find another approach
```

### Tweak-path lock edits (inline)

The adhoc tweak flow (`skills/adhoc/references/tweak.md`) may alter or remove a lock inline when a tweak conflicts with it - on the user's explicit yes, at one of two moments (the pre-edit conflict branch or the acceptance reconcile), WITHOUT this skill's unlock ceremony. Same discipline (explicit yes only, locked.md's existing format), lighter surface: a tweak thread gets one clean yes, never a ceremony AUQ, and a lock gets at most one write moment per thread. See tweak.md's "inline lock-edit path" for the rules.

## Remember

- **Locks are sacred** — they represent approved decisions
- **Context is crucial** — always record why something was locked
- **Enforcement is layered, not hooked** - implementers and validation enforce locks at story time, the adhoc Fit Check at tweak time; no hook blocks a write on lock compliance
- **Quality only goes up** — new locks can add requirements, never remove

Your goal: Turn "yes" into "always" — making decisions stick.
