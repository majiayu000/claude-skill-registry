---
name: pipeline-wgbs
description: "Execute ENCODE Whole Genome Bisulfite Sequencing (WGBS) pipeline from FASTQ to methylation calls. Child of pipeline-guide. Provides Nextflow execution with Docker and cloud deployment. Use when processing WGBS/bisulfite-seq data, calling methylation levels, generating bedMethyl files. Trigger on: WGBS pipeline, bisulfite sequencing, methylation calling, DNA methylation pipeline, bismark, bwa-meth, bedMethyl."
---

# ENCODE WGBS Pipeline: FASTQ to Methylation Calls

## When to Use

- User wants to run a WGBS/bisulfite sequencing pipeline from FASTQ to methylation calls
- User asks about "WGBS pipeline", "bisulfite sequencing", "methylation calling", "Bismark", or "bedMethyl"
- User needs to process whole-genome bisulfite sequencing data following ENCODE standards
- Example queries: "process my WGBS FASTQs", "call methylation levels from bisulfite-seq", "run Bismark on my WGBS data"

Execute the ENCODE DNA methylation pipeline for Whole Genome Bisulfite Sequencing data,
producing per-CpG methylation levels in bedMethyl format.

## Pipeline Overview

```
FASTQ -> Trim adapters -> Bismark align -> Deduplicate -> MethylDackel extract -> bedMethyl
  |           |               |                |                |                    |
  QC      Trim Galore    Bismark/bwa-meth   Picard         Per-CpG calls      Final output
```

### ENCODE Repository

- **GitHub**: `ENCODE-DCC/dna-me-pipeline`
- **Container**: `encodedcc/dna-me-pipeline`
- **WDL**: Available for Cromwell execution
- **This skill**: Nextflow DSL2 reimplementation for portability

## Core Tools and Versions

| Tool | Version | Purpose | Citation |
|------|---------|---------|----------|
| Trim Galore | 0.6.10 | Adapter + quality trimming (bisulfite-aware) | Krueger (Babraham) |
| Bismark | 0.24.2 | Bisulfite-aware alignment + methylation | Krueger & Andrews 2011 |
| bwa-meth | 0.2.7 | Alternative bisulfite aligner (faster) | Pedersen 2014 |
| MethylDackel | 0.6.1 | Methylation extraction from BAM | Ryan (GitHub) |
| Picard | 3.1.1 | Duplicate marking | Broad Institute |
| samtools | 1.19 | BAM operations | Li et al. 2009 |
| FastQC | 0.12.1 | Read quality assessment | Andrews (Babraham) |
| MultiQC | 1.21 | Aggregated QC reporting | Ewels et al. 2016 |

## Key Literature

1. **Krueger & Andrews 2011** - "Bismark: a flexible aligner and methylation caller for
   Bisulfite-Seq applications" (Bioinformatics, ~4,000 citations)
   DOI: 10.1093/bioinformatics/btr167

2. **Lister et al. 2009** - "Human DNA methylomes at base resolution show widespread
   epigenomic differences" (Nature, ~5,000 citations)
   DOI: 10.1038/nature08514

3. **Schultz et al. 2015** - "Human body epigenome maps reveal noncanonical DNA
   methylation variation" (Nature, ~1,500 citations)
   DOI: 10.1038/nature14248

4. **Pedersen et al. 2014** - "Fast and accurate alignment of long bisulfite-seq reads"
   arXiv:1401.1129 (bwa-meth)

5. **Amemiya et al. 2019** - "The ENCODE Blacklist" (Scientific Reports, ~1,372 citations)
   DOI: 10.1038/s41598-019-45839-z

## Execution

### Quick Start (Local)

```bash
nextflow run main.nf \
    -profile local \
    --reads '/data/fastq/*_R{1,2}.fastq.gz' \
    --genome_dir '/ref/bismark_index' \
    --outdir results/ \
    -resume
```

### SLURM HPC

