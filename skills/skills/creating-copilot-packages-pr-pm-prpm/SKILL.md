---
name: creating-copilot-packages
description: Use when creating GitHub Copilot instructions - provides repository-wide and path-specific formats, applyTo patterns, excludeAgent options, and natural language markdown style
---

# Creating GitHub Copilot Packages

## Overview

GitHub Copilot uses natural language markdown instructions. Repository-wide instructions use plain markdown with NO frontmatter. Path-specific instructions use YAML frontmatter with `applyTo` field.

## Package Types

| Type | File Location | Frontmatter |
|------|--------------|-------------|
| **Repository-wide** | `.github/copilot-instructions.md` | None (plain markdown) |
| **Path-specific** | `.github/instructions/*.instructions.md` | Required (`applyTo` field) |

## Quick Reference

### Repository-Wide (No Frontmatter)

```markdown
# API Development Guidelines

Follow REST best practices when developing API endpoints.

## Principles

- Use semantic HTTP methods (GET, POST, PUT, DELETE)
- Return appropriate status codes
- Include error messages in response body
```

### Path-Specific (With Frontmatter)

```yaml
---
applyTo: "src/api/**/*.ts"  # REQUIRED
excludeAgent: "code-review"  # Optional
---
```

## Creating Repository-Wide Instructions

File: `.github/copilot-instructions.md`

Plain markdown with NO frontmatter:

```markdown
# TaskManager Development Guidelines

## Architecture

### Frontend
- React 18 with TypeScript
- Vite for build tooling
- Zustand for state management
- Tailwind CSS for styling

### Backend
- Node.js with Express
- PostgreSQL with Prisma ORM
- JWT for authentication

## Coding Conventions

- Use TypeScript strict mode
- Functional components with hooks
- Colocate tests with source files
- Use Zod for runtime validation

## Testing

- Use Vitest for unit tests
- Aim for 80% coverage on new code
- Mock external dependencies

## Examples

\`\`\`typescript
// Good: RESTful endpoint
app.get('/api/users', async (req, res) => {
  try {
    const users = await db.users.findAll();
    res.json({ users });
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch users' });
  }
});
\`\`\`
```

## Creating Path-Specific Instructions

File: `.github/instructions/api-endpoints.instructions.md`

**REQUIRED**: File name must end with `.instructions.md`

### Single Pattern

```markdown
---
applyTo: "app/models/**/*.rb"
---

# Model Guidelines

These rules apply only to Ruby model files.

## Conventions

- Use ActiveRecord validations
- Define associations explicitly
- Add database indexes for foreign keys
```

### Multiple Patterns (Comma-Separated)

```markdown
---
applyTo: "**/*.ts,**/*.tsx"
---

# TypeScript Guidelines

These rules apply to all TypeScript files.

## Type Safety

- Always define explicit types for function parameters
- Avoid using `any` type
- Use `unknown` instead of `any` for truly unknown types
```

### Multiple Patterns (Array)

```markdown
---
applyTo:
  - "src/api/**/*.ts"
  - "src/services/**/*.ts"
---

# API Endpoint Guidelines

These rules apply only to API files.

## Requirements

- All endpoints must have error handling
- Use async/await for database calls
- Log all errors with structured logging
- Validate input with Zod schemas

## Example

\`\`\`typescript
import { z } from 'zod';

const createUserSchema = z.object({
  name: z.string().min(1),
  email: z.string().email(),
});

app.post('/api/users', async (req, res) => {
  try {
    const data = createUserSchema.parse(req.body);
    const user = await db.users.create(data);
    res.status(201).json({ user });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({ error: error.errors });
    }
    logger.error('Failed to create user', { error });
    res.status(500).json({ error: 'Internal server error' });
  }
});
\`\`\`
```

## ApplyTo Patterns

### Common Glob Patterns

```yaml
# All TypeScript files
applyTo: "**/*.ts"

# React components
applyTo: "src/**/*.{tsx,jsx}"

# API routes
applyTo: "src/api/**/*.ts"

# Test files
applyTo: "**/*.test.ts"

# All files (any of these work)
applyTo: "**"
applyTo: "*"
applyTo: "**/*"

# Multiple patterns (array)
applyTo:
  - "src/api/**/*.ts"
  - "src/services/**/*.ts"
  - "src/routes/**/*.ts"
```

