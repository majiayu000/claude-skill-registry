---
name: web-deploy
cluster: web-dev
description: "Deployment: Cloudflare Pages/Workers, Vercel, Netlify, Docker, GitHub Actions CI/CD"
tags: ["deployment","ci-cd","cloudflare","web"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "deploy cloudflare pages vercel netlify ci cd pipeline github actions"
---

# web-deploy

## Purpose
This skill automates deployment of web applications to platforms like Cloudflare Pages/Workers, Vercel, Netlify, Docker, and GitHub Actions CI/CD pipelines. It focuses on streamlining the process from code commit to live deployment, handling configurations, builds, and environment integrations.

## When to Use
Use this skill for deploying static sites, serverless functions, or containerized apps. Apply it when setting up CI/CD for frequent updates, migrating projects to cloud platforms, or automating deployments in response to GitHub events. Ideal for web-dev workflows involving version control and cloud services.

## Key Capabilities
- Deploy static sites to Cloudflare Pages using Git integration or CLI.
- Handle serverless deployments to Cloudflare Workers via API or Wrangler CLI.
- Automate Vercel deployments with CLI commands and environment variables.
- Set up Netlify for site builds and deploys using their API or CLI.
- Containerize applications with Docker and orchestrate CI/CD via GitHub Actions.
- Manage pipelines that include build steps, testing, and deployment triggers.

## Usage Patterns
Follow these patterns to integrate deployments into your workflow:
- For new projects, initialize with a platform-specific config file (e.g., `vercel.json` for Vercel).
- In CI/CD, trigger deployments on pull requests or merges using GitHub Actions workflows.
- Use environment variables for secrets, like `$CLOUDFLARE_API_TOKEN` for authentication.
- Example 1: Deploy a React app to Vercel—Clone repo, run `npx vercel` in project root, select options, and push changes.
- Example 2: Set up CI/CD for a Dockerized app—Create a `.github/workflows/deploy.yml` file with steps to build Docker image and deploy to Netlify via API call.

## Common Commands/API
Use these exact commands and APIs for tasks:
- Cloudflare Pages: Run `npx wrangler pages deploy ./build --project-name=my-site` to deploy a build folder; API endpoint: POST https://api.cloudflare.com/client/v4/accounts/{account_id}/pages/projects/{project_name}/deployments with JSON body {"files": [...]}, auth via `$CLOUDFLARE_API_TOKEN`.
- Vercel: Execute `npx vercel deploy --prod` from project directory; config in `vercel.json`: {"version": 2, "builds": [{"src": "package.json", "use": "@vercel/node"}]}, auth with `$VERCEL_TOKEN`.
- Netlify: Command: `netlify deploy --dir=build --prod`; API: POST https://api.netlify.com/api/v1/sites/{site_id}/deploys with form data, using `$NETLIFY_ACCESS_TOKEN`.
- Docker: Build image with `docker build -t my-app:latest .`; Push to registry: `docker push my-repo/my-app:latest`.
- GitHub Actions: In YAML file, use: `run: echo "::set-env name=GITHUB_TOKEN::${{ secrets.GITHUB_TOKEN }}"` then `run: gh workflow run deploy.yml`; Example snippet:
  ```
  jobs:
    build:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v2
        - run: docker build . -t my-app
  ```
- For CI/CD, add workflow triggers: `on: [push, pull_request]` in `.github/workflows/main.yml`.

## Integration Notes
Integrate by setting environment variables in your CI/CD config, e.g., add `env: { API_KEY: ${{ secrets.SERVICE_API_KEY }} }` in GitHub Actions. For multi-platform setups, use a monorepo with separate configs (e.g., `netlify.toml` and `vercel.json`). Link with GitHub by adding webhooks: POST to https://api.github.com/repos/{owner}/{repo}/hooks with JSON payload. Ensure Docker images are tagged correctly for deployments, like `docker tag my-app:latest registry.example.com/my-app:1.0`. For API integrations, handle rate limits by checking response headers like X-RateLimit-Remaining.

## Error Handling
Handle errors by checking exit codes and logs; for CLI commands, use try-catch in scripts (e.g., in Bash: `if ! npx vercel deploy; then echo "Deployment failed"; exit 1; fi`). Common issues: Authentication failures—verify env vars like `$CLOUDFLARE_API_TOKEN` is set; resolve with `export CLOUDFLARE_API_TOKEN=your_key`. For API errors, parse responses (e.g., if status code is 429, wait and retry). In GitHub Actions, use `continue-on-error: true` for non-critical steps, then check outputs. Example snippet for error logging:
  ```
  try {
    await fetch('https://api.cloudflare.com/...', { headers: { Authorization: `Bearer ${process.env.CLOUDFLARE_API_TOKEN}` } });
  } catch (error) {
    console.error('API error:', error.message);
  }
  ```
Debug deployments by enabling verbose modes, like `npx vercel deploy --debug`.

## Graph Relationships
- Related to cluster: web-dev (e.g., shares nodes with skills like web-build or api-integration).
- Connected via tags: deployment (links to ci-cd skills), ci-cd (connects to github-actions tools), cloudflare (associates with web-hosting skills), web (ties to frontend-dev capabilities).
