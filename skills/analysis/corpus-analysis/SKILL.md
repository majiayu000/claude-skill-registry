---
name: corpus-analysis
description: Gap detection and knowledge mapping techniques for comparing BRD requirements against corpus coverage. Includes SurrealQL queries for analyzing sources, entities, and topic coverage, plus prioritization frameworks for research task generation.
---

# Corpus Analysis and Gap Detection

This skill provides methods for analyzing corpus coverage, detecting knowledge gaps, and generating prioritized research tasks.

## Coverage Analysis Methods

### 1. Source Distribution Analysis

Analyze how research sources map to planned chapters/sections.

**Questions to ask**:
- Which chapters have the most/least source support?
- Are sources evenly distributed or clustered?
- Which topics have only one source (single point of failure)?

**SurrealQL query**:
```surql
-- Count sources per chapter
SELECT chapter, count() as source_count
FROM section->cites->source
GROUP BY chapter
ORDER BY source_count DESC;
```

### 2. Entity Coverage Analysis

Identify which characters, locations, concepts, events are well-documented vs underrepresented.

**Questions to ask**:
- Which entities appear in only one source?
- Which entities lack descriptive detail?
- Which relationships are missing supporting evidence?

**SurrealQL queries**:
```surql
-- Entity mention frequency
SELECT name, count(<-supports<-source) as source_count
FROM concept
ORDER BY source_count ASC;

-- Characters with sparse descriptions
SELECT name, description, count(<-appears_in<-section) as appearances
FROM character
WHERE length(description) < 100
ORDER BY appearances DESC;

-- Locations not yet introduced
SELECT name, description
FROM location
WHERE introduced = false;
```

### 3. Topic Coverage Analysis

Map topics from BRD against corpus to find coverage gaps.

**Questions to ask**:
- Which BRD topics have zero corpus representation?
- Which plot points lack factual grounding?
- For nonfiction: which thesis components lack evidence?

**SurrealQL queries**:
```surql
-- Topics mentioned in sources
SELECT name, count() as mentions
FROM concept<-related_to<-source
GROUP BY name
ORDER BY mentions DESC;

-- Timeline gaps (missing events)
SELECT * FROM event
ORDER BY sequence;

-- Uncited knowledge gaps
SELECT question, context, created_at
FROM knowledge_gap
WHERE resolved = false
ORDER BY created_at ASC;
```

### 4. Source Quality Analysis

Evaluate reliability distribution across the corpus.

**Questions to ask**:
- What percentage of sources are high reliability?
- Are critical claims supported by high-quality sources?
- Which topics rely primarily on low-reliability sources?

**SurrealQL queries**:
```surql
-- Source reliability distribution
SELECT reliability, count() as count
FROM source
GROUP BY reliability
ORDER BY reliability DESC;

-- Sources by type
SELECT source_type, count() as count
FROM source
GROUP BY source_type;

-- Low-reliability sources supporting key concepts
SELECT
  <-supports<-source.title as source_title,
  <-supports<-source.reliability as reliability,
  name as concept
FROM concept
WHERE <-supports<-source.reliability IN ['low', 'very low'];
```

## Knowledge Gap Detection Patterns

### Pattern 1: BRD Requirements Without Corpus Support

**Method**: Compare BRD sections to corpus entities and sources.

**Steps**:
1. Extract key requirements from each BRD section
2. Query corpus for matching concepts, characters, locations
3. Flag requirements with zero or low matches

**Example**:
- BRD mentions "wireless operator training protocols at Beaulieu 1942"
- Query: `SELECT * FROM concept WHERE name CONTAINS 'wireless' OR name CONTAINS 'Beaulieu'`
- If no results: FLAG as high-priority gap

### Pattern 2: Shallow Coverage (Single Source)

**Method**: Identify topics mentioned in only one source.

**Why it matters**: Single-source claims are fragile and hard to verify.

