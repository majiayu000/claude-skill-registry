# gnomAD Variants — Literature References

**Last updated:** 2026-03-07
**Purpose:** Reference catalog for the gnomad-variants skill — key papers informing population allele frequency databases, gene constraint metrics, structural variant catalogs, and their application to interpreting regulatory variation in ENCODE-annotated genomic regions.

---

## Core gnomAD Releases

---

### Karczewski et al. 2020 — gnomAD v2: mutational constraint across 141,456 exomes

- **Citation:** Karczewski KJ, Francioli LC, Tiao G, Cummings BB, Alfoldi J,
  Wang Q, Collins RL, Laricchia KM, Ganna A, Birnbaum DP, et al. The
  mutational constraint spectrum quantified from variation in 141,456 humans.
  Nature, 581(7809):434-443, 2020.
- **DOI:** [10.1038/s41586-020-2308-7](https://doi.org/10.1038/s41586-020-2308-7)
- **PMID:** 32461654 | **PMC:** PMC7334197
- **Citations:** ~5,000
- **Key findings:** The gnomAD v2 release aggregated exome sequencing from
  141,456 individuals and whole-genome sequencing from 15,708 individuals
  across 8 biogeographic ancestry groups (African/African American, Amish,
  Latino/Admixed American, Ashkenazi Jewish, East Asian, Finnish, Non-Finnish
  European, South Asian). Introduced the LOEUF (Loss-of-function
  Observed/Expected Upper bound Fraction) metric as a continuous measure of
  gene constraint, replacing the binary pLI score. LOEUF ranges from 0 (highly
  constrained, essentially no observed loss-of-function variants despite
  expectation) to >1 (tolerant of LoF), with the most constrained decile
  (LOEUF < 0.35) enriched 11-fold for established haploinsufficiency disease
  genes. For ENCODE data interpretation, gnomAD enables filtering variants
  overlapping regulatory elements by population frequency — variants found at
  >1% frequency in any population are generally benign per ACMG criteria,
  while ultra-rare variants in constrained genes' regulatory regions represent
  the highest-priority candidates for functional characterization.

---

### Lek et al. 2016 — ExAC: analysis of protein-coding variation in 60,706 humans

- **Citation:** Lek M, Karczewski KJ, Minikel EV, Samocha KE, Banks E, Fennell
  T, O'Donnell-Luria AH, Ware JS, Hill AJ, Cummings BB, et al. Analysis of
  protein-coding genetic variation in 60,706 humans. Nature,
  536(7616):285-291, 2016.
- **DOI:** [10.1038/nature19057](https://doi.org/10.1038/nature19057)
- **PMID:** 27535533 | **PMC:** PMC5018207
- **Citations:** ~7,000
- **Key findings:** The Exome Aggregation Consortium (ExAC), direct precursor
  to gnomAD, aggregated 60,706 exomes and cataloged 10 million genetic
  variants including 3.2 million never previously observed. Demonstrated that
  each individual genome carries ~100 genuine loss-of-function (LoF) variants,
  ~20 of which are homozygous — meaning that natural human "knockouts" exist
  for thousands of genes. Introduced the pLI (probability of being loss-of-
  function intolerant) metric: genes with pLI > 0.9 are significantly depleted
  for LoF variants relative to neutral expectation, identifying 3,230 LoF-
  intolerant genes enriched for known disease genes and essential cellular
  functions. ExAC established the fundamental paradigm that population allele
  frequency is the single most informative annotation for clinical variant
  interpretation — a variant observed in thousands of apparently healthy
  individuals is overwhelmingly likely to be benign regardless of its
  computational pathogenicity prediction.

---

### Chen et al. 2024 — gnomAD v4: expanded diversity and non-coding constraint

- **Citation:** Chen S, Francioli LC, Goodrich JK, Collins RL, Kanai M, Wang
  Q, Alfoldi J, Watts NA, Vittal C, Gauthier LD, et al. A genomic mutational
  constraint map using variation in 76,156 human genomes. Nature,
  625(7993):92-100, 2024.
- **DOI:** [10.1038/s41586-023-06045-0](https://doi.org/10.1038/s41586-023-06045-0)
- **PMID:** 38057664 | **PMC:** PMC10764060
- **Citations:** ~200
- **Key findings:** gnomAD v4 expanded to 807,162 exomes and 76,215 whole
  genomes with substantially improved global population diversity — including
  the largest cohorts to date of Middle Eastern (4,513), South Asian (20,969),
  and East Asian (20,950) individuals, partially addressing the historical
  Eurocentric bias of previous releases. The landmark contribution was
  extension of mutational constraint analysis from coding regions to the non-
  coding genome, identifying 4.2% of non-coding sequence under significant
  purifying selection based on depletion of rare variants relative to neutral
  expectation. These non-coding constrained regions are highly enriched for
  ENCODE-annotated enhancers, CTCF binding sites, and ultraconserved elements,
  providing independent population-genetic validation that ENCODE functional
  annotations identify biologically important regulatory elements. The non-
  coding constraint scores enable the gnomad-variants skill to prioritize
  ENCODE regulatory regions not just by chromatin state but by evolutionary
  intolerance to mutation — a constrained enhancer carrying a rare variant is
  a far higher priority for functional follow-up than an unconstrained one.

---

## Structural Variants

---

### Collins et al. 2020 — gnomAD structural variant resource

- **Citation:** Collins RL, Brand H, Karczewski KJ, Zhao X, Alfoldi J,
  Francioli LC, Khera AV, Lowber C, Gauthier LD, Wang H, et al. A structural
  variation reference for medical and population genetics. Nature,
  581(7809):444-451, 2020.
- **DOI:** [10.1038/s41586-020-2287-8](https://doi.org/10.1038/s41586-020-2287-8)
- **PMID:** 32461652 | **PMC:** PMC7334194
- **Citations:** ~1,500
- **Key findings:** Generated a population reference of 433,371 structural
  variants (SVs) from 14,891 gnomAD whole genomes, cataloging deletions
  (179,396), duplications (47,637), insertions (130,227), inversions (786),
  multiallelic complex SVs (5,765), and other complex rearrangements.
  Demonstrated that SVs contribute 25% of all rare protein-altering variants
  per individual despite being individually far less frequent than single-
  nucleotide variants, yet they have been historically underrepresented in
  functional genomic analyses. Showed that SVs disrupting ENCODE-annotated
  regulatory elements — particularly enhancers, CTCF insulator sites, and
  promoters — are under strong purifying selection distinct from selection
  patterns at coding SVs, with common SVs rarely deleting conserved enhancers.
  The gnomAD-SV dataset enables assessment of whether ENCODE-identified
  regulatory elements are disrupted by common structural variants in the
  population, providing a critical filter: regulatory elements frequently
  deleted in healthy populations are less likely to be essential.

---

## Clinical Application

---

### Gudmundsson et al. 2022 — Practical variant interpretation using gnomAD

- **Citation:** Gudmundsson S, Singer-Berk M, Watts NA, Phu W, Goodrich JK,
  Solomonson M, et al. Variant interpretation using population databases:
  Lessons from gnomAD. Human Mutation, 43(8):1012-1030, 2022.
- **DOI:** [10.1002/humu.24309](https://doi.org/10.1002/humu.24309)
- **PMID:** 34859531 | **PMC:** PMC9160216
- **Citations:** ~300
- **Key findings:** Comprehensive practical guide to using gnomAD for variant
  interpretation in clinical genetics and research settings, covering the
  gnomAD v3.1 whole-genome dataset (76,156 genomes) with improved
  representation of non-European populations. Provided detailed guidance on
  quality filtering — using site-level filters (PASS vs. filtered), allele
  balance for heterozygous calls, genotype quality scores, and read depth
  thresholds — essential for avoiding false-positive variant calls that can
  mislead downstream analyses. Addressed the critical issue of population-
  specific allele frequency interpretation: a variant at 0.5% in African
  populations but absent in European populations may be incorrectly classified
  as "rare" if only European reference data is consulted. Detailed the
  "frequency as benign evidence" framework: under ACMG criteria, a variant
  present at >0.1% (allele frequency > 0.001) in any gnomAD population can be
  classified as likely benign for rare Mendelian conditions (BA1 criterion),
  making gnomAD population frequency the most widely applied single piece of
  evidence in clinical variant classification.

---

### Whiffin et al. 2017 — Using variant frequencies to inform clinical decisions

- **Citation:** Whiffin N, Minikel E, Walsh R, O'Donnell-Luria AH, Karczewski
  K, Ing AY, Barber PJF, Ing A, Thomson KL, Consortium TE, et al. Using high-
  resolution variant frequencies to empower clinical genome interpretation.
  Genetics in Medicine, 19(10):1151-1158, 2017.
- **DOI:** [10.1038/gim.2017.26](https://doi.org/10.1038/gim.2017.26)
- **PMID:** 28518168 | **PMC:** PMC5633148
- **Citations:** ~800
- **Key findings:** Developed a formal statistical framework for calculating
  the maximum credible population allele frequency (AF) for a pathogenic
  variant, based on disease-specific parameters: maximum credible AF =
  (prevalence x maximum allelic contribution x 1/penetrance) / 2. For example,
  a dominant disease with 1 in 10,000 prevalence, 10% genetic heterogeneity
  (maximum allelic contribution = 0.1), and 50% penetrance has a maximum
  credible AF of 0.001% — any variant exceeding this frequency in gnomAD can
  be confidently filtered as too common to cause the condition. This disease-
  specific thresholding is far more powerful than a single universal frequency
  cutoff because rare diseases tolerate lower-frequency variants while common
  pharmacogenomic variants can exist at much higher frequencies. The framework
  is directly applicable to the gnomad-variants skill when filtering variants
  that overlap ENCODE regulatory elements: population frequency thresholds
  should be calibrated to the disease being studied rather than using a fixed
  1% or 0.1% cutoff.

---

## Complementary Resources

---

### Wang et al. 2021 — Rare variant contribution to disease in UK Biobank

- **Citation:** Wang Q, Dhindsa RS, Carss K, Harper AR, Nag A, Tachmazidou I,
  Vitsios D, Deevi SVV, Mackay A, Muthas D, et al. Rare variant contribution
  to human disease in 281,104 UK Biobank exomes. Nature, 597(7877):527-532,
  2021.
- **DOI:** [10.1038/s41586-021-03855-y](https://doi.org/10.1038/s41586-021-03855-y)
- **PMID:** 34375979 | **PMC:** PMC8459922
- **Citations:** ~500
- **Key findings:** Analyzed 281,104 UK Biobank exomes to identify rare
  variant associations with 7,994 phenotypes using gene-burden tests that
  aggregate the effects of rare predicted loss-of-function and damaging
  missense variants across individuals within each gene. Discovered 564
  significant gene-phenotype associations, of which 301 (53%) were novel —
  demonstrating that rare variant analysis provides substantial gene discovery
  power complementary to common variant GWAS. Genes identified through rare
  variant burden tests were enriched in ENCODE-defined regulatory hotspots
  (regions with multiple overlapping histone modification and TF binding
  annotations) and were disproportionately represented among known drug
  targets, suggesting that genes under strong regulatory control are more
  likely to be therapeutically relevant. This study established the value of
  combining rare variant association analysis with ENCODE regulatory
  annotations: rare non-coding variants disrupting conserved enhancer elements
  or TF binding sites within gene regulatory regions can be included in burden
  tests to increase statistical power beyond coding variants alone.

---
