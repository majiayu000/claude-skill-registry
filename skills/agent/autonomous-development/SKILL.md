---
name: autonomous-development
description: Comprehensive autonomous development strategies including milestone planning, incremental implementation, auto-debugging, and continuous quality assurance for full development lifecycle management
version: 1.0.0
---

## Overview

The Autonomous Development skill provides comprehensive strategies, patterns, and best practices for managing full development lifecycles autonomously - from user requirements to production-ready implementation with minimal human intervention.

## When to Apply

Use Autonomous Development strategies when:
- Implementing features from high-level requirements
- Managing complex multi-phase development projects
- Need to maintain quality while developing autonomously
- Implementing with continuous testing and validation
- Debugging and fixing issues automatically
- Ensuring parameter consistency and type safety

## Milestone Planning Strategies

### Requirements Decomposition

**Pattern: Feature-to-Milestone Mapping**

```
User Requirement → Feature Breakdown → Milestone Plan

Example: "Add MQTT broker with certificate support"

Decomposition:
1. Dependencies & Configuration (Simple)
   - Install required libraries
   - Create configuration module
   - Time: 10-15 minutes

2. Core Functionality (Medium)
   - Implement main feature logic
   - Add error handling
   - Time: 20-30 minutes

3. Integration & Testing (Medium)
   - Write unit tests
   - Write integration tests
   - Time: 15-25 minutes

4. Documentation (Simple)
   - API documentation
   - Usage examples
   - Time: 10-15 minutes
```

**Complexity Assessment Matrix**

```
Simple Milestone:
├─ Single file modification
├─ Well-defined scope
├─ No external dependencies
├─ Existing patterns to follow
└─ Estimated: 10-20 minutes

Medium Milestone:
├─ Multiple file modifications
├─ Some external dependencies
├─ Integration with existing code
├─ Moderate complexity
└─ Estimated: 20-45 minutes

Complex Milestone:
├─ Multiple component changes
├─ New dependencies or frameworks
├─ Significant integration work
├─ Architectural considerations
└─ Estimated: 45-90 minutes

Expert Milestone:
├─ Major architectural changes
├─ Multiple system integrations
├─ Advanced algorithms or patterns
├─ Security-critical implementations
└─ Estimated: 90+ minutes
```

### Milestone Sequencing

**Pattern: Dependency-First Ordering**

```
Order milestones to minimize dependencies:

1. Foundation Layer
   - Dependencies
   - Configuration
   - Data models

2. Core Logic Layer
   - Business logic
   - Core algorithms
   - Main functionality

3. Integration Layer
   - API endpoints
   - External integrations
   - Service connections

4. Quality Layer
   - Testing
   - Documentation
   - Validation
```

## Incremental Development Patterns

### Commit-Per-Milestone Strategy

**Pattern: Working State Commits**

```
Each milestone must result in a working state:

✅ Good Milestone:
- Feature partially complete but functional
- All tests pass for implemented functionality
- No breaking changes to existing code
- Commit: "feat: add user authentication (phase 1/3)"

❌ Bad Milestone:
- Feature incomplete and non-functional
- Tests failing
- Breaking changes uncommitted
- Half-implemented logic
```

**Conventional Commit Format**

```
<type>(<scope>): <description>

[optional body]

[optional footer]

Types:
- feat: New feature
- fix: Bug fix
- refactor: Code refactoring
- test: Adding tests
- docs: Documentation
- chore: Maintenance
- perf: Performance improvement

Examples:
feat(mqtt): add broker connection with SSL
fix(auth): correct token validation logic
test(api): add integration tests for user endpoints
docs(readme): update installation instructions
```

### Progressive Enhancement Pattern

```
Start simple, enhance progressively:

Phase 1: Basic Implementation
├─ Core functionality only
├─ No error handling
├─ No optimization
└─ Purpose: Prove concept works

Phase 2: Error Handling
├─ Add try-catch blocks
├─ Add input validation
├─ Add logging
└─ Purpose: Make it robust

Phase 3: Optimization
├─ Performance improvements
├─ Memory optimization
├─ Caching if needed
└─ Purpose: Make it efficient

Phase 4: Polish
├─ Documentation
├─ Examples
├─ Edge case handling
└─ Purpose: Make it production-ready
```

