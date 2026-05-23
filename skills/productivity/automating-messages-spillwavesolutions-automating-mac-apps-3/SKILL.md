---
name: automating-messages
description: Automates macOS Messages (iMessage/SMS) via JXA with reliable service→buddy resolution. Use when asked to "automate iMessage", "send Messages via script", "JXA Messages automation", or "read Messages history". Covers send-bug workarounds, UI scripting for attachments, chat.db forensics, and launchd polling bots.
allowed-tools:
  - Bash
  - Read
  - Write
---

# Automating Messages (JXA-first with UI/DB fallbacks)

## Contents
- [Permissions and scope](#permissions-and-scope)
- [Default workflow](#default-workflow-happy-path)
- [Quick recipe](#quick-recipe-defensive-send)
- [Attachments and UI fallback](#attachments-and-ui-fallback)
- [Data access and forensics](#data-access-and-forensics)
- [Validation Checklist](#validation-checklist)
- [When Not to Use](#when-not-to-use)
- [What to load](#what-to-load)

## Permissions and scope
- Grants needed: Automation + Accessibility; Full Disk Access for any `chat.db` reads.
- Keep automation scoped and auditable; avoid unsolicited sends and DB writes.
- Pairs with `automating-mac-apps` for common setup (permissions, osascript invocation, UI scripting basics).

## Default workflow (happy path)
1) [ ] Resolve transport: pick `serviceType` (`iMessage` or `SMS`) before targeting a buddy.
2) [ ] Identify recipient: filter buddies by `handle` (phone/email). Avoid ambiguous names.
3) [ ] Send via app-level `send`: pass Buddy object to `Messages.send()`.
4) [ ] Verify window context: activate Messages when mixing with UI steps.
5) [ ] Fallbacks: if send/attachments fail, use UI scripting; for history, use SQL.

## Quick recipe (defensive send)
```javascript
const Messages = Application('Messages');
Messages.includeStandardAdditions = true;

function safeSend(text, handle, svcType = 'iMessage') {
  const svc = Messages.services.whose({ serviceType: svcType })[0];
  if (!svc) throw new Error(`Service ${svcType} missing`);
  const buddy = svc.buddies.whose({ handle })[0];
  if (!buddy) throw new Error(`Buddy ${handle} missing on ${svcType}`);
  Messages.send(text, { to: buddy });
}
```
- Wrap with `try/catch` and log; add small delays when activating UI.
- For groups, target an existing chat by GUID or fall back to UI scripting; array sends are unreliable.

## Attachments and UI fallback
- Messages lacks a stable JXA attachment API; use clipboard + System Events paste/send.
- Ensure Accessibility permission, bring app forward, paste file, press Enter.
- See `references/ui-scripting-attachments.md` for the full flow and ObjC pasteboard snippet.

## Data access and forensics

**Reading messages limitation:** The AppleScript/JXA API for Messages is effectively **write-only**. While `send()` works reliably, reading messages via `chat.messages()` or similar methods is broken/unsupported in modern macOS. The only reliable way to read message history is via direct SQLite access to `~/Library/Messages/chat.db`.

**Security consideration:** Reading `chat.db` requires **Full Disk Access** permission, which grants broad filesystem access beyond just Messages. This is a significant security trade-off - granting Full Disk Access to scripts or applications exposes all user data. Consider whether reading message history is truly necessary before enabling this permission.

- Use SQL against `chat.db` for history; JXA `chat.messages()` is unreliable/non-functional.
- Requires: **System Settings > Privacy & Security > Full Disk Access** for your terminal/script.
- Remember Cocoa epoch conversion (nanoseconds since 2001-01-01); use `sqlite3 -json` for structured results.
- See `references/database-forensics.md` for schema notes, typedstream handling, and export tooling.

**Example read query (requires Full Disk Access):**
```sql
sqlite3 ~/Library/Messages/chat.db "SELECT
  CASE WHEN m.is_from_me = 1 THEN 'Me' ELSE 'Them' END as sender,
  m.text,
  datetime(m.date/1000000000 + 978307200, 'unixepoch', 'localtime') as date
FROM message m
JOIN handle h ON m.handle_id = h.rowid
WHERE h.id LIKE '%PHONE_NUMBER%'
ORDER BY m.date DESC LIMIT 10;"
```

## Bots and monitoring
- Implement polling daemons with `launchd` now that on-receive handlers are gone.
- Track `rowid`, query diffs, dispatch actions, and persist state.
- See `references/monitoring-daemons.md` for the polling pattern and plist notes.

## Validation Checklist
- [ ] Automation + Accessibility permissions granted
- [ ] Service resolves: `Messages.services.whose({ serviceType: 'iMessage' })[0]` returns object
- [ ] Buddy lookup works: `svc.buddies.whose({ handle })[0]` returns target
- [ ] Test send completes without errors
- [ ] Full Disk Access granted if using `chat.db` reads

## When Not to Use
- For reading message history without Full Disk Access (AppleScript/JXA cannot read messages)
- For cross-platform messaging (use platform APIs or third-party services)
- For business SMS automation (use Twilio or similar APIs)
- When iMessage/SMS features are not available on the target system
- For bulk messaging (rate limits and security restrictions apply)
- When security policy prohibits Full Disk Access grants (required for any read operations)

## What to load
- Control plane and send reliability: `references/control-plane.md`
- UI scripting + attachments fallback: `references/ui-scripting-attachments.md`
- SQL/history access: `references/database-forensics.md`
- Polling bots/launchd: `references/monitoring-daemons.md`
