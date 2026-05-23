---
name: pipeline-hic
description: "Execute ENCODE Hi-C pipeline from FASTQ to contact matrices and loop calls. Child of pipeline-guide. Provides Nextflow execution with Docker and cloud deployment. Use when processing Hi-C data, generating contact matrices, calling loops or TADs. Trigger on: Hi-C pipeline, chromatin conformation, contact matrix, loop calling, TAD detection, Juicer, HiCCUPS, 3D genome."
---

# ENCODE Hi-C Pipeline: FASTQ to Contact Matrices and Loops

## When to Use

- User wants to run a Hi-C processing pipeline from FASTQ to contact matrices and loop calls
- User asks about "Hi-C pipeline", "contact matrix", "loop calling", "Juicer", "HiCCUPS", or "TAD detection"
- User needs to process Hi-C data for 3D genome structure analysis
- Example queries: "process my Hi-C FASTQs", "generate contact matrices from Hi-C", "call chromatin loops with HiCCUPS"

Execute the ENCODE Hi-C pipeline for chromatin conformation capture data,
producing multi-resolution contact matrices, loop calls, and compartment annotations.

## Pipeline Overview

```
FASTQ -> Trim -> BWA (per-mate) -> pairtools parse -> dedup -> .pairs
                                                                 |
                                                    +------------+------------+
                                                    |                         |
                                              Juicer pre -> .hic        cooler -> .mcool
                                                    |                         |
                                              HiCCUPS loops              Compartments
```

### ENCODE Repository

- **GitHub**: `ENCODE-DCC/hic-pipeline`
- **Container**: `encodedcc/hic-pipeline`
- **WDL**: Available for Cromwell execution
- **This skill**: Nextflow DSL2 reimplementation for portability

## Core Tools and Versions

| Tool | Version | Purpose | Citation |
|------|---------|---------|----------|
| BWA-MEM | 0.7.17 | Alignment (per-mate) | Li & Durbin 2009 |
| pairtools | 1.0.3 | Pair classification, dedup | Open2C |
| Juicer tools | 2.20.00 | .hic generation, HiCCUPS | Durand et al. 2016 |
| cooler | 0.9.3 | .cool/.mcool generation | Abdennur & Mirny 2020 |
| samtools | 1.19 | BAM operations | Li et al. 2009 |
| FastQC | 0.12.1 | Read quality | Andrews (Babraham) |
| MultiQC | 1.21 | Aggregated QC | Ewels et al. 2016 |

## Key Literature

1. **Rao et al. 2014** - "A 3D Map of the Human Genome at Kilobase Resolution
   Reveals Principles of Chromatin Looping" (Cell, ~5,000 citations)
   DOI: 10.1016/j.cell.2014.11.021

2. **Lieberman-Aiden et al. 2009** - "Comprehensive Mapping of Long-Range
   Interactions Reveals Folding Principles of the Human Genome" (Science, ~6,000 citations)
   DOI: 10.1126/science.1181369

3. **Durand et al. 2016** - "Juicer Provides a One-Click System for Analyzing
   Loop-Resolution Hi-C Experiments" (Cell Systems, ~2,000 citations)
   DOI: 10.1016/j.cels.2016.07.002

4. **Abdennur & Mirny 2020** - "Cooler: scalable storage for Hi-C data and
   other genomically labeled arrays" (Bioinformatics)
   DOI: 10.1093/bioinformatics/btz540

5. **Amemiya et al. 2019** - "The ENCODE Blacklist" (Scientific Reports, ~1,372 citations)
   DOI: 10.1038/s41598-019-45839-z

## Execution

### Quick Start (Local)

```bash
nextflow run main.nf \
    -profile local \
    --reads '/data/fastq/*_R{1,2}.fastq.gz' \
    --bwa_index '/ref/bwa_index/genome.fa' \
    --chrom_sizes '/ref/hg38.chrom.sizes' \
    --restriction_site 'GATC' \
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
    --restriction_site 'GATC' \
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
    --restriction_site 'GATC' \
    --outdir 'gs://bucket/results/' \
    -resume
```

