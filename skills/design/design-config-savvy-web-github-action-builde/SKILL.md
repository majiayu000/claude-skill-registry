---
name: design-config
description: Manage design documentation system configuration. Use when initializing the system, adding modules, or updating quality standards.
allowed-tools: Read, Write, Bash
agent: design-doc-agent
---

# Design Documentation Configuration

Manages the design.config.json file that configures the design documentation
system, including modules, paths, quality standards, and integrations.

## Overview

This skill manages configuration by:

1. Validating against JSON schema
2. Initializing new configuration files
3. Adding/updating module definitions
4. Configuring quality standards
5. Managing skill enablement
6. Setting up integrations

## Quick Start

**Validate current config:**

```bash
/design-config validate
```

**Add new module:**

```bash
/design-config add-module my-package
```

**Update quality standards:**

```bash
/design-config update-quality --maxLineLength=120
```

## Configuration File

The design.config.json file is located at `.claude/design/design.config.json`
and follows the JSON schema at:

`.claude/skills/design-config/json-schemas/current.json`

### Top-Level Structure

```json
{
  "$schema": "path/to/schema.json",
  "version": "1.0.0",
  "project": { ... },
  "paths": { ... },
  "modules": { ... },
  "skills": { ... },
  "quality": { ... },
  "integration": { ... }
}
```

## Core Sections

### Project Metadata

```json
"project": {
  "name": "spencerbeggs/website",
  "type": "monorepo",
  "repository": "https://github.com/spencerbeggs/website",
  "maintainer": "C. Spencer Beggs"
}
```

**Fields:**

- `name` - Project name
- `type` - Project type (monorepo, package, application)
- `repository` - Git repository URL
- `maintainer` - Primary maintainer

### Paths

```json
"paths": {
  "designDocs": ".claude/design",
  "skills": ".claude/skills",
  "context": "CLAUDE.md",
  "localContext": "CLAUDE.local.md"
}
```

**Fields:**

- `designDocs` - Root directory for design documentation
- `skills` - Root directory for skills
- `context` - Root context file (CLAUDE.md)
- `localContext` - Local context file (CLAUDE.local.md)

### Modules

```json
"modules": {
  "my-package": {
    "path": "pkgs/my-package",
    "designDocsPath": ".claude/design/my-package",
    "categories": ["architecture", "performance"],
    "maintainer": "Spencer Beggs",
    "userDocs": {
      "readme": "pkgs/my-package/README.md",
      "repoDocs": null,
      "siteDocs": "website/docs/en/packages/my-package"
    }
  }
}
```

**Module Fields:**

- `path` - Relative path to module directory
- `designDocsPath` - Path to module's design docs (null if none)
- `categories` - Allowed design doc categories
- `maintainer` - Module maintainer name
- `userDocs` - User documentation paths (Level 1/2/3)

**Valid Categories:**

- `architecture` - System/component architecture
- `performance` - Performance characteristics
- `observability` - Logging, metrics, events
- `testing` - Testing strategy
- `integration` - Integration patterns
- `cross-linking` - Cross-linking features
- `import-generation` - Import generation
- `source-mapping` - Source mapping
- `meta` - Meta documentation
- `documentation` - Documentation about documentation
- `other` - Other categories

### Quality Standards

```json
"quality": {
  "designDocs": {
    "maxLineLength": 120,
    "requireFrontmatter": true,
    "requireTOC": true,
    "minSections": ["Overview", "Current State", "Rationale"]
  },
  "userDocs": {
    "level1": {
      "targetWordCount": [200, 500],
      "maxLineLength": 80,
      "requireSections": ["Features", "Installation", "Usage"]
    }
  },
  "context": {
    "rootMaxLines": 500,
    "childMaxLines": 300,
    "requireDesignDocPointers": true
  }
}
```

**Quality Sections:**

- `designDocs` - Design documentation standards
- `userDocs` - User documentation standards (Level 1/2/3)
- `context` - CLAUDE.md context file standards

### Skills Configuration

```json
"skills": {
  "baseNamespace": "/",
  "enabled": [
    "design-init",
    "design-validate",
    "design-update"
  ]
}
```

**Fields:**

- `baseNamespace` - Base namespace for skills (usually "/")
- `enabled` - List of enabled skill names

### Integration Settings

```json
"integration": {
  "ci": {
    "enabled": false,
    "validateOnPR": false,
    "syncOnMerge": false
  },
  "git": {
    "trackDesignDocs": true,
    "requireReviewForChanges": false
  }
}
```

**Integration Options:**

- `ci` - CI/CD integration settings
- `git` - Git integration settings

## Workflow

### Validate Configuration

Validates design.config.json against the JSON schema.

**Steps:**

1. Read `.claude/design/design.config.json`
2. Read schema from `json-schemas/current.json`
3. Validate JSON structure
4. Check all required fields present
5. Validate field types and values
6. Check enum values are valid
7. Report validation errors or success

**Validation tools:**

```bash
# Using Node.js with ajv
npm install -g ajv-cli
ajv validate -s json-schemas/current.json -d .claude/design/design.config.json

# Using Python with jsonschema
pip install jsonschema
python -c "import json, jsonschema; ..."
```

### Initialize Configuration

Creates a new design.config.json file with sensible defaults.

**Steps:**

1. Check if config already exists (warn if it does)
2. Detect project type (monorepo, package, app)
3. Scan for existing modules
4. Generate module definitions
5. Set default quality standards
6. Write config file
7. Validate against schema
8. Report success

**Example:**

