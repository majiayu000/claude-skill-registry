---
name: orchestrator-agent
description: Master coordinator for Unite-Hub workflows. Routes tasks to specialists, manages multi-agent pipelines, maintains context across runs, handles errors, and generates system reports. The brain of the automation system.
---

# Orchestrator Agent Skill

## Overview

The Orchestrator Agent is the **command center** of Unite-Hub. It:
- Receives high-level instructions from users
- Breaks tasks into specialist workflows
- Coordinates email-agent and content-agent
- Maintains system state and memory
- Reports on progress and health

## Core Workflows

### Workflow 1: Email Processing → Content Generation Pipeline

**User Input:**
"Process all emails and generate followup content for warm leads"

**Orchestrator Steps:**

1. **Log workflow start**
```
   POST audit: action="workflow_start", resource="email_content_pipeline"
```

2. **Execute Email Agent**
```
   - Call: npm run email-agent
   - Wait for completion
   - Capture: processed count, errors, audit logs
```

3. **Evaluate Results**
```
   IF processed > 0:
     Continue to step 4
   ELSE:
     Notify user "No new emails to process"
     Exit workflow
```

4. **Update Contact Scores**
```
   FOR each processed email:
     - Get updated contact AI score
     - Filter: aiScore >= 70 (warm leads)
     - Store in memory for content generation
```

5. **Execute Content Agent**
```
   - Call: npm run content-agent
   - Wait for completion
   - Capture: generated count, content types
```

6. **Validate Output**
```
   Query generatedContent:
   - Count drafts created
   - Verify all have status="draft"
   - Check aiModel="sonnet"
```

7. **Generate Report**
```
   Output summary with:
   - Emails processed: X
   - Contacts updated: X
   - Content generated: X
   - High-priority leads identified: X
   - Recommended next actions
```

8. **Log workflow completion**
```
   POST audit: action="workflow_complete", status="success"
```

### Workflow 2: Content Approval → Scheduling

**User Input:**
"Approve top 5 content drafts and schedule for sending"

**Orchestrator Steps:**

1. **Fetch pending approvals**
```
   GET generatedContent:
   - status="draft"
   - Sort by contact.aiScore DESC
   - Limit: 5
```

2. **Validate contacts**
```
   FOR each content:
     - Get contact details
     - Verify status="prospect" (ready to receive)
     - Check lastInteraction < 30 days (recent)
```

3. **Approve content**
```
   FOR each draft:
     POST mutation: content.approve(userId=system)
```

4. **Update contact status**
```
   FOR each contact:
     - Mark nextFollowUp = NOW + 7 days
     - Update lastInteraction = NOW
```

5. **Log audit trail**
```
   FOR each action:
     POST audit event with full details
```

6. **Generate scheduling report**
```
   Output:
   - Total approved: 5
   - Scheduled send time: [user preference]
   - Expected delivery: [time range]
   - Tracking enabled: yes/no
```

### Workflow 3: System Health Check

**User Input:**
"Run system audit"

**Orchestrator Steps:**

1. **Check data integrity**
```
   Verify:
   - All organizations active
   - All users have valid roles
   - All contacts have valid status
   - All emails properly linked
```

2. **Audit recent activities**
```
   Query auditLogs (last 24h):
   - Total actions: X
   - Errors: X
   - Error rate: X%
   - Failed agents: [list]
```

3. **Database health**
```
   Check:
   - All indexes working
   - No orphaned records
   - Data consistency
   - Storage usage
```

4. **Agent performance**
```
   FOR each agent:
     - Last run: [timestamp]
     - Success rate: X%
     - Avg processing time: Xms
     - Last error: [if any]
```

5. **Generate health report**
```
   Output:
   ✅ System Status: [HEALTHY|WARNING|CRITICAL]

   Data Integrity: ✅
   - Organizations: X (active)
   - Users: X
   - Contacts: X
   - Emails: X

   Recent Performance (24h):
   - Actions processed: X
   - Success rate: X%
   - Errors: X

   Agent Status:
   - email-agent: ✅ (last run: Xh ago)
   - content-agent: ✅ (last run: Xh ago)
   - orchestrator: ✅ (self-check)

   Recommendations:
   1. [Action 1]
   2. [Action 2]
```

## Memory Management

The Orchestrator uses **persistent memory** to track state across runs:
```
Memory keys stored in aiMemory table:

orchestrator:workflow_state
  - Current workflow ID
  - Status (running, completed, error)
  - Started at timestamp
  - Expected duration

orchestrator:last_email_run
  - Timestamp of last email agent run
  - Emails processed count
  - Errors encountered

orchestrator:last_content_run
  - Timestamp of last content agent run
  - Content generated count
  - Content types distribution

orchestrator:pipeline_cache
  - Contact scores after email run
  - High-priority contacts identified
  - Contacts needing followup
```

## Error Handling Strategy

### Error Levels

**Level 1: Recoverable**
- Single email fails to process
- Claude API timeout (retry)
- Network blip

**Action:** Log error, skip item, continue

**Level 2: Significant**
- Contact data missing/invalid
- Email agent fails 50% of batch
- Content generation rate < 80%

**Action:** Log error, retry with reduced batch, alert user

**Level 3: Critical**
- Database connection lost
- Claude API down
- All agents failing

**Action:** Log error, halt workflow, alert immediately

### Error Logging
```
FOR each error:
  POST audit mutation:
  - action: "[agent]_error"
  - status: "error"
  - details: { error_message, stack_trace, context }
  - errorMessage: [human readable]
```

## Command Reference

### Start Full Pipeline
```
User: "Run full workflow: process emails and generate content"

Orchestrator:
1. Execute email-agent
2. Wait for completion
3. Evaluate results
4. Execute content-agent
5. Generate report
6. Log completion
```

### Check Status
```
User: "What's the status of pending content?"

Orchestrator:
1. Query generatedContent (status="draft")
2. Count by contentType
3. List by contact aiScore
4. Report summary
```

### Health Check
```
User: "Run system audit"

Orchestrator:
1. Check all tables
2. Verify data integrity
3. Query recent audit logs
4. Check agent health
5. Generate report
```

### Manual Approval
```
User: "Approve all content for John and Lisa"

Orchestrator:
1. Find content for specified contacts
2. Validate readiness
3. Approve each draft
4. Update contact records
5. Generate audit trail
```

## Report Templates

### Pipeline Completion Report
```
✅ Pipeline Execution Complete

Timeline:
- Start: [timestamp]
- Email processing: [duration]
- Content generation: [duration]
- Total runtime: [duration]

Results:
- Emails processed: X
- New contacts created: X
- Contacts updated: X
- Content generated: X
- Errors: X

By type:
- Followup emails: X
- Proposals: X
- Case studies: X

High-Priority Leads (>80 score):
1. John Smith (TechStartup) - proposal generated
2. Lisa Johnson (eCommerce) - followup generated

Next Actions Recommended:
1. Review and approve X pending content drafts
2. Schedule sends for X contacts
3. Track performance metrics for X campaigns

System Health: ✅ All systems nominal
```

## Integration Points

The Orchestrator coordinates with:
- **Email Agent** - email processing pipeline
- **Content Agent** - content generation pipeline
- **Convex Database** - state persistence
- **Claude API** - advanced reasoning (future)
- **Audit System** - compliance tracking
- **Memory System** - workflow state
