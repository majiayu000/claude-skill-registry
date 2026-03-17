---
name: creating-windsurf-packages
description: Use when creating Windsurf rules - provides plain markdown format with NO frontmatter, 12,000 character limit, and single-file structure requirements
---

# Creating Windsurf Packages

## Overview

Windsurf uses a single `.windsurf/rules` file containing plain markdown instructions with NO frontmatter.

**CRITICAL CONSTRAINTS:**
- **No frontmatter** - Pure markdown only
- **12,000 character limit** - Hard limit enforced by Windsurf
- **Single file** - All rules in one `.windsurf/rules` file

## Quick Reference

| Aspect | Requirement |
|--------|-------------|
| Format | Plain markdown |
| Frontmatter | None (forbidden) |
| Character limit | 12,000 max |
| File location | `.windsurf/rules` (single file) |

## Creating Rules

Plain markdown with optional H1 title and organized sections:

```markdown
# React Development Guidelines

Guidelines for building React applications in this project.

## Component Structure

- Use functional components with hooks
- Keep components under 200 lines
- Extract logic into custom hooks when appropriate
- Co-locate styles with components

## State Management

We use Zustand for global state:

- Create stores in `src/stores/`
- Use selectors to prevent unnecessary re-renders
- Keep stores focused on single concerns

\`\`\`typescript
// Good: Focused store
const useAuthStore = create((set) => ({
  user: null,
  login: (user) => set({ user }),
  logout: () => set({ user: null }),
}));
\`\`\`

## Testing

- Write tests alongside components (`.test.tsx`)
- Use React Testing Library
- Test user behavior, not implementation details
- Aim for 80% coverage on new code
```

## Character Budget Tips

To stay under 12,000 characters:

1. **Focus on project-specific patterns** - AI already knows general best practices
2. **Use concise language** - Every word counts
3. **Limit code examples** - Only essential patterns
4. **Skip obvious practices** - Don't repeat what AI knows
5. **Reference external docs** - Link instead of repeating

## Example: Project-Specific Context

```markdown
# Project Architecture

## Tech Stack

- **Frontend**: React 18 + TypeScript + Vite
- **Styling**: Tailwind CSS
- **State**: Zustand
- **Routing**: React Router v6
- **API**: REST with axios

## Directory Structure

\`\`\`
src/
  components/     # Reusable UI components
  features/       # Feature-specific code
  hooks/          # Custom React hooks
  stores/         # Zustand stores
  utils/          # Helper functions
  types/          # TypeScript types
\`\`\`

## Coding Conventions

- Use PascalCase for components
- Use camelCase for functions/variables
- Use kebab-case for file names
- Export components as named exports

## API Integration

All API calls go through `src/api/client.ts`:

\`\`\`typescript
import { apiClient } from '@/api/client';

// Use the client
const users = await apiClient.get('/users');
\`\`\`

## Environment Variables

Access via `import.meta.env`:

- `VITE_API_URL` - Backend API URL
- `VITE_APP_ENV` - Environment (dev/staging/prod)
```

## Content Format

Standard markdown including:

- **H1 title**: Main heading (optional)
- **H2/H3 sections**: Organize content
- **Lists**: Unordered and ordered
- **Code blocks**: With language specifiers
- **Standard markdown**: Bold, italic, links

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Adding YAML frontmatter | No frontmatter allowed - plain markdown only |
| Exceeding 12,000 chars | Prioritize project-specific content, trim aggressively |
| Multiple files | All content in single `.windsurf/rules` file |
| Generic best practices | Focus on project-specific patterns |
| Verbose examples | Keep examples minimal and focused |

## Checking Character Count

Use this command to check character count:

```bash
wc -m .windsurf/rules
```

Stay well under 12,000 to leave room for updates.

## What to Include

**High Priority** (include these):
- Project-specific tech stack
- Directory structure and naming conventions
- API patterns unique to your project
- Custom tooling and scripts
- Environment-specific configuration
- Team conventions and workflows

**Low Priority** (skip these):
- General programming best practices
- Language syntax explanations
- Framework basics (React, TypeScript)
- Obvious code quality rules
- Verbose explanations of standard patterns

## Example: Full Stack Project

```markdown
# TaskMaster Development Guide

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

## Compression Techniques

**Verbose (100+ words):**
```markdown
When you are working with React components, it's very important to remember
that you should always use functional components with hooks instead of class
components. This is because hooks provide a more modern and flexible way to
manage state and side effects. Additionally, you should keep your components
small and focused on a single responsibility...
```

**Concise (30 words):**
```markdown
## React Components

- Use functional components with hooks (no classes)
- Keep under 200 lines
- Single responsibility
- Custom hooks for complex logic
```

## Migration from Other Formats

When converting to Windsurf:

1. **Strip all frontmatter** - Remove YAML headers completely
2. **Combine multiple files** - Merge into single document
3. **Prioritize content** - Keep project-specific, remove generic
4. **Trim examples** - Only essential code samples
5. **Monitor length** - Check character count regularly

## Validation

Documentation: `/Users/khaliqgant/Projects/prpm/app/packages/converters/docs/windsurf.md`

Schema location: `/Users/khaliqgant/Projects/prpm/app/packages/converters/schemas/windsurf.schema.json`

## Best Practices

1. **Be concise** - 12,000 character limit means prioritize
2. **Single file** - Combine all project context cohesively
3. **Clear structure** - Use headers for scannable sections
4. **Real examples** - Show actual code patterns from project
5. **Update regularly** - Keep in sync with architecture changes
6. **No frontmatter** - Plain markdown only, no YAML

---

**Remember**: Windsurf uses plain markdown with NO frontmatter. 12,000 character limit. Single `.windsurf/rules` file.