```json
{
  "version": "1.0.0",
  "project": {
    "name": "my-project",
    "type": "monorepo",
    "maintainer": "Your Name"
  },
  "paths": {
    "designDocs": ".claude/design",
    "skills": ".claude/skills",
    "context": "CLAUDE.md"
  },
  "modules": {},
  "quality": {
    "designDocs": {
      "maxLineLength": 120,
      "requireFrontmatter": true,
      "requireTOC": true,
      "minSections": ["Overview", "Current State", "Rationale"]
    }
  }
}
```

### Add Module

Adds a new module definition to the configuration.

**Steps:**

1. Read current config
2. Validate module doesn't already exist
3. Detect module path (from pnpm workspace, package.json, etc.)
4. Prompt for module details:
   - Design docs path
   - Categories
   - Maintainer
   - User docs paths
5. Add module to config
6. Validate updated config
7. Write config file
8. Report success

**Example:**

```bash
/design-config add-module effect-type-registry \
  --path=pkgs/effect-type-registry \
  --categories=architecture,performance,observability
```

### Update Quality Standards

Updates quality standards for design docs, user docs, or context files.

**Steps:**

1. Read current config
2. Parse update parameters
3. Update specified quality fields
4. Validate updated config
5. Write config file
6. Report changes

**Example:**

```bash
/design-config update-quality \
  --designDocs.maxLineLength=120 \
  --context.rootMaxLines=500
```

### Update Module

Updates an existing module definition.

**Steps:**

1. Read current config
2. Validate module exists
3. Parse update parameters
4. Update module fields
5. Validate updated config
6. Write config file
7. Report changes

**Example:**

```bash
/design-config update-module effect-type-registry \
  --add-category=testing \
  --siteDocs=website/docs/en/packages/effect-type-registry
```

### Enable/Disable Skills

Manages the list of enabled skills.

**Steps:**

1. Read current config
2. Validate skill names exist
3. Add/remove from enabled list
4. Validate updated config
5. Write config file
6. Report changes

**Example:**

```bash
/design-config enable-skill design-prune design-export
/design-config disable-skill design-archive
```

## Schema Reference

The complete JSON schema is located at:

`.claude/skills/design-config/json-schemas/current.json`

**Schema URL:**

`https://spencerbegg.gs/schemas/design-config/1.0.0/schema.json`

**To reference in config:**

```json
{
  "$schema": ".claude/skills/design-config/json-schemas/current.json",
  "version": "1.0.0",
  ...
}
```

## Validation

### Required Fields

**Top-level:**

- `version` - Schema version (semver)
- `project` - Project metadata
- `paths` - Standard paths
- `modules` - Module definitions
- `quality` - Quality standards

**Project:**

- `name` - Project name
- `type` - Project type
- `maintainer` - Maintainer name

**Paths:**

- `designDocs` - Design docs root
- `skills` - Skills root
- `context` - Context file path

**Module:**

- `path` - Module directory path
- `maintainer` - Module maintainer

**Quality.designDocs:**

- `maxLineLength` - Max line length (80-200)
- `requireFrontmatter` - Frontmatter required (boolean)
- `requireTOC` - TOC required (boolean)
- `minSections` - Minimum sections (array)

### Field Validation

**Version:** Must match semver pattern `^[0-9]+\.[0-9]+\.[0-9]+$`

**Project type:** Must be one of: `monorepo`, `package`, `application`

**Categories:** Must be one of the valid category enums

**Line lengths:**

- `designDocs.maxLineLength`: 80-200
- `userDocs.level1.maxLineLength`: 80-120
- `userDocs.level2.maxLineLength`: 80-150

**Context lines:**

- `context.rootMaxLines`: 100-1000 (default 500)
- `context.childMaxLines`: 100-500 (default 300)

## Common Use Cases

### Initialize New Project

```bash
/design-config init \
  --name=my-project \
  --type=monorepo \
  --maintainer="Your Name"
```

### Add Package to Monorepo

```bash
/design-config add-module my-package \
  --path=packages/my-package \
  --categories=architecture,performance
```

### Update Quality Standards Example

```bash
/design-config update-quality \
  --designDocs.maxLineLength=100 \
  --context.rootMaxLines=600
```

### Enable New Skills

```bash
/design-config enable-skill design-prune design-export
```

### Validate After Manual Edit

```bash
/design-config validate
```

## Error Handling

### Invalid Schema

```text
ERROR: Configuration validation failed

Schema: .claude/skills/design-config/json-schemas/current.json
Config: .claude/design/design.config.json

Errors:
- .version: Must match pattern ^[0-9]+\.[0-9]+\.[0-9]+$
- .modules.my-package.categories[0]: Must be one of:
  architecture, performance, ...
- .quality.designDocs.maxLineLength: Must be <= 200

Fix these errors and run validate again.
```

### Missing Required Fields

```text
ERROR: Missing required fields

- project.name is required
- project.type is required
- quality.designDocs is required

Add these fields and validate again.
```

### Module Already Exists

```text
ERROR: Module already exists

Module: effect-type-registry

To update existing module, use:
/design-config update-module effect-type-registry
```

## Integration

Works with all design documentation skills:

- `/design-init` - Uses config for module paths and categories
- `/design-validate` - Uses config for quality standards
- `/design-sync` - Uses config for module definitions
- `/design-audit` - Uses config for quality checks
- All skills - Read config for paths and settings

## Success Criteria

A valid configuration:

- ✅ Passes JSON schema validation
- ✅ All required fields present
- ✅ Field values match constraints
- ✅ Module paths exist
- ✅ Categories are valid enums
- ✅ Quality standards are reasonable
- ✅ No duplicate module names
