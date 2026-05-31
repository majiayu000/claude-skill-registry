---
name: avoid-feature-creep
description: Prevent feature creep when building software, apps, and AI-powered products. Use this skill when planning features, reviewing scope, building MVPs, managing backlogs, or when a user says "just one more feature." Helps developers and AI agents stay focused, ship faster, and avoid bloated products.
---

# Avoid Feature Creep for Agents

Stop building features nobody needs. This skill helps you ship products that solve real problems without drowning in unnecessary complexity.

Feature creep kills products. It delays launches, burns budgets, exhausts teams, and creates software nobody wants to use. The most successful products do fewer things well.

## The Core Problem

Feature creep is the gradual accumulation of features beyond what your product needs to deliver value. It happens slowly, then all at once.

**Warning signs you're in trouble:**
- Release scope keeps growing without clear user value
- You're copying competitor features without validating need
- Stakeholders keep adding "just one more thing"
- The codebase is getting harder to maintain
- Users complain the product is confusing or bloated
- You haven't shipped in months

**What it costs:**
- Development time on features 80% of users never touch
- Increased bug surface area
- Team burnout and context switching
- Delayed time-to-market
- Technical debt that compounds
- User confusion and abandonment

## Decision Framework

Before adding ANY feature, run through this checklist:

```
1. VALIDATE THE PROBLEM
   □ Does this solve a real, validated user pain point?
   □ Have we talked to actual users about this need?
   □ What evidence supports building this?

2. CHECK ALIGNMENT
   □ Does this support the core product vision?
   □ Would this delay our current release?
   □ What are we NOT building if we build this?

3. MEASURE IMPACT
   □ How will we know if this feature succeeds?
   □ What KPIs will change?
   □ Can we quantify the value (time saved, revenue, retention)?

4. ASSESS COMPLEXITY
   □ What's the true cost (build + test + maintain + document)?
   □ Does this add dependencies or technical debt?
   □ Can we ship a simpler version first?

5. FINAL GUT CHECK
   □ Would we delay launch by a month for this feature?
   □ Is this a differentiator or just table stakes?
   □ Would removing this harm the core experience?
```

If you can't answer YES to questions 1-3 with evidence, do not build the feature.

## Scope Management Rules

**Rule 1: Define and Defend Your MVP**

Write down exactly what "done" means before you start. Document what you're NOT building. Reference this constantly.

```markdown
## MVP Scope Document Template

### Core Problem
[One sentence describing the user problem]

### Success Criteria
[How we know we've solved it]

### In Scope (v1)
- Feature A: [brief description]
- Feature B: [brief description]

### Explicitly Out of Scope
- Feature X: Deferred to v2
- Feature Y: Will not build unless [condition]
- Feature Z: Not our problem to solve

### Non-Negotiables
- Ship by [date]
- Budget: [hours/dollars]
- Core user: [specific persona]
```

**Rule 2: Use Version Control for Scope**

Treat scope like code. Track changes. Require approval for additions.

```bash
# Create a scope document and track it
git add SCOPE.md
git commit -m "Initial MVP scope definition"

# Any scope changes require explicit commits
git commit -m "SCOPE CHANGE: Added feature X - approved by [stakeholder] - impact: +2 weeks"
```

**Rule 3: The 48-Hour Rule**

When someone requests a new feature, wait 48 hours before adding it to the backlog. Most "urgent" requests feel less urgent after reflection.

**Rule 4: Budget-Based Scoping**

Every feature has a cost. When something new comes in, something else must go out.

"Yes, we can add that. Which of these three features should we cut to make room?"

## Saying No

Saying no to features is a skill. Here are templates:

**To stakeholders:**
> "That's an interesting idea. Based on our user research, it doesn't solve our core user's top three problems. Let's add it to the v2 consideration list and revisit after we validate the MVP."

**To executives:**
> "I understand the value this could bring. If we add this, we'll delay launch by [X weeks] and deprioritize [Y feature]. Here are the trade-offs - which path should we take?"

**To users:**
> "Thanks for the feedback. We're focused on [core problem] right now. I've logged this for future consideration. Can you tell me more about why this would be valuable?"

**To yourself:**
> "Is this scratching my own itch or solving a real user problem? Would I bet the release date on this?"

**To AI agents (Claude, Opus, Codex, Ralph, Cursor):**
> "Stop. Before we add this feature, answer: Does this solve the core user problem we defined at the start of this session? If not, add it to a DEFERRED.md file and stay focused on the current scope."

When working with AI coding agents:
- State your scope constraints at the start of every session
- Agents will suggest improvements. Most are out of scope.
- Treat agent suggestions like stakeholder requests: apply the 48-hour rule
- If an agent keeps pushing a feature, ask "Why?" three times to find the real need

## AI-Specific Guidelines

When building AI-powered products, feature creep has extra risks:

**AI Feature Creep Red Flags:**
- Adding AI because "everyone else is"
- Building AI summaries without validating users want them
- Multiple AI features without clear differentiation
- AI capabilities that don't connect to core user workflows

