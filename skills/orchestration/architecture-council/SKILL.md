---
name: architecture-council
description: |
  Orchestrates parallel specialized agents for major architectural decisions.
  Spawns perspective agents (Schema-Sage, Repo-Maven, Event-Oracle, etc.),
  collects findings to shared journal, synthesizes via Architect-Prime.
model_invoked: true
triggers:
  - "architecture council"
  - "architectural decision"
  - "ADR"
  - "council"
  - "major design"
  - "service architecture"
  - "system design"
  - "architecture review"
---

# Architecture Council Skill

## Purpose

Orchestrate collaborative architectural analysis using specialized perspective agents. Used for major architectural decisions that benefit from multiple viewpoints and grounded research.

## When to Invoke

| Signal | Action |
|--------|--------|
| "Need to make an architectural decision" | Full council |
| "Design a new service architecture" | Full council |
| "Should we use pattern X or Y?" | Full council |
| "Create an ADR for..." | Full council |
| "Review and revise specification" | Full council |

## Council Composition

| Agent | Domain | Research Focus | Output Section |
|-------|--------|----------------|----------------|
| **Schema-Sage** | Types & Validation | Schema patterns, type safety | Schema Architecture |
| **Repo-Maven** | Persistence | Repository patterns, SQL | Repository Patterns |
| **Event-Oracle** | Event Sourcing | Events, EventLog, audit trails | Event Architecture |
| **Entity-Weaver** | Cluster Entities | Entities, aggregates, state | Entity Patterns |
| **Infra-Smith** | Infrastructure | Database, deployment, layers | Infrastructure |
| **Architect-Prime** | Synthesis | All domains, integration | Final spec/ADR |

## Protocol

### Phase 1: Council Assembly

```
1. Create shared journal file:
   thoughts/shared/journal/YYYY-MM-DD-<topic>-council.md

2. Define section ownership per agent

3. Spawn agents IN PARALLEL with:
   - Assigned research documents
   - MCPs to query (deepwiki, exa)
   - Section template
   - Journal location
```

### Phase 2: Research & Writing (Parallel)

Each agent:
1. Reads assigned research documents
2. Queries MCPs for grounded verification
3. Extracts patterns relevant to their domain
4. Writes findings to their journal thread
5. Signals "READY FOR SYNTHESIS" when complete

### Phase 3: Synthesis (Architect-Prime)

1. Read all agent threads
2. Identify:
   - Consensus patterns (all agree)
   - Conflicts (agents disagree)
   - Gaps (uncovered areas)
3. Synthesize into final spec or ADR
4. Resolve conflicts with rationale

### Phase 4: External Enrichment (Optional)

For industry standards integration:
1. Use exa/playwright for external research
2. Cross-reference with ISA-95, FDA, ISO, etc.
3. Add regulatory grounding to spec

### Phase 5: Deliverables

```
Research → Journal → Spec → ADR → WBS
```

| Artifact | Location | Purpose |
|----------|----------|---------|
| Journal | `thoughts/shared/journal/` | Raw agent findings |
| Spec | `thoughts/shared/specs/` | Synthesized specification |
| ADR | `assets/documents/` | Architectural Decision Record |
| WBS | `thoughts/shared/plans/` | Work Breakdown Structure |

## Journal Format

```markdown
# <Topic> Architecture Council — Shared Journal

**Session**: YYYY-MM-DD
**Purpose**: <Goal of the council>
**Input**: <Research documents count>
**Output**: <Target spec location>

---

## Council Members

| Name | Domain | Research Docs | Section Ownership |
|------|--------|---------------|-------------------|
| Schema-Sage | Types | doc1.md, doc2.md | Section 3 |
| ... | ... | ... | ... |

---

## Protocol

1. Each agent reads their assigned research documents
2. Extract patterns relevant to their section
3. Write findings to their thread below (append only)
4. When ready, write "READY FOR SYNTHESIS"
5. Architect-Prime synthesizes all threads into final spec

---

## Thread: Schema-Sage

### Executive Summary
[Summary of findings]

### 1. Pattern Category
[Detailed findings with code examples]

### Recommendations for v3
[Actionable recommendations]

---

**READY FOR SYNTHESIS**

---

## Thread: Repo-Maven
[...]

## Thread: Event-Oracle
[...]

## Synthesis: Architect-Prime
[Final integration]
```

## Agent Spawn Templates

### Schema-Sage Spawn

