---
name: skill-library-manager
description: "Manage Claude skills lifecycle in the Skills_librairie repository at /Users/guillaumebld/Documents/Skills/Skills_librairie. Skills are organized in Skills/ directory by category (Meta-skill/, Automation/, Infrastructure-DevOps/, Development/, Design-Creative/, Communication/, Document-Generation/, AI-Agents/). Create new skills following best practices, search existing skills, manage versions with semantic versioning, sync with GitHub (GuillaumeBld/Skills_librairie), and install skills to Claude.ai or local directories. Use when creating skills for this specific library, searching for existing skills, updating skill versions, syncing with GitHub, or organizing your skill collection. Requires GitHub CLI (gh) for authentication. Repository path: /Users/guillaumebld/Documents/Skills/Skills_librairie"
---

# Skill Library Manager

Complete lifecycle management for Claude skills in the **Skills_librairie** repository.

**Repository-Specific Configuration:**
- **Repository Path**: `/Users/guillaumebld/Documents/Skills/Skills_librairie`
- **GitHub Repository**: `https://github.com/GuillaumeBld/Skills_librairie.git`
- **Skills Location**: `Skills/` directory (capital S) organized by category
- **Categories**: Meta-skill, Automation, Infrastructure-DevOps, Development, Design-Creative, Communication, Document-Generation, AI-Agents
- **Catalog**: Auto-generated `catalog.json` at repository root

This skill is specifically designed to manage skills within this repository structure. All paths and commands assume you are working within `/Users/guillaumebld/Documents/Skills/Skills_librairie`.

## Prerequisites

- GitHub CLI (`gh`) installed and authenticated
- Git installed
- Python 3.8+ (for catalog operations)
- Access to https://github.com/GuillaumeBld/Skills_librairie.git

### First-Time Setup

```bash
# Repository location: /Users/guillaumebld/Documents/Skills/Skills_librairie

# 1. Install GitHub CLI (if not already installed)
# macOS: brew install gh
# Linux: See https://github.com/cli/cli/blob/trunk/docs/install_linux.md
# Windows: winget install --id GitHub.cli

# 2. Authenticate
gh auth login

# 3. Navigate to repository
cd /Users/guillaumebld/Documents/Skills/Skills_librairie

# 4. Verify structure
ls Skills/
# Expected categories: Meta-skill/, Automation/, Infrastructure-DevOps/, Development/, Design-Creative/, Communication/, Document-Generation/, AI-Agents/

# 5. Test GitHub access
gh repo view GuillaumeBld/Skills_librairie
```

## Quick Start: Complete Workflow

### 1. Initialize Library (First Use)

```bash
# Repository is located at: /Users/guillaumebld/Documents/Skills/Skills_librairie
cd /Users/guillaumebld/Documents/Skills/Skills_librairie

# Verify structure
ls Skills/
# Expected categories: Meta-skill/, Automation/, Infrastructure-DevOps/, Development/, Design-Creative/, Communication/, Document-Generation/, AI-Agents/

# Each category contains skill directories, e.g.:
# Skills/Meta-skill/skill-library-manager/
# Skills/Automation/n8n-workflow-patterns/
# Skills/Infrastructure-DevOps/vps-deployment-stack/
```

If catalog.json doesn't exist at the repository root, create it:
```bash
cd /Users/guillaumebld/Documents/Skills/Skills_librairie
cat > catalog.json << 'EOF'
{
  "version": "1.0.0",
  "updated": "2026-01-10",
  "repository": "https://github.com/GuillaumeBld/Skills_librairie",
  "skills": []
}
EOF
```

### 2. Create New Skill

Use `scripts/create-skill.sh` to automate the full workflow.

**Example: Create a PostgreSQL backup skill in Infrastructure-DevOps category**

```bash
# Run creation script from skill-library-manager
cd /Users/guillaumebld/Documents/Skills/Skills_librairie
bash Skills/skill-library-manager/scripts/create-skill.sh

# Interactive prompts:
# Skill name: postgres-backup
# Category: Infrastructure-DevOps
# Description: Automate PostgreSQL backups with pg_dump and S3 upload
# Author: Guillaume
# Tags: database, backup, postgresql, s3
# Version: 1.0.0

# Script will:
# 1. Create skill structure in Skills/Infrastructure-DevOps/postgres-backup/
# 2. Open editor for SKILL.md
# 3. Validate skill structure
# 4. Update catalog.json at repository root
# 5. Git commit + push
# 6. Create Git tag (postgres-backup-v1.0.0)
```

