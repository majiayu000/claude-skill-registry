# Stage 4: Peak Calling and IDR

## Tools
- **MACS2 v2.2.7+**: Peak caller (Zhang et al. 2008)
- **IDR v2.0.4+**: Irreproducible Discovery Rate (Li et al. 2011)

## MACS2 Parameters for ATAC-seq

ATAC-seq peak calling differs from ChIP-seq in several key ways:
1. **No control/input file** -- peaks are called against local background
2. **Shift and extension** -- correct for Tn5 insertion site
3. **Use NFR BAM only** -- nucleosome-free fragments for accessibility peaks

| Parameter | Value | Notes |
|-----------|-------|-------|
| `--format` | BAMPE | Use actual fragment sizes |
| `--gsize` | hs (2.7e9) | Use mm for mouse |
| `--nomodel` | yes | Do not build shifting model |
| `--shift` | -75 | Center on Tn5 cut site |
| `--extsize` | 150 | Extend to 150bp from cut site |
| `--qvalue` | 0.05 | FDR threshold |
| `--keep-dup` | all | Already deduplicated |
| `--call-summits` | yes | Identify sub-peak summits |
| `-B` | yes | Generate bedGraph for signal |

**Note**: When using BAMPE format with Tn5-shifted BAM, the `--shift` and `--extsize`
parameters are not needed because BAMPE uses actual fragment coordinates. Use them
only when calling peaks on BED format or single-end data.

## Commands

```bash
# Peak calling on NFR fragments (primary)
macs2 callpeak -t nfr.bam \
  -f BAMPE -g hs -n sample_nfr \
  --nomodel --keep-dup all --call-summits \
  --qvalue 0.05 -B

# Alternative: Peak calling on all fragments with shift correction
macs2 callpeak -t final.bam \
  -f BAMPE -g hs -n sample_all \
  --nomodel --keep-dup all --call-summits \
  --qvalue 0.05 -B

# IDR on true replicates
idr --samples rep1_peaks.narrowPeak rep2_peaks.narrowPeak \
  --input-file-type narrowPeak \
  --rank p.value \
  --output-file idr_peaks.txt \
  --plot \
  --idr-threshold 0.05
```

## IDR Interpretation

| Metric | Expected (Good) | Concern |
|--------|-----------------|---------|
| IDR peaks (0.05 threshold) | 50,000-150,000 | <30,000 suggests poor signal |
| Rescue ratio | <2 | >2 suggests replicate discordance |
| Self-consistency ratio | <2 | >2 suggests noisy data |

## QC Checkpoints

| Check | Threshold | Action if Failed |
|-------|-----------|------------------|
| FRiP | >=0.3 (ATAC-seq standard) | Poor accessibility signal |
| Peak count | >50,000 (IDR filtered) | Low enrichment |
| Peak width distribution | Median 200-500 bp | Check if calling mode correct |
| Peaks at TSS | Enrichment visible | Fundamental ATAC-seq signal |

## Notes

- ATAC-seq FRiP is typically much higher than ChIP-seq (0.3-0.6 vs 0.01-0.1)
  because open chromatin is a large fraction of the genome.
- Always call peaks on NFR fragments for accessibility analysis.
- For nucleosome positioning, use the mono-nucleosomal fragments separately.
- IDR is standard for ATAC-seq with biological replicates.
