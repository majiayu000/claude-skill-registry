---
name: cross-reference
description: Cross-reference ENCODE data with PubMed, bioRxiv, ClinicalTrials.gov, Open Targets, GTEx, ClinVar, GWAS Catalog, gnomAD, Ensembl, and other scientific databases. Use when the user wants to find publications, preprints, or clinical trials related to ENCODE experiments, chain ENCODE data with other scientific MCP servers, or build translational pipelines from genomic data to clinical application.
---

# Cross-Reference ENCODE with Other Databases

## When to Use

- User wants to connect ENCODE data to publications, clinical trials, or other databases
- User asks to "cross-reference", "link", or "connect" ENCODE with PubMed, bioRxiv, GEO, etc.
- User wants to find clinical trials related to ENCODE genomic targets
- User needs to build translational pipelines from ENCODE regulatory data to disease context
- User asks about drugs targeting genes identified in ENCODE experiments
- User wants to find variant annotations (ClinVar, gnomAD) for ENCODE regulatory regions

Help the user connect ENCODE genomics data to the broader scientific literature, clinical research, drug target discovery, and variant interpretation. This skill is the central hub for all multi-database workflows in the ENCODE Toolkit.

## Cross-Reference Workflows

### ENCODE + PubMed
1. Track an ENCODE experiment to extract PMIDs from publications
2. Use `encode_get_citations` or `encode_get_references` to get PMIDs
3. Pass PMIDs to PubMed tools (`search_articles`, `get_article_metadata`, `find_related_articles`)
4. Find related literature about the same targets, biosamples, or biological questions

### ENCODE + bioRxiv
1. Search bioRxiv for preprints in relevant categories (genomics, genetics, cell biology)
2. Look for preprints that reference ENCODE accession IDs or targets
3. Link discovered preprint DOIs to tracked experiments using `encode_link_reference`

### ENCODE + ClinicalTrials.gov
1. Identify disease-relevant ENCODE data (e.g., pancreatic tissue data for diabetes trials)
2. Use `encode_get_references` to find linked NCT IDs
3. Search ClinicalTrials.gov for trials targeting the same genes/proteins as ENCODE experiments
4. Link relevant trial NCT IDs to experiments using `encode_link_reference`

### ENCODE + Open Targets
1. Identify ENCODE ChIP-seq or CRISPR screen targets of interest
2. Resolve gene symbols to Ensembl Gene IDs via `search_entities`
3. Query Open Targets for disease associations, tractability, and drug candidates
4. Chain from ENCODE functional data to therapeutic hypotheses

### ENCODE + GTEx
1. Find ENCODE regulatory experiments in a tissue of interest
2. Annotate peaks with nearest genes using GENCODE annotations
3. Query GTEx for expression of those genes in the matching tissue
4. Validate that putative regulatory elements sit near actively transcribed genes

### ENCODE + GWAS Catalog + ClinVar
1. Obtain trait-associated variants from the GWAS Catalog
2. Check clinical significance in ClinVar
3. Intersect variant coordinates with ENCODE peak files and cCREs
4. Determine whether disease-associated variants fall in regulatory elements

### ENCODE + Consensus (Academic Search)
1. Search for high-quality research papers about ENCODE targets (H3K27me3, CTCF, etc.)
2. Find systematic reviews and meta-analyses relevant to ENCODE data types
3. Cross-validate ENCODE quality metrics against published benchmarks

### ENCODE + GEO
1. Check ENCODE experiment `dbxrefs` for GEO accessions (format: `GEO:GSExxxxx`)
2. Search GEO E-utilities for complementary datasets in the same tissue/assay
3. Link GEO accessions to tracked experiments using `encode_link_reference`
4. See `geo-connector` skill for detailed GEO API usage

### ENCODE + SRA
Raw sequencing reads for ENCODE experiments are deposited in NCBI SRA. GEO records link to SRA via E-utilities `elink`. For reprocessing ENCODE data or accessing raw reads not on the ENCODE Portal, query SRA via:
```bash
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=gds&db=sra&id=GDS_UID&tool=encode_mcp&email=YOUR_EMAIL"
```

### ENCODE + Ensembl
Use the Ensembl REST API to cross-reference ENCODE targets and regulatory elements with Ensembl annotations. See `ensembl-annotation` skill for VEP, Regulatory Build, and gene lookup endpoints.

---

## Identifier Format Quick Reference

