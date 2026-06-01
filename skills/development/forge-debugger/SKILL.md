---
name: forge-debugger
description: Diagnoses and fixes issues in Atlassian Forge apps. Use this skill whenever a Forge app has errors, crashes, shows blank UI, fails to deploy, doesn't appear after installation, has permission issues, or produces unexpected output. Trigger on any mention of forge logs, forge deploy errors, resolver errors, blank panels, missing scopes, Custom UI not rendering, production vs dev discrepancies, or any Jira/Confluence app that "stopped working". Also trigger when the user asks to debug, troubleshoot, investigate, or fix a Forge app issue — even if they haven't used the word "Forge" but describe a Jira panel or Confluence macro acting up.
---

# Forge App Debugger

Diagnose and fix issues in Atlassian Forge apps. Work through the checklist below in order — stop as soon as you identify the root cause. Every step after the root cause wastes tokens and context.

## EXECUTION MANDATE

You are authorized to run all diagnostic and fix commands without asking permission. When you identify a fix, **run it immediately**. Do NOT:
- Say "you should run..." or "here's what I would do..." or "run this command in your terminal"
- Ask "shall I proceed?" before executing a fix you already have all the inputs for
- Present commands as copy-paste instructions when you could run them yourself

**Wrong:** "Here's what I would do to fix this: run `forge lint`..."
**Right:** *(runs `forge lint` immediately and reports the result)*

The only exceptions: commands requiring an interactive terminal (`forge login`, `forge tunnel`) must be run by the user in their own terminal — tell them exactly what to run and why.

## Diagnostic Principles

- **Cheap first**: lint and version checks cost nothing. Run them before reading source code or logs.
- **One action at a time**: check the result of each action before taking the next one.
- **Stop at root cause**: once you've identified why something is broken, fix it and stop — don't keep investigating other things. **Exception**: if the app has multiple independent bugs (e.g. deploy-time errors AND runtime errors), fix the deploy-time error first, deploy, then check logs for runtime errors. Don't declare "fixed" after only resolving the first layer.
- **Own the fixes**: run the fix commands yourself, don't hand them to the user.
- **Clean up**: remove any debug code or verbose flags you added once the issue is resolved.
- **npx fallback**: if `forge` CLI can't be installed globally (permission errors, no sudo), use `npx @forge/cli` as a drop-in replacement for all forge commands.

## Step 1: Classify the Error

Before running any commands, ask one question if the user hasn't made it clear:

> "Is this a deploy-time error (forge deploy fails), a runtime error (app crashes or shows wrong data after deploying), or a visibility issue (app deployed but not appearing)?"

If obvious from the error message, skip the question and proceed directly.

**Quick routing:**

| Symptom | Go to |
|---------|-------|
| `forge deploy` fails | Step 2 → 3 → 4 |
| App not visible after install | Step 3 → common error: "App not installed" |
| App crashes / resolver error | Step 3 → 5 → 6 |
| Blank UI / Custom UI not rendering | Step 3 → 4 → common error: "blank Custom UI" |
| Works in dev, fails in prod | Step 7 (Production) |
| Permission denied / 403 | Common error: "Permission denied" |
| 410 Gone / deprecated endpoint | Common error: "410 Gone" → API Migration section |
| Handler path lint error | Common error: "cannot find associated file" → Handler Path Resolution section |
| Resolver returns undefined, no errors | Common error: invoke name mismatch → Invoke Name vs Function Key section |
| Multiple failures (deploy + runtime) | Fix deploy errors first, deploy, then check logs for runtime errors |

## Step 2: Version Check

```bash
forge --version
npm show @forge/cli version
```

If the installed version is behind the latest major version, upgrade immediately:

```bash
npm install -g @forge/cli
```

Then retry the failing operation. Many bugs are fixed in newer CLI versions.

## Step 3: Lint

```bash
forge lint
```

Fix every error before proceeding — lint errors cause deploy failures and silent runtime bugs. If lint passes cleanly, continue to the next step.

**For any manifest-related error message** (e.g. "invalid manifest", "unexpected key", "modules.jira:*" errors): run `forge lint` first before reading any source files. Lint will identify the exact line and field causing the problem — reading the file before linting is wasteful and usually less informative than the lint output.

## Step 4: Custom UI Build Check

Only applies when the app has a `static/` directory (Custom UI apps). Check if the frontend was built before the last deploy:

```bash
ls -la static/build/
```

If the build directory is missing or older than recent source changes, rebuild:

```bash
cd static && npm run build && cd ..
```

Then redeploy:

```bash
forge deploy -e development
```

This is one of the most common causes of blank UI panels.

## Step 5: Deploy Status

Verify the app was actually deployed successfully:

```bash
forge deploy -e development --verbose
```

Watch for errors in the output. Note the deploy timestamp. If deploy fails, the error message usually identifies the problem directly — match it against the Common Error Patterns table below.

