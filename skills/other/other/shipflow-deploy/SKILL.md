---
name: shipflow-deploy
description: Full deploy cycle — check, ship, restart, verify. Supports PM2, push-triggered (Vercel/Netlify), and static deploys.
disable-model-invocation: true
argument-hint: [optional: "skip-check"]
---

## Context

- Current directory: !`pwd`
- Project CLAUDE.md: !`head -80 CLAUDE.md 2>/dev/null || echo "no CLAUDE.md"`
- Package.json scripts: !`cat package.json 2>/dev/null | grep -E '^\s+"(dev|build|start|deploy|preview)"' || echo "no package.json"`
- PM2 ecosystem: !`cat ecosystem.config.cjs 2>/dev/null | head -30 || echo "no ecosystem.config.cjs"`
- Git status: !`git status --short 2>/dev/null | head -10 || echo "no git"`
- Current branch: !`git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown"`
- Remote: !`git remote -v 2>/dev/null | head -2 || echo "no remote"`
- Deploy config: !`ls -1 vercel.json netlify.toml fly.toml Dockerfile 2>/dev/null || echo "no deploy config"`

## Workspace root detection

If the current directory has no project markers (no `package.json`, no `requirements.txt`, no `src/` dir, no `lib.sh`) BUT contains multiple project subdirectories — you are at the **workspace root**.

Use **AskUserQuestion**:
- Question: "Which project should I deploy?"
- `multiSelect: false`
- One option per project from `/home/claude/shipflow_data/PROJECTS.md`

Then `cd` to that project and continue.

---

## Flow

### Step 1: Pre-deploy checks

**Skip this step if `$ARGUMENTS` is "skip-check".**

Run the same checks as `/shipflow-check` (typecheck, lint, build):
1. Detect project type from context.
2. Run typecheck → lint → build sequentially.
3. If any check fails: **STOP**. Report the failure and suggest running `/shipflow-check` to fix.

### Step 2: Ship

Run the same logic as `/shipflow-ship`:
1. `git add` changed files.
2. Generate commit message from staged changes.
3. `git commit` and `git push`.

If there are no changes to commit, skip this step (code is already pushed).

### Step 3: Detect deploy method and execute

Detect how this project is deployed:

**PM2** (has `ecosystem.config.cjs`):
```bash
pm2 reload ecosystem.config.cjs    # Zero-downtime reload
# or
pm2 restart ecosystem.config.cjs   # Full restart if reload not supported
```

**Push-triggered** (Vercel, Netlify, Cloudflare Pages):
- Deployment is automatic on push. Just confirm the push was successful.
- Check deploy status if CLI available: `vercel ls --limit 1` or `netlify status`

**Static** (no server process, built files served by Caddy/nginx):
- Build was already done in Step 1. Files are ready.
- If served by Caddy: no restart needed (files are served directly).

**Manual** (no detected deploy method):
- Report: "No deploy method detected. Build is ready at [dist/build/.next]."
- Suggest setting up deployment.

### Step 4: Health check

After deploy:
```bash
# Get the deploy URL from ecosystem.config.cjs, CLAUDE.md, or ask
curl -s -o /dev/null -w "%{http_code}" [deploy-url] --max-time 5
```

- **200-299**: Deploy successful
- **3xx**: Redirect (check target)
- **4xx/5xx**: Deploy may have failed
- **Timeout**: Server not responding

Retry up to 3 times with 5-second intervals if the first check fails (server may be restarting).

### Step 5: Report

```
DEPLOY: [project name]
═══════════════════════════════
Pre-checks     [✓/✗/skipped]
  Typecheck    [✓/✗]
  Lint         [✓/✗]
  Build        [✓/✗]
Ship           [✓/skipped — no changes]
  Commit       [hash]
  Push         [branch → remote]
Deploy         [✓/✗]
  Method       [PM2/Vercel/Netlify/Static/Manual]
Health check   [✓/✗/skipped]
  URL          [deploy-url]
  Status       [200/timeout/error]
═══════════════════════════════
```

### Step 6: Update tracking

Add a deploy note to the project's section in `/home/claude/shipflow_data/TASKS.md`:
```
- [x] Deploy [date] — [commit hash] — [status]
```

---

## Important

- **Never deploy without checks** unless explicitly skipped with "skip-check" argument.
- If build fails, STOP immediately. Don't push broken code.
- For PM2 deploys, always use `reload` first (zero-downtime), fall back to `restart` if reload fails.
- The health check URL should come from project config, not be guessed.
- Log every deploy attempt (success or failure) to TASKS.md.
- If deploying to production, confirm with the user first.
