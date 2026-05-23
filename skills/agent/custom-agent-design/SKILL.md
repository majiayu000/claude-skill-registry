---
name: custom-agent-design
description: Design custom agents from scratch using Claude Agent SDK patterns. Use when building domain-specific agents, designing agents with full SDK control, or creating specialized agents with custom tools and prompts.
allowed-tools: Read, Grep, Glob
---

# Custom Agent Design Skill

Design domain-specific agents using Claude Agent SDK patterns.

## Purpose

Guide the design of custom agents that solve domain-specific problems with full SDK control over Context, Model, Prompt, and Tools.

## When to Use

- Building a new custom agent
- Converting generic workflow to specialized agent
- Designing domain-specific automation
- Creating repeatable agent patterns

## Prerequisites

- Clear understanding of the domain problem
- Access to Claude Agent SDK documentation
- Understanding of when custom agents are appropriate (see @agent-evolution-path.md)

## Design Process

### Step 1: Define Agent Purpose

Answer these questions:

- What specific problem does this agent solve?
- What domain expertise does it need?
- What is the single purpose? (One agent, one purpose)
- Who are the stakeholders?

**Output**: Purpose statement (2-3 sentences)

### Step 2: Select Model

Choose based on task complexity:

| Task Type | Model | Why |
| --- | --- | --- |
| Simple transformations | Haiku | Fast, cheap |
| Balanced tasks | Sonnet | Good trade-off |
| Complex reasoning | Opus | Highest quality |

**Decision factors**:

- Speed requirements
- Quality requirements
- Cost constraints
- Task complexity

### Step 3: Design System Prompt

Choose architecture:

**Override** (`system_prompt=...`)

- When: Building a new product
- Result: NOT Claude Code anymore
- Full control over behavior

**Append** (`append_system_prompt=...`)

- When: Extending Claude Code
- Result: Enhanced Claude Code
- Adds capabilities

**System Prompt Template**:

```markdown
# [Agent Name]

## Purpose
[Identity and role definition - 2-3 sentences]

## Instructions
[Core behaviors - bullet list]
- Behavior 1
- Behavior 2

## Constraints
[What the agent must NOT do]

## Examples (if needed)
[Input/Output pairs]
```

### Step 4: Configure Tool Access

**Questions to answer**:

- What tools does this agent need?
- What tools should be blocked?
- Are custom tools required?

**Tool configuration**:

```python
# Whitelist approach
allowed_tools=["Read", "Write", "Bash"]

# Blacklist approach
disallowed_tools=["WebFetch", "WebSearch", "TodoWrite"]

# No default tools
disallowed_tools=["*"]

# Custom tools
mcp_servers={"domain": custom_mcp_server}
allowed_tools=["mcp__domain__tool1", "mcp__domain__tool2"]
```

### Step 5: Add Governance (Optional)

If security/governance required:

```python
hooks = {
    "PreToolUse": [
        HookMatcher(matcher="Read", hooks=[block_sensitive_files]),
        HookMatcher(hooks=[log_all_tool_usage]),
    ]
}
```

### Step 6: Select Deployment Form

| Form | Use When |
| --- | --- |
| Script | One-off automation, ADWs |
| Terminal REPL | Interactive tools |
| Backend API | UI integration |
| Data Stream | Real-time processing |
| Multi-Agent | Complex workflows |

### Step 7: Create Configuration

Assemble the ClaudeAgentOptions:

```python
options = ClaudeAgentOptions(
    # Context
    system_prompt=load_system_prompt("agent_system.md"),

    # Model
    model="opus",

    # Tools
    allowed_tools=["Read", "Write", "custom_tool"],
    disallowed_tools=["WebFetch", "WebSearch"],

    # Custom Tools (if needed)
    mcp_servers={"domain": domain_mcp_server},

    # Governance (if needed)
    hooks=security_hooks,

    # Session (if needed)
    resume=session_id,
)
```

## Output Format

When designing a custom agent, provide:

```markdown
## Custom Agent Design

**Name:** [agent-name]
**Purpose:** [1-2 sentences]
**Domain:** [area of expertise]

### Configuration

**Model:** [haiku/sonnet/opus] - [reason]

**System Prompt Architecture:**
- Type: [Override/Append]
- Reason: [why this choice]

**Tool Access:**
- Allowed: [list]
- Disallowed: [list]
- Custom: [list if any]

**Governance:**
- Hooks: [list if any]
- Security: [considerations]

**Deployment:**
- Form: [script/repl/api/stream/multi-agent]
- Reason: [why this form]

### System Prompt

[Full system prompt content]

### Implementation Notes

[Any special considerations]
```

## Design Checklist

- [ ] Purpose is specific and clear
- [ ] Model matches task complexity
- [ ] System prompt architecture chosen (override vs append)
- [ ] System prompt follows template
- [ ] Tool access is minimal (only what's needed)
- [ ] Governance hooks added if security required
- [ ] Deployment form selected
- [ ] Configuration assembled

## Anti-Patterns

| Avoid | Why | Instead |
| --- | --- | --- |
| Competing with Claude Code | Can't beat general agent | Specialize instead |
| Generic system prompts | No domain advantage | Domain-specific |
| Too many tools | Context overhead | Minimal tool set |
| Missing governance | Security risk | Add hooks |
| Override when append works | Loses Claude Code benefits | Use append |

## Cross-References

- @agent-evolution-path.md - When to build custom agents
- @core-four-custom.md - Core Four configuration
- @system-prompt-architecture.md - Override vs append
- @custom-tool-patterns.md - Tool creation
- @model-selection skill - Model selection guidance

## Version History

- **v1.0.0** (2025-12-26): Initial release

---

## Last Updated

**Date:** 2025-12-26
**Model:** claude-opus-4-5-20251101
