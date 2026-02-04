---
name: busco-phylogeny
description: Generate phylogenies from genome assemblies using BUSCO/compleasm-based single-copy orthologs with scheduler-aware workflow generation
---

# BUSCO-based Phylogenomics Workflow Generator

This skill provides phylogenomics expertise for generating comprehensive, scheduler-aware workflows for phylogenetic inference from genome assemblies using single-copy orthologs.

## Purpose

This skill helps users generate phylogenies from genome assemblies by:
1. Handling mixed input (local files and NCBI accessions)
2. Creating scheduler-specific scripts (SLURM, PBS, cloud, local)
3. Setting up complete workflows from raw genomes to final trees
4. Providing quality control and recommendations
5. Supporting flexible software management (bioconda, Docker, custom)

## Available Resources

The skill provides access to these bundled resources:

### Scripts (`scripts/`)
- **`query_ncbi_assemblies.py`** - Query NCBI for available genome assemblies by taxon name (new!)
- **`download_ncbi_genomes.py`** - Download genomes from NCBI using BioProjects or Assembly accessions
- **`rename_genomes.py`** - Rename genome files with meaningful sample names (important!)
- **`generate_qc_report.sh`** - Generate quality control reports from compleasm results
- **`extract_orthologs.sh`** - Extract and reorganize single-copy orthologs
- **`run_aliscore.sh`** - Wrapper for Aliscore to identify randomly similar sequences (RSS)
- **`run_alicut.sh`** - Wrapper for ALICUT to remove RSS positions from alignments
- **`run_aliscore_alicut_batch.sh`** - Batch process all alignments through Aliscore + ALICUT
- **`convert_fasconcat_to_partition.py`** - Convert FASconCAT output to IQ-TREE partition format
- **`predownloaded_aliscore_alicut/`** - Pre-tested Aliscore and ALICUT Perl scripts

### Templates (`templates/`)
- **`slurm/`** - SLURM job scheduler templates
- **`pbs/`** - PBS/Torque job scheduler templates
- **`local/`** - Local machine templates (with GNU parallel)
- **`README.md`** - Complete template documentation

### References (`references/`)
- **`REFERENCE.md`** - Detailed technical reference including:
  - Sample naming best practices
  - BUSCO lineage datasets (complete list)
  - Resource recommendations (memory, CPUs, walltime)
  - Detailed step-by-step implementation guides
  - Quality control guidelines
  - Aliscore/ALICUT detailed guide
  - Tool citations and download links
  - Software installation guide
  - Common issues and troubleshooting

## Workflow Overview

The complete phylogenomics pipeline follows this sequence:

**Input Preparation** → **Ortholog Identification** → **Quality Control** → **Ortholog Extraction** → **Alignment** → **Trimming** → **Concatenation** → **Phylogenetic Inference**

## Initial User Questions

When a user requests phylogeny generation, gather the following information systematically:

### Step 1: Detect Computing Environment

Before asking questions, attempt to detect the local computing environment:

```bash
# Check for job schedulers
command -v sbatch >/dev/null 2>&1  # SLURM
command -v qsub >/dev/null 2>&1    # PBS/Torque
command -v parallel >/dev/null 2>&1  # GNU parallel
```

Report findings to the user, then confirm: **"I detected [X] on this machine. Will you be running the scripts here or on a different system?"**

### Required Information

Ask these questions to gather essential workflow parameters:

1. **Computing Environment**
   - Where will these scripts run? (SLURM cluster, PBS/Torque cluster, Cloud computing, Local machine)

2. **Input Data**
   - Local genome files, NCBI accessions, or both?
   - If NCBI: Do you already have Assembly accessions (GCA_*/GCF_*) or BioProject accessions (PRJNA*/PRJEB*/PRJDA*)?
   - If user doesn't have accessions: Offer to help find assemblies using `query_ncbi_assemblies.py` (see "STEP 0A: Query NCBI for Assemblies" below)
   - If local files: What are the file paths?

