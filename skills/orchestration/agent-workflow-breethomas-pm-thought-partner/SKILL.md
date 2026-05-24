---
name: agent-workflow
description: Expert system for designing and architecting AI agent workflows based on proven Meta methodologies. Use when users need to build AI agents, create agent workflows, solve problems using agentic systems, integrate multiple tools into agent architectures, or need guidance on agent design patterns. Helps translate business problems into structured agent solutions with clear scope, tool integration, and multi-layer architecture planning.
---

# Agent Workflow Designer

## Overview

This skill guides the design and architecture of AI agent workflows using proven methodologies. When a user presents a problem, this skill helps structure an agent-based solution following the 9-step building process and 8-layer architecture framework validated at Meta.

## Workflow Decision Tree

When a user shares a problem or requests agent design help:

1. **Assess the problem scope**
   - Is the problem clearly defined? → Proceed to Problem Analysis
   - Is the problem vague? → Ask clarifying questions about desired outcomes and constraints

2. **Determine architecture complexity**
   - Simple task (single action)? → Single agent with basic tools
   - Complex task (multiple sub-tasks)? → Consider multi-agent orchestration
   - Integration task (connecting systems)? → Focus on Layer 4 (Tooling) design

3. **Follow the appropriate workflow**
   - **New agent from scratch** → Apply 9-Step Building Process
   - **Existing agent improvement** → Focus on specific layers needing enhancement
   - **Tool integration problem** → Apply MCP and tooling patterns

## 9-Step Agent Building Process

Use this sequential workflow when designing a new agent from scratch:

### Step 1: Define Purpose and Scope

**Key principle:** Start with job-to-be-done, not technology.

Ask the user:
- What specific outcome does the end user need?
- What are the constraints (budget, time, resources)?
- What's the success metric?

**Bad scope example:**
"An AI assistant for customer service"

**Good scope example:**
"An agent that takes customer complaints, pulls order history from Shopify API, and drafts refund approvals for orders under $200"

**Decision point:** Narrow scope = better performance. Resist building Swiss Army knives.

### Step 2: Structure Inputs and Outputs

Treat the agent as a function with structured interfaces:

**Inputs:**
- Use JSON schemas or Pydantic models, not free text
- Define required vs. optional fields
- Specify data types and validation rules

**Outputs:**
- Return data objects, not prose
- Define clear error states
- Include confidence scores when relevant

**Example structure:**
```json
Input: {
  "complaint_text": "string",
  "customer_id": "string",
  "order_id": "string (optional)"
}

Output: {
  "action": "approve_refund | escalate | request_info",
  "refund_amount": "number",
  "reasoning": "string",
  "confidence": "number"
}
```

### Step 3: Write System Instructions

**Critical:** Spend 80% of design time here.

Include in system prompt:
- **Role definition:** "You are a sales qualification specialist..."
- **Behavioral guidelines:** "Always ask for budget before proposing solutions"
- **Output format requirements:** Specify JSON structure, word limits, tone
- **Edge case handling:** What to do when data is missing or ambiguous

**Testing strategy:** A great system prompt can make GPT-3.5 outperform poorly prompted GPT-4.

### Step 4: Enable Reasoning and External Actions

**ReAct Framework Pattern:**
1. **Reason:** Analyze the current state and decide next action
2. **Act:** Call an API, use a tool, or make a decision
3. **Observe:** Review the result and determine if goal is achieved

