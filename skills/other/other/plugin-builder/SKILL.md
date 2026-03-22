---
name: plugin-builder
description: Automate Claude Code plugin creation, packaging, validation, and distribution. Use when creating plugins, packaging skills, generating manifests, validating plugin structure, setting up marketplaces, or distributing skill collections.
allowed-tools: Read, Write, Edit, Glob, Bash
---

# Plugin Builder

## Overview

plugin-builder automates the entire Claude Code plugin creation and distribution process. It generates valid plugin structures, manifests, validates compliance, packages existing skills, and prepares plugins for marketplace distribution.

**Purpose**: Transform skills into distributable plugins in minutes instead of hours

**Key Capabilities**:
- Initialize plugin directory structure
- Generate valid plugin.json and marketplace.json manifests
- Validate plugin structure and 2025 schema compliance
- Package existing skills into plugin format
- Automate repetitive plugin tasks

**Pattern**: Task-based (independent operations, flexible order)

**Time Savings**: 2-4 hours manual work → 15-30 minutes automated

## What Are Claude Code Plugins?

Plugins are distributable packages that extend Claude Code with custom functionality. They can contain:
- **Skills**: Agent capabilities (what we have 32 of!)
- **Commands**: Custom slash commands
- **Agents**: Specialized subagents
- **Hooks**: Event handlers
- **MCP Servers**: External tool integrations

**Distribution**: Plugins are shared via Git-based marketplaces. Users install with:
```
/plugin marketplace add owner/repo
/plugin install plugin-name@marketplace-name
```

**Structure**:
```
plugin-name/
├── .claude-plugin/
│   ├── plugin.json           # Required: Plugin metadata
│   └── marketplace.json      # Optional: For distribution
├── skills/                    # Your skills go here
├── commands/                  # Custom commands (optional)
├── agents/                    # Subagents (optional)
└── README.md                  # Recommended: Documentation
```

## When to Use

Use plugin-builder when you need to:

**Creating Plugins**:
- Package your skills for distribution
- Create installable skill collections
- Share skills with your team
- Publish to community marketplaces

**Validation & Quality**:
- Validate plugin structure before publishing
- Ensure 2025 schema compliance
- Check manifest correctness
- Verify component formatting

**Distribution Setup**:
- Create team/organization marketplaces
- Set up GitHub distribution
- Configure multi-plugin catalogs

**Bulk Operations**:
- Convert multiple skills to plugins
- Package entire skill ecosystems
- Migrate existing skills to plugin format

## Prerequisites

Before using plugin-builder:

**Knowledge**:
- Basic understanding of Claude Code skills
- Familiarity with terminal/command line
- Basic JSON concepts (scripts generate it for you)

**Tools**:
- Python 3.8+ installed
- Skills/commands/agents to package (for packaging operations)
- Git installed (for marketplace distribution)

**Optional**:
- GitHub account (for public distribution)
- Text editor (for manual manifest edits)

## Operations

### Operation 1: Initialize Plugin Structure

Create a complete plugin directory structure with minimal configuration.

**Purpose**: Quickly scaffold a new plugin with correct structure and minimal boilerplate

**When to Use**:
- Starting a new plugin from scratch
- Need proper directory layout
- Want generated README template

**Prerequisites**:
- Plugin name decided (kebab-case recommended)
- Basic metadata known (description, author)

**Inputs**:
- Plugin name
- Optional: Description, author information

**Process**:

**Method 1: Interactive Script (Recommended)**
```bash
cd /path/to/your/workspace
python /path/to/plugin-builder/scripts/init_plugin.py
```

Follow prompts:
1. Enter plugin name (will create directory with this name)
2. Enter description (brief, 1-2 sentences)
3. Enter author name
4. Enter author email (optional)
5. Choose components to include (skills/commands/agents)

**Method 2: Command Line**
```bash
python /path/to/plugin-builder/scripts/init_plugin.py my-plugin \
  --description "My awesome plugin" \
  --author "Your Name" \
  --email "you@example.com" \
  --components skills,commands
```

**Method 3: Manual Creation**
```bash
mkdir -p my-plugin/.claude-plugin
mkdir -p my-plugin/skills
mkdir -p my-plugin/commands  # optional
mkdir -p my-plugin/agents    # optional

# Create minimal plugin.json
cat > my-plugin/.claude-plugin/plugin.json <<'EOF'
{
  "name": "my-plugin"
}
EOF

# Create README
cat > my-plugin/README.md <<'EOF'
# My Plugin

Description of what this plugin does.

## Installation

\`\`\`bash
/plugin marketplace add your-username/your-repo
/plugin install my-plugin
\`\`\`
EOF
```

