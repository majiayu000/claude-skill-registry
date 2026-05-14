# QC and Trimming for CUT&RUN Data

CUT&RUN produces paired-end reads with a characteristic nucleosomal fragment
size distribution. Reads are typically shorter than ChIP-seq due to the
MNase cleavage mechanism.

## Pre-Trimming QC with FastQC

```bash
fastqc --threads 4 --outdir fastqc_raw/ sample_R1.fastq.gz sample_R2.fastq.gz
```

Key checks:
- Per-base quality (expect Phred >28)
- Adapter content (Nextera or Illumina universal adapter)
- Insert size (CUT&RUN fragments are often <150 bp, causing adapter read-through)
- Sequence duplication (moderate levels expected with low input)

**Note**: CUT&RUN libraries from low cell input often show higher duplication
than ChIP-seq. This is expected and not necessarily a quality issue.

## Adapter Trimming with Trim Galore

CUT&RUN fragments are often shorter than read length, causing adapter
read-through. Aggressive adapter trimming is important.

```bash
trim_galore \
    --paired \
    --quality 20 \
    --phred33 \
    --length 20 \
    --cores 4 \
    --fastqc \
    --nextera \
    --output_dir trim_galore/ \
    sample_R1.fastq.gz \
    sample_R2.fastq.gz
```

### Parameter Rationale

| Parameter | Value | Reason |
|-----------|-------|--------|
| `--quality 20` | Phred 20 | Standard quality cutoff |
| `--length 20` | 20 bp | Keep short sub-nucleosomal fragments |
| `--nextera` | Flag | CUT&RUN often uses Nextera adapters (check protocol) |
| `--cores 4` | 4 | Parallel processing |

### Adapter Type Selection

Check which adapter was used in library preparation:
- **Nextera**: Most CUT&Tag protocols (use `--nextera` flag)
- **Illumina TruSeq**: Some CUT&RUN protocols (default Trim Galore detection)
- If unsure, let Trim Galore auto-detect (omit `--nextera`)

## Post-Trimming Verification

After trimming, verify:
- >90% of reads pass quality filter
- Adapter contamination removed (often 20-50% for CUT&RUN)
- Read length distribution: 20-150 bp (many short reads are expected)

High adapter contamination rate (>30%) is NORMAL for CUT&RUN because
many fragments are shorter than the read length.

## Fragment Size Check (Post-Alignment)

After alignment, verify the fragment size distribution:

```bash
samtools view -f 2 -F 1804 sample.bam | \
    awk '{if($9 > 0) print $9}' | \
    sort -n | uniq -c | \
    awk '{print $2, $1}' > fragment_sizes.txt
```

Expected CUT&RUN fragment distribution:
- **TF targets**: Peak at <120 bp (sub-nucleosomal)
- **Histone marks**: Strong peak at ~150 bp (mononucleosomal)
- **Both**: Should show nucleosomal ladder pattern
- Broad smear with no peaks suggests protocol failure

## CUT&Tag vs CUT&RUN Trimming

CUT&Tag uses Tn5 transposase which adds 19 bp Mosaic End (ME) sequences.
For CUT&Tag data specifically:

```bash
trim_galore \
    --paired \
    --quality 20 \
    --length 20 \
    --cores 4 \
    --nextera \
    --fastqc \
    sample_R1.fastq.gz \
    sample_R2.fastq.gz
```

The `--nextera` flag is especially important for CUT&Tag since Tn5 inserts
Nextera-compatible adapters.
