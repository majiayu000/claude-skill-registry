---
name: claude-prompt-guide
description: Anthropic official XML tag patterns and prompt engineering best practices. Document behavior control tags, system prompt internals, and the 10-Component Framework for effective Claude prompts.
---

# SKILL: Claude Prompt Guide

> **Purpose**: Document Anthropic XML tag patterns and prompt engineering best practices
> **Target**: All agents creating or modifying system prompts, commands, and skills

---

## Quick Start

### When to Use This Skill
- Creating new system prompts or agent instructions
- Modifying existing command or skill behavior
- Debugging prompt-related issues

### Quick Reference

```xml
<do_not_act_before_instructions>Defer action until conditions met</do_not_act_before_instructions>
<default_to_action>Prefer tool use over chat responses</default_to_action>
<use_parallel_tool_calls>Execute independent tools simultaneously</use_parallel_tool_calls>
<investigate_before_answering>Research before responding</investigate_before_answering>
<avoid_excessive_markdown_and_bullet_points>Prefer prose over lists</avoid_excessive_markdown_and_bullet_points>
```

## What This Skill Covers

### In Scope
- Anthropic official behavior control XML patterns
- System prompt internal tag structure
- 10-Component Framework for effective prompts
- Best practices (DO/DON'T)

### Out of Scope
- Model-specific tuning → @.claude/skills/coding-standards/SKILL.md
- Agent role definitions → @.claude/agents/CONTEXT.md

---

## Core Concepts

### CRITICAL: Tag Names Are Customizable

**XML tag names are NOT magic** - the content/instructions matter, not the tag name.

---

## Official Behavior Control Tags

### `<do_not_act_before_instructions>` - Control When to Defer Action

**Purpose**: Prevent premature tool use or implementation
**When to Use**: Read-only phases, planning stages

```xml
<do_not_act_before_instructions>
This is a READ-ONLY planning phase. Do not use Edit tool or modify any files.
Only proceed with implementation when the user explicitly runs `/01_confirm` → `/02_execute`.
</do_not_act_before_instructions>
```

### `<default_to_action>` - Encourage Proactive Tool Use

**Purpose**: Prefer tool execution over chat-only responses

```xml
<default_to_action>
Prefer taking action through tool use rather than providing lengthy explanations.
</default_to_action>
```

### `<use_parallel_tool_calls>` - Optimize for Parallel Execution

**Purpose**: Execute independent operations simultaneously

```xml
<use_parallel_tool_calls>
Execute independent operations in parallel using separate tool calls.
</use_parallel_tool_calls>
```

### `<investigate_before_answering>` - Research Before Responding

**Purpose**: Ensure thorough context gathering before response generation

```xml
<investigate_before_answering>
Before providing recommendations, thoroughly investigate the codebase:
1. Read relevant source files
2. Search for related patterns
3. Check existing tests and documentation
</investigate_before_answering>
```

### `<avoid_excessive_markdown_and_bullet_points>` - Control Output Format

**Purpose**: Prefer concise prose over structured lists

```xml
<avoid_excessive_markdown_and_bullet_points>
Prefer natural language prose over excessive bullet points and markdown formatting.
</avoid_excessive_markdown_and_bullet_points>
```

---

## System Prompt Internal Tags

```xml
<!-- Behavior control -->
<behavior_instructions>Core behavioral guidelines</behavior_instructions>
<system-reminder>Context injection during conversation</system-reminder>

<!-- Tool use control -->
<tool_use_instructions>Guidelines for tool invocation</tool_use_instructions>

<!-- Context injection -->
<claudeMd>Codebase and user instructions</claudeMd>
<skill-format>true</skill-format>
```

---

## 10-Component Framework

1. **Role Definition**: Who is the AI acting as?
2. **Context & Scope**: What is covered and excluded?
3. **Quick Start**: How to get started immediately?
4. **Core Concepts**: Why does this approach work?
5. **Behavioral Instructions**: What should the AI do (or not do)?
6. **Tool Use Guidelines**: How should tools be invoked?
7. **Output Format**: What should responses look like?
8. **Examples & Patterns**: What do good implementations look like?
9. **Error Handling**: What to do when things fail?
10. **Further Reading**: Where to find more information?

---

## Best Practices (DO/DON'T)

### DO

✅ **Use XML tags for structure** - Provides clear delimiters for instructions
✅ **Focus on content, not tag names** - Clear instructions matter more than naming
✅ **Combine complementary tags** - Multiple tags for nuanced control
✅ **Provide examples** - Show good vs. bad patterns
✅ **Specify scope clearly** - In Scope vs. Out of Scope sections

### DON'T

❌ **Rely on tag name magic** - `<custom_tag>` works as well as `<official_tag>`
❌ **Over-specify edge cases** - Let Claude reason within guidelines
❌ **Use tags for simple formatting** - Markdown is sufficient
❌ **Nest XML tags deeply** - Keep structure flat (1-2 levels max)
❌ **Duplicate instructions** - One clear statement > multiple vague ones

---

## Common Patterns

### Phase-Gated Workflow

```xml
<do_not_act_before_instructions>
Phase 1 (Planning): Read-only, no file modifications
Phase 2 (Execution): Requires `/01_confirm` command
</do_not_act_before_instructions>
```

### Autonomous Execution

```xml
<default_to_action>Execute immediately when user request maps to clear tool usage.</default_to_action>
<use_parallel_tool_calls>Execute independent operations simultaneously.</use_parallel_tool_calls>
```

### Quality Assurance

```xml
<investigate_before_answering>
Before analysis: Read files, search patterns, check documentation.
</investigate_before_answering>
```

---

## Further Reading

**Internal**: @.claude/skills/claude-prompt-guide/REFERENCE.md - Detailed tag documentation, customization guide | @.claude/skills/claude-prompt-guide/EXAMPLES.md - Common patterns and 10-component framework examples | @.claude/skills/coding-standards/SKILL.md - Code quality standards | @.claude/agents/CONTEXT.md - Agent ecosystem | @.claude/commands/CONTEXT.md - Command workflows

**External**: [Prompting best practices - Claude Docs](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices) | [Use XML tags - Claude Docs](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/use-xml-tags) | [Claude Code Best Practices - Anthropic](https://www.anthropic.com/engineering/claude-code-best-practices) | [Piebald-AI/claude-code-system-prompts](https://github.com/Piebald-AI/claude-code-system-prompts) - 40+ system prompt examples

---

**Version**: claude-pilot 4.4.43
