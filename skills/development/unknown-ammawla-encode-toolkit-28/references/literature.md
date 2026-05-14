# Disease Research — Literature References

**Last updated:** 2026-03-07
**Purpose:** Reference catalog for the disease-research skill — papers on GWAS variant interpretation, functional annotation of disease-associated loci, chromatin state models, heritability partitioning, and enhancer-gene linking methods used to connect ENCODE regulatory elements with human disease.

---

## GWAS and Regulatory Element Overlap

### Maurano et al. 2012 — GWAS variants in regulatory DNA

- **Citation:** Maurano MT, Humbert R, Rynes E, Thurman RE, Haugen E, Wang H, Reynolds AP, Sandstrom R, Qu H, Brody J, Shafer A, Neri F, Lee K, Kutyavin T, Stehling-Sun S, Johnson AK, Canfield TK, Giste E, Diegel M, Bates D, Hansen RS, Neph S, Sabo PJ, Heimfeld S, Raubitschek A, Ziegler S, Cotsapas C, Sotoodehnia N, Glass I, Sunyaev SR, Kaul R, Stamatoyannopoulos JA. Systematic localization of common disease-associated variation in regulatory DNA. *Science*, 337(6099), 1190-1195, 2012.
- **DOI:** [10.1126/science.1222794](https://doi.org/10.1126/science.1222794)
- **PMID:** 22955828 | **PMC:** PMC3771521
- **Citations:** ~3,000
- **Key findings:** Demonstrated that the majority of GWAS-identified disease and trait-associated variants fall within DNase I hypersensitive sites (DHSs), particularly in cell-type-specific regulatory elements. The enrichment was strongest for variants associated with autoimmune, metabolic, and cardiovascular diseases. This paper established the fundamental principle that disease genetics operates primarily through regulatory mechanisms, providing the core rationale for using ENCODE regulatory annotations in disease research.

---

### Hindorff et al. 2009 — GWAS Catalog landscape

- **Citation:** Hindorff LA, Sethupathy P, Junkins HA, Ramos EM, Mehta JP, Collins FS, Manolio TA. Potential etiologic and functional implications of genome-wide association loci for human diseases and traits. *Proceedings of the National Academy of Sciences*, 106(23), 9362-9367, 2009.
- **DOI:** [10.1073/pnas.0903103106](https://doi.org/10.1073/pnas.0903103106)
- **PMID:** 19474294 | **PMC:** PMC2687147
- **Citations:** ~4,000
- **Key findings:** Provided the first systematic analysis of the NHGRI GWAS Catalog, revealing that 88% of trait-associated SNPs fell in non-coding regions. The analysis highlighted that intergenic and intronic variants predominated, and that many associated loci lacked obvious functional mechanisms. This observation motivated the integration of ENCODE functional annotations with GWAS data and remains the key reference for understanding why regulatory element databases are essential for interpreting disease-associated variation.

---

## Chromatin States and Disease Epigenomics

### Roadmap Epigenomics Consortium 2015 — Reference human epigenomes

- **Citation:** Roadmap Epigenomics Consortium, Kundaje A, Meuleman W, Ernst J, Bilenky M, Yen A, Heravi-Moussavi A, Kheradpour P, Zhang Z, Wang J, Ziller MJ, Amin V, Whitaker JW, Schultz MD, Ward LD, Sarkar A, Quon G, Sandstrom RS, Eaton ML, Wu YC, Pfenning AR, Wang X, Claussnitzer M, Liu Y, Coarfa C, Harris RA, Shoresh N, Epstein CB, Gjoneska E, Leung D, Xie W, Hawkins RD, Lister R, Hong C, Gasber P, Mungall AJ, Moore R, Chuah E, Tam A, Canfield TK, Hansen RS, Kaul R, Sabo PJ, Banber MS, Garber M, Gong P, Friel BJ, Zhang MQ, Smith ZD, Bernastein BC, Meissner A, Ecker JR, Stamatoyannopoulos JA, Kellis M. Integrative analysis of 111 reference human epigenomes. *Nature*, 518(7539), 317-330, 2015.
- **DOI:** [10.1038/nature14248](https://doi.org/10.1038/nature14248)
- **PMID:** 25693563 | **PMC:** PMC4530010
- **Citations:** ~4,500
- **Key findings:** Generated and analyzed 111 reference epigenomes spanning diverse human tissues and cell types, mapping histone modifications, DNA methylation, DNA accessibility, and RNA expression. Demonstrated tissue-specific enrichment of GWAS variants in regulatory chromatin states, with disease-associated variants enriched in enhancers active in disease-relevant tissues. This resource provides the tissue-specific epigenomic context essential for interpreting ENCODE data in disease research.

---

### Ernst & Kellis 2012 — ChromHMM for disease-relevant chromatin states

- **Citation:** Ernst J, Kellis M. ChromHMM: automating chromatin-state discovery and characterization. *Nature Methods*, 9(3), 215-216, 2012.
- **DOI:** [10.1038/nmeth.1906](https://doi.org/10.1038/nmeth.1906)
- **PMID:** 22373907 | **PMC:** PMC3577932
- **Citations:** ~2,500
- **Key findings:** Introduced ChromHMM, a multivariate hidden Markov model that segments genomes into chromatin states based on combinatorial patterns of histone modifications. The 15-state and 18-state models identify promoters, enhancers, transcribed regions, repressed domains, and quiescent states. ChromHMM state annotations from ENCODE and Roadmap Epigenomics are fundamental inputs for disease research, enabling the identification of disease-relevant regulatory states in specific cell types.

---

## Heritability and Functional Enrichment

### Finucane et al. 2015 — Partitioning heritability by functional annotation

- **Citation:** Finucane HK, Bulik-Sullivan B, Gusev A, Trynka G, Reshef Y, Loh PR, Anttila V, Xu H, Zang C, Farh K, Ripke S, Day FR, ReproGen Consortium, Schizophrenia Working Group of the Psychiatric Genomics Consortium, RACI Consortium, Purcell S, Smoller JW, Raychaudhuri S, Lander ES, Neale BM, Price AL. Partitioning heritability by functional annotation using genome-wide association summary statistics. *Nature Genetics*, 47(11), 1228-1235, 2015.
- **DOI:** [10.1038/ng.3404](https://doi.org/10.1038/ng.3404)
- **PMID:** 26414678 | **PMC:** PMC4626285
- **Citations:** ~2,500
- **Key findings:** Extended LD Score Regression to partition SNP-heritability across functional categories including ENCODE-defined regulatory elements. Demonstrated that conserved regions, H3K4me3 peaks, and DHS sites were highly enriched for heritability across multiple traits, while repressed regions were depleted. This method enables quantitative assessment of how much trait heritability is concentrated in specific ENCODE regulatory element classes, directly informing disease-research prioritization.

---

### Bulik-Sullivan et al. 2015 — LD Score Regression

- **Citation:** Bulik-Sullivan BK, Loh PR, Finucane HK, Ripke S, Yang J, Schizophrenia Working Group of the Psychiatric Genomics Consortium, Patterson N, Daly MJ, Price AL, Neale BM. LD Score regression distinguishes confounding from polygenicity in genome-wide association studies. *Nature Genetics*, 47(3), 291-295, 2015.
- **DOI:** [10.1038/ng.3211](https://doi.org/10.1038/ng.3211)
- **PMID:** 25642630 | **PMC:** PMC4495769
- **Citations:** ~3,000
- **Key findings:** Developed LD Score Regression, a method that uses the relationship between GWAS test statistics and linkage disequilibrium scores to distinguish true polygenic signal from confounding bias. This method provides robust estimates of SNP-heritability and genetic correlation between traits, and forms the statistical foundation for partitioned heritability analyses that integrate ENCODE annotations. It is an essential upstream method for the disease-research skill's enrichment analyses.

---

## Enhancer-Gene Linking

### Nasser et al. 2021 — ABC Model for enhancer-gene connections

- **Citation:** Nasser J, Bergman DT, Fulco CP, Gusev A, Engreitz JM. Genome-wide enhancer maps link risk variants to disease genes. *Nature*, 593(7858), 238-243, 2021.
- **DOI:** [10.1038/s41586-021-03446-x](https://doi.org/10.1038/s41586-021-03446-x)
- **PMID:** 33981038 | **PMC:** PMC8492567
- **Citations:** ~800
- **Key findings:** Applied the Activity-by-Contact (ABC) model to create genome-wide maps linking enhancers to their target genes across 131 biosamples, using ENCODE chromatin accessibility and H3K27ac data combined with Hi-C contact frequencies. Used these maps to connect GWAS variants to likely causal genes for 72 diseases. The ABC model provides a principled framework for linking ENCODE-defined regulatory elements to disease genes, which is a core function of the disease-research skill.

---

### Gasperini et al. 2019 — CRISPR-based enhancer mapping at scale

- **Citation:** Gasperini M, Hill AJ, McFaline-Figueroa JL, Martin B, Kim S, Zhang MD, Jackson D, Leith A, Schreiber J, Noble WS, Trapnell C, Ahfeldt T, Shendure J. A genome-scale screen for enhancers at single-cell resolution. *Cell*, 176(6), 1428-1443.e21, 2019.
- **DOI:** [10.1016/j.cell.2018.12.038](https://doi.org/10.1016/j.cell.2018.12.038)
- **PMID:** 30612741 | **PMC:** PMC6886585
- **Citations:** ~900
- **Key findings:** Used CRISPR interference (CRISPRi) coupled with single-cell RNA-seq to test 5,920 candidate enhancers at scale, identifying 470 enhancer-gene links and demonstrating that enhancer effects are often cell-type-specific and distance-independent. This work provides experimental validation for computationally predicted enhancer-gene links from ENCODE data and demonstrates that many ENCODE-defined cCREs have measurable effects on gene expression, directly supporting the disease-research workflow's functional annotation of regulatory variants.

---
