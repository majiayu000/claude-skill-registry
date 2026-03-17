---
name: automating-mail
description: Automates Apple Mail via JXA with AppleScript dictionary discovery. Use when asked to "automate email", "send mail via script", "JXA Mail automation", or "filter email messages". Covers accounts, mailboxes, batch message filtering, composition, attachments, and UI fallback.
allowed-tools:
  - Bash
  - Read
  - Write
---

# Automating Apple Mail (JXA-first, AppleScript discovery)

## Contents
- [Relationship to macOS automation skill](#relationship-to-the-macos-automation-skill)
- [Core Framing](#core-framing)
- [Workflow](#workflow-default)
- [Quick Start Examples](#quick-start-examples)
- [Validation Checklist](#validation-checklist)
- [When Not to Use](#when-not-to-use)
- [What to load](#what-to-load)

## Relationship to the macOS automation skill
- Use `automating-mac-apps` for permissions, shell, and UI scripting guidance.
- **PyXA Installation:** See `automating-mac-apps` skill (PyXA Installation section).

## Core Framing
- Mail dictionary is AppleScript-first; discover in Script Editor.
- Objects are specifiers: read via method calls (`message.subject()`), modify via assignments (`message.readStatus = true`).
- ObjC bridge available for advanced filesystem operations.

## Workflow (default)
1) [ ] Ensure Mail configured and automation permissions enabled.
2) [ ] Discover terms in Script Editor (Mail dictionary).
3) [ ] Prototype minimal AppleScript command.
4) [ ] Port to JXA with defensive checks.
5) [ ] Use batch reads for performance.
6) [ ] Use UI scripting for signature and UI-only actions.

## Quick Start Examples

**Read inbox (JXA):**
```javascript
const Mail = Application('Mail');
const message = Mail.inbox.messages[0];
console.log(message.subject());
```

**Compose message (JXA):**
```javascript
const msg = Mail.OutgoingMessage({
  subject: "Status Update",
  content: "All systems go."
});
Mail.outgoingMessages.push(msg);
msg.visible = true;
```

**PyXA alternative:**
```python
import PyXA
mail = PyXA.Mail()
inbox = mail.inboxes()[0]
message = inbox.messages()[0]
print(f"Subject: {message.subject()}")
```

## Validation Checklist
- [ ] Automation permissions granted (System Settings > Privacy > Automation)
- [ ] Inbox access works: `Mail.inbox.messages.length`
- [ ] Message property reads return expected values
- [ ] Composition creates visible draft
- [ ] Batch operations complete without errors

## When Not to Use
- For cross-platform email automation (use IMAP/SMTP libraries)
- For bulk email sending (use transactional email services like SendGrid)
- When processing untrusted email content (security risk)
- For non-macOS platforms

## What to load
- Mail JXA basics: `automating-mail/references/mail-basics.md`
- Recipes (filter, move, compose): `automating-mail/references/mail-recipes.md`
- Advanced patterns (batch ops, HTML, signatures): `automating-mail/references/mail-advanced.md`
- Dictionary translation table: `automating-mail/references/mail-dictionary.md`
- Rule scripts: `automating-mail/references/mail-rules.md`
- HTML + signature workflow: `automating-mail/references/html-signature-workflow.md`
- Attachment extraction pipeline: `automating-mail/references/attachment-extraction.md`
- Mailbox archiver: `automating-mail/references/mailbox-archiver.md`
- HTML data merge: `automating-mail/references/html-data-merge.md`
- **PyXA API Reference** (complete class/method docs): `automating-mail/references/mail-pyxa-api-reference.md`