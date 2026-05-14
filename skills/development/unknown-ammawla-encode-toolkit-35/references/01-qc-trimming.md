# Stage 1: QC and Trimming

## Input
- Raw FASTQ files (single-end or paired-end)
- Adapter sequences (auto-detected by Trim Galore or specify: Illumina TruSeq)

## Tools
- **FastQC v0.11.9+**: Per-base quality, adapter content, duplication rates, GC content
- **Trim Galore v0.6.7+** (wraps Cutadapt): Adapter trimming + quality filtering

## Parameters

| Parameter | Default | Notes |
|-----------|---------|-------|
| Quality cutoff | 20 | Phred score minimum |
| Min length | 36 | Discard reads shorter than this after trimming |
| Adapter | auto-detect | TruSeq for most ENCODE libraries |
| Stringency | 1 | Overlap with adapter sequence required |
| Error rate | 0.1 | Maximum allowed error rate in adapter detection |

## Commands

```bash
# Raw QC
fastqc -t 4 -o qc_raw/ sample_R1.fastq.gz sample_R2.fastq.gz

# Paired-end trimming
trim_galore --paired --quality 20 --length 36 --fastqc \
  --cores 4 -o trimmed/ sample_R1.fastq.gz sample_R2.fastq.gz

# Single-end trimming
trim_galore --quality 20 --length 36 --fastqc \
  --cores 4 -o trimmed/ sample.fastq.gz
```

## Expected Output
- `*_trimming_report.txt` -- trimming statistics (reads processed, trimmed, removed)
- `*_val_1.fq.gz`, `*_val_2.fq.gz` -- trimmed paired-end reads
- `*_trimmed.fq.gz` -- trimmed single-end reads
- FastQC HTML reports for both raw and trimmed reads

## QC Checkpoints

| Check | Threshold | Action if Failed |
|-------|-----------|------------------|
| Per-base quality | >Q20 across all positions after trimming | Check sequencing run quality |
| Adapter content | <5% after trimming | Verify trimming parameters |
| GC content | Unimodal, matching expected genome GC | Check for contamination |
| Sequence duplication | <50% at this stage | May indicate low complexity library |
| Read count | Record for downstream normalization | No hard threshold at this stage |

## Troubleshooting

- **High adapter content after trimming**: Increase `--stringency` parameter or specify adapter
  sequence explicitly with `--adapter` flag
- **Bimodal GC distribution**: Indicates possible contamination; run FastQ Screen to identify
  organism of origin
- **Very short reads after trimming**: Library insert size may be too short; consider adjusting
  `--length` threshold or investigating library preparation
