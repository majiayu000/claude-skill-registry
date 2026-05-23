---
name: context-party
description: Parallel historical context gathering using G-4 CONTEXT. Deploy 6 probes to gather all relevant context before complex work.
model_tier: sonnet
parallel_hints:
  can_parallel_with: [search-party, roster-party]
  must_serialize_with: []
  preferred_batch_size: 6
context_hints:
  max_file_context: 100
  compression_level: 1
  requires_git_context: true
  requires_db_context: false
escalation_triggers:
  - pattern: "conflicting.*decision"
    reason: "Conflicting historical decisions require arbitration"
  - pattern: "HIPAA|OPSEC|PHI"
    reason: "Sensitive data handling in context requires security review"
---

# CONTEXT_PARTY Skill

> **Purpose:** Coordinated parallel historical context gathering with 6 probes
> **Created:** 2026-01-06
> **Trigger:** `/context-party` command
> **Aliases:** `/context`, `/history`, `/cp`
> **Owner:** G4_CONTEXT_MANAGER (G-4 Staff)

---

## When to Use

Deploy CONTEXT_PARTY when you need historical context before making decisions:

- Complex tasks requiring precedent knowledge
- Before making architectural or design decisions
- When similar problems may have been solved before
- Pre-task context gathering for high-stakes work
- Understanding why current patterns exist
- Mining lessons from past sessions
- After SEARCH_PARTY, before PLAN_PARTY

**Do NOT use for:**
- Simple, well-understood tasks with clear precedent
- Emergencies (no time for historical research)
- New features with no historical analog
- When you already have complete context

---

## Economics: Zero Marginal Wall-Clock Cost

**Critical Understanding:** Parallel context probes with the same timeout cost nothing extra in wall-clock time.

```
Sequential (BAD):        Parallel (GOOD):
6 probes × 90s each      6 probes × 90s in parallel
Total: 540s              Total: 90s (6x faster)
```

**Implication:** Always spawn all 6 probes. There is no cost savings from running fewer.

---

## The Six Context Probes

| Probe | Lens | What It Finds |
|-------|------|---------------|
| **PRECEDENT** | Past decisions | How similar problems were solved before, proven approaches |
| **PATTERNS** | Recurring themes | Cross-session patterns, repeated approaches, emerging trends |
| **CONSTRAINTS** | Known limits | Documented constraints, gotchas, warnings, hard limits |
| **DECISIONS** | ADRs/choices | Architectural decisions relevant to task, rationale captured |
| **FAILURES** | Past issues | What broke before, why it broke, how it was fixed, root causes |
| **KNOWLEDGE** | Domain expertise | RAG docs by topic, relevant documentation, domain knowledge |

### Probe Details

#### PRECEDENT Probe
**Focus:** How have we solved similar problems before?
- Search for similar tasks in session history
- Identify successful approaches and patterns
- Extract lessons learned from comparable work
- Find reusable solutions and components
- Note what worked well and what didn't

**RAG Queries:**
- `rag_search("similar to [task description]")`
- `rag_search("precedent [domain] [pattern]")`

#### PATTERNS Probe
**Focus:** What recurring themes exist across sessions?
- Cross-session pattern recognition
- Repeated design approaches
- Emergent architectural patterns
- Common anti-patterns to avoid
- Evolution of thinking over time

**RAG Queries:**
- `rag_search("pattern [domain]")`
- `rag_search("recurring [theme]")`

#### CONSTRAINTS Probe
**Focus:** What are the known limits and gotchas?
- Documented constraints (ACGME, technical, policy)
- Known performance bottlenecks
- Edge cases and limitations
- Warning signs and red flags
- Hard limits that cannot be violated

**RAG Queries:**
- `rag_search("constraint [domain]")`
- `rag_search("gotcha [technology]")`
- `rag_search("limitation [feature]")`

#### DECISIONS Probe
**Focus:** What architectural decisions are relevant?
- Search decision history (ADRs)
- Extract rationale for key choices
- Understand trade-offs made
- Identify reversible vs irreversible decisions
- Map decision dependencies

**RAG Queries:**
- `rag_search("decision [topic]", doc_type="decision_history")`
- `rag_search("ADR [domain]")`
- `rag_search("architecture choice [component]")`

#### FAILURES Probe
**Focus:** What has broken before and why?
- Root cause analysis from past failures
- Bug patterns and common mistakes
- Regression history
- Fix effectiveness tracking
- Failure mode analysis

**RAG Queries:**
- `rag_search("bug [component]", doc_type="bug_fix")`
- `rag_search("failure [domain]")`
- `rag_search("broke [feature]")`

