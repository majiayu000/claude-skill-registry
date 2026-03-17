---
name: frontend-architecture
description: |
  This skill structures frontend code for scalability, readability, and API interaction. It establishes patterns for organizing frontend code beyond routing, including component organization, state management, and integration with backend APIs. Use when designing overall frontend code organization, planning component library structure, or establishing state management patterns.
allowed-tools: Read, Grep, Glob
---

# Frontend Architecture

## What This Skill Does

This skill structures frontend code for scalability, readability, and API interaction. It establishes patterns for organizing frontend code beyond routing, including component organization, state management, and integration with backend APIs.

## When to Use

- When designing overall frontend code organization
- When planning component library structure
- When establishing state management patterns
- When defining API integration patterns
- When creating reusable component systems
- When scaling frontend codebase organization

## When NOT to Use

- When working on backend code
- When designing routing (use nextjs-app-router)
- When implementing specific components
- When specifications haven't defined frontend requirements
- When frontend technology stack isn't confirmed

## Required Clarifications

Before implementing frontend architecture, clarify:

1. **Technology Stack**: Which frontend framework/library (React, Vue, Angular)?
2. **Application Type**: SPA, SSR, static site, or hybrid?
3. **State Management**: Simple useState, Context, Redux, Zustand, or other?
4. **UI Framework**: Tailwind, Material UI, custom CSS, or other?
5. **Team Size**: Small team, large team, or enterprise scale?

## Component Organization Patterns

### Feature-Based Structure
```
src/
├── components/
│   ├── ui/                 # Reusable UI components
│   │   ├── Button/
│   │   ├── Input/
│   │   └── Card/
│   ├── features/           # Feature-specific components
│   │   ├── auth/
│   │   ├── dashboard/
│   │   └── profile/
│   └── layouts/            # Layout components
│       ├── MainLayout/
│       └── AuthLayout/
├── hooks/                  # Custom hooks
│   ├── auth/
│   ├── data/
│   └── utils/
├── lib/                    # Utilities and helpers
│   ├── api/
│   ├── utils/
│   └── constants/
├── types/                  # TypeScript definitions
│   ├── globals.ts
│   └── features/
└── styles/                 # Global styles
    ├── globals.css
    └── themes/
```

### Page-Based Structure (Next.js App Router)
```
app/
├── (auth)/                 # Authenticated routes
│   ├── login/
│   └── signup/
├── (public)/               # Public routes
│   ├── home/
│   └── about/
├── dashboard/              # Protected routes
│   ├── layout.tsx
│   ├── page.tsx
│   └── components/
├── components/             # Shared components
│   ├── ui/                # Base UI components
│   └── features/          # Feature components
├── hooks/                  # Custom hooks
├── lib/                    # Utilities
│   ├── api/
│   └── utils/
└── types/                  # Type definitions
```

## State Management Strategies

### Global State Solutions
- **Small Apps**: React Context API
- **Medium Apps**: Zustand, Jotai
- **Large Apps**: Redux Toolkit, MobX
- **Data Heavy**: Apollo Client, RTK Query

### State Organization
```typescript
// stores/
├── auth/
│   ├── slice.ts          // Redux slice
│   ├── selectors.ts      // Selector functions
│   └── thunks.ts         // Async actions
├── ui/
│   ├── themeSlice.ts
│   └── modalSlice.ts
└── data/
    ├── userSlice.ts
    └── cacheSlice.ts
```

## API Integration Patterns

### Client-Side Data Fetching
```typescript
// lib/api/
├── client.ts             // API client instance
├── auth.ts              // Authentication endpoints
├── user.ts              // User endpoints
├── posts.ts             // Posts endpoints
└── types.ts             # API response types
```

### Hooks for Data Management
```typescript
// hooks/
├── useAuth.ts           // Authentication state
├── useUser.ts           // User data
├── usePosts.ts          // Posts data
└── useApi.ts            // Generic API hooks
```

## Styling Approaches