**Manual workflow:**
```bash
cd /Users/guillaumebld/Documents/Skills/Skills_librairie

# 1. Choose category (e.g., Infrastructure-DevOps, Meta-skill, Automation, etc.)
CATEGORY="Infrastructure-DevOps"
SKILL_NAME="postgres-backup"

# 2. Create skill directory structure
mkdir -p Skills/${CATEGORY}/${SKILL_NAME}/{scripts,references,assets}

# 3. Create SKILL.md with frontmatter
cat > Skills/${CATEGORY}/${SKILL_NAME}/SKILL.md << 'EOF'
---
name: postgres-backup
description: Automate PostgreSQL backups with pg_dump and S3 upload
---
# Postgres Backup

[Your skill instructions here]
EOF

# 4. Update catalog using the skill-library-manager script
python3 Skills/skill-library-manager/scripts/catalog-builder.py

# 5. Commit and push
git add Skills/${CATEGORY}/${SKILL_NAME}
git add catalog.json
git commit -m "Add ${SKILL_NAME} skill v1.0.0 to ${CATEGORY} category"
git tag ${SKILL_NAME}-v1.0.0
git push origin main --tags
```

### 3. Search Skills

```bash
cd /Users/guillaumebld/Documents/Skills/Skills_librairie

# Search by keyword
python3 Skills/skill-library-manager/scripts/search-skills.py database

# Search by tag
python3 Skills/skill-library-manager/scripts/search-skills.py --tag backup

# Search by category
python3 Skills/skill-library-manager/scripts/search-skills.py --category Infrastructure-DevOps

# List all skills
python3 Skills/skill-library-manager/scripts/search-skills.py --all

# Output example:
# Found 3 skills matching "database":
# 
# 1. postgres-backup (v1.0.0)
#    Category: Infrastructure-DevOps
#    Description: Automate PostgreSQL backups with pg_dump and S3 upload
#    Tags: database, backup, postgresql, s3
#    Location: Skills/Infrastructure-DevOps/postgres-backup/
#
# 2. mysql-monitoring (v2.1.0)
#    Category: Infrastructure-DevOps
#    Description: Monitor MySQL performance metrics and slow queries
#    Tags: database, monitoring, mysql
#    Location: Skills/Infrastructure-DevOps/mysql-monitoring/
#    ...
```

### 4. Install Skill

**Option A: Install to Claude.ai (Manual)**
```bash
cd /Users/guillaumebld/Documents/Skills/Skills_librairie

# Skills in this repository are organized as directories, not .skill packages
# Navigate to the skill directory
cd Skills/Infrastructure-DevOps/postgres-backup

# If you need to package it first, use the skill-creator tools:
# (Note: Check if package_skill.py is available in Meta-skill/skill-creator/scripts/)

# Upload in Claude.ai:
#    - Profile → Skills → Upload Skill
#    - Select the skill directory (Skills/Infrastructure-DevOps/postgres-backup/)
#    - Or zip it first: zip -r postgres-backup.zip Skills/Infrastructure-DevOps/postgres-backup/
#    - Confirm installation
```

**Option B: Install to Local Directory (Codex Skills)**
```bash
# For Codex/Claude Code, skills should be in ~/.codex/skills/
# Create category directory if needed
mkdir -p ~/.codex/skills/Infrastructure-DevOps

# Copy skill folder from repository
cp -r /Users/guillaumebld/Documents/Skills/Skills_librairie/Skills/Infrastructure-DevOps/postgres-backup \
      ~/.codex/skills/Infrastructure-DevOps/

# Or create symlink for development
ln -s /Users/guillaumebld/Documents/Skills/Skills_librairie/Skills/Infrastructure-DevOps/postgres-backup \
      ~/.codex/skills/Infrastructure-DevOps/postgres-backup
```

### 5. Update Existing Skill

