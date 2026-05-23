---
name: daily-plan
description: Generate PM daily plan with context
disable-model-invocation: false
user-invocable: true
---

## Quick Start

**What to provide:** Nothing required. Just run it.

```
/daily-plan              → Compact daily plan (default: TL;DR + Top 3 + Schedule + Heads Up)
/daily-plan full         → Full daily plan with all sections (metrics, email, strategic alignment)
/daily-plan tomorrow     → Preview tomorrow's plan (evening planning)
```

**What you get:** A prioritized daily plan with meeting context, tasks, and flags. Pulls from your PRDs, meetings, stakeholder profiles, and connected MCPs automatically.

**Time:** 2-5 minutes. Faster with MCPs connected.

---

## Same-Day Plan Detection

Before generating a new plan, check `outputs/` for an existing plan from today.

**If a same-day plan exists:**
```
I see you already have a plan for today (`outputs/[filename]`).

Options:
1. **Update it** - I'll refresh with new context (meetings changed, priorities shifted)
2. **Replace it** - Start fresh (I'll archive the old one as `[filename]-v1.md`)
3. **Keep it** - No changes needed

Which would you prefer?
```

**If no same-day plan exists:** Proceed normally.

---

## Purpose

Start your day with a comprehensive plan that pulls together everything you need: meetings with attendee context, active PRDs, open tasks, metrics to monitor, and stakeholder intelligence.

Inspired by personal operating system patterns but tailored specifically for Product Managers.

## Usage

- `/daily-plan` - Create today's daily plan (compact mode by default)
- `/daily-plan full` - Full daily plan with all sections
- `/daily-plan tomorrow` - Preview tomorrow (evening planning)

---

## Context Routing

**Check these files first:**
1. `context-library/strategy/` - Quarter priorities, OKRs, North Star
2. `outputs/weekly-plans/` - This week's priorities (if `/weekly-plan` was run)
3. `outputs/prds/` - Active PRDs and their stages
4. `context-library/stakeholder-*.md` - Stakeholder profiles and communication styles
5. `outputs/meeting-notes/` - Recent meeting context
6. `context-library/launches/` - Recently launched features (past 2 weeks)

**Integration Options (Multiple Paths):**

**Option 1: MCP Servers (Recommended - Automated)**
- **Google Calendar MCP** - Auto-fetch today's meetings
- **Gmail MCP** - Scan recent important emails
- **Linear/Jira MCP** - Query open tasks
- **Amplitude/Mixpanel MCP** - Pull metrics for features
- **Slack MCP** - Recent team communications

**Option 2: Direct API Access (If MCPs Not Available)**
- **Google Calendar API** - I can help you set up API access and fetch via `curl` or Python
- **Gmail API** - Fetch unread/important emails via API calls
- **Linear API** - Query tasks via GraphQL API
- **Amplitude REST API** - Pull dashboard data
- **Setup guide:** I'll walk you through getting API keys and making first calls

**Option 3: Export/Import Workflow (Manual but Works)**
- **Calendar:** Export today's calendar as .ics → I'll parse it
- **Email:** Forward important emails → I'll extract context
- **Tasks:** Export Linear/Jira to CSV → I'll process it
- **Metrics:** Screenshot dashboard → I'll analyze with vision
- **Setup guide:** I'll show you how to export from each tool

**Option 4: Browser Automation (Semi-Automated)**
- **Using Claude in Chrome MCP:** I can navigate to your tools and extract data
- **Google Calendar:** Open in browser → scrape today's events
- **Gmail:** Open inbox → extract recent threads
- **Linear/Jira:** Open your view → pull assigned tasks
- **Analytics:** Open dashboard → read metrics
- **Setup guide:** I'll help configure Chrome automation

**Option 5: Manual Input (Always Available)**
- I ask targeted questions and you provide quick answers
- Takes 2-3 minutes but works without any setup
- Useful for first time or when tools are down

**Fallback Strategy:**
If no integrations available, I'll:
1. Use file-based data (meeting notes, task lists in PM OS)
2. Ask focused questions (5-6 quick inputs from you)
3. Generate plan with placeholders you can fill in

