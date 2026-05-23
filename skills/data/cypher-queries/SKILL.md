---
name: cypher-queries
description: Run Cypher queries against the Neo4j knowledge graph. Provides ready-to-use query templates for gene expression, coculture effects, environmental stress, time series, and more. Use when the user wants to query the knowledge graph.
argument-hint: [query-description]
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash(cypher-shell *), Bash(docker exec *)
---

# Cypher Query Skill

Run Cypher queries against the Prochlorococcus-Alteromonas Neo4j knowledge graph.

## Connection

The Neo4j database runs via Docker. Connect using:

```bash
# Via cypher-shell inside the container
docker exec -i biocypher-neo4j cypher-shell -u neo4j -p neo4j
```

To run a query non-interactively:

```bash
echo "MATCH (n) RETURN labels(n), count(*) LIMIT 10;" | docker exec -i biocypher-neo4j cypher-shell -u neo4j -p neo4j
```

If the container name differs, check with `docker ps` first.

## Graph Schema Overview

### Direct Edges (1-hop queries)

**`affects_expression_of`**: Links a cause (organism or environmental condition) to a gene whose expression changed.

- **Source**: `organism_taxon` (coculture partner) OR `environmental_condition` (stress factor)
- **Target**: `gene`
- **Properties**: `log2_fold_change`, `adjusted_p_value`, `expression_direction` (up/down), `time_point`, `publications`
- **Context**: `environmental_treatment_condition_id` (on organism edges), `biological_context` (on environmental edges)

### Hub Model Edges (multi-factorial experiments)

- **`organism_treatment_in_test`**: organism_taxon -> statistical_test
- **`environmental_condition_in_test`**: environmental_condition -> statistical_test
- **`molecular_result_from_test`**: gene/protein -> statistical_test

### Key Node Types

- `gene` (properties: `locus_tag`, `product`)
- `protein` (properties: `primary_protein_name`)
- `organism` / `organism_taxon` (properties: `organism_name`)
- `environmental_condition` (properties: `condition_type`, `name`, plus condition-specific fields)
- `statistical_test` (properties: `name`, `test_type`, `control_condition`, `treatment_condition`, `timepoint`, `organism`)
- `biological_process`, `molecular_function` (GO terms)

## Query Templates

### Find What Affects a Gene

```cypher
// All factors affecting gene expression
MATCH (factor)-[r:affects_expression_of]->(g:gene {locus_tag: 'PMM0001'})
RETURN factor, r.expression_direction, r.log2_fold_change, r.adjusted_p_value
ORDER BY abs(r.log2_fold_change) DESC
```

### Find Genes Affected by Organism Coculture

```cypher
// Genes upregulated by Alteromonas coculture
MATCH (org:organism {organism_name: 'Alteromonas macleodii'})-[r:affects_expression_of {expression_direction: 'up'}]->(g:gene)
RETURN g.locus_tag, g.product, r.log2_fold_change, r.adjusted_p_value
ORDER BY r.log2_fold_change DESC
LIMIT 20

// Genes downregulated by Alteromonas coculture
MATCH (org:organism)-[r:affects_expression_of {expression_direction: 'down'}]->(g:gene)
WHERE org.organism_name CONTAINS 'Alteromonas'
RETURN g.locus_tag, g.product, r.log2_fold_change, r.adjusted_p_value
ORDER BY r.log2_fold_change ASC
LIMIT 20
```

### Find Genes Affected by Environmental Stress

```cypher
// Genes affected by nitrogen stress
MATCH (env:environmental_condition {condition_type: 'nutrient_stress'})-[r:affects_expression_of]->(g:gene)
WHERE env.nitrogen_level = 'starved'
RETURN g.locus_tag, g.product, r.expression_direction, r.log2_fold_change
ORDER BY abs(r.log2_fold_change) DESC

// Genes affected by light/dark shift
MATCH (env:environmental_condition)-[r:affects_expression_of]->(g:gene)
WHERE env.light_condition = 'darkness'
RETURN g.locus_tag, r.expression_direction, r.log2_fold_change
```

### Compare Conditions

```cypher
// Genes affected by BOTH Alteromonas AND nitrogen stress
MATCH (org:organism)-[r1:affects_expression_of]->(g:gene)
WHERE org.organism_name CONTAINS 'Alteromonas'
MATCH (env:environmental_condition)-[r2:affects_expression_of]->(g)
WHERE env.nitrogen_level = 'starved'
RETURN g.locus_tag, g.product,
       r1.expression_direction AS coculture_direction,
       r2.expression_direction AS stress_direction,
       r1.log2_fold_change AS coculture_fc,
       r2.log2_fold_change AS stress_fc

// Genes with OPPOSITE response to coculture vs stress
MATCH (org:organism)-[r1:affects_expression_of]->(g:gene)
MATCH (env:environmental_condition)-[r2:affects_expression_of]->(g)
WHERE r1.expression_direction <> r2.expression_direction
RETURN g.locus_tag, g.product, r1.expression_direction, r2.expression_direction
```

### Filter by Context (Environmental Condition)

