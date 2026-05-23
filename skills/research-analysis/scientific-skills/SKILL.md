---
name: scientific-skills
description: Comprehensive scientific research toolkit with 139 specialized skills for biology, chemistry, medicine, data science, and computational research. Transforms Claude into an AI research assistant with access to scientific databases, analysis tools, and domain-specific workflows.
license: MIT
version: 2.17.0
metadata:
  skill-author: K-Dense Inc.
  original-repo: https://github.com/K-Dense-AI/claude-scientific-skills
  categories:
    - scientific-databases
    - bioinformatics
    - cheminformatics
    - machine-learning
    - data-analysis
    - scientific-writing
  skill-count: 139
---

# Claude Scientific Skills

## Overview

A comprehensive collection of **139 ready-to-use scientific skills** that transform Claude into an AI research assistant capable of executing complex multi-step scientific workflows across biology, chemistry, medicine, and related fields.

## When to Use

Invoke this skill when:

- Working on scientific research tasks
- Need access to specialized databases (PubMed, ChEMBL, UniProt, etc.)
- Performing bioinformatics or cheminformatics analysis
- Creating literature reviews or scientific documents
- Analyzing single-cell RNA-seq, proteomics, or multi-omics data
- Drug discovery and molecular analysis workflows
- Statistical analysis and machine learning on scientific data

## Quick Start

```javascript
// Invoke the main skill catalog
Skill({ skill: 'scientific-skills' });

// Or invoke specific sub-skills directly
Skill({ skill: 'scientific-skills/rdkit' }); // Cheminformatics
Skill({ skill: 'scientific-skills/scanpy' }); // Single-cell analysis
Skill({ skill: 'scientific-skills/biopython' }); // Bioinformatics
Skill({ skill: 'scientific-skills/literature-review' }); // Literature review
```

## Skill Categories

### Scientific Databases (28+)

| Skill                     | Description                             |
| ------------------------- | --------------------------------------- |
| `pubchem`                 | Chemical compound database              |
| `chembl-database`         | Bioactivity database for drug discovery |
| `uniprot-database`        | Protein sequence and function database  |
| `pdb`                     | Protein Data Bank structures            |
| `drugbank-database`       | Drug and drug target information        |
| `kegg`                    | Pathway and genome database             |
| `clinvar-database`        | Clinical variant interpretations        |
| `cosmic-database`         | Cancer mutation database                |
| `ensembl-database`        | Genome browser and annotations          |
| `geo-database`            | Gene expression data                    |
| `gwas-database`           | Genome-wide association studies         |
| `reactome-database`       | Biological pathways                     |
| `string-database`         | Protein-protein interactions            |
| `alphafold-database`      | Protein structure predictions           |
| `biorxiv-database`        | Preprint server for biology             |
| `clinicaltrials-database` | Clinical trial registry                 |
| `ena-database`            | European Nucleotide Archive             |
| `fda-database`            | FDA drug approvals and labels           |
| `gene-database`           | Gene information from NCBI              |
| `zinc-database`           | Commercially available compounds        |
| `brenda-database`         | Enzyme database                         |
| `clinpgx-database`        | Pharmacogenomics annotations            |
| `uspto-database`          | Patent database                         |

### Python Analysis Libraries (55+)

| Skill                               | Description                  |
| ----------------------------------- | ---------------------------- |
| `rdkit`                             | Cheminformatics toolkit      |
| `scanpy`                            | Single-cell RNA-seq analysis |
| `anndata`                           | Annotated data matrices      |
| `biopython`                         | Computational biology tools  |
| `pytorch-lightning`                 | Deep learning framework      |
| `scikit-learn`                      | Machine learning library     |
| `transformers`                      | NLP and deep learning models |
| `pandas` / `polars` / `vaex`        | Data manipulation            |
| `matplotlib` / `seaborn` / `plotly` | Visualization                |
| `deepchem`                          | Deep learning for chemistry  |
| `esm`                               | Evolutionary Scale Modeling  |
| `datamol`                           | Molecular data processing    |
| `pymatgen`                          | Materials science            |
| `qiskit`                            | Quantum computing            |
| `pymoo`                             | Multi-objective optimization |
| `statsmodels`                       | Statistical modeling         |
| `sympy`                             | Symbolic mathematics         |
| `networkx`                          | Network analysis             |
| `geopandas`                         | Geospatial analysis          |
| `shap`                              | Model explainability         |

### Bioinformatics & Genomics

| Skill              | Description                     |
| ------------------ | ------------------------------- |
| `gget`             | Gene and transcript information |
| `pysam`            | SAM/BAM file manipulation       |
| `deeptools`        | NGS data analysis               |
| `pydeseq2`         | Differential expression         |
| `scvi-tools`       | Deep learning for single-cell   |
| `etetoolkit`       | Phylogenetic analysis           |
| `scikit-bio`       | Bioinformatics algorithms       |
| `bioservices`      | Web services for biology        |
| `cellxgene-census` | Cell atlas exploration          |

### Cheminformatics & Drug Discovery

| Skill       | Description               |
| ----------- | ------------------------- |
| `rdkit`     | Molecular manipulation    |
| `datamol`   | Molecular data handling   |
| `molfeat`   | Molecular featurization   |
| `diffdock`  | Molecular docking         |
| `torchdrug` | Drug discovery ML         |
| `pytdc`     | Therapeutics data commons |
| `cobrapy`   | Metabolic modeling        |

### Scientific Communication

