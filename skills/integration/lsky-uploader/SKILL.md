---
name: lsky-uploader
description: Upload files to the self-hosted Lsky image bed (https://lsky.xueguo.us/api/v1), fetch the returned URLs/Markdown snippets, and manage albums or strategies via the REST API. Use this skill whenever you need to programmatically push screenshots/assets to Lsky and return shareable links inside Codex.
---

# Lsky Uploader

## Overview

This skill wraps the Lsky Pro API used by your self-hosted image bed. It explains how to authenticate with personal tokens, how to call `/upload`, and provides a ready-to-run Python helper (`scripts/upload_image.py`) that handles headers, multipart form-data, and prints the resulting URLs/Markdown snippets. See [references/api_overview.md](references/api_overview.md) for a condensed manual extracted from the official docs.

## Quick Start

1. **Credentials**
   - Generate a personal token inside the Lsky dashboard and copy the raw token string (without the `Bearer` prefix).
   - Default base URL is `https://lsky.xueguo.us/api/v1`. Override via the env var `LSKY_BASE_URL` or the `--base-url` flag if your deployment differs.
   - Set the token in your shell (PowerShell: `$env:LSKY_TOKEN='1|xxxx'`, bash: `export LSKY_TOKEN=1|xxxx`).
2. **Upload**
   - Run `python scripts/upload_image.py path/to/file.png`.
   - Optional flags: `--album-id`, `--strategy-id`, `--permission 0|1`, `--name custom-display-name`.
   - The script prints the direct URL, Markdown snippet, delete URL, and the full JSON payload so you can update `.lsky_upload_cache.json`.
3. **Use the links**
   - `links.url` is the canonical image URL, `links.markdown` can be pasted into blog Markdown, `links.delete_url` lets you remove the asset later.
   - If the script exits with `Lsky API error: ...`, inspect the message/HTTP status and cross-check rate limits or permissions.

## Manual Steps (without script)

When custom logic is needed, follow these HTTP patterns (details in [references/api_overview.md](references/api_overview.md)):

- **Upload** `POST /upload`: multipart form-data with `file` plus optional `album_id`, `strategy_id`, `permission`, `name`.
- **List images** `GET /images?page=1&limit=50&order=latest`: pagination response contains `data.total` and `data.data[]`, each item exposing `links`, `id`, `album_id`, etc.
- **Albums** `GET /albums`, `POST /albums`, `DELETE /albums/:id`: useful for separating assets per project.
- **Delete an image** `DELETE /images/:id`: image IDs are available via the list endpoint or the upload response (`data.image.id`).
- **Rate limiting**: watch `X-RateLimit-Remaining` and pause when it hits zero to avoid HTTP 429.

## Script Reference

`scripts/upload_image.py`

- Dependency: `requests` (install via `pip install requests` if missing).
- Environment variables:
  - `LSKY_TOKEN` (required unless you pass `--token`)
  - `LSKY_BASE_URL` (defaults to `https://lsky.xueguo.us/api/v1`)
- Exit codes:
  - `0` = success
  - Non-zero = invalid arguments or API errors (an explanatory message is printed)

For automation, capture stdout and parse the final JSON block:
```bash
python scripts/upload_image.py demo.png --token "$LSKY_TOKEN" \
  --base-url https://lsky.xueguo.us/api/v1 > upload.json
```
Then feed into `jq` or PowerShell `ConvertFrom-Json`.

## Troubleshooting

- **401 Unauthorized**: token missing/expired or header omitted.
- **403 Forbidden**: API disabled by the admin; adjust permissions server-side.
- **413 Payload too large**: respect `allow_suffixes` and `max_size` configured in Lsky.
- **429 Too Many Requests**: back off for ~60 seconds; inspect the rate-limit headers.
- **Custom TLS/Proxy**: if running behind an internal CA, call requests with `verify=False` (not recommended) or install the CA cert on the machine.

## Resources

- [references/api_overview.md](references/api_overview.md) - condensed API cheat sheet derived from <https://v1.lskypro.com/page/api-docs.html>.
- `scripts/upload_image.py` - helper script for uploads.
