---
name: complexity-management
description: Maintain and improve code quality using PHPInsights without decreasing quality thresholds. Use when PHPInsights fails, cyclomatic complexity is too high, code quality drops, or when refactoring for better maintainability. Always maintains 94% complexity and 100% quality/architecture/style scores.
---

# Code Complexity Management

## Context (Input)

- PHPInsights checks fail (`make phpinsights` returns errors)
- Cyclomatic complexity exceeds thresholds
- Code quality score drops below 100%
- Architecture score falls below 100%
- Style score drops below 100%
- Complexity score falls below 93%
- Adding new features that increase complexity
- Refactoring existing code for better maintainability

## Task (Function)

Maintain exceptional code quality standards using PHPInsights while preserving hexagonal architecture, DDD patterns, and CQRS design.

**Success Criteria**:

- `make phpinsights` passes without errors
- Code quality: 100%
- Complexity: ≥ 94%
- Architecture: 100%
- Style: 100%

---

## Protected Quality Thresholds

**CRITICAL**: These thresholds in `phpinsights.php` must NEVER be lowered:

```php
'requirements' => [
    'min-quality' => 100,      // Code quality
    'min-complexity' => 94,    // Cyclomatic complexity
    'min-architecture' => 100, // Architecture compliance
    'min-style' => 100,        // Coding style
],
```

**Policy**: If PHPInsights fails, fix the code - NEVER lower these thresholds.

---

## ⚠️ CRITICAL POLICY: NEVER CHANGE CONFIG

```
╔═══════════════════════════════════════════════════════════════╗
║  When PHPInsights fails, you MUST FIX THE CODE.               ║
║  NEVER lower thresholds in phpinsights.php.                   ║
║                                                               ║
║  ❌ FORBIDDEN: Changing config to pass checks                 ║
║  ✅ REQUIRED:  Refactoring code to meet standards             ║
╚═══════════════════════════════════════════════════════════════╝
```

---

## Quick Start Workflow

### Step 1: Identify Complex Classes

```bash
# Find top 20 most complex classes
make analyze-complexity

# Find top 10 classes
make analyze-complexity N=10

# Export as JSON for tracking
make analyze-complexity-json N=20 > complexity-report.json
```

**Output shows**:

- **CCN (Cyclomatic Complexity)**: > 15 is critical
- **WMC (Weighted Method Count)**: Sum of all method complexities
- **Avg Complexity**: CCN ÷ Methods (target: < 5)
- **Max Complexity**: Highest complexity of any single method
- **Maintainability Index**: 0-100 (target: > 65)

**See**: [reference/analysis-tools.md](reference/analysis-tools.md)

### Step 2: Run PHPInsights

```bash
make phpinsights
```

### Step 3: Identify Failing Metric

```
❌ [COMPLEXITY] 93.5 pts (target: 94%)
✗ Method `CustomerCommandHandler::handle` has cyclomatic complexity of 12
```

### Step 4: Apply Refactoring Strategy

**See**: [refactoring-strategies.md](refactoring-strategies.md) for proven patterns:

- Extract Methods
- Strategy Pattern
- Early Returns
- Functional Composition

### Step 5: Verify Improvements

```bash
make phpinsights
```

Repeat until all scores meet thresholds.

---

## Quick Fix Guide by Issue Type

### Cyclomatic Complexity Too High

**Problem**: Method has too many decision points (if/else/switch/loops)

**Identify hotspots**:

```bash
make analyze-complexity N=10
```

**Solutions**:

1. **Extract methods**: Break complex method into smaller private methods
2. **Strategy pattern**: Replace conditionals with polymorphism
3. **Early returns**: Reduce nesting with guard clauses
4. **Command pattern**: Separate command handling logic

**See**: [refactoring-strategies.md](refactoring-strategies.md) for DDD/CQRS-specific patterns

---

### Architecture Violations

**Problem**: Layer dependencies violated (e.g., Domain depending on Infrastructure)

**Solutions**:

1. **Review layer boundaries**: Domain → Application → Infrastructure
2. **Use interfaces**: Define contracts in Domain, implement in Infrastructure
3. **Dependency injection**: Inject dependencies through constructors
4. **Repository pattern**: Keep data access in Infrastructure layer

**See**: [deptrac-fixer](../deptrac-fixer/SKILL.md) skill for fixing architectural violations

