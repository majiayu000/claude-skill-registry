---
name: pipeline-cutandrun
description: "Execute CUT&RUN processing pipeline from FASTQ to peaks and signal tracks. Child of pipeline-guide. Provides Nextflow execution with Docker and cloud deployment. Use when processing CUT&RUN or CUT&Tag data, an alternative to ChIP-seq with lower background. Trigger on: CUT&RUN pipeline, CUT&Tag, SEACR, Henikoff, targeted chromatin, pA-MNase, process CUT&RUN."
---

# ENCODE CUT&RUN Pipeline: FASTQ to Peaks and Signal Tracks

## When to Use

- User wants to run a CUT&RUN or CUT&Tag processing pipeline from FASTQ to peaks
- User asks about "CUT&RUN pipeline", "CUT&Tag", "SEACR", "spike-in normalization", or "targeted chromatin"
- User needs to process CUT&RUN/CUT&Tag data with spike-in calibration and SEACR peak calling
- Example queries: "process my CUT&RUN FASTQs", "run SEACR on CUT&Tag data", "normalize CUT&RUN with spike-in controls"

Execute the CUT&RUN/CUT&Tag processing pipeline for targeted chromatin profiling,
producing peak calls with SEACR and spike-in normalized signal tracks.

## Pipeline Overview

```
FASTQ -> Trim -> Bowtie2 align (genome) -> Filter/dedup -> SEACR peaks
                     |                          |              |
              Bowtie2 align (spike-in)   Spike-in normalize  Signal tracks
                     |
              Scale factor calculation
```

### ENCODE Repository

- **GitHub**: `ENCODE-DCC/cutandrun-pipeline`
- **Container**: `encodedcc/cutandrun-pipeline`
- **This skill**: Nextflow DSL2 reimplementation for portability

## Core Tools and Versions

| Tool | Version | Purpose | Citation |
|------|---------|---------|----------|
| Bowtie2 | 2.5.3 | Alignment (genome + spike-in) | Langmead & Salzberg 2012 |
| SEACR | 1.3 | Peak calling (CUT&RUN-specific) | Meers et al. 2019 |
| MACS2 | 2.2.9.1 | Alternative peak caller | Zhang et al. 2008 |
| Picard | 3.1.1 | Duplicate marking | Broad Institute |
| samtools | 1.19 | BAM operations | Li et al. 2009 |
| bedtools | 2.31.0 | Genomic arithmetic | Quinlan & Hall 2010 |
| deepTools | 3.5.4 | Signal track generation | Ramirez et al. 2016 |
| FastQC | 0.12.1 | Read quality | Andrews (Babraham) |
| MultiQC | 1.21 | Aggregated QC | Ewels et al. 2016 |

## Key Literature

1. **Skene & Henikoff 2017** - "An efficient targeted nuclease strategy for
   high-resolution mapping of DNA binding sites" (eLife, ~1,500 citations)
   DOI: 10.7554/eLife.21856

2. **Meers et al. 2019** - "Peak calling by Sparse Enrichment Analysis for
   CUT&RUN chromatin profiling" (Epigenetics & Chromatin, ~800 citations)
   DOI: 10.1186/s13072-019-0287-4

3. **Kaya-Okur et al. 2019** - "CUT&Tag for efficient epigenomic profiling
   of small samples and single cells" (Nature Communications, ~1,200 citations)
   DOI: 10.1038/s41467-019-09982-5

4. **Nordin et al. 2023** - "The CUT&RUN suspect list of problematic regions"
   (Genome Biology)
   DOI: 10.1186/s13059-023-02960-3

5. **Amemiya et al. 2019** - "The ENCODE Blacklist" (Scientific Reports, ~1,372 citations)
   DOI: 10.1038/s41598-019-45839-z

## Execution

### Quick Start (Local)

