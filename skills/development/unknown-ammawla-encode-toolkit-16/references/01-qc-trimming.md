# Stage 1: QC and Trimming

## Input
- Raw paired-end FASTQ files (ENCODE standard is paired-end stranded RNA-seq)
- Adapter sequences: TruSeq adapters (Illumina TruSeq Stranded mRNA kit)

## Tools
- **FastQC v0.11.9+**: Per-base quality, adapter content, duplication rates, GC bias
- **Trim Galore v0.6.7+** (wraps Cutadapt): Adapter trimming + quality filtering

## Key Difference from ATAC-seq / ChIP-seq
RNA-seq uses **Illumina TruSeq** adapters, not Nextera. Trim Galore auto-detects
TruSeq adapters by default. RNA-seq reads tend to be longer (75-150 bp) and have
higher quality than ATAC-seq, but poly-A tails in adapter read-through are common
with short inserts.

## RNA-seq Specific QC Checks
- **Poly-A tail contamination**: Adapter content plot may show poly-A sequences if
  library inserts are shorter than read length. Trim Galore handles this automatically.
- **rRNA contamination**: High duplication rates combined with skewed GC content can
  indicate failed rRNA depletion. Check with `sortmerna` or RSeQC downstream.
- **GC bias**: RNA-seq GC content should reflect transcriptome composition, not genome.
  A bimodal GC plot may indicate contamination or degraded RNA.

## Parameters

| Parameter | Default | Notes |
|-----------|---------|-------|
| Quality cutoff | 20 | Phred score minimum |
| Min length | 36 | Longer minimum than ATAC-seq due to longer fragments |
| Adapter | TruSeq (auto-detect) | Illumina TruSeq adapters |
| Stringency | 1 | Overlap with adapter sequence required |
| Max N | 10 | Maximum Ns allowed in read |

## Commands

```bash
# Raw QC
fastqc -t 4 -o qc_raw/ sample_R1.fastq.gz sample_R2.fastq.gz

# Paired-end trimming with TruSeq adapters (auto-detected)
trim_galore --paired --quality 20 --length 36 --fastqc \
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
| Adapter content | <5% after trimming | Verify adapter detection |
| GC content | Unimodal, ~50% for human transcriptome | Check for contamination or rRNA |
| Duplication rate | <60% (variable in RNA-seq) | High duplication is common for abundant transcripts |
| Read count | >=30M PE reads recommended | May need more sequencing |

## Troubleshooting
- **High adapter content**: Short library inserts cause adapter read-through. Ensure
  `--length 36` retains enough reads after trimming.
- **Bimodal GC content**: Likely rRNA contamination or DNA contamination. Check with
  downstream rRNA rate from STAR log.
- **Very high duplication**: Some duplication is biological (highly expressed genes).
  True PCR duplicates are only a concern if NRF <0.5. Mark but do not remove duplicates
  for RNA-seq quantification.
