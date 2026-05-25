---
name: gwas-catalog
description: "Guide for integrating NHGRI-EBI GWAS Catalog associations with ENCODE regulatory data. Use when users need to find GWAS variants in ENCODE peaks, connect regulatory elements to disease associations, or prioritize functional variants using ENCODE annotations. Trigger on: GWAS, genome-wide association, SNP association, trait association, GWAS Catalog, disease association, risk variant, lead SNP, LD proxy."
---

# Integrating NHGRI-EBI GWAS Catalog with ENCODE Regulatory Data

## When to Use

- User wants to intersect ENCODE regulatory elements with GWAS-associated variants
- User asks about "GWAS", "genome-wide association", "disease variants", or "trait-associated SNPs"
- User needs to find which GWAS hits overlap enhancers, promoters, or TF binding sites
- User wants to prioritize GWAS loci by functional annotation from ENCODE data
- Example queries: "find GWAS variants in my H3K27ac peaks", "which diabetes GWAS hits overlap pancreas enhancers?", "annotate GWAS loci with ENCODE regulatory marks"

Connect genome-wide association study findings with ENCODE functional annotations to identify which regulatory elements harbor disease-associated variants and prioritize causal mechanisms for non-coding GWAS hits.

## Scientific Rationale

**The question**: "Which of the disease-associated variants from GWAS fall within active regulatory elements, and what can ENCODE tell us about their functional impact?"

The GWAS Catalog (maintained by NHGRI-EBI) contains over 500,000 variant-trait associations from 6,000+ publications. The central challenge of post-GWAS analysis is that >90% of these associations point to non-coding regions of the genome. ENCODE provides the essential functional annotation layer: if a GWAS variant falls within an active enhancer in disease-relevant tissue, that enhancer becomes a candidate causal mechanism.

This was first demonstrated systematically by Maurano et al. (2012, Science), who showed that disease-associated variants are enriched in DNase I hypersensitive sites (DHSs), and that the cell-type specificity of the DHS predicts the relevant disease tissue. This foundational insight drives the entire GWAS-ENCODE integration framework.

### Scale of the Problem

- GWAS Catalog: 500,000+ associations, 100,000+ unique variants, 5,000+ traits
- ENCODE cCREs: 926,535 regulatory elements covering 7.9% of the genome
- Overlap expectation: ~8% of random variants would overlap a cCRE by chance
- Observed enrichment: GWAS variants show 2-5x enrichment in regulatory elements (higher for tissue-matched elements)

## Key Literature

