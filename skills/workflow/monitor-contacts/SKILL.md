---
name: monitor-contacts
description: >
  Always-on contact freshness monitoring service. Periodically re-researches
  stale contacts via /dogpile, detects job changes and company news, and
  alerts via Discord when significant changes are found.
allowed-tools: ["Bash", "Read", "Write", "Task"]
triggers:
  - monitor contacts
  - contact monitoring
  - watch contacts
  - track contacts
  - contact freshness
  - are my contacts current
  - stale contacts
  - contact changes
metadata:
  short-description: "Always-on contact freshness monitoring with change detection"
  author: "Graham"
  version: "0.1.0"

provides:
  - monitor-contacts
composes: [, task-monitor]
---

# monitor-contacts

Always-on contact freshness monitoring service. Runs on a schedule (via
`/scheduler`) to keep contact profiles current, detect significant changes
(job moves, company news, acquisitions), and alert via Discord.

## Why This Exists

Contact enrichment is a point-in-time snapshot. People change jobs. Companies
get acquired. Programs end. This service ensures your contact intelligence
stays fresh without manual re-research.

## Continuous Operation (Non-Negotiable)

This skill is **always-on**. It:
- Runs on its configured schedule indefinitely — it NEVER stops unless explicitly halted by the user
- The agent MUST NOT stop and wait for the human to ask for status or remember to check
- If a cycle fails, diagnose the failure, attempt auto-repair, and continue
- Only escalate to the human if genuinely blocked after exhausting /dogpile research
- Gracefully handles restarts and maintains state across cycles
- Is designed for multi-day/week/month autonomous operation

**Anti-pattern**: Reporting status and waiting for the human to ask "what next?" is UNACCEPTABLE. The agent must proactively fix issues and continue the monitoring loop.

## Architecture

```
┌──────────────────────────────────────────────────────┐
│              monitor-contacts                         │
│  - Scheduled via /scheduler (nightly or weekly)      │
│  - Staleness-based priority queue                    │
│  - Change detection engine                           │
│  - Discord alerting                                  │
└──────────────────────────────────────────────────────┘
         │                    │                    │
    ┌────┴─────┐        ┌────┴─────┐        ┌────┴──────┐
    │ Staleness │        │ Change   │        │ Alert     │
    │ Scanner   │        │ Detector │        │ Engine    │
    ├──────────┤        ├──────────┤        ├───────────┤
    │ Age check │        │ Diff old │        │ Discord   │
    │ Priority  │        │ vs new   │        │ webhook   │
    │ queue     │        │ profile  │        │ Summary   │
    └──────────┘        └──────────┘        └───────────┘
```

## Commands

```bash
# Start monitoring (foreground)
./run.sh monitor

# Start as background service
./run.sh start

# Stop background service
./run.sh stop

# Check service status
./run.sh status

# Run one monitoring cycle manually
./run.sh cycle

# Show contact freshness report
./run.sh report

# Show recent changes
./run.sh changes --since 7d

# Configure monitoring
./run.sh config --interval weekly --budget 10 --alert-channel contacts
```

## Monitoring Cycle

Each cycle:

```
1. SCAN — Find contacts with staleness > threshold
   ├── Default threshold: 30 days
   ├── High-priority contacts: 14 days
   └── Low-priority contacts: 90 days

2. PRIORITIZE — Sort by staleness + importance
   ├── Contacts with upcoming meetings/events → top
   ├── Contacts in active deals/programs → high
   └── Cold contacts → low

3. RESEARCH — Re-enrich top N stale contacts
   ├── Uses /discover-contacts research pipeline
   ├── Budget-limited (default: 10 contacts per cycle)
   └── Rate-limited to avoid API exhaustion

4. DIFF — Compare new profile vs stored profile
   ├── Job title changed?
   ├── Company changed?
   ├── New publications?
   ├── Company news (funding, acquisition)?
   └── Email likely stale?

5. ALERT — Notify on significant changes
   ├── Discord embed with change summary
   ├── Color-coded: green (positive), yellow (neutral), red (attention)
   └── Weekly digest option
```

## Change Detection

The change detector tracks these signals:

| Signal | Severity | Example |
|--------|----------|---------|
| **Job change** | High | "John Rushby moved from SRI to DARPA" |
| **Company acquisition** | High | "Galois acquired by [company]" |
| **New DARPA program** | Medium | "Contact's company awarded new DARPA contract" |
| **New publication** | Low | "3 new papers on ArXiv" |
| **Email bounce** | Medium | "Email domain changed" |
| **Company funding** | Medium | "Series B announced" |
| **Company layoffs** | High | "Major restructuring reported" |
| **Conference appearance** | Low | "Speaking at [event]" |

## Discord Alerts

