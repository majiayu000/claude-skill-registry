---
name: sdd-design-frontend
description: |
  Design component architecture, state management, and React patterns.
  Use when: sdd-design assigns Component Architecture section.
  Triggers: "design components", "component architecture", "state management", "react patterns"
---

# SDD Design Frontend

Write the Component Architecture section of a design document.

## Scope

| Responsible For | Not Responsible For |
|-----------------|---------------------|
| Component hierarchy | Visual layout (→ uiux) |
| State management strategy | Loading spinners design (→ uiux) |
| Data flow | Security validation (→ security) |
| File/folder structure | Bundle size limits (→ perf) |
| React pattern selection | Accessibility details (→ uiux) |
| Library candidates (functional fit) | Library final selection (→ perf) |
| Props interface design | — |

## Cross-Cutting Roles

> **Note:** Cross-cutting concerns are an extension to `docs/sdd-guidelines.md` for specialist coordination. See sdd-design for full mapping.

Frontend is:
- **Primary owner:** Error handling, Code display, User input
- **Reviewer for:** Accessibility (owned by uiux)

## Instructions

### Step 1: Read Context

1. Design skeleton (from sdd-design)
2. All REQs in your section's `@derives`
3. Foundation anchors (especially `TECH-*`, `CONSTRAINT-*`)

### Step 2: Analyze Requirements

For each assigned REQ, extract:

| REQ | User Action | Components Needed | State Needed |
|-----|-------------|-------------------|--------------|
| | | | |

**Tip:** Start from user actions, not implementation.

### Step 3: Design Component Hierarchy

Decompose from features to components. Example structure:

```
{FeatureRoot}
├── {StateHolder}      ← manages state
│   ├── {Child}        ← receives props
│   └── {Child}
└── {Shared}
```

**Principles:**
- Colocation: state close to where it's used
- Single responsibility: one reason to change
- Composition over inheritance

Adapt to project's existing patterns.

### Step 4: Design Props Interfaces

For each component, define props contract. See [reference/props-design.md](reference/props-design.md).

**Decision points:**
- Controlled vs uncontrolled?
- Required vs optional?
- Callback naming convention?

### Step 5: Define State Management

Determine state location based on REQ implications:

| REQ Implies | State Location |
|-------------|----------------|
| "shareable", "bookmarkable", "linkable" | URL (router) |
| "real-time update", "immediately reflects" | Lifted state or Context |
| "persists across views/navigation" | Context or external store |
| "isolated", no cross-component requirement | Local (useState) |
| Complex update logic in REQ | useReducer |

**Default:** Start with local state unless REQ implies otherwise.

### Step 6: Select Patterns

Match each REQ need to a pattern:

| Need | Pattern |
|------|---------|
| Components that work together | Compound Components |
| Render customization by consumer | Render Props |
| Reusable stateful logic | Custom Hooks |
| Avoid prop drilling | Context |
| Parent controls value | Controlled Components |

Document pattern → REQ connection with `@derives` in your section.

### Step 7: List Library Candidates

**Your job:** List functionally suitable options.  
**Perf's job:** Final selection based on size.

| Purpose | Candidates | Notes for Perf |
|---------|------------|----------------|
| {need} | lib-a, lib-b, lib-c | {size hints, tree-shaking support, lighter alternatives} |

**Example notes:** "lib-a is tree-shakable", "lib-b has lighter fork", "lib-c requires full import"

**Evaluation criteria (functional only):**
- API fits our use case
- TypeScript support
- Active maintenance
- Documentation quality

### Step 8: Define File Structure

Follow project conventions. Example structure:

```
src/
├── components/{Feature}/
├── hooks/
├── context/
└── types/
```

**Note:** Adapt to project's existing conventions.

### Step 9: Write Section

```markdown
## Component Architecture

@derives: {REQ-IDs}

### Component Hierarchy
### Props Interfaces  
### State Management
### Patterns Used
### Library Candidates
### File Structure

**Status:** draft
```

Note: Ownership tracked in `.sdd/state.yaml`, not in document.

### Step 10: Add Decisions

For non-obvious choices, add to Decisions Log:

```markdown
| ID | Decision | Rationale | Owner |
|----|----------|-----------|-------|
| DEC-001 | {what} | {why this satisfies REQ} | frontend |
```

Or inline for medium significance:

```markdown
@rationale: Chose X over Y — {reason connecting to REQ}
```

See `docs/sdd-guidelines.md` §1.4 for when to use which format.

### Step 11: Handoff

Per `docs/sdd-guidelines.md` §4.3 and §10.6.

#### 1. Update Section Status

In design document:

```markdown
## Component Architecture

@derives: REQ-REACT-001, REQ-REACT-002

...

**Status:** verified
```

#### 2. Update State File

```yaml
# .sdd/state.yaml
documents:
  design:
    status: partial
    sections:
      component-architecture: verified  # ← update
      uiux: pending
      security: pending
      perf: pending
```

#### 3. Create Handoff Record

```yaml
# .sdd/handoffs/{timestamp}-frontend.yaml
from: sdd-design-frontend
to: sdd-design
timestamp: {ISO-8601}

completed:
  - design.component-architecture: verified

in_progress: []

blocked: []
  # - design.component-architecture: "Waiting on perf for library selection"

gaps: []
  # - id: GAP-001
  #   description: "..."

next_steps:
  - sdd-design-perf: Review library candidates, select within 10KB budget
  - sdd-design-uiux: Review accessibility props support
```

#### 4. Cross-Cutting Status

Update cross-cutting table in design document:

| Concern | Primary | Reviewer | Status |
|---------|---------|----------|--------|
| Error handling | frontend | security | `ready-for-review` |
| Accessibility | uiux | frontend | `pending` |

**Status values:**
- Primary done → `ready-for-review`
- Reviewer approved → `approved`

**Completeness test:** Next agent can start without asking clarifying questions.

## @derives Judgment

**A component/decision `@derives` from a REQ when:**

| Criterion | Example |
|----------|---------|
| Directly implements REQ's feature | `PatternList` → REQ's "gallery displays patterns" |
| Enables REQ's acceptance criteria | `PropControl` → REQ's "manipulate props in real-time" |
| Architectural support for REQ | `ErrorBoundary` → REQ's "syntax error display" |

**NOT @derives:**
- Generic utilities not tied to specific REQ
- Implementation details that could serve any REQ

**Format:**
```markdown
@derives: REQ-XXX-001, REQ-XXX-002

- REQ-XXX-001: {which parts of this section address it}
- REQ-XXX-002: {which parts of this section address it}
```

More examples: [reference/derives-examples.md](reference/derives-examples.md)

## Verification

- [ ] All assigned REQs have @derives coverage
- [ ] Each @derives has clear justification
- [ ] Component hierarchy matches user actions from REQs
- [ ] Props interfaces defined for key components
- [ ] State locations justified by REQ implications
- [ ] Library candidates listed (not final selections)
- [ ] File structure follows project conventions
- [ ] Each pattern/library choice has decision entry
- [ ] Cross-cutting items flagged for reviewers

## References

| File | Content |
|------|---------|
| [reference/derives-examples.md](reference/derives-examples.md) | @derives judgment examples |
| [reference/props-design.md](reference/props-design.md) | Props interface patterns for SDD |

## Examples

| File | Content |
|------|---------|
| [examples/react-sample.md](examples/react-sample.md) | Complete example for react-sample package |
