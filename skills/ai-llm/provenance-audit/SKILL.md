---
name: provenance-audit
description: AI generation provenance and audit trail tracking. Records decision factors, data lineage, reasoning chains, confidence scoring, and cost tracking for AI-generated content.
license: MIT
compatibility: TypeScript/JavaScript, Python
metadata:
  category: ai
  time: 8h
  source: drift-masterguide
---

# AI Provenance & Audit Trail

Complete provenance tracking for AI-generated content with decision factors, data lineage, and cost tracking.

## When to Use This Skill

- Need to explain why AI made specific suggestions
- Regulatory compliance requires audit trails
- Want to track AI generation costs
- Need confidence scoring for AI outputs
- Building explainable AI systems

## Core Concepts

Provenance tracking captures: decision factors (why), data lineage (from what), reasoning chain (how), confidence scoring, and generation metrics (cost/tokens).


## Implementation

### TypeScript

```typescript
enum InsightType {
  CONTENT_SUGGESTION = 'content_suggestion',
  IMAGE_GENERATION = 'image_generation',
  TEXT_GENERATION = 'text_generation',
}

enum ConfidenceLevel {
  VERY_HIGH = 'very_high',  // 90-100%
  HIGH = 'high',            // 75-89%
  MEDIUM = 'medium',        // 50-74%
  LOW = 'low',              // 25-49%
  VERY_LOW = 'very_low',    // 0-24%
}

interface DataSource {
  sourceType: string;       // 'database', 'api', 'cache'
  sourceKey: string;        // 'postgres:users', 'openai:gpt-4'
  recordsUsed: number;
  freshnessSeconds: number;
  qualityScore: number;     // 0-1
  sampleIds: string[];
}

interface DecisionFactor {
  factorName: string;
  rawValue: number;
  normalizedValue: number;  // 0-1
  weight: number;
  contribution: number;     // normalizedValue * weight
  reasoning: string;
}

interface ReasoningStep {
  stepNumber: number;
  operation: string;        // 'filter', 'score', 'generate'
  description: string;
  inputCount: number;
  outputCount: number;
  algorithm: string;
  durationMs: number;
}

interface GenerationMetrics {
  model: string;
  promptTokens: number;
  completionTokens: number;
  totalTokens: number;
  latencyMs: number;
  estimatedCostUsd: number;
}

interface ProvenanceRecord {
  provenanceId: string;
  workerId: string;
  userId: string;
  insightType: InsightType;
  computedAt: Date;
  durationMs: number;
  insightId: string;
  insightSummary: string;
  confidenceScore: number;
  confidenceLevel: ConfidenceLevel;
  dataSources: DataSource[];
  decisionFactors: DecisionFactor[];
  reasoningChain: ReasoningStep[];
  generationMetrics?: GenerationMetrics;
  validationPassed: boolean;
  tags: string[];
}
```


