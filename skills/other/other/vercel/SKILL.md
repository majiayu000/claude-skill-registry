---
name: vercel
description: "Deploy and manage Vercel projects, domains, environment variables, and serverless functions using the `vercel` CLI."
---

# Vercel Skill

Use the `vercel` CLI to deploy and manage Vercel projects.

## Deployments

Deploy current directory:
```bash
vercel
```

Deploy to production:
```bash
vercel --prod
```

List recent deployments:
```bash
vercel ls
```

Inspect a deployment:
```bash
vercel inspect <deployment-url>
```

View deployment logs:
```bash
vercel logs <deployment-url>
```

Redeploy a previous deployment:
```bash
vercel redeploy <deployment-url>
```

## Projects

List all projects:
```bash
vercel project ls
```

Link current directory to a project:
```bash
vercel link
```

Remove a project:
```bash
vercel project rm <project-name>
```

## Domains

List domains:
```bash
vercel domains ls
```

Add a domain to a project:
```bash
vercel domains add <domain> <project-name>
```

Check domain configuration:
```bash
vercel domains inspect <domain>
```

## Environment Variables

List env vars for a project:
```bash
vercel env ls
```

Add an env var:
```bash
vercel env add <name>
```

Pull env vars to local .env file:
```bash
vercel env pull
```

Remove an env var:
```bash
vercel env rm <name>
```

## Local Development

Run project locally with Vercel's dev server:
```bash
vercel dev
```

Pull latest project settings:
```bash
vercel pull
```

Build project locally:
```bash
vercel build
```

## Secrets (Legacy)

Note: Secrets are deprecated in favor of Environment Variables.

## Teams

List teams:
```bash
vercel teams ls
```

Switch to a team:
```bash
vercel switch <team-slug>
```

## Authentication

Check current login:
```bash
vercel whoami
```

Login:
```bash
vercel login
```

Logout:
```bash
vercel logout
```
