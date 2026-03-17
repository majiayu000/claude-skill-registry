---
name: ai-daily-digest
description: Daily AI news digest covering technical advances, business news, and engineering impact. Aggregates from research papers, tech blogs, HN, newsletters. Use daily for staying current on AI developments.
argument-hint: "[--focus technical|business|engineering|leadership]"
allowed-tools: WebSearch, WebFetch, Read, Write
user-invocable: true
---

# AI Daily Digest Skill

Generate comprehensive daily AI news digest with technical, business, and engineering coverage.

## Arguments

Parse from `$ARGUMENTS`:

- `--focus [technical|business|engineering|leadership|all]` — Default: all

## State Files

### Last Run Date

Track last run date in:

```text
./findings/ai-daily-digest/.last-run
```

Format: `YYYY-MM-DD`

### Previous Stories (Deduplication)

Track previously covered stories in:

```text
./findings/ai-daily-digest/.covered-stories
```

**Format:** Each story on one line with pipe-separated fields:

```text
{date}|{story_id}|{url}
```

Where:
- `date` — Date story was covered (YYYY-MM-DD)
- `story_id` — Normalized identifier: lowercase, no spaces, key terms only (e.g., `falcon-h1r-7b-release`, `xai-20b-funding`, `openai-gpt5-launch`)
- `url` — Source URL

**Example:**

```text
2026-01-28|deepseek-r1-release|https://api-docs.deepseek.com/news/news250120
2026-01-29|falcon-h1r-7b-release|https://falcon-lm.github.io/blog/falcon-h1r-7b/
2026-01-29|xai-20b-funding|https://news.crunchbase.com/venture/biggest-funding-rounds
```

Keep last 300 entries (trim oldest when exceeding).

**Purpose:** Prevents duplicate stories across days. Web searches return same popular stories regardless of date filters. Story ID enables fuzzy matching across different URLs covering same event.

## Friday Weekly Recap Mode

When running on Friday, automatically enable broader research:

- **Extended date range:** Cover full week (7 days) regardless of last run
- **More search queries:** Add "this week in AI", "AI weekly roundup" patterns
- **Lower-tier sources:** Include more community sources (Reddit, Twitter)
- **Catch-up section:** Add "📅 Stories You Might Have Missed" section
- **Digest title:** Use "Weekly Recap" instead of "Daily Digest"
- **Blog discovery:** Search for new indie bloggers (see below)

### Blog Discovery (Friday)

Search for new interesting smaller blogs:

```text
"AI blog" OR "ML blog" interesting {date_range}
site:substack.com AI machine learning
site:medium.com AI LLM practical (filter by quality)
site:dev.to AI machine learning tutorial
HN "Show HN" AI blog
```

When finding new quality blogs:

1. Add to "🆕 New Blogs Discovered" section in digest
2. Suggest adding to `sources.md` if consistently good

Quality signals:

- Original content (not aggregation)
- Technical depth
- Practical examples
- Active (posted in last 3 months)

## Workflow

### Phase 1: Setup

1. Read `sources.md` for search patterns and URLs
2. Read `output-template.md` for digest format
3. Parse arguments for focus area
4. **Read `.last-run` file:**
   - If exists: set date range from last run date to today
   - If missing: default to past 7 days (first run)
5. Calculate days since last run for digest header
6. **Read `.covered-stories` file (CRITICAL):**
   - Parse each line: `{date}|{story_id}|{url}`
   - Build two lookup sets:
     - `covered_ids` — Set of all story_ids
     - `covered_urls` — Set of all URLs
   - If file missing or old format (URLs only): migrate by extracting story_ids, or start fresh
7. **Friday check:** If today is Friday, enable weekly recap mode

### Phase 2: Technical Research

**Skip if focus excludes technical**

Search patterns:

- `AI LLM breakthrough OR release site:arxiv.org {date_range}`
- `AI model release OR launch {date_range}`
- `LLM framework tool release {date_range}`
- `site:huggingface.co blog {date_range}`
- `site:openai.com blog {date_range}`
- `site:anthropic.com news {date_range}`

