---
name: search-encode
description: Search and explore ENCODE Project genomics data. Use when the user wants to find experiments, files, or explore what data is available for specific assays, organs, cell lines, or targets.
---

# Search ENCODE Data

## When to Use

- User wants to find ENCODE experiments matching specific criteria (assay, organ, cell type, target)
- User asks "what ENCODE data exists for [tissue/target/assay]?"
- User wants to explore available data before downloading
- User needs to find specific file types (BED, BAM, bigWig) across experiments
- User wants to know how many experiments exist for a condition
- User asks about available assays, organisms, or biosamples in ENCODE

Help the user find ENCODE experiments and files. Use the appropriate tools based on what they need.

## Search Strategy

1. **Finding experiments**: Use `encode_search_experiments` with filters:
   - `assay_title`: "Histone ChIP-seq", "ATAC-seq", "RNA-seq", "TF ChIP-seq", "Hi-C", "CUT&RUN", "WGBS", etc.
   - `organ`: "pancreas", "brain", "liver", "heart", "kidney", "lung", etc.
   - `biosample_type`: "tissue", "cell line", "primary cell", "organoid"
   - `biosample_term_name`: specific name like "GM12878", "HepG2", "K562"
   - `target`: ChIP/CUT&RUN target like "H3K27me3", "H3K4me3", "CTCF", "p300"
   - `organism`: "Homo sapiens" (default) or "Mus musculus"

2. **Finding files across experiments**: Use `encode_search_files` when the user wants specific file types from multiple experiments.

3. **Exploring available data**: Use `encode_get_facets` to see counts of what exists before searching. Use `encode_get_metadata` to list valid filter values.

4. **Getting experiment details**: Use `encode_get_experiment` for full metadata on a single experiment. Use `encode_list_files` to see all files for one experiment.

## Search Strategy Guide

Effective ENCODE searching follows a three-phase pattern: explore, search, refine. Jumping straight to a filtered search often produces empty results or misses relevant data.

### Phase 1: Explore with Facets

Always start with `encode_get_facets` to understand what data exists. Facets return counts per filter value, so you can see immediately whether your target organ, assay, or biosample has data.

```
encode_get_facets(organ="pancreas")
  -> Shows: Histone ChIP-seq (42), ATAC-seq (8), RNA-seq (15), TF ChIP-seq (6), ...
  -> Also shows: biosample types, life stages, labs, replication types
```

This avoids the frustrating pattern of searching for data that does not exist. Facets may also reveal data you did not expect -- for example, CUT&RUN data where you only anticipated ChIP-seq, or organoid samples alongside tissue.

### Phase 2: Validate Filter Values

Before searching, confirm that your filter values match ENCODE's controlled vocabulary. A mistyped assay name returns zero results with no error.

```
encode_get_metadata(metadata_type="assays")
  -> Returns all valid assay_title values: "Histone ChIP-seq", "TF ChIP-seq", "ATAC-seq", ...
```

Available metadata types: `assays`, `organisms`, `organs`, `biosample_types`, `file_formats`, `output_types`, `output_categories`, `assemblies`, `life_stages`, `replication_types`, `statuses`, `file_statuses`.

### Phase 3: Search and Refine

Start with broad filters and add constraints one at a time. If a search returns too many results (>100), add a filter. If it returns zero, remove the most restrictive filter first.

```
# Too broad: 2,400 results
encode_search_experiments(assay_title="Histone ChIP-seq")

# Add organ: 42 results
encode_search_experiments(assay_title="Histone ChIP-seq", organ="pancreas")

# Add target: 6 results
encode_search_experiments(assay_title="Histone ChIP-seq", organ="pancreas", target="H3K27ac")
```

## Pitfalls & Edge Cases