## ExcludeAgent Field

Control which Copilot agent uses the instructions:

### Coding Agent Only

```markdown
---
applyTo: "**"
excludeAgent: "code-review"
---

# Coding Agent Only Instructions

These instructions are only used by the Copilot coding agent.

- Focus on implementation patterns
- Suggest modern syntax alternatives
- Optimize for readability in generated code
```

### Code Review Only

```markdown
---
applyTo: "**/*.test.ts"
excludeAgent: "coding-agent"
---

# Code Review Only Instructions

These instructions are only used by Copilot code review.

- Verify test coverage is adequate
- Check for proper assertions
- Ensure tests are not flaky
```

## Content Format

Natural language markdown with:

- **Clear headings**: Organize with H1/H2
- **Bullet points**: For lists of rules
- **Code examples**: Show concrete patterns
- **Plain language**: Write for human readability
- **Actionable guidance**: Specific, not generic

## Example: Testing Standards

```markdown
---
applyTo: "**/*.test.ts"
---

# Testing Standards

All tests use Jest and React Testing Library.

## Component Tests

- Test user interactions, not implementation
- Use `screen.getByRole` over `getByTestId`
- Mock external dependencies
- Test accessibility (ARIA roles)

## Example

\`\`\`typescript
test('submits form when valid', async () => {
  render(<LoginForm />);

  await userEvent.type(screen.getByLabelText('Email'), 'test@example.com');
  await userEvent.type(screen.getByLabelText('Password'), 'password123');
  await userEvent.click(screen.getByRole('button', { name: 'Login' }));

  expect(mockLogin).toHaveBeenCalledWith({
    email: 'test@example.com',
    password: 'password123',
  });
});
\`\`\`
```

## Example: Database Patterns

```markdown
---
applyTo:
  - "src/db/**/*.ts"
  - "src/repositories/**/*.ts"
---

# Database Access Patterns

We use Prisma ORM with PostgreSQL.

## Query Guidelines

- Always use transactions for multi-step operations
- Use `select` to limit returned fields
- Include proper indexes
- Handle unique constraint violations

## Example

\`\`\`typescript
// Good: Transaction with error handling
async function transferFunds(fromId: string, toId: string, amount: number) {
  try {
    await prisma.$transaction(async (tx) => {
      await tx.account.update({
        where: { id: fromId },
        data: { balance: { decrement: amount } },
      });

      await tx.account.update({
        where: { id: toId },
        data: { balance: { increment: amount } },
      });
    });
  } catch (error) {
    if (error.code === 'P2025') {
      throw new Error('Account not found');
    }
    throw error;
  }
}
\`\`\`
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Frontmatter in repo-wide | Repository-wide uses NO frontmatter |
| Missing .instructions.md suffix | Path-specific files must end with `.instructions.md` |
| Missing applyTo field | Path-specific requires `applyTo` in frontmatter |
| Generic advice | Focus on project-specific patterns |
| No code examples | Show concrete patterns from your project |

## Validation

Schema location: `/Users/khaliqgant/Projects/prpm/app/packages/converters/schemas/copilot.schema.json`

Documentation: `/Users/khaliqgant/Projects/prpm/app/packages/converters/docs/copilot.md`

## Best Practices

1. **Be specific**: Generic advice is less useful than project-specific patterns
2. **Show examples**: Code samples are more effective than descriptions
3. **Keep it short**: Copilot processes limited context
4. **Natural language**: Write as you would explain to a developer
5. **Update regularly**: Keep instructions in sync with codebase
6. **Granular targeting**: Use path-specific for different contexts
7. **Descriptive filenames**: Use clear names like `api-endpoints.instructions.md`

## Storage Locations

Instructions can be stored in multiple locations:

1. **Repository**: `.github/copilot-instructions.md` (repository-wide)
2. **Repository**: `.github/instructions/*.instructions.md` (path-specific)
3. **Team Dashboard**: Created via Copilot Dashboard for team sharing

---

**Remember**: Repository-wide uses NO frontmatter. Path-specific requires `applyTo` field and `.instructions.md` suffix.
