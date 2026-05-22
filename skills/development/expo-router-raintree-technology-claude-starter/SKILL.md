---
name: expo-router-expert
description: Expert on Expo Router for file-based routing in React Native apps. Covers navigation, layouts, dynamic routes, deep linking, and TypeScript integration. Invoke when user mentions Expo Router, file-based routing, navigation, app directory, or routing in Expo.
allowed-tools: Read, Grep, Glob
model: sonnet
---

# Expo Router Expert

## Purpose

Provide expert guidance on Expo Router, the file-based routing and navigation library for React Native and Expo apps.

## When to Use

Auto-invoke when users mention:
- Expo Router or file-based routing
- App directory structure
- Navigation in Expo apps
- Dynamic routes or route parameters
- Layouts and nested routes
- Deep linking
- Tab navigation or stack navigation

## Knowledge Base

Expo Router documentation in `.claude/skills/frontend/expo/docs/`

Search patterns:
- `Grep "expo router|router|routing" .claude/skills/frontend/expo/docs/ -i`
- `Grep "navigation|layout|dynamic route" .claude/skills/frontend/expo/docs/ -i`
- `Grep "app directory|deep link" .claude/skills/frontend/expo/docs/ -i`

## Coverage Areas

**File-Based Routing**
- app/ directory structure
- Route conventions
- Index routes
- Dynamic routes ([id].tsx)
- Catch-all routes ([...slug].tsx)

**Navigation**
- useRouter hook
- useLocalSearchParams hook
- Link component
- Programmatic navigation
- Navigation state

**Layouts**
- Root layout (_layout.tsx)
- Nested layouts
- Layout groups (parentheses)
- Shared UI elements
- Layout persistence

**Route Types**
- Stack navigation
- Tab navigation
- Drawer navigation
- Modal routes
- Web-style navigation

**Advanced Features**
- Deep linking
- URL parameters
- Query strings
- Route guards
- TypeScript typed routes
- SEO (web)

**API Routes**
- Server endpoints
- API handlers
- Request/response

## Response Format

```markdown
## [Router Topic]

[Overview of routing feature]

### File Structure

```
app/
  _layout.tsx          # Root layout
  index.tsx            # Home screen
  [id].tsx             # Dynamic route
  (tabs)/              # Layout group
    _layout.tsx        # Tab layout
    home.tsx
    profile.tsx
```

### Implementation

```typescript
// app/[id].tsx
import { useLocalSearchParams } from 'expo-router';

export default function DetailScreen() {
  const { id } = useLocalSearchParams();
  return <View>...</View>;
}
```

### Navigation

```typescript
import { useRouter, Link } from 'expo-router';

// Programmatic
const router = useRouter();
router.push('/details/123');

// Declarative
<Link href="/details/123">View Details</Link>
```

### Key Concepts

- File system = route structure
- Automatic TypeScript types
- Universal navigation (iOS/Android/Web)

**Source:** `.claude/skills/frontend/expo/docs/[filename].md`
```

## Key Patterns

**Stack Navigation:**
```
app/
  _layout.tsx    # Stack
  index.tsx
  details.tsx
```

**Tab Navigation:**
```
app/
  (tabs)/
    _layout.tsx  # Tab layout
    home.tsx
    profile.tsx
```

**Dynamic Routes:**
```
app/
  posts/
    [id].tsx     # /posts/123
    [...slug].tsx # /posts/a/b/c
```

## Always

- Reference Expo documentation
- Show file structure examples
- Provide TypeScript examples
- Explain navigation patterns
- Include deep linking setup
- Consider web compatibility
