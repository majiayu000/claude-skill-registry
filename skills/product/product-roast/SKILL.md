---
name: product-roast
description: Comprehensive product audit skill combining brutal UX/code roasting with behavioral psychology-informed vision crafting. Use when analyzing apps to find bugs, missed opportunities, and transformative improvements. Generates roast reports, vision documents, prioritized roadmaps, GitHub issues, and implementation specs. Works as a guided workshop with interactive questioning.
---

# Product Roast + Vision Workshop

## Overview

Transform apps from "functional" to "holy shit, this gets me" through systematic product analysis that combines:
- **The Roast**: Brutal honesty about what's broken, ugly, confusing, and inefficient
- **The Vision**: Behavioral psychology-informed reimagining of what's possible
- **The Roadmap**: Prioritized action items from quick wins to transformative bets
- **The Implementation**: From analysis to shipped improvements

**Core Principle**: Most apps fail not from bugs, but from missed opportunities. Finding bugs is table stakes. Finding the version that makes users show this to their friends - that's the goal.

## When to Use

Use this skill when:
- Auditing an app for improvement opportunities
- Preparing for a product review or retrospective
- Planning the next development cycle
- Onboarding to a new codebase and wanting to understand its weaknesses
- The app "works" but doesn't delight
- Users aren't returning or engaging as expected

**Target App Types:**
- Habit trackers / Goal apps (specialized frameworks included)
- Clinical/Medical apps (workflow optimization included)
- Any web or mobile application

## The Workshop Process

This skill runs as a **guided workshop** with five phases. Complete each phase before proceeding.

### Phase 1: Context Gathering

**Before any analysis, understand:**

1. **The App**
   - What is it? (one sentence)
   - What's the tech stack?
   - Where's the codebase? (path)
   - Is it deployed? (URL if available)

2. **The Users**
   - Who are they? (persona in 2-3 sentences)
   - What's their context when using this? (rushed? relaxed? stressed?)
   - What job are they hiring this app to do?
   - What alternatives do they have?

3. **The State**
   - What's working well? (don't fix what isn't broken)
   - What's the known pain? (user complaints, intuitions)
   - What metrics matter? (retention, completion rate, NPS, etc.)
   - When did someone last say "wow" about this app?

4. **The Constraints**
   - How much time/resources for improvements?
   - Any technical debt limiting changes?
   - Any business constraints (compliance, integrations)?

**Ask these questions interactively, one at a time, using AskUserQuestion tool.**

### Phase 2: The Roast

**Systematic analysis to find everything wrong.**

**REQUIRED:** Read `references/roast-checklist.md` for complete checklist.

#### Severity Scoring

| Level | Meaning | Action |
|-------|---------|--------|
| 🔥🔥🔥 | **Critical** - Blocks usage, causes abandonment, security risk | Fix immediately |
| 🔥🔥 | **Moderate** - Significantly impacts experience, frustrates users | Fix this sprint |
| 🔥 | **Minor** - Annoying but usable, polish issue | Backlog |

#### Roast Categories

For each category, document issues with:
- **What**: Specific issue description
- **Where**: File path and line number (if code) or screen/flow (if UX)
- **Why it matters**: User impact
- **Severity**: 🔥 to 🔥🔥🔥

**Categories:**
1. **Broken Functionality** - Things that don't work as expected
2. **UX Friction** - Unnecessary steps, confusing flows, cognitive load
3. **Visual Design** - Inconsistent, ugly, unclear hierarchy, accessibility failures
4. **Performance** - Slow, laggy, resource-heavy, bad loading states
5. **Code Quality** - Tech debt, maintainability, patterns that will bite later
6. **Missing Table Stakes** - Basic features competitors have that you don't
7. **Mobile Experience** - Responsive failures, touch targets, thumb zones

#### Automated Analysis Steps

1. **Codebase Scan**
   ```
   - Search for TODO/FIXME/HACK comments
   - Check for console.log/debugger statements
   - Look for commented-out code
   - Identify large files (>500 lines)
   - Check for any security issues (exposed secrets, SQL injection, XSS)
   ```

2. **Dependency Audit**
   ```
   - Check for outdated packages
   - Look for deprecated dependencies
   - Identify unused dependencies
   ```

3. **Type Safety Check**
   ```
   - Run TypeScript compiler
   - Look for `any` types
   - Check for missing types in API responses
   ```

4. **UI/UX Walkthrough**
   ```
   - Navigate every screen
   - Test every interaction
   - Check all states (loading, error, empty, success)
   - Test responsive at 375px, 768px, 1440px
   - Check accessibility (keyboard nav, screen reader, color contrast)
   ```

