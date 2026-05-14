# TF Footprinting Analysis for DNase-seq

Transcription factor footprinting detects protein-DNA interactions from
DNase-seq cleavage patterns. Bound TFs protect DNA from cleavage, creating
a "footprint" -- a local depression in the DNase-seq signal.

## Prerequisites

Reliable footprinting requires:
- **Deep sequencing**: >100 million uniquely mapped reads
- **Paired-end data**: Better resolution than single-end
- **High SPOT score**: >0.4 (clean signal)
- **Peak calls**: DHS regions from Hotspot2

## HINT-ATAC Footprinting

HINT-ATAC (from the Regulatory Genomics Toolbox) works for both DNase-seq
and ATAC-seq data:

```bash
rgt-hint footprinting \
    --dnase-seq \
    --paired-end \
    --organism hg38 \
    --output-location footprints/ \
    --output-prefix sample \
    sample_final.bam \
    sample.DHS.narrowPeak
```

### Key Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| `--dnase-seq` | Flag | Use DNase-seq cleavage model (not ATAC-seq) |
| `--paired-end` | Flag | Use paired-end fragment information |
| `--organism` | hg38 | Genome build for bias correction |

**Important**: Use `--dnase-seq` for DNase-seq data and `--atac-seq` for
ATAC-seq data. They have different cleavage bias models.

## Motif Matching in Footprints

After calling footprints, match to known TF motifs:

```bash
rgt-motifanalysis matching \
    --organism hg38 \
    --input-files footprints/sample.bed \
    --output-location motif_matches/ \
    --motif-dbs /ref/JASPAR2024_CORE_vertebrates.meme
```

## Wellington Footprinting (Alternative)

Wellington uses a different statistical approach for footprint detection:

```bash
wellington_footprints.py \
    -A \
    -p 20 \
    -fdrlimit 0.01 \
    sample.DHS.narrowPeak \
    sample_final.bam \
    wellington_out/
```

### HINT vs Wellington Comparison

| Feature | HINT-ATAC | Wellington |
|---------|-----------|-----------|
| Bias correction | Sequence-specific | Position-based |
| Speed | Moderate | Fast |
| Sensitivity | Higher | More conservative |
| DNase + ATAC | Both | Both |
| Active development | Yes | Limited |

## Footprint Quality Assessment

### Per-Motif Footprint Depth

```bash
# Calculate average footprint depth at known CTCF sites
bedtools intersect \
    -a CTCF_motif_sites.bed \
    -b footprints/sample.bed \
    -wa -wb \
    | awk '{print $NF}' \
    | awk '{sum+=$1; n++} END {print "Mean CTCF footprint score:", sum/n}'
```

### Footprint vs Background Signal Ratio

Good footprints show:
- Clear signal depression at the motif center
- Flanking shoulders of higher cleavage
- Depth-to-flank ratio > 1.5

### Expected Footprint Counts

| Sequencing Depth | Expected Footprints |
|------------------|---------------------|
| 50M reads | Unreliable |
| 100M reads | 50,000-100,000 |
| 200M reads | 100,000-200,000 |
| 500M reads | 200,000-400,000 |

## Aggregate Footprint Visualization

Generate aggregate footprint profiles across all instances of a motif:

```bash
# Using HINT differential footprinting
rgt-hint differential \
    --organism hg38 \
    --bc \
    --nc 8 \
    --mpbs-files motif_matches/sample_mpbs.bed \
    --reads-files sample_final.bam \
    --conditions sample \
    --output-location diff_footprints/
```

This produces per-motif aggregate profiles showing the average cleavage
pattern across all binding sites, which is more robust than individual
footprint calls.

## Comparison with Vierstra 2020 Reference Map

The Vierstra et al. 2020 reference map provides a global catalog of human
TF footprints from 243 DNase-seq datasets. Use it to:

1. Validate your footprint calls
2. Compare tissue-specific footprinting
3. Identify novel TF binding events

```bash
# Download Vierstra reference footprints
# Available at: https://www.vierstra.org/resources/dgf

# Compare overlap
bedtools intersect \
    -a footprints/sample.bed \
    -b vierstra_consensus_footprints.bed \
    -u | wc -l
```
