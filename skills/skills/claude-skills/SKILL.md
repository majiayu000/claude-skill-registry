---
name: claude-skills
description: Guide for creating Agent Skills with progressive disclosure and best practices. Use when creating new skills, understanding skill structure, or implementing progressive disclosure.
---

# Agent Skills

Comprehensive guide for creating modular, self-contained Agent Skills that extend Claude's capabilities with specialized knowledge.

## What Are Agent Skills?

Agent Skills are organized directories containing instructions, scripts, and resources that Claude can dynamically discover and load. They enable a single general-purpose agent to gain domain-specific expertise without requiring separate custom agents for each use case.

### Key Concepts

- **Modularity**: Self-contained packages that can be mixed and matched
- **Reusability**: Share and distribute expertise across projects and teams
- **Progressive Disclosure**: Load context only when needed, keeping interactions efficient
- **Specialization**: Deep domain knowledge without sacrificing generality

## How Skills Work

Skills operate on a principle of progressive disclosure across multiple levels:

### Level 1: Discovery
Agent system prompts include only skill names and descriptions, allowing Claude to decide when each skill is relevant based on the task at hand.

### Level 2: Activation
When Claude determines a skill applies, it loads the full `SKILL.md` file into context, gaining access to the complete procedural knowledge and guidelines.

### Level 3+: Deep Context
Additional bundled files (like references, forms, or documentation) load only when needed for specific scenarios, keeping token usage efficient.

This tiered approach maintains efficient context windows while supporting potentially unbounded skill complexity.

## Skill Structure

### Minimal Requirements

Every skill must have:

```
skill-name/
└── SKILL.md
```

### Complete Structure

More complex skills can include additional resources:

```
skill-name/
├── SKILL.md           # Required: Core skill definition
├── scripts/           # Optional: Executable code for deterministic tasks
├── references/        # Optional: Documentation loaded on-demand
└── assets/            # Optional: Templates, images, boilerplate
```

## SKILL.md Format

Each `SKILL.md` file must begin with YAML frontmatter followed by Markdown content:

```markdown
---
name: skill-name
description: Concise explanation of when Claude should use this skill
license: MIT
---

# Skill Name

Main instructional content goes here...
```

### Required YAML Properties

- `name`:
   Hyphen-case identifier matching directory name (lowercase alphanumeric and hyphens only, max 64 characters)
   Maximum 64 characters
   Must contain only lowercase letters, numbers, and hyphens
   Cannot contain XML tags
   Cannot contain reserved words: "anthropic", "claude"
- `description`: 
   Explains the skill's purpose and when Claude should utilize it
   Must be non-empty
   Maximum 1024 characters
   Cannot contain XML tags
   The description should include both what the Skill does and when Claude should use it. For complete authoring guidance, see the best practices guide.



**Description Constraints** (from Anthropic best-practices):
- Maximum 1024 characters
- Must use third person (not "I can help you" or "You can use this")
- Must include both **what it does** AND **when to use it**
- Use pattern: `[What it does]. Use when [trigger conditions].`

> **Critical**: The `description` is the ONLY text Claude sees during skill discovery (Level 1).
> The body's "When to Use" section only loads AFTER activation (Level 2) and cannot trigger it.
> All activation triggers must be in the description.


### Optional YAML Properties

- `license`: License name or filename reference
- `allowed-tools`: Pre-approved tools list (Claude Code support only)
- `metadata`: Key-value string pairs for client-specific properties

### Markdown Body

The content section has no restrictions and should contain:

- When to activate the skill
- Core procedural knowledge
- Best practices and guidelines
- Examples and patterns
- References to additional resources (if any)

## Creating Skills: Seven-Step Workflow

### 1. Understanding Through Examples

Gather concrete use cases to clarify what the skill should support. Real-world examples reveal actual needs better than theoretical requirements.

**Example:**
```
Use Case: Help developers follow Git best practices
Examples:
- Creating conventional commit messages
- Rebasing feature branches
- Resolving merge conflicts
- Creating descriptive branch names
```

### 2. Planning Resources

Analyze examples to identify needed components:

- **Scripts**: For tasks requiring deterministic reliability or that would need repeated rewriting
- **References**: Documentation to load into context as needed
- **Assets**: Output files like templates or boilerplate (not loaded into context)

