---
description: "Generate production-ready Claude AI skills from documentation, GitHub repos, or PDFs using Skill Seekers with automated quality validation"
allowed-tools: ["Bash(pip:install,show)", "Bash(skill-seekers:*)", "Bash(python3:-c,-m)", "Bash(which:*)", "Bash(ls:-la)", "Bash(mkdir:-p)", "Bash(mv:*)", "Bash(test:-f)", "Read", "Write"]
output-format: "json"
author: "Claude Command and Control"
version: "2.0.0"
category: "Skills Development"
complexity: "moderate"
execution-time: "5-25 minutes"
---

# Create Skill

## Purpose
Generate production-ready Claude AI skills from documentation websites, GitHub repositories, or PDF files using [Skill Seekers](https://github.com/yusufkaraaslan/Skill_Seekers). Automatically outputs to `/INTEGRATION/incoming` for seamless integration with the existing workflow.

## Production-Grade Enhancements (v2.0)

This command now implements production-grade patterns from [Document 02: Command Creation](../../docs/best-practices/02-Individual-Command-Creation.md) and [Document 09: Skill Development](../../docs/best-practices/09-Developing-High-Impact-Claude-Skills.md):

- ✅ **Pre-execution validation**: Source accessibility and prerequisite checks
- ✅ **Quality gates**: Automated SKILL.md validation and structure verification
- ✅ **Structured output**: JSON format for CI/CD integration
- ✅ **Success metrics**: Quality scoring with pass/fail thresholds
- ✅ **Evaluation framework**: LLM-as-judge quality assessment
- ✅ **Hooks integration**: Recommended PostToolUse validation hooks
- ✅ **Progressive disclosure**: External references for detailed workflows

## Features
- 🌐 **Documentation Scraping** - Convert doc sites to skills (React, FastAPI, Just, etc.)
- 🐙 **GitHub Integration** - Extract skills from repositories with AST parsing
- 📄 **PDF Processing** - Transform technical PDFs into structured skills
- ⚙️ **Config-Driven** - 25+ pre-configured frameworks in `configs/` directory
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

### Using Config File (Recommended for Best Results)
```bash
# Use pre-configured framework from repository
/create-skill --config configs/fastapi.json
/create-skill --config configs/react.json
/create-skill --config configs/just.json

# Or use remote config URL
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

## Pre-Execution Validation

Before beginning skill generation, validate prerequisites and inputs:

### Input Validation
```bash
# Validate required parameters
if [ -z "$URL" ] && [ -z "$GITHUB" ] && [ -z "$PDF" ] && [ -z "$CONFIG" ]; then
  echo "❌ Error: One of --url, --github, --pdf, or --config is required"
  exit 1
fi

# Validate source accessibility
if [ -n "$URL" ]; then
  curl -sI "$URL" | head -1 | grep -q "200" || {
    echo "❌ Error: URL not accessible: $URL"
    exit 1
  }
fi

# Validate PDF exists
if [ -n "$PDF" ]; then
  test -f "$PDF" || {
    echo "❌ Error: PDF file not found: $PDF"
    exit 1
  }
fi

# Validate config exists
if [ -n "$CONFIG" ]; then
  test -f "$CONFIG" || {
    echo "❌ Error: Config file not found: $CONFIG"
    echo "💡 Available configs: ls configs/"
    exit 1
  }
fi
```

### Disk Space Check
```bash
# Ensure adequate space in INTEGRATION/incoming
AVAILABLE=$(df -h INTEGRATION/incoming | awk 'NR==2 {print $4}' | sed 's/G//')
if [ "$AVAILABLE" -lt 1 ]; then
  echo "⚠️  Warning: Low disk space (${AVAILABLE}GB available)"
  echo "Recommended: >1GB free in INTEGRATION/incoming"
fi
```

### Prerequisite Verification
```bash
# Verify Python environment
python3 --version >/dev/null 2>&1 || {
  echo "❌ Error: Python 3.8+ required"
  exit 1
}

# Verify pip is available
pip --version >/dev/null 2>&1 || {
  echo "❌ Error: pip not found"
  exit 1
}
```

Display validation status:
```
✅ Pre-execution validation passed
  • Input parameters: Valid
  • Source accessibility: Confirmed
  • Disk space: Adequate (XGB available)
  • Prerequisites: Python 3.x, pip installed
```

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

**Config locations:**
- **Local configs** (PRIMARY): `configs/[framework].json`
- Remote configs: `https://raw.githubusercontent.com/.../config.json`

**Available configs in repository:**
- `configs/fastapi.json` - FastAPI Python web framework
- `configs/react.json` - React JavaScript library
- `configs/django.json` - Django Python web framework
- `configs/braiins-pool.json` - Braiins mining pool
- `configs/braiins-os.json` - Braiins OS firmware
- `configs/farm-monitor.json` - Farm monitoring
- `configs/just.json` - Just command runner (task automation)
- `configs/kubernetes.json` - Kubernetes orchestration
- `configs/tailwind.json` - Tailwind CSS
- And 20+ more frameworks...

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

### 7. Quality Gates & Validation

Run automated quality checks on generated skill:

#### Structure Validation
```bash
# Verify required components
SKILL_DIR="INTEGRATION/incoming/[NAME]"

# Check SKILL.md exists and has minimum content
if [ -f "$SKILL_DIR/SKILL.md" ]; then
  LINES=$(wc -l < "$SKILL_DIR/SKILL.md")
  if [ "$LINES" -lt 50 ]; then
    echo "⚠️  Quality Warning: SKILL.md only $LINES lines (expected >50)"
  else
    echo "✅ SKILL.md: $LINES lines"
  fi
else
  echo "❌ CRITICAL: SKILL.md not found"
  exit 1
fi

# Check for required sections
grep -q "## Description" "$SKILL_DIR/SKILL.md" || echo "⚠️  Missing: Description section"
grep -q "## When to Use" "$SKILL_DIR/SKILL.md" || echo "⚠️  Missing: Activation triggers"
grep -q "## Example" "$SKILL_DIR/SKILL.md" || echo "⚠️  Missing: Examples"
```

#### Content Quality Assessment
```bash
# Count examples (should have 2-5)
EXAMPLES=$(grep -c "^### Example" "$SKILL_DIR/SKILL.md")
if [ "$EXAMPLES" -lt 2 ]; then
  echo "⚠️  Quality Warning: Only $EXAMPLES example(s), recommend 2-5"
elif [ "$EXAMPLES" -ge 2 ]; then
  echo "✅ Examples: $EXAMPLES provided"
fi

# Check knowledge directory size
if [ -d "$SKILL_DIR/knowledge" ]; then
  KNOWLEDGE_COUNT=$(find "$SKILL_DIR/knowledge" -type f | wc -l)
  echo "✅ Knowledge files: $KNOWLEDGE_COUNT extracted"
else
  echo "⚠️  Warning: No knowledge directory created"
fi
```

#### Activation Trigger Validation
```python
# Validate trigger clarity (Python snippet)
import re

with open(f'{SKILL_DIR}/SKILL.md', 'r') as f:
    content = f.read()

# Check for action-oriented triggers
triggers = re.findall(r'- When.*?(create|generate|analyze|review|build)', content, re.IGNORECASE)
if len(triggers) >= 3:
    print("✅ Activation triggers: Clear and action-oriented")
else:
    print("⚠️  Weak triggers: Add explicit action verbs (create, generate, analyze)")
```

#### Quality Scoring Rubric

Based on [Document 09: Quality Assessment](../../docs/best-practices/09-Developing-High-Impact-Claude-Skills.md#skill-quality-assessment):

| Criterion | Weight | Score | Status |
|-----------|--------|-------|--------|
| **Structure** (SKILL.md exists, sections present) | 25% | X/5 | ✅/⚠️/❌ |
| **Examples** (2-5 examples with input/output) | 25% | X/5 | ✅/⚠️/❌ |
| **Triggers** (3+ clear activation conditions) | 20% | X/5 | ✅/⚠️/❌ |
| **Knowledge** (extracted content >10 files) | 15% | X/5 | ✅/⚠️/❌ |
| **Documentation** (prerequisites, workflow steps) | 15% | X/5 | ✅/⚠️/❌ |

**Target Score**: ≥20/25 (80%) for production deployment

Display quality results:
```
╔═══════════════════════════════════════════════════╗
║          QUALITY ASSESSMENT RESULTS               ║
╚═══════════════════════════════════════════════════╝

STRUCTURE:     ✅ 5/5 (All sections present)
EXAMPLES:      ✅ 4/5 (3 examples provided)
TRIGGERS:      ⚠️  3/5 (Triggers need action verbs)
KNOWLEDGE:     ✅ 5/5 (42 files extracted)
DOCUMENTATION: ✅ 5/5 (Complete workflow)

TOTAL SCORE:   22/25 (88%) ✅ PASSED

RECOMMENDATIONS:
  • Strengthen activation triggers with explicit verbs
  • Consider adding 1-2 edge case examples

DEPLOYMENT STATUS: Ready for production ✅
```

### 8. Auto-Scan Integration

Automatically run `/integration-scan` to categorize the new skill:

```bash
# Invoke integration-scan command
@.claude/commands/integration-scan.md
```

Display:
```
🔍 Auto-scanning new skill for integration...
```

### 9. Structured Output (JSON)

For CI/CD integration and programmatic consumption:

```json
{
  "status": "success",
  "skill": {
    "name": "[NAME]",
    "source": {
      "type": "documentation|github|pdf|config",
      "url": "[SOURCE_URL]",
      "config": "[CONFIG_PATH]"
    },
    "output": {
      "directory": "INTEGRATION/incoming/[NAME]",
      "size_mb": 5.2,
      "files": {
        "skill_md": true,
        "knowledge_count": 42,
        "examples_count": 3,
        "references_count": 1
      }
    },
    "quality": {
      "score": 22,
      "max_score": 25,
      "percentage": 88,
      "status": "passed",
      "breakdown": {
        "structure": {"score": 5, "weight": 0.25},
        "examples": {"score": 4, "weight": 0.25},
        "triggers": {"score": 3, "weight": 0.20},
        "knowledge": {"score": 5, "weight": 0.15},
        "documentation": {"score": 5, "weight": 0.15}
      },
      "recommendations": [
        "Strengthen activation triggers with explicit verbs",
        "Consider adding 1-2 edge case examples"
      ]
    },
    "execution": {
      "duration_minutes": 12,
      "enhanced": true,
      "timestamp": "2026-01-23T06:30:00Z"
    },
    "integration": {
      "scanned": true,
      "scan_report": "/INTEGRATION/logs/scan-report-20260123-063000.md"
    }
  },
  "next_steps": [
    "Review skill: INTEGRATION/incoming/[NAME]/SKILL.md",
    "Run '/integration-process' to finalize integration",
    "Test skill: 'Use [NAME] skill to...'"
  ]
}
```

### 10. Final Summary

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

QUALITY ASSESSMENT:
  Score: 22/25 (88%) ✅ PASSED
  • Structure: 5/5 ✓
  • Examples: 4/5 ⚠️
  • Triggers: 3/5 ⚠️
  • Knowledge: 5/5 ✓
  • Documentation: 5/5 ✓

INTEGRATION STATUS:
  ✅ Scanned and categorized by /integration-scan
  📋 Report: /INTEGRATION/logs/scan-report-[timestamp].md
  📊 JSON output: /INTEGRATION/logs/creation-result-[timestamp].json

NEXT STEPS:
  1. Review skill: INTEGRATION/incoming/[NAME]/SKILL.md
  2. Address recommendations (strengthen triggers)
  3. Run '/integration-process' to finalize integration
  4. Test skill: "Use [NAME] skill to..."

Time: [X] minutes | Size: [X] MB | Quality: ✅ Ready for Production
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
# Best approach: Use pre-configured config file from repository
/create-skill --config configs/fastapi.json
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

### Example 3: Just Command Runner (From Repository Config)
```bash
/create-skill --config configs/just.json
```

**Result**: Just command runner skill with recipe syntax, examples, and task automation patterns.

**Time**: ~6 minutes (smaller doc site)

### Example 4: Custom API Manual
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
  - Use configs from `configs/` directory (25+ pre-configured frameworks)
  - Create new configs in `configs/` directory for reusability
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

**Creating a new config:**
1. Create file in `configs/` directory: `configs/your-framework.json`
2. Use existing configs as templates (e.g., `configs/fastapi.json`)
3. Test with: `/create-skill --config configs/your-framework.json`
4. Commit to repository for reuse

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

**Example: Just command runner config** (`configs/just.json`):
```json
{
  "name": "just",
  "description": "Just command runner for project task automation",
  "base_url": "https://just.systems/",
  "start_urls": ["https://just.systems/man/en/"],
  "url_patterns": {
    "include": ["/man/en/"],
    "exclude": ["/blog/", "/changelog/"]
  },
  "categories": {
    "getting_started": ["introduction", "quick-start"],
    "recipes": ["recipes", "syntax"],
    "features": ["features", "patterns"]
  },
  "rate_limit": 0.5,
  "max_pages": 50
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

## Hooks Integration (Recommended)

For production deployments, implement quality enforcement hooks as described in [Document 02: Hooks](../../docs/best-practices/02-Individual-Command-Creation.md#introduction-to-hooks-runtime-validation):

### PostToolUse Hook: Automatic Skill Validation

Create `.claude/hooks/posttooluse_skill_quality.sh`:

```bash
#!/bin/bash
# Auto-validate generated skills after creation

INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name')

# Only run for Bash commands that moved files to INTEGRATION/incoming
if [ "$TOOL_NAME" = "Bash" ]; then
  COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command')

  if echo "$COMMAND" | grep -q "mv.*INTEGRATION/incoming"; then
    # Extract skill name from move command
    SKILL_NAME=$(echo "$COMMAND" | grep -oP 'INTEGRATION/incoming/\K[^/]+')
    SKILL_PATH="INTEGRATION/incoming/$SKILL_NAME"

    if [ -d "$SKILL_PATH" ]; then
      # Run validation
      if [ ! -f "$SKILL_PATH/SKILL.md" ]; then
        echo "❌ Quality gate failed: SKILL.md not found in $SKILL_NAME" >&2
        exit 2  # Blocking error
      fi

      # Check minimum line count
      LINES=$(wc -l < "$SKILL_PATH/SKILL.md")
      if [ "$LINES" -lt 50 ]; then
        echo "⚠️  Quality warning: SKILL.md only $LINES lines (expected >50)" >&2
      fi

      echo "✅ Quality gate passed: $SKILL_NAME validated"
    fi
  fi
fi

exit 0
```

**Configuration** (`.claude/settings.json`):
```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": ".claude/hooks/posttooluse_skill_quality.sh",
        "timeout": 10
      }]
    }]
  }
}
```

**Benefits**:
- **Automatic enforcement**: Skills must pass validation before proceeding
- **Fail-fast**: Catch quality issues immediately after generation
- **Zero manual oversight**: Hook runs deterministically

See [Document 05: Production-Grade Hooks](../../docs/best-practices/05-Testing-and-Quality-Assurance.md#production-grade-hooks-for-quality-assurance) for comprehensive hook patterns.

## CI/CD Integration

### GitHub Actions Example

Integrate skill generation into CI/CD pipelines:

```yaml
name: Auto-Generate Skills

