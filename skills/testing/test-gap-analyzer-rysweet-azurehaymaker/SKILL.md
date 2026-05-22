---
name: test-gap-analyzer
version: 1.0.0
description: |
  Analyzes code to identify untested functions, low coverage areas, and missing edge cases.
  Use when reviewing test coverage or planning test improvements.
  Generates specific test suggestions with example templates following amplihack's testing pyramid (60% unit, 30% integration, 10% E2E).
  Can use coverage.py for Python projects.
---

# Test Gap Analyzer Skill

## Purpose

This skill automatically analyzes codebases to identify untested functions, low coverage areas, and missing edge case tests. It generates actionable test suggestions organized by priority and risk impact, following amplihack's testing pyramid (60% unit, 30% integration, 10% E2E).

## When to Use This Skill

- **Code review**: Before merging PRs, identify test gaps
- **Test planning**: Prioritize what to test next based on risk
- **Coverage improvement**: Target low-coverage areas systematically
- **Edge case discovery**: Find untested failure modes and boundaries
- **New modules**: Ensure comprehensive test coverage before release
- **Legacy code**: Incrementally improve test coverage
- **Refactoring**: Verify coverage before and after changes

## Core Concepts

### Testing Pyramid in Amplihack

Tests should follow this distribution:

- **60% Unit Tests**: Individual function/method behavior with mocked dependencies
- **30% Integration Tests**: Multiple components working together
- **10% E2E Tests**: Full user workflows end-to-end

This skill helps balance tests across these layers while prioritizing coverage.

### Gap Analysis Categories

The skill identifies gaps in these areas:

1. **Untested Functions/Methods**: Functions with zero test coverage
2. **Low Coverage Areas**: Modules/functions below target threshold (85%+)
3. **Missing Edge Cases**: Boundary conditions, error paths, null checks
4. **Integration Gaps**: Component interactions not tested
5. **Error Path Coverage**: Exception handling and failure modes

## Analysis Process

### Step 1: Codebase Scanning

The analyzer:

1. Discovers all source code files in specified directory
2. Identifies all functions, methods, and classes
3. Maps code structure and dependencies
4. Determines current test coverage (if available)

### Step 2: Coverage Analysis

For each function/method:

1. Check if tests exist
2. Calculate line coverage if coverage data available
3. Identify untested branches and paths
4. Note error handling coverage

### Step 3: Gap Identification

Classify gaps by:

1. **Risk Level**: High/Medium/Low based on function complexity and criticality
2. **Type**: Untested, partial coverage, missing edge cases
3. **Effort**: Estimate time to write adequate tests
4. **Impact**: How important this function is to system reliability

### Step 4: Test Suggestion Generation

For each gap, generate:

1. Specific test case descriptions
2. Test templates with example code
3. Edge cases to cover
4. Expected behaviors
5. Error conditions to test

### Step 5: Prioritization

Organize suggestions by:

1. Risk impact (critical functions first)
2. Test pyramid distribution
3. Effort required
4. Dependency relationships

## Skill Capabilities

### Code Analysis

- Scans Python, JavaScript, TypeScript, Go codebases
- Identifies all public and private functions
- Detects complex functions needing more tests
- Maps function dependencies
- Finds unused parameters and dead code paths

### Coverage Detection

- Parses `.coverage` files (Python)
- Analyzes coverage.json reports
- Identifies uncovered branches
- Finds partially tested functions
- Detects coverage threshold violations

### Test Gap Discovery

- Functions with zero tests
- Branches never executed
- Error paths untested
- Boundary conditions missed
- Integration points not covered
- Timeout scenarios missing
- Resource exhaustion cases

### Edge Case Identification

- Null/None inputs
- Empty collections
- Boundary values (0, max_int, etc.)
- Unicode/multibyte strings
- Concurrency issues
- Resource limits
- Type mismatches
- Async/await patterns

### Test Template Generation

Provides ready-to-use test templates for:

- Unit tests (mocked dependencies)
- Integration tests (real components)
- E2E tests (full workflows)
- Parametrized tests
- Property-based tests
- Performance tests

## Usage Examples

### Example 1: Analyze Python Project

