---
name: nextjs-app-router-navigation
description: "Provides guidance and reusable assets for implementing navigation in Next.js App Router. Covers file-based routing, dynamic routes, layouts, loading/error UI, protected routes with middleware, and navigation patterns like Link, useRouter, and redirect. Use when working on routing or navigation tasks in a Next.js App Router project."
---

# Next.js App Router Navigation

This skill provides guidance and reusable assets for implementing routing and navigation in a Next.js application using the App Router.

## Core Concepts

The Next.js App Router introduces several conventions and patterns for handling routing, UI states, and navigation. This skill covers the most important ones.

### When to Use This Skill

Use this skill when you need to:
-   Understand or implement file-based routing.
-   Create dynamic routes (e.g., for blog posts or product pages).
-   Structure your app with layouts or route groups.
-   Implement loading and error UIs.
-   Protect routes using middleware for authentication.
-   Navigate between pages using `<Link>`, `useRouter`, or `redirect`.
-   Implement advanced patterns like parallel or intercepting routes.

## Table of Contents

1.  [**Routing Patterns**](#routing-patterns)
2.  [**UI Patterns**](#ui-patterns)
3.  [**Navigation**](#navigation)
4.  [**Protected Routes**](#protected-routes)
5.  [**Reusable Assets**](#reusable-assets)

---

## 1. Routing Patterns

File-based routing is the core of the App Router. Folders define route segments, and `page.tsx` files make them publicly accessible.

-   **Dynamic Routes**: Use `[folderName]` for dynamic segments.
-   **Catch-all Routes**: Use `[...folderName]` to match multiple segments.
-   **Route Groups**: Use `(folderName)` to organize routes without affecting the URL.

For detailed examples and file structures, refer to the routing patterns guide:
**Read: [references/routing-patterns.md](./references/routing-patterns.md)**

---

## 2. UI Patterns

The App Router has special file conventions for creating UI for different states.

-   **`layout.tsx`**: Shared UI for a segment and its children.
-   **`loading.tsx`**: A loading indicator shown during server-side rendering.
-   **`error.tsx`**: A fallback UI for unexpected errors.
-   **Parallel Routes**: Render multiple pages in the same layout using named slots (`@folder`).
-   **Intercepting Routes**: Intercept a route to show another route in its place, useful for modals.

For implementation details and code examples, see the UI patterns guide:
**Read: [references/ui-patterns.md](./references/ui-patterns.md)**

---

## 3. Navigation

There are several ways to handle navigation in the App Router, depending on the context (client or server).

-   **`<Link>` component**: The primary method for client-side navigation. Prefetches routes for a faster experience.
-   **`useRouter` hook**: For programmatic navigation in Client Components.
-   **`redirect` function**: To redirect users from Server Components or Server Actions.

For usage examples of each method, consult the navigation guide:
**Read: [references/navigation.md](./references/navigation.md)**

---

## 4. Protected Routes

Use middleware to protect routes that require authentication. Middleware runs before a request is completed and can redirect users based on their session status.

-   Create a `middleware.ts` file in the root of your project.
-   Use the `matcher` config to specify which paths the middleware should apply to.

For a detailed explanation and a complete middleware example, see the protected routes guide:
**Read: [references/protected-routes.md](./references/protected-routes.md)**

---

## 5. Reusable Assets

This skill includes several templates to help you get started quickly.

-   **Full App Router Template**: A complete directory structure demonstrating many of the concepts in this skill.
    -   **Location**: `assets/app-router-template/`
-   **Middleware Template**: A ready-to-use middleware file for authentication.
    -   **Read**: `assets/middleware-template.ts`
-   **Root Layout Template**: A basic root layout with navigation.
    -   **Read**: `assets/layout-template.tsx`
-   **Navigation Component Template**: A responsive navigation bar component.
    -   **Read**: `assets/navigation-component-template.tsx`

To use a template, copy the file or directory structure into your project and adapt it to your needs.