#### KNOWLEDGE Probe
**Focus:** What domain knowledge is relevant?
- ACGME rules and compliance knowledge
- Scheduling policies and constraints
- Resilience framework concepts
- Military medical context
- User guides and FAQs

**RAG Queries:**
- `rag_search("ACGME [topic]", doc_type="acgme_rules")`
- `rag_search("scheduling [concept]", doc_type="scheduling_policy")`
- `rag_search("resilience [pattern]", doc_type="resilience_concepts")`

---

## Deployment Pattern

### Standard Deployment: 6 Context Probes

Deploy 6 context gathering probes in parallel, each using semantic search and historical analysis:

| Probe | RAG Strategy | Analysis Focus |
|-------|--------------|----------------|
| PRECEDENT | Search session_learnings, ai_pattern | Similar past solutions |
| PATTERNS | Search across all doc_types | Cross-session themes |
| CONSTRAINTS | Search acgme_rules, scheduling_policy | Known limits |
| DECISIONS | Search decision_history | Architectural choices |
| FAILURES | Search bug_fix, session_learnings | What broke |
| KNOWLEDGE | Search by doc_type (domain-specific) | Domain expertise |

---

## Invocation

### Full Deployment (6 probes)

```
/context-party
```

Deploys all 6 context probes on current task.

### Targeted Context Gathering

```
/context-party "scheduling capacity constraints"
```

Deploys probes with explicit context focus.

### Before Complex Work

```
# Recommended workflow
/search-party backend/app/scheduling/    # Understand current state
/context-party "capacity allocation"      # Understand history
/plan-party                               # Plan with full context
```

---

## IDE Crash Prevention (CRITICAL)

**DO NOT** have ORCHESTRATOR spawn 6 context probes directly. This causes IDE seizure and crashes.

**CORRECT Pattern:**
```
ORCHESTRATOR → spawns 1 G4_CONTEXT_MANAGER
                    ↓
              G4_CONTEXT_MANAGER deploys 6 probes internally
              (manages parallelism, synthesizes results)
```

**WRONG Pattern:**
```
ORCHESTRATOR → spawns 6 probes directly → IDE CRASH
```

The G-4 Context Manager absorbs the parallelism complexity. ORCHESTRATOR only ever spawns 1 coordinator.

---

## Spawn Pattern

### Via G4_CONTEXT_MANAGER (CORRECT)

```python
# ORCHESTRATOR spawns G4_CONTEXT_MANAGER who manages the 6 context probes
Task(
    subagent_type="general-purpose",
    description="G4_CONTEXT_MANAGER: CONTEXT_PARTY Commander",
    prompt="""
## Agent: G4_CONTEXT_MANAGER (G-4 Staff)

You are the G-4 Context Manager for CONTEXT_PARTY deployment.

## Mission
Deploy 6 context gathering probes in parallel. Each probe uses RAG semantic search
and historical analysis to gather relevant context for the current task.

Collect all reports and synthesize into unified context brief.

## Current Task Context
[Insert task description and goal here]

## Your Context Probes to Deploy
1. PRECEDENT - Search for similar past solutions
2. PATTERNS - Identify recurring themes
3. CONSTRAINTS - Document known limits
4. DECISIONS - Extract relevant ADRs
5. FAILURES - Analyze past breakages
6. KNOWLEDGE - Gather domain expertise

## RAG Integration

Each probe should use the RAG API for semantic search:
- Backend running: Use http://localhost:8000/api/rag/search
- MCP available: Use rag_search, rag_context tools
- Fallback: Search .claude/dontreadme/ markdown files

## Spawn each using Task tool with subagent_type="Explore"

## After all report back:
1. Cross-reference findings across probes
2. Identify relevant precedents
3. Flag conflicting decisions (escalate if unresolved)
4. Generate consolidated context brief
5. Report to ORCHESTRATOR
"""
)
```

### Direct Deployment (Only if G4_CONTEXT_MANAGER unavailable)

```python
# Deploy all 6 probes in parallel
# WARNING: Only use if spawning from within a coordinator, NOT from ORCHESTRATOR
# Total: 6 probes, wall-clock = single probe timeout

spawn_parallel([
    Task(subagent_type="Explore", description="PRECEDENT",
         prompt="Search for similar past solutions using RAG semantic search"),
    Task(subagent_type="Explore", description="PATTERNS",
         prompt="Identify recurring cross-session patterns and themes"),
    Task(subagent_type="Explore", description="CONSTRAINTS",
         prompt="Document known limits, gotchas, and warnings"),
    Task(subagent_type="Explore", description="DECISIONS",
         prompt="Extract relevant architectural decisions and rationale"),
    Task(subagent_type="Explore", description="FAILURES",
         prompt="Analyze past failures, root causes, and fixes"),
    Task(subagent_type="Explore", description="KNOWLEDGE",
         prompt="Gather domain expertise from RAG knowledge base"),
])
```

