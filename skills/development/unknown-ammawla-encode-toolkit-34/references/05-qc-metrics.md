# Stage 5: QC Metrics and Signal Tracks

## Signal Track Generation

Signal tracks provide normalized coverage for genome browser visualization.

```bash
# Fold change over control (preferred for visualization)
macs2 bdgcmp -t treatment_pileup.bdg -c control_lambda.bdg \
  -o fc.bdg -m FE
sort -k1,1 -k2,2n fc.bdg > fc.sorted.bdg
bedGraphToBigWig fc.sorted.bdg chrom.sizes fc.bw

# Signal p-value track (statistical significance)
macs2 bdgcmp -t treatment_pileup.bdg -c control_lambda.bdg \
  -o pval.bdg -m ppois
sort -k1,1 -k2,2n pval.bdg > pval.sorted.bdg
bedGraphToBigWig pval.sorted.bdg chrom.sizes pval.bw
```

## Strand Cross-Correlation (phantompeakqualtools)

Computes NSC and RSC metrics that measure ChIP enrichment quality independent of
peak calling. Reference: Kharchenko et al. 2008; Landt et al. 2012.

```bash
run_spp.R -c=final.bam -savp=cc_plot.pdf -out=cc_scores.txt -tmpdir=tmp/
# Output columns: filename, numReads, estFragLen, corr_estFragLen,
#                 phantomPeak, corr_phantomPeak, argmin_corr, min_corr,
#                 NSC, RSC, QualityTag
```

## Comprehensive QC Metrics Table

| Metric | Tool | Threshold | Stage |
|--------|------|-----------|-------|
| Total reads | samtools flagstat | Record | 1 |
| Mapped reads | samtools flagstat | >=20M TF / >=45M histone | 2 |
| Mapping rate | samtools flagstat | >80% | 2 |
| NRF | Picard | >=0.8 | 3 |
| PBC1 | Picard | >=0.8 | 3 |
| PBC2 | Picard | >=3 | 3 |
| NSC | phantompeakqualtools | >1.05 | 5 |
| RSC | phantompeakqualtools | >0.8 | 5 |
| FRiP | custom calculation | >=1% | 4 |
| IDR peaks | IDR | >20,000 (TF) | 4 |
| Duplication rate | Picard | <30% | 3 |

## FRiP Calculation

```bash
# Count reads in peaks
READS_IN_PEAKS=$(bedtools intersect -a final.bam -b peaks.narrowPeak -u -f 0.20 | \
  samtools view -c -)
TOTAL_READS=$(samtools view -c final.bam)
FRIP=$(echo "scale=4; $READS_IN_PEAKS / $TOTAL_READS" | bc)
echo "FRiP: $FRIP"
```

## MultiQC Aggregated Report

```bash
multiqc . -o multiqc_report/ -f
```

MultiQC aggregates outputs from FastQC, Picard, samtools stats, and MACS2
into a single interactive HTML report. This is the primary deliverable for
QC review before proceeding to downstream analysis.

## Fingerprint Plot (deeptools)

```bash
plotFingerprint -b treatment.bam control.bam \
  --labels ChIP Input \
  --plotFile fingerprint.pdf \
  --outRawCounts fingerprint_counts.txt
```

The fingerprint plot visually shows enrichment: a good ChIP sample curves away
from the diagonal (uniform coverage), while input stays close to the diagonal.
