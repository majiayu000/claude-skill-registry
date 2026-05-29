---
name: find-candidates
description: Guidelines for systematically finding new candidate words to add to candidate_words.json for later dictionary entry creation.
user_invocable: true
invocations:
  - /find-candidates
---

# Finding Candidate Words for the Dictionary

Use this skill when asked to find new words to add to `candidate_words.json` for later addition to the dictionary.

## Workflow Overview

1. Determine the search strategy based on user request and dictionary maturity
2. Check each word against eligibility criteria (MANDATORY duplicate checks)
3. Add qualifying words to `candidate_words.json` using the manage_candidates script
4. Report what was added

## Duplicate Prevention (AUTOMATIC)

**The `manage_candidates.py add` command now AUTOMATICALLY checks for duplicates.**

When you run:
```bash
python3 build/manage_candidates.py add "食べる" "たべる" "to eat"
```

The script will:
1. Check `entries_index.json` for matching reading or headword
2. Check `candidate_words.json` for matching reading or word
3. **REFUSE to add the word if any match is found**
4. Display the existing match so you know why it was rejected

### Example of Automatic Rejection
```
$ python3 build/manage_candidates.py add "食べる" "たべる" "to eat"
ERROR: Duplicate detected!
  Exact match in dictionary: 00396_taberu (食べる / たべる)

This word already exists. NOT adding to candidates.
```

### Pre-Check Command (Optional)
If you want to check a word before attempting to add it:
```bash
python3 build/manage_candidates.py check "漢字" "かんじ"
```

### Batch Checking (Optional)
To check multiple words at once before adding:
```bash
python3 build/check_duplicate.py --batch "食べる:たべる" "飲む:のむ" "書く:かく"
```

### Near-Duplicate Patterns to Watch

The automatic check catches exact matches. You should still watch for:
- **Verb forms**: する verbs may exist as standalone nouns (勉強 vs 勉強する)
- **Kanji variants**: 見る/観る, 聞く/聴く - check if one already covers the meaning
- **Okurigana variations**: 行なう/行う, 現われる/現れる
- **Prefix/suffix forms**: Check if 大～ or ～的 forms exist as part of other entries
- **Reading variations**: Long vowels (おう vs おお), particles in readings

## Eligibility Criteria (ALL must be met)

### 1-1. Not Already in the Dictionary

Check that the word is NOT already in `entries_index.json` (by reading AND headword).

### 1-2. Not Already a Candidate

Check that the word is NOT already in `candidate_words.json` (by reading AND word).

### 1-3. Not a Proper Noun

**EXCLUDE** the following categories:
- Place names (東京, ニューヨーク, 富士山, etc.)
- Personal names (田中, マイク, etc.)
- Company/brand names (トヨタ, ソニー, etc.)
- Other proper nouns (specific event names, specific work titles, etc.)

**Note:** Proper nouns may be added systematically in a future phase.

## Selection Criteria (At least ONE must be met)

A word qualifies for addition if it meets at least one of these criteria:

### 2-1. Similar Frequency/Centrality to Existing Entries

The word should have a usage frequency or centrality to contemporary Japanese similar to words already in `entries_index.json`.

**How to assess:**
- Consider whether an intermediate learner would encounter this word regularly
- Compare to existing entries at similar frequency levels
- Note: All new entries are assigned to the general tier (basic and core tiers are complete)

### 2-2. Semantic Relation to Existing Entries

The word is a common **synonym**, **antonym**, or **related word** to an entry already in the dictionary.

**Types of semantic relations:**
- **Synonyms:** Words with similar meanings at different registers or contexts
- **Antonyms:** Opposite meanings
- **Semantic groups:** Words belonging to the same category as existing entries

### 2-3. Modern Widespread Terms

Words that have come into widespread, stable usage in contemporary Japanese. This includes vocabulary from technology, media, lifestyle, and other areas of modern life. Focus on terms with established, lasting usage rather than ephemeral trends.

### 2-4. Informal/Colloquial Terms Useful for Learners

Well-known informal or colloquial terms that:
- Do not typically appear on formal vocabulary lists
- Are commonly encountered in everyday Japanese
- Would help learners understand natural speech

**Exclude:** Highly ephemeral slang, vulgar terms, discriminatory language

---

## Search Strategies

The dictionary has ~6,000 entries plus ~700 candidates. Use a variety of strategies to find remaining gaps while ensuring comprehensive coverage.

### Vocabulary Tier Status

**The basic and core tiers are complete (as of January 2026).**

- Basic: 795 entries (target met)
- Core: 1,998 entries (target met)
- General: 4,566+ entries (all new vocabulary goes here)

**All new candidate words will be assigned to the general tier.** Focus on finding useful vocabulary for advanced learners, specialized topics, and vocabulary that complements existing entries.

### Strategy: Corpus-Driven Gap Analysis

