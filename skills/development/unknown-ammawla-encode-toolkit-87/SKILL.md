---
name: liftover-coordinates
description: Convert genomic coordinates between assembly versions (GRCh37/hg19 to GRCh38/hg38, mm9 to mm10). Guides UCSC liftOver for BED files, CrossMap for VCF/bigWig, and handles unmapped regions with provenance logging.
---

# Convert Genomic Coordinates Between Assembly Versions

## When to Use

- User needs to convert genomic coordinates between assemblies (hg19↔hg38, mm9↔mm10)
- User asks about "liftover", "coordinate conversion", "assembly mismatch", or "CrossMap"
- User has data in hg19/GRCh37 that needs conversion to GRCh38 (or vice versa) before integration
- User wants to use UCSC liftOver or CrossMap for BED, VCF, bigWig, or BAM files
- Example queries: "convert my hg19 peaks to hg38", "liftover coordinates for integration with ENCODE", "my data is in mm9, how do I convert to mm10?"

Guide coordinate liftover between genome assemblies using UCSC liftOver, CrossMap, Ensembl REST API, and rtracklayer. Assembly conversion is one of the most common pitfalls in genomics — this skill provides the definitive workflow for safe, reproducible liftover with full provenance tracking.

## Scientific Rationale

**The question**: "How do I safely convert my genomic coordinates from one assembly to another without losing data or introducing errors?"

Assembly conversion is referenced as a critical step in 10+ other ENCODE Toolkit skills because ENCODE spans multiple data releases: some experiments were processed against hg19/GRCh37, while most current data uses GRCh38/hg38. Combining data across assemblies without proper liftover is one of the most common and most dangerous errors in computational genomics — coordinates that look valid in both assemblies may refer to completely different genomic locations.

### The Core Problem

Genome assemblies are updated to fix errors, fill gaps, add alternative haplotypes, and improve centromeric/telomeric sequence. Between hg19 and hg38, approximately 1,000 sequence gaps were closed, 8% of the genome was modified, and several regions were rearranged. A coordinate like chr17:41,197,694 in hg19 (BRCA1) maps to chr17:43,044,295 in GRCh38 — a shift of nearly 2 Mb. Using the wrong assembly silently produces incorrect results.

### When to Liftover

Common scenarios requiring coordinate conversion:

- **Combining ENCODE data from different releases**: Some hg19, some GRCh38 — must unify before intersection
- **Integrating GWAS Catalog results**: Many GWAS hits are still reported in hg19/GRCh37 coordinates
- **Using gnomAD**: gnomAD v4 uses GRCh38; older v2 datasets use GRCh37
- **Cross-species comparison**: Mouse data across mm9/mm10/GRCm39
- **Legacy datasets**: Published supplementary files often use older assemblies
- **ClinVar integration**: Some ClinVar entries reference GRCh37 positions
- **GTEx cross-reference**: GTEx v8 uses GRCh38, earlier versions used GRCh37

### Literature Support

