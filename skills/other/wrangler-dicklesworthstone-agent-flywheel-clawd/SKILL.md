---
name: wrangler
description: "Deploy and manage Cloudflare Workers, Pages, KV, R2, D1, and other Cloudflare services using the `wrangler` CLI."
---

# Wrangler Skill

Use the `wrangler` CLI to manage Cloudflare Workers and related services.

## Workers

List deployed workers:
```bash
wrangler deployments list
```

Deploy a worker:
```bash
wrangler deploy
```

Tail live logs from a worker:
```bash
wrangler tail <worker-name>
```

Run worker locally:
```bash
wrangler dev
```

## KV (Key-Value Storage)

List KV namespaces:
```bash
wrangler kv namespace list
```

List keys in a namespace:
```bash
wrangler kv key list --namespace-id <namespace-id>
```

Get a value:
```bash
wrangler kv key get <key> --namespace-id <namespace-id>
```

Put a value:
```bash
wrangler kv key put <key> <value> --namespace-id <namespace-id>
```

## R2 (Object Storage)

List R2 buckets:
```bash
wrangler r2 bucket list
```

List objects in a bucket:
```bash
wrangler r2 object list <bucket-name>
```

Upload a file:
```bash
wrangler r2 object put <bucket-name>/<key> --file <local-path>
```

## D1 (SQLite Database)

List D1 databases:
```bash
wrangler d1 list
```

Execute SQL query:
```bash
wrangler d1 execute <database-name> --command "SELECT * FROM users LIMIT 10"
```

Run migrations:
```bash
wrangler d1 migrations apply <database-name>
```

## Pages

List Pages projects:
```bash
wrangler pages project list
```

Deploy a directory to Pages:
```bash
wrangler pages deploy <directory> --project-name <project>
```

## Secrets

Set a secret:
```bash
echo "secret-value" | wrangler secret put <SECRET_NAME>
```

List secrets:
```bash
wrangler secret list
```

## Configuration

Check current authentication:
```bash
wrangler whoami
```

Login (opens browser):
```bash
wrangler login
```
