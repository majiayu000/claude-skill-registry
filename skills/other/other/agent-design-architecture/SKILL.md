---
name: Agent Design Architecture
description: Design effective AI agent systems with clear architecture, capability planning, and tool integration. Use when building agent systems, designing agent workflows, planning tool ecosystems, defining agent roles and boundaries, or architecting multi-agent systems. Covers agent patterns, agentic loops, capability design, and system composition.
---

# Agent Design Architecture

Effective agent systems require thoughtful architecture that balances capability, safety, and maintainability. This skill guides designing agent systems from first principles.

## Agent Fundamentals

### What Makes an Effective Agent

An agent is a system that:
- **Perceives** its environment (through tools, data, human input)
- **Reasons** about goals and available actions
- **Acts** to change state toward objectives
- **Reflects** on outcomes to improve future actions
- **Communicates** intent and reasoning to humans

**Key distinction from simple chatbots**:
- Agents have *goals* beyond responding conversationally
- Agents *persist* across multiple interactions
- Agents *compose* multiple tools into workflows
- Agents *reason* about outcomes and adapt
- Agents operate with *bounded autonomy* (within constraints)

## Agent Architecture Patterns

### Pattern 1: Tool-Using Agent (Simplest)
```
User Request → Model Reasoning → Tool Selection → Tool Execution → Result → Response
```

**When to use**: Single-step tasks, straightforward tool selection
**Example**: "Find the latest sales data and summarize"
**Complexity**: Low | **Autonomy**: Low

**Design considerations**:
- Clear tool descriptions for LLM selection
- Explicit constraints on tool combinations
- Fallback handling for tool failures

---

### Pattern 2: Agentic Loop (Iterative)
```
Goal → Reasoning → Action Selection → Execute → Observe → Success?
                      ↑_____No_________↓
                    Reflect & Replan
```

**When to use**: Complex, multi-step tasks; planning required
**Example**: "Analyze customer complaints, identify patterns, propose solutions"
**Complexity**: Medium | **Autonomy**: Medium

