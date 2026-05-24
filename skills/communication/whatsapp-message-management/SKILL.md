---
name: whatsapp-message-management
description: Use when user wants to capture tasks, send briefings, or manage life via WhatsApp - leverages existing WhatsApp MCP for mobile-first workflow
---

# WhatsApp Message Management

## Overview

Transform WhatsApp into a powerful life management interface that works seamlessly with ExoMind's task, habit, and knowledge systems. This skill enables mobile-first workflows where you can capture thoughts, receive daily briefings, check in on habits, and manage your life through natural WhatsApp conversations.

**Core principle:** Meet users where they are (on their phone) with quick, actionable messages that integrate with the broader ExoMind ecosystem.

**Announce at start:** "I'm using the WhatsApp message management skill to help you manage your life via mobile messaging."

## Quick Reference

| Phase | Key Activities | Tool Usage | Output |
|-------|---------------|------------|--------|
| **1. Setup** | Configure WhatsApp MCP connection | Check MCP server status | Connected messaging channel |
| **2. Quick Capture** | Parse incoming messages for tasks/notes | `mcp__whatsapp__send_message`, Task creation | Captured items in system |
| **3. Daily Briefing** | Generate and send morning/evening updates | Life OS skills, `mcp__whatsapp__send_message` | Timely briefings delivered |
| **4. Habit Check-ins** | Send reminders and log responses | Habit tracking, `mcp__whatsapp__send_message` | Habit streaks maintained |
| **5. Contextual Queries** | Answer questions using ExoMind knowledge | RAG search, `mcp__whatsapp__send_message` | Informed responses |

## Life OS Integration

This skill integrates seamlessly with the Life OS workflow system:

- **daily-planning**: Get morning priorities and tasks for briefings
- **weekly-review**: Send weekly summaries and reflection prompts
- **processing-inbox**: Quick capture flows into inbox processing
- **conducting-life-assessment**: Track progress via daily briefings
- **goal-setting**: Link daily tasks to quarterly goals

## When to Use

- User mentions "send me" or "message me on WhatsApp"
- Daily briefing requests ("morning summary", "evening recap")
- Quick capture scenarios ("I'll message you the task")
- Habit tracking reminders ("remind me to...")
- Mobile-first workflows
- Time-sensitive notifications
- On-the-go task management

## The Pattern

Copy this checklist to track progress:

```
WhatsApp Management Progress:
- [ ] Phase 1: Setup (WhatsApp MCP configured and tested)
- [ ] Phase 2: Quick Capture (message parsing and task creation working)
- [ ] Phase 3: Daily Briefing (scheduled briefings configured)
- [ ] Phase 4: Habit Check-ins (reminder system active)
- [ ] Phase 5: Contextual Queries (RAG integration functional)
```

### Phase 1: Setup & Connection

**Verify WhatsApp MCP is available:**
- Check MCP server connection status
- Test send/receive capabilities
- Configure user's phone number if needed
- Set up Do Not Disturb hours (default: 22:00-07:00)

**Example verification:**
```bash
# Check if WhatsApp MCP is available
claude mcp list | grep whatsapp

# Test connection with a ping message
# Use appropriate WhatsApp MCP tool to send test message
```

### Phase 2: Quick Capture (Enhanced)

**Parse incoming WhatsApp messages for tasks and notes:**

**Capture patterns to recognize:**
- Task indicators: "remind me", "todo", "task:", "I need to"
- Note indicators: "note:", "remember", "idea:"
- Voice note indicators: "voice memo", "audio note"
- Photo indicators: Image attachments
- Context indicators: "@work", "@home", "#project-name"
- Priority indicators: "urgent", "important", "!!!"

**Enhanced Processing Workflow:**

