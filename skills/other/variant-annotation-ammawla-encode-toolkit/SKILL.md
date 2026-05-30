---
name: variant-annotation
description: Annotate genetic variants (GWAS hits, eQTLs, rare variants) with ENCODE functional data to interpret non-coding variation. Use when the user has variants of interest and wants to understand their regulatory context, identify causal variants from GWAS loci, assess variant impact on regulatory elements, perform enrichment testing of variant sets in tissue-specific annotations, or link variants to target genes through enhancer-gene maps. Handles the full post-GWAS workflow from variant set → tissue mapping → functional annotation → fine-mapping awareness → enrichment → variant-to-gene → prioritization. Use this skill for ANY variant interpretation task involving ENCODE chromatin, accessibility, TF binding, or 3D genome data.
---

# Functional Annotation of Genetic Variants with ENCODE Data

## When to Use

- User wants to annotate genetic variants with ENCODE regulatory element overlap and functional evidence
- User asks about "variant annotation", "regulatory variants", "non-coding variants", or "variant prioritization"
- User needs to assess whether a variant falls in an active enhancer, promoter, or TF binding site
- User wants to build a multi-evidence variant interpretation combining ENCODE + ClinVar + gnomAD
- Example queries: "annotate my GWAS hits with ENCODE regulatory data", "does this variant disrupt a TF binding site?", "prioritize non-coding variants by regulatory impact"

Interpret non-coding genetic variation by layering ENCODE functional genomics annotations to identify causal regulatory variants and link them to target genes.

## Scientific Rationale

**The question**: "Which of my GWAS/eQTL variants actually disrupt regulatory elements, and what genes do they affect?"

Over 90% of disease-associated variants from GWAS fall in non-coding regions of the genome. Without functional annotation, a GWAS locus is just a genomic coordinate — it does not tell you which variant is causal, what regulatory element it disrupts, or which gene it affects. ENCODE provides the richest catalog of functional elements for interpreting these variants.

### The Core Challenge

A typical GWAS locus contains dozens to hundreds of variants in linkage disequilibrium (LD) with the lead SNP. The causal variant(s) may not be the one with the strongest association. Functional annotation helps distinguish causal from tag variants by asking: does this variant overlap a regulatory element that is active in disease-relevant tissue?

### The ENCODE Solution: Candidate cis-Regulatory Elements (cCREs)

The ENCODE Phase 3 project (ENCODE Project Consortium 2020, Nature, ~1,656 citations) established a registry of **926,535 human candidate cis-regulatory elements (cCREs)** covering 7.9% of the genome. These are classified into:

| cCRE Class | Abbreviation | Definition | Count (human) |
|-----------|-------------|-----------|--------------|
| Promoter-like | PLS | DNase + H3K4me3 ± H3K27ac near TSS | ~34,000 |
| Proximal enhancer-like | pELS | DNase + H3K27ac within 2kb of TSS | ~46,000 |
| Distal enhancer-like | dELS | DNase + H3K27ac >2kb from TSS | ~670,000 |
| CTCF-only | CTCF-only | DNase + CTCF, no H3K4me3/H3K27ac | ~83,000 |
| DNase-H3K4me3 | DNase-H3K4me3 | DNase + H3K4me3, not near TSS | ~93,000 |

These cCREs are accessible via the SCREEN web interface and provide the foundation for variant annotation.

### Literature Support

