---
name: depth-filtration-sizing
description: Size and stage depth filtration for wine and spirits using FILTROX AF/XS
  filter sheet grades, turbidity targets, flow limits, and sheet-count formulas.
metadata:
  version: 1.0.0
  source: https://github.com/Davitip/filtrox-bot
---
# Depth Filtration Sizing (Wine & Spirits)

Depth filtration removes particles by trapping them throughout the thickness of a
cellulose sheet, not just at its surface. Sizing it means answering two questions
in order:

1. **Which stage am I in?** — set by the *incoming* turbidity, not by the wine's age or price.
2. **How many sheets does that stage need?** — set by volume and the grade's per-sheet capacity.

Getting these backwards is the most common mistake: picking a fine grade because
the wine is premium, rather than because the turbidity is already low enough for
that grade to survive the run.

## The cascade rule

**Never skip a stage.** Each grade is specified for a narrow turbidity band. Feeding
a fine sheet water that belongs to a coarse stage blinds it within minutes — the
differential pressure spikes, flow collapses, and the sheets are spent long before
their rated volume. When someone reports "the sheets clogged immediately," the
cause is almost always a skipped upstream stage, not a defective sheet.

Wine cascade, with the turbidity band each stage is expected to deliver:

| Stage | In → Out (NTU) | Grades | Flow rate | Max ΔP |
|---|---|---|---|---|
| 1. Coarse | ~50 → 15 | AF 21 / XE 34 | 700 l/m²/h | 2.5 bar |
| 2. Polishing | ~15 → ~5 | AF 71 / XE 94 (barrel reds), AF 101 / XE 104 (standard) | 500 / 400 l/m²/h | 1.5 bar |
| 3. Final | ~5 → <3 | AF 130 (red & white), AF 140 (premium white) | 350 / 300 l/m²/h | 1.5 bar |
| 4. Sterile | <3, pre-bottling | CLAROX® MP/W membrane cartridges | — | — |

**Above 50 NTU, do not filter at all.** Stabilize or centrifuge first. Sheets are
not a clarification tool; they are a polishing tool that assumes clarification
already happened.

Spirits cascade:

| Stage | Purpose | Grades | Flow rate |
|---|---|---|---|
| 1. Rough | Remove oily/fatty matter | XS 34 (0.6–1.05 µm) | 1500 l/m²/h, max 2.5 bar |
| 2. Cold | Chill haze removal at −5 °C to −20 °C, 24–48 h hold | XS 90 | 800–1200 l/m²/h |
| 3. Final | High purity / sterile | XS 100, XS 110 | 600–1000 / 400–800 l/m²/h |

Cold filtration only works if the spirit is *held* at temperature through the
filter. Chilling the tank and then filtering at ambient re-dissolves the haze and
wastes the run.

## Sizing the sheet count

Sheet counts below assume the **40×40 cm** sheet format, which is what the
per-sheet capacities are quoted against. For any other plate size, scale by area
before using these numbers.

```
sheets = floor(volume_hl / capacity_hl_per_sheet) + 1
```

The `+ 1` is deliberate and is applied even when the division is exact — it is the
spare sheet, not a rounding artifact. A run that ends one sheet short means
breaking the filter train mid-batch with wine already in the plates.

Per-sheet capacity, 40×40 cm:

| Product | Grade | Capacity | Typical use |
|---|---|---|---|
| Wine | AF 71 | 4.0 hl/sheet | Barrel-aged wine |
| Wine | AF 130 | 3.5 hl/sheet | Red and white |
| Wine | AF 140 | 3.0 hl/sheet | Premium white |
| Spirits | XS 90 | 400 hl/sheet | Cold filtration |
| Spirits | XS 100 | 350 hl/sheet | High purity |
| Spirits | XS 110 | 280 hl/sheet | Sterile |

Note the direction: **finer grade → lower capacity**. AF 140 is the tightest wine
grade and gives up ~15 % of AF 130's throughput to get there. Two orders of
magnitude separate wine from spirits capacity because spirits carry far less
colloidal load per hectolitre.

Worked example — 100 hl of premium white through AF 140:
`floor(100 / 3.0) + 1 = 33 + 1 = 34 sheets`.

When the user gives a volume without naming a grade, quote all grades valid for
their product so they can see the capacity/tightness trade-off, rather than
picking one for them.

## Sterile filtration and the integrity test

The membrane step is matched to the sheet grade immediately upstream:

- **0.65 µm CLAROX® MP/W** — after AF 130
- **0.45 µm CLAROX® MP/W** — after AF 140

An **integrity test before bottling is mandatory**, not advisory. A membrane that
passed yesterday is not evidence about today's cartridge: it can be compromised by
a single pressure shock or a steam cycle. Bottling behind an untested membrane
means the sterility claim is unverified for that entire batch.

Log reduction ratings for the final sheet stage: AF 130 >10⁷, AF 140 >10⁸. These
are sheet ratings and do not substitute for the membrane — they describe how much
load reaches the cartridge.

## Answering sizing questions well

Ask for what you actually need and nothing more:

- **Volume in hectolitres** — the unit these capacities are quoted in. Convert
  litres or bottles before calculating, and say that you did.
- **Current turbidity in NTU** — determines the entry stage. If the user does not
  know it, say that the stage cannot be chosen without it and recommend measuring;
  do not guess a stage from the wine's description.
- **Product type** — wine and spirits use disjoint grade families (AF/XE vs XS).

Report the answer as a sheet count per grade, with the capacity that produced it
visible, so the number can be checked. Flag when a requested volume implies an
unusually large train — the practical limit is the filter housing's plate count,
not the arithmetic.

## Reference

`references/filter-grades.md` — the full grade table with flow rates, pressure
limits, micron ratings, and stage assignments for both cascades.

Grades and capacities in this skill are FILTROX product specifications as
distributed by ENOTECH Georgia. Verify against the current FILTROX datasheet
before committing to a purchase — specifications are revised between product
generations, and this skill is a sizing aid, not a datasheet.
