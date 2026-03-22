---
name: email
description: Manage inbox email. Uses the inbox script and stores metadata (ids) to open or archive messages later.
---

# Email (inbox)

## Goal
List Gmail/iCloud inboxes showing a clean user view while preserving metadata (IDs) for later actions.

## Base command
- Helper in the skill: `scripts/email-inbox`
- Always pass `--json-out` to save metadata.
- Configure accounts in `~/.config/skills/config.json` under `email`:
  - `gmail_accounts`: list of Gmail accounts
  - `icloud_user`: iCloud user (optional)

Example:
```json
{
  "email": {
    "gmail_accounts": ["you@gmail.com", "other@gmail.com"],
    "icloud_user": "you@icloud.com"
  }
}
```

Example:
```
scripts/email-inbox
```

## Flow
1) Run the command with `--json-out /tmp/inbox.json`.
2) Show the user ONLY the clean output (numbered list), using the agreed format (see "Output format").
3) Read `/tmp/inbox.json` to get IDs and keep them for later actions.
4) Propose recommended actions (archive/open/reply/wait) using your own judgment; ask for confirmation before acting.

Helpers (from the skill folder):
- `scripts/email-open --index <n>` (Gmail/iCloud) opens and writes `/tmp/email-open.json`.
- `scripts/email-archive --index <n>` (Gmail/iCloud) archives the message/thread. Accepts multiple indices.
- `scripts/email-reply --index <n> --body-file <path>` replies to the message (Gmail/iCloud).
- `scripts/email-mailboxes --account <icloud>` lists iCloud mailboxes.

## Metadata format
The JSON contains a list of items with:
- `index` (number shown to the user)
- `source` (`gmail` or `icloud`)
- `account`
- `id` (Gmail: threadId, iCloud: UID)
- `from`
- `subject`

## Open an email (Gmail)
Use the helper:
```
scripts/email-open --index <n>
```
This prints the email (from/subject/date/body) and saves metadata to `/tmp/email-open.json`.

## Reply to an email (Gmail/iCloud)
Before sending, **always** show the draft to the user and ask for explicit approval.

Use the helper:
```
scripts/email-reply --index <n> --body-file /tmp/reply.txt
```

- If you need to reply-all (Gmail), add `--reply-all`.
- To force a subject: `--subject "Re: ..."`
- iCloud replies via SMTP with the same app password and **stores a copy in Sent**.
- To save to Sent without sending (already sent): `--append-only`.
- To avoid saving to Sent: `--no-append-sent`.
- By default it replies-all and keeps CC. To reply only to the sender: `--no-reply-all`.
- After sending a reply, archive the thread with `scripts/email-archive --index <n>` to keep the inbox clean.

## Archive an email (Gmail)
Use the helper:
```
scripts/email-archive --index <n>
```
Examples:
```
scripts/email-archive --index 1 --index 2 --index 3
scripts/email-archive --index 1,2,3,4,9,10
```

## iCloud (current state)
- List: supported by `inbox`.
- Open: supported by `scripts/email-open --index <n>` (uses UID).
- Archive: supported by `scripts/email-archive --index <n>`.
  - If it cannot detect the archive mailbox, use `--mailbox "<Name>"`.
  - To list mailbox names: `scripts/email-mailboxes --account <icloud>`.

## Missing context
- If the JSON is stale or missing, run inbox again with `--json-out`.

## Notes
- The script may prompt for the iCloud password if env vars are missing.
- Avoid showing IDs to the user; only show the clean list.

## Output format
- Separate by account (Gmail/iCloud) while keeping the absolute numbering.
- Account header in bold: `📧 **<account>**`.
- Separator line after the header: `—`.
- Use emojis before each message with this legend:
  - 🔍 open
  - 🗂️ archive
  - 👀 review
  - ⏳ wait
- Do not bold the sender; bold is only for the account header.

## Optional triage rules
If the user notices failures, add specific rules in `rules.json` to refine future recommendations.

### Active rules
Rules live in `rules.json` inside this skill (single source of truth).