```bash
cd /Users/guillaumebld/Documents/Skills/Skills_librairie

# 1. Navigate to the skill (organized by category)
cd Skills/Infrastructure-DevOps/vps-deployment-stack
# Edit SKILL.md, add scripts, references, assets, etc.

# 2. Update version in SKILL.md frontmatter
# In the frontmatter, add or update version: 1.1.0

# 3. Create or update CHANGELOG.md (optional but recommended)
cat >> CHANGELOG.md << 'EOF'
## v1.1.0 - 2026-01-15
- Added backup automation scripts
- Improved troubleshooting guide
EOF

# 4. Update catalog to reflect new version
cd /Users/guillaumebld/Documents/Skills/Skills_librairie
python3 Skills/skill-library-manager/scripts/catalog-builder.py

# 5. Commit with version bump
git add Skills/Infrastructure-DevOps/vps-deployment-stack
git add catalog.json
git commit -m "Update vps-deployment-stack to v1.1.0"
git tag vps-deployment-stack-v1.1.0
git push origin main --tags
```

### 6. Sync Library

```bash
# Pull latest changes from GitHub
cd /Users/guillaumebld/Documents/Skills/Skills_librairie
git pull origin main --tags

# Push local changes
git push origin main --tags

# Or use the sync script
bash Skills/skill-library-manager/scripts/sync-library.sh
```

## Workflows

### Workflow 1: "I need a skill for X, let me check if I have one"

```bash
cd /Users/guillaumebld/Documents/Skills/Skills_librairie

# Search your library
python3 Skills/skill-library-manager/scripts/search-skills.py "kubernetes deployment"

# Or search by browsing categories
ls Skills/Infrastructure-DevOps/
ls Skills/Automation/
# etc.

# If found: Reference it from Skills/{category}/{skill-name}/
# If not found: Create it (see Workflow 2)
```

### Workflow 2: "Create a new skill and save it"

```bash
cd /Users/guillaumebld/Documents/Skills/Skills_librairie

# Option A: Automated (recommended)
bash Skills/skill-library-manager/scripts/create-skill.sh
# Follow prompts: name, category, description, tags, version

# Option B: Manual (more control)
# 1. Choose category (Meta-skill, Automation, Infrastructure-DevOps, Development, Design-Creative, Communication, Document-Generation, AI-Agents)
CATEGORY="Meta-skill"  # or appropriate category
SKILL_NAME="my-new-skill"

# 2. Create directory structure
mkdir -p Skills/${CATEGORY}/${SKILL_NAME}/{scripts,references,assets}

# 3. Create SKILL.md with frontmatter (use Skills/skill-library-manager/references/skill-template.md as reference)
# Edit content
code Skills/${CATEGORY}/${SKILL_NAME}/SKILL.md

# 4. Update catalog
python3 Skills/skill-library-manager/scripts/catalog-builder.py

# 5. Commit
git add Skills/${CATEGORY}/${SKILL_NAME}
git add catalog.json
git commit -m "Add ${SKILL_NAME} v1.0.0 to ${CATEGORY} category"
git tag ${SKILL_NAME}-v1.0.0
git push origin main --tags
```

### Workflow 3: "Share skill with team"

```bash
cd /Users/guillaumebld/Documents/Skills/Skills_librairie

# 1. Ensure skill is pushed to GitHub
git push origin main --tags

# 2. Share repository URL
# Team members clone: 
#   cd ~/Documents/Skills
#   gh repo clone GuillaumeBld/Skills_librairie

# 3. Or share the specific skill directory
# Team members can reference: Skills/{category}/{skill-name}/
# Or zip it: zip -r my-skill.zip Skills/Infrastructure-DevOps/my-skill/
```

### Workflow 4: "Update skill after improvements"

See section 5 above (Update Existing Skill).

### Workflow 5: "Browse all skills in library"

```bash
cd /Users/guillaumebld/Documents/Skills/Skills_librairie

# List all with metadata
python3 Skills/skill-library-manager/scripts/search-skills.py --all

# View catalog directly (if it exists)
cat catalog.json | jq '.skills' 2>/dev/null || echo "catalog.json not found, run catalog-builder.py"

# Browse by category
tree -L 2 Skills/  # Shows all categories and their skills
# Or manually:
ls -la Skills/*/

# Browse on GitHub
gh repo view GuillaumeBld/Skills_librairie --web

# Or open in file browser
open Skills/
```

