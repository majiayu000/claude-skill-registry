---
name: epigenome-profiling
description: Build comprehensive epigenomic profiles for tissues or cell types using ENCODE data. Use when the user wants to characterize chromatin states, assemble histone modification panels, create epigenomic landscapes, run ChromHMM segmentation, identify super-enhancers or bivalent domains, profile regulatory elements across a biosample, or understand epigenetic regulation in a specific biological context. Covers histone marks, chromatin accessibility, TF binding, transcription, DNA methylation, and 3D genome structure.
---

# Build Comprehensive Epigenomic Profiles with ENCODE

## When to Use

- User wants to build a comprehensive epigenomic profile for a tissue or cell type
- User asks about "chromatin states", "epigenome", or "histone landscape" for a biosample
- User wants to identify super-enhancers, bivalent domains, or regulatory elements
- User needs to assemble a panel of histone marks, accessibility, and TF binding data
- User wants to run ChromHMM segmentation on ENCODE data
- User asks "what epigenomic data does ENCODE have for [tissue]?"

Assemble a complete epigenomic profile for a tissue or cell type by systematically gathering histone modifications, chromatin accessibility, transcription factor binding, transcription, DNA methylation, and 3D chromatin structure data from ENCODE. Interpret the resulting profile using ChromHMM chromatin state segmentation.

## Literature Foundation