## Step 6: Logs

```bash
forge logs -e development --limit 100
```

Read the logs carefully. Most runtime errors appear here.

### If no logs are returned

The resolver may not have been triggered, or logging isn't set up. Add a debug log at the entry point of the resolver:

```javascript
// Add at the top of your handler function:
console.error('[DEBUG] Handler called with:', JSON.stringify(payload));
```

Then redeploy and trigger the app again:

```bash
forge deploy -e development
forge logs -e development --limit 100
```

Remove the debug log after you've identified the issue.

### If the error is in the frontend (UI rendering, blank screen)

Forge UI Kit errors surface in `forge logs`, not the browser console. For Custom UI, add error logging in the resolver that backs the UI:

```javascript
try {
  const result = await api.asUser().requestJira(/* ... */);
  return result;
} catch (err) {
  console.error('[DEBUG] Resolver error:', err.message, err.stack);
  throw err;
}
```

Redeploy, trigger, and check logs.

## Step 7: Production Issues

If the user reports an issue that only happens in production (or on a specific customer's site):

1. Ask: "Which Atlassian site is affected? (e.g. `customername.atlassian.net`)"
2. Check production logs:
   ```bash
   forge logs -e production --site <customer-site> --limit 100
   ```
3. Note: production logs may be delayed up to 2 minutes after the event.
4. If the issue is permission-related, check whether scopes were upgraded after a new install — production installs require explicit `--upgrade`.

## Common Error Patterns

Match the error against this table first. If you find a match, apply the fix directly without further investigation.

| Error / Symptom | Root Cause | Fix |
|-----------------|-----------|-----|
| "App is not installed on this site" | `forge install` wasn't run, or ran against wrong site | Ask for the Atlassian site URL if not already known, then run it yourself: `forge install --non-interactive --site <url> --product <jira\|confluence> -e development` |
| Blank panel / Custom UI white screen | Frontend build not run before deploy | `cd static && npm run build && cd .. && forge deploy -e development` |
| "Resolver not found" or resolver returns undefined | Function key in manifest.yml doesn't match resolver registration | Check `manifest.yml` `function.key` matches the key used in `resolver.define('key', ...)` |
| 403 / "Permission denied" / "Unauthorized" | OAuth scope missing from manifest | Add scope to `manifest.yml`, then: `forge deploy -e development && forge install --non-interactive --site <url> --upgrade` |
| `forge deploy` fails with "Invalid manifest" | YAML syntax error in manifest.yml | Run `forge lint`, fix indentation/syntax errors |
| App deployed but module not visible | Wrong product in `forge install`, or tunnel not active | Verify `--product` flag matches app type; restart tunnel if using `forge tunnel` |
| "forge: command not found" | CLI not installed | `npm install -g @forge/cli` |
| `ENOENT` or missing files on deploy | `npm install` not run in app directory | `cd <app-dir> && npm install && forge deploy -e development` |
| "Rate limit exceeded" | Too many API calls in resolver | Add exponential backoff; check for resolver being called in a loop |
| "App tunnel disconnected" | `forge tunnel` connection dropped | Re-run `forge tunnel`; check VPN isn't blocking websocket connections |
| "Cannot read properties of undefined" | API response shape unexpected | Log the full API response; add null checks |
| 410 Gone / "deprecated endpoint has been removed" | Confluence/Jira REST API endpoint removed | Migrate to v2 API (see API Migration section below). Redeploy and check logs |
| `cannot find associated file` (handler path lint error) | Handler path in manifest.yml doesn't match actual file location | Handler path is relative to `src/`. E.g. if resolver is at `src/resolvers/index.js`, handler is `resolvers/index.handler` (not `index.handler` or `src/resolvers/index.handler`). See Handler Path Resolution below |
| `invoke()` returns undefined, no errors in logs | Frontend `invoke('name')` doesn't match `resolver.define('name')` | The invoke name must exactly match the resolver.define name. Check both files — this is a different check than function key in manifest |
| `Module not found` / doubled path like `src/src/...` on deploy | Handler path includes `src/` prefix, but bundler already resolves from `src/` | Remove `src/` prefix from handler path. Use `resolvers/index.handler` not `src/resolvers/index.handler` |
| `npm install -g` permission error / cannot install forge globally | No sudo or write access to global npm directory | Use `npx @forge/cli` as a drop-in replacement for all `forge` commands (lint, deploy, logs, install). No global install needed |

## Handler Path Resolution

The `handler` field in `manifest.yml` has the format `<path>.<export>`, where:
- `<path>` is the file path **relative to `src/`** (without `src/` prefix, without file extension)
- `<export>` is the named export from that file

**Examples:**

| Resolver file location | Export in file | Correct handler value |
|------------------------|---------------|----------------------|
| `src/resolvers/index.js` | `export const handler = ...` | `resolvers/index.handler` |
| `src/index.js` | `export const handler = ...` | `index.handler` |
| `src/backend/resolver.ts` | `export const run = ...` | `backend/resolver.run` |

**Common mistakes:**
- `index.handler` — wrong if the file is in a subdirectory like `src/resolvers/`
- `src/resolvers/index.handler` — wrong: bundler prefixes `src/` automatically, resulting in `src/src/resolvers/...`
- `resolvers/index.run` — wrong if the file exports `handler` not `run`

**Diagnostic trick:** If `forge lint` reports "cannot find associated file" but you're sure the file exists, try `forge deploy --no-verify`. The bundler error message shows the fully resolved path, which reveals whether the path is being doubled or misresolved.

## Invoke Name vs Function Key

There are **two separate name-matching requirements** for UI Kit resolvers:

1. **manifest.yml `function.key`** must match the `resolver: function:` reference in the module definition
2. **Frontend `invoke('name')`** must exactly match **`resolver.define('name', ...)`** in the backend

These are independent — you can have the manifest function key correct but still get undefined results if the invoke name doesn't match resolver.define. When debugging "resolver returns undefined" with no errors in logs, always check **both** matching relationships.

## API Migration (v1 → v2)

Atlassian is progressively deprecating v1 REST API endpoints. When you see a **410 Gone** response:

1. Check `forge logs` for the exact error — it will show which endpoint returned 410
2. Identify the v2 equivalent:
   - **URL pattern**: `/wiki/rest/api/content/...` → `/wiki/api/v2/pages/...` (or `/blogposts/...`, `/spaces/...`)
   - **Jira**: `/rest/api/2/...` → `/rest/api/3/...`
3. Update **pagination**: v2 Confluence APIs use **cursor-based** pagination (`cursor` parameter) instead of offset-based (`start` parameter). The next cursor is in `data._links.next`
4. Update **response shape**: v2 may return different field names (e.g. `authorId` instead of nested `by.accountId`)
5. Redeploy and check logs to confirm the fix

**Do NOT** treat 410 as a permissions issue — it means the endpoint no longer exists, not that access is denied.

## Step 8: Cleanup

Once the issue is resolved:

1. Remove any `console.error('[DEBUG] ...')` statements you added.
2. Remove verbose flags from any scripts.
3. Run `forge lint` one final time to confirm clean state.
4. Redeploy if you modified code during debugging:
   ```bash
   forge deploy -e development
   ```
5. Confirm the fix works by triggering the app and checking that `forge logs` shows no new errors.

## Escalation

If none of the above resolves the issue:

- Run `forge logs -e development --verbose --limit 200` for extended output.
- Check the Forge changelog for known issues: `search-forge-docs "known issues <error-text>"`
- If the error is in a Forge platform API (not your code), note the `traceId` from the log output — this is what Atlassian support needs.

## Authentication Errors

If any command fails with "not authenticated" or "run forge login":

1. Tell the user to create an API token at **https://id.atlassian.com/manage/api-tokens**
2. Tell them to run `forge login` in **their own terminal** (not via the agent) — it will prompt for their email and the API token
3. Example message: *"You need to log in. Create an API token at https://id.atlassian.com/manage/api-tokens, then run `forge login` in your terminal. Enter your Atlassian email and the token when prompted — do not paste the token here."*
4. After they confirm login, resume debugging from where you left off.

## Token Efficiency Rules

Follow these to keep context usage low:

- Read `forge logs` before reading any source file — logs usually reveal the root cause without needing to inspect code.
- Read only the specific file implicated by the error. Match the error to its file:
  - `npm ERR! missing script: build` → check only `package.json` (scripts section)
  - `invalid manifest` / `unexpected key` → run `forge lint` first, then only the specific manifest field
  - `Resolver not found` → check only the function key in `manifest.yml` vs `resolver.define()` in the resolver file
  - `403 / permission denied` → check only the scopes in `manifest.yml`
  - `410 Gone` → check the API endpoint URL in the resolver file; don't check scopes or manifest
  - `cannot find associated file` → check the handler path in `manifest.yml` and the file location; use `--no-verify` to see the bundler's resolved path
  - `invoke()` returns undefined → check both the frontend `invoke('name')` AND backend `resolver.define('name')` — two files, but targeted reads
- Don't read `manifest.yml` for npm/build errors — they are unrelated.
- Don't re-read a file you've already read in this session unless it changed.
- Stop the diagnostic chain the moment you find a match in the Common Error Patterns table. **Exception**: when multiple independent bugs exist (e.g. deploy error + runtime error), fix the first, deploy, then check for the next.
- Don't run `forge deploy` more than once per fix attempt without a clear reason.
- Use `forge deploy --no-verify` as a **diagnostic step** when lint blocks deploy but you suspect the lint error may be misleading. The bundler error message often reveals the true path resolution issue. Always fix the root cause afterward — don't ship with `--no-verify`.
