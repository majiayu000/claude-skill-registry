---
name: lisp-validator
description: Validate Lisp code (Clojure, Racket, Scheme, Common Lisp) for syntax errors, parenthesis balance, and semantic issues. This skill should be used when validating Lisp code files, checking for syntax errors before execution, or validating LLM-generated Lisp code including incomplete or partial expressions. Provides structured JSON output optimized for automated workflows.
license: AGPL 3.0 - Complete terms in LICENSE
---

# Lisp Validator

## Overview

This skill validates Lisp code across multiple dialects (Clojure, Racket, Scheme, Common Lisp) using dialect-specific tools optimized for LLM workflows. Critical for validating incomplete or partially-generated code during LLM-guided editing, it provides structured error output with precise file:line:col information for targeted fixes.

**Key capabilities:**
- Auto-detects Lisp dialect from file extension and content
- Handles incomplete code via tree-sitter (critical for LLM workflows)
- Provides structured JSON output for machine parsing
- Multi-tool validation for comprehensive error detection
- Installation detection and guidance for missing tools

## When to Use This Skill

Use this skill to:
- Validate Lisp code files before execution or commit
- Check LLM-generated Lisp code for syntax errors
- Validate incomplete or partial expressions during code generation
- Detect unbalanced parentheses and structural issues
- Lint entire projects for style and semantic issues
- Determine which validation tools are available on the system

## Workflow Decision Tree

```
┌─ Code complete? ────┐
│                     │
YES                  NO (incomplete/partial)
│                     │
├─ Detect dialect     └─ Use tree-sitter
│                        (handles incomplete)
├─ Clojure? ──→ clj-kondo + joker
├─ Racket/Scheme? ──→ raco tools
├─ Common Lisp? ──→ SBLint + SBCL
├─ Elisp? ──→ tree-sitter
└─ Unknown? ──→ tree-sitter fallback
```

## Quick Start

### Check Available Tools

Before validating, check which tools are installed:

```bash
python3 scripts/check_tools.py
```

This shows:
- Which validation tools are available
- Tool installation status per dialect
- Installation commands for missing tools
- Recommendations based on detected tools

### Validate Any Lisp File (Auto-Detect)

```bash
# Auto-detects dialect and uses appropriate validator
python3 scripts/validate.py <file-or-directory>

# Examples
python3 scripts/validate.py src/core.clj
python3 scripts/validate.py project/src/
```

**Output:** JSON with findings, severity, file:line:col locations

### Format Options

```bash
# JSON output (default, best for parsing)
python3 scripts/validate.py file.clj --format json

# Human-readable text
python3 scripts/validate.py file.clj --format text

# Summary only
python3 scripts/validate.py file.clj --format summary
```

## Quick Reference

| Task | Command |
|------|---------|
| Check available tools | `python3 scripts/check_tools.py` |
| Auto-detect & validate | `python3 scripts/validate.py src/` |
| Validate incomplete code | `python3 scripts/validate.py file.clj --tree-sitter` |
| Force specific dialect | `python3 scripts/validate.py file.scm --dialect scheme` |
| Clojure-specific | `python3 scripts/validate_clojure.py src/` |
| Racket/Scheme-specific | `python3 scripts/validate_scheme.py src/` |
| Common Lisp-specific | `python3 scripts/validate_common_lisp.py src/` |
| Human-readable output | `python3 scripts/validate.py src/ --format text` |
| JSON output (default) | `python3 scripts/validate.py src/ --format json` |
| Summary only | `python3 scripts/validate.py src/ --format summary` |

**Exit Codes:**
- `0` - No issues found
- `2` - Warnings only (code should run)
- `3` - Errors present (code may not run)

## Examples

### Example 1: Validating During Code Generation

When generating Clojure code incrementally with an LLM:

```bash
# After each edit, validate with tree-sitter (handles incomplete code)
python3 scripts/validate.py partial.clj --tree-sitter --format summary

# Once complete, run comprehensive validation
python3 scripts/validate.py complete.clj --format text
```

**Output** (incomplete code):
```
0 errors, 1 warnings (tree-sitter)
```

**Output** (complete code):
```
Target: complete.clj
Dialect: clojure

No issues found!

Summary: 0 errors, 0 warnings
Tools used: clj-kondo, joker
```

