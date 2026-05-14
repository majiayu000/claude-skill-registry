# Methylation Calling with MethylDackel

MethylDackel (formerly PileOMeth) extracts per-CpG methylation levels from
bisulfite-aligned BAM files, producing bedMethyl output compatible with
ENCODE standards.

## M-bias Assessment (Run First)

Before extracting methylation, generate M-bias plots to identify positional biases:

```bash
MethylDackel mbias \
    --CHG --CHH \
    --nOT 0,0,0,0 \
    --nOB 0,0,0,0 \
    /ref/genome/genome.fa \
    sample_dedup.bam \
    sample_mbias
```

This produces SVG plots showing methylation level by read position. Look for:
- Elevated methylation at the 5' end of read 2 (end-repair artifact)
- Irregular methylation at read ends (adapter contamination)
- ENCODE typically trims: `--nOT 0,0,0,10 --nOB 0,10,0,0` (10 bp from R2 5' end)

## Methylation Extraction

```bash
MethylDackel extract \
    --mergeContext \
    --minDepth 5 \
    --maxDepth 8000 \
    --nOT 0,0,0,10 \
    --nOB 0,10,0,0 \
    --CHG --CHH \
    --opref sample_output \
    /ref/genome/genome.fa \
    sample_dedup.bam
```

### Key Parameters

| Parameter | Value | Reason |
|-----------|-------|--------|
| `--mergeContext` | Enabled | Merge forward/reverse strand CpG data |
| `--minDepth 5` | 5 reads | Minimum coverage for reliable calls |
| `--maxDepth 8000` | 8000 reads | Exclude extreme pileups (centromeres, repeats) |
| `--nOT 0,0,0,10` | Trim 10bp | OT: original top strand -- trim R2 5' end |
| `--nOB 0,10,0,0` | Trim 10bp | OB: original bottom strand -- trim R1 3' end |
| `--CHG --CHH` | Enabled | Also extract non-CpG methylation (useful for ESCs, neurons) |

### Context-Specific Output Files

MethylDackel produces separate files per context:
- `sample_output_CpG.bedGraph` -- CpG methylation (primary)
- `sample_output_CHG.bedGraph` -- CHG methylation (non-CpG)
- `sample_output_CHH.bedGraph` -- CHH methylation (non-CpG)

## Convert to bedMethyl Format

MethylDackel bedGraph output needs conversion to full bedMethyl:

```bash
awk 'BEGIN {OFS="\t"} {
    coverage = $5 + $6;
    methpct = ($5 / coverage) * 100;
    print $1, $2, $3, ".", int(methpct * 10), "+", $2, $3, "0,0,0", coverage, methpct
}' sample_output_CpG.bedGraph > sample.CpG.bedMethyl

# Sort and compress
sort -k1,1 -k2,2n sample.CpG.bedMethyl | bgzip > sample.CpG.bedMethyl.gz
tabix -p bed sample.CpG.bedMethyl.gz
```

## Per-Chromosome Extraction (Parallel)

For large BAMs, parallelize by chromosome:

```bash
for chr in $(samtools idxstats sample_dedup.bam | cut -f1 | grep -v '*'); do
    MethylDackel extract \
        --mergeContext \
        --minDepth 5 \
        --nOT 0,0,0,10 \
        --nOB 0,10,0,0 \
        --opref "perchr/${chr}" \
        -r "${chr}" \
        /ref/genome/genome.fa \
        sample_dedup.bam &
done
wait

# Concatenate results
cat perchr/*_CpG.bedGraph | sort -k1,1 -k2,2n > sample_CpG.bedGraph
```

## Global Methylation Summary

Compute genome-wide methylation statistics:

```bash
awk '{
    meth += $5; unmeth += $6
} END {
    total = meth + unmeth;
    print "Total CpGs:", NR;
    print "Mean methylation:", (meth/total)*100 "%";
    print "Methylated reads:", meth;
    print "Unmethylated reads:", unmeth
}' sample_output_CpG.bedGraph
```

Expected values for mammalian somatic tissue:
- Global CpG methylation: 70-85%
- CpG islands: 5-15% (mostly unmethylated)
- Gene bodies: 60-80%
- Intergenic: 75-90%
