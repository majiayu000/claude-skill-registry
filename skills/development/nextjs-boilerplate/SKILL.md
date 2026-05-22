---
name: nextjs-boilerplate
description: Bootstrap a new Next.js development environment with Tailwind CSS, shadcn/ui components, and assistant-ui for AI chat interfaces. Use when the user asks to "create a new Next.js project", "bootstrap Next.js with shadcn", "set up a Next.js app", "create an AI chat app", "start a new React project with Tailwind", or mentions creating a fresh frontend project with modern tooling.
---

# Next.js Boilerplate Setup

Bootstrap a production-ready Next.js project with modern tooling.

## When to Use

- User asks to create a new Next.js project
- User wants to set up a React app with Tailwind CSS
- User needs shadcn/ui components
- User wants to build an AI chat interface
- Starting a fresh frontend project with modern tooling

## Stack Overview

| Layer | Technology | Purpose |
|-------|------------|---------|
| Framework | Next.js 14+ (App Router) | React framework with SSR/SSG |
| Styling | Tailwind CSS | Utility-first CSS |
| Components | shadcn/ui | Accessible, customizable components |
| AI Chat | assistant-ui | Pre-built AI chat interface components |
| TypeScript | Strict mode | Type safety |

## Setup Process

### Step 1: Create Next.js Project

```bash
npx create-next-app@latest my-app --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"
cd my-app
```

**Flags explained:**
- `--typescript`: TypeScript support
- `--tailwind`: Tailwind CSS pre-configured
- `--eslint`: ESLint for code quality
- `--app`: App Router (not Pages Router)
- `--src-dir`: Use `src/` directory structure
- `--import-alias`: Clean imports with `@/`

### Step 2: Initialize shadcn/ui

```bash
npx shadcn@latest init
```

**Recommended configuration:**
- Style: Default
- Base color: Slate (or user preference)
- CSS variables: Yes
- React Server Components: Yes
- Import alias for components: `@/components`
- Import alias for utils: `@/lib/utils`

### Step 3: Add Common Components

```bash
npx shadcn@latest add button card input label
npx shadcn@latest add dialog dropdown-menu
npx shadcn@latest add form (includes react-hook-form + zod)
```

### Step 4: Add assistant-ui (Optional - for AI Chat)

```bash
npx assistant-ui@latest create
```

Or manual installation:

```bash
pnpm add @assistant-ui/react @assistant-ui/react-markdown
```

## Project Structure

```
src/
├── app/
│   ├── layout.tsx      # Root layout with providers
│   ├── page.tsx        # Home page
│   ├── globals.css     # Tailwind imports + custom styles
│   └── (routes)/       # Route groups
├── components/
│   ├── ui/             # shadcn/ui components
│   └── ...             # Custom components
├── lib/
│   └── utils.ts        # Utility functions (cn, etc.)
└── hooks/              # Custom React hooks
```

## Essential Configurations

### tailwind.config.ts

shadcn/ui sets this up, but verify:
- Dark mode: `class` strategy
- Content paths include all component locations
- CSS variables for theming

### TypeScript (tsconfig.json)

Ensure strict mode:

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true
  }
}
```

### ESLint

Add helpful rules to `.eslintrc.json`:

```json
{
  "extends": ["next/core-web-vitals"],
  "rules": {
    "@typescript-eslint/no-unused-vars": ["error", { "argsIgnorePattern": "^_" }]
  }
}
```

## Common Patterns

### Layout with Theme Provider

```tsx
// src/app/layout.tsx
import { ThemeProvider } from "@/components/theme-provider"

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
          {children}
        </ThemeProvider>
      </body>
    </html>
  )
}
```

### cn() Utility Usage

```tsx
import { cn } from "@/lib/utils"

<div className={cn(
  "base-styles",
  condition && "conditional-styles",
  className
)} />
```

### Form Pattern with react-hook-form + zod

```tsx
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"

const schema = z.object({
  email: z.string().email(),
})

function MyForm() {
  const form = useForm({
    resolver: zodResolver(schema),
  })
  // ...
}
```

## assistant-ui Integration

### Basic Chat Setup

```tsx
import { Thread } from "@assistant-ui/react"
import { useVercelAIRuntime } from "@assistant-ui/react-ai-sdk"
import { useChat } from "ai/react"

export function Chat() {
  const chat = useChat({ api: "/api/chat" })
  const runtime = useVercelAIRuntime(chat)

  return <Thread runtime={runtime} />
}
```

### API Route (App Router)

```tsx
// src/app/api/chat/route.ts
import { openai } from "@ai-sdk/openai"
import { streamText } from "ai"

export async function POST(req: Request) {
  const { messages } = await req.json()
  const result = await streamText({
    model: openai("gpt-4o"),
    messages,
  })
  return result.toDataStreamResponse()
}
```

## Verification Checklist

After setup, verify:

- [ ] `pnpm dev` starts without errors
- [ ] Tailwind styles apply correctly
- [ ] shadcn/ui Button renders properly
- [ ] Dark mode toggle works (if added)
- [ ] TypeScript has no errors: `pnpm tsc --noEmit`
- [ ] ESLint passes: `pnpm lint`

## Common Issues

### Tailwind Not Working

1. Check `globals.css` has Tailwind directives
2. Verify `tailwind.config.ts` content paths
3. Restart dev server after config changes

### shadcn/ui Component Not Found

```bash
npx shadcn@latest add [component-name]
```

### Hydration Mismatch

Add `suppressHydrationWarning` to `<html>` tag when using theme providers.

### Import Errors

Verify `tsconfig.json` paths match shadcn/ui init choices.

## Quick Reference Commands

```bash
# Development
pnpm dev

# Build
pnpm build

# Type check
pnpm tsc --noEmit

# Lint
pnpm lint

# Add shadcn component
npx shadcn@latest add [name]

# List available components
npx shadcn@latest add
```

## When NOT to Use This Stack

- Simple static sites (use Astro or plain HTML)
- Apps requiring different styling approach (CSS Modules, styled-components)
- Non-React projects
- When the user has an existing project with different tooling
