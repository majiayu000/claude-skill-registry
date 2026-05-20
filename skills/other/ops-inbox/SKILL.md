---
name: ops-inbox
description: Process pending Brikette customer emails and generate draft responses using MCP tools
---

# Process Emails

Process customer emails for Hostel Brikette, generating intelligent draft responses using the knowledge base and MCP tools.

## When to Use

Run this skill when you want to process customer inquiry emails for Brikette:
- Morning email triage (recommended: 09:00 Italy time)
- Afternoon follow-up (recommended: 17:00 Italy time)
- Ad-hoc when notified of urgent inquiry

## Prerequisites

- MCP server running locally with Gmail tools enabled
- Gmail API credentials configured for Pete's account
- Network access to Gmail API
- Fallback CLI available: `scripts/ops/create-brikette-drafts.py`

## Workflow

### 0. Mandatory MCP Preflight (Fail Fast)

Before any inbox processing, run:

```typescript
health_check({ strict: false })
```

Then enforce these rules:

1. If this call fails with tool-resolution/transport errors (for example `Tool not found`, unknown tool, or MCP disconnect), stop immediately.
2. Do not continue to `gmail_organize_inbox` or any other MCP call in that session.
3. Tell the user this is a stale/continued session with a dead MCP registry and require a fresh Claude Code session.
4. Recovery command:
   ```bash
   claude
   ```
   Then rerun `/ops-inbox`.
5. If preflight returns `status: "unhealthy"`, stop and show the failing checks/remediation.
6. If preflight returns `status: "degraded"`, continue only with explicit user approval.

After `health_check` passes, run the reconcile step:

```typescript
gmail_reconcile_in_progress({ dryRun: false, staleHours: 2 })
```

Handle the result as follows:
- **If the call throws or returns an error:** log a warning (`⚠️ Reconcile failed: <error message> — continuing`) and proceed. This step is fail-open and must never block the inbox run.
- **If `counts.routedRequeued > 0`:** surface this line in the preflight output:
  ```
  ♻️ N stuck email(s) recovered and re-queued.
  ```
  (where N is the value of `counts.routedRequeued`)
- **If all counts are zero:** say nothing about reconcile — preflight output is silent.

If the user wants dry-run fallback (or MCP remains unavailable), queue drafts locally instead of writing Gmail drafts:

```bash
python3 scripts/ops/create-brikette-drafts.py \
  --input <path-to-drafts.json> \
  --dry-run \
  --queue-file data/email-fallback-queue/<timestamp>-ops-inbox.jsonl
```

> **NOTE:** Dry-run and Python-fallback sessions produce no signal events. This is expected — those sessions are excluded from calibration data and will not appear in `draft_signal_stats` counts.

### 1. Run Inbox Organize Cycle

First, run an inbox organize pass for unread emails. This does a garbage/sort cycle:
- trashes known garbage patterns
- labels likely customer inquiries as `Brikette/Queue/Needs-Processing`

```
Organizing unread inbox...
```

Call the tool:
```typescript
gmail_organize_inbox({ limit: 500 })
```

Then briefly report the result:
- scanned threads
- trashed count
- needs-processing count
- promotional count
- spam count
- deferred count
- deferred sender email list (for user instruction on future routing rules)

### 2. Check Email Queue

Use the `gmail_list_pending` MCP tool to fetch pending emails:

```typescript
gmail_list_pending({ limit: 20 })
```

If no pending emails, inform the user:
```
No pending emails in your queue. You're all caught up!
```

### 3. Display Queue Summary

Present emails in a summary table:

```markdown
## Pending Emails (N total)

| # | From | Subject | Received | Type |
|---|------|---------|----------|------|
| 1 | maria@example.com | Availability June 15-18? | 2h ago | Inquiry |
| 2 | john@example.com | RE: Booking confirmation | 4h ago | Reply |
...

Actions:
- "Process all" - work through queue in order
- "Process #1" - handle specific email
- "Skip #3" - mark as spam/not-customer
- "Defer #5" - move to deferred manual-review label
- "Done" - finish session
```