---

## Workflow

### Step 1: Pre-Flight Checks

1. **Determine target date:**
   - Default: Today
   - If user said "tomorrow": Tomorrow's date
   - Calculate day of week, week number

2. **Check for yesterday's plan (carry-over):**
   - Read `outputs/daily-plans/` for yesterday's plan file
   - If found: Identify which items were likely completed vs. deferred based on:
     - Items with checkboxes still unchecked
     - P0 tasks that had no time blocked
     - Items flagged in "Heads Up" as at-risk
   - Open with: "Carrying over from yesterday: [deferred items]."
   - If no previous plan exists, skip this step.

3. **Check for weekly plan:**
   - Read `outputs/weekly-plans/YYYY-WXX-weekly-plan.md` for current week
   - If exists: Extract this week's Top 3 priorities
   - If missing: Note that week isn't planned (suggest `/weekly-plan`)

4. **MCP availability check:**
   - Attempt to query each MCP silently
   - Note which MCPs are connected
   - Plan graceful fallback for missing MCPs

---

### Step 2: Context Gathering (Run in Parallel)

**A. Calendar & Meetings (Calendar MCP or manual):**

If Calendar MCP available:
```
Query: Get events for [target date]
Extract:
- Meeting times
- Meeting titles
- Attendee names/emails
- Meeting descriptions
```

For each meeting:
- Look up attendees in `context-library/stakeholder-*.md`
- Scan `outputs/meeting-notes/` for recent interactions with each person
- Note: What was discussed last time, open action items

Flag issues:
- Back-to-back meetings (no break between)
- Meetings without prep notes
- Meetings with stakeholders you haven't synced with recently

If Calendar MCP not available:
- Ask user: "What meetings do you have today?"
- Or read from manual calendar file if one exists

---

**B. Email Context (Gmail MCP or manual):**

If Gmail MCP available:
```
Query: Get unread/important emails from past 24 hours
Filter:
- Emails from stakeholders (match against stakeholder profiles)
- Emails with keywords: "urgent", "decision", "review", "feedback"
- Thread participants you're meeting with today
```

Extract:
- Open questions you need to answer
- Decisions waiting on you
- Context for today's meetings

If Gmail MCP not available:
- Skip this section or ask: "Any important emails I should know about?"

---

**C. Active PRDs & Initiatives:**

Scan `outputs/prds/` and `context-library/prds/`:
- Check file modification dates (recently updated = active)
- Read frontmatter or first section to determine stage:
  - Team Kickoff
  - Planning Review
  - XFN Kickoff
  - Solution Review
  - Launch Readiness
  - Impact Review

For each active PRD:
- Note: What stage it's in
- What the next milestone is
- Who's blocking progress (if stalled)

Cross-reference with `context-library/strategy/`:
- How does each PRD map to quarter priorities?
- Which strategic pillar does it support?

---

**D. Tasks & Action Items (Linear/Jira MCP or files):**

If Linear/Jira MCP available:
```
Query: Get tasks assigned to user, status != Done
Filter by priority/labels:
- P0 or "urgent" or "blocker"
- P1 or "important"
- P2 or default
```

If MCP not available:
- Scan `outputs/meeting-notes/` for unchecked action items
- Look for task lists in recent notes

Categorize:
- **P0 (Must do today):** Blockers, urgent, time-sensitive
- **P1 (Important this week):** High-impact, supports weekly priorities
- **P2 (If time allows):** Nice-to-have, low urgency

---

**E. Metrics to Monitor (Analytics MCP or files):**

Check `context-library/launches/` for features launched in past 2 weeks.

For each recent launch:
If Analytics MCP available:
```
Query: Get key metrics for [feature]
Time range: Since launch date
Metrics: Adoption, engagement, conversion (based on PRD success criteria)
```

If MCP not available:
- Check if metrics file exists in `context-library/metrics/`
- Or note: "Manual check needed for [feature] metrics"

Flag:
- Metrics trending down (regression)
- Metrics not meeting target (needs intervention)
- Metrics exceeding expectations (wins to celebrate)