```javascript
// 1. Receive message via WhatsApp MCP
mcp__whatsapp__list_messages({
  after: lastCheckTime,
  limit: 20
});

// 2. Parse different media types
async function parseQuickCapture(message) {
  if (message.hasAudio) {
    // Voice note to task conversion
    const transcription = await transcribeVoiceNote(message.audioPath);
    return parseTaskFromText(transcription);
  }

  if (message.hasImage) {
    // Photo capture for reference
    const imageContext = await analyzeImage(message.imagePath);
    return {
      type: 'note',
      content: message.caption || 'Visual reference',
      attachment: message.imagePath,
      context: imageContext
    };
  }

  // Text parsing
  return parseTaskFromText(message.text);
}

// 3. Create item and add to inbox (processing-inbox skill)
async function quickCaptureToInbox(parsedItem) {
  const inboxItem = {
    content: parsedItem.content,
    type: parsedItem.type,
    context: parsedItem.context,
    priority: parsedItem.priority,
    tags: parsedItem.tags,
    source: 'whatsapp',
    capturedAt: new Date(),
    attachment: parsedItem.attachment
  };

  // Add to inbox for later processing
  await addToInbox(inboxItem);

  // Send confirmation
  await mcp__whatsapp__send_message({
    recipient: parsedItem.userPhone,
    message: formatConfirmation(inboxItem)
  });
}
```

**Enhanced Capture Examples:**

**Text Capture:**
```
User (WhatsApp): "Remind me to call dentist tomorrow @health"
ExoMind: "✓ Task added to inbox: Call dentist
Due: Tomorrow | Context: health
Process inbox? Reply 'inbox'"
```

**Voice Note Capture:**
```
User (WhatsApp): [Sends voice note: "Remember to buy milk, eggs, and bread on the way home"]
ExoMind: "🎤 Voice note captured and transcribed:
✓ Task added to inbox: Buy milk, eggs, and bread
Context: errands
Process now? Reply 'yes'"
```

**Photo Capture:**
```
User (WhatsApp): [Sends photo of whiteboard with caption "Project ideas from today's meeting"]
ExoMind: "📸 Photo note saved:
'Project ideas from today's meeting'
✓ Added to inbox with visual reference
View later: Reply 'show photos'"
```

**Quick Batch Capture:**
```
User (WhatsApp): "todo: buy groceries, call mom, schedule dentist @personal"
ExoMind: "✓ 3 tasks added to inbox:
1. Buy groceries
2. Call mom
3. Schedule dentist

Context: personal | Ready to process? Reply 'inbox'"
```

**Integration with processing-inbox skill:**

All quick captures flow into the inbox processing workflow:
1. Capture via WhatsApp → Inbox
2. User processes inbox (mobile or desktop)
3. Items converted to tasks, events, or notes
4. Context and priority preserved throughout

### Phase 3: Daily Briefing (Life OS Integration)

**Morning Briefing Template (07:00-09:00):**

Uses **daily-planning** skill to generate structured morning briefing:

```javascript
// Integration with daily-planning skill
const morningBriefing = {
  priorities: [], // Top 3 tasks from daily plan
  calendar: [],   // Next 3 meetings/events
  habits: [],     // Active habits for today
  energy: null,   // Energy level from yesterday
  focus: null     // Today's main focus area
};

// Send via WhatsApp MCP
mcp__whatsapp__send_message({
  recipient: userPhoneNumber,
  message: formatMorningBriefing(morningBriefing)
});
```

**Morning Message Format:**
```
☀️ Good morning! {Day}, {Date}

🎯 TOP 3 PRIORITIES:
1. ⚡ {Priority Task 1} ({Time estimate})
2. ⚡ {Priority Task 2} ({Time estimate})
3. ⚡ {Priority Task 3} ({Time estimate})

📅 NEXT 3 MEETINGS:
• {Meeting 1} at {Time}
• {Meeting 2} at {Time}
• {Meeting 3} at {Time}

✅ PENDING TASKS: {Count}
🔄 HABITS: {Count to complete}

💡 Focus: {Today's main focus area}
⚡ Energy: {Yesterday's energy level}

Reply "done" + number to check off
Reply "plan" for full daily plan
```

**Evening Briefing Template (18:00-20:00):**

