---
name: apps-script
description: >
  Google Apps Script development workflow and best practices. Use when writing,
  reviewing, debugging, or deploying Apps Script code — including container-bound
  scripts (Sheets, Docs, Forms, Slides), standalone scripts, web apps, add-ons,
  and API executables. Triggers on: "Apps Script", "google script", ".gs files",
  "clasp", "appsscript.json", "SpreadsheetApp", "DocumentApp", "GmailApp",
  "UrlFetchApp", "onOpen", "onEdit", "doGet", "doPost", "custom function",
  "Sheets automation", "Google Workspace automation", "bound script",
  "time-driven trigger", "installable trigger", "Apps Script deployment",
  "Apps Script add-on", "HtmlService sidebar", "script properties",
  "journal entry", "trial balance", "bank reconciliation", "aging report",
  "chart of accounts", "period close", "invoice generator", "accounting spreadsheet",
  "timesheet", "billable hours", "utilization", "retainer", "project profitability",
  "rate card", "expense allocation", "consultancy billing", "invoice from timesheets".
---

# /apps-script — Google Apps Script Development

## Core Workflow

### 1. Orient — Understand the Project

Before writing any code, determine:

- **Project type**: standalone, container-bound (Sheets/Docs/Forms/Slides), web app, add-on, or API executable
- **Manifest**: Read `appsscript.json` — check runtime version, scopes, dependencies, time zone
- **clasp config**: Read `.clasp.json` — check `scriptId`, `rootDir`
- **Existing triggers**: Note any `onOpen`, `onEdit`, time-driven, or installable triggers
- **Quotas at risk**: If the task involves bulk operations, email, or URL fetches, check quotas early

### 2. Develop — Write Correct, Performant Code

**Read `references/performance.md` before writing any Sheets/data-heavy code.**

Key rules (always apply):

- **Batch reads/writes**: Never call `getValue()`/`setValue()` in a loop. Use `getValues()`/`setValues()` on full ranges. This is the single biggest performance difference (~70x).
- **Minimize service calls**: Pure JS array operations are orders of magnitude faster than Google service calls. Read all data into arrays, process in memory, write back once.
- **Cache expensive fetches**: Use `CacheService` for external API responses (up to 6hr TTL, 100KB per entry).
- **Handle timeouts**: Scripts have a 6-minute hard limit (30 seconds for simple triggers and custom functions). For long tasks, use the continuation pattern with `PropertiesService` + time-driven triggers. See `references/common-patterns.md § Continuation Pattern`.
- **Use `fetchAll()`**: When making multiple HTTP requests, `UrlFetchApp.fetchAll()` runs them in parallel.
- **Avoid libraries in UI-heavy scripts**: Each library call is a remote invocation adding latency.

### 3. Secure — Protect Scopes, Secrets, and Input

**Read `references/scopes-and-security.md` before modifying `appsscript.json` or handling user input.**

Key rules (always apply):

- **Never hardcode secrets**. Use `PropertiesService.getScriptProperties()` for API keys, tokens, credentials.
- **Narrowest scopes**: Use `spreadsheets.readonly` not `spreadsheets` if you only read. Use `drive.file` not `drive` if you only access files the app created. Always prefer the most restrictive scope that works.
- **Do not widen scopes** in `appsscript.json` unless the feature truly requires it. Explain scope changes to the user.
- **Validate all input** in `doGet(e)`/`doPost(e)` — parameters, postData, content types.
- **No `eval()`** or dynamic code construction from untrusted input.
- **Use `LockService`** when multiple users/triggers may write to the same resource concurrently.

### 4. Test — Validate Before Pushing

- Use the head deployment (`/dev` URL) for web apps
- Test simple triggers by actually opening/editing the document
- For installable triggers, remember they run under the **creator's** account
- Check `Logger.log()` output in the editor execution log during development
- Use `console.log()` for production logging (goes to Cloud Logging)
- Verify quotas won't be exceeded: `MailApp.getRemainingDailyQuota()`, check execution dashboard

### 5. Deploy — Push and Release Safely

**Read `references/clasp-workflow.md` for the full command reference.**

Key rules (always apply):

