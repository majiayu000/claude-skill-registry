---
name: architect
description: Review and evolve the codebase architecture — evaluate patterns, layers, and design decisions (Alex + Daniel workflow)
---

Evaluate the architecture: $ARGUMENTS

## Step 1 — Read Current Architecture
Read every layer of the codebase (see Layers table in project config for the complete file list).

## Step 2 — Evaluate Layer Boundaries
Check the dependency graph (see Layers in project config for layer → path mapping):
- Does any lower layer import from a higher layer?
- Are there circular imports?
- Is business logic leaking into route handlers?
- Is core/device logic leaking into the service layer?
- Are there god objects (classes doing too much)?

## Step 3 — Evaluate Design Patterns
Review patterns in use and their appropriateness (see Design Patterns in project config):
- Is the primary protocol/interface sufficient? Does it need extending?
- Is the DI chain clean? Any circular dependencies?
- Is the current state storage sufficient? Need persistence?
- Is middleware the right layer for cross-cutting concerns?
- Is the factory pattern extensible for new implementations?
- Should state changes notify external systems?

## Step 4 — Evaluate Scalability Concerns
- **Multi-resource**: Can the architecture support multiple external resources?
- **Multi-user**: Can it handle concurrent users with different permissions?
- **Multi-instance**: Can multiple API instances share state?
- **Event-driven**: Can it push state changes (WebSocket, SSE)?
- **Persistence**: Should state survive restarts?

## Step 5 — Identify Technical Debt
- Code that works but is in the wrong layer
- Abstractions that are too tight or too loose
- Missing abstractions (repeated patterns not extracted)
- Configuration that should be dynamic but is static
- Tests that test implementation instead of behavior

## Step 6 — Propose Improvements
For each improvement, evaluate:
- **Impact**: How much does this improve the codebase?
- **Effort**: How much work is required?
- **Risk**: What could break?
- **Priority**: Must-do / Should-do / Nice-to-have

Format:
```markdown
### Proposal: <title>
**Impact:** High/Medium/Low
**Effort:** Small/Medium/Large
**Risk:** Low/Medium/High
**Priority:** Must/Should/Nice

**Current state:** <what exists now>
**Proposed state:** <what it should become>
**Migration path:** <how to get there safely>
**Files affected:** <list>
```

## Step 7 — Architecture Decision Record
If a significant change is proposed, document it:
```markdown
# ADR-<number>: <title>

## Status: Proposed / Accepted / Rejected

## Context
<why this decision is needed>

## Decision
<what we decided>

## Consequences
<positive and negative effects>
```

## Rules
- Architecture changes MUST maintain backwards compatibility
- Never propose changes without migration paths
- Evaluate trade-offs explicitly — no "this is just better"
- Consider the team's current capacity and skill level
- Prefer incremental evolution over big-bang rewrites