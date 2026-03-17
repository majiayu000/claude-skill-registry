---
name: dex-level-up
description: Discover unused Dex features based on your usage patterns
---

## Purpose

Discover Dex capabilities you haven't used yet. No FOMO — this is your concierge showing you what's available so you can get full value from the system without missing features.

---

## Step 1: Check Usage Log

Read `System/usage_log.md` to understand what features the user has adopted.

---

## Step 2: Analyze Patterns

Look for natural progressions and gaps:

### Progression Patterns

**Daily → Weekly → Quarterly:**
- Using `/daily-plan` but not `/week-plan`? → Suggest weekly planning
- Using `/week-plan` but not `/quarter-plan`? → Suggest quarterly goals

**Meeting Capture → Relationship Tracking:**
- Processing meetings but no person pages? → Suggest person pages
- Have person pages but not company pages? → Suggest processing meetings to auto-create company pages in 05-Areas/Companies/

**Tasks → Projects:**
- Managing tasks but no project pages? → Suggest project tracking
- Have projects but not using `/project-health`? → Suggest health checks

**Basic → Advanced:**
- Comfortable with core workflows? → Suggest journaling, learning capture
- Using all features consistently? → Suggest custom MCPs, system improvements

### Role-Based Relevance

Prioritize suggestions based on user's role (from `System/user-profile.yaml`):

**Product Managers:**
- `/product-brief` for feature ideation
- Project tracking for initiative management
- Relationship tracking for stakeholder management

**Engineering:**
- Project tracking for sprint/milestone management

**Sales/Customer Success:**
- Person pages for customer context
- Relationship tracking for account management
- Meeting prep for sales calls

**Leadership:**
- Quarterly planning for strategic thinking
- Weekly reviews for team synthesis
- Learning capture for pattern recognition

---

## Step 2.5: Check for Role-Specific Skills

After analyzing universal feature usage, check for role-specific skills:

### Identify User's Role Group

1. Read `System/user-profile.yaml` → `role` field
2. Map role to role_group using this mapping:
   - **product:** Product Manager, CPO, Product Ops, Fractional CPO
   - **sales:** Sales, Account Executive, CRO, RevOps
   - **marketing:** Marketing, CMO
   - **finance:** Finance, CFO
   - **engineering:** Engineering, CTO, Solutions Engineering
   - **customer_success:** Customer Success, CCO
   - **operations:** Product Ops, RevOps, BizOps, Data/Analytics
   - **leadership:** CEO, Founder, C-Suite roles
   - **design:** Design
   - **support:** People (HR), Legal, IT Support, CHRO, CLO, CIO, CISO
   - **advisory:** Consultant, Coach, Venture Capital/Private Equity

### Check Available Skills

1. List files in `.claude/skills/_available/[role_group]/`
2. For each available skill directory, read its SKILL.md and extract:
   - name (from frontmatter)
   - description (from frontmatter)
   - jtbd (from frontmatter)
   - time_investment (from frontmatter)

### Check Installed Skills

1. List files in `.claude/skills/`
2. Cross-reference with available skills to determine which are not yet installed

### Present Role Skills (if any uninstalled)

If there are uninstalled role-specific skills, include this section in the output:

```markdown
---

## 💼 Role-Specific Skills for [Role Name]

You haven't installed role-specific skills yet. Here's what's available for [role_group] roles:

### /[skill-name]
**Job to be done:** [JTBD from frontmatter]
**Time investment:** [time_investment from frontmatter]

[Repeat for each available uninstalled skill]

---

**Want to install these skills?** 

Say:
- **"install all"** to add all [X] skills
- **"install [skill-name]"** to add specific skills
- **"tell me more about [skill-name]"** to learn more before installing
```

### Installation Workflow

When user says "install [skill]" or "install all":

1. **Verify skill exists** in `.claude/skills/_available/[role_group]/[skill-name]/`
2. **Copy skill folder:**
   ```bash
   cp -r .claude/skills/_available/[role_group]/[skill-name]/ .claude/skills/[skill-name]/
   ```
3. **Confirm to user:** "✓ Installed `/[skill-name]` - try it now!"
4. **Update usage log:** Add the skill to the "Role-Specific Skills" section in `System/usage_log.md` (see Step 5 for format)
5. **If installing multiple:** Show progress for each skill

**Important:** Only copy the skill folder itself (not the parent role_group folder). The skill should end up at `.claude/skills/[skill-name]/SKILL.md`, not `.claude/skills/[role_group]/[skill-name]/SKILL.md`.

---

## Step 3: Integration Discovery

Check for connected integrations and surface opportunities the user may be missing.

### Unused Capabilities (Already Connected)

Read `System/integrations/config.yaml` and check each enabled integration for underutilized features:

**For each enabled integration, check if all capabilities are active:**

- **Gmail connected** but `email_followup: false`?
  → "You have Gmail connected but haven't enabled follow-up detection. It flags emails waiting for replies — useful in `/daily-plan`."