**Example:**
```
Git skill resources:
- scripts/analyze-commit.sh - Parse git diff for commit message
- references/conventional-commits.md - Detailed commit format spec
- assets/gitignore-templates/ - Common .gitignore files
```

### 3. Initialization

Create the skill directory structure with the required `SKILL.md` file. Ensure the directory name matches the `name` property exactly.

```bash
mkdir -p my-skill/{scripts,references,assets}
touch my-skill/SKILL.md
```

### 4. Editing

Develop resource files and update `SKILL.md` with:
- Purpose and activation criteria
- Usage guidelines and best practices
- Implementation details and examples
- References to supplementary files

**Use imperative/infinitive form** rather than second-person instruction for clarity.

✅ Good: "Follow the Conventional Commits specification"
✅ Good: "Use descriptive branch names with type prefixes"
❌ Avoid: "You should try to use descriptive names when possible"

Keep core procedural information in `SKILL.md` and detailed reference material in separate files.

### 5. Documentation

**Document all sources in the plugin's `sources.md`**. For each skill created, record:
- URLs of documentation, guides, and references used
- Purpose of each source
- Key topics and concepts extracted
- Date accessed (if relevant)

This maintains traceability and helps others understand the skill's foundation.

### 6. Validation

Test the skill with representative scenarios to ensure:
- Claude activates it appropriately
- Instructions are clear and actionable
- Progressive disclosure works effectively
- Token usage remains efficient

### 7. Iteration

Refine based on real-world usage feedback. Monitor how Claude actually uses the skill and adjust the description and content accordingly.

## Best Practices

### Start with Evaluation

Identify specific capability gaps by testing agents on representative tasks. Build skills incrementally to address actual shortcomings rather than anticipated needs.

### Structure for Scale

Split unwieldy `SKILL.md` files into separate referenced documents:
- Keep commonly-used contexts together
- Separate mutually exclusive information to reduce token usage
- Use progressive disclosure to load details only when needed

**Example:**
```markdown
# Git Skill

For detailed conventional commit format, see references/conventional-commits.md
For rebase workflow, see references/rebasing-guide.md
```

### Consider Claude's Perspective

The skill name and description heavily influence when Claude activates it. Pay particular attention to:

- **Name**: Should be clear and reflect the domain (e.g., `git-operations`, `elixir-phoenix`)
- **Description**: Should specify both what the skill does and when to use it

> **Critical**: The `description` is the ONLY text Claude sees during skill discovery (Level 1).
> The body's "When to Use" section only loads AFTER activation (Level 2) and cannot trigger it.
> All activation triggers must be in the description using patterns like "Use when [scenarios]".

**Examples:**

✅ Good Description:
```yaml
description: Guide for Git operations including commits, branches, rebasing, and conflict resolution. Use when working with version control or the user mentions git, commits, or branches.
```

❌ Too Vague:
```yaml
description: Helps with Git
```

❌ Missing "Use when" triggers:
```yaml
description: Guide for Git operations including commits, branches, rebasing, and conflict resolution
```

Monitor real usage patterns and iterate based on actual behavior.

### Iterate Collaboratively

Work with Claude to capture successful approaches and common mistakes into reusable skill components. Ask Claude to self-reflect on what contextual information actually matters.

### Write for AI Consumption

Use clear, imperative language that Claude can follow:

✅ Good:
- "Follow the Conventional Commits specification"
- "Use descriptive branch names with type prefixes"
- "Run tests before committing"

❌ Avoid:
- "You should try to use descriptive names when possible"
- "It might be good to run tests"
- "Consider following best practices"

Include concrete examples wherever possible to illustrate patterns and approaches.

### Security Considerations

Install skills only from trusted sources. When evaluating unfamiliar skills:
- Thoroughly audit bundled files and scripts
- Review code dependencies
- Examine instructions directing Claude to connect with external services
- Verify the skill doesn't request sensitive information or dangerous operations

## Anti-Fabrication Requirements

All skills MUST adhere to strict anti-fabrication requirements to ensure factual, measurable content.

### Core Principles

- Base all outputs on actual analysis of real data using tool execution
- Execute Read, Glob, Bash, or other validation tools before making claims
- Mark uncertain information as "requires analysis", "needs validation", or "requires investigation"
- Use precise, factual language without superlatives or unsubstantiated performance claims
- Execute tests before marking tasks complete and report actual results
- Validate integration recommendations through actual framework detection using tool analysis

