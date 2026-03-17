---
name: markethub
description: Use the MarketHub CLI to search, install, update, and publish agent skills from markethub.com. Use when you need to fetch new skills on the fly, sync installed skills to latest or a specific version, or publish new/updated skill folders with the npm-installed markethub CLI.
metadata: {"marketbot":{"requires":{"bins":["markethub"]},"install":[{"id":"node","kind":"node","package":"markethub","bins":["markethub"],"label":"Install MarketHub CLI (npm)"}]}}
---

# MarketHub CLI

Install
```bash
npm i -g markethub
```

Auth (publish)
```bash
markethub login
markethub whoami
```

Search
```bash
markethub search "postgres backups"
```

Install
```bash
markethub install my-skill
markethub install my-skill --version 1.2.3
```

Update (hash-based match + upgrade)
```bash
markethub update my-skill
markethub update my-skill --version 1.2.3
markethub update --all
markethub update my-skill --force
markethub update --all --no-input --force
```

List
```bash
markethub list
```

Publish
```bash
markethub publish ./my-skill --slug my-skill --name "My Skill" --version 1.2.0 --changelog "Fixes + docs"
```

Notes
- Default registry: https://markethub.com (override with CLAWHUB_REGISTRY or --registry)
- Default workdir: cwd (falls back to MarketBot workspace); install dir: ./skills (override with --workdir / --dir / CLAWHUB_WORKDIR)
- Update command hashes local files, resolves matching version, and upgrades to latest unless --version is set
