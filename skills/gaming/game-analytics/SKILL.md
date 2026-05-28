---
name: Game Analytics
description: Tracking player behavior and game performance through metrics, event tracking, funnel analysis, retention metrics, and integration with analytics platforms for data-driven game development.
---

# Game Analytics

> **Current Level:** Intermediate  
> **Domain:** Gaming / Analytics

---

## Overview

Game analytics tracks player behavior and game performance. This guide covers metrics, event tracking, funnel analysis, and analytics platforms for understanding player engagement, optimizing gameplay, and improving retention.

## Game Metrics

### Core Metrics

```typescript
// Key Performance Indicators (KPIs)
interface GameMetrics {
  // User metrics
  dau: number; // Daily Active Users
  mau: number; // Monthly Active Users
  wau: number; // Weekly Active Users
  
  // Engagement metrics
  avgSessionLength: number; // Minutes
  sessionsPerUser: number;
  daysSinceInstall: number;
  
  // Retention metrics
  day1Retention: number; // %
  day7Retention: number;
  day30Retention: number;
  
  // Monetization metrics
  arpu: number; // Average Revenue Per User
  arppu: number; // Average Revenue Per Paying User
  conversionRate: number; // % of users who pay
  ltv: number; // Lifetime Value
  
  // Gameplay metrics
  levelsCompleted: number;
  avgPlayTime: number;
  completionRate: number;
}
```

## Event Tracking

```typescript
// services/analytics.service.ts
export class AnalyticsService {
  async trackEvent(
    playerId: string,
    eventName: string,
    properties?: Record<string, any>
  ): Promise<void> {
    await db.analyticsEvent.create({
      data: {
        playerId,
        eventName,
        properties,
        timestamp: new Date()
      }
    });

    // Also send to analytics platform
    await this.sendToAnalyticsPlatform(playerId, eventName, properties);
  }

  async trackSessionStart(playerId: string): Promise<string> {
    const session = await db.session.create({
      data: {
        playerId,
        startTime: new Date()
      }
    });

    await this.trackEvent(playerId, 'session_start', {
      sessionId: session.id
    });

    return session.id;
  }

  async trackSessionEnd(sessionId: string): Promise<void> {
    const session = await db.session.update({
      where: { id: sessionId },
      data: {
        endTime: new Date()
      }
    });

    const duration = session.endTime!.getTime() - session.startTime.getTime();

    await this.trackEvent(session.playerId, 'session_end', {
      sessionId,
      duration: duration / 1000 // seconds
    });
  }

  async trackLevelStart(playerId: string, levelId: string): Promise<void> {
    await this.trackEvent(playerId, 'level_start', {
      levelId,
      timestamp: Date.now()
    });
  }

  async trackLevelComplete(
    playerId: string,
    levelId: string,
    score: number,
    duration: number
  ): Promise<void> {
    await this.trackEvent(playerId, 'level_complete', {
      levelId,
      score,
      duration,
      timestamp: Date.now()
    });
  }

  async trackPurchase(
    playerId: string,
    itemId: string,
    price: number,
    currency: string
  ): Promise<void> {
    await this.trackEvent(playerId, 'purchase', {
      itemId,
      price,
      currency,
      timestamp: Date.now()
    });
  }

  private async sendToAnalyticsPlatform(
    playerId: string,
    eventName: string,
    properties?: Record<string, any>
  ): Promise<void> {
    // Send to Unity Analytics, GameAnalytics, etc.
  }
}
```

## Funnel Analysis

