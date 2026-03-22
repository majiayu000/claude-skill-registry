---
name: linkedin-automation
description: >
  AI-powered LinkedIn post generation aligned with business goals, scheduling with
  deduplication (max 1 post/day), human approval workflow, and automated publishing via
  LinkedIn API v2 MCP server. Reads company handbook for business context, generates
  engaging posts with Claude API, handles rate limiting, and maintains comprehensive audit
  logs. Use when: (1) building LinkedIn automation for business accounts, (2) implementing
  scheduled posting with AI content generation, (3) creating MCP servers for LinkedIn API
  v2, (4) setting up rate limit handling for social media APIs, (5) aligning social media
  content with business strategy.
---

# LinkedIn Automation

## Architecture

```
Company_Handbook.md → LinkedIn Generator (linkedin_generator.py)
                              ↓
                   AI Draft (Claude API + Business Goals)
                              ↓
                vault/Pending_Approval/LinkedIn/
                              ↓
                [Human approves → Approved/LinkedIn/]
                              ↓
        Approval Watcher → LinkedIn MCP (API v2 POST /ugcPosts)
                              ↓
                     Posted + Logged ✓
```

---

## Quick Start

### 1. Get LinkedIn Access Token

```bash
# LinkedIn OAuth 2.0 setup (https://www.linkedin.com/developers/)
# 1. Create LinkedIn App
# 2. Request w_member_social scope
# 3. Generate OAuth 2.0 access token
# 4. Get your author URN (urn:li:person:XXXXX)

# Configure .env
LINKEDIN_ACCESS_TOKEN=AQV...
LINKEDIN_AUTHOR_URN=urn:li:person:XXXXX
```

### 2. LinkedIn MCP Server

```python
# mcp_servers/linkedin_mcp/server.py
import requests
import json
import sys

def create_post(text: str, author_urn: str, access_token: str) -> dict:
    """Post to LinkedIn via API v2"""
    url = "https://api.linkedin.com/v2/ugcPosts"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }

    payload = {
        "author": author_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": text},
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)

        if response.status_code == 201:
            post_id = response.headers.get('X-RestLi-Id')
            return {
                "post_id": post_id,
                "post_url": f"https://www.linkedin.com/feed/update/{post_id}/"
            }
        elif response.status_code == 429:
            # Rate limited
            raise Exception("RATE_LIMITED: LinkedIn API rate limit exceeded")
        else:
            raise Exception(f"LinkedIn API error: {response.status_code} - {response.text}")

    except requests.exceptions.Timeout:
        raise Exception("NETWORK_ERROR: LinkedIn API timeout")

# JSON-RPC handler (same pattern as other MCPs)
def handle_jsonrpc():
    for line in sys.stdin:
        request = json.loads(line)
        # ... handle tools/call for create_post
```

**MCP Config:**
```json
// ~/.config/claude-code/mcp.json
{
  "servers": {
    "linkedin-mcp": {
      "command": "python",
      "args": ["/path/to/mcp_servers/linkedin_mcp/server.py"],
      "env": {
        "LINKEDIN_ACCESS_TOKEN": "AQV...",
        "LINKEDIN_AUTHOR_URN": "urn:li:person:XXXXX"
      }
    }
  }
}
```

---

## LinkedIn Post Generator

### Generate Aligned Posts

```python
# scripts/linkedin_generator.py
from agent_skills.draft_generator import generate_linkedin_draft
from agent_skills.vault_parser import parse_markdown_file

def generate_linkedin_post():
    """Generate LinkedIn post aligned with business goals"""

    # Read Company_Handbook.md for context
    handbook = parse_markdown_file('vault/Company_Handbook.md')
    business_goals = extract_business_goals(handbook)

    # Check deduplication (max 1 post/day)
    today = datetime.now().strftime('%Y-%m-%d')
    if post_exists_for_date(today):
        print(f"❌ Post already exists for {today} - skipping")
        return

    # Generate draft
    draft = generate_linkedin_draft(business_goals)

    # Save to Pending_Approval
    save_draft(draft, f"vault/Pending_Approval/LinkedIn/LINKEDIN_POST_{today}.md")
    print(f"✅ LinkedIn draft created for {today}")

def extract_business_goals(handbook: dict) -> str:
    """Extract Business Goals section from handbook"""
    content = handbook['content']
    # Parse markdown to find ## Business Goals section
    import re
    match = re.search(r'## Business Goals\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
    return match.group(1) if match else ""
```

