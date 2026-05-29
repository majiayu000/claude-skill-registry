---
name: sla-tracking
description: Generic SLA (Service Level Agreement) tracking for lead response times. Use when monitoring response performance, ensuring timely follow-ups, or building accountability systems. Framework for project-specific implementations.
---

# SLA Tracking Framework

Generic patterns for tracking and enforcing Service Level Agreements on lead response times.

## When to Use

- Monitoring lead response performance
- Ensuring timely follow-ups
- Building accountability systems
- Analyzing response time impact on conversions
- Automating escalations

## NOT Project-Specific

This is a **framework skill** providing generic patterns. For project-specific implementations:
- Create implementation skill in your project
- Reference this framework with `extends: "lead-generation-framework/sla-tracking"`
- Define your SLA thresholds via skill.config.json

## Core Concepts

### SLA Tiers (Generic Template)

```
URGENT:    <1 hour   | Hot leads (score 80+), high-value inquiries
HIGH:      <4 hours  | Warm leads (score 60-79), direct inquiries
NORMAL:    <24 hours | Medium leads (score 40-59), general questions
LOW:       <48 hours | Cold leads (score 20-39), newsletter signups
```

### SLA States

```typescript
enum SLAStatus {
  PENDING = 'pending',           // Awaiting first response
  IN_PROGRESS = 'in_progress',   // Response sent, conversation ongoing
  MET = 'met',                   // Responded within SLA
  BREACHED = 'breached',         // Exceeded SLA deadline
  ESCALATED = 'escalated'        // Escalated to manager
}
```

## Implementation Patterns

### 1. SLA Configuration

```typescript
export interface SLAConfig {
  tier: string;
  responseTimeMinutes: number;
  escalationTimeMinutes: number;
  assignee?: string;
}

export const SLA_TIERS: Record<string, SLAConfig> = {
  URGENT: {
    tier: 'urgent',
    responseTimeMinutes: 60,      // 1 hour
    escalationTimeMinutes: 90     // Escalate if no response in 1.5h
  },
  HIGH: {
    tier: 'high',
    responseTimeMinutes: 240,     // 4 hours
    escalationTimeMinutes: 300    // Escalate after 5h
  },
  NORMAL: {
    tier: 'normal',
    responseTimeMinutes: 1440,    // 24 hours
    escalationTimeMinutes: 1560   // Escalate after 26h
  },
  LOW: {
    tier: 'low',
    responseTimeMinutes: 2880,    // 48 hours
    escalationTimeMinutes: 3000   // Escalate after 50h
  }
};

// Determine SLA tier based on lead score
export function determineSLATier(leadScore: number): SLAConfig {
  if (leadScore >= 80) return SLA_TIERS.URGENT;
  if (leadScore >= 60) return SLA_TIERS.HIGH;
  if (leadScore >= 40) return SLA_TIERS.NORMAL;
  return SLA_TIERS.LOW;
}
```

### 2. SLA Tracking Service

