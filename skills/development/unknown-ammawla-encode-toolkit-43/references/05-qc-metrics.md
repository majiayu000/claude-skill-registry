# CUT&RUN QC Metrics

Quality assessment for CUT&RUN data includes standard alignment metrics,
CUT&RUN-specific fragment analysis, spike-in validation, and peak quality.

## Fragment Size Distribution

The fragment size distribution is the most informative CUT&RUN QC metric:

```bash
# Extract fragment sizes from properly paired reads
samtools view -f 2 -F 1804 sample_final.bam | \
    awk '{if($9 > 0 && $9 < 1000) print $9}' | \
    sort -n | uniq -c | \
    awk '{print $2, $1}' > fragment_sizes.txt
```

### Expected Patterns by Target

| Target Type | Fragment Pattern | Example |
|-------------|-----------------|---------|
| TF (CTCF, etc.) | Peak <120 bp, some at 150 bp | Sharp sub-nucleosomal |
| Active histone (H3K4me3) | Strong 150 bp peak | Mononucleosomal |
| Repressive histone (H3K27me3) | 150 bp + 300 bp | Mono + dinucleosomal |
| IgG control | Flat distribution | No enrichment pattern |

### Red Flags in Fragment Distribution

- No nucleosomal periodicity: Protocol may have failed
- Only large fragments (>300 bp): Over-digestion or poor tagmentation
- Spike at exact read length: Adapter trimming incomplete
- Identical to IgG: No target enrichment

## Spike-in QC

### Spike-in Fraction

```bash
genome=$(samtools view -c -F 1804 -f 2 sample_final.bam)
spikein=$(samtools view -c -F 1804 -f 2 sample_spikein.bam)
fraction=$(echo "scale=4; $spikein / ($genome + $spikein)" | bc)
echo "Spike-in fraction: $fraction"
```

| Fraction | Status | Interpretation |
|----------|--------|---------------|
| 1-10% | Optimal | Good balance of target and calibration |
| 0.1-1% | Acceptable | Low spike-in, normalization less precise |
| <0.1% | Warning | Insufficient spike-in for normalization |
| >10% | Warning | Excess spike-in, may indicate poor enrichment |
| >30% | Fail | Mostly spike-in reads, minimal target signal |

### Spike-in Consistency Across Samples

For reliable normalization, spike-in counts should vary across samples
(reflecting different amounts of target material), but not be zero:

```bash
# Compare spike-in across all samples
for bam in *_spikein.bam; do
    sample=$(basename $bam _spikein.bam)
    count=$(samtools view -c -F 1804 -f 2 $bam)
    echo "$sample $count"
done | sort -k2 -n
```

## Alignment Statistics

```bash
samtools flagstat sample_final.bam > flagstat.txt
```

### Key Metrics

| Metric | Pass | Warning | Fail |
|--------|------|---------|------|
| Mapping rate | >80% | 60-80% | <60% |
| Properly paired | >90% | 70-90% | <70% |
| Duplication rate | <20% | 20-40% | >40% |

## FRiP (Fraction of Reads in Peaks)

```bash
total=$(samtools view -c -F 1804 -f 2 sample_final.bam)
in_peaks=$(bedtools intersect \
    -a sample_final.bam \
    -b peaks_filtered.bed \
    -u -bed | wc -l)
frip=$(echo "scale=4; $in_peaks / $total" | bc)
echo "FRiP: $frip"
```

| FRiP | Status | Note |
|------|--------|------|
| >20% | Excellent | Strong enrichment |
| 10-20% | Good | Standard CUT&RUN |
| 5-10% | Acceptable | May need more sequencing |
| <5% | Poor | Weak enrichment or high background |

CUT&RUN typically has higher FRiP than ChIP-seq because of lower background.

## Peak Count and Size

```bash
# Peak statistics
total_peaks=$(wc -l < peaks_filtered.bed)
echo "Total peaks: $total_peaks"

# Peak size distribution
awk '{print $3-$2}' peaks_filtered.bed | \
    awk '{sum+=$1; n++; a[n]=$1} END {
        asort(a);
        print "Median peak size:", a[int(n/2)];
        print "Mean peak size:", sum/n;
        print "Min:", a[1];
        print "Max:", a[n]
    }'
```

## MultiQC Aggregation

```bash
multiqc \
    --title "CUT&RUN Pipeline QC" \
    --filename multiqc_report \
    --outdir multiqc/ \
    fastqc/ trim_galore/ alignment/ qc/
```

## Summary QC Table

Generate a per-sample summary:

```bash
echo -e "Sample\tReads\tMap_Rate\tDedup_Rate\tSpikein_Frac\tPeaks\tFRiP\tFrag_Peak"
echo -e "${SAMPLE}\t${TOTAL}\t${MAP_RATE}\t${DUP_RATE}\t${SPIKEIN}\t${PEAKS}\t${FRIP}\t${FRAG}"
```
