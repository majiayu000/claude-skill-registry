---
name: Sales Pipeline
description: Tracking deals through stages from initial contact to close, including pipeline design, deal progression, forecasting, probability calculation, and sales analytics.
---

# Sales Pipeline

> **Current Level:** Intermediate  
> **Domain:** CRM / Sales

---

## Overview

Sales pipeline management tracks deals through stages from initial contact to close. This guide covers pipeline design, deal progression, forecasting, and analytics for managing sales processes and predicting revenue.

## Pipeline Concepts

```
Pipeline: Prospecting → Qualification → Proposal → Negotiation → Closed Won/Lost

Stage Properties:
- Name
- Probability (0-100%)
- Expected duration
- Required actions
```

## Database Schema

```sql
-- pipelines table
CREATE TABLE pipelines (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  is_default BOOLEAN DEFAULT FALSE,
  active BOOLEAN DEFAULT TRUE,
  
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- stages table
CREATE TABLE stages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  pipeline_id UUID REFERENCES pipelines(id) ON DELETE CASCADE,
  
  name VARCHAR(255) NOT NULL,
  type VARCHAR(50) DEFAULT 'open',
  display_order INTEGER NOT NULL,
  probability INTEGER DEFAULT 0,
  
  expected_duration_days INTEGER,
  required_fields TEXT[],
  
  active BOOLEAN DEFAULT TRUE,
  
  created_at TIMESTAMP DEFAULT NOW(),
  
  INDEX idx_pipeline (pipeline_id),
  INDEX idx_order (display_order)
);

-- deals table
CREATE TABLE deals (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  pipeline_id UUID REFERENCES pipelines(id),
  stage_id UUID REFERENCES stages(id),
  
  name VARCHAR(255) NOT NULL,
  amount DECIMAL(15, 2),
  currency VARCHAR(3) DEFAULT 'USD',
  
  contact_id UUID REFERENCES contacts(id),
  company_id UUID REFERENCES companies(id),
  owner_id UUID REFERENCES users(id),
  
  probability INTEGER DEFAULT 0,
  weighted_amount DECIMAL(15, 2),
  
  expected_close_date DATE,
  actual_close_date DATE,
  
  status VARCHAR(50) DEFAULT 'open',
  won_reason TEXT,
  lost_reason TEXT,
  
  next_step TEXT,
  
  custom_fields JSONB,
  
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  
  INDEX idx_pipeline (pipeline_id),
  INDEX idx_stage (stage_id),
  INDEX idx_owner (owner_id),
  INDEX idx_status (status),
  INDEX idx_close_date (expected_close_date)
);

-- deal_history table
CREATE TABLE deal_history (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  deal_id UUID REFERENCES deals(id) ON DELETE CASCADE,
  user_id UUID REFERENCES users(id),
  
  action VARCHAR(100) NOT NULL,
  from_stage_id UUID REFERENCES stages(id),
  to_stage_id UUID REFERENCES stages(id),
  
  changes JSONB,
  
  created_at TIMESTAMP DEFAULT NOW(),
  
  INDEX idx_deal (deal_id)
);

-- deal_activities table
CREATE TABLE deal_activities (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  deal_id UUID REFERENCES deals(id) ON DELETE CASCADE,
  
  type VARCHAR(50) NOT NULL,
  subject VARCHAR(255),
  description TEXT,
  
  completed BOOLEAN DEFAULT FALSE,
  completed_at TIMESTAMP,
  due_date TIMESTAMP,
  
  created_by UUID REFERENCES users(id),
  
  created_at TIMESTAMP DEFAULT NOW(),
  
  INDEX idx_deal (deal_id),
  INDEX idx_due_date (due_date)
);
```

## Deal Service