Uses **daily-planning** skill for retrospective:

```javascript
// Integration with daily-planning and weekly-review skills
const eveningBriefing = {
  wins: [],           // Min 3 wins from today
  tasksCompleted: 0,  // Count of completed tasks
  habitsCompleted: 0, // Count of completed habits
  energy: null,       // Energy level today (1-5)
  reflection: null,   // Brief reflection prompt
  tomorrow: []        // Preview of tomorrow's priorities
};

// Send via WhatsApp MCP
mcp__whatsapp__send_message({
  recipient: userPhoneNumber,
  message: formatEveningBriefing(eveningBriefing)
});
```

**Evening Message Format:**
```
🌙 Evening recap - {Day}

🎉 TODAY'S WINS (min 3):
1. {Win 1}
2. {Win 2}
3. {Win 3}

✅ COMPLETED:
• {X} tasks finished
• {X} habits maintained
🔥 Active streaks: {List streaks}

⚡ ENERGY CHECK:
How was your energy today? (1-5)
Reply with number

💭 REFLECTION:
{Reflection prompt based on weekly theme}

🔜 TOMORROW PREVIEW:
Top priority: {Tomorrow's #1 task}

Reply "reflect" to share insights
Reply "wins" to add more wins
```

**Weekly Briefing (Sunday Evening):**

Uses **weekly-review** skill:

```javascript
// Integration with weekly-review skill
const weeklyBriefing = {
  weekSummary: {},    // Week's achievements
  goalProgress: [],   // Progress on quarterly goals
  nextWeekFocus: null,// Next week's main focus
  habits: {},         // Habit completion rates
  reflection: null    // Weekly reflection prompt
};

// Send via WhatsApp MCP
mcp__whatsapp__send_message({
  recipient: userPhoneNumber,
  message: formatWeeklyBriefing(weeklyBriefing)
});
```

**Weekly Message Format:**
```
📊 WEEK {Number} SUMMARY

✅ ACCOMPLISHED:
• {X} tasks completed
• {X} habits maintained
• {Key achievements}

🎯 GOAL PROGRESS:
• {Goal 1}: {X}% complete
• {Goal 2}: {X}% complete
• {Goal 3}: {X}% complete

🔥 HABIT STREAKS:
• {Habit 1}: {X} days
• {Habit 2}: {X} days
• {Habit 3}: {X} days

🔜 NEXT WEEK FOCUS:
{Main focus area for upcoming week}

💭 WEEKLY REFLECTION:
{Reflection prompt for weekly review}

Ready for weekly review? Reply "review"
```

### Phase 4: Habit Check-ins

**Reminder scheduling:**
- Send reminders at configured times
- Track responses for habit completion
- Maintain streak counts
- Send encouragement for milestones

**Smart reminder logic:**
- Don't remind if already completed today
- Adjust timing based on completion patterns
- Scale back frequency if consistently completed
- Send encouragement on long streaks

**Example interaction:**
```
ExoMind (15:00): "🏃 Time for your afternoon walk! 7-day streak 🔥"
User: "done"
ExoMind: "✅ Walk logged! Streak: 8 days. You're crushing it!"

ExoMind (21:00): "📖 Evening reading reminder - 30 minutes to hit your goal"
User: "skip today, busy"
ExoMind: "No problem! Your 12-day streak is safe. We'll catch up tomorrow."
```

### Phase 5: Contextual Queries

**Handle questions and requests:**
- Use RAG to search knowledge base
- Pull relevant task/habit context
- Provide concise, mobile-friendly answers
- Offer follow-up actions

**Query patterns:**
- "What tasks do I have for [project]?"
- "Show me my [habit] streak"
- "What did I note about [topic]?"
- "When is [task] due?"

**Example:**
```
User: "What tasks do I have for the website project?"
ExoMind: "🌐 Website Project (3 tasks):
1. ⚡ Design homepage mockup (Due: Fri)
2. Write copy for About page (Due: Next week)
3. Set up hosting (No due date)

Want to see details for any of these?"
```

