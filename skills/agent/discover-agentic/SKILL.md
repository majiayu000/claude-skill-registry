---
name: discover-agentic
description: Automatically discover agentic workflow skills when building AI agents, implementing tool use patterns, managing context windows, decomposing complex tasks, or designing multi-step autonomous workflows. Activates for agentic AI development.
license: MIT
metadata:
  author: rand
  version: "3.1"
compatibility: Designed for Claude Code. Compatible with any agent supporting the Agent Skills format.
---

# Agentic Workflow Skills Discovery

Provides automatic access to skills for building autonomous AI agents, managing tool use, and orchestrating multi-step workflows.

## When This Skill Activates

This skill auto-activates when you're working with:
- AI agent development and autonomous workflows
- Task decomposition for LLM agents
- Function calling and tool use patterns
- Context window management and summarization
- Working memory, scratchpads, and state tracking
- Long-term memory and persistence patterns
- Multi-step reasoning and planning
- Failure recovery and re-planning strategies
- Parallel vs sequential execution decisions

## Available Skills

### Quick Reference

The Agentic category contains 3 specialized skills:

1. **agentic-task-decomposition** - Breaking complex goals into agent-executable steps, dependency graphs, re-planning
2. **agentic-tool-use** - Function calling patterns, parallel tool use, error handling, tool selection heuristics
3. **agentic-memory** - Context window management, working memory, long-term persistence, summarization

### Load Full Category Details

For complete descriptions and workflows:

Read <cc-polymath-root>/skills/agentic/INDEX.md


This loads the full Agentic category index with:
- Detailed skill descriptions
- Usage triggers for each skill
- Common workflow combinations
- Cross-references to related skills

### Load Specific Skills

Load individual skills as needed:


# Task planning and decomposition
Read <cc-polymath-root>/skills/agentic/agentic-task-decomposition.md

# Tool calling and execution
Read <cc-polymath-root>/skills/agentic/agentic-tool-use.md

# Context and memory management
Read <cc-polymath-root>/skills/agentic/agentic-memory.md


## Common Workflows

### Building an Agent from Scratch
**Sequence**: Decomposition -> Tool Use -> Memory

Read <cc-polymath-root>/skills/agentic/agentic-task-decomposition.md  # Plan the agent's task handling
Read <cc-polymath-root>/skills/agentic/agentic-tool-use.md            # Implement tool execution
Read <cc-polymath-root>/skills/agentic/agentic-memory.md              # Add context management


### Adding Tool Use to an Agent
**Sequence**: Tool Use -> Decomposition

Read <cc-polymath-root>/skills/agentic/agentic-tool-use.md            # Tool calling patterns
Read <cc-polymath-root>/skills/agentic/agentic-task-decomposition.md  # Multi-tool task planning


### Scaling Agent Sessions
**Sequence**: Memory -> Decomposition

Read <cc-polymath-root>/skills/agentic/agentic-memory.md              # Context management
Read <cc-polymath-root>/skills/agentic/agentic-task-decomposition.md  # Context-bounded task sizing


### Complete Agentic Stack
**Full implementation**:


# 1. Planning layer
Read <cc-polymath-root>/skills/agentic/agentic-task-decomposition.md

# 2. Execution layer
Read <cc-polymath-root>/skills/agentic/agentic-tool-use.md

# 3. Memory layer
Read <cc-polymath-root>/skills/agentic/agentic-memory.md


## Skill Selection Guide

**Choose task decomposition when:**
- Complex goal needs breaking into steps
- Tasks have dependencies or ordering constraints
- Need to handle ambiguous requirements
- Building a planning layer for an agent

**Choose tool use when:**
- Implementing function calling in an LLM agent
- Debugging tool call failures or inefficiency
- Designing tool schemas and structured outputs
- Optimizing multi-tool workflows

**Choose memory when:**
- Agent sessions are hitting context limits
- Need to persist state across turns or sessions
- Building multi-turn conversational agents
- Implementing retrieval-augmented generation

## Integration with Other Skills

Agentic skills commonly combine with:

**API skills** (`discover-api`):
- Agents that call REST/GraphQL APIs
- Tool schemas for API endpoints
- Authentication handling in agent workflows

**Testing skills** (`discover-testing`):
- Testing agent behaviors and tool use
- Autonomous test generation
- Verifying agent task completion

**Database skills** (`discover-database`):
- Database-backed agent memory
- Agents that query and modify data
- Persistent state management

**Infrastructure skills** (`discover-infra`, `discover-cloud`):
- Deploying agent systems
- Scaling agent workloads
- Cost optimization for LLM calls

## Usage Instructions

1. **Auto-activation**: This skill loads automatically when Claude Code detects agentic workflow tasks
2. **Browse skills**: Run `Read <cc-polymath-root>/skills/agentic/INDEX.md` for full category overview
3. **Load specific skills**: Use commands above to load individual skills
4. **Follow workflows**: Use recommended sequences for common agentic patterns
5. **Combine skills**: Load multiple skills for comprehensive coverage

## Progressive Loading

This gateway skill (~200 lines, ~2K tokens) enables progressive loading:
- **Level 1**: Gateway loads automatically (you're here now)
- **Level 2**: Load category INDEX.md (~3K tokens) for full overview
- **Level 3**: Load specific skills (~2-3K tokens each) as needed

Total context: 2K + 3K + skill(s) = 5-10K tokens vs 12K+ for entire category.

## Quick Start Examples

**"Build an autonomous coding agent"**:
Read <cc-polymath-root>/skills/agentic/agentic-task-decomposition.md


**"How should my agent call tools?"**:
Read <cc-polymath-root>/skills/agentic/agentic-tool-use.md


**"My agent is running out of context"**:
Read <cc-polymath-root>/skills/agentic/agentic-memory.md



**Next Steps**: Run `Read <cc-polymath-root>/skills/agentic/INDEX.md` to see full category details, or load specific skills using the commands above.
