# Cross-Reference — Literature References

**Last updated:** 2026-03-07
**Purpose:** Reference catalog for the cross-reference skill — key papers for the external
databases (GTEx, ClinVar, GWAS Catalog, GEO, JASPAR, gnomAD, Ensembl) that ENCODE data is
linked to for multi-database integrative analysis.

The cross-reference skill connects tracked ENCODE experiments to external resources: PubMed for
literature, GEO for complementary datasets, GTEx for tissue expression, ClinVar for clinical
variant interpretation, GWAS Catalog for disease associations, JASPAR for TF motifs, gnomAD for
population genetics, and Ensembl for genome annotation. Each database brings a distinct layer of
biological context to ENCODE functional genomic data.

The 7 papers below each describe one of the major external databases. They are organized by the
type of biological context they provide: expression (GTEx), clinical variants (ClinVar), disease
associations (GWAS Catalog), complementary datasets (GEO), TF motifs (JASPAR), population
genetics (gnomAD), and genome annotation (Ensembl).

---

## Expression and Tissue Context

Understanding which genes are expressed in which tissues provides essential context for ENCODE
regulatory elements. An enhancer active in a tissue is only meaningful if its target genes are
expressed there.

---

### GTEx Consortium 2020 — Tissue-specific expression atlas

- **Citation:** The GTEx Consortium. The GTEx Consortium atlas of genetic regulatory effects
  across human tissues. *Science*, 369(6509), 1318-1330, 2020.