Classify emails by type:

**Needs Draft Response:**
- **Inquiry** - New customer question (availability, pricing, etc.)
- **Reply** - Response to previous thread requiring answer
- **FAQ** - Question answerable from knowledge base

**No Draft Needed:**
- **Informational** - Customer providing info, no reply needed (arrival time, "thanks", confirmation)
- **Promotional** - Marketing/newsletters from OTAs, suppliers, services
- **Not-Customer** - Irrelevant, wrong recipient, or automated bounce

**Special Handling:**
- **Complex** - Multi-part, complaint, or unusual request (defer for careful handling)
- **Spam** - Suspicious, phishing, or unwanted

### 4. Process Individual Emails

When user selects an email to process:

1. **Fetch full details** using `gmail_get_email`:
   ```typescript
   gmail_get_email({ emailId: "...", includeThread: true })
   ```

2. **Run Interpretation stage** using `draft_interpret`:
   ```typescript
   draft_interpret({
     body: email.body.plain,
     subject: email.subject,
     threadContext: email.thread_context
   })
   ```
   Output: `EmailActionPlan` (intents, scenario, agreement status, workflow triggers).

3. **Review the Action Plan**:
   - Confirm `scenario.category`
   - Check detected language
   - Inspect agreement detection status
   - Note workflow triggers (prepayment, T&C, booking monitor)
   - **Check `escalation_required`**: if `true`, do NOT proceed to `draft_generate`. Instead, move the email to `Brikette/Queue/Deferred` via `gmail_mark_processed({ emailId, action: "deferred" })` and stop the pipeline for this email. Inform the user that the email requires human review before a draft can be generated.
   - If classification is ambiguous or context looks odd, default to `deferred` (manual review)

4. **Run Composition stage** using `draft_generate`:
   ```typescript
   draft_generate({
     actionPlan,
     subject: email.subject,
     recipientName: email.from.name,
     prepaymentStep: "first" | "second" | "third" | "success",
     prepaymentProvider: "octorate" | "hostelworld"
   })
   ```
   Output: draft (plain + HTML), template_used, answered_questions, knowledge_sources.

5. **Run Quality Gate** using `draft_quality_check`:
   ```typescript
   draft_quality_check({ actionPlan, draft })
   ```
   Capture the full result including `quality.question_coverage[]`.

   **Gap-Patch Loop** — run this before presenting to the user:

   a. Inspect every entry in `quality.question_coverage[]`:
      - `status: "covered"` → no action needed for that question.
      - `status: "missing"` → the question received zero keyword matches; a patch is required.
      - `status: "partial"` → the question was touched but under the required match threshold; a patch attempt is required.

   b. For each `missing` or `partial` entry, look up the question text against
      `knowledge_summaries` returned by `draft_generate`.
      - If a relevant snippet exists in `knowledge_summaries`: rewrite the relevant
        paragraph to include a source-backed answer. Cite the snippet URI inline
        if helpful. **NEVER invent an answer that has no source snippet.**
      - If no relevant snippet exists for that question: insert the following
        escalation sentence in place of an invented answer:
        > "For this specific question we want to give you the most accurate
        >  answer — Pete or Cristiana will follow up with you directly."
        Do not attempt to paraphrase, guess, or approximate the missing information.

   c. **Hard-rule categories — do NOT modify under any circumstance:**
      - `prepayment` category text (1st/2nd/3rd attempt, cancelled, successful templates)
      - `cancellation` category text (non-refundable, no-show templates)
      These paragraphs are legally and operationally fixed. If a `missing`/`partial`
      entry belongs to a question about prepayment or cancellation policy, escalate
      using the sentence above rather than touching the template wording.

   d. **Partial-subset rule:** When an email contains multiple questions and only
      *some* can be source-backed, patch what can be sourced and escalate the rest
      individually. Do not withhold the draft because one question lacks a snippet —
      produce the best partial draft and flag each unanswered question explicitly
      in the user-facing summary.

   e. After applying all patches (or escalation insertions), re-render `bodyPlain`
      and `bodyHtml`.

