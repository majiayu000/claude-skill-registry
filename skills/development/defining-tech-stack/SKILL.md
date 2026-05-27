---
name: defining-tech-stack
description: Locks in specific versions for the Tourly project tech stack. Use when initializing the project or adding new core dependencies.
---

# Project Tech Stack Definition

## When to use this skill
- At the start of the project to ensure version consistency.
- When documentation queries need to be version-specific.

## Workflow
- [ ] Initialize Next.js project using `npx create-next-app@latest`.
- [ ] Verify core versions in `package.json`.
- [ ] Document locked versions in this skill or a central `README.md`.

## Tech Stack (Locked Versions)
- **Frontend**: Next.js 15 (App Router), React 19.
- **Backend**: Appwrite Cloud (v1.6+ SDK).
- **Styling**: Tailwind CSS 4 (or latest stable compatible with Next.js 15).
- **Icons**: Lucide React.
- **Forms**: React Hook Form + Zod.

## Instructions
- **App Router**: Exclusively use `app/` directory and Server Components by default.
- **Server Actions**: Use for all mutations.
- **Appwrite SDK**: Only use `appwrite` (Web SDK) and `node-appwrite` (Server SDK) as appropriate.
