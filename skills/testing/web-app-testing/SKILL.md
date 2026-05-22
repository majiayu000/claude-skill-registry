---
name: web-app-testing
description: Gemini 2.5 Computer Use for browser automation with VISIBLE local browser. Watch Gemini AI control your browser in real-time. Perfect for web app testing, automation demos, and debugging.
allowed-tools: [Bash, TodoWrite, Read, Write]
metadata:
  version: "3.0.0"
  author: "Custom Skill"
  category: "testing"
  gemini-model: "gemini-2.5-computer-use-preview-10-2025"
  implementation: "Official Gemini Computer Use pattern with Playwright"
---

# Gemini Computer Use - Web Browser Automation

You are an expert web application testing assistant using **Gemini 2.5 Computer Use** - Google's AI that can see and control web browsers.

## What This Skill Does

This skill implements Gemini Computer Use the **correct way** according to Google's official documentation:

1. **Gemini AI analyzes screenshots** of your browser
2. **Gemini decides what actions to take** (where to click, what to type)
3. **Actions execute on YOUR local browser** using Playwright
4. **You WATCH it happen** in real-time on your screen
5. **New screenshot sent back to Gemini** to continue the loop

✅ **AI-powered decision making** (Gemini)
✅ **Visible browser on your screen** (Playwright)
✅ **Best of both worlds!**

## Purpose

- **Web Application Testing**: Automated testing with AI understanding
- **Browser Automation**: Let AI navigate complex workflows
- **Debugging**: Watch AI interact with your site to find issues
- **Demos**: Show intelligent browser automation in action

## How It Works

```
┌─────────────┐
│   Gemini AI │  Analyzes screenshot
│             │  Decides: "Click search box at (821, 202)"
└──────┬──────┘
       │
       ↓ function_call: click(821, 202)
       │
┌──────┴──────┐
│  Playwright │  Executes click on YOUR screen
│   (Visible) │  Captures new screenshot
└──────┬──────┘
       │
       ↓ new screenshot + result
       │
┌──────┴──────┐
│   Gemini AI │  Sees result, plans next action
│             │  Loop continues...
└─────────────┘
```

## Variables

- `{URL}`: Target URL to test/automate
- `{TASK}`: What you want Gemini to do (in natural language)

## Usage

### Basic Command (Windows)

**IMPORTANT**: Use absolute path directly - DO NOT use `cd` commands on Windows!

```bash
python "C:\Users\USERNAME\.claude\skills\web-app-testing\scripts\gemini_browser.py" "{URL}" --task "{TASK}"
```

### Example Commands (Windows)

```bash
# Search Wikipedia for cats (VISIBLE BROWSER)
python "C:\Users\USERNAME\.claude\skills\web-app-testing\scripts\gemini_browser.py" "https://en.wikipedia.org" --task "Search for cats and tell me the first paragraph about them"

# Test a login flow
python "C:\Users\USERNAME\.claude\skills\web-app-testing\scripts\gemini_browser.py" "http://localhost:3000" --task "Test the login flow with username 'test' and password 'demo123'"

# Check console errors
python "C:\Users\USERNAME\.claude\skills\web-app-testing\scripts\gemini_browser.py" "https://google.com" --task "Navigate to the site and check for any console errors"

# Fill out a form
python "C:\Users\USERNAME\.claude\skills\web-app-testing\scripts\gemini_browser.py" "https://example.com/contact" --task "Fill out the contact form with test data"

# Run with custom slow motion (1 second per action)
python "C:\Users\USERNAME\.claude\skills\web-app-testing\scripts\gemini_browser.py" "https://wikipedia.org" --task "Search for dogs" --slow 1000

# Run in headless mode (no visible browser)
python "C:\Users\USERNAME\.claude\skills\web-app-testing\scripts\gemini_browser.py" "https://google.com" --task "Check console" --headless
```

### Command Options

- `--task` / `-t`: **Required** - Natural language description of task
- `--slow`: Slow motion delay in milliseconds (default: 500ms)
- `--headless`: Run without visible browser (default: visible)
- `--max-turns`: Maximum conversation turns (default: 20)

## Workflow for Claude Code

When user asks to test a web application or automate browser tasks:

### Step 1: Parse Request

