---
name: escalation-handler
description: Handles escalations and determines appropriate escalation paths. Use when issues arise that need escalation or when determining whether to escalate to user vs. handle internally. Analyzes issues, determines severity, and routes to appropriate resolution path.
---

# Escalation Handler Skill

## Instructions

1. Analyze the issue or situation
2. Determine issue type and severity
3. Assess if issue can be handled internally
4. Determine appropriate escalation path
5. Prepare escalation information
6. Route to appropriate handler
7. Track escalation resolution

## Escalation Decision Process

### Step 1: Analyze Issue
- Understand the issue
- Identify issue type
- Assess severity
- Note impact

### Step 2: Check Internal Resolution
- Can issue be resolved internally?
- Do we have authority to resolve?
- Are resources available?
- Is it a technical or strategic decision?

### Step 3: Determine Escalation Path
- **Internal**: Handle with manager authority
- **User**: Escalate to user for decision
- **Other Agent**: Route to specialized agent

### Step 4: Prepare Escalation
- Gather context
- Prepare clear explanation
- Suggest options if applicable
- Document issue

### Step 5: Execute Escalation
- Route to appropriate path
- Communicate clearly
- Track resolution

## Escalation Criteria

### Escalate to User When

**Strategic Decisions**
- Business priorities conflict
- Resource allocation decisions
- Project direction changes
- Budget or timeline decisions

**Ambiguous Requirements**
- Requirements unclear
- Conflicting requirements
- Missing critical information
- Need clarification

**High-Impact Decisions**
- Decisions affecting project success
- Decisions with significant consequences
- Decisions requiring business input
- Decisions outside technical scope

**Resource Constraints**
- Insufficient resources
- Need additional resources
- Resource conflicts
- Budget constraints

**Quality Concerns**
- Quality issues requiring user attention
- Standards not being met
- Significant quality problems

### Handle Internally When

**Technical Decisions**
- Purely technical choices
- Implementation approaches
- Technology selections (within scope)
- Code structure decisions

**Process Issues**
- Workflow problems
- Agent coordination issues
- Process improvements
- Internal optimizations

**Agent Conflicts**
- Disagreements between agents
- Approach conflicts
- Can be resolved with manager authority

**Resource Reallocation**
- Can reallocate existing resources
- Workload balancing
- Agent assignment changes

## Escalation Types

### Type 1: Strategic Escalation
**When**: Business or strategic decisions needed
**Path**: User
**Example**: "Should we prioritize feature A or feature B?"

### Type 2: Clarification Escalation
**When**: Requirements unclear
**Path**: User
**Example**: "The specification doesn't specify authentication method. Should we use OAuth or JWT?"

### Type 3: Resource Escalation
**When**: Resource constraints
**Path**: User (if needs approval) or Internal (if can reallocate)
**Example**: "We need 3 more agents for this project. Should we hire them?"

### Type 4: Conflict Escalation
**When**: Agent conflicts
**Path**: Internal (manager resolves) or User (if strategic)
**Example**: "Two agents recommend different approaches. Which should we use?"

### Type 5: Quality Escalation
**When**: Quality issues
**Path**: User (if significant) or Internal (if can fix)
**Example**: "Code quality is below standards. Should we refactor or proceed?"

## Escalation Output Format

```markdown
## Escalation Decision

### Issue
[Description of issue]

### Issue Type
[Strategic / Clarification / Resource / Conflict / Quality / Other]

### Severity
[Critical / High / Medium / Low]

### Impact
[What is impacted by this issue]

### Analysis
[Analysis of issue and options]

### Recommendation
**Escalate to**: [User / Internal / Other Agent]
**Reason**: [Why this escalation path]

### Escalation Information
[Information to include in escalation]

### Suggested Options
[Options for user to consider, if applicable]
```

## Examples

### Example 1: Strategic Escalation

**Input**: Two high-priority features conflict for resources

**Output**:
```markdown
## Escalation Decision

### Issue
Two high-priority features (User Authentication and Payment Integration) both require implementation-engineer resources, but we only have capacity for one at a time. Both are marked as P0 (Critical).

### Issue Type
Strategic

### Severity
High

### Impact
- One feature will be delayed
- May impact project timeline
- Affects product launch readiness

### Analysis
- User Authentication: Required for user access, blocks other user features
- Payment Integration: Required for revenue, blocks monetization
- Both are critical but serve different purposes
- Need business decision on which to prioritize

### Recommendation
**Escalate to**: User
**Reason**: This is a strategic business decision about feature priorities that requires business input.

### Escalation Information
Two critical features conflict for resources:
1. User Authentication - Required for user access
2. Payment Integration - Required for revenue

We can only implement one at a time with current resources. Which should be prioritized?

### Suggested Options
1. Prioritize User Authentication first (enables user features)
2. Prioritize Payment Integration first (enables revenue)
3. Hire additional implementation-engineer to work in parallel
4. Delay one feature to next phase
```

### Example 2: Internal Handling

**Input**: Two agents recommend different API design approaches

**Output**:
```markdown
## Escalation Decision

### Issue
implementation-engineer recommends REST API design, while infrastructure-engineer recommends GraphQL. Both approaches are valid, but we need to choose one.

### Issue Type
Conflict

### Severity
Medium

### Impact
- Affects API implementation approach
- May impact development timeline
- Affects future API evolution

### Analysis
- REST: Simpler, more standard, easier to implement
- GraphQL: More flexible, better for complex queries
- Both are technical decisions within scope
- Can be resolved with manager authority based on project needs

### Recommendation
**Escalate to**: Internal (Manager resolves)
**Reason**: This is a technical decision that can be resolved internally. Manager can evaluate project needs and make decision.

### Escalation Information
[For internal resolution]
Two agents recommend different API approaches:
- REST (implementation-engineer): Simpler, standard
- GraphQL (infrastructure-engineer): More flexible

**Decision**: Choose REST for simplicity and faster implementation, as project doesn't require complex querying yet. Can migrate to GraphQL later if needed.

### Suggested Options
N/A - Resolved internally
```

### Example 3: Clarification Escalation

**Input**: Specification doesn't specify authentication method

**Output**:
```markdown
## Escalation Decision

### Issue
The specification requires user authentication but doesn't specify the authentication method (OAuth, JWT, Session-based, etc.). This affects implementation approach.

### Issue Type
Clarification

### Severity
High

### Impact
- Blocks authentication implementation
- Affects security architecture
- May require different infrastructure

### Analysis
- Multiple valid authentication approaches exist
- Choice affects implementation complexity
- May have security or integration implications
- Need clarification to proceed

### Recommendation
**Escalate to**: User
**Reason**: This is a requirement clarification needed to proceed with implementation.

### Escalation Information
The specification requires user authentication but doesn't specify the method. Which authentication method should we use?

### Suggested Options
1. OAuth 2.0 (Google, GitHub, etc.) - Easy for users, requires OAuth providers
2. JWT tokens - Standard, stateless, good for APIs
3. Session-based - Traditional, requires session storage
4. Other: [specify]
```

## Escalation Tracking

Track escalations:
- Issue description
- Escalation path
- Status (Pending, Resolved, Blocked)
- Resolution
- Follow-up actions

## Best Practices

- **Be Clear**: Clearly explain issue and why escalation is needed
- **Provide Context**: Include relevant background information
- **Suggest Options**: Offer options when possible
- **Be Timely**: Escalate promptly when needed
- **Track Resolution**: Follow up on escalations
- **Learn**: Use escalations to improve processes