| Identifier | Format | Example | Database | MCP Tool / Skill |
|---|---|---|---|---|
| PMID | numeric string | "35486828" | PubMed | `get_article_metadata` |
| DOI | 10.xxxx/... | "10.1038/s41586-020-2493-4" | CrossRef | `convert_article_ids` |
| NCT ID | NCT + 8 digits | "NCT04567890" | ClinicalTrials.gov | `get_trial_details` |
| GEO Series | GSE + digits | "GSE123456" | GEO/NCBI | `geo-connector` skill |
| GEO Sample | GSM + digits | "GSM1234567" | GEO/NCBI | `geo-connector` skill |
| bioRxiv DOI | 10.1101/YYYY.MM.DD.xxx | "10.1101/2024.06.15.598765" | bioRxiv | `get_preprint` |
| ENCODE Experiment | ENCSR + 6 alphanum | "ENCSR123ABC" | ENCODE | `encode_get_experiment` |
| ENCODE File | ENCFF + 6 alphanum | "ENCFF001AAA" | ENCODE | `encode_get_file_info` |
| Ensembl Gene | ENSG + 11 digits | "ENSG00000102974" | Ensembl | `ensembl-annotation` skill |
| Ensembl Transcript | ENST + 11 digits | "ENST00000264010" | Ensembl | `ensembl-annotation` skill |
| SRA Study | SRP + digits | "SRP123456" | SRA/NCBI | E-utilities |
| SRA Run | SRR + digits | "SRR1234567" | SRA/NCBI | E-utilities |
| ROR ID | 9 chars | "021nxhr62" | ROR | `search_by_funder` |
| ChEMBL ID | CHEMBL + digits | "CHEMBL25" | Open Targets | `search_entities` |
| rsID | rs + digits | "rs7903146" | dbSNP/ClinVar | `clinvar-annotation` skill |
| ClinVar Accession | RCV + digits | "RCV000012345" | ClinVar | `clinvar-annotation` skill |
| JASPAR Matrix | MA + digits + version | "MA0139.1" | JASPAR | `jaspar-motifs` skill |

---

## Code Examples

### 1. PubMed: "Find the original paper for this ENCODE experiment and link it"

```
Step 1: Track the experiment to extract publications
  encode_track_experiment(accession="ENCSR133RZO", fetch_publications=True)
  -> Extracts PMIDs from experiment metadata

Step 2: Get the PMIDs
  encode_get_references(experiment_accession="ENCSR133RZO", reference_type="pmid")
  -> Returns: [{"reference_id": "32728249", "reference_type": "pmid"}]

Step 3: Fetch full article metadata from PubMed
  get_article_metadata(pmids=["32728249"])
  -> Returns title, authors, journal, abstract, DOI

Step 4: Find related papers
  find_related_articles(pmids=["32728249"], link_type="pubmed_pubmed", max_results=10)
  -> Returns similar articles for further reading
```

### 2. bioRxiv: "Check if any preprints reference this ChIP-seq dataset"

```
Step 1: Get experiment details
  encode_get_experiment(accession="ENCSR000AKS")
  -> Note the target (e.g., H3K27me3), biosample, and any linked DOIs

Step 2: Search bioRxiv for related preprints
  search_preprints(category="genomics", recent_days=90, limit=20)
  -> Review abstracts for mentions of the target or ENCODE accession

Step 3: Link discovered preprint
  encode_link_reference(
    experiment_accession="ENCSR000AKS",
    reference_type="preprint_doi",
    reference_id="10.1101/2024.06.15.598765",
    description="Preprint analyzing H3K27me3 patterns in same tissue"
  )
```

### 3. GEO: "Link the GEO submission that corresponds to this ENCODE experiment"

```
Step 1: Check experiment metadata for GEO cross-references
  encode_get_experiment(accession="ENCSR133RZO")
  -> Look in dbxrefs for "GEO:GSExxxxxx"

Step 2: Link the GEO accession
  encode_link_reference(
    experiment_accession="ENCSR133RZO",
    reference_type="geo_accession",
    reference_id="GSE125066",
    description="GEO submission with same raw data and supplementary files"
  )
```

### 4. ClinicalTrials: "Find clinical trials studying the same gene target"

```
Step 1: Get the target from an ENCODE experiment
  encode_get_experiment(accession="ENCSR...")
  -> Target: "TP53" (a TF ChIP-seq experiment)

Step 2: Search ClinicalTrials.gov for trials involving the target
  search_trials(condition="cancer", intervention="TP53", status=["RECRUITING"])
  -> Returns active trials targeting TP53

Step 3: Link a relevant trial
  encode_link_reference(
    experiment_accession="ENCSR...",
    reference_type="nct_id",
    reference_id="NCT04567890",
    description="Phase 2 trial targeting TP53 in solid tumors"
  )
```

