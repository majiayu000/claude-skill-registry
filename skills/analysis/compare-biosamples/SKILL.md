---
name: compare-biosamples
description: Compare ENCODE experiments across different biosamples, tissues, or cell lines to identify tissue-specific regulatory patterns. Use when the user wants cross-tissue comparison, cell-type comparison, tissue-specific elements, differential chromatin, biosample matching, disease vs normal comparison, developmental time course, constitutive vs variable regulation, or multi-tissue data availability mapping. Handles batch effect detection, biosample hierarchy, and comparison design.
---

# Compare ENCODE Data Across Biosamples

## When to Use

- User wants to compare ENCODE experiments across different tissues, cell lines, or biosamples
- User asks about "tissue comparison", "cell-type differences", "tissue-specific enhancers", or "cross-tissue"
- User needs to identify constitutive vs tissue-specific regulatory elements
- User wants to map data availability across multiple biosamples before integrative analysis
- Example queries: "compare H3K27ac between liver and pancreas", "what marks are tissue-specific?", "find constitutive promoters across all tissues"

Help the user systematically compare data availability and experiments across different biosamples to identify tissue-specific regulatory patterns, constitutive elements, and cross-tissue differences.

## Scientific Rationale

Cross-biosample comparison is the foundation of understanding tissue-specific gene regulation. Regulatory elements -- particularly enhancers -- are the primary drivers of cell-type identity, with promoters being largely shared across tissues. Comparing the same assay across multiple biosamples reveals which regulatory elements are constitutive (shared) versus tissue-specific (unique to one or few cell types).

**The core question**: "Which regulatory features distinguish tissue A from tissue B, and which are shared?"

This requires careful matching of datasets, awareness of batch effects, and understanding of the biosample hierarchy to avoid confounding biological signal with technical variation.

## Literature Foundation

| # | Reference | Key Contribution |
|---|-----------|-----------------|
| 1 | Roadmap Epigenomics Consortium 2015, Nature, DOI:10.1038/nature14248 (~5,810 cit) | Generated 111 reference epigenomes across tissues/cell types; established the framework for cross-tissue epigenomic comparison. Showed that enhancer chromatin states are the most tissue-variable elements. |
| 2 | ENCODE Phase 3 2020, Nature, DOI:10.1038/s41586-020-2493-4 (~1,656 cit) | Expanded functional annotations to 1.3M candidate cis-regulatory elements (cCREs) across hundreds of biosamples; defined tissue-activity indices for regulatory elements. |
| 3 | Andersson et al. 2014, Nature, DOI:10.1038/nature12787 (~1,500 cit) | FANTOM5 atlas of active enhancers across 808 samples; demonstrated that only ~5% of enhancers are active across all tissues, with the majority being highly tissue-specific. |
| 4 | Heintzman et al. 2009, Nature, DOI:10.1038/nature07917 (~2,200 cit) | Showed histone modifications distinguish cell types: H3K4me1/H3K27ac at enhancers are the most discriminating tissue-specific marks, while H3K4me3 at promoters is largely shared. |
| 5 | Thurman et al. 2012, Nature, DOI:10.1038/nature11232 (~2,000 cit) | Mapped accessible chromatin across 125 cell types; demonstrated that DNase I hypersensitive sites define cell-type identity and that accessibility patterns cluster by tissue of origin. |
| 6 | Leek et al. 2010, Nat Rev Genet, DOI:10.1038/nrg2825 (~1,200 cit) | Comprehensive review of batch effects in genomic data; showed that lab, platform, and processing date can dominate biological variation if not properly controlled. |
| 7 | Forrest et al. 2014, Nature, DOI:10.1038/nature13182 (~1,100 cit) | FANTOM5 promoter-level expression atlas across 975 samples; demonstrated that promoter usage (not just gene expression) is tissue-specific and defines cell identity. |

## Tissue-Specific Regulation Principles

Understanding what varies across tissues and what does not is essential before designing a comparison.

### What Is Shared vs Tissue-Specific (Heintzman 2009; Andersson 2014)

