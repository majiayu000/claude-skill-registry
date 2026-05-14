# Download ENCODE — Literature References

**Last updated:** 2026-03-07
**Purpose:** Reference catalog for the download-encode skill — key papers establishing data
access principles, file format standards, quality filtering criteria, and the genomic blacklist
regions that must be applied when downloading and processing ENCODE files.

The download-encode skill retrieves ENCODE files (BED, FASTQ, BAM, bigWig) with MD5 verification
and organizes them by experiment, format, or both. Responsible data download requires understanding
FAIR principles for data stewardship, the ENCODE portal's file organization and quality audit
system, ChIP-seq quality metrics that inform file selection, blacklist regions for filtering, and
reference epigenome standards for cross-dataset compatibility.

These 5 papers cover three critical aspects: (1) the principles of findable, accessible,
interoperable, and reusable data, (2) the portal infrastructure and quality audit system for
file selection, and (3) the quality standards and blacklist regions that must be applied to
downloaded data before analysis.

---

## Data Access and Stewardship Principles

Data downloading is not merely a technical operation — it is the first step in a chain of
custody that must maintain data integrity, provenance, and reproducibility from source to
publication. The FAIR principles establish the framework for responsible data stewardship.

---

### Wilkinson et al. 2016 — FAIR principles for scientific data management

- **Citation:** Wilkinson MD, Dumontier M, Aalbersberg IJ, Appleton G, Axton M, Baak A,
  Blomberg N, Boiten JW, da Silva Santos LB, Bourne PE, et al. The FAIR Guiding Principles
  for scientific data management and stewardship. *Scientific Data*, 3, 160018, 2016.