### Example 2: CI/CD Integration

```yaml
# .github/workflows/validate-lisp.yml
name: Validate Lisp Code

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install validation tools
        run: |
          curl -sLO https://raw.githubusercontent.com/borkdude/clj-kondo/master/script/install-clj-kondo
          chmod +x install-clj-kondo && ./install-clj-kondo

      - name: Check available tools
        run: python3 scripts/check_tools.py

      - name: Validate Clojure code
        run: |
          python3 scripts/validate.py src/ --format json > validation-results.json
          cat validation-results.json | jq

      - name: Fail on errors
        run: |
          errors=$(jq '.summary.total_errors' validation-results.json)
          if [ "$errors" -gt 0 ]; then
            echo "❌ Found $errors errors"
            exit 1
          fi
          echo "✅ Validation passed"
```

### Example 3: Progressive Validation Workflow

```bash
# Stage 1: Fast structural check (< 1s)
python3 scripts/validate_tree_sitter.py src/core.clj

# Stage 2: Comprehensive validation (if stage 1 passes)
python3 scripts/validate_clojure.py src/core.clj

# Stage 3: Auto-format (only if validation passes)
if [ $? -eq 0 ]; then
    cljfmt fix src/core.clj
fi
```

### Example 4: Pre-Commit Hook

```bash
# .git/hooks/pre-commit
#!/bin/bash

echo "Validating Lisp files..."

# Get staged .clj files
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep '\.clj$')

if [ -z "$STAGED_FILES" ]; then
    exit 0
fi

# Validate each file
for FILE in $STAGED_FILES; do
    python3 scripts/validate.py "$FILE" --format summary
    if [ $? -eq 3 ]; then
        echo "❌ Validation failed for $FILE"
        echo "Fix errors before committing"
        exit 1
    fi
done

echo "✅ All files validated successfully"
exit 0
```

### Example 5: Handling Validation Errors in Scripts

```python
import subprocess
import json

def validate_and_report(file_path):
    """Validate a file and provide structured feedback."""
    result = subprocess.run(
        ["python3", "scripts/validate.py", file_path, "--format", "json"],
        capture_output=True,
        text=True
    )

    data = json.loads(result.stdout)

    if data["summary"]["total_errors"] > 0:
        print(f"⚠️  Found {data['summary']['total_errors']} errors in {file_path}:")
        for finding in data["findings"]:
            if finding["severity"] == "error":
                location = f"{finding['file']}:{finding['line']}:{finding['col']}"
                print(f"  {location}: {finding['message']}")
        return False

    print(f"✅ {file_path} validated successfully")
    return True

# Use it
if not validate_and_report("src/main.clj"):
    exit(1)
```

### Example 6: Checking Tool Installation

```bash
# Check which tools are available
python3 scripts/check_tools.py

# Install missing high-priority tools
python3 scripts/check_tools.py --json | \
    jq -r '.tools | to_entries[] | select(.value.available == false and .value.priority == "high") | .key'
```

**Output:**
```
=== Lisp Validation Tools Status ===

CLOJURE:
  [✓] clj-kondo (2024.03.13)
      Primary Clojure validator with JSON output
  [✗] joker
      Secondary Clojure validator with complementary checks

UNIVERSAL:
  [✓] tree-sitter-python (installed)
      Tree-sitter Python library (more reliable than CLI)
  [✗] tree-sitter
      Universal parser for incomplete/partial code (CLI)

=== Recommendations ===

CLOJURE:
  ℹ️  Consider installing joker (complementary checks)

UNIVERSAL:
  ℹ️  Consider tree-sitter Python library (more reliable)
```

## Dialect-Specific Validation

### Clojure

**Primary tool:** clj-kondo (JSON output, comprehensive)
**Secondary tool:** joker (complementary checks)

```bash
# Using dialect-specific validator
python3 scripts/validate_clojure.py <file-or-directory>

# Skip joker (faster, clj-kondo only)
python3 scripts/validate_clojure.py src/ --no-joker
```

**What it detects:**
- Unbalanced parentheses
- Mismatched delimiters (`{` closed with `)`)
- Unexpected EOF
- Undefined symbols
- Arity mismatches
- Unused bindings
- Style issues

