---
name: macro-calendar
description: Track macroeconomic events, Fed rates, CPI, and economic indicators affecting crypto.
metadata: { "cryptoclaw": { "emoji": "📅", "always": true } }
---

# Economic Calendar & Macro Data

Track macroeconomic events and economic indicators that impact crypto markets.

## Data Sources

### 1. FRED API (Federal Reserve Economic Data)

```
https://api.stlouisfed.org/fred/
```

Free API key: register at https://fred.stlouisfed.org/docs/api/api_key.html

If `FRED_API_KEY` is set, use it. Otherwise, note the data is unavailable and suggest the user register for a free key.

#### Key Series

| Series ID  | Description                    |
| ---------- | ------------------------------ |
| `FEDFUNDS` | Federal Funds Effective Rate   |
| `CPIAUCSL` | Consumer Price Index (CPI)     |
| `UNRATE`   | Unemployment Rate              |
| `GDP`      | Gross Domestic Product         |
| `DGS10`    | 10-Year Treasury Yield         |
| `DGS2`     | 2-Year Treasury Yield          |
| `T10Y2Y`   | 10Y-2Y Spread (yield curve)    |
| `M2SL`     | M2 Money Supply                |
| `WALCL`    | Fed Balance Sheet Total Assets |
| `DEXUSEU`  | USD/EUR Exchange Rate          |

#### Endpoints

Latest observation:

```
GET /fred/series/observations?series_id={id}&sort_order=desc&limit=1&api_key={key}&file_type=json
```

Historical data:

```
GET /fred/series/observations?series_id={id}&observation_start={YYYY-MM-DD}&api_key={key}&file_type=json
```

Series metadata:

```
GET /fred/series?series_id={id}&api_key={key}&file_type=json
```

### 2. Finnhub Economic Calendar

```
https://finnhub.io/api/v1/calendar/economic
```

Free API key: register at https://finnhub.io. Set `FINNHUB_API_KEY`.

#### Endpoint

```
GET /calendar/economic?from={YYYY-MM-DD}&to={YYYY-MM-DD}&token={key}
```

Returns upcoming economic events with:

- `event` — event name
- `country` — country code
- `impact` — `high`, `medium`, `low`
- `actual` / `estimate` / `prev` — data values
- `time` — event timestamp

## Key Events for Crypto

### High Impact

| Event                   | Frequency | Why It Matters                      |
| ----------------------- | --------- | ----------------------------------- |
| FOMC Rate Decision      | 8x/year   | Rate hikes → risk-off → crypto down |
| CPI (Inflation)         | Monthly   | High CPI → more hikes expected      |
| Non-Farm Payrolls (NFP) | Monthly   | Strong jobs → hawkish Fed           |
| GDP                     | Quarterly | Recession fears → flight to safety  |
| PCE Price Index         | Monthly   | Fed's preferred inflation gauge     |

### Medium Impact

| Event               | Frequency | Why It Matters             |
| ------------------- | --------- | -------------------------- |
| PMI (Manufacturing) | Monthly   | Economic health indicator  |
| Retail Sales        | Monthly   | Consumer spending strength |
| Jobless Claims      | Weekly    | Labor market pulse         |
| ISM Services        | Monthly   | Service sector health      |

## Impact on Crypto

General patterns (not financial advice):

- **Rate cuts / dovish Fed** → bullish for crypto (more liquidity)
- **Rate hikes / hawkish Fed** → bearish for crypto (less liquidity)
- **CPI above expectations** → bearish (more hikes coming)
- **CPI below expectations** → bullish (rate cuts possible)
- **Strong jobs data** → mixed (good economy but hawkish Fed)
- **Yield curve inversion** → recession signal, initially bearish then bullish

## Usage Notes

- Always note that macro-to-crypto correlation is not guaranteed
- Present event times in the user's timezone when possible
- For FOMC meetings, note both the date and the press conference time
- Combine with `crypto-news` for full market context
- If no API keys are available, summarize what data would be accessible and suggest registration

## Example Interactions

User: "When is the next Fed meeting?"
→ Check Finnhub calendar for FOMC events, report date and current rate expectations

User: "What's the current CPI?"
→ Fetch FRED series CPIAUCSL, report latest reading and YoY change

User: "Any major economic events this week?"
→ Fetch Finnhub calendar for current week, filter by high impact, list events

User: "How does the yield curve look?"
→ Fetch DGS10, DGS2, T10Y2Y from FRED, report current spread and inversion status
