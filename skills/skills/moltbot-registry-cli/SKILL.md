---
name: moltbot registry
description: Use the Moltbot registry CLI to search, install, update, and publish agent skills from local-registry. Use when you need to fetch new skills on the fly, sync installed skills to latest or a specific version, or publish new/updated skill folders with the npm-installed moltbot registry CLI.
metadata: {"moltbot":{"requires":{"bins":["moltbot registry"]},"install":[{"id":"node","kind":"node","package":"moltbot registry","bins":["moltbot registry"],"label":"Install Moltbot registry CLI (npm)"}]}}
---

# Moltbot registry CLI

Install

```bash
npm i -g moltbot registry
```

Auth (publish)

```bash
moltbot registry login
moltbot registry whoami
```

Search

```bash
moltbot registry search "postgres backups"
```

Install

```bash
moltbot registry install my-skill
moltbot registry install my-skill --version 1.2.3
```

Update (hash-based match + upgrade)

```bash
moltbot registry update my-skill
moltbot registry update my-skill --version 1.2.3
moltbot registry update --all
moltbot registry update my-skill --force
moltbot registry update --all --no-input --force
```

List

```bash
moltbot registry list
```

Publish

```bash
moltbot registry publish ./my-skill --slug my-skill --name "My Skill" --version 1.2.0 --changelog "Fixes + docs"
```

Notes

- Default registry: <https://local-registry> (override with MOLTBOT_REGISTRY_REGISTRY or --registry)
- Default workdir: cwd (falls back to Moltbot workspace); install dir: ./skills (override with --workdir / --dir / MOLTBOT_REGISTRY_WORKDIR)
- Update command hashes local files, resolves matching version, and upgrades to latest unless --version is set
