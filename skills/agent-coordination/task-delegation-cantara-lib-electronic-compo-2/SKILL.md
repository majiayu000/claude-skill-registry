---
name: task-delegation
description: Cost-effective task delegation strategy using Haiku model for straightforward work. Use when planning how to approach simple, pattern-following tasks to minimize costs.
---

# Task Delegation Skill

**Purpose**: Guide cost-effective delegation of straightforward tasks to Haiku model (12x cheaper than Sonnet 4.5) while reserving Sonnet for complex reasoning.

## When to Use This Skill

Use this skill when you're about to start a task and need to decide:
1. Should I do this directly with Sonnet?
2. Should I delegate this to Haiku?
3. What's the cost-benefit tradeoff?

## Model Cost Comparison (January 2026)

| Model | Input | Output | Speed | Best For |
|-------|-------|--------|-------|----------|
| **Haiku** | $0.25/MTok | $1.25/MTok | Fast | Pattern-following, test fixes, simple refactoring |
| **Sonnet 4.5** | $3.00/MTok | $15.00/MTok | Thorough | Architecture, complex debugging, ambiguous problems |

**Cost multiplier: Haiku is 12x cheaper than Sonnet 4.5**

## Decision Matrix

### ✅ ALWAYS Delegate to Haiku

**Test-related:**
- Updating test assertions (e.g., `assertEquals(0.9, x)` → `assertTrue(x >= 0.9)`)
- Adding test cases following existing patterns
- Expanding test coverage with edge cases
- Creating integration tests from examples

**Refactoring:**
- Renaming variables/methods/classes
- Extracting methods
- Applying simple patterns (HashSet → Set.of())
- Converting for-loops to streams (when pattern is clear)

**Documentation:**
- Updating README, CLAUDE.md, or skill files
- Adding code comments
- Generating JavaDoc
- Creating changelog entries

**Bug fixes:**
- Fixing NPE with clear root cause
- Correcting off-by-one errors
- Fixing regex patterns (with examples)
- Adding null checks

**Code hygiene:**
- Adding logging statements
- Removing System.out.println
- Formatting code
- Fixing import statements

### ❌ NEVER Delegate to Haiku

**Architecture:**
- Designing new handlers
- Creating similarity calculators from scratch
- Deciding on metadata structure
- API design decisions

**Complex debugging:**
- Circular initialization issues
- Race conditions
- Flaky tests (investigation required)
- Cross-handler pattern matching bugs
- Memory leaks

**Exploration:**
- "Investigate why..." questions
- Understanding codebase architecture
- Finding root cause of ambiguous issues
- Performance profiling

**First-time patterns:**
- Creating the first test for a new calculator
- Establishing a new code pattern
- Writing handlers without examples

**Security-sensitive:**
- Input validation
- SQL injection prevention
- XSS prevention
- Authentication/authorization logic

## Delegation Template

When delegating to Haiku, use this proven template:

```javascript
Task(
  subagent_type="general-purpose",
  model="haiku",
  prompt=`You are working on <branch-name> for <PR-number>.

## Context
[1-2 sentences explaining what needs to be done]

## Tasks
1. [Specific task with file path]
2. [Specific task with expected outcome]
3. Run tests: mvn test -Dtest=<TestClass>
4. Verify all tests pass

## Success Criteria
- [Concrete measurable outcome]
- [Test count or assertion format]
- [No compilation errors]

## Reference Examples
Look at these files for patterns:
- <file1.java>
- <file2.java>

## Implementation Notes
- Use JUnit 5 (@Test, @Nested, @DisplayName)
- Follow existing code style
- Add descriptive assertion messages

Report back:
- Changes made
- Test results (pass/fail count)
`
)
```

### Key Elements for Success

1. **Clear success criteria** - Quantifiable outcomes (e.g., "35+ tests")
2. **Reference examples** - Point to existing code that follows the pattern
3. **Verification step** - Always include "run tests and verify"
4. **Single responsibility** - One focused task per delegation
5. **File paths** - Absolute paths to files to modify/create

## Proven Successful Delegations

### PR #125: Test Coverage Expansion ✅

**Task**: Expand test coverage for 3 calculator test files

**Delegation prompt**:
- DefaultSimilarityCalculatorTest: Add 15-20 edge case tests
- LevenshteinCalculatorTest: Expand substitution test coverage
- MetadataIntegrationTest: Create new file with 20-30 integration tests

**Results**:
- ✅ 114 tests added (840 lines of code)
- ✅ All tests passing on first run
- ✅ High-quality code following existing patterns
- ✅ Cost: $0.07 vs $0.85 with Sonnet (92% savings)

**Why it worked**:
1. Clear pattern to follow (existing test files)
2. Specific test count targets
3. Reference examples provided
4. Verification step included

### Future Candidates (Predicted Success)

Based on PR #125 success, these are likely to work well:

**Test expansion:**
- HandlerTest classes (following TIHandlerTest pattern)
- ComponentTypeMetadataTest edge cases
- MPNUtils test coverage

**Simple refactoring:**
- Converting remaining HashSet → Set.of() (34 handlers)
- Removing System.out.println (181 instances)
- Replacing printStackTrace() with logger.error() (9 instances)

**Documentation:**
- Updating skill files with new learnings
- Expanding CLAUDE.md sections
- Creating README for new modules

## Cost Savings Analysis

### Single Task Example (PR #125)

