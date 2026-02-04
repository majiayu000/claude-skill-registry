---
name: extract-from-pdfs
description: This skill should be used when extracting structured data from scientific PDFs for systematic reviews, meta-analyses, or database creation. Use when working with collections of research papers that need to be converted into analyzable datasets with validation metrics.
---

# Extract Structured Data from Scientific PDFs

## Purpose

Extract standardized, structured data from scientific PDF literature using Claude's vision capabilities. Transform PDF collections into validated databases ready for statistical analysis in Python, R, or other frameworks.

**Core capabilities:**
- Organize metadata from BibTeX, RIS, directories, or DOI lists
- Filter papers by abstract using Claude (Haiku/Sonnet) or local models (Ollama)
- Extract structured data from PDFs with customizable schemas
- Repair and validate JSON outputs automatically
- Enrich with external databases (GBIF, WFO, GeoNames, PubChem, NCBI)
- Calculate precision/recall metrics for quality assurance
- Export to Python, R, CSV, Excel, or SQLite

## When to Use This Skill

Use when:
- Conducting systematic literature reviews requiring data extraction
- Building databases from scientific publications
- Converting PDF collections to structured datasets
- Validating extraction quality with ground truth metrics
- Comparing extraction approaches (different models, prompts)

Do not use for:
- Single PDF summarization (use basic PDF reading instead)
- Full-text PDF search (use document search tools)
- PDF editing or manipulation

## Getting Started

### 1. Initial Setup

Read the setup guide for installation and configuration:

```bash
cat references/setup_guide.md
```

Key setup steps:
- Install dependencies: `conda env create -f environment.yml`
- Set API keys: `export ANTHROPIC_API_KEY='your-key'`
- Optional: Install Ollama for free local filtering

### 2. Define Extraction Requirements

**Ask the user:**
- Research domain and extraction goals
- How PDFs are organized (reference manager, directory, DOI list)
- Approximate collection size
- Preferred analysis environment (Python, R, etc.)

**Provide 2-3 example PDFs** to analyze structure and design schema.

### 3. Design Extraction Schema

Create custom schema from template:

```bash
cp assets/schema_template.json my_schema.json
```

Customize for the specific domain:
- Set `objective` describing what to extract
- Define `output_schema` with field types and descriptions
- Add domain-specific `instructions` for Claude
- Provide `output_example` showing desired format

See `assets/example_flower_visitors_schema.json` for real-world ecology example.

## Workflow Execution

### Complete Pipeline

Run the 6-step pipeline (plus optional validation):

```bash
# Step 1: Organize metadata
python scripts/01_organize_metadata.py \
  --source-type bibtex \
  --source library.bib \
  --pdf-dir pdfs/ \
  --output metadata.json

# Step 2: Filter papers (optional - recommended)
# Choose backend: anthropic-haiku (cheap), anthropic-sonnet (accurate), ollama (free)
python scripts/02_filter_abstracts.py \
  --metadata metadata.json \
  --backend anthropic-haiku \
  --use-batches \
  --output filtered_papers.json

# Step 3: Extract from PDFs
python scripts/03_extract_from_pdfs.py \
  --metadata filtered_papers.json \
  --schema my_schema.json \
  --method batches \
  --output extracted_data.json

# Step 4: Repair JSON
python scripts/04_repair_json.py \
  --input extracted_data.json \
  --schema my_schema.json \
  --output cleaned_data.json

# Step 5: Validate with APIs
python scripts/05_validate_with_apis.py \
  --input cleaned_data.json \
  --apis my_api_config.json \
  --output validated_data.json

# Step 6: Export to analysis format
python scripts/06_export_database.py \
  --input validated_data.json \
  --format python \
  --output results
```

### Validation (Optional but Recommended)

Calculate extraction quality metrics:

```bash
# Step 7: Sample papers for annotation
python scripts/07_prepare_validation_set.py \
  --extraction-results cleaned_data.json \
  --schema my_schema.json \
  --sample-size 20 \
  --strategy stratified \
  --output validation_set.json

# Step 8: Manually annotate (edit validation_set.json)
# Fill ground_truth field for each sampled paper

# Step 9: Calculate metrics
python scripts/08_calculate_validation_metrics.py \
  --annotations validation_set.json \
  --output validation_metrics.json \
  --report validation_report.txt
```

