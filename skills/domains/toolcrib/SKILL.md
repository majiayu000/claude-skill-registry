---
name: ToolCrib
description: |
  Tool inventory management for MNMUK machine shop.
  Tracks tooling, inserts, consumables with reorder points and usage.
  USE WHEN user asks 'tool inventory', 'what inserts', 'reorder', 'tool crib',
  'do we have', 'tooling cost', or 'tool usage'.
---

# ToolCrib - Tooling Inventory Management

**Purpose:** Track tooling inventory, prevent stockouts, control costs, optimize usage.

## When to Activate

- "Do we have CNMG inserts in stock?"
- "What's our insert usage this month?"
- "Reorder list for tooling"
- "Tool cost per part for job X"
- "What endmills do we stock?"
- "Set up tool crib inventory"

---

## Inventory Categories

### 1. Indexable Inserts (Turning)

| Category | Examples | Typical Stock |
|----------|----------|---------------|
| OD Roughing | CNMG, WNMG, DNMG | 20-50 per grade |
| OD Finishing | DCMT, VCMT, CCMT | 10-30 per grade |
| Boring | CCMT, TCMT, DCMT | 10-20 per size |
| Threading | 16ER, 16IR (various pitches) | 5-10 per pitch |
| Grooving/Parting | Various widths | 10-20 per width |
| Copy turning | VCMT, DCMT | 10-20 per grade |

### 2. Indexable Inserts (Milling)

| Category | Examples | Typical Stock |
|----------|----------|---------------|
| Face milling | APKT, SEKN, ODMT | 20-40 per grade |
| Shoulder milling | APMT, LOGU | 10-30 per grade |
| Slot/pocket | APMT, various | 10-20 per size |
| High-feed | Various proprietary | 10-20 per size |

### 3. Solid Carbide Tools

| Category | Sizes | Typical Stock |
|----------|-------|---------------|
| Endmills (3-flute) | Ø3-20mm | 2-5 per size |
| Endmills (4-flute) | Ø6-25mm | 2-5 per size |
| Ball nose | Ø3-16mm | 1-3 per size |
| Drills | Ø1-20mm (0.5mm steps) | 2-5 per size |
| Reamers | Common sizes | 1-2 per size |
| Taps | M3-M20 | 3-10 per size |
| Thread mills | Common pitches | 1-2 per size |

### 4. Toolholders

| Category | Types |
|----------|-------|
| Turning | External, internal, threading, parting |
| Milling | Shrink fit, ER collet, hydraulic, side-lock |
| Boring | Modular boring bars, cartridge heads |

### 5. Consumables

| Item | Track |
|------|-------|
| Collets (ER, 5C, etc.) | By size |
| Chuck jaws | By chuck/type |
| Parallels, V-blocks | General stock |
| Workholding clamps | By type |
| Edge finders, indicators | Per machine |
| Gauge pins, thread gauges | By size/pitch |

---

## Inventory Database Template

### Insert Inventory

```markdown
# Insert Inventory

Last Updated: YYYY-MM-DD
Counted By: [Name]

## Turning Inserts

| Insert Code | Grade | Qty In Stock | Min Stock | Reorder Qty | Location | Last Count | Supplier | Cost Each |
|-------------|-------|--------------|-----------|-------------|----------|------------|----------|-----------|
| CNMG120408-PM | 4325 | | 20 | 50 | A1-01 | | Sandvik | £X.XX |
| CNMG120408-MR | 4325 | | 20 | 50 | A1-02 | | Sandvik | £X.XX |
| WNMG080408-PM | 4325 | | 10 | 30 | A1-03 | | Sandvik | £X.XX |
| DCMT11T304-PF | 4325 | | 10 | 30 | A1-04 | | Sandvik | £X.XX |
| VCMT110304-PF | 4325 | | 10 | 20 | A1-05 | | Sandvik | £X.XX |
| 16ER-1.5ISO | 4325 | | 10 | 20 | A2-01 | | Sandvik | £X.XX |
| 16IR-1.5ISO | 4325 | | 5 | 10 | A2-02 | | Sandvik | £X.XX |

## Milling Inserts

| Insert Code | Grade | Qty In Stock | Min Stock | Reorder Qty | Location | Last Count | Supplier | Cost Each |
|-------------|-------|--------------|-----------|-------------|----------|------------|----------|-----------|
| APMT1135-PM | 4240 | | 20 | 50 | B1-01 | | Sandvik | £X.XX |
| SEKN1203 | 4240 | | 10 | 30 | B1-02 | | Sandvik | £X.XX |

## Solid Carbide - Endmills

| Description | Diameter | Flutes | Coating | Qty | Min | Location | Supplier | Cost |
|-------------|----------|--------|---------|-----|-----|----------|----------|------|
| GP Endmill | Ø6mm | 4 | AlTiN | | 3 | C1-06 | | £XX |
| GP Endmill | Ø8mm | 4 | AlTiN | | 3 | C1-08 | | £XX |
| GP Endmill | Ø10mm | 4 | AlTiN | | 3 | C1-10 | | £XX |
| GP Endmill | Ø12mm | 4 | AlTiN | | 3 | C1-12 | | £XX |
| SS Endmill | Ø6mm | 5 | TiAlN | | 2 | C2-06 | | £XX |
| SS Endmill | Ø8mm | 5 | TiAlN | | 2 | C2-08 | | £XX |

## Drills

| Type | Diameter | Coating | Qty | Min | Location | Supplier | Cost |
|------|----------|---------|-----|-----|----------|----------|------|
| Carbide | Ø3.0mm | TiAlN | | 5 | D1-30 | | £XX |
| Carbide | Ø3.5mm | TiAlN | | 5 | D1-35 | | £XX |
| Carbide | Ø4.0mm | TiAlN | | 5 | D1-40 | | £XX |
| Carbide | Ø4.5mm | TiAlN | | 5 | D1-45 | | £XX |
| Carbide | Ø5.0mm | TiAlN | | 5 | D1-50 | | £XX |
```

