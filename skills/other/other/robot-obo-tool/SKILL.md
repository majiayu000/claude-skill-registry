---
name: robot-obo-tool
description: Skills for using ROBOT, the OBO ontology command-line toolkit for reasoning, template-based term creation, quality control, format conversion, and ontology manipulation. Use this when working with OWL/OBO ontologies that need automated processing.
---

# ROBOT Guide

## Overview

ROBOT (ROBOT is an OBO Tool) is the standard command-line tool for OBO ontology development. It handles reasoning, quality control, format conversion, module extraction, template-based term generation, and release automation. Almost every OBO Foundry ontology uses ROBOT in its build pipeline.

ROBOT is a Java application distributed as a JAR with a shell wrapper script.

Home page: <https://robot.obolibrary.org/>

## When to Use

Use ROBOT when you need to:

- **Reason over an ontology** - classify, check consistency, find unsatisfiable classes
- **Generate terms from templates** - create OWL from TSV/CSV spreadsheets
- **Run quality control** - check for missing labels, definitions, bad xrefs
- **Convert formats** - between OWL, OBO, Turtle, OFN, Manchester, JSON
- **Extract modules** - pull subsets from large ontologies
- **Diff ontologies** - compare two versions at the OWL level (consider OAK for higher level diffs)
- **Query with SPARQL** - run SELECT/CONSTRUCT/ASK queries
- **Build release pipelines** - chain commands for automated releases

Do NOT use ROBOT when:

- You want to search external ontologies interactively - use OAK or OLS MCP instead
- You want to edit individual OBO stanzas by hand - use obo-grep/obo-checkout tools instead
- You need programmatic ontology access from Python - use oaklib instead

## Installation & Setup

ROBOT requires Java 8+. Install via:

```bash
# Download latest
curl -L https://github.com/ontodev/robot/releases/latest/download/robot.jar -o robot.jar
curl -L https://raw.githubusercontent.com/ontodev/robot/master/bin/robot -o robot
chmod +x robot
```

For large ontologies, increase Java memory:

```bash
export ROBOT_JAVA_ARGS="-Xmx8G"
```

Verify installation:

```bash
robot --version
```

## Command Quick Reference

Every ROBOT command with a one-line description and key example. For full details on any command, read the corresponding file in `docs/` within this skill directory.

### Core Ontology Operations

| Command | Description | Key Example |
|---------|-------------|-------------|
| `merge` | Combine multiple ontologies | `robot merge --input a.owl --input b.owl --output merged.owl` |
| `reason` | Run reasoner, assert inferred axioms | `robot reason --reasoner ELK --input edit.owl --output reasoned.owl` |
| `relax` | Convert EquivalentClass to SubClassOf | `robot reason ... relax --output relaxed.owl` |
| `reduce` | Remove redundant SubClassOf axioms | `robot reason ... relax reduce --output reduced.owl` |
| `materialize` | Assert inferred superclass expressions | `robot materialize --reasoner ELK --input edit.owl --output mat.owl` |
| `unmerge` | Remove axioms of one ontology from another | `robot unmerge --input merged.owl --input remove.owl --output result.owl` |

### Extracting and Filtering

| Command | Description | Key Example |
|---------|-------------|-------------|
| `extract` | Extract module from ontology | `robot extract --method BOT --input ont.owl --term GO:0005634 --output module.owl` |
| `filter` | Keep only matching axioms | `robot filter --input ont.owl --term UBERON:0000955 --select "self ancestors" --output filtered.owl` |
| `remove` | Remove matching axioms | `robot remove --input ont.owl --select "imports" --output no-imports.owl` |

### Creating and Editing

| Command | Description | Key Example |
|---------|-------------|-------------|
| `template` | Generate OWL from TSV/CSV templates | `robot template --input ont.owl --template terms.tsv --output new-terms.owl` |
| `annotate` | Add ontology-level metadata | `robot annotate --input ont.owl --ontology-iri "http://purl.obolibrary.org/obo/my.owl" --output annotated.owl` |
| `rename` | Rename entity IRIs | `robot rename --input ont.owl --mappings mappings.tsv --output renamed.owl` |
| `expand` | Expand shortcut macros | `robot expand --input ont.owl --output expanded.owl` |
| `repair` | Fix deprecated class references | `robot repair --input ont.owl --output repaired.owl` |
| `collapse` | Collapse import hierarchy | `robot collapse --input ont.owl --output collapsed.owl` |