## Integration

### WhatsApp MCP Tools
**Primary interface for all messaging:**

```javascript
// Send text messages
mcp__whatsapp__send_message({
  recipient: "1234567890",  // Phone number or JID
  message: "Your briefing text here"
});

// Send files/images
mcp__whatsapp__send_file({
  recipient: "1234567890",
  media_path: "/absolute/path/to/file.jpg"
});

// Send voice messages
mcp__whatsapp__send_audio_message({
  recipient: "1234567890",
  media_path: "/absolute/path/to/audio.ogg"
});

// Receive messages
mcp__whatsapp__list_messages({
  after: "2025-01-15T00:00:00Z",
  limit: 20,
  include_context: true
});

// Search messages
mcp__whatsapp__search_contacts({
  query: "John"
});

// Download media from messages
mcp__whatsapp__download_media({
  message_id: "msg_123",
  chat_jid: "1234567890@s.whatsapp.net"
});
```

### Life OS Skill Integration

**daily-planning skill:**
```javascript
// Get today's priorities for morning briefing
const dailyPlan = await getDailyPlan(userId);
const morningBriefing = formatMorningBriefing({
  priorities: dailyPlan.topThree,
  meetings: dailyPlan.calendar,
  habits: dailyPlan.activeHabits
});

await mcp__whatsapp__send_message({
  recipient: userPhone,
  message: morningBriefing
});
```

**weekly-review skill:**
```javascript
// Generate weekly summary for Sunday briefing
const weeklyReview = await getWeeklyReview(userId);
const weeklyBriefing = formatWeeklyBriefing({
  summary: weeklyReview.achievements,
  goalProgress: weeklyReview.goals,
  nextWeek: weeklyReview.nextFocus
});

await mcp__whatsapp__send_message({
  recipient: userPhone,
  message: weeklyBriefing
});
```

**processing-inbox skill:**
```javascript
// Quick capture flows into inbox
const capturedItem = parseQuickCapture(whatsappMessage);
await addToInbox(capturedItem);

await mcp__whatsapp__send_message({
  recipient: userPhone,
  message: "✓ Added to inbox for processing"
});
```

**conducting-life-assessment skill:**
```javascript
// Track energy and reflection via WhatsApp
const energyCheck = await promptEnergyRating(userPhone);
const reflection = await promptReflection(userPhone);

await updateLifeAssessment(userId, {
  energy: energyCheck,
  reflection: reflection,
  date: new Date()
});
```

**goal-setting skill:**
```javascript
// Link daily tasks to quarterly goals in briefings
const goals = await getQuarterlyGoals(userId);
const todaysTasks = await getDailyTasks(userId);
const goalLinkedTasks = linkTasksToGoals(todaysTasks, goals);

// Include in morning briefing
const briefing = formatMorningBriefing({
  priorities: goalLinkedTasks,
  goalContext: goals
});
```

### ExoMind Components
- **Task Manager**: Create, update, complete tasks from messages
- **Habit Tracker**: Log completions, check streaks, send reminders
- **Knowledge Base (RAG)**: Search notes and context for queries
- **Calendar Integration**: Pull events for briefings
- **User Preferences**: DND hours, notification frequency, message style
- **Inbox System**: Quick capture flows into processing workflow

## Common Use Cases

### Use Case 1: Morning Commute Quick Capture
**Scenario:** User is on the train, thinks of three tasks
```
User: "todo: buy groceries, call mom, schedule dentist @personal"
ExoMind: "✓ Created 3 tasks in Personal context:
1. Buy groceries
2. Call mom
3. Schedule dentist

All added to your inbox for processing."
```

### Use Case 2: Daily Briefing Workflow
**Morning (07:30):**
```
ExoMind: "☀️ Good morning! Tuesday, Jan 15

📋 Today's Focus (3 tasks):
1. ⚡ Submit quarterly report (Due today)
2. Review team feedback
3. Prep for 2pm client call

🎯 Habits: Meditation, Exercise, Reading

Ready to crush it? Reply 'done 1' to check off tasks."
```

