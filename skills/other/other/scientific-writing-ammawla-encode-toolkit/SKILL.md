---
name: scientific-writing
description: "Generate publication-ready methods sections, figure legends, supplementary tables, and data availability statements from ENCODE analysis provenance. Implements the scientific documentation standards requiring complete metadata reporting. Use when the user needs to write methods, generate figure legends, create supplementary tables, draft data availability statements, compile tool citations, or auto-generate any publication text from their ENCODE analysis. Trigger on: methods section, figure legend, supplementary table, data availability, tool citations, publication writing, manuscript, write methods, methods draft, write up, write-up, paper writing, reproducible methods."
---

# Scientific Writing from ENCODE Provenance

Generate publication-quality scientific writing from ENCODE analysis records. This skill integrates with `data-provenance` and `cite-encode` to auto-generate methods from logged pipeline runs. Every generated section follows rigorous scientific documentation standards -- complete reporting of all experimental and computational parameters with zero ambiguity.

## When to Use

- User wants to write publication-ready methods sections, figure legends, or data availability statements
- User asks about "methods section", "figure legend", "scientific writing", or "manuscript preparation"
- User needs to auto-generate methods text from logged provenance/analysis steps
- User wants templates for supplementary tables, Key Resources Tables, or tool citation formatting
- Example queries: "write a methods section for my ChIP-seq analysis", "generate a figure legend for my heatmap", "format my data availability statement"

## Overview

Most methods sections in genomics papers are incomplete. They omit software versions, skip reference file details, conflate technical and biological replicates, and use phrases like "default parameters" without stating what those defaults are. Reviewers catch these omissions, and readers cannot reproduce the analysis.

This skill solves the problem by generating methods text directly from the provenance chain. When every processing step has been logged (via `data-provenance`), the methods section writes itself. When metadata has been captured from ENCODE (via `track-experiments`), the experimental details are already recorded. This skill assembles these records into publication-ready prose, figure legends, supplementary tables, and data availability statements.

This standard is not aspirational -- it is the minimum bar for reproducible science.

## Scientific Documentation Standards -- Required Metadata

Every methods section MUST report the following fields. Omitting any of these fields produces an incomplete methods section that reviewers will flag and readers cannot reproduce.

| Field | Example | Why Required |
|---|---|---|
| Library preparation | TruSeq ChIP | Affects fragment size distribution and GC bias |
| Biological replicates | n=2 per condition | Statistical power and reproducibility |
| Cells/nuclei per replicate | 50,000 cells | Input sufficiency for the assay |
| Sequencing reads | 30M paired-end | Coverage depth determines sensitivity |
| Read length | 2x150 bp | Alignment accuracy and mappability |
| Paired/single-end | Paired-end | Fragment size estimation, structural variants |
| Sequencer | NovaSeq 6000 | Quality profile, error model, binning |
| Lab/batch | Snyder Lab, Stanford | Batch effect awareness |
| Reference genome | GRCh38/hg38 | Coordinate system for all downstream analysis |
| Gene annotation | GENCODE v44 | Gene definitions change between versions |
| ENCODE accessions | ENCSR133RZO | Exact data provenance for reproducibility |
| Blacklist version | ENCODE Blacklist v2 | Artifact exclusion affects all peak-based analyses |

### How to Populate These Fields

```
# Track the experiment to capture metadata
encode_track_experiment(accession="ENCSR...", fetch_publications=True)

# Get full experiment details
encode_get_experiment(accession="ENCSR...")

# Get file-level metadata
encode_get_file_info(accession="ENCFF...")

# Get provenance for derived files
encode_get_provenance(file_path="/path/to/derived/file.bed")
```

## Methods Section Templates

Each template below is a fill-in-the-blank paragraph that reads like a real methods section. Bracketed fields `[like this]` are populated from ENCODE metadata and provenance records. Every template follows these documentation standards.

### ChIP-seq Methods

```text
Chromatin immunoprecipitation followed by sequencing (ChIP-seq) data for
[target] in [biosample] were obtained from the ENCODE Project (ENCODE
Project Consortium 2020) under accession [ENCSR accession]. [Library
preparation method] libraries were prepared from [number] biological
replicates ([cells/nuclei] per replicate) and sequenced on an Illumina
[sequencer model] to generate [read count]M [paired-end/single-end]
reads of [read length] bp per replicate.

Raw reads were assessed with FastQC (v[version]; Andrews 2010) and
trimmed with Trim Galore (v[version]; Krueger 2015) to remove adapter
sequences and low-quality bases (Phred < 20). Trimmed reads were aligned
to the [organism] reference genome ([assembly]) using BWA-MEM (v[version];
Li 2013) with default parameters. Duplicate reads were marked and removed
using Picard MarkDuplicates (v[version]; Broad Institute). Reads with
mapping quality < 30 were excluded using samtools (v[version]; Danecek
et al. 2021). Reads mapping to ENCODE Blacklist v2 regions (Amemiya et al.
2019) were removed using bedtools intersect (v[version]; Quinlan & Hall
2010).

Peaks were called using MACS2 (v[version]; Zhang et al. 2008) with
parameters [--broad for broad marks / -q 0.05 for narrow marks]. For
narrow-peak targets, IDR analysis (Li et al. 2011) was performed on
replicate peak sets with a threshold of [0.05]. Signal tracks (fold
change over control) were generated using MACS2 bdgcmp and converted
to bigWig format using bedGraphToBigWig (Kent et al. 2010). Of [N]
called peaks, [N] ([%]) passed IDR filtering and [N] ([%]) remained
after blacklist removal.
```

### ATAC-seq Methods

