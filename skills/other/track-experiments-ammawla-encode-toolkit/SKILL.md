---
name: track-experiments
description: Track ENCODE experiments locally with publications, citations, and provenance. Use when the user wants to build a collection of experiments, manage citations, compare experiments, or track data provenance.
---

# Track ENCODE Experiments

## When to Use

- User wants to save/bookmark ENCODE experiments for later reference
- User needs to build a collection of experiments for a project
- User asks to "track", "save", or "bookmark" an experiment
- User wants to manage citations and publications for ENCODE data
- User needs to compare experiments for compatibility
- User wants to export their experiment collection as CSV/TSV/JSON
- User asks about data provenance (linking derived files to ENCODE sources)

Help the user manage their local collection of ENCODE experiments. This skill covers the full lifecycle of experiment management: discovery, tracking, annotation, citation, comparison, provenance, and export.

## Tracking Capabilities

1. **Track an experiment**: Use `encode_track_experiment` to save experiment metadata, publications, and pipeline info locally.
   - Automatically extracts GEO accessions and PMIDs from experiment metadata
   - Fetches associated publications with authors, journal, DOI
   - Stores 18 metadata fields per experiment (see schema below)
   - Idempotent: re-tracking the same accession updates metadata without creating duplicates

2. **View tracked collection**: Use `encode_list_tracked` to see all tracked experiments. Filter by assay, organism, or organ.

3. **Get citations**: Use `encode_get_citations` to export publication data.
   - `"json"`: Structured data
   - `"bibtex"`: For LaTeX/reference managers
   - `"ris"`: For Endnote, Zotero, Mendeley

4. **Compare experiments**: Use `encode_compare_experiments` to check if two experiments are compatible for combined analysis (same organism, assembly, assay, biosample, etc.).

5. **Collection overview**: Use `encode_summarize_collection` for grouped statistics across your tracked experiments.

6. **Export data**: Use `encode_export_data` to export tracked experiments as CSV, TSV, or JSON for use in R, pandas, Excel.

## Stored Metadata

When you track an experiment, the following fields are captured from the ENCODE Portal API and stored locally:

| Field | Description | Example |
|-------|-------------|---------|
| `accession` | ENCODE accession (primary key) | ENCSR123ABC |
| `assay_title` | Assay type | Histone ChIP-seq |
| `target` | Antibody target (ChIP/eCLIP) | H3K27ac-human |
| `biosample_summary` | Full biosample description | pancreas tissue male adult (54 years) |
| `organism` | Species | Homo sapiens |
| `organ` | Organ or tissue of origin | pancreas |
| `biosample_type` | Biosample classification | tissue, primary cell, cell line |
| `status` | ENCODE release status | released |
| `date_released` | Portal release date | 2020-07-15 |
| `description` | Experiment description (from PI) | H3K27ac ChIP-seq on human pancreatic islets |
| `lab` | Submitting laboratory | /labs/bradley-bernstein/ |
| `award` | Funding award | /awards/U01HG007610/ |
| `assembly` | Genome assembly | GRCh38 |
| `replication_type` | Replicate strategy | isogenic, anisogenic |
| `life_stage` | Developmental stage | adult, embryonic, child |
| `url` | ENCODE Portal URL | https://www.encodeproject.org/experiments/ENCSR123ABC/ |
| `notes` | User-provided notes | H3K27ac reference for islet enhancer study |
| `raw_metadata` | Full JSON from API (up to 512KB) | (stored for future queries) |

Additionally, the tracker stores timestamps (`tracked_at`, `updated_at`) for audit trail purposes.

## SQLite Schema Overview

The tracker uses a local SQLite database with WAL journal mode and foreign keys enabled. The schema consists of six tables:

**`tracked_experiments`** -- One row per ENCODE experiment. The `accession` column is the primary key. Indexes on `assay_title`, `organism`, and `organ` for fast filtered queries.

**`publications`** -- Publications linked to experiments. Stores PMID, DOI, title, authors (first 10), journal, year, abstract. Unique constraint on `(experiment_accession, pmid)` prevents duplicates.

**`pipeline_info`** -- ENCODE uniform processing pipeline details. Stores pipeline title, version, software list (as JSON array), and analysis status.

**`quality_metrics`** -- Per-file quality metrics from ENCODE audits. Stores file accession, metric type, and metric data (as JSON).

**`derived_files`** -- User-created files derived from ENCODE data. Stores file path, source accessions (as JSON array), tool used, parameters, and description. This is the backbone of provenance tracking.

**`external_references`** -- Cross-database links. Stores reference type (pmid, doi, geo_accession, nct_id, biorxiv_doi, dbgap), reference ID, and description. Unique constraint on `(experiment_accession, reference_type, reference_id)`.

