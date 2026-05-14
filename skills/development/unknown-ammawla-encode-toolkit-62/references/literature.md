# Regulatory Elements — Literature References

**Last updated:** 2026-03-07
**Purpose:** Reference catalog for the regulatory-elements skill — key papers defining candidate
cis-regulatory elements (cCREs), DNase hypersensitive sites, enhancer identification,
enhancer-gene linkage, chromatin state annotation, and in vivo validation approaches that inform
the identification and characterization of regulatory elements from ENCODE data.

The regulatory-elements skill helps users identify, classify, and interpret non-coding regulatory
elements using ENCODE data. The field has evolved from individual enhancer discoveries to
genome-wide catalogs of >900,000 human cCREs. These elements are defined by chromatin
accessibility, histone modifications, and transcription factor binding, classified into promoters,
enhancers (proximal and distal), insulators, and silencers.

These 10 papers are organized into five thematic groups: (1) the ENCODE cCRE registry that
provides the current classification system, (2) chromatin accessibility landscapes that form the
foundation of regulatory element identification, (3) enhancer-gene linkage methods, (4) histone
modification signatures and chromatin state models, and (5) cross-species conservation and
in vivo validation.

---

## ENCODE cCRE Registry

The cCRE registry is the current standard for regulatory element classification in ENCODE.
It replaces earlier ad hoc catalogs with a unified, reproducible classification based on four
signal types: DNase accessibility, H3K4me3, H3K27ac, and CTCF. Understanding how cCREs are
defined and classified is essential for interpreting search results and selecting appropriate
ENCODE experiments for regulatory element analysis.

---

### Moore et al. 2020 — Defining 926,535 candidate cis-regulatory elements

- **Citation:** Moore JE, Purcaro MJ, Pratt HE, Epstein CB, Shoresh N, et al. Expanded
  encyclopaedias of DNA elements in the human and mouse genomes. *Nature*, 583(7818),
  699-710, 2020.
