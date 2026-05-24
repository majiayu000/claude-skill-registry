---
name: github-hunter
description: Automatically discover, score, and archive relevant GitHub repositories for BidDeed.AI and Life OS projects. Use this skill when the user requests to find GitHub repositories for specific topics, technologies, or domains that could be integrated into existing projects. Triggers include phrases like "find GitHub repos for", "discover repositories about", "search GitHub for projects related to", or when analyzing videos/articles that mention GitHub projects.
---

# GitHub Hunter Skill

Automatically discovers GitHub repositories relevant to BidDeed.AI and Life OS, scores them 0-100 based on criteria, and archives them to Supabase with integration recommendations.

## Workflow

### 1. Discovery Phase
Search GitHub for repositories using relevant keywords extracted from:
- User requests ("find repos for X")
- Video transcripts (projects mentioned in content)
- Technology domains (foreclosure data, ADHD productivity, etc.)

### 2. Scoring Phase (0-100)
Score each repository on:
- **Stars** (0-25 points): Logarithmic scale, 10K+ stars = 25
- **Recency** (0-20 points): Last updated within 30 days = 20, 1+ year = 0
- **Documentation** (0-15 points): README quality, examples, API docs
- **Relevance** (0-25 points): Direct applicability to BidDeed.AI or Life OS
- **License** (0-15 points): MIT/Apache = 15, GPL = 10, Proprietary = 0

Formula:
```python
score = min(100, 
    (log10(stars + 1) / log10(10000)) * 25 +
    max(0, 20 - (days_since_update / 15)) +
    documentation_score +
    relevance_score +
    license_score
)
```

### 3. Archive Phase
Insert to Supabase `insights` table with:
```json
{
  "category": "github_discovery",
  "subcategory": "auto_hunter",
  "title": "GitHub Hunter: {repo_name}",
  "content": {
    "repo_url": "https://github.com/{owner}/{name}",
    "score": 85,
    "stars": 1234,
    "description": "...",
    "language": "Python",
    "license": "MIT",
    "last_updated": "2025-12-20",
    "integration_recommendation": "...",
    "relevant_to": ["biddeed", "life-os"]
  }
}
```

### 4. Alert Phase
Notify Ariel via response with:
- Repository name and URL
- Score (with color coding: 🟢 80+, 🟡 60-79, 🟠 40-59, 🔴 <40)
- Brief summary (1-2 sentences)
- Integration recommendation
- Direct action: "Add to {repo}?" with yes/no

## Usage Triggers

**Explicit requests:**
- "Find GitHub repos for {topic}"
- "Search for projects about {domain}"
- "Discover repositories related to {technology}"

**Context-aware triggers:**
- Video transcripts mentioning GitHub projects → auto-hunt after transcript
- Articles/docs with GitHub URLs → extract and score
- User says "what could we integrate from that?" after discussing a topic

## Scoring Examples

**Score 95:** `fastapi/fastapi`
- 75K stars (25), updated 2 days ago (20), excellent docs (15), highly relevant to BidDeed.AI API (25), Apache license (15)

**Score 72:** `user/small-foreclosure-tool`
- 45 stars (8), updated 1 week ago (18), basic README (8), perfect relevance (25), MIT (15)

**Score 38:** `abandoned/old-project`
- 500 stars (15), updated 2 years ago (0), no docs (0), tangential relevance (8), MIT (15)

## Integration Recommendations Format

Provide actionable integration steps:

```markdown
### Integration Recommendation

**To BidDeed.AI:**
1. Use {feature} for {existing_workflow_stage}
2. Replace {current_approach} with {repo_approach}
3. Add workflow: `.github/workflows/{new_workflow}.yml`

**To Life OS:**
1. Integrate {tool} for {productivity_feature}
2. Add skill: `.claude/skills/{skill_name}/`
3. Update orchestrator to call {function}

**Estimated effort:** {hours} hours
**Dependencies:** {list}
**Risk level:** {low/medium/high}
```

## Alert Template