## Repository Structure

This Skills_librairie repository follows this structure:

```
/Users/guillaumebld/Documents/Skills/Skills_librairie/
├── README.md                          # Library overview
├── catalog.json                       # Searchable skill index (auto-generated)
├── .gitignore                         # Git ignore rules
├── Skills/                            # All skills organized by category
│   ├── Meta-skill/                    # Skills for managing skills
│   │   ├── skill-library-manager/     # This skill
│   │   │   ├── SKILL.md
│   │   │   ├── scripts/
│   │   │   │   ├── create-skill.sh
│   │   │   │   ├── catalog-builder.py
│   │   │   │   ├── search-skills.py
│   │   │   │   └── sync-library.sh
│   │   │   ├── references/
│   │   │   └── assets/
│   │   ├── skill-creator/
│   │   ├── skill-quality-auditor/
│   │   └── ...
│   ├── Automation/                    # n8n and workflow automation skills
│   │   ├── n8n-workflow-patterns/
│   │   ├── n8n-expression-syntax/
│   │   └── ...
│   ├── Infrastructure-DevOps/         # VPS, Docker, deployment skills
│   │   ├── vps-deployment-stack/
│   │   ├── vps-daily-operations/
│   │   ├── docker-development-workflow/
│   │   └── ...
│   ├── Development/                   # Development tools and workflows
│   ├── Design-Creative/               # Design and creative skills
│   ├── Communication/                 # Communication and branding skills
│   ├── Document-Generation/           # Document creation skills (docx, pdf, pptx, xlsx)
│   └── AI-Agents/                     # AI agent and RAG skills
│       └── rag-pipeline-expert/
└── (scripts are within skill-library-manager)
```

**Key points:**
- All skills are in `Skills/` directory (capital S)
- Skills are organized by category subdirectories
- Each skill is a directory containing `SKILL.md`, optional `scripts/`, `references/`, `assets/`
- Management scripts are in `Skills/Meta-skill/skill-library-manager/scripts/`
- Catalog is auto-generated at repository root

## Catalog Schema

`catalog.json` structure (located at repository root):

```json
{
  "version": "1.0.0",
  "updated": "2026-01-15T10:30:00Z",
  "repository": "https://github.com/GuillaumeBld/Skills_librairie",
  "repository_path": "/Users/guillaumebld/Documents/Skills/Skills_librairie",
  "skills": [
    {
      "name": "vps-deployment-stack",
      "category": "Infrastructure-DevOps",
      "version": "1.1.0",
      "description": "Deploy Dokploy + Traefik + Docker + Kuma with automatic HTTPS",
      "author": "Guillaume",
      "created": "2026-01-10",
      "updated": "2026-01-15",
      "tags": ["devops", "docker", "vps", "deployment", "traefik"],
      "dependencies": [],
      "compatibility": ["claude.ai", "claude-code"],
      "license": "MIT",
      "location": "Skills/Infrastructure-DevOps/vps-deployment-stack/",
      "absolute_path": "/Users/guillaumebld/Documents/Skills/Skills_librairie/Skills/Infrastructure-DevOps/vps-deployment-stack"
    },
    {
      "name": "skill-library-manager",
      "category": "Meta-skill",
      "version": "1.0.0",
      "description": "Manage Claude skills lifecycle in the Skills_librairie repository",
      "author": "Guillaume",
      "created": "2026-01-10",
      "updated": "2026-01-15",
      "tags": ["meta", "skill-management", "catalog", "github"],
      "dependencies": [],
      "compatibility": ["claude.ai", "claude-code"],
      "license": "MIT",
      "location": "Skills/Meta-skill/skill-library-manager/",
      "absolute_path": "/Users/guillaumebld/Documents/Skills/Skills_librairie/Skills/Meta-skill/skill-library-manager"
    }
  ],
  "categories": {
    "Meta-skill": ["skill-library-manager", "skill-creator", "skill-quality-auditor"],
    "Infrastructure-DevOps": ["vps-deployment-stack", "vps-daily-operations", "docker-development-workflow"],
    "Automation": ["n8n-workflow-patterns", "n8n-expression-syntax", "n8n-mcp-tools-expert"],
    "AI-Agents": ["rag-pipeline-expert"]
  }
}
```