---

## Extended Walkthroughs

### Walkthrough A: ENCODE + Open Targets -- From ChIP-seq Target to Drug Candidates

**Goal**: Use ENCODE TF ChIP-seq data to identify drug targets via Open Targets.

**Biological motivation**: Transcription factors mapped by ENCODE ChIP-seq may be druggable targets themselves or may regulate druggable pathways. Open Targets aggregates genetic association, somatic mutation, expression, and drug evidence to score target-disease relationships. By chaining ENCODE binding data with Open Targets, you can move from "where does this TF bind?" to "what diseases is it linked to, and are there drugs in development?"

```
Step 1: Find ENCODE experiments for a transcription factor
  encode_search_experiments(
    assay_title="TF ChIP-seq",
    target="CTCF",
    organism="Homo sapiens"
  )
  -> Returns experiments where CTCF binding is mapped genome-wide
  -> Note the accessions, biosamples, and labs

Step 2: Look up CTCF in Open Targets
  search_entities(query_strings=["CTCF"])
  -> Returns: {"id": "ENSG00000102974", "entity": "target"}
  -> This Ensembl Gene ID is required for all Open Targets GraphQL queries

Step 3: Query Open Targets for disease associations
  query_open_targets_graphql(
    query_string='query { target(ensemblId: "ENSG00000102974") {
      approvedName
      approvedSymbol
      associatedDiseases(page: {index: 0, size: 10}) {
        rows {
          disease { id name }
          score
          datasourceScores { componentId score }
        }
      }
    } }'
  )
  -> Returns diseases ranked by association score
  -> CTCF disruption is linked to various cancers and developmental disorders
  -> The datasourceScores breakdown shows which evidence types drive the association

Step 4: Query for drugs targeting CTCF-regulated pathways
  query_open_targets_graphql(
    query_string='query { target(ensemblId: "ENSG00000102974") {
      knownDrugs(size: 10) {
        rows { drug { name mechanismOfAction } disease { name } phase status }
      }
      tractability { label modality value }
    } }'
  )
  -> Tractability scores indicate whether the target is druggable
  -> knownDrugs lists any compounds in clinical development
  -> Note: many TFs have low tractability -- pathway-level interventions may be more relevant

Step 5: Find and link relevant clinical trials
  search_trials(condition="cancer", intervention="CTCF", status=["RECRUITING"])
  -> If no direct CTCF trials, broaden to pathway:
  search_trials(condition="cancer", intervention="chromatin remodeling", status=["RECRUITING"])
  -> Link the most relevant trial:
  encode_link_reference(
    experiment_accession="ENCSR...",
    reference_type="nct_id",
    reference_id="NCT...",
    description="Trial targeting chromatin regulation pathway relevant to CTCF"
  )
```

**Interpretation notes**: Most transcription factors are not directly druggable. When Open Targets returns low tractability, shift strategy: (a) look for druggable genes regulated by the TF using the ENCODE binding data, (b) explore pathway-level interventions, or (c) consider the TF as a biomarker rather than a direct drug target.

---

### Walkthrough B: ENCODE + GTEx -- Correlating Regulatory Activity with Tissue Expression

**Goal**: Check if genes near ENCODE enhancers are expressed in the relevant tissue, validating that regulatory elements are functionally active.

**Biological motivation**: An H3K27ac peak marks a putative active enhancer, but not every enhancer is active in every cell type within a tissue. By cross-referencing ENCODE histone ChIP-seq with GTEx bulk RNA-seq, you can assess whether the nearest gene is transcribed in that tissue, strengthening the case that the regulatory element is functional.

