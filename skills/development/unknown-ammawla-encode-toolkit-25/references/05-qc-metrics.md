# WGBS QC Metrics and Conversion Rate Assessment

Quality control for WGBS requires bisulfite-specific metrics beyond
standard alignment QC. The most critical metric is bisulfite conversion rate.

## Bisulfite Conversion Rate (Lambda Spike-in)

Lambda phage DNA is fully unmethylated. Any methylation detected on lambda
represents incomplete bisulfite conversion.

```bash
# Align to lambda genome
bismark \
    --genome /ref/lambda/ \
    --bowtie2 \
    --parallel 2 \
    -1 sample_R1_trimmed.fq.gz \
    -2 sample_R2_trimmed.fq.gz \
    --output_dir lambda_out/ \
    --unmapped

# Extract methylation from lambda alignments
MethylDackel extract \
    --mergeContext \
    --minDepth 1 \
    /ref/lambda/genome.fa \
    lambda_out/sample_pe.bam

# Calculate conversion rate
awk '{meth+=$5; unmeth+=$6} END {
    total=meth+unmeth;
    conv=(unmeth/total)*100;
    print "Conversion rate: " conv "%";
    print "Unconverted (false methylation): " (meth/total)*100 "%"
}' lambda_CpG.bedGraph
```

### Conversion Rate Thresholds

| Rate | Status | Action |
|------|--------|--------|
| >99.5% | Excellent | Proceed |
| 99.0-99.5% | Acceptable | Proceed with note |
| 98.0-99.0% | Warning | May inflate methylation estimates |
| <98.0% | Fail | Do NOT use this library |

## Non-CpG Methylation as Conversion Proxy

If no spike-in is available, use CHH methylation as a proxy:

```bash
awk '{meth+=$5; unmeth+=$6} END {
    print "CHH methylation: " (meth/(meth+unmeth))*100 "%"
}' sample_output_CHH.bedGraph
```

In somatic tissue, CHH methylation should be <1%. Higher values suggest
incomplete conversion. Exception: embryonic stem cells and neurons can have
genuine non-CpG methylation (2-5%).

## Coverage Statistics

```bash
# Genome-wide coverage distribution
samtools depth -a sample_filtered.bam | \
    awk '{cov[$3]++} END {for (c in cov) print c, cov[c]}' | \
    sort -k1,1n > coverage_distribution.txt

# Mean and median coverage
samtools depth -a sample_filtered.bam | \
    awk '{sum+=$3; n++; a[n]=$3} END {
        asort(a);
        print "Mean:", sum/n;
        print "Median:", a[int(n/2)];
        print "Total bases:", n;
        print "Bases >=5x:", sum5/n*100 "%"
    }'

# CpG-specific coverage
awk '{print $5+$6}' sample_output_CpG.bedGraph | \
    awk '{sum+=$1; n++; if($1>=1) c1++; if($1>=5) c5++; if($1>=10) c10++} END {
        print "CpGs with >=1x:", c1, "(" c1/n*100 "%)";
        print "CpGs with >=5x:", c5, "(" c5/n*100 "%)";
        print "CpGs with >=10x:", c10, "(" c10/n*100 "%)";
        print "Mean CpG coverage:", sum/n
    }'
```

## Mapping Statistics

```bash
samtools flagstat sample_filtered.bam > flagstat.txt
```

Key values to extract:
- Total reads (after filtering)
- Mapped reads (expect >70%)
- Properly paired (expect >95% of mapped)
- Duplication rate (from dedup step)

## MultiQC Report

Aggregate all QC metrics into a single report:

```bash
multiqc \
    --title "WGBS Pipeline QC" \
    --filename multiqc_report \
    --outdir multiqc/ \
    fastqc_raw/ trim_galore/ bismark_out/ dedup/ methylation/
```

MultiQC recognizes and parses:
- FastQC reports
- Trim Galore logs
- Bismark alignment reports
- Bismark deduplication reports
- Picard MarkDuplicates metrics

## Summary QC Table Format

Generate a per-sample summary for reporting:

```bash
echo -e "Sample\tTotal_Reads\tMapping_Rate\tDedup_Rate\tConversion\tMean_CpG_Cov\tCpGs_5x"
echo -e "${SAMPLE}\t${TOTAL}\t${MAP_RATE}\t${DEDUP_RATE}\t${CONV_RATE}\t${MEAN_COV}\t${CPGS_5X}"
```
