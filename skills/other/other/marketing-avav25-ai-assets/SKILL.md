---
name: marketing
description: Run marketing operations for the product by defining messaging, selecting channels, producing content tasks, humanizing all output, and reviewing performance signals.
---

# Marketing

End-to-end marketing workflow with two phases: **Init** (strategy setup) and **Execute** (recurring operations). Owns the `marketing/` directory.

This workflow creates and edits only markdown files in the `marketing/` directory.

## Phase Selection

- **`init`** — first-time setup: gather context, define strategy, create MARKETING.md
- **`execute`** — run a specific marketing operation

If `marketing/MARKETING.md` does not exist, start with `init`.

---

## Phase 1: Init

### 1. Gather Project Context

Read:

1. `AGENTS.md` — tech stack, project purpose
2. `README.md` — product description
3. `FEATURES.md` (if exists) — feature inventory
4. `marketing/` directory — existing materials
5. Blog posts directory — existing content

### 2. User Interview

Gather:

- Product name, one-line description, target audience
- Key problem solved, top 3 competitors
- Primary marketing goal (awareness / leads / signups / revenue)
- Active channels (X/Twitter, LinkedIn, Reddit, email, blog)
- Brand personality (3-5 adjectives) and topics to avoid
- Available resources and time per week

### 3. Define Strategy

Produce:

1. ICP and positioning (April Dunford framework)
2. Messaging framework — value proposition, 3-5 pillars, boilerplates
3. Channel strategy — focus channels, effort vs impact
4. Content pillars — 3-5 topic areas aligned with ICP pain points
5. Tactical plan — recurring tasks with frequency

### 4. Create MARKETING.md

Create `marketing/MARKETING.md` as single source of truth. Use template from `marketing-operations` skill.

### 5. Create Content Calendar

Create `marketing/content-calendar.md` with recurring task schedule.

### 6. Present and Approve

Present strategy summary, content calendar, and recommended first 3 actions.
Wait for user approval.

---

## Phase 2: Execute

### 1. Select Operation

| Operation | Description |
|---|---|
| **social-post** | Draft social media post(s) for one or more platforms |
| **blog-post** | Write a blog post (delegates to `blog-post` skill) |
| **email** | Draft email campaign or newsletter |
| **trend-research** | Research trends and content opportunities |
| **analytics** | Review marketing metrics and adjust tactics |
| **content-repurpose** | Adapt existing content for other channels |
| **community** | Plan community engagement responses |
| **strategy-review** | Monthly strategy review and adjustment |

### 2. Load Context

Read:

1. `marketing/MARKETING.md` — strategy, ICP, messaging, voice
2. `marketing/content-calendar.md` — planned tasks
3. Recent materials in `marketing/` — maintain consistency

### 3. Execute Operation

#### social-post

1. Determine topic from content calendar, trending topic, or user request
2. Research current conversations if trend-based
3. Draft post per platform:
   - X/Twitter: 280 chars max, hook first line, 1-3 hashtags
   - LinkedIn: professional tone, 1-3 paragraphs, 3-5 hashtags
   - Reddit: community tone, value-first, no self-promotion
4. Humanize — apply `humanizer` skill to remove AI writing patterns
5. Suggest visual direction if appropriate
6. Save to `marketing/posts/YYYY-MM-DD-[platform]-[topic].md`
7. Present draft. Wait for approval.

#### blog-post

Delegate to `blog-post` skill. Pass ICP, content pillars, and voice from MARKETING.md.

#### email

1. Define campaign type (newsletter / update / nurture / announcement)
2. Draft subject line (3 variants), preview text, body, CTA
3. Humanize — apply `humanizer` skill to remove AI writing patterns
4. Define target audience segment
5. Save to `marketing/emails/YYYY-MM-DD-[campaign-name].md`
6. Present draft. Wait for approval.

#### trend-research

1. Scan X/Twitter, Hacker News, Reddit, Google Trends, industry newsletters
2. Identify content opportunities and conversations to join
3. Save to `marketing/research/YYYY-MM-DD-trends.md`
4. Update content calendar with new ideas

#### analytics

1. Review metrics against KPIs in MARKETING.md
2. Analyze what is working and what is not
3. Recommend channel, content, or schedule adjustments
4. Save to `marketing/reports/YYYY-MM-DD-analytics.md`
5. Update MARKETING.md if strategy adjustments needed

#### content-repurpose

1. Select source (blog post, feature release, case study)
2. Adapt to other formats (X thread, LinkedIn post, email snippet)
3. Humanize adapted content
4. Save variants to `marketing/posts/`

#### community

1. Identify relevant threads and discussions
2. Draft helpful, value-first, non-promotional responses
3. Save to `marketing/community/YYYY-MM-DD-engagement.md`

#### strategy-review

1. Review MARKETING.md against actual results
2. Assess goal progress, channel effectiveness, content performance
3. Adjust strategy, pillars, channel priorities, resource allocation
4. Update `marketing/MARKETING.md` and `marketing/content-calendar.md`

### 4. Update Tracking

After every operation:

1. Update `marketing/content-calendar.md` — mark completed, add new items
2. If strategy implications — update `marketing/MARKETING.md`

### 5. Report

Summarize:

- Operation performed
- Materials created (file paths)
- Status (draft / published / scheduled)
- Next scheduled task from content calendar
- Follow-ups if any

## Integration

- **Skills**: `marketing-operations` (setup template, channel playbooks), `content-creation` (AI content tools, quality gates), `humanizer` (AI writing pattern removal)
- **Rules**: `humanize-content` (enforces humanizer pass on all marketing content)
- **Sub-workflows**: `blog-post`, `seo-review`, `docs`
- **Follow-up**: `pre-commit`, `create-pr`