```bash
nextflow run main.nf \
    -profile slurm \
    --reads '/data/fastq/*_R{1,2}.fastq.gz' \
    --genome_dir '/ref/bismark_index' \
    --outdir results/ \
    -resume
```

### Cloud (GCP / AWS)

```bash
nextflow run main.nf \
    -profile gcp \
    --reads 'gs://bucket/fastq/*_R{1,2}.fastq.gz' \
    --genome_dir 'gs://bucket/ref/bismark_index' \
    --outdir 'gs://bucket/results/' \
    -resume
```

## Resource Requirements

| Step | CPUs | RAM | Time (30x human) |
|------|------|-----|-------------------|
| Trim Galore | 4 | 4 GB | 1-2 hours |
| Bismark align | 8 | 48 GB | 8-16 hours |
| Deduplication | 2 | 16 GB | 1-2 hours |
| MethylDackel | 4 | 8 GB | 1-2 hours |
| **Total** | **8** | **48 GB** | **12-24 hours** |

## Pipeline Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--reads` | required | Glob pattern to paired FASTQ files |
| `--genome_dir` | required | Path to Bismark genome index directory |
| `--outdir` | `./results` | Output directory |
| `--aligner` | `bismark` | Aligner: `bismark` or `bwameth` |
| `--min_coverage` | `5` | Minimum coverage for CpG reporting |
| `--no_overlap` | `true` | Remove overlapping PE reads (avoid double-counting) |
| `--lambda_genome` | `null` | Lambda genome index for conversion rate QC |
| `--skip_dedup` | `false` | Skip deduplication (for RRBS data) |

## Output Files

```
results/
  fastqc/                    # Raw read quality
  trim_galore/               # Trimmed reads + reports
  bismark/
    alignments/              # Sorted, deduplicated BAMs
    dedup_reports/           # Duplication metrics
    methylation/             # bedMethyl files (primary output)
      {sample}.CpG.bedMethyl.gz
      {sample}.CHG.bedMethyl.gz   # Non-CpG contexts
      {sample}.CHH.bedMethyl.gz
    conversion_rate/         # Lambda/pUC19 conversion QC
  coverage/
    {sample}.coverage_stats.txt
  multiqc/
    multiqc_report.html
```

### bedMethyl Format

The primary output is per-CpG methylation in bedMethyl format:

```
chr1  10468  10470  .  1000  +  10468  10470  0,0,0  12  83.3
```

Columns: chr, start, end, name, score, strand, thickStart, thickEnd, color,
coverage, methylation_percentage

## QC Thresholds (ENCODE Standards)

| Metric | Pass | Warning | Fail |
|--------|------|---------|------|
| Bisulfite conversion rate | ≥98% | 95-98% | <95% |
| CpG coverage (genome-wide) | >10x | 5-10x | <5x |
| Mapping rate | >70% | 50-70% | <50% |
| Duplication rate | <30% | 30-50% | >50% |
| CpG sites covered (>=5x) | >80% | 60-80% | <60% |
| Lambda spike-in conversion | ≥98% | 95-98% | <95% |

## Critical Pitfalls

### RRBS vs WGBS
RRBS (Reduced Representation) uses MspI digestion and covers ~10% of CpGs.
WGBS covers the full genome. These are DIFFERENT protocols:
- RRBS: Skip deduplication (`--skip_dedup true`), different trimming
- WGBS: Full dedup required, standard Trim Galore settings
- Never mix RRBS and WGBS data in the same analysis

### Strand-Specific vs Merged CpG
Bismark reports methylation per strand by default. For most analyses, merge
complementary CpG strands:
- Forward C at position N and reverse G at position N+1 are the same CpG
- MethylDackel `--mergeContext` handles this automatically
- Always specify `--mergeContext` unless you need strand-specific data

### Incomplete Bisulfite Conversion
Conversion artifacts produce false methylation calls:
- Always include lambda phage or pUC19 spike-in DNA
- Unmethylated spike-in should show ≥98% conversion
- If conversion <98%, the library has systematic artifacts -- do NOT proceed

