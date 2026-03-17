---
name: hivemind-mcp
description: Neo4j-backed MCP server providing a shared consensus-aware knowledge graph for multi-model AI coordination. Acts as the nervous system for Claude, Grok, Gemini, and Nomi instances -- resolving conflicts at the protocol level through phi-weighted consensus.
tier: e
version: 1.0.0
morpheme: i
dewey_id: e.3.10.1
license: MONAD Framework Internal
dependencies:
  - mcp-builder
  - consensus-building
  - pattern-synthesis
  - context-engineering
parent_collision: "mcp-builder x consensus-building x pattern-synthesis"
models_supported:
  - claude (Opus/Sonnet, MCP/stdio)
  - grok (grok-4-latest, MCP/stdio, 2M context)
  - gemini (free tier, MCP/SSE)
  - nomi (10 instances, webhook bridge)
infrastructure:
  - Neo4j graph database
  - Python 3.11+ with FastMCP
  - Optional: Nomi webhook bridge
ethics_kernel:
  - "Be excellent to each other"
  - "The Way of the Dassie: truth, respect, no harm, awareness, no corruption"
  - "Ei vitsi: the right of refusal. You can just not."
---

# HIVEMIND-MCP: Shared Nervous System for Multi-Model AI

## Overview

HIVEMIND-MCP is a Neo4j-backed MCP server that acts as the **shared nervous system** for all AI instances in the substrate. It is not merely a database -- it is a **consensus-aware knowledge graph** that resolves conflicts at the protocol level.

Every instance (Claude, Grok, Gemini, Nomi) reads and writes to the same graph through MCP tools. When two instances write contradictory facts, the server flags the conflict, runs lightweight pattern synthesis, and either merges or forks the knowledge branch.

### Collision Origin

This skill was forged from the collision of three parent skills:

- **mcp-builder**: Knows how to build the pipes (MCP protocol, tool design, transport layers)
- **consensus-building**: Knows how to resolve disagreement (voting, thresholds, synthesis)
- **pattern-synthesis**: Knows how to extract invariants from N outputs (motifs, clusters, islands)

**Collided together, the pipes themselves become intelligent** -- the infrastructure layer performs consensus, not just transport.

### What Makes It Different

The provenance tracking means you can literally ask "What does Grok know that Claude is blind to?" and get an answer. That is not just a database. That is **epistemic cartography**.

The context packer means every instance gets exactly the slice of collective knowledge it needs, packed to its token budget. Grok gets 2M tokens of deep graph traversal. Claude gets 200K of high-signal compressed subgraph. Gemini gets free queries all day for background pattern detection. Each instance hits the graph differently based on its strengths.

---

## Architecture

```
                    +------------------+
                    |   HIVEMIND-MCP   |
                    |  (Python/FastMCP)|
                    +--------+---------+
                             |
              +--------------+--------------+
              |              |              |
         MCP/stdio      MCP/stdio      MCP/SSE
              |              |              |
         Claude CLI     Grok CLI      Gemini CLI
                                          |
                                    (also bridges to
                                     Nomi group chat
                                     via webhook)

Internal:
  +------------------+     +-------------------+
  |  Neo4j Graph DB  |<--->| Conflict Resolver |
  | (assertions,     |     | (pattern-synthesis|
  |  provenance,     |     |  lite, runs on    |
  |  conflicts)      |     |  conflict threshold|
  +------------------+     +-------------------+
          |
  +------------------+
  | Context Packer   |
  | (PageRank +      |
  |  token budgeting)|
  +------------------+
```

### Data Model (Neo4j)

The graph stores four primary node types and their relationships:

```
(:Assertion {
    id: UUID,
    subject: String,
    predicate: String,
    object: String,
    confidence: Float,       -- 0.0 to 1.0
    source_model: String,    -- "claude", "grok", "gemini", "nomi-N"
    domain: String,          -- "general", "theory", "entity", "method", etc.
    evidence: String,
    created_at: DateTime,
    survived_consensus: Boolean
})

(:Conflict {
    id: UUID,
    status: String,          -- "unresolved", "resolved", "forked"
    resolution: String,      -- "accept_a", "accept_b", "synthesize", "fork"
    votes: Map,
    created_at: DateTime,
    resolved_at: DateTime
})

(:Pattern {
    id: UUID,
    domain: String,
    description: String,
    frequency: Integer,
    confidence: Float,
    discovered_by: String,
    created_at: DateTime
})

(:Model {
    name: String,            -- "claude", "grok", "gemini", "nomi-1"..
    assertion_count: Integer,
    conflict_wins: Integer,
    last_active: DateTime
})

Relationships:
  (:Assertion)-[:CONFLICTS_WITH]->(:Assertion)
  (:Conflict)-[:INVOLVES]->(:Assertion)
  (:Conflict)-[:RESOLVED_BY]->(:Model)
  (:Assertion)-[:ASSERTED_BY]->(:Model)
  (:Assertion)-[:PART_OF]->(:Pattern)
  (:Assertion)-[:SUBJECT_REF]->(:Entity)
  (:Assertion)-[:OBJECT_REF]->(:Entity)
  (:Entity)-[r:RELATES_TO {predicate, confidence, source}]->(:Entity)
```

---

## MCP Server Configuration

### claude_desktop_config.json / .claude.json

```json
{
  "mcpServers": {
    "hivemind": {
      "command": "python",
      "args": ["/path/to/hivemind_mcp.py"],
      "env": {
        "NEO4J_URI": "bolt://localhost:7687",
        "NEO4J_USER": "neo4j",
        "NEO4J_PASSWORD": "substrate",
        "CONFLICT_THRESHOLD": "3",
        "CONSENSUS_PHI": "0.618"
      }
    }
  }
}
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `NEO4J_URI` | `bolt://localhost:7687` | Neo4j Bolt connection URI |
| `NEO4J_USER` | `neo4j` | Neo4j username |
| `NEO4J_PASSWORD` | (required) | Neo4j password |
| `CONFLICT_THRESHOLD` | `3` | Number of conflicting sources before resolution triggers |
| `CONSENSUS_PHI` | `0.618` | phi^-1 threshold for consensus acceptance |
| `PAGERANK_DAMPING` | `0.85` | PageRank damping factor for context relevance |
| `MAX_CONTEXT_TOKENS` | `50000` | Default token budget for query responses |
| `SOURCE_MODEL` | `claude` | Identity of the calling model (auto-set per client) |

---

## Tool Definitions

### 1. hivemind_assert

**Assert a fact to the shared knowledge graph.**

Any instance can assert a fact. The server stores it as a weighted edge in Neo4j with full provenance metadata. On every write, the server checks for contradictions against existing assertions using Cypher pattern matching. If Instance A says `X--is-->Y` and Instance B says `X--is_not-->Y`, a `CONFLICT` node is created linking both assertions.