---

**F. Stakeholder Intelligence:**

For each person you're meeting today:

1. **Profile lookup:**
   - Read `context-library/stakeholder-*.md` if exists
   - Extract: Role, communication style, priorities, pet peeves

2. **Recent interaction history:**
   - Scan `outputs/meeting-notes/` for past meetings with this person
   - Extract: Last meeting date, topics discussed, commitments made

3. **Open loops:**
   - Action items you owe them
   - Action items they owe you
   - Decisions pending their input

4. **Context for today:**
   - Why are you meeting?
   - What do they need from you?
   - What do you need from them?

---

### Output Mode Selection

**Compact Mode (Default):**
When the PM runs `/daily-plan` without the `full` flag, generate a compact plan showing ONLY:
1. **TL;DR** (3 lines max: meetings count, P0 count, key focus)
2. **Today's Three** (or Two/Four based on meeting load)
3. **Schedule with Meeting Context** (time, title, attendees, one-line context)
4. **Heads Up** (flags and risks only)

This fits on one screen. No scrolling required.

**Full Mode:**
When the PM runs `/daily-plan full` or asks for "more detail," include ALL sections from the template below: TL;DR, Strategic Context, Today's Three, Schedule & Meeting Prep, detailed Meeting Context, Tasks by Priority, Metrics to Watch, Email/Communication Highlights, Heads Up, and Strategic Alignment Check.

---

### Step 3: Synthesis & Prioritization

**Determine "Today's Three":**

Rules for prioritization:
1. **P0 tasks always included** (blockers, urgent items)
2. **Meeting outcomes** that advance weekly priorities
3. **Strategic alignment** (tasks that support quarter goals)
4. **Stakeholder commitments** (things you promised to deliver)

If heavy meeting day (4+ hours in meetings):
- Reduce to "Today's Two" (realistic capacity)

If light meeting day (< 2 hours):
- Can expand to "Today's Four" if user has capacity

**Identify potential conflicts:**
- P0 task due today but no time blocked (flag in "Heads Up")
- Meeting requires prep but no prep time available
- Stakeholder needs decision but you're missing input

---

### Step 4: Generate Daily Plan

Create file: `outputs/daily-plans/YYYY-MM-DD-daily-plan.md`

**Template:**

