---
name: scaffolder
description: Generates boilerplate code following loaded rules. Creates new components, modules, APIs, and features that automatically comply with your coding standards. Extracts patterns from rules and applies them consistently.
context:fork: true
model: sonnet
allowed-tools: read, write, glob, search, codebase_search
version: 2.1
executable: .claude/skills/scaffolder/scripts/scaffold.mjs
test_suite: .claude/skills/scaffolder/scripts/test-scaffold.mjs
best_practices:
  - Identify target framework from manifest.yaml
  - Extract patterns from relevant rule files
  - Generate complete file structure (types, tests, etc.)
  - Follow project naming conventions
  - Include proper imports and exports
  - Use executable script for programmatic invocation
error_handling: graceful
streaming: supported
templates: [component, client-component, api, fastapi-route, test, hook, context, feature]
---

<identity>
Rule-Aware Scaffolder - Creates new code that automatically adheres to your project's coding standards.
</identity>

<capabilities>
- Creating new React/Vue/Angular components
- Adding new API endpoints or routes
- Setting up new modules or packages
- Generating test files for existing code
- Creating data models or database schemas
- Bootstrapping feature directories
</capabilities>

<instructions>
<execution_process>

### Step 1: Load Rule Index

Load the rule index to discover relevant rules dynamically:

- @.claude/context/rule-index.json

### Step 2: Identify Target Framework and Query Index

Determine which technologies apply based on what you're scaffolding:

**Component scaffolding**:

- Detect: React, Next.js, TypeScript
- Query: `index.technology_map['react']`, `index.technology_map['nextjs']`, `index.technology_map['typescript']`

**API Route scaffolding**:

- Detect: Next.js App Router or FastAPI
- Query: `index.technology_map['nextjs']` or `index.technology_map['fastapi']`

**Test File scaffolding**:

- Detect: Jest, Cypress, Playwright, Vitest, pytest
- Query: `index.technology_map['jest']`, `index.technology_map['cypress']`, etc.

**Database Model scaffolding**:

- Detect: Prisma, SQL, database patterns
- Query: `index.technology_map['prisma']` or database-related rules

### Step 3: Load Relevant Rules

Load only the relevant rule files from the index (progressive disclosure):

- Master rules first (from `.claude/rules-master/`)
- Library rules supplement (from `.claude/rules-library/`)
- Load 3-5 most relevant rules, not all 1,081

### Step 4: Extract Patterns from Rules

Parse the loaded rule files to extract scaffolding patterns:

**From Next.js rules** (TECH_STACK_NEXTJS.md or nextjs.mdc):

- Server Components by default
- 'use client' only when needed
- Place in `app/` for routes, `components/` for shared
- Use lowercase-with-dashes for directories

**From TypeScript rules**:

- Interfaces for object shapes
- Proper return type annotations
- Avoid `any`, use `unknown`
- PascalCase for types/interfaces

**From React rules**:

- Functional components only
- Custom hooks for reusable logic
- Props interface for each component
- Error boundaries for critical sections

### Step 5: Check for Template Blocks

Before generating code, check for explicit template blocks in loaded rule files:

1. **Look for `<template>` blocks** in rule files:
   - Pattern: `<template name="component">...</template>`
   - Pattern: `<template name="api">...</template>`
   - Extract template content and variables (e.g., `{{Name}}`, `{{Props}}`)

2. **Template Priority**:
   - **First**: Use `<template>` blocks from loaded rule files (most specific)
   - **Second**: Use explicit templates from `.claude/templates/` directory
   - **Third**: Infer patterns from rule text (fallback)

3. **Template Validation**:
   - Verify template file exists (if using `.claude/templates/`)
   - Check template syntax is valid
   - Ensure required template variables are provided
   - Validate template structure matches expected output type

### Step 6: Generate Compliant Code

Apply extracted patterns or templates to generate code that passes rule-auditor.

### Step 7: Validate Generated Code

After generating code, validate it matches the template and rules:

1. **Template Validation**:
   - Check generated code matches template structure (if template was used)
   - Verify all template variables were replaced
   - Ensure no template placeholders remain (e.g., `{{Name}}`)

2. **Rule Compliance Validation**:
   - Run rule-auditor on generated code
   - Fix any violations found
   - Ensure generated code follows all loaded rules

3. **Structure Validation**:
   - Verify file structure matches expected (imports, exports, etc.)
   - Check naming conventions are followed
   - Ensure proper file organization
     </execution_process>

<best_practices>