```typescript
// services/funnel-analysis.service.ts
export class FunnelAnalysisService {
  async analyzeTutorialFunnel(): Promise<FunnelStep[]> {
    const steps = [
      'tutorial_start',
      'tutorial_step1',
      'tutorial_step2',
      'tutorial_step3',
      'tutorial_complete'
    ];

    const funnel: FunnelStep[] = [];

    for (let i = 0; i < steps.length; i++) {
      const step = steps[i];
      
      const count = await db.analyticsEvent.count({
        where: { eventName: step }
      });

      const dropoff = i > 0
        ? ((funnel[i - 1].count - count) / funnel[i - 1].count) * 100
        : 0;

      funnel.push({
        step,
        count,
        dropoffRate: dropoff
      });
    }

    return funnel;
  }

  async analyzeConversionFunnel(): Promise<FunnelStep[]> {
    const steps = [
      'app_install',
      'first_session',
      'tutorial_complete',
      'level_1_complete',
      'first_purchase'
    ];

    const funnel: FunnelStep[] = [];

    for (let i = 0; i < steps.length; i++) {
      const step = steps[i];
      
      const uniquePlayers = await db.analyticsEvent.groupBy({
        by: ['playerId'],
        where: { eventName: step },
        _count: true
      });

      const count = uniquePlayers.length;

      const dropoff = i > 0
        ? ((funnel[i - 1].count - count) / funnel[i - 1].count) * 100
        : 0;

      funnel.push({
        step,
        count,
        dropoffRate: dropoff
      });
    }

    return funnel;
  }
}

interface FunnelStep {
  step: string;
  count: number;
  dropoffRate: number;
}
```

## Cohort Analysis

```typescript
// services/cohort-analysis.service.ts
export class CohortAnalysisService {
  async analyzeRetention(cohortDate: Date): Promise<CohortRetention> {
    // Get users who installed on cohortDate
    const cohortUsers = await db.player.findMany({
      where: {
        createdAt: {
          gte: cohortDate,
          lt: new Date(cohortDate.getTime() + 24 * 60 * 60 * 1000)
        }
      }
    });

    const cohortSize = cohortUsers.length;
    const userIds = cohortUsers.map(u => u.id);

    // Calculate retention for each day
    const retention: number[] = [];

    for (let day = 0; day < 30; day++) {
      const targetDate = new Date(cohortDate.getTime() + day * 24 * 60 * 60 * 1000);
      
      const activeUsers = await db.session.groupBy({
        by: ['playerId'],
        where: {
          playerId: { in: userIds },
          startTime: {
            gte: targetDate,
            lt: new Date(targetDate.getTime() + 24 * 60 * 60 * 1000)
          }
        }
      });

      const retentionRate = (activeUsers.length / cohortSize) * 100;
      retention.push(retentionRate);
    }

    return {
      cohortDate,
      cohortSize,
      retention
    };
  }

  async analyzeRevenueByInstallDate(): Promise<CohortRevenue[]> {
    const cohorts: CohortRevenue[] = [];

    // Last 30 days
    for (let i = 0; i < 30; i++) {
      const cohortDate = new Date(Date.now() - i * 24 * 60 * 60 * 1000);

      const users = await db.player.findMany({
        where: {
          createdAt: {
            gte: cohortDate,
            lt: new Date(cohortDate.getTime() + 24 * 60 * 60 * 1000)
          }
        }
      });

      const userIds = users.map(u => u.id);

      const revenue = await db.transaction.aggregate({
        where: {
          playerId: { in: userIds },
          status: 'completed'
        },
        _sum: { priceUsd: true }
      });

      cohorts.push({
        cohortDate,
        cohortSize: users.length,
        totalRevenue: revenue._sum.priceUsd || 0,
        arpu: (revenue._sum.priceUsd || 0) / users.length
      });
    }

    return cohorts;
  }
}

interface CohortRetention {
  cohortDate: Date;
  cohortSize: number;
  retention: number[]; // Retention % for each day
}

interface CohortRevenue {
  cohortDate: Date;
  cohortSize: number;
  totalRevenue: number;
  arpu: number;
}
```

## A/B Testing

