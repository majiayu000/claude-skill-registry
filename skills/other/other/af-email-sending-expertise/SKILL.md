---
name: af-email-sending-expertise
description: Use when sending emails from Claude/AgentFlow via Gmail API. Covers service account authentication, composing messages with attachments, and delivery via holly@gaininsight.global.

# AgentFlow documentation fields
title: Email Sending Expertise
created: 2026-02-06
updated: 2026-02-06
last_checked: 2026-02-06
tags: [skill, expertise, email, gmail, sending, attachments]
parent: ../README.md
related:
  - ../af-quotation-expertise/SKILL.md
  - ../af-comms-expertise/SKILL.md
---

# Email Sending Expertise

## When to Use This Skill

Load this skill when you need to:
- Send an email from Claude/AgentFlow (e.g. quotation PDFs, reports, notifications)
- Compose emails with file attachments
- Send as `holly@gaininsight.global`

**Common triggers:**
- Quotation skill needs to email a PDF to a recipient
- Any workflow that produces a document for external delivery

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Sender address | `holly@gaininsight.global` |
| Sender name | Holly (AgentFlow) |
| Service account | `gmail-testing@gam-workspace-481110.iam.gserviceaccount.com` |
| Credentials | Doppler: `gi` project, `prd` config, `GMAIL_TESTING_SERVICE_ACCOUNT` |
| Required scope | `https://www.googleapis.com/auth/gmail.send` |
| Impersonate user | `holly@gaininsight.global` |
| API | Gmail API v1 |
| Server docs | `/srv/docs/GMAIL_TESTING.md` |

---

## Rules

1. **Always send as holly@gaininsight.global.** This is the authorised sender identity.
2. **Get credentials from Doppler.** Never hardcode or cache service account keys.
3. **Clean up credential files.** Delete temporary credential files after use.
4. **Include a clear subject line.** Recipients should know what the email contains.
5. **Always confirm delivery to the user.** Report success or failure.

---

## Workflow: Send an Email with Attachment

**When:** You need to email a file (PDF, report, etc.) to a recipient.

**Procedure:**

### Step 1: Get Credentials

```bash
sudo -u tmux-shared doppler secrets get GMAIL_TESTING_SERVICE_ACCOUNT --project gi --config prd --plain > /tmp/gmail-sa.json
```

### Step 2: Send the Email

Use a Node.js script (googleapis is already installed, or install with `npm install googleapis`):

```javascript
const { google } = require('googleapis');
const fs = require('fs');
const path = require('path');

async function sendEmail({ to, subject, body, attachmentPath }) {
  const credentials = JSON.parse(fs.readFileSync('/tmp/gmail-sa.json', 'utf8'));

  const auth = new google.auth.GoogleAuth({
    credentials,
    scopes: ['https://www.googleapis.com/auth/gmail.send'],
    clientOptions: {
      subject: 'holly@gaininsight.global'
    }
  });

  const gmail = google.gmail({ version: 'v1', auth });

  // Build MIME message
  const attachment = fs.readFileSync(attachmentPath);
  const encodedAttachment = attachment.toString('base64');
  const filename = path.basename(attachmentPath);

  const boundary = 'boundary_' + Date.now();
  const mimeMessage = [
    `From: Holly <holly@gaininsight.global>`,
    `To: ${to}`,
    `Subject: ${subject}`,
    `MIME-Version: 1.0`,
    `Content-Type: multipart/mixed; boundary="${boundary}"`,
    '',
    `--${boundary}`,
    'Content-Type: text/plain; charset="UTF-8"',
    '',
    body,
    '',
    `--${boundary}`,
    `Content-Type: application/pdf; name="${filename}"`,
    'Content-Transfer-Encoding: base64',
    `Content-Disposition: attachment; filename="${filename}"`,
    '',
    encodedAttachment,
    `--${boundary}--`
  ].join('\r\n');

  const encodedMessage = Buffer.from(mimeMessage)
    .toString('base64')
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=+$/, '');

  const res = await gmail.users.messages.send({
    userId: 'me',
    requestBody: { raw: encodedMessage }
  });

  return res.data;
}
```

### Step 3: Clean Up

```bash
rm -f /tmp/gmail-sa.json
```

---

## Workflow: Send a Plain Text Email

For emails without attachments, use a simpler MIME message:

```javascript
const mimeMessage = [
  `From: Holly <holly@gaininsight.global>`,
  `To: ${to}`,
  `Subject: ${subject}`,
  'Content-Type: text/plain; charset="UTF-8"',
  '',
  body
].join('\r\n');
```

---

## Integration Points

**Quotation skill** (af-quotation-expertise):
- Sends generated PDF quotations to recipients
- Subject format: `Quotation {REFERENCE} — {Project/Feature Name}`

**Communications** (af-comms-expertise):
- Zulip for team notifications, Gmail for external delivery
- Use Zulip for internal updates, email for client-facing documents

**Server docs:**
- Full Gmail API setup: `/srv/docs/GMAIL_TESTING.md`
- Google Workspace admin: `/srv/docs/GAM.md`

---

## Common Pitfalls

1. **Forgetting to impersonate.** Must set `subject: 'holly@gaininsight.global'` in auth options — without this, the service account can't send.
2. **Leaving credentials on disk.** Always `rm /tmp/gmail-sa.json` after sending.
3. **Large attachments.** Gmail API has a ~25MB limit per message. For larger files, use a download link instead.
4. **Missing googleapis package.** Not installed globally. Create a temp directory and install: `mkdir -p /tmp/email-test && cd /tmp/email-test && npm init -y && npm install googleapis`. Run scripts from that directory.

---

**Remember:**
1. Send as `holly@gaininsight.global` via Gmail API service account
2. Credentials from Doppler — never hardcode
3. Clean up credential files after use
4. Confirm delivery success/failure to the user