## Auto-Debugging Strategies

### Error Classification System

```
Error Categories and Fix Strategies:

1. Syntax Errors (100% auto-fixable)
   - Missing colons, brackets, quotes
   - Indentation errors
   - Strategy: Parse and fix immediately

2. Import Errors (95% auto-fixable)
   - Missing imports
   - Incorrect module paths
   - Strategy: Auto-add imports, fix paths

3. Type Errors (90% auto-fixable)
   - Type mismatches
   - Type hint violations
   - Strategy: Add type conversions or fix hints

4. Name Errors (85% auto-fixable)
   - Undefined variables
   - Typos in names
   - Strategy: Fix typos or add definitions

5. Logic Errors (60% auto-fixable)
   - Wrong algorithm
   - Incorrect conditions
   - Strategy: Analyze and refactor logic

6. Integration Errors (70% auto-fixable)
   - Connection failures
   - API mismatches
   - Strategy: Add retry logic, fix endpoints

7. Performance Errors (40% auto-fixable)
   - Timeouts
   - Memory issues
   - Strategy: Optimize algorithms, add caching
```

### Debug Loop Pattern

```
Maximum 5 iterations per issue:

Iteration 1: Quick Fix (confidence > 90%)
├─ Fix obvious issues (typos, imports)
├─ Success rate: 70%
└─ Time: 30 seconds

Iteration 2: Pattern-Based Fix (confidence 70-90%)
├─ Apply known successful patterns
├─ Success rate: 50%
└─ Time: 1-2 minutes

Iteration 3: Analysis-Based Fix (confidence 50-70%)
├─ Deep error analysis
├─ Root cause investigation
├─ Success rate: 30%
└─ Time: 3-5 minutes

Iteration 4: Alternative Approach (confidence 30-50%)
├─ Try different implementation
├─ Success rate: 20%
└─ Time: 5-10 minutes

Iteration 5: Last Attempt (confidence < 30%)
├─ Aggressive fixes
├─ Success rate: 10%
└─ Time: 10-15 minutes

If all iterations fail → Manual intervention required
```

### Common Fix Patterns

**Connection Retry Pattern**

```python
# Problem: Connection refused
# Fix: Add exponential backoff retry

import time
from functools import wraps

def with_retry(max_attempts=3, backoff_factor=2):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except ConnectionError as e:
                    if attempt == max_attempts - 1:
                        raise
                    delay = backoff_factor ** attempt
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

@with_retry(max_attempts=3)
def connect_to_service():
    # Connection logic
    pass
```

**Type Conversion Pattern**

```python
# Problem: Type mismatch (str vs int)
# Fix: Add safe type conversion

def safe_int(value, default=0):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

# Usage
user_id = safe_int(request.params.get('user_id'))
```

**Null Safety Pattern**

```python
# Problem: NoneType attribute error
# Fix: Add null checks

# Bad
result = data.get('user').get('name')

# Good
result = data.get('user', {}).get('name', 'Unknown')

# Better
user = data.get('user')
result = user.get('name', 'Unknown') if user else 'Unknown'
```

**Parameter Validation Pattern**

```python
# Problem: Invalid parameters
# Fix: Add validation decorator

from functools import wraps
from typing import get_type_hints

def validate_params(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        hints = get_type_hints(func)
        for param_name, param_type in hints.items():
            if param_name in kwargs:
                value = kwargs[param_name]
                if not isinstance(value, param_type):
                    raise TypeError(
                        f"{param_name} must be {param_type}, "
                        f"got {type(value)}"
                    )
        return func(*args, **kwargs)
    return wrapper

@validate_params
def create_user(name: str, age: int) -> dict:
    return {'name': name, 'age': age}
```

## Parameter Consistency Validation

### Cross-File Parameter Validation