**Evening (19:00):**
```
ExoMind: "🌙 Evening recap:

✅ Completed: 2 tasks, 3 habits
🔥 Streaks maintained: Meditation (45d), Reading (12d)

Tomorrow's priority: Finish marketing presentation

How did today go? (Great/Good/Tough)"
```

### Use Case 3: Habit Accountability
**Scenario:** User building a meditation habit
```
Day 1 (07:00): "🧘 Morning meditation time! Starting your new habit."
User: "done"
ExoMind: "✅ Great start! Day 1 complete."

Day 7 (07:00): "🧘 Morning meditation - 7 day streak! 🔥"
User: "done"
ExoMind: "✅ Week 1 complete! You're building a solid habit."

Day 30 (07:00): "🧘 Meditation time! 30-DAY MILESTONE! 🎉"
User: "done"
ExoMind: "✅ 30 DAYS! This is now part of who you are. Amazing work!"
```

### Use Case 4: Context-Aware Note Capture
**Scenario:** User learns something valuable
```
User: "Note: React useCallback only needed when passing callbacks to optimized child components - don't overuse #dev #react"

ExoMind: "✓ Note saved with tags: dev, react
Connected to 3 related notes in your knowledge base.
Want to see related content?"

User: "yes"

ExoMind: "Related notes:
1. React performance optimization patterns
2. When to use useMemo vs useCallback
3. React re-render debugging guide

Reply with number to view full note."
```

### Use Case 5: Project Context Switching
**Scenario:** User needs to focus on specific project
```
User: "Show me everything for website redesign project"

ExoMind: "🌐 Website Redesign Project:

📋 Tasks (5):
• Design homepage (Due: Thu) ⚡
• Write new copy (Due: Next week)
• Set up hosting (No due date)
• Configure analytics (No due date)
• Mobile testing (Blocked - needs design)

📝 Recent Notes: 2
🔗 Related Habits: Daily design review

What would you like to focus on?"
```

## Red Flags

### Do Not:
- **Spam messages** - Respect user's attention and DND hours
- **Send long messages** - Keep everything scannable on mobile
- **Ignore context** - Remember conversation history within session
- **Be overly formal** - Match user's communication style
- **Send during DND hours** - Default 22:00-07:00, user configurable
- **Over-notify** - Bundle related updates together
- **Lose messages** - Always confirm receipt and action taken

### Warning Signs:
- User says "too many messages" → Reduce frequency
- Messages go unread for days → Adjust timing or format
- User always uses "skip" on habits → Habit may not be right
- Repeated "I already did this" → Check for duplicate tracking
- User stops responding → Too much noise, dial back

## Message Style Guide

### Tone:
- **Encouraging but not pushy:** "Time for your walk 🏃" not "You MUST walk now!"
- **Celebratory on wins:** "7-day streak! 🔥" with emojis
- **Understanding on misses:** "No problem, we'll catch up tomorrow"
- **Concise and scannable:** Bullets, numbers, emojis for quick reading

### Formatting:
- **Emojis for context:** ✅ (done), ⚡ (urgent), 🔥 (streak), 📋 (tasks)
- **Numbers for quick action:** "Reply 'done 1' to mark complete"
- **Line breaks for readability:** Never send walls of text
- **Bold for key info:** Limited use, important items only

### Response Patterns:
```
Confirmation: "✓ [Action completed]"
Celebration: "✅ [Achievement] 🎉"
Reminder: "🔔 [Habit/Task] - [Context]"
Query result: "📋 [Category]: [List]"
Error: "❌ [Issue] - [What to do]"
```

## Technical Implementation Notes

