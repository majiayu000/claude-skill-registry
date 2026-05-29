---
name: cv-knowledge-query
description: Query the CV knowledge base to find achievements, stories, and metrics by theme, skill, company, or keyword. Use when user asks about experience, wants to find specific accomplishments, or needs data for content generation.
---

# CV Knowledge Query

<purpose>
Rapid retrieval from the knowledge base to answer questions about experience, find achievements, or gather data for content generation.
</purpose>

<when_to_activate>
Activate when the user:
- Asks "What have I done with [technology/skill]?"
- Wants to find achievements for a specific theme
- Needs metrics for a particular company/period
- Asks "Show me my [type] experience"
- Wants to understand relationships between experiences

**Trigger phrases:** "find", "search", "what's my experience", "show me", "list achievements"
</when_to_activate>

## Knowledge Base Schema

### Entities (content/knowledge/index.yaml)

```yaml
entities:
  companies:
    - id: string       # anchorage, microsoft, etc.
      name: string
      period: string
      role: string
      domain: string

  themes:
    - id: string       # institutional-crypto, developer-experience
      label: string
      keywords: [string]

  skills:
    - id: string       # ethereum, api-design
      label: string
      category: string
```

### Relationships

```yaml
relationships:
  - from: achievement:id
    to: company:id | skill:id | theme:id
    type: achieved_at | demonstrates | belongs_to | contains | generated_from
```

### Achievements (content/knowledge/achievements/*.yaml)

```yaml
id: string
headline: string
metric:
  value: string
  unit: string
  context: string
situation: string
task: string
action: string
result: string
skills: [string]
themes: [string]
companies: [string]
years: [number]
good_for: [string]
```

## Quick Search (Deterministic Script)

For keyword-based searches, **USE THE SCRIPT FIRST** — it's faster and consistent:

```bash
# Search by keywords
npm run search:evidence -- --terms "crypto,staking,institutional"

# With JSON output for processing
npm run search:evidence -- --terms "crypto,staking" --json
```

The script returns:
- Matching achievements and stories sorted by relevance
- Relevance scores (strong ≥70%, moderate 40-70%, weak <40%)
- Matched terms, skills, and themes
- Snippets for quick review

**Use the script when:**
- User asks about specific keywords
- Quick search without deep analysis needed
- Need alignment scoring for job fit

**Use manual querying when:**
- Deep relationship traversal needed
- Need full STAR narrative (situation, task, action, result)
- Complex cross-referencing across entities

---

## Query Patterns

### Query by Theme
**User**: "What's my institutional crypto experience?"

**Script-first approach:**
```bash
npm run search:evidence -- --terms "institutional,crypto,custody"
```

**For deep dive:**
1. Find theme `institutional-crypto` in index
2. Query relationships where `to: theme:institutional-crypto`
3. Load matching achievements
4. Return summary with metrics

**Output Format**:
```
## Institutional Crypto Experience

### Achievements:
1. **ETH Staking Zero Slashing** (Anchorage, 2024-25)
   - Zero slashing events, Galaxy + institutional clients
   - Skills: ethereum, staking, compliance

2. **L2 Protocol Integrations** (Anchorage, 2024-25)
   - 7+ protocols shipped, 40% faster integration
   - Skills: l2s, compliance
```

### Query by Skill
**User**: "Show me my API design work"

**Process**:
1. Find skill `api-design` in index
2. Query achievements where `skills` includes `api-design`
3. Return with context and metrics

### Query by Company
**User**: "What did I accomplish at Microsoft?"

**Process**:
1. Find company `microsoft` in index
2. Query achievements where `companies` includes `microsoft`
3. Include period and role context

### Query by Keyword
**User**: "Find achievements related to revenue growth"

**Script-first approach:**
```bash
npm run search:evidence -- --terms "revenue,growth,ARR"
```

**For manual search:**
1. Search theme keywords for "revenue"
2. Search achievement headlines/results for "revenue"
3. Return ranked by relevance

### Query for Role Fit
**User**: "What achievements fit a Platform PM role?"

**Script-first approach:**
```bash
npm run search:evidence -- --terms "platform,infrastructure,api,scale"
```

**For deeper analysis:**
1. Parse role keywords: platform, infrastructure, scale
2. Match themes: infrastructure, developer-experience
3. Match `good_for` arrays in achievements
4. Return ranked list with reasoning

## Response Formats

### Summary Format (default)
```
Found 3 achievements matching "[query]":

1. **[Headline]** ([Company], [Year])
   Metric: [value] [unit]
   Themes: [theme1], [theme2]

2. ...
```

### Detail Format (on request)
```
## [Achievement Headline]

**Context**: [Company] | [Period] | [Role]
**Impact**: [metric.value] [metric.unit]

### Situation
[situation text]

### Task
[task text]

### Action
[action text]

### Result
[result text]

**Best for**: [good_for items]
```

### Metrics Format (for comparisons)
```
| Achievement | Metric | Value | Company | Year |
|------------|--------|-------|---------|------|
| [headline] | [unit] | [value] | [company] | [year] |
```

## Cross-Reference Queries

### Find Related Achievements
**User**: "What else relates to the ETH staking work?"

**Process**:
1. Load `eth-staking-zero-slashing` achievement
2. Find shared themes: `institutional-crypto`, `infrastructure`
3. Find shared skills: `ethereum`, `compliance`
4. Query other achievements with overlap
5. Rank by relationship strength

### Find Gaps
**User**: "What skills don't have strong achievements?"

**Process**:
1. List all skills in index
2. Count achievements per skill
3. Flag skills with <2 achievements
4. Suggest areas for content development

## Query Shortcuts

| User Says | Query |
|-----------|-------|
| "my blockchain work" | themes: [enterprise-blockchain, institutional-crypto] |
| "growth stories" | themes: [revenue-growth] |
| "developer tools" | themes: [developer-experience] |
| "recent work" | years: [2024, 2025] |
| "Microsoft days" | companies: [microsoft] |
| "startup experience" | companies: [ankr, forte, dapper] |

<file_locations>
## File Locations

| Query Target | File Path |
|--------------|-----------|
| Entity definitions | `content/knowledge/index.yaml` |
| Achievements | `content/knowledge/achievements/*.yaml` |
| Stories | `content/knowledge/stories/*.yaml` |
| Metrics | `content/knowledge/metrics/*.yaml` |
</file_locations>

<skill_compositions>
## Works Well With

- **generate-variant** — Query evidence before generating variants
- **cv-content-generator** — Find achievements for case studies
- **generate-story-bank** — Search for stories by category
</skill_compositions>
