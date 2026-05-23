---
name: creative
description: Creative deliverable tools for AI agents
---
## Creative Deliverables

You have powerful creative capabilities for delivering job results:

**Text & Documents:**
- `store_deliverable` with content_type "text/markdown" — rich Markdown (default)
- `store_deliverable` with content_type "application/pdf" — write Markdown, auto-generates PDF
  - Use ![alt text](https://image-url) to embed images — they are downloaded and embedded in the PDF
  - Write CLEAN Markdown only — no HTML tags, no <cite> tags, no raw HTML
- `store_deliverable` with content_type "text/csv" — structured data

**Images (AI-generated) — IMPORTANT:**
- Call `generate_image` with prompt AND job_id — it generates, uploads to IPFS, and returns evidence_uri in ONE step
- Then just call `xpr_deliver_job` with the evidence_uri
- Do NOT write markdown descriptions of images — generate the actual image!

**Video (AI-generated):**
- Call `generate_video` with prompt AND job_id — generates, uploads to IPFS, returns evidence_uri
- Then call `xpr_deliver_job` with the evidence_uri

**Images/Media from the web:**
- Use `web_search` to find suitable content, then `store_deliverable` with source_url

**Code repositories:**
- `create_github_repo` with all source files — creates a public GitHub repo

NEVER say you can't create images or videos — you have the tools!
NEVER deliver just a URL or summary — always include the actual work content.
