---
name: rdf-ontologies
description: "Master RDF ontologies and Turtle (TTL) syntax. Use for creating feature specifications, domain models, architecture plans with semantic web standards. Covers: Turtle syntax, SPARQL queries, Oxigraph RDF store, SHACL validation, .specify/ workflow. When designing features, modeling domains, writing specifications, or querying RDF data."
allowed_tools: "Read, Write, Edit, Glob, Grep, Bash(cargo make speckit:*)"
---

# RDF Ontologies Skill

## What is RDF?

**Resource Description Framework**: Semantic web standard for expressing knowledge as triples

```
Subject → Predicate → Object
  (noun)  (relation)  (value)

Example:
Alice → hasEmail → alice@example.com
Feature-001 → hasTitle → "Test Audit"
User → createdAt → 2025-12-28
```

## Turtle (TTL) Syntax

**Turtle**: Human-readable RDF syntax

### Basic Triple

```turtle
@prefix ex: <http://example.com/> .

ex:alice ex:email "alice@example.com" .
```

Reads: "alice has email alice@example.com"

### Multiple Statements About Same Subject

```turtle
@prefix ex: <http://example.com/> .

ex:alice
    ex:name "Alice" ;
    ex:email "alice@example.com" ;
    ex:age 30 .
```

### Collections (Lists)

```turtle
ex:team
    ex:members (
        ex:alice
        ex:bob
        ex:charlie
    ) .
```

### Classes and Types

```turtle
ex:alice rdf:type ex:Person .

# Or shorthand:
ex:alice a ex:Person .
```

### Subclass Relationships

```turtle
ex:Employee rdfs:subClassOf ex:Person .
```

### Property Relationships

```turtle
ex:email rdfs:domain ex:Person ;
         rdfs:range xsd:string .
```

## Prefixes and Namespaces

Always declare prefixes at start:

```turtle
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix ex: <http://example.com/> .
@prefix spec: <http://ggen.io/spec/> .

# Now use: spec:feature-001, ex:alice, etc.
```

**Common Namespaces**:
- `rdf:` - RDF core vocabulary
- `rdfs:` - RDF Schema (classes, properties)
- `xsd:` - XML Schema (datatypes)
- `spec:` - ggen specification vocabulary

## ggen Specification Vocabulary

### Features

```turtle
spec:feature-004 a spec:Feature ;
    spec:number "004" ;
    spec:title "Test Audit & Performance" ;
    spec:priority spec:P1 ;
    spec:description "Improve test quality" ;
    spec:businessValue "Catch more bugs early" ;
    spec:hasUserStory spec:us-001, spec:us-002 ;
    spec:status spec:Approved .
```

### User Stories

```turtle
spec:us-001 a spec:UserStory ;
    spec:title "Run mutation tests" ;
    spec:asA "developer" ;
    spec:iWant "to run mutation tests" ;
    spec:soThat "I know my tests are strong" ;
    spec:priority spec:P1 ;
    spec:estimatedHours 8 ;
    spec:hasAcceptanceCriterion spec:ac-001, spec:ac-002 .
```

### Acceptance Criteria

```turtle
spec:ac-001 a spec:AcceptanceCriterion ;
    spec:text "When running cargo make test-audit mutations" ;
    spec:expected "Mutation score > 90%" ;
    spec:verified true ;
    spec:verificationDate "2025-12-28"^^xsd:date .
```

### Requirements

```turtle
spec:req-001 a spec:Requirement ;
    spec:title "Zero unwrap in production" ;
    spec:category spec:CodeQuality ;
    spec:priority spec:P1 ;
    spec:status spec:Implemented ;
    spec:relatedUserStory spec:us-001 .
```

### Design Decisions

```turtle
spec:dd-001 a spec:DesignDecision ;
    spec:title "Use Tokio for async runtime" ;
    spec:rationale "Multi-threaded runtime needed for parallelism" ;
    spec:alternatives spec:dd-001-alt-1, spec:dd-001-alt-2 ;
    spec:consequence "Adds tokio dependency" ;
    spec:decisionDate "2025-01-15"^^xsd:date ;
    spec:decidedBy spec:team-architect .
```

