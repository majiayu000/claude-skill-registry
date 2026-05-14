# Bowtie2 Alignment for CUT&RUN (Genome + Spike-in)

CUT&RUN uses Bowtie2 for alignment with specific settings optimized for the
short, paired-end fragments produced by MNase or Tn5 cleavage. Two separate
alignments are required: one to the target genome and one to the E. coli
spike-in genome.

## Genome Index Preparation

```bash
# Target genome (one-time)
bowtie2-build --threads 8 genome.fa genome_index

# E. coli spike-in genome (one-time)
# Use E. coli K12 MG1655 (GenBank: U00096.3)
bowtie2-build --threads 4 ecoli_K12.fa ecoli_index
```

## Target Genome Alignment

```bash
bowtie2 \
    --very-sensitive \
    --no-mixed \
    --no-discordant \
    --dovetail \
    --phred33 \
    -I 10 -X 700 \
    --threads 8 \
    -x genome_index \
    -1 sample_R1_val_1.fq.gz \
    -2 sample_R2_val_2.fq.gz \
    2> sample_bowtie2.log \
    | samtools view -@ 4 -bS - \
    | samtools sort -@ 4 -o sample_sorted.bam

samtools index sample_sorted.bam
```

### Bowtie2 Parameters for CUT&RUN

| Parameter | Value | Reason |
|-----------|-------|--------|
| `--very-sensitive` | Preset | Maximum sensitivity for short fragments |
| `--no-mixed` | Flag | Both mates must align |
| `--no-discordant` | Flag | Mates must be properly paired |
| `--dovetail` | Flag | Allow dovetail alignments (overlapping PE reads) |
| `-I 10` | 10 bp | Minimum insert size (very short fragments exist) |
| `-X 700` | 700 bp | Maximum insert size |

**Critical**: The `--dovetail` flag is essential because CUT&RUN fragments
are often shorter than read length, causing R1 and R2 to extend past each
other (dovetailing).

## Spike-in Alignment

Align reads that did NOT map to the target genome to the E. coli spike-in:

```bash
# Extract unmapped reads from genome alignment
samtools view -b -f 12 -F 256 sample_sorted.bam \
    | samtools sort -@ 4 -n -o unmapped_sorted.bam

bedtools bamtofastq -i unmapped_sorted.bam \
    -fq unmapped_R1.fq -fq2 unmapped_R2.fq

# Align to E. coli
bowtie2 \
    --very-sensitive \
    --no-mixed \
    --no-discordant \
    --dovetail \
    --phred33 \
    -I 10 -X 700 \
    --threads 4 \
    -x ecoli_index \
    -1 unmapped_R1.fq \
    -2 unmapped_R2.fq \
    2> sample_spikein.log \
    | samtools view -@ 2 -bS -q 10 -F 1804 -f 2 - \
    | samtools sort -@ 2 -o sample_spikein.bam

samtools index sample_spikein.bam
```

### Alternative: Direct Spike-in Alignment

Some workflows align ALL reads to both genomes simultaneously using a
concatenated index. This is simpler but less precise:

```bash
# Concatenate genomes (one-time)
cat genome.fa ecoli_K12.fa > combined.fa
bowtie2-build --threads 8 combined.fa combined_index

# Align to combined genome
bowtie2 --very-sensitive --no-mixed --no-discordant --dovetail \
    -I 10 -X 700 --threads 8 \
    -x combined_index \
    -1 R1.fq.gz -2 R2.fq.gz \
    | samtools view -bS - > combined.bam

# Separate by genome
samtools view -b combined.bam chr1 chr2 ... chrX chrY > genome.bam
samtools view -b combined.bam ecoli_chr > spikein.bam
```

## Spike-in Read Counts

```bash
# Count spike-in reads
spikein_count=$(samtools view -c -F 1804 -f 2 sample_spikein.bam)
genome_count=$(samtools view -c -F 1804 -f 2 sample_sorted.bam)
echo "Spike-in reads: ${spikein_count}"
echo "Genome reads: ${genome_count}"
echo "Spike-in fraction: $(echo "scale=4; $spikein_count / ($spikein_count + $genome_count)" | bc)"
```

Expected spike-in fraction:
- **1-10%**: Optimal range for normalization
- **<0.1%**: Too few spike-in reads for reliable normalization
- **>30%**: Excessive spike-in; may indicate poor target enrichment

## Alignment QC

```bash
# Parse Bowtie2 log for mapping rate
grep "overall alignment rate" sample_bowtie2.log
```

Expected mapping rates:
- **Target genome**: >80% for standard samples
- **Spike-in**: 1-10% of unmapped reads should map to E. coli

Low genome mapping rate may indicate:
- Contamination (check FastQ Screen)
- Wrong genome build
- Very poor library quality
