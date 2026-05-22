---
name: docs-generate
description: "Generate documentation for code, APIs, and components"
---

# Documentation Generator

Generate comprehensive documentation for the following code.

## Code to Document

$ARGUMENTS

## Documentation Strategy for Solo Developers

### 1. **Documentation Types**

**Code Documentation**
- JSDoc/TSDoc comments
- Function/method descriptions
- Parameter descriptions
- Return types and values
- Usage examples

**API Documentation**
- Endpoint descriptions
- Request/response formats
- Authentication requirements
- Error codes
- Examples with curl/fetch

**Component Documentation**
- Props interface
- Usage examples
- Visual examples
- Accessibility notes

**README Documentation**
- Project overview
- Setup instructions
- Environment variables
- Available scripts
- Deployment guide

### 2. **JSDoc/TSDoc Format**

```typescript
/**
 * Fetches user data from the database
 *
 * @param userId - The unique identifier for the user
 * @param options - Optional fetch parameters
 * @returns Promise resolving to user data
 * @throws {NotFoundError} When user doesn't exist
 * @throws {DatabaseError} When database query fails
 *
 * @example
 * ```typescript
 * const user = await getUser('123', { includeProfile: true })
 * console.log(user.email)
 * ```
 */
async function getUser(
  userId: string,
  options?: FetchOptions
): Promise<User> {
  // implementation
}
```

### 3. **API Documentation**

```markdown
## POST /api/users

Create a new user account.

### Authentication
Requires valid API key in `Authorization` header.

### Request Body
json
{
  "email": "user@example.com",
  "name": "John Doe",
  "role": "user"
}

### Response (201 Created)
json
{
  "id": "user_123",
  "email": "user@example.com",
  "name": "John Doe",
  "createdAt": "2025-01-01T00:00:00Z"
}

### Errors
- `400` - Invalid request body
- `401` - Missing or invalid API key
- `409` - Email already exists
- `500` - Server error
```

### 4. **Component Documentation**

```typescript
/**
 * UserCard Component
 *
 * Displays user information in a card layout with avatar,
 * name, email, and optional actions.
 *
 * @component
 * @example
 * ```tsx
 * <UserCard
 *   user={userData}
 *   onEdit={() => handleEdit(userData.id)}
 *   showActions={true}
 * />
 * ```
 */
interface UserCardProps {
  /** User data to display */
  user: User

  /** Optional callback when edit button is clicked */
  onEdit?: () => void

  /** Whether to show action buttons (default: false) */
  showActions?: boolean

  /** Additional CSS classes */
  className?: string
}

export function UserCard({
  user,
  onEdit,
  showActions = false,
  className
}: UserCardProps) {
  // implementation
}
```

### 5. **README Template**

```markdown
# Project Name

Brief description of what the project does.

## Features

- Feature 1
- Feature 2
- Feature 3

## Tech Stack

- Next.js 15
- React 19
- TypeScript
- Tailwind CSS
- Supabase

## Getting Started

### Prerequisites

- Node.js 18+
- npm or pnpm

### Installation

# Clone the repository
git clone https://github.com/username/project.git

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env.local

### Environment Variables

DATABASE_URL=           # Supabase database URL
NEXT_PUBLIC_API_URL=    # API endpoint

### Development

npm run dev            # Start dev server
npm run build          # Build for production
npm run start          # Start production server
npm test               # Run tests
npm run lint           # Run linter

## Project Structure

app/                # Next.js app directory
components/         # React components
lib/                # Utilities and helpers
types/              # TypeScript types
public/             # Static assets

## Deployment

Deployed on Vercel. Push to `main` branch triggers auto-deploy.

## License

MIT
```

### 6. **Inline Documentation Best Practices**

**Good Comments**
```typescript
// Cache expensive calculation for 5 minutes
const cachedResult = useMemo(() =>
  complexCalculation(data), [data]
)

// Retry failed requests up to 3 times with exponential backoff
const result = await retry(apiCall, { maxAttempts: 3 })
```

**Bad Comments** (Don't document the obvious)
```typescript
// Set x to 5
const x = 5

// Loop through items
items.forEach(item => { })
```

### 7. **Auto-Generated Docs**

**TypeDoc** (for TypeScript projects)
```bash
npm install -D typedoc
npx typedoc --out docs src
```

**Storybook** (for React components)
```bash
npx storybook@latest init
npm run storybook
```

## What to Generate

1. **JSDoc Comments** - For all exported functions/classes
2. **README Section** - Relevant project documentation
3. **API Docs** - For API routes (if applicable)
4. **Component Props** - TypeScript interface with descriptions
5. **Usage Examples** - Real-world code examples
6. **Troubleshooting** - Common issues and solutions

Focus on documentation that helps future you (or other developers) understand and use the code quickly. Don't document the obvious.