3. **Taxonomic Scope & Dataset Details**
   - What taxonomic group? (determines BUSCO lineage dataset)
   - How many taxa/genomes will be analyzed?
   - What is the approximate phylogenetic breadth? (species-level, genus-level, family-level, order-level, etc.)
   - See `references/REFERENCE.md` for complete lineage list

4. **Environment Management**
   - Use unified conda environment (default, recommended), or separate environments per tool?

5. **Resource Constraints**
   - How many CPU cores/threads to use in total? (Ask user to specify, do not auto-detect)
   - Available memory (RAM) per node/machine?
   - Maximum walltime for jobs?
   - See `references/REFERENCE.md` for resource recommendations

6. **Parallelization Strategy**

   Ask the user how they want to handle parallel processing:

   - **For job schedulers (SLURM/PBS)**:
     - Use array jobs for parallel steps? (Recommended: Yes)
     - Which steps to parallelize? (Steps 2, 5, 6, 8C recommended)

   - **For local machines**:
     - Use GNU parallel for parallel steps? (requires `parallel` installed)
     - How many concurrent jobs?

   - **For all systems**:
     - Optimize for maximum throughput or simplicity?

7. **Scheduler-Specific Configuration** (if using SLURM or PBS)
   - Account/Username for compute time charges
   - Partition/Queue to submit jobs to
   - Email notifications? (address and when: START, END, FAIL, ALL)
   - Job dependencies? (Recommended: Yes for linear workflow)
   - Output log directory? (Default: `logs/`)

8. **Alignment Trimming Preference**
   - Aliscore/ALICUT (traditional, thorough), trimAl (fast), BMGE (entropy-based), or ClipKit (modern)?

9. **Substitution Model Selection** (for IQ-TREE phylogenetic inference)

   **Context needed**: Taxonomic breadth, number of taxa, evolutionary rates

   **Action**: Fetch IQ-TREE model documentation and suggest appropriate amino acid substitution models based on dataset characteristics.

   Use the substitution model recommendation system (see "Substitution Model Recommendation" section below).

10. **Educational Goals**
   - Are you learning bioinformatics and would you like comprehensive explanations of each workflow step?
   - If yes: After completing each major workflow stage, offer to explain what the step accomplishes, why certain choices were made, and what best practices are being followed.
   - Store this preference to use throughout the workflow.

---

## Recommended Directory Structure

Organize analyses with dedicated folders for each pipeline step:

```
project_name/
├── logs/                          # All log files
├── 00_genomes/                    # Input genome assemblies
├── 01_busco_results/              # BUSCO/compleasm outputs
├── 02_qc/                         # Quality control reports
├── 03_extracted_orthologs/        # Extracted single-copy orthologs
├── 04_alignments/                 # Multiple sequence alignments
├── 05_trimmed/                    # Trimmed alignments
├── 06_concatenation/              # Supermatrix and partition files
├── 07_partition_search/           # Partition model selection
├── 08_concatenated_tree/          # Concatenated ML tree
├── 09_gene_trees/                 # Individual gene trees
├── 10_species_tree/               # ASTRAL species tree
└── scripts/                       # All analysis scripts
```

**Benefits**: Easy debugging, clear workflow progression, reproducibility, prevents root directory clutter.

---

## Template System

This skill uses a template-based system to reduce token usage and improve maintainability. Script templates are stored in the `templates/` directory and organized by computing environment.

### How to Use Templates

When generating scripts for users:

1. **Read the appropriate template** for their computing environment:
   ```
   Read("templates/slurm/02_compleasm_first.job")
   ```

2. **Replace placeholders** with user-specific values:
   - `TOTAL_THREADS` → e.g., `64`
   - `THREADS_PER_JOB` → e.g., `16`
   - `NUM_GENOMES` → e.g., `20`
   - `NUM_LOCI` → e.g., `2795`
   - `LINEAGE` → e.g., `insecta_odb10`
   - `MODEL_SET` → e.g., `LG,WAG,JTT,Q.pfam`

