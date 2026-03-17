---
name: post-linkedin
description: |
  Automatically create and post content on LinkedIn to generate business visibility
  and sales leads. Drafts posts based on business goals, creates approval requests,
  and publishes via Playwright browser automation after human approval.
  Use when scheduled to post or when the user requests a LinkedIn post.
---

# Post to LinkedIn

Create and publish LinkedIn posts for business development and sales generation.

## Workflow

### 1. Generate Post Content
Read `vault/Business_Goals.md` to understand current business objectives.
Draft a LinkedIn post that:
- Highlights business expertise or achievements
- Provides value to the target audience
- Includes a call-to-action when appropriate
- Stays professional and on-brand
- Is 150-300 words (optimal LinkedIn length)

### 2. Create Approval Request
**All LinkedIn posts require human approval before publishing.**

Create an approval file in `vault/Pending_Approval/`:
```markdown
---
type: approval_request
request_id: "YYYYMMDD_HHMMSS_linkedin_post"
action: linkedin_post
priority: medium
created: ISO-8601
expires: ISO-8601 (24 hours from creation)
status: pending
details:
  platform: "linkedin"
  content_preview: "First 100 chars of post..."
---

# Approval Required: LinkedIn Post

## Proposed Post Content
[Full post text here]

## How to Respond
- **To Approve**: Move this file to the `/Approved` folder
- **To Reject**: Move this file to the `/Rejected` folder
```

### 3. Publish (After Approval)
Once the file appears in `vault/Approved/`:

1. Start Playwright MCP if not running:
   ```bash
   bash .claude/skills/browsing-with-playwright/scripts/start-server.sh
   ```

2. Navigate to LinkedIn:
   ```bash
   python3 scripts/mcp-client.py call -u http://localhost:8808 -t browser_navigate \
     -p '{"url": "https://www.linkedin.com/feed/"}'
   ```

3. Click "Start a post" button:
   ```bash
   python3 scripts/mcp-client.py call -u http://localhost:8808 -t browser_snapshot -p '{}'
   # Find the "Start a post" button ref, then click it
   ```

4. Type the post content:
   ```bash
   python3 scripts/mcp-client.py call -u http://localhost:8808 -t browser_type \
     -p '{"element": "Post editor", "ref": "<ref>", "text": "<post content>"}'
   ```

5. Click Post/Publish:
   ```bash
   python3 scripts/mcp-client.py call -u http://localhost:8808 -t browser_click \
     -p '{"element": "Post button", "ref": "<ref>"}'
   ```

6. Verify success by checking for confirmation

### 4. Log the Action
Write to `vault/Logs/YYYY-MM-DD.json`:
```json
{
  "timestamp": "ISO-8601",
  "action_type": "linkedin_post_published",
  "actor": "claude_code",
  "platform": "linkedin",
  "content_preview": "First 100 chars...",
  "approval_status": "approved",
  "approved_by": "human",
  "result": "success"
}
```

### 5. Move to Done
Move the approval file from `/Approved` to `/Done` after publishing.

## Post Ideas by Category

### Thought Leadership
- Industry insights and trends
- Lessons learned from recent projects
- Best practices and tips

### Business Updates
- New service offerings
- Team achievements
- Case studies and success stories

### Engagement Posts
- Questions for the audience
- Polls about industry topics
- Celebrating milestones

## Important Rules
- **NEVER post without human approval** - always create approval request first
- Keep posts professional and aligned with business goals
- Include relevant hashtags (3-5 per post)
- Avoid controversial topics
- Do not share confidential client information
- Log every post attempt (success or failure)
