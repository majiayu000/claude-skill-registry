---
name: next
description: "Next.js framework patterns and best practices for fullstack React applications. Routing, SSR/SSG, API routes, middleware, deployment. Trigger: When building with Next.js, configuring SSR/SSG, or deploying Next.js apps."
skills:
  - conventions
  - react
  - typescript
  - architecture-patterns
  - humanizer
dependencies:
  next: ">=13.0.0 <15.0.0"
  react: ">=18.0.0 <19.0.0"
allowed-tools:
  - documentation-reader
  - web-search
---

# Next.js Skill

## When to Use

- Building React apps with SSR/SSG
- Implementing API routes or middleware
- Deploying fullstack React projects

## Critical Patterns

- Use file-based routing and dynamic routes
- Prefer server components for data fetching
- Leverage middleware for auth and rewrites

## Decision Tree

- SSR/SSG needed? → Use getServerSideProps/getStaticProps
- API needed? → Use /pages/api or app/api
- Custom routing? → Use dynamic routes

## Edge Cases

- Incremental static regeneration
- Middleware edge limitations
- API route cold starts
