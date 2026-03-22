---
name: user-interview
description: Systematically process user interviews to extract actionable insights. Batch processes interviews and generates research reports.
disable-model-invocation: false
user-invocable: true
---

# User Interview Processing Workflow

Systematically process user interviews to extract actionable insights using Claude Code.

## Quick Start

```
/user-interview

Just finished user interviews? Drop your transcripts and I'll extract insights.

Tell me:
1. How many interviews do you have? (paste transcripts or point me to files)
2. What was the research goal? (what were you trying to learn?)
3. Any specific hypotheses you were testing?

I'll cross-reference with your existing research, extract pain points,
feature requests, JTBD insights, and generate a shareable report.

Output: outputs/research-synthesis/[date]-interview-insights.md
```

---

### Scope Boundary: This Skill vs /user-research-synthesis

**Use /user-interview when:**
- Processing 1-3 interviews from a single research session
- Extracting quotes, themes, and action items from individual conversations
- Doing a quick post-interview debrief (same day)
- Output: Per-interview insight cards with VALIDATED/CHALLENGED/NEW theme labels

**Use /user-research-synthesis when:**
- Synthesizing 4+ interviews into a unified research report
- Looking for cross-interview patterns, personas, or journey insights
- Applying advanced frameworks (Mom Test validation, Five Whys root cause, affinity mapping)
- Output: Research report with theme hierarchy, evidence strength, and strategic recommendations

**Handoff:** After processing 3+ individual interviews with /user-interview, suggest: "You now have [N] processed interviews. Want to run /user-research-synthesis to find cross-interview patterns and build a research report?"

---

## Context Routing Logic (Internal - for Claude)

**Automatic Context Checks:**
When this skill is invoked, immediately check:

| Source | What to Check | Priority |
|--------|---------------|----------|
| context-library/research/ | Previous interview syntheses, existing themes | High |
| context-library/prds/ | Active PRDs that this interview relates to | High |
| context-library/stakeholder-template.md | If interviewee is a known stakeholder/customer | Medium |
| context-library/business-info-template.md | Company context, product positioning | Medium |
| context-library/launches/ | Recent launches the interviewee might reference | Low |

**Context Priority:**
1. Existing research and validated themes FIRST
2. Active PRDs and problem statements SECOND
3. Business context and positioning THIRD
4. Recent launches and stakeholder info FOURTH

**Cross-Skill Links:**
- Before interviews → `/interview-guide` for question preparation
- After processing → `/user-research-synthesis` for deeper analysis
- If insights inform a feature → `/prd-draft` to reference findings
- If insights reveal strategic shifts → `/write-prod-strategy`

---

## Overview

**Tools needed:** Claude Code (primary), Dovetail (optional)
**When to use:** After conducting 3+ user interviews

---

## Workflow

### Step 0: Connect to Existing Research

**Before processing new interviews, check existing context:**

1. Search `context-library/research/` for previous interview syntheses and findings
2. Identify validated themes from prior research
3. Note which PRDs or strategic initiatives these interviews relate to
4. Check `context-library/business-info-template.md` for product positioning context

**For each theme that emerges in the new interviews:**
- If it matches a previous finding: "This **validates** theme X from [previous research file]. Now supported by [N total] interviews."
- If it contradicts a previous finding: "This **challenges** theme X from [previous research file]. Previous research said [Y], but this interview suggests [Z]. Needs further investigation."
- If it's entirely new: "This is a **NEW theme** not seen in prior research. First surfaced in this batch. Recommend probing in future interviews."

**Show the PM a brief summary:**
```
## Existing Research Context
- Found [N] previous interview syntheses in context-library/research/
- Validated themes from prior research: [list]
- Active PRDs this research relates to: [list]
- New themes to watch for: [will identify during analysis]
```

---

### Step 1: Transcribe

**Option A: Otter.ai** (Recommended)
- Upload recordings
- Auto-transcribe
- Download as text files

**Option B: Your recording tool**
- Zoom, Meet, Teams all auto-transcribe
- Download transcripts
- Clean up formatting

**Option C: Claude**
- Upload audio files directly
- Ask for transcription
- Save outputs

### Step 2: Load Transcripts into Claude Code

1. Place all transcript files in a folder
2. Start Claude Code in that directory
3. Tell Claude: "I have [X] interview transcripts to analyze. Please read all the files in this folder."

### Step 3: Extract Insights

**Run these queries in order:**

