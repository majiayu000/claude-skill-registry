# Stage 4: Peak Calling and IDR

## Tools
- **MACS2 v2.2.7+**: Model-based Analysis of ChIP-Seq (Zhang et al. 2008, ~7,000 citations)
- **IDR v2.0.4+**: Irreproducible Discovery Rate (Li et al. 2011, ~1,500 citations)

## MACS2 Parameters

| Parameter | Narrow (TF) | Broad (Histone) | Notes |
|-----------|-------------|-----------------|-------|
| `--format` | BAMPE | BAMPE | Auto-detect fragment size from PE |
| `--gsize` | hs (2.7e9) | hs (2.7e9) | Use mm for mouse |
| `--qvalue` | 0.05 | 0.05 | FDR threshold |
| `--broad` | no | yes | Broad peak mode for repressive marks |
| `--broad-cutoff` | n/a | 0.1 | Linking threshold for broad peaks |
| `--nomodel` | yes (PE data) | yes (PE data) | Use actual fragment sizes |
| `--keep-dup` | all | all | Already deduplicated in Stage 3 |
| `--call-summits` | yes (narrow) | n/a | Subpeak summit positions |

## Narrow vs Broad Mark Decision

| Peak Type | Targets | Rationale |
|-----------|---------|-----------|
| **Narrow** | H3K4me3, H3K4me1, H3K27ac, H3K9ac, all TFs, CTCF | Punctate binding pattern |
| **Broad** | H3K27me3, H3K36me3, H3K9me3, H3K79me2 | Diffuse domain spreading |

## Commands

```bash
# Narrow peaks (TF and active histone marks)
macs2 callpeak -t treatment.bam -c control.bam \
  -f BAMPE -g hs -n sample_narrow \
  --qvalue 0.05 --nomodel --keep-dup all --call-summits

# Broad peaks (repressive histone marks)
macs2 callpeak -t treatment.bam -c control.bam \
  -f BAMPE -g hs -n sample_broad \
  --broad --broad-cutoff 0.1 --nomodel --keep-dup all

# IDR analysis on true replicates (narrow peaks only)
idr --samples rep1_peaks.narrowPeak rep2_peaks.narrowPeak \
  --input-file-type narrowPeak \
  --rank p.value \
  --output-file idr_peaks.txt \
  --plot \
  --idr-threshold 0.05

# Self-pseudoreplicate IDR (single replicate fallback)
idr --samples pr1_peaks.narrowPeak pr2_peaks.narrowPeak \
  --input-file-type narrowPeak \
  --output-file self_idr_peaks.txt \
  --plot
```

## IDR Interpretation

| Metric | Expected (Good) | Concern |
|--------|-----------------|---------|
| IDR peaks (0.05 threshold) | 50,000-200,000 (TF) | <20,000 suggests poor enrichment |
| Rescue ratio | <2 | >2 suggests replicate discordance |
| Self-consistency ratio | <2 | >2 suggests noisy data |
| IDR / individual rep ratio | 0.3-0.7 | <0.3 very stringent; >0.7 very lenient |

## QC Checkpoints

| Check | Threshold | Action if Failed |
|-------|-----------|------------------|
| FRiP | >=1% | Poor enrichment; check antibody |
| IDR optimal peaks | >20,000 (TF) | Low enrichment or poor replicates |
| Peak count ratio | IDR = 30-70% of rep peaks | Replicate consistency issue |

## Notes

- Always call peaks on individual replicates first, then run IDR to assess reproducibility.
- For broad marks, IDR is not standard practice. Use pooled replicate peak calls instead.
- The `--call-summits` flag identifies subpeak summits within broader peak regions,
  useful for motif analysis downstream.
- FRiP is calculated as: reads overlapping peaks / total reads in filtered BAM.
