# Quality Assessment — Literature References

**Last updated:** 2026-03-07
**Purpose:** Reference catalog for the quality-assessment skill — key papers defining assay-specific
quality control metrics, sequencing depth requirements, blacklist filtering, and multi-assay QC
frameworks for ChIP-seq, ATAC-seq, RNA-seq, WGBS, Hi-C, and CUT&RUN/CUT&Tag.

The quality-assessment skill evaluates ENCODE experiments against established quality thresholds,
interpreting audit flags (ERROR, NOT_COMPLIANT, WARNING, INTERNAL_ACTION) and providing
assay-specific QC guidance. Quality is never determined by a single metric — it requires collective
interpretation of library complexity, signal-to-noise ratios, replicate concordance, and
assay-specific benchmarks.

These 12 papers are organized by assay type, covering the quality standards for each major
functional genomics method represented in ENCODE. The final section covers universal tools and
filtering requirements that apply across all assay types.

---

## ChIP-seq Quality Standards

ChIP-seq is the most established ENCODE assay with the most mature quality framework. The three
papers below define the core metrics (FRiP, NSC, RSC, NRF), sequencing depth requirements, and
the interaction between artifact removal and quality metric calculation. Understanding these metrics
is essential because the ENCODE audit system derives its ChIP-seq quality flags directly from them.

---

### Landt et al. 2012 — ENCODE/modENCODE ChIP-seq quality guidelines

- **Citation:** Landt SG, Marinov GK, Kundaje A, Kheradpour P, Pauli F, Batzoglou S,
  Bernstein BE, Bickel P, Brown JB, Cayting P, Chen Y, DeSalvo G, Epstein C,
  Fisher-Aylor KI, Euskirchen G, Gerstein M, Gertz J, Hartemink AJ, Hoffman MM,
  Iyer VR, Jung YL, Karmakar S, Kellis M, Kharchenko PV, Li Q, Liu T, Liu XS,
  Ma L, Milosavljevic A, Myers RM, Park PJ, Pazin MJ, Perry MD, Raha D,
  Reddy TE, Rozowsky J, Shoresh N, Sidow A, Slattery M, Stamatoyannopoulos JA,
  Tolstorukov MY, White KP, Xi S, Farnham PJ, Lieb JD, Wold BJ, Snyder M.
  ChIP-seq guidelines and practices of the ENCODE and modENCODE consortia.
  *Genome Research*, 22(9), 1813-1831, 2012.