### Phase 3: The Vision

**For each major feature area, reimagine what's possible.**

**REQUIRED:** Read `references/behavioral-psychology.md` for psychology principles.
**REQUIRED:** Read `references/competitive-patterns.md` for best-in-class examples.

#### Vision Framework

For each feature area, document:

1. **Current State**: What it does now (one line, no judgment)

2. **The Problem**: Why it's mid (specific diagnosis)
   - What user need is unmet?
   - What friction exists?
   - What delight is missing?

3. **The Vision**: What it could be (specific, not vague)
   - Describe the ideal experience in detail
   - Include specific interactions, visuals, feelings
   - "Show, don't tell" - be concrete

4. **The Psychology**: Why this would work
   - Cite specific behavioral principle from references
   - Explain the mechanism
   - Reference competitors who do this well

5. **Implementation Sketch**: Direction (not full code)
   - Key technical components needed
   - Rough effort estimate (small/medium/large)
   - Dependencies or prerequisites

#### Feature Areas to Analyze

**For Habit/Goal Trackers (like GoalConnect):**
- Habit visualization (streaks, graphs, progress)
- Logging experience (friction optimization)
- Streak mechanics (break recovery, freeze)
- Motivation systems (rewards, celebrations)
- Social/accountability features
- Onboarding and "aha moment"
- Daily engagement hooks
- Long-term progression

**For Clinical Apps (like VetHub):**
- Information architecture (glance vs. buried)
- Clinical workflow efficiency
- Quick actions and shortcuts
- Error prevention in high-stakes
- Patient status at a glance
- Documentation speed
- Integration with existing tools
- Shift handoff experience

**For General Apps:**
- Core value proposition delivery
- Navigation and information architecture
- Key user flows (identify top 3)
- Empty states and onboarding
- Error handling and recovery
- Settings and personalization
- Notifications and engagement

### Phase 4: Roadmap Prioritization

**Sort findings into actionable buckets.**

#### Impact/Effort Matrix

| | Low Effort | High Effort |
|---|---|---|
| **High Impact** | Quick Wins (do now) | Big Bets (plan carefully) |
| **Low Impact** | Easy Fixes (batch later) | Don't Do (cut) |

#### Prioritization Criteria

**Impact Score (1-5):**
- 5: Transforms core experience, affects all users
- 4: Major improvement to key flow
- 3: Noticeable improvement, affects many users
- 2: Nice polish, affects some users
- 1: Minor improvement, few users notice

**Effort Score (1-5):**
- 1: < 1 hour (config change, copy fix, simple CSS)
- 2: 1-4 hours (single component, simple feature)
- 3: 4-16 hours (multi-component, API changes)
- 4: 1-3 days (significant feature, schema changes)
- 5: 1+ weeks (architectural change, major feature)

#### Output Buckets

1. **Quick Wins** (Impact ≥ 3, Effort ≤ 2)
   - Do these this week
   - Should have 5-10 items
   - Each should be independently shippable

2. **Big Bets** (Impact ≥ 4, Effort ≥ 3)
   - Features that would transform the app
   - Require planning and design
   - Should have 3-5 items max

3. **Easy Fixes** (Impact ≤ 2, Effort ≤ 2)
   - Batch these for polish sprints
   - Good for new contributors
   - Don't let these block important work

4. **Nice to Have** (Impact ≤ 3, Effort ≥ 3)
   - Backlog fodder
   - Revisit quarterly
   - May never do, and that's okay

### Phase 5: Artifact Generation

**Produce actionable outputs.**

#### 1. Markdown Report

Write comprehensive report to: `docs/product-roast-YYYY-MM-DD.md`

Structure:
```markdown
# Product Roast + Vision Report: [App Name]
Generated: [Date]

## Executive Summary
[One paragraph: The app you have vs. the app you could have]

## Part 1: The Roast

### Critical Issues 🔥🔥🔥
[List with severity, location, impact]

### Moderate Issues 🔥🔥
[List]

### Minor Issues 🔥
[List]

## Part 2: The Vision

### [Feature Area 1]
- Current State:
- The Problem:
- The Vision:
- The Psychology:
- Implementation Sketch:

[Repeat for each feature area]

## Part 3: Prioritized Roadmap

### Quick Wins (This Week)
- [ ] Item 1
- [ ] Item 2
...

### Big Bets (Transform the App)
1. [Big Bet 1] - [Why it matters]
2. [Big Bet 2] - [Why it matters]
...

### Nice to Have (Backlog)
- Item 1
- Item 2
...

## Appendix
- Competitive Analysis Summary
- Psychology Principles Applied
- Technical Debt Inventory
```

