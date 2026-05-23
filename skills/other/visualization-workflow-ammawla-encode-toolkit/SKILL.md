---
name: visualization-workflow
description: "Comprehensive guide for visualizing ENCODE data including deeptools heatmaps, IGV screenshots, UCSC track hubs, and publication-quality plots. Use when users need to create visualizations of ChIP-seq signal, peak landscapes, genome browser views, or any visual representation of ENCODE data. Trigger on: heatmap, visualization, genome browser, track hub, IGV, deeptools, signal plot, peak visualization, profile plot, publication figure, bigWig visualization."
---

# Visualization Workflow for ENCODE Data

## When to Use

- User wants to create genome browser visualizations, heatmaps, or signal track plots from ENCODE data
- User asks about "visualization", "genome browser", "deeptools", "heatmap", "signal track", or "IGV"
- User needs to generate publication-ready figures from ChIP-seq, ATAC-seq, or other genomic data
- User wants to compare signal profiles across conditions, tissues, or histone marks
- Example queries: "visualize H3K27ac signal at promoters", "create a heatmap of ChIP-seq signal", "set up a UCSC track hub for my data"

Help the user create informative, publication-quality visualizations of ENCODE genomic data. This skill covers four major visualization approaches: deepTools heatmaps and profiles, IGV genome browser views, UCSC track hubs for sharing, and publication-quality static plots using R and Python. Visualization is not decorative -- it is an essential analytical step that reveals patterns invisible in summary statistics and validates computational findings.

## Literature Foundation

