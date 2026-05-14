# Stage 5: QC Metrics

## Tools
- **RSeQC v4.0+**: RNA-seq quality control suite (Wang et al. 2012, ~3,500 citations)
- **MultiQC v1.14+**: Aggregated QC report generation

## RSeQC Modules

### infer_experiment.py (Strandedness Check)

```bash
infer_experiment.py -r hg38_RefSeq.bed -i Aligned.sortedByCoord.out.bam
```

Determines library strandedness by sampling read orientation relative to annotated
transcripts. Critical first check -- wrong strandedness silently produces near-zero counts.

| Output Pattern | Interpretation | RSEM Setting |
|----------------|---------------|-------------|
| "1++,1--,2+-,2-+" > 90% | Forward stranded | `--strandedness forward` |
| "1+-,1-+,2++,2--" > 90% | Reverse stranded (dUTP) | `--strandedness reverse` |
| ~50/50 split | Unstranded | `--strandedness none` |

**ENCODE standard**: Expect >90% reverse-stranded reads for dUTP libraries.

### read_distribution.py (Mapping Distribution)

```bash
read_distribution.py -r hg38_RefSeq.bed -i Aligned.sortedByCoord.out.bam
```

Reports fraction of reads mapping to CDS exons, 5' UTR, 3' UTR, introns, and
intergenic regions.

| Region | Expected (mRNA-seq) | Concern Threshold |
|--------|--------------------|--------------------|
| CDS exons | 40-60% | <30% suggests degradation or DNA contamination |
| 5' UTR | 5-10% | <2% suggests 5' degradation |
| 3' UTR | 15-25% | >40% suggests 3' bias (degraded RNA) |
| Introns | 10-25% | >40% suggests DNA contamination or pre-mRNA |
| Intergenic | <5% | >10% suggests DNA contamination |

### geneBody_coverage.py (Gene Body Coverage)

```bash
geneBody_coverage.py -r hg38_HouseKeeping.bed \
  -i Aligned.sortedByCoord.out.bam -o sample_coverage
```

Plots normalized coverage across gene bodies (5' to 3'). Uniform coverage indicates
intact RNA; strong 3' bias indicates degradation.

| Pattern | Interpretation |
|---------|---------------|
| Uniform (5'/3' ratio 0.7-1.3) | Good RNA quality |
| 3' bias (5'/3' ratio <0.5) | RNA degradation |
| 5' bias (5'/3' ratio >2.0) | Possible oligo-dT priming bias |

### inner_distance.py (Insert Size Distribution)

```bash
inner_distance.py -r hg38_RefSeq.bed \
  -i Aligned.sortedByCoord.out.bam -o sample_inner_dist
```

Reports the inner distance between paired-end read mates. For RNA-seq, negative
values indicate overlapping reads (common for short inserts). Peak should match
expected library insert size (typically 150-300 bp).

### STAR Log Metrics

The `Log.final.out` from STAR provides critical metrics:

| Metric | Threshold | Notes |
|--------|-----------|-------|
| Uniquely mapped reads % | >=70% | Primary quality indicator |
| Multi-mapped reads % | <10% | High suggests repetitive contamination |
| Unmapped: too short % | <10% | High suggests over-trimming |
| % of reads mapped to multiple loci | <10% | Expected for gene families |
| % of chimeric reads | <1% | Unless fusion analysis |
| Number of splices: Total | Millions expected | Low count suggests annotation mismatch |

### rRNA Rate Assessment

```bash
# Count rRNA reads from STAR ReadsPerGene or samtools
samtools view -c -F 4 Aligned.sortedByCoord.out.bam rRNA_intervals.bed
```

| rRNA Rate | Interpretation |
|-----------|---------------|
| <5% | Excellent rRNA depletion |
| 5-10% | Acceptable |
| 10-30% | Suboptimal; reduced effective depth |
| >30% | Failed rRNA depletion; consider re-prep |

### Saturation Analysis

```bash
# RSeQC RPKM saturation
RPKM_saturation.py -r hg38_RefSeq.bed \
  -i Aligned.sortedByCoord.out.bam -o sample_saturation
```

Subsamples reads at increasing fractions (5%, 10%, ..., 100%) and measures gene
detection. A plateau indicates sufficient sequencing depth. If the curve is still
rising at 100%, more sequencing is recommended.

## MultiQC Aggregation

```bash
multiqc . -o multiqc_output/ -f
```

MultiQC aggregates reports from FastQC, Trim Galore, STAR, RSEM, RSeQC, and Picard
into a single interactive HTML report. Review the MultiQC report as the first step
in QC assessment.

## Expected Output
- `infer_experiment.txt` -- strandedness inference
- `read_distribution.txt` -- mapping distribution by genomic feature
- `geneBody_coverage.png` -- gene body coverage plot
- `inner_distance_plot.pdf` -- insert size distribution
- `multiqc_report.html` -- aggregated QC report
