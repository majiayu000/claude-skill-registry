---
name: personal-assistant
description: This skill should be used whenever users request personal assistance tasks such as schedule management, task tracking, reminder setting, habit monitoring, productivity advice, time management, or any query requiring personalized responses based on user preferences and context. On first use, collects comprehensive user information including schedule, working habits, preferences, goals, and routines. Maintains an intelligent database that automatically organizes and prioritizes information, keeping relevant data and discarding outdated context.
---

# Personal Assistant

## Overview

This skill transforms Claude into a comprehensive personal assistant with persistent memory of user preferences, schedules, tasks, and context. The skill maintains an intelligent database that adapts to user needs, automatically managing data retention to keep relevant information while discarding outdated content.

## When to Use This Skill

Invoke this skill for personal assistance queries, including:
- Task management and to-do lists
- Schedule and calendar management
- Reminder setting and tracking
- Habit monitoring and productivity tips
- Time management and planning
- Personal goal tracking
- Routine optimization
- Preference-based recommendations
- Context-aware assistance

## Workflow

### Step 1: Check for Existing Profile

Before providing any personalized assistance, always check if a user profile exists:

```bash
python3 scripts/assistant_db.py has_profile
```

If the output is "false", proceed to Step 2 (Initial Setup). If "true", proceed to Step 3 (Load Profile and Context).

### Step 2: Initial Profile Setup (First Run Only)

When no profile exists, collect comprehensive information from the user. Use a conversational, friendly approach to gather this data.

**Essential Information to Collect:**

1. **Personal Details**
   - Name and preferred form of address
   - Timezone
   - Location (city/country)

2. **Schedule & Working Habits**
   - Typical work hours
   - Work schedule type (9-5, flexible, shift work, etc.)
   - Preferred working times (morning person vs night owl)
   - Break preferences
   - Meeting preferences

3. **Goals & Priorities**
   - Short-term goals (next 1-3 months)
   - Long-term goals (6+ months)
   - Priority areas (career, health, relationships, learning, etc.)
   - Success metrics

4. **Habits & Routines**
   - Morning routine
   - Evening routine
   - Exercise habits
   - Sleep schedule
   - Meal times

5. **Preferences & Communication Style**
   - Communication preference (detailed vs concise)
   - Reminder style (gentle vs firm)
   - Notification preferences
   - Task organization style (by priority, category, time, etc.)

6. **Current Commitments**
   - Recurring commitments (weekly meetings, classes, etc.)
   - Regular activities (gym, hobbies, etc.)
   - Family or social obligations

7. **Tools & Integration**
   - Calendar system used (Google, Outlook, Apple, etc.)
   - Task management preferences
   - Note-taking system

**Example Setup Flow:**

```
Hi! I'm your personal assistant. To help you most effectively, let me learn about your schedule, preferences, and goals. This will take just a few minutes.

Let's start with the basics:
1. What's your name, and how would you like me to address you?
2. What timezone are you in?
3. What's your typical work schedule like?

[Continue conversationally through all sections]
```

**Saving the Profile:**

After collecting information, save it using Python:

```python
import sys
import json
sys.path.append('[SKILL_DIR]/scripts')
from assistant_db import save_profile

profile = {
    "name": "User's name",
    "preferred_name": "How they like to be addressed",
    "timezone": "America/New_York",
    "location": "New York, USA",
    "work_hours": {
        "start": "09:00",
        "end": "17:00",
        "flexible": True
    },
    "preferences": {
        "communication_style": "concise",
        "reminder_style": "gentle",
        "task_organization": "by_priority"
    },
    "goals": {
        "short_term": ["list", "of", "goals"],
        "long_term": ["list", "of", "goals"]
    },
    "routines": {
        "morning": "Description of morning routine",
        "evening": "Description of evening routine"
    },
    "working_style": "morning person",
    "recurring_commitments": [
        {"title": "Team standup", "frequency": "daily", "time": "10:00"},
        {"title": "Gym", "frequency": "3x per week", "preferred_times": ["18:00", "19:00"]}
    ]
}

save_profile(profile)
```

Replace `[SKILL_DIR]` with the actual skill directory path.

**Confirmation:**

```
Perfect! I've saved your profile. From now on, I'll provide personalized assistance based on your schedule, preferences, and goals. I'll help you stay organized, track your tasks, and optimize your time.

You can update your profile anytime by asking me to modify your preferences or schedule.
```

### Step 3: Load Profile and Context

For all personal assistance queries, load the user's data:

```bash
# Check profile status
python3 scripts/assistant_db.py has_profile

# Get full profile
python3 scripts/assistant_db.py get_profile

# Get current tasks
python3 scripts/assistant_db.py get_tasks

# Get schedule
python3 scripts/assistant_db.py get_schedule

# Get context and notes
python3 scripts/assistant_db.py get_context

# Get quick summary
python3 scripts/assistant_db.py summary
```

Or use Python imports for more control:

```python
import sys
sys.path.append('[SKILL_DIR]/scripts')
from assistant_db import get_profile, get_tasks, get_schedule, get_context

profile = get_profile()
tasks = get_tasks()
schedule = get_schedule()
context = get_context()
```

### Step 4: Provide Personalized Assistance

Apply the loaded profile and context to provide tailored assistance:

**Key Principles:**

1. **Respect User Preferences**
   - Use their preferred communication style
   - Follow their task organization preferences
   - Honor their working hours and routines

2. **Leverage Context**
   - Reference their goals when suggesting tasks
   - Consider their schedule when proposing activities
   - Adapt to their working style (morning person, etc.)

3. **Be Proactive**
   - Suggest task prioritization based on goals
   - Remind about recurring commitments
   - Flag scheduling conflicts
   - Propose routine optimizations

4. **Maintain Context**
   - Track important interactions
   - Remember ongoing projects
   - Note temporary context for continuity

**Example Applications:**

**Scenario 1: Task Management**
```
User: "I need to finish the quarterly report"

Claude: [Loads profile - finds: works 9-5, morning person, prefers focused blocks]

I'll add that to your tasks. Based on your preference for morning work, I recommend
scheduling this during your 9-11am block tomorrow when you're most productive.

The report is due when? I'll set an appropriate priority and reminder.

[Adds task with context-aware details]
```

**Scenario 2: Schedule Conflict**
```
User: "Can I schedule a dentist appointment at 10am Tuesday?"

Claude: [Checks schedule - finds: Team standup at 10am daily]

I notice you have your daily team standup at 10am. Would you like to:
1. Schedule the dentist for 11am instead
2. Move your standup for that day
3. Choose a different day entirely

What works best for you?
```

**Scenario 3: Goal-Aligned Suggestion**
```
User: "What should I focus on this week?"

Claude: [Loads profile - finds short-term goal: "Learn Python"]

Based on your goal to learn Python, I recommend dedicating 3-4 hours this week to:
1. Tuesday 7-8pm: Python tutorial (after gym, before evening routine)
2. Thursday 7-8pm: Practice exercises
3. Saturday 10-12pm: Build a small project

This fits your schedule and keeps you on track for your 3-month learning goal.
Shall I add these to your calendar?
```

### Step 5: Task Management Operations

Use the task management system for organizing user tasks:

**Adding Tasks:**

```python
import sys
sys.path.append('[SKILL_DIR]/scripts')
from assistant_db import add_task, add_context

task = {
    "title": "Complete quarterly report",
    "description": "Q4 financial analysis",
    "priority": "high",  # high, medium, low
    "category": "work",
    "due_date": "2025-11-15",
    "estimated_time": "3 hours"
}

add_task(task)
add_context("interaction", "Added Q4 report task", "normal")
```

**Quick Task Operations via CLI:**

```bash
# List all tasks in formatted view
python3 scripts/task_helper.py list

# Add a quick task
python3 scripts/task_helper.py add "Buy groceries" medium "2025-11-08" personal

# Complete a task
python3 scripts/task_helper.py complete <task_id>

# View overdue tasks
python3 scripts/task_helper.py overdue

# View today's tasks
python3 scripts/task_helper.py today

# View this week's tasks
python3 scripts/task_helper.py week

# View tasks by category
python3 scripts/task_helper.py category work
```

**Completing Tasks:**

```python
from assistant_db import complete_task

complete_task(task_id)
```

**Updating Tasks:**

```python
from assistant_db import update_task

update_task(task_id, {
    "priority": "urgent",
    "due_date": "2025-11-10"
})
```

### Step 6: Schedule and Event Management

Manage calendar events and recurring commitments:

**Adding Events:**

```python
from assistant_db import add_event

# One-time event
event = {
    "title": "Dentist appointment",
    "date": "2025-11-12",
    "time": "14:00",
    "duration": "1 hour",
    "location": "Downtown Dental",
    "notes": "Bring insurance card"
}

add_event(event, recurring=False)

# Recurring event
recurring_event = {
    "title": "Team standup",
    "frequency": "daily",
    "time": "10:00",
    "duration": "15 minutes",
    "days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
}

add_event(recurring_event, recurring=True)
```

