---
name: docs
description: Generate Mintlify documentation for new Fair-Forge features. Use when adding new metrics, runners, generators, storage backends, or any new module. Automatically creates MDX files and updates docs.json navigation.
argument-hint: [module-type] [module-name]
---

# Fair-Forge Documentation Generator

Generate Mintlify MDX documentation for new Fair-Forge modules. Creates properly formatted documentation pages and updates navigation.

## Mintlify Documentation Reference

**IMPORTANT**: When you need to look up how to do something in Mintlify (components, configuration, styling, etc.), fetch this URL:

```
https://www.mintlify.com/docs/llms.txt
```

This contains the complete Mintlify documentation optimized for LLMs.

## Usage

```
/docs [module-type] [module-name]
```

Examples:
```
/docs metric agentic
/docs runner custom-api
/docs generator pdf-loader
/docs storage s3
```

## Supported Module Types

| Type | Directory | Template | Navigation Group |
|------|-----------|----------|------------------|
| `metric` | `docs/metrics/` | `templates/metric.mdx` | Metrics |
| `runner` | `docs/runners/` | `templates/runner.mdx` | Runners |
| `generator` | `docs/generators/` | `templates/generator.mdx` | Generators |
| `storage` | `docs/storage/` | `templates/storage.mdx` | Storage |
| `core-concept` | `docs/core-concepts/` | `templates/core-concept.mdx` | Core Concepts |

## Workflow

### 1. Analyze the Source Code

First, read the implementation to understand:
- Class name and inheritance
- Constructor parameters and their types
- Main methods and their signatures
- Return types and schemas
- Dependencies and extras needed

For metrics, check `fair_forge/metrics/{name}.py`
For runners, check `fair_forge/runners/{name}.py`
For generators, check `fair_forge/generators/{name}.py`
For storage, check `fair_forge/storage/{name}.py`

### 2. Generate MDX Documentation

Use the appropriate template from `templates/` directory:

1. Copy the template content
2. Replace all placeholders with actual values
3. Add code examples from the source or tests
4. Include configuration options table
5. Add troubleshooting section if needed

If you need to use a Mintlify component you're unsure about, fetch `https://www.mintlify.com/docs/llms.txt` for reference.

### 3. Update Navigation

Edit `docs/docs.json` to add the new page to navigation:

```json
{
  "navigation": {
    "tabs": [
      {
        "tab": "Documentation",
        "groups": [
          {
            "group": "Metrics",
            "pages": [
              "metrics/overview",
              "metrics/new-metric"  // Add here
            ]
          }
        ]
      }
    ]
  }
}
```

### 4. Verify Documentation

After creating the docs:
1. Run `mint dev` to preview
2. Check all links work
3. Verify code examples are correct
4. Ensure navigation is properly updated

## Template Placeholders

All templates use these common placeholders:

| Placeholder | Description | Example |
|-------------|-------------|---------|
| `{MODULE_NAME}` | Display name | `Agentic` |
| `{MODULE_SLUG}` | URL-friendly name | `agentic` |
| `{MODULE_DESCRIPTION}` | Short description | `Evaluate agentic AI behavior` |
| `{EXTRA_NAME}` | pip extra name | `agentic` |
| `{CLASS_NAME}` | Python class name | `Agentic` |
| `{IMPORT_PATH}` | Full import path | `fair_forge.metrics.agentic` |

## Mintlify Components Quick Reference

Common components (fetch `https://www.mintlify.com/docs/llms.txt` for full details):

- **CodeGroup** - Multiple code examples with tabs
- **Tabs** - Organize content by category
- **Cards/CardGroup** - Navigation cards
- **Accordion/AccordionGroup** - Collapsible sections
- **Note/Warning/Info** - Callout boxes
- **Steps** - Numbered step-by-step instructions

## File Structure

```
docs/
├── docs.json              # Navigation config
├── metrics/
│   ├── overview.mdx
│   └── {metric-name}.mdx
├── runners/
│   ├── overview.mdx
│   └── {runner-name}.mdx
├── generators/
│   ├── overview.mdx
│   └── {generator-name}.mdx
└── storage/
    ├── overview.mdx
    └── {storage-name}.mdx
```

## Best Practices

1. **Keep descriptions concise** - First paragraph should explain what the module does
2. **Show installation first** - Always include the pip install command with extras
3. **Provide working examples** - Code should be copy-pasteable
4. **Document all parameters** - Use tables for configuration options
5. **Include output examples** - Show what the results look like
6. **Add troubleshooting** - Common errors and solutions

## Resources

- **Mintlify Docs**: `https://www.mintlify.com/docs/llms.txt` (use WebFetch)
- Templates: `templates/` directory in this skill
- Existing docs: `docs/` directory for examples
- Source code: `fair_forge/` for implementation details
