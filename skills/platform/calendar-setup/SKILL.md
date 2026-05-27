---
name: calendar-setup
description: Grant Python calendar access for 30x faster calendar queries (30s → <1s)
---

# Calendar Setup - Enable Fast Queries

**Purpose:** Grant Python calendar access for 30x faster calendar queries (30s → <1s)

**When to run:**
- After initial Dex installation
- If calendar queries feel slow
- If you see "Calendar access denied" errors

---

## Process

1. **Check current permission status:**
   - Run the permission checker: `python3 core/mcp/scripts/check_calendar_permission.py`
   - Show the user what status was returned

2. **If Already Authorized:**
   - Great! Calendar queries are already optimized.
   - No action needed.

3. **If NotDetermined (permission not yet requested):**
   - The script will show a macOS permission dialog
   - Guide user: "Click 'OK' when the dialog appears to grant Python access to Calendar"
   - Run the script again to verify

4. **If Denied (previously rejected):**
   - Show clear instructions:
     ```
     To enable fast calendar queries:

     1. Open System Settings (Command+Space, type "System Settings")
     2. Click "Privacy & Security" in the sidebar
     3. Click "Calendars"
     4. Find "Python" or "python3" in the list
     5. Enable the checkbox
     6. Run `/calendar-setup` again to verify
     ```

5. **If Restricted:**
   - Explain: "Calendar access is blocked by system policies (parental controls or enterprise MDM)"
   - Calendar queries will use AppleScript (slower but functional)
   - No user action possible

6. **After Success:**
   - Confirm: "✅ Calendar access granted! Queries are now 30x faster."
   - Explain: "Calendar queries now use native EventKit instead of AppleScript"
   - No need to run this again - permission is persistent

---

## Technical Notes

- **EventKit vs AppleScript:** EventKit uses database queries (fast), AppleScript loads all events then filters (slow)
- **Permission is persistent:** Once granted, Python keeps access until explicitly revoked
- **Privacy:** All calendar data stays local - Dex never sends calendar data anywhere
- **Fallback:** If EventKit isn't available, Dex falls back to AppleScript (works but slower)

---

## Troubleshooting

**"Module EventKit not found":**
- Run: `pip3 install pyobjc-framework-EventKit`
- This should have been installed during Dex setup

**Permission dialog doesn't appear:**
- System Settings might already show "Denied" from a previous attempt
- Follow the manual steps above to toggle permission on

**Still seeing slow queries after granting access:**
- Restart your coding harness (Cursor/Claude Code/Pi) to reload MCP server
- Verify permission: `python3 core/mcp/scripts/check_calendar_permission.py`
