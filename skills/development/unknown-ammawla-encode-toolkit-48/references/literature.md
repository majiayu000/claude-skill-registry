# Variant Annotation — Literature References

**Last updated:** 2026-03-07
**Purpose:** Reference catalog for the variant-annotation skill — papers on variant effect prediction tools, pathogenicity scoring methods, clinical classification standards, and population frequency databases used for interpreting genetic variants in the context of ENCODE regulatory elements.

---

## Variant Effect Prediction Tools

### McLaren et al. 2016 — Ensembl Variant Effect Predictor (VEP)

- **Citation:** McLaren W, Gil L, Hunt SE, Riat HS, Ritchie GRS, Thormann A, Flicek P, Cunningham F. The Ensembl Variant Effect Predictor. *Genome Biology*, 17(1), 122, 2016.
- **DOI:** [10.1186/s13059-016-0974-4](https://doi.org/10.1186/s13059-016-0974-4)
- **PMID:** 27268795 | **PMC:** PMC4893825
- **Citations:** ~4,000
- **Key findings:** Described the Ensembl Variant Effect Predictor (VEP), the most widely used tool for determining the effect of genomic variants on genes, transcripts, and protein sequences. VEP annotates variants with consequence types (missense, splice site, regulatory region), SIFT/PolyPhen predictions, allele frequencies, and regulatory annotations. VEP's ability to annotate variants overlapping ENCODE regulatory elements makes it the primary tool for the variant-annotation skill's regulatory variant analysis.

---

### Wang et al. 2010 — ANNOVAR functional annotation

- **Citation:** Wang K, Li M, Hakonarson H. ANNOVAR: functional annotation of genetic variants from high-throughput sequencing data. *Nucleic Acids Research*, 38(16), e164, 2010.
- **DOI:** [10.1093/nar/gkq603](https://doi.org/10.1093/nar/gkq603)
- **PMID:** 20601685 | **PMC:** PMC2938201
- **Citations:** ~8,000
- **Key findings:** Introduced ANNOVAR, a command-line tool for functional annotation of genetic variants detected from diverse genomes. ANNOVAR performs gene-based, region-based, and filter-based annotations and can integrate custom annotation databases including ENCODE regulatory regions. Its high citation count reflects its widespread adoption as a standard variant annotation pipeline component, and it serves as a complementary tool to VEP for comprehensive variant characterization.

---

### Cingolani et al. 2012 — SnpEff and SnpSift

- **Citation:** Cingolani P, Platts A, Wang LL, Coon M, Nguyen T, Wang L, Land SJ, Lu X, Ruden DM. A program for annotating and predicting the effects of single nucleotide polymorphisms, SnpEff: SNPs in the genome of Drosophila melanogaster strain w1118; iso-2; iso-3. *Fly*, 6(2), 80-92, 2012.
- **DOI:** [10.4161/fly.19695](https://doi.org/10.4161/fly.19695)
- **PMID:** 22728672 | **PMC:** PMC3679285
- **Citations:** ~6,000
- **Key findings:** Presented SnpEff, a fast variant annotation and effect prediction tool that classifies variants by their impact (HIGH, MODERATE, LOW, MODIFIER) on gene products. SnpEff can annotate variants using custom interval files including ENCODE-defined regulatory regions. Its companion tool SnpSift enables filtering and manipulation of annotated variant files. Together they provide a lightweight alternative to VEP for pipeline-integrated variant annotation.

---

## Pathogenicity Scoring Methods

### Kircher et al. 2014 — CADD method for variant deleteriousness

- **Citation:** Kircher M, Witten DM, Jain P, O'Roak BJ, Cooper GM, Shendure J. A general framework for estimating the relative pathogenicity of human genetic variants. *Nature Genetics*, 46(3), 310-315, 2014.
- **DOI:** [10.1038/ng.2892](https://doi.org/10.1038/ng.2892)
- **PMID:** 24487276 | **PMC:** PMC3992975
- **Citations:** ~3,000
- **Key findings:** Introduced CADD (Combined Annotation Dependent Depletion), a method that integrates multiple annotations into a single deleteriousness score by contrasting variants that survived natural selection with simulated mutations. CADD scores correlate with allelic diversity, pathogenicity, disease severity, and regulatory effects. The original CADD framework incorporates ENCODE annotations as features, directly linking regulatory element data to variant pathogenicity prediction.

---

### Rentzsch et al. 2019 — CADD v1.4 and GRCh38 support

- **Citation:** Rentzsch P, Witten D, Cooper GM, Shendure J, Kircher M. CADD: predicting the deleteriousness of variants throughout the human genome. *Nucleic Acids Research*, 47(D1), D886-D894, 2019.
- **DOI:** [10.1093/nar/gky1016](https://doi.org/10.1093/nar/gky1016)
- **PMID:** 30371827 | **PMC:** PMC6323892
- **Citations:** ~2,500
- **Key findings:** Updated CADD to version 1.4 with GRCh38 genome support, expanded training data, and new annotations including updated ENCODE regulatory features. The GRCh38 compatibility is essential for scoring variants against current ENCODE annotations. CADD v1.4+ scores are the recommended deleteriousness metric for non-coding variants in ENCODE regulatory regions, complementing the direct overlap analysis with functional impact prediction.

---

### Ioannidis et al. 2016 — REVEL ensemble pathogenicity score

- **Citation:** Ioannidis NM, Rothstein JH, Pejaver V, Middha S, McDonnell SK, Baheti S, Musolf A, Li Q, Holzinger E, Karyadi D, Cannon-Albright LA, Teerlink CC, Stanford JL, Isaacs WB, Xu J, Cooney KA, Lange EM, Schleutker J, Carpten JD, Powell IJ, Cussenot O, Cancel-Tassin G, Giles GG, MacInnis RJ, Maier C, Hsieh CL, Wiklund F, Catalona WJ, Foulkes WD, Mandal D, Eeles RA, Kote-Jarai Z, Bustamante CD, Schaid DJ, Hastie T, Ostrander EA, Bailey-Wilson JE, Radivojac P, Thibodeau SN, Whittemore AS, Sieh W. REVEL: An Ensemble Method for Predicting the Pathogenicity of Rare Missense Variants. *American Journal of Human Genetics*, 99(4), 877-885, 2016.
- **DOI:** [10.1016/j.ajhg.2016.08.016](https://doi.org/10.1016/j.ajhg.2016.08.016)
- **PMID:** 27666373 | **PMC:** PMC5065685
- **Citations:** ~1,500
- **Key findings:** Developed REVEL, an ensemble method combining 13 individual pathogenicity prediction tools (including SIFT, PolyPhen, MutationAssessor, FATHMM, and others) to predict pathogenicity of rare missense variants. REVEL outperformed individual tools and other ensemble methods on multiple benchmarks. While primarily designed for coding variants, REVEL scores complement ENCODE-based regulatory variant annotation by providing strong missense pathogenicity estimates for variants in coding exons adjacent to regulatory elements.

---

## Clinical Classification Standards

### Richards et al. 2015 — ACMG variant classification guidelines

- **Citation:** Richards S, Aziz N, Bale S, Bick D, Das S, Gastier-Foster J, Grody WW, Hegde M, Lyon E, Spector E, Voelkerding K, Rehm HL, ACMG Laboratory Quality Assurance Committee. Standards and guidelines for the interpretation of sequence variants: a joint consensus recommendation of the American College of Medical Genetics and Genomics and the Association for Molecular Pathology. *Genetics in Medicine*, 17(5), 405-424, 2015.
- **DOI:** [10.1038/gim.2015.30](https://doi.org/10.1038/gim.2015.30)
- **PMID:** 25741868 | **PMC:** PMC4544753
- **Citations:** ~8,000
- **Key findings:** Established the five-tier classification system (pathogenic, likely pathogenic, uncertain significance, likely benign, benign) with 28 criteria for evaluating evidence strength. The ACMG/AMP guidelines include functional data as strong evidence for pathogenicity, which means ENCODE regulatory annotations (e.g., a variant disrupting a validated enhancer) can be used as supporting or moderate evidence in clinical variant classification. This is the definitive framework for clinical variant interpretation.

---

### Landrum et al. 2018 — ClinVar database

- **Citation:** Landrum MJ, Lee JM, Benson M, Brown GR, Chao C, Chitipiralla S, Gu B, Hart J, Hoffman D, Jang W, Karapetyan K, Katz K, Liu C, Maddipatla Z, Malheiro A, McDaniel K, Ovetsky M, Riley G, Zhou G, Holmes JB, Kattman BL, Maglott DR. ClinVar: improving access to variant interpretations and supporting evidence. *Nucleic Acids Research*, 46(D1), D1062-D1067, 2018.
- **DOI:** [10.1093/nar/gkx1153](https://doi.org/10.1093/nar/gkx1153)
- **PMID:** 29165669 | **PMC:** PMC5753237
- **Citations:** ~2,000
- **Key findings:** Described ClinVar, the NCBI public archive of reports on relationships between human variation and phenotypes, with supporting evidence. ClinVar aggregates variant classifications from clinical laboratories and research groups, enabling assessment of variant pathogenicity consensus. Cross-referencing ENCODE regulatory variants with ClinVar annotations reveals which disease-associated variants fall within functional elements, connecting variant annotation with clinical significance.

---

## Population Frequency and Constraint

### Karczewski et al. 2020 — gnomAD constraint metrics

- **Citation:** Karczewski KJ, Francioli LC, Tiao G, Cummings BB, Alfoldi J, Wang Q, Collins RL, Laricchia KM, Ganna A, Birnbaum DP, Gauthier LD, Brand H, Solomonson M, Watts NA, Rhodes D, Singer-Berk M, England EM, Seaby EG, Kosmicki JA, Walters RK, Tashman K, Farjoun Y, Banks E, Poterba T, Wang A, Seed C, Whiffin N, Chong JX, Samocha KE, Pierce-Hoffman E, Zappala Z, O'Donnell-Luria AH, Minikel EV, Weisburd B, Lek M, Ware JS, Vittal C, Armean IM, Bergelson L, Cibulskis K, Connolly KM, Covarrubias M, Donnelly S, Ferriera S, Gabriel S, Getz J, Gupta N, Hennigan C, Lebo M, Llanwarne C, Mahjneh I, Malecka-Trzaska M, Minikel EV, Neale BM, Nguyen TH, Ongchev I, Pontikos N, Poplin R, Sathirapongsasuti JF, Seed C, Singh T, Smith KS, VanderWeele M, Weisburd B, Weng Z, Zappala Z, MacArthur DG. The mutational constraint spectrum quantified from variation in 141,456 humans. *Nature*, 581(7809), 434-443, 2020.
- **DOI:** [10.1038/s41586-020-2308-7](https://doi.org/10.1038/s41586-020-2308-7)
- **PMID:** 32461654 | **PMC:** PMC7334197
- **Citations:** ~5,000
- **Key findings:** Presented the gnomAD v2.1 dataset with exome data from 125,748 individuals and genome data from 15,708 individuals, establishing gene-level constraint metrics (pLI, LOEUF, missense Z-scores). These metrics quantify intolerance to loss-of-function and missense variation, providing critical context for interpreting variants in ENCODE-annotated genes. Variants in constrained genes that overlap ENCODE regulatory elements are prioritized as potentially functional.

---

## Regulatory Variant Interpretation

### Cooper & Shendure 2011 — Challenges in regulatory variant interpretation

- **Citation:** Cooper GM, Shendure J. Needles in stacks of needles: finding disease-causal variants in a wealth of genomic data. *Nature Reviews Genetics*, 12(9), 628-640, 2011.
- **DOI:** [10.1038/nrg3046](https://doi.org/10.1038/nrg3046)
- **PMID:** 21850043
- **Citations:** ~800
- **Key findings:** Reviewed the challenges of identifying disease-causing variants among the millions of variants in each human genome, with particular focus on non-coding regulatory variants. The authors discussed how functional genomic annotations (including emerging ENCODE data) could be leveraged to prioritize regulatory variants, and outlined the conceptual framework for integrating evolutionary conservation, functional assays, and regulatory annotations. This paper provides the intellectual foundation for why ENCODE annotations are essential for variant interpretation.

---
