---
name: multi-agent-orchestration
description: >
  Patterns for multi-agent systems including orchestrator, pipeline, consensus, delegation,
  supervisor, and swarm patterns. Use when the user is building multi-agent workflows,
  coordinating multiple AI agents, implementing agent delegation or supervision, or
  designing systems where agents collaborate on complex tasks.
---

# Multi-Agent Orchestration

Patterns for coordinating multiple AI agents to solve complex tasks. Covers orchestrator,
pipeline, consensus, delegation, supervisor, and swarm architectures.

## When to Use
- User is building a system with multiple cooperating agents
- User needs task delegation or agent supervision patterns
- User wants consensus-based decision making across agents
- User is designing pipeline processing with agent stages
- User asks about swarm intelligence or emergent agent behavior

## Core Patterns

### Orchestrator Pattern

A central orchestrator decomposes tasks and delegates to specialized worker agents.

```python
import anthropic

client = anthropic.Anthropic()

def orchestrator(task: str) -> str:
    # Step 1: Plan and decompose
    plan = client.messages.create(
        model="claude-sonnet-4-6-20250514",
        max_tokens=2048,
        system="""You are a task orchestrator. Break the task into subtasks.
Return a JSON array of subtasks, each with "id", "agent", "instruction", and "depends_on" (list of ids).
Available agents: researcher, coder, reviewer.""",
        messages=[{"role": "user", "content": task}]
    )

    subtasks = json.loads(plan.content[0].text)

    # Step 2: Execute subtasks respecting dependencies
    results = {}
    for subtask in topological_sort(subtasks):
        dep_context = "\n".join(
            f"Result of {d}: {results[d]}" for d in subtask["depends_on"]
        )
        result = run_worker(
            agent=subtask["agent"],
            instruction=subtask["instruction"],
            context=dep_context
        )
        results[subtask["id"]] = result

    # Step 3: Synthesize final result
    synthesis = client.messages.create(
        model="claude-sonnet-4-6-20250514",
        max_tokens=4096,
        system="Synthesize the worker results into a coherent final response.",
        messages=[{"role": "user", "content": json.dumps(results)}]
    )
    return synthesis.content[0].text

def run_worker(agent: str, instruction: str, context: str) -> str:
    system_prompts = {
        "researcher": "You are a research agent. Find and summarize relevant information.",
        "coder": "You are a coding agent. Write clean, tested code.",
        "reviewer": "You are a review agent. Find bugs, security issues, and improvements."
    }
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",  # Workers use faster model
        max_tokens=2048,
        system=system_prompts[agent],
        messages=[{"role": "user", "content": f"{instruction}\n\nContext:\n{context}"}]
    )
    return response.content[0].text
```

### Pipeline Pattern

Agents process data sequentially, each stage transforming the output for the next.

```python
def pipeline(input_text: str) -> dict:
    stages = [
        ("extract", "Extract all entities, facts, and claims from this text. Return structured JSON."),
        ("validate", "Verify each fact and claim. Mark each as verified, unverified, or false. Return updated JSON."),
        ("summarize", "Create a concise summary highlighting only verified facts. Return final JSON with summary field.")
    ]

    current = input_text
    for stage_name, instruction in stages:
        response = client.messages.create(
            model="claude-sonnet-4-6-20250514",
            max_tokens=4096,
            system=f"You are the {stage_name} stage of a processing pipeline. {instruction}",
            messages=[{"role": "user", "content": current}]
        )
        current = response.content[0].text

    return json.loads(current)
```

### Consensus Pattern

Multiple agents independently analyze the same input, then a judge resolves disagreements.