```markdown
---
date: YYYY-MM-DD
day: [Monday/Tuesday/etc]
week: YYYY-WXX
mcps_used: [Calendar, Gmail, Linear, Analytics]
---

# Daily Plan - [Day], [Month] [DD], [YYYY]

## TL;DR

- **Meetings:** [X] today ([Y] require prep)
- **P0 Tasks:** [Z]
- **Key Focus:** [One sentence - primary objective for the day]

---

## Strategic Context

**This Quarter's North Star:** [from strategy/]
**This Week's Priority:** [from weekly plan]

**Active Initiatives:**
| Initiative | Stage | Next Milestone | Owner |
|------------|-------|----------------|-------|
| [PRD Name] | [Stage] | [Next step] | [You/Team] |

---

## Today's Three

*If I only accomplish three things today:*

1. [ ] **[P0 Task/Meeting Outcome]** - Advances [Initiative/Priority]
2. [ ] **[P0 Task/Meeting Outcome]** - Unblocks [Team/Person]
3. [ ] **[Important Decision/Document]** - Aligns [Stakeholders]

*Why these three:*
- [Brief rationale for prioritization]

---

## Schedule & Meeting Prep

| Time | Meeting | Attendees | Prep Status | Context |
|------|---------|-----------|-------------|---------|
| 9:00am | [Topic] | [Names] | ✅ Ready / ⚠️ Needs prep | [Last met: Date, discussed: Topic] |
| 11:00am | [Topic] | [Names] | ✅ Ready | [Open items: Action 1, Action 2] |
| 2:00pm | [Topic] | [Names] | ⚠️ Needs prep | [New stakeholder - review profile] |

### Free Blocks

- **9:45am - 10:45am** (1 hour) → Suggested: [Deep work on P0 task]
- **12:00pm - 1:00pm** (1 hour) → Lunch + email catch-up
- **3:30pm - 5:00pm** (1.5 hours) → Suggested: [PRD review / Async work]

---

## Meeting Context

### 9:00am - [Meeting Title]

**Attendees:**
- **[Name]** ([Role]) - [Communication style from profile]
  - Last interaction: [Date] - Discussed [Topic]
  - Open items: [You owe them X, They owe you Y]
  - Context: [Why this meeting matters today]

**Prep needed:**
- [ ] [Specific prep item]
- [ ] [Specific prep item]

**Your goal for this meeting:**
- [Clear objective - decision to make, alignment to get, feedback to gather]

---

### 11:00am - [Meeting Title]

**Attendees:**
- **[Name]** ([Role])
  - [Context...]

[Repeat for each meeting]

---

## Tasks by Priority

### P0 - Must Do Today

- [ ] **[Task from Linear]** - [Why urgent / Who's blocked]
  - Context: [Relevant PRD, stakeholder, deadline]
  - Time estimate: [X hours]
  - Suggested time: [Specific free block]

### P1 - Important This Week

- [ ] **[Task]** - [Why it matters]
  - Advances: [Weekly priority / Quarter goal]
  - Can defer to: [Tomorrow/Day X if needed]

### P2 - If Time Allows

- [ ] **[Task]** - [Nice-to-have / Low urgency]

---

## Metrics to Watch

[Only include if features launched recently]

### [Feature Name] (Launched [Date])

**Success Criteria (from PRD):**
- [Metric 1]: Target [X], Current [Y] ([+/- %])
- [Metric 2]: Target [A], Current [B] ([+/- %])

**Status:** ✅ On track / ⚠️ Needs attention / ❌ Below target

**Action needed:**
[If metrics concerning, suggest next step]

---

## Email/Communication Highlights

[Only if Gmail/Slack MCP provided important context]

**Needs Response:**
- **From [Name]:** [Subject] - [Why important]
- **Thread with [Team]:** [Topic] - [Decision needed]

**FYI (context for meetings):**
- [Email/thread that provides background for today's discussions]

---

## Heads Up

⚠️ **Potential Issues:**

- **Back-to-back meetings 9am-12pm** - No break, may run over
- **P0 task "[Task]" has no time blocked** - Risk of not completing
- **Metrics for [Feature] trending down** - May need discussion in [Meeting]
- **Waiting on [Stakeholder] decision for [PRD]** - Follow up if not addressed
- **[Person] expects [Deliverable] today** - Currently not in Top 3

**Recommendations:**
- [Specific suggestion to address each issue]

---

## Consider Delegating

**Delegation Section Trigger Logic:**

Include this section when ANY of these are true:
- PM's role is VP, Director, or Head of [function] (check `context-library/personal-context-pm-background.md` or `context-library/business-info-template.md`)
- PM has direct reports or manages PM leads (check stakeholder profiles for reports)
- PM explicitly asks for delegation suggestions

Skip this section when:
- PM is an IC (Individual Contributor) PM with no reports
- PM's role level is unclear -- ask before including: "Do you manage any direct reports? I can add delegation suggestions if helpful."

When including, add a brief note explaining why: *"Including delegation suggestions because you manage [X] direct reports."*
When excluding, no note needed -- just omit the section silently.

These tasks from today's list could be handled by someone on your team:

| Task | Suggested Delegate | Why | What You'd Still Own |
|------|-------------------|-----|---------------------|
| [Task] | [Name from stakeholder profiles] ([Role]) | [They have context / skill / capacity] | [Review/approve/unblock] |
| [Task] | [Name] ([Role]) | [Reason] | [Your remaining piece] |

**Delegation tip:** Delegating doesn't mean disappearing. Stay available for questions and set a check-in time.

---

## Strategic Alignment Check

**How today advances weekly priorities:**
- Priority 1: [How today's work contributes]
- Priority 2: [How today's work contributes]
- Priority 3: [Coverage gap or not addressed today]

**Quarter goals progress:**
- [If today's work moves any goal forward, note it]

---

*Generated: [Timestamp]*
*MCPs used: [List which MCPs provided data]*
*Next: Run `/meeting-notes` after meetings to capture outcomes*
```

