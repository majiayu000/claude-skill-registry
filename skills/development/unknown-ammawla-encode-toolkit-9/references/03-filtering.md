# Filtering and Deduplication for DNase-seq

After alignment, remove low-quality reads, duplicates, mitochondrial reads,
and blacklisted regions to produce a clean BAM for Hotspot2 analysis.

## Quality Filtering

```bash
samtools view -b -h \
    -q 30 \
    -F 1804 \
    -f 2 \
    sample_sorted.bam \
    | samtools sort -@ 4 -o sample_filtered.bam
```

### Filter Flags

| Flag | Meaning |
|------|---------|
| `-q 30` | MAPQ >= 30 (uniquely mapped) |
| `-F 4` | Remove unmapped |
| `-F 256` | Remove secondary alignments |
| `-F 512` | Remove QC-failed reads |
| `-F 1024` | Remove duplicates (after marking) |
| `-f 2` | Keep only properly paired |

Combined `-F 1804` removes unmapped + secondary + QC-fail + duplicates.

## Remove Mitochondrial Reads

```bash
# Get list of non-chrM chromosomes
samtools idxstats sample_filtered.bam | \
    awk '$1 != "chrM" && $1 != "*" {print $1}' > chroms.txt

# Filter to nuclear chromosomes only
samtools view -b -h \
    sample_filtered.bam \
    $(cat chroms.txt | tr '\n' ' ') \
    > sample_nuclear.bam

samtools index sample_nuclear.bam
```

## Duplicate Marking with Picard

```bash
picard MarkDuplicates \
    INPUT=sample_nuclear.bam \
    OUTPUT=sample_dedup.bam \
    METRICS_FILE=sample_dup_metrics.txt \
    REMOVE_DUPLICATES=true \
    VALIDATION_STRINGENCY=LENIENT \
    ASSUME_SORTED=true

samtools index sample_dedup.bam
```

### Library Complexity Metrics

From the Picard output, extract:

```bash
grep -A 1 'LIBRARY' sample_dup_metrics.txt | tail -1 | \
    awk '{
        print "Total pairs:", $3;
        print "Unique pairs:", $3 - $7;
        print "Duplication rate:", $9;
        print "Estimated library size:", $10
    }'
```

## Blacklist Removal

Remove reads overlapping ENCODE blacklist regions:

```bash
# Download blacklist
wget -q https://github.com/Boyle-Lab/Blacklist/raw/master/lists/hg38-blacklist.v2.bed.gz
gunzip hg38-blacklist.v2.bed.gz

# Remove blacklisted reads
bedtools intersect \
    -a sample_dedup.bam \
    -b hg38-blacklist.v2.bed \
    -v \
    > sample_final.bam

samtools index sample_final.bam
```

## NRF and PBC Metrics

ENCODE reports library complexity metrics:

```bash
# NRF = Non-Redundant Fraction = unique / total
# PBC1 = PCR Bottleneck Coefficient 1 = 1-position / 1-position-or-more

samtools view -F 1804 -f 2 sample_sorted.bam | \
    awk 'BEGIN{OFS="\t"} {print $3, $4, $3, $4}' | \
    sort | uniq -c | \
    awk 'BEGIN{mt=0; m0=0; m1=0; m2=0}
    {mt+=$1; m0++; if($1==1) m1++; if($1==2) m2++}
    END {
        print "NRF:", m0/mt;
        print "PBC1:", m1/m0;
        print "PBC2:", m1/m2
    }'
```

| Metric | Pass | Warning | Fail |
|--------|------|---------|------|
| NRF | >0.8 | 0.7-0.8 | <0.7 |
| PBC1 | >0.9 | 0.7-0.9 | <0.7 |
| PBC2 | >3.0 | 1.0-3.0 | <1.0 |

## Final BAM Statistics

```bash
samtools flagstat sample_final.bam > sample_final_flagstat.txt
echo "Final read count: $(samtools view -c sample_final.bam)"
```
