---
name: pipeline-dnaseseq
description: "Execute ENCODE DNase-seq pipeline from FASTQ to hotspots and footprints. Child of pipeline-guide. Provides Nextflow execution with Docker and cloud deployment. Use when processing DNase-seq data, calling DNase hypersensitive sites, performing footprinting analysis. Trigger on: DNase-seq pipeline, DNase hypersensitive, DHS, Hotspot2, footprinting, DNase I, chromatin accessibility DNase."
---

# ENCODE DNase-seq Pipeline: FASTQ to Hotspots and Footprints

## When to Use

- User wants to run a DNase-seq processing pipeline from FASTQ to hotspots and footprints
- User asks about "DNase-seq pipeline", "DNase hypersensitive sites", "Hotspot2", "footprinting", or "DHS"
- User needs to process DNase-seq data for chromatin accessibility and TF footprint analysis
- Example queries: "process my DNase-seq FASTQs", "call DNase hypersensitive sites", "run footprinting analysis on DNase-seq"

Execute the ENCODE DNase-seq pipeline for chromatin accessibility profiling,
producing DNase hypersensitive sites (DHSs) via Hotspot2 and transcription
factor footprints.

## Pipeline Overview

```
FASTQ -> Trim -> BWA-MEM align -> Filter/dedup -> Hotspot2 -> DHS peaks
                                       |                        |
                                    Signal track         Footprinting (HINT)
```

### ENCODE Repository

- **GitHub**: `ENCODE-DCC/dnase-seq-pipeline`
- **Container**: `encodedcc/dnase-seq-pipeline`
- **WDL**: Available for Cromwell execution
- **This skill**: Nextflow DSL2 reimplementation for portability

## Core Tools and Versions

| Tool | Version | Purpose | Citation |
|------|---------|---------|----------|
| BWA-MEM | 0.7.17 | Alignment | Li & Durbin 2009 |
| samtools | 1.19 | BAM operations | Li et al. 2009 |
| Picard | 3.1.1 | Duplicate marking | Broad Institute |
| Hotspot2 | 2.3.1 | DHS calling (ENCODE standard) | John et al. 2011 |
| bedtools | 2.31.0 | Genomic arithmetic | Quinlan & Hall 2010 |
| HINT-ATAC | 0.13.2 | TF footprinting | Li et al. 2019 |
| FastQC | 0.12.1 | Read quality | Andrews (Babraham) |
| MultiQC | 1.21 | Aggregated QC | Ewels et al. 2016 |

## Key Literature

1. **John et al. 2011** - "Chromatin accessibility pre-determines glucocorticoid
   receptor binding patterns" (Nature Genetics, ~600 citations)
   DOI: 10.1038/ng.759

2. **Thurman et al. 2012** - "The accessible chromatin landscape of the human
   genome" (Nature, ~3,000 citations)
   DOI: 10.1038/nature11232

3. **Vierstra et al. 2020** - "Global reference mapping of human transcription
   factor footprints" (Nature, ~600 citations)
   DOI: 10.1038/s41586-020-2528-x

4. **Amemiya et al. 2019** - "The ENCODE Blacklist" (Scientific Reports, ~1,372 citations)
   DOI: 10.1038/s41598-019-45839-z

5. **Li et al. 2019** - "Identification of transcription factor binding sites using
   ATAC-seq" (Genome Biology) -- HINT-ATAC footprinting
   DOI: 10.1186/s13059-019-1642-2

## Execution

### Quick Start (Local)

```bash
nextflow run main.nf \
    -profile local \
    --reads '/data/fastq/*_R{1,2}.fastq.gz' \
    --bwa_index '/ref/bwa_index/genome.fa' \
    --chrom_sizes '/ref/hg38.chrom.sizes' \
    --hotspot_index '/ref/hotspot2_index/' \
    --blacklist '/ref/hg38-blacklist.v2.bed' \
    --outdir results/ \
    -resume
```

### SLURM HPC

```bash
nextflow run main.nf \
    -profile slurm \
    --reads '/data/fastq/*_R{1,2}.fastq.gz' \
    --bwa_index '/ref/bwa_index/genome.fa' \
    --chrom_sizes '/ref/hg38.chrom.sizes' \
    --hotspot_index '/ref/hotspot2_index/' \
    --blacklist '/ref/hg38-blacklist.v2.bed' \
    --outdir results/ \
    -resume
```