```
User: Analyze test coverage gaps in my src/ directory

Claude:
1. Scans src/ for all Python files
2. Reads .coverage or uses ast analysis
3. Identifies untested functions
4. Generates gap report with suggestions

Output:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Test Gap Analysis Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Summary:
- Total functions: 145
- Untested: 23 (16%)
- Low coverage (< 85%): 34 (23%)

CRITICAL GAPS (High Risk):
1. payment_processor.py::process_payment()
   - Untested | Handles money | 15 min effort
   - Suggested tests:
     - Valid payment processing
     - Insufficient funds error
     - Payment timeout
     - Currency conversion

MEDIUM GAPS:
2. user_service.py::validate_email()
   - 40% coverage | Missing edge cases
   - Suggested tests:
     - Unicode characters
     - Long email addresses
     - Special characters

LOW GAPS:
3. utils.py::format_date()
   - 60% coverage
   - Suggested tests:
     - Timezone handling
     - Daylight saving transitions
```

### Example 2: Get Test Templates

```
User: Generate test templates for my untested auth module

Claude:
Creates templates organized by testing pyramid:

Unit Tests (60%):
- test_token_validation_valid()
- test_token_validation_expired()
- test_token_validation_invalid_signature()

Integration Tests (30%):
- test_auth_flow_with_database()
- test_multi_user_concurrent_auth()

E2E Tests (10%):
- test_user_login_to_protected_resource()
- test_session_persistence_across_requests()
```

### Example 3: Coverage Improvement Plan

```
User: Help me improve test coverage from 65% to 85%

Claude:
1. Analyzes current coverage
2. Identifies gaps blocking 85% threshold
3. Prioritizes by impact
4. Estimates effort

Output:
To reach 85% coverage:
- 12 quick wins (< 2 hours each)
- 3 medium tasks (2-4 hours each)
- 2 complex tasks (4+ hours each)

Recommended order:
1. Add error case tests (5 tests, 3 hours) -> +8%
2. Cover auth edge cases (8 tests, 4 hours) -> +6%
3. Add integration tests (12 tests, 6 hours) -> +7%
```

## Analysis Checklist

### Coverage Inspection

- [ ] Identify all source files in target directory
- [ ] Determine current coverage percentage
- [ ] Find all untested functions
- [ ] Locate functions below 85% coverage
- [ ] Map branch coverage gaps

### Gap Classification

- [ ] Categorize by risk level (high/med/low)
- [ ] Estimate effort for each gap
- [ ] Identify critical path functions
- [ ] Find dependency relationships
- [ ] Prioritize by impact

### Test Suggestion Generation

- [ ] Generate unit test templates
- [ ] Generate integration test templates
- [ ] Suggest edge cases
- [ ] Provide error scenario tests
- [ ] Include parametrized test examples

### Report Generation

- [ ] Summary statistics
- [ ] Gap listing by priority
- [ ] Test templates for each gap
- [ ] Estimated effort total
- [ ] Recommended testing order

## Output Format

### Standard Report Structure

```markdown
# Test Gap Analysis Report

## Summary

- Total functions: N
- Untested functions: N (X%)
- Functions < 85%: N (X%)
- Average coverage: X%

## Critical Gaps (Must Test)

1. Function name | Type | Priority | Effort
   Suggested tests: [list]

## Medium Priority Gaps

[Similar structure]

## Low Priority Gaps

[Similar structure]

## Testing Pyramid Distribution

Current:

- Unit: X% | Target: 60%
- Integration: X% | Target: 30%
- E2E: X% | Target: 10%

## Test Templates

[Ready-to-use test code]

## Effort Estimate

- Quick wins: N hours
- Medium tasks: N hours
- Complex work: N hours
- Total: N hours
```

## Test Template Examples

### Unit Test Template

```python
def test_function_name_happy_path():
    """Test function with valid inputs."""
    # Arrange
    input_data = {...}
    expected = {...}

    # Act
    result = function_name(input_data)

    # Assert
    assert result == expected
```

### Error Case Template

```python
def test_function_name_invalid_input():
    """Test function raises ValueError on invalid input."""
    with pytest.raises(ValueError, match="Expected error message"):
        function_name(invalid_input)
```

### Edge Case Template

```python
def test_function_name_edge_case():
    """Test function handles edge case correctly."""
    # Test boundary conditions
    result = function_name(boundary_value)
    assert result is not None
```

### Integration Test Template

```python
def test_user_service_with_database(test_db):
    """Test user service with real database."""
    user_service = UserService(test_db)
    user = user_service.create_user("test@example.com")
    assert user.id is not None
```

## Philosophy Alignment

### Ruthless Simplicity

- Focus on essential tests, not comprehensive coverage
- 85% coverage is sufficient (diminishing returns beyond)
- Avoid testing implementation details
- Test behavior, not code structure

### Zero-BS Implementation

- All test templates work out of the box
- No placeholder tests or TODO comments
- Tests provide real value
- Edge cases are specific, not generic

### Testing Pyramid