```
Query 1: Pain Points
"Analyze all transcripts. What are the top 5 pain points customers mentioned?
For each:
- How many customers mentioned it
- Specific quotes
- Severity (how painful)
- Current workarounds"

Query 2: Feature Requests
"What features did customers request?
For each:
- Frequency
- User quotes
- Underlying need
- Priority (must-have vs nice-to-have)"

Query 3: Jobs to Be Done
"For each major use case, what job is the customer trying to accomplish?
Include:
- The task/goal
- Why it matters to them
- What triggers the need
- What success looks like"

Query 4: User Segments
"Do different user types express different needs?
Identify:
- 2-3 distinct user archetypes
- Unique needs per archetype
- Common needs across all"

Query 5: Surprises
"What was surprising or unexpected in these interviews?
What assumptions were challenged?"
```

### Step 4: Create Output Doc

Ask Claude:
```
"Create an executive summary covering:
- Top 3 insights
- Top 5 pain points (ranked)
- Top 3 feature requests
- Recommended next steps
Format as a report I can share with my team.
Save to outputs/research-synthesis/[date]-interview-insights.md"
```

---

## Deep Dive

For more thorough analysis, add these steps:

### Step 5: Sentiment Analysis

```
"Analyze sentiment across all transcripts:

For each user:
- Overall sentiment (positive/neutral/negative)
- What they love
- What they're frustrated by
- Quote that captures their feeling

Then: Overall sentiment trends across all users"
```

### Step 6: Opportunity Scoring

```
"Based on these interviews, score each opportunity:
[paste pain points and feature requests from Step 3]

For each opportunity, rate 1-5:
- Pain level (how much it hurts)
- Frequency (how often encountered)
- Reach (how many users affected)
- Strategic value

Recommend top 3 to pursue."
```

### Step 7: Create Quote Bank

```
"Extract 15-20 powerful quotes from these interviews that:
- Illustrate key pain points
- Show user mental models
- Express emotional impact
- Could be used in PRDs or presentations

For each quote:
- The quote
- User context (role, company size, use case)
- What it illustrates"
```

Save these quotes for later use in PRDs, presentations, and marketing.

### Step 8: Competitive Mentions

```
"What did users say about competitors?
- Which competitors were mentioned
- What users like about them
- What users don't like
- Why they chose us (or didn't)

Identify: What can we learn?"
```

### Step 9: Workflow Analysis

```
"For each key workflow discussed:
- Step-by-step how users complete it today
- Where they get stuck
- What tools they use
- What they wish was different

Visualize: Current state → Desired future state"
```

---

## Using Dovetail (If You Have It)

Dovetail is purpose-built for research synthesis:

**Setup:**
1. Create new project
2. Import transcripts
3. Auto-generate insights
4. Tag key themes
5. Create highlight reels

**Benefits:**
- Team collaboration
- Video snippets
- Ongoing tagging system
- Integration with other tools

**Cost:** $300-500/month (worth it if you do research continuously)

---

## Automation Options

### Automated Transcription & Analysis

**Using Make.com or Zapier:**

1. **Trigger:** Recording uploaded to Drive/Dropbox
2. **Action:** Send to transcription service
3. **Action:** Send transcript to Claude for analysis
4. **Action:** Post summary to Slack
5. **Action:** Save to Notion/Confluence

**Result:** Automatic insights within an hour of interview completion.

### Scheduled Batch Processing

**Using Relay or n8n:**

1. **Schedule:** Every Friday at 5pm
2. **Action:** Find all transcripts from the week
3. **Action:** Synthesize with Claude
4. **Action:** Generate report
5. **Action:** Email to team

**Result:** Weekly research summary without manual effort.

---

## Output Templates

### Executive Summary Template

```markdown
# Customer Interview Insights - [Date]

## Executive Summary
[3-4 bullets: biggest insights]

## Interviews Conducted
- Number of interviews: [X]
- Date range: [Start] to [End]
- User segments: [List]

## Top Pain Points
1. **[Pain Point]** - [X] users mentioned
   - Quote: "[User quote]"
   - Impact: [Description]
   - Current workaround: [How they cope]

2. [Repeat for top 5]

## Top Feature Requests
1. **[Feature]** - Priority: [High/Medium/Low]
   - Requested by: [X] users
   - Quote: "[User quote]"
   - Underlying need: [Why they want this]

## User Archetypes
**Archetype 1: [Name]**
- Characteristics: [Description]
- Main use case: [What they do]
- Unique needs: [What they need]

## Key Insights
1. [Insight 1]
2. [Insight 2]
3. [Insight 3]

## Recommended Actions
1. [Action 1] - Owner: [Name] - Due: [Date]
2. [Action 2] - Owner: [Name] - Due: [Date]
3. [Action 3] - Owner: [Name] - Due: [Date]

## Appendix
- Full transcript links
- Complete quote bank
- Detailed user flows
```

