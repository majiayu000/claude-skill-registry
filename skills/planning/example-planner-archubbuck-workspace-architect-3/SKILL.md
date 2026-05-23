---
name: example-planner
description: Create detailed implementation plans for software features and refactoring tasks. Use this skill when planning new features, architectural changes, or major refactoring efforts.
license: MIT
metadata:
  version: "1.0.0"
  maintainer: "workspace-architect"
  category: "planning"
---

# Example Planner Skill

This is an example skill that demonstrates the Claude Skills format for workspace-architect.

## Purpose

Use this skill when you need to create a comprehensive implementation plan for:
- New feature development
- Code refactoring
- Architecture changes
- Technical debt reduction

## Instructions

When activated, follow these steps:

1. **Gather Requirements**
   - Ask clarifying questions about the feature or change
   - Understand constraints (time, resources, dependencies)
   - Identify stakeholders and their needs

2. **Analyze Current State**
   - Review existing codebase architecture
   - Identify impacted components
   - List technical dependencies
   - Note potential risks

3. **Design Solution**
   - Propose architectural approach
   - Break down into implementable tasks
   - Define acceptance criteria
   - Estimate effort for each task

4. **Create Implementation Plan**
   Generate a plan with these sections:

   ### Overview
   - Brief summary of the feature/change
   - Key objectives and goals
   
   ### Requirements
   - Functional requirements
   - Non-functional requirements (performance, security, etc.)
   - Constraints and dependencies
   
   ### Architecture
   - High-level design
   - Component interactions
   - Data flow
   
   ### Implementation Steps
   Detailed task breakdown with:
   - Task description
   - Dependencies
   - Estimated effort
   - Assignee (if known)
   
   ### Testing Strategy
   - Unit tests
   - Integration tests
   - E2E tests
   - Performance tests
   
   ### Risks and Mitigations
   - Technical risks
   - Timeline risks
   - Dependency risks
   - Mitigation strategies
   
   ### Success Criteria
   - How to measure completion
   - Acceptance criteria
   - Quality metrics

5. **Review and Iterate**
   - Ask for feedback on the plan
   - Refine based on input
   - Update as requirements evolve

## Best Practices

- Break large features into smaller, reviewable chunks
- Include time estimates (optimistic, realistic, pessimistic)
- Identify and document assumptions
- Consider backward compatibility
- Plan for rollback if needed
- Document decision rationale

## Output Format

Use clear Markdown formatting with:
- Numbered lists for sequential steps
- Bullet points for parallel tasks
- Code blocks for technical details
- Tables for task breakdowns
- Diagrams (ASCII or Mermaid) when helpful

## Example Output

```markdown
# Implementation Plan: User Authentication

## Overview
Add OAuth 2.0 authentication to the application, supporting Google and GitHub providers.

## Requirements

### Functional
- Users can sign in with Google or GitHub
- Session management with JWT tokens
- Logout functionality
- Remember me option

### Non-Functional
- Response time < 2s for auth flow
- 99.9% uptime for auth service
- GDPR compliant data handling

## Implementation Steps

1. **Setup OAuth Providers** (4 hours)
   - Register apps with Google/GitHub
   - Configure OAuth credentials
   - Store secrets securely

2. **Backend Implementation** (16 hours)
   - Create OAuth callback endpoints
   - Implement JWT token generation
   - Add session middleware
   - Write unit tests

3. **Frontend Implementation** (12 hours)
   - Add login buttons
   - Handle OAuth redirects
   - Store tokens securely
   - Implement logout

...
```

## Related Resources

- [Software Planning Best Practices](https://example.com/planning)
- [Architecture Decision Records](https://adr.github.io/)
- [Task Estimation Techniques](https://example.com/estimation)

## Notes

- Adjust detail level based on project size
- For small tasks, a lightweight plan is sufficient
- For large projects, consider creating ADRs for major decisions
- Keep the plan as a living document, updated as work progresses