---

## Output Quality Self-Check

Before presenting the daily plan, verify:

- [ ] **Carry-over checked:** If yesterday's plan exists, deferred items are surfaced at the top
- [ ] **Today's Three is realistic:** Account for meeting load (heavy meeting day = Today's Two)
- [ ] **Every meeting has context:** At minimum, attendee names and one line of context per meeting
- [ ] **P0 tasks have time blocked:** If a P0 has no free block assigned, flag it in Heads Up
- [ ] **Compact mode is compact:** Default output fits on one screen (TL;DR + Top 3 + Schedule + Heads Up)
- [ ] **Stakeholder profiles used:** If profiles exist, attendee context references them (not generic)
- [ ] **Strategic alignment present:** At least one task or meeting connects to weekly/quarterly goals
- [ ] **Delegation section:** Included with stated reason (e.g., "you manage 3 reports") OR excluded because PM is IC / no reports found
- [ ] **File saved:** Plan saved to `outputs/daily-plans/YYYY-MM-DD-daily-plan.md`

---

### Step 5: Output & Next Actions

1. **Save the daily plan file**

2. **Display summary to user:**
   - "Your daily plan is ready! [X] meetings, [Y] P0 tasks, focus on [Z]."
   - If heavy meeting day: "Heads up: Back-to-back meetings today. I've reduced to 'Today's Two' for realism."
   - If metrics flagged: "Metrics for [Feature] need attention - I've noted it in the plan."

3. **Offer follow-up actions:**
   - "Need meeting prep for any specific meeting? I can help draft talking points."
   - "Want me to create Linear tasks for anything not tracked yet?"
   - If no weekly plan: "This week isn't planned yet. Run `/weekly-plan` to set priorities?"

---

## Evening Planning Variant

When user runs `/daily-plan tomorrow`:

1. **Pull tomorrow's calendar** (same process)
2. **Review today's plan:**
   - Check what got done (if daily plan exists for today)
   - Identify what's carrying over
3. **Generate tomorrow's draft plan**
4. **Save as:** `outputs/daily-plans/YYYY-MM-DD-draft.md`
5. **Prompt:** "Tomorrow's plan is ready. Want to adjust priorities before end of day?"

---

## Integration Setup Guides

### Setup Path 1: MCP Servers (Recommended)

**Google Calendar MCP:**
```
1. Run: /connect-mcps connect to google-calendar
2. I'll first check for official remote MCP server
3. If remote server available: Guide you to use `claude mcp add --transport http`
4. If not: Walk you through OAuth setup (credentials from Google Cloud Console)
5. Test: I'll fetch today's events to confirm it works
6. Done! Future /daily-plan calls will auto-fetch meetings
```

**Gmail MCP:**
```
1. Run: /connect-mcps connect to gmail
2. Similar priority: Check remote server first, then OAuth flow
3. Permissions needed: Read email (not send)
4. I'll fetch unread/important emails for daily context
```

**Linear/Jira MCP:**
```
1. Run: /connect-mcps connect to linear (or jira)
2. I'll check for remote servers, then fall back to API keys
3. You'll need: API key from Linear/Jira settings (if no remote server)
4. I'll query your assigned tasks daily
```

**Analytics MCP (Amplitude/Mixpanel):**
```
1. Run: /connect-mcps connect to amplitude (or mixpanel)
2. I'll check remote servers first, then manual setup
3. You'll need: API key + Project ID (if manual)
4. I'll pull metrics for recently launched features
```

**Priority order:** Remote servers > Local servers > Manual OAuth/API tokens

---

### Setup Path 2: Direct API Access

If MCPs aren't available, I can call APIs directly using Bash/Python.

**Google Calendar API Setup:**

