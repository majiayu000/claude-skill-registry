---
name: gnomad-variants
description: Query gnomAD (Genome Aggregation Database) for population allele frequencies, gene constraint scores, and variant annotations to interpret ENCODE regulatory variants. Use when the user needs allele frequencies for variants in ENCODE regulatory elements, wants to assess gene constraint (pLI, LOEUF) for ENCODE target genes, needs population-specific frequencies for GWAS variants overlapping cCREs, wants to filter variants by rarity before functional annotation, or is interpreting ENCODE CRISPR/MPRA results in the context of population genetics. Also use when the user mentions gnomAD, allele frequency, pLI, LOEUF, constraint, rare variants, population frequency, ExAC, or variant filtering.
---

# Query gnomAD for Population Variant Data

## When to Use

- User wants to check population allele frequencies for variants in ENCODE regulatory regions
- User asks about "gnomAD", "allele frequency", "population genetics", "gene constraint", or "variant frequency"
- User needs to filter regulatory variants by rarity (common vs rare) using population data
- User wants to assess gene constraint (pLI, LOEUF) for targets identified from ENCODE ChIP-seq
- Example queries: "check gnomAD frequency for variants in my peaks", "is this regulatory variant rare?", "what's the constraint score for CTCF?"

Annotate ENCODE-identified regulatory variants with population allele frequencies and gene constraint scores from the Genome Aggregation Database.

## Scientific Rationale

**The question**: "How common is this variant in the population, and how constrained is the gene it regulates?"

ENCODE identifies regulatory elements and the variants within them, but does not provide population frequency data. gnomAD (v4.1: 807,162 individuals, 730,947 exomes + 76,215 genomes) fills this gap — enabling researchers to distinguish common regulatory variants (likely benign or with modest effect) from rare variants (potentially pathogenic or high-impact).

### Why gnomAD + ENCODE Together

| ENCODE Provides | gnomAD Provides | Combined Insight |
|----------------|----------------|------------------|
| Variant overlaps cCRE (dELS) | AF = 0.0001 (rare) | Rare variant disrupting an enhancer → high priority |
| Variant in TF binding site | AF = 0.15 (common) | Common regulatory variant → likely modest effect or GWAS candidate |
| Target gene identified | LOEUF = 0.12 (highly constrained) | Constrained gene + rare enhancer variant → strong candidate |
| Variant in CRISPR-validated enhancer | Not in gnomAD (absent) | Ultra-rare/de novo → possible pathogenic regulatory variant |

### Key Resources

- **gnomAD v4.1** (GRCh38): 807,162 individuals, 62.9M SNVs + 6.2M indels
- **gnomAD v3.1.2** (GRCh38): Genome-only dataset, 76,156 genomes
- **gnomAD v2.1.1** (GRCh37/hg19): Legacy dataset, still widely used
- **ExAC** (GRCh37): Superseded by gnomAD. All ExAC samples included in gnomAD v2+.
- **gnomAD browser**: https://gnomad.broadinstitute.org

### Literature Support

