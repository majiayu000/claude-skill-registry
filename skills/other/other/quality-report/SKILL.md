---
context: fork
---

# /quality-report

Generate comprehensive content quality metrics and scores for vault notes using parallel Sonnet sub-agents.

## Usage

```
/quality-report
/quality-report --type Adr        # Analyze only ADRs
/quality-report --threshold 60    # Show notes scoring below 60
/quality-report --output markdown # Export to QUALITY_REPORT.md
```

## Instructions

This skill uses **5 parallel Sonnet sub-agents** to analyze different quality dimensions concurrently, then produces an overall quality score for each note and the vault.

### Phase 1: Launch Parallel Quality Analyzers

Create **5 Task agents** running in parallel with `model: "sonnet"`:

**Agent 1: Readability Analysis** (Sonnet)
```
Task: Analyze text readability across all notes
- Use Glob to find all *.md files (exclude +Templates/)
- For each note:
  - Read content
  - Extract body text (exclude frontmatter, code blocks, tables)
  - Calculate readability metrics:
    * Flesch Reading Ease (0-100, higher = easier)
    * Flesch-Kincaid Grade Level (US grade level)
    * Average sentence length
    * Average word length
    * Complex word ratio (words > 3 syllables)
  - Score: (Flesch Reading Ease) / 100 * 100 = 0-100
- Return: Map of filename → readability score + metrics
Formula:
  Flesch Reading Ease = 206.835 - 1.015(words/sentences) - 84.6(syllables/words)
  Flesch-Kincaid Grade = 0.39(words/sentences) + 11.8(syllables/words) - 15.59
```

**Agent 2: Link Density Analysis** (Sonnet)
```
Task: Analyze wiki-link connectivity and density
- Use Glob to find all *.md files
- Build backlink index (which notes link to each note)
- For each note:
  - Count outgoing wiki-links (links to other notes)
  - Count backlinks (notes linking to this one)
  - Calculate link density = links per 100 words
  - Identify orphaned notes (0 backlinks)
  - Identify hub notes (top 10% by backlinks)
  - Check for broken links
- Score calculation:
  * Base: min(outgoing_links / 5, 1) * 40 points  # Cap at 5 links
  * Backlinks: min(backlinks / 3, 1) * 30 points  # Cap at 3 backlinks
  * Penalty: -20 if orphaned (0 backlinks)
  * Penalty: -10 if has broken links
  * Bonus: +10 if hub note (top 10%)
- Return: Map of filename → link density score + metrics
```

**Agent 3: Metadata Completeness Analysis** (Sonnet)
```
Task: Validate frontmatter completeness
- Use Glob to find all *.md files
- For each note:
  - Parse frontmatter
  - Check required fields based on type:
    * Universal: type, title, created
    * Task: completed, priority, due (optional)
    * Project: status, priority, category (optional)
    * ADR: status, relatedTo, supersedes, dependsOn, confidence, freshness
    * Meeting: date, attendees (optional), project (optional)
    * Person: role, organisation (optional), email (optional)
    * Page: description (recommended), tags (recommended)
  - Check optional quality fields:
    * tags (any type)
    * description (any type)
    * modified (any type)
  - Score calculation:
    * Required fields: 1 point each (max based on type)
    * Optional fields: 0.5 points each
    * Quality indicators (ADRs): confidence, freshness, source = 2 points each
    * Normalize to 0-100 scale based on note type
- Return: Map of filename → metadata score + missing fields
```

**Agent 4: Section Completeness Analysis** (Sonnet)
```
Task: Check for expected content sections
- Use Glob to find all *.md files
- For each note type, verify expected sections exist:

  **ADR sections** (required):
  - # Context or ## Context
  - # Decision or ## Decision
  - # Rationale or ## Rationale
  - # Consequences or ## Consequences
  - # Alternatives Considered (recommended)

  **Meeting sections** (recommended):
  - # Agenda or ## Agenda
  - # Attendees or ## Attendees (or in frontmatter)
  - # Discussion or ## Discussion or ## Notes
  - # Action Items or ## Actions or ## Next Steps

  **Project sections** (recommended):
  - # Overview or ## Overview or ## Summary
  - # Status or ## Progress
  - # Timeline or ## Milestones
  - # Risks or ## Challenges (optional)

  **Task sections** (optional, free-form):
  - # Description or ## Details

- Score calculation (per type):
  * ADRs: 20 points per required section (5 sections = 100)
  * Meetings: 25 points per section (4 sections = 100)
  * Projects: 33 points per section (3 sections = ~100)
  * Others: 100 points (no structure requirement)
- Return: Map of filename → structure score + missing sections
```

