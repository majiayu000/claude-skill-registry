---
name: multi-omics-integration
description: Integrate multiple ENCODE data types (RNA-seq, ATAC-seq, Histone ChIP-seq, TF ChIP-seq) for a tissue/cell type to build a comprehensive regulatory landscape. Use when the user wants to answer "what are the enhancers, promoters, and regulatory elements active in my tissue, and which transcription factors control them?" by layering expression, chromatin accessibility, histone marks, and TF binding data. Follows the Mawla et al. 2023 framework for cross-assay integration of islet cell type-specific data. Handles chromatin state annotation (ChromHMM), enhancer-gene linkage, TF motif enrichment, and cell type-specific regulatory element identification. Use for ANY multi-omic analysis, enhancer discovery, regulatory network construction, or epigenomic characterization using ENCODE data.
---

# Multi-Omics Integration of ENCODE Data

## When to Use

- User wants to integrate multiple ENCODE data types (RNA-seq + ATAC-seq + ChIP-seq) for a tissue
- User asks about "multi-omics", "integrative analysis", "regulatory landscape", or "layer epigenomic data"
- User needs to build a comprehensive view of active enhancers, promoters, and TF binding in a tissue
- User wants to combine expression with chromatin state to identify cell-type-specific regulatory networks
- Example queries: "integrate all ENCODE data for pancreas", "build a regulatory landscape for liver", "combine RNA-seq and ChIP-seq to find active enhancers"

Layer RNA-seq, ATAC-seq, Histone ChIP-seq, and TF ChIP-seq data from ENCODE to build a comprehensive regulatory landscape for a tissue or cell type.

## Scientific Rationale

**The question**: "What regulatory elements are active in my tissue, and how do expression, chromatin accessibility, histone marks, and TF binding converge to define cell identity?"

No single assay captures the full picture of gene regulation. RNA-seq tells you **what** is expressed. ATAC-seq tells you **where** chromatin is open. Histone ChIP-seq tells you **how** chromatin is modified. TF ChIP-seq tells you **who** is binding. Each assay provides one dimension; integrating them reveals the regulatory logic.

### The Framework (Mawla, van der Meulen & Huising 2023)

Mawla et al. (2023, BMC Genomics) demonstrated this integrative approach by comparing ATAC-seq chromatin accessibility between alpha, beta, and delta cells in mouse pancreatic islets. Key findings:

1. **Cell type-specific chromatin accessibility defines cell identity**: Differentially accessible regions between alpha, beta, and delta cells map to cell type-specific enhancers. Both alpha and delta cells appear poised, but repressed, from becoming beta cells.

2. **Distal-intergenic enrichment in beta cells**: Differential chromatin accessibility shows preferentially enriched distal-intergenic regions in beta cells compared to alpha or delta cells — indicating a larger enhancer repertoire.

3. **TF motif enrichment reveals regulatory logic**: Differentially accessible regions are enriched for binding motifs of known lineage-defining TFs, connecting chromatin structure to transcriptional regulation.

4. **Cross-validation with expression**: Common endocrine enhancers (accessible in all three cell types) map near genes expressed in all cell types, while cell type-specific enhancers map near differentially expressed genes.

5. **Enhancer databases as validation**: Previously discovered enhancer regions from the literature were confirmed and novel regions identified through chromatin accessibility analysis.

### Literature Support

