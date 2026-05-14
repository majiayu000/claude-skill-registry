# Peak Annotation — Literature References

**Last updated:** 2026-03-07
**Purpose:** Reference catalog for the peak-annotation skill — key papers informing genomic region annotation, functional enrichment, and differential binding analysis of ChIP-seq and ATAC-seq peaks.

---

## Annotation Tools

---

### Yu et al. 2015 — ChIPseeker: versatile peak annotation and visualization

- **Citation:** Yu G, Wang LG, He QY. ChIPseeker: an R/Bioconductor package
  for ChIP peak annotation, comparison and visualization. Bioinformatics,
  31(14):2382-2383, 2015.
- **DOI:** [10.1093/bioinformatics/btv145](https://doi.org/10.1093/bioinformat
  ics/btv145)
- **PMID:** 25765347
- **Citations:** ~3,200
- **Key findings:** ChIPseeker annotates peaks to genomic features (promoter,
  5'UTR, 3'UTR, exon, intron, downstream, intergenic) using a nearest-TSS
  approach with configurable promoter windows (default -3kb to +3kb). The
  package generates publication-quality visualizations including TSS-relative
  coverage profiles showing peak density relative to gene starts, pie charts
  of genomic feature distribution for quick characterization, and Venn
  diagrams for multi-sample peak overlap. Uniquely among annotation tools,
  ChIPseeker integrates with the clusterProfiler ecosystem for functional
  enrichment of peak-associated genes via GO, KEGG, Reactome, and Disease
  Ontology pathways. ChIPseeker became the standard R/Bioconductor tool
  because it handles annotation, visualization, and downstream enrichment in a
  unified workflow supporting all standard peak formats (narrowPeak,
  broadPeak, BED, GFF).

---

### McLean et al. 2010 — GREAT: regulatory domain-based functional annotation

- **Citation:** McLean CY, Bristor D, Hiller M, Clarke SL, Schaar BT, Lowe CB,
  Wenger AM, Bejerano G. GREAT improves functional interpretation of cis-
  regulatory regions. Nature Biotechnology, 28(5):495-501, 2010.
