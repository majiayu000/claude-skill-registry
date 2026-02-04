---
name: campaign-manager
description: >
  Goal-oriented binder design campaign planning and health assessment.
  Use this skill when: (1) Planning a complete binder design campaign,
  (2) Converting high-level goals into runnable pipelines,
  (3) Assessing campaign health and pass rates,
  (4) Diagnosing why designs are failing QC,
  (5) Estimating time, cost, and expected yields,
  (6) Selecting between design tools for a specific target.

  This skill orchestrates the other protein design tools.
  For individual tool parameters, use the specific tool skills.
license: MIT
category: orchestration
tags: [planning, campaign, coordination]
---

# Campaign Manager

## Goal-oriented design

### From goal to pipeline

When user says: "I need 10 good binders for EGFR"

**Campaign Planning:**
```
Goal: 10 high-quality binders for EGFR
├── Achievable: Yes (standard target)
├── Recommended pipeline: rfdiffusion → proteinmpnn → colabfold → protein-qc
├── Estimated designs needed: 500 backbones (to get ~50 passing QC)
├── Estimated time: 8-12 hours total
├── Estimated cost: ~$60 (Modal GPU compute)
└── Expected yield:
    ├── After backbone (500): 500 structures
    ├── After sequence (×8): 4,000 sequences
    ├── After validation: 4,000 predictions
    ├── After QC (~10-15%): 400-600 candidates
    └── After clustering: 10-20 diverse final designs
```

---

## Complete pipeline generator

### Standard miniprotein binder campaign

```bash
# Step 1: Fetch and prepare target (5 min)
curl -o target.pdb "https://files.rcsb.org/download/{PDB_ID}.pdb"
# Trim to binding region if needed

# Step 2: Generate backbones (2-3h, ~$15)
modal run modal_rfdiffusion.py \
  --pdb target.pdb \
  --contigs "A1-150/0 70-100" \
  --hotspot "A45,A67,A89" \
  --num-designs 500

# Checkpoint: ls output/*.pdb | wc -l  # Should be 500

# Step 3: Design sequences (1-2h, ~$10)
for f in output/*.pdb; do
  modal run modal_proteinmpnn.py \
    --pdb-path "$f" \
    --num-seq-per-target 8 \
    --sampling-temp 0.1
done

# Checkpoint: grep -c "^>" output/seqs/*.fa  # Should be ~4000

# Step 4: Quick ESM2 filter (30 min, ~$5, optional)
modal run modal_esm.py --fasta output/all_seqs.fa --mode pll
# Filter sequences with PLL < 0.0

# Step 5: Structure validation (3-4h, ~$35)
modal run modal_colabfold.py \
  --input-faa output/filtered_seqs.fa \
  --out-dir predictions/

# Checkpoint: find predictions -name "*rank_001.pdb" | wc -l

# Step 6: Filter and rank (protein-qc skill)
# Apply thresholds: pLDDT > 0.85, ipTM > 0.5, scRMSD < 2.0
# Compute composite score
# Cluster at 70% identity, select top from each cluster
```

**Total estimated time**: 8-12 hours
**Total estimated cost**: ~$60-70

---

## Campaign size recommendations

| Goal | Backbones | Sequences/BB | Total Seq | Expected Passing |
|------|-----------|--------------|-----------|------------------|
| 5 binders | 200 | 8 | 1,600 | 160-240 |
| 10 binders | 500 | 8 | 4,000 | 400-600 |
| 20 binders | 1,000 | 8 | 8,000 | 800-1,200 |
| 50 binders | 2,500 | 8 | 20,000 | 2,000-3,000 |

**Rule of thumb**: Generate 50x more designs than you need (10-15% pass rate × clustering).

---

## Tool selection guide

### When to use each tool

| Scenario | Recommended Tool | Reason |
|----------|------------------|--------|
| Standard miniprotein | RFdiffusion + ProteinMPNN | High diversity, proven |
| Need higher success rate | BindCraft | Integrated design loop |
| All-atom precision needed | BoltzGen | Side-chain aware |
| Difficult target | ColabDesign | AF2 gradient optimization |
| Need fast iteration | ESMFold + ESM2 | Quick screening |

