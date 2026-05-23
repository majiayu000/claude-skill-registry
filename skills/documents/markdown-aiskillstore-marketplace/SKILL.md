---
name: markdown
description: >
  Markdown linting and automated fixing using markdownlint-cli2. Use when Claude needs to: (1) Check markdown files for style issues, (2) Fix markdown formatting problems, (3) Ensure markdown follows best practices, (4) Validate markdown documents, or (5) Apply consistent markdown styling
---

# Markdown Lint

Automated markdown validation and fixing using markdownlint-cli2.

## Workflow Overview

```text
1. Run auto-fix     → markdownlint-cli2 --fix <file>
2. Check remaining  → markdownlint-cli2 <file>
3. Fix manually     → str_replace for structural issues
4. Verify           → markdownlint-cli2 <file> (should show 0 errors)
```

**Expected results**: Auto-fix resolves 70-90% of issues. Remaining 3-5
issues require manual correction.

## Basic Commands

```bash
# Auto-fix single file
markdownlint-cli2 --fix document.md

# Check file
markdownlint-cli2 document.md

# Multiple files
markdownlint-cli2 --fix file1.md file2.md

# All markdown in directory
markdownlint-cli2 --fix "**/*.md"

# With custom config
markdownlint-cli2 --config .markdownlint.json document.md
```

## File Paths

```bash
# Uploaded files
markdownlint-cli2 --fix /mnt/user-data/uploads/document.md

# Working directory
markdownlint-cli2 --fix /home/claude/document.md

# Output to user
cp /path/to/fixed.md /mnt/user-data/outputs/
```

## Manual Fixes Required

Auto-fix cannot resolve these issues - they need Claude's judgment:

### MD025 - Multiple H1 Headers

**Why**: Requires understanding document hierarchy  
**Fix**: Convert extra H1s to appropriate level

```markdown
# Main Title

# Second Title → Change to: ## Second Title
```

### MD036 - Emphasis as Header

**Why**: Requires determining author intent  
**Fix**: Replace bold/italic with proper header

```markdown
**Section Title** → Change to: ## Section Title
```

### MD013 - Line Too Long

**Why**: Requires deciding where to break content  
**Fix**: Wrap at natural points (spaces, punctuation)

```markdown
This is a very long line exceeding 80 characters that needs wrapping.
↓
This is a very long line exceeding 80 characters that needs
wrapping.
```

**Exception**: URLs typically exempt

### MD041 - Missing First Line Header

**Why**: Requires structural decision  
**Fix**: Add H1 at start or restructure

## Execution Pattern

### For Uploaded Files

```bash
# 1. Auto-fix
markdownlint-cli2 --fix /mnt/user-data/uploads/document.md

# 2. Check remaining
markdownlint-cli2 /mnt/user-data/uploads/document.md
# Output: "Summary: 3 error(s)"
# Lists specific errors like "MD025/single-title Multiple top-level headings"

# 3. Manual fixes (example)
str_replace "# Extra Title" → "## Extra Title"

# 4. Verify
markdownlint-cli2 /mnt/user-data/uploads/document.md
# Output: "Summary: 0 error(s)"

# 5. Output
cp /mnt/user-data/uploads/document.md /mnt/user-data/outputs/
```

### For New Content

```bash
create_file /home/claude/doc.md "content..."
markdownlint-cli2 --fix /home/claude/doc.md
markdownlint-cli2 /home/claude/doc.md
# Fix remaining issues if any
cp /home/claude/doc.md /mnt/user-data/outputs/
```

## Configuration

Create `.markdownlint.json` to customize rules:

```json
{
  "default": true,
  "MD013": { "line_length": 120 },
  "MD033": false
}
```

**Common adjustments**:

- `"MD013": false` - Disable line length checking
- `"MD013": { "line_length": 120 }` - Increase limit to 120
- `"MD013": { "code_blocks": false }` - Exclude code blocks
- `"MD033": false` - Allow HTML
- `"MD041": false` - Don't require first line header

**Config file search order**:

1. `.markdownlint-cli2.jsonc`
2. `.markdownlint-cli2.yaml`
3. `.markdownlint.jsonc` / `.markdownlint.json`
4. `.markdownlint.yaml` / `.markdownlint.yml`

## Reporting to User

Provide clear summary of fixes:

```text
✅ Markdown linting complete!

Initial: 18 errors
After auto-fix: 4 errors
Manual fixes:
  • MD025: Converted 2 H1 headers to H2
  • MD036: Replaced bold with proper header
  • MD013: Wrapped long line

Final: 0 errors
```

## Error Count Interpretation

**Before auto-fix**:

- 0-5: Minor issues
- 6-15: Moderate issues
- 16+: Significant issues

**After auto-fix**:

- 0-2: Excellent
- 3-5: Typical
- 6+: Check if config needed

## Common Fix Patterns

```bash
# Multiple H1s - analyze structure first
# If sections: convert to H2
str_replace "# Introduction" → "## Introduction"

# If subsections: convert to H3
str_replace "# Details" → "### Details"

# Emphasis as headers - determine appropriate level
str_replace "**Important**" → "## Important"
str_replace "_Note_" → "### Note"

# Long lines - break at natural points
# After conjunctions: and, but, or
# After punctuation: , . ;
# Preserve URLs on single line
```

## Troubleshooting

**Auto-fix not working**:

```bash
# Check file exists
view /path/to/file.md

# Verify permissions
ls -l /path/to/file.md

# Use absolute path
markdownlint-cli2 --fix /full/path/to/file.md
```

**Too many errors after auto-fix**:

```bash
# Create relaxed config
echo '{"MD013": false, "MD041": false}' > .markdownlint.json
markdownlint-cli2 --config .markdownlint.json --fix file.md
```

**Specific rule causing issues**:

- Disable in config: `"MD013": false`
- Or adjust parameters: `"MD013": { "line_length": 120 }`

## When NOT to Lint

Skip linting when:

- Code examples intentionally violate rules
- Embedded HTML/JSX required (disable MD033)
- Generated docs with different conventions
- Legacy docs where changes break references

Use custom config to disable problematic rules.

## Quick Rule Reference

Most common rules Claude will encounter:

- **MD001** - Header increment by one level
- **MD004** - Consistent list markers
- **MD009** - No trailing spaces
- **MD010** - No hard tabs
- **MD012** - No multiple blank lines
- **MD013** - Line length (default: 80)
- **MD018** - Space after # in headers
- **MD022** - Blank lines around headers
- **MD025** - Single H1 only
- **MD031** - Blank lines around code
- **MD032** - Blank lines around lists
- **MD034** - Bare URLs in <>
- **MD036** - No emphasis as headers
- **MD040** - Language for code blocks

Full rule documentation: <https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md>
