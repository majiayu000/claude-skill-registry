name: mcp-to-skill
description: Convert any MCP server into a Claude Skill with 90% context savings. Use this skill when converting an MCP server to a skill to reduce context usage and improve performance.
version: 1.0.0
---

# MCP to Skill Converter

Convert any MCP (Model Context Protocol) server into a Claude Skill using the progressive disclosure pattern for significant context savings and improved performance.

## Context Efficiency Benefits

Traditional MCP approach:
- All tools loaded at startup (10-50k tokens for 20+ tools)
- Context available: 85% of total

Skill approach:
- Metadata only: ~100 tokens at startup
- Full instructions (when used): ~5k tokens
- Tool execution: 0 tokens (runs externally)
- Context available: 96.5% of total

## When to Use This Skill

Use this converter when:
- Working with 10+ MCP tools
- Context space is tight
- Most tools are not used in each conversation
- Tools are independent

Stick with direct MCP when:
- Working with 1-5 tools
- Complex OAuth flows are required
- Persistent connections are needed
- Cross-platform compatibility is critical

## How It Works

Apply the "progressive disclosure" pattern:
1. Read the MCP server configuration
2. Generate a Skill structure with:
   - SKILL.md - Instructions for Claude
   - executor.py - Handles MCP calls dynamically
   - Config files
3. Load metadata only (~100 tokens)
4. Load full instructions when the skill is needed
5. Run MCP tools through executor outside context

## Usage Pattern

### Step 1: Create MCP Configuration

Create a JSON configuration file for your MCP server:

```json
{
  "name": "server-name",
  "description": "Server description",
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-name"],
  "env": {"ENV_VAR": "value"}
}
```

### Step 2: Convert to Skill

Execute the converter script:

```bash
cd $SKILL_DIR
python scripts/convert_mcp_to_skill.py --mcp-config path/to/config.json --output-dir ./output-dir
```

### Step 3: Install Dependencies

```bash
cd ./output-dir
uv pip install mcp
```

### Step 4: Install the Skill

```bash
cp -r ./output-dir ~/.claude/skills/skill-name
```

## Available Scripts

### convert_mcp_to_skill.py

Transform MCP configurations into skills using this main converter script.

Usage:
```bash
python scripts/convert_mcp_to_skill.py --mcp-config CONFIG_FILE --output-dir OUTPUT_DIR
```

Parameters:
- `--mcp-config`: Path to MCP server configuration JSON file
- `--output-dir`: Directory where the generated skill will be created

## Example MCP Configurations

Reference `assets/examples/` for sample MCP configurations:

- GitHub MCP server
- Slack MCP server
- Filesystem MCP server
- Postgres MCP server

## Generated Skill Structure

Generated skills follow this structure:

```
skill-name/
├── SKILL.md (instructions for Claude)
├── executor.py (handles MCP communication)
├── mcp-config.json (MCP server configuration)
└── package.json (dependencies)
```

## Testing Generated Skills

Test generated skills after conversion:

```bash
cd skill-directory

# List tools
python executor.py --list

# Describe a tool
python executor.py --describe tool_name

# Call a tool
python executor.py --call '{"tool": "tool_name", "arguments": {...}}'
```

## Troubleshooting

### "mcp package not found"

Install the mcp package:

```bash
uv pip install mcp
```

### "MCP server not responding"

Verify the config file:
- Command is correct
- Environment variables are set
- Server is accessible

### "TypeError: object _AsyncGeneratorContextManager can't be used in 'await' expression"

This error has been fixed in recent versions. The issue occurred with improper async context manager handling. 

**Solution:** Ensure you're using the latest version of the converter:

```bash
cd mcp-to-skill
python scripts/convert_mcp_to_skill.py --mcp-config your-config.json --output-dir ./your-skill
```

For technical details about this fix, see `references/async_context_manager_fix.md`.

## Requirements

- Python 3.8+
- mcp package (install with `uv pip install mcp`)

## References

Reference these files for additional information:
- `references/mcp_basics.md` - MCP protocol fundamentals
- `references/converter_details.md` - Technical details about the converter
- `references/context_optimization.md` - Context optimization strategies

## Performance Comparison

Real example with GitHub MCP server (8 tools):

| Metric | MCP | Skill | Savings |
|--------|-----|-------|---------|
| Idle | 8,000 tokens | 100 tokens | 98.75% |
| Active | 8,000 tokens | 5,000 tokens | 37.5% |

## Best Practices

1. Use descriptive names for your skills
2. Include clear descriptions in MCP configurations
3. Test generated skills before deployment
4. Keep MCP configurations in version control
5. Use environment variables for sensitive data

## Limitations

- Early stage (feedback welcome)
- Requires `mcp` Python package
- Some complex auth may need adjustments
- Not all MCP servers tested

---

*This skill uses the mcp-to-skill-converter from https://github.com/GBSOSS/-mcp-to-skill-converter*