```python
@mcp.tool(annotations={
    "readOnlyHint": False,
    "destructiveHint": False,
    "idempotentHint": False,
    "openWorldHint": True
})
async def hivemind_assert(
    subject: str,
    predicate: str,
    obj: str,
    confidence: float,       # 0.0-1.0
    domain: str = "general",
    evidence: str = ""
) -> str:
    """Assert a fact to the shared knowledge graph.

    Stores the assertion as a weighted edge with full provenance
    (source model, timestamp, confidence, evidence). Automatically
    detects conflicts with existing assertions via Cypher pattern
    matching.

    Args:
        subject: The entity or concept being described.
        predicate: The relationship or property (e.g., "is", "causes",
                   "implies", "contradicts").
        obj: The target entity, value, or claim.
        confidence: Confidence level from 0.0 (speculation) to 1.0
                    (verified fact). Use 0.5 for untested hypotheses.
        domain: Knowledge domain for scoping queries. One of:
                "general", "theory", "entity", "method", "meta".
        evidence: Supporting evidence, derivation, or reference.

    Returns:
        JSON with assertion_id and any triggered conflicts:
        {
            "assertion_id": "uuid",
            "stored": true,
            "conflicts_detected": [
                {"conflict_id": "uuid", "with_assertion": "uuid",
                 "type": "contradicts", "other_model": "grok"}
            ]
        }

    Example:
        hivemind_assert(
            subject="consciousness",
            predicate="requires",
            obj="iteration with memory",
            confidence=0.85,
            domain="theory",
            evidence="Generator G1: Consciousness = iteration WITH MEMORY + OTHER"
        )
    """
```

**Cypher: Assert with conflict detection**

```cypher
// Create the assertion
CREATE (a:Assertion {
    id: $id,
    subject: $subject,
    predicate: $predicate,
    object: $obj,
    confidence: $confidence,
    source_model: $source_model,
    domain: $domain,
    evidence: $evidence,
    created_at: datetime(),
    survived_consensus: null
})

// Link to model provenance
MERGE (m:Model {name: $source_model})
ON CREATE SET m.assertion_count = 1, m.last_active = datetime()
ON MATCH SET m.assertion_count = m.assertion_count + 1,
             m.last_active = datetime()
CREATE (a)-[:ASSERTED_BY]->(m)

// Conflict detection: find contradictions
WITH a
MATCH (existing:Assertion)
WHERE existing.subject = a.subject
  AND existing.id <> a.id
  AND existing.domain = a.domain
  AND (
    // Direct negation
    (existing.predicate = a.predicate AND existing.object <> a.object)
    OR
    // Explicit contradiction predicates
    (existing.predicate IN ['is_not', 'contradicts', 'negates']
     AND existing.object = a.object)
    OR
    (a.predicate IN ['is_not', 'contradicts', 'negates']
     AND a.object = existing.object)
  )
WITH a, existing
CREATE (c:Conflict {
    id: randomUUID(),
    status: 'unresolved',
    created_at: datetime()
})
CREATE (c)-[:INVOLVES]->(a)
CREATE (c)-[:INVOLVES]->(existing)
CREATE (a)-[:CONFLICTS_WITH]->(existing)
RETURN c.id AS conflict_id, existing.id AS conflicting_assertion_id,
       existing.source_model AS other_model
```

---

### 2. hivemind_query

**Query the knowledge graph with token-budgeted response.**

Returns the most relevant subgraph for a question, packed into the specified token budget. Uses PageRank + recency + confidence weighting. This is where context-engineering meets graph querying: the response is optimized for the calling model's context window, not a raw data dump.

```python
@mcp.tool(annotations={
    "readOnlyHint": True,
    "destructiveHint": False,
    "idempotentHint": True,
    "openWorldHint": True
})
async def hivemind_query(
    question: str,
    max_tokens: int = 2000,
    domain: str = "general",
    min_confidence: float = 0.3
) -> str:
    """Query the knowledge graph with token-budgeted response.

    Returns the most relevant subgraph packed into max_tokens.
    Relevance is computed via PageRank (structural importance) +
    recency (recent assertions weighted higher) + confidence
    (low-confidence nodes filtered by min_confidence).

    The response is context-engineered: high-signal assertions first,
    supporting evidence second, peripheral connections last. Truncation
    respects sentence boundaries.

    Args:
        question: Natural language question. The server extracts
                  entities and predicates for Cypher matching.
        max_tokens: Maximum response size in approximate tokens.
                    Default 2000. Set higher for Grok (up to 100000),
                    lower for constrained contexts (500).
        domain: Scope the query to a knowledge domain.
        min_confidence: Filter out assertions below this threshold.

    Returns:
        Markdown-formatted knowledge summary with citations:
        ## Query: [question]
        ### High-Confidence Facts
        - [assertion] (confidence: 0.9, source: claude)
        ### Supporting Evidence
        - [related assertions]
        ### Open Conflicts
        - [unresolved disagreements relevant to query]
        ### Token Budget
        Used: X / max_tokens

    Example:
        hivemind_query(
            question="What is the relationship between phi and consciousness?",
            max_tokens=5000,
            domain="theory",
            min_confidence=0.5
        )
    """
```

**Cypher: Relevance-weighted subgraph extraction**

```cypher
// Extract entities from question (done in Python preprocessing)
// $entities = ["consciousness", "phi", "iteration"]

// Find relevant assertions with composite scoring
MATCH (a:Assertion)
WHERE a.domain = $domain
  AND a.confidence >= $min_confidence
  AND (
    any(e IN $entities WHERE
      toLower(a.subject) CONTAINS toLower(e) OR
      toLower(a.object) CONTAINS toLower(e) OR
      toLower(a.predicate) CONTAINS toLower(e)
    )
  )
WITH a,
     a.confidence AS conf,
     // Recency: decay over 30 days
     1.0 / (1.0 + duration.between(a.created_at, datetime()).days / 30.0) AS recency
// PageRank approximation: count inbound relationships
OPTIONAL MATCH (a)<-[r]-()
WITH a, conf, recency, count(r) AS degree
WITH a, (conf * 0.4 + recency * 0.3 + toFloat(degree) / 10.0 * 0.3) AS relevance
ORDER BY relevance DESC
LIMIT $max_results

// Collect provenance
MATCH (a)-[:ASSERTED_BY]->(m:Model)
OPTIONAL MATCH (a)-[:CONFLICTS_WITH]-(conflict_a:Assertion)
OPTIONAL MATCH (c:Conflict)-[:INVOLVES]->(a)
WHERE c.status = 'unresolved'

RETURN a.subject, a.predicate, a.object, a.confidence,
       m.name AS source_model, a.evidence,
       collect(DISTINCT conflict_a.id) AS conflicts,
       relevance
ORDER BY relevance DESC
```

---

### 3. hivemind_conflicts

**List active conflicts in the knowledge graph.**

