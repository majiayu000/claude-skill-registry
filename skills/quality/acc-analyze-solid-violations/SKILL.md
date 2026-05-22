---
name: acc-analyze-solid-violations
description: Analyzes PHP codebase for SOLID principle violations. Detects God classes (SRP), type switches (OCP), broken contracts (LSP), fat interfaces (ISP), and concrete dependencies (DIP). Generates actionable reports with severity levels and remediation recommendations.
---

# SOLID Violations Analyzer

## Overview

This skill analyzes PHP codebases for SOLID principle violations and generates detailed reports with severity levels and remediation recommendations.

## Analysis Workflow

### Step 1: Scope Identification

Determine analysis scope from user input or detect automatically:

```bash
# Detect project structure
ls -la src/

# Identify key directories
find . -type d -name "Domain" -o -name "Application" -o -name "Infrastructure"
```

### Step 2: Run Detection Patterns

Execute detection patterns for each SOLID principle.

## SRP (Single Responsibility) Detection

### God Class Detection

```bash
# Find large classes (>500 lines)
find . -name "*.php" -path "*/src/*" -exec wc -l {} \; | awk '$1 > 500 {print "CRITICAL: " $0}'

# Find classes with many methods
for file in $(find . -name "*.php" -path "*/src/*"); do
  count=$(grep -c "public function" "$file" 2>/dev/null || echo 0)
  if [ "$count" -gt 15 ]; then
    echo "WARNING: $file has $count public methods"
  fi
done

# Classes with problematic names
grep -rn "class.*Manager\|class.*Handler\|class.*Helper\|class.*Util" --include="*.php" src/
```

### High Dependency Count

```bash
# Count constructor dependencies
grep -rn "__construct" --include="*.php" -A 20 src/ | \
  grep -E "private|readonly" | \
  awk -F: '{files[$1]++} END {for(f in files) if(files[f]>7) print "WARNING: " f " has " files[f] " dependencies"}'
```

### Multiple Responsibility Indicators

```bash
# Classes with "And" in name
grep -rn "class\s\+\w*And\w*" --include="*.php" src/

# Check for mixed concerns
grep -rn "class.*Service" --include="*.php" src/ -l | while read file; do
  if grep -q "Repository\|Mailer\|Logger" "$file"; then
    echo "INFO: $file may have mixed concerns"
  fi
done
```

## OCP (Open/Closed) Detection

### Type Switch Detection

```bash
# Switch on type property
grep -rn "switch.*->type\|match.*->type\|match.*::class" --include="*.php" src/

# instanceof chains
grep -rn "if.*instanceof\|elseif.*instanceof" --include="*.php" src/

# Type-based conditionals
grep -rn "if.*getType\(\)\s*===\|if.*->type\s*===" --include="*.php" src/

# Hardcoded type maps
grep -rn "\[.*::class\s*=>" --include="*.php" src/
```

### Extension Indicators

```bash
# Classes that need frequent modification (check git history if available)
git log --since="3 months ago" --name-only --pretty=format: -- "*.php" | \
  sort | uniq -c | sort -rn | head -20
```

## LSP (Liskov Substitution) Detection

### Contract Violations

```bash
# NotImplementedException throws
grep -rn "throw.*NotImplemented\|throw.*NotSupported\|throw.*UnsupportedOperation" --include="*.php" src/

# Empty method overrides
grep -rn "public function.*\{[\s]*\}" --include="*.php" src/

# Parent type checks in child classes
grep -rn "if.*parent::\|parent::.*?:" --include="*.php" src/
```

### Precondition/Postcondition Issues

```bash
# Additional validation in overrides
grep -rn "function.*override" --include="*.php" -A 10 src/ | grep "if.*throw"

# Return null where parent might not
grep -rn "return\s*null;" --include="*.php" src/
```

## ISP (Interface Segregation) Detection

### Fat Interface Detection

```bash
# Count methods in interfaces
for file in $(find . -name "*.php" -path "*/src/*" -exec grep -l "^interface" {} \;); do
  count=$(grep -c "public function" "$file" 2>/dev/null || echo 0)
  if [ "$count" -gt 5 ]; then
    echo "WARNING: $file interface has $count methods"
  fi
  if [ "$count" -gt 8 ]; then
    echo "CRITICAL: $file interface has $count methods - consider splitting"
  fi
done
```

### Unused Interface Methods

```bash
# Find "// TODO" or "// not implemented" in interface implementations
grep -rn "//\s*TODO\|//\s*not implemented\|//\s*unused" --include="*.php" src/

# Empty implementations
grep -rn "function.*\{[\s]*return;\s*\}" --include="*.php" src/
```

### Generic Interface Names

