---
name: claude-chrome
description: "Claude in Chrome - browser automation via the official Anthropic extension. Control your logged-in Chrome browser, automate workflows, fill forms, extract data, and run scheduled tasks."
---

# Claude in Chrome Skill

Control your real Chrome browser with Claude. The extension runs in your authenticated browser session, so Claude can interact with sites you're already logged into - Gmail, Google Docs, Notion, CRMs, and more.

## Integration Options

There are two ways to control Chrome:

1. **Claude Code + Chrome Extension** - Terminal-based browser control via `claude --chrome`
2. **Chrome DevTools MCP** - MCP server providing 26 browser automation tools

Both use your real Chrome with existing logins - no re-authentication needed.

---

## Option 1: Claude Code + Chrome Extension

### Prerequisites
- Google Chrome browser
- Claude in Chrome extension (v1.0.36+) from Chrome Web Store
- Claude Code CLI (v2.0.73+)
- Paid Claude plan (Pro, Team, Enterprise, or Max)

### Setup

Update Claude Code:
```bash
claude update
```

Start with Chrome enabled:
```bash
claude --chrome
```

Check connection status:
```
/chrome
```

Enable Chrome by default:
```
/chrome
# Select "Enabled by default"
```

### Browser Capabilities

**Navigation & Interaction:**
- Navigate to URLs
- Click elements (buttons, links, form fields)
- Type text into inputs
- Scroll pages
- Create and manage tabs
- Resize windows

**Information Retrieval:**
- Read page content and DOM state
- Access console logs and errors
- Monitor network requests
- Extract structured data from pages

**Advanced:**
- Fill forms automatically
- Record browser actions as GIFs
- Chain browser + terminal commands
- Work across multiple tabs

### Example Prompts

#### Basic Navigation
```
Go to github.com/anthropics and click on the "Code" tab
```

#### Form Testing
```
Open localhost:3000, try submitting the login form with invalid data,
and check if error messages appear correctly
```

#### Console Debugging
```
Open the dashboard page and check the console for any errors when
the page loads
```

#### Data Extraction
```
Go to the product listings page and extract the name, price, and
availability for each item. Save as CSV.
```

#### Authenticated Workflows
```
Draft a project update based on our recent commits and add it to
my Google Doc at docs.google.com/document/d/abc123
```

#### Form Automation
```
I have contacts in contacts.csv. For each row, go to crm.example.com,
click "Add Contact", and fill in the name, email, and phone fields.
```

#### Record Demo GIF
```
Record a GIF showing the checkout flow from adding an item to cart
through to the confirmation page
```

### How It Works

