---
name: clinvar-annotation
description: "Guide for annotating ENCODE regulatory variants with ClinVar clinical significance. Use when users need to check if variants in ENCODE peaks have clinical associations, find pathogenic variants in regulatory regions, or assess variant clinical impact. Trigger on: ClinVar, clinical significance, pathogenic variant, variant classification, clinical variant, disease variant, VUS, benign, likely pathogenic."
---

## When to Use

- User wants to check if variants in ENCODE regulatory peaks have clinical significance in ClinVar
- User asks about "ClinVar", "pathogenic variants", "clinical significance", or "variant classification"
- User needs to annotate ENCODE-derived regulatory variants with disease associations
- User wants to find clinically relevant variants within enhancers, promoters, or open chromatin regions
- Example queries: "check ClinVar for variants in my ATAC-seq peaks", "find pathogenic variants in pancreas enhancers", "annotate regulatory variants with clinical significance"

# Annotating ENCODE Regulatory Variants with ClinVar Clinical Significance

Cross-reference ENCODE functional genomic elements with ClinVar clinical variant classifications to identify pathogenic variants in regulatory regions and understand non-coding disease mechanisms.

## Scientific Rationale

**The question**: "Do any clinically significant variants fall within my ENCODE regulatory elements, and can ENCODE data explain their pathogenic mechanism?"

ClinVar is NCBI's public archive of variant-disease associations, aggregating submissions from clinical laboratories, research groups, and expert panels. Most ClinVar annotations focus on coding variants, but a growing number of non-coding variants are being classified. ENCODE provides the functional context to explain WHY a non-coding variant is pathogenic — by showing that it disrupts an active enhancer, promoter, or insulator in disease-relevant tissue.

This bidirectional integration serves two use cases:
1. **Forward**: Start from ENCODE peaks, find clinically significant variants within them
2. **Reverse**: Start from ClinVar pathogenic variants, use ENCODE to explain their mechanism

### The Non-Coding Variant Challenge

- ~90% of GWAS-associated variants are in non-coding regions (Maurano et al. 2012)
- ClinVar increasingly includes non-coding variants, but most lack mechanistic annotation
- ENCODE regulatory annotations provide the "why" behind non-coding pathogenicity
- A variant classified as VUS (variant of uncertain significance) may be reclassified with ENCODE functional evidence

## Key Literature