### Message Parsing (Enhanced)
```javascript
async function parseQuickCapture(message) {
  const patterns = {
    task: /^(todo:|task:|remind me to)/i,
    note: /^(note:|remember:|idea:)/i,
    habit: /^(done|complete|skip|did)/i,
    query: /^(show|what|when|find|plan)/i,
    context: /@(\w+)/g,
    tags: /#(\w+)/g,
    priority: /(!{1,3}|urgent|important|asap)/i,
    voiceNote: message.hasAudio,
    photo: message.hasImage
  };

  // Handle voice notes
  if (patterns.voiceNote) {
    const audioPath = await mcp__whatsapp__download_media({
      message_id: message.id,
      chat_jid: message.chatJid
    });
    const transcription = await transcribeAudio(audioPath.file_path);
    message.text = transcription;
  }

  // Handle photos
  if (patterns.photo) {
    const imagePath = await mcp__whatsapp__download_media({
      message_id: message.id,
      chat_jid: message.chatJid
    });
    return {
      type: 'note',
      content: message.caption || 'Visual reference',
      attachment: imagePath.file_path,
      source: 'whatsapp'
    };
  }

  // Extract type, content, metadata
  const type = Object.keys(patterns).find(key =>
    patterns[key] instanceof RegExp && patterns[key].test(message.text)
  );

  const contexts = [...message.text.matchAll(patterns.context)].map(m => m[1]);
  const tags = [...message.text.matchAll(patterns.tags)].map(m => m[1]);
  const hasPriority = patterns.priority.test(message.text);

  return {
    type: type || 'task',
    content: message.text.replace(patterns[type] || '', '').trim(),
    contexts,
    tags,
    priority: hasPriority ? 'high' : 'normal',
    source: 'whatsapp',
    timestamp: message.timestamp
  };
}
```

### Briefing Generation with Life OS Integration

```javascript
// Morning briefing using daily-planning skill
async function generateMorningBriefing(userId) {
  // Get data from Life OS skills
  const dailyPlan = await getDailyPlan(userId);
  const calendar = await getCalendarEvents(userId, 'today');
  const habits = await getActiveHabits(userId);
  const energy = await getLastEnergyLevel(userId);

  const briefing = `☀️ Good morning! ${formatDate('today')}

🎯 TOP 3 PRIORITIES:
${dailyPlan.priorities.slice(0, 3).map((t, i) =>
  `${i + 1}. ⚡ ${t.title} (${t.timeEstimate})`
).join('\n')}

📅 NEXT 3 MEETINGS:
${calendar.slice(0, 3).map(e =>
  `• ${e.title} at ${formatTime(e.start)}`
).join('\n')}

✅ PENDING TASKS: ${dailyPlan.pendingCount}
🔄 HABITS: ${habits.filter(h => !h.completedToday).length}

💡 Focus: ${dailyPlan.mainFocus}
⚡ Energy: ${energy ? energy.level + '/5' : 'Not tracked'}

Reply "done" + number to check off
Reply "plan" for full daily plan`;

  return briefing;
}

// Evening briefing using daily-planning and weekly-review skills
async function generateEveningBriefing(userId) {
  const completed = await getCompletedTasks(userId, 'today');
  const habits = await getCompletedHabits(userId, 'today');
  const streaks = await getActiveStreaks(userId);
  const tomorrow = await getTomorrowPriorities(userId);
  const reflectionPrompt = await getReflectionPrompt(userId);

  const briefing = `🌙 Evening recap - ${formatDate('today')}

🎉 TODAY'S WINS (min 3):
${completed.slice(0, 3).map((t, i) =>
  `${i + 1}. ${t.title}`
).join('\n')}

✅ COMPLETED:
• ${completed.length} tasks finished
• ${habits.length} habits maintained
🔥 Active streaks: ${streaks.map(s => s.name + ' (' + s.days + 'd)').join(', ')}

⚡ ENERGY CHECK:
How was your energy today? (1-5)
Reply with number

💭 REFLECTION:
${reflectionPrompt}

🔜 TOMORROW PREVIEW:
Top priority: ${tomorrow[0]?.title || 'Not set'}