1. **Wrong assay_title values**: Assay names must match ENCODE's controlled vocabulary exactly. Run `encode_get_metadata(metadata_type="assays")` first to discover valid values. For example, use "Histone ChIP-seq" not "ChIP-seq" or "H3K27ac ChIP".
2. **Confusing biosample_term_name vs organ**: `organ` is a broad anatomical system (e.g., "pancreas", "brain"). `biosample_term_name` is a specific cell or tissue name (e.g., "GM12878", "islet of Langerhans"). Use `organ` for tissue-level exploration, `biosample_term_name` when you know the exact biosample.
3. **Not exploring first**: Always call `encode_get_facets` before searching to see what data exists. This avoids empty results and reveals unexpected data availability. For example, facets may show CUT&RUN data exists for your organ when you only expected ChIP-seq.
4. **Mixing organisms**: Human and mouse experiments use different assemblies (GRCh38 vs mm10) and cannot be directly compared. Always filter by `organism` to avoid mixing species in results.
5. **Expecting file-level results from experiment search**: `encode_search_experiments` returns experiments, not individual files. If the user wants specific BED or bigWig files, use `encode_search_files` instead with `file_format` and `output_type` filters.
6. **Searching for deprecated data**: The default `status="released"` is correct for most use cases. Archived or revoked experiments may have known quality issues. Only change status if the user explicitly needs historical data.

## Gotchas

### organ vs biosample_term_name vs biosample_type

These three filters address different levels of the biosample hierarchy. Using the wrong one produces unexpected results.

| Filter | What it means | Example values | When to use |
|--------|---------------|----------------|-------------|
| `organ` | Broad anatomical system | "pancreas", "brain", "heart", "liver" | Exploring all data for an organ system |
| `biosample_term_name` | Exact biosample name | "GM12878", "K562", "islet of Langerhans", "HepG2" | You know the exact cell type or tissue name |
| `biosample_type` | Category of biosample | "tissue", "cell line", "primary cell", "organoid", "in vitro differentiated cells" | Filtering by how the sample was obtained |

Common mistake: using `biosample_term_name="pancreas"` when you mean `organ="pancreas"`. The term name "pancreas" matches whole-pancreas tissue samples only, missing islets, acinar cells, and other pancreatic substructures that are classified under the pancreas organ.

### assay_title Must Match Exactly

ENCODE uses a controlled vocabulary for assay names. Common mistakes:

| Wrong | Correct |
|-------|---------|
| "ChIP-seq" | "Histone ChIP-seq" or "TF ChIP-seq" |
| "H3K27ac ChIP" | "Histone ChIP-seq" (with `target="H3K27ac"`) |
| "ATAC" | "ATAC-seq" |
| "DNase" | "DNase-seq" |
| "Bisulfite-seq" | "WGBS" |
| "scRNA-seq" | "scRNA-seq" |
| "scATAC-seq" | "snATAC-seq" |

Always run `encode_get_metadata(metadata_type="assays")` to see valid values.

### target Names Are Case-Sensitive

Histone mark targets use a specific capitalization pattern. Common mistakes:

| Wrong | Correct |
|-------|---------|
| "h3k27ac" | "H3K27ac" |
| "H3K27AC" | "H3K27ac" |
| "H3K4Me3" | "H3K4me3" |
| "ctcf" | "CTCF" |

Pattern: H3K{number}{modification} where the modification is lowercase ("me3", "ac", "me1"). Transcription factor targets use all-uppercase names ("CTCF", "POLR2A", "EP300").

### Experiment Status Meanings

| Status | Meaning | When to use |
|--------|---------|-------------|
| `released` | Passed ENCODE quality standards. Default and recommended. | Nearly all searches |
| `archived` | Superseded by newer experiment or has known limitations. Data still accessible but not recommended. | Historical analysis, reproducing old studies |
| `revoked` | Serious quality problems identified post-release. Should not be used for new analysis. | Only if investigating specific quality issues |

## Common Filter Combinations

Ready-to-use filter combinations for common research questions:

| Research Question | Tool + Filters |
|---|---|
| All human heart data | `encode_search_experiments(organ="heart")` |
| Active enhancers in a tissue | `encode_search_experiments(assay_title="Histone ChIP-seq", target="H3K27ac", organ="liver")` |
| Active promoters in a tissue | `encode_search_experiments(assay_title="Histone ChIP-seq", target="H3K4me3", organ="liver")` |
| Repressed chromatin | `encode_search_experiments(assay_title="Histone ChIP-seq", target="H3K27me3", organ="brain")` |
| Open chromatin atlas | Run two searches: `assay_title="ATAC-seq"` and `assay_title="DNase-seq"` for the same organ |
| TF binding for a specific factor | `encode_search_experiments(assay_title="TF ChIP-seq", target="CTCF", organ="liver")` |
| Cell line data | `encode_search_experiments(biosample_type="cell line", organ="blood")` |
| Tier 1 cell line (most data) | `encode_search_experiments(biosample_term_name="K562")` or "GM12878" or "H1-hESC" |
| Mouse developmental data | `encode_search_experiments(organism="Mus musculus", life_stage="embryonic", organ="brain")` |
| Recent high-quality data | `encode_search_experiments(status="released", date_released_from="2023-01-01")` |
| Perturbation experiments | `encode_search_experiments(perturbed=True, organ="liver")` |
| CRISPR screen data | `encode_search_experiments(assay_title="CRISPR screen")` |
| 3D genome structure | `encode_search_experiments(assay_title="Hi-C", organ="brain")` |
| DNA methylation | `encode_search_experiments(assay_title="WGBS", organ="pancreas")` |
| Specific BED peak files | `encode_search_files(file_format="bed", output_type="IDR thresholded peaks", assembly="GRCh38")` |
| Signal tracks for visualization | `encode_search_files(file_format="bigWig", output_type="fold change over control", organ="heart")` |
| ENCODE-recommended files | `encode_search_files(preferred_default=True, assay_title="Histone ChIP-seq", organ="pancreas")` |

## Walkthrough: Finding Histone ChIP-seq for a Tissue

Goal: Find all H3K27ac ChIP-seq experiments in human pancreas with high-quality, analysis-ready peak files.

### Step 1: Check Available Data with Facets

```
encode_get_facets(organ="pancreas")
```

Review the output to see which assay types have data, how many experiments exist, which biosample types are represented (tissue vs cell line vs primary cell), and which labs contributed data. This tells you whether your search is feasible before committing to specific filters.

### Step 2: Search Experiments with Assay + Organ Filters

```
encode_search_experiments(
  assay_title="Histone ChIP-seq",
  organ="pancreas",
  target="H3K27ac",
  limit=50
)
```

Review the results table. Note the accessions, biosample names, labs, and replication types. If too many results, narrow by `biosample_type="tissue"` to exclude cell lines, or by `life_stage="adult"` to exclude embryonic samples.

### Step 3: Filter by Status and Assembly

The default `status="released"` is already applied. For files, you also want to specify the genome assembly to avoid mixing coordinate systems:

```
encode_list_files(
  experiment_accession="ENCSR...",
  assembly="GRCh38",
  file_format="bed"
)
```

This returns only GRCh38-aligned BED files, filtering out legacy hg19 files and raw FASTQs.

### Step 4: Check Quality with Audit Information

```
encode_get_experiment(accession="ENCSR...")
```

The full experiment record includes audit fields. Review them in priority order:
- **audit.ERROR**: Serious problems. Do not use this experiment without investigating.
- **audit.NOT_COMPLIANT**: Failed an ENCODE standard. Check what standard was missed.
- **audit.WARNING**: Minor issues. Usually acceptable but worth noting.
- **audit.INTERNAL_ACTION**: Portal bookkeeping. Safe to ignore.

For ChIP-seq, also check: FRiP (fraction of reads in peaks) should be at least 1%, NSC (normalized strand coefficient) should exceed 1.05, and the experiment should have 2+ biological replicates.

