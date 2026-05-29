---
name: daily-note
description: Create or update today's private journal entry. Use when asked to "daily note", "journal", "log today", "morning pages", or "capture thoughts".
allowed-tools: Read, Write, Edit, Glob, Grep, AskUserQuestion
---

# Daily Note

Create or update today's private journal entry with guided prompts, habit tracking, and metrics.

## Location

All private notes live in `content/private/` with flat structure (no subfolders).

## Personal Config

**IMPORTANT:** Read `.claude/skills/daily-note/habits-config.md` for Alexander's specific habits and metric targets. Use those instead of the generic defaults.

## Date Format

- Daily notes: `YYYY-MM-DD.md` (ISO 8601)
- Example: `2024-01-13.md`

---

## Phase 1: Check for Existing Note

Get today's date and check if a note exists:

```text
Glob: content/private/{today YYYY-MM-DD}.md
```

**If exists:** Read the file and proceed to Phase 4 (Update Mode).
**If missing:** Proceed to Phase 2 (Mode Selection).

---

## Phase 2: Mode Selection

Ask user what kind of entry they want:

```yaml
question: "What would you like to do?"
header: "Mode"
options:
  - label: "Quick capture"
    description: "Just log something quickly (1 min)"
  - label: "Morning check-in"
    description: "Start your day with intentions + habits"
  - label: "Evening reflection"
    description: "Review your day + track metrics"
  - label: "Full journal"
    description: "Complete daily entry with all sections"
```

Branch based on selection:
- **Quick capture** → Phase 3A
- **Morning check-in** → Phase 3B
- **Evening reflection** → Phase 3C
- **Full journal** → Phase 3D

---

## Phase 3A: Quick Capture

Simple and fast - just capture a thought:

```yaml
question: "What do you want to capture?"
header: "Capture"
options:
  - label: "A thought"
    description: "Something on your mind"
  - label: "A win"
    description: "Something good that happened"
  - label: "A learning"
    description: "Something you discovered"
  - label: "A todo"
    description: "Something to remember"
```

After user provides content, append to the appropriate section in the daily note.

---

## Phase 3B: Morning Check-in

### Step 1: How are you feeling?

```yaml
question: "How are you feeling this morning?"
header: "Mood"
options:
  - label: "Great 😊"
    description: "Energized and ready"
  - label: "Good 🙂"
    description: "Steady and calm"
  - label: "Okay 😐"
    description: "Neutral"
  - label: "Low 😔"
    description: "Tired or down"
```

### Step 2: Track habits

```yaml
question: "Which habits did you complete?"
header: "Habits"
multiSelect: true
options:
  - label: "Morning walk"
    description: "Morning movement"
  - label: "Read (30 min)"
    description: "Books or articles"
  - label: "Workout"
    description: "Strength or cardio"
  - label: "Deep work (45 min)"
    description: "Focused work block"
```

### Step 3: Intentions

Ask: "What's your main focus for today?" (free text input)

### Step 4: Generate morning entry

Create/update the daily note with morning sections filled in.

---

## Phase 3C: Evening Reflection

### Step 1: How was your day?

```yaml
question: "How did today go overall?"
header: "Day Rating"
options:
  - label: "Excellent ⭐⭐⭐"
    description: "Great day, accomplished a lot"
  - label: "Good ⭐⭐"
    description: "Solid day, decent progress"
  - label: "Mixed ⭐"
    description: "Some good, some challenges"
  - label: "Tough"
    description: "Difficult day"
```

### Step 2: Track daily metrics

```yaml
question: "Which metrics to log?"
header: "Metrics"
multiSelect: true
options:
  - label: "Steps"
    description: "Target: 7000+"
  - label: "Calories"
    description: "Target: < 2800"
  - label: "Protein"
    description: "Target: 180g+"
  - label: "Eating window"
    description: "Nothing after 20:00"
```

If metrics selected, ask for values:
- Steps: "How many steps today?"
- Calories: "Total calories?"
- Protein: "Total protein (g)?"
- Eating window: "Did you respect the eating window (nothing after 20:00)?"

### Step 3: Track habits (if not done in morning)

