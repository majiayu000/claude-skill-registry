---
name: frontend-react
description: Professional React development skill covering Next.js, React Server Components, Tailwind CSS, and the React ecosystem. Use this skill when building modern React applications, implementing Next.js features, creating UI components with shadcn/ui, or working with complex state management.
---

# React Development Skill

Comprehensive skill for modern React development, focusing on Next.js, TypeScript, Tailwind CSS, and the wider React ecosystem.

## Technology Stack

### Core Framework: React + Next.js

#### React Fundamentals
- **Component-Based**: Declarative UI building blocks
- **Hooks**: Functional state and side-effect management (`useState`, `useEffect`, `useContext`)
- **Virtual DOM**: Efficient reconciliation and rendering
- **React Server Components (RSC)**: Server-side rendering with zero client-side bundle size for static content

#### Next.js Features (App Router)
- **App Router**: File-system based routing in `app/` directory
- **Server Actions**: Direct server-side mutations from client components
- **Streaming SSR**: Progressive rendering with Suspense
- **Metadata API**: SEO and social share optimization
- **Route Handlers**: API endpoints (GET, POST, etc.) in `route.ts` files
- **Middleware**: Request interception and processing

### UI Framework: Tailwind CSS + shadcn/ui

#### Tailwind CSS
- Utility-first CSS framework
- Responsive design with prefixes (`md:`, `lg:`)
- Custom configuration via `tailwind.config.ts`
- Dark mode support

#### shadcn/ui
- Reusable components built with Radix UI and Tailwind CSS
- Accessible and customizable
- "Own your code" philosophy (components copied to your project)
- **Key Components**: Button, Dialog, Form, Dropdown, Card, Sheet

### State Management
- **Local State**: `useState`, `useReducer`
- **Global State**: React Context, Zustand (for lightweight global state)
- **Server State**: TanStack Query (React Query) for async data fetching and caching

## Project Architecture

### Recommended Directory Structure (Next.js App Router)
```
src/
├── app/
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Home page
│   ├── globals.css        # Global styles
│   ├── (auth)/            # Route group (doesn't affect URL path)
│   │   ├── login/
│   │   │   └── page.tsx
│   │   └── register/
│   │       └── page.tsx
│   └── api/               # API routes
├── components/
│   ├── ui/                # shadcn/ui components
│   │   ├── button.tsx
│   │   └── ...
│   ├── Navbar.tsx
│   └── Footer.tsx
├── lib/
│   ├── utils.ts           # Utility functions (cn, etc.)
│   └── db.ts              # Database connection
└── hooks/                 # Custom React hooks
    └── use-toast.ts
```

## Best Practices

### Component Design
- **Server by Default**: Use Server Components for everything that doesn't need interactivity.
- **Client Boundary**: Add `'use client'` directive only when using hooks or event listeners.
- **Composition**: Use `children` prop to avoid prop drilling.
- **Micro-Components**: Break down complex UIs into smaller, single-responsibility components.

### Performance
- **Image Optimization**: Use `next/image` for automatic optimization.
- **Font Optimization**: Use `next/font` to prevent layout shift.
- **Lazy Loading**: Use `next/dynamic` or `React.lazy` for heavy components.
- **Code Splitting**: Automatic in Next.js, but be mindful of large dependencies.

### Accessibility (a11y)
- Use semantic HTML tags (`<main>`, `<article>`, `<nav>`).
- Ensure all interactive elements have keyboard support.
- Use valid ARIA attributes when semantic HTML isn't enough.
- Radix UI primitives (used in shadcn/ui) handle many a11y concerns automatically.

## Common Code Patterns

### Next.js Page (Server Component)
```tsx
import { db } from "@/lib/db"

export default async function DashboardPage() {
  const data = await db.user.findMany()

  return (
    <main className="p-6">
      <h1 className="text-2xl font-bold">Dashboard</h1>
      <ul>
        {data.map(user => (
          <li key={user.id}>{user.name}</li>
        ))}
      </ul>
    </main>
  )
}
```

### Client Component with State
```tsx
"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"

export function Counter() {
  const [count, setCount] = useState(0)

  return (
    <div className="flex gap-4 items-center">
      <span>Count: {count}</span>
      <Button onClick={() => setCount(c => c + 1)}>Increment</Button>
    </div>
  )
}
```
