---
name: capture-pr-visuals
description: Auto-capture screenshots and GIFs of the running app for PR documentation using Playwright and project context from chalk.json
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Bash, Read, Write, Glob, Grep, Edit
argument-hint: "[optional: specific routes to capture, e.g. '/home /settings', or 'all']"
read-only: false
destructive: false
idempotent: false
open-world: true
user-invocable: true
tags: git, pr, visuals
---

Capture screenshots and GIFs of the running application for PR visual documentation. Reads `chalk.json` for dev server and route info, falls back to auto-discovery if chalk docs don't exist. Uses Playwright via npx.

## Workflow

### Step 1: Read Project Context

Read `.chalk/chalk.json` to get:
- `dev.command` — how to start the dev server
- `dev.port` — what port it runs on
- `dev.url` — the full URL
- `routes[]` — what pages to capture
- `project.framework` — for framework-specific handling (e.g., Electron)

#### Fallback: No chalk.json

If `chalk.json` doesn't exist or is missing key fields, auto-discover:

1. **Read `package.json`** — detect framework from dependencies:
   - `next` → Next.js (port 3000, file-based routing)
   - `vite` / `@vitejs/plugin-react` → Vite SPA (port 5173)
   - `react-scripts` → CRA (port 3000)
   - `nuxt` → Nuxt (port 3000)
   - `@angular/core` → Angular (port 4200)
   - `svelte` / `@sveltejs/kit` → SvelteKit (port 5173)
   - `electron` / `electron-vite` → Electron (renderer on separate port)
   - `vue` → Vue (port 5173 or 8080)

2. **Detect routes** — scan based on framework:
   - **File-based routing**: glob `app/**/page.{tsx,jsx,ts,js}` or `pages/**/*.{tsx,jsx,vue}`
   - **React Router**: grep for `<Route` or `createBrowserRouter` in `src/`
   - **Vue Router**: grep for `path:` in router configs
   - **Query-param routing** (Electron): grep for `searchParams.get`
   - **Fallback**: scan `src/pages/`, `src/views/`, `src/app/`, `src/routes/`

3. **Confirm with user** — show auto-detected URL and routes, let them correct before proceeding.

If auto-discovery also fails, ask the user for the dev URL and routes. Suggest running `/setup-chalk` for future use.

### Step 2: Analyze PR Changes

```bash
git diff main..HEAD --name-only
git diff main..HEAD --stat
```

Map changed files to affected routes using `chalk.json` `routes[].src` or the architecture docs. For example:
- Changes in `src/pages/dashboard/` → `/dashboard` route
- Changes in `src/components/Header.tsx` → all pages (shared component)

If the user provided specific routes as arguments, use those instead.

If no route mapping is possible (backend-only changes), inform the user and ask which pages to capture.

### Step 3: Ensure Dev Server is Running

```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:<PORT> 2>/dev/null
```

If not running:
- Start the dev server in the background using `dev.command` from chalk.json
- Wait for it to be ready (poll until HTTP response)
- For Electron apps: the renderer is served on a separate port during dev — detect from config or output

Note the PID if starting the server so it can be stopped later.

### Step 4: Ensure Playwright is Available

```bash
npx playwright install chromium 2>/dev/null || echo "Playwright install failed"
```

Check for ffmpeg (needed for GIF generation):

```bash
which ffmpeg 2>/dev/null
```

If ffmpeg is missing, warn: "ffmpeg not found — screenshots only (no GIFs). Install with `brew install ffmpeg` for GIF support."

### Step 5: Clean Old Artifacts and Capture New Ones

First, clean any previous screenshots to ensure a fresh capture:

```bash
rm -rf .github/pr-screenshots/ 2>/dev/null
mkdir -p .github/pr-screenshots/
```

Then create a temporary capture script at `.chalk/local/capture-script.ts`:

```typescript
import { chromium } from 'playwright';
import { mkdirSync } from 'fs';
import { join } from 'path';

const BASE_URL = '<DETECTED_URL>';
const ROUTES: { path: string; name: string }[] = [
  // Populated from chalk.json routes or Step 2 analysis
];
const OUTPUT_DIR = '.github/pr-screenshots';
const VIDEO_DIR = join(OUTPUT_DIR, 'videos');

(async () => {
  mkdirSync(OUTPUT_DIR, { recursive: true });
  mkdirSync(VIDEO_DIR, { recursive: true });

  const browser = await chromium.launch({ headless: true });

  for (const route of ROUTES) {
    const context = await browser.newContext({
      viewport: { width: 1280, height: 800 },
      recordVideo: { dir: VIDEO_DIR, size: { width: 1280, height: 800 } },
    });

    const page = await context.newPage();

    try {
      await page.goto(`${BASE_URL}${route.path}`, {
        waitUntil: 'networkidle',
        timeout: 15000,
      });

      await page.screenshot({
        path: join(OUTPUT_DIR, `${route.name}.png`),
        fullPage: true,
      });

      // Brief interaction for video
      await page.evaluate(() => window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' }));
      await page.waitForTimeout(1500);
      await page.evaluate(() => window.scrollTo({ top: 0, behavior: 'smooth' }));
      await page.waitForTimeout(1500);

    } catch (err) {
      console.error(`Failed to capture ${route.name}: ${err}`);
    }

    await page.close();
    await context.close();
  }

  await browser.close();
  console.log('Capture complete.');
})();
```

Adapt the script based on the project:
- Set `BASE_URL` from chalk.json `dev.url` or detected URL
- Populate `ROUTES` from chalk.json or Step 2 analysis
- For Electron query-param routing, use paths like `?home=true`
- Add project-specific interactions if relevant

Execute:

```bash
npx tsx .chalk/local/capture-script.ts
```

### Step 6: Convert Videos to GIFs

If ffmpeg is available:

```bash
for f in .github/pr-screenshots/videos/*.webm; do
  name=$(basename "$f" .webm)
  ffmpeg -y -i "$f" -vf "fps=10,scale=1280:-1:flags=lanczos" -loop 0 ".github/pr-screenshots/${name}.gif" 2>/dev/null
done
```

Clean up videos:

```bash
rm -rf .github/pr-screenshots/videos
```

### Step 7: Commit Artifacts

Commit the new visual artifacts:

```bash
git add .github/pr-screenshots/
git commit -m "chore: add PR visual artifacts"
```

### Step 8: Output

Print markdown references for the PR body:

```markdown
## Visual Preview

### <Page Name>
![<page-name> screenshot](/.github/pr-screenshots/<page-name>.png)
![<page-name> interaction](/.github/pr-screenshots/<page-name>.gif)
```

Suggest: "Visual artifacts committed. Run `/create-pr` to create the PR with embedded screenshots."

### Step 9: Cleanup

- Delete the temporary capture script: `rm -f .chalk/local/capture-script.ts`
- If the dev server was started by this skill, ask the user if they want to stop it

## Rules

- NEVER modify `package.json` or install permanent dependencies
- Always use `npx` for Playwright and tsx
- Clean previous screenshots before capturing new ones
- If capture fails for a route, log a warning but continue with other routes
- The capture script is ephemeral — delete it after execution
- Screenshots go in `.github/pr-screenshots/` (committed to the branch)
- For auth-gated pages, warn the user those pages may need manual screenshots

## Electron App Handling

If `chalk.json` has `project.framework: "electron"` or `package.json` has `electron` as a dependency:
- The renderer is served on a separate port during dev (auto-assigned by Vite)
- Check the dev server output or config for the renderer URL
- Use that renderer URL as `BASE_URL` (not the Electron window)
- Electron query-param routing (e.g., `?home=true`, `?canvas`) should be used as route paths
