---
name: acc-detect-code-smells
description: Detects code smells in PHP codebases. Identifies God Class, Feature Envy, Data Clumps, Long Parameter List, Long Method, Primitive Obsession, Message Chains, Inappropriate Intimacy. Generates actionable reports with refactoring recommendations.
---

# Code Smells Detector

## Overview

This skill analyzes PHP codebases for code smells (symptoms of deeper problems) and generates detailed reports with severity levels and refactoring recommendations.

## Code Smells Catalog

| Smell | Description | Detection | Severity |
|-------|-------------|-----------|----------|
| God Class | Class doing too much | >500 LOC, >15 methods | CRITICAL |
| Feature Envy | Method uses another class more | Foreign calls > own calls | WARNING |
| Data Clumps | Same fields appear together | 3+ repeated params/fields | WARNING |
| Long Parameter List | Method with many params | >4 parameters | WARNING |
| Long Method | Method doing too much | >50 LOC | WARNING |
| Primitive Obsession | Primitives instead of objects | string $email, int $money | INFO |
| Message Chains | Long getter chains | ->get()->get()->get() | WARNING |
| Inappropriate Intimacy | Classes knowing too much | Direct field access | WARNING |

## Detection Patterns

### God Class Detection

```bash
# Large classes (>500 lines)
Grep: "^class " --glob "**/*.php"
# Then check file line counts

# Many public methods (>15)
Grep: "public function " --glob "**/*.php"
# Count per file

# Many dependencies (>8)
Grep: "__construct" --glob "**/*.php" -A 20
# Count constructor parameters

# Problematic names
Grep: "class.*Manager|class.*Handler|class.*Helper|class.*Util|class.*Processor" --glob "**/*.php"
```

**Indicators:**
- Class > 500 lines → CRITICAL
- Class > 15 public methods → CRITICAL
- Class > 8 constructor dependencies → WARNING
- Class name contains Manager, Handler, Helper, Util → INFO

### Feature Envy Detection

```bash
# Methods using other class data excessively
Grep: "\$this->[a-z]+->get[A-Z]" --glob "**/*.php"

# Multiple calls to same foreign object
Grep: "\$[a-z]+->.*\$[a-z]+->" --glob "**/*.php"

# Getters called more than own methods
Grep: "function [a-z]+\(" --glob "**/*.php" -A 30
# Analyze method bodies for foreign vs own calls
```

**Indicators:**
- Method calls other object's methods > own methods → WARNING
- Multiple chained calls to foreign object → INFO
- Method only transforms data from another class → WARNING

### Data Clumps Detection

```bash
# Repeated parameter groups in constructors
Grep: "__construct\(" --glob "**/*.php" -A 10
# Look for patterns: (string $x, string $y, string $z) appearing multiple times

# Repeated parameter groups in methods
Grep: "function [a-z]+\(" --glob "**/*.php"
# Look for same 3+ parameter combinations

# Multiple classes with same field groups
Grep: "(private|readonly) (string|int|float)" --glob "**/*.php"
# Detect repeated field patterns
```

**Common Data Clumps:**
- `$street, $city, $zipCode, $country` → Address Value Object
- `$startDate, $endDate` → DateRange Value Object
- `$amount, $currency` → Money Value Object
- `$firstName, $lastName, $email` → Contact/Person Value Object

### Long Parameter List Detection

```bash
# Methods with many parameters
Grep: "function [a-z]+\(" --glob "**/*.php"
# Count parameters (comma-separated)

# Constructors with many parameters
Grep: "__construct\(" --glob "**/*.php" -A 15
# Count parameters
```

**Thresholds:**
- 4+ parameters → INFO
- 6+ parameters → WARNING
- 8+ parameters → CRITICAL

### Long Method Detection

```bash
# Find method definitions and count lines until closing brace
Grep: "function [a-z]+\(" --glob "**/*.php" -A 60
# Analyze method length

# Nested control structures (indicator of complexity)
Grep: "if\s*\(.*\{.*if\s*\(" --glob "**/*.php" --multiline
```

**Thresholds:**
- 30+ lines → INFO
- 50+ lines → WARNING
- 100+ lines → CRITICAL

### Primitive Obsession Detection

```bash
# String parameters that should be Value Objects
Grep: "string \$email|string \$phone|string \$url|string \$currency|string \$country" --glob "**/*.php"

# Integer amounts
Grep: "int \$amount|int \$price|int \$total|int \$money|int \$cents" --glob "**/*.php"

# Float for money
Grep: "float \$amount|float \$price|float \$money" --glob "**/*.php"

# String status/type
Grep: "string \$status|string \$type|string \$state" --glob "**/*.php"

# Magic strings
Grep: "=== 'pending'|=== 'active'|=== 'completed'|=== 'draft'" --glob "**/*.php"
```

**Should be Value Objects:**
- Email addresses → Email
- Phone numbers → PhoneNumber
- URLs → Url or Uri
- Money amounts → Money (with currency)
- Dates/periods → DateRange, Period
- Identifiers → UserId, OrderId, etc.
- Status/Type → Enum

### Message Chains Detection

```bash
# Long getter chains
Grep: "->get[A-Z][a-z]+\(\)->get[A-Z][a-z]+\(\)" --glob "**/*.php"

# Triple or more chains
Grep: "->.*->.*->" --glob "**/*.php"

# Law of Demeter violations
Grep: "\$this->[a-z]+->get[A-Z].*->get[A-Z]" --glob "**/*.php"
```

**Indicators:**
- 2 chained getters → INFO
- 3+ chained getters → WARNING
- Chains in loops → CRITICAL

