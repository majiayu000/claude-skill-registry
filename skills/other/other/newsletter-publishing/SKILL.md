---
name: newsletter-publishing
description: Email newsletter workflows for journalists and researchers. Use when creating, managing, or optimizing email newsletters, building subscriber lists, designing email templates, analyzing engagement metrics, or planning newsletter content calendars. Essential for independent journalists, academic communicators, and media organizations building direct audience relationships.
---

# Newsletter publishing

Practical workflows for building and managing email newsletters for journalism and academia.

## When to activate

- Creating a new newsletter from scratch
- Designing email templates for journalism content
- Building and segmenting subscriber lists
- Analyzing newsletter performance metrics
- Planning editorial calendars for newsletters
- Migrating between newsletter platforms
- Improving deliverability and open rates

## Newsletter architecture

### Content strategy framework

```markdown
## Newsletter strategy document

### Core identity
- **Name**:
- **Tagline** (one line):
- **What readers get**: [specific value proposition]
- **Frequency**: [ ] Daily [ ] Weekly [ ] Bi-weekly [ ] Monthly

### Target audience
- Primary reader:
- What they care about:
- Why they'll subscribe:
- What they'll do with this info:

### Content pillars
1. [Core topic 1] - [how often]
2. [Core topic 2] - [how often]
3. [Recurring feature] - [how often]

### Voice and tone
- Formal ↔ Conversational: [1-5]
- Serious ↔ Light: [1-5]
- Reported ↔ Personal: [1-5]

### Success metrics (first 6 months)
- Subscriber goal:
- Target open rate:
- Target click rate:
```

### Issue structure template

```markdown
## [Newsletter Name] - Issue #[XX]
**Date**: [Date]
**Subject line**: [Subject]
**Preview text**: [First 50-90 characters readers see]

---

### Opening hook
[2-3 sentences that make readers want to keep reading]

### Main story
[Your primary content - 300-600 words for most newsletters]

### Secondary items (if applicable)
- **Quick hit 1**: [Brief item with link]
- **Quick hit 2**: [Brief item with link]

### Recurring section
[Weekly column, data point, recommendation, etc.]

### Sign-off
[Personal note, call to action, or preview of next issue]

---

**Unsubscribe** | **Preferences** | **Forward to a friend**
```

## Technical implementation

