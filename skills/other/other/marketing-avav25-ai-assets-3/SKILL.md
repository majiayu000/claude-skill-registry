---
name: marketing
description: Marketing workflow — initialize marketing strategy with MARKETING.md, define channels and tactics, execute recurring marketing operations (social media, blog posts, email campaigns, trend research, analytics). Orchestrates marketing-strategist, product-manager, content-designer, content-writer, and seo-engineer roles. Owns marketing/ directory.
context: fork
---

# Marketing

End-to-end marketing workflow with two phases: **Init** (one-time strategy setup) and **Execute** (recurring marketing operations). Owns the `marketing/` directory for all materials.

**⚠️ CONSTRAINT: This workflow NEVER modifies source code (*.java, *.ts, *.tsx, *.py, *.go), configs (*.yaml, *.yml, *.json), infrastructure (*.tf, Dockerfile, Helm), or dependency files (pom.xml, package.json, requirements.txt). Marketing workflow creates and edits only markdown files in the `marketing/` directory.**

## Phase Selection

Ask the user:

- **`init`** — First-time setup: gather context, define strategy, create MARKETING.md
- **`execute`** — Run a specific marketing operation (social post, blog, email, trend research, etc.)

If `marketing/MARKETING.md` does not exist → start with `init` regardless.

---

## Phase 1: Init

### 1. Gather Project Context

**Apply `Agent(product-manager)` + `Agent(marketing-strategist)`.**

1. **Read project files**:
   - `CLAUDE.md` — tech stack, project purpose
   - `README.md` — product description
   - `FEATURES.md` (if exists) — feature inventory
   - Website/landing page (if URL known) — current positioning
2. **Read existing marketing materials** (if any):
   - `marketing/` directory contents
   - Blog posts directory
   - Any existing brand guidelines
3. **Summarize findings**: product type, target market signals, existing messaging, content gaps.

### 2. User Interview

Present the **Marketing Setup Questionnaire** from `marketing-operations` skill (`marketing-setup-template.md`). Gather:

<questionnaire>
**Product and Market**:
- Product name and one-line description
- Target audience (who buys/uses this?)
- Key problem you solve
- Top 3 competitors or alternatives (including "do nothing")
- Current stage (pre-launch / launched / growing / mature)

**Goals and Metrics**:
- Primary marketing goal (awareness / leads / signups / revenue)
- Target metrics (e.g., X signups/month, Y website visitors)
- Budget constraints (free/organic only, small budget, significant budget)
- Timeline (when do you need results?)

**Channels and Tools**:
- Active social accounts (X/Twitter, LinkedIn, Reddit, Product Hunt, etc.)
- Email list (exists? size? tool used?)
- Blog (exists? platform? publishing frequency?)
- Paid advertising (any? which platforms?)
- Analytics tools (GA4, Mixpanel, etc.)
- Community presence (Discord, Slack, forums?)

**Brand and Voice**:
- Brand personality (3-5 adjectives)
- Tone examples (link to existing content that represents your voice)
- Topics to avoid
- Compliance requirements (regulated industry? legal review needed?)

**Resources**:
- Who creates content? (founder only / small team / agency)
- Available time per week for marketing activities
- Design resources (can create visuals? tools available?)
</questionnaire>

Record all answers. Ask clarifying questions if answers are vague.

### 3. Define Strategy

**Apply `Agent(marketing-strategist)`.**

Based on project context + user answers, produce:

1. **ICP and Positioning** — ideal customer profile, JTBD, competitive positioning (April Dunford framework)
2. **Messaging Framework** — core value proposition, 3-5 pillars, proof points, boilerplates (short/medium/long)
3. **Channel Strategy** — which channels to focus on, why, expected effort vs impact
4. **Content Pillars** — 3-5 topic areas aligned with ICP pain points and product strengths
5. **Tactical Plan** — specific recurring tasks with frequency, matched to available resources

### 4. Create MARKETING.md

