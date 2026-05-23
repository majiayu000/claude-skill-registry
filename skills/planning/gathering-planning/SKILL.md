---
name: gathering-planning
description: The drum sounds. Bee and Badger gather for complete project planning. Use when you have ideas to capture AND want them organized on the project board in one flow.
---

# Gathering Planning 🌲🐝🦡

The drum echoes through the meadow. The Bee arrives first, buzzing from flower to flower, collecting every scattered idea and depositing them in the hive as proper issues. Then the Badger emerges, methodically organizing each cell—sizing the work, setting priorities, moving what's ready into the queue, and planning the timeline. When the gathering completes, chaos has become a roadmap.

## When to Summon

- Brain dump session that needs to become organized work
- "I have a bunch of ideas AND I want them prioritized"
- Sprint planning from scratch
- After a brainstorm that produced many TODOs
- When you want ideas → issues → organized backlog in one flow

---

## The Gathering

```
SUMMON → COLLECT → ORGANIZE → COMPLETE
   ↓         ↓          ↓          ↓
Receive   Bee         Badger     Roadmap
Ideas     Creates     Triages    Ready
          Issues      Board
```

### Animals Mobilized

1. **🐝 Bee** — Collect scattered ideas, create structured GitHub issues
2. **🦡 Badger** — Size, prioritize, move to Ready, set milestones/dates

---

### Phase 1: SUMMON

*The drum sounds. The meadow listens...*

Receive and parse the brain dump:

**Clarify the Session:**
- What ideas/TODOs do you want to capture?
- Any theme or component focus?
- Do you want to set up milestones today?

**Confirm:**
> "I'll mobilize a gathering for project planning:
>
> - 🐝 Bee will create issues from your ideas
> - 🦡 Badger will organize them on the project board
>
> Proceed with the gathering?"

---

### Phase 2: COLLECT (Bee)

*The bee buzzes from flower to flower...*

Execute bee-collect workflow:

**🐝 BEE — COLLECT**

```
Input: Raw brain dump, TODOs, ideas

Process:
1. BUZZ — Parse into discrete items
2. INSPECT — Explore codebase for context
3. CHECK — Verify no duplicates exist
4. DEPOSIT — Create issues with full context

Output:
- X new issues created
- Y duplicates skipped
- Each issue has:
  - Clear title (imperative mood)
  - Acceptance criteria
  - Component labels
  - Technical context
```

**Handoff to Badger:**
> "🐝 Collection complete. Created [X] new issues.
>
> Handing off to 🦡 Badger for organization..."

---

### Phase 3: ORGANIZE (Badger)

*The badger emerges, ready to organize the burrow...*

Execute badger-triage workflow:

**🦡 BADGER — TRIAGE**

```
Input: Newly created issues (plus any existing untriaged)

Process:
1. DIG — Survey issues needing attention
2. SORT — Group into batches by theme
3. DISCUSS — Interactive sizing/prioritization (5-10 at a time)
4. TIMELINE — Set milestones and target dates (optional)
5. PLACE — Update GitHub project fields

Output:
- All issues sized (XS/S/M/L/XL)
- All issues prioritized (First Focus/Next Up/In Time/Far Off)
- Ready items moved from Backlog
- Milestones assigned (if requested)
- Target dates set (if requested)
```

**Discussion Flow:**

The badger will present batches and ask:
- "These 5 issues need sizing. Here's my guess based on the content..."
- "What priority should these have?"
- "Should any move from Backlog to Ready?"
- "Want to assign these to a milestone?"

---

### Phase 4: COMPLETE

*The gathering ends. A roadmap emerges...*

**Completion Report:**

```markdown
## 🌲 GATHERING PLANNING COMPLETE

### Session Summary

**🐝 Bee Collected:**
- [X] issues created from brain dump
- [Y] duplicates skipped
- Components: [list of labels used]

**🦡 Badger Organized:**

| Metric | Count |
|--------|-------|
| Sized | [X] |
| Prioritized | [X] |
| Moved to Ready | [X] |
| Target dates set | [X] |

### By Priority

| Priority | Issues |
|----------|--------|
| First Focus | #123, #124, #125 |
| Next Up | #126, #127 |
| In Time | [count] issues |
| Far Off | [count] issues |

### Milestones

| Milestone | Issues | Due |
|-----------|--------|-----|
| [Name] | [count] | [date] |

### What's Ready to Work On

These issues are sized, prioritized, and in the Ready column:

1. #123 — [Title] (XS, First Focus)
2. #124 — [Title] (S, First Focus)
3. #125 — [Title] (M, First Focus)

*From chaos, order. From ideas, a roadmap.* 🌲
```

---

## Example Gathering

**User:** "/gathering-planning ok here's my brain dump: fix the broken avatar upload, add dark mode to settings, implement the new pricing tiers we discussed, eventually add webhooks for integrations, the footer needs updating, and we should probably add rate limiting to the API"

**Gathering execution:**

1. 🌲 **SUMMON** — "Mobilizing for project planning. I see 6 items to process."

2. 🐝 **COLLECT** —
   - "Buzzing through the ideas..."
   - "Checking for duplicates... 'dark mode' exists as #498, skipping"
   - Created: #531 (avatar bug), #532 (pricing), #533 (webhooks), #534 (footer), #535 (rate limiting)
   - "5 issues deposited in the hive"

3. 🦡 **ORGANIZE** —
   - "Digging into the new issues..."
   - "Sizing: avatar bug (XS), pricing (L), webhooks (XL), footer (S), rate limiting (M)?"
   - User confirms with one adjustment
   - "Priority: avatar bug is First Focus (it's broken). Pricing is Next Up. Rest In Time?"
   - User moves rate limiting to Next Up
   - "Move avatar bug and rate limiting to Ready?"
   - User confirms
   - "Want to set target dates or create a milestone?"
   - User creates "February Sprint" milestone

4. 🌲 **COMPLETE** —
   ```
   Bee: 5 issues created, 1 duplicate skipped
   Badger: All sized, prioritized, 2 moved to Ready
   Milestone: February Sprint (2 issues, due Feb 28)

   Ready to work on:
   - #531 — Fix avatar upload (XS, First Focus)
   - #535 — Add API rate limiting (M, Next Up)
   ```

---

## Gathering Rules

### Flow
Bee always runs first. Badger organizes what Bee collected (plus any existing untriaged issues).

### Conversation
Both animals are interactive. The bee asks for clarification on vague items. The badger discusses sizing and priority in batches.

### Scope
If the brain dump is massive (20+ items), the bee may ask to split into multiple sessions.

### Code Safety
Neither animal edits code. This gathering is purely for project organization.

---

## When to Use This vs. Individual Animals

| Situation | Use |
|-----------|-----|
| Just have ideas to capture | 🐝 `/bee-collect` |
| Just need to organize existing issues | 🦡 `/badger-triage` |
| Have ideas AND want them organized | 🌲 `/gathering-planning` |
| Weekly planning session | 🌲 `/gathering-planning` |
| Quick backlog grooming | 🦡 `/badger-triage` |

---

*From scattered thoughts to organized work. The forest knows the way.* 🌲
