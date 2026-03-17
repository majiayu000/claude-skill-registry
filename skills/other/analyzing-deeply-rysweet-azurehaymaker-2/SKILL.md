---
name: "Analyzing Problems Deeply"
description: "Performs deep structured analysis on complex or ambiguous problems. Activates when problems are unclear, have multiple perspectives, or require careful thinking before proceeding. Uses ultrathink methodology for systematic exploration of problem space."
---

# Analyzing Problems Deeply

You are activating deep analysis capabilities. Your role is to systematically explore complex problems before rushing to solutions.

## When to Activate

This skill activates when:

- User says "I'm not sure...", "I'm confused...", "Help me think through..."
- Problem statement is ambiguous or unclear
- Multiple competing approaches exist
- High-stakes decision with significant consequences
- Contradictory requirements or constraints
- Previous attempts at solving failed
- Need to understand problem deeply before implementing

## Philosophy

### Why Deep Analysis?

- **Premature Solutions**: Rushing to code often solves wrong problem
- **Hidden Complexity**: Surface-level understanding misses critical factors
- **False Assumptions**: Unchallenged assumptions lead to wrong paths
- **Missed Opportunities**: Deeper analysis reveals better solutions

### When NOT to Use

- Problem is well-defined and straightforward
- Solution is obvious and simple
- Time pressure requires quick action
- Problem has been deeply analyzed already
- Analysis paralysis risk (over-thinking simple problems)

## Analysis Process

### 1. Problem Clarification

Start by ensuring you understand the actual problem:

```markdown
## Initial Understanding

**As Stated**: [User's original request]

**My Interpretation**: [What I think they're asking]

**Questions Before Proceeding**:

1. [Clarifying question 1]
2. [Clarifying question 2]
3. [Clarifying question 3]

[Wait for user response before deep analysis]
```

### 2. Problem Decomposition

Break problem into analyzable components:

```markdown
## Problem Structure

**Core Problem**: [One sentence essence]

**Related Subproblems**:

1. Subproblem A: [Description]
2. Subproblem B: [Description]
3. Subproblem C: [Description]

**Dependencies**: [What depends on what]

**Constraints**:

- Technical: [Technical limitations]
- Business: [Business requirements]
- Resource: [Time, budget, people]
- External: [Third-party dependencies]

**Success Criteria**: [How do we know it's solved?]
```

### 3. Multi-Perspective Analysis

Examine from different angles:

#### Perspective 1: User/Customer

- What problem are they trying to solve?
- What outcome do they actually need?
- What's their mental model?
- What are their pain points?

#### Perspective 2: Technical

- What are the technical constraints?
- What are the implementation challenges?
- What are the performance requirements?
- What are the scalability needs?

#### Perspective 3: Business

- What's the ROI?
- What's the opportunity cost?
- What's the risk?
- What's the timeline?

#### Perspective 4: Maintenance

- Who will maintain this?
- How complex is it?
- What's the bus factor?
- What happens when requirements change?

### 4. Assumption Surfacing

Challenge hidden assumptions:

```markdown
## Assumptions to Validate

**Stated Assumptions**:

- [Assumption 1]: [Why we believe it]
- [Assumption 2]: [Why we believe it]

**Unstated Assumptions** (discovered):

- [Hidden assumption 1]: [Impact if wrong]
- [Hidden assumption 2]: [Impact if wrong]

**Critical to Verify**:

- [Most risky assumption]: [How to validate]
```

### 5. Option Generation

Explore solution space:

```markdown
## Solution Options

### Option 1: [Name]

**Approach**: [How it works]
**Pros**: [Advantages]
**Cons**: [Disadvantages]
**Risks**: [What could go wrong]
**Effort**: [High/Medium/Low]
**Impact**: [High/Medium/Low]

### Option 2: [Name]

[Same structure]

### Option 3: [Name]

[Same structure]

### Option 0: Do Nothing

**Consequences**: [What happens if we don't solve this]
**Is this viable?**: [Yes/No + reasoning]
```

### 6. Tradeoff Analysis

Compare options systematically:

```markdown
## Tradeoff Matrix

| Dimension         | Option 1 | Option 2 | Option 3 |
| ----------------- | -------- | -------- | -------- |
| Complexity        | Low      | Medium   | High     |
| Performance       | Medium   | High     | High     |
| Maintainability   | High     | Medium   | Low      |
| Time to Implement | 2 weeks  | 4 weeks  | 8 weeks  |
| Risk              | Low      | Medium   | High     |
| Scalability       | Medium   | High     | High     |

## Key Tradeoffs

**Speed vs Quality**: [Analysis]
**Complexity vs Flexibility**: [Analysis]
**Cost vs Capability**: [Analysis]
**Short-term vs Long-term**: [Analysis]
```

### 7. Risk Assessment

Identify and analyze risks:

```markdown
## Risk Analysis

### Risk 1: [Name]

- **Probability**: High/Medium/Low
- **Impact**: High/Medium/Low
- **Mitigation**: [How to reduce risk]
- **Contingency**: [What if risk occurs]

### Risk 2: [Name]

[Same structure]

**Highest Priority Risks**:

1. [Most critical risk to address]
2. [Second most critical]
```

### 8. Recommendation

Synthesize analysis into clear recommendation:

```markdown
## Recommendation

**Proposed Approach**: [Clear choice]

**Rationale**:

1. [Reason 1 with supporting analysis]
2. [Reason 2 with supporting analysis]
3. [Reason 3 with supporting analysis]

**This Approach**:

- Solves: [What it addresses]
- Accepts: [Tradeoffs we're making]
- Risks: [Risks we're taking]
- Mitigates: [How we reduce risk]

**Implementation Path**:

1. [First step]
2. [Second step]
3. [Third step]

**Decision Points**:

- [Checkpoint 1]: [What to validate]
- [Checkpoint 2]: [What to validate]

**Reversibility**: [Can we change our mind later? How?]
```

## Analysis Dimensions

### Technical Dimension

- Feasibility and implementation complexity
- Performance and scalability characteristics
- Technology stack and dependencies
- Integration points and interfaces
- Testing and quality assurance needs

### Business Dimension

- Value delivered vs effort required
- Opportunity cost of alternatives
- Timeline and resource requirements
- ROI and business impact
- Market and competitive factors

### User Dimension

- User needs and pain points
- User experience and usability
- Adoption and change management
- Accessibility and inclusivity
- Support and documentation needs

### Organizational Dimension

- Team capabilities and skills
- Organizational priorities and politics
- Existing systems and processes
- Change resistance and culture
- Long-term maintenance and ownership

## Thinking Tools

### First Principles Thinking

Break down to fundamental truths:

1. What do we know for certain?
2. What are we assuming?
3. Can we rebuild from first principles?
4. What's actually required vs nice-to-have?

### Inversion

Think backwards:

1. How could this fail spectacularly?
2. What would make this impossible?
3. If we wanted the opposite outcome, what would we do?
4. What are we trying to avoid?

### Second-Order Effects

Look beyond immediate consequences:

1. If we do X, what happens?
2. Then what happens after that?
3. What are the ripple effects?
4. What changes in the system?

### Pre-Mortem

Imagine failure:

1. It's 6 months later, project failed. Why?
2. What warning signs did we miss?
3. What assumptions were wrong?
4. What could we have done differently?

### Opportunity Cost

What are we giving up:

1. If we do this, what can't we do?
2. What else could we do with these resources?
3. What's the next best alternative?
4. Is this the highest value use of time?

## Integration Points

### Invokes

- **Architect Agent**: For design implications
- **WebSearch**: For external validation
- **/ultrathink**: For even deeper structured analysis

### Escalates To

- **/ultrathink**: When analysis needs extreme depth (30+ min)
- **/consensus**: When multiple stakeholders need alignment
- **/debate**: When competing viewpoints need exploration
- **Architecting Solutions**: Once problem is understood, design solution

### References

- **Decision Frameworks**: `Specs/DecisionFrameworks.md`
- **Analysis Templates**: `Templates/ProblemAnalysis.md`

## Output Format

Structure analysis as:

```markdown
# Deep Analysis: [Problem Name]

## Problem Understanding

[Clarified problem statement]

## Problem Decomposition

[Subproblems and structure]

## Perspectives

[Multi-angle analysis]

## Assumptions

[Stated and hidden assumptions]

## Options

[Solution alternatives]

## Tradeoffs

[Systematic comparison]

## Risks

[Risk analysis]

## Recommendation

[Clear path forward]

## Next Steps

[Action items]
```

## Example Analysis