```
Step 1: Find ENCODE H3K27ac experiments in liver
  encode_search_experiments(
    assay_title="Histone ChIP-seq",
    target="H3K27ac",
    organ="liver",
    organism="Homo sapiens"
  )
  -> Returns liver H3K27ac experiments
  -> Prefer experiments with status="released" and audit_category free of ERROR

Step 2: Download the peak file
  encode_list_files(
    accession="ENCSR...",
    file_format="bed",
    output_type="IDR thresholded peaks",
    assembly="GRCh38"
  )
  -> Select the preferred_default file if available
  -> Download with encode_download_files for local analysis

Step 3: Annotate peaks with nearest genes
  -> Use the peak-annotation skill or run:
  bedtools closest -a peaks.bed -b gencode.v43.annotation.bed -d
  -> For each peak, record the nearest gene name, Ensembl ID, and distance
  -> Peaks overlapping a gene promoter (within 2 kb of TSS) are most interpretable

Step 4: Check expression of nearby genes in GTEx liver
  -> Use the gtex-expression skill:
  -> GTEx REST API: GET /expression/medianTranscriptExpression
     ?gencodeId=ENSG00000...&tissueSiteDetailId=Liver
  -> For each annotated gene, retrieve median TPM in liver
  -> Classification:
     TPM > 10   = highly expressed (strong evidence the enhancer is active)
     TPM 1-10   = moderately expressed
     TPM < 1    = low/absent expression in bulk tissue
     TPM = 0    = gene is not expressed in this tissue context

Step 5: Validate and interpret
  -> High H3K27ac + high GTEx expression = strong evidence for active enhancer
     driving the nearest gene in liver
  -> High H3K27ac + low GTEx expression = possible enhancer for a rare cell type
     within the liver (e.g., cholangiocytes, stellate cells, immune infiltrates)
     Consider single-cell data from CellxGene to resolve cell-type specificity
  -> Low H3K27ac + high GTEx expression = gene is transcribed but this specific
     enhancer may not be the primary driver; check for other active enhancers nearby
```

**GTEx tissue ID mapping**: GTEx uses specific tissueSiteDetailId values that differ from ENCODE organ names. Common mappings:

| ENCODE organ | GTEx tissueSiteDetailId |
|---|---|
| liver | Liver |
| heart | Heart_Left_Ventricle, Heart_Atrial_Appendage |
| brain | Brain_Cortex, Brain_Cerebellum (13 subregions) |
| kidney | Kidney_Cortex, Kidney_Medulla |
| lung | Lung |
| pancreas | Pancreas |
| intestine | Small_Intestine_Terminal_Ileum, Colon_Transverse, Colon_Sigmoid |
| stomach | Stomach |
| skin of body | Skin_Sun_Exposed_Lower_leg, Skin_Not_Sun_Exposed_Suprapubic |

Always check the GTEx tissue list for exact IDs. Note the case sensitivity and underscores.

---

### Walkthrough C: ENCODE + ClinVar + GWAS Catalog -- Variant-to-Regulatory-Element Pipeline

**Goal**: Determine if a disease-associated variant falls in an ENCODE regulatory element.

**Biological motivation**: Over 90% of GWAS hits fall in non-coding regions. Many of these variants likely disrupt regulatory elements mapped by ENCODE. By intersecting GWAS/ClinVar variants with ENCODE peak files and cCREs, you can prioritize variants that may have functional consequences through altered transcription factor binding, enhancer activity, or chromatin accessibility.

```
Step 1: Get variants from the GWAS Catalog
  -> Use the gwas-catalog skill to find variants for a trait
  -> Example: type 2 diabetes (EFO_0001360)
  -> Retrieve lead SNPs with their coordinates (chr, pos, ref, alt)
  -> Note the reported p-value, odds ratio, and mapped genes
  -> Key variants for T2D: rs7903146 (TCF7L2), rs1801282 (PPARG), rs5219 (KCNJ11)

Step 2: Check ClinVar for clinical significance
  -> Use the clinvar-annotation skill: query ClinVar API with rsID or coordinates
  -> Classifications to note:
     Pathogenic / Likely pathogenic = strong clinical evidence
     Risk factor = population-level association (common for GWAS hits)
     Uncertain significance (VUS) = insufficient evidence to classify
     Benign / Likely benign = not disease-causing
  -> ClinVar also provides the condition and review status (star rating)

Step 3: Find ENCODE data overlapping the variant position
  encode_search_experiments(
    assay_title="Histone ChIP-seq",
    organ="pancreas",
    organism="Homo sapiens"
  )
  -> Download relevant peak files:
  encode_search_files(
    file_format="bed",
    output_type="IDR thresholded peaks",
    assembly="GRCh38"
  )
  -> Check if the variant coordinates fall within any peak
  -> Overlap with H3K27ac = active enhancer; H3K4me1 = poised/active enhancer;
     H3K4me3 = promoter; H3K27me3 = repressed

Step 4: Check ENCODE cCREs via UCSC
  -> Use the ucsc-browser skill to query ENCODE cCRE tracks at the variant position
  -> UCSC REST API: GET /getData/track?genome=hg38&track=encodeCcreCombined
     &chrom=chr10&start=112998580&end=112998600
  -> Determine the cCRE classification:
     PLS = promoter-like signature (high H3K4me3, high DNase)
     pELS = proximal enhancer-like signature (high H3K27ac, within 2 kb of TSS)
     dELS = distal enhancer-like signature (high H3K27ac, distal from TSS)
     CTCF-only = CTCF binding without enhancer/promoter marks
     DNase-H3K4me3 = DNase signal with H3K4me3 but not matching PLS criteria

Step 5: Link everything back to the tracked experiment
  encode_link_reference(
    experiment_accession="ENCSR...",
    reference_type="other",
    reference_id="rs7903146",
    description="T2D GWAS lead SNP in TCF7L2 locus, overlapping H3K27ac peak in pancreatic islets"
  )
  -> Also link the ClinVar accession:
  encode_link_reference(
    experiment_accession="ENCSR...",
    reference_type="other",
    reference_id="RCV000012345",
    description="ClinVar: risk factor for type 2 diabetes"
  )
```

