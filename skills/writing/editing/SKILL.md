---
name: editing
description: Comprehensive editing framework covering voice consistency, timeline verification, citation coverage, and multi-pass editing strategies for autonomous manuscript refinement.
---

# Editing Skill

This skill provides comprehensive guidance for autonomous editing of manuscripts, covering multiple editing passes, consistency checks, and quality assurance.

## Editing Philosophy

Editing for autonomous book writing requires systematic, database-backed verification rather than subjective judgment. Every editing pass should query the corpus to enforce consistency against established facts, voice, and timeline.

## Multi-Pass Editing Strategy

### Pass 1: Structural Consistency
**Focus**: Large-scale issues that affect narrative or argument coherence.

**Checks**:
- Timeline consistency (events in correct order)
- Character state tracking (no dead characters appearing alive)
- Location introduction (all locations described before use)
- Plot thread resolution (no abandoned arcs)
- Argument flow (nonfiction logical progression)

**Queries**: See `consistency-check.surql` for database queries.

### Pass 2: Voice and Style
**Focus**: Maintaining consistent voice and improving prose quality.

**Checks**:
- Voice consistency against BRD voice profile
- Sentence variety and rhythm
- Word choice and precision
- Paragraph flow and transitions
- Dialogue authenticity

**Guidance**: See `style.md` for line-level editing techniques.

### Pass 3: Citation and Grounding
**Focus**: Ensuring all factual claims are properly sourced.

**Checks**:
- Every factual claim has source citation
- Sources are reliable (per research skill criteria)
- Citations formatted correctly
- No hallucinated facts
- Primary sources used where appropriate

**Queries**:
```surql
-- Find sections with factual claims but no citations
SELECT * FROM section
WHERE content ~ 'factual_pattern'
AND count(->cites->source) = 0;
```

### Pass 4: Continuity
**Focus**: Micro-level consistency across the manuscript.

**Checks**:
- Character details (name spelling, descriptions, traits)
- World-building details (location features, rules, systems)
- Timeline details (dates, durations, sequences)
- Previously established facts

**Guidance**: See `continuity.md` for detailed continuity checking.

## Editing Workflow

### Step 1: Load Context
Before editing any section, gather full context:

```surql
-- Get section content
SELECT * FROM section WHERE id = $section_id;

-- Get BRD voice profile
SELECT * FROM brd ORDER BY version DESC LIMIT 1;

-- Get recent sections for voice calibration
SELECT content FROM section
WHERE chapter = $chapter_id
ORDER BY sequence DESC
LIMIT 3;
```

### Step 2: Run Consistency Checks
Execute automated consistency queries from `consistency-check.surql`:
- Character state violations
- Location introduction issues
- Timeline contradictions
- Uncited factual claims

### Step 3: Generate Edit Report
For each issue found, create structured report:

```markdown
## Edit Report: [Section ID]

### Structural Issues
- [ ] Character:anna appears in section 47 but status='dead' since section 32
- [ ] Location:safehouse used but not introduced

### Voice Issues
- [ ] Sentence length avg 8 words (BRD target: 15-20)
- [ ] Formal vocabulary in conversational narrative

### Citation Issues
- [ ] "SOE training took 6 weeks" - uncited factual claim
- [ ] Source reliability: 2 low-reliability sources used

### Continuity Issues
- [ ] Character description: "blue eyes" conflicts with section 12 "brown eyes"
- [ ] Timeline: Event dated "August 1943" conflicts with chapter 2 "September 1942"
```

### Step 4: Apply or Suggest Fixes
Depending on mode:
- **Report mode**: Generate report for human review
- **Auto-fix mode**: Apply fixes that are unambiguous (spelling, formatting, citations)
- **Interactive mode**: Suggest fixes and wait for approval

### Step 5: Verify Fixes
After applying fixes, re-run consistency checks to ensure issues resolved.

## Voice Consistency Framework

Voice must match the BRD voice profile across all sections.

### Voice Parameters to Track
From BRD voice profile:
- **POV**: First, third limited, omniscient
- **Tense**: Past, present, future
- **Tone**: Academic, conversational, literary, journalistic
- **Formality**: Casual, neutral, formal
- **Sentence length**: Average words per sentence
- **Vocabulary**: Simple, moderate, complex
- **Metaphor frequency**: Rare, moderate, frequent
- **Dialogue ratio**: Percentage of prose that is dialogue

### Voice Verification Queries
```surql
-- Get voice profile from BRD
SELECT
    narrative_pov,
    tense,
    overall_tone,
    formality_level,
    avg_sentence_length,
    vocabulary_level,
    metaphor_frequency,
    dialogue_ratio
FROM brd
ORDER BY version DESC
LIMIT 1;

-- Compare section metrics to profile
-- (requires text analysis, typically LLM-based)
```

