# BWA-MEM Alignment for DNase-seq

DNase-seq uses standard BWA-MEM alignment with paired-end reads.
Unlike Hi-C, DNase-seq reads come from contiguous fragments and can be
aligned as normal paired-end data.

## Genome Index Preparation

```bash
# Build BWA index (one-time, ~1 hour for human genome)
bwa index -a bwtsw genome.fa
```

Requires ~8 GB disk space for the human genome.

## Paired-End Alignment

```bash
bwa mem -t 8 -M \
    genome.fa \
    sample_R1_val_1.fq.gz \
    sample_R2_val_2.fq.gz \
    | samtools view -@ 4 -bS - \
    | samtools sort -@ 4 -o sample_sorted.bam

samtools index sample_sorted.bam
```

### BWA-MEM Parameters

| Parameter | Value | Reason |
|-----------|-------|--------|
| `-t 8` | 8 threads | Parallel alignment |
| `-M` | Mark shorter split as secondary | Picard compatibility |

Unlike ChIP-seq or ATAC-seq, DNase-seq does not need special alignment flags.
Standard BWA-MEM settings work well.

## Single-End Alignment

For older ENCODE DNase-seq datasets with single-end reads:

```bash
bwa mem -t 8 -M \
    genome.fa \
    sample_trimmed.fq.gz \
    | samtools view -@ 4 -bS - \
    | samtools sort -@ 4 -o sample_sorted.bam

samtools index sample_sorted.bam
```

## Alignment QC

```bash
samtools flagstat sample_sorted.bam > sample_flagstat.txt
```

Expected metrics:
- **Mapping rate**: >80% (typically 85-95%)
- **Properly paired**: >90% of mapped reads
- **Supplementary**: <5%
- **Secondary**: <5%

### MAPQ Distribution

```bash
samtools view sample_sorted.bam | \
    awk '{print $5}' | sort -n | uniq -c | sort -rn | head -20
```

Most reads should have MAPQ >= 30. A large fraction of MAPQ 0 reads suggests
the sample has high repeat content or contamination.

## Mitochondrial Reads

DNase-seq can contain significant mitochondrial DNA (chrM reads):

```bash
# Count mitochondrial reads
samtools idxstats sample_sorted.bam | awk '$1 == "chrM" {print "chrM reads:", $3}'
total=$(samtools view -c sample_sorted.bam)
chrm=$(samtools view -c sample_sorted.bam chrM)
echo "chrM fraction: $(echo "scale=4; $chrm / $total" | bc)"
```

Mitochondrial fraction:
- <5%: Normal
- 5-20%: Elevated but acceptable
- >20%: Poor nuclear enrichment

chrM reads are removed in the filtering step.

## Memory and Time Estimates

| Read Count | Threads | RAM | Time |
|-----------|---------|-----|------|
| 50M reads | 8 | 12 GB | 30-60 min |
| 100M reads | 8 | 12 GB | 1-2 hours |
| 200M reads | 8 | 12 GB | 2-4 hours |

BWA-MEM memory usage is dominated by index size (~8 GB for human genome),
not read count. RAM requirements are relatively stable.

## Alignment Considerations for Footprinting

If footprinting analysis is planned downstream, alignment quality is critical:
- Use paired-end data (SE data has lower footprint resolution)
- Do NOT remove soft-clipped bases (they indicate fragment boundaries)
- Higher depth is better: 100M+ reads for reliable footprints
- MAPQ 30 filter is applied downstream, not during alignment