### Cloud (GCP / AWS)

```bash
nextflow run main.nf \
    -profile gcp \
    --reads 'gs://bucket/fastq/*_R{1,2}.fastq.gz' \
    --bwa_index 'gs://bucket/ref/genome.fa' \
    --chrom_sizes 'gs://bucket/ref/hg38.chrom.sizes' \
    --hotspot_index 'gs://bucket/ref/hotspot2_index/' \
    --blacklist 'gs://bucket/ref/hg38-blacklist.v2.bed' \
    --outdir 'gs://bucket/results/' \
    -resume
```

## Resource Requirements

| Step | CPUs | RAM | Time (per sample) |
|------|------|-----|-------------------|
| BWA-MEM align | 8 | 16 GB | 1-2 hours |
| Filter/dedup | 4 | 8 GB | 30-60 min |
| Hotspot2 | 4 | 8 GB | 30-60 min |
| Signal generation | 2 | 4 GB | 15-30 min |
| Footprinting | 4 | 8 GB | 1-2 hours |
| **Total** | **8** | **16 GB** | **3-6 hours** |

## Pipeline Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--reads` | required | Glob pattern to paired FASTQ files |
| `--bwa_index` | required | Path to BWA genome index (.fa) |
| `--chrom_sizes` | required | Chromosome sizes file |
| `--hotspot_index` | required | Hotspot2 mappability index directory |
| `--blacklist` | required | ENCODE blacklist BED file |
| `--outdir` | `./results` | Output directory |
| `--fdr` | `0.05` | Hotspot2 FDR threshold |
| `--skip_footprint` | `false` | Skip footprinting analysis |
| `--motif_db` | `null` | JASPAR motif database for footprinting |

## Output Files

```
results/
  fastqc/                          # Raw read quality
  alignment/
    {sample}.filtered.bam          # Filtered, deduplicated BAM
    {sample}.filtered.bam.bai
  hotspots/
    {sample}.hotspots.fdr0.05.bed  # DHS peaks (primary output)
    {sample}.peaks.narrowPeak      # narrowPeak format
    {sample}.density.bw            # Signal track (bigWig)
    {sample}.allcalls.bed          # All hotspot calls (unfiltered)
    {sample}.SPOT.txt              # SPOT score
  footprints/
    {sample}.footprints.bed        # TF footprints
    {sample}.footprint_scores.txt  # Per-motif footprint scores
  qc/
    {sample}.flagstat.txt
    {sample}.insert_sizes.txt
  multiqc/
    multiqc_report.html
```

## QC Thresholds (ENCODE Standards)

| Metric | Pass | Warning | Fail |
|--------|------|---------|------|
| SPOT score (Signal Portion of Tags) | >0.4 | 0.2-0.4 | <0.2 |
| Hotspot count | >50,000 | 20,000-50,000 | <20,000 |
| Mapping rate | >80% | 60-80% | <60% |
| Duplication rate | <30% | 30-50% | >50% |
| NRF (Non-Redundant Fraction) | >0.8 | 0.7-0.8 | <0.7 |
| PBC1 (PCR Bottleneck Coefficient 1) | >0.9 | 0.7-0.9 | <0.7 |
| Insert size peak | 50-150 bp | Variable | Abnormal |

### SPOT Score

The SPOT score (Signal Portion of Tags) is the fraction of reads falling
within hotspots. It is the DNase-seq equivalent of FRiP for ChIP-seq.

Higher SPOT = more enrichment in accessible regions = better library quality.

## Hotspot2 vs MACS2

**IMPORTANT**: ENCODE uses Hotspot2 for DNase-seq, NOT MACS2.

| Feature | Hotspot2 | MACS2 |
|---------|----------|-------|
| Designed for | DNase-seq | ChIP-seq |
| Background model | Local tag density + mappability | Dynamic Poisson |
| ENCODE standard | Yes (DNase-seq) | Yes (ChIP-seq/ATAC-seq) |
| Mappability correction | Built-in | Not available |
| Output | Hotspots + peaks | Peaks only |

Hotspot2 accounts for mappability variation across the genome, which is
critical for DNase-seq because DNase I cuts accessible chromatin regardless
of whether it is uniquely mappable.

## Critical Pitfalls

