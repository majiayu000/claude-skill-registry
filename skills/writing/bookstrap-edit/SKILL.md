---
name: bookstrap-edit
description: Run editing passes over completed sections for voice consistency, timeline verification, contradiction flagging, and citation coverage
disable-model-invocation: true
allowed-tools: Bash, Read, Edit
---

# /bookstrap-edit - Run Editing Passes

Execute editing passes over completed sections to ensure voice consistency, timeline accuracy, factual correctness, and citation coverage. This command loads completed sections from the database, performs comprehensive consistency checks, and generates edit reports or applies fixes.

## Purpose

Review and polish written manuscript content through systematic editing passes. This command operates in **edit mode** where it analyzes completed sections against BRD requirements, verifies timeline consistency through graph queries, flags contradictions, checks citation coverage, and suggests line-level improvements.

This command delegates the editing work to the `editor` agent, which operates with read-only database access and focuses on consistency and quality checking.

## Input Arguments

None. This command reads completed sections from the database:
- Sections with status 'draft' or 'complete'
- Associated entities and relationships
- Timeline and sequence information
- Citation links to sources
- BRD voice specifications

## Processing Workflow

### 1. Load Completed Sections

Query the database to retrieve completed sections for editing:

```bash
# Query completed sections ready for editing
surreal sql --conn http://localhost:2665 \
  --user root --pass root \
  --ns bookstrap --db <database-name> \
  --query "SELECT * FROM section WHERE status IN ['draft', 'complete'] ORDER BY chapter ASC, sequence ASC;"
```

Filter and prioritize:
- Sections marked as 'draft' (first editing pass)
- Sections marked for review after revisions
- Sequential order within chapters (chapter ASC, sequence ASC)
- Include all associated metadata (entities, citations, relationships)

### 2. Load BRD Specifications

Retrieve BRD to establish editing criteria:

```surql
-- Load BRD for voice and style reference
SELECT * FROM brd ORDER BY version DESC LIMIT 1;
```

Extract from BRD:
- **Voice specifications**: Tone, formality, comparable titles
- **Genre requirements**: Conventions and expectations
- **Target audience**: Reading level and expectations
- **Constraints**: Must include, must avoid, sensitivity
- **Sample passages**: Voice reference examples

### 3. For Each Section

Execute editing checks on each section in sequence.

#### 3.1 Check Voice Consistency Against BRD

Verify the section matches BRD voice specifications:

**Voice Analysis**:
- Compare tone to BRD voice description
- Check formality level matches target audience
- Verify sentence structure aligns with comparable titles
- Assess word choice for genre appropriateness
- Identify voice drift from established patterns

**Consistency Checks**:
```surql
-- Get other sections for voice comparison
SELECT content FROM section
WHERE status = 'complete'
AND chapter < $current_chapter
ORDER BY sequence DESC
LIMIT 5;
```

**Output**: Voice consistency score, flagged deviations, suggested revisions

#### 3.2 Verify Timeline via Graph Queries

Ensure chronological consistency through database queries:

**Timeline Consistency Checks**:

```surql
-- Character state violations (appearing after death)
SELECT * FROM section
WHERE ->appears_in->character.status = 'dead'
AND sequence > (SELECT death_sequence FROM character WHERE ->appears_in->section = $section_id);

-- Location not introduced before use
SELECT * FROM section
WHERE ->located_in->location.introduced = false
OR ->located_in->location.introduced_in.sequence > $current_sequence;

-- Event sequence contradictions
SELECT * FROM event AS e1, event AS e2
WHERE e1.sequence > e2.sequence
AND e1.date < e2.date;

-- Timeline ordering violations
SELECT * FROM section AS s1, section AS s2
WHERE s1.sequence < s2.sequence
AND s1->contains->event.date > s2->contains->event.date;
```

**Character Timeline Verification**:
```surql
-- Track character state across sections
SELECT
  s.sequence,
  s.content,
  c.status,
  c.introduced_in.sequence AS first_appearance,
  c.death_sequence
FROM section s
WHERE s->appears_in->character = $character_id
ORDER BY s.sequence;
```