- **DOI:** [10.1038/s41586-020-2493-4](https://doi.org/10.1038/s41586-020-2493-4)
- **PMID:** 32728248 | **PMC:** PMC7410830
- **Citations:** ~1,500
- **Key findings:** Defined the ENCODE cCRE classification system with five groups:
  - PLS: promoter-like signatures (high DNase + H3K4me3), 36,573 human elements
  - pELS: proximal enhancer-like (<2kb from TSS, high DNase + H3K27ac), 52,998
  - dELS: distal enhancer-like (>2kb from TSS, high DNase + H3K27ac), 544,491
  - CTCF-only: high DNase + CTCF, low H3K4me3 and H3K27ac, 117,440
  - DNase-H3K4me3: high DNase + H3K4me3, low H3K27ac, 175,033

  Each cCRE has cell-type-specific activity assignments based on signal levels across
  biosamples. The regulatory-elements skill uses this five-group classification as its
  primary organizational framework, directing users to appropriate ENCODE assay combinations
  for identifying each element type.

---

### Luo et al. 2020 — cCRE registry architecture and portal implementation

- **Citation:** Luo Y, Hitz BC, Gabdank I, Hilton JA, Kagda MS, et al. New developments on
  the Encyclopedia of DNA Elements (ENCODE) data portal. *Nucleic Acids Research*, 48(D1),
  D882-D889, 2020.
- **DOI:** [10.1093/nar/gkz1062](https://doi.org/10.1093/nar/gkz1062)
- **PMID:** 31713622 | **PMC:** PMC7061942
- **Citations:** ~800
- **Key findings:** Described the cCRE registry implementation on the ENCODE portal, including
  element-centric search by accession (EH38E prefix for GRCh38), genomic coordinates, or
  activity state across cell types. The classification uses a decision tree: first requires
  high DNase signal, then branches on H3K4me3 (promoter-like vs. not), H3K27ac (enhancer-like
  vs. not), and CTCF (insulator-like vs. not). The registry includes cell-type activity matrices
  showing active vs. inactive states per biosample. The regulatory-elements skill uses these
  matrices to identify tissue-specific vs. constitutive regulatory elements.

---

## Chromatin Accessibility and DHS Landscape

DNase hypersensitivity is the foundational signal for regulatory element identification — an
element must be accessible to function. The two papers below established the genome-wide DHS
catalog and demonstrated that disease-associated variants concentrate in cell-type-specific
accessible regions.

---

### Thurman et al. 2012 — DNase hypersensitive site catalog across 125 cell types

- **Citation:** Thurman RE, Rynes E, Humbert R, Vierstra J, Maurano MT, et al. The accessible
  chromatin landscape of the human genome. *Nature*, 489(7414), 75-82, 2012.
- **DOI:** [10.1038/nature11232](https://doi.org/10.1038/nature11232)
- **PMID:** 22955617 | **PMC:** PMC3721348
- **Citations:** ~2,800
- **Key findings:** Mapped 2.89 million unique DHS across 125 cell types, revealing that the
  genome contains far more regulatory DNA than coding sequence. Demonstrated that DHSs cluster
  into cell-type-specific modules corresponding to known regulatory programs, and that >80% of
  DHSs are accessible in only a subset of cell types. Only ~5% of DHSs are ubiquitous.
  This paper established chromatin accessibility as the foundation for regulatory element
  discovery, defining the landscape that ENCODE cCREs are built upon.

---

### Maurano et al. 2012 — GWAS variants enriched in DNase hypersensitive sites

- **Citation:** Maurano MT, Humbert R, Rynes E, Thurman RE, et al. Systematic localization of
  common disease-associated variation in regulatory DNA. *Science*, 337(6099),
  1190-1195, 2012.
- **DOI:** [10.1126/science.1222794](https://doi.org/10.1126/science.1222794)
- **PMID:** 22955828 | **PMC:** PMC3771521
- **Citations:** ~3,000
- **Key findings:** Demonstrated that GWAS disease-associated variants concentrate in DHSs with
  cell-type-specific enrichment patterns: type 2 diabetes variants in islet DHSs, autoimmune
  variants in immune cell DHSs, neurological variants in brain DHSs. This cell-type-specific
  enrichment provides the framework for using ENCODE regulatory elements to interpret GWAS
  results. The regulatory-elements skill leverages this principle by enabling overlap analysis
  between variant sets and cell-type-specific cCREs, identifying the cell types most likely
  mediating disease mechanisms.

---

## Enhancer-Gene Linkage

Identifying which gene an enhancer regulates is one of the most challenging problems in
regulatory genomics. Proximity-based methods are imperfect because enhancers can act over
hundreds of kilobases. CRISPRi perturbation provides direct experimental evidence.

---

### Gasperini et al. 2019 — CRISPRi-based enhancer-gene mapping at scale

- **Citation:** Gasperini M, Hill AJ, McFaline-Figueroa JL, Martin B, et al. A genome-wide
  framework for mapping gene regulation via cellular genetic screens. *Cell*, 176(1-2),
  377-390, 2019.
- **DOI:** [10.1016/j.cell.2018.11.029](https://doi.org/10.1016/j.cell.2018.11.029)
- **PMID:** 30612741 | **PMC:** PMC6435518
- **Citations:** ~700
- **Key findings:** Applied CRISPRi to perturb 5,920 candidate enhancers in K562 cells,
  identifying 664 enhancer-gene pairs at single-element resolution. Key findings:
  - Most enhancers regulate only 1-2 genes
  - The target is often but not always the nearest gene
  - Some enhancers affect genes >1 Mb away
  - ~20% of tested enhancers had no detectable effect on nearby gene expression

  This provides ground-truth data for validating computational predictions. The
  regulatory-elements skill references these validated links as benchmarks and recommends
  CRISPRi data (available in ENCODE for selected biosamples) for confirming predicted targets.

---

## Enhancer Discovery and Histone Signatures

Before the cCRE registry, enhancers were identified by their histone modification signatures.
These foundational papers established the mark combinations that define different regulatory
element classes and remain the conceptual basis for the cCRE classification.

---

### Heintzman et al. 2007 — Histone signatures distinguishing promoters from enhancers

- **Citation:** Heintzman ND, Stuart RK, Hon G, Fu Y, et al. Distinct and predictive chromatin
  signatures of transcriptional promoters and enhancers in the human genome. *Nature
  Genetics*, 39(3), 311-318, 2007.
- **DOI:** [10.1038/ng1966](https://doi.org/10.1038/ng1966)
- **PMID:** 17277777
- **Citations:** ~2,800
- **Key findings:** Established the foundational histone signature model:
  - Promoters: H3K4me3 high, H3K4me1 low
  - Enhancers: H3K4me1 high, H3K4me3 low
  - Later refined with H3K27ac: active vs. poised enhancers

  This two-mark model remains the basis for enhancer identification in ENCODE data and
  directly informs the cCRE classification. The regulatory-elements skill uses this signature
  hierarchy: H3K4me1+/H3K27ac+ = active enhancer, H3K4me1+/H3K27ac- = poised enhancer,
  H3K4me3+/H3K27ac+ = active promoter.

---

### Ernst et al. 2011 — ChromHMM states mapping regulatory element classes

- **Citation:** Ernst J, Kheradpour P, Mikkelsen TS, Shoresh N, et al. Mapping and analysis of
  chromatin state dynamics in nine human cell types. *Nature*, 473(7345), 43-49, 2011.
- **DOI:** [10.1038/nature09906](https://doi.org/10.1038/nature09906)
- **PMID:** 21441907 | **PMC:** PMC3088773
- **Citations:** ~3,500
- **Key findings:** Applied ChromHMM to nine ENCODE cell types using nine histone marks,
  defining 15 chromatin states that partition the genome into functional categories:
  active promoter, poised promoter, strong enhancer, weak enhancer, insulator, transcribed,
  Polycomb repressed, and heterochromatin. Demonstrated that chromatin states predict gene
  expression levels, conservation, and cell-type-specific activity with high accuracy. The
  regulatory-elements skill maps ENCODE cCREs to ChromHMM states to provide functional
  context and increase confidence in element classification.

---

## Cross-Species Conservation and Validation

Regulatory elements evolve more rapidly than coding sequences. Cross-species comparison reveals
which elements are under constraint (functionally essential) and which are lineage-specific.
In vivo validation provides the gold standard for confirming enhancer function.

---

### Shen et al. 2012 — Mouse ENCODE regulatory landscape

- **Citation:** Shen Y, Yue F, McCleary DF, Ye Z, et al. A map of the cis-regulatory
  sequences in the mouse genome. *Nature*, 488(7409), 116-120, 2012.
- **DOI:** [10.1038/nature11243](https://doi.org/10.1038/nature11243)
- **PMID:** 22763441 | **PMC:** PMC4041622
- **Citations:** ~1,200
- **Key findings:** Generated enhancer, promoter, and insulator maps across 19 mouse tissues.
  Found that while promoters are highly conserved between human and mouse, enhancers show
  rapid evolutionary turnover — only ~50% of mouse enhancers have conserved human counterparts
  with equivalent activity. This has major implications: sequence conservation alone is
  insufficient for predicting enhancer function across species. The regulatory-elements skill
  warns that mouse ENCODE annotations do not directly transfer to human and recommends
  tissue-matched human data when available.

---

### Andersson et al. 2014 — CAGE-defined enhancer atlas with bidirectional transcription

- **Citation:** Andersson R, Gebhard C, Miguel-Escalada I, et al. An atlas of active enhancers
  across human cell types and tissues. *Nature*, 507(7493), 455-461, 2014.
- **DOI:** [10.1038/nature12787](https://doi.org/10.1038/nature12787)
- **PMID:** 24670763 | **PMC:** PMC5215096
- **Citations:** ~1,500
- **Key findings:** Used CAGE across 808 human samples (FANTOM5) to identify 43,011 active
  enhancers defined by bidirectional eRNA transcription — a chromatin-independent measure of
  enhancer activity. Demonstrated that eRNA production is a reliable indicator of enhancer
  activity independent of histone state. Combining ENCODE cCRE annotations with FANTOM5
  CAGE data increases confidence in enhancer calls. The regulatory-elements skill recommends
  this integration when high-confidence enhancer identification is required.

---

### Visel et al. 2009 — In vivo enhancer validation with transgenic reporters

- **Citation:** Visel A, Blow MJ, Li Z, Zhang T, et al. ChIP-seq accurately predicts
  tissue-specific activity of enhancers. *Nature*, 457(7231), 854-858, 2009.
- **DOI:** [10.1038/nature07730](https://doi.org/10.1038/nature07730)
- **PMID:** 19212405 | **PMC:** PMC2745234
- **Citations:** ~2,000
- **Key findings:** Validated ChIP-seq-predicted enhancers using transgenic mouse reporter
  assays (lacZ), demonstrating ~80% accuracy for tissue-specific activity prediction.
  Tested 86 predicted enhancers, 75 (87%) drove tissue-specific expression matching
  predictions. Established the Vista Enhancer Browser (>2,000 validated enhancers) as a
  community resource. This paper provides experimental validation that ChIP-seq-based
  enhancer predictions (the basis of ENCODE cCREs) are biologically meaningful. The
  regulatory-elements skill references Vista-validated enhancers as gold-standard benchmarks.

---
