---
name: prototype-feedback
description: Build → review → iterate prototype workflow. Structured feedback collection and iteration.
disable-model-invocation: false
user-invocable: true
---

# Prototype Feedback Loop Workflow

Rapidly iterate on prototypes using AI-powered building and automated feedback collection.

## Quick Start

1. Share a prototype link (v0/Lovable/Bolt) or describe what you built
2. I check the related PRD, design system, and user research for context
3. I run a structured feedback analysis (PRD alignment, usability, multi-perspective)
4. I deliver prioritized recommendations: must-fix, should-fix, and nice-to-have
5. You iterate on the prototype and we repeat until validated

**Example:** "Review my checkout prototype: [link]. PRD is in outputs/prds/checkout-redesign.md"

**Output:** Saved to `outputs/prototypes/[feature]-feedback-round-[N].md`

**Time:** 30 minutes per feedback round

## Context Routing

**Check these files before providing feedback:**

| Source | Files/Folders | What to Extract |
|--------|---------------|-----------------|
| PRD | `outputs/prds/`, `context-library/prds/` | Requirements, acceptance criteria, success metrics |
| Design System | `context-library/technical/`, design docs | Colors, typography, component patterns to match |
| Stakeholder Profiles | `context-library/stakeholder-*.md` | Who reviews this, their priorities and concerns |
| User Research | `context-library/research/` | User pain points, quotes, behavior patterns |
| Past Prototypes | `outputs/prototypes/` | Previous feedback rounds, resolved issues |

## Overview

**Tools:** v0/Lovable/Bolt + NotebookLM + Claude
**When:** Validating new features before full build

---

## Feedback Analysis Template

Use this structure for every feedback round:

### PRD Alignment Check

| PRD Requirement | Prototype Status | Gap? |
|----------------|-----------------|------|
| [Requirement 1] | Implemented / Partial / Missing | [Description if gap] |
| [Requirement 2] | Implemented / Partial / Missing | [Description if gap] |
| [Requirement 3] | Implemented / Partial / Missing | [Description if gap] |

### Usability Assessment

| Heuristic | Rating (1-5) | Issues | Recommendation |
|-----------|-------------|--------|----------------|
| Visibility of system status | | | |
| Match between system and real world | | | |
| User control and freedom | | | |
| Consistency and standards | | | |
| Error prevention | | | |
| Recognition over recall | | | |
| Flexibility and efficiency | | | |
| Aesthetic and minimal design | | | |

### Multi-Perspective Feedback

**Engineering view:** [Technical feasibility, performance concerns, implementation complexity, tech debt risks]

**Design view:** [Visual consistency, interaction patterns, accessibility gaps, design system alignment]

**User view:** [Ease of use, value clarity, friction points, learning curve, "would they actually use this?"]

### Tool-Specific Feedback Adjustments

Adjust feedback focus based on which tool generated the prototype:

**v0.dev prototypes (single components):**
- Focus on: Component behavior, interaction states, visual polish, responsive behavior
- De-emphasize: Navigation flow, multi-page consistency, backend integration (v0 is component-level)
- Ask: "Does this component work in isolation? How will it integrate with the existing UI?"

**Lovable/Bolt.new prototypes (full-stack apps):**
- Focus on: End-to-end user flow, page-to-page navigation, data persistence, error handling
- De-emphasize: Pixel-perfect styling (these tools prioritize function over form)
- Ask: "Does the full flow work? Are there dead ends or missing states?"

**Claude Artifacts (quick mockups):**
- Focus on: Conceptual accuracy, layout structure, content hierarchy
- De-emphasize: Visual fidelity, interaction details (Artifacts are low-fidelity by nature)
- Ask: "Does this capture the right concept? Is the information architecture correct?"

**Figma prototypes (designer-created):**
- Focus on: Design system compliance, accessibility, edge case handling, micro-interactions
- De-emphasize: Technical feasibility (that's the engineer's feedback domain)
- Ask: "Is this usable? Does it handle real-world scenarios beyond the happy path?"

