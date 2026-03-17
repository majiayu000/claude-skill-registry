---
name: vercel-deploy
description: Automated Vercel deployment skill.
category: infrastructure
version: 4.1.0-fractal
layer: master-skill
---

# Vercel Deployment Skill

> **Goal**: Seamlessly deploy any frontend/full-stack application to Vercel global edge network.

## 1. Prerequisites

- **CLI**: `vercel` (Install via `npm i -g vercel`)
- **Auth**: User must be logged in (`vercel login`) or provide `VERCEL_TOKEN`.

## 2. Deployment Workflow

1.  **Detection**:
    - Scanner checks `package.json` for frameworks (Next.js, Vite, Remix, Astro).
    - Identifies build command (`npm run build`) and output directory (`dist` or `.next`).

2.  **Configuration**:
    - Generates `vercel.json` if custom headers/rewrites are needed.
    - Sets project settings (Root Directory, Framework Preset).

3.  **Execution**:
    - **Preview**: `vercel --no-prod` (For testing feature branches).
    - **Production**: `vercel --prod` (For live release).

4.  **Verification**:
    - Checks deployment status via `vercel inspect <url>`.
    - Returns the **Claimable URL** for the user.

## 3. Environment Variables

- **Auto-Sync**: Pulls `.env` from Vercel Project Settings (`vercel env pull`).
- **Push**: Pushes local `.env` to Vercel (Interactive confirmation required).

## 4. Troubleshooting common errors

- **Build Fail**: Usually due to strict type checking or linting in CI. Suggest `ignoreBuildErrors: true` ONLY for hotfixes.
- **Missing Secrets**: Check if `VERCEL_TOKEN` is active in CI/CD environment.

---

**Command Reference**:
- `vercel link`: Link local folder to remote project.
- `vercel deploy`: Deploy preview.
- `vercel deploy --prod`: Deploy production.
