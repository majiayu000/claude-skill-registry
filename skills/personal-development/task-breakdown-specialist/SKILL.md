---
name: Task Breakdown Specialist
description: Break large tasks into ADHD-friendly micro-tasks that minimize activation energy and maximize momentum. Use when feeling overwhelmed, can't start a task, or need to make progress visible. Optimized for ADHD developers with 15-minute task chunking and dopamine-driven ordering.
version: 1.0.0
---

# Task Breakdown Specialist

**Lower activation energy. Build momentum. Make progress visible.**

## Core Principle

ADHD brains struggle with large, ambiguous tasks due to high activation energy. The solution: Break everything into tiny, achievable micro-tasks that provide frequent dopamine hits and visible progress.

**Key Insight:** Starting is the hardest part. Make starting ridiculously easy.

---

## The ADHD Task Problem

### Problem 1: Activation Energy

**Issue:** "Build authentication system" feels overwhelming
**Result:** Procrastination, anxiety, avoidance

### Problem 2: Time Blindness

**Issue:** Can't estimate how long tasks take
**Result:** Unrealistic plans, missed deadlines, frustration

### Problem 3: Working Memory

**Issue:** Can't hold large task in mind while working
**Result:** Losing track of what you're doing, constant re-reading

### Problem 4: Dopamine Deficit

**Issue:** Big tasks provide no intermediate rewards
**Result:** Motivation loss, task abandonment

---

## Phase 1: Quick Win Strategy

### Start with 2-Minute Tasks

**Why:** Zero activation energy, instant dopamine, builds momentum

```markdown
❌ Bad Task: "Build user authentication"

- Feels huge (overwhelm)
- Unclear start point (paralysis)
- No quick wins (no dopamine)

✅ Good Breakdown:

Quick Wins (Build Momentum) ⚡

1. [ ] Create /auth folder (30 sec) 🟢
2. [ ] Create auth.ts file (30 sec) 🟢
3. [ ] Install bcrypt package (1 min) 🟢

WHY START HERE:

- Combined: 2 minutes total
- Zero thinking required
- 3 quick dopamine hits
- Momentum established

THEN move to real work...
```

### The 2-5-15-30 Pattern

Break tasks into time categories:

**2-minute tasks (🟢)** - Setup, scaffolding, installs
**5-minute tasks (🟢)** - Simple functions, basic HTML
**15-minute tasks (🟡)** - Core logic, API calls
**30-minute tasks (🟡)** - Complex features, integration

**Rule:** Always start with 2-minute tasks!

---

## Phase 2: The Breakdown Formula

### Step 1: Capture the Big Task

Write down the overwhelming task:

```markdown
Big Task: Build user dashboard with analytics
```

### Step 2: Ask Clarifying Questions

```markdown
Questions:

- What's the absolute minimum? (MVP)
- What would "done" look like?
- What can I skip for now?
- What's P0 vs P1 vs P2?
```

### Step 3: Identify Micro-Tasks

Use this template:

```markdown
## Big Task: Build User Dashboard

### P0 (Must Have - MVP)

- Dashboard page exists
- Shows user name
- Shows one metric (login count)

### P1 (Should Have - Next)

- Charts and graphs
- Multiple metrics
- Time range selector

### P2 (Nice to Have - Later)

- Export data
- Custom widgets
- Real-time updates
```

### Step 4: Break P0 into Micro-Tasks

```markdown
## Building P0 Dashboard

Phase 1: Quick Wins (Momentum) ⚡

1. [ ] Create dashboard.tsx file (30 sec) 🟢
2. [ ] Add to navigation menu (1 min) 🟢
3. [ ] Add "Dashboard" heading (30 sec) 🟢
       Total: 2 minutes

Phase 2: Core Structure 🏗️ 4. [ ] Create dashboard layout (5 min) 🟢 5. [ ] Add user name display (5 min) 🟢 6. [ ] Style with Tailwind (10 min) 🟡
Total: 20 minutes

Phase 3: Data Integration 📊 7. [ ] Fetch user data from API (15 min) 🟡 8. [ ] Display login count (10 min) 🟡 9. [ ] Add loading state (5 min) 🟢
Total: 30 minutes

Phase 4: Polish & Ship ✨ 10. [ ] Handle error states (10 min) 🟡 11. [ ] Test all paths (10 min) 🟡 12. [ ] Deploy (5 min) 🟢
Total: 25 minutes

Grand Total: ~75 minutes
With ADHD tax (1.5x): ~110 minutes (2 hours)
```