### Step 5: List Preferred Default Files

```
encode_list_files(
  experiment_accession="ENCSR...",
  preferred_default=True
)
```

ENCODE curators mark recommended files as `preferred_default=True`. These are the best files for each output type. For Histone ChIP-seq, this typically includes:
- IDR thresholded peaks (BED narrowPeak) -- use for enhancer/promoter identification
- Fold change over control (bigWig) -- use for signal visualization in genome browsers
- Signal p-value (bigWig) -- use for statistical thresholding

If `preferred_default` returns no results, fall back to filtering manually:

```
encode_list_files(
  experiment_accession="ENCSR...",
  output_type="IDR thresholded peaks",
  assembly="GRCh38"
)
```

## Walkthrough: Cross-Assay Data Collection

Goal: Collect matched Histone ChIP-seq, ATAC-seq, and RNA-seq data for the same tissue to build a multi-omic regulatory map.

### Strategy

ENCODE does not provide a single query that retrieves matched experiments across assay types. Instead, search each assay type separately and match experiments by biosample. The key matching fields are `organ`, `biosample_term_name`, and `biosample_type`.

### Step 1: Survey All Available Assays for Your Tissue

```
encode_get_facets(organ="liver")
```

Review the assay counts. Confirm that all three assay types (Histone ChIP-seq, ATAC-seq, RNA-seq) have data for liver. Note which biosample types are represented -- you will need to match on the same biosample type across assays.

### Step 2: Search Each Assay Type Separately

```
encode_search_experiments(assay_title="Histone ChIP-seq", organ="liver", biosample_type="tissue", limit=100)
encode_search_experiments(assay_title="ATAC-seq", organ="liver", biosample_type="tissue", limit=100)
encode_search_experiments(assay_title="total RNA-seq", organ="liver", biosample_type="tissue", limit=100)
```

### Step 3: Match by Biosample

From each result set, extract the `biosample_term_name` values. Look for overlap: which specific biosample terms appear in all three result sets? For example, "liver" tissue may appear in all three, but "hepatocyte" primary cells may only have ChIP-seq and RNA-seq.

Present the coverage as a matrix:

| Biosample | Histone ChIP-seq | ATAC-seq | RNA-seq |
|-----------|-----------------|----------|---------|
| liver (tissue) | 12 experiments | 4 experiments | 8 experiments |
| hepatocyte (primary cell) | 3 experiments | 0 | 2 experiments |
| HepG2 (cell line) | 18 experiments | 6 experiments | 10 experiments |

### Step 4: Verify Coverage with Facets

For the matched biosample, use facets to confirm what histone marks and targets are available:

```
encode_get_facets(assay_title="Histone ChIP-seq", organ="liver")
```

This shows which targets (H3K27ac, H3K4me3, H3K27me3, etc.) are available. A minimal epigenomic profile requires at least H3K27ac (active enhancers) and H3K4me3 (active promoters). A comprehensive profile adds H3K27me3 (repression), H3K36me3 (gene bodies), and H3K4me1 (poised enhancers).

### Step 5: Collect Files for Matched Experiments

Once you identify matching experiments, use `encode_list_files` with `preferred_default=True` for each experiment to get the recommended analysis-ready files. Ensure all files use the same assembly (GRCh38 for human).

## Pagination

Search tools return paginated results. The response includes fields for navigating large result sets.

### Response Fields

| Field | Type | Meaning |
|-------|------|---------|
| `total` | integer | Total number of matching results across all pages |
| `has_more` | boolean | True if more results exist beyond the current page |
| `next_offset` | integer or null | The offset value to pass for the next page, null if no more pages |

### Paging Through Results

