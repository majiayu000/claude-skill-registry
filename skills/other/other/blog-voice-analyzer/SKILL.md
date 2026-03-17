---
name: blog-voice-analyzer
description: Run the AI Voice Analyzer on blog content to detect AI-sounding patterns and get actionable rewrite suggestions. Use when reviewing or improving blog articles before publishing.
allowed-tools: Bash(pipenv *), Bash(ls *), Bash(mkdir *)
---

# Blog Voice Analyzer

Analyze blog articles for AI-sounding patterns using NLP, then use the diagnostics to improve the writing before publishing. The goal is content that reads more human than virtually all other blog articles — and avoids being flagged by Google's helpful content signals.

Invoked by the user with `/blog-voice-analyzer` or when asked to "check" or "analyze" a blog post for AI patterns.

## Quick Start

```bash
pipenv run python3 scripts/blog/ai_voice_analyzer.py <path-to-markdown-file>
```

The script accepts any text file (markdown, plain text). It strips frontmatter, HTML, and markdown formatting before analysis.

## What It Detects

The analyzer runs 18 independent checks organized into four categories. Each scores 0-100 (higher = more human), and the overall score is a weighted average.

### Structural Patterns

| Check | What It Measures | AI Signature | Human Signature |
|-------|-----------------|--------------|-----------------|
| **Sentence length variance** | Std dev of word counts per sentence | Clusters around 15-20 words (std dev < 4) | Wild variation: 3-word fragments mixed with 30-word sentences (std dev 8+) |
| **Sentence opener diversity** | POS patterns of first 2 tokens in each sentence | 40%+ start with "The" or "This" | Fragments, questions, conjunctions, inversions, prepositional phrases |
| **Clause depth variety** | Max dependency tree depth per sentence | Uniform depth across sentences | Mix of flat simple sentences and deeply nested complex ones |
| **Paragraph size variety** | Coefficient of variation of paragraph word counts | Every paragraph roughly the same length | One-liners mixed with long blocks |

### Vocabulary & Word Choice

| Check | What It Measures | AI Signature | Human Signature |
|-------|-----------------|--------------|-----------------|
| **Vocabulary diversity (TTR)** | Type-token ratio of content words | Low TTR (< 45%) — recycles same words | Higher TTR, though some writers deliberately use simple vocabulary |
| **Hedge/filler phrases** | Exact match against ~50 AI-marker phrases + ~35 signal words | "It's important to note", "multifaceted", "leverage", "delve", "cornerstone" | Zero matches |
| **Weak adverbs** | Density of "really", "very", "literally", "significantly", etc. | > 1% density | Replaced with stronger verbs or cut entirely |
| **Nominalization density** | Nouns ending in -tion, -ment, -ness, -ity, -ence, -ance | > 5% — "reduction", "transition", "consumption" instead of active verbs | < 3% — prefers "reduce", "shift to", "consume" |
| **Vague verb phrases** | "contributes to", "remains a", "poses a", "provides a", "aims to", etc. | 4-6+ per article | Zero — uses direct assertions |
| **Word repetition** | Content words exceeding expected frequency (topic words get higher threshold) | "Substantial" 4x in 300 words | Topic words may repeat naturally; non-topic words stay varied |

### Voice & Personality

| Check | What It Measures | AI Signature | Human Signature |
|-------|-----------------|--------------|-----------------|
| **Personal voice** | First person ("I", "we"), second person ("you"), contractions ("don't", "it's") | Zero of all three | First person for opinions, second person for engagement, contractions for warmth |
| **Questions asked** | Sentences ending with `?` | Zero questions — pure declaration | 5-10% of sentences are questions (rhetorical or direct) |
| **Concrete specifics (NER)** | Named entities: people, places, dates, numbers, orgs | Zero — everything abstract and generic | Names, dates, numbers, real examples |
| **Readability register** | Flesch-Kincaid grade + avg syllables per word | Grade 14+ (academic), avg syllables > 1.8 | Grade 6-10 (conversational), avg syllables < 1.6 |

### Micro Patterns

