---
name: biogeobears
description: Set up and execute phylogenetic biogeographic analyses using BioGeoBEARS in R. Use when users request biogeographic reconstruction, ancestral range estimation, or want to analyze species distributions on phylogenies. Handles input file validation, data reformatting, RMarkdown workflow generation, and result visualization.
---

# BioGeoBEARS Biogeographic Analysis

## Overview

BioGeoBEARS (BioGeography with Bayesian and Likelihood Evolutionary Analysis in R Scripts) performs probabilistic inference of ancestral geographic ranges on phylogenetic trees. This skill helps set up complete biogeographic analyses by:

1. Validating and reformatting input files (phylogenetic tree and geographic distribution data)
2. Generating organized analysis folder structure
3. Creating customized RMarkdown analysis scripts
4. Guiding users through parameter selection and model choices
5. Producing publication-ready visualizations

## When to Use This Skill

Use this skill when users request:
- "Analyze biogeography on my phylogeny"
- "Reconstruct ancestral ranges for my species"
- "Run BioGeoBEARS analysis"
- "Which areas did my ancestors occupy?"
- "Test biogeographic models (DEC, DIVALIKE, BAYAREALIKE)"

The skill triggers when users mention phylogenetic biogeography, ancestral area reconstruction, or provide tree + distribution data.

## Required Inputs

Users must provide:

1. **Phylogenetic tree** (Newick format, .nwk, .tre, or .tree file)
   - Must be rooted
   - Tip labels will be matched to geography file
   - Branch lengths required

2. **Geographic distribution data** (any tabular format)
   - Species names (matching tree tips)
   - Presence/absence data for different geographic areas
   - Can be CSV, TSV, Excel, or already in PHYLIP format

## Workflow

### Step 1: Gather Information

When a user requests a BioGeoBEARS analysis, ask for:

1. **Input file paths**:
   - "What is the path to your phylogenetic tree file?"
   - "What is the path to your geographic distribution file?"

2. **Analysis parameters** (if not specified):
   - Maximum range size (how many areas can a species occupy simultaneously?)
   - Which models to compare (default: all six - DEC, DEC+J, DIVALIKE, DIVALIKE+J, BAYAREALIKE, BAYAREALIKE+J)
   - Output directory name (default: "biogeobears_analysis")

Use the AskUserQuestion tool to gather this information efficiently:

```
Example questions:
- "Maximum range size" - options based on number of areas (e.g., for 4 areas: "All 4 areas", "3 areas", "2 areas")
- "Models to compare" - options: "All 6 models (recommended)", "Only base models (DEC, DIVALIKE, BAYAREALIKE)", "Only +J models", "Custom selection"
- "Visualization type" - options: "Pie charts (show probabilities)", "Text labels (show most likely states)", "Both"
```

### Step 2: Validate and Prepare Input Files

#### Validate Tree File

Use the Read tool to check the tree file:

```r
# In R, basic validation:
library(ape)
tr <- read.tree("path/to/tree.nwk")
print(paste("Tips:", length(tr$tip.label)))
print(paste("Rooted:", is.rooted(tr)))
print(tr$tip.label)  # Check species names
```

Verify:
- File can be parsed as Newick
- Tree is rooted (if not, ask user which outgroup to use)
- Note the tip labels for geography file validation

#### Validate and Reformat Geography File

Use `scripts/validate_geography_file.py` to validate or reformat the geography file.

**If file is already in PHYLIP format** (starts with numbers):

```bash
python scripts/validate_geography_file.py path/to/geography.txt --validate --tree path/to/tree.nwk
```

This checks:
- Correct tab delimiters
- Species names match tree tips
- Binary codes are correct length
- No spaces in species names or binary codes

**If file is in CSV/TSV format** (needs reformatting):

```bash
python scripts/validate_geography_file.py path/to/distribution.csv --reformat -o geography.data --delimiter ","
```

Or for tab-delimited:

```bash
python scripts/validate_geography_file.py path/to/distribution.txt --reformat -o geography.data --delimiter tab
```

The script will:
- Detect area names from header row
- Convert presence/absence data to binary (handles "1", "present", "TRUE", etc.)
- Remove spaces from species names (replace with underscores)
- Create properly formatted PHYLIP file

**Always validate the reformatted file** before proceeding:

```bash
python scripts/validate_geography_file.py geography.data --validate --tree path/to/tree.nwk
```

### Step 3: Set Up Analysis Folder Structure

Create an organized directory for the analysis:

```
biogeobears_analysis/
├── input/
│   ├── tree.nwk                 # Original or copied tree
│   ├── geography.data            # Validated/reformatted geography file
│   └── original_data/            # Original input files
│       ├── original_tree.nwk
│       └── original_distribution.csv
├── scripts/
│   └── run_biogeobears.Rmd       # Generated RMarkdown script
├── results/                      # Created by analysis (output directory)
│   ├── [MODEL]_result.Rdata      # Saved model results
│   └── plots/                    # Visualization outputs
│       ├── [MODEL]_pie.pdf
│       └── [MODEL]_text.pdf
└── README.md                     # Analysis documentation
```

Create this structure programmatically:

```bash
mkdir -p biogeobears_analysis/input/original_data
mkdir -p biogeobears_analysis/scripts
mkdir -p biogeobears_analysis/results/plots

# Copy files
cp path/to/tree.nwk biogeobears_analysis/input/
cp geography.data biogeobears_analysis/input/
cp original_files biogeobears_analysis/input/original_data/
```

### Step 4: Generate RMarkdown Analysis Script

Use the template at `scripts/biogeobears_analysis_template.Rmd` and customize it with user parameters.

**Copy and customize the template**:

```bash
cp scripts/biogeobears_analysis_template.Rmd biogeobears_analysis/scripts/run_biogeobears.Rmd
```

**Create a parameter file** or modify the YAML header in the Rmd to use the user's specific settings:

Example customization via R code:

```r
# Edit YAML parameters programmatically or provide as params when rendering
rmarkdown::render(
  "biogeobears_analysis/scripts/run_biogeobears.Rmd",
  params = list(
    tree_file = "../input/tree.nwk",
    geog_file = "../input/geography.data",
    max_range_size = 4,
    models = "DEC,DEC+J,DIVALIKE,DIVALIKE+J,BAYAREALIKE,BAYAREALIKE+J",
    output_dir = "../results"
  ),
  output_file = "../results/biogeobears_report.html"
)
```

Or create a run script:

```bash
# biogeobears_analysis/run_analysis.sh
#!/bin/bash
cd "$(dirname "$0")/scripts"

R -e "rmarkdown::render('run_biogeobears.Rmd', params = list(
  tree_file = '../input/tree.nwk',
  geog_file = '../input/geography.data',
  max_range_size = 4,
  models = 'DEC,DEC+J,DIVALIKE,DIVALIKE+J,BAYAREALIKE,BAYAREALIKE+J',
  output_dir = '../results'
), output_file = '../results/biogeobears_report.html')"
```

### Step 5: Create README Documentation

Generate a README.md in the analysis directory explaining:

- What files are present
- How to run the analysis
- What parameters were used
- How to interpret results

Example:

```markdown
# BioGeoBEARS Analysis

## Overview

Biogeographic analysis of [NUMBER] species across [NUMBER] geographic areas.

## Input Data

- **Tree**: `input/tree.nwk` ([NUMBER] tips)
- **Geography**: `input/geography.data` ([NUMBER] species × [NUMBER] areas)
- **Areas**: [A, B, C, ...]

## Parameters

- Maximum range size: [NUMBER]
- Models tested: [LIST]

## Running the Analysis

### Option 1: Using RMarkdown directly

```r
library(rmarkdown)
render("scripts/run_biogeobears.Rmd",
       output_file = "../results/biogeobears_report.html")
```

### Option 2: Using the run script

```bash
bash run_analysis.sh
```

## Outputs

Results will be saved in `results/`:

- `biogeobears_report.html` - Full analysis report with visualizations
- `[MODEL]_result.Rdata` - Saved R objects for each model
- `plots/[MODEL]_pie.pdf` - Ancestral range reconstructions (pie charts)
- `plots/[MODEL]_text.pdf` - Ancestral range reconstructions (text labels)

## Interpreting Results

The HTML report includes:

1. **Model Comparison** - AIC scores, AIC weights, best-fit model
2. **Parameter Estimates** - Dispersal (d), extinction (e), founder-event (j) rates
3. **Likelihood Ratio Tests** - Statistical comparisons of nested models
4. **Ancestral Range Plots** - Visualizations on phylogeny
5. **Session Info** - R package versions for reproducibility

## Model Descriptions

- **DEC**: Dispersal-Extinction-Cladogenesis (general-purpose)
- **DIVALIKE**: Emphasizes vicariance
- **BAYAREALIKE**: Emphasizes sympatric speciation
- **+J**: Adds founder-event speciation parameter

See `references/biogeobears_details.md` for detailed model descriptions.

## Installation Requirements

```r
# Install BioGeoBEARS
install.packages("rexpokit")
install.packages("cladoRcpp")
library(devtools)
devtools::install_github(repo="nmatzke/BioGeoBEARS")

