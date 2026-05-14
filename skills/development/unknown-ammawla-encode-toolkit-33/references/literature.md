# CUT&RUN Pipeline — Literature References

**Last updated:** 2026-03-07
**Purpose:** Reference catalog for the pipeline-cutandrun skill — papers defining CUT&RUN and CUT&Tag methods, SEACR peak calling, spike-in normalization, and the CUT&RUN suspect list for artifact filtering.

---

## CUT&RUN / CUT&Tag Method Development

---

### Skene & Henikoff 2017 — CUT&RUN: targeted nuclease strategy

- **Citation:** Skene PJ, Henikoff S. An efficient targeted nuclease strategy for high-resolution mapping of DNA binding sites. eLife, 6:e21856, 2017.
- **DOI:** [10.7554/eLife.21856](https://doi.org/10.7554/eLife.21856)
- **PMID:** 28079019 | **PMC:** PMC5310842
- **Citations:** ~1,500
- **Key findings:** Introduced Cleavage Under Targets and Release Using Nuclease (CUT&RUN), which tethers protein A-Micrococcal Nuclease (pA-MNase) to an antibody bound to a target protein in situ, then activates cleavage by calcium addition. Released chromatin fragments diffuse out of the nucleus and are collected from the supernatant, eliminating the need for chromatin solubilization or immunoprecipitation. Produces extremely low background compared to ChIP-seq because only targeted fragments are released, while bulk chromatin remains in the nucleus. Requires as few as 100 cells and generates high-quality profiles for both histone marks and transcription factors with minimal sequencing depth (~5M reads vs 20-40M for ChIP-seq). The E. coli DNA carried over from pA-MNase production serves as an internal spike-in for normalization.

---

### Kaya-Okur et al. 2019 — CUT&Tag: efficient epigenomic profiling

- **Citation:** Kaya-Okur HS, Wu SJ, Codomo CA, Pledger ES, Bryson TD, Henikoff JG, Ahmad K, Henikoff S. CUT&Tag for efficient epigenomic profiling of small samples and single cells. Nature Communications, 10(1):1930, 2019.
- **DOI:** [10.1038/s41467-019-09982-5](https://doi.org/10.1038/s41467-019-09982-5)
- **PMID:** 31036827 | **PMC:** PMC6488672
- **Citations:** ~1,200
- **Key findings:** Introduced Cleavage Under Targets and Tagmentation (CUT&Tag), which replaces pA-MNase with protein A-Tn5 transposase (pA-Tn5). After antibody tethering, Tn5 simultaneously fragments and tags target chromatin with sequencing adapters. Key advantages over CUT&RUN: streamlined single-tube workflow, compatible with single-cell applications, and no separate library preparation step needed. However, CUT&Tag has higher background than CUT&RUN due to Tn5 insertion preferences in accessible chromatin. Both methods are supported by this pipeline with the same alignment and peak calling workflow, differing only in spike-in source (E. coli from Tn5 vs MNase production).

---

### Skene & Henikoff 2018 — CUT&RUN protocol optimization

- **Citation:** Skene PJ, Henikoff JG, Henikoff S. Targeted in situ genome-wide profiling with high efficiency for low cell numbers. Nature Protocols, 13(5):1006-1019, 2018.
- **DOI:** [10.1038/nprot.2018.015](https://doi.org/10.1038/nprot.2018.015)
- **PMID:** 29651053
- **Citations:** ~500
- **Key findings:** Detailed step-by-step CUT&RUN protocol with optimization guidelines for different targets (histone marks vs TFs). Established the standard experimental parameters: ConA bead binding for cell immobilization, 0°C calcium-activated cleavage for 30 minutes, fragment release at 37°C, and library preparation with NEBNext reagents. Provided troubleshooting guidance for common issues including low yield, high background, and incomplete cleavage. This protocol forms the basis for most published CUT&RUN experiments and informs the QC expectations in this pipeline.

---

## Peak Calling

---

### Meers et al. 2019 — SEACR: peak calling for CUT&RUN

- **Citation:** Meers MP, Tenenbaum D, Henikoff S. Peak calling by Sparse Enrichment Analysis for CUT&RUN chromatin profiling. Epigenetics & Chromatin, 12(1):42, 2019.
- **DOI:** [10.1186/s13072-019-0287-4](https://doi.org/10.1186/s13072-019-0287-4)
- **PMID:** 31300027 | **PMC:** PMC6626385
- **Citations:** ~800
- **Key findings:** Introduced SEACR (Sparse Enrichment Analysis for CUT&RUN), a peak caller specifically designed for the sparse, low-background signal profile of CUT&RUN data. Unlike MACS2 (which models background as a Poisson distribution), SEACR uses the empirical distribution of signal in control (IgG) or target data to identify enriched regions without parametric assumptions. Offers two modes: stringent (peaks must exceed both the global threshold and a local enrichment test) and relaxed (global threshold only). When no IgG control is available, SEACR uses the top 1% of target signal as a threshold. Benchmarking showed SEACR produces fewer false positives than MACS2 on CUT&RUN data, particularly in regions with low but genuine enrichment.

---

## Quality Control

---

### Nordin et al. 2023 — CUT&RUN suspect list

- **Citation:** Nordin A, Zambanini G, Pagella P, Bhatt DK, Bjork P, Nilsson J, Mead P, Boyle AP. The CUT&RUN suspect list of problematic regions of the genome. Genome Biology, 24:185, 2023.
- **DOI:** [10.1186/s13059-023-02960-3](https://doi.org/10.1186/s13059-023-02960-3)
- **PMID:** 37580722 | **PMC:** PMC10424377
- **Citations:** ~50
- **Key findings:** Identified genomic regions that produce artifactual signal in CUT&RUN and CUT&Tag experiments, distinct from the standard ENCODE blacklist. These "suspect" regions include areas with high MNase/Tn5 accessibility, specific repeat families, and regions prone to antibody-independent cleavage. The suspect list should be applied in addition to the ENCODE blacklist v2 (Amemiya et al. 2019) when filtering CUT&RUN/CUT&Tag peaks. Without suspect list filtering, up to 20% of called peaks may be artifacts, particularly for targets with moderate enrichment. This pipeline applies both the ENCODE blacklist and the CUT&RUN suspect list.

---

### Meers et al. 2019 — Spike-in normalization for CUT&RUN/CUT&Tag

- **Citation:** Meers MP, Bryson TD, Henikoff JG, Henikoff S. Improved CUT&RUN chromatin profiling tools. eLife, 8:e46314, 2019.
- **DOI:** [10.7554/eLife.46314](https://doi.org/10.7554/eLife.46314)
- **PMID:** 31232687 | **PMC:** PMC6632061
- **Citations:** ~400
- **Key findings:** Established the spike-in calibration framework for quantitative CUT&RUN. E. coli DNA carried over from pA-MNase production provides an internal standard: the ratio of spike-in reads between samples inversely correlates with target enrichment efficiency. Scale factors computed from spike-in counts enable quantitative comparison of signal intensity across samples and conditions. Demonstrated that spike-in normalization is essential for detecting global changes in histone modifications (e.g., drug treatments that globally increase or decrease a mark), which would be invisible with standard library-size normalization. This calibration approach is implemented in the pipeline's spike-in normalization step.

---

## Supplementary Tools (Non-CUT&RUN-Specific)

See pipeline-chipseq/references/literature.md for detailed descriptions of shared tools, and pipeline-atacseq/references/literature.md for Bowtie2.

---

### Langmead & Salzberg 2012 — Bowtie 2

- **DOI:** [10.1038/nmeth.1923](https://doi.org/10.1038/nmeth.1923) | **PMID:** 22388286 | **Citations:** ~47,300
- **CUT&RUN role:** Alignment of CUT&RUN/CUT&Tag reads to both the target genome and the E. coli spike-in genome. Bowtie2 is preferred over BWA-MEM for CUT&RUN because the short fragments typical of CUT&RUN (~150 bp mononucleosomal, <120 bp sub-nucleosomal) are well-suited to Bowtie2's alignment algorithm. Run with --very-sensitive and --dovetail flags.

---

### Zhang et al. 2008 — MACS2

- **DOI:** [10.1186/gb-2008-9-9-r137](https://doi.org/10.1186/gb-2008-9-9-r137) | **PMID:** 18798982 | **Citations:** ~7,000
- **CUT&RUN role:** Alternative peak caller for CUT&RUN data. MACS2 can be used instead of or alongside SEACR, but tends to overcall peaks due to CUT&RUN's low background. When using MACS2 on CUT&RUN data, use --nomodel and set appropriate --shift/--extsize parameters. Useful for comparison with ChIP-seq results processed with the same peak caller.

---

### Li et al. 2009 — SAMtools

- **DOI:** [10.1093/bioinformatics/btp352](https://doi.org/10.1093/bioinformatics/btp352) | **PMID:** 19505943 | **Citations:** ~53,700
- **CUT&RUN role:** BAM sorting, filtering, indexing, and alignment statistics.

---

### Broad Institute — Picard MarkDuplicates

- **URL:** [https://broadinstitute.github.io/picard/](https://broadinstitute.github.io/picard/)
- **CUT&RUN role:** PCR duplicate marking. CUT&RUN typically has lower duplication rates than ChIP-seq because it requires less input material and fewer PCR cycles. Duplication rates >20% suggest overamplification.

---

### Quinlan & Hall 2010 — BEDTools

- **DOI:** [10.1093/bioinformatics/btq033](https://doi.org/10.1093/bioinformatics/btq033) | **PMID:** 20110278 | **Citations:** ~12,000
- **CUT&RUN role:** Used for blacklist and suspect list filtering, FRiP calculation, and peak annotation.

---

### Ramírez et al. 2016 — deepTools2

- **DOI:** [10.1093/nar/gkw257](https://doi.org/10.1093/nar/gkw257) | **PMID:** 27079975 | **Citations:** ~6,100
- **CUT&RUN role:** Generates spike-in normalized signal tracks (bigWig) using bamCoverage with the --scaleFactor parameter computed from spike-in read counts. Also used for fingerprint plots and heatmaps.

---

### Amemiya et al. 2019 — ENCODE Blacklist

- **DOI:** [10.1038/s41598-019-45839-z](https://doi.org/10.1038/s41598-019-45839-z) | **PMID:** 31249361 | **Citations:** ~1,372
- **CUT&RUN role:** Blacklist v2 filtering applied alongside the CUT&RUN suspect list (Nordin 2023). Both filters are necessary: the blacklist addresses general sequencing/alignment artifacts while the suspect list addresses CUT&RUN-specific enzyme cleavage artifacts.

---

### Ewels et al. 2016 — MultiQC

- **DOI:** [10.1093/bioinformatics/btw354](https://doi.org/10.1093/bioinformatics/btw354) | **PMID:** 27312411 | **Citations:** ~6,800
- **CUT&RUN role:** Aggregates QC metrics from FastQC, Bowtie2, Picard, SEACR, and spike-in statistics into a unified HTML report.

---

### Andrews 2010 — FastQC

- **URL:** [https://www.bioinformatics.babraham.ac.uk/projects/fastqc/](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/)
- **CUT&RUN role:** Raw read quality assessment. CUT&RUN libraries typically show high-quality bases and characteristic nucleosomal fragment sizes.

---

### Martin 2011 — Cutadapt (basis for Trim Galore)

- **DOI:** [10.14806/ej.17.1.200](https://doi.org/10.14806/ej.17.1.200) | **Citations:** ~13,000
- **CUT&RUN role:** Adapter trimming. CUT&RUN sub-nucleosomal fragments frequently read through into adapters, making trimming important for accurate alignment.