---

## Reorder Management

### Reorder Point Formula

```
Reorder Point = (Daily Usage × Lead Time) + Safety Stock

Where:
- Daily Usage = Monthly usage ÷ Working days
- Lead Time = Supplier delivery days
- Safety Stock = 1-2 weeks usage (critical items)
```

### Reorder Report Template

```markdown
# Tool Reorder Report

Generated: YYYY-MM-DD

## Items Below Minimum Stock

| Item | Current Qty | Min Stock | Reorder Qty | Supplier | Est. Cost | Priority |
|------|-------------|-----------|-------------|----------|-----------|----------|
| | | | | | | HIGH |
| | | | | | | MEDIUM |
| | | | | | | LOW |

## Total Reorder Value: £X,XXX

## Approval

| | |
|---|---|
| Requested By: | |
| Approved By: | |
| Date: | |
| PO Number: | |
```

### Supplier Quick Reference

| Supplier | Lead Time | Min Order | Account # | Contact |
|----------|-----------|-----------|-----------|---------|
| Sandvik | 2-3 days | £100 | | |
| Seco | 2-3 days | £100 | | |
| Iscar | 2-3 days | £100 | | |
| Kennametal | 3-5 days | £100 | | |
| OSG | 3-5 days | £50 | | |
| Cutwel | Next day | £25 | | |

---

## Usage Tracking

### Insert Usage Log

```markdown
# Insert Usage Log

## Month: [YYYY-MM]

| Date | Job # | Insert Code | Qty Used | Machine | Reason | Operator |
|------|-------|-------------|----------|---------|--------|----------|
| | | | | | Wear | |
| | | | | | Chipped | |
| | | | | | Broken | |

## Monthly Summary

| Insert Code | Total Used | Cost | Top Consumer (Job) |
|-------------|------------|------|-------------------|
| | | £ | |
| | | £ | |

**Total Insert Cost This Month: £X,XXX**
```

### Tool Cost Per Part

```markdown
# Tool Cost Analysis - Job [Number]

| Tool | Insert/Item | Qty Used | Parts Made | Cost/Part | % of Total |
|------|-------------|----------|------------|-----------|------------|
| T1 | CNMG120408 | 4 | 500 | £0.XX | XX% |
| T2 | DCMT11T304 | 2 | 500 | £0.XX | XX% |
| T3 | Ø10 Drill | 1 | 500 | £0.XX | XX% |
| | | | | | |
| **Total** | | | | **£X.XX** | 100% |

**Target: £X.XX/part | Actual: £X.XX/part | Variance: XX%**
```

---

## Tool Life Management

### Insert Life Standards

| Insert Type | Material | Expected Life (edges) | Notes |
|-------------|----------|----------------------|-------|
| CNMG (rough) | Steel | 15-25 min/edge | 4 edges |
| CNMG (rough) | Stainless | 8-15 min/edge | 4 edges |
| DCMT (finish) | Steel | 20-40 min/edge | 2 edges |
| DCMT (finish) | Stainless | 10-20 min/edge | 2 edges |
| Threading | Steel | 50-100 threads/edge | |
| Endmill (carbide) | Steel | 60-120 min | Regrind 2-3x |
| Endmill (carbide) | Stainless | 30-60 min | Regrind 2-3x |
| Drill (carbide) | Steel | 500-2000 holes | Regrind 2-3x |