**Outputs**:
```
my-plugin/
├── .claude-plugin/
│   └── plugin.json       # Minimal manifest (name only)
├── skills/               # If selected
├── commands/             # If selected
├── agents/               # If selected
└── README.md             # Template with installation instructions
```

**Validation**:
- [ ] Directory created with correct name
- [ ] .claude-plugin/plugin.json exists with valid JSON
- [ ] README.md exists
- [ ] Selected component directories created

**Example**:
```bash
# Interactive mode
$ python scripts/init_plugin.py

Enter plugin name (kebab-case): team-toolkit
Enter description: Development tools for our team
Enter author name: DevOps Team
Enter author email (optional): devops@company.com
Include skills? (y/n): y
Include commands? (y/n): y
Include agents? (y/n): n

Creating plugin structure...
✓ Created team-toolkit/
✓ Created .claude-plugin/plugin.json
✓ Created README.md
✓ Created skills/
✓ Created commands/

Next steps:
1. Add your skills to team-toolkit/skills/
2. Add your commands to team-toolkit/commands/
3. Run: python scripts/generate_manifest.py team-toolkit/
4. Run: python scripts/validate_plugin.py team-toolkit/
```

**See Also**: [templates/plugin.json.minimal](templates/plugin.json.minimal) for the generated manifest structure

---

### Operation 2: Generate plugin.json

Create or update the plugin manifest file with complete metadata.

**Purpose**: Generate a valid, schema-compliant plugin.json with all recommended fields

**When to Use**:
- After initializing plugin structure
- Need to add/update metadata
- Want all optional fields included
- Upgrading from minimal to complete manifest

**Prerequisites**:
- Plugin directory exists
- Plugin name decided
- Metadata information available

**Inputs**:
- Plugin name (required)
- Version (recommended, default: 1.0.0)
- Description (recommended)
- Author information (optional but recommended)
- Homepage URL (optional)
- Repository URL (optional)
- License (optional, default: MIT)
- Keywords (optional, for discoverability)
- Component paths (optional, uses defaults)

**Process**:

**Method 1: Interactive Script (Recommended)**
```bash
python scripts/generate_manifest.py /path/to/my-plugin
```

Follow prompts for each field. Press Enter to accept defaults or skip optional fields.

**Method 2: Update Existing Manifest**
```bash
python scripts/generate_manifest.py /path/to/my-plugin --update
```

Loads existing manifest, prompts only for changes/additions.

**Method 3: Use Template**
```bash
python scripts/generate_manifest.py /path/to/my-plugin --template standard
```

Templates available:
- `minimal`: Name only (valid but basic)
- `standard`: Name, version, description, author (recommended)
- `complete`: All fields with examples

**Method 4: Manual Creation**

Copy from [templates/plugin.json.standard](templates/plugin.json.standard) and edit:
```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "Brief description of plugin functionality",
  "author": {
    "name": "Your Name",
    "email": "you@example.com"
  },
  "keywords": ["keyword1", "keyword2"],
  "license": "MIT"
}
```

Save to `my-plugin/.claude-plugin/plugin.json`.

**Outputs**:
- Valid `plugin.json` in `.claude-plugin/` directory
- JSON formatted and validated
- All required fields present
- Optional fields included as specified

**Validation**:
- [ ] JSON syntax is valid
- [ ] Name field present (required)
- [ ] Name is kebab-case
- [ ] Version follows semver if present
- [ ] No absolute paths
- [ ] File saved in correct location

**Example**:
```bash
$ python scripts/generate_manifest.py team-toolkit/

Generating plugin.json for team-toolkit
======================================

Name: team-toolkit (from directory)
Version [1.0.0]: 2.1.0
Description: Development and deployment tools for engineering team
Author name: DevOps Team
Author email: devops@company.com
Author URL (optional): https://company.com/devops
Homepage (optional): https://github.com/company/team-toolkit
Repository (optional): https://github.com/company/team-toolkit
License [MIT]: Apache-2.0
Keywords (comma-separated): deployment,ci-cd,automation,team

Component paths (optional, press Enter for defaults):
Skills path [./skills/]:
Commands path [./commands/]:
Agents path:

Generated plugin.json:
{
  "name": "team-toolkit",
  "version": "2.1.0",
  "description": "Development and deployment tools for engineering team",
  "author": {
    "name": "DevOps Team",
    "email": "devops@company.com",
    "url": "https://company.com/devops"
  },
  "homepage": "https://github.com/company/team-toolkit",
  "repository": "https://github.com/company/team-toolkit",
  "license": "Apache-2.0",
  "keywords": ["deployment", "ci-cd", "automation", "team"]
}

✓ Saved to team-toolkit/.claude-plugin/plugin.json
✓ Validation: All checks passed

Next steps:
1. Review generated manifest
2. Package your skills: python scripts/package_skills.py
3. Validate: python scripts/validate_plugin.py team-toolkit/
```

