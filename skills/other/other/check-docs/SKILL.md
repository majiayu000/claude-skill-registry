---
name: check-docs
version: "1.0.0"
last-updated: "2026-03-15"
---

# Check Docs - Validate Documentation Structure

Validate documentation structure compliance with framework standards and provide actionable fix suggestions.

## Overview

This skill provides comprehensive documentation validation by:

**What it does:**
1. **Structure Validation** - Checks required directories exist
2. **File Validation** - Verifies mandatory documentation files
3. **Naming Convention Validation** - Ensures kebab-case, UPPERCASE.md patterns
4. **ADR Validation** - Checks sequential numbering and completeness
5. **Compliance Scoring** - Generates 0-100 score with breakdown
6. **Fix Suggestions** - Provides actionable commands to resolve issues
7. **Auto-Fix Mode** - Optionally fixes issues automatically

**Why it's needed:**
Documentation structure inconsistencies lead to confusion, missed updates, and poor knowledge management. Manual validation is tedious and error-prone. This skill automates validation and provides clear guidance for fixes.

**When to use:**
- After `/init-docs` to verify structure created correctly
- Before major releases to ensure documentation complete
- In CI/CD pipelines to enforce standards
- When onboarding new projects to the framework

**Pairs with /init-docs:**
```
/init-docs        # Create documentation structure
/check-docs       # Validate structure compliance
/check-docs --fix # Auto-fix any issues
```

## Arguments

```bash
/check-docs [options]
```

**Common usage:**
```bash
/check-docs                    # Basic validation report
/check-docs --verbose          # Detailed file-by-file output
/check-docs --fix              # Auto-fix issues
/check-docs --profile tauri    # Check against specific profile
/check-docs --json             # JSON output for CI/CD
```

**Options:**
- `--verbose` - Show detailed output with file-by-file checks
- `--fix` - Automatically fix issues (rename files, create directories)
- `--profile <name>` - Check against specific profile (tauri, tauri-aws, nextjs-aws)
- `--json` - Output results in JSON format for automation

## AI Execution Instructions

**CRITICAL: Validation workflow and scoring**

When executing `/check-docs`, AI MUST follow this pattern:

### Step 1: Detect Profile

```python
# Read .framework-install to determine profile
try:
    with open('.framework-install', 'r') as f:
        install_data = json.load(f)
        profile = install_data.get('profile', 'minimal')
except FileNotFoundError:
    profile = 'minimal'  # Default fallback

# Override if --profile provided
if args.profile:
    profile = args.profile
```

### Step 2: Load Profile-Specific Requirements

```python
# Profile-specific directory requirements
PROFILE_DIRS = {
    'tauri': ['docs/desktop/'],
    'tauri-aws': ['docs/desktop/', 'docs/aws/'],
    'nextjs-aws': ['docs/aws/']
}

# Base requirements (all profiles)
required_dirs = [
    'docs/',
    'docs/ADRs/',
    'docs/architecture/',
    'docs/api/',
    'docs/guides/',
    'docs/diagrams/'
]

# Add profile-specific
if profile in PROFILE_DIRS:
    required_dirs.extend(PROFILE_DIRS[profile])
```

### Step 3: Run 4 Validation Dimensions

```python
scores = {
    "directories": validate_structure(required_dirs, max=30),
    "files": validate_files(required_files, max=40),
    "naming": validate_naming(all_files, max=15),
    "adrs": validate_adrs(adr_dir, max=15)
}

total_score = sum(scores.values())  # Max 100
```

### Step 4: Generate Fix Suggestions

```python
fixes = []

# Missing directories
for missing_dir in missing_directories:
    fixes.append({
        "type": "mkdir",
        "command": f"mkdir -p {missing_dir}",
        "description": f"Create missing directory: {missing_dir}"
    })

# Missing files
if missing_files:
    fixes.append({
        "type": "init-docs",
        "command": "/init-docs --force",
        "description": "Generate missing documentation files"
    })

# Naming violations
for violation in naming_violations:
    fixes.append({
        "type": "rename",
        "command": f"mv {violation.old} {violation.new}",
        "description": f"Fix naming: {violation.issue}"
    })

# ADR numbering
for gap in adr_gaps:
    fixes.append({
        "type": "renumber",
        "command": f"mv {gap.old} {gap.new}",
        "description": f"Fix ADR numbering gap: {gap.number}"
    })
```

### Step 5: Apply Auto-Fix (if --fix)