- **DOI:** [10.1126/science.aaz1776](https://doi.org/10.1126/science.aaz1776)
- **PMID:** 32913098 | **PMC:** PMC7737656
- **Citations:** ~4,000
- **Key findings:** Definitive atlas of gene expression and eQTLs across 54 human tissues from
  948 donors. GTEx v8 mapped 4.1 million cis-eQTL variant-gene pairs showing tissue-specific
  regulatory patterns. Cross-referencing ENCODE cCREs with GTEx eQTLs identifies which
  regulatory elements drive tissue-specific expression:
  - Enhancer in islets (ENCODE) -> target gene expression (GTEx) -> diabetes variant (GWAS)
  - Also provides splicing QTLs (sQTLs) for regulatory variants affecting RNA processing

  The cross-reference skill uses GTEx for expression context in tracked experiments.

---

## Clinical Variant Interpretation

Connecting ENCODE regulatory elements to clinically significant variants reveals regulatory
mechanisms of disease — variants may be pathogenic because they disrupt regulatory elements,
not proteins.

---

### Landrum et al. 2018 — ClinVar clinical variant database

- **Citation:** Landrum MJ, Lee JM, Benson M, Brown GR, Chao C, et al. ClinVar: improving
  access to variant interpretations and supporting evidence. *Nucleic Acids Research*,
  46(D1), D1062-D1067, 2018.
- **DOI:** [10.1093/nar/gkx1153](https://doi.org/10.1093/nar/gkx1153)
- **PMID:** 29165669 | **PMC:** PMC5753237
- **Citations:** ~2,000
- **Key findings:** ClinVar aggregates variant-disease associations with ACMG/AMP five-tier
  classification (pathogenic, likely pathogenic, VUS, likely benign, benign) from >1,400
  laboratories. Contains >1.5 million interpretations. Cross-referencing with ENCODE:
  - Pathogenic variant in CTCF site (ClinVar) + cCRE overlap (ENCODE) = regulatory mechanism
  - Review_status field indicates interpretation confidence

  The cross-reference skill surfaces review_status to help users assess confidence:
  no assertion, single submitter, multiple submitters, expert panel, practice guideline.

---

## Disease-Associated Variants

Over 90% of GWAS hits fall in non-coding regions, making ENCODE's regulatory element catalog
essential for functional interpretation.

---

### Buniello et al. 2019 — GWAS Catalog for disease variant enrichment

- **Citation:** Buniello A, MacArthur JAL, Cerezo M, Harris LW, et al. The NHGRI-EBI GWAS
  Catalog of published genome-wide association studies, targeted arrays and summary
  statistics 2019. *Nucleic Acids Research*, 47(D1), D1005-D1012, 2019.
- **DOI:** [10.1093/nar/gky1120](https://doi.org/10.1093/nar/gky1120)
- **PMID:** 30445434 | **PMC:** PMC6323933
- **Citations:** ~3,500
- **Key findings:** Curates >300,000 variant-trait associations from >6,000 GWAS studies with
  standardized effect sizes, p-values, and ancestry information. The cross-reference skill
  enables:
  - Direct overlap of GWAS lead SNPs + LD proxies with ENCODE cCREs
  - Cell-type-specific enrichment analysis (which biosamples show variant enrichment)
  - Full summary statistics for genome-wide enrichment (LD score regression, GARFIELD)

  This operationalizes the Maurano et al. 2012 observation that disease variants concentrate
  in cell-type-specific DNase hypersensitive sites.

---

## Complementary Genomic Datasets

ENCODE provides deep reference data for specific biosamples. GEO complements this with datasets
from diverse conditions, perturbations, and disease states.

---

### Barrett et al. 2013 — GEO complementary datasets

- **Citation:** Barrett T, Wilhite SE, Ledoux P, Evangelista C, et al. NCBI GEO: archive for
  functional genomics data sets — update. *Nucleic Acids Research*, 41(D1), D991-D995, 2013.
- **DOI:** [10.1093/nar/gks1193](https://doi.org/10.1093/nar/gks1193)
- **PMID:** 23193258 | **PMC:** PMC3531084
- **Citations:** ~4,200
- **Key findings:** Largest public functional genomics repository with >4 million samples
  across >200,000 series. While ENCODE provides reference data under standard conditions,
  GEO has:
  - Disease vs. normal comparisons
  - Perturbation experiments (drug treatment, cytokine stimulation)
  - Time courses and developmental series
  - Rare cell types not profiled by ENCODE

  The cross-reference skill links ENCODE experiments to GEO datasets using shared biosamples,
  targets, and conditions. GEO accessions (GSE/GSM) are stored alongside ENCODE accessions
  in the tracking database. GEO also links to SRA for raw data retrieval.

---

## Transcription Factor Binding Motifs

ENCODE ChIP-seq identifies TF binding locations but not the DNA motifs recognized. JASPAR
provides position weight matrices connecting binding to sequence mechanisms.

---

### Castro-Mondragon et al. 2022 — JASPAR 2022 TF motif database

- **Citation:** Castro-Mondragon JA, Riudavets-Puig R, Rauluseviciute I, et al. JASPAR 2022:
  the 9th release of the open-access database of transcription factor binding profiles.
  *Nucleic Acids Research*, 50(D1), D580-D587, 2022.
- **DOI:** [10.1093/nar/gkab1113](https://doi.org/10.1093/nar/gkab1113)
- **PMID:** 34850907 | **PMC:** PMC8728201
- **Citations:** ~1,400
- **Key findings:** Contains 1,956 TF binding profiles across six taxonomic groups. Each
  profile includes quality score, source experiment, TF class/family annotations, and
  UniProt links. Cross-referencing ENCODE peaks with JASPAR motifs:
  - Validates ChIP-seq peaks contain expected binding motif (QC)
  - Predicts TF binding at cCREs lacking direct ChIP-seq evidence

  The cross-reference skill connects ENCODE TF targets to JASPAR identifiers (MA prefix),
  supporting motif enrichment with HOMER or MEME. REST API at jaspar.elixir.no/api/v1/
  enables programmatic access.

---

## Population Genetics and Constraint

Regulatory elements under purifying selection are depleted of common variants. gnomAD provides
population-level variant frequencies for assessing evolutionary constraint.

---

### Karczewski et al. 2020 — gnomAD population variant database

- **Citation:** Karczewski KJ, Francioli LC, Tiao G, Cummings BB, et al. The mutational
  constraint spectrum quantified from variation in 141,456 humans. *Nature*, 581(7809),
  434-443, 2020.
- **DOI:** [10.1038/s41586-020-2308-7](https://doi.org/10.1038/s41586-020-2308-7)
- **PMID:** 32461654 | **PMC:** PMC7334197
- **Citations:** ~5,000
- **Key findings:** Cataloged 241 million short variants and 335,000 SVs from 141,456 humans
  across eight ancestry groups. Gene-level constraint metrics:
  - pLI: probability of loss-of-function intolerance
  - LOEUF: observed/expected loss-of-function ratio
  - Missense Z-scores for missense intolerance

  Cross-referencing ENCODE cCREs with gnomAD identifies elements under selection (depleted
  of common variants) vs. tolerant of variation. The skill annotates variants within cCREs
  with population frequencies — essential for distinguishing rare pathogenic variants
  (AF < 0.1%) from common benign polymorphisms. gnomAD GraphQL API enables efficient
  programmatic queries.

---

## Genome Annotation and Coordinate Systems

ENCODE regulatory elements need gene model annotation, variant effect prediction, and
coordinate mapping between assemblies. Ensembl provides all three.

---

### Cunningham et al. 2022 — Ensembl genome annotation and VEP

- **Citation:** Cunningham F, Allen JE, Allen J, et al. Ensembl 2022. *Nucleic Acids
  Research*, 50(D1), D988-D995, 2022.
- **DOI:** [10.1093/nar/gkab1049](https://doi.org/10.1093/nar/gkab1049)
- **PMID:** 34791404 | **PMC:** PMC8728283
- **Citations:** ~1,000
- **Key findings:** Comprehensive annotation including GENCODE gene models, the Ensembl
  Regulatory Build (integrating ENCODE + Roadmap), VEP variant prediction, and comparative
  genomics for 285 vertebrate genomes. The cross-reference skill uses Ensembl for:
  1. **Coordinate mapping:** Assembly Mapper API for GRCh38 <-> hg19 liftOver
  2. **Gene annotation:** GENCODE models for peak-to-gene assignment
  3. **Variant effects:** VEP classifies variants in regulatory elements

  VEP integrates ENCODE regulatory annotations to predict whether non-coding variants
  disrupt functional elements. REST API at rest.ensembl.org provides all capabilities
  programmatically without local database installation.

---