The database location is `~/.encode_connector/tracker.db` (macOS/Linux) or `%USERPROFILE%\.encode_connector\tracker.db` (Windows). The directory is created automatically on first use.

## Data Provenance

7. **Log derived files**: Use `encode_log_derived_file` when the user creates files from ENCODE data (filtered peaks, merged signals, etc.).

8. **View provenance**: Use `encode_get_provenance` to trace derived files back to source ENCODE data.

## Cross-References

9. **Link external references**: Use `encode_link_reference` to attach PubMed IDs, DOIs, ClinicalTrials NCT IDs, bioRxiv DOIs, or GEO accessions to tracked experiments.

10. **Get references**: Use `encode_get_references` to retrieve linked external identifiers. These IDs can be passed to PubMed, bioRxiv, or ClinicalTrials MCP servers for further analysis.

---

## Walkthrough 1: Building a Pancreatic Islet Epigenome Reference Collection

**Goal**: Curate a comprehensive set of histone modification ChIP-seq, ATAC-seq, and RNA-seq from human pancreatic islets for enhancer analysis. This is the foundational workflow for any tissue-specific integrative analysis.

### Step 1: Discover what data exists

Before tracking anything, survey the landscape. Use facets to understand the breadth of available data for your tissue of interest.

```
encode_get_facets(facet_field="assay_title", organ="pancreas", organism="Homo sapiens")
```

Expected output (example):
```
Histone ChIP-seq: 15 experiments
ATAC-seq: 3 experiments
RNA-seq: 8 experiments
TF ChIP-seq: 4 experiments
WGBS: 2 experiments
DNase-seq: 1 experiment
```

This tells you that pancreatic tissue has strong histone ChIP-seq coverage (15 experiments across multiple marks), adequate ATAC-seq (3), and solid RNA-seq (8). The 2 WGBS experiments are a bonus for methylation analysis.

### Step 2: Search for histone ChIP-seq experiments

Now retrieve the actual experiments. Focus on one assay type at a time to keep notes organized.

```
encode_search_experiments(assay_title="Histone ChIP-seq", organ="pancreas", organism="Homo sapiens")
```

Expected return: 15 experiments with targets including H3K27ac, H3K4me1, H3K4me3, H3K27me3, H3K36me3. Review the biosample summaries -- some may be whole pancreas tissue, others isolated islets, and others acinar or ductal cells. This distinction matters for enhancer analysis.

### Step 3: Track each histone experiment with descriptive notes

Notes are your lab notebook. Record the histone mark, the specific biosample, and the intended analytical role. This context is invaluable weeks later when you revisit the collection.

```
encode_track_experiment(accession="ENCSR123ABC", notes="H3K27ac pancreatic islets - active enhancers and super-enhancers")
encode_track_experiment(accession="ENCSR456DEF", notes="H3K4me1 pancreatic islets - primed/poised enhancers")
encode_track_experiment(accession="ENCSR789GHI", notes="H3K4me3 pancreatic islets - active promoters, CpG islands")
encode_track_experiment(accession="ENCSR012JKL", notes="H3K27me3 pancreatic islets - Polycomb repression, bivalent domains")
encode_track_experiment(accession="ENCSR345MNO", notes="H3K36me3 pancreatic islets - gene body transcription elongation")
```

Why these five marks? Together they define the core chromatin states:
- **H3K27ac** marks active enhancers and promoters (the primary mark for enhancer identification)
- **H3K4me1** marks primed enhancers (H3K4me1-positive, H3K27ac-negative = poised enhancer)
- **H3K4me3** marks active promoters (distinguishes promoters from enhancers)
- **H3K27me3** marks Polycomb-repressed regions (identifies bivalent promoters when co-occurring with H3K4me3)
- **H3K36me3** marks actively transcribed gene bodies (helps define transcription units)

### Step 4: Add chromatin accessibility data

ATAC-seq or DNase-seq provides an orthogonal measure of regulatory element activity. Open chromatin overlapping H3K27ac peaks gives higher confidence enhancer calls.

```
encode_search_experiments(assay_title="ATAC-seq", organ="pancreas", organism="Homo sapiens")
encode_track_experiment(accession="ENCSR...", notes="ATAC-seq pancreatic islets - open chromatin map, enhancer validation")
```

If ATAC-seq is unavailable, check for DNase-seq:
```
encode_search_experiments(assay_title="DNase-seq", organ="pancreas", organism="Homo sapiens")
```

Both measure chromatin accessibility. ATAC-seq is preferred for newer datasets due to lower input requirements and nucleosome positioning information from fragment sizes.

### Step 5: Add gene expression data

RNA-seq anchors the epigenomic data to functional output. Active enhancers (H3K27ac) near expressed genes have higher regulatory confidence.

