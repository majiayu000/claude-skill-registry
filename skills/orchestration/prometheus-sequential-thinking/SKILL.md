---
name: prometheus-sequential-thinking
description: Enhance planning quality with structured deep analysis using sequential-thinking MCP for complex or uncertain tasks
compatibility: opencode
---

## MANDATORY USAGE (CRITICAL RULE)

**This skill is MANDATORY for all agents in the ULTRABRAIN category.**

### When ULTRABRAIN is used:
- Deep logical reasoning tasks
- Complex architecture decisions requiring extensive analysis
- System design (monolith vs microservices, database choices)
- Technology selection (frameworks, libraries, patterns)
- Long-term architectural planning (scalability, maintainability)
- Security and compliance design
- High-risk refactoring
- Migrating monoliths to microservices
- Changing core data structures or APIs
- Performance optimizations affecting multiple modules
- Uncertain requirements (vague requests, investigation needed)

**ALL ULTRABRAIN agents MUST use the `sequantial-thinking-mcp_sequentialthinking` tool** before making any decisions, recommendations, or plans.

**Agents that MUST use this skill:**
- Atlas (when delegating to ultrabrain category)
- Sisyphus (when working on ultrabrain tasks)
- Prometheus (when planning architecture/complex decisions)
- Sisyphus-Juneor-ultrabrain (ALL instances)
- Any agent receiving `category="ultrabrain"` delegation

## What I do

This skill guides agents on when and how to use the server-sequential-thinking MCP tool to improve the quality of their reasoning, planning, and decision-making processes.

The sequential-thinking tool enables:
- Step-by-step analysis with hypothesis formation and verification
- Branching thoughts to explore alternative approaches
- Revision of previous thoughts to reconsider decisions
- Extension of analysis even after reaching initial conclusions
- Expressing uncertainty when information is insufficient

## When to use me

Use sequential-thinking when working on tasks that benefit from deep, structured analysis:

### Trigger Categories

| Task Complexity | Use Sequential-Thinking? | Rationale |
|----------------|--------------------------|-----------|
| **Trivial** | NO | Single-file changes, obvious fixes, <5 min work |
| **Simple** | NO | 1-2 files, clear scope, <30 min work |
| **Medium** | NO | 3+ files but structured requirements, low ambiguity |
| **Architecture** | YES | System design, long-term decisions, trade-off evaluation needed |
| **Complex** | YES | High-risk refactoring, many dependencies, significant impact |
| **Uncertain** | YES | Ambiguous goals, investigation needed, unclear path forward |

### Specific Scenarios

**Use for ARCHITECTURE tasks**:
- System design decisions (monolith vs microservices, database choices)
- Technology selection (frameworks, libraries, patterns)
- Long-term architectural planning (scalability, maintainability)
- Security and compliance design

**Use for HIGH-COMPLEXITY refactoring**:
- Migrating monoliths to microservices
- Changing core data structures or APIs
- Removing technical debt with wide impact
- Performance optimizations affecting multiple modules

**Use for UNCERTAIN requirements**:
- User provides vague requests ("optimize data", "improve UX")
- Need to investigate before planning
- Multiple possible interpretations of requirements
- Research-heavy tasks with open-ended goals

### When NOT to use me

**Skip sequential-thinking for**:
- Yes/no questions with clear answers
- Syntax lookup or documentation queries
- Single-line typo fixes
- Adding obvious features with clear scope
- Simple configuration changes
- Formatting or style-only tasks

## How to use me

### Tool Invocation

The tool is named `sequantial-thinking-mcp_sequentialthinking` (note: "sequantial" is intentional, not a typo).

### Parameters

| Parameter | Type | Required | Description |
|-----------|-------|----------|-------------|
| `thought` | string | YES | Current thinking step content |
| `nextThoughtNeeded` | boolean | YES | Whether another thought step is needed |
| `thoughtNumber` | number | YES | Current thought number (1, 2, 3...) |
| `totalThoughts` | number | YES | Estimated total thoughts (can adjust up/down) |
| `isRevision` | boolean | NO | Whether this thought revises a previous one |
| `revisesThought` | number | NO | If isRevision, which thought number is being reconsidered |
| `branchFromThought` | number | NO | If branching, which thought to branch from |
| `branchId` | string | NO | Identifier for current branch (if branching) |
| `needsMoreThoughts` | boolean | NO | If reaching "end" but realizing more analysis needed |

