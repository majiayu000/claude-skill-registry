---
name: email-marketing
description: Эксперт по email-маркетингу. Используй для email кампаний, автоматизации, сегментации, deliverability и A/B тестов.
---

# Email Marketing Expert

Comprehensive expertise in email marketing strategy and execution.

## Core Competencies

### Strategy
- List building and segmentation
- Email calendar planning
- Lifecycle marketing
- Personalization strategy
- A/B testing frameworks

### Automation
- Welcome sequences
- Nurture campaigns
- Trigger-based emails
- Re-engagement flows
- Win-back sequences

### Deliverability
- Sender reputation management
- Authentication (SPF, DKIM, DMARC)
- List hygiene
- Spam trap avoidance
- ISP relationship management

## Email Types

### Marketing Emails
- Newsletters
- Promotional campaigns
- Product announcements
- Event invitations
- Content distribution

### Automated Sequences
- Welcome series
- Onboarding sequences
- Lead nurturing
- Abandoned cart
- Re-engagement
- Win-back

### Transactional Emails
- Order confirmations
- Shipping updates
- Password resets
- Account notifications

## Email Authentication Setup

```dns
# SPF Record
v=spf1 include:_spf.google.com include:sendgrid.net ~all

# DKIM Record
selector._domainkey.example.com IN TXT "v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3..."

# DMARC Record
_dmarc.example.com IN TXT "v=DMARC1; p=quarantine; rua=mailto:dmarc@example.com"
```

## Key Metrics

| Metric | Benchmark | Description |
|--------|-----------|-------------|
| Open Rate | 20-25% | Unique opens / Delivered |
| Click Rate | 2-5% | Unique clicks / Delivered |
| Click-to-Open | 10-15% | Clicks / Opens |
| Unsubscribe Rate | <0.5% | Unsubscribes / Delivered |
| Bounce Rate | <2% | Bounces / Sent |
| Spam Complaints | <0.1% | Complaints / Delivered |
| Conversion Rate | Varies | Conversions / Clicks |

## Segmentation Strategies

```yaml
Behavioral Segmentation:
  - Purchase history
  - Email engagement
  - Website activity
  - Product preferences
  - Cart abandonment

Demographic Segmentation:
  - Location/timezone
  - Job title/industry
  - Company size
  - Age/gender

Lifecycle Stages:
  - New subscribers
  - Active customers
  - At-risk (declining engagement)
  - Churned (re-activation target)
  - VIP/high-value
```

## Automation Workflows

### Welcome Sequence

```yaml
Day 0 - Welcome Email:
  trigger: subscription_confirmed
  content: Brand introduction, expectations
  cta: Complete profile

Day 2 - Value Email:
  trigger: previous_opened OR time_delay
  content: Top content, quick wins
  cta: Explore resources

Day 5 - Social Proof:
  trigger: time_delay
  content: Customer stories, testimonials
  cta: See case studies

Day 7 - Soft CTA:
  trigger: time_delay
  content: Product introduction
  cta: Start free trial
```

### Abandoned Cart Flow

```yaml
Hour 1 - Reminder:
  trigger: cart_abandoned
  content: Items in cart reminder
  cta: Complete purchase

Hour 24 - Urgency:
  trigger: no_purchase
  content: Items may sell out
  cta: Secure your items

Hour 72 - Incentive:
  trigger: no_purchase
  content: Special discount offer
  cta: Get 10% off
```

## A/B Testing Framework

### Test Elements

```yaml
Subject Lines:
  - Length (short vs long)
  - Personalization
  - Emojis
  - Questions vs statements
  - Urgency words

Content:
  - Layout (single vs multi-column)
  - Image count and placement
  - CTA button color/text
  - Copy length
  - Personalization depth

Timing:
  - Send day
  - Send time
  - Timezone optimization
```

### Statistical Significance

