---
name: react-performance-optimizer
description: Analyzes React/Next.js code for performance bottlenecks, focusing on waterfalls, bundle size, and rendering efficiency.
license: MIT
metadata:
  author: Vercel Labs (Synthesized)
  version: "1.0.0"
compatibility:
  - product: VS Code
  - product: Claude Desktop
  - framework: React 18+
  - framework: Next.js 13+
allowed-tools:
  - read_file
  - search_file_content
---

# React Performance Optimization Skill

This skill assists in identifying and resolving common performance issues in React and Next.js applications. It applies rules from Vercel's engineering best practices.

## When to Use This Skill

*   When a user asks to "optimize" a React component or page.
*   When a user mentions "slow loading", "waterfalls", or "large bundle size".
*   When reviewing code for production readiness.

## Core Capabilities

1.  **Waterfall Detection**: Identifies nested data fetching patterns that block rendering.
2.  **Bundle Size Analysis**: Suggests dynamic imports (`next/dynamic`, `React.lazy`) for heavy components.
3.  **Render Optimization**: Checks for unnecessary re-renders and suggests `useMemo`, `useCallback`, or composition patterns.
4.  **Image Optimization**: Verifies usage of `next/image` and proper sizing attributes.
5.  **Server Components**: Recommends moving logic to Server Components (RSC) where appropriate to reduce client JS.

## Workflow

1.  **Analyze Imports**: Check for heavy libraries (e.g., moment.js, lodash) that could be tree-shaken or replaced.
2.  **Check Data Fetching**:
    *   Look for `await` inside loops or sequential `await` calls that could be `Promise.all`.
    *   Identify Client Components fetching data that could be Server Components.
3.  **Inspect Rendering Logic**:
    *   Look for expensive computations directly in the render body.
    *   Check for `useEffect` usage that triggers cascading updates.
4.  **Review References**: Consult `references/performance_rules.md` for specific patterns to avoid.

## Example Usage

**User**: "Why is my dashboard loading so slowly?"

**Agent**:
1.  Read `src/app/dashboard/page.tsx` and components.
2.  Identify multiple sequential `await fetch(...)` calls.
3.  Suggest using `Promise.all` or moving data fetching up to a layout/parent RSC.
4.  Suggest wrapping the Chart component with `next/dynamic`.

## References

*   `references/performance_rules.md`: detailed explanation of the rules.
