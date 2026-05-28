---
name: code-formatter
description: Automatically format code files using the appropriate formatter based on file type, providing clear feedback on changes made
author: pilot-test
---

# Code Formatter

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.



A skill to automatically format code files using language-specific formatters.

## Overview

This skill helps format code files by detecting the programming language and applying the appropriate formatter. It supports JavaScript/TypeScript (Prettier), Python (Black), and Rust (rustfmt), providing clear feedback on formatting changes.

## When to Use

Use this skill when you need to format code files to match standard style guides, prepare code for commits, or ensure consistent formatting across a project.

## Instructions

### Step 1: Validate Input File

Check that the specified file exists and is readable.

```bash
if [ ! -f "$FILE_PATH" ]; then
    echo "Error: File not found"
    exit 1
fi
```

### Step 2: Detect File Language

Determine the programming language based on file extension.

```bash
case "$FILE_PATH" in
    *.js|*.jsx|*.ts|*.tsx)
        FORMATTER="prettier"
        ;;
    *.py)
        FORMATTER="black"
        ;;
    *.rs)
        FORMATTER="rustfmt"
        ;;
    *)
        echo "Error: Unsupported file type"
        exit 1
        ;;
esac
```

### Step 3: Check Formatter Installation

Verify the required formatter is installed.

```bash
if ! command -v $FORMATTER &> /dev/null; then
    echo "Error: $FORMATTER not installed"
    exit 1
fi
```

### Step 4: Run Formatter

Execute the formatter on the file.

```bash
case "$FORMATTER" in
    prettier)
        prettier --write "$FILE_PATH"
        ;;
    black)
        black "$FILE_PATH"
        ;;
    rustfmt)
        rustfmt "$FILE_PATH"
        ;;
esac
```

### Step 5: Report Results

Display what was changed.

```bash
echo "Formatted $FILE_PATH with $FORMATTER"
```

## Examples

**Example 1**: Format a JavaScript file
- Input: `format src/app.js`
- Output: `Formatted src/app.js with prettier`

**Example 2**: Format a Python file
- Input: `format main.py`
- Output: `Formatted main.py with black`


---
*Promise: `<promise>V0_SKILL_VERIX_COMPLIANT</promise>`*
