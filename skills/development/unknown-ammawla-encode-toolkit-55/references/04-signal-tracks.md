# Stage 4: Signal Track Generation

## Tools
- **STAR**: Generates strand-specific bedGraph output during alignment
- **bedGraphToBigWig**: Converts bedGraph to bigWig (UCSC Kent tools)

## Overview

RNA-seq signal tracks display read coverage across the genome for visualization in
genome browsers (UCSC, IGV, WashU Epigenome Browser). For stranded RNA-seq, separate
plus-strand and minus-strand tracks are generated, enabling gene-level visualization
of sense and antisense transcription.

## STAR bedGraph Output

STAR generates bedGraph files directly during alignment when run with:
```
--outWigType bedGraph --outWigStrand Stranded
```

This produces four files:

| File | Contents |
|------|----------|
| `Signal.Unique.str1.out.bg` | Plus strand, uniquely mapped reads |
| `Signal.Unique.str2.out.bg` | Minus strand, uniquely mapped reads |
| `Signal.UniqueMultiple.str1.out.bg` | Plus strand, unique + multi-mapped reads |
| `Signal.UniqueMultiple.str2.out.bg` | Minus strand, unique + multi-mapped reads |

For most analyses, use `Signal.UniqueMultiple` to include multi-mapped reads (consistent
with ENCODE standard). Use `Signal.Unique` for conservative signal estimation.

## bedGraph to bigWig Conversion

```bash
# Sort bedGraph (required by bedGraphToBigWig)
sort -k1,1 -k2,2n Signal.UniqueMultiple.str1.out.bg > plus_sorted.bg
sort -k1,1 -k2,2n Signal.UniqueMultiple.str2.out.bg > minus_sorted.bg

# Convert to bigWig
bedGraphToBigWig plus_sorted.bg chrom.sizes sample_plus.bw
bedGraphToBigWig minus_sorted.bg chrom.sizes sample_minus.bw
```

## Chromosome Sizes File

```bash
# Generate chrom.sizes from STAR genome index
samtools view -H Aligned.sortedByCoord.out.bam | \
  grep '@SQ' | awk '{print $2"\t"$3}' | \
  sed 's/SN://;s/LN://' > chrom.sizes

# Or fetch from UCSC
wget https://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/hg38.chrom.sizes
```

## Signal Normalization

STAR bedGraph output is raw read counts per position. For cross-sample comparison,
normalize signal tracks:

| Method | Description | When to Use |
|--------|-------------|-------------|
| Raw | Unnormalized read counts | Single-sample visualization |
| RPM | Reads per million mapped | Cross-sample comparison (simple) |
| RPKM | RPM per kilobase | Length-normalized (rarely needed for signal) |

ENCODE provides both raw and RPM-normalized bigWig files. For publication, RPM is
standard for cross-sample comparison in browser screenshots.

## Alternative: bamCoverage (deepTools)

For more control over normalization, use deepTools `bamCoverage`:

```bash
bamCoverage -b Aligned.sortedByCoord.out.bam \
  -o sample.bw \
  --normalizeUsing RPKM \
  --binSize 10 \
  --filterRNAstrand forward \
  --numberOfProcessors 8
```

## Expected Output
- `sample_plus.bw` -- plus-strand bigWig signal track
- `sample_minus.bw` -- minus-strand bigWig signal track

## Notes
- bedGraphToBigWig requires sorted input and a chromosome sizes file.
- For stranded data, always generate separate plus/minus tracks. Combining them
  loses strand information and confounds sense/antisense transcription.
- bigWig files are typically 50-200 MB each, much smaller than BAM files.
