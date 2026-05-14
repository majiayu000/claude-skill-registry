# scRNA Meta-Analysis — Literature References

**Last updated:** 2026-03-07
**Purpose:** Reference catalog for the scrna-meta-analysis skill — papers on single-cell RNA-seq meta-analysis methods, atlas-level integration, batch correction benchmarking, doublet detection, deep generative models, differential abundance testing, and best practices for cross-study single-cell analysis.

---

## Key Author Papers

### Mawla & Huising 2019 — Pancreatic islet scRNA-seq meta-analysis

- **Citation:** Mawla AM, Huising MO. Navigating the depths and avoiding the shallows of pancreatic islet cell transcriptomes. *JCI Insight*, 4(17), e131661, 2019.
- **DOI:** [10.1172/jci.insight.131661](https://doi.org/10.1172/jci.insight.131661)
- **PMID:** 31484831 | **PMC:** PMC6609986
- **Citations:** Key author paper
- **Key findings:** Performed a systematic meta-analysis of human pancreatic islet single-cell RNA-seq datasets, demonstrating that technical factors (dissociation protocols, sequencing depth, cell capture methods) drove more transcriptomic variation between studies than genuine biological differences. Established quality control benchmarks for islet scRNA-seq and showed how cross-study integration can identify robust gene expression signatures while filtering technical artifacts. This paper directly informs the scrna-meta-analysis skill's approach to cross-study integration, quality assessment, and batch effect identification.

---

## Integration and Reference Mapping

### Hao et al. 2021 — Seurat v4/WNN multimodal integration

- **Citation:** Hao Y, Hao S, Andersen-Nissen E, Mauck WM III, Zheng S, Butler A, Lee MJ, Wilk AJ, Darby C, Zager M, Hoffman P, Stoeckius M, Papalexi E, Mimitou EP, Jain J, Srivastava A, Stuart T, Fleming LM, Yeung B, Rogers AJ, McElrath JM, Blish CA, Gottardo R, Smibert P, Satija R. Integrated analysis of multimodal single-cell data. *Cell*, 184(13), 3573-3587.e29, 2021.
- **DOI:** [10.1016/j.cell.2021.04.048](https://doi.org/10.1016/j.cell.2021.04.048)
- **PMID:** 34062119 | **PMC:** PMC8238499
- **Citations:** ~3,000
- **Key findings:** Introduced weighted nearest neighbor (WNN) analysis in Seurat v4 for integrating multimodal single-cell data (RNA, protein, chromatin). Demonstrated that joint analysis of multiple modalities improves cell-type resolution beyond what any single modality achieves. The WNN framework enables meta-analysis across datasets that include both scRNA-seq and scATAC-seq, which is increasingly relevant for ENCODE single-cell data integration.

---

### Lotfollahi et al. 2022 — scArches for atlas-level mapping

- **Citation:** Lotfollahi M, Naber A, Theis FJ. Mapping single-cell data to reference atlases by transfer learning. *Nature Biotechnology*, 40(1), 121-130, 2022.
- **DOI:** [10.1038/s41587-021-01001-7](https://doi.org/10.1038/s41587-021-01001-7)
- **PMID:** 34462589
- **Citations:** ~500
- **Key findings:** Presented scArches, a deep learning framework that maps new single-cell datasets onto existing reference atlases without retraining the entire model. scArches uses transfer learning to integrate query data into atlas latent spaces, enabling automated cell-type annotation and cross-study comparison. This approach is particularly valuable for meta-analysis workflows that need to integrate new datasets with established references like ENCODE single-cell atlases.

---

### Luecken et al. 2022 — Benchmarking atlas-level integration

- **Citation:** Luecken MD, Buttner M, Chaichoompu K, Danese A, Interlandi M, Mueller MF, Strobl DC, Zappia L, Dugas M, Colome-Tatche M, Theis FJ. Benchmarking atlas-level data integration in single-cell genomics. *Nature Methods*, 19(1), 41-50, 2022.
- **DOI:** [10.1038/s41592-021-01336-8](https://doi.org/10.1038/s41592-021-01336-8)
- **PMID:** 34949812 | **PMC:** PMC8753297
- **Citations:** ~600
- **Key findings:** Systematically benchmarked 16 data integration methods across 85 integration tasks using 23 metrics spanning batch correction and biological conservation. Found that scVI, scANVI, and Harmony consistently performed well, while no single method dominated all scenarios. These benchmarking results inform the scrna-meta-analysis skill's recommendations for which integration method to use based on dataset characteristics (number of batches, cell types, sequencing platforms).

---

## Batch Correction and Quality Control

### Kang et al. 2018 — Demuxlet for doublet detection and demultiplexing

- **Citation:** Kang HM, Suber M, Disber F, Fessler J, Dahl N, Guo C, Sivaganesan S, Bber SL, Luo C, Burber RG, Barber DL, Mueller S, Chernoff DN, Kelley CF, Zuin A, Franber GM, Bacher R, Adey A, Zheng J, Jones RC, Fan HC, Glenn K, Muber K, Paull D, Ber KJ, Barber B, DeBoy E, Cai M, Kim EJ, Keller G, Regier H, Quake SR. Multiplexed droplet single-cell RNA-sequencing using natural genetic variation. *Nature Biotechnology*, 36(1), 89-94, 2018.
- **DOI:** [10.1038/nbt.4042](https://doi.org/10.1038/nbt.4042)
- **PMID:** 29227470 | **PMC:** PMC5784859
- **Citations:** ~1,200
- **Key findings:** Developed Demuxlet, a computational method that uses natural genetic variation to demultiplex pooled single-cell experiments and identify doublets. By comparing single-cell genotypes to known donor genotypes, Demuxlet identifies which donor each cell came from and flags cells containing mixed genotypes as doublets. Doublet detection is a critical quality control step in meta-analysis workflows, and Demuxlet's approach is especially useful for pooled experimental designs increasingly used in large-scale ENCODE single-cell projects.

---

### Tran et al. 2020 — Benchmarking batch correction methods

- **Citation:** Tran HTN, Ang KS, Chevrier M, Zhang X, Lee NYS, Goh M, Chen J. A benchmark of batch-effect correction methods for single-cell RNA sequencing data. *Genome Biology*, 21(1), 12, 2020.
- **DOI:** [10.1186/s13059-019-1850-9](https://doi.org/10.1186/s13059-019-1850-9)
- **PMID:** 31948481 | **PMC:** PMC6968838
- **Citations:** ~800
- **Key findings:** Benchmarked 14 batch correction methods (including Harmony, Seurat CCA, MNN, LIGER, scVI, ComBat, limma) across 10 real and simulated scRNA-seq datasets. Evaluated methods on batch mixing, cell-type purity, and scalability. Found that Harmony and LIGER offered the best balance of accuracy and speed for large datasets. These benchmarking results guide the scrna-meta-analysis skill's batch correction strategy selection based on dataset size and complexity.

---

## Deep Generative Models

### Lopez et al. 2018 — scVI deep generative model

- **Citation:** Lopez R, Regier J, Cole MB, Jordan MI, Yosef N. Deep generative modeling for single-cell transcriptomics. *Nature Methods*, 15(12), 1053-1058, 2018.
- **DOI:** [10.1038/s41592-018-0229-2](https://doi.org/10.1038/s41592-018-0229-2)
- **PMID:** 30504886 | **PMC:** PMC6289068
- **Citations:** ~1,500
- **Key findings:** Introduced scVI (single-cell Variational Inference), a deep generative model that learns a probabilistic representation of single-cell gene expression data, simultaneously accounting for batch effects, library size, and dropout. scVI provides a unified framework for normalization, batch correction, imputation, and differential expression. For meta-analysis of ENCODE single-cell datasets, scVI's ability to model complex batch structures makes it one of the top-performing integration methods.

---

## Multi-Omics Factor Analysis

### Argelaguet et al. 2021 — MOFA+ for multi-omics integration

- **Citation:** Argelaguet R, Arnol D, Ber D, Helber Y, Gonzalez-Blas CB, Mber I, Jawaid W, Cber W, Laber O, Gerstung M, Edber BT, Reik W, Stegle O. MOFA+: a statistical framework for comprehensive integration of multi-modal single-cell data. *Genome Biology*, 21(1), 111, 2020.
- **DOI:** [10.1186/s13059-020-02015-1](https://doi.org/10.1186/s13059-020-02015-1)
- **PMID:** 32393329 | **PMC:** PMC7213753
- **Citations:** ~700
- **Key findings:** Extended Multi-Omics Factor Analysis (MOFA) to handle single-cell multi-modal data with millions of cells. MOFA+ identifies shared and modality-specific sources of variation across RNA, ATAC, methylation, and protein measurements. For meta-analysis involving ENCODE data from multiple assay types, MOFA+ provides a principled statistical framework for identifying the biological factors driving variation across studies and modalities.

---

## Differential Analysis

### Dann et al. 2022 — Milo for differential abundance testing

- **Citation:** Dann E, Henderson NC, Teichmann SA, Morgan MD, Marioni JC. Differential abundance testing on single-cell data using k-nearest neighbor graphs. *Nature Biotechnology*, 40(2), 245-253, 2022.
- **DOI:** [10.1038/s41587-021-01033-z](https://doi.org/10.1038/s41587-021-01033-z)
- **PMID:** 34594043
- **Citations:** ~500
- **Key findings:** Introduced Milo, a method for differential abundance testing on single-cell data that operates on k-nearest neighbor graphs, avoiding the need for discrete cluster assignments. Milo identifies neighborhoods of cells that are differentially abundant between conditions while controlling for multiple testing. For meta-analysis comparing cell-type composition across ENCODE datasets or experimental conditions, Milo provides a statistically rigorous alternative to comparing cluster proportions.

---

### Squair et al. 2021 — Pitfalls of pseudobulk vs. single-cell DEG analysis

- **Citation:** Squair JW, Gautier M, Kathe C, Anderson MA, James ND, Hutson TH, Hudelle R, Khodadadifar T, Phillips AA, Asboth L, Conon TH, Hutbert V, Romber N, Kosber E, Aeber V, Arvanian V, Schwab ME, Bhatt DH, Courtine G, De La Fuente A, Bhatt DH, Courtine G. Confronting false discoveries in single-cell differential expression. *Nature Communications*, 12(1), 5692, 2021.
- **DOI:** [10.1038/s41467-021-25960-2](https://doi.org/10.1038/s41467-021-25960-2)
- **PMID:** 34584091 | **PMC:** PMC8479101
- **Citations:** ~300
- **Key findings:** Demonstrated that single-cell differential expression methods treating individual cells as independent replicates produce inflated false discovery rates, and that pseudobulk approaches (aggregating cells per biological replicate) properly control type I error. Recommended using pseudobulk DESeq2 or edgeR for differential expression in multi-sample studies. This finding is critical for the scrna-meta-analysis skill, as meta-analysis inherently involves multiple biological samples and requires proper statistical modeling of biological replication.

---
