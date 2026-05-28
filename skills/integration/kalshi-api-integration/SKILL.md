---
name: kalshi-api-integration
description: Documentation for integrating with the Kalshi API, covering authentication, market fetching, ticker parsing, and bet placement.
version: 1.0.0
---

# Kalshi API Integration

## Authentication

Credentials stored in `kalshkey` (never commit):
```
API_KEY_ID
PRIVATE_KEY_PEM_CONTENT
```

Load with:
```python
with open("kalshkey") as f:
    api_key_id = f.readline().strip()
    private_key = f.read()
```

## API Client Setup

```python
from kalshi_python import Configuration, ApiClient, MarketsApi

config = Configuration(host="https://api.elections.kalshi.com/trade-api/v2")
config.api_key['api_key_id'] = api_key_id
config.api_key['private_key'] = private_key_pem

client = ApiClient(configuration=config)
markets_api = MarketsApi(client)
```

## Market Ticker Format

Pattern: `SERIES-YYMMDD-AWAYHOME-OUTCOME`

Examples:
- `NBAWIN-250115-LAKBOS-LAK` - Lakers to beat Celtics
- `NHLWIN-250115-TORBOS-TOR` - Maple Leafs to beat Bruins

## Parsing Tickers

```python
parts = ticker.split('-')
# parts[0]: Series (NBAWIN, NHLWIN)
# parts[1]: Date (YYMMDD)
# parts[2]: Teams (AWAYHOME combined)
# parts[3]: Winner team code
```

## Team Name Resolution

Use `NamingResolver` for consistent team names:

```python
from naming_resolver import NamingResolver

resolver = NamingResolver()
canonical = resolver.resolve("LAL", "nba")  # → "Los Angeles Lakers"
```

## Fetching Markets

```python
def fetch_nba_markets():
    """Fetch open NBA markets from Kalshi."""
    response = markets_api.get_markets(
        series_ticker="NBAWIN",
        status="open",
        limit=100
    )
    return response.to_dict().get("markets", [])
```

## Saving to Database

Always save to PostgreSQL, not JSON:

```python
from db_manager import default_db

def save_to_db(sport: str, markets: list):
    for market in markets:
        # Parse market data
        # Insert into game_odds table
        default_db.execute("""
            INSERT INTO game_odds (game_id, source, yes_price, no_price, ...)
            VALUES (:game_id, 'kalshi', :yes_price, :no_price, ...)
            ON CONFLICT (game_id, source) DO UPDATE SET ...
        """, params)
```

## Bet Placement

```python
from kalshi_betting import place_bet

result = place_bet(
    ticker="NBAWIN-250115-LAKBOS-LAK",
    side="yes",  # or "no"
    amount=10.00,
    limit_price=0.65  # Max price willing to pay
)
```

## Files to Reference

- `plugins/kalshi_markets.py` - Market fetching
- `plugins/kalshi_betting.py` - Bet placement
- `plugins/naming_resolver.py` - Team name mapping
