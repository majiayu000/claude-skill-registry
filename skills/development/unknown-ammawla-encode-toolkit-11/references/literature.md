# GWAS Catalog — Literature References

**Last updated:** 2026-03-07
**Purpose:** Reference catalog for the gwas-catalog skill — key papers informing genome-wide association study design, variant-to-function mapping, and integration of GWAS results with functional genomic annotations from ENCODE.

---

## Database Resources

---

### Buniello et al. 2019 — The NHGRI-EBI GWAS Catalog

- **Citation:** Buniello A, MacArthur JAL, Cerezo M, Harris LW, Hayhurst J,
  Malangone C, McMahon A, Morales J, Mountjoy E, Sollis E, et al. The NHGRI-
  EBI GWAS Catalog of published genome-wide association studies, targeted
  arrays and summary statistics 2019. Nucleic Acids Research,
  47(D1):D1005-D1012, 2019.
- **DOI:** [10.1093/nar/gky1120](https://doi.org/10.1093/nar/gky1120)
- **PMID:** 30445434 | **PMC:** PMC6323933
- **Citations:** ~3,500
- **Key findings:** Described the GWAS Catalog as the primary curated
  repository of published GWAS findings, containing >170,000 variant-trait
  associations from >4,000 publications at the time of writing. The database
  enforces standardized trait mapping using the Experimental Factor Ontology
  (EFO), genomic coordinates in GRCh38, and links to full summary statistics
  for ~8,000 studies enabling downstream fine-mapping and colocalization
  analyses. Introduced the distinction between curated associations (manually
  extracted from publications with significance threshold p < 5e-8) and
  deposited summary statistics (genome-wide results for all tested variants).
  The Catalog's REST API (ebi.ac.uk/gwas/rest/api) enables programmatic
  queries by trait, variant, gene, region, or study accession — essential for
  cross-referencing ENCODE regulatory annotations with disease-associated loci
  at scale.

---

### Sollis et al. 2023 — GWAS Catalog: expanded content and new tools

- **Citation:** Sollis E, Mosaku A, Abid A, Buniello A, Cerezo M, Gil L, Groza
  T, Gunes O, Hall P, Hayhurst J, et al. The NHGRI-EBI GWAS Catalog:
  knowledgebase and deposition resource. Nucleic Acids Research,
  51(D1):D1299-D1307, 2023.
- **DOI:** [10.1093/nar/gkac1010](https://doi.org/10.1093/nar/gkac1010)
- **PMID:** 36350656 | **PMC:** PMC9825413
- **Citations:** ~300
- **Key findings:** Updated the GWAS Catalog to >300,000 variant-trait
  associations from >6,000 publications, with full summary statistics
  available for >25,000 studies. Introduced structured ancestry reporting to
  quantify and address the historical Eurocentric bias in GWAS — over 85% of
  participants in GWAS have been of European ancestry, limiting the
  generalizability of findings. Added expanded sample metadata enabling cross-
  study meta-analysis, and integrated the PGS Catalog for polygenic risk
  scores linking GWAS discovery to clinical prediction models. The deposition
  service now allows researchers to submit summary statistics directly,
  accelerating data availability from years (waiting for journal publication)
  to weeks. These enhancements make the GWAS Catalog the most comprehensive
  single resource for connecting functional genomic annotations to disease-
  associated genetic variation.

---

## ENCODE-GWAS Integration

---

### Maurano et al. 2012 — GWAS variants are enriched in DNase I hypersensitive sites

- **Citation:** Maurano MT, Humbert R, Rynes E, Thurman RE, Haugen E, Wang H,
  Reynolds AP, Sandstrom R, Qu H, Brody J, et al. Systematic localization of
  common disease-associated variation in regulatory DNA. Science,
  337(6099):1190-1195, 2012.
- **DOI:** [10.1126/science.1222794](https://doi.org/10.1126/science.1222794)
- **PMID:** 22955828 | **PMC:** PMC3629424
- **Citations:** ~3,000
- **Key findings:** Landmark study demonstrating that ~76% of non-coding GWAS
  variants reside within or are in strong LD with DNase I hypersensitive sites
  (DHSs) from ENCODE, concentrated specifically in cell-type-specific
  regulatory elements rather than constitutive open chromatin shared across
  all cell types. Disease-associated variants show enrichment in DHSs from
  disease-relevant cell types — autoimmune variants in T cell and B cell DHSs,
  metabolic variants in hepatocyte and pancreatic islet DHSs, neuropsychiatric
  variants in brain DHSs — providing the first systematic genome-wide evidence
  that GWAS variants act through cell-type-specific gene regulation. Showed
  that the enrichment extends to variants in tight LD (r2 > 0.8) with lead
  GWAS SNPs, suggesting that causal variants can be prioritized by overlapping
  statistically fine-mapped credible sets with cell-type-specific
  accessibility maps. This paper established the ENCODE-GWAS integration
  paradigm that directly motivates the gwas-catalog skill's approach to
  annotating GWAS loci with functional genomic data.

---

### Finucane et al. 2015 — Partitioning heritability by functional annotation

- **Citation:** Finucane HK, Bulik-Sullivan B, Gusev A, Trynka G, Reshef Y,
  Loh PR, Anttila V, Xu H, Zang C, Farh K, et al. Partitioning heritability by
  functional annotation using genome-wide association summary statistics.
  Nature Genetics, 47(11):1228-1235, 2015.
- **DOI:** [10.1038/ng.3404](https://doi.org/10.1038/ng.3404)
- **PMID:** 26414678 | **PMC:** PMC4626285
- **Citations:** ~3,000
- **Key findings:** Developed stratified LD Score regression (S-LDSC) to
  partition SNP-based heritability across functional genomic annotations using
  only GWAS summary statistics, requiring no individual-level genotype data.
  Demonstrated that ~80% of heritability for complex traits is concentrated in
  ~2.5% of the genome annotated as regulatory by ENCODE and Roadmap
  Epigenomics — specifically in regions marked by DHS, H3K27ac, and H3K4me1.
  Cell-type-specific S-LDSC analyses showed that heritability enrichment
  patterns match known disease biology: autoimmune trait heritability
  concentrates in immune cell enhancers, neuropsychiatric trait heritability
  in brain-specific regulatory elements, and metabolic trait heritability in
  liver and islet enhancers. S-LDSC became the standard method for testing
  whether specific ENCODE-derived regulatory annotations (from any experiment
  type) are enriched for genetic contributions to disease risk, connecting
  chromatin profiling directly to human disease genetics.

---

### Nasser et al. 2021 — Activity-by-Contact model links enhancers to target genes

- **Citation:** Nasser J, Bergman DT, Fulco CP, Gusev A, Engreitz JM, et al.
  Genome-wide enhancer maps link risk variants to disease target genes.
  Nature, 593(7858):238-243, 2021.
- **DOI:** [10.1038/s41586-021-03446-x](https://doi.org/10.1038/s41586-021-03446-x)
- **PMID:** 33828297 | **PMC:** PMC8516355
- **Citations:** ~700
- **Key findings:** Applied the Activity-by-Contact (ABC) model to predict
  enhancer-gene connections across 131 cell types and tissues using
  ENCODE/Roadmap H3K27ac ChIP-seq and Hi-C contact frequency data. The ABC
  score for each enhancer-gene pair equals the product of enhancer activity
  (H3K27ac signal as a proxy for enhancer strength) and 3D contact frequency
  (Hi-C or a power-law distance estimate when Hi-C is unavailable), normalized
  by the total ABC score across all enhancers for that gene. Mapped 5,346
  fine-mapped GWAS variants to 2,249 unique target genes across 72 complex
  traits, finding that only 28% of variants regulate the nearest gene —
  directly challenging the widespread "nearest gene" assumption in GWAS
  interpretation. This framework demonstrates how ENCODE data products
  (H3K27ac ChIP-seq, ATAC-seq, Hi-C) can be computationally integrated to
  build variant-to-gene maps essential for translating GWAS discoveries into
  biological mechanisms.

---

## Conceptual Framework

---

### Visscher et al. 2017 — 10 Years of GWAS Discovery

- **Citation:** Visscher PM, Wray NR, Zhang Q, Sklar P, McCarthy MI, Brown MA,
  Yang J. 10 years of GWAS discovery: biology, function, and translation.
  American Journal of Human Genetics, 101(1):5-22, 2017.
- **DOI:** [10.1016/j.ajhg.2017.06.005](https://doi.org/10.1016/j.ajhg.2017.06.005)
- **PMID:** 28686856 | **PMC:** PMC5501872
- **Citations:** ~3,500
- **Key findings:** Comprehensive review of the first decade of genome-wide
  association studies, documenting >50,000 significant variant-trait
  associations for >3,000 human traits and diseases. Synthesized three
  transformative insights from GWAS: (1) common complex traits are highly
  polygenic, with most individual variants contributing tiny effects
  (explaining <0.1% of variance each); (2) the vast majority of risk variants
  (~90%) reside in non-coding regions and are likely regulatory; (3) trait
  heritability is spread broadly across the genome but concentrated in
  regulatory elements annotated by ENCODE and Roadmap. Discussed the emerging
  "omnigenic" model where a small number of core disease genes are influenced
  by thousands of peripheral genes through regulatory networks. Emphasized
  that the primary bottleneck shifted from variant discovery to functional
  interpretation — precisely the gap that ENCODE-GWAS integration addresses by
  connecting statistical associations to regulatory mechanisms.

---

### Gallagher & Chen-Plotkin 2018 — From GWAS to mechanism: functional follow-up

- **Citation:** Gallagher MD, Chen-Plotkin AS. The post-GWAS era: from
  association to function. American Journal of Human Genetics, 102(5):717-730,
  2018.
- **DOI:** [10.1016/j.ajhg.2018.04.002](https://doi.org/10.1016/j.ajhg.2018.04.002)
- **PMID:** 29727686 | **PMC:** PMC5986732
- **Citations:** ~400
- **Key findings:** Outlined the systematic workflow for functionally
  characterizing GWAS loci in the post-discovery era: (1) statistical fine-
  mapping using Bayesian methods (FINEMAP, SuSiE) to generate credible sets of
  candidate causal variants; (2) regulatory annotation using ENCODE chromatin
  maps, eQTL data, and chromatin conformation to link variants to genes; (3)
  allele-specific functional assays (MPRA, STARR-seq, luciferase reporters) to
  test whether specific variants alter regulatory element activity; and (4)
  CRISPR perturbation of candidate causal variants and enhancers to validate
  effects on target gene expression. Emphasized that overlapping a variant
  with an ENCODE ChIP-seq peak or DHS is suggestive but not sufficient
  evidence for causality — demonstrating allele-specific effects on TF binding
  affinity, chromatin accessibility, or target gene expression is required.
  This review articulates the conceptual framework underlying the gwas-catalog
  skill's multi-layer annotation approach.

---

## Post-GWAS Analysis Tools

---

### Watanabe et al. 2017 — FUMA: functional mapping and annotation of GWAS

- **Citation:** Watanabe K, Taskesen E, van Bochoven A, Posthuma D. Functional
  mapping and annotation of genetic associations with FUMA. Nature
  Communications, 8(1):1826, 2017.
- **DOI:** [10.1038/s41467-017-01261-5](https://doi.org/10.1038/s41467-017-01261-5)
- **PMID:** 29184056 | **PMC:** PMC5705698
- **Citations:** ~2,500
- **Key findings:** FUMA (Functional Mapping and Annotation of Genome-Wide
  Association Studies) is a web platform that ingests GWAS summary statistics
  and performs comprehensive post-GWAS annotation in minutes. The pipeline
  identifies independent significant SNPs (p < 5e-8, LD clumping), defines
  genomic risk loci, annotates candidate SNPs (in LD with lead SNPs) using
  ENCODE regulatory marks and GTEx eQTL associations, and maps variants to
  candidate causal genes using three strategies: positional (within gene body
  or promoter), eQTL-based (significant GTEx eQTL for a gene), and chromatin
  interaction-based (Hi-C contact with gene promoter). Integrates MAGMA gene-
  level analysis for gene set enrichment, connecting SNP-level GWAS signals to
  pathway-level biological insights. FUMA democratized post-GWAS analysis that
  previously required custom bioinformatic pipelines and extensive ENCODE/GTEx
  data processing, processing a complete GWAS in under 10 minutes.

---

### Uffelmann et al. 2021 — Genome-wide association studies: a primer

- **Citation:** Uffelmann E, Huang QQ, Munung NS, de Vries J, Okada Y, Martin
  AR, Martin HC, Lappalainen T, Posthuma D. Genome-wide association studies.
  Nature Reviews Methods Primers, 1(1):59, 2021.
- **DOI:** [10.1038/s43586-021-00056-9](https://doi.org/10.1038/s43586-021-00056-9)
- **PMID:** 37325440 | **PMC:** PMC10272025
- **Citations:** ~800
- **Key findings:** Authoritative primer covering GWAS methodology from
  experimental design through statistical analysis to functional
  interpretation and clinical translation. Detailed the core statistical
  framework: association testing via logistic or linear regression with
  additive genetic models, genome-wide significance threshold of p < 5e-8
  (Bonferroni correction for ~1 million independent tests), population
  stratification control using principal component analysis or linear mixed
  models, and fixed-effect meta-analysis for combining results across cohorts.
  Addressed critical methodological limitations including Winner's curse
  (systematic inflation of effect sizes at discovery), the population
  diversity gap and its consequences for portability of GWAS findings, and the
  fundamental challenge of fine-mapping causal variants from haplotype blocks
  inherited in linkage disequilibrium. Emphasized that functional annotation
  using ENCODE regulatory maps and GTEx expression data is now considered an
  integral component of GWAS analysis rather than an optional post-hoc
  exercise.

---