Collect:

- New model releases (GPT, Claude, Gemini, Llama, etc.)
- Research paper highlights
- Framework/tool updates (LangChain, LlamaIndex, vLLM, etc.)
- Benchmark results

### Phase 3: Business Research

**Skip if focus excludes business**

Search patterns:

- `AI startup funding OR acquisition {date_range}`
- `AI company valuation OR investment {date_range}`
- `site:techcrunch.com AI {date_range}`
- `site:venturebeat.com AI {date_range}`
- `OpenAI OR Anthropic OR Google AI business {date_range}`

Collect:

- Funding rounds
- Acquisitions/mergers
- Product launches
- Partnership announcements
- Market analysis

### Phase 4: Engineering Impact Research

**Skip if focus excludes engineering**

Search patterns:

- `AI coding assistant OR developer tools {date_range}`
- `AI engineering workflow productivity {date_range}`
- `AI job market developer skills {date_range}`
- `site:news.ycombinator.com AI OR LLM {date_range}`
- `site:reddit.com/r/MachineLearning {date_range}`
- `site:reddit.com/r/LocalLLaMA {date_range}`

Collect:

- New dev tools and integrations
- Workflow automation updates
- Job market trends
- Community discussions and sentiment

### Phase 5: Leadership Research

**Skip if focus excludes leadership**

Search patterns:

- `AI leadership engineering management {date_range}`
- `AI team strategy CTO VP engineering {date_range}`
- `site:hbr.org AI leadership management`
- `site:mckinsey.com AI leadership`
- `AI transformation organizational change {date_range}`
- `engineering leadership AI adoption {date_range}`

Collect:

- AI strategy for engineering orgs
- Team structure changes due to AI
- Leadership perspectives on AI adoption
- Org transformation case studies
- Skills and competencies for AI era

### Phase 6: GitHub Trending AI

Discover trending AI/ML repositories and tools:

**Direct fetch:**

- Fetch `https://github.com/trending?since=daily&spoken_language_code=en` for overall trending
- Fetch `https://github.com/trending/python?since=daily` (most AI repos)
- Fetch `https://github.com/trending/jupyter-notebook?since=daily` (ML notebooks)

**Search patterns:**

- `site:github.com "stars" AI LLM new {date_range}`
- `site:github.com trending machine learning {date_range}`
- `github AI tool "just released" OR "new release" {date_range}`
- `site:news.ycombinator.com "Show HN" github AI {date_range}`

**Collect:**

- New AI/ML repos gaining traction (100+ stars recently)
- Framework releases and major updates
- Interesting tools/demos with code
- Open-source model implementations

**Quality signals:**

- Stars growth rate (not just total)
- Active development (recent commits)
- Good documentation/README
- Practical utility for engineers

**Dedup note:** Same repo may appear across days — use `{repo-owner}-{repo-name}` as story_id.

**IMPORTANT:** Include interesting/valuable GitHub repos even if not brand new (e.g., trending for past week, recent major updates, or popular repos not yet covered). Check against `.covered-stories` - if repo not already covered, include it regardless of age. Value and utility matter more than recency for GitHub content.

### Phase 7: AI Tools for Professionals

Discover new AI apps/tools for specific professional domains:

**Software Engineers:**

Search patterns:

- `AI developer tools new release {date_range}`
- `AI coding assistant launch {date_range}`
- `AI code review tool {date_range}`
- `AI debugging assistant {date_range}`
- `"AI for developers" tool app {date_range}`
- `site:producthunt.com AI developer coding {date_range}`
- `AI IDE plugin extension {date_range}`
- `AI terminal CLI tool {date_range}`

Collect:

- New AI coding assistants (beyond Copilot/Cursor)
- AI-powered dev tools (testing, debugging, docs)
- CLI tools with AI features
- IDE plugins and extensions
- Code review and analysis tools
- AI for DevOps/infrastructure

**Photographers & Videographers:**

Search patterns:

- `AI photo editing tool new {date_range}`
- `AI video editing software {date_range}`
- `AI image generation photography {date_range}`
- `AI video upscaling enhancement {date_range}`
- `"AI for photographers" tool app {date_range}`
- `"AI for videographers" tool app {date_range}`
- `site:producthunt.com AI photo video {date_range}`
- `AI color grading tool {date_range}`
- `AI background removal tool {date_range}`
- `AI video stabilization {date_range}`

Collect:

- Photo editing AI tools (retouching, enhancement)
- Video editing assistants
- AI color grading/correction
- Background removal/replacement
- Image upscaling and restoration
- AI-powered camera apps
- Video generation and editing
- Motion tracking and VFX tools

**Writers & Content Creators:**

Search patterns:

- `AI writing tool new {date_range}`
- `AI content generation platform {date_range}`
- `"AI for writers" OR "AI writing assistant" {date_range}`
- `site:producthunt.com AI writing content {date_range}`
- `AI copywriting tool {date_range}`
- `AI blog post generator {date_range}`
- `AI script writing tool {date_range}`

Collect:

- AI writing assistants (beyond ChatGPT)
- Content generation platforms
- SEO-optimized content tools
- Script and screenplay tools
- Long-form content tools
- AI editing and proofreading

**Designers:**

Search patterns:

- `AI design tool new {date_range}`
- `AI Figma plugin {date_range}`
- `"AI for designers" tool app {date_range}`
- `site:producthunt.com AI design {date_range}`
- `AI logo generator OR brand design {date_range}`
- `AI UI UX design tool {date_range}`
- `generative design AI {date_range}`

Collect:

- AI design tools and platforms
- Figma/Sketch AI plugins
- Logo and brand design generators
- UI/UX design assistants
- Generative design tools
- Design system automation

**Researchers & Academics:**

Search patterns:

- `AI research tool new {date_range}`
- `AI literature review OR research assistant {date_range}`
- `"AI for researchers" OR "AI for academics" {date_range}`
- `AI paper summarization tool {date_range}`
- `AI citation management {date_range}`
- `AI data analysis research {date_range}`

Collect:

- Literature review tools
- Paper summarization services
- Research assistants
- Data analysis platforms
- Citation management tools
- Lab automation software

**Educators & Teachers:**

Search patterns:

- `AI education tool new {date_range}`
- `AI tutoring platform OR adaptive learning {date_range}`
- `"AI for teachers" OR "AI for educators" {date_range}`
- `site:producthunt.com AI education learning {date_range}`
- `AI lesson planning tool {date_range}`
- `AI grading assessment {date_range}`

Collect:

- AI tutoring platforms
- Adaptive learning systems
- Lesson planning assistants
- Assessment and grading tools
- Curriculum design tools
- Student engagement platforms

**Healthcare Professionals:**

Search patterns:

- `AI healthcare tool new {date_range}`
- `AI medical imaging OR diagnostics {date_range}`
- `"AI for doctors" OR "AI for clinicians" {date_range}`
- `AI clinical decision support {date_range}`
- `AI EHR electronic health records {date_range}`
- `AI medical scribing documentation {date_range}`

Collect:

- Medical imaging AI tools
- Diagnostic assistance
- Clinical decision support
- Medical documentation/scribing
- EHR integration tools
- Patient care optimization

**Legal Professionals:**

Search patterns:

- `AI legal tool new {date_range}`
- `AI contract review OR analysis {date_range}`
- `"AI for lawyers" OR "legal tech AI" {date_range}`
- `AI legal research platform {date_range}`
- `AI document automation legal {date_range}`
- `AI compliance tool {date_range}`

Collect:

- Contract review and analysis
- Legal research platforms
- Document automation
- Compliance tools
- Case law analysis
- E-discovery tools

**Finance & Accounting:**

Search patterns:

- `AI finance tool new {date_range}`
- `AI accounting automation {date_range}`
- `"AI for finance" OR "AI for accounting" {date_range}`
- `site:producthunt.com AI finance fintech {date_range}`
- `AI fraud detection financial {date_range}`
- `AI forecasting financial {date_range}`

Collect:

- Accounting automation
- Financial forecasting tools
- Fraud detection systems
- Tax preparation AI
- Audit assistance
- Investment analysis tools

**Quality signals (all domains):**

- Actually useful (not just demos)
- Accessible pricing or free tier
- Active development
- Good reviews/community reception
- Clear value proposition for target profession

### Phase 8: AI Application Domains

Discover AI applications across specific domains:

**AI in Education:**

Search patterns:

- `AI education platform OR edtech {date_range}`
- `adaptive learning AI personalized education {date_range}`
- `AI tutoring breakthrough {date_range}`
- `AI assessment education {date_range}`

Collect:

- New educational AI platforms
- Adaptive learning breakthroughs
- AI tutoring innovations
- Assessment technology
- Educational AI research

**AI in Healthcare & Biotech:**

Search patterns:

- `AI drug discovery OR biotech {date_range}`
- `AI diagnostics medical breakthrough {date_range}`
- `AI clinical trials healthcare {date_range}`
- `AI protein folding OR molecular {date_range}`
- `AI radiology pathology imaging {date_range}`

Collect:

- Drug discovery AI advances
- Diagnostic breakthroughs
- Clinical trial innovations
- Molecular biology AI
- Medical imaging advances
- Precision medicine tools

**AI in Creative Industries:**

Search patterns:

- `AI music generation OR composition {date_range}`
- `AI game development OR procedural generation {date_range}`
- `AI art generation breakthrough {date_range}`
- `AI film production OR VFX {date_range}`
- `AI voice cloning OR synthesis {date_range}`

Collect:

- Music generation tools
- Game development AI
- Art generation advances
- Film/VFX innovations
- Voice synthesis breakthroughs
- Creative AI tools

**AI in Robotics & Hardware:**

Search patterns:

- `AI robotics OR humanoid robot {date_range}`
- `embodied AI OR physical AI {date_range}`
- `robot learning OR manipulation {date_range}`
- `autonomous vehicle OR robotaxi {date_range}`
- `drone AI OR aerial robotics {date_range}`

Collect:

- Humanoid robot developments
- Embodied AI research
- Robot learning breakthroughs
- Autonomous vehicle advances
- Industrial robotics AI
- Consumer robotics

**AI in Gaming:**

Search patterns:

- `AI gaming NPC OR game AI {date_range}`
- `procedural generation AI game {date_range}`
- `AI game testing OR QA {date_range}`
- `AI esports OR competitive gaming {date_range}`

Collect:

- AI-powered NPCs
- Procedural generation tools
- Game testing automation
- AI in esports
- Game design AI

**AI in Scientific Research:**

Search patterns:

- `AI scientific discovery OR research {date_range}`
- `AI lab automation OR experiment {date_range}`
- `AI hypothesis generation {date_range}`
- `AI materials science OR chemistry {date_range}`
- `AI climate modeling OR simulation {date_range}`

Collect:

- Scientific discovery AI
- Lab automation advances
- Hypothesis generation tools
- Materials science AI
- Climate modeling breakthroughs
- Research acceleration tools

**Consumer AI Products:**

Search patterns:

- `AI consumer app launch {date_range}`
- `AI smartphone feature OR mobile {date_range}`
- `site:producthunt.com AI consumer {date_range}`
- `AI home automation OR smart home {date_range}`
- `AI personal assistant device {date_range}`

Collect:

- Consumer AI apps
- AI smartphone features
- Smart home innovations
- Personal AI assistants
- AI wearables
- Entertainment AI

### Phase 9: AI Safety & Ethics

**Search patterns:**

- `AI safety research OR alignment {date_range}`
- `AI ethics guidelines OR framework {date_range}`
- `AI regulation OR policy {date_range}`
- `site:anthropic.com alignment OR safety {date_range}`
- `AI incident OR failure {date_range}`
- `interpretability OR explainable AI {date_range}`
- `AI bias fairness {date_range}`

**Collect:**

