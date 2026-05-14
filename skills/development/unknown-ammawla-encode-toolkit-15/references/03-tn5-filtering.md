# Stage 3: Tn5 Shift, Filtering, and Fragment Selection

## Tools
- **Samtools v1.15+**: Mitochondrial read removal, flag filtering
- **Picard MarkDuplicates v2.27+**: PCR duplicate removal
- **bedtools v2.30+**: Blacklist filtering, Tn5 shift, fragment size selection
- **deeptools alignmentSieve**: Fragment size selection (alternative to bedtools)

## Tn5 Transposase Offset Correction

The Tn5 transposase creates a 9-bp target site duplication during insertion. To
accurately represent the cut site, reads must be shifted:
- **Forward strand (+)**: shift +4 bp
- **Reverse strand (-)**: shift -5 bp

This correction is critical for motif footprinting and accurate cut-site analysis.

## Commands

```bash
# Step 1: Remove mitochondrial reads
samtools view -@ 4 -b aligned.bam $(samtools idxstats aligned.bam | \
  awk '$1 != "chrM" && $1 != "*" {print $1}' | tr '\n' ' ') > no_mito.bam

# Step 2: Remove unmapped, mate unmapped, secondary, QC-fail, duplicates
samtools view -@ 4 -b -F 1804 -q 30 no_mito.bam | \
  samtools sort -@ 4 -o filtered.bam -

# Step 3: Mark and remove PCR duplicates
picard MarkDuplicates \
  INPUT=filtered.bam OUTPUT=dedup.bam \
  METRICS_FILE=dup_metrics.txt \
  REMOVE_DUPLICATES=true VALIDATION_STRINGENCY=LENIENT
samtools index dedup.bam

# Step 4: Apply Tn5 shift (+4/-5)
alignmentSieve --bam dedup.bam --outFile shifted.bam \
  --ATACshift --numberOfProcessors 4
samtools sort -@ 4 -o shifted.sorted.bam shifted.bam
samtools index shifted.sorted.bam

# Step 5: Remove blacklist regions
bedtools intersect -v -abam shifted.sorted.bam -b hg38-blacklist.v2.bed > final.bam
samtools index final.bam

# Step 6: Separate nucleosome-free and mono-nucleosomal fragments
alignmentSieve --bam final.bam --outFile nfr.bam \
  --maxFragmentLength 150 --numberOfProcessors 4
alignmentSieve --bam final.bam --outFile mononuc.bam \
  --minFragmentLength 150 --maxFragmentLength 300 --numberOfProcessors 4
samtools sort -@ 4 -o nfr.sorted.bam nfr.bam && samtools index nfr.sorted.bam
samtools sort -@ 4 -o mononuc.sorted.bam mononuc.bam && samtools index mononuc.sorted.bam
```

## Fragment Size Classes

| Class | Size (bp) | Use |
|-------|-----------|-----|
| NFR (nucleosome-free) | <150 | Peak calling, TF footprinting |
| Mono-nucleosome | 150-300 | Nucleosome positioning |
| Di-nucleosome | 300-500 | Chromatin architecture |

## QC Checkpoints

| Check | Threshold | Action if Failed |
|-------|-----------|------------------|
| Mitochondrial fraction | <20% (ideal <5%) | Optimize cell lysis |
| Duplication rate | <30% (NRF >= 0.8) | Low complexity library |
| NFR fraction | >40% of fragments <150bp | Check transposition efficiency |
| Post-filter reads | >=25M | May need deeper sequencing |

## Notes
- The `alignmentSieve --ATACshift` from deeptools applies the +4/-5 offset automatically.
- Alternative: use a custom awk script on BED format for Tn5 shifting.
- Blacklist: Amemiya et al. 2019 (hg38-blacklist.v2.bed, ~900 regions, ~40 Mb).