| Check | What It Measures | AI Signature | Human Signature |
|-------|-----------------|--------------|-----------------|
| **Passive voice** | Dependency labels `nsubjpass` / `auxpass` | > 15% of sentences | < 10% |
| **Transition word openers** | "However", "Furthermore", "Additionally" at sentence start | > 0.5 per paragraph | Let ideas flow without signposting |
| **Triple-item lists** | "X, Y, and Z" coordinated patterns | > 2 per 1000 words | Not everything comes in threes |
| **Paired adjective cliches** | "ADJ and ADJ" via dependency parse ("smooth and swift", "widespread and uniform") | > 3 per 1000 words | Picks the stronger word |

## How to Read the Output

### Overall Score

| Range | Interpretation |
|-------|---------------|
| **75-100** | Reads naturally. Minor tweaks on flagged items. |
| **55-74** | Some AI patterns visible. Targeted rewrites recommended. |
| **35-54** | Clear AI voice. Significant rewriting needed. |
| **0-34** | Strongly AI-generated. Full rewrite recommended. |

### Flagged Sentences

Only sentences with **2+ issues** are flagged (reduces noise). Each is labeled HIGH/MED severity with specific diagnostics like:

```
[HIGH] #13:
"The variability in charging station availability, especially in rural areas, poses a challenge..."
  → Vague verb: "poses a"
  → Nominalization-heavy (4): variability, station, availability, distance
  → Length (20w) ≈ average (21w)
```

These are the sentences to rewrite first.

### Priority Fixes

The summary lists the 5 worst-scoring dimensions with specific actions. Address these in order.

## How to Use the Output to Improve Content

### Step 1: Run the Analyzer

```bash
pipenv run python3 scripts/blog/ai_voice_analyzer.py path/to/article.md
```

### Step 2: Fix Priority Items Top-Down

Work through the priority fixes list. The most impactful improvements by category:

**If Personality scores low (< 70):**
- Add contractions throughout: "do not" → "don't", "it is" → "it's", "you are" → "you're"
- Add first person for opinions: "I find...", "In my experience...", "We've all been there"
- Add second person to engage the reader: "You know that feeling when..."

**If Questions score low (< 50):**
- Turn topic sentences into questions: "Decision fatigue depletes willpower" → "Why does making too many choices drain you?"
- Add rhetorical questions that make the reader feel seen: "Ever notice how the simplest decisions feel impossible by 8pm?"
- End sections with a question that leads to the next point

**If Readability scores low (< 70):**
- Replace latinate words with shorter ones: "utilize" → "use", "approximately" → "about", "demonstrate" → "show"
- Break long sentences at semicolons and em dashes
- Read it out loud — if you wouldn't say it to a friend, simplify it

**If Nominalization scores low (< 70):**
- Find every -tion/-ment/-ness noun and convert to active verb:
  - "The reduction of stress" → "Reducing stress"
  - "The implementation of the system" → "Implementing the system"
  - "His contribution to the project" → "He contributed to the project"

**If Hedge Phrases are detected:**
- Delete them. Every single one. They add no meaning:
  - "It's important to note that X" → "X"
  - "In today's fast-paced world" → delete entirely
  - "multifaceted" → "complex" or just describe the specific facets

**If Vague Verbs are detected:**
- Replace with direct assertions:
  - "X contributes to Y" → "X causes Y" or "X increases Y"
  - "X remains a significant challenge" → "X is still hard" or explain specifically why
  - "X aims to achieve Y" → "X does Y" or "X tries to Y"

**If Sentence Variance is low (< 70):**
- Add 3-5 word fragment sentences: "That's the point." / "And it works." / "Here's why."
- Break one paragraph's longest sentence into two
- Start a sentence with "But" or "And"

### Step 3: Re-run and Compare

```bash
pipenv run python3 scripts/blog/ai_voice_analyzer.py path/to/article-v2.md
```

Target: overall score > 80, zero HIGH-severity flagged sentences.

### Step 4 (Optional): Run the Model Benchmark

