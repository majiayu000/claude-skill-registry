---
name: bellog-structure
description: Provides file organization and naming conventions for the Bellog project. Triggers when creating new files or reorganizing code.
---

# Bellog File Organization

This skill defines the file structure, naming conventions, and organization patterns for the Bellog blog project.

## Project Structure

```
/Users/castle_bell/Projects/bellog/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── layout.tsx          # Root layout with fonts & metadata
│   │   ├── page.tsx            # Home page
│   │   ├── template.tsx        # Page transition wrapper
│   │   ├── providers.tsx       # Client-side providers
│   │   ├── posts/
│   │   │   ├── page.tsx        # All posts page
│   │   │   └── [slug]/
│   │   │       └── page.tsx    # Individual post
│   │   ├── api/
│   │   │   └── revalidate/
│   │   │       └── route.ts    # Cache revalidation endpoint
│   │   ├── robots.ts           # SEO robots.txt
│   │   └── sitemap.ts          # Dynamic sitemap
│   │
│   ├── components/
│   │   ├── common/             # App-wide shared components
│   │   │   ├── Navbar.tsx
│   │   │   ├── Footer.tsx
│   │   │   ├── Intro.tsx
│   │   │   ├── Header.tsx
│   │   │   └── ...
│   │   ├── posts/              # Post-specific components
│   │   │   ├── PostCard.tsx
│   │   │   ├── PostList.tsx
│   │   │   ├── PostRenderer.tsx
│   │   │   ├── NotionToc.tsx
│   │   │   └── ...
│   │   └── ui/                 # Low-level UI primitives
│   │       ├── Tag.tsx
│   │       ├── ThemeToggle.tsx
│   │       ├── switch.tsx
│   │       └── ...
│   │
│   ├── hooks/                  # Custom React hooks
│   │   ├── useScrollSpy.ts
│   │   ├── useTocObserver.ts
│   │   └── useHeadings.ts
│   │
│   ├── lib/                    # Business logic & utilities
│   │   ├── notion.ts           # Notion API client
│   │   ├── posts.ts            # Post data fetching
│   │   ├── tags.ts             # Tag utilities
│   │   └── utils.ts            # General utilities
│   │
│   ├── constants/              # Shared constants
│   │   └── ui.ts               # UI-related constants
│   │
│   ├── types/                  # TypeScript types
│   │   └── index.d.ts          # Global type definitions
│   │
│   └── styles/                 # Global styles
│       └── global.css          # Theme variables + Tailwind
│
├── public/                     # Static assets
├── .claude/                    # Claude Code configuration
│   ├── agents/                 # Custom sub-agents
│   └── skills/                 # Custom skills
├── .github/                    # GitHub configuration
│   └── PULL_REQUEST_TEMPLATE.md
├── .husky/                     # Git hooks
├── tailwind.config.ts          # Tailwind configuration
├── tsconfig.json               # TypeScript configuration
├── next.config.ts              # Next.js configuration
├── package.json                # Dependencies & scripts
├── commitlint.config.ts        # Commit message linting
├── CLAUDE.md                   # Project guide
└── README.md                   # Project documentation
```

## Naming Conventions

### Components

**Rule:** PascalCase

```
✅ Correct:
PostCard.tsx
NotionToc.tsx
ScrollToTop.tsx
ThemeToggle.tsx

❌ Wrong:
postCard.tsx
notion-toc.tsx
scroll_to_top.tsx
```

### Hooks

**Rule:** camelCase with `use` prefix

```
✅ Correct:
useScrollSpy.ts
useTocObserver.ts
useHeadings.ts
useScrollPosition.ts

❌ Wrong:
UseScrollSpy.ts
scroll-spy-hook.ts
scrollSpy.ts (missing use prefix)
```

### Utilities & Libraries

**Rule:** camelCase

```
✅ Correct:
notion.ts
posts.ts
tags.ts
utils.ts

❌ Wrong:
Notion.ts
Posts.ts
tag-utils.ts
```

### Types

**Rule:** camelCase file, PascalCase exports

```
✅ Correct:
File: index.d.ts
Export: interface Post { }
Export: type PostStatus = 'published' | 'draft';

❌ Wrong:
File: Post.d.ts
Export: interface post { }
```