```
Critical validation checklist:

1. Function Signatures
   ✓ Parameter names match between definition and calls
   ✓ Parameter order consistent
   ✓ Default values aligned

2. Configuration Files
   ✓ Config keys match code usage
   ✓ Environment variables consistent
   ✓ No undefined config references

3. Type Consistency
   ✓ Type hints present and correct
   ✓ Return types specified
   ✓ Type conversions explicit

4. API Contracts
   ✓ Request parameters match backend expectations
   ✓ Response structure consistent
   ✓ Error codes standardized

5. Database Schemas
   ✓ Column names match model attributes
   ✓ Data types aligned
   ✓ Foreign key constraints correct
```

### Validation Automation Pattern

```python
# Automated parameter validation

def validate_function_calls(codebase):
    issues = []

    # Extract all function definitions
    definitions = extract_function_definitions(codebase)

    # Extract all function calls
    calls = extract_function_calls(codebase)

    for call in calls:
        definition = definitions.get(call.function_name)

        if not definition:
            issues.append({
                'type': 'undefined_function',
                'function': call.function_name,
                'location': call.location
            })
            continue

        # Check parameter count
        if len(call.args) != len(definition.params):
            issues.append({
                'type': 'parameter_count_mismatch',
                'function': call.function_name,
                'expected': len(definition.params),
                'actual': len(call.args)
            })

        # Check parameter names (for keyword args)
        for arg_name in call.kwargs:
            if arg_name not in definition.param_names:
                issues.append({
                    'type': 'undefined_parameter',
                    'function': call.function_name,
                    'parameter': arg_name
                })

    return issues
```

## Quality Assurance Patterns

### Quality Score Calculation

```
Quality Score (0-100):

Code Quality (40 points):
├─ Syntax correctness (10)
├─ Style compliance (10)
├─ Code complexity (10)
└─ Best practices (10)

Test Quality (30 points):
├─ Test coverage (15)
├─ Test success rate (10)
└─ Test quality (5)

Documentation Quality (20 points):
├─ Docstrings (10)
├─ Comments (5)
└─ Examples (5)

Security Quality (10 points):
├─ No vulnerabilities (5)
├─ Secure patterns (5)

Thresholds:
├─ 85-100: Excellent (production-ready)
├─ 70-84: Good (acceptable)
├─ 50-69: Fair (needs improvement)
└─ 0-49: Poor (not acceptable)
```

### Auto-Fix Priority System

```
Fix Priority Order:

Priority 1 (Always fix):
├─ Syntax errors
├─ Import errors
├─ Undefined variables
├─ Type errors (obvious)
└─ Success rate: 95%+

Priority 2 (Usually fix):
├─ Style violations
├─ Missing docstrings
├─ Unused imports
├─ Simple complexity issues
└─ Success rate: 80-95%

Priority 3 (Suggest fix):
├─ Complex refactoring
├─ Performance optimizations
├─ Architecture improvements
└─ Success rate: 60-80%

Priority 4 (Report only):
├─ Design decisions
├─ Major refactoring
├─ Architectural changes
└─ Requires human judgment
```

## Testing Strategies for Autonomous Development

### Test Generation Priorities

```
Test Priority Matrix:

Critical Path Tests (Must have):
├─ Core functionality tests
├─ Error handling tests
├─ Edge case tests
└─ Coverage target: 100%

Integration Tests (Should have):
├─ Component integration
├─ External service integration
├─ End-to-end workflows
└─ Coverage target: 80%

Performance Tests (Nice to have):
├─ Load tests
├─ Stress tests
├─ Benchmark tests
└─ Coverage target: 50%
```

### Test-First Development Pattern

```
For autonomous development:

1. Generate Test Cases First
   - Based on requirements
   - Cover happy path and edge cases
   - Include error scenarios

2. Implement to Pass Tests
   - Write minimal code to pass
   - Refactor after passing
   - Maintain test coverage

3. Expand Tests as Needed
   - Add tests for bugs found
   - Add tests for edge cases discovered
   - Keep tests up-to-date
```

## Requirements Verification Patterns

### Acceptance Criteria Validation