| Reference | Journal | Key Contribution | DOI | Citations |
|-----------|---------|-----------------|-----|-----------|
| Ramirez et al. (2016) | Nucleic Acids Research | deepTools2: next-generation server for deep-sequencing data analysis; heatmaps, profiles, correlation, PCA | [10.1093/nar/gkw257](https://doi.org/10.1093/nar/gkw257) | ~3,800 |
| Robinson et al. (2011) | Nature Biotechnology | Integrative Genomics Viewer (IGV): interactive exploration of large genomic datasets | [10.1038/nbt.1754](https://doi.org/10.1038/nbt.1754) | ~10,000 |
| Kent et al. (2002) | Genome Research | The Human Genome Browser at UCSC: foundation for track-based genomic visualization | [10.1101/gr.229102](https://doi.org/10.1101/gr.229102) | ~8,000 |
| Ramirez et al. (2014) | Nucleic Acids Research | deepTools: flexible platform for exploring deep-sequencing data; original computeMatrix/plotHeatmap framework | [10.1093/nar/gku365](https://doi.org/10.1093/nar/gku365) | ~2,500 |
| Amemiya et al. (2019) | Scientific Reports | ENCODE Blacklist: comprehensive identification of artifact regions to exclude from visualization | [10.1038/s41598-019-45839-z](https://doi.org/10.1038/s41598-019-45839-z) | ~1,372 |
| Wickham (2016) | Springer | ggplot2: Elegant Graphics for Data Analysis; grammar of graphics for genomic visualization | ISBN: 978-3-319-24277-4 | ~30,000+ |

## Part 1: deepTools Heatmaps and Profiles

deepTools (Ramirez et al. 2014, 2016) is the standard toolkit for visualizing ChIP-seq and ATAC-seq signal across genomic regions. The core workflow is: compute a signal matrix, then render it as a heatmap or profile plot.

### 1a. computeMatrix: Building the Signal Matrix

`computeMatrix` extracts signal values from bigWig files across a set of genomic regions. Two modes are available:

**reference-point mode** -- centers the signal on a single anchor point (e.g., TSS, peak summit):

```bash
# Signal centered on peak summits, +/- 3kb
computeMatrix reference-point \
    -S H3K27ac_fc.bigWig H3K4me3_fc.bigWig ATAC_fc.bigWig \
    -R peaks.bed \
    --referencePoint center \
    -b 3000 -a 3000 \
    --binSize 50 \
    --missingDataAsZero \
    --sortRegions descend \
    --sortUsing mean \
    -o matrix_refpoint.gz \
    -p 8
```

**scale-regions mode** -- scales all regions to uniform length (e.g., gene bodies):

```bash
# Signal across scaled gene bodies with 2kb flanks
computeMatrix scale-regions \
    -S H3K36me3_fc.bigWig RNA_signal.bigWig \
    -R genes.bed \
    --regionBodyLength 5000 \
    -b 2000 -a 2000 \
    --binSize 50 \
    --missingDataAsZero \
    -o matrix_scaled.gz \
    -p 8
```

**When to use which mode**:
- `reference-point`: TF ChIP-seq peaks, ATAC-seq summits, TSSs, enhancer centers -- any feature defined by a point
- `scale-regions`: gene bodies, broad histone domains (H3K27me3, H3K36me3), TADs -- features with variable length

### 1b. plotHeatmap: Rendering the Matrix

```bash
plotHeatmap -m matrix_refpoint.gz \
    -o heatmap.png \
    --colorMap RdYlBu_r \
    --whatToShow "heatmap and colorbar" \
    --sortRegions descend \
    --sortUsing mean \
    --heatmapHeight 15 \
    --heatmapWidth 4 \
    --zMin 0 --zMax 10 \
    --samplesLabel "H3K27ac" "H3K4me3" "ATAC" \
    --regionsLabel "Peaks" \
    --dpi 300
```

**Clustering**: To reveal sub-patterns within peak sets:

```bash
plotHeatmap -m matrix_refpoint.gz \
    -o heatmap_clustered.png \
    --kmeans 4 \
    --colorMap viridis \
    --zMin 0 --zMax 10 \
    --outFileSortedRegions clusters.bed \
    --dpi 300
```

The `--outFileSortedRegions` flag exports the cluster assignments as a BED file, enabling downstream analysis of each cluster separately.

**Recommended color maps by mark type**:
| Mark Type | Recommended colorMap | Rationale |
|-----------|---------------------|-----------|
| Active marks (H3K27ac, H3K4me3) | Reds, YlOrRd | Warm colors for activation |
| Repressive marks (H3K27me3, H3K9me3) | Blues, PuBu | Cool colors for repression |
| Accessibility (ATAC, DNase) | Greens, YlGn | Distinct from histone colors |
| Multi-mark comparison | viridis, inferno | Perceptually uniform, colorblind-safe |

### 1c. plotProfile: Average Signal Plots

Profile plots show the average signal across all regions, useful for comparing samples:

```bash
plotProfile -m matrix_refpoint.gz \
    -o profile.png \
    --perGroup \
    --plotTitle "Signal at H3K27ac peaks" \
    --yAxisLabel "Fold change over input" \
    --samplesLabel "H3K27ac" "H3K4me3" "ATAC" \
    --dpi 300
```

Use `--perGroup` when you have multiple region sets (e.g., active vs poised enhancers) and want separate profile lines for each group.

### 1d. Signal Correlation and PCA

Before making complex visualizations, verify that replicates correlate and conditions separate:

```bash
# Build correlation matrix
multiBigwigSummary bins \
    -b sample1.bw sample2.bw sample3.bw sample4.bw \
    --labels Rep1 Rep2 Rep3 Rep4 \
    --binSize 10000 \
    -o results.npz \
    -p 8

# Correlation heatmap
plotCorrelation -in results.npz \
    --corMethod pearson \
    --whatToPlot heatmap \
    --plotFile correlation.pdf \
    --skipZeros

# PCA plot
plotPCA -in results.npz \
    --plotFile pca.pdf \
    --labels Rep1 Rep2 Rep3 Rep4
```

## Part 2: IGV Visualization

The Integrative Genomics Viewer (Robinson et al. 2011) provides interactive, locus-level inspection of ENCODE data. IGV is essential for validating computational findings at individual loci.

### 2a. Loading ENCODE Files in IGV

ENCODE data can be loaded directly from URLs without downloading:

1. Open IGV and select the correct genome (hg38 for GRCh38, mm10 for mouse)
2. File > Load from URL > paste the ENCODE file download URL
3. For bigWig files, IGV streams data on-the-fly (no full download needed)

**Recommended file types for IGV**:
| File Type | IGV Display | Best For |
|-----------|------------|----------|
| bigWig (fold change over control) | Continuous signal track | Viewing signal intensity |
| bigBed (IDR thresholded peaks) | Discrete interval track | Viewing peak locations |
| BAM (alignments) | Read pileup + coverage | Inspecting read-level evidence |

### 2b. Batch Screenshots with IGV

For systematic locus-level visualization across many genes, use IGV batch scripting:

```
new
genome hg38
load https://www.encodeproject.org/files/ENCFF.../@@download/ENCFF....bigWig
load https://www.encodeproject.org/files/ENCFF.../@@download/ENCFF....bigBed
snapshotDirectory /path/to/output/
goto chr11:2,159,779-2,161,209
snapshot INS_locus.png
goto chr7:44,182,955-44,184,393
snapshot GCK_locus.png
goto chr17:40,927,190-40,928,775
snapshot HNF1B_locus.png
```

Run with: `igv.sh -b batch_script.txt`

### 2c. IGV.js for Web-Based Viewing

For sharing interactive browser views without requiring local IGV installation:

```html
<div id="igv-div"></div>
<script src="https://cdn.jsdelivr.net/npm/igv@2.15.0/dist/igv.min.js"></script>
<script>
var options = {
    genome: "hg38",
    locus: "chr11:2,159,779-2,161,209",
    tracks: [
        {
            name: "H3K27ac Signal",
            url: "https://www.encodeproject.org/files/ENCFF.../@@download/ENCFF....bigWig",
            type: "wig",
            color: "rgb(255,128,0)"
        },
        {
            name: "ATAC Peaks",
            url: "https://www.encodeproject.org/files/ENCFF.../@@download/ENCFF....bigBed",
            type: "annotation",
            color: "rgb(0,150,0)"
        }
    ]
};
igv.createBrowser(document.getElementById("igv-div"), options);
</script>
```

## Part 3: UCSC Track Hubs

UCSC Track Hubs (Kent et al. 2002) enable sharing of custom visualization configurations with collaborators and reviewers. A track hub is a set of text files that describe how to display your data in the UCSC Genome Browser.

### 3a. Hub File Structure

A track hub requires three files hosted on a public web server:

```
hub.txt          # Hub metadata
genomes.txt      # Which genomes are available
hg38/
  trackDb.txt    # Track definitions
  *.bigWig       # Signal files
  *.bigBed        # Peak files
```

**hub.txt**:
```
hub myEncodeHub
shortLabel My ENCODE Analysis
longLabel Integrative analysis of pancreatic islet chromatin
genomesFile genomes.txt
email user@institution.edu
```

**genomes.txt**:
```
genome hg38
trackDb hg38/trackDb.txt
```

### 3b. trackDb.txt: Track Definitions

A composite track hub for comparing multiple experiments:

```
track histoneComposite
compositeTrack on
shortLabel Histone Marks
longLabel Histone modification ChIP-seq from pancreatic islets
type bigWig
visibility full
autoScale off
viewLimits 0:15
maxHeightPixels 100:50:8

    track H3K27ac_signal
    parent histoneComposite
    bigDataUrl H3K27ac_fc.bigWig
    shortLabel H3K27ac
    longLabel H3K27ac fold change over input - pancreatic islet
    type bigWig
    color 255,128,0
    visibility full

    track H3K4me3_signal
    parent histoneComposite
    bigDataUrl H3K4me3_fc.bigWig
    shortLabel H3K4me3
    longLabel H3K4me3 fold change over input - pancreatic islet
    type bigWig
    color 255,0,0
    visibility full

    track H3K27me3_signal
    parent histoneComposite
    bigDataUrl H3K27me3_fc.bigWig
    shortLabel H3K27me3
    longLabel H3K27me3 fold change over input - pancreatic islet
    type bigWig
    color 0,0,255
    visibility full

    track ATAC_signal
    parent histoneComposite
    bigDataUrl ATAC_fc.bigWig
    shortLabel ATAC-seq
    longLabel ATAC-seq signal - pancreatic islet
    type bigWig
    color 0,180,0
    visibility full

track peaksComposite
compositeTrack on
shortLabel Peaks
longLabel Peak calls from ENCODE pipeline
type bigBed
visibility dense

    track H3K27ac_peaks
    parent peaksComposite
    bigDataUrl H3K27ac_peaks.bigBed
    shortLabel H3K27ac peaks
    longLabel H3K27ac IDR thresholded peaks
    type bigBed
    color 255,128,0
    visibility dense

    track ATAC_peaks
    parent peaksComposite
    bigDataUrl ATAC_peaks.bigBed
    shortLabel ATAC peaks
    longLabel ATAC-seq IDR thresholded peaks
    type bigBed
    color 0,180,0
    visibility dense
```

### 3c. Hosting and Loading

Host the hub directory on any HTTPS-accessible server (institutional web space, AWS S3, GitHub Pages, Cyverse). Then load in UCSC:

```
https://genome.ucsc.edu/cgi-bin/hgTracks?db=hg38&hubUrl=https://yourserver.edu/hub.txt
```

**Recommended color scheme for chromatin marks**:
| Mark | RGB Color | Hex |
|------|-----------|-----|
| H3K4me3 | 255,0,0 | #FF0000 |
| H3K27ac | 255,128,0 | #FF8000 |
| H3K4me1 | 255,255,0 | #FFFF00 |
| H3K36me3 | 0,128,0 | #008000 |
| H3K27me3 | 0,0,255 | #0000FF |
| H3K9me3 | 128,128,128 | #808080 |
| ATAC/DNase | 0,180,0 | #00B400 |
| CTCF | 0,180,180 | #00B4B4 |

## Part 4: Publication-Quality Plots

### 4a. R: ggplot2 + GenomicRanges

```r
library(GenomicRanges)
library(ggplot2)
library(ChIPseeker)

# --- Genomic Feature Distribution ---
peaks <- readPeakFile("H3K27ac_peaks.narrowPeak")
txdb <- TxDb.Hsapiens.UCSC.hg38.knownGene::TxDb.Hsapiens.UCSC.hg38.knownGene
peakAnno <- annotatePeak(peaks, TxDb = txdb, level = "gene")

plotAnnoBar(peakAnno) +
    theme_minimal(base_size = 14) +
    ggtitle("H3K27ac Peak Distribution") +
    theme(plot.title = element_text(hjust = 0.5))
ggsave("peak_distribution.pdf", width = 8, height = 5)

# --- Distance to TSS ---
plotDistToTSS(peakAnno, title = "H3K27ac Distance to TSS") +
    theme_minimal(base_size = 14)
ggsave("tss_distance.pdf", width = 8, height = 5)

# --- Peak Width Distribution ---
peak_df <- data.frame(width = width(peaks))
ggplot(peak_df, aes(x = width)) +
    geom_histogram(bins = 100, fill = "#FF8000", alpha = 0.8) +
    scale_x_log10() +
    labs(x = "Peak Width (bp)", y = "Count", title = "H3K27ac Peak Width Distribution") +
    theme_minimal(base_size = 14)
ggsave("peak_widths.pdf", width = 8, height = 5)
```

### 4b. Python: matplotlib and seaborn

```python
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# --- Signal Heatmap from deepTools matrix ---
# Load the deepTools matrix (tab file)
# plotHeatmap --outFileNameMatrix matrix_values.tab exports the raw values
data = np.loadtxt("matrix_values.tab", skiprows=3)

fig, ax = plt.subplots(figsize=(6, 10))
sns.heatmap(
    data,
    cmap="YlOrRd",
    vmin=0, vmax=10,
    xticklabels=False,
    yticklabels=False,
    cbar_kws={"label": "Fold change over input"},
    ax=ax
)
ax.set_xlabel("Position relative to center")
ax.set_ylabel("Peaks (sorted by signal)")
ax.set_title("H3K27ac Signal at ATAC Peaks")
plt.tight_layout()
plt.savefig("signal_heatmap.pdf", dpi=300)

# --- Multi-Sample Correlation Matrix ---
# Use Pearson correlation values from deepTools plotCorrelation --outFileCorMatrix
corr_matrix = np.loadtxt("correlation_matrix.tab", skiprows=1, usecols=range(1,5))
labels = ["Islet_R1", "Islet_R2", "Liver_R1", "Liver_R2"]

fig, ax = plt.subplots(figsize=(7, 6))
sns.heatmap(
    corr_matrix,
    annot=True, fmt=".3f",
    xticklabels=labels, yticklabels=labels,
    cmap="RdYlBu_r",
    vmin=0.5, vmax=1.0,
    square=True,
    ax=ax
)
ax.set_title("Pearson Correlation of H3K27ac Signal")
plt.tight_layout()
plt.savefig("correlation_matrix.pdf", dpi=300)
```

### 4c. Recommended Visualization Settings for Publications

| Element | Recommendation |
|---------|---------------|
| Resolution | 300 DPI minimum for print; 150 DPI for screen |
| Format | PDF or SVG for vector; PNG for raster (avoid JPEG for genomic data) |
| Font | Arial or Helvetica, 8-12pt for labels |
| Color | Use colorblind-safe palettes (viridis, cividis); avoid red-green only |
| Scale bars | Always include genomic coordinate axis |
| Normalization label | State normalization method on y-axis (e.g., "Fold change over input") |
| Panel labels | Use (A), (B), (C) for multi-panel figures |

## Full Workflow

The recommended end-to-end visualization workflow for ENCODE data:

```
Step 1: Download signal and peak files
    encode_search_experiments(assay_title="Histone ChIP-seq", organ="pancreas")
    encode_list_files(experiment_accession="ENCSR...", file_format="bigWig",
                      output_type="fold change over control", assembly="GRCh38")
    encode_download_files(file_accessions=["ENCFF..."], download_dir="/data/")

Step 2: Quality check signal correlation
    multiBigwigSummary + plotCorrelation + plotPCA

Step 3: Generate deepTools heatmaps
    computeMatrix reference-point + plotHeatmap + plotProfile

Step 4: Create UCSC track hub for interactive sharing
    Build hub.txt + genomes.txt + trackDb.txt
    Host on public server and share URL

Step 5: Take IGV snapshots at key loci
    IGV batch script for loci of interest

Step 6: Build publication figures
    R/Python static plots with consistent styling
```

## Common Pitfalls

1. **bigWig normalization mismatch**: ENCODE provides multiple bigWig types per experiment. "Fold change over control" is input-normalized and suitable for cross-experiment comparison. "Signal of unique reads" is raw coverage and NOT comparable across experiments with different sequencing depths. "Signal p-value" shows statistical significance. Always use the same bigWig type across all samples in a visualization. When setting manual y-axis limits, verify the normalization matches.

2. **Color scale saturation**: Auto-scaling (`autoScale on` in UCSC, or default in deepTools) sets the color range to each track's individual min/max. This hides differences between samples -- a weak signal track will look identical to a strong signal track. Always set manual min/max values (`--zMin 0 --zMax 10` in deepTools, `viewLimits 0:15` in UCSC) that are consistent across all tracks being compared. Determine appropriate limits by inspecting the signal distribution first.

3. **Region selection quality**: Heatmaps and profiles are only as good as the regions used. If you compute a heatmap at all 200,000 MACS2 peaks, many will be noise. Filter peaks by IDR threshold, signal value, or overlap with other marks before visualization. For TF ChIP-seq, use IDR thresholded peaks. For comparison heatmaps, use a consensus peak set filtered by quality.

4. **Resolution mismatch**: bigWig files have a fixed bin size determined during generation. If the bigWig has 25bp bins but you set `computeMatrix --binSize 10`, deepTools interpolates rather than gaining resolution. Conversely, using `--binSize 1000` at a narrow locus produces a blocky visualization. Match your visualization bin size to the data resolution and the genomic scale being shown. For most ENCODE bigWigs (10-25bp bins), `--binSize 50` is a good default.

5. **Missing input control track**: Signal tracks without input normalization can show artifacts at high-copy regions, heterochromatic zones, and assembly gaps. Always include the input or IgG control as a reference track in genome browser views. For deepTools heatmaps, use "fold change over control" bigWigs which already have the input subtracted. When building track hubs, include the input track alongside the ChIP signal so reviewers can assess background.

## Presenting Results

When showing visualization commands and outputs to the user:

- **Show the full command** with all parameters, not just the tool name
- **Explain the output files**: list file names, formats, and what each shows
- **Suggest follow-up analyses**: if the heatmap reveals clusters, suggest differential analysis of each cluster; if IGV shows unexpected signal, suggest quality-checking the experiment
- **Provide figure legends**: draft publication-ready figure legends describing what is shown, what normalization was used, and what the color scale represents

## Walkthrough: Creating a Multi-Mark Signal Heatmap for Liver Enhancers

**Goal**: Visualize H3K27ac, H3K4me1, and ATAC-seq signal at liver enhancers using deeptools.
**Context**: User has identified liver enhancer peaks and wants publication-ready heatmaps.

### Step 1: Find signal tracks for three marks

```
encode_search_files(
  assay_title="Histone ChIP-seq",
  organ="liver",
  target="H3K27ac",
  file_format="bigWig",
  output_type="fold change over control",
  assembly="GRCh38"
)
```

Expected output:
```json
{
  "total": 6,
  "files": [{"accession": "ENCFF234ACE", "output_type": "fold change over control", "file_size_mb": 142.5}]
}
```

### Step 2: Download bigWig files for visualization

```
encode_download_files(
  accessions=["ENCFF234ACE", "ENCFF567ME1", "ENCFF890ATQ"],
  download_dir="/data/viz/liver_enhancers"
)
```

### Step 3: Generate heatmap with deeptools

Run computeMatrix and plotHeatmap (see bioinformatics-installer skill for deeptools installation):
- `computeMatrix reference-point -S H3K27ac.bw H3K4me1.bw ATAC.bw -R enhancers.bed`
- `plotHeatmap -m matrix.gz -o liver_enhancer_heatmap.pdf`

**Interpretation**: Active enhancers show H3K27ac + H3K4me1 flanking the ATAC-seq accessibility summit. Poised enhancers show H3K4me1 without H3K27ac.

## Code Examples

### 1. Search for signal tracks to visualize

```
encode_search_files(
  organ="brain",
  assay_title="ATAC-seq",
  file_format="bigWig",
  output_type="fold change over control",
  assembly="GRCh38"
)
```

Expected output:
```json
{
  "total": 12,
  "files": [
    {"accession": "ENCFF111BRN", "file_format": "bigWig", "output_type": "fold change over control", "file_size_mb": 98.7}
  ]
}
```

## Integration

| This skill produces... | Feed into... | Using tool/skill |
|---|---|---|
| Heatmap figures (PDF/PNG) | Figure legends | scientific-writing skill |
| Track hub configuration files | UCSC Genome Browser display | ucsc-browser skill |
| Signal matrices (deeptools) | Clustering analysis | integrative-analysis skill |
| Genome browser screenshots | Publication figures | scientific-writing -> figure legends |
| Peak-centered signal profiles | Motif enrichment context | motif-analysis skill |

## Related Skills

- **histone-aggregation** -- Merge histone ChIP-seq peaks across experiments before visualization; provides the peak sets for heatmaps
- **accessibility-aggregation** -- Merge ATAC-seq/DNase-seq peaks across experiments; provides accessible regions for signal visualization
- **epigenome-profiling** -- Build comprehensive epigenomic profiles that feed into multi-mark heatmaps and track hubs
- **quality-assessment** -- Verify experiment quality before investing time in visualization; poor quality data produces misleading heatmaps
- **download-encode** -- Retrieve the bigWig and BED files needed as input for all visualization approaches
- **publication-trust** -- Verify literature claims backing analytical decisions

## For the request: "$ARGUMENTS"
