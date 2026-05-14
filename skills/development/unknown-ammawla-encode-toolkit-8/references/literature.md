# Search ENCODE — Literature References

**Last updated:** 2026-03-07
**Purpose:** Reference catalog for the search-encode skill — key papers defining the ENCODE
Project, its data portal, and the candidate cis-regulatory element (cCRE) registry that
underpins experiment search and discovery.

The search-encode skill enables users to find ENCODE experiments by assay type, organ, biosample,
target, and organism. Understanding the project's evolution from pilot (2004) through comprehensive
catalogs (2012, 2020) and the architecture of the ENCODE portal is essential for effective data
discovery. These papers define the controlled vocabularies, metadata schemas, and cCRE
classifications that search queries rely on.

The 8 papers below are organized into three thematic groups: (1) the ENCODE Project's foundational
publications that define what data exists and how it is organized, (2) the data portal papers that
describe the technical infrastructure for programmatic search, and (3) the cCRE registry papers
that define the element-centric classification system used for filtering and categorizing results.

---

## ENCODE Project Foundation

The ENCODE Project has published three major consortium papers (2004, 2012, 2020) corresponding
to its three phases. Each phase expanded the scope of assay types, biosamples, and analytical
frameworks. Understanding which phase generated the data you are searching for is important
because metadata standards, quality thresholds, and file naming conventions evolved across
phases. Phase 1 (pilot) data used older assay protocols and may lack quality audit flags.
Phase 2 data covers 147 cell types with mature ChIP-seq and DNase-seq protocols. Phase 3 data
includes the newest assay types (CUT&RUN, CRISPR screens, single-cell methods) and the
cCRE registry.

---

### ENCODE Project Consortium 2004 — Launch of the Encyclopedia of DNA Elements

- **Citation:** The ENCODE Project Consortium. The ENCODE (ENCyclopedia Of DNA Elements)
  Project. *Science*, 306(5696), 636-640, 2004.