- **Mawla, van der Meulen & Huising 2023** (BMC Genomics): Integrated ATAC-seq across alpha, beta, and delta cells. Identified common and cell type-specific enhancers. Demonstrated that chromatin accessibility patterns predict cell identity and lineage plasticity. [DOI](https://doi.org/10.1186/s12864-023-09293-6)
- **ChromHMM** (Ernst & Kellis 2017, Nature Protocols, 711 citations): The standard tool for chromatin state segmentation. Uses combinatorial patterns of histone marks to annotate genome into functional states (active promoter, enhancer, repressed, etc.). [DOI](https://doi.org/10.1038/nprot.2017.124)
- **ENCODE Phase 3** (Gorkin et al. 2020, Nature, 301 citations): Created unified chromatin state annotations across 66 mouse epigenomes. 18 chromatin states annotated. Demonstrated that bivalent chromatin is enriched in silencers and polycomb targets.
- **ENCODE cCRE Registry** (ENCODE Project Consortium 2020, Nature): Defined ~926,000 candidate cis-regulatory elements (cCREs) in the human genome classified as promoter-like, enhancer-like, or CTCF-bound, using DNase, H3K4me3, H3K27ac, and CTCF signals.
- **SCENIC+** (Gonzalez-Blas et al. 2022, Nature Methods, 369 citations): Single-cell multi-omic inference of enhancers and gene regulatory networks. Predicts genomic enhancers, upstream TFs, and target genes from joint chromatin accessibility and expression data. [DOI](https://doi.org/10.1038/s41592-023-01938-4)
- **Minnoye et al. 2021** (Nature Reviews Methods Primers, 125 citations): Comprehensive review of chromatin accessibility profiling methods. Discusses orthogonal assays needed to interpret accessible regions — enhancer-promoter proximity, TF binding, regulatory function.
- **Roadmap Epigenomics** (Kundaje et al. 2015, Nature, 4,800+ citations): Mapped chromatin states across 111 human reference epigenomes. Established the canonical histone mark signatures for functional annotation.
- **ENCODE Blacklist** (Amemiya et al. 2019, Scientific Reports, 1,372 citations): Defined problematic genomic regions to filter from all functional genomics analyses. [DOI](https://doi.org/10.1038/s41598-019-45839-z)
- **ABC Model** (Fulco et al. 2019, Nature Genetics, 800+ citations): Activity-By-Contact model for predicting enhancer-gene connections. Combines enhancer activity (H3K27ac) with Hi-C contact frequency. Outperforms proximity-based assignment. [DOI](https://doi.org/10.1038/s41588-019-0538-0)
- **ROSE** (Whyte et al. 2013, Cell, 3,000+ citations): Algorithm for identifying super-enhancers from H3K27ac or Med1 ChIP-seq signal. Regions above the inflection point in ranked signal are classified as super-enhancers. [DOI](https://doi.org/10.1016/j.cell.2013.03.035)
- **GREAT** (McLean et al. 2010, Nature Biotechnology, 3,500+ citations): Genomic Regions Enrichment of Annotations Tool. Assigns biological meaning to sets of non-coding genomic regions (enhancers, accessible regions) by analyzing nearby gene annotations. [DOI](https://doi.org/10.1038/nbt.1630)
- **GRaNIE** (Kamal et al. 2023, Molecular Systems Biology): Enhancer-mediated gene regulatory network inference. Builds GRNs based on covariation of chromatin accessibility and RNA-seq across samples, connecting TFs → enhancers → target genes. Includes GRaNPA for unbiased GRN performance evaluation. [DOI](https://doi.org/10.15252/msb.202311627)
- **Enformer** (Avsec et al. 2021, Nature Methods): Deep learning model predicting gene expression from DNA sequence by integrating long-range interactions (up to 100kb). Accurately predicts variant effects and enhancer-promoter interactions directly from sequence. Useful for validating regulatory element predictions. [DOI](https://doi.org/10.1038/s41592-021-01252-x)
- **scVI/scANVI** (Lopez et al. 2018; Xu et al. 2021, Nature Methods / MSB): Deep generative models for single-cell RNA-seq. scANVI extends scVI with semi-supervised cell type annotation. When used with scATAC-seq multiome data, provides probabilistic cell type assignments that improve regulatory element annotation. [DOI](https://doi.org/10.1038/s41592-018-0229-2)
- **Luecken et al. 2022** (Nature Methods, scIB benchmark): Atlas-level integration benchmark of 68 methods. Found scANVI, scVI, Scanorama, and scGen perform best. Provides the standard framework (14 metrics) for evaluating single-cell integration quality. [DOI](https://doi.org/10.1038/s41592-021-01336-8)

## Step 1: Define the Regulatory Question

Multi-omics integration is not a single workflow — the approach depends on the question:

| Question | Required Data Layers | Approach |
|----------|---------------------|----------|
| "What enhancers are active in my tissue?" | ATAC-seq + H3K27ac + RNA-seq | Intersection of accessible + H3K27ac+ regions near expressed genes |
| "What chromatin states exist?" | H3K4me1 + H3K4me3 + H3K27ac + H3K27me3 + H3K36me3 | ChromHMM segmentation |
| "Which TFs drive cell identity?" | ATAC-seq + TF ChIP-seq + RNA-seq | TF footprinting + motif enrichment in accessible regions |
| "What distinguishes cell type A from B?" | Cell type-resolved ATAC-seq + RNA-seq | Differential accessibility + expression correlation |
| "Where are super-enhancers?" | H3K27ac + H3K4me1 + ATAC-seq | ROSE algorithm on H3K27ac + accessibility confirmation |
| "What are poised vs. active elements?" | H3K4me1 + H3K27ac + H3K27me3 | Poised = H3K4me1+ H3K27ac- (± H3K27me3+) |
| "What is the full regulatory network?" | All layers + multiome if available | GRaNIE (bulk) or SCENIC+ (single-cell) |
| "Which variants affect regulation?" | Enhancer catalog + variant list | Enformer variant effect prediction |

Clarify with the user which question they are asking before proceeding.

## Step 2: Inventory Available Data

For each data layer, search ENCODE systematically:

### RNA-seq (Expression Layer)
```
encode_search_experiments(
    assay_title="total RNA-seq",
    organ="pancreas",
    biosample_type="tissue",
    limit=50
)
```

For cell type-resolved expression, also check:
```
encode_search_experiments(
    assay_title="total RNA-seq",
    biosample_term_name="GM12878",  # specific cell line if applicable
    limit=50
)
```

### ATAC-seq (Accessibility Layer)
```
encode_search_experiments(
    assay_title="ATAC-seq",
    organ="pancreas",
    limit=50
)
```

### Histone ChIP-seq (Modification Layer)
Search for each core mark separately:
```python
core_marks = ["H3K27ac", "H3K4me1", "H3K4me3", "H3K27me3", "H3K36me3"]
# Optionally: "H3K9me3" (heterochromatin), "H3K9ac" (active)

for mark in core_marks:
    encode_search_experiments(
        assay_title="Histone ChIP-seq",
        target=mark,
        organ="pancreas",
        limit=50
    )
```

### TF ChIP-seq (Binding Layer)
```
encode_search_experiments(
    assay_title="TF ChIP-seq",
    organ="pancreas",
    limit=100
)
```

### Summary Matrix

Present to the user a data availability matrix:

```
Data Layer      | Experiments | Biosamples | Labs | Files Available
----------------|-------------|------------|------|----------------
RNA-seq         |      N      |     N      |   N  | gene quant TSV
ATAC-seq        |      N      |     N      |   N  | narrowPeak, bigWig
H3K27ac ChIP    |      N      |     N      |   N  | narrowPeak
H3K4me1 ChIP    |      N      |     N      |   N  | narrowPeak
H3K4me3 ChIP    |      N      |     N      |   N  | narrowPeak
H3K27me3 ChIP   |      N      |     N      |   N  | broadPeak
H3K36me3 ChIP   |      N      |     N      |   N  | broadPeak
TF ChIP-seq     |      N      |     N (TFs)|   N  | narrowPeak
```

**Critical**: Flag if any data layer is missing entirely — multi-omics integration is only as strong as its weakest layer. Missing H3K27ac makes enhancer calling unreliable. Missing ATAC-seq prevents accessibility-based enhancer validation.

## Step 3: Quality-Gate and Download

### Quality Requirements Per Assay

| Assay | Key Quality Metric | Threshold |
|-------|-------------------|-----------|
| RNA-seq | Mapping rate, library complexity | >80% mapping, >15,000 genes detected |
| ATAC-seq | FRiP, TSS enrichment, fragment size | FRiP >1%, TSS enrichment >5, nucleosomal ladder |
| Histone ChIP | FRiP, NSC, RSC, NRF | FRiP >1%, NSC >1.05, RSC >0.8, NRF >0.8 |
| TF ChIP | FRiP, IDR consistency | FRiP >1%, IDR peaks available |

### Download Strategy

For each assay, download the appropriate file type:

**RNA-seq**: Gene quantifications (TSV) or signal tracks (bigWig)
```
encode_list_files(
    experiment_accession="ENCSR...",
    output_type="gene quantifications",
    assembly="GRCh38",
    preferred_default=True
)
```

**ATAC-seq / Histone ChIP-seq**: IDR thresholded peaks + signal tracks
```
encode_list_files(
    experiment_accession="ENCSR...",
    output_type="IDR thresholded peaks",
    assembly="GRCh38"
)
```

For broad histone marks (H3K27me3, H3K36me3, H3K9me3), use broadPeak instead of narrowPeak.

**TF ChIP-seq**: IDR thresholded peaks
```
encode_list_files(
    experiment_accession="ENCSR...",
    output_type="IDR thresholded peaks",
    file_format="bed",
    assembly="GRCh38"
)
```

Always filter against ENCODE Blacklist regions before any analysis:
- Human GRCh38: `hg38-blacklist.v2.bed.gz` from [Boyle-Lab/Blacklist](https://github.com/Boyle-Lab/Blacklist)
- Mouse mm10: `mm10-blacklist.v2.bed.gz`

## Step 4: Integration Approaches

### 4a. Chromatin State Annotation (ChromHMM)

If you have 5+ histone marks, ChromHMM provides the most comprehensive regulatory annotation:

**Required marks** (minimum for useful segmentation):
- H3K4me3 (active promoter)
- H3K4me1 (enhancer/poised)
- H3K27ac (active enhancer/promoter)
- H3K27me3 (polycomb repression)
- H3K36me3 (transcribed gene body)

**ChromHMM output** — 15 or 18-state model:

| State | Marks Present | Interpretation |
|-------|--------------|----------------|
| Active TSS | H3K4me3, H3K27ac | Active promoter |
| Flanking TSS | H3K4me1, H3K4me3 | Promoter-proximal |
| Strong Enhancer | H3K4me1, H3K27ac | Active enhancer |
| Weak Enhancer | H3K4me1 only | Poised/weak enhancer |
| Bivalent TSS | H3K4me3, H3K27me3 | Bivalent/poised promoter |
| Bivalent Enhancer | H3K4me1, H3K27me3 | Poised enhancer (repressed) |
| Repressed Polycomb | H3K27me3 only | Polycomb-silenced |
| Transcription | H3K36me3 | Actively transcribed gene body |
| Quiescent | None | No marks (heterochromatin or desert) |

**Validation**: Cross-reference ChromHMM states with ATAC-seq peaks:
- Active promoters and enhancers SHOULD overlap accessible chromatin
- Repressed/polycomb regions should NOT be accessible
- Discordance (accessible + repressed marks) may indicate transitional states or artifacts

### 4b. Enhancer Identification (Following Mawla et al. 2023)

Active enhancers are defined by the convergence of multiple signals:

```
ENHANCER = H3K27ac+ AND H3K4me1+ AND ATAC-seq accessible AND NOT H3K4me3+ (not promoter)
```

**Step-by-step**:
1. Start with ATAC-seq peaks (accessible chromatin catalog)
2. Intersect with H3K27ac peaks (mark of active enhancers)
3. Intersect with H3K4me1 peaks (mark of enhancer priming)
4. Subtract H3K4me3 peaks (removes promoters)
5. Subtract TSS ± 2kb (removes promoter-proximal regions)
6. Filter against blacklist

**Poised enhancers**:
```
POISED = H3K4me1+ AND H3K27ac- AND (optionally H3K27me3+)
```

**Super-enhancers**: Use the ROSE algorithm on H3K27ac signal — regions above the inflection point in a ranked H3K27ac signal plot.

### 4c. Enhancer-Gene Linkage

Linking enhancers to their target genes is one of the hardest problems in genomics. Use multiple complementary approaches:

1. **Proximity-based**: Assign enhancer to nearest TSS (simplest, ~60% accuracy)
2. **ABC Model** (Fulco et al. 2019): Activity-By-Contact — multiplies enhancer activity (H3K27ac signal) by Hi-C contact frequency to score enhancer-gene pairs. Outperforms proximity alone. Requires H3K27ac + Hi-C data.
3. **Correlation-based**: Correlate enhancer accessibility/H3K27ac signal with gene expression across conditions or cell types (requires multiple samples)
4. **Hi-C contact**: Use chromatin loops (BEDPE) to link enhancer-containing regions to promoter-containing regions (gold standard for physical interaction)
5. **ENCODE cCRE-gene links**: Use ENCODE's pre-computed regulatory element-gene associations where available

**Caveats**:
- Nearest-gene assignment fails for >40% of enhancers — many skip the nearest gene
- Correlation requires sufficient samples (>5) for statistical power
- Hi-C resolution (5–25kb) may link entire bins, not individual elements
- Multiple enhancers often regulate the same gene (redundancy)

### 4d. TF Regulatory Network

Integrate TF ChIP-seq binding with enhancer locations and expression:

1. **Overlap TF peaks with enhancers**: Which TFs bind at identified enhancers?
2. **Motif enrichment**: In ATAC-seq peaks or differentially accessible regions, what TF motifs are enriched? (HOMER, MEME-ChIP)
3. **Expression filter**: Only consider TFs whose mRNA is detected in RNA-seq for the same tissue
4. **Network construction**: TF → enhancer → target gene

**From Mawla et al. 2023**: Differentially accessible chromatin between cell types shows enriched TF motifs that correspond to known lineage-defining factors. This validates the approach of using motif enrichment in differentially accessible regions to identify regulatory TFs.

### 4d-ii. Enhancer-Mediated GRN Inference (GRaNIE)

When you have matched chromatin accessibility + RNA-seq across multiple samples (e.g., individuals), **GRaNIE** (Kamal et al. 2023) provides a principled framework for building enhancer-mediated gene regulatory networks:

1. **TF-enhancer links**: Correlate TF expression with enhancer accessibility across samples. Significant positive correlations suggest TF activates that enhancer.
2. **Enhancer-gene links**: Correlate enhancer accessibility with nearby gene expression. Significant positive correlations establish enhancer-gene regulatory connections.
3. **Combined GRN**: Chain TF → enhancer → gene into a full regulatory network.
4. **Performance evaluation**: Use GRaNPA to assess GRN quality by testing whether inferred networks predict cell-type-specific differential expression.

**When to use GRaNIE vs. SCENIC+**:
- **GRaNIE**: Bulk or pseudo-bulk multi-omics across multiple samples/individuals. Requires sample-level covariation.
- **SCENIC+**: Single-cell multiome data (scRNA-seq + scATAC-seq from same cells). Infers cell-state-specific regulons.

### 4e. Multiome Integration (scATAC-seq + scRNA-seq)

When single-cell multiome data is available (joint scATAC-seq + scRNA-seq from the same cells), this is the gold standard for cell type-resolved multi-omics:

**Weighted Nearest Neighbor (WNN)** (Hao et al. 2021, Seurat v4):
- Learns cell-specific modality weights
- Cells where RNA is more informative get higher RNA weight (and vice versa)
- Produces a joint embedding that leverages both modalities

**Integration workflow**:
1. Process RNA modality: standard scRNA-seq pipeline (QC, normalize, HVGs, PCA)
2. Process ATAC modality: peak calling, TF-IDF normalization, LSI dimensionality reduction
3. Find multimodal neighbors via WNN
4. Joint clustering on WNN graph
5. Cell type annotation using RNA markers
6. Link peaks to genes within each cell type

**SCENIC+** (Gonzalez-Blas et al. 2023) can then infer cell-type-specific enhancer GRNs directly from the multiome data, identifying TF regulons that couple chromatin accessibility to gene expression.

**Caveats for multiome data**:
- Joint capture reduces data quality for both modalities compared to standalone assays
- ATAC-seq quality (fragments/cell) is typically lower in multiome than standalone ATAC
- Some cell types may be underrepresented due to differential survival during joint library prep
- Batch effects may differ between modalities within the same experiment

### 4f. Sequence-Based Regulatory Validation (Enformer)

**Enformer** (Avsec et al. 2021) can serve as an independent validation layer for identified regulatory elements:

1. **Variant effect prediction**: Score genetic variants in identified enhancers/promoters for predicted expression effects
2. **Enhancer-promoter interaction**: Enformer can predict enhancer-promoter interactions directly from DNA sequence — compare against your ChIP/ATAC-derived linkages
3. **Conservation of regulatory function**: Assess whether identified regulatory elements maintain predicted function across species

**When to use**: As a validation/prioritization layer, NOT as a primary discovery tool. Enformer predicts from sequence alone (no cell type specificity without additional cell-type-specific inputs). Use to prioritize enhancers or variants for experimental follow-up.

**Limitation**: Enformer was trained on bulk epigenomic data. Cell-type-specific predictions require additional frameworks (e.g., Enformer Celltyping, Murphy et al. 2024).

### 4g. Cell Type-Specific Integration (Following Mawla et al. 2023)

When cell type-resolved data is available:

1. **Differential accessibility**: Identify ATAC-seq peaks unique to each cell type
2. **Differential expression**: Identify genes unique to each cell type from RNA-seq
3. **Cross-validate**: Cell type-specific enhancers should be near cell type-specific genes
4. **Poised state identification**: Regions accessible in one cell type but not another, combined with H3K27me3 in the "off" cell type, suggest poised/repressed states (as found for alpha and delta cells relative to beta cell identity)

## Step 5: Validation and Cross-Referencing

### Against ENCODE cCRE Registry
Compare identified enhancers/promoters against ENCODE's candidate cis-regulatory elements:
```
# Download cCRE file for the relevant assembly
encode_search_files(
    search_term="cCRE",
    assembly="GRCh38",
    output_type="candidate Cis-Regulatory Elements"
)
```

Report:
- What fraction of your enhancers overlap ENCODE cCREs?
- What fraction of ENCODE cCREs are captured by your analysis?
- Novel regions not in ENCODE cCREs (potentially tissue-specific)

### Functional Enrichment of Identified Regions
Use GREAT (McLean et al. 2010) to assign biological meaning to enhancer/regulatory region sets:
- Upload enhancer BED file to GREAT (http://great.stanford.edu)
- Assess GO term enrichment, pathway enrichment, disease association
- Cell type-specific enhancers should enrich for tissue-relevant terms
- Whole-genome background is more appropriate than promoter-based background for distal elements

### Against Published Enhancer Databases
Cross-reference with:
- **VISTA Enhancer Browser**: In vivo validated enhancers (limited to ~3,000)
- **EnhancerAtlas 2.0**: Predicted enhancers across tissues
- **SEdb**: Super-enhancer database
- **GeneHancer**: Regulatory element-gene links

### Publication Linkage
```
encode_link_reference(
    experiment_accession="ENCSR...",
    reference_type="pmid",
    reference_id="37069576",
    description="Multi-omics integration using this experiment"
)
```

## Step 6: Log Provenance

Log all derived files:
```
encode_log_derived_file(
    file_path="/path/to/enhancer_catalog.bed",
    source_accessions=["ENCSR...", "ENCSR...", ...],
    description="Active enhancers in [tissue]: ATAC+H3K27ac+H3K4me1, TSS-subtracted",
    file_type="enhancer_catalog",
    tool_used="bedtools intersect + ENCODE Blacklist filter",
    parameters="H3K27ac AND H3K4me1 AND ATAC, NOT H3K4me3, NOT TSS±2kb"
)
```

```
encode_log_derived_file(
    file_path="/path/to/chromhmm_states.bed",
    source_accessions=["ENCSR...", "ENCSR...", ...],
    description="ChromHMM 18-state annotation for [tissue]",
    file_type="chromatin_states",
    tool_used="ChromHMM LearnModel + MakeSegmentation",
    parameters="18 states, 200bp bins, 5 marks"
)
```

## Pitfalls and Edge Cases

### Matched vs. Unmatched Biosamples
- **Ideal**: All assays from the SAME biosample/donor (matched multi-omics)
- **Common**: Each assay from DIFFERENT donors (unmatched)
- Unmatched data can still be integrated (Mawla et al. 2023 used separate ATAC-seq experiments per cell type), but adds noise and prevents individual-level correlation analyses
- Always report whether data layers are matched or unmatched

### Antibody and Protocol Variation
- H3K27ac antibodies from different vendors can show different peak profiles
- ATAC-seq protocols (standard vs. Omni-ATAC vs. FAST-ATAC) differ in signal-to-noise
- ChIP-seq depth requirements vary by mark: narrow marks need 20M reads, broad marks need 40M+
- Always check ENCODE audit details for antibody validation status

### Assembly Consistency
- **All data layers MUST use the same genome assembly** (GRCh38 for human, mm10 for mouse)
- Mixing assemblies introduces coordinate shifts that invalidate all intersection analyses
- Liftover is acceptable but introduces edge effects at assembly-discordant regions

### Incomplete Mark Panels
- ChromHMM with <4 marks produces unreliable states
- If H3K27ac is missing, enhancer calling is severely compromised (H3K4me1 alone is insufficient — many poised enhancers are H3K4me1+)
- If ATAC-seq is missing, "open chromatin" validation is not possible — rely on DNase-seq as substitute
- Missing H3K27me3 prevents identification of bivalent/poised states

### Cell Type Resolution
- Bulk data from mixed tissues conflates cell type-specific signals
- Cell type-specific enhancers in minority cell types may be invisible in bulk data
- Where possible, use cell type-sorted or single-cell data (as in Mawla et al. 2023)
- scATAC-seq + scRNA-seq multiome data is the gold standard for cell type-resolved multi-omics

### Signal Strength Interpretation
- A peak in ATAC-seq does NOT mean the region is an enhancer — it means chromatin is accessible (could be promoter, insulator, or structural element)
- H3K4me1 without H3K27ac marks poised, not active, enhancers
- H3K27me3 co-occurrence with H3K4me3 (bivalent) has biological meaning — do not treat as noise
- Low TF ChIP-seq signal may reflect transient binding rather than absence

### Sequence Model Limitations
- **Enformer** was trained on bulk data from a limited number of cell types — predictions may not generalize to rare or unstudied cell types
- Sequence-based predictions cannot capture epigenetic state or cell-type-specific chromatin context directly
- Variant effect predictions are most reliable for common regulatory motifs; rare or novel regulatory mechanisms may not be captured
- Always validate sequence-based predictions against experimental data (ChIP-seq, ATAC-seq, reporter assays)

### GRN Inference Caveats
- **Correlation ≠ causation**: GRaNIE and SCENIC+ identify statistical associations, not causal relationships
- GRN inference requires sufficient biological variation across samples — technical replicates provide no information
- GRaNIE requires bulk or pseudobulk data across individuals/conditions (minimum ~20 samples for robust networks)
- SCENIC+ requires multiome data (scATAC-seq + scRNA-seq from same cells)
- No complete ground truth exists for GRNs — use GRaNPA or TF perturbation data for validation
- Inferred networks are biased toward highly expressed TFs and accessible enhancers; low-abundance regulators may be missed

## Summary Statistics to Report

For the integrated regulatory landscape:
- Number of active enhancers identified (with mark combination used)
- Number of active promoters
- Number of poised enhancers (H3K4me1+ H3K27ac-)
- Number of repressed/bivalent regions
- ChromHMM state distribution (% genome per state)
- Enhancer-gene links established and method used
- TF binding enrichment at enhancers (top TFs)
- Overlap with ENCODE cCRE registry
- Data layers used and whether matched or unmatched
- If multiome: WNN integration metrics, cells per modality, cell type resolution
- If GRN: Number of TF-enhancer-gene links, key regulons identified, GRaNPA performance score
- If Enformer validation: Fraction of enhancers with predicted regulatory activity, variant effect scores for key loci

## Histone Mark Interpretation Reference

For detailed biological meaning of each histone mark, ChromHMM combinatorial states, functional categories (active promoters, active/poised enhancers, super-enhancers, silencers), contradictions, and cancer-specific states, consult the comprehensive reference at `skills/histone-aggregation/references/histone-marks-reference.md` (1,442 lines, 21 marks, 37 key papers).

## Walkthrough: Integrating Epigenomic, Transcriptomic, and 3D Genome Data for a Gene Locus

**Goal**: Combine ENCODE ChIP-seq, ATAC-seq, RNA-seq, and Hi-C data at a single gene locus to build a complete regulatory model.
**Context**: Multi-omics integration at a specific locus connects enhancer marks, accessibility, gene expression, and 3D contacts into a mechanistic regulatory model.

### Step 1: Gather all data types for the tissue

```
encode_get_facets(facet_field="assay_title", organ="heart", organism="Homo sapiens")
```

Expected output:
```json
{
  "facets": {
    "assay_title": {"Histone ChIP-seq": 45, "ATAC-seq": 18, "RNA-seq": 15, "Hi-C": 8, "WGBS": 6}
  }
}
```

### Step 2: Search for each data type

```
encode_search_experiments(assay_title="Histone ChIP-seq", organ="heart", target="H3K27ac", organism="Homo sapiens")
encode_search_experiments(assay_title="ATAC-seq", organ="heart", organism="Homo sapiens")
encode_search_experiments(assay_title="total RNA-seq", organ="heart", organism="Homo sapiens")
encode_search_experiments(assay_title="Hi-C", organ="heart", organism="Homo sapiens")
```

### Step 3: Download processed files

```
encode_download_files(accessions=["ENCFF100H3K", "ENCFF200ATK", "ENCFF300RNA", "ENCFF400HIC"], download_dir="/data/multiomics")
```

### Step 4: Integrate at a gene locus

Focus on MYH7 locus (chr14:23,380,000-23,500,000) — cardiac myosin gene:
1. H3K27ac peaks → identify active enhancers
2. ATAC-seq peaks → confirm chromatin accessibility at enhancers
3. RNA-seq TPM → confirm MYH7 is expressed
4. Hi-C loops → connect enhancers to MYH7 promoter

**Interpretation**: Enhancers with all 4 evidence layers (H3K27ac + ATAC + expression + 3D contact) are high-confidence regulatory elements for MYH7.

### Integration with downstream skills
- Histone data from → **histone-aggregation** provides enhancer peaks
- Accessibility from → **accessibility-aggregation** confirms open chromatin
- Hi-C from → **hic-aggregation** provides 3D connections
- Expression from → **gtex-expression** validates gene activity

## Code Examples

### 1. Survey available omics layers for a tissue
```
encode_get_facets(facet_field="assay_title", organ="heart", organism="Homo sapiens")
```

Expected output:
```json
{
  "facets": {"assay_title": {"Histone ChIP-seq": 45, "ATAC-seq": 18, "RNA-seq": 15, "Hi-C": 8}}
}
```

### 2. Compare experiments across omics
```
encode_compare_experiments(accession_1="ENCSR100CHI", accession_2="ENCSR200ATK")
```

Expected output:
```json
{
  "comparison": {
    "shared": {"organ": "heart", "organism": "Homo sapiens"},
    "differences": {"assay": ["Histone ChIP-seq", "ATAC-seq"]}
  }
}
```

### 3. Track multi-omics experiment collection
```
encode_summarize_collection()
```

Expected output:
```json
{
  "total_tracked": 4,
  "by_assay": {"Histone ChIP-seq": 1, "ATAC-seq": 1, "RNA-seq": 1, "Hi-C": 1}
}
```

## Presenting Results

When reporting multi-omics integration results:

- **Integration summary**: Present a table listing each data layer used (e.g., histone ChIP-seq, ATAC-seq, RNA-seq, WGBS, Hi-C), with ENCODE experiment accession(s), number of features contributed, and assembly verified as matching
- **Concordance metrics**: Report pairwise concordance between data layers (e.g., % of active enhancers with H3K27ac AND open chromatin, % of predicted target genes with correlated expression)
- **Key fields to include**: Total integrated features, number of multi-evidence regulatory elements, ChromHMM state assignments if used, and GRN links (TF-enhancer-gene triplets) if applicable
- **Always report**: Integration method and parameters, genome assembly, whether data layers were matched (same biosample) or unmatched (cross-biosample), and all ENCODE accessions used
- **Context to provide**: Note any missing data layers and how they limit interpretation (e.g., no Hi-C means enhancer-gene links are distance-based only), and whether batch effects across labs were assessed
- **Next steps**: Suggest `visualization-workflow` for publication-quality multi-track figures, or `epigenome-profiling` for broader epigenomic characterization of the tissue

## Related Skills

- `histone-aggregation` — Aggregate histone ChIP-seq across multiple experiments (input layer)
- `accessibility-aggregation` — Aggregate ATAC-seq/DNase-seq across experiments (input layer)
- `regulatory-elements` — Focused enhancer/promoter analysis
- `epigenome-profiling` — Broader epigenomic characterization
- `scrna-meta-analysis` — Single-cell RNA-seq integration (expression layer)
- `hic-aggregation` — Chromatin contact data for enhancer-gene linkage
- `methylation-aggregation` — DNA methylation data (additional regulatory layer)
- `publication-trust` — Verify literature claims backing analytical decisions

## For the request: "$ARGUMENTS"
