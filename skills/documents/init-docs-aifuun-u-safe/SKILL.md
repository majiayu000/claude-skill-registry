---
name: init-docs
version: "1.0.0"
description: |
  Auto-generate standard documentation structure for projects with profile-aware customization.
  TRIGGER when: user wants to initialize documentation ("initialize docs", "create documentation structure", "set up docs").
  DO NOT TRIGGER when: user wants to check existing docs (use /check-docs).
allowed-tools: Bash(mkdir *), Bash(cp *), Bash(ls *), Read, Write, Glob
disable-model-invocation: false
user-invocable: true
---

# Init Docs - Auto-generate Documentation Structure

Auto-generate standard documentation structure for projects with profile-aware customization.

## Overview

This skill automatically creates a comprehensive documentation structure following the framework's documentation standards:

**What it does:**
1. **Auto-detects project profile** from `.framework-install` (tauri, tauri-aws, nextjs-aws)
2. **Creates standard directories** - docs/ADRs/, docs/architecture/, docs/api/, docs/guides/, docs/diagrams/
3. **Generates template files** - README, PRD, ARCHITECTURE, SCHEMA, API, SETUP, TEST_PLAN, DEPLOYMENT
4. **Copies documentation manual** - DOCUMENTATION_MANUAL.md from framework to target project
5. **Substitutes variables** - projectName, profile, techStack from project context
6. **Handles existing content** gracefully with --force option
7. **Supports dry-run** preview mode

**Why it's needed:**
Starting a new project requires creating consistent documentation structure. Manual setup is error-prone, inconsistent across projects, and time-consuming (15-30 minutes). This skill automates the entire process in <10 seconds.

**When to use:**
- Starting a new project after running `init-project.py`
- Adding documentation to an existing project
- Standardizing documentation across multiple projects
- User says "initialize docs", "create documentation structure", "set up docs"

**When NOT to use:**
- Project already has docs/ directory (use --force to override)
- Custom documentation structure needed (manual setup recommended)
- Quick prototype without documentation needs

## Arguments

```bash
/init-docs [options]
```

**Common usage:**
```bash
/init-docs                    # Auto-detect profile
/init-docs --profile tauri    # Specify profile explicitly
/init-docs --dry-run          # Preview without creating
/init-docs --force            # Overwrite existing docs/
/init-docs --minimal          # Create minimal structure only
```

**Options:**
- `--profile <name>` - Specify profile explicitly (tauri, tauri-aws, nextjs-aws)
- `--dry-run` - Preview actions without creating files
- `--force` - Overwrite existing docs/ directory
- `--minimal` - Create minimal structure (directories only, no template files)

## AI Execution Instructions

**CRITICAL: Profile detection and template processing**

When executing `/init-docs`, AI MUST follow this pattern:

### Step 1: Detect Project Profile

```python
# Read .framework-install to get profile
if os.path.exists('.framework-install'):
    with open('.framework-install', 'r') as f:
        data = json.load(f)
        profile = data.get('profile', 'tauri')  # Default to tauri
else:
    # Ask user or use argument
    if '--profile' in args:
        profile = args['--profile']
    else:
        profile = AskUserQuestion("Which profile?", ["tauri", "tauri-aws", "nextjs-aws"])
```

### Step 2: Validate Environment

```python
# Check if docs/ already exists
if os.path.exists('docs/') and not args.get('--force'):
    print("❌ docs/ directory already exists")
    print("Use --force to overwrite or --dry-run to preview")
    return

# Check if in project root
if not os.path.exists('.git') and not os.path.exists('package.json'):
    print("⚠️  Not in project root?")
    confirm = AskUserQuestion("Continue anyway?", ["Yes", "No"])
    if confirm == "No":
        return
```

### Step 3: Create Directory Structure

