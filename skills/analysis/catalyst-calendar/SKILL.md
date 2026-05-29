---
name: catalyst-calendar
description: Maintain calendar of upcoming catalysts for portfolio positions and watchlist. Earnings dates, ex-div dates, regulatory events, macro releases. Triggers on "catalysts", "upcoming events", "earnings calendar", "what's coming up", "catalyst calendar".
---

# Catalyst Calendar

Track upcoming events that could move portfolio positions.

## Step 1: Collect Positions

If not provided, ask user for current portfolio and watchlist tickers.

## Step 2: Gather Catalysts

For each ticker, search for:

**Company-specific:**
- Next earnings date + time (pre/post market)
- Ex-dividend date + payment date
- Product launches / FDA decisions / regulatory milestones
- Management changes / investor days
- Lock-up expirations / secondary offerings
- Debt maturities / refinancing

**AR-specific:**
- Licitaciones de bonos (Finanzas/BCRA)
- Vencimientos de LECAPs/LEFIs/BONCAPs
- Pagos de renta y amortización (bonos soberanos y corporativos)
- Reuniones de directorio BCRA (tasa de política monetaria)
- Datos de inflación (INDEC) y REM (expectativas)
- Fechas de liquidación de cosecha (soja, trigo, maíz)
- Regulatory: CNV, BCRA circulares (parking, limits)

**US macro:**
- FOMC meetings + rate decisions
- CPI / PPI / NFP / GDP releases
- Options expiration (monthly OPEX, quarterly witching)

## Step 3: Calendar View

### Next 2 Weeks (Detail)

| Date | Time | Event | Ticker(s) | Expected Impact | Action |
|------|------|-------|-----------|-----------------|--------|
| | | | | High/Med/Low | Watch/Trade/Hedge |

### Next 30 Days (Summary)

| Week | Key Events | Tickers Affected |
|------|-----------|-----------------|
| | | |

### Next 90 Days (Horizon)

| Month | Major Catalysts |
|-------|----------------|
| | |

## Step 4: Risk Overlay

Flag clusters:
- Multiple earnings in same week → portfolio volatility spike
- FOMC + earnings overlap → compounded uncertainty
- AR regulatory dates near position settlement dates → liquidity risk

## Step 5: Output

```
═══ CATALYST CALENDAR ═══
Portfolio: [N] positions tracked
Next event: [event] for [ticker] on [date] ([N] days)
High-impact events this week: [count]

⚠️ ALERTS:
- [TICKER] earnings in [N] days — review thesis
- Cluster: [N] events on [date] — consider hedging
- [Bond ticker] coupon payment on [date]
```

## Notes

- Update calendar weekly at minimum
- Cross-reference with thesis-tracker: if a catalyst resolves a pillar, update both
- For options positions: flag when expiration approaches a catalyst (gamma risk)
- ALWAYS verify dates via web search — earnings dates shift frequently
- AR data: check Bolsar, BYMA, and Finanzas.gob.ar for official dates
