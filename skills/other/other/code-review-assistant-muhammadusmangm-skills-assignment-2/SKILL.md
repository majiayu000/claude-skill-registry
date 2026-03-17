---
name: code-review-assistant
description: Automated code review assistance including best practices evaluation, security vulnerability detection, performance optimization suggestions, code quality assessment, and style guide enforcement. Use when Claude needs to perform code reviews, assess code quality, identify potential issues, or provide improvement recommendations.
---

# Code Review Assistant

## Overview
This skill provides comprehensive code review capabilities to evaluate code quality, identify issues, and suggest improvements across multiple programming languages.

## When to Use This Skill
- Performing systematic code reviews
- Assessing code quality and maintainability
- Identifying potential security vulnerabilities
- Evaluating performance implications
- Ensuring adherence to coding standards
- Providing constructive feedback to developers

## Review Categories

### Code Quality
- Readability and maintainability
- Proper function/method length
- Meaningful variable and function names
- Appropriate level of abstraction
- DRY (Don't Repeat Yourself) principles

### Security Considerations
- Input validation and sanitization
- SQL injection prevention
- Cross-site scripting (XSS) protection
- Authentication and authorization
- Data encryption and privacy
- Dependency security

### Performance
- Algorithmic complexity
- Memory usage optimization
- Database query efficiency
- Caching strategies
- Resource management
- Asynchronous operations

### Best Practices
- Error handling and logging
- Proper exception management
- Code documentation and comments
- Testing coverage and quality
- Configuration management

## Review Process

### 1. Architecture & Design
- Evaluate overall structure
- Check for separation of concerns
- Assess scalability considerations
- Verify design pattern usage

### 2. Code Implementation
- Review logic correctness
- Check for edge cases
- Validate error handling
- Assess resource management

### 3. Security Assessment
- Identify potential vulnerabilities
- Check authentication/authorization
- Verify data validation
- Review dependency security

### 4. Performance Analysis
- Evaluate algorithm efficiency
- Check for memory leaks
- Assess database queries
- Review caching strategies

### 5. Maintainability
- Check code readability
- Assess documentation quality
- Verify test coverage
- Review naming conventions

## Feedback Guidelines
- Be specific and actionable
- Provide positive reinforcement
- Suggest alternatives when appropriate
- Prioritize issues by severity
- Reference relevant documentation

## Severity Levels
- Critical: Security vulnerability, data loss risk
- High: Functional defect, major performance issue
- Medium: Potential bug, maintainability concern
- Low: Style issue, minor improvement suggestion

## Scripts Available
- `scripts/run-security-check.js` - Security vulnerability scan
- `scripts/performance-analyzer.js` - Performance assessment
- `scripts/style-checker.js` - Coding style verification
- `scripts/test-coverage.js` - Coverage analysis

## References
- `references/security-checklist.md` - Comprehensive security checklist for code reviews
- `references/performance-guidelines.md` - Performance optimization guidelines and best practices