```yaml
question: "Which habits did you complete today?"
header: "Habits"
multiSelect: true
options:
  - label: "Morning walk"
    description: "Morning movement"
  - label: "Read (30 min)"
    description: "Books or articles"
  - label: "Workout"
    description: "Strength or cardio"
  - label: "Deep work (45 min)"
    description: "Focused work block"
```

### Step 4: Wins and learnings

Ask: "What's one win from today?" (free text)
Ask: "Any learnings or insights?" (free text, optional)

### Step 5: Gratitude

```yaml
question: "Want to capture gratitude?"
header: "Gratitude"
options:
  - label: "Yes"
    description: "Note what you're grateful for"
  - label: "Skip"
    description: "Not today"
```

If yes, ask: "What are you grateful for today?"

### Step 6: Generate evening entry

Update the daily note with evening sections filled in.

---

## Phase 3D: Full Journal

Run both morning and evening flows sequentially, plus:

### Additional: Tomorrow

```yaml
question: "Want to plan tomorrow?"
header: "Tomorrow"
options:
  - label: "Yes"
    description: "Set intentions for tomorrow"
  - label: "Skip"
    description: "Plan later"
```

If yes, ask: "What's your main priority for tomorrow?"

### Additional: Links

Search for public notes created/modified today and suggest wiki-links:

```text
Grep pattern: "date: {today}" glob: "content/*.md"
```

---

## Phase 4: Update Mode (Existing Note)

When a daily note already exists:

### 4.1 Display Current State

Read the file and show:
- Current mood and ratings
- Habits already tracked
- Metrics logged
- Sections with content

### 4.2 Choose What to Update

```yaml
question: "What would you like to add?"
header: "Update"
options:
  - label: "Quick thought"
    description: "Add something to captures"
  - label: "Track habits"
    description: "Log completed habits"
  - label: "Log metrics"
    description: "Add weight, sleep, etc."
  - label: "Evening review"
    description: "Complete the day's reflection"
```

Proceed to appropriate phase based on selection.

---

## Daily Note Template

Full template with all possible sections:

```markdown
---
title: "YYYY-MM-DD"
type: daily
date: YYYY-MM-DD
mood: good | great | okay | low
dayRating: 1 | 2 | 3
private: true
---

## Habits

- [ ] Morning walk
- [ ] Read (30 min)
- [ ] Workout
- [ ] Deep work (45 min)

## Metrics

| Metric | Value | Target |
|--------|-------|--------|
| Steps | | 7000+ |
| Calories | | < 2800 |
| Protein | | 180g+ |
| Eating window | | ✓ |

## Morning Intentions

{what to focus on today}

## Captures

- {quick thoughts throughout the day}

## Wins

- {good things that happened}

## Learnings

- {insights and discoveries}

## Gratitude

- {what you're thankful for}

## Tomorrow

- {priorities for the next day}

## Links Captured

- [[public-note-from-today]]
```

---

## Habits Reference

Alexander's daily habits:

| Habit | Target |
|-------|--------|
| Morning walk | Daily |
| Read | 30 min |
| Workout | Daily |
| Deep work | 45 min |

---

## Metrics Reference

Alexander's daily metrics:

| Metric | Target | Format |
|--------|--------|--------|
| Steps | 7000+ | number |
| Calories | < 2800 | number |
| Protein | 180g+ | grams |
| Eating window | Nothing after 20:00 | ✓ or ✗ |

---

## Quality Checklist

Before saving:
- [ ] Filename matches `YYYY-MM-DD.md` format
- [ ] Frontmatter has `type: daily` and `private: true`
- [ ] Date in title and frontmatter match
- [ ] At least one section has content
- [ ] Habits use checkbox format `- [x]` or `- [ ]`
- [ ] Metrics table is properly formatted
- [ ] Wiki-links use correct `[[slug]]` format

---

## Tips for Good Journaling

- **Consistency > Length**: A few bullet points daily beats long entries occasionally
- **Capture immediately**: Log wins and learnings when they happen
- **Be honest**: Track actual habits, not aspirational ones
- **Review weekly**: Use `/weekly-review` to find patterns

---

## Error Recovery

| Error | Recovery |
|-------|----------|
| User wants different date | Allow specifying date, adjust filename |
| Wants to customize habits | Accept custom habit names |
| Metric format unclear | Accept any format, don't enforce |
| Section too long | Accept without truncation |
| Wiki-link target doesn't exist | Warn but allow |
