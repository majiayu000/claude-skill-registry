---
name: google-apps-script
description: "Build Google Apps Script automation for Sheets and Workspace apps. Produces scripts with custom menus, triggers, dialogs, email automation, PDF export, and external API integration."
---

# Google Apps Script

Build automation scripts for Google Sheets and Workspace apps. Scripts run server-side on Google's infrastructure with a generous free tier.

## What You Produce

- Apps Script code pasted into Extensions > Apps Script
- Custom menus, dialogs, sidebars
- Automated triggers (on edit, time-driven, form submit)
- Email notifications, PDF exports, API integrations

## Workflow

### Step 1: Understand the Automation

Ask what the user wants automated. Common scenarios:
- Custom menu with actions (report generation, data processing)
- Auto-triggered behaviour (on edit, on form submit, scheduled)
- Sidebar app for data entry
- Email notifications from sheet data
- PDF export and distribution

### Step 2: Generate the Script

Follow the structure template below. Every script needs a header comment, configuration constants at top, and `onOpen()` for menu setup.

### Step 3: Provide Installation Instructions

All scripts install the same way:
1. Open the Google Sheet
2. **Extensions > Apps Script**
3. Delete any existing code in the editor
4. Paste the script
5. Click **Save**
6. Close the Apps Script tab
7. **Reload the spreadsheet** (onOpen runs on page load)

### Step 4: First-Time Authorisation

Each user gets a Google OAuth consent screen on first run. For unverified scripts (most internal scripts), users must click:

**Advanced > Go to [Project Name] (unsafe) > Allow**

This is a one-time step per user. Warn users about this in your output.

---

## Script Structure Template

Every script should follow this pattern:

```javascript
/**
 * [Project Name] - [Brief Description]
 *
 * [What it does, key features]
 *
 * INSTALL: Extensions > Apps Script > paste this > Save > Reload sheet
 */

// --- CONFIGURATION ---
const SOME_SETTING = 'value';

// --- MENU SETUP ---
function onOpen() {
  const ui = SpreadsheetApp.getUi();
  ui.createMenu('My Menu')
    .addItem('Do Something', 'myFunction')
    .addSeparator()
    .addSubMenu(ui.createMenu('More Options')
      .addItem('Option A', 'optionA'))
    .addToUi();
}

// --- FUNCTIONS ---
function myFunction() {
  // Implementation
}
```

---

## Critical Rules

### Public vs Private Functions

Functions ending with `_` (underscore) are **private** and CANNOT be called from client-side HTML via `google.script.run`. This is a silent failure — the call simply doesn't work with no error.

```javascript
// WRONG - dialog can't call this, fails silently
function doWork_() { return 'done'; }

// RIGHT - dialog can call this
function doWork() { return 'done'; }
```

**Also applies to**: Menu item function references must be public function names as strings.

### Batch Operations (Critical for Performance)

Read/write data in bulk, never cell-by-cell. The difference is 70x.

```javascript
// SLOW (70 seconds on 100x100) - reads one cell at a time
for (let i = 1; i <= 100; i++) {
  const val = sheet.getRange(i, 1).getValue();
}

// FAST (1 second) - reads all at once
const allData = sheet.getRange(1, 1, 100, 1).getValues();
for (const row of allData) {
  const val = row[0];
}
```

Always use `getRange().getValues()` / `setValues()` for bulk reads/writes.

### V8 Runtime

V8 is the **only** runtime (Rhino was removed January 2026). Supports modern JavaScript: `const`, `let`, arrow functions, template literals, destructuring, classes, async/generators.

**NOT available** (use Apps Script alternatives):

| Missing API | Apps Script Alternative |
|-------------|------------------------|
| `setTimeout` / `setInterval` | `Utilities.sleep(ms)` (blocking) |
| `fetch` | `UrlFetchApp.fetch()` |
| `FormData` | Build payload manually |
| `URL` | String manipulation |
| `crypto` | `Utilities.computeDigest()` / `Utilities.getUuid()` |

### Flush Before Returning

Call `SpreadsheetApp.flush()` before returning from functions that modify the sheet, especially when called from HTML dialogs. Without it, changes may not be visible when the dialog shows "Done."

### Simple vs Installable Triggers

| Feature | Simple (`onEdit`) | Installable |
|---------|-------------------|-------------|
| Auth required | No | Yes |
| Send email | No | Yes |
| Access other files | No | Yes |
| URL fetch | No | Yes |
| Open dialogs | No | Yes |
| Runs as | Active user | Trigger creator |

Use simple triggers for lightweight reactions. Use installable triggers (via `ScriptApp.newTrigger()`) when you need email, external APIs, or cross-file access.

### Custom Spreadsheet Functions

Functions used as `=MY_FUNCTION()` in cells have strict limitations:

```javascript
/**
 * Calculates something custom.
 * @param {string} input The input value
 * @return {string} The result
 * @customfunction
 */
function MY_FUNCTION(input) {
  // Can use: basic JS, Utilities, CacheService
  // CANNOT use: MailApp, UrlFetchApp, SpreadsheetApp.getUi(), triggers
  return input.toUpperCase();
}
```

- Must include `@customfunction` JSDoc tag
- 30-second execution limit (vs 6 minutes for regular functions)
- Cannot access services requiring authorisation

---

## Modal Progress Dialog

Block user interaction during long operations with a spinner that auto-closes. This is the recommended pattern for any operation taking more than a few seconds.

**Pattern: menu function > showProgress() > dialog calls action function > auto-close**

```javascript
function showProgress(message, serverFn) {
  const html = HtmlService.createHtmlOutput(`
    <!DOCTYPE html>
    <html>
    <head>
      <style>
        body {
          font-family: 'Google Sans', Arial, sans-serif;
          display: flex; flex-direction: column;
          align-items: center; justify-content: center;
          height: 100%; margin: 0; padding: 20px;
          box-sizing: border-box;
        }
        .spinner {
          width: 36px; height: 36px;
          border: 4px solid #e0e0e0;
          border-top: 4px solid #1a73e8;
          border-radius: 50%;
          animation: spin 0.8s linear infinite;
          margin-bottom: 16px;
        }
        @keyframes spin { to { transform: rotate(360deg); } }
        .message { font-size: 14px; color: #333; text-align: center; }
        .done { color: #1e8e3e; font-weight: 500; }
        .error { color: #d93025; font-weight: 500; }
      </style>
    </head>
    <body>
      <div class="spinner" id="spinner"></div>
      <div class="message" id="msg">${message}</div>
      <script>
        google.script.run
          .withSuccessHandler(function(result) {
            document.getElementById('spinner').style.display = 'none';
            var m = document.getElementById('msg');
            m.className = 'message done';
            m.innerText = 'Done! ' + (result || '');
            setTimeout(function() { google.script.host.close(); }, 1200);
          })
          .withFailureHandler(function(err) {
            document.getElementById('spinner').style.display = 'none';
            var m = document.getElementById('msg');
            m.className = 'message error';
            m.innerText = 'Error: ' + err.message;
            setTimeout(function() { google.script.host.close(); }, 3000);
          })
          .${serverFn}();
      </script>
    </body>
    </html>
  `).setWidth(320).setHeight(140);

  SpreadsheetApp.getUi().showModalDialog(html, 'Working...');
}

// Menu calls this wrapper
function menuDoWork() {
  showProgress('Processing data...', 'doTheWork');
}

// MUST be public (no underscore) for the dialog to call it
function doTheWork() {
  // ... do the work ...
  SpreadsheetApp.flush();
  return 'Processed 50 rows';  // shown in success message
}
```

---

## Error Handling

Always wrap external calls in try/catch. Return meaningful messages to dialogs.

```javascript
function fetchExternalData() {
  try {
    const response = UrlFetchApp.fetch('https://api.example.com/data', {
      headers: { 'Authorization': 'Bearer ' + getApiKey() },
      muteHttpExceptions: true
    });
    if (response.getResponseCode() !== 200) {
      throw new Error('API returned ' + response.getResponseCode());
    }
    return JSON.parse(response.getContentText());
  } catch (e) {
    Logger.log('Error: ' + e.message);
    throw e;  // re-throw for dialog error handler
  }
}
```

---

## Error Prevention

| Mistake | Fix |
|---------|-----|
| Dialog can't call function | Remove trailing `_` from function name |
| Script is slow on large data | Use `getValues()`/`setValues()` batch operations |
| Changes not visible after dialog | Add `SpreadsheetApp.flush()` before return |
| `onEdit` can't send email | Use installable trigger via `ScriptApp.newTrigger()` |
| Custom function times out | 30s limit — simplify or move to regular function |
| `setTimeout` not found | Use `Utilities.sleep(ms)` (blocking) |
| Script exceeds 6 min | Break into chunks, use time-driven trigger for batches |
| Auth popup doesn't appear | User must click Advanced > Go to (unsafe) > Allow |

## Common Pattern Index

See `references/patterns.md` for complete code examples:

| Pattern | When to Use |
|---------|-------------|
| Custom menus | Adding actions to the spreadsheet toolbar |
| Sidebar apps | Forms and data entry panels |
| Triggers | Automated reactions to edits, time, or form submissions |
| Email from sheets | Sending reports, notifications, schedules |
| PDF export | Generating and emailing sheet as PDF |
| Data validation | Creating dropdowns from lists or ranges |

See `references/recipes.md` for complete automation recipes (archive rows, highlight duplicates, auto-number, dashboards).

See `references/quotas.md` for execution limits, email quotas, and debugging tips.
