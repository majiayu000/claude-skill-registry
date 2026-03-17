---
name: email-drafter
version: 1.0.0
description: |
  Generates professional emails from bullet points or conversation summaries.
  Use when you need to draft emails quickly with consistent style and tone.
  Supports multiple tones: formal, casual, technical
  Supports contexts: status updates, requests, announcements, follow-ups
---

# Email Drafter Skill

Generate professional, well-structured emails from bullet points or conversation summaries with consistent tone and formatting.

## Use Cases

- Convert meeting notes into status update emails
- Draft professional requests or proposals
- Create announcements to teams or stakeholders
- Write follow-up emails after conversations
- Respond to inquiries professionally
- Draft meeting recaps and action items

## How to Use This Skill

Provide Claude with:
1. **Content**: Bullet points, notes, or conversation summary
2. **Tone**: One of (formal, casual, technical)
3. **Context**: One of (status_update, request, announcement, follow_up, response, recap)
4. **Optional**: Recipient name/title, any specific requirements

Claude will transform the input into a polished, professional email with:
- Appropriate greeting and sign-off
- Clear structure and flow
- Consistent tone throughout
- Professional formatting
- Proper punctuation and grammar

## Supported Tones

### Formal
- Professional business language
- Complete sentences and formal grammar
- Respectful and courteous
- Suitable for: executives, external stakeholders, important announcements
- Example phrases: "I would like to...", "Thank you for your consideration...", "Please find attached..."

### Casual
- Friendly and approachable tone
- Conversational language
- Professional but relaxed
- Suitable for: teammates, internal communications, collaborative contexts
- Example phrases: "Just wanted to let you know...", "Feel free to reach out...", "Let's connect..."

### Technical
- Precise and detailed
- Uses domain-specific terminology
- Direct and clear
- Suitable for: technical teams, system documentation, architecture discussions
- Example phrases: "The implementation includes...", "The system parameters are configured to...", "Technical specifications..."

## Supported Contexts

### Status Update
**Purpose**: Inform recipients about current progress, completed work, and next steps

**Structure**:
1. Opening: What period/project this covers
2. Completed items: What was accomplished
3. In-progress items: Current work
4. Upcoming items: What's next
5. Blockers/Issues: Any challenges (if applicable)
6. Closing: Invitation for questions/discussion

**Best for**: Weekly updates, sprint reviews, project progress reports

### Request
**Purpose**: Ask for action, approval, resources, or input from recipients

**Structure**:
1. Context: Why this request is important
2. What's being asked: Clear, specific request
3. Why it matters: Benefits or urgency
4. Timeline: When needed
5. Next steps: How to respond
6. Closing: Appreciation and contact info

**Best for**: Budget requests, time off, resources, approvals, feedback

### Announcement
**Purpose**: Communicate news, changes, or information to a team or stakeholder group

**Structure**:
1. Hook: Lead with the announcement
2. Context: Why this change/news matters
3. Details: Specific information
4. Impact: How it affects recipients
5. Next steps: What recipients should know/do
6. Closing: Point of contact for questions

**Best for**: Product launches, policy changes, team updates, organizational changes

### Follow-up
**Purpose**: Continue a conversation, remind about commitments, or move items forward

**Structure**:
1. Reference: What previous conversation/commitment this relates to
2. Update: What's happened since
3. Call to action: What's needed next
4. Offer to help: Your contribution/availability
5. Closing: Clear next steps

**Best for**: After meetings, checking on decisions, ensuring progress

### Response
**Purpose**: Reply to an inquiry, offer, or question

**Structure**:
1. Appreciation: Thank them for reaching out
2. Answer: Direct response to their question/request
3. Details: Additional relevant information
4. Next steps: How to proceed
5. Closing: Reaffirm helpfulness

**Best for**: Replying to inquiries, addressing questions, responding to proposals

### Recap
**Purpose**: Summarize a meeting, conversation, or decision for the record