```cypher
// Genes affected by Alteromonas under specific environmental conditions
MATCH (org:organism)-[r:affects_expression_of]->(g:gene)
WHERE org.organism_name CONTAINS 'Alteromonas'
MATCH (env:environmental_condition {id: r.environmental_treatment_condition_id})
WHERE env.light_condition = 'continuous_light'
RETURN g.locus_tag, r.log2_fold_change, env.name

// Compare coculture response under different environmental conditions
MATCH (org:organism)-[r1:affects_expression_of]->(g:gene)
MATCH (env1:environmental_condition {id: r1.environmental_treatment_condition_id})
WHERE env1.light_condition = 'continuous_light'
MATCH (org)-[r2:affects_expression_of]->(g)
MATCH (env2:environmental_condition {id: r2.environmental_treatment_condition_id})
WHERE env2.light_condition = 'darkness'
RETURN g.locus_tag,
       r1.log2_fold_change AS light_fc,
       r2.log2_fold_change AS dark_fc,
       env1.name AS light_condition,
       env2.name AS dark_condition
ORDER BY abs(r1.log2_fold_change - r2.log2_fold_change) DESC
```

### Get Gene Details with Function

```cypher
// Gene with its protein and GO annotations
MATCH (g:gene {locus_tag: 'PMM0001'})
OPTIONAL MATCH (g)-[:Gene_encodes_protein]->(p:protein)
OPTIONAL MATCH (p)-[:protein_involved_in_biological_process]->(bp:biological_process)
OPTIONAL MATCH (p)-[:protein_enables_molecular_function]->(mf:molecular_function)
RETURN g.locus_tag, g.product, p.primary_protein_name,
       collect(DISTINCT bp.name) AS biological_processes,
       collect(DISTINCT mf.name) AS molecular_functions
```

### Find Functionally Related Affected Genes

```cypher
// Genes in same biological process that are affected by Alteromonas
MATCH (org:organism)-[r:affects_expression_of]->(g:gene)
WHERE org.organism_name CONTAINS 'Alteromonas'
MATCH (g)-[:Gene_encodes_protein]->(p:protein)-[:protein_involved_in_biological_process]->(bp:biological_process)
RETURN bp.name AS process,
       collect(g.locus_tag) AS affected_genes,
       avg(r.log2_fold_change) AS avg_fold_change,
       count(g) AS gene_count
ORDER BY gene_count DESC
LIMIT 10
```

### Multi-factorial Experiments (Hub Model)

```cypher
// Find experiments with both coculture and environmental stress
MATCH (org:organism)-[:organism_treatment_in_test]->(test:statistical_test)
MATCH (env:environmental_condition)-[:environmental_condition_in_test]->(test)
RETURN test.name, org.organism_name, env.name, test.timepoint

// Get gene results from multi-factorial experiment
MATCH (org:organism)-[:organism_treatment_in_test]->(test:statistical_test)
MATCH (env:environmental_condition)-[:environmental_condition_in_test]->(test)
MATCH (g:gene)-[r:molecular_result_from_test]->(test)
WHERE org.organism_name CONTAINS 'Alteromonas'
RETURN g.locus_tag, r.log2_fold_change, r.direction,
       org.organism_name, env.name
ORDER BY abs(r.log2_fold_change) DESC
```

### Significance Filtering

```cypher
// Significantly differentially expressed genes (p < 0.05, |FC| > 2)
MATCH (factor)-[r:affects_expression_of]->(g:gene)
WHERE r.adjusted_p_value < 0.05 AND abs(r.log2_fold_change) > 1
RETURN factor, g.locus_tag, r.expression_direction, r.log2_fold_change, r.adjusted_p_value
ORDER BY r.adjusted_p_value ASC

// Top 10 most significantly affected genes
MATCH (org:organism)-[r:affects_expression_of]->(g:gene)
WHERE org.organism_name CONTAINS 'Alteromonas'
RETURN g.locus_tag, g.product, r.log2_fold_change, r.adjusted_p_value
ORDER BY r.adjusted_p_value ASC
LIMIT 10
```

### Time Series Analysis

```cypher
// Gene expression across time points
MATCH (org:organism)-[r:affects_expression_of]->(g:gene {locus_tag: 'PMM0001'})
WHERE org.organism_name CONTAINS 'Alteromonas'
RETURN r.time_point, r.log2_fold_change, r.expression_direction
ORDER BY r.time_point

// Genes with consistent response across time
MATCH (org:organism)-[r:affects_expression_of]->(g:gene)
WITH g, collect(r.expression_direction) AS directions
WHERE size([d IN directions WHERE d = 'up']) = size(directions)
   OR size([d IN directions WHERE d = 'down']) = size(directions)
RETURN g.locus_tag, g.product, directions
```

### Publication Traceability

```cypher
// Find which publication reported the expression change
MATCH (factor)-[r:affects_expression_of]->(g:gene)
WHERE g.locus_tag = 'PMM0001'
RETURN factor, r.log2_fold_change, r.publications

// All genes from a specific study
MATCH (factor)-[r:affects_expression_of]->(g:gene)
WHERE 'doi:10.1234/example' IN r.publications
RETURN g.locus_tag, factor, r.expression_direction
```

## Workflow

When the user invokes this skill (e.g., `/cypher-queries "genes affected by Alteromonas"`):

1. Understand the user's query intent
2. Select or adapt the most appropriate template above
3. Substitute actual values (gene IDs, organism names, conditions) as needed
4. Run the query against Neo4j via `docker exec`
5. Present the results in a readable format
6. Offer follow-up queries if appropriate
