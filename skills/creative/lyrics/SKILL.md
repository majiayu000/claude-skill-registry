---
name: amcs-lyrics-generator
description: Generate song lyrics with citations from pinned sources. Enforces rhyme scheme, meter, syllable counts, hook strategy, and profanity filter while retrieving from MCP sources with deterministic hash-based pinning. Use when creating lyrics with structural constraints, source attribution, and policy compliance.
---

# AMCS Lyrics Generator

Produces complete song lyrics that satisfy structural, stylistic, and policy constraints while maintaining full source provenance through hash-pinned retrieval.

## When to Use

Invoke this skill after PLAN and STYLE generation to create lyrics. Runs in parallel with PRODUCER node and feeds into COMPOSE.

## Input Contract

```yaml
inputs:
  - name: sds_lyrics
    type: amcs://schemas/lyrics-1.0.json
    required: true
    description: Lyrics entity from SDS with constraints and preferences
  - name: plan
    type: amcs://schemas/plan-1.0.json
    required: true
    description: Section order and target word counts
  - name: style
    type: amcs://schemas/style-1.0.json
    required: true
    description: Musical style for thematic alignment
  - name: sources
    type: array[amcs://schemas/source-1.0.json]
    required: false
    description: External knowledge sources for retrieval
  - name: blueprint
    type: amcs://schemas/blueprint-1.0.json
    required: true
    description: Genre-specific lyrical patterns and lexicon
  - name: seed
    type: integer
    required: true
    description: Determinism seed (use seed+2 for this node)
```

## Output Contract

```yaml
outputs:
  - name: lyrics
    type: string
    description: Complete lyrics text with section markers
  - name: citations
    type: array[citation]
    description: |
      Source chunks used with provenance:
      - chunk_hash: SHA-256 of source text
      - source_id: UUID of source
      - text: Actual source snippet
      - weight: Influence weight (0-1)
  - name: metrics
    type: object
    description: |
      Quality metrics:
      - rhyme_tightness: 0-1 score
      - singability: 0-1 score (syllable consistency)
      - hook_density: count per section
```

## Determinism Requirements

- **Seed**: `run_seed + 2` for LLM generation and retrieval tie-breaking
- **Temperature**: 0.3 for lyrics generation
- **Top-p**: 0.85
- **Retrieval**: Deterministic source chunk selection:
  - Fixed top-k (k=5 per source)
  - Sort by chunk_hash lexicographically for tie-breaking
  - Store all chunk hashes in citations
- **Hashing**: Hash every source chunk (SHA-256) for pinned retrieval

## Constraints & Policies

- Section order MUST match `plan.section_order`
- Total lines MUST NOT exceed `sds_lyrics.constraints.max_lines`
- Each section MUST satisfy `section_requirements` (min/max lines, must_end_with_hook)
- Rhyme scheme MUST match `sds_lyrics.rhyme_scheme` (e.g., AABB, ABAB)
- Syllable count per line MUST be within ±2 of `sds_lyrics.syllables_per_line`
- Profanity filter MUST enforce `sds_lyrics.constraints.explicit`:
  - If false, replace profanity with [[REDACTED]] or safe alternatives
  - If true, allow explicit content but score it in metrics
- Hook strategy MUST align with `sds_lyrics.hook_strategy`:
  - "chant": Repeat hook phrase ≥3 times in chorus
  - "lyrical": Strong memorable phrase, ≥2 occurrences
  - "melodic": Focus on singable phonetics
  - "call-response": Alternating lines
- Source citations MUST include ALL retrieved chunks with hashes

## Implementation Guidance

### Step 1: Prepare Source Retrieval (if sources provided)

1. For each source in `sources`:
   - Construct deterministic query from `style.mood + plan.section_order[0]`
   - Retrieve top-k=5 chunks from MCP source
   - Sort chunks by SHA-256 hash lexicographically (tie-breaking)
   - Store each chunk: `{chunk_hash, source_id, text}`
2. Apply source weights from `sds_lyrics.source_citations`
3. Store all chunks in citations array

### Step 2: Generate Section-by-Section

For each section in `plan.section_order`:

1. **Retrieve Section Constraints**:
   - Get `section_requirements[section]` for min/max lines
   - Get `target_word_counts[section]` from plan

2. **Build Context**:
   - Include style mood, energy, themes
   - Include relevant source chunks (prioritize by weight)
   - Include rhyme scheme and meter

