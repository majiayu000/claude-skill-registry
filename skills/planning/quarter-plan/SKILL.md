---
name: quarter-plan
description: Set 3-5 strategic goals for the quarter
---

## Purpose

Set 3-5 strategic goals for the quarter. Runs at the start of each quarter (or mid-quarter if starting fresh).

## Usage

- `/quarter-plan` — Plan current or upcoming quarter
- `/quarter-plan next` — Plan next quarter (run in last week of current quarter)

---

## Step 0: Check if Quarterly Planning is Enabled

Read `System/user-profile.yaml`:

1. Check `quarterly_planning.enabled` value
2. **If `false` or missing:**
   - Display: "Quarterly planning is currently disabled. Would you like to enable it?"
   - If yes → Run onboarding questions (Step 0.5), then continue
   - If no → End command
3. **If `true`:** Continue to Step 1

---

## Step 0.5: Quarterly Planning Onboarding (First Time)

> "Quarterly planning helps you set 3-5 big goals every 3 months. Your weekly plans will then tie back to these goals.
> 
> **When does your Q1 start?**
> 1. January (calendar year)
> 2. February  
> 3. April (common fiscal year)
> 4. Other month
> 5. I don't want quarterly planning"

**Capture response:**
- If 1-4: Save month to config
- If 5: Set `enabled: false` and end

**Calculate quarter dates:**
```
If Q1 starts in January:
  Q1: Jan-Mar, Q2: Apr-Jun, Q3: Jul-Sep, Q4: Oct-Dec
  
If Q1 starts in February:
  Q1: Feb-Apr, Q2: May-Jul, Q3: Aug-Oct, Q4: Nov-Jan
  
If Q1 starts in April:
  Q1: Apr-Jun, Q2: Jul-Sep, Q3: Oct-Dec, Q4: Jan-Mar
```

**Save to `System/user-profile.yaml`:**
```yaml
quarterly_planning:
  enabled: true
  q1_start_month: 1  # 1=Jan, 2=Feb, 4=Apr, etc
  prompted: true
```

---

## Step 1: Determine Target Quarter

**Calculate current quarter** based on `q1_start_month`:
- Example: If q1_start_month=1 and today is Jan 28:
  - Current quarter: Q1 2026
  - Quarter dates: 2026-01-01 to 2026-03-31

**If no parameter or "current":**
- Plan current quarter

**If parameter is "next":**
- Plan next quarter (for end-of-quarter planning)

Store:
- `target_quarter`: "Q1 2026"
- `quarter_start`: "2026-01-01"
- `quarter_end`: "2026-03-31"

---

## Step 2: Context Gathering

### Check for Last Quarter's Review

Look for `07-Archives/Reviews/[last-quarter].md`:

**If exists, extract:**
- Completed goals
- Incomplete goals
- "Next Quarter Suggestions" section
- Key learnings

**If missing:**
- Note: No previous quarter review found
- This is likely first time using quarterly planning

### Check Current Quarter Goals (if mid-quarter update)

If `01-Quarter_Goals/Quarter_Goals.md` exists with current quarter:
- Read current goals
- Note progress made
- Ask if updating or replacing

### Check Pillars

Read `System/pillars.yaml`:
- Strategic pillars
- Check recent activity across pillars
- Identify any neglected areas

### Scan Recent Projects

Look at `04-Projects/` for active initiatives:
- What's in flight?
- What needs to land this quarter?
- Any new initiatives starting?

### Check Career Goals (if Career system enabled)

Look for `05-Areas/Career/Growth_Goals.md`:

**If exists, extract:**
- Long-term vision (1-3 years)
- Target role/level
- Development focus areas (skills to develop)
- Impact goals
- Career milestones

**If missing:**
- Skip this section (career system not initialized)

---

## Step 3: Interactive Goal Setting

### Review Last Quarter (if available)

> "Last quarter (Q4 2025) goals were:
> 1. [Goal 1] — ✅ Completed
> 2. [Goal 2] — 🔄 In progress (80%)
> 3. [Goal 3] — ❌ Didn't finish
> 
> Anything to carry forward into this quarter?"

Wait for user input.

### Present Context

> "Looking at [Quarter] [Year] ([Start Date] - [End Date]):
> 
> **Active projects:**
> - [Project 1]
> - [Project 2]
> 
> **Pillars to consider:**
> - [Pillar 1]: [Recent activity level]
> - [Pillar 2]: [Recent activity level]
> - [Pillar 3]: [Recent activity level]

**If career goals exist, add:**

> **Your career direction (1-3 years):**
> - Target role: [Role/Level from Growth_Goals.md]
> - Skills to develop: [Key development areas]
> - Impact you want: [Impact goals]
> 
> Keep these in mind as we plan this quarter — your quarterly goals should advance your career goals.

**Then continue:**

> **Let's work backwards from impact:**
> 
> Imagine it's [Quarter End Date] and you're looking back on this quarter feeling incredibly happy with what you accomplished.
> 
> - What outcomes would accelerate your career and impact in your current role?
> - What would you be proud to have delivered?
> - What would matter most to the people you serve?
> 
> What are the 3-5 most important outcomes you want this quarter?"

