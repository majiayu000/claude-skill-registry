---
name: digital-fte-orchestrator
description: |
  Main task processing loop using Claude Code with Ralph Wiggum pattern.
  Use when running the orchestrator, debugging task processing,
  configuring approval workflows, or understanding the task lifecycle.
  NOT when creating individual watchers (use specific watcher skills).
  NOT when debugging specific integrations (use integration-specific skills).
---

# Digital FTE Orchestrator Skill

Core task processing engine with Ralph Wiggum loop pattern.

## Quick Start

```bash
# Normal mode
python src/orchestrator.py

# Process once and exit
python src/orchestrator.py --once

# Dry run (no execution)
python src/orchestrator.py --dry-run

# Via scripts
python scripts/run.py
```

## Task Flow

```
Needs_Action/ → [Claim] → In_Progress/ → [Process] → Done/
                                       ↓
                              Pending_Approval/ (if sensitive)
                                       ↓
                              [Human approves]
                                       ↓
                                  Approved/ → [Execute] → Done/
```

## Work Zones

The orchestrator operates in different modes based on environment:

| Zone | `FTE_ROLE` | Capabilities |
|------|------------|--------------|
| **Cloud** | `cloud` | Read-only, draft creation, analysis |
| **Local** | `local` | Full execution, financial actions, posting |

### Cloud Zone Restrictions
- All sends/posts forced to approval workflow
- Cannot execute financial transactions
- Cannot post to social media directly
- Creates drafts for human review

### Local Zone Powers
- Direct execution of approved tasks
- Financial actions (with audit logging)
- Social media posting
- WhatsApp message sending

## Claim-by-Move Pattern

Atomic task claiming prevents race conditions:

```python
# ✓ CORRECT - Atomic claim
src = Needs_Action / task_file
dst = In_Progress / task_file
src.rename(dst)  # Atomic on same filesystem

# ✗ WRONG - Race condition possible
if task_file in Needs_Action:  # Another agent could claim here!
    process(task_file)
```

## Skill Routing

The orchestrator routes tasks to appropriate skills based on task type:

| Task Type | Skill | Example Trigger |
|-----------|-------|-----------------|
| `email_*` | `sending-emails` | Email draft in queue |
| `whatsapp_*` | `watching-whatsapp` | WhatsApp message request |
| `facebook_*` | `posting-facebook` | Social media post |
| `invoice_*` | `managing-odoo` | Create invoice request |
| `calendar_*` | `managing-calendar` | Meeting request |

## Agentic Intelligence

Integrated with `src/intelligence/agentic_intelligence.py` for:
- Task complexity scoring
- Autonomous decision making
- Learning from outcomes
- Pattern recognition

## Configuration

| Flag | Default | Description |
|------|---------|-------------|
| `--max-iterations` | 10 | Max retries per task |
| `--poll-interval` | 30 | Seconds between polls |
| `--dry-run` | false | Test without execution |
| `--once` | false | Process once and exit |

Environment:
```bash
FTE_ROLE=local|cloud  # Determines work zone
```

## CEO Briefing Integration

Orchestrator generates briefings via `src/reports/ceo_briefing.py`:
- Weekly activity summaries
- Key metrics and KPIs
- Task completion rates
- Pending approvals count

## Verification

Run: `python scripts/verify.py`

## Related Skills

- `sending-emails` - Email sending patterns
- `watching-whatsapp` - WhatsApp monitoring
- `managing-calendar` - Calendar management
- `managing-odoo` - Accounting operations
- `posting-facebook` - Social media posting
- `generating-ceo-briefing` - Executive reports