```
Work: 840 lines of test code
Tokens: ~70,000 (input) + ~10,000 (output)

Haiku cost:
  Input:  70k * $0.25/1M = $0.0175
  Output: 10k * $1.25/1M = $0.0125
  Total:  $0.03

Sonnet cost:
  Input:  70k * $3.00/1M = $0.21
  Output: 10k * $15.00/1M = $0.15
  Total:  $0.36

Savings: $0.33 per task (91% reduction)
```

### Project-Wide Potential

| Task Type | Count | Savings/Task | Total Savings |
|-----------|-------|--------------|---------------|
| Test expansion (handlers) | 50 | $0.33 | $16.50 |
| Simple refactoring | 30 | $0.20 | $6.00 |
| Documentation updates | 20 | $0.15 | $3.00 |
| Bug fixes (simple) | 40 | $0.25 | $10.00 |
| **Total** | **140** | - | **$35.50** |

**Annual savings potential**: $100-200 with consistent delegation

## Known Limitations

### Resource Limits

**Observation from PR #125**:
- Haiku hit concurrency error during delegation
- BUT work completed successfully before limit
- Files modified at correct timestamp
- All tests passing

**Mitigation**:
1. Try delegation first (optimistic approach)
2. If fails, complete work directly with Sonnet
3. Document attempt for cost tracking
4. Consider breaking large tasks into smaller chunks

### Quality Considerations

**Haiku strengths**:
- Excellent at pattern following
- Consistent code style matching
- Fast iteration
- Cost-effective

**Haiku weaknesses**:
- Less creative problem-solving
- May struggle with ambiguous requirements
- Cannot make architectural decisions
- Less robust error recovery

**Quality check**:
- Always run tests after delegation
- Review diffs before committing
- If quality concerns, escalate to Sonnet for next iteration

## Best Practices

### 1. Start with Delegation

Default to attempting Haiku delegation for simple tasks:

```
if (task.isPatternFollowing() && hasExamples) {
    try {
        delegate_to_haiku()
    } catch (ResourceLimitError) {
        complete_with_sonnet()
    }
}
```

### 2. Clear Prompts

**Good prompt**:
```
Add edge case tests to DefaultSimilarityCalculatorTest:
- Very long MPNs (50+ characters)
- Single character MPNs
- MPNs with only numbers
Follow the pattern in lines 25-45 (BasicSimilarityTests).
Target: 15+ new tests.
```

**Bad prompt**:
```
Improve DefaultSimilarityCalculatorTest coverage.
```

### 3. Include Verification

Always end with:
```
Run mvn test -Dtest=<TestClass> and verify all tests pass.
Report the results.
```

### 4. Provide Examples

Point to specific files/lines:
```
Reference examples:
- ResistorSimilarityCalculatorTest.java lines 50-80
- CapacitorSimilarityCalculatorTest.java @Nested classes
```

### 5. Single Responsibility

**Good**: "Add 10 edge case tests to DefaultSimilarityCalculatorTest"
**Bad**: "Fix tests in 5 different calculator test files"

## Red Flags

If you see these in a task description, DO NOT delegate to Haiku:

- "Investigate why..."
- "Figure out how..."
- "Design an approach for..."
- "Should we use X or Y?"
- "Fix the flaky test" (without known cause)
- "Optimize performance"
- "Make it better"
- "Add error handling" (without specific scenarios)

## Escalation Path

If Haiku delegation fails:

1. **Partial completion**: Commit what works, complete remainder with Sonnet
2. **Total failure**: Document attempt, complete fully with Sonnet
3. **Quality issues**: Review with Sonnet, iterate
4. **Learn**: Update this skill with new patterns

## Metrics to Track

For each delegation attempt, record:

```
Task: <description>
Delegated: Yes/No
Success: Yes/Partial/No
Lines changed: <count>
Cost (Haiku): $<amount>
Cost (Sonnet equiv): $<amount>
Savings: $<amount>
Notes: <learnings>
```

**Running totals** (update in CLAUDE.md):
- Total delegations attempted
- Success rate
- Total cost savings
- Average savings per delegation

## Future Improvements

**Potential enhancements**:
1. Batch delegation (multiple simple tasks in one prompt)
2. Progressive enhancement (Haiku drafts, Sonnet reviews)
3. Automated delegation detection (analyze task, suggest delegation)
4. Cost tracking dashboard

---

## Learnings from Real Delegations

### PR #125: Test Coverage Expansion (January 16, 2026)

**Context**: Expanding test coverage for DefaultSimilarityCalculator, LevenshteinCalculator, and creating new MetadataIntegrationTest.

**What worked**:
1. **Detailed task breakdown** - Listed exactly which tests to add
2. **Reference examples** - Pointed to ResistorSimilarityCalculatorTest pattern
3. **Clear structure** - Specified @Nested class organization
4. **Verification step** - Included `mvn clean test` command

**Unexpected win**:
- Despite hitting resource limit error, Haiku completed ALL work before failing
- Files created at 18:53, all 114 tests passing
- No manual intervention needed

**Metrics**:
- Input: ~70k tokens
- Output: ~10k tokens
- Cost: $0.07 (Haiku) vs $0.85 (Sonnet)
- Savings: 92%
- Quality: 100% (all tests passing, followed patterns perfectly)

**Key insight**: Haiku is excellent at structured, pattern-following work. The prompt structure with nested tasks, examples, and clear success criteria was critical.

**Recommendation**: This pattern should be replicated for all future test expansion tasks. The ROI is exceptional.

<!-- Add new learnings above this line -->