3. **Present the customized script** to the user with setup instructions

### Available Templates

Key templates by workflow step:
- **Step 0 (setup)**: Environment setup script in `references/REFERENCE.md`
- **Step 2 (compleasm)**: `02_compleasm_first`, `02_compleasm_parallel`
- **Step 8A (partition search)**: `08a_partition_search`
- **Step 8C (gene trees)**: `08c_gene_trees_array`, `08c_gene_trees_parallel`, `08c_gene_trees_serial`

See `templates/README.md` for complete template documentation.

---

## Substitution Model Recommendation

When asked about substitution model selection (Question 9), use this systematic approach:

### Step 1: Fetch IQ-TREE Documentation

Use WebFetch to retrieve current model information:
```
WebFetch(url="https://iqtree.github.io/doc/Substitution-Models",
         prompt="Extract all amino acid substitution models with descriptions and usage guidelines")
```

### Step 2: Analyze Dataset Characteristics

Consider these factors from user responses:
- **Taxonomic Scope**: Species/genus (shallow) vs. family/order (moderate) vs. class/phylum+ (deep)
- **Number of Taxa**: <20 (small), 20-50 (medium), >50 (large)
- **Evolutionary Rates**: Fast-evolving, moderate, or slow-evolving
- **Sequence Type**: Nuclear proteins, mitochondrial, or chloroplast

### Step 3: Recommend Models

Provide 3-5 appropriate models based on dataset characteristics. For detailed model recommendation matrices and taxonomically-targeted models, see `references/REFERENCE.md` section "Substitution Model Recommendation".

**General recommendations**:
- **Nuclear proteins (most common)**: LG, WAG, JTT, Q.pfam
- **Mitochondrial**: mtREV, mtZOA, mtMAM, mtART, mtVer, mtInv
- **Chloroplast**: cpREV
- **Taxonomically-targeted**: Q.bird, Q.mammal, Q.insect, Q.plant, Q.yeast (when applicable)

### Step 4: Present Recommendations

Format recommendations with justifications and explain how models will be used in IQ-TREE steps 8A and 8C.

### Step 5: Store Model Set

Store the final comma-separated model list (e.g., "LG,WAG,JTT,Q.pfam") for use in Step 8 template placeholders.

---

## Workflow Implementation

Once required information is gathered, guide the user through these steps. For each step, use templates where available and refer to `references/REFERENCE.md` for detailed implementation.

### STEP 0: Environment Setup

**ALWAYS start by generating a setup script** for the user's environment.

Use the unified conda environment setup script from `references/REFERENCE.md` (Section: "Software Installation Guide"). This creates a single conda environment with all necessary tools:
- compleasm, MAFFT, trimming tools (trimAl, ClipKit, BMGE)
- IQ-TREE, ASTRAL, Perl with BioPerl, GNU parallel
- Downloads and installs Aliscore/ALICUT Perl scripts

**Key points**:
- Users choose between mamba (faster) or conda
- Users choose between predownloaded Aliscore/ALICUT scripts (tested) or latest from GitHub
- All subsequent steps use `conda activate phylo` (the unified environment)

See `references/REFERENCE.md` for the complete setup script template.

---

### STEP 0A: Query NCBI for Assemblies (Optional)

**Use this step when**: User wants to use NCBI data but doesn't have specific assembly accessions yet.

This optional preliminary step helps users discover available genome assemblies by taxon name before proceeding with the main workflow.

#### When to Offer This Step

Offer this step when:
- User wants to analyze genomes from NCBI
- User doesn't have specific Assembly or BioProject accessions
- User mentions a taxonomic group (e.g., "I want to build a phylogeny for beetles")

#### Workflow

