---
name: markdownlint-configuration
description: Configure markdownlint rules and options including rule management, configuration files, inline comments, and style inheritance.
allowed-tools: [Bash, Read]
---

# Markdownlint Configuration

Master markdownlint configuration including rule management, configuration files, inline comment directives, style inheritance, and schema validation for consistent Markdown linting.

## Overview

Markdownlint is a Node.js style checker and linter for Markdown/CommonMark files. It helps enforce consistent formatting and style across Markdown documentation by providing a comprehensive set of rules that can be customized through configuration files or inline comments.

## Installation and Setup

### Basic Installation

Install markdownlint in your project:

```bash
npm install --save-dev markdownlint markdownlint-cli
# or
pnpm add -D markdownlint markdownlint-cli
# or
yarn add -D markdownlint markdownlint-cli
```

### Verify Installation

```bash
npx markdownlint --version
```

## Configuration File Structure

### Basic .markdownlint.json

Create a `.markdownlint.json` file in your project root:

```json
{
  "default": true,
  "MD003": { "style": "atx_closed" },
  "MD007": { "indent": 4 },
  "no-hard-tabs": false,
  "whitespace": false
}
```

This configuration:
- Enables all default rules via `"default": true`
- Configures MD003 (heading style) to use ATX closed format
- Sets MD007 (unordered list indentation) to 4 spaces
- Disables the no-hard-tabs rule
- Disables all whitespace rules

### Rule Naming Conventions

