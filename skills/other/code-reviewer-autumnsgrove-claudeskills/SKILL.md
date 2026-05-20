---
name: code-reviewer
description: "Automated code review with security scanning, quality metrics, and best practices analysis. Use when reviewing code for: (1) Security vulnerabilities and common attack vectors, (2) Code quality issues and maintainability concerns, (3) Performance bottlenecks and optimization opportunities, (4) Best practices and design patterns, (5) Test coverage and testing strategies, (6) Documentation quality and completeness"
---

# Code Reviewer

Comprehensive automated code review skill that systematically analyzes code for security issues, quality metrics, performance problems, and adherence to best practices.

## Purpose

This skill provides structured code review workflows that combine automated analysis tools with expert guidance to identify issues across security, quality, performance, and maintainability dimensions.

## When to Use This Skill

Use this skill when:
- Reviewing pull requests or code submissions
- Conducting security audits of existing codebases
- Evaluating code quality before deployment
- Identifying technical debt and refactoring opportunities
- Establishing code review standards for teams
- Learning what to look for in code reviews

## Core Review Workflow

### Phase 1: Initial Analysis

#### 1.1 Understand the Context
- Read the PR description or change summary
- Identify the type of change (feature, bug fix, refactor, security patch)
- Determine the scope and affected components
- Note any related issues or tickets

#### 1.2 Code Overview
- Review file changes and additions/deletions
- Identify changed modules and their relationships
- Look for unexpected changes or scope creep
- Check for breaking changes

### Phase 2: Security Review

#### 2.1 Common Vulnerability Patterns

Check for these critical security issues:

**Input Validation**
- Unvalidated user input reaching sensitive operations
- SQL injection vulnerabilities
- Command injection possibilities
- Path traversal attacks
- XML/XXE injection points

**Authentication & Authorization**
- Missing authentication checks
- Broken access control
- Insecure password storage
- Weak session management
- Missing CSRF protection

**Data Exposure**
- Hardcoded credentials or API keys
- Sensitive data in logs
- Inadequate encryption
- Information disclosure in error messages
- Exposed configuration files

**Code Injection**
- Unsafe deserialization
- Template injection
- Code evaluation from user input
- Unsafe reflection usage

#### 2.2 Automated Security Scanning

Use security analysis tools:

**Python:**
```bash
# Run bandit for security issues
python scripts/review_helper.py --security-scan path/to/code

# Check dependencies for known vulnerabilities
safety check
pip-audit
```

**JavaScript/Node.js:**
```bash
# Check for vulnerabilities
npm audit
yarn audit

# Use ESLint security plugins
eslint --plugin security path/to/code
```

**Go:**
```bash
# Security scanning
gosec ./...
```

See `references/security_patterns.md` for detailed vulnerability patterns.

### Phase 3: Code Quality Analysis

#### 3.1 Code Structure

**Modularity & Organization**
- Single Responsibility Principle adherence
- Proper separation of concerns
- Appropriate abstraction levels
- Clear module boundaries
- Logical file organization

**Complexity Metrics**
- Cyclomatic complexity (target: < 10 per function)
- Function length (target: < 50 lines)
- Class size (target: < 300 lines)
- Nesting depth (target: < 4 levels)
- Parameter count (target: < 5 parameters)

**Code Smells**
- Duplicated code
- Long methods or god classes
- Feature envy (method uses more of another class)
- Data clumps (repeated parameter groups)
- Primitive obsession
- Inappropriate intimacy between classes

#### 3.2 Naming and Readability

**Naming Conventions**
- Descriptive, intention-revealing names
- Consistent naming patterns
- Appropriate length (not too short, not too long)
- Avoid abbreviations unless standard
- Boolean names start with is/has/should/can

**Code Clarity**
- Clear control flow
- Minimal cognitive load
- Self-documenting code
- Appropriate comments (why, not what)
- Consistent formatting

#### 3.3 Error Handling

**Robustness**
- Proper exception handling
- No bare except/catch blocks
- Appropriate error messages
- Resource cleanup (file handles, connections)
- Graceful degradation

**Edge Cases**
- Null/None checks
- Empty collection handling
- Boundary conditions
- Concurrent access issues
- Race condition prevention

### Phase 4: Performance Review

#### 4.1 Common Performance Issues

**Algorithm Efficiency**
- O(n²) or worse algorithms when better exists
- Unnecessary loops or iterations
- Inefficient data structure usage
- Missing memoization/caching opportunities

**Resource Management**
- Memory leaks
- Unclosed file handles or connections
- Excessive memory allocation
- Thread/process pool exhaustion

**Database Operations**
- N+1 query problems
- Missing indexes
- SELECT * usage
- Inefficient JOIN operations
- Missing query optimization

**Network Calls**
- Synchronous blocking calls
- Missing timeout configurations
- No retry logic
- Excessive API calls
- Missing connection pooling

See `references/performance_guide.md` for optimization strategies.

### Phase 5: Testing Assessment

#### 5.1 Test Coverage

**Coverage Metrics**
- Line coverage (target: > 80%)
- Branch coverage (target: > 75%)
- Function coverage (target: > 90%)
- Critical path coverage (target: 100%)

**Test Quality**
- Tests actually assert meaningful behavior
- Tests are independent and isolated
- Test names clearly describe what they test
- Proper use of mocks and stubs
- No test interdependencies

#### 5.2 Test Completeness

**Required Test Types**
- Unit tests for business logic
- Integration tests for component interaction
- Edge case and boundary tests
- Error condition tests
- Security-related tests