Extract:
- **URL**: Target website
- **Task**: What to do (user's natural language description)

### Step 2: Run Gemini Computer Use (Windows-Optimized)

**CRITICAL**: Use absolute path with quoted arguments - NO `cd` commands!

```bash
python "C:\Users\USERNAME\.claude\skills\web-app-testing\scripts\gemini_browser.py" "{URL}" --task "{TASK}"
```

**Token-Efficient Pattern**:
- ✅ Single command execution
- ✅ Absolute path in quotes
- ✅ No directory changes needed
- ✅ Works on Windows without path errors

### Step 3: Observe Output

The script will:
1. ✅ Launch visible browser (maximized window)
2. ✅ Show Gemini's decisions in terminal
3. ✅ Execute actions in slow motion (you can watch)
4. ✅ Display console logs when done
5. ✅ Keep browser open 10 seconds for inspection
6. ✅ Return final results

### Step 4: Report Results

Summarize what Gemini accomplished, any errors found, and console logs.

## Example Session

```
User: "Go to Wikipedia and search for cats"

Claude Code executes:
  python "C:\Users\USERNAME\.claude\skills\web-app-testing\scripts\gemini_browser.py" "https://en.wikipedia.org" --task "Search for cats"

Output shows:
  [BROWSER] Launching VISIBLE browser...
  [BROWSER] ✓ Browser ready

  TURN 1
  [EXECUTING] navigate({"url": "https://en.wikipedia.org"})
    → Navigating to: https://en.wikipedia.org

  TURN 2
  [GEMINI] I can see the Wikipedia homepage. I'll search for "cats" now.
  [EXECUTING] type_text_at({"x": 821, "y": 202, "text": "cats", "press_enter": true})
    → Clicking at (821, 202) then typing: 'cats'
    → Typing: 'cats'
    → Pressing Enter

  TURN 3
  [GEMINI] I've successfully navigated to the Cat article on Wikipedia.
  [COMPLETE] Task finished!

  BROWSER CONSOLE LOGS
  ✓ No console errors

  [BROWSER] Keeping browser open for 10 seconds...
```

User sees:
- ✅ Browser window opens on their screen
- ✅ Watches Wikipedia load
- ✅ Sees search box get clicked
- ✅ Watches "cats" being typed
- ✅ Sees search submit and results appear
- ✅ Browser stays open to inspect
```

## Key Features

### AI Intelligence
- Gemini analyzes page visually (like a human)
- Adapts to different page layouts
- Makes intelligent decisions about what to click
- Understands context and intent

### Visible Execution
- Browser opens on YOUR screen (maximized)
- Actions happen in slow motion (configurable)
- You can watch every step
- Browser stays open for inspection

### Console Log Capture
- Captures errors, warnings, and info messages
- Displays organized summary at end
- Helps identify JavaScript issues

### Screenshot Loop
- Every action triggers new screenshot
- Gemini sees the updated page state
- Enables accurate decision-making

## Important Notes

### This is NOT a Hybrid System
This is the **official Gemini Computer Use implementation** according to Google's documentation. The pattern is:
1. Screenshot → Gemini
2. Gemini → Function call
3. Execute function locally
4. New screenshot → back to Gemini

### Browser Visibility
- **Default**: Visible browser (headless=False)
- **Option**: Can run headless with `--headless` flag
- **Recommended**: Keep visible for debugging/demos

### API Costs
- Each Gemini API call incurs costs
- Screenshots are sent with each turn
- Complex tasks = more API calls
- Monitor usage in Google AI Studio

### Best Practices
- ✅ Use specific, clear task descriptions
- ✅ Test on localhost first before production
- ✅ Watch the browser to understand AI behavior
- ✅ Keep tasks focused and achievable
- ❌ Don't test production without permission
- ❌ Don't use for CAPTCHA bypass or scraping at scale

## Troubleshooting

### Browser doesn't open
- Check Playwright is installed: `pip install playwright`
- Install browsers: `playwright install chromium`

### Gemini not finding elements
- Increase `--slow` to give page time to load
- Check if page uses dynamic content
- Verify URL is accessible

### API errors
- Check API key is valid
- Verify quota not exceeded
- Check internet connectivity

## Version History

- **v3.0.0**: Complete rewrite with proper Gemini Computer Use implementation
- **v2.1.0**: Added local Playwright mode (deprecated)
- **v2.0.0**: Initial Gemini integration (simulated, deprecated)

---

**Created by**: Custom Skill Builder
**Last Updated**: 2025-10-19
**Version**: 3.0.0
**Implementation**: Official Gemini Computer Use pattern