```bash
# Overly generic interface names
grep -rn "interface\s\+\(Service\|Manager\|Handler\)\s*$" --include="*.php" src/
```

## DIP (Dependency Inversion) Detection

### Direct Instantiation

```bash
# New in methods (excluding exceptions, DateTime, stdClass)
grep -rn "new\s\+[A-Z]" --include="*.php" src/ | \
  grep -v "Exception\|DateTime\|stdClass\|DateTimeImmutable\|ArrayObject\|SplQueue"

# Static method calls to concrete classes
grep -rn "[A-Z][a-z]*::[a-z]" --include="*.php" src/ | \
  grep -v "self::\|static::\|parent::\|Uuid::\|Money::"
```

### Concrete Type Hints

```bash
# Constructor with concrete types (not interfaces)
grep -rn "__construct" --include="*.php" -A 15 src/ | \
  grep -E "(private|readonly)\s+[A-Z][a-z]*[A-Z][a-z]*\s+\\\$" | \
  grep -v "Interface\|Abstract\|Contract"
```

### Service Locator Anti-pattern

```bash
# Container/locator usage
grep -rn "container->get\|app()->make\|\\\$this->get(" --include="*.php" src/
```

## Report Generation

### Analysis Output Format

```markdown
# SOLID Violations Report

## Summary

| Principle | Critical | Warning | Info |
|-----------|----------|---------|------|
| SRP | X | X | X |
| OCP | X | X | X |
| LSP | X | X | X |
| ISP | X | X | X |
| DIP | X | X | X |

## Critical Violations

### SRP-001: God Class
- **File:** `src/Service/UserManager.php`
- **Lines:** 847
- **Issue:** Class exceeds 500 lines with 23 public methods
- **Recommendation:** Extract into focused classes
- **Skills:** `acc-create-use-case`, `acc-create-domain-service`

### OCP-001: Type Switch
- **File:** `src/Payment/PaymentProcessor.php:45`
- **Issue:** Switch on payment type requires modification for new types
- **Recommendation:** Apply Strategy pattern
- **Skills:** `acc-create-strategy`

## Warning Violations

### ISP-001: Fat Interface
- **File:** `src/Repository/UserRepository.php`
- **Methods:** 12
- **Issue:** Interface too large, clients forced to depend on unused methods
- **Recommendation:** Segregate into UserReader, UserWriter, UserStats

## Remediation Priority

1. **Immediate:** God classes blocking testing
2. **High:** Type switches preventing extension
3. **Medium:** Fat interfaces causing coupling
4. **Low:** Minor DIP violations
```

## Severity Classification

| Severity | Criteria | Action |
|----------|----------|--------|
| CRITICAL | >500 LOC, >10 deps, NotImplementedException | Immediate refactoring |
| WARNING | 300-500 LOC, 7-10 deps, type switches | Plan refactoring |
| INFO | 200-300 LOC, minor issues | Monitor in next iteration |

## Remediation Skills

| Violation | Recommended Skill |
|-----------|-------------------|
| God Class | `acc-create-use-case` |
| Type Switch | `acc-create-strategy` |
| No Interface | `acc-create-repository` |
| Domain Logic | `acc-create-domain-service` |
| Value Extraction | `acc-create-value-object` |
| Factory Missing | `acc-create-factory` |
| Decorator Need | `acc-create-decorator` |

## Quick Analysis Commands

```bash
# Full analysis
echo "=== SRP ===" && \
find . -name "*.php" -path "*/src/*" -exec wc -l {} \; | awk '$1 > 400' && \
echo "=== OCP ===" && \
grep -rn "switch.*type\|match.*::class" --include="*.php" src/ && \
echo "=== LSP ===" && \
grep -rn "NotImplemented\|NotSupported" --include="*.php" src/ && \
echo "=== ISP ===" && \
for f in $(find . -name "*.php" -exec grep -l "^interface" {} \;); do \
  c=$(grep -c "public function" "$f"); [ $c -gt 5 ] && echo "$f: $c methods"; \
done && \
echo "=== DIP ===" && \
grep -rn "new\s\+[A-Z]" --include="*.php" src/ | grep -v "Exception\|DateTime" | head -20
```

## Integration with acc-solid-knowledge

This analyzer uses detection patterns from `acc-solid-knowledge`. For detailed principle explanations and patterns, refer to:

- `acc-solid-knowledge/references/srp-patterns.md`
- `acc-solid-knowledge/references/ocp-patterns.md`
- `acc-solid-knowledge/references/lsp-patterns.md`
- `acc-solid-knowledge/references/isp-patterns.md`
- `acc-solid-knowledge/references/dip-patterns.md`
- `acc-solid-knowledge/references/antipatterns.md`

## Report Template

See `assets/report-template.md` for the full report format.