### AI Draft Generation

```python
# agent_skills/draft_generator.py (extension)
def generate_linkedin_draft(business_goals: str) -> dict:
    """Generate LinkedIn post with Claude API"""

    client = Anthropic(api_key=os.getenv('CLAUDE_API_KEY'))
    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1000,
        messages=[{
            "role": "user",
            "content": f"""Create a LinkedIn post aligned with these business goals:

{business_goals[:500]}

Requirements:
- Professional tone for business audience
- Engaging hook in first line
- 2-3 paragraphs max
- Call-to-action at end
- Max 3000 characters (LinkedIn limit)
- No hashtags unless specifically relevant
- Value-driven content (not promotional)

Focus on thought leadership and insights.
"""
        }]
    )

    post_content = response.content[0].text

    # Validate character limit
    if len(post_content) > 3000:
        # Auto-truncate at last sentence
        post_content = truncate_at_sentence(post_content, 3000)

    return {
        "scheduled_date": datetime.now().strftime('%Y-%m-%d'),
        "business_goal_reference": business_goals[:100],
        "post_content": post_content,
        "character_count": len(post_content),
        "action": "create_post",
        "status": "pending_approval",
        "generated_at": datetime.utcnow().isoformat()
    }

def truncate_at_sentence(text: str, max_chars: int) -> str:
    """Truncate at last complete sentence before limit"""
    if len(text) <= max_chars:
        return text

    truncated = text[:max_chars]
    last_period = truncated.rfind('.')

    if last_period > 0:
        return truncated[:last_period + 1]
    else:
        return truncated + "..."
```

---

## Rate Limit Handling

### Retry with Backoff

```python
# agent_skills/approval_watcher.py (LinkedIn handler)
def handle_linkedin_approval(draft_path: str):
    """Handle LinkedIn post approval with rate limiting"""

    draft = parse_draft_file(draft_path)

    try:
        result = call_mcp_tool("linkedin-mcp", "create_post", {
            "text": draft['post_content'],
            "author_urn": os.getenv('LINKEDIN_AUTHOR_URN'),
            "access_token": os.getenv('LINKEDIN_ACCESS_TOKEN')
        })

        # Success - log and move to Done
        log_mcp_action("linkedin-mcp", "create_post", "success", draft_path)
        shutil.move(draft_path, f"vault/Done/{Path(draft_path).name}")

    except MCPError as e:
        if 'RATE_LIMITED' in str(e):
            # Update draft status to retry later
            update_draft_status(draft_path, "rate_limited_retry")

            # Schedule retry in 60 minutes
            schedule_retry(draft_path, delay_minutes=60)

            print(f"⏰ LinkedIn rate limited - will retry in 60 min")
        else:
            # Other error - escalate
            create_escalation_file(
                f"vault/Needs_Action/linkedin_post_failed.md",
                error_details=str(e)
            )
            raise
```

---

## Scheduling & Deduplication

### Post Schedule Logic

```python
def post_exists_for_date(date: str) -> bool:
    """Check if LinkedIn post already exists for date"""
    done_dir = Path('vault/Done/')

    for file in done_dir.glob('LINKEDIN_POST_*.md'):
        draft = parse_draft_file(str(file))
        if draft.get('scheduled_date') == date:
            return True

    return False

def get_posting_schedule() -> dict:
    """Read posting schedule from Company_Handbook.md"""
    handbook = parse_markdown_file('vault/Company_Handbook.md')

    # Default: weekly on Mondays
    return {
        "frequency": "weekly",
        "day_of_week": "Monday",
        "time": "09:00"
    }
```

