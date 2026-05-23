---
name: debate-workflow
version: 1.0.0
description: Structured multi-perspective debate for important architectural decisions and complex trade-offs
auto_activates:
  - "architectural decision"
  - "design trade-off"
  - "framework selection"
  - "major refactoring"
  - "controversial change"
  - "multiple valid approaches"
explicit_triggers:
  - /amplihack:debate
confirmation_required: true
token_budget: 3500
---

# Debate Workflow Skill

## Purpose

Implement structured multi-perspective debate for important architectural decisions, design trade-offs, and complex problems where multiple valid approaches exist.

## When to Use This Skill

**USE FOR:**
- Major architectural decisions (framework selection, system design)
- Complex trade-offs with no clear winner
- Controversial changes affecting multiple teams
- High-impact decisions requiring buy-in
- When perspectives genuinely conflict

**AVOID FOR:**
- Simple implementation choices
- Decisions with obvious correct answer
- Time-sensitive hot fixes
- Minor refactoring
- Routine feature additions

## Configuration

### Core Parameters

**Number of Perspectives:**
- `3` - Default (security, performance, simplicity)
- `5` - Extended (add: maintainability, user-experience)
- `7` - Comprehensive (add: scalability, cost)

**Debate Rounds:**
- `2` - Quick (position + challenge)
- `3` - Standard (position + challenge + synthesis)
- `4-5` - Deep (multiple challenge/response cycles)

**Convergence Criteria:**
- `100%` - Strong consensus (all perspectives agree)
- `2/3` - Majority rule (two-thirds agreement)
- `synthesis` - Facilitator synthesizes best hybrid
- `evidence` - Follow strongest evidence/arguments

## Standard Perspective Profiles

**Security Perspective:**
- Focus: Vulnerabilities, attack vectors, data protection
- Questions: "What could go wrong? How do we prevent breaches?"
- Agent: security agent

**Performance Perspective:**
- Focus: Speed, scalability, resource efficiency
- Questions: "Will this scale? What are the bottlenecks?"
- Agent: optimizer agent

**Simplicity Perspective:**
- Focus: Minimal complexity, ruthless simplification
- Questions: "Is this the simplest solution? Can we remove abstractions?"
- Agent: cleanup agent + reviewer agent

**Maintainability Perspective:**
- Focus: Long-term evolution, technical debt
- Questions: "Can future developers understand this? How hard to change?"
- Agent: reviewer agent + architect agent

**User Experience Perspective:**
- Focus: API design, usability, developer experience
- Questions: "Is this intuitive? How will users interact with this?"
- Agent: api-designer agent

**Scalability Perspective:**
- Focus: Growth capacity, distributed systems
- Questions: "What happens at 10x load? 100x?"
- Agent: optimizer agent + architect agent

**Cost Perspective:**
- Focus: Resource usage, infrastructure costs, development time
- Questions: "What's the ROI? Are we over-engineering?"
- Agent: analyzer agent

## Execution Process

### Step 1: Frame the Decision

- **Use ambiguity agent** to clarify the decision to be made
- **Use prompt-writer agent** to create clear decision prompt
- Define decision scope and constraints
- Identify stakeholder concerns
- List evaluation criteria
- Document explicit user requirements that constrain options
- **CRITICAL: Frame decision as question, not predetermined answer**

**Decision Framing Template:**
```markdown
# Decision: [Brief Title]

## Question
[One-sentence question to be debated]

## Context
[Why this decision matters, background information]

## Constraints
[Non-negotiable requirements, technical limitations]

## Evaluation Criteria
[How we'll judge proposed solutions]

## Perspectives to Include
[Which viewpoints are most relevant]
```

**Example:**
```markdown
# Decision: Data Storage Strategy for User Analytics

## Question
Should we use PostgreSQL with JSONB, MongoDB, or ClickHouse
for storing and querying user analytics events?

## Context
- 10M events/day expected at launch
- 100M events/day within 2 years
- Complex queries for dashboard analytics
- Real-time and historical reporting needed

## Constraints
- Must handle 10M events/day minimum
- Query latency < 200ms for dashboards
- Budget: $5K/month infrastructure
- Team familiar with PostgreSQL, not ClickHouse

## Evaluation Criteria
1. Performance at scale
2. Query flexibility
3. Operational complexity
4. Cost at scale
5. Team learning curve

## Perspectives to Include
Performance, Cost, Maintainability, Scalability
```

