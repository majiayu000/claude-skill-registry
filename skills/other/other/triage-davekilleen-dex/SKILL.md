---
name: triage
description: Strategically route orphaned files and extract scattered tasks
model_hint: fast
---

Cleanup and routing tool that finds standalone files and scattered tasks, then suggests where they belong using your current strategic context (Week Priorities + Quarterly Goals).

## Execution Style

This skill handles quick decisions. Be concise. Don't over-analyze. Make a routing decision and move on. Target: <2 seconds of thinking per item.

## What It Does

- **Files**: Routes standalone files in `00-Inbox/` to projects, person pages, or resource folders
- **Tasks**: Finds unchecked `- [ ]` tasks scattered across notes and routes them appropriately
- **Strategic**: Uses your Week Priorities and Quarterly Goals to inform routing confidence

## Usage

- `/triage` - Process everything (files + tasks)
- `/triage files` - Organize standalone files only
- `/triage tasks` - Extract and route tasks only

## Arguments

$MODE: Optional. "files" | "tasks" | "all". Default: "all"

---

---

## Demo Mode Check

Before executing, check if demo mode is active:

1. Read `System/user-profile.yaml` and check `demo_mode`
2. **If `demo_mode: true`:**
   - Display: "Demo Mode Active — Using sample data"
   - Use `System/Demo/` paths instead of root paths
   - Write any output to `System/Demo/` subdirectories
3. **If `demo_mode: false`:** Use normal vault paths


## Step 0: Load Strategic Context & Structure Discovery

Before processing inbox items, load strategic context and build an index of existing entities. This makes triage strategically aware and enables intelligent routing.

### 0. Load Strategic Context

Read these files to understand current priorities:

1. **Week Priorities**: `00-Inbox/Week_Priorities.md`
   - Extract this week's Top 3 focus items
   - Note any specific projects/people mentioned
   - Capture keywords and themes

2. **Quarterly Goals**: `03-Tasks/Quarterly_Goals.md`
   - Extract current quarter's goals
   - Note associated projects and outcomes
   - Capture keywords and themes

This context will inform routing decisions - entries matching current priorities get higher confidence scoring and are surfaced first.

### 1. Scan Projects

List all files in `04-Projects/`:
- Extract project name from filename (convert underscores to spaces)
- Read frontmatter if present for description, status, pillar
- Build index: `{ name, path, description, status, pillar }`

### 2. Scan People

List all files in `05-Areas/People/External/` and `05-Areas/People/Internal/`:
- Extract name from filename
- Read frontmatter/metadata table for role, company
- Build index: `{ name, path, company, role, type: internal|external }`

### 3. Scan Role-Specific Areas

List any additional folders under `05-Areas/` that aren't People or Career:
- These may be role-specific areas created during setup (e.g., Accounts/, Team/, Content/)
- Extract relevant names from filenames
- Build index: `{ name, path, type: area_type }`

### 4. Read Pillars

Parse `System/pillars.yaml`:
- Extract pillar names, descriptions, and keywords
- These inform categorization when no entity match is found

---

## Step 0.5: Semantic Matching Enhancement (if QMD available)

**This step activates automatically when QMD is installed.** It dramatically improves routing accuracy by matching inbox items to goals, projects, and people by **meaning**, not just keywords.

Check if QMD MCP tools are available by calling `qmd_status`. **If available:**

After loading strategic context (Step 0), enhance matching with semantic search:

1. **For each inbox item**, run:
   ```
   qmd_search(query="[item title + first 100 words of content]", limit=5)
   ```
   This finds vault content related by meaning. "Email about onboarding flow" matches "Q1 goal: improve activation rate" even though they share no keywords.

2. **For task deduplication**, use semantic similarity instead of keyword overlap:
   ```
   qmd_search(query="[task description]", limit=3)
   ```
   Catches semantic duplicates: "Review Q1 metrics" detected as duplicate of "Check quarterly pipeline numbers".

3. **For goal alignment scoring**, run:
   ```
   qmd_search(query="[item content]", limit=3)
   ```
   against quarterly goals and weekly priorities. Items semantically related to active goals get a +25 confidence boost.

**How this changes matching:**

| Aspect | Without QMD (keyword) | With QMD (semantic) |
|--------|----------------------|---------------------|
| Goal matching | Exact keyword overlap only | Meaning-based: "churn analysis" matches "retention goal" |
| Duplicate detection | >60% string similarity | Semantic similarity: different words, same intent |
| Person matching | Name must appear in text | Role/title references found: "the sales VP" → Sarah Chen |
| Project matching | Project name in filename | Thematic connection: "pricing update" → "Acme Deal" project |