| Reference | Year | Journal | DOI | Citations | Contribution |
|-----------|------|---------|-----|-----------|-------------|
| Roadmap Epigenomics Consortium (Kundaje et al.) | 2015 | *Nature* | [10.1038/nature14248](https://doi.org/10.1038/nature14248) | ~5,810 | 111 reference epigenomes; 5-mark core model; 15/18/25-state ChromHMM |
| ENCODE Phase 3 (ENCODE Project Consortium) | 2020 | *Nature* | [10.1038/s41586-020-2493-4](https://doi.org/10.1038/s41586-020-2493-4) | ~1,656 | Registry of candidate cis-regulatory elements (cCREs) across 1,310+ experiments |
| Ernst & Kellis | 2012 | *Nat Methods* | [10.1038/nmeth.1906](https://doi.org/10.1038/nmeth.1906) | ~2,294 | ChromHMM: multivariate HMM for chromatin state discovery and characterization |
| Barski et al. | 2007 | *Cell* | [10.1016/j.cell.2007.05.009](https://doi.org/10.1016/j.cell.2007.05.009) | ~4,800 | First genome-wide ChIP-Seq of 20 histone methylations in human CD4+ T cells |
| Mikkelsen et al. | 2007 | *Nature* | [10.1038/nature06008](https://doi.org/10.1038/nature06008) | ~4,289 | Chromatin state maps in pluripotent and lineage-committed cells; H3K4me3/H3K27me3 discriminate expressed, poised, and repressed genes |
| Bernstein et al. | 2006 | *Cell* | [10.1016/j.cell.2006.02.041](https://doi.org/10.1016/j.cell.2006.02.041) | ~3,500 | Discovery of bivalent chromatin domains (H3K4me3+H3K27me3) in embryonic stem cells |
| Creyghton et al. | 2010 | *PNAS* | [10.1073/pnas.1016071107](https://doi.org/10.1073/pnas.1016071107) | ~2,800 | H3K27ac distinguishes active enhancers from poised (H3K4me1-only) enhancers |
| Whyte et al. | 2013 | *Cell* | [10.1016/j.cell.2013.03.035](https://doi.org/10.1016/j.cell.2013.03.035) | ~2,500 | Master transcription factors and super-enhancer identification via ROSE algorithm |
| Buenrostro et al. | 2013 | *Nat Methods* | [10.1038/nmeth.2688](https://doi.org/10.1038/nmeth.2688) | ~5,000 | ATAC-seq: transposase-based chromatin accessibility profiling |
| Heintzman et al. | 2007 | *Nat Genet* | [10.1038/ng1966](https://doi.org/10.1038/ng1966) | ~2,300 | H3K4me1 marks enhancers, H3K4me3 marks promoters — foundational chromatin signature for regulatory element classification |
| Rada-Iglesias et al. | 2011 | *Nature* | [10.1038/nature09692](https://doi.org/10.1038/nature09692) | ~1,200 | Discovered "poised enhancers" (H3K4me1+H3K27me3, no H3K27ac) that activate during differentiation |
| ENCODE Blacklist (Amemiya et al.) | 2019 | *Sci Rep* | [10.1038/s41598-019-45839-z](https://doi.org/10.1038/s41598-019-45839-z) | ~1,372 | Comprehensive set of problematic genomic regions to exclude from all analyses |

---

## Step 1: Choose the Target Biosample

Clarify the target biosample with the user. Check data availability across assay types:

```
encode_get_facets(organ="pancreas", biosample_type="tissue")
```

### ENCODE Cell Line Tiers

| Tier | Cell Lines | Data Depth | Notes |
|------|-----------|------------|-------|
| **Tier 1** (most data) | K562, GM12878, H1-hESC | Deep profiling across all assays | Preferred for methods development and benchmarking |
| **Tier 2** (good coverage) | HeLa-S3, HepG2, HUVEC, A549, MCF-7 | Most core marks and accessibility | Suitable for tissue-specific profiling |
| **Tier 3+** (variable) | 100+ additional cell lines and primary tissues | Variable coverage | Check availability per assay before committing |

For primary tissues, verify what biosamples are available:

```
encode_search_experiments(organ="pancreas", biosample_type="tissue", limit=50)
```

**Biosample hierarchy** (from most to least standardized): tissue > primary cell > cell line > in vitro differentiated cells > organoid. Cell lines offer the deepest profiling. Primary tissues offer biological relevance but greater heterogeneity.

---

## Step 2: Assemble the Histone Modification Panel

Search for each histone mark in the target biosample. Organize the panel into three tiers of increasing depth.

### Tier 1: Core 5-Mark Panel (ChromHMM Minimum)

This is the minimum set required for chromatin state segmentation. All 111 Roadmap Epigenomics reference epigenomes were profiled for these five marks (Kundaje et al. 2015). Ernst & Kellis (2012) demonstrated that these five marks suffice for the 15-state ChromHMM model that captures all major functional categories.

| Mark | What It Marks | Genomic Location | Writers | Readers | Key Reference |
|------|--------------|------------------|---------|---------|---------------|
| **H3K4me3** | Active and poised promoters | Sharp peaks at TSSs | SET1A/B (COMPASS), MLL1/2 | TAF3, ING proteins, CHD1 | Barski et al. 2007 |
| **H3K4me1** | Enhancers (primed and active) | Distal regulatory elements | MLL3 (KMT2C), MLL4 (KMT2D) | CHD1, BPTF | Heintzman et al. 2007 |
| **H3K27me3** | Polycomb-mediated repression | Broad domains over silent genes | EZH2 (PRC2), EZH1 | EED, CBX proteins (PRC1) | Bernstein et al. 2006 |
| **H3K36me3** | Actively transcribed gene bodies | Gene bodies, 5'-to-3' gradient | SETD2 (sole trimethylase) | DNMT3B, MSH6 | Mikkelsen et al. 2007 |
| **H3K9me3** | Constitutive heterochromatin | Repeats, TEs, ERVs, pericentromeric | SUV39H1/2, SETDB1 | HP1alpha/beta/gamma | Barski et al. 2007 |

**Note on H3K27ac**: While not in the Roadmap 5-mark core, H3K27ac is essential for distinguishing active from poised elements (Creyghton et al. 2010). It is included in the 18-state extended ChromHMM model. Always include H3K27ac if available.

Search for each:

```
encode_search_experiments(
    assay_title="Histone ChIP-seq",
    target="H3K4me3",
    biosample_term_name="...",
    biosample_type="tissue"
)
```

### Tier 2: Extended Panel

These marks provide finer-grained state resolution. The Ernst et al. (2011) 15-state model across 9 cell types used these marks together with the core 5 to define insulator, active promoter, and transcription states more precisely.

| Mark | What It Marks | Genomic Location | Key Reference |
|------|--------------|------------------|---------------|
| **H3K9ac** | Active promoters and regulatory regions | TSSs, co-occurs with H3K4me3 | Wang et al. 2008 |
| **H3K79me2** | Transcription elongation | Gene bodies (DOT1L-mediated) | Barski et al. 2007 |
| **H2A.Z (H2AFZ)** | Active regulatory elements | TSSs, enhancers, insulators | Barski et al. 2007 |
| **H4K20me1** | Transcription and cell cycle | Gene bodies | Barski et al. 2007 |
| **H3K27ac** | Active enhancers and promoters | Active regulatory elements (mutually exclusive with H3K27me3) | Creyghton et al. 2010 |

### Tier 3: Advanced Panel

These acetylation marks provide additional granularity for specialized analyses. They are rarely profiled outside Tier 1 cell lines but can distinguish subtypes of active chromatin.

| Mark | What It Marks | Genomic Location | Key Reference |
|------|--------------|------------------|---------------|
| **H3K14ac** | Active promoters, DNA damage response | Active TSSs, DNA double-strand break sites | Wang et al. 2008 |
| **H3K18ac** | Active transcription | Active promoters and enhancers | Wang et al. 2008 |
| **H3K23ac** | Active transcription | Active promoters | Wang et al. 2008 |
| **H4K5ac** | Active chromatin, super-enhancers | Promoters, enhancers | Das et al. 2023 |
| **H4K8ac** | Active chromatin, super-enhancers | Promoters, enhancers | Das et al. 2023 |
| **H4K16ac** | Euchromatin maintenance | Globally across active euchromatin | Shogren-Knaak et al. 2006 |

**For detailed mark biology, writers, erasers, readers, and contradictions, see the histone marks reference in the `histone-aggregation` skill's `references/histone-marks-reference.md` (1,442 lines, 74 references).**

---

## Step 3: Add Chromatin Accessibility

Open chromatin profiling is essential for identifying active regulatory elements. ATAC-seq is the current standard; DNase-seq is the legacy method with deeper ENCODE archives.

```
# Prefer ATAC-seq (Buenrostro et al. 2013) — lower input, faster protocol
encode_search_experiments(assay_title="ATAC-seq", biosample_term_name="...")

# Fall back to DNase-seq if ATAC-seq is unavailable
encode_search_experiments(assay_title="DNase-seq", biosample_term_name="...")
```

ATAC-seq and DNase-seq identify largely overlapping accessible regions (Pearson r > 0.8 at promoters), but ATAC-seq captures some distal elements missed by DNase-seq and vice versa (Corces et al. 2017). Do not mix the two assays in a single analysis without careful normalization.

---

## Step 4: Add Transcription Factor Binding

Two TFs provide critical structural and functional information for epigenomic profiling:

| TF | Role | Why Essential | ENCODE Tool Call |
|----|------|---------------|------------------|
| **CTCF** | Insulator, TAD boundary factor | Defines chromatin domains; required for ChromHMM insulator state in expanded models | `encode_search_experiments(assay_title="TF ChIP-seq", target="CTCF", biosample_term_name="...")` |
| **EP300 (p300)** | Enhancer co-activator | p300 binding marks active enhancers independently of histone marks (Visel et al. 2009) | `encode_search_experiments(assay_title="TF ChIP-seq", target="EP300", biosample_term_name="...")` |

Use `encode_get_facets` to discover which TFs are available for the target biosample:

```
encode_get_facets(assay_title="TF ChIP-seq", organ="pancreas")
```

---

## Step 5: Add Transcription Data

Gene expression data links chromatin states to functional output.

```
# Poly-A plus RNA-seq (mRNA)
encode_search_experiments(assay_title="polyA plus RNA-seq", biosample_term_name="...")

# Total RNA-seq (includes non-coding RNAs, intronic transcripts)
encode_search_experiments(assay_title="total RNA-seq", biosample_term_name="...")
```

Both are valuable: poly-A RNA-seq captures mRNA levels for gene-level correlation with chromatin states. Total RNA-seq captures eRNAs (enhancer RNAs), lncRNAs, and other non-coding transcripts that inform regulatory element activity.

---

## Step 6: Add DNA Methylation

Whole-genome bisulfite sequencing (WGBS) provides single-CpG resolution methylation across the entire genome. DNA methylation is anticorrelated with H3K4me3 at CpG island promoters and anticorrelated with H3K27me3 at bivalent domains (Bernstein et al. 2006).

```
encode_search_experiments(assay_title="WGBS", biosample_term_name="...")
```

If WGBS is unavailable, check for RRBS (reduced representation bisulfite sequencing). Note that RRBS covers only CpG-dense regions and is incompatible with genome-wide methylation analyses such as partially methylated domain (PMD) or large hypo-methylated region (HMR) identification.

---

## Step 7: Add 3D Chromatin Structure

3D genome organization data connects regulatory elements to their target genes through chromatin loops and topologically associating domains (TADs).

```
# Hi-C: genome-wide chromatin conformation
encode_search_experiments(assay_title="Hi-C", biosample_term_name="...")

# ChIA-PET: protein-centric interaction mapping
encode_search_experiments(assay_title="ChIA-PET", biosample_term_name="...")
```

Hi-C provides unbiased genome-wide contact maps. ChIA-PET enriches for interactions mediated by specific proteins (CTCF, RNAPII). Both are useful but not essential for a core epigenomic profile.

---

## Step 8: ChromHMM Chromatin State Segmentation

ChromHMM (Ernst & Kellis 2012) is the standard tool for learning chromatin states from combinatorial histone modification patterns. It uses a multivariate Hidden Markov Model to segment the genome into functionally distinct states.

### The 5-Mark Core Model (15 States)

The Roadmap Epigenomics 15-state model (Kundaje et al. 2015) uses **H3K4me3, H3K4me1, H3K36me3, H3K27me3, H3K9me3**:

| State | Name | H3K4me3 | H3K4me1 | H3K36me3 | H3K27me3 | H3K9me3 | Interpretation |
|-------|------|---------|---------|----------|----------|---------|----------------|
| 1 | TssA | HIGH | LOW | - | - | - | Active TSS |
| 2 | TssAFlnk | MED | MED | - | - | - | Flanking Active TSS |
| 3 | TxFlnk | LOW | MED | LOW | - | - | Transcription at gene 5' and 3' |
| 4 | Tx | - | - | HIGH | - | - | Strong Transcription |
| 5 | TxWk | - | - | MED | - | - | Weak Transcription |
| 6 | EnhG | - | MED | MED | - | - | Genic Enhancers |
| 7 | Enh | - | HIGH | - | - | - | Enhancers |
| 8 | ZNF/Rpts | - | - | LOW | - | HIGH | ZNF Genes & Repeats |
| 9 | Het | - | - | - | - | HIGH | Heterochromatin |
| 10 | TssBiv | HIGH | MED | - | HIGH | - | Bivalent/Poised TSS |
| 11 | BivFlnk | MED | MED | - | HIGH | - | Flanking Bivalent TSS/Enhancer |
| 12 | EnhBiv | - | HIGH | - | HIGH | - | Bivalent Enhancer |
| 13 | ReprPC | - | - | - | HIGH | - | Repressed Polycomb |
| 14 | ReprPCWk | - | - | - | MED | - | Weak Repressed Polycomb |
| 15 | Quies | - | - | - | - | - | Quiescent/Low signal |

**Source:** Kundaje et al. (2015) Table derived from the 15-state core model applied to 111 reference epigenomes.

### The 18-State Extended Model

Adding H3K27ac as a 6th mark (available for a subset of Roadmap epigenomes) enables the 18-state model, which splits:
- Active TSS by H3K27ac level
- Enhancers into active (with H3K27ac) versus poised (without)
- Genic enhancers with finer precision

### Running ChromHMM

ChromHMM requires binarized ChIP-seq signal (BED or BAM) for each mark. The standard pipeline:
1. Binarize signal into 200bp bins using `BinarizeBed` or `BinarizeBam`
2. Learn model with `LearnModel` (specify number of states; 15 is standard)
3. Assign states genome-wide with the learned emission/transition parameters
4. Compare across samples using `CompareModels` or `Reorder`

For full detail on ChromHMM state interpretation, see the histone marks reference in the `histone-aggregation` skill's `references/histone-marks-reference.md`, Part 2: Combinatorial Patterns.

---

## Functional Mark Combinations

Specific histone mark combinations carry distinct biological meanings. These are not arbitrary -- they reflect biochemically antagonistic or cooperative modifications at the same genomic locus.

### Active Elements

| Combination | Biological State | Location | Key Reference |
|-------------|-----------------|----------|---------------|
| H3K4me3 + H3K27ac | **Active promoter** | TSS | Creyghton et al. 2010 |
| H3K4me1 + H3K27ac | **Active enhancer** | Distal regulatory elements | Creyghton et al. 2010; Rada-Iglesias et al. 2011 |
| H3K36me3 + H3K79me2 | **Actively transcribed gene body** | Gene bodies | Barski et al. 2007 |

### Poised/Primed Elements

| Combination | Biological State | Location | Key Reference |
|-------------|-----------------|----------|---------------|
| H3K4me3 + H3K27me3 | **Bivalent promoter** | Developmental gene TSSs | Bernstein et al. 2006 |
| H3K4me1 + H3K27me3 | **Poised enhancer** | Developmental enhancers | Rada-Iglesias et al. 2011 |
| H3K4me1 alone (no H3K27ac) | **Primed enhancer** | Distal elements, latent regulatory | Creyghton et al. 2010 |

### Repressed Elements

| Combination | Biological State | Location | Key Reference |
|-------------|-----------------|----------|---------------|
| H3K27me3 alone | **Polycomb-repressed** | Facultative heterochromatin | Boyer et al. 2006 |
| H3K9me3 alone | **Constitutive heterochromatin** | Repeats, pericentromeric, TEs | Rea et al. 2000 |
| H3K9me3 + H3K36me3 | **ZNF/KRAB-ZFP gene** | KRAB zinc finger gene clusters | Not repressed -- unique state |

### Conflicting Signals

| Combination | Interpretation | Action |
|-------------|---------------|--------|
| H3K36me3 + H3K27me3 | Domain boundary or mixed cell populations | Investigate at single-cell level; do not interpret as a coherent state |
| H3K4me3 + H3K9me3 | Likely mixed signal from heterogeneous tissue | Filter for single-cell or sorted-population data |

---

## Bivalent Chromatin Domains

Bivalent domains carry both H3K4me3 (active mark) and H3K27me3 (repressive mark) at the same promoter. They were discovered in embryonic stem cells (Bernstein et al. 2006) and are enriched at developmental transcription factor genes.

### Key Properties

- **Prevalence**: ~2,000-3,000 bivalent promoters in human ESCs, decreasing upon differentiation (Mikkelsen et al. 2007).
- **Resolution**: During lineage commitment, bivalent domains resolve to H3K4me3-only (gene activated) or H3K27me3-only (gene stably repressed).
- **Same-nucleosome co-occurrence**: Sequential ChIP (re-ChIP) confirmed both marks on the same nucleosome or allele (Bernstein et al. 2006).
- **Not restricted to ESCs**: Found in adult stem cells and progenitor cells, though enriched in pluripotent states (Harikumar & Meshorer 2015).

### The Poising vs. Protection Debate

The original model proposed that bivalency "poises" genes for rapid activation upon developmental cues (Bernstein et al. 2006). An alternative model argues that H3K4me3 at bivalent promoters primarily protects CpG islands from de novo DNA methylation, preventing irreversible silencing (Kumar et al. 2021, *Genome Res*).

**Current consensus** (Macrae et al. 2022, *Nat Rev Mol Cell Biol*, DOI:10.1038/s41580-022-00544-w): Both models are compatible. Bivalency maintains epigenetic plasticity by preventing permanent silencing, which as a consequence preserves potential for future activation. In cancer, loss of bivalency at tumor suppressor promoters correlates with aberrant DNA hypermethylation and irreversible gene silencing (Ohm et al. 2007).

### Detecting Bivalent Domains in ENCODE Data

1. Call H3K4me3 peaks (narrowPeak, IDR thresholded)
2. Call H3K27me3 peaks (broadPeak preferred for this broad mark)
3. Intersect: regions carrying both marks within 2kb of a TSS are candidate bivalent promoters
4. Validate using ChromHMM state 10 (TssBiv) from the 15-state model

**Caveat**: In bulk tissue data, apparent bivalency may reflect mixed cell populations where one cell type expresses H3K4me3 and another H3K27me3 at the same locus. Single-cell or sorted-population ChIP-seq is required to confirm true bivalency.

---

## Super-Enhancer Identification

Super-enhancers are large clusters of enhancers with disproportionately high H3K27ac and Mediator (MED1) signal. They drive expression of cell-identity genes and are preferentially sensitive to perturbation (Whyte et al. 2013).

### ROSE Algorithm

The Rank Ordering of Super-Enhancers (ROSE) algorithm (Whyte et al. 2013; Loven et al. 2013, *Cell*, DOI:10.1016/j.cell.2013.03.036, ~2,700 cit):

1. Call H3K27ac peaks (or MED1/BRD4 peaks)
2. Stitch peaks within 12.5kb of each other (excluding +/- 2kb from TSSs to avoid promoter signal)
3. Rank stitched enhancers by total H3K27ac signal
4. Apply geometric inflection point to separate typical enhancers from super-enhancers

### Using ENCODE Data for Super-Enhancer Calls

```
encode_search_experiments(
    assay_title="Histone ChIP-seq",
    target="H3K27ac",
    biosample_term_name="...",
    biosample_type="..."
)
```

Download fold-change-over-control bigWig and IDR thresholded peaks for input to ROSE. Cancer cells acquire de novo super-enhancers at oncogenes (Hnisz et al. 2013, *Cell*, DOI:10.1016/j.cell.2013.09.053), making super-enhancer profiling valuable for disease research.

**Caveat**: The super-enhancer concept is debated. Pott & Lieb (2015, *Nat Genet* 47:8-12) argued that individual constituent enhancers within super-enhancers can function independently, and the term may imply a mechanistic distinction that does not exist.

---

## Step 9: Assess Profile Completeness

Present a coverage matrix to the user showing what data layers are available:

```
| Data Layer           | Assay        | Available | Accession   | Audit Status |
|----------------------|-------------|-----------|-------------|--------------|
| H3K4me3              | Histone ChIP | Yes       | ENCSR...    | PASS         |
| H3K4me1              | Histone ChIP | Yes       | ENCSR...    | PASS         |
| H3K27me3             | Histone ChIP | Yes       | ENCSR...    | WARNING      |
| H3K36me3             | Histone ChIP | Yes       | ENCSR...    | PASS         |
| H3K9me3              | Histone ChIP | No        | -           | -            |
| H3K27ac              | Histone ChIP | Yes       | ENCSR...    | PASS         |
| Accessibility        | ATAC-seq     | Yes       | ENCSR...    | PASS         |
| CTCF                 | TF ChIP-seq  | Yes       | ENCSR...    | PASS         |
| p300                 | TF ChIP-seq  | No        | -           | -            |
| mRNA expression      | RNA-seq      | Yes       | ENCSR...    | PASS         |
| Total RNA            | total RNA-seq| No        | -           | -            |
| DNA methylation      | WGBS         | No        | -           | -            |
| 3D structure         | Hi-C         | No        | -           | -            |
```

### Minimum viable profile
- 5 core histone marks (H3K4me3, H3K4me1, H3K27me3, H3K36me3, H3K9me3): enables 15-state ChromHMM
- + H3K27ac: enables active vs. poised distinction (18-state model)
- + Accessibility (ATAC-seq or DNase-seq): validates regulatory element calls
- + RNA-seq: links chromatin states to gene expression

### Track all found experiments

```
For each available experiment:
    encode_track_experiment(accession="ENCSR...")
```

Then summarize the collection:

```
encode_summarize_collection()
```

---

## Step 10: Download and Organize Profile Data

Use `encode_batch_download` with dry_run=True first to preview:

```
# Histone mark signal tracks
encode_batch_download(
    assay_title="Histone ChIP-seq",
    biosample_term_name="...",
    file_format="bigWig",
    output_type="fold change over control",
    assembly="GRCh38",
    download_dir="/path/to/epigenome_profile/signal",
    preferred_default=True,
    organize_by="experiment",
    dry_run=True
)

# Histone mark peak calls
encode_batch_download(
    assay_title="Histone ChIP-seq",
    biosample_term_name="...",
    file_format="bed",
    output_type="IDR thresholded peaks",
    assembly="GRCh38",
    download_dir="/path/to/epigenome_profile/peaks",
    preferred_default=True,
    organize_by="experiment",
    dry_run=True
)
```

### File Selection Priority

Follow this hierarchy when selecting files for analysis:
1. **preferred_default=True** files (ENCODE-recommended)
2. **IDR thresholded peaks** for narrow marks (H3K4me3, H3K4me1, H3K27ac, H3K9ac)
3. **Replicated peaks** for broad marks (H3K27me3, H3K9me3, H3K36me3)
4. **Fold change over control** bigWig for signal visualization
5. Assembly: **GRCh38** for human, **mm10** for mouse. Never mix assemblies in a single profile.

**Always filter with the ENCODE blacklist** (Amemiya et al. 2019) before any downstream analysis. Download from: `https://github.com/Boyle-Lab/Blacklist/blob/master/lists/hg38-blacklist.v2.bed.gz`

---

## Pitfalls and Caveats

### 1. Batch Effects Across Labs and Dates

Histone ChIP-seq experiments from different ENCODE labs can show substantial batch effects in signal intensity, peak width, and background levels. When assembling a profile from multiple labs, normalize signal tracks independently and compare peak calls rather than raw signal.

### 2. Antibody Lot Variation

Different antibody lots for the same histone mark target can have different specificities and affinities. ENCODE documents antibody lot information in experiment metadata. Prefer experiments using validated antibody lots. Be especially cautious with H3K9me3 and H3K27me3 antibodies, which can cross-react.

### 3. Cell Type Heterogeneity in Tissue Samples

Bulk tissue profiling averages signal across all cell types present. A chromatin mark detected in bulk tissue may be present in only a minor cell population. Apparent bivalent domains (H3K4me3+H3K27me3) in tissue may reflect distinct cell populations rather than true same-cell bivalency. Consider sorted-population or single-cell data (scATAC-seq, CUT&Tag) when available.

### 4. ChromHMM State Interpretation

ChromHMM states are probabilistic assignments, not deterministic annotations. The same genomic region may have different posterior probabilities for multiple states. A "Quiescent" call often means "low signal for all marks" -- this could be true quiescence or simply poor data quality in that region. Always cross-reference ChromHMM calls with individual mark tracks.

### 5. Broad Marks Require broadPeak Calls

H3K27me3, H3K9me3, and H3K36me3 form broad domains spanning tens to hundreds of kilobases. Use broadPeak (not narrowPeak) calls for these marks. NarrowPeak calls fragment broad domains into many small peaks and lose domain-level information critical for Polycomb and heterochromatin annotation.

### 6. H3K27ac vs. H3K27me3 Mutual Exclusivity

H3K27ac and H3K27me3 modify the same lysine residue and are biochemically mutually exclusive on the same histone tail. If both appear enriched at the same locus in bulk data, this reflects mixed cell populations. Do not interpret co-occurrence as a coherent chromatin state.

### 7. CUT&RUN and CUT&Tag Data

ENCODE increasingly includes CUT&RUN and CUT&Tag data alongside traditional ChIP-seq. These assays have lower background but different peak characteristics (sharper, lower read depth). Do not directly merge CUT&RUN peaks with ChIP-seq peaks without accounting for assay-specific biases. CUT&RUN data may also carry suspect regions not captured by the standard ENCODE blacklist (Nordin et al. 2023).

---

## Walkthrough: Building a Complete Epigenomic Profile for Pancreatic Islets

**Goal**: Assemble a comprehensive multi-mark epigenomic profile for a single tissue, combining histone modifications, chromatin accessibility, DNA methylation, and 3D genome data from ENCODE.
**Context**: A complete epigenomic profile requires multiple complementary assays. This walkthrough shows how to systematically collect and integrate them.

### Step 1: Survey available assay types for the tissue

```
encode_get_facets(facet_field="assay_title", organ="pancreas", organism="Homo sapiens")
```

Expected output:
```json
{
  "facets": {
    "assay_title": {"Histone ChIP-seq": 25, "ATAC-seq": 6, "RNA-seq": 12, "WGBS": 4, "Hi-C": 2, "TF ChIP-seq": 8}
  }
}
```

### Step 2: Collect the core marks

For a complete profile, gather:
```
encode_search_experiments(assay_title="Histone ChIP-seq", organ="pancreas", target="H3K27ac", organism="Homo sapiens")
encode_search_experiments(assay_title="Histone ChIP-seq", organ="pancreas", target="H3K4me3", organism="Homo sapiens")
encode_search_experiments(assay_title="Histone ChIP-seq", organ="pancreas", target="H3K27me3", organism="Homo sapiens")
encode_search_experiments(assay_title="ATAC-seq", organ="pancreas", organism="Homo sapiens")
```

### Step 3: Track all profiling experiments

```
encode_track_experiment(accession="ENCSR100PAN", notes="Pancreas H3K27ac for epigenome profiling")
```

Expected output:
```json
{"status": "tracked", "accession": "ENCSR100PAN", "notes": "Pancreas H3K27ac for epigenome profiling"}
```

### Step 4: Generate collection summary

```
encode_summarize_collection()
```

Expected output:
```json
{
  "total_tracked": 6,
  "by_assay": {"Histone ChIP-seq": 3, "ATAC-seq": 1, "WGBS": 1, "Hi-C": 1},
  "by_target": {"H3K27ac": 1, "H3K4me3": 1, "H3K27me3": 1}
}
```

### Integration with downstream skills
- Individual marks feed into **histone-aggregation** for cross-sample merge
- Chromatin accessibility feeds into **accessibility-aggregation**
- Combined profile feeds into **regulatory-elements** for chromatin state segmentation
- Complete profile enables **integrative-analysis** for multi-mark analysis

## Code Examples

### 1. Survey available marks for a tissue
```
encode_get_facets(facet_field="target.label", organ="pancreas", assay_title="Histone ChIP-seq", organism="Homo sapiens")
```

Expected output:
```json
{
  "facets": {"target.label": {"H3K27ac": 5, "H3K4me3": 4, "H3K27me3": 3, "H3K4me1": 3, "H3K36me3": 2}}
}
```

### 2. Get experiment details for profiling
```
encode_get_experiment(accession="ENCSR100PAN")
```

Expected output:
```json
{
  "accession": "ENCSR100PAN",
  "assay_title": "Histone ChIP-seq",
  "target": "H3K27ac",
  "biosample_summary": "pancreas",
  "replicates": 2
}
```

### 3. Summarize profiling collection
```
encode_summarize_collection()
```

Expected output:
```json
{
  "total_tracked": 6,
  "by_assay": {"Histone ChIP-seq": 3, "ATAC-seq": 1, "WGBS": 1, "Hi-C": 1}
}
```

## Integration

| This skill produces... | Feed into... | Purpose |
|---|---|---|
| Multi-mark peak sets | **histone-aggregation** | Aggregate individual marks across experiments |
| Complete chromatin profiles | **regulatory-elements** | ChromHMM/chromatin state segmentation |
| Epigenomic landscape | **integrative-analysis** | Multi-mark integrative analysis |
| Tissue-specific marks | **compare-biosamples** | Compare profiles between tissues |
| Profiling experiment collection | **visualization-workflow** | Multi-track genome browser sessions |
| Active enhancer maps | **peak-annotation** | Assign enhancers to target genes |
| Methylation + histone data | **methylation-aggregation** | Correlate methylation with histone marks |

## Related Skills

| Skill | When to Use |
|-------|------------|
| `histone-aggregation` | Merge peaks for a single histone mark across multiple experiments/donors into a union peak set |
| `regulatory-elements` | Identify and classify cis-regulatory elements (promoters, enhancers, insulators) using ENCODE cCRE catalog |
| `quality-assessment` | Evaluate ChIP-seq quality metrics (FRiP, NSC, RSC, NRF) and ENCODE audit flags before including experiments in the profile |
| `compare-biosamples` | Compare epigenomic profiles between two tissues or cell types to identify differential chromatin states |
| `accessibility-aggregation` | Merge ATAC-seq and DNase-seq peaks across experiments for comprehensive open chromatin maps |
| `methylation-aggregation` | Aggregate WGBS data across donors for per-CpG methylation maps and HMR/PMD identification |
| `single-cell-encode` | Single-cell epigenomic data resolves cell-type heterogeneity in bulk profiles |
| `multi-omics-integration` | Combine multiple data layers into a comprehensive regulatory landscape |
| `disease-research` | Epigenomic profiles are the foundation for disease regulatory models |
| `variant-annotation` | Variant annotation relies on the epigenomic profile for functional context |
| `hic-aggregation` | Hi-C data complements the 3D genome structure dimension of the profile |
| `data-provenance` | Document all profile assembly parameters, tool versions, and mark selections |
| `pipeline-guide` | Guidance for ChromHMM setup and other profile assembly pipelines |
| `ucsc-browser` | Retrieve ENCODE tracks and cCRE data from UCSC for profile visualization |
| `ensembl-annotation` | Ensembl Regulatory Build provides independent regulatory annotations to compare with ENCODE profiles |
| `visualization-workflow` | Visualize epigenomic profiles with genome browser tracks, heatmaps, and signal plots |
| `pipeline-chipseq` | Process raw ChIP-seq data through the full ENCODE-aligned pipeline |
| `publication-trust` | Verify literature claims backing analytical decisions |

---

## Presenting Results

- Present epigenomic profiles as a mark x tissue matrix showing signal presence/absence. Summarize chromatin states using the 15-state ChromHMM model. Suggest: "Would you like to compare with another tissue?"

## For the request: "$ARGUMENTS"
