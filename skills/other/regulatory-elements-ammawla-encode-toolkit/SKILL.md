---
name: regulatory-elements
description: Discover and characterize regulatory elements (enhancers, promoters, silencers, insulators, super-enhancers) using ENCODE data and the cCRE catalog. Use when the user wants to find candidate regulatory elements, identify active enhancers in a tissue, map promoter states, classify chromatin states with ChromHMM, identify super-enhancers with ROSE, understand the functional validation hierarchy (CRISPR > MPRA > reporter), or characterize non-coding genomic regions. Covers the full workflow from ENCODE cCRE lookup through chromatin state segmentation to functional validation and enhancer-gene linkage. Use this skill for ANY regulatory element discovery, classification, or characterization task.
---

# Discover and Characterize Regulatory Elements with ENCODE

## When to Use

- User wants to find enhancers, promoters, silencers, or insulators in a specific tissue using ENCODE
- User asks about "regulatory elements", "cCREs", "enhancer discovery", "ChromHMM", or "super-enhancers"
- User needs to classify chromatin states or identify active regulatory regions from histone mark data
- User wants to use ENCODE's 926,535 cCRE catalog or run functional validation (CRISPR/MPRA/reporter)
- Example queries: "find active enhancers in liver", "classify chromatin states for my tissue", "identify super-enhancers from H3K27ac data"

Identify, classify, and functionally characterize regulatory elements using ENCODE's catalog of 926,535 human candidate cis-regulatory elements (cCREs) and layered functional genomics data.

## Scientific Rationale

**The question**: "What regulatory elements are active in my tissue of interest, and what are they doing?"

The human genome contains an estimated 1–2 million regulatory elements — far outnumbering the ~20,000 protein-coding genes. These elements (enhancers, promoters, silencers, insulators) control when, where, and how much each gene is expressed. No single biochemical assay can definitively identify a regulatory element; instead, combinatorial patterns of chromatin marks, accessibility, and TF binding are used to classify candidate elements.

### The ENCODE cCRE Registry

The ENCODE Phase 3 project (ENCODE Project Consortium 2020) established a registry of **926,535 human and 339,815 mouse cCREs** covering 7.9% and 3.4% of their respective genomes. These are classified using combinations of DNase-seq, H3K4me3, H3K27ac, and CTCF ChIP-seq signals across hundreds of biosamples. The registry is accessible via the SCREEN web server and represents the most comprehensive catalog of candidate regulatory elements in any organism.

An expanded registry (Moore et al. 2024, bioRxiv preprint) extends this to **2.35 million human cCREs** with functional characterization from STARR-seq, MPRA, and CRISPR perturbation covering >90% of human cCREs.

### Key Distinction: Candidate vs. Validated

ENCODE cCREs are **candidate** regulatory elements identified by biochemical signatures. Biochemical activity (histone marks, accessibility) is necessary but not sufficient for function. A region marked by H3K27ac is likely regulatory, but functional validation (perturbation, reporter assays) is required to confirm that it actually regulates a target gene. The gap between biochemical annotation and validated function is the central challenge.

### Literature Support

