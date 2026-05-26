---
name: apex-evolve
description: Build and maintain apex articles—human-readable synthesis pieces.
---

# Apex Evolve

Build and maintain apex articles through creation, evolution, and length management.

## When to Use

- Creating a new apex article from the approved list
- Evolving an existing apex article when source content has changed
- Checking which apex articles need attention

## Invocation

```
/apex-evolve create "Article Title"
/apex-evolve evolve [article-slug]
/apex-evolve check
```

## Modes

### Mode 1: `create`

Generate a new apex article from scratch.

**Input**: Article title from the approved list in `obsidian/apex/apex-articles.md`

**Process**:
1. Look up the article in the master list to get source articles and thesis
2. Read all source articles to understand the material
3. Read `obsidian/project/writing-style.md` for apex article guidelines
4. Synthesize into a narrative that weaves sources together
5. Target length: 2500-4000 words
6. Create with required frontmatter (see below)

**Output**: New apex article at `obsidian/apex/[slug].md`

### Mode 2: `evolve`

Update an existing apex article when sources have changed.

**Input**: Specific article slug, or omit to auto-select stalest

**Process**: See 10-step evolution process below

**Output**: Improved article + review archive

### Mode 3: `check`

Report which apex articles need evolution.

**Process**:
1. Read all apex articles and their `apex_sources` frontmatter
2. For each source, check its `modified` date against the apex article's `apex_last_synthesis`
3. Report articles with stale sources, ordered by priority

**Output**: List of articles needing attention with staleness scores

---

## Frontmatter Schema

Apex articles use standard frontmatter plus apex-specific fields:

```yaml
---
title: "Article Title"
created: 2026-01-24
modified: 2026-01-24
human_modified: null
ai_modified: 2026-01-24T00:00:00+00:00
draft: false
topics: []
concepts: []
related_articles: []

ai_contribution: 100
author: null
ai_system: claude-opus-4-5-20251101
ai_generated_date: 2026-01-24
last_curated: null

# Apex-specific fields
apex_sources:
  - topics/free-will
  - topics/agent-causation
  - concepts/mental-causation
apex_last_synthesis: 2026-01-24T00:00:00+00:00
apex_thesis: "One-sentence thesis statement"
---
```

---

## Evolution Process (10 Steps)

### Step 1: Select Article

If article specified, use it. Otherwise, auto-select:
1. Read all apex articles in `obsidian/apex/`
2. For each, calculate staleness score:
   - Count sources modified after `apex_last_synthesis`
   - Score = days_stale × changed_source_count
3. Select highest-scoring article

### Step 2: Identify Changed Sources

Compare each source's `modified` date to `apex_last_synthesis`. List all changed sources.

### Step 3: Read Changed Sources

Read the full content of each changed source to understand new material.

### Step 4: Pessimistic Review

Apply three critical personas:

**Clarity Critic**: Where is the prose unclear, jargon-heavy, or hard to follow? Where does the narrative lose the reader?

**Redundancy Hunter**: What passages repeat information? Where does the article say the same thing twice? What can be cut without losing meaning?

**Narrative Flow Analyst**: Where does the argument structure break down? Are transitions smooth? Does the piece build to its conclusion?

### Step 5: Optimistic Review

Apply three supportive personas:

**Connection Finder**: What new connections from changed sources should be woven in? What synthesis opportunities exist?

**Synthesis Strengthener**: Where can the article better show how pieces fit together? Where is the "so what" unclear?

**Human Reader Advocate**: What would make this more engaging to read? Where does it feel like a reference rather than a narrative?

### Step 6: Length Assessment

1. Count current word length
2. Compare to target range: 2500-4000 words
3. Note whether condensation or expansion is needed

### Step 7: Apply Improvements

**Always do**:
- Fix issues identified by pessimistic review
- Integrate insights from changed sources
- Strengthen synthesis per optimistic review

**If over 4000 words** (condensation required):
- Remove redundant passages identified by Redundancy Hunter
- Tighten prose: eliminate filler words, combine sentences
- Move detailed explanations to source articles; replace with links
- Remove sections that duplicate what sources already cover well
- Preserve the narrative arc while reducing word count

**If under 2500 words** (expansion needed):
- Expand synthesis sections showing connections between sources
- Add transitions that guide the reader through the argument
- Deepen the narrative arc with richer examples

### Step 8: Update Frontmatter

```yaml
ai_modified: [current UTC timestamp]
apex_last_synthesis: [current UTC timestamp]
```

Adjust `ai_contribution` if human edits were preserved.

### Step 9: Create Review Archive

Create `obsidian/reviews/apex-evolve-[date]-[slug].md` containing:
- Article reviewed
- Changed sources identified
- Pessimistic review findings (3 personas)
- Optimistic review findings (3 personas)
- Length assessment (before/after word counts)
- Summary of changes made

### Step 10: Log and Commit

1. Log to `obsidian/workflow/changelog.md`:
   ```
   ## [timestamp] apex-evolve
   - **Status**: Complete
   - **Article**: [title]
   - **Changed sources**: [count]
   - **Word count**: [before] → [after]
   - **Review**: reviews/apex-evolve-[date]-[slug].md
   ```

2. Create git commit:
   ```
   feat(apex): Evolve [article-title]

   - Integrated changes from [N] updated sources
   - [Brief summary of improvements]
   ```

---

## Article Structure

Apex articles follow this structure:

```markdown
# [Title]

[Opening paragraph stating the integrated thesis - what this synthesis argues]

## [Narrative Section 1]

[Build the argument, drawing from multiple sources]
[Link to sources: "As explored in [[source-article]]..."]

## [Narrative Section 2]

[Continue building, showing connections between ideas]

## [Additional sections as needed]

## Synthesis

[Show how the pieces fit together in a way individual articles don't]
[This is the unique value of the apex article]

## Relation to Site Perspective

[Connect to tenets - required for all articles]

## Source Articles

This apex article synthesizes:
- [[source-1|Source 1 Title]]
- [[source-2|Source 2 Title]]
- ...
```

---

## Length Management Guidelines

**Target**: 2500-4000 words

**Why this range**:
- Under 2500: Not enough synthesis to justify an apex article
- Over 4000: Becomes unwieldy for human readers; defeats the purpose

**Condensation techniques**:
- "As [[source-article]] explores in detail..." (link instead of repeat)
- Combine related paragraphs
- Remove hedging language that adds words without adding meaning
- Cut examples that illustrate the same point

**Expansion techniques**:
- "This connects to [[other-source]] because..." (show synthesis)
- Add transitional paragraphs between major sections
- Deepen the "why this matters" throughout

---

## Cross-Review Integration

When other skills create or modify content that's an apex source:

1. After `/expand-topic` or `/research-topic` completes
2. Check if the new/modified article is in any apex article's `apex_sources`
3. If yes, add to `obsidian/workflow/todo.md`:
   ```markdown
   - [ ] P2 apex-evolve: [apex-article-slug] — source [modified-article] updated
   ```

This ensures apex articles stay current without manual tracking.

---

## Important

- **Approved subjects only**: Only create apex articles from the master list in `obsidian/apex/apex-articles.md`
- **Human-first**: Unlike topics/concepts, apex articles prioritize narrative flow over LLM-atomic structure
- **Media-neutral language**: Never use the phrase "apex article" in the article content itself. Content may be reproduced in contexts where our internal terminology is unknown. Write as standalone prose.
- **Condense actively**: Evolution must maintain length discipline; don't let articles grow unbounded
- **Link extensively**: Apex articles are synthesis—they should link heavily to source articles
- **Preserve thesis**: Each apex article has a thesis; edits should strengthen it, not dilute it
