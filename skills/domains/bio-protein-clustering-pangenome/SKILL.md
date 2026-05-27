---
name: bio-protein-clustering-pangenome
description: Cluster proteins into orthogroups and derive pangenome matrices.
---

# Bio Protein Clustering Pangenome

## When to use
- Cluster proteins into orthogroups and derive pangenome matrices.

## Prerequisites
- Tools installed via pixi (see pixi.toml).
- Protein FASTA inputs are available.

## Inputs
- proteins.faa (FASTA protein sequences)

## Outputs
- results/bio-protein-clustering-pangenome/orthogroups.tsv
- results/bio-protein-clustering-pangenome/presence_absence.parquet
- results/bio-protein-clustering-pangenome/pangenome_report.md
- results/bio-protein-clustering-pangenome/logs/

## Concepts

### Pangenome Components
The **pangenome** (pan-genome or supragenome) is the entire set of genes from all strains within a clade. It can be partitioned into distinct categories:

- **Core genome**: Genes present in all (or >99%) of genomes. These represent essential housekeeping functions and shared metabolic capabilities. Typically includes ~100 single-copy proteins in bacteria (ribosomal proteins, RNA/DNA polymerases, DNA repair proteins).

- **Shell genome**: Genes present at intermediate frequencies (typically 15-95% of genomes). These provide adaptive advantages in specific environments.

- **Accessory genome**: Genes present in a subset of genomes (<99% to ≥15%). Contains dispensable genes that provide niche-specific adaptations.

- **Cloud genome**: Rare genes present in very few genomes (<15%). Often includes strain-specific genes (singletons) and recently acquired genes.

### Gene Types in Pangenome Analysis

- **Orthologs**: Homologous genes that diverged via speciation (vertical inheritance). Present in multiple genomes with shared ancestry.

- **Single-copy orthologs (SCOs)**: Orthologous groups where each genome is represented by exactly one gene. Critical for phylogenetic analysis and genome completeness assessment (BUSCO scores).

- **Pan-orthologs**: All orthologous genes across the entire pangenome, including both single-copy and multi-copy orthologs.

- **Paralogs**: Homologous genes that arose via duplication within a lineage. Multiple copies may exist within a single genome. Can complicate ortholog identification if not properly discriminated.

- **Singletons**: Genes with no sequence homology to genes in any other genome in the dataset. Present in one and only one genome. May represent unique adaptations, recent horizontal gene transfers, or annotation artifacts.

### Key Metrics

- **Pangenome size**: Total number of unique gene families across all genomes
- **Core genome size**: Number of gene families present in all genomes
- **Accessory genome size**: Pangenome size - Core genome size
- **Genome completeness**: Percentage of expected single-copy orthologs present in a genome
- **Orthogroup occupancy**: Percentage of genomes represented in an orthogroup

## Steps
1. Cluster proteins with MMseqs2 or ProteinOrtho.
2. Build presence/absence matrix.
3. Compute core/accessory/cloud/singleton partitions.
4. Identify single-copy orthologs for phylogenetic analysis.
5. Discriminate paralogs from orthologs in multi-copy gene families.
6. Calculate pangenome statistics (completeness, orthogroup occupancy).

## Analyzing Orthogroups Output

### Understanding Orthogroup Tables
Orthogroup clustering tools (MMseqs2, ProteinOrtho, OrthoFinder, OrthoMCL) produce tables where:
- Rows = orthogroups (gene families)
- Columns = genomes
- Cells = gene identifiers (or counts)

### Identifying Single-Copy Pan-Orthologs
Single-copy pan-orthologs are the gold standard for phylogenetics and represent genes present exactly once in all genomes:

```python
# Filter for single-copy orthologs present in all genomes
sco_mask = (orthogroups_df.notna().sum(axis=1) == n_genomes) & \
           (orthogroups_df.notna().sum(axis=1) == orthogroups_df.count(axis=1))
single_copy_orthologs = orthogroups_df[sco_mask]
```

**Criteria**:
- Presence: Gene exists in 100% of genomes
- Copy number: Exactly 1 gene per genome
- Minimum occupancy: Often require ≥50% occupancy for relaxed SCO sets

### Finding Multi-Copy Orthologs (Paralogs)
Paralogs indicate gene duplication events:

```python
# Identify orthogroups with paralogs (>1 copy in any genome)
multi_copy_mask = orthogroups_df.apply(
    lambda row: any(isinstance(x, str) and ',' in x for x in row),
    axis=1
)
paralog_groups = orthogroups_df[multi_copy_mask]
```

**Analysis considerations**:
- Distinguish true paralogs from assembly artifacts
- Evaluate if duplication is lineage-specific or ancient
- Use conserved gene neighborhood (synteny) to refine ortholog assignments

### Identifying Singletons
Singletons are unique to one genome:

```python
# Find genes present in only one genome
singleton_mask = orthogroups_df.notna().sum(axis=1) == 1
singletons = orthogroups_df[singleton_mask]
```

**Interpretation**:
- Strain-specific adaptations
- Recently acquired via horizontal gene transfer (HGT)
- Potential annotation errors or poor quality genes
- Genes under rapid evolution or gene loss events

### Calculating Core vs Accessory Genome
Partition orthogroups by presence frequency:

```python
# Calculate presence across genomes
presence_freq = orthogroups_df.notna().sum(axis=1) / n_genomes

# Core genome (present in ≥99% of genomes)
core = orthogroups_df[presence_freq >= 0.99]

# Accessory genome (present in 15-99% of genomes)
accessory = orthogroups_df[(presence_freq >= 0.15) & (presence_freq < 0.99)]

# Cloud genome (present in <15% of genomes)
cloud = orthogroups_df[presence_freq < 0.15]
```

**Threshold guidance**:
- Core: ≥95-99% (adjust based on genome quality)
- Shell: 15-95% (intermediate frequency)
- Cloud: <15% (rare genes)

### Common Analysis Patterns for Microbial Comparative Genomics

1. **Completeness assessment**: Count single-copy orthologs per genome to evaluate assembly/annotation quality

2. **Pan-genome openness**: Plot cumulative gene count vs number of genomes
   - Open pangenome: Continues to grow with new genomes
   - Closed pangenome: Plateaus after sufficient sampling

3. **Phylogenetic marker identification**: Extract single-copy core genes for species tree construction

4. **Functional profiling**: Annotate orthogroups with COG/KEGG/Pfam to understand functional distribution across core/accessory partitions

5. **Presence/absence patterns**: Identify genes associated with phenotypes (pathogenicity, antibiotic resistance, niche adaptation)

### Decision Points

**If few single-copy orthologs identified (<50)**:
- Check genome annotation quality
- Verify genomes are from same species/genus
- Consider contamination or misassembled genomes
- Adjust clustering stringency

**If excessive singletons (>30% of genes)**:
- Review annotation parameters (overprediction likely)
- Check for contamination
- Evaluate sequence quality and completeness
- Consider stricter clustering thresholds

**If no clear core genome emerges**:
- Dataset may span too broad taxonomic range
- Poor quality genomes present
- Incorrect species assignments

## QC gates
- Cluster size distributions meet project thresholds.
- Matrix completeness meets project thresholds.
- On failure: retry with alternative parameters; if still failing, record in report and exit non-zero.

## Downstream Analysis

### Filtering Orthogroups by Presence/Absence Patterns

**Extract core genome genes**:
```bash
# Get orthogroups present in all genomes
awk -F'\t' 'NR==1 || (NF-1 == n_genomes && !/\t\t/)' orthogroups.tsv > core_orthogroups.tsv
```

**Find lineage-specific genes**:
```python
# Identify genes specific to a subset of genomes
lineage_genomes = ['genome1', 'genome2', 'genome3']
lineage_specific = orthogroups_df[
    (orthogroups_df[lineage_genomes].notna().all(axis=1)) &
    (orthogroups_df.drop(columns=lineage_genomes).isna().all(axis=1))
]
```

**Presence correlation analysis**:
```python
# Find genes with correlated presence patterns
from scipy.cluster.hierarchy import linkage, dendrogram
presence_matrix = orthogroups_df.notna().astype(int)
linkage_matrix = linkage(presence_matrix, method='average', metric='jaccard')
```

### Extracting Alignments from Single-Copy Orthologs

**Workflow for phylogenetic analysis**:
1. Identify single-copy core orthogroups (100% presence, 1 copy each)
2. Extract protein sequences for each orthogroup
3. Align each orthogroup separately with MAFFT/MUSCLE
4. Trim alignments with trimAl or BMGE
5. Concatenate alignments into supermatrix
6. Build phylogenetic tree with IQ-TREE/RAxML