Reply "reflect" to share insights
Reply "wins" to add more wins`;

  return briefing;
}

// Weekly briefing using weekly-review skill
async function generateWeeklyBriefing(userId) {
  const weekReview = await getWeeklyReview(userId);
  const goalProgress = await getGoalProgress(userId);
  const habitStats = await getWeeklyHabitStats(userId);

  const briefing = `📊 WEEK ${weekReview.weekNumber} SUMMARY

✅ ACCOMPLISHED:
• ${weekReview.tasksCompleted} tasks completed
• ${weekReview.habitsCompleted} habits maintained
• ${weekReview.keyAchievements.join('\n• ')}

🎯 GOAL PROGRESS:
${goalProgress.map(g =>
  `• ${g.name}: ${g.progress}% complete`
).join('\n')}

🔥 HABIT STREAKS:
${habitStats.map(h =>
  `• ${h.name}: ${h.streak} days`
).join('\n')}

🔜 NEXT WEEK FOCUS:
${weekReview.nextWeekFocus}

💭 WEEKLY REFLECTION:
${weekReview.reflectionPrompt}

Ready for weekly review? Reply "review"`;

  return briefing;
}
```

### Scheduling
```javascript
// Use cron jobs for automated briefings
const cron = require('node-cron');

// Morning briefing at 7:30 AM user's timezone
cron.schedule('30 7 * * *', async () => {
  const users = await getActiveUsers();
  for (const user of users) {
    if (!isInDNDHours(user)) {
      const briefing = await generateMorningBriefing(user.id);
      await mcp__whatsapp__send_message({
        recipient: user.phone,
        message: briefing
      });
    }
  }
}, {
  timezone: user.timezone
});

// Evening briefing at 7:00 PM
cron.schedule('0 19 * * *', async () => {
  const users = await getActiveUsers();
  for (const user of users) {
    if (!isInDNDHours(user)) {
      const briefing = await generateEveningBriefing(user.id);
      await mcp__whatsapp__send_message({
        recipient: user.phone,
        message: briefing
      });
    }
  }
}, {
  timezone: user.timezone
});

// Weekly briefing on Sunday at 6:00 PM
cron.schedule('0 18 * * 0', async () => {
  const users = await getActiveUsers();
  for (const user of users) {
    if (!isInDNDHours(user)) {
      const briefing = await generateWeeklyBriefing(user.id);
      await mcp__whatsapp__send_message({
        recipient: user.phone,
        message: briefing
      });
    }
  }
}, {
  timezone: user.timezone
});
```

### State Management
- Track conversation context within session
- Remember last 10 interactions for continuity
- Clear session after 30 minutes of inactivity
- Persist user preferences across sessions
- Store briefing history for pattern analysis
- Link WhatsApp interactions to Life OS data

## Privacy & Security

- **No message logging** - Process and discard, don't store full messages
- **Secure MCP connection** - Encrypted transport
- **User data stays local** - Only send what's necessary to WhatsApp
- **Opt-in by default** - User must enable WhatsApp integration
- **Easy opt-out** - "pause notifications" command anytime

## Examples

### Example 1: Full Morning Routine
```
[07:30 - Automated briefing]
ExoMind: "☀️ Good morning! Wednesday, Jan 16

📋 Today's Focus (4 tasks):
1. ⚡ Submit budget review (Due today)
2. Team standup at 10am
3. Review marketing materials
4. Plan weekend trip

🎯 Habits: Meditation, Exercise, Reading, Water intake
🌤️ Weather: Sunny, 72°F

Reply 'done' + number to check off tasks."

[07:45 - User interaction]
User: "done meditation"
ExoMind: "✅ Meditation complete! 46-day streak 🔥"

[08:30 - Quick capture]
User: "todo: book restaurant for anniversary @personal !!"
ExoMind: "✓ High priority task created: Book restaurant for anniversary
Added to Personal context. Due date?"

User: "friday"
ExoMind: "✓ Due date set: This Friday, Jan 18"

[12:00 - Contextual query]
User: "what's my afternoon looking like?"
ExoMind: "📋 Afternoon (3 items):
• Team standup at 10am ✅ (passed)
• Review marketing materials (Due today)
• Plan weekend trip (No due date)

You're on track! 🎯"
```

