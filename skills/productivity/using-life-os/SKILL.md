---
name: using-life-os
description: Entry point skill - introduces available Life OS skills, provides command reference, and guides users through the system
---

# Using Life OS

## Overview

**Life OS** is a comprehensive AI-powered personal operating system that helps you manage all aspects of your life through natural conversation. It integrates with your digital ecosystem (WhatsApp, Google Calendar, Google Tasks, Gmail, etc.) to provide intelligent assistance for:

- **Meal Planning & Grocery Shopping** - Automated weekly meal planning with smart grocery lists
- **Recipe Discovery** - Find and scale recipes based on your preferences and dietary needs
- **Task Management** - Capture, organize, and track tasks from any conversation
- **Daily Briefings** - Morning and evening summaries delivered via WhatsApp
- **Personality-Aware Assistance** - Adapts to your control preferences (control freak vs. get things done)

Life OS works seamlessly across devices through WhatsApp integration, making it accessible anywhere.

## Available Skills

### 1. **meal_planning**
Creates personalized weekly meal plans based on dietary needs, preferences, schedule, and budget. Automatically generates coordinated grocery lists.

**Use when:** Planning meals for the week or month

### 2. **recipe-finding**
Searches for recipes matching specific criteria and can resize portions to match your needs. Handles fractional amounts and scaling intelligently.

**Use when:** Looking for specific recipes or adjusting serving sizes

### 3. **grocery-shopping**
Consolidates ingredients across recipes, checks pantry inventory, converts to purchasable quantities, and provides automation for Costco/Instacart ordering.

**Use when:** Creating shopping lists or ordering groceries

### 4. **whatsapp-message-management**
Captures tasks from conversations, sends daily briefings, and enables mobile-first life management through WhatsApp.

**Use when:** Managing life via WhatsApp or setting up daily routines

### 5. **personality_assessment**
Assesses user personality traits to determine control preferences (control freak vs. get things done) and adapts interaction style accordingly.

**Use when:** First-time setup or when user preferences change

### 6. **using-life-os** (This Skill)
Entry point that introduces the system, provides command reference, and guides users through available features.

**Use when:** Getting started or exploring capabilities

## Command Reference

### Getting Started
```
/skill using-life-os
```
Shows this guide and available skills

### Meal Planning & Groceries
```
/skill meal_planning
"Plan my meals for the week - I'm vegetarian, budget is $150, prefer quick dinners"

/skill recipe-finding
"Find me a healthy chicken recipe for 4 people"
"Resize this recipe from 6 servings to 2 servings"

/skill grocery-shopping
"Create my grocery list from this week's meal plan"
"Generate Instacart order from my shopping list"
```

### Task & Message Management
```
/skill whatsapp-message-management
"Send me my morning briefing at 7am"
"Capture task: Buy birthday gift for mom"
"What tasks do I have for today?"
```

### Personality Assessment
```
/skill personality_assessment
"Assess my working style preferences"
```

## Getting Started

### Step 1: Personality Assessment (Optional)
Start by assessing your preferences so Life OS can adapt to your style:

```
/skill personality_assessment
```

This helps Life OS understand whether you prefer detailed control or streamlined automation.

### Step 2: Set Up Daily Briefings
Enable WhatsApp briefings to stay connected throughout the day:

```
/skill whatsapp-message-management
"Set up morning briefing at 7am and evening briefing at 6pm"
```

### Step 3: Plan Your First Week
Create a personalized meal plan:

```
/skill meal_planning
"Plan meals for the week. I'm [dietary preference], cooking for [number] people, budget is $[amount], prefer [quick/gourmet/etc] meals"
```

### Step 4: Generate Grocery List
Convert your meal plan into a shopping list:

```
/skill grocery-shopping
"Create grocery list from this week's meal plan"
```

### Step 5: Ongoing Usage
- **Find recipes**: Use recipe-finding skill when you need specific dishes
- **Capture tasks**: Send tasks via WhatsApp or mention them in conversation
- **Check briefings**: Get morning/evening updates with tasks, calendar, and reminders
- **Adjust preferences**: Update meal plans, dietary restrictions, or automation preferences anytime

## Integration

### SessionStart Hook
When you start a new session, Life OS automatically:

1. **Loads this skill** to remind you of available capabilities
2. **Restores context** from previous sessions (meal plans, preferences, active tasks)
3. **Checks for pending briefings** and scheduled tasks
4. **Suggests next actions** based on time of day and your routine

This ensures seamless continuity across conversations without needing to repeat preferences or context.

### Cross-Skill Coordination
Skills work together automatically:

- **meal_planning** → **grocery-shopping**: Meal plans automatically feed into shopping lists
- **recipe-finding** → **meal_planning**: Found recipes can be added to weekly plans
- **whatsapp-message-management** → All Skills: Briefings include relevant updates from all skills
- **personality_assessment** → All Skills: Preferences guide interaction style across all features

## Example Workflows

### Weekly Routine
```
Monday:
/skill meal_planning
"Plan this week's meals"

/skill grocery-shopping
"Create shopping list and order from Instacart"

Throughout the week:
- Morning briefings via WhatsApp (7am)
- Task capture as needed
- Evening briefings via WhatsApp (6pm)

Sunday:
Review week, plan next week
```

### Quick Dinner Solution
```
/skill recipe-finding
"Find a quick vegetarian dinner recipe for 2 people, under 30 minutes"

[Recipe found]

/skill grocery-shopping
"Add ingredients for this recipe to my shopping list"
```

### First-Time Setup
```
1. /skill using-life-os (read this guide)
2. /skill personality_assessment (set preferences)
3. /skill whatsapp-message-management (enable briefings)
4. /skill meal_planning (plan first week)
5. /skill grocery-shopping (first shopping list)
```

## Tips for Best Results

1. **Be specific with preferences**: Include dietary restrictions, budget, cooking time preferences
2. **Use WhatsApp integration**: Mobile access makes Life OS truly useful throughout the day
3. **Check pantry before shopping**: Update inventory to avoid duplicate purchases
4. **Adjust as you go**: Refine meal plans, change briefing times, update preferences anytime
5. **Capture tasks immediately**: Don't wait - send them via WhatsApp or mention in conversation

## Support & Feedback

- **Questions?** Just ask: "How do I [task]?"
- **Issues?** Report problems: "The [skill] isn't working correctly"
- **Suggestions?** Share ideas: "I wish Life OS could [feature]"

Life OS learns from your usage and adapts over time. The more you use it, the better it understands your preferences and routines.

---

**Welcome to Life OS - Your AI-powered personal operating system!** 🚀