### M-bias Plots
MethylDackel generates M-bias plots showing methylation level by read position:
- End-repair artifacts cause elevated methylation at read ends
- Use `--OT` and `--OB` flags to trim affected positions
- ENCODE typically trims 10 bp from 5' of read 2

### Low Coverage Regions
Regions with <5x coverage have unreliable methylation estimates:
- Filter bedMethyl to `--min_coverage 5` (default)
- For differential methylation analysis, consider `--min_coverage 10`
- Report the fraction of CpGs meeting coverage threshold

## Provenance Integration

After pipeline completion, log all outputs:

```python
# Log derived bedMethyl files
encode_log_derived_file(
    file_path="/results/bismark/methylation/sample1.CpG.bedMethyl.gz",
    source_accessions=["ENCSR...", "ENCFF..."],
    description="CpG methylation calls from ENCODE WGBS pipeline",
    file_type="bedMethyl",
    tool_used="Bismark 0.24.2 + MethylDackel 0.6.1",
    parameters="bismark --genome /ref -1 R1.fq.gz -2 R2.fq.gz; MethylDackel extract --mergeContext --minDepth 5"
)
```

## Reference Files

Detailed step-by-step documentation is provided in the `references/` directory:

1. `01-qc-trimming.md` -- Bisulfite-specific adapter trimming with Trim Galore
2. `02-bismark-alignment.md` -- Bismark alignment and bwa-meth alternative
3. `03-dedup-filtering.md` -- Deduplication and BAM filtering
4. `04-methylation-calling.md` -- MethylDackel extraction and bedMethyl generation
5. `05-qc-metrics.md` -- Conversion rate QC, coverage stats, M-bias

## Walkthrough: Processing ENCODE WGBS from FASTQ to Methylation Calls

**Goal**: Process whole-genome bisulfite sequencing FASTQ files through the ENCODE pipeline to generate per-CpG methylation calls for epigenomic analysis.
**Context**: WGBS requires bisulfite-aware alignment (Bismark) and per-CpG methylation extraction (MethylDackel), with ≥98% bisulfite conversion required.

### Step 1: Find WGBS experiment

```
encode_get_experiment(accession="ENCSR765JPC")
```

Expected output:
```json
{
  "accession": "ENCSR765JPC",
  "assay_title": "WGBS",
  "biosample_summary": "liver",
  "replicates": 2,
  "status": "released"
}
```

### Step 2: List FASTQ files

```
encode_list_files(accession="ENCSR765JPC", file_format="fastq")
```

Expected output:
```json
{
  "files": [
    {"accession": "ENCFF300BS1", "output_type": "reads", "paired_end": "1", "file_size_mb": 45000},
    {"accession": "ENCFF301BS2", "output_type": "reads", "paired_end": "2", "file_size_mb": 46000}
  ]
}
```

**Interpretation**: WGBS files are very large (~45GB per read file). Ensure adequate storage (>500GB for processing).

### Step 3: Run the WGBS pipeline

```bash
nextflow run pipeline-wgbs/main.nf \
  --fastq_r1 ENCFF300BS1.fastq.gz \
  --fastq_r2 ENCFF301BS2.fastq.gz \
  --genome GRCh38 \
  --bismark_index /ref/bismark_index/ \
  -profile docker
```

Key pipeline steps:
1. Adapter/quality trimming (Trim Galore)
2. Bisulfite-aware alignment (Bismark)
3. Deduplication (Bismark deduplicate)
4. Methylation extraction (MethylDackel)
5. CpG coverage and beta-value calculation
6. Bisulfite conversion rate check (≥98% required)

### Step 4: Validate output quality

| Metric | Threshold | Purpose |
|---|---|---|
| Bisulfite conversion | >= 98% | Library quality |
| CpG coverage | >= 10x for DMR calling | Statistical power |
| Mapping rate | > 40% (BS-aware) | Alignment success |
| Duplication rate | < 30% | Library complexity |

