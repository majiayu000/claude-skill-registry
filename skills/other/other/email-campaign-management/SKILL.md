---
name: email-campaign-management
description: Complete workflow for email marketing campaigns with conversion tracking and trial activation. Use when (1) Creating email campaigns, (2) Sending campaign emails via Resend API, (3) Tracking conversions and clicks, (4) Activating trials for campaign users, (5) Generating campaign reports, (6) Sending reminder emails. CRITICAL - Follow Resend rate limits (2 emails/second), use UPPERCASE for PostgreSQL enums.
---

# Email Campaign Management - Complete Workflow

**Purpose**: Reusable workflow for creating, tracking, and managing email marketing campaigns with conversion tracking, reminder emails, and trial activation.

**Scope**: Growth marketing, email campaigns, conversion tracking, trial activation, campaign analytics

---

## Campaign Database Schema

### `campaigns` table
```sql
CREATE TABLE campaigns (
    id UUID PRIMARY KEY,
    campaign_id VARCHAR(255) UNIQUE NOT NULL,  -- e.g., "ny2026", "summer2026"
    name VARCHAR(255) NOT NULL,
    description TEXT,
    trial_days INTEGER,
    tier VARCHAR(50),  -- ENTERPRISE, SCALE, etc.
    plan_name TEXT,
    offer_expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### `campaign_clicks` table
```sql
CREATE TABLE campaign_clicks (
    id UUID PRIMARY KEY,
    campaign_id VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    click_source VARCHAR(100),  -- e.g., "cta_button", "events_click"
    utm_source VARCHAR(100),
    utm_medium VARCHAR(100),
    utm_campaign VARCHAR(100),
    converted BOOLEAN DEFAULT FALSE,
    converted_at TIMESTAMP,
    user_id UUID,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## Campaign Statistics Query Patterns

### Get Campaign Overview
```sql
SELECT
    COUNT(*) as total_clicks,
    COUNT(DISTINCT email) as unique_users,
    COUNT(CASE WHEN converted = TRUE THEN 1 END) as converted_count,
    COUNT(CASE WHEN converted = FALSE THEN 1 END) as pending_count,
    ROUND(100.0 * COUNT(CASE WHEN converted = TRUE THEN 1 END) / COUNT(*), 2) as conversion_rate
FROM campaign_clicks
WHERE campaign_id = 'campaign-id-here';
```

### Get Registered vs Non-Registered
```sql
SELECT
    COUNT(CASE WHEN u.id IS NOT NULL THEN 1 END) as registered_users,
    COUNT(CASE WHEN u.id IS NULL THEN 1 END) as non_registered_users,
    COUNT(CASE WHEN s.tier != 'free' AND s.status = 'active' THEN 1 END) as already_paid_users
FROM campaign_clicks cc
LEFT JOIN users u ON u.email = cc.email
LEFT JOIN subscriptions s ON s.user_id = u.id
WHERE cc.campaign_id = 'campaign-id-here'
  AND cc.converted = FALSE;
```

---

## Resend API Integration

### Rate Limiting (CRITICAL)
**Resend Free Tier**: 2 requests per second (NOT 100/minute!)

**Correct Implementation**:
```python
import time

RATE_LIMIT_DELAY = 0.5  # 2 emails per second

for email in emails:
    send_email(email)
    if i < len(emails):
        time.sleep(RATE_LIMIT_DELAY)  # Wait 0.5 seconds
```

**WRONG Implementation** (causes 429 errors):
```python
# DON'T DO THIS - sends too fast
RATE_LIMIT = 100  # emails per minute
for email in emails:
    send_email(email)
    # Only pause every 100 emails - TOO LATE!
    if i % RATE_LIMIT == 0:
        time.sleep(60)
```

### Email Sending Function
```python
import os
import requests

RESEND_API_KEY = os.getenv("RESEND_API_KEY")
RESEND_API_URL = "https://api.resend.com/emails"
FROM_EMAIL = "no-reply@ainative.studio"

def send_campaign_email(email: str, campaign_id: str, template_html: str):
    """Send campaign email via Resend."""

    # Replace template variables
    html = template_html.replace("{{email}}", email)
    html = html.replace("{{campaign_id}}", campaign_id)

    payload = {
        "from": FROM_EMAIL,
        "to": [email],
        "subject": "Your campaign subject here",
        "html": html,
        "tags": [
            {"name": "campaign", "value": campaign_id},
            {"name": "type", "value": "reminder"}
        ]
    }

    response = requests.post(
        RESEND_API_URL,
        headers={
            "Authorization": f"Bearer {RESEND_API_KEY}",
            "Content-Type": "application/json"
        },
        json=payload,
        timeout=10
    )

    if response.status_code in [200, 201]:
        return True, response.json().get("id")
    else:
        return False, response.text
```

---

## Trial Activation Workflow

### Activate Trial (CRITICAL: Use UPPERCASE Enums)
```python
def activate_trial(user, campaign_id: str, trial_days: int, plan_name: str):
    """Activate ENTERPRISE trial for user."""

    trial_end = datetime.utcnow() + timedelta(days=trial_days)

    # CRITICAL: PostgreSQL enums are UPPERCASE
    # 'enterprise' → 'ENTERPRISE'
    # 'active' NOT 'trial' (trial status doesn't exist)

    if user['subscription_id']:
        # Update existing subscription
        cur.execute("""
            UPDATE subscriptions
            SET tier = 'ENTERPRISE',
                status = 'active',
                trial_ends_at = %s,
                plan_name = %s,
                plan_price = 0,
                current_period_end = %s,
                updated_at = NOW()
            WHERE id = %s
        """, (trial_end, plan_name, trial_end, user['subscription_id']))
    else:
        # Create new subscription
        cur.execute("""
            INSERT INTO subscriptions (
                user_id, tier, status,
                trial_ends_at, plan_name, plan_price,
                billing_email, start_date,
                current_period_start, current_period_end,
                max_users, max_projects, monthly_token_limit,
                max_ai_requests_per_day, max_models,
                created_at, updated_at
            ) VALUES (
                %s, 'ENTERPRISE', 'active',
                %s, %s, 0,
                %s, NOW(),
                NOW(), %s,
                10, 15, 1000000,
                10000, 100,
                NOW(), NOW()
            )
        """, (
            str(user['user_id']),
            trial_end,
            plan_name,
            user['email'],
            trial_end
        ))

    # Mark click as converted
    cur.execute("""
        UPDATE campaign_clicks
        SET converted = TRUE,
            converted_at = NOW(),
            user_id = %s
        WHERE id = %s
    """, (str(user['user_id']), user['click_id']))

    conn.commit()
```

---

## Common Pitfalls & Solutions

### PITFALL 1: Case-Sensitive Enums
**Problem**: `'enterprise'` fails with "invalid input value for enum"
**Solution**: Always use UPPERCASE: `'ENTERPRISE'`, `'SCALE'`, `'FREE'`

### PITFALL 2: Invalid Status Values
**Problem**: Using `status = 'trial'` (doesn't exist)
**Solution**: Use `status = 'active'` with `trial_ends_at` field

### PITFALL 3: Rate Limiting Too High
**Problem**: Setting rate limit to 100/minute causes 429 errors
**Solution**: Use 2 per second (0.5s delay between sends)

### PITFALL 4: Missing Organization ID
**Problem**: Some users don't have `organization_id`, causing NULL constraint errors
**Solution**: Check if `organization_id` exists before INSERT, use separate query if NULL

### PITFALL 5: Hardcoded Email in Templates
**Problem**: Test email in production template
**Solution**: Use `{{email}}` template variable, replace at send time

### PITFALL 6: Not Closing DB Connections
**Problem**: "too many clients already" error
**Solution**: Always use try/finally to close connections

---

## Email Template Requirements

### Template Structure
All campaign email templates MUST be stored in:
```
src/backend/app/services/templates/{campaign_id}_{type}.html
```

**Example filenames**:
- `ny2026_gift.html` - Initial campaign email
- `ny2026_reminder.html` - Reminder for non-registered users
- `summer2026_welcome.html` - Welcome email

### Required Template Variables
```html
<!-- Email parameter for personalized links -->
<a href="https://www.ainative.studio/register?gift={{campaign_id}}&email={{email}}">
    Claim Your Trial
</a>
```

### Styling Standards (Dark Theme)
```css
/* Base colors */
body {
    font-family: 'Poppins', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background-color: #131726;
}

.email-container {
    background-color: #22263c;
    border-radius: 16px;
}

/* Header gradient */
.header {
    background: linear-gradient(135deg, #4B6FED 0%, #5867EF 100%);
    padding: 50px 40px;
}

/* CTA Button */
.cta-button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: #ffffff;
    padding: 18px 48px;
    border-radius: 12px;
}
```

---

## Quick Reference Commands

### Check Campaign Stats
```bash
railway run -s "AINative- Core -Production" psql -c "
SELECT
    COUNT(*) as total_clicks,
    COUNT(DISTINCT email) as unique_users,
    COUNT(CASE WHEN converted THEN 1 END) as converted
FROM campaign_clicks
WHERE campaign_id = 'your-campaign-id';
"
```

### Send Reminder Campaign
```bash
railway run -s "AINative- Core -Production" \
  python3 scripts/send_{campaign_id}_reminder.py --yes
```

---

## End-to-End Campaign Checklist

- [ ] Create campaign record in database
- [ ] Add campaign to backend `VALID_CAMPAIGNS` config
- [ ] Create email templates (gift + reminder)
- [ ] Test email send to yourself
- [ ] Deploy backend changes to Railway
- [ ] Launch initial campaign
- [ ] Monitor click tracking (first 24h)
- [ ] Check conversion rate (day 3)
- [ ] Send reminder emails (day 7)
- [ ] Activate trials for registered users
- [ ] Generate final campaign report
