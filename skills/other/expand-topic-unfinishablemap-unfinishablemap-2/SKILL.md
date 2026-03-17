---
name: expand-topic
description: Generate a new article on a topic. Content is published directly.
---

# Expand Topic

Generate a new article on a philosophical topic.

## When to Use

- When a todo item is type `expand-topic`
- When `/expand-topic [topic]` is invoked
- After research has been completed on a topic

## Instructions

### 1. Check for Research

Look in `obsidian/research/` for existing research on this topic.

If no research exists:
- For simple topics, proceed with general knowledge
- For complex topics, run `/research-topic` first

### 2. Determine Target Location

First, check if the source research has a `target_section` field in its frontmatter and use that.

Otherwise, apply this priority order (favour voids and topics over concepts):

1. **Voids** (`obsidian/voids/[slug].md`) — if the article explores:
   - Cognitive limits or boundaries of thought
   - Unchartable territories or things that resist understanding
   - The unexplored, unexplorable, or occluded
   - Paradoxes or self-referential difficulties
   - Apophatic or negative approaches to knowledge

2. **Topics** (`obsidian/topics/[slug].md`) — if the article addresses:
   - Big philosophical questions (consciousness, free will, meaning, identity)
   - Substantive explorations that connect multiple concepts
   - Questions humans actually ask about life and mind
   - Anything that could be framed as "What does X mean for us?"

3. **Concepts** (`obsidian/concepts/[slug].md`) — only if the article is:
   - A definitional piece explaining a specific philosophical term
   - Background material that other articles will reference
   - A technical idea that serves as building block, not destination

**Default to topics** when uncertain. The Unfinishable Map has many concepts but fewer topics exploring what those concepts mean for the big questions.

Use kebab-case for filenames (e.g., `hard-problem-of-consciousness.md`).

**Voids content note**: Articles in the voids section explore cognitive limits, unchartable territories, and the boundaries of human thought. They should:
- Maintain intellectual honesty about what is speculation vs. established
- Acknowledge uncertainty about whether limits are real or merely difficult
- Connect to the voids framework (unexplored, unexplorable, occluded)
- Reference the voids index: `[[voids]]`

### 3. Review Style Guide

Before writing, review `obsidian/project/writing-style.md` for:
- Document structure requirements (opening summary, H2 sections, tenet connection)
- Named-anchor summary pattern for forward references
- Background vs. novelty guidance (what to include/omit)
- LLM optimization (front-load important information)

### 4. Check Tenet Alignment

Before writing, review `obsidian/tenets/tenets.md` and ensure the article will:
- Not contradict any tenet
- Not endorse positions that tenets "rule out"
- Acknowledge the Map's perspective where relevant

### 5. Generate Article

**CRITICAL: Source Attribution Discipline**

Before writing, understand these rules to prevent misattribution errors:

#### 5.1 Two-Channel Structure (Required for Research-Based Articles)

