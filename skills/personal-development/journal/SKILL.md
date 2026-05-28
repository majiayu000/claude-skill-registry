---
name: journal
description: Toggle journaling or start a journal entry (morning/evening/weekly)
---

## Purpose

Toggle journaling on/off, or start a journal entry.

## Usage

- `/journal on` — Enable daily journaling prompts
- `/journal off` — Disable journaling (daily planning works without it)
- `/journal` — Start today's journal (morning or evening based on time)
- `/journal morning` — Start morning journal
- `/journal evening` — Start evening journal
- `/journal week` — Start weekly journal

---

## Behavior

### `/journal on`

1. Update `System/user-profile.yaml` journaling section to enable all types (morning: true, evening: true, weekly: true)
2. Create `00-Inbox/Journals/` folder if it doesn't exist
3. Confirm: "Journaling enabled. I'll prompt you for morning reflection before daily planning, and offer evening reflection at end of day. Your journals will be in `00-Inbox/Journals/`."

### `/journal off`

1. Update `System/user-profile.yaml` journaling section to disable all types (morning: false, evening: false, weekly: false)
2. Confirm: "Journaling disabled. Daily planning will work normally without journal prompts. Your existing journals are preserved in `00-Inbox/Journals/`."
3. Do NOT delete existing journal entries

### `/journal` (no argument)

Check current time:
- Before 12pm → Start morning journal
- After 12pm → Start evening journal

### `/journal morning`

1. Check if today's morning journal exists
   - If yes: Open it for review/editing
   - If no: Create from template, guide user through prompts
2. After completion, offer to generate daily plan: "Ready to plan your day? I can create your Daily Note now."

### `/journal evening`

1. Check if today's evening journal exists
   - If yes: Open it for review/editing
   - If no: Create from template
2. Pull in morning journal intention for reflection
3. Guide user through evening prompts
4. After completion: "Day closed. See you tomorrow morning."

### `/journal week`

1. Check if this week's journal exists
   - If yes: Open for review/editing
   - If no: Create from template
2. Link to this week's daily journals
3. Summarize patterns from daily entries (if available)
4. Guide through weekly reflection
5. After completion, surface insights: "Based on your week, you might want to focus on {{pattern}} next week."

---

## Daily Planning Integration

When journaling is enabled and user asks to plan their day:

1. **Check for morning journal**
   - If missing: "Let's start with a quick morning reflection first. It'll take 5 minutes and helps you plan with more intention."
   - Guide through morning journal
   - Then generate daily plan

2. **Morning journal informs daily plan**
   - "ONE thing that matters most" from journal → First priority in daily plan
   - "What might derail me" → Blocked time or warnings in plan
   - Energy/mood → Adjust intensity of planned tasks

---

## Folder Structure

When journaling is enabled:

```
00-Inbox/
└── Journals/
    ├── 2024/
    │   ├── 01-January/
    │   │   ├── Morning/
    │   │   │   ├── 2024-01-15-morning.md
    │   │   │   └── 2024-01-16-morning.md
    │   │   ├── Evening/
    │   │   │   ├── 2024-01-15-evening.md
    │   │   │   └── 2024-01-16-evening.md
    │   │   └── Weekly/
    │   │       └── 2024-W03.md
```

---

## Why Journaling Matters

When explaining to users during onboarding or `/journal on`:

> **Morning journaling** (5 min) helps you start intentionally instead of reactively. You'll notice what's on your mind, set a clear focus, and anticipate obstacles before they derail you.
>
> **Evening journaling** (5 min) closes open loops, captures wins and lessons, and prevents the day from blurring into the next. What you notice, you can change.
>
> **Weekly journaling** (15 min) reveals patterns you can't see day-to-day. Energy cycles, recurring frustrations, what's actually getting your time vs. what matters.
>
> Research shows: Regular reflection improves decision-making, reduces stress, and increases goal achievement. It's not about writing perfectly — it's about paying attention to your own experience.

---

## Configuration

Journaling preferences are stored in `System/user-profile.yaml` under the `journaling` section:

```yaml
journaling:
  morning: true   # Enable morning journal prompts
  evening: true   # Enable evening journal prompts
  weekly: true    # Enable weekly journal prompts
```

Check this file to determine which journal types are enabled for the user.

---

## Prompting Style

When guiding journal entries:
- Ask one question at a time
- Don't overwhelm — templates are comprehensive, but conversation can be lighter
- Accept short answers
- Reflect back patterns when you notice them
- Be warm but not saccharine
- Respect if user wants to skip sections

Example morning flow:
```
Good morning. Before we plan your day, let's take 5 minutes to check in.

How are you arriving today? Rate your sleep, energy, and mood 1-5.

[User responds]

Got it. What's on your mind right now? Just free write whatever's there.

[User responds]

Thanks. Now the important one: If you could only accomplish ONE thing today, what would it be?

[User responds]

Why does that matter?

[User responds]

Great. One more: What might get in the way today, and how will you handle it?

[User responds]

Perfect. Your morning journal is saved. Ready to build your daily plan around that focus?
```
