---
name: code_review
description: Review code for quality, security, and best practices. Use when analyzing code, suggesting improvements, or conducting code reviews.
version: 1.0.0
author: Workshop Team
---

# Code Review Skill

Provides comprehensive code review capabilities covering quality, security, and best practices analysis.

## When to Use

- User asks you to review their code
- User wants to improve code quality
- User asks about security vulnerabilities in code
- User wants to identify antipatterns or code smells
- User requests best practices suggestions
- User wants a general code quality assessment

## Available Operations

1. **Analyze Code Structure**: Evaluate organization, modularity, and architecture
2. **Check Best Practices**: Compare against established coding standards
3. **Security Review**: Identify potential security vulnerabilities
4. **Antipattern Detection**: Find common code smells and antipatterns
5. **Generate Review Report**: Provide structured feedback with recommendations

## Multi-Step Review Workflow

When conducting a code review, follow these steps in order:

### Step 1: Initial Code Analysis

Read the code thoroughly and identify:
- Primary purpose and functionality
- Programming language and frameworks used
- Overall structure and organization
- Entry points and main logic flow

### Step 2: Best Practices Check

Evaluate the code against best practices. Load the best practices guide for comprehensive checks:
- `references/best_practices.md` - Comprehensive coding standards and practices

Key areas to check:
- Naming conventions (variables, functions, classes)
- Function design (single responsibility, proper parameters)
- Error handling patterns
- Code organization and modularity
- Documentation and comments

### Step 3: Security Review

Check for security vulnerabilities. Load the security checklist for detailed guidance:
- `references/security_checklist.md` - Security review checklist based on OWASP guidelines

Key security areas:
- Input validation and sanitization
- Authentication and authorization
- Injection vulnerabilities (SQL, command, etc.)
- Data exposure and encryption
- Dependency security

### Step 4: Antipattern Detection

Identify code smells and antipatterns. Load the antipatterns guide for reference:
- `references/common_antipatterns.md` - Common antipatterns and how to fix them

Common issues to look for:
- God classes/functions
- Deep nesting
- Magic numbers and strings
- Copy-paste code
- Resource leaks

### Step 5: Generate Review Report

Compile findings into a structured report:

```
## Code Review Summary

**File/Module**: [name]
**Language**: [language]
**Overall Assessment**: [Excellent/Good/Needs Improvement/Critical Issues]

### Strengths
- [List positive aspects]

### Issues Found

#### Critical (Must Fix)
- [Security vulnerabilities, bugs]

#### Major (Should Fix)
- [Significant antipatterns, bad practices]

#### Minor (Consider Fixing)
- [Style issues, small improvements]

### Recommendations
1. [Specific actionable recommendations]
2. [...]

### Resources Referenced
- [List which reference files were consulted]
```

## Resources

Reference these files for detailed guidance during reviews:

- `references/best_practices.md` - Comprehensive coding best practices covering organization, naming, error handling, testing, and documentation
- `references/security_checklist.md` - Security review checklist covering OWASP Top 10, input validation, authentication, and common vulnerabilities
- `references/common_antipatterns.md` - Guide to detecting and fixing common antipatterns like god classes, spaghetti code, and resource leaks

## Examples

### Example 1: Quick Review Request

User asks: "Can you review this function?"

Response approach:
1. Load this skill's full instructions
2. Analyze the provided code
3. Check against best practices (load `references/best_practices.md` if needed)
4. Identify any obvious security issues
5. Provide concise feedback with specific recommendations

### Example 2: Security-Focused Review

User asks: "Check this code for security vulnerabilities"

Response approach:
1. Load this skill's full instructions
2. Load `references/security_checklist.md` for comprehensive security checks
3. Systematically check each security category
4. Provide detailed security findings with severity ratings
5. Include specific fix recommendations

### Example 3: Comprehensive Code Review

User asks: "I need a thorough code review of my authentication module"

Response approach:
1. Load this skill's full instructions
2. Follow the complete multi-step workflow
3. Load all three reference files as needed
4. Provide comprehensive report covering all aspects
5. Prioritize recommendations by impact

## Notes

- Always be constructive in feedback - explain why something is an issue and how to fix it
- Severity ratings: Critical (security/bugs), Major (significant quality issues), Minor (style/polish)
- Focus on the most impactful issues first
- Provide specific code examples when suggesting fixes
- Consider the context - production code needs higher scrutiny than prototypes
- Reference specific sections of the guide files when making recommendations
