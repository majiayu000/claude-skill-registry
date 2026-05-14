# Ensembl Annotation — Literature References

**Last updated:** 2026-03-07
**Purpose:** Reference catalog for the ensembl-annotation skill — key papers informing genome annotation, variant effect prediction, regulatory build resources, and programmatic access to the Ensembl project infrastructure.

---

## Core Ensembl Releases

---

### Cunningham et al. 2022 — Ensembl 2022: comprehensive genome annotation

- **Citation:** Cunningham F, Allen JE, Allen J, Alvarez-Jarreta J, Amode MR,
  Armean IM, Austine-Orimoloye O, Azov AG, Barnes I, Bennett R, et al. Ensembl
  2022. Nucleic Acids Research, 50(D1):D988-D995, 2022.
- **DOI:** [10.1093/nar/gkab1049](https://doi.org/10.1093/nar/gkab1049)
- **PMID:** 34791404 | **PMC:** PMC8728283
- **Citations:** ~1,000
- **Key findings:** Ensembl 2022 annotated 273 vertebrate genomes with
  production-quality gene models, regulatory annotations, and comparative
  genomics data through its combined Havana (manual curation) and Ensembl
  (automated prediction) pipeline. The human annotation (GENCODE v39) included
  61,544 genes (19,957 protein-coding), 241,544 transcripts, and 1.4 million
  regulatory features from the Ensembl Regulatory Build integrating ENCODE
  Phase III data. Key updates included improved non-coding RNA annotation
  using Rfam classification, the expanded MANE (Matched Annotation from NCBI
  and EMBL-EBI) Select transcript set providing one agreed-upon representative
  transcript per protein-coding gene, and enhanced variant consequence
  prediction through VEP. The Ensembl gene annotation pipeline remains the
  reference standard for GRCh38 genome annotation, providing the coordinate
  framework that all ENCODE experiments use for peak-to-gene mapping, TSS
  definitions, and genomic feature classification.

---

### Yates et al. 2020 — Ensembl 2020: enabling non-vertebrate genomics research

- **Citation:** Yates AD, Achuthan P, Akanni W, Allen J, Allen J, Alvarez-
  Jarreta J, Amode MR, Armean IM, Azov AG, Bennett R, et al. Ensembl 2020.
  Nucleic Acids Research, 48(D1):D682-D688, 2020.
- **DOI:** [10.1093/nar/gkz966](https://doi.org/10.1093/nar/gkz966)
- **PMID:** 31691826 | **PMC:** PMC7145704
- **Citations:** ~700
- **Key findings:** Ensembl 2020 introduced Ensembl Rapid Release, a system
  for rapidly annotating newly assembled genomes without waiting for the full
  production cycle (which can take months), enabling timely gene model
  availability for emerging reference genomes. Deepened integration with the
  UniProt protein knowledge base through automatic cross-referencing of
  Ensembl transcript predictions with experimentally characterized protein
  sequences. Updated the pan-compara analysis to cover 296 species with
  improved gene tree inference and synteny detection, enabling orthology-based
  annotation transfer for species without direct experimental evidence. For
  ENCODE users, the key enhancement was improved MANE transcript selection —
  providing definitive transcript identifiers agreed upon by both
  Ensembl/GENCODE and NCBI RefSeq for unambiguous gene-level interpretation of
  regulatory data, resolving the long-standing confusion when different
  databases use different "canonical" transcripts for the same gene.

---

### Howe et al. 2021 — Ensembl 2021: rapid release and new vertebrate genomes

- **Citation:** Howe KL, Achuthan P, Allen J, Allen J, Alvarez-Jarreta J,
  Amode MR, Armean IM, Azov AG, Bennett R, Bhai J, et al. Ensembl 2021.
  Nucleic Acids Research, 49(D1):D884-D891, 2021.
- **DOI:** [10.1093/nar/gkaa942](https://doi.org/10.1093/nar/gkaa942)
- **PMID:** 33137190 | **PMC:** PMC7778937
- **Citations:** ~800
- **Key findings:** Ensembl 2021 annotated 238 vertebrate genomes with
  production-quality gene models and launched Ensembl Rapid Release covering
  311 additional species for a total of 549 species with gene annotations.
  Expanded the MANE Select set to cover >97% of human protein-coding genes
  (19,062 of 19,399), providing definitive transcript identifiers for clinical
  variant reporting and enabling consistent gene-level quantification across
  studies. Updated the coordinate liftover service with improved chain files
  for GRCh37-to-GRCh38 conversion, addressing persistent issues with ENCODE
  datasets generated on the older hg19/GRCh37 assembly that need to be mapped
  to the current GRCh38 reference. Introduced integrated gene pages unifying
  structural annotation, regulatory features, genetic variation, comparative
  genomics, and tissue-specific expression data into a single gene-centric
  view.

---

### Martin et al. 2023 — Ensembl 2023: T2T integration and pangenome support

- **Citation:** Martin FJ, Amode MR, Anber A, Apweiler R, Arkinson RG, et al.
  Ensembl 2023. Nucleic Acids Research, 51(D1):D933-D941, 2023.
- **DOI:** [10.1093/nar/gkac958](https://doi.org/10.1093/nar/gkac958)
- **PMID:** 36318249 | **PMC:** PMC9825606
- **Citations:** ~400
- **Key findings:** Ensembl 2023 incorporated the T2T-CHM13 assembly — the
  first truly complete, gapless human genome sequence — alongside GRCh38,
  enabling variant annotation, regulatory feature mapping, and gene model
  annotation on both reference assemblies. T2T-CHM13 added ~200 Mb of
  previously unresolved sequence including centromeres, telomeres, and
  segmental duplications, revealing new genes and regulatory elements in
  regions invisible to ENCODE experiments mapped against GRCh38. Expanded the
  Regulatory Build to integrate ENCODE Phase IV data with enhanced cell-type
  coverage and improved chromatin state assignments. Introduced Ensembl Tark
  (Transcript Archive) for tracking transcript model changes across Ensembl
  releases — essential for reproducibility when revisiting historical ENCODE
  analyses where gene model updates could change peak-to-gene annotations.
  Also began pangenome graph integration for representing human population
  structural diversity beyond single linear references.

---

## Variant Effect Prediction

---

### McLaren et al. 2016 — Variant Effect Predictor (VEP)

- **Citation:** McLaren W, Gil L, Hunt SE, Riat HS, Ritchie GRS, Thormann A,
  Flicek P, Cunningham F. The Ensembl Variant Effect Predictor. Genome
  Biology, 17(1):122, 2016.
- **DOI:** [10.1186/s13059-016-0974-4](https://doi.org/10.1186/s13059-016-0974-4)
- **PMID:** 27268795 | **PMC:** PMC4893825
- **Citations:** ~4,500
- **Key findings:** VEP annotates genetic variants with predicted functional
  consequences using Ensembl gene models, assigning standardized Sequence
  Ontology (SO) terms ranked by severity: transcript ablation and splice
  acceptor/donor variants (most severe), through frameshift, missense, and
  synonymous variants, to regulatory region and intergenic variants (least
  severe). Integrates pluggable pathogenicity prediction algorithms including
  SIFT (sequence-based), PolyPhen-2 (structure-based), CADD (combined
  annotation-dependent depletion), and REVEL (ensemble method), providing
  multiple complementary evidence streams for each variant. VEP maps variants
  to overlapping regulatory features from the Ensembl Regulatory Build,
  annotating whether a variant falls in a promoter, enhancer, CTCF site, or
  open chromatin region — directly integrating ENCODE-derived regulatory
  annotations into variant interpretation. For non-coding variants, VEP
  reports the regulatory feature stable ID and cell-type activity status,
  enabling researchers to determine whether a variant disrupts a regulatory
  element that is active in disease-relevant cell types. The plugin
  architecture supports custom annotation sources (ClinVar, gnomAD, ENCODE-
  specific tracks), processing millions of variants per run from standard VCF
  input.

---

## Regulatory Annotation

---

### Zerbino et al. 2018 — The Ensembl Regulatory Build

- **Citation:** Zerbino DR, Wilder SP, Johnson N, Juettemann T, Flicek P. The
  Ensembl Regulatory Build. Genome Biology, 16(1):56, 2015.
- **DOI:** [10.1186/s13059-015-0621-5](https://doi.org/10.1186/s13059-015-0621-5)
- **PMID:** 25887522 | **PMC:** PMC4407537
- **Citations:** ~800
- **Key findings:** Described the Ensembl Regulatory Build computational
  pipeline that integrates ENCODE and Roadmap Epigenomics data to annotate
  functional regulatory features across human and mouse genomes. The pipeline
  uses histone modification ChIP-seq (H3K4me3, H3K4me1, H3K27ac, H3K36me3),
  DNase-seq/ATAC-seq, CTCF ChIP-seq, and TF ChIP-seq to segment the genome
  into regulatory feature categories: promoters (H3K4me3 + H3K27ac near TSS),
  enhancers (H3K4me1 + H3K27ac distal from TSS), CTCF binding sites (CTCF
  ChIP-seq + characteristic motif), open chromatin regions (DHS/ATAC without
  histone marks), and TF binding sites (TF ChIP-seq peaks). Each regulatory
  feature is assigned cell-type-specific activity states (active, poised,
  repressed, inactive, NA) based on the pattern of histone marks observed in
  each profiled cell type. The Regulatory Build provides the unified
  regulatory annotation layer used by VEP for variant consequence prediction,
  translating raw ENCODE experimental data into functional categories
  interpretable by clinical geneticists and disease researchers.

---

## Programmatic Access

---

### Hunt et al. 2018 — Ensembl variation resources and REST API

- **Citation:** Hunt SE, McLaren W, Gil L, Thormann A, Schuilenburg H,
  Sheppard D, Parton A, Armean IM, Trevanion SJ, Flicek P, Cunningham F.
  Ensembl variation resources. Database, 2018:bay119, 2018.
- **DOI:** [10.1093/database/bay119](https://doi.org/10.1093/database/bay119)
- **PMID:** 30576484 | **PMC:** PMC6305438
- **Citations:** ~300
- **Key findings:** Documented the Ensembl REST API (rest.ensembl.org)
  endpoints for variant annotation, coordinate conversion, sequence retrieval,
  and regulatory feature lookup that the ensembl-annotation skill uses for
  programmatic data access. Key endpoints include: /vep/{species}/region
  (batch variant effect prediction), /overlap/region/{species}/{region}
  (features overlapping a genomic region), /lookup/id/{id} (gene/transcript
  metadata by Ensembl ID), /sequence/region/{species}/{region} (genomic
  sequence retrieval), and /regulatory/species/{species}/id/{id} (regulatory
  feature details). The API supports JSON and XML response formats with rate
  limiting at 15 requests/second for anonymous users and 55/second with
  registered API keys. For large-scale annotation tasks (>1,000 variants), the
  paper recommends batch VEP submission via POST request or local VEP
  installation with cached databases. The REST API enables real-time Ensembl
  queries without requiring local database installation, making it the
  preferred access method for the ensembl-annotation skill's on-demand
  annotation workflows.

---
