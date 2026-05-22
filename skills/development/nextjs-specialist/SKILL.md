---
name: nextjs_specialist
router_kit: DevOpsKit
description: Next.js 15 App Router, Server Components, SSR/SSG optimizasyonu ve modern Next.js best practices.
metadata:
  skillport:
    category: development
    tags: [accessibility, api integration, backend, browser apis, client-side, components, css3, debugging, deployment, frameworks, frontend, fullstack, html5, javascript, libraries, nextjs specialist, node.js, npm, performance optimization, responsive design, seo, state management, testing, typescript, ui/ux, web development]      - app-router
---

# ⚛️ Next.js Specialist

> Next.js 15 App Router ve Server Components rehberi.

---

## 📋 İçindekiler

1. [App Router Temelleri](#1-app-router-temelleri)
2. [Server vs Client Components](#2-server-vs-client-components)
3. [Data Fetching](#3-data-fetching)
4. [Rendering Stratejileri](#4-rendering-stratejileri)
5. [Optimizasyon](#5-optimizasyon)

---

## 1. App Router Temelleri

### Dosya Yapısı
```
app/
├── layout.tsx          # Root layout
├── page.tsx            # Home page (/)
├── loading.tsx         # Loading UI
├── error.tsx           # Error boundary
├── not-found.tsx       # 404 page
├── globals.css
│
├── (marketing)/        # Route group (URL'de görünmez)
│   ├── about/
│   │   └── page.tsx    # /about
│   └── contact/
│       └── page.tsx    # /contact
│
├── dashboard/
│   ├── layout.tsx      # Nested layout
│   ├── page.tsx        # /dashboard
│   └── settings/
│       └── page.tsx    # /dashboard/settings
│
├── blog/
│   ├── page.tsx        # /blog
│   └── [slug]/
│       └── page.tsx    # /blog/:slug (dynamic)
│
└── api/
    └── users/
        └── route.ts    # API route
```

### Special Files
| Dosya | Amaç |
|-------|------|
| `layout.tsx` | Shared layout, state korunur |
| `page.tsx` | Unique route content |
| `loading.tsx` | Suspense fallback |
| `error.tsx` | Error boundary |
| `not-found.tsx` | 404 handler |
| `route.ts` | API endpoint |

---

## 2. Server vs Client Components

### Server Components (Default)
```tsx
// app/users/page.tsx
// ✅ Server Component - 'use client' yok

async function UsersPage() {
  const users = await db.users.findMany(); // Direkt DB erişimi
  
  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}

export default UsersPage;
```

### Client Components
```tsx
'use client'; // ⚠️ Dosyanın en üstünde

import { useState } from 'react';

export function Counter() {
  const [count, setCount] = useState(0);
  
  return (
    <button onClick={() => setCount(c => c + 1)}>
      Count: {count}
    </button>
  );
}
```

### Composition Pattern
```tsx
// Server Component
import { Counter } from './Counter'; // Client Component

async function Dashboard() {
  const data = await fetchData(); // Server'da çalışır
  
  return (
    <div>
      <h1>{data.title}</h1>
      <Counter /> {/* Client Component */}
    </div>
  );
}
```

### Ne Zaman Hangisi?
| Server Component | Client Component |
|------------------|------------------|
| Data fetching | Interactivity (onClick, onChange) |
| Backend erişimi | Browser API (localStorage) |
| Sensitive logic | Hooks (useState, useEffect) |
| Büyük dependencies | Event listeners |

---

## 3. Data Fetching

### Server Components
```tsx
// Otomatik cache
async function Page() {
  const res = await fetch('https://api.example.com/data');
  const data = await res.json();
  return <div>{data.title}</div>;
}

// Cache control
const res = await fetch(url, {
  cache: 'force-cache', // Default - cache
  // cache: 'no-store',  // Her request'te fresh
  // next: { revalidate: 60 }, // ISR - 60 saniye
});
```

### Server Actions
```tsx
// app/actions.ts
'use server';

export async function createUser(formData: FormData) {
  const name = formData.get('name');
  await db.users.create({ data: { name } });
  revalidatePath('/users');
}

// app/users/page.tsx
import { createUser } from './actions';

export default function Page() {
  return (
    <form action={createUser}>
      <input name="name" />
      <button type="submit">Create</button>
    </form>
  );
}
```

---

## 4. Rendering Stratejileri

### Static (SSG)
```tsx
// Default - build time'da generate
export default function Page() {
  return <h1>Static Page</h1>;
}

// Dynamic segments için
export async function generateStaticParams() {
  const posts = await getPosts();
  return posts.map(post => ({ slug: post.slug }));
}
```

### Dynamic (SSR)
```tsx
// Her request'te render
export const dynamic = 'force-dynamic';

export default async function Page() {
  const data = await fetchRealTimeData();
  return <div>{data.value}</div>;
}
```

### Incremental Static Regeneration (ISR)
```tsx
export const revalidate = 60; // 60 saniye

export default async function Page() {
  const data = await fetchData();
  return <div>{data.value}</div>;
}
```

---

## 5. Optimizasyon

### Image Optimization
```tsx
import Image from 'next/image';

<Image
  src="/hero.jpg"
  alt="Hero"
  width={1200}
  height={600}
  priority // LCP için
  placeholder="blur"
  blurDataURL="data:image/..."
/>
```

### Font Optimization
```tsx
// app/layout.tsx
import { Inter } from 'next/font/google';

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
});

export default function Layout({ children }) {
  return (
    <html className={inter.className}>
      <body>{children}</body>
    </html>
  );
}
```

### Metadata
```tsx
// Static
export const metadata = {
  title: 'My App',
  description: 'App description',
};

// Dynamic
export async function generateMetadata({ params }) {
  const post = await getPost(params.slug);
  return {
    title: post.title,
    openGraph: { images: [post.image] },
  };
}
```

### Parallel Routes
```
app/
├── @modal/
│   └── login/page.tsx
├── @sidebar/
│   └── page.tsx
└── layout.tsx
```

```tsx
// layout.tsx
export default function Layout({ children, modal, sidebar }) {
  return (
    <>
      {sidebar}
      {children}
      {modal}
    </>
  );
}
```

---

*Next.js Specialist v1.1 - Enhanced*

## 🔄 Workflow

> **Kaynak:** [Next.js App Router Documentation](https://nextjs.org/docs/app) & [Vercel Security Guide](https://vercel.com/guides/nextjs-security-checklist)

### Aşama 1: Rendering Strategy
- [ ] **Default to Server**: Her component'e varsayılan olarak Server Component muamelesi yap.
- [ ] **Isolate Client**: Sadece etkileşim (`useState`, `onClick`) gereken yaprak (leaf) nodları Client Component yap.
- [ ] **Streaming**: `Suspense` sınırlarını belirle ve `loading.tsx` dosyalarını oluştur.

### Aşama 2: Data & Actions
- [ ] **Fetch**: Veri çekme işlemlerini Server Component içinde yap (Waterfall'u önlemek için `Promise.all` kullan).
- [ ] **Actions**: Form işlemleri için Server Actions kullan ve Zod ile input validasyonu yap.
- [ ] **Security**: Server Action'larda authentication ve authorization kontrolünü manuel yap (`auth()` çağır).

### Aşama 3: Performance (Core Web Vitals)
- [ ] **Images**: `next/image` kullan ve `sizes` prop'unu doğru ayarla.
- [ ] **Fonts**: `next/font` ile fontları optimize et (Layout shift'i önler).
- [ ] **Scripts**: 3. parti scriptleri `next/script` ve `strategy="lazyOnload"` ile yükle.

### Kontrol Noktaları
| Aşama | Doğrulama |
|-------|-----------|
| 1 | "Hydration Error" alıyor musun? (Server/Client HTML uyuşmazlığı) |
| 2 | LCP (Largest Contentful Paint) < 2.5s mi? |
| 3 | Hassas veriler (API Key) Client bundle'a sızıyor mu? |