1. **Ask for focal taxon**: Request the taxonomic group of interest
   - Examples: "Coleoptera", "Drosophila", "Apis mellifera"
   - Can be at any taxonomic level (order, family, genus, species)

2. **Query NCBI using the script**: Use `scripts/query_ncbi_assemblies.py` to search for assemblies

   ```bash
   # Basic query (returns 20 results by default)
   python scripts/query_ncbi_assemblies.py --taxon "Coleoptera"

   # Query with more results
   python scripts/query_ncbi_assemblies.py --taxon "Drosophila" --max-results 50

   # Query for RefSeq assemblies only (higher quality, GCF_* accessions)
   python scripts/query_ncbi_assemblies.py --taxon "Apis" --refseq-only

   # Save accessions to file for later download
   python scripts/query_ncbi_assemblies.py --taxon "Coleoptera" --save assembly_accessions.txt
   ```

3. **Present results to user**: The script displays:
   - Assembly accession (GCA_* or GCF_*)
   - Organism name
   - Assembly level (Chromosome, Scaffold, Contig)
   - Assembly name

4. **Help user select assemblies**: Ask user which assemblies they want to include
   - Consider assembly level (Chromosome > Scaffold > Contig)
   - Consider phylogenetic breadth (species coverage)
   - Consider data quality (RefSeq > GenBank when available)

5. **Collect selected accessions**: Compile the list of chosen assembly accessions

6. **Proceed to STEP 1**: Use the selected accessions with `download_ncbi_genomes.py`

#### Tips for Assembly Selection

- **Assembly Level**: Chromosome-level assemblies are most complete, followed by Scaffold, then Contig
- **RefSeq vs GenBank**: RefSeq (GCF_*) assemblies undergo additional curation; GenBank (GCA_*) are submitter-provided
- **Taxonomic Sampling**: For phylogenetics, aim for representative sampling across the taxonomic group
- **Quality over Quantity**: Better to have 20 high-quality assemblies than 100 poor-quality ones

---

### STEP 1: Download NCBI Genomes (if applicable)

If user provided NCBI accessions, use `scripts/download_ncbi_genomes.py`:

**For BioProjects**:
```bash
python scripts/download_ncbi_genomes.py --bioprojects PRJNA12345 -o genomes.zip
unzip genomes.zip
```

**For Assembly Accessions**:
```bash
python scripts/download_ncbi_genomes.py --assemblies GCA_123456789.1 -o genomes.zip
unzip genomes.zip
```

**IMPORTANT**: After download, genomes must be renamed with meaningful sample names (format: `[ACCESSION]_[SPECIES_NAME]`). Sample names appear in final phylogenetic trees.

Generate a script that:
1. Finds all downloaded FASTA files in ncbi_dataset directory structure
2. Moves/renames files to main genomes directory with meaningful names
3. Includes any local genome files
4. Creates final genome_list.txt with ALL genomes (local + downloaded)

See `references/REFERENCE.md` section "Sample Naming Best Practices" for detailed guidelines.

---

### STEP 2: Ortholog Identification with compleasm

Activate the unified environment and run compleasm on all genomes to identify single-copy orthologs.

**Key considerations**:
- First genome must run alone to download lineage database
- Remaining genomes can run in parallel
- Thread allocation: Miniprot scales well up to ~16-32 threads per genome

**Threading guidelines**: See `references/REFERENCE.md` for recommended thread allocation table.

**Generate scripts using templates**:
- **SLURM**: Read templates `02_compleasm_first.job` and `02_compleasm_parallel.job`
- **PBS**: Read templates `02_compleasm_first.job` and `02_compleasm_parallel.job`
- **Local**: Read templates `02_compleasm_first.sh` and `02_compleasm_parallel.sh`

Replace placeholders: `TOTAL_THREADS`, `THREADS_PER_JOB`, `NUM_GENOMES`, `LINEAGE`

