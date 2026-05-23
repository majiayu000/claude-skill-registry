---
name: claude-subagent-development
description: This skill should be used when the user asks to "create a subagent", "validate a subagent", "generate subagent schema", "check subagent configuration", "write subagent specification", or mentions subagent development, validation, or protocol documentation for Claude Code.
version: 1.0.0
---

# Claude Code Subagent Development

Comprehensive guidance for creating, validating, and documenting Claude Code subagents with schemas and protocol specifications.

## Purpose

This skill provides structured workflows for developing production-ready Claude Code subagents. Use when creating new subagents, validating existing configurations, generating JSON schemas for validation, or writing technical specifications for subagent protocols.

## When to Use

This skill should be used when:
- Creating new subagent configurations
- Validating subagent YAML frontmatter and structure
- Generating JSON schemas for subagent validation
- Writing protocol specifications and technical documentation
- Reviewing subagent configurations for best practices
- Debugging subagent loading or invocation issues

## Core Concepts

### Subagent Structure

Subagents are Markdown files with YAML frontmatter:

```markdown
---
name: subagent-identifier
description: When and how to use this subagent
tools: Tool1, Tool2
model: sonnet
permissionMode: default
skills: skill1, skill2
---

System prompt content in Markdown format.
```

### Required Fields

- **name**: Lowercase identifier with hyphens (pattern: `^[a-z0-9-]+$`)
- **description**: 10-2000 characters describing purpose and usage triggers
- **content**: Markdown body below frontmatter (implicit, not in frontmatter)

### Optional Fields

- **tools**: Comma-separated list of allowed tools (inherits all if omitted)
- **model**: `sonnet`, `opus`, `haiku`, or `inherit`
- **permissionMode**: `default`, `acceptEdits`, `bypassPermissions`, `plan`, `ignore`
- **skills**: Comma-separated skill names to auto-load

## Workflows

### Create a New Subagent

1. **Define purpose and scope**:
   - Identify the specific task or domain
   - List concrete usage examples
   - Determine required tools and permissions

2. **Use the subagent template**:
   ```bash
   cp assets/template.md .claude/agents/your-subagent.md
   ```

3. **Configure frontmatter**:
   - Set unique `name` (lowercase, hyphens)
   - Write specific `description` with trigger phrases
   - Specify minimal `tools` needed (or omit for all)
   - Choose appropriate `model` and `permissionMode`

4. **Write system prompt**:
   - Clear role definition
   - Step-by-step procedures
   - Expected behaviors and constraints
   - Output format guidance

5. **Validate configuration**:
   ```bash
   scripts/validate-subagent.sh .claude/agents/your-subagent.md
   ```

### Validate Existing Subagent

Use the validation script to check:
- YAML frontmatter syntax
- Required fields present
- Field value formats (name pattern, model alias, etc.)
- Tool names validity
- Description quality

```bash
scripts/validate-subagent.sh path/to/subagent.md
```

The script validates against the JSON schema in `assets/subagent-schema.json`.

### Generate JSON Schema

When needing a validation schema for tooling:

1. **Use the existing schema** in `assets/subagent-schema.json`
2. **Customize if needed** for specific validation requirements
3. **Integrate with CI/CD** for automated validation

The schema includes:
- Field types and patterns
- Required vs optional fields
- Value constraints (enums, lengths, patterns)
- Examples and descriptions

### Write Protocol Specification

For technical documentation:

1. **Reference the protocol spec**: `references/protocol-specification.md`
2. **Include key sections**:
   - Architecture overview
   - File format specification
   - Configuration schema
   - Lifecycle management
   - Security considerations
   - Examples

3. **Adapt for your needs**:
   - Extract relevant sections
   - Add project-specific details
   - Include team conventions

## Tools and Resources

### Validation Script

`scripts/validate-subagent.sh` checks:
- File exists and is readable
- Valid YAML frontmatter
- Required fields present
- Name pattern compliance
- Model alias validity
- Tool name validation (optional check)

Usage:
```bash
scripts/validate-subagent.sh <subagent-file>
```

Exit codes:
- 0: Valid configuration
- 1: Validation errors found

### Creation Script

`scripts/create-subagent.sh` scaffolds a new subagent:

```bash
scripts/create-subagent.sh <name> <scope>
```

Arguments:
- `name`: Subagent identifier (lowercase, hyphens)
- `scope`: `project` (.claude/agents/) or `user` (~/.claude/agents/)

Creates file from template and opens in editor.

### JSON Schema

`assets/subagent-schema.json` provides:
- Complete field definitions
- Validation rules
- Type constraints
- Pattern matching
- Example configurations

Use with validation tools:
```bash
# With ajv-cli
ajv validate -s assets/subagent-schema.json -d your-subagent.json

# With Python jsonschema
python -c "import json, jsonschema; \
  jsonschema.validate( \
    json.load(open('subagent.json')), \
    json.load(open('assets/subagent-schema.json')))"
```

## Best Practices

### Strong Descriptions

Include specific trigger phrases:

**Good**:
```yaml
description: Expert code reviewer. Use PROACTIVELY after code changes to review quality, security, and best practices. Checks for vulnerabilities, performance issues, style violations.
```

**Poor**:
```yaml
description: Helps with code
```

### Minimal Tool Permissions

Grant only necessary tools:

```yaml
# Read-only analysis
tools: Read, Grep, Glob

# Code modification
tools: Read, Edit, Write

# Full workflow
tools: Read, Edit, Write, Bash
```

### Clear System Prompts

Structure prompts with:
1. Role definition
2. When invoked actions
3. Methodology/checklist
4. Output format
5. Examples

### Model Selection

Choose appropriate model:
- **haiku**: Fast searches, simple tasks
- **sonnet**: General purpose, complex reasoning (default)
- **opus**: Maximum capability, critical tasks
- **inherit**: Match main conversation's model

## Additional Resources

### Reference Files

Comprehensive documentation in `references/`:

- **`protocol-specification.md`**: Complete subagent protocol spec (20,000+ words)
  - Architecture and data flow
  - File format specification
  - All configuration fields detailed
  - Lifecycle management
  - Security considerations
  - Built-in subagents reference

- **`field-reference.md`**: Detailed field-by-field reference
  - Each field's purpose, format, constraints
  - Examples and anti-patterns
  - Common mistakes to avoid

- **`best-practices.md`**: Advanced best practices
  - Design patterns for subagents
  - Tool permission strategies
  - Context management
  - Team collaboration workflows

### Example Files

Production-ready examples in `examples/`:

- **`code-reviewer.md`**: Comprehensive code review subagent
  - Security, quality, performance checks
  - Structured feedback format
  - Tool usage: Read, Grep, Glob, Bash

- **`debugger.md`**: Systematic debugging specialist
  - Root cause analysis methodology
  - Strategic debugging techniques
  - Common issue patterns

- **`test-runner.md`**: Test automation expert
  - Auto-detect test frameworks
  - Failure analysis and fixing
  - Fast execution with Haiku

### Asset Files

Templates and schemas in `assets/`:

- **`subagent-schema.json`**: Complete JSON Schema for validation
- **`template.md`**: Base template for new subagents

## Quick Reference

### Subagent File Locations

- Project scope: `.claude/agents/name.md`
- User scope: `~/.claude/agents/name.md`
- Plugin scope: `plugin-dir/agents/name.md`

### Precedence Order

When names conflict:
1. Project-level (highest)
2. User-level
3. CLI-defined
4. Built-in (lowest)

### Available Tools

Common tools for subagents:
- `Task` - Delegate to subagents
- `Bash` - Execute shell commands
- `Read, Edit, Write` - File operations
- `Grep, Glob` - Search operations
- `WebFetch, WebSearch` - Web operations
- `TodoWrite` - Task management
- MCP tools: `mcp__<server>__<tool>`

### Permission Modes

- `default`: Standard permission flow (recommended)
- `acceptEdits`: Auto-approve edit operations
- `bypassPermissions`: Skip all permissions (use cautiously)
- `plan`: Read-only exploration
- `ignore`: Ignore permission dialogs

## Troubleshooting

### Subagent Not Loading

Check:
1. File exists in correct location
2. Valid YAML frontmatter syntax
3. Required fields present (name, description)
4. Name follows pattern: `^[a-z0-9-]+$`

Run validation:
```bash
scripts/validate-subagent.sh path/to/subagent.md
```

### Subagent Not Triggering

Improve description:
- Add specific trigger phrases users would say
- Include concrete scenarios
- Use emphatic language ("PROACTIVELY", "MUST BE USED")

Example:
```yaml
description: Security auditor. Use PROACTIVELY when reviewing code, checking for vulnerabilities, or analyzing security. Checks OWASP Top 10, injection attacks, authentication issues.
```

### Tool Not Available

Verify:
1. Tool name spelled correctly (case-sensitive)
2. Tool in allowed list if `tools` specified
3. MCP tool format: `mcp__server__tool`

Check available tools:
```
Task, Bash, Glob, Grep, Read, Edit, Write, NotebookEdit,
WebFetch, WebSearch, BashOutput, KillShell, AskUserQuestion,
TodoWrite, Skill, SlashCommand
```

### Permission Denied

Adjust `permissionMode`:
- `default`: User approves operations
- `acceptEdits`: Auto-approve edits only
- `bypassPermissions`: Auto-approve all (use carefully)

Or grant specific tools in `tools` field.

## Implementation Checklist

Before deploying a subagent:

**Structure**:
- [ ] Valid YAML frontmatter
- [ ] Required fields present (name, description)
- [ ] Markdown body substantial (50+ characters)
- [ ] File in correct location

**Configuration**:
- [ ] Name follows pattern `^[a-z0-9-]+$`
- [ ] Description includes specific triggers
- [ ] Tools minimal but sufficient
- [ ] Model appropriate for task
- [ ] Permission mode suitable for automation level

**Content Quality**:
- [ ] Clear role definition
- [ ] Step-by-step procedures
- [ ] Concrete examples
- [ ] Expected output format
- [ ] Constraints and boundaries

**Validation**:
- [ ] Passes schema validation
- [ ] No YAML syntax errors
- [ ] Tool names valid
- [ ] Model alias correct

**Testing**:
- [ ] Triggers on expected queries
- [ ] Uses correct tools
- [ ] Produces quality output
- [ ] Respects permissions

## Version History

- **1.0.0** (2025-12-03): Initial release
  - Complete protocol specification
  - JSON schema validation
  - Validation and creation scripts
  - Three production-ready examples
  - Comprehensive reference documentation
