# Stage 1: QC and Trimming

## Input
- Raw paired-end FASTQ files (ATAC-seq is almost always paired-end)
- Adapter sequences: Nextera transposase adapters (not TruSeq)

## Tools
- **FastQC v0.11.9+**: Per-base quality, adapter content, duplication rates, insert size
- **Trim Galore v0.6.7+** (wraps Cutadapt): Adapter trimming + quality filtering

## Key Difference from ChIP-seq
ATAC-seq uses **Nextera** transposase adapters, not Illumina TruSeq. Trim Galore
auto-detects Nextera adapters, but you can force it with `--nextera`.

## Parameters

| Parameter | Default | Notes |
|-----------|---------|-------|
| Quality cutoff | 20 | Phred score minimum |
| Min length | 20 | Shorter than ChIP-seq due to NFR fragments |
| Adapter | Nextera (auto-detect) | Tn5 transposase adapters |
| Stringency | 1 | Overlap with adapter sequence required |
| Max N | 10 | Maximum Ns allowed in read |

## Commands

```bash
# Raw QC
fastqc -t 4 -o qc_raw/ sample_R1.fastq.gz sample_R2.fastq.gz

# Paired-end trimming with Nextera adapters
trim_galore --paired --nextera --quality 20 --length 20 --fastqc \
  --cores 4 -o trimmed/ sample_R1.fastq.gz sample_R2.fastq.gz
```

## Expected Output
- `*_trimming_report.txt` -- trimming statistics
- `*_val_1.fq.gz`, `*_val_2.fq.gz` -- trimmed paired-end reads
- FastQC HTML reports for raw and trimmed reads

## QC Checkpoints

| Check | Threshold | Action if Failed |
|-------|-----------|------------------|
| Per-base quality | >Q20 after trimming | Check sequencing run quality |
| Adapter content | <5% after trimming | Verify Nextera adapter detection |
| GC content | Unimodal, matching genome | Check for contamination |
| Insert size | Nucleosomal ladder visible | Inspect library prep |
| Read count | >=50M total recommended | May need more sequencing |

## Troubleshooting
- **High adapter content**: ATAC-seq libraries with short inserts have more adapter
  read-through. This is normal for NFR fragments. Ensure `--length 20` allows retention.
- **No nucleosomal pattern in insert sizes**: May indicate failed transposition or
  over-transposition. Check Tn5:cell ratio.
