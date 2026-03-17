---
name: recovery-coach-patterns
description: Follow Recovery Coach codebase patterns and conventions. Use when writing new code, components, API routes, or database queries. Activates for general development, code organization, styling, and architectural decisions in this project.
allowed-tools: Read,Write,Edit,Bash(npm:*,npx:*)
category: Lifestyle & Personal
tags:
  - recovery
  - patterns
  - next-js
---

# Recovery Coach Development Patterns

This skill helps you follow the established patterns and conventions in the Recovery Coach codebase.

## When to Use

✅ **USE this skill for:**
- Writing new components, pages, or API routes in Recovery Coach
- Following established code organization patterns
- Implementing database queries with Drizzle ORM
- Understanding project architecture and conventions
- Styling components to match the design system

❌ **DO NOT use for:**
- Crisis intervention implementation → use `crisis-response-protocol`
- General Next.js questions → use Next.js docs
- AI/LLM integration patterns → use `modern-drug-rehab-computer`
- Content moderation → use `recovery-community-moderator`

## Project Structure

```
src/
├── app/              # Next.js App Router
│   ├── api/          # API routes (REST endpoints)
│   │   ├── auth/     # Authentication endpoints
│   │   ├── check-in/ # Daily check-in endpoints
│   │   ├── chat/     # AI coaching endpoints
│   │   └── admin/    # Admin-only endpoints
│   ├── admin/        # Admin dashboard page
│   ├── settings/     # User settings page
│   └── page.tsx      # Home page
├── components/       # React components
│   ├── ui/           # Base UI components (Button, Card, etc.)
│   └── *.tsx         # Feature components
├── lib/              # Core business logic
│   ├── ai/           # Anthropic integration
│   ├── hipaa/        # HIPAA compliance utilities
│   ├── auth.ts       # Authentication
│   ├── db.ts         # Database connection
│   └── rate-limit.ts # Rate limiting
├── db/               # Database schema (Drizzle ORM)
│   ├── schema.ts     # Table definitions
│   └── secure-db.ts  # RLS-enforced queries
└── test/             # Test utilities

features/             # Feature manifests (YAML)
docs/                 # Documentation
scripts/              # Build and utility scripts
```

## API Route Pattern

```typescript
// src/app/api/[feature]/route.ts
import { NextResponse } from 'next/server';
import { getSession } from '@/lib/auth';
import { createRateLimiter } from '@/lib/rate-limit';
import { logPHIAccess } from '@/lib/hipaa/audit';
import { z } from 'zod';

// 1. Define rate limiter
const rateLimiter = createRateLimiter({
  windowMs: 60000,
  maxRequests: 30,
  keyPrefix: 'api:feature'
});

// 2. Define input schema
const RequestSchema = z.object({
  field: z.string().min(1).max(1000),
});

export async function POST(request: Request) {
  // 3. Check authentication
  const session = await getSession();
  if (!session) {
    return NextResponse.json(
      { error: 'Unauthorized' },
      { status: 401 }
    );
  }

  // 4. Apply rate limiting
  const rateLimitResult = await rateLimiter.check(session.userId);
  if (!rateLimitResult.allowed) {
    return NextResponse.json(
      { error: 'Rate limit exceeded' },
      { status: 429, headers: rateLimitResult.headers }
    );
  }

  // 5. Parse and validate input
  const body = await request.json();
  const parsed = RequestSchema.safeParse(body);
  if (!parsed.success) {
    return NextResponse.json(
      { error: 'Invalid input', details: parsed.error.issues },
      { status: 400 }
    );
  }

  // 6. Perform operation
  const result = await performOperation(session.userId, parsed.data);

  // 7. Audit log (if PHI)
  await logPHIAccess(session.userId, 'feature', result.id, 'CREATE');

  // 8. Return response
  return NextResponse.json(result);
}
```

## React Component Pattern

```typescript
// src/components/FeatureComponent.tsx
'use client';

import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/Button';
import { Card, CardHeader, CardContent } from '@/components/ui/Card';

interface FeatureProps {
  id: string;
  initialData?: FeatureData;
  onComplete?: (result: Result) => void;
}

export function FeatureComponent({
  id,
  initialData,
  onComplete
}: FeatureProps) {
  const [data, setData] = useState<FeatureData | null>(initialData ?? null);
  const [loading, setLoading] = useState(!initialData);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!initialData) {
      fetchData();
    }
  }, [id]);

  async function fetchData() {
    try {
      setLoading(true);
      const res = await fetch(`/api/feature/${id}`);
      if (!res.ok) throw new Error('Failed to fetch');
      const data = await res.json();
      setData(data);
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return <div className="animate-pulse">Loading...</div>;
  }

  if (error) {
    return (
      <Card className="border-destructive">
        <CardContent>Error: {error}</CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>Feature Title</CardHeader>
      <CardContent>
        {/* Content */}
      </CardContent>
    </Card>
  );
}
```