**Tips**:
- Use semantic versioning (MAJOR.MINOR.PATCH)
- Include keywords for discoverability
- Add repository URL for open source plugins
- Keep description under 200 characters
- Use kebab-case for plugin name

**See Also**:
- [references/plugin-json-schema.md](references/plugin-json-schema.md) - Complete field reference
- [templates/](templates/) - All manifest templates

---

### Operation 3: Generate marketplace.json

Create a marketplace catalog file for distributing one or more plugins.

**Purpose**: Set up a marketplace for team/community distribution of plugins

**When to Use**:
- Distributing plugins via GitHub repository
- Creating team marketplace
- Publishing multiple plugins
- Setting up plugin catalog

**Prerequisites**:
- One or more plugins ready for distribution
- Marketplace name decided
- Owner information available

**Inputs**:
- Marketplace name (required)
- Owner name and email (required)
- Plugin entries (required):
  - Plugin name
  - Source (path, GitHub repo, or git URL)
  - Description
  - Category (optional)
  - Version (optional)

**Process**:

**Method 1: Interactive Script (Recommended)**
```bash
python scripts/generate_marketplace.py
```

Follow prompts:
1. Marketplace name (kebab-case)
2. Marketplace description
3. Owner name and email
4. Plugin source directory (optional, for auto-discovery)
5. For each plugin:
   - Name
   - Source (local path, GitHub, git URL)
   - Description
   - Category
   - Version

**Method 2: Auto-Discover Plugins**
```bash
python scripts/generate_marketplace.py --scan plugins/
```

Automatically finds plugins in directory and prompts for metadata.

**Method 3: Manual Creation**

Copy from [templates/marketplace.json.minimal](templates/marketplace.json.minimal) and edit:
```json
{
  "name": "my-marketplace",
  "description": "Curated plugins for my team",
  "owner": {
    "name": "Team Name",
    "email": "team@company.com"
  },
  "plugins": [
    {
      "name": "plugin-one",
      "description": "First plugin",
      "source": "./plugins/plugin-one",
      "category": "development"
    }
  ]
}
```

Save to repository root as `.claude-plugin/marketplace.json`.

**Outputs**:
- Valid `marketplace.json` file
- All plugins listed with metadata
- Ready for Git repository hosting

**Validation**:
- [ ] JSON syntax valid
- [ ] Required fields present (name, owner, plugins)
- [ ] All plugin sources are valid
- [ ] Plugin names are kebab-case
- [ ] Categories are standard (development, productivity, security, learning)

**Example**:
```bash
$ python scripts/generate_marketplace.py --scan company-plugins/

Generating marketplace.json
===========================

Scanning company-plugins/ for plugins...
Found 3 plugins:
  - deployment-tools
  - security-scanner
  - test-automation

Marketplace name: company-approved-plugins
Marketplace description: Approved plugins for Company use
Owner name: Engineering Team
Owner email: engineering@company.com

Plugin 1: deployment-tools
  Description: Automated deployment and rollback tools
  Category [development]:
  Version [1.0.0]: 2.1.0
  Source [./plugins/deployment-tools]:

Plugin 2: security-scanner
  Description: Security analysis and vulnerability detection
  Category [security]:
  Version [1.0.0]: 1.5.0
  Source [./plugins/security-scanner]:

Plugin 3: test-automation
  Description: Automated testing framework and utilities
  Category [development]:
  Version [1.0.0]: 3.0.0
  Source [./plugins/test-automation]:

Generated marketplace.json (3 plugins)
✓ Saved to .claude-plugin/marketplace.json
✓ Validation: All checks passed

Next steps:
1. Create GitHub repository
2. Push marketplace.json to repo root
3. Users can add: /plugin marketplace add company/company-plugins
4. Users can install: /plugin install deployment-tools@company-approved-plugins
```