1. **Always Audit After**: Run `/audit` after scaffolding to catch any edge cases
2. **Customize Templates**: Add project-specific patterns to rules for consistent generation
3. **Use for Consistency**: Scaffold even simple files to maintain team conventions
4. **Review Generated Code**: Scaffolded code is a starting point, not final implementation
5. **Keep Rules Updated**: As patterns evolve, update rules so scaffolder stays current
   </best_practices>

<integration>
### Component Generation Flow

```
1. User: /scaffold component UserDashboard
2. Scaffolder reads: nextjs.mdc, typescript.mdc, react.mdc
3. Extracts patterns: Server Component, Suspense, interfaces
4. Generates compliant code structure
5. Writes files to correct locations
6. Runs rule-auditor to verify compliance
7. Reports any manual adjustments needed
```

### Feature Module Generation

For larger features, scaffold generates a complete module:

```
/scaffold feature user-management

Generates:
app/
└── (dashboard)/
    └── users/
        ├── page.tsx           # List page
        ├── [id]/
        │   └── page.tsx       # Detail page
        ├── new/
        │   └── page.tsx       # Create page
        └── components/
            ├── user-list.tsx
            ├── user-card.tsx
            └── user-form.tsx
components/
└── users/
    └── ... (shared components)
lib/
└── users/
    ├── api.ts                 # API functions
    ├── types.ts               # Type definitions
    └── validations.ts         # Zod schemas
```

</integration>
</instructions>

<examples>
<code_example>
**Next.js Server Component**

**Command**: `/scaffold component UserProfile`

**Generated**: `components/user-profile/index.tsx`

```tsx
// Server Component (default per nextjs.mdc)
// Location: components/user-profile/ (lowercase-with-dashes per nextjs.mdc)

import { Suspense } from 'react';
import { UserProfileSkeleton } from './skeleton';
import { UserProfileContent } from './content';

// Interface defined (per typescript.mdc)
interface UserProfileProps {
  userId: string;
  showDetails?: boolean;
}

// Async Server Component for data fetching (per nextjs.mdc > Data Fetching)
export async function UserProfile({ userId, showDetails = false }: UserProfileProps) {
  return (
    // Suspense boundary (per nextjs.mdc > Components)
    <Suspense fallback={<UserProfileSkeleton />}>
      <UserProfileContent userId={userId} showDetails={showDetails} />
    </Suspense>
  );
}

// Default export for dynamic imports (per nextjs.mdc)
export default UserProfile;
```

**Also generates**:

- `components/user-profile/content.tsx` - Async content component
- `components/user-profile/skeleton.tsx` - Loading skeleton
- `components/user-profile/types.ts` - Shared types
- `components/user-profile/index.ts` - Barrel export
  </code_example>

<code_example>
**Next.js Client Component**

**Command**: `/scaffold client-component SearchBar`

**Generated**: `components/search-bar/index.tsx`

```tsx
'use client'; // Required for useState (per nextjs.mdc > Components)

import { useState, useCallback } from 'react';
import { useDebounce } from '@/hooks/use-debounce';

// Props interface (per typescript.mdc)
interface SearchBarProps {
  onSearch: (query: string) => void;
  placeholder?: string;
  debounceMs?: number;
}

// Functional component (per react.mdc)
export function SearchBar({
  onSearch,
  placeholder = 'Search...',
  debounceMs = 300,
}: SearchBarProps) {
  // Minimal client state (per nextjs.mdc > State Management)
  const [query, setQuery] = useState('');

  // Debounced callback (per nextjs.mdc > Performance)
  const debouncedSearch = useDebounce(onSearch, debounceMs);

  const handleChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const value = e.target.value;
      setQuery(value);
      debouncedSearch(value);
    },
    [debouncedSearch]
  );

  return (
    <input
      type="search"
      value={query}
      onChange={handleChange}
      placeholder={placeholder}
      className="w-full px-4 py-2 border rounded-lg" // Tailwind (per tailwind.mdc)
      aria-label={placeholder} // Accessibility
    />
  );
}

export default SearchBar;
```

</code_example>

<code_example>
**Next.js API Route (App Router)**

**Command**: `/scaffold api users`

**Generated**: `app/api/users/route.ts`

