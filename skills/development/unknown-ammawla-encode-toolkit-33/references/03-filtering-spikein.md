# Filtering, Deduplication, and Spike-in Normalization

CUT&RUN data processing requires standard quality filtering, duplicate removal,
blacklist filtering, AND spike-in normalization for quantitative analysis.

## Quality Filtering

```bash
samtools view -b -h \
    -q 10 \
    -F 1804 \
    -f 2 \
    sample_sorted.bam \
    | samtools sort -@ 4 -o sample_filtered.bam
```

### Filter Parameters

| Flag | Meaning |
|------|---------|
| `-q 10` | MAPQ >= 10 (CUT&RUN uses lower threshold than ChIP-seq) |
| `-F 4` | Remove unmapped |
| `-F 256` | Remove secondary |
| `-F 512` | Remove QC-fail |
| `-F 1024` | Remove duplicates (after marking) |
| `-f 2` | Keep properly paired only |

**Note**: MAPQ 10 instead of 30 for CUT&RUN. The lower threshold retains
more signal because CUT&RUN targets can be in repetitive regions.

## Duplicate Marking

```bash
picard MarkDuplicates \
    INPUT=sample_filtered.bam \
    OUTPUT=sample_dedup.bam \
    METRICS_FILE=sample_dup_metrics.txt \
    REMOVE_DUPLICATES=true \
    VALIDATION_STRINGENCY=LENIENT \
    ASSUME_SORTED=true

samtools index sample_dedup.bam
```

CUT&RUN from low cell numbers may have higher duplication. Accept up to 40%.

## Blacklist + Suspect List Filtering

CUT&RUN requires filtering against BOTH the ENCODE blacklist and the
CUT&RUN-specific suspect list (Nordin 2023):

```bash
# Concatenate blacklist and suspect list
cat hg38-blacklist.v2.bed CUTandRUN.suspectlist.hg38.bed \
    | sort -k1,1 -k2,2n | bedtools merge > combined_blacklist.bed

# Filter BAM
bedtools intersect \
    -a sample_dedup.bam \
    -b combined_blacklist.bed \
    -v \
    > sample_final.bam

samtools index sample_final.bam
```

The suspect list identifies ~400 regions enriched in CUT&RUN controls
that produce false positive peaks, independent of the ENCODE blacklist.

## Spike-in Normalization

### Calculate Scale Factors

```bash
# Count spike-in reads per sample (from spike-in alignment)
echo "sample1 $(samtools view -c -F 1804 -f 2 sample1_spikein.bam)" > spikein_counts.txt
echo "sample2 $(samtools view -c -F 1804 -f 2 sample2_spikein.bam)" >> spikein_counts.txt
echo "sample3 $(samtools view -c -F 1804 -f 2 sample3_spikein.bam)" >> spikein_counts.txt

# Calculate scale factors (relative to minimum)
min_count=$(awk '{print $2}' spikein_counts.txt | sort -n | head -1)

awk -v min=$min_count '{
    scale = min / $2;
    print $1, $2, scale
}' spikein_counts.txt > scale_factors.txt
```

### Apply Spike-in Scaling to Signal

```bash
# Read scale factor
scale=$(awk -v s="sample1" '$1==s {print $3}' scale_factors.txt)

# Generate spike-in normalized bedGraph
bedtools genomecov \
    -ibam sample_final.bam \
    -bg \
    -pc \
    -scale ${scale} \
    -g hg38.chrom.sizes \
    | sort -k1,1 -k2,2n > sample_normalized.bedGraph

# Convert to bigWig
bedGraphToBigWig sample_normalized.bedGraph hg38.chrom.sizes sample_normalized.bw
```

### Alternative: deepTools Normalization

```bash
bamCoverage \
    --bam sample_final.bam \
    --outFileName sample_normalized.bw \
    --scaleFactor ${scale} \
    --binSize 10 \
    --normalizeUsing None \
    --extendReads \
    --numberOfProcessors 4
```

## Generate Fragment BED File

SEACR requires a fragment BED file as input:

```bash
# Convert BAM to fragment BED (PE fragments)
bedtools bamtobed -bedpe -i sample_final.bam \
    | awk 'BEGIN{OFS="\t"} {print $1, $2, $6, $7, $8, $9}' \
    | sort -k1,1 -k2,2n \
    > sample_fragments.bed

# Generate normalized fragment bedGraph
bedtools genomecov \
    -i sample_fragments.bed \
    -g hg38.chrom.sizes \
    -bg \
    -scale ${scale} \
    | sort -k1,1 -k2,2n > sample_fragments.bedGraph
```

## QC Statistics

```bash
# Final read count
echo "Final reads: $(samtools view -c sample_final.bam)"

# Flagstat
samtools flagstat sample_final.bam > sample_flagstat.txt

# Spike-in fraction
genome=$(samtools view -c -F 1804 -f 2 sample_final.bam)
spikein=$(samtools view -c -F 1804 -f 2 sample_spikein.bam)
echo "Spike-in fraction: $(echo "scale=4; $spikein / ($genome + $spikein)" | bc)"
```
