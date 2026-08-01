---
name: spec-pdf-to-schema
description: Ensure protocol facts derived from MIDI spec PDFs are reflected in canonical
  JSON schema/OpenAPI sources.
---

# Spec PDF to Schema Mapping

## Purpose
Ensure protocol facts derived from MIDI spec PDFs are reflected in canonical JSON schema/OpenAPI sources.

## When to Use
- Implementing protocol details sourced from PDF specifications
- Updating schema or OpenAPI definitions

## Steps
1. Render the relevant PDF pages to images for inspection.
2. Validate the bit layout or field definitions against the images.
3. Update `midi2.full.closed.schema.json` and `midi2.full.openapi.json` with the verified facts.
4. Implement code and tests only after schema/OpenAPI updates.
5. Document the source page/section in related notes or audit docs.

## Output Contract
- Canonical JSON schema/OpenAPI reflect the PDF-derived facts.
- Code/tests align with the updated canonical sources.
