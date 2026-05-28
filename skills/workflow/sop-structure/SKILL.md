---
name: sop-structure
description: Use when structuring Standard Operating Procedures with proper sections, organization, and markdown formatting. Covers SOP anatomy and section organization.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# SOP Structure

Well-structured SOPs follow consistent patterns that make them easy to understand, maintain, and execute. This skill covers the anatomy of effective SOPs and how to organize sections.

## Key Concepts

### Standard SOP Anatomy

Every SOP should include these core sections:

1. **Title**: Clear, action-oriented description
2. **Overview**: Brief summary of purpose and use cases
3. **Parameters**: Configurable inputs for reusability
4. **Prerequisites**: Required tools, knowledge, or setup
5. **Steps**: Sequential instructions for execution
6. **Success Criteria**: How to verify completion
7. **Error Handling**: What to do when things go wrong
8. **Related SOPs**: Links to related workflows

### File Naming Convention

SOP files MUST use the `.sop.md` extension:

```
✅ deployment-checklist.sop.md
✅ code-review-security.sop.md
✅ database-migration.sop.md

❌ deployment.md (missing .sop)
❌ checklist.sop.txt (wrong file type)
❌ SOP-Deployment.md (incorrect format)
```

## Best Practices

### Title Section

```markdown
# {Action Verb} {Specific Outcome}

Short form: Use kebab-case filename
Long form: Use Title Case heading
```

**Examples:**

```markdown
# Generate API Documentation

# Implement Feature Using TDD

# Review Pull Request for Security
```

### Overview Section

The overview should answer three questions:

1. **What**: What does this SOP accomplish?
2. **When**: When should you use this SOP?
3. **Why**: Why use this approach?

```markdown
## Overview

This SOP guides you through implementing new features using Test-Driven
Development (TDD). Use this when adding functionality that requires high
confidence in correctness. TDD ensures comprehensive test coverage and
reduces regression risk.
```

### Parameters Section

Define all configurable inputs at the beginning:

```markdown
## Parameters

- **Input Variable**: {variable_name} - Description and example values
- **Configuration**: {config_option} - Available options (option1, option2, option3)
- **Path**: {file_path} - Expected format and constraints
```

**Example:**

```markdown
## Parameters

- **Repository Path**: {repository_path} - Absolute path to git repository
- **Output Format**: {output_format} - Documentation format (markdown, html, pdf)
- **Verbosity**: {verbosity} - Detail level (concise, standard, comprehensive)
- **Include Tests**: {include_tests} - Whether to include test examples (yes, no)
```

### Prerequisites Section

List required tools, knowledge, and setup:

```markdown
## Prerequisites

### Required Tools
- Tool name (version X.X or higher)
- Another tool (version Y.Y or higher)

### Required Knowledge
- Understanding of concept A
- Familiarity with technology B

### Required Setup
- Environment variable {VAR_NAME} must be set
- Configuration file {config.json} must exist
```

**Example:**

```markdown
## Prerequisites

### Required Tools
- Node.js (v18 or higher)
- npm (v8 or higher)
- Git (v2.30 or higher)

### Required Knowledge
- Understanding of JavaScript/TypeScript
- Familiarity with testing frameworks
- Git workflow basics

### Required Setup
- Package.json exists in project root
- Test framework is installed (Jest, Vitest, or Mocha)
- Git repository is initialized
```

### Steps Section

Structure steps hierarchically:

```markdown
## Steps

1. First major step
   - Sub-step or detail
   - Another sub-step
   - Additional context

2. Second major step
   - Implementation detail
   - Expected outcome

3. Third major step
   - Specific action
   - Validation step
```

**With Validation:**

```markdown
## Steps

1. Analyze codebase structure
   - Identify main entry points
   - Map directory organization
   - List dependencies
   - **Validation**: Confirm all entry points are documented

2. Extract patterns
   - Identify design patterns
   - Document data flow
   - Note architectural decisions
   - **Validation**: Verify patterns are correctly identified

3. Generate documentation
   - Create overview section
   - Document public APIs
   - Add usage examples
   - **Validation**: Ensure documentation builds without errors
```