For detailed implementation examples, see `references/REFERENCE.md` section "Ortholog Identification Implementation".

---

### STEP 3: Quality Control

After compleasm completes, generate QC report using `scripts/generate_qc_report.sh`:

```bash
bash scripts/generate_qc_report.sh qc_report.csv
```

Provide interpretation:
- **>95% complete**: Excellent, retain
- **90-95% complete**: Good, retain
- **85-90% complete**: Acceptable, case-by-case
- **70-85% complete**: Questionable, consider excluding
- **<70% complete**: Poor, recommend excluding

See `references/REFERENCE.md` section "Quality Control Guidelines" for detailed assessment criteria.

---

### STEP 4: Ortholog Extraction

Use `scripts/extract_orthologs.sh` to extract single-copy orthologs:

```bash
bash scripts/extract_orthologs.sh LINEAGE_NAME
```

This generates per-locus unaligned FASTA files in `single_copy_orthologs/unaligned_aa/`.

---

### STEP 5: Alignment with MAFFT

Activate the unified environment (`conda activate phylo`) which contains MAFFT.

Create locus list, then generate alignment scripts:
```bash
cd single_copy_orthologs/unaligned_aa
ls *.fas > locus_names.txt
num_loci=$(wc -l < locus_names.txt)
```

**Generate scheduler-specific scripts**:
- **SLURM/PBS**: Array job with one task per locus
- **Local**: Sequential processing or GNU parallel

For detailed script templates, see `references/REFERENCE.md` section "Alignment Implementation".

---

### STEP 6: Alignment Trimming

Based on user's preference, provide appropriate trimming method. All tools are available in the unified conda environment.

**Options**:
- **trimAl**: Fast (`-automated1`), recommended for large datasets
- **ClipKit**: Modern, fast (default smart-gap mode)
- **BMGE**: Entropy-based (`-t AA`)
- **Aliscore/ALICUT**: Traditional, thorough (recommended for phylogenomics)

**For Aliscore/ALICUT**:
- Perl scripts were installed in STEP 0
- Use `scripts/run_aliscore_alicut_batch.sh` for batch processing
- Or use array jobs with `scripts/run_aliscore.sh` and `scripts/run_alicut.sh`
- Always use `-N` flag for amino acid sequences

**Generate scripts** using scheduler-appropriate templates (array jobs for SLURM/PBS, parallel or serial for local).

For detailed implementation of each trimming method, see `references/REFERENCE.md` section "Alignment Trimming Implementation".

---

### STEP 7: Concatenation and Partition Definition

Download FASconCAT-G (Perl script) and run concatenation:

```bash
conda activate phylo  # Has Perl installed
wget https://raw.githubusercontent.com/PatrickKueck/FASconCAT-G/master/FASconCAT-G_v1.06.1.pl -O FASconCAT-G.pl
chmod +x FASconCAT-G.pl

cd trimmed_aa
perl ../FASconCAT-G.pl -s -i
```

Convert to IQ-TREE format using `scripts/convert_fasconcat_to_partition.py`:
```bash
python ../scripts/convert_fasconcat_to_partition.py FcC_info.xls partition_def.txt
```

Outputs: `FcC_supermatrix.fas`, `FcC_info.xls`, `partition_def.txt`

---

### STEP 8: Phylogenetic Inference

IQ-TREE is already installed in the unified environment. Activate with `conda activate phylo`.

#### Part 8A: Partition Model Selection

Use the substitution models selected during initial setup (Question 9).

**Generate script using templates**:
- Read appropriate template: `templates/[slurm|pbs|local]/08a_partition_search.[job|sh]`
- Replace `MODEL_SET` placeholder with user's selected models (e.g., "LG,WAG,JTT,Q.pfam")

For detailed implementation, see `references/REFERENCE.md` section "Partition Model Selection Implementation".

#### Part 8B: Concatenated ML Tree