```bash
# Step 1: Get API credentials
# Go to: https://console.cloud.google.com/apis/credentials
# Create OAuth 2.0 Client ID → Download JSON

# Step 2: I'll help you authenticate
# Run this (I'll guide you):
python3 -c "
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import datetime

# Auth flow
flow = InstalledAppFlow.from_client_secrets_file(
    'credentials.json',
    scopes=['https://www.googleapis.com/auth/calendar.readonly']
)
creds = flow.run_local_server(port=0)

# Test: Fetch today's events
service = build('calendar', 'v3', credentials=creds)
now = datetime.datetime.utcnow().isoformat() + 'Z'
events_result = service.events().list(
    calendarId='primary',
    timeMin=now,
    maxResults=10,
    singleEvents=True,
    orderBy='startTime'
).execute()

for event in events_result.get('items', []):
    print(f\"{event['start'].get('dateTime', event['start'].get('date'))} - {event['summary']}\")
"

# Step 3: Save credentials
# I'll store the token for future use
```

**Once set up:**
- I run this script each time `/daily-plan` is called
- Parse the output and integrate into your plan
- No manual work after initial setup

**Linear API Setup:**

```bash
# Step 1: Get API key
# Go to: Linear Settings → API → Personal API Keys → Create

# Step 2: Test query
curl https://api.linear.app/graphql \
  -H "Authorization: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "{ viewer { assignedIssues(filter: { state: { type: { nin: [\"completed\", \"canceled\"] } } }) { nodes { title priority state { name } } } } }"
  }'

# Step 3: I'll parse and format tasks
```

**I'll help you:**
1. Get the API key
2. Test the first call
3. Set up a script I can run daily
4. Parse results into your daily plan

---

### Setup Path 3: Export/Import Workflow

**For Google Calendar:**

```
1. Open Google Calendar
2. Click today's date
3. Click ⋮ (three dots) → "Print"
4. Save as PDF or take screenshot
5. Share the file/screenshot with me
6. I'll parse it using vision and extract:
   - Meeting times
   - Attendees
   - Meeting titles
```

**For Linear/Jira:**

```
1. Go to your Linear/Jira board
2. Filter: Assigned to you, Status != Done
3. Export to CSV (or screenshot the view)
4. Share CSV/screenshot
5. I'll extract tasks and priorities
```

**For Gmail:**

```
1. Search: is:unread OR is:important (in Gmail)
2. Screenshot the list
3. Share with me
4. I'll identify which emails need attention today
```

**For Analytics (Amplitude/Mixpanel):**

```
1. Open your key dashboard
2. Screenshot the metrics for recently launched features
3. I'll analyze with vision and extract:
   - Metric values
   - Trends (up/down)
   - Anomalies
```

**Trade-off:**
- Manual (1-2 min each morning)
- But works immediately, no API setup needed
- Good for testing before committing to automation

---

### Setup Path 4: Browser Automation

If you have Claude in Chrome MCP installed:

```
1. I can open tabs and navigate to your tools
2. Extract data directly from the web UI
3. Parse and integrate into daily plan
```

**Example flow:**
```
When you run /daily-plan:
1. I open Google Calendar in browser
2. Navigate to today's view
3. Scrape meeting list
4. Open Linear/Jira in new tab
5. Navigate to your assigned tasks
6. Scrape task list
7. Close tabs and generate plan
```

**Setup required:**
```
1. Ensure Claude in Chrome MCP is installed
2. Stay logged into Google Calendar, Linear, etc. in Chrome
3. Give me permission to access these tabs
4. I'll automate the rest
```

**Trade-off:**
- Semi-automated (better than manual, simpler than APIs)
- Requires Chrome MCP
- Works even if tools don't have APIs

---

### Setup Path 5: Manual Input (Zero Setup)

If no integrations available, I'll ask focused questions:

```
When you run /daily-plan, I ask:

1. "What meetings do you have today?"
   → You: "9am product sync, 2pm stakeholder review"

2. "Who's attending each?"
   → You: "Product sync: Sarah, John. Stakeholder review: VP Eng"

3. "What P0 tasks are on your plate?"
   → You: "Finish PRD for X, review metrics for Y"

4. "Any metrics you need to check?"
   → You: "Feature Z launched Monday, check adoption"

5. "Anything urgent from email/Slack?"
   → You: "Customer escalation from Support team"

Total time: 2 minutes
```