```text
Assay for Transposase-Accessible Chromatin with sequencing (ATAC-seq) data
for [biosample] were obtained from the ENCODE Project (ENCODE Project
Consortium 2020) under accession [ENCSR accession]. [Number] biological
replicates of [cells/nuclei] [cells/nuclei] each were transposed with
Tn5 transposase ([library kit]) and sequenced on an Illumina [sequencer]
to generate [read count]M [paired-end/single-end] reads of [read length]
bp per replicate.

Raw reads were assessed with FastQC (v[version]; Andrews 2010) and
adapter-trimmed with Trim Galore (v[version]; Krueger 2015). Trimmed
reads were aligned to [assembly] using Bowtie2 (v[version]; Langmead &
Salzberg 2012) with parameters --very-sensitive -X 2000 --no-mixed
--no-discordant. Mitochondrial reads were removed. Duplicate reads were
removed using Picard MarkDuplicates (v[version]; Broad Institute). Reads
with mapping quality < 30 were excluded. Tn5 transposase offset
correction was applied (+4 bp on the positive strand, -5 bp on the
negative strand; Buenrostro et al. 2013). ENCODE Blacklist v2 regions
(Amemiya et al. 2019) were excluded.

Peaks were called using MACS2 (v[version]; Zhang et al. 2008) with
parameters --nomodel --shift -75 --extsize 150 --keep-dup all -q 0.05.
Nucleosome-free fragments (< 150 bp) were used for peak calling. Signal
tracks were generated as fold change over background. TSS enrichment
score was [value] (threshold >= 6; ENCODE data standards; Yan et al. 2020). Of [N]
called peaks, [N] ([%]) passed quality filtering.
```

### RNA-seq Methods

```text
RNA sequencing (RNA-seq) data for [biosample] were obtained from the
ENCODE Project (ENCODE Project Consortium 2020) under accession [ENCSR
accession]. Total RNA was extracted from [number] biological replicates
and [library preparation method] libraries were prepared. Libraries were
sequenced on an Illumina [sequencer] to generate [read count]M
[paired-end/single-end] reads of [read length] bp per replicate.

Raw reads were assessed with FastQC (v[version]; Andrews 2010) and
MultiQC (v[version]; Ewels et al. 2016). Adapter sequences were trimmed
with Trim Galore (v[version]; Krueger 2015). Reads were aligned to
[assembly] with [GENCODE annotation version] gene annotations using STAR
(v[version]; Dobin et al. 2013) in two-pass mode. Gene-level
quantification was performed using RSEM (v[version]; Li & Dewey 2011)
for expected counts and TPM values. Transcript-level quantification was
obtained with Kallisto (v[version]; Bray et al. 2016). Mapping rate was
[%] and rRNA contamination was [%] (thresholds: mapping 70-90%, rRNA <
10%; Conesa et al. 2016; ENCODE data standards). Replicate Pearson correlation was [r value]
(threshold >= 0.9).

Differential expression analysis was performed using DESeq2 (v[version];
Love et al. 2014) in R (v[version]). The design formula was [~ batch +
condition]. Genes with |log2 fold change| > [threshold] and Benjamini-
Hochberg adjusted p-value < [threshold] were considered differentially
expressed. Of [N] genes tested, [N] ([%]) were significantly
upregulated and [N] ([%]) were significantly downregulated.
```

### WGBS Methods

```text
Whole-genome bisulfite sequencing (WGBS) data for [biosample] were
obtained from the ENCODE Project (ENCODE Project Consortium 2020) under
accession [ENCSR accession]. Genomic DNA from [number] biological
replicates was bisulfite-converted using [conversion kit] and sequenced
on an Illumina [sequencer] to generate [read count]M [paired-end/
single-end] reads of [read length] bp per replicate.

Raw reads were assessed with FastQC (v[version]; Andrews 2010) and
trimmed with Trim Galore (v[version]; Krueger 2015) in --rrbs mode
[if applicable] or standard mode. Trimmed reads were aligned to
[assembly] using Bismark (v[version]; Krueger & Andrews 2011) with
Bowtie2 as the underlying aligner. Duplicate reads were removed using
Bismark deduplicate_bismark. Methylation calls were extracted using
MethylDackel (v[version]; https://github.com/dpryan79/MethylDackel)
with parameters [--minDepth X --mergeContext]. Bisulfite conversion
efficiency was [%] (threshold >= 98%; ENCODE data standards). CpG sites with
coverage >= [X]x were retained for analysis ([N] CpGs, [%] of all
genomic CpGs).

Differentially methylated regions (DMRs) were identified using DMRcate
(v[version]; Peters et al. 2021) with parameters [lambda, C]. CpG
sites within ENCODE Blacklist v2 regions (Amemiya et al. 2019) were
excluded prior to DMR calling.
```

### Hi-C Methods

```text
Hi-C data for [biosample] were obtained from the ENCODE Project (ENCODE
Project Consortium 2020) under accession [ENCSR accession]. Chromatin
was crosslinked, digested with [restriction enzyme], proximity-ligated,
and sequenced on an Illumina [sequencer] to generate [read count]M
[paired-end] reads of [read length] bp across [number] biological
replicates.

Read pairs were aligned to [assembly] using BWA-MEM (v[version]; Li
2013) and processed with pairtools (v[version]; Open2C et al. 2024) for
pair classification, deduplication, and filtering. Valid interaction
pairs (cis-reads with MAPQ >= 30) were retained. Contact matrices were
generated using cooler (v[version]; Abdennur & Mirny 2020) at
resolutions of [1kb, 5kb, 10kb, 25kb, 50kb, 100kb, 250kb, 500kb, 1Mb].
Matrices were balanced using iterative correction (ICE; Imakaev et al.
2012). Cis/trans ratio was [%] (threshold > 60%) and long-range cis
interactions (> 20kb) comprised [%] of total (threshold > 40%; Yardimci
et al. 2019).

Chromatin loops were called using HiCCUPS (Juicer v[version]; Durand
et al. 2016) at [resolutions] with default FDR thresholds.
Topologically associating domains (TADs) were identified using [method]
at [resolution]. [N] loops and [N] TADs were identified.
```

### CUT&RUN Methods

