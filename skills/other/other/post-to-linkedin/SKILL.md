# post-to-linkedin Skill

---
name: post-to-linkedin
description: Generate and post business updates to LinkedIn for sales generation. Creates professional posts about projects, achievements, industry insights, client success stories, and service offerings. Automatically drafts content using templates, applies brand voice guidelines, adds relevant hashtags, and creates approval requests. Use when user mentions "post to linkedin", "share on linkedin", "create linkedin post", "social media update", "generate business post", "linkedin content", or when scheduling automatic business updates for lead generation.
user-invocable: true
allowed-tools: [Read, Write, Bash, Glob, Grep]
context: fork
---

## Purpose

Automatically generate professional LinkedIn posts for business development and lead generation. This skill creates engaging content about your work, achievements, and expertise while maintaining brand consistency and requiring human approval before publishing.

## When to Use This Skill

This skill activates when:
- User asks to "post to LinkedIn" or "share on LinkedIn"
- Creating social media content for business updates
- Generating posts about completed projects or milestones
- Scheduling regular LinkedIn content
- Promoting services or achievements
- Sharing industry insights or tips
- Building thought leadership presence

## Workflow Overview

```
Business_Goals.md → Content Generation → Template Selection
        ↓                                        ↓
Recent Achievements ← Content Draft ← Brand Guidelines
        ↓                                        ↓
Hashtag Strategy → Final Post → Approval Request
        ↓                                        ↓
Human Approval → LinkedIn Publishing → Dashboard Log
```

## Step-by-Step Process

### Phase 1: Content Discovery (Gather Information)

**Objective:** Identify content-worthy activities and achievements.

1. **Read Business_Goals.md**
   ```bash
   # Location: Vault/Business_Goals.md
   # Look for: Active projects, recent milestones, Q1 objectives
   ```
   - Identify current business priorities
   - Check active projects and their status
   - Review key metrics and achievements
   - Note any specific content themes

2. **Scan Recent Completed Tasks**
   ```bash
   # Location: Vault/Done/
   # Pattern: Files from last 7 days
   ```
   - Look for completed project deliverables
   - Identify client wins or successful outcomes
   - Find interesting technical challenges solved
   - Note any learning moments or insights gained

3. **Check for Explicit Content Requests**
   ```bash
   # Location: Vault/Needs_Action/
   # Pattern: Files requesting LinkedIn posts
   ```
   - Process any direct requests to create LinkedIn content
   - Extract specific topics or angles requested
   - Note any deadlines or timing preferences

**Output:** Content theme and key points identified

---

### Phase 2: Content Generation (Create Draft)

**Objective:** Generate engaging, professional post content.

1. **Select Appropriate Template**

   Refer to [post-templates.md](./reference/post-templates.md) and choose based on content type:

   - **Project Milestone:** For completed deliverables, launches, achievements
   - **Client Success Story:** For positive outcomes, testimonials, case studies
   - **Industry Insight/Tip:** For sharing expertise, lessons learned, advice
   - **Service Offering:** For highlighting capabilities, solutions, specializations
   - **Behind-the-Scenes:** For process insights, tools, methodologies

2. **Apply Content Guidelines**

   Follow [content-guidelines.md](./reference/content-guidelines.md):

   - **Brand Voice:** Professional, approachable, expert (not arrogant)
   - **Length:** 150-300 words (optimal for LinkedIn engagement)
   - **Structure:** Hook → Value → Call-to-Action
   - **Tone:** Helpful, insightful, authentic
   - **Emoji Usage:** Minimal and professional (1-2 max)

3. **Draft Post Content**

   Template structure:
   ```markdown
   [Hook - attention-grabbing opening]

   [Context - what happened / why it matters]

   [Value - insight, lesson, or benefit]

   [Call-to-Action - invite engagement]

   #hashtag1 #hashtag2 #hashtag3
   ```

4. **Add Relevant Hashtags**

   Use [hashtag-strategy.md](./reference/hashtag-strategy.md):

   - Select 3-5 relevant hashtags
   - Mix: 2 industry-specific + 1 broad professional + 1-2 trending
   - Examples: #SoftwareDevelopment #AI #ProductivityHacks #TechLeadership

**Output:** Complete drafted LinkedIn post with hashtags

---

### Phase 3: Quality Review (Validate Content)

**Objective:** Ensure post meets quality standards before approval request.

1. **Check Against Company_Handbook.md**
   ```bash
   # Location: Vault/Company_Handbook.md
   # Section: Social Media Rules (if exists)
   ```
   - Verify compliance with brand guidelines
   - Check for prohibited topics
   - Confirm tone alignment
   - Validate professional standards