- AI safety research updates
- Alignment breakthroughs
- Policy and regulation developments
- AI ethics frameworks
- Incident reports and lessons
- Interpretability advances
- Bias and fairness research
- Safety organization updates (Anthropic, OpenAI, DeepMind safety teams)

### Phase 10: Open Source AI Ecosystem

**Search patterns:**

- `open source AI model release {date_range}`
- `open weights OR open source LLM {date_range}`
- `site:huggingface.co open source {date_range}`
- `AI dataset release OR open data {date_range}`
- `democratizing AI OR AI democratization {date_range}`
- `EleutherAI OR LAION OR BigScience {date_range}`

**Collect:**

- Open source model releases
- Open weight models (Apache 2.0, MIT, etc.)
- New open datasets
- Community-driven projects
- Democratization initiatives
- Open source AI tools/infrastructure
- Collaborative research efforts

### Phase 11: AI Infrastructure & Hardware

**Search patterns:**

- `AI chip OR AI accelerator {date_range}`
- `GPU OR TPU OR AI compute {date_range}`
- `Groq OR Cerebras OR AI hardware {date_range}`
- `AI training infrastructure {date_range}`
- `model serving OR inference optimization {date_range}`
- `edge AI OR on-device AI {date_range}`
- `AI datacenter OR compute cluster {date_range}`

**Collect:**

- AI chip announcements
- Custom silicon developments
- Training infrastructure innovations
- Model serving platforms
- Inference optimization tools
- Edge AI hardware
- Datacenter AI architecture
- Compute efficiency breakthroughs

### Phase 12: Regional AI Developments

**Search patterns:**

- `European AI OR EU AI regulation {date_range}`
- `China AI OR Chinese AI development {date_range}`
- `Japan AI OR Japanese AI {date_range}`
- `Korea AI OR Korean AI {date_range}`
- `India AI development {date_range}`
- `AI policy Europe OR Asia {date_range}`
- `Mistral OR French AI {date_range}`

**Collect:**

- European AI developments (Mistral, regulation, research)
- Chinese AI advances (DeepSeek, ByteDance, etc.)
- Japanese AI initiatives
- Korean AI developments
- Indian AI ecosystem
- Regional policy differences
- Non-US AI companies
- Regional AI research

### Phase 13: YouTube AI Videos

Discover new interesting AI-related YouTube content:

**Search patterns:**

- `AI tutorial OR explanation site:youtube.com {date_range}`
- `LLM OR "large language model" site:youtube.com {date_range}`
- `AI news OR update site:youtube.com {date_range}`
- `machine learning explained site:youtube.com {date_range}`
- `AI coding assistant demo site:youtube.com {date_range}`
- `"AI paper" review OR breakdown site:youtube.com {date_range}`

**Priority channels** (check for recent uploads):

- 3Blue1Brown (math/ML visualizations)
- Andrej Karpathy (neural nets, AI education)
- Yannic Kilcher (paper reviews)
- Two Minute Papers (research highlights)
- AI Explained (news, analysis)
- Fireship (dev-focused AI content)
- Matt Wolfe (AI tools, news)
- The AI Advantage (practical tutorials)
- AI Jason (tutorials, tools)
- Prompt Engineering (practical LLM use)

**Collect:**

- Paper breakdowns and explanations
- AI tool demos and tutorials
- News roundups and analysis
- Technical deep dives
- Practical how-to videos

**Quality signals:**

- Educational value (not just hype)
- Technical accuracy
- Good production quality
- Useful for engineers
- Recent uploads (within date range)

**Dedup note:** Use `youtube-{channel}-{video-slug}` as story_id.

### Phase 14: Cool & Thought-Provoking Research

Search for surprising, mind-bending, or philosophical AI content:

Search patterns:

- `AI "mind-blowing" OR "incredible" demo {date_range}`
- `AI art OR creative unexpected {date_range}`
- `AI philosophical implications {date_range}`
- `site:twitter.com AI demo viral {date_range}`
- `site:reddit.com/r/singularity {date_range}`
- `AI "you won't believe" OR "wait what" {date_range}`
- `AI ethics dilemma OR thought experiment {date_range}`

Collect:

- Viral demos showing unexpected capabilities
- Creative/artistic AI applications
- Philosophical thought experiments
- "Wait, that's possible now?" moments
- Unusual cross-domain applications
- Dystopian/utopian implications worth pondering

**Quality filter:** Must genuinely provoke thought, not just clickbait.

### Phase 15: Newsletter & Blog Aggregation

**IMPORTANT:** Always search BOTH specific known sources AND broader platforms. Don't limit to listed authors—actively discover new quality content.

#### Specific Known Sources

**Check these high-quality sources:**

- Simon Willison's blog (simonwillison.net)
- Latent Space blog (latent.space)
- The Batch (deeplearning.ai/the-batch)
- Ben's Bites (bensbites.com)

**Indie bloggers** (check for recent posts):

- Lilian Weng, Jay Alammar, Eugene Yan
- Chip Huyen, Vicki Boykis, Hamel Husain
- Sebastian Ruder, swyx, François Chollet

Search pattern: `site:{blog_url} {date_range}` OR `site:{blog_url} 2026-02` (flexible date format)

#### Broader Platform Searches (REQUIRED)

**Always search these platforms for AI content:**

**Substack AI Content:**
- `site:substack.com AI OR LLM {date_range}`
- `site:substack.com machine learning February 2026`
- Look for: Technical analysis, AI engineering insights, research breakdowns

**Medium AI Articles:**
- `site:medium.com AI machine learning {date_range}`
- `site:medium.com "last week in AI" OR "AI trends"`
- Look for: Industry analysis, practical tutorials, trend pieces

**DEV.to AI Content:**
- `site:dev.to AI tutorial OR insights {date_range}`
- `site:dev.to machine learning OR LLM`
- Look for: Developer tutorials, tool reviews, practical guides

**General AI Blog Search:**
- `AI blog post {date_range} analysis insights`
- `"AI engineering" OR "ML engineering" blog post this week`
- `AI research blog post analysis {date_range}`

**Newsletter Discovery:**
- `"AI newsletter" OR "ML newsletter" latest issue 2026`
- `AI weekly newsletter {date_range}`
- Look for: Curated news, research roundups, industry updates

**Quality Signals for New Sources:**
- Original analysis (not just aggregation)
- Technical depth appropriate for engineers
- Recent activity (last 3 months)
- Clear expertise/credibility
- Practical insights

**When finding new quality blogs:**
1. Note in digest under "🆕 New Blogs & Sources Discovered" section
2. Include: Blog name, URL, focus area, why interesting
3. Consider suggesting addition to sources.md if consistently high quality

### Phase 16: Synthesis (CRITICAL - Dedup BEFORE Digest Generation)

**⚠️ CRITICAL: All deduplication MUST happen in this phase BEFORE generating digest in Phase 17.**

**Step 1: Generate story IDs for all collected items**

For each story found, generate a normalized `story_id`:

- Lowercase, hyphen-separated
- Include: company/product name + action + key detail
- Examples:
  - "Falcon-H1R 7B release" → `falcon-h1r-7b-release`
  - "xAI raises $20B" → `xai-20b-funding`
  - "OpenAI launches GPT-5" → `openai-gpt5-launch`
  - "Simon Willison on sandboxes" → `simonwillison-sandboxes-post`
  - "CEO AI anxiety survey" → `wef-ceo-ai-anxiety-survey`

**Step 2: Deduplicate within session**

Remove duplicate stories across sources (same event, different URLs).

**Step 3: Deduplicate against history (STRICT - USE IN-MEMORY DATA FROM PHASE 1)**

⚠️ **Use the `.covered-stories` data loaded in Phase 1 (in-memory `covered_ids` and `covered_urls` sets).**

**DO NOT re-read the file. DO NOT update the file yet.**

Filter out ANY story where:

1. **Exact story_id match** in `covered_ids` → SKIP (e.g., `falcon-h1r-7b-release` already covered)
2. **Similar story_id** in `covered_ids` → SKIP (fuzzy: same product/company + same action)
3. **Exact URL match** in `covered_urls` → SKIP
4. **Same announcement, different angle** → SKIP