**Distribution Setup**:

After generating marketplace.json:

1. **Create GitHub Repository**:
```bash
cd /path/to/marketplace
git init
git add .
git commit -m "Initial marketplace setup"
git remote add origin git@github.com:username/my-marketplace.git
git push -u origin main
```

2. **Users Add Marketplace**:
```
/plugin marketplace add username/my-marketplace
```

3. **Users Install Plugins**:
```
/plugin install plugin-name@my-marketplace
```

**See Also**:
- [references/marketplace-json-schema.md](references/marketplace-json-schema.md) - Complete schema
- [references/distribution-guide.md](references/distribution-guide.md) - Setup instructions
- [templates/marketplace.json.multi](templates/marketplace.json.multi) - Multi-plugin example

---

### Operation 4: Validate Plugin

Comprehensive validation of plugin structure, manifests, and component compliance.

**Purpose**: Ensure plugin is correctly structured and ready for distribution

**When to Use**:
- Before publishing to marketplace
- After making changes to plugin
- Before creating GitHub release
- Troubleshooting plugin issues
- Ensuring 2025 schema compliance

**Prerequisites**:
- Plugin directory exists
- plugin.json file exists

**Inputs**:
- Plugin directory path

**Process**:

**Method 1: Script Validation (Comprehensive)**
```bash
python scripts/validate_plugin.py /path/to/my-plugin
```

**Method 2: Verbose Output**
```bash
python scripts/validate_plugin.py /path/to/my-plugin --verbose
```

Shows detailed checks and reasoning.

**Method 3: Specific Validation Type**
```bash
# Structure only
python scripts/validate_plugin.py /path/to/my-plugin --check structure

# Manifests only
python scripts/validate_plugin.py /path/to/my-plugin --check manifests

# Components only (skills, commands, agents)
python scripts/validate_plugin.py /path/to/my-plugin --check components

# 2025 schema compliance
python scripts/validate_plugin.py /path/to/my-plugin --check 2025
```

**Validation Categories**:

**1. Structure Validation**:
- [x] `.claude-plugin/` directory exists
- [x] `plugin.json` exists in `.claude-plugin/`
- [x] Component directories at plugin root (NOT in `.claude-plugin/`)
- [x] Directory names are kebab-case
- [x] README.md exists (recommended)

**2. Manifest Validation**:
- [x] `plugin.json` is valid JSON
- [x] Required field `name` present
- [x] Name is kebab-case (no spaces, underscores)
- [x] Version follows semver if present
- [x] No absolute paths (all paths relative with `./`)
- [x] Referenced files in manifest actually exist

**3. Component Validation**:
- [x] Skills have `SKILL.md` files
- [x] Skills have valid YAML frontmatter
- [x] Skills have `allowed-tools` field (2025 schema)
- [x] Commands have valid markdown with frontmatter
- [x] Agents have proper markdown structure
- [x] No placeholder TODO comments in production files

**4. 2025 Schema Compliance**:
- [x] All skills have `allowed-tools` field in frontmatter
- [x] `allowed-tools` lists valid Claude Code tools
- [x] Frontmatter format is correct

**Outputs**:

**Success Example**:
```
Validating plugin: team-toolkit
================================

✓ Structure validation passed (5/5 checks)
  ✓ .claude-plugin/ directory exists
  ✓ plugin.json exists
  ✓ Component directories at root
  ✓ Directory names valid
  ✓ README.md present

✓ Manifest validation passed (6/6 checks)
  ✓ Valid JSON syntax
  ✓ Required fields present
  ✓ Name format valid
  ✓ Version format valid
  ✓ Paths are relative
  ✓ Referenced files exist

✓ Component validation passed (8 skills, 3 commands)
  ✓ All skills have SKILL.md
  ✓ All skills have valid frontmatter
  ✓ All skills have allowed-tools field
  ✓ All commands valid

✓ 2025 schema compliance passed

================
RESULT: PASSED
================
0 errors, 0 warnings

✓ Plugin is ready for distribution!
```