**Agent 5: Freshness & Tag Relevance Analysis** (Sonnet)
```
Task: Analyze content freshness and tag quality
- Use Glob to find all *.md files
- For each note:
  - Check last modified date (from frontmatter or file stats)
  - Calculate days since modification
  - Determine freshness category by type:
    * Tasks: <7 days = fresh, 7-30 = recent, >30 = stale
    * Projects: <30 days = fresh, 30-90 = recent, >90 = stale
    * ADRs: <180 days = fresh, 180-365 = recent, >365 = stale
    * Meetings: age doesn't matter (scored by completeness)
    * Pages: <90 days = fresh, 90-180 = recent, >180 = stale
  - Analyze tags:
    * Has tags? (yes = good)
    * Tag count: 2-5 = optimal, 1 = okay, 0 = poor, >5 = excessive
    * Tag relevance: match type-specific patterns (e.g., Projects should have domain tags)
  - Score calculation:
    * Freshness: 0-60 points based on days since modification (capped by type thresholds)
    * Tags: 0-40 points (has tags +20, optimal count +20, else proportional)
- Return: Map of filename → freshness score + days old + tag analysis
```

### Phase 2: Wait for All Agents

Use TaskOutput with blocking to collect results from all 5 agents.

### Phase 3: Calculate Overall Quality Scores

For each note, combine the 5 dimension scores:

```javascript
// Overall Quality Score (0-100)
overallScore = (
  readabilityScore * 0.20 +      // 20% weight
  linkDensityScore * 0.25 +      // 25% weight
  metadataScore * 0.20 +         // 20% weight
  structureScore * 0.20 +        // 20% weight
  freshnessScore * 0.15          // 15% weight
)

// Grade assignment
if (overallScore >= 90) grade = 'A'
else if (overallScore >= 80) grade = 'B'
else if (overallScore >= 70) grade = 'C'
else if (overallScore >= 60) grade = 'D'
else grade = 'F'
```

### Phase 4: Generate Quality Report

