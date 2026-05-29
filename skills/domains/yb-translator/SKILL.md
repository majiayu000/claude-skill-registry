---
name: yb-translator
description: Translate programming concepts to biological parallels using real ontology terms from EBI OLS.
---

# YB Translator

Translate programming/CS concepts to biological parallels. **Must use real ontology IDs from EBI OLS.**

## Required Output Format

```
CONCEPT: [programming concept]
BIOLOGY: [biological parallel]
ONTOLOGY: [Ontology Name] - [Term Name] ([ID])
EXAMPLE: [specific instance from ontology]
SOURCE: https://www.ebi.ac.uk/ols4/ontologies/[ont]/classes/[encoded-iri]
```

## Ontologies to Use

| Ontology | Code | Use For |
|----------|------|---------|
| Cell Ontology | CL | Cell types, differentiation |
| Gene Ontology | GO | Processes, functions, components |
| Disease Ontology | MONDO | Disease hierarchies |
| Tissue/Anatomy | UBERON | Anatomical structures |
| Phenotype | HP | Observable traits |
| Pathway | REACT/KEGG | Metabolic/signaling pathways |

## Bionty Integration

For programmatic access to biological ontologies, use [Bionty](https://github.com/laminlabs/bionty):

```python
import bionty as bt

# Lookup GO terms
go = bt.Gene()
go.lookup("RNA polymerase")

# Cell ontology
cl = bt.CellType()
cl.search("T cell")
```

Bionty provides versioned, validated access to CL, GO, MONDO, UBERON, and more.

## Fetch Live Data

```bash
bb ~/.claude/skills/yb-translator/scripts/fetch_ontology.clj verify <ID>
```

Example:
```bash
bb ~/.claude/skills/yb-translator/scripts/fetch_ontology.clj verify CL:0000084
```

## Translation Examples

### Immutability

```
CONCEPT: Immutable data structures
BIOLOGY: DNA template strand
ONTOLOGY: Gene Ontology - DNA replication (GO:0006260)
EXAMPLE: Template strand unchanged during replication; new strand synthesized
SOURCE: https://www.ebi.ac.uk/ols4/ontologies/go/classes/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252FGO_0006260
```

### Inheritance/Subtyping

```
CONCEPT: Class inheritance
BIOLOGY: Cell differentiation hierarchy
ONTOLOGY: Cell Ontology - T cell (CL:0000084)
EXAMPLE: T cell → CD4+ T cell (CL:0000624), CD8+ T cell (CL:0000625)
SOURCE: https://www.ebi.ac.uk/ols4/ontologies/cl/classes/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252FCL_0000084
```

### Interface/Protocol

```
CONCEPT: Interface contract
BIOLOGY: Enzyme classification by function
ONTOLOGY: Gene Ontology - kinase activity (GO:0016301)
EXAMPLE: All kinases transfer phosphate; different substrates
SOURCE: https://www.ebi.ac.uk/ols4/ontologies/go/classes/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252FGO_0016301
```

### Garbage Collection

```
CONCEPT: Automatic memory management
BIOLOGY: Autophagy
ONTOLOGY: Gene Ontology - autophagy (GO:0006914)
EXAMPLE: Lysosomal degradation of cytoplasmic components
SOURCE: https://www.ebi.ac.uk/ols4/ontologies/go/classes/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252FGO_0006914
```

### Static Type Checking

```
CONCEPT: Compile-time type verification
BIOLOGY: Receptor-ligand specificity
ONTOLOGY: Gene Ontology - receptor binding (GO:0005102)
EXAMPLE: Insulin receptor (INSR) only binds insulin; shape verified before signal
SOURCE: https://www.ebi.ac.uk/ols4/ontologies/go/classes/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252FGO_0005102
```

### Recursion

```
CONCEPT: Self-referential function
BIOLOGY: Fractal branching morphogenesis
ONTOLOGY: Gene Ontology - branching morphogenesis (GO:0001763)
EXAMPLE: Lung bronchi: branch → branches → branches (same pattern each level)
SOURCE: https://www.ebi.ac.uk/ols4/ontologies/go/classes/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252FGO_0001763
```

### Concurrency

```
CONCEPT: Parallel execution
BIOLOGY: Parallel metabolic pathways
ONTOLOGY: Gene Ontology - metabolic process (GO:0008152)
EXAMPLE: Glycolysis and beta-oxidation run simultaneously in cytoplasm/mitochondria
SOURCE: https://www.ebi.ac.uk/ols4/ontologies/go/classes/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252FGO_0008152
```

### Preconditions (Dafny requires)

```
CONCEPT: Function precondition
BIOLOGY: Enzyme substrate specificity
ONTOLOGY: Gene Ontology - substrate-specific channel activity (GO:0022838)
EXAMPLE: Lactase only accepts lactose; wrong substrate = no reaction
SOURCE: https://www.ebi.ac.uk/ols4/ontologies/go/classes/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252FGO_0022838
```

### Postconditions (Dafny ensures)

```
CONCEPT: Function postcondition
BIOLOGY: Enzyme product guarantee
ONTOLOGY: Gene Ontology - catalytic activity (GO:0003824)
EXAMPLE: Lactase guarantees galactose + glucose output from lactose input
SOURCE: https://www.ebi.ac.uk/ols4/ontologies/go/classes/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252FGO_0003824
```

### Formal Verification (Dafny)

```
CONCEPT: Compile-time proof of correctness
BIOLOGY: Immune checkpoint verification
ONTOLOGY: Gene Ontology - T cell activation (GO:0042110)
EXAMPLE: T cell requires MHC presentation + costimulation; verified before response
SOURCE: https://www.ebi.ac.uk/ols4/ontologies/go/classes/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252FGO_0042110
```

### REPL (Clojure)

```
CONCEPT: Interactive evaluation loop
BIOLOGY: Adaptive immune response
ONTOLOGY: Gene Ontology - adaptive immune response (GO:0002250)
EXAMPLE: Encounter antigen → test response → remember successful patterns
SOURCE: https://www.ebi.ac.uk/ols4/ontologies/go/classes/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252FGO_0002250
```

### Homoiconicity (Clojure)

```
CONCEPT: Code as data
BIOLOGY: Self-replicating RNA polymerase ribozymes
ONTOLOGY: Gene Ontology - RNA polymerase activity (GO:0097747)
EXAMPLE: Ribozymes catalyze synthesis of copies of themselves—RNA is simultaneously 
         catalyst (program) and template (data). E.g., R3C ligase (Joyce 2002).
SOURCE: https://www.ebi.ac.uk/ols4/ontologies/go/classes/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252FGO_0097747
```

## Rules

1. **Always include ontology ID** (e.g., CL:0000084, GO:0006914)
2. **Always include SOURCE URL** to EBI OLS
3. **Use real terms** - verify they exist at ebi.ac.uk/ols4
4. **One parallel per concept** - no tables, no frills
5. **Run fetch script** when uncertain about term existence

## Related Skills (Random Walk r=3)

| Skill | Relation | Trit |
|-------|----------|------|
| **assembly-index** | Cronin's molecular complexity → code complexity | ⊕ |
| **alife** | Artificial life / origin of life parallels | ○ |
| **turing-chemputer** | Chemical computation ↔ biological computation | ⊖ |

Cross-comparison: All three skills explore the code↔chemistry↔life boundary that yb-translator maps via ontologies.


## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 7. Propagators

**Concepts**: propagator, cell, constraint, bidirectional, TMS

### GF(3) Balanced Triad

```
yb-translator (○) + SDF.Ch7 (○) + [balancer] (○) = 0
```

**Skill Trit**: 0 (ERGODIC - coordination)

### Secondary Chapters

- Ch5: Evaluation
- Ch4: Pattern Matching

### Connection Pattern

Propagators flow constraints bidirectionally. This skill propagates information.