### Success Criteria Section

Define measurable outcomes:

```markdown
## Success Criteria

- [ ] Specific measurable outcome 1
- [ ] Specific measurable outcome 2
- [ ] Specific measurable outcome 3
- [ ] All tests pass
- [ ] Documentation is complete
```

**Example:**

```markdown
## Success Criteria

- [ ] All new code has test coverage ≥ 90%
- [ ] All tests pass without warnings
- [ ] Code passes linter with zero errors
- [ ] Documentation includes usage examples
- [ ] Changes follow existing code patterns
```

### Error Handling Section

Provide guidance for common failures:

```markdown
## Error Handling

### Error: {Error Name or Code}

**Symptoms**: How this error manifests

**Cause**: Why this error occurs

**Resolution**:
1. First troubleshooting step
2. Second troubleshooting step
3. Alternative approach if steps fail
```

**Example:**

```markdown
## Error Handling

### Error: Tests Fail to Run

**Symptoms**: Test runner exits with error code, tests don't execute

**Cause**: Missing dependencies, incorrect test framework configuration, or environment issues

**Resolution**:
1. Verify test framework is installed: `npm list {test-framework}`
2. Check test configuration file exists and is valid
3. Ensure NODE_ENV is set correctly
4. If issue persists, reinstall dependencies: `rm -rf node_modules && npm install`

### Error: Type Errors During Build

**Symptoms**: TypeScript compiler reports type mismatches

**Cause**: Incorrect type annotations or missing type definitions

**Resolution**:
1. Run type checker: `npx -y --package typescript tsc`
2. Review error messages for specific type issues
3. Add necessary type annotations
4. Install missing @types packages if needed
```

### Related SOPs Section

Link to related workflows:

```markdown
## Related SOPs

- **{sop-name}**: Brief description of when to use this instead
- **{another-sop}**: How this complements the current SOP
```

**Example:**

```markdown
## Related SOPs

- **code-review**: Use after completing feature implementation to get peer review
- **deployment-checklist**: Use after code review passes to deploy changes
- **rollback-procedure**: Use if deployment fails or issues are discovered
```

## Examples

### Complete SOP Structure Example

```markdown
# Deploy Application to Production

## Overview

This SOP guides you through deploying application changes to production
environment safely. Use this after code review approval and successful
staging deployment. This ensures consistent deployment process and reduces
production incidents.

## Parameters

- **Environment**: {environment} - Target environment (staging, production)
- **Version**: {version} - Semantic version number (e.g., 1.2.3)
- **Rollback Plan**: {rollback_plan} - Strategy if deployment fails (automatic, manual)

## Prerequisites

### Required Tools
- kubectl (v1.24 or higher)
- Docker (v20.10 or higher)
- AWS CLI (v2.0 or higher)

### Required Knowledge
- Understanding of Kubernetes deployments
- Familiarity with application architecture
- Access to production monitoring dashboards

### Required Setup
- Production credentials configured in ~/.kube/config
- Docker registry authentication set up
- Monitoring alerts configured

## Steps

1. Pre-deployment verification
   - Verify {version} passed all staging tests
   - Confirm database migrations are ready
   - Check rollback procedures are documented
   - **Validation**: All tests passed, migrations reviewed

2. Build and push container image
   - Build Docker image with tag {version}
   - Run security scan on image
   - Push to container registry
   - **Validation**: Image pushed successfully, no critical vulnerabilities

3. Apply database migrations
   - Backup production database
   - Test migrations on backup
   - Apply migrations to production
   - **Validation**: Migrations applied, database accessible

4. Deploy application
   - Update Kubernetes deployment with new image
   - Monitor pod startup and health checks
   - Verify application responds correctly
   - **Validation**: All pods healthy, health checks passing

5. Post-deployment verification
   - Run smoke tests on production
   - Check error rates in monitoring
   - Verify key functionality works
   - Monitor for 15 minutes
   - **Validation**: Error rate normal, smoke tests pass

## Success Criteria

- [ ] Application version {version} is deployed
- [ ] All health checks passing
- [ ] Error rate within normal range
- [ ] Database migrations applied successfully
- [ ] Monitoring shows no anomalies
- [ ] Key user flows tested and working

## Error Handling

### Error: Pod Fails to Start

**Symptoms**: Pods stuck in CrashLoopBackOff, not reaching Ready state

**Cause**: Configuration error, resource limits, or dependency unavailability

**Resolution**:
1. Check pod logs: `kubectl logs -n production <pod-name>`
2. Describe pod for events: `kubectl describe pod -n production <pod-name>`
3. Verify configuration matches staging
4. If unresolvable, execute rollback plan

### Error: Health Checks Failing

**Symptoms**: Load balancer removes pods from rotation, service degraded

**Cause**: Application startup issues, database connectivity, or resource exhaustion

**Resolution**:
1. Check application logs for errors
2. Verify database connectivity
3. Check resource utilization
4. Scale up resources if needed
5. If unresolvable within 5 minutes, execute rollback plan

### Error: High Error Rate After Deployment

**Symptoms**: Monitoring shows spike in 500 errors, increased latency

**Cause**: Breaking changes, incompatible dependency, or configuration mismatch

**Resolution**:
1. Immediately execute {rollback_plan}
2. Capture error logs for analysis
3. Test fix in staging environment
4. Schedule new deployment after fix verified

## Related SOPs

- **rollback-procedure**: Execute if deployment fails or critical issues arise
- **database-migration**: Detailed process for database schema changes
- **incident-response**: Follow if deployment causes production incident
- **staging-deployment**: Complete before production deployment
```