2. **Content Quality Checklist**

   - [ ] Length: 150-300 words
   - [ ] Clear value proposition (insight/lesson/benefit)
   - [ ] Professional tone maintained
   - [ ] No typos or grammatical errors
   - [ ] Call-to-action included
   - [ ] Hashtags relevant (3-5 total)
   - [ ] No controversial or prohibited topics
   - [ ] Authentic and genuine voice

3. **Metadata Validation**

   - Platform: LinkedIn
   - Post type: Text update (image/video if specified)
   - Timing: Optimal posting time if scheduling
   - Target audience: Professional network

**Output:** Validated post ready for approval

---

### Phase 4: Approval Request Creation

**Objective:** Create formal approval request for human review.

1. **Integrate with handle-approval Skill**

   This skill MUST use the `handle-approval` skill (from Branch 1) to create approval requests.

   Reference: [handle-approval thresholds](../../handle-approval/reference/approval-thresholds.md)

2. **Create Approval File**

   Use [approval-template.md](../../handle-approval/reference/approval-template.md) as base:

   ```markdown
   ---
   type: approval_request
   action: social_media_post
   platform: linkedin
   created: [timestamp ISO 8601]
   expires: [72 hours from creation]
   priority: normal
   status: pending
   ---

   ## Action Summary
   Publish LinkedIn post: [One-line description of content]

   ## Post Content
   [Full drafted post with hashtags]

   ## Metadata
   - **Platform:** LinkedIn
   - **Post Type:** Text update
   - **Word Count:** [X words]
   - **Hashtags:** #tag1 #tag2 #tag3
   - **Character Count:** [X/3000]

   ## Context & Rationale
   - **Content Source:** [Project milestone / Achievement / Insight]
   - **Business Goal:** [Lead generation / Thought leadership / Engagement]
   - **Target Audience:** [Potential clients / Industry peers / General professional network]

   ## Risks & Considerations
   - Risk: Low (standard business update)
   - Compliance: Follows brand guidelines
   - Timing: [Optimal posting window if scheduled]

   ## To Approve
   Move this file to `/Approved` folder.

   ## To Reject
   Move this file to `/Rejected` folder and add reason at bottom.

   ---
   ## Human Edits (Optional)
   [Space for human to edit post content before approval]
   ```

3. **File Naming Convention**
   ```
   APPROVAL_LINKEDIN_[short-description]_[YYYY-MM-DD].md

   Examples:
   - APPROVAL_LINKEDIN_ProjectAlphaMilestone_2026-01-11.md
   - APPROVAL_LINKEDIN_IndustryInsightAI_2026-01-11.md
   - APPROVAL_LINKEDIN_ClientSuccessStory_2026-01-11.md
   ```

4. **Save to Pending Approval Folder**
   ```bash
   # Location: Vault/Pending_Approval/
   # File: APPROVAL_LINKEDIN_[description]_[date].md
   ```

**Output:** Approval request file created in /Pending_Approval

---

### Phase 5: Dashboard Logging

**Objective:** Maintain audit trail and activity log.

Update `Vault/Dashboard.md` with structured entry:

```markdown
## Recent Activity

- [YYYY-MM-DD HH:MM:SS] **LinkedIn Post Created**
  - Topic: [Brief description]
  - Template: [Template type used]
  - Word Count: [X words]
  - Status: Pending Approval
  - Approval File: APPROVAL_LINKEDIN_[description]_[date].md
  - Action: Human review required in /Pending_Approval
```

**Output:** Dashboard updated with pending post status

---

### Phase 6: Post-Approval Execution (After Human Approval)

**Note:** This phase executes ONLY after human moves approval file to `/Approved` folder.

1. **Detect Approved Post**
   ```bash
   # Monitor: Vault/Approved/
   # Pattern: APPROVAL_LINKEDIN_*.md
   ```

2. **Execute LinkedIn Publishing**

   Call LinkedIn API helper script:
   ```bash
   python scripts/linkedin_api_helper.py --approval-file "Vault/Approved/APPROVAL_LINKEDIN_xxx.md"
   ```

   The script (located at `.claude/skills/post-to-linkedin/scripts/linkedin_api_helper.py`) will:
   - Extract post content from approval file
   - Authenticate with LinkedIn API
   - Publish the post
   - Return success/failure status

3. **Handle Execution Results**

   **If Success:**
   - Move approval file from `/Approved` to `/Done`
   - Update Dashboard with success log
   - Record LinkedIn post URL (if available)

   **If Failure:**
   - Keep file in `/Approved`
   - Log error to Dashboard
   - Create alert in /Needs_Action for troubleshooting

4. **Final Dashboard Update**
   ```markdown
   - [YYYY-MM-DD HH:MM:SS] **LinkedIn Post Published** ✓
     - Topic: [Brief description]
     - Post URL: [LinkedIn post URL]
     - Engagement: [Track later if analytics available]
     - Status: Complete
   ```