### DNase-seq vs ATAC-seq
These are different assays measuring the same biology (chromatin accessibility):
- **DNase-seq**: Uses DNase I enzyme, requires more input material
- **ATAC-seq**: Uses Tn5 transposase, works on fewer cells
- Analysis pipelines differ: Hotspot2 for DNase-seq, MACS2 for ATAC-seq
- Data are largely concordant but not identical

### Fragment Size Distribution
DNase-seq produces a characteristic fragment size distribution:
- Peak at ~50-100 bp (sub-nucleosomal fragments at DHS)
- Secondary peak at ~150-200 bp (mononucleosomal fragments)
- Long tail of larger fragments
- If distribution is abnormal, check library preparation protocol

### Mappability Index
Hotspot2 requires a pre-computed mappability index. These are read-length
and genome-build specific:
- hg38 / 36 bp: Use ENCODE-provided index
- hg38 / 76 bp: Use ENCODE-provided index
- hg38 / 150 bp: May need to generate custom index
- Wrong mappability index = incorrect peak calls

### Blacklist Filtering
Always filter peaks against the ENCODE blacklist (Amemiya et al. 2019):
```bash
bedtools intersect -a hotspots.bed -b hg38-blacklist.v2.bed -v > hotspots_filtered.bed
```

Blacklist regions produce artifactual signal in accessibility assays.

## Footprinting Analysis

Transcription factor footprinting detects bound TFs from DNase-seq signal:

### HINT-ATAC Footprinting
```bash
rgt-hint footprinting \
    --atac-seq \
    --paired-end \
    --organism hg38 \
    --output-location footprints/ \
    sample.filtered.bam \
    hotspots.narrowPeak
```

### Interpretation
- Footprints are depressions in the DNase signal where a bound TF protects DNA
- Requires deep sequencing (>100M reads) for reliable footprints
- Sensitivity varies by TF: pioneer factors have shallow footprints
- Vierstra et al. 2020 provides a global reference map for comparison

## Provenance Integration

After pipeline completion, log all outputs:

```python
encode_log_derived_file(
    file_path="/results/hotspots/sample1.hotspots.fdr0.05.bed",
    source_accessions=["ENCSR...", "ENCFF..."],
    description="DNase hypersensitive sites from ENCODE DNase-seq pipeline",
    file_type="DHS_peaks",
    tool_used="BWA 0.7.17 + Hotspot2 2.3.1",
    parameters="FDR 0.05, blacklist filtered, ENCODE hg38 mappability index"
)
```

## Reference Files

Detailed step-by-step documentation is provided in the `references/` directory:

1. `01-qc-trimming.md` -- Read QC and adapter trimming
2. `02-alignment.md` -- BWA-MEM alignment for DNase-seq
3. `03-filtering.md` -- BAM filtering, deduplication, blacklist removal
4. `04-hotspot-calling.md` -- Hotspot2 DHS detection and signal generation
5. `05-footprinting.md` -- TF footprint detection with HINT-ATAC

## Walkthrough: Processing ENCODE DNase-seq from FASTQ to Hypersensitive Sites

**Goal**: Process raw DNase-seq FASTQ files through the ENCODE pipeline to generate DNase I hypersensitive site (DHS) peak calls.
**Context**: DNase-seq identifies open chromatin via DNase I enzyme digestion. The pipeline uses BWA alignment and Hotspot2 for DHS identification.

### Step 1: Find DNase-seq experiment

```
encode_search_experiments(assay_title="DNase-seq", biosample_term_name="K562", organism="Homo sapiens")
```

Expected output:
```json
{
  "total": 8,
  "results": [
    {"accession": "ENCSR000DNS", "assay_title": "DNase-seq", "biosample_summary": "K562", "status": "released"}
  ]
}
```

### Step 2: List and download FASTQ files

```
encode_list_files(accession="ENCSR000DNS", file_format="fastq")
```

### Step 3: Run the DNase-seq pipeline

```bash
nextflow run pipeline-dnaseseq/main.nf \
  --fastq_r1 ENCFF700DN1.fastq.gz \
  --genome GRCh38 \
  --blacklist encode_blacklist_v2.bed \
  -profile docker
```

Key pipeline steps:
1. Quality trimming
2. BWA-MEM alignment
3. Duplicate removal
4. Hotspot2 DHS calling
5. Signal track generation
6. Footprint analysis (HINT-ATAC)

### Step 4: Validate output quality