```bash
# Example: Extract sequences for single-copy orthogroup
for og in single_copy_orthogroups.txt; do
  grep -A1 -f <(cut -f2- orthogroups.tsv | grep "^${og}") proteins.faa > ${og}.faa
  mafft --auto ${og}.faa > ${og}.aln
  trimal -in ${og}.aln -out ${og}.trim -automated1
done

# Concatenate alignments
cat *.trim > concatenated_alignment.faa
```

### Identifying Horizontally Transferred Genes (HGT)

**Indicators of horizontal gene transfer**:
- Genes present in distant taxa but absent in close relatives
- Atypical GC content compared to genome average
- Different codon usage bias
- Phylogenetic incongruence (gene tree vs species tree)
- Presence in mobile genetic elements (plasmids, integrons, transposons)

**Analysis approach**:
```python
# Flag orthogroups with sparse, patchy distribution
def detect_hgt_candidates(presence_df, threshold=0.3):
    """Identify orthogroups with discontinuous presence patterns"""
    hgt_candidates = []
    for og in presence_df.index:
        presence = presence_df.loc[og]
        freq = presence.sum() / len(presence)
        # Low frequency + non-clustered distribution suggests HGT
        if 0.05 < freq < threshold:
            hgt_candidates.append(og)
    return hgt_candidates
```

**Validation steps**:
1. Align HGT candidate genes
2. Build individual gene trees
3. Compare to species tree topology
4. BLAST against broader database to find donor lineages
5. Check for association with mobile elements

### Functional Enrichment of Accessory Genome

**Annotate orthogroups**:
```bash
# Functional annotation with eggNOG-mapper
for og in accessory_orthogroups.txt; do
  emapper.py -i ${og}.faa --output ${og}_annotation
done
```

**Enrichment analysis**:
```python
# Test for overrepresented functions in accessory genome
from scipy.stats import fisher_exact

def enrichment_analysis(core_functions, accessory_functions, total_functions):
    """Fisher's exact test for functional enrichment"""
    enriched = []
    for func in set(accessory_functions):
        a = accessory_functions.count(func)  # Function in accessory
        b = len(accessory_functions) - a      # Other functions in accessory
        c = core_functions.count(func)        # Function in core
        d = len(core_functions) - c           # Other functions in core

        odds_ratio, p_value = fisher_exact([[a, b], [c, d]])
        if p_value < 0.05 and odds_ratio > 1:
            enriched.append((func, odds_ratio, p_value))
    return enriched
```

**Common patterns in bacterial accessory genomes**:
- Antibiotic resistance genes
- Virulence factors and toxins
- Secondary metabolite biosynthesis clusters
- Restriction-modification systems
- Niche-specific transporters and catabolic pathways

### Pangenome Visualization

**Recommended plots**:
1. **Pan-genome accumulation curve**: Genes vs genomes added
2. **Core genome decay curve**: Core size vs genomes added
3. **Presence/absence heatmap**: Orthogroups × genomes
4. **Functional category distribution**: Core vs accessory annotations
5. **Phylogenetic tree with gene presence**: Map accessory genes onto phylogeny

```python
# Example: Pan-genome accumulation
import matplotlib.pyplot as plt
import numpy as np
from itertools import permutations

def pangenome_curve(presence_df, n_permutations=100):
    """Calculate pan-genome growth curve"""
    n_genomes = presence_df.shape[1]
    genome_order = list(range(n_genomes))

    pan_sizes = np.zeros((n_permutations, n_genomes))

    for i in range(n_permutations):
        np.random.shuffle(genome_order)
        cumulative_genes = set()
        for j, genome_idx in enumerate(genome_order):
            cumulative_genes.update(
                presence_df.iloc[:, genome_idx].dropna().index
            )
            pan_sizes[i, j] = len(cumulative_genes)

    mean_pan = pan_sizes.mean(axis=0)
    std_pan = pan_sizes.std(axis=0)

    plt.plot(range(1, n_genomes+1), mean_pan)
    plt.fill_between(range(1, n_genomes+1),
                     mean_pan-std_pan, mean_pan+std_pan, alpha=0.3)
    plt.xlabel('Number of genomes')
    plt.ylabel('Number of gene families')
    plt.title('Pan-genome accumulation')
    return mean_pan
```

