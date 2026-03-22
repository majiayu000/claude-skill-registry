---
name: duffel
description: "Search, book, and manage flights via the Duffel Flights API. Covers 300+ airlines (NDC, GDS, LCC). Use when: (1) searching for flights between cities, (2) comparing prices and fare classes, (3) booking flights, (4) checking booking status, (5) cancelling bookings, (6) viewing seat maps, (7) looking up airport/city IATA codes. Supports one-way, round-trip, multi-passenger, cabin class filtering, and nonstop preferences."
---

# Duffel Flights

Search, book, and manage flights across 300+ airlines via the Duffel API.

## Setup

Set `DUFFEL_TOKEN` env var with your Duffel API access token.
Get one at https://app.duffel.com → Developers → Access Tokens.
Test tokens (prefix `duffel_test_`) use sandbox data with unlimited balance.

## Commands

### Search flights
```bash
python scripts/duffel.py search --from MIA --to LHR --date 2026-04-15
python scripts/duffel.py search --from MIA --to CDG --date 2026-03-15 --return-date 2026-03-22 --cabin business
python scripts/duffel.py search --from JFK --to LAX --date 2026-05-01 --nonstop --adults 2
```

Options: `--cabin economy|premium_economy|business|first`, `--nonstop`, `--adults N`, `--children N`, `--infants N`, `--sort price|duration`, `--max-results N`, `--json`

Results are numbered. Use the number with other commands.

### View offer details
```bash
python scripts/duffel.py offer 3
```
Shows segments, baggage, fare conditions (refund/change), available extras.

### Book a flight
```bash
python scripts/duffel.py book 3 --pax "RIBEIRO/FABIO MR 1977-01-31 fabio@ribei.ro +13059159687 BR m"
```
Pax format: `LAST/FIRST TITLE DOB EMAIL PHONE NATIONALITY GENDER`
- TITLE: MR, MRS, MS, MISS, DR
- GENDER: m or f
- Multiple passengers: repeat `--pax "..."` for each

Payment uses Duffel account balance. Top up at https://app.duffel.com.

### Check order status
```bash
python scripts/duffel.py order ord_0000XXXXX
```

### Cancel order
```bash
python scripts/duffel.py cancel ord_0000XXXXX           # Quote (shows refund amount)
python scripts/duffel.py cancel ord_0000XXXXX --confirm  # Execute cancellation
```

### Seat map
```bash
python scripts/duffel.py seatmap 3
```

### Airport/city lookup
```bash
python scripts/duffel.py places "new york"
```

## Typical workflow

1. `search` → browse numbered results
2. `offer N` → check details, baggage, conditions
3. `book N --pax "..."` → get PNR
4. `order <id>` → verify booking
5. `cancel <id>` → if needed

## Notes

- Offers expire (usually ~20 min). Re-search if expired.
- Test mode: unlimited balance, bookings on "Duffel Airways" (fake airline).
- Production: real airlines, real tickets. Balance must be funded.
- All commands support `--json` for raw API output.
- Last search saved to `/tmp/duffel-last-search.json` for index reference.
- For API details, see `references/api-guide.md` and `references/booking-flow.md`.
