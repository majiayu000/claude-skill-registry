---
name: skill-with-assets
description: Demonstrates how skills can bundle data files and configuration templates. Use when needing structured data, templates, configuration files, or static reference data.
---

# Skill with Assets

**Description:** Demonstrates how skills can bundle data files and configuration templates.

**When to use:** When a skill needs to reference structured data, templates, or configuration files.

## Workflow

1. Identify that configuration or data is needed
2. Load the appropriate asset from `assets/` directory
3. Parse and use the data

## Available Assets

- `config.json` - Example configuration file demonstrating bundled data

## Key Points

- Assets can be JSON, YAML, templates, etc.
- Assets are loaded on-demand (progressive disclosure)
- Useful for configuration, templates, test data
- Assets should be static data, not code

## Example Usage

**User asks:** "Show me the config"
**Response:** 
1. Read `assets/config.json`
2. Parse the JSON
3. Present the configuration

## When to Bundle Assets

Bundle assets when you need:
- Configuration templates
- Test data or fixtures
- Reference tables or mappings
- Example files
- Static structured data
