---
name: adw-design
description: Guide creation of AI Developer Workflows (ADWs) that combine deterministic orchestration code with non-deterministic agents. Use when building automated development pipelines, designing AFK agent systems, or implementing the PITER framework.
allowed-tools: Read, Grep, Glob
---

# ADW Design

Guide for creating AI Developer Workflows - reusable agentic workflows that combine deterministic code with non-deterministic agents.

## When to Use

- Building automated development pipelines
- Designing AFK (Away From Keyboard) agent systems
- Implementing the PITER framework
- Creating micro agent architectures
- Setting up GitHub issue → PR automation

## What is an ADW?

An ADW is the highest composition level of agentic coding:

```text
ADW = Orchestrator + Micro Agents + Triggers + Observability
```

Components:

1. **Orchestrator** - Python/TypeScript code that coordinates the workflow
2. **Micro Agents** - Specialized Claude Code invocations with single responsibilities
3. **Triggers** - Webhooks, cron, or manual invocation
4. **Observability** - Logging, issue comments, tracking

## ADW Design Process

### Step 1: Define the Workflow

Map out the phases:

```text
Input → Classify → Branch → Plan → Implement → Review
```

Questions to answer:

- What's the input source? (GitHub issues, Notion, Slack)
- What are the phases? (classify, plan, implement, review)
- What's the output? (PR, deployment, report)

### Step 2: Design Micro Agents

For each phase, define a specialized agent:

| Phase | Agent | Responsibility | Model |
| --- | --- | --- | --- |
| Classify | `issue_classifier` | Determine work type | Haiku |
| Branch | `branch_generator` | Create branch name | Haiku |
| Plan | `sdlc_planner` | Generate implementation plan | Sonnet |
| Build | `sdlc_implementer` | Implement the solution | Sonnet |
| Commit | `committer` | Create semantic commits | Haiku |
| PR | `pr_creator` | Create pull request | Haiku |

### Step 3: Create Templates

Each agent needs a slash command:

- `/classify-issue` - Classify issue type
- `/generate-branch-name` - Create branch name
- `/chore`, `/bug`, `/feature` - Generate plans
- `/implement` - Execute plans
- `/commit-with-agent` - Create commits
- `/pull-request` - Create PRs

### Step 4: Build Orchestrator

The orchestrator coordinates everything:

```python
# Pseudocode structure
def run_adw(issue_number, adw_id):
    issue = fetch_issue(issue_number)
    issue_type = execute_agent("classifier", issue)
    branch = execute_agent("branch_generator", issue)
    plan = execute_agent("planner", issue_type, issue)
    execute_agent("implementer", plan)
    execute_agent("pr_creator", branch, issue, plan)
```

### Step 5: Add Observability

Track everything:

- **ADW ID**: 8-char UUID for correlation
- **Issue comments**: Progress updates
- **Logs**: Structured output per agent
- **Metrics**: Success rate, duration

## ADW Directory Structure

```text
adws/
├── main_workflow.py       # Main orchestrator
├── agent.py               # Claude Code integration
├── data_types.py          # Type definitions
├── github.py              # GitHub operations
├── trigger_cron.py        # Cron trigger
├── trigger_webhook.py     # Webhook trigger
├── health_check.py        # Environment validation
└── README.md              # Documentation
```

## Model Selection Strategy

Match model to task:

| Task Complexity | Model | Examples |
| --- | --- | --- |
| Simple decision | Haiku | Classification, branch naming |
| Formatting | Haiku | Commit messages, PR body |
| Reasoning | Sonnet | Plan generation |
| Complex coding | Sonnet/Opus | Implementation |

## ADW Quality Checklist

Before deploying:

- [ ] Each agent has single responsibility
- [ ] Model selection matches task complexity
- [ ] ADW ID tracking implemented
- [ ] Issue comments posted at each phase
- [ ] Error handling with meaningful messages
- [ ] Logging captures all agent outputs
- [ ] Health check validates environment
- [ ] Templates tested independently
- [ ] End-to-end workflow tested

## Common Patterns

### Agent Executor Pattern

```python
def execute_agent(agent_name, *args):
    prompt = build_prompt(agent_name, args)
    result = subprocess.run([
        "claude", "-p", prompt,
        "--model", get_model(agent_name),
        "--output-format", "stream-json"
    ])
    log_result(agent_name, result)
    return parse_result(result)
```

### Issue Comment Pattern

```python
def update_issue(issue_number, adw_id, agent_name, message):
    comment = f"[{adw_id}_{agent_name}] {message}"
    gh_issue_comment(issue_number, comment)
```

### Error Handling Pattern

```python
def check_error(result, phase):
    if not result.success:
        update_issue(issue, adw_id, phase, f"ERROR: {result.error}")
        sys.exit(1)
```

## Anti-Patterns to Avoid

### Monolithic Agent

**Bad**: One agent doing everything

**Good**: Micro agents with single responsibilities

### Missing Observability

**Bad**: No logging, no issue comments

**Good**: ADW ID tracking, structured logs, progress comments

### Wrong Model Selection

**Bad**: Using Opus for branch naming

**Good**: Match model to task complexity

### No Error Handling

**Bad**: Silent failures

**Good**: Error comments, graceful degradation

## Related Memory Files

- @piter-framework.md - PITER elements for AFK agents
- @adw-anatomy.md - ADW structure and patterns
- @outloop-checklist.md - Deployment readiness
- @inloop-vs-outloop.md - When to use ADWs

## Version History

- **v1.0.0** (2025-12-26): Initial release

---

## Last Updated

**Date:** 2025-12-26
**Model:** claude-opus-4-5-20251101