To compare how different AI models perform on similar prompts:

```bash
pipenv run python3 scripts/blog/benchmark_models.py
```

This generates 3 articles per model (Claude Sonnet, Haiku; GPT-4o, 4o-mini, o3-mini) on psychology/productivity topics and scores them all. Edit `TOPICS` and `MODELS` in the script to customize.

## Known Limitations

**Things the analyzer catches well:**
- Vocabulary patterns (hedge phrases, signal words, nominalizations, vague verbs)
- Structural monotony (sentence length, opener repetition, clause depth)
- Voice absence (no personality, no questions, no contractions)
- Register mismatch (academic grade level for blog content)

**Things the analyzer does NOT catch:**
- **Semantic emptiness** — a sentence can sound varied and use no hedge phrases but still say nothing substantive. The tool can't judge whether content is insightful vs. generic platitudes.
- **Template structure at the section level** — Topic → Explanation → Topic → Explanation repeating throughout a piece is a strong AI pattern, but the tool only looks at sentence and paragraph level, not section-level templates.
- **Cliche ideas** — the tool checks *how* you write, not *what* you write. An article full of obvious advice ("get enough sleep", "exercise regularly") will score fine structurally.
- **Over-hedging without trigger phrases** — a passage can be wishy-washy and non-committal without using any of the specific phrases in our list.
- **Images, formatting, and layout** — the tool only analyzes prose text.
- **Short text** — articles under ~300 words produce unreliable scores because statistical measures need volume. Some dimensions (TTR, sentence variance) are especially noisy on short texts.
- **Topic word inflation** — the word repetition detector tries to exclude topic words (extracted from the title and first paragraph), but it's imperfect. If your article's subject uses common words, they may still get flagged.
- **Style vs. defect** — some writers deliberately use simple vocabulary (low TTR), avoid questions (declarative style), or write uniformly-sized paragraphs. The tool treats these as weaknesses because they correlate with AI output, but they may be intentional style choices. Use judgment.
- **False paired adjective flags** — some paired adjectives are natural and effective ("fast and powerful"). The tool applies a per-1000-words density threshold but can still flag good writing.

## Benchmark Reference Scores

From testing across known human and AI text:

| Text | Score | Notes |
|------|-------|-------|
| Paul Graham essays | 85-86 | Gold standard for clear, human prose |
| Clarido blog post (AI-written, edited) | 84 | Well-crafted AI output with personality |
| Claude Haiku (default prompt) | 82 avg | Best out-of-the-box AI model |
| Claude Sonnet (default prompt) | 77 avg | Higher grade level, more nominalizations |
| GPT-4o-mini (default prompt) | 70 avg | Low personality, no contractions |
| o3-mini (default prompt) | 68 avg | Zero contractions, impersonal |
| GPT-4o (default prompt) | 66 avg | Worst personality, fewest questions |
| Raw ChatGPT (no prompting) | 40 | Clear AI voice across all dimensions |

**Target for published content: 80+** with zero HIGH-severity flagged sentences.

## Technical Details

**Dependencies:** `spacy`, `textstat` (Python, installed via pipenv). Requires the `en_core_web_sm` spaCy model.

**How scoring works:** Each of the 18 dimensions scores 0-100. The overall score is a weighted average with personality (0.12), hedge phrases (0.10), entity density (0.08), sentence variance (0.08), and vague verbs (0.07) weighted highest. Full weight table is in `scripts/blog/ai_voice_analyzer.py` in the `analyze()` function.

**Sentence flagging threshold:** Only sentences with 2+ co-occurring issues are flagged. Single-issue sentences are not surfaced to reduce noise. The "length close to average" flag only triggers when the document's overall sentence length std dev is below 6 (indicating genuine monotony).

## Files

| File | Purpose |
|------|---------|
| `scripts/blog/ai_voice_analyzer.py` | Main analyzer — run on any text file |
| `scripts/blog/benchmark_models.py` | Generate + score articles across Claude and GPT models |
| `tmp/benchmark/` | Cached generated articles and results.json from benchmark runs |
