---
name: process-emails
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

## Workflow

### 1. Run Inbox Organize Cycle

First, run an inbox organize pass for unread emails. This does a garbage/sort cycle:
- trashes known garbage patterns
- labels likely customer inquiries as `Brikette/Inbox/Needs-Processing`

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
   If `passed=false`, present failed checks and ask how to proceed (edit or regenerate).

6. **Present to user**:
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
Archives email and labels `Brikette/Promotional` for batch review later.
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
Moves it out of the active queue and labels it `Brikette/Inbox/Deferred` for manual follow-up.

### Agreement Detection (T&C workflow)

Agreement detection is high-stakes:
- `confirmed` only for explicit agreement phrases (EN/IT/ES).
- `likely` or `unclear` requires human confirmation before any payment workflow.
- Always check `agreement.requires_human_confirmation`.

If the email includes agreement **and** questions, treat as mixed response:
1. Acknowledge agreement in the draft.
2. Answer all questions.
3. Keep the workflow state as awaiting confirmation if `likely/unclear`.

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
```

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

**Promotional** - Marketing (archive to Brikette/Promotional):
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

### Using Templates

When drafting a response:

1. **Match the scenario** - Find a template matching the customer's question
2. **Load the template** - Reference the category and subject
3. **Personalize** - Replace placeholders, add guest name, adjust tone
4. **Add specifics** - Include relevant details from their booking/question
5. **Validate** - Ensure accuracy before creating draft

Templates provide consistent messaging for common scenarios while maintaining the professional, warm tone expected by guests.