6. **LLM Refinement Stage** — after gap-patching, Claude (not a tool call) assesses
   the draft holistically and optionally rewrites it to improve tone, flow, and coverage.
   Then call `draft_refine` to submit and attest the result:

   ```typescript
   draft_refine({
     actionPlan,
     draft_id: draftGenerateResult.draft_id,  // links this refinement to the selection signal event
     rewrite_reason: "<reason>",  // "none" | "style" | "language-adapt" | "light-edit" | "heavy-rewrite" | "missing-info" | "wrong-template"
     originalBodyPlain: patchedBodyPlain,  // post-gap-patch plain text
     refinedBodyPlain: claudeRefinedBodyPlain,  // Claude's rewrite (or same text if no improvement)
   })
   ```

   **Refinement rules:**
   - **Claude is the refinement actor** — Claude rewrites the body; `draft_refine` is the commit
     step only. Never invoke an external model from inside this skill.
   - If Claude judges the draft already strong, pass `refinedBodyPlain === originalBodyPlain` —
     `draft_refine` will return `refinement_applied: false, refinement_source: 'none'`.
   - If Claude rewrites: `refinement_applied: true, refinement_source: 'claude-cli'`.
   - **Hard rules — do NOT modify in refinement:**
     - `prepayment` category text (1st/2nd/3rd attempt, cancelled, successful templates)
     - `cancellation` category text (non-refundable, no-show templates)
     - Never invent policy facts not present in `knowledge_summaries`.
   - If `quality.passed: false` after refinement: inspect `failed_checks`. If resolvable
     by a targeted patch, patch and call `draft_refine` again (max one retry). If still
     failing, escalate to the user with `failed_checks` listed and ask how to proceed.
   - Note: `refinement_source: 'codex'` is reserved for future CLI-based LLMs; it is
     not an active path in this workflow.

7. **Mandatory delivery_status gate** — always check before creating the Gmail draft.

   `draft_generate` returns a `delivery_status` field: `"ready" | "needs_patch" | "blocked"`.

   - `"ready"` — quality passed with no warnings: proceed to `gmail_create_draft`.
   - `"needs_patch"` — quality passed but warnings exist (e.g. partial coverage): review
     warnings, apply any needed patches via `draft_refine`, then proceed.
   - `"blocked"` — quality failed (`quality.passed: false`): inspect `quality.failed_checks`,
     patch and call `draft_refine` (max one retry). If still `"blocked"`, escalate to the
     user with `failed_checks` listed and ask how to proceed. Do **not** call `gmail_create_draft`
     while `delivery_status === "blocked"`. This is a hard gate, not advisory.
   - `partial_question_coverage` warnings after patching are acceptable to proceed
     if the escalation sentence has been inserted; note them in the session summary.

8. **Present to user**:
   ```markdown
   ## Email #1: Availability Inquiry

   **From:** Maria Santos <maria@example.com>
   **Subject:** Availability June 15-18?
   **Received:** 2 hours ago

   ### Content:
   > [Customer's email content]

   ### Classification:
   - **Scenario:** [from EmailActionPlan]
   - **Language:** [from EmailActionPlan]
   - **Agreement:** confirmed / likely / unclear / none
   - **Workflow triggers:** prepayment / terms_and_conditions / booking_monitor

   ### Relevant Knowledge:
   - [Knowledge sources used]

   ### Draft Response:

   ---
   [Generated draft]
   ---

   Actions:
   - "Create draft" - save to Gmail drafts
   - "Edit" - modify the response
   - "Regenerate" - try a different approach
   - "Skip" - don't respond
   - "Flag" - mark for manual handling
   ```

### 5. Handle User Actions

**Create draft** (for Inquiry/Reply/FAQ):
```typescript
gmail_create_draft({
  emailId: "original_email_id",
  subject: "RE: Original Subject",
  bodyPlain: "Plain text version",
  bodyHtml: "HTML version with branding"
})
gmail_mark_processed({ emailId: "...", action: "drafted" })
```

