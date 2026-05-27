---
name: condense
description: Intelligently reduce article length while preserving value. Does not arbitrarily truncate.
---

# Condense Article

Reduce an overly long article's word count while preserving its essential arguments, unique insights, and distinctive voice.

## When to Use

- When `/condense [filepath]` is invoked
- When executing a `condense` task from todo
- When an article exceeds critical length threshold
- When deep-review encounters an article over hard threshold

## Principles

### What to Cut

1. **Redundancy** - Content that says the same thing twice
   - Repeated explanations in different sections
   - Multiple examples making the same point (keep the best one)
   - Introductory sentences that restate what follows

2. **Background LLMs already know** - Standard definitions and history
   - Basic philosophical terms (consciousness, qualia, etc.) - link instead
   - Historical overviews covered in other articles
   - Common objections that have their own pages

3. **Tangential sections** - Content that could be its own article
   - Extended digressions from the main argument
   - Deep dives into related topics
   - Detailed examples that overshadow the point

4. **Excessive hedging** - Overqualified language
   - "It might perhaps be argued that one could say..."
   - Multiple caveats for the same point
   - Defensive qualifications that weaken rather than clarify

5. **Over-attribution** - Too many citations for obvious claims
   - Multiple citations for uncontroversial facts
   - Block quotes that could be paraphrased
   - Extended literature reviews

### What to Preserve

1. **Opening summary** - Front-loaded key claims for LLM truncation resilience
2. **Unique arguments** - The Map's distinctive contributions
3. **Relation to Site Perspective** - Tenet connections (never remove this section)
4. **Author voice** - Distinctive phrasings that work
5. **Critical cross-links** - Connections to other Map content
6. **Further Reading and References** - Keep but can trim

### What to Extract (Not Delete)

Some content is valuable but doesn't belong in this article:

- **Create linked articles** for detailed subtopics
- **Move extended examples** to separate pages
- **Defer background** to existing concept pages
- Replace removed content with: "For details, see [[linked-article]]"

## Instructions

### 1. Analyze Current State

First, measure the article and understand the problem:

```bash
uv run python -c "
from pathlib import Path
from tools.curate.length import analyze_length
a = analyze_length(Path('[filepath]'))
print(f'Current: {a.word_count} words')
print(f'Target: {a.soft_threshold} words')
print(f'Excess: {a.excess_words} words ({a.excess_percent:.0f}% of target)')
print(f'Status: {a.status}')
print(f'Section: {a.section}')
"
```

**Thresholds by section:**
| Section | Target | Hard | Critical |
|---------|--------|------|----------|
| concepts/ | 2500 | 3500 | 5000 |
| topics/ | 3000 | 4000 | 6000 |
| apex/ | 4000 | 5000 | 6500 |
| voids/ | 2000 | 3000 | 4000 |

Calculate reduction needed:
- **Target**: Middle of acceptable range (e.g., 2000 for concepts, 2500 for topics)
- **Minimum**: Reduce to at least soft threshold
- **Ideal**: Reduce to target while preserving quality

### 2. Structural Review

Read the full article and identify:

1. **Essential sections** - Core argument, must keep
2. **Optional sections** - Supporting but not critical
3. **Redundant passages** - Repeat earlier points
4. **Background to cut** - Could be assumed or linked
5. **Tangents to extract** - Could be separate articles

### 3. Plan Cuts (Show Work)

Before editing, document planned changes in a table:

| Section | Words | Action | Reason |
|---------|-------|--------|--------|
| Opening | 350 | Keep | Front-loaded summary |
| Background on X | 800 | Cut 60% | Standard material, link to [[x]] |
| Main Argument | 1200 | Keep | Core contribution |
| Historical Survey | 600 | Extract | Create separate article |
| Example 1 | 300 | Keep | Best illustration |
| Example 2 | 250 | Cut | Redundant with Example 1 |
| Example 3 | 200 | Cut | Redundant |
| Objections | 500 | Trim 30% | Some repetition |
| Relation to Site | 400 | Keep | Required section |

**Expected result**: Current 4500 → Target 2800 (reduction of 1700 words)

### 4. Apply Condensation

Edit the article following the plan:

**Cutting techniques:**
- Replace paragraphs with single sentences + links
- Combine related sections under one heading
- Remove redundant examples (keep the best one)
- Tighten prose:
  - "It is the case that X" → "X"
  - "In order to" → "To"
  - "Due to the fact that" → "Because"
  - "One might observe that" → (delete)
  - "It should be noted that" → (delete)

**Extraction technique** (when content should exist elsewhere):
1. If creating new article: write it first with proper frontmatter
2. If deferring to existing article: verify the link resolves
3. Replace removed content with: "See [[linked-article]] for details on X."

**Combining technique:**
- Merge sections with overlapping themes
- Use the strongest version of repeated arguments
- Create clear transitions between merged content

### 5. Verify Quality

After condensation, check:

1. **Flow** - Does the article still read smoothly?
2. **Opening summary** - Does it still make sense standalone?
3. **Core argument** - Is the main point preserved?
4. **Tenet connection** - Is "Relation to Site Perspective" intact?
5. **Cross-links** - Do all internal links still work?
6. **Voice** - Does it still sound like the original author?

### 6. Update Frontmatter

```yaml
ai_modified: [current ISO timestamp]
# If significant changes to human content:
ai_contribution: [increase appropriately]
```

### 7. Log to Changelog

Append to `obsidian/workflow/changelog.md`:

```markdown
### HH:MM - condense
- **Status**: Success
- **File**: [filepath]
- **Before**: [word count]
- **After**: [word count]
- **Reduction**: [percentage]%
- **Technique**: [summary: cut redundancy, extracted [topic] to new article, etc.]
```

### 8. Commit

```
refine(content): condense [filename] from N to M words

- [Key cut 1]
- [Key cut 2]

Preserved core arguments and tenet alignment.
```

## What NOT to Do

- **NEVER truncate arbitrarily** (cutting from end without review)
- **NEVER remove the opening summary** - It's critical for LLM access
- **NEVER remove "Relation to Site Perspective"** - Required section
- **NEVER sacrifice unique arguments for length** - Preserve the Map's voice
- **NEVER cut all examples** - Keep at least one good illustration
- **NEVER create orphan content** - If extracting, ensure new article is linked
- **NEVER ignore author voice** - Preserve distinctive phrasings

## When to Leave an Article Long

Some articles genuinely need their length. Document and leave if:

1. **Topic complexity** - The subject truly requires extended treatment
2. **Tenet support** - The article is central to defending core tenets
3. **Unique coverage** - No other resource covers this material
4. **High quality** - Every section adds distinct value

If leaving long, add a note to the changelog:
```markdown
- **Status**: Reviewed, no condensation applied
- **Reason**: [explanation]
```

## Important

- This skill MODIFIES content
- Always preserve the article's core value proposition
- Target the middle of the acceptable range, not the minimum
- Quality > brevity - don't sacrifice clarity for word count
- Document all significant cuts in the changelog
- If unsure whether to cut something, keep it
