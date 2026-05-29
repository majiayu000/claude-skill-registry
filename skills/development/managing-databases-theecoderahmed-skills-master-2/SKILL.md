---
name: managing-databases
description: Generates secure, owner-only admin dashboards for PostgreSQL or MongoDB. Capable of handling schema definitions, operational tasks, and basic CRUD, with flexible security models.
---

# Database Admin Generator

## When to use this skill
- When the user asks for an "Admin Panel", "Dashboard", or "Internal Tool" for their database.
- When the user needs to visualize or manipulate data in PostgreSQL or MongoDB.
- When the user demands high security for managing sensitive data.

## Workflow
1.  **Requirement Check**:
    - **DB Type**: PostgreSQL or MongoDB?
    - **Scope**: Structural (Schema/Models) or Operational (Raw SQL/Backups)?
    - **Auth**: Hardcoded (Env Var) or Identity (OAuth)?
2.  **Architecture Setup**:
    - Scaffold a **Next.js** application (App Router).
    - Install core libs: `prisma` (SQL) or `mongoose` (Mongo), plus UI components (Shadcn/UI recommended).
3.  **Security Implementation**:
    - Create a global `middleware.ts` to block ALL routes unless authenticated.
    - If **Hardcoded**: Check a session cookie against `ADMIN_PASSWORD`.
    - If **Identity**: Integrate NextAuth.js with `ALLOWED_EMAILS` whitelist.
4.  **Feature Build**:
    - **Schema Mode**: specialized pages for "Table Editor" or "Collection Manager".
    - **Ops Mode**: "Query Playground" and "Health/Metrics" pages.
5.  **Final Polish**:
    - Add "System Status" indicator.
    - Ensure strict Content Security Policy headers.

## Instructions

### 1. Database Connection Patterns
*   **PostgreSQL**: Always utilize **Prisma ORM** for type safety on the admin side.
    *   *Ops Mode*: Allow raw parameterized queries via `prisma.$queryRaw`.
*   **MongoDB**: Use **Mongoose** for schema definitions if "Structural" is requested; use raw `MongoClient` for "Ops" to allow unrestricted aggregation pipelines.

### 2. Security Patterns
*   **The "Ironclad" Middleware**:
    ```typescript
    // middleware.ts
    export function middleware(req) {
      const session = getSession(req);
      if (!session || !isOwner(session.user)) {
        return new Response("Unauthorized Access Prohibited", { status: 403 });
      }
    }
    ```
*   **Env Validation**: Fail build immediately if `ADMIN_SECRET` or `DATABASE_URL` is missing.

### 3. UI/UX Guidelines
*   **Aesthetics**: Use "Dark Mode" by default for admin tools (reduces eye strain for Ops).
*   **Feedback**: Every destructive action (Drop Table, Delete Many) **MUST** have a "Type the name to confirm" modal.
*   **Data Density**: Use compact tables with expandable rows for JSON/BSON data.

## Resources
*   [NextAuth.js Documentation](https://next-auth.js.org/)
*   [Prisma Best Practices](https://www.prisma.io/docs/)