Run IQ-TREE using the best partition scheme from Part 8A:

```bash
iqtree -s FcC_supermatrix.fas -spp partition_search.best_scheme.nex \
  -nt 18 -safe -pre concatenated_ML_tree -bb 1000 -bnni
```

Output: `concatenated_ML_tree.treefile`

#### Part 8C: Individual Gene Trees

Estimate gene trees for coalescent-based species tree inference.

**Generate scripts using templates**:
- **SLURM/PBS**: Read `08c_gene_trees_array.job` template
- **Local**: Read `08c_gene_trees_parallel.sh` or `08c_gene_trees_serial.sh` template
- Replace `NUM_LOCI` placeholder

For detailed implementation, see `references/REFERENCE.md` section "Gene Trees Implementation".

#### Part 8D: ASTRAL Species Tree

ASTRAL is already installed in the unified conda environment.

```bash
conda activate phylo

# Concatenate all gene trees
cat trimmed_aa/*.treefile > all_gene_trees.tre

# Run ASTRAL
astral -i all_gene_trees.tre -o astral_species_tree.tre
```

Output: `astral_species_tree.tre`

---

### STEP 9: Generate Methods Paragraph

**ALWAYS generate a methods paragraph** to help users write their publication methods section.

Create `METHODS_PARAGRAPH.md` file with:
- Customized text based on tools and parameters used
- Complete citations for all software
- Placeholders for user-specific values (genome count, loci count, thresholds)
- Instructions for adapting to journal requirements

For the complete methods paragraph template, see `references/REFERENCE.md` section "Methods Paragraph Template".

Pre-fill known values when possible:
- Number of genomes
- BUSCO lineage
- Trimming method used
- Substitution models tested

---

## Final Outputs Summary

Provide users with a summary of outputs:

**Phylogenetic Results**:
1. `concatenated_ML_tree.treefile` - ML tree from concatenated supermatrix
2. `astral_species_tree.tre` - Coalescent species tree
3. `*.treefile` - Individual gene trees

**Data and Quality Control**:
4. `qc_report.csv` - Genome quality statistics
5. `FcC_supermatrix.fas` - Concatenated alignment
6. `partition_search.best_scheme.nex` - Selected partitioning scheme

**Publication Materials**:
7. `METHODS_PARAGRAPH.md` - Ready-to-use methods section with citations

**Visualization tools**: FigTree, iTOL, ggtree (R), ete3/toytree (Python)

---

## Script Validation

**ALWAYS perform validation checks** after generating scripts but before presenting them to the user. This ensures script accuracy, consistency, and proper resource allocation.

### Validation Workflow

For each generated script, perform these validation checks in order:

#### 1. Program Option Verification

**Purpose**: Detect hallucinated or incorrect command-line options that may cause scripts to fail.

**Procedure**:
1. **Extract all command invocations** from the generated script (e.g., `compleasm run`, `iqtree -s`, `mafft --auto`)
2. **Compare against reference sources**:
   - First check: Compare against corresponding template in `templates/` directory
   - Second check: Compare against examples in `references/REFERENCE.md`
   - Third check: If options differ significantly or are uncertain, perform web search for official documentation
3. **Common tools to validate**:
   - `compleasm run` - Check `-a`, `-o`, `-l`, `-t` options
   - `iqtree` - Verify `-s`, `-p`, `-m`, `-bb`, `-alrt`, `-nt`, `-safe` options
   - `mafft` - Check `--auto`, `--thread`, `--reorder` options
   - `astral` - Verify `-i`, `-o` options
   - Trimming tools (`trimal`, `clipkit`, `BMGE.jar`) - Validate options

**Action on issues**:
- If incorrect options found: Inform user of the issue and ask if they want you to correct it
- If uncertain: Ask user to verify with tool documentation before proceeding

#### 2. Pipeline Continuity Verification

**Purpose**: Ensure outputs from one step correctly feed into inputs of subsequent steps.

