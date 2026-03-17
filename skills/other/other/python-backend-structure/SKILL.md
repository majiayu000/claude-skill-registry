---
name: python-backend-structure
description: "Organize backend Python code cleanly for FastAPI projects. This skill should be used when setting up initial backend directory structure, organizing code into logical modules, defining layer separation (routers, services, models), establishing import patterns and dependency flow, creating new backend features or domains, and reviewing code organization for consistency."
---

# Python Backend Structure

## Purpose
Organize backend Python code cleanly for FastAPI projects. This skill establishes directory structure, module organization, and code separation patterns that enable maintainable, testable backend development within the monorepo context.

## When to Use
- When setting up initial backend directory structure
- When organizing code into logical modules
- When defining layer separation (routers, services, models)
- When establishing import patterns and dependency flow
- When creating new backend features or domains
- When reviewing code organization for consistency

## When NOT to Use
- When the technology stack isn't confirmed as Python/FastAPI
- When working on frontend structure (use frontend-architecture)
- When designing API contracts (use rest-api-design)
- When implementing specific business logic
- When the monorepo structure hasn't been defined

## Required Clarifications
1. What is the specific technology stack being used (FastAPI version, database, etc.)?
2. What are the main feature domains for the backend?
3. What are the authentication and authorization requirements?
4. What are the database integration requirements?

## Optional Clarifications
5. Are there existing Python coding standards to follow?
6. Are there specific testing frameworks or patterns to use?
7. What are the deployment and containerization requirements?

## Responsibilities
- Define backend directory hierarchy (app/, routers/, services/, models/)
- Establish module responsibility boundaries
- Create import organization patterns
- Plan configuration and settings management
- Design test directory structure parallel to source
- Document dependency flow between layers
- Ensure compatibility with FastAPI application factory
- Maintain clean separation of concerns

## Inputs
- Monorepo backend directory location
- FastAPI application requirements
- Database and authentication integrations
- Feature domains and boundaries
- Coding standards and conventions

## Outputs
- Backend directory structure diagram
- Module organization guidelines
- Import pattern documentation
- Configuration management strategy
- Test organization parallel to source
- Layer dependency rules

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Existing structure, patterns, conventions to integrate with |
| **Conversation** | User's specific requirements, constraints, preferences |
| **Skill References** | Domain patterns from `references/` (Python/FASTAPI docs, best practices, examples) |
| **User Guidelines** | Project-specific conventions, team standards |

Ensure all required context is gathered before implementing.
Only ask user for THEIR specific requirements (domain expertise is in this skill).

## Implementation Workflow
1. Assess Python backend structure requirements
2. Define backend directory hierarchy
3. Establish module responsibility boundaries
4. Create import organization patterns
5. Plan configuration and settings management
6. Design test directory structure parallel to source
7. Document dependency flow between layers
8. Validate against constraints and anti-patterns

## Output Checklist
- [ ] Backend directory structure designed
- [ ] Module organization guidelines created
- [ ] Import pattern documentation created
- [ ] Configuration management strategy defined
- [ ] Test organization designed
- [ ] Layer dependency rules documented
- [ ] Constraints respected

## Constraints
- Never import from higher layers to lower layers
- Never mix business logic with infrastructure code
- Never scatter configuration across multiple locations
- Never create circular imports between modules
- Always maintain clear layer boundaries
- Always organize tests to mirror source structure
- Always use __init__.py appropriately for packages

## Interaction With Other Skills
- **monorepo-architecture:** Operates within defined backend directory
- **fastapi-architecture:** Provides structure for FastAPI application
- **sqlmodel-design:** Houses database model definitions
- **jwt-verification:** Organizes authentication middleware
- **claude-context-design:** Informs backend CLAUDE.md context

## Anti-Patterns
- **Flat structure:** All files in single directory without organization
- **Circular imports:** Module A imports B which imports A
- **Layer violation:** Services importing from routers
- **God module:** Single module handling all concerns
- **Scattered config:** Settings files in multiple random locations
- **Test chaos:** Tests not mirroring source structure
- **Import pollution:** Wildcard imports or overly long import lists

## Security Best Practices
- Secure configuration management (no hardcoded secrets)
- Proper dependency injection patterns
- Input validation at API boundaries
- Secure error handling and logging
- Follow Python security best practices
- Use environment variables for sensitive configuration

## Documentation Resources
- [Python Style Guide](https://peps.python.org/pep-0008/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [Python Testing](https://docs.pytest.org/)

## Phase Applicability
Phase II only. Phase I uses simple src/ structure for console application.