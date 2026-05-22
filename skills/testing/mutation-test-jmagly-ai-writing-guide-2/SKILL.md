---
name: mutation-test
description: Run mutation testing to validate test quality beyond code coverage. Use when assessing test effectiveness, finding weak tests, or validating test suite quality.
---


# Mutation Test Skill

## Purpose

Run mutation testing to measure test suite effectiveness. Mutation testing introduces small changes (mutants) to code and checks if tests catch them. High coverage with low mutation score indicates weak tests.

## Research Foundation

| Concept | Source | Reference |
|---------|--------|-----------|
| Mutation Testing Theory | IEEE TSE (2019) | Papadakis et al. "Mutation Testing Advances" |
| ICST Mutation Workshop | IEEE Annual | [Mutation 2024](https://conf.researchr.org/home/icst-2024/mutation-2024) |
| Stryker Mutator | Industry Tool | [stryker-mutator.io](https://stryker-mutator.io/) |
| PITest | Java Tool | [pitest.org](https://pitest.org/) |
| mutmut | Python Tool | [github.com/boxed/mutmut](https://github.com/boxed/mutmut) |

## When This Skill Applies

- User asks to "validate test quality" or "check test effectiveness"
- User mentions "mutation testing" or "mutation score"
- User wants to know if tests are "actually testing anything"
- High coverage but bugs still escaping
- Assessing test suite health
- Pre-release quality validation

## Trigger Phrases

| Natural Language | Action |
|------------------|--------|
| "Run mutation testing" | Execute mutation analysis |
| "Check if my tests are effective" | Run mutation + analyze |
| "Validate test quality" | Mutation score report |
| "Are my tests catching real bugs?" | Mutation analysis |
| "Find weak tests" | Identify low-score tests |
| "Why did this bug escape tests?" | Mutation analysis on module |

## Mutation Testing Concepts

### What is a Mutant?

A mutant is a small code change that should cause tests to fail:

```javascript
// Original
if (age >= 18) { return "adult"; }

// Mutant 1: Changed >= to >
if (age > 18) { return "adult"; }

// Mutant 2: Changed >= to ==
if (age == 18) { return "adult"; }

// Mutant 3: Changed "adult" to ""
if (age >= 18) { return ""; }
```

### Mutation Operators

| Operator | Example | Tests |
|----------|---------|-------|
| Arithmetic | `+` → `-` | Math operations |
| Relational | `>=` → `>` | Boundary conditions |
| Logical | `&&` → `\|\|` | Boolean logic |
| Literal | `true` → `false` | Constant handling |
| Return | `return x` → `return null` | Return value handling |

### Mutation Score

```
Mutation Score = (Killed Mutants / Total Mutants) × 100
```

| Score | Quality | Interpretation |
|-------|---------|----------------|
| 90%+ | Excellent | Tests are highly effective |
| 80-89% | Good | Target for production |
| 60-79% | Adequate | Room for improvement |
| <60% | Poor | Tests need significant work |

## Implementation Process

### 1. Detect Project and Install Tool

```python
def setup_mutation_tool(project_type):
    if project_type == "javascript":
        # Install Stryker
        return "npx stryker init"
    elif project_type == "python":
        # Install mutmut
        return "pip install mutmut"
    elif project_type == "java":
        # PITest via Maven/Gradle
        return "Add pitest plugin to pom.xml"
```

### 2. Configure Mutation Testing

**Stryker (JavaScript)**:
```json
// stryker.config.json
{
  "mutate": ["src/**/*.ts", "!src/**/*.test.ts"],
  "testRunner": "vitest",
  "reporters": ["html", "progress"],
  "coverageAnalysis": "perTest",
  "thresholds": {
    "high": 80,
    "low": 60,
    "break": 50
  }
}
```

**mutmut (Python)**:
```ini
# setup.cfg
[mutmut]
paths_to_mutate=src/
tests_dir=tests/
runner=pytest
```

**PITest (Java)**:
```xml
<!-- pom.xml -->
<plugin>
    <groupId>org.pitest</groupId>
    <artifactId>pitest-maven</artifactId>
    <version>1.15.0</version>
    <configuration>
        <targetClasses>
            <param>com.example.*</param>
        </targetClasses>
        <mutationThreshold>80</mutationThreshold>
    </configuration>
</plugin>
```

### 3. Run Mutation Analysis

```bash
# JavaScript
npx stryker run

# Python
mutmut run

# Java
mvn org.pitest:pitest-maven:mutationCoverage
```

### 4. Parse and Report Results

```python
def parse_mutation_results(report_path):
    """Parse mutation testing report"""
    return {
        "total_mutants": 150,
        "killed": 120,
        "survived": 25,
        "timeout": 5,
        "mutation_score": 80.0,
        "survivors": [
            {
                "file": "src/auth/validate.ts",
                "line": 45,
                "mutator": "RelationalOperator",
                "original": "age >= 18",
                "mutant": "age > 18",
                "status": "survived"
            }
            # ... more survivors
        ]
    }
```

## Output Format

```markdown
## Mutation Testing Report

**Module**: src/auth/
**Test Suite**: test/auth/

### Summary

| Metric | Value |
|--------|-------|
| Total Mutants | 150 |
| Killed | 120 (80%) |
| Survived | 25 (17%) |
| Timeout | 5 (3%) |
| **Mutation Score** | **80%** |

### Status: PASSED (threshold: 80%)

### Survived Mutants (Highest Priority)

#### 1. `src/auth/validate.ts:45`
```diff
- if (age >= 18) { return "adult"; }
+ if (age > 18) { return "adult"; }
```
**Problem**: Boundary condition not tested
**Fix**: Add test case for `age = 18`

#### 2. `src/auth/login.ts:23`
```diff
- if (attempts < maxAttempts) { allow(); }
+ if (attempts <= maxAttempts) { allow(); }
```
**Problem**: Off-by-one boundary not tested
**Fix**: Add test for `attempts = maxAttempts`

### Recommended Test Improvements

1. **Add boundary tests** for `validate.ts` (3 survivors)
2. **Add error path tests** for `login.ts` (2 survivors)
3. **Test null/undefined cases** in `session.ts` (1 survivor)

### Coverage vs Mutation Score

| File | Line Coverage | Mutation Score | Gap |
|------|--------------|----------------|-----|
| validate.ts | 95% | 72% | 23% |
| login.ts | 88% | 85% | 3% |
| session.ts | 100% | 91% | 9% |

*High coverage with low mutation score indicates weak assertions*
```

## Integration with CI

### GitHub Actions Integration

```yaml
- name: Run mutation testing
  run: npx stryker run --reporters json

- name: Check mutation threshold
  run: |
    SCORE=$(jq '.metrics.mutationScore' reports/mutation/stryker-incremental.json)
    if (( $(echo "$SCORE < 80" | bc -l) )); then
      echo "::error::Mutation score $SCORE% below 80% threshold"
      exit 1
    fi
```

## Optimization Tips

### Incremental Mutation Testing

Only test changed code:
```bash
# Stryker incremental
npx stryker run --incremental

# PITest history
mvn pitest:mutationCoverage -DwithHistory
```

### Target Critical Modules First

```json
{
  "mutate": [
    "src/auth/**/*.ts",
    "src/payment/**/*.ts",
    "src/validation/**/*.ts"
  ]
}
```

## Related Skills

- `tdd-enforce` - Enforce test-first development
- `flaky-detect` - Identify unreliable tests
- `test-sync` - Maintain test-code alignment

## Script Reference

### mutation_runner.py
Run mutation testing for project:
```bash
python scripts/mutation_runner.py --module src/auth
```

### mutation_analyzer.py
Analyze and prioritize survivors:
```bash
python scripts/mutation_analyzer.py --report stryker-report.json
```