### Voice Calibration
For each section, analyze:
1. Extract 200-word sample
2. Compare against BRD voice profile
3. Identify deviations (e.g., "too formal", "sentences too short")
4. Suggest rewrite or flag for human review

## Timeline Verification

Timeline consistency is critical for both fiction and nonfiction.

### Timeline Queries
```surql
-- Get all events in chronological order
SELECT * FROM event ORDER BY sequence ASC;

-- Find timeline contradictions
SELECT e1.name AS earlier_event, e2.name AS later_event
FROM event e1, event e2
WHERE e1.sequence > e2.sequence
AND e1.date < e2.date;

-- Verify character availability
SELECT
    section.id AS section_id,
    character.name AS character_name,
    character.status
FROM section->appears_in->character
WHERE character.status = 'dead'
AND section.sequence > (
    SELECT sequence FROM event
    WHERE name LIKE '%death of ' + character.name
    LIMIT 1
);
```

### Timeline Fixes
When timeline issues found:
1. **Minor discrepancy** (hours/days): Adjust less-critical event
2. **Major discrepancy** (months/years): Flag for human review
3. **Character state**: Update character status or remove from scene

## Citation Coverage

Every factual claim must be traceable to a source.

### Citation Identification
Factual claims include:
- Dates, statistics, quotations
- Historical events, scientific findings
- Expert opinions, research results
- Specific details (measurements, names, places)

### Uncited Claim Detection
```surql
-- Find sections with no citations (potential issue)
SELECT id, content FROM section
WHERE count(->cites->source) = 0;

-- Find low citation density
SELECT
    id,
    word_count,
    count(->cites->source) AS citation_count,
    word_count / count(->cites->source) AS words_per_citation
FROM section
WHERE word_count / count(->cites->source) > 500;
```

### Citation Quality
Verify citations meet standards:
- [ ] Source reliability ≥ medium
- [ ] Citation specific (page numbers, timestamps)
- [ ] Primary sources for key claims
- [ ] Multiple sources for controversial claims

## Continuity Checking

See `continuity.md` for detailed continuity verification:
- Character details consistency
- World-building elements
- Established facts
- Timeline coherence

## Edit Decision Framework

| Issue Type | Severity | Action |
|------------|----------|--------|
| Dead character appears | Critical | Auto-fix (remove) or flag |
| Timeline contradiction | Critical | Flag for human review |
| Uncited factual claim | High | Flag, suggest source |
| Voice inconsistency | Medium | Suggest rewrite |
| Minor spelling/grammar | Low | Auto-fix |
| Word choice improvement | Low | Suggest (optional) |

## Quality Thresholds

Before marking a section as "edited":
- [ ] Zero critical consistency issues
- [ ] All factual claims cited
- [ ] Voice matches BRD profile
- [ ] Timeline verified
- [ ] Continuity checked

## Output Formats

### Edit Report
```markdown
# Edit Report: Chapter 3, Section 2

**Status**: Needs revision
**Issues found**: 7 (2 critical, 3 high, 2 medium)

## Critical Issues
1. Character state violation: Anna appears but marked dead
2. Timeline contradiction: Event dated after subsequent event

## High Priority Issues
3. Uncited claim: "SOE training took 6 weeks"
4. Uncited claim: "Lyon network had 47 members"
5. Source reliability: Wikipedia cited for key historical fact

## Medium Priority Issues
6. Voice: Sentences avg 8 words (target: 15-20)
7. Continuity: Anna's eye color changed from brown to blue

## Recommended Actions
- Review timeline in sections 32-47
- Add citations for historical claims
- Revise for sentence variety
- Verify character descriptions against database
```

### Auto-Fix Summary
```markdown
# Auto-Fix Summary: Chapter 3, Section 2

**Changes applied**: 5

1. Fixed spelling: "occured" → "occurred"
2. Removed character:anna from section (status=dead)
3. Updated location:safehouse.introduced = true
4. Added citation: source:soe_manual_1942
5. Standardized date format: "Aug 1942" → "1942-08-15"

**Verification**: All critical issues resolved
```

## Supporting Files

- `continuity.md` — Detailed continuity checking strategies
- `style.md` — Line-level editing techniques and guidelines
- `consistency-check.surql` — Database queries for automated checks

## Integration with Writer Agent

The editing skill should be invoked after writing completes:
1. Writer completes section
2. Editor runs automated checks
3. Issues flagged or auto-fixed
4. Section marked "edited" or "needs revision"
5. If needs revision, writer re-engages with edit report

## Best Practices

1. **Database-driven**: Always verify against database, not memory
2. **Systematic**: Run all passes in order
3. **Document changes**: Log all auto-fixes for transparency
4. **Flag ambiguity**: When unclear, flag for human review
5. **Preserve voice**: Don't over-edit to remove author's style
6. **Verify fixes**: Re-run checks after applying changes