on:
  schedule:
    - cron: '0 2 * * 1'  # Weekly Monday 2 AM
  workflow_dispatch:
    inputs:
      framework:
        description: 'Framework config to generate'
        required: true
        type: choice
        options:
          - fastapi
          - react
          - django
          - just

jobs:
  generate-skill:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install Skill Seekers
        run: pip install skill-seekers

      - name: Generate Skill
        uses: anthropic/claude-code-action@v1
        with:
          api-key: ${{ secrets.ANTHROPIC_API_KEY }}
          command: /create-skill
          args: --config configs/${{ inputs.framework }}.json --enhance
          output-format: json

      - name: Parse Quality Results
        id: quality
        run: |
          SCORE=$(jq -r '.skill.quality.score' creation-result.json)
          MAX=$(jq -r '.skill.quality.max_score' creation-result.json)
          PERCENT=$(jq -r '.skill.quality.percentage' creation-result.json)

          echo "score=$SCORE" >> $GITHUB_OUTPUT
          echo "percentage=$PERCENT" >> $GITHUB_OUTPUT

          # Fail if quality below threshold
          if [ "$PERCENT" -lt 80 ]; then
            echo "❌ Quality check failed: $PERCENT% (minimum 80%)"
            exit 1
          fi

      - name: Create Pull Request
        if: steps.quality.outputs.percentage >= 80
        uses: peter-evans/create-pull-request@v5
        with:
          title: "feat(skills): add ${{ inputs.framework }} skill (quality: ${{ steps.quality.outputs.percentage }}%)"
          body: |
            ## Auto-Generated Skill

            **Framework**: ${{ inputs.framework }}
            **Quality Score**: ${{ steps.quality.outputs.score }}/25 (${{ steps.quality.outputs.percentage }}%)

            ### Quality Breakdown
            ${{ toJSON(steps.quality.outputs) }}

            ### Next Steps
            - [ ] Review SKILL.md content
            - [ ] Test skill activation
            - [ ] Verify examples work
            - [ ] Merge when satisfied
          branch: auto-skill/${{ inputs.framework }}
          labels: auto-generated, skills