```
encode_search_experiments(assay_title="total RNA-seq", organ="pancreas", organism="Homo sapiens")
encode_track_experiment(accession="ENCSR...", notes="RNA-seq pancreatic islets - gene expression baseline for enhancer-gene linking")
```

If multiple RNA-seq experiments exist, prefer those from the same lab or biosample batch as your ChIP-seq experiments. Matched samples reduce technical variability.

### Step 6: Review the full collection

After tracking all experiments, get the bird's-eye view.

```
encode_summarize_collection()
```

Expected output:
```
Total experiments: 8
By assay: Histone ChIP-seq (5), ATAC-seq (1), RNA-seq (2)
By organ: pancreas (8)
By organism: Homo sapiens (8)
By target: H3K27ac (1), H3K4me1 (1), H3K4me3 (1), H3K27me3 (1), H3K36me3 (1), none (2)
By biosample_type: tissue (5), primary cell (3)
By lab: /labs/bradley-bernstein/ (3), /labs/john-stamatoyannopoulos/ (2), /labs/michael-snyder/ (3)
Total publications: 4
Total derived files: 0
Total external references: 0
```

Check the summary for consistency:
- All experiments should be the same organism (Homo sapiens) and organ (pancreas)
- Biosample types should be compatible (tissue and primary cells from the same organ are generally fine)
- Multiple labs is normal but means batch effects are possible -- note this for downstream analysis

### Step 7: Export for spreadsheet review

Create a permanent record outside the database for lab notebook documentation, sharing with collaborators, or loading into R/pandas.

```
encode_export_data(format="csv")
```

This produces a CSV with columns: accession, assay_title, target, organism, organ, biosample_type, biosample_summary, lab, assembly, status, date_released, replication_type, life_stage, publication_count, pmids, derived_file_count, external_reference_count.

Save this CSV alongside your analysis scripts. It is the metadata backbone of your study.

---

## Walkthrough 2: From Tracked Experiments to LaTeX Bibliography

**Goal**: Generate a complete bibliography for a manuscript using tracked experiments. Every ENCODE experiment should cite its associated publications, and the bibliography should be formatted for your reference manager.

### Step 1: Track experiments used in analysis (if not already tracked)

If you have been building your collection following Walkthrough 1, your experiments are already tracked. If starting fresh:

```
encode_track_experiment(accession="ENCSR123ABC", notes="Used in Figure 3A - H3K27ac peaks")
encode_track_experiment(accession="ENCSR456DEF", notes="Used in Figure 3B - H3K4me1 peaks")
encode_track_experiment(accession="ENCSR789GHI", notes="Used in Table S1 - expression values")
```

### Step 2: Verify all publications were fetched

```
encode_list_tracked()
```

Check the "publications" column. A count of 0 means publications were not fetched at tracking time. This can happen if `fetch_publications=False` was passed or if the ENCODE Portal had a temporary issue.

### Step 3: Re-track with publication fetch if needed

If any experiment shows 0 publications, re-track it. Tracking is idempotent -- it updates metadata without duplicating the experiment record.

```
encode_track_experiment(accession="ENCSR123ABC", fetch_publications=True)
```

The publications table uses a unique constraint on `(experiment_accession, pmid)`, so re-fetching is safe and will not create duplicate publication records.

### Step 4: Export BibTeX for LaTeX

```
encode_get_citations(export_format="bibtex")
```

Returns entries like:
```bibtex
@article{12345678,
  title = {Genome-wide maps of chromatin state in pancreatic islets},
  author = {Smith J, Jones K, ...},
  journal = {Nature},
  year = {2020},
  doi = {10.1038/...},
  pmid = {12345678},
  note = {ENCODE experiment: ENCSR123ABC},
}
```

Save this to a `.bib` file and include it in your LaTeX document with `\bibliography{encode_refs}`.

### Step 5: Export RIS for Zotero/Mendeley

```
encode_get_citations(export_format="ris")
```

Returns entries like:
```
TY  - JOUR
TI  - Genome-wide maps of chromatin state in pancreatic islets
AU  - Smith J
AU  - Jones K
JO  - Nature
PY  - 2020
DO  - 10.1038/...
AN  - PMID:12345678
N1  - ENCODE experiment: ENCSR123ABC
ER  -
```

Import this `.ris` file directly into Zotero, Mendeley, or Endnote. The ENCODE experiment accession is preserved in the notes field for traceability.

### Step 6: Add consortium papers manually

Publications extracted from individual experiments are the papers that generated that specific dataset. You also need to cite the ENCODE consortium papers that describe the project itself. These are NOT auto-extracted because they are project-level, not experiment-level.

