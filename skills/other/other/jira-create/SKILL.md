---
name: jira-create
description: This skill should be used when creating JIRA epics, stories, and tasks from code files or descriptions. It analyzes the provided input, determines the appropriate issue hierarchy, and creates issues with comprehensive quality requirements including test-first development and documentation.
allowed-tools: ["Read", "Glob", "LS", "mcp__atlassian__createJiraIssue", "mcp__atlassian__getVisibleJiraProjects", "mcp__atlassian__getJiraProjectIssueTypesMetadata", "mcp__atlassian__getAccessibleAtlassianResources"]
---

# Create JIRA Issues from $ARGUMENTS

Analyze the provided file(s) and create a comprehensive JIRA hierarchy with all mandatory quality gates.

## Process

1. **Analyze**: Read $ARGUMENTS to understand scope
2. **Determine Structure**:
   - Epic needed if: multiple features, major changes, >3 related files
   - Direct tasks if: bug fix, single file, minor change
3. **Create Issues** with hierarchy:
   ```
   Epic → User Story → Tasks (test, implement, document, cleanup)
   ```

## Mandatory for Every Code Issue

**Test-First**: Write tests before implementation
**Quality Gates**: All tests/checks must pass, no SonarCloud violations
**Documentation**: Check existing, update/create new, remove obsolete
**Cleanup**: Remove temporary code, scripts, dev configs

## Validation Journey

Tickets that change runtime behavior should include a `Validation Journey` section in the description. This section is consumed by the `jira-journey` skill to automate verification.

### When to Include

Include a Validation Journey when the ticket involves:
- API endpoint changes (new, modified, or removed routes)
- Database schema changes (migrations, new columns, index changes)
- Background job or queue processing changes
- Library or utility function changes that affect exports
- Security fixes (authentication, authorization, input validation)
- Performance-critical changes requiring measurement

### When to Skip

Skip the Validation Journey for:
- Documentation-only changes
- Config-only changes (env vars, CI/CD, feature flags with no code)
- Type-definition-only changes (interfaces, types, no runtime effect)

### How to Write

Design the journey based on the **change type**. The agent executing the journey determines how to verify each step using patterns from the project's `verfication.md`. Place `[EVIDENCE: name]` markers at key verification points.

Add this section to the ticket description:

```text
h2. Validation Journey

h3. Prerequisites
- Local dev server running
- Database accessible
- Required environment variables set

h3. Steps
1. Verify the current state before changes
2. Apply the change (run migration, deploy, etc.)
3. Verify the expected new state [EVIDENCE: state-after-change]
4. Test error/edge cases [EVIDENCE: error-handling]
5. Verify rollback or cleanup if applicable [EVIDENCE: rollback-check]

h3. Assertions
- Describe what must be true after verification
- Each assertion is verified against the captured evidence
```

### Guidelines

1. **Steps must be concrete and verifiable** — "Run `curl -s localhost:3000/health`" not "Check the API"
2. **Evidence markers at verification points** — Place `[EVIDENCE: name]` at states that prove the change works. Use descriptive kebab-case names (e.g., `api-response`, `schema-check`, `rate-limit-hit`)
3. **Include 2-5 evidence markers** — Enough to prove the change works across happy path and error cases
4. **Assertions are testable statements** — "Health check returns 200 with status ok" not "API works"
5. **Prerequisites include environment setup** — Database connection, env vars, running services

## Issue Requirements

Each issue must clearly communicate to:

- **Coding Assistants**: Implementation requirements
- **Developers**: Technical approach
- **Stakeholders**: Business value

Default project: from jira-cli config (override via arguments)
Exclude unless requested: migration plans, performance tests

Execute the analysis and create the complete JIRA structure with proper parent-child relationships.
