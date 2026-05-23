---
name: eptr2-market-operations
description: Query Turkish electricity market operations data including Day-Ahead Market (GÖP) orders and clearing, Intraday Market (GİP) transactions and order books, bilateral contracts (İA), and Balancing Power Market (DGP) instructions. Use when asking about market volumes, trading activity, order books, block bids, flexible offers, or bilateral agreements in Turkey. Triggers on: GÖP, GİP, DGP, gün öncesi piyasası, gün içi piyasası, ikili anlaşmalar, market orders, block bids, YAL, YAT.
allowed-tools: Read, Bash(python:*)
---

# Turkish Electricity Market Operations with eptr2

## Overview

This skill helps you query electricity market trading data from Turkey's EPIAS Transparency Platform, covering the Day-Ahead Market (GÖP), Intraday Market (GİP), Bilateral Contracts (İA), and Balancing Power Market (DGP).

## Quick Start

```python
from eptr2 import EPTR2

# Initialize
eptr = EPTR2(use_dotenv=True, recycle_tgt=True)

# Get DAM clearing quantity
dam_clearing = eptr.call("dam-clearing", start_date="2024-07-29", end_date="2024-07-29")
print(dam_clearing)
```

## Market Structure Overview

| Market | Turkish | Abbreviation | Timing |
|--------|---------|--------------|--------|
| Day-Ahead Market | Gün Öncesi Piyasası | GÖP | D-1 (day before delivery) |
| Intraday Market | Gün İçi Piyasası | GİP | Until 1h before delivery |
| Balancing Power Market | Dengeleme Güç Piyasası | DGP | Real-time balancing |
| Bilateral Contracts | İkili Anlaşmalar | İA | OTC agreements |

---

## Day-Ahead Market (GÖP) Endpoints

### Quantities & Clearing

| Call | Description (EN) | Description (TR) |
|------|------------------|------------------|
| `dam-clearing` | DAM Matching Quantity | GÖP Eşleşme Miktarı |
| `dam-volume` | DAM Trade Value | GÖP İşlem Hacmi |
| `dam-bid` | DAM Submitted Bid Volume | GÖP Teklif Edilen Alış Miktarları |
| `dam-offer` | DAM Submitted Sales Volume | GÖP Teklif Edilen Satış Miktarları |

### Block & Flexible Orders

| Call | Description (EN) | Description (TR) |
|------|------------------|------------------|
| `dam-block-bid` | DAM Block Bid | GÖP Blok Alış Miktarı |
| `dam-block-offer` | DAM Block Offer | GÖP Blok Satış Miktarı |
| `dam-flexible-bid` | DAM Flexible Buying Offer | GÖP Esnek Alış Teklif |
| `dam-flexible-offer` | DAM Flexible Selling Offer | GÖP Esnek Satış Teklif |
| `dam-flexible-matching` | DAM Matched Flexible Offers | GÖP Esnek Teklif Eşleşme |

### Price Independent Orders

| Call | Description (EN) | Description (TR) |
|------|------------------|------------------|
| `pi-bid` | Price Independent Bid Order | Fiyattan Bağımsız Alış Teklifi |
| `pi-offer` | Price Independent Sales Order | Fiyattan Bağımsız Satış Teklifi |

### Supply-Demand

| Call | Description |
|------|-------------|
| `supply-demand` | DAM Supply-Demand curves at each price step |

---

## Intraday Market (GİP) Endpoints

### Quantities & Prices

| Call | Description (EN) | Description (TR) |
|------|------------------|------------------|
| `idm-qty` | IDM Matching Quantity | GİP Eşleşme Miktarı |
| `idm-volume` | IDM Trade Value | GİP İşlem Hacmi |
| `wap` | IDM Weighted Average Price | GİP Ağırlıklı Ortalama Fiyat |

### Min-Max Prices

| Call | Description |
|------|-------------|
| `idm-mm-bid` | IDM Min-Max Bid Price |
| `idm-mm-offer` | IDM Min-Max Offer Price |
| `idm-mm-matching` | IDM Min-Max Matching Price |

### Transaction & Order Data

| Call | Description |
|------|-------------|
| `idm-log` | IDM Transaction History (işlem akışı) |
| `idm-order-list` | IDM Order List |
| `idm-contract-list` | IDM Contract List |
| `idm-summary` | IDM Contract Summary |
| `idm-ob-qty` | IDM Bid/Offer Quantities |

---

## Balancing Power Market (DGP) Endpoints

| Call | Description (EN) | Description (TR) |
|------|------------------|------------------|
| `bpm-up` | Up Regulation Instructions | Yük Alma (YAL) Talimat |
| `bpm-down` | Down Regulation Instructions | Yük Atma (YAT) Talimat |
| `bpm-orders-w-avg` | BPM Instructions (Weighted Avg) | DGP Talimatları (AOF) |
| `smp-dir` | System Direction | Sistem Yönü |

---

## Bilateral Contracts (İA) Endpoints

| Call | Description (EN) | Description (TR) |
|------|------------------|------------------|
| `bi-long` | Bilateral Contracts Bid Quantity | İA Alış Miktarı |
| `bi-short` | Bilateral Contracts Offer Quantity | İA Satış Miktarı |
| `bi-euas` | EÜAŞ - Authorized Retailers Bilaterals | EÜAŞ - GTŞ İkili Anlaşmalar |

---

## Common Use Cases

### 1. DAM Trading Activity

```python
# Get DAM clearing and volume for a day
clearing = eptr.call("dam-clearing", start_date="2024-07-15", end_date="2024-07-15")
volume = eptr.call("dam-volume", start_date="2024-07-15", end_date="2024-07-15")

print(f"Total Cleared: {clearing['matchedQuantity'].sum():,.0f} MWh")
print(f"Total Volume: {volume['volume'].sum():,.0f} TL")
```

### 2. IDM Transaction History

```python
# Get intraday market transaction log
idm_log = eptr.call("idm-log", start_date="2024-07-15", end_date="2024-07-15")

# Analyze by contract
print(f"Total Transactions: {len(idm_log)}")
print(f"Total IDM Volume: {idm_log['quantity'].sum():,.0f} MWh")
```

### 3. Balancing Instructions

```python
# Get up and down regulation instructions
yal = eptr.call("bpm-up", start_date="2024-07-15", end_date="2024-07-15")
yat = eptr.call("bpm-down", start_date="2024-07-15", end_date="2024-07-15")

print(f"Total Up Regulation (YAL): {yal['upRegulationNet'].sum():,.0f} MWh")
print(f"Total Down Regulation (YAT): {yat['downRegulationNet'].sum():,.0f} MWh")
```

### 4. Bilateral Contracts Volume

```python
bi_long = eptr.call("bi-long", start_date="2024-07-15", end_date="2024-07-15")
bi_short = eptr.call("bi-short", start_date="2024-07-15", end_date="2024-07-15")

print(f"Bilateral Purchases: {bi_long['quantity'].sum():,.0f} MWh")
print(f"Bilateral Sales: {bi_short['quantity'].sum():,.0f} MWh")
```

---

## Market Volume Breakdown

Get comprehensive market volumes:

```python
# All market volumes in one call
market_volumes = eptr.call(
    "electricity-market-quantity",
    start_date="2024-07-15",
    end_date="2024-07-15"
)
print(market_volumes)
```

---

## Date Format

Always use ISO format: `YYYY-MM-DD` (e.g., "2024-07-29")

## Authentication

Set credentials in `.env` file:
```
EPTR_USERNAME=your_email@example.com
EPTR_PASSWORD=your_password
```

## For More Details

- See [examples.md](examples.md) for additional code examples
