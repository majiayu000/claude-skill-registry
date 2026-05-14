# QC and Trimming for Hi-C Data

Hi-C reads contain chimeric sequences from ligation junctions. Standard
adapter trimming is applied, but ligation junction trimming is handled
downstream by pairtools.

## Pre-Alignment QC with FastQC

```bash
fastqc --threads 4 --outdir fastqc_raw/ sample_R1.fastq.gz sample_R2.fastq.gz
```

Key checks:
- Per-base quality (expect Phred >28 across most positions)
- Adapter content (Illumina adapters)
- Sequence length distribution (Hi-C reads are typically 50-150 bp)
- Duplication level (Hi-C libraries often show high duplication at low depths)

**Note**: Hi-C data will show unusual insert size distributions because reads
originate from ligation junctions, not contiguous fragments. This is expected.

## Adapter Trimming with Trim Galore

Hi-C data benefits from light adapter trimming. Do NOT aggressively trim
quality since chimeric reads may have lower quality at the junction.

```bash
trim_galore \
    --paired \
    --quality 15 \
    --phred33 \
    --length 30 \
    --cores 4 \
    --fastqc \
    sample_R1.fastq.gz \
    sample_R2.fastq.gz
```

### Parameter Rationale

| Parameter | Value | Reason |
|-----------|-------|--------|
| `--quality 15` | Phred 15 | Lenient -- chimeric reads have junction artifacts |
| `--length 30` | 30 bp | Short reads still carry valid contact information |
| `--cores 4` | 4 | Trim Galore uses ~3x threads internally |

### Alternative: No Trimming

Some Hi-C pipelines (including Juicer) skip trimming entirely and rely on
the aligner to handle adapter contamination via soft-clipping. This is
acceptable for BWA-MEM:

```bash
# Skip trim_galore, proceed directly to alignment
# BWA-MEM will soft-clip adapter sequences
```

ENCODE recommendation: Light trimming with Trim Galore for consistency.

## Restriction Enzyme Verification

Before processing, verify which restriction enzyme was used:

| Enzyme | Recognition Site | Ligation Junction | Average Fragment |
|--------|-----------------|-------------------|------------------|
| MboI/DpnII | GATC | GATCGATC | ~256 bp |
| HindIII | AAGCTT | AAGCTAGCTT | ~4 kb |
| Arima | Two sites | Multiple | ~160 bp |
| NcoI | CCATGG | CCATGCATGG | ~2 kb |

```bash
# Check for ligation junction sequence in reads (MboI example)
zcat sample_R1.fastq.gz | head -10000 | grep -c 'GATCGATC'
```

If the junction sequence appears frequently (>1% of reads), the enzyme
assignment is confirmed.

## Post-Trimming Summary

After trimming, verify:
- >95% reads pass filters
- Median read length >40 bp
- Adapter detection rate is reasonable (typically 5-20% for Hi-C)