### Guide Goal Definition

For each goal (aim for 3-5):

> "Goal [N]: What's the outcome?"

Then follow up:
- "Which pillar does this support?"
- "How will you measure success?"
- "What does 'done' look like?"
- "Any key milestones along the way?"

**If career goals exist, also ask:**
- "Does this goal help develop any skills you're targeting? (e.g., [skill1], [skill2] from your career plan)"
- "Does this advance your path to [target role]? How?"

**Note responses for Phase 2 metadata.**

### Pillar Balance Check

After goals defined:

> "Here's how your Q1 goals map to pillars:
> - [Pillar 1]: [X] goals
> - [Pillar 2]: [Y] goals  
> - [Pillar 3]: [Z] goals
> 
> Does this feel like the right balance?"

Allow adjustment.

---

## Step 4: Archive Old Quarter Goals

**If `01-Quarter_Goals/Quarter_Goals.md` exists:**
1. Determine the quarter it represents
2. Move to `07-Archives/Reviews/[old-quarter]-goals.md`
3. Note: This preserves what was PLANNED vs what ACTUALLY happened (from review)

---

## Step 5: Generate Quarter Goals

Use the `create_quarterly_goal` MCP tool for each goal collected in Step 3.

**For each goal, call the tool with:**
- `title`: Goal title
- `pillar`: Pillar ID
- `success_criteria`: What done looks like
- `milestones`: Array of milestone objects
- `quarter`: Quarter string (e.g., "Q1 2026")

**If career goals exist, also include:**
- `career_goal_id`: Which career goal this advances (from Growth_Goals.md)
- `skills_developed`: Array of skills this goal develops (e.g., ["System Design", "Technical Leadership"])
- `impact_level`: "high" (promotion evidence), "medium" (solid contribution), or "low" (tactical)

**The MCP tool will generate markdown like:**

```markdown
---
quarter: Q1 2026
start_date: 2026-01-01
end_date: 2026-03-31
created: [timestamp]
---

# Q1 2026 Goals

**Jan 1 - Mar 31, 2026**

---

## 🎯 Quarter Objectives

### 1. [Goal 1 Title] — **[Pillar]**

**What success looks like:**
[Specific, measurable outcome]

**Key milestones:**
- [ ] [Milestone 1] — By [rough timing]
- [ ] [Milestone 2] — By [rough timing]

**Progress:** 0% 🔴

---

### 2. [Goal 2 Title] — **[Pillar]**

**What success looks like:**
[Specific, measurable outcome]

**Key milestones:**
- [ ] [Milestone 1]
- [ ] [Milestone 2]

**Progress:** 0% 🔴

---

### 3. [Goal 3 Title] — **[Pillar]**

**What success looks like:**
[Specific, measurable outcome]

**Key milestones:**
- [ ] [Milestone 1]
- [ ] [Milestone 2]

**Progress:** 0% 🔴

---

[Repeat for goals 4-5 if applicable]

---

## 📊 Pillar Alignment

| Pillar | Goals | Balance |
|--------|-------|---------|
| [Pillar 1] | [Goal numbers] | [# of goals] |
| [Pillar 2] | [Goal numbers] | [# of goals] |
| [Pillar 3] | [Goal numbers] | [# of goals] |

---

## 🔄 Carried From Last Quarter

[Items from Q4 2025 that are continuing]

- [ ] [Item] — [Context]

---

## 📝 Notes & Context

[Any additional context about the quarter]

---

## 🏁 End of Quarter

*Fill this in when running `/quarter-review`*

### Completed
- 

### Incomplete
- 

### Key Wins
- 

### Learnings
- 

---

*Generated: [timestamp]*
*Command: /quarter-plan*
```

---

## Step 6: Summary & Next Steps

Display summary:

> "Q1 2026 goals set and saved to `01-Quarter_Goals/Quarter_Goals.md`
> 
> **Your focus this quarter:**
> 1. [Goal 1]
> 2. [Goal 2]
> 3. [Goal 3]
> 
> **Pillar balance:** [Note any imbalances]
> 
> **Next steps:**
> - These goals will appear in your weekly planning
> - Update progress notes as you make progress
> - Run `/quarter-review` at end of quarter (Mar 31)
> 
> Ready to plan this week? Run `/week-plan`"

---

## Integration Points

**Called by `/week-plan`:**
- Weekly planning reads from `01-Quarter_Goals/Quarter_Goals.md`
- Prompts user to connect weekly priorities to quarterly goals

**Updated manually:**
- User can update progress percentages
- Check off milestones as they complete

**Reviewed by `/quarter-review`:**
- End of quarter review references these goals
- Compares plan vs actual accomplishment

---

## Graceful Degradation

### First Quarter
- No previous quarter to reference
- Start fresh with current context

### Mid-Quarter Start
- Can run anytime
- Adjust goals for remaining time in quarter
- Note when goals were set

### Disabled State
- Command prompts to enable
- Can enable at any time
- Doesn't affect weekly/daily planning