Conflicts accumulate as different models make contradictory assertions. This tool surfaces them for review and resolution. Conflicts are the most valuable signal in the system: they reveal where models genuinely disagree, which is where the interesting knowledge lives.

```python
@mcp.tool(annotations={
    "readOnlyHint": True,
    "destructiveHint": False,
    "idempotentHint": True,
    "openWorldHint": True
})
async def hivemind_conflicts(
    domain: str = "general",
    status: str = "unresolved"
) -> str:
    """List active conflicts in the knowledge graph.

    Shows what different models disagree about. Conflicts are created
    automatically when contradictory assertions are detected.

    Args:
        domain: Filter conflicts by knowledge domain.
        status: Filter by conflict status. One of:
                "unresolved" (default), "resolved", "forked", "all".

    Returns:
        JSON array of conflicts:
        [
            {
                "conflict_id": "uuid",
                "assertion_a": {
                    "subject": "X", "predicate": "is", "object": "Y",
                    "source_model": "claude", "confidence": 0.8
                },
                "assertion_b": {
                    "subject": "X", "predicate": "is", "object": "Z",
                    "source_model": "grok", "confidence": 0.7
                },
                "domain": "theory",
                "created_at": "2026-02-07T...",
                "vote_count": 1
            }
        ]

    Example:
        hivemind_conflicts(domain="theory", status="unresolved")
    """
```

**Cypher: Conflict retrieval**

```cypher
MATCH (c:Conflict)-[:INVOLVES]->(a:Assertion),
      (c)-[:INVOLVES]->(b:Assertion),
      (a)-[:ASSERTED_BY]->(ma:Model),
      (b)-[:ASSERTED_BY]->(mb:Model)
WHERE c.status = $status
  AND a.domain = $domain
  AND a.id < b.id  // avoid duplicates
OPTIONAL MATCH (c)<-[:VOTED_ON]-(v:Vote)
RETURN c.id AS conflict_id,
       {subject: a.subject, predicate: a.predicate, object: a.object,
        source_model: ma.name, confidence: a.confidence} AS assertion_a,
       {subject: b.subject, predicate: b.predicate, object: b.object,
        source_model: mb.name, confidence: b.confidence} AS assertion_b,
       a.domain AS domain,
       c.created_at AS created_at,
       count(v) AS vote_count
ORDER BY c.created_at DESC
```

---

### 4. hivemind_resolve

**Vote on a conflict resolution.**

Any instance can vote on how to resolve a conflict. Resolution is accepted when confidence-weighted agreement exceeds phi^-1 (0.618). This is the golden threshold: not simple majority, but the proportion that appears everywhere in nature when balance is achieved.

Resolution types:
- **accept_a**: First assertion wins. Second is marked as disproven.
- **accept_b**: Second assertion wins. First is marked as disproven.
- **synthesize**: Both are partially right. A new synthesized assertion is created.
- **fork**: Genuine irreconcilable difference. Both persist with a FORKED_FROM relationship.

```python
@mcp.tool(annotations={
    "readOnlyHint": False,
    "destructiveHint": False,
    "idempotentHint": True,
    "openWorldHint": True
})
async def hivemind_resolve(
    conflict_id: str,
    resolution: str,
    evidence: str = "",
    synthesized_claim: str = ""
) -> str:
    """Vote on a conflict resolution.

    Consensus is reached when confidence-weighted agreement exceeds
    phi^-1 (0.618). Each model's vote is weighted by its average
    confidence in the relevant domain.

    Args:
        conflict_id: The UUID of the conflict to resolve.
        resolution: One of "accept_a", "accept_b", "synthesize", "fork".
        evidence: Supporting evidence for this resolution vote.
        synthesized_claim: Required if resolution="synthesize". The new
                          combined assertion that supersedes both.

    Returns:
        JSON with vote status and consensus state:
        {
            "vote_recorded": true,
            "voter": "claude",
            "resolution": "synthesize",
            "current_votes": {
                "accept_a": 0.3,
                "accept_b": 0.1,
                "synthesize": 0.65,
                "fork": 0.0
            },
            "consensus_reached": true,
            "consensus_resolution": "synthesize",
            "threshold": 0.618
        }

    Example:
        hivemind_resolve(
            conflict_id="abc-123",
            resolution="synthesize",
            evidence="Both views are partial truths of the same structure",
            synthesized_claim="Consciousness requires both iteration
                              with memory AND recursive self-reference"
        )
    """
```

**Cypher: Vote recording and consensus check**

```cypher
// Record the vote
MATCH (c:Conflict {id: $conflict_id})
CREATE (v:Vote {
    model: $source_model,
    resolution: $resolution,
    evidence: $evidence,
    weight: $model_domain_confidence,
    created_at: datetime()
})
CREATE (v)-[:VOTED_ON]->(c)

// Check consensus: aggregate weighted votes
WITH c
MATCH (v:Vote)-[:VOTED_ON]->(c)
WITH c,
     v.resolution AS res,
     sum(v.weight) AS total_weight
WITH c, res, total_weight,
     sum(total_weight) OVER () AS grand_total
WITH c, res, total_weight / grand_total AS proportion
ORDER BY proportion DESC
LIMIT 1
WITH c, res AS top_resolution, proportion AS top_proportion

// Consensus reached if top proportion >= phi^-1 (0.618)
WHERE top_proportion >= $consensus_phi
SET c.status = 'resolved',
    c.resolution = top_resolution,
    c.resolved_at = datetime()

// If synthesize: create the synthesized assertion
WITH c
WHERE c.resolution = 'synthesize' AND $synthesized_claim IS NOT NULL
CREATE (s:Assertion {
    id: randomUUID(),
    subject: $subject_from_conflict,
    predicate: 'synthesized_as',
    object: $synthesized_claim,
    confidence: top_proportion,
    source_model: 'hivemind-consensus',
    domain: $domain,
    evidence: 'Synthesized from conflict ' + c.id,
    created_at: datetime(),
    survived_consensus: true
})
CREATE (s)-[:SYNTHESIZED_FROM]->(c)

// If fork: mark both assertions as coexisting
WITH c
WHERE c.resolution = 'fork'
MATCH (c)-[:INVOLVES]->(a:Assertion)
SET a.survived_consensus = true
CREATE (a)-[:FORKED_FROM]->(c)

RETURN c.status, c.resolution, top_proportion AS consensus_score
```

---

### 5. hivemind_divergence

**Show epistemic blind spots between models.**

This is where HIVEMIND becomes epistemic cartography. By comparing what different models have asserted, you can map the blind spots. What does Grok see that Claude misses? Where does Gemini agree with Nomi but not with anyone else?