**ASCII/napkin sketches (from /napkin-sketch):**
- Focus on: Layout logic, information hierarchy, flow completeness
- De-emphasize: Everything visual (it's ASCII art, not a design comp)
- Ask: "Is the structure right? Are we missing any screens or states?"

### Prioritized Recommendations

| # | Issue | Severity | Fix | Iteration |
|---|-------|----------|-----|-----------|
| 1 | [Must-fix before beta] | Critical | [Specific fix] | Current |
| 2 | [Should-fix before GA] | Medium | [Specific fix] | Next |
| 3 | [Nice-to-have polish] | Low | [Specific fix] | Later |

---

## Workflow

### Step 1: Build Initial Prototype

**Using v0 (for UI components):**

```bash
# Go to v0.dev
# Paste your feature description:

"Build a task management interface with:
- List view of tasks with checkboxes
- Ability to add new tasks
- Filter by status (all/active/completed)
- Clean, modern design similar to Linear

Include:
- Search functionality
- Due date display
- Priority labels (high/medium/low)"
```

**v0 generates:**
- React component
- Fully functional prototype
- Copy-paste ready code

**Using Lovable (for full-stack apps):**

```bash
# Go to lovable.dev
# Describe full feature:

"Build a customer feedback submission portal:
- Public form for submitting feedback
- Backend to store submissions
- Admin dashboard to review
- Email notifications on new submissions"
```

**Lovable generates:**
- Frontend + backend
- Database schema
- Working prototype with real functionality

**Using Bolt (middle ground):**
- Good for interactive prototypes
- Handles forms, validation, multi-step flows
- Between v0 (UI only) and Lovable (full stack)

**Pro tip:** Start with PRD from your PRD workflow, paste into AI builder, get 80% done automatically.

### Step 2: Refine Prototype (30-60 min)

**Iterate with AI:**

```
"Make these changes:
1. Move the search bar to the top right
2. Add bulk actions (select multiple, mark complete)
3. Make priority labels more prominent
4. Add keyboard shortcuts (enter to add task, / for search)"
```

AI updates code in real-time. Test changes immediately.

**Polish details:**
- [ ] Error states (what happens when something fails?)
- [ ] Empty states (what shows when no data?)
- [ ] Loading states (what shows while loading?)
- [ ] Mobile responsive (does it work on phone?)

### Step 3: Collect User Feedback (1 day)

**Deploy prototype:**
- v0: Export to CodeSandbox or Netlify
- Lovable: One-click deploy
- Bolt: Deploy to their hosting

**Share with users:**

**Email template:**
```
Subject: Quick feedback needed on [Feature] prototype

Hi [Name],

We're exploring [feature] and would love 15 minutes of your time to get feedback on a prototype.

Try it here: [link]
Then book time: [calendly link]

Or just reply with your thoughts!

Thanks,
[You]
```

**Interview script:**
```
1. Don't explain anything. Just share link.
2. Watch them try to use it (screen share).
3. Ask: "What do you think this does?"
4. Ask: "Try to [accomplish task]. Think out loud."
5. Note: Where do they get confused? What surprises them?
6. Ask: "Would you use this? Why/why not?"
7. Ask: "What's missing? What would you change?"
```

**Capture everything:**
- Record sessions (with permission)
- Take notes
- Screenshots of confused moments

### Step 4: Synthesize Feedback (30 min)

**Use NotebookLM:**

1. Upload all interview transcripts
2. Upload session recordings (transcribe first)
3. Upload notes

**Query:**
```
"Analyze these user feedback sessions:

1. What patterns did you see?
   - Where did users get confused?
   - What worked well?
   - What didn't work at all?

2. Group feedback into themes

3. Rate each issue by:
   - Frequency (how many users hit this?)
   - Severity (how bad is it?)

4. Recommend top 3 changes for next iteration"
```

**Output:** Prioritized list of changes to make.

### Step 5: Iterate Prototype (1-2 hours)

**Make top changes:**

```bash
# Back to v0/Lovable/Bolt

"Based on user feedback, make these changes:

High priority:
1. [Change 1 - 80% of users confused by X]
2. [Change 2 - 60% of users couldn't find Y]
3. [Change 3 - 100% of users asked for Z]

Update the prototype to address these issues."
```

AI updates the prototype. Test yourself.

### Step 6: Second Round of Feedback (1 day)

**Same process, new users (if possible):**
- Show updated prototype
- See if issues are fixed
- Discover new issues

**Or test with same users:**
- "Here's the updated version"
- "Did we address your concerns?"
- "What else needs work?"

### Step 7: Decide to Build or Iterate (30 min)

**Success criteria checklist:**
- [ ] Users understand what it does (>80%)
- [ ] Users can complete core tasks (>70%)
- [ ] Users would actually use this (>60%)
- [ ] No critical usability issues
- [ ] Feedback is mostly positive

**If yes:** Write real PRD and hand off to eng/design  
**If no:** Another iteration or pivot

---

## Automation Opportunities

### Automated Feedback Collection

**Using Typeform + Make.com:**

1. User tries prototype
2. Typeform survey pops up automatically
3. Responses go to Airtable
4. Claude synthesizes daily
5. Slack notification with insights

**Questions to ask:**
- What were you trying to do?
- Did you accomplish it? (Yes/No)
- What was confusing?
- What would you change?
- Would you use this? (1-5 scale)

### Automated Session Recording

**Using FullStory or Hotjar:**
- Tracks all user sessions
- Shows where users click, scroll, rage-click
- Heatmaps show attention patterns
- AI can analyze patterns

### Continuous Feedback Loop

**Weekly cycle:**
1. **Monday:** Build/update prototype
2. **Tuesday-Thursday:** Collect feedback
3. **Friday:** Synthesize and iterate
4. **Repeat** until validated

---

## Example: Full Cycle

**Week 1:**
- Built initial prototype (2 hours)
- Tested with 5 users (1 day)
- Found: Nobody understood the navigation
- Iterated: Simplified nav (1 hour)

**Week 2:**
- Tested new version with 5 users (1 day)
- Found: Nav fixed! But bulk actions confusing
- Iterated: Redesigned bulk actions (1 hour)

**Week 3:**
- Tested again with 3 users (1 day)
- Found: 100% success rate on core tasks
- Decision: Validated! Write real PRD

**Total time:** 3 weeks, ~12 hours of work  
**Alternative:** 7-12 weeks, full build, then discover it's wrong

**ROI:** 6-9 weeks saved, $50K+ in eng time saved

---

## Common Mistakes

**Don't:**
- ❌ Build production code (it's a prototype!)
- ❌ Make it perfect (good enough to test)
- ❌ Test with only internal team (get real users)
- ❌ Ignore negative feedback (embrace it)
- ❌ Iterate forever (set a limit: 3-4 rounds max)

**Do:**
- ✅ Build fast, test fast, learn fast
- ✅ Embrace rough edges (it's fine for a prototype)
- ✅ Get in front of real users ASAP
- ✅ Track feedback systematically
- ✅ Know when to kill bad ideas early

---

## Tool Recommendations

**For UI prototypes:** v0.dev  
**For full-stack apps:** Lovable.dev  
**For interactive flows:** Bolt.new  
**For feedback synthesis:** NotebookLM  
**For session recording:** FullStory or Hotjar  
**For surveys:** Typeform or Tally

**Start free, upgrade if you're using daily.**

---

## Advanced: Multi-Variant Testing

**Test 2-3 approaches at once:**

**Variant A:** Approach 1 (e.g., wizard-style onboarding)  
**Variant B:** Approach 2 (e.g., dashboard-style onboarding)  
**Variant C:** Approach 3 (e.g., tutorial-style onboarding)

**Split users:**
- 5 users per variant
- See which performs best
- Build the winner

**Faster learning, better outcomes.**

---

## Measuring Success

**Prototype velocity:**
- Ideas → prototype: <2 hours
- Prototype → feedback: <2 days
- Iterations per week: 2-3

**Validation quality:**
- User success rate: >70%
- Would-use rate: >60%
- Critical issues found: 0

**Business impact:**
- Features validated before build: 90%
- Failed features caught early: 100%
- Eng time saved: $50K+ per year

---

**Time saved:** 6-9 weeks per feature
**Cost saved:** $50K+ per year in eng time
**Success rate:** 90% (vs. 40% building without validation)

---

## Output Quality Self-Check

Before delivering prototype feedback, verify:

- [ ] **PRD alignment checked** -- Every PRD requirement is mapped to prototype status (implemented, partial, missing)
- [ ] **Usability heuristics scored** -- At least 5 Nielsen heuristics rated with specific issues noted
- [ ] **Multi-perspective feedback included** -- Engineering, design, and user viewpoints are all represented
- [ ] **Recommendations are prioritized** -- Issues ranked by severity with clear fix descriptions and iteration assignment
- [ ] **Context was checked** -- PRD, user research, and stakeholder profiles were referenced (not just generic feedback)
- [ ] **Actionable next steps** -- PM knows exactly what to change in the next iteration
- [ ] **Success criteria referenced** -- Feedback connects back to PRD success metrics and kill criteria
- [ ] **Previous feedback rounds referenced** -- If this is round 2+, confirm previous issues were resolved

If any check fails, fix it before delivering. Generic feedback wastes iteration cycles.
