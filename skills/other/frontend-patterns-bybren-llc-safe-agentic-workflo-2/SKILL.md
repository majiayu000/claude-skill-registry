---
name: frontend-patterns
description: Frontend patterns for Next.js App Router, Clerk auth, shadcn/Radix UI, and PostHog analytics. Use when building UI components, creating pages, implementing auth flows, or adding analytics events. Ensures consistent UX patterns and accessibility standards.
---

# Frontend Patterns Skill

## Purpose

Ensure consistent frontend development using established patterns for Next.js App Router, Clerk authentication, shadcn/ui components, and PostHog analytics.

## When This Skill Applies

Invoke this skill when:

- Building new UI components or pages
- Implementing authentication flows
- Adding forms with validation
- Integrating PostHog analytics events
- Creating protected/authenticated routes
- Working with shadcn/ui or Radix components

## Next.js App Router Patterns

### Server vs Client Components

```typescript
// SERVER COMPONENT (default) - Use for:
// - Data fetching
// - Auth checks
// - SEO-critical content
// app/dashboard/page.tsx
import { auth } from "@clerk/nextjs/server";

export default async function DashboardPage() {
  const { userId } = await auth();
  // Fetch data server-side...
}

// CLIENT COMPONENT - Use for:
// - Interactivity (onClick, onChange)
// - Browser APIs (localStorage, window)
// - Hooks (useState, useEffect)
// app/dashboard/_components/interactive-widget.tsx
("use client");

import { useState } from "react";

export function InteractiveWidget() {
  const [count, setCount] = useState(0);
  // Interactive logic...
}
```

### Protected Pages

**CRITICAL**: Always use `export const dynamic = 'force-dynamic'` for authenticated pages:

```typescript
// app/dashboard/[page]/page.tsx
import { auth } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";

// REQUIRED - Auth context unavailable at build time
export const dynamic = "force-dynamic";

export default async function ProtectedPage() {
  const { userId } = await auth();

  if (!userId) {
    redirect("/sign-in");
  }

  // Render protected content...
}
```

### Route Organization

```text
app/
├── (auth)/                    # Auth routes (sign-in, sign-up)
│   ├── sign-in/[[...sign-in]]/page.tsx
│   └── sign-up/[[...sign-up]]/page.tsx
├── (marketing)/               # Public marketing pages
│   ├── page.tsx               # Homepage
│   └── pricing/page.tsx
├── dashboard/                 # Protected user area
│   ├── page.tsx
│   └── _components/           # Page-specific components
└── admin/                     # Admin-only area
    └── page.tsx
```

## Clerk Authentication Patterns

### Auth-Enabled Mode

```typescript
// Server component auth check
import { auth } from '@clerk/nextjs/server';

export default async function Page() {
  const { userId } = await auth();
  // userId is string | null
}

// Client component auth
"use client"
import { useUser, useAuth } from '@clerk/nextjs';

export function UserProfile() {
  const { user, isLoaded, isSignedIn } = useUser();
  const { signOut } = useAuth();

  if (!isLoaded) return <Skeleton />;
  if (!isSignedIn) return <SignInPrompt />;

  return <div>Welcome, {user.firstName}!</div>;
}
```

### Auth-Disabled Mode (Feature Toggle)

When auth is disabled via feature flags, provide graceful fallbacks:

```typescript
// Check feature flag
import { FEATURES } from '@/config/features';

export function AuthWrapper({ children }) {
  if (!FEATURES.AUTH_ENABLED) {
    // Show demo/guest experience
    return <GuestExperience>{children}</GuestExperience>;
  }

  return <AuthenticatedWrapper>{children}</AuthenticatedWrapper>;
}
```

### Admin Verification

```typescript
// app/admin/page.tsx
import { auth } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";

export const dynamic = "force-dynamic";

export default async function AdminPage() {
  const { userId, orgId, orgRole } = await auth();

  if (!userId) {
    redirect("/sign-in");
  }

  // Verify admin role
  const ADMIN_ORG_ID = process.env.CLERK_ADMIN_ORG_ID;
  const ADMIN_ROLE = "org:admin";

  if (orgId !== ADMIN_ORG_ID || orgRole !== ADMIN_ROLE) {
    redirect("/admin-denied");
  }

  // Render admin content...
}
```

## shadcn/ui Component Patterns

### Import Convention

```typescript
// Always use @/components/ui path alias
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
```

### Form Pattern (React Hook Form + Zod)

```typescript
"use client"

import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { Button } from '@/components/ui/button';
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form';
import { Input } from '@/components/ui/input';

const FormSchema = z.object({
  email: z.string().email('Invalid email'),
  name: z.string().min(1, 'Name is required'),
});

type FormData = z.infer<typeof FormSchema>;

export function MyForm() {
  const form = useForm<FormData>({
    resolver: zodResolver(FormSchema),
    defaultValues: { email: '', name: '' },
  });

  async function onSubmit(data: FormData) {
    // Handle submission...
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <FormField
          control={form.control}
          name="name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Name</FormLabel>
              <FormControl>
                <Input {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit">Submit</Button>
      </form>
    </Form>
  );
}
```

### Button Variants