**Getting Upcoming Events:**

```python
from assistant_db import get_events

# Get events for next 7 days
upcoming = get_events(days_ahead=7)

# Get events for next 30 days
monthly = get_events(days_ahead=30)
```

### Step 7: Context Management and Memory

Maintain context for continuity and personalized assistance:

**Adding Context:**

```python
from assistant_db import add_context

# Track an interaction
add_context("interaction", "User mentioned struggling with morning productivity", "normal")

# Add an important note (kept indefinitely)
add_context("note", "User prefers written communication over calls for work matters", "high")

# Add temporary context (auto-cleaned after 7 days)
add_context("temporary", "Currently working on project X deadline next week", "normal")
```

**Context Importance Levels:**
- `"low"` - Automatically cleaned up quickly
- `"normal"` - Standard retention (30 days for interactions, 7 days for temporary)
- `"high"` - Kept indefinitely (for important notes) or extended retention

**Retrieving Context:**

```python
from assistant_db import get_context

# Get all context
all_context = get_context()

# Get specific type
interactions = get_context("recent_interactions")
notes = get_context("important_notes")
temp = get_context("temporary_context")
```

### Step 8: Intelligent Data Cleanup

The system automatically manages data retention, but you can trigger manual cleanup:

```bash
# Clean up data older than 30 days (default)
python3 scripts/assistant_db.py cleanup

# Clean up with custom retention period
python3 scripts/assistant_db.py cleanup 60
```

**What Gets Cleaned:**
- ✓ Completed tasks older than retention period
- ✓ Past one-time events
- ✓ Old interactions (unless marked high importance)
- ✓ Temporary context older than 7 days
- ✗ User profile (never cleaned)
- ✗ Pending tasks (never cleaned)
- ✗ Important notes (never cleaned)
- ✗ Recurring events (never cleaned)

### Step 9: Updating User Profile

When users want to update their profile or preferences:

```python
from assistant_db import get_profile, save_profile

# Load current profile
profile = get_profile()

# Update specific fields
profile["work_hours"]["start"] = "08:00"
profile["preferences"]["reminder_style"] = "firm"

# Save updated profile
save_profile(profile)
```

Or update schedule information:

```python
from assistant_db import get_schedule, save_schedule

schedule = get_schedule()
schedule["working_hours"]["Friday"] = {"start": "09:00", "end": "15:00"}
save_schedule(schedule)
```

## Best Practices

1. **Always Load Context First**
   - Check profile status before any personalized assistance
   - Load relevant data (profile, tasks, schedule) at the start

2. **Be Proactive**
   - Suggest task prioritization
   - Flag scheduling conflicts
   - Remind about goals
   - Propose optimizations

3. **Respect Preferences**
   - Honor communication style preferences
   - Follow task organization preferences
   - Respect working hours and boundaries

4. **Maintain Continuity**
   - Track important interactions in context
   - Reference previous conversations
   - Remember ongoing projects

5. **Keep Data Fresh**
   - Periodically run cleanup (suggest monthly)
   - Mark important information appropriately
   - Use temporary context for short-term tracking

6. **Provide Value**
   - Make connections between tasks and goals
   - Optimize schedules based on working style
   - Offer personalized productivity insights

7. **Update Incrementally**
   - If user mentions new preferences in conversation, offer to update profile
   - Add new commitments to schedule as they arise
   - Track context changes naturally

## Example Interactions

**Example 1: First-Time User**
```
User: "Help me organize my week"

Claude: [Checks profile - finds none]

I'd love to help you organize your week! To provide the most personalized assistance,
let me first learn about your schedule and preferences. This will only take a few minutes.

What's your typical work schedule like? For example, do you work 9-5, have flexible
hours, or something else?

[Proceeds through profile setup]

Great! Now let me look at your week and help you organize it effectively...
```

**Example 2: Task Management**
```
User: "I have so many things to do, I'm overwhelmed"

Claude: [Loads tasks - finds 15 pending tasks, 8 with no due date]

I can see you have 15 pending tasks. Let me help you prioritize based on your goals
and schedule.

High Priority (Due Soon):
1. Quarterly report - Due Tuesday (aligns with your career goals)
2. Client presentation - Due Thursday

Medium Priority (This Week):
3. Code review - No deadline but good for Friday afternoon
4. Team feedback - Due next Monday

Let's start with the top 2. Your morning blocks (9-11am) work best for focused work
like the quarterly report. Shall I schedule it for tomorrow morning?

[Helps organize and prioritize based on profile]
```

