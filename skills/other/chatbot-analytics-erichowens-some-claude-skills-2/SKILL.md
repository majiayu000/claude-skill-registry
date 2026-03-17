---
name: chatbot-analytics
description: Implement AI chatbot analytics and conversation monitoring. Use when adding conversation metrics, tracking AI usage, measuring user engagement with chat, or building conversation dashboards. Activates for AI analytics, token tracking, conversation categorization, and chat performance.
allowed-tools: Read,Write,Edit,Bash(npm:*,npx:*)
category: Data & Analytics
tags:
  - analytics
  - chatbot
  - ai-metrics
---

# AI Chatbot Analytics

This skill helps you implement analytics for the AI coaching chat feature while maintaining HIPAA compliance.

## Core Metrics to Track

Based on [industry best practices](https://hiverhq.com/blog/chatbot-analytics), track these 13 key metrics:

| Metric | Description | HIPAA Safe? |
|--------|-------------|-------------|
| Total Sessions | Number of chat sessions | Yes |
| Avg Messages/Session | Messages per conversation | Yes |
| Avg Session Duration | Time spent in chat | Yes |
| Engagement Rate | % users who use chat | Yes |
| Completion Rate | Sessions ended naturally | Yes |
| Abandonment Rate | Sessions ended early | Yes |
| Response Time | AI response latency | Yes |
| Token Usage | Total/avg tokens consumed | Yes |
| Error Rate | Failed responses | Yes |
| Fallback Rate | "I don't understand" responses | Yes |
| Topic Categories | What users discuss | Metadata only |
| Sentiment Trend | Emotional direction | Derived only |
| Crisis Triggers | Emergency detection | Metadata only |

## HIPAA-Compliant Analytics

### What to Track

```typescript
// Conversation metadata (SAFE)
interface ConversationAnalytics {
  id: string;
  conversationId: string;
  userId: string;  // For aggregation, not individual tracking
  startedAt: Date;
  endedAt: Date | null;
  messageCount: number;
  userMessageCount: number;
  aiMessageCount: number;
  totalTokens: number;
  inputTokens: number;
  outputTokens: number;
  category: string;  // Derived from metadata flags
  outcome: 'completed' | 'abandoned' | 'error' | 'crisis_escalated';
  avgResponseTime: number;
  hadFallback: boolean;
}
```

### What NOT to Track

```typescript
// NEVER store these in analytics
interface PROHIBITED {
  messageContent: string;      // PHI
  userQuery: string;           // PHI
  aiResponse: string;          // PHI
  specificTopics: string[];    // Could reveal health info
  exactSentiment: 'sad';       // Could reveal mental state
}
```

## Implementation Pattern

### Tracking Conversation Start

```typescript
// src/lib/ai/analytics.ts
export async function trackConversationStart(
  conversationId: string,
  userId: string
): Promise<void> {
  await db.insert(conversationAnalytics).values({
    id: generateId(),
    conversationId,
    userId,
    startedAt: new Date(),
    messageCount: 0,
    totalTokens: 0,
    category: 'unknown',
    outcome: 'in_progress'
  });
}
```

### Tracking Message Exchange

```typescript
export async function trackMessageExchange(
  conversationId: string,
  tokens: { input: number; output: number },
  responseTimeMs: number,
  flags: { hadFallback: boolean; hasCrisisIndicator: boolean }
): Promise<void> {
  await db
    .update(conversationAnalytics)
    .set({
      messageCount: sql`message_count + 1`,
      totalTokens: sql`total_tokens + ${tokens.input + tokens.output}`,
      inputTokens: sql`input_tokens + ${tokens.input}`,
      outputTokens: sql`output_tokens + ${tokens.output}`,
      avgResponseTime: sql`(avg_response_time * (message_count - 1) + ${responseTimeMs}) / message_count`,
      hadFallback: flags.hadFallback,
      ...(flags.hasCrisisIndicator && { outcome: 'crisis_escalated' })
    })
    .where(eq(conversationAnalytics.conversationId, conversationId));
}
```

### Tracking Conversation End

```typescript
export async function trackConversationEnd(
  conversationId: string,
  outcome: 'completed' | 'abandoned' | 'error'
): Promise<void> {
  await db
    .update(conversationAnalytics)
    .set({
      endedAt: new Date(),
      outcome
    })
    .where(eq(conversationAnalytics.conversationId, conversationId));
}
```

## Category Detection (Metadata-Based)

Detect conversation categories WITHOUT reading content:

```typescript
// Categories based on metadata flags from AI response
interface AIResponseMetadata {
  usedCopingStrategies: boolean;
  usedCrisisProtocol: boolean;
  usedCheckInSupport: boolean;
  usedGeneralChat: boolean;
  requestedClarification: boolean;
}

function deriveCategory(metadata: AIResponseMetadata): string {
  if (metadata.usedCrisisProtocol) return 'crisis_support';
  if (metadata.usedCopingStrategies) return 'coping_strategies';
  if (metadata.usedCheckInSupport) return 'checkin_support';
  if (metadata.requestedClarification) return 'clarification';
  return 'general_chat';
}
```

## Dashboard Aggregations

### Session Metrics

```typescript
// Get aggregated session stats (HIPAA safe - no individual data)
async function getSessionStats(days: number = 30) {
  const since = subDays(new Date(), days);

  return db
    .select({
      totalSessions: count(),
      avgMessages: avg(conversationAnalytics.messageCount),
      avgDuration: avg(
        sql`JULIANDAY(ended_at) - JULIANDAY(started_at)) * 24 * 60`
      ),
      completionRate: sql`
        CAST(SUM(CASE WHEN outcome = 'completed' THEN 1 ELSE 0 END) AS FLOAT) /
        CAST(COUNT(*) AS FLOAT)
      `,
      crisisEscalations: sql`
        SUM(CASE WHEN outcome = 'crisis_escalated' THEN 1 ELSE 0 END)
      `
    })
    .from(conversationAnalytics)
    .where(gte(conversationAnalytics.startedAt, since));
}
```

