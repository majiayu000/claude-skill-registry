---
name: discover-frontend
description: Automatically discover frontend development skills when working with React, Next.js, UI components, state management, data fetching, forms, accessibility, performance optimization, or SEO. Activates for frontend web development tasks.
---

# Frontend Skills Discovery

Provides automatic access to comprehensive frontend development skills.

## When This Skill Activates

This skill auto-activates when you're working with:
- React component development
- Next.js applications and App Router
- State management (Context, Zustand, Redux)
- Data fetching (SWR, React Query, Server Actions)
- Form handling and validation
- Web accessibility (WCAG, ARIA)
- Frontend performance optimization
- SEO and metadata
- UI/UX design implementation

## Available Skills

### Quick Reference

The Frontend category contains 10 core skills (+ elegant-design):

1. **react-component-patterns** - Component design, composition, hooks, performance
2. **nextjs-app-router** - Next.js 14+ App Router, Server Components, routing
3. **react-state-management** - Context, Zustand, Redux Toolkit patterns
4. **react-data-fetching** - SWR, React Query, Server Actions, data patterns
5. **react-form-handling** - React Hook Form, Zod validation, form patterns
6. **web-accessibility** - WCAG 2.1 AA compliance, ARIA, keyboard navigation
7. **frontend-performance** - Bundle optimization, Core Web Vitals, code splitting
8. **nextjs-seo** - SEO with Next.js, metadata API, structured data
9. **web-workers** - Web Workers API, message passing, offloading computation
10. **browser-concurrency** - Service Workers, SharedWorkers, Worklets, PWAs
11. **elegant-design/SKILL.md** - World-class accessible interfaces (separate Agent Skill)

### Load Full Category Details

For complete descriptions and workflows:

```bash
cat ~/.claude/skills/frontend/INDEX.md
```

This loads the full Frontend category index with:
- Detailed skill descriptions
- Usage triggers for each skill
- Common workflow combinations
- Cross-references to related skills

### Load Specific Skills

Load individual skills as needed:

```bash
# Core React patterns
cat ~/.claude/skills/frontend/react-component-patterns.md
cat ~/.claude/skills/frontend/react-state-management.md
cat ~/.claude/skills/frontend/react-data-fetching.md

# Next.js specific
cat ~/.claude/skills/frontend/nextjs-app-router.md
cat ~/.claude/skills/frontend/nextjs-seo.md

# Forms and validation
cat ~/.claude/skills/frontend/react-form-handling.md

# Quality and performance
cat ~/.claude/skills/frontend/web-accessibility.md
cat ~/.claude/skills/frontend/frontend-performance.md

# Concurrency and workers
cat ~/.claude/skills/frontend/web-workers.md
cat ~/.claude/skills/frontend/browser-concurrency.md

# Design system and UI (Agent Skill - auto-discovered separately)
# elegant-design/SKILL.md activates independently for UI design work
```

## Common Workflows

### New Next.js Application
**Sequence**: App Router → Components → Data Fetching

```bash
cat ~/.claude/skills/frontend/nextjs-app-router.md          # Setup routing, layouts
cat ~/.claude/skills/frontend/react-component-patterns.md   # Build components
cat ~/.claude/skills/frontend/react-data-fetching.md        # Fetch data
```

### Elegant UI Design
**Sequence**: Design System → Components → Accessibility

```bash
# Note: elegant-design auto-activates as separate Agent Skill
# for design-focused work (shadcn/ui, accessible interfaces, etc.)
cat ~/.claude/skills/frontend/react-component-patterns.md
cat ~/.claude/skills/frontend/web-accessibility.md
```

### Form Implementation
**Sequence**: Form Handling → State Management

```bash
cat ~/.claude/skills/frontend/react-form-handling.md     # Build forms
cat ~/.claude/skills/frontend/react-state-management.md  # Manage form state
```

### Production Optimization
**Sequence**: Performance → Accessibility → SEO

```bash
cat ~/.claude/skills/frontend/frontend-performance.md    # Optimize bundle
cat ~/.claude/skills/frontend/web-accessibility.md       # Ensure accessibility
cat ~/.claude/skills/frontend/nextjs-seo.md              # Optimize SEO
```

### CPU-Intensive Features & PWAs
**Sequence**: Workers → Concurrency → Performance

```bash
cat ~/.claude/skills/frontend/web-workers.md             # Offload heavy computation
cat ~/.claude/skills/frontend/browser-concurrency.md     # Service Workers, offline support
cat ~/.claude/skills/frontend/frontend-performance.md    # Optimize overall performance
```

## Skill Selection Guide

**React Component Patterns** → `react-component-patterns.md`:
- Component architecture and composition
- Custom hooks
- Performance optimization (memo, useMemo, useCallback)
- Design patterns (compound components, render props, HOCs)

**Next.js App Router** → `nextjs-app-router.md`:
- Server Components vs Client Components
- Routing and layouts
- Data fetching patterns
- Streaming and Suspense
- Route handlers and API routes

**State Management** → `react-state-management.md`:
- When to use Context vs external state libraries
- Zustand for simple global state
- Redux Toolkit for complex state
- Server state vs client state

**Data Fetching** → `react-data-fetching.md`:
- SWR for client-side fetching
- React Query (TanStack Query) for advanced patterns
- Next.js Server Actions
- Data mutation patterns
- Caching strategies