```typescript
// Provenance Builder - Fluent API
class ProvenanceBuilder {
  private record: Partial<ProvenanceRecord>;
  private startTime: number;
  private stepCounter = 0;

  constructor(insightType: InsightType, workerId: string) {
    this.startTime = Date.now();
    this.record = {
      provenanceId: crypto.randomUUID(),
      workerId,
      insightType,
      computedAt: new Date(),
      dataSources: [],
      decisionFactors: [],
      reasoningChain: [],
      tags: [],
      validationPassed: true,
    };
  }

  setUser(userId: string): this {
    this.record.userId = userId;
    return this;
  }

  addDatabaseSource(table: string, recordsUsed: number, freshnessSeconds: number): this {
    this.record.dataSources!.push({
      sourceType: 'database',
      sourceKey: `postgres:${table}`,
      recordsUsed,
      freshnessSeconds,
      qualityScore: 0.95,
      sampleIds: [],
    });
    return this;
  }

  addApiSource(provider: string, model: string): this {
    this.record.dataSources!.push({
      sourceType: 'api',
      sourceKey: `${provider}:${model}`,
      recordsUsed: 1,
      freshnessSeconds: 0,
      qualityScore: 0.9,
      sampleIds: [],
    });
    return this;
  }

  addFactor(name: string, rawValue: number, normalized: number, weight: number, reasoning: string): this {
    this.record.decisionFactors!.push({
      factorName: name,
      rawValue,
      normalizedValue: normalized,
      weight,
      contribution: normalized * weight,
      reasoning,
    });
    return this;
  }

  addReasoningStep(operation: string, description: string, inputCount: number, outputCount: number, algorithm: string, durationMs = 0): this {
    this.stepCounter++;
    this.record.reasoningChain!.push({
      stepNumber: this.stepCounter,
      operation,
      description,
      inputCount,
      outputCount,
      algorithm,
      durationMs,
    });
    return this;
  }

  setGenerationMetrics(metrics: GenerationMetrics): this {
    this.record.generationMetrics = metrics;
    return this;
  }

  setInsight(id: string, summary: string): this {
    this.record.insightId = id;
    this.record.insightSummary = summary;
    return this;
  }

  setConfidence(score: number): this {
    this.record.confidenceScore = score;
    this.record.confidenceLevel = getConfidenceLevel(score);
    return this;
  }

  build(): ProvenanceRecord {
    this.record.durationMs = Date.now() - this.startTime;
    return this.record as ProvenanceRecord;
  }
}

function getConfidenceLevel(score: number): ConfidenceLevel {
  const normalized = score <= 1 ? score * 100 : score;
  if (normalized >= 90) return ConfidenceLevel.VERY_HIGH;
  if (normalized >= 75) return ConfidenceLevel.HIGH;
  if (normalized >= 50) return ConfidenceLevel.MEDIUM;
  if (normalized >= 25) return ConfidenceLevel.LOW;
  return ConfidenceLevel.VERY_LOW;
}
```


## Usage Examples

```typescript
async function generateWithProvenance(userId: string, topic: string) {
  const provenance = new ProvenanceBuilder(InsightType.CONTENT_SUGGESTION, 'content-worker')
    .setUser(userId);

  // Step 1: Fetch data
  const data = await fetchTrending(topic);
  provenance
    .addDatabaseSource('trending_topics', data.length, 300)
    .addReasoningStep('filter', `Fetched ${data.length} items for "${topic}"`, 0, data.length, 'sql_query');

  // Step 2: Score
  const scored = scoreItems(data);
  provenance
    .addFactor('trend_velocity', scored.velocity, scored.normalizedVelocity, 0.4, 
      `Velocity of ${scored.velocity}/hr indicates ${scored.normalizedVelocity > 0.7 ? 'high' : 'moderate'} interest`)
    .addReasoningStep('score', 'Calculated weighted scores', data.length, data.length, 'weighted_average');

  // Step 3: Generate with AI
  const startGen = Date.now();
  const result = await openai.chat.completions.create({
    model: 'gpt-4',
    messages: [{ role: 'user', content: `Suggest content for: ${topic}` }],
  });

  provenance
    .addApiSource('openai', 'gpt-4')
    .setGenerationMetrics({
      model: 'gpt-4',
      promptTokens: result.usage?.prompt_tokens || 0,
      completionTokens: result.usage?.completion_tokens || 0,
      totalTokens: result.usage?.total_tokens || 0,
      latencyMs: Date.now() - startGen,
      estimatedCostUsd: calculateCost(result.usage),
    })
    .addReasoningStep('generate', 'Generated suggestion using GPT-4', 1, 1, 'gpt-4', Date.now() - startGen);

  // Finalize
  const suggestion = result.choices[0].message.content!;
  provenance
    .setInsight(crypto.randomUUID(), `Content suggestion for "${topic}"`)
    .setConfidence(0.85);

  const record = provenance.build();
  await provenanceStore.save(record);

  return { suggestion, provenanceId: record.provenanceId };
}
```

## Best Practices

1. Start provenance builder at function entry to capture full duration
2. Record all data sources with freshness information
3. Include human-readable reasoning for each decision factor
4. Track token usage and costs for budget monitoring
5. Store sample IDs for audit trail verification

## Common Mistakes

- Not capturing all data sources used in decision
- Missing reasoning explanations (just numbers)
- Forgetting to track generation costs
- Not persisting provenance records
- Skipping confidence scoring

## Related Patterns

- ai-generation-client (generation execution)
- ai-coaching (intent extraction)
- logging-observability (general logging)
