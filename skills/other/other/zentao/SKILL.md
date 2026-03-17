---
name: zentao
description: Use the zentao CLI to login and query ZenTao products and bugs. ZENTAO_URL usually includes /zentao.
homepage: https://www.npmjs.com/package/@leeguoo/zentao-mcp
metadata: {"openclaw":{"emoji":"🐞","install":[{"id":"node","kind":"node","package":"@leeguoo/zentao-mcp","bins":["zentao"],"label":"Install zentao CLI (node)"}]}}
---

# zentao (ZenTao CLI)

## When to use this skill

Use this skill when the user asks to:

- login to ZenTao via the CLI
- list products
- list bugs for a product
- view bug details
- list the user's own bugs

## Installation (recommended)

To install globally with pnpm:

```bash
pnpm i -g @leeguoo/zentao-mcp
```

If pnpm is not installed:

```bash
npm i -g pnpm
pnpm i -g @leeguoo/zentao-mcp
```

## Login workflow

1) Run login once:

```bash
zentao login \
  --zentao-url="https://zentao.example.com/zentao" \
  --zentao-account="leo" \
  --zentao-password="***"
```

2) This writes credentials to:

- `~/.config/zentao/config.toml` (or `$XDG_CONFIG_HOME/zentao/config.toml`)

3) Verify:

```bash
zentao whoami
```

IMPORTANT: `--zentao-url` usually must include `/zentao`.
If login returns HTML 404, the base path is likely missing `/zentao`.

## Commands

List products (simple by default):

```bash
zentao products list
```

List bugs for a product:

```bash
zentao bugs list --product 6
```

Get bug details:

```bash
zentao bug get --id 1329
```

List my bugs (include details):

```bash
zentao bugs mine --status active --include-details
```

Full JSON output:

- `zentao products list --json`
- `zentao bugs list --product 6 --json`
- `zentao bug get --id 1329 --json`
- `zentao bugs mine --include-details --json`