---

## Phase 3: Task Sizing with ADHD Tax

### Standard Time Estimates Are Lies

Neurotypical estimate × 1.5-2 = ADHD estimate

**Why:**

- Task switching overhead
- Distraction recovery time
- Setup/teardown time
- "Where was I?" moments
- Inevitable rabbit holes

### ADHD Time Multipliers

```markdown
Simple task (5 min estimated):
→ ADHD reality: 7-10 min (1.5x)

Medium task (30 min estimated):
→ ADHD reality: 45-60 min (1.5-2x)

Complex task (2 hours estimated):
→ ADHD reality: 3-4 hours (2x)

New/Unknown task (?? estimated):
→ ADHD reality: 3x whatever you think
```

### Honest Task Sizing

```markdown
## Feature: Add password reset

Traditional estimate: 1 hour

ADHD-honest estimate:

- Setup email service (5 min → 10 min)
- Generate reset token (10 min → 15 min)
- Build reset form (20 min → 30 min)
- Handle token validation (15 min → 25 min)
- Test flows (10 min → 20 min)

Subtotal: 60 min → 100 min

- Buffer for interruptions: +20 min
- Debugging time: +30 min

Real estimate: 2.5 hours

👍 Better to overestimate and finish early (dopamine!)
👎 Than underestimate and feel like failure
```

---

## Phase 4: Momentum-Based Ordering

### Dopamine-Optimized Task Sequence

**Don't do tasks in logical order. Do them in motivation order.**

```markdown
❌ Logical Order (ADHD-hostile):

1. Plan architecture (hard, no dopamine)
2. Set up database (boring, no dopamine)
3. Build API (complex, delayed dopamine)
4. Build UI (fun but blocked by above)

✅ Momentum Order (ADHD-friendly):

1. Build UI mockup (fun, instant visual) 🎨 Dopamine!
2. Add fake data (easy, looks real) 🎯 Dopamine!
3. Hook up API (has context now) 💪 Dopamine!
4. Set up database (motivated now) ✅ Dopamine!
5. Refine architecture (understand it now) 🚀 Done!

Why this works:

- Starts with fun (low activation energy)
- Provides instant feedback (dopamine)
- Builds understanding (easier to do hard parts)
- Maintains momentum (no dead zones)
```

### The Quick Win Sandwich

**Pattern:** Easy → Hard → Easy

```markdown
Session Plan (2 hours):

00:00 - 00:10: Quick wins (3 easy tasks)
→ Builds momentum
→ Establishes "I'm productive" mindset

00:10 - 01:30: Hard task (focus required)
→ You have momentum now
→ Feel accomplished from quick wins

01:30 - 02:00: Easy task (cool down)
→ End on high note
→ Easy to resume tomorrow
```

---

## Phase 5: Progress Visualization

### Make Progress Visible

ADHD brains need to SEE progress for dopamine release.

#### Progress Bars

```markdown
## Feature: User Authentication

Progress: ████████░░ 80%

✅ Phase 1: Setup (20%)
✅ Phase 2: Login (30%)
✅ Phase 3: Signup (30%)
🔄 Phase 4: Reset (20%) ← YOU ARE HERE

Next: Password reset form (15 min)
```

#### Checklist with Time Tracking

```markdown
## Today's Tasks

🔥 Streak: 3 days
⏱️ Focus time: 45 min

Morning Session (2 hours budgeted):

- [x] Fix login bug (15 min) ✅ 12 min (faster!)
- [x] Add loading spinner (5 min) ✅ 7 min
- [x] Update tests (10 min) ✅ 15 min
- [ ] Code review (20 min) ← CURRENT
- [ ] Deploy fix (10 min)

Progress: 3/5 tasks (60%)
Time spent: 34 min / 120 min
Remaining: 30 min of work

💪 You're crushing it!
```