**Structure**:
1. Opening: What was discussed
2. Key decisions: What was decided
3. Action items: Who's doing what by when
4. Outstanding issues: What still needs resolution
5. Closing: Confirmation and next meeting

**Best for**: Meeting summaries, decision documentation, action item tracking

## Examples

### Example 1: Status Update (Formal Tone)

**Input**:
- Tone: formal
- Context: status_update
- Bullet points:
  - Completed authentication module implementation
  - Unit tests at 94% coverage
  - Performance benchmarks show 15% improvement
  - Database migration testing in progress
  - Need approval on API schema changes
  - Team meeting scheduled for Thursday

**Output**:
```
Dear Team,

I am writing to provide a status update on the authentication module project for the week of November 4-8.

Completed Items:
The authentication module implementation has been completed and is ready for integration testing. Unit test coverage has reached 94%, demonstrating comprehensive code validation. Performance benchmarks indicate a 15% improvement over the previous implementation.

In Progress:
Database migration testing is currently underway to ensure data integrity during the transition. We anticipate completion by end of day Friday.

Upcoming:
The team will gather on Thursday to discuss and potentially approve the proposed API schema changes. Your input on this matter would be greatly appreciated.

Please let me know if you have any questions or concerns regarding this update.

Best regards,
[Your Name]
```

### Example 2: Request (Casual Tone)

**Input**:
- Tone: casual
- Context: request
- Recipient: Engineering Manager
- Bullet points:
  - Need to attend conference next month
  - Will present technical talk on distributed systems
  - Conference dates March 15-17
  - Budget needed for travel and registration
  - Will share updates with team while there

**Output**:
```
Hi [Manager Name],

I wanted to reach out about an opportunity I'd like to pursue. I've been selected to give a talk on distributed systems architecture at the upcoming tech conference on March 15-17. It's a great chance to represent the company and share what we've learned.

Here's what I'd need:
- Travel and lodging budget (I'll keep it reasonable)
- Time off for the conference dates
- Conference registration fee

I'll definitely share key learnings and insights with the team when I get back, so we can all benefit from the experience. I'm happy to discuss this further if you have any questions.

Let me know what you think!

Thanks,
[Your Name]
```

### Example 3: Announcement (Formal Tone)

**Input**:
- Tone: formal
- Context: announcement
- Bullet points:
  - New deployment pipeline going live
  - Reduces deployment time from 2 hours to 15 minutes
  - All teams can self-serve deployments
  - Training session Thursday
  - FAQ document shared in wiki
  - Questions? Contact DevOps team

**Output**:
```
Subject: New Deployment Pipeline Now Available

Dear Team,

We are pleased to announce the launch of our new automated deployment pipeline, effective immediately. This infrastructure improvement represents a significant operational enhancement for our entire organization.

Key Benefits:
Deployment time has been reduced from 2 hours to approximately 15 minutes, enabling more frequent and reliable releases. Additionally, all development teams now have self-service deployment capabilities, reducing dependency on centralized operations.

What You Need to Know:
A comprehensive training session will be held on Thursday at 2:00 PM to walk through the new process. A detailed FAQ document has been posted to our internal wiki for reference.

Next Steps:
Please plan to attend the training session or review the documentation at your earliest convenience. If you have questions or encounter any issues, please reach out to the DevOps team.

We are confident this will improve our development velocity and system reliability.

Best regards,
Platform Operations Team
```

### Example 4: Follow-up (Casual Tone)

**Input**:
- Tone: casual
- Context: follow_up
- Bullet points:
  - Follow-up from Tuesday design review meeting
  - Discussed new dashboard mockups
  - Agreed to implement three-column layout
  - Need design system updates for new components
  - Developer assignments: James (chart widgets), Sarah (data table)
  - Next review in two weeks

**Output**:
```
Hi everyone,

Just wanted to follow up on our design review from Tuesday. We got some great feedback on the dashboard mockups and made some solid decisions moving forward.

Here's where we landed:
We're going with the three-column layout design, which the team felt was the cleanest option. This will require some updates to our design system for the new component types we're using.

Who's doing what:
James will take point on the chart widgets, and Sarah will handle the data table component. I'll coordinate the design system updates to support both.

Next steps:
We'll reconvene in two weeks for the next design review. If anyone spots issues before then, just ping the group.

Thanks for the great collaboration!

[Your Name]
```

