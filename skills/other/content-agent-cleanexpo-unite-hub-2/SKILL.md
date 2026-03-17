---
name: content-agent
description: Generates personalized marketing content for Unite-Hub. Creates followup emails, proposals, and case studies based on contact data and interaction history. Uses Claude AI for high-quality, contextual content generation.
---

# Content Generation Agent Skill

## Overview
The Content Agent creates personalized, high-converting marketing content by:
1. Reading contact profiles and interaction history
2. Analyzing engagement patterns and sentiment
3. Generating contextually relevant content using Claude
4. Storing drafts for human review/approval
5. Tracking performance metrics

## Content Types

### 1. Followup Email
**When to generate:**
- Contact received email 7+ days ago (nextFollowUp date passed)
- Status is "lead" or "prospect"
- AI score > 60 (engaged)

**Context to include:**
- Reference their last interaction
- Mention their company/industry
- Highlight relevant case study or service
- Include clear CTA

**Example prompt:**
```
Generate a professional followup email for:
- Name: John Smith
- Company: TechStartup Inc
- Job Title: CEO
- Last interaction: "Interested in Q4 marketing services"
- Sentiment: positive
- Industry: Technology

The email should:
1. Reference their interest in partnership
2. Mention 1 specific success story relevant to tech startups
3. Propose a 15-minute strategy call
4. Be warm but professional
5. Keep under 150 words
```

### 2. Proposal Email
**When to generate:**
- Contact has shown high engagement (AI score > 80)
- Status is "prospect"
- Multiple positive interactions

**Context to include:**
- Personalized value proposition
- Estimated ROI/results
- Timeline and deliverables
- Investment/pricing range
- Next steps

**Example prompt:**
```
Generate a proposal email for:
- Name: Lisa Johnson
- Company: eCommerce Solutions
- Pain point: "Revamping marketing strategy"
- Budget indicator: Mid-market (medium budget)
- Timeline: Q4 2024

The proposal should:
1. Address their specific pain point
2. Outline 3-4 key deliverables
3. Mention expected metrics (e.g., "35% revenue increase")
4. Suggest 60-day engagement
5. Request a call to discuss
```

### 3. Case Study Reference
**When to generate:**
- Contact from specific industry
- AI score indicates readiness
- Relevant success story exists

**Context to include:**
- Similar company/industry case study
- Key metrics and results
- How it applies to their situation

## How the Agent Works

### Step 1: Identify Target Contacts

Query contacts where:
```
status = "prospect" OR "lead"
aiScore > 60
nextFollowUp <= NOW
```

### Step 2: For Each Contact

**A. Load Contact History**
```
GET contact details
GET contact's emails (interaction history)
GET any previous generated content for this contact
```

**B. Build Context Object**
```
{
  name: "John Smith",
  company: "TechStartup Inc",
  jobTitle: "CEO",
  industry: "Technology",
  aiScore: 78,
  sentiment: "positive",
  lastInteraction: "Interested in Q4 partnership",
  emailsSent: 2,
  engagementDays: 15,
  hasProposalBefore: false
}
```

**C. Determine Content Type**

Logic:
```
IF aiScore > 80 AND !hasProposalBefore
  → Generate "proposal"
ELSE IF aiScore > 60 AND lastInteraction > 7 days ago
  → Generate "followup"
ELSE IF industry has matching case study
  → Generate "case_study_reference"
ELSE
  → Generate "general_followup"
```

**D. Build Claude Prompt**

Template:
```
You are a professional B2B marketing copywriter for a marketing agency.

Generate a [CONTENT_TYPE] email for:
- Name: [NAME]
- Company: [COMPANY]
- Job Title: [JOB_TITLE]
- Industry: [INDUSTRY]
- Last interaction: [LAST_INTERACTION]
- Sentiment of previous emails: [SENTIMENT]
- Our success with similar companies: [CASE_STUDY_BRIEF]

Requirements:
1. Personalized to their specific situation
2. Reference their industry/company when possible
3. Include specific, measurable outcomes (if proposal)
4. Professional but warm tone
5. Clear call-to-action
6. [TYPE_SPECIFIC_REQUIREMENTS]

Keep under [WORD_LIMIT] words.

Generate the email body only (no "Subject:" or greeting).
```

**E. Call Claude API**
```
POST https://api.anthropic.com/v1/messages

{
  "model": "claude-sonnet-4-5-20250929",
  "max_tokens": 1000,
  "system": "You are an expert B2B marketing copywriter...",
  "messages": [
    {
      "role": "user",
      "content": "[BUILT_PROMPT]"
    }
  ]
}
```

**F. Parse Response**

Extract text from response:
```
response.content[0].text
```

**G. Store as Draft**

Call Convex mutation:
```
POST convex mutation content.store({
  orgId: "...",
  workspaceId: "...",
  contactId: "[CONTACT_ID]",
  contentType: "[TYPE]",
  title: "[AUTO_GENERATED_TITLE]",
  prompt: "[USED_PROMPT]",
  text: "[CLAUDE_RESPONSE]",
  aiModel: "sonnet",
  htmlVersion: null // Optional HTML formatting
})
```

**H. Log Audit Event**
```
POST convex mutation system.logAudit({
  orgId: "...",
  action: "content_generated",
  resource: "generatedContent",
  agent: "content-agent",
  details: {
    contactId: "...",
    contentType: "[TYPE]",
    aiScore: 78,
    tokensUsed: 234
  },
  status: "success"
})
```

### Step 3: Summary Report

Output:
```
✅ Content Generation Complete

Total generated: X
Followup emails: X
Proposals: X
Case studies: X
Drafts awaiting approval: X

By AI score:
- High priority (>80): X contacts
- Medium priority (60-80): X contacts

Sample generated content:
- John Smith (TechStartup): Followup email
- Lisa Johnson (eCommerce): Proposal

Next steps:
1. Review drafts in dashboard
2. Approve/edit content
3. Schedule for sending
4. Track performance metrics
```

## Error Handling

If Claude API call fails:
```
Log audit event with status: "error"
Try fallback: Use template-based content
Continue to next contact
```

If contact data incomplete:
```
Skip contact with warning
Log as skipped in audit trail
```

## Performance Tracking

After content is approved and sent:
```
Track:
- Opens (if integration available)
- Clicks
- Replies
- Conversions

Update generatedContent record with metrics:
{
  status: "sent",
  sentAt: timestamp,
  performanceMetrics: {
    opens: 0,
    clicks: 0,
    replies: 0
  }
}
```
