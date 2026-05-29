---
name: technical-communication
description: "Clear and effective technical communication for documentation, code comments, and team collaboration. Writing standards, documentation structure, commit messages. Trigger: When writing technical documentation, creating code comments, or communicating technical concepts."
skills:
  - conventions
  - humanizer
allowed-tools:
  - documentation-reader
  - web-search
---

# Technical Communication Skill

## Overview

Best practices for clear, concise, and effective technical communication in software development contexts.

## Objective

Enable developers to communicate technical concepts clearly through documentation, code comments, commit messages, and team collaboration.

---

## When to Use

Use this skill when:

- Writing API documentation or README files
- Creating code comments and JSDoc
- Writing commit messages and PR descriptions
- Documenting architecture decisions (ADRs)
- Explaining technical concepts to team members

Don't use this skill for:

- Marketing copy or user-facing content
- Non-technical communication

---

## Critical Patterns

### ✅ REQUIRED: Write Descriptive Commit Messages

**Two formats: Simple (default) and Descriptive**

**Simple format (default - one line):**

```
// ✅ CORRECT: Simple with ticket ID
[SM-14466] fix: handle API 500 error on service plan creation; add error handling for categoryIds; prevent premature Code Review

// ✅ CORRECT: Simple without ticket ID
feat: add user authentication with JWT; implement refresh tokens; include login and logout endpoints

// ❌ WRONG: Missing semicolons between summaries
[SM-123] feat: add feature update another thing do more stuff
```

**Descriptive format (when requested):**

```
// ✅ CORRECT: Descriptive with ticket ID
[SM-14466] fix: handle API 500 error on service plan creation

- Add error handling for 500 response when sending categoryIds
- Prevents moving ticket to Code Review if plans are not listed
- Adds explanatory comment for backend team

// ✅ CORRECT: Descriptive without ticket ID
feat: add user authentication with JWT

- Implements JWT-based authentication system
- Includes login, logout, and token refresh endpoints
- Adds session management and error handling
```

**Rules:**

- **Default to simple format** unless user requests "descriptive commit"
- **Simple**: `[TICKET-ID] type: summary; summary2; summary3` (one line, semicolons separate changes)
- **Descriptive**: `[TICKET-ID] type: summary` + bullet list (one summary line + detailed changes)
- Valid types: feat, fix, refactor, chore, docs, test, etc.
- Use only ASCII apostrophes (') and hyphens (-)
- If ticket ID provided: Start with `[TICKET-ID]` (e.g., `[SM-123]`, `[JIRA-456]`)
- If NO ticket ID: Omit `[TICKET-ID]` entirely, start with type
- Never use placeholder `[TICKET-ID]` without actual ticket number

### ✅ REQUIRED: Use Active Voice

```markdown
<!-- ✅ CORRECT: Active voice -->

The API validates the request and returns a 200 status.

<!-- ❌ WRONG: Passive voice -->

The request is validated by the API and a 200 status is returned.
```

### ✅ REQUIRED: Provide Examples

```markdown
<!-- ✅ CORRECT: With example -->

## Authentication

Include your API key in the Authorization header:

\`\`\`
Authorization: Bearer your-api-key
\`\`\`

<!-- ❌ WRONG: No example -->

## Authentication

Use the Authorization header with your API key.
```

---

## Conventions

Refer to conventions for:

- Code organization
- Documentation standards

### Technical Communication Specific

- Write clear, scannable documentation
- Use active voice
- Provide context and examples
- Keep sentences concise
- Use proper markdown formatting
- Write descriptive commit messages
- Document assumptions and decisions

---

## Decision Tree

**API documentation?** → Include endpoint, parameters, request/response examples, error codes.

**Code comment?** → Explain "why" not "what". Avoid obvious comments.

**Commit message?** → Use conventional commits format. **Default: simple format** (`[TICKET-ID] type: summary; summary2`). Use descriptive format only when user requests it (`[TICKET-ID] type: summary` + bullet list). Omit `[TICKET-ID]` if no ticket provided.

**README?** → Include: purpose, installation, usage, examples, contributing guidelines.

**Technical decision?** → Document with context, rationale, and impact.

**Complex concept?** → Use diagrams, examples, analogies. Break into smaller sections.

**Error message?** → State problem, cause, solution. Be specific and actionable.

---

## Example

Good commit message (simple format - default):

```
// With ticket ID
[SM-14466] fix: handle API 500 error on service plan creation; add error handling for categoryIds; prevent premature Code Review

// Without ticket ID
feat: add user authentication with JWT; implement refresh tokens; include login and logout endpoints
```

Good commit message (descriptive format - when requested):

```
// With ticket ID
[SM-14466] fix: handle API 500 error on service plan creation

- Add error handling for 500 response when sending categoryIds
- Prevents moving ticket to Code Review if plans are not listed
- Adds explanatory comment for backend team

// Without ticket ID
feat: add user authentication with JWT

- Implements JWT-based authentication system
- Includes login, logout, and token refresh endpoints
- Adds session management and error handling
```

Good documentation:

```markdown
## Authentication

The API uses JWT tokens for authentication. Include the token in the Authorization header:

\`\`\`
Authorization: Bearer <token>
\`\`\`

Tokens expire after 1 hour. Use the refresh endpoint to obtain a new token.
```

---

## Edge Cases

**Audience knowledge level:** Adjust technical depth based on audience. Avoid jargon for general audience.

**Outdated documentation:** Review and update docs regularly. Use doc tests or CI checks.

**Version-specific docs:** Clearly indicate which version documentation applies to.

**Non-native English speakers:** Use simple, clear language. Avoid idioms and complex sentences.

**Code examples:** Ensure examples are runnable and tested. Include necessary imports and setup.

---

## References

- https://www.writethedocs.org/guide/writing/style-guides/
- https://developers.google.com/style