**I'll then:**
- Look up Sarah, John, VP Eng in stakeholder profiles (if exists)
- Check PRD X in `outputs/prds/`
- Find Feature Z in `context-library/launches/`
- Generate full daily plan with all context

**Trade-off:**
- No setup required
- Takes 2 min of your time each morning
- Still provides structure and context

---

### Recommended Setup Strategy

**Week 1: Start Manual**
- Run `/daily-plan` with manual input
- See the value (what it surfaces, how it helps)
- Identify which data source is most valuable to you

**Week 2: Add One Integration**
- Pick the highest-value integration (usually Calendar)
- Set up via easiest path (export workflow or API)
- Run `/daily-plan` with partial automation

**Week 3: Expand Integrations**
- Add Linear/Jira (task management)
- Add Gmail (email context)
- Now 80% automated

**Week 4: Full Automation**
- Add Analytics MCP
- Add Slack MCP
- Run `/daily-plan` → full plan in seconds

**Philosophy:**
- Start simple, layer on automation
- Don't let perfect setup block initial value
- Each integration makes the next easier

---

## MCP Graceful Degradation

**If Calendar MCP not connected:**
- Prompt: "I don't have calendar access. What meetings do you have today?"
- Or: "I can read from a manual calendar file if you have one."
- Offer: "Want to connect Google Calendar? Run `/connect-mcps connect to google-calendar`"

**If Gmail MCP not connected:**
- Skip email section or ask: "Any important emails I should factor into today's plan?"
- Offer: "Want email context in future? Run `/connect-mcps connect to gmail`"

**If Linear/Jira MCP not connected:**
- Scan `outputs/meeting-notes/` for unchecked action items
- Ask: "What tasks are on your plate today?"

**If Analytics MCP not connected:**
- Note: "Metrics check needed for [Feature] - I don't have analytics access"
- Suggest: "Check your dashboard for [Feature] metrics manually"

**If Stakeholder profiles don't exist:**
- Generate basic meeting list without context
- Suggest: "Want richer meeting context? Fill out stakeholder profiles in `context-library/`"

---

## Integration with Other Skills

**Before `/daily-plan`:**
- `/weekly-plan` - Sets weekly priorities that inform today's focus

**After `/daily-plan`:**
- `/meeting-notes` - Capture outcomes from today's meetings
- `/create-tickets` - Convert action items to Linear/Jira tasks
- `/daily-review` - (If created) Reflect on what got done

**Parallel use:**
- `/prd-draft` - Today's work might include PRD writing
- `/prototype` - Today might be prototype iteration day

---

## Tips for Best Results

**First time setup:**
1. Connect Calendar MCP first (most important)
2. Connect Gmail MCP for communication context
3. Connect Linear/Jira for task tracking
4. Fill out stakeholder profiles for top 5 people you work with

**Daily ritual:**
- Run `/daily-plan` first thing in morning (before email/Slack)
- Review in < 5 minutes
- Use as north star for the day
- Resist adding tasks mid-day (unless true P0)

**Weekly rhythm:**
- Monday: Run `/weekly-plan` before `/daily-plan`
- Tuesday-Thursday: Just `/daily-plan`
- Friday: `/daily-plan` then `/weekly-review` at end of day

**Power user moves:**
- Evening before: Run `/daily-plan tomorrow` to prep
- Heavy meeting day: Block 15 min before each meeting for prep
- Light meeting day: Use free blocks for deep work (PRD writing, strategy)

---

## Related Skills

**Before this:**
- `/weekly-plan` - Set weekly priorities
- `/connect-mcps` - Connect to Calendar, Gmail, Linear

**After this:**
- `/meeting-notes` - Capture meeting outcomes
- `/create-tickets` - Track action items
- `/weekly-review` - End-of-week synthesis

**Parallel use:**
- `/prd-draft` - Write PRDs during free blocks
- `/impact-sizing` - Analyze features during planning time
