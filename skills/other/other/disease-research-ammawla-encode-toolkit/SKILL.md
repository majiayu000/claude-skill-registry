---
name: disease-research
description: Use ENCODE functional genomics data for disease mechanism research. Use when the user wants to connect GWAS variants to regulatory elements, annotate disease-associated loci with functional data, identify therapeutic targets from epigenomic data, build disease regulatory models, cross-reference with clinical trials and drug databases, or conduct any disease-focused, pathology-driven, or clinical variant interpretation workflow. Covers the full pipeline from disease-tissue mapping through GWAS variant annotation, heritability enrichment, cancer epigenomics, drug target identification, and clinical trial cross-referencing. Integrates ENCODE with Open Targets, PubMed, ClinicalTrials.gov, and bioRxiv.
---

# Disease Research with ENCODE Functional Genomics

## When to Use

- User wants to connect GWAS variants to ENCODE regulatory elements for disease mechanism research
- User asks about "disease", "pathology", "therapeutic targets", "GWAS interpretation", or "clinical variants"
- User needs to annotate disease-associated loci with functional genomics data from ENCODE
- User wants to identify drug targets from epigenomic evidence using Open Targets integration
- Example queries: "find enhancers disrupted by diabetes GWAS hits", "identify drug targets from ChIP-seq data", "connect my disease variants to regulatory elements"

Leverage ENCODE's 926,535 cCREs and multi-layer functional data to understand disease mechanisms, interpret disease-associated variants, identify therapeutic targets, and connect genomic findings to clinical applications.

## Scientific Rationale

**The question**: "How can ENCODE functional genomics help me understand a disease's molecular mechanisms and identify actionable targets?"

Over 90% of disease-associated variants from GWAS fall in non-coding regions (Maurano et al. 2012). They disrupt regulatory elements controlling gene expression, not protein sequences. ENCODE provides the most comprehensive catalog of these elements across hundreds of cell types and tissues. This skill connects (1) genetic association data, (2) ENCODE functional annotations, and (3) clinical/pharmacological databases for druggable targets.

## Literature Foundation

