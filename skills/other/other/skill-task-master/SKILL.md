---
name: task-master
description:
  AI-powered task management for structured, specification-driven development. Use this skill when
  you need to manage complex projects with PRDs, break down tasks into subtasks, track dependencies,
  and maintain organized development workflows across features and branches.
---

# Task Master AI

An AI-powered task management system that integrates seamlessly with AI Agents to manage
specification-driven development workflows.

## Quick Start

**Three Ways to Use Task Master:**

1. **MCP Tools** (Recommended) - Direct integration via Model Context Protocol
2. **CLI Commands** - Terminal-based task management
3. **Tagged Contexts** - Multi-branch/feature task isolation

## Core Capabilities

### Task Management

- Parse PRDs into actionable tasks automatically
- Break down complex tasks into manageable subtasks
- Track task dependencies and status
- Support for multiple task contexts (tags) for features/branches

### AI-Powered Features

- Complexity analysis with recommendations
- Research-backed task expansion
- Intelligent task updates based on implementation drift
- Fresh information gathering beyond knowledge cutoff

### Development Workflow

- Specification-driven development (SDD) support
- Iterative subtask implementation logging
- Git branch-aligned task contexts
- Team collaboration with isolated task lists

## When to Use This Skill

✅ **Use Task Master when:**

- Starting a new project from a PRD
- Managing complex multi-step features
- Working on feature branches with isolated tasks
- Need to track task dependencies and priorities
- Want AI-assisted task breakdown and planning
- Collaborating with team members on shared codebase
- Need to log implementation progress iteratively

❌ **Skip Task Master for:**

- Simple single-file changes
- Quick bug fixes
- Trivial tasks with no dependencies
- Projects without formal requirements

## Setup

### Prerequisites

- Node.js installed
- API keys for AI providers (Anthropic, Perplexity, etc.)
- Git repository (optional, for branch-based workflows)

### Installation

**Global Installation:**

```bash
npm install -g task-master-ai
```

**Project-Local:**

```bash
npm install task-master-ai
```

### MCP Configuration

Add to your MCP config file (`.cursor/mcp.json`, `.vscode/mcp.json`, etc.):

```json
{
  "mcpServers": {
    "task-master-ai": {
      "command": "npx",
      "args": ["-y", "task-master-ai"],
      "env": {
        "ANTHROPIC_API_KEY": "YOUR_KEY_HERE",
        "PERPLEXITY_API_KEY": "YOUR_KEY_HERE"
      }
    }
  }
}
```

For complete setup details, see `references/SETUP.md`.

## Basic Workflow

### 1. Initialize Project

```
Initialize taskmaster-ai in my project
```

### 2. Create PRD

Create your Product Requirements Document at `.taskmaster/docs/prd.txt`

### 3. Parse PRD

```
Parse my PRD at .taskmaster/docs/prd.txt
```

### 4. View Tasks

```
Show me the task list
```

### 5. Work on Tasks

```
What's the next task I should work on?
Can you help me implement task 3?
```

### 6. Track Progress

```
Mark task 3 as done
Update subtask 3.2 with my implementation findings
```

## Key Concepts

### Tagged Task Lists

Organize tasks into separate contexts (tags) for:

- Feature branches (`feature-auth`, `feature-dashboard`)
- Experiments (`experiment-zustand`)
- Team collaboration (`alice-work`, `bob-work`)
- Versions (`v1.0`, `v2.0`, `mvp`)

### Task Structure

- **ID**: Unique identifier (e.g., `1`, `1.2`)
- **Title**: Brief description
- **Description**: What needs to be done
- **Status**: `pending`, `in-progress`, `done`, `deferred`
- **Dependencies**: Prerequisites (e.g., `[1, 2.1]`)
- **Priority**: `high`, `medium`, `low`
- **Details**: Implementation notes
- **Subtasks**: Breakdown of complex tasks

### Complexity Analysis

AI analyzes task complexity (1-10 scale) and recommends:

- Number of subtasks needed
- Areas requiring research
- Implementation approach

## Common Commands

### Task Viewing

```
List all tasks
Show me task 5
Show me tasks 1, 3, and 5
What's the next task?
```

### Task Creation & Modification

```
Add a task to implement user authentication
Expand task 4 into subtasks
Update task 5 with new requirements
Mark task 3 as done
```

### Task Organization

```
Move task 5 to become subtask 7.3
Add dependency: task 8 depends on task 5
Create a new tag called feature-auth
Switch to the feature-auth tag
```

### Research & Analysis

```
Research the latest best practices for JWT authentication
Analyze task complexity for all pending tasks
Expand all pending tasks based on complexity
```

## Advanced Workflows

### PRD-Driven Feature Development

1. Create dedicated tag for feature
2. Write comprehensive PRD
3. Parse PRD into tag
4. Analyze complexity
5. Expand complex tasks
6. Implement iteratively

### Team Collaboration

1. Create personal tag for your work
2. Copy tasks from master
3. Work in isolation
4. Merge back when ready

### Branch-Based Development

1. Create git branch
2. Create matching tag from branch
3. Develop feature with isolated tasks
4. Merge code and tasks together

## Integration with Development

### Iterative Implementation

1. View subtask details
2. Plan implementation approach
3. Log plan to subtask
4. Begin coding
5. Log progress and findings
6. Mark complete
7. Commit changes

### Specification-Driven Development

Task Master supports full SDD workflow:

- Requirements gathering
- PRD creation
- Task generation
- Complexity analysis
- Implementation tracking
- Progress documentation

## Resources

- `references/SETUP.md` - Complete installation and configuration
- `references/WORKFLOW.md` - Detailed development workflows
- `references/COMMANDS.md` - Comprehensive command reference
- `references/BEST_PRACTICES.md` - Tips and patterns

## References

- [Task Master GitHub](https://github.com/eyaltoledano/claude-task-master)
- [Task Master Website](https://task-master.dev)
- [MCP Documentation](https://modelcontextprotocol.io)

---

**Quick Tips:**

- Always start with a detailed PRD
- Use complexity analysis before expanding tasks
- Log implementation findings to subtasks
- Leverage tags for feature isolation
- Use research tool for fresh information