**Catalog Generation:**
- Generated automatically by `Skills/skill-library-manager/scripts/catalog-builder.py`
- Scans `Skills/` directory for all `SKILL.md` files
- Extracts metadata from frontmatter
- Organizes by category structure

## Versioning Strategy

Follow **Semantic Versioning** (semver):

- **Major (x.0.0)**: Breaking changes, incompatible updates
- **Minor (1.x.0)**: New features, backward compatible
- **Patch (1.0.x)**: Bug fixes, minor improvements

**Examples:**
- `1.0.0` → `1.0.1`: Fixed typo in SKILL.md
- `1.0.1` → `1.1.0`: Added new reference file
- `1.1.0` → `2.0.0`: Restructured skill, changed interface

**Git Tags:**
- Format: `{skill-name}-v{version}`
- Example: `postgres-backup-v1.0.0`
- List tags: `git tag -l "postgres-backup-*"`

## GitHub Operations

### Common Commands

```bash
# Repository location: /Users/guillaumebld/Documents/Skills/Skills_librairie

# Clone library (if starting fresh)
cd /Users/guillaumebld/Documents/Skills
gh repo clone GuillaumeBld/Skills_librairie

# View repository
cd /Users/guillaumebld/Documents/Skills/Skills_librairie
gh repo view GuillaumeBld/Skills_librairie

# Create issue (for skill requests)
gh issue create --repo GuillaumeBld/Skills_librairie --title "Request: New skill for X" --body "Description of needed skill"

# List releases
gh release list --repo GuillaumeBld/Skills_librairie

# Create release (for major versions)
gh release create v1.0.0 --repo GuillaumeBld/Skills_librairie --title "Skills Library v1.0.0" --notes "Initial release"

# View repository in browser
gh repo view GuillaumeBld/Skills_librairie --web
```

### Backup Strategy

```bash
# Repository is at: /Users/guillaumebld/Documents/Skills/Skills_librairie

# Create timestamped backup
BACKUP_DIR=~/Backups/Skills_librairie-$(date +%Y%m%d)
mkdir -p ~/Backups
cp -r /Users/guillaumebld/Documents/Skills/Skills_librairie "$BACKUP_DIR"

# Or create compressed archive
cd /Users/guillaumebld/Documents/Skills
tar -czf ~/Backups/skills-library-$(date +%Y%m%d).tar.gz Skills_librairie/

# Or clone to backup location
gh repo clone GuillaumeBld/Skills_librairie ~/Backups/Skills_librairie-backup-$(date +%Y%m%d)
```

## Best Practices

### 1. Skill Naming
- Use kebab-case: `postgres-backup`, `vps-deployment`
- Be descriptive: `docker-dev-workflow` not `docker-skill`
- Avoid generic names: `database-utils` → `postgres-backup-automation`

### 2. Documentation
- Always include SKILL.md with clear description
- Add CHANGELOG.md for version history
- Include README.md in complex skills
- Document prerequisites clearly

### 3. Tagging
- Use 3-5 relevant tags per skill
- Common tags: devops, database, monitoring, backup, security, docker, kubernetes
- Consistent naming: `postgresql` not `postgres`, `backup` not `backups`

### 4. Versioning
- Start at v1.0.0 for production-ready skills
- Use v0.x.x for experimental/beta skills
- Always update CHANGELOG.md with version bumps
- Tag releases in Git

### 5. Organization
- Group related skills in catalog categories
- Keep skills focused (single responsibility)
- Extract common patterns into separate skills
- Document skill dependencies

## Troubleshooting

### Library Not Found
```bash
# Repository should be at: /Users/guillaumebld/Documents/Skills/Skills_librairie

# Check if exists
ls -la /Users/guillaumebld/Documents/Skills/Skills_librairie

# If not, clone
cd /Users/guillaumebld/Documents/Skills
gh repo clone GuillaumeBld/Skills_librairie
```

### GitHub Authentication Failed
```bash
# Re-authenticate
gh auth login

# Check status
gh auth status

# Test access
gh repo view GuillaumeBld/Skills_librairie
```