### HTML email template (responsive)

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{newsletter_name}}</title>
  <style>
    /* Reset styles for email clients */
    body { margin: 0; padding: 0; width: 100%; }
    table { border-collapse: collapse; }
    img { border: 0; display: block; }

    /* Responsive container */
    .container {
      max-width: 600px;
      margin: 0 auto;
      font-family: Georgia, serif;
      font-size: 18px;
      line-height: 1.6;
      color: #333;
    }

    /* Dark mode support */
    @media (prefers-color-scheme: dark) {
      .container { background-color: #1a1a1a; color: #e0e0e0; }
      a { color: #6db3f2; }
    }

    /* Mobile styles */
    @media only screen and (max-width: 480px) {
      .container { padding: 15px !important; }
      h1 { font-size: 24px !important; }
    }
  </style>
</head>
<body>
  <table role="presentation" width="100%">
    <tr>
      <td align="center" style="padding: 20px;">
        <div class="container">
          <!-- Header -->
          <table width="100%">
            <tr>
              <td style="padding-bottom: 20px; border-bottom: 2px solid #333;">
                <h1 style="margin: 0;">{{newsletter_name}}</h1>
                <p style="margin: 5px 0 0; color: #666;">{{issue_date}}</p>
              </td>
            </tr>
          </table>

          <!-- Content -->
          <table width="100%">
            <tr>
              <td style="padding: 30px 0;">
                {{content}}
              </td>
            </tr>
          </table>

          <!-- Footer -->
          <table width="100%">
            <tr>
              <td style="padding-top: 20px; border-top: 1px solid #ddd; font-size: 14px; color: #666;">
                <p>You're receiving this because you subscribed to {{newsletter_name}}.</p>
                <p>
                  <a href="{{unsubscribe_url}}">Unsubscribe</a> |
                  <a href="{{preferences_url}}">Update preferences</a>
                </p>
              </td>
            </tr>
          </table>
        </div>
      </td>
    </tr>
  </table>
</body>
</html>
```

### Python newsletter sender

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional
from enum import Enum
import hashlib

class SubscriberStatus(Enum):
    ACTIVE = "active"
    UNSUBSCRIBED = "unsubscribed"
    BOUNCED = "bounced"
    COMPLAINED = "complained"

@dataclass
class Subscriber:
    email: str
    name: Optional[str] = None
    subscribed_at: datetime = field(default_factory=datetime.now)
    status: SubscriberStatus = SubscriberStatus.ACTIVE
    tags: List[str] = field(default_factory=list)
    custom_fields: Dict = field(default_factory=dict)

    @property
    def hash_id(self) -> str:
        """Generate unique ID for unsubscribe links."""
        return hashlib.md5(self.email.encode()).hexdigest()[:12]

@dataclass
class NewsletterIssue:
    subject: str
    preview_text: str
    html_content: str
    plain_text: str
    scheduled_at: Optional[datetime] = None
    sent_at: Optional[datetime] = None
    issue_number: int = 0

    # Metrics
    sent_count: int = 0
    delivered_count: int = 0
    opened_count: int = 0
    clicked_count: int = 0
    bounced_count: int = 0
    unsubscribed_count: int = 0

    @property
    def open_rate(self) -> float:
        if self.delivered_count == 0:
            return 0.0
        return (self.opened_count / self.delivered_count) * 100

    @property
    def click_rate(self) -> float:
        if self.delivered_count == 0:
            return 0.0
        return (self.clicked_count / self.delivered_count) * 100

class NewsletterManager:
    """Core newsletter operations."""

    def __init__(self, name: str):
        self.name = name
        self.subscribers: List[Subscriber] = []
        self.issues: List[NewsletterIssue] = []

    def add_subscriber(self, email: str, name: str = None,
                       tags: List[str] = None) -> Subscriber:
        """Add new subscriber with double opt-in pending."""
        sub = Subscriber(
            email=email.lower().strip(),
            name=name,
            tags=tags or []
        )
        self.subscribers.append(sub)
        return sub

    def segment_subscribers(self, tags: List[str] = None,
                           min_engagement: float = None) -> List[Subscriber]:
        """Get subscribers matching criteria."""
        active = [s for s in self.subscribers
                  if s.status == SubscriberStatus.ACTIVE]

        if tags:
            active = [s for s in active
                     if any(t in s.tags for t in tags)]

        return active

    def calculate_engagement_score(self, subscriber: Subscriber) -> float:
        """Score subscriber engagement 0-100."""
        # Implementation would track opens/clicks per subscriber
        return 50.0  # Placeholder
```

## Subscriber management

### List hygiene workflow

```python
from datetime import datetime, timedelta

def clean_subscriber_list(manager: NewsletterManager,
                         inactive_threshold_days: int = 180) -> dict:
    """Identify and handle inactive subscribers."""
    cutoff = datetime.now() - timedelta(days=inactive_threshold_days)

    results = {
        'total': len(manager.subscribers),
        'active': 0,
        'inactive': [],
        'bounced': [],
        'unsubscribed': []
    }

    for sub in manager.subscribers:
        if sub.status == SubscriberStatus.BOUNCED:
            results['bounced'].append(sub.email)
        elif sub.status == SubscriberStatus.UNSUBSCRIBED:
            results['unsubscribed'].append(sub.email)
        elif sub.status == SubscriberStatus.ACTIVE:
            # Check last engagement
            engagement = manager.calculate_engagement_score(sub)
            if engagement < 10:  # Very low engagement
                results['inactive'].append(sub.email)
            else:
                results['active'] += 1

    return results

def run_reengagement_campaign(inactive_subscribers: List[str]) -> None:
    """Send win-back campaign to inactive subscribers."""
    # Send "We miss you" campaign
    # If no engagement after 2 attempts, mark for removal
    pass
```

### Subscriber segmentation

```markdown
## Recommended segments

### By engagement
- **VIPs**: Open rate > 80%, always click
- **Engaged**: Open rate 40-80%
- **Casual**: Open rate 10-40%
- **At-risk**: Haven't opened in 90 days
- **Inactive**: Haven't opened in 180 days

### By interest (tag-based)
- Topic preferences from signup
- Content they've clicked
- Surveys/polls they've answered

### By source
- Organic (website signup)
- Referral (forwarded by friend)
- Social media
- Paywall/registration wall
```

## Subject line optimization

### High-performing patterns

```markdown
## Subject line formulas that work

### For news/journalism
- **Breaking format**: "Breaking: [Concise news]"
- **Numbers**: "[X] things we learned about [topic]"
- **Question**: "Why did [entity] do [thing]?"
- **Direct**: "[Topic]: What you need to know"

### For analysis/opinion
- **Take**: "The real story behind [event]"
- **Contrarian**: "Why everyone is wrong about [topic]"
- **Insider**: "What [industry] insiders know about [topic]"

### What to avoid
- ALL CAPS
- Excessive punctuation!!!
- Clickbait that doesn't deliver
- Spam trigger words (FREE, URGENT, ACT NOW)
- Misleading preview text
```

### A/B testing framework

```python
import random
from typing import List, Tuple

def ab_test_subject_lines(subscribers: List[Subscriber],
                         subject_a: str,
                         subject_b: str,
                         test_percentage: float = 0.2) -> dict:
    """
    Test two subject lines on subset before full send.
    """
    test_size = int(len(subscribers) * test_percentage)
    test_group = random.sample(subscribers, test_size)

    # Split test group
    half = len(test_group) // 2
    group_a = test_group[:half]
    group_b = test_group[half:]

    remaining = [s for s in subscribers if s not in test_group]

    return {
        'group_a': {
            'subject': subject_a,
            'subscribers': group_a,
            'size': len(group_a)
        },
        'group_b': {
            'subject': subject_b,
            'subscribers': group_b,
            'size': len(group_b)
        },
        'remaining': {
            'subscribers': remaining,
            'size': len(remaining),
            'note': 'Send winner to this group after test period'
        },
        'test_duration_hours': 4
    }
```

## Deliverability best practices

### Email authentication setup

```markdown
## DNS records for deliverability

### SPF record
```
v=spf1 include:_spf.youresp.com ~all
```

### DKIM
- Generate keys through your ESP
- Add TXT record with public key
- Verify signature is applied to outgoing mail

### DMARC
```
v=DMARC1; p=quarantine; rua=mailto:dmarc@yourdomain.com
```

### Checklist before sending
- [ ] SPF, DKIM, DMARC configured
- [ ] Sending domain warmed up
- [ ] List is clean (no hard bounces)
- [ ] Unsubscribe link works
- [ ] Physical address in footer (CAN-SPAM)
- [ ] Test email received in inbox (not spam)
```

### Spam score checklist

```markdown
## Before you send

### Content checks
- [ ] No spam trigger words
- [ ] Text-to-image ratio good (mostly text)
- [ ] All links are to reputable domains
- [ ] No URL shorteners (use full links)
- [ ] Plain text version included

### Technical checks
- [ ] From address matches sending domain
- [ ] Reply-to address is monitored
- [ ] Preheader text is set
- [ ] Images have alt text
- [ ] Links are not broken
```

## Analytics and optimization

### Key metrics dashboard

```python
from dataclasses import dataclass

@dataclass
class NewsletterAnalytics:
    """Track newsletter performance over time."""

    issue: NewsletterIssue

    def summary(self) -> dict:
        return {
            'issue_number': self.issue.issue_number,
            'sent': self.issue.sent_count,
            'delivered': self.issue.delivered_count,
            'delivery_rate': self._pct(self.issue.delivered_count,
                                       self.issue.sent_count),
            'opens': self.issue.opened_count,
            'open_rate': self.issue.open_rate,
            'clicks': self.issue.clicked_count,
            'click_rate': self.issue.click_rate,
            'click_to_open': self._pct(self.issue.clicked_count,
                                       self.issue.opened_count),
            'unsubscribes': self.issue.unsubscribed_count,
            'unsubscribe_rate': self._pct(self.issue.unsubscribed_count,
                                          self.issue.delivered_count),
        }

    def _pct(self, numerator: int, denominator: int) -> float:
        if denominator == 0:
            return 0.0
        return round((numerator / denominator) * 100, 2)

# Benchmarks (journalism newsletters)
BENCHMARKS = {
    'open_rate': {'good': 40, 'excellent': 55},
    'click_rate': {'good': 4, 'excellent': 8},
    'unsubscribe_rate': {'acceptable': 0.5, 'concerning': 1.0},
}
```

## Platform comparison

| Platform | Best for | Pricing model | Key feature |
|----------|----------|---------------|-------------|
| Substack | Writer-first, paid subs | Revenue share | Built-in payments |
| Buttondown | Developers, minimal | Per subscriber | Markdown native |
| Ghost | Publishers, memberships | Flat fee | Full CMS included |
| beehiiv | Growth-focused | Freemium | Referral tools |
| ConvertKit | Creators | Per subscriber | Automation |
| Mailchimp | Small orgs | Tiered | Easy templates |

## Legal compliance

### CAN-SPAM requirements (US)

```markdown
- [ ] Accurate "From" name and email
- [ ] Non-deceptive subject line
- [ ] Physical postal address included
- [ ] Working unsubscribe mechanism
- [ ] Unsubscribe honored within 10 days
- [ ] No purchased lists
```

### GDPR requirements (EU subscribers)

```markdown
- [ ] Explicit consent obtained (not pre-checked)
- [ ] Clear privacy policy linked
- [ ] Easy unsubscribe process
- [ ] Data export available on request
- [ ] Data deletion on request
- [ ] Record of consent stored
```

## Related skills

- **web-scraping** - Automate content gathering for newsletters
- **data-journalism** - Include data visualizations in emails
- **academic-writing** - Write clear, structured content

---

## Skill metadata

| Field | Value |
|-------|-------|
| Version | 1.0.0 |
| Created | 2025-12-26 |
| Author | Claude Skills for Journalism |
| Domain | Publishing, Marketing |
| Complexity | Intermediate |
