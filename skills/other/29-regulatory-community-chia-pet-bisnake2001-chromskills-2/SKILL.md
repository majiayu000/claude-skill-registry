---
name: regulatory-community-analysis-ChIA-PET
description: This skill performs protein-mediated regulatory community analysis from ChIA-PET datasets and provide a way for visualizing the communities. Use this skill when you have a annotated peak file (in BED format) from ChIA-PET experiment and you want to identify the protein-mediated regulatory community according to the BED and BEDPE file from ChIA-PET.
---

# Protein-Mediated Regulatory Community Analysis from ChIA-PET

## 1. Overview

Main steps include:

- Refer to the **Inputs & Outputs** section to check available inputs and design the output structure.
- Standardize the information contained in the BED format peak file.
- Build a chromatin interaction network where:
   - nodes = protein binding sites (peaks)
   - edges = protein-mediated loops.
- Detect regulatory communities (3D modules) using graph clustering.
- Prioritize hub anchors using network centrality.
- Visualize the largest regulatory communities.

Tools called in this skill:

- `mcp__igraph-tools__build_chromatin_network`
- `mcp__igraph-tools__analyze_chromatin_network`
- `mcp__igraph-tools__plot_chromatin_communities`

---

## 2. When to use this skill

Use this skill when you have ChIA-PET data in BEDPE and BED format and you want to:

- Reveal **regulatory communities** (3D modules) formed by:
  - promoters
  - enhancers
  - other regulatory elements
- Identify **hub anchors** (peaks involved in many interactions) for a particular protein.
- Study **protein-mediated rewiring** of chromatin structure between conditions by comparing networks.
- Generate interpretable **network visualizations** for specific communities or loci.

Typical biological questions:

- Which promoters act as 3D regulatory hubs for my ChIA-PET factor (e.g., RNAPII, CTCF)?
- Which enhancers cluster with a given gene in 3D?
- Do disease-associated loci participate in specific regulatory communities?
- How does the chromatin interaction network structure change under perturbation (e.g., KO, treatment)?

---

## Inputs & Outputs

### Inputs

```bash
<sample>.bedpe # ChIA-PET loops: chr1  start1  end1  chr2  start2  end2  PET_count  [optional extra fields...]
<sample>.bed # Tab-delimited file with at least 3 columns: chr, start, end
```

### Outputs

```bash
ChIA_PET_community/
  communities/
    ${sample}_communities_membership.tsv # Network membership table
    ${sample}.graphml
  plots/
    ${sample}_communities.pdf # Community network plots
  temp/
    ... # other temp files
```

---

## Decision tree

### Step 1: Standardize the information contained in the BED format peak file

- Check whether the <peak_id> and <type> (e.g. promoter or other annotations) information if provided in the BED file.
- If not provided, assign "peak_${i}" as the <peak_id> column and "others" as the <type> column.
- Make sure that order of the information in the BED file is:
  - 'chr' 'start' 'end' 'peak_id' 'type'

### Step 2: Build the Chromatin Interaction Network
Call:

- `mcp__igraph-tools__build_chromatin_network`

with:

- `loops_file`: path to BEDPE-like loops file.
- `peaks_file`: path to annotated peaks BED file.
- `proj_dir`: project directory (e.g. `ChIA_PET_community`).
- `graph_name` (optional): output GraphML filename.
- `min_pet` (optional): filter on PET counts (default `1`).

This tool will:

- Reads the loops and peaks files.
- Builds an **undirected igraph**:
- Saves the graph as:
   - `${sample}.graphml` (GraphML)

---

### Step 2: Detect Communities and Compute Network Centrality

Call:

- `mcp__igraph-tools__analyze_chromatin_network`

with:

- `graph_path`: GraphML file from Step 1 (e.g. `${sample}.graphml`).
- `proj_dir`: same project directory.
- `membership_name` (optional): output TSV name, (e.g. `${sample}_communities_membership.tsv`).
- `weight_attr` (optional): edge weight attribute, default `"weight"`.
- `seed` (optional): random seed for community detection, default `1`.

This tool will:

- Load the GraphML network.
- Run **Louvain (multilevel)** community detection
- Compute centralities
- Export a **membership table**:
  `${sample}_communities_membership.tsv` with columns

- Update the GraphML file with the new vertex attributes (community & centralities).

### Step 3 — Visualize Top Regulatory Communities

Call:

- `mcp__igraph-tools__plot_chromatin_communities`

with:

- `graph_path`: GraphML file with community attributes (from Step 2).
- `proj_dir`: project directory.
- `pdf_name` (optional): output PDF filename (e.g. `${sample}_communities.pdf`).
- `top_n` (optional): number of largest communities to plot, default `12`.
- `size_attr` (optional): vertex attribute for node size, default `"degree"`.
- `community_attr` (optional): vertex attribute containing community IDs, default `"community"`.

This tool will:

- Load the graph and verify that `community_attr` is present.
- Compute **plot aesthetics**
- Identify the **largest communities** (by vertex count), up to `top_n`.
- For each community:
   - Create an induced subgraph.
   - Compute a **Fruchterman–Reingold** layout.
   - Draw nodes + edges + labels into a separate page of a multi-page PDF.
- Save the PDF as:
   - `${sample}_communities.pdf`
