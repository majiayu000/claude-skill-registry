---
name: sop-authoring
description: Use when writing or creating new Standard Operating Procedures (SOPs) for AI agents. Covers effective SOP writing, clarity principles, and actionable instruction design.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# SOP Authoring

Effective Standard Operating Procedures (SOPs) transform complex workflows into reusable, deterministic instructions for AI agents. This skill covers the principles and practices for writing clear, actionable SOPs.

## Key Concepts

### What Makes a Good SOP

1. **Single Responsibility**: Each SOP addresses one specific workflow or task
2. **Deterministic**: Same inputs produce same outputs
3. **Actionable**: Every step is concrete and executable
4. **Parameterized**: Variables enable reuse across contexts
5. **Self-Contained**: Minimal external dependencies

### SOP vs. General Documentation

- **SOPs**: Prescriptive workflows with specific steps
- **Documentation**: Descriptive reference material
- **Guides**: Educational content with explanations
- **Tutorials**: Step-by-step learning experiences

Use SOPs when you need consistent, repeatable execution of multi-step processes.

## Best Practices

### Writing Clear Instructions

**DO:**

- Use active voice and imperative mood
- Start steps with action verbs (analyze, generate, validate)
- Be specific about expected outcomes
- Include success criteria for each step
- Use numbered lists for sequential steps
- Use bullet points for unordered items

**DON'T:**

- Use passive voice ("should be done" → "do this")
- Include vague instructions ("improve the code")
- Mix procedural and reference content
- Assume implicit knowledge without stating it

### Title and Description

```markdown
# {Action Verb} {Outcome} SOP

## Overview
{1-2 sentences describing what this SOP accomplishes and when to use it}
```

**Good Titles:**

- "Generate Codebase Documentation"
- "Implement Feature Using TDD"
- "Review Pull Request for Security"

**Poor Titles:**

- "Documentation" (too vague)
- "How to Maybe Improve Code Quality" (uncertain)
- "The Complete Guide to Everything" (too broad)

### Structuring Steps

**Sequential Steps:**

```markdown
## Steps

1. Analyze the codebase structure
   - Identify main entry points
   - Map directory organization
   - Document key dependencies

2. Extract architectural patterns
   - Identify design patterns in use
   - Document data flow
   - Note component relationships

3. Generate documentation
   - Create README.md with overview
   - Document API interfaces
   - Add setup instructions
```

**Conditional Logic:**

```markdown
## Steps

1. Check if tests exist
   - If tests exist: Run existing test suite
   - If no tests: Create test structure first

2. Implement feature based on test results
   - If tests pass: Add new functionality
   - If tests fail: Fix failing tests before proceeding
```

### Parameters

Define parameters that make SOPs reusable:

```markdown
## Parameters

- **Repository Path**: {repository_path}
- **Output Format**: {output_format} (markdown, json, html)
- **Verbosity Level**: {verbosity} (concise, detailed, comprehensive)
```

**Usage in Steps:**

```markdown
1. Navigate to {repository_path}
2. Generate documentation in {output_format} format
3. Use {verbosity} level of detail
```

### Success Criteria

Include explicit success criteria:

```markdown
## Success Criteria

- [ ] All source files are documented
- [ ] README.md exists with setup instructions
- [ ] API documentation is complete
- [ ] Examples are tested and working
```

## Examples

### Example 1: Code Review SOP

```markdown
# Review Code Changes for Quality

## Overview
Systematically review code changes for quality, maintainability, and adherence to project standards.

## Parameters

- **Pull Request URL**: {pr_url}
- **Review Depth**: {depth} (quick, standard, thorough)

## Steps

1. Fetch pull request details from {pr_url}
   - Read PR description and context
   - Identify changed files
   - Note breaking changes

2. Review code quality
   - Check for code smells
   - Verify error handling
   - Assess test coverage
   - Validate documentation updates

3. Check architectural consistency
   - Ensure patterns match existing code
   - Verify separation of concerns
   - Review dependency additions

4. Generate review feedback
   - List issues by severity (critical, major, minor)
   - Suggest specific improvements
   - Highlight positive changes

## Success Criteria

- [ ] All critical issues identified
- [ ] Feedback is specific and actionable
- [ ] Code style checked against project standards
- [ ] Security implications reviewed
```

