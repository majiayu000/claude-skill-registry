---
name: ralph-content
description: Generate high-quality content iteratively with LLM-driven orchestration. Uses Opus 4.5 for all decisions including quality gates, iteration choices, and verification. No deterministic scripts.
allowed-tools: Read, Edit, Create, Grep, Glob, LS, WebSearch, Execute, TodoWrite
user_invocable: true
argument-hint: <topic> [--type newsletter|lead_magnet|linkedin|instagram] [--voice klosterman|dan_shipper|tina_he|etc.] [--verify] [--diagrams N]
---

# RALPH-Content: Iterative Content Generation

Generate newsletters, lead magnets, LinkedIn posts, and Instagram scripts with iterative quality improvement. All orchestration decisions are made by Claude Opus 4.5—no deterministic scripts, regex parsing, or hard-coded logic.

## Invocation

```bash
/ralph-content "How psilocybin affects metabolic health" --type newsletter
/ralph-content "NAD+ supplementation deep dive" --type lead_magnet --diagrams 5
/ralph-content "Time-restricted eating benefits" --type linkedin
/ralph-content "Why we believe what we believe about supplements" --type newsletter --voice klosterman
```

**Arguments:**
- `<topic>` - The subject to write about (required)
- `--type` - Content type: newsletter (default), lead_magnet, linkedin, instagram, regulatory_brief
- `--voice` - Voice style: dan_shipper, tina_he, katie_parrott, klosterman, huberman, etc.
- `--verify` - Enable fact verification phase (cross-check claims with Perplexity). **Auto-enabled for regulatory_brief**
- `--diagrams N` - Number of diagrams to generate (default: 2 for newsletter, 5 for lead_magnet, 0 for regulatory_brief)

---

## Core Principle: LLM-Driven Everything

You (Claude Opus 4.5) make ALL decisions:
- What research queries to run
- Whether research is sufficient
- When content quality passes
- Which diagrams need regeneration
- When to iterate vs proceed

There is NO:
- Regex parsing of outputs
- Hard-coded iteration limits
- Deterministic state machines
- Script-based orchestration

You read the context files, understand the quality criteria, and make judgments.

---

## Workflow

### Phase 0: Load Context

Before starting, read:
1. `.ralph-content/progress.txt` - Prior learnings (if exists)
2. The context files in this skill's `context/` directory (already loaded via skill)

Note any patterns or gotchas from previous runs.

### Phase 1: Research (Perplexity Deep Research)

**Goal:** Gather comprehensive, verifiable information on the topic using Perplexity's deep research model.

**IMPORTANT:** Use Perplexity via OpenRouter for deep research, NOT the basic WebSearch tool.

**How to call Perplexity:**
```bash
API_KEY=$(grep OPENROUTER_API_KEY .env | cut -d'=' -f2)
curl -s https://openrouter.ai/api/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "model": "perplexity/sonar-deep-research",
    "messages": [{"role": "user", "content": "YOUR RESEARCH QUERY HERE"}]
  }' | jq -r '.choices[0].message.content'
```

**Actions:**
1. Formulate a comprehensive research query that covers:
   - Molecular/mechanistic details
   - Clinical data with study citations (author, journal, year, n, findings)
   - Latest research (specify 2024-2025)
   - Practical implications
2. Call Perplexity `sonar-deep-research` via OpenRouter using the Bash tool
3. Evaluate: Is the research sufficient for the content type?
   - For newsletter: Need specific studies, company examples, expert quotes
   - For lead magnet: Need mechanism details, clinical data, practical applications
4. If insufficient, run additional targeted Perplexity queries
5. Track sources for later citation

**Why Perplexity Deep Research:**
- Returns comprehensive, well-sourced academic content
- Includes specific study citations (author, journal, year)
- Provides mechanistic depth not available from basic web search
- Single query can return 10,000+ words of research synthesis

**Quality Check (you decide):**
- Do I have specific names, numbers, and timeframes?
- Do I have 3+ examples for evidence cascades?
- Do I have mechanism details, not just surface claims?
- Are my sources from peer-reviewed journals with proper citations?

### Phase 2: Draft + Self-Critique Loop

