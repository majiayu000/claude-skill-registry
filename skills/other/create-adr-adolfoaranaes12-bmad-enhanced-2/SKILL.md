---
name: create-adr
description: Create Architecture Decision Records (ADRs) documenting key architectural choices. Analyzes context, evaluates alternatives, and captures decisions using standard ADR template. Use when documenting database design, technology selection, pattern choices, or architectural trade-offs.
acceptance:
  - adr_complete: "ADR document created with all required sections"
  - alternatives_analyzed: "At least 2 alternatives evaluated with pros/cons"
  - rationale_clear: "Decision rationale clearly explained"
  - consequences_documented: "Positive and negative consequences identified"
inputs:
  context:
    type: string
    required: true
    description: "Decision context (e.g., file path to analyze, or description of decision)"
    validation: "Must describe what decision needs to be made or what to analyze"
  decision_number:
    type: number
    required: false
    description: "ADR number (auto-incremented if not provided)"
outputs:
  adr_created:
    type: boolean
    description: "Whether ADR was successfully created"
  adr_path:
    type: string
    description: "Path to created ADR file"
  decision_number:
    type: number
    description: "ADR number assigned"
telemetry:
  emit: "skill.create-adr.completed"
  track:
    - decision_number
    - context_type
    - alternatives_count
    - duration_ms
---

# Create Architecture Decision Record (ADR)

## Overview

Create comprehensive Architecture Decision Records following industry best practices. ADRs document architectural choices, alternatives considered, rationale, and consequences to provide context for future development.

**ADR Structure:**
- **Context**: Problem and constraints
- **Decision**: What was decided
- **Alternatives**: Options evaluated with pros/cons
- **Rationale**: Why this decision was made
- **Consequences**: Positive, negative, and neutral impacts

## Prerequisites

- docs/adrs/ directory (created if missing)
- Context for decision (file to analyze, problem description, or existing architecture)

---

## Workflow

### Step 0: Determine ADR Number

**Action:** Find next available ADR number.

```bash
# List existing ADRs
ls -la docs/adrs/ 2>/dev/null || echo "ADR directory does not exist"

# Find highest number
find docs/adrs/ -name "adr-*.md" 2>/dev/null | \
  sed 's/.*adr-\([0-9]*\)-.*/\1/' | \
  sort -n | \
  tail -1
```

**Calculate next number:**
- If no ADRs exist: Start at 001
- If ADRs exist: Increment highest by 1

**Create ADR directory if missing:**
```bash
mkdir -p docs/adrs
```

---

### Step 1: Analyze Context

**Action:** Understand what decision needs to be documented.

**Context Types:**

**1. File/Schema Analysis** (like Prisma schema):
```bash
# Read the file to analyze
Read(file_path: {context_path})
```

Analyze to identify:
- **Technology choices**: Database, ORM, patterns used
- **Data modeling decisions**: Schema structure, relationships
- **Architectural patterns**: Multi-tenancy, event sourcing, etc.
- **Design tradeoffs**: Normalization vs. denormalization, indexing strategies

**2. Technology Selection:**
- List technologies being compared
- Identify requirements driving selection
- Note constraints (team skills, budget, timeline)

**3. Pattern Adoption:**
- Describe pattern being adopted
- Explain problem it solves
- Note implementation approach

---

### Step 2: Identify Key Decisions

**Action:** Extract architectural decisions from context.

**For Schema/File Analysis:**
Scan for decision indicators:
- Database technology (PostgreSQL, MySQL, MongoDB)
- ORM choice (Prisma, TypeORM, Sequelize)
- Schema patterns (multi-tenancy, soft deletes, audit logs)
- Relationship modeling (one-to-many, many-to-many)
- Indexing strategy
- Enum usage for type safety
- JSON/JSONB for flexibility

