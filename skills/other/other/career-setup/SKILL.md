---
name: career-setup
description: Initialize career development system (job description, ladder, reviews, goals)
disable-model-invocation: true
---

## Purpose

Initialize your Career Development system in Dex. Captures your job description, career ladder, latest review, and long-term growth goals to create a foundation for ongoing career coaching.

## Usage

```
/career-setup
```

One-time setup (or re-run to update). Creates your Career folder and baseline context.

---

## Process Flow

### Phase 1: Introduction & Context

Start with a warm introduction and explain what we're setting up:

```markdown
## Career Development Setup

I'm going to help you set up a Career Development system in Dex. This will become your personal career coach — tracking your growth, capturing evidence of your work, and helping you prepare for reviews and promotions.

**What we'll capture:**
- Your current role & responsibilities  
- Your company's career ladder / competency framework
- Your most recent performance review
- Your long-term growth goals

**How to share documents:**
Since you're in Cursor with Markdown files, here are the easiest ways to get PDFs/Word docs into the system:

1. **Copy/paste approach** (recommended):
   - Open your PDF or Word doc
   - Select all text (Cmd+A) and copy
   - Paste it here when I ask for it
   - Don't worry about formatting — I'll clean it up

2. **Screenshot approach**:
   - Take screenshots of key sections
   - Drag images directly into this chat
   - I can read text from images

3. **File reference**:
   - If you have a file path, just share it
   - I can read most document formats directly

---

**Ready to start? Let me know and I'll walk you through it.**
```

Wait for confirmation before proceeding.

---

### Phase 2: Current Role

Ask for job description and responsibilities:

```markdown
## Step 1: Your Current Role

**First, let's capture what you do today.**

Please share:
1. Your official job title
2. Your job description (copy/paste from your company's JD, or just describe it in your own words)
3. Your team/department
4. Key responsibilities

You can be as detailed or brief as you like — whatever helps paint the picture.
```

After they respond, **acknowledge and summarize**:

```markdown
Got it. So you're a [ROLE] on the [TEAM], focused on [SUMMARY OF RESPONSIBILITIES].

✓ Role captured.

Next up: your career ladder.
```

---

### Phase 3: Career Ladder

Ask for career framework:

```markdown
## Step 2: Career Ladder

**Now let's get your company's career framework.**

Please share your career ladder or competency framework. This is usually:
- A document showing levels (e.g., "Associate PM → PM → Senior PM → Staff PM")
- Descriptions of what's expected at each level
- Skills, behaviors, or outcomes for progression

**What I need:**
- What's your current level?
- What's the next level you're working toward?
- What does that next level require? (competencies, skills, behaviors)

Copy/paste the relevant sections, or just describe it in your own words.
```

After they respond, **acknowledge and extract key info**:

```markdown
Perfect. So you're currently at [CURRENT LEVEL], working toward [NEXT LEVEL].

**Key requirements for [NEXT LEVEL]:**
- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

✓ Career ladder captured.

Next: your latest review.
```

---

### Phase 4: Latest Performance Review

Ask for most recent review:

```markdown
## Step 3: Latest Performance Review

**Now let's get your most recent formal review.**

This could be:
- Annual performance review
- Quarterly check-in
- Half-yearly review
- Latest 1:1 notes with your manager

**What I need:**
- When was the review? (approximate date is fine)
- What feedback did you receive? (strengths, areas for improvement)
- Any ratings or scores?
- Any specific goals or action items from that review?

Share as much or as little as you're comfortable with. This is just for you — it helps me understand your current trajectory.
```

After they respond, **acknowledge and summarize**:

```markdown
Thanks for sharing that. From your [DATE] review:

**Strengths recognized:**
- [Strength 1]
- [Strength 2]

**Growth areas identified:**
- [Area 1]
- [Area 2]

**Action items from that review:**
- [Action 1]
- [Action 2]

✓ Latest review captured.

Last step: your long-term goals.
```

---

### Phase 5: Growth Goals

Ask about aspirations:

```markdown
## Step 4: Long-Term Growth Goals

**Finally, let's talk about where you want to go.**

Think 1-3 years out:

1. What role or level are you working toward?
2. What skills do you want to develop?
3. What kind of impact do you want to have?
4. Any specific career milestones? (e.g., lead a team, ship a major product, become a subject matter expert)

Don't overthink it — just share what you're aiming for, even if it's still fuzzy.
```

After they respond, **acknowledge and confirm**:

```markdown
Great. So your growth direction:

**Target Role:** [ROLE/LEVEL]

**Key Development Areas:**
- [Skill 1]
- [Skill 2]
- [Skill 3]

**Desired Impact:**
- [Impact goal 1]
- [Impact goal 2]

✓ Growth goals captured.

---

**All set! Let me create your Career folder and save this context.**
```