```python
directories = [
    'docs',
    'docs/ADRs',
    'docs/architecture',
    'docs/api',
    'docs/guides',
    'docs/diagrams'
]

# Profile-specific additions
if profile == 'tauri':
    directories.append('docs/desktop')
elif profile in ['tauri-aws', 'nextjs-aws']:
    directories.extend(['docs/aws', 'docs/deployment'])

for dir_path in directories:
    if args.get('--dry-run'):
        print(f"Would create: {dir_path}/")
    else:
        os.makedirs(dir_path, exist_ok=True)
        print(f"✓ Created: {dir_path}/")
```

### Step 4: Generate Template Files

```python
# Template file list
templates = [
    ('README.md', 'Navigation hub'),
    ('PRD.md', 'Product requirements'),
    ('ARCHITECTURE.md', 'System overview'),
    ('SCHEMA.md', 'Data models'),
    ('API.md', 'API endpoints'),
    ('SETUP.md', 'Installation guide'),
    ('TEST_PLAN.md', 'Testing strategy'),
    ('DEPLOYMENT.md', 'Deployment guide')
]

# Skip if --minimal flag
if args.get('--minimal'):
    print("Skipping template files (--minimal mode)")
    return

# Load templates and substitute variables
project_name = get_project_name()  # From package.json or directory name
tech_stack = get_tech_stack(profile)  # Profile-specific stack

for template_name, description in templates:
    template_path = f'framework/.prot-template/docs-templates/{template_name}.template'

    if os.path.exists(template_path):
        content = load_template(template_path)
        # Variable substitution
        content = content.replace('{{projectName}}', project_name)
        content = content.replace('{{profile}}', profile)
        content = content.replace('{{techStack}}', tech_stack)

        output_path = f'docs/{template_name}'

        if args.get('--dry-run'):
            print(f"Would create: {output_path} ({description})")
        else:
            with open(output_path, 'w') as f:
                f.write(content)
            print(f"✓ Created: {output_path}")
    else:
        # Template not found - create stub
        print(f"⚠️  Template missing: {template_name}, creating stub")
        create_stub_file(f'docs/{template_name}', description)
```

### Step 5: Create ADR Index

```python
# Create ADR index file
adr_readme = """# Architecture Decision Records (ADRs)

This directory contains Architecture Decision Records for this project.

## Index

| # | Title | Status | Date |
|---|-------|--------|------|
| - | - | - | - |

## How to Create New ADRs

Use the `/adr` skill:

```bash
/adr "Title of decision"
```

Or manually create files following the template in `framework/.prot-template/adr-template.md`.

## ADR Lifecycle

- **Proposed** - Under discussion
- **Accepted** - Approved and implemented
- **Deprecated** - No longer relevant
- **Superseded** - Replaced by newer ADR
"""

if args.get('--dry-run'):
    print("Would create: docs/ADRs/README.md")
else:
    with open('docs/ADRs/README.md', 'w') as f:
        f.write(adr_readme)
    print("✓ Created: docs/ADRs/README.md")
```

### Step 6: Report Success

```python
print("""
🎉 Documentation structure created successfully!

Structure:
docs/
├── ADRs/           # Architecture decisions
├── architecture/   # System design docs
├── api/            # API documentation
├── guides/         # User guides
├── diagrams/       # Architecture diagrams
├── README.md       # Navigation hub
├── PRD.md          # Product requirements
├── ARCHITECTURE.md # System overview
├── SCHEMA.md       # Data models
├── API.md          # API endpoints
├── SETUP.md        # Installation
├── TEST_PLAN.md    # Testing strategy
└── DEPLOYMENT.md   # Deployment guide

Next steps:
1. Review generated files: ls docs/
2. Customize templates with project-specific content
3. Validate structure: /check-docs
4. Start documenting!

Profile: {profile}
Files created: {file_count}
""")
```

## Workflow Steps

Copy this checklist when executing:

```
Task Progress:
- [ ] Step 1: Detect project profile
- [ ] Step 2: Validate environment
- [ ] Step 3: Create directory structure
- [ ] Step 4: Generate template files (unless --minimal)
- [ ] Step 4.5: Copy DOCUMENTATION_MANUAL.md
- [ ] Step 5: Create ADR index
- [ ] Step 6: Report success
```

