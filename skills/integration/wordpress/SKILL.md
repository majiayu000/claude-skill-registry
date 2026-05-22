---
name: wordpress
description: OpenClaw skill that provides a WordPress REST API CLI for posts, pages, categories, tags, users, and custom requests using plain HTTP.
---

# WordPress REST API Skill (Advanced)

## Purpose
Provide a production-ready CLI for WordPress REST API automation. This skill focuses on content workflows (posts/pages), taxonomy (categories/tags), user reads, and safe custom requests without external HTTP libraries.

## Best fit
- You want a stable CLI for automation and bot workflows.
- You need JSON-in/JSON-out for pipelines.
- You prefer simple HTTP with no extra dependencies.

## Not a fit
- You must handle OAuth flows or complex browser-based auth.
- You need advanced media uploads (multipart streaming).

## Requirements
- Node.js 18+ (for native `fetch`).

## One-time setup
1. Enable the WordPress REST API (default in modern WordPress).
2. Create an Application Password for a WordPress user.
3. Confirm the user has the right role (e.g., Editor/Admin).

## Install
```bash
cd wordpress
npm install
```

## Run
```bash
node scripts/wp-cli.js help
node scripts/wp-cli.js posts:list --query per_page=5
node scripts/wp-cli.js posts:create '@post.json'
```

You can also use npm:
```bash
npm run wp -- posts:list --query per_page=5
```

## Credentials
Supported options (first match wins):
- Basic auth token: `WP_BASIC_TOKEN` (base64 of `user:app_password`)
- User + app password: `WP_USER` + `WP_APP_PASSWORD`
- JWT bearer token: `WP_JWT_TOKEN`

## Required env
- `WP_BASE_URL` (e.g., `https://example.com`)

## Input conventions
- JSON can be inline or loaded from file with `@path`.
- Query params use `--query key=value` (repeatable) or `--query key1=value1,key2=value2`.

## Command map (high level)
Posts:
- `posts:list`, `posts:get`, `posts:create`, `posts:update`, `posts:delete`

Pages:
- `pages:list`, `pages:get`, `pages:create`, `pages:update`, `pages:delete`

Taxonomy:
- `categories:list`, `categories:create`
- `tags:list`, `tags:create`

Users:
- `users:list`, `users:get`

Advanced:
- `request` (raw method + path)

## Operational guidance
- Prefer `context=view` for read-only list calls.
- Use `status=draft` when staging content.
- Implement retries for `429` and transient `5xx` errors in orchestrators.

## Expected output
- JSON to stdout; non-zero exit code on errors.

## Security notes
- Never log or commit tokens or application passwords.
- Use a dedicated low-privilege WordPress account where possible.
