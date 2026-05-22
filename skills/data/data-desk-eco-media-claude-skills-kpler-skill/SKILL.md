---
name: kpler
description: Use when fetching oil/gas trade flow data from Kpler. Covers authentication, trade queries, flow aggregations, entity search, vessel positions, and company fleet data.
---

# Kpler Trade Data API

Access oil and gas trade flows, vessel tracking, and company data from the Kpler terminal.

## Prerequisites

1. **Kpler account** with terminal access
2. Store credentials in `.env`:

```bash
KPLER_USERNAME=user@example.com
KPLER_PASSWORD=your_password
```

## Setup

Copy the client module to your project:

```bash
cp .claude/skills/kpler/scripts/kpler_client.py scripts/
```

Install dependencies:

```bash
uv add httpx pyjwt python-dotenv
```

## Quick start

```python
import asyncio
from kpler_client import KplerClient

async def main():
    async with KplerClient() as client:
        # Search for a player
        results = await client.search("shell", categories=["PLAYER"])
        shell_id = results["players"][0]["entity"]["id"]

        # Query their trades
        trades = await client.query_trades(players=[shell_id], size=20)
        print(f"Found {len(trades['result']['trades'])} trades")

asyncio.run(main())
```

## Authentication

The client handles Auth0 OAuth automatically:

- Auto-login from `.env` credentials
- Token storage in `.kpler_token`, `.kpler_refresh_token`
- Automatic refresh 5 minutes before expiry
- Retry on 401 with fresh token

Manual auth control:

```python
client = KplerClient()
await client.login("user@example.com", "password")  # Manual login
client.is_authenticated()  # Check status
await client.logout()  # Clear tokens
```

## API methods

### Search entities

Find players, vessels, installations, zones, and products by name:

```python
results = await client.search(
    text="gazprom",
    categories=["PLAYER", "INSTALLATION"],  # Optional filter
    commodity_types=["lng"],  # Optional: lng, oil, lpg, dry
)

# Results grouped by type
for player in results.get("players", []):
    print(f"{player['entity']['name']} (ID: {player['entity']['id']})")
```

**Categories:** `PLAYER`, `VESSEL`, `INSTALLATION`, `ZONE`, `PRODUCT`

### Query trades

Get individual trade records:

```python
trades = await client.query_trades(
    # Pagination
    from_=0,
    size=100,

    # Filters (use IDs from search - strings work, converted to ints)
    locations=[1234],  # Zone/installation IDs
    products=[5678],   # Product IDs
    players=[3836],    # Company IDs
    vessels=[9012],    # Vessel IDs

    # Trade status
    statuses=["completed"],  # ongoing, completed, cancelled
    trade_types=["import", "export"],

    # Options
    with_forecasted=False,
)

for trade in trades["data"]:
    origin = trade.get("portCallOrigin", {}).get("zone", {}).get("name", "Unknown")
    dest = trade.get("portCallDestination", {}).get("zone", {}).get("name", "Unknown")
    print(f"{origin} → {dest}")
```

### Query flows (aggregated)

Get aggregated flow data with time series:

```python
flows = await client.query_flows(
    # Required
    direction="export",  # export, import
    granularity="months",  # years, months, weeks, days

    # Date range
    start_date="2024-01-01",
    end_date="2024-12-31",

    # Filters
    locations=[1234],
    products=[5678],
    players=[3836],

    # Split results by dimension
    split_on="countries",  # countries, ports, products, vessels, buyers, sellers

    # Options
    cumulative=False,
    forecasted=False,
    intra=False,  # Include intra-region flows
)

# Response format: series by date with split values
for entry in flows["series"]:
    year = entry["date"]
    for dataset in entry.get("datasets", []):
        for split in dataset.get("splitValues", []):
            vol = split["values"]["volume"]
            print(f"{year}: {split['name']} = {vol/1e6:.1f} Mt")
```

**Split options:** `countries`, `ports`, `products`, `vessels`, `buyers`, `sellers`, `charterers`

### Get vessel positions

Raw AIS tracking data:

```python
positions = await client.get_vessel_positions(
    vessel_id=12345,
    start_date="2024-01-01T00:00:00Z",  # ISO 8601
    end_date="2024-01-31T23:59:59Z",
    limit=1000,
)

for pos in positions:
    print(f"{pos['timestamp']}: {pos['lat']}, {pos['lon']}")
```

### Get player fleet

Company fleet information:

```python
fleet = await client.get_player_fleet(player_id=3836)

print(f"Company: {fleet['name']}")
print(f"Vessels owned: {len(fleet.get('ownedVessels', []))}")
print(f"Subsidiaries: {len(fleet.get('subsidiaries', []))}")
```

### Query contracts

Long-term agreements and tenders:

```python
contracts = await client.query_contracts(
    types=["SPA", "LTA"],  # Tender, SPA, LTA, TUA
    players=[3836],
    from_=0,
    size=50,
)
```

## ETL pattern for notebooks

Typical workflow for building a DuckDB database:

```python
# scripts/fetch_kpler.py
import asyncio
import duckdb
from kpler_client import KplerClient
from dotenv import load_dotenv

load_dotenv()

async def fetch_data():
    async with KplerClient() as client:
        # Search for entities
        russia = await client.search("russia", categories=["ZONE"])
        russia_id = russia["zones"][0]["entity"]["id"]

        # Get export flows
        flows = await client.query_flows(
            direction="export",
            locations=[russia_id],
            granularity="months",
            start_date="2020-01-01",
            end_date="2024-12-31",
            split_on="countries",
        )

        return flows["result"]["series"]

def build_database(data):
    con = duckdb.connect("data/data.duckdb")
    con.execute("""
        CREATE OR REPLACE TABLE flows (
            date DATE,
            destination VARCHAR,
            volume_kt DOUBLE
        )
    """)

    for series in data:
        for point in series.get("data", []):
            con.execute(
                "INSERT INTO flows VALUES (?, ?, ?)",
                [point["date"], series["name"], point["value"]]
            )

    con.close()

if __name__ == "__main__":
    data = asyncio.run(fetch_data())
    build_database(data)
```

Add to Makefile:

```makefile
data:
	uv run python scripts/fetch_kpler.py
```

## Rate limits

The Kpler API has rate limits. Add delays for large queries:

```python
import asyncio

for player_id in player_ids:
    data = await client.query_trades(players=[player_id])
    await asyncio.sleep(0.5)  # Rate limit protection
```

## Common entity IDs

Search to find current IDs, as these may change:

| Entity | Example search | Type |
|--------|----------------|------|
| Russia | `russia` | ZONE |
| China | `china` | ZONE |
| Shell | `shell` | PLAYER |
| TotalEnergies | `total` | PLAYER |
| Crude oil | `crude` | PRODUCT |
| LNG | `lng` | PRODUCT |

## Troubleshooting

**401 Unauthorized:** Credentials invalid or expired. Check `.env` file.

**Empty results:** Verify entity IDs are correct. Use `search()` to find current IDs.

**Token errors:** Delete `.kpler_token*` files and re-authenticate.

**Rate limited:** Add delays between requests. The API may temporarily block rapid queries.

## API reference

Base URL: `https://terminal.kpler.com/api`

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/trades` | POST | Query trade records |
| `/flows` | POST | Aggregate flow data |
| `/contracts` | GET | Contract data |
| `/players/{id}` | GET | Company fleet info |
| `/vessels/{id}/positions` | GET | AIS positions |
| `/graphql/` | POST | Entity search |