**Example from Prisma Schema:**
```prisma
// Decision indicators:
- PostgreSQL chosen (ADR: Database Selection)
- Prisma ORM (ADR: ORM Selection)
- Multi-tenancy via hotelId (ADR: Multi-Tenancy Strategy)
- Clerk for auth (ADR: Authentication Provider)
- Event sourcing pattern (ADR: Event Processing Architecture)
```

**Prioritize decisions:**
1. **High Impact**: Database, framework, major patterns
2. **Medium Impact**: Libraries, architectural patterns
3. **Low Impact**: Utility choices, minor patterns

Focus on 1-3 most significant decisions per ADR.

---

### Step 3: Research Alternatives

**Action:** Identify alternatives that could have been chosen.

**For Technology Decisions:**
```
Database: PostgreSQL
Alternatives:
- MySQL (widely used, simpler)
- MongoDB (NoSQL, flexible schema)
- SQLite (embedded, simple)
```

**For each alternative, identify:**
- **Pros**: Advantages and strengths
- **Cons**: Disadvantages and limitations
- **Use cases**: When it's the better choice

**Research sources:**
- Official documentation
- Comparison articles
- Team experience
- Industry best practices

**Minimum alternatives:** At least 2 (typically 3-4)

---

### Step 4: Determine Rationale

**Action:** Explain why the chosen option was selected.

**Rationale factors:**
- **Requirements fit**: How well option meets requirements
- **Team expertise**: Existing skills and experience
- **Timeline**: Impact on delivery speed
- **Cost**: Licensing, hosting, maintenance
- **Scalability**: Handles expected growth
- **Community**: Support availability
- **Risk**: Maturity and stability

**Example rationale:**
```
PostgreSQL chosen over MongoDB because:
1. Data is highly relational (users → hotels → conversations)
2. ACID transactions required for billing
3. Team has strong SQL experience (no MongoDB experience)
4. Scale fits PostgreSQL capabilities (100K users proven)
5. Full-text search built-in (eliminates Elasticsearch)
```

**Make rationale specific and measurable.**

---

### Step 5: Identify Consequences

**Action:** Document impacts of the decision.

**Consequence Types:**

**Positive Consequences:**
- Benefits gained
- Problems solved
- Capabilities enabled

**Negative Consequences:**
- Limitations introduced
- Tradeoffs accepted
- Future constraints

**Mitigation Strategies:**
For each negative consequence, document mitigation:
```
Negative: PostgreSQL vertical scaling limits
Mitigation: Plan read replica strategy, monitor query performance
```

**Neutral Consequences:**
- Changes with mixed/unclear impact
- Future considerations
- Monitoring needs

**Be honest about tradeoffs** - every decision has pros and cons.

---

### Step 6: Write ADR

**Action:** Create ADR document using standard template.

**ADR Template:**
```markdown
# ADR-{NUMBER}: {Decision Title}

**Date:** {YYYY-MM-DD}
**Status:** Accepted
**Deciders:** {Team/Role}

## Context

{What problem are we solving? What constraints exist?}

{For schema analysis: Describe the schema structure and requirements}

## Decision

We will use **{CHOSEN OPTION}** for {PURPOSE}.

## Alternatives Considered

### Option 1: {Chosen Option}
**Pros:**
- {Advantage 1}
- {Advantage 2}

**Cons:**
- {Disadvantage 1}
- {Disadvantage 2}

### Option 2: {Alternative}
**Pros:**
- {Advantage 1}

**Cons:**
- {Disadvantage 1}

### Option 3: {Alternative}
**Pros:**
- {Advantage 1}

**Cons:**
- {Disadvantage 1}

## Rationale

{Explain why chosen option was selected over alternatives}

{Be specific: "PostgreSQL chosen because data is relational and team has SQL expertise"}

## Consequences

**Positive:**
- {Benefit 1}
- {Benefit 2}

**Negative:**
- {Limitation 1}
  - *Mitigation:* {How we'll address this}

**Neutral:**
- {Consideration 1}

## Related Decisions

- ADR-XXX: {Related decision}

## Notes

{Additional context, benchmarks, links, team discussions}
```