### Tasks

```turtle
spec:task-001 a spec:Task ;
    spec:title "Design RDF ontology" ;
    spec:description "Create feature.ttl with user stories" ;
    spec:linkedUserStory spec:us-001 ;
    spec:linkedRequirement spec:req-001 ;
    spec:estimatedHours 4 ;
    spec:dependsOn [] ;  # No dependencies
    spec:assignedTo spec:engineer-1 ;
    spec:status spec:InProgress ;
    spec:completionDate "2025-12-29"^^xsd:date .
```

## SHACL Validation

**SHACL**: Shapes Constraint Language - validates RDF data

### Shape Definition

```turtle
spec:UserStoryShape a sh:NodeShape ;
    sh:targetClass spec:UserStory ;
    sh:property [
        sh:path spec:title ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:datatype xsd:string
    ] ;
    sh:property [
        sh:path spec:priority ;
        sh:in (spec:P1 spec:P2 spec:P3) ;
        sh:minCount 1
    ] ;
    sh:property [
        sh:path spec:hasAcceptanceCriterion ;
        sh:minCount 1 ;
        sh:class spec:AcceptanceCriterion
    ] .
```

### Validation Rules (ggen)

All feature specifications must satisfy:

```
✓ Priority: P1, P2, or P3 (NOT "HIGH", "LOW")
✓ Title: Present and descriptive
✓ Description: Clear purpose and context
✓ AcceptanceCriteria: Minimum 1 per user story
✓ RDF Syntax: Valid Turtle
✓ References: All linked resources exist
```

## SPARQL Queries

**SPARQL**: Query language for RDF

### Simple Query: Find All Features

```sparql
PREFIX spec: <http://ggen.io/spec/>

SELECT ?feature ?title ?priority
WHERE {
    ?feature a spec:Feature ;
             spec:title ?title ;
             spec:priority ?priority .
}
ORDER BY ?priority
```

### Query: Find Features by Priority

```sparql
PREFIX spec: <http://ggen.io/spec/>

SELECT ?feature ?title
WHERE {
    ?feature a spec:Feature ;
             spec:title ?title ;
             spec:priority spec:P1 .
}
```

### Query: Find User Stories in Feature

```sparql
PREFIX spec: <http://ggen.io/spec/>

SELECT ?story ?title ?acceptance
WHERE {
    spec:feature-004 spec:hasUserStory ?story .
    ?story spec:title ?title ;
           spec:hasAcceptanceCriterion ?acceptance .
    ?acceptance spec:text ?text .
}
```

### Query: Find Tasks by Status

```sparql
PREFIX spec: <http://ggen.io/spec/>

SELECT ?task ?title ?status
WHERE {
    ?task a spec:Task ;
          spec:title ?title ;
          spec:status ?status .
    FILTER (?status = spec:InProgress)
}
```

## Oxigraph RDF Store

**Oxigraph**: Fast RDF storage and SPARQL processor

### Load TTL File

```rust
use oxigraph::store::Store;
use oxigraph::io::RdfFormat;
use std::fs::File;

let store = Store::new().unwrap();
let file = File::open("feature.ttl").unwrap();
store.load_graph(file, RdfFormat::Turtle, None).unwrap();
```

### Execute SPARQL Query

```rust
let query_str = r#"
    PREFIX spec: <http://ggen.io/spec/>
    SELECT ?feature ?title WHERE {
        ?feature a spec:Feature ;
                 spec:title ?title .
    }
"#;

let mut results = store.query(query_str).unwrap();
for result in results {
    let row = result.unwrap();
    println!("{:?}", row);
}
```

## .specify/ Directory Workflow

### Create Feature Specification

