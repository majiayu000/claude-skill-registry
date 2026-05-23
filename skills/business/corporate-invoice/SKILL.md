---
name: corporate-invoice
description: |
  Invoice and billing requests for corporate reimbursement. Triggers on "invoice",
  "VAT", "tax info", "company purchase", "expense report", "reimbursement".
sample_size: 720
validation:
  forbidden_patterns:
    - "(?i)we can fill (out )?your tax form"
    - "(?i)we will fill (out )?your tax form"
    - "(?i)we can complete the .*tax form"
metrics:
  sample_size: 720
  avg_thread_length: 3.73
  top_phrases:
    - phrase: "let me know if"
      count: 232
      percent: 32.2
    - phrase: "a fully customized invoice"
      count: 207
      percent: 28.7
    - phrase: "fully customized invoice here"
      count: 205
      percent: 28.5
    - phrase: "customized invoice here https"
      count: 205
      percent: 28.5
    - phrase: "me know if you"
      count: 198
      percent: 27.5
    - phrase: "view a fully customized"
      count: 197
      percent: 27.4
    - phrase: "the prepared for section"
      count: 178
      percent: 24.7
    - phrase: "you re logged in"
      count: 176
      percent: 24.4
    - phrase: "to the prepared for"
      count: 173
      percent: 24.0
    - phrase: "re logged in you"
      count: 172
      percent: 23.9
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
