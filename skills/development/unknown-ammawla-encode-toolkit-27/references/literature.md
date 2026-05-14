# ClinVar Annotation — Literature References

**Last updated:** 2026-03-07
**Purpose:** Reference catalog for the clinvar-annotation skill — key papers informing variant clinical significance classification, curation standards, and database resources for clinical genomics.

---

## Database Resources

---

### Landrum et al. 2018 — ClinVar: improving access to variant interpretations

- **Citation:** Landrum MJ, Lee JM, Benson M, Brown GR, Chao C, Chitipiralla
  S, Gu B, Hart J, Hoffman D, Jang W, et al. ClinVar: improving access to
  variant interpretations and supporting evidence. Nucleic Acids Research,
  46(D1):D1062-D1067, 2018.
- **DOI:** [10.1093/nar/gkx1153](https://doi.org/10.1093/nar/gkx1153)
- **PMID:** 29165669 | **PMC:** PMC5753237
- **Citations:** ~2,000
- **Key findings:** Described the ClinVar database infrastructure for
  aggregating variant-disease interpretations submitted by clinical
  laboratories, research groups, expert panels, and professional societies.
  ClinVar uses a star-based review status system reflecting evidence quality:
  0 stars (single submitter, no assertion criteria provided), 1 star (single
  submitter with criteria), 2 stars (multiple submitters with no conflicts), 3
  stars (reviewed by expert panel), and 4 stars (practice guideline).
  Approximately 12% of variants with multiple submissions have conflicting
  interpretations, highlighting the inherent difficulty of variant
  classification and the importance of checking review status rather than
  relying on a single interpretation. The database tracks interpretation
  changes over time through versioned submissions, enabling laboratories to
  monitor whether their classifications have been superseded by newer evidence
  — a critical feature for clinical genomics where variant reclassification
  can alter patient management.

---

### Harrison et al. 2021 — ClinVar 2021: public archive of variant interpretations

- **Citation:** Harrison SM, Biesecker LG, Rehm HL. ClinVar as a resource to
  track and share variant interpretations. Current Protocols, 1(12):e315,
  2021.
- **DOI:** [10.1002/cpz1.315](https://doi.org/10.1002/cpz1.315)
- **PMID:** 34964606 | **PMC:** PMC8858745
- **Citations:** ~500
- **Key findings:** Documented ClinVar's growth to >1.7 million unique
  variants with >2.3 million submitted interpretations as of 2021, with
  submission rates accelerating as clinical next-generation sequencing becomes
  standard of care. Detailed the variant aggregation algorithm that assigns an
  overall "review status" and "aggregate classification" when multiple
  submitters report on the same variant, automatically flagging conflicting
  interpretations for attention. Provided practical guidance for integrating
  ClinVar into variant annotation pipelines, including the critical
  distinction between GRCh37 and GRCh38 coordinate systems (variants must be
  queried in the correct assembly), the importance of checking submission
  dates (older submissions may use outdated classification criteria), and the
  use of ClinVar's XML or VCF downloads for high-throughput annotation. Also
  documented the E-utilities API (esearch/efetch with db=clinvar) and the
  Variation Services API for programmatic access.

---

## Classification Standards

---

### Richards et al. 2015 — ACMG/AMP standards for variant interpretation

- **Citation:** Richards S, Aziz N, Bale S, Bick D, Das S, Gastier-Foster J,
  Grody WW, Hegde M, Lyon E, Spector E, Voelkerding K, Rehm HL, ACMG
  Laboratory Quality Assurance Committee. Standards and guidelines for the
  interpretation of sequence variants: a joint consensus recommendation of the
  American College of Medical Genetics and Genomics and the Association for
  Molecular Pathology. Genetics in Medicine, 17(5):405-424, 2015.
- **DOI:** [10.1038/gim.2015.30](https://doi.org/10.1038/gim.2015.30)
- **PMID:** 25741868 | **PMC:** PMC4544753
- **Citations:** ~8,000
- **Key findings:** Established the five-tier classification system used
  universally in clinical genetics: pathogenic (P), likely pathogenic (LP),
  variant of uncertain significance (VUS), likely benign (LB), and benign (B).
  Defined 28 weighted evidence criteria organized by strength — very strong
  (PVS1: null variant in a gene where LoF is a known disease mechanism),
  strong (PS1-PS4), moderate (PM1-PM6), and supporting (PP1-PP5) for
  pathogenicity, with corresponding benign criteria (BA1, BS1-BS4, BP1-BP7).
  These criteria are combined using a semi-quantitative Bayesian-inspired
  framework: pathogenic requires either 1 very strong + 1 strong, 2 strong, 1
  strong + 3 supporting, or other defined combinations. These guidelines are
  the foundation of virtually all ClinVar submissions, though they were
  designed primarily for rare Mendelian disease variants and require
  adaptation for complex disease, pharmacogenomic, somatic cancer, and
  regulatory variants relevant to ENCODE.

---

### Nykamp et al. 2017 — Sherloc: comprehensive variant classification framework

- **Citation:** Nykamp K, Anderson M, Powers M, Garcia J, Herber B, Kim YH,
  Ferber M, Lebo M, Seidman C, Seidman J, et al. Sherloc: a comprehensive
  refinement of the ACMG-AMP variant classification criteria. Genetics in
  Medicine, 19(10):1105-1117, 2017.
- **DOI:** [10.1038/gim.2017.37](https://doi.org/10.1038/gim.2017.37)
- **PMID:** 28492532 | **PMC:** PMC5632834
- **Citations:** ~600
- **Key findings:** Sherloc (Semiquantitative, Hierarchical Evidence-based
  Rules for Locus interpretation) refined the ACMG/AMP criteria by assigning
  explicit numerical point values to each evidence type, enabling transparent
  quantitative combination rather than the original qualitative counting
  rules. Subdivided several broad ACMG categories into more granular tiers —
  for example, splitting functional evidence (PS3) into tiers based on assay
  validation level: well-validated functional assays in established cell
  models receive more points than reporter assays or computational
  predictions. Demonstrated that quantitative scoring reduces inter-analyst
  variability from ~80% concordance with standard ACMG to >90% concordance
  with Sherloc, directly addressing the "conflicting interpretations" problem
  in ClinVar. The framework is particularly valuable for ClinVar submitters
  because it produces transparent, auditable classification logic where the
  contribution of each evidence type to the final classification can be traced
  and reviewed.

---

### Plon et al. 2008 — IARC classification system for sequence variants

- **Citation:** Plon SE, Eccles DM, Easton D, Foulkes WD, Genuardi M,
  Greenblatt MS, Hogervorst FB, Hoogerbrugge N, Lancaster JM, Nathanson KL, et
  al. Sequence variant classification and reporting: recommendations for
  improving the interpretation of cancer susceptibility genetic test results.
  Human Mutation, 29(11):1282-1291, 2008.
- **DOI:** [10.1002/humu.20880](https://doi.org/10.1002/humu.20880)
- **PMID:** 18951446 | **PMC:** PMC3075918
- **Citations:** ~1,200
- **Key findings:** Established the IARC five-class system for classifying
  variants in cancer susceptibility genes with explicit posterior probability
  thresholds: Class 5 (definitely pathogenic, >0.99 posterior probability),
  Class 4 (likely pathogenic, 0.95-0.99), Class 3 (uncertain, 0.05-0.949),
  Class 2 (likely not pathogenic/little clinical significance, 0.001-0.049),
  Class 1 (not pathogenic/no clinical significance, <0.001). The probability
  thresholds were derived from formal clinical decision theory, balancing the
  consequences of false-positive classification (unnecessary prophylactic
  surgery, surveillance, psychological burden) against false-negative
  classification (missed cancer prevention opportunities). This framework
  preceded and directly influenced the ACMG/AMP 2015 guidelines, establishing
  two critical principles: (1) variant classification is inherently
  probabilistic, not binary, and (2) "uncertain" is a legitimate and important
  classification reflecting genuine epistemic uncertainty rather than
  analytical failure. The IARC system remains the standard for hereditary
  cancer gene variant classification in ClinVar, applied by expert panels for
  BRCA1/2, MMR genes, and TP53.

---

## Curation Infrastructure

---

### Rehm et al. 2015 — ClinGen: authoritative central resource for clinical genomics

- **Citation:** Rehm HL, Berg JS, Brooks LD, Bustamante CD, Evans JP, Landrum
  MJ, Ledbetter DH, Maglott DR, Martin CL, Nussbaum RL, et al. ClinGen — the
  Clinical Genome Resource. New England Journal of Medicine,
  372(23):2235-2242, 2015.
- **DOI:** [10.1056/NEJMsr1406261](https://doi.org/10.1056/NEJMsr1406261)
- **PMID:** 26014595 | **PMC:** PMC4474187
- **Citations:** ~1,500
- **Key findings:** Introduced the Clinical Genome Resource (ClinGen) as an
  NIH-funded initiative to build an authoritative resource defining the
  clinical relevance of genes and variants for precision medicine. ClinGen
  operates through two types of expert panels: Gene Curation Expert Panels
  (GCEPs) that assess gene-disease validity on a scale from Definitive to
  Disputed using a semi-quantitative scoring matrix, and Variant Curation
  Expert Panels (VCEPs) that apply ACMG/AMP criteria with gene-specific
  modifications. Gene-disease validity assessments systematically evaluate
  genetic evidence (case-level variant data, segregation studies, case-control
  statistics) and experimental evidence (functional assays, animal models,
  rescue experiments). ClinGen expert panel reviews represent the highest tier
  of variant curation (4-star review status in ClinVar) and are increasingly
  recognized as the reference standard by clinical laboratories — when a
  ClinGen VCEP publishes a variant classification, it supersedes individual
  laboratory submissions.

---

### Riggs et al. 2020 — ClinGen CNV classification framework

- **Citation:** Riggs ER, Andersen EF, Cherry AM, Kantarci S, Kearney H, Patel
  A, Raca G, Ritter DI, South ST, Thorland EC, et al. Technical standards for
  the interpretation and reporting of constitutional copy-number variants: a
  joint consensus recommendation of the American College of Medical Genetics
  and Genomics (ACMG) and the Clinical Genome Resource (ClinGen). Genetics in
  Medicine, 22(2):245-257, 2020.
- **DOI:** [10.1038/s41436-019-0686-8](https://doi.org/10.1038/s41436-019-0686-8)
- **PMID:** 31690835 | **PMC:** PMC7313390
- **Citations:** ~1,000
- **Key findings:** Extended the ACMG/AMP variant interpretation framework to
  copy number variants (CNVs), addressing a critical gap since the 2015
  guidelines were designed primarily for sequence variants (SNVs, small
  indels). Introduced a quantitative scoring system with evidence categories
  specific to CNVs: genomic content (number of protein-coding genes
  encompassed, presence of known haploinsufficiency or triplosensitivity
  genes), overlap with established pathogenic/benign CNV regions, and clinical
  evidence (published case reports, segregation data, de novo occurrence). The
  framework distinguishes between deletions and duplications, recognizing that
  haploinsufficiency and triplosensitivity have fundamentally different
  pathogenic mechanisms and evidence requirements. ClinGen dosage sensitivity
  curation groups apply these standards to evaluate genes and genomic regions
  for copy number sensitivity, directly informing ClinVar CNV classifications
  and enabling ENCODE regulatory element annotations to be interpreted in the
  context of CNV pathogenicity — a regulatory enhancer deletion encompassing a
  dosage-sensitive gene is more likely pathogenic.

---