Validation produces precision, recall, and F1 metrics per field and overall.

## Detailed Documentation

Access comprehensive guides in the `references/` directory:

**Setup and installation:**
```bash
cat references/setup_guide.md
```

**Complete workflow with examples:**
```bash
cat references/workflow_guide.md
```

**Validation methodology:**
```bash
cat references/validation_guide.md
```

**API integration details:**
```bash
cat references/api_reference.md
```

## Customization

### Schema Customization

Modify `my_schema.json` to match the research domain:

1. **Objective:** Describe what data to extract
2. **Instructions:** Step-by-step extraction guidance
3. **Output schema:** JSON schema defining structure
4. **Important notes:** Domain-specific rules
5. **Examples:** Show desired output format

Use imperative language in instructions. Be specific about data types, required vs optional fields, and edge cases.

### API Configuration

Configure external database validation in `my_api_config.json`:

Map extracted fields to validation APIs:
- `gbif_taxonomy` - Biological taxonomy
- `wfo_plants` - Plant names specifically
- `geonames` - Geographic locations
- `geocode` - Address to coordinates
- `pubchem` - Chemical compounds
- `ncbi_gene` - Gene identifiers

See `assets/example_api_config_ecology.json` for ecology-specific example.

### Filtering Customization

Edit filtering criteria in `scripts/02_filter_abstracts.py` (line 74):

Replace TODO section with domain-specific criteria:
- What constitutes primary data vs review?
- What data types are relevant?
- What scope (geographic, temporal, taxonomic) is needed?

Use conservative criteria (when in doubt, include paper) to avoid false negatives.

## Cost Optimization

**Backend selection for filtering (Step 2):**
- Ollama (local): $0 - Best for privacy and high volume
- Haiku (API): ~$0.25/M tokens - Best balance of cost/quality
- Sonnet (API): ~$3/M tokens - Best for complex filtering

**Typical costs for 100 papers:**
- With filtering (Haiku + Sonnet): ~$4
- With local Ollama + Sonnet: ~$3.75
- Without filtering (Sonnet only): ~$7.50

**Optimization strategies:**
- Use abstract filtering to reduce PDF processing
- Use local Ollama for filtering (free)
- Enable prompt caching with `--use-caching`
- Process in batches with `--use-batches`

## Quality Assurance

**Validation workflow provides:**
- Precision: % of extracted items that are correct
- Recall: % of true items that were extracted
- F1 score: Harmonic mean of precision and recall
- Per-field metrics: Identify weak fields

**Use metrics to:**
- Establish baseline extraction quality
- Compare different approaches (models, prompts, schemas)
- Identify areas for improvement
- Report extraction quality in publications

**Recommended sample sizes:**
- Small projects (<100 papers): 10-20 papers
- Medium projects (100-500 papers): 20-50 papers
- Large projects (>500 papers): 50-100 papers

## Iterative Improvement

1. Run initial extraction with baseline schema
2. Validate on sample using Steps 7-9
3. Analyze field-level metrics and error patterns
4. Revise schema, prompts, or model selection
5. Re-extract and re-validate
6. Compare metrics to verify improvement
7. Repeat until acceptable quality achieved

See `references/validation_guide.md` for detailed guidance on interpreting metrics and improving extraction quality.

## Available Scripts

**Data organization:**
- `scripts/01_organize_metadata.py` - Standardize PDFs and metadata

**Filtering:**
- `scripts/02_filter_abstracts.py` - Filter by abstract (Haiku/Sonnet/Ollama)

**Extraction:**
- `scripts/03_extract_from_pdfs.py` - Extract from PDFs with Claude vision

**Processing:**
- `scripts/04_repair_json.py` - Repair and validate JSON
- `scripts/05_validate_with_apis.py` - Enrich with external databases
- `scripts/06_export_database.py` - Export to analysis formats

**Validation:**
- `scripts/07_prepare_validation_set.py` - Sample papers for annotation
- `scripts/08_calculate_validation_metrics.py` - Calculate P/R/F1 metrics

## Assets

**Templates:**
- `assets/schema_template.json` - Blank extraction schema template
- `assets/api_config_template.json` - API validation configuration template

**Examples:**
- `assets/example_flower_visitors_schema.json` - Ecology extraction example
- `assets/example_api_config_ecology.json` - Ecology API validation example
