---
name: output-customization
description: Central authority for Claude Code output styles. Covers built-in output styles (Default, Explanatory, Learning), custom output styles, output style frontmatter (name, description, keep-coding-instructions), /output-style command, style switching, output style creation and customization, output style comparisons (vs CLAUDE.md, vs agents, vs slash commands), and output style settings. Assists with selecting appropriate output styles, creating custom styles, configuring output behavior, and understanding style differences. Delegates 100% to docs-management skill for official documentation.
user-invocable: false
allowed-tools: Read, Glob, Grep, Skill
---

# Output Styles Meta Skill

> ## 🚨 MANDATORY: Invoke docs-management First
>
> **STOP - Before providing ANY response about output styles:**
>
> 1. **INVOKE** `docs-management` skill
> 2. **QUERY** for the user's specific topic
> 3. **BASE** all responses EXCLUSIVELY on official documentation loaded
>
> **Skipping this step results in outdated or incorrect information.**
>
> ### Verification Checkpoint
>
> Before responding, verify:
>
> - [ ] Did I invoke docs-management skill?
> - [ ] Did official documentation load?
> - [ ] Is my response based EXCLUSIVELY on official docs?
>
> If ANY checkbox is unchecked, STOP and invoke docs-management first.

## Overview

Central authority for Claude Code output styles. This skill uses **100% delegation to docs-management** - it contains NO duplicated official documentation.

**Architecture:** Pure delegation with keyword registry. All official documentation is accessed via docs-management skill queries.

## When to Use This Skill

**Keywords:** output styles, output style, concise style, verbose style, markdown style, code-sparse style, /output-style command, custom output styles, output style frontmatter, output style prompt, style switching, output behavior, response format, output formatting

**Use this skill when:**

- Understanding available output styles
- Selecting appropriate output style for a task
- Creating custom output styles
- Configuring output style frontmatter
- Switching between output styles
- Comparing output style behaviors
- Customizing output format and verbosity

## Keyword Registry for docs-management Queries

Use these keywords when querying docs-management skill for official documentation:

### Output Style Fundamentals

| Topic | Keywords |
| --- | --- |
| Overview | "output styles", "output style overview", "response formatting" |
| Built-in Styles | "built-in output styles", "default styles" |
| Custom Styles | "custom output styles", "creating output styles" |

### Built-in Styles

| Topic | Keywords |
| --- | --- |
| Default Style | "default output style", "default style", "software engineering style" |
| Explanatory Style | "explanatory style", "explanatory output", "educational insights", "codebase insights" |
| Learning Style | "learning style", "learning output", "learn-by-doing", "TODO human markers", "collaborative coding" |

### Style Configuration

| Topic | Keywords |
| --- | --- |
| Frontmatter | "output style frontmatter", "style YAML frontmatter" |
| Name Field | "output style name", "style naming" |
| Description Field | "output style description", "style description" |
| Keep Coding Instructions | "keep-coding-instructions", "coding instructions", "software engineering prompts" |
| Style File Location | "output style file location", "~/.claude/output-styles", ".claude/output-styles", "user level styles", "project level styles" |

### Style Management

| Topic | Keywords |
| --- | --- |
| Switching Styles | "/output-style command", "switch output style", "change style" |
| Style Selection | "select output style", "choose style", "style recommendations" |
| Style Comparison | "compare output styles", "style differences", "style comparison" |

### Use Cases

| Topic | Keywords |
| --- | --- |
| Task-Based Selection | "output style use cases", "when to use styles" |
| Coding Tasks | "output style coding", "code-focused style" |
| Documentation Tasks | "output style documentation", "writing-focused style" |
| Learning Tasks | "output style learning", "educational style" |

### Comparisons to Related Features

| Topic | Keywords |
| --- | --- |
| vs CLAUDE.md | "output styles vs CLAUDE.md", "system prompt vs user message", "output style CLAUDE.md difference" |
| vs append-system-prompt | "output styles vs append-system-prompt", "system prompt modification", "--append-system-prompt" |
| vs Agents | "output styles vs agents", "output style agent difference", "sub-agents vs output styles" |
| vs Slash Commands | "output styles vs slash commands", "stored prompts vs stored system prompts" |

### Custom Style Development

| Topic | Keywords |
| --- | --- |
| Creating Styles | "create custom output style", "new output style" |
| Style Templates | "output style template", "style starting point" |
| Style Location | "output style file location", "where to save styles" |
| Style Testing | "test output style", "validate style" |

## Quick Decision Tree

**What do you want to do?**

1. **Understand available styles** -> Query docs-management: "built-in output styles", "output style overview"
2. **Use default coding assistant** -> Query docs-management: "default output style", "software engineering style"
3. **Learn about the codebase** -> Query docs-management: "explanatory style", "educational insights"
4. **Learn by doing (hands-on)** -> Query docs-management: "learning style", "TODO human markers", "learn-by-doing"
5. **Switch output style** -> Query docs-management: "/output-style command", "switch output style"
6. **Create custom style** -> Query docs-management: "create custom output style", "output style frontmatter"
7. **Compare to related features** -> Query docs-management: "output styles vs CLAUDE.md", "output styles vs agents"
8. **Where to save style files** -> Query docs-management: "output style file location", "~/.claude/output-styles"

## Topic Coverage

### Built-in Output Styles

- Default: Standard software engineering assistant behavior
- Explanatory: Adds educational "Insights" between tasks to help understand implementation choices
- Learning: Collaborative learn-by-doing mode with `TODO(human)` markers for user contributions