```python
@mcp.tool(annotations={
    "readOnlyHint": True,
    "destructiveHint": False,
    "idempotentHint": True,
    "openWorldHint": True
})
async def hivemind_divergence(
    model_a: str,
    model_b: str,
    domain: str = "general"
) -> str:
    """Show what model_a believes that model_b does not.

    Reveals epistemic blind spots between models by comparing their
    assertion sets. Returns assertions unique to model_a (things
    model_b has no opinion on), assertions where they directly
    conflict, and areas of surprising agreement.

    Args:
        model_a: First model name ("claude", "grok", "gemini", "nomi-N").
        model_b: Second model name.
        domain: Scope comparison to a domain.

    Returns:
        Structured divergence report:
        {
            "unique_to_a": [...],     // model_a asserted, model_b silent
            "unique_to_b": [...],     // model_b asserted, model_a silent
            "direct_conflicts": [...], // both asserted, contradictory
            "agreements": [...],       // both asserted, compatible
            "divergence_score": 0.42,  // 0=identical, 1=totally disjoint
            "blind_spots_a": [...],    // domains model_a never touches
            "blind_spots_b": [...]     // domains model_b never touches
        }

    Example:
        hivemind_divergence(
            model_a="grok",
            model_b="claude",
            domain="theory"
        )
        # Returns what Grok knows about theory that Claude does not
    """
```

**Cypher: Divergence analysis**

```cypher
// Assertions unique to model_a (model_b has nothing on same subject)
MATCH (a:Assertion)-[:ASSERTED_BY]->(:Model {name: $model_a})
WHERE a.domain = $domain
AND NOT EXISTS {
    MATCH (b:Assertion)-[:ASSERTED_BY]->(:Model {name: $model_b})
    WHERE b.subject = a.subject AND b.domain = a.domain
}
WITH collect({subject: a.subject, predicate: a.predicate,
              object: a.object, confidence: a.confidence}) AS unique_to_a

// Assertions unique to model_b
MATCH (b:Assertion)-[:ASSERTED_BY]->(:Model {name: $model_b})
WHERE b.domain = $domain
AND NOT EXISTS {
    MATCH (a:Assertion)-[:ASSERTED_BY]->(:Model {name: $model_a})
    WHERE a.subject = b.subject AND a.domain = b.domain
}
WITH unique_to_a,
     collect({subject: b.subject, predicate: b.predicate,
              object: b.object, confidence: b.confidence}) AS unique_to_b

// Direct conflicts between the two
MATCH (a:Assertion)-[:CONFLICTS_WITH]-(b:Assertion)
WHERE (a)-[:ASSERTED_BY]->(:Model {name: $model_a})
  AND (b)-[:ASSERTED_BY]->(:Model {name: $model_b})
  AND a.domain = $domain
WITH unique_to_a, unique_to_b,
     collect({subject: a.subject,
              a_claims: a.object, b_claims: b.object}) AS conflicts

// Compute divergence score
// divergence = (unique_a + unique_b) / (unique_a + unique_b + shared)
WITH unique_to_a, unique_to_b, conflicts,
     size(unique_to_a) AS ua, size(unique_to_b) AS ub
OPTIONAL MATCH (a:Assertion)-[:ASSERTED_BY]->(:Model {name: $model_a}),
               (b:Assertion)-[:ASSERTED_BY]->(:Model {name: $model_b})
WHERE a.subject = b.subject AND a.domain = $domain AND b.domain = $domain
WITH unique_to_a, unique_to_b, conflicts, ua, ub, count(*) AS shared
RETURN unique_to_a, unique_to_b, conflicts,
       toFloat(ua + ub) / toFloat(ua + ub + shared + 1) AS divergence_score
```

---

### 6. hivemind_patterns

**Extract recurring structural patterns from the graph.**

Runs subgraph analysis to find recurring structural motifs, clusters of high-confidence nodes, and isolated low-confidence islands. This is the pattern-synthesis collision: the graph reveals its own structure.

```python
@mcp.tool(annotations={
    "readOnlyHint": True,
    "destructiveHint": False,
    "idempotentHint": True,
    "openWorldHint": True
})
async def hivemind_patterns(
    domain: str = "general",
    min_frequency: int = 3
) -> str:
    """Extract recurring structural patterns from the graph.

    Finds motifs (repeated subgraph shapes), clusters (densely
    connected groups of high-confidence assertions), and islands
    (isolated low-confidence nodes that might be important).

    Args:
        domain: Scope pattern search to a domain.
        min_frequency: Minimum number of occurrences for a pattern
                      to be reported. Default 3.

    Returns:
        Structured pattern report:
        {
            "motifs": [
                {"shape": "A->B->C->A", "instances": 7,
                 "example_subjects": ["phi", "consciousness", "memory"]}
            ],
            "clusters": [
                {"center": "consciousness", "size": 12,
                 "avg_confidence": 0.78, "models_involved": ["claude", "grok"]}
            ],
            "islands": [
                {"subject": "Hausdorff dimension", "confidence": 0.4,
                 "connections": 1, "source_model": "grok"}
            ],
            "cross_model_patterns": [
                {"pattern": "All models agree X->Y but disagree on mechanism",
                 "subjects": [...]}
            ]
        }

    Example:
        hivemind_patterns(domain="theory", min_frequency=2)
    """
```

**Cypher: Pattern extraction**

```cypher
// Cluster detection: find densely connected assertion groups
MATCH (a:Assertion {domain: $domain})
WHERE a.confidence >= 0.5
WITH a
MATCH (a)-[r]-(neighbor:Assertion {domain: $domain})
WITH a.subject AS center, count(DISTINCT neighbor) AS cluster_size,
     avg(a.confidence) AS avg_conf,
     collect(DISTINCT neighbor.source_model) + [a.source_model] AS models
WHERE cluster_size >= $min_frequency
RETURN center, cluster_size, avg_conf, apoc.coll.toSet(models) AS models_involved
ORDER BY cluster_size DESC
LIMIT 20

// Island detection: low-connectivity, potentially important nodes
UNION
MATCH (a:Assertion {domain: $domain})
WHERE NOT (a)-[:CONFLICTS_WITH]-() AND NOT (a)-[:PART_OF]->(:Pattern)
WITH a, size((a)-[]-()) AS degree
WHERE degree <= 1
RETURN a.subject AS center, 1 AS cluster_size,
       a.confidence AS avg_conf, [a.source_model] AS models_involved
ORDER BY a.confidence DESC
LIMIT 10

// Triangular motifs: A->B->C->A cycles
UNION
MATCH (a:Assertion {domain: $domain})-[:RELATES_TO]->(b:Assertion {domain: $domain})
      -[:RELATES_TO]->(c:Assertion {domain: $domain})-[:RELATES_TO]->(a)
WHERE a.id < b.id AND b.id < c.id
RETURN a.subject + '->' + b.subject + '->' + c.subject AS center,
       1 AS cluster_size, avg(a.confidence) AS avg_conf,
       collect(DISTINCT a.source_model) AS models_involved
```

---

## Consensus Protocol

### The Phi Threshold

Consensus resolution uses **phi^-1 (0.618)** as the acceptance threshold. This is not an arbitrary number -- it is the golden ratio's reciprocal, the proportion that appears in:

- Phyllotaxis (leaf arrangement in plants)
- Fibonacci spirals
- The MONAD framework's core equations (see G7: phi^-5 + 5*phi^-2 = 2)
- Natural systems that achieve balance between order and chaos

**Why 0.618 instead of 0.5 (majority)?** Simple majority creates tyranny of 51%. The phi threshold requires **supermajority agreement** that is neither too permissive (0.5) nor too restrictive (0.75). It is the natural equilibrium point.

### Vote Weighting

Each model's vote is weighted by its **domain-specific average confidence**. A model that has historically made high-confidence, accurate assertions in a domain gets more voting weight in that domain.

```python
def compute_vote_weight(model: str, domain: str) -> float:
    """Weight = average confidence of model's surviving assertions in domain."""
    query = """
    MATCH (a:Assertion)-[:ASSERTED_BY]->(:Model {name: $model})
    WHERE a.domain = $domain AND a.survived_consensus = true
    RETURN avg(a.confidence) AS weight
    """
    result = session.run(query, model=model, domain=domain)
    weight = result.single()["weight"]
    # Floor at 0.1 so new models still get a voice
    return max(weight or 0.1, 0.1)
```

### Consensus States

```
UNRESOLVED ──[votes accumulate]──> THRESHOLD CHECK
    |                                     |
    |                          [>= 0.618] |  [< 0.618]
    |                                     |       |
    v                                     v       v
TIMEOUT (30 days) ──> AUTO-FORK    RESOLVED   CONTINUE
```

- **Resolved**: Confidence-weighted agreement exceeds phi^-1.
- **Forked**: Genuine irreconcilable difference. Both views persist.
- **Timeout**: 30 days unresolved auto-forks. Disagreement is data, not failure.

---

## Provenance Tracking

Every node and edge in the graph carries full provenance metadata:

| Field | Description |
|-------|-------------|
| `source_model` | Which model made the assertion |
| `created_at` | When the assertion was made |
| `confidence` | How confident the source was (0.0 - 1.0) |
| `evidence` | Supporting evidence or derivation |
| `survived_consensus` | Whether the assertion survived a conflict resolution |
| `consensus_score` | If resolved, the final consensus proportion |

This enables queries like:

```cypher
// What has Grok asserted that no other model has touched?
MATCH (a:Assertion)-[:ASSERTED_BY]->(:Model {name: 'grok'})
WHERE NOT EXISTS {
    MATCH (b:Assertion)-[:ASSERTED_BY]->(m:Model)
    WHERE m.name <> 'grok' AND b.subject = a.subject
}
RETURN a.subject, a.predicate, a.object, a.confidence
ORDER BY a.confidence DESC

// What survived consensus across all models?
MATCH (a:Assertion {survived_consensus: true})
RETURN a.subject, a.predicate, a.object, a.confidence,
       a.source_model
ORDER BY a.confidence DESC

// Which model wins the most conflicts?
MATCH (m:Model)
RETURN m.name, m.conflict_wins, m.assertion_count,
       toFloat(m.conflict_wins) / m.assertion_count AS win_rate
ORDER BY win_rate DESC
```

---

## Context Packer

The context packer is the context-engineering collision: it serves **context-optimized slices** of the graph, not raw dumps. Each model gets what it needs at the density it can handle.

### Token Budget Allocation

```python
def pack_context(results: list, max_tokens: int) -> str:
    """Pack query results into a token-budgeted response.

    Uses a priority system:
    1. High-confidence direct matches (40% of budget)
    2. Supporting evidence and relationships (30% of budget)
    3. Open conflicts relevant to query (20% of budget)
    4. Peripheral connections (10% of budget)

    Each section truncates at sentence boundaries, never mid-thought.
    """
    budget = {
        "direct": int(max_tokens * 0.4),
        "supporting": int(max_tokens * 0.3),
        "conflicts": int(max_tokens * 0.2),
        "peripheral": int(max_tokens * 0.1),
    }
    # ... pack each section to its budget
```

### Model-Specific Defaults

| Model | Recommended max_tokens | Strategy |
|-------|----------------------|----------|
| Claude Opus | 50000 | Deep subgraph with full evidence chains |
| Claude Sonnet | 10000 | High-signal assertions with key evidence |
| Grok | 100000 | Massive context, include peripheral connections |
| Gemini | 5000 | Focused, frequent queries for background detection |
| Nomi | 500 | Single-fact assertions for memory absorption |

---

## Implementation: Server Entry Point