```python
if args.fix:
    for fix in fixes:
        if fix.type == "mkdir":
            os.makedirs(fix.path, exist_ok=True)
        elif fix.type == "rename":
            shutil.move(fix.old, fix.new)
        elif fix.type == "init-docs":
            # Call init-docs skill for missing files
            Skill("init-docs", args="--force")

    # Re-validate after fixes
    new_score = run_validation()
    report_improvement(old_score, new_score)
```

### Step 6: Output Report

```python
if args.json:
    output_json(scores, fixes, total_score)
else:
    output_human_readable(scores, fixes, total_score, args.verbose)

# Exit with appropriate code
sys.exit(get_exit_code(total_score))
```

## Workflow Steps

Copy this checklist to track progress:

```
Task Progress:
- [ ] Step 1: Detect profile
- [ ] Step 2: Load requirements
- [ ] Step 3: Validate structure (4 dimensions)
- [ ] Step 4: Generate fix suggestions
- [ ] Step 5: Apply auto-fix (if --fix)
- [ ] Step 6: Output report and exit
```

Execute these steps in sequence:

### Step 1: Detect Profile

**Determine which profile to validate against:**

```bash
# Check .framework-install
cat .framework-install

# Extract profile
PROFILE=$(cat .framework-install | grep -o '"profile": "[^"]*' | cut -d'"' -f4)

# Fallback to minimal if not found
PROFILE=${PROFILE:-minimal}
```

**Override with --profile flag if provided.**

### Step 2: Load Requirements

**Base requirements (all profiles):**
- **Directories**: docs/, docs/ADRs/, docs/architecture/, docs/api/, docs/guides/, docs/diagrams/
- **Files**: README.md, PRD.md, ARCHITECTURE.md, SCHEMA.md, API.md, SETUP.md, TEST_PLAN.md, DEPLOYMENT.md

**Profile-specific additions:**
- **tauri**: docs/desktop/
- **tauri-aws**: docs/desktop/, docs/aws/
- **nextjs-aws**: docs/aws/

### Step 3: Validate Structure (4 Dimensions)

**Dimension 1: Directory Validation (30 points)**

```bash
# Check each required directory exists
for dir in "${required_dirs[@]}"; do
    if [ -d "$dir" ]; then
        score=$((score + 6))
    else
        missing+=("$dir")
    fi
done

# Max 30 points (5 base dirs × 6 pts each)
```

**Dimension 2: File Validation (40 points)**

```bash
# Check each required file exists
required_files=(
    "docs/README.md"
    "docs/PRD.md"
    "docs/ARCHITECTURE.md"
    "docs/SCHEMA.md"
    "docs/API.md"
    "docs/SETUP.md"
    "docs/TEST_PLAN.md"
    "docs/DEPLOYMENT.md"
)

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        score=$((score + 5))
    else
        missing_files+=("$file")
    fi
done

# Max 40 points (8 files × 5 pts each)
```

**Dimension 3: Naming Convention Validation (15 points)**

```bash
violations=0

# Check directory names (kebab-case)
find docs/ -type d | while read dir; do
    basename=$(basename "$dir")
    if [[ ! "$basename" =~ ^[a-z0-9-]+$ ]]; then
        violations=$((violations + 1))
        echo "❌ Directory naming violation: $dir"
    fi
done

# Check file names (UPPERCASE.md for top-level)
find docs/ -maxdepth 1 -name "*.md" | while read file; do
    basename=$(basename "$file" .md)
    if [[ ! "$basename" =~ ^[A-Z_]+$ ]] && [ "$basename" != "README" ]; then
        violations=$((violations + 1))
        echo "❌ File naming violation: $file"
    fi
done

# Check ADR naming (NNN-title.md)
find docs/ADRs/ -name "*.md" | while read adr; do
    basename=$(basename "$adr")
    if [[ ! "$basename" =~ ^[0-9]{3}-[a-z0-9-]+\.md$ ]] && [ "$basename" != "README.md" ]; then
        violations=$((violations + 1))
        echo "❌ ADR naming violation: $adr"
    fi
done

# Scoring: 15 points - (violations × 3)
naming_score=$((15 - violations * 3))
naming_score=$((naming_score < 0 ? 0 : naming_score))
```

**Dimension 4: ADR Validation (15 points)**

```bash
# Check ADRs are numbered sequentially
adrs=$(find docs/ADRs/ -name "[0-9]*.md" | sort)
adr_count=$(echo "$adrs" | wc -l)

expected=0
gaps=0

for adr in $adrs; do
    number=$(basename "$adr" | grep -o '^[0-9]\+')
    if [ "$number" -ne "$expected" ]; then
        gaps=$((gaps + 1))
        echo "❌ ADR numbering gap: expected $expected, found $number"
    fi
    expected=$((number + 1))
done

# Check ADR index exists
if [ ! -f "docs/ADRs/README.md" ]; then
    echo "❌ ADR index missing: docs/ADRs/README.md"
    gaps=$((gaps + 1))
fi

# Scoring: 15 points - (gaps × 5)
adr_score=$((15 - gaps * 5))
adr_score=$((adr_score < 0 ? 0 : adr_score))
```