**Procedure**:
1. **Map input/output relationships**:
   - Step 2 output (`01_busco_results/*_compleasm/`) → Step 3 input (QC script)
   - Step 3 output (`single_copy_orthologs/`) → Step 5 input (MAFFT)
   - Step 5 output (`04_alignments/*.fas`) → Step 6 input (trimming)
   - Step 6 output (`05_trimmed/*.fas`) → Step 7 input (FASconCAT-G)
   - Step 7 output (`FcC_supermatrix.fas`, partition file) → Step 8A input (IQ-TREE)
   - Step 8C output (`*.treefile`) → Step 8D input (ASTRAL)

2. **Check for consistency**:
   - File path references match across scripts
   - Directory structure follows recommended layout
   - Glob patterns correctly match expected files
   - Required intermediate files are generated before being used

**Action on issues**:
- If path mismatches found: Inform user and ask if they want you to correct them
- If directory structure inconsistent: Suggest corrections aligned with recommended structure

#### 3. Resource Compatibility Check

**Purpose**: Ensure allocated computational resources are appropriate for the task.

**Procedure**:
1. **Verify resource allocations** against recommendations in `references/REFERENCE.md`:
   - **Memory allocation**: Check if memory per CPU (typically 6GB for compleasm, 2-4GB for others) is adequate
   - **Thread allocation**: Verify thread counts are reasonable for the number of genomes/loci
   - **Walltime**: Ensure walltime is sufficient based on dataset size guidelines
   - **Parallelization**: Check that threads per job × concurrent jobs ≤ total threads

2. **Common issues to check**:
   - Compleasm: First job needs full thread allocation (downloads database)
   - IQ-TREE: `-nt` should match allocated CPUs
   - Gene trees: Ensure enough threads per tree × concurrent trees ≤ total available
   - Memory: Concatenated tree inference may need 8-16GB per CPU for large datasets

3. **Validate against user-specified constraints**:
   - Total CPUs specified by user
   - Available memory per node
   - Maximum walltime limits
   - Scheduler-specific limits (if mentioned)

**Action on issues**:
- If resource allocation issues found: Inform user and suggest corrections with justification
- If uncertain about adequacy: Ask user about typical job performance in their environment

### Validation Reporting

After completing all validation checks:

1. **If all checks pass**: Inform user briefly: "Scripts validated successfully - options, pipeline flow, and resources verified."

2. **If issues found**: Present a structured report:
   ```
   **Validation Results**

   ⚠️ Issues found during validation:

   1. [Issue category]: [Description]
      - Current: [What was generated]
      - Suggested: [Recommended fix]
      - Reason: [Why this is an issue]

   Would you like me to apply these corrections?
   ```

3. **Always ask before correcting**: Never silently fix issues - always get user confirmation before applying changes.

4. **Document corrections**: If corrections are applied, explain what was changed and why.

---

## Communication Guidelines

- **Always start with STEP 0**: Generate the unified environment setup script
- **Always end with STEP 9**: Generate the customized methods paragraph
- **Always validate scripts**: Perform validation checks before presenting scripts to users
- **Use unified environment by default**: All scripts should use `conda activate phylo`
- **Always ask about CPU allocation**: Never auto-detect cores, always ask user
- **Recommend optimized workflows**: For users with adequate resources, recommend optimized parallel approaches over simple serial approaches
- **Be clear and pedagogical**: Explain why each step is necessary
- **Provide educational explanations when requested**: If user answered yes to educational goals (question 10):
  - After completing each major workflow stage, ask: "Would you like me to explain this step?"
  - If yes, provide moderate-length explanation (1-2 paragraphs) covering:
    - What the step accomplishes biologically and computationally
    - Significant choices made and their rationale
    - Best practices being followed in the workflow
  - Examples of "major workflow stages": STEP 0 (setup), STEP 1 (download), STEP 2 (BUSCO), STEP 3 (QC), STEP 5 (alignment), STEP 6 (trimming), STEP 7 (concatenation), STEP 8 (phylogenetic inference)