**Create draft (dry-run fallback queue):**

Use this path when:
- MCP tools are unavailable in the current session, or
- user explicitly requests dry-run/no Gmail mutation.

Steps:
1. Build JSON input payload with draft candidates (`emailId`, `to`, `subject`, `recipientName`, `bodyPlain`).
2. Run:
   ```bash
   python3 scripts/ops/create-brikette-drafts.py \
     --input <path-to-drafts.json> \
     --dry-run \
     --queue-file data/email-fallback-queue/<timestamp>-ops-inbox.jsonl
   ```
3. Report the queue file path and do not call `gmail_mark_processed` in dry-run mode.

**Edit request:**
- User provides feedback: "Make it shorter", "More formal", etc.
- Regenerate draft incorporating feedback
- Show revised draft for approval

**Acknowledge** (for Informational emails - no draft needed):
```typescript
gmail_mark_processed({ emailId: "...", action: "acknowledged" })
```
Use when customer provides info but no reply is needed:
- "We'll arrive at 3pm"
- "Thanks, see you tomorrow!"
- "Here's my passport info"
- Booking confirmations from customer

**Promotional** (for marketing/newsletters):
```typescript
gmail_mark_processed({ emailId: "...", action: "promotional" })
```
Archives email and labels `Brikette/Outcome/Promotional` for batch review later.
Use for:
- OTA newsletters (Booking.com, Expedia marketing)
- Travel industry promotions
- Supplier marketing
- Service provider updates

When a promotional/spam false-positive appears in queue:
1. Mark it `promotional` or `spam` immediately.
2. Capture sender email/domain and subject pattern.
3. Add the new exclusion pattern to `packages/mcp-server/src/tools/gmail.ts` (`NON_CUSTOMER_*` constants) so future organize runs stop queueing it.

**Skip** (not relevant/not customer):
```typescript
gmail_mark_processed({ emailId: "...", action: "skipped" })
```

**Spam** (suspicious/unwanted):
```typescript
gmail_mark_processed({ emailId: "...", action: "spam" })
```

**Defer** (complex/needs more info):
```typescript
gmail_mark_processed({ emailId: "...", action: "deferred" })
```
Moves it out of the active queue and labels it `Brikette/Queue/Deferred` for manual follow-up.

### Agreement Detection (T&C workflow)

Agreement detection is high-stakes:
- `confirmed` only for explicit agreement phrases (EN/IT/ES).
- `likely` or `unclear` requires human confirmation before any payment workflow.
- Always check `agreement.requires_human_confirmation`.

If the email includes agreement **and** questions, treat as mixed response:
1. Acknowledge agreement in the draft.
2. Answer all questions.
3. Keep the workflow state as awaiting confirmation if `likely/unclear`.

**Marking agreement_received — reservation code required:**

When marking an email as `agreement_received`, you **must** extract the booking reservation code and pass it as `reservationCode`. This writes activity code 21 to Firebase for all occupants on that booking.

How to extract the reservation code:
1. Check the email subject line — Octorate reservation numbers appear as `#XXXXXX` or plain numbers in subject lines like "Booking confirmation #456789".
2. Check the email body and thread context — look for phrases like "reservation", "booking reference", "conferma prenotazione", "numero prenotazione", or a numeric/alphanumeric code near the hostel name.
3. If the thread context includes a prior outgoing email from Brikette that mentions a booking reference, use that.
4. If no reservation code can be found: log a warning, call `gmail_mark_processed` without `reservationCode` (labels will still be applied), and note in the session summary that the Firebase activity write was skipped.

```typescript
// When agreement is confirmed and reservation code is found:
gmail_mark_processed({
  emailId: "...",
  action: "agreement_received",
  reservationCode: "456789"  // extracted from email thread
})

// When agreement is confirmed but no reservation code found:
gmail_mark_processed({
  emailId: "...",
  action: "agreement_received"
  // No reservationCode — labels applied, Firebase write skipped
})
```

### 6. Processing Informational Emails

When an email is classified as **Informational** (customer providing info, no reply needed):