#### Commit-Based Progress

```markdown
## This Week's Progress

Mon: ✅✅✅✅✅ (5 commits)
Tue: ✅✅✅ (3 commits)
Wed: ✅✅✅✅✅✅✅ (7 commits) 🔥 Best day!
Thu: ✅✅✅✅ (4 commits)
Fri: ✅ (1 commit) ← TODAY

Total: 20 commits this week
Goal: 15 commits (exceeded! 🎉)

Keep the streak alive!
```

---

## Phase 6: Task Breakdown Patterns

### Pattern 1: Feature Breakdown

```markdown
# Feature: Add dark mode

## Step 1: Identify Components

What needs to change?

- Colors
- Component styles
- Toggle button
- Persistence

## Step 2: Break Down Each

### Colors (30 min total)

- [ ] Define dark color palette (5 min) 🟢
- [ ] Add CSS variables (10 min) 🟡
- [ ] Test contrast ratios (15 min) 🟡

### Component Styles (45 min total)

- [ ] Update Button component (10 min) 🟡
- [ ] Update Card component (10 min) 🟡
- [ ] Update Input component (10 min) 🟡
- [ ] Update Header component (15 min) 🟡

### Toggle Button (20 min total)

- [ ] Create ThemeToggle component (15 min) 🟡
- [ ] Add to header (5 min) 🟢

### Persistence (15 min total)

- [ ] Save preference to localStorage (10 min) 🟡
- [ ] Load on app start (5 min) 🟢

Total: 110 min (2 hours realistic)
```

### Pattern 2: Bug Fix Breakdown

```markdown
# Bug: Users can't reset password

## Step 1: Reproduce (10 min)

- [ ] Try reset flow locally (5 min) 🟢
- [ ] Check error logs (5 min) 🟢

## Step 2: Investigate (20 min)

- [ ] Find reset-password.ts file (1 min) 🟢
- [ ] Read through code (5 min) 🟢
- [ ] Identify issue (token expiry) (10 min) 🟡
- [ ] Confirm root cause (4 min) 🟢

## Step 3: Fix (30 min)

- [ ] Update token expiry logic (20 min) 🟡
- [ ] Add better error message (10 min) 🟡

## Step 4: Test (15 min)

- [ ] Test locally (10 min) 🟡
- [ ] Test on staging (5 min) 🟢

## Step 5: Deploy (10 min)

- [ ] Create PR (3 min) 🟢
- [ ] Deploy to production (7 min) 🟢

Total: 85 min (1.5 hours)
```

### Pattern 3: Learning Task Breakdown

```markdown
# Learn: Next.js App Router

❌ Bad: "Learn Next.js App Router" (too vague)

✅ Good Breakdown:

## Phase 1: Overview (30 min)

- [ ] Watch official intro video (15 min) 🟢
- [ ] Read "Getting Started" docs (15 min) 🟢

## Phase 2: Hands-On (1 hour)

- [ ] Create new Next.js project (5 min) 🟢
- [ ] Build simple page (15 min) 🟡
- [ ] Add dynamic route (20 min) 🟡
- [ ] Try server components (20 min) 🟡

## Phase 3: Apply (2 hours)

- [ ] Migrate one page in my project (30 min) 🟡
- [ ] Test and debug (30 min) 🟡
- [ ] Migrate second page (30 min) 🟡
- [ ] Document learnings (30 min) 🟡

Total: 3.5 hours over 2 days
Day 1: Phase 1 + 2 (1.5 hours)
Day 2: Phase 3 (2 hours)
```

---

## Phase 7: Anti-Patterns (What NOT to Do)

### ❌ Anti-Pattern 1: Perfectionist Breakdown

```markdown
Bad:

- [ ] Research best authentication library (no time limit)
- [ ] Compare 10 different approaches (rabbit hole)
- [ ] Design perfect architecture (never starts)

Good:

- [ ] Choose auth library (10 min, use NextAuth)
- [ ] Follow quickstart guide (30 min)
- [ ] Ship MVP, iterate later
```

### ❌ Anti-Pattern 2: Too Granular

