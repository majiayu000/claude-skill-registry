---
name: create-mcp-skill
description: Create a new skill that uses an MCP server, following best practices from the MCP CLI guide. Use when user wants to create a skill for a new MCP server or integrate MCP functionality into a skill.
allowed-tools: Bash, Read, Write, Edit, Glob
---

# Create MCP Skill

Guide for creating new skills that use MCP (Model Context Protocol) servers with optimized performance patterns.

**📚 Reference:** See [MCP CLI Guide](../../.docs/mcp-cli.md) for detailed patterns and best practices.

## Overview

This skill helps you create a new skill that uses an MCP server by:
1. Setting up the skill directory structure
2. Discovering available MCP tools
3. Creating optimized command patterns
4. Applying performance best practices

## Prerequisites

- MCP CLI installed (`brew install mcp` or `go install github.com/f/mcptools/cmd/mcptools@latest`)
- Target MCP server available (npm package, binary, etc.)

## Process

### 1. Discover Available Tools

**First, explore what the MCP server offers:**

```bash
# List all tools
mcp tools SERVER_COMMAND

# Get detailed JSON schema
mcp tools SERVER_COMMAND --format json

# Interactive exploration
mcp shell SERVER_COMMAND
# Type /h for help
```

**Example:**
```bash
# Chrome DevTools
mcp tools bunx -y chrome-devtools-mcp@latest

# Filesystem server
mcp tools npx @modelcontextprotocol/server-filesystem ~
```

### 2. Test Individual Tools

**Test each tool before documenting:**

```bash
# Template
echo -e 'TOOL_NAME {"param":"value"}\nexit' | timeout 30 mcp shell SERVER_COMMAND

# Example
echo -e 'navigate_page {"url":"https://example.com"}\nexit' | timeout 30 mcp shell bunx -y chrome-devtools-mcp@latest -- --isolated
```

**Check for:**
- Required vs optional parameters
- Empty parameter schema issues
- Response format
- Execution time

### 3. Create Skill Structure

```
skills/SKILL_NAME/
├── SKILL.md           # Main skill documentation
└── .examples/         # (Optional) Example outputs
```

### 4. Write Skill Documentation

**Template for SKILL.md:**

```markdown
---
name: SKILL_NAME
description: Brief description of what this skill does and when to use it.
allowed-tools: Bash, Read, Write
---

# Skill Name

Brief overview.

**📚 See also:** [MCP CLI Guide](../../.docs/mcp-cli.md)

## Setup

\`\`\`bash
# Installation instructions for the MCP server
\`\`\`

## Quick Start (FASTEST)

### Common Task 1

\`\`\`bash
pkill -9 -f "server-pattern" 2>/dev/null; sleep 1; \\
echo -e 'command1 {"param":"value"}\\ncommand2 {"param":"value"}\\nexit' | \\
timeout 30 mcp shell SERVER_COMMAND [FLAGS]
\`\`\`

### Common Task 2

\`\`\`bash
# Another optimized pattern
\`\`\`

**⚡ Pattern:** cleanup; sleep; echo commands | timeout shell

## Key Tools

- **tool1** - Description (required params: `param1`, `param2`)
- **tool2** - Description (optional params: `param1`)

## Important Notes

- Server-specific quirks
- Performance considerations
- Common gotchas

## Troubleshooting

**Problem: [Common issue]**

\`\`\`bash
# Solution
\`\`\`
```

## Best Practices Checklist

When creating an MCP-based skill, ensure:

### ✅ Performance

- [ ] Quick Start section at the top with copy-paste ready commands
- [ ] All examples use the optimized pattern: `cleanup; sleep; echo | timeout shell`
- [ ] Shell mode recommended over individual calls
- [ ] Cleanup commands included (pkill pattern)
- [ ] Timeout wrapper on all shell commands (30s default)

### ✅ Parameter Handling

- [ ] Parameters passed directly (no `{"arguments":{}}` wrapper)
- [ ] Tools with optional-only params documented with workaround
- [ ] Empty parameter bug addressed where applicable
- [ ] Example commands show correct parameter format

### ✅ Documentation

- [ ] Reference to MCP CLI guide included
- [ ] Server installation instructions provided
- [ ] Quick start patterns for common tasks
- [ ] Key tools listed with parameter requirements
- [ ] Troubleshooting section for common issues
- [ ] Performance tips highlighted

### ✅ Command Structure

- [ ] Correct argument order: `mcp call TOOL SERVER --params '{}'`
- [ ] Server flags properly positioned with `--` separator
- [ ] Exit command included in shell mode examples
- [ ] One-liner format (no backslash continuations if possible)

## Example: Chrome DevTools Skill