# Other packages
install.packages(c("ape", "rmarkdown", "knitr", "kableExtra"))
```
```

### Step 6: Provide User Instructions

After setting up the analysis, provide clear instructions to the user:

```
Analysis Setup Complete!

Directory structure created at: biogeobears_analysis/

📁 Files created:
   ✓ input/tree.nwk - Phylogenetic tree ([N] tips)
   ✓ input/geography.data - Geographic distribution data (validated)
   ✓ scripts/run_biogeobears.Rmd - RMarkdown analysis script
   ✓ README.md - Documentation and instructions
   ✓ run_analysis.sh - Convenience script to run analysis

📋 Next steps:

1. Review the README.md for analysis details

2. Install BioGeoBEARS if not already installed:
   ```r
   install.packages("rexpokit")
   install.packages("cladoRcpp")
   library(devtools)
   devtools::install_github(repo="nmatzke/BioGeoBEARS")
   ```

3. Run the analysis:
   ```bash
   cd biogeobears_analysis
   bash run_analysis.sh
   ```

   Or in R:
   ```r
   setwd("biogeobears_analysis")
   rmarkdown::render("scripts/run_biogeobears.Rmd",
                     output_file = "../results/biogeobears_report.html")
   ```

4. View results:
   - Open results/biogeobears_report.html in web browser
   - Check results/plots/ for PDF visualizations

⏱️ Expected runtime: [ESTIMATE based on tree size]
   - Small trees (<50 tips): 5-15 minutes
   - Medium trees (50-100 tips): 15-60 minutes
   - Large trees (>100 tips): 1-4 hours

💡 The HTML report includes model comparison, parameter estimates, and visualization of ancestral ranges on your phylogeny.
```

## Analysis Parameter Guidance

When users ask for guidance on parameters, consult `references/biogeobears_details.md` and provide recommendations:

### Maximum Range Size

**Ask**: "What's the maximum number of areas a species in your group can realistically occupy?"

Common approaches:
- **Conservative**: Number of areas - 1 (prevents unrealistic cosmopolitan ancestral ranges)
- **Permissive**: All areas (if biologically plausible)
- **Data-driven**: Maximum observed in extant species

**Impact**: Larger values increase computational time exponentially

### Model Selection

**Default recommendation**: Run all 6 models for comprehensive comparison

- DEC, DIVALIKE, BAYAREALIKE (base models)
- DEC+J, DIVALIKE+J, BAYAREALIKE+J (+J variants)

**Rationale**:
- Model comparison is key to inference
- +J parameter is often significant
- Small additional computational cost

If computation is a concern, suggest starting with DEC and DEC+J.

### Visualization Options

**Pie charts** (`plotwhat = "pie"`):
- Show probability distributions across all possible states
- Better for conveying uncertainty
- Can be cluttered with many areas

**Text labels** (`plotwhat = "text"`):
- Show only maximum likelihood state
- Cleaner, easier to read
- Doesn't show uncertainty

**Recommendation**: Generate both in the analysis (template does this automatically)

## Common Issues and Troubleshooting

### Species Name Mismatches

**Symptom**: Error about species in tree not in geography file (or vice versa)

**Solution**: Use the validation script with `--tree` option to identify mismatches, then either:
1. Edit the geography file to match tree tip labels
2. Edit tree tip labels to match geography file
3. Remove species that aren't in both

### Tree Not Rooted

**Symptom**: Error about unrooted tree

**Solution**:
```r
library(ape)
tr <- read.tree("tree.nwk")
tr <- root(tr, outgroup = "outgroup_species_name")
write.tree(tr, "tree_rooted.nwk")
```

Ask user which species to use as outgroup.

### Formatting Errors in Geography File

**Symptom**: Validation errors about tabs, spaces, or binary codes

**Solution**: Use the reformat option:
```bash
python scripts/validate_geography_file.py input.csv --reformat -o geography.data
```

### Optimization Fails to Converge

**Symptom**: NA values in parameter estimates or very negative log-likelihoods

**Possible causes**:
- Tree and geography data mismatch
- All species in same area (no variation)
- Unrealistic max_range_size

**Solution**: Check input data quality and try simpler model first (DEC only)

### Very Slow Runtime

**Causes**:
- Large number of areas (>6-7 areas gets slow)
- Large max_range_size
- Many tips (>200)

