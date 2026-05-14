# ATAC-seq vs DNase-seq: Concordance and Differences

Reference guide for understanding when ATAC-seq and DNase-seq are interchangeable and when platform-specific considerations matter.

## The Corces et al. 2017 Concordance Study

Corces et al. (2017, Nature Methods, 733 citations) performed the definitive comparison of ATAC-seq and DNase-seq for chromatin accessibility profiling. Key findings:

- ATAC-seq captures approximately **75% of DNase-seq hypersensitive sites**
- Sites detected by both assays show **highly concordant signal intensities** (Pearson r > 0.8)
- ATAC-specific sites tend to be **weaker** DNase sites (present but below DNase calling threshold)
- DNase-specific sites tend to be in **GC-rich regions** where Tn5 insertion is biased
- For regulatory element discovery, the two assays are **largely interchangeable**

**Implication for aggregation**: Combining ATAC-seq and DNase-seq peaks in a union set is scientifically justified. Both assays detect the same biological signal (open chromatin) through different enzymatic mechanisms.

## Enzymatic Mechanism Differences

| Property | ATAC-seq | DNase-seq |
|----------|----------|-----------|
| Enzyme | Tn5 transposase | DNase I endonuclease |
| Mechanism | Inserts sequencing adapters into open chromatin | Cleaves exposed DNA |
| Fragment sizes | Nucleosome-free (<150bp) + mono-nucleosome (~200bp) | Continuous size range |
| Resolution | High (single-nucleotide Tn5 insertion sites) | High (DNase I cut sites) |
| Input cells | 500 - 50,000 cells | 100,000 - 1,000,000 cells |
| Protocol complexity | Simple (1-2 hour protocol) | Complex (multi-day) |

## Known Biases

### Tn5 Sequence Preference (ATAC-seq)

Tn5 transposase has a mild sequence preference for insertion:
- Slight bias toward **10bp periodicity** matching nucleosome wrapping
- Moderate **GC content preference** at insertion sites
- These biases affect peak **intensity** (signal strength), not peak **presence**
- For union-based aggregation, this is acceptable since we care about detection, not quantification

### DNase I Cleavage Bias (DNase-seq)

DNase I also has sequence preferences:
- Slight preference for **WW dinucleotides** (W = A or T)
- Less GC-biased than Tn5
- Can create false hotspots at highly accessible repetitive elements

### Mitochondrial DNA Contamination (ATAC-seq)

ATAC-seq libraries typically contain **30-80% mitochondrial reads** because:
- Mitochondrial DNA is highly accessible (no histones)
- Tn5 readily inserts into mtDNA
- ENCODE pipeline removes these reads post-alignment
- Always verify mtDNA fraction in QC metrics

DNase-seq does **not** have this issue because the protocol uses nuclei (mitochondria excluded).

## Fragment Size Information

ATAC-seq uniquely provides chromatin structure information through fragment sizes:

| Fragment Class | Size Range | Represents |
|---------------|------------|------------|
| Sub-nucleosomal | < 100 bp | Open chromatin / Tn5 artifacts |
| Nucleosome-free | 100-150 bp | True open chromatin regions |
| Mono-nucleosome | 180-250 bp | Single nucleosome wrapping |
| Di-nucleosome | 315-475 bp | Two nucleosomes |

This information is **not available** in DNase-seq. For peak-based aggregation, fragment size filtering is typically already done by the ENCODE pipeline.

## When to Combine ATAC + DNase

### Recommended (same tissue, different assays)

Combine when building a comprehensive accessibility catalog:
- Maximizes genomic coverage
- Captures sites each assay alone might miss
- Union approach handles platform-specific sensitivity differences

### Caution Needed

- **Quantitative comparisons**: Do not directly compare signal intensities between ATAC and DNase peaks. Normalize separately.
- **Footprinting analysis**: Tn5 and DNase I have different cleavage profiles. Do not combine for transcription factor footprinting.
- **Nucleosome positioning**: Only ATAC-seq provides fragment size-based nucleosome information.

### Not Recommended

- **Differential accessibility**: Do not treat ATAC and DNase as replicates in differential analysis. Platform effects dominate.
- **Single-cell comparisons**: scATAC-seq and scDNase-seq (if available) have very different sparsity patterns.

## ENCODE Data Availability

| Assay | ENCODE Experiments | Period | Peak Caller |
|-------|-------------------|--------|-------------|
| DNase-seq | ~800+ experiments | 2007-present | Hotspot2, MACS2 |
| ATAC-seq | ~400+ experiments | 2015-present | MACS2 |

For tissues with both assay types available, combining yields the most comprehensive map. For tissues with only one assay, either is sufficient for accessibility cataloging.

## Practical Workflow for Combined Aggregation

```bash
# 1. Download ATAC and DNase peaks separately
# 2. Filter both through ENCODE blacklist
# 3. Apply signalValue filter to each sample independently
# 4. Tag peaks by sample AND assay type

awk -v sid="atac_donor1" 'BEGIN{OFS="\t"} {$4=sid; print}' atac_sample.narrowPeak > tagged.bed
awk -v sid="dnase_donor1" 'BEGIN{OFS="\t"} {$4=sid; print}' dnase_sample.narrowPeak >> tagged.bed

# 5. Union merge (treat as equal sources)
cat *.tagged.bed | bedtools sort | bedtools merge -c 4 -o count_distinct > union.bed

# 6. Optionally annotate whether support comes from ATAC, DNase, or both
```

## References

- Corces et al. 2017, Nature Methods -- definitive ATAC vs DNase concordance study (733 citations)
- Buenrostro et al. 2013, Nature Methods -- original ATAC-seq protocol (6,800+ citations)
- Thurman et al. 2012, Nature -- DNase-seq regulatory landscape (ENCODE Phase 2)
- Yan et al. 2020, Genome Biology -- comprehensive Tn5 sequence bias characterization
- Sung et al. 2014, Nature Methods -- DNase-seq protocol optimization
- Zhao & Boyle 2020, NAR Genomics -- F-Seq2 peak caller for both ATAC and DNase