```typescript
// services/deal.service.ts
export class DealService {
  async createDeal(data: CreateDealDto): Promise<Deal> {
    // Get default pipeline
    const pipeline = await db.pipeline.findFirst({
      where: { isDefault: true },
      include: { stages: { orderBy: { displayOrder: 'asc' } } }
    });

    if (!pipeline || pipeline.stages.length === 0) {
      throw new Error('No pipeline configured');
    }

    const firstStage = pipeline.stages[0];

    const deal = await db.deal.create({
      data: {
        ...data,
        pipelineId: pipeline.id,
        stageId: firstStage.id,
        probability: firstStage.probability,
        weightedAmount: data.amount * (firstStage.probability / 100),
        status: 'open'
      }
    });

    // Log creation
    await this.logDealHistory(deal.id, 'created', null, firstStage.id);

    return deal;
  }

  async updateDeal(dealId: string, updates: Partial<Deal>): Promise<Deal> {
    const deal = await db.deal.update({
      where: { id: dealId },
      data: {
        ...updates,
        updatedAt: new Date()
      }
    });

    // Recalculate weighted amount if amount or probability changed
    if (updates.amount || updates.probability) {
      await this.updateWeightedAmount(dealId);
    }

    return deal;
  }

  async moveDealToStage(dealId: string, stageId: string, userId: string): Promise<Deal> {
    const [deal, stage] = await Promise.all([
      db.deal.findUnique({ where: { id: dealId } }),
      db.stage.findUnique({ where: { id: stageId } })
    ]);

    if (!deal || !stage) {
      throw new Error('Deal or stage not found');
    }

    // Update deal
    const updated = await db.deal.update({
      where: { id: dealId },
      data: {
        stageId,
        probability: stage.probability,
        weightedAmount: deal.amount * (stage.probability / 100),
        updatedAt: new Date()
      }
    });

    // Log stage change
    await this.logDealHistory(dealId, 'stage_changed', deal.stageId, stageId, userId);

    // Check if deal is won or lost
    if (stage.type === 'won') {
      await this.markDealAsWon(dealId);
    } else if (stage.type === 'lost') {
      await this.markDealAsLost(dealId);
    }

    return updated;
  }

  async markDealAsWon(dealId: string, reason?: string): Promise<Deal> {
    return db.deal.update({
      where: { id: dealId },
      data: {
        status: 'won',
        actualCloseDate: new Date(),
        wonReason: reason,
        probability: 100
      }
    });
  }

  async markDealAsLost(dealId: string, reason?: string): Promise<Deal> {
    return db.deal.update({
      where: { id: dealId },
      data: {
        status: 'lost',
        actualCloseDate: new Date(),
        lostReason: reason,
        probability: 0,
        weightedAmount: 0
      }
    });
  }

  async getDealsByStage(stageId: string): Promise<Deal[]> {
    return db.deal.findMany({
      where: {
        stageId,
        status: 'open'
      },
      include: {
        contact: true,
        company: true,
        owner: true
      },
      orderBy: {
        expectedCloseDate: 'asc'
      }
    });
  }

  async getDealsByOwner(ownerId: string, status: string = 'open'): Promise<Deal[]> {
    return db.deal.findMany({
      where: {
        ownerId,
        status
      },
      include: {
        stage: true,
        contact: true,
        company: true
      },
      orderBy: {
        expectedCloseDate: 'asc'
      }
    });
  }

  private async updateWeightedAmount(dealId: string): Promise<void> {
    const deal = await db.deal.findUnique({ where: { id: dealId } });
    
    if (deal) {
      await db.deal.update({
        where: { id: dealId },
        data: {
          weightedAmount: deal.amount * (deal.probability / 100)
        }
      });
    }
  }

  private async logDealHistory(
    dealId: string,
    action: string,
    fromStageId: string | null,
    toStageId: string,
    userId?: string
  ): Promise<void> {
    await db.dealHistory.create({
      data: {
        dealId,
        action,
        fromStageId,
        toStageId,
        userId
      }
    });
  }
}

interface CreateDealDto {
  name: string;
  amount: number;
  contactId?: string;
  companyId?: string;
  ownerId: string;
  expectedCloseDate?: Date;
}
```

## Pipeline Visualization