**Design considerations**:
- Loop termination criteria (max iterations, goal achieved, resource exhausted)
- State tracking between iterations
- Reflection mechanism (what worked, what didn't)
- Tool selection constraints per iteration

---

### Pattern 3: Planning Agent (Explicit Reasoning)
```
Goal → Decompose → Create Plan → Execute Step → Verify → Adapt Plan
```

**When to use**: Complex goals requiring explicit planning; stakeholder visibility
**Example**: "Develop a product roadmap balancing technical debt and features"
**Complexity**: High | **Autonomy**: High

**Design considerations**:
- Plan representation (tree, graph, narrative)
- Verification steps between plan and execution
- Adaptation triggers (deviation thresholds)
- Human-in-the-loop review points

---

### Pattern 4: Hierarchical Agent (Specialization)
```
Coordinator Agent
    ├─ Research Agent (gathers info)
    ├─ Analysis Agent (processes data)
    └─ Synthesis Agent (creates output)
```

**When to use**: Complex domains requiring specialized sub-agents
**Example**: "Write a comprehensive research report"
**Complexity**: High | **Autonomy**: High

**Design considerations**:
- Clear handoff protocols between agents
- Shared context/state management
- Coordinator error recovery
- Sub-agent autonomy boundaries

---

### Pattern 5: Reactive Agent (Event-driven)
```
Event → Trigger Rules → Immediate Action → Update State
```

**When to use**: Real-time monitoring, rapid response
**Example**: "Monitor system alerts and escalate critical issues"
**Complexity**: Medium | **Autonomy**: Medium

**Design considerations**:
- Event classification and prioritization
- Response action mapping to events
- State consistency across async operations
- Throttling/rate limiting

---

### Pattern 6: Multi-Agent Ecosystem
```
        User Interface
            ↓
    Orchestration Layer
    ↙   ↓   ↓   ↓   ↘
Agent  Agent Agent Agent Agent
(specialized roles)
```

**When to use**: Organization-scale automation, diverse domains
**Example**: "Coordinate content creation across marketing, sales, support"
**Complexity**: Very High | **Autonomy**: High

**Design considerations**:
- Agent discovery and registry
- Message passing/communication protocol
- Conflict resolution between agents
- Global state consistency
- Observability across agents

## Agent Capability Design

### Step 1: Define Agent Boundaries
Clarify what the agent owns vs. what it doesn't:

```
AGENT OWNS:
✓ Reasoning and planning for goals
✓ Tool orchestration within domain
✓ Data gathering and synthesis
✓ Communicating confidence/uncertainty

HUMAN OWNS:
✓ Final decisions on high-stakes items
✓ Setting priorities and constraints
✓ Defining success criteria
✓ Judging value of outcomes

SHARED RESPONSIBILITY:
~ Monitoring for issues
~ Learning from outcomes
~ Ethical judgment calls
```

### Step 2: Design Tool Set
Tools are how agents affect the world. Thoughtful tool design is critical.

**Tool Selection Criteria**:
- **Necessity**: Does agent actually need this to succeed?
- **Sufficiency**: Combined, do tools solve the problem class?
- **Safety**: What's the worst that could happen? Is it contained?
- **Clarity**: Can the agent understand when to use it?
- **Feedback**: Does tool provide actionable feedback?

**Tool Description Template**:
```
Name: [Clear, unambiguous]
Purpose: [What problem does this solve?]
When to use: [Specific situations]
When NOT to use: [Common mistakes]
Required inputs: [Parameters, formats, constraints]
Output: [Structure, semantics, error cases]
Limitations: [What it doesn't do]
Side effects: [What else happens when called?]
Cost: [Latency, computational, financial]
```

**Example: Good Tool Description**
```
Name: CheckInventoryLevel
Purpose: Query current stock levels for a specific product
When to use: Before committing to delivery dates or promotions
When NOT to use: Don't use to predict future demand (use ForecastDemand instead)
Required inputs: product_id (string), warehouse_id (string, optional)
Output: {
  available_units: int,
  reserved_units: int,
  low_stock_threshold: int,
  last_updated: timestamp,
  confidence: "high" | "medium" | "low"
}
Limitations: Data updates every 15 minutes; historical data not available
Side effects: Increments query count (throttled at 100/min)
Cost: ~50ms latency
```

### Step 3: Define Success & Failure
Explicit criteria prevent agent drift:

**Success criteria** (agent should optimize for):
- What does good output look like?
- What metrics matter? (speed, accuracy, coverage, cost)
- What trade-offs are acceptable?
- When is "good enough" sufficient?

**Failure modes** (agent should avoid):
- Hallucinating facts not in sources
- Recommending actions outside domain
- Persisting with failing strategies
- Exceeding resource/time budgets
- Violating stated constraints

**Example**:
```
GOAL: Write product descriptions for 100 SKUs

SUCCESS LOOKS LIKE:
✓ Descriptions are 50-100 words
✓ Highlight unique features accurately
✓ Reading level is accessible (8th grade)
✓ Include relevant keywords naturally
✓ Completed in <2 hours

AVOID:
✗ Making up product features
✗ Copying competitor descriptions
✗ Generic templated language
✗ Inaccurate specifications
✗ Exceeding 2-hour time budget
```

### Step 4: Set Autonomy Boundaries
Define what agent can decide vs. what requires human approval:

**Autonomy Levels**:

1. **Informed** - Agent gathers info, human decides
   - "Research competitors; I'll decide pricing"

2. **Recommended** - Agent proposes, human approves
   - "Recommend marketing budget allocation; I'll approve"

3. **Delegated** - Agent decides within guardrails
   - "Respond to customer emails; escalate complaints"

4. **Autonomous** - Agent decides freely within domain
   - "Optimize code formatting"

**Decision tree for setting boundaries**:
```
Is decision REVERSIBLE?
  → Yes → Is impact LOW-STAKES?
          → Yes → AUTONOMOUS (agent decides freely)
          → No  → DELEGATED (with monitoring)
  → No  → Is decision TIME-SENSITIVE?
          → Yes → DELEGATED (with human review)
          → No  → RECOMMENDED (with human approval)
```

## Tool Ecosystem Design

### Tool Composition Patterns

**Atomic Tools** (Single responsibility):
- `GetCustomerHistory()` - retrieve only
- `UpdateOrderStatus()` - modify only
- `ValidateEmailAddress()` - verify only

**Composite Tools** (Common combinations):
- `CreateAndAssignTicket()` - create ticket + assign to agent + notify
- `AnalyzeSentimentAndRoute()` - analyze + determine category + route

**Rule of thumb**: Start atomic, compose at the agent logic level, create composites only for frequent, safe combinations.

### Tool Safety & Constraints

**Input Validation**:
```
Tool receives: customer_id
Validate:
  ✓ Is non-null string
  ✓ Matches expected format (UUID)
  ✓ Customer exists in system
  ✓ Current user authorized to access
  → Only then: Execute
```

**Output Safety**:
```
Tool computes: credit_score
Before returning to agent:
  ✓ Is score within expected range?
  ✓ Is score based on fresh data?
  ✓ Should sensitive fields be redacted?
  → Return with confidence/caveat info
```

**Rate Limiting & Quotas**:
```
Tool: SendEmail
Limits:
  - 10 emails per agent per minute
  - 100 emails per day total
  - No sending outside business hours
  - Escalate if limits approached
```

## Agent Workflow Design

### Step 1: Map the Happy Path
What's the ideal flow if everything works?

```
User: "Analyze my Q3 sales and recommend changes"

1. Agent: Gather sales data for Q3
2. Agent: Segment by product/region/customer
3. Agent: Calculate trends (YoY, MoM)
4. Agent: Identify top performers and underperformers
5. Agent: Research market context
6. Agent: Synthesize recommendations
7. Agent: Present findings with confidence levels
8. User: Review and decide
```

### Step 2: Anticipate Failure Points
Where could things go wrong?

```
FAILURE POINT: Sales data incomplete/corrupted
DETECTION: Verify data completeness before analysis
HANDLING: Report gaps, ask for manual data, skip analysis

FAILURE POINT: Market context misleading
DETECTION: Cross-reference multiple sources
HANDLING: Flag conflicting info, present both interpretations

FAILURE POINT: Recommendation outside feasibility
DETECTION: Run recommendation through feasibility checker
HANDLING: Adjust recommendation or escalate

FAILURE POINT: Analysis takes too long
DETECTION: Track elapsed time against budget
HANDLING: Report progress, offer partial results, ask to continue
```

### Step 3: Design Error Recovery
How does agent recover from failures?

**Retry Logic**:
- Transient errors (network): Retry with backoff (3x, then escalate)
- Data errors (missing): Use fallback data or skip step
- Logic errors (hallucination): Re-prompt with constraints

**Escalation**:
- Agent tries recovery steps
- If still failing: Escalate to human with context
- Human provides guidance or exception handling

**State Management**:
- Save progress between steps
- Don't repeat work already done
- Resume from last checkpoint

## Multi-Agent Coordination

### Communication Patterns

**Sequential Handoff** (Agent A → Agent B):
```
ResearchAgent gathers data
  → Passes to AnalysisAgent
    → Passes to WritingAgent
      → Returns result
```
**Best for**: Linear workflows
**Challenge**: One agent bottleneck blocks others

**Parallel Execution** (A & B & C run concurrently):
```
ResearchAgent-A gathers market data
ResearchAgent-B gathers competitor data
ResearchAgent-C gathers internal data
  → All results → AnalysisAgent (merges)
```
**Best for**: Gathering info from multiple sources
**Challenge**: Coordinating and merging results

**Broadcast** (Agent communicates to many):
```
CoordinatorAgent creates plan
  → Sends to all sub-agents
    → Each executes their part
      → Reports back progress
```
**Best for**: Orchestrating specialization
**Challenge**: Managing dependencies and failures

### State Management

**Shared State** (All agents access common state):
```
{
  "goal": "..."
  "status": "in_progress",
  "findings": [...],
  "blockers": [...],
  "decisions_needed": [...]
}
```
**Advantage**: Agents always see current picture
**Risk**: Conflicts if multiple agents modify

**Passed State** (State passes between agents):
```
Agent-A → outputs with state → Agent-B reads and updates → Agent-C reads updated state
```
**Advantage**: Clear causality
**Risk**: Out-of-sync if agents modify independently

**Event Logging** (Append-only record):
```
Events:
- Agent-A started
- Agent-A found X
- Agent-B started
- Agent-B found Y (contradicts X)
- Issue flagged: contradiction
```
**Advantage**: Auditability, no conflicts
**Risk**: Complexity in reconstructing state

## Practical Design Checklist

When designing an agent system, verify:

- [ ] **Clear boundaries**: What does agent own vs. not own?
- [ ] **Explicit goals**: Success criteria and metrics defined
- [ ] **Tool sufficiency**: Do tools enable goal achievement?
- [ ] **Tool clarity**: Descriptions unambiguous to LLM?
- [ ] **Safety constraints**: Guardrails for risky actions?
- [ ] **Autonomy level**: Appropriate for decision type?
- [ ] **Happy path**: Ideal flow documented?
- [ ] **Failure modes**: Expected failures anticipated?
- [ ] **Recovery**: How does agent recover from errors?
- [ ] **Escalation**: When does human get involved?
- [ ] **Observability**: Can humans understand agent reasoning?
- [ ] **Resource budgets**: Time, cost, API call limits?
- [ ] **Iteration limit**: Max steps before asking human?
- [ ] **State management**: How is progress tracked?
- [ ] **Testing**: How will you validate agent behavior?

## Common Anti-Patterns to Avoid

| **Anti-Pattern** | **Problem** | **Solution** |
|------------------|-----------|------------|
| **Too much autonomy** | Agent makes poor decisions without guidance | Define clear boundaries and constraints |
| **Unclear tool descriptions** | Agent misuses tools, makes mistakes | Invest in precise tool documentation |
| **No iteration limit** | Agent loops forever, wastes resources | Set max iterations + explicit exit criteria |
| **Silent failures** | Agent appears successful but isn't | Return confidence scores, flag assumptions |
| **No state tracking** | Can't debug or resume | Log decisions and reasoning |
| **Unrealistic tool set** | Agent "hallucinates" because tools insufficient | Audit tool sufficiency for goal class |
| **Single point of failure** | One tool breaks, whole workflow fails | Provide tool alternatives/fallbacks |
| **Vague success criteria** | Agent doesn't know what "good" looks like | Define explicit metrics and examples |

## Resources & Next Steps

- Evaluate agent using: Agent Reasoning & Decision-Making skill
- Ensure reliability with: Agent Reliability & Safety skill
- Optimize human collaboration: Agent Human-AI Collaboration skill
- Measure effectiveness: Agent Evaluation & Monitoring skill