- **DOI:** [10.1038/sdata.2016.18](https://doi.org/10.1038/sdata.2016.18)
- **PMID:** 26978244 | **PMC:** PMC4792175
- **Citations:** ~8,000
- **Key findings:** Defined the four foundational principles for scientific data:
  - **Findable:** persistent identifiers, rich metadata indexed in searchable resources
  - **Accessible:** retrievable by identifier via open, standardized protocols
  - **Interoperable:** formal, shared vocabularies and qualified references
  - **Reusable:** clear licensing, provenance documentation, domain standards

  ENCODE's REST API, accession system (ENCSR/ENCFF prefixes), controlled vocabularies, and
  Creative Commons licensing implement these principles. The download-encode skill enforces
  FAIR compliance by preserving accession linkage in file names and directories, verifying
  MD5 checksums for integrity (Accessible), and maintaining provenance records linking
  downloaded files to source experiments (Reusable). The organize_by options (experiment,
  format, experiment_format) ensure local file organization preserves the logical structure
  needed for findability.

---

## ENCODE Portal and File Access

The ENCODE portal organizes files within a hierarchy: experiments contain replicates, replicates
produce files, and files have derived_from relationships. Understanding this hierarchy is
essential for selecting the correct files.

---

### Davis et al. 2018 — ENCODE data portal file access and audit system

- **Citation:** Davis CA, Hitz BC, Sloan CA, Chan ET, Davidson JM, Gabdank I, Hilton JA,
  Jain K, Baymuradov UK, Narayanan AK, Onate KC, Graham K, Miyasato SR, Dreszer TR,
  Strattan JS, Jolanki O, Tanaka FY, Cherry JM. The Encyclopedia of DNA elements (ENCODE):
  data portal update. *Nucleic Acids Research*, 46(D1), D794-D801, 2018.
- **DOI:** [10.1093/nar/gkx1081](https://doi.org/10.1093/nar/gkx1081)
- **PMID:** 29126249 | **PMC:** PMC5753278
- **Citations:** ~400
- **Key findings:** Documented the portal's file organization including:
  - Output type hierarchy: raw data (FASTQ) > alignments (BAM) > signal (bigWig) > peaks (BED)
  - preferred_default flag identifying recommended files per experiment
  - Four-tier audit system: ERROR, NOT_COMPLIANT, WARNING, INTERNAL_ACTION
  - File status lifecycle: uploaded > in progress > released > archived/revoked
  - Batch download manifests and cloud access (s3://encode-public, gs://encode-public)

  The download skill uses preferred_default=True to select IDR thresholded peaks for
  ChIP-seq, optimal peaks for ATAC-seq, and gene quantifications for RNA-seq. The audit
  system surfaces quality concerns that the skill reports to users.

---

## Quality-Informed File Selection

Downloading data without understanding quality leads to false discoveries. The ENCODE audit
system catches many issues, but users must understand assay-specific metrics to make informed
decisions about which files to use.

---

### Landt et al. 2012 — ChIP-seq guidelines defining quality metrics

- **Citation:** Landt SG, Marinov GK, Kundaje A, Kheradpour P, Pauli F, et al. ChIP-seq
  guidelines and practices of the ENCODE and modENCODE consortia. *Genome Research*,
  22(9), 1813-1831, 2012.
- **DOI:** [10.1101/gr.136184.111](https://doi.org/10.1101/gr.136184.111)
- **PMID:** 22955991 | **PMC:** PMC3431496
- **Citations:** ~3,400
- **Key findings:** Established the quality metrics that determine which files pass ENCODE
  audit and receive preferred_default:
  - FRiP >= 1% for broad marks, 5-20% typical for TFs
  - NSC > 1.05 (normalized strand coefficient)
  - RSC > 0.8 (relative strand coefficient)
  - NRF >= 0.8 (non-redundant fraction, library complexity)

  Also established IDR framework: optimal peaks (IDR < 0.05) represent reproducible binding.
  The IDR thresholded peak file (preferred_default for most ChIP-seq) balances sensitivity
  and specificity. When downloading peaks, prefer IDR thresholded > pooled peaks > individual
  replicate peaks. Different expectations apply for sharp-peak TFs vs. broad histone marks.

---

### Amemiya et al. 2019 — ENCODE Blacklist v2 for filtering downloaded data

- **Citation:** Amemiya HM, Kundaje A, Boyle AP. The ENCODE Blacklist: identification of
  problematic regions of the genome. *Scientific Reports*, 9(1), 9354, 2019.
- **DOI:** [10.1038/s41598-019-45839-z](https://doi.org/10.1038/s41598-019-45839-z)
- **PMID:** 31249361 | **PMC:** PMC6597582
- **Citations:** ~1,400
- **Key findings:** Defined the ENCODE Blacklist v2 — 910 genomic regions in GRCh38 (~0.5%
  of genome, ~15 Mb) producing artifact signal from:
  - Collapsed repetitive sequences
  - Satellite DNA arrays
  - Assembly gaps and errors

  These regions can contain >50% of signal in input/control samples, creating false-positive
  peaks. ENCODE processed files (peaks, signal tracks) are already blacklist-filtered, but
  raw data (FASTQ, unfiltered BAM) are not. Official blacklist accessions:
  - ENCFF356LFX (human GRCh38)
  - ENCFF547MET (mouse mm10)

  The download skill warns users to apply blacklist filtering to raw data. Failure to filter
  is the most common source of false-positive peaks in published ChIP-seq and ATAC-seq.

---

## Reference Epigenomes for Cross-Dataset Compatibility

When downloading from multiple experiments for integrative analysis, users must ensure
cross-dataset compatibility: matching assemblies, consistent normalization, and comparable
quality.

---

### Kundaje et al. 2015 — Roadmap Epigenomics reference standards

- **Citation:** Kundaje A, Meuleman W, Ernst J, Bilenky M, Yen A, et al. Integrative analysis
  of 111 reference human epigenomes. *Nature*, 518(7539), 317-330, 2015.
- **DOI:** [10.1038/nature14248](https://doi.org/10.1038/nature14248)
- **PMID:** 25693563 | **PMC:** PMC4530010
- **Citations:** ~4,500
- **Key findings:** Produced 111 reference epigenomes with standardized five-mark panel
  (H3K4me3, H3K4me1, H3K36me3, H3K27me3, H3K9me3), establishing:
  - Minimum mark panel for ChromHMM (5 marks for 15-state model)
  - Normalization standards: RPKM within-experiment, quantile cross-experiment
  - Quality thresholds for inclusion in integrative analysis
  - Assembly standards: hg19 for Roadmap, GRCh38 for ENCODE Phase 3

  When downloading data from both sources, coordinate liftOver is required before merging.
  The download skill validates assembly consistency and warns when mixing GRCh38 and hg19
  coordinates. Users should prioritize experiments matching these reference assay
  combinations for ChromHMM compatibility.

---