## Common Patterns

### Template for Code Analysis SOP

```markdown
# {Analyze|Review|Audit} {Target} for {Quality Aspect}

## Overview
{1-2 sentences: what, when, why}

## Parameters
- **Target**: {target} - What to analyze
- **Depth**: {depth} - Analysis thoroughness
- **Output Format**: {format} - Result format

## Prerequisites
{Tools, knowledge, setup required}

## Steps
1. Identify scope and boundaries
2. Gather relevant information
3. Perform analysis
4. Document findings
5. Generate recommendations

## Success Criteria
- [ ] Analysis complete for all areas
- [ ] Findings documented with examples
- [ ] Recommendations are actionable

## Error Handling
{Common issues and resolutions}

## Related SOPs
{Complementary workflows}
```

### Template for Implementation SOP

```markdown
# Implement {Feature} Using {Methodology}

## Overview
{1-2 sentences: what, when, why}

## Parameters
- **Feature Description**: {description}
- **Framework**: {framework}
- **Test Coverage**: {coverage}

## Prerequisites
{Tools, knowledge, setup required}

## Steps
1. Design feature interface
2. Create tests
3. Implement functionality
4. Refactor and optimize
5. Document changes

## Success Criteria
- [ ] Feature meets requirements
- [ ] Tests pass with coverage ≥ {coverage}
- [ ] Documentation updated

## Error Handling
{Common issues and resolutions}

## Related SOPs
{Complementary workflows}
```

## Anti-Patterns

**Avoid These Structure Mistakes:**

1. **Missing Parameters**
   - ❌ Hard-coding values in steps
   - ✅ Define parameters at the beginning

2. **Unclear Prerequisites**
   - ❌ Assuming tools are installed
   - ✅ Explicitly list required tools and versions

3. **Vague Success Criteria**
   - ❌ "Code should be good quality"
   - ✅ "Code passes linter with 0 errors and has test coverage ≥ 80%"

4. **No Error Handling**
   - ❌ Only describing happy path
   - ✅ Including common failures and resolutions

5. **Poor Section Organization**
   - ❌ Steps before parameters, success criteria mixed with steps
   - ✅ Consistent section order: Overview → Parameters → Prerequisites → Steps → Success Criteria → Error Handling

## Related Skills

- **sop-authoring**: Learn to write clear, actionable instructions
- **sop-rfc2119**: Use RFC 2119 keywords for precise requirements
- **sop-maintenance**: Keep SOPs current and relevant
