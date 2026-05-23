---
name: holded-invoices
description: "Process invoice emails: download PDF attachments, extract vendor + date, generate normalized filename, and send to Holded inbox via n8n webhook."
---

# Holded invoices (Gmail → PDF → n8n webhook → Holded inbox)

Goal: when an email contains an invoice PDF, upload it to Holded via an n8n webhook.

## Destinations

Configure defaults in `~/.config/skills/config.json` under `holded_invoices`:
- `company_email`
- `freelancer_email`
- `webhook`

Example:
```json
{
  "holded_invoices": {
    "company_email": "empresa@holdedbox.com",
    "freelancer_email": "autonomo@holdedbox.com",
    "webhook": "https://n8n.example.com/webhook/..."
  }
}
```

Webhook fields:
- `email` (Holded inbox) (HTTP header)
- `nombre` (base filename, without extension) (HTTP header)
- Body: raw PDF (`Content-Type: application/pdf`)

Filename convention:
- `<company>-<YYYY>-<MM>.pdf`
- Vendor slug: lowercased, spaces → dashes, simplified (e.g. "Google INC" → `google`).

## Scripts

### 1) Extract vendor + date from a PDF

- `scripts/invoice-extract.js --pdf /path/to/invoice.pdf`
  - Outputs JSON: `{ vendor, vendorSlug, year, month }`

### 2) Upload a PDF to Holded via n8n

- `scripts/holded-upload.sh --pdf /path/to/invoice.pdf --email <holdedbox> --nombre google-2026-01.pdf`
  - If not configured, pass `--webhook` explicitly.

### 3) End-to-end: from a Gmail message ID

Downloads the first PDF attachment, suggests a filename, and (optionally) uploads.

- `scripts/holded-from-gmail.sh --account <gmail-account> --message-id <id> --type empresa|autonomo`
  - If not configured, pass `--email-empresa`, `--email-autonomo`, and/or `--webhook`.

Flags:
- `--yes` skip confirmation and upload

## Agent workflow

When reviewing an email thread with a PDF invoice:
1) Ask: is it `empresa` or `autonomo`.
2) Download the PDF attachment.
3) Run `invoice-extract.js` to infer vendor + year/month.
4) Propose filename and ask for confirmation.
5) Call webhook via `holded-upload.sh`.

If extraction fails, ask for vendor + date and continue.
