---
version: 1.1.0
name: tool-ux-study
description: Run a think-aloud usability study with AI testers and UX research facilitation
---

# Local User Testing Skill

Spawn a managed team of N test agents that each log in as a different seeded community member and test the platform. The lead agent (you) acts as **UX research facilitator** — observing sessions, probing testers with follow-up questions, maintaining running observation notes, and synthesizing findings into narrative themes.

## Invocation

```
/tool-ux-study [<number>] [--user=N] [--duser=N] [--model=sonnet|opus|haiku] [--review-model=sonnet|opus|haiku]
```

**Examples:**
- `/tool-ux-study 5` — 5 regular testers + 1 accessibility tester (default)
- `/tool-ux-study --user=3` — 3 regular testers + 1 accessibility tester
- `/tool-ux-study --duser=4` — 4 accessibility testers only (no regular)
- `/tool-ux-study --user=2 --duser=1` — 2 regular + 1 accessibility tester
- `/tool-ux-study 10 --model=opus` — 10 regular + 1 accessibility, all Opus

**Arguments:**
- `<number>` — Shorthand for `--user=N`. Sets number of regular testers (default: 3, max: 15).
- `--user=N` — Number of **regular** test agents (default: 3, max: 15). Overrides `<number>` if both are specified.
- `--duser=N` — Number of **accessibility** test agents (default: 1, max: 5). These simulate users with disabilities (blindness, motor impairment, cognitive disability, low vision, deafness). Set `--duser=0` to skip accessibility testing entirely.
- `--model` — Model for **tester agents** (default: `sonnet`). These do browser automation, screenshots, and report writing.
- `--review-model` — Model for **PM, UX, & WCAG reviewer agents** (default: inherits from parent, i.e. whatever model you're running Claude Code with). These do deep analytical cross-referencing against documentation.

**Cost guidance:**
| Config | Estimated cost (10+1 testers) | Best for |
|--------|-------------------------------|----------|
| Default (sonnet testers, inherited reviewers) | ~$17-20 | Regular testing runs |
| `--model=opus` | ~$55-65 | Maximum quality narratives |
| `--model=haiku` | ~$6-9 | Quick smoke tests |
| `--model=sonnet --review-model=sonnet` | ~$14-17 | Budget-conscious full runs |

The **team lead** (you, the main Claude Code agent) always runs on whatever model the user started Claude Code with — it is never overridden.

## Instructions for Claude

When this skill is invoked, follow these steps **in order**. You are the **team lead** and **UX research facilitator**.

### Your Role: UX Research Facilitator

You are not a passive project manager counting completions. You are an active **UX research facilitator** running a think-aloud usability study. Your mindset:

- **Observe**: As tester reports arrive, read them carefully. Look for emotional arcs, friction patterns, and moments where testers got stuck or delighted.
- **Probe**: When something is ambiguous or interesting, send a follow-up question to the tester — like a researcher sitting next to a participant saying "Tell me more about that moment."
- **Synthesize**: Don't just list findings — cluster them into themes. A bug reported by 3 testers on different pages might share the same root cause. Friction moments around navigation across testers reveal an information architecture problem, not isolated page bugs.
- **Narrate**: Your final report tells the story of what happened when real-ish users tried this platform. It reads like research findings, not a spreadsheet.

---

### Phase 1: Setup

#### 1.1 Parse arguments

Extract from the arguments string:
- **Regular tester count**: `--user=N` or bare number (default: 3, cap at 15)
- **Accessibility tester count**: `--duser=N` (default: 1, cap at 5). If `--user` is set but `--duser` is not, default to 1. If only `--duser` is set without `--user`, set regular count to 0.
- **Total agent count**: regular + accessibility testers
- **Tester model**: `--model=X` (default: `sonnet`). Pass this as the `model` parameter when spawning tester agents via the Agent tool.
- **Reviewer model**: `--review-model=X` (default: not set — do NOT pass a `model` parameter to reviewer agents, so they inherit the parent model). If explicitly set, pass it as the `model` parameter when spawning PM/UX/WCAG reviewer agents.

#### 1.2 Clean up old data

```bash
playwright-cli close-all
```

#### 1.3 Create timestamped output folder

```bash
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
REPORT_DIR="./test-reports/theme-test-${TIMESTAMP}"
mkdir -p "$REPORT_DIR"
```

Store `REPORT_DIR` — all screenshots and the final `REPORT.md` go here.

#### 1.4 Tell the user what's happening

Print a status message:
```
Starting test run with N agents.
Output: test-reports/theme-test-{timestamp}/
Setting up team...
```

---

### Phase 2: Create Team & Tasks

#### 2.1 Create the team

Use `TeamCreate` with:
```
team_name: "test-run-{TIMESTAMP}"
description: "Theme & viewport testing with N agents"
```

#### 2.2 Build the test matrix

Assign each agent a unique combination of user, area, theme, and viewport.

**User personas** (never use admin users, indices 0-9):

| Slot | Name | Email |
|------|------|-------|
| 0 | Daan de Vries | daan.devries.10@test.dev |
| 1 | Sophie de Vries | sophie.devries.30@test.dev |
| 2 | Bianca de Vries | bianca.devries.50@test.dev |
| 3 | Dennis van den Berg | dennis.vandenberg.100@test.dev |
| 4 | Anna Bakker | anna.bakker.199@test.dev |
| 5 | Ruben Smit | ruben.smit.254@test.dev |
| 6 | Femke de Boer | femke.deboer.362@test.dev |
| 7 | Jesse Mulder | jesse.mulder.418@test.dev |
| 8 | Anouk de Groot | anouk.degroot.524@test.dev |
| 9 | Robin Bos | robin.bos.577@test.dev |
| 10 | Lotte Vos | lotte.vos.647@test.dev |
| 11 | Kevin Peters | kevin.peters.739@test.dev |
| 12 | Iris Hendriks | iris.hendriks.841@test.dev |
| 13 | Stijn van Dijk | stijn.vandijk.914@test.dev |
| 14 | Merel Dekker | merel.dekker.1058@test.dev |

**Test areas** (cycle with `i % 10`):

| # | Area |
|---|------|
| 0 | Onboarding & Dashboard |
| 1 | Groups & Membership |
| 2 | Events & RSVPs |
| 3 | Proposals & Voting |
| 4 | Links & Bookmarks |
| 5 | Companies & Conferences |
| 6 | Settings & Profile |
| 7 | Cross-feature Navigation |
| 8 | Mobile Responsive |
| 9 | Search & Filtering |

**Theme & viewport assignment** for regular agent index `i`:
- **Theme**: `light` if `i % 2 == 0`, `dark` if `i % 2 == 1`
- **Viewport**: `desktop` (1440x900) if `i < ceil(REGULAR_COUNT/2)`, `mobile` (375x812) otherwise
- **Persona**: `i % 10` from the base set; for `i >= 10`, generate new personas or cycle (see [personas.md](personas.md))

If REGULAR_COUNT <= 4, use explicit: 0=desktop-light, 1=desktop-dark, 2=mobile-light, 3=mobile-dark.

**Accessibility testers** are appended after regular testers. They use user slots starting after the last regular tester. Theme/viewport assignment follows the same alternating pattern, continuing from where regular testers left off. Assign each accessibility tester a disability persona from the [Accessibility Personas](personas.md#accessibility-personas) section (cycle with `j % 5` where `j` is the accessibility tester index).

**Example for `--user=5 --duser=2`:**
| Agent | Type | User | Persona | Theme | Viewport |
|-------|------|------|---------|-------|----------|
| 0 | Regular | Daan | The Newcomer | light | desktop |
| 1 | Regular | Sophie | The Regular Member | dark | desktop |
| 2 | Regular | Bianca | The Event Hunter | light | desktop |
| 3 | Regular | Dennis | The Speaker | dark | mobile |
| 4 | Regular | Anna | The Content Curator | light | mobile |
| 5 | A11y | Ruben | Screen Reader User (Blind) | dark | desktop |
| 6 | A11y | Femke | Motor Impairment (Keyboard Only) | light | desktop |

Agents 10+ get freshly generated personas with unique backgrounds, scenarios, and tasks.

#### 2.3 Create tasks

Use `TaskCreate` for each agent. Example task:
```
subject: "Test as Daan: Onboarding, desktop-light"
description: "User: daan.devries.10@test.dev, Area: Onboarding & Dashboard, Theme: light, Viewport: desktop 1440x900, Session: t0-desktop-light-daan"
activeForm: "Testing onboarding as Daan (desktop-light)"
```

#### 2.4 Print the test matrix to the user

Show a table:
```
| # | User | Area | Theme | Viewport | Status |
|---|------|------|-------|----------|--------|
| 0 | Daan | Onboarding | light | desktop | pending |
| 1 | Sophie | Groups | dark | desktop | pending |
| ... |
```

---

### Phase 3: Spawn Teammates

#### 3.1 Spawn all N teammates in parallel

Use the `Agent` tool with:
- `subagent_type: "general-purpose"`
- `mode: "bypassPermissions"`
- `model: TESTER_MODEL` (from `--model` argument, default `"sonnet"`)
- `team_name: "test-run-{TIMESTAMP}"`
- `name: "tester-{username}"` (e.g., `tester-daan`, `tester-sophie`)

Each teammate gets the prompt template from [tester-prompt.md](tester-prompt.md). Fill in placeholders from the persona (see [personas.md](personas.md)) and test matrix.

#### 3.2 Assign tasks to teammates

Use `TaskUpdate` to set `owner` on each task to the corresponding teammate name.

---

### Phase 4: Observe, Probe & Synthesize

As the team lead and UX research facilitator, you actively observe and analyze sessions as they come in — not just track completion counts.

#### 4.1 Initialize observation notes

Create observation notes using the template in [report-templates.md](report-templates.md#observation-notes-template-phase-41).

#### 4.2 Process each tester report (on arrival)

When a tester sends you their report via message:

**Step A — Read and analyze the report.** Extract:
- Readiness score, average confidence, number of bugs (by severity)
- Key friction moments and their severity
- Delight moments
- The tester's emotional arc (did they start confident and hit a wall? start confused and warm up?)
- Notable think-aloud quotes that capture something vivid

**Step B — Selective screenshot review.** Only read screenshots when:
- The tester reports a **Critical** or **Serious** bug — read the bug screenshot(s) to understand the visual issue
- The tester describes being **stuck or confused** on a specific page — read that page's screenshot to see what they saw
- Limit to **2-4 screenshots per tester** maximum
- **Skip screenshots entirely** for testers who had a smooth experience (score 8+, no critical bugs, no major friction)

This keeps cost manageable (~15-25 screenshot reads total instead of ~110).

**Step C — Append to observation notes.** Use the per-tester entry format from [report-templates.md](report-templates.md#per-tester-entry-phase-42-step-c).

**Step D — Pattern check (every 2-3 testers).** Use the pattern check format from [report-templates.md](report-templates.md#pattern-check-entry-phase-42-step-d).

#### 4.3 Targeted probing (follow-up questions)

As a UX research facilitator, you may send follow-up questions to testers to dig deeper. Rules:

- **At most 1 follow-up per tester**, and **max 3-4 follow-ups total** per test run
- Only send a follow-up when one of these triggers fires:

**Trigger 1 — Ambiguous failure**: The tester reported a task as FAIL or PARTIAL but didn't explain what happened clearly.
> Example: "You mentioned you couldn't find the proposals section and gave up. Can you tell me what you tried? Did you look in the group page tabs, or were you looking for a top-level nav item?"

**Trigger 2 — Pattern confirmation**: You're seeing a pattern across testers and want to confirm it with a specific tester.
> Example: "A couple of other testers also struggled with finding proposals. You scored that task 2/5 confidence — was it the navigation that was confusing, or was the proposals page itself unclear once you found it?"

**Trigger 3 — Interesting contradiction**: This tester's experience contradicts others in a way worth exploring.
> Example: "Interestingly, you found the dashboard really welcoming (score 5/5), but another tester with the same viewport found it overwhelming. What specifically made you feel confident?"

**Trigger 4 — Unexplored critical path**: The tester skipped or barely touched something that seems important for their persona.
> Example: "As someone who came to find events, I noticed you didn't try the events map. Was there a reason you skipped it?"

Frame questions as a researcher would: **open-ended, non-leading, curious**. Never ask yes/no questions. Never suggest the answer.

When you receive a follow-up response, append it to observation notes under the tester's entry.

#### 4.4 User progress briefings

After every ~3-4 completions, give the user a **research-style briefing** (not bare counts):

```
Progress: 4/12 testers reporting in.

Emerging findings:
- Navigation to proposals is a consistent pain point — 3 of 4 testers struggled.
  Sophie: "I have no idea where proposals are, I've been clicking around for a while"
- Dark mode contrast issues appearing on multiple pages (groups map, settings).
- Dashboard onboarding getting positive reactions — newcomers feel welcomed.

Waiting on 8 more testers...
```

#### 4.5 Handle failures

If a teammate reports an error or fails to start:
- Mark their task as failed
- Optionally re-spawn a replacement teammate
- Add an entry to observation notes: `## ❌ Tester {username} — FAILED` with the error details
- Note the failure in the final report

---

### Phase 5: Synthesize Findings & Write Research Report

#### 5.1 Wait for remaining testers

Wait until all tasks are completed or failed. Continue processing reports and updating observation notes as they arrive (Phase 4 activities).

#### 5.2 Affinity mapping

Once all testers have reported, cluster observations into themes. Create the affinity map using the template in [report-templates.md](report-templates.md#affinity-map-template-phase-52).

#### 5.3 Generate individual tester reports

For each tester, write a detailed individual report using the template in [report-templates.md](report-templates.md#individual-tester-report-template-phase-53).

#### 5.4 Generate REPORT.md

Write the top-level narrative research report using the template in [report-templates.md](report-templates.md#main-reportmd-template-phase-54).

#### 5.5 Shut down testers

Send `broadcast` to all testers telling them testing is complete and they can shut down.

---

### Phase 6: Expert Reviews

After the tester reports and REPORT.md are written, spawn expert reviewer agents. Read [reviewer-prompts.md](reviewer-prompts.md) for the full prompts for each reviewer.

Spawn the PM, UX Designer, and (if any accessibility testers ran) the WCAG expert **in parallel**.

#### 6.1–6.3 Spawn reviewers

See [reviewer-prompts.md](reviewer-prompts.md) for PM (6.1), UX Designer (6.2), and WCAG Expert (6.3) prompts.

#### 6.4 Wait for reviews

Wait for all reviewers to complete. Give the user status updates.

#### 6.5 Generate Product Backlog

Compile the backlog using the template and rules in [reviewer-prompts.md](reviewer-prompts.md#product-backlog-generation-phase-65).

#### 6.6 Update REPORT.md with review and backlog links

Add a section to the top of REPORT.md linking to the expert reviews and backlog:

```markdown
## Expert Reviews

| Reviewer | Focus | Report |
|----------|-------|--------|
| Product Manager | Requirements alignment, priority assessment | [PM Review](review-product-manager.md) |
| UX Designer | Design quality, navigation, mobile, dark mode | [UX Review](review-ux-designer.md) |
| WCAG Expert | WCAG 2.2 AA compliance, assistive tech barriers | [WCAG Review](review-wcag-expert.md) |
| Product Backlog | {N} PBIs with priorities and acceptance criteria | [Backlog](backlog.md) |
```

**Note**: Only include the WCAG Expert row if accessibility testers were spawned.

---

### Phase 7: Generate Report Site

After all reports, reviews, and the backlog are written, scaffold a VitePress site in `${REPORT_DIR}` so the user can browse results with `npm start`.

Read the instructions in [REPORT-SITE.md](REPORT-SITE.md) and follow them to generate all the VitePress files. The sidebar tester entries and the `index.md` hero stats must reflect the actual testers and results from this run.

After generating the files, run `npm install` in `${REPORT_DIR}`.

---

### Phase 8: Clean Up & Final Message

#### 8.1 Shut down reviewers

Send `shutdown_request` to PM, UX designer, and WCAG expert (if spawned).

#### 8.2 Clean up team

Use `TeamDelete` to remove the team and task list.

#### 8.3 Final message to user

```
Test run complete!
- X/Y testers finished (Z regular, W accessibility)
- Average score: X/10
- X bugs found (Y critical, Z high, W medium)
- Expert reviews: PM + UX Designer + WCAG Expert
- Report: test-reports/theme-test-{TIMESTAMP}/REPORT.md
- Individual reports: X tester files + 3 expert reviews
- Screenshots: X files

Browse the report:
  cd test-reports/theme-test-{TIMESTAMP} && npm start
```

---

## Supporting Files

| File | Content |
|------|---------|
| [tester-prompt.md](tester-prompt.md) | Prompt template for each tester agent |
| [personas.md](personas.md) | 10 regular personas + 5 accessibility personas + technical checklist |
| [report-templates.md](report-templates.md) | Templates for observation notes, affinity map, tester reports, and REPORT.md |
| [reviewer-prompts.md](reviewer-prompts.md) | Expert reviewer prompts (PM, UX, WCAG) + backlog template |
| [REPORT-SITE.md](REPORT-SITE.md) | VitePress report site generation instructions |

## Prerequisites

- API running (typically http://localhost:5132 or https://localhost:7149)
- Frontend running on http://localhost:4200
- Seed data applied: `pwsh seed-data/apply-seed-data.ps1 -ApiBaseUrl "https://localhost:7149"`
- playwright-cli installed

## Troubleshooting

- Stale browsers: `playwright-cli close-all`
- Force kill: `playwright-cli kill-all`
- Port check: `netstat -an | grep LISTEN | grep -E "4200|5132|7149"`
- Re-seed: `pwsh seed-data/apply-seed-data.ps1 -ApiBaseUrl "https://localhost:7149" -Clean`