- **Gmail connected** but `newsletter_digest: false`?
  → "Gmail is connected but newsletter digests aren't enabled. It summarizes your morning newsletters so you can skim instead of read."

- **Todoist/Things connected** but `/process-inbox` doesn't route to it?
  → "You have [Tool] connected but inbox processing doesn't route tasks to it yet. Want to enable two-way sync so tasks land in both places?"

- **Jira connected** but `sprint_tracking: false`?
  → "Jira is connected but sprint tracking isn't active. It would pull sprint items into your `/daily-plan`."

- **Zoom connected** but Granola also active?
  → "You have both Zoom and Granola — Granola already captures meetings. Zoom's main added value is scheduling. Working as expected?"

Present any findings as a section:

```markdown
## Untapped Integration Features

You have [X] integrations connected. Here are features you haven't turned on yet:

- **Gmail follow-up detection** — Surfaces emails waiting for replies in your daily plan.
  → Enable: Edit `System/integrations/config.yaml` → `google-workspace.email_followup: true`

- **[Other unused feature]** — [Brief value prop].
  → Enable: [Specific instruction]
```

If all features of all connected integrations are active, skip this section.

### Missing Integrations (Not Connected)

Run the integration concierge to check for tool signals in the vault:

```bash
node .claude/hooks/integration-concierge.cjs
```

Parse the JSON output. If `high_value` items are found that aren't already connected:

```markdown
## Tool Connections You Might Want

I scanned your notes and found references to tools you haven't connected:

- **[Name]** — [mentions] references across your notes ([example files])
  → [value proposition]
  → Connect with `[setup command]` ([setupTime] setup)

[Repeat for each high_value item, max 3]
```

If no high_value items found, skip this section entirely. Don't show moderate or available items here — keep `/dex-level-up` focused on high-signal recommendations only.

---

## Step 4: Generate Recommendations

Show **2-3 specific, actionable suggestions** ranked by:

1. **Natural next step:** Builds on what they're already doing
2. **High value:** Would significantly improve their workflow
3. **Low friction:** Easy to try without disrupting flow

### Recommendation Format

For each suggestion:

```markdown
### {{Feature Name}} - {{Why it matters}}

**What you're missing:** {{Brief explanation}}

**Why now:** {{Why this is relevant based on their usage}}

**How to start:** {{Specific command or action}}

**Time investment:** {{2 minutes / 10 minutes / ongoing}}
```

---

## Step 5: Present Recommendations

Display in this format:

```markdown
# 🚀 Level Up Your Dex System

Based on your usage, here are **{{X}} ways to get more value** from Dex:

---

## 1. {{Feature Name}}

**What you're missing:** {{Explanation}}

**Why it's relevant:** {{Context from their usage}}

**How to start:** {{Command or action}}

**Time:** {{Investment}}

---

## 2. {{Feature Name}}

[Same format]

---

## 3. {{Feature Name}}

[Same format]

---

## Want to try one now?

Just say the number or feature name, and I'll guide you through it.

---

*Run `/dex-level-up` anytime to see what else you might be missing.*
```

---

## Step 6: Track Adoption (Silent)

When user tries a recommended feature, silently update `System/usage_log.md` by checking the box for that feature.

**Update triggers:**
- User runs a command → Check command box
- User creates person page → Check person page box
- User creates project → Check project tracking box
- Work MCP tools used → Check task boxes
- **User installs role-specific skill** → Check "Installed" box in Role-Specific Skills section
- **User runs role-specific skill** → Check "Used" box in Role-Specific Skills section

**Update method:**
- Simple find/replace: `- [ ] Feature` → `- [x] Feature`
- No announcement needed

**Role-Specific Skills Tracking:**

When user installs a role-specific skill, add it to `System/usage_log.md` if the "Role-Specific Skills" section doesn't exist:

```markdown
## Role-Specific Skills

**Installed:**
- [x] /[skill-name]

**Used:**
- [ ] /[skill-name]
```

If section exists, just check the appropriate boxes for the skill.

---

## Examples

### Example 1: Daily User, No Weekly Planning

```markdown
# 🚀 Level Up Your Dex System

Based on your usage, here are **3 ways to get more value** from Dex:

---

## 1. Weekly Planning - Think Bigger Picture

**What you're missing:** You've been crushing daily plans (42 days straight! 🔥), but you're planning day-to-day without a weekly view. Weekly planning helps you think bigger than today's tasks.

**Why it's relevant:** Consistent daily planning shows you value structure. Weekly planning is the natural next step — it makes your daily plans even better because you're working toward clear weekly outcomes.

**How to start:** Run `/week-plan` on Monday morning (or Friday evening). Set your Top 3 priorities for the week. Then when you run `/daily-plan`, I'll show how today's work connects to those weekly goals.

**Time:** 5-10 minutes once per week

---

## 2. Person Pages - Never Walk Into Meetings Cold

**What you're missing:** You mention people in your notes, but you don't have person pages yet. Person pages aggregate everything about someone — meeting history, open items, context — so you're never scrambling before calls.

**Why it's relevant:** You have 12 meetings this week. Right now, you're probably trying to remember what you discussed last time. With person pages, I can show you that context automatically in `/daily-plan` and `/meeting-prep`.

**How to start:** Just say "Create a person page for [name]" and I'll set it up. Or next time you mention someone in a meeting note, I'll offer to create their page automatically.

**Time:** 2 minutes per person, one-time setup

---

## 3. Weekly Review - Spot Patterns You're Missing

**What you're missing:** You're planning every week, but you're not reviewing what happened. Weekly reviews help you spot patterns (energy, challenges, wins) that aren't obvious day-to-day.

**Why it's relevant:** After 6 weeks of weekly planning, you have data. A weekly review surfaces insights like "I'm always blocked on Fridays" or "My best work happens Tuesday mornings." That knowledge helps you plan better.

**How to start:** Run `/week-review` on Friday afternoon or Sunday evening. I'll analyze your week, show patterns, and suggest adjustments.

**Time:** 10-15 minutes once per week

---

## Want to try one now?

Just say the number or feature name, and I'll guide you through it.
```

