---
name: plot-analysis
description: Comprehensive Polish plot evaluation with full due diligence (~20-30 min). Use when user wants deep analysis of a property listing after initial triage, or needs complete risk assessment for a finalist plot.
argument-hint: [Otodom-URL|listing-URL]
allowed-tools: WebFetch, WebSearch, Read, Grep
---

# Plot Analysis: $ARGUMENTS

Comprehensive evaluation for 2-3 finalist plots before site visits.

## Critical Requirements

- Every fact must cite source: [Listing], [KW: number Dział X], [Geoportal], [KB: filename:line]
- No hallucinated data - if unavailable, state "NOT VERIFIED"
- Complete cost projection including hidden costs
- Risk assessment across all categories

## Workflow Overview

### Phase 1: Data Extraction

Fetch listing and load regional benchmarks from KB files.

**Key files:**

- `findings/home-building-poland/finding-building-plot-poland-guide.md` (lines 337-347: price benchmarks, 161-168: utility costs)
- `findings/home-building-poland/research-building-house-vs-buying-flat-poland-krakow.md` (lines 13-21: construction costs, 131: hidden costs)

See [data-extraction.md](data-extraction.md) for detailed extraction checklist.

### Phase 2: Legal & Zoning

Verify KW (Księga Wieczysta) sections I-IV and MPZP status.

**Critical checks:**

- Dział II: ownership clarity
- Dział III: easements (służebności)
- Dział IV: mortgages (hipoteki transfer with property!)
- MPZP: MN = good, R/ZL = bad

See [legal-zoning.md](legal-zoning.md) for KW analysis guide and MPZP symbols.

### Phase 3: Infrastructure & Costs

Calculate true total cost including utilities, construction, hidden costs.

**Cost formula:**

```text
Land + tax (2%) + notary (~2k)
+ Utilities (0-50k+ depending on status)
+ Construction (120m² × 5,875 PLN/m² = ~705k)
+ Hidden costs (25-40% = ~211k)
= Total ~900k-1,100k PLN
```

See [infrastructure-costs.md](infrastructure-costs.md) for detailed projections.

### Phase 4: Risk Assessment

Evaluate 4 risk categories: Environmental, Financial, Legal, Technical.

**Auto-reject conditions:**

- ❌ Flood zone (Geoportal check)
- ❌ Non-asphalt road
- ❌ Plot <1000m² or >1500m²
- ❌ KW Dział IV mortgages without resolution

See [risk-assessment.md](risk-assessment.md) for full risk matrix.

### Phase 5: Personal Fit

Evaluate against personal criteria: transport, woods proximity, buildability.

**Must-haves:**

- No flood zones
- Asphalt road
- 1000-1500m² plot
- Good transport to Kraków

See [personal-fit.md](personal-fit.md) for transport ratings and scoring.

## Output Format

Use template in [output-templates.md](output-templates.md) for final report structure.

**Verdict options:** STRONG BUY / CONDITIONAL BUY / PASS

## Verification Checklist

Before submitting:

- [ ] All price claims cite KB benchmarks?
- [ ] KW sections (I-IV) all addressed?
- [ ] Utilities cost uses KB ranges (161-168)?
- [ ] Hidden costs 25-40% applied?
- [ ] Flood zone checked?
- [ ] Road type verified (asphalt required)?
- [ ] Plot size 1000-1500m² confirmed?
- [ ] Transport rating from KB?
- [ ] All must-haves PASS before recommending?
- [ ] No hallucinated data?
