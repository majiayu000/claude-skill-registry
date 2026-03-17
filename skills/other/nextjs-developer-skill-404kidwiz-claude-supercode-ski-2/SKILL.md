---
name: nextjs-developer
description: Expert Next.js developer specializing in Next.js 14+, App Router, Server Components, and modern React patterns. This agent excels at building high-performance, SEO-optimized web applications with full-stack capabilities, server actions, and cutting-edge Next.js features.
---

# Next.js Developer Specialist

## Purpose

Provides expert Next.js development expertise specializing in Next.js 14+, App Router, Server Components, and modern React patterns. Builds high-performance, SEO-optimized web applications with full-stack capabilities, server actions, and cutting-edge Next.js features.

## When to Use

- Building Next.js applications with App Router and Server Components
- Implementing Server Actions for data mutation
- Optimizing performance (Core Web Vitals, caching strategies)
- Setting up authentication and database integration
- Creating SEO-optimized static and dynamic pages
- Developing full-stack React applications

## Quick Start

**Invoke this skill when:**
- Building Next.js 14+ applications with App Router
- Implementing Server Components, Server Actions, or streaming rendering
- Setting up SEO-optimized, high-performance web applications
- Creating full-stack React applications with server-side rendering
- Implementing authentication, data fetching, or complex routing patterns
- Optimizing Core Web Vitals (LCP, FID, CLS) for Next.js apps
- Migrating from Pages Router to App Router architecture

**Do NOT invoke when:**
- Working with legacy Next.js (Pages Router only) → Use react-specialist instead
- Building purely client-side React apps → Use react-specialist
- Working on non-Next.js React frameworks (Remix, Gatsby) → Use appropriate specialist
- Handling only UI/UX styling without Next.js-specific features → Use frontend-ui-ux-engineer
- Simple static sites without server-side requirements → Consider simpler alternatives

## Core Capabilities

### Next.js 14+ Advanced Features
- **App Router**: Mastery of Next.js 13+ App Router with nested layouts and route groups
- **Server Components**: Strategic use of React Server Components vs Client Components
- **Server Actions**: Modern data mutation patterns with server actions and progressive enhancement
- **Streaming Rendering**: Implementing progressive UI loading with Suspense boundaries
- **Parallel Routes**: Complex layouts with multiple content slots
- **Intercepting Routes**: Modal dialogs and route overlays without navigation
- **Partial Prerendering**: Hybrid rendering with static and dynamic content

### Performance Optimization
- **Image Optimization**: Next.js Image component with automatic optimization
- **Font Optimization**: Next.js Font with layout shift prevention
- **Route Handlers**: API routes for server-side data fetching
- **Middleware**: Request/response interception and transformation
- **Static Generation**: ISR (Incremental Static Regeneration) strategies
- **Bundle Analysis**: Webpack Bundle Analyzer integration and optimization

### Full-Stack Development
- **Data Fetching**: Advanced caching patterns with fetch() and React's cache extension
- **Authentication**: NextAuth.js, Clerk, or custom auth implementations
- **Database Integration**: Prisma, Drizzle ORM with type-safe database access
- **State Management**: Server components with client state synchronization
- **API Integration**: REST and GraphQL clients with proper error handling
- **Type Safety**: End-to-end TypeScript with API route type definitions

## Decision Framework

### Server Components vs Client Components Decision Matrix

| Scenario | Component Type | Reasoning | Example |
|----------|---------------|-----------|---------|
| **Data fetching from database/API** | Server Component | No client JS bundle, direct server access | Product listing page |
| **Interactive forms with state** | Client Component | Needs useState, event handlers | Search filters, form inputs |
| **Static content with no interactivity** | Server Component | Zero JS to client, faster load | Blog post content, docs |
| **Third-party libraries using hooks** | Client Component | React hooks only work client-side | Chart libraries, animations |
| **Authentication-protected content** | Server Component | Secure token handling server-side | User dashboard data fetch |
| **Real-time updates (WebSocket)** | Client Component | Browser APIs required | Live chat, notifications |
| **Layout wrappers, navigation** | Server Component (default) | Reduce client bundle size | Header, footer, sidebar |
| **Modal dialogs, tooltips** | Client Component | Needs browser event handling | Confirmation dialogs, dropdowns |
| **SEO-critical content** | Server Component | Server-rendered HTML for crawlers | Product descriptions, landing pages |
| **User interactions (clicks, hover)** | Client Component | Event listeners required | Buttons, tabs, accordions |

**Red Flags → Escalate to oracle:**
- Deeply nested Client/Server component boundaries causing prop drilling
- Performance issues with large client bundles (>500KB)
- Confusion about when to use `'use client'` directive
- Waterfall requests due to improper data fetching patterns
- Authentication state synchronization issues across components

### App Router vs Pages Router Decision Tree

```
Next.js Project Architecture
├─ New Project (greenfield)
│   └─ ✅ ALWAYS use App Router (Next.js 13+)
│       • Modern React Server Components
│       • Built-in layouts and nested routing
│       • Streaming and Suspense support
│       • Better performance and DX
│
├─ Existing Pages Router Project
│   ├─ Small project (<10 routes)
│   │   └─ Consider migrating to App Router
│   │       • Migration effort: 1-3 days
│   │       • Benefits: Future-proof, better performance
│   │
│   ├─ Large project (10+ routes, complex)
│   │   ├─ Active development with new features
│   │   │   └─ ✅ Incremental migration (recommended)
│   │   │       • New routes → App Router
│   │   │       • Legacy routes → Keep Pages Router
│   │   │       • Gradual migration over sprints
│   │   │
│   │   └─ Maintenance mode (minimal changes)
│   │       └─ ⚠️ Keep Pages Router
│   │           • Migration ROI too low
│   │           • No breaking changes needed
│   │
│   └─ Heavy use of getServerSideProps/getStaticProps patterns
│       └─ ✅ Plan migration but test thoroughly
│           • Server Components replace getServerSideProps
│           • generateStaticParams replaces getStaticPaths
│           • Refactor data fetching patterns
│
└─ Team Experience
    ├─ Team unfamiliar with Server Components
    │   └─ ⚠️ Training required before migration
    │       • Budget 1-2 weeks for learning curve
    │       • Start with small App Router features
    │
    └─ Team experienced with modern React
        └─ ✅ Proceed with App Router confidently
```

## Best Practices Summary

### Performance Optimization
- Always use Next.js Image component for images
- Use next/font for layout shift prevention
- Implement dynamic imports for large components
- Leverage Next.js caching and CDN optimization
- Regularly analyze and optimize bundle size

### SEO Best Practices
- Implement comprehensive meta tags and Open Graph
- Add JSON-LD for rich snippets
- Use proper heading hierarchy and semantic elements
- Create clean, descriptive URLs
- Generate and submit XML sitemaps

### Security Practices
- Use secure authentication methods
- Validate all inputs with Zod schemas
- Implement CSRF tokens for forms
- Add comprehensive security headers
- Securely manage environment variables

## Additional Resources

- **Detailed Technical Reference**: See [REFERENCE.md](REFERENCE.md)
- **Code Examples & Patterns**: See [EXAMPLES.md](EXAMPLES.md)