### Output Style Frontmatter

- name field (optional - defaults to filename)
- description field (optional - for UI display in /output-style menu)
- keep-coding-instructions field (optional - default false, whether to keep coding instructions in system prompt)

### Style Configuration Options

- Default style configuration
- Per-session style switching
- Style persistence across sessions

### /output-style Command

- List available styles
- Switch to different style
- View current style
- Style selection syntax

### Custom Style Creation

- File location for custom styles
- Frontmatter structure
- Prompt crafting for custom behavior
- Testing and validation

### Style Selection Criteria

- Task-based recommendations
- Verbosity preferences
- Output format needs
- Code vs explanation balance

### Style Comparisons

- Output Styles vs CLAUDE.md vs --append-system-prompt (system prompt modification approaches)
- Output Styles vs Agents (main loop vs specific tasks, different configuration options)
- Output Styles vs Slash Commands (stored system prompts vs stored prompts)
- When to use each approach

## Delegation Patterns

### Standard Query Pattern

```text
User asks: "What output styles are available?"

1. Invoke docs-management skill
2. Use keywords: "built-in output styles", "output style overview"
3. Load official documentation
4. Provide guidance based EXCLUSIVELY on official docs
```

### Multi-Topic Query Pattern

```text
User asks: "I want brief responses with less code"

1. Invoke docs-management skill with multiple queries:
   - "concise style", "brief responses"
   - "code-sparse style", "minimal code"
2. Synthesize guidance from official documentation
```

### Troubleshooting Pattern

```text
User reports: "My custom output style isn't working"

1. Invoke docs-management skill
2. Use keywords: "output style frontmatter", "create custom output style"
3. Check official docs for style configuration requirements
4. Guide user through proper style setup
```

## Troubleshooting Quick Reference

| Issue | Keywords for docs-management |
| --- | --- |
| Style not changing | "/output-style command", "switch output style" |
| Custom style not loading | "output style frontmatter", "style file location" |
| Too verbose responses | "concise style", "brief responses" |
| Not enough detail | "verbose style", "detailed responses" |
| Want formatted output | "markdown style", "formatted output" |
| Too much code in output | "code-sparse style", "minimal code" |
| Style selection guidance | "output style use cases", "style recommendations" |

## Repository-Specific Notes

This repository does not currently use custom output styles. Output style documentation is relevant for:

- Understanding how output styles affect response behavior
- Potential custom style creation for repository-specific workflows
- Understanding style configuration for team preferences

When working with output style topics, always use the docs-management skill to access official documentation.

## Auditing Output Styles

This skill provides the validation criteria used by the `output-style-auditor` agent for formal audits.

### Audit Resources

| Resource | Location | Purpose |
| --- | --- | --- |
| Audit Framework | `references/audit-framework.md` | Query guides and scoring criteria |

### Scoring Categories

| Category | Points | Key Criteria |
| --- | --- | --- |
| File Structure | 20 | Correct location, .md extension |
| YAML Frontmatter | 30 | Required fields present and valid |
| Content Quality | 30 | Clear instructions, proper structure |
| Compatibility | 20 | Works with style switching, no conflicts |

**Thresholds:** 85+ = PASS, 70-84 = PASS WITH WARNINGS, <70 = FAIL

### Related Agent

The `output-style-auditor` agent (Haiku model) performs formal audits using this skill:

- Auto-loads this skill via `skills: output-customization`
- Uses audit framework and docs-management for rules
- Generates structured audit reports
- Invoked by `/audit-output-styles` command

### External Technology Validation

When auditing output styles that reference external technologies (scripts, packages, runtimes), the auditor MUST validate claims using MCP servers before flagging findings.

**Technologies Requiring MCP Validation:**

- .NET/C# scripts: Validate with microsoft-learn + perplexity
- Node.js/npm packages: Validate with context7 + perplexity
- Python scripts/packages: Validate with context7 + perplexity
- Shell scripts: Validate with perplexity
- Any version-specific claims: ALWAYS validate with perplexity

**Validation Rule:**

Never flag a technology usage as incorrect without first:

1. Querying appropriate MCP server(s) for current documentation
2. Verifying with perplexity for recent changes (especially .NET 10+)
3. Documenting MCP sources in the finding

**Stale Data Warning:**

- microsoft-learn can return cached/outdated documentation
- ALWAYS pair microsoft-learn with perplexity for version verification
- Trust perplexity for version numbers and recently-released features

## References

**Official Documentation (via docs-management skill):**

- Primary: "output-styles" documentation
- Related: "settings", "configuration", "terminal-config"

**Repository-Specific:**

- Output style settings: `.claude/settings.json` (outputStyle setting)

## Version History

- **v1.1.0** (2025-11-27): Content accuracy fixes
  - Fixed built-in styles (Default, Explanatory, Learning - not concise/verbose/markdown/code-sparse)
  - Fixed frontmatter fields (keep-coding-instructions, not "prompt")
  - Added "Comparisons to Related Features" section (vs CLAUDE.md, vs Agents, vs Slash Commands)
  - Added file location keywords (~/.claude/output-styles, .claude/output-styles)
  - Updated decision tree with correct styles
  - Updated topic coverage with accurate descriptions
- **v1.0.0** (2025-11-26): Initial release
  - Pure delegation architecture
  - Comprehensive keyword registry
  - Quick decision tree
  - Topic coverage for all output style features
  - Troubleshooting quick reference

---

## Last Updated

**Date:** 2025-11-28
**Model:** claude-opus-4-5-20251101