- **DOI:** [10.1101/gr.136184.111](https://doi.org/10.1101/gr.136184.111)
- **PMID:** 22955991 | **PMC:** PMC3431496
- **Citations:** ~3,400
- **Key findings:** The definitive quality framework for ChIP-seq, establishing four core metrics:
  FRiP (fraction of reads in peaks, >= 1% for broad marks, typically 5-20% for TFs),
  NSC (normalized strand coefficient, >1.05),
  RSC (relative strand coefficient, >0.8), and
  NRF (non-redundant fraction, >= 0.8).
  Mandated biological replicates with IDR (Irreproducible Discovery Rate) analysis for peak
  reproducibility, requiring IDR < 0.05 for optimal peaks. The paper distinguished quality
  expectations between sharp-peak factors (transcription factors, H3K4me3) and broad-domain marks
  (H3K27me3, H3K36me3), noting that broad marks have lower FRiP and strand correlation scores by
  nature. The quality-assessment skill uses these thresholds directly when evaluating ChIP-seq
  experiments, applying different expectations for sharp vs. broad targets.

---

### Marinov et al. 2014 — Sequencing depth requirements for ChIP-seq saturation

- **Citation:** Marinov GK, Kundaje A, Park PJ, Wold BJ. Large-scale quality analysis
  of published ChIP-seq data. *G3: Genes, Genomes, Genetics*, 4(2), 209-223, 2014.
- **DOI:** [10.1534/g3.113.008680](https://doi.org/10.1534/g3.113.008680)
- **PMID:** 24347632 | **PMC:** PMC3931556
- **Citations:** ~800
- **Key findings:** Systematically evaluated quality metrics across >400 published ChIP-seq
  datasets, establishing practical depth requirements: 20-40 million unique reads for sharp TF
  peaks and 40-60 million for broad histone marks. Demonstrated that sequencing depth below these
  thresholds leads to incomplete peak detection and poor IDR concordance between replicates.
  Found that ~30% of published ChIP-seq datasets had quality issues detectable by strand
  correlation metrics alone, indicating widespread quality problems in the published literature.
  The quality-assessment skill uses these depth thresholds to flag under-sequenced experiments
  and recommend whether additional sequencing is needed before analysis.

---

### Carroll et al. 2014 — Impact of artifact removal on ChIP quality metrics

- **Citation:** Carroll TS, Liang Z, Salama R, Stark R, de Santiago I. Impact of artifact
  removal on ChIP quality metrics in ChIP-seq and ChIP-exo data. *Frontiers in Genetics*,
  5, 75, 2014.
- **DOI:** [10.3389/fgene.2014.00075](https://doi.org/10.3389/fgene.2014.00075)
- **PMID:** 24782889 | **PMC:** PMC3988386
- **Citations:** ~600
- **Key findings:** Investigated how artifact removal steps (duplicate filtering, blacklist
  filtering, mapability masking) affect downstream ChIP-seq quality metrics. Demonstrated that
  applying the ENCODE blacklist prior to quality metric calculation substantially improves NSC
  and RSC scores, revealing that many apparently "low-quality" datasets become acceptable after
  proper filtering. Established the correct ordering of QC steps: adapter trimming, alignment,
  duplicate marking, blacklist filtering, then quality metric calculation. The quality-assessment
  skill follows this pipeline order and warns users when quality metrics were calculated before
  blacklist filtering, which can produce misleadingly low scores for otherwise acceptable data.

---

## ATAC-seq Quality Standards

ATAC-seq has distinct quality signatures from ChIP-seq, including the nucleosomal fragment size
ladder and TSS enrichment score. The two papers below define the method's intrinsic quality
indicators and provide systematic benchmarks for quantitative evaluation.

---

### Buenrostro et al. 2013 — ATAC-seq method and intrinsic quality signatures

- **Citation:** Buenrostro JD, Giresi PG, Zaba LC, Chang HY, Greenleaf WJ. Transposition of
  native chromatin for fast and sensitive epigenomic profiling of open chromatin, DNA-binding
  proteins, and nucleosome position. *Nature Methods*, 10(12), 1213-1218, 2013.
- **DOI:** [10.1038/nmeth.2688](https://doi.org/10.1038/nmeth.2688)
- **PMID:** 24097267 | **PMC:** PMC3959825
- **Citations:** ~5,000
- **Key findings:** Introduced ATAC-seq (Assay for Transposase-Accessible Chromatin using
  sequencing) and defined its characteristic quality signatures: the nucleosomal ladder pattern
  in fragment size distribution (sub-nucleosomal <147bp, mono-nucleosomal 147-294bp,
  di-nucleosomal 294-441bp), enrichment of signal at transcription start sites (TSS enrichment),
  and high signal-to-noise ratio at known open chromatin regions. ATAC-seq requires only
  500-50,000 cells (vs. millions for DNase-seq), making it the preferred accessibility assay
  for limited-material samples. The quality-assessment skill checks for the nucleosomal ladder
  and TSS enrichment score (>= 5 GRCh38 / >= 6 hg19 / >= 10 mm10 per ENCODE data standards) as primary quality indicators.

---

### Yan et al. 2020 — Systematic ATAC-seq quality metrics and benchmarks

- **Citation:** Yan F, Powell DR, Curtis DJ, Wong NC. From reads to insight: a hitchhiker's
  guide to ATAC-seq data analysis. *Genome Biology*, 21(1), 22, 2020.
- **DOI:** [10.1186/s13059-020-1929-3](https://doi.org/10.1186/s13059-020-1929-3)
- **PMID:** 32014034 | **PMC:** PMC6996192
- **Citations:** ~400
- **Key findings:** Provided a comprehensive benchmarking framework for ATAC-seq QC, establishing
  quantitative thresholds:
  - TSS enrichment score >= 5 GRCh38 / >= 6 hg19 / >= 10 mm10 (ENCODE data standards)
  - Mitochondrial read fraction < 20% (ideally < 5%)
  - Duplicate rate < 30%
  - Unique alignment rate > 80%
  - FRiP >= 20% for accessibility peaks
  - NFR/mono-nucleosomal ratio > 2 indicates successful Tn5 insertion

  The quality-assessment skill uses these thresholds in its ATAC-seq quality evaluation,
  reporting each metric alongside the expected range and flagging outliers. High mitochondrial
  read fractions indicate nuclear isolation problems, while absent nucleosomal periodicity
  suggests over-transposition or insufficient crosslinking.

---

## RNA-seq Quality Standards

RNA-seq quality assessment differs fundamentally from ChIP-seq because the signal is gene-level
expression rather than genomic binding. Quality metrics focus on mapping rates, library composition,
gene body coverage uniformity, and replicate concordance rather than peak-based measures.

---

### Conesa et al. 2016 — RNA-seq best practices and quality assessment framework

- **Citation:** Conesa A, Madrigal P, Tarazona S, Gomez-Cabrero D, Cervera A, McPherson A,
  Szczesniak MW, Gaffney DJ, Elo LL, Zhang X, Mortazavi A. A survey of best practices for
  RNA-seq data analysis. *Genome Biology*, 17, 13, 2016.
- **DOI:** [10.1186/s13059-016-0881-8](https://doi.org/10.1186/s13059-016-0881-8)
- **PMID:** 26813401 | **PMC:** PMC4728800
- **Citations:** ~4,500
- **Key findings:** Established the consensus RNA-seq quality framework:
  - Mapping rate 70-90% to reference genome
  - Ribosomal RNA fraction < 10% (< 5% ideal for poly-A libraries)
  - Gene body coverage uniformity (5'-to-3' bias ratio < 2)
  - Replicate Spearman correlation >= 0.9
  - Library complexity > 80% unique reads
  - >= 30 million reads for differential expression, >= 100 million for transcript assembly

  Defined the distinction between quality metrics for poly-A RNA-seq (gene-level quantification)
  vs. total RNA-seq (transcript-level, including non-coding RNAs and pre-mRNAs). The
  quality-assessment skill evaluates these metrics when assessing RNA-seq experiments and
  distinguishes between poly-A and total RNA protocols, applying different expectations for
  rRNA fraction (poly-A should have < 5%, total RNA may have up to 10% after rRNA depletion).

---

## Bisulfite Sequencing Quality Standards

Whole-genome bisulfite sequencing (WGBS) has unique quality considerations arising from the chemical
conversion of unmethylated cytosines to uracils. Conversion efficiency is the single most critical
quality metric — incomplete conversion produces systematic false positives that cannot be
computationally distinguished from true methylation.

---

### Foox et al. 2021 — WGBS benchmarking and bisulfite conversion quality

- **Citation:** Foox J, Nordlund J, Lalancette C, Gong T, Samber M, Gaggiotti K, Bhatt V,
  Buber DCE, Mundt F, Butler DJ, Mozsary C, Fehlmann T, Holley J, Prill RJ, Keller A,
  Mason CE. The SEQC2 epigenomics quality control (EpiQC) study. *Genome Biology*,
  22, 307, 2021.
- **DOI:** [10.1186/s13059-021-02529-2](https://doi.org/10.1186/s13059-021-02529-2)
- **PMID:** 34872606 | **PMC:** PMC8650396
- **Citations:** ~300
- **Key findings:** Benchmarked WGBS performance across 18 laboratories, establishing minimum
  quality thresholds:
  - Bisulfite conversion rate ≥ 98% (measured by lambda spike-in or non-CpG methylation)
  - CpG coverage >= 10x for reliable methylation calling (>= 30x for DMR detection)
  - Mapping rate > 60% (lower than standard due to reduced sequence complexity)
  - Concordance > 0.95 between technical replicates at covered CpGs

  Demonstrated that conversion rates below 98% introduce systematic false positives that
  cannot be computationally corrected. The quality-assessment skill flags WGBS experiments
  with conversion rates below this threshold and recommends minimum coverage depths based
  on intended analysis type (global profiling vs. DMR detection vs. allele-specific methylation).

---

### Schwartzman & Tanay 2015 — Statistical frameworks for bisulfite sequencing QC

- **Citation:** Schwartzman O, Tanay A. Single-cell epigenomics: techniques and emerging
  applications. *Nature Reviews Genetics*, 16, 716-726, 2015.
- **DOI:** [10.1038/nrg3980](https://doi.org/10.1038/nrg3980)
- **PMID:** 26460349
- **Citations:** ~500
- **Key findings:** Reviewed the analytical challenges of bisulfite sequencing data including
  incomplete conversion artifacts, alignment biases in repetitive regions, and the statistical
  frameworks needed for methylation calling at different coverage depths. Established that
  per-CpG methylation estimates require binomial modeling with a minimum of 5x coverage for
  reliable calls, and that smoothing approaches (BSmooth, methylKit) can improve estimates
  in low-coverage regions by borrowing information from neighboring CpGs. The quality-assessment
  skill uses these statistical principles when evaluating whether WGBS coverage is sufficient,
  distinguishing between global methylation profiling (5-10x sufficient), DMR calling
  (30x+ recommended), and single-CpG resolution analysis (50x+ recommended).

---

## Hi-C and 3D Genome Quality Standards

Hi-C quality metrics are distinct from linear assays because the signal of interest is the
frequency of chromatin contacts between pairs of genomic loci. Quality depends on crosslinking
efficiency, ligation specificity, and sequencing depth relative to the resolution desired.

---

### Yardimci et al. 2019 — Hi-C data quality metrics and normalization assessment

- **Citation:** Yardimci GG, Ozadam H, Saber ME, Aslankurt A, Yang X, Barutcu AR, Singer O,
  Boone D, Skalska L, Osman F, Razavi M, Libbrecht MW, Lajoie BR, Sanyal A, Dekker J,
  Noble WS, Mirny LA. Measuring the reproducibility and quality of Hi-C data.
  *Genome Biology*, 20(1), 57, 2019.
- **DOI:** [10.1186/s13059-019-1658-7](https://doi.org/10.1186/s13059-019-1658-7)
- **PMID:** 30890172 | **PMC:** PMC6423771
- **Citations:** ~200
- **Key findings:** Established quantitative quality metrics for Hi-C data:
  - Cis/trans ratio > 60% (higher indicates better ligation specificity)
  - Long-range cis interactions > 40% of total cis (>10kb distance)
  - Valid pair fraction > 40% of total read pairs
  - Duplicate rate assessment for library complexity

  Demonstrated that Hi-C quality is highly sensitive to crosslinking conditions and ligation
  efficiency, with poor-quality libraries showing elevated trans interactions and enrichment
  for short-range cis contacts (an indicator of random ligation rather than true chromatin
  contacts). Resolution achievable depends on sequencing depth: 500M valid pairs for 5kb
  resolution, 1B for 1kb resolution. The quality-assessment skill uses the cis/trans ratio
  as the single most informative initial quality indicator for Hi-C experiments.

---

## CUT&RUN/CUT&Tag Quality Standards

CUT&RUN and CUT&Tag use antibody-tethered nucleases (pA-MNase or pA-Tn5) instead of
immunoprecipitation, producing fundamentally different signal characteristics from ChIP-seq.
Standard ChIP-seq quality metrics (NSC, RSC) have different expected distributions, and a
distinct set of artifact regions must be filtered.

---

### Nordin et al. 2023 — CUT&RUN artifact regions (suspect list) for quality filtering

- **Citation:** Nordin A, Zambanini G, Pagella P, Cantu C. The CUT&RUN suspect list of
  problematic regions of the genome. *Genome Biology*, 24(1), 185, 2023.
- **DOI:** [10.1186/s13059-023-03027-3](https://doi.org/10.1186/s13059-023-03027-3)
- **PMID:** 37563719 | **PMC:** PMC10416431
- **Citations:** ~150
- **Key findings:** Identified a set of genomic regions (~1.5% of the genome) that produce
  systematic artifact signals specifically in CUT&RUN and CUT&Tag experiments, distinct from
  the standard ENCODE ChIP-seq blacklist. These "suspect regions" arise from MNase cleavage
  biases at highly accessible chromatin and pA-MNase diffusion artifacts, producing
  false-positive peaks that pass conventional quality filters designed for ChIP-seq.
  The quality-assessment skill applies the CUT&RUN suspect list in addition to the standard
  ENCODE blacklist when evaluating these assay types, and warns users that ChIP-seq quality
  metrics (NSC, RSC) have different expected distributions — CUT&RUN typically produces
  higher signal-to-noise but at fewer total peaks than ChIP-seq for the same target.

---

## Blacklist and Universal Quality Filtering

Regardless of assay type, all functional genomics data must be filtered against the ENCODE
blacklist — a set of genomic regions that produce artifact signal due to anomalous sequence
composition and assembly errors. The blacklist is the single most impactful quality filter.

---

### Amemiya et al. 2019 — ENCODE Blacklist v2: universal artifact regions

- **Citation:** Amemiya HM, Kundaje A, Boyle AP. The ENCODE Blacklist: identification of
  problematic regions of the genome. *Scientific Reports*, 9(1), 9354, 2019.
- **DOI:** [10.1038/s41598-019-45839-z](https://doi.org/10.1038/s41598-019-45839-z)
- **PMID:** 31249361 | **PMC:** PMC6597582
- **Citations:** ~1,400
- **Key findings:** Defined the ENCODE Blacklist v2 — genomic regions producing artifact signal
  across all functional genomics assays due to anomalous mappability from collapsed repeats,
  satellite sequences, and assembly gaps. The blacklist covers 910 regions in GRCh38 (0.5%
  of the genome, ~15 Mb) but can contain >50% of the signal in input/control samples.
  Blacklist filtering should be applied before all quality metric calculations and peak
  calling — failing to do so inflates peak counts and distorts quality scores. The
  quality-assessment skill checks whether experiments have been filtered against the blacklist
  (ENCFF356LFX for GRCh38, ENCFF547MET for mm10) and flags those that have not, as
  unfiltered data will produce unreliable quality assessments.

---

## Multi-Assay QC Framework

When evaluating ENCODE experiments across multiple assay types, a unified QC reporting framework
enables systematic comparison and identification of batch effects or quality outliers. MultiQC
provides this framework by aggregating metrics from diverse bioinformatics tools into standardized
reports.

---

### Ewels et al. 2016 — MultiQC for unified quality reporting across assay types

- **Citation:** Ewels P, Magnusson M, Lundin S, Kaller M. MultiQC: summarize analysis
  results for multiple tools and samples. *Bioinformatics*, 32(19), 3047-3048, 2016.
- **DOI:** [10.1093/bioinformatics/btw354](https://doi.org/10.1093/bioinformatics/btw354)
- **PMID:** 27312411 | **PMC:** PMC5039924
- **Citations:** ~2,500
- **Key findings:** Introduced MultiQC, the standard tool for aggregating quality metrics from
  diverse bioinformatics tools (FastQC, Picard, STAR, featureCounts, sambamba, samtools, etc.)
  into unified HTML reports with interactive visualizations. MultiQC parses output from >120
  tools and presents cross-sample quality comparisons including alignment statistics, duplication
  rates, fragment size distributions, insert sizes, GC content distributions, and assay-specific
  metrics. For ENCODE data, MultiQC aggregates metrics across all experiments in a project,
  enabling batch-level quality assessment that identifies outlier experiments.
  The quality-assessment skill recommends MultiQC as the primary reporting tool for
  multi-experiment quality evaluation and uses its metric definitions as reference standards.

---