### Quality Control

| Command | Description | Key Example |
|---------|-------------|-------------|
| `report` | QC report with built-in checks | `robot report --input ont.owl --output report.tsv` |
| `verify` | Check SPARQL-based rules | `robot verify --input ont.owl --queries rules/*.sparql` |
| `validate-profile` | Validate OWL profile compliance | `robot validate-profile --input ont.owl --profile EL --output violations.tsv` |

### Querying and Exporting

| Command | Description | Key Example |
|---------|-------------|-------------|
| `query` | Run SPARQL queries | `robot query --input ont.owl --query q.sparql results.csv` |
| `export` | Export entities as table | `robot export --input ont.owl --header "ID\|LABEL\|SubClass Of" --export terms.csv` |
| `diff` | Compare two ontologies | `robot diff --left v1.owl --right v2.owl --output changes.md` |
| `measure` | Ontology metrics | `robot measure --input ont.owl --output metrics.tsv` |

### Debugging

| Command | Description | Key Example |
|---------|-------------|-------------|
| `explain` | Explain inferred axioms | `robot explain --input ont.owl --reasoner ELK --axiom "'eye' SubClassOf 'organ'" --explanation result.md` |

### Other

| Command | Description | Key Example |
|---------|-------------|-------------|
| `convert` | Convert between formats | `robot convert --input ont.owl --format obo --output ont.obo` |
| `mirror` | Download imported ontologies | `robot mirror --input ont.owl --directory mirror/ --output catalog.xml` |

## Deep Dive: Reasoning

Reasoning is the most critical ROBOT operation. It validates logical consistency and infers new axioms from existing definitions.

### Reasoner Choice

| Reasoner | Speed | Expressivity | When to Use |
|----------|-------|-------------|-------------|
| **ELK** | Fast | EL++ (no negation/disjunction) | Default for most OBO ontologies |
| **HermiT** | Slow | Full OWL DL | When ELK misses inferences or you need full DL |
| **Whelk** | Fast | EL++ | Alternative to ELK, Scala-based |
| **Structural** | Very fast | None (syntactic only) | Quick checks, no reasoning |

Most OBO ontologies use ELK. Only use HermiT when you specifically need full OWL DL reasoning.

### Key Options

```bash
robot reason \
  --reasoner ELK \
  --equivalent-classes-allowed asserted-only \
  --exclude-tautologies structural \
  --input edit.owl \
  --output reasoned.owl
```

- `--equivalent-classes-allowed asserted-only` - Fail if reasoning produces unexpected equivalent class pairs (catches modeling errors)
- `--exclude-tautologies structural` - Skip trivially true axioms
- `--annotate-inferred-axioms true` - Mark inferred axioms with `is_inferred true` annotation
- `--exclude-duplicate-axioms true` - Skip axioms already in imports
- `--create-new-ontology true` - Put inferences in a separate ontology

### Debugging Unsatisfiable Classes with explain

When reasoning finds unsatisfiable classes (classes that cannot have any instances), use `explain` to generate human-readable markdown explanations:

```bash
robot merge --input ont.owl \
  explain \
    --reasoner ELK \
    -M unsatisfiability \
    --unsatisfiable all \
    --explanation unsats.md
```

This generates a markdown file showing the chain of axioms that leads to each unsatisfiability. This is invaluable for debugging.

You can also explain specific entailments:

```bash
robot explain --input ont.owl \
  --reasoner ELK \
  --axiom "'retina' SubClassOf 'part of' some 'eye'" \
  --explanation explanation.md
```

The `--axiom` uses Manchester OWL syntax. Use single quotes around class/property names that contain spaces.


## Deep Dive: Templates

ROBOT templates let you create OWL ontology content from TSV/CSV spreadsheets. This is the preferred way to manage large sets of terms that follow regular patterns, because domain experts can edit spreadsheets without learning OWL.

### Template File Structure

A ROBOT template is a TSV (or CSV) file with:

- **Row 1**: Human-readable column headers
- **Row 2**: ROBOT template strings (tell ROBOT how to convert each column to OWL)
- **Row 3+**: Data rows (one per term)

### Template String Reference

#### Identity and Type

| Template | Description | Example Value |
|----------|-------------|---------------|
| `ID` | Term IRI (CURIE) | `OBI:0000070` |
| `LABEL` | rdfs:label | `assay` |
| `TYPE` | rdf:type | `owl:Class` (default) |