**Error Example**:
```
Validating plugin: my-plugin
============================

✗ Structure validation failed (4/5 checks)
  ✓ .claude-plugin/ directory exists
  ✓ plugin.json exists
  ✗ Component directories at root
    ERROR: skills/ directory found in .claude-plugin/ (should be at plugin root)
  ✓ Directory names valid
  ✓ README.md present

✗ Manifest validation failed (5/6 checks)
  ✓ Valid JSON syntax
  ✓ Required fields present
  ✗ Paths are relative
    ERROR: "commands" field has absolute path: /home/user/commands
    FIX: Change to relative path: ./commands
  ✓ Referenced files exist

✗ Component validation failed (2/3 skills)
  ✓ All skills have SKILL.md
  ✗ Skills missing allowed-tools field
    ERROR: skills/my-skill/SKILL.md missing allowed-tools in frontmatter
    FIX: Add "allowed-tools: Read, Write, Bash" to YAML frontmatter

================
RESULT: FAILED
================
3 errors, 0 warnings

Fix errors above before distributing plugin.
```

**Exit Codes**:
- `0`: All validation passed, plugin ready
- `1`: Errors found, plugin not ready
- `2`: Script execution error

**Common Errors and Fixes**:

**Error**: Component directory in `.claude-plugin/`
```
ERROR: skills/ found in .claude-plugin/ (should be at plugin root)
FIX: Move skills/ to plugin root directory
```

**Error**: Absolute paths in manifest
```
ERROR: "skills" field has absolute path: /Users/me/skills
FIX: Change to relative path: ./skills
```

**Error**: Missing `allowed-tools` field
```
ERROR: skill missing allowed-tools in frontmatter (2025 schema)
FIX: Add to SKILL.md frontmatter:
---
name: my-skill
description: ...
allowed-tools: Read, Write, Glob, Bash
---
```

**Error**: Invalid JSON syntax
```
ERROR: plugin.json has invalid JSON (trailing comma)
FIX: Remove trailing comma in JSON file
```

**Error**: Non-kebab-case name
```
ERROR: Plugin name "my_plugin" should be kebab-case
FIX: Change name to "my-plugin"
```

**Validation Checklist**:

Before publishing, ensure all pass:
- [ ] Structure validation: 0 errors
- [ ] Manifest validation: 0 errors
- [ ] Component validation: 0 errors
- [ ] 2025 compliance: All skills have allowed-tools
- [ ] README exists and is complete
- [ ] Test installation locally

**See Also**:
- [references/validation-rules.md](references/validation-rules.md) - Complete validation rules
- [references/plugin-json-schema.md](references/plugin-json-schema.md) - Schema reference

---

### Operation 5: Package Skills

Copy existing skills into plugin structure and update manifest.

**Purpose**: Convert standalone skills into plugin-packaged skills ready for distribution

**When to Use**:
- Converting `.claude/skills/` to plugin format
- Packaging skill collections
- Migrating existing skills to plugins
- Creating skill-focused plugins

**Prerequisites**:
- Plugin structure initialized
- Skills exist in source directory
- Skills are 2025-compliant (or will be validated and flagged)

**Inputs**:
- Source skills directory path
- Target plugin path
- Optional: Specific skills to package (default: all)
- Optional: Validation mode (strict/warn)

**Process**:

**Method 1: Package All Skills**
```bash
python scripts/package_skills.py /path/to/skills /path/to/plugin
```

Copies all skills from source to plugin/skills/ directory.

**Method 2: Package Specific Skills**
```bash
python scripts/package_skills.py /path/to/skills /path/to/plugin \
  --skills skill1,skill2,skill3
```

**Method 3: Package with Validation**
```bash
python scripts/package_skills.py /path/to/skills /path/to/plugin --validate
```

Validates each skill for 2025 compliance before packaging.

**Method 4: Dry Run (Preview)**
```bash
python scripts/package_skills.py /path/to/skills /path/to/plugin --dry-run
```

Shows what would be packaged without actually copying.

**What Happens**:

1. **Scans Source Directory**:
   - Finds all skill directories
   - Identifies skills with SKILL.md files
   - Lists skills to be packaged

2. **Validates Skills** (if --validate):
   - Checks SKILL.md exists
   - Validates YAML frontmatter
   - Checks for `allowed-tools` field (2025 schema)
   - Reports warnings for missing fields

3. **Copies Skills**:
   - Creates plugin/skills/ if doesn't exist
   - Copies each skill directory
   - Preserves structure (SKILL.md, references/, scripts/)
   - Copies all files (no modification)

4. **Updates Manifest**:
   - Adds skills to plugin.json
   - Updates skills array (if field exists)
   - Preserves existing manifest fields

5. **Reports Results**:
   - Number of skills packaged
   - Any warnings or issues
   - Next steps