**Examples of stories to SKIP:**

- Falcon-H1R 7B covered yesterday → skip even if new benchmark article
- Simon Willison blog post covered → skip even if different site quotes it
- xAI $20B funding covered → skip follow-up analysis articles
- CEO AI survey covered → skip reposts on different sites

**Stories to INCLUDE:**

- Genuinely new announcements (story_id NOT in `covered_ids`, URL NOT in `covered_urls`)
- New developments on previously covered topics (e.g., acquisition CLOSED vs announced)
- Different products from same company

**Step 4: Keep only filtered stories**

Store the filtered list. These are the ONLY stories that will appear in the digest.

**Step 5: Rank remaining stories**

Score by:

- Source credibility (tier 1: arxiv, official blogs; tier 2: tech news; tier 3: social)
- Engagement signals
- Relevance to engineering work

**Step 6: Categorize**

Assign to template sections.

**Step 7: Top 5**

Select most impactful stories from NEW filtered content only.

### Phase 17: Generate Digest

⚠️ **Only use the filtered stories from Phase 16 Step 4. Do NOT include any stories that were filtered out.**

1. Load `output-template.md`
2. Fill sections with filtered items from Phase 16
3. Format:
   - Each item: `- [ ] **[Title]** — [1-line summary] [Source: URL]`
   - **Checkbox prefix `- [ ]`** on ALL story items with source URLs (renders as clickable task in Notion)
   - **NO checkbox** on: Top 5 summary, prose bullets (Workflow Changes, Job Market, Org Transformation), Action Items, Things to Explore, Connections, Sources section
   - Include source URLs
   - Add personal takeaways section
4. If fewer than 5 stories after filtering, note "Light news day" in digest

### Phase 18: Save Digest Files (DO NOT Update .covered-stories Yet)

⚠️ **CRITICAL: Do NOT update `.covered-stories` in this phase. That happens in Phase 20 AFTER verification.**

**Step 1:** Create directories if needed

```bash
mkdir -p ./findings/ai-daily-digest
```

**Step 2: 🔴 SAVE TO NOTION WORKSPACE (REQUIRED - DO NOT SKIP)**

⚠️ **CRITICAL: This step is MANDATORY. The digest MUST be saved to Notion.**

**Step 2a: Load Notion MCP tool**

Notion tools are deferred and must be loaded first using ToolSearch:

```text
select:mcp__notion__notion-create-pages
```

**Step 2b: Read digest content**

Read the digest file just created to get the full content.

**Step 2c: Create Notion page**

Use `mcp__notion__notion-create-pages` to create page under parent "🤖 AI Digests":

- Parent page ID: `3035f40a-a0f4-81ea-8033-fc823dd8eb92`
- Title property: `🤖 AI Digest {YYYY-MM-DD}`
- Content: Full digest markdown (excluding the H1 title line, which goes in properties)

Example call:

```json
{
  "parent": {"page_id": "3035f40a-a0f4-81ea-8033-fc823dd8eb92"},
  "pages": [{
    "properties": {"title": "🤖 AI Digest 2026-02-16"},
    "content": "**Focus:** All\n**Coverage:** ...\n\n## 🔬 Technical Advances\n..."
  }]
}
```

**Verification:** Confirm Notion page created successfully (returns page URL) before continuing.

**Step 3:** Write archive copy

```text
./findings/ai-daily-digest/ai-digest-{YYYY-MM-DD}.md
```

**Step 4: Update last run date ONLY**

```text
./findings/ai-daily-digest/.last-run
```

Use Write tool to save today's date in `YYYY-MM-DD` format (e.g., `2026-01-28`).
File contains only the date string, nothing else.

⚠️ **DO NOT update `.covered-stories` yet. Wait for verification in Phase 19.**

**Verification:** Confirm files written successfully (Notion page + 1 archive file + 1 last-run file) before proceeding to Phase 19.

### Phase 19: Duplicate Verification (Spawn Agent)

