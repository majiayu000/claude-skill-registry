---
name: sparql-university
description: Guidance for writing and verifying SPARQL queries against RDF datasets, particularly university/academic ontologies. This skill should be used when tasks involve querying RDF data with SPARQL, working with academic datasets (students, professors, departments, courses), or performing complex graph pattern matching with filters and aggregations.
---

# SPARQL University Query Tasks

## Overview

This skill provides structured approaches for writing SPARQL queries against RDF datasets, with emphasis on university/academic ontologies. It covers ontology analysis, query construction, verification strategies, and common pitfalls to avoid.

## Workflow

### Step 1: Analyze the Ontology Structure

Before writing any query, thoroughly understand the RDF schema:

1. **Identify relevant classes** - Determine which classes represent the entities in the query (e.g., `uni:Person`, `uni:Department`, `uni:Course`, `uni:Student`)
2. **Map predicates** - Find predicates connecting entities:
   - Person → Department relationships (e.g., `uni:worksIn`)
   - Person → Role relationships (e.g., `uni:hasRole`)
   - Student → Course relationships (e.g., `uni:enrolledIn`)
   - Course → Department relationships (e.g., `uni:offeredBy`)
3. **Understand data types** - Check for string patterns, date formats, country codes
4. **Examine sample data** - Query a few instances to verify assumptions about the data structure

### Step 2: Decompose Complex Requirements

Break down multi-condition queries into discrete logical components:

1. **Entity identification** - Define criteria for selecting primary entities (e.g., "Full Professor" means roles starting with "Professor of" but excluding "Assistant Professor")
2. **Relationship filtering** - Specify how entities connect across the graph
3. **Aggregation logic** - Define grouping and counting requirements
4. **Temporal conditions** - Handle date-based filters (e.g., "currently enrolled" means no graduation date OR graduation date in the future)
5. **Geographic/categorical filters** - Prepare explicit value lists (e.g., EU-27 country codes)

### Step 3: Construct the Query Incrementally

Build queries layer by layer, testing each component:

```sparql
# Start with basic pattern matching
SELECT ?entity WHERE {
  ?entity rdf:type uni:Person .
  ?entity uni:hasRole ?role .
}

# Add role filtering
FILTER(STRSTARTS(?role, "Professor of") && !STRSTARTS(?role, "Assistant Professor"))

# Add subquery or EXISTS clause for complex conditions
FILTER EXISTS {
  # Nested pattern for conditional logic
}
```

**Key query patterns:**

- Use `STRSTARTS()` or `CONTAINS()` for string matching on roles/titles
- Use `FILTER EXISTS { }` for conditional relationship requirements
- Use `COUNT(DISTINCT ?var)` when entities may appear multiple times
- Use `GROUP BY` with `HAVING` for aggregate conditions
- Use `IN (...)` for explicit value lists (e.g., country codes)

### Step 4: Verify the Query

**Critical: Always verify file contents after writing.**

1. **Read back the written file** - After using Write tool, immediately Read the file to confirm complete content
2. **Check for truncation** - Verify closing brackets, complete filter lists, and proper termination
3. **Validate syntax** - Install and use `rdflib` or another SPARQL parser to check syntax before execution:

```python
from rdflib import Graph
g = Graph()
g.parse("data.ttl", format="turtle")
results = g.query(open("solution.sparql").read())
```

4. **Verify results against expectations** - Cross-check output against known test cases or sample data

### Step 5: Handle Result Interpretation

Understand what the query returns vs. what qualifies entities:

- A professor qualifies based on meeting criteria in ONE department
- The query returns ALL associated data (e.g., all countries where they work)
- Non-qualifying values in output (e.g., non-EU countries) appear because the entity qualified through other relationships

## Common Pitfalls

### File Writing Issues

- **Truncated writes** - Long FILTER IN clauses with many values (e.g., country codes) may appear truncated in tool output. Always read the file back to verify.
- **Incomplete syntax** - Missing closing parentheses, brackets, or GROUP BY clauses cause silent failures

### Logic Errors

- **Role matching** - "Full Professor" typically excludes "Assistant Professor" - use compound string conditions
- **Date handling** - "Currently enrolled" usually means either no end date OR end date >= reference date
- **Distinct counting** - Students enrolled in multiple courses in one department should count once per department

### Query Structure

- **EXISTS vs. direct pattern** - Use EXISTS when the condition determines qualification but shouldn't affect output structure
- **Subquery placement** - COUNT aggregations often require subqueries to avoid GROUP BY complications
- **Variable scope** - Variables in EXISTS clauses don't bind to outer query

## Verification Checklist

Before submitting any SPARQL solution:

- [ ] Read the solution file back to verify complete content
- [ ] Verify all closing brackets and parentheses are present
- [ ] Confirm filter value lists are complete (especially long lists like country codes)
- [ ] Test syntax with an RDF library (rdflib, Apache Jena)
- [ ] Verify results match expected output format
- [ ] Confirm edge cases are handled (null values, multiple relationships)

## Resources

See `references/sparql_patterns.md` for common SPARQL patterns and syntax examples.
