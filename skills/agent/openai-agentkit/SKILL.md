---
name: OpenAI AgentKit Expert
description: Build production-ready multi-agent systems using OpenAI AgentKit and Agents SDK with best practices for agent orchestration, handoffs, and routines
version: 1.1.0
last_updated: 2026-01-06
external_version: "OpenAI Agents SDK 0.6.4, GPT-5.2"
---

# OpenAI AgentKit Expert Skill

## Purpose
This skill provides comprehensive guidance on building production-ready multi-agent systems using OpenAI's AgentKit platform and Agents SDK, following 2026 best practices.

## Platform Overview

### OpenAI AgentKit (2026)
Complete platform for building, deploying, and optimizing agents with enterprise-grade tooling.

**Core Components:**
- **Agent Builder** - Visual canvas for creating and versioning multi-agent workflows
- **Connector Registry** - Central management for data and tool connections
- **ChatKit** - Embeddable customizable chat-based agent experiences
- **Evaluation Suite** - Datasets, trace grading, automated prompt optimization
- **Multi-Model Support** - Third-party model integration capabilities

### Agents SDK (Production-Ready)
The Agents SDK is the production evolution of the experimental Swarm framework. **Use Agents SDK for all production work** - Swarm is educational only.

**Migration Note:** If you encounter legacy Swarm code, migrate to Agents SDK immediately.

## Core Concepts

### 1. Agents
An Agent encapsulates:
- A set of instructions (system prompt)
- A set of functions/tools
- The capability to hand off execution to another Agent

**Design Principle:** Agents should be **lightweight and specialized** rather than monolithic and general-purpose.

### 2. Routines
A **routine** is a sequence of actions an agent can perform:
- Natural language instructions (via system prompt)
- Available tools needed to execute
- Context and state management
- Success criteria

**Think of it as:** A mini-workflow that an agent owns and executes autonomously.

### 3. Handoffs
**Handoffs** enable agent-to-agent transitions in execution flow.

**Key Pattern:** When an agent encounters a task outside its specialization, it hands off to a more appropriate agent.

**Example:**
```python
# Triage agent determines which specialist to use
if task.type == "refund":
    handoff_to(refund_agent)
elif task.type == "sales":
    handoff_to(sales_agent)
```

## Architectural Patterns

### Pattern 1: Triage Pattern
**Use Case:** Routing requests to specialized sub-agents

**Structure:**
```
User Request → Triage Agent → [Determines Category] → Specialist Agent
```

**Example Implementation:**
```python
# Triage agent with handoff capabilities
triage_agent = Agent(
    name="Customer Service Triage",
    instructions="Analyze customer requests and route to appropriate specialist",
    functions=[analyze_request],
    handoffs=[refund_agent, sales_agent, support_agent]
)
```

**When to Use:**
- Multiple distinct capability domains
- Clear categorization logic
- Different agents need different tools/context

### Pattern 2: Sequential Orchestration
**Use Case:** Multi-step workflows where each step has a specialist

**Structure:**
```
Step 1 Agent → [Complete] → Handoff → Step 2 Agent → ... → Final Agent
```

**Example:**
```python
# Research → Analysis → Report Generation pipeline
research_agent → analysis_agent → report_agent
```

**When to Use:**
- Clear sequential dependencies
- Each step requires specialized expertise
- Output of one step feeds the next

### Pattern 3: Parallel Decomposition
**Use Case:** Breaking complex tasks into parallel subtasks

**Structure:**
```
Coordinator Agent
    ↓
    ├─→ Subtask Agent 1
    ├─→ Subtask Agent 2
    └─→ Subtask Agent 3
    ↓
Synthesis Agent (combines results)
```

**When to Use:**
- Independent subtasks can run concurrently
- Need to aggregate multiple perspectives
- Performance optimization through parallelization

## Best Practices

### Agent Design

**DO:**
✅ Keep agents focused on single responsibilities
✅ Provide clear, specific instructions in system prompts
✅ Define explicit handoff conditions
✅ Use descriptive agent names (helps with debugging)
✅ Test agents in isolation before integration