- **Landrum et al. 2018** "ClinVar: improving access to variant interpretations and supporting evidence" (Nucleic Acids Research, ~2,000 citations). Describes the ClinVar database architecture, submission standards, and the star-rating review system for variant classifications. [DOI: 10.1093/nar/gkx1153](https://doi.org/10.1093/nar/gkx1153)
- **Riggs et al. 2020** "Technical standards for the interpretation and reporting of constitutional copy-number variants: a joint consensus recommendation of the ACMG and ClinGen" (Genetics in Medicine, ~500 citations). Framework for interpreting structural variants, relevant when ENCODE elements overlap CNVs. [DOI: 10.1038/s41436-019-0686-8](https://doi.org/10.1038/s41436-019-0686-8)
- **Richards et al. 2015** "Standards and guidelines for the interpretation of sequence variants: ACMG/AMP joint consensus recommendation" (Genetics in Medicine, ~12,000 citations). The ACMG variant classification framework (pathogenic through benign). ENCODE functional data can provide evidence for PS3/BS3 (functional studies) criteria. [DOI: 10.1038/gim.2015.30](https://doi.org/10.1038/gim.2015.30)
- **ENCODE Project Consortium 2020** (Nature, ~1,656 citations). Registry of 926,535 human cCREs — the functional annotation layer for interpreting non-coding ClinVar variants. [DOI: 10.1038/s41586-020-2493-4](https://doi.org/10.1038/s41586-020-2493-4)

## ClinVar Clinical Significance Categories

| Classification | Meaning | ENCODE Relevance |
|---------------|---------|-----------------|
| **Pathogenic** | Causes disease | If in regulatory region, ENCODE explains mechanism |
| **Likely pathogenic** | Strong evidence for disease causation | ENCODE data may upgrade to pathogenic |
| **Uncertain significance (VUS)** | Not enough evidence to classify | ENCODE functional data may help resolve |
| **Likely benign** | Strong evidence against pathogenicity | — |
| **Benign** | Does not cause disease | — |
| **Conflicting interpretations** | Labs disagree on classification | ENCODE data may resolve conflict |
| **Risk factor** | Increases disease risk | May overlap ENCODE regulatory elements |

### ClinVar Star Ratings

| Stars | Review Status | Confidence |
|-------|-------------|-----------|
| 0 | No assertion criteria | Very low — treat with caution |
| 1 | Single submitter with criteria | Low-moderate |
| 2 | Multiple submitters, no conflict | Moderate |
| 3 | Expert panel reviewed | High |
| 4 | Practice guideline | Highest |

**Always check star ratings.** A 0-star "pathogenic" classification has very different reliability than a 3-star classification.

## NCBI E-utilities API Reference

**Base URL**: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/`

No authentication required for low-volume use. Rate limit: 3 requests/second without API key, 10/second with NCBI API key.

### Key Endpoints

| Endpoint | Purpose | Example |
|---------|---------|---------|
| `esearch.fcgi?db=clinvar&term=...` | Search ClinVar | Search by gene, variant, condition |
| `efetch.fcgi?db=clinvar&id=...` | Fetch full record | Get complete variant details |
| `esummary.fcgi?db=clinvar&id=...` | Summary record | Get classification, review status |
| `elink.fcgi?db=clinvar&dbfrom=...` | Cross-database links | Link to PubMed, Gene, etc. |

### ClinVar VCF Downloads

For bulk intersection with ENCODE peaks, download the ClinVar VCF:
- GRCh38: `https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/clinvar.vcf.gz`
- GRCh37: `https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh37/clinvar.vcf.gz`

Updated monthly on the first Thursday.

## Step 1: Define the Scope

Determine which direction the analysis runs:

### Forward: ENCODE Peaks to ClinVar Variants

Starting from ENCODE regulatory elements, find clinically significant variants within them.

```
# Get ENCODE peaks for target tissue
encode_search_experiments(
    assay_title="Histone ChIP-seq",
    target="H3K27ac",
    organ="pancreas",
    biosample_type="tissue"
)

encode_list_files(
    experiment_accession="ENCSR...",
    file_format="bed",
    output_type="IDR thresholded peaks",
    assembly="GRCh38"
)
```

### Reverse: ClinVar Variants to ENCODE Context

Starting from ClinVar pathogenic variants, determine if they overlap ENCODE regulatory elements.

```python
import requests

# Search ClinVar for pathogenic variants in a gene
url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
params = {
    "db": "clinvar",
    "term": "INS[gene] AND pathogenic[clinical significance]",
    "retmax": 50,
    "retmode": "json"
}
response = requests.get(url, params=params)
result = response.json()
variant_ids = result["esearchresult"]["idlist"]
```

## Step 2: Query ClinVar via E-utilities

### Search for Variants by Gene

```python
import requests
import time

def search_clinvar(gene_symbol, significance="pathogenic"):
    """Search ClinVar for variants in a gene with given clinical significance."""
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    term = f"{gene_symbol}[gene] AND {significance}[clinical significance]"
    params = {
        "db": "clinvar",
        "term": term,
        "retmax": 100,
        "retmode": "json"
    }
    response = requests.get(url, params=params)
    time.sleep(0.34)  # Rate limit: 3/sec
    return response.json()["esearchresult"]["idlist"]
```

### Get Variant Details

```python
def get_clinvar_summary(variant_ids):
    """Get summary for ClinVar variant IDs."""
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
    params = {
        "db": "clinvar",
        "id": ",".join(variant_ids[:20]),  # Max 20 per request
        "retmode": "json"
    }
    response = requests.get(url, params=params)
    time.sleep(0.34)
    return response.json()["result"]
```

### Search by Genomic Region

```python
# Search for ClinVar variants in a specific genomic region (GRCh38)
term = "11[chromosome] AND 2159000:2162000[chrpos38] AND pathogenic[clinical significance]"
```

## Step 3: Intersect ClinVar with ENCODE Peaks

### Using bedtools (Command Line)

```bash
# Download ClinVar VCF (GRCh38)
wget https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/clinvar.vcf.gz
wget https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/clinvar.vcf.gz.tbi

# Filter to pathogenic/likely pathogenic only
bcftools view -i 'INFO/CLNSIG~"Pathogenic" || INFO/CLNSIG~"Likely_pathogenic"' \
    clinvar.vcf.gz | \
    bcftools query -f '%CHROM\t%POS0\t%END\t%ID\t%INFO/CLNSIG\t%INFO/CLNDN\n' \
    > clinvar_pathogenic.bed

# Intersect with ENCODE peaks
# NOTE: ClinVar VCF is 1-based, BED is 0-based — bcftools query with %POS0 handles this
bedtools intersect \
    -a clinvar_pathogenic.bed \
    -b encode_h3k27ac_peaks.bed \
    -wa -wb \
    > clinvar_in_encode_enhancers.bed
```

### Using Python

```python
import pysam

# Open ClinVar VCF
vcf = pysam.VariantFile("clinvar.vcf.gz")

# Define ENCODE peak region (0-based)
chrom, start, end = "chr11", 2159000, 2162000

# Find ClinVar variants in region
for record in vcf.fetch(chrom, start, end):
    clnsig = record.info.get("CLNSIG", [])
    clndn = record.info.get("CLNDN", [])
    print(f"{record.chrom}:{record.pos} {record.ref}>{record.alts} "
          f"Significance: {clnsig} Condition: {clndn}")
```

## Step 4: Classify the Regulatory Impact

For each ClinVar variant overlapping an ENCODE element, assess the regulatory impact:

### Impact Classification Framework

| ClinVar Variant in... | ENCODE Context | Interpretation |
|----------------------|---------------|----------------|
| Active enhancer (H3K27ac+) | Tissue-specific, near disease gene | High impact — variant may disrupt enhancer |
| Active promoter (H3K4me3+) | At TSS of disease gene | High impact — variant may affect transcription initiation |
| CTCF binding site | TAD boundary | High impact — may disrupt chromatin insulation |
| Open chromatin only (ATAC+) | No histone marks | Moderate — accessible but function unclear |
| TF binding site | Specific TF known for disease gene | High impact — may disrupt TF binding |
| No ENCODE overlap | Not in regulatory element | Mechanism may be coding, splicing, or untested tissue |

### ACMG Evidence Integration

ENCODE functional data can support ACMG criteria for variant classification:

| ACMG Criterion | How ENCODE Data Contributes |
|---------------|----------------------------|
| PS3 (Functional studies) | ENCODE shows variant disrupts active regulatory element |
| PM1 (Critical domain) | Variant in a regulatory element active in disease tissue |
| PP3 (Computational evidence) | Multiple ENCODE annotations converge on regulatory disruption |
| BS3 (No functional impact) | ENCODE shows region is inactive in all relevant tissues |

## Step 5: Report Findings

### Per-Variant Summary Table

| Variant | ClinVar ID | Classification | Stars | Condition | ENCODE Overlap | Tissue Active | Impact |
|---------|-----------|---------------|-------|----------|---------------|--------------|--------|
| chr11:2160994 A>G | VCV000012345 | Pathogenic | 3 | Neonatal diabetes | H3K27ac enhancer | Pancreas | High |
| chr7:87654321 C>T | VCV000067890 | VUS | 1 | Cystic fibrosis | ATAC-seq peak | Lung | Moderate |

### Summary Statistics

Report:
- Total ClinVar variants in region/gene
- Number overlapping ENCODE regulatory elements (by element type)
- Breakdown by clinical significance
- Star rating distribution
- Tissues with ENCODE data used

## Step 6: Log Provenance

```
encode_log_derived_file(
    file_path="/path/to/clinvar_encode_intersection.tsv",
    source_accessions=["ENCSR...", "ENCSR..."],
    description="Intersection of ClinVar pathogenic variants with ENCODE H3K27ac and ATAC-seq peaks in pancreas",
    file_type="variant_annotation",
    tool_used="bedtools intersect + ClinVar VCF (2024-01 release)",
    parameters="GRCh38, pathogenic+likely_pathogenic, IDR thresholded peaks"
)

encode_link_reference(
    experiment_accession="ENCSR...",
    reference_type="other",
    reference_id="ClinVar:VCV000012345",
    description="Pathogenic variant for neonatal diabetes overlapping pancreas enhancer"
)
```

## Pitfalls & Edge Cases

- **ClinVar classifications change over time**: A variant classified as VUS today may be reclassified as pathogenic tomorrow. Always record the ClinVar version/date when annotating variants. Re-check classifications before publication.
- **Star rating indicates review quality**: ClinVar uses a 0-4 star system for assertion confidence. Single-submitter entries (1 star) may conflict with expert panel reviews (3-4 stars). Always prefer higher star ratings.
- **Coordinate system mismatch**: ClinVar uses 1-based coordinates while BED files are 0-based. Off-by-one errors when intersecting ClinVar with ENCODE peaks are extremely common. Always convert before comparison.
- **Regulatory variants are underrepresented**: ClinVar is heavily biased toward coding and splice-site variants. Absence of a regulatory variant in ClinVar does NOT mean it is benign — it likely has not been assessed.
- **Multiple classifications for the same variant**: Different submitters may classify the same variant differently (one says pathogenic, another says benign). Check the "conflicting interpretations" flag and review individual submissions.
- **GRCh37 vs GRCh38 in ClinVar**: ClinVar provides coordinates in both assemblies but some older submissions only have GRCh37. Always specify the assembly when downloading and verify coordinate consistency.

## Walkthrough: Annotating ENCODE Regulatory Variants with Clinical Significance

**Goal**: Cross-reference variants in ENCODE-defined regulatory elements with ClinVar clinical significance to identify non-coding variants with known disease associations.
**Context**: Most GWAS hits fall in non-coding regions. ENCODE maps the regulatory landscape; ClinVar provides clinical interpretation.

### Step 1: Find regulatory element experiments

```
encode_search_experiments(assay_title="ATAC-seq", organ="heart", organism="Homo sapiens")
```

Expected output:
```json
{
  "total": 18,
  "results": [
    {"accession": "ENCSR789HRT", "assay_title": "ATAC-seq", "biosample_summary": "heart left ventricle", "status": "released"}
  ]
}
```

### Step 2: Download peak files for regulatory regions

```
encode_list_files(accession="ENCSR789HRT", file_format="bed", output_type="IDR thresholded peaks", assembly="GRCh38")
```

Expected output:
```json
{
  "files": [
    {"accession": "ENCFF101ATK", "output_type": "IDR thresholded peaks", "file_format": "bed narrowPeak", "file_size_mb": 0.8}
  ]
}
```

### Step 3: Query ClinVar for variants in peaks

Using ClinVar E-utilities (via skill guidance):
```
GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=clinvar&term=chr1[chr]+AND+10000:20000[chrpos]+AND+pathogenic[clnsig]
```

Expected response:
```json
{
  "esearchresult": {
    "count": "3",
    "idlist": ["12345", "67890", "11111"]
  }
}
```

### Step 4: Interpret clinical significance in regulatory context

For each ClinVar variant in an ENCODE peak:
- **Pathogenic/Likely pathogenic** in a heart ATAC-seq peak = high-confidence disease-regulatory variant
- **VUS (Variant of Uncertain Significance)** in an active enhancer = candidate for functional validation
- **Benign** in an open chromatin region = regulatory region tolerates this variant

**Interpretation**: Non-coding pathogenic variants in heart-specific open chromatin suggest regulatory disruption of cardiac gene expression. These are candidates for CRISPR validation.

### Integration with downstream skills
- ENCODE peaks from **regulatory-elements** define the regions to query in ClinVar
- Clinical variants feed into **variant-annotation** for comprehensive annotation
- Pathogenic regulatory variants inform **disease-research** for mechanism studies
- Population frequencies from **gnomad-variants** contextualize ClinVar findings

## Code Examples

### 1. Find ENCODE regulatory data matching ClinVar tissue
```
encode_get_facets(facet_field="organ", assay_title="ATAC-seq", organism="Homo sapiens")
```

Expected output:
```json
{
  "facets": {
    "organ": {"brain": 32, "heart": 18, "liver": 14, "lung": 10, "kidney": 8}
  }
}
```

### 2. Get experiment details for quality check
```
encode_get_experiment(accession="ENCSR789HRT")
```

Expected output:
```json
{
  "accession": "ENCSR789HRT",
  "assay_title": "ATAC-seq",
  "biosample_summary": "heart left ventricle",
  "replicates": 2,
  "status": "released",
  "audit": {"WARNING": 0, "ERROR": 0}
}
```

### 3. Track experiments used for clinical annotation
```
encode_track_experiment(accession="ENCSR789HRT", notes="Heart ATAC-seq for ClinVar regulatory variant annotation")
```

Expected output:
```json
{
  "status": "tracked",
  "accession": "ENCSR789HRT",
  "notes": "Heart ATAC-seq for ClinVar regulatory variant annotation"
}
```

## Integration

| This skill produces... | Feed into... | Purpose |
|---|---|---|
| Clinical variant annotations | **variant-annotation** | Comprehensive variant annotation with clinical significance |
| Pathogenic regulatory variants | **disease-research** | Connect non-coding variants to disease mechanisms |
| ClinVar gene-disease associations | **peak-annotation** | Prioritize peaks near clinically relevant genes |
| Variant pathogenicity scores | **gwas-catalog** | Overlay GWAS hits with ClinVar clinical evidence |
| Regulatory variant coordinates | **gnomad-variants** | Add population frequency context to clinical variants |
| Tissue-specific clinical variants | **gtex-expression** | Check expression of genes near pathogenic regulatory variants |
| Clinical regulatory elements | **regulatory-elements** | Classify ClinVar-annotated elements by regulatory function |

## Presenting Results

When reporting ClinVar annotation results:

- **Variant table**: Present a table with columns: variant_id (rsID or HGVS), clinical_significance, review_status, star_rating (0-4), condition(s), and whether the variant overlaps an ENCODE peak
- **Always report**: ClinVar release date used, genome assembly (must be GRCh38 for ENCODE compatibility), total variants queried, and number with ClinVar entries vs no entry
- **Key fields to include**: Number of pathogenic/likely pathogenic variants in regulatory regions, number of VUS that overlap active enhancers or promoters, and the breakdown by clinical significance category
- **Context to provide**: Note that absence from ClinVar does not imply benign status (especially for non-coding variants), and that ClinVar classifications change monthly as new evidence accumulates
- **Star rating guidance**: Emphasize that 0-1 star variants have limited review and should be interpreted cautiously; 2+ stars indicate multiple submitters with concordant interpretation
- **Next steps**: Suggest `gnomad-variants` for population frequency context, or `variant-annotation` for a full ENCODE-based regulatory variant prioritization workflow

## Related Skills

- `variant-annotation` — Full ENCODE variant annotation workflow with prioritization scoring
- `gwas-catalog` — GWAS variants in ENCODE peaks (population-level associations)
- `gnomad-variants` — Population frequency context for ClinVar variants
- `disease-research` — Disease-focused ENCODE analysis workflows
- `cross-reference` — Linking ENCODE experiments to ClinVar and other databases
- `regulatory-elements` — Characterizing the regulatory elements disrupted by variants
- `publication-trust` — Verify literature claims backing analytical decisions

## For the request: "$ARGUMENTS"
