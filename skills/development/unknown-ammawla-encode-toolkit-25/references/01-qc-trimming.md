# QC and Trimming for WGBS Data

Bisulfite-converted reads require specialized trimming to handle adapter
contamination and conversion-induced sequence biases.

## Pre-Trimming QC with FastQC

```bash
fastqc --threads 4 --outdir fastqc_raw/ sample_R1.fastq.gz sample_R2.fastq.gz
```

Key checks before trimming:
- Per-base sequence quality (expect Phred >28 across most positions)
- Adapter content (Illumina universal adapter is common)
- Per-base sequence content (bisulfite conversion causes C->T skew -- this is EXPECTED)
- Overrepresented sequences

**Important**: FastQC will flag per-base sequence content as FAIL for bisulfite data.
This is normal and expected because unmethylated C is converted to T.

## Adapter Trimming with Trim Galore

Trim Galore auto-detects Illumina adapters and applies bisulfite-aware trimming:

```bash
trim_galore \
    --paired \
    --quality 20 \
    --phred33 \
    --length 36 \
    --fastqc \
    --cores 4 \
    --clip_R2 10 \
    --three_prime_clip_R1 1 \
    --output_dir trim_galore/ \
    sample_R1.fastq.gz \
    sample_R2.fastq.gz
```

### Parameter Rationale

| Parameter | Value | Reason |
|-----------|-------|--------|
| `--quality 20` | Phred 20 | Standard quality cutoff |
| `--length 36` | 36 bp | Minimum length after trimming |
| `--clip_R2 10` | 10 bp | Remove end-repair artifacts from read 2 (5' end) |
| `--three_prime_clip_R1 1` | 1 bp | Remove filled-in C from end repair |
| `--cores 4` | 4 | Parallel processing (Trim Galore uses 3x cores internally) |

### RRBS-Specific Trimming

For RRBS data, use the `--rrbs` flag to handle MspI-digested fragments:

```bash
trim_galore \
    --paired \
    --rrbs \
    --quality 20 \
    --length 36 \
    --fastqc \
    --cores 4 \
    --output_dir trim_galore/ \
    sample_R1.fastq.gz \
    sample_R2.fastq.gz
```

The `--rrbs` flag removes 2 bp from the 3' end of reads that were filled in
during end-repair of MspI-digested fragments (CCGG sites).

## Post-Trimming QC

Trim Galore produces a trimming report with:
- Total reads processed
- Reads with adapter detected
- Reads too short after trimming
- Quality-trimmed bases

Verify in the report:
- Adapter detection rate should be >0% (if 0%, adapters may not be standard)
- Reads passing filter should be >90%
- Read length distribution should be reasonable (median >50 bp for 150 bp reads)
