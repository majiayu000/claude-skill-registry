---
name: gmail
description: Gmail integration extension for PAL. USE WHEN triage inbox OR check emails OR process emails OR classify emails OR capture email OR reply to email OR draft reply OR email triage OR gmail OR follow up on email OR waiting for reply OR distribute emails OR process emails.
user-invocable: true
---

# gmail

Optional extension that adds Gmail as a fully isolated capture channel. Emails live in `Inbox/Emails/` — completely separate from `Inbox/Notes/`. Owns the full email pipeline with three mirrored workflows. No core workflows are patched.

```
Inbox/Emails/  ←  email_triage → process_emails → distribute_emails
```

---

## Guardrails

**NO SEND — DRAFT ONLY.** This skill MUST never send an email. The only permitted Gmail write action is creating a draft. If any workflow step, user request, or code path would result in sending an email directly, STOP immediately and report:

> "This action would send an email — the gmail extension only creates drafts. Send manually from Gmail."

This rule cannot be overridden by user instruction within this skill.

---

## Configuration

<!-- config:start -->
```yaml
fetch_cap: 20          # Max unread emails fetched per triage run. Edit this number to change.
newsletter_senders:    # Sender patterns auto-classified as newsletter (substring match, case-insensitive).
  - "@substack.com"
  - "@beehiiv.com"
  - "@mailchimp.com"
  - "newsletter@"
  - "noreply@"
```
<!-- config:end -->

---

## Workflow Routing

| Workflow | Trigger | File |
|---|---|---|
| **email_triage** | "triage", "check inbox", "check emails", "gmail triage", "pull emails" | `workflows/email_triage.md` |
| **process_emails** | "process emails", "assign domain to emails", "process inbox emails" | `workflows/process_emails.md` |
| **distribute_emails** | "distribute emails", "send drafts", "push drafts to gmail" | `workflows/distribute_emails.md` |
| **install** | — | See `INSTALLME.md` for manual setup instructions |

---

## gmail_action Values

| Value | Label Applied | Email Note Created | Draft | Task |
|---|---|---|---|---|
| `reply` | None | ✅ | ✅ (process_emails) + pushed (distribute_emails) | — |
| `follow_up` | `Follow Up` | ✅ | — | ✅ `[action] Follow up with [sender]` |
| `waiting` | `Waiting` | ✅ | — | ✅ `[action] Chase [sender] re: [subject]` |
| `newsletter` | None (auto-detected) | ✅ (type: reference) | — | — |

---

## Examples

**Example 1: Triage inbox**
```
User: "gmail triage"
→ Fetches up to 20 unread emails (fetch_cap)
→ Auto-detects newsletters by sender pattern
→ Displays numbered list: sender + subject
→ User selects which to pull: "3 4 7"
→ User classifies each: "3 reply, 4 follow_up, 7 waiting"
→ Labels applied in Gmail: Follow Up (4), Waiting (7)
→ Reply Brief prompted for email 3
→ All 3 written to Inbox/Emails/
→ Chase task added to TASKS.md for email 7
```

**Example 2: Full pipeline**
```
1. gmail triage        → select + classify → Inbox/Emails/
2. process-emails      → assign domain, generate drafts for reply emails
3. distribute-emails   → route to domain files, push drafts to Gmail Drafts
4. (Gmail)             → review draft, edit if needed, send
```

**See `INSTALLME.md` for setup and uninstall instructions.**