- **ENCODE Project Consortium 2020** (Nature, ~1,656 citations): Registry of 926,535 human cCREs. The primary resource for variant-to-regulatory-element annotation. [DOI](https://doi.org/10.1038/s41586-020-2493-4)
- **Boyle et al. 2012** (Genome Research, ~2,623 citations): RegulomeDB — integrates ENCODE ChIP-seq, DNase-seq, eQTLs to score non-coding variants on a 1–6 scale. [DOI](https://doi.org/10.1101/gr.137323.112)
- **Kircher et al. 2014** (Nature Genetics, ~5,719 citations): CADD — Combined Annotation-Dependent Depletion. SVM trained on 14.7M simulated vs. high-frequency alleles, pre-computes scores for all 8.6B possible human SNVs. [DOI](https://doi.org/10.1038/ng.2892)
- **Rentzsch et al. 2019** (Nucleic Acids Research, ~1,500 citations): CADD v1.4/v1.6 update with GRCh38 support. [DOI](https://doi.org/10.1093/nar/gky1016)
- **Finucane et al. 2015** (Nature Genetics, ~2,253 citations): Stratified LD Score Regression (S-LDSC) — partitions SNP heritability into functional categories using GWAS summary statistics. Foundational for quantifying how much disease heritability is attributable to ENCODE-defined regulatory elements. [DOI](https://doi.org/10.1038/ng.3404)
- **Iotchkova et al. 2019** (Nature Genetics, ~157 citations): GARFIELD — GWAS enrichment in regulatory annotations with LD correction, allele frequency, and TSS distance confounders. [DOI](https://doi.org/10.1038/s41588-018-0322-6)
- **Wang et al. 2020** (JRSS-B, ~500 citations): SuSiE — Sum of Single Effects model for Bayesian fine-mapping, outputs credible sets per independent signal. [DOI](https://doi.org/10.1111/rssb.12388)
- **Weissbrod et al. 2020** (Nature Genetics, ~200 citations): PolyFun — leverages ENCODE/Roadmap functional annotations as prior causal probabilities for fine-mapping. PolyFun+SuSiE identified 32% more causal variants than SuSiE alone. [DOI](https://doi.org/10.1038/s41588-020-00735-5)
- **Nasser et al. 2021** (Nature, ~468 citations): ABC model enhancer-gene maps in 131 cell types. Links 5,036 GWAS signals to 2,249 genes. >20-fold enrichment of causal variants in cell-type-specific predicted enhancers. [DOI](https://doi.org/10.1038/s41586-021-03446-x)
- **Broekema et al. 2020** (Open Biology, ~107 citations): Practical review of post-GWAS fine-mapping and gene prioritization strategies. [DOI](https://doi.org/10.1098/rsob.190221)
- **Schaub et al. 2012** (Genome Research, ~675 citations): Early framework linking ENCODE functional data with GWAS disease associations. Functional annotations for up to 80% of reported associations. [DOI](https://doi.org/10.1101/gr.136127.111)
- **Maurano et al. 2012** (Science, ~2,800 citations): Systematic demonstration that disease-associated variants concentrate in DNase I hypersensitive sites. 88% of variant-containing DHSs are active during fetal development. Enabled de novo identification of pathogenic cell types. [DOI](https://doi.org/10.1126/science.1222794)
- **Amemiya et al. 2019** (Scientific Reports, ~1,372 citations): ENCODE Blacklist — regions producing artifactual signal in functional genomics. Must filter before annotation. [DOI](https://doi.org/10.1038/s41598-019-45839-z)

## Step 1: Define the Variant Set and Disease Context

Before any annotation, clarify the input:

### Variant Set Types
| Input Type | Description | LD Consideration |
|-----------|------------|-----------------|
| GWAS lead SNPs | Top associations per locus | Must expand to LD proxies (r² > 0.8) |
| Fine-mapped credible sets | Post-fine-mapping variants with posterior probabilities | Already LD-aware — annotate directly |
| eQTL variants | Expression-associated SNPs | May need LD expansion depending on source |
| Rare variants (ClinVar) | Pathogenic/likely pathogenic | No LD concern — annotate directly |
| Candidate variants | User-curated list | Clarify whether LD expansion is needed |

### LD Awareness is Critical

**A GWAS lead SNP is NOT necessarily causal.** It is the variant with the strongest statistical signal, but the true causal variant may be any of the dozens to hundreds of SNPs in LD. Before annotation:

- If the user provides **lead SNPs only**: recommend expanding to LD proxies (r² ≥ 0.8 in the relevant population) using LDlink, LDproxy, or 1000 Genomes
- If the user provides **credible sets from fine-mapping**: no expansion needed — these already account for LD
- If the user provides **a single variant of known interest**: proceed directly

## Step 2: Map Disease to Relevant Tissues

ENCODE regulatory elements are **highly tissue-specific**. An enhancer active in liver may be completely silent in brain. The disease context determines which ENCODE data to query.

### Common Disease-Tissue Mappings
| Disease Category | Primary Tissues | Key ENCODE Biosamples |
|-----------------|----------------|----------------------|
| Type 2 diabetes | Pancreas, liver, adipose, muscle | pancreas tissue, HepG2, adipose tissue |
| Alzheimer's disease | Brain (hippocampus, cortex) | brain tissue, astrocytes, neurons |
| Cardiovascular | Heart, blood vessels | heart tissue, HUVEC, aorta |
| Blood disorders | Blood, bone marrow | K562, GM12878, CD34+ cells |
| Autoimmune | Immune cells, thymus | GM12878, Treg, Th17, monocytes |
| Cancer | Tissue of origin | K562 (CML), HepG2 (liver), MCF-7 (breast), A549 (lung) |
| Inflammatory bowel | Intestine, colon | intestine tissue, sigmoid colon |
| Respiratory | Lung | lung tissue, A549 |

Check what ENCODE data exists for the relevant tissue:
```
encode_get_facets(organ="pancreas")
encode_get_facets(organ="liver")
```

**If the relevant tissue has limited ENCODE data**: check whether Tier 1 cell lines (K562, GM12878, H1-hESC) or Roadmap Epigenomics data can serve as proxies. Document the tissue mismatch explicitly.

## Step 3: Retrieve Tissue-Specific Functional Data

For each disease-relevant tissue, systematically gather ENCODE data layers:

### Layer 1: Chromatin Accessibility (where regulation happens)
```
encode_search_experiments(assay_title="ATAC-seq", organ="...", biosample_type="tissue")
encode_search_experiments(assay_title="DNase-seq", organ="...", biosample_type="tissue")
```

### Layer 2: Active Regulatory Marks (what type of element)
```
# Active enhancers + promoters
encode_search_experiments(assay_title="Histone ChIP-seq", target="H3K27ac", organ="...")
# Active promoters specifically
encode_search_experiments(assay_title="Histone ChIP-seq", target="H3K4me3", organ="...")
# Enhancer mark (active + poised)
encode_search_experiments(assay_title="Histone ChIP-seq", target="H3K4me1", organ="...")
# Repressive marks (for context)
encode_search_experiments(assay_title="Histone ChIP-seq", target="H3K27me3", organ="...")
```

### Layer 3: Transcription Factor Binding (who binds there)
```
encode_search_experiments(assay_title="TF ChIP-seq", organ="...")
# CTCF specifically for insulator/boundary annotation
encode_search_experiments(assay_title="TF ChIP-seq", target="CTCF", organ="...")
```

### Layer 4: 3D Chromatin (enhancer-gene connections)
```
encode_search_experiments(assay_title="Hi-C", organ="...")
encode_search_experiments(assay_title="ChIA-PET", organ="...")
```

### Layer 5: Gene Expression (for target gene validation)
```
encode_search_experiments(assay_title="total RNA-seq", organ="...", biosample_type="tissue")
```

For each experiment, get peak files:
```
encode_list_files(
    experiment_accession="ENCSR...",
    file_format="bed",
    output_type="IDR thresholded peaks",
    assembly="GRCh38",
    preferred_default=True
)
```

Track all experiments used:
```
encode_track_experiment(accession="ENCSR...", notes="variant annotation - [disease]")
```

## Step 4: Systematic Variant Annotation

**Pre-annotation filter**: Before annotating, filter out variants overlapping ENCODE Blacklist regions (Amemiya et al. 2019, Scientific Reports, 1,372 citations). Blacklisted regions produce artifactual signal in functional genomics assays. Variants in these regions cannot be reliably annotated.
- Human GRCh38: `hg38-blacklist.v2.bed.gz` from [Boyle-Lab/Blacklist](https://github.com/Boyle-Lab/Blacklist)
- Mouse mm10: `mm10-blacklist.v2.bed.gz`

For each variant, determine overlap with functional elements using a tiered approach:

### Tier 1: cCRE Overlap (ENCODE SCREEN)
Does the variant fall within any ENCODE cCRE in the relevant tissue?
- **PLS overlap** → variant in promoter-like element
- **pELS/dELS overlap** → variant in enhancer-like element
- **CTCF-only overlap** → variant may disrupt insulator/boundary
- **No cCRE overlap** → variant outside cataloged regulatory elements (but may still be functional in untested cell types)

### Tier 2: Chromatin State Classification
Using downloaded peak files, classify each variant's chromatin context:

| Variant Context | Interpretation | Confidence |
|----------------|---------------|-----------|
| DNase/ATAC peak + H3K27ac + H3K4me3 | Active promoter | High |
| DNase/ATAC peak + H3K27ac + H3K4me1 (no H3K4me3) | Active enhancer | High |
| DNase/ATAC peak + H3K4me1 + H3K27me3 | Poised/bivalent enhancer | Medium |
| DNase/ATAC peak only | Open chromatin, possible regulatory | Medium |
| H3K27me3 broad domain | Polycomb-repressed | Medium |
| TF ChIP-seq peak | Direct TF binding site | High (if peak is narrow) |
| No overlap with any mark | Not active in tested tissue | Low (may be active elsewhere) |

### Tier 3: TF Binding Disruption
If the variant overlaps a TF ChIP-seq peak:
- Identify which TFs bind at the variant position
- Multiple TF binding = regulatory hub (higher confidence)
- Check whether the variant disrupts a known TF binding motif (requires external motif analysis with HOMER, MEME, or similar)

### Tier 4: Tissue Specificity Assessment
Compare the variant's annotation across multiple tissues:
- **Tissue-specific enhancer**: Active only in disease-relevant tissue → strong candidate
- **Constitutive element**: Active across many tissues → less disease-specific
- **Tissue-discordant**: Active in unrelated tissue → lower priority for this disease

## Step 5: Fine-Mapping Integration

If the user has GWAS summary statistics (not just lead SNPs), recommend fine-mapping to identify credible causal variants:

### Fine-Mapping Hierarchy (Broekema et al. 2020)
1. **Statistical fine-mapping** (SuSiE, FINEMAP): Identifies credible sets of potentially causal variants per locus
2. **Functionally-informed fine-mapping** (PolyFun + SuSiE): Uses ENCODE/Roadmap annotations as priors to improve causal variant identification — identifies ~32% more high-confidence causal variants (Weissbrod et al. 2020)
3. **Colocalization** (coloc, eCAVIAR): Tests whether GWAS and eQTL signals share the same causal variant

### Key Principle
Fine-mapping BEFORE functional annotation is more powerful than annotation alone. A variant with posterior inclusion probability (PIP) > 0.5 that also overlaps a tissue-specific enhancer is a much stronger candidate than either line of evidence alone.

If fine-mapping is not feasible (no summary statistics available), document this limitation explicitly.

## Step 6: Enrichment Testing

For variant sets (not single variants), test whether variants are enriched in specific regulatory annotations:

### S-LDSC (Finucane et al. 2015)
Partitioned heritability using GWAS summary statistics:
- Tests whether ENCODE-defined regulatory element classes (enhancers, promoters, etc.) explain disproportionate disease heritability
- Requires GWAS summary statistics + LD scores
- Can partition by cell type using ENCODE tissue-specific annotations
- **Interpretation**: If disease heritability is enriched in pancreatic islet enhancers (e.g., 10x enrichment), this validates the tissue mapping in Step 2

### GARFIELD (Iotchkova et al. 2019)
Enrichment testing with proper LD correction:
- Tests whether GWAS variants are enriched in ENCODE regulatory annotations
- Corrects for LD, allele frequency, and distance to TSS
- Available as R package
- **Advantage over naive overlap**: Accounts for the fact that regulatory elements tend to be in gene-dense, LD-rich regions

### When to Use Each
| Scenario | Recommended Method |
|---------|-------------------|
| Full GWAS summary statistics available | S-LDSC (most powerful) |
| Lead SNPs + p-values only | GARFIELD |
| Small variant set (<50 variants) | Direct overlap (enrichment testing underpowered) |

## Step 7: Variant-to-Gene Mapping

Identifying the target gene is often harder than identifying the regulatory element. The nearest gene is frequently NOT the target — enhancers can regulate genes over distances >1 Mb.

### Approach 1: ABC Model (Nasser et al. 2021)
Activity-By-Contact model uses ENCODE ATAC-seq + H3K27ac + Hi-C to predict enhancer-gene links:
- Available for 131 cell types/tissues
- Linked 5,036 GWAS signals to 2,249 genes across 72 diseases
- >20-fold enrichment of causal variants in cell-type-specific enhancers
- **Use when**: Hi-C + H3K27ac + ATAC-seq all available for your tissue

### Approach 2: Hi-C/ChIA-PET Chromatin Contacts
```
encode_search_experiments(assay_title="Hi-C", organ="...")
```
- Check whether the variant's enhancer physically contacts a gene promoter
- Loop-level resolution (~5–10 kb) is sufficient for most enhancer-gene assignments
- **Caveat**: Not all enhancer-promoter contacts are functional

### Approach 3: Correlation-Based
- Correlate enhancer activity (H3K27ac) with gene expression (RNA-seq) across ENCODE biosamples
- Requires data from multiple tissues/conditions
- Higher correlation = more likely regulatory relationship

### Approach 4: eQTL Colocalization
- If the variant is an eQTL in GTEx or ENCODE RNA-seq:
  - The eQTL target gene is a strong candidate
  - Colocalization (coloc, eCAVIAR) tests whether GWAS and eQTL share the same causal variant
- Cross-reference with Open Targets (if available via MCP)

## Step 8: Prioritization Framework

After completing all annotation layers, prioritize variants using a scoring approach:

### Evidence Scoring
| Evidence Layer | Points | Rationale |
|---------------|--------|-----------|
| In fine-mapped credible set (PIP > 0.1) | +3 | Statistical evidence of causality |
| Overlaps tissue-specific cCRE | +2 | Active regulatory element in relevant tissue |
| Overlaps tissue-specific ATAC/DNase peak | +2 | Open chromatin in relevant tissue |
| Overlaps H3K27ac peak (tissue-specific) | +2 | Active enhancer/promoter |
| Overlaps TF ChIP-seq peak | +1 | Direct protein-DNA interaction |
| Disrupts known TF motif | +2 | Mechanistic evidence |
| ABC model links to known disease gene | +3 | Enhancer-gene connection |
| eQTL for nearby gene in relevant tissue | +2 | Expression association |
| Hi-C contact with gene promoter | +1 | Physical proximity |
| RegulomeDB score 1a–1f | +2 | Integrated regulatory evidence |
| CADD score > 15 (top 3% deleterious) | +1 | Evolutionary constraint |

### Priority Categories
- **Score ≥ 8**: High-priority causal candidate — recommend for experimental validation
- **Score 4–7**: Moderate priority — functional but less certain
- **Score 1–3**: Low priority — limited evidence, may be tag SNP
- **Score 0**: No functional evidence in tested tissues — try additional biosamples

**This scoring is a guide, not a definitive ranking.** A variant with a single strong piece of evidence (e.g., disrupts a motif for a known disease TF) may be more compelling than one with many weak overlaps.

## Step 9: Log Provenance

Document the full annotation:
```
encode_log_derived_file(
    file_path="/path/to/variant_annotations.tsv",
    source_accessions=["ENCSR...", "ENCSR...", ...],
    description="Functional annotation of [N] GWAS variants for [disease] using ENCODE H3K27ac, ATAC-seq, TF ChIP-seq, and Hi-C in [tissue]",
    file_type="variant_annotation",
    tool_used="bedtools intersect + custom scoring",
    parameters="LD expansion r2>0.8 EUR, GRCh38, IDR thresholded peaks, priority scoring v1"
)
```

Link to external references:
```
encode_link_reference(
    experiment_accession="ENCSR...",
    reference_type="doi",
    reference_id="10.xxxx/original_gwas_doi",
    description="Original GWAS study providing variant set"
)
```

## Pitfalls and Edge Cases

### LD Structure Awareness
- **Never annotate lead SNPs alone** without acknowledging LD. The lead SNP has the strongest statistical signal, but the causal variant is often a different SNP in LD.
- LD patterns are population-specific — use appropriate population reference (EUR, EAS, AFR, etc.)
- Fine-mapped credible sets bypass this issue entirely

### Tissue Relevance
- An enhancer active in K562 (CML cell line) may not reflect normal hematopoiesis
- Cell lines are immortalized and may have aberrant chromatin states
- Primary tissue > primary cells > cell lines for disease relevance
- If the relevant tissue is not in ENCODE, document this gap explicitly

### Functional ≠ Causal
- Overlapping a regulatory element does NOT prove the variant is causal
- The variant must actually DISRUPT the element's function (e.g., break a TF binding motif)
- Functional validation (CRISPR, MPRA, reporter assay) is the gold standard

### Assembly Consistency
- All variants and ENCODE data MUST use the same genome assembly (GRCh38 recommended)
- If variants are in hg19/GRCh37, liftOver before annotation OR use hg19 ENCODE files
- NEVER mix assemblies — coordinates will not match

### Multiple Testing
- When annotating many variants across many regulatory annotations, the probability of spurious overlap increases
- Enrichment testing (S-LDSC, GARFIELD) properly accounts for this
- For individual variants, require multiple lines of converging evidence

### Nearest Gene Fallacy
- The nearest gene to a variant is the correct target in only ~50–60% of cases
- Enhancers can skip over intervening genes to regulate distant targets
- Always use enhancer-gene linking (ABC model, Hi-C) rather than simple proximity

### Cell Line vs. Primary Tissue
- ENCODE Tier 1 cell lines (K562, GM12878, H1-hESC) have the most comprehensive data but are transformed/immortalized
- Regulatory landscapes in cell lines may differ substantially from primary tissue
- Use cell line data as a starting point, but validate key findings against tissue data when available

## Summary Statistics to Report

For the final variant annotation, report:
- Total variants annotated and source (GWAS catalog, fine-mapping, etc.)
- Number overlapping ENCODE cCREs (by class: PLS, pELS, dELS, CTCF-only)
- Tissue(s) used for annotation and justification
- Number of ENCODE experiments queried (per assay type)
- Fine-mapping status (was it performed? method used?)
- Enrichment results (if variant set is large enough)
- Top prioritized variants with evidence summary
- Variant-to-gene links identified and method used

## Walkthrough: Multi-Source Variant Annotation for ENCODE Regulatory Variants

**Goal**: Comprehensively annotate variants in ENCODE-defined regulatory elements by combining Ensembl VEP, ClinVar, gnomAD, and GWAS Catalog data into a unified variant annotation pipeline.
**Context**: Individual annotation databases provide partial information. Combining them creates a complete picture of variant function, clinical significance, and population context.

### Step 1: Define the regulatory variant set

Start with ENCODE ATAC-seq peaks to define accessible regulatory regions:
```
encode_search_experiments(assay_title="ATAC-seq", organ="pancreas", organism="Homo sapiens")
```

Expected output:
```json
{
  "total": 6,
  "results": [
    {"accession": "ENCSR400PAN", "assay_title": "ATAC-seq", "biosample_summary": "islet of Langerhans", "status": "released"}
  ]
}
```

### Step 2: Download peaks and extract variant positions

```
encode_download_files(accessions=["ENCFF500ISL"], download_dir="/data/variant_annotation")
```

### Step 3: Layer 1 — Ensembl VEP consequence prediction

Using Ensembl REST API:
```
POST https://rest.ensembl.org/vep/human/region
{"variants": ["10 114758349 . T C"]}
```

Result: `regulatory_region_variant` in active promoter region.

### Step 4: Layer 2 — ClinVar clinical significance

```
GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=clinvar&term=rs7903146
```

Result: `Pathogenic` for type 2 diabetes mellitus.

### Step 5: Layer 3 — gnomAD population frequency

```graphql
{
  variant(dataset: gnomad_r4, variantId: "10-114758349-T-C") {
    genome { af populations { id af } }
  }
}
```

Result: AF=0.30 globally, AF=0.08 in East Asian populations.

### Step 6: Layer 4 — GWAS Catalog trait association

```
GET https://www.ebi.ac.uk/gwas/rest/api/singleNucleotidePolymorphisms/rs7903146
```

Result: Associated with type 2 diabetes (p=2.4×10⁻¹²), fasting glucose, insulin resistance.

### Step 7: Generate unified annotation report

Combine all layers:
| Field | Value |
|---|---|
| Variant | rs7903146 (chr10:114758349 T>C) |
| VEP consequence | regulatory_region_variant |
| ClinVar significance | Pathogenic |
| gnomAD AF | 0.30 (global) |
| GWAS trait | Type 2 diabetes (p=2.4e-12) |
| ENCODE context | In islet ATAC-seq peak (open chromatin) |

**Interpretation**: This is a well-characterized T2D risk variant in an islet-specific regulatory element. The 30% global AF confirms it's a common risk variant, consistent with its role in polygenic T2D risk.

### Integration with downstream skills
- ENCODE peaks from → **regulatory-elements** define the variant search space
- VEP annotations from → **ensembl-annotation** provide consequence predictions
- Clinical data from → **clinvar-annotation** adds pathogenicity calls
- Frequency data from → **gnomad-variants** provides population context
- Trait associations from → **gwas-catalog** connect variants to diseases
- Expression effects validated via → **gtex-expression** eQTL data

## Code Examples

### 1. Find regulatory experiments for variant context
```
encode_search_experiments(assay_title="ATAC-seq", organ="pancreas", organism="Homo sapiens")
```

Expected output:
```json
{
  "total": 6,
  "results": [
    {"accession": "ENCSR400PAN", "assay_title": "ATAC-seq", "biosample_summary": "islet of Langerhans"}
  ]
}
```

### 2. Get peak files for variant intersection
```
encode_list_files(accession="ENCSR400PAN", file_format="bed", output_type="IDR thresholded peaks", assembly="GRCh38")
```

Expected output:
```json
{
  "files": [
    {"accession": "ENCFF500ISL", "output_type": "IDR thresholded peaks", "file_format": "bed narrowPeak", "file_size_mb": 0.8}
  ]
}
```

### 3. Track variant annotation experiments
```
encode_track_experiment(accession="ENCSR400PAN", notes="Islet ATAC-seq for multi-source variant annotation pipeline")
```

Expected output:
```json
{
  "status": "tracked",
  "accession": "ENCSR400PAN",
  "notes": "Islet ATAC-seq for multi-source variant annotation pipeline"
}
```

## Integration

| This skill produces... | Feed into... | Purpose |
|---|---|---|
| Unified variant annotation table | **disease-research** | Connect annotated variants to disease mechanisms |
| VEP-annotated variants | **ensembl-annotation** | Detailed consequence prediction for regulatory variants |
| ClinVar-annotated variants | **clinvar-annotation** | Clinical significance assessment |
| Frequency-filtered variants | **gnomad-variants** | Population frequency context |
| Trait-associated variants | **gwas-catalog** | GWAS evidence for variant-disease connections |
| Regulatory variant BED | **peak-annotation** | Assign annotated variants to target genes |
| Annotated variant reports | **visualization-workflow** | Generate variant annotation summary visualizations |
| Variant-gene links | **gtex-expression** | Validate expression effects of annotated variants |

## Related Skills

- `regulatory-elements` — Characterizing the regulatory elements themselves (not variant-specific)
- `multi-omics-integration` — Combining ENCODE data types for deeper regulatory analysis
- `disease-research` — Broader disease-focused workflows using ENCODE
- `quality-assessment` — Evaluating quality of ENCODE experiments used in annotation
- `histone-aggregation` — Aggregating histone ChIP-seq peaks across samples for annotation
- `accessibility-aggregation` — Aggregating ATAC-seq/DNase-seq peaks across samples
- `hic-aggregation` — Aggregated Hi-C data improves enhancer-gene linkage for variant interpretation
- `single-cell-encode` — Cell type-resolved scATAC-seq peaks improve variant annotation in heterogeneous tissues
- `epigenome-profiling` — Build a complete epigenomic profile of the disease tissue to contextualize variants
- `data-provenance` — Document the full variant annotation pipeline for reproducibility
- `pipeline-guide` — Guidance for running fine-mapping, S-LDSC, and other computational pipelines
- `gnomad-variants` — Population frequency and gene constraint data for variant prioritization
- `ensembl-annotation` — VEP consequence prediction, CADD/REVEL scores, Regulatory Build overlap
- `ucsc-browser` — Retrieve ENCODE tracks and sequence context from UCSC for variant regions
- `clinvar-annotation` — Annotate variants with clinical significance, pathogenicity, and review status
- `gwas-catalog` — Check GWAS associations for variants and retrieve trait-associated loci
- `gtex-expression` — Check tissue expression of variant-associated genes across 54 GTEx tissues
- `jaspar-motifs` — Check if variant disrupts transcription factor binding motif
- `publication-trust` — Verify literature claims backing analytical decisions

## Presenting Results

- Present variant annotations as: variant | position | gene | consequence | population_freq | clinical_significance. Highlight pathogenic or rare variants. Suggest: "Would you like to check if these variants fall in ENCODE regulatory regions?"

## For the request: "$ARGUMENTS"