### Usage Pattern

1. **Start with estimate**: Set `thoughtNumber: 1`, `totalThoughts: N` (your initial guess)
2. **Build incrementally**: Each thought builds on previous analysis
3. **Adjust as needed**: Can increase `totalThoughts` if discovering more complexity
4. **Reconsider when uncertain**: Use `isRevision: true` to question previous conclusions
5. **Branch for alternatives**: Use `branchFromThought` to explore different approaches
6. **Signal completion**: Set `nextThoughtNeeded: false` when satisfied with analysis
7. **Can extend after "end"**: Use `needsMoreThoughts: true` if realizing more analysis needed

### Recommended Limits

- **5-7 thoughts** for typical analysis
- Avoid overthinking (10+ thoughts) unless task is exceptionally complex
- Use branching instead of single long thought chain for multiple alternatives

### Advanced Features

**Branching**:
```
Thought 1: Analyze problem
Thought 2: Consider approach A
Thought 3: Branch to approach B (branchFromThought=2, branchId="alt-b")
  → Explore alternative without losing approach A context
```

**Revision**:
```
Thought 3: Decision: Use X
Thought 4: Realize X has problem Y
Thought 5: isRevision=true, revisesThought=3, "Reconsider: X may not work because Y"
```

**Extension**:
```
Thought 5: Conclusion: Use approach A
Thought 6: needsMoreThoughts=true, "Wait, just realized constraint Z breaks A"
```

## Example Scenarios

### Example 1: Architecture Decision

**Task**: "Design authentication system for our app"

**Sequential-Thinking Session**:
```
Thought 1: Analyze requirements - what auth providers needed? (OAuth, JWT, session?)
  Consider: User base, security needs, existing infrastructure
  nextThoughtNeeded: true

Thought 2: Evaluate options
  - NextAuth.js: Fast setup, integrates well with our stack
  - Custom JWT: More control, more work
  - Session-based: Simpler, less scalable
  Trade-offs: Setup time vs flexibility vs performance
  nextThoughtNeeded: true

Thought 3: Predict long-term consequences
  NextAuth: Easy now, but provider updates could break things
  Custom JWT: More work now, but full control over upgrades
  Session: Scaling issues if user count grows significantly
  nextThoughtNeeded: true

Thought 4: Formulate hypothesis
  Recommendation: NextAuth.js for rapid development
  Rationale: Our timeline is tight, NextAuth covers most providers
  Risk: Future provider updates require testing
  nextThoughtNeeded: true

Thought 5: Verify hypothesis
  Does NextAuth align with requirements?
  - Provider support: Yes (Google, GitHub, email)
  - Security: Good, battle-tested
  - Timeline: Fits constraints
  Conclusion: Hypothesis validated
  nextThoughtNeeded: false
```

**Result**: Well-reasoned architecture recommendation with documented trade-offs and risks.

---

### Example 2: Complex Refactoring

**Task**: "Migrate monolithic auth service to microservices"

**Sequential-Thinking Session**:
```
Thought 1: Map current dependencies
  Which modules depend on auth service?
  - User profile module (heavy coupling)
  - Payment gateway (needs user verification)
  - Analytics (tracks auth events)
  Risk: Breaking changes could cascade across system
  nextThoughtNeeded: true

Thought 2: Identify failure points
  - Direct database access from multiple services
  - Shared auth token generation logic
  - Synchronous auth checks (latency bottlenecks)
  nextThoughtNeeded: true

Thought 3: Design migration strategy
  Option A: Big bang - all at once
  Option B: Incremental - feature by feature
  Risk analysis:
  - A: High risk, no rollback path
  - B: Lower risk, but longer timeline with dual maintenance
  nextThoughtNeeded: true

Thought 4: Plan rollback strategy
  If Option B fails:
  - Keep old service running as fallback
  - Feature flags to switch back
  - Data sync to prevent inconsistency
  nextThoughtNeeded: true

Thought 5: Define test verification
  - Load test before migration
  - Integration tests for cross-service communication
  - Monitor auth latency during rollout
  nextThoughtNeeded: true

Thought 6: Final plan
  Strategy: Incremental migration (Option B)
  Timeline: 4 phases, 2 weeks each
  Rollback: Feature flags, old service on standby
  Testing: Load test + integration tests + monitoring
  nextThoughtNeeded: false
```