---

### Style Issues

**Problem**: Code doesn't meet PSR-12 or Symfony coding standards

**Solution**:

```bash
# Auto-fix most style issues
make phpcsfixer

# Re-run PHPInsights to verify
make phpinsights
```

---

### Line Length > 100 Characters

**Problem**: Lines exceed configured limit

**Solutions**:

1. Break long method calls into multiple lines
2. Extract complex expressions into variables
3. Use named parameters (PHP 8+)
4. Refactor long argument lists into DTOs

**See**: [reference/project-configuration.md](reference/project-configuration.md)

---

## Constraints (Parameters)

### NEVER

- Lower quality thresholds in `phpinsights.php`
- Lower thresholds in `phpinsights-tests.php`
- Skip PHPInsights checks to "save time"
- Disable sniffs without understanding impact
- Ignore architecture violations
- Put business logic in Application layer (belongs in Domain)

### ALWAYS

- Fix code to meet standards (not config to meet code)
- Run `make phpinsights` after refactoring
- Maintain hexagonal architecture while reducing complexity
- Keep Domain layer pure (no framework dependencies)
- Use `make analyze-complexity` to find hotspots
- Run `make ci` before committing
- Preserve test coverage while refactoring

---

## Format (Output)

### Expected PHPInsights Output

```
[CODE] 100.0 pts       ✅ Target: 100%
[COMPLEXITY] 94.0 pts  ✅ Target: 94%
[ARCHITECTURE] 100 pts ✅ Target: 100%
[STYLE] 100.0 pts      ✅ Target: 100%
```

### Expected CI Output

```
✅ CI checks successfully passed!
```

---

## Verification Checklist

After refactoring:

- [ ] `make phpinsights` passes without errors
- [ ] Code quality: 100%
- [ ] Complexity: ≥ 94%
- [ ] Architecture: 100%
- [ ] Style: 100%
- [ ] No layer boundary violations (`make deptrac` passes)
- [ ] All tests still pass (`make all-tests`)
- [ ] Test coverage maintained
- [ ] Code remains aligned with hexagonal architecture

---

## Related Skills

- [quality-standards](../quality-standards/SKILL.md) - Overview of all protected quality thresholds
- [implementing-ddd-architecture](../implementing-ddd-architecture/SKILL.md) - Proper layer separation and patterns
- [deptrac-fixer](../deptrac-fixer/SKILL.md) - Fix architectural violations
- [ci-workflow](../ci-workflow/SKILL.md) - Run comprehensive CI checks
- [testing-workflow](../testing-workflow/SKILL.md) - Maintain test coverage during refactoring

---

## Quick Commands

```bash
# Find complex classes
make analyze-complexity N=10

# Run PHPInsights
make phpinsights

# Find complex methods with PHPMD
make phpmd

# Auto-fix style issues
make phpcsfixer

# Validate architecture
make deptrac

# Run all tests
make all-tests

# Full CI check
make ci
```

---

## Reference Documentation

For detailed patterns, strategies, and troubleshooting:

- **⚡ [Quick Start Guide](reference/quick-start.md)** - Fast-track workflow for immediate action
- **🔧 [Analysis Tools](reference/analysis-tools.md)** - Complete guide to complexity analysis commands
- **📚 [Refactoring Strategies](refactoring-strategies.md)** - Modern PHP patterns with real-world examples
- **📊 [Complexity Metrics](reference/complexity-metrics.md)** - Understanding what each metric means
- **🛠️ [Troubleshooting](reference/troubleshooting.md)** - Common issues and solutions
- **📈 [Monitoring](reference/monitoring.md)** - Track improvements over time
- **⚙️ [Project Configuration](reference/project-configuration.md)** - Project-specific settings and patterns

---

## Priority Order for Fixes

When facing multiple issues:

1. **CRITICAL (Complexity > 15)**: Immediate refactoring required
2. **HIGH (Architecture violations)**: Breaks hexagonal/DDD boundaries
3. **MEDIUM (Complexity 10-15)**: Plan refactoring
4. **LOW (Style issues)**: Quick fixes, often auto-fixable

---

## External Resources

- **PHPInsights Documentation**: https://phpinsights.com/
- **Project Architecture**: See CLAUDE.md for hexagonal/DDD/CQRS patterns
- **CodelyTV DDD**: Inspiration for architecture patterns
