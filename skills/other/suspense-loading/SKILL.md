---
name: suspense-loading
description: |
  Suspense and loading state patterns for this Next.js application.
  Covers loading.tsx files, skeleton components, INP optimization, and streaming SSR.
  Use this skill when implementing loading states or optimizing perceived performance.
allowed-tools: Read, Glob, Grep
version: 1.0.0
---

# Suspense & Loading States Skill

Patterns for implementing loading states and Suspense boundaries in this Next.js 15 application.

## Architecture Overview

```
LOADING STATE ARCHITECTURE:

Route-Level Loading (loading.tsx):
├── app/dashboard/(main)/loading.tsx     # Dashboard home skeleton
├── app/dashboard/settings/loading.tsx   # Settings overview skeleton
├── app/dashboard/settings/*/loading.tsx # Setting-specific skeletons
├── app/dashboard/features/loading.tsx   # Features placeholder skeleton
└── app/dashboard/(main)/[entity]/       # Entity list skeleton (existing)

Skeleton Components (core/components/ui/):
├── skeleton.tsx           # Base Skeleton + SkeletonContainer + SkeletonText
├── skeleton-dashboard.tsx # SkeletonDashboardHome, SkeletonStatsGrid, etc.
├── skeleton-settings.tsx  # SkeletonSettingsOverview, SkeletonProfileForm, etc.
├── skeleton-features.tsx  # SkeletonFeaturePlaceholder, SkeletonAnalyticsPage
├── skeleton-list.tsx      # SkeletonEntityList, SkeletonTable
├── skeleton-form.tsx      # SkeletonEntityForm, SkeletonFormCard
└── skeleton-detail.tsx    # SkeletonEntityDetail, SkeletonDetailCard
```

## INP Optimizations

The skeleton system includes optimizations for Interaction to Next Paint (INP):

### 1. CSS Containment

```css
/* Isolates layout/paint calculations */
.skeleton-contained {
  contain: content;
}

/* Container-level containment */
.skeleton-container {
  contain: layout style;
}
```

### 2. Content Visibility

```css
/* Skips rendering of off-screen skeleton items */
.skeleton-container > * {
  content-visibility: auto;
  contain-intrinsic-size: auto 100px;
}
```

### 3. GPU-Accelerated Animations

```css
@keyframes skeleton-pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.animate-skeleton-pulse {
  animation: skeleton-pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
  will-change: opacity;
}
```

### 4. Reduced Motion Support

```css
@media (prefers-reduced-motion: reduce) {
  .animate-skeleton-pulse {
    animation: none;
  }
}
```

## Component Patterns

### Base Skeleton

```typescript
import { Skeleton, SkeletonContainer, SkeletonText } from '@nextsparkjs/core/components/ui/skeleton'

// Simple skeleton
<Skeleton className="h-4 w-32" />

// Text skeleton with multiple lines
<SkeletonText lines={3} />

// Container for multiple skeletons (enables content-visibility)
<SkeletonContainer className="space-y-4">
  <Skeleton className="h-10 w-full" />
  <Skeleton className="h-10 w-full" />
  <Skeleton className="h-10 w-full" />
</SkeletonContainer>
```

### Loading.tsx Pattern

```typescript
// app/dashboard/settings/profile/loading.tsx
import { SkeletonProfileForm } from '@nextsparkjs/core/components/ui/skeleton-settings'

export default function ProfileLoading() {
  return <SkeletonProfileForm />
}
```

### Suspense Boundary in Component

```typescript
import { Suspense } from 'react'
import { SkeletonStatsGrid } from '@nextsparkjs/core/components/ui/skeleton-dashboard'

export default function DashboardPage() {
  return (
    <div>
      {/* Header (instant) */}
      <h1>Dashboard</h1>

      {/* Stats with Suspense boundary (streamed) */}
      <Suspense fallback={<SkeletonStatsGrid />}>
        <DashboardStats />
      </Suspense>

      {/* Activity with Suspense boundary (streamed) */}
      <Suspense fallback={<SkeletonActivity />}>
        <RecentActivity />
      </Suspense>
    </div>
  )
}
```