## Resource Requirements

| Step | CPUs | RAM | Time (2B contacts) |
|------|------|-----|---------------------|
| BWA alignment | 8 | 16 GB | 4-6 hours |
| pairtools parse | 4 | 8 GB | 2-3 hours |
| pairtools dedup | 4 | 16 GB | 1-2 hours |
| Juicer pre + hic | 4 | 64 GB | 2-4 hours |
| HiCCUPS | 4 | 16 GB (+ GPU optional) | 1-2 hours |
| **Total** | **8** | **64 GB** | **8-16 hours** |

## Pipeline Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--reads` | required | Glob pattern to paired FASTQ files |
| `--bwa_index` | required | Path to BWA genome index (.fa with .bwt etc.) |
| `--chrom_sizes` | required | Chromosome sizes file |
| `--restriction_site` | `GATC` | Restriction enzyme site (GATC for MboI/DpnII) |
| `--outdir` | `./results` | Output directory |
| `--resolutions` | `1000,5000,10000,25000,50000,100000,250000,500000,1000000` | Matrix resolutions |
| `--min_mapq` | `30` | Minimum MAPQ for pair filtering |
| `--assembly` | `hg38` | Genome assembly name for .hic header |

## Output Files

```
results/
  fastqc/                         # Raw read quality
  alignment/
    {sample}.R1.bam               # Per-mate alignments
    {sample}.R2.bam
  pairs/
    {sample}.pairs.gz             # Classified, deduplicated pairs
    {sample}.dedup_stats.txt      # Duplication metrics
    {sample}.pair_stats.txt       # Pair type classification
  matrices/
    {sample}.hic                  # Juicer .hic file (primary output)
    {sample}.mcool                # Cooler multi-resolution matrix
  loops/
    {sample}.hiccups_loops.bedpe  # Called loops (HiCCUPS)
  qc/
    {sample}.contact_stats.txt    # Contact statistics
  multiqc/
    multiqc_report.html
```

### .hic File Format

The .hic format (Juicer) stores multi-resolution contact matrices with
normalization vectors. Can be visualized in Juicebox and loaded by
`hic-straw` in Python/R.

### .mcool File Format

The .mcool format (cooler) is an HDF5-based multi-resolution contact matrix.
Widely supported by `cooler`, `cooltools`, `HiGlass`, and `FAN-C`.

## QC Thresholds (ENCODE Standards)

| Metric | Pass | Warning | Fail |
|--------|------|---------|------|
| Valid pair fraction | >40% | 25-40% | <25% |
| Cis contacts (>20kb) | >40% | 25-40% | <25% |
| Cis/trans ratio | >1.5 | 1.0-1.5 | <1.0 |
| Library complexity (unique/total) | >0.7 | 0.5-0.7 | <0.5 |
| Contacts per resolution | See below | - | - |

### Resolution vs Depth Requirements

| Resolution | Minimum Contacts Needed | Typical Depth |
|------------|------------------------|---------------|
| 1 kb | >2 billion | Very deep |
| 5 kb | >500 million | Deep |
| 10 kb | >200 million | Standard |
| 25 kb | >50 million | Moderate |
| 100 kb | >10 million | Low |

## Pair Classification

pairtools classifies read pairs into categories:

| Category | Description | Use |
|----------|-------------|-----|
| UU | Both uniquely mapped | Valid contact |
| UR/RU | One unique, one rescued | Valid (rescued) |
| UX/XU | One unique, one unmapped | Not used |
| DD | Both duplicate | Removed |
| WW | Walk pair (same strand) | Indicates ligation artifact |
| NR | Null/rescue pair | Not used |

Only UU pairs (and optionally UR) are used for contact matrices.

## Critical Pitfalls

### Restriction Enzyme Choice
The restriction enzyme determines fragment size and resolution:
- **MboI/DpnII** (GATC): 4-cutter, ~256 bp average fragment -- higher resolution
- **HindIII** (AAGCTT): 6-cutter, ~4 kb average fragment -- lower resolution
- **Arima** (proprietary): Two enzymes, ~160 bp average -- highest resolution
- Always verify which enzyme was used before processing

