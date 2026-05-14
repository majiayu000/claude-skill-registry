# Bismark Alignment for WGBS

Bisulfite-converted reads require a specialized aligner that accounts for
C-to-T conversion. Bismark handles this by aligning to both C-to-T and G-to-A
converted genomes simultaneously.

## Genome Preparation

Build the bisulfite-converted genome index (one-time step):

```bash
bismark_genome_preparation \
    --bowtie2 \
    --parallel 4 \
    --verbose \
    /ref/genome/
```

This creates two converted genomes:
- C-to-T converted (for original top strand and complementary to bottom)
- G-to-A converted (for original bottom strand and complementary to top)

Requires approximately 12 GB disk space for human genome.

## Bismark Alignment

```bash
bismark \
    --genome /ref/genome/ \
    --bowtie2 \
    --parallel 4 \
    --score_min L,0,-0.2 \
    --no_mixed \
    --no_discordant \
    --maxins 1000 \
    --temp_dir /tmp/bismark/ \
    -1 sample_R1_trimmed.fq.gz \
    -2 sample_R2_trimmed.fq.gz \
    --output_dir bismark_out/
```

### Key Parameters

| Parameter | Value | Reason |
|-----------|-------|--------|
| `--parallel 4` | 4 instances | Each uses 2 Bowtie2 threads = 8 total threads |
| `--score_min L,0,-0.2` | Linear penalty | ENCODE default; tolerates bisulfite mismatches |
| `--no_mixed` | Discard | Both mates must align |
| `--no_discordant` | Discard | Mates must be properly paired |
| `--maxins 1000` | 1000 bp | Maximum insert size for paired reads |

### Memory Requirements

Bismark parallel mode uses approximately 6 GB per Bowtie2 instance.
With `--parallel 4`, expect ~24 GB peak RAM for human genome alignment.

## Alternative: bwa-meth

bwa-meth is faster than Bismark for large genomes and uses less memory:

```bash
# Index genome (one-time)
bwameth.py index /ref/genome/genome.fa

# Align
bwameth.py \
    --threads 8 \
    --reference /ref/genome/genome.fa \
    sample_R1_trimmed.fq.gz \
    sample_R2_trimmed.fq.gz \
    | samtools sort -@ 4 -o sample_bwameth.bam

samtools index sample_bwameth.bam
```

### Bismark vs bwa-meth Comparison

| Feature | Bismark | bwa-meth |
|---------|---------|----------|
| Speed | Slower (~2x) | Faster |
| RAM | ~48 GB (parallel) | ~16 GB |
| Accuracy | Gold standard | Comparable |
| ENCODE pipeline | Primary | Supported |
| Methylation calling | Built-in | Requires MethylDackel |

Recommendation: Use Bismark for ENCODE compatibility. Use bwa-meth when
processing many samples and speed is critical.

## Lambda/pUC19 Spike-in Alignment

If spike-in DNA was used, align to the spike-in genome to measure conversion rate:

```bash
bismark \
    --genome /ref/lambda/ \
    --bowtie2 \
    -1 sample_R1_trimmed.fq.gz \
    -2 sample_R2_trimmed.fq.gz \
    --output_dir lambda_out/ \
    --unmapped
```

The lambda genome is fully unmethylated, so any detected methylation represents
incomplete bisulfite conversion. Expect conversion rate ≥98%.

## Alignment QC Checks

After alignment, verify in the Bismark report:
- **Mapping efficiency**: >70% for WGBS (lower than standard WGS due to conversion)
- **Unique alignments**: Should dominate over multimappers
- **C methylated in CpG context**: Typically 70-85% for mammalian somatic tissue
- **C methylated in CHG context**: Should be <1% in somatic tissue (>5% in plants/ESCs)
- **C methylated in CHH context**: Should be <1% in somatic tissue
