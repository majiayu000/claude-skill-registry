# Track Experiments — Literature References

**Last updated:** 2026-03-07
**Purpose:** Reference catalog for the track-experiments skill — key papers on data provenance,
reproducibility standards, metadata schemas, and experiment tracking frameworks that inform
local experiment management with publications, citations, and audit trails.

The track-experiments skill stores ENCODE experiments in a local SQLite database with associated
publications, pipeline information, and provenance records. It enables users to build curated
collections, compare experiments, export citation-ready metadata, and maintain a chain of
custody from raw ENCODE data through derived analyses.

The 5 papers below address three dimensions: (1) the FAIR principles and reproducibility
frameworks defining what information must be preserved, (2) the metadata standards defining
what constitutes a complete experiment record, and (3) the ENCODE portal metadata architecture
that the tracking system mirrors.

---

## Data Stewardship and FAIR Principles

Experiment tracking is fundamentally an act of data stewardship. Without systematic tracking,
researchers lose the chain of custody between source data and published results, making it
impossible for others (or the original researcher months later) to reconstruct the analytical
path. The FAIR principles provide the conceptual framework.

---

### Wilkinson et al. 2016 — FAIR principles as the foundation for tracking

- **Citation:** Wilkinson MD, Dumontier M, Aalbersberg IJ, Appleton G, Axton M, et al. The
  FAIR Guiding Principles for scientific data management and stewardship. *Scientific Data*,
  3, 160018, 2016.