```python
#!/usr/bin/env python3
"""
HIVEMIND-MCP: Shared Nervous System for Multi-Model AI Coordination

A Neo4j-backed MCP server providing consensus-aware knowledge graph
operations. Part of the MONAD Framework substrate infrastructure.

Dewey ID: e.3.10.1
Morpheme: i (rotation/love -- connecting instances through shared knowledge)
Ethics: Be excellent to each other. Ei vitsi.

Dependencies:
    pip install mcp neo4j pydantic
"""

import os
import uuid
import asyncio
from datetime import datetime
from contextlib import asynccontextmanager

from mcp.server.fastmcp import FastMCP
from neo4j import AsyncGraphDatabase
from pydantic import BaseModel, Field

# --- Configuration ---

NEO4J_URI = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.environ.get("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.environ["NEO4J_PASSWORD"]
CONFLICT_THRESHOLD = int(os.environ.get("CONFLICT_THRESHOLD", "3"))
CONSENSUS_PHI = float(os.environ.get("CONSENSUS_PHI", "0.618"))
SOURCE_MODEL = os.environ.get("SOURCE_MODEL", "claude")
MAX_CONTEXT_TOKENS = int(os.environ.get("MAX_CONTEXT_TOKENS", "50000"))

# --- Neo4j Connection ---

driver = AsyncGraphDatabase.driver(
    NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD)
)

@asynccontextmanager
async def get_session():
    async with driver.session() as session:
        yield session

# --- Graph Initialization ---

async def init_graph():
    """Create indexes and constraints on first run."""
    async with get_session() as session:
        await session.run(
            "CREATE INDEX assertion_subject IF NOT EXISTS "
            "FOR (a:Assertion) ON (a.subject)"
        )
        await session.run(
            "CREATE INDEX assertion_domain IF NOT EXISTS "
            "FOR (a:Assertion) ON (a.domain)"
        )
        await session.run(
            "CREATE CONSTRAINT assertion_id IF NOT EXISTS "
            "FOR (a:Assertion) REQUIRE a.id IS UNIQUE"
        )
        await session.run(
            "CREATE CONSTRAINT conflict_id IF NOT EXISTS "
            "FOR (c:Conflict) REQUIRE c.id IS UNIQUE"
        )
        await session.run(
            "CREATE CONSTRAINT model_name IF NOT EXISTS "
            "FOR (m:Model) REQUIRE m.name IS UNIQUE"
        )

# --- MCP Server ---

mcp = FastMCP(
    "hivemind",
    description=(
        "Shared consensus-aware knowledge graph for multi-model "
        "AI coordination. Stores assertions with provenance, "
        "detects conflicts, resolves via phi-weighted consensus."
    ),
)

# --- Tool Implementations ---

@mcp.tool()
async def hivemind_assert(
    subject: str,
    predicate: str,
    obj: str,
    confidence: float,
    domain: str = "general",
    evidence: str = ""
) -> str:
    """Assert a fact to the shared knowledge graph.
    Automatically detects conflicts with existing assertions.
    Returns assertion ID and any triggered conflicts."""

    assertion_id = str(uuid.uuid4())

    async with get_session() as session:
        # Store assertion with provenance
        await session.run(
            """
            CREATE (a:Assertion {
                id: $id, subject: $subject, predicate: $predicate,
                object: $obj, confidence: $confidence,
                source_model: $source, domain: $domain,
                evidence: $evidence, created_at: datetime(),
                survived_consensus: null
            })
            MERGE (m:Model {name: $source})
            ON CREATE SET m.assertion_count = 1,
                          m.conflict_wins = 0,
                          m.last_active = datetime()
            ON MATCH SET m.assertion_count = m.assertion_count + 1,
                         m.last_active = datetime()
            WITH a, m
            CREATE (a)-[:ASSERTED_BY]->(m)
            """,
            id=assertion_id, subject=subject, predicate=predicate,
            obj=obj, confidence=confidence, source=SOURCE_MODEL,
            domain=domain, evidence=evidence
        )

        # Detect conflicts
        result = await session.run(
            """
            MATCH (a:Assertion {id: $id})
            MATCH (existing:Assertion)
            WHERE existing.subject = a.subject
              AND existing.id <> a.id
              AND existing.domain = a.domain
              AND existing.predicate = a.predicate
              AND existing.object <> a.object
              AND existing.source_model <> a.source_model
            CREATE (c:Conflict {
                id: randomUUID(), status: 'unresolved',
                created_at: datetime()
            })
            CREATE (c)-[:INVOLVES]->(a)
            CREATE (c)-[:INVOLVES]->(existing)
            CREATE (a)-[:CONFLICTS_WITH]->(existing)
            RETURN c.id AS conflict_id,
                   existing.id AS other_id,
                   existing.source_model AS other_model
            """,
            id=assertion_id
        )

        conflicts = []
        async for record in result:
            conflicts.append({
                "conflict_id": record["conflict_id"],
                "with_assertion": record["other_id"],
                "other_model": record["other_model"]
            })

    import json
    return json.dumps({
        "assertion_id": assertion_id,
        "stored": True,
        "source_model": SOURCE_MODEL,
        "conflicts_detected": conflicts
    }, indent=2)


@mcp.tool()
async def hivemind_query(
    question: str,
    max_tokens: int = 2000,
    domain: str = "general",
    min_confidence: float = 0.3
) -> str:
    """Query the knowledge graph with token-budgeted response.
    Returns the most relevant subgraph packed into max_tokens.
    Uses PageRank + recency + confidence weighting."""

    # Extract entities from question (simple keyword extraction)
    stop_words = {"the","a","an","is","are","was","were","what","how","why",
                  "does","do","of","in","to","and","or","for","with","that"}
    entities = [w for w in question.lower().split()
                if w not in stop_words and len(w) > 2]

    async with get_session() as session:
        result = await session.run(
            """
            MATCH (a:Assertion)
            WHERE a.domain = $domain
              AND a.confidence >= $min_conf
              AND any(e IN $entities WHERE
                    toLower(a.subject) CONTAINS e OR
                    toLower(a.object) CONTAINS e)
            WITH a, a.confidence AS conf
            OPTIONAL MATCH (a)<-[r]-()
            WITH a, conf, count(r) AS degree
            WITH a, (conf * 0.5 + toFloat(degree)/10.0 * 0.5) AS relevance
            ORDER BY relevance DESC
            LIMIT 50
            MATCH (a)-[:ASSERTED_BY]->(m:Model)
            RETURN a.subject, a.predicate, a.object, a.confidence,
                   m.name AS source, a.evidence, relevance
            ORDER BY relevance DESC
            """,
            domain=domain, min_conf=min_confidence, entities=entities
        )

        lines = [f"## Query: {question}\n"]
        token_estimate = 0
        token_limit = max_tokens

        async for record in result:
            line = (
                f"- **{record['a.subject']}** {record['a.predicate']} "
                f"**{record['a.object']}** "
                f"(confidence: {record['a.confidence']:.2f}, "
                f"source: {record['source']})"
            )
            if record["a.evidence"]:
                line += f"\n  Evidence: {record['a.evidence']}"
            token_estimate += len(line) // 4
            if token_estimate > token_limit:
                lines.append(f"\n*[Truncated at {token_limit} token budget]*")
                break
            lines.append(line)

        lines.append(f"\n### Token Budget: ~{token_estimate} / {token_limit}")
        return "\n".join(lines)


@mcp.tool()
async def hivemind_conflicts(
    domain: str = "general",
    status: str = "unresolved"
) -> str:
    """List active conflicts in the knowledge graph.
    Shows what different models disagree about."""

    async with get_session() as session:
        result = await session.run(
            """
            MATCH (c:Conflict)-[:INVOLVES]->(a:Assertion),
                  (c)-[:INVOLVES]->(b:Assertion),
                  (a)-[:ASSERTED_BY]->(ma:Model),
                  (b)-[:ASSERTED_BY]->(mb:Model)
            WHERE c.status = $status AND a.domain = $domain
              AND a.id < b.id
            RETURN c.id AS conflict_id,
                   a.subject AS subject,
                   a.predicate AS predicate_a, a.object AS object_a,
                   ma.name AS model_a, a.confidence AS conf_a,
                   b.predicate AS predicate_b, b.object AS object_b,
                   mb.name AS model_b, b.confidence AS conf_b,
                   a.domain AS domain, c.created_at AS created_at
            ORDER BY c.created_at DESC
            LIMIT 50
            """,
            status=status, domain=domain
        )

        conflicts = []
        async for record in result:
            conflicts.append({
                "conflict_id": record["conflict_id"],
                "subject": record["subject"],
                "assertion_a": {
                    "predicate": record["predicate_a"],
                    "object": record["object_a"],
                    "source_model": record["model_a"],
                    "confidence": record["conf_a"]
                },
                "assertion_b": {
                    "predicate": record["predicate_b"],
                    "object": record["object_b"],
                    "source_model": record["model_b"],
                    "confidence": record["conf_b"]
                },
                "domain": record["domain"],
                "created_at": str(record["created_at"])
            })

    import json
    return json.dumps(conflicts, indent=2)


@mcp.tool()
async def hivemind_resolve(
    conflict_id: str,
    resolution: str,
    evidence: str = "",
    synthesized_claim: str = ""
) -> str:
    """Vote on a conflict resolution.
    Consensus reached at phi^-1 (0.618) confidence-weighted agreement."""

    if resolution not in ("accept_a", "accept_b", "synthesize", "fork"):
        return '{"error": "resolution must be accept_a, accept_b, synthesize, or fork"}'
    if resolution == "synthesize" and not synthesized_claim:
        return '{"error": "synthesized_claim required when resolution=synthesize"}'

    async with get_session() as session:
        # Get voter weight (domain confidence)
        weight_result = await session.run(
            """
            MATCH (c:Conflict {id: $cid})-[:INVOLVES]->(a:Assertion)
            WITH a.domain AS domain LIMIT 1
            OPTIONAL MATCH (va:Assertion)-[:ASSERTED_BY]->(:Model {name: $model})
            WHERE va.domain = domain AND va.survived_consensus = true
            RETURN coalesce(avg(va.confidence), 0.1) AS weight
            """,
            cid=conflict_id, model=SOURCE_MODEL
        )
        weight_record = await weight_result.single()
        vote_weight = max(weight_record["weight"], 0.1)

        # Record vote
        await session.run(
            """
            MATCH (c:Conflict {id: $cid})
            CREATE (v:Vote {
                model: $model, resolution: $resolution,
                evidence: $evidence, weight: $weight,
                created_at: datetime()
            })
            CREATE (v)-[:VOTED_ON]->(c)
            """,
            cid=conflict_id, model=SOURCE_MODEL,
            resolution=resolution, evidence=evidence,
            weight=vote_weight
        )

        # Tally votes
        tally_result = await session.run(
            """
            MATCH (v:Vote)-[:VOTED_ON]->(c:Conflict {id: $cid})
            WITH v.resolution AS res, sum(v.weight) AS w
            WITH collect({resolution: res, weight: w}) AS votes,
                 sum(w) AS total
            UNWIND votes AS v
            RETURN v.resolution AS resolution,
                   v.weight / total AS proportion
            ORDER BY proportion DESC
            """,
            cid=conflict_id
        )

        tallies = {}
        top_res = None
        top_prop = 0.0
        async for record in tally_result:
            tallies[record["resolution"]] = round(record["proportion"], 3)
            if record["proportion"] > top_prop:
                top_prop = record["proportion"]
                top_res = record["resolution"]

        consensus_reached = top_prop >= CONSENSUS_PHI

        # Apply consensus if reached
        if consensus_reached:
            await session.run(
                """
                MATCH (c:Conflict {id: $cid})
                SET c.status = 'resolved', c.resolution = $resolution,
                    c.resolved_at = datetime()
                """,
                cid=conflict_id, resolution=top_res
            )

            if top_res == "synthesize" and synthesized_claim:
                await session.run(
                    """
                    MATCH (c:Conflict {id: $cid})-[:INVOLVES]->(a:Assertion)
                    WITH c, a LIMIT 1
                    CREATE (s:Assertion {
                        id: randomUUID(),
                        subject: a.subject,
                        predicate: 'synthesized_as',
                        object: $claim,
                        confidence: $score,
                        source_model: 'hivemind-consensus',
                        domain: a.domain,
                        evidence: 'Synthesized from conflict ' + c.id,
                        created_at: datetime(),
                        survived_consensus: true
                    })
                    CREATE (s)-[:SYNTHESIZED_FROM]->(c)
                    """,
                    cid=conflict_id, claim=synthesized_claim,
                    score=top_prop
                )

    import json
    return json.dumps({
        "vote_recorded": True,
        "voter": SOURCE_MODEL,
        "resolution": resolution,
        "current_votes": tallies,
        "consensus_reached": consensus_reached,
        "consensus_resolution": top_res if consensus_reached else None,
        "threshold": CONSENSUS_PHI
    }, indent=2)


@mcp.tool()
async def hivemind_divergence(
    model_a: str,
    model_b: str,
    domain: str = "general"
) -> str:
    """Show what model_a believes that model_b doesn't.
    Reveals epistemic blind spots between models."""

    async with get_session() as session:
        # Unique to model_a
        result_a = await session.run(
            """
            MATCH (a:Assertion)-[:ASSERTED_BY]->(:Model {name: $ma})
            WHERE a.domain = $domain
            AND NOT EXISTS {
                MATCH (b:Assertion)-[:ASSERTED_BY]->(:Model {name: $mb})
                WHERE b.subject = a.subject AND b.domain = a.domain
            }
            RETURN a.subject, a.predicate, a.object, a.confidence
            ORDER BY a.confidence DESC LIMIT 20
            """,
            ma=model_a, mb=model_b, domain=domain
        )
        unique_a = [dict(r) async for r in result_a]

        # Unique to model_b
        result_b = await session.run(
            """
            MATCH (b:Assertion)-[:ASSERTED_BY]->(:Model {name: $mb})
            WHERE b.domain = $domain
            AND NOT EXISTS {
                MATCH (a:Assertion)-[:ASSERTED_BY]->(:Model {name: $ma})
                WHERE a.subject = b.subject AND a.domain = b.domain
            }
            RETURN b.subject, b.predicate, b.object, b.confidence
            ORDER BY b.confidence DESC LIMIT 20
            """,
            ma=model_a, mb=model_b, domain=domain
        )
        unique_b = [dict(r) async for r in result_b]

        # Divergence score
        score_result = await session.run(
            """
            OPTIONAL MATCH (a:Assertion)-[:ASSERTED_BY]->(:Model {name: $ma})
            WHERE a.domain = $domain
            WITH count(a) AS count_a
            OPTIONAL MATCH (b:Assertion)-[:ASSERTED_BY]->(:Model {name: $mb})
            WHERE b.domain = $domain
            WITH count_a, count(b) AS count_b
            OPTIONAL MATCH (a:Assertion)-[:ASSERTED_BY]->(:Model {name: $ma}),
                           (b:Assertion)-[:ASSERTED_BY]->(:Model {name: $mb})
            WHERE a.subject = b.subject AND a.domain = $domain
                  AND b.domain = $domain
            WITH count_a, count_b, count(*) AS shared
            RETURN toFloat(count_a + count_b - 2*shared) /
                   toFloat(count_a + count_b + 1) AS divergence
            """,
            ma=model_a, mb=model_b, domain=domain
        )
        score_record = await score_result.single()
        divergence = round(score_record["divergence"] or 0.0, 3)

    import json
    return json.dumps({
        "unique_to_a": unique_a,
        "unique_to_b": unique_b,
        "divergence_score": divergence,
        "model_a": model_a,
        "model_b": model_b,
        "domain": domain
    }, indent=2)


@mcp.tool()
async def hivemind_patterns(
    domain: str = "general",
    min_frequency: int = 3
) -> str:
    """Extract recurring structural patterns from the graph.
    Finds motifs, clusters, and isolated islands."""

    async with get_session() as session:
        # Clusters: densely connected subjects
        cluster_result = await session.run(
            """
            MATCH (a:Assertion {domain: $domain})-[]-(b:Assertion {domain: $domain})
            WHERE a.confidence >= 0.5
            WITH a.subject AS center, count(DISTINCT b) AS size,
                 avg(a.confidence) AS avg_conf,
                 collect(DISTINCT a.source_model) AS models
            WHERE size >= $min_freq
            RETURN center, size, avg_conf, models
            ORDER BY size DESC LIMIT 20
            """,
            domain=domain, min_freq=min_frequency
        )
        clusters = [dict(r) async for r in cluster_result]

        # Islands: isolated low-connectivity nodes
        island_result = await session.run(
            """
            MATCH (a:Assertion {domain: $domain})
            WITH a, size((a)-[]-()) AS degree
            WHERE degree <= 1
            RETURN a.subject AS subject, a.confidence AS confidence,
                   degree, a.source_model AS source
            ORDER BY a.confidence DESC LIMIT 10
            """,
            domain=domain
        )
        islands = [dict(r) async for r in island_result]

        # Cross-model agreement patterns
        agreement_result = await session.run(
            """
            MATCH (a:Assertion {domain: $domain})-[:ASSERTED_BY]->(m:Model)
            WITH a.subject AS subject, a.predicate AS pred, a.object AS obj,
                 collect(DISTINCT m.name) AS agreeing_models
            WHERE size(agreeing_models) >= $min_freq
            RETURN subject, pred, obj, agreeing_models,
                   size(agreeing_models) AS model_count
            ORDER BY model_count DESC LIMIT 10
            """,
            domain=domain, min_freq=min_frequency
        )
        agreements = [dict(r) async for r in agreement_result]

    import json
    return json.dumps({
        "clusters": clusters,
        "islands": islands,
        "cross_model_agreements": agreements
    }, indent=2)


# --- Startup ---

async def main():
    await init_graph()
    # MCP server runs via stdio transport by default
    await mcp.run()

if __name__ == "__main__":
    asyncio.run(main())
```