Create `marketing/MARKETING.md` using the template from `marketing-operations` skill (`marketing-setup-template.md`).

This file is the **single source of truth** for marketing strategy. Sections:

- Product summary and positioning
- ICP and personas
- Messaging framework (value prop, pillars, boilerplates)
- Channel strategy with prioritization
- Content pillars and calendar
- Tactical plan (daily/weekly/monthly tasks)
- KPIs and measurement plan
- Brand voice guidelines
- Tools and accounts

### 5. Create Content Calendar

Create `marketing/content-calendar.md` with the recurring task schedule. Recommended defaults (adjust based on user resources):

| Frequency | Task | Channel | Role |
|---|---|---|---|
| Daily | Social media post | X/Twitter, LinkedIn | `Agent(content-designer)` |
| Daily | Community engagement | X/Twitter, Reddit, forums | `Agent(marketing-strategist)` |
| 2-3x/week | Blog post | Blog | `/blog-post` |
| Weekly | Trend research | X/Twitter, HN, Reddit, Google Trends | `Agent(marketing-strategist)` |
| Weekly | Analytics review | GA4, social analytics | `Agent(marketing-strategist)` |
| Bi-weekly | Email newsletter | Email list | `Agent(content-writer)` |
| Monthly | Strategy review and adjustment | — | `Agent(marketing-strategist)` + `Agent(product-manager)` |

### 6. Present and Approve

Present the complete strategy to the user:

- MARKETING.md summary
- Content calendar
- Recommended first 3 actions to start immediately

**Wait for user approval.** Adjust based on feedback.

---

## Phase 2: Execute

### 1. Select Operation

Ask the user which marketing operation to perform:

| Operation | Description | Typical Frequency |
|---|---|---|
| **social-post** | Draft social media post(s) for one or more platforms | Daily |
| **blog-post** | Write a blog post (delegates to `/blog-post`) | 2-3x/week |
| **email** | Draft email campaign or newsletter | Bi-weekly |
| **trend-research** | Research trends and content opportunities | Weekly |
| **analytics** | Review marketing metrics and adjust tactics | Weekly |
| **content-repurpose** | Adapt existing content for other channels | As needed |
| **community** | Plan community engagement responses | Daily |
| **strategy-review** | Monthly strategy review and adjustment | Monthly |

### 2. Load Context

1. **Read `marketing/MARKETING.md`** — strategy, ICP, messaging, voice
2. **Read `marketing/content-calendar.md`** — planned tasks, completed items
3. **Scan recent materials** in `marketing/` — maintain consistency

### 3. Execute Operation

#### social-post

**Apply `Agent(content-designer)` + `Agent(marketing-strategist)`.**

1. **Determine topic**: Content calendar, trending topic, product update, or user request
2. **Research** (if trend-based): Search X/Twitter, HN, Reddit for current conversations
3. **Draft post** per platform. See `marketing-operations` skill `channel-playbooks.md` for format rules:
   - **X/Twitter**: ≤280 chars, hook first line, 1-3 hashtags, thread if longer
   - **LinkedIn**: Professional tone, 1-3 paragraphs, personal angle, 3-5 hashtags
   - **Reddit**: Community tone, value-first, no self-promotion, context-aware
4. **Humanize** — apply `@humanizer` skill to remove AI writing patterns from the draft
5. **Visual direction**: Suggest image/graphic if appropriate
6. **Save to `marketing/posts/YYYY-MM-DD-[platform]-[topic].md`**
7. Present draft. **Wait for user approval.**

#### blog-post

Delegate to `/blog-post` workflow. Pass context from `marketing/MARKETING.md` (ICP, content pillars, voice).

#### email

**Apply `Agent(content-writer)` + `Agent(marketing-strategist)`.**