```

**Benefits**:
- **Automated skill updates**: Weekly refresh of documentation-based skills
- **Quality gates**: PR only created if score ≥80%
- **Structured reporting**: JSON output feeds PR description
- **Human approval**: PR workflow ensures review before merge

## Success Metrics & Monitoring

Track skill creation effectiveness over time:

### Key Performance Indicators

| Metric | Target | Measurement | Alert Threshold |
|--------|--------|-------------|-----------------|
| **Generation Success Rate** | >95% | Successful completions / total attempts | <90% |
| **Quality Score Average** | >85% | Mean quality score across all skills | <80% |
| **Time to Generate** | <15 min | P95 generation time | >25 min |
| **Post-Generation Edits** | <10% | Skills requiring manual fixes | >20% |
| **Activation Reliability** | >80% | Skills that activate on first try | <70% |

### Tracking Implementation

```python
# skill_metrics.py - Log creation metrics
import json
from datetime import datetime

def log_skill_creation(skill_name, quality_score, duration_min, source_type):
    """Log skill creation for trend analysis"""
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "skill": skill_name,
        "quality_score": quality_score,
        "duration_minutes": duration_min,
        "source_type": source_type,
        "success": quality_score >= 20  # 80% threshold
    }

    with open("INTEGRATION/logs/skill-creation-metrics.jsonl", "a") as f:
        f.write(json.dumps(log_entry) + "\n")

