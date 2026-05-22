---
name: lead-scoring-system
description: Generic lead scoring framework for any business. Use when implementing lead qualification, tracking engagement, or building conversion funnels. Framework for project-specific implementations.
---

# Lead Scoring System Framework

Generic patterns for implementing lead scoring across any business model.

## When to Use

- Building lead qualification system
- Tracking prospect engagement
- Prioritizing sales follow-ups
- Measuring conversion funnel effectiveness
- Automating lead routing

## NOT Project-Specific

This is a **framework skill** providing generic patterns. For project-specific implementations:
- Create implementation skill in your project
- Reference this framework with `extends: "lead-generation-framework/lead-scoring-system"`
- Define your funnel stages and scoring via skill.config.json

## Core Concepts

### Lead Scoring Model (1-100 Scale)

```
 0-20   | Cold Lead      | Initial awareness, minimal engagement
21-40   | Warm Lead      | Active research, content consumption
41-60   | Hot Lead       | Intent signals, direct inquiries
61-80   | Very Hot Lead  | Detailed engagement, pricing questions
81-100  | Conversion     | Ready to buy, transaction initiated
```

### Scoring Philosophy

**Progressive Scoring:** Each action increases score incrementally
```
Page View (+5) → Content Download (+15) → Form Started (+40)
→ Contact Info Submitted (+60) → Direct Contact (+85) → Purchase (+100)
```

**Decay Model:** Scores decrease over time without engagement
```typescript
function applyDecay(score: number, daysSinceLastActivity: number): number {
  const decayRate = 0.02; // 2% per day
  const decayFactor = Math.pow(1 - decayRate, daysSinceLastActivity);
  return Math.floor(score * decayFactor);
}
```

## Implementation Patterns

### 1. Define Funnel Stages

```typescript
// Generic funnel stages - customize per project
export const FUNNEL_STAGES = {
  // Awareness (0-20)
  AWARENESS: {
    PAGE_VIEW: { score: 5, event: 'page_view' },
    ORGANIC_SEARCH: { score: 10, event: 'organic_arrival' },
    SOCIAL_MEDIA: { score: 8, event: 'social_arrival' }
  },

  // Interest (21-40)
  INTEREST: {
    CONTENT_VIEW: { score: 15, event: 'content_viewed' },
    VIDEO_WATCH: { score: 20, event: 'video_watched' },
    RESOURCE_DOWNLOAD: { score: 25, event: 'resource_downloaded' }
  },

  // Consideration (41-60)
  CONSIDERATION: {
    INQUIRY_STARTED: { score: 40, event: 'inquiry_started' },
    FORM_PROGRESS: { score: 50, event: 'form_progressed' },
    CONTACT_INFO: { score: 60, event: 'contact_info_submitted' }
  },

  // Intent (61-80)
  INTENT: {
    PRICING_VIEW: { score: 65, event: 'pricing_viewed' },
    DEMO_REQUEST: { score: 70, event: 'demo_requested' },
    DIRECT_CONTACT: { score: 85, event: 'direct_contact_initiated' }
  },

  // Conversion (81-100)
  CONVERSION: {
    QUOTE_REQUEST: { score: 90, event: 'quote_requested' },
    PURCHASE_INTENT: { score: 95, event: 'purchase_intent' },
    TRANSACTION: { score: 100, event: 'transaction_completed' }
  }
};
```

### 2. Lead Scoring Service

```typescript
import { createClient } from '@supabase/supabase-js';

interface Lead {
  id: string;
  email: string;
  score: number;
  stage: string;
  last_activity: Date;
  source: string;
}

interface ScoringEvent {
  event_name: string;
  score_delta: number;
  timestamp: Date;
  metadata?: Record<string, any>;
}

export class LeadScoringService {
  constructor(
    private supabase: ReturnType<typeof createClient>
  ) {}

  async trackEvent(leadId: string, event: ScoringEvent): Promise<Lead> {
    // 1. Get current lead
    const { data: lead } = await this.supabase
      .from('leads')
      .select('*')
      .eq('id', leadId)
      .single();

    if (!lead) {
      throw new Error(`Lead ${leadId} not found`);
    }

    // 2. Calculate new score
    const newScore = Math.min(100, lead.score + event.score_delta);
    const newStage = this.determineStage(newScore);

    // 3. Update lead
    const { data: updatedLead } = await this.supabase
      .from('leads')
      .update({
        score: newScore,
        stage: newStage,
        last_activity: event.timestamp
      })
      .eq('id', leadId)
      .select()
      .single();

    // 4. Log scoring event
    await this.supabase.from('lead_scoring_events').insert({
      lead_id: leadId,
      event_name: event.event_name,
      score_delta: event.score_delta,
      score_before: lead.score,
      score_after: newScore,
      timestamp: event.timestamp,
      metadata: event.metadata
    });

    // 5. Trigger stage-specific actions
    if (newStage !== lead.stage) {
      await this.handleStageChange(updatedLead, lead.stage, newStage);
    }

    return updatedLead;
  }

  private determineStage(score: number): string {
    if (score <= 20) return 'cold';
    if (score <= 40) return 'warm';
    if (score <= 60) return 'hot';
    if (score <= 80) return 'very_hot';
    return 'conversion';
  }

  private async handleStageChange(
    lead: Lead,
    oldStage: string,
    newStage: string
  ): Promise<void> {
    // Project-specific: Send notifications, trigger automations, etc.
    console.log(`Lead ${lead.id} moved from ${oldStage} to ${newStage}`);

    // Example: Hot lead notification
    if (newStage === 'hot' && oldStage === 'warm') {
      await this.notifySalesTeam(lead);
    }
  }

  private async notifySalesTeam(lead: Lead): Promise<void> {
    // Project-specific notification logic
  }
}
```

