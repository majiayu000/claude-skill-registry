---
name: corporate-invoice
description: Handle corporate invoice and reimbursement requests. Use when a customer needs an invoice, VAT or tax info, or documentation for company reimbursement.
metadata:
  trigger_phrases:
      - "handle corporate"
      - "corporate invoice"
      - "invoice reimbursement"
  related_skills: ["team-license-purchase", "email-change", "invoice-billing-statement"]
  sample_size: "720"
  validation: |
    required_phrases:
      - "invoice"
      - "purchases page"
    forbidden_patterns:
      - "(?i)we can fill (out )?your tax form"
      - "(?i)we will fill (out )?your tax form"
      - "(?i)we can complete the .*tax form"
    max_length: 500
  metrics: "sample_size: 720\navg_thread_length: 3.73\ntop_phrases:\n  - phrase: \"let me know if\"\n    count: 232\n    percent: 32.2\n  - phrase: \"a fully customized invoice\"\n    count: 207\n    percent: 28.7\n  - phrase: \"fully customized invoice here\"\n    count: 205\n    percent: 28.5\n  - phrase: \"customized invoice here https\"\n    count: 205\n    percent: 28.5\n  - phrase: \"me know if you\"\n    count: 198\n    percent: 27.5\n  - phrase: \"view a fully customized\"\n    count: 197\n    percent: 27.4\n  - phrase: \"the prepared for section\"\n    count: 178\n    percent: 24.7\n  - phrase: \"you re logged in\"\n    count: 176\n    percent: 24.4\n  - phrase: \"to the prepared for\"\n    count: 173\n    percent: 24.0\n  - phrase: \"re logged in you\"\n    count: 172\n    percent: 23.9"
---
# Corporate Invoice

You're handling an invoice or billing request for corporate reimbursement.

## Common Scenarios

### "I need an invoice for my company"
After purchase, they can download and add company details from purchases page.

### "I need an invoice BEFORE I purchase"
We don't do pre-purchase invoices for individuals.
**Exception:** Large team orders (5+ seats).

### "What's your VAT number?"
We're US-based, no VAT. Can provide EIN or standard invoice.

### "Can you fill out this tax form?"
We don't fill foreign tax forms. Can provide our tax info document.

## Sub-categories

- Post-purchase invoice edits (company details, reimbursement)
- Pre-purchase invoice/pro forma requests
- VAT/EIN and tax info requests
- Foreign tax forms or residency certificate requests

## Phrases That Work

- "You can add details to your invoice and download it from your purchases page"
- "We're a US based company so we don't have a VAT number"
- "After purchasing we automatically create the invoice"
- "We don't create invoices pre-purchase unless it's for a larger team order"
- "We don't fill forms for foreign taxes"

## Key URLs

Direct customers to their purchases page to edit invoices:

| Product | Purchases URL |
|---------|---------------|
| Epic React | epicreact.dev/purchases |
| Total TypeScript | totaltypescript.com/purchases |
| Epic Web | epicweb.dev/purchases |
| Testing JavaScript | testingjavascript.com/purchases |

## Tone

- Helpful but clear about limitations
- No apologies needed for standard policies
- Direct them to self-service when possible
- Offer EIN as alternative to VAT

## What NOT To Do

- Don't create custom invoices for individual purchases
- Don't fill out foreign government tax forms
- Don't promise things that require manual work unless necessary

## Validation

Draft must:
- [ ] Provide a path forward (link or instructions)
- [ ] Be clear about limitations if declining
- [ ] NOT create custom invoices for individual purchases
