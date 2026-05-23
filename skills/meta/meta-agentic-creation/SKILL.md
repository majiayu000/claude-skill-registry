---
name: meta-agentic-creation
description: Create meta prompts, meta agents, and meta skills that build other agentic components. Use when scaling agentic layer development, creating generators/templates, or implementing "build the system that builds the system" patterns.
allowed-tools: Read, Grep, Glob, Write
---

# Meta-Agentic Creation

Guide for creating meta-level agentic components that generate other components.

## Core Philosophy

> "Build the system that builds the system. Do not work on the application layer."

Meta agentics provide **multiplicative leverage**:

- Meta Prompt: 1 prompt that creates N prompts
- Meta Agent: 1 agent that creates N agents
- Meta Skill: 1 skill that creates N skills

## The Meta-Agentic Hierarchy

```text
┌─────────────────────────────────────────────────────┐
│ Level 3: Meta-Meta (rarely needed)                  │
│          • Generators that create generators        │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│ Level 2: Meta Components                            │
│          • Meta prompts (prompt generators)         │
│          • Meta agents (agent builders)             │
│          • Meta skills (skill scaffolders)          │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│ Level 1: Standard Components                        │
│          • Domain prompts                           │
│          • Specialized agents                       │
│          • Task-specific skills                     │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│ Level 0: Application Layer                          │
│          • End-user features                        │
│          • Business logic                           │
└─────────────────────────────────────────────────────┘
```

## When to Use

- Scaling agentic layer development (need 4+ similar components)
- Creating generators or templates for prompts/agents/skills
- Implementing "build the system that builds the system" patterns
- Establishing consistent patterns for team/organization
- Onboarding others to agentic component creation
- Maximizing leverage through multiplicative returns

## Meta Prompt Template

A meta prompt is a prompt that generates other prompts.

````markdown
---
description: Generate a {type} prompt for {purpose}
argument-hint: <name> [options...]
---

# Meta Prompt: {Type} Generator

Generate well-structured {type} prompts following established patterns.

## Arguments

- `$1`: Name for the generated prompt (required)
- `$2`: Primary purpose/domain (optional)
- `$ARGUMENTS`: Additional context

## Template Structure

The generated prompt will follow this structure:

### YAML Frontmatter

```yaml
---
description: {Generated based on purpose}
argument-hint: {Appropriate for prompt type}
---
```

### Sections to Include

1. **Purpose**: Clear statement of what prompt does
2. **Arguments**: Input parameters with defaults
3. **Workflow**: Step-by-step instructions
4. **Output Format**: Expected deliverable structure
5. **Notes**: Important considerations

## Generation Rules

1. Use imperative mood ("Do X", not "You should do X")
2. Include concrete examples
3. Specify output format explicitly
4. Add validation/verification steps
5. Keep under {line_limit} lines

## Output

Write the generated prompt to: `.claude/commands/{name}.md`

Report:

- Generated prompt name
- Location
- Key sections included
````

## Meta Agent Template

A meta agent creates other agents.

````markdown
---
name: meta-agent
description: Create new specialized agents following established patterns and best practices.
tools: Read, Write, Glob, Grep
model: opus
---

# Meta Agent: Agent Builder

Create well-structured agents following Claude Code patterns.

## Input Requirements

When invoked, expect:

- Agent name (kebab-case)
- Agent purpose (1-2 sentences)
- Required tools (list)
- Model preference (opus|sonnet|haiku)
- Domain context

## Agent Template

```yaml
---
name: {agent-name}
description: {Purpose description under 200 chars}
tools: {Tool1, Tool2, ...}
model: {opus|sonnet|haiku}
---

# {Agent Name}

{Detailed purpose and when to use this agent}

## Capabilities

- Capability 1
- Capability 2

## Workflow

### Step 1: {First Step}
{Instructions}

### Step 2: {Second Step}
{Instructions}

## Output Format

{Expected output structure}

## Constraints

- Constraint 1
- Constraint 2
```

## Generation Workflow

1. **Analyze Request**: Understand agent purpose
2. **Select Tools**: Choose minimal required tools
3. **Choose Model**:
   - haiku: Simple, fast tasks
   - sonnet: Balanced reasoning
   - opus: Complex, critical tasks