**Missing Tests**
- Untested error paths
- Missing negative test cases
- Uncovered edge conditions
- No regression tests for bug fixes

### Phase 6: Documentation Review

#### 6.1 Code Documentation

**Function/Method Documentation**
- Purpose and behavior description
- Parameter descriptions with types
- Return value documentation
- Exception documentation
- Usage examples for complex APIs

**Module/Class Documentation**
- High-level purpose
- Architecture overview
- Design decisions
- Dependencies
- Public API contracts

#### 6.2 External Documentation

**README Updates**
- Installation instructions
- Configuration changes
- New feature documentation
- Breaking change notices
- Migration guides

**API Documentation**
- Endpoint descriptions
- Request/response formats
- Authentication requirements
- Error responses
- Rate limiting

## Review Checklist

Use this checklist to ensure comprehensive review:

### Security
- [ ] No hardcoded credentials or secrets
- [ ] Input validation on all user inputs
- [ ] Proper authentication and authorization
- [ ] No SQL/command injection vulnerabilities
- [ ] Secure password handling
- [ ] HTTPS/TLS for sensitive data
- [ ] Security scanning tools executed
- [ ] Dependencies checked for vulnerabilities

### Code Quality
- [ ] Functions follow Single Responsibility Principle
- [ ] Cyclomatic complexity under 10
- [ ] No code duplication
- [ ] Consistent naming conventions
- [ ] Proper error handling
- [ ] No TODO/FIXME without tickets
- [ ] Code is self-documenting

### Performance
- [ ] No obvious performance bottlenecks
- [ ] Efficient algorithms and data structures
- [ ] Proper resource cleanup
- [ ] Database queries optimized
- [ ] No N+1 query problems
- [ ] Appropriate caching strategies

### Testing
- [ ] Tests included for new functionality
- [ ] Edge cases covered
- [ ] Test coverage meets standards
- [ ] Tests are independent and repeatable
- [ ] No flaky tests introduced

### Documentation
- [ ] Public APIs documented
- [ ] Complex logic explained
- [ ] README updated if needed
- [ ] Breaking changes documented
- [ ] Migration guide provided if needed

## Using the Review Helper Script

The `scripts/review_helper.py` provides automated analysis:

```bash
# Full code review analysis
python scripts/review_helper.py --file path/to/file.py --report full

# Security-focused scan
python scripts/review_helper.py --security-scan path/to/directory

# Complexity analysis
python scripts/review_helper.py --complexity path/to/file.py

# Generate review report
python scripts/review_helper.py --file path/to/file.py --output report.md
```

## Best Practices

### For Reviewers

**Be Constructive**
- Focus on improvement, not criticism
- Explain the "why" behind suggestions
- Offer alternatives or solutions
- Recognize good code and patterns

**Be Thorough but Efficient**
- Use automated tools for mechanical checks
- Focus human review on logic and design
- Don't bikeshed on style issues (use linters)
- Prioritize security and correctness over style

**Be Consistent**
- Apply the same standards to all code
- Reference team coding standards
- Create reusable review templates
- Document common feedback patterns

### For Code Authors

**Prepare for Review**
- Self-review before requesting review
- Run linters and formatters
- Execute test suite
- Add context in PR description
- Keep changes focused and small

**Respond to Feedback**
- Address all comments
- Ask questions if unclear
- Don't take feedback personally
- Mark conversations as resolved

## Common Review Feedback Patterns

### Security Issues
```
❌ Security: Hardcoded API key found
→ Move to environment variable or secrets management
→ See: references/security_patterns.md#secrets-management

❌ Security: SQL injection vulnerability
→ Use parameterized queries instead of string concatenation
→ Example: cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
```

### Quality Issues
```
❌ Quality: Function complexity too high (complexity: 15)
→ Break down into smaller, focused functions
→ Target: < 10 cyclomatic complexity

❌ Quality: Duplicated code across 3 locations
→ Extract common logic into shared function
→ DRY principle violation
```

### Performance Issues
```
❌ Performance: N+1 query problem detected
→ Use JOIN or eager loading instead
→ See: references/performance_guide.md#database-optimization

❌ Performance: Inefficient O(n²) algorithm
→ Consider using set/hash for O(1) lookup
→ Current: nested loops, Suggested: set intersection
```

## Additional Resources

- **Security Patterns**: `references/security_patterns.md` - Common vulnerabilities and fixes
- **Performance Guide**: `references/performance_guide.md` - Optimization strategies
- **Review Checklist**: `examples/review_checklist.md` - Comprehensive review template
- **Helper Scripts**: `scripts/review_helper.py` - Automated analysis tools

## Language-Specific Considerations

### Python
- Check for proper use of context managers (with statements)
- Verify list comprehensions aren't overly complex
- Look for opportunities to use generators
- Check for mutable default arguments

### JavaScript/TypeScript
- Verify proper async/await usage
- Check for callback hell
- Look for memory leaks in event listeners
- Verify proper typing in TypeScript

### Java
- Check for proper exception handling
- Verify resource cleanup (try-with-resources)
- Look for proper use of immutability
- Check for thread safety issues

### Go
- Check for proper error handling (not ignoring errors)
- Verify goroutine leak prevention
- Look for race conditions
- Check for proper context usage

## Conclusion

Effective code review combines automated tooling with human expertise. Use automated tools for mechanical checks (security, style, complexity) and focus human review on logic, design, and maintainability. Always be constructive, thorough, and consistent in your reviews.