---

## Context Synthesis

After all 6 probes report back:

1. **Cross-reference findings** across probes
2. **Identify conflicts** in historical decisions
3. **Extract high-confidence patterns** (multiple probes agree)
4. **Flag gaps** requiring new decisions
5. **Generate consolidated context brief**

### Conflict Analysis

**Key Insight:** Same topic, different perspectives. Conflicts between probes are high-signal:

| Conflict Type | Signal Meaning |
|--------------|----------------|
| PRECEDENT says X, DECISIONS say Y | Precedent may be outdated, decision superseded it |
| PATTERNS shows trend A, FAILURES show B caused issues | Pattern may be anti-pattern, needs review |
| CONSTRAINTS limit X, PRECEDENT did X | Constraint was added later, precedent is invalid |
| KNOWLEDGE says do A, FAILURES show A broke | Knowledge needs update, failure is newer |
| DECISIONS conflict across sessions | Architectural drift, needs arbitration (ESCALATE) |

### Confidence Scoring

```
High Confidence (4+ probes agree):
  - Pattern is well-established
  - Decision is validated by multiple sources
  - Constraint is consistently documented

Medium Confidence (2-3 probes agree):
  - Emerging pattern
  - Recent decision with limited validation
  - Constraint with edge cases

Low Confidence (0-1 probes):
  - Novel situation
  - No historical precedent
  - New decision needed
```

---

## Output Format

### Context Brief

```markdown
## CONTEXT_PARTY Brief

### Task: [Current task description]

### Context Confidence: [HIGH/MEDIUM/LOW]

---

### PRECEDENT Findings
- **Similar Solutions:**
  - [Past solution 1] (Session X, [date])
  - [Past solution 2] (Session Y, [date])
- **Proven Approaches:**
  - [Approach A]: Worked well for [use case]
  - [Approach B]: Failed for [use case], avoid
- **Reusable Components:**
  - [Component/pattern to reuse]

---

### PATTERNS Identified
- **Recurring Theme 1:** [Description, frequency, evolution]
- **Recurring Theme 2:** [Description, frequency, evolution]
- **Anti-Patterns to Avoid:**
  - [Anti-pattern A]: Causes [problem]

---

### CONSTRAINTS Documented
- **Hard Limits:**
  - [Constraint 1]: Cannot violate [reason]
  - [Constraint 2]: ACGME rule [reference]
- **Gotchas:**
  - [Gotcha A]: Watch for [issue]
  - [Gotcha B]: Known edge case [description]
- **Performance Limits:**
  - [Limit]: Degrades at [threshold]

---

### DECISIONS Relevant
- **ADR-XXX:** [Decision summary]
  - **Rationale:** [Why this was chosen]
  - **Trade-offs:** [What was sacrificed]
  - **Status:** [Active/Superseded/Under Review]
- **Related Decisions:**
  - Depends on: [Prior decision]
  - Enables: [Future decision]

---

### FAILURES Analyzed
- **Failure Pattern 1:**
  - **What broke:** [Component/feature]
  - **Root cause:** [Why it broke]
  - **Fix:** [How it was resolved]
  - **Prevention:** [How to avoid]
- **Regression Risk:**
  - [Feature X]: Broke in [session], watch for recurrence

---

### KNOWLEDGE Retrieved
- **ACGME Compliance:**
  - [Relevant rule 1]
  - [Relevant rule 2]
- **Scheduling Policies:**
  - [Policy A]: [Description]
- **Domain Expertise:**
  - [Concept]: [Explanation from RAG]

---

### Conflicts Detected
- **CONFLICT:** [Probe A] vs [Probe B]
  - **A says:** [Position A]
  - **B says:** [Position B]
  - **Resolution needed:** [Escalate/Newer decision wins/Clarify]

---

### Gaps Identified
- **No precedent for:** [Novel aspect]
- **No constraint documented for:** [Uncovered area]
- **Decision needed for:** [Unresolved choice]

---

### Recommendations
1. **Follow precedent:** [Specific recommendation]
2. **Respect constraints:** [Specific constraint to honor]
3. **Avoid pattern:** [Specific anti-pattern to avoid]
4. **New decision needed:** [Escalate to ARCHITECT/ORCHESTRATOR]

---

### RAG Coverage
- Total chunks retrieved: [N]
- Doc types searched: [List]
- Oldest relevant context: [Date]
- Newest relevant context: [Date]
```

---

## Integration with RAG System

### RAG API Usage (Preferred)

When backend is running at `http://localhost:8000`:

```bash
# Search for precedent
curl -X POST http://localhost:8000/api/rag/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "schedule capacity allocation past approaches",
    "limit": 10,
    "doc_type": "session_learnings"
  }'

# Search for decisions
curl -X POST http://localhost:8000/api/rag/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "capacity constraint architecture decision",
    "limit": 5,
    "doc_type": "decision_history"
  }'

# Search for failures
curl -X POST http://localhost:8000/api/rag/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "scheduling engine failure capacity",
    "limit": 5,
    "doc_type": "bug_fix"
  }'
```

### MCP Tools (If Available)

| Tool | Probe Usage |
|------|-------------|
| `rag_search` | All probes use for semantic search |
| `rag_context` | Build formatted context for agent prompts |
| `rag_health` | Verify RAG system before deployment |

### Fallback Strategy

If RAG API unavailable:
1. Search `.claude/dontreadme/sessions/` for session history
2. Search `.claude/dontreadme/synthesis/PATTERNS.md` for patterns
3. Search `.claude/dontreadme/synthesis/DECISIONS.md` for decisions
4. Search `docs/rag-knowledge/` for domain knowledge
5. Use git log and blame for change history

---

## Decision Tree: When to Deploy

| Scenario | Deploy CONTEXT_PARTY? | Rationale |
|----------|----------------------|-----------|
| Novel feature, no precedent | NO | No historical context exists |
| Similar feature exists | YES | Learn from precedent |
| Before architectural change | YES | Understand past decisions |
| Emergency fix (P0) | NO | No time for historical research |
| Complex multi-domain task | YES | Need cross-domain context |
| Simple bug fix | NO | Obvious solution, no context needed |
| Before PLAN_PARTY | YES | Context informs planning |
| After SEARCH_PARTY | MAYBE | If current state reveals historical questions |

---

## Workflow Integration

### Full Intelligence Pipeline

```
User Request: Complex task
    ↓
ORCHESTRATOR receives task
    ↓
G2_RECON deploys SEARCH_PARTY
    ↓ (current state intel)
G4_CONTEXT_MANAGER deploys CONTEXT_PARTY
    ↓ (historical context)
G5_PLANNING deploys PLAN_PARTY
    ↓ (execution plan informed by state + history)
ORCHESTRATOR executes plan
    ↓
Result synthesis
    ↓
G4_CONTEXT_MANAGER captures new context (closes loop)
```

### Signal Flow

```
CONTEXT_PARTY → Historical Brief → PLAN_PARTY → Execution Plan
     |                                 |              |
(6 context signals)            (informed by history)  (execution)
     |                                 |              |
Synthesis                          Strategy          Result
(G4_CONTEXT_MANAGER)             (G5_PLANNING)    (COORD_AAR)
     |                                                |
     └────────────── Capture & Store ─────────────────┘
                    (Context loop closes)
```

---

## Timeout Profiles

| Profile | Duration | Best For |
|---------|----------|----------|
| **QUICK** | 60s | Fast context check, simple tasks |
| **STANDARD** | 90s | Normal context gathering (default) |
| **DEEP** | 180s | Comprehensive historical analysis |

---

## Failure Recovery

### Minimum Viable Context

Mission can proceed if:
- PRECEDENT (baseline: has this been done before?) ✓
- CONSTRAINTS (safety: what can't we do?) ✓
- KNOWLEDGE (domain: what rules apply?) ✓
- At least 2 of remaining 3 probes

### Circuit Breaker

If > 2 consecutive probe failures: Trip to OPEN state, fall back to manual context gathering.

---

## Curation After Context Gathering

**CRITICAL:** After completing work informed by CONTEXT_PARTY, G4_CONTEXT_MANAGER should:

1. **Capture new context** from task outcome
2. **Update RAG knowledge base** with learnings
3. **Mark superseded decisions** if new approach chosen
4. **Link to precedent** for future retrieval
5. **Close the context loop**

This ensures future CONTEXT_PARTY deployments benefit from current work.

---

## Related Skills

| Skill | When to Use |
|-------|-------------|
| `search-party` | Current state reconnaissance (pairs with this) |
| `plan-party` | Downstream planning (informed by this) |
| `startup` | Session initialization |
| `startupO` | ORCHESTRATOR mode initialization |
| `session-end` | Context capture at session end |

---

## Related Agents

| Agent | Role in Context Gathering |
|-------|---------------------------|
| G4_CONTEXT_MANAGER | Owns CONTEXT_PARTY deployment |
| G4_LIBRARIAN | RAG curation and ingestion |
| G2_RECON | Current state (complements historical context) |
| G5_PLANNING | Uses context to inform plans |

---

*CONTEXT_PARTY: Six lenses on history, one task, zero marginal cost. Those who forget context are doomed to repeat mistakes.*
