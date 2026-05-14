# Stage 3: Filtering and Deduplication

## Tools
- **Picard MarkDuplicates v2.27+**: Mark and remove PCR duplicates
- **Samtools v1.15+**: Remove mitochondrial, unmapped, and low-quality reads
- **bedtools v2.30+**: Blacklist region filtering

## Blacklist

Download the ENCODE blacklist for artifact region removal:
- **Human (hg38)**: `https://github.com/Boyle-Lab/Blacklist/raw/master/lists/hg38-blacklist.v2.bed.gz`
- **Mouse (mm10)**: `https://github.com/Boyle-Lab/Blacklist/raw/master/lists/mm10-blacklist.v2.bed.gz`
- Reference: Amemiya et al. 2019 (Scientific Reports, ~1,372 citations)

The hg38 blacklist contains ~900 regions covering ~40 Mb of problematic sequence
including high-signal artifacts, satellite repeats, and assembly gaps.

## Samtools Flag Filtering

For paired-end data, use flag `-F 1804` to remove:
- Bit 4: read unmapped
- Bit 8: mate unmapped
- Bit 256: secondary alignment
- Bit 512: read fails quality checks
- Bit 1024: PCR duplicate (pre-Picard, optional)

## Commands

```bash
# Remove mitochondrial reads, unmapped, mate unmapped, low quality
samtools view -@ 4 -b -F 1804 -q 30 aligned.bam | \
  samtools sort -@ 4 -o filtered.bam -

# Mark and remove PCR duplicates
picard MarkDuplicates \
  INPUT=filtered.bam \
  OUTPUT=dedup.bam \
  METRICS_FILE=dup_metrics.txt \
  REMOVE_DUPLICATES=true \
  VALIDATION_STRINGENCY=LENIENT

# Remove blacklist regions
bedtools intersect -v -abam dedup.bam -b hg38-blacklist.v2.bed > final.bam
samtools index final.bam

# Record final read count
samtools flagstat final.bam > final_flagstat.txt
```

## Expected Output
- `dedup.bam` -- deduplicated BAM
- `dup_metrics.txt` -- Picard duplication metrics (NRF, PBC1, PBC2 derivable)
- `final.bam` + `final.bam.bai` -- blacklist-filtered, ready for peak calling
- `final_flagstat.txt` -- final read count after all filtering

## QC Checkpoints

| Check | Threshold | Action if Failed |
|-------|-----------|------------------|
| Duplication rate | <30% (NRF >= 0.8) | Low-input library; consider re-prep |
| Post-filter read count | >=20M TF / >=45M histone | May need deeper sequencing |
| Mitochondrial fraction | <5% | Normal for some cell types |
| Blacklist overlap | <1% of reads | Expected; higher suggests artifacts |

## Library Complexity Metrics

Derived from Picard MarkDuplicates output:
- **NRF** = Unique reads / Total reads (Non-Redundant Fraction)
- **PBC1** = Locations with exactly 1 read / Distinct locations
- **PBC2** = Locations with exactly 1 read / Locations with exactly 2 reads

These metrics quantify PCR amplification bottleneck severity.
