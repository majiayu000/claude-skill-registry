# Stage 2: Alignment

## Tools
- **Bowtie2 v2.4.5+**: Primary aligner for ATAC-seq (Langmead & Salzberg 2012, ~30,000 citations)
- **Samtools v1.15+**: BAM conversion, sorting, indexing, and statistics

## Why Bowtie2 Instead of BWA
Bowtie2 is preferred for ATAC-seq because:
1. Better handling of short fragments (NFR <150 bp)
2. `--very-sensitive` mode provides optimal alignment for ATAC-seq read characteristics
3. Concordant paired-end alignment with fragment size constraints
4. Standard in the ENCODE ATAC-seq pipeline

## Reference Genome

| Organism | Assembly | Bowtie2 Index Source |
|----------|----------|---------------------|
| Human | GRCh38 (hg38) | `https://www.encodeproject.org/files/GRCh38_no_alt_analysis_set_GCA_000001405.15/` |
| Mouse | mm10 (GRCm38) | `https://www.encodeproject.org/files/mm10_no_alt_analysis_set_ENCODE/` |

Use the ENCODE "no alt" analysis set (excludes alternate haplotypes and decoys).

## Parameters

| Parameter | Value | Notes |
|-----------|-------|-------|
| Bowtie2 mode | --very-sensitive | Optimal sensitivity for ATAC-seq |
| Threads | 8 | Adjust to available cores |
| Max fragment size (-X) | 2000 | Accommodate di/tri-nucleosomal fragments |
| No mixed (--no-mixed) | yes | Require both mates to align |
| No discordant (--no-discordant) | yes | Require concordant alignment |
| MAPQ filter | 30 | Remove multi-mappers |

## Commands

```bash
# Paired-end alignment with Bowtie2
bowtie2 --very-sensitive -X 2000 --no-mixed --no-discordant \
  --threads 8 -x genome_index \
  -1 trimmed_R1.fq.gz -2 trimmed_R2.fq.gz | \
  samtools view -@ 4 -bS -q 30 -f 2 - | \
  samtools sort -@ 4 -m 4G -o aligned.bam -
samtools index aligned.bam

# Alignment statistics
samtools flagstat aligned.bam > flagstat.txt
samtools idxstats aligned.bam > idxstats.txt
```

## Expected Output
- `aligned.bam` + `aligned.bam.bai` -- coordinate-sorted, indexed BAM
- `flagstat.txt` -- alignment summary
- `idxstats.txt` -- per-chromosome read counts (critical for mito assessment)

## QC Checkpoints

| Check | Threshold | Action if Failed |
|-------|-----------|------------------|
| Overall alignment rate | >80% | Check genome build, contamination |
| Concordant pair rate | >90% | Check library prep |
| MAPQ>=30 fraction | >60% of mapped | Expected lower than ChIP due to open chromatin |
| Mitochondrial reads | <20% (record) | Will be removed in Stage 3 |
| Total mapped reads | >=25M after mito removal | May need deeper sequencing |

## Notes
- The `-f 2` flag in samtools retains only properly paired reads.
- `-X 2000` allows Bowtie2 to map large fragments from di/tri-nucleosomal DNA.
- Mitochondrial read fraction varies by cell type and preparation; record it here
  but filter in Stage 3.
