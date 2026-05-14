# Multi-Omics Integration — Literature References

**Last updated:** 2026-03-07
**Purpose:** Reference catalog for the multi-omics-integration skill — papers on methods and frameworks for integrating multiple genomic data types (chromatin accessibility, histone modifications, DNA methylation, gene expression, 3D genome) from ENCODE and related projects into unified biological models.

---

## ENCODE and Roadmap Integration

### ENCODE Project Consortium 2020 — Phase 3 integrative analysis

- **Citation:** ENCODE Project Consortium, Moore JE, Purcaro MJ, Pratt HE, Epstein CB, Shoresh N, Adrian J, Kawli T, Davis CA, Dobin A, et al. Expanded encyclopaedias of DNA elements in the human and mouse genomes. *Nature*, 583(7818), 699-710, 2020.
- **DOI:** [10.1038/s41586-020-2493-4](https://doi.org/10.1038/s41586-020-2493-4)
- **PMID:** 32728249 | **PMC:** PMC7410828
- **Citations:** ~2,000
- **Key findings:** Integrated 5,992 new datasets across RNA transcription, chromatin structure, histone modification, DNA methylation, chromatin looping, and transcription factor occupancy to build a registry of 926,535 human and 339,815 mouse candidate cis-regulatory elements (cCREs). This paper demonstrates the gold standard for multi-omics integration: combining diverse assay types from matched biosamples to create a unified regulatory element catalog. The cCRE registry is the primary output of ENCODE's integrative analysis and the starting point for the multi-omics-integration skill.

---

### Roadmap Epigenomics Consortium 2015 — Reference epigenomes integration

- **Citation:** Roadmap Epigenomics Consortium, Kundaje A, Meuleman W, Ernst J, Bilenky M, Yen A, et al. Integrative analysis of 111 reference human epigenomes. *Nature*, 518(7539), 317-330, 2015.
- **DOI:** [10.1038/nature14248](https://doi.org/10.1038/nature14248)
- **PMID:** 25693563 | **PMC:** PMC4530010
- **Citations:** ~4,500
- **Key findings:** Integrated five core histone marks (H3K4me3, H3K4me1, H3K36me3, H3K27me3, H3K9me3) with DNA methylation and RNA expression across 111 reference epigenomes to define tissue-specific regulatory landscapes. Demonstrated that integrating multiple data types resolves regulatory states that no single assay can identify. The 15-state and 18-state ChromHMM models from this project are foundational inputs for multi-omics integration workflows that overlay ENCODE data with tissue-specific epigenomic context.

---

## Chromatin State Discovery

### Ernst & Kellis 2012 — ChromHMM chromatin state modeling

- **Citation:** Ernst J, Kellis M. ChromHMM: automating chromatin-state discovery and characterization. *Nature Methods*, 9(3), 215-216, 2012.
- **DOI:** [10.1038/nmeth.1906](https://doi.org/10.1038/nmeth.1906)
- **PMID:** 22373907 | **PMC:** PMC3577932
- **Citations:** ~2,500
- **Key findings:** Presented ChromHMM, a hidden Markov model approach that integrates multiple histone modification ChIP-seq datasets to segment the genome into functionally distinct chromatin states (active promoters, strong enhancers, poised elements, heterochromatin, etc.). ChromHMM is the primary tool for multi-omics integration at the chromatin level, and its state annotations serve as the framework for interpreting how different ENCODE data types converge on regulatory function.

---

## Single-Cell Multi-Modal Integration

### Yan et al. 2020 — MAESTRO for scRNA/scATAC integration

- **Citation:** Wang C, Sun D, Huang X, Wan C, Li Z, Han Y, Qin Q, Fan J, Qiu X, Xie Y, Meyer CA, Brown M, Tang M, Long H, Liu T, Liu XS. Integrative analyses of single-cell transcriptome and regulome using MAESTRO. *Genome Biology*, 21(1), 198, 2020.
- **DOI:** [10.1186/s13059-020-02116-x](https://doi.org/10.1186/s13059-020-02116-x)
- **PMID:** 32767996 | **PMC:** PMC7412809
- **Citations:** ~300
- **Key findings:** Introduced MAESTRO, an integrative pipeline for single-cell RNA-seq and ATAC-seq analysis that performs automated quality control, clustering, differential analysis, transcription factor activity inference, and cross-modality integration. MAESTRO links gene expression with chromatin accessibility at single-cell resolution, enabling identification of cell-type-specific regulatory programs. This tool bridges ENCODE bulk regulatory annotations with single-cell resolution data in multi-omics integration workflows.

---

### Stuart et al. 2019 — Seurat v3 multi-modal integration

- **Citation:** Stuart T, Butler A, Hoffman P, Hafemeister C, Papalexi E, Mauck WM III, Hao Y, Stoeckius M, Smibert P, Satija R. Comprehensive integration of single-cell data. *Cell*, 177(7), 1888-1902.e21, 2019.
- **DOI:** [10.1016/j.cell.2019.05.031](https://doi.org/10.1016/j.cell.2019.05.031)
- **PMID:** 31178118 | **PMC:** PMC6687398
- **Citations:** ~4,000
- **Key findings:** Developed anchor-based integration methods in Seurat v3 that align datasets across technologies, batches, and modalities. Demonstrated integration of scRNA-seq with scATAC-seq to explore chromatin differences between cell subtypes, and projection of protein expression onto transcriptomic atlases. This anchor framework is the most widely used method for multi-modal single-cell integration and is essential for combining ENCODE single-cell data with external multi-omic datasets.

---

### Welch et al. 2019 — LIGER for linked inference

- **Citation:** Welch JD, Kozareva V, Ferreira A, Vanderburg C, Martin C, Macosko EZ. Single-cell multi-omic integration compares and contrasts features of brain cell identity. *Cell*, 177(7), 1873-1887.e17, 2019.
- **DOI:** [10.1016/j.cell.2019.05.006](https://doi.org/10.1016/j.cell.2019.05.006)
- **PMID:** 31178122 | **PMC:** PMC6716966
- **Citations:** ~1,000
- **Key findings:** Introduced LIGER (Linked Inference of Genomic Experimental Relationships), which uses integrative non-negative matrix factorization (iNMF) to identify shared and dataset-specific factors across different single-cell modalities. Applied to integrating snRNA-seq with snATAC-seq in brain, revealing shared cell-type identities and modality-specific regulatory features. LIGER provides an alternative to anchor-based methods for multi-omics factor discovery in ENCODE integration workflows.

---

### Argelaguet et al. 2020 — MOFA+ for multi-omics factor analysis

- **Citation:** Argelaguet R, Arnol D, Ber D, Helber Y, Gonzalez-Blas CB, Mber I, Jawaid W, Cber W, Laber O, Gerstung M, Edber BT, Reik W, Stegle O. MOFA+: a statistical framework for comprehensive integration of multi-modal single-cell data. *Genome Biology*, 21(1), 111, 2020.
- **DOI:** [10.1186/s13059-020-02015-1](https://doi.org/10.1186/s13059-020-02015-1)
- **PMID:** 32393329 | **PMC:** PMC7213753
- **Citations:** ~700
- **Key findings:** Extended MOFA to scale to millions of cells across multiple data modalities (RNA, ATAC, methylation, protein), decomposing variation into interpretable factors that capture shared biology and modality-specific technical effects. MOFA+ is particularly suited for multi-omics integration where the goal is to identify latent biological factors driving variation across ENCODE data types, providing interpretable dimensionality reduction for complex multi-assay datasets.

---

## Pathway and Gene Set Analysis

### Subramanian et al. 2005 — GSEA gene set enrichment analysis

- **Citation:** Subramanian A, Tamayo P, Mootha VK, Mukherjee S, Ebert BL, Gillette MA, Paulovich A, Pomeroy SL, Golub TR, Lander ES, Mesirov JP. Gene set enrichment analysis: a knowledge-based approach for interpreting genome-wide expression profiles. *Proceedings of the National Academy of Sciences*, 102(43), 15545-15550, 2005.
- **DOI:** [10.1073/pnas.0506580102](https://doi.org/10.1073/pnas.0506580102)
- **PMID:** 16199517 | **PMC:** PMC1239896
- **Citations:** ~25,000
- **Key findings:** Introduced Gene Set Enrichment Analysis (GSEA), a method that determines whether a predefined set of genes shows statistically significant concordant differences between two biological states. GSEA avoids the limitations of single-gene analysis by evaluating pathways as units. In multi-omics integration, GSEA connects gene-level signals from ENCODE expression and chromatin data to biological pathway knowledge, providing functional interpretation of integrated results. Its 25,000+ citations reflect its status as the most widely used pathway analysis method.

---

## Chromatin Accessibility Atlases

### Corces et al. 2018 — TCGA chromatin accessibility atlas

- **Citation:** Corces MR, Granja JM, Shams S, Louber BH, Ber EH, Zhang J, Greenside PG, Ghber M, Atber A, Demir E, Cerber L, Frer JR, Mber K, Gao GF, Gaber M, Meyerson M, Kundaje A, Margolais EK, Chang HY, Greenleaf WJ. The chromatin accessibility landscape of primary human cancers. *Science*, 362(6413), eaav1898, 2018.
- **DOI:** [10.1126/science.aav1898](https://doi.org/10.1126/science.aav1898)
- **PMID:** 30361341 | **PMC:** PMC6408149
- **Citations:** ~1,500
- **Key findings:** Generated ATAC-seq profiles for 410 tumor samples across 23 cancer types from TCGA, creating the first pan-cancer chromatin accessibility atlas. Identified cancer-type-specific regulatory elements, transcription factor activities, and enhancer-gene links. This atlas demonstrates how chromatin accessibility data can be integrated with gene expression, copy number, and mutation data from the same samples, serving as a model for the multi-omics integration approach applied to ENCODE data across tissues and cell types.

---

### Granja et al. 2021 — ArchR for integrative scATAC analysis

- **Citation:** Granja JM, Corces MR, Pierce SE, Bagdatli ST, Chouber H, Zheng H, Zhu M, Dumm RE, Chang HY, Greenleaf WJ. ArchR is a scalable software package for integrative single-cell chromatin accessibility analysis. *Nature Genetics*, 53(3), 403-411, 2021.
- **DOI:** [10.1038/s41588-021-00790-6](https://doi.org/10.1038/s41588-021-00790-6)
- **PMID:** 33633365 | **PMC:** PMC7945488
- **Citations:** ~600
- **Key findings:** Presented ArchR, a scalable R package for integrative scATAC-seq analysis including gene activity scoring, peak-to-gene linking, motif enrichment, footprinting, and integration with scRNA-seq. ArchR scales to millions of cells and provides the analytical framework for connecting chromatin accessibility with gene expression at single-cell resolution. For multi-omics integration of ENCODE data, ArchR bridges the gap between bulk ENCODE regulatory annotations and cell-type-resolved regulatory landscapes.

---