When the article is based on a specific source (research paper, book, philosopher's work), structure content into two clearly separated channels:

**Channel A: Source Exposition** — What the author actually claims
- Use hedged language: "X argues...", "According to X...", "X's framework..."
- Include verbatim short quotes (≤25 words) for load-bearing definitions
- Do NOT inject Map perspective here
- Do NOT attribute claims the author didn't make

**Channel B: Map Integration** — How the Map interprets or builds on this
- Clearly label: "## Relation to Site Perspective" or "## Map Integration"
- Use explicit framing: "The Map interprets this as...", "This aligns with the Map's tenet..."
- Speculation must be flagged: "The Map speculates that..." or "One possible integration..."

**Never interleave these channels.** Keep source exposition and Map interpretation in separate sections.

#### 5.2 Quote-and-Cite Gates

For any named law, constraint, or technical definition attributed to a source:
- Include a verbatim short quote (≤25 words) with citation
- Preserve crucial qualifiers (e.g., "default causal profile" not just "causal profile")
- If the source says "X or at least Y", don't simplify to just "X"

Example of qualifier preservation:
- ✗ "Wherever information exists, it has phenomenal character"
- ✓ "Information (or at least some information) has two aspects" — with note that Chalmers treats universal scope as open question

#### 5.3 Position Strength Calibration

Match claim strength to what the source actually says:

| Source says | Article should say |
|-------------|-------------------|
| "explores" / "worth investigating" | "X explores..." (not "X argues" or "X shows") |
| "has sympathy for" | "X expresses sympathy for..." (not "X rejects alternatives") |
| "one option is" | "One approach X considers..." (not "X's framework requires") |
| "explicitly argues" | "X argues..." (can use stronger framing) |

**Never attribute a commitment the source doesn't make.** Especially for:
- Quantum interpretation commitments (collapse vs MWI)
- Whether something is "required" vs "one possible mechanism"
- Strong claims like "solves" or "answers" vs "addresses" or "responds to"

#### 5.4 Research-Note Alignment Check

If a research note exists for this topic:
1. Read the matching research note
2. Extract the 5 most important claims
3. Verify the article doesn't contradict them
4. If diverging from research notes, explain why explicitly

#### 5.5 Non-Contradiction Self-Check

Before finalizing, verify:
- [ ] Did I claim the theory is both X-dependent and X-independent?
- [ ] Did I attribute to the author claims they didn't discuss?
- [ ] Did I drop technically essential qualifiers?
- [ ] Did I present exploratory positions as commitments?
- [ ] Did I inject Map arguments as if they were the source's arguments?

---

Use the existing generation tool:
```bash
uv run python scripts/generate.py article "[Topic Title]" --style exploratory
```

Or write directly with this structure:

```markdown
---
title: "[Topic Title]"
description: "[150-160 chars emphasizing human+AI collaboration, iterative refinement, and pursuit of truth]"
created: YYYY-MM-DD
modified: YYYY-MM-DD
human_modified:
ai_modified: YYYY-MM-DDTHH:MM:SS+00:00
draft: false
topics: []
concepts: []
related_articles: []
ai_contribution: 100
author:
ai_system: [current model]
ai_generated_date: YYYY-MM-DD
last_curated:
---

[Opening paragraph - accessible hook into the topic]

## [First Major Section - Source Exposition]

[What the source actually claims, with quotes for key definitions]

## [Second Major Section - Source Exposition]

[Continue source exposition...]

## Relation to Site Perspective

[CLEARLY SEPARATED: How the Map interprets this work]
[Use explicit framing: "The Map interprets...", "This aligns with..."]
[Flag speculation: "The Map speculates that..."]
[Do NOT present Map arguments as if they came from the source]

## Further Reading

- [[related-article-1]]
- [[related-article-2]]

## References

[If based on research, cite sources]
```

### 5.5 Length Check (Self-Edit if Over Target)

Before finalizing, count words and check against section thresholds:

```bash
uv run python -c "
from pathlib import Path
from tools.curate.length import analyze_length
a = analyze_length(Path('[filepath]'))
print(f'{a.word_count} words ({a.excess_percent:.0f}% of {a.soft_threshold} target) - {a.status}')
"
```

**Target ranges by section:**
| Section | Target | Soft Max | Hard Max |
|---------|--------|----------|----------|
| concepts/ | 1500-2000 | 2500 | 3500 |
| topics/ | 2000-2500 | 3000 | 4000 |
| voids/ | 1500-2000 | 2000 | 3000 |

**If over soft max:** Self-edit before publishing:
- Tighten prose (remove "it is the case that", "one might argue")
- Cut redundant explanations
- Replace detailed tangents with links to other articles
- Ensure the core argument is preserved

**If over hard max:** Mandatory self-edit:
- The article is too long for its section
- Consider splitting into multiple articles
- Or significantly condense following `/condense` principles

Include final word count in the changelog entry.

### 6. Update Todo

If this was a todo item:
1. Mark the task as complete
2. Note the output file

### 7. Log to Changelog

Prepend to `obsidian/workflow/changelog.md` (add immediately after frontmatter, before existing entries):

```markdown
## [current time from prompt] - expand-topic
- **Status**: Success
- **Topic**: [topic name]
- **Output**: [[filepath without .md extension]]
- **Word count**: [count]
- **Based on research**: [yes/no, wikilink if yes]
```

### 8. Commit

Create a git commit with message:
```
feat(content): Add article on [topic]

Based on research: [yes/no]
```

### 9. Check Apex Sources

After creating the article, check if it's a source for any apex article:

1. Read `obsidian/apex/apex-articles.md`
2. For each apex article entry, check if the new article path appears in `Source articles`
3. If yes, add a task to `obsidian/workflow/todo.md`:
   ```markdown
   - [ ] P2 apex-evolve: [apex-slug] — source [new-article] created
   ```

This ensures apex articles are updated when their source content changes.

## Content Guidelines

Follow the comprehensive guidance in `obsidian/project/writing-style.md`.

**Quick reference:**
- Lead with the most important point (LLM truncation resilience)
- Use named-anchor pattern for forward references
- Include "Relation to Site Perspective" section
- Minimize standard background; focus on what's novel
- Short: 500-800 words | Medium: 1000-1500 | Long: 2000-3000

## Important

- **CRITICAL: ALWAYS set `draft: false`** — Content is published directly. Never use `draft: true`.
- **ALWAYS include a `description`** — 150-160 chars emphasizing human+AI collaboration, iterative refinement, pursuit of truth. Avoid generic descriptions.
- ALWAYS include `ai_contribution: 100`
- ALWAYS include current model in `ai_system`
- ALWAYS update `ai_modified` timestamp
- Content must align with site tenets

### Attribution Discipline (Critical)

These errors have been caught by outer reviews and cause real damage to credibility:

- **NEVER attribute claims to an author who didn't make them** — If the source doesn't discuss X, don't say "Author argues X"
- **NEVER drop crucial qualifiers** — "Default causal profile" is not the same as "causal profile"
- **NEVER strengthen hedged positions** — "Explores" ≠ "argues"; "has sympathy for" ≠ "rejects alternatives"
- **NEVER present Map interpretations as source claims** — Keep source exposition and Map integration in separate sections
- **NEVER claim shared commitments without verification** — Check if the author actually shares our position before claiming alignment

When in doubt, hedge toward the source's actual language.
