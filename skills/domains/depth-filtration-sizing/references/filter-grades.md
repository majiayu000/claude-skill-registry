# FILTROX Filter Grade Reference

Full grade tables for the wine (AF/XE) and spirits (XS) depth filtration
cascades, plus the CLAROX® membrane step. Source: the stage guides and
calculator tables in `bot.py` (`WINE_DATA`, `SPIRITS_DATA`, `calculate_wine`,
`calculate_spirits`).

All per-sheet capacities are for the **40×40 cm** sheet format.

## Wine — AF / XE grades

| Grade | Stage | Turbidity band (NTU) | Flow rate | Max ΔP | Capacity | Notes |
|---|---|---|---|---|---|---|
| AF 21 / XE 34 | Coarse | ~50 → 15 | 700 l/m²/h | 2.5 bar | — | Entry stage; requires <50 NTU feed |
| AF 71 / XE 94 | Polishing | ~15 → ~5 | 500 l/m²/h | 1.5 bar | 4.0 hl/sheet | Barrel-aged reds |
| AF 101 / XE 104 | Polishing | ~15 → ~5 | 400 l/m²/h | 1.5 bar | — | Standard polishing |
| AF 130 | Final | ~5 → <3 | 350 l/m²/h | 1.5 bar | 3.5 hl/sheet | Red and white; >10⁷ log reduction |
| AF 140 | Final | ~5 → <3 | 300 l/m²/h | 1.5 bar | 3.0 hl/sheet | Premium white; >10⁸ log reduction |

Capacities are published only for the three grades the sheet calculator covers
(AF 71, AF 130, AF 140). For AF 21 and AF 101, size from flow rate and run
duration against the housing's filter area instead:

```
area_m2 = (volume_hl × 100) ÷ (flow_rate_l_per_m2_h × hours)
```

**Pre-filtration gate:** above 50 NTU, stabilize or centrifuge before any sheet
stage. Sheets clarify nothing at that load; they blind.

## Spirits — XS grades

| Grade | Stage | Rating | Flow rate | Max ΔP | Capacity | Notes |
|---|---|---|---|---|---|---|
| XS 34 | Rough | 0.6–1.05 µm | 1500 l/m²/h | 2.5 bar | — | Removes oily/fatty matter |
| XS 90 | Cold | — | 800–1200 l/m²/h | — | 400 hl/sheet | Run at −5 °C to −20 °C |
| XS 100 | Final | — | 600–1000 l/m²/h | — | 350 hl/sheet | High purity |
| XS 110 | Final | — | 400–800 l/m²/h | — | 280 hl/sheet | Sterile grade |

**Cold filtration conditions:** cool to between −5 °C and −20 °C and hold for
24–48 hours before filtering. The spirit must stay at temperature *through* the
filter — chill haze that is filtered warm simply re-dissolves.

## Membrane step — CLAROX® MP/W

| Cartridge | Pairs with |
|---|---|
| 0.65 µm | AF 130 |
| 0.45 µm | AF 140 |

An integrity test is mandatory before bottling on every run.

## Sheet count formula

```
sheets = floor(volume_hl / capacity_hl_per_sheet) + 1
```

The `+ 1` is a spare sheet and is applied unconditionally, including when the
division is exact.

| Volume | AF 71 (4.0) | AF 130 (3.5) | AF 140 (3.0) |
|---|---|---|---|
| 50 hl | 13 | 15 | 17 |
| 100 hl | 26 | 29 | 34 |
| 200 hl | 51 | 58 | 67 |
| 500 hl | 126 | 143 | 167 |

| Volume | XS 90 (400) | XS 100 (350) | XS 110 (280) |
|---|---|---|---|
| 500 hl | 2 | 2 | 2 |
| 1000 hl | 3 | 3 | 4 |
| 5000 hl | 13 | 15 | 18 |

For sheet formats other than 40×40 cm, scale capacity by area:
a 60×60 cm sheet is 2.25× the area, so 2.25× the capacity.

## Unit conversions

| From | To hectolitres |
|---|---|
| 1 litre | 0.01 hl |
| 1 US gallon | 0.0378541 hl |
| 1 standard 750 ml bottle | 0.0075 hl |
| 1 barrique (225 l) | 2.25 hl |

## Verification

These figures are FILTROX product specifications as distributed by ENOTECH
Georgia, the official FILTROX representative in Georgia. Confirm against the
current FILTROX datasheet before purchasing — specifications change between
product generations.
