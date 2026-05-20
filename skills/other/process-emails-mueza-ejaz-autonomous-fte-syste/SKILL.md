---
name: process-emails
description: Process emails from Gmail Watcher, categorize by priority (urgent/normal/low), draft appropriate responses using templates, flag items requiring immediate attention. Use when processing emails, checking inbox, handling Gmail notifications, or user mentions "email", "inbox", "gmail", "messages", "check mail", "respond to email".
user-invocable: true
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash]
---

# Process Emails Skill

**Purpose:** Automatically process emails detected by Gmail Watcher, categorize them by priority, draft appropriate responses, and manage approval workflow for sending replies.

**Dependencies:**
- Gmail Watcher (creates EMAIL_*.md files in `Vault/Needs_Action`)
- handle-approval skill (for sending email responses)
- Email MCP Server (for actual email sending)
- `Vault/Company_Handbook.md` (for response guidelines)

**Trigger Phrases:**
- "process emails"
- "check my inbox"
- "check emails"
- "handle emails"
- "respond to emails"
- "what emails need attention"
- "process gmail"

---

## Overview

This skill implements a complete email processing workflow:

1. **Detection:** Scan `Vault/Needs_Action` for EMAIL_* files created by Gmail Watcher
2. **Analysis:** Extract and categorize email metadata
3. **Prioritization:** Classify emails as urgent/normal/low priority
4. **Response:** Draft appropriate replies using templates
5. **Approval:** Create approval requests for email responses
6. **Logging:** Update Dashboard with all email activities

---

## Workflow Phases

### Phase 1: Scan for New Emails

**Objective:** Identify unprocessed email files in the `Vault/Needs_Action` folder.

**Steps:**
1. Use Glob tool to find all EMAIL_*.md files in `Vault/Needs_Action`
2. Filter out files already processed (check Dashboard log)
3. Sort by priority metadata if available
4. Process in order: urgent → normal → low

**Output:** List of email files to process

---

### Phase 2: Extract Email Metadata

**Objective:** Parse email file to extract sender, subject, body, and metadata.

**Steps:**
1. Read the EMAIL_*.md file using Read tool
2. Extract YAML frontmatter:
   - `type: email`
   - `from: sender@example.com`
   - `subject: Email subject line`
   - `received: timestamp`
   - `priority: high/normal/low`
   - `message_id: unique_id`
3. Extract email body content
4. Optionally use parse_email_metadata.py script for complex parsing

