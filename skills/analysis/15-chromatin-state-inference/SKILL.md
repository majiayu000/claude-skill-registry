---
name: chromatin-state-inference
description: This skill should be used when users need to infer chromatin states from histone modification ChIP-seq data using chromHMM. It provides workflows for chromatin state segmentation, model training, state annotation.
---

# ChromHMM Chromatin State Inference

## Overview

This skill enables comprehensive chromatin state analysis using chromHMM for histone modification ChIP-seq data. ChromHMM uses a multivariate Hidden Markov Model to segment the genome into discrete chromatin states based on combinatorial patterns of histone modifications.

Main steps include:

- Refer to **Inputs & Outputs** to verify necessary files.
- **Always prompt user** if required files are missing.
- **Always prompt user** for genome assembly used.
- **Always prompt user** for the bin size for generating binarized files.
- **Always prompt user** for the bin size for the number of states the ChromHMM target.
- **Always prompt user** for the absolute path of ChromHMM JAR file.
- **Run chromHMM workflow**: Binarization → Learning.

---

## When to use this skill

Use this skill when you need to infer chromatin states from histone modification ChIP-seq data using chromHMM.

---

## Inputs & Outputs

### Inputs

(1) Option 1: BED files of aligned reads 

```bash
<mark1>.bed
<mark2>.bed
... # Other marks
```

(1) Option 2: BAM files of aligned reads 

```bash
<mark1>.bam
<mark2>.bam
... # Other marks
```

### Outputs

```bash
chromhmm_output/
  binarized/
    *.txt 
  model/
    *.txt
    ... # other files output by the ChromHMM
```
---

## Decision Tree

### Step 1: Prepare the `cellmarkfile`

- Prepare a .txt file (without header) containing following three columns:
  - sample name
  - marker name
  - name of the BED/BAM file

### Step 2: Data Binarization

- For BAM inputs:  
     Call:
     - `mcp__chromhmm-tools__binarize_bam` 
     with:
     - `ChromHMM_path`: Path to ChromHMM JAR file, provided by user
     - `genome`: Provide by user (e.g. `hg38`)
     - `input_dir`: Directory containing BAM files
     - `cellmarkfile`: Cell mark file defining histone modifications
     - `output_dir`: (e.g. `binarized/`)
     - `bin_size`: Provided by user

- For BED inputs:  
  Call `mcp__chromhmm-tools__binarize_bed` instead.

### Step 3: Model Learning

Call 
- `mcp__chromhmm-tools__learn_model`

with:
- `ChromHMM_path`: Path to ChromHMM JAR file, provided by user
- `binarized_dir`: Directory binarized file located in
- `num_states`: Provide by user (e.g. 15)
- `output_model_dir`: (e.g. `model_15_states/`)
- `genome`: Provide by user (e.g. `hg38`)
- `num_states`: Provide by user (e.g. `hg38`)
- `threads`: (e.g. 4)

## Parameter Optimization

### Number of States
- **8 states**: Basic chromatin states
- **15 states**: Standard comprehensive states
- **25 states**: High-resolution states
- **Optimization**: Use Bayesian Information Criterion (BIC)

### Bin Size
- **200bp**: Standard resolution
- **100bp**: High resolution (requires more memory)
- **500bp**: Low resolution (faster computation)

## State Interpretation

### Common Chromatin States
1. **Active Promoter**: H3K4me3, H3K27ac
2. **Weak Promoter**: H3K4me3
3. **Poised Promoter**: H3K4me3, H3K27me3
4. **Strong Enhancer**: H3K27ac, H3K4me1
5. **Weak Enhancer**: H3K4me1
6. **Insulator**: CTCF
7. **Transcribed**: H3K36me3
8. **Repressed**: H3K27me3
9. **Heterochromatin**: Low signal across marks

## Troubleshooting
- **Memory errors**: Reduce bin size or number of states
- **Convergence problems**: Increase iterations or adjust learning rate
- **Uninterpretable states**: Check input data quality and mark combinations
- **Missing chromosomes**: Verify chromosome naming consistency
