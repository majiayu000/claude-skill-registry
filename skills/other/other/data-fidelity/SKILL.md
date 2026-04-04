---
name: data-fidelity
description: Fact-checking and source verification workflow for research documents. Launches parallel fact-checkers, aggregates findings, applies corrections systematically.
version: 1.0.0
---

# Data Fidelity

Activates when research documents need verification, fact-checking, or data updates.

## When to Use

- After initial research documents are written (quality gate before publish)
- When refreshing documents with current data (market prices, company stats)
- When a user says "check for errors", "verify claims", "fact check", "add fidelity"

## Workflow

### Phase 1: Fact-Check Fleet
Launch 2-3 parallel fact-checker agents, each covering a different document range:
- Agent A: docs 01-12
- Agent B: docs 13-24
- Agent C: forward-looking/speculative docs (if any)

### Phase 2: Aggregate Findings
Collect reports. Categorize by severity:
- **ERROR** — factually wrong, must fix
- **QUESTIONABLE** — might be wrong, needs verification
- **INCONSISTENCY** — contradicts another document

### Phase 3: Data Refresh
Launch market-researcher agents for current pricing, company data, and industry stats.

### Phase 4: Apply Corrections
Systematic edit pass:
1. Fix all ERRORs first
2. Resolve INCONSISTENCYs (pick the correct value, update all occurrences)
3. Update data with fresh market research
4. Flag QUESTIONABLE items that couldn't be resolved

### Phase 5: Rebuild
If documents have HTML/PDF output, rebuild after corrections:
```bash
bash build.sh
```

## Quality Standards

- Every numerical claim should have a source or explicit reasoning
- Cross-document consistency: same number must be the same everywhere
- Dates should be specific (not "recently" — say "March 2026")
- Company names should be current (post-merger names, current HQ)
- Legal citations should include statute number (USC, CFR, RCW)
