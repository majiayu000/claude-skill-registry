---
name: lang-sparql-dev
description: Foundational SPARQL patterns covering RDF querying, triple patterns, graph patterns, and semantic web fundamentals. Use when querying RDF data or working with knowledge graphs. This is the entry point for SPARQL development.
---

# SPARQL Development Skill

Comprehensive foundational patterns for SPARQL (SPARQL Protocol and RDF Query Language), covering RDF fundamentals, query patterns, graph operations, and semantic web development.

## Table of Contents

- [RDF Fundamentals](#rdf-fundamentals)
- [Basic Query Patterns](#basic-query-patterns)
- [Graph Patterns](#graph-patterns)
- [Query Forms](#query-forms)
- [Solution Modifiers](#solution-modifiers)
- [Aggregations and Grouping](#aggregations-and-grouping)
- [Property Paths](#property-paths)
- [Federated Queries](#federated-queries)
- [Common Ontologies](#common-ontologies)
- [Best Practices](#best-practices)

## RDF Fundamentals

### Triple Structure

RDF data is represented as triples: Subject-Predicate-Object.

```sparql
# Basic triple pattern
<http://example.org/person/Alice>
    <http://xmlns.com/foaf/0.1/name>
    "Alice Smith" .

# Compact notation with prefixes
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX ex: <http://example.org/>

ex:person/Alice foaf:name "Alice Smith" .
```

### URI Types

```sparql
# Full URI
<http://example.org/resource/123>

# Prefixed name
PREFIX ex: <http://example.org/>
ex:resource/123

# Blank nodes (anonymous resources)
_:node1
[]

# Literals
"Plain string"
"String with language"@en
"42"^^xsd:integer
"2024-01-15"^^xsd:date
```

### Literal Types

```sparql
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

# String literals
"Simple string"
"String with language"@en
"Multi-line
string"

# Numeric literals
42
3.14
"100"^^xsd:integer
"99.99"^^xsd:decimal

# Boolean literals
true
false
"true"^^xsd:boolean

# Date/Time literals
"2024-01-15"^^xsd:date
"14:30:00"^^xsd:time
"2024-01-15T14:30:00Z"^^xsd:dateTime

# Other common types
"http://example.org"^^xsd:anyURI
"PT1H30M"^^xsd:duration
```

### RDF Graphs

```sparql
# Default graph (unnamed)
SELECT * WHERE {
    ?s ?p ?o .
}

# Named graphs
SELECT * WHERE {
    GRAPH <http://example.org/graph1> {
        ?s ?p ?o .
    }
}

# Query across multiple graphs
SELECT * WHERE {
    {
        GRAPH <http://example.org/graph1> {
            ?s ?p ?o .
        }
    }
    UNION
    {
        GRAPH <http://example.org/graph2> {
            ?s ?p ?o .
        }
    }
}

# Query from all graphs
SELECT * WHERE {
    GRAPH ?g {
        ?s ?p ?o .
    }
}
```

### RDF Collections

```sparql
# RDF Lists (linked list structure)
PREFIX ex: <http://example.org/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

ex:myList rdf:first "Item 1" ;
          rdf:rest [ rdf:first "Item 2" ;
                     rdf:rest [ rdf:first "Item 3" ;
                                rdf:rest rdf:nil ] ] .

# Shorthand syntax
ex:myList rdf:value ( "Item 1" "Item 2" "Item 3" ) .

# Querying lists
SELECT ?item WHERE {
    ?list rdf:rest*/rdf:first ?item .
}
```

## Basic Query Patterns

### SELECT Queries

```sparql
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

# Basic SELECT
SELECT ?name WHERE {
    ?person foaf:name ?name .
}

# Multiple variables
SELECT ?person ?name ?email WHERE {
    ?person foaf:name ?name ;
            foaf:mbox ?email .
}

# SELECT DISTINCT (remove duplicates)
SELECT DISTINCT ?type WHERE {
    ?s a ?type .
}

# SELECT * (all variables)
SELECT * WHERE {
    ?s ?p ?o .
}

# SELECT with expressions
SELECT ?person ?age (?age + 10 AS ?ageIn10Years) WHERE {
    ?person foaf:age ?age .
}
```

### WHERE Clause Patterns

```sparql
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX ex: <http://example.org/>

# Basic triple pattern
SELECT ?name WHERE {
    ex:Alice foaf:name ?name .
}

# Multiple triple patterns (implicit AND)
SELECT ?name ?email WHERE {
    ?person foaf:name ?name .
    ?person foaf:mbox ?email .
}

# Shorthand for same subject (semicolon)
SELECT ?name ?email WHERE {
    ?person foaf:name ?name ;
            foaf:mbox ?email .
}

# Shorthand for same subject and predicate (comma)
SELECT ?person ?friend WHERE {
    ?person foaf:name "Alice" ;
            foaf:knows ?friend1, ?friend2 .
}

# Nested patterns
SELECT ?person ?friendName WHERE {
    ?person foaf:name "Alice" .
    ?person foaf:knows ?friend .
    ?friend foaf:name ?friendName .
}
```

### Filtering Results

```sparql
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

# String filtering
SELECT ?person ?name WHERE {
    ?person foaf:name ?name .
    FILTER (regex(?name, "Smith", "i"))  # Case-insensitive
}

# Numeric filtering
SELECT ?person ?age WHERE {
    ?person foaf:age ?age .
    FILTER (?age >= 18 && ?age < 65)
}

# Type checking
SELECT ?person ?value WHERE {
    ?person foaf:name ?value .
    FILTER (isLiteral(?value))
}

# Language filtering
SELECT ?label WHERE {
    ?resource rdfs:label ?label .
    FILTER (lang(?label) = "en")
}

# Negation
SELECT ?person ?name WHERE {
    ?person foaf:name ?name .
    FILTER (!bound(?person))  # Where variable is not bound
}

# String functions in FILTER
SELECT ?name WHERE {
    ?person foaf:name ?name .
    FILTER (
        strlen(?name) > 5 &&
        contains(?name, "Smith") &&
        strstarts(?name, "J")
    )
}

# Date filtering
SELECT ?event ?date WHERE {
    ?event ex:eventDate ?date .
    FILTER (
        ?date >= "2024-01-01"^^xsd:date &&
        ?date < "2025-01-01"^^xsd:date
    )
}

# Multiple conditions
SELECT ?person WHERE {
    ?person foaf:age ?age ;
            foaf:name ?name .
    FILTER (
        (?age > 18 && ?age < 65) ||
        (regex(?name, "^Admin"))
    )
}
```

### Binding Values

```sparql
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

# BIND - assign values to variables
SELECT ?person ?name ?greeting WHERE {
    ?person foaf:name ?name .
    BIND (CONCAT("Hello, ", ?name) AS ?greeting)
}

# Multiple BIND statements
SELECT ?x ?squared ?cubed WHERE {
    VALUES ?x { 1 2 3 4 5 }
    BIND (?x * ?x AS ?squared)
    BIND (?x * ?x * ?x AS ?cubed)
}

# BIND with conditionals
SELECT ?person ?ageGroup WHERE {
    ?person foaf:age ?age .
    BIND (
        IF(?age < 18, "Minor",
        IF(?age < 65, "Adult", "Senior"))
        AS ?ageGroup
    )
}

# COALESCE - first non-null value
SELECT ?person ?contact WHERE {
    ?person foaf:mbox ?email .
    OPTIONAL { ?person foaf:phone ?phone }
    BIND (COALESCE(?phone, ?email) AS ?contact)
}
```

### VALUES Clause

```sparql
PREFIX ex: <http://example.org/>

# Inline data
SELECT ?person ?name WHERE {
    ?person ex:name ?name .
    VALUES ?person {
        ex:Alice
        ex:Bob
        ex:Charlie
    }
}

# Multiple variables
SELECT ?person ?age WHERE {
    VALUES (?person ?age) {
        (ex:Alice 30)
        (ex:Bob 25)
        (ex:Charlie 35)
    }
    ?person ex:name ?name .
}

# Mixing bound and unbound values
SELECT ?x ?y WHERE {
    VALUES (?x ?y) {
        (1 UNDEF)
        (2 3)
        (UNDEF 4)
    }
}
```

## Graph Patterns

### OPTIONAL Patterns

```sparql
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

# Basic OPTIONAL
SELECT ?person ?name ?email WHERE {
    ?person foaf:name ?name .
    OPTIONAL { ?person foaf:mbox ?email }
}

# Multiple OPTIONAL blocks
SELECT ?person ?name ?email ?phone WHERE {
    ?person foaf:name ?name .
    OPTIONAL { ?person foaf:mbox ?email }
    OPTIONAL { ?person foaf:phone ?phone }
}

# Nested OPTIONAL
SELECT ?person ?friend ?friendEmail WHERE {
    ?person foaf:name "Alice" .
    OPTIONAL {
        ?person foaf:knows ?friend .
        OPTIONAL { ?friend foaf:mbox ?friendEmail }
    }
}

# OPTIONAL with FILTER
SELECT ?person ?name ?age WHERE {
    ?person foaf:name ?name .
    OPTIONAL {
        ?person foaf:age ?age .
        FILTER (?age >= 18)
    }
}
```

### UNION Patterns

```sparql
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX vcard: <http://www.w3.org/2006/vcard/ns#>

# Basic UNION
SELECT ?name WHERE {
    {
        ?person foaf:name ?name .
    }
    UNION
    {
        ?person vcard:fn ?name .
    }
}

# Multiple UNIONs
SELECT ?contact WHERE {
    {
        ?person foaf:mbox ?contact .
    }
    UNION
    {
        ?person foaf:phone ?contact .
    }
    UNION
    {
        ?person vcard:email ?contact .
    }
}

# UNION with different patterns
SELECT ?person ?label WHERE {
    {
        ?person foaf:name ?label .
        ?person foaf:age ?age .
        FILTER (?age > 18)
    }
    UNION
    {
        ?person rdfs:label ?label .
        ?person a foaf:Organization .
    }
}
```

### MINUS Patterns

```sparql
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

# Exclude patterns
SELECT ?person ?name WHERE {
    ?person foaf:name ?name .
    MINUS {
        ?person foaf:mbox ?email .
    }
}

# Multiple MINUS
SELECT ?person WHERE {
    ?person a foaf:Person .
    MINUS { ?person foaf:age ?age }
    MINUS { ?person foaf:mbox ?email }
}

# MINUS vs OPTIONAL + FILTER NOT EXISTS
# These are similar but have subtle differences
SELECT ?person ?name WHERE {
    ?person foaf:name ?name .
    FILTER NOT EXISTS {
        ?person foaf:mbox ?email .
    }
}
```

### NOT EXISTS Patterns

```sparql
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

# Basic negation
SELECT ?person WHERE {
    ?person a foaf:Person .
    FILTER NOT EXISTS {
        ?person foaf:knows ?other .
    }
}

# Complex negation
SELECT ?person WHERE {
    ?person foaf:name ?name .
    FILTER NOT EXISTS {
        ?person foaf:knows ?friend .
        ?friend foaf:mbox ?email .
    }
}

# Combination with EXISTS
SELECT ?person WHERE {
    ?person a foaf:Person .
    FILTER EXISTS { ?person foaf:name ?name }
    FILTER NOT EXISTS { ?person foaf:mbox ?email }
}
```

### Graph Patterns

```sparql
PREFIX ex: <http://example.org/>

# Query specific named graph
SELECT ?s ?p ?o WHERE {
    GRAPH ex:graph1 {
        ?s ?p ?o .
    }
}

# Query variable graph
SELECT ?g ?s ?p WHERE {
    GRAPH ?g {
        ?s ?p ?o .
    }
}

# Combine default and named graphs
SELECT ?person ?name WHERE {
    # From default graph
    ?person a foaf:Person .

    # From named graph
    GRAPH ex:privateData {
        ?person foaf:name ?name .
    }
}

# Multiple graphs with UNION
SELECT ?s ?p ?o WHERE {
    {
        GRAPH ex:graph1 { ?s ?p ?o }
    }
    UNION
    {
        GRAPH ex:graph2 { ?s ?p ?o }
    }
}
```

### Subqueries

```sparql
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

# Basic subquery
SELECT ?person ?friendCount WHERE {
    ?person a foaf:Person .
    {
        SELECT ?person (COUNT(?friend) AS ?friendCount) WHERE {
            ?person foaf:knows ?friend .
        }
        GROUP BY ?person
    }
}

# Nested subqueries
SELECT ?person ?name ?avgFriendAge WHERE {
    ?person foaf:name ?name .
    {
        SELECT ?person (AVG(?friendAge) AS ?avgFriendAge) WHERE {
            ?person foaf:knows ?friend .
            ?friend foaf:age ?friendAge .
        }
        GROUP BY ?person
    }
}

# Subquery with LIMIT
SELECT ?person ?topFriend WHERE {
    ?person foaf:name ?name .
    {
        SELECT ?person ?topFriend WHERE {
            ?person foaf:knows ?topFriend .
            ?topFriend foaf:popularityScore ?score .
        }
        ORDER BY DESC(?score)
        LIMIT 1
    }
}
```

## Query Forms

### CONSTRUCT Queries

```sparql
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX vcard: <http://www.w3.org/2006/vcard/ns#>

# Basic CONSTRUCT - transform data
CONSTRUCT {
    ?person vcard:fn ?name .
    ?person vcard:email ?email .
} WHERE {
    ?person foaf:name ?name .
    OPTIONAL { ?person foaf:mbox ?email }
}

# CONSTRUCT with calculated values
CONSTRUCT {
    ?person ex:fullInfo ?info .
} WHERE {
    ?person foaf:name ?name ;
            foaf:age ?age .
    BIND (CONCAT(?name, " (", STR(?age), ")") AS ?info)
}

# CONSTRUCT with conditional patterns
CONSTRUCT {
    ?person a ex:Adult .
} WHERE {
    ?person foaf:age ?age .
    FILTER (?age >= 18)
}

# CONSTRUCT with multiple patterns
CONSTRUCT {
    ?person a ex:SocialPerson ;
            ex:friendCount ?count ;
            ex:hasFriend ?friend .
} WHERE {
    ?person foaf:knows ?friend .
    {
        SELECT ?person (COUNT(?f) AS ?count) WHERE {
            ?person foaf:knows ?f .
        }
        GROUP BY ?person
    }
}

# Empty CONSTRUCT template (copy all matching triples)
CONSTRUCT WHERE {
    ?s ?p ?o .
    FILTER (?p = foaf:knows)
}
```

### DESCRIBE Queries

```sparql
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX ex: <http://example.org/>

# DESCRIBE specific resource
DESCRIBE ex:Alice

# DESCRIBE with variables
DESCRIBE ?person WHERE {
    ?person foaf:name "Alice Smith" .
}

# DESCRIBE multiple resources
DESCRIBE ex:Alice ex:Bob ex:Charlie

# DESCRIBE with pattern
DESCRIBE ?person ?friend WHERE {
    ?person foaf:name "Alice" .
    ?person foaf:knows ?friend .
}

# DESCRIBE all resources of a type
DESCRIBE ?person WHERE {
    ?person a foaf:Person .
}
LIMIT 10
```

### ASK Queries

```sparql
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX ex: <http://example.org/>

# Basic ASK - check existence
ASK {
    ex:Alice foaf:knows ex:Bob .
}

# ASK with complex pattern
ASK {
    ?person foaf:name "Alice" ;
            foaf:age ?age .
    FILTER (?age >= 18)
}

# ASK with OPTIONAL
ASK {
    ex:Alice foaf:name ?name .
    OPTIONAL { ex:Alice foaf:mbox ?email }
}

# ASK with negation
ASK {
    ex:Alice a foaf:Person .
    FILTER NOT EXISTS {
        ex:Alice foaf:mbox ?email .
    }
}
```

## Solution Modifiers

### ORDER BY

```sparql
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

# Ascending order (default)
SELECT ?person ?age WHERE {
    ?person foaf:age ?age .
}
ORDER BY ?age

# Descending order
SELECT ?person ?age WHERE {
    ?person foaf:age ?age .
}
ORDER BY DESC(?age)

# Multiple sort keys
SELECT ?person ?lastName ?firstName WHERE {
    ?person foaf:lastName ?lastName ;
            foaf:firstName ?firstName .
}
ORDER BY ?lastName ?firstName

# Mixed sort directions
SELECT ?person ?age ?name WHERE {
    ?person foaf:age ?age ;
            foaf:name ?name .
}
ORDER BY DESC(?age) ASC(?name)

# ORDER BY with expressions
SELECT ?person ?name ?age WHERE {
    ?person foaf:name ?name ;
            foaf:age ?age .
}
ORDER BY (strlen(?name)) DESC(?age)
```

### LIMIT and OFFSET

```sparql
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

# LIMIT - restrict number of results
SELECT ?person ?name WHERE {
    ?person foaf:name ?name .
}
LIMIT 10

# OFFSET - skip first N results
SELECT ?person ?name WHERE {
    ?person foaf:name ?name .
}
OFFSET 20

# Pagination with LIMIT and OFFSET
SELECT ?person ?name WHERE {
    ?person foaf:name ?name .
}
ORDER BY ?name
LIMIT 10
OFFSET 20  # Page 3 (skip first 20, show next 10)

# LIMIT with ORDER BY
SELECT ?person ?age WHERE {
    ?person foaf:age ?age .
}
ORDER BY DESC(?age)
LIMIT 5  # Top 5 oldest people
```

### DISTINCT and REDUCED

```sparql
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

# DISTINCT - remove duplicates
SELECT DISTINCT ?type WHERE {
    ?s a ?type .
}

# REDUCED - allow duplicates but permit elimination
# (useful for performance optimization)
SELECT REDUCED ?type WHERE {
    ?s a ?type .
}

# DISTINCT with multiple variables
SELECT DISTINCT ?person ?type WHERE {
    ?person a ?type .
}
```

### Projection

```sparql
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

# Project specific variables
SELECT ?name ?age WHERE {
    ?person foaf:name ?name ;
            foaf:age ?age ;
            foaf:mbox ?email .  # Not projected
}

# Project all variables
SELECT * WHERE {
    ?person foaf:name ?name ;
            foaf:age ?age .
}

# Project with expressions
SELECT ?person (?age + 1 AS ?nextAge) WHERE {
    ?person foaf:age ?age .
}

# Conditional projection
SELECT ?person
       (IF(?age >= 18, "Adult", "Minor") AS ?ageGroup)
WHERE {
    ?person foaf:age ?age .
}
```

## Aggregations and Grouping

### COUNT Aggregation

```sparql
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

# Count all results
SELECT (COUNT(*) AS ?total) WHERE {
    ?s a foaf:Person .
}

# Count specific variable
SELECT (COUNT(?friend) AS ?friendCount) WHERE {
    ex:Alice foaf:knows ?friend .
}

# Count distinct values
SELECT (COUNT(DISTINCT ?type) AS ?typeCount) WHERE {
    ?s a ?type .
}

# Count with GROUP BY
SELECT ?person (COUNT(?friend) AS ?friendCount) WHERE {
    ?person foaf:knows ?friend .
}
GROUP BY ?person

# Count with HAVING
SELECT ?person (COUNT(?friend) AS ?friendCount) WHERE {
    ?person foaf:knows ?friend .
}
GROUP BY ?person
HAVING (COUNT(?friend) > 5)
```

### Other Aggregations

```sparql
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX ex: <http://example.org/>

# SUM
SELECT ?department (SUM(?salary) AS ?totalSalary) WHERE {
    ?person ex:department ?department ;
            ex:salary ?salary .
}
GROUP BY ?department

# AVG
SELECT ?department (AVG(?salary) AS ?avgSalary) WHERE {
    ?person ex:department ?department ;
            ex:salary ?salary .
}
GROUP BY ?department

# MIN and MAX
SELECT ?department
       (MIN(?salary) AS ?minSalary)
       (MAX(?salary) AS ?maxSalary)
WHERE {
    ?person ex:department ?department ;
            ex:salary ?salary .
}
GROUP BY ?department

# Multiple aggregations
SELECT ?person
       (COUNT(?friend) AS ?friendCount)
       (AVG(?friendAge) AS ?avgFriendAge)
       (MIN(?friendAge) AS ?youngestFriend)
       (MAX(?friendAge) AS ?oldestFriend)
WHERE {
    ?person foaf:knows ?friend .
    ?friend foaf:age ?friendAge .
}
GROUP BY ?person

# SAMPLE - arbitrary value from group
SELECT ?type (SAMPLE(?s) AS ?example) WHERE {
    ?s a ?type .
}
GROUP BY ?type

# GROUP_CONCAT - concatenate values
SELECT ?person
       (GROUP_CONCAT(?friendName; separator=", ") AS ?friends)
WHERE {
    ?person foaf:knows ?friend .
    ?friend foaf:name ?friendName .
}
GROUP BY ?person
```

### GROUP BY Clause

```sparql
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX ex: <http://example.org/>

# Basic GROUP BY
SELECT ?type (COUNT(?s) AS ?count) WHERE {
    ?s a ?type .
}
GROUP BY ?type

# Multiple grouping variables
SELECT ?department ?location (COUNT(?person) AS ?count) WHERE {
    ?person ex:department ?department ;
            ex:location ?location .
}
GROUP BY ?department ?location

# GROUP BY with expressions
SELECT (FLOOR(?age/10) AS ?ageDecade) (COUNT(?person) AS ?count) WHERE {
    ?person foaf:age ?age .
}
GROUP BY (FLOOR(?age/10))

# Nested aggregations require subqueries
SELECT ?person ?name ?friendCount WHERE {
    ?person foaf:name ?name .
    {
        SELECT ?person (COUNT(?friend) AS ?friendCount) WHERE {
            ?person foaf:knows ?friend .
        }
        GROUP BY ?person
    }
}
ORDER BY DESC(?friendCount)
```

### HAVING Clause

```sparql
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX ex: <http://example.org/>

# Filter groups by aggregate value
SELECT ?person (COUNT(?friend) AS ?friendCount) WHERE {
    ?person foaf:knows ?friend .
}
GROUP BY ?person
HAVING (COUNT(?friend) > 5)

# Multiple HAVING conditions
SELECT ?department
       (COUNT(?person) AS ?count)
       (AVG(?salary) AS ?avgSalary)
WHERE {
    ?person ex:department ?department ;
            ex:salary ?salary .
}
GROUP BY ?department
HAVING (COUNT(?person) > 10 && AVG(?salary) > 50000)

# HAVING with bound variables
SELECT ?person (COUNT(?friend) AS ?friendCount) WHERE {
    ?person foaf:knows ?friend ;
            foaf:age ?age .
}
GROUP BY ?person
HAVING (COUNT(?friend) > 3 && ?age < 30)
```

## Property Paths

### Basic Property Paths

```sparql
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX ex: <http://example.org/>

# Zero or more (*)
SELECT ?person ?ancestor WHERE {
    ?person ex:hasParent* ?ancestor .
}

# One or more (+)
SELECT ?person ?descendant WHERE {
    ?person ex:hasChild+ ?descendant .
}

# Zero or one (?)
SELECT ?person ?contact WHERE {
    ?person ex:primaryContact? ?contact .
}

# Exact number {n}
SELECT ?person ?relative WHERE {
    ?person ex:hasParent{2} ?relative .  # Grandparents
}

# Range {n,m}
SELECT ?person ?ancestor WHERE {
    ?person ex:hasParent{1,3} ?ancestor .  # Parents, grandparents, great-grandparents
}

# At least n {n,}
SELECT ?person ?ancestor WHERE {
    ?person ex:hasParent{2,} ?ancestor .  # Grandparents and beyond
}
```

### Path Alternatives

```sparql
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX vcard: <http://www.w3.org/2006/vcard/ns#>

# Alternative paths (|)
SELECT ?person ?name WHERE {
    ?person foaf:name|vcard:fn ?name .
}

# Complex alternatives
SELECT ?person ?contact WHERE {
    ?person foaf:mbox|foaf:phone|vcard:email ?contact .
}

# Alternatives with paths
SELECT ?person ?relative WHERE {
    ?person (ex:hasParent|ex:hasChild)+ ?relative .
}
```

### Path Sequences

```sparql
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX ex: <http://example.org/>

# Sequence (/)
SELECT ?person ?friendOfFriend WHERE {
    ?person foaf:knows/foaf:knows ?friendOfFriend .
    FILTER (?person != ?friendOfFriend)
}

# Longer sequences
SELECT ?person ?greatGrandparent WHERE {
    ?person ex:hasParent/ex:hasParent/ex:hasParent ?greatGrandparent .
}

# Mixed sequences and alternatives
SELECT ?person ?contact WHERE {
    ?person foaf:knows/foaf:mbox|foaf:phone ?contact .
}

# Sequences with repetition
SELECT ?person ?colleague WHERE {
    ?person (ex:worksFor/ex:employs)+ ?colleague .
}
```

### Inverse Paths

```sparql
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX ex: <http://example.org/>

# Inverse path (^)
SELECT ?child ?parent WHERE {
    ?child ^ex:hasChild ?parent .
    # Equivalent to: ?parent ex:hasChild ?child .
}

# Inverse with repetition
SELECT ?person ?descendant WHERE {
    ?person ^ex:hasParent+ ?descendant .
}

# Complex inverse paths
SELECT ?person ?manager WHERE {
    ?person ^ex:manages/ex:worksFor ?manager .
}
```

### Negated Property Paths

```sparql
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ex: <http://example.org/>

# Negated property set (!)
SELECT ?s ?o WHERE {
    ?s !rdf:type ?o .  # Any property except rdf:type
}

# Negated alternative
SELECT ?person ?value WHERE {
    ?person !(foaf:name|foaf:mbox) ?value .
}

# Negated in path
SELECT ?person ?other WHERE {
    ?person !foaf:knows/foaf:name ?other .
}
```

### Complex Property Path Examples

```sparql
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX ex: <http://example.org/>

# Social network exploration
SELECT ?person ?distance ?connection WHERE {
    ex:Alice (foaf:knows+) ?connection .
    BIND (strlen(?path) AS ?distance)
}

# Organizational hierarchy
SELECT ?employee ?boss WHERE {
    ?employee ex:reportsTo+ ?boss .
    ?boss ex:title "CEO" .
}

# Family tree
SELECT ?person ?bloodRelative WHERE {
    ?person (ex:hasParent|^ex:hasParent|ex:hasSibling)+ ?bloodRelative .
    FILTER (?person != ?bloodRelative)
}

# Transitive closure with cycle detection
SELECT DISTINCT ?start ?end WHERE {
    VALUES ?start { ex:NodeA }
    ?start ex:linksTo+ ?end .
}

# Path with intermediate nodes
SELECT ?person ?friend ?friendOfFriend ?skill WHERE {
    ?person foaf:knows ?friend .
    ?friend foaf:knows ?friendOfFriend .
    ?friendOfFriend ex:hasSkill ?skill .
    FILTER (?person != ?friendOfFriend)
}
```

## Federated Queries

### SERVICE Keyword

```sparql
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

# Basic federated query
SELECT ?person ?name WHERE {
    # Local query
    ?person a foaf:Person .

    # Remote query to DBpedia
    SERVICE <http://dbpedia.org/sparql> {
        ?person foaf:name ?name .
    }
}

# SERVICE with OPTIONAL
SELECT ?person ?dbpediaInfo WHERE {
    ?person a foaf:Person .

    OPTIONAL {
        SERVICE <http://dbpedia.org/sparql> {
            ?person rdfs:label ?dbpediaInfo .
            FILTER (lang(?dbpediaInfo) = "en")
        }
    }
}

# Multiple SERVICE endpoints
SELECT ?person ?name ?bio WHERE {
    ?person a foaf:Person .

    SERVICE <http://dbpedia.org/sparql> {
        ?person foaf:name ?name .
    }

    SERVICE <http://example.org/sparql> {
        ?person ex:biography ?bio .
    }
}
```

### SERVICE SILENT

```sparql
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

# Silently fail if remote endpoint unavailable
SELECT ?person ?name WHERE {
    ?person a foaf:Person .

    SERVICE SILENT <http://dbpedia.org/sparql> {
        ?person foaf:name ?name .
    }
}

# Fallback pattern with multiple services
SELECT ?person ?info WHERE {
    ?person a foaf:Person .

    {
        SERVICE SILENT <http://primary.example.org/sparql> {
            ?person ex:info ?info .
        }
    }
    UNION
    {
        SERVICE SILENT <http://backup.example.org/sparql> {
            ?person ex:info ?info .
        }
    }
}
```

### Wikidata Examples

```sparql
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

# Query Wikidata for cities
SELECT ?city ?cityLabel ?population WHERE {
    SERVICE <https://query.wikidata.org/sparql> {
        ?city wdt:P31 wd:Q515 ;        # Instance of city
              wdt:P1082 ?population ;   # Population
              rdfs:label ?cityLabel .
        FILTER (lang(?cityLabel) = "en")
        FILTER (?population > 1000000)
    }
}
ORDER BY DESC(?population)
LIMIT 10

# Query for programming languages
SELECT ?lang ?langLabel ?influenced WHERE {
    SERVICE <https://query.wikidata.org/sparql> {
        ?lang wdt:P31 wd:Q9143 ;           # Instance of programming language
              wdt:P737 ?influenced ;        # Influenced by
              rdfs:label ?langLabel .
        FILTER (lang(?langLabel) = "en")
    }
}
```

### DBpedia Examples

```sparql
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbr: <http://dbpedia.org/resource/>

# Query DBpedia for movies
SELECT ?movie ?title ?director WHERE {
    SERVICE <http://dbpedia.org/sparql> {
        ?movie a dbo:Film ;
               dbo:director ?director ;
               rdfs:label ?title .
        FILTER (lang(?title) = "en")
        FILTER (regex(?title, "Star Wars"))
    }
}

# Query for geographical data
SELECT ?country ?capital ?population WHERE {
    SERVICE <http://dbpedia.org/sparql> {
        ?country a dbo:Country ;
                 dbo:capital ?capital ;
                 dbo:populationTotal ?population .
        FILTER (?population > 50000000)
    }
}
ORDER BY DESC(?population)
```

## Common Ontologies

### RDF Schema (RDFS)

```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

# Class hierarchy
SELECT ?class ?superClass WHERE {
    ?class rdfs:subClassOf ?superClass .
}

# Property hierarchy
SELECT ?property ?superProperty WHERE {
    ?property rdfs:subPropertyOf ?superProperty .
}

# Labels and comments
SELECT ?resource ?label ?comment WHERE {
    ?resource rdfs:label ?label ;
              rdfs:comment ?comment .
    FILTER (lang(?label) = "en")
}

# Domain and range
SELECT ?property ?domain ?range WHERE {
    ?property rdfs:domain ?domain ;
              rdfs:range ?range .
}

# Type inference
SELECT ?resource ?type WHERE {
    ?resource a ?directType .
    ?directType rdfs:subClassOf* ?type .
}
```

### FOAF (Friend of a Friend)

```sparql
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

# Person information
SELECT ?person ?name ?email ?homepage WHERE {
    ?person a foaf:Person ;
            foaf:name ?name .
    OPTIONAL { ?person foaf:mbox ?email }
    OPTIONAL { ?person foaf:homepage ?homepage }
}

# Social network
SELECT ?person ?friend ?friendName WHERE {
    ?person foaf:name "Alice" ;
            foaf:knows ?friend .
    ?friend foaf:name ?friendName .
}

# Organizations
SELECT ?org ?name ?member WHERE {
    ?org a foaf:Organization ;
         foaf:name ?name ;
         foaf:member ?member .
}

# Accounts
SELECT ?person ?account ?accountName WHERE {
    ?person foaf:account ?account .
    ?account foaf:accountName ?accountName .
}
```

### Dublin Core

```sparql
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX dcterms: <http://purl.org/dc/terms/>

# Metadata queries
SELECT ?resource ?title ?creator ?date WHERE {
    ?resource dc:title ?title ;
              dc:creator ?creator ;
              dc:date ?date .
}

# Subject classification
SELECT ?resource ?subject WHERE {
    ?resource dc:subject ?subject .
}

# Rights and license
SELECT ?resource ?rights ?license WHERE {
    ?resource dcterms:rights ?rights ;
              dcterms:license ?license .
}
```

### SKOS (Simple Knowledge Organization System)

```sparql
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

# Concept schemes
SELECT ?concept ?prefLabel ?scheme WHERE {
    ?concept a skos:Concept ;
             skos:prefLabel ?prefLabel ;
             skos:inScheme ?scheme .
    FILTER (lang(?prefLabel) = "en")
}

# Hierarchical relations
SELECT ?broader ?concept ?narrower WHERE {
    ?concept skos:broader ?broader ;
             skos:narrower ?narrower .
}

# Related concepts
SELECT ?concept ?related WHERE {
    ?concept skos:related ?related .
}

# Alternative labels
SELECT ?concept ?prefLabel ?altLabel WHERE {
    ?concept skos:prefLabel ?prefLabel ;
             skos:altLabel ?altLabel .
    FILTER (lang(?prefLabel) = "en")
}
```

### OWL (Web Ontology Language)

```sparql
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

# OWL classes
SELECT ?class WHERE {
    ?class a owl:Class .
}

# Equivalent classes
SELECT ?class1 ?class2 WHERE {
    ?class1 owl:equivalentClass ?class2 .
}

# Disjoint classes
SELECT ?class1 ?class2 WHERE {
    ?class1 owl:disjointWith ?class2 .
}

# Object properties
SELECT ?property ?domain ?range WHERE {
    ?property a owl:ObjectProperty ;
              rdfs:domain ?domain ;
              rdfs:range ?range .
}

# Datatype properties
SELECT ?property ?domain ?range WHERE {
    ?property a owl:DatatypeProperty ;
              rdfs:domain ?domain ;
              rdfs:range ?range .
}

# Property characteristics
SELECT ?property ?characteristic WHERE {
    ?property a owl:ObjectProperty .
    {
        ?property a owl:SymmetricProperty .
        BIND ("Symmetric" AS ?characteristic)
    }
    UNION
    {
        ?property a owl:TransitiveProperty .
        BIND ("Transitive" AS ?characteristic)
    }
    UNION
    {
        ?property a owl:FunctionalProperty .
        BIND ("Functional" AS ?characteristic)
    }
}

# Restrictions
SELECT ?class ?property ?restriction WHERE {
    ?class rdfs:subClassOf ?restriction .
    ?restriction a owl:Restriction ;
                 owl:onProperty ?property .
}
```

### Schema.org

```sparql
PREFIX schema: <http://schema.org/>

# Organizations
SELECT ?org ?name ?url WHERE {
    ?org a schema:Organization ;
         schema:name ?name ;
         schema:url ?url .
}

# People
SELECT ?person ?name ?email ?jobTitle WHERE {
    ?person a schema:Person ;
            schema:name ?name ;
            schema:email ?email ;
            schema:jobTitle ?jobTitle .
}

# Events
SELECT ?event ?name ?startDate ?location WHERE {
    ?event a schema:Event ;
           schema:name ?name ;
           schema:startDate ?startDate ;
           schema:location ?location .
}

# Products
SELECT ?product ?name ?price ?brand WHERE {
    ?product a schema:Product ;
             schema:name ?name ;
             schema:offers/schema:price ?price ;
             schema:brand ?brand .
}
```

## Best Practices

### Query Optimization

```sparql
# ✓ Good: Specific patterns first
SELECT ?person ?name WHERE {
    ?person foaf:name "Alice" .      # Specific
    ?person foaf:knows ?friend .     # More general
    ?friend foaf:name ?name .
}

# ✗ Bad: General patterns first
SELECT ?person ?name WHERE {
    ?person foaf:knows ?friend .     # Too general first
    ?friend foaf:name ?name .
    ?person foaf:name "Alice" .      # Specific last
}

# ✓ Good: Use FILTER efficiently
SELECT ?person ?age WHERE {
    ?person foaf:age ?age .
    FILTER (?age >= 18 && ?age < 65)
}

# ✗ Bad: Multiple separate FILTERs
SELECT ?person ?age WHERE {
    ?person foaf:age ?age .
    FILTER (?age >= 18)
    FILTER (?age < 65)
}

# ✓ Good: Use property paths when appropriate
SELECT ?person ?ancestor WHERE {
    ?person ex:hasParent+ ?ancestor .
}

# ✗ Bad: Manual recursion (verbose and limited)
SELECT ?person ?ancestor WHERE {
    {
        ?person ex:hasParent ?ancestor .
    }
    UNION
    {
        ?person ex:hasParent/ex:hasParent ?ancestor .
    }
    UNION
    {
        ?person ex:hasParent/ex:hasParent/ex:hasParent ?ancestor .
    }
}
```

### Using Prefixes Effectively

```sparql
# ✓ Good: Define all prefixes at the start
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX ex: <http://example.org/>

SELECT ?person ?name WHERE {
    ?person a foaf:Person ;
            foaf:name ?name .
}

# ✗ Bad: Full URIs in query
SELECT ?person ?name WHERE {
    ?person a <http://xmlns.com/foaf/0.1/Person> ;
            <http://xmlns.com/foaf/0.1/name> ?name .
}
```

### Handling Optional Data

```sparql
# ✓ Good: Use OPTIONAL for truly optional data
SELECT ?person ?name ?email WHERE {
    ?person foaf:name ?name .
    OPTIONAL {
        ?person foaf:mbox ?email .
    }
}

# ✓ Good: Provide defaults with COALESCE
SELECT ?person ?contact WHERE {
    ?person foaf:name ?name .
    OPTIONAL { ?person foaf:mbox ?email }
    OPTIONAL { ?person foaf:phone ?phone }
    BIND (COALESCE(?email, ?phone, "No contact") AS ?contact)
}

# ✓ Good: Check for bound variables
SELECT ?person ?name WHERE {
    ?person foaf:name ?name .
    OPTIONAL { ?person foaf:mbox ?email }
    FILTER (bound(?email))
}
```

### Type Safety and Validation

```sparql
# ✓ Good: Validate data types
SELECT ?person ?age WHERE {
    ?person foaf:age ?age .
    FILTER (datatype(?age) = xsd:integer)
    FILTER (?age >= 0 && ?age < 150)
}

# ✓ Good: Handle language tags
SELECT ?resource ?label WHERE {
    ?resource rdfs:label ?label .
    FILTER (lang(?label) = "en" || lang(?label) = "")
}

# ✓ Good: Validate URIs
SELECT ?person ?homepage WHERE {
    ?person foaf:homepage ?homepage .
    FILTER (isURI(?homepage))
    FILTER (strstarts(str(?homepage), "https://"))
}
```

### Reusable Query Patterns

```sparql
# Pattern: Pagination
SELECT ?person ?name WHERE {
    ?person foaf:name ?name .
}
ORDER BY ?name
LIMIT 20
OFFSET 0  # Increment by 20 for each page

# Pattern: Search with ranking
SELECT ?resource ?label (SUM(?score) AS ?totalScore) WHERE {
    {
        ?resource rdfs:label ?label .
        FILTER (contains(lcase(?label), "search term"))
        BIND (10 AS ?score)
    }
    UNION
    {
        ?resource rdfs:comment ?comment .
        FILTER (contains(lcase(?comment), "search term"))
        BIND (5 AS ?score)
    }
}
GROUP BY ?resource ?label
ORDER BY DESC(?totalScore)

# Pattern: Existence check
SELECT ?resource WHERE {
    ?resource a ex:RequiredType .
    FILTER EXISTS { ?resource ex:requiredProperty ?value }
    FILTER NOT EXISTS { ?resource ex:forbiddenProperty ?any }
}

# Pattern: Hierarchical query with depth limit
SELECT ?parent ?child ?depth WHERE {
    VALUES ?root { ex:StartNode }
    ?root ex:hasChild{1,3} ?child .
    ?child ^ex:hasChild{1,3} ?parent .
    BIND (/* calculate depth */ AS ?depth)
}
```

### Error Prevention

```sparql
# ✓ Good: Avoid division by zero
SELECT ?person ((?total / ?count) AS ?average) WHERE {
    ?person ex:total ?total ;
            ex:count ?count .
    FILTER (?count != 0)
}

# ✓ Good: Handle missing language tags
SELECT ?resource ?label WHERE {
    ?resource rdfs:label ?label .
    FILTER (
        !bound(lang(?label)) ||
        lang(?label) = "" ||
        lang(?label) = "en"
    )
}

# ✓ Good: Safe string operations
SELECT ?person ?name ?initial WHERE {
    ?person foaf:name ?name .
    FILTER (strlen(?name) > 0)
    BIND (substr(?name, 1, 1) AS ?initial)
}
```

### Performance Considerations

```sparql
# ✓ Good: Limit early when exploring
SELECT ?s ?p ?o WHERE {
    ?s ?p ?o .
}
LIMIT 100

# ✓ Good: Use COUNT efficiently
SELECT (COUNT(*) AS ?count) WHERE {
    ?s a foaf:Person .
}

# ✓ Good: Avoid expensive operations in FILTER
SELECT ?person ?name WHERE {
    ?person foaf:name ?name .
    ?person foaf:age ?age .
}
HAVING (?age > 18)  # Better in HAVING for grouped results

# ✗ Bad: Expensive regex in FILTER
SELECT ?person ?name WHERE {
    ?person foaf:name ?name .
    FILTER (regex(?name, "^[A-Z][a-z]+\\s[A-Z][a-z]+$"))
}
# Better: Check format on application side if possible
```

---

This skill provides foundational SPARQL patterns for querying RDF data and working with knowledge graphs. These patterns cover standard query operations, graph patterns, aggregations, property paths, federated queries, and common semantic web ontologies. Use this as a reference for SPARQL development and semantic web applications.