```text
Cleavage Under Targets and Release Using Nuclease (CUT&RUN) data for
[target] in [biosample] were obtained from the ENCODE Project (ENCODE
Project Consortium 2020) under accession [ENCSR accession]. [Number]
biological replicates of [cells/nuclei] each were incubated with
[antibody] and processed with protein A-MNase. Released DNA fragments
were sequenced on an Illumina [sequencer] to generate [read count]M
[paired-end] reads of [read length] bp per replicate.

Raw reads were assessed with FastQC (v[version]; Andrews 2010) and
trimmed with Trim Galore (v[version]; Krueger 2015). Reads were aligned
to [assembly] using Bowtie2 (v[version]; Langmead & Salzberg 2012) with
parameters --very-sensitive --no-mixed --no-discordant -X 700. Spike-in
reads (E. coli or S. cerevisiae) were aligned separately and used for
calibration normalization ([spike-in method]). Duplicate reads were
removed with Picard MarkDuplicates (v[version]; Broad Institute). ENCODE
Blacklist v2 and suspect list regions (Amemiya et al. 2019; Nordin et
al. 2023) were excluded.

Peaks were called using SEACR (v[version]; Meers et al. 2019) in
[stringent/relaxed] mode with [IgG control / numeric threshold]. Note:
CUT&RUN has different QC profiles than ChIP-seq; standard ChIP-seq
metrics (FRiP, NSC, RSC) should not be directly applied (Nordin et al.
2023). [N] peaks were identified across replicates.
```

### Single-cell RNA-seq Methods

```text
Single-cell RNA sequencing (scRNA-seq) data for [biosample] were obtained
from the ENCODE Project (ENCODE Project Consortium 2020) under accession
[ENCSR accession]. [Cell/nuclei isolation method] was performed on
[number] biological replicates. Libraries were prepared using [10x
Genomics Chromium / Smart-seq2 / other platform] targeting [N] cells per
replicate, and sequenced on an Illumina [sequencer] to generate [read
count]M reads per sample.

Raw reads were processed with [CellRanger v[version] (10x Genomics) /
STARsolo (STAR v[version]; Dobin et al. 2013)] to generate gene-cell
count matrices against [assembly] with [GENCODE annotation version].
Ambient RNA contamination was estimated and removed using [SoupX
(v[version]; Young & Behjati 2020) / CellBender (v[version]; Fleming
et al. 2023)]. Doublets were detected and removed using [Scrublet
(v[version]; Wolock et al. 2019) / DoubletFinder (v[version]; McGinnis
et al. 2019)]. Cells with [< N genes, > N% mitochondrial reads, < N
UMIs] were excluded.

Data were normalized using [SCTransform (v[version]; Hafemeister & Satija
2019) / scran (v[version]; Lun et al. 2016)] and integrated across
samples using [Harmony (v[version]; Korsunsky et al. 2019) / scVI
(v[version]; Lopez et al. 2018)]. Dimensionality reduction was performed
using PCA ([N] components) followed by UMAP (n_neighbors=[N],
min_dist=[value]; McInnes et al. 2018). Clustering was performed using
the Leiden algorithm (resolution=[value]; Traag et al. 2019) implemented
in [Seurat v[version] (Hao et al. 2024) / Scanpy v[version] (Wolf et
al. 2018)]. Cell types were annotated based on [marker genes / reference
mapping / automated annotation with method]. Final dataset comprised [N]
cells across [N] clusters representing [N] cell types.
```

## Figure Legend Templates

### Genome Browser Screenshot

```text
Figure [N]. Genome browser view of [mark/signal] at the [gene name]
locus ([chr]:[start]-[end], [assembly]). Tracks shown from top to
bottom: [track 1 description, e.g., "H3K27ac ChIP-seq signal in
pancreatic islets (ENCSR...)"], [track 2], [track 3]. Signal tracks
represent fold change over input control. [Gene models from GENCODE
v[version] are shown at bottom.] [Shaded region highlights the
[promoter/enhancer/regulatory element] of interest.] Data were obtained
from the ENCODE Project (ENCODE Project Consortium 2020).
```

### Heatmap

```text
Figure [N]. Heatmap of [signal type, e.g., "H3K27ac ChIP-seq signal"]
across [N] [regions/genes/peaks] in [N] [samples/conditions/cell types].
Rows represent [individual peaks / genes / genomic regions], sorted by
[k-means clustering (k=[N]) / hierarchical clustering (method=[ward.D2],
distance=[euclidean]) / signal intensity]. Columns represent [samples /
cell types / conditions]. Color scale indicates [log2 fold change /
z-scored signal / CPM / RPKM] with [color scheme, e.g., "blue-white-red
diverging scale, range [-2, 2]"]. [Normalization method: quantile /
library size / spike-in.] Heatmap was generated using [deepTools
computeMatrix + plotHeatmap (v[version]; Ramirez et al. 2016) /
ComplexHeatmap (v[version]; Gu et al. 2016) / pheatmap (v[version];
Kolde 2019)].
```

### Volcano Plot

```text
Figure [N]. Volcano plot of differentially expressed genes between
[condition A] and [condition B] in [biosample/cell type]. X-axis shows
log2 fold change; y-axis shows -log10 adjusted p-value (Benjamini-
Hochberg correction). Significance thresholds: |log2FC| > [threshold]
(vertical dashed lines) and adjusted p-value < [threshold] (horizontal
dashed line). Red points: [N] significantly upregulated genes. Blue
points: [N] significantly downregulated genes. Gray points: [N] non-
significant genes. [Selected genes are labeled.] Differential expression
analysis was performed using [DESeq2 / edgeR / limma-voom] (v[version]).
[N] total genes were tested.
```

### Hi-C Contact Map

```text
Figure [N]. Hi-C contact frequency map of [region, e.g., "chromosome 7:
25-30 Mb"] in [biosample] at [resolution, e.g., "10 kb"] resolution.
Upper triangle: [observed / Knight-Ruiz balanced / ICE-normalized]
contact frequencies displayed on a [log / linear] color scale. [Lower
triangle: [comparison condition / O/E ratio / difference map].] [Loops
identified by HiCCUPS are marked with [circles/squares].] [TAD
boundaries identified by [method] are shown as [lines/triangles].]
Contact matrix was generated using [cooler (Abdennur & Mirny 2020) /
Juicer (Durand et al. 2016)] from [N]M valid read pairs. Data were
obtained from ENCODE accession [ENCSR...].
```

### UMAP / tSNE

