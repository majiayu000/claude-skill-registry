# Stage 2: STAR Alignment

## Tools
- **STAR v2.7.10b+**: Splice-aware aligner (Dobin et al. 2013, ~12,000 citations)
- **Samtools v1.17+**: BAM conversion, sorting, indexing, and statistics

## Why STAR Instead of HISAT2 or Bowtie2
STAR is preferred for ENCODE RNA-seq because:
1. Native splice junction awareness with 2-pass mode for novel junction discovery
2. Simultaneous output of genome BAM + transcriptome BAM (for RSEM)
3. Built-in gene count quantification (`--quantMode GeneCounts`)
4. Native bedGraph signal generation (`--outWigType bedGraph`)
5. Chimeric read detection for gene fusion analysis
6. Standard in the ENCODE RNA-seq uniform pipeline

## Reference Genome and Annotation

| Organism | Assembly | STAR Index Source | GTF Annotation |
|----------|----------|-------------------|----------------|
| Human | GRCh38 (hg38) | Build from ENCODE FASTA | GENCODE v38+ (comprehensive) |
| Mouse | mm10 (GRCm38) | Build from ENCODE FASTA | GENCODE vM27+ (comprehensive) |

Use the ENCODE "no alt" analysis set FASTA with GENCODE comprehensive gene annotation.

## STAR Index Generation

```bash
# Generate genome index (run once, requires ~32GB RAM for human)
STAR --runMode genomeGenerate \
  --genomeDir star_index/ \
  --genomeFastaFiles GRCh38.primary_assembly.genome.fa \
  --sjdbGTFfile gencode.v38.primary_assembly.annotation.gtf \
  --sjdbOverhang 100 \
  --runThreadN 8
```

The `--sjdbOverhang` should ideally be `read_length - 1`. The default of 100 works well
for 101 bp reads and is robust across typical read lengths (75-150 bp).

## STAR 2-Pass Alignment

```bash
STAR --genomeDir star_index/ \
  --readFilesIn R1.fq.gz R2.fq.gz \
  --readFilesCommand zcat \
  --runThreadN 8 \
  --outSAMtype BAM SortedByCoordinate \
  --outSAMunmapped Within \
  --outFilterMultimapNmax 20 \
  --alignSJoverhangMin 8 \
  --alignSJDBoverhangMin 1 \
  --outFilterMismatchNmax 999 \
  --outFilterMismatchNoverReadLmax 0.04 \
  --alignIntronMin 20 \
  --alignIntronMax 1000000 \
  --alignMatesGapMax 1000000 \
  --quantMode TranscriptomeSAM GeneCounts \
  --twopassMode Basic \
  --outWigType bedGraph \
  --outWigStrand Stranded
```

## Parameters

| Parameter | Value | Notes |
|-----------|-------|-------|
| 2-pass mode | `--twopassMode Basic` | Discovers novel junctions, re-maps in 2nd pass |
| Multi-map max | `--outFilterMultimapNmax 20` | Allow up to 20 alignments (RSEM handles them) |
| SJ overhang | `--alignSJoverhangMin 8` | Minimum overhang for unannotated junctions |
| SJ DB overhang | `--alignSJDBoverhangMin 1` | Minimum overhang for annotated junctions |
| Mismatch rate | `--outFilterMismatchNoverReadLmax 0.04` | Max 4% mismatch rate |
| Intron min | `--alignIntronMin 20` | Minimum intron length |
| Intron max | `--alignIntronMax 1000000` | Maximum intron length (1 Mb) |
| Quant mode | `TranscriptomeSAM GeneCounts` | Output transcriptome BAM + gene counts |
| Signal output | `--outWigType bedGraph --outWigStrand Stranded` | Strand-specific bedGraph |

## Expected Output
- `Aligned.sortedByCoord.out.bam` -- genome-sorted BAM
- `Aligned.toTranscriptome.out.bam` -- transcriptome BAM (input for RSEM)
- `ReadsPerGene.out.tab` -- STAR gene counts (column 1: unstranded, 2: sense, 3: antisense)
- `SJ.out.tab` -- splice junction table (novel + annotated)
- `Signal.UniqueMultiple.str1.out.bg` -- plus-strand bedGraph
- `Signal.UniqueMultiple.str2.out.bg` -- minus-strand bedGraph
- `Log.final.out` -- alignment summary statistics

## QC Checkpoints

| Check | Threshold | Action if Failed |
|-------|-----------|------------------|
| Uniquely mapped reads | >=70% | Check genome build, contamination, rRNA |
| Multi-mapped reads | <10% | High multi-map suggests repetitive contamination |
| Unmapped: too short | <10% | High rate suggests aggressive trimming or poor quality |
| Unmapped: too many mismatches | <5% | Check for contamination (wrong organism) |
| Chimeric reads | <1% (unless fusion analysis) | High rate may indicate structural variants |
| Splice junctions (novel) | Thousands expected | Very few suggests annotation mismatch |

## Notes
- STAR 2-pass mode is slower than 1-pass but discovers 10-20% more novel splice junctions.
- The transcriptome BAM (`Aligned.toTranscriptome.out.bam`) must NOT be coordinate-sorted;
  RSEM requires it in its native transcript-coordinate order.
- `--outFilterMultimapNmax 20` is essential for RSEM. Do not reduce this before RSEM.
- For chimeric/fusion detection, add `--chimSegmentMin 12 --chimJunctionOverhangMin 8
  --chimOutType Junctions WithinBAM SoftClip`.
