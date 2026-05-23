---
name: flight-fare-flex
description: Flexible-date flight fare finder for routes like NYC to SFO. Use when the user asks for cheapest flights, lowest fare in a date range, best travel dates, or fare comparison across a period. Default behavior is round-trip and nonstop unless the user explicitly asks otherwise. Produces ranked options with dates, price signals, and booking links.
metadata: {"openclaw":{"emoji":"✈️","os":["darwin","linux"],"requires":{"bins":["node"]}}}
---

# Flight Fare Flex

Use this skill for airfare requests where the user wants low prices with flexible dates.
Default policy is `balanced`: show price when available, but mark confidence.
Execution policy is `live API first (Amadeus if configured)`, then fallback to web-estimated mode.

## Inputs

Collect these fields first:

- `from`: origin city/airport code (e.g., `NYC`, `JFK`)
- `to`: destination city/airport code (e.g., `SFO`)
- `start`: start date (`YYYY-MM-DD`)
- `end`: end date (`YYYY-MM-DD`)
- optional: `trip` = `round` or `oneway` (default `round`)
- optional: `stops` = `nonstop` or `any` (default `nonstop`)
- optional: `price-mode` = `strict` or `balanced` or `aggressive` (default `balanced`)
- optional: `provider` = `auto` or `amadeus` or `ddg` (default `auto`)
- optional: `adults` = `1..9` (default `1`)
- optional: `cabin` = `economy` | `premium_economy` | `business` | `first` (default `economy`)
- optional: `recheck-top` = re-validate top live results once (default `3`)
- optional (round trip): `stay-min` and `stay-max` nights (default `3` and `7`)

## Command

```bash
node "{baseDir}/scripts/flex_flight_search.mjs" \
  --from "NYC" --to "SFO" \
  --start "2026-03-10" --end "2026-03-25" \
  --trip round --stops nonstop --price-mode balanced --provider auto \
  --adults 1 --cabin economy --recheck-top 3 \
  --stay-min 3 --stay-max 7 --max-itins 12 --json
```

Parameter note:
- Both kebab-case and snake_case are accepted for these options: `price-mode/price_mode`, `recheck-top/recheck_top`, `stay-min/stay_min`, `stay-max/stay_max`, `max-itins/max_itins`.

## Response policy

- Return top 3-5 cheapest options first.
- Include: dates, detected price, price type, provider, and Google Flights link.
- Keep default as round-trip + nonstop unless user explicitly requests otherwise.
- If user request is vague (e.g., "find cheap flights") or required fields are missing, provide command presets first using:
  `node "{baseDir}/scripts/flex_flight_search.mjs" --examples`
- `strict`: only high-confidence live-looking prices.
- `balanced` (default): prefer strict, then fallback to estimated price.
- `aggressive`: prioritize always showing a numeric estimate if detectable.
- Expose `liveProviderAvailable` and `generatedAt` in JSON output for traceability.
- If exact price extraction fails, say so clearly and still return usable booking links.
- Never claim a confirmed fare unless a numeric price was actually detected.

## Live Provider Setup (Optional but Recommended)

Set these environment variables to enable live API pricing:

- `AMADEUS_CLIENT_ID`
- `AMADEUS_CLIENT_SECRET`
- optional: `AMADEUS_BASE_URL` (defaults to Amadeus test endpoint)

## Safety

- Do not bypass login/paywall/captcha.
- Do not perform bookings or payments without explicit user approval.