**DON'T:**
❌ Create monolithic "do-everything" agents
❌ Allow agents to communicate directly (use handoffs)
❌ Over-engineer with too many specialized agents
❌ Ignore error handling in handoffs
❌ Skip agent boundary testing

### Routine Design

**Effective Routines:**
- Have clear entry and exit conditions
- Include error handling paths
- Specify required context/state
- Document expected inputs/outputs
- Define success metrics

**Example:**
```python
routine = {
    "name": "Process Refund",
    "entry": "User requests refund",
    "steps": [
        "Verify order exists",
        "Check refund eligibility",
        "Calculate refund amount",
        "Process payment reversal",
        "Send confirmation"
    ],
    "exit": "Refund confirmed or rejection reason provided",
    "error_handling": "Escalate to human agent if verification fails"
}
```

### Handoff Design

**Critical Elements:**
- **Clear Trigger Conditions** - When should handoff occur?
- **Context Passing** - What information transfers?
- **Return Path** - Can control return to originating agent?
- **Failure Handling** - What if target agent unavailable?

**Example:**
```python
def handoff_condition(state):
    """Determine if handoff needed"""
    if state.requires_specialized_knowledge:
        return specialist_agent
    if state.exceeds_authority_level:
        return supervisor_agent
    return None  # Continue with current agent
```

## Performance Optimization

### Minimize LLM Calls
**Principle:** Frameworks that limit LLM involvement and rely on predefined or direct execution flows operate more efficiently.

**Strategies:**
- Use deterministic logic where possible
- Cache common responses
- Batch similar requests
- Pre-compute decision trees
- Use smaller models for simple tasks

### Efficient Tool Use
**Principle:** Give agents only the tools they need for their specialty.

**Pattern:**
```python
# Specialized agents get targeted toolsets
refund_agent.tools = [verify_order, calculate_refund, process_payment]
sales_agent.tools = [check_inventory, create_quote, process_order]
# NOT: both agents get all 6 tools
```

### Latency Reduction
- Prefer single-agent solutions when possible
- Use async operations for I/O-bound tasks
- Implement request coalescing
- Monitor and optimize hot paths

## Common Anti-Patterns

### 1. Over-Decomposition
**Problem:** Too many agents for simple tasks creates overhead

**Solution:** Start simple, add agents only when complexity demands it

### 2. Circular Handoffs
**Problem:** Agent A → Agent B → Agent A creates loops

**Solution:** Design clear hierarchy or state-based termination

### 3. Stateless Agents
**Problem:** Agents lose context across handoffs

**Solution:** Implement proper state management and context passing

### 4. Unclear Boundaries
**Problem:** Overlapping agent responsibilities cause conflicts

**Solution:** Define explicit agent domains and decision criteria

## Evaluation & Testing

### Key Metrics

**Agent-Level:**
- Task completion rate
- Average response time
- Tool usage efficiency
- Handoff accuracy

**System-Level:**
- End-to-end success rate
- Total latency
- Cost per interaction
- User satisfaction scores

### Testing Strategy

**Unit Testing:**
```python
# Test individual agent behaviors
def test_refund_agent():
    result = refund_agent.process(valid_refund_request)
    assert result.status == "approved"
    assert result.amount > 0
```

**Integration Testing:**
```python
# Test agent handoffs
def test_triage_to_refund():
    initial_state = {"request": "I want a refund"}
    final_state = orchestrator.run(initial_state)
    assert final_state.handling_agent == "refund_agent"
    assert final_state.completed == True
```

**End-to-End Testing:**
```python
# Test full user journeys
def test_customer_journey():
    scenarios = load_test_scenarios()
    for scenario in scenarios:
        result = system.execute(scenario)
        assert result.meets_requirements()
```

## Production Deployment

### Monitoring
**Essential Observability:**
- Agent invocation traces
- Handoff decision logs
- Tool call success rates
- Error patterns and frequencies
- Latency distributions