```
🔍 **GitHub Hunter Discovery**

**{repo_name}** [{score_emoji} {score}/100]
https://github.com/{owner}/{name}

{description}

**Stats:** ⭐ {stars} | 📅 {last_updated} | 📜 {license} | 💬 {language}

**Integration:**
{integration_recommendation}

**Add to BidDeed.AI?** [Yes/No]
**Add to Life OS?** [Yes/No]
```

## Advanced: Batch Discovery

When user provides a list of topics or a domain:

```bash
# Example: "Find repos for foreclosure data scraping, PDF parsing, and workflow orchestration"

Topics:
1. foreclosure data scraping
2. PDF parsing  
3. workflow orchestration

For each topic:
- Search GitHub API with 3-5 keyword variations
- Score top 10 results per topic
- Archive scores 60+ to Supabase
- Alert Ariel with top 3 across all topics
```

## Repository Addition Workflow

When user approves a repo:

1. **Determine target repo:**
   - BidDeed.AI → `breverdbidder/biddeed-conversational-ai`
   - Life OS → `breverdbidder/life-os`
   - Both → add to both

2. **Create integration plan:**
   - If library: Add to requirements.txt or package.json
   - If workflow: Create `.github/workflows/{name}.yml`
   - If skill: Create `.claude/skills/{name}/SKILL.md`
   - If script: Add to `src/integrations/` or `agents/`

3. **Document in README:**
   - Add to "Integrations" section
   - Link to repo
   - Note version and license

4. **Archive decision:**
   - Update Supabase insight with `integration_status: "added"`
   - Record which repo(s) it was added to
   - Note commit SHA

## Filters

**Exclude repos with:**
- Archived status
- No commits in 2+ years (unless legendary/foundational)
- Proprietary license for core BidDeed.AI features
- <10 stars AND <30 days old (likely spam)

**Prioritize repos with:**
- Python (BidDeed.AI), JavaScript/TypeScript (Life OS)
- AI/ML, web scraping, document processing, workflow automation
- Active maintenance (commits in last 60 days)
- Clear documentation
- Permissive licenses (MIT, Apache, BSD)

## GitHub API Usage

Use web_search to find repos, then web_fetch for details:

```python
# Search
query = "foreclosure auction data scraping language:python"
search_url = f"https://github.com/search?q={query}&type=repositories&s=stars&o=desc"

# Fetch repo details
repo_url = "https://api.github.com/repos/{owner}/{name}"
# Get: stars, last_updated, description, language, license, topics
```

## Supabase Schema

Insert to `insights` table at `mocerqjnksmhcjzxrewo.supabase.co`:

```sql
INSERT INTO insights (category, subcategory, title, content, created_at)
VALUES (
  'github_discovery',
  'auto_hunter',
  'GitHub Hunter: {repo_name}',
  '{
    "repo_url": "...",
    "score": 85,
    "stars": 1234,
    "description": "...",
    "language": "Python",
    "license": "MIT",
    "last_updated": "2025-12-20",
    "integration_recommendation": "...",
    "relevant_to": ["biddeed"],
    "integration_status": "pending"
  }'::jsonb,
  NOW()
);
```

## Example Session

```
User: "Find GitHub repos for PDF form filling and data extraction"

Claude: [triggers github-hunter skill]

1. Search: "PDF form filling python", "PDF data extraction", "fillable pdf automation"
2. Discover: 
   - PyPDF2 (8.2K stars, score: 78)
   - pdfplumber (6.1K stars, score: 82)
   - pdf-form-fill (234 stars, score: 71)
3. Archive top 2 to Supabase
4. Alert:

🔍 **GitHub Hunter Discovery**

**pdfplumber** [🟢 82/100]
https://github.com/jsvine/pdfplumber

Plumb a PDF for detailed information about tables, text, images. Maintained, excellent docs.

**Stats:** ⭐ 6.1K | 📅 2025-12-15 | 📜 MIT | 💬 Python

**Integration:**
Replace manual PDF parsing in BECA scraper with pdfplumber for structured table extraction.
Use for tax certificate downloads from RealTDM.

**Add to BidDeed.AI?** [Yes/No]
```

## Notes

- Always archive to Supabase BEFORE asking for approval
- Score threshold for alerts: 60+
- Batch discovery: alert top 3 only, archive all 60+
- If repo already in our codebase, mark as `integration_status: "existing"`