**Variant interpretation matrix**:

| GWAS signal | ClinVar classification | ENCODE overlap | Interpretation |
|---|---|---|---|
| Significant | Pathogenic | Active enhancer | High-confidence regulatory variant |
| Significant | Risk factor | Active enhancer | Strong candidate for functional follow-up |
| Significant | VUS | CTCF-only | May affect chromatin architecture |
| Significant | Benign | No overlap | Likely in LD with true causal variant |
| Significant | Not in ClinVar | Poised enhancer | Novel candidate -- needs experimental validation |

---

### Walkthrough D: ENCODE + Consensus -- Finding Systematic Reviews About ENCODE Data Types

**Goal**: Find the most-cited, highest-quality papers about a specific ENCODE assay type for literature reviews and grant writing.

**Biological motivation**: When writing methods sections, grants, or reviews, you need authoritative references for ENCODE data types. The Consensus academic search tool searches 200M+ papers and provides citation counts and journal quality metrics, helping identify the definitive references.

```
Step 1: Search Consensus for systematic reviews
  search(
    query="ATAC-seq chromatin accessibility systematic review",
    year_min=2020,
    sjr_max=2
  )
  -> Returns high-quality reviews of ATAC-seq methodology from Q1/Q2 journals
  -> Look for papers with high citation counts as authoritative references

Step 2: Find papers that cite ENCODE ATAC-seq data specifically
  search(
    query="ENCODE project ATAC-seq chromatin accessibility analysis pipeline"
  )
  -> Identifies how the community uses ENCODE accessibility data
  -> Note which analysis tools and pipelines are most commonly applied

Step 3: Search for benchmarking studies comparing methods
  search(
    query="ATAC-seq peak calling comparison benchmark ENCODE",
    year_min=2021,
    sjr_max=1
  )
  -> Finds methodological comparisons useful for justifying analysis choices
  -> These papers often include ENCODE data as ground truth or benchmarks

Step 4: Link key papers to tracked experiments
  -> Extract PMIDs from the Consensus results
  -> For each relevant paper:
  encode_link_reference(
    experiment_accession="ENCSR...",
    reference_type="pmid",
    reference_id="...",
    description="Methodological reference for ATAC-seq analysis"
  )

Step 5: Export a complete bibliography
  encode_get_citations(
    experiment_accession="ENCSR...",
    format="bibtex"
  )
  -> Generates a BibTeX file with all linked references
  -> Import directly into reference managers (Zotero, Mendeley, EndNote)
```

**Search strategy by use case**:

| Goal | Consensus query pattern | Filters |
|---|---|---|
| Definitive method paper | "[assay] protocol methodology" | sjr_max=1, year_min=2018 |
| Quality metrics reference | "[assay] quality control metrics benchmarks" | sjr_max=2 |
| Comparison with other assays | "[assay1] vs [assay2] comparison" | human=True |
| Disease application | "ENCODE [assay] [disease] regulatory" | year_min=2020 |
| Tool/pipeline reference | "[tool name] [assay] analysis pipeline" | -- |

---

### Walkthrough E: Multi-Database Chaining -- End-to-End GWAS Hit to Drug Target to Clinical Trial

**Goal**: Complete translational pipeline from a GWAS variant to clinical application. This is the most advanced cross-referencing workflow, chaining eight databases together.

**Biological motivation**: Translational genomics aims to connect population genetic associations to therapeutic interventions. A single GWAS hit triggers a cascade of questions: Is the variant in a regulatory element? What gene does it regulate? Is the gene expressed in the relevant tissue? Is it druggable? Are there active clinical trials? This walkthrough answers all of them.