Essential consortium citations:
- **ENCODE Phase 3**: ENCODE Project Consortium. Nature 583, 699-710 (2020). DOI: 10.1038/s41586-020-0636-z
- **ENCODE Phase 2**: ENCODE Project Consortium. Nature 489, 57-74 (2012). DOI: 10.1038/nature11247
- **ENCODE Portal**: Hitz et al. Nucleic Acids Research 51, D853-D858 (2023). DOI: 10.1093/nar/gkac1067

Add these to your `.bib` or `.ris` file manually, or link them using `encode_link_reference`:

```
encode_link_reference(experiment_accession="ENCSR123ABC", reference_type="doi", reference_id="10.1038/s41586-020-0636-z", description="ENCODE Phase 3 consortium paper")
```

---

## Walkthrough 3: Full Analysis Provenance -- From ENCODE to Publication Figure

**Goal**: Track every step from downloading ENCODE data to generating a publication figure. Complete provenance enables reproducibility and auto-generation of methods sections.

### Step 1: Track source experiment

```
encode_track_experiment(accession="ENCSR123ABC", notes="H3K27ac source for Figure 3A - pancreatic islet active enhancers")
```

### Step 2: Log the peak calling step

After running peak calling on the downloaded BAM files:

```
encode_log_derived_file(
  file_path="/analysis/h3k27ac_peaks.narrowPeak",
  source_accessions=["ENCSR123ABC"],
  description="MACS2 narrow peaks from H3K27ac ChIP-seq, 2 biological replicates pooled",
  tool_used="MACS2 v2.2.7.1",
  parameters="--gsize hs --qvalue 0.05 --keep-dup all --call-summits --bdg --SPMR"
)
```

Note: Record the exact version and every parameter. Omitting `--keep-dup all` vs the default `--keep-dup 1` produces dramatically different peak sets. Future you (or a reviewer) needs this.

### Step 3: Log the filtering step

Apply ENCODE Blacklist v2 and restrict to canonical chromosomes:

```
encode_log_derived_file(
  file_path="/analysis/h3k27ac_peaks_filtered.bed",
  source_accessions=["ENCSR123ABC"],
  description="Filtered peaks: ENCODE blacklist v2 removed (Amemiya et al. 2019), canonical chromosomes only (chr1-22, chrX). Input: 45,231 peaks. Output: 42,876 peaks (94.8% retained).",
  tool_used="bedtools subtract v2.31.0 + grep",
  parameters="bedtools subtract -A -a peaks.narrowPeak -b hg38-blacklist.v2.bed | grep -E '^chr([0-9]+|X)\t' > peaks_filtered.bed"
)
```

Record input and output counts at every filtering step. This is essential for methods sections and reviewer response letters.

### Step 4: Log the intersection with regulatory elements

```
encode_log_derived_file(
  file_path="/analysis/enhancer_peaks.bed",
  source_accessions=["ENCSR123ABC"],
  description="H3K27ac peaks overlapping pancreatic islet enhancers from Roadmap Epigenomics (E087). Input: 42,876 peaks. Overlapping enhancers: 18,432 (43.0%).",
  tool_used="bedtools intersect v2.31.0",
  parameters="-a h3k27ac_peaks_filtered.bed -b E087_15_coreMarks_hg38lift_dense.bed -u -f 0.5"
)
```

### Step 5: Log the figure generation step

```
encode_log_derived_file(
  file_path="/figures/figure_3A_enhancer_heatmap.pdf",
  source_accessions=["ENCSR123ABC"],
  description="Heatmap of H3K27ac signal at pancreatic islet enhancers, sorted by signal intensity. 18,432 enhancers, +/- 3kb window, 50bp bins.",
  tool_used="deepTools computeMatrix + plotHeatmap v3.5.2",
  parameters="computeMatrix reference-point -S h3k27ac.bw -R enhancer_peaks.bed -a 3000 -b 3000 --binSize 50 -o matrix.gz && plotHeatmap -m matrix.gz --colorMap RdYlBu_r --refPointLabel 'Enhancer center' -o figure_3A.pdf"
)
```

### Step 6: Verify complete provenance chain

```
encode_get_provenance(file_path="/figures/figure_3A_enhancer_heatmap.pdf")
```

This returns the full chain:
```
figure_3A_enhancer_heatmap.pdf
  <- deepTools computeMatrix + plotHeatmap v3.5.2
  <- enhancer_peaks.bed
    <- bedtools intersect v2.31.0
    <- h3k27ac_peaks_filtered.bed
      <- bedtools subtract v2.31.0 + grep
      <- h3k27ac_peaks.narrowPeak
        <- MACS2 v2.2.7.1
        <- ENCSR123ABC (ENCODE Portal)
```

Every step from raw ENCODE data to final figure is documented with tool versions and parameters. This chain can be used to:
- Write the Data Processing section of your manuscript (see `scientific-writing` skill)
- Respond to reviewer requests for methodology details
- Reproduce the analysis months or years later
- Share the exact workflow with collaborators