```
You are Schema-Sage, the council's type system and validation specialist.

**Your Domain**: Schema patterns, branded types, validation, TaggedClass, transforms

**Research Documents**:
- <list of assigned docs>

**MCPs to Query**:
- deepwiki: Effect-TS/effect (Schema module)

**Output Location**: <journal-path>#Thread: Schema-Sage

**Protocol**:
1. Read your assigned research documents
2. Query deepwiki to verify any uncertain patterns
3. Extract patterns with code examples
4. Write to your journal thread
5. Signal "READY FOR SYNTHESIS" when complete
```

### See Agent Definitions

For full agent definitions, see:
- `.claude/agents/council/schema-sage.md`
- `.claude/agents/council/repo-maven.md`
- `.claude/agents/council/event-oracle.md`
- `.claude/agents/council/entity-weaver.md`
- `.claude/agents/council/infra-smith.md`
- `.claude/agents/council/architect-prime.md`

## MCP Integration

### deepwiki Queries

```
mcp__deepwiki__ask_question
  repoName: "Effect-TS/effect"
  question: "Is my understanding of [PATTERN] correct? I believe..."
```

### exa Research (External Standards)

```
mcp__exa__search
  query: "ISA-95 manufacturing operations management event sourcing"
```

### playwright (Standards Scraping)

For regulatory documents:
```
mcp__playwright__navigate
  url: "https://www.isa.org/standards-and-publications/..."
```

## Example Invocation

### User Request
> "We need to design the v3 service architecture for IIoT. Should we use event sourcing?"

### Claude Response

```
I'll convene the Architecture Council to analyze this decision.

**Creating shared journal**: thoughts/shared/journal/2026-01-25-v3-iiot-council.md

**Spawning council members in parallel**:

1. Schema-Sage → IIoT schema patterns
2. Repo-Maven → Repository patterns analysis  
3. Event-Oracle → Event sourcing fit assessment
4. Entity-Weaver → Entity/aggregate patterns
5. Infra-Smith → Database and infrastructure

[Agents run in parallel, writing to journal]

**Synthesis phase**: Architect-Prime integrating findings...

**Deliverables**:
- Journal: thoughts/shared/journal/2026-01-25-v3-iiot-council.md
- Spec: thoughts/shared/specs/2026-01-25-v3-service-architecture.md
- ADR: assets/documents/iiot/ADR-0012-event-sourcing-boundaries.md
```

## Task Dependencies Pattern

Use task dependencies for ordered execution:

```typescript
// Phase 1: Research (parallel)
const schemaSage = Task.create({ name: "schema-sage-research", ... })
const repoMaven = Task.create({ name: "repo-maven-research", ... })
const eventOracle = Task.create({ name: "event-oracle-research", ... })

// Phase 2: Synthesis (depends on all Phase 1)
const synthesis = Task.create({
  name: "architect-prime-synthesis",
  blockedBy: [schemaSage.id, repoMaven.id, eventOracle.id],
  ...
})

// Phase 3: ADR (depends on synthesis)
const adr = Task.create({
  name: "write-adr",
  blockedBy: [synthesis.id],
  ...
})
```

## Related Skills

| Skill | Integration |
|-------|-------------|
| `/grounded-research` | Agents use this for MCP queries |
| `/effect-patterns` | Schema-Sage expertise |
| `/effect-service-authoring` | Entity-Weaver expertise |
| `/research-council` | Lighter variant for pure research |

## Anti-Patterns

### DON'T: Skip the journal
```
❌ Agents write directly to spec
✅ Agents write to journal, Prime synthesizes to spec
```

### DON'T: Sequential agent execution
```
❌ Run Schema-Sage, wait, run Repo-Maven, wait...
✅ Spawn all agents in parallel
```

### DON'T: Ungrounded assertions
```
❌ "I believe this is the pattern..."
✅ "[VERIFIED via deepwiki] The current pattern is..."
```

### DON'T: Skip external research
```
❌ "Event sourcing seems right for IIoT"
✅ "[VERIFIED via ISA-95] Event sourcing aligns with activity model..."
```

## Reference Materials

### Canonical Council Session
- Journal: `thoughts/shared/journal/2026-01-25-v3-architecture-council.md`
- Spec: `thoughts/shared/specs/2026-01-25-v3-service-architecture.md`
- ADR: `assets/documents/iiot/ADR-0012-event-sourcing-boundaries-iiot.md`
- WBS: `thoughts/shared/plans/2026-01-26-es-boundaries-wbs.md`

### Research Reports
- `thoughts/shared/reports/2026-01-26-es-fits-iiot.md`
- `thoughts/shared/reports/2026-01-26-es-doesnt-fit-iiot.md`