```
Step 1: Start with a GWAS hit
  -> GWAS Catalog: rs7903146 (TCF7L2 locus)
  -> This is the strongest known common variant association with type 2 diabetes
  -> Coordinates: chr10:112998590 (GRCh38)
  -> Risk allele: T, odds ratio ~1.4, p-value < 1e-200

Step 2: Check ENCODE regulatory landscape at the locus
  encode_search_experiments(
    assay_title="Histone ChIP-seq",
    organ="pancreas",
    organism="Homo sapiens"
  )
  -> Find H3K27ac and H3K4me1 experiments covering the TCF7L2 locus
  -> Also search for ATAC-seq / DNase-seq for chromatin accessibility:
  encode_search_experiments(
    assay_title="ATAC-seq",
    organ="pancreas",
    organism="Homo sapiens"
  )
  -> Download peak files and check if rs7903146 falls in:
     (a) an active enhancer (H3K27ac peak)
     (b) an accessible chromatin region (ATAC-seq peak)
     (c) a CTCF binding site (CTCF ChIP-seq peak)
  -> The variant falls in an islet-specific enhancer marked by H3K27ac and H3K4me1

Step 3: Identify the target gene
  -> Peak annotation: which gene does this enhancer regulate?
  -> TCF7L2 is the nearest protein-coding gene -- a WNT pathway transcription factor
  -> Check GTEx for expression:
     GTEx API: tissueSiteDetailId=Pancreas, gencodeId=ENSG00000148737
  -> TCF7L2 is expressed in pancreatic islets (median TPM > 5)
  -> Also check expression in other T2D-relevant tissues: adipose, liver, skeletal muscle
  -> TCF7L2 is broadly expressed but has islet-specific regulatory patterns

Step 4: Assess population frequency and clinical significance
  -> gnomAD (via gnomad-variants skill):
     rs7903146 T allele frequency: ~30% in European populations, ~25% global
     This is a common variant, consistent with a GWAS hit
  -> ClinVar (via clinvar-annotation skill):
     rs7903146 is classified as "risk factor" for type 2 diabetes
     Review status: multiple submitters with criteria provided
  -> Also check Ensembl VEP for predicted functional consequences:
     Ensembl REST: GET /vep/human/id/rs7903146
     -> Regulatory region variant, falls in ENSR00000... (Ensembl Regulatory Build)

Step 5: Evaluate as a drug target via Open Targets
  search_entities(query_strings=["TCF7L2"])
  -> Returns: {"id": "ENSG00000148737", "entity": "target"}

  query_open_targets_graphql(
    query_string='query { target(ensemblId: "ENSG00000148737") {
      approvedName approvedSymbol
      tractability { label modality value }
      associatedDiseases(page: {index: 0, size: 5}) {
        rows { disease { name } score }
      }
      knownDrugs(size: 10) {
        rows { drug { name } disease { name } phase status }
      }
    } }'
  )
  -> Check tractability: is TCF7L2 druggable with small molecules, antibodies, or other modalities?
  -> Review disease associations: T2D should appear as a top association
  -> If TCF7L2 is not directly druggable, consider WNT pathway targets instead:
  search_entities(query_strings=["WNT3A", "CTNNB1", "GSK3B"])
  -> Query druggability for upstream/downstream WNT pathway members

Step 6: Find active clinical trials
  search_trials(
    condition="type 2 diabetes",
    intervention="WNT",
    status=["RECRUITING"]
  )
  -> Also search broader:
  search_trials(
    condition="type 2 diabetes",
    phase=["PHASE2", "PHASE3"],
    status=["RECRUITING"]
  )
  -> Look for trials targeting pathways regulated by TCF7L2
  -> Link the most relevant trial:
  encode_link_reference(
    experiment_accession="ENCSR...",
    reference_type="nct_id",
    reference_id="NCT...",
    description="Phase 3 T2D trial targeting WNT/TCF7L2 regulatory pathway"
  )

Step 7: Document the full chain with provenance
  -> Track all ENCODE experiments used:
  encode_track_experiment(accession="ENCSR...", fetch_publications=True)
  -> Link all references:
  encode_link_reference(reference_type="other", reference_id="rs7903146",
    description="GWAS lead SNP, TCF7L2 locus, T2D")
  encode_link_reference(reference_type="pmid", reference_id="...",
    description="Original GWAS discovery paper")
  encode_link_reference(reference_type="nct_id", reference_id="NCT...",
    description="Relevant clinical trial")
  -> Log any derived analysis files:
  encode_log_derived_file(
    experiment_accession="ENCSR...",
    description="Intersection of rs7903146 with H3K27ac peaks in pancreatic islets",
    file_path="/path/to/variant_enhancer_overlap.bed"
  )
  -> Export the complete reference list:
  encode_get_citations(experiment_accession="ENCSR...", format="bibtex")
```