```typescript
import { createClient } from '@supabase/supabase-js';

interface SLARecord {
  id: string;
  lead_id: string;
  tier: string;
  status: SLAStatus;
  created_at: Date;
  deadline: Date;
  first_response_at?: Date;
  response_time_minutes?: number;
  assignee?: string;
  escalated_at?: Date;
}

export class SLATrackingService {
  constructor(private supabase: ReturnType<typeof createClient>) {}

  async createSLA(leadId: string, leadScore: number): Promise<SLARecord> {
    const tier = determineSLATier(leadScore);
    const createdAt = new Date();
    const deadline = new Date(createdAt.getTime() + tier.responseTimeMinutes * 60000);

    const { data: sla } = await this.supabase
      .from('sla_records')
      .insert({
        lead_id: leadId,
        tier: tier.tier,
        status: 'pending',
        created_at: createdAt,
        deadline: deadline,
        escalation_deadline: new Date(
          createdAt.getTime() + tier.escalationTimeMinutes * 60000
        )
      })
      .select()
      .single();

    // Schedule automatic checks
    await this.scheduleChecks(sla);

    return sla;
  }

  async recordResponse(slaId: string): Promise<SLARecord> {
    const now = new Date();

    const { data: sla } = await this.supabase
      .from('sla_records')
      .select('*')
      .eq('id', slaId)
      .single();

    const responseTime = Math.floor(
      (now.getTime() - new Date(sla.created_at).getTime()) / 60000
    );

    const status = now <= new Date(sla.deadline) ? 'met' : 'breached';

    const { data: updated } = await this.supabase
      .from('sla_records')
      .update({
        first_response_at: now,
        response_time_minutes: responseTime,
        status: status
      })
      .eq('id', slaId)
      .select()
      .single();

    // Log breach if applicable
    if (status === 'breached') {
      await this.logBreach(updated);
    }

    return updated;
  }

  async checkPendingSLAs(): Promise<void> {
    const now = new Date();

    // Find overdue SLAs
    const { data: overdueSLAs } = await this.supabase
      .from('sla_records')
      .select('*')
      .eq('status', 'pending')
      .lt('deadline', now.toISOString());

    for (const sla of overdueSLAs || []) {
      await this.handleBreach(sla);
    }

    // Find SLAs needing escalation
    const { data: escalationSLAs } = await this.supabase
      .from('sla_records')
      .select('*')
      .eq('status', 'pending')
      .lt('escalation_deadline', now.toISOString())
      .is('escalated_at', null);

    for (const sla of escalationSLAs || []) {
      await this.escalate(sla);
    }
  }

  private async handleBreach(sla: SLARecord): Promise<void> {
    // Update status
    await this.supabase
      .from('sla_records')
      .update({ status: 'breached' })
      .eq('id', sla.id);

    // Log breach
    await this.logBreach(sla);

    // Notify team
    await this.notifyBreach(sla);
  }

  private async escalate(sla: SLARecord): Promise<void> {
    const now = new Date();

    await this.supabase
      .from('sla_records')
      .update({
        status: 'escalated',
        escalated_at: now
      })
      .eq('id', sla.id);

    // Notify manager
    await this.notifyEscalation(sla);
  }

  private async logBreach(sla: SLARecord): Promise<void> {
    await this.supabase.from('sla_breaches').insert({
      sla_id: sla.id,
      lead_id: sla.lead_id,
      tier: sla.tier,
      deadline: sla.deadline,
      breached_at: new Date(),
      assignee: sla.assignee
    });
  }

  private async notifyBreach(sla: SLARecord): Promise<void> {
    // Project-specific notification logic
    console.log(`SLA breach: Lead ${sla.lead_id} (${sla.tier})`);
  }

  private async notifyEscalation(sla: SLARecord): Promise<void> {
    // Project-specific escalation logic
    console.log(`SLA escalated: Lead ${sla.lead_id} (${sla.tier})`);
  }

  private async scheduleChecks(sla: SLARecord): Promise<void> {
    // Use cron job or background worker to check SLAs
    // Implementation varies by platform (Vercel Cron, Supabase Edge Functions, etc.)
  }
}
```

### 3. Database Schema

```sql
-- SLA records
CREATE TABLE sla_records (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  lead_id UUID REFERENCES leads(id) ON DELETE CASCADE,
  tier TEXT NOT NULL CHECK (tier IN ('urgent', 'high', 'normal', 'low')),
  status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'in_progress', 'met', 'breached', 'escalated')),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  deadline TIMESTAMP WITH TIME ZONE NOT NULL,
  escalation_deadline TIMESTAMP WITH TIME ZONE NOT NULL,
  first_response_at TIMESTAMP WITH TIME ZONE,
  response_time_minutes INTEGER,
  assignee TEXT,
  escalated_at TIMESTAMP WITH TIME ZONE,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- SLA breaches log
CREATE TABLE sla_breaches (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  sla_id UUID REFERENCES sla_records(id) ON DELETE CASCADE,
  lead_id UUID REFERENCES leads(id) ON DELETE CASCADE,
  tier TEXT NOT NULL,
  deadline TIMESTAMP WITH TIME ZONE NOT NULL,
  breached_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  assignee TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_sla_status ON sla_records(status);
CREATE INDEX idx_sla_deadline ON sla_records(deadline);
CREATE INDEX idx_sla_lead ON sla_records(lead_id);
CREATE INDEX idx_breaches_assignee ON sla_breaches(assignee, breached_at DESC);

-- RLS Policies
ALTER TABLE sla_records ENABLE ROW LEVEL SECURITY;
ALTER TABLE sla_breaches ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Authenticated users can view SLAs" ON sla_records
  FOR SELECT USING (auth.role() = 'authenticated');

CREATE POLICY "Authenticated users can view breaches" ON sla_breaches
  FOR SELECT USING (auth.role() = 'authenticated');
```

