---
name: auto-dev
description: Use when working with Auto.dev APIs, vehicle data, VIN decoding, car listings, vehicle photos, specs, recalls, payments, interest rates, taxes, OEM build data, plate-to-VIN, or any automotive data API calls
version: 1.0.2
tags:
  - automotive
  - vehicle-data
  - vin
  - listings
  - api
  - auto-dev
  - car-search
  - recalls
homepage: https://github.com/drivly/auto-dev-skill
metadata:
  openclaw:
    requires:
      env:
        - AUTODEV_API_KEY
    primaryEnv: AUTODEV_API_KEY
---

# Auto.dev API

V2 is the primary API. V1 provides supplemental endpoints with no V2 equivalent.

## Authentication

Check for `AUTODEV_API_KEY` environment variable first. If not set, ask: "Do you have an Auto.dev API key?"

- **If yes:** Ask them to paste it or set it with `export AUTODEV_API_KEY="your-key-here"`
- **If no:** Direct them to https://www.auto.dev/pricing to sign up (free Starter plan available)

**V2** (base: `https://api.auto.dev`): `Authorization: Bearer {key}` or `?apiKey={key}`
**V1** (base: `https://auto.dev/api`): `?apikey={key}` (query string only)

## API Reference — Copy These URLs

Use these exact URL patterns. Do NOT guess parameter names — wrong params return 400.

**Search Listings** (Starter)
```
GET https://api.auto.dev/listings?vehicle.make=Audi&vehicle.model=R8&retailListing.price=1-60000&retailListing.state=FL&limit=100&page=1&apiKey={key}
```
More filters: `vehicle.year=2022-2024`, `vehicle.bodyStyle=SUV`, `vehicle.drivetrain=AWD`, `retailListing.miles=1-50000`, `zip=33132&distance=50`. See v2-listings-api.md for all filters.

**Single Listing** (Starter)
```
GET https://api.auto.dev/listings/{vin}?apiKey={key}
```

**VIN Decode** (Starter)
```
GET https://api.auto.dev/vin/{vin}?apiKey={key}
```

**Vehicle Photos** (Starter)
```
GET https://api.auto.dev/photos/{vin}?apiKey={key}
```

**Specifications** (Growth)
```
GET https://api.auto.dev/specs/{vin}?apiKey={key}
```

**OEM Build Data** (Growth — $0.10/call)
```
GET https://api.auto.dev/build/{vin}?apiKey={key}
```

**Vehicle Recalls** (Growth)
```
GET https://api.auto.dev/recalls/{vin}?apiKey={key}
```

**Total Cost of Ownership** (Growth)
```
GET https://api.auto.dev/tco/{vin}?zip=33132&apiKey={key}
```

**Vehicle Payments** (Growth) — `price` and `zip` are required
```
GET https://api.auto.dev/payments/{vin}?price=39520&zip=33132&downPayment=5000&loanTerm=60&apiKey={key}
```

**Interest Rates** (Growth) — `year`, `make`, `model`, `zip`, `creditScore` are required
```
GET https://api.auto.dev/apr/{vin}?year=2024&make=Audi&model=R8&zip=33132&creditScore=720&apiKey={key}
```

**Open Recalls** (Scale)
```
GET https://api.auto.dev/openrecalls/{vin}?apiKey={key}
```

**Plate-to-VIN** (Scale — $0.55/call)
```
GET https://api.auto.dev/plate/{state}/{plate}?apiKey={key}
```

**Taxes & Fees** (Scale) — `price` and `zip` are required
```
GET https://api.auto.dev/taxes/{vin}?price=39520&zip=33132&apiKey={key}
```

### V1 Supplemental (No V2 Equivalent)

```
GET https://auto.dev/api/models?apikey={key}
GET https://auto.dev/api/cities?apikey={key}
GET https://auto.dev/api/zip/{zip}?apikey={key}
GET https://auto.dev/api/autosuggest/{term}?apikey={key}
```

### Parameters That Do NOT Exist (Will Return 400)

```
make=          ← use vehicle.make
model=         ← use vehicle.model
_order=        ← no sort parameter exists
sort=          ← no sort parameter exists
rows=          ← use limit
state=         ← use retailListing.state
price=         ← use retailListing.price (on /listings), or price= (on /payments, /taxes)
```

## Plans & Pricing

See pricing.md for full per-call costs and upgrade links.

| Plan | Monthly | Includes |
|------|---------|----------|
| Starter | Free + data fees | VIN Decode, Listings, Photos (1,000 free calls/mo) |
| Growth | $299/mo + data fees | + Specs, Recalls, TCO, Payments, APR, Build |
| Scale | $599/mo + data fees | + Open Recalls, Plate-to-VIN, Taxes & Fees |

All plans charge per-call data fees on every request. Growth/Scale have no cap on volume but data fees still apply.

## Important Rules

- **Before batch operations**, call the endpoint once with a single item to see the actual response shape. Do not guess field names or nesting — inspect the real response first.
- **Include ALL fields** from the API response unless the user explicitly says to exclude some.
- **Small results** (<10 items, single VIN): Display inline as formatted table
- **Large results** (10+ listings): Ask user preference, default to CSV export
- **Always support**: CSV, JSON export when user requests
- **Chain APIs** when the query spans multiple endpoints

## Deep Reference

**API Docs:** v2-listings-api.md | v2-vin-apis.md | v2-plate-api.md | v1-apis.md
**Workflows:** chaining-patterns.md | interactive-explorer.md | business-workflows.md
**Code Gen:** code-patterns.md | app-scaffolding.md | integration-recipes.md
**Other:** error-recovery.md | pricing.md | examples.md