| Feature | Cross-Tissue Behavior | Implication for Comparison |
|---------|----------------------|---------------------------|
| **Promoters (H3K4me3)** | Largely shared (~70% active in most tissues) | Poor discriminators between tissues |
| **Enhancers (H3K27ac + H3K4me1)** | Highly tissue-specific (~5% shared across all tissues) | Best discriminators; focus comparison here |
| **Chromatin accessibility (ATAC/DNase)** | Moderate tissue-specificity (~20-30% shared) | Good secondary discriminator; clusters by tissue of origin |
| **Polycomb repression (H3K27me3)** | Tissue-specific (marks silenced developmental genes) | Useful for identifying repressed lineage programs |
| **Gene expression (RNA-seq)** | Moderate tissue-specificity | Housekeeping genes shared; tissue-specific TFs are key |
| **CTCF binding** | Largely constitutive (~70% conserved) | Defines structural boundaries; less tissue-variable |
| **DNA methylation** | Bimodal; enhancers show tissue-variable methylation | Hypomethylation at active enhancers is tissue-specific |

### Key Insight

H3K27ac at enhancers is the single most informative mark for distinguishing tissues (Heintzman et al. 2009, Roadmap 2015). If the user can only compare one mark across tissues, H3K27ac should be the first choice, followed by chromatin accessibility (ATAC-seq or DNase-seq).

## ENCODE Biosample Hierarchy

| Level | Description | Biological Relevance | Reproducibility | Caveats |
|-------|-------------|---------------------|-----------------|---------|
| **Tissue** | Primary tissue from donor (e.g., pancreas, liver) | Highest -- in vivo biology preserved | Lower -- donor variation, cell-type heterogeneity | Mixed cell populations; composition varies by donor age/sex/health |
| **Primary cell** | Cells isolated from tissue (e.g., hepatocytes, islets) | High -- enriched for cell type | Moderate -- isolation stress, limited passages | Isolation method alters phenotype; culture conditions matter |
| **Cell line** | Immortalized cells (e.g., K562, HepG2, GM12878) | Lower -- transformed phenotype | Highest -- clonal, reproducible | May not represent normal tissue biology; passage number matters |
| **In vitro differentiated** | Cells derived from stem cells (e.g., iPSC-derived cardiomyocytes) | Moderate -- model system | Moderate -- protocol-dependent | Differentiation efficiency varies; often immature phenotype |
| **Organoid** | 3D self-organizing structures | Moderate-high -- recapitulates tissue architecture | Lower -- heterogeneous | Emerging data type in ENCODE; limited coverage |

### Tier 1 Cell Lines (Most Comprehensive ENCODE Data)

| Cell Line | Origin | Cancer/Normal | Best For |
|-----------|--------|--------------|----------|
| **K562** | Chronic myelogenous leukemia | Cancer | Hematopoietic chromatin, TF binding, 3D genome |
| **GM12878** | Lymphoblastoid (EBV-transformed B cells) | Transformed-normal | Immune regulation, 3D genome (Rao et al. 2014 Hi-C reference) |
| **H1-hESC** | Human embryonic stem cells | Normal | Developmental regulation, bivalent chromatin |

These three cell lines have the most complete multi-omic profiling in ENCODE. They are excellent positive controls for verifying comparison pipelines before applying to user-specific tissues.

### Biosample Comparability Rules

- **Same biosample type preferred**: Compare tissue-to-tissue, cell line-to-cell line
- **Cross-type comparisons require caution**: Cell line vs tissue introduces both biological and technical confounders
- **Donor matching**: When comparing tissues, match for life_stage, sex, and age when possible
- **Passage number matters for cell lines**: Different passages of the same cell line can diverge epigenomically

## Step 1: Define the Comparison Design

Clarify the comparison type with the user. Each design has different requirements:

### Comparison Design Patterns

| Design | Description | Required Matching | Key Tools | Best File Types |
|--------|-------------|-------------------|-----------|----------------|
| **Cross-tissue (same assay)** | Same mark/assay in different organs | Same assay, same target, same assembly, same biosample_type | `encode_search_experiments`, `encode_get_facets` | IDR thresholded peaks, fold change over control |
| **Multi-omic (same tissue)** | Multiple assays in one biosample | Same biosample_term_name, same assembly | `encode_get_facets`, `encode_search_experiments` | Depends on assay |
| **Disease vs normal** | Pathological vs healthy tissue | Same organ, same assay, matched demographics | `encode_search_experiments` with biosample filter | IDR thresholded peaks, gene quantifications |
| **Developmental time course** | Same tissue at different life stages | Same organ, same assay, different life_stage | `encode_search_experiments` with life_stage filter | Signal tracks, gene quantifications |
| **Cell line vs primary tissue** | Transformed vs in vivo | Same organ of origin, same assay | `encode_search_experiments`, `encode_compare_experiments` | IDR thresholded peaks |
| **Cross-species** | Human vs mouse homologous tissues | Same organ, same assay, different organism | `encode_search_experiments` with organism filter | Requires liftOver; use signal tracks |

