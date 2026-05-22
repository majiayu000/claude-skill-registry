---
name: perl-validate
description: 'This skill should be used when the user asks to "validate Perl script", "check Perl syntax", "verify Perl code", "/perl-validate", or mentions script validation, compile check, security review, or best practice compliance for Perl code.'
allowed-tools: Bash(perl -c:*), Bash(perl -wc:*), Bash(perlcritic:*), Read, Grep, Glob
---

# Perl Script Validation

Comprehensive validation of Perl scripts for syntax, security, and best practices.

## Validation Checklist

1. Syntax check (`perl -c`)
2. Essential pragmas verification
3. Security pattern review
4. Best practice compliance
5. Documentation check

## Syntax Validation

### Basic Compile Check

```bash
# Check syntax
perl -c script.pl

# With warnings
perl -wc script.pl

# Check module
perl -c -I lib lib/MyApp/Module.pm
```

### Expected Output

**Success:**

```text
script.pl syntax OK
```

**Failure:**

```text
syntax error at script.pl line 15, near "my $"
script.pl had compilation errors.
```

## Essential Pragmas Check

Every production script MUST have:

```perl
#!/usr/bin/env perl
use strict;
use warnings;
use autodie;  # For scripts with file operations
```

### Validation Pattern

```bash
# Check for strict
grep -l 'use strict' script.pl || echo "MISSING: use strict"

# Check for warnings
grep -l 'use warnings' script.pl || echo "MISSING: use warnings"

# Check shebang
head -1 script.pl | grep -q '^#!' || echo "MISSING: shebang line"
```

## Security Validation

### Critical Checks

| Issue                    | Pattern to Find       | Fix                     |
| ------------------------ | --------------------- | ----------------------- |
| Two-arg open             | `open\s+\w+,\s*[^<>]` | Use 3-arg open          |
| Backticks with variables | `` `.*\$` ``          | Use IPC::System::Simple |
| eval with string         | `eval\s+"`            | Use eval block          |
| No taint mode            | `#!/.*perl\s*$`       | Add `-T` flag           |

### Security Check Commands

```bash
# Find two-argument open
grep -n 'open\s\+[A-Z]\+\s*,' script.pl

# Find unsafe backticks
grep -n '`.*\$' script.pl

# Find string eval
grep -n 'eval\s*"' script.pl

# Check for system with string
grep -n 'system\s*"' script.pl
```

## Best Practices Validation

### Variable Declarations

```bash
# Find undeclared variables (after perl -c passes)
# These would be caught by strict, but double-check:
grep -n '\$[a-z_][a-z0-9_]*\s*=' script.pl | head -20
```

### Function Definitions

Check for proper function structure:

```perl
# Good pattern
sub function_name {
    my ($arg1, $arg2) = @_;
    # ...
}

# Check for named parameters
grep -n 'sub.*{' script.pl
```

### Error Handling

```bash
# Find eval blocks without error check
grep -n 'eval\s*{' script.pl

# These should be followed by or do { } patterns
```

## Documentation Validation

### POD Check

```bash
# Validate POD syntax
podchecker script.pl

# Check for POD presence
perl -MPod::Usage -e 'pod2usage(-input => shift)' script.pl >/dev/null 2>&1 || echo "No POD documentation"
```

### Required POD Sections

```bash
# Check for NAME section
grep -l '^=head1 NAME' script.pl || echo "MISSING: =head1 NAME"

# Check for SYNOPSIS
grep -l '^=head1 SYNOPSIS' script.pl || echo "MISSING: =head1 SYNOPSIS"
```

## Comprehensive Validation Script

Run complete validation:

```bash
#!/bin/bash
# validate-perl.sh

FILE="$1"
ERRORS=0

if [[ ! -f "$FILE" ]]; then
    echo "Usage: validate-perl.sh <file.pl>"
    exit 1
fi

echo "=== Validating: $FILE ==="
echo ""

# 1. Syntax check
echo "--- Syntax Check ---"
if perl -wc "$FILE" 2>&1; then
    echo "PASS: Syntax OK"
else
    echo "FAIL: Syntax errors"
    ERRORS=$((ERRORS + 1))
fi
echo ""

# 2. Pragmas
echo "--- Essential Pragmas ---"
if grep -q 'use strict' "$FILE"; then
    echo "PASS: use strict found"
else
    echo "FAIL: Missing 'use strict'"
    ERRORS=$((ERRORS + 1))
fi

if grep -q 'use warnings' "$FILE"; then
    echo "PASS: use warnings found"
else
    echo "FAIL: Missing 'use warnings'"
    ERRORS=$((ERRORS + 1))
fi
echo ""

# 3. Security patterns
echo "--- Security Checks ---"
if grep -q 'open\s\+[A-Z]\+\s*,' "$FILE"; then
    echo "WARN: Possible bareword filehandle (check manually)"
else
    echo "PASS: No bareword filehandles detected"
fi

if grep -q '`.*\$' "$FILE"; then
    echo "WARN: Backticks with variables (potential injection)"
else
    echo "PASS: No unsafe backticks"
fi
echo ""

# 4. Documentation
echo "--- Documentation ---"
if podchecker "$FILE" 2>&1 | grep -q 'pod syntax OK'; then
    echo "PASS: POD syntax OK"
elif grep -q '^=head1' "$FILE"; then
    echo "WARN: POD present but may have issues"
else
    echo "INFO: No POD documentation"
fi
echo ""

# Summary
echo "=== Summary ==="
if [[ $ERRORS -eq 0 ]]; then
    echo "All critical checks passed."
    exit 0
else
    echo "Found $ERRORS critical issue(s)."
    exit 1
fi
```

## Quick Validation Commands

**Syntax only:**

```bash
perl -wc script.pl
```

**Pragmas check:**

```bash
head -10 script.pl | grep -E 'use (strict|warnings|autodie)'
```

**Security scan:**

```bash
perlcritic --severity 5 script.pl
```

**Full validation:**

```bash
perl -wc script.pl && \
  grep -q 'use strict' script.pl && \
  grep -q 'use warnings' script.pl && \
  echo "Basic validation passed"
```

## Fixing Common Issues

### Missing strict/warnings

Add to top of script:

```perl
use strict;
use warnings;
```

### Two-argument open

```perl
# Wrong
open FILE, $filename;

# Correct
open my $fh, '<', $filename;
```

### Unsafe system calls

```perl
# Wrong
system("rm $file");
`ls $dir`;

# Correct
use IPC::System::Simple qw(system capture);
system('rm', $file);
my $output = capture('ls', $dir);
```

### Missing error handling

```perl
# Wrong
open my $fh, '<', $file;

# Correct (with autodie)
use autodie;
open my $fh, '<', $file;

# Or explicit
open my $fh, '<', $file
    or die "Cannot open $file: $!";
```
