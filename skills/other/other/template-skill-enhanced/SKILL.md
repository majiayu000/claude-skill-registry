---
name: your-skill-name
description: >-
  Brief description of what this skill does (1-2 sentences).
  Use when [specific trigger condition]. Keep under 200 words total.
author: Your Name <your.email@example.com>
version: 1.0.0
license: MIT
tags: [category1, category2, category3]
created: 2024-01-01
updated: 2024-01-01
triggers:
  - primary trigger phrase
  - secondary trigger phrase
  - tertiary trigger phrase
dependencies:
  skills: []
  tools: []
token_estimate: ~2500
---

# Skill Title

Brief overview paragraph (2-3 sentences) explaining what this skill provides, its purpose, and scope. Include the key value proposition and what makes this skill unique.

## When to Use This Skill

Specific scenarios that should activate this skill:

- **Primary Use Case**: Description of the main scenario
- **Secondary Use Case**: Description of another common scenario
- **Edge Case**: Less common but supported scenario
- Avoid using when [anti-pattern or wrong use case]

### Activation Triggers

Keywords and phrases that indicate this skill should activate:

- "keyword phrase one"
- "keyword phrase two"
- "related technical term"

## Core Principles

Essential knowledge required for effective skill execution. This section loads immediately when the skill activates.

### Principle 1: Foundation Concept

Explanation of the first essential concept:

```language
// Simple, clear example demonstrating the concept
// Include comments explaining key decisions
example_code_here()
```

**Key Points:**
- Critical aspect that must be understood
- Common misconception to avoid
- Relationship to other principles

### Principle 2: Core Pattern

Second essential concept building on the foundation:

```language
// Example showing pattern application
// Demonstrate best practices
apply_pattern()
```

**When to Apply:**
- Condition indicating this pattern is appropriate
- Another condition for application
- Context where this pattern excels

### Principle 3: Quality Standard

Quality requirements for implementations using this skill:

- **Requirement 1**: Description and rationale
- **Requirement 2**: Description and rationale
- **Verification**: How to confirm this standard is met

## Implementation Patterns

Detailed patterns for common scenarios. Load this section when deeper guidance is needed.

### Pattern 1: [Pattern Name]

**Problem**: Describe the specific problem this pattern solves

**Solution**: Explain the approach at a high level

**Implementation**:

```language
// Complete, working example
// Well-commented to explain approach
// Include error handling

function patternImplementation(input) {
    // Step 1: Validate input
    validate(input);

    // Step 2: Apply transformation
    const result = transform(input);

    // Step 3: Return with proper formatting
    return format(result);
}
```

**Trade-offs**:
| Aspect | Benefit | Cost |
|--------|---------|------|
| Performance | Fast execution | Higher memory |
| Maintainability | Clear structure | More boilerplate |
| Flexibility | Easy to extend | Initial complexity |

**When to Use**: Specific criteria for applying this pattern

**When to Avoid**: Situations where this pattern is inappropriate

### Pattern 2: [Alternative Pattern Name]

**Problem**: Different problem domain or same problem with different constraints

**Solution**: Alternative approach with different trade-offs

**Implementation**:

```language
// Alternative implementation
// Highlight differences from Pattern 1
alternative_approach()
```

**Comparison with Pattern 1**:
- Choose Pattern 1 when: [condition]
- Choose Pattern 2 when: [condition]

## Advanced Usage

Deeper patterns for complex scenarios. Load only when needed for sophisticated implementations.

### Advanced Pattern: [Complex Scenario]

Context explaining when this advanced usage is necessary:

```language
// More sophisticated example
// Show integration with multiple concepts
// Demonstrate production-ready code

class AdvancedImplementation {
    constructor(config) {
        this.config = this.validateConfig(config);
    }

    execute() {
        // Complex implementation
        // Include error handling
        // Show performance considerations
    }
}
```

**Considerations**:
- **Performance**: Impact on system resources
- **Scalability**: Behavior under load
- **Security**: Potential vulnerabilities to address
- **Maintenance**: Long-term code health

### Edge Cases and Error Handling

Common edge cases and how to handle them:

| Scenario | Expected Behavior | Handling Strategy |
|----------|-------------------|-------------------|
| Empty input | Graceful failure | Return default or throw descriptive error |
| Invalid format | Validation error | Provide clear error message with fix guidance |
| Resource exhaustion | Graceful degradation | Implement backoff and retry logic |

## Best Practices

Quick reference for implementing this skill effectively.

### Do's

- **Do this first**: Explanation of why this is important
- **Always validate**: Specific validation requirements
- **Prefer approach X**: Rationale for preferred approach
- **Document decisions**: What to capture and why
- **Test thoroughly**: Minimum testing requirements

### Don'ts

- **Don't skip validation**: Consequences of skipping
- **Avoid anti-pattern X**: Why this pattern causes problems
- **Never hardcode Y**: Alternative approach
- **Don't ignore errors**: Proper error handling approach
- **Avoid premature optimization**: When optimization is appropriate

### Performance Guidelines

- Optimization technique with expected improvement
- Caching strategy and when to apply
- Resource management best practices
- Profiling approach to identify bottlenecks

### Security Considerations

- Input validation requirements
- Output encoding needs
- Authentication/authorization checks
- Secrets management approach

## Anti-Patterns

Common mistakes to avoid when using this skill.

### Anti-Pattern 1: [Descriptive Name]

**What it looks like**:

```language
// Incorrect approach (anti-pattern)
bad_implementation_example()
```

**Why it's problematic**:
- Consequence 1
- Consequence 2
- Long-term impact

**Correct approach**:

```language
// Correct implementation
correct_implementation_example()
```

### Anti-Pattern 2: [Another Common Mistake]

**What it looks like**: Brief description

**Why it's problematic**: Explanation of consequences

**How to fix**: Guidance on correct approach

## Testing Strategies

### Unit Testing

```language
describe('Feature under test', () => {
    it('handles expected case correctly', () => {
        // Arrange
        const input = prepareInput();

        // Act
        const result = executeFunction(input);

        // Assert
        expect(result).toEqual(expectedOutput);
    });

    it('handles edge case gracefully', () => {
        // Edge case testing
    });
});
```

### Integration Testing

```language
// Integration test example
// Show testing across boundaries
integration_test_example()
```

## Troubleshooting

### Issue 1: [Common Problem]

**Symptoms**: Observable behavior indicating this issue

**Likely Causes**:
1. Most common cause
2. Second most common
3. Less common possibility

**Resolution Steps**:
1. Check this first
2. Verify this condition
3. Apply this fix

**Prevention**: How to avoid this issue in the future

### Issue 2: [Another Problem]

**Symptoms**: What the user observes

**Quick Fix**: Immediate solution if available

**Root Cause**: Underlying issue explanation

## External Resources

### Official Documentation
- [Documentation Name](https://example.com/docs) - Primary reference
- [API Reference](https://example.com/api) - Technical details

### Community Resources
- [Tutorial/Article](https://example.com/tutorial) - Hands-on guide
- [Video Course](https://example.com/video) - Visual learning

### Related Skills
- **skill-name-1**: How this skill complements the current one
- **skill-name-2**: When to use together

### Tools and Libraries
- **Tool 1**: Purpose and when to use
- **Library 1**: Integration approach

## Changelog

### 1.0.0 (YYYY-MM-DD)
- Initial release
- Core patterns implemented
- Examples validated

## Bundled Resources

This skill includes the following resources:

### References (Load as needed)
- `references/README.md` - Guide to using reference documentation
- `references/detailed-patterns.md` - Extended pattern documentation

### Examples
- `examples/basic.md` - Simple usage example with annotations

### Validation
- `validation/rubric.yaml` - Quality scoring rubric for skill outputs

## Skill Metadata

**Token Efficiency**: This skill is designed for progressive disclosure:
- Tier 1 (Core Principles): ~1000 tokens - Always loaded
- Tier 2 (Implementation Patterns): ~1500 tokens - Loaded when needed
- Tier 3 (Advanced + Resources): ~2000+ tokens - Loaded for complex scenarios

**Quality Targets**:
- Clarity score: >= 4/5
- Completeness score: >= 4/5
- Accuracy score: >= 5/5
- Usefulness score: >= 4/5

---

*This skill follows the cortex cookbook pattern for enhanced skill bundling.*