- **DOI:** [10.1038/nbt.1630](https://doi.org/10.1038/nbt.1630)
- **PMID:** 20436461 | **PMC:** PMC4840234
- **Citations:** ~2,800
- **Key findings:** Introduced GREAT (Genomic Regions Enrichment of
  Annotations Tool), which assigns biological meaning to genomic regions by
  associating each region with genes using a regulatory domain model rather
  than simple nearest-gene assignment. GREAT extends gene regulatory domains
  up to 1 Mb from the TSS (limited by the regulatory domain of the neighboring
  gene), capturing distal enhancer-gene associations that proximity-based
  methods systematically miss. Uses dual statistical evaluation: a binomial
  test assessing whether the fraction of the genome covered by regulatory
  domains of a gene set exceeds expectation, and a hypergeometric test
  assessing gene count enrichment. This approach was transformative for
  interpreting peaks from enhancer-associated marks (H3K4me1, H3K27ac, p300)
  where the nearest gene is often NOT the regulated target — GREAT showed that
  ~40% of enhancer peaks regulate non-nearest genes.

---

### Zhu et al. 2010 — ChIPpeakAnno: peak annotation and cross-experiment comparison

- **Citation:** Zhu LJ, Gazin C, Lawson ND, Pages H, Lin SM, Lapointe DS,
  Green MR. ChIPpeakAnno: a Bioconductor package to annotate ChIP-seq and
  ChIP-chip data. BMC Bioinformatics, 11:237, 2010.
- **DOI:** [10.1186/1471-2105-11-237](https://doi.org/10.1186/1471-2105-11-237)
- **PMID:** 20459804 | **PMC:** PMC2881054
- **Citations:** ~1,800
- **Key findings:** ChIPpeakAnno was one of the first dedicated Bioconductor
  packages for ChIP-seq peak annotation, providing nearest-feature annotation
  with configurable distance thresholds, overlapping feature identification
  with multiple assignment strategies (nearest TSS, nearest bidirectional,
  overlapping feature body), and Venn diagram visualization for multi-
  experiment peak overlap. Introduced a permutation-based approach to test
  whether observed peak overlaps between two experiments exceed random
  expectation, accounting for peak widths and chromosomal distribution —
  critical for determining if two TFs co-bind more than expected by chance.
  The package also implements batch annotation against Ensembl and UCSC gene
  models, with support for custom annotation databases. ChIPpeakAnno's early
  adoption (2010) established the reference implementation for basic peak
  annotation in R, though ChIPseeker later surpassed it in visualization and
  enrichment integration.

---

## Enrichment Analysis

---

### Sheffield & Bock 2016 — LOLA: genomic region set enrichment analysis

- **Citation:** Sheffield NC, Bock C. LOLA: enrichment analysis for genomic
  region sets and regulatory elements in R and Bioconductor. Bioinformatics,
  32(4):587-589, 2016.
- **DOI:** [10.1093/bioinformatics/btv612](https://doi.org/10.1093/bioinformat
  ics/btv612)
- **PMID:** 26508757 | **PMC:** PMC4743627
- **Citations:** ~600
- **Key findings:** LOLA (Locus OverLap Analysis) tests enrichment of a query
  genomic region set against a database of reference region sets using
  Fisher's exact test with proper universe specification. Unlike gene-based
  enrichment methods (GO/KEGG), LOLA operates directly on genomic coordinates,
  enabling comparison of peaks against ENCODE ChIP-seq datasets, Roadmap
  Epigenomics chromatin states, CODEX regulatory elements, CpG islands, repeat
  elements, and custom databases. The choice of background universe
  dramatically affects results — using all called peaks vs. accessible
  chromatin vs. full genome as the universe changes which enrichments appear
  significant. LOLA was the first tool to systematically address this
  confound, requiring explicit universe definition and providing diagnostic
  plots for universe sensitivity. This fills the gap between single-feature
  annotation (ChIPseeker assigns peaks to genes) and pathway analysis (GREAT
  tests gene set enrichment) by enabling direct region-to-region enrichment
  testing across hundreds of regulatory datasets simultaneously.

---

## Genomic Interval Infrastructure

---

### Quinlan & Hall 2010 — BEDTools: genomic interval arithmetic

- **Citation:** Quinlan AR, Hall IM. BEDTools: a flexible suite of utilities
  for comparing genomic features. Bioinformatics, 26(6):841-842, 2010.
- **DOI:** [10.1093/bioinformatics/btq033](https://doi.org/10.1093/bioinformat
  ics/btq033)
- **PMID:** 20110278 | **PMC:** PMC2832824
- **Citations:** ~8,000
- **Key findings:** BEDTools provides the fundamental genomic interval
  operations (intersect, merge, subtract, closest, window, coverage,
  complement, shuffle) that underpin virtually all peak annotation workflows.
  The intersect command with configurable overlap fractions (-f, -r for
  reciprocal) enables assignment of peaks to annotated genomic features
  including gene bodies, promoters, enhancers, CpG islands, and repeat
  elements. The closest command with distance reporting (-d flag) enables
  distance-to-TSS calculations central to peak characterization. BEDTools'
  streaming architecture processes arbitrarily large files without loading
  them into memory, and its UNIX-pipe compatibility enables complex multi-step
  annotation pipelines composable from simple operations. It remains the
  foundational layer upon which higher-level tools (ChIPseeker, GREAT, HOMER
  annotate) build their annotation functionality, handling the coordinate
  arithmetic while the wrapper tools add statistical testing and
  visualization.

---

### Lawrence et al. 2013 — GenomicRanges: infrastructure for genomic interval operations in R

- **Citation:** Lawrence M, Huber W, Pages H, Aboyoun P, Carlson M, Gentleman
  R, Morgan MT, Carey VJ. Software for computing and annotating genomic
  ranges. PLoS Computational Biology, 9(8):e1003118, 2013.
- **DOI:** [10.1371/journal.pcbi.1003118](https://doi.org/10.1371/journal.pcbi
  .1003118)
- **PMID:** 23950696 | **PMC:** PMC3738458
- **Citations:** ~2,500
- **Key findings:** GenomicRanges provides the core data structure (GRanges)
  for representing and manipulating genomic intervals in R/Bioconductor,
  serving as the foundation for ChIPseeker, DiffBind, ChIPpeakAnno, and nearly
  all R-based peak analysis tools. GRanges objects store chromosome, start,
  end, strand, and arbitrary metadata columns with efficient set operations
  (union, intersect, setdiff) and overlap queries implemented using interval
  trees for O(n log n) performance. The findOverlaps function enables peak-to-
  annotation mapping with configurable minimum overlap, maximum gap tolerance,
  and strand-awareness. The countOverlaps function provides peak-in-feature
  counting essential for enrichment analyses and differential binding. This
  infrastructure standardized genomic data representation across the entire
  Bioconductor ecosystem, enabling seamless interoperability between dozens of
  packages for peak analysis, variant annotation, and expression
  quantification.

---

## Differential Binding Analysis

---

### Ross-Innes et al. 2012 — DiffBind applied to differential estrogen receptor binding

- **Citation:** Ross-Innes CS, Stark R, Teschendorff AE, Holmes KA, Ali HR,
  Dunning MJ, Brown GD, Gojis O, Ellis IO, Green AR, et al. Differential
  oestrogen receptor binding is associated with clinical outcome in breast
  cancer. Nature, 481(7381):389-393, 2012.
- **DOI:** [10.1038/nature10730](https://doi.org/10.1038/nature10730)
- **PMID:** 22217937 | **PMC:** PMC3272464
- **Citations:** ~2,500
- **Key findings:** Applied the DiffBind framework to identify differentially
  bound estrogen receptor (ER) sites between breast tumors with good and poor
  clinical outcomes, discovering 1,302 differential ER binding sites that
  predict metastasis-free survival. Demonstrated that differential binding
  analysis of ChIP-seq data can identify clinically relevant regulatory
  differences between patient groups, analogous to how differential expression
  analysis of RNA-seq identifies disease-relevant genes. Read counts within
  consensus peak regions were used as input to DESeq2/edgeR for statistical
  testing with size factor normalization, establishing the count-based
  approach to differential binding that is now standard. This landmark study
  validated differential ChIP-seq as a discovery tool for biomedically
  significant regulatory variation and showed that TF binding differences
  between tumors carry prognostic information beyond what gene expression
  alone provides.

---

### Stark & Brown 2011 — DiffBind: differential binding analysis of ChIP-Seq peak data

- **Citation:** Stark R, Brown GD. DiffBind: differential binding analysis of
  ChIP-Seq peak data. Bioconductor package version, 2011.
- **DOI:** [10.18129/B9.bioc.DiffBind](https://doi.org/10.18129/B9.bioc.DiffBind)
- **PMID:** N/A | **PMC:** N/A
- **Citations:** ~1,500
- **Key findings:** DiffBind provides a complete computational framework for
  differential binding analysis with four stages: (1) consensus peakset
  construction by merging peaks present in a minimum number of replicates,
  reducing false positives from individual samples; (2) read count matrix
  generation by counting reads in consensus peaks across all samples; (3)
  normalization using library size, reads-in-peaks (RiP), TMM, or spike-in
  methods; and (4) statistical testing via DESeq2 or edgeR for identifying
  significantly different peaks between conditions. The choice of
  normalization is critical because ChIP-seq signal can vary globally between
  conditions (e.g., a drug that reduces total TF binding), and standard
  library-size normalization assumes most peaks are unchanged. DiffBind's
  occupancy analysis (presence/absence of peaks across samples) addresses a
  different biological question from affinity analysis (quantitative signal
  differences): whether a factor binds at all in a condition vs. whether
  binding strength changes.

---