```bash
nextflow run main.nf \
    -profile local \
    --reads '/data/fastq/*_R{1,2}.fastq.gz' \
    --bowtie2_index '/ref/bowtie2_index/genome' \
    --spikein_index '/ref/bowtie2_ecoli/ecoli' \
    --chrom_sizes '/ref/hg38.chrom.sizes' \
    --blacklist '/ref/hg38-blacklist.v2.bed' \
    --outdir results/ \
    -resume
```

### SLURM HPC

```bash
nextflow run main.nf \
    -profile slurm \
    --reads '/data/fastq/*_R{1,2}.fastq.gz' \
    --bowtie2_index '/ref/bowtie2_index/genome' \
    --spikein_index '/ref/bowtie2_ecoli/ecoli' \
    --chrom_sizes '/ref/hg38.chrom.sizes' \
    --blacklist '/ref/hg38-blacklist.v2.bed' \
    --outdir results/ \
    -resume
```

### Cloud (GCP / AWS)

```bash
nextflow run main.nf \
    -profile gcp \
    --reads 'gs://bucket/fastq/*_R{1,2}.fastq.gz' \
    --bowtie2_index 'gs://bucket/ref/bowtie2_index/genome' \
    --spikein_index 'gs://bucket/ref/bowtie2_ecoli/ecoli' \
    --chrom_sizes 'gs://bucket/ref/hg38.chrom.sizes' \
    --blacklist 'gs://bucket/ref/hg38-blacklist.v2.bed' \
    --outdir 'gs://bucket/results/' \
    -resume
```

## Resource Requirements

| Step | CPUs | RAM | Time (per sample) |
|------|------|-----|-------------------|
| Bowtie2 align (genome) | 8 | 8 GB | 30-60 min |
| Bowtie2 align (spike-in) | 4 | 4 GB | 10-20 min |
| Filter/dedup | 4 | 8 GB | 15-30 min |
| SEACR peaks | 2 | 4 GB | 10-20 min |
| Signal tracks | 4 | 8 GB | 15-30 min |
| **Total** | **8** | **8 GB** | **1.5-3 hours** |

## Pipeline Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--reads` | required | Glob pattern to paired FASTQ files |
| `--bowtie2_index` | required | Bowtie2 genome index prefix |
| `--spikein_index` | required | Bowtie2 E. coli spike-in index prefix |
| `--chrom_sizes` | required | Chromosome sizes file |
| `--blacklist` | required | ENCODE blacklist BED file |
| `--outdir` | `./results` | Output directory |
| `--seacr_mode` | `stringent` | SEACR mode: `stringent` or `relaxed` |
| `--seacr_norm` | `norm` | SEACR normalization: `norm` or `non` |
| `--control` | `null` | IgG control BAM (if available) |
| `--peak_caller` | `seacr` | Peak caller: `seacr` or `macs2` or `both` |
| `--skip_spikein` | `false` | Skip spike-in normalization |

## Output Files

```
results/
  fastqc/                           # Raw read quality
  alignment/
    {sample}.filtered.bam           # Filtered, deduplicated BAM
    {sample}.filtered.bam.bai
  spikein/
    {sample}.spikein_counts.txt     # Spike-in read counts
    {sample}.scale_factor.txt       # Computed scale factor
  peaks/
    {sample}.seacr.stringent.bed    # SEACR stringent peaks
    {sample}.seacr.relaxed.bed      # SEACR relaxed peaks
    {sample}.macs2_peaks.narrowPeak # MACS2 peaks (if requested)
  signal/
    {sample}.normalized.bw          # Spike-in normalized signal
    {sample}.fragments.bed          # Fragment BED file
  qc/
    {sample}.flagstat.txt
    {sample}.fragment_sizes.txt
    {sample}.frip.txt
  multiqc/
    multiqc_report.html
```

## QC Thresholds

| Metric | Pass | Warning | Fail |
|--------|------|---------|------|
| Mapping rate (genome) | >80% | 60-80% | <60% |
| Spike-in reads | 1-10% of total | 0.1-1% or 10-30% | <0.1% or >30% |
| Duplication rate | <20% | 20-40% | >40% |
| FRiP (peaks) | >10% | 5-10% | <5% |
| Peak count | >5,000 | 1,000-5,000 | <1,000 |
| Fragment size | Nucleosomal pattern | Irregular | No pattern |