### Target difficulty assessment

| Indicator | Easy Target | Difficult Target |
|-----------|-------------|------------------|
| Surface type | Concave pocket | Flat or convex |
| Conservation | High | Low |
| Known binders | Yes | No |
| Flexibility | Rigid | Flexible |
| Expected pass rate | 15-20% | 5-10% |

---

## Campaign health assessment

### Quick metrics check

```python
import pandas as pd

def assess_campaign(csv_path):
    df = pd.read_csv(csv_path)

    # Calculate pass rates
    plddt_pass = (df['pLDDT'] > 0.85).mean()
    iptm_pass = (df['ipTM'] > 0.50).mean()
    scrmsd_pass = (df['scRMSD'] < 2.0).mean()
    all_pass = ((df['pLDDT'] > 0.85) & (df['ipTM'] > 0.5) & (df['scRMSD'] < 2.0)).mean()

    # Determine health
    if all_pass > 0.15:
        health = "EXCELLENT"
    elif all_pass > 0.10:
        health = "GOOD"
    elif all_pass > 0.05:
        health = "MARGINAL"
    else:
        health = "POOR"

    # Identify top issue
    issues = []
    if plddt_pass < 0.20:
        issues.append("Low pLDDT - backbone or sequence issue")
    if iptm_pass < 0.20:
        issues.append("Low ipTM - hotspot or interface issue")
    if scrmsd_pass < 0.50:
        issues.append("High scRMSD - sequence doesn't specify backbone")

    return {
        "health": health,
        "overall_pass_rate": all_pass,
        "plddt_pass_rate": plddt_pass,
        "iptm_pass_rate": iptm_pass,
        "scrmsd_pass_rate": scrmsd_pass,
        "top_issues": issues
    }
```

### Interpreting results

| Health | Pass Rate | Action |
|--------|-----------|--------|
| EXCELLENT | > 15% | Proceed to selection |
| GOOD | 10-15% | Proceed, normal yield |
| MARGINAL | 5-10% | Review failure tree |
| POOR | < 5% | Diagnose and restart |

---

## Cost estimation

### Per-tool costs (Modal)

| Tool | GPU | $/hour | Typical Job | Cost |
|------|-----|--------|-------------|------|
| RFdiffusion | A10G | ~$1.20 | 500 designs/2h | ~$2.50 |
| ProteinMPNN | T4 | ~$0.60 | 4000 seq/1.5h | ~$1.00 |
| ESM2 (PLL) | A10G | ~$1.20 | 4000 seq/30min | ~$0.60 |
| ColabFold | A100 | ~$4.50 | 4000 preds/4h | ~$18.00 |
| Chai | A100 | ~$4.50 | 500 preds/1h | ~$4.50 |

### Campaign cost estimates

| Campaign Size | Total Cost | Notes |
|---------------|------------|-------|
| Small (100 bb) | ~$15 | Quick exploration |
| Standard (500 bb) | ~$60 | Most campaigns |
| Large (1000 bb) | ~$120 | Comprehensive |
| XL (5000 bb) | ~$600 | Very thorough |

---

## Pipeline variants

### High-throughput (maximize diversity)

```bash
# More backbones, fewer sequences each
modal run modal_rfdiffusion.py --num-designs 2000
modal run modal_proteinmpnn.py --num-seq-per-target 4 --sampling-temp 0.2
```

### High-quality (maximize per-design quality)

```bash
# Fewer backbones, more sequences each, lower temperature
modal run modal_rfdiffusion.py --num-designs 200
modal run modal_proteinmpnn.py --num-seq-per-target 32 --sampling-temp 0.1
```

### Quick exploration (fast iteration)

```bash
# Small batch, ESMFold instead of ColabFold
modal run modal_rfdiffusion.py --num-designs 50
modal run modal_proteinmpnn.py --num-seq-per-target 8
modal run modal_esmfold.py --fasta all_seqs.fa  # Faster than ColabFold
```

---

## See also

- Tool-specific parameters: `rfdiffusion`, `proteinmpnn`, `colabfold`, `chai`, `boltz`
- QC thresholds and filtering: `protein-qc`
- Tool selection guidance: `binder-design`