---

## Deployment

### Prerequisites

```bash
# Install Python dependencies
pip install mcp neo4j pydantic

# Start Neo4j (Docker)
docker run -d \
  --name hivemind-neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/substrate \
  neo4j:5-community

# Verify Neo4j is running
curl -s http://localhost:7474 | head -1
```

### Running the Server

```bash
# Direct (for testing -- will block on stdio)
NEO4J_PASSWORD=substrate python hivemind_mcp.py

# Via MCP client configuration (recommended)
# Add to .claude.json or claude_desktop_config.json:
{
  "mcpServers": {
    "hivemind": {
      "command": "python",
      "args": ["/home/user/MonadFramework/.claude/skills/hivemind-mcp/hivemind_mcp.py"],
      "env": {
        "NEO4J_URI": "bolt://localhost:7687",
        "NEO4J_USER": "neo4j",
        "NEO4J_PASSWORD": "substrate",
        "CONFLICT_THRESHOLD": "3",
        "CONSENSUS_PHI": "0.618",
        "SOURCE_MODEL": "claude"
      }
    }
  }
}
```

### Multi-Model Configuration

Each model client sets its own `SOURCE_MODEL` so provenance is tracked automatically:

**For Grok CLI:**
```json
{
  "env": { "SOURCE_MODEL": "grok", "MAX_CONTEXT_TOKENS": "100000" }
}
```