**Databases used in this workflow**:

| Database | Purpose | Access method |
|---|---|---|
| GWAS Catalog | Trait-variant associations | `gwas-catalog` skill |
| ENCODE | Regulatory element maps | ENCODE Toolkit tools |
| GTEx | Tissue gene expression | `gtex-expression` skill |
| ClinVar | Clinical variant classification | `clinvar-annotation` skill |
| gnomAD | Population allele frequencies | `gnomad-variants` skill |
| Ensembl | VEP, Regulatory Build | `ensembl-annotation` skill |
| Open Targets | Drug targets, tractability | `query_open_targets_graphql` |
| ClinicalTrials.gov | Active trials | `search_trials` |
| PubMed | Publication links | `get_article_metadata` |

---

## Pitfalls and Edge Cases

1. **PMID format mismatches**: PMIDs are plain numeric strings (e.g., "35486828"), not prefixed with "PMID:" or "pmid:". When passing PMIDs from ENCODE references to PubMed MCP tools, strip any prefix. The `encode_get_references` tool returns clean PMIDs.

2. **DOI format inconsistency**: Normalize DOIs to the bare format "10.xxxx/..." without the "https://doi.org/" prefix. ENCODE sometimes stores DOIs with the URL prefix; strip it before passing to `encode_link_reference`. Both formats work for lookups but the bare form is canonical.

3. **Preprint vs published DOI**: bioRxiv preprint DOIs (format: "10.1101/YYYY.MM.DD.xxxxxx") differ from the final journal DOIs. A paper may have both. Track both using separate `encode_link_reference` calls with `reference_type="preprint_doi"` and `reference_type="doi"` respectively. Use `search_published_preprints` on bioRxiv MCP to find if a preprint has been published.

4. **GEO accession confusion**: GSE is a series (collection of samples), GSM is a single sample. ENCODE experiments typically map to GSE accessions, not GSM. When linking, use the GSE identifier. You can find GEO accessions in the experiment's `dbxrefs` field via `encode_get_experiment`.

5. **NCT ID format**: Must be exactly "NCT" followed by 8 digits (e.g., "NCT04567890"). ClinicalTrials.gov tools require this exact format. Do not include spaces or hyphens.

6. **ENCODE dbxrefs parsing**: GEO accessions in experiment `dbxrefs` are prefixed with "GEO:" (e.g., "GEO:GSE125066"). Strip the "GEO:" prefix before passing to GEO tools. Similarly, other dbxref prefixes include "IHEC:" for International Human Epigenome Consortium and "Roadmap:" for Roadmap Epigenomics accessions.

7. **PubMed article vs. preprint**: Some ENCODE experiments link to the preprint DOI in their publication field, not the published paper. Always check if a published version exists using `search_published_preprints` from the bioRxiv MCP or `convert_article_ids` from PubMed to map between DOI and PMID. The published version is the citable record.

8. **Open Targets gene IDs**: Open Targets uses Ensembl Gene IDs (ENSG format), not gene symbols. Always resolve gene symbols to Ensembl IDs first using `search_entities(query_strings=["GENE_SYMBOL"])`. Passing a gene symbol directly to a GraphQL query will fail silently or return no data.

9. **GTEx tissue naming**: GTEx tissue IDs use specific formatting (e.g., "Pancreas", "Heart_Left_Ventricle") that does not match ENCODE organ names (e.g., "pancreas", "heart"). Normalize case and check the GTEx tissue list. Some ENCODE organs map to multiple GTEx tissues (e.g., ENCODE "brain" covers 13 GTEx brain subregions).

10. **Clinical trial linking scope**: Not all ENCODE targets have clinical trials. Transcription factors are rarely direct drug targets and often lack clinical trials. In these cases, search for pathway-level interventions (e.g., "WNT pathway" instead of "TCF7L2") or consider the target as a biomarker. Kinases, receptors, and enzymes are far more likely to have active trials.

11. **Assembly coordinate mismatches**: When cross-referencing variant coordinates between databases, verify the genome assembly. ENCODE uses GRCh38 for human; GWAS Catalog uses GRCh38 and GRCh37; ClinVar provides both. Never mix assemblies. Use the `liftover-coordinates` skill to convert between GRCh37 and GRCh38 when needed.

12. **Rate limiting across databases**: When chaining multiple external API calls (Open Targets, GTEx, ClinVar, GWAS Catalog), be aware that each service has its own rate limits. If queries fail, add delays between requests. PubMed E-utilities allow 3 requests/second without an API key and 10 requests/second with one.

---

