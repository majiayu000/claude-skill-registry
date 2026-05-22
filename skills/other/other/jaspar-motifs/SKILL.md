---
name: jaspar-motifs
description: "Guide for using JASPAR transcription factor binding profiles with ENCODE ChIP-seq data. Use when users need to find TF binding motifs in ENCODE peaks, validate ChIP-seq targets with known motifs, or scan regulatory regions for TF binding potential. Trigger on: JASPAR, motif database, binding profile, PWM, position weight matrix, TF motif, motif enrichment, motif scanning, binding site prediction."
---

# Using JASPAR Transcription Factor Binding Profiles with ENCODE ChIP-seq Data

Integrate JASPAR position weight matrices (PWMs) with ENCODE ChIP-seq peaks to validate TF binding targets, discover co-binding partners, and scan regulatory elements for TF binding potential.

## Scientific Rationale

**The question**: "Does the expected TF binding motif appear in my ENCODE ChIP-seq peaks, and what other TF motifs are enriched?"

ENCODE TF ChIP-seq experiments identify where a transcription factor binds in the genome, but the peak coordinates alone do not confirm direct DNA binding or reveal the binding sequence specificity. JASPAR provides curated position weight matrices (PWMs) — mathematical representations of TF binding preferences — that enable two critical analyses:

1. **Target validation**: If CTCF ChIP-seq peaks are enriched for the CTCF motif (JASPAR MA0139.1), the experiment worked correctly. If they are NOT enriched, something may be wrong with the antibody, crosslinking, or peak calling.

2. **Co-factor discovery**: Motif enrichment analysis in ChIP-seq peaks often reveals motifs for co-binding TFs that were not the ChIP target, uncovering regulatory complexes.

### What JASPAR Provides

- **900+ curated TF binding profiles** across 7 taxonomic groups
- **Position Frequency Matrices (PFMs)**, Position Weight Matrices (PWMs), and sequence logos
- **Multiple profile versions** reflecting binding mode diversity
- **Quality scores** (based on validation evidence)
- **Taxonomic classification** and TF structural class annotation
- **REST API** for programmatic access

### The ENCODE-JASPAR Synergy

| ENCODE provides | JASPAR provides | Together |
|----------------|----------------|---------|
| Where a TF binds (peak coordinates) | How a TF recognizes DNA (binding motif) | Validated binding sites with sequence specificity |
| TF binding in specific tissues | Universal binding preferences | Tissue-specific motif usage |
| Co-occupancy data (multiple ChIP-seq) | Co-factor motif profiles | Regulatory complex architecture |
| Chromatin context (accessibility, marks) | Motif sequence requirements | Context-dependent binding rules |

## Key Literature

