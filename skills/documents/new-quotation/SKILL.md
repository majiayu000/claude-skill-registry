---
name: new-quotation
description: Generate a Sentient.io-branded quotation by gathering client inputs, filling the Sentient Quotation template, and delivering the document into the correct Work Day Google Drive folder via the work-day skill.
---

# New Quotation Skill

Create production-ready sales quotations that adhere to Sentient.io's commercial standards and automatically land in the appropriate Work Day folder for record keeping.

## When to Use
- A user requests a "new quotation", "customer quote", or pricing proposal for a prospect
- Sales or delivery teams need a refreshed quotation aligned to the Sentient template
- A quotation must be stored in the SNMG18 Working Docs hierarchy alongside other daily files

## Required Inputs
Collect and confirm the following details before drafting the quotation:
- Client company name and primary contact details (name, role, email, phone)
- Opportunity or engagement name, objectives, and scope summary
- Proposed deliverables, milestones, and owners
- Pricing line items, quantities, unit prices, taxes, and payment terms
- Commercial assumptions, dependencies, and quotation validity period
- Requested delivery or kickoff timeline
- Target work day (defaults to today) for filing the quotation

If any information is missing, ask the user for clarification before proceeding.

## References & Assets
- Load `templates/sentient-quotation-template.md` to follow Sentient.io's structure, section ordering, and branding cues.
- For tone and visual consistency, optionally consult the `sentient-brand-guidelines` skill.
- Use the `work-day` skill to prepare the destination folder structure in Google Drive.

## Workflow

### 1. Confirm Scope & Inputs
1. Paraphrase the request to ensure alignment on the opportunity and deliverables.
2. Capture all required inputs in a structured checklist.
3. Highlight any gaps or assumptions and request confirmation.

### 2. Prepare Work Day Folder
1. Determine the work day date supplied by the user (or default to today).
2. Invoke the **work-day** skill to ensure the `YYYY-MM Work/YYYY-MM-DD` folder exists under `SNMG00 Management/SNMG18 Working Docs`.
3. Record the target folder link or ID for later use.

### 3. Draft the Quotation
1. Open the Sentient Quotation template file (`templates/sentient-quotation-template.md`).
2. Replace placeholder tokens (e.g., `{{client_company}}`, `{{total_amount}}`) with the confirmed inputs.
3. Maintain Sentient.io's professional, audit-ready tone:
   - Use confident yet consultative language.
   - Keep executive summary to ≤120 words.
   - Align currency and tax references with the user's region.
4. Ensure pricing tables total correctly and that taxes/fees are explicit.
5. Include acceptance table with client and Sentient signatories.

### 4. Create Google Doc Deliverable
1. Generate a document title using the pattern `Quotation - <Client> - <Engagement> - <YYYYMMDD>`.
2. Use Zapier's Google Docs integration to create a document from plain text:
   - Preferred action: `Zapier:google_docs_create_document_from_text` (or equivalent) with the assembled markdown converted to clean doc text.
   - Store the document temporarily in My Drive.
3. After creation, move the document into the prepared Work Day folder using Google Drive integration (`Zapier:google_drive_move_file` or create-in-folder option).
4. Set sharing to company-internal (view access) unless user specifies otherwise.

### 5. Deliver Summary Back to User
Provide a confirmation message that includes:
- Quotation title and Google Drive link
- Target work day folder path
- Summary of major sections (objectives, deliverables, total investment, validity)
- Any follow-up actions or outstanding assumptions

## Quality Checklist
Before responding to the user, verify that:
- [ ] All template placeholders have been replaced with real values or removed if not applicable
- [ ] Pricing totals sum correctly and match the described payment terms
- [ ] Assumptions and validity period are explicitly stated
- [ ] Document lives in the correct Work Day folder and shares appropriately
- [ ] Final response includes link, folder path, and concise recap

## Error Handling
- If the work-day skill cannot find/create the target folder, inform the user and pause until resolved.
- If Google Docs creation fails, supply the completed quotation content in-chat and note manual upload is required.
- If required inputs are missing after reasonable clarification attempts, summarize outstanding items instead of proceeding.

## Packaging Notes
- Store this skill definition at `new-quotation/skill.md`.
- Include the template file within `new-quotation/templates/` when packaging for deployment.
- Update repository README or catalog as needed when promoting this skill to production.