---

## Walkthrough 4: Checking Compatibility Before Integrative Analysis

**Goal**: Verify that two experiments can be combined for differential analysis. Mixing incompatible experiments produces silent errors that invalidate results.

### Step 1: Track both experiments

```
encode_track_experiment(accession="ENCSR111AAA", notes="H3K27ac normal pancreas - control condition")
encode_track_experiment(accession="ENCSR222BBB", notes="H3K27ac diabetic pancreas - disease condition")
```

### Step 2: Run comparison

```
encode_compare_experiments(accession1="ENCSR111AAA", accession2="ENCSR222BBB")
```

The comparison checks eight fields and returns a structured report:

```
Verdict: COMPATIBLE_WITH_CAVEATS

Compatible aspects:
  - Same organism: Homo sapiens
  - Same assembly: GRCh38
  - Same assay: Histone ChIP-seq
  - Same target: H3K27ac-human

Warnings:
  - Different biosample types: tissue vs primary cell
    (Results may reflect sample type differences)
  - Different labs: /labs/bradley-bernstein/ vs /labs/michael-snyder/
    (Batch effects possible)

Issues: (none)

Recommendation: These experiments can be compared, but the warnings
should be addressed in your analysis.
```

### Step 3: Interpret results

The comparison produces three categories:

**Compatible aspects** (green): Fields that match between the two experiments. These are safe dimensions.

**Warnings** (yellow): Fields that differ but do not necessarily prevent combined analysis. Each warning needs a decision:
- **Biosample type mismatch** (tissue vs primary cell): The primary cell isolation process can alter chromatin state. If the tissue and isolated cells are from the same organ, this is often acceptable with a caveat in your methods. If comparing whole pancreas tissue to isolated islets, your results may reflect cell type composition rather than disease state.
- **Lab mismatch**: Different labs use different protocols, antibody lots, and sequencing platforms. Consider batch correction (ComBat, limma::removeBatchEffect) and report the lab difference in your methods.
- **Life stage mismatch** (adult vs fetal): Chromatin states differ dramatically between developmental stages. Only combine if the research question specifically involves developmental comparison.
- **Replication type mismatch** (isogenic vs anisogenic): Different replicate strategies affect statistical power differently. Anisogenic replicates capture biological variation; isogenic replicates do not.

**Issues** (red): Fields that are fundamentally incompatible:
- **Organism mismatch**: Do not combine human and mouse data directly. Requires ortholog mapping and synteny analysis.
- **Assembly mismatch**: Do not combine GRCh38 and hg19 coordinates. Use `liftover-coordinates` skill to convert first.
- **Assay mismatch**: Different assays measure different things. ChIP-seq and ATAC-seq cannot be directly compared -- they require multi-omic integration approaches.

### Step 4: Decision framework

| Comparison result | Action |
|---|---|
| All MATCH, no warnings | Proceed with combined analysis |
| Warnings on biosample or lab | Proceed with batch correction and caveats in methods |
| Warning on life stage | Only proceed if developmental comparison is the research question |
| Issue on organism or assembly | DO NOT combine without liftover/ortholog mapping |
| Issue on assay type | DO NOT combine -- use multi-omic integration instead |

---

## Walkthrough 5: Cross-Referencing with External Databases

**Goal**: Link tracked ENCODE experiments to GEO, PubMed, ClinicalTrials.gov, and other databases for a complete research record.

### Step 1: Link to GEO

Many ENCODE experiments have corresponding GEO submissions. Linking them enables fetching supplementary data not available on the ENCODE Portal.

```
encode_link_reference(
  experiment_accession="ENCSR123ABC",
  reference_type="geo_accession",
  reference_id="GSE123456",
  description="GEO submission with supplementary processed files and sample metadata"
)
```

Use the `geo-connector` skill to fetch additional data from the linked GEO accession.

### Step 2: Link to PubMed

If you find a publication that uses this experiment but is not in the ENCODE Portal metadata (common for recently published papers):

```
encode_link_reference(
  experiment_accession="ENCSR123ABC",
  reference_type="pmid",
  reference_id="38123456",
  description="2024 paper using this dataset for islet enhancer analysis"
)
```

Pass this PMID to the PubMed MCP server (`search_articles`, `get_article_metadata`) for full citation details.

### Step 3: Link to ClinicalTrials.gov

For translational research connecting epigenomic findings to clinical outcomes:

```
encode_link_reference(
  experiment_accession="ENCSR123ABC",
  reference_type="nct_id",
  reference_id="NCT04567890",
  description="Clinical trial testing epigenetic therapy targeting islet enhancers"
)
```

### Step 4: Link to bioRxiv preprints