### Inappropriate Intimacy Detection

```bash
# Direct public property access
Grep: "\$[a-z]+->(?!get|set|is|has|can)[a-z]+" --glob "**/*.php"

# Friend classes accessing private state (via reflection)
Grep: "ReflectionClass|ReflectionProperty|setAccessible" --glob "**/*.php"

# Classes knowing internal structure
Grep: "->getInternalState|->getRawData|->getFields" --glob "**/*.php"
```

## Report Format

```markdown
# Code Smells Analysis Report

## Summary

| Smell | Critical | Warning | Info |
|-------|----------|---------|------|
| God Class | X | X | - |
| Feature Envy | - | X | X |
| Data Clumps | - | X | - |
| Long Parameter List | X | X | X |
| Long Method | - | X | X |
| Primitive Obsession | - | X | X |
| Message Chains | - | X | X |
| Inappropriate Intimacy | - | X | - |

**Total Issues:** X critical, X warnings, X info

## Critical Issues

### SMELL-001: God Class
- **File:** `src/Service/OrderManager.php`
- **Lines:** 847
- **Public Methods:** 23
- **Dependencies:** 12
- **Issue:** Class has too many responsibilities
- **Refactoring:**
  - Extract `OrderValidator` (validation logic)
  - Extract `OrderNotifier` (notification logic)
  - Extract `OrderPriceCalculator` (pricing logic)
- **Skills:** `acc-create-use-case`, `acc-create-domain-service`

### SMELL-002: Long Parameter List
- **File:** `src/Domain/Order/Order.php:45`
- **Method:** `createOrder()`
- **Parameters:** 9
- **Issue:** Too many parameters, hard to maintain
- **Refactoring:** Introduce Parameter Object
- **Skills:** `acc-create-dto`, `acc-create-builder`

## Warning Issues

### SMELL-003: Data Clump
- **Files:**
  - `src/Domain/User/User.php:15` — $street, $city, $zipCode
  - `src/Domain/Company/Company.php:23` — $street, $city, $zipCode
  - `src/Application/DTO/CreateOrderDTO.php:8` — $street, $city, $zipCode
- **Issue:** Address fields repeated across 3 classes
- **Refactoring:** Extract Address Value Object
- **Skills:** `acc-create-value-object`

### SMELL-004: Feature Envy
- **File:** `src/Service/ReportGenerator.php:89`
- **Method:** `generateUserReport()`
- **Issue:** Method makes 15 calls to User object, only 2 to own class
- **Refactoring:** Move method to User or create UserReportBuilder
- **Skills:** `acc-create-domain-service`

### SMELL-005: Primitive Obsession
- **File:** `src/Domain/User/User.php:12`
- **Field:** `private string $email`
- **Issue:** Email should be Value Object for validation
- **Refactoring:** Create Email Value Object
- **Skills:** `acc-create-value-object`

### SMELL-006: Message Chain
- **File:** `src/Application/Handler/CreateOrderHandler.php:34`
- **Code:** `$user->getCompany()->getAddress()->getCountry()`
- **Issue:** Law of Demeter violation, tight coupling
- **Refactoring:** Add shortcut method or delegate

## Info Issues

### SMELL-007: Long Method
- **File:** `src/Infrastructure/Repository/OrderRepository.php:78`
- **Method:** `findByComplexCriteria()`
- **Lines:** 45
- **Issue:** Method approaching complexity threshold
- **Refactoring:** Extract query builder or specification

## Refactoring Priority

1. **Immediate:** God Classes blocking testing
2. **High:** Data Clumps causing duplication
3. **Medium:** Long Parameter Lists
4. **Low:** Message Chains, minor smells
```

## Remediation Skills

| Smell | Recommended Skill | Approach |
|-------|-------------------|----------|
| God Class | `acc-create-use-case`, `acc-create-domain-service` | Extract focused classes |
| Feature Envy | `acc-create-domain-service` | Move method to data owner |
| Data Clumps | `acc-create-value-object` | Extract Value Object |
| Long Parameter List | `acc-create-dto`, `acc-create-builder` | Introduce Parameter Object |
| Long Method | `acc-create-use-case` | Extract methods |
| Primitive Obsession | `acc-create-value-object` | Replace with Value Object |
| Message Chains | (refactoring) | Hide delegate, extract method |
| Inappropriate Intimacy | (refactoring) | Move method, extract class |

## Quick Analysis Commands

```bash
# Full smell detection
echo "=== God Classes ===" && \
find . -name "*.php" -path "*/src/*" -exec wc -l {} \; | awk '$1 > 400' && \
echo "=== Long Parameter Lists ===" && \
grep -rn "function [a-z]*(" --include="*.php" src/ | grep -E "(\$[a-z]+,\s*){5,}" && \
echo "=== Primitive Obsession ===" && \
grep -rn "string \$email\|string \$phone\|int \$amount\|float \$price" --include="*.php" src/ && \
echo "=== Message Chains ===" && \
grep -rn "->get[A-Z].*->get[A-Z].*->get[A-Z]" --include="*.php" src/ && \
echo "=== Magic Strings ===" && \
grep -rn "=== '[a-z]*'\|== '[a-z]*'" --include="*.php" src/
```

## Integration with Other Skills

This skill works alongside:
- `acc-analyze-solid-violations` — SOLID violations overlap with some smells
- `acc-structural-auditor` — architectural context for smells
- `acc-ddd-auditor` — domain model quality assessment

## References

Based on Martin Fowler's "Refactoring" catalog:
- https://refactoring.guru/refactoring/smells
- "Refactoring: Improving the Design of Existing Code" (Fowler)