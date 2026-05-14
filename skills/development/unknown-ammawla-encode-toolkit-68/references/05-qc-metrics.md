# Stage 5: QC Metrics and Signal Tracks

## Signal Track Generation

```bash
# Normalized signal using deeptools (RPKM normalization)
bamCoverage -b final.bam -o signal.bw \
  --normalizeUsing RPKM --binSize 10 \
  --numberOfProcessors 8 --extendReads

# NFR-only signal track
bamCoverage -b nfr.bam -o nfr_signal.bw \
  --normalizeUsing RPKM --binSize 10 \
  --numberOfProcessors 8 --extendReads
```

## TSS Enrichment Score

The most important ATAC-seq quality metric. Measures enrichment at transcription
start sites relative to flanking regions.

```bash
# Using deeptools
computeMatrix reference-point -S signal.bw \
  -R tss.bed -a 2000 -b 2000 \
  --referencePoint TSS -o tss_matrix.gz

plotProfile -m tss_matrix.gz -o tss_enrichment.pdf \
  --perGroup --refPointLabel TSS

# TSS enrichment score = max(TSS signal) / mean(flanking signal)
```

| TSS Score | Quality | ENCODE Standard |
|-----------|---------|-----------------|
| >=7 | Excellent | Pass |
| 5-7 | Good | Pass (ENCODE minimum = 5) |
| 3-5 | Marginal | Borderline |
| <3 | Poor | Fail |

## Fragment Size Distribution

```bash
# Using Picard CollectInsertSizeMetrics
picard CollectInsertSizeMetrics \
  INPUT=final.bam OUTPUT=insert_sizes.txt \
  HISTOGRAM_FILE=insert_sizes.pdf

# Using deeptools bamPEFragmentSize
bamPEFragmentSize -b final.bam -o fragment_sizes.pdf \
  --maxFragmentLength 1000 --numberOfProcessors 4
```

Expected pattern: peaks at ~200 bp (NFR), ~400 bp (mono-nuc), ~600 bp (di-nuc).

## Comprehensive QC Metrics Table

| Metric | Tool | Threshold | Stage |
|--------|------|-----------|-------|
| Total reads | samtools flagstat | >=50M recommended | 1 |
| Mapping rate | samtools flagstat / Bowtie2 | >80% | 2 |
| Mitochondrial fraction | samtools idxstats | <20% | 3 |
| NRF | Picard | >=0.8 | 3 |
| PBC1 | Picard | >=0.8 | 3 |
| TSS enrichment | deeptools | >=5 | 5 |
| FRiP | custom | >=0.3 | 4 |
| NFR fraction | fragment size distribution | >40% | 3 |
| IDR optimal peaks | IDR | >50,000 | 4 |

## ataqv (ATAC-seq QC)

Comprehensive ATAC-seq-specific QC tool from Parker Lab (Orchard et al. 2020):

```bash
ataqv --peak-file peaks.narrowPeak --tss-file tss.bed \
  --name sample_name --metrics-file sample.ataqv.json \
  human final.bam

# Generate HTML report
mkarv my_ataqv_report/ sample.ataqv.json
```

ataqv reports: TSS enrichment, fragment length distribution, peak metrics,
mitochondrial fraction, and duplicate rate in a single interactive report.

## MultiQC Aggregated Report

```bash
multiqc . -o multiqc_report/ -f
```

Aggregates FastQC, Picard, Bowtie2, and MACS2 outputs into a single HTML report.