```
Verification Checklist Template:

Functional Requirements:
├─ [ ] Feature X implemented
├─ [ ] Feature Y working
├─ [ ] All specified behaviors present
└─ [ ] Edge cases handled

Non-Functional Requirements:
├─ [ ] Performance targets met
├─ [ ] Security requirements satisfied
├─ [ ] Scalability considered
└─ [ ] Maintainability ensured

Quality Requirements:
├─ [ ] Tests passing (100%)
├─ [ ] Code quality ≥ 85/100
├─ [ ] Documentation complete
└─ [ ] No critical issues

User Experience:
├─ [ ] Easy to use
├─ [ ] Clear error messages
├─ [ ] Good documentation
└─ [ ] Examples provided
```

## Integration with Learning System

### Pattern Storage for Development

```json
{
  "dev_pattern": {
    "requirement_type": "mqtt_integration",
    "complexity": "medium",

    "successful_approach": {
      "milestone_count": 5,
      "milestone_sequence": [
        "dependencies",
        "core_logic",
        "integration",
        "testing",
        "documentation"
      ],
      "avg_milestone_time": 9.7,
      "total_time": 48.5
    },

    "common_issues": [
      {
        "issue": "certificate_path_mismatch",
        "frequency": 0.65,
        "fix": "use_relative_paths",
        "success_rate": 0.95
      },
      {
        "issue": "connection_timeout",
        "frequency": 0.45,
        "fix": "add_retry_logic",
        "success_rate": 0.88
      }
    ],

    "quality_metrics": {
      "avg_code_quality": 92,
      "avg_test_coverage": 91,
      "avg_security_score": 94
    },

    "skill_effectiveness": {
      "code-analysis": 0.94,
      "testing-strategies": 0.91,
      "security-patterns": 0.88
    }
  }
}
```

## Best Practices

### DO's

✅ **Break Down Complexity**
- Decompose requirements into small, manageable milestones
- Each milestone should be independently testable
- Commit each working milestone

✅ **Validate Continuously**
- Run tests after each change
- Check parameter consistency frequently
- Validate type safety throughout

✅ **Debug Systematically**
- Start with high-confidence fixes
- Use pattern-based approaches
- Learn from failures

✅ **Document Progressively**
- Document as you implement
- Keep documentation synchronized
- Include usage examples

✅ **Learn from Experience**
- Store successful patterns
- Record failed approaches
- Optimize based on learnings

### DON'Ts

❌ **Don't Skip Validation**
- Never commit without tests passing
- Don't ignore parameter mismatches
- Don't skip quality checks

❌ **Don't Implement Everything at Once**
- Avoid big-bang implementation
- Don't commit non-working code
- Don't skip incremental commits

❌ **Don't Ignore Patterns**
- Don't repeat failed approaches
- Don't ignore learned patterns
- Don't make same mistakes twice

❌ **Don't Compromise Quality**
- Don't accept quality score < 70
- Don't skip security validation
- Don't skip documentation

## Advanced Patterns

### Parallel Milestone Execution

```
When milestones are independent:

Sequential (slower):
Milestone 1 → Milestone 2 → Milestone 3
Total time: 30 minutes

Parallel (faster):
Milestone 1 ─┐
Milestone 2 ─┼→ Sync → Milestone 4
Milestone 3 ─┘
Total time: 12 minutes

Use parallel execution for:
- Independent components
- Test generation
- Documentation updates
- Multiple bug fixes
```

### Adaptive Planning Pattern

```
Adjust plan based on execution:

Initial Plan:
├─ Milestone 1: 15 min (estimated)
├─ Milestone 2: 20 min (estimated)
├─ Milestone 3: 15 min (estimated)
└─ Total: 50 minutes

After Milestone 1 (took 25 min):
├─ Reason: Unexpected complexity
├─ Adjust remaining estimates: +10 min each
├─ New total: 70 minutes
└─ Re-evaluate approach if needed
```

The Autonomous Development skill provides comprehensive guidance for managing full development lifecycles with minimal human intervention, ensuring high quality and continuous improvement through learning.
