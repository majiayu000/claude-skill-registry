---
name: sdd-design-perf
description: |
  Design bundle strategy, lazy loading, and render optimization.
  Use when: sdd-design assigns Performance Strategy section.
  Triggers: "performance design", "bundle size", "lazy loading", "optimization"
---

# SDD Design Perf

Write the Performance Strategy section of a design document.

## Scope

| Responsible For | Not Responsible For |
|-----------------|---------------------|
| Bundle budget | Component structure (→ frontend) |
| Library selection (size) | Library API fit (→ frontend) |
| Code splitting strategy | State management (→ frontend) |
| Lazy loading | Visual loading states (→ uiux) |
| Render optimization | Interaction design (→ uiux) |
| Caching strategy | Security headers (→ security) |

## Cross-Cutting Roles

> **Note:** Cross-cutting concerns are an extension to sdd-guidelines for specialist coordination. See sdd-design for full mapping.

Perf is:
- **Primary owner:** (none in typical frontend projects)
- **Reviewer for:** Loading states (owned by uiux), Code display (owned by frontend)

## Instructions

### Step 1: Read Context

1. Design skeleton (from sdd-design)
2. All REQs in your section's `@derives`
3. Foundation anchors (especially `CONSTRAINT-*` for size limits)
4. Frontend section (for library candidates)

### Step 2: Identify Performance Requirements

Extract from REQs:

| REQ | Performance Implication |
|-----|------------------------|
| | |

**Look for:**
- Explicit size/speed constraints
- "Fast", "instant", "responsive" language
- Large data sets, many items
- Mobile/low-power device mentions

### Step 3: Define Bundle Budget

Based on REQ constraints:

| Category | Budget | @derives |
|----------|--------|----------|
| Initial JS | {X}KB | REQ/CONSTRAINT |
| Lazy chunks | {X}KB | REQ/CONSTRAINT |
| CSS | {X}KB | REQ/CONSTRAINT |
| Total | {X}KB | REQ/CONSTRAINT |

**If no explicit constraint:** Use sensible defaults based on project type.

Document with `@derives` linking to REQ or CONSTRAINT.

### Step 4: Select Libraries

Review frontend's candidates against budget:

| Purpose | Candidates | Size (gzip) | Selection | @derives |
|---------|------------|-------------|-----------|----------|
| | | | | CONSTRAINT-XXX |

**Selection criteria:**
- Fits within budget
- Tree-shakable preferred
- No unnecessary features

### Step 5: Design Code Splitting

Based on user flow from REQs:

| Chunk | Contents | Load Trigger | Size |
|-------|----------|--------------|------|
| main | Core UI | Immediate | |
| | | | |

**Principles:**
- Critical path in main bundle
- Features on-demand
- Route-based splitting when applicable

### Step 6: Design Lazy Loading

For heavy resources:

| Resource | Strategy | Trigger | @derives |
|----------|----------|---------|----------|
| | | | REQ-XXX |

**Strategies:**
- Route-based: `React.lazy()`
- Scroll-based: Intersection Observer
- User-action: On click/expand

### Step 7: Identify Render Optimizations

For REQs with "real-time" or "immediate" language:

| Optimization | Where | Technique | @derives |
|--------------|-------|-----------|----------|
| | | | REQ-XXX |

**Common techniques:**
- `React.memo` for pure components
- `useMemo` / `useCallback` for expensive computations
- Virtualization for long lists

### Step 8: Define Caching Strategy

| Resource | Cache | TTL |
|----------|-------|-----|
| Static assets | Immutable | ∞ |
| | | |

### Step 9: Define Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| LCP | <{X}s | Lighthouse |
| FID | <{X}ms | Lighthouse |
| CLS | <{X} | Lighthouse |
| Bundle size | <{X}KB | Build output |

### Step 10: Write Section

```markdown
## Performance Strategy

@derives: {REQ-IDs}

### Bundle Budget
### Library Selection
### Code Splitting
### Lazy Loading
### Render Optimization
### Caching Strategy
### Performance Metrics

**Status:** draft
```

### Step 11: Add Decisions

For library selections and trade-offs:

```markdown
| ID | Decision | Rationale | Owner |
|----|----------|-----------|-------|
| DEC-00x | {what} | {why — connect to budget/REQ} | perf |
```

### Step 12: Handoff

Per sdd-guidelines §4.3 and §10.6.

#### 1. Update Section Status

```markdown
**Status:** verified
```

#### 2. Update State File

```yaml
# .sdd/state.yaml
documents:
  design:
    sections:
      perf: verified
```

#### 3. Create Handoff Record

```yaml
# .sdd/handoffs/{timestamp}-perf.yaml
from: sdd-design-perf
to: sdd-design
timestamp: {ISO-8601}

completed:
  - design.perf: verified

in_progress: []

blocked: []

gaps: []

next_steps:
  - sdd-design-frontend: Use selected libraries
  - sdd-design-uiux: Review — loading states align with lazy loading
```

#### 4. Cross-Cutting Status

| Concern | Primary | Reviewer | Status |
|---------|---------|----------|--------|
| Loading states | uiux | perf | `approved` or `needs-revision` |
| Code display | frontend | perf | `approved` or `needs-revision` |

## @derives Judgment

**A performance decision `@derives` from a REQ when:**

| Criterion | Example |
|-----------|---------|
| Satisfies REQ's size constraint | Library selection → CONSTRAINT-LIGHTWEIGHT |
| Enables REQ's speed requirement | Lazy loading → REQ's "instant load" |
| Addresses REQ's scale | Virtualization → REQ's "1000+ items" |

**NOT @derives:**
- Generic optimizations not tied to REQ
- Premature optimization without constraint

## Verification

- [ ] Bundle budget defined and justified
- [ ] Library selections within budget
- [ ] Code splitting covers all lazy-loadable features
- [ ] Lazy loading for heavy resources
- [ ] Render optimizations for "real-time" REQs
- [ ] Decisions logged with rationale
- [ ] Cross-cutting reviews completed

## References

| File | Content |
|------|---------|
| [reference/bundle-analysis.md](reference/bundle-analysis.md) | How to analyze and optimize bundles |
| [reference/library-sizing.md](reference/library-sizing.md) | Common library sizes for comparison |

## Examples

| File | Content |
|------|---------|
| [examples/react-sample.md](examples/react-sample.md) | Complete example for react-sample package |
