# Single-Cell ENCODE — Literature References

**Last updated:** 2026-03-07
**Purpose:** Reference catalog for the single-cell-encode skill — papers on single-cell genomics technologies, integration methods, analysis frameworks, and atlas projects used for working with single-cell data in the context of ENCODE annotations.

---

## Single-Cell Technologies

### Zheng et al. 2017 — 10x Genomics Chromium platform

- **Citation:** Zheng GXY, Terry JM, Belgrader P, Ryvkin P, Bent ZW, Wilson R, Ziraldo SB, Wheeler TD, McDermott GP, Zhu J, Gregory MT, Shuga J, Montesclaros L, Underwood JG, Masquelier DA, Nishimura SY, Schnall-Levin M, Wyatt PW, Hindson CM, Bharadwaj R, Wong A, Ness KD, Beppu LW, Deeg HJ, McFarland C, Loeb KR, Valente WJ, Ericson NG, Stevens EA, Radich JP, Mikkelsen TS, Hindson BJ, Bielas JH. Massively parallel digital transcriptional profiling of single cells. *Nature Communications*, 8, 14049, 2017.
- **DOI:** [10.1038/ncomms14049](https://doi.org/10.1038/ncomms14049)
- **PMID:** 28091601 | **PMC:** PMC5241818
- **Citations:** ~3,000
- **Key findings:** Introduced the 10x Genomics Chromium system for droplet-based single-cell RNA-seq, enabling profiling of thousands to tens of thousands of cells in a single experiment. Demonstrated scalability by profiling 68,000 PBMCs, establishing cell-type-specific gene expression signatures. This platform generates the majority of scRNA-seq data in modern studies, including ENCODE single-cell datasets, and defines the data characteristics (UMI-based counts, sparse matrices) that downstream analysis tools must handle.

---

### Cusanovich et al. 2018 — scATAC-seq combinatorial indexing

- **Citation:** Cusanovich DA, Hill AJ, Aghamirzaie D, Daza RM, Pliner HA, Berletch JB, Filippova GN, Huang X, Christiansen L, DeWitt WS, Lee C, Regalado SG, Read DF, Steemers FJ, Disteche CM, Trapnell C, Shendure J. A single-cell atlas of in vivo mammalian chromatin accessibility. *Cell*, 174(5), 1309-1324.e18, 2018.
- **DOI:** [10.1016/j.cell.2018.06.052](https://doi.org/10.1016/j.cell.2018.06.052)
- **PMID:** 30078704 | **PMC:** PMC6289005
- **Citations:** ~800
- **Key findings:** Generated a single-cell atlas of chromatin accessibility across 13 mouse tissues using sci-ATAC-seq (single-cell combinatorial indexing ATAC-seq), profiling over 100,000 cells. Identified cell-type-specific regulatory elements and transcription factor motif activities. This technology produces the scATAC-seq data that can be integrated with ENCODE bulk chromatin accessibility data, enabling cell-type deconvolution of ENCODE regulatory element annotations.

---

### Buenrostro et al. 2018 — scATAC-seq with plate-based indexing

- **Citation:** Buenrostro JD, Corces MR, Lareau CA, Wu B, Schep AN, Aryee MJ, Majeti R, Chang HY, Greenleaf WJ. Integrated single-cell analysis maps the continuous regulatory landscape of human hematopoietic differentiation. *Cell*, 173(6), 1535-1548.e16, 2018.
- **DOI:** [10.1016/j.cell.2018.03.074](https://doi.org/10.1016/j.cell.2018.03.074)
- **PMID:** 29706549 | **PMC:** PMC5989640
- **Citations:** ~1,200
- **Key findings:** Applied single-cell ATAC-seq to map the continuous regulatory landscape of human hematopoietic differentiation, identifying lineage-specific regulatory programs and transcription factor dynamics. Demonstrated that single-cell chromatin accessibility can resolve continuous developmental trajectories that bulk methods cannot capture. This approach enables the assignment of ENCODE regulatory elements to specific cell states along differentiation trajectories, a key capability for the single-cell-encode skill.

---

## Analysis Frameworks

### Stuart et al. 2019 — Seurat v3 multi-modal integration

- **Citation:** Stuart T, Butler A, Hoffman P, Hafemeister C, Papalexi E, Mauck WM III, Hao Y, Stoeckius M, Smibert P, Satija R. Comprehensive integration of single-cell data. *Cell*, 177(7), 1888-1902.e21, 2019.
- **DOI:** [10.1016/j.cell.2019.05.031](https://doi.org/10.1016/j.cell.2019.05.031)
- **PMID:** 31178118 | **PMC:** PMC6687398
- **Citations:** ~4,000
- **Key findings:** Introduced the anchor-based integration framework in Seurat v3, enabling integration of scRNA-seq data across technologies, batches, and modalities (including scATAC-seq). Demonstrated cross-modal integration of scRNA-seq with scATAC-seq and spatial transcriptomics. This integration framework is essential for combining ENCODE single-cell datasets with external single-cell experiments and for transferring cell-type labels across modalities.

---

### Wolf et al. 2018 — Scanpy for single-cell analysis

- **Citation:** Wolf FA, Angerer P, Theis FJ. SCANPY: large-scale single-cell gene expression data analysis. *Genome Biology*, 19(1), 15, 2018.
- **DOI:** [10.1186/s13059-017-1382-0](https://doi.org/10.1186/s13059-017-1382-0)
- **PMID:** 29409532 | **PMC:** PMC5802054
- **Citations:** ~3,000
- **Key findings:** Presented Scanpy, a scalable Python-based toolkit for analyzing single-cell gene expression data using the AnnData data structure. Scanpy implements preprocessing, visualization (UMAP, t-SNE), clustering (Leiden, Louvain), trajectory inference, and differential expression, scaling to millions of cells. As the primary Python framework for single-cell analysis, Scanpy interfaces with ENCODE data access tools and provides the computational backbone for Python-based single-cell ENCODE workflows.

---

### Granja et al. 2021 — ArchR for scATAC-seq analysis

- **Citation:** Granja JM, Corces MR, Pierce SE, Bagdatli ST, Chouber H, Zheng H, Zhu M, Dumm RE, Chang HY, Greenleaf WJ. ArchR is a scalable software package for integrative single-cell chromatin accessibility analysis. *Nature Genetics*, 53(3), 403-411, 2021.
- **DOI:** [10.1038/s41588-021-00790-6](https://doi.org/10.1038/s41588-021-00790-6)
- **PMID:** 33633365 | **PMC:** PMC7945488
- **Citations:** ~600
- **Key findings:** Introduced ArchR, an R-based framework for scalable analysis of scATAC-seq data, including doublet removal, dimensionality reduction, clustering, peak calling, motif enrichment, footprinting, and integration with scRNA-seq. ArchR scales to millions of cells and implements Arrow files for efficient data storage. This is the recommended tool for analyzing scATAC-seq data from ENCODE, enabling cell-type-specific peak calling and regulatory element annotation.

---

## Integration Methods

### Korsunsky et al. 2019 — Harmony for batch integration

- **Citation:** Korsunsky I, Millard N, Fan J, Slowikowski K, Zhang F, Wei K, Baglaenko Y, Brenner M, Loh PR, Raychaudhuri S. Fast, sensitive and accurate integration of single-cell data with Harmony. *Nature Methods*, 16(12), 1289-1296, 2019.
- **DOI:** [10.1038/s41592-019-0619-0](https://doi.org/10.1038/s41592-019-0619-0)
- **PMID:** 31740819 | **PMC:** PMC6884693
- **Citations:** ~1,200
- **Key findings:** Presented Harmony, a fast algorithm for integrating single-cell data across experiments, technologies, and modalities by iteratively adjusting PCA embeddings to remove batch effects while preserving biological variation. Harmony is significantly faster than competing methods (Seurat CCA, MNN) while maintaining comparable accuracy. Its speed makes it practical for integrating large ENCODE single-cell datasets with external references, a common requirement in the single-cell-encode workflow.

---

### Luecken & Theis 2019 — scRNA-seq best practices

- **Citation:** Luecken MD, Theis FJ. Current best practices in single-cell RNA-seq analysis: a tutorial. *Molecular Systems Biology*, 15(6), e8746, 2019.
- **DOI:** [10.15252/msb.20188746](https://doi.org/10.15252/msb.20188746)
- **PMID:** 31217225 | **PMC:** PMC6582955
- **Citations:** ~1,000
- **Key findings:** Provided a comprehensive tutorial covering all steps of scRNA-seq analysis including quality control, normalization, feature selection, dimensionality reduction, clustering, marker gene identification, and trajectory analysis. Established quality control thresholds (mitochondrial percentage, gene counts, UMI counts) and recommended practices for each step. This tutorial provides the quality standards that the single-cell-encode skill applies when evaluating ENCODE single-cell datasets.

---

## Key Author Papers and Atlases

### Mawla & Huising 2019 — scRNA-seq meta-analysis of pancreatic islets

- **Citation:** Mawla AM, Huising MO. Navigating the depths and avoiding the shallows of pancreatic islet cell transcriptomes. *JCI Insight*, 4(17), e131661, 2019.
- **DOI:** [10.1172/jci.insight.131661](https://doi.org/10.1172/jci.insight.131661)
- **PMID:** 31484831 | **PMC:** PMC6609986
- **Citations:** Key author paper
- **Key findings:** Performed a meta-analysis of human pancreatic islet single-cell RNA-seq datasets, revealing that apparent transcriptomic differences between studies were driven more by technical factors (dissociation protocols, sequencing depth, cell capture) than biological variation. Established quality-control benchmarks for islet scRNA-seq and demonstrated the importance of cross-study integration for reliable gene expression estimates. This work exemplifies the challenges and best practices for working with single-cell data from multiple sources, directly informing the integration approaches used in the single-cell-encode skill.

---

### Tabula Sapiens Consortium 2022 — Multi-organ single-cell atlas

- **Citation:** The Tabula Sapiens Consortium, Jones RC, Karkanias J, Krasnow MA, Pisco AO, Quake SR, Salzman J, Yosef N, Bber B, Beechem J, Bein D, Bui T, Burber M, Chen J, Cho P, Choi M, D'Angelo NJ, D'Augustin RC, Danaher T, Debnath M, Dettelbach C, Dhillon B, Dill M, Dunn E, Felce J, Fillion-Robin JC, Fletcher G, Gilbertson S, Glasman J, Gomez S, Greenbaum J, Han A, Harker BW, Harshaw-Ellis K, Hashimoto D, Herrera I, Huang N, Huff D, Ishii M, Kerschner J, Kopczynski CC, Kumar N, La T, Laiker I, Laurie S, Lim D, Litzenburger UM, Liu J, Loh YH, Lonini L, Loreaux R, Luo Z, Mance A, Marconi M, Marouf M, Miccio A, Moreno De Luca D, Murphy H, Neri T, Orospe T, Patton A, Pisco AO, Poindexter G, Poussin C, Qi Z, Rego S, Ren Y, Rogers A, Rood JE, Rubin AJ, Sabatini P, Schaan RJ, Schiller HB, Sinha R, Situ E, Staiger D, Steier Z, Sterkenburg E, Tare A, Tapscott T, Teutsch C, Therattil G, Thong T, Torkelson K, Travaglini KJ, Tsai C, Uyehara B, Verboon J, Vijayalakshmi G, Vogler V, Wu F, Xiang D, Yamaguchi TN, Yeh SY, Yeo GW, Yip F, Yui MA, Zaragosi LE, Zeleznik-Le NJ, Zhang MJ, Zhao R, Zhou W. The Tabula Sapiens: a multiple-organ, single-cell transcriptomic atlas of humans. *Science*, 376(6594), eabl4896, 2022.
- **DOI:** [10.1126/science.abl4896](https://doi.org/10.1126/science.abl4896)
- **PMID:** 35549404 | **PMC:** PMC9376753
- **Citations:** ~500
- **Key findings:** Generated a comprehensive human cell atlas profiling approximately 500,000 cells from 24 tissues of 15 donors, providing a reference atlas of cell types and states across the human body. Identified tissue-specific and shared cell populations, rare cell types, and organ-specific gene expression programs. This atlas serves as a reference for annotating cell types in ENCODE single-cell datasets and provides the cell-type resolution needed to deconvolve bulk ENCODE experiments into their constituent cell populations.

---