### Individual Change Alert
```
Contact Change Detected
━━━━━━━━━━━━━━━━━━━━━━

John Rushby
  Was: Senior Computer Scientist @ SRI International
  Now: Program Manager @ DARPA I2O

  Change Type: Job Change (High Priority)
  Detected: 2026-02-12
  Source: LinkedIn via Brave Search

  Action: Update contact record and reach out?
```

### Weekly Digest
```
Contact Monitor — Weekly Digest
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Contacts Checked: 15/60
Changes Found: 3

  Job Changes (1):
    • John Rushby: SRI → DARPA

  Company News (1):
    • Galois, Inc.: Awarded DARPA PROOFS Phase 2

  New Publications (1):
    • Natasha Neogi: 2 new papers on ArXiv

  Stale Contacts (5):
    • 5 contacts not refreshed in 60+ days

Next cycle: 2026-02-19
Budget used: 8/10 /dogpile calls
```

## Priority Tiers

Contacts can be tagged with priority tiers:

```yaml
priority_tiers:
  critical:    # Check every 14 days
    - contacts with active deals
    - contacts in current programs
  standard:    # Check every 30 days (default)
    - general professional network
  cold:        # Check every 90 days
    - historical contacts
    - inactive relationships
```

## Schedule Configuration

```yaml
# monitor-contacts config
schedule:
  interval: weekly          # daily, weekly, biweekly, monthly
  day: sunday               # for weekly
  time: "02:00"             # off-peak
  budget_per_cycle: 10      # max /dogpile calls
  concurrency: 2            # parallel research

alerts:
  discord_channel: contacts # channel name
  webhook_url: ${DISCORD_CONTACTS_WEBHOOK}
  digest: weekly            # individual, weekly, both

thresholds:
  critical_staleness: 14    # days
  standard_staleness: 30    # days
  cold_staleness: 90        # days
```

## Memory + Taxonomy Integration

The skill integrates with the shared memory and taxonomy systems via
`memory_integration.py` for longitudinal contact freshness tracking:

- **Pre-hook (`recall_contact_changes`)**: Before checking a contact, recalls prior
  change history to surface patterns (e.g., frequent job moves, company instability).
- **Post-hook (`learn_contact_change`)**: After detecting a change, stores the change
  event (person, type, old/new values, severity) to memory for trend tracking.
- **Bridge keywords**: Precision, Resilience, Fragility, Corruption, Loyalty, Stealth
  (tuned to contact monitoring domain).
- **Tags**: `["monitor_contacts", person_name, "drift_tracking"] + bridges`

Gracefully degrades if `common.memory_client` or `taxonomy/taxonomy.py` are unavailable.

## File Structure

```
monitor-contacts/
  SKILL.md                   # This file
  run.sh                     # Shell entry point
  sanity.sh                  # Sanity checks
  config.py                  # Paths, constants, skill references
  memory_integration.py      # Memory + Taxonomy hooks
```

## Storage

```
/mnt/storage12tb/media/personas/references/
├── darpa_arcos_contacts.csv          # Source contacts
├── darpa_arcos_enriched.yaml         # Current enriched profiles
├── company_profiles/                 # Company intelligence
├── change_log/                       # Historical changes
│   ├── 2026-02/
│   │   ├── 2026-02-12_changes.json
│   │   └── 2026-02-19_changes.json
│   └── ...
├── enrichment_log.json               # Audit trail
└── monitor_config.yaml               # Service configuration
```

## Integration with /scheduler

```bash
# Register with scheduler for weekly runs
/scheduler add monitor-contacts --cron "0 2 * * 0" --budget 10

# Or via run.sh
./run.sh start --schedule weekly
```

## Leveraged Skills

| Skill | Purpose |
|-------|---------|
| `/discover-contacts` | Contact research pipeline |
| `/dogpile` | Multi-source deep research |
| `/memory` | Store/recall enriched profiles |
| `/ops-discord` | Discord webhook alerts |
| `/scheduler` | Scheduled execution |
| `/task-monitor` | Progress tracking |
| `/ops-sam-gov` | Government contract monitoring |
| `/ops-darpa` | DARPA program tracking |

## Task-Monitor Integration

The monitoring service registers with `/task-monitor`:

```json
{
  "task_id": "monitor-contacts-cycle",
  "description": "Contact freshness monitoring cycle",
  "completed": 8,
  "total": 15,
  "stats": {
    "contacts_checked": 8,
    "changes_found": 2,
    "dogpile_calls": 6,
    "budget_remaining": 4
  }
}
```

## Privacy & Ethics

- All research uses publicly available information only
- No automated outreach or email sending
- Change detection is passive (no login scraping)
- Data stored locally on 12TB drive only
- Audit trail tracks all research activity
- Respect rate limits on all sources