#### Annotations

| Template | Description | Example Value |
|----------|-------------|---------------|
| `A <property>` | String annotation | `A rdfs:comment` |
| `AT <property>^^<datatype>` | Typed annotation | `AT rdfs:label^^xsd:string` |
| `AL <property>@<lang>` | Language-tagged annotation | `AL definition@en` |
| `AI <property>` | IRI annotation | `AI has curation status` |

#### Class Axioms

| Template | Description | Example Value |
|----------|-------------|---------------|
| `SC %` | SubClassOf (named class) | Parent CURIE in cell |
| `SC 'relation' some %` | SubClassOf (existential restriction) | Filler CURIE in cell |
| `EC %` | EquivalentClass expression | Manchester syntax |
| `DC %` | DisjointClass | Class CURIE |
| `C %` | Class expression (type set by CLASS_TYPE column) | Expression |
| `CLASS_TYPE` | Controls `C %` behavior: `subclass`, `equivalent`, or `disjoint` | `equivalent` |

#### Modifiers

| Modifier | Description | Example |
|----------|-------------|---------|
| `SPLIT=\|` | Split cell value on delimiter for multiple values | `A alternative label SPLIT=\|` |

### Real-World Template Example (OBI-style)

Here is a simplified template for defining assay types, based on patterns from the OBI ontology:

**assays.tsv:**

```
ontology ID	label	definition	parent class	has part	evaluant	associated axiom
ID	LABEL	AL definition@en	SC %	SC 'has part' some % SPLIT=|	SC ('has specified input' some (% and 'has role' some 'evaluant role'))	C %
OBI:0000070	assay	A planned process with the objective to produce information about a material entity.	OBI:0000011
OBI:0000716	ChIP-seq assay	An assay using chromatin immunoprecipitation followed by sequencing.	OBI:0000070	OBI:0000626
OBI:0000087	fluorescence microscopy assay	A light microscopy assay using specimen fluorescence.	OBI:0000070		'material entity' and ('has characteristic' some fluorescence)
```

Key patterns to notice:

- `SC %` for simple parent class
- `SC 'has part' some % SPLIT=|` for multiple parts separated by `|`
- `SC ('has specified input' some (% and 'has role' some 'evaluant role'))` for complex restrictions using Manchester syntax
- `C %` combined with `CLASS_TYPE` for flexible subclass/equivalent declarations
- Empty cells are skipped (no axiom generated)

### Template Build Integration

Templates are typically processed in a Makefile:

```makefile
# Generate OWL module from template
src/ontology/modules/%.owl: src/ontology/templates/%.tsv
	$(ROBOT) merge --input src/ontology/edit.owl \
	template --template $< \
	annotate --ontology-iri "http://purl.obolibrary.org/obo/ont/modules/$(notdir $@)" \
	--output $@
```

The `merge --input` before `template` is critical: it provides the base ontology so that CURIEs in the template can be resolved.

### Merging Strategies

- **No merge (default)**: Template result is a standalone ontology
- `--merge-before`: Merge template result into the input ontology immediately
- `--merge-after`: Keep template result separate, merge for subsequent chained commands

### Template Tips

- Use `SPLIT=|` when a cell needs multiple values (e.g., multiple synonyms, multiple parents)
- Manchester syntax in template cells must use single quotes around names with spaces: `'has part' some 'protein complex'`
- Use `--force true` during development to continue past errors
- Use `--errors errors.tsv` to capture template errors to a file
- The `>A`, `>AT`, `>AL`, `>AI` templates add axiom annotations to the preceding logical axiom

## Common Pipelines

### Release Pipeline

The standard OBO ontology release workflow:

```bash
robot merge --input src/ontology/edit.owl \
  reason --reasoner ELK \
    --equivalent-classes-allowed asserted-only \
    --exclude-tautologies structural \
  relax \
  reduce \
  annotate \
    --ontology-iri "http://purl.obolibrary.org/obo/ONT.owl" \
    --version-iri "http://purl.obolibrary.org/obo/ONT/releases/2024-01-01/ONT.owl" \
    --annotation owl:versionInfo "2024-01-01" \
  convert --format obo \
  --output ONT.obo
```

### Template Pipeline

Generate terms and merge into the ontology:

```bash
robot merge --input edit.owl \
  template --template new-terms.tsv \
  --merge-before \
  annotate --ontology-iri "http://example.org/ont.owl" \
  --output result.owl
```

### QC Pipeline

Run quality control before release:

```bash
robot report --input edit.owl \
  --fail-on ERROR \
  --output qc-report.tsv
```

Or with custom rules:

```bash
robot verify --input edit.owl \
  --queries src/sparql/qc-*.sparql \
  --output-dir reports/
```

### Module Extraction

Extract a focused module around specific terms:

```bash
robot extract --method BOT \
  --input large-ont.owl \
  --term-file my-terms.txt \
  --output module.owl
```

Extraction methods:
- **BOT** (most common): Includes superclasses and related axioms
- **TOP**: Includes subclasses
- **STAR**: Minimal module (seed + inter-relations)
- **MIREOT**: Preserves hierarchy, requires upper/lower terms
- **subset**: Just seed terms + relations between them


## Common Pitfalls

### Java Memory

Large ontologies (Uberon, GO, ChEBI) need more memory:

```bash
export ROBOT_JAVA_ARGS="-Xmx8G"    # 8 GB
export ROBOT_JAVA_ARGS="-Xmx16G"   # 16 GB for very large ontologies
```

Symptom: `java.lang.OutOfMemoryError: Java heap space`

### Reasoner Timeouts

If ELK is too slow, check for:
- Circular definitions
- Complex nested class expressions
- Large numbers of disjointness axioms

If HermiT hangs, try ELK (it handles most OBO use cases).

### OBO Format Conversion Issues

`robot convert --format obo` may fail with `--check true` (default). Common causes:
- Classes with multiple labels
- Untranslatable OWL axioms (GCIs, complex restrictions)

Fix with `--check false` or use `--clean-obo` options:

```bash
robot convert --format obo \
  --clean-obo drop-extra-labels drop-untranslatable-axioms \
  --output ont.obo
```

### Template Quoting

In TSV templates, be careful with:
- Tab characters (use actual tabs, not spaces)
- Manchester syntax quoting: use single quotes for names with spaces
- CURIE resolution: ensure all prefixes are defined (via `--prefix` or input ontology)

### Unsatisfiable Classes

If `reason` reports unsatisfiable classes:

1. First, generate explanations: `robot explain -M unsatisfiability --unsatisfiable all --explanation unsats.md`
2. Read the markdown - it shows the axiom chain causing each unsatisfiability
3. Common causes: incorrect disjointness axioms, wrong domain/range restrictions, conflicting definitions
4. Fix the source ontology and re-run reasoning

### Import Resolution

If ROBOT cannot find imported ontologies:

```bash
robot --catalog catalog-v001.xml merge --input edit.owl ...
```

The catalog XML maps import IRIs to local files.

## Chaining Commands

ROBOT's most powerful feature is command chaining. Instead of writing intermediate files:

```bash
# Without chaining (slow, creates temp files)
robot merge --input a.owl --input b.owl --output merged.owl
robot reason --input merged.owl --output reasoned.owl
robot convert --input reasoned.owl --format obo --output result.obo
```

Chain commands (fast, no intermediate files):

```bash
robot merge --input a.owl --input b.owl \
  reason --reasoner ELK \
  convert --format obo \
  --output result.obo
```

Only the first command needs `--input` and only the last needs `--output`. Each command passes its result to the next.

## Global Options

These apply to all commands:

```bash
# Custom prefixes
robot --prefix "MYONT: http://example.org/myont/" merge ...

# Import catalog
robot --catalog catalog-v001.xml merge ...

# Verbosity
robot -v merge ...     # WARN level
robot -vv merge ...    # INFO level
robot -vvv merge ...   # DEBUG level with stack traces

# Strict mode (fail on unparsed triples)
robot --strict merge ...
```

## Reference

For detailed documentation on every command option, read the files in the `docs/` subdirectory of this skill:

- `docs/reason.md` - Full reasoning documentation
- `docs/template.md` - Full template documentation
- `docs/explain.md` - Full explain documentation
- `docs/extract.md` - Module extraction methods
- `docs/report.md` - QC report configuration
- `docs/query.md` - SPARQL query execution
- `docs/chaining.md` - Command chaining details
- `docs/global.md` - Global options (prefixes, catalogs, Java)
- `docs/examples/` - Example ontology files, templates, and SPARQL queries
- `docs/report_queries/` - Built-in QC report query definitions
