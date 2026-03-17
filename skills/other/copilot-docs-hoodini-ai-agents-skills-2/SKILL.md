---
name: copilot-docs
description: Configure GitHub Copilot with custom instructions. Use when setting up .github/copilot-instructions.md, customizing Copilot behavior, or creating repository-specific AI guidance. Triggers on Copilot instructions, copilot-instructions.md, GitHub Copilot config.
---

# GitHub Copilot Custom Instructions

Configure repository-specific instructions for GitHub Copilot.

## Quick Start

Create `.github/copilot-instructions.md` in your repository:

```markdown
# Copilot Instructions

## Code Style
- Use TypeScript with strict mode
- Prefer functional components with hooks
- Use Tailwind CSS for styling

## Project Context
This is a Next.js 14 app using the App Router.
API routes are in `app/api/`.
```

## Effective Patterns

### Project Context
```markdown
# Project Context

## Tech Stack
- Next.js 14 with App Router
- TypeScript 5.3+
- Tailwind CSS 3.4
- Prisma ORM with PostgreSQL

## Architecture
- `app/` - Next.js App Router pages and API routes
- `components/` - React components
- `lib/` - Utility functions and shared code
- `prisma/` - Database schema and migrations
```

### Code Standards
```markdown
# Code Standards

## TypeScript
- Enable strict mode
- Prefer `interface` over `type` for object shapes
- Use explicit return types on functions

## React
- Use functional components exclusively
- Prefer named exports
- Extract hooks to `hooks/` directory

## Error Handling
- Use Result pattern for fallible operations
- Always handle async errors with try/catch
- Log errors with structured format
```

### Naming Conventions
```markdown
# Naming Conventions

## Files
- Components: PascalCase (Button.tsx)
- Utilities: camelCase (formatDate.ts)
- Constants: SCREAMING_SNAKE_CASE

## Code
- Boolean variables: is*, has*, should* prefix
- Event handlers: handle* prefix (handleClick)
- Async functions: *Async suffix
```

### Testing
```markdown
# Testing Guidelines

## Unit Tests
- Use Vitest for unit testing
- Place tests next to source files (*.test.ts)
- Mock external dependencies

## Test Patterns
```typescript
describe('Component', () => {
  it('should render correctly', () => {
    // Arrange, Act, Assert pattern
  });
});
```
```

### API Patterns
```markdown
# API Patterns

## Route Handlers
```typescript
// Standard response format
return NextResponse.json({
  data: result,
  error: null,
  meta: { timestamp: Date.now() }
});

// Error response
return NextResponse.json(
  { data: null, error: { code: 'NOT_FOUND', message: '...' } },
  { status: 404 }
);
```

## Validation
- Use Zod for request validation
- Validate early, fail fast
```

### Do's and Don'ts
```markdown
# Guidelines

## Do
- Write self-documenting code
- Add JSDoc comments for public APIs
- Use meaningful variable names

## Don't
- Use `any` type
- Leave console.log in production code
- Commit sensitive data
```

## File Location

The file must be at `.github/copilot-instructions.md` (not in root).

## Resources

- **GitHub Docs**: https://docs.github.com/en/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot
- **VS Code Copilot**: https://code.visualstudio.com/docs/copilot/copilot-customization
