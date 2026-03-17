---
name: cv-data-ingestion
description: Ingest and organize raw career data from Obsidian notes, CSV files, zip archives, and markdown documents into the Universal CV portfolio system. Use when processing career history, work experience, testimonials, case studies, or resume data from multiple sources. Outputs structured YAML/Markdown validated against Zod schemas.
---

# Universal CV Data Ingestion & Organization

<purpose>
Transform unstructured career data into the portfolio's content structure, ready for variant generation and "hired-on-sight" presentation.
</purpose>

<when_to_activate>
Activate when the user:
- Provides raw career data (Obsidian vault, CSV, zip, markdown)
- Says "ingest", "import", "process my data", "load my experience"
- Wants to populate the knowledge base from source files
- Has files in `source-data/` directory to process

**Trigger phrases:** "ingest", "import", "process", "load data", "parse my resume"
</when_to_activate>

## Input Directory

**Drop all source files in `source-data/`** — this directory is gitignored.

```
source-data/
├── obsidian-vault/       # Obsidian folders with .md files
├── linkedin-export.csv   # CSV exports
├── resume.pdf            # Resumes
├── gemini-review.md      # AI summaries (processed first)
└── archive.zip           # Bulk exports
```

## Target Output Structure

All output goes to the existing `content/` directory:

```
content/
├── profile.yaml              # Identity, hero, about, stats
├── experience/index.yaml     # Work history with rich details
├── case-studies/*.md         # Project deep-dives (frontmatter + markdown)
├── testimonials/index.yaml   # Social proof quotes
├── certifications/index.yaml # Certs and credentials
├── passion-projects/index.yaml
├── skills/index.yaml         # Technical & domain skills
└── variants/                 # Job-specific personalizations
```

## Supported Input Formats

### Obsidian Vault (.md files)
- Daily notes, project notes, work journals
- YAML frontmatter with metadata
- Tags, links, dataview syntax
- Nested folder structures

### CSV Files
- LinkedIn exports
- Spreadsheet data (experience, skills, projects)
- Any structured tabular career data

### Zip Archives
- Mixed content (CSV, text, images, videos)
- Bulk exports from tools
- Compressed vault backups

### Text Files
- Resume text dumps
- Job descriptions
- Performance reviews
- Testimonial snippets

### Images & Media
- Screenshots of achievements
- Certificates
- Project visuals
- Linked for case studies

---

## Processing Workflow

### Phase 0: Schema Understanding (MANDATORY FIRST STEP)

**Objective**: Read and internalize the actual Zod schemas before writing ANY content.

**CRITICAL**: This step MUST be completed before any file writes. Schema mismatches were the #1 source of validation errors in past runs.

```bash
# Always read the schema file first
Read src/lib/schemas.ts
```

**Key Schema Constraints to Verify**:

| Content Type | Field | Constraint |
|-------------|-------|------------|
| Skills | `skills` | `z.array(z.string())` — simple strings only, NOT objects |
| Case Study Media | `type` | `z.enum(['blog', 'twitter', 'linkedin', 'video', 'article', 'slides'])` |
| Testimonial | `featured` | `z.boolean()` — required, not optional |
| Experience | `highlights` | `z.array(z.string())` — simple strings only |
| Case Study CTA | `action` | `z.enum(['contact', 'calendly', 'linkedin'])` — only these 3 values |

**Before writing any file, confirm**:
1. ✅ Field types match schema exactly (string vs object vs array)
2. ✅ Enum values are from the allowed set
3. ✅ Required fields are present
4. ✅ Optional fields use correct null/undefined handling

---

### Phase 1: Data Discovery & Inventory

**Objective**: Map all source files before processing.

#### Step 1a: Check for Existing AI Summaries (HIGH PRIORITY)

**Before parsing raw files**, look for existing AI-generated summaries or reviews. These are often more structured and save significant parsing time.

```bash
# Look for AI review files
find source-data/ -name "*review*" -o -name "*summary*" -o -name "*gemini*" -o -name "*claude*" -o -name "*gpt*"

# Check for structured exports
find source-data/ -name "*.json" -o -name "*export*"
```

**If found**: Use as PRIMARY source, cross-reference with raw data for verification.

#### Step 1b: Inventory Raw Sources

```bash
# For Obsidian vault
find source-data/ -name "*.md" -type f | head -50

# For zip archive (extract first)
unzip -l source-data/*.zip | head -50

# Categorize by type
find source-data/ -type f \( -name "*.md" -o -name "*.csv" -o -name "*.txt" -o -name "*.json" \)
```

Create an inventory table with confidence scores:
| File | Type | Category | Priority | Confidence |
|------|------|----------|----------|------------|
| gemini-review.md | AI Summary | All | HIGH | ⬛⬛⬛ High |
| work-history.md | Markdown | Experience | High | ⬛⬛⬜ Medium |
| skills.csv | CSV | Skills | Medium | ⬛⬛⬛ High |
| testimonials.txt | Text | Social Proof | High | ⬛⬜⬜ Low |

