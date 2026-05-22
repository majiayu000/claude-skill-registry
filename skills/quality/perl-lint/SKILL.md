---
name: perl-lint
description: 'This skill should be used when the user asks to "lint Perl code", "run perlcritic", "check Perl style", "format Perl code", "run perltidy", "/perl-lint", or mentions Perl::Critic policies, code formatting, or style checking.'
allowed-tools: Bash(perlcritic:*), Bash(perltidy:*), Bash(perl -c:*), Read, Grep, Glob
---

# Perl Linting and Formatting

Run Perl::Critic analysis and perltidy formatting with automatic tool detection.

## Workflow

1. Check if perlcritic/perltidy are installed
2. Run analysis on specified files
3. Report findings with severity levels
4. Suggest fixes or format code

## Tool Detection

First, verify tools are available:

```bash
# Check perlcritic
command -v perlcritic >/dev/null && echo "perlcritic available" || echo "Install: cpanm Perl::Critic"

# Check perltidy
command -v perltidy >/dev/null && echo "perltidy available" || echo "Install: cpanm Perl::Tidy"
```

## Perl::Critic Analysis

### Running perlcritic

```bash
# Default analysis (severity 5 - gentle)
perlcritic script.pl

# All severities (1 = strictest)
perlcritic --severity 1 script.pl

# Specific severity level
perlcritic --severity 3 script.pl

# With verbose explanations
perlcritic --verbose 11 script.pl

# Single policy
perlcritic --single-policy RequireUseStrict script.pl

# Exclude policies
perlcritic --exclude RequireUseWarnings script.pl
```

### Severity Levels

| Level | Name   | Description                   |
| ----- | ------ | ----------------------------- |
| 5     | Gentle | Obvious, unambiguous issues   |
| 4     | Stern  | Usually bad practices         |
| 3     | Harsh  | Controversial but recommended |
| 2     | Cruel  | Pickier about style           |
| 1     | Brutal | Maximum strictness            |

### Common Policies

| Policy                      | Severity | Issue                      |
| --------------------------- | -------- | -------------------------- |
| RequireUseStrict            | 5        | Missing `use strict`       |
| RequireUseWarnings          | 4        | Missing `use warnings`     |
| ProhibitBarewordFileHandles | 5        | Using bareword filehandles |
| ProhibitTwoArgOpen          | 5        | Two-argument open()        |
| ProhibitStringyEval         | 5        | Using eval with string     |
| RequireTidyCode             | 1        | Code not formatted         |

### Configuration File

Create `.perlcriticrc` in project root:

```ini
# .perlcriticrc
severity = 3
verbose = 8
theme = core

# Exclude specific policies
[-Documentation::RequirePodSections]
[-InputOutput::RequireBriefOpen]

# Configure specific policy
[CodeLayout::RequireTidyCode]
perltidyrc = .perltidyrc

[Variables::ProhibitPackageVars]
packages = Data::Dumper File::Find

[TestingAndDebugging::ProhibitNoStrict]
allow = refs
```

### Verbose Formats

| Level | Output Format            |
| ----- | ------------------------ |
| 1     | Line only                |
| 4     | Line + Column            |
| 8     | Line + Policy + Severity |
| 10    | Full explanation         |
| 11    | With PBP page reference  |

## Perltidy Formatting

### Basic Usage

```bash
# Format file (creates .bak backup)
perltidy script.pl

# Format to stdout (no backup)
perltidy -st script.pl

# In-place edit (no backup)
perltidy -b -nst script.pl

# Check if tidy (exit code)
perltidy -st script.pl | diff -q - script.pl
```

### Common Options

```bash
# Basic formatting
perltidy -i=4 -ci=4 -l=100 script.pl

# Full command with common options
perltidy \
    --indent-columns=4 \
    --continuation-indentation=4 \
    --maximum-line-length=100 \
    --vertical-tightness=2 \
    --paren-tightness=1 \
    --brace-tightness=1 \
    script.pl
```

### Configuration File

Create `.perltidyrc` in project root:

```text
# .perltidyrc

# Indentation
--indent-columns=4
--continuation-indentation=4

# Line length
--maximum-line-length=100

# Blank lines
--blank-lines-before-subs=1
--blank-lines-after-block-opening=0

# Spaces
--paren-tightness=1
--brace-tightness=1
--square-bracket-tightness=1

# Vertical alignment
--no-outdent-long-quotes
--no-outdent-long-comments

# Output
--backup-and-modify-in-place
--backup-file-extension=/
```

## Combined Workflow

### Lint and Fix

```bash
#!/bin/bash
# lint-perl.sh

FILE="$1"

if [[ ! -f "$FILE" ]]; then
    echo "Usage: lint-perl.sh <file.pl>"
    exit 1
fi

echo "=== Syntax Check ==="
perl -c "$FILE" || exit 1

echo ""
echo "=== Perl::Critic ==="
if command -v perlcritic >/dev/null; then
    perlcritic --severity 4 "$FILE"
else
    echo "perlcritic not installed. Run: cpanm Perl::Critic"
fi

echo ""
echo "=== Formatting Check ==="
if command -v perltidy >/dev/null; then
    if ! perltidy -st "$FILE" | diff -q - "$FILE" >/dev/null 2>&1; then
        echo "File needs formatting. Run: perltidy $FILE"
    else
        echo "File is properly formatted."
    fi
else
    echo "perltidy not installed. Run: cpanm Perl::Tidy"
fi
```

## Interpreting Results

### Severity 5 (Critical)

Must fix immediately:

```text
Bareword file handle opened at line 10, column 1.
Two-argument "open" used at line 15, column 5.
```

**Fix:**

```perl
# Wrong
open FILE, $filename;

# Correct
open my $fh, '<', $filename;
```

### Severity 4 (Important)

Should fix:

```text
Code before strictures are enabled at line 1.
```

**Fix:**

```perl
# Add at top
use strict;
use warnings;
```

### Severity 3 (Recommended)

Consider fixing:

```text
Regular expression without "/x" flag at line 25.
```

## Installation

If tools are missing:

```bash
# Install both tools
cpanm Perl::Critic Perl::Tidy

# Verify installation
perlcritic --version
perltidy --version
```

## Quick Commands

**Lint specific file:**

```bash
perlcritic --severity 4 --verbose 8 path/to/file.pl
```

**Lint all Perl files in directory:**

```bash
find . -name '*.pl' -o -name '*.pm' | xargs perlcritic --severity 4
```

**Format all files:**

```bash
find . -name '*.pl' -o -name '*.pm' | xargs perltidy -b
```
