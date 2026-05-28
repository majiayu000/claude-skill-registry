---
name: nextjs
category: frontend
version: 2.0.0
description: Next.js 15 patterns with 2025-2026 design system and Australian context
author: Unite Group
priority: 3
triggers:
  - frontend
  - nextjs
  - react
  - page
  - app router
---

# Next.js 15 Patterns

## App Router Structure

```
app/
  (auth)/           # Route group for auth pages
    login/
      page.tsx
    register/
      page.tsx
    layout.tsx      # Shared auth layout
  (dashboard)/      # Route group for dashboard
    dashboard/
      page.tsx
    settings/
      page.tsx
    layout.tsx      # Dashboard layout with sidebar
  api/
    route.ts        # API routes
  layout.tsx        # Root layout (with en-AU locale)
  page.tsx          # Home page
```

## Server Components (Default)

```typescript
// app/users/page.tsx - Server Component
import { getUsers } from '@/lib/api';

export default async function UsersPage() {
  const users = await getUsers(); // Direct data fetching

  return (
    <div className="bento-grid">
      {users.map(user => (
        <UserCard key={user.id} user={user} />
      ))}
    </div>
  );
}
```

## Client Components (2025-2026 Aesthetic)

```typescript
'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';

export function Counter() {
  const [count, setCount] = useState(0);

  return (
    <motion.button
      onClick={() => setCount(c => c + 1)}
      className="glass-card hover-scale"
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
    >
      <span className="text-primary-600">Count: {count}</span>
    </motion.button>
  );
}

// Bento Grid Layout (2025-2026 aesthetic)
export function BentoGrid({ children }: { children: React.ReactNode }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 p-4">
      {children}
    </div>
  );
}

// Glassmorphism Card (NO Lucide icons!)
export function GlassCard({
  title,
  children,
  icon: Icon  // AI-generated custom icon component
}: {
  title: string;
  children: React.ReactNode;
  icon?: React.ComponentType<{ className?: string }>;
}) {
  return (
    <div className="glass-card">
      <div className="flex items-center gap-3 mb-4">
        {Icon && <Icon className="w-6 h-6 text-primary-600" />}
        <h3 className="text-xl font-semibold">{title}</h3>
      </div>
      {children}
    </div>
  );
}
```

## Data Fetching

### Server-Side
```typescript
// In Server Components
async function getData() {
  const res = await fetch('https://api.example.com/data', {
    next: { revalidate: 3600 } // Revalidate every hour
  });

  if (!res.ok) {
    throw new Error('Failed to fetch data');
  }

  return res.json();
}

// Australian context in data fetching
async function getAustralianData() {
  const res = await fetch('https://api.example.com/data', {
    headers: {
      'Accept-Language': 'en-AU',
      'X-Timezone': 'Australia/Brisbane'
    },
    next: { revalidate: 3600 }
  });

  return res.json();
}
```

### Client-Side with SWR
```typescript
'use client';

import useSWR from 'swr';

const fetcher = (url: string) =>
  fetch(url, {
    headers: {
      'Accept-Language': 'en-AU'
    }
  }).then(res => res.json());

export function UserProfile({ userId }: { userId: string }) {
  const { data, error, isLoading } = useSWR(
    `/api/users/${userId}`,
    fetcher
  );

  if (isLoading) return <Skeleton />;
  if (error) return <ErrorCard message="Failed to load user" />;

  return <Profile user={data} />;
}
```

## Route Handlers (Australian Context)

```typescript
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const query = searchParams.get('query');

  // Get Australian users
  const users = await getUsers({
    query,
    locale: 'en-AU',
    timezone: 'Australia/Brisbane'
  });

  return NextResponse.json(users);
}

export async function POST(request: NextRequest) {
  const body = await request.json();

  // Validate Australian phone format
  if (body.phone && !isValidAustralianPhone(body.phone)) {
    return NextResponse.json(
      { error: 'Invalid Australian phone format. Use 04XX XXX XXX' },
      { status: 422 }
    );
  }

  // Validate postcode (4 digits)
  if (body.postcode && !/^\d{4}$/.test(body.postcode)) {
    return NextResponse.json(
      { error: 'Invalid postcode. Australian postcodes are 4 digits' },
      { status: 422 }
    );
  }

  const user = await createUser(body);
  return NextResponse.json(user, { status: 201 });
}

// Helper functions
function isValidAustralianPhone(phone: string): boolean {
  const cleaned = phone.replace(/\s/g, '');
  return /^04\d{8}$/.test(cleaned);  // Mobile format
}
```

## Middleware (Australian Context)

```typescript
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  // Set Australian locale headers
  const response = NextResponse.next();

  response.headers.set('X-Locale', 'en-AU');
  response.headers.set('X-Timezone', 'Australia/Brisbane');
  response.headers.set('X-Currency', 'AUD');

  // Check auth
  const token = request.cookies.get('token');

  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  return response;
}

export const config = {
  matcher: ['/dashboard/:path*', '/api/:path*'],
};
```

## Loading & Error States (2025-2026 Aesthetic)