### Utility-First (Tailwind)
```typescript
// components/ui/Button.tsx
export const Button = ({ variant, size, className, ...props }) => {
  const baseClasses = "inline-flex items-center justify-center rounded-md font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50"

  const variantClasses = {
    primary: "bg-primary text-primary-foreground hover:bg-primary/90",
    secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/80",
  }

  return (
    <button
      className={`${baseClasses} ${variantClasses[variant]} ${className}`}
      {...props}
    />
  )
}
```

### Component-Based Styling (Styled Components)
```typescript
// components/ui/styled/Button.styled.ts
import styled from 'styled-components'

export const StyledButton = styled.button<{
  variant?: 'primary' | 'secondary'
  size?: 'sm' | 'md' | 'lg'
}>`
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 0.375rem;
  font-weight: 500;
  transition-property: background-color, border-color, color, box-shadow;

  ${({ variant }) => variant === 'primary' && `
    background-color: var(--primary);
    color: var(--primary-foreground);
  `}
`
```

## Performance Optimization

### Code Splitting
```typescript
// components/lazy/
const LazyDashboard = lazy(() => import('./Dashboard'))
const LazyProfile = lazy(() => import('./Profile'))

// routes/
const DashboardRoute = () => (
  <Suspense fallback={<LoadingSpinner />}>
    <LazyDashboard />
  </Suspense>
)
```

### Component Memoization
```typescript
// Use useMemo for expensive calculations
const ExpensiveComponent = ({ data, filters }) => {
  const processedData = useMemo(() => {
    return data.filter(item =>
      filters.some(filter => item.category === filter)
    ).sort((a, b) => a.name.localeCompare(b.name))
  }, [data, filters])

  return <List items={processedData} />
}

// Use memo for components that render frequently
export const UserProfile = memo(({ user }) => {
  return (
    <div className="user-profile">
      <img src={user.avatar} alt={user.name} />
      <span>{user.name}</span>
    </div>
  )
})
```

## Testing Strategy

### Component Testing Structure
```
components/
├── Button/
│   ├── Button.tsx
│   ├── Button.test.tsx
│   └── Button.stories.tsx
└── UserProfile/
    ├── UserProfile.tsx
    ├── UserProfile.test.tsx
    └── UserProfile.integration.test.tsx
```

### Testing Types
- **Unit Tests**: Individual component functionality
- **Integration Tests**: Component interactions
- **End-to-End Tests**: Full user flows

## Security Considerations

### Input Validation
- Sanitize user inputs before rendering
- Validate data from external APIs
- Use proper encoding for dynamic content

### Authentication Integration
- Secure token storage (preferably httpOnly cookies)
- Proper session management
- CSRF protection

## Accessibility Standards

### ARIA Labels and Roles
```typescript
// components/AccessibleButton.tsx
interface AccessibleButtonProps {
  label: string
  onClick: () => void
  disabled?: boolean
}

export const AccessibleButton = ({
  label,
  onClick,
  disabled = false
}: AccessibleButtonProps) => {
  return (
    <button
      aria-label={label}
      onClick={onClick}
      disabled={disabled}
      tabIndex={disabled ? -1 : 0}
      className={disabled ? 'opacity-50 cursor-not-allowed' : ''}
    >
      {label}
    </button>
  )
}
```

## Anti-Patterns to Avoid

- **Component Soup**: All components in single directory
- **Prop Drilling**: Passing props through many component layers
- **State Scatter**: State management without clear patterns
- **Type Absence**: Missing TypeScript interfaces and types
- **Utility Chaos**: Helper functions scattered without organization
- **Excessive Coupling**: Components tightly coupled to each other
- **Naming Inconsistency**: Different naming conventions throughout

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Existing structure, patterns, conventions to integrate with |
| **Conversation** | User's specific requirements, constraints, preferences |
| **Skill References** | Domain patterns from `references/` (library docs, best practices, examples) |
| **User Guidelines** | Project-specific conventions, team standards |

## Interaction With Other Skills

- **nextjs-app-router**: Provides routing context for architecture
- **api-client-design**: Integrates API clients into architecture
- **auth-aware-ui**: Coordinates auth state within architecture
- **better-auth-integration**: Houses auth integration code
- **monorepo-architecture**: Fits within monorepo frontend directory

## Phase Applicability

Phase II only. Phase I uses console interface without web frontend.