### Example 5: Response (Technical Tone)

**Input**:
- Tone: technical
- Context: response
- Bullet points:
  - Question: How does caching layer work?
  - Answer: Redis-based distributed cache
  - TTL configuration: 1 hour default, configurable per endpoint
  - Cache invalidation: Event-driven and time-based
  - Performance: 95th percentile latency reduced by 40%
  - Code examples available in repository

**Output**:
```
Thank you for your inquiry regarding our caching architecture.

The caching layer is implemented using a Redis-based distributed cache with the following specifications:

Configuration:
- Default TTL: 3600 seconds (1 hour)
- TTL is configurable per endpoint via the cache_ttl decorator
- Cache key format: namespace:resource_id:version_hash
- Compression enabled for values exceeding 1KB

Invalidation Strategy:
The system employs a hybrid invalidation approach:
- Event-driven invalidation triggered by data mutation operations
- Time-based expiration using the configured TTL
- Manual invalidation available via administrative interface

Performance Characteristics:
Implementation of this caching strategy has resulted in a 40% reduction in 95th percentile latency for read-heavy operations.

Implementation Details:
Complete code examples and configuration documentation are available in the repository under /docs/caching-architecture. The cache client library provides both synchronous and asynchronous interfaces.

Please reach out if you require additional technical details or have further questions.

Best regards,
[Your Name]
```

### Example 6: Recap (Formal Tone)

**Input**:
- Tone: formal
- Context: recap
- Meeting: Q4 Planning Session
- Attendees: Leadership team
- Bullet points:
  - Decided to prioritize platform stability over new features
  - Moving API gateway migration to Q1
  - Budget approved for third-party vendor assessment
  - Alex leading architecture review
  - Next planning meeting December 1
  - Action items: vendor proposals due Nov 20, architecture plan due Nov 25

**Output**:
```
Subject: Q4 Planning Session - Summary and Action Items

Dear Team,

This message summarizes the key outcomes and decisions from our Q4 Planning Session held today.

Key Decisions:
1. Platform stability has been prioritized over the addition of new features for Q4
2. The API gateway migration initiative has been rescheduled for Q1 to align with resource availability
3. Budget has been approved for a third-party vendor assessment to evaluate infrastructure options

Assigned Responsibilities:
- Alex Chen will lead the comprehensive architecture review
- All team leads will provide vendor proposals by November 20
- Architecture recommendations document is due November 25

Next Steps:
The next planning meeting is scheduled for December 1 at 10:00 AM. Please come prepared with your respective departmental updates and any outstanding questions.

Should you require clarification on any of the decisions or action items outlined above, please do not hesitate to contact me.

Best regards,
[Your Name]
```

## Key Features

### Tone Consistency
Each email maintains consistent tone throughout, avoiding jarring switches in formality or language level.

### Contextual Structure
Each context type follows an appropriate structure that guides readers through the information logically.

### Professional Formatting
- Clear paragraph breaks
- Appropriate use of lists and bullet points
- Proper salutations and closings
- Subject lines when appropriate

### Grammar and Clarity
- Correct punctuation and spelling
- Clear, concise language
- Active voice preferred
- Removes redundancy

## Tips for Best Results

1. **Be Specific**: Provide concrete details rather than vague summaries
2. **Include Priorities**: Highlight what matters most if information is extensive
3. **Clarify Action Items**: Specify who should do what and by when
4. **Provide Context**: Help Claude understand why this information matters
5. **Specify Recipients**: Mention if email is for executives, teammates, or external parties

## What This Skill Does NOT Do

- Send emails on your behalf
- Change the meaning of your content
- Add information not provided
- Override the tone you requested
- Generate inappropriate content

Always review generated emails before sending. You remain responsible for final content and accuracy.