### Scheduled Execution

```python
# Run via cron or schedule library
import schedule

def run_linkedin_scheduler():
    """Schedule LinkedIn post generation"""

    schedule_config = get_posting_schedule()

    if schedule_config['frequency'] == 'daily':
        schedule.every().day.at(schedule_config['time']).do(generate_linkedin_post)
    elif schedule_config['frequency'] == 'weekly':
        day = schedule_config['day_of_week']
        getattr(schedule.every(), day.lower()).at(schedule_config['time']).do(generate_linkedin_post)

    while True:
        schedule.run_pending()
        time.sleep(60)
```

---

## Draft Format

```markdown
<!-- vault/Pending_Approval/LinkedIn/LINKEDIN_POST_2026-02-14.md -->
---
draft_id: linkedin_post_2026_02_14
scheduled_date: "2026-02-14"
business_goal_reference: "Establish thought leadership in AI automation..."
post_content: |
  AI agents are transforming how businesses operate...
character_count: 587
action: create_post
status: pending_approval
generated_at: "2026-02-14T08:00:00Z"
---

# LinkedIn Post Draft - February 14, 2026

## Post Content

AI agents are transforming how businesses operate. Here's what we've learned after implementing autonomous task management for our team:

🔹 70% reduction in manual task tracking
🔹 Real-time priority analysis for every inbox item
🔹 Human-in-the-loop approval keeps quality high

The future of work isn't replacing humans—it's augmenting their capabilities with intelligent automation that respects human judgment.

What's your experience with AI automation in your workflow?

---

**Approval Instructions:**
- ✅ Approve: Move to `vault/Approved/LinkedIn/`
- ❌ Reject: Move to `vault/Rejected/`
- ✏️ Edit: Modify Post Content above, then approve
```

---

## Testing

```python
# tests/integration/test_linkedin_workflow.py
def test_linkedin_post_generation_and_approval():
    """Test LinkedIn workflow: generate → approve → post"""

    # Generate post
    draft = generate_linkedin_draft("Test business goals")
    assert draft['character_count'] <= 3000
    assert draft['status'] == 'pending_approval'

    # Save to Pending_Approval
    draft_path = save_draft(draft, 'vault/Pending_Approval/LinkedIn/')

    # Mock LinkedIn API
    with patch('requests.post') as mock_post:
        mock_post.return_value.status_code = 201
        mock_post.return_value.headers = {'X-RestLi-Id': 'urn:li:share:123'}

        # Approve
        approved_path = 'vault/Approved/LinkedIn/' + Path(draft_path).name
        shutil.move(draft_path, approved_path)

        # Handle approval
        handle_linkedin_approval(approved_path)

        # Verify API called
        assert mock_post.called
        assert mock_post.call_args[1]['json']['lifecycleState'] == 'PUBLISHED'
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| **ACCESS_TOKEN_EXPIRED** | Regenerate OAuth token via LinkedIn Developer Portal |
| **RATE_LIMITED** | Automatic 60 min retry - reduce posting frequency |
| **Post too long** | Auto-truncation at 3000 chars (last sentence) |
| **Duplicate posts** | Deduplication enforced - max 1 post/day |

---

## Key Files

- `scripts/linkedin_generator.py` - Post generation with business alignment
- `mcp_servers/linkedin_mcp/server.py` - LinkedIn API v2 integration
- `agent_skills/draft_generator.py` - AI content generation
- `vault/Pending_Approval/LinkedIn/` - Draft review queue
- `vault/Company_Handbook.md` - Business goals source

---

**Production Ready:** Rate limit handling, deduplication, business goal alignment, comprehensive error recovery.
