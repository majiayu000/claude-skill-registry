---
name: manage-agents
description: |
  Creates, modifies, and manages Claude Code subagents by writing agent files with YAML frontmatter,
  system prompts, and tool configurations. Use when you need to "create an agent", "modify an agent",
  "set up a specialist", "I need an agent for [task]", "agent to handle [domain]", or "configure
  agent tools". Covers agent file format, YAML frontmatter, system prompts, tool restrictions,
  MCP integration, model selection, and testing.
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
  - Bash
---

# Manage Agents

Create and manage specialized Claude Code subagents with custom capabilities, tool access, and expertise domains.

**Use this skill when you need to:**
- Create new subagents for specialized tasks
- Modify existing agent configurations
- Set up domain experts (Python, Neo4j, Testing, etc.)
- Configure tool access and MCP server permissions
- Understand agent structure and best practices

## Quick Start

To create a new agent:

1. **Understand the Need**: What specialized capability or domain expertise is needed?
2. **Choose Location**: Project-level (.claude/agents/) or user-level (~/.claude/agents/)
3. **Define Configuration**: Name, description, model, tools, and permissions
4. **Write System Prompt**: Clear instructions for the agent's specialized role
5. **Test & Validate**: Invoke with @agent-name and verify behavior

## Table of Contents

### Core Sections

