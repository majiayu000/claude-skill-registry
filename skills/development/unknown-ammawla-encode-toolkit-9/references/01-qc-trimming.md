# QC and Trimming for DNase-seq Data

DNase-seq reads are standard Illumina paired-end reads. Quality control and
trimming follow conventional practices with attention to fragment size.

## Pre-Trimming QC with FastQC

```bash
fastqc --threads 4 --outdir fastqc_raw/ sample_R1.fastq.gz sample_R2.fastq.gz
```

Key checks:
- Per-base quality (expect Phred >28)
- Adapter content (Illumina universal adapter)
- Sequence duplication (DNase-seq libraries can show moderate duplication)
- GC content (should match genome, ~40% for human)

## Adapter Trimming with Trim Galore

```bash
trim_galore \
    --paired \
    --quality 20 \
    --phred33 \
    --length 20 \
    --cores 4 \
    --fastqc \
    --output_dir trim_galore/ \
    sample_R1.fastq.gz \
    sample_R2.fastq.gz
```

### Parameter Rationale

| Parameter | Value | Reason |
|-----------|-------|--------|
| `--quality 20` | Phred 20 | Standard quality cutoff |
| `--length 20` | 20 bp | DNase-seq can have short fragments; keep short reads |
| `--cores 4` | 4 | Parallel processing |

DNase-seq fragments can be very short (sub-nucleosomal), so the minimum
read length after trimming is set lower than typical (20 bp vs 36 bp).

## Post-Trimming Verification

After trimming, verify:
- >95% of reads pass quality filter
- Adapter contamination removed
- Read length distribution shows reads from 20-150 bp

## Fragment Size Distribution Check

After alignment, verify the insert size distribution:

```bash
picard CollectInsertSizeMetrics \
    INPUT=sample.bam \
    OUTPUT=insert_sizes.txt \
    HISTOGRAM_FILE=insert_size_histogram.pdf \
    MINIMUM_PCT=0.05
```

Expected DNase-seq fragment sizes:
- Primary peak: 50-100 bp (sub-nucleosomal, DHS fragments)
- Secondary peak: ~170 bp (mononucleosomal)
- Tail extending to 500+ bp
- If no sub-nucleosomal peak, library may have size-selection issues

## Single-End vs Paired-End

ENCODE DNase-seq data exists in both SE and PE formats:

For single-end data, trim with:
```bash
trim_galore \
    --quality 20 \
    --phred33 \
    --length 20 \
    --cores 4 \
    --fastqc \
    sample.fastq.gz
```

Paired-end is preferred for:
- Better duplicate detection
- Insert size QC
- Fragment-level analysis
- Footprinting (requires properly paired reads)
