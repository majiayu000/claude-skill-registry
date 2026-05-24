---
name: feature-dev
description: Feature development workflow with exploration, architecture, implementation, and review phases. Use for implementing new features or significant changes.
dependencies:
  - deep-analysis
  - architecture-patterns
  - language-patterns
  - technical-diagrams
  - code-quality
  - changelog-format
---

# Feature Development Workflow

Execute a structured 7-phase feature development workflow. This workflow guides you through understanding, exploring, designing, implementing, and reviewing a feature.

## Phase Overview

Execute these phases in order, completing all of them:

1. **Discovery** - Understand the feature requirements
2. **Codebase Exploration** - Map relevant code areas
3. **Clarifying Questions** - Resolve ambiguities
4. **Architecture Design** - Design the implementation approach
5. **Implementation** - Build the feature
6. **Quality Review** - Review for issues
7. **Summary** - Document accomplishments

---

## Phase 1: Discovery

**Goal:** Understand what the user wants to build.

1. Analyze the feature description from `$ARGUMENTS`:
   - What is the core functionality?
   - What are the expected inputs and outputs?
   - Are there any constraints mentioned?
   - What success criteria can you infer?

2. Summarize your understanding to the user. Prompt the user to confirm if your understanding is correct before proceeding.

---

## Phase 2: Codebase Exploration

**Goal:** Understand the relevant parts of the codebase.

1. **Run deep-analysis workflow:**
   - Refer to the **deep-analysis** skill for the exploration and synthesis workflow.
   - Pass the feature description from Phase 1 as the analysis context.
   - This handles reconnaissance, team planning, parallel exploration, and synthesis.

2. Present the synthesized analysis to the user.

---

## Phase 3: Clarifying Questions

**Goal:** Resolve any ambiguities before designing.

1. Review the feature requirements and exploration findings.

2. Identify underspecified aspects:
   - Edge cases not covered
   - Technical decisions that could go multiple ways
   - Integration points that need clarification
   - Performance or scale requirements

3. **Ask clarifying questions:**
   Prompt the user to answer critical unknowns. Only ask questions that would significantly impact the implementation.

   If no clarifying questions are needed, inform the user and proceed.

---

## Phase 4: Architecture Design

**Goal:** Design the implementation approach.

1. **Load skills for this phase:**
   - Refer to the **architecture-patterns**, **language-patterns**, and **technical-diagrams** skills and apply their guidance for any Mermaid diagrams in architecture proposals.

2. **Delegate to 2-3 independent architecture agents to design different approaches:**

   ```
   Agent 1: Design a minimal, focused approach prioritizing simplicity
   Agent 2: Design a flexible, extensible approach prioritizing future changes
   Agent 3: Design an approach optimized for the project's existing patterns (if applicable)
   ```

   Each agent should receive:
   ```
   Feature: [feature description]
   Design approach: [specific approach for this agent]

   Based on the codebase exploration:
   [Summary of relevant files and patterns]

   Design an implementation that:
   - Lists files to create/modify
   - Describes the changes needed in each file
   - Explains the data flow
   - Identifies risks and mitigations

   Return a detailed implementation blueprint.
   ```

3. **Present approaches:**
   - Summarize each approach
   - Compare trade-offs (simplicity, flexibility, performance, maintainability)
   - Make a recommendation with justification

4. **User chooses approach:**
   Prompt the user to choose:
   - Select an approach as-is
   - Request modifications to an approach

5. **Generate ADR artifact:**
   - Use the ADR template below
   - Create an ADR documenting:
     - Context: Why this feature is needed
     - Decision: The chosen approach
     - Consequences: Trade-offs and implications
     - Alternatives: Other approaches considered
   - Determine the next ADR number by checking existing files in `internal/docs/adr/`
   - Save to `internal/docs/adr/NNNN-[feature-slug].md` (create `internal/docs/adr/` if needed)
   - Inform the user of the saved ADR location

---

## Phase 5: Implementation

**Goal:** Build the feature.

1. **Require explicit approval:**
   Ask the user: "Ready to begin implementation of [feature] using [chosen approach]?"
   Wait for confirmation before proceeding.

2. **Read all relevant files:**
   Before making any changes, read the complete content of every file you will modify.

3. **Implement the feature:**
   - Follow the chosen architecture design
   - Match existing code patterns and conventions
   - Create new files as needed
   - Modify existing files with targeted edits
   - Add appropriate error handling
   - Include inline comments only where logic is not obvious

4. **Test if applicable:**
   - If the project has tests, add tests for the new functionality
   - Run existing tests to ensure nothing broke