| Skill                   | Description                   |
| ----------------------- | ----------------------------- |
| `literature-review`     | Systematic literature reviews |
| `scientific-writing`    | Academic writing assistance   |
| `scientific-schematics` | AI-generated figures          |
| `scientific-slides`     | Presentation generation       |
| `hypothesis-generation` | Hypothesis development        |
| `venue-templates`       | Journal-specific formatting   |
| `citation-management`   | Reference management          |

### Clinical & Medical

| Skill                       | Description               |
| --------------------------- | ------------------------- |
| `clinical-decision-support` | Clinical reasoning        |
| `clinical-reports`          | Medical report generation |
| `treatment-plans`           | Treatment planning        |
| `pyhealth`                  | Healthcare ML             |
| `pydicom`                   | Medical imaging           |

### Laboratory & Integration

| Skill                   | Description              |
| ----------------------- | ------------------------ |
| `benchling-integration` | Lab informatics platform |
| `dnanexus-integration`  | Genomics cloud platform  |
| `pylabrobot`            | Laboratory automation    |
| `flowio`                | Flow cytometry data      |
| `omero-integration`     | Bioimaging platform      |

## Core Workflows

### Literature Review Workflow

```python
# 7-phase systematic literature review
# 1. Planning with PICO framework
# 2. Multi-database search execution
# 3. Screening with PRISMA flow
# 4. Data extraction and quality assessment
# 5. Thematic synthesis
# 6. Citation verification
# 7. PDF generation
```

### Drug Discovery Workflow

```python
# Using RDKit + ChEMBL + datamol
from rdkit import Chem
from rdkit.Chem import Descriptors, AllChem

# 1. Query ChEMBL for bioactivity data
# 2. Calculate molecular properties
# 3. Filter by drug-likeness (Lipinski)
# 4. Similarity screening
# 5. Substructure analysis
```

### Single-Cell Analysis Workflow

```python
# Using scanpy + anndata
import scanpy as sc

# 1. Load and QC data
# 2. Normalization and feature selection
# 3. Dimensionality reduction (PCA, UMAP)
# 4. Clustering (Leiden algorithm)
# 5. Marker gene identification
# 6. Cell type annotation
```

### Hypothesis Generation Workflow

```python
# 8-step systematic process
# 1. Understand phenomenon
# 2. Literature search
# 3. Synthesize evidence
# 4. Generate competing hypotheses
# 5. Evaluate quality
# 6. Design experiments
# 7. Formulate predictions
# 8. Generate report
```

## Sub-Skill Structure

Each sub-skill follows a consistent structure:

```
scientific-skills/
├── SKILL.md                    # This file (catalog/index)
├── skills/                     # Individual skill directories
│   ├── rdkit/
│   │   ├── SKILL.md           # Skill documentation
│   │   ├── references/        # API references, patterns
│   │   └── scripts/           # Example scripts
│   ├── scanpy/
│   ├── biopython/
│   └── ... (139 total)
```

## Invoking Sub-Skills

### Direct Invocation

```javascript
// Invoke specific skill
Skill({ skill: 'scientific-skills/rdkit' });
Skill({ skill: 'scientific-skills/scanpy' });
```

### Chained Workflows

```javascript
// Multi-skill workflow
Skill({ skill: 'scientific-skills/literature-review' });
Skill({ skill: 'scientific-skills/hypothesis-generation' });
Skill({ skill: 'scientific-skills/scientific-schematics' });
```

## Prerequisites

- **Python 3.9+** (3.12+ recommended)
- **uv** package manager (recommended)
- Platform: macOS, Linux, or Windows with WSL2

## Best Practices

1. **Start with the right skill**: Use the category tables above to find appropriate skills
2. **Chain skills for complex workflows**: Literature review → Hypothesis → Experiment design
3. **Use database skills for data access**: Query databases before analysis
4. **Visualize results**: Use matplotlib/seaborn/plotly skills for publication-quality figures
5. **Document findings**: Use scientific-writing skill for formal documentation

## Integration with Agent Framework

### Recommended Agent Pairings

| Agent                | Scientific Skills                     |
| -------------------- | ------------------------------------- |
| `data-engineer`      | polars, dask, vaex, zarr-python       |
| `python-pro`         | All Python-based skills               |
| `database-architect` | Database skills for schema design     |
| `technical-writer`   | literature-review, scientific-writing |

### Example Agent Spawn

```javascript
Task({
  subagent_type: 'python-pro',
  description: 'Analyze molecular dataset with RDKit',
  prompt: `You are the PYTHON-PRO agent with scientific research expertise.

## Task
Analyze the molecular dataset for drug-likeness properties.

## Skills to Invoke
1. Skill({ skill: "scientific-skills/rdkit" })
2. Skill({ skill: "scientific-skills/datamol" })

## Workflow
1. Load molecular data
2. Calculate descriptors
3. Apply Lipinski filters
4. Generate visualization
5. Report findings
`,
});
```

## Resources

### Bundled Documentation

- `skills/*/SKILL.md` - Individual skill documentation
- `skills/*/references/` - API references and patterns
- `skills/*/scripts/` - Example scripts and templates

### External Resources

- [K-Dense AI GitHub](https://github.com/K-Dense-AI/claude-scientific-skills)
- [RDKit Documentation](https://www.rdkit.org/docs/)
- [Scanpy Documentation](https://scanpy.readthedocs.io/)
- [BioPython Tutorial](https://biopython.org/wiki/Tutorial)

## Version History

- **v2.17.0** - Current version with 139 skills
- Integrated from K-Dense-AI/claude-scientific-skills repository

## License

MIT License - Open source and freely available for research and commercial use.