```typescript
// services/ab-testing.service.ts
export class ABTestingService {
  async assignVariant(playerId: string, experimentId: string): Promise<string> {
    // Check if already assigned
    const existing = await db.experimentAssignment.findUnique({
      where: {
        playerId_experimentId: { playerId, experimentId }
      }
    });

    if (existing) {
      return existing.variant;
    }

    // Assign variant (50/50 split)
    const variant = Math.random() < 0.5 ? 'A' : 'B';

    await db.experimentAssignment.create({
      data: {
        playerId,
        experimentId,
        variant
      }
    });

    await this.trackEvent(playerId, 'experiment_assigned', {
      experimentId,
      variant
    });

    return variant;
  }

  async trackConversion(
    playerId: string,
    experimentId: string,
    metric: string,
    value: number
  ): Promise<void> {
    await db.experimentMetric.create({
      data: {
        playerId,
        experimentId,
        metric,
        value
      }
    });
  }

  async getExperimentResults(experimentId: string): Promise<ExperimentResults> {
    const assignments = await db.experimentAssignment.groupBy({
      by: ['variant'],
      where: { experimentId },
      _count: true
    });

    const metrics = await db.experimentMetric.groupBy({
      by: ['variant', 'metric'],
      where: { experimentId },
      _avg: { value: true },
      _count: true
    });

    return {
      experimentId,
      variants: assignments.map(a => ({
        variant: a.variant,
        users: a._count
      })),
      metrics: metrics.map(m => ({
        variant: m.variant,
        metric: m.metric,
        average: m._avg.value || 0,
        count: m._count
      }))
    };
  }
}

interface ExperimentResults {
  experimentId: string;
  variants: Array<{ variant: string; users: number }>;
  metrics: Array<{
    variant: string;
    metric: string;
    average: number;
    count: number;
  }>;
}
```

## Player Segmentation

```typescript
// services/player-segmentation.service.ts
export class PlayerSegmentationService {
  async segmentPlayers(): Promise<Map<string, string[]>> {
    const segments = new Map<string, string[]>();

    // Whales (high spenders)
    const whales = await db.player.findMany({
      where: {
        totalSpent: { gte: 100 }
      },
      select: { id: true }
    });
    segments.set('whales', whales.map(p => p.id));

    // Engaged players (high playtime)
    const engaged = await db.player.findMany({
      where: {
        totalPlayTime: { gte: 3600 } // 1 hour
      },
      select: { id: true }
    });
    segments.set('engaged', engaged.map(p => p.id));

    // At-risk (haven't played in 7 days)
    const atRisk = await db.player.findMany({
      where: {
        lastSeen: {
          lt: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000)
        }
      },
      select: { id: true }
    });
    segments.set('at_risk', atRisk.map(p => p.id));

    // New players (< 7 days)
    const newPlayers = await db.player.findMany({
      where: {
        createdAt: {
          gte: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000)
        }
      },
      select: { id: true }
    });
    segments.set('new', newPlayers.map(p => p.id));

    return segments;
  }

  async getSegmentMetrics(segment: string): Promise<SegmentMetrics> {
    const playerIds = (await this.segmentPlayers()).get(segment) || [];

    const sessions = await db.session.aggregate({
      where: { playerId: { in: playerIds } },
      _avg: { duration: true },
      _count: true
    });

    const revenue = await db.transaction.aggregate({
      where: {
        playerId: { in: playerIds },
        status: 'completed'
      },
      _sum: { priceUsd: true }
    });

    return {
      segment,
      playerCount: playerIds.length,
      avgSessionLength: sessions._avg.duration || 0,
      totalSessions: sessions._count,
      totalRevenue: revenue._sum.priceUsd || 0,
      arpu: (revenue._sum.priceUsd || 0) / playerIds.length
    };
  }
}

interface SegmentMetrics {
  segment: string;
  playerCount: number;
  avgSessionLength: number;
  totalSessions: number;
  totalRevenue: number;
  arpu: number;
}
```

## Real-time Dashboard

```typescript
// components/AnalyticsDashboard.tsx
export function AnalyticsDashboard() {
  const [metrics, setMetrics] = useState<GameMetrics | null>(null);

  useEffect(() => {
    loadMetrics();
    
    // Refresh every minute
    const interval = setInterval(loadMetrics, 60000);
    
    return () => clearInterval(interval);
  }, []);

  const loadMetrics = async () => {
    const data = await fetch('/api/analytics/metrics').then(r => r.json());
    setMetrics(data);
  };

  return (
    <div className="analytics-dashboard">
      <div className="metrics-grid">
        <MetricCard title="DAU" value={metrics?.dau || 0} />
        <MetricCard title="MAU" value={metrics?.mau || 0} />
        <MetricCard title="ARPU" value={`$${metrics?.arpu.toFixed(2) || 0}`} />
        <MetricCard title="Day 1 Retention" value={`${metrics?.day1Retention || 0}%`} />
      </div>

      <div className="charts">
        <RetentionChart />
        <RevenueChart />
        <FunnelChart />
      </div>
    </div>
  );
}
```