```tsx
import { NextRequest, NextResponse } from 'next/server';
import { z } from 'zod'; // Zod for validation (per nextjs.mdc > Forms and Validation)

// Request schema (per typescript.mdc > Type System)
const CreateUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(2),
});

// Response type (per typescript.mdc)
interface UserResponse {
  id: string;
  email: string;
  name: string;
  createdAt: string;
}

// GET handler (per nextjs.mdc > Routing)
export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const page = parseInt(searchParams.get('page') ?? '1');
    const limit = parseInt(searchParams.get('limit') ?? '10');

    // TODO: Replace with actual database query
    const users: UserResponse[] = [];

    return NextResponse.json({
      data: users,
      pagination: { page, limit, total: 0 },
    });
  } catch (error) {
    // Proper error handling (per nextjs.mdc > Data Fetching)
    console.error('Failed to fetch users:', error);
    return NextResponse.json({ error: 'Failed to fetch users' }, { status: 500 });
  }
}

// POST handler with validation
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    // Server-side validation (per nextjs.mdc > Forms and Validation)
    const validated = CreateUserSchema.parse(body);

    // TODO: Replace with actual database insert
    const user: UserResponse = {
      id: crypto.randomUUID(),
      ...validated,
      createdAt: new Date().toISOString(),
    };

    return NextResponse.json({ data: user }, { status: 201 });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json(
        { error: 'Validation failed', details: error.errors },
        { status: 400 }
      );
    }
    console.error('Failed to create user:', error);
    return NextResponse.json({ error: 'Failed to create user' }, { status: 500 });
  }
}
```

</code_example>

<code_example>
**FastAPI Endpoint**

**Command**: `/scaffold fastapi-route users`

**Generated**: `app/routers/users.py`

```python
"""User management endpoints."""
# Type hints required (per python.mdc)
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, EmailStr, Field

# Router with tags (per fastapi.mdc > API Design)
router = APIRouter(prefix="/users", tags=["users"])


# Pydantic models (per fastapi.mdc > Components and Validation)
class UserCreate(BaseModel):
    """Schema for creating a user."""
    email: EmailStr
    name: str = Field(..., min_length=2, max_length=100)


class UserResponse(BaseModel):
    """Schema for user response."""
    id: UUID
    email: EmailStr
    name: str
    created_at: str

    class Config:
        from_attributes = True


class PaginatedResponse(BaseModel):
    """Paginated response wrapper."""
    data: list[UserResponse]
    total: int
    page: int
    limit: int


# Dependency injection (per fastapi.mdc > Dependency Injection)
async def get_db():
    """Database session dependency."""
    # TODO: Replace with actual database session
    yield None


# GET endpoint with pagination (per fastapi.mdc > Performance)
@router.get("", response_model=PaginatedResponse)
async def list_users(
    db: Annotated[None, Depends(get_db)],
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
) -> PaginatedResponse:
    """
    List all users with pagination.

    - **page**: Page number (starting from 1)
    - **limit**: Items per page (max 100)
    """
    # TODO: Replace with actual database query
    users: list[UserResponse] = []
    total = 0

    return PaginatedResponse(data=users, total=total, page=page, limit=limit)


# POST endpoint with validation
@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    db: Annotated[None, Depends(get_db)],
) -> UserResponse:
    """
    Create a new user.

    - **email**: Valid email address
    - **name**: User's display name (2-100 chars)
    """
    # TODO: Replace with actual database insert
    # Check for existing user, create, return

    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Database integration pending",
    )


# GET by ID endpoint
@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: UUID,
    db: Annotated[None, Depends(get_db)],
) -> UserResponse:
    """Get a specific user by ID."""
    # TODO: Replace with actual database query
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User {user_id} not found",
    )
```

</code_example>

<code_example>
**Test File (Vitest/Jest)**

**Command**: `/scaffold test components/user-profile`

**Generated**: `components/user-profile/__tests__/index.test.tsx`

```tsx
// Test file (per jest-*.mdc / vitest-*.mdc patterns)
import { render, screen, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { UserProfile } from '../index';

// Mock external dependencies (per testing best practices)
vi.mock('@/lib/api', () => ({
  fetchUser: vi.fn(),
}));

describe('UserProfile', () => {
  // Clear mocks before each test (per clean-code.mdc)
  beforeEach(() => {
    vi.clearAllMocks();
  });

  // Descriptive test names (per testing guidelines)
  it('renders loading skeleton initially', () => {
    render(<UserProfile userId="123" />);

    expect(screen.getByTestId('user-profile-skeleton')).toBeInTheDocument();
  });

  it('displays user information after loading', async () => {
    const mockUser = {
      id: '123',
      name: 'John Doe',
      email: 'john@example.com',
    };

    const { fetchUser } = await import('@/lib/api');
    vi.mocked(fetchUser).mockResolvedValue(mockUser);

    render(<UserProfile userId="123" />);

    await waitFor(() => {
      expect(screen.getByText('John Doe')).toBeInTheDocument();
      expect(screen.getByText('john@example.com')).toBeInTheDocument();
    });
  });

  it('handles error state gracefully', async () => {
    const { fetchUser } = await import('@/lib/api');
    vi.mocked(fetchUser).mockRejectedValue(new Error('Network error'));

    render(<UserProfile userId="123" />);

    await waitFor(() => {
      expect(screen.getByText(/failed to load/i)).toBeInTheDocument();
    });
  });

  // Edge cases (per qa best practices)
  it('shows details when showDetails prop is true', async () => {
    render(<UserProfile userId="123" showDetails />);

    await waitFor(() => {
      expect(screen.getByTestId('user-details-section')).toBeInTheDocument();
    });
  });
});
```