- **Sollis et al. 2023** "The NHGRI-EBI GWAS Catalog: knowledgebase and deposition resource" (Nucleic Acids Research). The current GWAS Catalog publication describing the REST API, summary statistics hosting, and expanded annotation pipeline. [DOI: 10.1093/nar/gkac1010](https://doi.org/10.1093/nar/gkac1010)
- **Buniello et al. 2019** "The NHGRI-EBI GWAS Catalog of published genome-wide association studies, targeted arrays and summary statistics 2019" (Nucleic Acids Research, ~3,500 citations). The widely-cited GWAS Catalog reference describing curation standards and the move to EFO ontology for traits. [DOI: 10.1093/nar/gky1120](https://doi.org/10.1093/nar/gky1120)
- **Maurano et al. 2012** "Systematic localization of common disease-associated variation in regulatory DNA" (Science, ~3,000 citations). The foundational demonstration that GWAS variants concentrate in DNase I hypersensitive sites, with cell-type-specific enrichment predicting disease-relevant tissues. Enabled de novo identification of pathogenic cell types from variant sets. [DOI: 10.1126/science.1222794](https://doi.org/10.1126/science.1222794)
- **ENCODE Project Consortium 2020** (Nature, ~1,656 citations). Registry of 926,535 human cCREs that provides the regulatory annotation layer for GWAS variant interpretation. [DOI: 10.1038/s41586-020-2493-4](https://doi.org/10.1038/s41586-020-2493-4)
- **Finucane et al. 2015** (Nature Genetics, ~2,253 citations). Stratified LD Score Regression (S-LDSC) for partitioning heritability into ENCODE-defined functional categories. [DOI: 10.1038/ng.3404](https://doi.org/10.1038/ng.3404)
- **Nasser et al. 2021** (Nature, ~468 citations). ABC model linked 5,036 GWAS signals to 2,249 genes using ENCODE data. [DOI: 10.1038/s41586-021-03446-x](https://doi.org/10.1038/s41586-021-03446-x)

## GWAS Catalog REST API Reference

**Base URL**: `https://www.ebi.ac.uk/gwas/rest/api`

No authentication required. Responses are JSON (HAL format).

### Key Endpoints

| Endpoint | Purpose | Parameters |
|---------|---------|-----------|
| `/singleNucleotidePolymorphisms/{rsId}` | Get variant details | rsId (e.g., rs7903146) |
| `/singleNucleotidePolymorphisms/{rsId}/associations` | Get associations for a variant | rsId |
| `/associations?pubmedId={pmid}` | Get associations from a study | PubMed ID |
| `/studies?diseaseTrait={trait}` | Find studies by trait name | Trait string |
| `/efoTraits/{efoId}` | Get trait details by EFO ID | EFO ID |
| `/efoTraits/{efoId}/associations` | Associations for a trait | EFO ID |
| `/studies/{studyId}` | Study details | Study accession (GCST...) |

### Pagination

All list endpoints support pagination:
- `?page=0&size=20` (default page size is 20, max is 500)

### Bulk Downloads

For genome-wide analysis, use the GWAS Catalog downloads (faster than API):
- All associations: `https://www.ebi.ac.uk/gwas/api/search/downloads/full`
- Alternative: `https://www.ebi.ac.uk/gwas/docs/file-downloads`
- Format: TSV with columns for variant, trait, p-value, OR/beta, study, etc.

## Step 1: Define the Disease/Trait and Relevant Tissues

### Query GWAS Catalog for a Trait

```python
import requests

# Search by trait name
trait = "type 2 diabetes"
url = "https://www.ebi.ac.uk/gwas/rest/api/studies"
params = {"diseaseTrait": trait}
response = requests.get(url, params=params)
studies = response.json()["_embedded"]["studies"]

print(f"Found {len(studies)} GWAS studies for '{trait}'")
for study in studies[:5]:
    print(f"  {study['accessionId']}: {study['publicationInfo']['title'][:80]}...")
```

### Use EFO IDs for Standardized Trait Queries

The Experimental Factor Ontology (EFO) standardizes trait names:

| Common Trait | EFO ID | EFO Term |
|-------------|--------|----------|
| Type 2 diabetes | EFO_0001360 | type II diabetes mellitus |
| Breast cancer | EFO_0000305 | breast carcinoma |
| Alzheimer's disease | MONDO_0004975 | Alzheimer disease |
| Crohn's disease | EFO_0000384 | Crohn's disease |
| Coronary artery disease | EFO_0001645 | coronary artery disease |
| Schizophrenia | EFO_0000692 | schizophrenia |

```python
# Query by EFO ID (more precise)
efo_id = "EFO_0001360"
url = f"https://www.ebi.ac.uk/gwas/rest/api/efoTraits/{efo_id}/associations"
params = {"size": 500}
response = requests.get(url, params=params)
```

### Map Trait to ENCODE Tissues

Following the Maurano 2012 framework — disease-associated variants are enriched in tissue-specific regulatory elements:

| Disease Category | Expected Enriched ENCODE Tissues |
|-----------------|--------------------------------|
| Type 2 diabetes | Pancreatic islets, liver, adipose, skeletal muscle |
| Autoimmune diseases | Immune cells (T/B cells, monocytes), thymus |
| Neuropsychiatric | Brain (cortex, hippocampus), neurons |
| Cardiovascular | Heart, blood vessels, blood |
| Liver disease | Liver, hepatocytes (HepG2) |
| Inflammatory bowel | Intestine, colon, immune cells |
| Cancer | Tissue of origin + immune microenvironment |

```
# Check ENCODE data availability for disease-relevant tissue
encode_get_facets(organ="pancreas")
encode_get_facets(organ="liver")
```

## Step 2: Retrieve GWAS Variants

### Get Associations for a Variant

```python
def get_gwas_associations(rs_id):
    """Get all GWAS associations for a variant."""
    url = f"https://www.ebi.ac.uk/gwas/rest/api/singleNucleotidePolymorphisms/{rs_id}/associations"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["_embedded"]["associations"]
    return []

# Example: rs7903146 (strongest T2D variant, in TCF7L2)
associations = get_gwas_associations("rs7903146")
for assoc in associations:
    trait = assoc["efoTraits"][0]["trait"] if assoc["efoTraits"] else "Unknown"
    pval = assoc["pvalue"]
    print(f"  Trait: {trait}, p-value: {pval}")
```

### Get All Variants for a Study

```python
def get_study_associations(study_id):
    """Get all associations from a GWAS study."""
    url = f"https://www.ebi.ac.uk/gwas/rest/api/studies/{study_id}/associations"
    params = {"size": 500}
    response = requests.get(url, params=params)
    return response.json()["_embedded"]["associations"]

# Example: Mahajan et al. 2018 T2D GWAS
associations = get_study_associations("GCST006867")
```

### Extract Variant Coordinates

GWAS Catalog provides variant locations. Extract for BED format:

```python
def associations_to_bed(associations):
    """Convert GWAS Catalog associations to BED format lines."""
    bed_lines = []
    for assoc in associations:
        for locus in assoc.get("loci", []):
            for gene in locus.get("strongestRiskAlleles", []):
                rs_id = gene.get("riskAlleleName", "").split("-")[0]
        # Get location from the SNP endpoint
        snp_url = f"https://www.ebi.ac.uk/gwas/rest/api/singleNucleotidePolymorphisms/{rs_id}"
        snp_resp = requests.get(snp_url)
        if snp_resp.status_code == 200:
            snp = snp_resp.json()
            for loc in snp.get("locations", []):
                chrom = f"chr{loc['chromosomeName']}"
                pos = int(loc['chromosomePosition'])
                bed_lines.append(f"{chrom}\t{pos-1}\t{pos}\t{rs_id}")
    return bed_lines
```

## Step 3: LD Expansion

**Critical**: GWAS lead SNPs are NOT necessarily causal. The causal variant is often a different SNP in linkage disequilibrium (LD).

### When to Expand

| Input | LD Expansion Needed? |
|-------|---------------------|
| GWAS Catalog lead SNPs | YES — expand to r2 >= 0.8 proxies |
| Fine-mapped credible sets (SuSiE, FINEMAP) | NO — already LD-aware |
| Single candidate variant | NO — annotate directly |

### LD Expansion Tools

- **LDlink** (NIH): `https://ldlink.nih.gov/?tab=ldproxy` — Web and API
  - API: `https://ldlink.nih.gov/LDlinkRest/ldproxy?var={rsId}&pop={population}&r2_d=r2&token={token}`
  - Requires free API token
- **1000 Genomes**: Reference panel for LD calculation
- **PLINK**: `plink --ld-snp {rsId} --ld-window-r2 0.8`

### Population-Specific LD

Always use the appropriate ancestry population:

| Population | Code | Use When |
|-----------|------|---------|
| European | EUR | Most GWAS to date |
| East Asian | EAS | EAS-specific GWAS |
| African | AFR | AFR-specific or trans-ethnic |
| South Asian | SAS | SAS-specific GWAS |
| All | ALL | Trans-ethnic or unknown |

## Step 4: Intersect GWAS Variants with ENCODE Peaks

### Retrieve ENCODE Peak Files

```
# Chromatin accessibility
encode_search_experiments(assay_title="ATAC-seq", organ="pancreas", biosample_type="tissue")
encode_search_experiments(assay_title="DNase-seq", organ="pancreas", biosample_type="tissue")

# Active regulatory marks
encode_search_experiments(assay_title="Histone ChIP-seq", target="H3K27ac", organ="pancreas")
encode_search_experiments(assay_title="Histone ChIP-seq", target="H3K4me3", organ="pancreas")

# TF binding
encode_search_experiments(assay_title="TF ChIP-seq", organ="pancreas")

# Get IDR thresholded peak files (GRCh38)
encode_list_files(
    experiment_accession="ENCSR...",
    file_format="bed",
    output_type="IDR thresholded peaks",
    assembly="GRCh38",
    preferred_default=True
)
```

### bedtools Intersection

```bash
# Create BED file from GWAS variants (with LD proxies)
# gwas_variants_ld.bed: chr start end rsId pvalue trait

# Intersect with ENCODE peaks
bedtools intersect \
    -a gwas_variants_ld.bed \
    -b encode_h3k27ac_peaks.bed \
    -wa -wb \
    > gwas_in_enhancers.bed

bedtools intersect \
    -a gwas_variants_ld.bed \
    -b encode_atac_peaks.bed \
    -wa -wb \
    > gwas_in_accessible.bed

bedtools intersect \
    -a gwas_variants_ld.bed \
    -b encode_ctcf_peaks.bed \
    -wa -wb \
    > gwas_in_ctcf.bed
```

### Enrichment Calculation

```python
# Simple enrichment: observed vs. expected overlap
total_variants = 1000
variants_in_peaks = 150
genome_fraction_in_peaks = 0.02  # 2% of genome covered by peaks

expected = total_variants * genome_fraction_in_peaks
enrichment = variants_in_peaks / expected
print(f"Enrichment: {enrichment:.1f}x (observed={variants_in_peaks}, expected={expected:.0f})")
```

For rigorous enrichment testing, use S-LDSC (Finucane et al. 2015) or GARFIELD (Iotchkova et al. 2019) as described in the `variant-annotation` skill.

## Step 5: Classify Regulatory Impact

For each GWAS variant in an ENCODE peak, classify the regulatory mechanism:

### The Maurano 2012 Framework

1. **Identify the DHS/ATAC peak** — confirms the region is accessible in disease tissue
2. **Classify the element type** — H3K27ac (enhancer/promoter), H3K4me3 (promoter), CTCF (insulator)
3. **Determine tissue specificity** — tissue-specific elements are more likely causal
4. **Link to target gene** — Hi-C, ABC model, eQTL colocalization

### Regulatory Impact Table

| GWAS Variant in... | ENCODE Evidence | Priority |
|-------------------|----------------|---------|
| Tissue-specific active enhancer (H3K27ac+, tissue-restricted) | Variant disrupts tissue-specific regulatory element | Highest |
| Tissue-specific ATAC peak (no histone marks) | Accessible region, possibly regulatory | High |
| Active promoter (H3K4me3+) near GWAS gene | Variant may affect transcription initiation | High |
| CTCF binding site at TAD boundary | Variant may disrupt chromatin insulation | High |
| Broadly active enhancer (many tissues) | Less tissue-specific, but still functional | Moderate |
| No ENCODE overlap in disease tissue | Variant may act in untested cell type or be non-causal | Low |

## Step 6: Variant-to-Gene Linking

The nearest gene to a GWAS variant is the correct target only ~50-60% of the time. Use ENCODE data for better gene assignment:

### ABC Model (Nasser et al. 2021)

Activity-By-Contact predictions link enhancers to genes using ENCODE ATAC-seq + H3K27ac + Hi-C:
- Pre-computed for 131 cell types
- Download from: https://www.engreitzlab.org/abc/
- Linked 5,036 GWAS signals to 2,249 target genes

### Hi-C Contact Maps

```
encode_search_experiments(assay_title="Hi-C", organ="pancreas")
```

Check whether the variant-containing enhancer physically contacts a gene promoter.

### eQTL Colocalization

Cross-reference with GTEx eQTLs to identify the gene regulated by the GWAS variant. See `gtex-expression` skill for API details.

## Step 7: Log Provenance

```
encode_track_experiment(accession="ENCSR...", notes="GWAS-ENCODE overlay for T2D")

encode_log_derived_file(
    file_path="/path/to/gwas_encode_intersection.tsv",
    source_accessions=["ENCSR...", "ENCSR...", "ENCSR..."],
    description="Intersection of T2D GWAS variants (Mahajan 2018, LD r2>0.8 EUR) with ENCODE H3K27ac and ATAC-seq peaks in pancreas",
    file_type="variant_annotation",
    tool_used="bedtools intersect + GWAS Catalog REST API + LDlink",
    parameters="GRCh38, genome-wide significant (p<5e-8), IDR thresholded peaks, EUR LD r2>0.8"
)

encode_link_reference(
    experiment_accession="ENCSR...",
    reference_type="pmid",
    reference_id="30297969",
    description="Mahajan et al. 2018 T2D GWAS providing variant set"
)
```

## Pitfalls and Caveats

### 1. Lead SNP Is Not Causal Variant
The GWAS Catalog reports lead SNPs (strongest statistical signal per locus). The causal variant is often a different SNP in LD. Always expand to LD proxies (r2 >= 0.8) before intersecting with ENCODE peaks. Fine-mapped credible sets (SuSiE, FINEMAP) bypass this issue.

### 2. P-Value Thresholds
Genome-wide significance is p < 5 x 10^-8. Suggestive significance (p < 1 x 10^-5) may be included in some GWAS Catalog entries. For regulatory annotation, focus on genome-wide significant variants unless the user specifically requests suggestive hits. Sub-threshold variants have higher false-positive rates.

### 3. Population Specificity
LD patterns differ substantially by ancestry. A lead SNP in a European GWAS may not tag the same LD block in African or East Asian populations. Always use population-matched LD reference panels. Trans-ethnic fine-mapping can narrow credible sets by exploiting LD differences.

### 4. Trait Ontology Mapping
The GWAS Catalog uses EFO (Experimental Factor Ontology) for trait standardization. Free-text trait names in the API may not match exactly. Use EFO IDs for precise queries. The mapping between disease traits and ENCODE tissue/biosample terms requires manual curation.

### 5. Assembly Consistency
The GWAS Catalog provides coordinates in GRCh38. Older GWAS studies may report hg19/GRCh37 positions. ENCODE peaks should be in GRCh38. Always verify assembly match. Use UCSC liftOver or CrossMap for coordinate conversion if needed. NEVER mix assemblies.

## Walkthrough: Connecting GWAS Variants to ENCODE Regulatory Elements

**Goal**: Identify GWAS-significant variants that fall within ENCODE-defined regulatory elements to prioritize causal non-coding variants for a disease of interest.
**Context**: Type 2 diabetes has hundreds of GWAS hits, most in non-coding regions. ENCODE maps which of these overlap active regulatory elements.

### Step 1: Find ENCODE regulatory data for pancreas

```
encode_search_experiments(assay_title="ATAC-seq", organ="pancreas", organism="Homo sapiens")
```

Expected output:
```json
{
  "total": 6,
  "results": [
    {"accession": "ENCSR456PAN", "assay_title": "ATAC-seq", "biosample_summary": "pancreas", "status": "released"},
    {"accession": "ENCSR457ISL", "assay_title": "ATAC-seq", "biosample_summary": "islet of Langerhans", "status": "released"}
  ]
}
```

**Interpretation**: Both whole pancreas and islet-specific ATAC-seq available. Islet data is more relevant for T2D (beta cell disease).

### Step 2: Download regulatory peak files

```
encode_list_files(accession="ENCSR457ISL", file_format="bed", output_type="IDR thresholded peaks", assembly="GRCh38")
```

Expected output:
```json
{
  "files": [
    {"accession": "ENCFF200ISL", "output_type": "IDR thresholded peaks", "file_format": "bed narrowPeak", "file_size_mb": 0.9}
  ]
}
```

### Step 3: Query GWAS Catalog for T2D associations

Using GWAS Catalog REST API (via skill guidance):
```
GET https://www.ebi.ac.uk/gwas/rest/api/associations?efoTrait=EFO_0001360&pvalueFilter=5e-8
```

Expected key fields per association:
```json
{
  "riskFrequency": "0.30",
  "pvalue": 2.4e-12,
  "snps": [{"rsId": "rs7903146", "chromosomeName": "10", "chromosomePosition": 114758349}],
  "efoTraits": [{"trait": "type 2 diabetes mellitus"}]
}
```

### Step 4: Intersect GWAS variants with ENCODE peaks

```bash
bedtools intersect -a t2d_gwas_variants.bed -b ENCFF200ISL.bed -wa -wb > t2d_regulatory_variants.bed
```

**Interpretation**: GWAS variants overlapping islet ATAC-seq peaks are strong candidates for causal regulatory variants. Variants in islet-specific (but not other tissue) peaks suggest tissue-restricted regulatory mechanisms for T2D.

### Step 5: Prioritize candidates with multi-evidence support

Rank variants by evidence layers:
1. GWAS significant (p < 5×10⁻⁸) ✓
2. In islet open chromatin (ATAC-seq peak) ✓
3. Near islet-expressed gene (GTEx) — check via **gtex-expression**
4. In H3K27ac-marked enhancer — check via **histone-aggregation**
5. ClinVar annotation — check via **clinvar-annotation**

### Integration with downstream skills
- ENCODE peaks from → **regulatory-elements** define regions to intersect with GWAS hits
- Overlapping variants feed into → **variant-annotation** for functional prediction
- Population frequencies from → **gnomad-variants** contextualize GWAS allele frequencies
- Expression effects checked via → **gtex-expression** eQTL data
- Clinical significance from → **clinvar-annotation** adds clinical interpretation

## Code Examples

### 1. Survey ENCODE data for GWAS-relevant tissues
```
encode_get_facets(facet_field="organ", assay_title="ATAC-seq", organism="Homo sapiens")
```

Expected output:
```json
{
  "facets": {
    "organ": {"brain": 32, "heart": 18, "liver": 14, "pancreas": 6, "blood": 25}
  }
}
```

### 2. Find histone mark data to layer on GWAS regions
```
encode_search_experiments(assay_title="Histone ChIP-seq", organ="pancreas", target="H3K27ac", organism="Homo sapiens")
```

Expected output:
```json
{
  "total": 4,
  "results": [
    {"accession": "ENCSR300ACE", "assay_title": "Histone ChIP-seq", "target": "H3K27ac", "biosample_summary": "islet of Langerhans"}
  ]
}
```

### 3. Track experiments used for GWAS annotation
```
encode_track_experiment(accession="ENCSR457ISL", notes="Islet ATAC-seq for T2D GWAS variant annotation")
```

Expected output:
```json
{
  "status": "tracked",
  "accession": "ENCSR457ISL",
  "notes": "Islet ATAC-seq for T2D GWAS variant annotation"
}
```

## Integration

| This skill produces... | Feed into... | Purpose |
|---|---|---|
| GWAS variant coordinates | **regulatory-elements** | Intersect trait variants with ENCODE cCREs |
| Trait-associated loci | **variant-annotation** | Comprehensive functional annotation of GWAS hits |
| Risk allele frequencies | **gnomad-variants** | Compare GWAS frequencies with population data |
| GWAS gene associations | **gtex-expression** | Validate expression of GWAS-implicated genes |
| Lead SNP + LD proxy coordinates | **peak-annotation** | Assign GWAS loci to target genes via peak overlap |
| Disease-trait mappings | **disease-research** | Connect ENCODE regulatory findings to disease phenotypes |
| GWAS variant BED files | **clinvar-annotation** | Cross-reference GWAS hits with clinical significance |
| Multi-trait variant overlaps | **visualization-workflow** | Generate Manhattan plots with regulatory annotation overlay |

## Presenting Results

### Summary Table

| Locus | Lead SNP | p-value | Trait | LD Variants Tested | In ENCODE Peak | Element Type | Target Gene | Priority |
|-------|---------|---------|-------|-------------------|---------------|-------------|-------------|---------|
| 10q25 | rs7903146 | 2e-120 | T2D | 47 (r2>0.8) | rs7903146 (lead) | H3K27ac enhancer | TCF7L2 | Highest |
| 11p15 | rs2237892 | 5e-20 | T2D | 23 | rs2237895 (proxy) | ATAC-seq peak | KCNQ1 | High |

### Key Numbers to Report

- Total GWAS variants analyzed (lead + LD proxies)
- Fraction overlapping ENCODE regulatory elements (by element type)
- Enrichment over background (observed/expected)
- Number of tissue-specific elements harboring variants
- Variant-to-gene links established and method used
- Diseases/traits represented

## Related Skills

- `variant-annotation` — Full ENCODE variant annotation and prioritization workflow
- `clinvar-annotation` — Clinical significance of variants in ENCODE peaks
- `gnomad-variants` — Population frequency for GWAS variants
- `disease-research` — Disease-focused ENCODE analysis workflows
- `regulatory-elements` — Characterizing ENCODE regulatory elements at GWAS loci
- `gtex-expression` — eQTL colocalization and expression context for GWAS genes
- `publication-trust` — Verify literature claims backing analytical decisions

## For the request: "$ARGUMENTS"
