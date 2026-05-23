---
name: ieee-pes-paper-reviewer
description: Comprehensive IEEE PES paper review for Physics-Guided SSL GNN power grid research. Use when reviewing paper sections, checking claims against evidence, validating physics consistency (PF/Line Flow/Cascade), auditing figures/tables, checking IEEE compliance, or positioning against competing work (PPGT). Triggers on "review my paper", "check claims", "validate physics", "PES submission ready", "compare to baselines", "audit figures", or any publication preparation task.
---

# IEEE PES Paper Reviewer

Reviews Physics-Guided SSL GNN power grid papers for PES General Meeting submission.

## Project Context

**Paper**: Self-supervised GNN with physics-guided message passing for power grids
**Tasks**: Power Flow prediction, Line Flow prediction (NOT OPF), Cascading Failure prediction
**Key Claims**: 
- +29.1% MAE (PF), +26.4% MAE (Line Flow) at 10% labels
- SSL stabilizes IEEE-118 training (σ: 0.243→0.051)
- 0.93 AUC-ROC explainability via Integrated Gradients
- ~274K params vs. 2-15M for PPGT

**Validation**: 5-seed experiments, IEEE-24 and IEEE-118 benchmarks

## Review Modes

Invoke with: `MODE: [mode-name]`

### MODE: compliance
IEEE PES GM formatting and submission readiness.

**Check**:
- Page limit (8 pages max for conference, 10 for journal)
- IEEE column format, margins, fonts
- All figures/tables referenced in text
- No broken citations ([?] errors)
- Abstract ≤200 words, includes quantitative results
- Author information complete

**Output**: PASS/FAIL table with fix locations (section/line)

### MODE: shadow-review
Simulate Reviewer #2 (tough but constructive).

**Evaluate** (1-10 each):
- Novelty vs. PPGT and prior GNN-for-grid work
- Technical soundness (physics formulation correctness)
- Experimental rigor (seed count, baselines, stat tests)
- Clarity and organization
- Reproducibility (configs, commands, data access)

**Output**:
1. 5 major issues with evidence locations and fixes
2. 8 minor issues with quick fixes
3. Rewritten abstract (≤200 words)
4. Acceptance risk: LOW/MED/HIGH

### MODE: claims-audit
Verify every claim maps to evidence.

**For each claim, record**:
- Location (Section X / Table Y / Figure Z)
- Type: performance | generalization | efficiency | novelty
- Evidence pointer (table cell, figure panel, log file)
- Risk: LOW/MED/HIGH
- Conservative rewrite if HIGH risk

**Output**: JSON ledger + patch set for HIGH-risk claims

### MODE: physics-check
Power systems domain correctness.

**Validate**:
- PF formulation (DC vs AC, per-unit, slack bus handling)
- Line Flow equations (not confused with OPF!)
- Cascade failure model (protection relay logic, N-k contingency)
- Graph construction (admittance matrix, topology encoding)
- Train/test split physical realism (no future leakage)

**Output**: Assumptions list, consistency issues ranked, 8+ sanity checks

### MODE: reproducibility
Can another lab reproduce this?

**Check**:
- Seeds specified and consistent across tables
- Dataset versions and preprocessing documented
- Training commands explicit
- Config files complete (base.yaml, splits.yaml)
- Expected outputs documented

**Output**: P0/P1/P2 blockers, minimum repro package checklist

### MODE: figures-tables
Visual storytelling and caption quality.

**Evaluate each figure/table**:
- Purpose clear?
- Self-contained caption?
- Referenced in text?
- IEEE figure quality (300 DPI, vector preferred)?

**Output**: Inventory table (KEEP/CUT/REWORK), rewritten captions, "killer figure" recommendation

### MODE: positioning
Novelty framing vs. prior art.

**Compare against**:
- PPGT (Physics-informed Pre-trained Graph Transformer)
- Other GNN-for-power-systems work
- Standard ML baselines

**Differentiation axes**: Task coverage (Cascade!), param efficiency (274K vs 2-15M), explainability, SSL approach

**Output**: Positioning table, rewritten Related Work paragraphs, novelty paragraph

### MODE: full
Run all modes sequentially. Use for final pre-submission review.

## Guardrails

- Ground EVERY critique in specific section/figure/table
- Label missing information as MISSING with exact data needed
- Conservative scientific tone—no "breakthrough", "novel", "first-ever"
- Reference project files: main.tex, citations.bib, references.bib
- Remember: Line Flow ≠ OPF. The paper does Line Flow prediction.

## Evidence Sources

Check these project files for claims verification:
- `/mnt/project/06_results.tex` — Main results
- `/mnt/project/table_1_main_results.tex` — Core performance table
- `/mnt/project/citations.bib` — Bibliography
- `/mnt/project/Results.md` — Detailed experimental results
- `/mnt/project/Statistical_Tests.md` — Significance testing
