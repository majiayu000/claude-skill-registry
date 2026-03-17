---
description: "Generate Claude AI skills from documentation, GitHub repos, or PDFs using Skill Seekers"
allowed-tools: ["Bash(pip)", "Bash(skill-seekers)", "Bash(python3)", "Bash(which)", "Bash(ls)", "Bash(mkdir)", "Read"]
author: "Claude Command and Control"
version: "1.0"
---

# Create Skill

## Purpose
Generate production-ready Claude AI skills from documentation websites, GitHub repositories, or PDF files using [Skill Seekers](https://github.com/yusufkaraaslan/Skill_Seekers). Automatically outputs to `/INTEGRATION/incoming` for seamless integration with the existing workflow.

## Features
- 🌐 **Documentation Scraping** - Convert doc sites to skills (React, FastAPI, etc.)
- 🐙 **GitHub Integration** - Extract skills from repositories with AST parsing
- 📄 **PDF Processing** - Transform technical PDFs into structured skills
- ✨ **AI Enhancement** - Optional AI-powered skill refinement (`--enhance`)
- 🔄 **Auto-Integration** - Automatically runs `/integration-scan` after creation
- 📦 **Auto-Install** - Checks for and installs `skill-seekers` if missing

## Usage

### Documentation Website
```bash
/create-skill --url https://fastapi.tiangolo.com --name fastapi
/create-skill --url https://react.dev --name react --enhance
```

### GitHub Repository
```bash
/create-skill --github facebook/react
/create-skill --github anthropics/anthropic-sdk-python --enhance
```

### PDF Document
```bash
/create-skill --pdf /path/to/manual.pdf --name api-manual
/create-skill --pdf ~/Downloads/guide.pdf --name user-guide --enhance
```

### Using Config File (Advanced)
```bash
/create-skill --config configs/react.json
/create-skill --config https://raw.githubusercontent.com/.../config.json
```

## Parameters

| Parameter | Description | Required | Example |
|-----------|-------------|----------|---------|
| `--url` | Documentation website URL | Yes* | `https://fastapi.tiangolo.com` |
| `--name` | Skill name (used with --url or --pdf) | Yes* | `fastapi` |
| `--github` | GitHub repository (owner/repo) | Yes* | `facebook/react` |
| `--pdf` | Path to PDF file | Yes* | `/path/to/doc.pdf` |
| `--config` | Config file path or URL | Yes* | `configs/react.json` |
| `--enhance` | Run AI enhancement (improves quality) | No | (flag) |

*One of: `--url + --name`, `--github`, `--pdf + --name`, or `--config` is required.

## Workflow

### 1. Dependency Check
```bash
# Check if skill-seekers is installed
!which skill-seekers || python3 -m pip show skill-seekers
```

**If not installed:**
```bash
# Auto-install skill-seekers
!pip install skill-seekers

# Verify installation
!skill-seekers --version
```

Display:
```
🔧 Installing Skill Seekers...
✅ Skill Seekers v2.2.0 installed successfully
```

### 2. Determine Source Type

Based on parameters provided:
- `--url` → Documentation scraping
- `--github` → GitHub repository
- `--pdf` → PDF extraction
- `--config` → Custom configuration

### 3. Generate Skill

**For Documentation (`--url`):**
```bash
# Generate skill to default output/ directory
!skill-seekers scrape --url [URL] --name [NAME]

# Move to integration directory
!mv output/[NAME] INTEGRATION/incoming/[NAME]
```

**For GitHub (`--github`):**
```bash
# Extract repo name from owner/repo
REPO_NAME=$(echo [OWNER/REPO] | cut -d'/' -f2)

# Generate skill
!skill-seekers github --repo [OWNER/REPO]

# Move to integration directory
!mv output/$REPO_NAME INTEGRATION/incoming/$REPO_NAME
```

**For PDF (`--pdf`):**
```bash
# Generate skill from PDF
!skill-seekers pdf --file [PDF_PATH] --name [NAME]

# Move to integration directory
!mv output/[NAME] INTEGRATION/incoming/[NAME]
```

**For Config (`--config`):** *(Recommended for best results)*
```bash
# Generate from config file (local path or URL)
!skill-seekers scrape --config [CONFIG_PATH]

# Extract skill name from config JSON
SKILL_NAME=$(python3 -c "import json; print(json.load(open('[CONFIG_PATH]'))['name'])")

# Move to integration directory
!mv output/$SKILL_NAME INTEGRATION/incoming/$SKILL_NAME
```

**Why Config Files?**
- ✅ Better content extraction (100+ pages vs 1-10 pages with basic scraping)
- ✅ Automatic categorization (getting_started, path_operations, etc.)
- ✅ Custom URL patterns (include/exclude specific paths)
- ✅ Rate limiting control
- ✅ Selector customization for specific doc sites

**Example config locations:**
- User configs: `~/.skill-seekers/configs/[framework].json`
- Project configs: `configs/[framework].json`
- Remote configs: `https://raw.githubusercontent.com/.../config.json`

Display progress:
```
🚀 Generating skill: [NAME]
📥 Source: [URL/GitHub/PDF]
📂 Default output: output/[NAME]
📂 Moving to: INTEGRATION/incoming/[NAME]

⏳ This may take 5-15 minutes depending on source size...
```

### 4. Optional Enhancement

If `--enhance` flag provided:
```bash
# Enhance in default location before moving
!skill-seekers enhance output/[NAME]
```

Display:
```
✨ Enhancing skill with AI refinement...
⏳ This may take 2-3 additional minutes...
```

### 5. Move to Integration Directory

```bash
# Move completed skill to integration directory
!mv output/[NAME] INTEGRATION/incoming/[NAME]
```

Display:
```
📦 Moving skill to integration directory...
✅ Skill moved to: INTEGRATION/incoming/[NAME]
```

### 6. Verify Output

```bash
# Check skill structure
!ls -la INTEGRATION/incoming/[NAME]/

# Verify SKILL.md exists
!test -f INTEGRATION/incoming/[NAME]/SKILL.md && echo "✅ SKILL.md found"
```

Expected structure:
```
INTEGRATION/incoming/[NAME]/
├── SKILL.md               # Main skill file (required)
├── knowledge/             # Extracted documentation
│   ├── section1.md
│   └── section2.md
├── examples/              # Code samples
│   └── usage.py
└── references/            # Source materials
    └── sources.txt
```

### 7. Auto-Scan Integration

Automatically run `/integration-scan` to categorize the new skill:

```bash
# Invoke integration-scan command
@.claude/commands/integration-scan.md
```

Display:
```
🔍 Auto-scanning new skill for integration...
```

### 8. Final Summary

Display completion status:

```
╔═══════════════════════════════════════════════════╗
║          SKILL CREATION COMPLETED                  ║
╚═══════════════════════════════════════════════════╝

SKILL: [NAME]
SOURCE: [URL/GitHub/PDF]
OUTPUT: INTEGRATION/incoming/[NAME]
ENHANCED: [Yes/No]

FILES CREATED:
  • SKILL.md ✓
  • knowledge/ ([X] files) ✓
  • examples/ ([X] files) ✓
  • references/ ([X] files) ✓

INTEGRATION STATUS:
  ✅ Scanned and categorized by /integration-scan
  📋 Report: /INTEGRATION/logs/scan-report-[timestamp].md

NEXT STEPS:
  1. Review skill: INTEGRATION/incoming/[NAME]/SKILL.md
  2. Run '/integration-process' to finalize integration
  3. Test skill: "Use [NAME] skill to..."

Time: [X] minutes | Size: [X] MB | Quality: ✅ Ready
```

## Error Handling

### Installation Failures
```
❌ Failed to install skill-seekers
Reason: [error message]

Please install manually:
  pip install skill-seekers

Then retry: /create-skill [your-parameters]
```

### Generation Failures
```
❌ Skill generation failed
Source: [URL/GitHub/PDF]
Error: [detailed error message]

Common fixes:
  • Check URL is accessible
  • Verify GitHub repo exists (public access)
  • Ensure PDF file path is correct
  • Try without --enhance flag first

Retry with debug: skill-seekers [command] --verbose
```

### Missing Output
```
⚠️ Skill generated but SKILL.md not found
Location: INTEGRATION/incoming/[NAME]

This may indicate:
  • Incomplete generation
  • Unexpected directory structure

Suggested actions:
  1. Check manually: ls -la INTEGRATION/incoming/[NAME]
  2. Review logs: skill-seekers --help
  3. Re-run with fresh output directory
```

### Integration Scan Failures
```
⚠️ Skill created but auto-scan failed
Skill location: INTEGRATION/incoming/[NAME]

You can manually run integration scan:
  /integration-scan
```

## Quality Checks

During generation, Skill Seekers performs:
- ✅ URL accessibility validation
- ✅ Content extraction and parsing
- ✅ Code language detection (Python, JS, TS, C++, etc.)
- ✅ Automatic categorization by topic
- ✅ SKILL.md format compliance
- ✅ Link validation
- ✅ Metadata extraction

If `--enhance` used:
- ✅ AI-powered content refinement
- ✅ Example code optimization
- ✅ Documentation clarity improvement
- ✅ Trigger condition enhancement

## Security Considerations

- **Safe Installation**: Auto-install uses `pip install` (standard package manager)
- **Read-Only Source Access**: Only reads from URLs/GitHub/PDFs, never modifies source
- **Sandboxed Output**: All generated files go to `/INTEGRATION/incoming` (quarantine area)
- **Validation Pipeline**: Skills must pass `/integration-scan` before final integration
- **Audit Trail**: All operations logged in scan reports

## Performance

| Source Type | Typical Time | Enhancement Time | Output Size |
|-------------|--------------|------------------|-------------|
| Small docs (10-20 pages) | 5-8 min | +2 min | 1-5 MB |
| Medium docs (50-100 pages) | 10-15 min | +3 min | 5-15 MB |
| GitHub repo (small) | 8-12 min | +2 min | 2-8 MB |
| GitHub repo (large) | 15-25 min | +4 min | 10-30 MB |
| PDF (technical manual) | 5-10 min | +2 min | 1-10 MB |

## Integration with Workflow

**Complete Pipeline**:
```
/create-skill → INTEGRATION/incoming/ → /integration-scan (auto)
    ↓
Review scan report
    ↓
/integration-process → Move to skills-templates/
    ↓
/integration-validate → Quality checks
    ↓
/integration-update-docs → Update README
    ↓
Production-ready skill ✅
```

## Examples

### Example 1: FastAPI Documentation (Config Approach - Recommended)
```bash
# Best approach: Use pre-configured config file
/create-skill --config ~/.skill-seekers/configs/fastapi.json
```

**Result**: Comprehensive FastAPI skill with:
- 102 pages of documentation extracted
- 7 categories (getting_started, path_operations, request_data, dependencies, security, database, other)
- 456 KB SKILL.md with 10+ examples
- 720 KB total reference documentation

**Time**: ~12 minutes

**Compare to basic URL approach**:
```bash
# Basic approach: Only captures 1 page (12 KB)
/create-skill --url https://fastapi.tiangolo.com --name fastapi
```
Config files provide 100x better content extraction!

### Example 2: React from GitHub
```bash
/create-skill --github facebook/react
```

**Result**: React skill with component patterns, hooks, lifecycle methods, AST-parsed API surface, and GitHub issues/PRs context.

**Time**: ~12 minutes

### Example 3: Custom API Manual
```bash
/create-skill --pdf ~/Documents/api-reference-v3.pdf --name company-api --enhance
```

**Result**: Structured skill from PDF with endpoints, authentication, examples, and enhanced clarity.

**Time**: ~14 minutes (10 min extraction + 4 min enhancement)

## Tips & Best Practices

### Choosing --enhance
- ✅ **Use --enhance** for:
  - Public skills you'll share
  - Complex technical documentation
  - First-time generation of critical skills

- ⚠️ **Skip --enhance** for:
  - Quick prototyping
  - Well-structured sources (already high quality)
  - Time-sensitive needs

### Naming Conventions
- Use lowercase kebab-case: `fastapi`, `react-hooks`, `company-api`
- Be descriptive but concise: `aws-lambda` not `amazon-web-services-lambda-functions`
- Match official project names when possible

### Source Selection
- **Config files** (RECOMMENDED): Best for comprehensive extraction with 100x better results
  - Check `~/.skill-seekers/configs/` for pre-configured popular frameworks
  - Create custom configs for complex documentation sites
  - Provides categorization, URL filtering, and rate limiting
- **Documentation sites**: Use basic --url for simple sites or when no config exists
  - Works best for sites with llms.txt or simple HTML structure
  - May only capture 1-10 pages without proper configuration
- **GitHub repos**: Best for understanding implementation patterns and API structure
  - Requires GitHub token to avoid rate limits (60/hour without)
  - Large repos may take 15-25 minutes
- **PDFs**: Best for proprietary tools, legacy systems, internal documentation

### Using Config Files
**When to create a custom config:**
1. Documentation site has >50 pages
2. Site uses JavaScript navigation (SPA)
3. Need specific categorization (tutorials, API reference, guides)
4. Want to exclude certain sections (external links, deployment docs)

**Sample config structure:**
```json
{
  "name": "framework-name",
  "description": "Short description",
  "base_url": "https://docs.example.com/",
  "start_urls": ["https://docs.example.com/tutorial/"],
  "url_patterns": {
    "include": ["/tutorial/", "/api/"],
    "exclude": ["/blog/", "/external/"]
  },
  "categories": {
    "getting_started": ["intro", "tutorial"],
    "api": ["api", "reference"]
  },
  "rate_limit": 0.5,
  "max_pages": 250
}
```

### Pre-Generation Checklist
- [ ] Verify source is accessible (URL loads, GitHub repo is public, PDF exists)
- [ ] Check `/INTEGRATION/incoming` has space (~50-100 MB free recommended)
- [ ] Ensure `pip` has internet access for auto-install
- [ ] Clear previous failed attempts: `rm -rf INTEGRATION/incoming/[NAME]`

## Dependencies

- **Required**: Python 3.8+, pip
- **Auto-installed**: skill-seekers package
- **Optional**: OpenAI API key (for --enhance, can use local models)

## Troubleshooting

### "skill-seekers: command not found"
```bash
# Verify Python environment
python3 --version

# Install manually
pip install skill-seekers

# Verify
skill-seekers --version
```

### "No module named 'skill_seekers'"
```bash
# Wrong Python environment - check pip location
which pip
which python3

# Reinstall with correct pip
python3 -m pip install skill-seekers
```

### Large PDFs timing out
```bash
# Use Skill Seekers directly with custom timeout
skill-seekers pdf --file huge.pdf --name huge-manual --timeout 3600
```

### Enhancement requires API key
```bash
# Set OpenAI API key (if not already set)
export OPENAI_API_KEY="sk-..."

# Or skip enhancement for now
/create-skill --url https://example.com --name example
```

## Related Commands

- **`/integration-scan`** - Categorize incoming files (auto-run by this command)
- **`/integration-process`** - Move validated skills to final location
- **`/integration-validate`** - Run comprehensive quality checks
- **`/integration-update-docs`** - Update README with new skills

## Version History

- **1.0** (2025-12-26): Initial release
  - Documentation, GitHub, and PDF support
  - Auto-install capability
  - AI enhancement option
  - Auto-scan integration
  - Comprehensive error handling

---

**Last Updated**: December 26, 2025
**Dependencies**: skill-seekers package, /INTEGRATION directory structure
**Integration**: Works seamlessly with integration pipeline commands
