# Hotspot2 DHS Calling and Signal Generation

Hotspot2 is the ENCODE-standard peak caller for DNase-seq data. It identifies
DNase I Hypersensitive Sites (DHSs) using a local tag density model that
accounts for mappability variation across the genome.

## Hotspot2 Execution

```bash
hotspot2.sh \
    -c /ref/hg38.chrom.sizes \
    -C /ref/center_sites.starch \
    -M /ref/mappable_regions.bed \
    -f ${FDR} \
    -F 0.05 \
    -p "DNase-seq" \
    -s sample_final.bam \
    -o hotspot2_output/
```

### Key Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| `-c` | chrom.sizes | Chromosome sizes |
| `-C` | center_sites.starch | Tag density center sites |
| `-M` | mappable_regions.bed | Mappability regions (read-length specific) |
| `-f` | 0.05 | FDR threshold for hotspot calling |
| `-F` | 0.05 | FDR threshold for peak calling within hotspots |
| `-p` | "DNase-seq" | Protocol type |

### Mappability Index

Hotspot2 requires a mappability index that is specific to:
- Genome build (hg38, mm10)
- Read length (36, 50, 76, 100, 150 bp)

ENCODE provides pre-built indices for common configurations:
```
/ref/hotspot2_index/
    hg38.K36.mappable_only.bed
    hg38.K76.mappable_only.bed
    hg38.K150.mappable_only.bed
```

If no matching index exists, generate one:
```bash
hotspot2-mappability \
    --genome genome.fa \
    --kmer-length 150 \
    --output /ref/hotspot2_index/hg38.K150.mappable_only.bed
```

## Output Files

Hotspot2 produces several output files:

| File | Description |
|------|-------------|
| `*.hotspots.fdr0.05.starch` | Hotspot regions passing FDR cutoff |
| `*.peaks.narrowPeak` | Individual peaks within hotspots |
| `*.allcalls.starch` | All hotspot calls (unfiltered) |
| `*.SPOT.txt` | SPOT score |
| `*.density.starch` | Per-base tag density |

## Convert to BED and narrowPeak

```bash
# Convert starch to BED
unstarch hotspot2_output/sample.hotspots.fdr0.05.starch > sample.hotspots.bed

# Hotspot2 already produces narrowPeak format
# Ensure blacklist filtering
bedtools intersect \
    -a hotspot2_output/sample.peaks.narrowPeak \
    -b /ref/hg38-blacklist.v2.bed \
    -v \
    > sample.DHS.narrowPeak
```

## SPOT Score Calculation

The SPOT score is computed by Hotspot2:

```bash
cat hotspot2_output/sample.SPOT.txt
```

If computing manually:
```bash
total_tags=$(samtools view -c sample_final.bam)
tags_in_hotspots=$(bedtools intersect \
    -a sample_final.bam \
    -b sample.hotspots.bed \
    -u -bed | wc -l)
echo "SPOT score: $(echo "scale=4; $tags_in_hotspots / $total_tags" | bc)"
```

## Signal Track Generation

Generate a normalized signal track for genome browser visualization:

```bash
# Create bedGraph of tag density
bedtools genomecov \
    -ibam sample_final.bam \
    -bg \
    -pc \
    -g /ref/hg38.chrom.sizes \
    > sample.bedGraph

# Normalize to reads-per-million
total=$(samtools view -c -F 1804 -f 2 sample_final.bam)
scale=$(echo "scale=10; 1000000 / $total" | bc)

awk -v s=$scale 'BEGIN{OFS="\t"} {$4=$4*s; print}' sample.bedGraph \
    | sort -k1,1 -k2,2n > sample_rpm.bedGraph

# Convert to bigWig
bedGraphToBigWig sample_rpm.bedGraph /ref/hg38.chrom.sizes sample.density.bw
```

## Peak Annotation

Annotate DHSs with genomic features:

```bash
# Count peaks by category
total=$(wc -l < sample.DHS.narrowPeak)
echo "Total DHSs: $total"

# Overlap with gene promoters (TSS +/- 2kb)
promoter=$(bedtools intersect -a sample.DHS.narrowPeak -b promoters.bed -u | wc -l)
echo "Promoter DHSs: $promoter ($(echo "scale=1; $promoter*100/$total" | bc)%)"

# Overlap with known enhancers
enhancer=$(bedtools intersect -a sample.DHS.narrowPeak -b enhancers.bed -u | wc -l)
echo "Enhancer DHSs: $enhancer ($(echo "scale=1; $enhancer*100/$total" | bc)%)"
```
