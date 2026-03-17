---
name: Zero Creator
description: Gerador de Projetos Autônomo projetado por um Arquiteto PhD. Orquestra Vercel, Supabase e Frameworks para criar aplicações fullstack prontas para produção.
---

# Zero Creator

The **Zero Creator** is a meta-skill that orchestrates other skills (Vercel, Supabase, Node, Git) to bootstrap detailed, production-ready full-stack applications.

## Capability

It transforms a high-level idea (e.g., "A SaaS for managing dog walkers") into a deployed URL with database, auth, and frontend configured.

## Workflows

### 1. Bootstrap Full Stack App

Creates a Next.js (Frontend) + Supabase (Backend) project.

**Usage:**
"Zero, create a new SaaS called 'DogWalkerPro' using Next.js and Supabase."

**Steps:**

1. **Init Frontend:** `npx create-next-app@latest ./dog-walker-pro --typescript --tailwind --eslint`
2. **Init Backend:** `cd dog-walker-pro && supabase init`
3. **Setup Auth:** Configure Supabase Auth (requires user interaction for keys).
4. **Scaffold UI:** Generate landing page, dashboard shell, and login page.
5. **Git Init:** `git init && git add . && git commit -m "feat: initial commit by Zero Creator"`

### 2. Deploy to Production

Connects the local project to Vercel and deploys.

**Usage:**
"Zero, deploy this project to production."

**Steps:**

1. **Vercel Link:** `vercel link`
2. **Vercel Env:** `vercel env pull .env.local`
3. **Deploy:** `vercel deploy --prod`

## Best Practices (PhD Level)

- **Architecture:** Always use a 'src' directory. Separate 'components', 'hooks', 'lib', and 'types'.
- **Type Safety:** Strict TypeScript everywhere. No `any`. Zod for validation.
- **Styling:** Tailwind CSS with a predefined design system (colors, spacing) in `tailwind.config.js`.
- **Error Handling:** Global Error Boundaries and Toast notifications for user feedback.

## Commands

```bash
# Meta-command placeholder (Agent orchestrates actual CLI calls)
zero-creator scaffold <project-name> <stack>
```
