# Deduplication and Filtering for WGBS

PCR duplicates inflate coverage estimates and bias methylation calls.
Deduplication is essential for WGBS but must NOT be used for RRBS.

## Bismark Deduplication

Bismark provides its own deduplication tool optimized for bisulfite data:

```bash
deduplicate_bismark \
    --bam \
    --paired \
    --output_dir dedup/ \
    bismark_out/sample_pe.bam
```

Bismark deduplication identifies duplicates by their alignment positions on
both strands, accounting for bisulfite conversion. This is preferred over
Picard for bisulfite data.

### Expected Duplication Rates

| Library Quality | Duplication Rate | Action |
|----------------|------------------|--------|
| Good | <20% | Proceed |
| Acceptable | 20-40% | Proceed with caution |
| Poor | 40-60% | Consider resequencing |
| Very poor | >60% | Library failed -- redo |

## Alternative: Picard MarkDuplicates

If using bwa-meth (which does not have built-in dedup), use Picard:

```bash
picard MarkDuplicates \
    INPUT=sample_bwameth_sorted.bam \
    OUTPUT=sample_dedup.bam \
    METRICS_FILE=sample_dup_metrics.txt \
    REMOVE_DUPLICATES=true \
    VALIDATION_STRINGENCY=LENIENT \
    ASSUME_SORTED=true
```

## BAM Filtering

After deduplication, apply quality filters:

```bash
samtools view -b -h \
    -q 10 \
    -F 1804 \
    -f 2 \
    sample_dedup.bam \
    | samtools sort -@ 4 -o sample_filtered.bam

samtools index sample_filtered.bam
```

### Filter Flag Explanation

| Flag | Binary | Meaning |
|------|--------|---------|
| `-q 10` | MAPQ >= 10 | Minimum mapping quality |
| `-F 4` | 0x4 | Remove unmapped reads |
| `-F 256` | 0x100 | Remove secondary alignments |
| `-F 512` | 0x200 | Remove reads failing QC |
| `-F 1024` | 0x400 | Remove PCR duplicates |
| `-f 2` | 0x2 | Keep only properly paired |

Combined: `-F 1804` removes unmapped + secondary + QC-fail + duplicates.

## RRBS: Skip Deduplication

For RRBS libraries, MspI digestion creates identical fragment starts at cut
sites. These are NOT PCR duplicates and must be retained:

```bash
# Do NOT run deduplication for RRBS
# Instead, just filter for quality
samtools view -b -h -q 10 -F 780 -f 2 sample.bam \
    | samtools sort -@ 4 -o sample_filtered.bam
```

## Coverage Statistics

Generate coverage statistics for the filtered BAM:

```bash
samtools depth -a sample_filtered.bam \
    | awk '{sum+=$3; n++} END {print "Mean coverage:", sum/n}'

samtools flagstat sample_filtered.bam > sample_flagstat.txt

# CpG-specific coverage
bedtools intersect \
    -a sample_filtered.bam \
    -b /ref/CpG_sites.bed \
    -wa -wb \
    | awk '{print $NF}' | sort -n | uniq -c
```