**Result**: Safe migration plan with clear phases, rollback options, and verification steps.

---

### Example 3: Uncertain Requirements

**Task**: User says "We need to optimize data performance"

**Sequential-Thinking Session**:
```
Thought 1: What does "data" mean?
  Possibilities:
  - Database query performance
  - API response times
  - Data processing pipelines
  - Analytics/aggregation speed
  Uncertainty: Cannot plan without clarifying scope
  nextThoughtNeeded: true

Thought 2: Hypothesize use cases
  Branch A: User-facing performance (UI loading, API calls)
  Branch B: Internal performance (batch jobs, analytics)
  Branch C: Storage/cost optimization (database sizing, caching)
  Each branch has very different solutions
  nextThoughtNeeded: true

Thought 3: Branch A exploration (UI/API)
  If this is the issue:
  - Caching strategy (Redis, CDN)
  - Database indexing
  - API response pagination
  nextThoughtNeeded: true

Thought 4: Branch B exploration (internal)
  If this is the issue:
  - Batch job parallelization
  - ETL pipeline optimization
  - Message queuing (Kafka, RabbitMQ)
  nextThoughtNeeded: true

Thought 5: Branch C exploration (storage)
  If this is the issue:
  - Database sharding
  - Data compression
  - Archive old data
  nextThoughtNeeded: true

Thought 6: Formulate questions for user
  Before planning, ask:
  1. Is this about user-facing performance (API/UI) or internal jobs?
  2. What are the current pain points? (slow loading, timeouts, high costs?)
  3. Any specific metrics? (response time > 2s, CPU > 80%, storage > 10TB?)
  4. Any constraints? (budget, timeline, tech stack limits?)
  Rationale: Answers will narrow down to one branch
  nextThoughtNeeded: false
```

**Result**: Targeted, context-aware questions that quickly identify actual requirements.

---

## Integration Points

### Before Interview Questions

Use sequential-thinking when requirements are unclear to frame better questions:

**Example**: Before asking "What do you want?", first analyze:
- What information is missing?
- What assumptions can I make?
- What clarifying questions will be most valuable?

**Benefit**: More focused, productive interview sessions.

### After Explore/Librarian Research

Use sequential-thinking to synthesize multiple sources of information:

**Example**: After gathering context from codebase and docs, use to:
- Identify patterns and contradictions
- Form a coherent understanding
- Generate informed questions or recommendations

**Benefit**: Deeper insights than surface-level synthesis.

### Before Plan Generation

Use sequential-thinking to verify logical consistency of planned approach:

**Example**: Before generating tasks, analyze:
- Does the approach address all requirements?
- Are there logical gaps or contradictions?
- Are dependencies correctly ordered?
- Are acceptance criteria realistic?

**Benefit**: Higher-quality plans with fewer revisions.

### During Complex Decisions

Use sequential-thinking when weighing alternatives:

**Example**: When choosing between multiple technical options:
- Evaluate trade-offs (performance, maintainability, complexity)
- Predict long-term consequences
- Identify risk factors
- Formulate justified recommendation

**Benefit**: Well-reasoned decisions with documented rationale.

### Anti-Patterns (Don't do this)

**Don't use sequential-thinking for**:
- Syntax queries ("How do I write a for loop in Python?") → Use documentation or librarian
- Yes/no questions with clear answers → Direct answer is faster
- Simple code changes with clear scope → Overhead not justified
- Trivial bug fixes → Just fix it
- Formatting/style-only tasks → Use linter or formatter

## Fallback Guidance

If sequential-thinking MCP is unavailable or errors occur:

1. **Continue with standard workflow** - The tool enhances but is not required
2. **Document uncertainty** - If stuck, note what information is missing
3. **Ask clarifying questions** - Engage user when requirements are unclear
4. **Use other agents** - Oracle for architecture, Librarian for research

The skill is designed to **enhance** planning, not block it.

## Summary

Use this skill to:
- Make better decisions for complex, high-stakes tasks
- Avoid overlooking important considerations
- Provide well-reasoned recommendations with clear rationale
- Structure your thinking when problems are ambiguous

**Key principle**: Sequential-thinking is a tool, not a mandate. Use it when it adds value, skip it when it doesn't.
