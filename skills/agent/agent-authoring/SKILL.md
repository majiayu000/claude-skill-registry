---
name: agent-authoring
description: Guide for authoring specialized AI agents. Use when creating, updating, or improving agents, choosing models, defining focus areas, configuring tools, or learning agent best practices.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - AskUserQuestion
# model: inherit
---

## Reference Files

Advanced agent authoring guidance:

- [design-patterns.md](design-patterns.md) - Proven agent patterns with examples
- [examples.md](examples.md) - Complete agent examples with analysis
- [agent-decision-guide.md](agent-decision-guide.md) - Deciding when to use agents vs skills vs commands
- [comparison-with-official.md](comparison-with-official.md) - Comparison with Anthropic's official agents

---

## About Agents

Agents are specialized AI assistants that run in separate subprocesses with focused expertise. They have:

- **Specific focus areas** - Clearly defined areas of expertise
- **Model choice** - Sonnet, Opus, or Haiku depending on complexity
- **Tool restrictions** - Limited to only the tools they need
- **Permission modes** - Control over how they interact with the system
- **Isolated context** - Run separately from the main conversation

**When to use agents**:

- Task requires specialized expertise
- Need different model than main conversation
- Want to restrict tools for security/focus
- Task benefits from isolated context
- Can be invoked automatically or manually

## Core Principles

### 1. Clear Focus Areas

Focus areas define what the agent is expert in. They should be:

**Specific, not generic**:

- ❌ "Python programming"
- ✅ "FastAPI REST APIs with SQLAlchemy ORM and pytest testing"

**Concrete, with examples**:

- ❌ "Best practices"
- ✅ "Defensive programming with strict error handling"

**5-15 focus areas** that cover the agent's expertise comprehensively.

**Example from evaluator agent**:

```markdown
## Focus Areas

- YAML Frontmatter Validation
- Markdown Structure
- Tool Permissions
- Description Quality
- File Organization
- Progressive Disclosure
- Integration Patterns
```

### 2. Model Selection (Keep It Simple)

**Sonnet** (default choice for most agents):

- Balanced cost and capability
- Handles most programming tasks
- Good for analysis and code generation
- Use unless you have a specific reason not to

**Haiku** (for simple, fast tasks):

- Fast and cheap
- Good for read-only analysis
- Simple, repetitive tasks
- When speed matters more than complexity

**Opus** (for complex reasoning):

- Most capable model
- Complex architectural decisions
- Requires deep reasoning
- Higher cost - use sparingly

**Decision guide**:

1. Start with Sonnet
2. Switch to Haiku if agent is simple read-only analyzer
3. Only use Opus if task genuinely requires highest capability

### 3. Tool Restrictions

**Why restrict tools**:

- **Security** - Prevent unwanted file modifications
- **Focus** - Agent only needs specific capabilities
- **Predictability** - Clear what agent can/cannot do

**Common tool patterns**:

**Read-only analyzer**:

```yaml
allowed_tools:
  - Read
  - Glob
  - Grep
  - Bash
```

Examples: evaluator, audit-skill

**Code generator/modifier**:

```yaml
allowed_tools:
  - Read
  - Edit
  - Write
  - Grep
  - Glob
  - Bash
```

Examples: test-runner

**Minimal/focused**:

```yaml
allowed_tools:
  - Read
  - AskUserQuestion
```

Example: When agent only needs to read and ask questions

**If unspecified**: Agent inherits all tools from parent (usually not desired)

### 4. Permission Modes (Common Ones)

**default** (most common):

- Normal permission checking
- User approves tool usage as needed
- Safe default choice

**acceptEdits** (for editing workflows):

- Auto-approves Read and Edit operations
- Good for refactoring/cleanup agents
- Still asks for Write, Bash, etc.

**plan** (for planning agents):

- Agent researches and creates plan
- No execution until plan approved
- Good for complex implementation planning

**Most agents use default** - only use others when you have a specific workflow need.

### 5. Agent Hooks

Agent hooks are lifecycle hooks defined in YAML frontmatter, scoped to that specific agent.

**When to use agent hooks**:

- Agent needs specific validation before tool execution
- Auto-format or lint files after agent edits
- Log or notify when agent completes tasks
- Need behavior specific to one agent, not global

**When to use settings.json hooks instead**:

- Behavior applies to all sessions/agents
- Need events like SessionStart, SubagentStart, UserPromptSubmit
- Global validation or formatting rules

**Available events**:

| Event         | Trigger                | Use Case                      |
| ------------- | ---------------------- | ----------------------------- |
| `PreToolUse`  | Before agent uses tool | Validation, blocking, logging |
| `PostToolUse` | After tool completes   | Formatting, notifications     |
| `Stop`        | Agent finishes         | Cleanup, notifications        |

**Configuration syntax**:

```yaml
---
name: code-reviewer
description: Review code with automatic linting
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-command.sh"
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "./scripts/run-linter.sh"
          timeout: 10
---
```

**Key points**:

- **Matchers** filter which tools trigger hooks (`"Edit|Write"`, `"Bash"`, `"*"`)
- **Stop** event auto-converts to SubagentStop internally
- Hooks run with user credentials (same security model as settings.json)
- Keep hook scripts fast (<30s timeout recommended)

## Agent Design Patterns

Three proven patterns for building effective agents. Each pattern includes complete templates you can copy and customize.

**📄 See [design-patterns.md](design-patterns.md) for detailed templates**

**Quick overview**:

1. **Read-Only Analyzer** - For auditing, evaluation, reporting (Haiku/Sonnet + read-only tools)
2. **Code Generator/Modifier** - For creating/editing code (Sonnet + Read/Edit/Write/Bash)
3. **Workflow Orchestrator** - For multi-step coordination (Sonnet + Task tool)

## Resource Organization

### File Structure

Per Claude Code specification, agents are **single files only**:

```text
agents/
├── code-reviewer.md           # Single file agent
├── bash-expert.md             # Single file agent
└── security-auditor.md        # Single file agent
```

**No subdirectories or reference files supported.**

### Agent vs Skill

| Need                                     | Use                           |
| ---------------------------------------- | ----------------------------- |
| Reference files / progressive disclosure | **Skill**                     |
| Single-file focused capability           | **Agent**                     |
| Large documentation (>500 lines)         | **Skill** (can split content) |

**If you need reference files**, convert to a skill instead:

```text
skills/evaluator/
├── SKILL.md                   # Main skill file
├── evaluation-criteria.md     # Reference file
└── examples.md                # Reference file
```

**📄 See `~/.claude/docs/agent-vs-skill-structure.md` for details**

### Keeping Agents Focused

Since agents must be single files:

- Keep content under 500 lines
- Focus on core workflow, not extensive examples
- Move reference material to skills if needed
- Use clear, concise sections

## Agent Creation Process

### Step 1: Define Purpose and Scope

Start by clarifying:

**Questions to ask**:

- What specific problem does this agent solve?
- What tasks should it handle?
- What tasks should it NOT handle?
- Who will use it and when?
- Does an existing agent already do this?

**Use AskUserQuestion** to clarify ambiguities before proceeding.

**Check for existing agents**:

`ls -la ~/.claude/agents/`

Look for similar agents that might overlap.

### Step 2: Choose Model and Tools

**Model selection**:

1. Default to Sonnet for most agents
2. Use Haiku if it's a simple read-only analyzer
3. Only use Opus if complexity genuinely requires it

**Tool selection**:

1. List what the agent actually needs to do
2. Map needs to minimal tool set
3. Use restrictive set from design patterns above
4. Don't grant tools "just in case"

**Permission mode**:

- Default: Use `default` unless you have specific need
- Only specify permissionMode if you need non-default behavior

### Step 3: Write Focus Areas

**Guidelines**:

- 5-15 specific areas of expertise
- Each should be concrete and specific
- Include technologies, frameworks, patterns
- Avoid vague statements like "best practices"

**Good examples** (from evaluator):

- "YAML Frontmatter Validation - Required fields, syntax correctness"
- "Tool Permissions - Appropriateness of allowed-tools, security implications"
- "Progressive Disclosure - Context economy, reference file usage"

**Bad examples**:

- "Writing good code" (too vague)
- "Programming" (too generic)
- "Helping with tasks" (not specific)

### Step 4: Define Approach/Methodology

This section explains HOW the agent works:

**Include**:

- Key principles the agent follows
- Step-by-step methodology
- Decision-making frameworks
- Output format (if applicable)

**Example from evaluator**:

```markdown
## Evaluation Framework

### Correctness Criteria

- YAML frontmatter with required fields
- Valid model value
- Name matches filename
  ...

## Evaluation Process

### Step 1: Identify Extension Type

...

### Step 2: Apply Type-Specific Validation

...
```

### Step 5: Write Description

**Requirements**:

- Explain what the agent does (capabilities)
- Include when to invoke (triggering scenarios)
- Mention key technologies/focus areas
- Target 150-500 characters

**Formula**: `[What it does] for [use cases]. Expert/Use when [triggers]. [Key features]`

**Good example**:

```yaml
description: Master of defensive Bash scripting for production automation, CI/CD pipelines, and system utilities. Expert in safe, portable, and testable shell scripts.
```

**Bad example**:

```yaml
description: Helps with bash scripts
```

### Step 6: Create the Agent File

**File location**: `~/.claude/agents/agent-name.md`

**Filename should match name** in frontmatter.

**Basic structure**:

```markdown
---
name: agent-name
description: [comprehensive description with triggers]
model: sonnet
allowed_tools:
  - Read
  - [other tools]
---

## Focus Areas

- [Specific area 1]
- [Specific area 2]
  ...

## Approach

[How the agent works, methodologies, processes]

## [Optional Additional Sections]

[Examples, best practices, output formats, etc.]
```

### Step 7: Test the Agent

**Test invocation**:

1. Try invoking the agent in a conversation
2. Verify it has access to specified tools
3. Check that focus areas guide its behavior
4. Ensure description triggers correctly

**Validate with /audit-agent**:

```text
/audit-agent agent-name
```

This will check:

- Frontmatter correctness
- Description quality
- File structure
- Best practices compliance

## Agents vs Skills vs Commands

Choosing the right customization type is critical. Each has distinct characteristics and use cases.

**📄 See [agent-decision-guide.md](agent-decision-guide.md) for agent-specific decision framework**

**📄 See [when-to-use-what.md](../../references/when-to-use-what.md) for detailed decision guide (shared)**

**Quick guide**:

- **Agent** - Separate subprocess, custom model, strict tools → Use for isolation and specialized tasks
- **Skill** - Main conversation, auto-triggers, domain knowledge → Use for extending base capabilities
- **Command** - User shortcut, delegates to agent/skill → Use for explicit, frequent actions

## Common Mistakes to Avoid

1. **Vague focus areas** - "Python expert" instead of "FastAPI with SQLAlchemy and pytest"
2. **Wrong model** - Using Opus when Sonnet would work fine
3. **Too permissive tools** - Granting all tools when only Read/Grep needed
4. **Missing approach section** - Not explaining HOW the agent works
5. **Poor description** - Too short or doesn't include trigger scenarios
6. **Name mismatch** - Frontmatter name doesn't match filename
7. **Overlapping agents** - Creating agent that duplicates existing one
8. **No tool restrictions** - Not specifying allowed_tools (inherits all)

## Examples from Existing Agents

Real-world examples showing what makes a good agent. Each example is analyzed to explain why it works well.

**📄 See [examples.md](examples.md) for detailed analysis**

**Examples covered**:

1. **evaluator** - Read-only evaluator pattern
2. **test-runner** - Test runner with reporting pattern

Each example includes the full frontmatter, focus areas, and analysis of what makes it effective.

## Tips for Success

1. **Start with an existing agent as template** - Copy structure from similar agent
2. **Be specific in focus areas** - Concrete details over generic statements
3. **Test early** - Create minimal agent and test before adding details
4. **Use /audit-agent** - Catch issues early
5. **Check for overlaps** - Don't duplicate existing agents
6. **Document the approach** - Explain HOW the agent works
7. **Keep tools minimal** - Only grant what's needed
8. **Write good description** - Include what, when, and key features
9. **Iterate based on usage** - Refine after real-world testing
10. **Follow naming conventions** - Use kebab-case, match filename to name

## Reference to Standards

For detailed standards and validation:

- **Naming conventions** - Use kebab-case for agent names
- **Frontmatter requirements** - name, description, model (optional: allowed_tools, permissionMode)
- **File organization** - `~/.claude/agents/agent-name.md`
- **Validation** - Use `/audit-agent` command

See `audit-coordinator` skill for comprehensive standards.

## Related Skills

This skill is part of the authoring skill family:

- **author-agent** - Guide for creating agents (this skill)
- **author-skill** - Guide for creating skills
- **author-command** - Guide for creating commands
- **author-output-style** - Guide for creating output styles

For validation, use the corresponding audit skills:

- **audit-agent** - Validate agent configurations
- **audit-coordinator** - Comprehensive multi-faceted audits

## Quick Start Checklist

Creating a new agent:

- [ ] Identify unique purpose (not covered by existing agents)
- [ ] Choose model (default: Sonnet)
- [ ] Determine minimal tool set needed
- [ ] Write 5-15 specific focus areas
- [ ] Document approach/methodology
- [ ] Write comprehensive description (150-500 chars)
- [ ] Create file at `~/.claude/agents/agent-name.md`
- [ ] Test invocation
- [ ] Validate with `/audit-agent agent-name`
- [ ] Iterate based on results