1. **Define campaign**: Newsletter / product update / nurture sequence / announcement
2. **Draft**: Subject line (3 variants), preview text, body, CTA
3. **Humanize** — apply `@humanizer` skill to remove AI writing patterns
4. **Segmentation**: Target audience segment
5. **Save to `marketing/emails/YYYY-MM-DD-[campaign-name].md`**
6. Present draft. **Wait for user approval.**

#### trend-research

**Apply `Agent(marketing-strategist)`.**

1. **Scan sources**: X/Twitter (niche hashtags, competitor accounts), Hacker News (trending), Reddit (subreddits), Google Trends, industry newsletters
2. **Identify opportunities**: Content ideas, conversations to join, emerging topics
3. **Save to `marketing/research/YYYY-MM-DD-trends.md`**
4. **Update content calendar** with new content ideas

#### analytics

**Apply `Agent(marketing-strategist)`.**

1. **Review metrics** against KPIs in MARKETING.md
2. **Analyze**: What's working? What's not? Why?
3. **Recommend adjustments**: Channel mix, content topics, posting schedule
4. **Save to `marketing/reports/YYYY-MM-DD-analytics.md`**
5. **Update MARKETING.md** if strategy adjustments needed

#### content-repurpose

**Apply `Agent(content-designer)`.**

1. **Select source**: Blog post, feature release, case study, documentation
2. **Adapt**: Blog → X thread, LinkedIn post, email snippet, social graphics, short video script
3. **Save variants to `marketing/posts/`**

#### community

**Apply `Agent(marketing-strategist)`.**

1. **Identify targets**: Relevant threads, questions, discussions on X/Twitter, Reddit, HN, forums
2. **Draft responses**: Helpful, value-first, non-promotional
3. **Save to `marketing/community/YYYY-MM-DD-engagement.md`**

#### strategy-review

**Apply `Agent(marketing-strategist)` + `Agent(product-manager)`.**

1. **Review MARKETING.md** against actual results
2. **Assess**: Goal progress, channel effectiveness, content performance, ROI
3. **Adjust**: Strategy, content pillars, channel priorities, tactics, resource allocation
4. **Update** `marketing/MARKETING.md` and `marketing/content-calendar.md`

### 4. Update Tracking

After every operation:

1. Update `marketing/content-calendar.md` — mark completed, add new items
2. If strategy implications → update `marketing/MARKETING.md`

### 5. Summary

```
## Marketing Operation Summary

- **Operation**: [social-post / blog-post / email / trend-research / analytics / etc.]
- **Roles applied**: [list]
- **Materials created**:
  - [file path]: [description]
- **Status**: [draft ready / published / scheduled]
- **Next scheduled task**: [from content calendar]
- **Follow-ups**: [if any]
```

## Directory Structure

```
marketing/
├── MARKETING.md              # Strategy document (single source of truth)
├── content-calendar.md       # Recurring task schedule and tracking
├── posts/                    # Social media posts
│   └── YYYY-MM-DD-[platform]-[topic].md
├── emails/                   # Email campaigns
│   └── YYYY-MM-DD-[campaign-name].md
├── research/                 # Trend research and analysis
│   └── YYYY-MM-DD-trends.md
├── reports/                  # Analytics reports
│   └── YYYY-MM-DD-analytics.md
└── community/                # Community engagement plans
    └── YYYY-MM-DD-engagement.md
```

## Integration

- **Roles**: `Agent(marketing-strategist)` (strategy, analysis), `Agent(product-manager)` (product context, ICP), `Agent(content-designer)` (social posts, copy), `Agent(content-writer)` (blog, email), `Agent(seo-engineer)` (SEO optimization)
- **Skills**: `marketing-operations` skill (setup template, channel playbooks), `content-creation` skill (AI content tools), `@humanizer` (AI writing pattern removal)
- **Rules**: `humanize-content` (auto-enforces humanizer pass on all content)
- **Sub-workflows**: `/blog-post` (blog content), `/seo-review` (SEO audit), `/docs` (documentation)
- **Follow-up**: `/pre-commit`, `/create-pr`