**Output**: Timeline violations, contradictions, recommended fixes

#### 3.3 Flag Factual Contradictions

Identify conflicting claims within the manuscript:

**Contradiction Detection**:

```surql
-- Uncited factual claims (potential hallucinations)
SELECT * FROM section
WHERE content REGEXP '(according to|research shows|studies indicate|historians note)'
AND count(->cites->source) = 0;

-- Conflicting facts across sections
SELECT
  s1.content AS claim_1,
  s2.content AS claim_2,
  s1.sequence AS sequence_1,
  s2.sequence AS sequence_2
FROM section s1, section s2
WHERE s1.embedding <|0.95|> s2.embedding
AND s1.id != s2.id
AND s1.chapter = s2.chapter;
```

**Entity Consistency**:
```surql
-- Character description contradictions
SELECT
  c.name,
  c.description,
  s.content,
  s.sequence
FROM character c, section s
WHERE c->appears_in->s
AND s.content NOT LIKE '%' + c.description + '%'
ORDER BY c.name, s.sequence;

-- Location description contradictions
SELECT
  l.name,
  l.description,
  s.content,
  s.sequence
FROM location l, section s
WHERE s->located_in->l
ORDER BY l.name, s.sequence;
```

**Output**: Identified contradictions, severity rating, suggested resolutions

#### 3.4 Check Citation Coverage

Verify all factual claims are properly sourced:

**Citation Analysis**:

```surql
-- Sections with low citation coverage
SELECT
  s.id,
  s.chapter,
  s.sequence,
  s.word_count,
  count(s->cites->source) AS citation_count,
  (count(s->cites->source) * 1000.0 / s.word_count) AS citations_per_1000_words
FROM section s
WHERE s.status IN ['draft', 'complete']
GROUP BY s.id
HAVING citations_per_1000_words < 2.0
ORDER BY citations_per_1000_words ASC;

-- Source reliability check
SELECT
  s.id,
  s.sequence,
  src.title,
  src.reliability,
  src.source_type
FROM section s, source src
WHERE s->cites->src
AND src.reliability = 'low'
ORDER BY s.sequence;

-- Orphaned claims (factual statements without sources)
SELECT * FROM section
WHERE content REGEXP '(was|were|had|did|said|reported|confirmed|discovered|found)'
AND count(->cites->source) = 0;
```

**Coverage Metrics**:
- Citations per 1,000 words
- Percentage of factual claims cited
- Source reliability distribution
- Primary vs. secondary source ratio

**Output**: Citation gaps, under-sourced sections, reliability warnings

#### 3.5 Suggest Line-Level Improvements

Generate specific editorial suggestions:

**Editorial Checks**:
- **Clarity**: Identify unclear or ambiguous phrasing
- **Conciseness**: Flag verbose or redundant passages
- **Pacing**: Detect pacing issues (genre-specific)
- **Dialogue**: Check naturalistic dialogue patterns
- **Show vs. Tell**: Identify telling that should be showing
- **Active Voice**: Flag excessive passive voice
- **Repetition**: Detect word or phrase repetition
- **Transitions**: Verify smooth transitions between sections

**Genre-Specific Checks**:
```surql
-- Load genre requirements from BRD
SELECT genre FROM brd ORDER BY version DESC LIMIT 1;

-- Apply genre-specific patterns
-- For thriller: pacing, tension escalation, reveals
-- For historical: period accuracy, anachronism detection
-- For memoir: authenticity, narrative balance
-- For technical: clarity, example coverage
```

**Voice Consistency**:
- Compare word choice to BRD sample passages
- Check sentence length variation
- Verify tone consistency
- Assess formality level

**Output**: Line-by-line suggestions, severity (minor/major), recommended edits

### 4. Generate Edit Report

Compile comprehensive edit report for each section:

**Report Structure**:

```markdown
# Edit Report: Chapter {N}, Section {M}

## Section Metadata
- Title: {section_title}
- Sequence: chapter-{N}-section-{M}
- Word Count: {word_count}
- Status: {status}
- Citations: {citation_count}

## Voice Consistency
Score: {score}/10
- Tone: {matches|deviates} from BRD
- Formality: {appropriate|too formal|too casual}
- Comparable to: {similar_titles}
- Deviations: {list}

## Timeline Verification
Status: {pass|warnings|violations}
- Character states: {pass|fail}
- Location introductions: {pass|fail}
- Event sequences: {pass|fail}
- Chronological order: {pass|fail}

Violations:
- {violation_description}

## Factual Contradictions
Status: {clean|warnings|errors}
- Internal contradictions: {count}
- Entity inconsistencies: {count}
- Uncited claims: {count}

Details:
- {contradiction_description}

## Citation Coverage
Score: {citations_per_1000_words} citations/1000 words
- Total citations: {count}
- Source reliability: {high|medium|low}
- Coverage: {adequate|insufficient}

Gaps:
- {uncited_claim_description}

## Line-Level Suggestions
Count: {suggestion_count}

### Major Issues
1. {suggestion_with_severity_major}

### Minor Issues
1. {suggestion_with_severity_minor}

## Recommendations
- {actionable_recommendation}

## Summary
Overall Quality: {excellent|good|needs_work|major_issues}
Ready for Publish: {yes|no}
```

Save report to database:
```surql
CREATE edit_report SET
  section = $section_id,
  voice_score = $voice_score,
  timeline_status = $timeline_status,
  contradiction_count = $contradiction_count,
  citation_coverage = $citation_coverage,
  suggestions = $suggestions,
  overall_quality = $overall_quality,
  ready_for_publish = $ready_for_publish,
  created_at = time::now();
```

### 5. Delegate to Editor Agent

Invoke the `editor` agent to perform detailed editing analysis:

```bash
# Load editor agent with context
# Agent will:
# 1. Load next section for editing
# 2. Retrieve BRD voice specifications
# 3. Run voice consistency checks
# 4. Execute timeline verification queries
# 5. Detect factual contradictions
# 6. Analyze citation coverage
# 7. Generate line-level suggestions
# 8. Compile edit report
# 9. Store report in database
# 10. Continue to next section or exit when complete
```

The editor agent has read-only database access, NO web access, and uses the `editing`, `surrealdb`, and `writing` skills.

### 6. Continue Until All Sections Reviewed

The editor agent continues processing sections until:
- **All sections reviewed**: Complete editing pass
- **Major issues found**: Pause for human review
- **Database error**: Cannot query or store results
- **BRD missing**: Cannot establish voice baseline

## Output Format

Report editing progress to the user:

```
EDITING EXECUTION
=================

Configuration:
- Database: bookstrap/my_book
- BRD version: 2
- Sections to review: 8
- Edit mode: comprehensive

SECTION 1/8: Chapter 1, Section 2
----------------------------------
Title: "The Training Begins"
Sequence: chapter-1-section-2
Word count: 1,250
Citations: 3

Voice Consistency:
  Score: 8.5/10
  → Tone matches BRD specifications
  → Formality appropriate for target audience
  → Minor deviation: sentence variety could improve

Timeline Verification:
  Status: PASS
  ✓ Character states: valid (anna: alive, introduced)
  ✓ Location: beaulieu_training_facility (introduced in ch1-sec1)
  ✓ Event sequence: consistent with timeline
  ✓ Chronological order: no contradictions

Factual Contradictions:
  Status: CLEAN
  ✓ No internal contradictions found
  ✓ Entity descriptions consistent
  ✓ All factual claims cited

Citation Coverage:
  Score: 2.4 citations/1000 words
  ✓ Adequate coverage for genre
  → 3 sources cited (2 primary, 1 secondary)
  → All sources rated 'high' reliability

Line-Level Suggestions:
  Minor (3):
    1. Line 12: Consider varying sentence structure
    2. Line 34: "very" is weak intensifier, suggest alternative
    3. Line 87: Repetition of "training" (3x in paragraph)

Overall Quality: GOOD
Ready for Publish: Yes (after minor revisions)

Report saved: edit_report:section-1-2

---

SECTION 2/8: Chapter 1, Section 3
----------------------------------
Title: "First Transmission"
Sequence: chapter-1-section-3
Word count: 1,480
Citations: 1

Voice Consistency:
  Score: 9.0/10
  → Excellent tone consistency
  → Pacing appropriate for thriller genre
  → Strong tension escalation

Timeline Verification:
  Status: WARNING
  ! Location issue detected
  → safehouse_alpha mentioned but not introduced
  → First mention in section-3, should be introduced in section-2
  Recommendation: Add location introduction in previous section

Factual Contradictions:
  Status: WARNING
  ! Potential contradiction detected
  → This section: "Anna used Morse code"
  → Previous section: "Wireless operators used one-time pads"
  → Clarify: Morse code + OTP encryption or just OTP?

Citation Coverage:
  Score: 0.7 citations/1000 words
  ✗ INSUFFICIENT for factual content
  → Only 1 source cited for technical details
  → Wireless protocol details uncited (requires source)
  → German counter-intelligence methods uncited

  Uncited claims:
    1. Line 45: "German direction-finding equipment..."
    2. Line 67: "Standard SOE transmission procedure..."
    3. Line 103: "Lyon's German garrison monitored..."

Line-Level Suggestions:
  Major (1):
    1. Line 45-52: Technical details need citation support

  Minor (2):
    1. Line 23: Dialogue tag redundant
    2. Line 89: Consider breaking long paragraph

Overall Quality: NEEDS WORK
Ready for Publish: No (citation gaps, location issue)

Report saved: edit_report:section-1-3
Action: Flagged for revision

---

PROGRESS SUMMARY
================

Sections reviewed: 8/8
Overall quality distribution:
  - Excellent: 2
  - Good: 4
  - Needs work: 2
  - Major issues: 0

Ready for publish: 6/8 (75%)
Sections flagged for revision: 2

ISSUES FOUND
------------

Voice Consistency:
  - Average score: 8.3/10
  - Deviations: 3 sections (minor)

Timeline Verification:
  - Status: 2 warnings, 0 violations
  - Character issues: 0
  - Location issues: 2
  - Event issues: 0

Factual Contradictions:
  - Total contradictions: 1
  - Entity inconsistencies: 0
  - Uncited claims: 12

Citation Coverage:
  - Average: 1.8 citations/1000 words
  - Target: 2.0 citations/1000 words
  - Under-cited sections: 3
  - Low-reliability sources: 0

Line-Level Suggestions:
  - Total suggestions: 24
  - Major issues: 3
  - Minor issues: 21

RECOMMENDATIONS
---------------

1. Address citation gaps in sections 1-3, 2-1, 2-3
   - Add source citations for technical claims
   - Find sources for German counter-intelligence details
   - Cite SOE training protocols

2. Fix location introduction issue in chapter 1
   - Introduce safehouse_alpha in section-2
   - Or adjust section-3 to remove early reference

3. Clarify Morse code vs. OTP contradiction
   - Verify historical accuracy
   - Ensure technical details consistent

4. Apply minor line-level suggestions
   - Sentence variety improvements
   - Dialogue tag cleanup
   - Paragraph break adjustments

NEXT STEPS
----------

Option 1: Review edit reports and apply fixes manually
  - Read edit reports in database
  - Revise flagged sections
  - Re-run /bookstrap-edit to verify

Option 2: Run research cycle for citation gaps
  - /bookstrap-plan-research (generate tasks for missing sources)
  - /bookstrap-research (find citation sources)
  - Re-run /bookstrap-edit to verify coverage

Option 3: Continue to next stage
  - /bookstrap-status (check overall progress)
  - /bookstrap-query (explore specific issues)
  - Export manuscript when ready

Time elapsed: 12 minutes
```

## Behavior Characteristics

### Edit Mode (Read-Only Analysis)

This command operates in **edit mode**:
- ✗ NO web access
- ✗ NO content modification (analysis only)
- ✓ Read-only database queries
- ✓ Generates reports and suggestions
- ✓ Flags issues for human review
- ✓ Comprehensive consistency checking

### Autonomous Execution