1. Extension uses Chrome's Native Messaging API to receive commands
2. Claude opens new tabs for tasks (doesn't take over existing tabs)
3. Uses your browser's login state - no re-authentication needed
4. Pauses for CAPTCHAs, login prompts, or modal dialogs (you handle, then continue)

### Troubleshooting

**Extension not detected:**
```bash
claude --version  # Should be 2.0.73+
```
Then run `/chrome` and select "Reconnect extension"

**Browser not responding:**
- Check for blocking modal dialogs (alert, confirm, prompt)
- Ask Claude to create a new tab and retry
- Restart Chrome extension (disable/re-enable in chrome://extensions)

---

## Option 2: Chrome DevTools MCP

An alternative/complementary approach using Model Context Protocol.

### Installation

```bash
claude mcp add chrome-devtools npx chrome-devtools-mcp@latest
```

Or add to MCP config:
```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest"]
    }
  }
}
```

### Available Tools (26 total)

**Input Automation (8 tools):**
- `click` - Click elements
- `drag` - Drag and drop
- `fill` - Fill input fields
- `fill_form` - Fill entire forms
- `handle_dialog` - Handle alerts/confirms/prompts
- `hover` - Hover over elements
- `press_key` - Keyboard input
- `upload_file` - Upload files

**Navigation (6 tools):**
- `navigate_page` - Go to URL
- `new_page` - Create new tab
- `close_page` - Close tab
- `list_pages` - List open pages
- `select_page` - Switch to page
- `wait_for` - Wait for element/condition

**Debugging (5 tools):**
- `take_screenshot` - Capture page
- `take_snapshot` - Capture DOM
- `evaluate_script` - Run JavaScript
- `get_console_message` - Get console log
- `list_console_messages` - Get all logs

**Network (2 tools):**
- `list_network_requests` - List requests
- `get_network_request` - Get request details

**Performance (3 tools):**
- `performance_start_trace` - Start tracing
- `performance_stop_trace` - Stop tracing
- `performance_analyze_insight` - Analyze results

**Emulation (2 tools):**
- `emulate` - Emulate device
- `resize_page` - Resize viewport

### Configuration Options

```bash
# Connect to running Chrome
npx chrome-devtools-mcp@latest --browser-url http://localhost:9222

# Headless mode
npx chrome-devtools-mcp@latest --headless

# Custom viewport
npx chrome-devtools-mcp@latest --viewport 1920x1080

# Use Chrome Canary
npx chrome-devtools-mcp@latest --channel canary
```

---

## Claude in Chrome Extension Features

### Workflow Shortcuts

Create reusable shortcuts (type "/" in extension):

**Record a workflow:**
1. Click cursor icon or type "/" → "Record workflow"
2. Perform actions while Claude watches
3. Claude generates shortcut with name, description, URL

**Save from conversation:**
- Click "Convert to task" on conversation header
- Or hover over a sent prompt and save it

### Scheduled Tasks

Set recurring browser automation:

1. When creating shortcut, toggle "Schedule"
2. Set frequency: daily, weekly, monthly, annually
3. Choose date/time and model
4. Claude runs automatically with notifications

Example scheduled tasks:
- Daily inbox cleanup at 9am
- Weekly competitor scan every Monday
- Monthly expense report filing

### Multi-Tab Workflows

Claude can see and work across tabs in the same tab group:
- Reference information from multiple tabs
- Copy data between tabs
- Coordinate actions across sites

### Workflow Examples

**Email Management:**
```
/inbox-cleanup
Archive emails from newsletters, star emails mentioning deadlines,
delete obvious spam
```

**Research:**
```
/competitor-scan
Check competitor blogs, pricing pages, and careers pages.
Summarize any changes since last week.
```

**Form Filling:**
```
/vendor-application
Fill vendor application form using our company documents.
Pause before final submission for review.
```

**Meeting Prep:**
```
/stakeholder-map
Research LinkedIn profiles of meeting attendees.
Summarize their backgrounds and priorities.
```

---

## Best Practices

### When to Use Browser Automation

**Good for:**
- Form filling and data entry
- Button clicking and navigation
- Extracting data from authenticated pages
- Testing web applications
- Executing predefined workflows
- Tasks behind logins

**Better manually:**
- One-click tasks (faster by hand)
- Subjective decisions
- Exploratory research (use Claude.ai chat instead)

### Tips

1. **Be specific** - Ambiguous instructions produce inconsistent results
2. **Add verification** - For long lists, add "verify you completed all items"
3. **Handle modals** - Dismiss alerts manually, then tell Claude to continue
4. **Use fresh tabs** - If a tab becomes unresponsive, ask for a new one
5. **Filter console output** - Specify patterns vs. requesting all logs

### Security

- Site-level permissions control which sites Claude can access
- High-risk actions (publish, purchase, share data) require confirmation
- Some site categories blocked (financial services, adult content)
- Manage permissions in extension settings

---

## Common Workflows for Clawdbot

### Testing Local Development
```
"Open localhost:3000, test the new form validation, check console for errors,
and screenshot any issues you find"
```

### Authenticated Data Extraction
```
"Go to my Google Analytics, get this week's traffic summary,
and save it to a file"
```

### Content Management
```
"Open my Notion workspace, find the Q4 planning doc,
and add a new section with today's meeting notes"
```

### Email Drafts
```
"Open Gmail, find unread emails from the engineering team,
and draft replies for each one without sending"
```

### Multi-Site Research
```
"Compare pricing on our product page vs the top 3 competitors.
Create a markdown table with the differences."
```

---

## Requirements

| Component | Minimum Version |
|-----------|-----------------|
| Google Chrome | Latest stable |
| Claude in Chrome Extension | 1.0.36+ |
| Claude Code CLI | 2.0.73+ |
| Claude Plan | Pro, Team, Enterprise, or Max |
| Node.js (for DevTools MCP) | 20.19+ |

**Not supported:**
- Other Chromium browsers (Brave, Arc, Edge)
- WSL (Windows Subsystem for Linux)
- Headless mode (for extension; DevTools MCP supports headless)
- Mobile devices