```text
Figure [N]. [UMAP / tSNE] projection of [N] single cells from
[biosample] colored by [cluster identity / gene expression / sample
origin / cell cycle phase]. [UMAP parameters: n_neighbors=[N],
min_dist=[value], computed on [N] principal components. / tSNE
parameters: perplexity=[N], computed on [N] principal components.]
[N] clusters were identified using the [Leiden / Louvain] algorithm
(resolution=[value]). Cell types were annotated based on [canonical
marker gene expression / reference-based mapping using [SingleR /
Azimuth / scArches] / manual curation]. [Inset: expression of [gene
name] across clusters, showing enrichment in [cell type].]
```

### Venn / UpSet Diagram

```text
Figure [N]. [Venn diagram / UpSet plot] showing overlap of [peak sets /
gene lists / regulatory elements] across [N] [conditions / cell types /
datasets]. Set definitions: [Set A] = [N] [peaks/genes] from [source],
[Set B] = [N] [peaks/genes] from [source][, Set C = ...]. Overlaps were
computed using [bedtools intersect (minimum [N] bp overlap) / exact gene
ID matching]. [N] [peaks/genes] ([%]) were shared across all sets; [N]
([%]) were unique to [Set A]. [Statistical significance of overlap was
assessed using [Fisher exact test / hypergeometric test / permutation
test (N=[iterations])]; p = [value].] [UpSet plot generated with
UpSetR (v[version]; Conway et al. 2017).]
```

### Peak Genomic Distribution Bar Chart

```text
Figure [N]. Genomic feature distribution of [N] [peak type, e.g.,
"H3K27ac peaks"] in [biosample]. Peaks were annotated using ChIPseeker
(v[version]; Yu et al. 2015) with [GENCODE v[version] / TxDb annotation
version] gene models. Bars show percentage of peaks overlapping each
genomic feature category: promoter (<= [N] kb from TSS, [%]), 5' UTR
([%]), 3' UTR ([%]), exon ([%]), intron ([%]), downstream (<= [N] kb,
[%]), and intergenic ([%]). [Background genomic distribution is shown
for comparison (gray bars).] [A second panel shows the distribution of
peak distance to nearest TSS.]
```

## Supplementary Table Templates

### Table S1: Experiment Metadata

A master table listing all ENCODE experiments used in the study.

| Column | Description | Source |
|--------|-------------|--------|
| ENCODE Accession | ENCSR identifier | encode_get_experiment |
| Assay | Assay type (ChIP-seq, ATAC-seq, etc.) | encode_get_experiment |
| Target | Antibody target (for ChIP/CUT&RUN) | encode_get_experiment |
| Biosample | Tissue or cell type | encode_get_experiment |
| Organism | Species | encode_get_experiment |
| Assembly | Genome build | encode_get_experiment |
| Lab | Submitting laboratory | encode_get_experiment |
| Biological Replicates | Number of bio reps | encode_get_experiment |
| Sequencing Reads | Total reads per replicate | File metadata |
| Read Length | bp, paired/single | File metadata |
| Sequencer | Instrument model | encode_get_experiment |
| Library | Library preparation method | encode_get_experiment |
| Date Released | Release date on ENCODE portal | encode_get_experiment |
| Audit Status | ENCODE quality audit level | encode_get_experiment |

Generate with:
```
encode_export_data(format="csv")
```

### Table S2: Quality Control Metrics

Assay-specific QC metrics for all experiments. Columns depend on the assay type.

**ChIP-seq columns**: Accession, Target, Total reads, Mapped reads, Mapping rate, Duplicate rate, NRF, PBC1, PBC2, NSC, RSC, FRiP, Peak count, IDR peaks

**ATAC-seq columns**: Accession, Total reads, Mapped reads, Mapping rate, Mitochondrial rate, Duplicate rate, NRF, TSS enrichment, Fragment size distribution (NFR/mono/di), FRiP, Peak count

**RNA-seq columns**: Accession, Total reads, Mapped reads, Mapping rate, rRNA rate, Exonic rate, Intronic rate, Intergenic rate, Genes detected (TPM > 1), Replicate correlation (Pearson r)

**WGBS columns**: Accession, Total reads, Mapped reads, Mapping rate, Bisulfite conversion rate, CpG coverage (mean), CpGs at 1x, CpGs at 5x, CpGs at 10x, Global methylation (%)

**Hi-C columns**: Accession, Total read pairs, Valid pairs, Cis pairs (%), Trans pairs (%), Long-range cis (%), Short-range cis (%), Duplicate rate, Library complexity

**QC thresholds** (include as table footnotes):
- ChIP-seq: FRiP >= 1%, NSC > 1.05, RSC > 0.8, NRF >= 0.8 (Landt et al. 2012)
- ATAC-seq: TSS enrichment >= 5 (GRCh38), >= 6 (hg19), >= 10 (mm10); nucleosomal ladder visible (ENCODE data standards; Yan et al. 2020)
- RNA-seq: Mapping 70-90%, rRNA < 10%, replicate r >= 0.9 (Conesa et al. 2016; ENCODE data standards)
- WGBS: Conversion >= 98%, CpG coverage >= 10x for DMRs (ENCODE data standards)
- Hi-C: Cis/trans > 60%, long-range cis > 40% (Yardimci et al. 2019)

### Table S3: Differential Results

For differential expression, differential accessibility, or differential methylation analyses.

| Column | Description |
|--------|-------------|
| Feature ID | Gene ID / Peak ID / CpG ID |
| Gene Symbol | Gene name (for expression) |
| Chromosome | chr |
| Start | Start coordinate |
| End | End coordinate |
| log2 Fold Change | Effect size |
| Standard Error | SE of log2FC |
| Stat | Test statistic |
| P-value | Raw p-value |
| Adjusted P-value | BH-corrected FDR |
| Base Mean / Mean Signal | Average expression or signal |

### Table S4: Peak / Region Catalog

For aggregated or filtered peak sets.