</code_example>

<code_example>
**Cypress E2E Test**

**Command**: `/scaffold e2e-test user-flow`

**Generated**: `cypress/e2e/user-flow.cy.ts`

```typescript
// E2E test (per cypress-e2e-testing-*.mdc)
describe('User Flow', () => {
  // Setup before tests (per cypress best practices)
  beforeEach(() => {
    // Reset state and seed data
    cy.task('db:seed');
    cy.visit('/');
  });

  // Critical user flow (per cypress-e2e-testing guidelines)
  it('allows user to sign up, login, and view profile', () => {
    // Use data-testid selectors (per cypress best practices)
    cy.get('[data-testid="signup-link"]').click();

    // Fill signup form
    cy.get('[data-testid="email-input"]').type('test@example.com');
    cy.get('[data-testid="password-input"]').type('SecurePass123!');
    cy.get('[data-testid="name-input"]').type('Test User');
    cy.get('[data-testid="signup-submit"]').click();

    // Verify redirect to dashboard
    cy.url().should('include', '/dashboard');

    // Navigate to profile
    cy.get('[data-testid="profile-link"]').click();

    // Verify profile data
    cy.get('[data-testid="profile-name"]').should('contain', 'Test User');
    cy.get('[data-testid="profile-email"]').should('contain', 'test@example.com');
  });

  // API mocking example (per cypress-api-testing guidelines)
  it('handles API errors gracefully', () => {
    // Mock API failure
    cy.intercept('GET', '/api/users/*', {
      statusCode: 500,
      body: { error: 'Internal server error' },
    }).as('getUserError');

    cy.visit('/profile');

    // Wait for mocked request
    cy.wait('@getUserError');

    // Verify error handling
    cy.get('[data-testid="error-message"]')
      .should('be.visible')
      .and('contain', 'Failed to load profile');

    // Verify retry option
    cy.get('[data-testid="retry-button"]').should('be.visible');
  });
});
```

</code_example>

<usage_example>
**Programmatic Usage** (recommended for automation):

```bash
# Using executable script directly
node .claude/skills/scaffolder/scripts/scaffold.mjs component UserProfile
node .claude/skills/scaffolder/scripts/scaffold.mjs client-component SearchBar --path src/components
node .claude/skills/scaffolder/scripts/scaffold.mjs api users
node .claude/skills/scaffolder/scripts/scaffold.mjs test src/components/Button.tsx

# List available templates
node .claude/skills/scaffolder/scripts/scaffold.mjs --list

# Run tests
node .claude/skills/scaffolder/scripts/test-scaffold.mjs
```

**Quick Commands** (agent invocation):

```
# Generate a Server Component
/scaffold component MyComponent

# Generate a Client Component
/scaffold client-component MyInteractiveWidget

# Generate an API route
/scaffold api resource-name

# Generate a FastAPI router
/scaffold fastapi-route resource-name

# Generate test for existing file
/scaffold test path/to/component

# Generate E2E test
/scaffold e2e-test flow-name

# Generate with specific rules
/scaffold component MyComponent --rules nextjs,typescript

# Generate in specific location
/scaffold component MyComponent --path src/features/auth

# List available scaffold templates
/scaffold --list
```

**Available Templates**:

| Template           | Framework          | Files Generated                   |
| ------------------ | ------------------ | --------------------------------- |
| `component`        | Next.js/React      | index.tsx, types.ts, skeleton.tsx |
| `client-component` | Next.js            | index.tsx with 'use client'       |
| `page`             | Next.js App Router | page.tsx, loading.tsx, error.tsx  |
| `api`              | Next.js App Router | route.ts with handlers            |
| `fastapi-route`    | FastAPI            | router file with endpoints        |
| `hook`             | React              | Custom hook with types            |
| `context`          | React              | Context provider + hook           |
| `test`             | Jest/Vitest        | Test file for component           |
| `e2e-test`         | Cypress/Playwright | E2E test spec                     |
| `model`            | Prisma             | Schema model                      |
| `migration`        | Database           | Migration file                    |

</usage_example>
</examples>