### Step 4: Generate Fix Suggestions

**For missing directories:**
```bash
echo "Fix: mkdir -p docs/ADRs docs/architecture docs/api docs/guides docs/diagrams"
```

**For missing files:**
```bash
echo "Fix: /init-docs --force"
echo "  Or create manually:"
echo "    touch docs/README.md docs/PRD.md docs/ARCHITECTURE.md ..."
```

**For naming violations:**
```bash
echo "Fix: mv docs/My-Guide.md docs/my-guide.md"
echo "Fix: mv docs/adr-001.md docs/ADRs/001-decision-title.md"
```

**For ADR numbering:**
```bash
echo "Fix: mv docs/ADRs/005-title.md docs/ADRs/003-title.md  # Fill gap"
```

### Step 5: Apply Auto-Fix (if --fix)

**Execute fix commands automatically:**

```bash
# Create missing directories
mkdir -p docs/ADRs docs/architecture docs/api docs/guides docs/diagrams

# Rename files
mv docs/My-Guide.md docs/my-guide.md

# Create missing files via init-docs
/init-docs --force

# Renumber ADRs
# (Complex logic to renumber sequentially)
```

**After fixes, re-validate and show improvement:**
```bash
echo "Before: 65/100"
echo "After:  95/100"
echo "Improvement: +30 points"
```

### Step 6: Output Report and Exit

**Human-readable format:**
```
📊 Documentation Compliance Report

**Score**: 85/100 ⚠️ Needs improvement
**Profile**: tauri

## Breakdown
✅ Directory Structure: 30/30
⚠️  Required Files: 35/40 (1 missing)
✅ Naming Conventions: 15/15
⚠️  ADR Validation: 5/15 (gaps in numbering)

## Issues Found

### Missing Files (5 points deducted)
- docs/DEPLOYMENT.md

### ADR Issues (10 points deducted)
- Numbering gap: expected 003, found 005
- ADR index missing: docs/ADRs/README.md

## Fix Suggestions

1. Create missing file:
   touch docs/DEPLOYMENT.md

2. Renumber ADR:
   mv docs/ADRs/005-title.md docs/ADRs/003-title.md

3. Create ADR index:
   /adr list > docs/ADRs/README.md

4. Or use auto-fix:
   /check-docs --fix

## Next Steps
- Fix issues manually using commands above
- Or run: /check-docs --fix
- Target score: 100/100
```

**JSON format (for CI/CD):**
```json
{
  "timestamp": "2026-03-15T10:30:00Z",
  "profile": "tauri",
  "score": 85,
  "max_score": 100,
  "status": "needs_improvement",
  "breakdown": {
    "directories": {"score": 30, "max": 30},
    "files": {"score": 35, "max": 40},
    "naming": {"score": 15, "max": 15},
    "adrs": {"score": 5, "max": 15}
  },
  "issues": [
    {"type": "missing_file", "severity": "minor", "path": "docs/DEPLOYMENT.md"},
    {"type": "adr_gap", "severity": "major", "expected": 3, "found": 5},
    {"type": "missing_file", "severity": "major", "path": "docs/ADRs/README.md"}
  ],
  "fixes": [
    {"command": "touch docs/DEPLOYMENT.md", "description": "Create missing file"},
    {"command": "mv docs/ADRs/005-title.md docs/ADRs/003-title.md", "description": "Fix ADR numbering"},
    {"command": "/adr list > docs/ADRs/README.md", "description": "Create ADR index"}
  ]
}
```

**Exit codes:**
```bash
if [ $score -eq 100 ]; then
    exit 0  # Perfect compliance
elif [ $score -ge 70 ]; then
    exit 1  # Minor issues
elif [ $score -gt 0 ]; then
    exit 2  # Major issues
else
    exit 3  # Validation error (docs/ not found)
fi
```

## Validation Logic Details

### Directory Structure Validation

**Required directories (base):**
- `docs/` - Root documentation directory
- `docs/ADRs/` - Architecture Decision Records
- `docs/architecture/` - System architecture documentation
- `docs/api/` - API documentation
- `docs/guides/` - User and developer guides
- `docs/diagrams/` - Architecture diagrams

