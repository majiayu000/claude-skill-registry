# SignalValue Filtering for Histone Peak Aggregation

Reference guide for per-sample noise filtering using signalValue thresholds, based on Perna et al. 2024 and the corrected quantile computation.

## Background

NarrowPeak/broadPeak files include a **signalValue** column (column 7) representing the enrichment of the ChIP signal over input at each peak. Higher signalValue indicates stronger evidence for true binding. However, peak callers report many weak peaks that are inconsistent across processing pipelines and sequencing depths.

## The Perna et al. 2024 Finding

Perna et al. (2024, BMC Genomics) systematically compared how different processing pipelines affect ChIP-seq peak reproducibility. Key finding:

> Peaks in the **top 75% by signalValue** (above the 25th percentile) are the most reproducible across different aligners, peak callers, and parameter settings. The bottom 25% of peaks by signal are the most variable and least trustworthy.

This provides a principled, per-sample noise filter: remove the weakest quartile of peaks before cross-sample merging.

## Correct Quantile Computation

### The Bug (Fixed)

The original implementation computed 25% of the signalValue **range**, not the true 25th percentile of the **distribution**:

```bash
# WRONG: 25% of range (min to max)
RANGE_25=$(awk 'NR==1{min=$7; max=$7} {if($7<min)min=$7; if($7>max)max=$7} END{print min + 0.25*(max-min)}' file.narrowPeak)
```

This is incorrect because signal distributions are typically right-skewed (many weak peaks, few strong peaks). A range-based threshold retains too many weak peaks.

### The Correct Implementation

Compute the true 25th percentile of the signalValue distribution:

```bash
# CORRECT: True distribution quantile (25th percentile)
TOTAL=$(wc -l < sample.filtered.narrowPeak)
LINE_25=$(echo "$TOTAL" | awk '{printf "%d", $1 * 0.25}')
THRESHOLD=$(sort -k7,7n sample.filtered.narrowPeak | awk -v line="$LINE_25" 'NR==line{print $7}')
awk -v t="$THRESHOLD" '$7 >= t' sample.filtered.narrowPeak > sample.qfiltered.narrowPeak
```

### Numerical Example

Given 10,000 peaks with signalValues ranging from 0.5 to 500:

| Method | Threshold | Peaks Retained | Issue |
|--------|-----------|---------------|-------|
| Range-based (wrong) | 0.5 + 0.25 * (500 - 0.5) = 125.4 | ~200 | Removes 98% of peaks |
| Distribution quantile (correct) | Value at position 2,500 | 7,500 | Removes bottom 25% |

The range-based method is catastrophically wrong for right-skewed distributions. It retains only the very strongest peaks rather than the intended 75%.

## Per-Sample vs Global Threshold

### Why Per-Sample?

Each ChIP-seq experiment has a different signal distribution depending on:
- **Sequencing depth**: Deeper sequencing recovers more peaks but with lower average signal
- **Antibody quality**: Better antibodies produce higher signal-to-noise
- **Library complexity**: Higher complexity yields better peak resolution
- **Lab protocol**: Different crosslinking, sonication, etc.

Applying a single global threshold across all samples biases toward high-signal experiments and discards most peaks from lower-signal (but still valid) experiments.

### Workflow

```
For each sample:
  1. Filter by ENCODE blacklist
  2. Compute the 25th percentile of signalValue for THIS sample
  3. Remove peaks below that sample's threshold
  4. Proceed to cross-sample merging
```

## When to Adjust the Threshold

| Scenario | Threshold | Rationale |
|----------|-----------|-----------|
| Standard aggregation | 25th percentile | Perna et al. 2024 recommendation |
| Conservative (high confidence) | 50th percentile | Top half only, for stringent analyses |
| Permissive (maximum catalog) | 10th percentile | Keep more peaks, accept more noise |
| Very few peaks (<1,000) | No filtering | Small peak sets are already stringent |

## Interaction with Other Filters

The signalValue filter should be applied **after** blacklist filtering and **before** merging:

```
Raw peaks
  -> ENCODE blacklist removal (Amemiya et al. 2019)
  -> SignalValue percentile filter (Perna et al. 2024)
  -> Sample tagging
  -> Cross-sample union merge (bedtools merge)
  -> Confidence annotation
```

## Validation

After filtering, verify the signalValue distribution shifted as expected:

```bash
# Before filtering
awk '{print $7}' sample.filtered.narrowPeak | sort -n | awk 'NR==1{print "Pre-filter min:", $1} END{print "Pre-filter max:", $1}'

# After filtering
awk '{print $7}' sample.qfiltered.narrowPeak | sort -n | awk 'NR==1{print "Post-filter min:", $1} END{print "Post-filter max:", $1}'
```

Use `validate_peaks.py` from the scripts directory to verify file integrity after filtering.

## Alternative Approaches

| Method | Tool | Description | Trade-off |
|--------|------|-------------|-----------|
| SignalValue percentile | Manual (awk) | Per-sample 25th pct | Simple, well-validated |
| IDR (Irreproducible Discovery Rate) | ENCODE pipeline | Cross-replicate concordance | Already applied in ENCODE files |
| MSPC | Jalili et al. 2021 | Rescues weak-but-replicated peaks | More sensitive, requires replicates |
| PBS (Probability-of-Being-Signal) | Hecht et al. 2023 | Read-depth-aware scoring | Best for heterogeneous depths |

When using ENCODE IDR thresholded peaks, the IDR filter has already removed irreproducible peaks. The signalValue filter provides an additional layer of noise reduction beyond IDR.

## References

- Perna et al. 2024, BMC Genomics -- signalValue top 75% most consistent across pipelines
- Hecht et al. 2023, PLoS Computational Biology -- Probability-of-Being-Signal for cross-dataset comparison
- Jalili et al. 2021, BMC Bioinformatics -- MSPC for rescuing weak peaks across replicates
- Li et al. 2011, Annals of Applied Statistics -- IDR framework for reproducibility
