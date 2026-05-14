# Hypomethylated Region (HMR) Definitions and Classification

## Overview

DNA methylation landscapes contain three major domain types defined by their methylation levels. Correct identification and classification of these domains is essential for interpreting ENCODE WGBS aggregation results.

## Domain Definitions

### UMR — Unmethylated Region
- **Methylation level**: <10% average CpG methylation
- **Typical size**: 200bp - 5kb
- **Genomic location**: CpG islands, active promoters
- **Biological function**: Marks active regulatory elements, especially promoters
- **Identification**: Contiguous CpGs with <10% methylation, minimum 4 CpGs
- **Reference**: Schultz et al. 2015 (Nature, ~1,500 citations) DOI: 10.1038/nature14248

### LMR — Low-Methylated Region
- **Methylation level**: 10-50% average CpG methylation
- **Typical size**: 200bp - 2kb
- **Genomic location**: Distal enhancers, TF binding sites
- **Biological function**: Marks active or poised enhancers, TF binding reduces methylation
- **Identification**: Contiguous CpGs with 10-50% methylation
- **Key insight**: LMRs correlate strongly with ENCODE H3K4me1 and H3K27ac peaks
- **Reference**: Stadler et al. 2011 (Nature, ~1,200 citations) DOI: 10.1038/nature10716

### PMD — Partially Methylated Domain
- **Methylation level**: 50-70% average methylation across large domains
- **Typical size**: 100kb - 10Mb
- **Genomic location**: Gene-poor, late-replicating regions
- **Biological function**: Associated with heterochromatin, gene silencing, aging
- **Identification**: Large domains where bulk methylation drops below genome average (~80%)
- **Important caveat**: PMDs are cell-type specific and expand with cellular aging/passaging
- **Reference**: Lister et al. 2009 (Nature, ~5,000 citations) DOI: 10.1038/nature08514

### HMR — Hypomethylated Region (general term)
- Umbrella term encompassing UMRs and LMRs
- Some tools (e.g., MethPipe) call HMRs without distinguishing UMR vs LMR
- If using HMR calls, separate by size and CpG density: large + CpG-dense = UMR, small + CpG-poor = LMR

## Coverage Sensitivity

HMR identification is highly sensitive to sequencing coverage:

| Coverage | Reliability | Notes |
|----------|------------|-------|
| <5x per CpG | Unreliable | High noise, many false HMRs |
| 5-10x | Acceptable | Sufficient for most analyses |
| 10-30x | Good | ENCODE standard for WGBS |
| >30x | Excellent | Diminishing returns above 30x |

### Minimum Coverage Thresholds
- **Per-CpG minimum**: Require >=5 reads covering each CpG before including in calculations
- **Per-region minimum**: Require >=4 CpGs meeting coverage threshold within each domain
- **Strand merging**: Merge + and - strand counts at each CpG (doubles effective coverage)

## Tools for Domain Calling

| Tool | Calls | Method | Reference |
|------|-------|--------|-----------|
| MethPipe | HMRs | HMM-based, 2-state model | Song et al. 2013 |
| MethylSeekR | UMRs, LMRs, PMDs | Segmentation with FDR | Burger et al. 2013 |
| DMRcate | DMRs | Kernel smoothing | Peters et al. 2021 |
| Roadmap method | UMRs, LMRs, PMDs | Thresholds + size | Schultz et al. 2015 |

### Recommended Approach (from Aggregation Skill)
For union-based aggregation of ENCODE WGBS data:
1. Call per-CpG methylation with >=5x coverage filter
2. Compute weighted average across samples (coverage-weighted)
3. Segment into UMR/LMR/PMD using Schultz 2015 thresholds
4. For HMR union: a CpG detected as hypomethylated in ANY sample enters the union catalog

## Cross-Reference with ENCODE Marks

| Domain | Expected ENCODE marks |
|--------|-----------------------|
| UMR | H3K4me3 (active promoter), ATAC-seq peak, DNase-seq peak |
| LMR | H3K4me1, H3K27ac (active enhancer), ATAC-seq peak |
| PMD | H3K9me3 (heterochromatin), low ATAC/DNase signal |
| Fully methylated | H3K36me3 (gene body), or no marks (intergenic) |

## References
- Schultz et al. 2015 — Roadmap Epigenomics methylation landscape (Nature, ~1,500 cit)
- Stadler et al. 2011 — LMRs at distal regulatory elements (Nature, ~1,200 cit)
- Lister et al. 2009 — First whole-genome methylome, PMD discovery (Nature, ~5,000 cit)
- Burger et al. 2013 — MethylSeekR UMR/LMR/PMD segmentation (Genome Biology)
- Peters et al. 2021 — DMRcate differential methylation (NAR)
