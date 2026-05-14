# Stage 3: Gene and Transcript Quantification

## Tools
- **RSEM v1.3.3+**: Gene/transcript quantification (Li & Dewey 2011, ~6,000 citations)
- **Kallisto v0.48.0+**: Fast pseudoalignment quantification (Bray et al. 2016, ~4,000 citations)

## RSEM Quantification (Primary)

RSEM uses an expectation-maximization (EM) algorithm to probabilistically assign
multi-mapped reads to genes and transcripts, providing accurate quantification even
for overlapping gene families and repetitive elements.

### RSEM Index Preparation

```bash
# Prepare RSEM reference (run once)
rsem-prepare-reference --gtf gencode.v38.primary_assembly.annotation.gtf \
  --star GRCh38.primary_assembly.genome.fa rsem_index/GRCh38
```

### RSEM Quantification

```bash
rsem-calculate-expression \
  --paired-end \
  --bam \
  --no-bam-output \
  --estimate-rspd \
  --strandedness reverse \
  --num-threads 8 \
  Aligned.toTranscriptome.out.bam \
  rsem_index/GRCh38 \
  sample_name
```

### RSEM Output Files

| File | Contents | Key Columns |
|------|----------|-------------|
| `sample.genes.results` | Gene-level quantification | gene_id, transcript_id(s), length, effective_length, expected_count, TPM, FPKM |
| `sample.isoforms.results` | Transcript-level quantification | transcript_id, gene_id, length, effective_length, expected_count, TPM, FPKM, IsoPct |

### RSEM Strandedness Flags

| Library Type | RSEM Flag | Description |
|-------------|-----------|-------------|
| dUTP / rf-stranded | `--strandedness reverse` | ENCODE standard |
| fr-stranded | `--strandedness forward` | Directional ligation |
| Unstranded | `--strandedness none` | SMARTer, SMART-Seq2, older protocols |

## Kallisto Quantification (Optional Fast Alternative)

Kallisto uses pseudoalignment (k-mer matching without full alignment) for ultra-fast
transcript quantification. It runs 10-100x faster than STAR+RSEM but does not produce
BAM files or support fusion detection.

### Kallisto Index

```bash
# Build Kallisto index from transcriptome FASTA (run once)
kallisto index -i kallisto_index.idx gencode.v38.transcripts.fa
```

### Kallisto Quantification

```bash
kallisto quant \
  -i kallisto_index.idx \
  -o kallisto_out/ \
  --rf-stranded \
  -t 8 \
  R1.fq.gz R2.fq.gz
```

### Kallisto Output

| File | Contents |
|------|----------|
| `abundance.tsv` | transcript_id, length, effective_length, est_counts, tpm |
| `abundance.h5` | Binary HDF5 format (for sleuth) |
| `run_info.json` | Run metadata and statistics |

## TPM vs FPKM vs Raw Counts

| Metric | Definition | Cross-Sample Comparable | Use Case |
|--------|-----------|------------------------|----------|
| **Raw counts** | Number of reads/fragments mapped to gene | No | Input for DESeq2/edgeR differential expression |
| **TPM** (Transcripts Per Million) | Counts normalized by gene length then library size | Yes | Cross-sample expression comparison |
| **FPKM** (Fragments Per Kilobase per Million) | Counts normalized by library size then gene length | No | Legacy; avoid for cross-sample comparison |

### When to Use Each

- **Differential expression**: Use raw `expected_count` from RSEM with DESeq2 or edgeR.
  These tools apply their own normalization (median-of-ratios or TMM).
- **Cross-sample comparison**: Use TPM. It sums to 1M per sample, enabling direct comparison.
- **Single-gene reporting**: TPM is appropriate for reporting expression of individual genes.
- **Avoid FPKM**: FPKM does not sum to a constant across samples, making it unreliable
  for cross-sample comparison. TPM is strictly preferred.

## QC Checkpoints

| Check | Threshold | Action if Failed |
|-------|-----------|------------------|
| Detected genes (TPM>1) | >12,000 (human) | Check sequencing depth, RNA quality |
| RSEM mapping rate | >70% of transcriptome BAM reads | Check strandedness setting |
| TPM correlation between replicates | r > 0.95 (Pearson) | Check batch effects, sample swap |
| Gene count distribution | Log-normal shape expected | Skewed distribution suggests degradation |