**Outputs**:
```
plugin/
├── .claude-plugin/
│   └── plugin.json          # Updated with skills reference
├── skills/
│   ├── skill1/
│   │   ├── SKILL.md
│   │   ├── references/
│   │   └── scripts/
│   ├── skill2/
│   │   └── SKILL.md
│   └── skill3/
│       ├── SKILL.md
│       └── references/
└── README.md
```

**Validation**:
- [ ] All skills copied successfully
- [ ] Directory structure preserved
- [ ] SKILL.md files exist in each skill
- [ ] plugin.json updated (if applicable)
- [ ] 2025 compliance checked

**Example**:
```bash
$ python scripts/package_skills.py .claude/skills skrillz-ecosystem --validate

Packaging skills into plugin: skrillz-ecosystem
==============================================

Scanning .claude/skills for skills...
Found 32 skills:
  ✓ analysis
  ✓ anthropic-expert
  ✓ auto-updater
  ... (29 more)

Validating skills (2025 schema compliance)...
  ✓ analysis: Valid (allowed-tools present)
  ✓ anthropic-expert: Valid (allowed-tools present)
  ⚠ legacy-skill: WARNING - Missing allowed-tools field
  ... (checking all 32)

Results: 31 valid, 1 warning

Packaging skills...
  ✓ Copied analysis (245 KB, 3 files)
  ✓ Copied anthropic-expert (1.2 MB, 12 files)
  ✓ Copied auto-updater (180 KB, 5 files)
  ... (29 more)

✓ 32 skills packaged successfully
✓ Total size: 15.8 MB
✓ Updated plugin.json

Warnings:
  ⚠ legacy-skill missing allowed-tools field (2025 compliance)
    Add to SKILL.md frontmatter: allowed-tools: Read, Write, Bash

Next steps:
1. Fix warnings (add allowed-tools to legacy-skill)
2. Review plugin/skills/ directory
3. Update README.md with skill list
4. Validate: python scripts/validate_plugin.py skrillz-ecosystem
5. Test: /plugin install skrillz-ecosystem (local test)
```

**Handling 2025 Compliance**:

If skills are missing `allowed-tools` field:

1. **Manual Fix**: Add to SKILL.md frontmatter:
```yaml
---
name: my-skill
description: Skill description
allowed-tools: Read, Write, Edit, Glob, Bash
---
```

2. **Common Tool Sets**:
- **Read-only analysis**: `Read, Grep, Glob`
- **File editing**: `Read, Write, Edit`
- **Automation**: `Read, Write, Bash`
- **Research**: `Read, WebSearch, WebFetch`
- **All tools**: `Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch`

3. **Re-package** after fixing:
```bash
python scripts/package_skills.py .claude/skills plugin --validate
```

**Tips**:
- Use `--validate` to catch issues early
- Use `--dry-run` to preview before packaging
- Fix 2025 compliance warnings before distribution
- Keep original skills as backup
- Test plugin installation locally before publishing

**See Also**:
- [references/component-packaging-guide.md](references/component-packaging-guide.md) - Detailed packaging guide
- [references/validation-rules.md](references/validation-rules.md) - 2025 compliance rules

---

## Best Practices

### Plugin Development

**1. Start with MVP**:
- Get basic plugin working first
- Add optional metadata later
- Test early, test often

**2. Use Semantic Versioning**:
- Format: MAJOR.MINOR.PATCH (e.g., 1.2.3)
- MAJOR: Breaking changes
- MINOR: New features, backward compatible
- PATCH: Bug fixes

**3. Write Good Descriptions**:
- Clear, concise (under 200 chars)
- Explain what plugin does
- Mention key features
- Include use cases

**4. Include Comprehensive README**:
- Installation instructions
- Usage examples
- List of components
- Configuration options
- Troubleshooting

**5. Validate Before Publishing**:
```bash
python scripts/validate_plugin.py my-plugin/
# Should show 0 errors
```

**6. Test Installation Locally**:
```bash
# Create local marketplace
python scripts/generate_marketplace.py

# Test installation (if possible)
/plugin marketplace add ./my-marketplace
/plugin install my-plugin
```

### Manifest Best Practices

**1. Always Include**:
- `name`: Clear, kebab-case identifier
- `version`: Semantic version
- `description`: What it does
- `author`: Who maintains it

**2. Highly Recommended**:
- `keywords`: For discoverability
- `license`: Legal clarity (MIT, Apache-2.0, etc.)
- `repository`: Source code location
- `homepage`: Documentation URL

