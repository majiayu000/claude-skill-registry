---
name: Suspense & Streaming Generator
description: Implémente Suspense et Streaming pour progressive rendering. MANDATORY pour async Server Components. À utiliser lors de async data, loading states, ou quand l'utilisateur mentionne "suspense", "streaming", "loading", "skeleton".
allowed-tools: [Read, Write, Edit]
---

# Suspense & Streaming Generator

## 🎯 Mission

Implémenter **Suspense** et **Streaming** pour un **progressive rendering** et une meilleure perceived performance.

## 🌊 Concept

**Suspense** permet de :
- ✅ Afficher un fallback pendant le chargement
- ✅ Streamer le contenu progressivement
- ✅ Ne pas bloquer toute la page
- ✅ Améliorer la perceived performance

## 📝 Template Server Component

```typescript
// app/(dashboard)/coach/page.tsx

import { Suspense } from 'react';
import { ClubStats } from '@/features/club-management/components/ClubStats';
import { MembersList } from '@/features/club-management/components/MembersList';
import { ClubStatsSkeleton } from '@/features/club-management/components/ClubStatsSkeleton';
import { MembersListSkeleton } from '@/features/club-management/components/MembersListSkeleton';

export default function CoachDashboard() {
  return (
    <div className="space-y-8">
      <h1>Dashboard Coach</h1>

      {/* Section 1 - Streams independently */}
      <Suspense fallback={<ClubStatsSkeleton />}>
        <ClubStats />
      </Suspense>

      {/* Section 2 - Streams independently */}
      <Suspense fallback={<MembersListSkeleton />}>
        <MembersList />
      </Suspense>
    </div>
  );
}
```

### Async Server Component

```typescript
// features/club-management/components/ClubStats.tsx
// (Server Component - NO 'use client')

import { clubsApi } from '../api/clubs.api';

export async function ClubStats() {
  // Async data fetching
  const stats = await clubsApi.getStats();

  return (
    <div className="grid grid-cols-3 gap-4">
      <StatCard title="Membres" value={stats.membersCount} />
      <StatCard title="Équipes" value={stats.teamsCount} />
      <StatCard title="Matchs" value={stats.matchesCount} />
    </div>
  );
}
```

### Skeleton Component

```typescript
// features/club-management/components/ClubStatsSkeleton.tsx

export function ClubStatsSkeleton() {
  return (
    <div className="grid grid-cols-3 gap-4">
      {[...Array(3)].map((_, i) => (
        <div key={i} className="h-24 bg-muted animate-pulse rounded-lg" />
      ))}
    </div>
  );
}
```

## 🎨 Patterns

### Nested Suspense

```typescript
<Suspense fallback={<PageSkeleton />}>
  <Header />

  <Suspense fallback={<ContentSkeleton />}>
    <Content />

    <Suspense fallback={<CommentsSkeleton />}>
      <Comments />
    </Suspense>
  </Suspense>
</Suspense>
```

### Parallel Loading

```typescript
export default function Page() {
  return (
    <>
      {/* Both load in parallel */}
      <Suspense fallback={<Skeleton1 />}>
        <SlowComponent1 />
      </Suspense>

      <Suspense fallback={<Skeleton2 />}>
        <SlowComponent2 />
      </Suspense>
    </>
  );
}
```

### Loading avec Streaming

```typescript
// app/(dashboard)/loading.tsx (route-level loading)

export default function Loading() {
  return <DashboardSkeleton />;
}

// Ou Suspense granulaire (preferred)
<Suspense fallback={<Skeleton />}>
  <AsyncComponent />
</Suspense>
```

## ✅ Checklist

- [ ] Tous async Server Components wrappés dans `<Suspense>`
- [ ] Skeleton component pour chaque section
- [ ] Skeleton correspond visuellement au contenu
- [ ] Pas de `loading.tsx` global (préférer Suspense granulaire)
- [ ] Parallel loading pour sections indépendantes

---

**Rappel**: MANDATORY pour async Server Components = Progressive rendering optimal.