### Fragment Size Distribution

CUT&RUN produces a characteristic nucleosomal ladder:
- **<120 bp**: Sub-nucleosomal (TF binding)
- **~150 bp**: Mononucleosomal (histone marks)
- **~300 bp**: Dinucleosomal
- Absence of nucleosomal pattern suggests protocol issues

## Spike-in Normalization

Spike-in normalization is CRITICAL for CUT&RUN quantitative comparison.

### How It Works

1. E. coli DNA is carried over from pA-MNase/pA-Tn5 production
2. Each sample has a different amount of spike-in reads
3. Samples with more target cleavage have fewer spike-in reads (proportionally)
4. Scale factor = 1 / (spike-in reads / minimum spike-in reads across samples)

### Scale Factor Calculation

```
Sample A: 200,000 spike-in reads -> scale = 1.0 (minimum)
Sample B: 400,000 spike-in reads -> scale = 0.5
Sample C: 100,000 spike-in reads -> scale = 2.0
```

Higher spike-in counts = less target enrichment = lower scale factor.

## SEACR vs MACS2

| Feature | SEACR | MACS2 |
|---------|-------|-------|
| Designed for | CUT&RUN/CUT&Tag | ChIP-seq |
| Background model | Sparse enrichment | Dynamic Poisson |
| Control required | Optional (IgG) | Recommended |
| Low background | Handles well | May overcall |
| Stringent mode | Very conservative | Via q-value |
| ENCODE recommendation | Primary for CUT&RUN | Alternative |

SEACR is specifically designed for the sparse, low-background signal
profile of CUT&RUN data. MACS2 may overcall peaks due to the low background.

## Critical Pitfalls

### Spike-in Calibration is CRITICAL
Without spike-in normalization, quantitative comparisons between samples are
unreliable. The amount of pA-MNase (or pA-Tn5) varies between experiments,
and spike-in reads provide the internal calibration standard.

### IgG Control vs No-Antibody Control
- **IgG control**: Non-specific antibody, captures background binding
- **No-antibody**: No antibody, captures MNase accessibility background
- IgG is preferred but not always available
- SEACR can work without control (uses top 1% of signal as threshold)

### SEACR Stringent vs Relaxed Mode
- **Stringent**: Returns only the most enriched peaks (fewer, higher confidence)
- **Relaxed**: Returns a broader set including weaker peaks
- For initial analysis, use stringent mode
- For comprehensive catalogs, use relaxed mode with downstream filtering

### CUT&RUN Suspect List (Nordin 2023)
In addition to the ENCODE blacklist, filter CUT&RUN peaks against the
suspect list (Nordin et al. 2023), which identifies regions with
artifactual signal specific to CUT&RUN/CUT&Tag protocols:

```bash
# Download suspect list
wget https://github.com/Boyle-Lab/Blacklist/raw/master/lists/CUTandRUN.suspectlist.hg38.bed.gz

# Filter peaks
bedtools intersect \
    -a peaks.bed \
    -b hg38-blacklist.v2.bed CUTandRUN.suspectlist.hg38.bed \
    -v \
    > peaks_filtered.bed
```

### CUT&RUN vs CUT&Tag
Both protocols are supported by this pipeline. Differences:
- **CUT&RUN**: Uses pA-MNase, E. coli spike-in from MNase production
- **CUT&Tag**: Uses pA-Tn5, E. coli spike-in from Tn5 production
- CUT&Tag has higher background from Tn5 insertion preference
- CUT&Tag may work better for histone marks; CUT&RUN for TFs

## Provenance Integration

After pipeline completion, log all outputs:

```python
encode_log_derived_file(
    file_path="/results/peaks/sample1.seacr.stringent.bed",
    source_accessions=["ENCSR...", "ENCFF..."],
    description="CUT&RUN peaks from ENCODE CUT&RUN pipeline",
    file_type="CUT&RUN_peaks",
    tool_used="Bowtie2 2.5.3 + SEACR 1.3",
    parameters="stringent mode, spike-in normalized, blacklist + suspect list filtered"
)
```

