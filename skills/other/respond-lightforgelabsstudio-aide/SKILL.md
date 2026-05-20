---
name: respond
description: Apply findings from a /findings review to an ADR and write a response file
---

# Respond

Handle the designer's side of the ADR review loop. Read findings, triage them, apply agreed changes, and write a response record.

Pairs with `/findings` (reviewer writes findings) and `/design` (designer writes ADR).

## Inputs

- Path to the ADR under review, or enough context to locate it
- The findings file must already exist alongside the ADR as `<slug>.findings.md`

## Workflow

1. **Locate files** — Find the ADR in `docs/decisions/` or `.aide/docs/decisions/`. Look for the sibling `<slug>.findings.md`. If not found, stop and tell the user.

2. **Read both files** — Read the ADR and the findings file in full.

3. **Triage findings** — For each finding, decide:
   - **Apply** — finding is correct, change the ADR
   - **Reject** — finding is incorrect or out of scope; record reasoning
   - **Defer** — valid but out of scope for this ADR; note where it should land

4. **Apply changes** — Edit the ADR for all accepted findings. Do not change the ADR status — the reviewer (`/findings`) owns that.

5. **Write response file** — Write `<slug>.response.md` alongside the ADR with this structure:
   ```
   # Review Response: <ADR Title>
   ## Applied
   ## Rejected
   ## Deferred
   ```
   Each entry cites the finding and gives a one-line reason.

6. **Confirm** — Report a summary of applied / rejected / deferred counts to the user.

## Reference

- ADR locations: `docs/decisions/` (game decisions), `.aide/docs/decisions/` (AIDE decisions)
- Findings file written by: `/findings`