### Regrind Tracking

```markdown
# Regrind Log

| Tool ID | Description | Diameter | Regrinds | Max | Status | Location |
|---------|-------------|----------|----------|-----|--------|----------|
| EM-001 | 4FL Ø12 AlTiN | 12.00mm | 0 | 3 | In use | M3-T5 |
| EM-001 | 4FL Ø12 AlTiN | 11.85mm | 1 | 3 | Stock | C1-12R |
| EM-001 | 4FL Ø12 AlTiN | 11.70mm | 2 | 3 | Stock | C1-12R |
| EM-002 | 4FL Ø10 AlTiN | 9.85mm | 1 | 3 | For regrind | Regrind box |
```

---

## Inventory Audit

### Monthly Audit Checklist

```markdown
# Tool Crib Monthly Audit

Date: YYYY-MM-DD
Auditor: [Name]

## Physical Count vs. System

| Location | Items Counted | Discrepancies | Value Variance |
|----------|---------------|---------------|----------------|
| A - Turning inserts | | | £ |
| B - Milling inserts | | | £ |
| C - Solid carbide | | | £ |
| D - Drills | | | £ |
| E - Taps/reamers | | | £ |
| F - Holders | | | £ |

## Condition Check

| Issue | Items Found | Action Taken |
|-------|-------------|--------------|
| Damaged packaging | | |
| Corroded tools | | |
| Wrong location | | |
| Expired (shelf life) | | |

## Stock Optimization

| Item | Current Stock | 6-Month Usage | Recommendation |
|------|---------------|---------------|----------------|
| | | 0 | Remove from stock |
| | | Low | Reduce min level |
| | | High | Increase min level |

## Summary

| Metric | Value |
|--------|-------|
| Total SKUs | |
| Total Value | £ |
| Items below min | |
| Items overstocked | |
| Accuracy % | |
```

---

## Cost Control

### Monthly Tooling Report

```markdown
# Tooling Cost Report - [Month YYYY]

## Summary

| Category | Budget | Actual | Variance |
|----------|--------|--------|----------|
| Turning inserts | £ | £ | £ |
| Milling inserts | £ | £ | £ |
| Solid carbide | £ | £ | £ |
| Drills/taps | £ | £ | £ |
| Regrinding | £ | £ | £ |
| **Total** | **£** | **£** | **£** |

## Cost Per Machine Hour

| Machine | Hours | Tool Cost | £/Hour |
|---------|-------|-----------|--------|
| NMV3000 | | £ | |
| DMU50 | | £ | |
| NLX2500 | | £ | |
| CITIZEN | | £ | |
| **Average** | | | **£** |

## Top 10 Cost Items

| Rank | Item | Qty Used | Cost | % of Total |
|------|------|----------|------|------------|
| 1 | | | £ | |
| 2 | | | £ | |
| 3 | | | £ | |

## Cost Reduction Actions

| Action | Potential Savings | Status |
|--------|-------------------|--------|
| | £ | |
```

### Tooling Budget Guidelines

| Metric | Target | Notes |
|--------|--------|-------|
| Tooling as % of sales | 3-5% | Industry benchmark |
| Tool cost per machine hour | £5-15 | Depends on materials |
| Insert cost per part | <2% of part cost | Target |

---

## Storage Organization

### Tool Crib Layout

```
┌─────────────────────────────────────────────────────┐
│                    TOOL CRIB                        │
├─────────┬─────────┬─────────┬─────────┬────────────┤
│    A    │    B    │    C    │    D    │     E      │
│ Turning │ Milling │ Solid   │ Drills  │ Taps &     │
│ Inserts │ Inserts │ Carbide │         │ Reamers    │
├─────────┴─────────┴─────────┴─────────┴────────────┤
│                       F                             │
│              Toolholders & Collets                  │
├─────────────────────────────────────────────────────┤
│                       G                             │
│              Workholding & Fixtures                 │
├─────────────────────────────────────────────────────┤
│         REGRIND          │       NEW STOCK          │
│          BOX             │       INTAKE             │
└─────────────────────────────────────────────────────┘
```

### Location Coding

```
Format: [Section][Row]-[Position]

Example: A1-05 = Section A, Row 1, Position 05

Sections:
A = Turning inserts
B = Milling inserts
C = Solid carbide endmills
D = Drills
E = Taps, reamers, thread mills
F = Toolholders
G = Workholding
```

---

## Integration

- **CNCSetup:** Reference tool locations in setup sheets
- **QuoteEstimator:** Tool cost per part in quotes
- **CuttingParams:** Link recommended inserts to inventory
- **TribalKnowledge:** Capture preferred tool selections by job