### 3. Client-Side Tracking

```typescript
// Track page views
export function trackPageView(page: string): void {
  trackLeadEvent('page_view', {
    score_delta: 5,
    metadata: { page }
  });
}

// Track content engagement
export function trackContentView(contentId: string, timeSpent: number): void {
  const scoreDelta = timeSpent > 30 ? 20 : 15; // Bonus for >30s
  trackLeadEvent('content_viewed', {
    score_delta: scoreDelta,
    metadata: { contentId, timeSpent }
  });
}

// Track form progress
export function trackFormProgress(formId: string, completionPercent: number): void {
  const scoreDelta = Math.floor(40 + (completionPercent * 0.2)); // 40-60 range
  trackLeadEvent('form_progressed', {
    score_delta: scoreDelta,
    metadata: { formId, completionPercent }
  });
}

// Generic event tracker
async function trackLeadEvent(
  eventName: string,
  data: { score_delta: number; metadata?: any }
): Promise<void> {
  await fetch('/api/leads/track', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      event_name: eventName,
      score_delta: data.score_delta,
      timestamp: new Date().toISOString(),
      metadata: data.metadata
    })
  });
}
```

### 4. Database Schema

```sql
-- Leads table
CREATE TABLE leads (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT UNIQUE NOT NULL,
  score INTEGER DEFAULT 0 CHECK (score >= 0 AND score <= 100),
  stage TEXT DEFAULT 'cold',
  source TEXT,
  first_seen TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  last_activity TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Scoring events log
CREATE TABLE lead_scoring_events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  lead_id UUID REFERENCES leads(id) ON DELETE CASCADE,
  event_name TEXT NOT NULL,
  score_delta INTEGER NOT NULL,
  score_before INTEGER NOT NULL,
  score_after INTEGER NOT NULL,
  timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
  metadata JSONB,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_leads_score ON leads(score DESC);
CREATE INDEX idx_leads_stage ON leads(stage);
CREATE INDEX idx_leads_last_activity ON leads(last_activity DESC);
CREATE INDEX idx_scoring_events_lead ON lead_scoring_events(lead_id, timestamp DESC);

-- RLS Policies
ALTER TABLE leads ENABLE ROW LEVEL SECURITY;
ALTER TABLE lead_scoring_events ENABLE ROW LEVEL SECURITY;

-- Allow authenticated users to read/update leads
CREATE POLICY "Users can manage leads" ON leads
  FOR ALL USING (auth.role() = 'authenticated');

CREATE POLICY "Users can view scoring events" ON lead_scoring_events
  FOR SELECT USING (auth.role() = 'authenticated');
```

## Lead Routing Patterns

### Automatic Assignment Based on Score

```typescript
async function autoAssignLead(lead: Lead): Promise<void> {
  let assignee: string;

  if (lead.score >= 80) {
    // Very hot leads → Senior sales rep
    assignee = await getSeniorSalesRep();
  } else if (lead.score >= 60) {
    // Hot leads → Sales team (round robin)
    assignee = await getNextSalesRep();
  } else if (lead.score >= 40) {
    // Warm leads → Marketing automation
    await addToNurtureSequence(lead);
    return;
  } else {
    // Cold leads → No immediate action
    return;
  }

  await assignLeadToRep(lead.id, assignee);
  await notifyAssignee(assignee, lead);
}
```

### Prioritization Queue

```typescript
interface LeadQueue {
  urgent: Lead[];      // Score 80-100, <24h old
  high: Lead[];        // Score 60-79, <48h old
  medium: Lead[];      // Score 40-59, <7d old
  low: Lead[];         // Score 20-39, any age
}

async function getLeadQueue(): Promise<LeadQueue> {
  const now = new Date();
  const leads = await supabase
    .from('leads')
    .select('*')
    .gte('score', 20)
    .order('score', { ascending: false });

  return {
    urgent: leads.filter(l =>
      l.score >= 80 && daysSince(l.last_activity) < 1
    ),
    high: leads.filter(l =>
      l.score >= 60 && l.score < 80 && daysSince(l.last_activity) < 2
    ),
    medium: leads.filter(l =>
      l.score >= 40 && l.score < 60 && daysSince(l.last_activity) < 7
    ),
    low: leads.filter(l =>
      l.score >= 20 && l.score < 40
    )
  };
}
```