| Reference | Year | Journal | Key Contribution | Citations | DOI |
|-----------|------|---------|-----------------|-----------|-----|
| ENCODE Phase 3 | 2020 | Nature | 926,535 human cCREs across 400+ biosamples, SCREEN portal | ~1,656 | [10.1038/s41586-020-2493-4](https://doi.org/10.1038/s41586-020-2493-4) |
| Maurano et al. | 2012 | Science | Disease variants enriched in regulatory DNA; DNase hotspots explain 76.6% of GWAS SNPs | ~3,500 | [10.1126/science.1222794](https://doi.org/10.1126/science.1222794) |
| Finucane et al. | 2015 | Nat Genet | S-LDSC partitions heritability into functional annotations; ENCODE categories explain disproportionate heritability | ~2,253 | [10.1038/ng.3404](https://doi.org/10.1038/ng.3404) |
| Nasser et al. | 2021 | Nature | ABC model links enhancers to genes in 131 cell types; connected 5,036 GWAS signals to 2,249 genes | ~468 | [10.1038/s41586-021-03446-x](https://doi.org/10.1038/s41586-021-03446-x) |
| Roadmap Epigenomics | 2015 | Nature | 111 reference epigenomes; tissue-specific chromatin states; disease variant enrichment in tissue-specific marks | ~5,810 | [10.1038/nature14248](https://doi.org/10.1038/nature14248) |
| Visscher et al. | 2017 | Am J Hum Genet | GWAS review — 10 years of discoveries, statistical frameworks, shift toward functional interpretation | ~2,500 | [10.1016/j.ajhg.2017.06.005](https://doi.org/10.1016/j.ajhg.2017.06.005) |
| Buniello et al. | 2019 | Nucleic Acids Res | GWAS Catalog — curated repository; >250,000 SNP-trait associations | ~3,000 | [10.1093/nar/gky1120](https://doi.org/10.1093/nar/gky1120) |
| Ochoa et al. | 2021 | Nucleic Acids Res | Open Targets Platform — integrates GWAS, functional genomics, drugs for systematic target identification | ~600 | [10.1093/nar/gkaa1027](https://doi.org/10.1093/nar/gkaa1027) |

## Step 1: Map Disease to Relevant Tissues

ENCODE regulatory elements are highly tissue-specific. Correct tissue mapping is the single most important decision.

### Disease-Tissue Mapping Table

| Disease Category | Primary Tissues | Key Cell Types | ENCODE Cell Lines | Example Diseases |
|-----------------|----------------|---------------|-------------------|-----------------|
| Neurological | brain (cortex, hippocampus, cerebellum) | neurons, astrocytes, microglia | SK-N-SH, SK-N-DZ, BE2C | Alzheimer's, Parkinson's, schizophrenia |
| Cardiovascular | heart, aorta, blood vessels | cardiomyocytes, endothelial, smooth muscle | HUVEC, HCASMC | coronary artery disease, heart failure |
| Metabolic | pancreas, liver, adipose, muscle | beta cells, hepatocytes, adipocytes | HepG2, Panc1 | type 2 diabetes, NAFLD, obesity |
| Cancer | tissue of origin | tumor cells, microenvironment | K562, HepG2, MCF-7, A549, HCT116, PC-3 | leukemia, breast cancer, lung cancer |
| Autoimmune | blood, immune organs, thymus | T cells, B cells, macrophages | GM12878, Jurkat | RA, lupus, MS, type 1 diabetes |
| Respiratory | lung, trachea | alveolar epithelial, bronchial | A549, IMR-90 | asthma, COPD, pulmonary fibrosis |
| Renal | kidney | podocytes, tubular epithelial | HEK293 | CKD, IgA nephropathy, FSGS |
| Hepatic | liver, bile duct | hepatocytes, cholangiocytes | HepG2, Hep3B | NAFLD, cirrhosis, hepatitis |
| Endocrine | thyroid, adrenal, pituitary, pancreas | thyrocytes, adrenal cortical, beta cells | — | hypothyroidism, Cushing's |
| Musculoskeletal | bone, cartilage, skeletal muscle | osteoblasts, chondrocytes, myocytes | — | osteoarthritis, osteoporosis |
| Gastrointestinal | intestine, colon, stomach | epithelial, goblet, Paneth cells | HCT116, Caco-2 | IBD, Crohn's, celiac |
| Hematological | blood, bone marrow | HSCs, erythrocytes, megakaryocytes | K562, GM12878, CD34+ | sickle cell, thalassemia, AML |

Check ENCODE availability:
```
encode_get_facets(organ="pancreas")
encode_get_facets(organ="brain")
```

**If tissue has limited data**: Use Tier 1 cell lines (K562, GM12878, H1-hESC) or Roadmap Epigenomics as proxies. Document the mismatch explicitly.

## Step 2: Find Disease-Relevant ENCODE Data

### For GWAS / Genetic Diseases
Open chromatin and active enhancers in disease tissue (Maurano et al. 2012):
```
encode_search_experiments(assay_title="ATAC-seq", organ="...", biosample_type="tissue")
encode_search_experiments(assay_title="Histone ChIP-seq", target="H3K27ac", organ="...")
encode_search_experiments(assay_title="DNase-seq", organ="...", biosample_type="tissue")
```
Then use the `variant-annotation` skill to overlap variants with functional elements.

### For Cancer Research
ENCODE cancer cell lines (NOT tumors — see Cancer Epigenomics section below):
```
encode_search_experiments(biosample_term_name="K562")    # CML
encode_search_experiments(biosample_term_name="HepG2")   # Hepatocellular carcinoma
encode_search_experiments(biosample_term_name="MCF-7")   # ER+ breast cancer
encode_search_experiments(biosample_term_name="A549")     # Lung adenocarcinoma
```

### For Perturbation Studies
```
encode_search_experiments(perturbed=True, organ="...")
encode_search_experiments(assay_title="CRISPR screen", organ="...")
```

### For Rare Diseases
1. Search for closest available tissue; 2. Check Roadmap Epigenomics; 3. Use Tier 1 cell lines as baseline; 4. Document tissue proxy limitations.

## Step 3: Cross-Reference with Disease Databases

### PubMed — Disease Literature
```
search_articles(query="[DISEASE] AND (ENCODE OR regulatory element OR enhancer)")
```
Track experiments and link papers:
```
encode_track_experiment(accession="ENCSR...", notes="Disease research - [disease]")
encode_get_citations(accession="ENCSR...")
encode_link_reference(experiment_accession="ENCSR...", reference_type="pmid", reference_id="12345678")
```

### ClinicalTrials.gov — Active Trials
```
search_trials(condition="[DISEASE]", intervention="[TARGET_GENE or DRUG]", status=["RECRUITING"])
```
Link trials: `encode_link_reference(experiment_accession="ENCSR...", reference_type="nct_id", reference_id="NCT...")`

### Open Targets — Target-Disease Associations
```
search_entities(query_strings=["[GENE_NAME]"])
query_open_targets_graphql(
    query_string="query target($ensemblId: String!) { target(ensemblId: $ensemblId) { approvedSymbol knownDrugs { rows { drug { name } phase mechanismOfAction } } } }",
    variables={"ensemblId": "ENSG..."}
)
```

### bioRxiv — Recent Preprints
```
search_preprints(category="genetics", recent_days=90)
encode_link_reference(experiment_accession="ENCSR...", reference_type="preprint_doi", reference_id="10.1101/...")
```

## Step 4: Annotate Disease Variants with ENCODE Functional Data

### Variant-to-Regulatory-Element Annotation

| Overlap Category | ENCODE Data Type | Interpretation |
|-----------------|-----------------|----------------|
| cCRE-PLS | DNase + H3K4me3 near TSS | Variant in promoter-like element |
| cCRE-dELS | DNase + H3K27ac >2kb from TSS | Variant in distal enhancer |
| cCRE-pELS | DNase + H3K27ac within 2kb of TSS | Variant in proximal enhancer |
| cCRE-CTCF | DNase + CTCF | Variant may disrupt insulator/boundary |
| TF ChIP peak | TF ChIP-seq | Variant at TF binding site |
| No overlap | — | Not active in tested tissues |

Retrieve functional data files:
```
encode_list_files(experiment_accession="ENCSR...", file_format="bed", output_type="IDR thresholded peaks", assembly="GRCh38", preferred_default=True)
```

### GWAS Variant Interpretation Workflow (Maurano 2012 + Finucane 2015)

From GWAS hits to candidate causal variants to target genes:
1. **Obtain GWAS loci** from the GWAS Catalog (Buniello et al. 2019) or published study
2. **Expand to LD proxies** (r2 > 0.8) — lead SNPs are NOT necessarily causal
3. **Map to disease tissue** using the tissue mapping table (Step 1)
4. **Overlay with ENCODE cCREs** active in disease tissue
5. **Layer additional annotations**: TF binding, chromatin state, 3D genome
6. **Prioritize**: Variants in tissue-specific enhancers with TF binding = highest priority
7. **Link to target genes** via ABC model (Nasser et al. 2021), Hi-C, or eQTL colocalization

This reduces a typical locus from 50-200 LD variants to 1-5 high-confidence candidates.

## Step 5: Build the Disease Regulatory Model

6-layer model combining ENCODE data types:

1. **Active regulatory elements**: ATAC-seq + H3K27ac identify enhancers/promoters in disease tissue
2. **TF binding**: TF ChIP-seq maps which factors bind at regulatory elements
3. **Enhancer-gene linkage**: Hi-C/ChIA-PET + ABC model (Nasser et al. 2021) connect enhancers to target genes
4. **Gene expression**: RNA-seq measures baseline expression of candidate targets
5. **Disease variant overlay**: Intersect GWAS/eQTL variants with layers 1-4
6. **Druggable target assessment**: Cross-reference target genes with Open Targets and ClinicalTrials.gov

```
encode_search_experiments(assay_title="ATAC-seq", organ="...", biosample_type="tissue")
encode_search_experiments(assay_title="Histone ChIP-seq", target="H3K27ac", organ="...")
encode_search_experiments(assay_title="TF ChIP-seq", organ="...")
encode_search_experiments(assay_title="Hi-C", organ="...")
encode_search_experiments(assay_title="total RNA-seq", organ="...", biosample_type="tissue")
```

## Step 6: Identify Therapeutic Targets

Connect ENCODE regulatory elements to druggable targets (Ochoa et al. 2021).

**The variant-to-drug pipeline**:
- GWAS variant disrupts an enhancer (ENCODE annotation)
- Enhancer regulates Gene X (ABC model / Hi-C)
- Gene X is druggable (Open Targets tractability)
- Existing drug targets Gene X (Open Targets knownDrugs)
- Clinical trials test that drug (ClinicalTrials.gov)

```
search_entities(query_strings=["[GENE_NAME]"])
query_open_targets_graphql(
    query_string="query target($ensemblId: String!) { target(ensemblId: $ensemblId) { approvedSymbol tractability { label modality value } knownDrugs { count rows { drug { name } phase status } } } }",
    variables={"ensemblId": "ENSG..."}
)
```

Targets with both ENCODE regulatory evidence AND GWAS genetic association are the strongest candidates — orthogonal lines of support.

## Step 7: Validate Findings

### Cross-Study Replication
```
encode_track_experiment(accession="ENCSR...", notes="Validation - independent replicate")
encode_compare_experiments(accession1="ENCSR...", accession2="ENCSR...")
```

### Functional Validation Hierarchy

| Level | Method | Strength | In ENCODE? |
|-------|--------|----------|-----------|
| Strongest | CRISPRi/CRISPRa perturbation | Direct causal test | Yes (ENCODE 4) |
| Strong | MPRA / STARR-seq | High-throughput activity | Yes (ENCODE 4) |
| Moderate | Reporter assays / eQTL coloc | Element activity / statistical | External |
| Supportive | Chromatin annotation / conservation | Biochemical / evolutionary | Yes / External |

```
encode_search_experiments(perturbed=True, organ="...")
encode_search_experiments(assay_title="CRISPR screen", organ="...")
```

## Step 8: Clinical Trial Cross-Reference

```
search_trials(condition="[DISEASE]", intervention="[GENE or DRUG]", status=["RECRUITING"])
search_trials(condition="[DISEASE]", phase=["PHASE2", "PHASE3"])
search_by_sponsor(sponsor_name="[PHARMA]", condition="[DISEASE]", phase=["PHASE3"])
analyze_endpoints(condition="[DISEASE]", phase=["PHASE3"])
```

Link trials to tracked experiments:
```
encode_link_reference(experiment_accession="ENCSR...", reference_type="nct_id", reference_id="NCT...", description="Trial targeting [gene] from ENCODE analysis")
```

## Step 9: Document for Publication

```
encode_track_experiment(accession="ENCSR...", notes="Disease research - [disease] - [layer]")
encode_log_derived_file(
    file_path="/path/to/disease_model.bed",
    source_accessions=["ENCSR...", "ENCSR..."],
    description="Disease regulatory model - active enhancers overlapping GWAS loci",
    file_type="disease_model", tool_used="bedtools intersect + ABC model",
    parameters="GRCh38, IDR thresholded peaks, ABC score > 0.015"
)
encode_get_citations(export_format="bibtex")
encode_export_data(format="csv")
```

## Heritability Enrichment with ENCODE Annotations

S-LDSC (Finucane et al. 2015) quantifies how much disease heritability is attributable to ENCODE-defined annotation categories. This is the most rigorous validation that ENCODE elements are disease-relevant.

**Why it matters**: If heritability is enriched in tissue-specific enhancers (e.g., 15x in pancreatic islet enhancers for T2D), this confirms correct tissue mapping and that regulatory variation drives disease risk.

**Requirements**: Full GWAS summary statistics, LD score files, ENCODE BED annotations, ldsc software.

**Interpretation**: Enrichment > 1 = more heritability than expected by annotation size. Compare across tissues to confirm disease-relevant tissue. Significant enrichment (p < 0.05/n_annotations) validates the ENCODE-based disease model.

## Cancer Epigenomics with ENCODE

| Cell Line | Cancer Type | Key Features | Caveats |
|-----------|------------|-------------|---------|
| K562 | CML | Tier 1 — most ENCODE data; BCR-ABL | Transformed hematopoietic |
| HepG2 | Hepatocellular carcinoma | Tier 2 — extensive liver regulatory data | Well-differentiated |
| MCF-7 | ER+ breast cancer | Hormone-responsive model | ER+ only |
| A549 | Lung adenocarcinoma | Epithelial lung cancer model | KRAS-mutant |
| HCT116 | Colorectal carcinoma | MSI-H model | Not MSS CRC |
| PC-3 | Prostate adenocarcinoma | Androgen-independent | Late-stage only |

**Cell line vs. tumor caveats**: Cell lines are clonal, immortalized, and lack tumor heterogeneity. Regulatory landscapes diverge from primary tumors. High-passage lines accumulate epigenetic drift. Use for hypothesis generation; validate against TCGA/primary tumor data. Comparing cancer cell line vs. normal tissue counterpart (e.g., HepG2 vs. primary liver) can reveal cancer-specific regulatory changes.

## Pitfalls and Common Mistakes

### 1. Tissue Relevance Mismatch
Annotating variants with wrong-tissue data is the most common error. Verify tissue selection against published heritability enrichment (Finucane 2015; Roadmap 2015).

### 2. Cell Line vs. Primary Tissue
Tier 1 cell lines have deepest data but are transformed. Prioritize: primary tissue > primary cells > cell lines. State cell line limitations explicitly.

### 3. LD Confounding
A lead SNP is NOT the causal variant. Always expand to LD proxies (r2 > 0.8) or use fine-mapped credible sets. Annotating only lead SNPs misses the causal variant in most cases.

### 4. Functional Does Not Equal Causal
Regulatory element overlap is necessary but not sufficient. The variant must DISRUPT the element. CRISPRi/MPRA validation is required for proof. Chromatin overlap is context, not mechanism.

### 5. Publication Bias and Ascertainment
ENCODE is biased toward well-studied tissues. Rare disease-relevant tissues may lack coverage. Absence of data does NOT mean absence of regulatory elements.

### 6. Over-Interpreting Regulatory Overlap
Multiple LD variants may overlap regulatory elements by chance. Enrichment testing (S-LDSC, GARFIELD) and fine-mapping distinguish real signal from LD-driven overlap.

## Integration

| This skill produces... | Feed into... | Using tool/skill |
|---|---|---|
| GWAS hits in ENCODE regulatory elements | Drug target identification | cross-reference → Open Targets |
| Disease-tissue regulatory map | Enhancer annotation | regulatory-elements skill |
| Candidate therapeutic targets | Clinical trial search | cross-reference → ClinicalTrials.gov |
| Variant-regulatory element intersections | Variant annotation | variant-annotation + clinvar-annotation |
| Tissue-specific regulatory network | Expression correlation | gtex-expression skill |

## Walkthrough: ENCODE-Driven Disease Mechanism Discovery for Alzheimer's Disease

**Goal**: Use ENCODE regulatory data combined with disease databases to identify candidate regulatory mechanisms underlying Alzheimer's disease risk variants.
**Context**: Alzheimer's GWAS has identified 75+ risk loci, most in non-coding regions. ENCODE maps the regulatory landscape to interpret these variants.

### Step 1: Survey ENCODE data for brain tissue

```
encode_get_facets(facet_field="assay_title", organ="brain", organism="Homo sapiens")
```

Expected output:
```json
{
  "facets": {
    "assay_title": {"Histone ChIP-seq": 120, "TF ChIP-seq": 45, "ATAC-seq": 32, "RNA-seq": 28, "DNase-seq": 22, "Hi-C": 8}
  }
}
```

**Interpretation**: Extensive brain epigenomic data available. Histone ChIP-seq (120 experiments) and ATAC-seq (32) provide the strongest regulatory element maps.

### Step 2: Find brain enhancer experiments

```
encode_search_experiments(assay_title="Histone ChIP-seq", organ="brain", target="H3K27ac", organism="Homo sapiens")
```

Expected output:
```json
{
  "total": 24,
  "results": [
    {"accession": "ENCSR100BRN", "assay_title": "Histone ChIP-seq", "target": "H3K27ac", "biosample_summary": "brain"},
    {"accession": "ENCSR101CTX", "assay_title": "Histone ChIP-seq", "target": "H3K27ac", "biosample_summary": "frontal cortex"}
  ]
}
```

### Step 3: Cross-reference with Alzheimer's GWAS variants

Using → **gwas-catalog** skill:
```
# Query GWAS Catalog for Alzheimer's disease associations
GET https://www.ebi.ac.uk/gwas/rest/api/associations?efoTrait=EFO_0000249
```

Intersect GWAS variants with ENCODE brain H3K27ac peaks to identify risk variants in active brain enhancers.

### Step 4: Annotate candidate regulatory variants

Using → **variant-annotation** pipeline:
1. VEP consequence prediction (→ **ensembl-annotation**)
2. ClinVar pathogenicity (→ **clinvar-annotation**)
3. gnomAD population frequency (→ **gnomad-variants**)
4. Brain-specific gene expression (→ **gtex-expression**)

### Step 5: Identify disease mechanism hypotheses

For each Alzheimer's risk variant in a brain enhancer:
- **Which gene?** → Peak-annotation assigns target genes
- **Which cell type?** → scATAC-seq reveals neuron vs. microglia specificity
- **What pathway?** → Open Targets provides pathway context
- **Existing drugs?** → Open Targets identifies therapeutic opportunities

### Step 6: Generate disease research summary

```
encode_summarize_collection()
```

**Interpretation**: A comprehensive disease research report links ENCODE regulatory data → GWAS variants → annotated variants → candidate genes → therapeutic targets, creating an end-to-end discovery pipeline.

### Integration with downstream skills
- Brain enhancer peaks from → **histone-aggregation** provide the regulatory landscape
- GWAS variants from → **gwas-catalog** define the disease-associated search space
- Variant annotation from → **variant-annotation** provides functional predictions
- Expression validation from → **gtex-expression** confirms tissue-specific gene activity
- Single-cell resolution from → **cellxgene-context** identifies disease-relevant cell types
- Drug targets from Open Targets connect to therapeutic opportunities

## Code Examples

### 1. Survey ENCODE data for a disease-relevant tissue
```
encode_get_facets(facet_field="assay_title", organ="brain", organism="Homo sapiens")
```

Expected output:
```json
{
  "facets": {
    "assay_title": {"Histone ChIP-seq": 120, "ATAC-seq": 32, "RNA-seq": 28, "Hi-C": 8}
  }
}
```

### 2. Find experiments for disease-relevant cell types
```
encode_search_experiments(assay_title="ATAC-seq", biosample_term_name="microglia", organism="Homo sapiens")
```

Expected output:
```json
{
  "total": 4,
  "results": [
    {"accession": "ENCSR200MIC", "assay_title": "ATAC-seq", "biosample_summary": "microglia", "status": "released"}
  ]
}
```

### 3. Get citations for disease research
```
encode_get_citations(accession="ENCSR100BRN")
```

Expected output:
```json
{
  "citations": [
    {"pmid": "31234567", "title": "Brain enhancer atlas reveals Alzheimer regulatory mechanisms", "year": 2023}
  ]
}
```

## Related Skills

- `variant-annotation` — Detailed variant-level functional annotation with ENCODE data
- `regulatory-elements` — Discovering and characterizing regulatory elements independent of disease context
- `quality-assessment` — Evaluating quality of ENCODE experiments used in disease research
- `cross-reference` — Connecting ENCODE data to PubMed, bioRxiv, ClinicalTrials.gov
- `data-provenance` — Tracking the full chain from ENCODE source data to derived disease models
- `epigenome-profiling` — Build tissue epigenomic profiles as the foundation for disease regulatory models
- `single-cell-encode` — Cell type-resolved data for dissecting disease mechanisms in heterogeneous tissues
- `histone-aggregation` — Aggregate histone peaks across donors before disease variant annotation
- `accessibility-aggregation` — Aggregate ATAC-seq peaks across donors for improved sensitivity
- `multi-omics-integration` — Combine RNA, ATAC, histone, and TF data for comprehensive disease regulatory landscapes
- `pipeline-guide` — Guidance for S-LDSC, fine-mapping, and other disease genomics pipelines
- `gnomad-variants` — Population frequency filtering and gene constraint for disease gene prioritization
- `ensembl-annotation` — VEP annotation and phenotype associations from Ensembl
- `ucsc-browser` — UCSC Genome Browser tracks for disease locus visualization
- `geo-connector` — Find complementary disease expression datasets in GEO
- `clinvar-annotation` — Clinical significance of disease variants from ClinVar
- `gwas-catalog` — GWAS trait associations and risk alleles from NHGRI-EBI catalog
- `gtex-expression` — Tissue expression context for disease genes across 54 GTEx tissues
- `publication-trust` — Verify literature claims backing analytical decisions

## Presenting Results

- Present disease-relevant findings as: gene/variant | disease | evidence_type | source | confidence. Show ENCODE regulatory support. Suggest: "Would you like to find clinical trials related to these findings?"

## For the request: "$ARGUMENTS"