**SurrealQL**:
```surql
-- Topics with only one supporting source
SELECT name, count(<-supports<-source) as source_count
FROM concept
WHERE count(<-supports<-source) = 1;
```

### Pattern 3: Missing Relationships

**Method**: Check for expected but missing graph edges.

**Examples**:
- Character mentioned but no `->knows->` relationships
- Location exists but never `->located_in->` any section
- Event with no `->precedes->` or `->follows->` temporal links

**SurrealQL**:
```surql
-- Characters with no relationships
SELECT name FROM character
WHERE count(->knows->character) = 0;

-- Events with no temporal ordering
SELECT name FROM event
WHERE count(->precedes->event) = 0
AND count(->follows->event) = 0;
```

### Pattern 4: Timeline Inconsistencies

**Method**: Detect chronological gaps or conflicts.

**SurrealQL**:
```surql
-- Events without dates
SELECT name, description
FROM event
WHERE date IS NONE;

-- Sequence gaps (e.g., 1, 2, 5, 6 — missing 3 and 4)
SELECT sequence FROM event
ORDER BY sequence;
```

### Pattern 5: Uncited Sections

**Method**: Find written sections without source citations.

**SurrealQL**:
```surql
-- Sections with no citations
SELECT * FROM section
WHERE count(->cites->source) = 0;
```

## Prioritization Framework

Use this framework to prioritize research tasks based on impact and urgency.

### High Priority (Blocks Multiple Sections)

**Criteria**:
- Gap affects 3+ planned chapters/sections
- Core to the BRD thesis/premise
- Required for major plot point or key argument
- Timeline-critical (early chapters need it)

**Examples**:
- "SOE training protocols" (affects multiple training scenes)
- "Lyon resistance network structure" (entire middle section depends on it)
- "Protagonist's historical timeline" (affects chronological consistency)

**Research task template**:
```
Priority: HIGH
Blocking: [list chapter/section IDs]
Query: [specific research question]
Context: [why this is needed, what we already know]
Success criteria: [what would resolve this gap]
```

### Medium Priority (Blocks One Section)

**Criteria**:
- Gap affects 1-2 sections
- Adds depth but isn't critical to plot/argument
- Can be worked around if research fails
- Later chapters (writing not imminent)

**Examples**:
- "Daily life details in Lyon 1943" (enriches setting but not critical)
- "German counter-intelligence methods" (adds realism to one scene)
- "Specific wireless equipment specs" (detail-level enhancement)

**Research task template**:
```
Priority: MEDIUM
Blocking: [section ID]
Query: [specific research question]
Fallback: [how to proceed if research fails]
```

### Low Priority (Nice to Have)

**Criteria**:
- Doesn't block any section
- Enhances detail or authenticity
- Can be added in editing pass
- Background/contextual knowledge

**Examples**:
- "Period-accurate slang terms"
- "Weather patterns in occupied France"
- "Secondary character backstory details"

**Research task template**:
```
Priority: LOW
Enhancement for: [section or theme]
Query: [research question]
```

## Research Task Generation Templates

### Template 1: Factual Gap

```markdown
**Task**: Research [specific topic]
**Priority**: [HIGH/MEDIUM/LOW]
**Blocks**: [chapter/section IDs]
**Context**:
- BRD requires: [what the BRD says]
- Corpus has: [what we currently know]
- Gap: [what's missing]

**Research questions**:
1. [Specific question 1]
2. [Specific question 2]

**Success criteria**:
- [ ] Found 2+ reliable sources on [topic]
- [ ] Extracted key facts: [list expected facts]
- [ ] Resolved knowledge_gap:[id]

**Search strategy**:
- Academic databases: [keywords]
- Primary sources: [archives, documents]
- Web search: [specific queries]
```

### Template 2: Character/Entity Gap