## Analytics & Reporting

### Funnel Conversion Analysis

```typescript
async function analyzeFunnelConversion(startDate: Date, endDate: Date) {
  const conversions = await supabase
    .from('lead_scoring_events')
    .select('lead_id, event_name, score_after, timestamp')
    .gte('timestamp', startDate.toISOString())
    .lte('timestamp', endDate.toISOString());

  // Group by stage
  const stages = {
    cold_to_warm: 0,      // 0-20 → 21-40
    warm_to_hot: 0,       // 21-40 → 41-60
    hot_to_very_hot: 0,   // 41-60 → 61-80
    very_hot_to_conv: 0   // 61-80 → 81-100
  };

  // Calculate conversion rates
  // ... implementation

  return {
    stages,
    overallConversionRate: stages.very_hot_to_conv / stages.cold_to_warm,
    avgTimeToConvert: calculateAvgTime(conversions)
  };
}
```

### Lead Source Performance

```typescript
async function analyzeLeadSourceROI() {
  const leadsBySource = await supabase
    .from('leads')
    .select('source, score, created_at');

  const sourceMetrics = {};

  leadsBySource.forEach(lead => {
    if (!sourceMetrics[lead.source]) {
      sourceMetrics[lead.source] = {
        count: 0,
        avgScore: 0,
        conversions: 0
      };
    }

    sourceMetrics[lead.source].count++;
    sourceMetrics[lead.source].avgScore += lead.score;
    if (lead.score >= 100) {
      sourceMetrics[lead.source].conversions++;
    }
  });

  // Calculate averages and conversion rates
  Object.keys(sourceMetrics).forEach(source => {
    const metrics = sourceMetrics[source];
    metrics.avgScore = metrics.avgScore / metrics.count;
    metrics.conversionRate = (metrics.conversions / metrics.count) * 100;
  });

  return sourceMetrics;
}
```

## Configuration Requirements

**Environment Variables:**
- `SUPABASE_URL` - Supabase project URL
- `SUPABASE_ANON_KEY` - Supabase anonymous key
- `NOTIFICATION_WEBHOOK_URL` - (Optional) Slack/email webhook

**Database:**
- `leads` table with scoring fields
- `lead_scoring_events` table for audit trail
- RLS policies for security

**Scoring Configuration** (skill.config.json):
```json
{
  "configuration": {
    "funnel_stages": {
      "awareness": { "min": 0, "max": 20 },
      "interest": { "min": 21, "max": 40 },
      "consideration": { "min": 41, "max": 60 },
      "intent": { "min": 61, "max": 80 },
      "conversion": { "min": 81, "max": 100 }
    },
    "scoring_events": {
      "page_view": 5,
      "content_view": 15,
      "inquiry_started": 40,
      "contact_info": 60,
      "direct_contact": 85,
      "transaction": 100
    }
  }
}
```

## Key Rules

### DO:
- Start with simple scoring model (adjust based on data)
- Track every scoring event for analysis
- Implement score decay for stale leads
- Set clear thresholds for sales handoff
- Monitor conversion rates by source
- A/B test score values

### DON'T:
- Make scoring too complex initially
- Ignore score decay (leads go stale)
- Assign low-score leads to sales (waste time)
- Use same scoring for different products/markets
- Forget to validate assumptions with data
- Skip audit trail (need to debug scoring)

## Testing Scoring Model

```typescript
// Test scoring progression
describe('Lead Scoring', () => {
  it('should progress through funnel correctly', async () => {
    const lead = await createTestLead();

    // Page view → cold (5)
    await trackEvent(lead.id, 'page_view', 5);
    expect(lead.score).toBe(5);
    expect(lead.stage).toBe('cold');

    // Content view → warm (20)
    await trackEvent(lead.id, 'content_view', 15);
    expect(lead.score).toBe(20);
    expect(lead.stage).toBe('warm');

    // Inquiry started → hot (60)
    await trackEvent(lead.id, 'inquiry_started', 40);
    expect(lead.score).toBe(60);
    expect(lead.stage).toBe('hot');

    // Direct contact → very hot (85)
    await trackEvent(lead.id, 'direct_contact', 25);
    expect(lead.score).toBe(85);
    expect(lead.stage).toBe('very_hot');

    // Transaction → conversion (100)
    await trackEvent(lead.id, 'transaction', 15);
    expect(lead.score).toBe(100);
    expect(lead.stage).toBe('conversion');
  });
});
```

## Resources

- **Supabase Docs**: https://supabase.com/docs
- **Lead Scoring Best Practices**: HubSpot, Salesforce guides
- **Analytics**: PostHog, Mixpanel for event tracking

## Example Implementations

See project-specific skills that extend this framework:
- `myarmy-skills/lead-scoring-myarmy` - Swiss military lead funnel
- Your implementation here!