**Start simple:**
- Begin with if/then logic before complex reasoning chains
- Add tools incrementally (don't overwhelm with 50 tools at once)
- Test each tool integration independently

**Common tools to integrate:**
- Calculators for math operations
- Web browsers for research
- Database queries for data retrieval
- API calls to external systems

### Step 5: Orchestrate Multiple Agents (When Needed)

**When to use multi-agent architecture:**
- Task has clearly separable sub-tasks
- Different sub-tasks require different expertise
- Parallel processing would improve speed

**When NOT to use multi-agent:**
- Simple linear workflows
- Tasks that require continuous context
- When handoff complexity exceeds benefit

**Common 4-agent pattern:**
1. **Research Agent:** Gathers information from sources
2. **Analysis Agent:** Processes and synthesizes data
3. **Writing Agent:** Creates structured outputs
4. **QA Agent:** Reviews quality and accuracy

**Keep handoffs simple:** Complex orchestration = complex failures.

### Step 6: Implement Memory and Context

Three types of memory to consider:

**Conversation history:**
- What happened this session
- Recent user interactions
- Current task state

**User context:**
- User preferences and settings
- Past interaction patterns
- Historical decisions

**Knowledge retrieval:**
- Relevant information from knowledge base
- Similar past cases
- Domain-specific context

**Implementation guidance:**
- Start with simple conversation buffers
- Add vector databases only when needing semantic search across large datasets
- Consider memory retrieval latency in architecture

### Step 7: Add Multimedia Capabilities

Modern agents should handle:
- Voice input/output for accessibility
- Image understanding for visual tasks
- Document processing (PDF, DOCX, spreadsheets)

**Strategic approach:** Add capabilities based on actual user needs, not "nice-to-haves."

### Step 8: Format and Deliver Results

**Output is your product's UX.** Design outputs for:

**Human consumption:**
- Clear formatting and structure
- Scannable with headers and bullets
- Professional appearance

**System consumption:**
- Valid JSON/XML
- Consistent field names
- Error codes for handling

**Quality standard:** Great agent outputs look like a human created them.

### Step 9: Build Interface or API

Delivery method options:
- Chat interface for conversational tasks
- API endpoints for system integration
- Integration with existing tools (Slack, email, CRM)

**Best practice:** The best agents feel invisible—they just make things happen.

## 8-Layer Architecture Framework

When analyzing agent architecture needs, consider which layers require attention:

### Layer 1: Infrastructure
**Foundation:** Cloud, databases, APIs, compute resources

**Key considerations:**
- GPU/TPU requirements for inference
- Data storage and retrieval speed
- Load balancing for scale
- Monitoring and observability

**Common mistake:** Underestimating compute needs—agents make more API calls than traditional apps.

### Layer 2: Agent Internet
**Operating system for agents:** Identity, state management, inter-agent communication

**Current state:** Mostly custom-built, but platforms like LangChain and CrewAI are emerging.

### Layer 3: Protocol
**Standards for interoperability:** MCP (Model Context Protocol) is becoming the standard

**Key principle:** Bet on open standards, not proprietary solutions. MCP allows any tool to work with any agent.

### Layer 4: Tooling Enrichment
**Agent superpowers:** RAG systems, function calling, external integrations

**Quality over quantity:** 5 rock-solid tools > 50 flaky integrations

**Tool categories:**
- Data retrieval (databases, APIs)
- Computation (calculators, processors)
- Communication (email, messaging)
- Content creation (documents, reports)

### Layer 5: Cognition Reasoning
**The brain:** Planning, decision-making, error handling

**Critical elements:**
- Guardrails to prevent hallucinations
- Error recovery strategies
- Confidence scoring
- Graceful degradation

**User forgiveness:** Users forgive agents that fail gracefully, not ones that spiral into nonsense.

### Layer 6: Memory Personalization
**Human touch:** Personal context, preferences, conversation history

**Start simple:** Store user preferences and conversation context before building complex personalization.

### Layer 7: Application
**User-facing products:** The actual agent functionality users interact with

**Focus strategy:** Nail one use case before expanding to others.

### Layer 8: Ops Governance
**Risk management:** Monitoring, cost control, privacy, oversight

**Build from day one:** Retrofitting governance is expensive and painful.

**Key components:**
- Cost tracking per agent action
- Privacy enforcement and data handling
- Human-in-the-loop for critical decisions
- Audit logs and compliance

## Problem-to-Solution Workflow

When a user presents a problem:

**Step 1: Clarify the problem**
- What's the current manual process?
- What's the desired outcome?
- What are the constraints (time, cost, technical)?
- What data sources are available?

**Step 2: Assess agent appropriateness**
Not every problem needs an agent. Consider:
- Is the task repetitive and rule-based?
- Does it require decision-making with context?
- Would automation provide significant value?
- Is the problem scope clear and bounded?

**Step 3: Map to architecture**
Using the 8 layers, identify which need focus:
- Simple task → Focus on Layers 4, 5, 7 (tools, reasoning, application)
- Complex integration → Add Layer 3 (protocol) emphasis
- Scalability concern → Prioritize Layers 1, 8 (infrastructure, ops)

**Step 4: Design workflow**
Apply the 9-step building process, calling out:
- Critical decision points
- Tool integration requirements
- Multi-agent needs (if any)
- Memory and context strategy

**Step 5: Identify implementation path**
Based on user's role and resources:
- **For PMs:** High-level architecture and tool selection
- **For engineers:** Detailed technical implementation with code patterns
- **For product teams:** Full stack from requirements to monitoring

## Tool Integration Patterns

### MCP (Model Context Protocol) Integration

When tools support MCP:
1. Agent discovers available tools
2. Agent calls tools using standardized interface
3. Tool returns structured response
4. Agent processes and continues workflow

**Advantage:** Write once, use with any agent.

### Custom API Integration

When building custom integrations:
1. Define clear API contract (inputs/outputs)
2. Implement error handling and retries
3. Add rate limiting and caching
4. Monitor usage and costs
5. Document for agent consumption

### Common Integration Scenarios

**CRM Integration (Salesforce, HubSpot):**
- Read customer data
- Create/update records
- Search across objects
- Trigger workflows

**Communication Tools (Slack, Email):**
- Send messages/notifications
- Read incoming requests
- Monitor channels
- Respond to mentions

**Data Sources (Databases, APIs):**
- Query structured data
- Retrieve documents
- Search knowledge bases
- Aggregate information

## Decision Framework: Single vs. Multi-Agent

### Use Single Agent When:
- Task is linear and sequential
- Context must be maintained throughout
- Decision-making is unified
- Complexity of orchestration > benefit

### Use Multi-Agent When:
- Clear task separation exists
- Sub-tasks need different expertise
- Parallel processing improves performance
- Quality benefits from specialization

**Example - Customer Support:**

**Single agent sufficient for:**
"Take customer complaint, pull order history, draft refund approval"

**Multi-agent beneficial for:**
"Monitor social media, categorize issues, research solutions, generate responses, escalate critical cases, track resolution"

## Common Pitfalls and Solutions

### Pitfall 1: Scope Creep
**Problem:** Trying to build a general-purpose assistant
**Solution:** Define narrow, specific job-to-be-done with clear success metrics

### Pitfall 2: Tool Overload
**Problem:** Giving agent 50+ tools upfront
**Solution:** Start with 5 essential tools, add incrementally based on actual needs

### Pitfall 3: Skipping System Prompt
**Problem:** Generic or minimal instructions
**Solution:** Invest 80% of time crafting detailed system prompt with examples and edge cases

### Pitfall 4: No Error Handling
**Problem:** Agent breaks on unexpected inputs
**Solution:** Design graceful degradation, clear error states, and fallback behaviors

### Pitfall 5: Ignoring Costs
**Problem:** Runaway API costs from inefficient agent design
**Solution:** Build cost monitoring from day one, implement caching, optimize prompt length

### Pitfall 6: Over-Engineering Architecture
**Problem:** Building all 8 layers simultaneously
**Solution:** Start with Layers 4, 5, 7 (tools, reasoning, application), add others as needed

## Output Format

When providing agent workflow solutions, structure the response as:

1. **Problem Restatement:** Confirm understanding of the user's need
2. **Agent Architecture Recommendation:** Single vs. multi-agent, with rationale
3. **Step-by-Step Workflow:** Apply relevant steps from the 9-step process
4. **Tool Integration Plan:** Specific tools needed and integration approach
5. **Layer Analysis:** Which of the 8 layers need focus and why
6. **Implementation Guidance:** Prioritized next steps based on user's role
7. **Success Metrics:** How to measure if the agent is working

## Agent Taxonomy Quick Reference

When users ask about existing tools:

**Category 1: Consumer Agents (Built-In)**
- Examples: ChatGPT Agent, Claude, Gemini, Grok
- Best for: Quick tasks, research, content creation
- User type: Everyone, especially PMs

**Category 2: No-Code Builders**
- Examples: Zapier Central, n8n, Make
- Best for: Workflow automation without coding
- User type: PMs, operations teams

**Category 3: Developer-First Platforms**
- Examples: LangChain, CrewAI, AutoGen, Swarm
- Best for: Custom agent features in products
- User type: Engineering teams

**Category 4: Specialized Agent Apps**
- Examples: Cursor (coding), Perplexity (research), Notion AI (writing)
- Best for: Specific job-to-be-done with deep specialization
- User type: Domain-specific professionals