**3. Path Rules**:
- Always use relative paths: `./skills/`
- Never use absolute paths: `/Users/me/skills`
- Use forward slashes (cross-platform): `./path/to/file`

**4. Naming Conventions**:
- Plugin names: `kebab-case`
- No spaces, underscores, or special chars
- Descriptive and memorable

### 2025 Schema Compliance

**1. All Skills Must Have allowed-tools**:
```yaml
---
name: my-skill
description: What it does
allowed-tools: Read, Write, Bash
---
```

**2. Common Tool Combinations**:
- Analysis: `Read, Grep, Glob`
- Editing: `Read, Write, Edit`
- Automation: `Read, Write, Bash`
- Research: `Read, WebSearch, WebFetch`

**3. Be Specific**:
- Only list tools skill actually uses
- Don't include all tools if not needed
- Helps Claude optimize execution

### Distribution Best Practices

**1. GitHub Repository Setup**:
- Clear repository name
- Comprehensive README.md
- LICENSE file
- .gitignore for OS files

**2. Version Management**:
- Tag releases: `git tag v1.0.0`
- Write changelogs
- Follow semver strictly

**3. Documentation**:
- Installation instructions
- Usage examples
- Component documentation
- Troubleshooting guide

**4. Team Distribution**:
- Use `.claude/settings.json` for team-wide:
```json
{
  "extraKnownMarketplaces": [
    {"source": "github", "repo": "company/approved-plugins"}
  ]
}
```

## Common Mistakes

### Mistake 1: Component Directories in Wrong Location

**❌ Wrong**:
```
my-plugin/
└── .claude-plugin/
    ├── plugin.json
    └── skills/          # WRONG LOCATION
```

**✅ Correct**:
```
my-plugin/
├── .claude-plugin/
│   └── plugin.json
└── skills/              # AT PLUGIN ROOT
```

**Why**: Claude looks for components at plugin root, not in `.claude-plugin/`

**Fix**: Move component directories to plugin root

---

### Mistake 2: Absolute Paths in Manifests

**❌ Wrong**:
```json
{
  "name": "my-plugin",
  "skills": "/Users/me/my-plugin/skills"
}
```

**✅ Correct**:
```json
{
  "name": "my-plugin",
  "skills": "./skills"
}
```

**Why**: Absolute paths break on other machines

**Fix**: Use relative paths starting with `./`

---

### Mistake 3: Non-Kebab-Case Names

**❌ Wrong**:
```json
{
  "name": "My_Plugin"     // Underscores and capitals
}
```

**✅ Correct**:
```json
{
  "name": "my-plugin"     // Kebab-case
}
```

**Why**: Naming convention expected by Claude Code

**Fix**: Use lowercase with hyphens

---

### Mistake 4: Missing allowed-tools (2025 Schema)

**❌ Wrong**:
```yaml
---
name: my-skill
description: What it does
---
```

**✅ Correct**:
```yaml
---
name: my-skill
description: What it does
allowed-tools: Read, Write, Bash
---
```

**Why**: 2025 schema requires explicit tool permissions

**Fix**: Add `allowed-tools` field to all skills

---

### Mistake 5: Invalid JSON Syntax

**❌ Wrong**:
```json
{
  "name": "my-plugin",
  "version": "1.0.0",    // Trailing comma
}
```

**✅ Correct**:
```json
{
  "name": "my-plugin",
  "version": "1.0.0"
}
```

**Why**: JSON doesn't allow trailing commas

**Fix**: Remove trailing commas, validate JSON

---

### Mistake 6: No README

**❌ Wrong**:
```
my-plugin/
├── .claude-plugin/plugin.json
└── skills/
```

**✅ Correct**:
```
my-plugin/
├── .claude-plugin/plugin.json
├── README.md           # Installation & usage
└── skills/
```

**Why**: Users need to understand what plugin does and how to install it

**Fix**: Create README with installation instructions

---

### Mistake 7: Not Validating Before Publishing

**❌ Wrong**:
```bash
git push origin main    # Push without validation
```

**✅ Correct**:
```bash
python scripts/validate_plugin.py my-plugin/
# Fix any errors
git push origin main
```

**Why**: Catch errors before users try to install

**Fix**: Always validate before publishing

---

### Mistake 8: No Version Bumping

**❌ Wrong**:
```json
{
  "version": "1.0.0"     // Never changes
}
```

**✅ Correct**:
```json
{
  "version": "1.1.0"     // Bumped for each release
}
```

**Why**: Users need to know when updates are available

