---
name: seo-pseo-planner
description: "Programmatic SEO strategies. Use when: creating scalable content, building directories/galleries. Triggers on: 'PSEO', 'programmatic SEO', 'content at scale'."
allowed-tools:
  - webfetch
  - Read
  - Write
  - mcp__gsc__search_analytics
  - mcp__gsc__enhanced_search_analytics
---

# Programmatic SEO (PSEO) Planner

Plan scalable SEO content generation strategies that can create hundreds of pages automatically using code.

## What is PSEO?

Programmatic SEO leverages programming to generate SEO content at scale. Instead of manually creating each page, you:

1. Acquire substantial data
2. Shape it into various formats
3. Display it to users via automatically generated pages

**When to use PSEO**:
- You can generate 100+ unique pages
- Content follows a repeatable template
- Data is available or can be collected
- Keywords have clear patterns (e.g., "{style} tattoo ideas")

**When NOT to use PSEO**:
- Only 3-5 pages needed → Create manually
- No scalable data source available
- Content would be too shallow/thin

---

## The Six-Step PSEO Framework

### Step 1: Identify Opportunities

**Criteria for PSEO viability**:

```
□ Can generate 100+ unique pages
□ Clear keyword pattern exists (e.g., "{city} photographers")
□ Low keyword difficulty (KD < 20) for long-tail variations
□ Sufficient search volume across variations
□ Data source available or creatable
□ Content can provide REAL value (not just scraped data)
```

**Good PSEO opportunities**:
- Directories (photographers, agencies, tools)
- Inspiration galleries (designs, templates, examples)
- Idea generators (tattoos, names, prompts)
- Comparison pages (tool vs tool)
- Location-based listings

**Questions to answer**:
1. What's the main keyword category?
2. How many long-tail variations exist?
3. What data will populate each page?
4. Can users find this data elsewhere easily? (If yes, add more value)

---

### Step 2: Establish Page Structure

**Define your keyword hierarchy**:

```
Main Keyword (head term)
├── Category Level
│   ├── Subcategory Level
│   │   └── Individual Pages
```

**Example - Tattoo Ideas**:
```
tattoo ideas (main)
├── dragon tattoo ideas (category)
├── flower tattoo ideas (category)
│   ├── rose tattoo ideas (subcategory)
│   └── lotus tattoo ideas (subcategory)
└── name tattoo ideas (category)
```

**Example - Landing Page Inspiration**:
```
landing page inspiration (main)
├── saas landing page (industry)
├── product landing page (industry)
├── marketing landing page (industry)
└── pricing page design (page type)
```

**URL Structure**:
```
/[main-category]/
/[main-category]/[subcategory]/
/[main-category]/[subcategory]/[item]/
```

**Critical**: Ensure keyword alignment. Each page targets a DISTINCT keyword to avoid cannibalization.

---

### Step 3: Gather Content (Data Collection)

**Data Sources**:

| Source | Example | Pros | Cons |
|--------|---------|------|------|
| **User Generated Content (UGC)** | User submissions via your tool | Unique, scalable | Needs initial users |
| **APIs** | Google Maps, Product Hunt | Structured, reliable | Rate limits, costs |
| **Web Scraping** | Screenshots, competitor data | Rich data | Legal considerations |
| **AI Generation** | GPT-generated descriptions | Scalable | Quality control needed |
| **Public Datasets** | Government data, open APIs | Free, authoritative | May need processing |

**UGC Strategy** (Best for unique content):
1. Build a free tool that generates user value
2. Collect user inputs and outputs
3. Aggregate into categorized pages
4. Automated via cron jobs

**Example - Tattoos AI**:
- Users describe tattoo → AI generates image
- Cron job collects prompts daily
- Auto-categorizes: "black cat tattoo" → cat category
- Creates page when category hits 100+ items

---

### Step 4: Shape the Content

**Content Processing Pipeline**:

```
Raw Data → Cleaning → Enrichment → Categorization → Formatting
```

**Enrichment Methods**:

| Method | Use Case | Tool |
|--------|----------|------|
| AI Summarization | Condense long content | GPT-4 |
| Auto-tagging | Categorize items | NLP/Keywords |
| Image Processing | Screenshots, thumbnails | Puppeteer, APIs |
| Data Aggregation | Combine multiple sources | Custom scripts |
| Review Extraction | Ratings, highlights | Scraping + AI |

**Tagging Strategy**:
- Extract keywords from content
- Map to predefined categories
- Allow multiple tags per item
- Create pages when threshold met (e.g., 50-100 items)

**AI Content Guidelines**:
- Use AI to ASSIST, not REPLACE human quality
- Always add unique value beyond raw AI output
- Human review for quality control
- Avoid generic, templated descriptions

---

### Step 5: Setup Display Structure

**Page Template Components**:

```
┌─────────────────────────────────────┐
│ SEO Title: "111 Best {Category} Designs" │
├─────────────────────────────────────┤
│ Meta Description (150-160 chars)    │
├─────────────────────────────────────┤
│ H1: Main Title                      │
├─────────────────────────────────────┤
│ Introduction (100-200 words)        │
│ - What this page offers             │
│ - Why it's valuable                 │
├─────────────────────────────────────┤
│ Content Grid/List                   │
│ - Items with images/data            │
│ - Pagination if needed              │
├─────────────────────────────────────┤
│ [CTA: Your Product Promotion]       │
├─────────────────────────────────────┤
│ Related Categories (internal links) │
├─────────────────────────────────────┤
│ FAQ Section (optional)              │
└─────────────────────────────────────┘
```

**Dynamic Elements**:
- Title with count: "111 Best {X}" (updates automatically)
- Fresh date indicators
- Category navigation
- Search/filter functionality
- Infinite scroll or pagination

**Content Depth Requirements**:
- Minimum 100-200 words of text per page
- Unique intro/description per category
- Internal links to related pages
- Avoid thin content at all costs

---

### Step 6: Promote Your Offering

**Monetization Integration**:

| Position | Strategy | Example |
|----------|----------|---------|
| **In-content CTA** | Button after X items | "Design your own tattoo" |
| **List insertion** | Your product as #3 option | "Try HeadshotPro instead" |
| **Sidebar** | Persistent promotion | Free tool banner |
| **Exit intent** | Popup on leave | Newsletter/product signup |
| **Related section** | Your tools as related | "Also try our generator" |

**Example - Tattoos AI**:
- Browse tattoo ideas → See CTA "Design Your Own"
- Click → Goes to paid AI generator
- Result: $4,000/month passive revenue

**Example - Landingfolio**:
- Free inspiration gallery → Build traffic
- Later add: Figma/Tailwind component library for sale

---

## PSEO Anti-Patterns (What NOT to Do)

### 1. Shallow Content
❌ **Bad**: Just list names and addresses from Google Maps
✅ **Good**: Add reviews, photos, analysis, unique insights

**HeadshotPro Failure Case**:
- Listed photographers from Google Maps
- No unique value over Google Maps itself
- Result: Failed to rank

### 2. AI Content Spam
❌ **Bad**: 100% AI-generated pages with no human review
✅ **Good**: AI assists, humans refine and add value

### 3. Crawl Budget Abuse
❌ **Bad**: Publish 1,000 pages at once
✅ **Good**: Spread over weeks/months, let Google index gradually

### 4. Keyword Cannibalization
❌ **Bad**: Multiple pages targeting same keyword
✅ **Good**: Each page targets distinct long-tail variation

### 5. Duplicate Content
❌ **Bad**: Same description across all pages
✅ **Good**: Unique intro, unique meta, unique content per page

### 6. Thin Content
❌ **Bad**: Title + 3 images + no text
✅ **Good**: 100-200+ words of valuable context per page

---

## PSEO Planning Template

### Opportunity Assessment

```
## PSEO Opportunity: [Name]

### Concept
[One sentence description]

### Keyword Analysis
- **Main Keyword**: [keyword] ([volume]/mo, KD [X])
- **Pattern**: "[variable] + [main keyword]"
- **Estimated Pages**: [X]+
- **Long-tail Examples**:
  - [variation 1] ([volume], KD [X])
  - [variation 2] ([volume], KD [X])
  - [variation 3] ([volume], KD [X])

### Data Source
- **Type**: [UGC / API / Scraping / AI]
- **Collection Method**: [description]
- **Update Frequency**: [daily/weekly/manual]
- **Unique Value Added**: [what makes it better than raw data]

### Page Structure
```
[URL hierarchy diagram]
```

### Content Template
- **Title Pattern**: "[Count] Best [Category] [Type]"
- **Content Components**: [list]
- **Minimum Content**: [X] words + [X] items

### Monetization
- **Primary**: [strategy]
- **Secondary**: [strategy]
- **CTA Placement**: [where]

### Technical Requirements
- **Stack**: [technologies]
- **APIs Needed**: [list]
- **Automation**: [cron jobs, pipelines]

### Risk Assessment
- **Thin Content Risk**: [low/medium/high]
- **Cannibalization Risk**: [low/medium/high]
- **Competition**: [analysis]

### Timeline
- Week 1: [milestone]
- Week 2: [milestone]
- Week 3: [milestone]
- Week 4: [milestone]
```

---

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Pages indexed | 80%+ of published | Google Search Console |
| Organic traffic | Growing monthly | GSC / Analytics |
| Ranking keywords | 50%+ in top 20 | Ahrefs / GSC |
| Bounce rate | < 70% | Analytics |
| Time on page | > 1 min | Analytics |
| Conversions | Defined by monetization | Analytics |

---

## Reference Files

- [CASE-STUDIES.md](CASE-STUDIES.md) - Detailed success and failure case studies