## Validation
- Verify proteins.faa is non-empty and amino acid encoded.

## Tools

### Primary Clustering Tools
- **mmseqs2 v18-8cc5c**: Ultra-fast sequence clustering and search. Good for large datasets (>1000 genomes).
- **proteinortho v6.3.6**: Detects orthologs using reciprocal best hits with graph-based clustering.
- **OrthoFinder**: Phylogenetic orthology inference with gene trees, duplication events, and species tree. Excellent for detailed comparative genomics and paralog discrimination.
- **OrthoMCL**: Uses conserved gene neighborhood for improved paralog separation. Good for closely related bacterial strains.

### Tool Selection Guide
- **Small datasets (<50 genomes)**: OrthoFinder (most comprehensive output)
- **Medium datasets (50-500 genomes)**: ProteinOrtho or MMseqs2
- **Large datasets (>500 genomes)**: MMseqs2 (fastest)
- **Closely related strains**: OrthoMCL or PEPPAN (paralog discrimination)
- **High phylogenetic resolution needed**: OrthoFinder (produces gene trees)

### Recommended Pipelines
- **GET_HOMOLOGUES**: Comprehensive bacterial pan-genome analysis with multiple clustering algorithms
- **Roary**: Fast pan-genome pipeline specifically for prokaryotes
- **PEPPAN**: Accurate reconstruction with paralogous score calculation
- **BPGA**: Browser-based pan-genome analysis platform
- **Anvi'o**: Integrated pangenomics with visualization
- **RIBAP**: Core genome annotation pipeline for pangenome calculation beyond species level

## Paper summaries (2023-2025)
- summaries/ (include example use cases and tool settings used)

## Tool documentation
- [MMseqs2](docs/mmseqs2.html) - Ultra-fast sequence clustering and search
- [ProteinOrtho](docs/proteinortho.html) - Ortholog detection with reciprocal best hits

## References

### Key Concepts and Definitions
- [Pan-genome - Wikipedia](https://en.wikipedia.org/wiki/Pan-genome)
- [The bacterial pangenome as a new tool for analysing pathogenic bacteria - PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC4552756/)
- [A gentle introduction to pangenomics - PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11570541/)
- [First Steps in the Analysis of Prokaryotic Pan-Genomes](https://journals.sagepub.com/doi/full/10.1177/1177932220938064)

### Tools and Methods
- [OrthoFinder: phylogenetic orthology inference for comparative genomics - Genome Biology](https://link.springer.com/article/10.1186/s13059-019-1832-y)
- [Linkage-based ortholog refinement in bacterial pangenomes with CLARC - Nucleic Acids Research](https://academic.oup.com/nar/article/53/12/gkaf488/8169778)
- [RIBAP: comprehensive bacterial core genome annotation pipeline - Genome Biology](https://genomebiology.biomedcentral.com/articles/10.1186/s13059-024-03312-9)
- [Accurate reconstruction of bacterial pan- and core genomes with PEPPAN - PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC7605250/)
- [OrthoSNAP: tree splitting and pruning algorithm for single-copy orthologs - PLOS Biology](https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.3001827)

### Analysis Strategies
- [Comparison of gene clustering criteria reveals intrinsic uncertainty in pangenome analyses - Genome Biology](https://genomebiology.biomedcentral.com/articles/10.1186/s13059-023-03089-3)
- [Genome and pan-genome analysis to classify emerging bacteria - Biology Direct](https://link.springer.com/article/10.1186/s13062-019-0234-0)
- [An anvi'o workflow for microbial pangenomics](https://merenlab.org/2016/11/08/pangenomics-v2/)
- [Exploring OrthoFinder's results - OrthoFinder Tutorials](https://davidemms.github.io/orthofinder_tutorials/exploring-orthofinders-results.html)

### Recent Developments
- [Genotyping sequence-resolved CNV using pangenomes - Nature Genetics](https://www.nature.com/articles/s41588-025-02346-4)
- [M1CR0B1AL1Z3R 2.0: enhanced web server for bacterial genome analysis - Nucleic Acids Research](https://academic.oup.com/nar/article/53/W1/W369/8131114)
- [OrthoDB in 2025: annotation of orthologs with wider sampling - Nucleic Acids Research](https://academic.oup.com/nar/article/53/D1/D516/7899526)

### Additional Resources
- See ../bio-skills-references.md