| Metric | Threshold | Purpose |
|---|---|---|
| SPOT score | > 0.4 | Signal portion of tags |
| Hotspot count | > 100,000 | Sensitivity |
| Duplicate rate | < 30% | Library complexity |

### Step 5: Compare with ATAC-seq

```
encode_search_experiments(assay_title="ATAC-seq", biosample_term_name="K562", organism="Homo sapiens")
```

**Interpretation**: DNase-seq and ATAC-seq both measure accessibility but with different biases. Compare peaks from both assays -- concordant peaks are high confidence.

### Integration with downstream skills
- DHS peaks feed into -> **accessibility-aggregation** alongside ATAC-seq peaks
- Footprint data feeds into -> **motif-analysis** for TF binding prediction
- Signal tracks feed into -> **visualization-workflow**
- Peaks integrate with -> **regulatory-elements** for cCRE classification

## Code Examples

### 1. Survey DNase-seq availability

```
encode_get_facets(assay_title="DNase-seq", facet_field="organ", organism="Homo sapiens")
```

Expected output:
```json
{
  "facets": {
    "organ": {"blood": 45, "brain": 30, "liver": 20, "heart": 15, "lung": 12}
  }
}
```

### 2. Check for existing DHS peaks

```
encode_list_files(accession="ENCSR000DNS", file_format="bed", output_type="peaks", assembly="GRCh38")
```

Expected output:
```json
{
  "files": [
    {"accession": "ENCFF800DHS", "output_type": "peaks", "file_format": "bed narrowPeak", "file_size_mb": 1.5}
  ]
}
```

### 3. Track DNase-seq experiments

```
encode_track_experiment(accession="ENCSR000DNS", notes="K562 DNase-seq for accessibility comparison with ATAC-seq")
```

Expected output:
```json
{
  "status": "tracked",
  "accession": "ENCSR000DNS",
  "notes": "K562 DNase-seq for accessibility comparison with ATAC-seq"
}
```

## Integration

| This skill produces... | Feed into... | Purpose |
|---|---|---|
| DHS peaks (narrowPeak) | **accessibility-aggregation** | Union merge with ATAC-seq peaks |
| TF footprints | **motif-analysis** | Validate motif predictions with footprint evidence |
| Signal tracks (bigWig) | **visualization-workflow** | Genome browser display |
| Accessible regions | **regulatory-elements** | cCRE classification |
| DHS coordinates | **variant-annotation** | Annotate variants in hypersensitive sites |
| QC metrics | **quality-assessment** | Validate SPOT score and sensitivity |
| Pipeline parameters | **data-provenance** | Record BWA/Hotspot2 versions |
| DHS peak regions | **jaspar-motifs** | Scan accessible sites for known TF motifs |

## Related Skills

- `pipeline-guide` -- Parent skill with compute resource assessment and cloud setup
- `accessibility-aggregation` -- Aggregate DHS data across samples/tissues
- `quality-assessment` -- Evaluate pipeline output quality metrics
- `data-provenance` -- Track all pipeline inputs, outputs, and parameters
- `download-encode` -- Download ENCODE DNase-seq FASTQ files for pipeline input
- `publication-trust` -- Verify literature claims backing analytical decisions

## Presenting Results

When reporting DNase-seq pipeline results:

- **Hotspot counts**: Report total Hotspot2 DHS calls at the specified FDR threshold and the number remaining after blacklist filtering
- **Signal-to-noise (SPOT score)**: Report the SPOT score prominently (>0.4 pass, 0.2-0.4 warning, <0.2 fail). This is the DNase-seq equivalent of FRiP
- **Footprint depth**: If footprinting was performed, report the number of TF footprints detected and note the sequencing depth (>100M reads recommended for reliable footprints)
- **FRiP equivalent**: Report the fraction of reads in hotspots as a complementary enrichment metric
- **Key QC metrics**: Present mapping rate (>80%), duplication rate (<30%), NRF (>0.8), PBC1 (>0.9), and insert size peak in a summary table
- **Output paths**: Provide paths to hotspot BED files, narrowPeak files, signal bigWig tracks, and footprint results
- **Mappability note**: Confirm which Hotspot2 mappability index was used and that it matches the read length
- **Next steps**: Suggest `motif-analysis` for TF motif enrichment in DHS peaks, or `accessibility-aggregation` for merging DHS data across samples

## For the request: "$ARGUMENTS"