## Available Skeleton Components

### Dashboard

| Component | Description |
|-----------|-------------|
| `SkeletonDashboardHome` | Complete dashboard home page skeleton |
| `SkeletonStatsGrid` | 4-card stats grid |
| `SkeletonStatCard` | Single stat card |
| `SkeletonQuickActions` | Quick actions section |
| `SkeletonActivity` | Activity feed |

### Settings

| Component | Description |
|-----------|-------------|
| `SkeletonSettingsOverview` | Settings navigation cards |
| `SkeletonProfileForm` | Profile edit form |
| `SkeletonBillingPage` | Billing/plans page |
| `SkeletonPasswordPage` | Password change form |
| `SkeletonSecurityPage` | Sessions list |
| `SkeletonApiKeysPage` | API keys list |
| `SkeletonNotificationsPage` | Notification settings |
| `SkeletonTeamsPage` | Teams list |
| `SkeletonInvoicesPage` | Invoices table |
| `SkeletonPlansPage` | Plans grid |

### Features

| Component | Description |
|-----------|-------------|
| `SkeletonFeaturePlaceholder` | Feature gate placeholder |
| `SkeletonAnalyticsPage` | Analytics dashboard |
| `SkeletonWebhooksPage` | Webhooks configuration |
| `SkeletonAutomationPage` | Automation list |

### Entity Pages

| Component | Description |
|-----------|-------------|
| `SkeletonEntityList` | Complete entity list page |
| `SkeletonEntityForm` | Entity create/edit form |
| `SkeletonEntityDetail` | Entity detail view |

## Best Practices

### 1. Match Skeleton to Content

Skeletons should closely match the final content layout:

```typescript
// Good - matches actual content structure
<div className="max-w-4xl space-y-6">
  <header>
    <Skeleton className="h-8 w-32 mb-2" />
    <Skeleton className="h-5 w-64" />
  </header>
  {/* ... */}
</div>

// Bad - generic box that doesn't match
<Skeleton className="h-[500px] w-full" />
```

### 2. Use Route-Level Loading

Prefer `loading.tsx` files over component-level loading states:

```
app/dashboard/settings/profile/
├── page.tsx       # Actual content
└── loading.tsx    # Skeleton shown during load
```

### 3. Wrap Multiple Skeletons

Use `SkeletonContainer` for lists to enable content-visibility:

```typescript
// Good - enables off-screen optimization
<SkeletonContainer className="divide-y">
  {Array.from({ length: 10 }).map((_, i) => (
    <SkeletonListItem key={i} />
  ))}
</SkeletonContainer>

// Less optimal - no content-visibility
<div className="divide-y">
  {Array.from({ length: 10 }).map((_, i) => (
    <SkeletonListItem key={i} />
  ))}
</div>
```

### 4. Consider Inheritance

Next.js inherits `loading.tsx` from parent routes. You only need specific loading files for pages with different layouts:

```
app/dashboard/settings/
├── loading.tsx           # Covers /settings and simple subroutes
├── profile/
│   └── loading.tsx       # Different layout, needs own skeleton
├── billing/
│   └── loading.tsx       # Different layout, needs own skeleton
├── password/             # Uses parent loading.tsx
├── security/             # Uses parent loading.tsx
└── notifications/        # Uses parent loading.tsx
```

## Testing Loading States

```typescript
// Cypress test for loading states
it('should show skeleton while content loads', () => {
  // Simulate slow network
  cy.intercept('GET', '/api/**', (req) => {
    req.on('response', (res) => res.setDelay(500))
  })

  cy.visit('/dashboard/settings/profile')

  // Skeleton should appear briefly
  // Content should replace skeleton
  cy.get('[data-cy="settings-profile-container"]', { timeout: 10000 })
    .should('be.visible')
})
```

## Related Skills

- `react-patterns` - Server/Client components, Suspense basics
- `shadcn-components` - UI component library
- `tanstack-query` - Data fetching with loading states
