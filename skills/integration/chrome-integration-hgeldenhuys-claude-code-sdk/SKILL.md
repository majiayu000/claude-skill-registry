---
name: chrome-integration
description: Guide for using Claude Code with Chrome browser integration. Use when automating browser tasks, debugging web apps, testing UI, or extracting data from websites. Covers setup, capabilities, and common workflows.
allowed-tools: ["Read", "Bash", "Glob", "Grep"]
---

# Chrome Integration

Connect Claude Code to Chrome for browser automation, live debugging, and web app testing.

## Quick Reference

| Element | Requirement |
|---------|-------------|
| Status | Beta (Chrome only, no Brave/Arc/WSL) |
| CLI Flag | `claude --chrome` |
| Slash Command | `/chrome` (status/enable in-session) |
| Extension | Claude in Chrome v1.0.36+ |
| Claude Code | v2.0.73+ |
| Plan | Pro, Team, or Enterprise |

## What You Can Do

| Capability | Description |
|------------|-------------|
| **Live Debugging** | Read console errors, DOM state, fix code directly |
| **Design Verification** | Build UI, open in browser, verify against mocks |
| **Web App Testing** | Test forms, check regressions, verify user flows |
| **Authenticated Apps** | Access Google Docs, Gmail, Notion using your login |
| **Data Extraction** | Pull structured data from web pages |
| **Task Automation** | Automate data entry, form filling, multi-site workflows |
| **Session Recording** | Record browser interactions as GIFs |

## Setup

### Prerequisites

1. Google Chrome browser installed
2. [Claude in Chrome extension](https://chromewebstore.google.com/detail/claude/fcoeoabgfenejglbffodgkkbkcdhcgfn) v1.0.36+
3. Claude Code v2.0.73+
4. Paid Claude plan

### Enable Chrome Integration

**Option 1: At startup**
```bash
claude --chrome
```

**Option 2: In-session**
```
/chrome
```

### Verify Connection

Run `/chrome` to check status. If extension not detected, you'll see install instructions.

## How It Works

- Claude Code communicates via Chrome's Native Messaging API
- Extension receives commands and executes in browser
- Opens **new tabs** for tasks (doesn't take over existing)
- **Shares login state** - if you're logged into a site, Claude can access it
- **Visible browser** required (no headless mode)

### Handling Blockers

When Claude encounters login pages, CAPTCHAs, or other blockers:
1. Claude pauses and asks you to handle it
2. You can provide credentials or log in manually
3. Tell Claude to continue when ready

## Common Workflows

### Debug a Web App

```
Open localhost:3000, check the console for errors,
and fix any issues you find in the code
```

### Test a Form

```
Go to my signup form at localhost:3000/signup,
try submitting with invalid data, and verify
the error messages are correct
```

### Extract Data

```
Go to https://example.com/products, extract all
product names and prices, and save them to products.json
```

### Verify Design

```
Open localhost:3000 and compare the header layout
to this Figma screenshot: [paste screenshot]
```

### Automate Multi-Step Task

```
Log into my staging site, navigate to settings,
update the company name to "Acme Corp", and
take a screenshot of the confirmation
```

## Workflow: Browser Debugging Session

### Prerequisites
- [ ] Chrome extension installed
- [ ] Claude Code v2.0.73+
- [ ] Dev server running (if testing local app)

### Steps

1. **Start Claude with Chrome**
   - [ ] Run `claude --chrome`
   - [ ] Verify connection with `/chrome`

2. **Navigate to Your App**
   - [ ] Ask Claude to open your URL
   - [ ] Wait for page to load

3. **Debug Issues**
   - [ ] Claude reads console errors
   - [ ] Claude inspects DOM state
   - [ ] Claude fixes code in terminal
   - [ ] Refresh to verify fix

4. **Document Results**
   - [ ] Record GIF of working feature
   - [ ] Commit fixes

### Validation
- [ ] Console errors resolved
- [ ] UI renders correctly
- [ ] User flows work as expected

## Tips and Best Practices

### Be Specific with URLs
```
# Good
Go to localhost:3000/dashboard

# Avoid
Open my app
```

### Chain Terminal and Browser Actions
```
Run the tests, then open the coverage report
in Chrome and summarize the uncovered areas
```

### Use for Visual Verification
```
Build a card component matching this design,
then open it in Chrome and verify the spacing
```

### Handle Dynamic Content
```
Wait for the loading spinner to disappear,
then extract the table data
```

## Limitations

| Limitation | Details |
|------------|---------|
| Chrome Only | No Brave, Arc, or other Chromium browsers |
| No WSL | Windows Subsystem for Linux not supported |
| No Headless | Requires visible browser window |
| Your Session | Uses your login state (feature, not bug) |
| Extension Required | Claude in Chrome must be installed |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Extension not detected | Install/update Claude in Chrome extension |
| Connection failed | Restart Chrome, try `/chrome` again |
| Can't access site | Log in manually, then tell Claude to continue |
| Action failed | Try being more specific about what to click/type |
| Slow responses | Close unnecessary Chrome tabs |

## Security Considerations

- Chrome integration uses **your browser session**
- Claude can access any site you're logged into
- Sensitive actions (banking, etc.) require your explicit guidance
- Session recordings may capture sensitive data
- Use separate Chrome profile for sensitive work if needed

## Reference

| Resource | Description |
|----------|-------------|
| [Chrome Docs](https://code.claude.com/docs/en/chrome.md) | Official documentation |
| [Extension](https://chromewebstore.google.com/detail/claude/fcoeoabgfenejglbffodgkkbkcdhcgfn) | Chrome Web Store link |
| `/chrome` | In-session status and management |