Execute in sequence with progress tracking.

### Step 1: Detect Project Profile

**Auto-detection:**
```bash
# Check for .framework-install
if [ -f .framework-install ]; then
    PROFILE=$(jq -r '.profile' .framework-install)
else
    PROFILE="tauri"  # Default
fi
```

**If --profile flag provided:**
- Override auto-detection
- Validate profile name (tauri, tauri-aws, nextjs-aws)
- Abort if invalid

**Output:** Profile name (tauri, tauri-aws, or nextjs-aws)

### Step 2: Validate Environment

**Checks:**
1. Not already initialized
   ```bash
   if [ -d docs/ ] && [ "$FORCE" != "true" ]; then
       echo "❌ docs/ already exists. Use --force to overwrite"
       exit 1
   fi
   ```

2. In project root (optional check)
   ```bash
   if [ ! -f package.json ] && [ ! -f .git ]; then
       echo "⚠️  Not in project root?"
       # Ask user or continue
   fi
   ```

3. Template directory accessible
   ```bash
   if [ ! -d framework/.prot-template/docs-templates/ ]; then
       echo "⚠️  Template directory not found"
       echo "Creating stub templates instead"
   fi
   ```

**Abort if:** Critical checks fail (unless --force)

### Step 3: Create Directory Structure

**Standard directories (all profiles):**
```
docs/
├── ADRs/
├── architecture/
├── api/
├── guides/
└── diagrams/
```

**Profile-specific additions:**

**tauri profile:**
```
docs/desktop/  # Desktop app specific docs
```

**tauri-aws and nextjs-aws profiles:**
```
docs/aws/        # AWS infrastructure docs
docs/deployment/ # Deployment procedures
```

**Execution:**
```bash
for dir in "${DIRS[@]}"; do
    if [ "$DRY_RUN" = "true" ]; then
        echo "Would create: $dir/"
    else
        mkdir -p "$dir"
        echo "✓ Created: $dir/"
    fi
done
```

### Step 4: Generate Template Files

**Template files (9 total - 8 templates + DOCUMENTATION_MANUAL.md):**

1. **README.md** - Documentation navigation hub
   ```markdown
   # {{projectName}} Documentation

   ## Quick Links
   - [Product Requirements](PRD.md)
   - [Architecture Overview](ARCHITECTURE.md)
   - [API Documentation](API.md)
   - [Setup Instructions](SETUP.md)
   ```

2. **PRD.md** - Product requirements document
   ```markdown
   # Product Requirements Document

   ## Overview
   {{projectDescription}}

   ## User Stories
   - As a user, I want to...
   ```

3. **ARCHITECTURE.md** - System architecture overview
   ```markdown
   # Architecture Overview

   ## Tech Stack
   {{techStack}}

   ## Component Diagram
   [Placeholder for diagram]
   ```

4. **SCHEMA.md** - Data models and schemas
   ```markdown
   # Data Schema

   ## Entities
   [Define your data models here]
   ```

5. **API.md** - API endpoint documentation
   ```markdown
   # API Documentation

   ## Endpoints
   [List your API endpoints]
   ```

6. **SETUP.md** - Installation and setup guide
   ```markdown
   # Setup Guide

   ## Prerequisites
   - Node.js 18+
   - {{additionalPrereqs}}

   ## Installation
   \`\`\`bash
   npm install
   \`\`\`
   ```

7. **TEST_PLAN.md** - Testing strategy
   ```markdown
   # Test Plan

   ## Test Strategy
   - Unit tests: 80% coverage
   - Integration tests: Critical paths
   ```

8. **DEPLOYMENT.md** - Deployment procedures
   ```markdown
   # Deployment Guide

   ## Environments
   - Development
   - Staging
   - Production
   ```