Rules can be referenced by their ID (MD###) or friendly name:

```json
{
  "MD001": false,
  "heading-increment": false,
  "MD003": { "style": "atx" },
  "heading-style": { "style": "atx" },
  "no-inline-html": {
    "allowed_elements": ["strong", "em", "br"]
  }
}
```

Both ID and friendly name work identically.

## Configuration Options

### Enable/Disable All Rules

```json
{
  "default": true
}
```

When `"default": false`, only explicitly enabled rules are active:

```json
{
  "default": false,
  "MD001": true,
  "MD003": { "style": "atx" },
  "line-length": true
}
```

### Rule-Specific Parameters

#### Heading Style (MD003)

```json
{
  "heading-style": {
    "style": "atx"
  }
}
```

Options: `"atx"`, `"atx_closed"`, `"setext"`, `"setext_with_atx"`, `"setext_with_atx_closed"`

#### Unordered List Style (MD004)

```json
{
  "ul-style": {
    "style": "asterisk"
  }
}
```

Options: `"asterisk"`, `"dash"`, `"plus"`, `"consistent"`, `"sublist"`

#### List Indentation (MD007)

```json
{
  "ul-indent": {
    "indent": 4,
    "start_indented": true
  }
}
```

#### Line Length (MD013)

```json
{
  "line-length": {
    "line_length": 100,
    "heading_line_length": 120,
    "code_block_line_length": 120,
    "code_blocks": true,
    "tables": false,
    "headings": true,
    "strict": false,
    "stern": false
  }
}
```

#### No Trailing Spaces (MD009)

```json
{
  "no-trailing-spaces": {
    "br_spaces": 2,
    "list_item_empty_lines": false,
    "strict": false
  }
}
```

#### No Inline HTML (MD033)

```json
{
  "no-inline-html": {
    "allowed_elements": [
      "strong",
      "em",
      "br",
      "sub",
      "sup",
      "kbd",
      "details",
      "summary"
    ]
  }
}
```

#### Horizontal Rule Style (MD035)

```json
{
  "hr-style": {
    "style": "---"
  }
}
```

Options: `"---"`, `"***"`, `"___"`, or custom like `"- - -"`

#### First Line Heading (MD041)

```json
{
  "first-line-heading": {
    "level": 1,
    "front_matter_title": ""
  }
}
```

#### Required Headings

```json
{
  "required-headings": {
    "headings": [
      "# Title",
      "## Description",
      "## Examples",
      "## Resources"
    ]
  }
}
```

#### Proper Names (MD044)

```json
{
  "proper-names": {
    "names": [
      "JavaScript",
      "TypeScript",
      "GitHub",
      "markdownlint",
      "npm"
    ],
    "code_blocks": false
  }
}
```

## Inline Configuration Comments

### Disable Rules for Entire File

```markdown
<!-- markdownlint-disable-file -->

# This file has no linting applied

Any markdown content here will not be checked.
```

### Disable Specific Rules for File

```markdown
<!-- markdownlint-disable-file MD013 MD033 -->

# Long lines and HTML are allowed in this file

This line can be as long as you want without triggering MD013.

<div>Inline HTML is also allowed</div>
```

### Disable Rules Temporarily

```markdown
<!-- markdownlint-disable MD033 -->

<div class="custom-block">
  HTML content here
</div>

<!-- markdownlint-enable MD033 -->

Regular markdown content with rules enforced.
```

### Disable for Single Line

```markdown
This line follows all rules.

Long line that exceeds limit <!-- markdownlint-disable-line MD013 -->

This line follows all rules again.
```

### Disable for Next Line

```markdown
<!-- markdownlint-disable-next-line MD013 -->
This is a very long line that would normally trigger the line-length rule but won't because of the comment above.

This line follows normal rules.
```

### Capture and Restore Configuration

```markdown
<!-- markdownlint-capture -->
<!-- markdownlint-disable -->

Any violations allowed here.

<!-- markdownlint-restore -->

Back to original configuration.
```

### Configure Rules Inline

```markdown
<!-- markdownlint-configure-file {
  "line-length": {
    "line_length": 120
  },
  "no-inline-html": {
    "allowed_elements": ["strong", "em"]
  }
} -->

# Document Title

Rest of document follows inline configuration.
```

## Configuration File Formats

### JSON Configuration

`.markdownlint.json`:

```json
{
  "$schema": "https://raw.githubusercontent.com/DavidAnson/markdownlint/main/schema/markdownlint-config-schema.json",
  "default": true,
  "MD003": { "style": "atx" },
  "MD007": { "indent": 2 },
  "MD013": {
    "line_length": 100,
    "code_blocks": false
  },
  "MD033": {
    "allowed_elements": ["br", "strong", "em"]
  }
}
```

### YAML Configuration

`.markdownlint.yaml`:

```yaml
default: true
MD003:
  style: atx
MD007:
  indent: 2
MD013:
  line_length: 100
  code_blocks: false
MD033:
  allowed_elements:
    - br
    - strong
    - em
```

### JavaScript Configuration

`.markdownlint.js`:

```javascript
module.exports = {
  default: true,
  MD003: { style: "atx" },
  MD007: { indent: 2 },
  MD013: {
    line_length: 100,
    code_blocks: false
  },
  MD033: {
    allowed_elements: ["br", "strong", "em"]
  }
};
```

## Configuration Inheritance

### Extending Base Configurations

Create a base configuration:

`base.json`:
```json
{
  "default": true,
  "line-length": {
    "line_length": 100
  }
}
```

Extend it in your project:

`custom.json`:
```json
{
  "extends": "base.json",
  "no-inline-html": false,
  "line-length": {
    "line_length": 120
  }
}
```

### Using Predefined Styles

Markdownlint includes predefined style configurations:

```json
{
  "extends": "markdownlint/style/relaxed"
}
```

Available styles:
- `markdownlint/style/relaxed` - Less strict rules
- `markdownlint/style/prettier` - Compatible with Prettier

## Schema Validation

### Enable IDE Support

Include the `$schema` property for autocomplete and validation:

```json
{
  "$schema": "https://raw.githubusercontent.com/DavidAnson/markdownlint/main/schema/markdownlint-config-schema.json",
  "default": true
}
```

This enables:
- Autocomplete for rule names
- Validation of configuration values
- Inline documentation in supported editors

## Project-Specific Configurations

### Per-Directory Configuration

Place `.markdownlint.json` in specific directories:

```
project/
├── .markdownlint.json          # Root config
├── docs/
│   ├── .markdownlint.json      # Docs-specific config
│   └── guides/
│       └── .markdownlint.json  # Guides-specific config
```

### Monorepo Configuration

Root `.markdownlint.json`:

```json
{
  "default": true,
  "line-length": {
    "line_length": 100
  }
}
```

Package-specific `packages/api/docs/.markdownlint.json`:

```json
{
  "extends": "../../../.markdownlint.json",
  "no-inline-html": {
    "allowed_elements": ["code", "pre", "div"]
  }
}
```

## Common Configuration Patterns

### Strict Documentation Standards

```json
{
  "default": true,
  "heading-style": { "style": "atx" },
  "ul-style": { "style": "dash" },
  "ol-prefix": { "style": "ordered" },
  "line-length": {
    "line_length": 80,
    "strict": true
  },
  "no-trailing-spaces": {
    "strict": true
  },
  "no-inline-html": false,
  "first-line-heading": {
    "level": 1
  },
  "required-headings": {
    "headings": [
      "# Title",
      "## Description",
      "## Usage",
      "## API"
    ]
  }
}
```

### Relaxed Blog/Article Style

```json
{
  "default": true,
  "line-length": false,
  "no-inline-html": {
    "allowed_elements": [
      "img",
      "a",
      "strong",
      "em",
      "br",
      "div",
      "span"
    ]
  },
  "no-duplicate-heading": {
    "siblings_only": true
  },
  "first-line-heading": false,
  "single-title": false
}
```

### Technical Documentation

```json
{
  "default": true,
  "line-length": {
    "line_length": 120,
    "code_blocks": false,
    "tables": false
  },
  "no-inline-html": {
    "allowed_elements": [
      "details",
      "summary",
      "kbd",
      "sub",
      "sup",
      "br"
    ]
  },
  "code-block-style": {
    "style": "fenced"
  },
  "code-fence-style": {
    "style": "backtick"
  },
  "emphasis-style": {
    "style": "asterisk"
  },
  "strong-style": {
    "style": "asterisk"
  }
}
```

### README Template

```json
{
  "default": true,
  "line-length": {
    "line_length": 100,
    "tables": false,
    "code_blocks": false
  },
  "no-inline-html": {
    "allowed_elements": [
      "img",
      "br",
      "details",
      "summary",
      "sup"
    ]
  },
  "required-headings": {
    "headings": [
      "# *",
      "## Installation",
      "## Usage",
      "## License"
    ]
  },
  "first-line-heading": {
    "level": 1
  }
}
```

## When to Use This Skill

- Setting up markdownlint in new projects
- Configuring linting rules for documentation
- Creating custom rule configurations for teams
- Troubleshooting configuration issues
- Establishing Markdown style guides
- Migrating from other Markdown linters
- Enforcing consistent documentation standards
- Configuring monorepo Markdown linting

## Best Practices

1. **Use Schema Validation** - Always include `$schema` for IDE support
2. **Start with Defaults** - Begin with `"default": true` and disable selectively
3. **Document Exceptions** - Comment why specific rules are disabled
4. **Consistent Naming** - Use either rule IDs or friendly names, not both
5. **Version Control Config** - Commit `.markdownlint.json` to repository
6. **Team Agreement** - Discuss rule changes with team before applying
7. **Progressive Adoption** - Gradually enable stricter rules over time
8. **Test Changes** - Run linter after configuration changes
9. **Use Inheritance** - Leverage extends for shared configurations
10. **Inline Sparingly** - Prefer file-level config over inline comments
11. **Monitor Rule Updates** - Review new rules in markdownlint updates
12. **Environment-Specific** - Use different configs for different doc types
13. **Automation Integration** - Include linting in pre-commit hooks
14. **Regular Review** - Periodically review and update configurations
15. **Clear Comments** - Add comments explaining complex configurations

## Common Pitfalls

1. **Conflicting Rules** - Enabling contradictory rules (e.g., different heading styles)
2. **Over-Configuration** - Specifying too many inline disable comments
3. **Missing Schema** - Not including `$schema` for validation
4. **Incorrect Paths** - Using wrong paths in extends property
5. **Rule Name Typos** - Misspelling rule names (fails silently)
6. **JSON Syntax Errors** - Invalid JSON breaks configuration parsing
7. **Overly Strict** - Enabling strict rules without team buy-in
8. **Ignoring Warnings** - Dismissing legitimate style issues
9. **No Base Config** - Not establishing project-wide defaults
10. **Hardcoded Values** - Not using variables for repeated values
11. **Stale Configurations** - Not updating after markdownlint upgrades
12. **Missing Allowed Elements** - Blocking necessary HTML elements
13. **Inconsistent Inheritance** - Different base configs across projects
14. **No Testing** - Not testing configuration before committing
15. **Unclear Disable Reasons** - Using disable without explanation

## Resources

- [markdownlint GitHub Repository](https://github.com/DavidAnson/markdownlint)
- [markdownlint Rules Documentation](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md)
- [Configuration Schema](https://github.com/DavidAnson/markdownlint/blob/main/schema/markdownlint-config-schema.json)
- [markdownlint-cli Documentation](https://github.com/igorshubovych/markdownlint-cli)
- [Custom Rules Guide](https://github.com/DavidAnson/markdownlint/blob/main/doc/CustomRules.md)