```markdown
# Vault Quality Report

Generated: {{TIMESTAMP}}
Total Notes Analyzed: {{count}}

## 📊 Overall Vault Quality

**Average Score:** {{avg_score}}/100 ({{grade}})

**Distribution:**
- Grade A (90-100): {{count}} notes ({{%}})
- Grade B (80-89):  {{count}} notes ({{%}})
- Grade C (70-79):  {{count}} notes ({{%}})
- Grade D (60-69):  {{count}} notes ({{%}})
- Grade F (<60):    {{count}} notes ({{%}})

---

## 🔍 Quality Dimensions

### 1. Readability ({{avg}}/100)

**Top Performers:**
- [[{{note}}]]: {{score}}/100 (Flesch: {{flesch}}, Grade Level: {{grade}})
- [[{{note}}]]: {{score}}/100

**Needs Improvement:**
- [[{{note}}]]: {{score}}/100 (Too complex: Grade {{grade}} reading level)
- [[{{note}}]]: {{score}}/100 (Poor structure: avg {{words}} words/sentence)

**Metrics:**
- Average Flesch Reading Ease: {{avg}} ({{interpretation}})
- Average Grade Level: {{grade}} ({{interpretation}})
- Notes with readability < 50: {{count}}

---

### 2. Link Density ({{avg}}/100)

**Hub Notes (Most Connected):**
- [[{{note}}]]: {{backlinks}} backlinks, {{outgoing}} outgoing
- [[{{note}}]]: {{backlinks}} backlinks, {{outgoing}} outgoing

**Orphaned Notes (No Backlinks):**
- [[{{note}}]]: 0 backlinks, {{outgoing}} outgoing (isolated)
- [[{{note}}]]: 0 backlinks, 0 outgoing (completely isolated)

**Metrics:**
- Average links per note: {{avg}}
- Orphaned notes: {{count}} ({{%}})
- Hub notes (top 10%): {{count}}
- Broken links detected: {{count}}

---

### 3. Metadata Completeness ({{avg}}/100)

**Complete Metadata:**
- [[{{note}}]]: {{score}}/100 (all fields + quality indicators)
- [[{{note}}]]: {{score}}/100

**Missing Metadata:**
- [[{{note}}]]: {{score}}/100 (missing: {{fields}})
- [[{{note}}]]: {{score}}/100 (missing: {{fields}})

**Metrics:**
- Notes with complete required fields: {{count}} ({{%}})
- Notes with tags: {{count}} ({{%}})
- Notes with descriptions: {{count}} ({{%}})
- ADRs with quality indicators: {{count}}/{{total ADRs}} ({{%}})

---

### 4. Structure Completeness ({{avg}}/100)

**Well-Structured:**
- [[{{note}}]]: {{score}}/100 (all sections present)
- [[{{note}}]]: {{score}}/100

**Missing Sections:**
- [[{{note}}]]: {{score}}/100 (missing: {{sections}})
- [[{{note}}]]: {{score}}/100 (missing: {{sections}})

**By Type:**
- ADRs with complete structure: {{count}}/{{total}} ({{%}})
- Meetings with complete structure: {{count}}/{{total}} ({{%}})
- Projects with complete structure: {{count}}/{{total}} ({{%}})

---

### 5. Freshness & Tags ({{avg}}/100)

**Recently Updated:**
- [[{{note}}]]: Updated {{days}} days ago
- [[{{note}}]]: Updated {{days}} days ago

**Stale Content:**
- [[{{note}}]]: {{score}}/100 (last updated {{days}} days ago)
- [[{{note}}]]: {{score}}/100 (last updated {{days}} days ago)

**Tag Analysis:**
- Notes with optimal tag count (2-5): {{count}} ({{%}})
- Notes with no tags: {{count}} ({{%}})
- Notes with excessive tags (>5): {{count}} ({{%}})

---

## 📉 Low-Quality Notes (Score < 60)

| Note | Score | Grade | Issues |
|------|-------|-------|--------|
| [[{{note}}]] | {{score}} | {{grade}} | {{top 2 issues}} |
| [[{{note}}]] | {{score}} | {{grade}} | {{top 2 issues}} |

---

## 📈 High-Quality Notes (Score >= 90)

| Note | Score | Grade | Strengths |
|------|-------|-------|-----------|
| [[{{note}}]] | {{score}} | A | {{top 2 strengths}} |
| [[{{note}}]] | {{score}} | A | {{top 2 strengths}} |

---

## 🎯 Improvement Recommendations

### Quick Wins (High Impact, Low Effort)

1. **Fix Orphaned Notes** ({{count}} notes)
   - Add backlinks to: [[{{note}}]], [[{{note}}]], [[{{note}}]]
   - Link from relevant MOCs or Projects

2. **Complete Metadata** ({{count}} notes missing fields)
   - Add required fields: {{list top 10 notes}}
   - Add quality indicators to ADRs: {{list}}

3. **Update Stale Content** ({{count}} notes >{{threshold}} days old)
   - Review and update: [[{{note}}]], [[{{note}}]]
   - Archive or delete: [[{{note}}]], [[{{note}}]]

### Medium Effort

4. **Improve Readability** ({{count}} notes with score < 50)
   - Simplify: [[{{note}}]] (currently Grade {{grade}} level)
   - Break up long sentences in: [[{{note}}]]

5. **Add Missing Sections** ({{count}} notes incomplete)
   - Complete ADR structure: [[{{note}}]]
   - Add meeting action items: [[{{note}}]]

### Long Term

6. **Build Link Network**
   - Target average: 3-5 links per note (current: {{avg}})
   - Focus on connecting Projects ↔ ADRs ↔ Tasks

7. **Establish Update Cadence**
   - Review Projects monthly
   - Update ADRs when decisions change
   - Archive completed work promptly

---

## 📋 Quality Metrics Summary

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Average Score | {{score}} | 80+ | {{status}} |
| Readability | {{score}} | 70+ | {{status}} |
| Link Density | {{score}} | 75+ | {{status}} |
| Metadata | {{score}} | 90+ | {{status}} |
| Structure | {{score}} | 85+ | {{status}} |
| Freshness | {{score}} | 70+ | {{status}} |
| Orphaned Notes | {{count}} | <5% | {{status}} |
| Broken Links | {{count}} | 0 | {{status}} |

---

## 🔄 Next Steps

1. Run `/broken-links` to fix connectivity issues
2. Update stale notes identified in this report
3. Complete metadata for low-scoring notes
4. Re-run quality report in 1 week to track progress

**Export this report:**
```bash
npm run health:markdown > QUALITY_REPORT.md
```

**Schedule automated quality checks:**
```yaml
# .github/workflows/quality-check.yml
on:
  schedule:
    - cron: '0 9 * * 1'  # Monday 9 AM
```
```

## Output Modes

1. **Console (default)** - Colorized terminal output
2. **Markdown** - Save to `QUALITY_REPORT.md`
3. **JSON** - Machine-readable format for dashboards
4. **Dashboard** - Interactive HTML (requires export + viewer)

## Use Cases

**Vault Maintenance:**
- Weekly quality checks
- Pre-publication review
- Migration validation
- Cleanup prioritization

**Content Governance:**
- Ensure ADR quality standards
- Project documentation completeness
- Meeting notes follow template
- Metadata compliance

**Continuous Improvement:**
- Track quality trends over time
- Measure impact of improvements
- Identify systematic issues
- Set quality targets

**Knowledge Management:**
- Find isolated knowledge (orphans)
- Improve discoverability (links)
- Maintain freshness (stale detection)
- Optimize readability

## Performance

- **5 parallel agents** = 5x faster than sequential
- **~500 notes**: 45-90 seconds
- **~2000 notes**: 2-4 minutes
- **~5000 notes**: 5-8 minutes

## Notes

- Readability scoring may not apply well to code-heavy notes or technical specifications
- Freshness scoring is type-aware (ADRs can be old if still valid)
- Structure requirements are recommendations, not strict rules
- Link density considers both quality (backlinks) and quantity (outgoing links)
- Excludes templates and system notes from scoring
- Can be run on subsets with `--type` filter