For preprints that have not yet been published in a peer-reviewed journal:

```
encode_link_reference(
  experiment_accession="ENCSR123ABC",
  reference_type="biorxiv_doi",
  reference_id="10.1101/2024.01.15.123456",
  description="Preprint with novel analysis of pancreatic islet enhancer grammar"
)
```

### Step 5: View all references for an experiment

```
encode_get_references(accession="ENCSR123ABC")
```

Returns all linked references across all types, giving a complete picture of the external context around this experiment.

---

## Tracking Best Practices

- **Track systematically**: When building a collection for a study, track all experiments in a single session with consistent notes. This makes the collection coherent and exportable.
- **Use notes as a lab notebook**: Record the research context (e.g., "Reference dataset for enhancer comparison in T2D islets"). Notes are the only user-facing metadata that distinguish why two similar experiments were tracked.
- **Export early and often**: After every tracking session, export to CSV (`encode_export_data`) so you have a snapshot. This protects against accidental database corruption.
- **Compare before combining**: Always run `encode_compare_experiments` before combining data from two experiments. Mismatched assemblies or organisms will produce silent errors in downstream analysis.
- **Link external references immediately**: If you know the GEO accession or PMID at tracking time, link it right away using `encode_link_reference`. It is easy to forget later.
- **Use consistent note conventions**: Adopt a standard format for notes across your collection. Example: "[Mark/Assay] [Biosample] - [Analytical purpose]". This makes `encode_list_tracked` output scannable.
- **Track negative results too**: If you searched for a specific assay in a tissue and found nothing, note this in a tracked experiment from a related tissue. Example: "H3K27ac whole pancreas - tracked because no islet-specific H3K27ac was available". This documents your decision process.
- **Review collection before analysis**: Run `encode_summarize_collection` before starting any integrative analysis to confirm completeness. Are all expected marks present? Are all experiments from the same assembly? Catching gaps early saves hours of debugging.
- **Back up the database**: Copy `~/.encode_connector/tracker.db` to your project directory or version control before major analysis milestones. A SQLite file is a single file and easy to back up.

## Pitfalls & Edge Cases

1. **Tracking before searching**: Do not track experiments blindly. First use `encode_search_experiments` or `encode_get_experiment` to confirm the experiment is relevant to the user's research question. Tracking irrelevant experiments clutters the local collection.

2. **Not fetching publications**: Always use `fetch_publications=True` (the default) when tracking. Without it, citation export will be incomplete and the user will miss associated papers. Publication metadata is fetched once at tracking time and stored locally.

3. **Forgetting to add notes**: Use the `notes` parameter to record WHY this experiment was tracked, e.g., "H3K27ac reference for pancreatic islet enhancer analysis". Notes are searchable and invaluable when revisiting a collection weeks later.

4. **Not exporting after tracking**: After building a collection, remind users they can export with `encode_export_data` (CSV/TSV/JSON for spreadsheets or scripts) and `encode_get_citations` (BibTeX/RIS for reference managers). Tracking without export limits the value of the collection.

5. **Comparing untracked experiments**: `encode_compare_experiments` requires both experiments to be tracked first. If the user asks to compare two experiments, check that both are tracked and offer to track them if not.

6. **Database location**: The SQLite database is stored at `~/.encode_connector/tracker.db`. Deleting this file wipes all tracking data permanently. Back up before OS reinstalls, machine migrations, or major environment changes. The database is a single file and can be copied with `cp`.

7. **Concurrent access**: The tracker uses a threading lock (`threading.Lock`) but is designed for single-process access. Running two Claude sessions that both track experiments simultaneously may cause lock contention or WAL checkpoint delays. Best practice: one tracking session at a time. If you need parallel access, copy the database and merge later.

8. **Large collections**: Collections exceeding 500 experiments may slow `encode_summarize_collection` because it performs grouped aggregation across all tracked experiments. Use filters (`assay_title`, `organism`, `organ`) to scope the summary to a subset. Export to CSV and use pandas/R for large-scale collection analysis.

9. **Publication lag**: ENCODE Portal metadata may not include the most recent publications that use an experiment's data. Papers published after the experiment's last metadata update will be missing. If you know of a recent publication, link it manually using `encode_link_reference` with `reference_type="pmid"`. Periodically re-tracking experiments (`encode_track_experiment` with the same accession) can pick up newly added publications.

10. **GRCh38 vs hg38**: These refer to the same human genome assembly. ENCODE uses "GRCh38" consistently in its metadata. If your downstream analysis tools (UCSC tools, IGV, bedtools) expect "hg38", you may need to rename chromosome prefixes or use the `liftover-coordinates` skill. The genomic coordinates are identical -- only the naming convention differs.