### Catalog Out of Sync
```bash
# Rebuild catalog from Skills/ directory
cd /Users/guillaumebld/Documents/Skills/Skills_librairie
python3 Skills/skill-library-manager/scripts/catalog-builder.py

# Commit updated catalog
git add catalog.json
git commit -m "Rebuild catalog from Skills/ directory structure"
git push
```

### Merge Conflicts
```bash
# Pull latest changes first
git pull origin main

# If conflicts, resolve manually
git status
# Edit conflicting files
git add .
git commit -m "Resolve merge conflicts"
git push
```

### Skill Validation Fails
```bash
cd /Users/guillaumebld/Documents/Skills/Skills_librairie

# Check skill structure manually
CATEGORY="Meta-skill"  # or appropriate category
SKILL_NAME="my-skill"
ls -la Skills/${CATEGORY}/${SKILL_NAME}/

# Verify SKILL.md exists and has valid frontmatter
head -10 Skills/${CATEGORY}/${SKILL_NAME}/SKILL.md

# Common issues:
# - Missing SKILL.md in skill directory
# - Invalid YAML frontmatter (missing --- markers, syntax errors)
# - Missing name or description in frontmatter
# - Skill directory not in correct category location
# - Files outside expected structure (scripts/, references/, assets/ are optional)
```

## Reference Files

All reference files are located in `Skills/skill-library-manager/`:

- **scripts/create-skill.sh** - Automated skill creation workflow
  - Location: `/Users/guillaumebld/Documents/Skills/Skills_librairie/Skills/skill-library-manager/scripts/create-skill.sh`
- **scripts/catalog-builder.py** - Generate/update catalog.json from Skills/ directory
  - Location: `/Users/guillaumebld/Documents/Skills/Skills_librairie/Skills/skill-library-manager/scripts/catalog-builder.py`
- **scripts/search-skills.py** - Search catalog by keywords/tags/category
  - Location: `/Users/guillaumebld/Documents/Skills/Skills_librairie/Skills/skill-library-manager/scripts/search-skills.py`
- **scripts/sync-library.sh** - Git pull + push wrapper
  - Location: `/Users/guillaumebld/Documents/Skills/Skills_librairie/Skills/skill-library-manager/scripts/sync-library.sh`
- **references/skill-template.md** - Template for new skills
  - Location: `/Users/guillaumebld/Documents/Skills/Skills_librairie/Skills/skill-library-manager/references/skill-template.md`
- **references/github-workflow.md** - Detailed GitHub operations
  - Location: `/Users/guillaumebld/Documents/Skills/Skills_librairie/Skills/skill-library-manager/references/github-workflow.md`
- **references/versioning-guide.md** - Semantic versioning examples
  - Location: `/Users/guillaumebld/Documents/Skills/Skills_librairie/Skills/skill-library-manager/references/versioning-guide.md`
- **assets/catalog-schema.json** - JSON schema for catalog validation
  - Location: `/Users/guillaumebld/Documents/Skills/Skills_librairie/Skills/skill-library-manager/assets/catalog-schema.json`

## Related Skills in This Repository

- **Meta-skill/skill-creator** - Foundation for creating skills (based on Anthropic's skill-creator)
- **Infrastructure-DevOps/vps-deployment-stack** - Example of well-structured skill with references
- **Infrastructure-DevOps/docker-development-workflow** - Example with multiple reference files and assets
- **Automation/n8n-workflow-patterns** - Example of comprehensive skill documentation
- **Meta-skill/skill-quality-auditor** - Quality assurance for skills

## Repository-Specific Notes

- **Repository Path**: `/Users/guillaumebld/Documents/Skills/Skills_librairie`
- **GitHub Remote**: `https://github.com/GuillaumeBld/Skills_librairie.git`
- **Skill Organization**: Skills are organized by category in `Skills/` directory
- **Categories**: Meta-skill, Automation, Infrastructure-DevOps, Development, Design-Creative, Communication, Document-Generation, AI-Agents
- **Catalog Location**: `catalog.json` at repository root (auto-generated)
- **Management Scripts**: Located in `Skills/skill-library-manager/scripts/`