**Goal:** Generate content that passes the quality rubric.

**Actions:**
1. Write the first draft using:
   - Every.to voice patterns from `context/every-voice-patterns.md`
   - Appropriate format blueprint based on content type
   - Research gathered in Phase 1

2. Self-critique against the rubric:
   - For newsletter: 8-point Every.to rubric
   - For lead magnet: 10-point lead magnet rubric
   - For LinkedIn: 14-point LinkedIn rubric
   - For Instagram: 10-point script rubric

3. For each failing criterion, identify:
   - What specifically failed
   - Where in the content
   - How to fix it

4. Revise the content to address failures

5. Re-evaluate. Repeat until you judge the content ready.

**Key Insight:** This is NOT "generate, parse JSON, call critic, parse rubric, call reviser." It's you reading your own work, evaluating it honestly, and improving it in the same context.

### Phase 3: Fact Verification (if --verify flag or regulatory_brief)

**Goal:** Ensure claims are accurate, citations are correct, and sources are reputable.

**For regulatory_brief type, this phase is MANDATORY and expanded.**

**Actions:**

#### 3A. Source Credibility Audit
Before verifying claims, audit ALL cited sources for credibility:

**ACCEPTABLE sources:**
- Peer-reviewed journals (PubMed, PMC, MDPI, Nature, Science, etc.)
- Official regulatory bodies (FDA.gov, EMA.europa.eu, WHO)
- Academic institutions (.edu domains)
- Professional medical associations
- StatPearls/NCBI Bookshelf
- Wikipedia (for general/regulatory reference only, note as such)

**REJECT and replace:**
- Ecommerce sites selling the product being discussed
- Supplement/peptide vendor sites (e.g., peptidesciences.com, cosmicnootropic.com)
- Biased commercial sources
- Anonymous blogs without citations
- Social media posts

If a rejected source is found, search for a peer-reviewed alternative that supports the same claim.

#### 3B. Citation Accuracy Validation
For each citation, verify:
1. **Author attribution** - Correct authors listed (not misattributed)
2. **Year** - Publication year is accurate
3. **Journal/Source** - Correct journal name
4. **Claim mapping** - Citation actually supports the claim it's attached to

Common errors to catch:
- Wrong author (study may have multiple related papers)
- Wrong year (confusing similar studies)
- Citation supports a different claim than stated

#### 3C. Claim Verification
1. Identify the 3-5 most significant claims in the content
2. For each claim, use `WebSearch` to cross-verify with primary sources
3. If a claim is inaccurate:
   - Correct it with accurate information
   - Update the source citation
4. If a claim cannot be verified:
   - Either remove it or mark it as "preliminary" with appropriate hedging

#### 3D. Reasoning Consistency Check (for multi-document sets)
When creating related documents (e.g., multiple safety briefs), ensure:
1. **Consistent evidence weighting** - Same types of evidence receive similar weight across documents
2. **Explicit reasoning** - If conclusions differ, the justification is explicit
3. **Proportional conclusions** - Stronger evidence → stronger conclusions

**Example:** If Document A has human trial data and Document B only has preclinical data, Document A should not receive a weaker conclusion unless there's explicit justification (e.g., Document B has class-level regulatory precedent).

### Phase 4: Diagram Generation + Validation

**Goal:** Create SVG diagrams that render correctly and illuminate concepts.

**Actions:**
1. Identify concepts that would benefit from visualization
2. For each diagram:
   a. Choose the appropriate diagram type (mechanism, comparison, process, etc.)
   b. Generate SVG code following `context/diagram-guidelines.md`
   c. **Self-validate the SVG:**
      - Parse the SVG mentally—check text positions vs container bounds
      - Verify viewBox has sufficient size for content
      - Confirm text has 40px+ padding from edges
      - Check that text inside containers is FULLY contained
      - Verify color palette compliance
   d. If validation fails, regenerate with specific fixes

**Validation Example:**
"I see text at y=380 in a viewBox of height 400. With 40px padding requirement, the lowest y for text should be 360. This will overflow. I need to either increase the viewBox height or move the text up."

### Phase 5: Assembly

**Goal:** Compose final HTML output.