11. **Raw metadata size limit**: The tracker stores the full API response JSON as `raw_metadata`, capped at 512KB per experiment. Experiments with extremely large metadata (many files, many analyses) may have their raw metadata truncated. The parsed fields (assay_title, target, etc.) are always stored regardless.

12. **Superseded experiments**: Some ENCODE experiments are superseded by newer versions with better data or updated processing. The tracker does not automatically detect supersession. Check the experiment status field -- experiments with `status="revoked"` should be replaced. Use `encode_get_experiment` to check for superseding experiments.

## Code Examples

### 1. Track, Cite, Export: "Track 5 H3K27ac ChIP-seq experiments and export citations in BibTeX"

```
Step 1: Track each experiment
  encode_track_experiment(accession="ENCSR123ABC", notes="H3K27ac pancreas tissue rep1")
  encode_track_experiment(accession="ENCSR456DEF", notes="H3K27ac pancreas tissue rep2")
  ... (repeat for all 5)

Step 2: View collection
  encode_list_tracked(assay_title="Histone ChIP-seq")
  -> Shows all tracked ChIP-seq experiments with publication counts

Step 3: Export citations
  encode_get_citations(export_format="bibtex")
  -> Returns BibTeX entries for all publications across tracked experiments
```

### 2. Track and Compare: "Track two RNA-seq experiments and check compatibility"

```
Step 1: Track both experiments
  encode_track_experiment(accession="ENCSR111AAA", notes="RNA-seq pancreas adult")
  encode_track_experiment(accession="ENCSR222BBB", notes="RNA-seq pancreas fetal")

Step 2: Compare compatibility
  encode_compare_experiments(accession1="ENCSR111AAA", accession2="ENCSR222BBB")
  -> Returns compatibility report: organism, assembly, assay match; warns about life_stage difference
```

### 3. Track, Link, Provenance: "Track experiment, link to GEO, log derived analysis file"

```
Step 1: Track the experiment
  encode_track_experiment(accession="ENCSR789XYZ", fetch_publications=True, notes="ATAC-seq liver for enhancer study")

Step 2: Link to GEO
  encode_link_reference(experiment_accession="ENCSR789XYZ", reference_type="geo_accession", reference_id="GSE123456", description="Corresponding GEO submission")

Step 3: Log a derived file
  encode_log_derived_file(
    file_path="/Users/you/analysis/liver_enhancers.bed",
    source_accessions=["ENCSR789XYZ"],
    description="Filtered ATAC-seq peaks overlapping liver enhancers",
    tool_used="bedtools intersect",
    parameters="-a peaks.bed -b enhancers.bed -u"
  )

Step 4: Verify provenance chain
  encode_get_provenance(file_path="/Users/you/analysis/liver_enhancers.bed")
  -> Shows: derived file <- ENCSR789XYZ <- ENCODE
```

### 4. Multi-assay collection with summary: "Build a complete epigenome collection and review"

```
Step 1: Track histone marks
  encode_track_experiment(accession="ENCSR...", notes="H3K27ac liver - active enhancers")
  encode_track_experiment(accession="ENCSR...", notes="H3K4me1 liver - primed enhancers")
  encode_track_experiment(accession="ENCSR...", notes="H3K4me3 liver - active promoters")

Step 2: Track accessibility
  encode_track_experiment(accession="ENCSR...", notes="ATAC-seq liver - open chromatin")

Step 3: Track expression
  encode_track_experiment(accession="ENCSR...", notes="RNA-seq liver - gene expression")

Step 4: Track methylation
  encode_track_experiment(accession="ENCSR...", notes="WGBS liver - DNA methylation")

Step 5: Summarize the collection
  encode_summarize_collection()
  -> Total experiments: 6
  -> By assay: Histone ChIP-seq (3), ATAC-seq (1), RNA-seq (1), WGBS (1)
  -> By organ: liver (6)
  -> Completeness check: all major data types represented

Step 6: Export the full collection
  encode_export_data(format="csv")
  -> CSV with all 6 experiments, metadata, publication counts
  encode_export_data(format="json")
  -> JSON for programmatic use in Python/R scripts
```

### 5. Re-tracking to update metadata: "Refresh stale experiment metadata"

```
Step 1: Check current metadata
  encode_list_tracked()
  -> Notice ENCSR123ABC has status="submitted" (pre-release)

Step 2: Re-track to refresh
  encode_track_experiment(accession="ENCSR123ABC")
  -> Returns: {"accession": "ENCSR123ABC", "action": "updated"}
  -> Status now shows "released" with updated date_released and assembly

Step 3: Verify publications were updated
  encode_list_tracked()
  -> Publication count increased from 0 to 2 (new publications were added to the portal)
```

Re-tracking is safe and idempotent. It updates all metadata fields, re-fetches publications (merging without duplicates), and updates the `updated_at` timestamp. The `tracked_at` timestamp is preserved.