```python
def consensus_review(code: str) -> dict:
    perspectives = [
        ("security_expert", "Review for security vulnerabilities. Rate severity."),
        ("performance_engineer", "Review for performance issues and optimization opportunities."),
        ("maintainability_reviewer", "Review for code quality, readability, and maintainability.")
    ]

    # Gather independent reviews in parallel
    reviews = {}
    for role, instruction in perspectives:
        response = client.messages.create(
            model="claude-sonnet-4-6-20250514",
            max_tokens=2048,
            system=f"You are a {role}. {instruction}",
            messages=[{"role": "user", "content": f"Review this code:\n```\n{code}\n```"}]
        )
        reviews[role] = response.content[0].text

    # Judge synthesizes and resolves conflicts
    judge_response = client.messages.create(
        model="claude-sonnet-4-6-20250514",
        max_tokens=4096,
        system="""You are a senior engineering judge. Synthesize multiple code reviews.
Resolve any disagreements. Produce a final verdict with prioritized action items.
Return JSON with: overall_rating, critical_issues, recommendations, and dissenting_opinions.""",
        messages=[{"role": "user", "content": json.dumps(reviews)}]
    )
    return json.loads(judge_response.content[0].text)
```

### Delegation Pattern

An agent decides at runtime which specialist to delegate to.

```python
def delegating_agent(user_request: str) -> str:
    # Agent decides which specialist to invoke
    routing = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=256,
        system="""Route the request to the best specialist. Return JSON:
{"specialist": "sql_expert|api_designer|frontend_dev|devops_engineer", "refined_task": "..."}""",
        messages=[{"role": "user", "content": user_request}]
    )

    route = json.loads(routing.content[0].text)

    specialist_prompts = {
        "sql_expert": "You write optimized, safe SQL queries. Always use parameterized queries.",
        "api_designer": "You design RESTful APIs following OpenAPI 3.0 best practices.",
        "frontend_dev": "You build accessible, performant React components.",
        "devops_engineer": "You write infrastructure as code and CI/CD pipelines."
    }

    result = client.messages.create(
        model="claude-sonnet-4-6-20250514",
        max_tokens=4096,
        system=specialist_prompts[route["specialist"]],
        messages=[{"role": "user", "content": route["refined_task"]}]
    )
    return result.content[0].text
```

### Supervisor Pattern

A supervisor monitors worker agents, intervenes on failure, and ensures quality.

```python
def supervised_execution(task: str, max_retries: int = 3) -> str:
    for attempt in range(max_retries):
        # Worker attempts the task
        worker_result = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=4096,
            system="Complete the task. Return your result in <result> tags and confidence (0-1) in <confidence> tags.",
            messages=[{"role": "user", "content": task}]
        )
        worker_output = worker_result.content[0].text

        # Supervisor evaluates quality
        evaluation = client.messages.create(
            model="claude-sonnet-4-6-20250514",
            max_tokens=1024,
            system="""Evaluate the worker's output. Return JSON:
{"approved": true/false, "issues": ["..."], "guidance": "feedback for retry if not approved"}""",
            messages=[{
                "role": "user",
                "content": f"Task: {task}\n\nWorker output:\n{worker_output}"
            }]
        )

        verdict = json.loads(evaluation.content[0].text)
        if verdict["approved"]:
            return worker_output

        # Provide feedback for next attempt
        task = f"{task}\n\nPrevious attempt feedback: {verdict['guidance']}"

    return worker_output  # Return best effort after max retries
```

## Anti-Patterns
- Using the most expensive model for every agent (use Haiku for workers, Sonnet for orchestrators)
- Not passing context between dependent agents (each agent works blind)
- Running all agents sequentially when they could run in parallel
- Letting agents communicate in free-form text without structured interfaces
- No termination condition in agentic loops (infinite retries)
- Single agent doing everything instead of decomposing into specialists
- Not logging intermediate results (makes debugging impossible)

## Quick Reference

| Pattern | When to Use | Tradeoff |
|---------|-------------|----------|
| Orchestrator | Complex tasks needing decomposition | Flexible but adds latency |
| Pipeline | Sequential data transformation | Simple but rigid ordering |
| Consensus | High-stakes decisions needing validation | Thorough but expensive |
| Delegation | Variable task types needing routing | Fast but needs good routing |
| Supervisor | Quality-critical output needing review | Reliable but slower |
| Swarm | Emergent problem-solving | Adaptive but hard to debug |

Model selection for agents:
- Orchestrator / Judge / Supervisor: `claude-sonnet-4-6` or `claude-opus-4-6`
- Workers / Routers: `claude-haiku-4-5` (3x cost savings)
- Critical analysis: `claude-opus-4-6` with extended thinking