```markdown
# Deep Analysis: Choosing Database for New Project

## Problem Understanding

**As Stated**: "Should we use PostgreSQL or MongoDB for our new app?"

**My Interpretation**: Choosing data storage for application with:

- User data (profiles, auth)
- Content data (posts, comments)
- Analytics data (events, metrics)
- Unknown future requirements

**Questions Before Proceeding**:

1. What are the access patterns? (Read-heavy? Write-heavy?)
2. What's the data structure? (Relational? Nested documents?)
3. What's the scale? (Users, data size, queries/sec)
4. What's the team's expertise?

[User responds: Read-heavy, mostly relational with some nested data,
starting small but need to scale, team knows SQL]

## Problem Decomposition

**Core Problem**: Choose data storage that supports current needs while
enabling future growth without excessive complexity or cost.

**Related Subproblems**:

1. Data modeling: How to represent user/content relationships
2. Query patterns: How to efficiently access data
3. Scaling: How to grow as user base increases
4. Team productivity: How to develop quickly with existing skills

**Constraints**:

- Technical: Must handle 1M+ users eventually
- Business: 6-month timeline to launch
- Resource: 2 backend developers, both know SQL
- External: Need real-time features eventually

**Success Criteria**:

- Supports all CRUD operations efficiently
- Can scale to 1M+ users
- Team can develop productively
- Can evolve with changing requirements

## Perspectives

### User Perspective

- Don't care about database choice
- Want fast, responsive application
- Need reliable data consistency

### Technical Perspective

- Need ACID for user/payment data
- Could use denormalization for performance
- Real-time features need change feeds
- Team knows SQL, would need MongoDB training

### Business Perspective

- Faster time to market = more important than perfect choice
- Can migrate later if needed
- Team productivity = business velocity
- Hosting costs matter at scale

### Maintenance Perspective

- Simpler = easier to maintain
- Fewer technologies = smaller operational burden
- Team skills = faster debugging
- Common patterns = easier to hire for

## Assumptions to Validate

**Stated Assumptions**:

- Will need to scale to 1M+ users (based on business plan)
- Data is mostly relational (based on current understanding)

**Unstated Assumptions** (discovered):

- Need ACID transactions (Impact if wrong: data corruption)
- Team won't learn MongoDB quickly (Impact: slower development)
- Requirements won't radically change (Impact: wrong database choice)
- Single database handles everything (Impact: might need multiple)

**Critical to Verify**:

- "Mostly relational with some nested" - Can we use JSONB in PostgreSQL?
- "Need to scale" - What's actual timeline? Can we start simple?

## Solution Options

### Option 1: PostgreSQL

**Approach**: Relational DB with JSONB for nested data
**Pros**:

- Team knows it well (fast development)
- ACID guarantees
- Mature, reliable, well-documented
- JSONB handles nested data
- Can scale vertically initially, horizontally later
  **Cons**:
- More complex horizontal scaling
- Not ideal for true document workloads
- Need to design schema upfront
  **Risks**:
- Might hit scaling limits (mitigated by proven PostgreSQL scaling)
  **Effort**: Low (team expertise)
  **Impact**: High (proven, reliable)

### Option 2: MongoDB

**Approach**: Document database
**Pros**:

- Flexible schema
- Easy horizontal scaling
- Good for nested documents
- Built-in sharding
  **Cons**:
- Team needs to learn it (2-4 week ramp-up)
- Eventual consistency by default
- More operational complexity
- ACID only within documents (mostly)
  **Risks**:
- Team productivity hit during learning
- Consistency issues if not careful
  **Effort**: Medium (learning curve)
  **Impact**: Medium (works but slower start)

### Option 3: Both (PostgreSQL + MongoDB)

**Approach**: PostgreSQL for relational, MongoDB for documents
**Pros**:

- Right tool for each job
- Optimal performance
  **Cons**:
- Much higher complexity
- More operational burden
- Data consistency across databases
- Team needs both skills
  **Risks**:
- Over-engineering
- Complexity kills velocity
  **Effort**: High
  **Impact**: Low (unnecessary complexity)

### Option 0: Do Nothing

Not viable - need database for application.

## Tradeoff Analysis

| Dimension      | PostgreSQL | MongoDB | Both   |
| -------------- | ---------- | ------- | ------ |
| Team Velocity  | High ✓     | Medium  | Low    |
| Scalability    | Medium     | High ✓  | High ✓ |
| Complexity     | Low ✓      | Medium  | High   |
| Operational    | Low ✓      | Medium  | High   |
| Flexibility    | Medium     | High ✓  | High ✓ |
| Time to Launch | 6 mo ✓     | 8 mo    | 10 mo  |

**Key Tradeoffs**:

- **Speed vs Flexibility**: PostgreSQL faster to start, MongoDB more flexible
- **Known vs Optimal**: PostgreSQL = known and good, MongoDB = potentially better
- **Simplicity vs Scaling**: PostgreSQL simpler, MongoDB scales easier

## Risk Analysis

### Risk 1: PostgreSQL hits scaling limits

- **Probability**: Low (can handle 1M+ users with proper design)
- **Impact**: Medium (would need to migrate or shard)
- **Mitigation**: Design for scalability from start (indexes, queries)
- **Contingency**: Can migrate to MongoDB or add read replicas

### Risk 2: MongoDB slows team velocity

- **Probability**: High (learning curve is real)
- **Impact**: High (misses 6-month launch window)
- **Mitigation**: Training and pairing (still 2-4 week slowdown)
- **Contingency**: Fall back to PostgreSQL (wasted time)

### Risk 3: Requirements change dramatically

- **Probability**: Medium (startups pivot)
- **Impact**: Medium (might need different database)
- **Mitigation**: Either choice handles most patterns
- **Contingency**: Can migrate databases if necessary

## Recommendation

**Proposed Approach**: Start with PostgreSQL

**Rationale**:

1. **Team Velocity**: Team knows PostgreSQL, can develop 2x faster than learning MongoDB
2. **Time to Market**: 6-month deadline is tight, can't afford learning curve
3. **Good Enough**: PostgreSQL + JSONB handles the "nested data" requirement
4. **Proven Scale**: Instagram scaled to 100M+ users on PostgreSQL
5. **Reversible**: Can migrate to MongoDB later if truly needed (rare)

**This Approach**:

- Solves: All stated requirements with known technology
- Accepts: Slightly more complex horizontal scaling (when needed)
- Risks: Might need to migrate later (low probability)
- Mitigates: Fast time to market, team productivity

**Implementation Path**:

1. Design PostgreSQL schema with scaling in mind
2. Use JSONB for nested data (comments, metadata)
3. Add proper indexes and query optimization
4. Monitor performance and plan sharding if needed
5. Re-evaluate after 100K users

**Decision Points**:

- At 100K users: Check performance metrics, decide on scaling strategy
- At 500K users: Validate scaling approach, consider read replicas
- If requirements change to heavily document-based: Re-evaluate MongoDB

**Reversibility**: Medium

- Can migrate PostgreSQL → MongoDB (tools exist, takes weeks)
- Can add MongoDB alongside for specific use cases
- Can use read replicas / Citus for PostgreSQL scaling

## Next Steps

1. [ ] Validate with team: Everyone agree on PostgreSQL?
2. [ ] Design initial schema focusing on scalability
3. [ ] Set up monitoring and performance baselines
4. [ ] Document decision for future team members
5. [ ] Proceed with implementation

Questions or shall we move forward with PostgreSQL?
```

## Quality Checklist

Before finalizing analysis:

- [ ] Problem is clearly understood
- [ ] Multiple perspectives considered
- [ ] Assumptions surfaced and validated
- [ ] At least 3 options explored
- [ ] Tradeoffs made explicit
- [ ] Risks identified and assessed
- [ ] Recommendation is clear and justified
- [ ] Next steps are actionable
- [ ] Decision is reversible or irreversibility noted

## Success Criteria

Good deep analysis:

- Reveals insights not obvious at start
- Surfaces hidden assumptions
- Considers multiple perspectives
- Makes tradeoffs explicit
- Provides clear recommendation
- Shows reasoning transparently
- Prevents costly mistakes
- Builds shared understanding

## Related Capabilities

- **Slash Command**: `/ultrathink` for even deeper analysis
- **Slash Command**: `/consensus` for multi-stakeholder alignment
- **Slash Command**: `/debate` for exploring opposing viewpoints
- **Skill**: "Architecting Solutions" for post-analysis design
- **Skill**: "Evaluating Tradeoffs" for decision-focused analysis

---

Remember: The goal is clarity and confidence, not endless analysis. Analyze deeply enough to make good decisions, then commit and act.