### Step 2: Initialize Perspectives

- Select N perspectives relevant to decision
- **Spawn Claude subprocess for each perspective**
- Each subprocess receives decision framing doc
- Each subprocess assigned perspective profile
- **No context sharing between perspectives yet**
- Each forms initial position independently

**Initial Position Requirements:**
- State recommended approach
- Provide 3-5 supporting arguments
- Identify risks of alternative approaches
- Quantify claims where possible

### Step 3: Debate Round 1 - Initial Positions

- Collect initial positions from all perspectives
- **Use analyzer agent** to synthesize positions
- Document each perspective's recommendation
- Identify areas of agreement
- Identify areas of conflict
- Surface assumptions made by each perspective

**Round 1 Output Structure:**
```markdown
## Security Perspective: [Recommendation]

Arguments For:
1. [Argument with evidence]
2. [Argument with evidence]
3. [Argument with evidence]

Concerns About Alternatives:
- [Alternative A]: [Specific concern]
- [Alternative B]: [Specific concern]

Assumptions:
- [Assumption 1]
- [Assumption 2]
```

### Step 4: Debate Round 2 - Challenge and Respond

- Share all Round 1 positions with all perspectives
- Each perspective challenges other perspectives' arguments
- Each perspective defends their position against challenges
- **Use analyzer agent** to track argument strength
- Identify which arguments withstand scrutiny
- Document concessions and refinements

**Challenge Format:**
```markdown
## [Perspective A] challenges [Perspective B]

Challenge: [Question or counter-argument]
Evidence: [Supporting data or examples]
Request: [What would change your position?]
```

**Response Format:**
```markdown
## [Perspective B] responds to [Perspective A]

Response: [Address the challenge]
Concession: [Points where you agree or adjust]
Counter: [Additional evidence or reasoning]
```

### Step 5: Debate Round 3 - Find Common Ground

- Identify points of consensus across perspectives
- Surface remaining disagreements explicitly
- Explore hybrid approaches combining insights
- **Use architect agent** to design synthesis options
- Validate hybrid approaches against all perspectives
- Document convergence or divergence

**Convergence Analysis:**
```markdown
## Areas of Agreement
1. [Consensus point 1]
2. [Consensus point 2]

## Remaining Disagreements
1. [Disagreement 1]
   - Security says: [position]
   - Performance says: [position]
   - Potential resolution: [hybrid approach]

## Hybrid Approaches Identified
1. [Hybrid Option 1]
   - Combines: [which perspectives]
   - Trade-offs: [explicit costs/benefits]
```

### Step 6: Facilitator Synthesis

- **Use architect agent** as neutral facilitator
- **Use analyzer agent** to evaluate all arguments
- Review all debate rounds systematically
- Identify strongest evidence-based arguments
- Make recommendation with confidence level
- Document decision rationale thoroughly
- Include dissenting views explicitly

**Synthesis Structure:**
```markdown
## Facilitator Synthesis

### Recommendation
[Clear statement of recommended approach]

### Confidence Level
[High/Medium/Low] confidence based on:
- Consensus level: [X% of perspectives agree]
- Evidence quality: [Strong/Moderate/Weak]
- Risk level: [Low/Medium/High if wrong]

### Rationale
[Explanation of why this recommendation]

### Key Arguments That Won
1. [Argument that swayed decision]
2. [Argument that swayed decision]
3. [Argument that swayed decision]

### Key Arguments Against (Dissenting Views)
1. [Strongest counter-argument]
2. [Remaining concern]

### Implementation Guidance
[How to execute this decision]

### Success Metrics
[How we'll know if this was the right choice]

### Revisit Triggers
[Conditions that would require reconsidering this decision]
```

### Step 7: Decision Documentation