### Prohibited Language and Claims

- **Superlatives**: Avoid "excellent", "comprehensive", "advanced", "optimal", "perfect"
- **Unsubstantiated Metrics**: Never fabricate percentages, success rates, or performance numbers
- **Assumed Capabilities**: Don't claim features exist without tool verification
- **Generic Claims**: Replace vague statements with specific, measurable observations
- **Fabricated Testing**: Never report test results without actual execution

### Time and Effort Estimation Rule

- Never provide time estimates, effort estimates, or completion timelines without actual measurement or analysis
- If estimates are requested, execute tools to analyze scope (e.g., count files, measure complexity, assess dependencies) before providing data-backed estimates
- When estimates cannot be measured, explicitly state "timeline requires analysis of [specific factors]"
- Avoid fabricated scheduling language like "15 minutes", "2 hours", "quick task" without factual basis

### Validation Requirements

- **File Claims**: Use Read or Glob tools before claiming files exist or contain specific content
- **System Integration**: Use Bash or appropriate tools to verify system capabilities
- **Framework Detection**: Execute actual detection logic before claiming framework presence
- **Test Results**: Only report test outcomes after actual execution with tool verification
- **Performance Claims**: Base any performance statements on actual measurement or analysis

## Skill Examples

### Simple Skill (Git)

```markdown
---
name: git
description: Guide for Git operations including commits, branches, rebasing, and conflict resolution
license: MIT
---

# Git Operations

## When to Use

Activate when:
- Creating commit messages
- Managing branches
- Resolving conflicts
- Rebasing or merging

## Conventional Commits

Follow the format: `type(scope): description`

Types: feat, fix, docs, style, refactor, test, chore

Example: `feat(auth): add OAuth2 login support`

## Branch Naming

Use format: `type/description`

Examples:
- `feature/user-authentication`
- `fix/memory-leak`
- `docs/api-reference`

## Rebasing Workflow

1. Update main: `git checkout main && git pull`
2. Rebase feature: `git checkout feature-branch && git rebase main`
3. Resolve conflicts if needed
4. Force push: `git push --force-with-lease`
```

### Complex Skill (Phoenix)

```markdown
---
name: phoenix
description: Guide for building Phoenix web applications with LiveView, contexts, and best practices
license: MIT
---

# Phoenix Framework

## When to Use

Activate for:
- Phoenix application development
- LiveView implementations
- Context design
- Channel setup

## Project Structure

Phoenix apps follow:
```
lib/
├── my_app/          # Business logic (contexts)
├── my_app_web/      # Web interface
└── my_app.ex
```

## Contexts

Group related functionality:

```elixir
defmodule MyApp.Accounts do
  def list_users, do: Repo.all(User)
  def get_user!(id), do: Repo.get!(User, id)
  def create_user(attrs), do: ...
end
```

For detailed context patterns, see references/contexts.md

## LiveView

For real-time interfaces, see references/liveview-guide.md
```

## Common Pitfalls

### Too Generic

❌ Avoid:
```yaml
name: programming
description: Helps with programming
```

✅ Better:
```yaml
name: elixir-phoenix
description: Guide for building Phoenix web applications with LiveView, contexts, and Elixir best practices
```

### Too Much in SKILL.md

❌ Avoid putting entire API reference in SKILL.md

✅ Better: Keep core patterns in SKILL.md, detailed reference in `references/`

### Missing Activation Criteria

❌ Avoid:
```markdown
# My Skill

This skill helps with stuff.
```

✅ Better:
```markdown
# My Skill

## When to Use

Activate when:
- Specific scenario 1
- Specific scenario 2
- Specific scenario 3
```

## References

claude-skills/
└── templates/
    └── level1.md (example skill metadata)
    └── level2.md (example skill body)
    └── level3.md (example skill folder structure)
    └── skill.md (example basic skill)

For more information:
- **Agent Skills Blog**: https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- **Example Skills**: https://github.com/anthropics/skills
- **Skills Cookbook**: https://github.com/anthropics/claude-cookbooks/tree/main/skills
- **Skill Creator Guide**: https://github.com/anthropics/skills/blob/main/skill-creator/SKILL.md
- **Agent Skills Specification**: https://github.com/anthropics/skills/blob/main/agent_skills_spec.md