# Monthly analysis
def analyze_monthly_trends():
    """Generate monthly skill creation report"""
    # Parse logs, calculate averages, identify patterns
    # Output: Markdown report for review
```

### Dashboard Visualization

**Grafana Dashboard** (if using observability stack):
- Line chart: Generation success rate over time
- Histogram: Quality score distribution
- Heat map: Generation time by source type
- Table: Top 10 skills by activation frequency

## Command Composability

Break down `/create-skill` into atomic operations for flexible orchestration:

### Atomic Commands

```markdown
# /skill-generate - Generate skill (no validation)
!skill-seekers scrape --config $1 && mv output/* INTEGRATION/incoming/

# /skill-validate - Run quality checks only
!python3 validate_skill.py INTEGRATION/incoming/$1

# /skill-enhance - AI enhancement only
!skill-seekers enhance INTEGRATION/incoming/$1
```

### Orchestration Pattern

```markdown
# /create-skill-comprehensive - Full pipeline
1. Pre-validate source: /skill-validate-source $1
2. Generate: /skill-generate $1
3. Enhance: /skill-enhance $1
4. Quality check: /skill-validate $1
5. Integrate: /integration-scan
6. Report: Output JSON summary
```

**Benefits**:
- **Reusability**: Use `/skill-validate` independently for existing skills
- **Flexibility**: Skip enhancement for faster generation
- **Testability**: Test each atomic operation separately
- **Maintainability**: Fix one command, all compositions benefit

See [Document 02: Command Composability](../../docs/best-practices/02-Individual-Command-Creation.md#command-composability-and-orchestration) for orchestration patterns.

## Related Commands

- **`/integration-scan`** - Categorize incoming files (auto-run by this command)
- **`/integration-process`** - Move validated skills to final location
- **`/integration-validate`** - Run comprehensive quality checks
- **`/integration-update-docs`** - Update README with new skills

## Security & Compliance

### Least Privilege Principle

This command implements restrictive tool permissions:

```yaml
allowed-tools:
  - "Bash(pip:install,show)"        # Only pip install and show
  - "Bash(skill-seekers:*)"          # All skill-seekers commands
  - "Bash(python3:-c,-m)"            # Only -c and -m flags
  - "Bash(which:*)"                   # Binary location checks
  - "Bash(ls:-la)"                    # List with details only
  - "Bash(mkdir:-p)"                  # Create directories only
  - "Bash(mv:*)"                      # Move operations
  - "Bash(test:-f)"                   # File existence checks only
  - "Read"                            # Read files
  - "Write"                           # Write logs
```

**What's NOT allowed**:
- ❌ Unrestricted shell access (`Bash` without patterns)
- ❌ File deletion commands (`rm`, `rmdir`)
- ❌ Network operations beyond pip/skill-seekers
- ❌ System modifications (`chmod`, `chown`)

### Data Sanitization

```bash
# Sanitize skill name input (prevent path traversal)
SKILL_NAME=$(echo "$INPUT_NAME" | sed 's/[^a-zA-Z0-9_-]//g')

# Validate config file path (prevent directory traversal)
if echo "$CONFIG_PATH" | grep -q '\.\./'; then
  echo "❌ Security: Path traversal detected in config path"
  exit 1
fi

# Sanitize URLs (prevent malicious redirects)
if ! echo "$URL" | grep -qE '^https?://[a-zA-Z0-9.-]+'; then
  echo "❌ Security: Invalid URL format"
  exit 1
fi
```

### Audit Trail

All skill creation operations logged:

```json
{
  "timestamp": "2026-01-23T06:30:00Z",
  "user": "${USER}",
  "command": "/create-skill",
  "parameters": {
    "config": "configs/fastapi.json",
    "enhance": true
  },
  "output": {
    "skill_name": "fastapi",
    "quality_score": 22,
    "status": "success"
  },
  "security_events": []
}
```

Log location: `INTEGRATION/logs/skill-creation-audit.jsonl`

See [Document 02: Security Standards](../../docs/best-practices/02-Individual-Command-Creation.md#security) and [Document 06: Audit Trails](../../docs/best-practices/06-Production-Deployment-and-Maintenance.md#audit-trails-and-change-management) for compliance patterns.

## Progressive Disclosure Architecture

Rather than embedding all workflow details inline, reference external documentation:

### Skill Generation Workflows

For detailed generation procedures, see:
- **Documentation scraping**: `.claude/rules/skill-generation-docs.md`
- **GitHub extraction**: `.claude/rules/skill-generation-github.md`
- **PDF processing**: `.claude/rules/skill-generation-pdf.md`
- **Quality validation**: `.claude/rules/skill-quality-standards.md`

### Config File Specifications

For config creation guidelines, see:
- **Config schema**: `.claude/rules/skill-config-schema.json`
- **Best practices**: `.claude/rules/skill-config-best-practices.md`
- **Available frameworks**: `configs/README.md`

**Benefits**:
- Prevents context window saturation (command stays <600 lines)
- Enables on-demand retrieval (Claude loads only when needed)
- Supports ownership distribution (different teams maintain different rule files)

See [Document 02: Progressive Disclosure](../../docs/best-practices/02-Individual-Command-Creation.md#progressive-disclosure-for-commands) for modular architecture patterns.

## Testing Strategy

### Unit Testing Commands

Test atomic operations independently:

```python
# tests/test_create_skill_command.py
import subprocess
import json
import pytest

def test_input_validation():
    """Verify input validation catches invalid parameters"""
    result = subprocess.run(
        ["claude", "code", "/create-skill"],  # No parameters
        capture_output=True,
        text=True
    )
    assert result.returncode == 1
    assert "Error: One of --url, --github, --pdf, or --config is required" in result.stderr

def test_source_accessibility():
    """Verify source accessibility check"""
    result = subprocess.run(
        ["claude", "code", "/create-skill", "--url", "https://invalid-domain-12345.com", "--name", "test"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 1
    assert "URL not accessible" in result.stderr

def test_quality_scoring():
    """Verify quality scoring rubric"""
    # Generate test skill
    result = subprocess.run(
        ["claude", "code", "/create-skill", "--config", "tests/fixtures/minimal.json"],
        capture_output=True,
        text=True
    )

    # Parse JSON output
    output = json.loads(result.stdout)

    # Validate quality structure
    assert "quality" in output["skill"]
    assert output["skill"]["quality"]["score"] >= 0
    assert output["skill"]["quality"]["score"] <= 25
    assert output["skill"]["quality"]["percentage"] >= 0
    assert output["skill"]["quality"]["percentage"] <= 100

@pytest.mark.slow
def test_fastapi_config_generation():
    """Integration test: Full FastAPI skill generation"""
    result = subprocess.run(
        ["claude", "code", "/create-skill", "--config", "configs/fastapi.json"],
        capture_output=True,
        text=True,
        timeout=900  # 15 minutes
    )

    assert result.returncode == 0
    output = json.loads(result.stdout)

    # Validate output
    assert output["status"] == "success"
    assert output["skill"]["quality"]["percentage"] >= 80
    assert output["skill"]["output"]["files"]["skill_md"] == True

    # Verify file exists
    import os
    assert os.path.exists("INTEGRATION/incoming/fastapi/SKILL.md")
```

### Integration Testing with CI

```yaml
# .github/workflows/test-create-skill.yml
name: Test Create Skill Command

on:
  pull_request:
    paths:
      - '.claude/commands/create-skill.md'
      - 'configs/**'

jobs:
  test-command:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install Dependencies
        run: |
          pip install skill-seekers pytest

      - name: Run Unit Tests
        run: pytest tests/test_create_skill_command.py -v

      - name: Test Config Validation
        run: |
          # Verify all configs are valid JSON
          for config in configs/*.json; do
            jq empty "$config" || exit 1
          done

      - name: Integration Test (Fast Config)
        run: |
          # Test with small, fast config
          claude code /create-skill --config tests/fixtures/minimal.json

          # Verify output
          test -f INTEGRATION/incoming/minimal/SKILL.md
```

See [Document 05: Testing Strategies](../../docs/best-practices/05-Testing-and-Quality-Assurance.md) for comprehensive testing patterns.

## Anti-Patterns to Avoid

Based on production experience and [Document 09: Common Pitfalls](../../docs/best-practices/09-Developing-High-Impact-Claude-Skills.md#common-pitfalls):

### ❌ Don't: Generate without validation
```bash
# BAD: Generate blindly
skill-seekers scrape --url $URL --name $NAME
```

### ✅ Do: Validate then generate
```bash
# GOOD: Check source first
curl -sI "$URL" | grep -q "200" && skill-seekers scrape --url $URL --name $NAME
```

### ❌ Don't: Ignore quality scores
```bash
# BAD: Move to integration regardless of quality
mv output/$NAME INTEGRATION/incoming/
```

### ✅ Do: Enforce quality gates
```bash
# GOOD: Check quality threshold
SCORE=$(calculate_quality_score)
if [ "$SCORE" -ge 20 ]; then
  mv output/$NAME INTEGRATION/incoming/
else
  echo "❌ Quality gate failed: Score $SCORE/25 (need ≥20)"
  exit 1
fi
```

### ❌ Don't: Use hardcoded paths
```bash
# BAD: Assumes specific directory structure
mv output/fastapi ~/my-skills/fastapi
```

### ✅ Do: Use dynamic paths
```bash
# GOOD: Respects configuration
INTEGRATION_DIR="${INTEGRATION_DIR:-INTEGRATION/incoming}"
mv output/$NAME "$INTEGRATION_DIR/$NAME"
```

### ❌ Don't: Grant wildcard shell access
```yaml
# BAD: Unrestricted access
allowed-tools: ["Bash"]
```

### ✅ Do: Use explicit permission scoping
```yaml
# GOOD: Specific operations only
allowed-tools: ["Bash(skill-seekers:*)", "Bash(mv:*)", "Read", "Write"]
```

## Troubleshooting Decision Tree

```
Skill generation failed?
│
├─> ❌ "Command not found"
│   └─> Check: Python installed? pip available?
│       Fix: python3 --version && pip --version
│
├─> ❌ "URL not accessible"
│   └─> Check: URL loads in browser? Behind auth?
│       Fix: Use --pdf for downloaded docs OR create config with auth headers
│
├─> ❌ "Quality score < 20"
│   ├─> Missing examples?
│   │   Fix: Run with --enhance flag
│   ├─> Weak activation triggers?
│   │   Fix: Manually edit SKILL.md to add action verbs
│   └─> Insufficient knowledge extracted?
│       Fix: Use config file instead of basic --url
│
├─> ❌ "SKILL.md not found"
│   └─> Check: skill-seekers version up to date?
│       Fix: pip install --upgrade skill-seekers
│
└─> ❌ "Out of disk space"
    └─> Check: df -h INTEGRATION/incoming
        Fix: Clean up old skills OR increase disk space
```

## Version History

- **2.0.0** (2026-01-23): Production-grade enhancements (**BREAKING CHANGE**)
  - **Breaking**: Enforces quality gates (score ≥20/25 required)
  - **Breaking**: Requires explicit permission scoping in allowed-tools
  - Added pre-execution validation (source accessibility, disk space, prerequisites)
  - Added quality scoring rubric (5 criteria, 25-point scale)
  - Added structured JSON output for CI/CD integration
  - Added hooks integration patterns (PostToolUse validation)
  - Added CI/CD examples (GitHub Actions workflow)
  - Added success metrics & monitoring (KPIs, logging)
  - Added command composability patterns (atomic operations)
  - Added security & compliance (audit trails, input sanitization)
  - Added progressive disclosure architecture (external rule files)
  - Added comprehensive testing strategy (unit, integration, CI)
  - Added anti-patterns and troubleshooting decision tree
  - Updated documentation references to consolidated docs/best-practices/

- **1.1** (2025-12-28): Config directory integration
  - Use local `configs/` directory for all configurations
  - Added 25+ pre-configured framework configs
  - Added Just command runner example
  - Improved config creation workflow
  - Config file reusability across team

- **1.0** (2025-12-26): Initial release
  - Documentation, GitHub, and PDF support
  - Auto-install capability
  - AI enhancement option
  - Auto-scan integration
  - Comprehensive error handling

---

## Summary of Enhancements (v2.0)

This version implements production-grade patterns from:
- [Document 02: Command Creation](../../docs/best-practices/02-Individual-Command-Creation.md) - Three-tier hierarchy, composability, permissions, progressive disclosure, hooks, CI/CD
- [Document 08: Skills Guide](../../docs/best-practices/08-Claude-Skills-Guide.md) - Skills-first paradigm, activation reliability
- [Document 09: Skills Development](../../docs/best-practices/09-Developing-High-Impact-Claude-Skills.md) - Quality assessment, evaluation framework, testing

**Key Improvements**:
1. **Quality Enforcement**: 25-point rubric with 80% threshold
2. **Security Hardening**: Least privilege, input sanitization, audit trails
3. **CI/CD Ready**: JSON output, GitHub Actions integration, automated PR creation
4. **Observable**: Comprehensive logging, metrics tracking, quality scoring
5. **Composable**: Atomic operations, orchestration patterns, flexible workflows
6. **Testable**: Unit tests, integration tests, CI validation
7. **Maintainable**: Progressive disclosure, modular architecture, clear anti-patterns

**Breaking Changes**:
- Quality scores below 20/25 now FAIL (was: warn only)
- Explicit permission scoping required (was: `["Bash"]` wildcard)
- JSON output format (was: text only)

**Migration Guide**:
- Update `.claude/settings.json` with explicit `allowed-tools` scoping
- Add quality gate handling in CI/CD pipelines (check `skill.quality.percentage >= 80`)
- Parse JSON output instead of text parsing

---

**Last Updated**: January 23, 2026
**Version**: 2.0.0 (Production-Grade)
**Dependencies**:
  - skill-seekers package (≥2.2.0)
  - /INTEGRATION directory structure
  - configs/ directory (25+ frameworks)
  - Python 3.8+
  - pip package manager
**Integration**: Works seamlessly with integration pipeline commands
**Documentation**: See docs/best-practices/ for comprehensive patterns
**Available Configs**: 25+ frameworks in `configs/` directory (FastAPI, React, Django, Just, Kubernetes, Tailwind, and more)