- **DOI:** [10.1126/science.1105136](https://doi.org/10.1126/science.1105136)
- **PMID:** 15499007 | **PMC:** PMC3232742
- **Citations:** ~2,200
- **Key findings:** Announced the ENCODE Project, defining its mission to identify all
  functional elements in the human genome. The pilot phase targeted 1% of the genome
  (30 Mb across 44 regions) using multiple approaches including ChIP-chip, DNase-seq,
  and RNA profiling. Established the project's organizational framework, data-sharing
  principles, and the consortium model that would scale to genome-wide coverage. For
  search purposes, this paper defines the foundational vocabulary of "functional elements"
  that ENCODE catalogs: promoters, enhancers, silencers, insulators, and non-coding RNA
  genes. The open data-sharing model established here — immediate public release with no
  embargo — directly enables the API access that search-encode relies on.

---

### ENCODE Project Consortium 2012 — Comprehensive encyclopedia across 147 cell types

- **Citation:** The ENCODE Project Consortium. An integrated encyclopedia of DNA elements in
  the human genome. *Nature*, 489(7414), 57-74, 2012.
- **DOI:** [10.1038/nature11247](https://doi.org/10.1038/nature11247)
- **PMID:** 22955616 | **PMC:** PMC3439153
- **Citations:** ~8,000
- **Key findings:** The integrative analysis paper from ENCODE Phase 2, reporting 1,640
  datasets across 147 cell types. Demonstrated that 80.4% of the human genome participates
  in at least one biochemical event, redefining genome functionality. Established the
  chromatin state model using histone modification combinations, defined cell-type-specific
  regulatory landscapes, and provided the first comprehensive catalog of distal elements.

  This paper defines the core assay categories (ChIP-seq, DNase-seq, RNA-seq, FAIRE-seq)
  and biosample hierarchy used for search filtering. The 147 cell types profiled established
  the biosample ontology — including the Tier 1 (K562, GM12878, H1-hESC), Tier 2, and
  Tier 3 classification — that remains the organizational backbone for ENCODE data browsing.
  Phase 2 data constitutes the largest block of ENCODE experiments and is the most common
  target of search queries.

---

### ENCODE Project Consortium 2020 — Phase 3 with expanded biosamples and assays

- **Citation:** The ENCODE Project Consortium, Moore JE, Purcaro MJ, Pratt HE, et al.
  Expanded encyclopaedias of DNA elements in the human and mouse genomes. *Nature*,
  583(7818), 699-710, 2020.
- **DOI:** [10.1038/s41586-020-2493-4](https://doi.org/10.1038/s41586-020-2493-4)
- **PMID:** 32728249 | **PMC:** PMC7410828
- **Citations:** ~1,200
- **Key findings:** ENCODE Phase 3 expanded the registry to 926,535 human and 339,815 mouse
  candidate cis-regulatory elements (cCREs), classified into:
  - Promoter-like signatures (PLS)
  - Proximal enhancer-like signatures (pELS)
  - Distal enhancer-like signatures (dELS)
  - CTCF-only
  - DNase-H3K4me3

  Introduced the Registry of cCREs as the primary organizational framework. This paper is
  the definitive reference for the cCRE classification system that search queries leverage.
  Phase 3 added CUT&RUN, CUT&Tag, CRISPR screens, MPRA, STARR-seq, and single-cell assays,
  expanding the assay_title vocabulary for search filtering. The biosample ontology now
  covers tissues, primary cells, cell lines, in vitro differentiated cells, and organoids
  across both human and mouse.

---

## ENCODE Data Portal

The ENCODE data portal (encodeproject.org) provides both a web-based search interface and a
REST API for programmatic access. The search-encode skill wraps the REST API, translating user
queries into API calls with appropriate parameters. Understanding the portal's metadata model —
how experiments relate to biosamples, files relate to experiments, and quality audits relate to
both — is essential for constructing effective searches.

---

### Sloan et al. 2016 — ENCODE data portal architecture and programmatic access

- **Citation:** Sloan CA, Chan ET, Davidson JM, Malladi VS, Strattan JS, Hitz BC, Gabdank I,
  Narayanan AK, Ho M, Lee BT, et al. ENCODE data at the ENCODE portal. *Nucleic Acids
  Research*, 44(D1), D726-D732, 2016.
- **DOI:** [10.1093/nar/gkv1160](https://doi.org/10.1093/nar/gkv1160)
- **PMID:** 26527727 | **PMC:** PMC4702836
- **Citations:** ~600
- **Key findings:** Described the ENCODE portal architecture including:
  - REST API with JSON-LD metadata model
  - Faceted search interface with ~200 biosample types
  - Standardized assay categories and audit-based quality tiers
  - Programmatic access via JSON API endpoints with pagination

  The metadata schema determines which fields are searchable and how experiments are
  organized. Key design: experiments have a single assay_title, can have multiple
  replicates, files are children of experiments with own quality metrics, and audit flags
  propagate from files to experiments. The search-encode skill mirrors these API patterns.

---

### Davis et al. 2018 — ENCODE portal update with improved search

- **Citation:** Davis CA, Hitz BC, Sloan CA, Chan ET, Davidson JM, Gabdank I, Hilton JA,
  Jain K, Baymuradov UK, Narayanan AK, Onate KC, Graham K, Miyasato SR, Dreszer TR,
  Strattan JS, Jolanki O, Tanaka FY, Cherry JM. The Encyclopedia of DNA elements (ENCODE):
  data portal update. *Nucleic Acids Research*, 46(D1), D794-D801, 2018.
- **DOI:** [10.1093/nar/gkx1081](https://doi.org/10.1093/nar/gkx1081)
- **PMID:** 29126249 | **PMC:** PMC5753278
- **Citations:** ~400
- **Key findings:** Updated the portal with improved search facets, matrix views for experiment
  discovery, and enhanced visualization. Introduced audit system refinements with quality
  flags enabling search-time quality filtering. Added support for new assay types (CRISPR
  screens, MPRA, single-cell assays). Documents the search matrix interface for
  cross-tabulation of biosamples vs. assay types — the conceptual model behind search-encode's
  multi-dimensional filtering. Also describes file relationship tracking (derived_from chains)
  and batch download manifests for downstream workflows.

---

## Candidate cis-Regulatory Elements (cCREs)

The cCRE registry represents a paradigm shift from experiment-centric to element-centric search.
Users can query for specific regulatory elements by classification, location, or activity state
across cell types. The three papers below describe the registry's construction, portal
implementation, and the functional annotation framework.

---

### Luo et al. 2020 — cCRE registry architecture on the portal

- **Citation:** Luo Y, Hitz BC, Gabdank I, Hilton JA, Kagda MS, et al. New developments on
  the Encyclopedia of DNA Elements (ENCODE) data portal. *Nucleic Acids Research*, 48(D1),
  D882-D889, 2020.
- **DOI:** [10.1093/nar/gkz1062](https://doi.org/10.1093/nar/gkz1062)
- **PMID:** 31713622 | **PMC:** PMC7061942
- **Citations:** ~800
- **Key findings:** Described the Registry of cCREs as the primary search framework, replacing
  experiment-centric browsing with element-centric discovery. Each cCRE has a unique accession
  (EH38E prefix for GRCh38, EH38ME for mm10). The classification decision tree:
  1. Requires high DNase signal (accessibility)
  2. Branches on H3K4me3 (promoter-like vs. not)
  3. Branches on H3K27ac (enhancer-like vs. not)
  4. Branches on CTCF (insulator-like vs. not)

  This system supports search-encode queries filtering by element type. The paper also
  describes visualization improvements including genome browser integration and interactive
  summary plots of cCRE distributions across cell types.

---

### Moore et al. 2020 — Defining 926,535 human cCREs

- **Citation:** Moore JE, Purcaro MJ, Pratt HE, Epstein CB, Shoresh N, et al. Expanded
  encyclopaedias of DNA elements in the human and mouse genomes. *Nature*, 583(7818),
  699-710, 2020.
- **DOI:** [10.1038/s41586-020-2493-4](https://doi.org/10.1038/s41586-020-2493-4)
- **PMID:** 32728248 | **PMC:** PMC7410830
- **Citations:** ~1,500
- **Key findings:** Detailed methodology for the five-group classification:
  - PLS: 36,573 human elements (promoter-like)
  - pELS: 52,998 (proximal enhancer-like)
  - dELS: 544,491 (distal enhancer-like — the largest category)
  - CTCF-only: 117,440
  - DNase-H3K4me3: 175,033

  Each cCRE has cell-type-specific activity states. Benchmarks: 75% of PLS overlap
  GENCODE TSSs; dELS show 3-fold enrichment for Vista-validated enhancers. This vocabulary
  is essential for interpreting search results and understanding what regulatory elements
  are represented in returned experiments.

---

### Abascal et al. 2020 — Functional annotation from expanded experiments

- **Citation:** Abascal F, Acosta R, Addleman NJ, Adrian J, Afzal V, et al. Expanded
  encyclopaedias of DNA elements in the human and mouse genomes. *Nature*, 583(7818),
  693-698, 2020.
- **DOI:** [10.1038/s41586-020-2489-0](https://doi.org/10.1038/s41586-020-2489-0)
- **PMID:** 32728247 | **PMC:** PMC7410826
- **Citations:** ~600
- **Key findings:** Broader perspective on ENCODE Phase 3 functional annotations, including
  integration of new assay types (CUT&RUN, CRISPR perturbations, single-cell) into the
  registry. Established a hierarchy of evidence for regulatory annotation:
  - Observational: ChIP-seq, DNase-seq
  - Correlative: eQTL, Hi-C
  - Perturbational: CRISPRi/CRISPRa
  - Direct functional: reporter assays (MPRA, STARR-seq)

  Documents the expanded assay vocabulary available in Phase 3 and the rationale behind
  assay category groupings used in search filters. Also discusses the transition to
  comparative human-mouse analysis enabling cross-species search queries.

---
