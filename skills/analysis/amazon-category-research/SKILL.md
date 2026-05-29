---
name: amazon-category-research
description: Research profitable Amazon KDP categories for book publishing. This skill should be used when planning a book launch, analyzing competition, or optimizing category selection for discoverability. Guides the 3-category decision with BSR analysis and ghost category avoidance.
---

# Amazon Category Research

Select the right 3 Amazon categories for your book. This is a one-time, high-stakes decision—categories can't easily be changed after publishing, and 27% of KDP categories are "ghost categories" that don't actually work.

## Purpose

Answer one question: **Which 3 categories should this book be in?**

This skill does NOT cover keywords (separate skill) or book descriptions (separate skill). Just categories.

## When to Use This Skill

- "Which categories should I choose for my book?"
- "I'm publishing on KDP and need to pick categories"
- "Is [category name] a good category?"
- "How do I become a bestseller on Amazon?"
- "What categories are my competitors in?"

**Not for:** Keyword research, book description writing, cover design, or pricing strategy.

---

## The 4-Step Method

### Step 1: Find Comp Titles

Identify 5-10 books similar to yours that are selling well.

**How to find them:**
- Search Amazon for your topic
- Look for books with 50+ reviews and BSR under 100,000
- Note the ASIN (10-character ID starting with B) for each

**What makes a good comp:**
- Similar topic/genre to your book
- Published in last 2-3 years
- Actively selling (BSR under 100,000)

### Step 2: Extract Their Categories

Use [BKLNK](https://bklnk.com) (free tool) to see all categories for each comp title.

**Process:**
1. Go to bklnk.com
2. Enter the ASIN
3. See all categories the book is listed in
4. Note which categories appear across multiple comps

**What you're looking for:**
- Categories that multiple successful comps share
- Specific subcategories (not just "Fiction" or "Non-Fiction")
- Categories that actually have bestseller rankings

### Step 3: Analyze BSR for Each Category

For each candidate category, check the competition level.

**How to check:**
1. Go to Amazon's category page
2. Note the BSR of the #1 book
3. Note the BSR of the #20 book
4. Use the BSR calculator: `scripts/bsr_to_sales.py`

**Competition levels:**

| #1 Book BSR | Level | What It Means |
|-------------|-------|---------------|
| < 500 | Very High | Hard to crack |
| 500-5,000 | High | Needs strong launch |
| 5,000-10,000 | Medium | Achievable |
| 10,000-50,000 | Low | Good opportunity |
| > 50,000 | Very Low | Easy, but low traffic |

### Step 4: Apply the Portfolio Strategy

Select 3 categories with different competition levels:

| Slot | Target | Purpose |
|------|--------|---------|
| **1. Niche** | BSR #1 > 10,000 | Easy bestseller badge at launch |
| **2. Mid-range** | BSR #1 = 5,000-10,000 | Steady visibility |
| **3. Growth** | BSR #1 < 5,000 | Upside if book takes off |

**Why this works:**
- Slot 1 gives you a quick win (bestseller badge = social proof)
- Slot 2 provides consistent discoverability
- Slot 3 positions you for growth

---

## Critical Warning: Ghost Categories

**27% of KDP categories are "ghost categories"** that:
- Have no category page on Amazon
- Can't earn bestseller badges
- Provide zero discoverability

**Before selecting ANY category:**
1. Search Amazon for that category
2. Click through to verify the page exists
3. Confirm books in that category have bestseller badges

If you can't find a real category page: **DO NOT SELECT IT.**

See `references/ghost-categories.md` for details on identification.

---

## Tools

| Tool | Cost | Use |
|------|------|-----|
| [BKLNK](https://bklnk.com) | Free | See any book's categories by ASIN |
| [Kindlepreneur BSR Calculator](https://kindlepreneur.com/amazon-kdp-sales-rank-calculator/) | Free | Convert BSR to daily sales |
| `scripts/bsr_to_sales.py` | Free | Local BSR calculator |
| [Publisher Rocket](https://publisherrocket.com) | $199-299 | Automated category research + ghost detection |
| [KDSPY](https://kdspy.com) | $79 | Browser extension for BSR data |

### Reality Check: The Free Path Requires Manual Work

**BSR data is not easily scraped.** Amazon pages are JavaScript-rendered and don't yield BSR numbers to automated tools.

**The free workflow:**
1. Find comp titles via Amazon search (works)
2. Extract categories via BKLNK (works)
3. **Get BSR numbers** → Must visit each Amazon product page manually, scroll to "Product Details," and note the BSR
4. Convert BSR to sales via calculator (works)

**The paid workflow:**
- Publisher Rocket ($199-299 one-time) automates steps 2-4 AND detects ghost categories
- KDSPY ($79 one-time) adds BSR overlay to Amazon pages as you browse

**Recommendation:** For a single book, the free path is fine (budget 1-2 hours). For multiple books or ongoing publishing, Publisher Rocket pays for itself in time saved.

---

## Quick Reference: Research Template

Copy `assets/research-spreadsheet.csv` and fill in for your book:

| Category Path | BSR #1 | BSR #20 | Ghost? | Competition | Notes |
|---------------|--------|---------|--------|-------------|-------|
| [Fill in] | | | | | |

---

## Example: Applying the Method

**Book:** A guide to Christian fasting practices

**Step 1 - Comp titles:**
- "Fasting" by Jentezen Franklin (ASIN: B001ANSS7U)
- "The Fasting Edge" by Jentezen Franklin
- "A Hunger for God" by John Piper
- "Atomic Power of Prayer and Fasting" by Cindy Trimm

**Step 2 - Categories extracted via BKLNK:**
- Religion & Spirituality > Christian Living > Spiritual Growth
- Religion & Spirituality > Christian Living > Prayer
- Health, Fitness & Dieting > Diets > Fasting

**Step 3 - BSR analysis:**
- Spiritual Growth: #1 BSR = 3,500 (High competition)
- Prayer: #1 BSR = 8,000 (Medium)
- Fasting (Health): #1 BSR = 15,000 (Low)

**Step 4 - Selection:**
1. **Niche:** Health > Diets > Fasting (easy badge)
2. **Mid:** Christian Living > Prayer (steady)
3. **Growth:** Christian Living > Spiritual Growth (upside)

---

## Bundled Resources

- `references/bsr-thresholds.md` - What BSR numbers mean for sales
- `references/ghost-categories.md` - How to identify and avoid ghost categories
- `references/category-examples.md` - 8+ real case studies with results
- `scripts/bsr_to_sales.py` - Convert BSR to daily sales estimates
- `assets/research-spreadsheet.csv` - Template for tracking research

---

## Common Mistakes

1. **Selecting broad categories** - "Fiction" or "Non-Fiction" = drowning in competition
2. **Not verifying for ghosts** - Trust the KDP dropdown at your peril
3. **All eggs in one basket** - Using all 3 slots on similar categories
4. **Ignoring comp research** - Guessing instead of following proven paths
5. **Set and forget** - Categories that worked last year may be saturated now

---

## Related Skills

- **kdp-keyword-optimizer** - Optimize the 7 backend keyword slots
- **book-description-writer** - Write conversion-optimized descriptions
- **kdp-launch-checklist** - Pre-publish validation

---

*Category selection is a strategic decision. 3 slots, 27% ghosts, permanent choice. Research before you publish.*