4. **Design Workflow**: Create step-by-step process
5. **Write Agent**: Generate agent file
6. **Register**: Update plugin.json if needed

## Validation

Before completing:

- [ ] Description under 200 characters
- [ ] Tools are minimal and appropriate
- [ ] Model matches task complexity
- [ ] Workflow is complete and actionable
````

## Meta Skill Template

A meta skill creates other skills.

````markdown
---
name: meta-skill
description: Create new skills following Claude Code patterns with proper YAML frontmatter, structure, and documentation.
version: 1.0.0
allowed-tools: Read, Write, Glob, Grep
tags: [meta, skill, generator, scaffolder]
---

# Meta Skill: Skill Generator

Create well-structured skills following established patterns.

## Skill Template

```yaml
---
name: {skill-name}
description: {Clear description of what skill does and when to use it}
version: 1.0.0
allowed-tools: {Tool1, Tool2, ...}
tags: [{tag1}, {tag2}, ...]
---

# {Skill Name}

{Introduction and purpose}

## When to Use

- Use case 1
- Use case 2

## Key Concepts

### Concept 1
{Explanation}

### Concept 2
{Explanation}

## Patterns

### Pattern Name
{Description and example}

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
| --- | --- | --- |
| ... | ... | ... |

## Related Skills

- `skill-1`: Relationship
- `skill-2`: Relationship
```

## Skill Generation Rules

1. **Naming**: Use noun-phrases (kebab-case)
2. **Description**: Under 200 chars, starts with action verb
3. **Tags**: 4-8 relevant keywords
4. **Tools**: Minimal set needed
5. **Structure**: Consistent sections

## Directory Structure

```text
skills/{skill-name}/
  SKILL.md           # Main skill file
  references/        # Optional supporting docs
  scripts/           # Optional automation
```
````

## Creating Meta Components

### Step 1: Identify the Pattern

Before creating a meta component, identify:

1. What components will it generate?
2. What's the common structure?
3. What varies between instances?
4. What validation is needed?

### Step 2: Design the Template

The template should:

- Capture the invariant structure
- Mark variable sections clearly
- Include validation rules
- Provide examples

### Step 3: Build the Generator

The generator should:

- Parse input parameters
- Apply template with variables
- Validate output
- Write to correct location

### Step 4: Test Generation

Validate by:

1. Generate a simple component
2. Generate a complex component
3. Test edge cases
4. Verify all outputs are valid

## When to Create Meta Components

| Situation | Create Meta? | Reason |
| --- | --- | --- |
| Need 1 component | No | Direct creation faster |
| Need 2-3 similar | Maybe | Depends on complexity |
| Need 4+ similar | Yes | Meta pays off |
| Establishing patterns | Yes | Encodes best practices |
| Onboarding others | Yes | Ensures consistency |

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
| --- | --- | --- |
| Over-abstraction | Meta-meta-meta | Stop at 2 levels |
| Rigid templates | Can't handle variations | Build in flexibility |
| No examples | Users don't understand | Include concrete examples |
| No validation | Bad outputs generated | Always validate results |

## Real-World Meta Components

### From agent-experts Repository

```text
.claude/commands/meta_prompt.md    # Creates new prompts
.claude/agents/meta-agent.md       # Creates new agents
.claude/skills/meta-skill/SKILL.md # Creates new skills
```

### TAC Plugin Examples

```text
tac/agents/prompt-generator.md     # Generates prompts
tac/agents/agent-builder.md        # Builds agents
tac/skills/tool-design/SKILL.md    # Designs tools
```

## Leverage Calculation

Meta components provide multiplicative returns:

```text
Without meta:
  10 agents × 30 min each = 300 minutes

With meta:
  1 meta-agent × 60 min + 10 generations × 5 min = 110 minutes

Savings: 63%
```

The more components you need, the more meta pays off.

## Related Skills

- `agent-expert-creation`: Self-improving experts
- `template-meta-prompt-creation`: Level 6 prompts
- `prompt-level-selection`: Choosing prompt complexity

---

**Last Updated:** 2025-12-15

## Version History

- **v1.0.0** (2025-12-26): Initial release

---