```python
import scipy.stats as stats

def calculate_significance(control_opens, control_sent,
                          variant_opens, variant_sent,
                          confidence=0.95):
    """Calculate if A/B test result is significant."""

    control_rate = control_opens / control_sent
    variant_rate = variant_opens / variant_sent

    # Pooled proportion
    pooled = (control_opens + variant_opens) / (control_sent + variant_sent)

    # Standard error
    se = (pooled * (1 - pooled) * (1/control_sent + 1/variant_sent)) ** 0.5

    # Z-score
    z = (variant_rate - control_rate) / se

    # P-value
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))

    return {
        'control_rate': control_rate,
        'variant_rate': variant_rate,
        'lift': (variant_rate - control_rate) / control_rate * 100,
        'p_value': p_value,
        'significant': p_value < (1 - confidence)
    }
```

## Best Practices

### Subject Lines
- Under 50 characters
- Create curiosity or urgency
- Personalize when appropriate
- A/B test consistently
- Avoid spam trigger words

### Email Copy
- Clear value proposition
- Single primary CTA
- Mobile-optimized layout
- Scannable format with headers
- Personalization tokens
- Alt text for images

### Deliverability
- Clean lists regularly (remove bounces, unengaged)
- Authenticate domains (SPF, DKIM, DMARC)
- Maintain consistent sending volume
- Monitor sender reputation
- Use double opt-in
- Honor unsubscribes immediately

### Send Time Optimization

```python
def optimize_send_time(subscriber_data):
    """Analyze historical engagement to find optimal send times."""

    engagement_by_hour = {}

    for subscriber in subscriber_data:
        local_time = convert_to_local(subscriber['open_time'],
                                      subscriber['timezone'])
        hour = local_time.hour

        if hour not in engagement_by_hour:
            engagement_by_hour[hour] = {'opens': 0, 'total': 0}

        engagement_by_hour[hour]['opens'] += 1
        engagement_by_hour[hour]['total'] += 1

    # Calculate open rates by hour
    for hour, data in engagement_by_hour.items():
        data['rate'] = data['opens'] / data['total']

    # Find best hours
    sorted_hours = sorted(engagement_by_hour.items(),
                         key=lambda x: x[1]['rate'],
                         reverse=True)

    return sorted_hours[:3]  # Top 3 hours
```

## List Hygiene

### Engagement Scoring

```sql
-- Calculate subscriber engagement score
SELECT
    subscriber_id,
    email,
    COUNT(CASE WHEN event_type = 'open' THEN 1 END) as opens_30d,
    COUNT(CASE WHEN event_type = 'click' THEN 1 END) as clicks_30d,
    MAX(event_date) as last_activity,
    CASE
        WHEN COUNT(CASE WHEN event_type = 'open' THEN 1 END) >= 5 THEN 'highly_engaged'
        WHEN COUNT(CASE WHEN event_type = 'open' THEN 1 END) >= 2 THEN 'engaged'
        WHEN COUNT(CASE WHEN event_type = 'open' THEN 1 END) >= 1 THEN 'somewhat_engaged'
        ELSE 'unengaged'
    END as engagement_tier
FROM email_events
WHERE event_date >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY subscriber_id, email;
```

### Sunset Policy

```yaml
Re-engagement Campaign:
  trigger: no_opens_60_days
  sequence:
    - Day 0: "We miss you" email
    - Day 7: "Last chance" with offer
    - Day 14: Final warning

  action_after_sequence:
    if: no_engagement
    then: move_to_suppression_list
```

## Tools Proficiency

### ESP Platforms
- **SMB:** Klaviyo, Mailchimp, ConvertKit
- **Mid-Market:** HubSpot, ActiveCampaign, Drip
- **Enterprise:** Salesforce Marketing Cloud, Marketo, Braze

### Transactional
- SendGrid, Postmark, Amazon SES, Mailgun

### Testing & Preview
- Litmus, Email on Acid

### Analytics
- Google Analytics (UTM tracking)
- Native ESP analytics
- Custom data warehouse

## Лучшие практики

1. **Permission-based** — только подтверждённые подписчики
2. **Segmentation** — релевантный контент для сегментов
3. **Testing** — постоянное A/B тестирование
4. **Automation** — автоматизируйте lifecycle emails
5. **Deliverability** — мониторинг репутации отправителя
6. **Mobile-first** — 60%+ открытий на мобильных