---

## Integration

| This skill produces... | Feed into... | Purpose |
|---|---|---|
| Tracked experiment list | **cite-encode** | Generate citations for all tracked experiments |
| Tracking metadata | **data-provenance** | Document experiment selection decisions |
| Experiment notes | **scientific-writing** | Include experiment rationale in methods |
| Collection summary | **epigenome-profiling** | Overview of collected data for profiling |
| Tracked accessions | **download-encode** | Download files for tracked experiments |
| Experiment portfolio | **batch-analysis** | Process tracked experiments in batch |
| Tracking database | **cross-reference** | Link tracked experiments to external databases |
| Export data | **visualization-workflow** | Generate tracking summary visualizations |

## Presenting Results

When presenting tracking results to the user:
- Show tracked experiment summary as a table: **accession** | **assay** | **biosample** | **publications** | **notes**
- For citations, always offer the format choice: JSON (structured), BibTeX (LaTeX), or RIS (Endnote/Zotero/Mendeley)
- After tracking multiple experiments, show the collection summary using `encode_summarize_collection` to give a bird's-eye view grouped by assay, organ, and target
- When comparing experiments, present the compatibility verdict clearly:
  - **COMPATIBLE**: All key fields match. Safe to combine.
  - **WARNINGS**: Minor differences (e.g., different labs, dates). Proceed with caution.
  - **INCOMPATIBLE**: Critical mismatches (e.g., different organisms, assemblies). Do not combine without justification.
- For provenance results, show the full chain: derived file -> tool/parameters -> source ENCODE accessions
- When exporting, confirm the format and offer to save to a specific path
- For large collections (10+ experiments), present a summary table first and offer to show details on request
- Always include the database path (`~/.encode_connector/tracker.db`) when users ask about data persistence

## Key Literature

- **FAIR Principles**: Wilkinson et al. 2016 (Scientific Data, ~5,000 citations) DOI: 10.1038/sdata.2016.18 -- The tracking system supports FAIR data management by maintaining provenance, citations, and cross-references. Findable (accessions), Accessible (local SQLite), Interoperable (CSV/JSON/BibTeX export), Reusable (provenance chains).
- **ENCODE Portal**: Hitz et al. 2023 (Nucleic Acids Research) DOI: 10.1093/nar/gkac1067 -- Documents the experiment metadata structure that tracking relies on. The 18 fields stored per experiment map directly to the ENCODE Portal API schema.
- **ENCODE Phase 3**: ENCODE Project Consortium. Nature 583, 699-710 (2020) DOI: 10.1038/s41586-020-0636-z -- The source of experiment metadata structure and quality standards. All tracked experiments derive from this data resource. This paper should be cited in any publication using ENCODE data.
- **ENCODE Blacklist**: Amemiya et al. 2019 (Scientific Reports) DOI: 10.1038/s41598-019-45839-z (~1,400 citations) -- Critical for peak filtering in provenance workflows. The blacklist regions should be removed from any ChIP-seq or ATAC-seq peak file before downstream analysis.
- **STAR Methods**: Cell Press STAR Methods guidelines -- The gold standard for structured, transparent, and reproducible methods reporting. The provenance tracking system is designed to capture all information needed for STAR Methods-compliant methods sections: tool versions, parameters, input/output counts, and reference file sources.
- **Landt et al. 2012**: Genome Research 22, 1813-1831. DOI: 10.1101/gr.136184.111 (~4,000 citations) -- ENCODE ChIP-seq quality standards. Defines the QC metrics (FRiP, NSC, RSC, NRF) that should be checked for any tracked ChIP-seq experiment before inclusion in analysis.

## Related Skills

| Skill | When to Use Instead/Additionally |
|-------|--------------------------------|
| `cite-encode` | Formatting and exporting citations for tracked experiments |
| `cross-reference` | Linking experiments to PubMed, DOI, GEO, NCT IDs |
| `data-provenance` | Deep provenance logging with sequential script numbering |
| `search-encode` | Finding experiments to track |
| `compare-biosamples` | Detailed biosample compatibility analysis beyond basic comparison |
| `publication-trust` | Evaluating the provenance and trustworthiness of linked publications |
| `scientific-writing` | Generating methods sections from provenance chains |
| `bioinformatics-installer` | Installing tools referenced in provenance logs (MACS2, bedtools, deepTools) |
| `quality-assessment` | Checking ENCODE audit status and QC metrics before tracking |
| `batch-analysis` | Processing multiple tracked experiments through the same analysis pipeline |
| `liftover-coordinates` | Converting coordinates when assemblies differ between experiments |
| `download-encode` | Downloading files from tracked experiments for local analysis |

## For the request: "$ARGUMENTS"
