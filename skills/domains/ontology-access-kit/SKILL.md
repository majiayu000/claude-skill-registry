---
name: ontology-access-kit
description: Skills for querying ontologies using the Ontology Access Kit (OAK). This should only be used for complex ontology operations, for basic external ontology searching use the OLS MCP
---

# OAK Guide

## Overview

OAK is a powerful command line library for accessing ontologies. It can be installed via:

- `uv add oaklib`
- `pip install oaklib`

The main command is `runoak`

## When to use

OAK is generally to be used for more complex operations.

- if you want to do basic search over external ontologies, you should favor the OLS MCP over OAK
- if you are working with local obo files, then hacky obo tools like `obo-grep.pl` may be better

## Adapters

You typically want to use the sqlite adapter. This gives you fast access to any ontology in OBO, plus a number of other commonly used ontologies, found in semantic-sql.

Example:

`runoak -i sqlite:obo:cl COMMAND COMMAND-OPTS ARGS`

Note the `-i` comes (*before*) the command-specific opts

You can also access any ontology in OLS or BioPortal:

- `runoak -i bioportal:snomedct relationships SNOMEDCT:128351009`
- `runoak -i bioportal:efo tree -p i EFO:0004200`

But some OAK commands may not be implemented.

With OLS or BioPortal you can also do searches over all ontologies:

- `runoak -i bioportal: info l~NovaSeq`
- `runoak -i ols: info l~NovaSeq`

To work with local obo files:

- `runoak -i impleobo:my_ont.obo info MY:1234 -O obo`

## Common Operations

You can find a list of all commands with `runoak --help`. oak is highly fully featured, and you are encouraged to
explore to find the functionality you need. We provide some examples below.

We use `info` for many examples, but note that many options and arguments work across different commands

* Lookup
   * By exact label: `runoak -i sqlite:obo:cl info neuron` (returns `CL:0000540 ! neuron`)
   * By exact label (multiple): `runoak -i sqlite:obo:uberon info finger toe`
   * Search (any match): `runoak -i sqlite:obo:cl info  'l~T cell'`
   * Search (starts with): `runoak -i sqlite:obo:cl info l^neuron`
* Fetching detailed info
   * OBO format: `runoak -i sqlite:obo:cl info CL:0000540 -O obo`
   * relationships: `runoak -i sqlite:obo:cl  relationships --direction both CL:0000540`
   * mappings: `runoak -i sqlite:obo:mondo mappings 'Marfan syndrome'`
   * tree (is-a only): `runoak -i sqlite:obo:cl tree -p i CL:0000540`
   * metadata: `runoak -i sqlite:obo:chebi term-metdata CHEBI:35235`
* Complex queries
   * subclasses: `runoak -i sqlite:obo:cl info .sub CL:0000540 | head`
   * disjunctions (OR): `runoak -i sqlite:obo:cl info .sub neuron .sub 'T cell' | tail`
   * conjunctions: `runoak -i sqlite:obo:cl info .sub neuron .and .desc//p=i,p forebrain` (neurons and is-a/part-of the forebrain)
   * minus: `runoak -i sqlite:obo:cl info .sub neuron .minus .desc//p=i,p forebrain` (neurons and NOT is-a/part-of the forebrain)
* Visualization
   * `cl viz -p i,p,RO:0002215 'dopaminergic neuron' -o /tmp/dn.png` - subgraph from a CL term.
   * note that graphviz requires installing og2dot   
* Subsets
   * list subsets: `runoak -i sqlite:obo:go subsets` - list all subsets (goslim_prokaryote etc)
   * terms in subsets: `runoak -i sqlite:obo:go info .in goslim_generic` - all terms in a subset
   * terms in subsets: `runoak -i sqlite:obo:go info .in goslim_generic .minus .in goslim_prokaryote` - all terms in a subset not in another
* Other
   * `runoak lexmatch --help` for aligning ontologies
   * `runoak statistics --help` for summary stats
## Common Options and Idioms

### Graphs

OAK is very graph oriented, following ontologies like GO, CL

Typically for graph operations you want to operate over only is-a and part-of, so use `-p i,p`

You can also specify RO/BFO ids.

E.g.

```bash
runoak -i sqlite:obo:ro info 'capable of'
RO:0002215 ! capable of
```

```bash
cl relationships -p RO:0002215 'dopaminergic neuron'
subject	predicate	object	subject_label	predicate_label	object_label
CL:0000700	RO:0002215	GO:0061527	dopaminergic neuron	capable of	dopamine secretion, neurotransmission
```