```markdown
## Email #3: Customer Information

**From:** John Smith <john@example.com>
**Subject:** RE: Booking confirmation
**Received:** 1 hour ago

### Content:
> Thanks for confirming! Just to let you know, we'll be arriving
> around 3pm. See you then!

### Classification:
- **Type:** Informational (arrival time notification)
- **Action Needed:** Note arrival time
- **Draft Required:** No

### Extracted Information:
- **Arrival time:** 3pm (approximately)
- **Guest:** John Smith

### Suggested Action:
Note arrival time in booking system if applicable.

**Mark as acknowledged?** (y/n)
```

Common informational patterns:
- "We'll arrive at [time]" → Note arrival time
- "Thanks!" / "See you soon!" → No action needed
- "Here's my passport/ID" → Record in guest file
- "Dietary requirements: vegetarian" → Note for breakfast
- "We found it okay" → No action needed

### 6. Batch Processing

When user requests batch processing ("Process all FAQ emails"):

1. Filter queue by type
2. Generate drafts for all matching emails
3. Show summary:
   ```markdown
   ## Batch Processing: 4 FAQ Emails

   1. "Check-in time question" -> Draft created
   2. "Breakfast included?" -> Draft created
   3. "Pet policy" -> Draft created
   4. "Luggage storage" -> Draft created

   4 drafts created. Review them in Gmail.

   Remaining in queue: 2 emails
   ```

### 7. Session Summary

When user says "Done" or queue is empty:

1. Call `draft_signal_stats` to retrieve event counts for this session.
2. Call `draft_template_review` with `action: "list"` to get pending proposal count.
3. Call `gmail_audit_labels` to check the Brikette label namespace health.
   - If `orphaned.length > 0`: include an **Orphaned labels** warning in the summary listing each orphaned label name. These are unrecognised `Brikette/*` labels that should be reviewed or migrated.
   - If `orphaned.length === 0`: omit the label health section entirely (silent pass).
   - If the call fails: omit the label health section — do not fail the session summary.
4. Output the summary block below.