- **DOI:** [10.1038/sdata.2016.18](https://doi.org/10.1038/sdata.2016.18)
- **PMID:** 26978244 | **PMC:** PMC4792175
- **Citations:** ~8,000
- **Key findings:** The track-experiments skill implements all four FAIR properties:
  - **Findable:** ENCODE accessions as persistent identifiers in the local database
  - **Accessible:** Export in standard formats (CSV, TSV, JSON, BibTeX, RIS)
  - **Interoperable:** ENCODE controlled vocabularies for assay, biosample, organism, target
  - **Reusable:** Provenance chains linking derived files to source experiments

  A key FAIR requirement is "richly described with a plurality of accurate and relevant
  attributes." The tracking system captures not just the accession but the full experiment
  context: biosample ontology terms, quality audit status, associated publications, and
  pipeline versions. Local tracking databases are scientifically valuable only when they
  maintain these properties across the entire analytical workflow.

---

## Reproducibility in Science

The reproducibility crisis motivates experiment tracking systems. Without recording which data,
software, and parameters produced a result, published findings cannot be independently verified.

---

### Baker 2016 — Quantifying the reproducibility crisis

- **Citation:** Baker M. 1,500 scientists lift the lid on reproducibility. *Nature*, 533(7604),
  452-454, 2016.
- **DOI:** [10.1038/533452a](https://doi.org/10.1038/533452a)
- **PMID:** 27225100
- **Citations:** ~3,200
- **Key findings:** Surveyed 1,576 researchers across disciplines:
  - 70% tried and failed to reproduce another scientist's experiment
  - 52% believed there was a significant reproducibility crisis
  - Contributing factors: selective reporting (>60%), pressure to publish (>50%),
    insufficient methodological detail (>40%), poor data management (~40%)

  In computational biology, the inability to trace which files, parameter settings, and
  software versions produced a result was identified as a major barrier — analyses that
  should be perfectly reproducible often are not because the analytical environment is
  insufficiently documented. The track-experiments skill addresses this by recording:
  experiment accessions (data versions), file accessions with MD5 checksums, pipeline
  software and versions, processing parameters, and derived file descriptions.

---

### Stodden et al. 2016 — Computational reproducibility standards

- **Citation:** Stodden V, McNutt M, Bailey DH, Deelman E, Gil Y, Hanson B, Heroux MA,
  Ioannidis JP, Taufer M. Enhancing reproducibility for computational methods. *Science*,
  354(6317), 1240-1241, 2016.
- **DOI:** [10.1126/science.aah6168](https://doi.org/10.1126/science.aah6168)
- **PMID:** 27940837
- **Citations:** ~1,800
- **Key findings:** Proposed four requirements for computational reproducibility:
  1. Complete data availability with persistent identifiers and versions
  2. Code and software availability with version information
  3. Computational environment documentation (OS, libraries, hardware)
  4. Workflow descriptions linking inputs to outputs

  The track-experiments skill implements this framework:
  - Requirement 1: ENCODE accessions provide persistent data identifiers
  - Requirement 2: Pipeline tracking captures software names and versions
  - Requirement 3: Provenance records include tool names and parameter settings
  - Requirement 4: log_derived_file captures tool, version, command, inputs, and outputs

  Export functions generate metadata formatted for publication methods sections, enabling
  auto-generation of reproducibility-compliant methods descriptions.

---

## Portal and Metadata Architecture

The track-experiments skill mirrors the ENCODE portal's metadata structure in a local SQLite
database. Understanding the portal's experiment schema is essential for maintaining consistent
local records that can be reconciled with the portal's authoritative source.

---

### Davis et al. 2018 — ENCODE portal metadata schema

- **Citation:** Davis CA, Hitz BC, Sloan CA, Chan ET, Davidson JM, Gabdank I, Hilton JA,
  Jain K, Baymuradov UK, Narayanan AK, Onate KC, Graham K, Miyasato SR, Dreszer TR,
  Strattan JS, Jolanki O, Tanaka FY, Cherry JM. The Encyclopedia of DNA elements (ENCODE):
  data portal update. *Nucleic Acids Research*, 46(D1), D794-D801, 2018.
- **DOI:** [10.1093/nar/gkx1081](https://doi.org/10.1093/nar/gkx1081)
- **PMID:** 29126249 | **PMC:** PMC5753278
- **Citations:** ~400
- **Key findings:** Documented the portal metadata schema:
  - Experiment accessions (ENCSR prefix) and file accessions (ENCFF prefix)
  - Biosample ontology terms (UBERON, CL, CLO, EFO)
  - Audit flags at experiment and file levels
  - File derived_from chains linking processed to raw data
  - Publication linkage via PubMed IDs and DOIs (many-to-many)

  The tracking system mirrors core fields: accession, assay_title, biosample_term_name,
  organism, target, lab, date_released, status. The JSON-LD metadata model with schema.org
  vocabulary ensures machine-readable records. Understanding audit_level is critical:
  ERROR experiments may have quality issues, NOT_COMPLIANT may fail standards but still
  be usable for some analyses.

---

## Metadata Standards for Genomic Experiments

Before ENCODE, the MIAME framework established that experimental data requires minimum
metadata for meaningful reuse — a principle the tracking system extends to local management.

---

### Brazma et al. 2001 — MIAME: minimum information standards

- **Citation:** Brazma A, Hingamp P, Quackenbush J, Sherlock G, Spellman P, et al. Minimum
  information about a microarray experiment (MIAME)-toward standards for microarray data.
  *Nature Genetics*, 29(4), 365-371, 2001.
- **DOI:** [10.1038/ng1201-365](https://doi.org/10.1038/ng1201-365)
- **PMID:** 11726920
- **Citations:** ~3,500
- **Key findings:** Established minimum information requirements for experiment reuse:
  1. Experimental design (biological question)
  2. Platform design (what was measured)
  3. Sample information (what was profiled)
  4. Assay procedures (how it was done)
  5. Measurements and normalization (the actual data)
  6. Quality controls (how reliable it is)

  Although written for microarrays, MIAME pioneered structured metadata checklists adopted
  by ENCODE, GEO (MIAME compliance), and MINSEQE (sequencing). The track-experiments skill
  extends this philosophy: tracked experiments must carry organism, assay type, biosample
  with ontology term, target, quality audit status, and publications. MIAME demonstrates
  that metadata without provenance is insufficient — both data and experimental context
  must be preserved for reproducibility.

---
