---
name: fullstack-dev
description: Use when developing the frontend and backend together, making UI changes, or setting up local dev with linked inspect_ai/scout libraries. Triggers on frontend changes, "yarn dev", "vite", "www/", or React component work.
---

# Frontend application

We have a frontend React app in www/. It is pretty lightweight for the moment. It has some views to list eval sets, scans, and samples, from the data warehouse DB.

It embeds the inspect_ai and inspect_scout frontend components.

If you want to make changes to inspect_ai and inspect_scout, you can link them to this project.

Inspect_ai uses yarn and inspect_scout uses pnpm.

It's perfectly okay to make changes to inspect_ai and inspect_scout. We can contribute changes upstream.

## Running the backend

You should have an env file that corresponds to the environment you're using.

E.g.

```
set -a ; source env/dev3; set +a ; uv run fastapi dev hawk/api/server.py --port 8080
```

## Running the frontend

**Requires Node.js ≥22.12.0** (CI uses 22.21.1). Check with `node --version`. Use `nvm` to install if needed:

```bash
nvm install 22
nvm use 22
```

```
cd www
# optional
yarn link "@meridianlabs/log-viewer"
yarn dev
```

## Running dependencies

```
cd ~/dev/inspect_ai/src/inspect_ai/_view/www
yarn link -g
yarn dev:lib
```

Scout is a little trickier because it uses pnpm not yarn.