**Variable substitution:**
- `{{projectName}}` - From package.json name or directory name
- `{{profile}}` - Detected profile
- `{{techStack}}` - Profile-specific tech stack
- `{{projectDescription}}` - From package.json description

**Template loading:**
```bash
TEMPLATE_DIR="framework/.prot-template/docs-templates"

if [ -f "$TEMPLATE_DIR/${filename}.template" ]; then
    sed -e "s/{{projectName}}/$PROJECT_NAME/g" \
        -e "s/{{profile}}/$PROFILE/g" \
        "$TEMPLATE_DIR/${filename}.template" > "docs/$filename"
else
    # Create stub
    create_stub "docs/$filename"
fi
```

**Skip if --minimal:** Only create directories, no files

### Step 4.5: Copy Documentation Manual

**Purpose:** Copy the documentation standards reference from framework to target project.

**Source file:** `docs/DOCUMENTATION_MANUAL.md` (in framework)
**Target location:** `docs/DOCUMENTATION_MANUAL.md` (in target project)

**Copy operation:**
```bash
# Define paths
SOURCE_MANUAL="$FRAMEWORK_ROOT/docs/DOCUMENTATION_MANUAL.md"
TARGET_MANUAL="$TARGET_PROJECT/docs/DOCUMENTATION_MANUAL.md"

# Check if source exists
if [ -f "$SOURCE_MANUAL" ]; then
    if [ "$DRY_RUN" = "true" ]; then
        echo "Would copy: DOCUMENTATION_MANUAL.md"
    else
        cp "$SOURCE_MANUAL" "$TARGET_MANUAL"
        echo "✓ Copied: DOCUMENTATION_MANUAL.md"
    fi
else
    echo "⚠️  DOCUMENTATION_MANUAL.md not found in framework"
    echo "Expected: $SOURCE_MANUAL"
fi
```

**What the manual contains:**
- Standard documentation directory structure
- File naming conventions
- Required files checklist
- Quality checklist
- Examples and templates

**Why copy it:**
- Provides local reference for documentation standards
- Enables offline usage
- Required by `/maintain-project` skill for validation
- Ensures consistency across projects

**Skip if --minimal:** No, always copy (even in minimal mode for reference)

### Step 5: Create ADR Index

**ADR README.md:**
```markdown
# Architecture Decision Records (ADRs)

## Index
(Empty - add ADRs using /adr skill)

## How to Create ADRs
Use: /adr "Decision title"
```

**Location:** `docs/ADRs/README.md`

### Step 6: Report Success

**Success message:**
```
🎉 Documentation structure created!

Created:
✓ 6 directories
✓ 10 files (8 templates + DOCUMENTATION_MANUAL.md + ADR index)

Profile: tauri
Location: docs/

Next steps:
1. Review: ls docs/
2. Customize templates
3. Validate: /check-docs
```

**Dry-run message:**
```
📋 Dry Run Preview

Would create:
□ 6 directories
□ 10 files

Run without --dry-run to execute
```

## Error Handling

**docs/ already exists:**
```
❌ Documentation already initialized

Found: docs/ directory
Created: {date from .framework-install}

Options:
1. Use --force to overwrite
2. Use --dry-run to preview changes
3. Manually review docs/ contents
```

**Invalid profile:**
```
❌ Invalid profile: custom-profile

Valid profiles:
- tauri
- tauri-aws
- nextjs-aws

Fix: /init-docs --profile tauri
```

**Template directory missing:**
```
⚠️  Template directory not found

Expected: framework/.prot-template/docs-templates/
Actual: Not found

Creating stub templates instead...
```

**Permission denied:**
```
❌ Permission denied: docs/

Cause: Cannot write to current directory

Fix: Check directory permissions
```

## Examples

### Example 1: Auto-detect Profile

**User says:**
> "initialize documentation"

**Workflow:**
1. Read `.framework-install` → profile: tauri
2. Validate: no docs/ exists
3. Create 6 directories
4. Generate 9 template files
5. Substitute variables (projectName, profile)
6. Report success