5. Proceed immediately to Phase 6.

---

## Phase 6: Quality Review

**Goal:** Review the implementation for issues.

1. **Load skills for this phase:**
   - Refer to the **code-quality** skill and apply its guidance.

2. **Delegate to 3 independent review agents with different focuses (correctness, security, maintainability):**

   ```
   Agent 1: Review for correctness and edge cases
   Agent 2: Review for security and error handling
   Agent 3: Review for maintainability and code quality
   ```

   Each agent should receive:
   ```
   Review focus: [specific focus for this agent]

   Files to review:
   [List of files modified/created]

   Review the implementation and report:
   - Issues found with confidence scores (0-100)
   - Suggestions for improvement
   - Positive observations

   Only report issues with confidence >= 80.
   ```

3. **Aggregate findings:**
   - Collect results from all reviewers
   - Deduplicate similar issues
   - Prioritize by severity and confidence

4. **Present findings:**
   Show the user:
   - Critical issues (must fix)
   - Moderate issues (should fix)
   - Minor suggestions (nice to have)

5. **User decides:**
   Prompt the user to choose:
   - Fix all issues now
   - Fix critical issues only
   - Proceed without fixes
   - I will fix manually later

6. If fixing: make the changes and re-review if needed.

7. Proceed immediately to Phase 7.

---

## Phase 7: Summary

**Goal:** Document and celebrate accomplishments.

1. **Summarize accomplishments:**
   Present to the user:
   - What was built
   - Key files created/modified
   - Architecture decisions made
   - Architecture diagram (Mermaid flowchart showing the implemented structure)
   - Any known limitations or future work

2. **Update CHANGELOG.md:**
   - Use the changelog entry template below
   - Refer to the **changelog-format** skill for Keep a Changelog guidelines
   - Create an entry under the `[Unreleased]` section with:
     - Appropriate category (Added, Changed, Fixed, etc.)
     - Concise description of the feature
   - If `CHANGELOG.md` does not exist, create it with proper header
   - Add the entry to the appropriate section under `[Unreleased]`
   - Inform the user of the update

3. **Final message:**
   Congratulate the user and offer next steps:
   - Commit the changes
   - Create a PR
   - Additional testing suggestions

---

## Error Handling

If any phase fails:
1. Explain what went wrong
2. Prompt the user to choose:
   - Retry the phase
   - Skip to next phase
   - Abort the workflow

---

## Agent Coordination

When launching parallel agents (architecture agents, review agents):
- Give each agent a distinct focus area
- Wait for all agents to complete before proceeding
- Handle agent failures gracefully (continue with partial results)

---

## ADR Template

Use this template when generating Architecture Decision Records in Phase 4.

### Template

```markdown
# ADR-NNNN: [Title]

**Date:** YYYY-MM-DD
**Status:** Accepted
**Feature:** [Feature name/description]

## Context

[Describe the situation that led to this decision. Include:]
- What problem are we solving?
- What constraints do we have?
- What are the driving forces?

## Decision

[State the decision clearly and concisely. Include:]
- What approach are we taking?
- Key architectural choices made
- Technologies/patterns selected

## Consequences

### Positive
- [Benefit 1]
- [Benefit 2]
- [Benefit 3]

### Negative
- [Tradeoff 1]
- [Tradeoff 2]

### Risks
- [Risk 1 and mitigation]
- [Risk 2 and mitigation]

## Alternatives Considered

### Alternative 1: [Name]
[Brief description]
- **Pros:** [List]
- **Cons:** [List]
- **Why rejected:** [Reason]

### Alternative 2: [Name]
[Brief description]
- **Pros:** [List]
- **Cons:** [List]
- **Why rejected:** [Reason]

## Implementation Notes

[Any specific implementation guidance:]
- Key files to create/modify
- Important patterns to follow
- Integration points

## References

- [Link to related docs]
- [Link to similar implementations]
```

### Usage Instructions

1. **Determine ADR number:**
   - Check existing files in `internal/docs/adr/`
   - Use the next sequential number (e.g., 0001, 0002)
   - If no ADRs exist, start with 0001

2. **Create filename:**
   - Format: `NNNN-feature-slug.md`
   - Use kebab-case for the slug
   - Example: `0003-user-authentication.md`

3. **Fill in the template:**
   - Be specific about the context
   - State the decision clearly
   - List real consequences (not just benefits)
   - Document alternatives that were considered

4. **Save location:**
   - Create `internal/docs/adr/` directory if it does not exist
   - Save the ADR to that directory