### Normalization Method
Different normalization methods yield different results:
- **KR** (Knight-Ruiz): Default in Juicer, balanced normalization
- **ICE** (Imakaev et al.): Used by cooler/cooltools, iterative correction
- **VC** (Vanilla Coverage): Simple coverage normalization
- ENCODE standard: KR normalization. Always document which was used.

### Resolution Depends on Depth
Do not call features at resolutions unsupported by sequencing depth:
- Calling 1 kb loops from 100M contacts will produce noise
- Check the Juicer resolution QC to determine achievable resolution
- Loop calling (HiCCUPS) typically requires 5-10 kb resolution

### Ligation Artifacts
Same-strand pairs (WW) indicate self-ligation or undigested fragments:
- High WW fraction (>30%) suggests poor digestion
- Monitor pair type distribution as a QC metric
- Re-ligation distance plots should show enrichment at restriction sites

## Provenance Integration

After pipeline completion, log all outputs:

```python
encode_log_derived_file(
    file_path="/results/matrices/sample1.hic",
    source_accessions=["ENCSR...", "ENCFF..."],
    description="Hi-C contact matrix from ENCODE Hi-C pipeline",
    file_type="hic",
    tool_used="BWA 0.7.17 + pairtools 1.0.3 + Juicer 2.20.00",
    parameters="MboI digestion, KR normalization, resolutions 1kb-1Mb"
)
```

## Reference Files

Detailed step-by-step documentation is provided in the `references/` directory:

1. `01-qc-trimming.md` -- Read QC and adapter trimming
2. `02-alignment.md` -- BWA per-mate alignment strategy
3. `03-pair-processing.md` -- pairtools parse, sort, and dedup
4. `04-matrix-generation.md` -- Juicer .hic and cooler .mcool generation
5. `05-loop-calling.md` -- HiCCUPS loop detection and QC

## Walkthrough: Processing ENCODE Hi-C from FASTQ to Contact Maps and Loops

**Goal**: Process raw Hi-C FASTQ files through the ENCODE pipeline to generate contact matrices, TAD calls, and chromatin loop predictions.
**Context**: Hi-C captures 3D chromatin organization. The pipeline uses BWA for chimeric read alignment, pairtools for pair processing, and Juicer/HiCCUPS for loop calling.

### Step 1: Find Hi-C experiment

```
encode_get_experiment(accession="ENCSR000AKA")
```

Expected output:
```json
{
  "accession": "ENCSR000AKA",
  "assay_title": "Hi-C",
  "biosample_summary": "GM12878",
  "replicates": 2,
  "status": "released"
}
```

### Step 2: List FASTQ files

```
encode_list_files(accession="ENCSR000AKA", file_format="fastq")
```

Expected output:
```json
{
  "files": [
    {"accession": "ENCFF500HI1", "output_type": "reads", "paired_end": "1", "file_size_mb": 35000},
    {"accession": "ENCFF501HI2", "output_type": "reads", "paired_end": "2", "file_size_mb": 36000}
  ]
}
```

**Interpretation**: Hi-C paired-end reads represent chimeric ligation junctions. Each read pair captures a 3D contact.

### Step 3: Run the Hi-C pipeline

```bash
nextflow run pipeline-hic/main.nf \
  --fastq_r1 ENCFF500HI1.fastq.gz \
  --fastq_r2 ENCFF501HI2.fastq.gz \
  --genome GRCh38 \
  --restriction_enzyme DpnII \
  --resolution 5000,10000,25000 \
  -profile docker
```

Key pipeline steps:
1. BWA-MEM alignment (chimeric read handling)
2. pairtools parse (extract valid pairs)
3. pairtools dedup (remove PCR duplicates)
4. Contact matrix generation (.hic format)
5. TAD calling (directionality index or insulation score)
6. Loop calling (HiCCUPS at 5kb/10kb/25kb resolution)

### Step 4: Validate output quality

| Metric | Threshold | Purpose |
|---|---|---|
| Cis/trans ratio | > 60% cis | Library quality |
| Long-range cis | > 40% of cis | Useful contacts |
| Valid pairs | > 50% of mapped | Ligation success |
| Duplicate rate | < 30% | Library complexity |