- **Castro-Mondragon et al. 2022** "JASPAR 2022: the 9th release of the open-access database of transcription factor binding profiles" (Nucleic Acids Research, ~1,400 citations). The current JASPAR release with 1,956 profiles across 7 taxonomic groups, including unvalidated (UNVALIDATED collection) profiles. Introduced TFBSTools integration and improved REST API. [DOI: 10.1093/nar/gkab1113](https://doi.org/10.1093/nar/gkab1113)
- **Sandelin et al. 2004** "JASPAR: an open-access database for eukaryotic transcription factor binding profiles" (Nucleic Acids Research, ~2,000 citations). The founding JASPAR publication establishing the curated, open-access model for TF binding profiles. [DOI: 10.1093/nar/gkh012](https://doi.org/10.1093/nar/gkh012)
- **Grant et al. 2011** "FIMO: scanning for occurrences of a given motif" (Bioinformatics, ~2,500 citations). FIMO (Find Individual Motif Occurrences) — the standard tool for scanning sequences with PWMs. Part of the MEME Suite. [DOI: 10.1093/bioinformatics/btr064](https://doi.org/10.1093/bioinformatics/btr064)
- **Heinz et al. 2010** "Simple combinations of lineage-determining transcription factors prime cis-regulatory elements required for macrophage and B cell identities" (Molecular Cell, ~5,000 citations). Introduced HOMER motif analysis — the most widely used tool for de novo and known motif enrichment in ChIP-seq peaks. [DOI: 10.1016/j.molcel.2010.05.004](https://doi.org/10.1016/j.molcel.2010.05.004)
- **ENCODE Project Consortium 2020** (Nature, ~1,656 citations). The TF ChIP-seq experiments that JASPAR motifs validate and enrich. [DOI: 10.1038/s41586-020-2493-4](https://doi.org/10.1038/s41586-020-2493-4)

## When to Use This Skill

| Scenario | How JASPAR Helps |
|---------|-----------------|
| Validating ENCODE TF ChIP-seq | Check if target TF motif is enriched in peaks |
| Finding co-binding TFs | Scan peaks for additional enriched motifs |
| Interpreting ENCODE enhancers | Identify which TFs can bind enhancer sequences |
| Variant in TF binding site | Check if variant disrupts a JASPAR motif |
| Comparing TF binding across tissues | Determine if same motif is used in different contexts |
| Planning CRISPR validation | Identify core motif bases to mutate |

## JASPAR REST API Reference

**Base URL**: `https://jaspar.genereg.net/api/v1/`

No authentication required. Responses are JSON.

### Key Endpoints

| Endpoint | Purpose | Key Parameters |
|---------|---------|---------------|
| `/matrix/` | List/search all profiles | `name`, `collection`, `tax_group`, `tf_class` |
| `/matrix/{id}/` | Get specific profile | Matrix ID (e.g., MA0139.1) |
| `/matrix/{id}/?format=pfm` | Get PFM (counts) | — |
| `/matrix/{id}/?format=pwm` | Get PWM (log-odds) | — |
| `/matrix/{id}/?format=jaspar` | Get JASPAR format | — |
| `/matrix/{id}/?format=meme` | Get MEME format | Ready for FIMO scanning |
| `/taxon/` | List taxonomic groups | — |
| `/tfclass/` | List TF structural classes | — |

### Common Matrix IDs for ENCODE TFs

| TF | JASPAR ID | Class | Notes |
|----|----------|-------|-------|
| CTCF | MA0139.1 | C2H2 zinc finger | Most common ENCODE TF ChIP-seq target |
| TP53 (p53) | MA0106.3 | p53 family | Tumor suppressor |
| SP1 | MA0079.5 | C2H2 zinc finger | GC-rich promoter binding |
| FOXA1 | MA0148.4 | Forkhead | Pioneer factor |
| FOXA2 | MA0047.3 | Forkhead | Liver, pancreas |
| HNF4A | MA0114.4 | Nuclear receptor | Hepatocyte-enriched |
| NRF1 | MA0506.2 | bZIP | Mitochondrial regulation |
| REST (NRSF) | MA0138.2 | C2H2 zinc finger | Neuronal gene repressor |
| MYC | MA0147.3 | bHLH | Oncogene, E-box binding |
| JUN (AP-1) | MA0488.1 | bZIP | Immediate early response |
| GATA4 | MA0482.2 | GATA | Cardiac, endoderm |
| PAX6 | MA0069.1 | Paired box | Eye, brain development |

## Step 1: Retrieve ENCODE ChIP-seq Peaks

```
# Find TF ChIP-seq experiments
encode_search_experiments(
    assay_title="TF ChIP-seq",
    target="CTCF",
    organ="pancreas",
    biosample_type="tissue"
)

# Get IDR thresholded peaks (highest confidence)
encode_list_files(
    experiment_accession="ENCSR...",
    file_format="bed",
    output_type="IDR thresholded peaks",
    assembly="GRCh38",
    preferred_default=True
)
```

Track the experiment:
```
encode_track_experiment(accession="ENCSR...", notes="CTCF ChIP-seq for motif analysis")
```

## Step 2: Get JASPAR Motif Profiles

### Query by TF Name

```python
import requests

def get_jaspar_matrix(tf_name, tax_group="vertebrates", collection="CORE"):
    """Get JASPAR matrix for a TF."""
    url = "https://jaspar.genereg.net/api/v1/matrix/"
    params = {
        "name": tf_name,
        "tax_group": tax_group,
        "collection": collection,
        "format": "json"
    }
    response = requests.get(url, params=params)
    results = response.json()["results"]
    if results:
        # Return the highest-version profile
        return sorted(results, key=lambda x: x["version"], reverse=True)[0]
    return None

ctcf_profile = get_jaspar_matrix("CTCF")
print(f"ID: {ctcf_profile['matrix_id']}, Version: {ctcf_profile['version']}")
```

### Get the Position Frequency Matrix (PFM)

```python
def get_pfm(matrix_id):
    """Get Position Frequency Matrix from JASPAR."""
    url = f"https://jaspar.genereg.net/api/v1/matrix/{matrix_id}/"
    params = {"format": "json"}
    response = requests.get(url, params=params)
    data = response.json()
    pfm = data["pfm"]
    # pfm is a dict with keys A, C, G, T, each a list of counts per position
    return pfm

pfm = get_pfm("MA0139.1")
print(f"Motif length: {len(pfm['A'])} bp")
for base in ["A", "C", "G", "T"]:
    print(f"{base}: {pfm[base]}")
```

### Get MEME Format (for FIMO Scanning)

```python
def get_meme_format(matrix_id):
    """Get motif in MEME format for use with FIMO."""
    url = f"https://jaspar.genereg.net/api/v1/matrix/{matrix_id}/"
    params = {"format": "meme"}
    response = requests.get(url, params=params)
    return response.text

meme_motif = get_meme_format("MA0139.1")
# Save to file for FIMO input
with open("ctcf_motif.meme", "w") as f:
    f.write(meme_motif)
```

## Step 3: Extract Peak Sequences

Before scanning for motifs, extract the DNA sequences underlying ENCODE peaks.

### Using bedtools getfasta

```bash
# Download reference genome (if not available)
# GRCh38: https://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/hg38.fa.gz

# Extract sequences from ENCODE peak regions
# Use summit +/- 100bp for narrow peaks (better motif enrichment)
awk 'BEGIN{OFS="\t"} {mid=int(($2+$3)/2); print $1, mid-100, mid+100, $4}' \
    encode_peaks.bed > peak_summits_200bp.bed

bedtools getfasta \
    -fi hg38.fa \
    -bed peak_summits_200bp.bed \
    -fo peak_sequences.fa
```

### Summit-Centered Extraction

For motif analysis, center on peak summits (column 10 in narrowPeak format):

```bash
# narrowPeak summit is relative to peak start (column 10)
awk 'BEGIN{OFS="\t"} {summit=$2+$10; print $1, summit-100, summit+100, $4}' \
    encode_narrowpeak.bed > summit_regions.bed
```

## Step 4: Motif Scanning and Enrichment

### Option A: FIMO (Individual Motif Occurrences)

FIMO scans sequences for individual occurrences of a given motif.

```bash
# Scan peak sequences for CTCF motif
fimo --thresh 1e-4 \
     --oc fimo_output/ \
     ctcf_motif.meme \
     peak_sequences.fa

# Output: fimo_output/fimo.tsv with columns:
# motif_id, motif_alt_id, sequence_name, start, stop, strand, score, p-value, q-value, matched_sequence
```

### Option B: HOMER (Known and De Novo Motif Enrichment)

HOMER findMotifsGenome.pl is the most popular tool for ChIP-seq motif analysis.

```bash
# Known motif enrichment
findMotifsGenome.pl \
    encode_peaks.bed \
    hg38 \
    homer_output/ \
    -size 200 \
    -mask \
    -p 4

# Output includes:
# knownResults.html — enrichment of known motifs (including JASPAR)
# homerResults.html — de novo discovered motifs
```

### Option C: MEME-ChIP (Comprehensive Suite)

```bash
# Full motif analysis pipeline
meme-chip \
    -oc meme_output/ \
    -db JASPAR2022_CORE_vertebrates.meme \
    peak_sequences.fa
```

### Interpreting Enrichment Results

| Enrichment Result | Interpretation |
|------------------|----------------|
| Target TF motif ranked #1 with p < 1e-100 | Excellent — ChIP-seq validated |
| Target TF motif ranked #1 but p only 1e-5 | Moderate — may indicate indirect binding or weak motif |
| Target TF motif NOT in top 10 | Concerning — may indicate antibody cross-reactivity, indirect binding, or wrong motif version |
| Unexpected TF motif ranked #1 | May indicate co-factor or pioneer factor binding |
| Multiple TF motifs highly enriched | Regulatory hub — multiple TFs co-bind |

## Step 5: Variant Impact on TF Motifs

When a variant falls within an ENCODE TF ChIP-seq peak, check whether it disrupts the underlying motif.

### Motif Disruption Analysis

```python
import numpy as np

def score_sequence(sequence, pwm):
    """Score a sequence against a PWM (log-odds)."""
    base_to_idx = {"A": 0, "C": 1, "G": 2, "T": 3}
    score = 0
    for i, base in enumerate(sequence.upper()):
        if base in base_to_idx:
            score += pwm[base][i]
    return score

def variant_motif_impact(ref_seq, alt_seq, pwm):
    """Calculate motif score change from variant."""
    ref_score = score_sequence(ref_seq, pwm)
    alt_score = score_sequence(alt_seq, pwm)
    delta = alt_score - ref_score
    return {
        "ref_score": ref_score,
        "alt_score": alt_score,
        "delta_score": delta,
        "disrupted": delta < -2  # Threshold: >2 log-odds decrease
    }
```

### Using motifbreakR (R Package)

```r
library(motifbreakR)
library(BSgenome.Hsapiens.UCSC.hg38)

# Define variant
variant <- snps.from.rsid(
    rsid = "rs7903146",
    dbSNP = SNPlocs.Hsapiens.dbSNP155.GRCh38
)

# Scan against JASPAR motifs
results <- motifbreakR(
    snpList = variant,
    filterp = TRUE,
    pwmList = MotifDb,
    threshold = 1e-4,
    method = "log",
    bkg = c(A=0.25, C=0.25, G=0.25, T=0.25),
    show.neutral = FALSE
)
```

## Step 6: Multi-TF Co-Binding Analysis

ENCODE often has ChIP-seq for multiple TFs in the same biosample. JASPAR motifs can reveal co-binding logic.

### Workflow

1. Get all TF ChIP-seq peaks for a biosample:
```
encode_search_experiments(
    assay_title="TF ChIP-seq",
    biosample_term_name="K562"
)
```

2. Find peaks shared by multiple TFs (co-occupied regions)
3. Scan co-occupied peaks for JASPAR motifs to identify the binding grammar
4. Grammar example: GATA motif + TAL1 motif within 50bp = erythroid enhancer

### Motif Spacing Analysis

TF cooperativity often requires specific motif spacing:

```bash
# Find GATA and TAL1 motifs in co-occupied peaks
fimo --thresh 1e-4 gata_motif.meme cooccupied_peaks.fa > gata_hits.tsv
fimo --thresh 1e-4 tal1_motif.meme cooccupied_peaks.fa > tal1_hits.tsv

# Analyze spacing between GATA and TAL1 motifs in same peaks
# Characteristic spacing indicates cooperative binding
```

## Step 7: Present Results

### Target Validation Table

| TF ChIP-seq | Target Motif | JASPAR ID | Enrichment p-value | % Peaks with Motif | Validation |
|-------------|-------------|----------|-------------------|-------------------|-----------|
| CTCF | CTCF | MA0139.1 | 1e-2456 | 78% | Strong |
| FOXA2 | FOXA2 | MA0047.3 | 1e-345 | 45% | Strong |
| HNF4A | HNF4A | MA0114.4 | 1e-189 | 52% | Strong |
| EP300 | No specific motif | — | — | — | Expected (coactivator) |

### Co-Factor Discovery Table

| TF ChIP-seq Target | Unexpected Enriched Motif | JASPAR ID | p-value | Interpretation |
|-------------------|-------------------------|----------|---------|---------------|
| HNF4A in liver | FOXA2 | MA0047.3 | 1e-78 | Known co-binding at liver enhancers |
| GATA1 in K562 | TAL1 | MA0140.2 | 1e-234 | Erythroid TF complex |
| TP53 | SP1 | MA0079.5 | 1e-12 | Co-regulation at GC-rich promoters |

## Pitfalls & Edge Cases

- **Motif similarity causes false matches**: Many TF families share similar motifs (e.g., all bHLH factors bind E-boxes). A JASPAR motif match does not prove which specific family member is binding. Combine with ChIP-seq evidence.
- **PWM score thresholds are arbitrary**: JASPAR motifs use position weight matrices but the "significant" score threshold varies by motif length and information content. Use relative scores (>80% of max) rather than absolute cutoffs.
- **Redundant motifs in JASPAR**: JASPAR contains multiple profiles for the same TF from different studies. These profiles may have different quality. Prefer the most recent version and check the data source (ChIP-seq > SELEX > PBM).
- **GC content bias in background model**: Motif enrichment depends heavily on the background model. Genomic sequence, shuffled peaks, and matched random regions give very different p-values. Always use matched GC-content background.
- **Motif presence ≠ binding**: A genomic sequence matching a JASPAR PWM does not mean the TF actually binds there. Chromatin accessibility, co-factor availability, and DNA methylation all modulate binding. Validate with ChIP-seq or ATAC-seq footprinting.
- **Species-specific motifs**: JASPAR motifs are often derived from one species. A mouse-derived motif may not perfectly represent the human TF binding preference. Check the taxon field when using motifs across species.

## Walkthrough: Identifying Transcription Factor Binding Motifs in ENCODE Enhancers

**Goal**: Scan ENCODE-defined enhancer peaks for enriched transcription factor binding motifs using the JASPAR database to predict which TFs regulate enhancer activity.
**Context**: ENCODE H3K27ac peaks mark active enhancers, but don't reveal which TFs bind there. JASPAR motif scanning predicts TF occupancy.

### Step 1: Find H3K27ac enhancer experiments

```
encode_search_experiments(assay_title="Histone ChIP-seq", organ="liver", target="H3K27ac", organism="Homo sapiens")
```

Expected output:
```json
{
  "total": 6,
  "results": [
    {"accession": "ENCSR100LIV", "assay_title": "Histone ChIP-seq", "target": "H3K27ac", "biosample_summary": "liver"}
  ]
}
```

### Step 2: Download enhancer peak files

```
encode_list_files(accession="ENCSR100LIV", file_format="bed", output_type="IDR thresholded peaks", assembly="GRCh38")
```

Expected output:
```json
{
  "files": [
    {"accession": "ENCFF150ENH", "output_type": "IDR thresholded peaks", "file_format": "bed narrowPeak", "file_size_mb": 1.1}
  ]
}
```

### Step 3: Query JASPAR for liver-relevant TF motifs

Using JASPAR REST API (via skill guidance):
```
GET https://jaspar.elixir.no/api/v2/matrix/?tax_id=9606&collection=CORE&profile_class=liver
```

Key liver TFs and their JASPAR matrix IDs:
- HNF4A (MA0114.4) — master hepatocyte TF
- CEBPA (MA0102.4) — liver differentiation
- FOXA2 (MA0047.3) — pioneer factor for liver enhancers

### Step 4: Scan enhancer peaks for motif enrichment

```bash
# Extract sequences under peaks
bedtools getfasta -fi GRCh38.fa -bed ENCFF150ENH.bed -fo enhancer_seqs.fa

# Scan with MEME/FIMO using JASPAR motifs
fimo --thresh 1e-4 JASPAR_liver_motifs.meme enhancer_seqs.fa > motif_hits.tsv
```

**Interpretation**: If HNF4A motifs are enriched 5× over background in liver enhancers, this confirms HNF4A as a key driver. Unexpected motifs (e.g., TP53) may suggest stress response enhancers.

### Step 5: Validate with ENCODE TF ChIP-seq

```
encode_search_experiments(assay_title="TF ChIP-seq", organ="liver", target="HNF4A", organism="Homo sapiens")
```

Expected output:
```json
{
  "total": 3,
  "results": [
    {"accession": "ENCSR200HNF", "assay_title": "TF ChIP-seq", "target": "HNF4A", "biosample_summary": "liver"}
  ]
}
```

**Interpretation**: If JASPAR-predicted HNF4A motif sites overlap actual HNF4A ChIP-seq peaks → validated motif prediction.

### Integration with downstream skills
- Enhancer peaks from → **peak-annotation** provide regions for motif scanning
- Motif-predicted TFs validated against → **motif-analysis** de novo motif discovery
- TF binding predictions inform → **regulatory-elements** enhancer classification
- Predicted TF-enhancer links feed into → **disease-research** for TF-disease connections

## Code Examples

### 1. Find TF ChIP-seq to validate motif predictions
```
encode_get_facets(assay_title="TF ChIP-seq", facet_field="target.label", organ="liver", organism="Homo sapiens")
```

Expected output:
```json
{
  "facets": {
    "target.label": {"HNF4A": 3, "CEBPA": 2, "FOXA2": 2, "RXRA": 2, "TP53": 1}
  }
}
```

### 2. Compare predicted vs. observed TF binding
```
encode_compare_experiments(accession_1="ENCSR100LIV", accession_2="ENCSR200HNF")
```

Expected output:
```json
{
  "comparison": {
    "shared": {"organ": "liver", "organism": "Homo sapiens", "assembly": "GRCh38"},
    "differences": {
      "assay": ["Histone ChIP-seq", "TF ChIP-seq"],
      "target": ["H3K27ac", "HNF4A"]
    }
  }
}
```

### 3. Track motif analysis experiments
```
encode_track_experiment(accession="ENCSR100LIV", notes="Liver H3K27ac for JASPAR motif scanning - HNF4A/CEBPA/FOXA2")
```

Expected output:
```json
{
  "status": "tracked",
  "accession": "ENCSR100LIV",
  "notes": "Liver H3K27ac for JASPAR motif scanning - HNF4A/CEBPA/FOXA2"
}
```

## Integration

| This skill produces... | Feed into... | Purpose |
|---|---|---|
| TF motif enrichment scores | **motif-analysis** | Compare JASPAR database motifs with de novo discovered motifs |
| Predicted TF binding sites | **peak-annotation** | Annotate enhancer peaks with predicted TF regulators |
| TF-enhancer regulatory links | **regulatory-elements** | Classify enhancers by predicted TF driver identity |
| Motif-disrupting variant positions | **variant-annotation** | Identify SNPs that alter TF binding motifs |
| Tissue-specific TF motif profiles | **compare-biosamples** | Compare TF regulatory programs between tissues |
| TF binding predictions | **disease-research** | Connect TF motif disruption to disease mechanisms |
| Motif scanning results | **visualization-workflow** | Generate motif logos and enrichment heatmaps |
| Validated TF-target pairs | **gtex-expression** | Check TF expression in tissue via GTEx |

## Presenting Results

When reporting JASPAR motif scanning results:

- **Motif hit table**: Present a table with columns: TF_name, matrix_id (e.g., MA0139.1), p-value, score, genomic_location (chr:start-end), strand, and matched_sequence
- **Always report**: JASPAR version (e.g., JASPAR 2024), scanning tool and version (FIMO, MOODS, or PWMScan), p-value threshold used, and genome assembly scanned
- **Key fields to include**: Total regions scanned, number of motif hits passing threshold, number of unique TFs with hits, and whether repeat masking was applied
- **Context to provide**: Emphasize that motif presence does not guarantee TF binding in vivo -- chromatin accessibility (ATAC-seq/DNase-seq) and actual TF occupancy (ChIP-seq) from ENCODE provide essential validation layers
- **Enrichment context**: If testing for enrichment over background, report the background model (genome-wide, GC-matched, shuffled), fold enrichment, and statistical test used
- **Next steps**: Suggest `motif-analysis` for de novo motif discovery with HOMER/MEME, or `regulatory-elements` to characterize the ENCODE regulatory elements containing the motif hits

## Related Skills

- `regulatory-elements` — Characterizing ENCODE regulatory elements that motifs help annotate
- `epigenome-profiling` — Building tissue epigenomic profiles including TF binding landscapes
- `variant-annotation` — Assessing whether variants disrupt TF binding motifs in ENCODE peaks
- `compare-biosamples` — Comparing TF binding and motif usage across ENCODE biosamples
- `quality-assessment` — Using motif enrichment as a quality control metric for TF ChIP-seq
- `gwas-catalog` — GWAS variants that disrupt TF motifs in ENCODE peaks
- `publication-trust` — Verify literature claims backing analytical decisions

## For the request: "$ARGUMENTS"