**Reference:** See [Email File Format](#email-file-format) below

---

### Phase 3: Categorize Email

**Objective:** Classify email into appropriate category and priority level.

**Categorization Process:**
1. Load categorization rules from [reference/categorization.md](./reference/categorization.md)
2. Analyze email content for:
   - Sender domain (client, internal, vendor)
   - Subject keywords (invoice, urgent, meeting, etc.)
   - Body content patterns
3. Assign category:
   - Client Communications
   - Sales/Leads
   - Administrative
   - Internal Team
   - Spam/Low Priority

**Priority Assessment:**
1. Load priority rules from [reference/priority-rules.md](./reference/priority-rules.md)
2. Check for urgency indicators:
   - Keywords: "urgent", "asap", "immediate", "deadline"
   - VIP sender list
   - Subject line patterns
   - Time-sensitive content
3. Assign priority: urgent / normal / low

**Output:** Category and priority classification

---

### Phase 4: Draft Response

**Objective:** Generate appropriate email response based on category and content.

**Response Generation:**
1. Load email templates from [reference/email-templates.md](./reference/email-templates.md)
2. Select template based on:
   - Email category
   - Request type (inquiry, invoice, meeting, support)
   - Priority level
3. Personalize template with:
   - Sender name
   - Specific details from original email
   - `Vault/Company_Handbook.md` tone and style
   - `Vault/Business_Goals.md` context (if relevant)
4. Draft response following professional standards

**Quality Checks:**
- Appropriate greeting and closing
- Addresses all questions from original email
- Professional tone consistent with Company_Handbook
- No typos or formatting issues
- Includes relevant information/attachments

**Reference:** See [email-templates.md](./reference/email-templates.md) for all templates

---

### Phase 5: Create Approval Request

**Objective:** Generate approval request for email response following safety protocols.

**Approval Logic:**
1. Check approval thresholds (from handle-approval skill):
   - **Auto-approve:** Replies to known contacts < 200 words (NOT IMPLEMENTED - all require approval for safety)
   - **Require approval:** New contacts, bulk sends, attachments, sensitive content
2. For Silver Tier: **ALL EMAIL SENDS REQUIRE APPROVAL**

**Create Approval File:**
1. Use approval-template from handle-approval skill
2. Create file: `Vault/Pending_Approval/EMAIL_[recipient-name]_[date].md`
3. Include:
   ```yaml
   ---
   type: approval_request
   action: send_email
   to: recipient@example.com
   subject: Response subject line
   created: [timestamp]
   expires: [48 hours from creation]
   priority: [based on email priority]
   status: pending
   original_email_file: EMAIL_xxx.md
   ---
   ```
4. Include full email body in approval request
5. Add context from original email
6. Note any risks or considerations

**Reference:** Use handle-approval skill's approval-template.md

---

### Phase 6: Handle Special Cases

**Urgent Emails:**
- Flag in Dashboard with 🚨 indicator
- Set approval expiration to 24 hours (not 48)
- Add "URGENT" tag to approval filename
- Log with high priority in Dashboard

**Spam/Low Priority:**
- Move directly to `Vault/Done` with "SPAM" or "LOW_PRIORITY" tag
- No response needed
- Log in Dashboard as filtered

**Automated Notifications:**
- Service alerts, newsletters, automated receipts
- Archive to `Vault/Done` with "AUTO_NOTIFICATION" tag
- No action required
- Brief log entry in Dashboard

**Errors/Parsing Issues:**
- If email file is malformed or unreadable
- Create error log in `Vault/Logs`
- Move problematic file to `Vault/Needs_Action/ERROR_*`
- Alert in Dashboard for manual review

---

### Phase 7: Dashboard Logging

**Objective:** Maintain comprehensive audit trail of all email processing.

**Log Entry Format:**
```markdown
## [YYYY-MM-DD HH:MM:SS] Email Processing

**Email:** [Subject line]
**From:** [Sender name/email]
**Category:** [Category]
**Priority:** [urgent/normal/low]
**Action:** [Response drafted / Archived as spam / Flagged for manual review]
**Approval Status:** [Created approval request / Auto-archived]
**File:** [Original EMAIL_*.md filename]
**Approval File:** [APPROVAL_EMAIL_*.md filename if created]

---
```

**Dashboard Update:**
1. Read current `Vault/Dashboard.md`
2. Append new entry under "Recent Activity" section
3. Update email processing statistics if tracked
4. Save `Vault/Dashboard.md`

---

## Email File Format

Email files created by Gmail Watcher follow this standard format:

```markdown
---
type: email
from: sender@example.com
from_name: John Doe
subject: Invoice Request for January
received: 2026-01-11T10:30:00Z
priority: normal
message_id: unique_gmail_id
status: pending
---

## Email Content

[Email body text here]

Multiple paragraphs preserved.

## Suggested Actions

- [ ] Reply to sender
- [ ] Forward to relevant party
- [ ] Archive after processing
- [ ] Flag as urgent

## Metadata

- **Labels:** Important, Work
- **Thread ID:** thread_123
- **Attachments:** invoice.pdf (if any)
```

---

## Integration with Other Skills

### handle-approval Skill
- **When:** After drafting email response
- **How:** Call handle-approval to create approval request
- **Workflow:** process-emails → draft response → handle-approval → create APPROVAL_EMAIL_*.md

### create-plan Skill
- **When:** Email requires complex multi-step action
- **Example:** "Please update our website and send me a proposal"
- **How:** Create plan for complex request, email response confirms plan creation

---

## Error Handling

**File Not Found:**
- Log error to Dashboard
- Continue processing other emails
- Do not stop workflow

**Malformed Email File:**
- Move to `Vault/Needs_Action/ERROR_EMAIL_[filename]`
- Log to Dashboard with error details
- Create manual review task

**Template Not Found:**
- Use generic professional response template
- Log warning to Dashboard
- Email still gets processed

**Approval Creation Fails:**
- Log error to `Vault/Logs`
- Do not send email (safety first)
- Alert in Dashboard for manual intervention

---

## Security & Safety

**Never Auto-Send:**
- All email sends require human approval (Silver Tier standard)
- No exceptions for "trusted" contacts yet (implement in Gold Tier)

**PII Protection:**
- Never include passwords, API keys, credit card numbers in email
- Validate email addresses before creating approval
- Check for typos in recipient address

**Content Validation:**
- Ensure response is professional and appropriate
- No offensive language
- Factually accurate based on Company_Handbook
- Addresses recipient's actual questions

**Rate Limiting:**
- Process maximum 20 emails per batch
- Prevent overwhelming approval queue
- Prevent accidental mass sends

---

## Testing & Validation

**Test with Dummy Email:**
1. Create test email file in `Vault/Needs_Action`
2. Run skill with `/process-emails`
3. Verify categorization is correct
4. Check response draft quality
5. Confirm approval request created properly
6. Validate Dashboard logging

**Test Cases:**
- Urgent client email
- Normal inquiry email
- Spam email
- Automated notification
- Malformed email file

---

## Performance Optimization

**For Large Email Volumes:**
- Process in batches of 10-20
- Prioritize urgent emails first
- Archive spam immediately
- Defer low-priority processing

**For Quick Responses:**
- Use haiku model for categorization (faster, cheaper)
- Cache email templates in memory
- Reuse approval template structure

---

## Reference Files

This skill uses progressive disclosure. Load these files on-demand:

1. **[email-templates.md](./reference/email-templates.md)**
   - Response templates for common scenarios
   - Client inquiry, invoice request, meeting scheduling, etc.

2. **[priority-rules.md](./reference/priority-rules.md)**
   - Urgency keywords and patterns
   - VIP sender list
   - Auto-approve vs require approval logic

3. **[categorization.md](./reference/categorization.md)**
   - Email categorization criteria
   - Domain-based classification
   - Content pattern matching

---

## Scripts

**parse_email_metadata.py:**
- Python script for complex email parsing
- Extracts sender, subject, body, attachments
- Returns structured JSON metadata
- Usage: `python scripts/parse_email_metadata.py EMAIL_xxx.md`

---

## Success Criteria

✅ **Skill Working If:**
- Detects EMAIL_* files in `Vault/Needs_Action`
- Correctly categorizes email priority
- Drafts professional, relevant responses
- Creates approval requests for all sends
- Logs all activity to Dashboard
- Handles errors gracefully

---

## Troubleshooting

**Skill doesn't activate:**
- Check trigger phrases in description
- Verify EMAIL_* files exist in `Vault/Needs_Action`
- Try explicit invocation: `/process-emails`

**Wrong email category:**
- Review categorization.md rules
- Check for new sender domains
- Update categorization logic

**Poor response quality:**
- Review email-templates.md
- Update Company_Handbook.md tone guidelines
- Add more context to templates

**Approval not created:**
- Verify handle-approval skill is available
- Check `Vault/Pending_Approval` folder exists
- Review error logs in Dashboard

---

## Future Enhancements (Gold Tier)

- Auto-approve for trusted contacts (after pattern learning)
- Email threading (reply in context)
- Attachment handling
- Calendar integration for meeting requests
- Multi-language support
- Sentiment analysis for urgent detection

---

**End of SKILL.md**

Total Lines: ~340 (Under 500 ✓)
Structure: Progressive disclosure with reference files
Status: Ready for testing