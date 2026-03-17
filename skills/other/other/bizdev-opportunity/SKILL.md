---
name: bizdev-opportunity
description: Iterative BizDev Opportunity Intelligence. Analyze meeting transcripts and emails to identify opportunities using Ralph-style iterative processing with quality gates. Drafts contextual emails and proposals with closed feedback loops.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, TodoWrite, AskUserQuestion, mcp__google-drive__list_files, mcp__google-drive__export_google_doc, mcp__google-drive__get_file_content, mcp__gmail__list_emails, mcp__gmail__get_email_content, mcp__gmail__search_threads
user_invocable: true
argument-hint: <command> [--folder-id ID] [--lookback N] [--draft-emails] [--draft-proposals]
---

# BizDev Opportunity Intelligence (v2 - Iterative)

Analyze meeting transcripts and emails to identify business development opportunities. Uses Ralph-style iterative processing with quality gates, subagent delegation, and closed feedback loops to not just identify opportunities but also draft emails and proposals.

## Overview

This skill transforms from a simple scanner into an autonomous opportunity processing engine:

1. **Scan** - Extract opportunities from transcripts and emails
2. **Analyze** - Classify, score, and validate with quality gates
3. **Unify** - Cross-reference transcripts AND emails for complete context
4. **Draft** - Generate contextual emails and proposals with full relationship history
5. **Iterate** - Refine outputs until quality criteria met
6. **Compound** - Log learnings for future sessions