**AI Feature Discipline:**
1. One AI feature at a time
2. Validate the use case with users first
3. Measure actual usage, not just availability
4. Question: "Does the AI make the core task faster or better?"

**Before adding any AI feature, answer:**
- What specific task does this automate?
- How is this better than the non-AI alternative?
- What happens when the AI is wrong?
- Can we ship without this AI feature?

## Backlog Hygiene

A messy backlog enables feature creep. Clean it ruthlessly.

**Monthly Backlog Audit:**
```
For each item older than 30 days:
1. Has anyone asked about this since it was added?
2. Does it still align with current product vision?
3. If we never built this, would anyone notice?

If the answer to all three is "no" → Delete it.
```

**Priority Framework (MoSCoW):**
- **Must Have**: Product doesn't work without it
- **Should Have**: Important but not critical for launch
- **Could Have**: Nice but can wait
- **Won't Have**: Explicitly out of scope

Be honest: Most "Should Haves" are actually "Could Haves" in disguise.

## AI Session Discipline

**Session Start Check:**
Before coding with any AI assistant (Claude, Cursor, OpenCode), state:
- What specific feature you're building
- What's explicitly out of scope for this session
- When you'll stop and ship

**Mid-Session Check:**
Every 30-60 minutes, ask your AI:
"Are we building the right thing today, or are we adding scope?"

If the answer is "adding scope," stop. Commit what you have. Start fresh.

**Session End Check:**
Before closing an AI coding session:
- What did we actually build vs. what we planned?
- Did scope expand? Why?
- What should we defer to the next session?

**Daily AI Check:**
At the end of each day working with AI assistants:
```
1. Features completed today: [list]
2. Scope additions today: [list]  
3. Was each addition validated? [yes/no]
4. Tomorrow's focus: [single item]
```

**Sprint Planning Guard Rails:**
- No new features mid-sprint without removing something
- Capacity for bug fixes and debt paydown (20% minimum)
- Clear definition of done for each item

**Stakeholder Management:**
Create a single source of truth for scope decisions:

```markdown
## Scope Decision Log

| Date | Request | Source | Decision | Rationale | Trade-off |
|------|---------|--------|----------|-----------|-----------|
| 2025-01-15 | Add export to PDF | PM | Deferred v2 | Not core to MVP | Would delay launch 2 weeks |
| 2025-01-16 | Dark mode | User feedback | Approved | User research shows demand | Removed social sharing |
| 2025-01-17 | Add caching layer | Claude | Deferred | Premature optimization | Stay focused on core feature |
| 2025-01-17 | Refactor to hooks | Cursor | Rejected | Works fine as is | Technical scope creep |
```

**Agents as Stakeholders:**
AI coding agents are now stakeholders in your project. They have opinions. They make suggestions. Treat them like any other stakeholder:

- **Log agent suggestions** in your scope decision log with the agent name as source
- **Apply the same rigor** you would to a PM or executive request
- **Agents optimize for different things** (code quality, patterns, completeness) than you might need right now
- **"The agent suggested it" is not a valid reason** to add a feature

Common agent-driven scope creep patterns:
- "Let me also add error handling for edge cases you haven't hit yet"
- "This would be cleaner with a refactor"
- "You should probably add tests for this"
- "Let me add TypeScript types for these additional scenarios"

Each of these might be good ideas. None of them are your current scope unless you decide they are.

## Recovery: You're Already Bloated

If feature creep has already happened:

**Step 1: Audit Current Features**
- List every feature
- Check usage data for each
- Identify features with <5% engagement

**Step 2: Categorize**
- Core: Users can't accomplish their goal without it
- Supporting: Makes core better
- Peripheral: Nice but not necessary
- Bloat: Nobody uses it

**Step 3: Remove or Hide**
- Deprecate bloat with warning period
- Move peripheral features behind advanced settings
- Communicate changes clearly to users

**Step 4: Prevent Recurrence**
- Add feature creep checks to your PR/code review process
- Require usage metrics before features graduate from beta
- Build feature flags so you can easily remove experiments

## Quick Reference Commands

When reviewing any feature request, ask:

```
1. "What user problem does this solve?"
2. "What's the smallest version we could ship?"
3. "What are we NOT building to make room for this?"
4. "How will we measure success?"
5. "What happens if we never build this?"
```

If you can't answer these clearly → Do not proceed.

## The Golden Rule

**Ship something small that works. Then iterate based on real usage data.**

Users don't remember features. They remember whether your product solved their problem.

Every feature you don't build is:
- Time you get back
- Bugs you don't have to fix
- Documentation you don't have to write
- Code you don't have to maintain
- Confusion you don't add

The best products aren't the ones with the most features. They're the ones that do the right things exceptionally well.

---

*"Perfection is achieved not when there is nothing more to add, but when there is nothing left to take away."* - Antoine de Saint-Exupéry