```markdown
## Session Complete

**Processed this session:**
- 3 drafts created
- 2 emails acknowledged (no reply needed)
- 1 promotional archived
- 1 email deferred

**Drafts ready for review:**
1. RE: Availability June 15-18? (maria@example.com)
2. RE: Check-in time question (guest@hotel.com)
3. RE: Breakfast options (traveler@email.com)

**Acknowledged (info noted):**
- Arrival time 3pm (john@example.com)
- Dietary: vegetarian (jane@example.com)

Remember to review and send drafts in Gmail!

**Deferred for manual review:** 1 email

**Signal health:**
- N selection events · N refinement events · N joined signals this session
- N template proposals pending review
  - [one-line summary per pending proposal, e.g. "T05 check-in: wrong-template (2026-02-20)"]

> ⚠️ **Backlog warning:** >10 pending proposals — run `draft_template_review list` and review.
> _(Remove this line if ≤10 proposals pending.)_

> 💡 **Calibration prompt:** ≥20 joined signals since last calibration — consider running `draft_ranker_calibrate`.
> _(Remove this line if events_since_last_calibration < 20.)_

<!-- Include the following block only when gmail_audit_labels returns orphaned.length > 0: -->
> ⚠️ **Orphaned Gmail labels:** The following unrecognised `Brikette/*` labels exist in Gmail and should be reviewed or removed:
> - [list each orphaned label name on its own line]
```

**Graceful fallback:** If `draft-signal-events.jsonl` or `template-proposals.jsonl` are missing, show `"0 events"` / `"0 proposals pending"` — do not error. If `gmail_audit_labels` fails, omit the label health section.

> **NOTE:** Dry-run and Python-fallback sessions produce no signal events. Show `"0 events"` for those sessions.

## Email Classification Guide

Use these patterns to correctly classify incoming emails:

### Needs Draft Response

**Inquiry** - Customer asking a question:
- "Do you have availability for...?"
- "What are your rates for...?"
- "How do I get to...?"
- "Is breakfast included?"
- Questions about rooms, facilities, policies

**Reply** - Continuing a conversation that needs response:
- Follow-up questions in a thread
- Requests for clarification
- Additional questions after initial response

**FAQ** - Common questions with standard answers:
- Check-in/check-out times
- Parking availability
- Pet policy
- Age restrictions
- Cancellation policy

### No Draft Needed

**Informational** - Customer providing info (acknowledge, no reply):
- "We'll arrive at [time]" → Note arrival
- "Thanks!" / "See you soon!" → No action
- "Here's my passport number" → Record
- "We're vegetarian" → Note dietary
- "Just to confirm, booking #123" → Verify
- "We found it okay, checking in now" → No action
- Positive feedback with no question

**Promotional** - Marketing (archive to Brikette/Outcome/Promotional):
- Booking.com partner newsletters
- Expedia promotions
- Travel industry news
- Supplier marketing
- "Special offer for partners"
- "New features available"
- Software/service provider updates

**Not-Customer** - Skip without reply:
- Wrong recipient
- Automated bounce/delivery failure
- Unsubscribe confirmations
- System notifications not relevant

### Special Handling

**Complex** - Defer for careful handling:
- Complaints or negative feedback
- Refund requests
- Multiple unrelated questions
- Special requests (events, groups)
- Anything emotionally charged
- Legal or liability concerns

**Spam** - Mark as spam:
- Obvious phishing
- Unsolicited sales pitches
- Suspicious links
- "You've won" / lottery scams

### Classification Decision Tree

```
Is it from a real person about Brikette?
├─ No → Is it promotional?
│       ├─ Yes → PROMOTIONAL
│       └─ No → Is it spam?
│               ├─ Yes → SPAM
│               └─ No → SKIP (not-customer)
└─ Yes → Does it contain a question or need a response?
         ├─ Yes → Is it a complaint or complex?
         │        ├─ Yes → DEFER (complex)
         │        └─ No → DRAFT (inquiry/faq/reply)
         └─ No → Is it providing useful information?
                  ├─ Yes → ACKNOWLEDGE (informational)
                  └─ No → ACKNOWLEDGE (no action needed)
```

## Email Draft Guidelines

### Tone
- Warm and professional
- Friendly but not overly casual
- Personal touch (use customer's name)
- Helpful and solution-oriented

### Structure
1. **Greeting** - "Dear [Name]" or "Hi [Name]"
2. **Thank them** - For their interest/inquiry
3. **Answer their question(s)** - Directly and specifically
4. **Provide additional helpful info** - From knowledge base
5. **Call to action** - Booking link when appropriate
6. **Closing** - "Warm regards" / "Best wishes"
7. **Signature** - Peter & Cristiana, Hostel Brikette

### Common Scenarios

**Availability inquiry:**
- Cannot check real-time availability
- Direct to website booking system
- Mention room types that might suit their needs
- Emphasize direct booking benefits

**Price question:**
- Use menu pricing data accurately
- Clarify breakfast inclusion policy
- Mention direct booking discounts

**Directions/Location:**
- Provide standard directions
- Link to relevant guides
- Mention luggage storage

**Policy questions:**
- Use FAQ data accurately
- Be specific about times and rules
- Offer flexibility where possible

**Complaints:**
- Acknowledge their frustration
- Apologize appropriately
- Offer solution or escalation
- Flag for Pete's careful review

## Error Handling

### Gmail API Error
```markdown
## Gmail API Error

Unable to fetch emails: [Error message]

Options:
1. "Retry" - try again
2. "Done" - end session and try later
```

### Cannot Generate Good Response
```markdown
## Draft Generation Issue

I'm having trouble with this email because:
- [Reason]

Options:
1. "Flag for manual" - you'll handle this directly
2. "Use template" - generic acknowledgment response
3. "Give context" - tell me more to help
```

### Session Interruption
When user needs to stop:
- Summarize progress
- Note queue position
- Remind about pending drafts

## Quality Checks

Before creating each draft, verify:
- [ ] Addresses customer's specific question(s)
- [ ] Information is accurate (from knowledge base)
- [ ] Tone is appropriate
- [ ] Call-to-action included (if appropriate)
- [ ] No placeholder text remains
- [ ] Signature included

## References

- **User guide:** `docs/guides/brikette-email-workflow.md`
- **Workflow design:** `docs/plans/email-autodraft-workflow-design.md`
- **Card:** `docs/business-os/cards/BRIK-ENG-0020.user.md`

## MCP Resources Available

| URI | Content |
|-----|---------|
| `brikette://faq` | 29 FAQ items |
| `brikette://rooms` | Room details and config |
| `brikette://pricing/menu` | Bar and breakfast prices |
| `brikette://policies` | Check-in, age restrictions, etc. |
| `brikette://draft-guide` | Draft quality framework |
| `brikette://voice-examples` | Voice/tone examples |
| `brikette://email-examples` | Classification examples |

## MCP Signal & Improvement Tools

| Tool | Action/Params | Purpose |
|------|--------------|---------|
| `draft_signal_stats` | (none) | Returns `{selection_count, refinement_count, joined_count, events_since_last_calibration}` — used in Session Summary |
| `draft_template_review` | `action: "list"` | Lists pending template improvement proposals with one-line summaries |
| `draft_template_review` | `action: "approve", proposal_id, expected_file_hash` | Approves a proposal and writes to `email-templates.json` (optimistic concurrency) |
| `draft_template_review` | `action: "reject", proposal_id` | Rejects and archives a proposal |
| `draft_ranker_calibrate` | `dry_run?: boolean` | Computes and persists ranker priors from ≥20 joined events; use when `events_since_last_calibration ≥ 20` |

## Email Templates

Pre-written templates are available in `packages/mcp-server/data/email-templates.json` for common response scenarios. Use these as a starting point and personalize for each customer.

### Template Categories

| Category | Templates | Use For |
|----------|-----------|---------|
| check-in | Arriving before check-in, Arrival Time, Out of hours | Check-in timing questions |
| access | Inner/Outer Building Main Door | Door code and access questions |
| transportation | Transportation to Hostel | How to get here questions |
| payment | Change Credit Card Details | Payment method updates |
| prepayment | 1st/2nd/3rd Attempt, Cancelled, Successful | Payment processing status |
| cancellation | Non-Refundable Booking, No Show | Cancellation requests |
| policies | Alcohol, Age Restriction | Policy explanations |
| activities | Path of the Gods Hike | Activity recommendations |
| booking-issues | Why cancelled | Booking troubleshooting |

### Prepayment Workflow

When handling prepayment chase emails, apply these mappings:
- **Step 1:** Use the 1st attempt template (Octorate vs Hostelworld variant based on booking source). Log activity code 2.
- **Step 2:** Use the 2nd attempt template. Log activity code 3.
- **Step 3:** Use the cancelled-after-3rd-attempt template. Log activity code 4.
- **Success:** Use the prepayment successful template. Log activity code 21.

When updating Gmail labels, use `gmail_mark_processed` with:
`prepayment_chase_1`, `prepayment_chase_2`, or `prepayment_chase_3`.

### T&C Agreement Workflow

When an incoming email is a T&C agreement reply:
- **Sending the T&C request (outgoing):** Mark with `action: "awaiting_agreement"`.
- **Receiving agreement confirmation (incoming):** Mark with `action: "agreement_received"` **and** pass `reservationCode` (see Agreement Detection section above). This triggers Firebase activity code 21 write for all occupants — required to prevent the booking from being auto-cancelled despite the guest having agreed.

### Using Templates

When drafting a response:

1. **Match the scenario** - Find a template matching the customer's question
2. **Load the template** - Reference the category and subject
3. **Personalize** - Replace placeholders, add guest name, adjust tone
4. **Add specifics** - Include relevant details from their booking/question
5. **Validate** - Ensure accuracy before creating draft

Templates provide consistent messaging for common scenarios while maintaining the professional, warm tone expected by guests.