**NEW (v3): Master Command Center** - Anti-degradation system prevents the recurring pattern of context loss between sessions. Every session must follow the Command Center protocol. See [Command Center Protocol](#command-center-protocol) below.

**IMPORTANT - Email Drafting Rules:**
1. **Search ALL threads** - When researching a contact, search for ALL emails with that person (by email address), not just the original thread. People may have responded in separate threads.
2. **Draft in existing threads** - When drafting follow-up emails, create them as replies to the most recent thread with that contact. Never create a new thread for a follow-up.
3. **Check SENT folder** - Always verify what we've already sent to avoid duplicate outreach.

## Quick Commands

```bash
# RECOMMENDED: Refresh status and regenerate dashboard
/bizdev-opportunity refresh

# Full iterative scan with Haiku 4.5
/bizdev-opportunity scan-deep --folder-id YOUR_FOLDER_ID --lookback 6

# Resume interrupted session
/bizdev-opportunity execute

# Generate dashboard
/bizdev-opportunity report

# Search for contact context
/bizdev-opportunity context "Dr. Smith" --email james@smith.com

# View opportunity details
/bizdev-opportunity detail opp-abc123

# Prepare proposal
/bizdev-opportunity proposal opp-abc123

# Add notes to an opportunity
/bizdev-opportunity note opp-001 "Bill prefers technical details" --type approach_guidance

# Archive/unarchive opportunities
/bizdev-opportunity archive opp-001 --reason "Unresponsive"
/bizdev-opportunity unarchive opp-001
```

---

## Command Center Protocol (MANDATORY)

Every session that touches bizdev opportunities MUST follow this protocol. This prevents the recurring pattern of context loss, draft overwrites, and quality degradation.

### Session Start (always do this first)

```python
import sys
sys.path.insert(0, '.claude/skills/bizdev-opportunity')
from degradation_detector import DegradationDetector
import json

detector = DegradationDetector()
report = detector.run_health_check()
print(json.dumps(report, indent=2, default=str))

if report["has_degradation"]:
    print("⚠ DEGRADATION DETECTED - address alerts before proceeding")
    for alert in report["alerts"]:
        print(f"  [{alert['severity']}] {alert['message']}")
        print(f"  → {alert['recommendation']}")
```

### Before Generating Any Email Draft

```python
from context_registry import ContextRegistry

registry = ContextRegistry.load()
state = registry.get_or_create("opp-001", "Contact Name", "email@co.com", "Company")

# Check if context is sufficient
passed = state.evaluate_gate(require_pricing=False)
if not passed:
    print(f"BLOCKED: {state.context_gate_failures}")
    # Must gather missing context before proceeding
```

### Before Generating Any Proposal

```python
# Proposals require pricing extraction
passed = state.evaluate_gate(require_pricing=True)
if not passed:
    print(f"BLOCKED: {state.context_gate_failures}")
    # MUST search transcripts for pricing terms
```

### After Any Draft/Proposal Generation

```python
from draft_ledger import DraftLedger

ledger = DraftLedger.load()
entry = ledger.log_draft(
    opportunity_id="opp-001",
    draft_type="email",  # or "proposal"
    contact_name="Contact Name",
    content=draft_content,
    file_path=".bizdev/drafts/emails/contact.md",
    quality_result={"score": 0.85, "passed": True, "passedChecks": [...], "failedChecks": [...]}
)
ledger.save()
```

### Session End (always do this last)

```python
detector.save_snapshot()  # Save health snapshot for next session
registry.save()           # Save context state
ledger.save()             # Save draft history
```

### Key Rules

1. **NEVER** skip the health check at session start
2. **NEVER** generate a draft without verifying context completeness
3. **NEVER** generate a proposal without extracting pricing from transcripts
4. **NEVER** overwrite a draft file without logging the new version to the ledger
5. **ALWAYS** save all state files at session end

### Command Center Files

| File | Purpose | Location |
|------|---------|----------|
| `context_registry.json` | Tracks what context was gathered per opportunity | `.bizdev/command-center/` |
| `draft_ledger.json` | Version history of all drafts with quality scores | `.bizdev/command-center/` |
| `health_snapshots.json` | System health over time (30 snapshots kept) | `.bizdev/command-center/` |
| `session_log.json` | Audit trail of all actions per session | `.bizdev/command-center/` |

### Command Center Modules

| Module | Purpose |
|--------|---------|
| `context_registry.py` | Tracks context completeness per opportunity |
| `draft_ledger.py` | Versions all drafts with quality scores |
| `degradation_detector.py` | Detects system regression between sessions |
| `command_center.py` | Full orchestrator (use for complex sessions) |
| `unified_task_streams.py` | Aggregates personal, product, and professional tasks |
| `proactive_drafter.py` | Document Studio integration for auto-teed-up drafts/proposals |

### Quality Gate: Context Completeness

The new `evaluate_context_completeness` gate in `quality_gates.py` checks:
1. Was transcript searched for this contact?
2. Was email searched for this contact?
3. Was unified context generated (merged transcript + email)?
4. Was pricing extracted from transcripts? (required for proposals)
5. Is context fresh (not older than 7 days)?

This gate MUST pass before any draft/proposal generation.

---

## Unified Task Streams (v4: Multi-Stream)

The Command Center now aggregates tasks from THREE streams into a unified view:

### Stream Overview

| Stream | Color | Sources | Default Owner |
|--------|-------|---------|---------------|
| **Personal & Admin** | Green | Julie's Slack priorities, Motion recaps, manual | anant |
| **Product & Engineering** | Purple | Motion team meetings, Slack #product/#dev, GitHub issues | jeff |
| **BizDev & Professional** | Gold | Pipeline actions, email threads, transcripts, Motion sales meetings | anant |

### Quick Commands - Multi-Stream

```python
cc = CommandCenter.initialize()

# View all three streams at once
summary = cc.get_task_summary()

# Today's critical actions (across all streams)
today = cc.get_today_actions()

# Filter by stream
personal = cc.get_stream_tasks("personal")
product = cc.get_stream_tasks("product")
professional = cc.get_stream_tasks("professional")

# Filter by owner (team member view)
jeff_queue = cc.get_owner_queue("jeff")
julie_queue = cc.get_owner_queue("julie")

# Add a task manually
cc.add_task(
    title="Return Leela's library books",
    stream="personal",
    priority="high",
    due_date="2026-02-06"
)

# Complete a task
cc.complete_task("per-0001")
```

### Importing Tasks from Sources

```python
cc = CommandCenter.initialize()

# Import from bizdev pipeline (creates professional tasks from opportunities)
cc.import_bizdev_tasks(opportunities_list)

# Import from Motion meeting recaps (auto-categorizes into all three streams)
cc.import_motion_tasks(motion_recaps)

# Import from Slack messages (Julie's priorities + team channels)
cc.import_slack_tasks(slack_tasks)
```

### Task Data File

| File | Purpose | Location |
|------|---------|----------|
| `unified_tasks.json` | All tasks across three streams | `.bizdev/command-center/` |

### Task Priority & Staleness

| Priority | Stale After | Action |
|----------|-------------|--------|
| Critical | 1 day | Do today |
| High | 7 days | This week |
| Medium | 14 days | This sprint |
| Low | 30 days | Backlog |

---

## Proactive Draft Tee-Up (v4: Document Studio Integration)

The Command Center now proactively scans the pipeline to identify opportunities that are READY for draft/proposal generation via the document-studio skill.

### How It Works

```
Pipeline Opportunities
        ↓
Context Registry (are transcripts/emails/pricing searched?)
        ↓
Proactive Drafter (scan for readiness)
        ↓
Tee-Up Queue (ready briefs with document-studio instructions)
        ↓
Document Studio (generates proposal/email HTML)
        ↓
Draft Ledger (logs result with quality score)
```

### Quick Commands - Proactive Drafts

```python
cc = CommandCenter.initialize()

# Scan pipeline for ready-to-generate opportunities
teeup = cc.scan_for_teeup(opportunities)
# Returns: {ready_count: 5, almost_ready_count: 8, ready_emails: 4, ready_proposals: 1}

# Get highest-priority ready brief
next_draft = cc.get_next_teeup()
# Returns: {instructions: "...", output_path: "...", contact: "...", type: "..."}
# Pass next_draft["instructions"] to /document-studio

# See what's blocking almost-ready drafts
unblock = cc.get_teeup_unblock_actions()
# Returns: {"opp-001:email_warm": ["Search transcripts for 'Dr. Smith'"]}
```

### Standalone Functions

```python
from proactive_drafter import scan_and_teeup, get_next_to_generate

# One-call scan + save queue
summary = scan_and_teeup(min_priority=50.0)

# Get next ready brief
next_brief = get_next_to_generate()
if next_brief:
    print(next_brief["instructions"])  # Pass to document-studio
```

### Readiness Levels

| Level | Meaning | Action |
|-------|---------|--------|
| **READY** | All context gathered, quality gate passed | Generate immediately via document-studio |
| **ALMOST** | 1-2 minor gaps (e.g., unified context missing) | Run unblock steps, then generate |
| **BLOCKED** | Major context missing (no transcript/email search) | Must gather context first |
| **ALREADY_DRAFTED** | Good draft exists (quality >= 0.7) | Skip unless refinement needed |

### Tee-Up Data Files

| File | Purpose | Location |
|------|---------|----------|
| `teeup_queue.json` | Ready and almost-ready draft briefs | `.bizdev/command-center/` |

---

## NEW: Status & Next Steps Refresh Protocol (v3.0)

The dashboard now includes two auto-generated columns:

### 1. **Status Column** (Auto-Generated)
- Summarizes recent email activity and meeting outcomes
- Shows activity level (active/warm/cooling/cold)
- Captures sentiment (positive/negative/pending)
- Expandable detail view with topics discussed

### 2. **Next Steps Column** (Auto-Generated)
- Actionable items with urgency levels (critical/high/medium/low)
- Direct links to ready-to-send email and proposal drafts
- "+ Email" / "+ Proposal" buttons to generate missing drafts

### Refresh Protocol

When `/bizdev-opportunity refresh` is invoked, the system:

1. **Parse Latest Emails** - Fetches Gmail threads for each contact
2. **Extract Status** - Analyzes sentiment, topics, and activity level
3. **Find Meeting Transcripts** - Searches for relevant meeting notes
4. **Generate Next Steps** - Determines actionable items based on:
   - Days since last contact
   - Pipeline stage (lead → qualified → demo → proposal → pilot)
   - Sentiment from email analysis
   - Existing notes and blockers
5. **Link Drafts** - Finds existing email/proposal drafts or marks for generation
6. **Regenerate Dashboard** - Updates HTML with new columns

### CLI Scripts

```bash
# Refresh all opportunities (status + next steps)
python3 .bizdev/scripts/opportunity_refresh.py refresh

# Refresh single opportunity
python3 .bizdev/scripts/opportunity_refresh.py refresh opp-001

# Show detailed status for one opportunity
python3 .bizdev/scripts/opportunity_refresh.py status opp-001

# Generate dashboard after refresh
python3 .bizdev/scripts/generate_dashboard.py

# Or do both in one command
python3 .bizdev/scripts/generate_dashboard.py --refresh
```

### Status Schema

Each opportunity now has `auto_status` and `auto_next_steps` fields:

```json
{
  "auto_status": {
    "generated_at": "2026-02-04T12:00:00Z",
    "summary": "Engaged - reviewing proposal",
    "detail": "Topics: Pricing Discussion, API Integration",
    "activity_level": "warm",
    "email_status": {
      "sentiment": "positive",
      "mentioned_topics": ["Pricing Discussion", "API Integration"]
    },
    "meeting_outcomes": {
      "meetings_found": 2,
      "summary": "Positive meeting - agreed on next steps"
    }
  },
  "auto_next_steps": {
    "generated_at": "2026-02-04T12:00:00Z",
    "primary_action": {
      "action": "Follow up on proposal",
      "type": "email",
      "urgency": "high"
    },
    "secondary_actions": [
      {"action": "Add approach notes for better drafting", "type": "note"}
    ],
    "email_draft": ".bizdev/drafts/emails/opp-001-larry-siegel.md",
    "proposal_draft": ".bizdev/drafts/proposals/opp-001-larry-siegel.html",
    "urgency": "high"
  }
}
```

### Dashboard Features

The comprehensive dashboard at `content/docs/bizdev-dashboard-comprehensive.html` includes:

| Column | Content |
|--------|---------|
| Score | Priority score (0-100) |
| Contact | Name, company, ID |
| Type | Opportunity type badge |
| Days | Days since last contact |
| **Status** | Activity level + summary (expandable) |
| **Next Steps** | Action + urgency + draft buttons |
| Notes | Note count (click to view/add) |
| Actions | Refresh (↻) and Archive (✕) buttons |

### Viewing the Dashboard

```bash
# Generate and open dashboard
python3 .bizdev/scripts/generate_dashboard.py
open content/docs/bizdev-dashboard-comprehensive.html

# Or serve via HTTP
cd content/docs && python3 -m http.server 8888 &
open "http://localhost:8888/bizdev-dashboard-comprehensive.html"
```

---

## CORE: Iterative Subagent Extraction (v3.0)

The system uses **Haiku 4.5 subagents** to deeply analyze each transcript, email, and Slack thread individually. This ensures thorough extraction rather than shallow batch scanning.

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│  ORCHESTRATOR (Sonnet/Opus) - You                               │
│  - Lists items to process (transcripts, emails, Slack)          │
│  - Dispatches Haiku subagents in parallel                       │
│  - Aggregates results into crm-state.json                       │
│  - Generates dashboard from accumulated state                   │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│ Haiku Agent 1 │   │ Haiku Agent 2 │   │ Haiku Agent 3 │
│ Transcript    │   │ Email Thread  │   │ Slack Thread  │
│               │   │               │   │               │
│ Returns JSON: │   │ Returns JSON: │   │ Returns JSON: │
│ - Contacts    │   │ - Contact     │   │ - Tasks       │
│ - Opps (multi)│   │ - Thread stat │   │ - Decisions   │
│ - Commitments │   │ - Opps        │   │ - Blockers    │
│ - Next steps  │   │ - Actions     │   │ - Category    │
└───────────────┘   └───────────────┘   └───────────────┘
```

### Why Iterative Processing?

| Aspect | Batch Scanning | Iterative + Subagents |
|--------|----------------|----------------------|
| **Quality** | Shallow pattern matching | Deep analysis per item |
| **Multi-Opp Detection** | Often misses secondary opportunities | Creates consulting + enterprise + membership per contact |
| **Commitments** | Frequently missed | Explicitly extracted with deadlines |
| **State** | All-or-nothing | Incremental, resumable |
| **Parallelism** | Sequential | 3-5 subagents simultaneously |

### Execution Protocol

#### Deep Scan (First Run / Periodic Audit)

```bash
/bizdev-opportunity deep-scan --lookback 3
```

**Steps:**
1. **List all transcripts** from Drive folder (last N months)
2. **List all email threads** via gog CLI (non-marketing, external contacts)
3. **List all relevant Slack threads** via MCP
4. **For each item NOT yet processed:**
   - Spawn Haiku subagent with extraction prompt
   - Await structured JSON result
   - Merge into `crm-state.json`
   - Mark item as processed with timestamp
5. **Generate dashboard** from accumulated state

#### Incremental Update (Daily Use)

```bash
/bizdev-opportunity update
```

**Steps:**
1. Load `crm-state.json` with `last_scan` timestamp
2. Fetch only NEW items since last scan
3. Process each new item with Haiku subagent
4. Detect deltas (new responses, gone stale, commitments due)
5. Update dashboard

### Subagent Dispatch Pattern

When processing each item, spawn a Haiku subagent:

```
Task(
  subagent_type="general-purpose",
  model="haiku",
  prompt="""
[Extraction prompt from extraction_prompts.md]

**CONTENT TO ANALYZE:**
{actual_content}

Return ONLY valid JSON, no additional text.
""",
  description="Extract opportunities from [transcript/email/slack]"
)
```

**Parallel dispatch example (3 items):**
```
# In a single message, dispatch multiple subagents:
Task(model="haiku", prompt="Analyze transcript 1...", description="Extract: Larry Siegel")
Task(model="haiku", prompt="Analyze email thread 2...", description="Extract: Bill Liatsis")
Task(model="haiku", prompt="Analyze Slack DM 3...", description="Extract: Julie tasks")
```

### Extraction Prompt Templates

See `extraction_prompts.md` for detailed prompts:
- **Transcript Extraction**: Multi-opportunity detection, pain points, commitments, quotes
- **Email Thread Extraction**: Thread status, response needed, relationship signals
- **Slack Thread Extraction**: Tasks, decisions, blockers, category classification

### State Persistence (`crm-state.json`)

```json
{
  "last_scan": "2026-02-04T10:00:00Z",
  "processed_items": {
    "transcripts": {
      "drive-file-123": {"processed_at": "2026-02-04T10:05:00Z", "opportunities_found": 2}
    },
    "emails": {
      "thread-abc": {"processed_at": "2026-02-04T10:06:00Z", "contact": "bill@helos.health"}
    },
    "slack": {
      "C123-1234567890": {"processed_at": "2026-02-04T10:07:00Z", "category": "personal_admin"}
    }
  },
  "contacts": {
    "bill@helos.health": {
      "name": "Bill Liatsis",
      "company": "Helos",
      "opportunities": ["opp-bill-enterprise", "opp-bill-consulting"],
      "last_contact": "2026-02-01",
      "awaiting_response_from": "them"
    }
  },
  "opportunities": [...],
  "tasks": {
    "product_work": [...],
    "personal_admin": [...]
  }
}
```

### Quality Gates

Each extraction result is validated before merging:
1. **JSON validity** - Must parse correctly
2. **Required fields** - contacts[], opportunities[], source{}
3. **Confidence threshold** - Only opportunities with confidence >= 0.5 are included
4. **Deduplication** - Same contact + same opportunity type = merge, don't duplicate

---

## NEW: Automatic Email & Proposal Drafting (v2.2)

The dashboard now automatically generates contextual email drafts and proposals for all opportunities, with clickable links directly in the dashboard.

### How It Works

1. **Email Drafting**: For every opportunity, an appropriate email is generated based on:
   - Opportunity type (consulting, enterprise, commons, media)
   - Relationship status (cold, warm follow-up, re-engagement)
   - Days since last contact
   - Prior conversation context

2. **Proposal Generation**: For high-priority opportunities (score ≥70) of type consulting or enterprise, a full proposal is generated with:
   - Executive summary customized to the contact/company
   - Value proposition tailored to opportunity type
   - **Pricing validation** (see below)
   - Next steps and call-to-action

### ⚠️ CRITICAL: Pricing Extraction from Transcripts

**Before generating ANY proposal**, you MUST search transcripts and emails for pricing commitments. Default pricing should ONLY be used when no specific pricing was discussed.

**Required Search Pattern:**
```bash
# Search for pricing discussions
grep -i "199\|299\|499\|discount\|special\|offer\|month" .bizdev/drafts/*<contact>*
grep -i "pricing\|rate\|cost" <transcript_file>
```

**Extract these fields from transcripts:**
| Field | Example | Where to Find |
|-------|---------|---------------|
| `agreed_price` | $199/month | "I can do $199 for you" |
| `discount_reason` | Referral from Lale | "Since Lale introduced us" |
| `discount_percent` | 60% | "That's 60% off standard" |
| `duration` | 6 months | "For the first 6 months" |
| `special_terms` | Unlimited reports | "I'll include unlimited" |

**Quality Gate - Pricing Validation:**
Before finalizing a proposal, verify:
1. ✅ Searched ALL transcripts mentioning contact name
2. ✅ Searched ALL email threads with contact
3. ✅ Checked `.bizdev/drafts/email-*` for prior draft context
4. ✅ If discount discussed → proposal reflects exact terms
5. ✅ If no pricing discussed → use default from `pricing_config.py`

**Failure Mode (What Went Wrong with Arda Lembet):**
- Transcript clearly stated "$199/month (discounted from $499)"
- Transcript noted "50% discount that Lale had negotiated"
- Proposal was generated with default $499/month
- **Root cause**: Proposal generation pulled from opportunity summary, not transcript details

3. **Dashboard Integration**: Each opportunity row includes an "Outreach" column with:
   - **Email** button → Opens pre-drafted email with copy-to-clipboard
   - **Proposal** button → Opens full HTML proposal

### File Locations

| Type | Markdown Source | HTML (Browser) |
|------|-----------------|----------------|
| Emails | `.bizdev/drafts/emails/*.md` | `content/docs/bizdev-drafts/emails/*.html` |
| Proposals | `.bizdev/drafts/proposals/*.html` | `content/docs/bizdev-drafts/proposals/*.html` |

### Email Templates by Type

| Opportunity Type | Cold | Warm Follow-up | Re-engagement |
|------------------|------|----------------|---------------|
| **Consulting** | Pattern recognition hook | Post-meeting follow-up | Value-add return |
| **Enterprise** | Lab report time savings | Demo/sandbox offer | New features update |
| **Commons** | AI discoverability hook | Partnership benefits | Profile update |
| **Media** | Content collaboration | Format discussion | Topic refresh |

### Proposal Templates

| Type | Default Rate | Includes | Override |
|------|--------------|----------|----------|
| **Consulting** | $10,000/month | Weekly meetings, Slack integration, strategy formulation | Check transcript for negotiated rate |
| **Enterprise** | $499/month | 200 reports, AI Lab Report Generator, customization | Check transcript for discounts/special offers |

**⚠️ ALWAYS check transcripts for pricing commitments before using defaults.**

### Using the Outreach Links

1. **Start the local server:**
   ```bash
   cd content/docs && python3 -m http.server 8888
   ```

2. **Open the dashboard:**
   ```bash
   open "http://localhost:8888/bizdev-dashboard-2026-02-03.html"
   ```

3. **Click Email/Proposal buttons** to view drafts

4. **Use "Copy Email" button** to copy text to clipboard for pasting into Gmail

### Email Generation Protocol (gog CLI - Context-Gated)

**CRITICAL**: Before generating ANY email, ALWAYS fetch real email content using the `gog` CLI. This prevents hallucinated context and ensures emails reference actual conversations.

#### Before Generating ANY Email:

1. **ALWAYS Fetch Latest Thread First**:
   ```bash
   GOG_KEYRING_PASSWORD=ngm GOG_ACCOUNT=anant@nextgenerationmedicine.co \
     gog gmail search "from:{email} OR to:{email}" --max 5
   ```

2. **Get Full Thread Content**:
   ```bash
   GOG_KEYRING_PASSWORD=ngm GOG_ACCOUNT=anant@nextgenerationmedicine.co \
     gog gmail thread {THREAD_ID}
   ```

3. **Extract Signals from ACTUAL Email Content**:
   - What did they ACTUALLY express interest in? (exact quotes)
   - What specific requests did they make?
   - What timeline/urgency did they mention?
   - What is the relationship context?

4. **Generate Email Using REAL Context**:
   - Reference their ACTUAL words from the thread
   - Address their SPECIFIC ask (not generic assumptions)
   - Match the tone and context of the conversation

#### Never Use Hardcoded/Cached Context

The system MUST fetch fresh email content before generating. Never use:
- Hardcoded `ENRICHED_DATA` dictionaries
- Cached signals from previous sessions
- Assumed context from unrelated transcripts

#### Anti-Hallucination Rules

| Pattern | ❌ Avoid | ✅ Instead |
|---------|----------|-----------|
| Vague reference | "Your point about the challenges you're facing" | "Your point about teaching timeline constraints" |
| Generic callback | "Based on what you shared" | "When you mentioned needing reports for 20 locations" |
| Invented context | "The topics we discussed" | Reference actual signal content |
| False familiarity | "Great connecting earlier" | Only use when there WAS a prior connection |

#### Context Validation Module

Use `context_validator.py` to check if an opportunity has sufficient context:

```python
from context_validator import validate_context

is_valid, assessment = validate_context(opportunity, "warm-followup")
if not is_valid:
    # Trigger auto-enrichment or flag for manual review
    for gap in assessment["gaps"]:
        print(f"Missing: {gap['field']} - {gap['issue']}")
```

#### Auto-Enrichment via gog CLI (PREFERRED)

Use `fetch_email_context.py` to get real email content before generating:

```bash
# Get full context for a contact
python3 .bizdev/scripts/fetch_email_context.py --email azaidi@gmail.com --name "Ali Zaidi" --format-prompt

# Extract signals in JSON format
python3 .bizdev/scripts/fetch_email_context.py --email azaidi@gmail.com --extract-signals

# Get specific thread
python3 .bizdev/scripts/fetch_email_context.py --thread 19bbda6ce9a1205b
```

Or use gog CLI directly:
```bash
# Search for emails
GOG_KEYRING_PASSWORD=ngm GOG_ACCOUNT=anant@nextgenerationmedicine.co \
  gog gmail search "from:contact@example.com OR to:contact@example.com" --max 5

# Get thread content
GOG_KEYRING_PASSWORD=ngm GOG_ACCOUNT=anant@nextgenerationmedicine.co \
  gog gmail thread THREAD_ID
```

---

### Regenerating Drafts (CRITICAL: Use Iterative Generator)

**⚠️ DO NOT USE `generate_drafts.py`** - It produces generic, context-disconnected output.

**USE THE ITERATIVE GENERATOR:**

```bash
cd /path/to/project

# Generate contextual drafts for ALL opportunities (requires ANTHROPIC_API_KEY)
python3 .bizdev/scripts/iterative_draft_generator.py

# Generate draft for a SINGLE opportunity (recommended for testing)
python3 .bizdev/scripts/iterative_draft_generator.py --single opp-002

# Dry run to see context extraction without LLM calls
python3 .bizdev/scripts/iterative_draft_generator.py --dry-run
```

**Or let Claude generate directly** (within skill execution):

```bash
# Get the contextual prompt for Claude to execute
python3 .bizdev/scripts/generate_draft_for_opportunity.py opp-002 email
python3 .bizdev/scripts/generate_draft_for_opportunity.py opp-002 proposal
```

### OLD vs NEW Draft Generator Comparison

| Aspect | OLD (`generate_drafts.py`) | NEW (`iterative_draft_generator.py`) |
|--------|---------------------------|--------------------------------------|
| Pain points | ❌ IGNORED completely | ✅ Extracts and references all |
| Key quotes | ❌ IGNORED completely | ✅ Quotes their words back |
| Follow-up requests | ❌ IGNORED completely | ✅ Addresses specifically |
| Notes | ❌ Truncated to 50 chars | ✅ Full notes included |
| Quality gates | ❌ NONE | ✅ 3-iteration refinement loop |
| Personalization | ❌ Name only | ✅ Full context personalization |
| Consulting upsell | ❌ NONE | ✅ Tasteful enterprise upsell |
| MCP context | ❌ NONE | ✅ Gmail/Drive enrichment workflows |

### Scripts Reference

| Script | Purpose | Use When |
|--------|---------|----------|
| `iterative_draft_generator.py` | Full iterative draft generation with LLM | Batch generation with API key |
| `generate_draft_for_opportunity.py` | Generate prompt for Claude to execute | Within Claude skill execution |
| `mcp_context_enricher.py` | Enrich context from Gmail/Drive/Slack | Before drafting for full context |
| ~~`generate_drafts.py`~~ | ❌ DEPRECATED - produces generic output | NEVER USE |

---

## NEW: Priority-Based Opportunity Tracking (v2.1)

### Enhanced Features

1. **Sent Email Tracking**: Cross-references opportunities with Gmail SENT folder to track:
   - Last outbound email date
   - Days waiting for response
   - Response rate per contact

2. **Intelligent Prioritization**: Composite scoring algorithm (0-100) combining:
   - Confidence score (40% weight)
   - Time urgency / decay factor (20%)
   - Engagement history (20%)
   - Opportunity type value (20%)
   - Signal strength bonuses

3. **Opportunity Status Tracking**:
   - `ACTIVE` - Recent activity, engaged
   - `STALE` - No activity >30 days
   - `NEEDS_FOLLOWUP` - We need to reach out
   - `AWAITING_RESPONSE` - Ball in their court

4. **Daily Actions Generator**: Priority-sorted action list with specific next steps

### New Files

| File | Purpose |
|------|---------|
| `opportunity_tracker.py` | Unified tracking with email cross-reference |
| `templates/pipeline-priority.html` | Priority-sorted dashboard template |
| `.bizdev/opportunities-enhanced.json` | Full enriched opportunity data |
| `.bizdev/daily-actions.md` | Today's priority actions |

### Priority Score Calculation

```
Priority Score = (Confidence × 0.4) + Time_Score + Engagement_Score + Type_Value + Bonuses

Where:
- Time_Score: 5-20 based on days since contact + awaiting response boost
- Engagement_Score: 0-20 based on communication history balance
- Type_Value: consulting=1.5×, enterprise=1.4×, membership=1.0×, commons=0.8×
- Bonuses: +5 explicit interest, +5 follow-up request, +3-15 urgency level
```

### Urgency Levels

| Level | Criteria | Action |
|-------|----------|--------|
| 🔴 Critical | Awaiting >14 days OR status=stale | Do today |
| 🟡 High | Priority ≥70 OR needs_followup | This week |
| 🟢 Medium | Priority ≥50 | Nurture |
| ⚪ Low | Priority <50 | Background |

### Gmail Access (gog CLI) - REQUIRED for Email Generation

**IMPORTANT**: Always use gog CLI to fetch actual email content before generating emails. This ensures no hallucinated context.

```bash
# Search all emails with a contact
GOG_KEYRING_PASSWORD=ngm GOG_ACCOUNT=anant@nextgenerationmedicine.co \
  gog gmail search "from:contact@example.com OR to:contact@example.com" --max 10

# Get full thread content
GOG_KEYRING_PASSWORD=ngm GOG_ACCOUNT=anant@nextgenerationmedicine.co \
  gog gmail thread THREAD_ID

# Search sent emails to a contact
GOG_KEYRING_PASSWORD=ngm GOG_ACCOUNT=anant@nextgenerationmedicine.co \
  gog gmail search "to:contact@example.com in:sent" --max 20
```

**Helper Script**:
```bash
# Use the fetch_email_context.py helper for structured output
python3 .bizdev/scripts/fetch_email_context.py --email contact@example.com --format-prompt
```

### Running Priority Scan

```bash
cd /home/botadmin/clawd/ngm-website-official
python3 .bizdev/run_priority_scan.py
```

### Output Locations

- **Enhanced Data**: `.bizdev/opportunities-enhanced.json`
- **Priority Dashboard**: `content/docs/bizdev-dashboard-priority.html`
- **Daily Actions**: `.bizdev/daily-actions.md`

---

## Deep Scan Mode (Haiku 4.5)

The `scan-deep` command uses Claude 3.5 Haiku to analyze each transcript with:

- **Fresh context**: Each transcript gets isolated LLM context (no bias)
- **Quality gates**: Extractions must have exact quotes, proper names, reasoning
- **Iterative refinement**: Up to 3 attempts per transcript with feedback
- **Audit logging**: Every iteration logged for debugging

### Requirements

1. Set `ANTHROPIC_API_KEY` environment variable
2. Transcripts downloaded and converted to text

### Cost

- ~$0.01-0.02 per transcript
- ~$1.50-3.00 for 150 transcripts

### New Files

| File | Purpose |
|------|---------|
| `fast_llm_client.py` | Haiku 4.5 API client |
| `iterative_scanner.py` | Deep scan execution loop |

---

## Iterative Execution Flow

```
┌────────────────────────────────────────────────────────────────────────┐
│                      /bizdev-opportunity                                │
│                                                                         │
│  ┌─────────────┐   ┌───────────────────────────────────────────────┐   │
│  │   PLANNING  │   │              EXECUTION LOOP                   │   │
│  │             │──▶│                                               │   │
│  │ • Parse     │   │  ┌─────────┐  ┌─────────┐  ┌───────────────┐ │   │
│  │   sources   │   │  │ SCAN    │─▶│ ANALYZE │─▶│ QUALITY GATE  │ │   │
│  │ • Generate  │   │  │ Source  │  │ Signals │  │ (Pass/Fail)   │ │   │
│  │   task PRD  │   │  └─────────┘  └─────────┘  └───────┬───────┘ │   │
│  │ • Init      │   │                                    │         │   │
│  │   tracking  │   │  ┌─────────┐  ┌─────────┐  ┌───────▼───────┐ │   │
│  └─────────────┘   │  │ REFINE  │◀─│EVALUATE │◀─│ UNIFIED CTX   │ │   │
│                    │  │ (loop)  │  │ Quality │  │ + DRAFT       │ │   │
│                    │  └────┬────┘  └─────────┘  └───────────────┘ │   │
│                    │       │                                       │   │
│                    │       ▼ (max 3 iterations per item)           │   │
│                    └───────────────────────────────────────────────┘   │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                     AUDIT LOG & LEARNING                        │   │
│  │  Every action logged • Patterns captured • Context preserved    │   │
│  │  Unified context: Transcripts + Emails merged before drafting   │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────────────────┘
```

---

## Standard Pricing Architecture (Updated 2026-01-18)

### Consulting Services

| Tier | Rate | Commitment | When to Use |
|------|------|------------|-------------|
| **Standard** | $10,000/month | 3-month upfront ($30,000), then month-to-month | **DEFAULT for ALL proposals** |
| **Early-Stage** | $5,000/month | 3-month upfront ($15,000), then month-to-month | **ONLY when user explicitly instructs** |

**IMPORTANT:** 
- Default to $10,000/month for all proposals
- The $5,000/month rate is reserved exclusively for early-stage companies/startups
- Apply the $5,000 rate ONLY when the user explicitly instructs you to do so
- Never present both options in the same proposal—use one rate or the other

**Deliverables include:**
- Weekly synchronous meetings
- Integration into client team operating systems (Slack, Notion, etc.)
- Product specification review and feedback
- Clinical strategy formulation
- Technology strategy development

### Longevity Platform (Report Generator)

| Tier | Rate | Included |
|------|------|----------|
| **Base** | $499/month | 200 generated reports |
| **Volume** | Tiered pricing | Scales beyond baseline volume |

*Note: Include platform pricing only when relevant to the opportunity or when user requests it.*

---

## Value Proposition Differentiators

**IMPORTANT:** Weave these into all proposals and emails.

### 1. World-Class Expertise
- Track record building multiple $100M+ healthcare companies
- Pioneered the first vertically integrated longevity clinic in the United States
- Current advisor to industry leaders including MidiHealth and Superpower
- Unparalleled industry perspective from active engagement with top-tier organizations

### 2. Proprietary Technology Platform
- Built on years of curated longevity and frontier medicine data
- Cell biology-first approach vs. conventional guidelines—the future of medicine
- Delivers insights fundamentally irreplicable by generic LLMs or competing platforms
- Continuously updated core asset capturing cutting-edge research

### 3. Integrated Cross-Domain Mastery
- Rare convergence of deep expertise across technology, medicine, and business
- This integration is virtually unavailable elsewhere in the market
- Translates to accelerated timelines and cost savings for clients
- Eliminates the need for multiple disparate consultants

**Key Message:** This combination of proven execution, proprietary infrastructure, and cross-functional fluency represents a world-class offering that compresses development cycles and de-risks strategic decisions.

---

## Consulting Upsell Strategy

**IMPORTANT:** Tastefully upsell custom consulting services in ALL proposals and email drafts where there's a natural fit. This is a world-class offering that should be woven into outreach organically.

### Why Consulting is Compelling

Dr. Vinjamoori's consulting practice is derived from:
- **Pioneering experience** building one of the first vertically integrated longevity clinics in the United States
- **Working with the top names in the space** — current advisor to industry leaders, with a track record spanning multiple $100M+ healthcare companies
- **Truly world-class expertise** that's virtually impossible to find elsewhere

### The Integrated Advantage

Unlike hiring separate specialists, NGM consulting covers **any aspect of your business**:

| Domain | What's Covered |
|--------|----------------|
| **Clinical** | Protocol development, service line design, clinical operations, quality assurance, provider training |
| **Technology** | Product strategy, AI/ML implementation, platform architecture, technical due diligence, build vs. buy decisions |
| **Operations** | Scaling playbooks, workflow optimization, team structure, vendor selection, operational efficiency |
| **Business** | Go-to-market strategy, pricing models, partnership development, fundraising positioning, competitive analysis |

**Cost Savings Message:** Clients save money and accelerate timelines by getting an integrated perspective from one advisor who spans clinical, tech, and ops—rather than coordinating multiple expensive specialists who don't talk to each other.

### How to Upsell Tastefully

1. **Identify the hook** — Look for pain points in transcripts/emails that suggest they need strategic guidance beyond just a product or service
2. **Bridge naturally** — Connect their immediate need to the broader challenge ("Beyond the report generator, it sounds like you're also figuring out how to structure your longevity service line...")
3. **Position as optional** — Present consulting as an "if you'd find it valuable" addition, not a hard sell
4. **Lead with outcomes** — Focus on what they'll achieve (faster launch, fewer mistakes, proven playbooks) not the consulting itself

### Example Upsell Language

**In emails:**
> "If it would be helpful, I also work with a select number of companies on broader clinical and operational strategy—drawing from my experience building Modern Age and advising companies like Superpower and Midi Health. Happy to discuss if that's relevant to where you're headed."

**In proposals:**
> "While the Report Generator addresses your immediate lab interpretation needs, I've noticed [COMPANY] is also navigating [CHALLENGE from transcript]. If valuable, I offer strategic advisory that spans clinical, technology, and operations—an integrated perspective that typically requires multiple consultants to achieve."

### When NOT to Upsell

- The opportunity is purely transactional (e.g., simple Commons listing with no broader needs)
- The contact has explicitly said they're only interested in one thing
- The relationship is too cold for a consulting pitch (save for follow-up)
- Budget signals suggest consulting is out of reach

---

## Opportunity Types

| Type | Description | Value Range |
|------|-------------|-------------|
| **Consulting** | Advisory retainers, clinical strategy, product guidance | $5,000 - $10,000/month |
| **Membership** | Longevity Intelligence Platform subscriptions | $499/month (200 reports) |
| **Report Generator** | AI lab report capability (standalone) | $499/month base tier |
| **Commons Partnership** | Vendor profiles on NGM Commons + LinkedIn features | $5,000 - $12,500/year |
| **Enterprise** | Multi-location platform deployments, API integrations | Custom pricing |
| **Media/Content** | Podcast appearances, content collaboration | Brand value |

---

## CRITICAL: Multi-Opportunity Extraction Approach

### Why One Contact = Multiple Opportunities

The old deep scan produced **251 opportunities from 144 unique contacts** (avg 1.7 opps per contact). This is because **one contact can have multiple opportunity types** based on what they discussed or expressed interest in.

**Example: Larry Siegel (Yunique Medical)**
- Row 1: `enterprise` - Platform deployment for 20 clinic locations
- Row 2: `consulting` - Hormone pellet dosing algorithm collaboration

**Example: Catherine Grant**
- Row 1: `consulting` - DPC practice strategy
- Row 2: `enterprise` - Lab interpretation workflow integration

**Example: Tom Joseph**
- Row 1: `consulting` - TRT/peptides telehealth advisory
- Row 2: `membership` - LIP platform for new practice

### Multi-Opportunity Extraction Algorithm

When analyzing EACH transcript, extract opportunities for EVERY service type mentioned:

```
FOR each transcript:
  1. Read full transcript content
  2. Identify contact name(s) and company
  3. Extract ALL service interests mentioned:
     - Consulting signals: "advisory", "strategy", "guidance", "mentor"
     - Enterprise signals: "platform", "API", "integration", "scale", "multi-location"
     - Membership signals: "join", "subscribe", "reports", "access"
     - Report Generator signals: "lab reports", "biomarkers", "interpretation"
     - Commons signals: "partnership", "profile", "directory", "visibility"
     - Media signals: "podcast", "interview", "article", "content"
  4. CREATE SEPARATE OPPORTUNITY ROWS for each type with signals
  5. Cross-reference with email threads for additional context
```

### Expected Output Scale

| Scan Input | Expected Opportunities |
|------------|------------------------|
| 50 transcripts | 75-125 opportunities |
| 100 transcripts | 150-250 opportunities |
| 150 transcripts | 225-375 opportunities |

If your scan produces significantly fewer opportunities than this scale, you're likely:
- De-duplicating by contact (wrong - keep multiple types per contact)
- Filtering too aggressively (include medium confidence)
- Not analyzing transcript content for multi-type signals

### Dashboard Row Format

Each row in the dashboard should show:
- **Contact**: Name + badges (UNIFIED if transcript+email, urgency level)
- **Company**: Company name
- **Type**: Specific opportunity type (consulting, enterprise, etc.)
- **Urgency**: Critical/High/Medium/Low
- **Source Meeting**: Transcript or email source
- **Date**: Last contact date
- **Next Action**: Specific action for THIS opportunity type
- **Outreach**: Email/Proposal buttons

### UNIFIED Badge

Contacts with BOTH transcript AND email history get a **"UNIFIED"** badge to indicate high-confidence opportunity with cross-referenced context. These should be prioritized.

### Implementation Checklist

When implementing deep scan:
- [ ] Process each transcript individually (fresh LLM context)
- [ ] Extract MULTIPLE opportunity types per transcript
- [ ] Create separate rows for each opportunity type
- [ ] Cross-reference with email threads for UNIFIED badge
- [ ] Include transcript-only AND email-only contacts
- [ ] Do NOT de-duplicate by contact - keep all opportunity rows
- [ ] Sort by priority score, not alphabetically

### Commons Partnership - LinkedIn Social Amplification

**IMPORTANT:** NGM Commons partnerships include exposure through Dr. Vinjamoori's LinkedIn—one of the most trusted and high-engagement accounts in the emerging longevity space (10K+ followers, consistently high engagement from physicians, executives, and investors).

| Tier | LinkedIn Benefits |
|------|-------------------|
| **Partner** ($5,000/year) | Featured LinkedIn post (1x) introducing the partner and their value to the longevity community |
| **Sponsor** ($12,500/year) | Multiple LinkedIn placements including: dedicated feature post, LinkedIn Live stream appearance, ongoing social amplification in relevant discussions, and co-branded content opportunities |

**When discussing Commons partnerships, always mention:**
- Research-driven profile on NGM Commons with AI discoverability
- LinkedIn exposure to the longevity medicine community
- The difference in social amplification between Partner (single post) and Sponsor (multiple touchpoints including live streams)

---

## Quality Gates

Every output is evaluated against explicit criteria:

### Opportunity Analysis Gate
- Signal confidence ≥ 0.6 for at least one signal
- Contact info completeness (name + email OR company)
- Classification confidence ≥ 0.5
- No contradictory signals

### Email Draft Gate
- Opens with value, not cliche phrases
- Under word limit (cold: 200, warm: 300)
- References specific pain points
- Has single, clear CTA
- No salesy patterns

### Proposal Gate
- All required sections present
- No placeholder text
- Pricing matches recommended tier
- Pain points addressed
- Valid HTML structure

---

## Session Files

```
.bizdev/
├── prd.json              # Current PRD with task status
├── progress.txt          # Learnings and patterns
├── opportunities.json    # Discovered opportunities
└── drafts/
    ├── emails/           # Generated email drafts (.md source)
    └── proposals/        # Generated proposals (.html)

content/docs/
├── bizdev-pipeline-deep-scan.html    # Main dashboard
└── bizdev-drafts/
    ├── emails/           # Browser-viewable email drafts (.html)
    └── proposals/        # Browser-viewable proposals (.html)

.claude/skills/bizdev-opportunity/changelogs/
└── session-YYYY-MM-DD-HHmmss.md   # Session audit logs
```

## Dashboard & Outreach Viewing

The dashboard at `content/docs/bizdev-pipeline-deep-scan.html` includes an **Outreach** column with clickable Email/Proposal buttons.

### Starting the Local Server

To view the dashboard with working links:

```bash
cd content/docs && python3 -m http.server 8080 &
open "http://localhost:8080/bizdev-pipeline-deep-scan.html"
```

To stop the server:
```bash
pkill -f "python3 -m http.server 8080"
```

### Email HTML Generation

Emails are stored as markdown in `.bizdev/drafts/emails/` but rendered as HTML in `content/docs/bizdev-drafts/emails/` for browser viewing with:
- Styled header with To/Subject metadata
- Properly formatted body with bold text and lists
- **Copy Email** button for one-click copy to clipboard
- Back to Dashboard link

### Generating Browser-Viewable Emails

After creating email drafts, run this to generate HTML versions:

```bash
cd "/path/to/project"
for f in .bizdev/drafts/emails/*.md; do
  name=$(basename "$f" .md)
  to=$(grep "^To:" "$f" | sed 's/^To: //')
  subject=$(grep "^Subject:" "$f" | sed 's/^Subject: //')
  body=$(sed '1,/^---$/d' "$f" | sed '1,/^---$/d')
  
  cat > "content/docs/bizdev-drafts/emails/${name}.html" << HTMLEOF
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Email: ${subject}</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 700px; margin: 40px auto; padding: 20px; line-height: 1.6; background: #f5f5f5; }
    .email-container { background: white; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); overflow: hidden; }
    .email-header { background: #1a1a2e; color: white; padding: 20px; }
    .email-header h2 { margin: 0 0 5px 0; font-size: 14px; opacity: 0.7; }
    .email-header h1 { margin: 0; font-size: 18px; }
    .email-meta { padding: 15px 20px; background: #f8f9fa; border-bottom: 1px solid #eee; font-size: 14px; }
    .email-body { padding: 25px; font-size: 15px; color: #333; }
    .email-body p { margin: 0 0 15px 0; }
    .email-body strong { font-weight: 600; }
    .email-body ul { margin: 10px 0 15px 0; padding-left: 20px; }
    .email-body li { margin: 5px 0; }
    .copy-btn { position: fixed; top: 20px; right: 20px; background: #2563eb; color: white; border: none; padding: 12px 20px; border-radius: 8px; cursor: pointer; font-size: 14px; font-weight: 500; }
    .copy-btn:hover { background: #1d4ed8; }
    .copy-btn.copied { background: #059669; }
    .back-link { display: inline-block; margin-bottom: 15px; color: #2563eb; text-decoration: none; font-size: 14px; }
  </style>
</head>
<body>
  <a href="../../bizdev-pipeline-deep-scan.html" class="back-link">← Back to Dashboard</a>
  <button class="copy-btn" onclick="copyEmail()">Copy Email</button>
  <div class="email-container">
    <div class="email-header">
      <h2>TO</h2>
      <h1>${to}</h1>
    </div>
    <div class="email-meta">
      <span><strong>Subject:</strong> ${subject}</span>
    </div>
    <div class="email-body" id="emailBody">
      <!-- Markdown body converted to HTML -->
    </div>
  </div>
  <script>
    function copyEmail() {
      const body = document.getElementById('emailBody').innerText;
      navigator.clipboard.writeText(body).then(() => {
        const btn = document.querySelector('.copy-btn');
        btn.textContent = 'Copied!';
        btn.classList.add('copied');
        setTimeout(() => { btn.textContent = 'Copy Email'; btn.classList.remove('copied'); }, 2000);
      });
    }
  </script>
</body>
</html>
HTMLEOF
done
```

---

## Module Reference

### Core Modules

| File | Purpose |
|------|---------|
| `SKILL.md` | This documentation |
| `main.py` | Entry point and orchestration |
| `types.py` | Data structures and enums |
| `prompts.py` | LLM prompt templates |
| `analyzer.py` | Scoring and classification |
| `dashboard.py` | HTML pipeline generation |
| `pricing_config.py` | **Centralized pricing & value proposition (2026-01-18)** |

### Iterative Modules

| File | Purpose |
|------|---------|
| `prd_generator.py` | Task generation (Ralph-style) |
| `quality_gates.py` | Evaluation criteria and rubrics |
| `email_drafter.py` | Email generation with value prop integration |
| `email_searcher.py` | Gmail context search |
| `context_loader.py` | NGM context aggregation |
| `subagents.py` | Fresh-context delegation |
| `proposal_bridge.py` | Proposal integration with pricing tiers |
| `unified_context.py` | **Cross-references transcripts AND emails for unified context** |

### Templates

| File | Purpose |
|------|---------|
| `templates/pipeline.html` | Dashboard HTML template |
| `templates/components.html` | UI components |
| `templates/email_templates.md` | Email patterns by type |
| `templates/evaluation_rubrics.md` | Quality gate rubrics |
| `changelogs/changelog-template.md` | Session log template |

---

## Unified Context Workflow (NEW)

When drafting emails or proposals for an opportunity, the system now cross-references **both meeting transcripts AND email history** to ensure complete context. This prevents:

- Missing prior commitments made in emails
- Duplicating topics already discussed in meetings
- Ignoring relationship history from email threads

### How It Works

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      UNIFIED CONTEXT AGGREGATION                             │
│                                                                              │
│  ┌───────────────────┐        ┌───────────────────┐                         │
│  │   TRANSCRIPTS     │        │      EMAILS       │                         │
│  │ • PDF meeting     │        │ • Gmail threads   │                         │
│  │   transcripts     │        │ • Prior outreach  │                         │
│  │ • Pain points     │        │ • Commitments     │                         │
│  │ • Discussed items │        │ • Action items    │                         │
│  └─────────┬─────────┘        └─────────┬─────────┘                         │
│            │                            │                                    │
│            └──────────┬─────────────────┘                                   │
│                       ▼                                                      │
│           ┌───────────────────────┐                                         │
│           │   MERGE & DEDUPE      │                                         │
│           │ • Match by contact    │                                         │
│           │ • Chronological order │                                         │
│           │ • Extract key signals │                                         │
│           └───────────┬───────────┘                                         │
│                       ▼                                                      │
│           ┌───────────────────────┐                                         │
│           │  UNIFIED CONTEXT      │                                         │
│           │ • All touchpoints     │                                         │
│           │ • Relationship stage  │                                         │
│           │ • Open action items   │                                         │
│           │ • Pain points summary │                                         │
│           └───────────┬───────────┘                                         │
│                       ▼                                                      │
│           ┌───────────────────────┐                                         │
│           │  DRAFT EMAIL/PROPOSAL │                                         │
│           │ • References meetings │                                         │
│           │ • Continues threads   │                                         │
│           │ • Honors commitments  │                                         │
│           └───────────────────────┘                                         │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Key Functions

| Function | Purpose |
|----------|---------|
| `generate_unified_context_workflow()` | Main orchestration - gathers all context sources |
| `extract_transcript_context()` | Extracts key signals from meeting transcripts |
| `extract_email_context()` | Extracts signals from email threads |
| `merge_contexts()` | Deduplicates and orders touchpoints chronologically |
| `generate_email_prompt_with_unified_context()` | Builds LLM prompt with full context |

### Usage

The unified context is automatically used when:

1. **Drafting emails** - The email drafter calls `generate_unified_context_workflow()` before generating
2. **Creating proposals** - Proposals include context from all prior interactions
3. **Manual context lookup** - Use `/bizdev-opportunity context "Name" --email email@example.com`

### Example Context Output

```markdown
## Unified Context for: Dr. James Smith

### Relationship Summary
- **First Contact:** Meeting (2026-01-10)
- **Total Touchpoints:** 4 (2 meetings, 2 email threads)
- **Relationship Stage:** warm_engaged

### Key Signals (Chronological)
1. [Meeting 2026-01-10] Discussed lab interpretation challenges
2. [Email 2026-01-12] Sent API documentation, asked about timeline
3. [Meeting 2026-01-18] Demoed report generator, mentioned budget approval pending
4. [Email 2026-01-20] Confirmed interest in pilot program

### Open Action Items
- [ ] Send pricing proposal (from meeting 2026-01-18)
- [ ] Schedule follow-up with their tech lead (from email 2026-01-20)

### Pain Points Mentioned
- Manual lab interpretation taking too much time
- Staff overwhelmed with patient volume
- Need for scalable solution before Q2
```

---

## Example Session

```
> /bizdev-opportunity scan-iterative --folder-id 1abc123 --lookback 3

BIZDEV OPPORTUNITY PLANNING
━━━━━━━━━━━━━━━━━━━━━━━━━━━

Sources Found:
  - 8 transcripts in Google Drive
  - 12 matching email threads

Tasks Generated: 20
  - Scan & Extract: 20
  - Email Drafts: TBD (depends on scores)
  - Proposals: TBD (depends on scores)

PRD saved to: .bizdev/prd.json
Progress log: .bizdev/progress.txt

Begin iterative execution? [Y/n]

---

ITERATION 3 of 20
━━━━━━━━━━━━━━━━

Source: Meeting-DrSmith-2026-01-10.docx
Status: IN_PROGRESS

Step 1: Scanning...
  ✓ 3 signals extracted
  ✓ Contact: Dr. James Smith, Smith Wellness
  
Step 2: Quality Gate (Opportunity)
  ✓ Signal confidence: 0.78 (≥0.6)
  ✓ Contact completeness: PASS
  ✓ Classification: consulting (0.82)
  
Step 3: Drafting Email...
  → Searching Gmail for prior context...
    Found: 2 prior threads with Dr. Smith
  → Generating warm follow-up email
  
Step 4: Quality Gate (Email)
  ✗ FAIL: Opens with sales pitch
  → Iteration 1: Refining...
  ✓ PASS: Value-first opening, clear CTA
  
Step 5: Drafting Proposal (score: 72 ≥ 60)
  ✓ Proposal generated
  ✓ Quality Gate: PASS

Step 6: Logging...
  → Updated progress.txt
  → Opportunity saved

Iteration 3 complete: PASSED

---

FINAL REPORT
━━━━━━━━━━━━

Opportunities Found: 15
  - High Priority (≥70): 4
  - Medium (40-69): 7
  - Low (<40): 4

Drafts Generated:
  - Emails: 11 (4 cold, 5 warm, 2 re-engagement)
  - Proposals: 4

Quality Gate Results:
  - Pass on first try: 8
  - Pass after refinement: 5
  - Skipped (low confidence): 7

Outputs:
  - Dashboard: content/docs/bizdev-dashboard-2026-01-16.html
  - Email drafts: .bizdev/drafts/emails/
  - Proposals: .bizdev/drafts/proposals/

Learnings captured in: .bizdev/progress.txt
```

---

## Configuration

### Required MCP Servers

Configure these in `.mcp.json`:

```json
{
  "mcpServers": {
    "google-drive": {
      "command": "npx",
      "args": ["ts-node", "mcp-servers/google-drive/src/index.ts"],
      "env": {
        "GOOGLE_SERVICE_ACCOUNT_PATH": "path/to/service-account.json"
      }
    },
    "gmail": {
      "command": "npx",
      "args": ["ts-node", "mcp-servers/gmail/src/index.ts"],
      "env": {
        "GOOGLE_SERVICE_ACCOUNT_PATH": "path/to/service-account.json",
        "GMAIL_USER_EMAIL": "your-email@domain.com"
      }
    }
  }
}
```

### Score Thresholds

| Setting | Default | Description |
|---------|---------|-------------|
| `email_score_threshold` | 40 | Min confidence to draft email |
| `proposal_score_threshold` | 60 | Min confidence to draft proposal |
| `lookback_months` | 6 | How far back to scan |

---

## Key Differences from v1

| Aspect | v1 (Original) | v2 (Iterative) |
|--------|---------------|----------------|
| Execution | Single-pass | Iterative with retries |
| Quality | None | Explicit gates per output |
| Drafts | Manual | Automatic with evaluation |
| Context | Per-run | Persisted in progress.txt |
| Subagents | None | Fresh context for drafting |
| Email Search | Basic | Deep search for conversation history |
| Audit | None | Full session changelogs |
| Learning | None | Patterns compound in progress.txt |
| **Context Sources** | Single source | **Unified: Transcripts + Emails cross-referenced** |

---

## Related Skills

| Skill | Integration |
|-------|-------------|
| `proposal-generator` | HTML proposal creation |
| `edusales-writer` | Email drafting patterns |
| `document-studio` | Design system, brand guidelines |
| `outreach-responder` | LinkedIn/email response crafting |

---

## CRITICAL: Comprehensive Data Extraction (Lessons Learned 2026-02-04)

### The Problem: Data Gaps Between Scans

On Feb 4, 2026, we discovered that the "new" scan methodology was missing significant data compared to the Jan 24 scan:

| Metric | Old Scan (Jan 17-24) | New Scan (Feb 4) |
|--------|----------------------|------------------|
| Transcripts Found | 196 | 36 |
| Opportunities | 251 | 24 |
| Unique Contacts | 144 | ~30 |
| Eric Huynh | ✅ Present | ❌ Missing |

**Root Cause:** The transcript discovery logic was too restrictive, missing 407 of 443 transcripts in Google Drive.

### Fix: Use Comprehensive Transcript Lists

**ALWAYS use MCP `list_files` with pagination to get ALL transcripts:**

```bash
# Get ALL files from transcript folder (handle pagination if >100)
mcp__google-drive__list_files(folder_id="1CfvHgljboEJy9TB29ZvUp6nIavgODDkI", page_size=1000)
```

**Expected transcript counts:**
- Google Drive folder: 443 total files
- After filtering PDFs with "transcript" in name: ~420
- External (sales) transcripts: ~365
- Internal (product) transcripts: ~87

### Three-Category Task System

The dashboard must track THREE categories from DIFFERENT sources:

| Category | Sources | Example Tasks |
|----------|---------|---------------|
| **Sales/BizDev** | Transcripts + Emails + **Motion Recaps** | Larry Siegel proposal, INEXION demo, Welldercare API |
| **Product Work** | **Motion Recaps** + Slack #ngm-partnership | Build Slack bot, launch directory, upload sessions |
| **Personal/Admin** | **Julie's Daily Slack Messages** + Motion Recaps | Leela's library books, Hawaii itinerary, compound planning |

### CRITICAL: Julie's Daily Priorities (Personal Tasks Source)

**Julie posts daily priority messages in Slack** that contain personal/admin tasks. These are the PRIMARY source for personal task extraction.

**How to extract:**
```bash
# Search Julie's daily messages
mcp__slack__conversations_search_messages(
  search_query="from:julie priorities",
  filter_date_after="2026-01-20",
  limit=30
)
```

**Personal task patterns to extract:**
- "Overdue Books of Leela need to return" → Library books
- "Finalized Itinerary for Hawaii Trip" → Travel planning
- "Check Leela's camp Activity for Summer Break" → Summer camp booking
- "Coordinate prenatal massage for Nithya" → Family appointments
- "Babysitter - Please confirm..." → Childcare coordination
- "Shades Installation follow up" → Home improvement
- "Complete Superpower tax forms" → Finance/legal
- "IMLCC fingerprinting / LiveScan" → Medical licenses

### CRITICAL: Motion Recaps (Meeting Notes Source)

**Motion sends email recaps after every meeting** with summaries and action items. These are a comprehensive source for ALL THREE categories.

**How to fetch:**
```bash
# Search for Motion recap emails (last 3 months)
gog gmail search "from:motion subject:recap after:2025/11/01" --max=100

# Get specific recap content
gog gmail thread <email_id>
```

**Categorization logic:**
- **sales_bizdev** (default): Any external meeting (e.g., "Larry Siegel <> Anant", "INEXION follow up")
- **product_work**: Internal team meetings (keywords: "Weekly Team", "Albert", "Sarthak", "Jeph", "Markus", "Julie 1:1", "AI Working Session")
- **personal_admin**: Personal meetings (keywords: "Compound Planning", "family", "personal")

**Extraction script:** `.bizdev/scripts/process_motion_recaps.py`

**Output file:** `.bizdev/motion-recaps-extracted.json`

**Feb 2026 scan results:**
| Category | Count |
|----------|-------|
| Sales/BizDev meetings | 79 |
| Product Work meetings | 20 |
| Personal/Admin meetings | 1 |
| **Total Recaps** | 100 |
| **Unique Contacts** | 111 |
| **Action Items** | 26 |

**Key contacts discovered via Motion recaps:**
- Eric Huynh (Erik-Anant Catch Up)
- Philip Deibel
- Umar Latif
- Akshay Ahooja (Alan Mottram connection)
- Birendra Singh
- Craig (Twin Health)
- Susan (Sloan Ketter)
- Paolo Trivellato
- Ian Wendt (INEXION)
- Kanishka Acharya (Welldercare)

**Action items to merge:**
- "build a Claude/Moldbot in Slack" → product_work
- "launch the conference site and directory listing" → product_work
- "share the API spec and sample executions" → sales_bizdev (Welldercare)
- "review investing strategy after receiving a bonus" → personal_admin

### Legacy Data Reference

The old comprehensive scan data exists at:
```
.ai-workspaces/.bizdev/
├── contacts_deduplicated.json  # 139 contacts, 195 opportunities
├── transcript_queue.json       # 196 transcript entries
├── deep_scan_results/          # 196 individual extraction JSONs
└── run_deep_scan.py           # Original Haiku extraction script
```

**If current data seems incomplete, cross-reference with this legacy data.**

### State Files (Updated)

```
.bizdev/
├── opportunities-enhanced.json     # Sales/BizDev opportunities (204+)
├── task-state.json                 # Product + Personal tasks
├── deep-scan-transcripts.json      # Current transcript list
├── deep-scan-transcripts-comprehensive.json  # Full 420 transcripts
└── crm-state.json                  # Unified CRM state

content/docs/
└── bizdev-dashboard-comprehensive.html  # All 3 categories dashboard
```

### Verification Checklist

Before considering a scan "complete", verify:

- [ ] Transcript count ≥ 400 (not just 36)
- [ ] Opportunities count ≥ 150 (not just 24)
- [ ] Eric Huynh present in contacts
- [ ] Julie's daily Slack messages scanned for personal tasks
- [ ] **Motion recaps processed (100 expected for 3-month lookback)**
- [ ] Product tasks from Motion recaps included (20+ from Weekly Team meetings)
- [ ] Sales contacts from Motion recaps included (79 external meetings)
- [ ] All three categories populated in dashboard

### Migration Script (if needed)

To migrate old data to new system:
```python
import json

# Load old data
with open('.ai-workspaces/.bizdev/contacts_deduplicated.json') as f:
    old_contacts = json.load(f)

# Load current data
with open('.bizdev/opportunities-enhanced.json') as f:
    current = json.load(f)

# Find missing contacts
current_names = {o['contact_name'] for o in current.get('opportunities', [])}
for contact in old_contacts:
    if contact['name'] not in current_names:
        # Migrate this contact's opportunities
        for opp in contact.get('opportunities', []):
            # Add to current system
            pass
```

---

## Troubleshooting

### "Folder ID not found"
- Verify the folder ID is correct (from URL)
- Ensure service account has access to the folder
- Share the folder with the service account email

### "No opportunities detected"
- Check that transcripts contain relevant keywords
- Verify lookback window covers the file dates
- Try expanding search terms

### "Gmail connection failed"
- Verify domain-wide delegation is configured
- Check GMAIL_USER_EMAIL is set correctly
- Ensure service account has Gmail API scope

---

## CRITICAL: PDF Transcript Handling

### The Problem

The MCP Google Drive `get_file_content` tool returns **raw PDF binary data** when fetching PDF files. This binary data gets corrupted during JSON serialization, resulting in "needs OCR" or "corrupted PDF" errors even when the PDF contains extractable text.

**Symptoms:**
- `%PDF-1.3` header visible in raw content
- pdfplumber returns "Data-loss while decompressing corrupted data"
- Files incorrectly logged as "image-based, needs OCR"

### The Solution: Use `gog drive download`

**ALWAYS use the `gog` CLI tool to download PDF transcripts** instead of MCP `get_file_content`. This preserves binary integrity.

```bash
# Download PDF with proper binary handling
GOG_KEYRING_PASSWORD=ngm GOG_ACCOUNT=anant@nextgenerationmedicine.co \
  gog drive download FILE_ID --out /tmp/transcript.pdf

# Then extract text with pdfplumber
python3 -c "
import pdfplumber
with pdfplumber.open('/tmp/transcript.pdf') as pdf:
    text = ''
    for page in pdf.pages:
        text += page.extract_text() or ''
    print(text)
"
```

### Workflow for Processing Transcripts

1. **List transcripts** via MCP `list_files` (this works fine for metadata)
2. **Download each PDF** via `gog drive download FILE_ID --out /tmp/NAME.pdf`
3. **Extract text** via `pdfplumber.open()`
4. **Analyze with Haiku subagent** passing the extracted text

### Example Implementation

```python
import subprocess
import pdfplumber
import os

def download_and_extract_pdf(file_id: str, name: str) -> str:
    """Download PDF via gog CLI and extract text."""
    output_path = f"/tmp/{name}.pdf"

    # Download with proper binary handling
    result = subprocess.run([
        "gog", "drive", "download", file_id, "--out", output_path
    ], capture_output=True, text=True, env={
        **os.environ,
        "GOG_KEYRING_PASSWORD": "ngm",
        "GOG_ACCOUNT": "anant@nextgenerationmedicine.co"
    })

    if result.returncode != 0:
        raise Exception(f"Download failed: {result.stderr}")

    # Extract text
    with pdfplumber.open(output_path) as pdf:
        text = ""
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    return text
```

### When MCP `get_file_content` is OK

- **Google Docs** (text/plain export) - Works fine
- **Plain text files** (.txt, .vtt) - Works fine
- **JSON files** - Works fine

**Never use MCP for:**
- PDF files (use `gog drive download`)
- Binary files (images, etc.)

### Updating the PDF Extraction Issues Log

If a PDF fails extraction, log it to `.bizdev/pdf-extraction-issues.json`:

```json
{
  "extraction_issues": [
    {
      "name": "Meeting-Name-Date",
      "file_id": "DRIVE_FILE_ID",
      "issue": "Description of the issue",
      "resolution": "Use gog drive download instead of MCP"
    }
  ]
}
```

### "Quality gate keeps failing"
- Review the specific failures in the output
- Check the evaluation_rubrics.md for criteria
- Try the suggestions provided by the gate

### Resume interrupted session
```
/bizdev-opportunity execute
```
This loads the existing PRD and continues from the last pending task.

---

## NEW: Master Command Center (v5.0)

The Master Command Center provides a unified view of ALL tasks, opportunities, and initiatives across the operational landscape.

### Quick Commands - Scan Recent

```bash
# Scan recent emails and Motion recaps (default 7 days)
/bizdev-opportunity scan-recent

# Custom lookback period
/bizdev-opportunity scan-recent --days 14

# Scan only Motion recaps
/bizdev-opportunity scan-recent --motion-only

# Scan only emails
/bizdev-opportunity scan-recent --email-only

# Start HTTP server for dashboard button integration
/bizdev-opportunity scan-server
```

### Quick Commands - Command Center

```bash
# Full system scan (Slack, Email, Motion, Repo)
/bizdev-opportunity command-center scan

# Scan specific sources
/bizdev-opportunity command-center scan --slack-only
/bizdev-opportunity command-center scan --motion-only
/bizdev-opportunity command-center scan --bizdev-only

# Task management
/bizdev-opportunity command-center add "Task title" --owner jeff --category product
/bizdev-opportunity command-center complete task-001

# Team views
/bizdev-opportunity command-center queue jeff
/bizdev-opportunity command-center queue julie
/bizdev-opportunity command-center queue ayen

# Generate dashboard
/bizdev-opportunity command-center dashboard
```

### CLI Scripts

```bash
# Unified scan with HTTP server support
python3 .bizdev/scripts/scan_recent.py                    # Default 7 days
python3 .bizdev/scripts/scan_recent.py --days 14          # Custom lookback
python3 .bizdev/scripts/scan_recent.py --server           # Start HTTP server
python3 .bizdev/scripts/scan_recent.py --port 8765        # Custom server port

# Master scanner for multi-source tasks
python3 .bizdev/scripts/master_scanner.py scan            # Full scan
python3 .bizdev/scripts/master_scanner.py scan --slack-only
python3 .bizdev/scripts/master_scanner.py scan --motion-only
python3 .bizdev/scripts/master_scanner.py queue jeff      # Show Jeff's tasks
python3 .bizdev/scripts/master_scanner.py add "Task" --owner julie --category backend

# Generate unified dashboard
python3 .bizdev/scripts/generate_master_dashboard.py
```

### Dashboard URLs

- **Master Command Center**: `content/docs/master-command-center.html`
- **BizDev Dashboard**: `content/docs/bizdev-dashboard-comprehensive.html`

### Data Files

- **Master Tasks**: `.bizdev/master-tasks.json`
- **Opportunities**: `.bizdev/opportunities-enhanced.json`
- **Motion Recaps**: `.bizdev/motion-recaps-extracted.json`
- **Scan State**: `.bizdev/scan-state.json`

### Task Categories

| Category | Default Owner | Color |
|----------|---------------|-------|
| `product` | jeff | Purple |
| `bizdev` | unassigned | Gold |
| `personal` | unassigned | Green |
| `engineering` | ayen | Blue |
| `backend` | julie | Orange |

### Team Structure

| Member | Role | Slack Channels |
|--------|------|----------------|
| **Jeff** | Product & Strategy | #product |
| **Julie** | Backend & Transcripts | #backend |
| **Ayen** | Engineering | #dev |

### HTTP Server Endpoints

When running `python3 .bizdev/scripts/scan_recent.py --server`:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/scan-recent` | POST | Full scan (emails + Motion) |
| `/scan-emails` | POST | Email scan only |
| `/scan-motion` | POST | Motion recap scan only |
| `/scan-status` | GET | Return last scan state |

### Slack Task Extraction

The Slack task extractor recognizes these patterns:

```
TODO: <task>
ACTION ITEM: <task>
TASK: <task>
@jeff/@julie/@ayen: <task>
[TASK] <task>
- [ ] <checkbox item>
Can you <verb>...
Please <verb>...
Need to <verb>...
```

Priority keywords:
- **High**: urgent, asap, critical, important, blocker, p0, p1, today, now
- **Medium**: soon, this week, p2, when you can
- **Low**: later, eventually, nice to have, p3, backlog, someday

---

## NEW: Thoroughness Auditor (v5.1)

A cross-verification agent that uses **alternative methods** to audit dashboard data for completeness. It catches gaps the main scanners might miss.

### Quick Commands

```bash
# Full audit across all sources
/bizdev-opportunity audit

# Audit specific source
/bizdev-opportunity audit --source motion
/bizdev-opportunity audit --source bizdev
/bizdev-opportunity audit --source drafts

# Show only gaps (no suggestions)
/bizdev-opportunity audit-gaps
```

### CLI Usage

```bash
# Full audit
python3 .bizdev/scripts/thoroughness_auditor.py audit

# Audit specific source
python3 .bizdev/scripts/thoroughness_auditor.py audit --source motion
python3 .bizdev/scripts/thoroughness_auditor.py audit --source bizdev
python3 .bizdev/scripts/thoroughness_auditor.py audit --source drafts
python3 .bizdev/scripts/thoroughness_auditor.py audit --source cross_reference

# Show only gaps
python3 .bizdev/scripts/thoroughness_auditor.py gaps

# Generate full report
python3 .bizdev/scripts/thoroughness_auditor.py report
```

### What It Checks

| Source | Verification Method |
|--------|---------------------|
| Motion Recaps | Alternative regex patterns for action detection |
| BizDev Opps | Task coverage, stale records, duplicates |
| Drafts | Email/proposal coverage for high-priority opps |
| Cross-Reference | Names in transcripts vs opportunity records |

### Output Files

- **Audit Report**: `.bizdev/audit-report.json`

### Coverage Scores

The auditor calculates coverage scores (0-100%) for each source:
- ✅ **80%+**: Good coverage
- ⚠️ **60-79%**: Needs attention
- ❌ **<60%**: Critical gaps
