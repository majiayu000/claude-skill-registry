---
name: libgraph
description: >
  libgraph - RDF graph index using N3 library. GraphIndex stores and queries
  linked data triples. PREFIXES provides standard namespaces (schema, rdf, rdfs,
  foaf). parseTripleQuery parses subject-predicate-object patterns.
  serializeShacl generates SHACL constraints. Use for knowledge graphs, semantic
  queries, and linked data processing.
---

# libgraph Skill

## When to Use

- Building and querying knowledge graphs
- Storing RDF triples for semantic data
- Executing subject-predicate-object pattern queries
- Working with linked data and ontologies

## Key Concepts

**GraphIndex**: Storage-backed index for RDF triples with pattern-based
querying.

**PREFIXES**: Standard namespace prefixes for common vocabularies (schema.org,
RDF, RDFS, FOAF).

**Triple patterns**: Query graphs using subject-predicate-object patterns with
wildcards.

## Usage Patterns

### Pattern 1: Query graph triples

```javascript
import { createGraphIndex, PREFIXES } from "@copilot-ld/libgraph";

const index = await createGraphIndex(storage, "knowledge");
const results = await index.query(
  `${PREFIXES.schema}Person`,
  `${PREFIXES.schema}name`,
  "?",
);
```

### Pattern 2: Parse triple query string

```javascript
import { parseTripleQuery } from "@copilot-ld/libgraph";

const { subject, predicate, object } = parseTripleQuery("schema:Person ? ?");
```

## Integration

Used by Graph service for knowledge queries. Processes ontology.ttl files.