```typescript
// services/pipeline-visualization.service.ts
export class PipelineVisualizationService {
  async getPipelineView(pipelineId: string): Promise<PipelineView> {
    const pipeline = await db.pipeline.findUnique({
      where: { id: pipelineId },
      include: {
        stages: {
          orderBy: { displayOrder: 'asc' }
        }
      }
    });

    if (!pipeline) throw new Error('Pipeline not found');

    const stagesWithDeals = await Promise.all(
      pipeline.stages.map(async (stage) => {
        const deals = await db.deal.findMany({
          where: {
            stageId: stage.id,
            status: 'open'
          },
          include: {
            contact: true,
            company: true,
            owner: true
          }
        });

        const totalValue = deals.reduce((sum, deal) => sum + deal.amount, 0);
        const weightedValue = deals.reduce((sum, deal) => sum + deal.weightedAmount, 0);

        return {
          stage,
          deals,
          count: deals.length,
          totalValue,
          weightedValue
        };
      })
    );

    return {
      pipeline,
      stages: stagesWithDeals,
      totalDeals: stagesWithDeals.reduce((sum, s) => sum + s.count, 0),
      totalValue: stagesWithDeals.reduce((sum, s) => sum + s.totalValue, 0),
      totalWeightedValue: stagesWithDeals.reduce((sum, s) => sum + s.weightedValue, 0)
    };
  }
}

interface PipelineView {
  pipeline: Pipeline;
  stages: StageWithDeals[];
  totalDeals: number;
  totalValue: number;
  totalWeightedValue: number;
}

interface StageWithDeals {
  stage: Stage;
  deals: Deal[];
  count: number;
  totalValue: number;
  weightedValue: number;
}
```

## Forecasting

```typescript
// services/sales-forecast.service.ts
export class SalesForecastService {
  async getForecast(period: ForecastPeriod): Promise<Forecast> {
    const deals = await db.deal.findMany({
      where: {
        status: 'open',
        expectedCloseDate: {
          gte: period.start,
          lte: period.end
        }
      },
      include: {
        stage: true,
        owner: true
      }
    });

    // Best case: all deals close
    const bestCase = deals.reduce((sum, deal) => sum + deal.amount, 0);

    // Worst case: only high probability deals close
    const worstCase = deals
      .filter(deal => deal.probability >= 80)
      .reduce((sum, deal) => sum + deal.amount, 0);

    // Most likely: weighted by probability
    const mostLikely = deals.reduce((sum, deal) => sum + deal.weightedAmount, 0);

    // By stage
    const byStage = this.groupByStage(deals);

    // By owner
    const byOwner = this.groupByOwner(deals);

    return {
      period,
      bestCase,
      worstCase,
      mostLikely,
      dealCount: deals.length,
      byStage,
      byOwner
    };
  }

  async getHistoricalWinRate(ownerId?: string): Promise<WinRateStats> {
    const where: any = {
      status: { in: ['won', 'lost'] }
    };

    if (ownerId) {
      where.ownerId = ownerId;
    }

    const deals = await db.deal.findMany({ where });

    const won = deals.filter(d => d.status === 'won').length;
    const lost = deals.filter(d => d.status === 'lost').length;
    const total = won + lost;

    return {
      winRate: total > 0 ? (won / total) * 100 : 0,
      totalDeals: total,
      wonDeals: won,
      lostDeals: lost,
      averageDealSize: this.calculateAverageDealSize(deals.filter(d => d.status === 'won'))
    };
  }

  private groupByStage(deals: Deal[]): Record<string, ForecastByStage> {
    const grouped: Record<string, Deal[]> = {};

    deals.forEach(deal => {
      const stageName = deal.stage.name;
      if (!grouped[stageName]) {
        grouped[stageName] = [];
      }
      grouped[stageName].push(deal);
    });

    return Object.fromEntries(
      Object.entries(grouped).map(([stage, stageDeals]) => [
        stage,
        {
          count: stageDeals.length,
          totalValue: stageDeals.reduce((sum, d) => sum + d.amount, 0),
          weightedValue: stageDeals.reduce((sum, d) => sum + d.weightedAmount, 0)
        }
      ])
    );
  }

  private groupByOwner(deals: Deal[]): Record<string, ForecastByOwner> {
    const grouped: Record<string, Deal[]> = {};

    deals.forEach(deal => {
      const ownerName = deal.owner.name;
      if (!grouped[ownerName]) {
        grouped[ownerName] = [];
      }
      grouped[ownerName].push(deal);
    });

    return Object.fromEntries(
      Object.entries(grouped).map(([owner, ownerDeals]) => [
        owner,
        {
          count: ownerDeals.length,
          totalValue: ownerDeals.reduce((sum, d) => sum + d.amount, 0),
          weightedValue: ownerDeals.reduce((sum, d) => sum + d.weightedAmount, 0)
        }
      ])
    );
  }

  private calculateAverageDealSize(deals: Deal[]): number {
    if (deals.length === 0) return 0;
    return deals.reduce((sum, d) => sum + d.amount, 0) / deals.length;
  }
}

interface ForecastPeriod {
  start: Date;
  end: Date;
}

interface Forecast {
  period: ForecastPeriod;
  bestCase: number;
  worstCase: number;
  mostLikely: number;
  dealCount: number;
  byStage: Record<string, ForecastByStage>;
  byOwner: Record<string, ForecastByOwner>;
}

interface ForecastByStage {
  count: number;
  totalValue: number;
  weightedValue: number;
}

interface ForecastByOwner {
  count: number;
  totalValue: number;
  weightedValue: number;
}

interface WinRateStats {
  winRate: number;
  totalDeals: number;
  wonDeals: number;
  lostDeals: number;
  averageDealSize: number;
}
```