### Example 2: Habit Building Journey
```
[Week 1]
Day 1: "🏃 Afternoon walk reminder - let's start strong!"
User: "done"
ExoMind: "✅ Day 1 complete! Great start."

Day 3: "🏃 Walk time! You're 3 for 3 🔥"
User: "skip today, raining"
ExoMind: "No problem! Weather happens. Tomorrow's a new day."

Day 4: "🏃 Back at it! 3-day streak still alive."
User: "done"
ExoMind: "✅ Resilience! That's how habits stick."

[Week 4]
Day 28: "🏃 Walk time - almost at 30 days! 🔥"
User: "done"
ExoMind: "✅ 28 days! Weekend milestone coming up! 🎉"

[Month 2]
Day 60: "🏃 2-MONTH MILESTONE! 🎉 You've walked 60 days!"
User: "done"
ExoMind: "✅ 60 DAYS! This is officially who you are now. Incredible!"
```

### Example 3: Project-Based Workflow
```
User: "Starting work on mobile app project"
ExoMind: "📱 Mobile App Project activated.

Current status:
📋 5 tasks (2 urgent)
📝 8 notes in knowledge base
🔗 Related: UI design habit

Want the task breakdown?"

User: "yes"

ExoMind: "📋 Mobile App Tasks:
1. ⚡ Fix login bug (Due today)
2. ⚡ Review PR #234 (Due today)
3. Design settings screen (Due Fri)
4. Write API docs (Next week)
5. User testing prep (No date)

Start with #1? Reply 'done 1' when complete."

[Later that day]
User: "done 1"
ExoMind: "✅ Login bug fixed!
⚡ Next up: Review PR #234
4 tasks remaining on Mobile App"

User: "note: Login issue was OAuth token expiration, fixed by refreshing tokens every 55min instead of 60min #mobile-app #auth"

ExoMind: "✓ Technical note saved!
Auto-tagged: mobile-app, auth
Connected to 2 related notes.

Back to PR #234 review?"
```

## Life OS Command Reference

Quick commands users can send via WhatsApp:

### Briefing Commands
- `"morning"` or `"briefing"` - Get current morning briefing
- `"evening"` or `"recap"` - Get evening recap
- `"weekly"` - Get weekly summary
- `"plan"` - Get full daily plan

### Task Management
- `"done 1"` - Mark task #1 as complete
- `"done [task name]"` - Mark named task as complete
- `"tasks"` - List all pending tasks
- `"todo: [task]"` - Quick add task to inbox

### Habit Tracking
- `"done [habit]"` - Log habit completion
- `"skip [habit]"` - Skip habit for today
- `"streaks"` - Show all active streaks
- `"habits"` - List today's habits

### Inbox Processing
- `"inbox"` - Show inbox count
- `"process"` - Start inbox processing
- `"capture: [item]"` - Quick capture to inbox

### Energy & Reflection
- `"energy [1-5]"` - Log energy level
- `"reflect"` - Start reflection prompt
- `"wins"` - Add today's wins
- `"wins [text]"` - Quick add win

### Context & Projects
- `"show [project]"` - Show project tasks
- `"focus [area]"` - Set focus area
- `"context @[name]"` - Switch context

### Weekly Review
- `"review"` - Start weekly review
- `"goals"` - Show goal progress
- `"next week"` - Set next week focus

---

## Success Metrics

**Track these to optimize the system:**
- Message response rate (target: >80%)
- Time to task capture (<30 seconds)
- Briefing read rate (target: >90%)
- Habit completion rate improvement
- User satisfaction with notification timing
- Average session length
- "Too many messages" complaints (target: <5%)

**Iterate based on:**
- User feedback on timing and frequency
- Completion patterns (morning vs evening people)
- Response times (adjust send times)
- Habit streaks (celebrate more, remind less as habits stick)
