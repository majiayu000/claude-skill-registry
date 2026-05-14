# Publication Trust — Literature References

**Last updated:** 2026-03-07
**Purpose:** Reference catalog for the publication-trust skill — papers on research reproducibility, publication quality assessment, image integrity, retraction patterns, and assay-specific quality standards used to evaluate the trustworthiness of genomic studies.

---

## Reproducibility and Research Quality

### Ioannidis 2005 — Why most published research findings are false

- **Citation:** Ioannidis JPA. Why most published research findings are false. *PLoS Medicine*, 2(8), e124, 2005.
- **DOI:** [10.1371/journal.pmed.0020124](https://doi.org/10.1371/journal.pmed.0020124)
- **PMID:** 16060722 | **PMC:** PMC1182327
- **Citations:** ~10,000
- **Key findings:** Demonstrated mathematically that for most study designs and settings, the probability that a research claim is true depends on study power, bias, and the pre-study odds of the hypothesis being true. When studies are small, effect sizes are small, there are many tested relationships, or there is flexibility in designs and outcomes, most published findings are likely false. This paper is the foundational reference for understanding why publication quality assessment is necessary, and it motivates the critical evaluation framework used by the publication-trust skill.

---

### Baker 2016 — 1,500 scientists on reproducibility

- **Citation:** Baker M. 1,500 scientists lift the lid on reproducibility. *Nature*, 533(7604), 452-454, 2016.
- **DOI:** [10.1038/533452a](https://doi.org/10.1038/533452a)
- **PMID:** 27225100
- **Citations:** ~3,200
- **Key findings:** Reported results from a Nature survey where more than 70% of 1,576 researchers had tried and failed to reproduce another scientist's experiments, and more than half had failed to reproduce their own. Selective reporting, pressure to publish, and insufficient documentation were cited as key factors. This survey provides empirical evidence for the scale of the reproducibility problem and underscores why the publication-trust skill evaluates methodological rigor, sample sizes, and statistical reporting.

---

### Steen et al. 2013 — Retraction patterns in biomedical literature

- **Citation:** Steen RG, Casadevall A, Fang FC. Why has the number of scientific retractions increased? *PLoS ONE*, 8(7), e68397, 2013.
- **DOI:** [10.1371/journal.pone.0068397](https://doi.org/10.1371/journal.pone.0068397)
- **PMID:** 23874614 | **PMC:** PMC3715440
- **Citations:** ~500
- **Key findings:** Analyzed 2,047 retracted biomedical and life-science articles indexed in PubMed and found that the increase in retractions was due to both increased scrutiny and an increase in the fraction of articles requiring retraction. Fraud accounted for 43% of retractions, with duplicate publication (14%) and plagiarism (10%) also prominent. Understanding retraction patterns helps the publication-trust skill identify red flags in cited literature and provides context for why automated quality checks are valuable.

---

### Bik et al. 2016 — Image manipulation in published papers

- **Citation:** Bik EM, Casadevall A, Fang FC. The prevalence of inappropriate image duplication in biomedical research publications. *mBio*, 7(3), e00809-16, 2016.
- **DOI:** [10.1128/mBio.00809-16](https://doi.org/10.1128/mBio.00809-16)
- **PMID:** 27273827 | **PMC:** PMC4916379
- **Citations:** ~400
- **Key findings:** Screened 20,621 papers from 40 journals and found that 3.8% contained problematic figures with inappropriately duplicated images, with about half of these representing deliberate manipulation. The prevalence was consistent across journals and over time. This work highlights a specific category of research integrity issues that the publication-trust skill should flag when evaluating experimental evidence, particularly for studies claiming novel functional genomic findings.

---

## Assay-Specific Quality Standards

### Conesa et al. 2016 — RNA-seq best practices survey

- **Citation:** Conesa A, Madrigal P, Tarazona S, Gomez-Cabrero D, Cervera A, McPherson A, Szczesniak MW, Gaffney DJ, Elo LL, Zhang X, Mortazavi A. A survey of best practices for RNA-seq data analysis. *Genome Biology*, 17, 13, 2016.
- **DOI:** [10.1186/s13059-016-0881-8](https://doi.org/10.1186/s13059-016-0881-8)
- **PMID:** 26813401 | **PMC:** PMC4728800
- **Citations:** ~2,500
- **Key findings:** Provided comprehensive guidelines for RNA-seq experimental design and analysis, covering read depth, replication, alignment, quantification, normalization, differential expression, and quality control metrics. Recommended mapping rates above 80%, rRNA contamination below 10%, and replicate correlations of 0.9 or higher. These benchmarks are used by the publication-trust skill to evaluate whether RNA-seq studies citing ENCODE data meet minimum quality standards.

---

### Landt et al. 2012 — ChIP-seq quality guidelines

- **Citation:** Landt SG, Marinov GK, Kundaje A, Kheradpour P, Pauli F, Batzoglou S, Bernstein BE, Bickel P, Brown JB, Cayting P, Chen Y, DeSalvo G, Epstein C, Fisher-Aylor KI, Euskirchen G, Gerstein M, Gertz J, Hartemink AJ, Hoffman MM, Iyer VR, Jung YL, Karmakar S, Kellis M, Kharchenko PV, Li Q, Liu T, Liu XS, Ma L, Miber A, Morrison A, Mnoz D, Myers RM, Park PJ, Pazin MJ, Perry MD, Raha D, Reddy TE, Rozowsky J, Shoresh N, Sidow A, Slattery M, Stamatoyannopoulos JA, Tolstorukov MY, White KP, Xi S, Farnham PJ, Green RD, Hager GL, Spencer V, Snyder M. ChIP-seq guidelines and practices of the ENCODE and modENCODE consortia. *Genome Research*, 22(9), 1813-1831, 2012.
- **DOI:** [10.1101/gr.136184.111](https://doi.org/10.1101/gr.136184.111)
- **PMID:** 22955991 | **PMC:** PMC3431496
- **Citations:** ~3,400
- **Key findings:** Established the ENCODE ChIP-seq quality standards including FRiP (fraction of reads in peaks) of at least 1%, NSC (normalized strand coefficient) above 1.05, RSC (relative strand coefficient) above 0.8, NRF (non-redundant fraction) of at least 0.8, and requirements for biological replication with IDR analysis. These metrics define the gold standard for ChIP-seq quality and are the primary reference for evaluating ChIP-seq experiments in the publication-trust framework.

---

### Amemiya et al. 2019 — ENCODE Blacklist for filtering artifacts

- **Citation:** Amemiya HM, Kundaje A, Boyle AP. The ENCODE Blacklist: identification of problematic regions of the genome. *Scientific Reports*, 9(1), 9354, 2019.
- **DOI:** [10.1038/s41598-019-45839-z](https://doi.org/10.1038/s41598-019-45839-z)
- **PMID:** 31249361 | **PMC:** PMC6597562
- **Citations:** ~1,400
- **Key findings:** Defined genomic regions that produce artifactual signal in functional genomics experiments due to excessive mappability, assembly errors, or problematic repeat content. The blacklist covers regions in human (GRCh38, hg19), mouse (mm10), worm, and fly genomes. Failure to apply the ENCODE Blacklist is a significant quality concern that the publication-trust skill checks for, as peaks or signals in blacklisted regions represent technical artifacts rather than genuine biological signal.

---