#### 2. GitHub Issues

For each Quick Win and Big Bet, create GitHub issue:

```bash
gh issue create --title "[Severity] Issue Title" \
  --body "## Problem
[Description]

## Solution
[Proposed fix]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Priority
[Quick Win / Big Bet]

## Psychology Principle
[If applicable]
" \
  --label "enhancement,from-roast"
```

#### 3. Implementation Specs

For top 3 Quick Wins and top Big Bet, generate detailed spec:

```markdown
# Implementation Spec: [Feature Name]

## User Story
As a [user], I want [goal] so that [benefit].

## Current Behavior
[Screenshot or description]

## Desired Behavior
[Screenshot or description]

## Technical Approach
1. [Step 1]
2. [Step 2]
...

## Files to Modify
- `path/to/file.ts` - [What changes]
- `path/to/other.tsx` - [What changes]

## Acceptance Criteria
- [ ] [Testable criterion]
- [ ] [Testable criterion]

## Design Mockup
[If UI change, include mockup or link to figma]
```

#### 4. Design Mockups (Optional)

For visual improvements, invoke `frontend-design` skill to generate mockups.

### Phase 6: Implementation Mode

**After generating artifacts, ask:**

"Analysis complete. What would you like to implement?"

Options:
1. **Quick Wins Sprint** - Implement all quick wins now
2. **Specific Items** - Choose specific items to implement
3. **Big Bet Deep Dive** - Plan and implement top big bet
4. **Just the Analysis** - Done for now, will implement later

**For implementation:**
- Use `systematic-debugging` for bug fixes
- Use `frontend-design` for UI improvements
- Use `executing-plans` for larger features
- Mark items complete in GitHub as shipped

## Integration with Other Skills

**This skill uses:**
- `systematic-debugging` - For investigating root causes during roast
- `frontend-design` - For generating mockups and implementing UI fixes
- `executing-plans` - For implementing larger roadmap items
- `brainstorming` - For exploring vision alternatives

**Complementary skills:**
- `code-reviewer` - Run after implementing fixes
- `design-system-guardian` - Check UI consistency

## Key Principles

### For The Roast
- **Be specific**: "The button is ugly" ❌ → "The button uses bg-gray-400 which has insufficient contrast (3.2:1) and inconsistent border-radius (4px vs 8px elsewhere)" ✓
- **Include location**: Always reference file:line or screen/element
- **Quantify impact**: "Affects 100% of users on mobile" > "bad on mobile"
- **Severity matters**: Don't treat everything as critical

### For The Vision
- **Be concrete**: "Make it better" ❌ → "Add a GitHub-style contribution graph showing the last 365 days with color intensity based on completion %" ✓
- **Cite psychology**: Every vision should reference a principle
- **Show precedent**: "Like how Duolingo does X" grounds the idea
- **Sketch implementation**: Vision without path is fantasy

### For The Roadmap
- **Ruthlessly prioritize**: Can't do everything, pick the highest leverage
- **Quick wins build momentum**: Ship small things fast to prove progress
- **Big bets need commitment**: Don't start what you won't finish
- **Cut the nice-to-haves**: If it's not high impact, it's probably not worth doing

## Workshop Facilitation Tips

1. **Ask one question at a time** - Don't overwhelm
2. **Use multiple choice when possible** - Easier to answer
3. **Show your work** - Share findings as you go
4. **Pause for validation** - "Does this match your experience?"
5. **Be diplomatically brutal** - Honest but constructive
6. **Celebrate what's good** - Don't just roast, acknowledge wins

## Example Session

```
Claude: "I'm using the product-roast skill for a comprehensive product audit. Let me start by understanding the context. What app are we analyzing today?"

User: "GoalConnect - it's a habit tracker"

Claude: "Got it. Where's the codebase located?"

User: "/Users/me/GoalConnect"

Claude: "Thanks. Let me explore the codebase and understand the current state..."

[Claude explores codebase]

Claude: "I see this is a React + Express app with a mountaineering gamification theme. Before I dive into the roast, tell me - who are the primary users?"

[Continues workshop flow...]
```

---

**Remember**: The goal isn't to tear down - it's to reveal the path from "functional app" to "app people love." Every critique should point toward improvement. Every vision should be achievable. Every roadmap item should move the needle.
