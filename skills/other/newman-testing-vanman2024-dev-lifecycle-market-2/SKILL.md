---
name: Newman Testing
description: Newman/Postman collection testing patterns for API testing with environment variables, test assertions, and reporting. Use when building API tests, running Newman collections, testing REST APIs, validating HTTP responses, creating Postman collections, configuring API test environments, generating test reports, or when user mentions Newman, Postman, API testing, collection runner, integration tests, API validation, test automation, or CI/CD API testing.
---

# Newman Testing

**CRITICAL: The description field above controls when Claude auto-loads this skill.**

## Overview

Provides comprehensive patterns, templates, and scripts for Newman/Postman API testing including collection structure, environment management, test assertions, reporting, and CI/CD integration.

## Instructions

### 1. Collection Structure and Organization

**Understand Collection Architecture:**
- Organize requests into logical folders (auth, users, products, etc.)
- Use pre-request scripts for setup (tokens, dynamic data)
- Use test scripts for assertions and validation
- Leverage collection-level variables and scripts

**Create Collections:**
1. Use `scripts/init-collection.sh` to scaffold new collection structure
2. Use templates to create well-structured requests
3. Follow naming conventions (verb + resource: GET Users, POST Product)
4. Group related endpoints into folders

### 2. Environment Variable Management

**Setup Environments:**
1. Use `scripts/setup-environment.sh` to create environment files
2. Define variables for different deployment stages (dev, staging, prod)
3. Store sensitive data in environment files (not in collections)
4. Use dynamic variables for timestamps, UUIDs, random data

**Variable Hierarchy:**
- Global variables: Shared across all collections
- Environment variables: Environment-specific (URLs, credentials)
- Collection variables: Collection-specific configuration
- Local variables: Request/script-specific temporary data

### 3. Test Assertion Patterns

**Write Effective Tests:**
1. Reference `templates/test-assertions-basic.js` for common patterns
2. Reference `templates/test-assertions-advanced.js` for complex validations
3. Test status codes, response times, headers, body content
4. Chain requests using `pm.environment.set()` for dynamic workflows

**Test Organization:**
- Status code validation (200, 201, 400, 401, 404, 500)
- Response structure validation (schema, required fields)
- Data validation (types, formats, ranges)
- Business logic validation (calculations, relationships)

### 4. Running Newman Tests

**Execute Collections:**
1. Use `scripts/run-newman.sh` for basic execution
2. Use `scripts/run-newman-ci.sh` for CI/CD pipeline integration
3. Specify environment files with `-e` flag
4. Generate reports with reporters (cli, json, html, junit)

**Common Execution Patterns:**
```bash
# Run with environment
bash scripts/run-newman.sh collection.json -e env.json

# Run with multiple reporters
bash scripts/run-newman.sh collection.json --reporters cli,json,html

# Run in CI/CD with junit output
bash scripts/run-newman-ci.sh collection.json -e ci-env.json
```

### 5. Reporting and Output

**Generate Reports:**
1. Use `scripts/generate-reports.sh` for comprehensive reporting
2. Configure multiple reporters (HTML for humans, JUnit for CI)
3. Parse JSON output for custom analysis
4. Track test results over time

**Available Report Formats:**
- **CLI**: Console output for quick feedback
- **JSON**: Machine-readable for analysis
- **HTML**: Visual reports with charts
- **JUnit**: CI/CD integration (Jenkins, GitLab, GitHub Actions)
- **TeamCity**: TeamCity-specific format

### 6. CI/CD Integration

**Pipeline Integration:**
1. Reference `examples/github-actions-integration.md` for GitHub Actions
2. Reference `examples/gitlab-ci-integration.md` for GitLab CI
3. Install Newman as part of build process
4. Run tests as separate pipeline stage
5. Parse results and fail builds on test failures

**Best Practices:**
- Use environment variables for secrets
- Run Newman in Docker containers for consistency
- Cache Newman installation for faster builds
- Archive test reports as build artifacts

### 7. Error Handling and Debugging

**Debugging Tests:**
1. Use `console.log()` in pre-request/test scripts
2. Enable verbose output with `--verbose` flag
3. Use `--delay-request` to troubleshoot race conditions
4. Export newman run data with `--export-*` flags

**Common Issues:**
- Authentication failures: Check token refresh logic
- Timing issues: Use `pm.test()` with delays
- Environment mismatch: Verify environment file loaded
- SSL errors: Use `--insecure` flag for self-signed certs

## Available Scripts

1. **init-collection.sh**: Initialize new Postman collection structure with folders and basic requests
2. **setup-environment.sh**: Create environment JSON files with variable templates
3. **run-newman.sh**: Execute Newman collections with various options and reporters
4. **run-newman-ci.sh**: CI/CD-optimized Newman execution with proper exit codes and reporting
5. **generate-reports.sh**: Generate comprehensive test reports in multiple formats

## Available Templates

1. **collection-basic.json**: Basic collection structure with folders and sample requests
2. **collection-advanced.json**: Advanced collection with auth, pre-request scripts, and test chains
3. **environment-template.json**: Environment file template with common variables
4. **test-assertions-basic.js**: Common test assertion patterns (status, headers, body)
5. **test-assertions-advanced.js**: Advanced assertions (schema validation, chaining, conditional tests)
6. **pre-request-scripts.js**: Pre-request script patterns (auth tokens, dynamic data, setup)

## Available Examples

1. **basic-usage.md**: Simple Newman execution with single collection and environment
2. **advanced-testing.md**: Complex test scenarios with chaining, data-driven tests, and workflows
3. **github-actions-integration.md**: Complete GitHub Actions workflow for Newman testing
4. **gitlab-ci-integration.md**: GitLab CI configuration for automated API testing
5. **error-handling-debugging.md**: Common errors, troubleshooting steps, and debugging techniques

## Requirements

- Newman CLI installed (`npm install -g newman`)
- Valid Postman collection JSON files
- Environment files for different stages
- Proper variable management (no hardcoded secrets)
- Clear test descriptions and assertions
- CI/CD integration following best practices

## Progressive Disclosure

For additional reference material:
- Read `examples/basic-usage.md` for quick start
- Read `examples/advanced-testing.md` for complex scenarios
- Read `examples/github-actions-integration.md` or `examples/gitlab-ci-integration.md` for CI/CD setup
- Read `examples/error-handling-debugging.md` when troubleshooting

---

**Skill Location**: plugins/05-quality/skills/newman-testing/SKILL.md
**Version**: 1.0.0
