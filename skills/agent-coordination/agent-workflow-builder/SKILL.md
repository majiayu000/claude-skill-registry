---
name: Agent Workflow Builder
slug: agent-workflow-builder
description: Build multi-agent AI workflows with orchestration, tool use, and state management
category: ai-ml
complexity: advanced
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "build agent workflow"
  - "multi-agent system"
  - "AI agents"
  - "agent orchestration"
  - "agentic AI"
tags:
  - agents
  - orchestration
  - workflow
  - LLM
  - automation
---

# Agent Workflow Builder

The Agent Workflow Builder skill guides you through designing and implementing multi-agent AI systems that can plan, reason, use tools, and collaborate to accomplish complex tasks. Modern AI applications increasingly rely on agentic architectures where LLMs act as reasoning engines that orchestrate actions rather than just generate text.

This skill covers agent design patterns, tool integration, state management, error handling, and human-in-the-loop workflows. It helps you build robust agent systems that can handle real-world complexity while maintaining safety and controllability.

Whether you are building autonomous assistants, workflow automation, or complex reasoning systems, this skill ensures your agent architecture is well-designed and production-ready.

## Core Workflows

### Workflow 1: Design Agent Architecture
1. **Define** the agent's scope:
   - What tasks should it handle autonomously?
   - What requires human approval?
   - What is explicitly out of scope?
2. **Choose** architecture pattern:
   | Pattern | Description | Use When |
   |---------|-------------|----------|
   | Single Agent | One LLM with tools | Simple tasks, clear scope |
   | Router Agent | Classifies and delegates | Multiple distinct domains |
   | Sequential Chain | Agents in order | Pipeline processing |
   | Hierarchical | Manager + worker agents | Complex, decomposable tasks |
   | Collaborative | Peer agents discussing | Requires diverse expertise |
3. **Design** tool set:
   - What capabilities does the agent need?
   - How are tools defined and documented?
   - What are the safety boundaries?
4. **Plan** state management:
   - Conversation history
   - Task state and progress
   - External system state
5. **Document** architecture decisions

### Workflow 2: Implement Agent Loop
1. **Build** core agent loop:
   ```python
   class Agent:
       def __init__(self, llm, tools, system_prompt):
           self.llm = llm
           self.tools = {t.name: t for t in tools}
           self.system_prompt = system_prompt

       async def run(self, user_input, max_steps=10):
           messages = [
               {"role": "system", "content": self.system_prompt},
               {"role": "user", "content": user_input}
           ]

           for step in range(max_steps):
               response = await self.llm.chat(messages, tools=self.tools)

               if response.tool_calls:
                   # Execute tools
                   for call in response.tool_calls:
                       result = await self.execute_tool(call)
                       messages.append({"role": "tool", "content": result})
               else:
                   # Final response
                   return response.content

           raise MaxStepsExceeded()

       async def execute_tool(self, call):
           tool = self.tools[call.name]
           return await tool.execute(call.arguments)
   ```
2. **Implement** tools with clear interfaces
3. **Add** error handling and retries
4. **Include** logging and observability
5. **Test** with diverse scenarios

### Workflow 3: Build Multi-Agent System
1. **Define** agent roles:
   ```python
   agents = {
       "planner": Agent(
           llm=gpt4,
           tools=[search, create_task],
           system_prompt="You decompose complex tasks into steps..."
       ),
       "researcher": Agent(
           llm=claude,
           tools=[web_search, read_document],
           system_prompt="You gather and synthesize information..."
       ),
       "executor": Agent(
           llm=gpt4,
           tools=[code_interpreter, file_system],
           system_prompt="You execute tasks and produce outputs..."
       ),
       "reviewer": Agent(
           llm=claude,
           tools=[validate, provide_feedback],
           system_prompt="You review work for quality and correctness..."
       )
   }
   ```
2. **Implement** orchestration:
   - How do agents communicate?
   - Who decides what runs when?
   - How is work passed between agents?
3. **Manage** shared state:
   - Task board or work queue
   - Shared memory or context
   - Artifact storage
4. **Handle** failures gracefully
5. **Add** human checkpoints where needed

## Quick Reference