**Output structure:**
```json
{
  "target": "src/core.clj",
  "dialect": "clojure",
  "findings": [
    {
      "file": "src/core.clj",
      "line": 10,
      "col": 15,
      "end_line": 10,
      "end_col": 20,
      "severity": "error",
      "message": "Unexpected EOF.",
      "type": "unexpected-eof",
      "tool": "clj-kondo"
    }
  ],
  "summary": {
    "total_errors": 1,
    "total_warnings": 0,
    "tools_used": ["clj-kondo", "joker"]
  }
}
```

**Exit codes:**
- 0: No issues
- 2: Warnings only
- 3: Errors present

### Racket/Scheme

**Tools used:** raco expand, raco review, raco warn (tiered validation)
**Note:** raco tools work for both Racket and generic Scheme when Racket is installed

```bash
# Using dialect-specific validator
python3 scripts/validate_scheme.py <file-or-directory>

# Force raco tools (default if available)
python3 scripts/validate_scheme.py file.rkt --raco

# Fallback to specific Scheme dialect
python3 scripts/validate_scheme.py file.scm --no-raco --dialect guile
```

**Supported Scheme dialects (when raco unavailable):**
- guile
- chez
- chicken
- mit

**Validation stages:**
1. **Fast check** (raco expand): Safe syntax validation without execution
2. **Surface lint** (raco review): Quick error detection
3. **Deep analysis** (raco warn): Comprehensive warnings with suggestions

**What it detects:**
- Unbound identifiers
- Duplicate bindings
- Arity mismatches
- Type errors (Typed Racket)
- Unused variables
- Style violations

### Common Lisp

**Primary tool:** SBLint (machine-readable output)
**Secondary tool:** SBCL (deep semantic validation)

```bash
# Using dialect-specific validator
python3 scripts/validate_common_lisp.py <file-or-directory>

# Skip SBCL (faster, SBLint only)
python3 scripts/validate_common_lisp.py src/ --no-sbcl
```

**What it detects:**
- Undefined variables
- Undefined functions
- Unused variables
- Style warnings
- Compilation errors
- Read errors (syntax)

**Note:** SBCL provides verbose output requiring parsing; SBLint provides machine-readable format.

### Tree-Sitter (Incomplete Code)

**Critical for LLM workflows:** Handles partial/incomplete expressions

```bash
# Using tree-sitter validator
python3 scripts/validate_tree_sitter.py <file>

# Use Python library (more reliable)
python3 scripts/validate_tree_sitter.py file.lisp

# Use CLI only
python3 scripts/validate_tree_sitter.py file.lisp --no-python
```

**When to use:**
- Code is incomplete (missing closing parens)
- Validating partial expressions during generation
- Traditional validators fail on incomplete code
- Structural validation without semantic analysis

**Supported grammars:**
- Clojure (`tree-sitter-clojure`)
- Common Lisp (`tree-sitter-commonlisp`)
- Emacs Lisp (`tree-sitter-elisp`)

**Output:** Marks ERROR and MISSING nodes in parse tree

## Validation Workflows

### Progressive Validation (Recommended)

Validate in stages from fast to comprehensive:

```bash
# Stage 1: Fast check (< 1s)
python3 scripts/validate_tree_sitter.py file.clj

# Stage 2: Comprehensive (if stage 1 passes)
python3 scripts/validate_clojure.py file.clj

# Stage 3: Auto-format (only if validation passes)
# [Apply formatter like cljfmt, raco fmt, etc.]
```

### Incomplete Code Validation

When validating LLM-generated partial code:

```bash
# Force tree-sitter for incomplete code
python3 scripts/validate.py partial_code.clj --tree-sitter
```

**Interpreting results for incomplete code:**
- ERROR nodes: Unparseable sections
- MISSING nodes: Expected tokens absent
- "Unexpected EOF" is expected for incomplete code

Serious structural errors beyond incompleteness warrant attention.

### Project-Wide Validation

```bash
# Validate entire project (auto-detects files)
python3 scripts/validate.py project/src/

# Clojure project
python3 scripts/validate_clojure.py src/

# Racket package
python3 scripts/validate_scheme.py src/ --raco

# Common Lisp system
python3 scripts/validate_common_lisp.py src/
```

## Using Validation Scripts

### Main Orchestrator

`scripts/validate.py` auto-detects dialect and routes to appropriate validator.

