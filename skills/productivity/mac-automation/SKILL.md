---
name: mac-automation
description: 'This skill should be used when the user requests Mac automation via
  AppleScript, including: Mail operations, Reminders/Calendar management, Safari control,
  Finder operations, system controls (volume,'
---

---
name: mac-automation
description: This skill should be used when the user requests Mac automation via AppleScript, including: Mail operations, Reminders/Calendar management, Safari control, Finder operations, system controls (volume, brightness, notifications, app launching), third-party apps (development tools, task management, media players), or mentions "AppleScript" or "automate Mac".
author: 7Sageer, Claude
version: 0.0.5
---

# Mac Automation via AppleScript

This skill enables control of macOS applications and system functions through AppleScript execution via the `osascript` command.

## Core Principle

Execute AppleScript commands using the Bash tool with `osascript`:

```bash
osascript -e 'AppleScript code here'
```

For multi-line scripts:
```bash
osascript <<'EOF'
tell application "App Name"
    -- commands here
end tell
EOF
```

## Supported Applications & Functions

### 1. Mail (邮件)
- Send emails with subject, body, recipients
- Read unread emails
- Search emails
- Create drafts

### 2. Reminders (提醒事项)
- Create reminders with due dates
- List reminders by list
- Complete/delete reminders
- Create reminder lists

### 3. Calendar (日历)
- Create events with time, location, notes
- List today's/upcoming events
- Delete events
- Create calendars

### 4. Notification Center (通知中心)
- Display system notifications
- Custom title, subtitle, message
- Sound alerts

### 5. Safari
- Open URLs
- Get current page info
- Execute JavaScript
- Manage tabs and windows

### 6. Finder
- Open folders
- Get/set file info
- Move, copy, delete files
- Create folders
- Reveal files

### 7. System Controls (系统控制)
- Volume control (mute, set level)
- Brightness (via external tools)
- Open applications
- System info queries
- Sleep/restart/shutdown (with care)

### 8. Third-Party Applications

Many third-party apps support AppleScript. Common categories include development tools (iTerm2, VS Code), task management (OmniFocus, Things), media players (Spotify), browsers (Chrome), and communication tools. To check if an app supports AppleScript, open Script Editor to browse its dictionary, or try basic commands like `tell application "AppName" to get name`.

## Execution Guidelines

### Security Considerations

1. **Permission Prompts**: First-time use of certain apps triggers macOS permission dialogs. Inform user if automation fails due to permissions.

2. **Sensitive Operations**: For destructive operations (delete, shutdown), confirm with user before executing.

3. **Privacy-Sensitive Data**: When reading emails or calendar events, only display what user explicitly requests.

### Error Handling

Common errors and solutions:
- `"Application not found"` → Check app name spelling
- `"Not authorized"` → Guide user to System Preferences > Privacy & Security
- `"Can't get..."` → Resource doesn't exist, handle gracefully

### Best Practices

1. **Use exact app names**: "Mail", "Reminders", "Calendar", "Safari", "Finder"
2. **Escape special characters**: Use `\"` for quotes in strings
3. **Handle Unicode**: AppleScript handles Chinese/Unicode natively
4. **Check app state**: Some operations require app to be running

## Quick Reference

### Notifications
```bash
osascript -e 'display notification "消息内容" with title "标题"'
```

### Open Application
```bash
osascript -e 'tell application "AppName" to activate'
```

### Volume Control
```bash
# Get volume
osascript -e 'output volume of (get volume settings)'
# Set volume (0-100)
osascript -e 'set volume output volume 50'
# Mute
osascript -e 'set volume output muted true'
```

### System Commands
```bash
# Get clipboard
osascript -e 'the clipboard'
# Set clipboard
osascript -e 'set the clipboard to "text"'
```

## Additional Resources

### Reference Files

For detailed AppleScript patterns by application, consult:
- **`references/mail-applescript.md`** - Email operations: send, read, search, drafts
- **`references/reminders-applescript.md`** - Reminder operations: create, list, complete
- **`references/calendar-applescript.md`** - Calendar operations: events, calendars
- **`references/safari-applescript.md`** - Safari operations: URLs, tabs, JavaScript
- **`references/finder-applescript.md`** - Finder operations: files, folders
- **`references/system-applescript.md`** - System controls: volume, apps, clipboard

### Example Files

Working examples in `examples/`:
- **`daily-briefing.applescript`** - Get today's calendar and unread emails
- **`quick-note.applescript`** - Create reminder from clipboard

### Utility Scripts

Scripts in `scripts/`:
- **`run-applescript.sh`** - Wrapper for safe AppleScript execution

## Workflow Patterns

### Pattern 1: Information Retrieval
1. Execute AppleScript to query data
2. Parse output
3. Present formatted results to user

### Pattern 2: Action Execution
1. Confirm action with user if destructive
2. Execute AppleScript
3. Verify success
4. Report result

### Pattern 3: Multi-App Automation
1. Chain multiple AppleScript calls
2. Pass data between calls using shell variables
3. Handle errors at each step

## Common User Requests

| User Request | Action |
|-------------|--------|
| "发送邮件给xxx" | Use Mail to create and send |
| "提醒我明天..." | Create Reminder with due date |
| "添加日历事件" | Create Calendar event |
| "打开xxx网站" | Safari open URL |
| "调低音量" | Set volume lower |
| "显示通知" | Display notification |
| "打开文件夹" | Finder reveal |

## Troubleshooting

If AppleScript fails:
1. Check app is installed
2. Verify permissions in System Preferences
3. Ensure app name is exact
4. Try running app manually first
5. Check for syntax errors in script

For permission issues, guide user to:
**System Preferences > Privacy & Security > Automation**

## Self-Improvement Protocol

When an AppleScript execution fails or produces unexpected results, follow this protocol to improve the skill's reference documentation:

### 1. Error Analysis
- Identify the root cause of the failure
- Determine if it's a code issue, permission issue, or conceptual misunderstanding
- Check if the error is reproducible

### 2. Reference File Review
- Locate the relevant reference file in `references/` directory
- Review existing examples for similar patterns
- Identify if the error stems from incorrect or incomplete examples

### 3. Documentation Update
When you identify a fixable issue in the reference documentation:

**For incorrect examples:**
- Update the example code with the correct implementation
- Add inline comments explaining the fix
- Test the corrected code to verify it works

**For missing edge cases:**
- Add a new example demonstrating the correct approach
- Include explanatory comments about why this approach is needed

**For common pitfalls:**
- Add a "Common Pitfalls" or "Important Notes" section
- Document the error message users might encounter
- Explain the correct solution

### 4. Update Guidelines

Use the Edit tool to modify reference files:
```
Edit tool on: references/{app}-applescript.md
- Fix incorrect code examples
- Add warning notes for known issues
- Include error messages and solutions
```

### 5. Documentation Standards

When updating reference files, maintain:
- Clear, working code examples
- Inline comments for complex logic
- Error messages and their solutions
- Date-stamped notes for significant fixes

### 6. Version Tracking

After significant improvements:
- Update the version number in SKILL.md frontmatter
- Consider documenting major fixes in a changelog

This protocol ensures the skill continuously improves based on real-world usage and errors encountered.