Ask the user: "What tissues/cell types are you comparing, and what assay are you focusing on?"

## Step 2: Map Data Availability Across Biosamples

Use `encode_get_facets` to build an availability matrix before searching for specific experiments.

### 2a. Check What Exists for Each Biosample

```
# For each tissue of interest, discover available assays and targets
encode_get_facets(organ="pancreas")
encode_get_facets(organ="liver")
encode_get_facets(organ="brain")
```

### 2b. Check What Exists for a Specific Assay Across Tissues

```
# See which organs have Histone ChIP-seq data
encode_get_facets(assay_title="Histone ChIP-seq")

# See which organs have ATAC-seq data
encode_get_facets(assay_title="ATAC-seq")
```

### 2c. Build the Availability Matrix

Present to the user a matrix like:

| Assay / Target | Pancreas tissue | Liver tissue | Brain tissue | K562 | GM12878 |
|---------------|:-:|:-:|:-:|:-:|:-:|
| H3K27ac ChIP-seq | 3 exp | 5 exp | 8 exp | 12 exp | 10 exp |
| H3K4me3 ChIP-seq | 2 exp | 4 exp | 6 exp | 11 exp | 9 exp |
| ATAC-seq | 1 exp | 3 exp | 5 exp | 4 exp | 3 exp |
| RNA-seq | 4 exp | 6 exp | 10 exp | 15 exp | 8 exp |
| WGBS | 0 | 2 exp | 3 exp | 2 exp | 2 exp |

Highlight gaps: "Pancreas has no WGBS data -- comparison of methylation patterns will be limited to liver and brain."

## Step 3: Identify Matched Datasets

For a valid cross-tissue comparison, datasets must be matched on technical parameters. Search each tissue:

```
encode_search_experiments(
    assay_title="Histone ChIP-seq",
    target="H3K27ac",
    organ="pancreas",
    biosample_type="tissue",
    limit=50
)
```

### Matching Criteria Checklist

For each experiment pair across tissues, verify:

| Parameter | Must Match? | How to Check |
|-----------|:-:|-------------|
| Assay title | Yes | Search filter |
| Target (for ChIP) | Yes | Search filter |
| Genome assembly | Yes | File metadata; use GRCh38 |
| Biosample type | Recommended | Search filter |
| Organism | Yes | Search filter |
| Life stage | Recommended | Experiment metadata |
| Sex | Preferred | Experiment metadata |
| Pipeline version | Preferred | `encode_get_experiment` |
| Sequencing depth | Comparable (within 2x) | File metadata |
| Read length | Preferred | File metadata |

## Step 4: Check Pairwise Compatibility

Track candidate experiments and use `encode_compare_experiments` for each cross-tissue pair:

```
# Track experiments from each tissue
encode_track_experiment(accession="ENCSR_pancreas")
encode_track_experiment(accession="ENCSR_liver")

# Check compatibility
encode_compare_experiments(
    accession1="ENCSR_pancreas",
    accession2="ENCSR_liver"
)
```

The compatibility tool checks:
- Organism match
- Assembly match
- Assay type match
- Biosample differences (expected for cross-tissue comparison)
- Target match
- Replication strategy
- Lab differences (potential batch effect source)

**For cross-tissue comparison**: Biosample mismatch is *expected* -- it is the variable of interest. Focus on ensuring all other parameters match.

## Step 5: Assess and Control for Batch Effects (Leek et al. 2010)

Batch effects are the most common confounder in cross-biosample comparisons. When experiments come from different labs, platforms, or processing dates, technical variation can dominate biological signal.

### Known Batch Effect Sources

| Source | Impact | Detection Method |
|--------|--------|-----------------|
| **Lab of origin** | High -- different protocols, antibodies, cell handling | Check `lab` field; PCA of signal should not cluster by lab |
| **Sequencing platform** | Moderate -- read quality, GC bias | Check `platform` in file metadata |
| **Library preparation date** | Moderate -- reagent lots, operator variation | Check experiment date_released |
| **Antibody lot** | High for ChIP-seq -- different enrichment profiles | Check antibody_lot_reviews in experiment metadata |
| **Pipeline version** | Low-moderate -- different peak calling parameters | Check analysis pipeline version |
| **Read length** | Low-moderate -- affects mappability | Check read_length in file metadata |

### How to Detect Batch Effects