**Profile-specific directories:**
- **tauri**: `docs/desktop/` - Desktop app specific docs
- **tauri-aws/nextjs-aws**: `docs/aws/` - AWS infrastructure docs

**Scoring:** 6 points per directory (max 30)

### File Validation

**Required files (all profiles):**
1. `docs/README.md` - Navigation hub and documentation index
2. `docs/PRD.md` - Product Requirements Document
3. `docs/ARCHITECTURE.md` - System architecture overview
4. `docs/SCHEMA.md` - Data models and database schema
5. `docs/API.md` - API endpoints and contracts
6. `docs/SETUP.md` - Installation and setup instructions
7. `docs/TEST_PLAN.md` - Testing strategy and test cases
8. `docs/DEPLOYMENT.md` - Deployment procedures

**Scoring:** 5 points per file (max 40)

### Naming Convention Rules

**Directory names:**
- Must use lowercase letters
- Hyphens allowed for word separation (kebab-case)
- No spaces, underscores, or camelCase
- Examples: ✅ `user-guides`, `api-docs` | ❌ `User_Guides`, `apiDocs`

**Top-level file names:**
- UPPERCASE with underscores
- `.md` extension
- Examples: ✅ `README.md`, `API.md`, `TEST_PLAN.md` | ❌ `readme.md`, `Api.md`

**ADR file names:**
- Pattern: `NNN-title.md` where NNN is 3-digit number
- Title uses lowercase with hyphens
- Examples: ✅ `001-skill-patterns.md` | ❌ `adr-001.md`, `1-skill-patterns.md`

**Scoring:** 15 points - (violations × 3)

### ADR Validation Rules

**Sequential numbering:**
- ADRs must be numbered 000, 001, 002, 003... without gaps
- Numbering starts at 000 or 001 (both valid)
- Gap detection: If 001, 002, 005 exist → gap at 003, 004

**ADR index:**
- Must exist at `docs/ADRs/README.md`
- Should list all ADRs with links

**Scoring:** 15 points - (gaps × 5)

## Error Handling

**Common errors and solutions:**

**docs/ directory not found:**
```
❌ Documentation directory not found

Expected: docs/
Current directory: {pwd}

Fix:
1. Initialize documentation: /init-docs
2. Or create manually: mkdir docs
```

**Permission denied:**
```
❌ Permission denied reading docs/

Fix: chmod -R u+r docs/
```

**.framework-install missing:**
```
⚠️ .framework-install not found

Using default profile: minimal

Fix: Run /init-project or specify profile:
  /check-docs --profile tauri
```

**Invalid profile:**
```
❌ Invalid profile: custom-profile

Valid profiles: tauri, tauri-aws, nextjs-aws

Fix: /check-docs --profile tauri
```

## Examples

### Example 1: Basic Validation

**User says:**
> "check my documentation structure"

**Execute:**
```bash
/check-docs
```

**Output:**
```
📊 Documentation Compliance Report

**Score**: 100/100 ✅ Perfect compliance
**Profile**: tauri

## Breakdown
✅ Directory Structure: 30/30
✅ Required Files: 40/40
✅ Naming Conventions: 15/15
✅ ADR Validation: 15/15

🎉 Documentation structure is perfect!
No issues found.
```

**Time:** <5 seconds

### Example 2: Validation with Issues

**User says:**
> "check docs in verbose mode"

**Execute:**
```bash
/check-docs --verbose
```

**Output:**
```
📊 Documentation Compliance Report

**Score**: 75/100 ⚠️ Needs improvement
**Profile**: tauri

## Detailed Check Results

### Directory Structure (24/30)
✅ docs/ exists
✅ docs/ADRs/ exists
✅ docs/architecture/ exists
✅ docs/api/ exists
❌ docs/guides/ missing (-6)
✅ docs/diagrams/ exists
✅ docs/desktop/ exists (profile: tauri)

### Required Files (35/40)
✅ docs/README.md
✅ docs/PRD.md
✅ docs/ARCHITECTURE.md
✅ docs/SCHEMA.md
✅ docs/API.md
✅ docs/SETUP.md
❌ docs/TEST_PLAN.md missing (-5)
✅ docs/DEPLOYMENT.md

### Naming Conventions (12/15)
✅ Directory names: docs/, ADRs/, architecture/, api/, diagrams/, desktop/
❌ File: docs/Api-Guide.md should be docs/API_GUIDE.md (-3)
✅ ADR names: 001-patterns.md, 002-workflow.md

### ADR Validation (10/15)
✅ ADRs numbered sequentially (001, 002)
❌ ADR index missing: docs/ADRs/README.md (-5)

## Fix Suggestions
1. mkdir -p docs/guides
2. touch docs/TEST_PLAN.md
3. mv docs/Api-Guide.md docs/API_GUIDE.md
4. /adr list > docs/ADRs/README.md

Or use: /check-docs --fix
```