### Token Usage for Cost Tracking

```typescript
async function getTokenUsage(days: number = 30) {
  const since = subDays(new Date(), days);

  const result = await db
    .select({
      totalTokens: sum(conversationAnalytics.totalTokens),
      inputTokens: sum(conversationAnalytics.inputTokens),
      outputTokens: sum(conversationAnalytics.outputTokens),
      avgTokensPerSession: avg(conversationAnalytics.totalTokens)
    })
    .from(conversationAnalytics)
    .where(gte(conversationAnalytics.startedAt, since));

  // Estimate cost (Claude pricing)
  const inputCost = (result.inputTokens / 1_000_000) * 3.00;  // $3/M input
  const outputCost = (result.outputTokens / 1_000_000) * 15.00; // $15/M output

  return {
    ...result,
    estimatedCost: inputCost + outputCost
  };
}
```

### Category Breakdown

```typescript
async function getCategoryBreakdown(days: number = 30) {
  const since = subDays(new Date(), days);

  return db
    .select({
      category: conversationAnalytics.category,
      count: count(),
      percentage: sql`
        CAST(COUNT(*) AS FLOAT) * 100.0 /
        (SELECT COUNT(*) FROM conversation_analytics WHERE started_at >= ${since})
      `
    })
    .from(conversationAnalytics)
    .where(gte(conversationAnalytics.startedAt, since))
    .groupBy(conversationAnalytics.category)
    .orderBy(desc(count()));
}
```

## Alert Configuration

Set up alerts for concerning patterns:

```typescript
interface AnalyticsAlert {
  type: 'crisis_spike' | 'error_spike' | 'abandonment_spike';
  threshold: number;
  windowHours: number;
  action: 'log' | 'email' | 'slack';
}

const alerts: AnalyticsAlert[] = [
  {
    type: 'crisis_spike',
    threshold: 5,  // 5+ crisis escalations
    windowHours: 24,
    action: 'email'
  },
  {
    type: 'error_spike',
    threshold: 10, // 10+ errors
    windowHours: 1,
    action: 'slack'
  },
  {
    type: 'abandonment_spike',
    threshold: 0.5, // 50%+ abandonment rate
    windowHours: 24,
    action: 'log'
  }
];
```

## Database Schema

```sql
CREATE TABLE conversation_analytics (
  id TEXT PRIMARY KEY,
  conversation_id TEXT NOT NULL,
  user_id TEXT NOT NULL,
  started_at TEXT NOT NULL,
  ended_at TEXT,
  message_count INTEGER DEFAULT 0,
  user_message_count INTEGER DEFAULT 0,
  ai_message_count INTEGER DEFAULT 0,
  total_tokens INTEGER DEFAULT 0,
  input_tokens INTEGER DEFAULT 0,
  output_tokens INTEGER DEFAULT 0,
  category TEXT DEFAULT 'unknown',
  outcome TEXT DEFAULT 'in_progress',
  avg_response_time REAL DEFAULT 0,
  had_fallback INTEGER DEFAULT 0,

  FOREIGN KEY (conversation_id) REFERENCES conversations(id),
  FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE INDEX idx_conv_analytics_started ON conversation_analytics(started_at);
CREATE INDEX idx_conv_analytics_user ON conversation_analytics(user_id);
CREATE INDEX idx_conv_analytics_outcome ON conversation_analytics(outcome);
```

## Testing Analytics

```typescript
describe('Conversation Analytics', () => {
  it('tracks session without PHI', async () => {
    const analytics = await trackConversationStart('conv-123', 'user-456');

    // Verify no PHI is stored
    expect(analytics).not.toHaveProperty('messageContent');
    expect(analytics).not.toHaveProperty('userQuery');

    // Verify metadata is stored
    expect(analytics.conversationId).toBe('conv-123');
    expect(analytics.messageCount).toBe(0);
  });

  it('calculates aggregates correctly', async () => {
    const stats = await getSessionStats(30);

    expect(stats.totalSessions).toBeGreaterThanOrEqual(0);
    expect(stats.completionRate).toBeBetween(0, 1);
  });
});
```

## Resources

- [Chatbot Analytics Guide](https://hiverhq.com/blog/chatbot-analytics)
- [Botpress Analytics](https://botpress.com/blog/chatbot-analytics)
- [13 Core Metrics](https://www.tidio.com/blog/chatbot-analytics/)
- Admin Suite Design: `docs/ADMIN-DEVELOPER-SUITE.md`