⚠️ **NOTE: `.covered-stories` has NOT been updated yet with today's stories. This is intentional.**

Spawn a **separate verification agent** to check for duplicates as a sanity check.

**Agent task:**

```text
Verify AI digest for duplicate stories against recent history.

Files to read:
1. Today's digest: ./findings/ai-daily-digest/ai-digest-{YYYY-MM-DD}.md
2. Last 3 digests from ./findings/ai-daily-digest/ (by date, excluding today)
3. Covered stories: ./findings/ai-daily-digest/.covered-stories (should NOT include today's stories yet)

Check for:
1. **Exact duplicates** — Same story_id in today's digest and .covered-stories (before today)
2. **Near duplicates** — Same company/product + similar action within 7 days
3. **URL duplicates** — Same URL appeared in previous digests
4. **Topic fatigue** — Same topic (e.g., "GPT-5 rumors") covered 3+ times in past week

For each potential duplicate found:
- Story title from today's digest
- Matching story from history (date, story_id, URL)
- Duplicate type (exact/near/url/fatigue)
- Recommendation: REMOVE or KEEP (with justification)

Output format:
## Duplicate Check Results

### ❌ Duplicates Found (Remove)
- **{Story}** — matches {history_story} from {date} [{type}]

### ⚠️ Borderline (Review)
- **{Story}** — similar to {history_story} [{type}] — {why borderline}

### ✅ All Clear
{count} stories verified as unique

If duplicates found, list specific line numbers in today's digest to remove.
```

**Agent type:** `general-purpose`

**On duplicate detection:**

1. If agent finds duplicates marked REMOVE:
   - Read the duplicate report
   - Edit both digest files (Obsidian + archive) to remove flagged stories
   - Log removed stories
   - **DO NOT proceed to Phase 20 until duplicates are removed**

2. If only borderline items:
   - Keep stories but note in digest footer: `*Verification: {N} borderline items retained*`
   - Proceed to Phase 20

3. If all clear:
   - Proceed to Phase 20

## Output Requirements

- Use emojis for section headers (per Notion conventions)
- Bullet points over paragraphs
- Include wikilinks to existing workspace pages where relevant
- All items must have source URLs
- Top 5 stories section required
- Personal takeaways with actionable items
- Show coverage period in header (e.g., "Coverage: Jan 25 - Jan 28 (3 days)")

## Error Handling

- If WebSearch fails for a source, log and continue with others
- Minimum viable digest: at least 5 items total across categories
- If < 5 items found, expand date range by 1 day and retry
- Only update `.last-run` on successful digest generation

## Example Invocations

```bash
# Full digest since last run
/ai-digest

# Technical focus only
/ai-digest --focus technical

# Business news only
/ai-digest --focus business
```

### Phase 20: Update Covered Stories (FINAL STEP)

⚠️ **Only execute this phase AFTER Phase 19 verification passes (or duplicates are removed).**

**Append to covered stories:**

```text
./findings/ai-daily-digest/.covered-stories
```

For each story in today's FINAL digest (after any removals from Phase 19), append line in format:

```text
{date}|{story_id}|{url}
```

Example entries:

```text
2026-01-30|nvidia-isaac-groot-n16|https://nvidianews.nvidia.com/news/nvidia-releases-new-physical-ai-models
2026-01-30|apple-qai-acquisition|https://techstartups.com/2026/01/29/apple-acquires-israeli-ai-startup
2026-01-30|simonwillison-sprites-dev|https://simonwillison.net/2026/Jan/9/sprites-dev/
```

**Implementation:**

Use Bash with heredoc to append all stories at once.

**Cleanup:** Keep file under 300 lines — if over, trim oldest entries from top.

**Final verification:** Confirm file updated successfully. Digest generation complete.

---

## 📬 Newsletter Integration

Story items use `- [ ]` checkbox format for newsletter curation:

- **Unchecked `- [ ]`** = not selected
- **Checked `- [x]`** = selected for weekly newsletter

User checks stories in Notion → `/ai-newsletter` extracts checked items into curated weekly newsletter. See `ai-newsletter` skill for details.