**File naming:**
```
docs/adrs/adr-{NUMBER}-{kebab-case-title}.md

Examples:
- docs/adrs/adr-001-database-selection.md
- docs/adrs/adr-002-orm-choice.md
- docs/adrs/adr-003-multi-tenancy-strategy.md
```

---

### Step 7: Verify ADR Quality

**Action:** Check ADR completeness and quality.

**Quality Checklist:**

✅ **Context section:**
- [ ] Problem clearly stated
- [ ] Constraints identified
- [ ] Requirements listed

✅ **Alternatives (minimum 2):**
- [ ] Each has pros and cons
- [ ] Comparison is balanced
- [ ] Technical depth appropriate

✅ **Rationale:**
- [ ] Explains "why" not just "what"
- [ ] Specific and measurable
- [ ] References requirements

✅ **Consequences:**
- [ ] Positive impacts listed
- [ ] Negative impacts with mitigations
- [ ] Honest about tradeoffs

✅ **Writing quality:**
- [ ] Clear and concise
- [ ] No jargon without explanation
- [ ] Readable by future team members

**If quality checks fail:**
- Revise weak sections
- Add missing details
- Clarify ambiguous statements

---

## Output

Return structured output:

```json
{
  "adr_created": true,
  "adr_path": "docs/adrs/adr-001-database-selection.md",
  "decision_number": 1,
  "decision_title": "Database Selection",
  "alternatives_count": 3,
  "telemetry": {
    "skill": "create-adr",
    "decision_number": 1,
    "context_type": "schema_analysis",
    "alternatives_count": 3,
    "duration_ms": 12000
  }
}
```

---

## Error Handling

### Error 1: No Context Provided
**Error:** "Context required for ADR creation"
**Action:** Ask user for decision context or file to analyze

### Error 2: Cannot Determine Decision
**Error:** "Cannot identify architectural decision from context"
**Action:** Ask user to clarify what decision needs documenting

### Error 3: Insufficient Alternatives
**Error:** "At least 2 alternatives required"
**Action:** Research additional options or ask user for alternatives

---

## Examples

### Example 1: Database Schema Analysis

**Input:** `context: "packages/backend/src/schema.prisma"`

**Output ADR:**
```markdown
# ADR-001: PostgreSQL Database with Prisma ORM

**Date:** 2025-11-05
**Status:** Accepted
**Deciders:** Backend Team

## Context

Need database for multi-tenant SaaS application managing hotels, conversations, and analytics. Requirements:
- Relational data (hotels → users → conversations → messages)
- ACID transactions (billing, user management)
- Full-text search
- Multi-tenancy via hotelId
- TypeScript integration

## Decision

Use **PostgreSQL** with **Prisma ORM** for database layer.

[... rest of ADR with alternatives, rationale, consequences ...]
```

### Example 2: Technology Selection

**Input:** `context: "Choose state management for React app"`

**Output ADR:**
```markdown
# ADR-002: State Management Strategy

**Date:** 2025-11-05
**Status:** Accepted

## Context

React application needs client state management for:
- User authentication state
- Global UI state (theme, modals)
- Form state (multi-step wizards)

[... alternatives: Zustand, Redux, Context ...]
```

---

## Using This Skill

**From Winston subagent:**
```bash
/winston *create-adr "packages/backend/src/schema.prisma"
/winston *create-adr "Choose between REST and GraphQL"
```

**Directly:**
```bash
Use create-adr skill with context: "Analyze authentication strategy in src/auth/"
```

---

## Philosophy

ADRs are **living documentation** that:
- **Preserve context** for future developers
- **Document tradeoffs** honestly
- **Explain "why"** not just "what"
- **Guide future decisions** through patterns

Good ADRs prevent "why did we do this?" questions 6 months later.

---

## References

- Michael Nygard's ADR template (original)
- ThoughtWorks Technology Radar ADR guidance
- MADR (Markdown ADR) format specification
- `references/adr-examples.md` for complete examples