**Time:** <10 seconds

### Example 3: Auto-Fix Mode

**User says:**
> "fix my documentation structure automatically"

**Execute:**
```bash
/check-docs --fix
```

**Output:**
```
🔧 Auto-Fix Mode

Before fixes: 75/100

Applying fixes:
✅ Created directory: docs/guides/
✅ Created file: docs/TEST_PLAN.md
✅ Renamed: docs/Api-Guide.md → docs/API_GUIDE.md
✅ Created ADR index: docs/ADRs/README.md

Re-validating...

After fixes: 100/100 ✅

🎉 All issues resolved!
Improvement: +25 points
```

**Time:** <10 seconds

### Example 4: CI/CD Integration

**User says:**
> "validate docs for CI/CD pipeline"

**Execute:**
```bash
/check-docs --json
```

**Output (JSON):**
```json
{
  "timestamp": "2026-03-15T10:30:00Z",
  "profile": "tauri",
  "score": 100,
  "max_score": 100,
  "status": "perfect",
  "breakdown": {
    "directories": {"score": 30, "max": 30, "issues": []},
    "files": {"score": 40, "max": 40, "issues": []},
    "naming": {"score": 15, "max": 15, "issues": []},
    "adrs": {"score": 15, "max": 15, "issues": []}
  },
  "issues": [],
  "fixes": []
}
```

**Exit code:** 0 (perfect compliance)

**Time:** <5 seconds

## Integration

**Workflow with /init-docs:**
```
1. /init-docs              # Create documentation structure
2. [Edit documentation]    # Add content
3. /check-docs             # Validate structure
4. /check-docs --fix       # Auto-fix any issues
5. git commit              # Commit documentation
```

**CI/CD pipeline integration:**
```yaml
# .github/workflows/docs-check.yml
name: Documentation Check

on: [push, pull_request]

jobs:
  check-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Validate documentation structure
        run: |
          /check-docs --json
        continue-on-error: true
      - name: Report results
        run: |
          SCORE=$(cat .check-docs-result.json | jq .score)
          if [ $SCORE -lt 70 ]; then
            echo "❌ Documentation score too low: $SCORE/100"
            exit 1
          fi
```

**Cross-skill workflows:**
- `/init-docs` → Creates structure → `/check-docs` validates
- `/check-docs --fix` → Can call `/init-docs --force` for missing files
- `/adr` → Creates ADRs → `/check-docs` validates numbering

## Best Practices

1. **Run after /init-docs** - Validate immediately after structure creation
2. **Use --verbose for debugging** - See detailed file-by-file checks
3. **Fix incrementally** - Address highest-scoring issues first
4. **Integrate in CI/CD** - Enforce standards automatically
5. **Run before releases** - Ensure documentation complete
6. **Use --fix cautiously** - Review changes before committing

## Compliance Levels

**100/100 - Perfect ✅**
- All directories exist
- All files present
- All naming conventions followed
- ADRs numbered sequentially
- Ready for production

**70-99 - Good ⚠️**
- Minor issues (1-2 missing files)
- Small naming violations
- ADR index missing
- Can proceed with notes

**40-69 - Needs Work 🔧**
- Multiple missing files
- Several naming violations
- ADR numbering gaps
- Fix before merging

**0-39 - Critical ❌**
- Core structure missing
- Most files absent
- Requires /init-docs or major rework

## Task Management

When executing via AI orchestration, track progress:

```
- [ ] Profile detected
- [ ] Requirements loaded
- [ ] Directory validation complete
- [ ] File validation complete
- [ ] Naming validation complete
- [ ] ADR validation complete
- [ ] Score calculated
- [ ] Fixes generated
- [ ] Report outputted
```

## Final Verification

**Critical checks before completion:**

```
- [ ] All 4 validation dimensions executed
- [ ] Score calculated (0-100)
- [ ] Fix suggestions provided
- [ ] Appropriate exit code returned
- [ ] Report formatted correctly
```

## Related Skills

- **/init-docs** - Creates documentation structure (counterpart to this skill)
- **/adr** - Manages Architecture Decision Records
- **/configure-permissions** - Sets up automation permissions

---

**Version:** 1.0.0
**Last Updated:** 2026-03-15
**Changelog:**
- v1.0.0 (2026-03-15): Initial release - documentation structure validation skill

**Pattern:** Validation Skill (checks compliance, provides fixes)
**Compliance:** ADR-001 ✅