**Tools:**
- AgentKit built-in evaluation suite
- Custom logging to centralized system
- Real-time alerting on failures
- Performance dashboards

### Security

**Agent Security:**
- Scope tools to minimum required permissions
- Validate all tool inputs
- Sanitize user inputs before agent processing
- Implement rate limiting per agent
- Audit trail for all agent actions

**Data Protection:**
- Never expose sensitive data in prompts unnecessarily
- Use secure credential management
- Encrypt state/context storage
- Implement PII detection and masking

### Scaling Strategies

**Horizontal Scaling:**
- Deploy agent instances across multiple servers
- Use load balancing for agent requests
- Implement agent pools for high-volume scenarios

**Vertical Optimization:**
- Profile and optimize slow agents
- Use caching strategically
- Batch similar requests
- Upgrade to more powerful models selectively

## Code Examples

### Basic Agent Structure
```python
from openai import OpenAI

client = OpenAI()

# Define specialized agent
support_agent = {
    "name": "Technical Support Agent",
    "model": "gpt-4o",
    "instructions": """You are a technical support specialist.
    Help users troubleshoot technical issues.
    If issue requires refund, hand off to refund agent.
    If issue is sales-related, hand off to sales agent.""",
    "tools": [
        {"type": "function", "function": troubleshooting_guide},
        {"type": "function", "function": escalate_to_human}
    ]
}
```

### Handoff Implementation
```python
def execute_agent_workflow(initial_request):
    current_agent = triage_agent
    context = {"request": initial_request, "history": []}

    while not is_complete(context):
        # Execute current agent
        response = client.chat.completions.create(
            model=current_agent.model,
            messages=build_messages(context, current_agent),
            tools=current_agent.tools
        )

        # Check for handoff
        next_agent = determine_handoff(response)
        if next_agent:
            context["history"].append({
                "from": current_agent.name,
                "to": next_agent.name
            })
            current_agent = next_agent
        else:
            context["result"] = response
            break

    return context
```

## Integration with Other Systems

### With Claude SDK
Use AgentKit for OpenAI-based workflows, Claude SDK for Anthropic-based workflows, and MCP to bridge data sources to both.

### With LangGraph
LangGraph provides more fine-grained control flow. Use AgentKit for simpler workflows, LangGraph for complex state machines.

### With MCP
AgentKit agents can consume MCP servers as tools, standardizing data source connections.

## Migration Guide

### From Swarm to Agents SDK

**Key Changes:**
1. Replace `swarm.run()` with Agents SDK orchestration
2. Update agent definitions to new schema
3. Migrate handoff logic to production patterns
4. Add proper error handling
5. Implement monitoring and observability

**Timeline:** Swarm is maintenance-only. Migrate all production code by Q2 2025.

## Decision Framework

**Use OpenAI AgentKit when:**
- Building on OpenAI models (GPT-4, etc.)
- Need visual agent builder for non-technical stakeholders
- Want integrated evaluation and monitoring
- Prefer managed platform over open-source frameworks

**Consider alternatives when:**
- Need model flexibility (use LangGraph)
- Require complex state machines (use LangGraph)
- Want full control over orchestration (use custom solution)
- Working with Anthropic models (use Claude SDK)

## Resources

**Official Documentation:**
- AgentKit Platform: https://platform.openai.com/docs/agents
- Agents SDK: https://github.com/openai/agents-sdk
- Best Practices: https://platform.openai.com/docs/guides/agents-best-practices

**Community:**
- OpenAI Developer Forum
- AgentKit Discord
- GitHub Discussions

## Final Principles

1. **Simplicity First** - Start with single agents, add complexity only when needed
2. **Specialization Over Generalization** - Focused agents perform better
3. **Explicit Handoffs** - Clear routing beats implicit behavior
4. **Production-Ready** - Use Agents SDK, not Swarm, for real applications
5. **Measure Everything** - Observability is critical for multi-agent systems

---

*This skill ensures you build robust, scalable, production-ready multi-agent systems using OpenAI's latest platform capabilities in 2025.*
