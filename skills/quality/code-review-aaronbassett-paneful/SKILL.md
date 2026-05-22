---
name: code-review
description: Comprehensive code review guidance for quality, performance, and architecture across all programming languages. Use when (1) User explicitly requests code review, (2) After writing significant code changes, (3) Before commits/PRs, (4) Reviewing existing codebases, (5) Analyzing code quality, (6) Detecting performance issues, (7) Identifying architectural problems, (8) Finding code smells. Provides automated analysis scripts and manual review checklists for thorough code evaluation.
---

# Code Review

Comprehensive code review for quality, performance, and architecture across all languages.

## Quick Start

### Automated Review

Run complete analysis:
```bash
./scripts/review_code.sh /path/to/code
```

This runs:
- Language-specific linters (ESLint, Pylint, Clippy)
- Complexity analysis
- Code smell detection
- Report generation

### Manual Review

Use comprehensive checklist:
- See [review-checklist.md](references/review-checklist.md) for complete checklist

### Individual Analyzers

**Complexity analysis:**
```bash
./scripts/analyze_complexity.py /path/to/code
```

**Code smells:**
```bash
./scripts/detect_code_smells.py /path/to/code
```

## When to Use

**Trigger this skill when:**
- User says "review this code" or similar
- After significant code implementation
- Before committing/creating PRs
- Analyzing unfamiliar codebases
- Investigating quality issues
- Optimizing performance
- Refactoring

## What This Skill Provides

### Automated Analysis Scripts

**`review_code.sh`** - Complete review orchestrator
- Detects project type (JS/TS/Python/Rust)
- Runs appropriate linters
- Analyzes complexity
- Detects code smells
- Generates comprehensive report

**`analyze_complexity.py`** - Complexity metrics
- Cyclomatic complexity
- Function length
- Nesting depth
- Identifies problematic functions

**`detect_code_smells.py`** - Code smell detection
- Long parameter lists
- Magic numbers
- Duplicated code
- Deep nesting
- God classes

**`generate_review_report.py`** - Report generation
- Aggregates all findings
- Prioritizes issues
- Provides recommendations

### Manual Review Guidance

**[review-checklist.md](references/review-checklist.md)** - Complete review checklist
- Code quality checks
- Performance considerations
- Architecture review
- Security checklist
- Testing coverage

**[code-smells.md](references/code-smells.md)** - Code smell catalog
- Common smells by category
- Detection strategies
- Refactoring solutions

## Review Focus Areas

### 1. Code Quality
- Naming and readability
- DRY (Don't Repeat Yourself)
- YAGNI (You Aren't Gonna Need It)
- Consistent style
- Proper comments

### 2. Performance
- Algorithmic complexity
- Unnecessary loops/nesting
- Database query optimization
- Memory management
- Caching opportunities

### 3. Architecture
- Modularity and organization
- SOLID principles
- Coupling and cohesion
- Dependency management
- Design patterns

### 4. Code Smells
- Bloaters (long methods, large classes)
- Object-orientation abusers
- Change preventers
- Dispensables (dead code, duplication)
- Couplers (tight coupling)

## Common Workflows

### Workflow 1: Complete Project Review

```bash
# Run automated analysis
./scripts/review_code.sh /path/to/project

# Review output
cat .code-review-output/REVIEW.md

# Manual checklist review
# Consult references/review-checklist.md

# Address findings
# Refactor based on recommendations
```

### Workflow 2: Quick Complexity Check

```bash
# Analyze complexity
./scripts/analyze_complexity.py /path/to/code

# Identify complex functions
# Refactor functions with complexity >10
```

### Workflow 3: Pre-Commit Review

1. Run automated review
2. Check for high-severity issues
3. Review manual checklist
4. Ensure tests pass
5. Commit if approved

### Workflow 4: Legacy Code Analysis

1. Run full review to understand codebase
2. Identify problematic areas
3. Prioritize refactoring
4. Address incrementally

## Understanding Results

### Complexity Metrics

**Cyclomatic Complexity:**
- 1-5: Simple, easy to test
- 6-10: Moderate complexity
- 11-20: High complexity, consider refactoring
- 21+: Very high, definitely refactor

**Function Length:**
- ≤20 lines: Excellent
- 21-50 lines: Good
- 51-100 lines: Consider splitting
- 100+ lines: Refactor

**Nesting Depth:**
- 1-2 levels: Good
- 3-4 levels: Acceptable
- 5+ levels: Refactor

### Code Smell Severity

**High** - Address immediately:
- God classes
- Duplicated critical logic
- Deep nesting in hot paths

**Medium** - Address soon:
- Long parameter lists
- Feature envy
- Duplicated code

**Low** - Address when convenient:
- Magic numbers
- Minor duplication
- Speculative generality

## Language Support

### Detected Automatically

**JavaScript/TypeScript:**
- ESLint integration
- TypeScript compiler checks
- Complexity analysis
- Code smell detection

**Python:**
- Pylint integration
- Flake8 support
- MyPy type checking
- Complexity analysis

**Rust:**
- Clippy integration
- Cargo check
- Basic complexity analysis

### Additional Languages

For languages not automatically detected:
- Manual checklist still applies
- Use language-specific linters
- Complexity principles are universal

## Best Practices

1. **Review Early** - Don't wait until code is "complete"
2. **Focus on Impact** - High-severity issues first
3. **Be Constructive** - Suggest improvements, not just problems
4. **Consider Context** - Performance vs. readability tradeoffs
5. **Automate** - Use tools before manual review
6. **Test Changes** - Ensure refactoring doesn't break functionality
7. **Document Decisions** - Explain WHY, not just WHAT
8. **Iterate** - Re-review after changes

## Integration

### CI/CD Integration

Add to GitHub Actions:
```yaml
- name: Code Review
  run: |
    ./scripts/review_code.sh .
    # Fail if high-severity issues found
```

### Pre-commit Hook

```bash
#!/bin/bash
./scripts/review_code.sh . --quick
```

### Editor Integration

Most linters integrate with VS Code, IntelliJ, etc.

## Limitations

- **Static Analysis Only** - Doesn't catch runtime issues
- **Heuristic-Based** - Some false positives possible
- **Language Coverage** - Best for JS/TS/Python/Rust
- **No Business Logic** - Can't evaluate correctness
- **Context Unaware** - Doesn't understand project-specific conventions

## Getting Help

**For specific issues:**
- Complexity problems → See complexity thresholds above
- Code smells → See [code-smells.md](references/code-smells.md)
- General quality → See [review-checklist.md](references/review-checklist.md)

**After review:**
1. Address high-severity issues
2. Refactor complex functions
3. Remove code smells
4. Re-run review to verify

## Example Output

```
# Code Review Report

## Executive Summary
- Total Functions Analyzed: 127
- Code Smells Detected: 23
  - High Severity: 3
  - Medium Severity: 15
  - Low Severity: 5

## Complexity Analysis
- Average Complexity: 4.2
- Maximum Complexity: 18
- Functions Needing Attention: 8

## Recommendations
- Refactor 3 highly complex functions
- Address 3 high-severity code smells
- Extract duplicated code in 5 locations
```

---

**Note:** This skill provides guidance and automated checks. Final decisions on code quality depend on project context, team conventions, and business requirements.