| Column | Description |
|--------|-------------|
| Chromosome | chr |
| Start | Start coordinate (0-based) |
| End | End coordinate |
| Name | Peak identifier |
| Score | Scaled score (0-1000) |
| Signal Value | Fold enrichment or signal |
| P-value | -log10(p-value) |
| Q-value | -log10(q-value) |
| Summit | Distance from start to summit |
| Source Accession | ENCODE file accession |
| Biosample | Source tissue/cell type |

### Table S5: Software Versions

Every tool used in the analysis with version and citation.

| Column | Description |
|--------|-------------|
| Software | Tool name |
| Version | Exact version string |
| Purpose | What it was used for |
| Citation | Publication reference |
| DOI | Digital Object Identifier |
| URL | Download or documentation URL |

## Data Availability Statements

### Standard ENCODE Data Availability

```text
All sequencing data used in this study are publicly available through
the ENCODE Project portal (https://www.encodeproject.org) under the
following experiment accessions: [ENCSR list]. Processed files including
[peak calls / gene quantifications / contact matrices / methylation
calls] used in this analysis are available under file accessions [ENCFF
list]. ENCODE data are released under unrestricted use policy with no
embargo period (ENCODE Project Consortium 2020).
```

### Derived Data Availability

```text
All derived data generated in this study, including [filtered peak sets /
merged catalogs / differential results / aggregated matrices], are
available at [repository URL / GEO accession / Zenodo DOI]. Complete
analysis scripts, provenance logs, and software environment
specifications are available at [GitHub URL]. A detailed description of
all processing steps, parameters, and software versions is provided in
Supplementary Table S[N].
```

### Code Availability

```text
Code used for all analyses in this study is available at [GitHub URL].
The repository includes [Nextflow / Snakemake / Bash / R / Python]
scripts for [list major analyses], along with the complete software
environment specification ([Docker image / conda environment YAML /
renv.lock]). All computational tools and their versions are listed in
Supplementary Table S[N].
```

### GEO Cross-Reference (when applicable)

```text
Raw sequencing data generated in this study have been deposited in the
Gene Expression Omnibus (GEO) under accession [GSE number]. Processed
data are available at the same accession. Previously published ENCODE
data used in this study are available at https://www.encodeproject.org
under accessions listed in Supplementary Table S1.
```

## Tool Citation Reference

Every bioinformatics tool used in an analysis must be cited with its full publication reference. The following table covers the most commonly used tools in ENCODE-based analyses.

### Alignment and Read Processing

| Tool | Citation | Journal | Year | DOI |
|------|----------|---------|------|-----|
| BWA-MEM | Li H | arXiv | 2013 | 10.48550/arXiv.1303.3997 |
| Bowtie2 | Langmead B & Salzberg SL | Nature Methods | 2012 | 10.1038/nmeth.1923 |
| STAR | Dobin A et al. | Bioinformatics | 2013 | 10.1093/bioinformatics/bts635 |
| HISAT2 | Kim D et al. | Nature Biotechnology | 2019 | 10.1038/s41587-019-0201-4 |
| minimap2 | Li H | Bioinformatics | 2018 | 10.1093/bioinformatics/bty191 |
| samtools | Danecek P et al. | GigaScience | 2021 | 10.1093/gigascience/giab008 |
| Picard | Broad Institute | -- | -- | broadinstitute.github.io/picard |
| sambamba | Tarasov A et al. | Bioinformatics | 2015 | 10.1093/bioinformatics/btv098 |

### Quality Control

| Tool | Citation | Journal | Year | DOI |
|------|----------|---------|------|-----|
| FastQC | Andrews S | Babraham Bioinformatics | 2010 | bioinformatics.babraham.ac.uk |
| MultiQC | Ewels P et al. | Bioinformatics | 2016 | 10.1093/bioinformatics/btw354 |
| Trim Galore | Krueger F | Babraham Bioinformatics | 2015 | github.com/FelixKrueger/TrimGalore |
| fastp | Chen S et al. | Bioinformatics | 2018 | 10.1093/bioinformatics/bty560 |
| Preseq | Daley T & Smith AD | Nature Methods | 2013 | 10.1038/nmeth.2375 |
| Qualimap | Okonechnikov K et al. | Bioinformatics | 2016 | 10.1093/bioinformatics/btv566 |

### Peak Calling and Signal Analysis

| Tool | Citation | Journal | Year | DOI |
|------|----------|---------|------|-----|
| MACS2 | Zhang Y et al. | Genome Biology | 2008 | 10.1186/gb-2008-9-9-r137 |
| IDR | Li Q et al. | Annals of Applied Statistics | 2011 | 10.1214/11-AOAS466 |
| SEACR | Meers MP et al. | Epigenetics & Chromatin | 2019 | 10.1186/s13072-019-0287-4 |
| Hotspot2 | John S et al. | -- | 2022 | github.com/Altius/hotspot2 |
| HOMER | Heinz S et al. | Molecular Cell | 2010 | 10.1016/j.molcel.2010.05.004 |
| F-Seq2 | Zhao H et al. | Bioinformatics | 2020 | 10.1093/bioinformatics/btab273 |
| deepTools | Ramirez F et al. | Nucleic Acids Research | 2016 | 10.1093/nar/gkw257 |
| bedtools | Quinlan AR & Hall IM | Bioinformatics | 2010 | 10.1093/bioinformatics/btq033 |
| bedGraphToBigWig | Kent WJ et al. | Bioinformatics | 2010 | 10.1093/bioinformatics/btq351 |

### RNA-seq Quantification and Differential Expression

| Tool | Citation | Journal | Year | DOI |
|------|----------|---------|------|-----|
| RSEM | Li B & Dewey CN | BMC Bioinformatics | 2011 | 10.1186/1471-2105-12-323 |
| Kallisto | Bray NL et al. | Nature Biotechnology | 2016 | 10.1038/nbt.3519 |
| Salmon | Patro R et al. | Nature Methods | 2017 | 10.1038/nmeth.4197 |
| featureCounts | Liao Y et al. | Bioinformatics | 2014 | 10.1093/bioinformatics/btt656 |
| HTSeq | Anders S et al. | Bioinformatics | 2015 | 10.1093/bioinformatics/btu638 |
| DESeq2 | Love MI et al. | Genome Biology | 2014 | 10.1186/s13059-014-0550-8 |
| edgeR | Robinson MD et al. | Bioinformatics | 2010 | 10.1093/bioinformatics/btp616 |
| limma | Ritchie ME et al. | Nucleic Acids Research | 2015 | 10.1093/nar/gkv007 |

