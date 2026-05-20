---
description: Explain what code does line by line so you can understand and learn from it.
---

# Explain Code

Explain what code does, line by line, so you can understand and learn from it.

## Instructions

When the user asks you to explain code:

### Step 1: Identify the Code

If the user provides a file path, read that file. If they paste code directly, use that.

If no code is specified, ask:
> "What code would you like me to explain? Please provide a file path or paste the code."

### Step 2: Provide Overview

Start with a high-level summary:
- What is the purpose of this code?
- What problem does it solve?
- How does it fit into the larger application?

### Step 3: Walk Through Line by Line

For each significant section, explain:
- **What** it does (literally)
- **Why** it's needed (purpose)
- **How** it works (mechanism)

Use this format:

```
Lines X-Y: [Brief description]
- This code [what it does]
- It's needed because [why]
- It works by [how]
```

### Step 4: Highlight Key Concepts

Point out important patterns and concepts:
- Design patterns used
- Language features that might be unfamiliar
- Best practices demonstrated
- Potential gotchas or edge cases

### Step 5: Summarize

End with:
- Key takeaways
- What the user should understand now
- Suggestions for further learning if applicable

## Example Output

```
## Overview

This is a React custom hook that manages authentication state. It handles
login, logout, and automatic token refresh.

## Line-by-Line Explanation

### Lines 1-5: Imports
```typescript
import { useState, useEffect, useCallback } from 'react';
import { authApi } from '@/services/api';
import { User } from '@/types';
```
- Imports React hooks for state management and side effects
- Imports the auth API service for making authentication requests
- Imports the User type for type safety

### Lines 7-15: Hook Definition and State
```typescript
export function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
```
- Creates a custom hook that can be used in any component
- `user` state holds the current user (or null if logged out)
- `loading` state tracks whether we're still checking auth status
- Starting with `loading: true` prevents flash of unauthenticated content

### Lines 17-30: Auto-refresh Effect
[... continue explanation ...]

## Key Concepts

1. **Custom Hooks**: Reusable logic extracted from components
2. **Optimistic Updates**: UI updates before server confirms
3. **Token Refresh**: Automatic re-authentication before expiry

## Takeaways

- This hook centralizes all auth logic in one place
- Components just need to call `useAuth()` to access auth state
- The refresh logic runs automatically in the background
```

## Tips for Users

Ask me to explain:
- "Explain this function" (paste code)
- "Explain src/hooks/useAuth.ts"
- "Explain lines 50-100 of api.ts"
- "What does this regex do?"
- "Why is this pattern used here?"

I'll adjust the depth based on what you ask. For simple code, I'll be brief. For complex code, I'll be thorough.