## Reference Files

Detailed step-by-step documentation is provided in the `references/` directory:

1. `01-qc-trimming.md` -- Read QC and adapter trimming for CUT&RUN
2. `02-bowtie2-alignment.md` -- Bowtie2 alignment to genome and spike-in
3. `03-filtering-spikein.md` -- Filtering, dedup, and spike-in normalization
4. `04-seacr-peaks.md` -- SEACR peak calling and MACS2 alternative
5. `05-qc-metrics.md` -- Fragment sizes, FRiP, spike-in QC

## Walkthrough: Processing ENCODE CUT&RUN from FASTQ to Peaks

**Goal**: Process CUT&RUN/CUT&Tag FASTQ files through the ENCODE-compatible pipeline to generate peak calls with spike-in normalization.
**Context**: CUT&RUN uses targeted MNase digestion (lower background than ChIP-seq) but requires different peak calling (SEACR instead of MACS2) and spike-in normalization for quantitative comparisons.

### Step 1: Find CUT&RUN experiment

```
encode_search_experiments(assay_title="CUT&RUN", organism="Homo sapiens")
```

Expected output:
```json
{
  "total": 35,
  "results": [
    {"accession": "ENCSR900CUR", "assay_title": "CUT&RUN", "target": "H3K27me3", "biosample_summary": "K562", "status": "released"}
  ]
}
```

### Step 2: List FASTQ files

```
encode_list_files(accession="ENCSR900CUR", file_format="fastq")
```

Expected output:
```json
{
  "files": [
    {"accession": "ENCFF900CR1", "output_type": "reads", "paired_end": "1", "file_size_mb": 800},
    {"accession": "ENCFF901CR2", "output_type": "reads", "paired_end": "2", "file_size_mb": 850}
  ]
}
```

**Interpretation**: CUT&RUN yields smaller files than ChIP-seq (~800MB vs ~2.5GB) due to lower background.

### Step 3: Run the CUT&RUN pipeline

```bash
nextflow run pipeline-cutandrun/main.nf \
  --fastq_r1 ENCFF900CR1.fastq.gz \
  --fastq_r2 ENCFF901CR2.fastq.gz \
  --genome GRCh38 \
  --spike_in_genome dm6 \
  --target H3K27me3 \
  --peak_caller seacr \
  -profile docker
```

Key pipeline steps:
1. Adapter trimming (Trim Galore)
2. Bowtie2 alignment (very-sensitive-local)
3. Spike-in alignment (E. coli or Drosophila)
4. Spike-in normalization (scale factor)
5. SEACR peak calling (stringent mode)
6. Signal track generation with spike-in scaling

### Step 4: Validate output quality

| Metric | Threshold | Purpose |
|---|---|---|
| Spike-in alignment | 0.5-5% of reads | Normalization calibration |
| Fragment size | < 150bp majority | CUT&RUN characteristic |
| FRiP (SEACR) | >= 5% | Higher than ChIP-seq due to lower background |
| Duplicate rate | < 20% | Library complexity |

**Key difference from ChIP-seq**: CUT&RUN has inherently lower background, so peak callers like MACS2 overfit. Use SEACR (Meers et al. 2019) instead.

### Step 5: Compare with ChIP-seq for the same target

```
encode_search_experiments(assay_title="Histone ChIP-seq", biosample_term_name="K562", target="H3K27me3", organism="Homo sapiens")
```

**Interpretation**: CUT&RUN typically identifies fewer but higher-confidence peaks than ChIP-seq. Concordant peaks between both methods are the highest confidence.

### Integration with downstream skills
- SEACR peaks feed into -> **histone-aggregation** for cross-experiment comparison
- Spike-in normalized signals feed into -> **visualization-workflow**
- Peak regions feed into -> **regulatory-elements** for chromatin state classification
- QC uses different thresholds than ChIP-seq -> **quality-assessment** (see suspect list)
- Pipeline provenance logged by -> **data-provenance**