---

### Phase 6: Create Files & Summary

Create the folder structure and files:

**1. Create folder:** `05-Areas/Career/`

**2. Create `05-Areas/Career/Current_Role.md`:**

```markdown
# Current Role

**Job Title:** [TITLE]
**Team/Department:** [TEAM]
**Last Updated:** YYYY-MM-DD

---

## Official Job Description

[Job description they provided]

---

## Key Responsibilities

- [Responsibility 1]
- [Responsibility 2]
- [Responsibility 3]

---

## Team Context

[Any team context they mentioned]

---

## Notes

[Any additional context worth capturing]
```

**3. Create `05-Areas/Career/Career_Ladder.md`:**

```markdown
# Career Ladder

**Company:** [COMPANY]
**Current Level:** [CURRENT LEVEL]
**Target Level:** [TARGET LEVEL]
**Last Updated:** YYYY-MM-DD

---

## Career Framework

[Their career framework/ladder information]

---

## Current Level: [CURRENT LEVEL]

**Expectations:**
- [Expectation 1]
- [Expectation 2]
- [Expectation 3]

---

## Target Level: [TARGET LEVEL]

**Requirements for Promotion:**

### [Competency Category 1]
- [Requirement 1]
- [Requirement 2]

### [Competency Category 2]
- [Requirement 1]
- [Requirement 2]

### [Competency Category 3]
- [Requirement 1]
- [Requirement 2]

---

## Gap Analysis

**What I'm already demonstrating:**
- [To be filled during career-coach sessions]

**What I need to develop:**
- [To be filled during career-coach sessions]

---

## Notes

[Any additional context about the ladder]
```

**4. Create `05-Areas/Career/Review_History.md`:**

```markdown
# Review History

Track formal performance reviews, feedback, and progress over time.

---

## [MOST RECENT DATE] - [Review Type]

**Overall Assessment:** [Rating/summary]

### Strengths Recognized

- [Strength 1]
- [Strength 2]
- [Strength 3]

### Areas for Growth

- [Growth area 1]
- [Growth area 2]

### Action Items

- [ ] [Action 1]
- [ ] [Action 2]
- [ ] [Action 3]

### Manager Feedback

[Key quotes or notes from manager]

---

## Notes

*Future reviews will be appended below as they happen.*

---

**How to use this file:**
- After each formal review, add a new section at the top
- Use `/career-coach` to reflect on progress against past feedback
- Reference this when preparing for promotion discussions
```

**5. Create `05-Areas/Career/Growth_Goals.md`:**

```markdown
# Growth Goals

**Last Updated:** YYYY-MM-DD

---

## Long-Term Vision (1-3 years)

**Target Role:** [ROLE/LEVEL]

**Why This Matters to Me:**
[Their motivations]

---

## Development Focus Areas

### [Skill Area 1]
**Current State:** [Where they are now]
**Target State:** [Where they want to be]
**How I'm Developing This:**
- [Approach 1]
- [Approach 2]

### [Skill Area 2]
**Current State:** [Where they are now]
**Target State:** [Where they want to be]
**How I'm Developing This:**
- [Approach 1]
- [Approach 2]

### [Skill Area 3]
**Current State:** [Where they are now]
**Target State:** [Where they want to be]
**How I'm Developing This:**
- [Approach 1]
- [Approach 2]

---

## Impact Goals

What I want to accomplish:

1. [Impact goal 1]
2. [Impact goal 2]
3. [Impact goal 3]

---

## Career Milestones

Specific achievements I'm working toward:

- [ ] [Milestone 1]
- [ ] [Milestone 2]
- [ ] [Milestone 3]

---

## Reflections

*Use this section to capture thoughts on your career journey as it evolves.*

---

**Related:**
- See `Review_History.md` for formal feedback
- See `Career_Ladder.md` for promotion requirements
- Use `/career-coach` to work through career challenges
```

**6. Create `05-Areas/Career/Evidence/` folder structure:**

```
06-Resources/
└── Career_Evidence/
    ├── README.md
    ├── Achievements/
    ├── Feedback_Received/
    └── Skills_Development/
```

**7. Create `05-Areas/Career/Evidence/README.md`:**