**Solutions**:
- Reduce max_range_size
- Combine geographic areas if appropriate
- Use `force_sparse = TRUE` in run object
- Run on HPC cluster

## Resources

This skill includes:

### scripts/

- **validate_geography_file.py** - Validates and reformats geography files
  - Checks PHYLIP format compliance
  - Validates against tree tip labels
  - Reformats from CSV/TSV to PHYLIP
  - Usage: `python validate_geography_file.py --help`

- **biogeobears_analysis_template.Rmd** - RMarkdown template for complete analysis
  - Model fitting for DEC, DIVALIKE, BAYAREALIKE (with/without +J)
  - Model comparison with AIC, AICc, weights
  - Likelihood ratio tests
  - Parameter visualization
  - Ancestral range plotting
  - Customizable via YAML parameters

### references/

- **biogeobears_details.md** - Comprehensive reference including:
  - Detailed model descriptions
  - Input file format specifications
  - Parameter interpretation guidelines
  - Plotting options and customization
  - Citations and further reading
  - Computational considerations

Load this reference when:
- Users ask about specific models
- Need to explain parameter estimates
- Troubleshooting complex issues
- Users want detailed methodology for publications

## Best Practices

1. **Always validate input files** before analysis - saves time debugging later

2. **Organize analysis in a dedicated directory** - keeps everything together and reproducible

3. **Run all 6 models by default** - model comparison is crucial for biogeographic inference

4. **Document parameters and decisions** - analysis README helps with reproducibility

5. **Generate both visualization types** - pie charts for uncertainty, text labels for clarity

6. **Save intermediate results** - the RMarkdown template does this automatically

7. **Check parameter estimates** - unrealistic values suggest data or model issues

8. **Provide context with visualizations** - explain what dispersal/extinction rates mean for the user's system

## Output Interpretation

When presenting results to users, explain:

### Model Selection

- **AIC weights** represent probability that each model is best
- **ΔAIC < 2**: Models essentially equivalent
- **ΔAIC 2-7**: Considerably less support
- **ΔAIC > 10**: Essentially no support

### Parameter Estimates

- **d (dispersal rate)**: Higher = more range expansions
- **e (extinction rate)**: Higher = more local extinctions
- **j (founder-event rate)**: Higher = more jump dispersal at speciation
- **Ratio d/e**: > 1 favors expansion, < 1 favors contraction

### Ancestral Ranges

- **Pie charts**: Larger slices = higher probability
- **Colors**: Represent areas (single area = bright color, multiple areas = blended)
- **Node labels**: Most likely ancestral range
- **Split events** (at corners): Range changes at speciation

### Statistical Tests

- **LRT p < 0.05**: +J parameter significantly improves fit
- **High AIC weight** (>0.7): Strong evidence for one model
- **Similar AIC weights**: Model uncertainty - report results from multiple models

## Example Usage

```
User: "I have a phylogeny of 30 bird species and their distributions across 5 islands. Can you help me figure out where their ancestors lived?"

Claude (using this skill):
1. Ask for tree and distribution file paths
2. Validate tree file (check 30 tips, rooted)
3. Validate/reformat geography file (5 areas)
4. Ask about max_range_size (suggest 4 areas)
5. Ask about models (suggest all 6)
6. Set up biogeobears_analysis/ directory structure
7. Copy template RMarkdown script with parameters
8. Generate README.md and run_analysis.sh
9. Provide clear instructions to run analysis
10. Explain expected outputs and how to interpret them

Result: User has complete, ready-to-run analysis with documentation
```

## Attribution

This skill was created based on:
- **BioGeoBEARS** package by Nicholas Matzke
- Tutorial resources from http://phylo.wikidot.com/biogeobears
- Example workflows from the BioGeoBEARS GitHub repository

## Additional Notes

**Time estimate for skill execution**:
- File validation: 1-2 minutes
- Directory setup: < 1 minute
- Total setup time: 5-10 minutes

**Analysis runtime** (separate from skill execution):
- Depends on tree size and number of areas
- Small datasets (<50 tips, ≤5 areas): 10-30 minutes
- Large datasets (>100 tips, >5 areas): 1-6 hours

**Installation requirements** (user must have):
- R (≥4.0)
- BioGeoBEARS R package
- Supporting packages: ape, rmarkdown, knitr, kableExtra
- Python 3 (for validation script)

**When to consult references/**:
- Load `biogeobears_details.md` when users need detailed explanations of models, parameters, or interpretation
- Reference it for troubleshooting complex issues
- Use it to help users write methods sections for publications