### Example ADR

```markdown
# ADR-0003: User Authentication with JWT

**Date:** 2024-01-15
**Status:** Accepted
**Feature:** User login and session management

## Context

The application needs user authentication. Users should be able to log in and maintain sessions across page refreshes. The API is stateless and serves both web and mobile clients.

Key constraints:
- Must work with stateless API
- Must support multiple clients
- Session should persist across browser refreshes
- Need to handle token refresh gracefully

## Decision

We will use JWT (JSON Web Tokens) for authentication with the following approach:
- Access tokens with 15-minute expiry
- Refresh tokens with 7-day expiry stored in httpOnly cookies
- Token refresh handled automatically by API client interceptor

## Consequences

### Positive
- Stateless authentication scales horizontally
- Works seamlessly with mobile clients
- Standard approach with good library support

### Negative
- Cannot immediately invalidate tokens (must wait for expiry)
- More complex than session-based auth
- Requires careful handling of token storage

### Risks
- Token theft: Mitigated by short access token expiry and httpOnly cookies
- XSS attacks: Mitigated by not storing tokens in localStorage

## Alternatives Considered

### Alternative 1: Session-based authentication
Using server-side sessions with cookies.
- **Pros:** Simple, immediate revocation
- **Cons:** Requires session storage, harder to scale
- **Why rejected:** Does not fit our stateless API architecture

### Alternative 2: OAuth 2.0 with external provider
Using Google/GitHub for authentication.
- **Pros:** No password management, trusted providers
- **Cons:** Dependency on external services, some users prefer local accounts
- **Why rejected:** Users need local account option

## Implementation Notes

- Create `src/auth/` module for authentication logic
- Use `jsonwebtoken` library for JWT operations
- Add middleware to verify tokens on protected routes
- Store refresh token in `users.refresh_token` column

## References

- JWT Best Practices: https://tools.ietf.org/html/rfc8725
- OWASP Auth Cheatsheet: https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
```

---

## Changelog Entry Template

Use this template when adding feature changelog entries in Phase 7.

### Entry Format

Entries should be concise, user-focused lines under the appropriate category:

```markdown
### Added
- Add [feature name] with [key capability]

### Changed
- Update [component] to [new behavior]

### Fixed
- Fix [issue description]
```

### Usage Instructions

1. **Locate CHANGELOG.md:**
   - Find the project's `CHANGELOG.md` in the repository root
   - If it does not exist, create it using the structure below

2. **Find the `[Unreleased]` section:**
   - Entries go under `## [Unreleased]`
   - If the section does not exist, add it after the header

3. **Choose the appropriate category:**
   - **Added** - New features or capabilities
   - **Changed** - Changes to existing functionality
   - **Deprecated** - Features that will be removed
   - **Removed** - Features that were removed
   - **Fixed** - Bug fixes
   - **Security** - Security improvements

4. **Write concise entries:**
   - Use imperative mood ("Add feature" not "Added feature")
   - Focus on user-facing changes
   - One line per distinct change
   - Reference related ADRs if applicable

### CHANGELOG.md Structure

If creating a new CHANGELOG.md:

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- Your new feature entry here
```

### Example Entries

#### Simple Feature
```markdown
### Added
- Add user profile editing with avatar upload support
```

#### Feature with Multiple Changes
```markdown
### Added
- Add profile edit form with real-time validation
- Add avatar upload with image cropping

### Changed
- Update navigation to display user avatar
```

#### Referencing ADRs
```markdown
### Added
- Add JWT-based user authentication (see ADR-0003)
```

### Categories Reference

Use these categories from Keep a Changelog (in this order):

| Category | Use For |
|----------|---------|
| **Added** | New features |
| **Changed** | Changes to existing functionality |
| **Deprecated** | Features that will be removed in future |
| **Removed** | Features that were removed |
| **Fixed** | Bug fixes |
| **Security** | Security improvements |

For feature development, **Added** and **Changed** are most common.

### Tips

- Keep entries concise - detailed implementation notes belong in commits or ADRs
- Focus on what users can now do, not implementation details
- If a feature spans multiple categories, add entries to each relevant one
- Refer to the **changelog-format** skill for additional Keep a Changelog guidelines

---

## Integration Notes

This skill requires the following capabilities:
- **File read/write**: Reading source files, writing new files, modifying existing files
- **Shell execution**: Running tests, checking git state, creating directories
- **User interaction**: Confirming understanding, choosing approaches, approving implementation
- **Sub-agent delegation**: Launching parallel architecture agents (2-3) and review agents (3) with independent focus areas