### Bisulfite Sequencing / Methylation

| Tool | Citation | Journal | Year | DOI |
|------|----------|---------|------|-----|
| Bismark | Krueger F & Andrews SR | Bioinformatics | 2011 | 10.1093/bioinformatics/btr167 |
| MethylDackel | Ryan DP | GitHub | -- | github.com/dpryan79/MethylDackel |
| DMRcate | Peters TJ et al. | Epigenetics & Chromatin | 2021 | 10.1186/s13072-021-00428-1 |
| bsmap | Xi Y & Li W | BMC Bioinformatics | 2009 | 10.1186/1471-2105-10-232 |
| methylKit | Akalin A et al. | Genome Biology | 2012 | 10.1186/gb-2012-13-10-r87 |

### 3D Genome / Hi-C

| Tool | Citation | Journal | Year | DOI |
|------|----------|---------|------|-----|
| pairtools | Open2C et al. | PLOS Computational Biology | 2024 | 10.1371/journal.pcbi.1012164 |
| cooler | Abdennur N & Mirny LA | Bioinformatics | 2020 | 10.1093/bioinformatics/btz540 |
| Juicer | Durand NC et al. | Cell Systems | 2016 | 10.1016/j.cels.2016.07.002 |
| HiCCUPS | Rao SSP et al. | Cell | 2014 | 10.1016/j.cell.2014.11.021 |
| FAN-C | Kruse K et al. | Genome Biology | 2020 | 10.1186/s13059-020-02215-9 |
| Mustache | Roayaei Ardakany A et al. | Genome Biology | 2020 | 10.1186/s13059-020-02167-0 |
| HiGlass | Kerpedjiev P et al. | Genome Biology | 2018 | 10.1186/s13059-018-1486-1 |

### Single-Cell Analysis

| Tool | Citation | Journal | Year | DOI |
|------|----------|---------|------|-----|
| Seurat | Hao Y et al. | Nature Biotechnology | 2024 | 10.1038/s41587-023-01767-y |
| Scanpy | Wolf FA et al. | Genome Biology | 2018 | 10.1186/s13059-017-1382-0 |
| SCTransform | Hafemeister C & Satija R | Genome Biology | 2019 | 10.1186/s13059-019-1874-1 |
| scran | Lun ATL et al. | Genome Biology | 2016 | 10.1186/s13059-016-0947-7 |
| Harmony | Korsunsky I et al. | Nature Methods | 2019 | 10.1038/s41592-019-0619-0 |
| scVI | Lopez R et al. | Nature Methods | 2018 | 10.1038/s41592-018-0229-2 |
| CellRanger | 10x Genomics | -- | -- | support.10xgenomics.com |
| STARsolo | Kaminow B et al. | Cell Genomics | 2021 | 10.1016/j.xgen.2021.100004 |
| Scrublet | Wolock SL et al. | Cell Systems | 2019 | 10.1016/j.cels.2018.11.005 |
| DoubletFinder | McGinnis CS et al. | Cell Systems | 2019 | 10.1016/j.cels.2019.03.003 |
| SoupX | Young MD & Behjati S | GigaScience | 2020 | 10.1093/gigascience/giaa151 |
| SingleR | Aran D et al. | Nature Immunology | 2019 | 10.1038/s41590-018-0276-y |

### Annotation and Enrichment

| Tool | Citation | Journal | Year | DOI |
|------|----------|---------|------|-----|
| ChIPseeker | Yu G et al. | Bioinformatics | 2015 | 10.1093/bioinformatics/btv145 |
| GREAT | McLean CY et al. | Nature Biotechnology | 2010 | 10.1038/nbt.1630 |
| clusterProfiler | Wu T et al. | Innovation | 2021 | 10.1016/j.xinn.2021.100141 |
| GSEA | Subramanian A et al. | PNAS | 2005 | 10.1073/pnas.0506580102 |
| Enrichr | Kuleshov MV et al. | Nucleic Acids Research | 2016 | 10.1093/nar/gkw377 |
| DAVID | Huang DW et al. | Nature Protocols | 2009 | 10.1038/nprot.2008.211 |
| ChromHMM | Ernst J & Kellis M | Nature Methods | 2012 | 10.1038/nmeth.1906 |
| liftOver | Kent WJ et al. | Genome Research | 2002 | 10.1101/gr.229102 |

### Visualization

| Tool | Citation | Journal | Year | DOI |
|------|----------|---------|------|-----|
| IGV | Robinson JT et al. | Nature Biotechnology | 2011 | 10.1038/nbt.1754 |
| ggplot2 | Wickham H | Springer | 2016 | ISBN: 978-3-319-24277-4 |
| ComplexHeatmap | Gu Z et al. | Bioinformatics | 2016 | 10.1093/bioinformatics/btw313 |
| Gviz | Hahne F & Ivanek R | Methods in Molecular Biology | 2016 | 10.1007/978-1-4939-3578-9_16 |
| pyGenomeTracks | Lopez-Delisle L et al. | Bioinformatics | 2021 | 10.1093/bioinformatics/btaa692 |
| HiGlass | Kerpedjiev P et al. | Genome Biology | 2018 | 10.1186/s13059-018-1486-1 |
| UpSetR | Conway JR et al. | Bioinformatics | 2017 | 10.1093/bioinformatics/btx364 |

### Workflow Management

| Tool | Citation | Journal | Year | DOI |
|------|----------|---------|------|-----|
| Nextflow | Di Tommaso P et al. | Nature Biotechnology | 2017 | 10.1038/nbt.3820 |
| Snakemake | Molder F et al. | F1000Research | 2021 | 10.12688/f1000research.29032.2 |
| Docker | Merkel D | Linux Journal | 2014 | -- |
| Singularity | Kurtzer GM et al. | PLOS ONE | 2017 | 10.1371/journal.pone.0177459 |