- Create decision record: `decisions/YYYY-MM-DD-decision-name.md`
- Document full debate transcript
- Include all perspective arguments
- Record synthesis and final decision
- Add to `.claude/context/DISCOVERIES.md`
- Update relevant architecture docs

**Decision Record Template:**
```markdown
# Decision Record: [Title]

Date: [YYYY-MM-DD]
Status: Accepted
Decision Makers: [List perspectives included]

## Context
[What decision was needed and why]

## Decision
[What was decided]

## Consequences
[What happens because of this decision]

## Alternatives Considered
[What other options were debated]

## Debate Summary
[Key arguments from each perspective]

## Dissenting Opinions
[Perspectives that disagreed and why]

## Review Date
[When to revisit this decision]

---

## Full Debate Transcript

### Round 1: Initial Positions
[Complete positions from all perspectives]

### Round 2: Challenges and Responses
[All challenge/response exchanges]

### Round 3: Convergence Analysis
[Common ground and hybrid approaches]

### Facilitator Synthesis
[Complete synthesis document]
```

### Step 8: Implement Decision

- **Use builder agent** to implement chosen approach
- Follow the decided path from synthesis
- Implement monitoring for success metrics
- Set up alerts for revisit triggers
- Document decision in code comments
- Create runbook if operational complexity added

## Trade-Offs

**Cost:** Multiple agent cycles, longer decision time
**Benefit:** Well-reasoned decisions, surface hidden risks
**Best For:** Decisions that are expensive to reverse

## Examples

### Example 1: API Design - REST vs GraphQL

**Configuration:**
- Perspectives: 5 (Simplicity, Performance, User-Experience, Maintainability, Cost)
- Rounds: 3
- Convergence: Synthesis

**Debate Summary:**
- Simplicity: REST is straightforward, well-understood
- Performance: GraphQL reduces over-fetching, fewer round trips
- UX: GraphQL gives frontend flexibility, better DX
- Maintainability: REST easier to version and evolve
- Cost: GraphQL higher learning curve, more complex infrastructure

**Result:** REST for initial MVP, GraphQL for v2
- Rationale: Team knows REST, faster to ship
- Migration path: Add GraphQL layer in 6 months
- Trigger: When frontend requests 3+ endpoints per view

### Example 2: Testing Strategy - Unit vs Integration Heavy

**Configuration:**
- Perspectives: 3 (Simplicity, Maintainability, Performance)
- Rounds: 2
- Convergence: 2/3 majority

**Debate Summary:**
- Simplicity: Unit tests, mock all dependencies
- Maintainability: Integration tests, test real interactions
- Performance: Mix, optimize for feedback speed

**Result:** 70% unit, 30% integration (Majority agreed)
- Rationale: Unit tests faster feedback, integration tests catch real issues
- Dissent: Simplicity wanted 90% unit tests (overruled by maintainability concerns)

### Example 3: Deployment Strategy - Kubernetes vs Serverless

**Configuration:**
- Perspectives: 5 (Cost, Simplicity, Scalability, Performance, Maintainability)
- Rounds: 4
- Convergence: Synthesis (no majority)

**Debate Summary:**
- Long, contentious debate with no clear winner
- Cost and Simplicity favored serverless
- Scalability and Performance favored Kubernetes
- Maintainability split (serverless simpler, k8s more control)

**Result:** Serverless with k8s option researched
- Rationale: Start simple, team small, serverless faster
- Hybrid: Evaluate k8s at 10x scale or complex networking needs
- Strong dissent documented: Performance perspective believes this will need revisiting soon

## Philosophy Alignment

This workflow enforces:
- **Perspective Diversity:** Multiple viewpoints surface hidden trade-offs
- **Evidence-Based:** Arguments must be supported, not just opinions
- **Transparent Trade-offs:** Dissent is documented, not hidden
- **Structured Exploration:** Debate format prevents premature convergence
- **Decision Quality:** Better decisions through rigorous analysis
- **Learning:** Debate transcripts become organizational knowledge

## Integration with Default Workflow

This workflow replaces Step 4 (Research and Design) of the DEFAULT_WORKFLOW when complex decisions require multi-perspective analysis. Implementation (Step 5) proceeds with the consensus decision.