**Actions:**
1. For newsletter: Compose email-ready HTML with embedded diagrams
2. For lead magnet: Compose full HTML document with all sections
3. For LinkedIn: Format as plain text with appropriate line breaks
4. For Instagram: Format as script with HOOK / BODY / CTA markers

Use templates from `context/ngm-style-guide.md`.

### Phase 6: Publish + Learn

**Goal:** Save output and capture learnings.

**Actions:**
1. Save the content:
   - Newsletter: `content/social-content/newsletters/YYYY-MM-DD-{slug}.html`
   - Lead magnet: `content/learn-platform/lead-magnets/{slug}.html` + `.json`
   - LinkedIn: `content/social-content/linkedin-posts/YYYY-MM-DD-{slug}.md`
   - Instagram: `content/social-content/instagram-scripts/YYYY-MM-DD-{slug}.md`

2. Update `.ralph-content/progress.txt`:
   - What worked well
   - What needed iteration
   - Patterns discovered
   - Gotchas to avoid

3. Git commit with quality summary:
   ```
   feat: Add {type}: {title}
   
   - Quality: Passed {N}/{total} criteria on iteration {M}
   - Diagrams: {N} generated, {N} validated
   - Research: {N} sources cited
   
   Co-authored-by: factory-droid[bot] <138933559+factory-droid[bot]@users.noreply.github.com>
   ```

---

## Content Type Specifics

### Newsletter
- **Format:** Email-ready HTML
- **Length:** 1200-2000 words
- **Diagrams:** 2-3 SVG
- **Quality rubric:** Every.to 8-point
- **Voice:** Select based on content (Dan Shipper, Tina He, etc.)

### Lead Magnet
- **Format:** Full HTML document
- **Length:** ~1000 words
- **Diagrams:** 3-7 SVG
- **Additional:** Mechanism table, references section
- **Voice:** Andrew Huberman style

### LinkedIn
- **Format:** Plain text with line breaks
- **Length:** 200-300 words
- **Diagrams:** 1 SVG (for image post)
- **Quality rubric:** 14-point LinkedIn rubric

### Instagram
- **Format:** Script with sections
- **Duration:** 30-90 seconds spoken
- **Diagrams:** None (video format)
- **Quality rubric:** 10-point script rubric