**Options:**
```bash
--dialect <dialect>    Force specific dialect
--tree-sitter          Force tree-sitter (incomplete code)
--format <format>      Output format (json|text|summary)
```

**Examples:**
```bash
# Auto-detect
python3 scripts/validate.py src/

# Force dialect
python3 scripts/validate.py file.scm --dialect scheme

# Incomplete code
python3 scripts/validate.py partial.clj --tree-sitter

# Human-readable output
python3 scripts/validate.py src/ --format text
```

### Dialect-Specific Validators

Each validator provides focused validation for its dialect:

**Clojure:**
```bash
python3 scripts/validate_clojure.py <target> [--no-joker]
```

**Racket/Scheme:**
```bash
python3 scripts/validate_scheme.py <target> [--no-raco] [--dialect <dialect>]
```

**Common Lisp:**
```bash
python3 scripts/validate_common_lisp.py <target> [--no-sbcl]
```

**Tree-sitter:**
```bash
python3 scripts/validate_tree_sitter.py <file> [--no-python]
```

### Tool Checker

`scripts/check_tools.py` shows installation status and provides installation guidance.

```bash
# Text output (default)
python3 scripts/check_tools.py

# JSON output
python3 scripts/check_tools.py --json
```

## Reference Documentation

Detailed information is available in the `references/` directory:

### references/tool_comparison.md

Load this when determining which validation tools to use.

Contains:
- Complete tool comparison matrix
- Detailed tool profiles (installation, usage, output formats)
- Dialect-specific recommendations
- Performance comparison
- Exit code standards
- Optimal tool combinations for LLM workflows

**Use when:**
- Selecting validation tools for a project
- Understanding tool capabilities and limitations
- Comparing different validators
- Setting up CI/CD pipelines

### references/error_patterns.md

Load this when parsing validation tool output.

Contains:
- Regex patterns for each tool's output format
- Structured output formats (JSON, parseable text)
- Unstructured output parsing strategies (SBCL, Scheme dialects)
- Unified error schema for normalization
- Common error types by dialect
- Edge cases and parsing best practices

**Use when:**
- Parsing validation output programmatically
- Normalizing errors across multiple tools
- Implementing custom error handlers
- Debugging parsing issues

### references/integration_strategies.md

Load this when integrating validation into LLM workflows.

Contains:
- Core principles (progressive validation, structured output)
- Dialect-specific strategies and pipelines
- LLM-specific patterns (edit validation loop, partial expression validation)
- CI/CD integration examples
- Performance optimization techniques
- Error recovery strategies

**Use when:**
- Implementing LLM-guided code editing workflows
- Setting up automated validation pipelines
- Optimizing validation performance
- Handling validation errors in LLM context

## Interpreting Validation Results

### Error Severity Levels

- **error**: Code will not run (syntax errors, undefined symbols)
- **warning**: Code may run but has issues (unused variables, style)
- **info**: Informational messages (suggestions, style recommendations)

### Common Error Types

**Unbalanced parentheses:**
```
error: Unexpected EOF (missing closing parenthesis)
error: Unmatched delimiter: )
```

**Undefined symbols:**
```
error: Unresolved symbol: foo
error: Unbound variable: bar
```

**Arity mismatches:**
```
error: Wrong number of args (3) passed to function (expects 2)
```

### Acting on Validation Results

1. **Errors first:** Fix syntax and structural errors before warnings
2. **Location precision:** Use file:line:col to locate exact problem
3. **Suggestions:** Some tools (raco warn) provide fix suggestions
4. **Multiple tools:** Different tools may catch different issues
5. **Incomplete code:** Distinguish between "incomplete" and "invalid"

## Installation Guidance

### Recommended Tools by Dialect

**Clojure:**
```bash
# Primary: clj-kondo
brew install borkdude/brew/clj-kondo
# Or: npm install -g clj-kondo

# Secondary: joker
brew install candid82/joker/joker
```

**Racket/Scheme:**
```bash
# Install Racket (provides raco)
brew install racket  # macOS
# Or download from: https://racket-lang.org

# Install raco packages
raco pkg install review syntax-warn
```

**Common Lisp:**
```bash
# Install Roswell
brew install roswell  # macOS

# Install SBCL and SBLint
ros install sbcl
ros use sbcl
ros install cxxxr/sblint
```