- Prioritize unit tests (fast, isolated)
- Add integration tests (verify contracts)
- Minimal E2E tests (verify user flows)
- Balanced distribution prevents brittleness

## Integration with Other Skills

### Works With

- **code-quality-analyzer**: Identifies complexity
- **module-spec-generator**: Aligns tests with specs
- **refactor-advisor**: Plans test changes
- **type-safety-checker**: Tests type contracts

### Feeds Into

- **CI Validation**: Ensures tests pass before merge
- **Documentation**: Demonstrates module usage
- **Regression Prevention**: Protects against regressions

## Common Patterns

### Pattern 1: Fast Gap Discovery

```
User: Quick test coverage review of api/

Claude:
- Scans directory
- Identifies top 5 gaps
- Provides quick recommendations
- Total time: < 2 minutes
```

### Pattern 2: Systematic Coverage Improvement

```
User: Plan test coverage improvement from 60% to 85%

Claude:
- Analyzes gaps
- Creates phased improvement plan
- Prioritizes by risk
- Provides effort estimates
- Generates all test templates
```

### Pattern 3: New Module Test Planning

```
User: Generate complete test plan for new auth module

Claude:
- Analyzes module structure
- Maps public functions
- Creates test suggestions
- Balances testing pyramid
- Provides all templates
```

## Quality Checks

After analysis, verify:

- [ ] Gap identification is accurate
- [ ] Test templates are ready to use
- [ ] Effort estimates are realistic
- [ ] Prioritization follows risk analysis
- [ ] Testing pyramid is balanced
- [ ] Edge cases are specific, not generic
- [ ] Integration points are identified
- [ ] Error paths are covered

## Common Pitfalls to Avoid

### ❌ Over-Testing Implementation

Test behavior, not how the code works. Details can change.

### ❌ Generic Edge Cases

Be specific: "Test empty string" not "Test edge cases"

### ❌ Ignoring Integration

Don't just test functions in isolation. Test how they work together.

### ❌ Missing Error Paths

Every error condition should have at least one test.

### ❌ Untested Dependencies

Mock external systems, but test the integration points.

## Success Criteria

A good test gap analysis:

- [ ] Identifies all untested functions
- [ ] Prioritizes by risk and impact
- [ ] Provides ready-to-use test templates
- [ ] Balances testing pyramid
- [ ] Estimates effort realistically
- [ ] Includes edge case suggestions
- [ ] Maps integration gaps
- [ ] Provides actionable recommendations

## Tips for Effective Test Planning

1. **Start with critical functions**: Money, security, data integrity
2. **Use test templates**: Don't write from scratch
3. **Balance the pyramid**: Don't over-test edge cases
4. **Test contracts, not implementations**: Behavior matters, details don't
5. **Include happy path and error cases**: Both are important
6. **Automate coverage tracking**: Catch regressions early
7. **Iterative improvement**: 85% coverage is realistic, 100% is overkill
8. **Document why tests exist**: Future maintainers should understand intent

## Tools and Commands

### For Python Projects

```bash
# Generate coverage report
coverage run -m pytest
coverage json  # Creates coverage.json

# Analyze gaps with this skill
Claude: Analyze test gaps in my project using coverage.json
```

### For TypeScript/JavaScript

```bash
# Generate coverage report
jest --coverage

# Analyze gaps
Claude: Analyze test gaps in my TypeScript project
```

## Real-World Example

### Before Analysis

```
Project Stats:
- 156 functions
- 52% test coverage
- Unknown untested functions
- Scattered test files
```

### After Analysis

```
Gap Report:
- 24 untested functions (15%)
- 34 functions < 85% (22%)
- 12 critical gaps (high impact)
- 45 medium gaps (medium impact)
- 40 low gaps (low priority)

Recommendations:
1. Focus on critical gaps (payment, auth, data)
2. Add error case tests (20 tests, 8 hours)
3. Cover edge cases (15 tests, 6 hours)
4. Integration tests (12 tests, 10 hours)

Result after implementing:
- 89% test coverage
- All critical functions tested
- Balanced testing pyramid
- Improved confidence in refactoring
```

## Next Steps

After gap analysis:

1. **Review Report**: Understand current state
2. **Prioritize Gaps**: Focus on critical functions first
3. **Use Templates**: Implement suggested tests
4. **Run Tests**: Verify new tests pass
5. **Track Coverage**: Monitor improvement
6. **Iterate**: Gradually increase coverage

## Success Metrics

Effective test gap analysis results in:

- Clear picture of coverage status
- Actionable improvement plan
- 85%+ test coverage achieved
- Balanced testing pyramid
- Improved developer confidence
- Faster debugging and refactoring
- Fewer production issues
