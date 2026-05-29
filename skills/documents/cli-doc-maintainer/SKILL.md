---
name: CLI Documentation Maintainer
description: Maintain AILANG CLI help as single source of truth. Use when: adding new commands, adding environment variables, updating command behavior, auditing CLI documentation, ensuring help.go matches codebase implementation, improving CLI discoverability for AIs.
---

# CLI Documentation Maintainer

Ensure AILANG CLI help system (`ailang --help`) remains the authoritative, accurate, and complete source of truth for all CLI features. Critical for AI discoverability in external repositories where CLAUDE.md isn't available.

## Quick Start

**Most common usage:**
```bash
# User says: "I added a new command, update the help"
# This skill will:
# 1. Audit help.go against main.go for missing commands
# 2. Check environment variables usage
# 3. Suggest improvements to help text
# 4. Validate all documented features exist
# 5. Update help.go with new content
```

## When to Use This Skill

Invoke this skill when:
- Adding new commands to cmd/ailang/main.go
- Adding new environment variables (DEBUG_*, AILANG_*, etc.)
- Updating command behavior or flags
- Auditing CLI documentation for accuracy
- Improving CLI discoverability for AIs
- After adding new features (ensure they're documented)
- Quarterly CLI documentation review
- **Proactively**: After implementing any user-facing CLI change

## Available Scripts

### `scripts/audit_commands.sh`
Compare commands in main.go against help.go to find undocumented commands.

**Usage:**
```bash
scripts/audit_commands.sh
```

**Output:**
- Lists all commands in main.go
- Highlights commands missing from help.go
- Shows commands in help.go that don't exist in main.go (stale)
- Exit code 0 if synchronized, 1 if discrepancies found

### `scripts/audit_env_vars.sh`
Find environment variables used in codebase and compare against help.go documentation.

**Usage:**
```bash
scripts/audit_env_vars.sh
```

**Output:**
- Lists all DEBUG_* and AILANG_* variables found in internal/
- Shows which are documented in help.go
- Highlights undocumented variables
- Flags documented variables that don't exist in code (stale)
- Exit code 0 if synchronized, 1 if discrepancies found

### `scripts/suggest_improvements.sh`
Analyze help text organization and suggest improvements.

**Usage:**
```bash
scripts/suggest_improvements.sh
```

**Output:**
- Checks help text length (should be scannable)
- Verifies examples are present
- Suggests missing categories or groupings
- Recommends cross-references between related commands
- Flags verbose or unclear descriptions

## Workflow

### 1. Audit Phase

Run audit scripts to identify discrepancies:

```bash
# Check commands
.claude/skills/cli-doc-maintainer/scripts/audit_commands.sh

# Check environment variables
.claude/skills/cli-doc-maintainer/scripts/audit_env_vars.sh
```

### 2. Analysis Phase

For each discrepancy found:
- **Missing command**: Add to appropriate category in help.go
- **Missing env var**: Document with clear purpose and example
- **Stale documentation**: Remove or update
- **New feature**: Add examples showing usage

### 3. Update Phase

Update [cmd/ailang/help.go](../../../cmd/ailang/help.go):
- Add new commands in correct category
- Document new flags/subcommands
- Add environment variables with examples
- Include practical usage examples
- Maintain consistent formatting

### 4. Validation Phase

```bash
# Rebuild binary
make quick-install

# Test help output
ailang --help

# Test specific command help
ailang <command> --help

# Verify examples work
# (copy examples from help and test them)
```

### 5. Documentation Phase

Update supporting documentation:
- CHANGELOG.md - Document CLI changes
- This skill's reference.md - Update best practices if needed
- Website docs (docs/docs/) - Mirror critical CLI info

## Resources

### CLI Documentation Best Practices
See [resources/best_practices.md](resources/best_practices.md) for:
- Formatting conventions
- Category organization
- Example writing guidelines
- Environment variable naming conventions

### Help Text Template
See [resources/help_template.md](resources/help_template.md) for:
- Command entry templates
- Category section templates
- Environment variable documentation template
- Example section templates

## Progressive Disclosure

This skill loads information progressively:

1. **Always loaded**: This SKILL.md file (YAML frontmatter + workflow overview)
2. **Execute as needed**: Scripts in `scripts/` (audit, validate)
3. **Load on demand**: `resources/best_practices.md`, `resources/help_template.md`

## Design Principles

1. **CLI as Source of Truth**: Help text is THE authoritative reference
2. **AI-First**: Optimize for discoverability by AIs in external repos
3. **Progressive Disclosure**: Main help scannable, detailed help via subcommands
4. **Practical Examples**: Every major command has a working example
5. **Accurate**: Zero stale documentation - audit regularly

## Notes

- Run audits after every CLI change (make it a habit)
- Environment variables must be used in code before documenting
- Commands must exist in main.go before adding to help.go
- Keep main help.go under 250 lines (currently ~220)
- Per-command help (e.g., `coordinator --help`) can be longer
- Test examples actually work before documenting them
