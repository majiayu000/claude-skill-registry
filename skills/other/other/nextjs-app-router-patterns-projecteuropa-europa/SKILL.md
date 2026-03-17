---
name: nextjs-app-router-patterns
description: Master Next.js 16+ App Router with Server Components, streaming, parallel routes, and advanced data fetching. Use when building Next.js applications, implementing SSR/SSG, or optimizing React Server Components.
---

# Next.js App Router Patterns

Comprehensive patterns for Next.js 16+ App Router architecture, Server Components, and modern full-stack React development.

> [!CAUTION]
> **Project Europa 制約**: このプロジェクトは `output: 'export'` (静的エクスポート) を使用しているため、以下の機能は**使用不可**です:
> - Server Components (RSC)
> - Server Actions (`'use server'`)
> - Streaming / Suspense boundaries
> - Route Handlers (API Routes)
> - ISR / Cache tags
>
> 代替: TanStack Query でクライアントサイドデータ取得、Hono バックエンド (`/api/v2/`) を使用してください。

## Use this skill when

- Building new Next.js applications with App Router (v16+)
- Migrating from Pages Router to App Router
- Implementing Server Components and streaming
- Setting up parallel and intercepting routes
- Optimizing data fetching and caching
- Building full-stack features with Server Actions

## Do not use this skill when

- The task is unrelated to next.js app router patterns
- You need a different domain or tool outside this scope

## Instructions

- Clarify goals, constraints, and required inputs.
- Apply relevant best practices and validate outcomes.
- Provide actionable steps and verification.
- If detailed examples are required, open `resources/implementation-playbook.md`.

## Resources

- `resources/implementation-playbook.md` for detailed patterns and examples.