**Output:** Post published to LinkedIn and logged

---

## Integration with Other Skills

### Required Dependencies

1. **handle-approval Skill** (Branch 1)
   - MUST be used for all approval request creation
   - Enforces security thresholds
   - Manages expiration policies

### Optional Integrations

2. **create-plan Skill** (Branch 1)
   - Use for content calendar planning
   - Break down multi-post campaigns

3. **process-tasks Skill** (Bronze)
   - Process explicit LinkedIn post requests from /Needs_Action

---

## Security & Safety Protocols

### Never Auto-Approve

- All LinkedIn posts REQUIRE human approval (zero exceptions)
- Social media is public and permanent
- Brand reputation risk is HIGH
- Approval expiration: 72 hours (3 days)

### Content Validation Required

Before creating approval request:
- [ ] No confidential information disclosed
- [ ] No client names without permission
- [ ] No controversial or political content
- [ ] No negative comments about competitors
- [ ] Professional language throughout
- [ ] Aligned with brand voice guidelines

### Rate Limiting

- **Maximum Frequency:** 3 posts per week (per Business_Goals.md)
- **Minimum Spacing:** 24 hours between posts
- **Optimal Timing:** Tuesday-Thursday, 9-11 AM or 4-6 PM (business hours)

---

## Error Handling

### Common Issues

1. **No Recent Content Found**
   - Action: Suggest creating general industry insight post
   - Template: Use "Industry Insight/Tip" template
   - Source: Company_Handbook expertise areas

2. **Business_Goals.md Missing**
   - Action: Alert user to create file
   - Fallback: Use Company_Handbook for content themes

3. **LinkedIn API Authentication Failure**
   - Action: Log error to Dashboard
   - Alert: Create troubleshooting task in /Needs_Action
   - Reference: Setup guide for re-authentication

4. **Approval File Format Invalid**
   - Action: Validate YAML frontmatter
   - Fix: Auto-correct common formatting issues
   - Log: Warning in Dashboard if corrections made

---

## Testing & Validation

### Dry-Run Mode

When testing, use the `--dry-run` flag in linkedin_api_helper.py:
```bash
python scripts/linkedin_api_helper.py --dry-run --approval-file "path/to/file.md"
```

This will:
- Parse the approval file
- Validate content
- Show what would be posted
- NOT actually publish to LinkedIn

### Success Criteria

- [ ] Post content generated successfully
- [ ] Template selection appropriate
- [ ] Hashtags relevant and not excessive
- [ ] Approval request created in correct format
- [ ] Dashboard logging complete
- [ ] Content passes quality checklist

---

## Trigger Phrases for Auto-Activation

This skill should activate when user says:
- "post to linkedin"
- "share on linkedin"
- "create linkedin post"
- "generate linkedin content"
- "social media update"
- "publish to linkedin"
- "draft linkedin post"
- "schedule linkedin post"
- "create business post"
- "share [project/achievement] on linkedin"

---

## Reference Files

- [Post Templates](./reference/post-templates.md) - 5+ template examples with structure
- [Content Guidelines](./reference/content-guidelines.md) - Brand voice, tone, length standards
- [Hashtag Strategy](./reference/hashtag-strategy.md) - Industry tags, trending topics

---

## Examples

### Example 1: Project Milestone Post
```
User: "Create a LinkedIn post about completing Project Alpha"

Skill Actions:
1. Reads Business_Goals.md → finds Project Alpha
2. Checks Done/ folder → finds completed tasks
3. Selects "Project Milestone" template
4. Generates draft with achievement highlights
5. Adds hashtags: #ProjectManagement #SoftwareDevelopment #AgileDelivery
6. Creates APPROVAL_LINKEDIN_ProjectAlphaCompletion_2026-01-11.md
7. Logs to Dashboard
8. Waits for human approval
```

### Example 2: Industry Insight Post
```
User: "Share a tip about AI automation on LinkedIn"

Skill Actions:
1. Selects "Industry Insight/Tip" template
2. Crafts post about AI automation best practices
3. Adds hashtags: #ArtificialIntelligence #Automation #TechTrends
4. Creates approval request
5. Human reviews and approves
6. Posts to LinkedIn via API
7. Logs success to Dashboard
```

---

## Notes

- LinkedIn character limit: 3,000 characters (optimal: 150-300 words)
- Include line breaks for readability (every 2-3 sentences)
- Emoji usage: 1-2 max, professional context only
- Links: Include if relevant (LinkedIn auto-generates preview)
- Images/Video: Supported but requires additional configuration

---

*Skill Version: 1.0*
*Created: 2026-01-11*
*Branch: feat/linkedin-automation*
*Dependencies: handle-approval (Branch 1)*
