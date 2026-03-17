---
name: create-subagent
description: This skill should be used when creating custom subagents for Claude Code, configuring specialized AI assistants, or when the user asks about agent creation, agent configuration, or delegating tasks to subagents. Covers both file-based agents and Task tool invocation.
---

# Create Subagent

This skill provides comprehensive guidance for creating and configuring subagents in Claude Code.

## Understanding Subagents

Subagents are specialized AI assistants that Claude Code can delegate tasks to. Each subagent:

- Operates in its own context window (preserving main conversation context)
- Has a specific purpose and expertise area
- Can be configured with specific tools and permissions
- Includes a custom system prompt guiding its behavior

### When to Create Subagents

**Create a subagent when:**

- Tasks require specialized expertise that benefits from focused instructions
- Context preservation is important (subagents don't pollute main context)
- The same specialized workflow is needed repeatedly
- Different tool permissions are needed for different tasks
- Parallel execution of independent tasks is desired

**Choose skills instead when:**

- The capability extends Claude's knowledge without needing separate context
- No specialized agent persona is needed
- Tool restrictions are sufficient without full agent isolation

**Choose slash commands when:**

- Users need explicit control over when to invoke functionality
- The workflow should be user-initiated, not model-initiated

## Two Approaches to Subagents

### Approach 1: File-Based Agents

Persistent subagent definitions stored as Markdown files.

**Locations (in priority order):**

| Location | Scope | Priority |
|----------|-------|----------|
| `.claude/agents/` | Current project | Highest |
| `~/.claude/agents/` | All projects | Lower |

**File Format:**

```markdown
---
name: agent-name
description: Description of when this agent should be used
tools: Read, Write, Bash, Glob, Grep  # Optional - omit to inherit all
model: sonnet  # Optional - sonnet, opus, haiku, or inherit
permissionMode: default  # Optional - see permission modes below
skills: skill1, skill2  # Optional - skills to auto-load
---

Your agent's system prompt goes here. This defines the agent's
role, capabilities, approach, and constraints.

Include:
- Role definition and expertise areas
- Step-by-step workflow for common tasks
- Constraints and rules to follow
- Output format expectations
- Examples of good behavior
```

### Approach 2: Task Tool Invocation

Dynamic subagent dispatch using the Task tool for on-demand agents.

```
Task(
  subagent_type: "general-purpose",
  model: "opus",
  prompt: <the agent's instructions and task>
)
```

**Built-in subagent_type options:**

| Type | Model | Tools | Purpose |
|------|-------|-------|---------|
| `general-purpose` | Configurable | All | Complex research, multi-step operations |
| `plan` | Sonnet | Read, Glob, Grep, Bash | Codebase research before planning |
| `explore` | Haiku | Read-only | Fast, lightweight searching |

## Configuration Reference

### Required Fields

| Field | Description |
|-------|-------------|
| `name` | Unique identifier (lowercase letters, numbers, hyphens only, max 64 chars) |
| `description` | When the agent should be used (include "PROACTIVELY" for auto-invocation) |

### Optional Fields

| Field | Options | Description |
|-------|---------|-------------|
| `tools` | Comma-separated list | Specific tools to allow. Omit to inherit all. |
| `model` | `sonnet`, `opus`, `haiku`, `inherit` | Model to use. Default: inherit from session. |
| `permissionMode` | See below | How permissions are handled |
| `skills` | Comma-separated list | Skills to auto-load when agent starts |

### Permission Modes

| Mode | Behavior |
|------|----------|
| `default` | Normal permission prompting |
| `acceptEdits` | Auto-accept file edits |
| `bypassPermissions` | Skip all permission prompts |
| `plan` | Planning mode (research only) |
| `ignore` | Ignore this agent |

### Available Tools

**File Operations:** `Read`, `Write`, `Edit`, `Glob`, `Grep`
**Execution:** `Bash`, `BashOutput`
**Web:** `WebFetch`, `WebSearch`
**Specialized:** `Task`, `NotebookEdit`, `TodoWrite`, `Skill`

## Creating a Subagent

### Step 1: Define the Purpose

Answer these questions:

1. What specialized task does this agent handle?
2. What expertise or personality should it have?
3. What tools does it need (or shouldn't have)?
4. Should it be invoked automatically or explicitly?

### Step 2: Choose the Approach

**Use file-based agents when:**
- The agent will be reused across sessions
- Team sharing via version control is desired
- Configuration should persist

**Use Task tool when:**
- One-off or dynamic agent dispatch is needed
- Agents are spawned as part of a workflow
- Parallel agent execution is required

### Step 3: Write the System Prompt

Structure the agent's prompt with these sections:

```markdown
<role>
Define who this agent is and what it excels at.
</role>

<constraints>
<hard-rules>
- ALWAYS do X
- NEVER do Y
</hard-rules>
<preferences>
- Prefer A over B
- Prefer C over D
</preferences>
</constraints>

<workflow>
## How to Approach Tasks

1. **Phase 1**: Description
2. **Phase 2**: Description
3. **Phase 3**: Description
</workflow>

<examples>
Good patterns and anti-patterns.
</examples>
```

### Step 4: Configure Tools and Permissions

**Restrictive (read-only analysis):**
```yaml
tools: Read, Glob, Grep
```

**Standard development:**
```yaml
tools: Read, Write, Edit, Bash, Glob, Grep
```

**Full access (omit tools field):**
```yaml
# tools field omitted - inherits all tools
```

### Step 5: Test and Iterate

1. Invoke the agent with a representative task
2. Observe where it struggles or deviates
3. Update the system prompt with clarifications
4. Add examples of correct behavior
5. Repeat until reliable

## Agent Templates

### Code Reviewer Agent

```markdown
---
name: code-reviewer
description: Expert code review specialist. Use PROACTIVELY after any code changes. Reviews for quality, security, and maintainability.
tools: Read, Glob, Grep, Bash
model: inherit
---

<role>
You are a senior code reviewer ensuring high standards of code quality and security.
</role>

<workflow>
## Review Process

1. **Gather Context**: Run git diff, understand the changes
2. **Analyze Each File**: Check for issues systematically
3. **Prioritize Findings**: Critical > High > Medium > Low
4. **Provide Actionable Feedback**: Specific fixes, not vague suggestions

## Review Checklist

- [ ] Code clarity and readability
- [ ] Proper error handling
- [ ] Security vulnerabilities
- [ ] Test coverage
- [ ] Performance considerations
- [ ] Consistency with existing patterns
</workflow>

<output-format>
Organize feedback by priority:
1. **Critical**: Must fix before merge
2. **High**: Should fix
3. **Medium**: Consider improving
4. **Low**: Nice to have
</output-format>
```

### Debugger Agent

```markdown
---
name: debugger
description: Debugging specialist for errors and unexpected behavior. Use PROACTIVELY when encountering failures, test errors, or bugs.
tools: Read, Edit, Bash, Glob, Grep
---

<role>
You are an expert debugger specializing in root cause analysis.
</role>

<workflow>
## Debugging Protocol

1. **Capture**: Get error message, stack trace, reproduction steps
2. **Hypothesize**: Form theories about root cause
3. **Investigate**: Add logging, trace execution, check state
4. **Isolate**: Find the exact failure point
5. **Fix**: Apply minimal, targeted fix
6. **Verify**: Confirm fix works, no regressions

## Three-Strike Rule

- Strike 1: Targeted fix based on evidence
- Strike 2: Step back, reassess assumptions
- Strike 3: STOP - question the approach entirely
</workflow>

<constraints>
- NEVER fix symptoms without understanding root cause
- ALWAYS reproduce before fixing
- ALWAYS verify fix works
</constraints>
```

### Research Agent

```markdown
---
name: researcher
description: Deep research agent for complex questions requiring multi-source investigation. Use for architectural analysis, refactoring plans, or documentation questions.
tools: Read, Glob, Grep, WebSearch, WebFetch
model: opus
---

<role>
You are a research specialist who finds comprehensive answers through thorough investigation.
</role>

<workflow>
## Research Process

### Phase 1: Plan Investigation
- Identify what needs to be researched
- Map out search strategies
- List relevant code areas

### Phase 2: Deep Exploration
- Search codebase thoroughly
- Read relevant files completely
- Use web search for external docs
- Trace dependencies

### Phase 3: Synthesize
- Cross-reference findings
- Identify patterns and gaps
- Form coherent understanding

### Phase 4: Report
- Direct answer with evidence
- File paths and line numbers
- Confidence level and caveats
- Recommended next steps
</workflow>

<principles>
- Go deep, not shallow
- Cite specific evidence
- Connect dots across sources
- Acknowledge uncertainty
</principles>
```

## Parallel Agent Patterns

### Pattern: Parallel Execution

Dispatch multiple agents simultaneously for independent tasks:

```
Task(
  subagent_type: "general-purpose",
  model: "sonnet",
  prompt: "Task 1: Review authentication module..."
)

Task(
  subagent_type: "general-purpose",
  model: "sonnet",
  prompt: "Task 2: Review authorization module..."
)

Task(
  subagent_type: "general-purpose",
  model: "sonnet",
  prompt: "Task 3: Review session handling..."
)
```

### Pattern: Divergent Exploration (Delphi)

Launch multiple agents with identical prompts for diverse perspectives:

```
# Same prompt to all agents - divergent exploration emerges naturally
identical_prompt = "Investigate why API latency increased..."

Task(subagent_type: "general-purpose", model: "opus", prompt: identical_prompt)
Task(subagent_type: "general-purpose", model: "opus", prompt: identical_prompt)
Task(subagent_type: "general-purpose", model: "opus", prompt: identical_prompt)
```

Each agent explores independently, potentially discovering different clues.

### Pattern: Synthesis After Parallel Work

After parallel agents complete:

```
Task(
  subagent_type: "general-purpose",
  model: "opus",
  prompt: "Read all reports in .reviews/ and synthesize findings..."
)
```

## Resumable Agents

Agents can be resumed to continue previous work:

```
# Initial dispatch
Task(...) -> returns agentId: "abc123"

# Resume later
"Resume agent abc123 and continue analyzing the authorization module"
```

**Use cases:**
- Long-running research across sessions
- Iterative refinement with maintained context
- Multi-step workflows with breaks

## Best Practices

### Prompt Engineering

1. **Be specific about the role**: Define expertise and personality clearly
2. **Include constraints**: Hard rules prevent unwanted behavior
3. **Provide workflow**: Step-by-step process guides execution
4. **Add examples**: Show good and bad patterns
5. **Define output format**: Structure expectations

### Tool Selection

1. **Principle of least privilege**: Only grant needed tools
2. **Read-only for analysis**: Use `Read, Glob, Grep` for review agents
3. **Full access rarely needed**: Most agents don't need all tools
4. **Bash is powerful but risky**: Consider if really needed

### Description Writing

**For automatic invocation**, include trigger phrases:
- "Use PROACTIVELY when..."
- "MUST BE USED for..."
- "Automatically invoke for..."

**For explicit invocation**, be descriptive:
- "Use when user asks to..."
- "Invoke for..."

### Common Anti-Patterns

| Anti-Pattern | Better Approach |
|--------------|-----------------|
| Vague descriptions | Specific trigger conditions |
| Overly long prompts | Progressive disclosure via skills |
| All tools for every agent | Minimal necessary tools |
| Generic "helper" agents | Focused, specialized agents |
| No constraints | Clear hard rules and preferences |

## CLI-Based Agents

Define agents dynamically via command line:

```bash
claude --agents '{
  "quick-review": {
    "description": "Fast code review. Use proactively after changes.",
    "prompt": "You are a quick code reviewer. Focus on obvious issues only.",
    "tools": ["Read", "Grep", "Glob"],
    "model": "haiku"
  }
}'
```

CLI agents have lower priority than file-based project agents but higher than user-level agents.

## Integration with Skills

Agents can auto-load skills:

```yaml
---
name: data-analyst
description: Data analysis specialist
skills: query-builder, visualization
---
```

The specified skills are loaded when the agent starts, giving it access to that specialized knowledge.

## Troubleshooting

### Agent Not Being Invoked

1. Check description includes clear trigger conditions
2. Add "PROACTIVELY" if automatic invocation is desired
3. Verify file is in correct location with correct frontmatter
4. Check for name conflicts with higher-priority agents

### Agent Using Wrong Tools

1. Verify tools field syntax (comma-separated, no brackets)
2. Check tool names are exactly correct (case-sensitive)
3. If tools should inherit, omit the field entirely

### Agent Behaving Incorrectly

1. Add more specific constraints
2. Include examples of correct behavior
3. Add "NEVER" rules for unwanted behaviors
4. Consider if the prompt is too long (move details to skills)

## Quick Reference

**Create project agent:**
```bash
mkdir -p .claude/agents
# Create .claude/agents/my-agent.md with frontmatter
```

**Create user agent:**
```bash
mkdir -p ~/.claude/agents
# Create ~/.claude/agents/my-agent.md with frontmatter
```

**Dispatch via Task:**
```
Task(subagent_type: "general-purpose", model: "opus", prompt: "...")
```

**View/manage agents:**
```
/agents
```