**Universal (all dialects):**
```bash
# tree-sitter CLI
npm install -g tree-sitter-cli@0.19.3

# tree-sitter Python library (more reliable)
pip install tree-sitter tree-sitter-commonlisp tree-sitter-clojure tree-sitter-elisp
```

### Checking Installation Status

Always check which tools are available before validating:

```bash
python3 scripts/check_tools.py
```

This provides:
- Installation status per tool
- Platform-specific installation commands
- Dialect-specific recommendations
- Warnings for missing high-priority tools

## Best Practices

1. **Check tools first:** Run `check_tools.py` to verify available validators
2. **Use structured output:** JSON format for programmatic parsing
3. **Validate incrementally:** After each code edit in LLM workflows
4. **Handle incomplete code:** Use tree-sitter for partial expressions
5. **Combine tools:** Multiple validators catch different error types
6. **Read references:** Load relevant reference docs for detailed guidance
7. **Interpret exit codes:** 0=success, 2=warnings, 3=errors
8. **Fix errors before warnings:** Prioritize structural issues
9. **Use progressive validation:** Fast check → comprehensive → auto-fix
10. **Cache when possible:** clj-kondo and raco warn support caching

## Exit Codes

All validation scripts use consistent exit codes:

- **0**: Validation passed (no errors or warnings)
- **2**: Warnings only (code should run)
- **3**: Errors present (code may not run)

Use these for automation:

```bash
if python3 scripts/validate.py src/; then
    echo "✓ Validation passed"
else
    exit_code=$?
    if [ $exit_code -eq 2 ]; then
        echo "⚠ Warnings present"
    elif [ $exit_code -eq 3 ]; then
        echo "✗ Errors found"
    fi
fi
```

## Troubleshooting

### "Tool not found" errors

**Problem:** `clj-kondo not found` even though it's installed

```bash
# 1. Check if tool is in PATH
which clj-kondo

# 2. Verify installation
clj-kondo --version

# 3. Check PATH variable
echo $PATH

# 4. If not found, install it
brew install borkdude/brew/clj-kondo
# or
npm install -g clj-kondo
```

### "Cannot parse output" errors

**Problem:** Tree-sitter parse errors on valid code

This usually means you're using tree-sitter CLI 0.20+. Downgrade to 0.19.3:

```bash
# Uninstall current version
npm uninstall -g tree-sitter-cli

# Install correct version
npm install -g tree-sitter-cli@0.19.3

# Verify version
tree-sitter --version
# Should output: tree-sitter 0.19.3
```

### "Unexpected EOF" on complete code

**Problem:** Getting EOF errors but code looks complete

```bash
# Use tree-sitter to find exact error location
python3 scripts/validate_tree_sitter.py file.clj

# Check for hidden characters or mismatched delimiters
cat -A file.clj  # Shows hidden characters

# Count delimiters
grep -o '(' file.clj | wc -l  # Count opening parens
grep -o ')' file.clj | wc -l  # Count closing parens
```

### False positives

**Problem:** Joker flags macro-introduced bindings as errors

```bash
# Cross-reference with clj-kondo only
python3 scripts/validate_clojure.py file.clj --no-joker

# Compare tools side by side
python3 scripts/validate_clojure.py file.clj --format json | \
    jq '.findings[] | select(.tool == "joker")'
```

### Performance issues

**Problem:** Validation takes too long on large projects

```bash
# Skip secondary tools for faster validation
python3 scripts/validate_clojure.py src/ --no-joker
python3 scripts/validate_common_lisp.py src/ --no-sbcl

# Validate only changed files (with git)
git diff --name-only --cached | \
    grep '\.clj$' | \
    xargs python3 scripts/validate.py

# Parallel validation for multiple files
find src -name '*.clj' | \
    xargs -P 4 -I {} python3 scripts/validate.py {}
```

### JSON parsing errors

**Problem:** Cannot parse validation output as JSON

```bash
# Ensure you're getting JSON output
python3 scripts/validate.py file.clj --format json | jq

# Check for stderr contamination
python3 scripts/validate.py file.clj --format json 2>/dev/null | jq

# Validate JSON structure
python3 scripts/validate.py file.clj --format json | python3 -m json.tool
```
