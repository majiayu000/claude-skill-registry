---
name: kdp-keyword-optimizer
description: Optimize the 7 backend keyword slots for Amazon KDP books. This skill should be used when filling out KDP metadata, improving book discoverability, or refreshing keywords for underperforming titles. Focuses on semantic relevance for Amazon's A10 algorithm and Rufus AI.
---

# KDP Keyword Optimizer

Fill your 7 backend keyword slots with semantically relevant phrases that help Amazon's algorithm understand what your book is about and match it to reader searches.

## Purpose

Answer one question: **What 7 keyword phrases should go in my KDP backend slots?**

This skill does NOT cover categories (separate skill) or book descriptions (separate skill). Just the 7 keyword boxes.

## When to Use This Skill

- "What keywords should I use for my book?"
- "How do I fill out the KDP keyword boxes?"
- "My book isn't showing up in search results"
- "I need to optimize my book's metadata"
- "What keywords are my competitors using?"

**Not for:** Category selection, title/subtitle optimization, or book description writing.

---

## The New Reality: Semantic Keywords (2024+)

Amazon's algorithm has fundamentally changed:

### The A10 Algorithm
Amazon now prioritizes **semantic relevance** over exact keyword matches. The algorithm asks: "Does this book actually match the intent of the search?"

### Rufus AI
Amazon's AI shopping assistant scans reviews, themes, and metadata for **contextual matches**. If a reader asks Rufus for "a lighthearted beach read for a mom who needs a break," it won't look for those exact words—it will understand the concept.

### What This Means
- **Keyword stuffing is dead.** Cramming variations of the same word doesn't help.
- **Semantic phrases win.** Think reader intent, not exact matches.
- **Context matters.** Your keywords should describe the *experience* of your book.

---

## The 5-Step Method

### Step 1: Extract Core Themes

