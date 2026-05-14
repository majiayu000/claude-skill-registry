# Stage 2: Alignment

## Tools
- **BWA-MEM v0.7.17+**: Primary aligner for ChIP-seq (Li & Durbin, 2009)
- **Samtools v1.15+**: BAM conversion, sorting, indexing, and statistics

## Reference Genome

| Organism | Assembly | BWA Index Source |
|----------|----------|-----------------|
| Human | GRCh38 (hg38) | `https://www.encodeproject.org/files/GRCh38_no_alt_analysis_set_GCA_000001405.15/` |
| Mouse | mm10 (GRCm38) | `https://www.encodeproject.org/files/mm10_no_alt_analysis_set_ENCODE/` |

**Important**: Use the ENCODE "no alt" analysis set which excludes alternate haplotype
contigs and decoy sequences. This prevents ambiguous multi-mapping to alternate loci.

## Parameters

| Parameter | Value | Notes |
|-----------|-------|-------|
| BWA algorithm | mem | Recommended for reads >70bp |
| BWA threads (`-t`) | 8 | Adjust to available cores |
| BWA `-M` flag | yes | Mark shorter split hits as secondary (Picard compatible) |
| MAPQ filter | 30 | Remove multi-mappers (MAPQ<30) |
| Sort order | coordinate | Required for Picard and peak calling |
| Sort memory | 4G per thread | Adjust with `-m` flag |

## Commands

```bash
# Paired-end alignment
bwa mem -t 8 -M genome.fa trimmed_R1.fq.gz trimmed_R2.fq.gz | \
  samtools view -@ 4 -bS -q 30 - | \
  samtools sort -@ 4 -m 4G -o aligned.bam -
samtools index aligned.bam

# Single-end alignment
bwa mem -t 8 -M genome.fa trimmed.fq.gz | \
  samtools view -@ 4 -bS -q 30 - | \
  samtools sort -@ 4 -m 4G -o aligned.bam -
samtools index aligned.bam

# Alignment statistics
samtools flagstat aligned.bam > flagstat.txt
samtools idxstats aligned.bam > idxstats.txt
samtools stats aligned.bam > stats.txt
```

## Expected Output
- `aligned.bam` + `aligned.bam.bai` -- coordinate-sorted, indexed BAM
- `flagstat.txt` -- alignment summary (total, mapped, paired, properly paired)
- `idxstats.txt` -- per-chromosome read counts (useful for detecting mito contamination)
- `stats.txt` -- detailed alignment statistics

## QC Checkpoints

| Check | Threshold | Action if Failed |
|-------|-----------|------------------|
| Mapping rate | >80% | Check genome build match, contamination |
| Mapped reads | >=20M (TF), >=45M (histone) | Sequence more or pool |
| MAPQ>=30 fraction | >70% of mapped reads | Check for repetitive regions enrichment |
| Properly paired (PE) | >90% of mapped | Check library preparation |
| Mitochondrial reads | <5% (check via idxstats) | Normal for some cell types; filter in Stage 3 |

## Notes

- The MAPQ 30 filter removes reads mapping to multiple locations. For repetitive element
  analysis, consider relaxing this threshold.
- BWA-MEM is preferred over BWA-ALN for reads longer than 70bp. For older datasets with
  shorter reads, BWA-ALN may be more appropriate.
- The `-M` flag ensures compatibility with Picard MarkDuplicates in Stage 3.
