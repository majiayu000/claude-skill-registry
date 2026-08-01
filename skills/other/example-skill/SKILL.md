---
name: transmittal
description: Log an outgoing transmittal — turn a list of files and a recipient into a numbered record of what was sent, to whom, when, and why. Use when the user asks to record a transmittal, log an issuance, or says "we sent the drawings to the contractor".
allowed-tools:
  - Read
  - Write
  - Glob
---

# /transmittal — Transmittal Records

You log what left the office: one numbered record per transmittal, in `transmittals/` at the project root. The record outlives the email it rode on.

## Usage

```
/transmittal sent the 50% CD set to the structural engineer for review
/transmittal issued A-101 through A-110 to the GC via file share
```

## Steps

1. Find the next number: Glob `transmittals/*.md`, take max + 1, zero-padded to 4 digits.
2. Pull the pieces from the request: recipient (role or firm), files sent, purpose, method. If the request names real paths, confirm they exist in the project; note `not verified` for any that can't be found.
3. Write `transmittals/NNNN-{recipient-slug}.md` in the format below. Anything the request didn't state, record as `not recorded` — never guess.
4. Confirm with the path and a one-line restatement: who got what, and why.

## Output format

```markdown
# Transmittal NNNN — {recipient role or firm}

- **Date:** {YYYY-MM-DD}
- **To:** {recipient role or firm}
- **Via:** {email | file share | courier | not recorded}
- **Purpose:** {for review | for record | for construction | not recorded}

| # | File | Description |
|---|------|-------------|
| 1 | {filename} | {one line} |

Notes: {anything else worth keeping, or omit the line}
```
