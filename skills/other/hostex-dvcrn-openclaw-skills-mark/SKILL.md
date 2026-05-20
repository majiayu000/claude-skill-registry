---
name: hostex
description: "Hostex (hostex.io) OpenAPI v3.0 skill for querying and managing vacation rental properties, room types, reservations, availability, listing calendars, guest messaging, reviews, and webhooks via the Hostex API. Use when you need to integrate with Hostex API using a Hostex PAT (Hostex-Access-Token / HostexAccessToken) or when you need safe, intent-level API calls (read-only by default, optional write operations with explicit confirmation)."
---

# Hostex API Skill (Node)

## Auth (PAT)

- Set env var: `HOSTEX_ACCESS_TOKEN`
- Requests use header: `Hostex-Access-Token: <PAT>`
- OpenAPI security scheme name: `HostexAccessToken`

**Default recommendation:** use a **read-only** PAT.

## Dates / timezone

- All date params are `YYYY-MM-DD`
- Interpret dates in **property timezone** (no UTC timestamps)

## OpenAPI source of truth

Stable OpenAPI JSON:
- https://hostex.io/open_api/v3/config.json

Use `scripts/openapi-sync.mjs` to cache a local copy into `references/openapi.json`.

## Quick commands (scripts)

All scripts expect `HOSTEX_ACCESS_TOKEN`.

### Read-only (safe)

List properties:
```bash
node skills/hostex/scripts/hostex-read.mjs list-properties --limit 20
```

List reservations (by check-in range):
```bash
node skills/hostex/scripts/hostex-read.mjs list-reservations --start-check-in-date 2026-02-01 --end-check-in-date 2026-02-28 --limit 20
```

List reservations (by reservation code):
```bash
node skills/hostex/scripts/hostex-read.mjs list-reservations --reservation-code 0-1234567-abcdef
```

Get availability:
```bash
node skills/hostex/scripts/hostex-read.mjs get-availabilities --start 2026-02-10 --end 2026-02-20 --property-id 123
```

### Writes (guarded)

Writes are disabled unless:
- `HOSTEX_ALLOW_WRITES=true`

and you pass `--confirm`.

Send message:
```bash
HOSTEX_ALLOW_WRITES=true node skills/hostex/scripts/hostex-write.mjs send-message --conversation-id 123 --text "Hello!" --confirm
```

Update listing prices (single range example):
```bash
HOSTEX_ALLOW_WRITES=true node skills/hostex/scripts/hostex-write.mjs update-listing-prices \
  --channel-type airbnb \
  --listing-id 456 \
  --start 2026-02-10 \
  --end 2026-02-15 \
  --price 199 \
  --confirm
```

Update listing prices (multi-range in one request):
```bash
HOSTEX_ALLOW_WRITES=true node skills/hostex/scripts/hostex-write.mjs update-listing-prices \
  --channel-type booking_site \
  --listing-id 100541-10072 \
  --prices "2026-02-03..2026-02-05:599,2026-02-06..2026-02-07:699,2026-02-08..2026-02-09:599" \
  --confirm
```

Create reservation (Direct Booking) (example):
```bash
HOSTEX_ALLOW_WRITES=true node skills/hostex/scripts/hostex-write.mjs create-reservation \
  --property-id 123 \
  --custom-channel-id 77 \
  --check-in-date 2026-02-10 \
  --check-out-date 2026-02-12 \
  --guest-name "Alice" \
  --currency USD \
  --rate-amount 200 \
  --commission-amount 0 \
  --received-amount 200 \
  --income-method-id 3 \
  --confirm
```

Update property availabilities (close/open) (example):
```bash
# Close a property for a date range
HOSTEX_ALLOW_WRITES=true node skills/hostex/scripts/hostex-write.mjs update-availabilities \
  --property-ids "11322075" \
  --available false \
  --start-date 2026-02-03 \
  --end-date 2027-02-02 \
  --confirm
```

## Operational guardrails (mandatory)

When doing any write operation:
1) **Summarize the change** (who/what/when/how much).
2) Require the user to explicitly confirm (e.g. `CONFIRM`).
3) Prefer `--dry-run` first if available.

## Notes

- Pagination: endpoints commonly accept `offset` + `limit` (limit max 100).
- Never print tokens in logs; scripts redact secrets automatically.