**Fix**: Bump version for each release following semver

---

## Quick Reference

### Essential Commands

```bash
# Initialize new plugin
python scripts/init_plugin.py my-plugin

# Generate manifest (interactive)
python scripts/generate_manifest.py my-plugin/

# Generate marketplace
python scripts/generate_marketplace.py

# Validate plugin
python scripts/validate_plugin.py my-plugin/

# Package skills
python scripts/package_skills.py .claude/skills my-plugin/

# Package with validation
python scripts/package_skills.py .claude/skills my-plugin/ --validate
```

### Plugin Structure

```
plugin-name/
├── .claude-plugin/
│   ├── plugin.json           # Required: Metadata
│   └── marketplace.json      # Optional: Distribution
├── skills/                    # Your skills
├── commands/                  # Custom slash commands
├── agents/                    # Specialized agents
└── README.md                  # Recommended: Docs
```

### plugin.json Minimal

```json
{
  "name": "my-plugin"
}
```

### plugin.json Standard

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "What this plugin does",
  "author": {
    "name": "Your Name",
    "email": "you@example.com"
  },
  "keywords": ["keyword1", "keyword2"],
  "license": "MIT"
}
```

### marketplace.json

```json
{
  "name": "my-marketplace",
  "description": "Plugin marketplace",
  "owner": {
    "name": "Maintainer",
    "email": "maintainer@example.com"
  },
  "plugins": [
    {
      "name": "plugin-one",
      "description": "First plugin",
      "source": "./plugins/plugin-one",
      "category": "development"
    }
  ]
}
```

### 2025 Skill Frontmatter

```yaml
---
name: my-skill
description: What it does. Use when [triggers].
allowed-tools: Read, Write, Bash
---
```

### Validation Checklist

Before publishing:
- [ ] Run `python scripts/validate_plugin.py my-plugin/`
- [ ] 0 errors, 0 warnings
- [ ] README.md exists and is complete
- [ ] All skills have allowed-tools field
- [ ] Version number bumped (if updating)
- [ ] Git tag created for release
- [ ] Test installation locally

### Distribution Workflow

1. **Create Plugin**:
   ```bash
   python scripts/init_plugin.py my-plugin
   python scripts/generate_manifest.py my-plugin/
   python scripts/package_skills.py .claude/skills my-plugin/
   ```

2. **Validate**:
   ```bash
   python scripts/validate_plugin.py my-plugin/
   ```

3. **Create Marketplace**:
   ```bash
   python scripts/generate_marketplace.py
   ```

4. **Push to GitHub**:
   ```bash
   cd my-marketplace
   git init
   git add .
   git commit -m "Initial plugin marketplace"
   git remote add origin git@github.com:username/my-marketplace.git
   git push -u origin main
   ```

5. **Users Install**:
   ```
   /plugin marketplace add username/my-marketplace
   /plugin install my-plugin@my-marketplace
   ```

### Common Tool Sets (2025)

- **Read-only**: `Read, Grep, Glob`
- **File editing**: `Read, Write, Edit`
- **Automation**: `Read, Write, Bash`
- **Research**: `Read, WebSearch, WebFetch`
- **Full access**: `Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch`

### Script Help

All scripts support `--help`:
```bash
python scripts/init_plugin.py --help
python scripts/generate_manifest.py --help
python scripts/validate_plugin.py --help
python scripts/package_skills.py --help
```

---

## Next Steps After MVP

This MVP includes the core operations needed to package and distribute plugins. Future enhancements could include:

**Additional Operations**:
- Package commands (Operation 6)
- Package agents (Operation 7)
- Update existing plugin (Operation 9)
- Bulk package multiple plugins (Operation 10)

**Enhanced Features**:
- Automated GitHub repo creation
- Change log generation
- Dependency resolution
- Plugin analytics

**For Now**:
The MVP operations (1-5) are sufficient to:
- Create plugins
- Package your 32 skills
- Distribute via GitHub
- Validate compliance
- Share with team or community

---

## References

Detailed guides for advanced topics:

- **[plugin-json-schema.md](references/plugin-json-schema.md)** - Complete field reference, all options, examples
- **[marketplace-json-schema.md](references/marketplace-json-schema.md)** - Marketplace structure, source types, plugin entries
- **[validation-rules.md](references/validation-rules.md)** - All validation checks, error fixes, 2025 compliance

---

**plugin-builder** makes plugin creation fast, validated, and reliable. Use it to package your skills and share them with your team or the community!