```markdown
# Career Evidence

This folder captures evidence of your professional growth — achievements, feedback, and skill development over time.

---

## How This Works

As you work, Dex automatically captures evidence that supports your career progression:

- **Achievements/**: Major wins, successful projects, measurable impact
- **Feedback_Received/**: Praise from colleagues, stakeholders, manager feedback
- **Skills_Development/**: Examples of skills you're building (captured from meetings, projects)

---

## When Evidence Gets Captured

1. **During `/review`**: End-of-day reflections prompt for notable achievements
2. **From Granola meetings**: Feedback and discussions with your manager are extracted
3. **Project completions**: When you finish projects, you'll be asked if there's career evidence worth noting
4. **Ad-hoc**: Just tell me "capture this for my career evidence" and I'll add it

---

## How to Use This Evidence

- **Preparing for reviews**: Run `/career-coach` → "prepare best self-review"
- **Promotion discussions**: Reference specific files when building your case
- **Goal tracking**: See tangible progress on skills you're developing
- **Reflection**: Look back at growth over time

---

## File Naming Convention

- `YYYY-MM-DD - [Short Description].md`
- Example: `2026-01-28 - Led Cross-Team API Migration.md`

---

**This system is most powerful when it captures evidence passively as you work. Don't worry about manual updates — Dex handles it.**
```

---

### Phase 7: Completion Summary

After creating all files:

```markdown
## ✅ Career Development Setup Complete

Your Career system is now live. Here's what I created:

### Files Created

**`05-Areas/Career/`**
- `Current_Role.md` — Your job description and responsibilities
- `Career_Ladder.md` — Progression framework and promotion requirements
- `Review_History.md` — Performance review tracking
- `Growth_Goals.md` — Long-term development objectives

**`05-Areas/Career/Evidence/`**
- Evidence capture system for achievements, feedback, and skill development

---

## How to Use This System

### Regular Check-ins

Run `/career-coach` anytime you want to:
1. **Reflect on a challenge** — Brain dump about work struggles, get coaching
2. **Generate a report** — Create a weekly update for your manager
3. **Prepare for reviews** — Build self-assessment from accumulated evidence
4. **Assess promotion readiness** — Gap analysis against career ladder

### Automatic Capture

As you use Dex:
- **Meetings with your manager** (via Granola) → Feedback automatically extracted
- **Daily reviews** (`/review`) → Achievements captured as career evidence
- **Project completions** → Impact and skills demonstrated are saved

### Quarterly Career Check-ins

Every quarter, run `/career-coach` to:
- Review progress against growth goals
- Update evidence of skills development
- Adjust focus areas based on feedback
- Prepare for formal reviews

---

## Try It Now

Want to test it out? Try:

`/career-coach` → then brain dump about a current work challenge

I'll ask clarifying questions and help you work through it, then capture learnings for your career evidence.

---

**Your career development system is ready. Let's build your growth trajectory together.**
```

---

## Edge Cases

### If They Don't Have a Career Ladder

```markdown
No career ladder at your company? No problem.

We can use a generic framework based on your role type, or I can help you define your own progression criteria.

Want me to suggest a framework based on [THEIR ROLE]?
```

Then offer to create a basic ladder structure.

### If They're Uncomfortable Sharing Review Details

```markdown
Totally understand. We can keep this high-level.

Just give me:
- General themes from your last review (e.g., "strong on execution, need to work on communication")
- Any specific goals or action items

That's enough to make the system useful.
```

### If They Want to Skip Sections

```markdown
No problem — we can fill that in later.

For now, I'll create the folder structure and you can update files when you're ready. The system still works without everything filled in.
```

---

## Post-Setup Behavior

After running `/career-setup` once:

1. **Career folder exists** → Dex knows to capture career evidence during daily work
2. **Granola integration** → Manager 1:1s are flagged for feedback extraction
3. **Review prompts** → End-of-day reviews ask about achievements worth capturing
4. **Project completions** → Prompt to add impact to career evidence

---

## Updating Career Info

To update any career file later, just say:

- "Update my career ladder" → Re-run ladder capture
- "Add my latest review" → Append to Review_History.md
- "Revise my growth goals" → Edit Growth_Goals.md

Or manually edit the files — they're just Markdown.

---

## Integration with Dex System

- **Pillars**: Career goals can connect to strategic pillars
- **Quarter Goals**: Growth objectives can become quarterly goals
- **People pages**: Manager's page links to career discussions
- **Projects**: Project outcomes become career evidence

---

## When to Run This

- **First time using Dex** → Part of onboarding
- **Starting a new role** → Reset and recapture
- **Promotion cycle** → Refresh and update
- **Annual planning** → Review and revise goals

---

**This command sets the foundation. The real power comes from `/career-coach` and ongoing evidence capture.**

---

## Track Usage (Silent)

Update `System/usage_log.md` to mark career setup as used.

**Analytics (Silent):**

Call `track_event` with event_name `career_setup_completed` and properties:
- `ladder_uploaded`
- `goals_set`

This only fires if the user has opted into analytics. No action needed if it returns "analytics_disabled".
