---
name: skill-packager
description: Package skills into uploadable ZIP files for Claude. Use after skill-builder/skill-enhancer to create final upload package.
tools: Read, Write, Bash
---

# Skill Packager Skill

## Purpose

Single responsibility: Package completed skill directories into ZIP files ready for upload to Claude AI. (BP-4)

## Grounding Checkpoint (Archetype 1 Mitigation)

Before executing, VERIFY:

- [ ] Skill directory exists with required structure
- [ ] SKILL.md is present and non-empty
- [ ] At least one reference file exists
- [ ] No sensitive data in skill directory
- [ ] Output path for ZIP is writable

**DO NOT package without validating skill structure.**

## Uncertainty Escalation (Archetype 2 Mitigation)

ASK USER instead of guessing when:

- Skill structure incomplete - proceed anyway?
- Large files detected - include or exclude?
- Sensitive patterns found (API keys, passwords)
- Multiple skill directories - which to package?

**NEVER package potentially sensitive content without review.**

## Context Scope (Archetype 3 Mitigation)

| Context Type | Included | Excluded |
|--------------|----------|----------|
| RELEVANT | Skill directory contents, package config | Other skills |
| PERIPHERAL | Package size estimates | Source data |
| DISTRACTOR | Build process details | Scraping history |

## Workflow Steps

### Step 1: Validate Skill Structure (Grounding)

```bash
# Required structure check
test -f output/<skill-name>/SKILL.md || echo "ERROR: Missing SKILL.md"
test -d output/<skill-name>/references || echo "ERROR: Missing references/"

# Check SKILL.md is not empty
test -s output/<skill-name>/SKILL.md || echo "ERROR: SKILL.md is empty"

# Check for at least one reference
ls output/<skill-name>/references/*.md >/dev/null 2>&1 || echo "ERROR: No reference files"
```

### Step 2: Security Check

```bash
# Scan for potential sensitive data
grep -rE "(api[_-]?key|password|secret|token|credential)" output/<skill-name>/ && \
  echo "WARNING: Potential sensitive data found - review before packaging"

# Check for large files
find output/<skill-name>/ -size +10M -exec echo "WARNING: Large file: {}" \;

# Check for binary files
find output/<skill-name>/ -type f ! -name "*.md" ! -name "*.json" ! -name "*.txt" \
  -exec file {} \; | grep -v "text" && echo "WARNING: Non-text files found"
```

### Step 3: Calculate Package Size

```bash
# Estimate final size
du -sh output/<skill-name>/

# Count files
find output/<skill-name>/ -type f | wc -l

# List file types
find output/<skill-name>/ -type f -name "*.*" | sed 's/.*\.//' | sort | uniq -c
```

### Step 4: Create Package

**Option A: With skill-seekers**

```bash
# Standard packaging
skill-seekers package output/<skill-name>/

# With upload (if API key set)
skill-seekers package output/<skill-name>/ --upload
```

**Option B: Manual packaging**

```bash
# Navigate to output directory
cd output/

# Create ZIP (exclude backups and temp files)
zip -r <skill-name>.zip <skill-name>/ \
  -x "*.backup" \
  -x "*.tmp" \
  -x ".DS_Store" \
  -x "__MACOSX/*"

# Verify ZIP contents
unzip -l <skill-name>.zip
```

### Step 5: Validate Package

```bash
# Check ZIP integrity
unzip -t output/<skill-name>.zip

# Verify required files are included
unzip -l output/<skill-name>.zip | grep "SKILL.md"
unzip -l output/<skill-name>.zip | grep "references/"

# Check size is reasonable
ls -lh output/<skill-name>.zip
```

## Recovery Protocol (Archetype 4 Mitigation)

On error:

1. **PAUSE** - Don't overwrite existing ZIP
2. **DIAGNOSE** - Check error type:
   - `Missing files` → Run skill-builder first
   - `ZIP error` → Check disk space, permissions
   - `Large size` → Exclude unnecessary files
   - `Sensitive data` → Clean files, re-package
3. **ADAPT** - Adjust package configuration
4. **RETRY** - With corrected settings (max 3 attempts)
5. **ESCALATE** - Report packaging issues to user

## Checkpoint Support

State saved to: `.aiwg/working/checkpoints/skill-packager/`

```
checkpoints/skill-packager/
├── validation_results.json  # Pre-package validation
├── security_scan.json       # Security check results
├── package_manifest.json    # Files included
└── package_log.txt          # Packaging process log
```

## Package Manifest

Generate manifest for verification:

```json
{
  "skill_name": "myskill",
  "packaged_at": "2025-01-15T10:30:00Z",
  "files": [
    {"path": "SKILL.md", "size": 15234, "hash": "abc123..."},
    {"path": "references/index.md", "size": 2045, "hash": "def456..."},
    {"path": "references/api.md", "size": 45678, "hash": "ghi789..."}
  ],
  "total_files": 5,
  "total_size": 62957,
  "package_size": 18234
}
```

## Upload Options

### Option 1: Automatic Upload (API)

```bash
export ANTHROPIC_API_KEY=sk-ant-...
skill-seekers package output/<skill-name>/ --upload
```

### Option 2: Manual Upload

1. Package creates `output/<skill-name>.zip`
2. Open output folder automatically
3. Go to https://claude.ai/skills
4. Click "Upload Skill"
5. Select ZIP file
6. Done!

### Option 3: Via Claude Code (MCP)

```
"Package and upload the myskill skill"
```

## Exclusion Patterns

Default exclusions:

```
*.backup
*.tmp
*.log
.DS_Store
__MACOSX/
.git/
node_modules/
__pycache__/
*.pyc
.env
*.key
*.pem
```

## Size Limits

| Platform | Max Size | Recommendation |
|----------|----------|----------------|
| Claude.ai | 50MB | Keep under 10MB |
| API | Variable | Keep under 20MB |

If over limit:
1. Remove large images
2. Compress reference files
3. Split into sub-skills

## Configuration Options

```json
{
  "skill_dir": "output/myskill/",
  "output_zip": "output/myskill.zip",
  "options": {
    "include_manifest": true,
    "compress_level": 9,
    "exclude_patterns": ["*.backup", "*.tmp"],
    "security_check": true,
    "auto_upload": false
  }
}
```

## Troubleshooting

| Issue | Diagnosis | Solution |
|-------|-----------|----------|
| ZIP too large | Large assets | Exclude or compress images |
| Missing files | Validation failed | Run skill-builder first |
| Upload failed | API error | Check API key, retry |
| Corrupt ZIP | Disk issue | Check disk space, re-create |

## References

- Claude Skills Upload: https://claude.ai/skills
- Skill Seekers Packaging: https://github.com/jmagly/Skill_Seekers
- REF-001: Production-Grade Agentic Workflows (BP-2 direct functions)
- REF-002: LLM Failure Modes (Archetype 1 grounding before action)