```typescript
// app/dashboard/loading.tsx
export default function Loading() {
  return (
    <div className="bento-grid">
      {[1, 2, 3, 4, 5, 6].map(i => (
        <div key={i} className="glass-card animate-pulse">
          <div className="h-6 bg-gray-200 rounded-lg mb-4" />
          <div className="h-4 bg-gray-200 rounded-lg mb-2" />
          <div className="h-4 bg-gray-200 rounded-lg w-2/3" />
        </div>
      ))}
    </div>
  );
}

// app/dashboard/error.tsx
'use client';

export default function Error({
  error,
  reset,
}: {
  error: Error;
  reset: () => void;
}) {
  return (
    <div className="glass-card max-w-md mx-auto mt-8">
      <h2 className="text-2xl font-semibold mb-4">Something went wrong</h2>
      <p className="text-gray-600 mb-6">
        We're sorry, but something unexpected happened. Please try again.
      </p>
      <button
        onClick={reset}
        className="btn-primary"
      >
        Try again
      </button>
    </div>
  );
}
```

## Metadata (Australian SEO)

```typescript
// app/layout.tsx
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: {
    template: '%s | Unite Group',
    default: 'Unite Group - Australian Water Damage Restoration',
  },
  description: 'Professional water damage restoration services across Brisbane, Sydney, and Melbourne. Available 24/7.',
  keywords: ['water damage', 'restoration', 'Brisbane', 'Sydney', 'Melbourne', 'Australia'],
  authors: [{ name: 'Unite Group' }],
  openGraph: {
    type: 'website',
    locale: 'en_AU',
    url: 'https://unite-group.com.au',
    siteName: 'Unite Group',
  },
  twitter: {
    card: 'summary_large_image',
  },
};

// Dynamic metadata (Australian city pages)
export async function generateMetadata(
  { params }: { params: { city: string } }
): Promise<Metadata> {
  const city = params.city;

  return {
    title: `Water Damage Restoration in ${city}`,
    description: `24/7 emergency water damage restoration services in ${city}, Australia. Fast response, professional service.`,
    openGraph: {
      locale: 'en_AU',
    },
  };
}
```

## Australian Context Utilities

```typescript
// lib/australian-context.ts

// Format date in Australian DD/MM/YYYY
export function formatDateAU(date: Date): string {
  return date.toLocaleDateString('en-AU', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  });
}

// Format currency in AUD
export function formatCurrencyAUD(amount: number): string {
  return new Intl.NumberFormat('en-AU', {
    style: 'currency',
    currency: 'AUD'
  }).format(amount);
}

// Format phone number (Australian)
export function formatPhoneAU(phone: string): string {
  const cleaned = phone.replace(/\D/g, '');

  if (cleaned.startsWith('04') && cleaned.length === 10) {
    // Mobile: 0412 345 678
    return `${cleaned.slice(0, 4)} ${cleaned.slice(4, 7)} ${cleaned.slice(7)}`;
  }

  if (cleaned.length === 10) {
    // Landline: (02) 1234 5678
    return `(${cleaned.slice(0, 2)}) ${cleaned.slice(2, 6)} ${cleaned.slice(6)}`;
  }

  return phone;
}

// Get Australian state name
export function getStateName(code: string): string {
  const states: Record<string, string> = {
    QLD: 'Queensland',
    NSW: 'New South Wales',
    VIC: 'Victoria',
    SA: 'South Australia',
    WA: 'Western Australia',
    TAS: 'Tasmania',
    NT: 'Northern Territory',
    ACT: 'Australian Capital Territory'
  };

  return states[code] || code;
}

// Get Australian timezone
export function getAustralianTimezone(state: string): string {
  const timezones: Record<string, string> = {
    QLD: 'Australia/Brisbane',
    NSW: 'Australia/Sydney',
    VIC: 'Australia/Melbourne',
    SA: 'Australia/Adelaide',
    WA: 'Australia/Perth',
    TAS: 'Australia/Hobart',
    NT: 'Australia/Darwin',
    ACT: 'Australia/Sydney'
  };

  return timezones[state] || 'Australia/Brisbane';
}
```

## Design System Components (2025-2026 Aesthetic)

```typescript
// components/ui/bento-card.tsx
'use client';

import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';

export function BentoCard({
  children,
  className,
  size = 'default'
}: {
  children: React.ReactNode;
  className?: string;
  size?: 'small' | 'default' | 'large';
}) {
  const sizeClasses = {
    small: 'col-span-1',
    default: 'col-span-1 md:col-span-2',
    large: 'col-span-1 md:col-span-2 lg:col-span-3'
  };

  return (
    <motion.div
      className={cn(
        'glass-card',
        sizeClasses[size],
        className
      )}
      whileHover={{ scale: 1.02 }}
      transition={{ duration: 0.15 }}
    >
      {children}
    </motion.div>
  );
}

// NO Lucide icons - Use AI-generated custom icons only
// Example custom icon component:
export function WaterDropIcon({ className }: { className?: string }) {
  return (
    <svg
      className={className}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
    >
      {/* Custom SVG path generated by AI */}
      <path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z" />
    </svg>
  );
}
```

## Verification Checklist

- [ ] `pnpm build` passes without errors
- [ ] No hydration mismatches
- [ ] Correct use of 'use client' directive
- [ ] Data fetching works correctly
- [ ] Loading states implemented (Bento grid skeleton)
- [ ] Error boundaries in place (glassmorphism cards)
- [ ] Australian context applied (en-AU, DD/MM/YYYY, AUD)
- [ ] NO Lucide icons used (AI-generated custom only)
- [ ] Design tokens followed (`.claude/data/design-tokens.json`)
- [ ] 2025-2026 aesthetic (Bento grids, glassmorphism, micro-interactions)
- [ ] Soft colored shadows (NEVER pure black)
- [ ] WCAG 2.1 AA compliance

See: `apps/web/`, `design/design-system.skill.md`, `australian/australian-context.skill.md`