## Code Examples

### 1. Survey CUT&RUN/CUT&Tag availability

```
encode_get_facets(assay_title="CUT&RUN", facet_field="target.label", organism="Homo sapiens")
```

Expected output:
```json
{
  "facets": {
    "target.label": {"H3K27me3": 15, "H3K4me3": 12, "H3K27ac": 8, "CTCF": 5}
  }
}
```

### 2. Find matching ChIP-seq for comparison

```
encode_search_experiments(assay_title="Histone ChIP-seq", biosample_term_name="K562", target="H3K27me3", organism="Homo sapiens")
```

Expected output:
```json
{
  "total": 5,
  "results": [
    {"accession": "ENCSR000CHI", "assay_title": "Histone ChIP-seq", "target": "H3K27me3", "biosample_summary": "K562"}
  ]
}
```

### 3. Track CUT&RUN experiments

```
encode_track_experiment(accession="ENCSR900CUR", notes="K562 H3K27me3 CUT&RUN - SEACR peaks for comparison with ChIP-seq")
```

Expected output:
```json
{
  "status": "tracked",
  "accession": "ENCSR900CUR",
  "notes": "K562 H3K27me3 CUT&RUN - SEACR peaks for comparison with ChIP-seq"
}
```

## Integration

| This skill produces... | Feed into... | Purpose |
|---|---|---|
| SEACR peaks | **histone-aggregation** | Cross-experiment comparison (note: different caller than ChIP-seq) |
| Spike-in normalized signal | **visualization-workflow** | Quantitatively comparable browser tracks |
| Peak regions | **regulatory-elements** | Chromatin state classification |
| CUT&RUN-specific QC | **quality-assessment** | Validate with CUT&RUN-appropriate thresholds |
| Peak coordinates | **motif-analysis** | TF motif discovery at CUT&RUN peaks |
| Pipeline parameters | **data-provenance** | Record SEACR/spike-in normalization details |
| Peak files | **variant-annotation** | Identify variants in CUT&RUN peaks |
| Comparison with ChIP-seq | **compare-biosamples** | Cross-assay concordance analysis |

## Related Skills

- `pipeline-guide` -- Parent skill with compute resource assessment and cloud setup
- `histone-aggregation` -- Aggregate histone mark data across samples
- `quality-assessment` -- Evaluate pipeline output quality metrics
- `data-provenance` -- Track all pipeline inputs, outputs, and parameters
- `download-encode` -- Download ENCODE CUT&RUN FASTQ files for pipeline input
- `publication-trust` -- Verify literature claims backing analytical decisions

## Presenting Results

When reporting CUT&RUN pipeline results:

- **SEACR peak counts**: Report peak counts for both stringent and relaxed modes. If MACS2 was also run, include those counts for comparison
- **Spike-in normalization factor**: Report the computed scale factor per sample and the spike-in read fraction (ideal 1-10% of total reads). Explain that higher spike-in counts indicate less target enrichment
- **FRiP**: Report the fraction of reads in peaks (>10% pass, 5-10% warning, <5% fail). Note that CUT&RUN FRiP thresholds differ from ChIP-seq
- **Signal track paths**: Provide paths to spike-in normalized bigWig files for genome browser visualization
- **Fragment size distribution**: Confirm the expected nucleosomal ladder pattern and note the dominant fragment class (sub-nucleosomal for TFs, mononucleosomal for histone marks)
- **Key QC metrics**: Present mapping rate (>80%), duplication rate (<20%), and spike-in calibration status in a summary table
- **Suspect list filtering**: Note whether peaks were filtered against both the ENCODE blacklist and the CUT&RUN suspect list (Nordin 2023)
- **Next steps**: Suggest `peak-annotation` for gene association of peaks, or `visualization-workflow` for genome browser session generation

## For the request: "$ARGUMENTS"