### Step 5: Identify significant loops

Download loop calls for downstream analysis:
```
encode_list_files(accession="ENCSR000AKA", file_format="bedpe", assembly="GRCh38")
```

### Integration with downstream skills
- Loop calls (BEDPE) feed into -> **hic-aggregation** for cross-tissue loop catalog
- TAD boundaries feed into -> **regulatory-elements** for domain-level regulation
- Loop anchors feed into -> **peak-annotation** for enhancer-promoter assignment
- Contact data integrates with -> **visualization-workflow** for 3D genome display
- Pipeline provenance logged by -> **data-provenance**

## Code Examples

### 1. Find Hi-C data for 3D genome analysis

```
encode_search_experiments(
  assay_title="Hi-C",
  organ="heart"
)
```

Expected output:
```json
{
  "total": 4,
  "experiments": [
    {
      "accession": "ENCSR654HRT",
      "assay_title": "Hi-C",
      "biosample_summary": "heart left ventricle tissue male adult (51 years)",
      "status": "released"
    }
  ]
}
```

### 2. Get experiment details for pipeline configuration

```
encode_get_experiment(accession="ENCSR654HRT")
```

Expected output:
```json
{
  "accession": "ENCSR654HRT",
  "assay_title": "Hi-C",
  "replicates": 2,
  "biosample_summary": "heart left ventricle tissue male adult (51 years)",
  "files_count": 18,
  "assembly": "GRCh38",
  "audit": {"ERROR": 0, "WARNING": 1}
}
```

## Integration

| This skill produces... | Feed into... | Purpose |
|---|---|---|
| Chromatin loops (BEDPE) | **hic-aggregation** | Cross-tissue loop catalog |
| TAD boundaries | **regulatory-elements** | Domain-level regulatory architecture |
| Loop anchors (BED) | **peak-annotation** | Assign genes to loop-connected enhancers |
| Contact matrices (.hic) | **visualization-workflow** | 3D genome visualization |
| Loop-disrupting coordinates | **variant-annotation** | Identify variants breaking chromatin contacts |
| QC metrics | **quality-assessment** | Validate Hi-C library quality |
| Pipeline parameters | **data-provenance** | Record BWA/pairtools/Juicer versions |
| Loop anchor regions | **motif-analysis** | Discover CTCF motifs at loop anchors |

## Related Skills

- `pipeline-guide` -- Parent skill with compute resource assessment and cloud setup
- `hic-aggregation` -- Aggregate Hi-C loops across samples/tissues
- `quality-assessment` -- Evaluate pipeline output quality metrics
- `data-provenance` -- Track all pipeline inputs, outputs, and parameters
- `download-encode` -- Download ENCODE Hi-C FASTQ files for pipeline input
- `publication-trust` -- Verify literature claims backing analytical decisions

## Presenting Results

When reporting Hi-C pipeline results:

- **Valid pair count**: Report total valid pairs (UU + optionally UR) and the fraction of all read pairs that are valid contacts
- **Cis/trans ratio**: Report the cis/trans contact ratio (>1.5 pass) and long-range cis fraction (>20kb, >40% expected). These are the primary Hi-C quality indicators
- **Contact matrix resolution**: Report the achievable resolution based on sequencing depth (e.g., "500M valid pairs supports 5kb resolution") and list all resolutions generated
- **Loop counts**: Report HiCCUPS loop count at each resolution tested and note the resolution with the most loops called
- **Matrix paths**: Provide paths to the .hic file (Juicebox-compatible) and .mcool file (cooler/HiGlass-compatible)
- **Key QC metrics**: Present library complexity (unique/total >0.7), WW pair fraction (<30%), and pair classification distribution in a summary table
- **Normalization**: Note which normalization was applied (KR default for Juicer)
- **Next steps**: Suggest `hic-aggregation` for cross-sample loop catalogs, or `visualization-workflow` for Juicebox/HiGlass session setup

## For the request: "$ARGUMENTS"