Use corpus frequency data to find common words still missing.

**Method:**
1. Consider the top 10,000 words in corpora like BCCWJ (Balanced Corpus of Contemporary Written Japanese)
2. Compare against entries_index.json
3. Words in the top 10,000 by frequency that aren't in the dictionary are high-priority candidates

**Why effective:** Guarantees discovered words are genuinely common.

### Strategy: Collocational Mining

Find words that commonly appear with existing entries but aren't in the dictionary.

**Method:**
1. Take existing entries, especially verbs and adjectives
2. Consider their most common collocates (words they frequently appear with)
3. Check if those collocates are in the dictionary

**Why effective:** Finds words learners need to use existing vocabulary naturally.

### Strategy: Register/Formality Pairs

For existing entries, find their register variants (formal ↔ informal, written ↔ spoken).

**Method:**
1. Take informal words in the dictionary, find their formal equivalents
2. Take formal/written words, find their colloquial equivalents
3. Check keigo (honorific) variants of common verbs

**Why effective:** Learners need multiple registers; dictionaries often have gaps here.

### Strategy: Semantic Domain Exploration

Explore semantic domains to find gaps, but **choose domains creatively** based on what seems underrepresented rather than following a fixed list.

**Method:**
1. Browse existing entries to identify which semantic domains have coverage
2. Notice which domains seem thin or missing
3. Systematically check for gaps in those domains
4. Be creative—consider domains that are practical for daily life, work, study, or cultural understanding

**Why effective:** Ensures balanced coverage across the vocabulary learners need.

### Strategy: Productive Pattern Completion

Systematically complete morphological patterns already partially in the dictionary.

**Method:**
1. Identify word-formation patterns that are productive in Japanese (compound verbs, adjectival derivations, noun compounds, etc.)
2. Check which common words using those patterns are missing
3. Add gaps

**Why effective:** These patterns are productive and predictable; gaps are easy to identify systematically.

### Strategy: Cross-Reference Expansion

Expand from existing entries by finding mentioned but unlisted words.

**Method:**
1. Read recent dictionary entries
2. For each entry, identify synonyms, antonyms, and related words mentioned in notes or cross-references
3. Check if those related words are in the dictionary
4. Add missing ones as candidates

**Why effective:** Useful for incremental expansion from established content.

### Strategy: Written vs Spoken Japanese Balance

Ensure the dictionary covers both written and spoken Japanese.

**Method:**
1. Check for gaps in formal/written vocabulary (news, academic, business contexts)
2. Check for gaps in casual/spoken vocabulary (conversation, sentence-final expressions, contracted forms)

**Why effective:** Dictionaries often skew toward one medium; this ensures balanced coverage.

---

## Creative Exploration

**Don't limit yourself to the strategies above.** Each search session should involve creative thinking about what vocabulary learners need that might be missing. Consider:

- What practical situations would learners encounter?
- What vocabulary would help them understand media, conversations, or texts?
- What semantic fields feel underrepresented?
- What word types (verbs, adjectives, adverbs, etc.) might have gaps?

The goal is comprehensive, balanced coverage—not deep exploration of any single category at the expense of others.

---

## Adding Candidates

After identifying qualifying words, add them using:

```bash
python3 build/manage_candidates.py add "漢字表記" "ひらがな読み" "brief English note"
```

**IMPORTANT: Readings must be in hiragana, not katakana.**

Even for loanwords with katakana headwords, the reading must be hiragana:
```bash
# Correct:
python3 build/manage_candidates.py add "スキー" "すきー" "skiing"

# Wrong (katakana reading):
python3 build/manage_candidates.py add "スキー" "スキー" "skiing"
```

**Notes field guidance:**
- Brief English gloss or description
- Can include part of speech hint
- Keep under 50 characters

**Example:**
```bash
python3 build/manage_candidates.py add "提案" "ていあん" "proposal, suggestion"
```

## Output Format

After adding candidates, report:
1. Number of words added
2. Summary of categories/sources (aim for variety)
3. Any notable gaps identified for future sessions

## Quality Reminders

- **Duplicates are blocked automatically:** The `manage_candidates.py add` command will refuse to add duplicates
- **Watch for near-duplicates:** The automatic check catches exact matches; manually verify for verb forms, kanji variants, etc.
- **Breadth over depth:** Aim for broad coverage across many domains rather than deep coverage of a few
- **General tier only:** All new entries are assigned to the general tier (basic and core are complete)
- **Learner utility:** Prioritize words an intermediate learner would benefit from knowing
- **No proper nouns:** Save those for systematic addition later
- **Stable vocabulary:** Avoid ephemeral slang or highly specialized jargon
- **Creative variety:** Each session should explore different areas; avoid repeatedly searching the same categories
- **Use batch checks:** When planning which words to add: `python3 build/check_duplicate.py --batch "word1:reading1" ...`