```markdown
Bad:

- [ ] Open VS Code (10 sec)
- [ ] Navigate to file (10 sec)
- [ ] Type 'import' (5 sec)

This is ridiculous. You'll spend more time reading the list.

Good:

- [ ] Add imports to auth.ts (2 min)
```

### ❌ Anti-Pattern 3: All Hard Tasks

```markdown
Bad:

- [ ] Refactor authentication (2 hours)
- [ ] Optimize database queries (3 hours)
- [ ] Fix critical bug (2 hours)

No quick wins = No momentum = No dopamine = Procrastination

Good:

- [ ] Update README (5 min) 🟢 ← Start here!
- [ ] Refactor one function (30 min) 🟡
- [ ] Take break (5 min)
- [ ] Fix critical bug (2 hours) 🟡
```

### ❌ Anti-Pattern 4: Vague Tasks

```markdown
Bad:

- [ ] Work on dashboard
- [ ] Fix bugs
- [ ] Improve performance

What does "done" mean? ADHD brain will wander.

Good:

- [ ] Add user stats to dashboard (15 min)
- [ ] Fix login timeout bug (#123) (20 min)
- [ ] Reduce API response time to < 200ms (1 hour)
```

---

## Phase 8: Emergency Task Breakdown

### When You're Stuck RIGHT NOW

**5-Minute Breakdown Exercise:**

1. **Write the overwhelming task:**

   ```
   _________________________________
   ```

2. **What's the FIRST tiny action?** (< 2 min)

   ```
   _________________________________
   ```

3. **Do ONLY that action. Nothing else.**

4. **Dopamine hit! Now write next action:**

   ```
   _________________________________
   ```

5. **Repeat.**

**Example:**

```
1. Overwhelming: "Build entire checkout flow"
2. First tiny action: "Create checkout.tsx file"
3. [DO IT NOW - 30 seconds]
4. ✅ Done! Dopamine!
5. Next action: "Add basic form HTML"
6. [DO IT - 5 min]
7. Keep going...
```

---

## Checklist: Good Task Breakdown

Use this to validate your task breakdown:

- [ ] Tasks are 15 minutes or less
- [ ] Starts with 2-3 "quick win" tasks (2-5 min)
- [ ] Each task has clear "done" criteria
- [ ] Time estimates include ADHD tax (1.5x)
- [ ] Uses progress visualization (%, bars, checklists)
- [ ] Easy tasks mixed with hard tasks (momentum maintenance)
- [ ] No vague tasks ("work on", "improve", "fix")
- [ ] Total time estimated honestly (not wishful thinking)
- [ ] First task has near-zero activation energy

---

## Tools & Templates

### Daily Task Template

```markdown
# Today: [Date]

## ONE Main Goal

[The ONE thing that matters today]

## Morning Session (2 hours)

Quick Wins:

- [ ] Task 1 (2 min) 🟢
- [ ] Task 2 (5 min) 🟢

Main Work:

- [ ] Task 3 (30 min) 🟡
- [ ] Task 4 (45 min) 🟡

Cool Down:

- [ ] Task 5 (10 min) 🟢

## Afternoon Session (2 hours)

[Same pattern]

## Wins Log

[What you completed - for dopamine]
```

### Project Breakdown Template

```markdown
# Project: [Name]

## MVP Definition

What's the absolute minimum to ship?

## Phases

### Phase 1: Foundation (Quick wins)

- [ ] Tasks...

### Phase 2: Core Features

- [ ] Tasks...

### Phase 3: Polish

- [ ] Tasks...

## Time Estimate

Naive: X hours
ADHD-realistic: Y hours (1.5-2x)
```

---

## Related Skills

- **context-preserver** - Save state between tasks
- **focus-session-manager** - Manage work sessions
- **completion-coach** - Finish what you start
- **adhd-workflow-architect** - Design ADHD-friendly workflows

---

## Success Metrics

You're using this skill well when:

- ✅ Starting tasks feels easy (low activation energy)
- ✅ You see progress every 15 minutes
- ✅ Time estimates are realistic
- ✅ You finish tasks instead of abandoning them
- ✅ You feel in control (not overwhelmed)

---

**Break it down. Start small. Build momentum. Ship things.** 💪
