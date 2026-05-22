---
name: add_platform.research
description: "Captures CLI configuration and hooks system documentation for the new platform. Use when starting platform integration."
user-invocable: false

---

# add_platform.research

**Step 1/4** in **integrate** workflow

> Full workflow to integrate a new AI platform into DeepWork

> Adds a new AI platform to DeepWork with adapter, templates, and tests. Use when integrating Cursor, Windsurf, or other AI coding tools.


## Instructions

**Goal**: Captures CLI configuration and hooks system documentation for the new platform. Use when starting platform integration.

# Research Platform Documentation

## Objective

Capture comprehensive documentation for the new AI platform's CLI configuration and hooks system, creating a local reference that will guide the implementation phases.

## Task

Research the target platform's official documentation and create two focused documentation files that will serve as the foundation for implementing platform support in DeepWork.

### Process

1. **Identify the platform's documentation sources**
   - Find the official documentation website
   - Locate the CLI/agent configuration documentation
   - Find the hooks or customization system documentation
   - Note: Focus ONLY on slash command/custom command hooks, not general CLI hooks

2. **Gather CLI configuration documentation**
   - How is the CLI configured? (config files, environment variables, etc.)
   - Where are custom commands/skills stored?
   - What is the command file format? (markdown, YAML, etc.)
   - What metadata or frontmatter is supported?
   - How does the platform discover and load commands?

3. **Gather hooks system documentation**
   - What hooks are available for custom command definitions?
   - Focus on hooks that trigger during or after command execution
   - Examples: `stop_hooks`, `pre_hooks`, `post_hooks`, validation hooks
   - Document the syntax and available hook types
   - **Important**: Only document hooks available on slash command definitions, not general CLI hooks

4. **Create the documentation files**
   - Place files in `doc/platforms/<platform_name>/`
   - Each file must have a header comment with source and date
   - Content should be comprehensive but focused

## Output Format

### cli_configuration.md

Located at: `doc/platforms/<platform_name>/cli_configuration.md`

**Structure**:
```markdown
<!--
Last Updated: YYYY-MM-DD
Source: [URL where this documentation was obtained]
-->

# <Platform Name> CLI Configuration

## Overview

[Brief description of the platform and its CLI/agent system]

## Configuration Files

[Document where configuration lives and its format]

### File Locations

- [Location 1]: [Purpose]
- [Location 2]: [Purpose]

### Configuration Format

[Show the configuration file format with examples]

## Custom Commands/Skills

[Document how custom commands are defined]

### Command Location

[Where command files are stored]

### Command File Format

[The format of command files - markdown, YAML, etc.]

### Metadata/Frontmatter

[What metadata fields are supported in command files]

```[format]
[Example of a minimal command file]
```

## Command Discovery

[How the platform discovers and loads commands]

## Platform-Specific Features

[Any unique features relevant to command configuration]
```

### hooks_system.md

Located at: `doc/platforms/<platform_name>/hooks_system.md`

**Structure**:
```markdown
<!--
Last Updated: YYYY-MM-DD
Source: [URL where this documentation was obtained]
-->

# <Platform Name> Hooks System (Command Definitions)

## Overview

[Brief description of hooks available for command definitions]

**Important**: This document covers ONLY hooks available within slash command/skill definitions, not general CLI hooks.

## Available Hooks

### [Hook Name 1]

**Purpose**: [What this hook does]

**Syntax**:
```yaml
[hook_name]:
  - [configuration]
```

**Example**:
```yaml
[Complete example of using this hook]
```

**Behavior**: [When and how this hook executes]

### [Hook Name 2]

[Repeat for each available hook]

## Hook Execution Order

[Document the order in which hooks execute, if multiple are supported]

## Comparison with Other Platforms

| Feature | <Platform> | Claude Code | Other |
|---------|-----------|-------------|-------|
| [Feature 1] | [Support] | [Support] | [Support] |

## Limitations

[Any limitations or caveats about the hooks system]
```

## Quality Criteria

- Both files exist in `doc/platforms/<platform_name>/`
- Each file has a header comment with:
  - Last updated date (YYYY-MM-DD format)
  - Source URL where documentation was obtained
- `cli_configuration.md` comprehensively covers:
  - Configuration file locations and format
  - Custom command file format and location
  - Command discovery mechanism
- `hooks_system.md` comprehensively covers:
  - All hooks available for slash command definitions
  - Syntax and examples for each hook
  - NOT general CLI hooks (only command-level hooks)
- Documentation is detailed enough to implement the platform adapter
- No extraneous topics (only CLI config and command hooks)
- When all criteria are met, include `<promise>✓ Quality Criteria Met</promise>` in your response

## Context

This is the foundation step for adding a new platform to DeepWork. The documentation you capture here will be referenced throughout the implementation process:
- CLI configuration informs how to generate command files
- Hooks documentation determines what features the adapter needs to support
- This documentation becomes a permanent reference in `doc/platforms/`

Take time to be thorough - incomplete documentation will slow down subsequent steps.

## Tips

- Use the platform's official documentation as the primary source
- If documentation is sparse, check GitHub repos, community guides, or changelog entries
- When in doubt about whether something is a "command hook" vs "CLI hook", err on the side of inclusion and note the ambiguity
- Include code examples from the official docs where available


### Job Context

A workflow for adding support for a new AI platform (like Cursor, Windsurf, etc.) to DeepWork.

The **integrate** workflow guides you through four phases:
1. **Research**: Capture the platform's CLI configuration and hooks system documentation
2. **Add Capabilities**: Update the job schema and adapters with any new hook events
3. **Implement**: Create the platform adapter, templates, tests (100% coverage), and README updates
4. **Verify**: Ensure installation works correctly and produces expected files

The workflow ensures consistency across all supported platforms and maintains
comprehensive test coverage for new functionality.

**Important Notes**:
- Only hooks available on slash command definitions should be captured
- Each existing adapter must be updated when new hooks are added (typically with null values)
- Tests must achieve 100% coverage for any new functionality
- Installation verification confirms the platform integrates correctly with existing jobs


## Required Inputs

**User Parameters** - Gather from user before starting:
- **platform_name**: Clear identifier of the platform (e.g., 'cursor', 'windsurf-editor', 'github-copilot-chat')


## Work Branch

Use branch format: `deepwork/add_platform-[instance]-YYYYMMDD`

- If on a matching work branch: continue using it
- If on main/master: create new branch with `git checkout -b deepwork/add_platform-[instance]-$(date +%Y%m%d)`

## Outputs

**Required outputs**:
- `cli_configuration.md`
- `hooks_system.md`

## Guardrails

- Do NOT skip prerequisite verification if this step has dependencies
- Do NOT produce partial outputs; complete all required outputs before finishing
- Do NOT proceed without required inputs; ask the user if any are missing
- Do NOT modify files outside the scope of this step's defined outputs

## On Completion

1. Verify outputs are created
2. Inform user: "integrate step 1/4 complete, outputs: cli_configuration.md, hooks_system.md"
3. **Continue workflow**: Use Skill tool to invoke `/add_platform.add_capabilities`

---

**Reference files**: `.deepwork/jobs/add_platform/job.yml`, `.deepwork/jobs/add_platform/steps/research.md`