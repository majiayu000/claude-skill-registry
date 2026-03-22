---
name: authy
description: "Inject secrets into subprocesses via environment variables. You never see secret values — authy run injects them directly. Use for any command that needs API keys, credentials, or tokens."
license: MIT
compatibility: Requires `authy` on PATH. Auth via AUTHY_TOKEN (run-only) + AUTHY_KEYFILE.
metadata:
  author: eric8810
  version: "0.3.0"
  homepage: https://github.com/eric8810/authy
  openclaw:
    requires:
      bins: ["authy"]
      env: ["AUTHY_KEYFILE", "AUTHY_TOKEN"]
      files: ["$AUTHY_KEYFILE"]
---

# Authy — Secure Secret Injection

Inject secrets into subprocesses as environment variables. You never see, handle, or log secret values.

## How It Works

Your token is run-only. You can discover secret **names** with `authy list` and inject them into subprocesses with `authy run`. You never see secret values directly.

## Inject Secrets into a Command

```bash
authy run --scope <policy> --uppercase --replace-dash '_' -- <command> [args...]
```

The `--uppercase --replace-dash '_'` flags turn secret names like `db-host` into env vars like `DB_HOST`.

Examples:
```bash
authy run --scope deploy --uppercase --replace-dash '_' -- ./deploy.sh
authy run --scope backend --uppercase --replace-dash '_' -- node server.js
authy run --scope testing --uppercase --replace-dash '_' -- pytest
```

## Discover Secret Names

```bash
authy list --scope <policy> --json
```

Output: `{"secrets":[{"name":"db-host","version":1,...}]}`

## Write Scripts That Use Secrets

Write code that reads environment variables, then run it with `authy run`:

```bash
cat > task.sh << 'EOF'
#!/bin/bash
curl -H "Authorization: Bearer $API_KEY" https://api.example.com/data
EOF
chmod +x task.sh
authy run --scope my-scope --uppercase --replace-dash '_' -- ./task.sh
```

## Error Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 2 | Auth failed — check AUTHY_TOKEN / AUTHY_KEYFILE |
| 3 | Secret or policy not found |
| 4 | Access denied or run-only restriction |
| 6 | Token invalid, expired, or revoked |

## Rules

1. **Only use `authy run` and `authy list`** — these are the only commands available to you
2. **Never hardcode credentials** — reference env vars, run via `authy run`
3. **Never echo, print, or log env vars** in subprocess scripts — secrets exist in memory only
4. **Never redirect env vars to files** — do not write `$SECRET` to disk
5. **Use `--scope`** to limit access to needed secrets only