**Forms** → `react-form-handling.md`:
- React Hook Form for performance
- Zod for validation
- Form state management
- Error handling
- File uploads

**Accessibility** → `web-accessibility.md`:
- WCAG 2.1 AA compliance
- ARIA attributes
- Keyboard navigation
- Screen reader support
- Color contrast and focus management

**Performance** → `frontend-performance.md`:
- Bundle size optimization
- Code splitting and lazy loading
- Core Web Vitals
- Image optimization
- Font optimization
- Runtime performance

**SEO** → `nextjs-seo.md`:
- Next.js Metadata API
- Open Graph and Twitter cards
- Structured data (JSON-LD)
- Sitemap and robots.txt
- Dynamic metadata

**Web Workers** → `web-workers.md`:
- Offloading heavy computation
- Web Workers API and message passing
- Transferable objects for zero-copy
- React integration with custom hooks
- Worker pools for parallel processing
- TypeScript type safety

**Browser Concurrency** → `browser-concurrency.md`:
- Service Workers for offline support and PWAs
- SharedWorkers for cross-tab state
- Audio/Paint/Animation Worklets
- Background sync and push notifications
- Caching strategies
- BroadcastChannel for cross-tab messaging

## Integration with Other Skills

Frontend skills commonly combine with:

**API skills** (`discover-api`):
- Consuming REST APIs
- GraphQL client integration
- API error handling in UI
- Authentication flows

**Testing skills** (`discover-testing`):
- Component testing
- E2E testing with Playwright
- Visual regression testing
- Accessibility testing

**Design** (`elegant-design` Agent Skill):
- shadcn/ui components
- Accessible design patterns
- Chat/terminal/code UIs
- Streaming interfaces
- Design systems

**Database skills** (`discover-database`):
- Server Actions with database queries
- ORM integration in Server Components
- Real-time data updates

**Deployment skills** (`discover-deployment`):
- Vercel deployment
- Netlify deployment
- Performance monitoring
- CDN configuration

## Progressive Loading

This gateway skill enables progressive loading:
- **Level 1**: Gateway loads automatically (you're here now)
- **Level 2**: Load category INDEX.md (~4K tokens) for full overview
- **Level 3**: Load specific skills (~3-4K tokens each) as needed

Total context: 2K + 4K + skill(s) = 6-12K tokens vs 25K+ for entire index.

## Quick Start Examples

**"Build a Next.js app with App Router"**:
```bash
cat ~/.claude/skills/frontend/nextjs-app-router.md
```

**"Create reusable React components"**:
```bash
cat ~/.claude/skills/frontend/react-component-patterns.md
```

**"Implement global state management"**:
```bash
cat ~/.claude/skills/frontend/react-state-management.md
```

**"Build a form with validation"**:
```bash
cat ~/.claude/skills/frontend/react-form-handling.md
```

**"Optimize my app performance"**:
```bash
cat ~/.claude/skills/frontend/frontend-performance.md
```

**"Make my app accessible"**:
```bash
cat ~/.claude/skills/frontend/web-accessibility.md
```

**"Improve SEO"**:
```bash
cat ~/.claude/skills/frontend/nextjs-seo.md
```

**"Offload heavy computation"**:
```bash
cat ~/.claude/skills/frontend/web-workers.md
```

**"Build a PWA with offline support"**:
```bash
cat ~/.claude/skills/frontend/browser-concurrency.md
```

## React vs Next.js Decision

**Use React (Vite)** when:
- Building SPAs or client-heavy apps
- Don't need SSR or SSG
- Want full control over routing
- Building component libraries

**Use Next.js** when:
- Need SEO (Server-Side Rendering)
- Want file-based routing
- Need API routes
- Building full-stack apps
- Want optimal performance out of the box

## State Management Decision

**Use Component State (useState)** when:
- State is local to a component
- Simple state that doesn't need sharing

**Use Context** when:
- Sharing state across a few components
- Theme, auth, or user preferences
- Not frequently updated

**Use Zustand** when:
- Need global state
- Want simple API
- State updates are moderate

**Use Redux Toolkit** when:
- Complex state logic
- Need middleware (sagas, thunks)
- Large team with established patterns
- Time-travel debugging needed

For detailed guidance:
```bash
cat ~/.claude/skills/frontend/react-state-management.md
```

## Data Fetching Decision

**Server Components** (Next.js App Router):
- Default choice for Next.js 14+
- Fetch on server, zero client JS
- Direct database access

**Server Actions** (Next.js):
- For mutations and form handling
- Progressive enhancement
- Type-safe with TypeScript

**SWR**:
- Client-side data fetching
- Built-in caching
- Optimistic updates
- Focus on user experience

**React Query**:
- Advanced caching strategies
- Complex data dependencies
- Offline support
- DevTools for debugging

For detailed patterns:
```bash
cat ~/.claude/skills/frontend/react-data-fetching.md
```

## Usage Instructions

1. **Auto-activation**: This skill loads automatically when Claude Code detects frontend work
2. **Browse skills**: Run `cat ~/.claude/skills/frontend/INDEX.md` for full category overview
3. **Load specific skills**: Use bash commands above to load individual skills
4. **Follow workflows**: Use recommended sequences for common patterns
5. **elegant-design**: Note that elegant-design is a separate Agent Skill that auto-activates for UI design work

---

**Next Steps**: Run `cat ~/.claude/skills/frontend/INDEX.md` to see full category details, or load specific skills using the bash commands above.