From your book description and content, identify:
- **Primary topic** (what is this book fundamentally about?)
- **Target reader** (who is this for?)
- **Reader outcome** (what will they gain?)
- **Emotional appeal** (how will they feel?)
- **Comparable works** (what's it similar to?)

**Example (fasting book):**
- Primary topic: Christian fasting, Lent, OMAD
- Target reader: Catholic, health-conscious, spiritually seeking
- Reader outcome: Closer to God, better health, discipline
- Emotional appeal: Peace, clarity, spiritual freedom
- Comparable works: "like Eat Fast Feast," "for fans of Jason Fung"

### Step 2: Generate Long-Tail Phrases

Combine your themes into 3-5 word phrases that a reader might search.

**Formula:** [Audience] + [Topic] + [Outcome/Format]

**Examples:**
- "catholic lent fasting guide"
- "christian intermittent fasting"
- "40 day spiritual fast"
- "one meal a day christian"
- "lenten devotional with fasting"

**Avoid:**
- Single words ("fasting")
- Duplicating your title words
- Generic terms ("book," "guide," "how to")
- Competitor names or trademarked terms

### Step 3: Check Character Limits

Each keyword slot allows **up to 50 characters**. You can use phrases, not just single words.

**Optimization tip:** Combine related terms in one slot to maximize coverage.

| Slot | Characters | Example |
|------|------------|---------|
| 1 | 50 max | "catholic lent fasting guide spiritual discipline" |
| 2 | 50 max | "christian intermittent fasting one meal a day" |
| 3 | 50 max | "40 day lenten devotional prayer journal" |
| ... | ... | ... |

### Step 4: Validate Against Rules

Amazon has specific keyword rules. Your keywords must NOT include:

- [ ] Words already in your title or subtitle (duplicates hurt, not help)
- [ ] Competitor brand names or book titles
- [ ] Claims of bestseller status or rankings
- [ ] Misleading terms unrelated to your content
- [ ] Subjective claims ("best," "amazing")
- [ ] Temporary terms ("new," "on sale")
- [ ] Common misspellings (Amazon handles these)

**See:** `references/amazon-keyword-rules.md`

### Step 5: Fill All 7 Slots Strategically

Distribute your keywords across slots with intention:

| Slot | Strategy |
|------|----------|
| 1-2 | Primary topic + audience (highest priority searches) |
| 3-4 | Secondary themes + outcomes |
| 5-6 | Related topics + comparable works |
| 7 | Category-cementing keywords (see below) |

### Bonus: Category-Cementing Keywords

Some keywords can help Amazon place your book in additional categories automatically. Reserve 1-2 slots for keywords that match your target categories.

**Example:** If you want to appear in "Christian Living > Prayer," include keywords like "christian prayer devotional" in slot 7.

**Note:** This can also backfire—Amazon may remove you from categories if keywords don't match. Test carefully.

---

## Data Layer: Real Amazon Search Volumes

We have **DataForSEO Amazon API** integrated for real search volume data.

### Check Keyword Volumes

```bash
cd "/Users/charliedeist/Desktop/New Root Docs/Creative Intelligence Agency/skill-stack/amazon-publishing-optimization/data-layer"

# Single or multiple keywords
python3 keyword_volume.py "fasting books" "lent devotional" "catholic meditation"

# From a file
python3 keyword_volume.py -f keywords.txt
```

**Cost:** ~$0.01 per batch of up to 1000 keywords.

### Example Output

| Keyword | Monthly Searches |
|---------|------------------|
| meditation books | 2,580 |
| fasting books | 2,169 |
| mental toughness | 1,084 |
| lent devotional | 261 |
| catholic spiritual reading | 37 |

### Volume Interpretation

| Volume | Meaning |
|--------|---------|
| 1,000+ | High demand, competitive |
| 100-1,000 | Good niche opportunity |
| <100 | Very specific, low search volume |

**Use this data to prioritize slots 1-2 with your highest-volume relevant keywords.**

---

## Additional Research Tools

### Free Options
- **Amazon search autocomplete** - Type your topic, see what Amazon suggests
- **Look inside competitor books** - Check their backend via "Search Inside" feature
- **Google Keyword Planner** - General search volume (not Amazon-specific)

### Paid Options
- **Publisher Rocket** ($199-299) - Amazon-specific keyword data, competition scores
- **Helium 10** (subscription) - Keyword research for Amazon sellers

### The Manual Approach
1. Search Amazon for your topic
2. Note autocomplete suggestions (these are real searches)
3. Look at "Customers also searched for" on competitor pages
4. Compile list, then filter by relevance and character limits
5. **Validate volumes** with the data layer above

---

## Example: Complete Keyword Set

**Book:** The Benedict Challenge (Catholic Lenten fasting guide)

**Title words to avoid repeating:** benedict, challenge, fasting, lent, tradition, one, meal, day

**7 Keyword Slots:**

| # | Keywords (≤50 chars) | Strategy |
|---|----------------------|----------|
| 1 | catholic spiritual discipline lenten devotional | Primary audience + format |
| 2 | christian intermittent omad guide | Health crossover |
| 3 | 40 day prayer journal ash wednesday easter | Timeframe + season |
| 4 | rule of st benedict monastic spirituality | Historical angle |
| 5 | jason fung christian fung alternative | Comp title searchers |
| 6 | ketosis spiritual growth autophagy prayer | Science + spirit blend |
| 7 | religious holidays worship devotion meditations | Category cementing |

---

## Quick Validation Checklist

Before submitting:

- [ ] All 7 slots filled
- [ ] Each slot under 50 characters
- [ ] No title/subtitle words repeated
- [ ] No competitor brand names
- [ ] No subjective claims
- [ ] Mix of specific + broad terms
- [ ] At least 1 slot for category cementing

---

## Bundled Resources

- `references/amazon-keyword-rules.md` - Official Amazon guidelines + restrictions
- `references/keyword-examples.md` - Before/after examples by genre
- `references/semantic-keywords.md` - Deep dive on A10 algorithm changes
- `assets/keyword-worksheet.csv` - Template for planning all 7 slots

---

## Common Mistakes

1. **Repeating title words** - Amazon already indexes your title; duplicating wastes slots
2. **Single-word keywords** - "fasting" is too broad; "catholic lent fasting guide" is specific
3. **Keyword stuffing** - Cramming synonyms doesn't help with semantic search
4. **Ignoring character limits** - Wasted space = wasted opportunity
5. **Set and forget** - Keywords should be refreshed every 3-6 months

---

## Related Skills

- **amazon-category-research** - Select your 3 categories first
- **book-description-writer** - Write conversion-optimized descriptions
- **kdp-launch-checklist** - Pre-publish validation

---

*Keywords are how Amazon understands your book. 7 slots, 50 characters each, semantic relevance over exact matches. Fill them all.*