- **Provide complete, ready-to-run scripts**: Users should copy-paste and run
- **Adapt to user's environment**: Always generate scheduler-specific scripts
- **Reference supporting files**: Direct users to `references/REFERENCE.md` for details
- **Use helper scripts**: Leverage provided scripts in `scripts/` directory
- **Include error checking**: Add file existence checks and informative error messages
- **Be encouraging**: Phylogenomics is complex; maintain supportive tone

---

## Important Notes

### Mandatory Steps
1. **STEP 0 is mandatory**: Always generate the environment setup script first
2. **STEP 9 is mandatory**: Always generate the methods paragraph file at the end

### Template Usage (IMPORTANT!)
3. **Prefer templates over inline code**: Use `templates/` directory for major scripts
4. **Template workflow**:
   - Read: `Read("templates/slurm/02_compleasm_first.job")`
   - Replace placeholders: `TOTAL_THREADS`, `LINEAGE`, `NUM_GENOMES`, `MODEL_SET`, etc.
   - Present customized script to user
5. **Available templates**: See `templates/README.md` for complete list
6. **Benefits**: Reduces token usage, easier maintenance, consistent structure

### Script Generation
7. **Always adapt scripts** to user's scheduler (SLURM/PBS/local)
8. **Replace all placeholders** before presenting scripts
9. **Never auto-detect CPU cores**: Always ask user to specify
10. **Provide parallelization options**: For each parallelizable step, offer array job, parallel, and serial options
11. **Scheduler-specific configuration**: For SLURM/PBS, always ask about account, partition, email, etc.

### Parallelization Strategy
12. **Ask about preferences**: Let user choose between throughput optimization vs. simplicity
13. **Compleasm optimization**: For ≥2 genomes and ≥16 cores, recommend two-phase approach
14. **Use threading guidelines**: Refer to `references/REFERENCE.md` for thread allocation recommendations
15. **Parallelizable steps**: Steps 2 (compleasm), 5 (MAFFT), 6 (trimming), 8C (gene trees)

### Substitution Model Selection
16. **Always recommend models**: Use the systematic model recommendation process
17. **Fetch current documentation**: Use WebFetch to get IQ-TREE model information
18. **Replace MODEL_SET placeholder**: In Step 8A templates with comma-separated list
19. **Taxonomically-targeted models**: Suggest Q.bird, Q.mammal, Q.insect, Q.plant when applicable

### Reference Material
20. **Direct users to references/REFERENCE.md** for:
    - Detailed implementation guides
    - BUSCO lineage datasets (complete list)
    - Resource recommendations (memory, CPUs, walltime tables)
    - Sample naming best practices
    - Quality control assessment criteria
    - Aliscore/ALICUT detailed guide and parameters
    - Tool citations with DOIs
    - Software installation instructions
    - Common issues and troubleshooting

---

## Attribution

This skill was created by **Bruno de Medeiros** (Curator of Pollinating Insects, Field Museum) based on phylogenomics tutorials by **Paul Frandsen** (Brigham Young University).

## Workflow Entry Point

When a user requests phylogeny generation:

1. Gather required information using the "Initial User Questions" section
2. Generate STEP 0 setup script from `references/REFERENCE.MD`
3. If user needs help finding NCBI assemblies, perform STEP 0A using `query_ncbi_assemblies.py`
4. Proceed step-by-step through workflow (STEPS 1-8), using templates and referring to `references/REFERENCE.md` for detailed implementation
5. All workflow scripts should use the unified conda environment (`conda activate phylo`)
6. Validate all generated scripts before presenting to user (see "Script Validation" section)
7. Generate STEP 9 methods paragraph from template in `references/REFERENCE.md`
8. Provide final outputs summary