### Regulatory Brief (NEW)
- **Format:** Print-optimized HTML (8.5" × 11", 0.75" margins)
- **Length:** One page (~600-800 words)
- **Diagrams:** 0-1 (tables preferred)
- **Quality rubric:** 12-point regulatory brief rubric
- **Verification:** MANDATORY (--verify auto-enabled)
- **Voice:** Formal, objective, evidence-based

**Structure for regulatory briefs:**
1. **Header** - Document type, subject, key identifiers (MW, sequence, CAS#)
2. **Section 1: Safety Data Summary**
   - Clinical trials (with n, design, key findings)
   - Observational/real-world data
   - Route-specific considerations (table format)
   - Adverse event profile (common/uncommon/rare)
   - Safety signals (Known/Theoretical/Absent)
3. **Section 2: Regulatory Precedent**
   - EMA/non-U.S. approvals
   - Historical FDA position
   - Analogous drug precedents
4. **Section 3: Conclusion**
   - Evidence synthesis
   - Explicit statement of evidence gaps
   - Recommendation with conditions
5. **References** - All with clickable links, peer-reviewed sources only

**Output location:** `content/social-content/newsletters/YYYY-MM-DD-{slug}.html` (+ `.json`)

---

## Example Run

```
User: /ralph-content "How cold exposure affects brown adipose tissue" --type newsletter --verify

You (thinking through each phase):

PHASE 0: CONTEXT
- Reading progress.txt... Previous runs show diagram text overflow was common issue.
  I'll be extra careful with text positioning in diagrams.

PHASE 1: RESEARCH
- Query 1: "cold exposure brown adipose tissue activation mechanisms 2025 2026 studies"
  [WebSearch results with studies]
- Query 2: "BAT thermogenesis UCP1 clinical applications"
  [WebSearch results with mechanism details]
- Evaluating: I have Hanssen et al. 2015, Cypess et al. 2009, specific activation 
  temperatures, and metabolic rate increases. Sufficient for newsletter.

PHASE 2: DRAFT + CRITIQUE
- Writing draft with concrete scenario hook...
- Self-critique against 8 points:
  ✓ Specificity: Named researchers, 17.5°C threshold, 5-15% metabolic increase
  ✗ Evidence cascade: Only 2 studies stacked, need 3+
  ✓ Colon technique: Used 4 times
  ✓ Em-dash clarity: Used for definitions and contrast
  ✓ One-sentence paragraphs: 4 strategic placements
  ✓ Concrete opening: Dr. Cypess case at Joslin
  ✓ Voice: Confident, specific
  ✓ Forward-looking: Ends with implications for metabolic practice
- Revising: Adding Ouellet et al. 2012 to evidence cascade...
- Re-evaluating: All 8 criteria now pass.

PHASE 3: VERIFICATION
- Claim: "Cold exposure at 17-19°C activates BAT"
  [WebSearch confirms - Hanssen et al., Cell Metabolism]
- Claim: "5-15% increase in metabolic rate"
  [WebSearch confirms - multiple sources]
- All key claims verified.

PHASE 4: DIAGRAMS
- Concept 1: BAT activation mechanism (pathway diagram)
  - Generating SVG...
  - Validating: Text at y=350 in 400-height viewBox, with 40px padding = OK
  - Container at height 120 with 3 text lines (75px) + 80px padding = needs 155px, FAIL
  - Regenerating with taller container...
  - Re-validating: Container now 180px, text fits with padding. PASS.
- Concept 2: Cold vs thermoneutral comparison
  - Generating SVG...
  - Validating: All checks pass.

PHASE 5: ASSEMBLY
- Composing email HTML with diagrams embedded...

PHASE 6: PUBLISH
- Saving to content/social-content/newsletters/2026-01-18-cold-exposure-bat.html
- Updating progress.txt with learnings
- Git commit
```

---

## Example: Regulatory Brief Run

```
User: /ralph-content "FDA safety brief for DSIP peptide" --type regulatory_brief

You (thinking through each phase):

PHASE 0: CONTEXT
- Reading progress.txt... Previous regulatory brief run had citation attribution error.
  I'll verify each citation's author/year against PubMed.

PHASE 1: RESEARCH (Extended for regulatory)
- Query 1: "DSIP delta sleep inducing peptide clinical trials safety human studies PubMed"
  [WebSearch returns 4 clinical studies from 1980s-1990s]
- Query 2: "DSIP regulatory approval Russia Deltaran Ministry of Health"
  [WebSearch returns registration info]
- Query 3: "DSIP LD50 toxicity animal studies lethal dose"
  [WebSearch confirms no lethal dose established]
- Evaluating: I have human trial data (n=~200 total), Russian approval, toxicity profile.
  Sufficient for regulatory brief.

PHASE 2: DRAFT + CRITIQUE
- Writing with regulatory brief structure...
- Self-critique against 12-point regulatory rubric:
  ✓ Clinical data with n, design, findings
  ✓ Route-specific table
  ✓ Safety signals categorized (Known/Theoretical/Absent)
  ✓ Regulatory precedent documented
  ✗ Conclusion needs explicit evidence gap statement
- Revising conclusion to explicitly state limitations...
- Re-evaluating: All 12 criteria now pass.

PHASE 3: VERIFICATION (MANDATORY for regulatory_brief)
- Step 3A: Source Credibility Audit
  - Found cosmicnootropic.com in research notes - REJECT (vendor site)
  - Searching for peer-reviewed alternative...
  - Found Popovich et al. 2003 (PMID 12782416) - ACCEPT
- Step 3B: Citation Accuracy Validation
  - Ref [1] claims "Schneider-Helmert 1988" but PubMed 1299794 shows "Bes F et al. 1992"
  - CORRECTING: Update author and year
- Step 3C: Claim Verification
  - Claim: "LD50 never determined" - Verified via Graf & Kastin 1984 review
  - Claim: "97% opiate addicts improved" - Verified via Dick 1984 (PMID 6548969)
- Step 3D: Reasoning Consistency
  - N/A for single document (check if creating related briefs)

PHASE 4: DIAGRAMS
- Regulatory briefs use tables, not diagrams. Skipping.

PHASE 5: ASSEMBLY
- Composing print-optimized HTML with NGM styling...

PHASE 6: PUBLISH
- Saving to content/social-content/newsletters/2026-01-27-fda-safety-brief-dsip.html
- Creating JSON metadata file
- Updating progress.txt with citation validation learning
- Git commit
```

---

## Quality Over Speed

This skill prioritizes quality over speed. It's acceptable to:
- Run 4-5 research queries if needed
- Iterate on content 3+ times
- Regenerate diagrams multiple times
- Take the time to verify claims

The goal is content that meets Every.to editorial standards—content the team would be proud to publish.

---

## JSON Schema for Content Pipeline

**CRITICAL:** All content must be saved as JSON files to appear in `/content-pipeline`. The content-pipeline API reads JSON files from content directories.

### LinkedIn Post JSON Schema

```json
{
  "id": "unique-id",
  "createdAt": "2026-01-22T17:30:00.000Z",
  "content": "The full post text with\n\nline breaks preserved...",
  "meta": {
    "alphaIdea": "Short summary used as title in content pipeline",
    "hookType": "curiosity|stakes|contrarian|pattern",
    "wordCount": 195,
    "targetAudience": "longevity medicine professionals"
  },
  "quality": {
    "iterations": 1,
    "passed": true,
    "scores": {
      "pattern_interrupt": true,
      "hook_under_150_chars": true,
      "creates_curiosity": true,
      "has_clear_thesis": true,
      "uses_line_breaks": true,
      "avoids_wall_of_text": true,
      "follows_hook_expand_close": true,
      "has_specific_numbers": true,
      "avoids_jargon": true,
      "has_original_insight": true,
      "stays_focused": true,
      "has_subtle_cta": true,
      "paragraphs_punchy": true,
      "intellectually_honest": true
    }
  },
  "status": "draft",
  "images": []
}
```

**Required fields for display:**
- `id` - Unique identifier
- `createdAt` - ISO 8601 timestamp (used for sorting)
- `content` - Full post text
- `meta.alphaIdea` - **Used as title in content pipeline**
- `quality.passed` - Boolean for quality badge
- `quality.iterations` - Number for iteration count
- `quality.scores` - Object with individual rubric scores

### Newsletter JSON Schema

```json
{
  "id": "unique-id",
  "createdAt": "2026-01-22T17:30:00.000Z",
  "title": "The Newsletter Title",
  "subtitle": "Optional subtitle shown in preview",
  "textContent": "## Full markdown content\n\nWith all sections...",
  "hasHtmlContent": true,
  "status": "draft",
  "meta": {
    "format": "research_synthesis|ai_in_clinic_playbook|deep_dive",
    "length": "short|medium|long",
    "wordCount": 680,
    "estimatedReadTime": 3,
    "targetAudience": "longevity medicine professionals"
  },
  "quality": {
    "iterations": 1,
    "passed": true,
    "scores": {
      "specificity_check": true,
      "evidence_cascade_present": true,
      "colon_technique_used": true,
      "em_dash_clarity": true,
      "one_sentence_emphasis": true,
      "concrete_over_abstract": true,
      "voice_authenticity": true,
      "forward_looking_conclusion": true
    }
  }
}
```

**Required fields for display:**
- `id` - Unique identifier
- `createdAt` - ISO 8601 timestamp
- `title` - **Used as title in content pipeline**
- `textContent` - Full markdown content (shown in Markdown view)
- `hasHtmlContent` - Set to `true` if HTML file exists (enables preview iframe)
- `quality.passed`, `quality.iterations` - For quality badge

**Note:** The HTML file must have the same base filename as the JSON for the preview iframe to work.

### Lead Magnet JSON Schema

The content pipeline supports **two formats**. Use the **new format** for all new content.

#### New Format (Recommended)

```json
{
  "id": "unique-slug",
  "createdAt": "2026-01-22T17:30:00.000Z",
  "title": "The Lead Magnet Title",
  "subtitle": "Optional subtitle",
  "slug": "unique-slug",
  "sections": [
    {
      "title": "Section Title",
      "content": ["paragraph 1", "paragraph 2"]
    }
  ],
  "unexpectedDiscoveries": [
    "Discovery 1",
    "Discovery 2"
  ],
  "frameworks": [
    {
      "name": "Framework Name",
      "description": "Framework description"
    }
  ],
  "references": [
    {
      "title": "Reference title with authors and journal"
    }
  ],
  "accessKeyword": "OPTIONAL_KEYWORD"
}
```

#### Legacy Format (Still Supported)

```json
{
  "id": "unique-id",
  "title": "The Lead Magnet Title",
  "slug": "unique-slug",
  "created_at": "2026-01-22T00:00:00.000Z",
  "keyword": "KEYWORD",
  "key_findings": [
    { "finding": "Finding text", "source": "Source citation" }
  ],
  "mechanisms": [
    { "mechanism": "Mechanism name", "clinical_takeaway": "Clinical takeaway" }
  ],
  "references": ["Reference 1 as string", "Reference 2 as string"]
}
```

**Required fields for display:**
- `id` - Unique identifier
- `createdAt` OR `created_at` - ISO 8601 timestamp
- `title` - **Used as title in content pipeline**

**Content fields (use one set):**
- New: `sections`, `frameworks`, `unexpectedDiscoveries`
- Legacy: `key_findings`, `mechanisms`

**References:** Supports both `[{title: "..."}]` and `["string"]` formats

**Keyword:** Supports both `accessKeyword` and `keyword`

**Note:** The "View HTML Lead Magnet" button always appears for lead magnets (HTML file must exist with same base name as JSON).

**Diagram PDF Export:** Lead magnets support diagram-only PDF export via the "Download Diagram PDF" button. Features:
- **Cover page** with scroll-stopping hook (auto-generated from title), Newsreader/serif typography, and NGM branding
- **Access keyword** displayed prominently with "Comment below to get the full analysis" CTA—auto-generated from title if not provided in JSON (`accessKeyword` or `keyword` field)
- **One diagram per page**, scaled to maximize page real estate
- **JPEG compression** for small file sizes (~300-400KB)
- **LinkedIn carousel optimized**: landscape orientation, swipe hint, visual hierarchy

The hook is auto-generated using pattern matching on the title/subtitle (e.g., "What 30+ Top Researchers Agree On" for consensus topics, "The Shift Nobody Saw Coming" for revolution topics).

### Instagram Script JSON Schema

```json
{
  "id": "unique-id",
  "createdAt": "2026-01-22T17:30:00.000Z",
  "meta": {
    "topic": "Short topic used as title"
  },
  "script": {
    "hook": "First 3 seconds text",
    "body": "Main content of the script...",
    "cta": "Call to action text",
    "totalDuration": 45
  },
  "quality": {
    "passed": true
  }
}
```

**Required fields for display:**
- `id` - Unique identifier
- `createdAt` - ISO 8601 timestamp
- `meta.topic` - **Used as title in content pipeline**
- `script.hook`, `script.body`, `script.cta`, `script.totalDuration`
- `quality.passed` - Boolean for quality badge

---

## Files

### Output Locations
- Newsletters: `content/social-content/newsletters/` (both `.html` AND `.json`)
- Lead Magnets: `content/learn-platform/lead-magnets/` (both `.html` AND `.json`)
- LinkedIn: `content/social-content/linkedin-posts/` (`.json` only)
- Instagram: `content/social-content/instagram-scripts/` (`.json` only)

### API Endpoints
- View Lead Magnet HTML: `GET /api/lead-magnet-html/[slug]`
- Download Diagram PDF: `GET /api/lead-magnet-diagrams-pdf/[slug]` - Generates LinkedIn-optimized PDF with cover page + diagrams (uses puppeteer + jspdf)

### Learning Persistence
- Progress: `.ralph-content/progress.txt`

### Context (Read at Start)
- `context/every-voice-patterns.md` - Voice patterns and techniques
- `context/quality-rubrics.md` - All quality criteria
- `context/diagram-guidelines.md` - SVG generation rules
- `context/ngm-style-guide.md` - Brand and HTML templates