## Pipeline Metrics

```typescript
// services/pipeline-metrics.service.ts
export class PipelineMetricsService {
  async getMetrics(pipelineId: string, period: DateRange): Promise<PipelineMetrics> {
    const deals = await db.deal.findMany({
      where: {
        pipelineId,
        createdAt: {
          gte: period.start,
          lte: period.end
        }
      },
      include: {
        stage: true
      }
    });

    const wonDeals = deals.filter(d => d.status === 'won');
    const lostDeals = deals.filter(d => d.status === 'lost');

    return {
      totalDeals: deals.length,
      openDeals: deals.filter(d => d.status === 'open').length,
      wonDeals: wonDeals.length,
      lostDeals: lostDeals.length,
      
      winRate: this.calculateWinRate(wonDeals.length, lostDeals.length),
      averageDealSize: this.calculateAverageDealSize(wonDeals),
      averageSalesCycle: await this.calculateAverageSalesCycle(wonDeals),
      
      conversionRates: await this.calculateConversionRates(pipelineId),
      
      totalValue: deals.reduce((sum, d) => sum + d.amount, 0),
      wonValue: wonDeals.reduce((sum, d) => sum + d.amount, 0),
      pipelineValue: deals.filter(d => d.status === 'open').reduce((sum, d) => sum + d.amount, 0)
    };
  }

  private calculateWinRate(won: number, lost: number): number {
    const total = won + lost;
    return total > 0 ? (won / total) * 100 : 0;
  }

  private calculateAverageDealSize(deals: Deal[]): number {
    if (deals.length === 0) return 0;
    return deals.reduce((sum, d) => sum + d.amount, 0) / deals.length;
  }

  private async calculateAverageSalesCycle(deals: Deal[]): Promise<number> {
    const cycles = deals
      .filter(d => d.actualCloseDate)
      .map(d => {
        const created = new Date(d.createdAt);
        const closed = new Date(d.actualCloseDate!);
        return (closed.getTime() - created.getTime()) / (1000 * 60 * 60 * 24); // Days
      });

    if (cycles.length === 0) return 0;
    return cycles.reduce((sum, c) => sum + c, 0) / cycles.length;
  }

  private async calculateConversionRates(pipelineId: string): Promise<Record<string, number>> {
    const stages = await db.stage.findMany({
      where: { pipelineId },
      orderBy: { displayOrder: 'asc' }
    });

    const rates: Record<string, number> = {};

    for (let i = 0; i < stages.length - 1; i++) {
      const currentStage = stages[i];
      const nextStage = stages[i + 1];

      const dealsInCurrent = await db.deal.count({
        where: { stageId: currentStage.id }
      });

      const dealsMovedToNext = await db.dealHistory.count({
        where: {
          fromStageId: currentStage.id,
          toStageId: nextStage.id
        }
      });

      rates[`${currentStage.name} → ${nextStage.name}`] = 
        dealsInCurrent > 0 ? (dealsMovedToNext / dealsInCurrent) * 100 : 0;
    }

    return rates;
  }
}

interface PipelineMetrics {
  totalDeals: number;
  openDeals: number;
  wonDeals: number;
  lostDeals: number;
  winRate: number;
  averageDealSize: number;
  averageSalesCycle: number;
  conversionRates: Record<string, number>;
  totalValue: number;
  wonValue: number;
  pipelineValue: number;
}

interface DateRange {
  start: Date;
  end: Date;
}
```

