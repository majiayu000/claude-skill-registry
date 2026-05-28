---
name: ref-development-standards
description: Core development principles for Plan-Marshall projects - when to ask users, research best practices, tool usage, and dependency management
user-invocable: false
allowed-tools:
standards:
  - standards/general-development-rules.md
  - standards/file-operations.md
  - standards/search-operations.md
  - standards/tool-usage-patterns.md
---

# CUI General Development Rules

Foundational development principles that guide all work in CUI projects.

## What This Skill Provides

### Core Development Principles
- **User Interaction Guidelines** - When to ask vs when to proceed
- **Research Requirements** - Using research-best-practices agent for finding current best practices
- **Tool Usage Standards** - Proper tools for file operations (Read, Write, Edit vs cat, tail, find)
- **Document Management** - When to create vs reuse documents
- **Dependency Management** - Approval requirements for adding dependencies

### Cross-Cutting Standards

This skill provides the foundational rules that apply across ALL development activities:
- Agent development
- Command development
- Code implementation
- Documentation creation
- Testing strategies

## When to Activate This Skill

Activate this skill when:

**Starting any development work:**
- Creating new agents or commands
- Implementing features
- Writing documentation
- Making architectural decisions

**Uncertain about approach:**
- Unsure whether to ask user or proceed
- Need to research current best practices
- Choosing between different implementation approaches

**Tool selection:**
- Deciding which tools to use for file operations
- Implementing file discovery or content search
- Working with file system operations

**Project decisions:**
- Adding new dependencies
- Creating new documentation
- Proliferating new files or structures

## Workflow

### Step 1: Load Core Development Rules

**Load the complete set of development principles:**

```
Read: standards/general-development-rules.md
```

This provides:
- Decision tree for when to ask users
- Research best practices using research-best-practices agent
- Tool usage standards (references ref-development-standards skill)
- Document proliferation guidelines
- Dependency approval requirements

### Step 2: Apply Rules Throughout Development

**During development, follow these principles:**

1. **When uncertain** - Ask the user (don't guess or be creative)
2. **When researching** - Use research-best-practices agent for current best practices
3. **When performing file operations** - Use proper tools (Read, Write, Edit, Glob, Grep)
4. **When creating documents** - Check if context-relevant documents exist first
5. **When adding dependencies** - Always get user approval

### Step 3: Reference Related Skills

**For specific areas, reference specialized skills:**

**Tool Usage Patterns:**
```
Skill: plan-marshall:ref-development-standards
```
- Detailed file operation patterns
- Non-prompting tool usage
- Error handling strategies

**Research Execution:**
```
Task: plan-marshall:research-best-practices
```
- Comprehensive web research
- Finding current best practices for technologies/frameworks

## Standards Organization

```
standards/
  general-development-rules.md  # Core principles for all development work
  file-operations.md            # File operation patterns (merged from diagnostic-patterns)
  search-operations.md          # Search operation patterns (merged from diagnostic-patterns)
  tool-usage-patterns.md        # Tool usage patterns (merged from diagnostic-patterns)
```

**Consolidated structure:**
- Core development rules plus detailed tool usage patterns
- All patterns now in one skill for easier reference
- Delegates to research-best-practices agent for research

## Tool Access

**No special tools required** - This skill uses standard Read tool to load standards.

**For research:** Delegates to research-best-practices agent (has WebSearch, WebFetch)
**For tool patterns:** References ref-development-standards skill

## Usage Examples

### Example 1: Starting Feature Implementation

```markdown
## Step 0: Load Development Guidelines

```
Skill: plan-marshall:ref-development-standards
```

This loads core development principles including when to ask users, research requirements, and tool usage standards.

## Step 1: Research Best Practices

Before implementing, research current best practices:

```
Task:
  subagent_type: plan-marshall:research-best-practices
  prompt: Research best practices for {feature/technology}
```
```

### Example 2: Creating New Agent

```markdown
## Step 1: Load Development Rules

```
Skill: plan-marshall:ref-development-standards
```

This ensures I follow core principles for tool usage, asking users when uncertain, and proper file operations.

## Step 2: Load Tool Usage Patterns

For detailed file operation patterns:

```
Skill: plan-marshall:ref-development-standards
```
```

### Example 3: Uncertain About Approach

```markdown
## Applying General Development Rules

Following general-development-rules principle: "If in doubt, ask the user."

I need clarification on: {specific question}

[Ask user for guidance before proceeding]
```

## Integration with plan-marshall Bundle

This skill integrates with other plan-marshall components:

### Agents
- **research-best-practices** - This skill delegates research to this agent for finding current best practices

### Skills
- **ref-development-standards** - This skill references ref-development-standards for detailed tool usage patterns

### Commands
- All commands should follow these general development rules
- Commands that need research should delegate to research-best-practices agent

## Key Principles

### 1. Ask When In Doubt
Never guess or be creative. If uncertain, ask the user for guidance.

### 2. Research Current Best Practices
Always use research-best-practices agent to find latest best practices for technologies/frameworks. Don't rely on outdated knowledge.

### 3. Use Proper Tools
Use Read, Write, Edit, Glob, Grep (not cat, tail, find, test via Bash). See ref-development-standards skill for details.

### 4. Don't Proliferate Documents
Use context-relevant existing documents. Only create new documents with user approval.

### 5. Get Dependency Approval
Never add dependencies without user approval. Always ask first.

## Quality Verification

Standards in this skill ensure:

- [x] Self-contained (no external references except to other skills/agents)
- [x] Clear decision guidance for common scenarios
- [x] Proper delegation to specialized skills (ref-development-standards)
- [x] Proper delegation to specialized agents (research-best-practices)
- [x] Simple, focused structure (single standards file)
- [x] Cross-cutting applicability to all development work

## References

- research-best-practices agent - For comprehensive web research and finding current best practices
- ref-development-standards skill - For detailed tool usage patterns and non-prompting file operations