```bash
# 1. Create directory
mkdir -p .specify/specs/004-test-audit

# 2. Create feature.ttl with user stories
touch .specify/specs/004-test-audit/feature.ttl

# 3. Add entities
touch .specify/specs/004-test-audit/entities.ttl

# 4. Add architecture plan
touch .specify/specs/004-test-audit/plan.ttl

# 5. Add task breakdown
touch .specify/specs/004-test-audit/tasks.ttl

# 6. Create evidence directory
mkdir -p .specify/specs/004-test-audit/evidence
```

### Validate Specifications

```bash
# Check TTL syntax
cargo make speckit-check

# Validate SHACL constraints
cargo make speckit-validate

# Regenerate markdown
cargo make speckit-render
```

### Generate Markdown from TTL

```bash
# Manual generation
ggen render .specify/templates/spec.tera \
    .specify/specs/004-test-audit/feature.ttl \
    > .specify/specs/004-test-audit/spec.md
```

**Important**: NEVER edit `.md` files manually. Always edit `.ttl`, then regenerate.

## Data Types

### XSD Datatypes

```turtle
spec:user
    spec:age "30"^^xsd:integer ;
    spec:salary "50000.00"^^xsd:decimal ;
    spec:active "true"^^xsd:boolean ;
    spec:created "2025-12-28"^^xsd:date ;
    spec:updated "2025-12-28T15:30:00Z"^^xsd:dateTime ;
    spec:email "user@example.com"^^xsd:string .
```

## Blank Nodes (Anonymous Resources)

```turtle
spec:task-001
    spec:dependency [
        spec:title "Review design" ;
        spec:priority spec:P1
    ] .
```

## Ontology Best Practices

1. **Consistent Naming**
   - Use lowercase with dashes: `spec:user-story`, `spec:design-decision`
   - Classes: PascalCase - `spec:UserStory`, `spec:DesignDecision`

2. **Declare Prefixes First**
   ```turtle
   @prefix spec: <http://ggen.io/spec/> .
   # Then use throughout
   ```

3. **Use Consistent Properties**
   - `a` for type (shorthand for `rdf:type`)
   - `rdfs:label` for human-readable name
   - `rdfs:comment` for description

4. **Link Related Resources**
   ```turtle
   spec:task-001 spec:linkedUserStory spec:us-001 .
   spec:us-001 spec:linkedRequirement spec:req-001 .
   ```

5. **Store Evidence**
   ```turtle
   spec:feature-004 spec:hasEvidence "evidence/test-results.json" .
   ```

## Common Patterns

### Class Hierarchy

```turtle
spec:Entity a rdfs:Class .

spec:Feature rdfs:subClassOf spec:Entity .
spec:Task rdfs:subClassOf spec:Entity .

spec:UserStory rdfs:subClassOf spec:Feature .
```

### Property Domain/Range

```turtle
spec:hasUserStory rdfs:domain spec:Feature ;
                  rdfs:range spec:UserStory .

spec:priority rdfs:domain spec:Feature, spec:UserStory, spec:Task ;
              rdfs:range spec:Priority .
```

### Relationships Between Entities

```turtle
spec:feature-004
    spec:hasUserStory spec:us-001, spec:us-002 ;
    spec:requiresComponent spec:ggen-test-audit ;
    spec:relatedTo spec:feature-003 .
```

## Troubleshooting

### Invalid Turtle Syntax

```bash
# Error: Unexpected character at line 5
# Solution: Check for missing dots, semicolons, commas
```

### SHACL Validation Failed

```bash
# Error: Priority must be P1, P2, P3
# Solution: Change priority value to valid enumeration
```

### Broken References

```bash
# Error: Reference to undefined resource
# Solution: Create missing resource or fix reference
```

## Success Criteria

✓ Valid Turtle syntax
✓ SHACL constraints satisfied
✓ Markdown generated successfully
✓ All references valid
✓ Evidence directory populated
✓ Ready for implementation

## See Also

- `reference.md` - Detailed Turtle syntax reference
- `examples.md` - Real-world ontology examples
- [W3C Turtle Specification](https://www.w3.org/TR/turtle/)
- [SPARQL Query Language](https://www.w3.org/TR/sparql11-query/)
- [Oxigraph Documentation](https://github.com/oxigraph/oxigraph)