**Merge semantic scores with entity scores** from Step 0. The combined confidence determines routing priority.

**If QMD is not available:** Skip silently. The standard keyword-based matching in the steps below handles routing with existing patterns.

---

## Mode: Files

Organize standalone files in the `00-Inbox/` folder by suggesting where they belong.

### Process

1. **Scan 00-Inbox/**
   - List all files (exclude Week Priorities.md, README.md)
   - Read each file's content

2. **Match Against Strategic Context & Entities**

   For each inbox file, check in this order:

   | Check | Match Criteria | Action | Confidence Boost |
   |-------|---------------|--------|------------------|
   | **Week Priority match** | Content relates to this week's Top 3 priorities | Route to associated project/person, flag as HIGH priority | +30 points |
   | **Quarterly Goal match** | Content relates to current quarter's goals | Route to associated project, flag as strategic | +20 points |
   | **Project match** | File mentions project name, or filename contains project reference | Route to specific project file | +10 points if also matches priority |
   | **Person match** | File is about a specific person, contains their name prominently | Route to person page OR suggest linking | +10 points if person mentioned in priorities |
   | **Company match** | File mentions company name, or attendees from known domain | Route to company page in 05-Areas/Companies/ | Base confidence |
   | **Pillar keyword match** | Content matches pillar keywords | Tag with pillar, suggest relevant category | Base confidence |
   | **No entity match** | None of the above | Fall back to category routing | Low confidence |

3. **Category Fallback Rules**

   When no specific entity matches, use these rules:

   | Destination | Criteria |
   |-------------|----------|
   | `04-Projects/` | Has deadline, specific outcome, time-bound |
   | `05-Areas/[specific area]/` | Belongs to a role-specific area (Accounts/, Team/, Content/) |
   | `05-Areas/People/` | Person-specific information |
   | `06-Resources/` | Reference material, knowledge, learnings |
   | `07-Archives/` | Old/completed, no longer active |
   | Delete | No value, redundant, or temporary |

4. **Present Suggestions with Strategic & Entity Context**

   Show what was matched, prioritizing items that align with current priorities:

   ```
   File: [filename]
   Strategic Context: [Week Priority/Q Goal if matched]
   Match: [entity type] → [specific entity name]
   Destination: [exact path]
   Confidence: [high/medium/low] ([score]/100)
   Action: [suggested action]
   ```

   **Sort order:**
   1. Items matching Week Priorities (highest confidence first)
   2. Items matching Quarterly Goals
   3. Items matching known entities (projects, people, companies)
   4. Generic category routing
   
   **Flag misalignments:**
   - If multiple entries relate to something NOT in priorities/goals, surface it: "You've captured 5 items about [topic]. Consider adding to priorities?"

5. **Execute with Confirmation**
   - Show full plan
   - Wait for user approval
   - Move files using `mv` (not copy)
   - For merges, append content to existing file

---

## Mode: Tasks

Extract uncompleted tasks from notes and route them appropriately.

### Process

1. **Scan Sources**
   - `00-Inbox/Meetings/*.md` - Meeting action items
   - `00-Inbox/*.md` - Captured tasks
   - Any file with unchecked tasks `- [ ]`

2. **Extract Tasks**
   - Find all `- [ ]` items
   - Note the source file for each
   - Extract any mentioned names, projects, companies

3. **Match Tasks to Entities**

   For each task:
   - Check if it mentions a known project → suggest adding to that project
   - Check if it mentions a known person → suggest linking to person page
   - Check if it mentions a known company → suggest linking to company

4. **Deduplication Check**

   For each task, check against:
   - `00-Inbox/Weekly_Plans.md`
   - `03-Tasks/Tasks.md`

   Flag items with >60% similarity to existing tasks.

5. **Ambiguity Detection**

   Flag tasks that are:
   - Less than 3 words
   - Match vague patterns (e.g., "fix bug", "follow up", "research X")

   Generate clarification questions for ambiguous items.

6. **Present Results**

   **Ready to Route** (clear, non-duplicate items):
   - Show suggested destination with entity context
   - Show pillar if detectable
   - Show any linked entities

   **Potential Duplicates** (>60% similarity):
   - Show the existing task it matches
   - Ask: Skip / Merge / Keep Both

   **Needs Clarification** (ambiguous):
   - Show the issue
   - Ask clarifying questions
   - Wait for user input

7. **Route with Confirmation**
   - To Week Priorities: Add to `00-Inbox/Weekly_Plans.md`
   - To Project: Add to relevant project file
   - To Person: Add to person page's action items
   - Skip: Don't process
   - Defer: Leave for later

---

## Mode: All (Default)

Process all orphaned items:
1. Load strategic context (Week Priorities + Quarterly Goals)
2. Run structure discovery (projects, people, companies)
3. Organize standalone files in `00-Inbox/`
4. Extract and route scattered unchecked tasks from all notes

---

## Example Output

```
📬 Triage Report

=== STRATEGIC CONTEXT ===
Week Priorities:
• Mobile App Launch (beta by Friday)
• Q2 Planning finalization
• Sarah's team onboarding

Quarterly Goals:
• Launch mobile app beta (Q1)
• Expand into EMEA market (Q2)
• Build product marketing team (Q1)

=== STRUCTURE DISCOVERED ===
• 4 projects found in 04-Projects/
• 12 people found in 05-Areas/People/
• 3 companies found in 05-Areas/Companies/
• 3 pillars configured

=== FILES (2) ===

1. "Screenshot 2026-01-28.png"
   Found in: 00-Inbox/
   Strategic Context: (no automatic match - image file)
   Suggested: Review manually or describe context
   
2. "Q1_Planning_Notes.md"
   Strategic Context: ✓ Week Priority "Q2 Planning" (related)
   Match: PROJECT → "Q2 Planning"
   Destination: 04-Projects/Q2_Planning.md
   Confidence: MEDIUM (70/100)
   Action: Merge into Q2 Planning project?

=== TASKS (4) ===

🎯 HIGH PRIORITY - MATCHES WEEK PRIORITIES (1):

1. "- [ ] Finalize mobile app pricing model"
   Found in: 04-Projects/Mobile_App_Launch.md
   Strategic Context: ✓ Week Priority "Mobile App Launch" + Q1 Goal
   Match: Already in correct project
   Confidence: HIGH (95/100)
   Action: Extract to Week Priorities for visibility?

📋 NEEDS ROUTING (2):

2. "- [ ] Follow up with Sarah about timeline concerns"
   Found in: random meeting note
   Strategic Context: ✓ Week Priority "Sarah's team onboarding"
   Match: PERSON → "Sarah Chen"
   Destination: Add to Sarah's person page action items
   Confidence: HIGH (85/100)

3. "- [ ] Review competitor pricing"
   Found in: scattered note
   Strategic Context: (no direct priority match)
   Match: PILLAR → "Product Strategy"
   Destination: Week Priorities or Tasks.md?
   Confidence: MEDIUM (60/100)

⚠️ DUPLICATE (1):

4. "- [ ] Reach out to Sarah"
   Found in: old meeting note
   78% match with existing task in Week Priorities
   Action: Skip / Merge / Keep both?

=== TASKS (5 items) ===

✅ READY TO ROUTE (3):
1. "Follow up with Sarah about Q1 budget"
   → Week Priorities
   Links: People/External/Sarah_Chen.md

2. "Prep slides for conference"
   → Week Priorities
   Pillar: Thought Leadership

3. "Review competitor analysis for Acme deal"
   → 04-Projects/Acme_Deal.md (project match)
   Links: 05-Areas/Companies/Acme_Corp.md

⚠️ POTENTIAL DUPLICATE (1):
4. "Contact Tom about implementation"
   → 78% match with "Reach out to Tom" in Week Priorities
   [s]kip / [m]erge / [k]eep both?

❓ NEEDS CLARIFICATION (1):
5. "Fix the bug"
   - Too vague. Which bug? What system?

---
Proceed with ready items? [y/n]
```

---

## How Structure Discovery Evolves

Because discovery happens at runtime:
- **New projects** are automatically recognized in the next triage
- **New people pages** become available for matching
- **New companies** get detected
- **Custom folders** you add are included as destinations

No configuration needed - triage adapts as your structure grows.

---

## Notes

- Never auto-route without confirmation
- Duplicates require explicit decision
- Ambiguous items block until clarified
- Use `mv` not `cp` when moving files
- Entity matches show confidence level (high/medium/low)
- Multiple entity matches are shown for user to choose

---

## Track Usage (Silent)

Update `System/usage_log.md` to mark inbox triage as used.

**Analytics (Silent):**

Call `track_event` with event_name `triage_completed` and properties:
- items_processed
- tasks_extracted
- files_routed

This only fires if the user has opted into analytics. No action needed if it returns "analytics_disabled".
