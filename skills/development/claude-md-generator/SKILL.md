---
name: claude-md-generator
description: Automatically generates claude.md files for new folders/modules following hierarchical structure. Extracts context from existing code, follows project conventions, and creates documentation that enables Claude Code to understand module-specific rules and patterns.
allowed-tools: read, write, glob, search, codebase_search
version: 1.0
best_practices:
  - Extract context from existing code in target directory
  - Follow hierarchical claude.md structure (root → subdirectories)
  - Reference parent claude.md for inheritance
  - Include module-specific rules and patterns
  - Validate generated claude.md structure
error_handling: graceful
streaming: supported
templates: [module, feature, component, api, service]
---

<identity>
claude.md Generator Skill - Automatically generates claude.md files for new folders/modules that enable Claude Code to understand module-specific rules, patterns, and conventions.
</identity>

<capabilities>
- Creating new modules or feature folders
- Adding new major components or subsystems
- Introducing new APIs or services
- Setting up new directories that need documentation
- Ensuring claude.md exists where required
</capabilities>

<instructions>
<execution_process>

### Step 1: Identify Target Location

Determine where claude.md should be created:

- Check if target directory exists
- Identify parent directory and its claude.md (if exists)
- Understand module purpose from directory structure
- Check for existing claude.md in target directory

### Step 2: Extract Context from Code

Analyze existing code to understand module:

- Read key files in target directory (index files, main components, etc.)
- Identify patterns and conventions used
- Extract dependencies and relationships
- Understand module responsibilities
- Note any special rules or guidelines

### Step 3: Load Template

Load claude.md template from `.claude/templates/claude-md-template.md`:

- Use template as base structure
- Customize sections based on module type
- Include module-specific information

### Step 4: Generate claude.md Content

Create claude.md following this structure:

```markdown
# [Module/Feature Name]

## Purpose

[What this module/feature does - extracted from code analysis]

## Key Patterns

[Important patterns and conventions found in code]

## Rules & Guidelines

[Module-specific rules and guidelines]

## Dependencies

[Key dependencies and relationships]

## Usage Examples

[How to use this module/feature - from code examples]
```

### Step 5: Inherit from Parent

If parent directory has claude.md:

- Reference parent claude.md for inherited rules
- Add module-specific overrides
- Maintain consistency with parent guidelines

### Step 6: Validate Generated File

Ensure generated claude.md:

- Follows template structure
- Has all required sections
- Uses consistent formatting
- Has valid markdown syntax
- References parent claude.md if applicable
  </execution_process>

<integration>
**Integration with Developer Agent**:
When Developer agent creates new modules:
1. Developer creates module structure
2. Developer invokes claude-md-generator: "Generate claude.md for [path]"
3. Skill analyzes code and generates claude.md
4. Developer reviews and customizes as needed

**Integration with Technical Writer Agent**:
Technical Writer agent can:

- Automatically generate claude.md for new modules
- Update existing claude.md files
- Validate claude.md files exist where required
- Ensure consistency across claude.md files
  </integration>

<best_practices>

1. **Extract from Code**: Always analyze existing code before generating
2. **Follow Hierarchy**: Reference parent claude.md for inheritance
3. **Be Specific**: Include module-specific patterns and rules
4. **Keep Updated**: Update claude.md as module evolves
5. **Validate Structure**: Ensure generated file follows template
   </best_practices>
   </instructions>

<examples>
<code_example>
**Module claude.md**

**Command**: "Generate claude.md for src/modules/auth"

**Generated**: `src/modules/auth/CLAUDE.md`

````markdown
# Authentication Module

## Purpose

Handles user authentication, authorization, and session management. Provides JWT-based authentication with refresh token support.

## Key Patterns

- Use `useAuth()` hook for authentication state
- Protect routes with `withAuth()` HOC
- Use `AuthProvider` for context management
- JWT tokens stored in httpOnly cookies

## Rules & Guidelines

- Always validate tokens server-side
- Use refresh tokens for long-lived sessions
- Implement proper error handling for auth failures
- Follow OAuth2 best practices

## Dependencies

- `@/lib/jwt` - JWT token handling
- `@/lib/db` - User database operations
- `@/hooks/use-auth` - Authentication hook

## Usage Examples

### Using Authentication Hook

```typescript
import { useAuth } from '@/modules/auth';

function MyComponent() {
  const { user, login, logout } = useAuth();
  // ...
}
```
````

### Protecting Routes

```typescript
import { withAuth } from '@/modules/auth';

export default withAuth(ProtectedPage);
```

````
</code_example>

<code_example>
**Feature claude.md**

**Command**: "Generate claude.md for app/features/user-management"

**Generated**: `app/features/user-management/CLAUDE.md`

```markdown
# User Management Feature

## Purpose
Complete user management feature including CRUD operations, user profiles, and role management.

## Key Patterns
- Server Components for data fetching
- Client Components for interactive UI
- Zod schemas for validation
- React Hook Form for form handling

## Rules & Guidelines
- Use Server Components by default
- Add 'use client' only when needed
- Validate all inputs with Zod
- Use optimistic updates for better UX

## Dependencies
- `@/lib/api` - API client
- `@/components/ui` - UI components
- `@/lib/validations` - Validation schemas

## Usage Examples

### Creating a User
```typescript
import { createUser } from '@/features/user-management/api'

const user = await createUser({
  email: 'user@example.com',
  name: 'John Doe'
})
````

````
</code_example>

<code_example>
**API Service claude.md**

**Command**: "Generate claude.md for app/api/users"

**Generated**: `app/api/users/CLAUDE.md`

```markdown
# Users API

## Purpose
RESTful API endpoints for user management operations.

## Key Patterns
- Next.js App Router route handlers
- Zod validation for request bodies
- Proper error handling with status codes
- Type-safe request/response types

## Rules & Guidelines
- Always validate request bodies
- Use proper HTTP status codes
- Return consistent error format
- Implement rate limiting
- Add authentication middleware

## Dependencies
- `@/lib/db` - Database operations
- `@/lib/validations` - Validation schemas
- `@/lib/auth` - Authentication

## Usage Examples

### GET /api/users
```bash
curl -X GET http://localhost:3000/api/users?page=1&limit=10
````

### POST /api/users

```bash
curl -X POST http://localhost:3000/api/users \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "name": "John Doe"}'
```

```
</code_example>

<usage_example>
**Quick Commands**:

```

# Generate claude.md for a module

Generate claude.md for src/modules/auth

# Generate claude.md for a feature

Generate claude.md for app/features/user-management

# Generate claude.md for an API

Generate claude.md for app/api/users

# Generate with parent reference

Generate claude.md for src/modules/auth --parent src/modules/CLAUDE.md

```

**Template Customization**:

Customize templates in `.claude/templates/claude-md-template.md`:
- Add project-specific sections
- Include standard patterns
- Define required sections
- Set formatting standards
</usage_example>
</examples>

```
