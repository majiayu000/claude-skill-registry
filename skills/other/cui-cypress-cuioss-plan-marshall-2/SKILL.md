---
name: cui-cypress
description: Cypress E2E testing standards including framework adaptations, test organization, and best practices
user-invocable: false
allowed-tools: Read, Grep, Glob
requirements:
  - Modern JavaScript knowledge
  - Understanding of E2E testing concepts
  - Familiarity with test automation patterns
standards:
  - cypress-configuration.md
  - test-organization.md
  - testing-patterns.md
  - console-monitoring.md
  - build-integration.md
---

# Cypress E2E Testing Standards Skill

**REFERENCE MODE**: This skill provides reference material. Load specific standards on-demand based on current task.

## Overview

This skill provides comprehensive standards for Cypress End-to-End (E2E) testing in CUI projects. It extends base JavaScript testing standards with framework-specific adaptations designed for browser-based test automation scenarios.

## What This Skill Provides

**Framework Configuration:**
- ESLint configuration adapted for Cypress testing contexts
- Complexity thresholds adjusted for E2E test scenarios
- Plugin integration for Cypress-specific rules

**Test Organization:**
- Directory structure and file naming conventions
- Custom command patterns for reusable test logic
- Constants organization using DSL-style patterns
- Test isolation and session management strategies

**Quality Standards:**
- Console error monitoring and zero-error policy
- Allowed warnings system for third-party libraries
- Test reliability and stability requirements
- Performance optimization patterns

**Best Practices:**
- No branching logic in tests (mandatory)
- Explicit assertions over conditional checks
- Session management for test isolation
- Navigation patterns and page type verification
- Modern Cypress patterns (cy.session, custom commands)

**Build Integration:**
- NPM scripts configuration
- Maven integration patterns
- CI/CD pipeline considerations

## When to Activate

Activate this skill when:
- Implementing Cypress E2E tests in CUI projects
- Configuring Cypress testing infrastructure
- Creating custom commands or test utilities
- Reviewing or refactoring existing E2E test suites
- Troubleshooting test reliability issues
- Integrating E2E tests with build systems

## Workflow

### 1. Initial Setup
- Review `cypress-configuration.md` for ESLint and framework setup
- Apply `build-integration.md` for Maven and NPM integration
- Implement `console-monitoring.md` patterns for error tracking

### 2. Test Development
- Follow `test-organization.md` for file structure and naming
- Apply `testing-patterns.md` for custom commands and reusable logic
- Use DSL-style constants for selectors and test data

### 3. Quality Assurance
- Enforce no-branching-logic rule in all tests
- Implement console error monitoring
- Verify session management and test isolation
- Apply performance optimization patterns

### 4. Maintenance
- Keep custom commands updated with application changes
- Validate test reliability in CI/CD environment
- Review and update allowed warnings list as needed

## Standards Organization

### Core Configuration
**cypress-configuration.md** - ESLint setup, complexity adaptations, global configuration

### Test Structure
**test-organization.md** - Directory layout, file naming, constants organization, custom commands

### Testing Patterns
**testing-patterns.md** - Best practices, session management, navigation patterns, error handling, anti-patterns

### Quality Monitoring
**console-monitoring.md** - Zero-error policy, allowed warnings system, error tracking implementation

### Build System
**build-integration.md** - NPM scripts, Maven integration, CI/CD pipeline setup, dependency management

## Tool Access

This skill requires:
- Read access to project files for analysis
- Write access for creating/updating test files and configuration
- Bash access for running Cypress commands and build tools
- Grep/Glob for searching existing test patterns

## Integration with Other Skills

This skill builds upon:
- **cui-javascript**: Base JavaScript standards and modern patterns
- **cui-javascript-linting**: ESLint configuration foundation
- **cui-javascript-unit-testing**: Shared testing concepts and patterns
- **cui-javascript-project**: Project structure and dependency management

## Critical Rules

**Mandatory:**
- No branching logic (`if/else`, `switch`, ternary) in tests
- Use navigation helpers instead of direct `cy.visit()` or `cy.url()`
- Always verify session context after authentication
- Implement console error monitoring in all test suites

**Prohibited:**
- `cy.wait()` with fixed timeouts
- Element existence checks in test logic
- Manual session clearing without helpers
- Direct URL manipulation

## Success Criteria

Tests following these standards will:
- Execute reliably in CI/CD environments
- Provide clear failure diagnostics
- Complete within reasonable timeframes
- Maintain clean session isolation
- Detect console errors and warnings
- Use consistent, maintainable patterns