### Phase 2: Experience Enrichment

For each work role, extract/synthesize:

```yaml
# Target: content/experience/index.yaml
jobs:
  - company: "Company Name"
    role: "Job Title"
    period: "YYYY – YYYY"
    location: "City, State"
    logo: "/images/logos/company.svg"  # Optional, nullable
    url: "https://company.com"         # Company website - ALWAYS extract if available
    highlights:
      - "Achievement with specific metric (e.g., 15× revenue growth)"
      - "Technical accomplishment with stack details"
      - "Cross-functional impact with scope"
      - "Decision/trade-off that shows judgment"
      - "Scale indicator (users, transactions, team size)"
    tags: ["Domain1", "Tech1", "Skill1"]
```

**Enrichment criteria**:
- 3-4 highlights per role (focused, not exhaustive)
- Specific metrics > vague claims (SMART: Specific, Measurable, Achievable, Relevant)
- Technologies and methodologies named
- Collaboration scope mentioned
- Key decisions with trade-offs

#### Product Links in Highlights (IMPORTANT)

**Highlights support markdown links** — use `[Product Name](url)` to link to shipped products, docs, or proof.

```yaml
# Example with inline product links
highlights:
  - "Shipped [Advanced API](https://ankr.com/docs/advanced-api/) from 0→1, serving 1M+ daily requests"
  - "Built [Xbox royalties blockchain](https://ey.com/case-study) achieving 99% faster processing"
  - "Launched [Playground V2](https://play.flow.com/) improving developer onboarding by 60%"
```

**Link priority for highlights**:
1. Live product/demo URLs (highest credibility)
2. Official documentation
3. NPM/PyPI package pages
4. GitHub repos
5. Case studies or press coverage

**Why this matters**: Recruiters verify claims. A clickable link to a live product instantly validates the work is real.

#### Link Extraction (IMPORTANT)

**Always extract and verify company/project URLs** so viewers can quickly validate the work is real.

**Sources for URLs**:
1. Company websites mentioned in source docs
2. LinkedIn company pages
3. Product URLs, app store links
4. GitHub repos, documentation sites
5. Press releases, news articles

**Link extraction process**:
```bash
# Search source files for URLs
grep -oE 'https?://[^\s<>"]+' [SOURCE_FILES]

# Common patterns to look for
- "company.com", "startup.io", "project.xyz"
- LinkedIn: linkedin.com/company/[name]
- GitHub: github.com/[org]
- Product Hunt, Crunchbase links
```

**Validation**:
- Verify URL is still active (not 404)
- Prefer official company domain over third-party
- For defunct companies: use archive.org link or LinkedIn

| Company Type | URL Priority |
|-------------|--------------|
| Active startup | Official website (e.g., mempools.com) |
| Enterprise | Company careers/about page |
| Acquired | Parent company or press release |
| Defunct | LinkedIn or archive.org |

#### Confidence Scoring for Experience Data

Track extraction confidence for each data point:

| Confidence | Criteria | Action |
|------------|----------|--------|
| ⬛⬛⬛ **High** | Exact quote from source, verified metric, named source | Use directly |
| ⬛⬛⬜ **Medium** | Synthesized from multiple sources, approximated metric | Use with note |
| ⬛⬜⬜ **Low** | Inferred, placeholder metric like "[X%]", uncertain date | Flag for user review |

**Before writing experience file**:
1. List all LOW confidence items for user confirmation
2. Mark uncertain metrics with `[VERIFY]` prefix in draft
3. Only write after user confirms or provides corrections

#### Pre-Validation Check (Before Writing)

```yaml
# Validate structure matches schema BEFORE writing
# ExperienceSchema expects:
jobs:
  - company: string      # Required
    role: string         # Required
    period: string       # Required: "YYYY – YYYY" format
    location: string     # Required
    logo: string | null  # Optional
    url: string | null   # Optional - but ALWAYS try to populate!
    highlights: string[] # Required: array of STRINGS (not objects!)
    tags: string[]       # Required
```

### Phase 3: Case Study Mining

Identify projects with case study potential:

**Criteria**:
- Clear problem → approach → result arc
- Quantifiable impact (revenue, users, time saved)
- Decision points with reasoning
- Lessons learned (what worked, what didn't)

```yaml
# Target: content/case-studies/NN-slug.md frontmatter
---
id: [next_available_number]
slug: project-slug
title: "Project Title"
company: "Company Name"
year: "YYYY-YY"
tags: [Tag1, Tag2, Tag3]
duration: "X months"
role: "Your Role"

hook:
  headline: "One-line impact statement"
  impactMetric:
    value: "XX%"
    label: "metric label"
  subMetrics:
    - value: "YY"
      label: "secondary metric"
  thumbnail: /images/case-study-slug.png

cta:
  headline: "Call to action question"
  subtext: "Optional elaboration"
  action: calendly  # or: contact, linkedin
  linkText: "Let's talk →"
---

[Markdown body with: Challenge, Approach, Key Decision, Execution, Results, Learnings]
```

### Phase 4: Testimonial Extraction

#### Distinguishing Personal vs Project Testimonials (CRITICAL)

**Personal testimonials** (USE these):
- About the individual: "Working with [Name]...", "[Name] is exceptional at..."
- Collaboration focused: "...a pleasure to work with", "...always delivered"
- Skill endorsements: "...best product manager I've worked with"
- Growth observations: "...grew from... to..."

**Project testimonials** (DO NOT use as personal):
- About the project/product: "The blockchain solution transformed..."
- Company endorsements: "Microsoft's approach to..."
- Generic team praise: "The team delivered..."

#### Detection Heuristics

**High-confidence personal testimonial signals**:
```
✅ Contains person's name + positive verb: "[Name] led", "[Name] designed"
✅ Uses "I" + relationship: "I worked with", "I hired", "I managed"
✅ Personal qualities: "collaborative", "thoughtful", "proactive"
✅ Recommendation language: "I recommend", "would hire again"
✅ Source: LinkedIn recommendation, performance review
```

**Low-confidence / Project quote signals**:
```
⚠️ No personal name mentioned
⚠️ Focuses on deliverable, not person
⚠️ Source: press release, case study, marketing material
⚠️ Generic praise: "great work", "successful project"
```

#### Search Patterns for Testimonials

```bash
# Phrases indicating personal testimonials
grep -i "working with \[name\]" [SOURCE]
grep -i "I recommend" [SOURCE]
grep -i "pleasure to work" [SOURCE]
grep -i "\[name\] is" [SOURCE]
grep -i "one of the best" [SOURCE]

# LinkedIn recommendation patterns
grep -i "I had the opportunity" [SOURCE]
grep -i "I've had the pleasure" [SOURCE]
```

#### Testimonial Quality Checklist

Before including a testimonial:
- [ ] Is it about the PERSON, not just the project?
- [ ] Does it include specific details (not generic praise)?
- [ ] Can the source be verified (LinkedIn, named author)?
- [ ] Is the author's relationship clear (manager, peer, report)?

```yaml
# Target: content/testimonials/index.yaml
testimonials:
  - quote: >
      Full testimonial text with specific details about
      collaboration, impact, or skills demonstrated.
    author: "Full Name"  # Or "Engineering Lead" if anonymized
    initials: "FN"
    role: "Their Role"
    company: "Company Name"
    avatar: null  # Or path to image
    featured: true  # Required boolean - for prominent display
```

#### Gap Handling

If no valid personal testimonials found:
1. **Flag as HIGH priority gap** in gap analysis
2. Suggest manual follow-up actions:
   - Export LinkedIn recommendations
   - Request recommendations from past colleagues
   - Check old emails for praise snippets
3. **DO NOT fabricate** or use project quotes as personal testimonials

### Phase 5: Skills Taxonomy

#### CRITICAL: Schema Constraint

**The skills schema expects SIMPLE STRINGS, not objects!**

```yaml
# ❌ WRONG - This will fail validation
categories:
  - name: "Technical Leadership"
    skills:
      - name: "Platform Architecture"
        level: "expert"
        evidence: "..."

# ✅ CORRECT - Simple string array
categories:
  - name: "Technical Leadership"
    skills:
      - "Platform Architecture"
      - "API Design"
      - "System Integration"
```

#### Preserving Evidence (Workaround)

Since the schema doesn't support evidence fields, preserve context using YAML comments:

```yaml
# Target: content/skills/index.yaml
categories:
  - name: "Technical Leadership"
    skills:
      # Evidence: Designed multi-client validator infra at Anchorage
      - "Platform Architecture"
      # Evidence: Shipped Ankr Advanced APIs, 1M+ daily requests
      - "API Design"

  - name: "Web3 & Blockchain"
    skills:
      # Evidence: First smart contract at Microsoft (2016)
      - "Ethereum"
      # Evidence: ETF-grade validator provisioning
      - "Staking Infrastructure"
```

#### Pre-Validation Check

```typescript
// SkillsSchema from src/lib/schemas.ts:
SkillsSchema = z.object({
  categories: z.array(z.object({
    name: z.string(),
    skills: z.array(z.string())  // <-- STRINGS ONLY!
  }))
});
```

**Before writing skills file**:
1. Verify each skill is a plain string
2. Move any evidence/level data to comments
3. Test parse the YAML structure mentally

### Phase 6: Validation & Gap Analysis

```bash
# Validate all content against Zod schemas
npm run validate

# Check for gaps
```

**Gap checklist**:
- [ ] All required fields populated
- [ ] No placeholder URLs (demo.com, example.com)
- [ ] Metrics are specific, not vague ("improved" → "improved by 40%")
- [ ] Missing metrics marked with `[METRIC]` for user to fill (e.g., "Increased revenue by [METRIC]%")
- [ ] Each experience has 3-4 highlights (focused, not exhaustive)
- [ ] Product links included for every shipped product/tool
- [ ] All dates in consistent format (YYYY or YYYY–YY)

---

## Schema Reference

### Experience Entry
```typescript
{
  company: string;      // Required
  role: string;         // Required
  period: string;       // Required: "YYYY – YYYY" or "YYYY – Present"
  location: string;     // Required
  logo?: string;        // Optional: path to logo
  url?: string;         // Optional: company website - ALWAYS include if available
  highlights: string[]; // Required: 3-4 items with [Product](url) links where possible
  tags: string[];       // Required: 2-5 tags
}
```

### Case Study Frontmatter
```typescript
{
  id: number;           // Required: unique incremental
  slug: string;         // Required: URL-friendly
  title: string;        // Required
  company: string;      // Required
  year: string;         // Required: "YYYY" or "YYYY-YY"
  tags: string[];       // Required
  duration: string;     // Required
  role: string;         // Required
  hook: {
    headline: string;
    impactMetric: { value: string; label: string };
    subMetrics?: { value: string; label: string }[];
    thumbnail?: string;
  };
  cta: {
    headline: string;
    subtext?: string;
    action: "contact" | "calendly" | "linkedin";
    linkText: string;
  };
  // Optional links
  demoUrl?: string;
  githubUrl?: string;
  docsUrl?: string;
  media?: { type: string; url: string; label?: string }[];
}
```

### Testimonial Entry
```typescript
{
  quote: string;        // Required: the testimonial text
  author: string;       // Required: name or title if anonymized
  initials: string;     // Required: for avatar fallback
  role: string;         // Required
  company: string;      // Required
  avatar?: string;      // Optional: image path
  featured?: boolean;   // Optional: for prominent display
}
```

---

## Automation Outputs

After processing, generate:

1. **Data Lineage Document** (`docs/data-lineage.md`)
   - Source file → target field mapping
   - Transformation notes
   - Decisions made during processing

2. **Gap Analysis Report** (`docs/gap-analysis.md`)
   - Missing required fields
   - Thin content areas
   - Recommended improvements

3. **Processing Summary**
   - Files processed count
   - Content items created/updated
   - Validation status

---

## Example Workflows

### Workflow 1: Obsidian Vault Import

```
User: "I have an Obsidian vault at ~/Documents/Career-Notes with my work history"

Steps:
1. Scan vault for relevant files (work, projects, reviews folders)
2. Parse each markdown file, extract structured data
3. Map to experience/index.yaml format
4. Identify case study candidates
5. Extract any testimonial quotes
6. Validate and report gaps
```

### Workflow 2: LinkedIn Export + Resume

```
User: "I have a LinkedIn CSV export and my resume as text"

Steps:
1. Parse CSV for positions, skills, recommendations
2. Parse resume text for additional details
3. Merge and deduplicate
4. Enrich highlights with specific metrics
5. Create skills taxonomy
6. Validate against schemas
```

### Workflow 3: Zip Archive with Mixed Content

```
User: "I have a zip file with CSV files, text notes, and screenshots"

Steps:
1. Extract archive to temp directory
2. Inventory all files by type
3. Process CSVs for structured data
4. Process text files for testimonials/notes
5. Catalog images for case study thumbnails
6. Consolidate into content structure
7. Clean up temp files
```

---

## Quality Criteria

### "Hired-on-Sight" Standard

Every piece of content should pass this test:

- **Specific**: Numbers, names, technologies — not vague claims
- **Verified**: Can point to source data
- **Impactful**: Shows business/user value, not just activity
- **Consistent**: Formatting, dates, terminology aligned
- **Complete**: No "TODO" or placeholder content

### Validation Commands

```bash
# Full content validation
npm run validate

# Build to catch any issues
npm run build

# Preview locally
npm run dev
```

---

## Tips

- **Preserve source references**: Note which file each piece of data came from
- **Prioritize metrics**: "Shipped feature" < "Shipped feature used by 10K users"
- **Anonymize carefully**: If removing names, keep role context
- **Check dates**: Ensure no overlapping periods, consistent formatting
- **Cross-reference**: Same project might appear in experience AND as case study
- **Images**: Store in `/public/images/`, reference as `/images/filename.png`

---

## Dependencies

- Node.js (for validation scripts)
- `npm run validate` command
- Zod schemas in `src/lib/schemas.ts`

No additional packages required.