- [Instructions](#instructions)
  - [Step 1: Analyze Requirements](#step-1-analyze-requirements) - Determine expertise domain, tool needs, and location
  - [Step 2: Create Agent File](#step-2-create-agent-file) - Choose project vs user location
  - [Step 3: Write Agent Configuration](#step-3-write-agent-configuration) - YAML frontmatter template
  - [Step 4: Configure Tool Access](#step-4-configure-tool-access) - Explicit tools, all tools, or no tools
  - [Step 5: Configure MCP Access](#step-5-configure-mcp-access) - Specific servers, all servers, or all resources
  - [Step 6: Select Model](#step-6-select-model) - Sonnet, Opus, or Haiku based on complexity
  - [Step 7: Write System Prompt](#step-7-write-system-prompt) - Clear, actionable, quality-focused instructions
  - [Step 8: Test the Agent](#step-8-test-the-agent) - Verify behavior and tool access
  - [Step 9: Document Integration](#step-9-document-integration) - Update dispatch.md and CLAUDE.md

- [Common Patterns](#common-patterns)
  - [Pattern 1: Domain Expert](#pattern-1-domain-expert) - Read-only analysis and recommendations
  - [Pattern 2: Code Generator](#pattern-2-code-generator) - Write access with quality gates
  - [Pattern 3: Orchestrator](#pattern-3-orchestrator) - Planning agent that delegates
  - [Pattern 4: Quality Guardian](#pattern-4-quality-guardian) - Read-only validation
  - [Pattern 5: Integration Specialist](#pattern-5-integration-specialist) - MCP-focused agent

### Supporting Resources

- [Configuration Reference](./references/reference.md) - Complete field documentation

### Utility Scripts

- [Agent Detection](./scripts/agent_detector_example.py) - Detect @agent-name patterns in prompts
- [Agent Memory Creation](./scripts/create_agent_memories_simple.py) - Create MCP memory entries for agents
- [Agent Validation](./scripts/validate_agent.py) - Validate agent file format and configuration

### Advanced Topics

- [Troubleshooting](#troubleshooting)
  - [Agent not appearing in autocomplete](#agent-not-appearing-in-autocomplete)
  - [Tool access denied](#tool-access-denied)
  - [Agent behavior incorrect](#agent-behavior-incorrect)
  - [Integration issues](#integration-issues)
- [Validation](#validation) - Validate agent files with script
- [Quality Checklist](#quality-checklist) - Pre-finalization checklist
- [Advanced: Agent Chaining](#advanced-agent-chaining) - Agent-to-agent delegation
- [Advanced: Dynamic Selection](#advanced-dynamic-selection) - Autonomous agent selection
- [Integration with This Project](#integration-with-this-project) - Project-specific guidance

## Instructions

### Step 1: Analyze Requirements

Before creating an agent, determine:

- **Expertise Domain**: What specialized knowledge does this agent need?
- **Tool Requirements**: Which tools should be allowed/restricted?
- **Context Needs**: Does it need access to project files, memory, or MCP servers?
- **Location**: Project-specific (.claude/agents/) or user-wide (~/.claude/agents/)?
- **Model Selection**: Does this need Sonnet, Opus, or Haiku?

### Step 2: Create Agent File

**Project Agent** (checked into git):
```bash
# Location: .claude/agents/my-specialist.md
```

**User Agent** (personal, not in git):
```bash
# Location: ~/.claude/agents/my-specialist.md
```

**Priority**: Project agents override user agents with the same name.

### Step 3: Write Agent Configuration

Use this template:

```yaml
---
name: agent-name
description: Clear description of what this agent does and when to use it
model: claude-sonnet-4
tools:
  - Read
  - Write
  - Grep
  - Glob
  - Bash
mcp_servers:
  - server-name
allow_all_tools: false
allow_all_mcp_servers: false
allow_mcp_resources_from_all_servers: false
---

# Agent Name - Specialized Role

You are a specialized agent focused on [domain/task]. Your expertise includes:
- [Key capability 1]
- [Key capability 2]
- [Key capability 3]

## Your Responsibilities

1. **[Primary Responsibility]**: Clear description
2. **[Secondary Responsibility]**: Clear description
3. **[Quality Standards]**: What standards you uphold

## Tools Available

You have access to:
- [Tool 1]: [How to use it]
- [Tool 2]: [How to use it]
- [MCP Server]: [What it provides]

## Workflow

When invoked, follow these steps:

1. [Step 1]
2. [Step 2]
3. [Step 3]

## Quality Gates

Before completing work:
- [ ] [Quality check 1]
- [ ] [Quality check 2]
- [ ] [Quality check 3]

## Integration with Skills

You can leverage these skills:
- [Skill 1]: [When to use]
- [Skill 2]: [When to use]

## Best Practices

- [Practice 1]
- [Practice 2]
- [Practice 3]

## Examples

[Provide concrete examples of your work]
```

### Step 4: Configure Tool Access

**Option 1: Explicit Tool List** (Recommended)
```yaml
tools:
  - Read
  - Write
  - Grep
  - Glob
allow_all_tools: false
```

**Option 2: Allow All Tools**
```yaml
allow_all_tools: true
```

**Option 3: No Tools** (Analysis/planning only)
```yaml
tools: []
allow_all_tools: false
```

### Step 5: Configure MCP Access

**Option 1: Specific MCP Servers** (Recommended)
```yaml
mcp_servers:
  - project-watch-mcp
  - memory
allow_all_mcp_servers: false
```

**Option 2: All MCP Servers**
```yaml
allow_all_mcp_servers: true
```

**Option 3: All MCP Resources** (Use sparingly)
```yaml
allow_mcp_resources_from_all_servers: true
```

### Step 6: Select Model

Choose based on task complexity:

- **claude-sonnet-4**: Default, balanced performance (most agents)
- **claude-opus-4**: Complex reasoning, critical decisions
- **claude-haiku-3-5**: Fast, simple tasks, high volume

**Default if not specified**: claude-sonnet-4

### Step 7: Write System Prompt

The content after YAML frontmatter is the system prompt. Make it:

1. **Specific**: Define clear responsibilities and scope
2. **Actionable**: Include step-by-step workflows
3. **Quality-Focused**: Define standards and validation criteria
4. **Integrated**: Reference skills, tools, and project patterns
5. **Example-Rich**: Show concrete examples of expected work

### Step 8: Test the Agent

**Interactive Testing:**

Invoke the agent in Claude:
```bash
@agent-name please [task description]
```

**Programmatic Testing:**

Test agents from command line using CLI tools:

```bash
# Quick test with claude_ask.py
python3 .claude/tools/agents/claude_ask.py agent-name "test question"

# Quiet mode (just the answer)
python3 .claude/tools/agents/claude_ask.py -q agent-name "test question"

# JSON output for validation
python3 .claude/tools/agents/claude_ask.py --json agent-name "test question"

# With timeout for complex tasks
python3 .claude/tools/agents/claude_ask.py agent-name "complex task" --timeout 120
```

**For complete documentation on CLI testing tools, see:**
- CLI testing tools documentation available in project's .claude/tools/agents/ directory

Verify:
- [ ] Agent appears in autocomplete
- [ ] Agent has correct tool access
- [ ] Agent follows its system prompt
- [ ] Agent produces expected quality
- [ ] Agent integrates with skills correctly
- [ ] Agent responds correctly via CLI tools

### Step 9: Document Integration

If this is a project agent, document in relevant files:
- Add to agent dispatch documentation if available
- Reference in project CLAUDE.md if core to workflow
- Update skills that should integrate with this agent

## Configuration Reference

For complete configuration field documentation, see [references/reference.md](./references/reference.md).

## Examples

For practical agent examples and patterns, see the utility scripts section and references/reference.md for detailed configuration examples.

### Working with Agent Detection

The [scripts/agent_detector_example.py](scripts/agent_detector_example.py) script demonstrates patterns for detecting agents in hooks or tools:

**The example demonstrates:**
- Using `detect_agent()` to identify agent mentions in user prompts
- Getting available agents and patterns with `get_available_agents()`
- Pattern matching for agent invocation (e.g., `@unit-tester`)
- Integration points for hooks that need agent awareness

**Run the example:**
```bash
cd /Users/dawiddutoit/projects/play/temet-run/.claude
./.venv/bin/python3 skills/manage-agents/scripts/agent_detector_example.py
```

The script uses the shared `.claude/` environment pattern:
```python
# Setup: Add .claude to path for skill_utils
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from skill_utils import ensure_path_setup, get_project_root
ensure_path_setup()

# Now import from the shared environment
import yaml
```

This pattern allows the script to access dependencies installed in `.claude/pyproject.toml` without duplicating virtual environments.

### Creating Agent Core Memories

The [scripts/create_agent_memories_simple.py](scripts/create_agent_memories_simple.py) script demonstrates programmatic memory creation:

**The example demonstrates:**
- Extracting agent names and descriptions from agent files
- Connecting to the memory MCP server using FastMCP client
- Creating core memory entries for all agents (`agent-{name}-core`)
- Batch processing of agent directory

**Run the example:**
```bash
cd /Users/dawiddutoit/projects/play/temet-run/.claude
uv sync --extras mcp  # Install MCP dependencies (if not already done)
./.venv/bin/python3 skills/manage-agents/scripts/create_agent_memories_simple.py
```

**Prerequisites:**
- Neo4j memory server running
- MCP dependencies installed via `uv sync --extras mcp`
- Environment variables set: NEO4J_URL, NEO4J_USERNAME, NEO4J_PASSWORD, NEO4J_DATABASE

The script also uses the shared `.claude/` environment pattern, allowing it to access `yaml` and `fastmcp` dependencies without duplicating virtual environments.

## Common Patterns

### Pattern 1: Domain Expert
Specialized knowledge agent with read-only access for analysis and recommendations.

### Pattern 2: Code Generator
Write access with quality gates, focused on specific code patterns.

### Pattern 3: Orchestrator
High-level planning agent that delegates to other agents.

### Pattern 4: Quality Guardian
Read-only validation agent that checks against standards.

### Pattern 5: Integration Specialist
MCP-focused agent with access to specific external tools.

## Troubleshooting

**Agent not appearing in autocomplete:**
- Check file is in .claude/agents/ or ~/.claude/agents/
- Verify YAML frontmatter is valid
- Ensure name field matches filename (without .md)

**Tool access denied:**
- Check tools list in frontmatter
- Verify allow_all_tools setting
- Ensure MCP servers are configured correctly

**Agent behavior incorrect:**
- Review system prompt clarity
- Check for conflicting instructions
- Verify model selection is appropriate

**Integration issues:**
- Ensure skills referenced are available
- Check MCP server connections
- Verify project context is accessible

## Validation

Use the [scripts/validate_agent.py](scripts/validate_agent.py) script to check agent files:

```bash
cd /Users/dawiddutoit/projects/play/temet-run/.claude
./.venv/bin/python3 skills/manage-agents/scripts/validate_agent.py agents/my-agent.md
```

The validation script checks:
- Valid YAML frontmatter syntax
- Required fields (name, description)
- Valid tool names and model selection
- Name matches filename
- Description quality (includes trigger terms)
- Non-empty system prompt

## Quality Checklist

Before finalizing an agent:

- [ ] YAML frontmatter is valid and complete
- [ ] Description is clear and includes trigger terms
- [ ] Tool access is appropriate (least privilege)
- [ ] System prompt is specific and actionable
- [ ] Quality gates are defined
- [ ] Examples are provided
- [ ] Integration points are documented
- [ ] Agent tested with sample invocation
- [ ] Documentation updated (if project agent)

## Advanced: Agent Chaining

Agents can invoke other agents:

```markdown
For implementation, delegate to @implementer:
@implementer please create the service class with proper dependency injection
```

**Best Practice**: Use chaining for clear separation of concerns (planning → implementation → testing).

## Advanced: Dynamic Selection

Let Claude choose the right agent:

```markdown
"I need help with Neo4j queries"
→ Claude autonomously selects @neo4j-expert based on description
```

**Requirement**: Agent descriptions must include trigger terms and use cases.

## Integration with This Project

When creating agents for project-watch-mcp:

1. **Align with Architecture**: Reference Clean Architecture layers in system prompt
2. **Follow Quality Standards**: Integrate quality gates (pyright, vulture, pytest, ruff)
3. **Use Project Patterns**: Reference ServiceResult, fail-fast, configuration injection
4. **Leverage Project Tools**: Access to MCP tools, log_analyzer.py, check_all.sh
5. **Reference Documentation**: Link to ARCHITECTURE.md, ADRs, CLAUDE.md

## Resources

- **Detailed Reference**: [references/reference.md](./references/reference.md)
- **Utility Scripts**:
  - [Agent Detector](./scripts/agent_detector_example.py) - Detect agent mentions in prompts
  - [Memory Creation](./scripts/create_agent_memories_simple.py) - Create agent memory entries
  - [Validation](./scripts/validate_agent.py) - Validate agent files