See `skills/chrome-devtools/SKILL.md` for a complete example that follows all best practices.

**Key features:**
- Quick start patterns at the top
- 6-9x performance improvement documented
- Optimized one-liners for common tasks
- Comprehensive troubleshooting guide
- References MCP CLI guide

## Template Generator

**Generate a basic skill structure:**

```bash
# Set variables
SKILL_NAME="my-mcp-skill"
SERVER_COMMAND="bunx my-mcp-server@latest"
SERVER_PATTERN="my-mcp-server"

# Create directory
mkdir -p "skills/$SKILL_NAME"

# Create SKILL.md with template
cat > "skills/$SKILL_NAME/SKILL.md" << 'EOF'
---
name: SKILL_NAME
description: TODO - Add description
allowed-tools: Bash, Read, Write
---

# Skill Name

TODO - Add overview

**📚 See also:** [MCP CLI Guide](../../.docs/mcp-cli.md)

## Setup

```bash
# TODO - Add installation
```

## Quick Start (FASTEST)

### Common Task

```bash
pkill -9 -f "SERVER_PATTERN" 2>/dev/null; sleep 1; \
echo -e 'COMMAND\nexit' | \
timeout 30 mcp shell SERVER_COMMAND
```

## Key Tools

- **tool1** - TODO

## Important Notes

- TODO

## Troubleshooting

**Problem: Issue**

```bash
# Solution
```
EOF

# Discover tools
mcp tools $SERVER_COMMAND

# Test interactively
mcp shell $SERVER_COMMAND
```

## Common Patterns

### Pattern 1: Single Command Check

```bash
pkill -9 -f "PATTERN" 2>/dev/null; sleep 1; \
echo -e 'TOOL {"param":"value"}\nexit' | \
timeout 30 mcp shell SERVER -- --isolated
```

### Pattern 2: Multi-Command Debug

```bash
pkill -9 -f "PATTERN" 2>/dev/null; sleep 1; \
echo -e 'CMD1 {"p":"v"}\nCMD2 {"p":"v"}\nCMD3 {"p":"v"}\nexit' | \
timeout 30 mcp shell SERVER -- --isolated
```

### Pattern 3: With Custom Flags

```bash
pkill -9 -f "PATTERN" 2>/dev/null; sleep 1; \
echo -e 'COMMAND\nexit' | \
timeout 30 mcp shell SERVER -- --flag1 --flag2=value
```

## Testing Your Skill

1. **Test cleanup pattern works:**
   ```bash
   pkill -9 -f "PATTERN" 2>/dev/null; sleep 1; echo "Cleanup OK"
   ```

2. **Test basic command:**
   ```bash
   echo -e 'list_tools\nexit' | timeout 10 mcp shell SERVER
   ```

3. **Test multi-command:**
   ```bash
   echo -e 'cmd1\ncmd2\ncmd3\nexit' | timeout 30 mcp shell SERVER
   ```

4. **Test with cleanup:**
   ```bash
   pkill -9 -f "PATTERN" 2>/dev/null; sleep 1; \
   echo -e 'cmd1\ncmd2\nexit' | timeout 30 mcp shell SERVER
   ```

5. **Verify no hanging:**
   - Commands should complete within timeout
   - Exit command should terminate session cleanly

## Optimization Checklist

Compare your skill against the optimized pattern:

| Aspect | Before | After |
|--------|--------|-------|
| Commands per task | 5-10 | 1 |
| Manual cleanup | Yes | Automated |
| Failures from locks | Common | Zero |
| Execution time | 60-90s | 5-10s |
| Success rate | 60-70% | 100% |

## Resources

- [MCP CLI Guide](../../.docs/mcp-cli.md) - Complete MCP CLI reference
- [Chrome DevTools Skill](../chrome-devtools/SKILL.md) - Reference implementation
- [MCP Documentation](https://modelcontextprotocol.io/) - Official MCP docs
- [mcptools GitHub](https://github.com/f/mcptools) - CLI tool source

## Quick Reference

**Every MCP skill should have:**

1. **Quick Start section** - Copy-paste ready commands
2. **Optimized pattern** - `cleanup; sleep; echo | timeout shell`
3. **Performance note** - Document speed improvement
4. **MCP CLI guide reference** - Link to `.docs/mcp-cli.md`
5. **Troubleshooting** - Common issues and solutions

**Every command should:**

1. Include cleanup (`pkill -9 -f "PATTERN"`)
2. Wait after cleanup (`sleep 1`)
3. Use shell mode for 2+ commands
4. Have timeout wrapper
5. End with `exit`
6. Use correct parameter format (no "arguments" wrapper)