### Step 5: Identify differentially methylated regions

Feed per-CpG methylation into -> **methylation-aggregation** for cross-tissue comparison and HMR/UMR/PMD identification.

### Integration with downstream skills
- Per-CpG methylation files feed into -> **methylation-aggregation** for cross-tissue atlas
- DMRs feed into -> **peak-annotation** for nearest gene assignment
- Methylation at regulatory elements connects to -> **regulatory-elements**
- CpG variant methylation integrates with -> **variant-annotation**
- Pipeline provenance logged by -> **data-provenance**

## Code Examples

### 1. Find WGBS data for methylation analysis

```
encode_search_experiments(
  assay_title="WGBS",
  organ="brain"
)
```

Expected output:
```json
{
  "total": 6,
  "experiments": [
    {
      "accession": "ENCSR321BRN",
      "assay_title": "WGBS",
      "biosample_summary": "brain tissue female adult (53 years)",
      "status": "released"
    }
  ]
}
```

### 2. Download processed methylation files

```
encode_search_files(
  assay_title="WGBS",
  organ="brain",
  file_format="bed",
  output_type="methylation state at CpG",
  assembly="GRCh38"
)
```

Expected output:
```json
{
  "total": 3,
  "files": [
    {
      "accession": "ENCFF567MET",
      "output_type": "methylation state at CpG",
      "assembly": "GRCh38",
      "file_size_mb": 845.2
    }
  ]
}
```

## Integration

| This skill produces... | Feed into... | Purpose |
|---|---|---|
| Per-CpG methylation (bedMethyl) | **methylation-aggregation** | Cross-tissue methylation atlas |
| Differentially methylated regions | **peak-annotation** | Assign DMRs to nearest genes |
| Methylation at regulatory sites | **regulatory-elements** | Correlate methylation with cCRE activity |
| CpG methylation near variants | **variant-annotation** | Annotate variants affecting CpG methylation |
| Signal tracks (bigWig) | **visualization-workflow** | Display methylation signal in genome browser |
| QC metrics | **quality-assessment** | Validate conversion rate and coverage |
| Pipeline parameters | **data-provenance** | Record Bismark/MethylDackel versions |
| Methylation at promoters | **gtex-expression** | Correlate promoter methylation with gene expression |

## Related Skills

- `pipeline-guide` -- Parent skill with compute resource assessment and cloud setup
- `methylation-aggregation` -- Aggregate methylation data across samples/tissues
- `quality-assessment` -- Evaluate pipeline output quality metrics
- `data-provenance` -- Track all pipeline inputs, outputs, and parameters
- `download-encode` -- Download ENCODE WGBS FASTQ files for pipeline input
- `publication-trust` -- Verify literature claims backing analytical decisions

## Presenting Results

When reporting WGBS pipeline results:

- **Bisulfite conversion rate**: Report the lambda/pUC19 spike-in conversion rate prominently (≥98% pass, 95-98% warning, <95% fail). This is the most critical QC metric for WGBS
- **CpG coverage depth**: Report genome-wide mean CpG coverage and fraction of CpGs meeting the minimum depth threshold (>=5x for reporting, >=10x for DMR analysis)
- **Global methylation level**: Report the genome-wide average CpG methylation percentage and note any non-CpG (CHG/CHH) methylation if relevant to the tissue
- **bedMethyl output paths**: Provide paths to the primary CpG bedMethyl files and any CHG/CHH context files generated
- **M-bias assessment**: Note whether M-bias trimming was applied and which read positions were excluded
- **Key QC metrics**: Present mapping rate (>70%), duplication rate (<30%), and coverage statistics in a summary table
- **Output summary**: Report total CpG sites called, sites passing coverage filter, and estimated data completeness
- **Next steps**: Suggest `methylation-aggregation` for cross-sample averaging and HMR/UMR/PMD identification

## For the request: "$ARGUMENTS"