### Example 2: Feature Implementation SOP

```markdown
# Implement Feature Using Test-Driven Development

## Overview
Implement new feature following TDD red-green-refactor cycle with comprehensive test coverage.

## Parameters

- **Feature Description**: {feature_description}
- **Test Framework**: {test_framework}

## Steps

1. Create failing test (RED)
   - Write test that describes desired behavior
   - Run test to confirm it fails
   - Verify failure message is correct

2. Implement minimal code (GREEN)
   - Write simplest code to pass the test
   - Avoid premature optimization
   - Run test to confirm it passes

3. Refactor (REFACTOR)
   - Improve code structure
   - Extract common patterns
   - Run tests to ensure they still pass

4. Repeat for each requirement
   - Break feature into small increments
   - Follow red-green-refactor for each
   - Commit after each complete cycle

## Success Criteria

- [ ] All tests pass
- [ ] Test coverage ≥ 80%
- [ ] No code duplication
- [ ] Feature meets requirements
```

### Example 3: Documentation Generation SOP

```markdown
# Generate Comprehensive Codebase Documentation

## Overview
Analyze codebase and generate comprehensive documentation including architecture overview, API reference, and setup instructions.

## Parameters

- **Repository Path**: {repository_path}
- **Documentation Format**: {format} (markdown, html, pdf)
- **Include Examples**: {include_examples} (yes, no)

## Steps

1. Analyze repository structure
   - Identify programming languages
   - Map directory organization
   - Locate configuration files
   - Find existing documentation

2. Extract architectural information
   - Identify main entry points
   - Document data flow
   - Map component dependencies
   - Note design patterns

3. Document public APIs
   - List all public functions/methods
   - Extract parameter types
   - Document return values
   - Include usage examples if {include_examples} is yes

4. Generate setup instructions
   - List prerequisites
   - Document installation steps
   - Provide configuration examples
   - Include troubleshooting section

5. Create documentation files
   - Generate README.md with overview
   - Create API.md with interface documentation
   - Add CONTRIBUTING.md if project accepts contributions
   - Format output as {format}

## Success Criteria

- [ ] Documentation covers all public APIs
- [ ] Setup instructions are complete
- [ ] Architecture is clearly explained
- [ ] Examples are tested and accurate
```

## Common Patterns

### Error Handling

```markdown
## Error Handling

If any step fails:
1. Document the failure reason
2. Provide troubleshooting steps
3. Suggest alternative approaches
4. Do NOT proceed to next step
```

### Validation Steps

```markdown
## Validation

After each major step:
- Verify output meets quality criteria
- Check for errors or warnings
- Confirm results match expectations
```

### Iterative Processes

```markdown
## Process

For each {item} in {collection}:
1. Perform action on {item}
2. Validate result
3. Continue to next {item}
```

## Anti-Patterns

**Avoid These Common Mistakes:**

1. **Overly General Instructions**
   - ❌ "Improve the code quality"
   - ✅ "Run linter and fix all errors, then remove code duplication"

2. **Missing Context**
   - ❌ "Run the tests"
   - ✅ "Run test suite using `npm test` and verify all tests pass"

3. **Ambiguous Success Criteria**
   - ❌ "Code should be good"
   - ✅ "Code passes all linter checks and has no security vulnerabilities"

4. **Hidden Assumptions**
   - ❌ Assuming tools are installed
   - ✅ Explicitly list prerequisites

5. **Mixing Multiple Workflows**
   - ❌ Combining testing, deployment, and monitoring in one SOP
   - ✅ Create separate SOPs that can be composed

## Related Skills

- **sop-structure**: Learn how to organize SOP sections
- **sop-rfc2119**: Use RFC 2119 keywords for precise requirements
- **sop-maintenance**: Keep SOPs up to date and relevant