### 4. Automated SLA Monitoring (Cron Job)

```typescript
// API Route: /api/cron/check-slas
import { NextRequest, NextResponse } from 'next/server';
import { SLATrackingService } from '@/lib/sla-tracking';
import { createClient } from '@supabase/supabase-js';

export async function GET(req: NextRequest) {
  // Verify cron secret
  const authHeader = req.headers.get('authorization');
  if (authHeader !== `Bearer ${process.env.CRON_SECRET}`) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const supabase = createClient(
    process.env.SUPABASE_URL!,
    process.env.SUPABASE_SERVICE_ROLE_KEY!
  );

  const slaService = new SLATrackingService(supabase);

  try {
    await slaService.checkPendingSLAs();
    return NextResponse.json({ success: true });
  } catch (error) {
    console.error('SLA check failed:', error);
    return NextResponse.json({ error: 'Check failed' }, { status: 500 });
  }
}
```

**Vercel Cron Configuration:**
```json
{
  "crons": [{
    "path": "/api/cron/check-slas",
    "schedule": "*/15 * * * *"
  }]
}
```

## Analytics & Reporting

### SLA Performance Dashboard

```typescript
async function getSLAMetrics(startDate: Date, endDate: Date) {
  const { data: slas } = await supabase
    .from('sla_records')
    .select('*')
    .gte('created_at', startDate.toISOString())
    .lte('created_at', endDate.toISOString());

  const metrics = {
    total: slas.length,
    met: slas.filter(s => s.status === 'met').length,
    breached: slas.filter(s => s.status === 'breached').length,
    escalated: slas.filter(s => s.status === 'escalated').length,
    byTier: {
      urgent: { met: 0, breached: 0, avgResponseTime: 0 },
      high: { met: 0, breached: 0, avgResponseTime: 0 },
      normal: { met: 0, breached: 0, avgResponseTime: 0 },
      low: { met: 0, breached: 0, avgResponseTime: 0 }
    }
  };

  // Calculate tier-specific metrics
  slas.forEach(sla => {
    const tier = metrics.byTier[sla.tier];
    if (sla.status === 'met') tier.met++;
    if (sla.status === 'breached') tier.breached++;
    if (sla.response_time_minutes) {
      tier.avgResponseTime += sla.response_time_minutes;
    }
  });

  // Calculate averages
  Object.keys(metrics.byTier).forEach(tier => {
    const data = metrics.byTier[tier];
    const total = data.met + data.breached;
    if (total > 0) {
      data.avgResponseTime = data.avgResponseTime / total;
      data.complianceRate = (data.met / total) * 100;
    }
  });

  return metrics;
}
```

### Team Performance Analysis

```typescript
async function getTeamPerformance() {
  const { data: slas } = await supabase
    .from('sla_records')
    .select('assignee, status, response_time_minutes, tier')
    .not('assignee', 'is', null);

  const teamMetrics = {};

  slas.forEach(sla => {
    if (!teamMetrics[sla.assignee]) {
      teamMetrics[sla.assignee] = {
        total: 0,
        met: 0,
        breached: 0,
        avgResponseTime: 0,
        complianceRate: 0
      };
    }

    const metrics = teamMetrics[sla.assignee];
    metrics.total++;
    if (sla.status === 'met') metrics.met++;
    if (sla.status === 'breached') metrics.breached++;
    if (sla.response_time_minutes) {
      metrics.avgResponseTime += sla.response_time_minutes;
    }
  });

  // Calculate rates
  Object.keys(teamMetrics).forEach(assignee => {
    const metrics = teamMetrics[assignee];
    metrics.avgResponseTime = metrics.avgResponseTime / metrics.total;
    metrics.complianceRate = (metrics.met / metrics.total) * 100;
  });

  return teamMetrics;
}
```

## Business Hours Adjustment

For SLAs that should only count business hours:

```typescript
function calculateBusinessHours(
  start: Date,
  end: Date,
  businessHours: { start: number; end: number } = { start: 9, end: 17 }
): number {
  let minutes = 0;
  const current = new Date(start);

  while (current < end) {
    const hour = current.getHours();
    const day = current.getDay();

    // Skip weekends
    if (day !== 0 && day !== 6) {
      // Count business hours only
      if (hour >= businessHours.start && hour < businessHours.end) {
        minutes++;
      }
    }

    current.setMinutes(current.getMinutes() + 1);
  }

  return minutes;
}

// Adjust SLA deadlines for business hours
function calculateBusinessHoursDeadline(
  start: Date,
  minutes: number
): Date {
  const deadline = new Date(start);
  let remainingMinutes = minutes;

  while (remainingMinutes > 0) {
    const hour = deadline.getHours();
    const day = deadline.getDay();

    // Skip weekends
    if (day === 0) {
      deadline.setDate(deadline.getDate() + 1);
      deadline.setHours(9, 0, 0, 0);
      continue;
    }

    if (day === 6) {
      deadline.setDate(deadline.getDate() + 2);
      deadline.setHours(9, 0, 0, 0);
      continue;
    }

    // Handle business hours (9am-5pm)
    if (hour < 9) {
      deadline.setHours(9, 0, 0, 0);
    } else if (hour >= 17) {
      deadline.setDate(deadline.getDate() + 1);
      deadline.setHours(9, 0, 0, 0);
    } else {
      deadline.setMinutes(deadline.getMinutes() + 1);
      remainingMinutes--;
    }
  }

  return deadline;
}
```

## Configuration Requirements

**Environment Variables:**
- `SUPABASE_URL` - Supabase project URL
- `SUPABASE_SERVICE_ROLE_KEY` - Service role key (for cron jobs)
- `CRON_SECRET` - Secret for securing cron endpoints
- `NOTIFICATION_WEBHOOK_URL` - (Optional) Slack webhook for alerts

**SLA Configuration** (skill.config.json):
```json
{
  "configuration": {
    "sla_tiers": {
      "urgent": {
        "response_time_minutes": 60,
        "escalation_time_minutes": 90,
        "lead_score_threshold": 80
      },
      "high": {
        "response_time_minutes": 240,
        "escalation_time_minutes": 300,
        "lead_score_threshold": 60
      },
      "normal": {
        "response_time_minutes": 1440,
        "escalation_time_minutes": 1560,
        "lead_score_threshold": 40
      }
    },
    "business_hours": {
      "enabled": true,
      "start_hour": 9,
      "end_hour": 17,
      "exclude_weekends": true
    }
  }
}
```

## Key Rules

### DO:
- Check SLAs frequently (every 15 minutes minimum)
- Log all breaches for accountability
- Escalate high-priority breaches immediately
- Track performance by team member
- Adjust SLA targets based on data
- Consider business hours vs 24/7 support

### DON'T:
- Set unrealistic SLA targets
- Ignore breach patterns (indicates systemic issues)
- Skip escalation process
- Forget to notify assignees of new SLAs
- Mix business hours and calendar hours
- Forget timezone considerations

## Testing

```typescript
describe('SLA Tracking', () => {
  it('should create SLA with correct deadline', () => {
    const leadScore = 85; // Urgent tier
    const sla = await slaService.createSLA('lead-123', leadScore);

    expect(sla.tier).toBe('urgent');
    expect(sla.deadline).toBeWithinMinutes(60);
  });

  it('should mark as breached when overdue', async () => {
    // Create SLA
    const sla = await slaService.createSLA('lead-123', 85);

    // Simulate time passing
    jest.advanceTimersByTime(61 * 60 * 1000); // 61 minutes

    // Check SLAs
    await slaService.checkPendingSLAs();

    // Verify breach
    const updated = await getSLA(sla.id);
    expect(updated.status).toBe('breached');
  });
});
```

## Resources

- **Supabase Cron**: https://supabase.com/docs/guides/functions/schedule-functions
- **Vercel Cron**: https://vercel.com/docs/cron-jobs
- **SLA Best Practices**: Industry standards vary by business type

## Example Implementations

See project-specific skills that extend this framework:
- `myarmy-skills/sla-tracking-myarmy` - Swiss market response times (1h/4h/24h/48h)
- Your implementation here!