1. **PCA of signal**: If the first principal component of signal tracks separates by lab (not by tissue), batch effects dominate
2. **Check housekeeping loci**: H3K4me3 at housekeeping promoters should be consistent across tissues. If it varies, suspect technical confounders.
3. **CTCF as control**: CTCF binding is ~70% constitutive. If CTCF shows tissue-specific differences that correlate with lab, suspect batch effects.

### How to Mitigate

- **Use ENCODE uniform pipeline outputs**: All experiments processed through the same pipeline are more comparable than custom-processed data
- **Match pipeline versions**: Use files processed by the same pipeline version when possible
- **Use fold-change-over-control signal tracks**: Normalized to input, reducing depth and background differences
- **Document all technical differences**: In the comparison metadata, record every known technical difference between datasets

## Step 6: Select Comparable Files

For each matched experiment, select files that are directly comparable:

```
# Get the recommended files for each experiment
encode_list_files(
    experiment_accession="ENCSR...",
    preferred_default=True,
    assembly="GRCh38"
)
```

**ENCODE Blacklist filtering (required before comparison)**: Before any cross-tissue comparison, remove peaks and signal in ENCODE Blacklist regions (Amemiya et al. 2019, Scientific Reports, 1,372 citations). Blacklisted regions produce artifactual signal that appears consistent across tissues, inflating the count of "constitutive" elements. They can also show variable signal due to copy number differences between cell lines, creating false tissue-specific hits. Filter before comparison:
- Human GRCh38: `hg38-blacklist.v2.bed.gz` from [Boyle-Lab/Blacklist](https://github.com/Boyle-Lab/Blacklist)
- Mouse mm10: `mm10-blacklist.v2.bed.gz`
- Filter with: `bedtools intersect -v -a peaks.bed -b blacklist.bed > peaks.filtered.bed`

### File Selection by Comparison Goal

| Comparison Goal | File Type | Output Type | Why |
|----------------|-----------|-------------|-----|
| Peak overlap / tissue-specific peaks | bed narrowPeak | IDR thresholded peaks | Binary: present or absent in each tissue |
| Quantitative signal comparison | bigWig | fold change over control | Normalized signal; comparable across experiments |
| Differential expression | tsv | gene quantifications | TPM/FPKM for cross-tissue expression comparison |
| Chromatin state annotation | bed narrowPeak | All histone marks | Required for ChromHMM/chromatin state analysis |
| Visualization / heatmaps | bigWig | signal of unique reads | Raw signal for deepTools or genome browser |

### Critical: Use Same Output Type Across All Tissues

Do NOT mix IDR thresholded peaks from one tissue with pseudoreplicated peaks from another. This introduces systematic differences in peak number and stringency that confound biological comparison.

## Step 7: Build the Comparison Matrix

Assemble a structured metadata table for all experiments in the comparison:

```
| Biosample | Organ | Type | Assay | Target | Accession | Audit | Depth | Lab | Pipeline |
|-----------|-------|------|-------|--------|-----------|-------|-------|-----|----------|
| Pancreas  | pancreas | tissue | Histone ChIP | H3K27ac | ENCSR... | clean | 22M | Bernstein | v2.1 |
| Liver     | liver | tissue | Histone ChIP | H3K27ac | ENCSR... | warn  | 18M | Snyder | v2.1 |
| Brain     | brain | tissue | Histone ChIP | H3K27ac | ENCSR... | clean | 25M | Bernstein | v2.1 |
```

Use `encode_summarize_collection` after tracking all experiments for a bird's-eye view:

```
# After tracking all experiments
encode_summarize_collection()
```

Flag potential issues in the matrix:
- Depth differences >2x between tissues
- Different labs (batch effect risk)
- Different pipeline versions
- WARNING or ERROR audit flags
- Missing data for some tissues (incomplete comparison)

## Step 8: Suggest Analysis Strategies by Comparison Type

### Tissue-Specific Elements

Peaks (or signals) present in one tissue but absent in others. The canonical approach:

1. Download IDR thresholded peaks for each tissue
2. Use `bedtools intersect -v` to find peaks unique to each tissue
3. Annotate tissue-specific peaks with genomic features (promoter, enhancer, intergenic)
4. Expect: enhancer peaks will be the most tissue-variable (Heintzman 2009, Andersson 2014)

### Constitutive Elements

Peaks present across ALL tissues compared:

1. Use `bedtools multiintersect` across all tissue peak files
2. Filter for regions present in all (or N-1) tissues
3. Expect: promoters and CTCF sites will dominate constitutive elements
4. Use as positive controls to verify comparison pipeline

### Differential Quantitative Analysis

For continuous signal comparison across tissues:

1. Download fold-change-over-control bigWig files for each tissue
2. Use deepTools `multiBigwigSummary` to compute genome-wide signal matrix
3. PCA and hierarchical clustering to verify tissues separate by biology (not batch)
4. Use deepTools `plotHeatmap` at tissue-specific peak sets to visualize differences

### Disease vs Normal Comparison

1. Match disease and normal samples on demographics (age, sex, life_stage)
2. Use `encode_search_experiments` with treatment or biosample filters
3. Be aware that disease samples may have altered cell-type composition
4. Differential peaks may reflect composition changes, not regulatory rewiring

### Developmental Time Course

1. Use life_stage filter to find experiments at different developmental stages
2. Order by developmental time (embryonic, child, adult)
3. Track which elements gain or lose activity over development
4. Roadmap Epigenomics (2015) provides reference developmental trajectories

## Step 9: Document and Track with Provenance

Record the entire comparison design and results:

```
# Track all experiments in the comparison
encode_track_experiment(accession="ENCSR_tissue1", notes="Cross-tissue H3K27ac comparison - pancreas")
encode_track_experiment(accession="ENCSR_tissue2", notes="Cross-tissue H3K27ac comparison - liver")

# Log any derived comparison files
encode_log_derived_file(
    file_path="/path/to/tissue_specific_peaks.bed",
    source_accessions=["ENCSR_tissue1", "ENCSR_tissue2"],
    description="Pancreas-specific H3K27ac peaks not found in liver",
    file_type="differential_peaks",
    tool_used="bedtools intersect v2.31.0",
    parameters="bedtools intersect -a pancreas.bed -b liver.bed -v"
)

# Link relevant publications
encode_link_reference(
    experiment_accession="ENCSR_tissue1",
    reference_type="doi",
    reference_id="10.1038/nature14248",
    description="Roadmap Epigenomics reference for cross-tissue comparison methodology"
)
```

## Pitfalls and Common Mistakes

1. **Confounding batch with biology**: If all pancreas experiments come from Lab A and all liver experiments from Lab B, you cannot distinguish tissue differences from lab effects. Check lab metadata before interpreting any cross-tissue difference. Leek et al. (2010) showed that batch effects can dominate over 50% of total variation.

2. **Mixing biosample types**: Comparing K562 (cell line) H3K27ac with primary liver tissue H3K27ac conflates transformation-driven changes with tissue-specific regulation. Always compare within the same biosample type when possible.

3. **Assembly mismatch**: ALL files in a comparison must use the same genome assembly. GRCh38 and hg19 coordinates are NOT compatible. Use `encode_compare_experiments` to catch this.

4. **Ignoring cell-type heterogeneity**: Bulk tissue samples contain mixed cell populations. A "pancreas-specific" peak might actually be present in a minority cell type (e.g., delta cells). Single-cell data (scATAC-seq, scRNA-seq) can deconvolve this, but is not available for all tissues in ENCODE.

5. **Depth-driven false differences**: A deeply sequenced tissue will have more peaks called than a shallowly sequenced one, even if the underlying biology is identical. Always check sequencing depth and prefer normalized signal (fold change over control) for quantitative comparisons.

6. **Incomplete panel comparison**: Comparing 5 histone marks in tissue A but only 3 in tissue B produces a biased view. Document which marks are available in each tissue and restrict comparison to the intersection of available assays.

## Walkthrough: Comparing Epigenomic Landscapes Between Normal and Cancer Tissues

**Goal**: Systematically compare ENCODE epigenomic data between normal tissue and cancer cell lines to identify disease-specific regulatory changes.
**Context**: Comparing biosamples reveals which regulatory elements are gained or lost in disease states.

### Step 1: Find experiments for both biosamples

```
encode_search_experiments(assay_title="Histone ChIP-seq", organ="liver", target="H3K27ac", organism="Homo sapiens")
```

Expected output:
```json
{
  "total": 8,
  "results": [
    {"accession": "ENCSR100LIV", "biosample_summary": "liver", "target": "H3K27ac"},
    {"accession": "ENCSR200HEP", "biosample_summary": "HepG2", "target": "H3K27ac"}
  ]
}
```

### Step 2: Compare the two experiments

```
encode_compare_experiments(accession_1="ENCSR100LIV", accession_2="ENCSR200HEP")
```

Expected output:
```json
{
  "comparison": {
    "shared": {"assay": "Histone ChIP-seq", "target": "H3K27ac", "organism": "Homo sapiens"},
    "differences": {
      "biosample": ["liver", "HepG2"],
      "biosample_type": ["tissue", "cell line"]
    }
  }
}
```

### Step 3: Download peak files for both

```
encode_download_files(accessions=["ENCFF100LIV", "ENCFF200HEP"], download_dir="/data/comparison")
```

### Step 4: Identify differential peaks

```bash
bedtools intersect -v -a liver_peaks.bed -b hepg2_peaks.bed > liver_specific.bed
bedtools intersect -v -a hepg2_peaks.bed -b liver_peaks.bed > hepg2_specific.bed
bedtools intersect -a liver_peaks.bed -b hepg2_peaks.bed > shared_peaks.bed
```

**Interpretation**: HepG2-specific H3K27ac peaks mark cancer-gained enhancers. Liver-specific peaks mark enhancers lost in cancer.

### Integration with downstream skills
- Differential peaks feed into **peak-annotation** for gene assignment
- Biosample-specific enhancers connect to **disease-research**
- Cell composition differences contextualized by **cellxgene-context**
- Expression differences validated via **gtex-expression**

## Code Examples

### 1. Compare two experiments
```
encode_compare_experiments(accession_1="ENCSR100LIV", accession_2="ENCSR200HEP")
```

Expected output:
```json
{
  "comparison": {
    "shared": {"assay": "Histone ChIP-seq", "target": "H3K27ac"},
    "differences": {"biosample": ["liver", "HepG2"]}
  }
}
```

### 2. Find matching experiments across biosamples
```
encode_get_facets(assay_title="Histone ChIP-seq", facet_field="biosample_ontology.term_name", target="H3K27ac", organism="Homo sapiens")
```

Expected output:
```json
{
  "facets": {
    "biosample_ontology.term_name": {"K562": 8, "GM12878": 7, "HepG2": 5, "liver": 4, "brain": 3}
  }
}
```

### 3. Track compared experiments
```
encode_track_experiment(accession="ENCSR100LIV", notes="Liver H3K27ac - normal tissue control for HepG2 comparison")
```

Expected output:
```json
{"status": "tracked", "accession": "ENCSR100LIV", "notes": "Liver H3K27ac - normal tissue control for HepG2 comparison"}
```

## Integration

| This skill produces... | Feed into... | Purpose |
|---|---|---|
| Differential peak sets | **peak-annotation** | Assign biosample-specific peaks to genes |
| Biosample-specific enhancers | **disease-research** | Identify disease-gained/lost regulatory elements |
| Shared regulatory elements | **regulatory-elements** | Define constitutive vs. tissue-specific cCREs |
| Cell composition context | **cellxgene-context** | Deconvolve tissue heterogeneity effects |
| Expression differences | **gtex-expression** | Validate regulatory changes with expression data |
| Comparison metadata | **data-provenance** | Document biosample comparison analysis |
| Differential regions | **variant-annotation** | Find variants in biosample-specific regulatory elements |

## Related Skills

- **integrative-analysis**: Combine multiple data types (ChIP + RNA-seq + ATAC) within or across biosamples
- **epigenome-profiling**: Build comprehensive epigenomic profiles for individual biosamples before comparing them
- **quality-assessment**: Evaluate data quality for each experiment BEFORE including it in a cross-tissue comparison
- **histone-aggregation**: Aggregate peaks across multiple experiments for the SAME tissue before cross-tissue comparison
- **accessibility-aggregation**: Aggregate ATAC-seq/DNase-seq peaks across experiments for the SAME tissue
- **methylation-aggregation**: Aggregate DNA methylation data across experiments for cross-tissue methylation comparison
- **regulatory-elements**: Use tissue-specific peak sets to discover enhancers, promoters, and other cis-regulatory elements
- **single-cell-encode**: Cell type-resolved data can deconvolve bulk cross-tissue comparisons
- **multi-omics-integration**: Combine multiple ENCODE assay types for deeper regulatory characterization
- **data-provenance**: Document all comparison parameters, tool versions, and results for reproducibility
- **publication-trust**: Verify literature claims backing analytical decisions

## Presenting Results

- Present comparison as: metric | biosample_1 | biosample_2 | difference. Highlight significant differences. Include compatibility verdict (COMPATIBLE/WARNING/INCOMPATIBLE). Suggest: "Would you like to download the compatible experiments?"

## For the request: "$ARGUMENTS"
