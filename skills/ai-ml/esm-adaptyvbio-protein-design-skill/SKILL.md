---
name: esm
description: >
  ESM2 protein language model for embeddings and sequence scoring.
  Use this skill when: (1) Computing pseudo-log-likelihood (PLL) scores,
  (2) Getting protein embeddings for clustering,
  (3) Filtering designs by sequence plausibility,
  (4) Zero-shot variant effect prediction,
  (5) Analyzing sequence-function relationships.

  For structure prediction, use chai or boltz.
  For QC thresholds, use protein-qc.
license: MIT
category: design-tools
tags: [sequence-design, embeddings, scoring]
proteinbase_slug: esm2-optimization
proteinbase_url: https://proteinbase.com/design-methods/esm2-optimization
biomodals_script: modal_esm2_predict_masked.py
---

# ESM2 Protein Language Model

## Prerequisites

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Python | 3.8+ | 3.10 |
| PyTorch | 1.10+ | 2.0+ |
| CUDA | 11.0+ | 11.7+ |
| GPU VRAM | 8GB | 24GB (A10G) |
| RAM | 16GB | 32GB |

## How to run

> **First time?** See [Installation Guide](../../docs/installation.md) to set up Modal and biomodals.

### Option 1: Modal
```bash
cd biomodals
modal run modal_esm2_predict_masked.py \
  --input-faa sequences.fasta \
  --out-dir embeddings/
```

**GPU**: A10G (24GB) | **Timeout**: 300s default

### Option 2: Python API (recommended)
```python
import torch
import esm

# Load model
model, alphabet = esm.pretrained.esm2_t33_650M_UR50D()
batch_converter = alphabet.get_batch_converter()
model = model.eval().cuda()

# Process sequences
data = [("seq1", "MKTAYIAKQRQISFVK...")]
batch_labels, batch_strs, batch_tokens = batch_converter(data)

with torch.no_grad():
    results = model(batch_tokens.cuda(), repr_layers=[33])

# Get embeddings
embeddings = results["representations"][33]
```

## Key parameters

### ESM2 Models

| Model | Parameters | Speed | Quality |
|-------|------------|-------|---------|
| esm2_t6_8M | 8M | Fastest | Fast screening |
| esm2_t12_35M | 35M | Fast | Good |
| esm2_t33_650M | 650M | Medium | Better |
| esm2_t36_3B | 3B | Slow | Best |

## Output format

```
embeddings/
├── embeddings.npy       # (N, 1280) array
├── pll_scores.csv       # PLL for each sequence
└── metadata.json        # Sequence info
```

## Sample output

### Successful run
```
$ modal run modal_esm2_predict_masked.py --input-faa designs.fasta
[INFO] Loading ESM2-650M model...
[INFO] Processing 100 sequences...
[INFO] Computing pseudo-log-likelihood...

embeddings/pll_scores.csv:
sequence_id,pll,pll_normalized,length
design_0,-0.82,0.15,78
design_1,-0.95,0.08,85
design_2,-1.23,-0.12,72
...

Summary:
  Mean PLL: -0.91
  Sequences with PLL > 0: 42/100 (42%)
```

**What good output looks like:**
- PLL_normalized: > 0.0 (more natural-like)
- Embeddings shape: (N, 1280) for 650M model
- Higher PLL = more natural sequence

## Decision tree

```
Should I use ESM2?
│
├─ What do you need?
│  ├─ Sequence plausibility score → ESM2 PLL ✓
│  ├─ Embeddings for clustering → ESM2 ✓
│  ├─ Variant effect prediction → ESM2 ✓
│  └─ Structure prediction → Use ESMFold
│
├─ What model size?
│  ├─ Fast screening → esm2_t12_35M
│  ├─ Standard use → esm2_t33_650M ✓
│  └─ Best quality → esm2_t36_3B
│
└─ Use case?
   ├─ QC filtering → PLL > 0.0 threshold
   ├─ Diversity analysis → Mean-pooled embeddings
   └─ Mutation scanning → Per-position log-odds
```

## PLL interpretation

| Normalized PLL | Interpretation |
|----------------|----------------|
| > 0.2 | Very natural sequence |
| 0.0 - 0.2 | Good, natural-like |
| -0.5 - 0.0 | Acceptable |
| < -0.5 | May be unnatural |

## Typical performance

| Campaign Size | Time (A10G) | Cost (Modal) | Notes |
|---------------|-------------|--------------|-------|
| 100 sequences | 5-10 min | ~$1 | Quick screen |
| 1000 sequences | 30-60 min | ~$5 | Standard |
| 5000 sequences | 2-3h | ~$20 | Large batch |

**Throughput**: ~100-200 sequences/minute with 650M model.

---

## Verify

```bash
wc -l embeddings/pll_scores.csv  # Should match input + 1 (header)
```

---

## Troubleshooting

**OOM errors**: Use smaller model or batch sequences
**Slow processing**: Use esm2_t12_35M for speed
**Low PLL scores**: May indicate unusual/designed sequences

### Error interpretation

| Error | Cause | Fix |
|-------|-------|-----|
| `RuntimeError: CUDA out of memory` | Sequence too long or large batch | Reduce batch size |
| `KeyError: representation` | Wrong layer requested | Use layer 33 for 650M model |
| `ValueError: sequence` | Invalid amino acid | Check for non-standard AAs |

---

**Next**: Structure prediction with `chai` or `boltz` → `protein-qc` for filtering.
