---
name: vcr-record
description: Record, validate, update, and clean VCR cassettes for BioETL HTTP tests with secret-safety checks.
---

# VCR Record

## Objective
Manage VCR cassette lifecycle for provider integration tests.

## Source Of Truth
- Primary instructions: `../../../.claude/skills/vcr-record.md`

## Workflow
1. Open and follow `../../../.claude/skills/vcr-record.md`.
2. Adapt shell examples to the current environment when needed.
3. Always include cassette validation and secret sanitization checks.
4. Prefer repository-local commands (`uv run ...`) consistent with project standards.

## Notes
- The `.claude` skill file contains the canonical action modes (`record`, `list`, `validate`, `update`, `clean`).
