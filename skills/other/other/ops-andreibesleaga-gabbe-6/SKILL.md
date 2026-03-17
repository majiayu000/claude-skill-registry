---
name: cloud-deploy
description: Deploy applications to modern cloud platforms (Vercel, Railway, AWS).
context_cost: medium
---
# Cloud Deploy Skill

## Triggers
- deploy
- vercel
- railway
- aws
- sst
- serverless
- lambda
- flightcontrol
- neon
- supabase

## Purpose
To configure rapid, developer-friendly deployments on modern PaaS and Serverless platforms.

## Capabilities

### 1. Vercel (Frontend & Edge)
-   **Config**: `vercel.json` for headers, redirects, and clean URLs.
-   **Edge Functions**: Deploying middleware and lightweight backend logic.
-   **Preview Mode**: Setting up preview comments on PRs.

### 2. Railway (Backend & DBs)
-   **Config**: `railway.toml` for build commands and monorepo root.
-   **Databases**: Provisioning Postgres, Redis, MySQL plugins.
-   **Variables**: Managing secrets and environment variables.

### 3. AWS (SST / CDK)
-   **SST**: Defining `sst.config.ts` for serverless stacks (Next.js, API Gateway, DynamoDB).
-   **Constructs**: Using high-level constructs for easy setup (Cron, Bucket, Queue).
-   **IAM**: Setting up fine-grained permissions for functions.

## Instructions
1.  **Platform Choice**:
    -   **Frontend/Fullstack JS**: Vercel.
    -   **Docker/Stateful/Backend**: Railway.
    -   **Enterprise/Complex/Serverless**: AWS (via SST).
2.  **Environment Parity**: Ensure `.env` vars match across local and cloud (but values differ).
3.  **Infrastructure as Code**: Always define the deployment config locally (don't click-ops settings).

## Deliverables
-   `vercel.json`
-   `railway.toml`
-   `sst.config.ts`
