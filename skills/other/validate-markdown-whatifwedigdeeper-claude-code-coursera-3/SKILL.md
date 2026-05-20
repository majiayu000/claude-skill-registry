---
skill: validate-markdown
description: Validate and fix markdown formatting issues: $ARGUMENTS (file path or '.' for all)
location: project
---

# Validate Markdown: $ARGUMENTS

I'll validate markdown files for common formatting issues and optionally fix them.

This will include:
1. Checking for duplicate code block markers
2. Detecting unclosed code blocks
3. Identifying common markdown issues
4. Optionally fixing issues automatically
5. Generating a validation report

Let's begin!

---

## Process Steps

### 1. Determine Scope

Identify which files to validate based on arguments:

```bash
if [ "$ARGUMENTS" = "." ] || [ "$ARGUMENTS" = "all" ]; then
  # Validate all markdown files in repository
  FILES=$(find . -name "*.md" -not -path "*/node_modules/*" -not -path "*/.git/*" -not -path "*/plans/*")
  echo "📊 Validating all markdown files in repository"
elif [ -f "$ARGUMENTS" ]; then
  # Validate specific file
  FILES="$ARGUMENTS"
  echo "📝 Validating: $ARGUMENTS"
elif [ -d "$ARGUMENTS" ]; then
  # Validate all markdown in directory
  FILES=$(find "$ARGUMENTS" -name "*.md")
  echo "📁 Validating markdown files in: $ARGUMENTS"
else
  echo "❌ Error: File or directory not found: $ARGUMENTS"
  exit 1
fi

FILE_COUNT=$(echo "$FILES" | wc -l | tr -d ' ')
echo "Found $FILE_COUNT file(s) to validate"
echo ""
```

### 2. Check for Duplicate Code Block Markers

The most common markdown issue - consecutive ` ``` ` markers:

```bash
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔍 Checking for duplicate code blocks..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

TOTAL_DUPLICATES=0
FILES_WITH_DUPLICATES=0

for file in $FILES; do
  # Find consecutive ``` markers
  DUPLICATES=$(awk '/^```$/{if(prev=="```")print NR-1 "-" NR; prev="```"; next} {prev=$0}' "$file")

  if [ ! -z "$DUPLICATES" ]; then
    echo "❌ $file"
    echo "$DUPLICATES" | while read line; do
      DUPLICATE_COUNT=$(echo "$DUPLICATES" | wc -l | tr -d ' ')
      echo "   Lines: $line"
    done
    echo ""

    ((FILES_WITH_DUPLICATES++))
    DUPLICATE_COUNT=$(echo "$DUPLICATES" | wc -l | tr -d ' ')
    TOTAL_DUPLICATES=$((TOTAL_DUPLICATES + DUPLICATE_COUNT))
  fi
done

if [ $FILES_WITH_DUPLICATES -eq 0 ]; then
  echo "✅ No duplicate code blocks found"
else
  echo "⚠️  Found duplicates in $FILES_WITH_DUPLICATES file(s)"
fi
echo ""
```

### 3. Check for Unclosed Code Blocks

Detect odd number of ` ``` ` markers (unclosed blocks):

```bash
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔍 Checking for unclosed code blocks..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

FILES_WITH_UNCLOSED=0

for file in $FILES; do
  CODE_BLOCK_COUNT=$(grep -c '^```' "$file" 2>/dev/null || echo 0)

  if [ $((CODE_BLOCK_COUNT % 2)) -ne 0 ]; then
    echo "❌ $file"
    echo "   Total ``` markers: $CODE_BLOCK_COUNT (should be even)"
    echo ""
    ((FILES_WITH_UNCLOSED++))
  fi
done

if [ $FILES_WITH_UNCLOSED -eq 0 ]; then
  echo "✅ All code blocks properly closed"
else
  echo "⚠️  Found unclosed blocks in $FILES_WITH_UNCLOSED file(s)"