```markdown
**Task**: Research [character/entity name]
**Priority**: [HIGH/MEDIUM/LOW]
**Blocks**: [section IDs]
**Context**:
- Mentioned in: [where entity appears in BRD/outline]
- Current knowledge: [what corpus has]
- Needed: [missing details]

**Research questions**:
1. Background/history: [specifics]
2. Relationships: [who/what they connect to]
3. Timeline: [when they appear, key dates]

**Success criteria**:
- [ ] CREATE/UPDATE entity with full description
- [ ] Establish relationships via RELATE statements
- [ ] Add timeline anchors (dates, sequence)

**Sources to check**:
- [Specific books, archives, websites]
```

### Template 3: Thematic/Conceptual Gap

```markdown
**Task**: Research [theme/concept]
**Priority**: [HIGH/MEDIUM/LOW]
**Blocks**: [section IDs]
**Context**:
- BRD theme: [core theme/argument]
- Current support: [sources that touch on this]
- Gap: [missing evidence, examples, or depth]

**Research questions**:
1. [Theoretical/conceptual question]
2. [Evidence/example question]
3. [Counter-argument/complexity question]

**Success criteria**:
- [ ] Found diverse perspectives on [concept]
- [ ] Identified concrete examples/case studies
- [ ] Created concept entity with supporting sources

**Expected outcomes**:
- 3+ sources with varied reliability levels
- Clear link to BRD thesis
```

## SurrealQL Queries for Gap Analysis

### Comprehensive Coverage Report

```surql
-- Get overview of corpus completeness
LET $total_sources = (SELECT count() FROM source)[0].count;
LET $total_characters = (SELECT count() FROM character)[0].count;
LET $total_concepts = (SELECT count() FROM concept)[0].count;
LET $open_gaps = (SELECT count() FROM knowledge_gap WHERE resolved = false)[0].count;

RETURN {
  sources: $total_sources,
  characters: $total_characters,
  concepts: $total_concepts,
  open_gaps: $open_gaps,
  source_reliability: (SELECT reliability, count() as count FROM source GROUP BY reliability),
  chapters_with_citations: (SELECT chapter, count() as cites FROM section->cites->source GROUP BY chapter)
};
```

### Gap Detection by Section

```surql
-- Find sections with weak source support
SELECT
  id,
  chapter,
  sequence,
  count(->cites->source) as citation_count,
  word_count
FROM section
WHERE count(->cites->source) < 2
ORDER BY chapter, sequence;
```

### Entity Relationship Completeness

```surql
-- Characters without sufficient context
SELECT
  name,
  count(->knows->character) as relationships,
  count(<-appears_in<-section) as appearances,
  length(description) as desc_length
FROM character
WHERE count(->knows->character) = 0
   OR length(description) < 50
ORDER BY appearances DESC;
```

## Example Gap Detection Workflow

1. **Load BRD**: Read BRD requirements for next chapter
2. **Query corpus**: Run coverage analysis queries
3. **Identify gaps**: Compare BRD needs vs corpus results
4. **Prioritize**: Apply HIGH/MEDIUM/LOW framework
5. **Generate tasks**: Use templates to create research tasks
6. **Store gaps**: `CREATE knowledge_gap SET question=..., context=..., resolved=false`
7. **Report**: Summarize findings with specific task IDs

## Output Format

When performing corpus analysis, provide:

```markdown
## Corpus Analysis Report

### Coverage Summary
- Total sources: [count]
- Source reliability: [high: X, medium: Y, low: Z]
- Entities extracted: [characters: X, locations: Y, events: Z]
- Open knowledge gaps: [count]

### Gaps by Priority

#### High Priority (Blocking)
1. [Gap description] — Blocks: [sections] — Research: [topic]
2. ...

#### Medium Priority
1. [Gap description] — Blocks: [sections] — Research: [topic]
2. ...

#### Low Priority
1. [Gap description] — Enhancement for: [context]
2. ...

### Recommended Next Action
[Research these high-priority gaps / Continue to plan-write / etc.]
```
