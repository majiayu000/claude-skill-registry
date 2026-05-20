---
name: launch-announcement
description: Use when creating internal product launch announcements - gathers information from PRDs and user input to write customer-centric feature launch communications for internal teams
---

# Launch Announcement

## Purpose

Create crisp, clear, customer-centric internal launch announcements for new features and experiments. This skill generates structured communication for cross-functional teams (product, eng, design, data, sales, CS, marketing, leadership) about shipped features.

## When to Use This Skill

Activate when:
- User invokes `/launch-announcement`
- Writing internal launch announcement for shipped feature
- Communicating feature release to internal stakeholders
- Documenting feature launch after deployment

**When NOT to use:**
- External customer communications (press releases, blog posts)
- Pre-launch feature previews or teasers
- Roadmap updates (use `roadmap-updating` instead)

## Workflow

### Step 1: Announce and Research

**Announce to user:** "I'm researching existing documentation to pre-fill the announcement template. Looking for PRDs, experiments, and related product documentation."

**Search workspace:**
- Look in `datasets/product/prds/` for matching PRD
- Check `datasets/product/roadmap.md` for feature references
- Search `datasets/meetings/` for customer signals related to the feature

**Report findings:** Tell user what you found and what information you can pre-fill.

### Step 2: Gather Missing Information

**Ask user for information not found in documentation:**

Required inputs:
- **Org/Team name**: Which team shipped this?
- **Feature name**: What is the feature called?
- **Short descriptor/tagline**: Brief descriptor for title
- **Rollout details**: GA, beta, experiment, A/B test? Who is exposed?
- **What actually shipped**: Confirm specifics match documentation (often differs)

Optional inputs (ask if not found):
- **Customer segment/persona**: Who is this for?
- **Customer problem details**: Expand on PRD's customer statement if needed
- **Detailed components that shipped**: What specific pieces were delivered?
- **Surfaces/pages where it appears**: Where in product?
- **"Coming soon" items + timing**: What's next and when?
- **Success metrics (baseline + targets)**: Actual values, not assumptions
- **Monitoring/VOC plans**: How will you track this?
- **Early success story**: Any early customer wins?
- **Contributor list by function**: Who to thank?
- **Resource links**: Videos, FAQs, docs, playbooks

**CRITICAL**: Never fabricate numbers, names, or metrics. Always ask user when information is missing.

### Step 3: Structure Announcement

**Follow this exact section ordering:**

#### 1. Launch Title
Format: `[emoji] [Org/Team name] launches [Feature name] [short descriptor] [emoji]`

Example emojis: `:rocket:`, `:sparkles:`, `:chart_with_upwards_trend:`

#### 2. Context & Overview (1-2 paragraphs)
- Short history of the problem
- How it affected customers
- What this launch changes and why it matters
- Customer-first language (their pain, not just tech)

**Source from PRD background section if available.**

#### 3. Customer Problem
Structure as persona statement:
```
I AM [who the customer is]
I AM TRYING TO [their goal]
BUT [what's blocking them]
BECAUSE [root cause]
WHICH MAKES ME FEEL [emotional impact]
```

**Source from PRD's customer statement if available.**

#### 4. What Was Launched?
- 1-2 sentence summary (GA/beta/experiment, exposure)
- Bullet list of key components with:
  - What it is
  - How it works (high level)
  - Why it matters for customers
- **Where it shows up** in product
- **Coming soon** items with timeframes

**Always confirm with user - shipped product often differs from PRD.**

#### 5. From → To (value shift)
Show before/after in bullets:
```
- [Old state] → [New state]
- [Limited capability] → [Comprehensive capability]
- [No insight] → [Clear confidence]
```

**Source from PRD, but confirm with user for accuracy.**

#### 6. How Will We Define Success?
List metrics with baseline and target:
```
- [Metric description]
  - Baseline: [value and unit]
  - Target: [desired value and % change]
```

**NEVER assume metrics. Always confirm with user. Source from PRD/EDD but validate.**

#### 7. What's Next?
- Current status (experiment, phase 1, etc.)
- What you'll be monitoring
- Future phases or related initiatives
- Dependencies or upcoming improvements

**Check roadmap, but validate with user.**

#### 8. Early Success Story (optional)
2-4 sentences about real customer impact already observed.

**Only include if user provides specific story. Do not fabricate.**

#### 9. Shout Outs & HUGE THANKS
- Brief paragraph acknowledging cross-functional effort
- List people grouped by function:
  - Product, Design, Engineering, Data Science/Analytics
  - PMM, Sales/CSM/Support
  - Trust & Safety/Policy/Legal
  - Leadership/Sponsors
  - Special thanks

#### 10. Resources (optional)
- Demo/walkthrough videos
- Internal docs, FAQs, playbooks
- Enablement materials

**Only include if links exist. Do not create placeholder URLs.**

### Step 4: Write Announcement File

**Output location:** `datasets/product/launch-announcements/{YYYY}/launch-{feature-slug}.md`

**Format requirements:**
- Markdown with bold section headers
- Blank lines between sections
- Bullet lists where indicated
- Light, work-appropriate emojis (similar to examples)

**Tone:**
- Clear, confident, customer-first
- Appropriately celebratory ("we shipped!")
- Use "we" for team, "our customers" for users
- Avoid jargon unless standard in org

**Acceptable jargon:**
- "C1" = customer of ours (brands, businesses)
- "C2" = business' customers (subscribers, members)

### Step 5: Confirm with User

Show user the announcement and ask:
- "Does this accurately reflect what was shipped?"
- "Any corrections or additions needed?"

## Quality Gates

**Information Accuracy:**
- No fabricated numbers, names, or metrics
- Shipped features confirmed with user
- All metrics validated (baseline + target)

**Citation Requirements:**
- Reference PRDs and source documents when used
- Customer quotes attributed with dates

**Style Compliance:**
- Bold section headers used consistently
- Blank lines between sections
- Emojis used appropriately (not overdone)

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Fabricating metrics or baselines | Always ask user for actual values |
| Assuming PRD matches shipped product | Confirm what actually shipped with user |
| Creating placeholder URLs | Only include links that exist |
| Over-using emojis | Light, work-appropriate emojis only |
| Making up success stories | Only include if user provides specific story |
| Skipping research phase | Always search for PRD/docs first |

## Success Criteria

- Announcement file written to correct location
- All 9 required sections included (10 if resources available)
- No fabricated information (TBD if unknown)
- Customer-centric language throughout
- User confirms accuracy of shipped features
- Metrics validated with user
- Template structure followed exactly

## Related Skills

- **prd-creation**: Source for customer problem and requirements
- **meeting-synthesis**: Source for customer signals and quotes
- **content-style**: General content quality standards