### Constants

**Rule:** SCREAMING_SNAKE_CASE for values, camelCase for file

```
✅ Correct:
File: ui.ts
Exports:
  export const HEADER_OFFSET = 80;
  export const SCROLL_SPY_OFFSET = 100;

❌ Wrong:
export const headerOffset = 80;
export const header-offset = 80;
```

### API Routes

**Rule:** camelCase folder, route.ts file

```
✅ Correct:
app/api/revalidate/route.ts

❌ Wrong:
app/api/Revalidate/route.ts
app/api/revalidate/revalidate.ts
```

## Where to Place Files

### Decision Tree

**Q: Is it a React component?**
- Yes → `/src/components/`
  - App-wide (Navbar, Footer) → `/src/components/common/`
  - Post-specific (PostCard, NotionToc) → `/src/components/posts/`
  - Reusable UI primitive (Tag, Button) → `/src/components/ui/`

**Q: Is it a custom hook?**
- Yes → `/src/hooks/use[Name].ts`

**Q: Is it business logic or data fetching?**
- Yes → `/src/lib/`
  - Notion API → `/src/lib/notion.ts`
  - Post data → `/src/lib/posts.ts`
  - Utility functions → `/src/lib/utils.ts`

**Q: Is it a constant value?**
- Yes → `/src/constants/`
  - UI-related → `/src/constants/ui.ts`
  - API-related → `/src/constants/api.ts`

**Q: Is it a TypeScript type?**
- Yes → `/src/types/index.d.ts`

**Q: Is it a page or route?**
- Yes → `/src/app/[route]/page.tsx`

**Q: Is it an API endpoint?**
- Yes → `/src/app/api/[endpoint]/route.ts`

## Component Organization

### Common Components (`/src/components/common/`)

Components used across multiple pages:
- Layout components (Navbar, Footer)
- Page sections (Intro, Header)
- Shared widgets (ProgressBar)

**Examples:**
- `Navbar.tsx` - Site navigation
- `Footer.tsx` - Site footer
- `Intro.tsx` - Hero section with animations
- `ProgressBar.tsx` - Scroll progress indicator
- `Header.tsx` - Page headers

### Post Components (`/src/components/posts/`)

Components specific to blog posts:
- Post rendering (PostRenderer)
- Post navigation (NotionToc, PostNavigation)
- Post lists (PostList, PostCard)

**Examples:**
- `PostCard.tsx` - Individual post preview
- `PostList.tsx` - Grid of post cards
- `PostRenderer.tsx` - Notion content renderer
- `NotionToc.tsx` - Table of contents
- `PostNavigation.tsx` - Previous/Next navigation
- `GiscusComments.tsx` - Comment system

### UI Components (`/src/components/ui/`)

Low-level, reusable UI primitives:
- Buttons, inputs, switches
- Tags, badges
- Shadcn/ui components

**Examples:**
- `Tag.tsx` - Tag display
- `TagList.tsx` - Tag filtering
- `ThemeToggle.tsx` - Dark/light mode toggle
- `switch.tsx` - Radix UI switch (shadcn/ui)

## File Templates

### Component Template

```typescript
// For interactive components
"use client";

import { useState } from 'react';
import { motion } from 'framer-motion';

interface ComponentNameProps {
  // Props
}

export function ComponentName({ }: ComponentNameProps) {
  // Logic

  return (
    <div>
      {/* JSX */}
    </div>
  );
}
```

### Hook Template

```typescript
import { useState, useEffect } from 'react';

/**
 * Brief description of what this hook does
 *
 * @example
 * const value = useHookName();
 */
export function useHookName() {
  // Hook logic

  return value;
}
```

### Utility Template

```typescript
/**
 * Brief description of utility function
 *
 * @param paramName - Description
 * @returns Description
 */
export function utilityName(paramName: Type): ReturnType {
  // Implementation
}
```

### Type Definition Template

```typescript
// /src/types/index.d.ts

export interface Post {
  id: string;
  title: string;
  slug: string;
  date: string;
  description: string;
  tags: string[];
  status: PostStatus;
}

export type PostStatus = 'published' | 'draft' | 'archived';
```

## Import Organization

### Order