## Best Practices

1. **Pipeline Design** - Create clear, logical stages
2. **Probability** - Assign realistic probabilities to stages
3. **Forecasting** - Use weighted forecasting
4. **Metrics** - Track conversion rates between stages
5. **Activities** - Log all deal-related activities
6. **Win/Loss** - Analyze win/loss reasons
7. **Sales Cycle** - Monitor and optimize sales cycle length
8. **Automation** - Automate stage progression rules
9. **Reporting** - Generate regular pipeline reports
10. **Training** - Train team on pipeline management

---

## Quick Start

### Pipeline Stages

```typescript
const PIPELINE_STAGES = [
  { name: 'Prospecting', probability: 10, duration: 7 },
  { name: 'Qualification', probability: 25, duration: 14 },
  { name: 'Proposal', probability: 50, duration: 7 },
  { name: 'Negotiation', probability: 75, duration: 14 },
  { name: 'Closed Won', probability: 100 },
  { name: 'Closed Lost', probability: 0 }
]

async function moveDealToStage(dealId: string, stageName: string) {
  const stage = PIPELINE_STAGES.find(s => s.name === stageName)
  
  await db.deals.update({
    where: { id: dealId },
    data: {
      stage: stageName,
      probability: stage.probability,
      expectedCloseDate: stage.duration 
        ? addDays(new Date(), stage.duration)
        : undefined
    }
  })
}
```

### Pipeline Forecasting

```typescript
async function forecastRevenue(pipelineId: string): Promise<number> {
  const deals = await db.deals.findMany({
    where: { pipelineId, status: 'open' }
  })
  
  return deals.reduce((sum, deal) => {
    return sum + (deal.value * deal.probability / 100)
  }, 0)
}
```

---

## Production Checklist

- [ ] **Pipeline Design**: Define pipeline stages
- [ ] **Stage Properties**: Probability and duration per stage
- [ ] **Deal Tracking**: Track deals through pipeline
- [ ] **Forecasting**: Revenue forecasting
- [ ] **Analytics**: Pipeline analytics and metrics
- [ ] **Automation**: Automate stage progression
- [ ] **Reporting**: Regular pipeline reports
- [ ] **Integration**: Integrate with CRM
- [ ] **Training**: Train team on pipeline
- [ ] **Documentation**: Document pipeline process
- [ ] **Optimization**: Optimize pipeline stages
- [ ] **Monitoring**: Monitor pipeline health

---

## Anti-patterns

### ❌ Don't: No Probability

```typescript
// ❌ Bad - No probability
const deal = { value: 10000, stage: 'Proposal' }
// Can't forecast!
```

```typescript
// ✅ Good - With probability
const deal = { 
  value: 10000, 
  stage: 'Proposal',
  probability: 50  // 50% chance
}
// Forecast: $5,000
```

### ❌ Don't: Stale Deals

```markdown
# ❌ Bad - Deals stuck in pipeline
Deal 1: In "Proposal" for 6 months
Deal 2: In "Negotiation" for 1 year
```

```markdown
# ✅ Good - Deal hygiene
- Auto-close stale deals
- Regular pipeline reviews
- Deal age tracking
```

---

## Integration Points

- **Lead Management** (`32-crm-integration/lead-management/`) - Lead to deal
- **Salesforce Integration** (`32-crm-integration/salesforce-integration/`) - CRM sync
- **Analytics** (`23-business-analytics/`) - Pipeline analytics

---

## Further Reading

- [Sales Pipeline Management](https://www.salesforce.com/resources/articles/sales-pipeline/)
- [Pipeline Metrics](https://www.hubspot.com/sales/pipeline-metrics)

## Resources
- [Sales Forecasting](https://www.pipedrive.com/en/blog/sales-forecasting)