- **Karczewski et al. 2020** (Nature, ~5,000 citations): gnomAD — mutational constraint spectrum from 141,456 individuals. Defined LOEUF as primary constraint metric. [DOI](https://doi.org/10.1038/s41586-020-2308-7)
- **Lek et al. 2016** (Nature, ~7,000 citations): ExAC — analysis of protein-coding variation in 60,706 humans. Established pLI for gene constraint. [DOI](https://doi.org/10.1038/nature19057)
- **Maurano et al. 2012** (Science, ~2,800 citations): Disease variants concentrate in DNase hypersensitive sites. [DOI](https://doi.org/10.1126/science.1222794)
- **Finucane et al. 2015** (Nature Genetics, ~2,253 citations): Stratified LD score regression partitioning heritability into ENCODE annotations. [DOI](https://doi.org/10.1038/ng.3404)

## Step 1: Determine the Query Type

| User Has | Query Strategy |
|----------|---------------|
| Specific variant (rs ID or chr-pos-ref-alt) | Single variant lookup |
| List of GWAS/eQTL variants | Batch variant query |
| Gene of interest (ENCODE target) | Gene constraint lookup |
| Genomic region with ENCODE peaks | Region variant query |

## Step 2: Query gnomAD via GraphQL API

**Endpoint**: `https://gnomad.broadinstitute.org/api`
**Method**: POST with GraphQL query in JSON body
**Authentication**: None required
**Rate limit**: IP-level throttling; throttle to ~1 request/second for batch queries

### Single Variant Lookup

```bash
curl -X POST https://gnomad.broadinstitute.org/api \
  -H "Content-Type: application/json" \
  -d '{
    "query": "query { variant(variantId: \"1-55517991-C-CAT\", dataset: gnomad_r4) { exome { ac an af } genome { ac an af } joint { ac an af } } }"
  }'
```

**Variant ID format**: `CHR-POS-REF-ALT` (1-based position, no "chr" prefix)

### Gene Constraint Lookup

```bash
curl -X POST https://gnomad.broadinstitute.org/api \
  -H "Content-Type: application/json" \
  -d '{
    "query": "query { gene(gene_symbol: \"BRCA2\", reference_genome: GRCh38) { symbol gene_id gnomad_constraint { pLI oe_lof oe_lof_lower oe_lof_upper oe_mis oe_mis_lower oe_mis_upper } } }"
  }'
```

### Region Variant Query

```bash
curl -X POST https://gnomad.broadinstitute.org/api \
  -H "Content-Type: application/json" \
  -d '{
    "query": "query { region(chrom: \"1\", start: 55505222, stop: 55530526, reference_genome: GRCh38) { variants(dataset: gnomad_r4) { variant_id pos ref alt exome { ac af } genome { ac af } } } }"
  }'
```

## Step 3: Interpret Constraint Scores

### Gene Constraint (Karczewski et al. 2020)

| Metric | Definition | Interpretation |
|--------|-----------|----------------|
| **LOEUF** | Loss-of-function observed/expected upper bound 90% CI | <0.35 = highly constrained (v2); <0.6 = constrained (v4) |
| **pLI** | Probability of being loss-of-function intolerant | >0.9 = LoF-intolerant (legacy metric from ExAC) |
| **oe_lof** | Observed/expected loss-of-function ratio | <0.2 = highly constrained |
| **oe_mis** | Observed/expected missense ratio | <0.6 = missense constrained |
| **Z_syn** | Synonymous Z-score | Near 0 expected; deviation suggests selection |

**LOEUF is preferred over pLI** for gnomAD v4+. LOEUF is continuous and better calibrated.

### Applying Constraint to ENCODE Analysis

For genes identified as targets of ENCODE regulatory elements:

| LOEUF | Interpretation | Implication for Regulatory Variants |
|-------|---------------|-------------------------------------|
| <0.35 | Highly constrained (haploinsufficient) | Regulatory variants likely pathogenic; even modest expression changes may be deleterious |
| 0.35-0.6 | Moderately constrained | Regulatory variants worth investigating |
| >0.6 | Tolerant of LoF | Expression changes likely tolerated; regulatory variants less likely pathogenic |

## Step 4: Allele Frequency Filtering

### Standard Frequency Thresholds

| Category | Allele Frequency | Use Case |
|----------|-----------------|----------|
| Ultra-rare | AF < 0.0001 (1 in 10,000) | Mendelian disease candidates |
| Rare | AF < 0.01 (1%) | Rare disease, high-penetrance |
| Low-frequency | 0.01-0.05 | eQTL fine-mapping |
| Common | AF > 0.05 (5%) | GWAS, population-level effects |

### Population-Specific Frequencies

gnomAD provides frequencies for genetic ancestry groups:
- **African/African American** (afr)
- **Admixed American/Latino** (amr)
- **Ashkenazi Jewish** (asj)
- **East Asian** (eas)
- **European (Finnish)** (fin)
- **European (non-Finnish)** (nfe)
- **Middle Eastern** (mid)
- **South Asian** (sas)

**Critical**: A variant "rare" globally may be common in one population. Always check population-specific frequencies when interpreting regulatory variants in disease context.

## Step 5: Integrated ENCODE + gnomAD Workflow

```
1. Identify regulatory variants from ENCODE:
   encode_search_files(output_type="IDR thresholded peaks", organ="pancreas", file_format="bed")
   → Intersect peaks with GWAS/eQTL variants using bedtools

2. Get allele frequencies from gnomAD:
   → GraphQL query for each variant
   → Filter by desired AF threshold

3. Check constraint of target genes:
   → For each variant-to-gene link (from ABC model, ENCODE enhancer-gene maps)
   → Query gnomAD gene constraint (LOEUF)

4. Prioritize:
   → Rare variant (AF < 0.01) + active enhancer + constrained gene (LOEUF < 0.35) = HIGH PRIORITY
   → Common variant (AF > 0.05) + active enhancer = potential GWAS mechanism
   → Absent from gnomAD + CRISPR-validated enhancer = potential de novo pathogenic

5. Track provenance:
   encode_log_derived_file(
       file_path="/path/to/prioritized_variants.tsv",
       source_accessions=["ENCSR...", "gnomAD_v4.1"],
       description="ENCODE regulatory variants filtered by gnomAD AF and constraint",
       tool_used="bedtools intersect + gnomAD GraphQL"
   )
```

## Step 6: Bulk Data Access

For genome-wide analysis, downloading gnomAD VCFs is more efficient than API queries:

```bash
# gnomAD v4 genome VCFs (GRCh38)
# Available at: https://gnomad.broadinstitute.org/downloads
# Files hosted on Google Cloud Storage and AWS

# Download a single chromosome
gsutil cp gs://gcp-public-data--gnomad/release/4.1/vcf/genomes/gnomad.genomes.v4.1.sites.chr1.vcf.bgz .

# Or use Hail for cloud-native analysis
```

**File sizes are large**: Full genome VCF is ~1TB. Download per-chromosome files for targeted analysis.

## Pitfalls and Caveats

1. **gnomAD excludes pediatric disease cohorts**: gnomAD explicitly removes individuals with severe pediatric disease. Pathogenic variants may be absent or at extremely low frequency.
2. **Variant ID format matters**: gnomAD uses `CHR-POS-REF-ALT` with 1-based positions and no "chr" prefix. Convert from VCF/BED coordinates carefully.
3. **ExAC is superseded**: Do not use ExAC for new analyses. All ExAC samples are included in gnomAD v2+. Use gnomAD v4.1 (GRCh38) for current work.
4. **Assembly consistency**: gnomAD v4 uses GRCh38, matching ENCODE. gnomAD v2.1.1 uses GRCh37 — do NOT mix with GRCh38 ENCODE data without liftOver.
5. **Non-coding coverage gaps**: gnomAD exome data only covers protein-coding regions. For non-coding regulatory variants, use gnomAD **genome** data specifically.
6. **GraphQL rate limiting**: No published threshold, but automated batch queries can trigger IP-level blocks. Throttle to ~1 req/sec for batch operations.
7. **LOEUF vs pLI**: Use LOEUF (continuous, better calibrated) for gnomAD v4. pLI is still reported for backward compatibility but is not recommended for new analyses.
8. **Structural variants**: gnomAD-SV provides structural variant data separately. Use for CNV/SV analysis around ENCODE regulatory elements.

## Walkthrough: Population Frequency Context for ENCODE Regulatory Variants

**Goal**: Use gnomAD population allele frequencies to contextualize variants found in ENCODE regulatory elements, distinguishing rare disease-causing variants from common regulatory polymorphisms.
**Context**: gnomAD provides allele frequencies across 76,000+ genomes. Variants in ENCODE regulatory regions with low population frequency are candidates for disease-causing regulatory mutations.

### Step 1: Find ENCODE regulatory peaks

```
encode_search_experiments(assay_title="ATAC-seq", organ="kidney", organism="Homo sapiens")
```

Expected output:
```json
{
  "total": 8,
  "results": [
    {"accession": "ENCSR900KID", "assay_title": "ATAC-seq", "biosample_summary": "kidney", "status": "released"}
  ]
}
```

### Step 2: Download peak files

```
encode_list_files(accession="ENCSR900KID", file_format="bed", output_type="IDR thresholded peaks", assembly="GRCh38")
```

Expected output:
```json
{
  "files": [
    {"accession": "ENCFF950KID", "output_type": "IDR thresholded peaks", "file_format": "bed narrowPeak", "file_size_mb": 0.7}
  ]
}
```

### Step 3: Query gnomAD for variants in regulatory peaks

Using gnomAD GraphQL API (via skill guidance):
```graphql
{
  region(dataset: gnomad_r4, chrom: "16", start: 68771195, stop: 68771395) {
    variants {
      variant_id
      pos
      ref
      alt
      genome {
        ac
        an
        af
        populations { id ac an af }
      }
    }
  }
}
```

Expected response:
```json
{
  "data": {
    "region": {
      "variants": [
        {"variant_id": "16-68771250-C-T", "genome": {"af": 0.00012, "ac": 18, "an": 152312}},
        {"variant_id": "16-68771300-G-A", "genome": {"af": 0.35, "ac": 53321, "an": 152312}}
      ]
    }
  }
}
```

**Interpretation**:
- 16-68771250-C-T (AF=0.012%) — rare variant in kidney ATAC-seq peak → candidate disease variant
- 16-68771300-G-A (AF=35%) — common polymorphism → likely benign regulatory variant

### Step 4: Filter for rare regulatory variants

Apply gnomAD frequency filters:
- **Ultra-rare** (AF < 0.01%): highest priority for Mendelian disease
- **Rare** (AF 0.01–1%): consider for complex disease risk
- **Common** (AF > 1%): likely benign, but may contribute to common disease via GWAS

### Step 5: Check gene constraint scores

```graphql
{
  gene(gene_symbol: "PKD1", reference_genome: GRCh38) {
    gnomad_constraint {
      pLI
      oe_lof
      oe_lof_upper
    }
  }
}
```

**Interpretation**: pLI near 1.0 = gene is loss-of-function intolerant. Rare regulatory variants near constrained genes are higher priority.

### Integration with downstream skills
- Rare variants in ENCODE peaks feed into → **variant-annotation** for comprehensive annotation
- Population frequencies contextualize → **clinvar-annotation** pathogenicity calls
- Gene constraint scores inform → **disease-research** gene prioritization
- Frequency-filtered variants integrate with → **gwas-catalog** for allele frequency comparison

## Code Examples

### 1. Find ENCODE data for gnomAD-relevant tissues
```
encode_get_facets(facet_field="organ", assay_title="ATAC-seq", organism="Homo sapiens")
```

Expected output:
```json
{
  "facets": {
    "organ": {"brain": 32, "heart": 18, "liver": 14, "kidney": 8, "lung": 10}
  }
}
```

### 2. Get experiment details before variant annotation
```
encode_get_experiment(accession="ENCSR900KID")
```

Expected output:
```json
{
  "accession": "ENCSR900KID",
  "assay_title": "ATAC-seq",
  "biosample_summary": "kidney",
  "replicates": 2,
  "status": "released",
  "audit": {"WARNING": 0, "ERROR": 0}
}
```

### 3. Track experiments used for variant frequency analysis
```
encode_track_experiment(accession="ENCSR900KID", notes="Kidney ATAC-seq for gnomAD regulatory variant filtering")
```

Expected output:
```json
{
  "status": "tracked",
  "accession": "ENCSR900KID",
  "notes": "Kidney ATAC-seq for gnomAD regulatory variant filtering"
}
```

## Integration

| This skill produces... | Feed into... | Purpose |
|---|---|---|
| Population allele frequencies | **variant-annotation** | Frequency-based variant prioritization |
| Gene constraint scores (pLI, LOEUF) | **disease-research** | Identify intolerant genes for disease gene prioritization |
| Rare variant coordinates | **clinvar-annotation** | Cross-reference rare variants with clinical significance |
| Population-specific frequencies | **gwas-catalog** | Compare GWAS risk allele frequencies across populations |
| Variant frequency filters | **regulatory-elements** | Identify regulatory regions under selection pressure |
| Frequency-annotated variant BED | **peak-annotation** | Prioritize rare variants near gene promoters |
| Gene constraint metrics | **gtex-expression** | Check expression of constrained genes with regulatory variants |

## Related Skills

| Skill | When to Use Instead/Additionally |
|-------|--------------------------------|
| `variant-annotation` | Full post-GWAS annotation workflow with ENCODE cCREs, RegulomeDB, CADD |
| `regulatory-elements` | Identifying what regulatory elements a variant falls in |
| `disease-research` | Connecting ENCODE data to disease mechanisms |
| `ucsc-browser` | Getting cCRE annotations and TF binding at variant positions |
| `ensembl-annotation` | VEP annotation and regulatory feature overlap for variants |
| `data-provenance` | Logging gnomAD + ENCODE combined analysis provenance |
| `clinvar-annotation` | Clinical significance and pathogenicity for gnomAD variants |
| `gwas-catalog` | GWAS associations for variants with population frequency context |
| `publication-trust` | Verify literature claims backing analytical decisions |

## Presenting Results

- Present population frequency data as: variant | rsID | allele_freq | population | homozygotes. Flag variants absent from gnomAD (potentially novel). Suggest: "Would you like to check ClinVar significance for these variants?"

## For the request: "$ARGUMENTS"