- **Never push or deploy without explicit user instruction.** Always confirm before `clasp push` (overwrites remote) or `clasp deploy`.
- **Always `clasp pull` first** if the user may have edited in the browser editor — `clasp push` overwrites remote files completely.
- **Version before deploying**: `clasp version "description"` then `clasp deploy --versionNumber N`
- **Share `/exec` URLs** (versioned), never `/dev` URLs (head deployment, for testing only).
- **Validate manifest before push**: Check `appsscript.json` for scope correctness, timezone, dependencies.

---

## Project Type Quick Reference

| Type | Created Via | Special Capabilities |
|------|------------|---------------------|
| **Standalone** | script.google.com or `clasp create` | Appears in Drive; web apps; API executables |
| **Container-bound** | Extensions > Apps Script in Sheets/Docs/Forms/Slides | `getActiveSpreadsheet()`, `getUi()`, custom menus, dialogs, sidebars, simple triggers, custom functions |
| **Web App** | Any script with `doGet(e)`/`doPost(e)` | Served at URL; execute as owner or user |
| **Add-on** | Published to Marketplace | Editor or Workspace add-ons; requires OAuth verification |
| **API Executable** | Exposed via Apps Script API | Called externally via REST; requires OAuth |

---

## Trigger Rules

**Read `references/triggers-and-quotas.md` for full details.**

| | Simple Triggers | Installable Triggers |
|---|----------------|---------------------|
| Setup | Reserved function name (`onOpen`, `onEdit`) | Created via UI or `ScriptApp.newTrigger()` |
| Auth services | NO (cannot call Gmail, Drive, UrlFetch, etc.) | YES |
| Max runtime | 30 seconds | 6 minutes |
| Runs as | Current user | Trigger creator |
| Max per script | N/A | 20 per user per script |
| Time-driven | NO | YES |

**Common pitfall**: Writing an `onEdit` that calls `UrlFetchApp` — this silently fails because simple triggers cannot use authorized services. Use an installable trigger instead.

---

## Common Services

| Service | When to Use |
|---------|------------|
| `SpreadsheetApp` | Read/write spreadsheet data |
| `DocumentApp` | Create/edit Google Docs |
| `SlidesApp` | Create/edit Google Slides |
| `FormApp` | Create/edit Google Forms |
| `DriveApp` | File management in Drive |
| `GmailApp` / `MailApp` | Send/read email (`MailApp` for simple sends, `GmailApp` for full access) |
| `UrlFetchApp` | HTTP requests to external APIs |
| `PropertiesService` | Persistent key-value storage (secrets, config, state) |
| `CacheService` | Temporary cache (max 6hr TTL, 100KB/entry) |
| `LockService` | Prevent concurrent write conflicts |
| `HtmlService` | Web app pages, dialogs, sidebars |
| `CalendarApp` | Calendar event management |
| `ContactsApp` | Contact management |

---

## Anti-Patterns to Flag

When reviewing or writing Apps Script code, flag these:

1. **Cell-by-cell reads/writes** — `getValue()`/`setValue()` inside loops
2. **Hardcoded secrets** — API keys, tokens, passwords in source code
3. **Missing error handling on `UrlFetchApp`** — always use `muteHttpExceptions: true` and check response codes
4. **Overly broad scopes** — `https://www.googleapis.com/auth/drive` when `drive.file` suffices
5. **Simple trigger doing authorized work** — `onEdit` calling `UrlFetchApp` or `GmailApp`
6. **No timeout handling** — long loops without chunking or time checks
7. **Missing `LockService`** — concurrent writes to shared resources (PropertiesService, Sheets)
8. **`eval()` or dynamic code** from user input
9. **Infinite trigger loops** — `onEdit` handler that writes to the sheet, re-triggering itself
10. **Using `/dev` URL in production** — always use versioned `/exec` deployments

---

## Reference Files

Load these as needed — do not load all at once:

- `references/performance.md` — Batch patterns, caching, timeout handling, optimization
- `references/triggers-and-quotas.md` — Trigger types, quota tables, runtime limits
- `references/scopes-and-security.md` — OAuth scopes, secret management, input validation, web app security
- `references/clasp-workflow.md` — clasp commands, project setup, deployment workflow
- `references/common-patterns.md` — Read-process-write, custom menus, dialogs, continuation, retry patterns
- `references/accountancy-patterns.md` — Journal entries, trial balance, bank reconciliation, AR aging, period locking, invoice numbering, tax helpers, multi-currency
- `references/consultancy-billing-patterns.md` — Timesheet-to-invoice pipeline, utilization tracking, project profitability, retainer management, rate cards, expense allocation, payment tracking