3. **Generate Lyrics**:
   - Use LLM with seed `run_seed + 2 + section_index`
   - Temperature: 0.3
   - Enforce syllable target: `sds_lyrics.syllables_per_line` ± 2
   - Enforce rhyme scheme
   - If section is "Chorus" and `must_end_with_hook`, ensure last line is hook

4. **Apply Profanity Filter**:
   - If `explicit = false`, scan for profanity
   - Replace with [[REDACTED]] or safe synonym
   - Log replacements

5. **Store Section**:
   - Prepend section marker: `[Verse 1]`, `[Chorus]`, etc.
   - Append to complete lyrics text

### Step 3: Enforce Hook Strategy

1. If `hook_strategy = "chant"`:
   - Identify hook phrase (usually chorus last line)
   - Count occurrences across all chorus sections
   - Ensure ≥3 occurrences

2. If `hook_strategy = "lyrical"`:
   - Ensure at least 2 chorus sections contain identical hook line

3. If `hook_strategy = "call-response"`:
   - Alternate line structure in chorus sections

### Step 4: Calculate Metrics

1. **Rhyme Tightness**:
   - For each section, check line-end rhyme against scheme
   - Score: (matching_rhymes / expected_rhymes)

2. **Singability**:
   - For each line, count syllables
   - Score: 1 - (avg_deviation_from_target / target)

3. **Hook Density**:
   - Count hook occurrences per section
   - Store as `metrics.hook_density`

### Step 5: Validate and Return

1. Check total lines ≤ `max_lines`
2. Validate all section requirements met
3. Compute hash of complete lyrics text
4. Return `{lyrics, citations, metrics, _hash}`

## Examples

### Example 1: Christmas Pop with Family Source

**Input**:
```json
{
  "sds_lyrics": {
    "language": "en",
    "pov": "1st",
    "tense": "present",
    "rhyme_scheme": "AABB",
    "syllables_per_line": 8,
    "hook_strategy": "chant",
    "section_order": ["Intro", "Verse", "Chorus", "Verse", "Chorus"],
    "constraints": {
      "explicit": false,
      "max_lines": 40,
      "section_requirements": {
        "Chorus": {"min_lines": 6, "must_end_with_hook": true}
      }
    },
    "source_citations": [{"source_id": "family-doc-uuid", "weight": 0.8}]
  },
  "sources": [
    {
      "source_id": "family-doc-uuid",
      "chunks": [
        {"hash": "abc123", "text": "Our family gathers every Christmas Eve..."},
        {"hash": "abc456", "text": "The kids love decorating the tree together..."}
      ]
    }
  ],
  "seed": 44
}
```

**Output**:
```json
{
  "lyrics": "[Intro]\nSnowflakes falling, lights aglow\n\n[Verse]\nGathering 'round on Christmas Eve (8 syllables)\nThe kids decorate, we all believe (8 syllables)\n\n[Chorus]\nFamily time is what we need (8 syllables)\nLove and joy in every deed (8 syllables)\nSinging carols, feeling free (8 syllables)\nChristmas magic, you and me (8 syllables)\nFamily time is what we need (8 syllables - HOOK)\nLove and joy in every deed (8 syllables)\n\n[Verse]\n...\n\n[Chorus]\n...",
  "citations": [
    {
      "chunk_hash": "abc123",
      "source_id": "family-doc-uuid",
      "text": "Our family gathers every Christmas Eve...",
      "weight": 0.8
    },
    {
      "chunk_hash": "abc456",
      "source_id": "family-doc-uuid",
      "text": "The kids love decorating the tree together...",
      "weight": 0.8
    }
  ],
  "metrics": {
    "rhyme_tightness": 0.95,
    "singability": 0.88,
    "hook_density": 3
  },
  "_hash": "ghi789..."
}
```

## Common Pitfalls

1. **Missing Citations**: Not recording source chunk hashes breaks determinism
2. **Syllable Variance**: Exceeding ±2 syllable tolerance reduces singability
3. **Hook Absence**: Missing hooks in "chant" strategy fails validation
4. **Profanity Leak**: Not filtering when `explicit=false` violates policy
5. **Section Overflow**: Exceeding `max_lines` per section truncates lyrics
6. **Rhyme Scheme Break**: Not enforcing scheme reduces rhyme_tightness score
7. **Non-Deterministic Retrieval**: Not sorting chunks by hash causes variation across runs