| Action | Command/Trigger |
|--------|-----------------|
| Design agent | "Design an agent for [task]" |
| Add tools | "What tools for [agent type]" |
| Build multi-agent | "Build multi-agent system for [goal]" |
| Handle errors | "Agent error handling patterns" |
| Add human-in-loop | "Add human approval to agent workflow" |
| Debug agent | "Debug agent workflow" |

## Best Practices

- **Start Simple**: Single agent with tools before multi-agent
  - Prove value with minimal complexity
  - Add agents only when necessary
  - Each agent should have clear, distinct responsibility

- **Design Tools Carefully**: Tools are the agent's hands
  - Clear, descriptive names and documentation
  - Well-defined input/output schemas
  - Proper error handling and messages
  - Idempotent operations where possible

- **Limit Agent Autonomy**: Constrain the blast radius
  - Define what agents cannot do
  - Require approval for high-impact actions
  - Implement spending/rate limits
  - Log all actions for audit

- **Manage State Explicitly**: Don't rely on LLM memory alone
  - Persist conversation and task state
  - Summarize long contexts to fit windows
  - Track what has been tried/completed

- **Fail Gracefully**: Agents will encounter errors
  - Clear error messages for the agent to reason about
  - Retry logic with backoff
  - Fallback strategies
  - Human escalation paths

- **Observe Everything**: Debugging agents is hard
  - Log all LLM calls and tool invocations
  - Track reasoning chains and decisions
  - Measure success rates by task type

## Advanced Techniques

### ReAct Pattern (Reasoning + Acting)
Structure agent thinking explicitly:
```python
REACT_PROMPT = """
You are an agent that solves tasks step by step.

For each step:
1. Thought: Analyze the current situation and decide what to do
2. Action: Choose a tool and provide arguments
3. Observation: Review the tool result

Continue until you can provide a final answer.

Available tools: {tool_descriptions}

Current task: {task}

Begin:
"""
```

### Planning Agent with Task Decomposition
Break complex tasks into manageable steps:
```python
class PlanningAgent:
    async def solve(self, task):
        # Step 1: Create plan
        plan = await self.create_plan(task)

        # Step 2: Execute each step
        results = []
        for step in plan.steps:
            result = await self.execute_step(step, context=results)
            results.append(result)

            # Replan if needed
            if result.status == "blocked":
                plan = await self.replan(task, results)

        # Step 3: Synthesize final output
        return await self.synthesize(task, results)
```

### Reflection and Self-Correction
Let agents review and improve their work:
```python
async def solve_with_reflection(self, task, max_attempts=3):
    for attempt in range(max_attempts):
        # Generate solution
        solution = await self.generate_solution(task)

        # Self-critique
        critique = await self.critique_solution(task, solution)

        if critique.is_acceptable:
            return solution

        # Improve based on critique
        task = f"{task}\n\nPrevious attempt issues: {critique.issues}"

    return solution  # Return best effort
```

### Human-in-the-Loop Checkpoints
Integrate human approval into workflows:
```python
class HumanApprovalTool:
    async def execute(self, action_description, risk_level):
        if risk_level == "low":
            return {"approved": True, "auto": True}

        # Send to approval queue
        approval_request = await self.create_request(action_description)

        # Wait for human response (with timeout)
        response = await self.wait_for_approval(
            approval_request.id,
            timeout_minutes=30
        )

        return {
            "approved": response.approved,
            "feedback": response.feedback,
            "auto": False
        }
```

### Memory Management
Handle long conversations and context:
```python
class AgentMemory:
    def __init__(self, max_tokens=8000):
        self.max_tokens = max_tokens
        self.messages = []
        self.summaries = []

    def add(self, message):
        self.messages.append(message)

        if self.token_count() > self.max_tokens:
            self.compress()

    def compress(self):
        # Summarize older messages
        old_messages = self.messages[:-5]  # Keep recent
        summary = summarize(old_messages)

        self.summaries.append(summary)
        self.messages = self.messages[-5:]

    def get_context(self):
        return {
            "summaries": self.summaries,
            "recent_messages": self.messages
        }
```

## Common Pitfalls to Avoid

- Building multi-agent systems when a single agent suffices
- Giving agents too much autonomy without safety bounds
- Not handling tool failures and edge cases
- Forgetting that LLMs can hallucinate tool calls
- Infinite loops when agents get stuck
- Not logging enough to debug agent behavior
- Assuming agents will follow instructions perfectly
- Ignoring cost (token usage) in agent loops