- **ENCODE Project Consortium 2020** (Nature, ~1,656 citations): Registry of 926,535 human cCREs. Introduces the SCREEN web server. [DOI](https://doi.org/10.1038/s41586-020-2493-4)
- **Kundaje et al. 2015** (Nature, ~5,810 citations): Roadmap Epigenomics — integrative analysis of 111 reference human epigenomes. Chromatin state maps across tissues. Disease variants enriched in tissue-specific epigenomic marks. [DOI](https://doi.org/10.1038/nature14248)
- **Ernst & Kellis 2012** (Nature Methods, ~2,294 citations): ChromHMM — multivariate hidden Markov model for chromatin state discovery from combinatorial histone modification patterns. [DOI](https://doi.org/10.1038/nmeth.1906)
- **Hnisz et al. 2013** (Cell, ~3,215 citations): Super-enhancer catalog across human cell types. Disease-associated variation enriched in super-enhancers of disease-relevant cells. [DOI](https://doi.org/10.1016/j.cell.2013.09.053)
- **Whyte et al. 2013** (Cell, ~2,500 citations): Defined super-enhancers as large enhancer clusters occupied by master TFs and Mediator. Introduced the ROSE algorithm. [DOI](https://doi.org/10.1016/j.cell.2013.03.035)
- **Shlyueva et al. 2014** (Nature Reviews Genetics, ~1,200 citations): Authoritative review of enhancer sequence properties, chromatin signatures, genome-wide prediction, and high-throughput activity assays. [DOI](https://doi.org/10.1038/nrg3682)
- **Schoenfelder & Fraser 2019** (Nature Reviews Genetics, ~869 citations): How enhancer-promoter interactions are established through 3D genome architecture (TADs, CTCF loops). [DOI](https://doi.org/10.1038/s41576-019-0128-0)
- **Visel et al. 2007** (Nucleic Acids Research, ~1,079 citations): VISTA Enhancer Browser — in vivo transgenic mouse validation of enhancers. 4,500+ experiments. [DOI](https://doi.org/10.1093/nar/gkl822)
- **Gasperini et al. 2019** (Cell, ~465 citations): CRISPRi screen of 5,920 candidate enhancers with scRNA-seq readout. Identified 664 enhancer-gene pairs. Established the "crisprQTL" framework. [DOI](https://doi.org/10.1016/j.cell.2018.11.029)
- **Yao et al. 2024** (Nature Methods, ~26 citations): ENCODE4 Functional Characterization Centers — 108 CRISPRi screens, >540,000 perturbations. Pre-designed sgRNAs targeting 3.27M ENCODE SCREEN cCREs. [DOI](https://doi.org/10.1038/s41592-024-02216-7)
- **Nasser et al. 2021** (Nature, ~468 citations): ABC model enhancer-gene maps in 131 cell types. [DOI](https://doi.org/10.1038/s41586-021-03446-x)
- **Heintzman et al. 2007** (Nature Genetics, ~2,300 citations): Discovered that H3K4me1 marks enhancers while H3K4me3 marks promoters — the foundational chromatin signature for distinguishing regulatory element classes. [DOI](https://doi.org/10.1038/ng1966)
- **Rada-Iglesias et al. 2011** (Nature, ~1,200 citations): Identified "poised enhancers" marked by H3K4me1+H3K27me3 (without H3K27ac) in hESCs. These activate during differentiation by gaining H3K27ac. [DOI](https://doi.org/10.1038/nature09692)
- **Amemiya et al. 2019** (Scientific Reports, ~1,372 citations): ENCODE Blacklist — regions producing artifactual signal across ChIP-seq, ATAC-seq, and DNase-seq. Must be filtered before any regulatory element classification. [DOI](https://doi.org/10.1038/s41598-019-45839-z)

## Step 1: Define the Element Type and Tissue Context

### ENCODE cCRE Classification System

| cCRE Class | Abbreviation | Biochemical Signature | Genomic Context | Example |
|-----------|-------------|----------------------|----------------|---------|
| Promoter-like | PLS | DNase+ H3K4me3+ (±H3K27ac) | Within 200bp of annotated TSS | Gene promoter |
| Proximal enhancer-like | pELS | DNase+ H3K27ac+ (H3K4me3-) | Within 2kb of TSS | Proximal enhancer |
| Distal enhancer-like | dELS | DNase+ H3K27ac+ (H3K4me3-) | >2kb from TSS | Distal enhancer |
| CTCF-only | CTCF-only | DNase+ CTCF+ (no H3K4me3/H3K27ac) | Any | Insulator/boundary |
| DNase-H3K4me3 | DNase-H3K4me3 | DNase+ H3K4me3+ | >200bp from TSS | Unannotated promoter-like |

### Extended Element Types (Beyond cCRE Classification)

| Element Type | Key Signatures | ENCODE Assays | Notes |
|-------------|---------------|---------------|-------|
| Active promoter | H3K4me3+ H3K27ac+ accessible | Histone ChIP-seq, ATAC/DNase | Corresponds to PLS cCREs |
| Active enhancer | H3K4me1+ H3K27ac+ H3K4me3- accessible | Histone ChIP-seq, ATAC/DNase | Corresponds to pELS/dELS |
| Poised enhancer | H3K4me1+ H3K27me3+ H3K27ac- | Histone ChIP-seq | Bivalent; may activate upon differentiation |
| Primed enhancer | H3K4me1+ only (no H3K27ac, no H3K27me3) | Histone ChIP-seq | Ready for activation but not currently active |
| Super-enhancer | Broad H3K27ac, multiple TFs, high Mediator | ChIP-seq, TF ChIP-seq | ROSE algorithm (Whyte 2013) |
| Silencer | H3K27me3+ (Polycomb) or H3K9me3+ (heterochromatin) | Histone ChIP-seq | Two distinct repressive mechanisms |
| Insulator | CTCF binding at TAD boundary | TF ChIP-seq (CTCF), Hi-C | Blocks enhancer-promoter communication |
| Stretch enhancer | >3kb H3K27ac domain (not classified as super-enhancer) | Histone ChIP-seq | Parker et al. 2013; enriched for disease variants |

Check data availability for the target tissue:
```
encode_get_facets(organ="...", biosample_type="tissue")
```

## Step 2: Search for Tissue-Specific Functional Data

### Minimal Data Requirements
For basic regulatory element identification, you need at minimum:
1. **Chromatin accessibility** (ATAC-seq or DNase-seq) — defines open chromatin
2. **H3K27ac** — distinguishes active from poised elements
3. **H3K4me3** — distinguishes promoters from enhancers

### Comprehensive Profiling
For full chromatin state classification (ChromHMM), collect all available marks:

```
# Core marks (essential)
encode_search_experiments(assay_title="Histone ChIP-seq", target="H3K27ac", organ="...", biosample_type="...")
encode_search_experiments(assay_title="Histone ChIP-seq", target="H3K4me3", organ="...", biosample_type="...")
encode_search_experiments(assay_title="Histone ChIP-seq", target="H3K4me1", organ="...", biosample_type="...")
encode_search_experiments(assay_title="Histone ChIP-seq", target="H3K27me3", organ="...", biosample_type="...")

# Extended marks (important for ChromHMM)
encode_search_experiments(assay_title="Histone ChIP-seq", target="H3K36me3", organ="...", biosample_type="...")
encode_search_experiments(assay_title="Histone ChIP-seq", target="H3K9me3", organ="...", biosample_type="...")

# Accessibility
encode_search_experiments(assay_title="ATAC-seq", organ="...", biosample_type="...")
encode_search_experiments(assay_title="DNase-seq", organ="...", biosample_type="...")

# TF binding (for super-enhancers and insulator identification)
encode_search_experiments(assay_title="TF ChIP-seq", target="CTCF", organ="...", biosample_type="...")
encode_search_experiments(assay_title="TF ChIP-seq", target="p300", organ="...", biosample_type="...")
```

### Download Peak Files
For each passing experiment:
```
encode_list_files(
    experiment_accession="ENCSR...",
    file_format="bed",
    output_type="IDR thresholded peaks",
    assembly="GRCh38",
    preferred_default=True
)
```

**Note**: H3K27me3, H3K9me3, and H3K36me3 produce **broad peaks** (broadPeak format), not narrow peaks. Use `output_type="replicated peaks"` for these marks.

**ENCODE Blacklist filtering (required)**: Before using any peak or signal files, remove regions overlapping the ENCODE Blacklist (Amemiya et al. 2019, Scientific Reports, 1,372 citations). Blacklisted regions produce artifactual signal in ChIP-seq, ATAC-seq, and DNase-seq assays — they will appear as regulatory elements if not removed. This step is essential before ChromHMM, cCRE overlap analysis, or any regulatory element classification.
- Human GRCh38: `hg38-blacklist.v2.bed.gz` from [Boyle-Lab/Blacklist](https://github.com/Boyle-Lab/Blacklist)
- Mouse mm10: `mm10-blacklist.v2.bed.gz`
- Filter with: `bedtools intersect -v -a peaks.bed -b blacklist.bed > peaks.filtered.bed`

Track all experiments:
```
encode_track_experiment(accession="ENCSR...", notes="regulatory element discovery - [tissue]")
```

## Step 3: ChromHMM Chromatin State Segmentation

ChromHMM (Ernst & Kellis 2012) uses a multivariate hidden Markov model to segment the genome into chromatin states based on combinatorial histone modification patterns. This is the standard approach for genome-wide regulatory element classification.

### Standard ChromHMM Models

**5-mark model** (most common, used by Roadmap Epigenomics):
Uses H3K4me3, H3K4me1, H3K36me3, H3K27me3, H3K9me3

Produces 15 or 18 states:

| State | Marks Present | Interpretation |
|-------|-------------|----------------|
| TssA | H3K4me3 | Active TSS |
| TssAFlnk | H3K4me1 | Flanking active TSS |
| TxFlnk | H3K4me1 | Transcription at gene 5' and 3' |
| Tx | H3K36me3 | Strong transcription |
| TxWk | (weak H3K36me3) | Weak transcription |
| EnhG | H3K4me1 + H3K36me3 | Genic enhancers |
| Enh | H3K4me1 | Enhancers |
| ZNF/Rpts | H3K9me3 + H3K36me3 | ZNF genes & repeats |
| Het | H3K9me3 | Heterochromatin |
| TssBiv | H3K4me3 + H3K27me3 | Bivalent/poised TSS |
| BivFlnk | H3K4me1 + H3K27me3 | Flanking bivalent TSS/enhancer |
| EnhBiv | H3K4me1 + H3K27me3 | Bivalent enhancer |
| ReprPC | H3K27me3 | Repressed Polycomb |
| ReprPCWk | (weak H3K27me3) | Weak repressed Polycomb |
| Quies | (no marks) | Quiescent/low |

**Extended model** (6+ marks including H3K27ac):
Adding H3K27ac allows distinguishing active from poised enhancers and promoters.

### When ChromHMM is Available vs. Needed
- **Roadmap Epigenomics** (Kundaje et al. 2015) provides pre-computed ChromHMM states for 111 reference epigenomes — check if your tissue is covered before running de novo
- **ENCODE SCREEN** provides cCRE classifications that serve a similar purpose
- **De novo ChromHMM** is needed when: your tissue is not in Roadmap, you have extended mark panels, or you want to compare states across conditions

## Step 4: Super-Enhancer Identification

Super-enhancers are large clusters of enhancers (typically >10kb) with exceptionally high levels of H3K27ac, Mediator binding, and master TF occupancy. They drive expression of cell-identity genes and are enriched for disease-associated variants (Hnisz et al. 2013).

### ROSE Algorithm (Whyte et al. 2013)
The Rank Ordering of Super-Enhancers (ROSE) algorithm:
1. Identifies H3K27ac peaks (or Mediator ChIP-seq peaks)
2. Stitches peaks within 12.5kb of each other (excluding promoters within ±2kb of TSS)
3. Ranks stitched enhancers by total H3K27ac signal
4. Identifies the inflection point in the signal vs. rank curve
5. Regions above the inflection point = super-enhancers

### ENCODE Data Needed
```
# H3K27ac for super-enhancer calling
encode_search_experiments(assay_title="Histone ChIP-seq", target="H3K27ac", organ="...", biosample_type="...")

# BRD4 or MED1 ChIP-seq (if available) for validation
encode_search_experiments(assay_title="TF ChIP-seq", target="BRD4", organ="...", biosample_type="...")
```

### Super-Enhancer Caveats
- The stitching distance (12.5kb) and inflection point threshold are somewhat arbitrary
- Super-enhancer vs. stretch enhancer vs. large enhancer cluster — terminology varies by publication
- Not all highly-ranked H3K27ac regions are "super" in biological importance
- Disease variant enrichment is well-established (Hnisz et al. 2013) but the mechanism (sensitivity to perturbation) is debated

## Step 5: Functional Validation Hierarchy

Not all biochemically-defined regulatory elements are functionally validated. The validation hierarchy, in decreasing order of confidence:

### Level 1: Genetic Perturbation (Highest Confidence)
- **CRISPRi/CRISPRa screens**: Direct loss/gain-of-function in endogenous context. Gasperini et al. 2019 tested 5,920 enhancers; ENCODE4 (Yao et al. 2024) tested >540,000 perturbations across 108 screens.
- **CRISPR deletion/mutagenesis**: Complete removal or specific mutation of the element
- **Limitation**: Limited to cell lines amenable to CRISPR delivery; cannot test in primary tissue

Search for ENCODE perturbation data:
```
encode_search_experiments(assay_title="CRISPR screen", organ="...", biosample_type="...")
encode_search_experiments(perturbed=True, organ="...")
```

### Level 2: Reporter Assays (High Confidence for Activity, Not Endogenous Context)
- **STARR-seq**: Self-transcribing active regulatory region sequencing — tests thousands of candidates in parallel
- **MPRA**: Massively parallel reporter assay — tests element activity outside genomic context
- **Limitation**: Removes element from its native chromatin environment; may not reflect endogenous regulation

```
encode_search_experiments(assay_title="STARR-seq", organ="...", biosample_type="...")
encode_search_experiments(assay_title="MPRA", organ="...", biosample_type="...")
```

### Level 3: In Vivo Validation (High Confidence, Low Throughput)
- **VISTA Enhancer Browser** (Visel et al. 2007): Transgenic mouse LacZ reporter assays at E11.5. 4,500+ experiments. Gold standard for developmental enhancers.
- **Limitation**: Only embryonic day 11.5 mouse; tissue-restricted expression may be missed

### Level 4: Biochemical Signatures (Correlative, Highest Throughput)
- **ENCODE cCREs**: Histone marks + accessibility + CTCF binding
- **ChromHMM states**: Combinatorial chromatin patterns
- **Limitation**: Biochemical activity is necessary but not sufficient for function

### Practical Guidance
For most analyses, Level 4 (biochemical) is the starting point. Level 1–3 validation data exists for a minority of elements. When available, always check:
1. Does the element overlap a validated region from ENCODE CRISPR screens?
2. Does it show activity in STARR-seq or MPRA?
3. Is it in the VISTA database (for developmental enhancers)?

## Step 6: Enhancer-Gene Linkage

Identifying the target gene of an enhancer is critical. Enhancers can regulate genes >1 Mb away, skipping intervening genes.

### ABC Model (Nasser et al. 2021)
Activity-By-Contact model = Enhancer Activity (H3K27ac × ATAC) × Contact Frequency (Hi-C)
- Available for 131 cell types/tissues
- Best current method for genome-wide enhancer-gene prediction
- Requires ATAC-seq + H3K27ac + Hi-C for the target tissue

### Hi-C / ChIA-PET
```
encode_search_experiments(assay_title="Hi-C", organ="...", biosample_type="...")
encode_search_experiments(assay_title="ChIA-PET", organ="...", biosample_type="...")
```
- Direct measurement of 3D chromatin contacts
- ChIA-PET (Pol2 or H3K27ac) enriches for active regulatory contacts

### Correlation-Based Approaches
- Correlate enhancer activity across ENCODE biosamples with gene expression
- Requires data from multiple tissues (Roadmap Epigenomics is ideal for this)
- Higher correlation across tissues = more likely regulatory relationship

### Proximity-Based (Lowest Confidence)
- Assign enhancer to nearest gene TSS
- **Only correct ~50–60% of the time** — use only as last resort
- Always document when using proximity-based assignment

## Step 7: Cross-Resource Integration

ENCODE is the richest single resource, but compare with:

### ENCODE SCREEN
- Web interface for the cCRE registry
- Tissue-specific activity scores for each cCRE
- Pre-computed enhancer-gene predictions

### Roadmap Epigenomics (Kundaje et al. 2015)
- 111 reference epigenomes with ChromHMM states
- Broader tissue coverage than ENCODE for some tissues
- Disease variant enrichment analysis across tissues

### VISTA Enhancer Browser (Visel et al. 2007)
- In vivo validated enhancers (transgenic mouse)
- Gold standard for developmental enhancers
- Limited to E11.5 developmental stage

### FANTOM5
- CAGE-defined enhancers (bidirectionally transcribed)
- Complementary definition to ENCODE (activity-based, not mark-based)
- Useful for cross-validation of enhancer calls

## Step 8: Log Provenance

```
encode_log_derived_file(
    file_path="/path/to/regulatory_elements.bed",
    source_accessions=["ENCSR...", "ENCSR...", ...],
    description="Regulatory element catalog for [tissue]: [N] enhancers, [N] promoters, [N] super-enhancers",
    file_type="regulatory_elements",
    tool_used="ChromHMM / ROSE / bedtools intersect",
    parameters="ChromHMM 15-state model, ROSE stitching=12.5kb, GRCh38"
)
```

## Pitfalls and Edge Cases

### Biochemical ≠ Functional
- H3K27ac marks correlate with activity but do not prove function
- An element with strong H3K27ac may have no effect on any gene when deleted
- Always be explicit about whether evidence is biochemical (correlative) or functional (perturbation)

### Tissue Specificity
- ~80% of enhancers are active in only one or a few tissues (Roadmap Epigenomics)
- An element absent in your tissue may be active in an untested tissue
- Report negative results (element not found) alongside positive results

### Catalog Saturation
- ENCODE's catalog, while the largest, is not complete
- Novel regulatory elements continue to be discovered with new cell types and assays
- "Absence of evidence is not evidence of absence"

### Super-Enhancer Thresholds
- The ROSE inflection point is data-dependent and somewhat arbitrary
- Small changes in stitching distance (12.5kb) or promoter exclusion (±2kb) alter results
- Report ROSE parameters explicitly when identifying super-enhancers

### Poised/Bivalent Elements
- Bivalent elements (H3K4me1/me3 + H3K27me3) are important in development
- They may resolve to active or repressed states upon differentiation
- Be cautious about calling them "enhancers" — they are poised but not active

### CUT&RUN/CUT&Tag Data
- Newer assays with lower background than ChIP-seq
- May detect additional elements, especially low-signal ones
- But also have different artifact profiles — CUT&RUN suspect list (Nordin et al. 2023) should be applied

### Assembly and Annotation Version
- Regulatory element coordinates are assembly-specific (GRCh38 vs hg19)
- TSS annotations (for promoter-like classification) depend on gene annotation version (GENCODE)
- Document genome assembly AND gene annotation version used

## Summary Statistics to Report

For the final regulatory element catalog, report:
- Total elements identified by class (PLS, pELS, dELS, CTCF-only, super-enhancer)
- Tissue/biosample used and number of ENCODE experiments queried
- Marks available vs. marks used for classification
- ChromHMM model used (if applicable) and number of states
- Number of super-enhancers identified and top target genes
- Fraction with functional validation data (CRISPR, MPRA, STARR-seq, VISTA)
- Number with enhancer-gene predictions (ABC model, Hi-C)
- Cross-validation rate with other resources (Roadmap, FANTOM5)

## Histone Mark Interpretation Reference

For detailed biology of each histone mark (writers, erasers, readers, contradictions, cancer-specific states) and ChromHMM combinatorial state definitions, consult `skills/histone-aggregation/references/histone-marks-reference.md` (1,442 lines, 21 marks, 37 key papers).

## Walkthrough: Classifying ENCODE Regulatory Elements by Chromatin Signature

**Goal**: Use ENCODE histone marks and accessibility data to classify regulatory elements into functional categories (active enhancer, poised enhancer, active promoter, insulator, heterochromatin).
**Context**: ENCODE's candidate cis-regulatory elements (cCREs) are classified by their chromatin signature combinations.

### Step 1: Find available marks for classification

```
encode_get_facets(facet_field="target.label", organ="liver", assay_title="Histone ChIP-seq", organism="Homo sapiens")
```

Expected output:
```json
{
  "facets": {"target.label": {"H3K27ac": 6, "H3K4me3": 5, "H3K4me1": 4, "H3K27me3": 3, "CTCF": 4}}
}
```

### Step 2: Search for experiments

```
encode_search_experiments(assay_title="Histone ChIP-seq", organ="liver", target="H3K27ac", organism="Homo sapiens")
```

### Step 3: Classify elements by chromatin signature

| Signature | Classification |
|---|---|
| H3K27ac + H3K4me1 (no H3K4me3) | Active enhancer |
| H3K4me1 (no H3K27ac) | Poised enhancer |
| H3K4me3 + H3K27ac | Active promoter |
| H3K4me3 + H3K27me3 | Bivalent promoter |
| CTCF (no H3K4me1/H3K4me3) | Insulator/CTCF-only |
| H3K27me3 | Polycomb-repressed |

### Step 4: Download and intersect mark files

```
encode_download_files(accessions=["ENCFF100AC", "ENCFF200K4M1", "ENCFF300K4M3"], download_dir="/data/regulatory")
```

### Integration with downstream skills
- Classified elements feed into → **peak-annotation** for gene assignment
- Active enhancers connect to → **motif-analysis** for TF prediction
- Bivalent promoters inform → **disease-research** for developmental disease
- Classifications validated by → **quality-assessment** QC metrics

## Code Examples

### 1. Find CTCF data for insulator classification
```
encode_search_experiments(assay_title="TF ChIP-seq", organ="liver", target="CTCF", organism="Homo sapiens")
```

Expected output:
```json
{
  "total": 4,
  "results": [{"accession": "ENCSR500CTF", "target": "CTCF", "biosample_summary": "liver"}]
}
```

### 2. List preferred peak files
```
encode_list_files(accession="ENCSR500CTF", file_format="bed", output_type="IDR thresholded peaks", assembly="GRCh38")
```

Expected output:
```json
{
  "files": [{"accession": "ENCFF600CTF", "output_type": "IDR thresholded peaks", "file_size_mb": 0.5}]
}
```

### 3. Track regulatory classification experiments
```
encode_track_experiment(accession="ENCSR500CTF", notes="Liver CTCF for insulator classification in regulatory element mapping")
```

Expected output:
```json
{"status": "tracked", "accession": "ENCSR500CTF"}
```

## Related Skills

- `variant-annotation` — Annotating genetic variants with regulatory element overlap
- `multi-omics-integration` — Combining regulatory elements with expression data and TF binding
- `histone-aggregation` — Aggregating histone ChIP-seq peaks across samples
- `accessibility-aggregation` — Aggregating ATAC-seq/DNase-seq peaks across samples
- `epigenome-profiling` — Building comprehensive epigenomic profiles
- `quality-assessment` — Evaluating ENCODE experiment quality for regulatory element analysis
- `disease-research` — Regulatory elements are central to disease variant interpretation
- `single-cell-encode` — Cell type-resolved scATAC-seq provides cell type-specific regulatory element catalogs
- `compare-biosamples` — Comparing regulatory elements across tissues is a primary use case
- `hic-aggregation` — Hi-C data enables enhancer-gene linkage for regulatory element annotation
- `methylation-aggregation` — DNA methylation at regulatory elements (hypomethylation at active enhancers) is a key signature
- `data-provenance` — Document all regulatory element discovery parameters for reproducibility
- `ucsc-browser` — Retrieve ENCODE cCRE tracks and TF binding clusters from UCSC for regulatory annotation
- `ensembl-annotation` — Ensembl Regulatory Build provides independent classification of regulatory features
- `gnomad-variants` — Gene constraint scores help prioritize regulatory elements near constrained genes
- `motif-analysis` — Discover TF motifs enriched in regulatory peaks using HOMER and MEME
- `peak-annotation` — Annotate peaks with genomic features (promoter, enhancer, intergenic)
- `jaspar-motifs` — Validate TF binding in regulatory elements using JASPAR matrix profiles
- `publication-trust` — Verify literature claims backing analytical decisions

## Presenting Results

- Present regulatory elements as: region | chr:start-end | element type | supporting marks | confidence. Include the number of supporting assays. Suggest: "Would you like to annotate these elements with nearby genes?"

## For the request: "$ARGUMENTS"
