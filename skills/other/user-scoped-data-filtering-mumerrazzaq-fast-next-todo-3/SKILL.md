---
name: user-scoped-data-filtering
description: "Provides patterns and guidance for implementing user-scoped data filtering and multi-tenancy in web applications. Use this skill when you need to: (1) Restrict data access based on user identity, (2) Implement ownership checks for database operations, (3) Build multi-tenant applications with organization-level data scoping, (4) Implement admin bypass for viewing all data, (5) Create audit trails for data access. This skill focuses on Python, FastAPI, and SQLAlchemy."
---

# User-Scoped Data Filtering

This skill provides patterns and best practices for implementing robust user-scoped data filtering and multi-tenancy in your application. The focus is on a Python-based stack using FastAPI for the web framework and SQLAlchemy for the ORM.

## Overview

Implementing proper data scoping is critical for security and privacy in multi-user applications. This skill breaks down the process into several key areas, each with its own reference guide.

## Core Concepts & Workflow

1.  **User Context Extraction**: The first step is to reliably identify the current user. This is typically done by extracting user information from an authentication token (e.g., JWT).
    *   For implementation details, see `references/user-context.md`.

2.  **Scoped Database Queries**: Once you have the user's identity, you must filter all database queries to only return data they are authorized to see.
    *   For service layer patterns and SQLAlchemy examples, see `references/scoped-queries.md`.

3.  **Ownership Verification**: For write operations (updates and deletes), you must verify that the user owns the resource they are trying to modify. This is often implemented using decorators or dependencies.
    *   For decorator patterns, see `references/ownership-verification.md`.

4.  **Multi-Tenancy**: In many applications, data is scoped not just by user, but by a higher-level entity like an organization or a team.
    *   For examples of organization-level scoping, see `references/multi-tenancy.md`.

5.  **Admin Bypass**: Administrative users often need to bypass these scoping rules to view and manage data across all users and organizations.
    *   For patterns to implement this safely, see `references/admin-bypass.md`.

6.  **Audit Trail**: It's important to log who is accessing and modifying data, especially when admin bypass is used.
    *   For guidance on creating audit trails, see `references/audit-trail.md`.

## Getting Started

Start by reviewing `references/user-context.md` to set up your user identification dependency. Then, move on to `references/scoped-queries.md` to apply filtering to your data access layer. Implement the other patterns as needed for your application's requirements.