```
# Page 1: first 25 results
encode_search_experiments(assay_title="Histone ChIP-seq", limit=25, offset=0)
  -> total: 142, has_more: true, next_offset: 25

# Page 2: results 26-50
encode_search_experiments(assay_title="Histone ChIP-seq", limit=25, offset=25)
  -> total: 142, has_more: true, next_offset: 50

# ... continue until has_more is false
```

### Choosing a Limit

- `limit=25` (default): Good for initial exploration and presenting results to the user.
- `limit=50`: Good for moderate result sets where you need a broader view.
- `limit=100`: Use for comprehensive searches or when collecting all data for an analysis. This is the maximum recommended for a single call.

For very large result sets (>100), page through with `offset` rather than setting an extremely high limit. This keeps response times fast and avoids overwhelming the user with too many results at once.

## Search Tips

- **Start broad, then narrow**: Begin with `encode_get_facets` to understand the data landscape, then add filters incrementally.
- **Use metadata discovery**: Call `encode_get_metadata(metadata_type="assays")` to see all valid assay names before searching. Same for "organs", "biosample_types", "output_types".
- **Pagination**: Default `limit=25`. Use `limit=100` for comprehensive searches. Check the `total` count in results. Use `offset` to page through large result sets.
- **Free text search**: Use `search_term` parameter for keyword search across all fields when structured filters are insufficient (e.g., `search_term="CRISPR screen pancreatic"`).
- **Tier 1 cell lines**: K562, GM12878, and H1-hESC have the most data across all assay types. Use these as starting points for exploratory analysis.
- **Life stage matters**: Filter by `life_stage` ("adult", "embryonic", "child") when comparing developmental stages. This is especially important for tissue samples.
- **Date filtering**: Use `date_released_from` and `date_released_to` (YYYY-MM-DD format) to find recently released experiments or to scope searches to a specific time window.
- **Perturbation experiments**: Set `perturbed=True` to find only experiments with genetic modifications or treatments. Combine with `genetic_modification="CRISPR"` or `treatment` to narrow further.
- **Lab filtering**: If you know which lab produced the data you need, use `lab` to restrict results. This is useful for finding data from specific ENCODE production centers.

## Code Examples

### 1. Discover, Search, Filter: "Find all H3K27ac ChIP-seq in human pancreas tissue"

```
Step 1: Explore what's available
  encode_get_facets(organ="pancreas")
  -> Shows assay types and counts available for pancreas
  -> Example output: Histone ChIP-seq (42), ATAC-seq (8), RNA-seq (15)

Step 2: Search experiments
  encode_search_experiments(
    assay_title="Histone ChIP-seq",
    organ="pancreas",
    target="H3K27ac",
    limit=50
  )
  -> Returns matching experiments with accession, biosample, lab, status

Step 3: Get files for a specific experiment
  encode_list_files(
    experiment_accession="ENCSR...",
    file_format="bed",
    output_type="IDR thresholded peaks",
    assembly="GRCh38"
  )
  -> Returns peak files ready for analysis

Step 4: Or get the recommended default files directly
  encode_list_files(
    experiment_accession="ENCSR...",
    preferred_default=True
  )
  -> Returns ENCODE's recommended files for this experiment
```

### 2. Multi-assay comparison: "Compare available ATAC-seq vs DNase-seq for liver"

```
Step 1: Check ATAC-seq availability
  encode_get_facets(assay_title="ATAC-seq", organ="liver")
  -> Shows biosample types, counts, life stages, and labs

Step 2: Check DNase-seq availability
  encode_get_facets(assay_title="DNase-seq", organ="liver")
  -> Compare counts and biosample coverage against ATAC-seq

Step 3: Search both assays
  encode_search_experiments(assay_title="ATAC-seq", organ="liver", limit=50)
  encode_search_experiments(assay_title="DNase-seq", organ="liver", limit=50)
  -> Present side-by-side comparison of experiment counts, biosamples, labs

Step 4: Present comparison summary
  -> "ATAC-seq: 12 experiments across 4 biosample types (3 labs)"
  -> "DNase-seq: 28 experiments across 7 biosample types (5 labs)"
  -> "DNase-seq has broader biosample coverage; ATAC-seq experiments are more recent"
```

