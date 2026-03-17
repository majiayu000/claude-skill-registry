---
name: nixtla-plugin-scaffolder
description: "Generate production-ready plugin structures from PRD documents with enterprise-compliant files. Use when scaffolding new plugins, converting PRDs to plugin skeletons, or initializing plugin projects. Trigger with 'scaffold plugin', 'create plugin from PRD', or 'initialize plugin structure'."
allowed-tools: "Write,Glob,Read,Bash(mkdir:*)"
version: "1.0.0"
author: "Jeremy Longshore <jeremy@intentsolutions.io>"
license: MIT
---

# Nixtla Plugin Scaffolder

Rapidly scaffold production-ready Claude Code plugin structures from PRD documents, generating all required files with enterprise compliance standards.

## Overview

This skill transforms PRD documents into complete plugin scaffolds:

- **Parse PRDs**: Extract plugin metadata, functional requirements, and MCP tools
- **Generate structure**: Create plugin directories with correct layout
- **Create templates**: Generate plugin.json, SKILL.md, README.md, tests
- **Ensure compliance**: Follow enterprise standards for naming, licensing, author info
- **Accelerate development**: Turn 11 planned plugins into scaffolds in hours, not days

## Prerequisites

**Required**:
- Python 3.8+
- PRD documents in `000-docs/000a-planned-plugins/*/02-PRD.md` format
- Write access to target plugin directory

**Optional**:
- `jq`: For JSON validation (install via `apt install jq` or `brew install jq`)

## Instructions

### Step 1: Identify PRD

Locate the PRD document for the plugin to scaffold:
```bash
ls 000-docs/000a-planned-plugins/*/02-PRD.md
```

### Step 2: Run Scaffold Script

Execute the scaffolding script with the PRD path:
```bash
python {baseDir}/scripts/scaffold_plugin.py \
    --prd 000-docs/000a-planned-plugins/implemented/nixtla-roi-calculator/02-PRD.md \
    --output 005-plugins/nixtla-roi-calculator
```

### Step 3: Review Generated Files

The script creates a complete plugin structure:
```
005-plugins/nixtla-roi-calculator/
├── plugin.json               # Plugin metadata and configuration
├── README.md                 # Plugin documentation
├── .claude/
│   ├── skills/
│   │   └── nixtla-roi-calculator/
│   │       └── SKILL.md      # Main skill definition
│   ├── commands/             # Slash commands
│   └── agents/               # Custom agents
├── scripts/
│   └── roi_mcp_server.py     # MCP server implementation
└── tests/
    └── test_roi_calculator.py # Test suite
```

### Step 4: Customize Generated Files

Edit the generated files to match specific requirements:
- **plugin.json**: Update MCP server configurations
- **SKILL.md**: Expand instructions and examples
- **README.md**: Add plugin-specific documentation
- **scripts/**: Implement MCP server logic

### Step 5: Validate Plugin Structure

Run the plugin validator to ensure compliance:
```bash
python 004-scripts/validate_skills_v2.py --verbose
```

## Output

- **Complete plugin scaffold** with all required files
- **Enterprise-compliant metadata** (author, license, version)
- **MCP server template** ready for implementation
- **Test framework** with example tests
- **Documentation templates** for README and SKILL.md

## Error Handling

1. **Error**: `PRD file not found`
   **Solution**: Verify PRD path, check `000-docs/000a-planned-plugins/` directory

2. **Error**: `Output directory already exists`
   **Solution**: Use `--force` flag to overwrite or choose different output path

3. **Error**: `Invalid PRD format`
   **Solution**: Ensure PRD has required sections (Overview, Functional Requirements, MCP Server Tools)

4. **Error**: `Permission denied creating directory`
   **Solution**: Check write permissions on target directory

5. **Error**: `Missing plugin name in PRD`
   **Solution**: PRD must specify plugin name in header (e.g., `**Plugin:** nixtla-roi-calculator`)

## Examples

### Example 1: Scaffold ROI Calculator Plugin

```bash
python {baseDir}/scripts/scaffold_plugin.py \
    --prd 000-docs/000a-planned-plugins/implemented/nixtla-roi-calculator/02-PRD.md \
    --output 005-plugins/nixtla-roi-calculator \
    --author "Jeremy Longshore <jeremy@intentsolutions.io>" \
    --license MIT
```

**Generated plugin.json**:
```json
{
  "name": "nixtla-roi-calculator",
  "version": "0.1.0",
  "description": "Enterprise ROI calculator for TimeGPT vs. build-in-house analysis",
  "author": { "name": "Jeremy Longshore", "email": "jeremy@intentsolutions.io" },
  "license": "MIT",
  "mcpServers": {
    "nixtla-roi-calculator": {
      "command": "python",
      "args": ["scripts/nixtla_roi_calculator_mcp_server.py"]
    }
  }
}
```

### Example 2: Scaffold Multiple Plugins in Batch

```bash
for prd in 000-docs/000a-planned-plugins/*/02-PRD.md; do
    plugin_name=$(basename $(dirname "$prd"))
    python {baseDir}/scripts/scaffold_plugin.py \
        --prd "$prd" \
        --output "005-plugins/$plugin_name"
done
```

### Example 3: Scaffold with Custom Template

```bash
python {baseDir}/scripts/scaffold_plugin.py \
    --prd 000-docs/000a-planned-plugins/implemented/nixtla-forecast-explainer/02-PRD.md \
    --output 005-plugins/nixtla-forecast-explainer \
    --template {baseDir}/assets/templates/plugin_custom.json
```

## Resources

- **Claude Code Plugin Spec**: https://code.claude.com/docs/en/plugins
- **MCP Protocol**: https://modelcontextprotocol.io/
- **Enterprise Plugin Standard**: `000-docs/6767-e-OD-REF-enterprise-plugin-readme-standard.md`
- **Validator v2**: `004-scripts/validate_skills_v2.py`

**Related Skills**:
- `nixtla-prd-to-code`: Transform PRD into implementation tasks
- `nixtla-demo-generator`: Generate Jupyter notebook demos
- `nixtla-test-generator`: Create comprehensive test suites

**Scripts**:
- `{baseDir}/scripts/scaffold_plugin.py`: Main scaffolding script
- `{baseDir}/assets/templates/plugin.json`: Plugin metadata template
- `{baseDir}/assets/templates/skill_template.md`: SKILL.md template
