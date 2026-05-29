---
name: dex-demo
description: Toggle demo mode (see `.claude/reference/demo-mode.md`)
disable-model-invocation: false
---

Toggle demo mode on/off, reset demo content, or launch interactive demo selector.

## Usage

- `/dex-demo on` - Enable demo mode and launch interactive demo selector
- `/dex-demo off` - Disable demo mode
- `/dex-demo menu` - Show demo scenario menu (when demo mode is on)
- `/dex-demo status` - Check current mode
- `/dex-demo reset` - Restore demo content to original state

## What Demo Mode Does

When demo mode is ON:
- Commands read/write from `System/Demo/` instead of your real vault
- You see pre-populated content for a fictional PM named "Alex Chen"
- Your real data is untouched
- Changes you make are sandboxed to the demo folder

When demo mode is OFF:
- Normal operation - commands use your real vault data

## Process

### For `/dex-demo on`

1. Read `System/user-profile.yaml`
2. Set `demo_mode: true`
3. Write back to file
4. Display welcome message introducing Alex Chen persona
5. Display interactive menu with 12 validated demo scenarios
6. Wait for user to select a number (1-12)
7. Execute the selected scenario with guided walkthrough

**Welcome message template:**

```
Demo mode enabled! ✨

You're now Alex Chen, Senior Product Manager (L4) at TechCorp.

**Your current situation:**
- Working toward L5 promotion (6-9 month timeline)
- Leading mobile app launch (shipping Feb 15)
- Kicking off customer portal redesign
- Building cross-functional relationships

**Demo content includes:**
- 5 days of plans and journals (Jan 20-24)
- 3 active projects with tasks
- 6 people (colleagues and customers)
- 1 company page (Acme Corp)
- Career development system (L4→L5 path)
- Learning and improvement backlog

---

**Choose a demo scenario (1-12):**

**Daily Workflow**
1. Morning Journal - Start day with intention
2. Daily Planning - Context-aware daily plan
3. Daily Review - Capture learnings and reflect
4. Inbox Triage - Process scattered notes

**People & Context**
5. Person Lookup - See relationship tracking
6. Company Intelligence - Organization-level rollup

**Planning & Review**
7. Weekly Planning - Set Top 3 priorities
8. Weekly Review - Synthesize the week
9. Task Management - Strategic task organization

**Career Development**
10. Career System - Role, ladder, goals, evidence
11. Career Coach - Weekly reports and reflections

**System Evolution**
12. Learning & Backlog - Continuous improvement

Enter a number (1-12) or type `/dex-demo menu` to see this again.
```

### For `/dex-demo menu`

1. Check if demo mode is enabled
2. If not, error: "Demo mode is not enabled. Run `/dex-demo on` first."
3. If yes, display the same interactive menu from above (scenarios 1-12)
4. Wait for user to select a number

### For `/dex-demo off`

1. Read `System/user-profile.yaml`
2. Set `demo_mode: false`
3. Write back to file
4. Confirm: "Demo mode disabled. You're now using your real vault data."

### For `/dex-demo status`

1. Read `System/user-profile.yaml`
2. Check `demo_mode` value
3. Report current status with brief context

### For `/dex-demo reset`

1. Check if `System/Demo/_original/` exists
2. If not, error: "Demo backup not found. Cannot reset."
3. If exists, copy all from `_original/` to parent Demo folder
4. Confirm: "Demo content reset! All changes reverted to original demo state."

## Executing Demo Scenarios

When user selects a scenario number (1-12):

1. Read `.claude/reference/demo-scenarios.md` to get scenario details
2. Execute the scenario according to its definition:
   - For scenarios with commands to RUN: Execute those commands and provide guided walkthrough
   - For scenarios with files to SHOW: Read and display those files with talking points
   - For scenarios with both: Show files first, then run commands
3. After scenario completes, display the full menu again with: "Try another scenario? Enter a number (1-12):"

**Scenario execution guidelines:**

- **Scenarios 1-4, 7-8, 11-12:** Run the actual commands (`/journal`, `/daily-plan`, `/review`, `/triage`, `/week-plan`, `/week-review`, `/career-coach`, `/dex-backlog`, `/dex-whats-new`)
- **Scenarios 5-6, 9-10:** Read and display files with talking points, don't run commands
- Provide context before and after each action
- Reference the scenario's "Talking points" to guide the walkthrough
- Keep narration concise but informative

## Demo Content Overview

The demo vault represents a week in the life of Alex Chen, PM at TechCorp:

**Projects:** Mobile App Launch, Customer Portal Redesign, API Partner Program

**People:** Jordan Lee (Eng Lead), Maya Patel (Designer), Mike Rodriguez (VP Sales), Sarah Chen, Tom Wilson, Lisa Park

**Tasks:** Pre-populated across P0-P3 priorities with pillar and career tags

**Meetings:** A week of realistic meeting notes (Jan 20-24)

**Career:** Complete L4→L5 promotion path with evidence system

**Learning:** Backlog with 10 AI-ranked ideas, mistake patterns, working preferences
