---
name: linear-method
description: Linear's proven methodology for software development and project organization. Use when helping users plan work, create issues, structure projects, set direction, prioritize tasks, or organize development workflows. Applies Linear's principles of momentum, simplicity, and focus—not API integration. For solo developers and teams organizing software projects.
---

# Linear Method

This skill embodies Linear's philosophy and best practices for building software with focus, momentum, and quality. Use it to help organize work according to proven principles that distinguish world-class product teams.

## Core Philosophy

**Speed through simplicity**: Tools should help creators stay productive, not create bureaucracy. Keep individuals moving fast rather than generating perfect reports.

**Momentum over perfection**: Take swift action daily. Ship constantly. Multiple small launches beat one big launch.

**Clarity of direction**: Connect every task to larger goals. Everyone should understand what matters and why.

**Manageable scope**: Scope projects down aggressively. Break large work into completable stages. Small, concrete tasks feel great to finish.

## Writing Issues (The Linear Way)

Issues communicate tasks clearly and concisely. NO user stories—they're cargo cult that wastes time.

### Issue Structure

**Title**: Plain language describing the task
```
Good: "Add password reset flow"
Bad: "As a user, I want to reset my password so that..."
```

**Description** (when needed):
- What needs to be done
- Why it matters (brief context)
- Acceptance criteria (if complex)
- Links to relevant user feedback (quote directly, don't summarize)

### Key Principles

1. **Write your own issues**: Forces deep thinking about the problem
2. **Describe tasks with clear outcomes**: Code, design, document, or action
3. **Keep it brief**: If it needs explanation, it's too big—break it down
4. **Quote user feedback directly**: Users describe pain authentically
5. **Everyone writes their own work**: The person doing the work understands it best

### What Makes a Good Issue

✅ **Good Issues**:
- "Implement email verification for signup"
- "Fix sidebar navigation on mobile (clips off screen)"
- "Add loading state to dashboard while fetching data"
- "Research best practices for rate limiting APIs"

❌ **Bad Issues** (User Stories):
- "As a user, I want email verification so I can secure my account"
- "As a mobile user, I want to see the full sidebar..."
- Long, detailed specifications that should be project specs

### Issue Size

Issues should be completable in 1-3 days max. If longer:
- Break into sub-issues
- Create a Project to organize related issues
- Scope down the initial version

### Special Cases

**Exploration issues**: "Explore design options for dashboard" or "Research authentication libraries" are valid placeholder issues that get broken down later.

**Bug reports from others**: Frame as problem description, let assignee determine solution and rewrite as task.

**Feature requests**: Include direct user quotes and link to original conversation. Focus on the pain point, not the requested solution.

## Structuring Projects

Projects organize related issues toward a specific deliverable or feature.

### Project Anatomy

**Name**: Clear, specific feature or deliverable
```
Good: "User Authentication System"
Bad: "Authentication Improvements"
```

**Brief spec** (1-2 paragraphs):
- **Why**: What problem this solves
- **What**: What you're building
- **How**: High-level approach

**Timeline**: Target completion date (use for planning, not pressure)

**Issues**: 5-15 specific tasks that deliver the project

### Project Principles

1. **Scope down aggressively**: Shorter projects = faster shipping = quicker feedback
2. **Break into stages**: If can't scope down, ship V1 then V2
3. **Small teams move faster**: Solo or 2-3 people max when possible
4. **Write specs before building**: Spend days/weeks thinking through the approach first
5. **Ship early versions**: Use your own product immediately to find issues

### Example Project Breakdown

**Project**: "User Authentication"
- Set up auth library
- Create signup form + API
- Create login form + API  
- Add session management
- Build password reset flow
- Add email verification
- Test complete auth flow

Each issue = 1-3 days of work = completable this week

## Setting Direction

Direction keeps work aligned to meaningful goals.

### Hierarchy

**Initiatives** (months) → **Projects** (weeks) → **Issues** (days)

### Initiatives

Major streams of work over 2-6 months:
- "Build MVP Core Features"
- "Acquire First 100 Users"
- "Launch Payment System"

**Purpose**: Everyone understands what's most important and why

### Goals

Measurable targets that push you forward:
- Start small: 10 users → 100 users → $1K MRR
- Walk back from big goals: path to 10 users starts with 1 user
- Make it measurable: "Launch to users" is vague; "10 weekly active users" is clear

### Product Timeline

Map initiatives and projects on a timeline:
- Shows path of execution for near future
- Slightly out of reach (ambitious but achievable)
- Visible to everyone for alignment

## Prioritization Framework

Not all work is equal. Distinguish enablers from blockers, now from later.

### Enablers vs Blockers

**Blockers**: Gaps preventing someone from using your product
**Enablers**: Features opening new opportunities or markets

Ask: "Does this prevent usage or is it nice-to-have?"

### Now vs Later

**Critical questions**:
1. Is this important NOW or can it wait?
2. Does this help achieve current goals?
3. What are the compounding effects of building it now?
4. What complexity or costs does it add?

**Prioritize**: Things that move the needle this week/month

### Timely Prioritization

In early stages, many features are "eventually needed."

Build the minimum to unblock progress now. Add polish later. Focus on what enables the next growth milestone.

## Working in Cycles

Cycles create healthy routine and focus.

### Standard Cycle: 2 Weeks

- Short enough: Don't lose sight of priorities
- Long enough: Ship meaningful features
- Natural review rhythm: What worked? What's next?

### Cycle Principles

1. **Don't overload**: Cycles should feel reasonable
2. **Auto-move unfinished work**: No guilt about things moving to next cycle
3. **Review at boundaries**: What got done, what blocked you, plan next priorities
4. **Pull from projects**: Take issues from planned projects based on current goals

### Solo Developer Cycles

- Week 1: Build 3-5 issues
- Week 2: Build 3-5 issues + polish + write changelog
- Review: What shipped? What's next priority?

## Building with Momentum

Momentum comes from consistent, visible progress.

### Daily Momentum

- Take swift action—decide to do or not do, don't just think about it
- Complete 1-3 small issues daily
- Mark things Done (feels great!)
- Show the diff/output—visible progress is motivating

### Weekly Momentum  

- Ship something every week
- Write changelog entries (even with few users)
- See progress accumulate
- Build habits of constant shipping

### Launch Momentum

- Launch multiple times (not one big launch)
- Announce → Beta → Public → Funding → Major features
- Each launch builds following for next launch
- Better than waiting for "perfect moment"

### Build in Public

- Publish weekly changelogs
- Show what you're building openly
- Your speed discourages competition more than secrecy helps

## Managing Backlogs

Keep backlogs manageable—you don't need every idea forever.

### Auto-Archive

- Completed issues after X months
- Completed cycles/projects when all issues archived
- Keeps focus on what matters now

### Delete vs Archive

- **Archive**: Let Linear manage automatically for completed work
- **Delete**: Use for mistakes, duplicates, truly wrong ideas

### Feedback as Research Library

- Collect all user feedback
- Don't treat it as backlog of work
- Use to spot trends when planning features
- Attach feedback to relevant issues

## Design and Exploration Work

Design requires structure but needs freedom to explore.

### Design Project Flow

1. **Verify the problem**: Does it exist? Is it worth solving?
2. **Explore freely**: Create "Explore designs" issue, try multiple options
3. **Get early feedback**: Share rough work, don't polish first
4. **Pick direction**: Choose best option after feedback
5. **Break into tasks**: "Design login screen", "Design dashboard layout"
6. **Implement**: Work closely with engineering throughout

### Collaboration Patterns

- Write project specs together
- Share Figma/screenshots in issue comments
- Use sub-issues to split design/engineering tasks
- Get feedback while still exploring

## Balance User Feedback with Vision

Build WITH users, not just FOR users.

### Using Feedback Well

1. **Ask about the problem**: "What are you trying to solve?" not "What feature do you want?"
2. **Understand use case**: Why does this matter to them?
3. **Evaluate timing**: Is this for your target user NOW?
4. **Refine your vision**: Let feedback inform, not dictate

### When to Ignore Feedback

- From non-target users (enterprise feedback when building for startups)
- Feature requests without understanding the pain point
- When it conflicts with your product vision
- Nice-to-haves that don't unblock usage

## References

For detailed examples and patterns:

- `references/issue_examples.md` - Extensive examples of good vs bad issues
- `references/project_templates.md` - Project spec templates and breakdowns
- `references/solo_workflows.md` - Specific workflows for solo developers

## When to Use This Skill

Apply Linear Method principles when:

- Creating issues (ensure plain language, clear scope)
- Planning projects (scope down, write specs, break into stages)
- Setting priorities (enablers vs blockers, now vs later)
- Organizing work (cycles, initiatives, goals)
- Writing specs or changelogs
- Deciding what to build next
- Helping users think through software development workflow

This skill provides **conceptual guidance**, not API integration. When users ask to "create an issue about X", help them craft it according to these principles—don't write API code.
