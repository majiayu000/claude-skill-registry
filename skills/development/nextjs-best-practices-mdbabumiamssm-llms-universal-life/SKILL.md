---name: nextjs-best-practices
description: Guidelines for building scalable, SEO-friendly applications with Next.js (App Router).
license: MIT
metadata:
  author: AI Group
  version: "1.0.0"
  category: Software_Engineering
compatibility:
  - system: Next.js 14+
  - system: React 18+
allowed-tools:
  - read_file
  - replace
  - write_file

keywords:
  - nextjs-best-practices
  - automation
  - biomedical
measurable_outcome: execute task with >95% success rate.
---"

# Next.js Best Practices

This skill outlines the standards for developing modern web applications using the Next.js App Router. It covers server components, data fetching, caching strategies, and route handling.

## When to Use This Skill

*   **Project Setup**: Initializing a new Next.js project.
*   **Architecture Design**: Deciding between Server vs. Client Components.
*   **Optimization**: Improving Core Web Vitals, LCP, and CLS.
*   **SEO Strategy**: Implementing Metadata API and sitemaps.

## Core Capabilities

1.  **App Router Architecture**: structuring `app/`, `layout.tsx`, `page.tsx`, and `loading.tsx`.
2.  **Server Actions**: Handling form submissions and mutations without API routes.
3.  **Data Fetching**: Implementing `fetch` with caching tags and revalidation strategies.
4.  **Middleware**: Authentication and request processing at the edge.

## Workflow

1.  **Determine Component Type**: Default to Server Components. "Use Client" only for interactivity (hooks, event listeners).
2.  **Plan Data Access**: Fetch data directly in Server Components where possible.
3.  **Implement Metadata**: specific exportable `metadata` objects for SEO.
4.  **Handle Errors**: Use `error.tsx` and `global-error.tsx` for graceful degradation.

## Example Usage

**User**: "Create a blog post page that fetches data from a CMS."

**Agent Action**:
1.  Reads `references/rules.md`.
2.  Generates `app/blog/[slug]/page.tsx` as an async Server Component.
3.  Uses `generateStaticParams` for SSG.