**Output:**
```
🎉 Documentation structure created!

Profile: tauri (auto-detected)
Files: 10
Directories: 6

Next: Customize templates in docs/
```

**Time:** <10 seconds

### Example 2: Explicit Profile with Dry-run

**User says:**
> "preview documentation structure for nextjs-aws"

**Workflow:**
1. Parse: `--profile nextjs-aws --dry-run`
2. Validate: profile valid
3. Preview directory creation (no actual files)
4. Preview template generation
5. Show summary

**Output:**
```
📋 Dry Run Preview

Would create directories:
□ docs/
□ docs/ADRs/
□ docs/architecture/
□ docs/api/
□ docs/guides/
□ docs/diagrams/
□ docs/aws/              # nextjs-aws specific
□ docs/deployment/       # nextjs-aws specific

Would create files:
□ docs/README.md
□ docs/PRD.md
□ docs/DOCUMENTATION_MANUAL.md
... (7 more files)

Run without --dry-run to execute
```

**Time:** <5 seconds

### Example 3: Force Overwrite Existing

**User says:**
> "reinitialize documentation, overwrite existing"

**Workflow:**
1. Parse: `--force`
2. Validate: docs/ exists, --force flag present
3. Backup existing docs/ → docs.backup/
4. Delete docs/
5. Create new structure
6. Report success with backup location

**Output:**
```
⚠️  Existing docs/ backed up to docs.backup/

🎉 Documentation structure recreated!

Files: 10
Backup: docs.backup/ (restore if needed)

Next: Review new structure
```

**Time:** <10 seconds

### Example 4: Minimal Structure Only

**User says:**
> "create documentation folders only, no templates"

**Workflow:**
1. Parse: `--minimal`
2. Create directories only
3. Skip template generation
4. Create ADR index
5. Report

**Output:**
```
🎉 Minimal documentation structure created!

Created directories:
✓ docs/
✓ docs/ADRs/
✓ docs/architecture/
✓ docs/api/
✓ docs/guides/
✓ docs/diagrams/

Files: 1 (ADR index only)
Templates: Skipped (--minimal mode)

Next: Manually create documentation files
```

**Time:** <5 seconds

## Integration

**Pairs with /check-docs:**
```
/init-docs              # Create structure
/check-docs             # Validate compliance
```

**Workflow integration:**
```
Project Initialization:
1. python3 scripts/init-project.py --profile=tauri --name=my-app
2. /init-docs           # Auto-detects profile from step 1
3. /check-docs          # Validate structure
4. Customize templates
5. /check-docs          # Re-validate after customization
```

**Files created:**
- `docs/` - All documentation files
- `docs/ADRs/README.md` - ADR index

**Files read:**
- `.framework-install` - Profile detection
- `package.json` - Project name, description
- `framework/.prot-template/docs-templates/` - Template source

## Best Practices

1. **Run after init-project.py** - Ensures profile is set correctly
2. **Use --dry-run first** - Preview before creating
3. **Customize templates immediately** - Don't leave placeholders
4. **Validate with /check-docs** - Ensure compliance
5. **Update README.md** - Add project-specific navigation
6. **Create ADRs early** - Document decisions as you make them

## Performance

- **Auto-detect mode:** <10 seconds
- **With templates:** <15 seconds (depends on template count)
- **--minimal mode:** <5 seconds (directories only)
- **--dry-run:** <5 seconds (preview only)

Fast because:
- Simple file I/O operations
- Minimal validation checks
- Template substitution is straightforward

## Related Skills

- **/check-docs** - Validates documentation structure compliance
- **/adr** - Creates Architecture Decision Records
- **/init-project.py** - Project initialization (sets profile)

---

**Version:** 1.0.0
**Pattern:** Tool-Reference (generates files based on templates)
**Compliance:** ADR-001 ✅
**Last Updated:** 2026-03-15
**Changelog:**
- v1.0.0: Initial release - auto-generate documentation structure