## Database Query Pattern

```typescript
// Use secure-db for user data (RLS enforced)
import { db, users, checkIns } from '@/db/secure-db';
import { eq, desc } from 'drizzle-orm';

// Get user's own data (RLS automatically filters)
async function getUserCheckIns(userId: string) {
  return db
    .select()
    .from(checkIns)
    .where(eq(checkIns.userId, userId))
    .orderBy(desc(checkIns.createdAt))
    .limit(30);
}

// For admin queries, use requireAdmin
import { requireAdmin } from '@/db/secure-db';

async function getAdminStats() {
  const admin = await requireAdmin();
  if (!admin) throw new Error('Admin required');

  // Now can query across all users
  return db.select({ count: count() }).from(users);
}
```

## Design System

### Color Palette (Therapeutic)

```css
/* From globals.css */
--navy: #1a365d;      /* Primary - trust, stability */
--teal: #319795;      /* Secondary - calm, healing */
--coral: #ed8936;     /* Accent - warmth, energy */
--cream: #fffaf0;     /* Background - comfort */
```

### Time-Based Themes

```typescript
function getTimeTheme(): 'dawn' | 'day' | 'dusk' | 'night' {
  const hour = new Date().getHours();
  if (hour >= 5 && hour < 9) return 'dawn';
  if (hour >= 9 && hour < 17) return 'day';
  if (hour >= 17 && hour < 21) return 'dusk';
  return 'night';
}
```

### Component Styling

```typescript
// Use Tailwind with design tokens
<Button
  className="bg-navy hover:bg-navy/90 text-white"
  variant="default"
>
  Primary Action
</Button>

<Card className="bg-cream border-teal/20">
  <CardContent className="text-navy">
    Therapeutic content
  </CardContent>
</Card>
```

## Testing Pattern

```typescript
// src/lib/__tests__/feature.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

describe('Feature', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('loads and displays data', async () => {
    vi.mocked(fetch).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ data: 'test' })
    } as Response);

    render(<FeatureComponent id="123" />);

    await waitFor(() => {
      expect(screen.getByText('test')).toBeInTheDocument();
    });
  });

  it('handles errors gracefully', async () => {
    vi.mocked(fetch).mockRejectedValueOnce(new Error('Network error'));

    render(<FeatureComponent id="123" />);

    await waitFor(() => {
      expect(screen.getByText(/error/i)).toBeInTheDocument();
    });
  });
});
```

## Error Handling

```typescript
// Use structured error responses
interface APIError {
  error: string;
  code?: string;
  details?: unknown;
}

// In API routes
return NextResponse.json<APIError>(
  {
    error: 'Validation failed',
    code: 'VALIDATION_ERROR',
    details: zodError.issues
  },
  { status: 400 }
);

// In components
try {
  await submitData();
} catch (e) {
  if (e instanceof APIError) {
    toast.error(e.message);
  } else {
    toast.error('An unexpected error occurred');
    console.error(e); // Log for debugging, not shown to user
  }
}
```

## Environment Variables

Required variables (validated at startup):

```bash
# Authentication
SESSION_SECRET=           # 32+ random characters

# AI Integration
ANTHROPIC_API_KEY=        # Claude API key

# Database
DATABASE_URL=             # SQLite path or connection string

# Optional
VAPID_PUBLIC_KEY=         # Push notifications
VAPID_PRIVATE_KEY=
```

## Pre-Commit Checklist

Before committing any changes:

1. [ ] `npm run lint` passes
2. [ ] `npm run test` passes
3. [ ] `npm run feature:validate` passes
4. [ ] Feature manifest updated (if applicable)
5. [ ] No secrets in code
6. [ ] HIPAA compliance maintained (audit logs)
7. [ ] Accessibility considered (semantic HTML, ARIA)

## Common Imports

```typescript
// Authentication
import { getSession, requireAuth } from '@/lib/auth';

// Database
import { db } from '@/db/secure-db';
import { eq, desc, and } from 'drizzle-orm';

// Audit
import { logPHIAccess, logSecurityEvent } from '@/lib/hipaa/audit';

// Rate limiting
import { createRateLimiter } from '@/lib/rate-limit';

// Validation
import { z } from 'zod';

// UI Components
import { Button } from '@/components/ui/Button';
import { Card, CardHeader, CardContent } from '@/components/ui/Card';
import { Input } from '@/components/ui/Input';
```