## Integration

| This skill produces... | Feed into... | Purpose |
|---|---|---|
| PubMed links | **cite-encode** | Publication citations for ENCODE experiments |
| GEO dataset links | **geo-connector** | Connect to complementary GEO data |
| ClinicalTrials.gov links | **disease-research** | Connect ENCODE data to clinical studies |
| Cross-database identifiers | **data-provenance** | Full audit trail of external references |
| Publication metadata | **publication-trust** | Verify cited publications |
| Linked references | **scientific-writing** | Include cross-references in methods sections |
| External database IDs | **track-experiments** | Annotate tracked experiments with external links |

## Presenting Results

When presenting cross-reference results to the user:
- Show linked references as a table: **type** | **ID** | **description** | **experiment**
- For PubMed results, include the article title, journal name, and publication year
- For bioRxiv preprints, note whether they have been published in a peer-reviewed journal
- For ClinicalTrials results, include the trial phase and recruitment status
- For Open Targets results, include the overall association score and top evidence types
- For GTEx results, report TPM values with tissue name and state the expression threshold used
- For variant annotations, include the variant coordinates, cCRE classification, and clinical significance
- After linking references, suggest: "Would you like to export all references in BibTeX format?" (use `encode_get_citations`)
- When multiple databases are involved, group results by database source for clarity
- In multi-database workflows, present a summary chain showing how data flows between databases

---

## Key Literature

- **ENCODE Phase 3**: The ENCODE Project Consortium. Nature 583, 699-710 (2020). DOI: 10.1038/s41586-020-2493-4 -- Describes the expanded ENCODE encyclopedia including cCREs, the Registry of cCREs, and cross-database integration.
- **ENCODE Data Reuse**: Hitz et al. 2023 (Nucleic Acids Research). DOI: 10.1093/nar/gkac1067 -- Documents the cross-referencing capabilities of the ENCODE portal including dbxrefs and publication links.
- **GTEx v8**: The GTEx Consortium. Science 369, 1318-1330 (2020). DOI: 10.1126/science.aaz1776 -- Comprehensive tissue expression atlas used for enhancer-gene validation across 54 human tissues.
- **Open Targets Platform**: Ochoa et al. Nucleic Acids Research 51, D1302-D1310 (2023). DOI: 10.1093/nar/gkac1064 -- Integrative drug target evidence platform linking genetics, expression, and drugs.
- **ClinVar 2024**: Landrum et al. Nucleic Acids Research 52, D1324-D1331 (2024). DOI: 10.1093/nar/gkad1077 -- Clinical variant interpretation database critical for variant-to-regulatory-element pipelines.
- **GWAS Catalog**: Sollis et al. Nucleic Acids Research 51, D1016-D1024 (2023). DOI: 10.1093/nar/gkac1010 -- Curated catalog of published genome-wide association studies.
- **Identifier Interoperability**: McMurry et al. 2017 (PLOS Biology). DOI: 10.1371/journal.pbio.2001414 -- Foundational work on identifier mapping across biomedical databases, relevant to all cross-referencing workflows.

---

## Related Skills

| Skill | When to Use Instead/Additionally |
|-------|--------------------------------|
| `track-experiments` | Tracking and managing local experiment collection |
| `data-provenance` | Logging derived files and analysis chains |
| `cite-encode` | Exporting citations for tracked experiments |
| `disease-research` | Connecting ENCODE data to disease biology |
| `publication-trust` | Evaluating the provenance and trustworthiness of linked publications |
| `gtex-expression` | Cross-reference with GTEx tissue expression data across 54 tissues |
| `clinvar-annotation` | Cross-reference with ClinVar clinical variant annotations |
| `gwas-catalog` | Cross-reference with NHGRI-EBI GWAS Catalog trait associations |
| `cellxgene-context` | Cross-reference with CellxGene single-cell atlas data |
| `gnomad-variants` | Population allele frequencies and gene constraint scores |
| `ensembl-annotation` | VEP variant annotation, Regulatory Build, coordinate liftover |
| `ucsc-browser` | ENCODE cCRE tracks, TF binding profiles, sequence retrieval |
| `jaspar-motifs` | Transcription factor binding motif analysis at variant positions |
| `variant-annotation` | Comprehensive variant effect prediction workflow |
| `functional-screen-analysis` | CRISPR/MPRA/STARR-seq functional validation of regulatory elements |
| `geo-connector` | Detailed GEO dataset discovery and metadata retrieval |
| `peak-annotation` | Annotating peaks with genes, cCREs, and functional categories |

## For the request: "$ARGUMENTS"
