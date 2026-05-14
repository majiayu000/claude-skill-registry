# GEO Connector — Literature References

**Last updated:** 2026-03-07
**Purpose:** Reference catalog for the geo-connector skill — key papers informing the Gene Expression Omnibus repository, data submission/retrieval standards, and complementary genomic data archives for discovering datasets that extend ENCODE functional genomic data.

---

## GEO Database

---

### Barrett et al. 2013 — NCBI GEO: archive for functional genomics data

- **Citation:** Barrett T, Wilhite SE, Ledoux P, Evangelista C, Kim IF,
  Tomashevsky M, Marshall KA, Phillippy KH, Sherman PM, Holko M, et al. NCBI
  GEO: archive for functional genomics data sets — update. Nucleic Acids
  Research, 41(D1):D991-D995, 2013.
- **DOI:** [10.1093/nar/gks1193](https://doi.org/10.1093/nar/gks1193)
- **PMID:** 23193258 | **PMC:** PMC3531084
- **Citations:** ~4,200
- **Key findings:** Described GEO as the largest public repository of
  functional genomics data, hosting >1 million samples across microarray, RNA-
  seq, ChIP-seq, ATAC-seq, methylation array, and other assay types. The GEO
  data architecture uses three core entities: Platform (GPL, technology
  definition including probe sequences for arrays or library construction
  protocol for sequencing), Sample (GSM, individual measurement from one
  biological specimen), and Series (GSE, collection of related samples
  constituting a complete experiment). GEO DataSets (GDS) provide a curated
  layer with standardized gene identifiers, background subtraction, and cross-
  platform normalization for selected high-value Series — though GDS curation
  covers only a small fraction of all deposited Series, so most programmatic
  discovery relies on GSE-level metadata. The E-utilities API (eSearch for
  finding entries, eFetch for retrieving metadata, eLink for cross-database
  connections) enables programmatic search and retrieval essential for the geo-
  connector skill's automated discovery of datasets complementary to ENCODE —
  for example, finding RNA-seq expression datasets from the same tissue types
  profiled by ENCODE ChIP-seq, or identifying perturbation experiments (drug
  treatment, knockout, siRNA) that test the functional consequences of
  disrupting ENCODE-annotated regulatory elements. As of 2025, GEO contains
  over 5 million samples across more than 200,000 Series, making it by far
  the largest single source of reusable functional genomics data worldwide.
  The structured metadata fields — including organism, tissue source, cell
  type, molecule type (total RNA, polyA RNA, genomic DNA), and library
  strategy (RNA-Seq, ChIP-Seq, Bisulfite-Seq) — enable precise queries that
  match the experimental parameters tracked by the ENCODE portal, facilitating
  systematic identification of complementary datasets.

---

### Edgar et al. 2002 — Gene Expression Omnibus: original design and deposition

- **Citation:** Edgar R, Domrachev M, Lash AE. Gene Expression Omnibus: NCBI
  gene expression and hybridization array data repository. Nucleic Acids
  Research, 30(1):207-210, 2002.
- **DOI:** [10.1093/nar/30.1.207](https://doi.org/10.1093/nar/30.1.207)
- **PMID:** 11752295 | **PMC:** PMC99122
- **Citations:** ~4,000
- **Key findings:** Established GEO as the original NCBI repository for gene
  expression data, implementing the MIAME (Minimum Information About a
  Microarray Experiment) standard for metadata completeness requiring
  description of experimental design, sample characteristics, hybridization
  protocols, normalization methods, and data processing steps. The founding
  design principles that still govern GEO were: (1) accept any high-throughput
  functional genomics data type, not limiting to expression; (2) require
  structured metadata for reproducibility; (3) provide free, unrestricted
  public access with no registration required for downloads; and (4) support
  both web-based browsing and programmatic API access. GEO pioneered the
  concept of mandatory data deposition as a condition of journal publication,
  which became the norm across genomics and fundamentally enabled re-analysis
  and meta-analysis of published data — a practice that transformed genomics
  from a field where data was hoarded to one where open sharing is the
  default. The repository's permissive data model — accepting virtually any
  array or sequencing-based assay — allowed it to grow from microarray
  expression data to encompass ChIP-seq, ATAC-seq, WGBS, Hi-C, single-cell
  RNA-seq, spatial transcriptomics, and CRISPR screens, making it the most
  comprehensive complement to ENCODE's focused regulatory genomics collection.
  For the geo-connector skill, GEO's founding principle of unrestricted
  programmatic access remains critical, as it enables automated batch queries
  across the entire repository without API keys or authentication.

---

## Data Retrieval

---

### Clough & Barrett 2016 — Practical GEO data retrieval methods

- **Citation:** Clough E, Barrett T. The Gene Expression Omnibus Database.
  Methods in Molecular Biology, 1418:93-110, 2016.
- **DOI:** [10.1007/978-1-4939-3578-9_5](https://doi.org/10.1007/978-1-4939-3578-9_5)
- **PMID:** 27008011 | **PMC:** PMC4944384
- **Citations:** ~500
- **Key findings:** Comprehensive practical guide to searching, browsing, and
  downloading GEO data through multiple interfaces: the web search
  (ncbi.nlm.nih.gov/geo), GEO Profiles (gene-centric view showing expression
  across all experiments), GEO DataSets (experiment-centric view with curated
  metadata), and programmatic access via the GEOquery R/Bioconductor package
  and NCBI E-utilities. Detailed the critical distinction between raw data
  (CEL files for microarrays, FASTQ files deposited in the Sequence Read
  Archive for sequencing experiments) and processed data (expression matrices,
  peak files, methylation beta values), emphasizing that raw data enables
  independent re-analysis and quality assessment while processed data may
  embed pipeline-specific normalization artifacts that are difficult to detect
  without inspecting the original reads. Described GEO2R, the web-based
  differential expression tool that applies limma/GEOquery to compare user-
  defined sample groups without requiring local computation — useful for rapid
  preliminary analysis but limited to microarray and simple count matrix
  designs. Recommended searching GEO with MeSH terms and organism filters for
  systematic dataset discovery, and using the eLink utility to traverse from
  GEO Series to associated PubMed publications, BioProject records, and SRA
  runs. This chapter established the practical workflow for integrating GEO
  datasets with ENCODE: search by tissue type and assay, verify experimental
  quality through metadata inspection, download processed or raw data, and
  harmonize coordinate systems (GRCh37 vs. GRCh38) and gene identifiers
  (Ensembl vs. RefSeq vs. gene symbols) with ENCODE. The guide also
  emphasized the importance of examining sample-level metadata for batch
  information (processing date, technician, flow cell) and biological
  covariates (age, sex, disease status) that may confound downstream
  integrative analyses with ENCODE data.

---

## Complementary Archives

---

### Leinonen et al. 2011 — The Sequence Read Archive

- **Citation:** Leinonen R, Sugawara H, Shumway M, International Nucleotide
  Sequence Database Collaboration. The Sequence Read Archive. Nucleic Acids
  Research, 39(Database issue):D19-D21, 2011.
- **DOI:** [10.1093/nar/gkq1019](https://doi.org/10.1093/nar/gkq1019)
- **PMID:** 21062823 | **PMC:** PMC3013647
- **Citations:** ~3,000
- **Key findings:** Described the Sequence Read Archive (SRA) as the
  international repository for raw next-generation sequencing data, jointly
  operated by NCBI (SRA), EMBL-EBI (European Nucleotide Archive/ENA), and DDBJ
  (DNA Data Bank of Japan) with automatic data mirroring across all three
  nodes ensuring global data persistence and redundancy. SRA stores raw reads
  in a compressed binary format with conversion tools (fastq-dump, the newer
  fasterq-dump, and the cloud-native SRA Toolkit) for extracting FASTQ files.
  The SRA accession hierarchy links Study (SRP) to Experiment (SRX) to Run
  (SRR), with cross-references to BioProject and BioSample providing
  standardized experimental metadata including organism, tissue source,
  library strategy, and sequencing platform. For the geo-connector skill,
  understanding the GEO-SRA bidirectional linkage is critical: most GEO Series
  with sequencing data have corresponding SRA accessions accessible via the
  E-utilities eLink service, and SRA Run Browser provides quality metrics
  (read count, base count, mean quality score) for pre-screening datasets
  before committing to full download. ENCODE experiments often have
  complementary datasets in GEO/SRA from the same cell types or conditions but
  with different assays or perturbations, and SRA's comprehensive raw data
  archive enables re-processing with updated pipelines, reference genomes, and
  gene models — essential when harmonizing older GEO datasets with current
  ENCODE processing standards. The SRA cloud computing initiative (SRA on
  AWS, Google Cloud, and Azure) also provides direct cloud-based access to
  raw reads without local download, enabling scalable re-analysis pipelines
  that can process hundreds of GEO/SRA datasets in parallel.

---

### Kolesnikov et al. 2015 — ArrayExpress/BioStudies: European counterpart to GEO

- **Citation:** Kolesnikov N, Hastings E, Keays M, Melnichuk O, Tang YA,
  Williams E, Dylag M, Kurbatova N, Brandizi M, Burdett T, et al. ArrayExpress
  update — simplifying data submissions. Nucleic Acids Research,
  43(D1):D1113-D1116, 2015.
- **DOI:** [10.1093/nar/gku1057](https://doi.org/10.1093/nar/gku1057)
- **PMID:** 25361974 | **PMC:** PMC4383899
- **Citations:** ~800
- **Key findings:** Described ArrayExpress (now BioStudies at EMBL-EBI) as the
  European counterpart to GEO, containing >70,000 experiments including a
  curated subset automatically imported from GEO. ArrayExpress uses the MAGE-
  TAB (MicroArray Gene Expression Tabular) format for experiment description,
  which provides richer structured metadata than GEO's SOFT format —
  particularly for experimental design variables, factor values (what differs
  between samples), sample characteristics (organism, tissue, cell type,
  genotype), and detailed protocol descriptions. The MAGE-TAB format
  explicitly encodes multi-factor experimental designs (e.g., tissue x
  treatment x timepoint), making it substantially easier to programmatically
  identify experiments with specific experimental contrasts relevant to a
  research question. The database serves as the European Node of the
  International Nucleotide Sequence Database Collaboration (INSDC) for
  functional genomics metadata. For the geo-connector skill, ArrayExpress/
  BioStudies provides two advantages: (1) an alternative search interface to
  cross-archived data (many studies are in both GEO and ArrayExpress),
  offering different search facets that may surface datasets missed by GEO
  queries; and (2) access to European-origin datasets and curated experiment
  collections (like the Expression Atlas, which provides pre-computed
  differential expression results for thousands of experiments) that may not
  be fully indexed or easily discoverable through GEO alone. The Expression
  Atlas in particular provides ready-to-use gene expression baselines across
  tissues and cell types that complement ENCODE regulatory annotations with
  transcriptional output data. When used together, GEO, SRA, and
  ArrayExpress/BioStudies form a comprehensive discovery layer for identifying
  functional genomics datasets that extend, replicate, or complement ENCODE's
  curated regulatory element catalog.

---
