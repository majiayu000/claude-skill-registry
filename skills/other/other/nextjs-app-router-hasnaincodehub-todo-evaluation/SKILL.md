---
name: nextjs-app-router
description: "Design Next.js App Router structure with server/client components. This skill should be used when designing Next.js application structure, planning route organization with App Router, deciding server vs client component boundaries, implementing layouts and nested routing, planning data fetching patterns, and optimizing for server-side rendering."
---

# Next.js App Router

## Purpose
Design Next.js App Router structure with server/client components. This skill establishes patterns for organizing Next.js applications using the App Router paradigm, correctly separating server and client components, and leveraging Next.js features effectively.

## When to Use
- When designing Next.js application structure
- When planning route organization with App Router
- When deciding server vs client component boundaries
- When implementing layouts and nested routing
- When planning data fetching patterns
- When optimizing for server-side rendering

## When NOT to Use
- When working on backend code
- When the frontend framework isn't Next.js
- When using Pages Router instead of App Router
- When designing API contracts (use rest-api-design)
- When frontend technology hasn't been confirmed

## Required Clarifications
1. What are the specific route structures and navigation requirements?
2. What are the performance and SEO requirements for the application?
3. What are the data fetching patterns needed for different routes?
4. What are the authentication and protected route requirements?

## Optional Clarifications
5. Are there specific UI component libraries being used?
6. Are there existing Next.js patterns in the codebase to follow?
7. What are the accessibility requirements for the application?

## Responsibilities
- Design app/ directory structure
- Plan route grouping and organization
- Define server vs client component boundaries
- Establish layout and template patterns
- Configure loading and error boundaries
- Plan metadata and SEO strategy
- Design parallel and intercepting routes if needed
- Document data fetching patterns per route

## Inputs
- Feature specifications with UI requirements
- Frontend architecture requirements
- Authentication integration needs
- Performance requirements
- SEO and metadata requirements

## Outputs
- App directory structure diagram
- Route organization plan
- Server/client component boundary documentation
- Layout hierarchy design
- Loading and error state patterns
- Metadata strategy documentation

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Existing structure, patterns, conventions to integrate with |
| **Conversation** | User's specific requirements, constraints, preferences |
| **Skill References** | Domain patterns from `references/` (Next.js docs, best practices, examples) |
| **User Guidelines** | Project-specific conventions, team standards |

Ensure all required context is gathered before implementing.
Only ask user for THEIR specific requirements (domain expertise is in this skill).

## Implementation Workflow
1. Assess Next.js App Router requirements and structure
2. Design app/ directory structure
3. Plan route organization and grouping
4. Define server vs client component boundaries
5. Establish layout and template patterns
6. Configure loading and error boundaries
7. Plan metadata and SEO strategy
8. Document data fetching patterns
9. Validate against constraints and anti-patterns

## Output Checklist
- [ ] App directory structure designed
- [ ] Route organization plan created
- [ ] Server/client component boundaries defined
- [ ] Layout hierarchy designed
- [ ] Loading and error states configured
- [ ] Metadata strategy documented
- [ ] Data fetching patterns planned
- [ ] Constraints respected

## Constraints
- Never use client components unnecessarily
- Never fetch data in client components when server fetch is possible
- Never ignore loading and error states
- Never create deeply nested route structures without justification
- Always prefer server components by default
- Always define clear component boundaries
- Always implement proper loading states

## Interaction With Other Skills
- **frontend-architecture:** Operates within broader frontend structure
- **better-auth-integration:** Coordinates auth with App Router patterns
- **api-client-design:** Integrates API calls with routing
- **auth-aware-ui:** Coordinates protected routes
- **monorepo-architecture:** Fits within monorepo frontend directory

## Anti-Patterns
- **Client overuse:** Making everything a client component
- **Waterfall fetching:** Nested data fetches that could be parallelized
- **Layout leakage:** Not leveraging layouts for shared UI
- **Route chaos:** Disorganized route structure without grouping
- **Loading neglect:** Missing loading states causing poor UX
- **Error swallowing:** Not handling route-level errors
- **Metadata absence:** Missing SEO and metadata configuration

## Security Best Practices
- Sanitize user input in dynamic routes
- Implement proper authentication checks in server components
- Use Next.js middleware for route protection
- Validate and sanitize route parameters
- Implement proper CSP headers
- Protect against XSS in client components

## Documentation Resources
- [Next.js App Router Documentation](https://nextjs.org/docs/app)
- [Server and Client Components](https://nextjs.org/docs/app/building-your-application/rendering/server-components)
- [Routing Guide](https://nextjs.org/docs/app/building-your-application/routing)
- [Data Fetching](https://nextjs.org/docs/app/building-your-application/data-fetching)
- [Performance Optimization](https://nextjs.org/docs/app/building-your-application/optimizing)

## Phase Applicability
Phase II only. Phase I uses console interface without web frontend.