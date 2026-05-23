---
name: requirement-summary
description: Generate concise, structured summaries of requirements for quick team understanding. Use when analyzing requirements from text documents (MD, TXT, DOCX) or technical specifications to create bullet-point summaries that highlight core functionality and dependencies/constraints. Ideal for sprint planning, stakeholder updates, team onboarding, or any situation requiring rapid comprehension of requirement documents.
---

# Requirement Summary

## Overview

Generate structured, bullet-point summaries (5-7 items) from requirement documents that enable teams to quickly grasp core functionality and critical constraints without reading full specifications.

## Workflow

### 1. Analyze the Requirement Document

Read the provided requirement document thoroughly to identify:
- Core functionality and features being requested
- Technical dependencies and system constraints
- Integration points with existing systems
- Critical limitations or blockers
- Success criteria or acceptance conditions

### 2. Extract Key Information

Focus on information that directly impacts implementation decisions:
- **What** is being built (features, capabilities, user-facing changes)
- **Why** it's needed (business value, problem being solved)
- **Dependencies** (external systems, APIs, data sources, prerequisites)
- **Constraints** (technical limitations, performance requirements, compliance needs)
- **Scope boundaries** (what's explicitly excluded or deferred)

### 3. Structure the Summary

Create a bullet-point list with 5-7 items following this pattern:

```
**[Category]**: [Concise description]
```

Recommended categories:
- **Core Functionality**: Primary features or capabilities
- **Key Dependencies**: External systems, APIs, or prerequisites
- **Technical Constraints**: Performance, scalability, or platform limitations
- **Integration Points**: How this connects with existing systems
- **Success Criteria**: Measurable outcomes or acceptance conditions
- **Out of Scope**: Explicitly excluded features or future considerations

### 4. Apply Clarity Principles

Each bullet point should:
- Start with a bold category label for scannability
- Use active, specific language (avoid vague terms like "improve" or "enhance")
- Include concrete details (numbers, systems, technologies) when available
- Be self-contained and understandable without reading other bullets
- Focus on "what" and "why" rather than "how"

### 5. Validate Completeness

Ensure the summary answers:
- What problem does this solve?
- What are we building?
- What systems does this depend on or integrate with?
- What are the critical constraints or limitations?
- How will we know it's successful?

## Example

**Input**: A 3-page technical specification for a user authentication system

**Output**:
```
**Core Functionality**: Implement OAuth 2.0 authentication with support for Google and GitHub providers, including token refresh and session management

**Key Dependencies**: Requires integration with existing user database (PostgreSQL), Redis for session storage, and external OAuth provider APIs

**Technical Constraints**: Must support 10,000 concurrent users with <200ms authentication latency; sessions expire after 24 hours of inactivity

**Integration Points**: Connects to existing user profile service via REST API; emits authentication events to event bus for audit logging

**Security Requirements**: Enforce HTTPS-only, implement CSRF protection, store tokens encrypted at rest using AES-256

**Out of Scope**: Multi-factor authentication and single sign-on (SSO) deferred to Phase 2
```

## Tips

- Prioritize information that affects implementation decisions over background context
- Use specific technical terms (API names, technologies, metrics) rather than generic descriptions
- When requirements are ambiguous, note the ambiguity in the summary
- For large documents, focus on the most critical 5-7 points rather than trying to cover everything
- If the document lacks key information (dependencies, constraints), explicitly note what's missing
