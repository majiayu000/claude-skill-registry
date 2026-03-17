---
name: cluster-documents
description: Automated content similarity and grouping analysis. Groups related documents by topic, purpose, or content similarity.
required_roles:
  scribe: roles/scribe.viewer
personas: [information-architect, data-analyst, researcher]
---

# Document Clustering Skill

Analyze a repository of documents to group them based on content similarity, topic, or purpose. This skill helps organize large collections, identify redundancies, and discover relationships.

## Inputs

- `PATH` - The repository to analyze (e.g., "/repository")
- `SIMILARITY_THRESHOLD` - (Optional) Float (0.0-1.0), threshold for grouping (default: 0.8)
- `VISUALIZATION` - (Optional) Boolean, whether to generate a visual representation (default: false)

## Workflow

### Step 1: Text Processing

Ingest documents from `PATH`.
- Normalize text (remove stop words, stemming/lemmatization).
- Generate embeddings or TF-IDF vectors for each document.

### Step 2: Clustering Analysis

Apply clustering algorithms (e.g., K-Means, DBSCAN) to the document vectors.
- Group documents that meet the `SIMILARITY_THRESHOLD`.
- Identify outliers or unique documents.

### Step 3: Cluster Labeling

Analyze the centroid or representative terms of each cluster to assign a meaningful label (Topic).

### Step 4: Output Generation

Generate the clustering report.
- If `VISUALIZATION` is true, create a scatter plot or dendrogram data.

## Required Outputs

A `CLUSTERING_REPORT` object containing:
- **Cluster List**: ID, Label, and List of Documents in each cluster.
- **Redundancy Report**: Sets of highly similar documents (potential duplicates).
- **Visualization Data**: (If requested) Coordinates for plotting.

## Quick Reference

- **Purpose**: Organize unstructured content and find duplicates.
- **Techniques**: Text Mining, NLP, Vector Space Models.
