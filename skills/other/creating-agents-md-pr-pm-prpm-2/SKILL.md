---
name: creating-agents-md
description: Use when creating agents.md files - provides plain markdown format with NO frontmatter, free-form structure, and project context guidelines for AI coding assistants
---

# Creating agents.md Files

## Overview

The `agents.md` format provides project-specific context for AI coding assistants. It's the simplest format: **plain markdown only** with NO YAML frontmatter, NO special syntax.

**CRITICAL:**
- **No frontmatter** - Pure markdown only (no YAML)
- **Free-form content** - No required structure
- **Single file** - Typically `agents.md` in project root

## Quick Reference

| Aspect | Requirement |
|--------|-------------|
| Format | Plain markdown |
| Frontmatter | None (forbidden) |
| Structure | Free-form |
| File location | `agents.md` in project root |

## Creating agents.md Files

Plain markdown with no frontmatter:

```markdown
# TaskMaster Development Guide

## Project Overview

TaskMaster is a task management application for remote teams, built with real-time collaboration features and offline-first architecture.

## Architecture

### Frontend

- React 18 with TypeScript
- Vite for build tooling
- Zustand for state management
- React Query for server state
- Tailwind CSS for styling

### Backend

- Node.js with Express
- PostgreSQL with Prisma ORM
- WebSocket for real-time features
- Redis for caching and pub/sub
- JWT for authentication

## Coding Conventions

- Use TypeScript strict mode
- Functional components with hooks (no class components)
- Server components by default in Next.js
- Colocate tests with source files (*.test.tsx)
- Use Zod for runtime validation

## File Structure

\`\`\`
src/
  components/     # Reusable UI components
  features/       # Feature-based modules
  hooks/          # Custom React hooks
  lib/            # Utility functions
  pages/          # Route pages
  types/          # TypeScript types
\`\`\`

## Development Workflow

1. Create feature branch from `main`
2. Write tests first (TDD)
3. Implement feature
4. Run `pnpm test` and `pnpm lint`
5. Create PR with description
6. Merge after approval

## Testing

- Use Vitest for unit tests
- Use Playwright for E2E tests
- Aim for 80% coverage on new code
- Mock external dependencies
```

## What to Include

Focus on project-specific information AI doesn't already know:

**High Priority:**
- Project overview and purpose
- Architecture decisions and patterns
- Tech stack and dependencies
- File structure and organization
- Coding conventions
- Development workflow
- Testing approach
- Domain knowledge and business logic

**Skip:**
- General programming best practices
- Language syntax explanations
- Framework basics
- Obvious code quality rules

## Example: Backend API Project

```markdown
# Payment Gateway API

## Overview

RESTful API for payment processing with support for multiple payment providers.

## Tech Stack

- Node.js 20.x
- Express
- PostgreSQL 15
- Redis for rate limiting
- Stripe and PayPal integrations

## API Design

### Endpoints

All endpoints follow REST conventions:

- `GET /api/payments` - List payments
- `GET /api/payments/:id` - Get payment details
- `POST /api/payments` - Create payment
- `PUT /api/payments/:id` - Update payment
- `DELETE /api/payments/:id` - Cancel payment

### Error Handling

Return consistent error format:

\`\`\`json
{
  "error": {
    "code": "PAYMENT_FAILED",
    "message": "Payment could not be processed",
    "details": {...}
  }
}
\`\`\`

## Security

- All endpoints require JWT authentication
- Rate limiting: 100 requests/minute per IP
- Input validation with Zod schemas
- SQL injection prevention via Prisma
- PCI DSS compliance for payment data

## Database

### Conventions

- Use snake_case for table/column names
- Add timestamps (created_at, updated_at) to all tables
- Use UUIDs for primary keys
- Foreign keys follow `{table}_id` pattern
```

## Example: Frontend Component Library

```markdown
# Design System Components

A React component library following Atomic Design principles.

## Component Structure

All components follow this structure:

\`\`\`
ComponentName/
  ComponentName.tsx       # Main component
  ComponentName.test.tsx  # Tests
  ComponentName.stories.tsx # Storybook stories
  index.ts                 # Exports
\`\`\`

## Styling

- Use Tailwind CSS utility classes
- Create custom classes in `styles/components/` for complex components
- Follow BEM naming for custom classes
- Responsive by default (mobile-first)

## TypeScript

\`\`\`typescript
// Good: Explicit prop types
interface ButtonProps {
  variant: 'primary' | 'secondary' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  onClick?: () => void;
  children: React.ReactNode;
}

export function Button({ variant, size = 'md', ...props }: ButtonProps) {
  return <button className={cn(variants[variant], sizes[size])} {...props} />;
}
\`\`\`

## Accessibility

- All interactive elements must be keyboard accessible
- Use semantic HTML (button, nav, main, etc.)
- Include ARIA labels for icon-only buttons
- Test with screen readers
- Maintain minimum 4.5:1 contrast ratio
```

## Content Format

Free-form markdown including:

- **Project overview**: Purpose and goals
- **Architecture notes**: Technical decisions and patterns
- **Conventions**: Coding standards and practices
- **Context**: Domain knowledge and business logic
- **Workflows**: Development processes
- **File structure**: Directory organization
- **Dependencies**: Key libraries and tools

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Adding YAML frontmatter | No frontmatter allowed - plain markdown only |
| Generic best practices | Focus on project-specific patterns |
| Verbose explanations | Be concise, AI already knows general concepts |
| Language tutorials | Skip basics, focus on project conventions |
| Missing context | Include domain knowledge and business logic |

## Writing Style

**Concise (Good):**
```markdown
## Testing

- Vitest for unit tests
- Playwright for E2E
- 80% coverage target
- Mock external dependencies
```

**Verbose (Bad):**
```markdown
## Testing

When you are writing tests, it's important to understand that we use Vitest
for our unit tests because it's fast and modern. For end-to-end testing,
we have chosen to use Playwright because it provides excellent cross-browser
support and has a great developer experience...
```

## File Placement

Typically in project root:
```
project-root/
  agents.md           # Main file
  src/
  tests/
  package.json
```

Can also be in subdirectories for monorepos:
```
monorepo/
  packages/
    frontend/
      agents.md       # Frontend-specific context
    backend/
      agents.md       # Backend-specific context
```

## Validation

Documentation: `/Users/khaliqgant/Projects/prpm/app/packages/converters/docs/agents-md.md`

Schema location: `/Users/khaliqgant/Projects/prpm/app/packages/converters/schemas/agents-md.schema.json`

## Best Practices

1. **Be concise**: Focus on project-specific info (AI knows general practices)
2. **Keep updated**: Review and update as project evolves
3. **Real examples**: Show actual code patterns from your project
4. **Plain markdown**: No YAML frontmatter or special syntax
5. **Human-readable**: Write for both AI and human developers
6. **Project-specific**: Avoid generic advice that AI already knows
7. **Natural structure**: Organize however makes sense for your project

## Migration from Other Formats

When converting to agents.md:

1. **Strip all frontmatter** - Remove YAML headers completely
2. **Focus on content** - Keep only markdown content
3. **Combine files** - Merge multiple rule files into one cohesive document
4. **Simplify** - Remove format-specific features (globs, regex, etc.)
5. **Plain markdown only** - Use standard markdown syntax

## Official Specification

For the authoritative specification, see: https://github.com/openai/agents.md

---

**Remember**: agents.md uses plain markdown with NO frontmatter. Free-form structure. Focus on project-specific context AI doesn't already know.
