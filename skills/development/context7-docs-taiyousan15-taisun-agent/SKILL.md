---
name: context7-docs
description: Use this skill when working with any framework or library (React, Next.js, Vue, Astro, etc.) to fetch up-to-date documentation and prevent hallucinated APIs. Triggers on keywords like "use context7", "latest docs", "current API", or when working with rapidly evolving frameworks.
---

# Context7 Documentation Fetching

This skill enables fetching up-to-date, version-specific documentation directly from official sources.

## Problem Solved

LLMs have stale training data. When working with Next.js 15, React 19, or any library that evolved since the model's cutoff date, you get:
- Hallucinated APIs that don't exist
- Deprecated patterns
- Outdated code examples

## When to Use

- Working with any framework/library (React, Next.js, Vue, Astro, Tailwind, etc.)
- Need current official documentation
- Want accurate code examples
- Encountering unfamiliar APIs
- Starting a new project with latest versions

## How to Activate

Simply include "use context7" in your prompt:

```
use context7 でNext.js 15のApp Routerについて教えて
```

```
use context7 React 19の新機能を使ってコンポーネントを作って
```

## Available Tools

### 1. resolve-library-id
Converts library name to Context7 ID.

```
Input: "next.js"
Output: "/vercel/next.js/v15.0.0"
```

### 2. get-library-docs
Fetches documentation chunks and code examples.

Parameters:
- `context7_id`: Library ID from resolve-library-id
- `topic` (optional): Specific topic to filter
- `tokens` (optional): Max tokens (default 5000)

## Example Usage

### Basic Documentation Fetch

```
User: use context7 でReact 19のuseActionStateの使い方を教えて

AI: [Calls resolve-library-id with "react"]
    [Calls get-library-docs with topic "useActionState"]
    [Returns current, accurate documentation]
```

### Framework Setup

```
User: use context7 で最新のAstro 5プロジェクトをセットアップして

AI: [Fetches current Astro 5 documentation]
    [Provides accurate setup commands and configuration]
```

## Supported Libraries

Context7 supports documentation from major frameworks and libraries:

| Category | Libraries |
|----------|-----------|
| **Frontend** | React, Vue, Svelte, Angular, Solid |
| **Meta-frameworks** | Next.js, Nuxt, Astro, Remix, SvelteKit |
| **Styling** | Tailwind CSS, CSS-in-JS libraries |
| **State** | Redux, Zustand, Jotai, Recoil |
| **Testing** | Jest, Vitest, Playwright, Cypress |
| **Backend** | Express, Fastify, Hono, tRPC |
| **Database** | Prisma, Drizzle, TypeORM |
| **Build** | Vite, esbuild, webpack, turbopack |

## Best Practices

1. **Always use for rapidly evolving frameworks**
   - Next.js (major updates frequently)
   - React (new features in v19)
   - Tailwind (v4 breaking changes)

2. **Specify version when needed**
   ```
   use context7 Next.js 15.1の新機能
   ```

3. **Combine with specific topics**
   ```
   use context7 Prismaのリレーション設定
   ```

4. **Use for debugging**
   ```
   use context7 このエラーはReact 19で解決されてる？
   ```

## Integration with TAISUN

Context7 is automatically available via MCP. No additional setup required.

When you include "use context7" or work with framework-specific tasks, the system will:
1. Detect the library/framework
2. Resolve the Context7 ID
3. Fetch relevant documentation
4. Provide accurate, current information

## Source

- [Context7 GitHub](https://github.com/upstash/context7)
- [Upstash Blog](https://upstash.com/blog/context7-mcp)