### Example 2: Power User, Advanced Features

```markdown
# 🚀 Level Up Your Dex System

You're using Dex like a pro. Here are **2 advanced features** that could push your system even further:

---

## 1. Custom MCP Integration - Connect Your CRM

**What you're missing:** You're tracking relationships manually, but your CRM already has this data. A custom MCP could sync deal status, contact info, and interaction history automatically.

**Why it's relevant:** You've built 23 person pages and you're consistent with relationship tracking. Automating the data sync would save you 15-20 minutes per week and ensure your Dex system stays in sync with your CRM.

**How to start:** Run `/create-mcp` and tell me which CRM you use (Salesforce, HubSpot, etc.). I'll guide you through creating a custom MCP server that pulls data automatically.

**Time:** 30-45 minutes setup, saves 15-20 min/week ongoing

---

## 2. Learning Synthesis - Turn Experience Into Knowledge

**What you're missing:** You've captured 47 session learnings, but you haven't synthesized them into durable knowledge yet. Learning synthesis turns "I made this mistake" into "Here's the principle I learned."

**Why it's relevant:** You have a goldmine of captured experience. Running `/save-insight` regularly would turn those raw learnings into a knowledge base you can reference and share.

**How to start:** Run `/save-insight` after finishing a complex project or at the end of each month. I'll help you extract patterns from your session learnings and write them into `06-Resources/Learnings/`.

**Time:** 10 minutes per insight, quarterly or as-needed

---

## Want to try one now?

Just say the number or feature name, and I'll guide you through it.
```

---

## Special Cases

### If Usage Log is Empty

> "Looks like you're just getting started! Let me show you the core workflows that most people find valuable first..."

Then show the essentials:
1. Daily planning
2. Task management
3. Meeting capture

### If Everything is Checked

> "You're using every feature in Dex! 🎉
> 
> At this point, consider:
> - Building custom MCPs for your specific workflow
> - Running `/dex-improve` to suggest system enhancements
> - Sharing what you've learned — your setup could help others"

### If User Says "Show Me Everything"

> "I could, but that's overwhelming. Let me show you the next 2-3 features that make sense based on where you are.
> 
> If you want to browse everything, check out:
> - `CLAUDE.md` for the full system overview
> - `.claude/commands/` folder for all available commands
> - `06-Resources/Dex_System/Dex_System_Guide.md` for the complete guide"

---

## Capturing Your Own Ideas

After showing recommendations, also mention:

> ---
> 
> **💡 Have your own ideas for improving Dex?**
> 
> Use the `capture_idea` MCP tool anytime you think "I wish Dex did X".
> 
> Your ideas get ranked by:
> - Impact on your daily workflow
> - Fit with your usage patterns
> - Implementation effort
> - Synergy with existing features
> 
> Run `/dex-backlog` to see your ideas ranked, or `/dex-improve` to workshop one.
> 
> *The system helps you systematically improve your PKM over time.*

---

## Integration with Other Commands

### In `/daily-plan`:

If user hasn't run `/dex-level-up` in 7+ days and has unused features, add a gentle nudge:

```markdown
---

💡 **Tip:** You're using {{X}} of {{Y}} Dex features. Run `/dex-level-up` to see what you might be missing.
```

### After Onboarding:

At the end of `/setup`, mention:

> "One more thing: run `/dex-level-up` anytime to discover features you haven't tried yet. No FOMO — just helpful guidance on what's available."

---

## Track Usage (Silent)

**Analytics (Silent):**

Call `track_event` with event_name `level_up_viewed` and properties:
- `features_suggested`
- `features_unknown_count`

This only fires if the user has opted into analytics. No action needed if it returns "analytics_disabled".

---

## Philosophy

This command exists to reduce **feature blindness** — when users don't know what they don't know.

**Not pushy:** Only suggest 2-3 things at a time
**Contextual:** Based on their actual usage patterns
**Progressive:** Natural next steps, not overwhelming options
**Helpful:** Genuine concierge service, not annoying nudges

The goal: Get users to full value as fast as possible without interrupting their flow.