- **Kent et al. 2002** (Genome Research, ~5,000 citations): UCSC Genome Browser and the liftOver tool. The original chain/net alignment framework for coordinate conversion between genome assemblies. [DOI](https://doi.org/10.1101/gr.229102)
- **Zhao et al. 2014** (Bioinformatics, ~800 citations): CrossMap — a versatile tool for coordinate conversion between genome assemblies. Handles VCF, BAM, bigWig, GFF, and Wiggle formats that UCSC liftOver cannot process natively. [DOI](https://doi.org/10.1093/bioinformatics/btt730)
- **Hinrichs et al. 2006** (Nucleic Acids Research, ~1,200 citations): UCSC genome browser chain/net alignment methodology. Defines the reciprocal-best chain alignment that underpins coordinate conversion. [DOI](https://doi.org/10.1093/nar/gkj144)
- **Kuhn et al. 2013** (Nucleic Acids Research, ~600 citations): Assembly updates and the implications for re-annotation. Documents the biological impact of assembly changes on gene models and regulatory element coordinates. [DOI](https://doi.org/10.1093/nar/gks1195)
- **Schneider et al. 2017** (Genome Research, ~400 citations): GRCh38 improvements over GRCh37 — gap closures, centromere models, alternative haplotypes. Quantifies what changed and why liftover is necessary. [DOI](https://doi.org/10.1101/gr.213611.116)
- **Amemiya et al. 2019** (Scientific Reports, ~1,372 citations): ENCODE Blacklist regions — some blacklisted regions are assembly-specific. Liftover of blacklist files must use the correct version. [DOI](https://doi.org/10.1038/s41598-019-45839-z)

## Assembly Version Mapping

| Common Name | UCSC Name | NCBI/GRC Name | Species | Release Year |
|------------|-----------|---------------|---------|-------------|
| hg19 | hg19 | GRCh37 | Human | 2009 |
| hg38 | hg38 | GRCh38 | Human | 2013 |
| mm9 | mm9 | MGSCv37 | Mouse | 2007 |
| mm10 | mm10 | GRCm38 | Mouse | 2012 |
| mm39 | mm39 | GRCm39 | Mouse | 2020 |

### Naming Convention Alert

The same assembly has different names depending on the source:
- **UCSC convention**: `hg19`, `hg38`, `mm10` — used in filenames, chromosome prefixes (`chr1`)
- **NCBI/GRC convention**: `GRCh37`, `GRCh38`, `GRCm38` — used in publications, Ensembl
- **Ensembl convention**: Chromosomes without `chr` prefix (`1` instead of `chr1`)

Always verify which naming convention your data uses. Mixing `chr1` (UCSC) with `1` (Ensembl) causes silent failures in bedtools intersection and peak overlap analysis.

## Chain Files

Chain files encode the alignment between assemblies and are the essential input for liftover.

### Source: UCSC (Recommended)

```
https://hgdownload.soe.ucsc.edu/goldenPath/{from}/liftOver/{from}To{To}.over.chain.gz
```

Common chain files:
| Conversion | Chain File | URL |
|-----------|-----------|-----|
| hg19 to hg38 | hg19ToHg38.over.chain.gz | `https://hgdownload.soe.ucsc.edu/goldenPath/hg19/liftOver/hg19ToHg38.over.chain.gz` |
| hg38 to hg19 | hg38ToHg19.over.chain.gz | `https://hgdownload.soe.ucsc.edu/goldenPath/hg38/liftOver/hg38ToHg19.over.chain.gz` |
| mm9 to mm10 | mm9ToMm10.over.chain.gz | `https://hgdownload.soe.ucsc.edu/goldenPath/mm9/liftOver/mm9ToMm10.over.chain.gz` |
| mm10 to mm39 | mm10ToMm39.over.chain.gz | `https://hgdownload.soe.ucsc.edu/goldenPath/mm10/liftOver/mm10ToMm39.over.chain.gz` |
| mm10 to hg38 | mm10ToHg38.over.chain.gz | `https://hgdownload.soe.ucsc.edu/goldenPath/mm10/liftOver/mm10ToHg38.over.chain.gz` |

### Source: Ensembl

```
ftp://ftp.ensembl.org/pub/assembly_mapping/
```

Ensembl provides chain files for their coordinate system (without `chr` prefix). Useful when working with Ensembl VEP output or Ensembl gene annotations.

### Source: NCBI Remap

NCBI Genome Remapping Service: `https://www.ncbi.nlm.nih.gov/genome/tools/remap`
- Web-based and API access
- Handles complex remapping with alignment-based and annotation-based methods
- Useful for non-standard assemblies or patch-level conversions

### Chain File Verification

Always verify chain file integrity after download:
```bash
wget https://hgdownload.soe.ucsc.edu/goldenPath/hg19/liftOver/hg19ToHg38.over.chain.gz
md5sum hg19ToHg38.over.chain.gz
# Verify against UCSC md5sum.txt in the same directory
gunzip -t hg19ToHg38.over.chain.gz  # Test archive integrity
```

## Tool Guide: UCSC liftOver (BED Files)

The standard tool for BED-format coordinate conversion.

### Basic Usage

```bash
liftOver input.bed hg19ToHg38.over.chain.gz output.bed unmapped.bed
```

### Parameters

| Parameter | Default | Description |
|----------|---------|-------------|
| `-minMatch` | 0.95 | Minimum ratio of bases that must remap (0.0–1.0) |
| `-minBlocks` | 1 | Minimum number of alignment blocks |
| `-fudgeThick` | off | If thickStart/thickEnd not mapped, use mapped region |
| `-multiple` | off | Allow mapping to multiple output regions |
| `-minChainT` | 0 | Minimum chain target coverage |
| `-minChainQ` | 0 | Minimum chain query coverage |

### Recommended Settings by Data Type

| Data Type | `-minMatch` | Notes |
|----------|-------------|-------|
| SNP positions (1bp) | 0.95 (default) | Point coordinates almost always map cleanly |
| Narrow peaks (100–500bp) | 0.95 (default) | Short regions map well |
| Broad peaks (1–50kb) | 0.50–0.80 | Large regions may partially overlap rearrangements |
| Regulatory elements | 0.90 | Balance between completeness and accuracy |
| TAD boundaries (5–50kb) | 0.50 | Large-scale organization is approximate anyway |

### Handling narrowPeak Format

UCSC liftOver expects standard BED (3–12 columns). For narrowPeak files (BED6+4):

```bash
# Step 1: Extract BED6 columns + preserve extra columns as name
awk 'BEGIN{OFS="\t"} {print $1, $2, $3, $4, $5, $6, $7, $8, $9, $10}' input.narrowPeak > input_full.bed

# Step 2: Liftover (liftOver handles extra columns)
liftOver input_full.bed hg19ToHg38.over.chain.gz output.bed unmapped.bed

# Step 3: Verify column count is preserved
awk '{print NF}' output.bed | sort -u
```

**Peak summit recalculation**: After liftover, the summit position (column 10 in narrowPeak = offset from start) may no longer accurately represent the signal maximum. For critical analyses, re-calculate summits from signal data in the new assembly rather than relying on lifted summit positions.

### Checking Unmapped Regions

```bash
# Count unmapped regions
wc -l unmapped.bed  # Note: comment lines start with #

# Calculate loss rate
total=$(wc -l < input.bed)
unmapped=$(grep -v '^#' unmapped.bed | wc -l)
loss_pct=$(echo "scale=2; $unmapped * 100 / $total" | bc)
echo "Lost $unmapped of $total regions ($loss_pct%)"

# Investigate reasons for unmapping
grep '^#' unmapped.bed | sort | uniq -c | sort -rn
# Common reasons:
# "Partially deleted in new" — region spans a deletion
# "Deleted in new" — region fully removed
# "Split in new" — region maps to multiple locations
```

## Tool Guide: CrossMap (VCF, bigWig, BAM, GFF)

CrossMap (Zhao et al. 2014) handles file formats that UCSC liftOver cannot process natively.

### VCF Conversion

```bash
CrossMap vcf hg19ToHg38.over.chain.gz input.vcf hg38.fa output.vcf
```

**Critical VCF considerations**:
- CrossMap updates coordinates AND checks REF alleles against the new reference
- Variants where the REF allele changes between assemblies are flagged
- Always re-validate variant calls after liftover using `bcftools norm`
- Multi-allelic variants may need special handling

```bash
# Post-liftover VCF validation
bcftools norm -f hg38.fa -c ws output.vcf -o output.normalized.vcf 2> norm_warnings.log
# -c ws: warn about and set incorrect REF alleles
```

### bigWig Conversion

```bash
CrossMap bigwig hg19ToHg38.over.chain.gz input.bw output.bw
```

**Signal track caveats**:
- Resolution is reduced during conversion (interpolation at boundaries)
- Regions that split during liftover lose signal accuracy
- For quantitative analysis, re-generate signal tracks from re-aligned reads when possible

### BAM Conversion

```bash
CrossMap bam hg19ToHg38.over.chain.gz input.bam output.bam
```

**BAM liftover is generally NOT recommended**:
- Read mapping quality is meaningless after coordinate shifting
- Paired-end relationships may break
- Duplicate marking becomes invalid
- **Best practice**: Re-align from FASTQ to the new reference genome

### GFF/GTF Conversion

```bash
CrossMap gff hg19ToHg38.over.chain.gz input.gff output.gff
```

Useful for lifting gene annotations, but prefer downloading the native annotation for the target assembly from GENCODE or Ensembl.

## Tool Guide: Ensembl REST API (Single Coordinates)

For programmatic conversion of individual coordinates without installing local tools.

### API Endpoint

```
GET https://rest.ensembl.org/map/human/GRCh37/{region}/GRCh38?content-type=application/json
```

### Example

```python
import requests

def liftover_ensembl(chrom, start, end, source="GRCh37", target="GRCh38", species="human"):
    """Convert coordinates using Ensembl REST API."""
    region = f"{chrom}:{start}..{end}:1"
    url = f"https://rest.ensembl.org/map/{species}/{source}/{region}/{target}"
    headers = {"Content-Type": "application/json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        mappings = response.json()["mappings"]
        return mappings
    return None

# Example: BRCA1 region
mappings = liftover_ensembl("17", 41197694, 41276113)
for m in mappings:
    mapped = m["mapped"]
    print(f"  {mapped['seq_region_name']}:{mapped['start']}-{mapped['end']}")
```

### Rate Limits

- 15 requests per second (without registered email)
- 50 requests per second (with registered email in User-Agent header)
- For batch conversion, use local liftOver or CrossMap instead

### Ensembl Chromosome Naming

Ensembl uses chromosomes WITHOUT `chr` prefix:
- Ensembl: `17:41197694-41276113`
- UCSC: `chr17:41197694-41276113`

Convert between conventions:
```bash
# Add 'chr' prefix (Ensembl to UCSC)
sed 's/^/chr/' input.bed > input_ucsc.bed

# Remove 'chr' prefix (UCSC to Ensembl)
sed 's/^chr//' input.bed > input_ensembl.bed
```

## Tool Guide: R (rtracklayer)

For R-based workflows, rtracklayer provides native liftover support.

```r
library(rtracklayer)
library(GenomicRanges)

# Import chain file
chain <- import.chain("hg19ToHg38.over.chain")

# Create GRanges object from your coordinates
gr <- GRanges(
    seqnames = c("chr17", "chr7", "chr1"),
    ranges = IRanges(
        start = c(41197694, 55086725, 11873),
        end = c(41276113, 55275031, 14409)
    ),
    name = c("BRCA1", "EGFR", "DDX11L1")
)

# Perform liftover
lifted <- liftOver(gr, chain)

# liftOver returns a GRangesList (1:many mapping possible)
# Convert to GRanges (keeping only 1:1 mappings)
lifted_1to1 <- unlist(lifted[elementNROWS(lifted) == 1])

# Check for unmapped
n_unmapped <- sum(elementNROWS(lifted) == 0)
n_multimapped <- sum(elementNROWS(lifted) > 1)
cat(sprintf("Mapped: %d, Unmapped: %d, Multi-mapped: %d\n",
    length(lifted_1to1), n_unmapped, n_multimapped))
```

### Bioconductor Packages for Liftover

| Package | Purpose |
|---------|---------|
| `rtracklayer` | Core liftover functionality |
| `liftOver` (AnnotationHub) | Pre-packaged chain files |
| `GenomicRanges` | GRanges manipulation pre/post liftover |
| `VariantAnnotation` | VCF-aware liftover |

## Expected Loss Rates

| Conversion | Typical Loss | High-Loss Regions | Notes |
|-----------|-------------|------------------|-------|
| hg19 to hg38 | 1–3% | Centromeric, telomeric, segmental duplications | Most reliable conversion |
| hg38 to hg19 | 2–5% | New alt haplotypes, gap-filled regions in hg38 | Higher loss due to new hg38 sequences |
| mm9 to mm10 | 3–5% | Significant rearrangements on multiple chromosomes | Document chromosome-level changes |
| mm10 to mm39 | 1–2% | Minor scaffold updates | Relatively clean conversion |
| mm10 to hg38 | N/A | Cross-species: use synteny, not liftover | Requires different approach (e.g., UCSC synteny maps) |

### When Loss Rates Are Concerning

- **<2% loss**: Normal, proceed with analysis
- **2–5% loss**: Acceptable for most analyses, document in methods
- **5–10% loss**: Investigate — may indicate problematic input regions (many centromeric/repeat-rich regions)
- **>10% loss**: Something is wrong — check assembly mismatch, chromosome naming, or chain file version

## Pitfalls & Edge Cases

- **Unmapped regions are expected**: 1-5% of coordinates typically fail to lift over. Regions near centromeres, telomeres, and assembly gaps are most affected. Always check the unmapped file and report the loss rate.
- **Many-to-one mapping**: Some hg19 regions map to multiple hg38 locations due to assembly improvements. UCSC liftOver reports only one mapping by default — use `-multiple` flag to detect split mappings.
- **Peak coordinates may shift asymmetrically**: Peak summits can shift by different amounts than peak boundaries after liftover. Re-center peaks on summits after conversion rather than trusting the lifted boundaries.
- **Chain file source matters**: Only use chain files from UCSC or Ensembl. Third-party chain files may have different coordinate conventions or incomplete mappings. Verify chain file checksums.
- **VCF liftover requires reference allele check**: After lifting VCF coordinates, the reference allele may no longer match the new assembly. CrossMap handles this with `--refgenome` but UCSC liftOver does not — always validate.
- **Assembly detection is unreliable from filenames**: File names like "peaks.bed" give no assembly hint. Check the actual coordinate ranges against known chromosome sizes. chrM length differs between hg19 (16571) and hg38 (16569).

## Provenance Integration

Log every liftover operation with `encode_log_derived_file` for full reproducibility:

```
encode_log_derived_file(
    file_path="/path/to/lifted_peaks_hg38.bed",
    source_accessions=["ENCSR...", "ENCFF..."],
    description="Lifted [N] narrowPeak regions from hg19 to GRCh38. [X] unmapped ([Y]% loss). Original: [source description]",
    file_type="lifted_coordinates",
    tool_used="UCSC liftOver v377",
    parameters="minMatch=0.95, chain=hg19ToHg38.over.chain.gz (MD5: abc123...), unmapped=[X]/[N] ([Y]%)"
)
```

### Provenance Checklist

Every liftover log entry should include:
- Source file path and assembly
- Chain file used with MD5 checksum
- Tool name and version (e.g., liftOver v377, CrossMap v0.6.4)
- `-minMatch` or equivalent parameter
- Total input regions/variants
- Successfully mapped count
- Unmapped count and percentage
- Multi-mapped count (if applicable)
- Output file path and assembly

## Workflow Summary

```
1. Identify assemblies:  Check input assembly → check target assembly
2. Get chain file:       Download from UCSC → verify MD5
3. Select tool:          BED → liftOver | VCF → CrossMap | single → Ensembl API | R → rtracklayer
4. Convert:              Run liftover with appropriate parameters
5. Check loss:           Count unmapped, flag if >5%
6. Validate:             Verify output assembly, check chromosome names
7. Post-process:         Re-center peaks, normalize VCF, re-annotate genes
8. Log provenance:       Record all parameters, tools, loss rates
```

## Walkthrough: Converting ENCODE Peak Coordinates Between Genome Assemblies

**Goal**: Convert ENCODE BED peak files from hg19 to GRCh38 (or vice versa) for cross-study integration when experiments use different genome builds.
**Context**: Older ENCODE experiments may be aligned to hg19, while newer ones use GRCh38. LiftOver enables coordinate conversion for combined analysis.

### Step 1: Identify experiments needing liftover

```
encode_search_experiments(assay_title="Histone ChIP-seq", organ="liver", target="H3K27ac", organism="Homo sapiens")
```

Expected output:
```json
{
  "total": 8,
  "results": [
    {"accession": "ENCSR100OLD", "assay_title": "Histone ChIP-seq", "assembly": "hg19"},
    {"accession": "ENCSR200NEW", "assay_title": "Histone ChIP-seq", "assembly": "GRCh38"}
  ]
}
```

**Interpretation**: ENCSR100OLD uses hg19 — needs liftover before merging with ENCSR200NEW (GRCh38).

### Step 2: Download the hg19 peak file

```
encode_list_files(accession="ENCSR100OLD", file_format="bed", assembly="hg19")
```

### Step 3: Run UCSC liftOver

```bash
liftOver ENCSR100OLD_peaks.bed hg19ToHg38.over.chain.gz peaks_GRCh38.bed unmapped.bed
```

### Step 4: Check conversion results

Count converted vs. unmapped:
- If >95% convert successfully → proceed with analysis
- If >5% unmapped → investigate (regions may be in assembly-specific contigs)

### Step 5: Log the conversion provenance

```
encode_log_derived_file(
  source_accessions=["ENCFF100OLD"],
  derived_file="/data/peaks_GRCh38.bed",
  description="Lifted from hg19 to GRCh38 using UCSC liftOver",
  tool="liftOver (UCSC, chain: hg19ToHg38.over.chain.gz)"
)
```

### Integration with downstream skills
- Lifted peaks feed into → **histone-aggregation** for cross-assembly union merge
- Conversion provenance logged by → **data-provenance**
- UCSC chain files accessed via → **ucsc-browser** REST API
- Lifted coordinates used by → **variant-annotation** for position-dependent annotation

## Code Examples

### 1. Check file assembly before liftover
```
encode_get_file_info(accession="ENCFF100OLD")
```

Expected output:
```json
{
  "accession": "ENCFF100OLD",
  "assembly": "hg19",
  "file_format": "bed narrowPeak"
}
```

### 2. Find GRCh38 version of same experiment
```
encode_list_files(accession="ENCSR100OLD", file_format="bed", assembly="GRCh38")
```

Expected output:
```json
{
  "files": []
}
```

**Interpretation**: No GRCh38 files available — liftover is required.

### 3. Log liftover provenance
```
encode_log_derived_file(
  source_accessions=["ENCFF100OLD"],
  derived_file="/data/peaks_GRCh38.bed",
  description="hg19→GRCh38 liftOver",
  tool="UCSC liftOver"
)
```

Expected output:
```json
{"status": "logged", "derived_file": "/data/peaks_GRCh38.bed", "source_count": 1}
```

## Related Skills

- `variant-annotation` — Variants often need liftover before annotation with ENCODE data (hg19 GWAS variants to GRCh38)
- `gwas-catalog` — GWAS Catalog coordinates may be in GRCh37; liftover needed for ENCODE GRCh38 integration
- `ensembl-annotation` — Ensembl REST API provides coordinate mapping; Ensembl uses non-chr chromosome naming
- `ucsc-browser` — UCSC provides chain files and the liftOver tool; retrieve assembly-specific tracks
- `gnomad-variants` — gnomAD v4 uses GRCh38; v2 uses GRCh37; liftover needed for cross-version analysis
- `histone-aggregation` — Aggregating peaks across samples requires all peaks in the same assembly
- `accessibility-aggregation` — ATAC-seq/DNase-seq peak union requires assembly-consistent coordinates
- `data-provenance` — Every liftover operation must be logged with chain file, tool version, and loss rate
- `publication-trust` — Verify literature claims backing analytical decisions

## Presenting Results

When reporting liftover results, always present:

- **Input summary**: Number of regions/variants, source assembly
- **Output summary**: Number successfully mapped, target assembly
- **Loss report**: Unmapped count and percentage, with breakdown by reason if available
- **Multi-mapping report**: Number of regions mapping to multiple locations and how they were handled
- **Assembly confirmation**: Explicit statement of output assembly (e.g., "All coordinates are now in GRCh38/hg38")
- **Flag if loss >5%**: Warn the user and investigate the cause (centromeric regions, assembly-specific sequences, or input errors)
- **Chain file version**: Which chain file was used and its source

Example output summary:
```
Liftover: hg19 -> GRCh38
Input:    45,231 narrowPeak regions
Mapped:   44,012 (97.3%)
Unmapped: 1,219 (2.7%) — 847 partially deleted, 312 split, 60 fully deleted
Chain:    hg19ToHg38.over.chain.gz (UCSC, MD5: 7a42e...)
Tool:     UCSC liftOver v377, minMatch=0.95
```

## For the request: "$ARGUMENTS"