### 3. Time-based discovery: "Find recently released CRISPR screen experiments"

```
Step 1: Validate the assay name
  encode_get_metadata(metadata_type="assays")
  -> Confirms "CRISPR screen" is a valid assay_title

Step 2: Search with date filter
  encode_search_experiments(
    assay_title="CRISPR screen",
    date_released_from="2024-01-01",
    limit=25
  )
  -> Returns recent CRISPR screen experiments

Step 3: Explore details for a specific experiment
  encode_get_experiment(accession="ENCSR...")
  -> Full metadata including genetic modifications, biosamples, audit status

Step 4: Check audit status for quality
  -> Look at audit.ERROR, audit.NOT_COMPLIANT, audit.WARNING fields
  -> Experiments with ERROR audits should be flagged to the user
```

### 4. File-level search: "Find all IDR thresholded peak BED files for human brain ChIP-seq"

```
Step 1: Search files directly across experiments
  encode_search_files(
    file_format="bed",
    output_type="IDR thresholded peaks",
    assay_title="Histone ChIP-seq",
    organ="brain",
    assembly="GRCh38",
    limit=100
  )
  -> Returns BED files with accessions, experiment links, sizes, and download URLs

Step 2: Filter to recommended files only
  encode_search_files(
    preferred_default=True,
    assay_title="Histone ChIP-seq",
    organ="brain",
    assembly="GRCh38",
    limit=100
  )
  -> Returns only ENCODE-curated recommended files
```

## Integration

| This skill produces... | Feed into... | Purpose |
|---|---|---|
| Experiment accessions | **download-encode** | Download files for found experiments |
| Search results | **track-experiments** | Track discovered experiments |
| Experiment lists | **batch-analysis** | Process multiple experiments together |
| Filtered experiments | **quality-assessment** | Evaluate quality of search results |
| Experiment metadata | **compare-biosamples** | Compare experiments across biosamples |
| Assay-specific results | **pipeline-guide** | Route to correct processing pipeline |
| Target-specific experiments | **histone-aggregation** | Collect experiments for aggregation |
| Facet data | **epigenome-profiling** | Survey available data for profiling |

## Presenting Results

When presenting search results to the user:
- Show results in a clear table format with columns: **accession** | **assay** | **biosample** | **target** | **lab** | **status**
- Always show the total count and note if results are paginated (e.g., "Showing 25 of 142 experiments")
- Suggest narrowing filters if too many results (>100)
- Suggest broadening filters if no results returned
- Suggest next steps: "Would you like to see files for any of these experiments?" or "Would you like to track any of these experiments?"
- When results span multiple labs or biosample types, summarize the distribution

## Key Literature

- **ENCODE Phase 3**: ENCODE Project Consortium 2020 (Nature, ~2,000 citations) DOI: 10.1038/s41586-020-2493-4 -- Defines the catalog of functional genomic elements that this search covers.
- **ENCODE Portal**: Hitz et al. 2023 (Nucleic Acids Research) DOI: 10.1093/nar/gkac1067 -- Documents the portal, search API, and data access patterns used by this skill.

## Related Skills

| Skill | When to Use Instead/Additionally |
|-------|--------------------------------|
| `download-encode` | Downloading files after finding experiments |
| `track-experiments` | Saving found experiments to local collection |
| `quality-assessment` | Evaluating experiment quality before use |
| `compare-biosamples` | Comparing data across tissues, cell lines, or conditions |
| `cross-reference` | Linking experiments to PubMed, DOI, GEO, NCT IDs |
| `epigenome-profiling` | Building comprehensive tissue profiles from search results |
| `publication-trust` | Evaluating the provenance and trustworthiness of linked publications |

## For the request: "$ARGUMENTS"
