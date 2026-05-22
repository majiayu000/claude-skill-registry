---
name: lead-scoring
description: Implement and manage lead scoring systems. Use when working with lead qualification, conversion tracking, or lead funnel optimization. Triggers on "lead", "scoring", "conversion", "funnel", "qualification".
---

# Lead Scoring System

Implement progressive lead scoring based on user engagement and conversion events.

## When to Use

- User mentions "lead", "scoring", "qualification"
- User asks about conversion tracking
- User wants to optimize lead funnel
- User needs to track user engagement
- User mentions WhatsApp or form conversions

## Lead Scoring Scale (1-100)

| Score | Stage | Event |
|-------|-------|-------|
| 5 | Awareness | Page view |
| 15 | Interest | Content view |
| 40 | Consideration | Inquiry started |
| 60 | Intent | Contact info provided |
| 85 | Evaluation | WhatsApp contact |
| 100 | Conversion | Form submitted |

## Event Implementation

```typescript
import { LEAD_GENERATION_EVENTS, LEAD_SCORES } from '@akson/cortex-utilities/events';

// Track page view (Score: 5)
trackEvent(LEAD_GENERATION_EVENTS.LEAD_PAGE_VIEW, {
  page_path: '/badges',
  lead_score: LEAD_SCORES.PAGE_VIEW
});

// Track content engagement (Score: 15)
trackEvent(LEAD_GENERATION_EVENTS.LEAD_CONTENT_VIEW, {
  content_type: 'product',
  lead_score: LEAD_SCORES.CONTENT_VIEW
});

// Track inquiry start (Score: 40)
trackEvent(LEAD_GENERATION_EVENTS.LEAD_INQUIRY_STARTED, {
  form_type: 'quote_request',
  lead_score: LEAD_SCORES.INQUIRY_STARTED
});

// Track contact info (Score: 60)
trackEvent(LEAD_GENERATION_EVENTS.LEAD_CONTACT_INFO, {
  contact_method: 'email',
  lead_score: LEAD_SCORES.CONTACT_INFO
});

// Track WhatsApp contact (Score: 85)
trackEvent(LEAD_GENERATION_EVENTS.LEAD_WHATSAPP_CONTACT, {
  phone_number_provided: true,
  lead_score: LEAD_SCORES.WHATSAPP_CONTACT
});

// Track form submission (Score: 100)
trackEvent(LEAD_GENERATION_EVENTS.LEAD_FORM_SUBMITTED, {
  form_id: 'quote_form',
  lead_score: LEAD_SCORES.FORM_SUBMITTED
});
```

## Lead Database Schema

```sql
CREATE TABLE leads (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  phone_number TEXT,
  first_name TEXT,
  last_name TEXT,
  email TEXT,
  status TEXT DEFAULT 'new',
  score INTEGER DEFAULT 0,
  form_data JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index for quick lookups
CREATE INDEX idx_leads_phone ON leads(phone_number);
CREATE INDEX idx_leads_status ON leads(status);
CREATE INDEX idx_leads_score ON leads(score DESC);
```

## Lead Statuses

| Status | Description |
|--------|-------------|
| new | Just created, not contacted |
| contacted | Initial contact made |
| qualified | Confirmed interest |
| proposal | Quote sent |
| won | Converted to customer |
| lost | Did not convert |

## SLA Tracking

| Lead Score | Response SLA |
|------------|--------------|
| 85-100 | 1 hour |
| 60-84 | 4 hours |
| 40-59 | 24 hours |
| < 40 | 48 hours |

## Query High-Value Leads

```sql
-- Get hot leads (score >= 85)
SELECT id, phone_number, first_name, last_name, email, score, created_at
FROM leads
WHERE score >= 85 AND status = 'new'
ORDER BY score DESC, created_at ASC;

-- Get leads needing follow-up
SELECT id, phone_number, score, status, created_at
FROM leads
WHERE status IN ('new', 'contacted')
AND created_at < NOW() - INTERVAL '24 hours'
ORDER BY score DESC;
```

## Key Rules

### DO:
- Track all lead journey events
- Use standardized event names
- Update lead scores in real-time
- Monitor SLA compliance
- Segment by score for prioritization

### DON'T:
- Skip intermediate events
- Use arbitrary score values
- Ignore low-score leads completely
- Forget to update status after contact

## Analytics Integration

Lead events flow to:
- **PostHog**: User journey analysis
- **GA4**: Conversion funnel visualization
- **Google Ads**: Conversion optimization
- **Slack**: High-value lead alerts