## Auto-Generation from Provenance

The provenance chain logged by the `data-provenance` skill contains all information needed to auto-generate a complete methods section. The workflow is:

### Step 1: Query Provenance for a Derived File

```
encode_get_provenance(file_path="/path/to/derived/final_peaks.bed")
```

This returns the full chain: derived_file -> processing_steps -> source ENCODE files.

### Step 2: Extract Tool Names, Versions, Parameters

From each provenance record, extract:
- `tool_used` field: tool name and version
- `parameters` field: command-line arguments or function calls
- `source_accessions` field: ENCODE experiment and file accessions

### Step 3: Map to Methods Template

Match each tool to the appropriate methods template section:
- BWA-MEM / Bowtie2 / STAR -> Alignment paragraph
- MACS2 / SEACR / Hotspot2 -> Peak calling paragraph
- DESeq2 / edgeR -> Differential analysis paragraph
- bedtools / samtools -> Filtering paragraph

### Step 4: Fill in Metadata from Tracked Experiment

```
encode_get_experiment(accession="ENCSR...")
```

Populate template fields: biosample, target, lab, replicates, sequencer, read length, read count, library preparation.

### Step 5: Generate Citations for All Tools

Cross-reference every tool in the provenance chain against the Tool Citation Reference table above. Compile a complete bibliography.

### Step 6: Assemble and Review

Combine all sections into a complete methods draft:
1. Data acquisition paragraph (ENCODE sources)
2. Processing paragraphs (one per major step)
3. Analysis paragraphs (differential, enrichment, etc.)
4. Data availability statement
5. Supplementary table definitions
6. Complete tool citations

Review the draft against the documentation standards checklist to ensure no required fields are missing.

### Example: Auto-Generated from Provenance

Given a provenance chain:
```
final_peaks.bed
  <- tool: bedtools v2.31.0, params: intersect -v blacklist
  <- filtered_peaks.bed
       <- tool: awk, params: '$7 >= 4.5'
       <- ENCFF123ABC.bed (IDR thresholded peaks, ENCSR456DEF)
```

Auto-generated methods:
```text
H3K27ac ChIP-seq data for human pancreas were obtained from the ENCODE
Project (ENCODE Project Consortium 2020) under accession ENCSR456DEF.
IDR-thresholded peaks (ENCFF123ABC) aligned to GRCh38 were selected for
downstream analysis. Peaks were filtered to retain only those with MACS2
signal value >= 4.5 (retaining 34,521 of 45,231 peaks; 76.3%). Peaks
overlapping ENCODE Blacklist v2 regions (Amemiya et al. 2019) were
excluded using bedtools intersect (v2.31.0; Quinlan & Hall 2010),
yielding 34,198 peaks (99.1% of filtered set) for downstream analysis.
```

## Pitfalls

### Critical Omissions That Reviewers Will Flag

1. **Not reporting software versions**: "Reads were aligned with STAR" is unacceptable. Reviewers require "STAR v2.7.11a (Dobin et al. 2013)." Every tool needs name, version, and citation.

2. **Missing biological replicate counts**: "ChIP-seq was performed" does not tell readers whether results are from 1 replicate or 5. Always state: "n=[N] biological replicates per condition."

3. **Confusing technical vs biological replicates**: Technical replicates (same sample, sequenced twice) are NOT biological replicates (independent biological samples). Reporting "4 replicates" when 2 are technical inflates apparent statistical power.

4. **Not specifying genome assembly version**: "Reads were aligned to the human genome" is ambiguous. hg19, hg38, GRCh37, GRCh38, T2T-CHM13 are all different. Always specify: "GRCh38/hg38."

5. **Using "default parameters" without stating what those defaults are**: "MACS2 was run with default parameters" is not reproducible because defaults change between versions. State the actual parameter values.

6. **Missing blacklist filtering mention**: Peaks or signal tracks without blacklist filtering contain artifact regions. Always report: "ENCODE Blacklist v2 regions (Amemiya et al. 2019) were excluded."

7. **Not reporting IDR threshold for ChIP-seq**: IDR analysis is standard for ENCODE ChIP-seq. Report: "IDR threshold of 0.05" or whichever threshold was used.

8. **Omitting spike-in normalization details for CUT&RUN**: CUT&RUN relies on spike-in normalization. Report the spike-in organism, calibration method, and scaling factor.

9. **Not distinguishing paired-end from single-end in methods**: PE and SE reads produce different fragment size estimates, alignment rates, and duplicate detection. Always specify.

10. **Omitting gene annotation version**: GENCODE v38 and v44 define different gene sets. "Genes were annotated using GENCODE" is insufficient -- state the exact version.

11. **Not reporting filtering statistics**: Every filtering step should report input count, output count, and percentage retained. "Peaks were filtered" without numbers is uninformative.

12. **Missing normalization method**: "Signal tracks were compared across samples" -- how? Library-size normalization? Spike-in? RPKM? RPM? This changes interpretation.

## Literature Foundation

| Reference | Year | Journal | Key Contribution | Citations |
|-----------|------|---------|-----------------|-----------|
| Landt et al. | 2012 | Genome Research | ChIP-seq reporting guidelines and quality standards; established FRiP, NSC, RSC thresholds | ~3,400 |
| ENCODE Consortium | 2020 | Nature | ENCODE Phase 3 expanded encyclopaedias; defined current data standards and uniform pipelines | ~1,200 |
| Conesa et al. | 2016 | Genome Biology | RNA-seq best practices survey; defined mapping rate, rRNA, and correlation thresholds | ~4,500 |
| Wilkinson et al. | 2016 | Scientific Data | FAIR data principles (Findable, Accessible, Interoperable, Reusable); framework for data sharing | ~8,000 |
| Sandve et al. | 2013 | PLOS Computational Biology | Ten simple rules for reproducible computational research; foundational reproducibility guide | ~1,800 |
| Baker | 2016 | Nature | 1,500 scientists lift the lid on reproducibility; established scale of reproducibility crisis | ~3,200 |
| Amemiya et al. | 2019 | Scientific Reports | ENCODE Blacklist: identification and exclusion of artifact regions across genome assemblies | ~1,372 |
| Buenrostro et al. | 2013 | Nature Methods | ATAC-seq method development; defined TSS enrichment and nucleosomal fragment thresholds | ~5,000 |
| Foox et al. | 2021 | Genome Biology | WGBS benchmarking and quality standards; bisulfite conversion thresholds | ~200 |
| Yardimci et al. | 2019 | Genome Biology | Hi-C quality metrics; cis/trans ratio and long-range cis thresholds | ~150 |
| Nordin et al. | 2023 | Genome Biology | CUT&RUN/CUT&Tag QC: different profiles from ChIP-seq; suspect list regions | ~50 |