fi
echo ""
```

### 4. Check for Common Issues

Additional markdown issues to detect:

```bash
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔍 Checking for other common issues..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

OTHER_ISSUES=0

for file in $FILES; do
  FILE_ISSUES=()

  # Check for tabs in YAML front matter
  if grep -q $'^---\n.*\t' "$file"; then
    FILE_ISSUES+=("YAML front matter contains tabs (use spaces)")
  fi

  # Check for very long lines (>500 chars) which may be unintentional
  LONG_LINES=$(awk 'length > 500 {print NR}' "$file" | head -5)
  if [ ! -z "$LONG_LINES" ]; then
    FILE_ISSUES+=("Very long lines found: $(echo $LONG_LINES | tr '\n' ',')")
  fi

  # Check for trailing spaces
  if grep -q ' $' "$file"; then
    TRAILING_COUNT=$(grep -c ' $' "$file")
    FILE_ISSUES+=("$TRAILING_COUNT lines with trailing spaces")
  fi

  # Report issues for this file
  if [ ${#FILE_ISSUES[@]} -gt 0 ]; then
    echo "⚠️  $file"
    for issue in "${FILE_ISSUES[@]}"; do
      echo "   - $issue"
    done
    echo ""
    ((OTHER_ISSUES++))
  fi
done

if [ $OTHER_ISSUES -eq 0 ]; then
  echo "✅ No other issues found"
fi
echo ""
```

### 5. Generate Summary Report

Create comprehensive validation summary:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 VALIDATION SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Files checked: $FILE_COUNT

Issues found:
  🔴 Duplicate code blocks: $FILES_WITH_DUPLICATES files
  🔴 Unclosed code blocks: $FILES_WITH_UNCLOSED files
  🟡 Other issues: $OTHER_ISSUES files

Total files with issues: $(($FILES_WITH_DUPLICATES + $FILES_WITH_UNCLOSED + $OTHER_ISSUES))
```

### 6. Offer to Fix Issues

If issues found, offer automatic fixing:

```bash
TOTAL_ISSUES=$(($FILES_WITH_DUPLICATES + $FILES_WITH_UNCLOSED + $OTHER_ISSUES))

if [ $TOTAL_ISSUES -gt 0 ]; then
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "🔧 FIX OPTIONS"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo ""
  echo "Would you like to automatically fix these issues? (yes/no)"
  echo ""
  echo "What will be fixed:"
  echo "  ✓ Remove duplicate code block markers"
  echo "  ✓ Remove trailing whitespace"
  echo "  ⚠️  Unclosed blocks require manual review"
  echo ""

  # Wait for user response
else
  echo ""
  echo "✅ All markdown files are valid!"
  echo ""
  echo "No issues found. All files pass validation."
fi
```

### 7. Apply Fixes (If Approved)

Automatically fix issues that are safe to auto-correct:

```bash
if [ "$USER_RESPONSE" = "yes" ]; then
  echo "🔧 Applying fixes..."
  echo ""

  FIXED_COUNT=0

  for file in $FILES; do
    FIXED_THIS_FILE=false

    # Fix 1: Remove duplicate code block markers
    DUPLICATES=$(awk '/^```$/{if(prev=="```")print NR-1 "-" NR; prev="```"; next} {prev=$0}' "$file")
    if [ ! -z "$DUPLICATES" ]; then
      # Remove consecutive duplicate ``` markers
      awk 'BEGIN{prev=""} {if($0=="```" && prev=="```"){prev=""; next} print; prev=$0}' "$file" > "$file.tmp"
      mv "$file.tmp" "$file"
      echo "  ✓ Fixed duplicate code blocks in: $file"
      FIXED_THIS_FILE=true
    fi

    # Fix 2: Remove trailing whitespace
    if grep -q ' $' "$file"; then
      sed -i '' 's/[[:space:]]*$//' "$file"
      echo "  ✓ Removed trailing spaces in: $file"
      FIXED_THIS_FILE=true
    fi

    if [ "$FIXED_THIS_FILE" = true ]; then
      ((FIXED_COUNT++))
    fi
  done

  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "✅ Applied fixes to $FIXED_COUNT file(s)"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo ""

  if [ $FILES_WITH_UNCLOSED -gt 0 ]; then
    echo "⚠️  Manual Review Required:"
    echo ""
    echo "The following files have unclosed code blocks"
    echo "and need manual inspection:"
    echo ""
    # List files with unclosed blocks
    echo "Use VSCode preview (Cmd+Shift+V) to identify issues"
  fi
else
  echo "Skipping automatic fixes."
  echo ""
  echo "To fix manually, see: CLAUDE.md ## Markdown Documentation Guidelines"
fi
```

### 8. Provide Remediation Guidance

If issues remain, provide specific fix instructions:

```markdown
## How to Fix Common Issues

### Duplicate Code Block Markers

**Problem:** Consecutive ` ``` ` on adjacent lines

```markdown
# Wrong
echo "test"
```
```

Some text
```

**Fix:** Remove the duplicate marker

```markdown
# Correct
echo "test"
```

Some text
```

### Unclosed Code Blocks

**Problem:** Odd number of ` ``` ` markers

**Fix:** Use VSCode preview (Cmd+Shift+V) to locate where highlighting breaks, then add missing closing marker

### Nested Code Blocks

**Problem:** Showing code blocks within markdown examples

**Fix:** Use 4 backticks for outer block

````markdown
Example:

```bash
echo "test"
```
````

## Validation Script

Alternative: Run the standalone validation script:

```bash
bash .claude/scripts/validate-markdown.sh
```
```

---

## Example Usage

### Validate All Files

```bash
validate-markdown .
```

**Expected output:**
```
📊 Validating all markdown files in repository
Found 15 file(s) to validate

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 Checking for duplicate code blocks...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❌ skills.md
   Lines: 258-259
   Lines: 387-388

⚠️  Found duplicates in 1 file(s)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 VALIDATION SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Files checked: 15
Issues found:
  🔴 Duplicate code blocks: 1 files
  🔴 Unclosed code blocks: 0 files
  🟡 Other issues: 0 files
```

### Validate Specific File

```bash
validate-markdown skills.md
```

### Validate Directory

```bash
validate-markdown .claude/skills/
```

---

## Integration Options

### Pre-commit Hook

Add to `.git/hooks/pre-commit`:

```bash
#!/bin/bash

# Validate markdown files before commit
echo "Validating markdown files..."

# Get staged .md files
STAGED_MD=$(git diff --cached --name-only --diff-filter=ACM | grep '\.md$')

if [ ! -z "$STAGED_MD" ]; then
  for file in $STAGED_MD; do
    # Check for duplicate code blocks
    DUPLICATES=$(awk '/^```$/{if(prev=="```")print NR-1 "-" NR; prev="```"; next} {prev=$0}' "$file")

    if [ ! -z "$DUPLICATES" ]; then
      echo "❌ Markdown validation failed: $file"
      echo "   Found duplicate code blocks at lines: $DUPLICATES"
      echo ""
      echo "Run: validate-markdown $file"
      exit 1
    fi
  done
fi

echo "✅ Markdown validation passed"
```

### GitHub Actions

Add to `.github/workflows/validate-markdown.yml`:

```yaml
name: Validate Markdown

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Validate markdown files
        run: bash .claude/scripts/validate-markdown.sh
```

---

## Related Documentation

- **Markdown Guidelines:** [CLAUDE.md § Markdown Documentation Guidelines](../../CLAUDE.md#markdown-documentation-guidelines)
- **Validation Script:** [.claude/scripts/validate-markdown.sh](../scripts/validate-markdown.sh)
- **Skills Guide:** [skills.md](../../skills.md)