---

## Best Practices

### Before Interviews

**Prepare:**
- Define research goals
- Create interview guide (use `/interview-guide`)
- Get recording consent
- Test recording setup

**During Interviews:**
- Record everything (with permission)
- Take lightweight notes
- Ask follow-up questions
- Capture emotions, not just facts

### After Interviews

**Process quickly:**
- Within 24-48 hours (while fresh)
- Don't let transcripts pile up
- One batch per week maximum

**Share insights:**
- Post summary to team Slack
- Add to product wiki
- Reference in next PRD
- Close the loop with customers

### Continuous Research

**Build a repository:**
- All past interviews in `context-library/research/`
- Searchable by theme/topic
- Updated quote bank
- Trend tracking over time

**Regular synthesis:**
- Monthly: Review new interviews
- Quarterly: Analyze trends
- Annually: Update personas/archetypes

---

## Common Mistakes

**Don't:**
- ❌ Process interviews individually (do batch processing)
- ❌ Focus only on positive feedback (dig into problems)
- ❌ Let AI interpretation replace your judgment
- ❌ Forget to thank and follow up with users
- ❌ Let insights sit in a doc (turn into action)

**Do:**
- ✅ Process 5-10 interviews at once (pattern detection)
- ✅ Triangulate AI findings with your observations
- ✅ Create action items from insights
- ✅ Share findings broadly across team
- ✅ Reference in future product decisions

---

## Measuring Success

**Quality metrics:**
- Insights extracted per interview: 8-12
- Actionable findings: 3-5 per batch
- Insights referenced in PRDs: 80%+

**Business impact:**
- Features validated before build: 90%+
- Customer satisfaction with built features: 75%+
- Product decisions backed by research: 60%+

---

## Advanced: Continuous Research System

### Setup Repository

**Using Notion or Confluence:**
1. Create "Customer Research" database
2. Fields: Date, User name, Segment, Pain points, Quotes, Insights
3. Upload all past transcripts
4. Tag by theme

### Build Search System

**Using Claude Code:**
- Keep all transcripts in `context-library/research/interviews/`
- Query anytime: "Search all interviews for mentions of [topic]"
- Get instant insights from entire history

### Automate Monitoring

**Using MCP + Claude:**
```
"Monitor our customer research repository.
When 3+ users mention same pain point:
- Alert me
- Provide summary
- Suggest potential solutions"
```

---

## Tool Recommendations by Budget

**Free:**
- Claude.ai (analysis)
- Otter.ai free tier (transcription)
→ Total cost: $0

**$50-100/month:**
- Claude Pro ($20/month)
- Otter.ai Pro ($17/month)
- Make.com ($9/month)
→ Total cost: $46/month

**$300-500/month:**
- Dovetail ($300+)
- Grain ($29/month)
- Claude Pro ($20/month)
→ Total cost: $349/month

**Start free. Upgrade when you're doing 10+ interviews/month.**

---

## Output Quality Self-Check

Before delivering the final research synthesis, verify:

| Check | Criteria | Pass? |
|-------|----------|-------|
| **Existing research referenced** | Cross-referenced with `context-library/research/` findings | [ ] |
| **Themes labeled correctly** | Each theme marked as VALIDATED, CHALLENGED, or NEW vs. prior research | [ ] |
| **Quotes are real** | Every quote is directly from a transcript (not paraphrased or invented) | [ ] |
| **Pain points quantified** | Each pain point shows how many users mentioned it + severity | [ ] |
| **Actionable recommendations** | At least 3 specific next steps with owners and timelines | [ ] |
| **PRD linkage** | Insights connected to relevant active PRDs in `context-library/prds/` | [ ] |
| **Segments identified** | At least 2 distinct user archetypes with unique needs called out | [ ] |
| **Surprises captured** | At least 1 unexpected finding or challenged assumption noted | [ ] |
| **Scope boundary stated** | User knows when to use this skill vs /user-research-synthesis | [ ] |
| **Output file saved** | Report saved to `outputs/research-synthesis/[date]-interview-insights.md` | [ ] |

**If any check fails, address it before delivering the output.**

---

## Next Steps

1. Do 3-5 user interviews this week
2. Process with Claude Code
3. Extract top 3 insights
4. Reference in your next PRD
5. Build this into regular cadence

**Goal:** User insights inform every product decision.