## Integration

| This skill produces... | Feed into... | Using tool/skill |
|---|---|---|
| Methods section text | Manuscript draft | Publication submission |
| Figure legends | Manuscript figures | visualization-workflow outputs |
| Data availability statements | Manuscript appendix | cite-encode accession lists |
| Supplementary table templates | Manuscript supplements | track-experiments → encode_export_data |
| Tool citation paragraphs | Bibliography | cite-encode → BibTeX/RIS export |

## Walkthrough: Generating Publication-Ready Methods for an ENCODE Analysis

**Goal**: Auto-generate a publication-ready methods section describing ENCODE data acquisition, processing, and analysis, with complete tool citations and reproducible parameters.
**Context**: Journal methods sections require precise documentation of every tool, version, parameter, and data source. This skill automates that process using tracked provenance data.

### Step 1: Review tracked experiments

```
encode_list_tracked()
```

Expected output:
```json
{
  "experiments": [
    {"accession": "ENCSR000AKA", "assay": "Histone ChIP-seq", "notes": "GM12878 H3K27ac"},
    {"accession": "ENCSR637ENO", "assay": "ATAC-seq", "notes": "GM12878 accessibility"}
  ]
}
```

### Step 2: Get provenance for derived files

```
encode_get_provenance(file_path="/data/analysis/enhancers_filtered.bed")
```

Expected output:
```json
{
  "file": "/data/analysis/enhancers_filtered.bed",
  "tool": "bedtools v2.31.0",
  "sources": [{"accession": "ENCFF001ABC"}],
  "description": "Blacklist-filtered H3K27ac peaks"
}
```

### Step 3: Get collection summary

```
encode_summarize_collection()
```

### Step 4: Draft methods paragraph

Using provenance data, generate:
"H3K27ac ChIP-seq data for GM12878 (ENCSR000AKA) were obtained from the ENCODE Portal (ENCODE Project Consortium, 2012). IDR-thresholded peaks (ENCFF001ABC) were filtered against the ENCODE blacklist v2 (Amemiya et al., 2019) using bedtools v2.31.0 (Quinlan & Hall, 2010)."

### Integration with downstream skills
- Provenance data from → **data-provenance** provides tool versions and parameters
- Citations from → **cite-encode** provide proper references
- QC metrics from → **quality-assessment** document quality thresholds used
- Pipeline details from → **pipeline-guide** describe processing workflows

## Code Examples

### 1. List tracked experiments for methods
```
encode_list_tracked()
```

Expected output:
```json
{
  "experiments": [
    {"accession": "ENCSR000AKA", "assay": "Histone ChIP-seq"}
  ]
}
```

### 2. Get provenance for a derived file
```
encode_get_provenance(file_path="/data/peaks_filtered.bed")
```

Expected output:
```json
{
  "file": "/data/peaks_filtered.bed",
  "tool": "bedtools v2.31.0",
  "sources": [{"accession": "ENCFF001ABC"}]
}
```

### 3. Get experiment citations for bibliography
```
encode_get_citations(accession="ENCSR000AKA")
```

Expected output:
```json
{
  "citations": [{"pmid": "29126249", "title": "ENCODE encyclopedia", "year": 2012}]
}
```

## Related Skills

| Skill | Relationship |
|---|---|
| data-provenance | Source of provenance records for methods auto-generation; log every operation |
| cite-encode | Citation formatting and ENCODE data use policy compliance |
| quality-assessment | QC metrics to include in methods sections and Table S2 |
| pipeline-guide | Pipeline parameters for methods text; links to assay-specific pipeline skills |
| publication-trust | Verify integrity of cited publications before including in references |
| pipeline-chipseq | ChIP-seq pipeline parameters for methods template |
| pipeline-atacseq | ATAC-seq pipeline parameters for methods template |
| pipeline-rnaseq | RNA-seq pipeline parameters for methods template |
| pipeline-wgbs | WGBS pipeline parameters for methods template |
| pipeline-hic | Hi-C pipeline parameters for methods template |
| pipeline-cutandrun | CUT&RUN pipeline parameters for methods template |
| visualization-workflow | Figure generation workflow to pair with figure legends |
| peak-annotation | Peak annotation details for methods and figure legends |
| batch-analysis | Multi-experiment analyses requiring comprehensive methods |

## Presenting Results

When generating scientific writing, present:

1. **Complete methods paragraph(s)** in a code block for easy copy-paste. Every paragraph should be self-contained and ready for insertion into a manuscript.

2. **Documentation standards checklist** showing which required metadata fields are covered vs. missing:
   ```
   [x] Library preparation: TruSeq ChIP
   [x] Biological replicates: n=2
   [x] Sequencing reads: 42.3M PE
   [ ] Cells/nuclei per replicate: NOT FOUND -- check experiment metadata
   [x] Read length: 76 bp
   ...
   ```

3. **Citation list** of all tools referenced in the methods, formatted for the target reference manager (BibTeX, RIS, or inline text).

4. **Supplementary table structure** with column headers and example rows, ready to populate.

5. **Data availability statement** draft customized to the specific ENCODE accessions used.

6. **Missing information flags**: If any required documentation fields cannot be populated from available metadata, flag them explicitly with suggestions for how to obtain them (e.g., "Cells per replicate not available in ENCODE metadata -- check the associated publication or contact the submitting lab").

## For the request: "$ARGUMENTS"
