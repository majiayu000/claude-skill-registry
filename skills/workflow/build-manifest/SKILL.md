---
name: build-manifest
description: Templates and scripts for generating layered BUILD-GUIDE.json/md from Airtable plugin index - shows available commands organized by infrastructure layers
---

# Build Manifest Generation

This skill provides templates and scripts for generating **BUILD-GUIDE** files (both JSON and Markdown) that show available commands organized by infrastructure layers.

## Purpose

The BUILD-GUIDE is a **layered execution blueprint** that:
- Queries Airtable (as an index to marketplace plugins)
- Identifies available commands for the project's tech stack
- Organizes commands into sequential execution layers
- Detects gaps where tech is mentioned but no plugin exists
- Provides both machine-parseable (JSON) and human-readable (Markdown) formats

## When to Use This Skill

Use this skill when:
- Initializing a new project after `/planning:wizard` completes
- Architecture docs exist with tech stack identified
- Need to generate a build execution plan
- Want to see what commands are available for the detected stack
- Need to identify missing plugins for technologies mentioned in specs

## Layer Structure

BUILD-GUIDE organizes commands into sequential layers:

### Layer 1: Infrastructure Foundation
- Core project setup (detection, specs, worktrees)
- Same for most projects
- Plugins: `foundation`, `planning`, `supervisor`

### Layer 2: Tech Stack Initialization
- Initialize detected frameworks
- Dynamic based on project files (README, roadmap/*.json, specs/)
- Plugins: Project-specific (nextjs-frontend, fastapi-backend, supabase, etc.)

### Layer 3: Feature Implementation
- Build features from specs
- Reference spec files
- Use commands + agents from detected plugins

### Layer 4: Quality & Deployment
- Testing, validation, deployment
- Plugins: `quality`, `deployment`, `versioning`

## Templates

### JSON Template
Location: `templates/BUILD-GUIDE.json.template`

Shows the complete JSON structure with:
- Tech stack detection results
- Layered command organization
- Gap detection for missing plugins
- Available/unavailable status per command

### Markdown Template
Location: `templates/BUILD-GUIDE.md.template`

Human-readable version with:
- Tech stack summary
- Commands grouped by layer
- Usage examples
- Gap warnings

## Scripts

### generate-manifest.py
Location: `scripts/generate-manifest.py`

**Purpose**: Query Airtable and generate BUILD-GUIDE files

**Usage**:
```bash
python scripts/generate-manifest.py \
  --project files (README, roadmap/*.json, specs/)/architecture/README.md \
  --output BUILD-GUIDE
```

**Process**:
1. Read project files (README, roadmap/*.json, specs/) to detect tech stack
2. Query Airtable for plugins matching detected technologies
3. Query Airtable for commands in those plugins
4. Organize commands into layers
5. Detect gaps (tech mentioned but no plugin exists)
6. Generate both .json and .md files

**Requirements**:
- AIRTABLE_TOKEN environment variable
- Architecture docs must exist
- Airtable base ID: appHbSB7WhT1TxEQb

## Examples

### Example Output Structure

See `examples/BUILD-GUIDE.json` for complete Next.js + FastAPI + Supabase example
See `examples/BUILD-GUIDE.md` for markdown version

### Example Gap Detection

```json
{
  "gaps": [
    {
      "technology": "Redis",
      "mentioned_in": "docs/architecture/caching.md",
      "reason": "No redis plugin found in any marketplace",
      "suggestion": "Create redis plugin with /domain-plugin-builder:build-plugin redis"
    }
  ]
}
```

## Integration with build-manifest-generator Agent

The `build-manifest-generator` agent in this plugin uses this skill:

```markdown
!{skill planning:build-manifest}
```

The agent:
1. Invokes this skill to load templates
2. Uses scripts to query Airtable
3. Generates BUILD-GUIDE.json and BUILD-GUIDE.md
4. Places files at project root

## Output Files

**BUILD-GUIDE.json**:
- Machine-parseable
- Complete structure with metadata
- Used by Claude when user requests features
- Location: Project root

**BUILD-GUIDE.md**:
- Human-readable
- Summary format
- Documentation reference
- Location: Project root

## Security

All templates use placeholder format:
- `your_service_key_here` for API keys
- Environment variable references in code examples
- No hardcoded credentials

## Validation

The skill validates:
- Architecture docs exist and are readable
- Airtable connection successful
- All detected plugins have valid commands
- Generated JSON is valid
- Generated Markdown renders correctly

## Usage Pattern

Typical workflow:
```bash
# 1. Planning wizard creates project files (README, roadmap/*.json, specs/)
/planning:wizard

# 2. Generate build manifest
/planning:generate-build-guide  # Uses this skill

# 3. Reference during development
# Claude reads BUILD-GUIDE.json when user says "add authentication"
# Claude sees: /supabase:add-auth available
```

## Maintenance

When adding new plugins to marketplaces:
1. Plugin metadata syncs to Airtable automatically (via sync scripts)
2. Regenerate BUILD-GUIDE for existing projects: `/planning:generate-build-guide --refresh`
3. New commands appear in Layer 2 (Tech Stack Initialization)