Runs fully autonomously:
- No human approval needed per section
- Processes sections sequentially (maintains context)
- Flags issues for review (doesn't auto-fix)
- Generates detailed reports
- Logs all detected issues
- Tracks quality metrics

### Quality Over Speed

Prioritizes thorough analysis:
- Multiple consistency checks per section
- Cross-reference with entire corpus
- Deep timeline verification via graph queries
- Citation reliability assessment
- Genre-specific convention checking
- Line-level detailed suggestions

## Configuration

Editing behavior configured in `bookstrap.config.json`:

```json
{
  "editing": {
    "voice_check": true,
    "timeline_verification": true,
    "contradiction_detection": true,
    "citation_check": true,
    "min_citations_per_1000_words": 2.0,
    "line_level_suggestions": true,
    "genre_conventions": true,
    "auto_fix": false
  },
  "git": {
    "auto_commit": false,
    "commit_after": null
  }
}
```

Settings:
- `voice_check`: Enable voice consistency analysis
- `timeline_verification`: Run timeline consistency queries
- `contradiction_detection`: Flag factual contradictions
- `citation_check`: Verify citation coverage
- `min_citations_per_1000_words`: Target citation density
- `line_level_suggestions`: Generate detailed editorial feedback
- `genre_conventions`: Apply genre-specific checks
- `auto_fix`: Apply fixes automatically (false = report only)

## Error Handling

| Error | Recovery |
|-------|----------|
| BRD not found | Abort, report error, cannot establish baseline |
| Section not found | Skip, continue to next |
| Database query fails | Retry up to 3 times, then skip check |
| Report storage fails | Log locally, continue processing |
| Graph query timeout | Use simplified query, note limitation |
| Missing metadata | Use defaults, flag incomplete data |

## Pre-requisites

Before running `/bookstrap-edit`:

1. **BRD created**: `/bookstrap-init` must have been run
2. **SurrealDB running**: Database must be accessible
3. **Sections written**: `/bookstrap-write` must have produced content
4. **Entities extracted**: Sections must have associated entities
5. **Citations linked**: Sections must have source relationships

## Related Commands

- `/bookstrap-write` - Write sections (run before editing)
- `/bookstrap-research` - Fill citation gaps (if editing finds uncited claims)
- `/bookstrap-query` - Explore specific issues found during editing
- `/bookstrap-status` - Monitor overall manuscript quality

## Supporting Agents

| Agent | Role |
|-------|------|
| `editor` | Executes editing checks, generates reports, flags issues |

## Supporting Skills

| Skill | Purpose |
|-------|---------|
| `editing/` | Core editing workflow, consistency checking, style guidelines |
| `editing/continuity.md` | Timeline and character consistency verification |
| `editing/style.md` | Line-level editing suggestions and voice analysis |
| `surrealdb/` | Database query patterns for consistency checks |
| `writing/` | Voice reference and citation standards |

## Supporting Scripts

| Script | Purpose |
|--------|---------|
| `scripts/consistency-check.surql` | Timeline and entity consistency queries |

## Example Usage

```bash
# After writing sections, run editing pass
/bookstrap-write
/bookstrap-edit

# Review edit reports
/bookstrap-query "Show edit reports with major issues"

# Fix citation gaps with research
/bookstrap-plan-research
/bookstrap-research

# Re-run editing to verify fixes
/bookstrap-edit

# Check overall quality
/bookstrap-status
```

## Integration with Workflow

This command is part of the iterative refinement cycle:

```
init → ingest → plan-research → research
                     ↑              │
                     │              ▼
                     │         plan-write → write → edit
                     │              │         │      │
                     └──── gaps ────┘         └──────┘
                                           revisions
```

Editing provides feedback that may trigger:
1. Research cycle (to fill citation gaps)
2. Writing revisions (to fix contradictions)
3. Manual review (for voice consistency)
4. Quality approval (sections ready for publish)

## Statistics to Track

Calculate and report:
- Sections reviewed vs. remaining
- Average voice consistency score
- Timeline violations (count and types)
- Contradiction count (severity breakdown)
- Citation coverage (average per section)
- Line-level suggestions (major vs. minor)
- Sections ready for publish
- Overall quality distribution
- Time per section (estimate remaining time)

## Logging

Detailed logging for transparency:

```
[2024-01-15 17:15:12] [EDIT] Section 1/8 started: Chapter 1, Section 2
[2024-01-15 17:15:13] [LOAD] BRD loaded: version 2
[2024-01-15 17:15:14] [CHECK] Voice: score 8.5/10 (minor deviations)
[2024-01-15 17:15:15] [QUERY] Timeline: character states (pass)
[2024-01-15 17:15:16] [QUERY] Timeline: location introductions (pass)
[2024-01-15 17:15:17] [QUERY] Timeline: event sequences (pass)
[2024-01-15 17:15:18] [CHECK] Contradictions: none detected
[2024-01-15 17:15:19] [CHECK] Citations: 2.4/1000 words (adequate)
[2024-01-15 17:15:20] [SUGGEST] Line-level: 3 minor suggestions
[2024-01-15 17:15:21] [REPORT] Generated: edit_report:section-1-2
[2024-01-15 17:15:22] [EDIT] Section 1/8 complete (10s)
```

## Implementation Notes

### Agent Delegation

This command is a thin wrapper that:
1. Verifies database connection
2. Checks that sections exist for editing
3. Loads BRD and editing configuration
4. Invokes the `editor` agent
5. Displays the agent's output
6. Reports final quality statistics

The actual editing logic lives in the `editor` agent to keep concerns separated.

### Idempotency

Re-running `/bookstrap-edit` is safe:
- Analyzes current section state
- Generates fresh reports
- Overwrites previous edit reports
- No content modification
- Can be run repeatedly to verify fixes

### Read-Only Analysis

Edit mode never modifies content:
- **Analysis only**: Generates reports and suggestions
- **Human review**: Issues flagged for manual resolution
- **No auto-fix**: Preserves authorial control
- **Quality metrics**: Quantitative feedback on readiness

## Advanced Features

### Voice Fingerprinting

Create voice signature from BRD sample:
- Analyze sentence length distribution
- Extract word choice patterns
- Measure formality markers
- Compare sections to signature
- Flag deviations with confidence scores

### Contradiction Graph

Build contradiction graph:
- Nodes: factual claims
- Edges: contradictions or confirmations
- Weights: confidence scores
- Traverse to find conflict chains
- Suggest resolution strategies

### Citation Network

Analyze citation patterns:
- Build source citation network
- Identify heavily-cited sources
- Detect under-utilized sources
- Flag single-source dependencies
- Suggest citation diversification

### Quality Heatmap

Generate quality visualization:
- Map sections to quality scores
- Color-code by readiness
- Identify problematic chapters
- Track improvement over iterations
- Export quality metrics

## Troubleshooting

### No sections found for editing

```
Status: 0 sections ready for editing
Action: Run writing first
```

Solution:
```bash
/bookstrap-write
/bookstrap-edit
```

### BRD not found

```
Error: Cannot load BRD for voice baseline
Action: Editing paused, create BRD first
```

Solution:
```bash
/bookstrap-init
# Complete BRD creation
/bookstrap-edit
```

### Timeline query timeout

```
Section: Chapter 3, Section 5
Warning: Timeline verification query timeout
Action: Using simplified checks
```

Automatic recovery:
- Fall back to basic consistency checks
- Flag for manual timeline review
- Continue with other sections

### Major quality issues found

```
Section: Chapter 2, Section 3
Quality: MAJOR ISSUES
Ready for Publish: No
Action: Pausing for human review
```

Recommended action:
- Review edit report details
- Fix major issues manually
- Re-run editing to verify
- Continue when quality improves

## Quality Metrics

Track editing effectiveness:
- **Voice consistency**: Average score across sections
- **Timeline accuracy**: Violation rate per section
- **Citation density**: Citations per 1,000 words
- **Contradiction rate**: Contradictions per chapter
- **Ready for publish**: Percentage of sections approved
- **Issue detection**: False positive rate
- **Suggestion quality**: User acceptance rate
- **Time efficiency**: Sections reviewed per minute