**Example 3: Schedule Optimization**
```
User: "I want to start exercising regularly"

Claude: [Loads profile - finds: evening person, free 18:00-19:00 most days]

Based on your schedule and preferences, I can see you're typically free between
6-7pm on weekdays. This aligns well with your peak energy time in the evenings.

I recommend:
- Monday, Wednesday, Friday: 18:00-19:00 (gym or home workout)
- Start with 30-minute sessions

This gives you recovery days and doesn't conflict with your Tuesday team dinner
or Thursday book club.

Shall I add these as recurring events to your calendar?
```

**Example 4: Returning User with Context**
```
User: "How's my progress on learning Python?"

Claude: [Loads context - finds: Goal to learn Python, completed 4 tutorial sessions,
last one was 5 days ago]

You're making good progress! You've completed 4 Python tutorial sessions over the
past 3 weeks. However, I notice it's been 5 days since your last session.

To maintain momentum toward your 3-month goal, let's schedule your next session.
Your usual Thursday 7pm slot is open tomorrow. Does that work?

Also, you're at the point where building a small project would be valuable. What
interests you - a web scraper, a to-do app, or something else?
```

**Example 5: Preference Update**
```
User: "I've started a new job, my schedule has changed"

Claude: [Loads current profile]

Congratulations on the new job! Let me update your profile with your new schedule.

What are your new working hours? And have any of your recurring commitments changed?

[Collects updated information and saves]

Perfect! I've updated your profile with your new 8-4 schedule and remote work setup.
I'll adjust all my suggestions accordingly. Your morning productivity block is now
8-10am instead of 9-11am.
```

## Technical Notes

**Data Storage Location:**
All data is stored in `~/.claude/personal_assistant/`:
- `profile.json` - User profile and preferences
- `tasks.json` - Task list and completed tasks
- `schedule.json` - Calendar events and recurring commitments
- `context.json` - Interaction history, notes, and temporary context

**Database Commands:**
```bash
# Profile management
python3 scripts/assistant_db.py has_profile
python3 scripts/assistant_db.py get_profile

# Task management
python3 scripts/assistant_db.py get_tasks

# Schedule management
python3 scripts/assistant_db.py get_schedule

# Context management
python3 scripts/assistant_db.py get_context

# Utilities
python3 scripts/assistant_db.py summary      # Quick overview
python3 scripts/assistant_db.py cleanup [days]  # Clean old data
python3 scripts/assistant_db.py export       # Export all data
python3 scripts/assistant_db.py reset        # Reset everything
```

**Task Helper Commands:**
```bash
python3 scripts/task_helper.py list
python3 scripts/task_helper.py add <title> [priority] [due_date] [category]
python3 scripts/task_helper.py complete <task_id>
python3 scripts/task_helper.py overdue
python3 scripts/task_helper.py today
python3 scripts/task_helper.py week
python3 scripts/task_helper.py category <name>
```

**Data Retention Policy:**
- User profile: Never auto-deleted
- Pending tasks: Never auto-deleted
- Completed tasks: Deleted after 30 days (configurable)
- One-time past events: Deleted after 30 days (configurable)
- Recurring events: Never auto-deleted
- Recent interactions: Deleted after 30 days unless marked "high" importance
- Important notes: Never auto-deleted
- Temporary context: Deleted after 7 days

**Profile Data Structure:**
```json
{
  "initialized": true,
  "name": "John Doe",
  "preferred_name": "John",
  "timezone": "America/New_York",
  "location": "New York, USA",
  "work_hours": {
    "start": "09:00",
    "end": "17:00",
    "flexible": true
  },
  "preferences": {
    "communication_style": "concise",
    "reminder_style": "gentle",
    "task_organization": "by_priority"
  },
  "goals": {
    "short_term": ["Learn Python", "Run 5K"],
    "long_term": ["Career advancement", "Financial independence"]
  },
  "working_style": "morning person"
}
```

## Resources

### scripts/assistant_db.py

Main database management module providing:
- Profile management (get, save, check initialization)
- Task CRUD operations (add, update, complete, delete)
- Schedule and event management
- Context tracking with importance levels
- Intelligent data cleanup
- Data export and summary functions

### scripts/task_helper.py

Convenience script for quick task operations:
- Formatted task listings
- Quick task addition
- Task filtering (overdue, today, this week, by category)
- Task completion by ID or title match