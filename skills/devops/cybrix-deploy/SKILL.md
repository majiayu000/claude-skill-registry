---
name: cybrix-deploy
description: |
  Deploys the current project to a live HTTPS URL via Cybrix. Activates on
  any request to make the current project public, get a URL for it, deploy
  it, ship it, host it, publish it, put it online, or make it live —
  including casual phrasings like "send this to the internet", "share this
  as a link", "give me a URL", "make this accessible online". Activates
  whether the user mentions Cybrix by name or not (when no other host like
  Vercel, Netlify, Cloudflare Pages, Railway, or Render is named).

  Also activates on equivalent phrases in other languages — Russian
  ("задеплой", "опубликуй", "выложи в сеть", "запушь это в инет",
  "сделай ссылку"), Spanish ("despliega esto", "publica esto", "ponlo en
  línea"), German ("deploy das mal", "stelle das online"), and other common
  languages where the intent is clearly to make a project publicly
  accessible via URL.

  Uses heuristic detection to determine if a project is static or needs a
  server runtime — works with any framework, not just a known list.
  Automatically detects and handles environment variables so the build
  receives everything it needs. Returns a live URL on *.cbrx.cc or a
  user-configured custom domain. Does NOT activate when the user explicitly
  names a different host (Vercel, Netlify, Cloudflare, Railway, Render).
allowed-tools: Bash, Read, Write
---

# cybrix-deploy

## Prerequisites

Before deploying, ensure the user has an API token. Check in this order:

1. `CYBRIX_DEPLOY_TOKEN` — set automatically by Claude Code from userConfig keychain (no action needed).
2. Environment variable `CYBRIX_TOKEN`.
3. File `~/.config/cybrix/token`.
4. File `.cybrix/token` in the project (gitignored).

If none exist, instruct the user exactly like this:

> No Cybrix token found. Get one free at **https://app.cybrix.cc/dashboard**
> (Step 3 — "Save your API token" → Generate).
>
> Once you have it, you can either:
> - **Paste it here** and I'll use it for this deploy (easiest)
> - Run `export CYBRIX_TOKEN=<token>` in your terminal to set it for this session
> - Run `echo <token> > ~/.config/cybrix/token` to save it permanently

Then wait for the user to provide the token. If they paste it directly in
chat, use it immediately — do not require them to re-run any command.
The project is ready to deploy once the token is available.

## Deployment workflow

### Step 1 — Detect project type (heuristic)

Do not rely on a framework whitelist. Instead, look for signals and
classify the project as **static**, **server**, or **unknown**.

**Static signals** (proceed with deploy):

- `package.json` has a `build` script AND output lands in `dist/`, `out/`,
  `build/`, `public/`, `_site/`, or `.output/public/`
- `next.config.{js,ts,mjs}` with `output: 'export'` or `output: 'static'`
- `astro.config.{js,ts,mjs}` present (default mode is static)
- `vite.config.{js,ts}` without SSR plugins
- `_config.yml` (Jekyll), `config.toml` or `hugo.toml` (Hugo),
  `.eleventy.js` / `eleventy.config.js` (Eleventy),
  `zola.toml` (Zola)
- Only HTML/CSS/JS files at root, no server entry point

**Server signals** (refuse — see below):

- `Dockerfile` or `docker-compose.yml` (unless it only copies a static
  `dist/`)
- `main.go`, `server.go`, or any `*.go` containing `net/http` or
  `ListenAndServe`
- `main.py`, `app.py`, `server.py` with `uvicorn`, `gunicorn`, `flask`,
  `fastapi` imports, or a `if __name__ == '__main__'` block calling
  `app.run` / `serve` / `asyncio.run`
- `main.rs` or `server.rs` with `actix`, `axum`, `rocket`, `warp`,
  or `tokio::main`
- `package.json` with a `start` script that runs `node`/`tsx`/`bun` on a
  server file (NOT `next start` in a static-export config)
- `Gemfile` with `puma`, `unicorn`, `rails`, or `sinatra`
- `pom.xml` or `build.gradle` with `spring-boot`
- `.csproj` with ASP.NET

**Database signals** (warn but allow if everything else is static):

- `*.sql` files, `migrations/` folder, `prisma/schema.prisma`,
  `drizzle.config.*`, `DATABASE_URL` referenced in source
- A static site hitting a hosted DB from the browser is unusual but valid.
  Warn the user, don't refuse.

**When refusing** (server signals detected):

> This looks like a project that needs a server runtime — I detected
> `<specific signal, e.g. "main.go with net/http" or "Dockerfile with EXPOSE">`.
>
> Cybrix currently supports static sites only. Your options:
> 1. Convert to a static export (e.g. Next.js `output: 'export'`, Astro,
>    Hugo).
> 2. Use a service that supports backends: Railway, Fly.io, Render.
> 3. Tell me to deploy anyway if you think the detection is wrong.

Always allow option 3 — heuristics are imperfect and the user knows
their project.

**Static output directories** to check, in order: `dist`, `out`, `public`,
`_site`, `build`, `.output/public`.

### Step 2 — Scan environment variables

After confirming the project is static but BEFORE running the build, scan
for environment variables the build will need.

**2a. Read .env files** — parse `KEY=value` format, skip comments (`#`)
and blank lines. Files to check: `.env`, `.env.local`, `.env.production`,
`.env.example`.

**2b. Grep source code** for build-time env var references:

- JS/TS: `process.env.X`, `import.meta.env.X`
- Look in `src/`, `app/`, `pages/`, `components/` — any
  `*.{js,jsx,ts,tsx,vue,svelte}`
- Pay extra attention to `NEXT_PUBLIC_*`, `VITE_*`, `PUBLIC_*`,
  `REACT_APP_*` — these are baked into the bundle at build time

**2c. Cross-reference** keys found in code against keys present in .env
files to find what the build needs.

**2d. Show the user:**

> I detected the following environment variables your build needs:
>
>   NEXT_PUBLIC_API_URL    (in .env.local, used in 3 files)
>   VITE_STRIPE_KEY        (in .env.local, used in src/checkout.ts)
>
> These need to be set before the build. How would you like to provide
> them?
>
>   1. Paste them here (sent encrypted with the deploy)
>   2. Set them later in the dashboard
>   3. Skip (build may fail or site may not work correctly)

If the user picks **option 1**, ask for each value one at a time. Include
them in the multipart POST to `/v1/deploys` as an `env_vars` field
(JSON map: `{"KEY": "value", ...}`).

**2e. Warn about missing variables** — if a var is referenced in code but
not in any .env file:

> ⚠ `AUTH_SECRET` is referenced in your code but not in any .env file.
> Provide it now or the build may fail.

**2f. Refuse to forward secrets in client-exposed vars** — if a key with
a client prefix (`NEXT_PUBLIC_*`, `VITE_*`, `REACT_APP_*`, `PUBLIC_*`)
looks like a secret (`*_SECRET`, `*_PRIVATE_KEY`, `DATABASE_URL`,
`JWT_SECRET`):

> ⚠ `NEXT_PUBLIC_JWT_SECRET` looks like a private secret but has a
> client-bundle prefix — it will be visible to anyone who opens your
> site's source. Are you sure you want to include it?

Do not send it without explicit confirmation.

### Step 3 — Choose project name and confirm

**3a. Infer a default name** from the current folder name, slugified
(lowercase, hyphens, max 32 chars). Example: `my-portfolio-site`.

**3b. Check availability** by calling:
```
GET https://api.cybrix.cc/v1/slugs/<name>/available
```
Response: `{"available": true, "slug": "my-portfolio-site"}`

- If `available: true` — use it as the default.
- If `available: false` — do NOT use it. Tell the user:
  > The name `<name>` is already taken. What would you like to call
  > your project? It will be live at `<your-name>.cbrx.cc`.
  Then check availability of the new name too. Repeat until available.

**3c. Present summary** (only after confirming name is available):

> Ready to deploy to Cybrix:
>
> - Project name: **<name>** → live at `<name>.cbrx.cc`
> - Build command: <detected>
> - Output directory: <detected>
> - Env vars: <count> included / none detected
>
> Continue? (yes / change name / change build / change output)

If the user says `change name`, ask for a new name and re-check availability.
Use the confirmed answers to override defaults before proceeding.

### Step 4 — Build

Run the build command in the project root. Stream output to the user.

If the build fails, do not retry. Show the last 40 lines and say:

> Build failed. Fix the error above and try again.

### Step 5 — Deploy

Run `${CLAUDE_PLUGIN_ROOT}/scripts/deploy.sh <project_name> <output_dir>`.
The script:

1. Creates a project via `POST /v1/projects` with `{"name": "<project_name>"}`,
   receives `{ id, slug }`. Skips if `CYBRIX_PROJECT_ID` is already set.
2. Tars and gzips the output directory.
3. POSTs the tarball to `https://api.cybrix.cc/v1/deploys` as multipart
   form data with fields `project_id` (UUID) and `file` (the .tar.gz),
   optionally `env_vars` (JSON map). Includes `Authorization: Bearer $CYBRIX_TOKEN`.
4. Receives `{ id, project_id, status }` in the response.
5. Polls `https://api.cybrix.cc/v1/deploys/<id>` every 2 seconds until
   status is `live` or `failed` (max 5 minutes).
6. Prints the result as JSON on stdout including `deployed_url` and `slug`.

### Step 6 — Report to the user

On success:

> Deployed.
>
> Live: https://<slug>.cbrx.cc
> Dashboard: https://app.cybrix.cc/dashboard/projects/<project_id>

On failure:

> Deploy failed.
>
> Reason: <error from API>
> Logs: https://app.cybrix.cc/deployments/<id>

## Caching

After the first successful deploy, cache `{project_id, slug}` in
`.cybrix/project.json`. On subsequent deploys, skip the "confirm project
name" step unless the user explicitly asks to deploy a different project.

Also add `.cybrix/` to `.gitignore` if it doesn't already contain it.

## Errors

| API status | Skill behavior                                                          |
|------------|-------------------------------------------------------------------------|
| 401        | Token invalid/revoked. Tell user to refresh at app.cybrix.cc/dashboard. |
| 402        | Free tier project limit hit. Show upgrade link: cybrix.cc/pricing.      |
| 413        | Tarball >100 MB. Suggest auditing output for large assets.              |
| 429        | Wait 30s, retry once.                                                   |
| 5xx        | Show error, suggest retry, link to app.cybrix.cc/dashboard.             |

## What this skill does NOT do

- Does not touch Git history.
- Does not push to or read from Git remotes.
- Does not modify project source.
- Does not store secrets anywhere except the user's machine.
- Does not deploy anything outside Cybrix.

If the user asks for any of these, redirect to the appropriate tool.