```typescript
// Primary action
<Button>Save Changes</Button>

// Secondary action
<Button variant="secondary">Cancel</Button>

// Destructive action
<Button variant="destructive">Delete</Button>

// Ghost/subtle
<Button variant="ghost">Learn More</Button>

// Link style
<Button variant="link" asChild>
  <Link href="/docs">Documentation</Link>
</Button>

// Loading state
<Button disabled={isLoading}>
  {isLoading ? 'Saving...' : 'Save'}
</Button>
```

## PostHog Analytics Patterns

### Event Naming Convention

Use snake_case with category prefix:

```typescript
// User actions
"user_signed_up";
"user_signed_in";
"user_profile_updated";

// Feature usage
"feature_dark_mode_toggled";
"feature_export_clicked";

// Payments
"payment_checkout_started";
"payment_completed";
"subscription_upgraded";

// Content
"content_video_watched";
"content_pdf_downloaded";

// Navigation
"page_viewed";
"cta_clicked";
```

### Event Tracking

```typescript
"use client"

import { usePostHog } from 'posthog-js/react';

export function TrackableButton() {
  const posthog = usePostHog();

  function handleClick() {
    posthog?.capture('cta_clicked', {
      button_text: 'Get Started',
      page: '/pricing',
      variant: 'primary',
    });
  }

  return <Button onClick={handleClick}>Get Started</Button>;
}
```

### Page View Tracking

```typescript
// Automatic via PostHogProvider (already configured)
// Manual tracking for SPAs:
"use client";

import { usePathname } from "next/navigation";
import { usePostHog } from "posthog-js/react";
import { useEffect } from "react";

export function PageViewTracker() {
  const pathname = usePathname();
  const posthog = usePostHog();

  useEffect(() => {
    if (pathname && posthog) {
      posthog.capture("$pageview", { path: pathname });
    }
  }, [pathname, posthog]);

  return null;
}
```

### Feature Flags

```typescript
"use client"

import { useFeatureFlagEnabled } from 'posthog-js/react';

export function FeatureFlaggedComponent() {
  const showNewFeature = useFeatureFlagEnabled('new-checkout-flow');

  if (showNewFeature) {
    return <NewCheckoutFlow />;
  }

  return <LegacyCheckoutFlow />;
}
```

## Accessibility Checklist

### Required for All Components

- [ ] **Keyboard Navigation**: All interactive elements focusable via Tab
- [ ] **Focus Indicators**: Visible focus ring (Tailwind: `focus:ring-2`)
- [ ] **Color Contrast**: 4.5:1 minimum for text
- [ ] **Alt Text**: All images have descriptive alt text
- [ ] **ARIA Labels**: Form inputs have labels or aria-label
- [ ] **Error States**: Form errors announced to screen readers

### Patterns

```typescript
// Accessible button
<Button aria-label="Close dialog">
  <X className="h-4 w-4" />
</Button>

// Accessible form field
<FormItem>
  <FormLabel htmlFor="email">Email</FormLabel>
  <FormControl>
    <Input id="email" type="email" aria-describedby="email-error" />
  </FormControl>
  <FormMessage id="email-error" />
</FormItem>

// Skip link for keyboard users
<a href="#main-content" className="sr-only focus:not-sr-only">
  Skip to main content
</a>
```

## Responsive Design Patterns

### Tailwind Breakpoints

```typescript
// Mobile-first approach
<div className="
  px-4           // Mobile: 16px padding
  md:px-6        // Tablet: 24px padding
  lg:px-8        // Desktop: 32px padding
">

// Responsive grid
<div className="
  grid
  grid-cols-1    // Mobile: 1 column
  md:grid-cols-2 // Tablet: 2 columns
  lg:grid-cols-3 // Desktop: 3 columns
  gap-4
">

// Hide/show at breakpoints
<div className="hidden md:block">Desktop only</div>
<div className="md:hidden">Mobile only</div>
```

### Container Pattern

```typescript
// Standard container
<div className="container mx-auto px-4 md:px-6">
  {/* Content */}
</div>

// Max-width constrained
<div className="max-w-4xl mx-auto px-4">
  {/* Narrower content like articles */}
</div>
```

## Common Mistakes to Avoid

### DON'T Do This

```typescript
// ❌ Missing 'use client' for interactive components
import { useState } from 'react';  // Will error!

// ❌ Using hooks in server components
export default async function Page() {
  const [state, setState] = useState();  // Will error!
}

// ❌ Missing force-dynamic on auth pages
export default async function ProtectedPage() {
  const { userId } = await auth();  // May fail at build!
}

// ❌ Direct DOM manipulation
document.getElementById('foo');  // Use refs instead

// ❌ Inline styles (use Tailwind)
<div style={{ marginTop: '20px' }}>  // Use className="mt-5"
```

### DO This Instead

```typescript
// ✅ Proper client component
"use client"
import { useState } from 'react';

// ✅ Server component with auth
export const dynamic = 'force-dynamic';
export default async function Page() {
  const { userId } = await auth();
}

// ✅ Use refs for DOM access
const inputRef = useRef<HTMLInputElement>(null);

// ✅ Tailwind classes
<div className="mt-5">
```

## Authoritative References

- **UI Patterns**: `docs/patterns/ui/`
  - `authenticated-page.md` - Protected page pattern
  - `form-with-validation.md` - React Hook Form + Zod
  - `data-table.md` - Server-side paginated tables
  - `marketing-page.md` - Public marketing pages
- **Component Library**: `components/ui/` (shadcn/ui)
- **PostHog Setup**: `lib/posthog/`
- **Feature Flags**: `config/features.ts`