```typescript
// 1. React & Next.js
import { useState } from 'react';
import Link from 'next/link';

// 2. Third-party libraries
import { motion } from 'framer-motion';
import { Search } from 'lucide-react';

// 3. Internal imports (@/...)
import { Button } from '@/components/ui/button';
import { getAllPosts } from '@/lib/posts';
import { HEADER_OFFSET } from '@/constants/ui';

// 4. Relative imports
import { helperFunction } from '../utils';

// 5. Type imports (separate)
import type { Post } from '@/types';
```

### Path Aliases

Bellog uses `@/` for root imports:

```typescript
// ✅ Correct
import { PostCard } from '@/components/posts/PostCard';
import { getAllPosts } from '@/lib/posts';
import { HEADER_OFFSET } from '@/constants/ui';

// ❌ Wrong (no relative paths from root)
import { PostCard } from '../../components/posts/PostCard';
```

## Code Organization Patterns

### Single Responsibility

```typescript
// ✅ Good - Each file has one clear purpose
// /src/lib/notion.ts - Notion API calls
// /src/lib/posts.ts - Post data transformation
// /src/lib/tags.ts - Tag utilities

// ❌ Bad - Everything in one file
// /src/lib/everything.ts
```

### Group Related Code

```typescript
// ✅ Good - Related components together
/src/components/posts/
  PostCard.tsx
  PostList.tsx
  PostNavigation.tsx

// ❌ Bad - All components flat
/src/components/
  PostCard.tsx
  Navbar.tsx
  PostList.tsx
  Footer.tsx
```

### Constants Extraction

```typescript
// ✅ Good - Constants in separate file
// /src/constants/ui.ts
export const HEADER_OFFSET = 80;
export const SCROLL_SPY_OFFSET = 100;

// Component uses constants
import { HEADER_OFFSET } from '@/constants/ui';

// ❌ Bad - Magic numbers in component
const offset = 80; // What is this?
```

## File Size Guidelines

**Components:** < 200 lines
- If larger, consider splitting into smaller components

**Hooks:** < 100 lines
- If larger, consider extracting helper functions

**Utils:** < 50 lines per function
- If larger, break into smaller functions

**Types:** No limit
- Types can be long, that's okay

## Barrel Exports (Avoid)

```typescript
// ❌ Avoid barrel exports (index.ts files)
// /src/components/index.ts
export { PostCard } from './PostCard';
export { PostList } from './PostList';

// ✅ Prefer direct imports
import { PostCard } from '@/components/posts/PostCard';
import { PostList } from '@/components/posts/PostList';
```

**Why:** Barrel exports slow down builds and complicate tree-shaking.

## Environment Files

```
.env.local          # Local development secrets (gitignored)
.env.example        # Template (committed to git)
```

**Never commit:**
- `.env.local`
- `.env`
- Any file with actual secrets

## Git Ignore Patterns

Ensure these are in `.gitignore`:

```
# Dependencies
node_modules/
.pnp
.pnp.js

# Next.js
.next/
out/

# Environment
.env.local
.env

# IDE
.vscode/
.idea/

# OS
.DS_Store
```

## Documentation Structure

```
/                           # Root
├── README.md              # Project overview & setup
├── CLAUDE.md              # Development guide (for AI)
└── docs/                  # Detailed documentation (if needed)
    ├── architecture.md
    └── deployment.md
```

## Quick Reference

```
Components:     PascalCase.tsx      /src/components/{common,posts,ui}/
Hooks:          useName.ts          /src/hooks/
Utilities:      name.ts             /src/lib/
Constants:      NAME                /src/constants/
Types:          name.d.ts           /src/types/
Pages:          page.tsx            /src/app/[route]/
API:            route.ts            /src/app/api/[endpoint]/
```

## Checklist for New Files

- [ ] File in correct directory
- [ ] Naming convention followed (PascalCase / camelCase)
- [ ] Imports organized by category
- [ ] Using @ alias for imports (not relative from root)
- [ ] TypeScript types defined
- [ ] No magic numbers (use constants)
- [ ] Single responsibility (one clear purpose)
- [ ] File size reasonable (< 200 lines for components)

Remember: Organization is about findability. When someone looks for a file, it should be obvious where it is.