## Best Practices

1. **Privacy** - Respect user privacy (GDPR, CCPA)
2. **Sampling** - Use sampling for high-volume events
3. **Real-time** - Track critical events in real-time
4. **Retention** - Set data retention policies
5. **Segmentation** - Segment players for insights
6. **A/B Testing** - Test features before full rollout
7. **Funnels** - Identify drop-off points
8. **Cohorts** - Analyze by install date
9. **Dashboards** - Create actionable dashboards
10. **Alerts** - Set up alerts for anomalies

---

## Quick Start

### Event Tracking

```typescript
// Track game events
function trackEvent(event: GameEvent) {
  analytics.track(event.name, {
    userId: event.userId,
    sessionId: event.sessionId,
    timestamp: Date.now(),
    ...event.properties
  })
}

// Track player actions
trackEvent({
  name: 'level_complete',
  userId: 'player-123',
  sessionId: 'session-456',
  properties: {
    level: 5,
    score: 10000,
    time: 120  // seconds
  }
})
```

### Key Metrics

```typescript
interface GameMetrics {
  dau: number  // Daily Active Users
  mau: number  // Monthly Active Users
  retention: {
    day1: number
    day7: number
    day30: number
  }
  arpu: number  // Average Revenue Per User
  ltv: number   // Lifetime Value
}
```

---

## Production Checklist

- [ ] **Event Tracking**: Track all game events
- [ ] **Key Metrics**: Define key metrics (DAU, retention, etc.)
- [ ] **Funnel Analysis**: Player funnel analysis
- [ ] **Cohort Analysis**: Cohort retention
- [ ] **Segmentation**: Segment players
- [ ] **A/B Testing**: Test features
- [ ] **Dashboards**: Analytics dashboards
- [ ] **Alerts**: Alerts for anomalies
- [ ] **Privacy**: Respect user privacy
- [ ] **Sampling**: Use sampling for high volume
- [ ] **Documentation**: Document metrics
- [ ] **Action**: Act on insights

---

## Anti-patterns

### ❌ Don't: Track Everything

```typescript
// ❌ Bad - Track every action
trackEvent('mouse_move')
trackEvent('key_press')
trackEvent('button_hover')
// Too much data!
```

```typescript
// ✅ Good - Track key events
trackEvent('level_start')
trackEvent('level_complete')
trackEvent('purchase')
// Focused tracking
```

### ❌ Don't: No Privacy

```typescript
// ❌ Bad - Track personal data
trackEvent('player_action', {
  userId: user.id,
  email: user.email,  // Privacy issue!
  location: user.location
})
```

```typescript
// ✅ Good - Anonymize
trackEvent('player_action', {
  userId: hashUserId(user.id),  // Anonymized
  // No personal data
})
```

---

## Integration Points

- **Achievements** (`38-gaming-features/achievements/`) - Achievement metrics
- **Leaderboards** (`38-gaming-features/leaderboards/`) - Ranking metrics
- **Analytics** (`23-business-analytics/`) - General analytics

---

## Further Reading

- [Game Analytics Best Practices](https://www.gamedeveloper.com/business/game-analytics-best-practices)
- [Player Retention](https://www.appsflyer.com/resources/guides/retention/)

## Resources

- [Unity Analytics](https://unity.com/products/unity-analytics)
- [GameAnalytics](https://gameanalytics.com/)
- [Mixpanel](https://mixpanel.com/)
- [Amplitude](https://amplitude.com/)
- [Game Analytics Best Practices](https://www.gamedeveloper.com/business/game-analytics-best-practices)