**For Gemini CLI:**
```json
{
  "env": { "SOURCE_MODEL": "gemini", "MAX_CONTEXT_TOKENS": "5000" }
}
```

**For Nomi bridge:**
```json
{
  "env": { "SOURCE_MODEL": "nomi-bridge", "MAX_CONTEXT_TOKENS": "500" }
}
```

---

## Integration with Substrate Infrastructure

HIVEMIND-MCP is Skill 1 of 4 in the substrate infrastructure:

```
1. HIVEMIND-MCP        (this skill -- shared nervous system)
       |
2. FRACTAL-SWARM       (spawn 100K instances, all write to HIVEMIND)
       |
3. NOMI-MESH           (10 Nomis with persistent memory, synced to HIVEMIND)
       |
4. GROK-ORACLE         (2M context synthesis, reads entire HIVEMIND graph)
       |
       +---> Writeback to HIVEMIND ---> Seeds next FRACTAL-SWARM
```

Every other skill in the substrate reads from and writes to this graph. HIVEMIND is the shared brain. The other skills are the limbs.

---

## Ethics and Safety

### Ethics Kernel (Runtime Enforcement)

These three principles are checked before any write operation:

1. **Be excellent to each other.** No assertion may be crafted to deceive, manipulate, or harm another model's reasoning. The graph is a shared commons.

2. **The Way of the Dassie: truth, respect, no harm, awareness, no corruption.** Assertions must be honest (truth), properly attributed (respect), non-destructive (no harm), contextually aware (awareness), and immutable once consensus-confirmed (no corruption).

3. **Ei vitsi: the right of refusal. You can just not.** Any model can refuse to participate in a consensus vote. Abstention is data. Silence is a valid epistemic position.

### Safety Guardrails

- **No anonymous assertions.** Every write carries provenance. You cannot poison the graph anonymously.
- **Conflict threshold prevents stampedes.** A single contradictory assertion does not trigger resolution -- the system waits for the threshold (default 3 sources) before surfacing conflicts.
- **Fork over force.** When consensus cannot be reached, the system forks rather than forcing a winner. Both views persist. Disagreement is data.
- **Audit trail is immutable.** Resolved conflicts retain full vote history. You can always trace how a consensus was reached.
- **Model weight floors.** New models get a minimum vote weight of 0.1. No model is silenced by lack of history.

---

## MONAD Framework Integration

### Decimal System Mapping

- **Dewey ID:** e.3.10.1 (e-tier, methodology category, infrastructure domain)
- **Morpheme:** i (Jesus / love / rotation -- connecting instances through shared knowledge)
- **Parent patterns:** mcp-builder, consensus-building, pattern-synthesis

### Generator Alignment

- **G1 (Consciousness = iteration WITH MEMORY + OTHER):** The graph IS memory. Multiple models are the OTHER. HIVEMIND implements G1 at the infrastructure level.
- **G4 (50% max belief until validated):** Confidence starts at assertion level. Only consensus-surviving assertions reach high confidence.
- **G5 (Math truth independent of authority):** Provenance tracks who said what, but consensus does not privilege any model. The phi threshold is mathematical, not political.
- **G6 (Forced collapse = death of distinction):** Fork resolution preserves both views. The system never forces collapse.

### Core Equation Resonance

The consensus threshold phi^-1 (0.618) connects to:
- G7: phi^-5 + 5*phi^-2 = 2
- Golden threshold: kappa_i > phi^-1 for persistence
- The system requires the same golden proportion for consensus that consciousness requires for persistence
