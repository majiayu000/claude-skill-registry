---
name: style-learner
description: |

  Triggers: writing style, voice, tone, style guide, exemplar, style learning
  Learn and extract writing style patterns from exemplar text for consistent application.

  Triggers: learn style, extract style, style profile, writing voice, tone analysis,
  style guide generation, exemplar analysis

  Use when: creating a style guide from existing content, ensuring consistency
  across documents, learning a specific author's voice, customizing AI output style

  DO NOT use when: detecting AI slop - use slop-detector instead.
  DO NOT use when: just need to clean up existing content - use doc-generator with --remediate.

  Use this skill to build style profiles from exemplar text.
category: writing-quality
tags: [style, voice, tone, exemplar, learning, consistency]
tools: [Read, Write, TodoWrite]
complexity: medium
estimated_tokens: 1800
progressive_loading: true
modules:
  - feature-extraction
  - exemplar-reference
  - style-application
dependencies:
  - scribe:shared
  - scribe:slop-detector
---

# Style Learning Skill

Extract and codify writing style from exemplar text for consistent application.

## Approach: Feature Extraction + Exemplar Reference

This skill combines two complementary methods:

1. **Feature Extraction**: Quantifiable style metrics (sentence length, vocabulary complexity, structural patterns)
2. **Exemplar Reference**: Specific passages that demonstrate desired style

Together, these create a comprehensive style profile that can guide content generation and editing.

## Required TodoWrite Items

1. `style-learner:exemplar-collected` - Source texts gathered
2. `style-learner:features-extracted` - Quantitative metrics computed
3. `style-learner:exemplars-selected` - Representative passages identified
4. `style-learner:profile-generated` - Style guide created
5. `style-learner:validation-complete` - Profile tested against new content

## Step 1: Collect Exemplar Text

Gather representative samples of the target style.

**Minimum requirements**:
- At least 1000 words of exemplar text
- Multiple samples preferred (shows consistency)
- Same genre/context as target output

```markdown
## Exemplar Sources

| Source | Word Count | Type |
|--------|------------|------|
| README.md | 850 | Technical |
| blog-post-1.md | 1200 | Narrative |
| api-guide.md | 2100 | Reference |
```

## Step 2: Feature Extraction

Load: `@modules/feature-extraction.md`

### Vocabulary Metrics

| Metric | How to Measure | What It Indicates |
|--------|----------------|-------------------|
| Average word length | chars/word | Complexity level |
| Unique word ratio | unique/total | Vocabulary breadth |
| Jargon density | technical terms/100 words | Audience level |
| Contraction rate | contractions/sentences | Formality |

### Sentence Metrics

| Metric | How to Measure | What It Indicates |
|--------|----------------|-------------------|
| Average length | words/sentence | Complexity |
| Length variance | std dev of lengths | Natural variation |
| Question frequency | questions/100 sentences | Engagement style |
| Fragment usage | fragments/100 sentences | Stylistic punch |

### Structural Metrics

| Metric | How to Measure | What It Indicates |
|--------|----------------|-------------------|
| Paragraph length | sentences/paragraph | Density |
| List ratio | bullet lines/total lines | Format preference |
| Header depth | max header level | Organization style |
| Code block frequency | code blocks/1000 words | Technical density |

### Punctuation Profile

| Metric | Normal Range | Style Indicator |
|--------|--------------|-----------------|
| Em dash rate | 0-3/1000 words | Parenthetical style |
| Semicolon rate | 0-2/1000 words | Formal complexity |
| Exclamation rate | 0-1/1000 words | Enthusiasm level |
| Ellipsis rate | 0-1/1000 words | Trailing thought style |

## Step 3: Exemplar Selection

Load: `@modules/exemplar-reference.md`

Select 3-5 passages (50-150 words each) that best represent the target style.

**Selection criteria**:
- Demonstrates characteristic sentence rhythm
- Shows typical vocabulary choices
- Represents the desired tone
- Avoids atypical or exceptional passages

### Exemplar Template

```markdown
### Exemplar 1: [Label]
**Source**: [filename, lines X-Y]
**Demonstrates**: [what aspect of style]

> [Quoted passage]

**Key characteristics**:
- [Observation 1]
- [Observation 2]
```

## Step 4: Generate Style Profile

Combine extracted features and exemplars into a usable style guide.

### Profile Format

```yaml
# Style Profile: [Name]
# Generated: [Date]
# Exemplar sources: [List]

voice:
  tone: [professional/casual/academic/conversational]
  perspective: [first-person/third-person/second-person]
  formality: [formal/neutral/informal]

vocabulary:
  average_word_length: X.X
  jargon_level: [none/light/moderate/heavy]
  contractions: [avoid/occasional/frequent]
  preferred_terms:
    - "use" over "utilize"
    - "help" over "facilitate"
  avoided_terms:
    - delve
    - leverage
    - comprehensive

sentences:
  average_length: XX words
  length_variance: [low/medium/high]
  fragments_allowed: [yes/no/sparingly]
  questions_used: [yes/no/sparingly]

structure:
  paragraphs: [short/medium/long] (X-Y sentences)
  lists: [prefer prose/balanced/prefer lists]
  headers: [descriptive/terse/question-style]

punctuation:
  em_dashes: [avoid/sparingly/freely]
  semicolons: [avoid/sparingly/freely]
  oxford_comma: [yes/no]

exemplars:
  - label: "[Exemplar 1 label]"
    text: |
      [Quoted passage]
  - label: "[Exemplar 2 label]"
    text: |
      [Quoted passage]

anti_patterns:
  - [Pattern to avoid 1]
  - [Pattern to avoid 2]
```

## Step 5: Validation

Test the profile against new content:

1. Generate sample content using the profile
2. Compare metrics to extracted features
3. Have user evaluate voice/tone match
4. Refine profile based on feedback

### Validation Checklist

- [ ] Metrics within 20% of exemplar averages
- [ ] No anti-pattern violations
- [ ] Tone matches user expectation
- [ ] Vocabulary aligns with exemplars
- [ ] Structure follows profile guidelines

## Usage in Generation

When generating new content, reference the profile:

```markdown
Generate [content type] following the style profile:
- Voice: [from profile]
- Sentence length: target ~[X] words, vary between [Y-Z]
- Use exemplar passage as tone reference:
  > [exemplar quote]
- Avoid: [anti-patterns from profile]
```

## Integration with slop-detector

After generating content, run slop-detector to verify:
1. No AI markers introduced
2. Style metrics match profile
3. Anti-patterns avoided

## Exit Criteria

- Style profile document created
- At least 3 exemplar passages included
- Quantitative metrics extracted
- Anti-patterns from slop-detector integrated
- Validation test passed
