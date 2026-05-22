---
name: anti-slop-toolkit
description: >
  Automated detection and cleanup tools for AI slop patterns. Provides Python
  and R scripts for active slop detection, scoring, and cleanup across codebases.
  Use when you need automated quality enforcement.
applies_to:
  - "**/*.py"
  - "**/*.R"
  - "**/*.md"
  - "**/*.txt"
tags: [automation, quality-assurance, ci-cd, linting, code-review]
related_skills:
  - r/anti-slop
  - python/anti-slop
  - text/anti-slop
  - anti-slop
version: 2.0.0
---

# Anti-Slop Toolkit

## When to Use This Skill

Use anti-slop-toolkit when:
- ✓ Running automated slop detection across a codebase
- ✓ Integrating slop checks into CI/CD pipelines
- ✓ Setting up pre-commit hooks for quality enforcement
- ✓ Auditing large projects for generic AI patterns
- ✓ Batch processing multiple files for cleanup
- ✓ Establishing quantitative quality thresholds

Do NOT use when:
- Manual review is more appropriate (use domain-specific anti-slop skills)
- Dealing with non-text files (images, binaries)
- Working with languages not covered by scripts (use manual skills)

## Quick Example

**Running Detection**:
```bash
# Text file detection
$ python3 scripts/detect_slop.py report.md --verbose

Analyzing: report.md
Overall Slop Score: 45/100

High-Risk Phrases (3 found):
  Line 12: "delve into the complexities"
  Line 34: "in today's fast-paced world"
  Line 67: "it's important to note that"

Recommendations:
- Remove meta-commentary
- Simplify wordy phrases
- Replace buzzwords with direct language

# R code detection
$ Rscript scripts/detect_slop.R analysis.R --verbose

Analyzing: analysis.R
Overall Slop Score: 52/100

Generic Variables (5 found):
  Line 8: df
  Line 15: data
  Line 23: result

Recommendations:
- Replace generic variable names
- Add namespace qualification
- Remove obvious comments
```

**Running Cleanup**:
```bash
# Preview changes
$ python3 scripts/clean_slop.py report.md

Would remove:
  Line 12: "delve into the complexities" → "examine"
  Line 34: "in today's fast-paced world" → [deleted]

# Apply changes (creates backup)
$ python3 scripts/clean_slop.py report.md --save

Backup created: report.md.backup
Cleaned: report.md
Removed 15 slop patterns
```

## When to Use What

| If you need to... | Use this tool | Options |
|-------------------|---------------|---------|
| Detect text slop | `detect_slop.py <file>` | `--verbose` for details |
| Clean text slop | `clean_slop.py <file> --save` | `--aggressive` for more changes |
| Detect R code slop | `detect_slop.R <file>` | Works on files or directories |
| Audit entire codebase | workflow-1-audit-codebase | Batch processing |
| Set up CI/CD checks | workflow-2-ci-cd-integration | Exit codes for pass/fail |
| Create pre-commit hook | workflow-3-pre-commit-hook | Automatic enforcement |

## Core Workflow

### 3-Step Automated Quality Check

1. **Run detection to assess scope**
   ```bash
   # Single file
   python3 scripts/detect_slop.py document.md --verbose

   # Multiple files
   find . -name "*.md" -exec python3 scripts/detect_slop.py {} \;
   ```

2. **Review findings and set thresholds**
   ```bash
   # Acceptable: score < 30
   # Needs work: score 30-50
   # Must fix: score > 50
   ```

3. **Apply automated cleanup where safe**
   ```bash
   # Conservative cleanup (preserves meaning)
   python3 scripts/clean_slop.py document.md --save

   # Aggressive cleanup (may change nuance)
   python3 scripts/clean_slop.py document.md --save --aggressive
   ```

## Quick Reference Checklist

For CI/CD integration:

- [ ] Scripts installed in project (copy from toolkit/scripts/)
- [ ] Detection thresholds defined (e.g., fail if score > 40)
- [ ] File types to check specified
- [ ] Exceptions documented (files that can't be cleaned)
- [ ] Backup strategy for cleanup operations
- [ ] Exit codes configured for pipeline failures

For manual use:

- [ ] Run detection first (never blind cleanup)
- [ ] Review verbose output for context
- [ ] Test cleanup on copy before applying
- [ ] Verify cleaned output maintains meaning
- [ ] Commit cleaned files separately for easy review

## Common Workflows

### Workflow 1: Audit Entire Codebase

**Context**: Review project for generic AI patterns before release.

**Steps**:

1. **Run comprehensive detection**
   ```bash
   #!/bin/bash
   # audit_slop.sh

   echo "=== Text Files ==="
   find . -name "*.md" -o -name "*.txt" | while read file; do
     score=$(python3 scripts/detect_slop.py "$file" | grep "Score:" | awk '{print $3}')
     echo "$file: $score"
   done

   echo ""
   echo "=== R Files ==="
   find . -name "*.R" | while read file; do
     score=$(Rscript scripts/detect_slop.R "$file" | grep "Score:" | awk '{print $3}')
     echo "$file: $score"
   done
   ```

2. **Generate summary report**
   ```bash
   # Count files by severity
   echo "Files by severity:"
   echo "Low (0-20): $(grep -c "1[0-9]/100\|[0-9]/100" audit.log)"
   echo "Moderate (20-40): $(grep -c "[23][0-9]/100" audit.log)"
   echo "High (40-60): $(grep -c "[45][0-9]/100" audit.log)"
   echo "Severe (60+): $(grep -c "6[0-9]/100\|7[0-9]/100\|8[0-9]/100\|9[0-9]/100" audit.log)"
   ```

3. **Prioritize high-severity files**
   ```bash
   # List files with score > 50
   grep -E "[5-9][0-9]/100" audit.log | sort -t: -k2 -rn > high_priority.txt
   ```

4. **Apply cleanup to high-priority files**
   ```bash
   # Clean files with score > 50
   while read line; do
     file=$(echo $line | cut -d: -f1)
     python3 scripts/clean_slop.py "$file" --save
   done < high_priority.txt
   ```

5. **Verify improvements**
   ```bash
   # Re-run detection on cleaned files
   while read line; do
     file=$(echo $line | cut -d: -f1)
     python3 scripts/detect_slop.py "$file"
   done < high_priority.txt
   ```

**Expected outcome**: Prioritized cleanup plan with before/after scores

---

### Workflow 2: CI/CD Pipeline Integration

**Context**: Enforce quality standards in continuous integration.

**Steps**:

1. **Create detection script for CI**
   ```bash
   #!/bin/bash
   # ci_check_slop.sh

   THRESHOLD=40
   FAILED=0

   # Check markdown files
   for file in $(find . -name "*.md"); do
     score=$(python3 scripts/detect_slop.py "$file" | grep -oP "Score: \K\d+")
     if [ "$score" -gt "$THRESHOLD" ]; then
       echo "FAIL: $file (score: $score, threshold: $THRESHOLD)"
       FAILED=1
     else
       echo "PASS: $file (score: $score)"
     fi
   done

   # Check R files
   for file in $(find . -name "*.R"); do
     score=$(Rscript scripts/detect_slop.R "$file" | grep -oP "Score: \K\d+")
     if [ "$score" -gt "$THRESHOLD" ]; then
       echo "FAIL: $file (score: $score, threshold: $THRESHOLD)"
       FAILED=1
     fi
   done

   exit $FAILED
   ```

2. **Add to GitHub Actions**
   ```yaml
   # .github/workflows/quality-check.yml
   name: Quality Check

   on: [pull_request]

   jobs:
     anti-slop:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3
         - name: Set up Python
           uses: actions/setup-python@v4
           with:
             python-version: '3.x'
         - name: Set up R
           uses: r-lib/actions/setup-r@v2
         - name: Check for slop
           run: |
             chmod +x ci_check_slop.sh
             ./ci_check_slop.sh
   ```

3. **Configure for GitLab CI**
   ```yaml
   # .gitlab-ci.yml
   quality_check:
     stage: test
     image: rocker/r-ver:latest
     before_script:
       - apt-get update && apt-get install -y python3
     script:
       - chmod +x ci_check_slop.sh
       - ./ci_check_slop.sh
     allow_failure: false
   ```

4. **Add quality gate**
   ```bash
   # Only fail on severe slop (score > 60)
   THRESHOLD=60
   # Warn on moderate slop (score 40-60) but don't fail
   WARN_THRESHOLD=40
   ```

5. **Generate CI report**
   ```bash
   # Add to CI script
   if [ "$score" -gt "$THRESHOLD" ]; then
     echo "::error file=$file::Slop score $score exceeds threshold $THRESHOLD"
   elif [ "$score" -gt "$WARN_THRESHOLD" ]; then
     echo "::warning file=$file::Slop score $score exceeds warning threshold"
   fi
   ```

**Expected outcome**: Automated quality enforcement in pull requests

---

### Workflow 3: Pre-commit Hook Setup

**Context**: Prevent slop from entering repository with pre-commit hooks.

**Steps**:

1. **Create pre-commit hook**
   ```bash
   #!/bin/bash
   # .git/hooks/pre-commit

   # Get staged files
   STAGED_MD=$(git diff --cached --name-only --diff-filter=ACM | grep "\.md$")
   STAGED_R=$(git diff --cached --name-only --diff-filter=ACM | grep "\.R$")

   THRESHOLD=50
   ISSUES=0

   # Check markdown files
   for file in $STAGED_MD; do
     if [ -f "$file" ]; then
       score=$(python3 scripts/detect_slop.py "$file" | grep -oP "Score: \K\d+")
       if [ "$score" -gt "$THRESHOLD" ]; then
         echo "ERROR: $file has slop score $score (threshold: $THRESHOLD)"
         ISSUES=1
       fi
     fi
   done

   # Check R files
   for file in $STAGED_R; do
     if [ -f "$file" ]; then
       score=$(Rscript scripts/detect_slop.R "$file" | grep -oP "Score: \K\d+")
       if [ "$score" -gt "$THRESHOLD" ]; then
         echo "ERROR: $file has slop score $score (threshold: $THRESHOLD)"
         ISSUES=1
       fi
     fi
   done

   if [ $ISSUES -ne 0 ]; then
     echo ""
     echo "Commit rejected: Files exceed slop threshold"
     echo "Run 'python3 scripts/clean_slop.py <file> --save' to clean"
     echo "Or use 'git commit --no-verify' to bypass (not recommended)"
     exit 1
   fi

   exit 0
   ```

2. **Make hook executable**
   ```bash
   chmod +x .git/hooks/pre-commit
   ```

3. **Test hook**
   ```bash
   # Create test file with slop
   echo "It's important to note that we will delve into..." > test.md
   git add test.md
   git commit -m "Test"
   # Should fail with error message
   ```

4. **Add auto-fix option**
   ```bash
   # Add to hook after detecting issues
   echo ""
   echo "Attempt auto-fix? (y/n)"
   read -r response
   if [ "$response" = "y" ]; then
     for file in $STAGED_MD; do
       python3 scripts/clean_slop.py "$file" --save
       git add "$file"
     done
     echo "Files cleaned and re-staged"
     exit 0
   fi
   ```

5. **Share hook with team**
   ```bash
   # Create shared hooks directory
   mkdir -p .githooks
   cp .git/hooks/pre-commit .githooks/

   # Configure git to use shared hooks
   git config core.hooksPath .githooks

   # Document in README
   echo "Run: git config core.hooksPath .githooks" >> README.md
   ```

**Expected outcome**: Automatic slop prevention before commits

## Script Reference

### detect_slop.py

**Purpose**: Analyze text files for AI slop patterns.

**Usage**:
```bash
python scripts/detect_slop.py <file> [--verbose]
```

**What it detects**:
- High-risk phrases (delve, navigate complexities, fast-paced world)
- Wordy constructions (in order to, due to the fact that)
- Meta-commentary (it's important to note)
- Buzzwords (leverage, synergistic, paradigm)
- Excessive hedging (might possibly, could potentially)

**Output**:
```
Overall Slop Score: 45/100

High-Risk Phrases (3):
  Line 12: "delve into"
  Line 34: "in today's world"

Recommendations:
- Remove meta-commentary
- Simplify wordy phrases
```

**Scoring**:
- 0-20: Low slop (authentic)
- 20-40: Moderate slop (some patterns)
- 40-60: High slop (many patterns)
- 60+: Severe slop (heavily generic)

---

### clean_slop.py

**Purpose**: Automatically remove common slop patterns from text.

**Usage**:
```bash
# Preview changes
python scripts/clean_slop.py <file>

# Apply changes (creates backup)
python scripts/clean_slop.py <file> --save

# Output to different file
python scripts/clean_slop.py <file> --output cleaned.txt

# Aggressive mode (may change meaning)
python scripts/clean_slop.py <file> --save --aggressive
```

**What it cleans**:
- High-risk phrases → direct alternatives
- Wordy constructions → concise equivalents
- Meta-commentary → deleted
- Buzzwords → plain language
- Redundant qualifiers → removed
- Empty intensifiers → deleted

**Safety**:
- Always creates `.backup` file when using `--save`
- Preview mode shows all changes before applying
- Conservative by default (preserves meaning)
- Aggressive mode removes more but may alter nuance

**Example transformations**:
```
Before: "It's important to note that we will delve into..."
After: "We examine..."

Before: "In order to understand this, due to the fact that..."
After: "To understand this, because..."

Before: "Leverage synergistic paradigms..."
After: "Use cooperative approaches..."
```

---

### detect_slop.R

**Purpose**: Analyze R code files for AI slop patterns.

**Usage**:
```bash
# Single file
Rscript scripts/detect_slop.R <file.R> [--verbose]

# Directory
Rscript scripts/detect_slop.R <directory> [--verbose]

# Package R/ folder
Rscript scripts/detect_slop.R mypackage/R/
```

**What it detects**:
- Generic variable names (df, data, temp, result, res, out)
- Generic function names (process_*, do_*, helper)
- Obvious comments ("Load the library", "Filter the data")
- Unnecessary single pipes (`x %>% f()` instead of `f(x)`)
- Overly long pipe chains (>8 operations)
- Generic roxygen documentation (@param data The data)

**Output**:
```
Analyzing: analysis.R
Overall Slop Score: 52/100

Generic Variables (5):
  Line 8: df
  Line 15: data
  Line 23: result

Generic Function Names (2):
  Line 45: process_data()
  Line 78: helper()

Obvious Comments (4):
  Line 5: "# Load the library"
  Line 12: "# Filter the data"

Recommendations:
- Replace generic variable names with descriptive ones
- Add namespace qualification (use ::)
- Remove obvious comments
- Simplify single-pipe constructs
```

**Scoring**:
- 0-20: Low slop (thoughtful R code)
- 20-40: Moderate slop (some generic patterns)
- 40-60: High slop (many AI patterns)
- 60+: Severe slop (heavily generic code)

## Best Practices

### When to Use Automation

**Good use cases**:
- Large codebases with many files
- Consistent pattern enforcement across team
- Pre-release quality audits
- Continuous integration checks
- Batch cleanup of known patterns

**Poor use cases**:
- Nuanced writing requiring context
- Academic papers with domain conventions
- Code with intentional generic names (e.g., `data` in function examples)
- First-time quality review (start manual)

### Setting Thresholds

**Conservative thresholds** (strict standards):
- Fail: score > 30
- Warn: score > 20
- Good for: Public releases, documentation, client deliverables

**Moderate thresholds** (balanced):
- Fail: score > 50
- Warn: score > 30
- Good for: Internal code, team projects, iterative work

**Lenient thresholds** (pragmatic):
- Fail: score > 70
- Warn: score > 50
- Good for: Exploratory work, drafts, legacy code

### Cleanup Strategy

**Always**:
1. Run detection first (understand scope)
2. Preview cleanup changes (review transformations)
3. Create backups (use `--save` for automatic backup)
4. Test output (verify meaning preserved)
5. Commit separately (easy to review/revert)

**Never**:
- Blind batch cleanup without review
- Aggressive mode on important documents
- Skip manual verification of automated changes
- Apply to files with domain-specific conventions

## Integration Patterns

### With Git Workflow

```bash
# Before committing
git diff --name-only | grep "\.md$" | while read file; do
  python scripts/detect_slop.py "$file"
done

# Clean before commit
python scripts/clean_slop.py changed_file.md --save
git add changed_file.md
git commit -m "Clean slop from documentation"
```

### With Make/Build System

```makefile
# Makefile
.PHONY: check-slop clean-slop

check-slop:
	@find . -name "*.md" | while read f; do \
		python scripts/detect_slop.py "$$f"; \
	done

clean-slop:
	@find . -name "*.md" | while read f; do \
		python scripts/clean_slop.py "$$f" --save; \
	done

# Usage: make check-slop
```

### With R Package Development

```r
# R/zzz.R
check_slop <- function(path = "R/") {
  r_files <- list.files(path, pattern = "\\.R$", full.names = TRUE)
  lapply(r_files, function(f) {
    system(paste("Rscript scripts/detect_slop.R", f))
  })
}

# Usage: check_slop()
```

## Limitations

### Script Coverage

**detect_slop.py**:
- Text files only (.md, .txt)
- English language optimized
- Can't understand all contexts
- May flag acceptable domain conventions

**detect_slop.R**:
- R code files only (.R)
- Doesn't detect all R-specific patterns
- May flag intentional generic names in examples
- Doesn't check roxygen completeness (just generic patterns)

**clean_slop.py**:
- Text files only
- May alter meaning in aggressive mode
- Can't handle all edge cases
- Requires manual review

### Manual Skills for Other Cases

- **Python code**: Use python/anti-slop skill (manual)
- **Design/visualization**: Use design/anti-slop skill (manual)
- **Julia/C++ code**: Use julia/anti-slop or cpp/anti-slop (manual)
- **Complex documentation**: Use text/anti-slop skill (manual)

### Context Sensitivity

Scripts can't understand:
- Domain-specific conventions
- Acceptable generic names in specific contexts
- Intentional stylistic choices
- Academic writing requirements
- Legal/regulatory language needs

**Always combine automated detection with manual review.**

## Troubleshooting

### Script Not Found

```bash
# Ensure scripts directory exists
ls toolkit/scripts/

# Should see:
# detect_slop.py
# clean_slop.py
# detect_slop.R
```

### Python Dependencies

```bash
# Scripts use only standard library
# No dependencies needed
python3 scripts/detect_slop.py --help
```

### R Script Fails

```bash
# Ensure R is installed
which Rscript

# Scripts use only base R
# No packages needed
Rscript scripts/detect_slop.R --help
```

### Permissions

```bash
# Make scripts executable
chmod +x scripts/*.py
chmod +x scripts/*.R
```

### High False Positive Rate

- Adjust thresholds (increase threshold values)
- Use manual review for edge cases
- Whitelist specific files in CI scripts
- Document acceptable exceptions

## Resources & Advanced Topics

### Script Locations

All scripts in `toolkit/scripts/`:
- `detect_slop.py` - Text detection
- `clean_slop.py` - Text cleanup
- `detect_slop.R` - R code detection

### Related Skills

- **r/anti-slop** - Manual R code review
- **python/anti-slop** - Manual Python code review
- **text/anti-slop** - Manual text review
- **anti-slop** - Meta-skill coordinator

### Extending the Toolkit

**Add new pattern detection**:
```python
# In detect_slop.py
new_patterns = [
    "your custom pattern",
    "another pattern"
]
```

**Add new cleanup rules**:
```python
# In clean_slop.py
cleanup_rules = [
    ("old phrase", "replacement"),
    ("another old", "another new")
]
```

**Create language-specific detector**:
```bash
# Model on detect_slop.R structure
# Define patterns for your language
# Score based on pattern frequency
```

## Integration with Domain Skills

This toolkit provides **automated detection and cleanup**.

Use together with domain skills for complete coverage:

| Task | Use Toolkit | + Domain Skill |
|------|-------------|----------------|
| Audit codebase | detect_slop.py/R | + manual review with domain skill |
| Clean text files | clean_slop.py | + text/anti-slop for review |
| Check R code | detect_slop.R | + r/anti-slop for refactoring |
| CI/CD integration | All scripts | + domain skills for exceptions |

**Key distinction**:
- **Toolkit** provides automated detection/cleanup
- **Domain skills** provide context and manual refinement

Both are complementary equals for maintaining quality standards.
