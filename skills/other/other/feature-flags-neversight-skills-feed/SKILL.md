---
name: feature-flags
description: Feature flag patterns for controlled rollouts, A/B testing, kill switches, and runtime configuration. Use when implementing feature toggles, feature flags, gradual rollouts, canary releases, percentage rollouts, dark launches, user targeting, A/B tests, experiments, circuit breakers, emergency kill switches, model switching, or infrastructure flags.
keywords: feature flag, feature toggle, LaunchDarkly, Unleash, split, canary, gradual rollout, percentage rollout, dark launch, A/B test, experiment, kill switch, circuit breaker, model switching, infrastructure flag, runtime config, feature gate
---

# Feature Flags

## Overview

Feature flags (also called feature toggles or feature gates) enable runtime control over feature availability without code deployments. They support gradual rollouts, A/B testing, user targeting, emergency kill switches, ML model switching, and infrastructure configuration. This skill covers implementation patterns, best practices, integration with LaunchDarkly/Unleash, and flag lifecycle management.

## Agents

- **senior-software-engineer** - Feature flag strategy, architecture decisions, rollout planning
- **software-engineer** - Implements feature flags, integrations, and flag evaluation logic
- **security-engineer** - Feature flag security, access controls, audit logging
- **senior-infrastructure-engineer** - Feature flag infrastructure, distributed systems, caching strategies

## Key Concepts

### Flag Types

**Boolean Flags** - Simple on/off toggles:

```typescript
interface BooleanFlag {
  key: string;
  enabled: boolean;
  description: string;
}

// Usage
if (featureFlags.isEnabled("new-checkout-flow")) {
  return <NewCheckoutFlow />;
}
return <LegacyCheckout />;
```

**Percentage Rollout Flags** - Gradual exposure:

```typescript
interface PercentageFlag {
  key: string;
  percentage: number; // 0-100
  salt: string; // For consistent hashing
}

function isEnabledForUser(flag: PercentageFlag, userId: string): boolean {
  // Consistent hashing ensures same user always gets same result
  const hash = createHash("md5").update(`${flag.salt}:${userId}`).digest("hex");
  const bucket = parseInt(hash.substring(0, 8), 16) % 100;
  return bucket < flag.percentage;
}
```

**User-Targeted Flags** - Specific user segments:

```typescript
interface TargetedFlag {
  key: string;
  defaultValue: boolean;
  rules: TargetingRule[];
}

interface TargetingRule {
  attribute: string; // 'userId', 'email', 'country', 'plan'
  operator: "in" | "notIn" | "equals" | "contains" | "startsWith" | "matches";
  values: string[];
  value: boolean;
}

// Example: Enable for beta users and premium plans
const flag: TargetedFlag = {
  key: "advanced-analytics",
  defaultValue: false,
  rules: [
    {
      attribute: "email",
      operator: "in",
      values: ["beta@example.com"],
      value: true,
    },
    {
      attribute: "plan",
      operator: "in",
      values: ["premium", "enterprise"],
      value: true,
    },
    { attribute: "country", operator: "in", values: ["US", "CA"], value: true },
  ],
};
```

**Multivariate Flags** - Multiple variants for A/B testing:

```typescript
interface MultivariateFlag<T> {
  key: string;
  variants: Variant<T>[];
  defaultVariant: string;
}

interface Variant<T> {
  name: string;
  value: T;
  weight: number; // Percentage allocation
}

// Example: Button color A/B test
const buttonColorFlag: MultivariateFlag<string> = {
  key: "checkout-button-color",
  defaultVariant: "control",
  variants: [
    { name: "control", value: "#007bff", weight: 34 },
    { name: "green", value: "#28a745", weight: 33 },
    { name: "orange", value: "#fd7e14", weight: 33 },
  ],
};
```

### Custom Implementation

```typescript
import { Redis } from "ioredis";
import { createHash } from "crypto";

interface FeatureFlag {
  key: string;
  type: "boolean" | "percentage" | "targeted" | "multivariate";
  enabled: boolean;
  percentage?: number;
  rules?: TargetingRule[];
  variants?: Variant<unknown>[];
  salt: string;
  description: string;
  createdAt: Date;
  updatedAt: Date;
}

interface EvaluationContext {
  userId?: string;
  email?: string;
  country?: string;
  plan?: string;
  [key: string]: string | number | boolean | undefined;
}

class FeatureFlagService {
  private redis: Redis;
  private cache: Map<string, { flag: FeatureFlag; expiresAt: number }> =
    new Map();
  private cacheTTL = 60000; // 1 minute

  constructor(redis: Redis) {
    this.redis = redis;
  }

  async getFlag(key: string): Promise<FeatureFlag | null> {
    // Check local cache
    const cached = this.cache.get(key);
    if (cached && cached.expiresAt > Date.now()) {
      return cached.flag;
    }

    // Fetch from Redis
    const data = await this.redis.get(`flag:${key}`);
    if (!data) return null;

    const flag: FeatureFlag = JSON.parse(data);
    this.cache.set(key, { flag, expiresAt: Date.now() + this.cacheTTL });
    return flag;
  }

  async evaluate(
    key: string,
    context: EvaluationContext = {}
  ): Promise<boolean> {
    const flag = await this.getFlag(key);
    if (!flag) return false;
    if (!flag.enabled) return false;

    switch (flag.type) {
      case "boolean":
        return true;

      case "percentage":
        return this.evaluatePercentage(flag, context.userId || "anonymous");

      case "targeted":
        return this.evaluateTargeting(flag, context);

      default:
        return false;
    }
  }

  async evaluateVariant<T>(
    key: string,
    context: EvaluationContext = {}
  ): Promise<T | null> {
    const flag = await this.getFlag(key);
    if (!flag || !flag.enabled || !flag.variants) return null;

    const userId = context.userId || "anonymous";
    const hash = createHash("md5")
      .update(`${flag.salt}:${userId}`)
      .digest("hex");
    const bucket = parseInt(hash.substring(0, 8), 16) % 100;

    let cumulative = 0;
    for (const variant of flag.variants) {
      cumulative += variant.weight;
      if (bucket < cumulative) {
        return variant.value as T;
      }
    }

    return (flag.variants[0]?.value as T) ?? null;
  }

  private evaluatePercentage(flag: FeatureFlag, userId: string): boolean {
    const hash = createHash("md5")
      .update(`${flag.salt}:${userId}`)
      .digest("hex");
    const bucket = parseInt(hash.substring(0, 8), 16) % 100;
    return bucket < (flag.percentage ?? 0);
  }

  private evaluateTargeting(
    flag: FeatureFlag,
    context: EvaluationContext
  ): boolean {
    if (!flag.rules || flag.rules.length === 0) return true;

    for (const rule of flag.rules) {
      const attributeValue = String(context[rule.attribute] ?? "");

      let matches = false;
      switch (rule.operator) {
        case "in":
          matches = rule.values.includes(attributeValue);
          break;
        case "notIn":
          matches = !rule.values.includes(attributeValue);
          break;
        case "equals":
          matches = attributeValue === rule.values[0];
          break;
        case "contains":
          matches = rule.values.some((v) => attributeValue.includes(v));
          break;
        case "startsWith":
          matches = rule.values.some((v) => attributeValue.startsWith(v));
          break;
        case "matches":
          matches = rule.values.some((v) => new RegExp(v).test(attributeValue));
          break;
      }

      if (matches) return rule.value;
    }

    return false;
  }

  // Admin methods
  async setFlag(flag: FeatureFlag): Promise<void> {
    await this.redis.set(`flag:${flag.key}`, JSON.stringify(flag));
    this.cache.delete(flag.key);

    // Publish change for other instances
    await this.redis.publish("flag-updates", JSON.stringify({ key: flag.key }));
  }

  async deleteFlag(key: string): Promise<void> {
    await this.redis.del(`flag:${key}`);
    this.cache.delete(key);
    await this.redis.publish(
      "flag-updates",
      JSON.stringify({ key, deleted: true })
    );
  }
}
```

### Gradual Rollouts and Canary Releases

```typescript
interface RolloutStrategy {
  type: "linear" | "exponential" | "manual";
  startPercentage: number;
  targetPercentage: number;
  incrementPercentage: number;
  intervalMinutes: number;
  currentPercentage: number;
  startedAt: Date;
  pausedAt?: Date;
}

class RolloutManager {
  private flags: FeatureFlagService;

  async startRollout(
    flagKey: string,
    strategy: RolloutStrategy
  ): Promise<void> {
    const flag = await this.flags.getFlag(flagKey);
    if (!flag) throw new Error("Flag not found");

    flag.percentage = strategy.startPercentage;
    flag.rolloutStrategy = strategy;
    await this.flags.setFlag(flag);

    // Schedule automatic increments
    if (strategy.type !== "manual") {
      this.scheduleIncrement(flagKey, strategy);
    }
  }

  private async scheduleIncrement(
    flagKey: string,
    strategy: RolloutStrategy
  ): Promise<void> {
    const incrementJob = async () => {
      const flag = await this.flags.getFlag(flagKey);
      if (!flag || flag.rolloutStrategy?.pausedAt) return;

      const current = flag.percentage ?? 0;
      let newPercentage: number;

      if (strategy.type === "linear") {
        newPercentage = Math.min(
          current + strategy.incrementPercentage,
          strategy.targetPercentage
        );
      } else {
        // Exponential: double each time
        newPercentage = Math.min(current * 2, strategy.targetPercentage);
      }

      flag.percentage = newPercentage;
      await this.flags.setFlag(flag);

      // Continue if not at target
      if (newPercentage < strategy.targetPercentage) {
        setTimeout(incrementJob, strategy.intervalMinutes * 60 * 1000);
      }
    };

    setTimeout(incrementJob, strategy.intervalMinutes * 60 * 1000);
  }

  async pauseRollout(flagKey: string): Promise<void> {
    const flag = await this.flags.getFlag(flagKey);
    if (flag?.rolloutStrategy) {
      flag.rolloutStrategy.pausedAt = new Date();
      await this.flags.setFlag(flag);
    }
  }

  async rollback(flagKey: string): Promise<void> {
    const flag = await this.flags.getFlag(flagKey);
    if (flag) {
      flag.percentage = 0;
      flag.enabled = false;
      await this.flags.setFlag(flag);
    }
  }
}
```

### A/B Testing Integration

```typescript
interface Experiment {
  id: string;
  flagKey: string;
  name: string;
  hypothesis: string;
  metrics: string[]; // Metrics to track
  variants: ExperimentVariant[];
  status: "draft" | "running" | "paused" | "completed";
  startDate?: Date;
  endDate?: Date;
  sampleSize: number;
  confidenceLevel: number; // e.g., 0.95
}

interface ExperimentVariant {
  name: string;
  weight: number;
  conversions: number;
  impressions: number;
}

class ABTestingService {
  async trackExposure(
    experimentId: string,
    variantName: string,
    userId: string
  ): Promise<void> {
    // Record that user was exposed to variant
    await this.analytics.track({
      event: "experiment_exposure",
      userId,
      properties: {
        experimentId,
        variant: variantName,
        timestamp: new Date(),
      },
    });

    // Increment impression count
    await this.redis.hincrby(
      `experiment:${experimentId}:${variantName}`,
      "impressions",
      1
    );
  }

  async trackConversion(
    experimentId: string,
    userId: string,
    metric: string
  ): Promise<void> {
    // Get user's assigned variant
    const variant = await this.redis.hget(
      `experiment:${experimentId}:assignments`,
      userId
    );
    if (!variant) return;

    await this.analytics.track({
      event: "experiment_conversion",
      userId,
      properties: {
        experimentId,
        variant,
        metric,
        timestamp: new Date(),
      },
    });

    await this.redis.hincrby(
      `experiment:${experimentId}:${variant}`,
      "conversions",
      1
    );
  }

  async getResults(experimentId: string): Promise<ExperimentResults> {
    const experiment = await this.getExperiment(experimentId);

    const results = await Promise.all(
      experiment.variants.map(async (variant) => {
        const data = await this.redis.hgetall(
          `experiment:${experimentId}:${variant.name}`
        );
        return {
          name: variant.name,
          impressions: parseInt(data.impressions || "0"),
          conversions: parseInt(data.conversions || "0"),
          conversionRate:
            parseInt(data.conversions || "0") /
            parseInt(data.impressions || "1"),
        };
      })
    );

    // Calculate statistical significance
    const control = results.find((r) => r.name === "control");
    const treatments = results.filter((r) => r.name !== "control");

    return {
      experimentId,
      results,
      winners: treatments.filter((t) =>
        this.isStatisticallySignificant(control!, t, experiment.confidenceLevel)
      ),
    };
  }

  private isStatisticallySignificant(
    control: VariantResult,
    treatment: VariantResult,
    confidenceLevel: number
  ): boolean {
    // Z-test for proportions
    const p1 = control.conversionRate;
    const p2 = treatment.conversionRate;
    const n1 = control.impressions;
    const n2 = treatment.impressions;

    const pooledP = (p1 * n1 + p2 * n2) / (n1 + n2);
    const se = Math.sqrt(pooledP * (1 - pooledP) * (1 / n1 + 1 / n2));
    const z = (p2 - p1) / se;

    // Z-score for 95% confidence is 1.96
    const zThreshold = confidenceLevel === 0.95 ? 1.96 : 2.58; // 99%
    return Math.abs(z) > zThreshold;
  }
}
```

### Kill Switches

```typescript
interface KillSwitch {
  key: string;
  description: string;
  affectedServices: string[];
  activatedAt?: Date;
  activatedBy?: string;
  reason?: string;
  autoRecoveryMinutes?: number;
}

class KillSwitchService {
  private redis: Redis;
  private alerting: AlertingService;

  async activate(
    key: string,
    reason: string,
    activatedBy: string
  ): Promise<void> {
    const killSwitch = await this.getKillSwitch(key);
    if (!killSwitch) throw new Error("Kill switch not found");

    killSwitch.activatedAt = new Date();
    killSwitch.activatedBy = activatedBy;
    killSwitch.reason = reason;

    await this.redis.set(`killswitch:${key}`, JSON.stringify(killSwitch));

    // Broadcast to all instances immediately
    await this.redis.publish(
      "killswitch-activated",
      JSON.stringify(killSwitch)
    );

    // Alert on-call
    await this.alerting.sendCritical({
      title: `Kill Switch Activated: ${key}`,
      message: `Reason: ${reason}\nActivated by: ${activatedBy}\nAffected: ${killSwitch.affectedServices.join(
        ", "
      )}`,
    });

    // Schedule auto-recovery if configured
    if (killSwitch.autoRecoveryMinutes) {
      setTimeout(
        () => this.deactivate(key, "Auto-recovery"),
        killSwitch.autoRecoveryMinutes * 60 * 1000
      );
    }
  }

  async deactivate(key: string, reason: string): Promise<void> {
    const killSwitch = await this.getKillSwitch(key);
    if (!killSwitch) return;

    killSwitch.activatedAt = undefined;
    killSwitch.activatedBy = undefined;
    killSwitch.reason = undefined;

    await this.redis.set(`killswitch:${key}`, JSON.stringify(killSwitch));
    await this.redis.publish(
      "killswitch-deactivated",
      JSON.stringify({ key, reason })
    );

    await this.alerting.sendInfo({
      title: `Kill Switch Deactivated: ${key}`,
      message: `Reason: ${reason}`,
    });
  }

  async isActive(key: string): Promise<boolean> {
    const data = await this.redis.get(`killswitch:${key}`);
    if (!data) return false;
    const killSwitch: KillSwitch = JSON.parse(data);
    return !!killSwitch.activatedAt;
  }
}

// Usage in application code
async function processPayment(payment: Payment): Promise<PaymentResult> {
  // Check kill switch first
  if (await killSwitches.isActive("payments-disabled")) {
    throw new ServiceUnavailableError(
      "Payment processing temporarily disabled"
    );
  }

  // Normal processing
  return paymentProcessor.process(payment);
}
```

### Flag Lifecycle Management

```typescript
interface FlagLifecycle {
  key: string;
  status:
    | "planning"
    | "development"
    | "testing"
    | "rollout"
    | "stable"
    | "deprecated"
    | "removed";
  owner: string;
  team: string;
  createdAt: Date;
  plannedRemovalDate?: Date;
  jiraTicket?: string;
  staleAfterDays: number;
}

class FlagLifecycleManager {
  async checkStaleFlags(): Promise<StaleFlag[]> {
    const flags = await this.getAllFlags();
    const now = new Date();

    return flags.filter((flag) => {
      const lifecycle = flag.lifecycle;
      if (!lifecycle) return false;

      const ageInDays =
        (now.getTime() - lifecycle.createdAt.getTime()) / (1000 * 60 * 60 * 24);

      // Flag is stale if:
      // 1. It's older than staleAfterDays and still in development/testing
      // 2. It's past its planned removal date
      // 3. It's been stable for > 30 days (should be permanent or removed)

      if (lifecycle.status === "stable" && ageInDays > 30) return true;
      if (lifecycle.plannedRemovalDate && lifecycle.plannedRemovalDate < now)
        return true;
      if (
        ["development", "testing"].includes(lifecycle.status) &&
        ageInDays > lifecycle.staleAfterDays
      )
        return true;

      return false;
    });
  }

  async generateCleanupReport(): Promise<CleanupReport> {
    const staleFlags = await this.checkStaleFlags();

    return {
      generatedAt: new Date(),
      staleFlags: staleFlags.map((flag) => ({
        key: flag.key,
        status: flag.lifecycle.status,
        owner: flag.lifecycle.owner,
        age: this.calculateAge(flag.lifecycle.createdAt),
        recommendation: this.getRecommendation(flag),
      })),
      summary: {
        total: staleFlags.length,
        byStatus: this.groupBy(staleFlags, (f) => f.lifecycle.status),
        byTeam: this.groupBy(staleFlags, (f) => f.lifecycle.team),
      },
    };
  }

  private getRecommendation(flag: FlagWithLifecycle): string {
    const { status, plannedRemovalDate } = flag.lifecycle;

    if (plannedRemovalDate && plannedRemovalDate < new Date()) {
      return "URGENT: Past planned removal date. Remove flag and clean up code.";
    }
    if (status === "stable") {
      return "Flag is stable. Either make permanent (remove flag, keep feature) or deprecate.";
    }
    if (status === "development" || status === "testing") {
      return "Flag stuck in development. Complete rollout or remove if abandoned.";
    }
    return "Review flag status and update lifecycle.";
  }
}
```

### LaunchDarkly Integration

```typescript
import * as LaunchDarkly from "launchdarkly-node-server-sdk";

const ldClient = LaunchDarkly.init(process.env.LAUNCHDARKLY_SDK_KEY!);

interface LDUser {
  key: string;
  email?: string;
  name?: string;
  custom?: Record<string, string | number | boolean>;
}

async function evaluateFlag(
  flagKey: string,
  user: LDUser,
  defaultValue: boolean
): Promise<boolean> {
  await ldClient.waitForInitialization();
  return ldClient.variation(flagKey, user, defaultValue);
}

async function evaluateFlagWithReason(
  flagKey: string,
  user: LDUser,
  defaultValue: boolean
) {
  await ldClient.waitForInitialization();
  const detail = await ldClient.variationDetail(flagKey, user, defaultValue);

  return {
    value: detail.value,
    reason: detail.reason,
    variationIndex: detail.variationIndex,
  };
}

// Track custom events for experiments
function trackConversion(
  user: LDUser,
  eventKey: string,
  data?: Record<string, unknown>
): void {
  ldClient.track(eventKey, user, data);
}

// React hook for client-side
function useFeatureFlag(
  flagKey: string,
  defaultValue: boolean = false
): boolean {
  const ldClient = useLDClient();
  const [value, setValue] = useState(defaultValue);

  useEffect(() => {
    if (!ldClient) return;

    setValue(ldClient.variation(flagKey, defaultValue));

    const handler = (newValue: boolean) => setValue(newValue);
    ldClient.on(`change:${flagKey}`, handler);

    return () => ldClient.off(`change:${flagKey}`, handler);
  }, [ldClient, flagKey, defaultValue]);

  return value;
}
```

### ML Model Feature Flags

```typescript
interface ModelFlag {
  key: string;
  modelVariants: ModelVariant[];
  routingStrategy: "percentage" | "performance" | "custom";
  fallbackModel: string;
  performanceThresholds?: {
    latencyMs: number;
    errorRate: number;
  };
}

interface ModelVariant {
  name: string;
  modelId: string;
  version: string;
  weight?: number; // For percentage routing
  endpoint: string;
}

class ModelFlagService {
  async evaluateModel(
    flagKey: string,
    context: { userId?: string; inputSize?: number }
  ): Promise<ModelVariant> {
    const flag = await this.getModelFlag(flagKey);

    switch (flag.routingStrategy) {
      case "percentage":
        return this.percentageRouting(flag, context.userId || "anonymous");

      case "performance":
        return this.performanceRouting(flag);

      case "custom":
        return this.customRouting(flag, context);

      default:
        return flag.modelVariants.find((v) => v.name === flag.fallbackModel)!;
    }
  }

  private async performanceRouting(flag: ModelFlag): Promise<ModelVariant> {
    // Get real-time performance metrics for each model
    const metrics = await Promise.all(
      flag.modelVariants.map(async (variant) => ({
        variant,
        latency: await this.getAverageLatency(variant.modelId),
        errorRate: await this.getErrorRate(variant.modelId),
      }))
    );

    // Filter models meeting performance thresholds
    const eligible = metrics.filter(
      (m) =>
        m.latency < flag.performanceThresholds!.latencyMs &&
        m.errorRate < flag.performanceThresholds!.errorRate
    );

    // Return best performing model or fallback
    if (eligible.length === 0) {
      return flag.modelVariants.find((v) => v.name === flag.fallbackModel)!;
    }

    return eligible.sort((a, b) => a.latency - b.latency)[0].variant;
  }

  async trackModelInference(
    flagKey: string,
    modelVariant: ModelVariant,
    metrics: {
      latencyMs: number;
      success: boolean;
      inputTokens: number;
      outputTokens: number;
    }
  ): Promise<void> {
    // Track metrics for performance-based routing
    await this.redis.zadd(
      `model:${modelVariant.modelId}:latency`,
      Date.now(),
      metrics.latencyMs
    );

    await this.redis.hincrby(
      `model:${modelVariant.modelId}:stats`,
      metrics.success ? "success" : "failure",
      1
    );

    // Track costs
    await this.redis.hincrby(
      `model:${modelVariant.modelId}:tokens`,
      "input",
      metrics.inputTokens
    );
    await this.redis.hincrby(
      `model:${modelVariant.modelId}:tokens`,
      "output",
      metrics.outputTokens
    );
  }
}

// Usage example
async function generateResponse(
  prompt: string,
  userId: string
): Promise<string> {
  const modelVariant = await modelFlags.evaluateModel("chat-model", { userId });

  const startTime = Date.now();
  try {
    const response = await fetch(modelVariant.endpoint, {
      method: "POST",
      body: JSON.stringify({ prompt, model: modelVariant.modelId }),
    });

    const data = await response.json();

    await modelFlags.trackModelInference("chat-model", modelVariant, {
      latencyMs: Date.now() - startTime,
      success: true,
      inputTokens: data.usage.input_tokens,
      outputTokens: data.usage.output_tokens,
    });

    return data.response;
  } catch (error) {
    await modelFlags.trackModelInference("chat-model", modelVariant, {
      latencyMs: Date.now() - startTime,
      success: false,
      inputTokens: 0,
      outputTokens: 0,
    });
    throw error;
  }
}
```

### Infrastructure Feature Flags

```typescript
interface InfrastructureFlag {
  key: string;
  type: "database" | "cache" | "queue" | "storage" | "cdn";
  variants: InfraVariant[];
  healthCheckInterval: number;
  autoFailover: boolean;
}

interface InfraVariant {
  name: string;
  config: {
    host?: string;
    port?: number;
    url?: string;
    region?: string;
    [key: string]: string | number | boolean | undefined;
  };
  healthEndpoint?: string;
  healthy: boolean;
  priority: number; // Lower = higher priority
}

class InfrastructureFlagService {
  private healthChecks: Map<string, NodeJS.Timer> = new Map();

  async startHealthChecks(flagKey: string): Promise<void> {
    const flag = await this.getInfraFlag(flagKey);

    const interval = setInterval(async () => {
      for (const variant of flag.variants) {
        if (!variant.healthEndpoint) continue;

        try {
          const response = await fetch(variant.healthEndpoint, {
            timeout: 5000,
          });
          variant.healthy = response.ok;
        } catch {
          variant.healthy = false;
        }
      }

      await this.updateInfraFlag(flag);
    }, flag.healthCheckInterval);

    this.healthChecks.set(flagKey, interval);
  }

  async getActiveVariant(flagKey: string): Promise<InfraVariant> {
    const flag = await this.getInfraFlag(flagKey);

    // Get healthy variants sorted by priority
    const healthyVariants = flag.variants
      .filter((v) => v.healthy)
      .sort((a, b) => a.priority - b.priority);

    if (healthyVariants.length === 0) {
      if (flag.autoFailover) {
        // Use unhealthy variant as last resort
        console.error(`No healthy variants for ${flagKey}, using fallback`);
        return flag.variants.sort((a, b) => a.priority - b.priority)[0];
      } else {
        throw new Error(`No healthy variants available for ${flagKey}`);
      }
    }

    return healthyVariants[0];
  }
}

// Database migration example
class DatabaseConnection {
  private infraFlags: InfrastructureFlagService;
  private currentConnection?: Connection;

  async getConnection(): Promise<Connection> {
    const variant = await this.infraFlags.getActiveVariant("primary-database");

    // Reuse connection if config hasn't changed
    if (this.currentConnection?.config.host === variant.config.host) {
      return this.currentConnection;
    }

    // Create new connection to migrated database
    this.currentConnection = await createConnection({
      host: variant.config.host as string,
      port: variant.config.port as number,
      database: variant.config.database as string,
    });

    return this.currentConnection;
  }
}

// CDN migration example
class AssetService {
  async getAssetUrl(assetPath: string): Promise<string> {
    const cdnVariant = await infraFlags.getActiveVariant("cdn-provider");

    return `${cdnVariant.config.url}/${assetPath}`;
  }
}
```

### Flag Cleanup and Technical Debt Management

```typescript
interface FlagCleanupTask {
  flagKey: string;
  status: "pending" | "in-progress" | "completed" | "blocked";
  type: "remove-flag" | "make-permanent" | "deprecate";
  estimatedEffort: "small" | "medium" | "large";
  affectedCodePaths: string[];
  dependencies: string[];
  assignee?: string;
  dueDate?: Date;
}

class FlagCleanupService {
  async analyzeCodeImpact(flagKey: string): Promise<CodeImpactReport> {
    // Scan codebase for flag references
    const references = await this.findFlagReferences(flagKey);

    return {
      flagKey,
      totalReferences: references.length,
      fileCount: new Set(references.map((r) => r.file)).size,
      byFileType: this.groupBy(references, (r) => r.fileExtension),
      complexityScore: this.calculateComplexity(references),
      recommendations: this.generateRecommendations(references),
    };
  }

  private calculateComplexity(references: CodeReference[]): number {
    let score = 0;

    for (const ref of references) {
      // Nested conditions increase complexity
      if (ref.context.includes("if") && ref.context.includes("else")) {
        score += 2;
      }

      // Multiple flags in same file
      const otherFlags = this.countOtherFlags(ref.file);
      score += otherFlags * 0.5;

      // Presence in critical paths
      if (ref.file.includes("payment") || ref.file.includes("auth")) {
        score += 3;
      }
    }

    return score;
  }

  async generateCleanupPlan(staleFlags: string[]): Promise<FlagCleanupTask[]> {
    const tasks: FlagCleanupTask[] = [];

    for (const flagKey of staleFlags) {
      const flag = await this.getFlag(flagKey);
      const impact = await this.analyzeCodeImpact(flagKey);

      // Determine cleanup type
      let type: FlagCleanupTask["type"];
      if (flag.percentage === 100 && flag.lifecycle.status === "stable") {
        type = "make-permanent"; // Remove flag, keep new code path
      } else if (flag.percentage === 0) {
        type = "remove-flag"; // Remove flag and new code path
      } else {
        type = "deprecate"; // Mark for future removal
      }

      tasks.push({
        flagKey,
        status: "pending",
        type,
        estimatedEffort:
          impact.complexityScore < 5
            ? "small"
            : impact.complexityScore < 15
            ? "medium"
            : "large",
        affectedCodePaths:
          impact.fileCount > 0
            ? Array.from(new Set(impact.references.map((r) => r.file)))
            : [],
        dependencies: await this.findDependentFlags(flagKey),
      });
    }

    // Sort by effort (easiest first for quick wins)
    return tasks.sort((a, b) => {
      const effortMap = { small: 1, medium: 2, large: 3 };
      return effortMap[a.estimatedEffort] - effortMap[b.estimatedEffort];
    });
  }

  async trackCleanupProgress(): Promise<CleanupMetrics> {
    const allFlags = await this.getAllFlags();
    const tasks = await this.getAllCleanupTasks();

    return {
      totalFlags: allFlags.length,
      staleFlags: allFlags.filter((f) => this.isStale(f)).length,
      flagsWithCleanupTasks: tasks.length,
      completedCleanups: tasks.filter((t) => t.status === "completed").length,
      averageAgeOfStaleFlags: this.calculateAverageAge(
        allFlags.filter((f) => this.isStale(f))
      ),
      projectedCleanupDate: this.estimateCompletionDate(tasks),
    };
  }
}

// Automated cleanup detection
class FlagCleanupMonitor {
  async runDailyCleanupCheck(): Promise<void> {
    const staleFlags = await this.flagLifecycle.checkStaleFlags();

    if (staleFlags.length === 0) return;

    // Create Jira tickets for cleanup
    for (const flag of staleFlags) {
      const impact = await this.cleanup.analyzeCodeImpact(flag.key);

      await this.ticketingSystem.createTicket({
        title: `Clean up feature flag: ${flag.key}`,
        description: `
          Flag Status: ${flag.lifecycle.status}
          Age: ${this.calculateAge(flag.lifecycle.createdAt)} days
          References: ${impact.totalReferences} in ${impact.fileCount} files
          Complexity: ${impact.complexityScore}

          Recommendations:
          ${impact.recommendations.join("\n")}
        `,
        priority:
          impact.complexityScore < 5
            ? "low"
            : impact.complexityScore < 15
            ? "medium"
            : "high",
        labels: ["technical-debt", "feature-flags", "cleanup"],
        assignee: flag.lifecycle.owner,
      });
    }

    // Send weekly digest to engineering team
    if (new Date().getDay() === 1) {
      // Monday
      await this.sendCleanupDigest(staleFlags);
    }
  }
}
```

## Best Practices

1. **Flag Naming Conventions**

   - Use descriptive, consistent names: `feature-checkout-v2`, `experiment-button-color`
   - Include type prefix: `release-*`, `experiment-*`, `ops-*`, `kill-*`
   - Avoid abbreviations and ensure team-wide understanding

2. **Flag Hygiene**

   - Set expiration dates for temporary flags
   - Remove flags after features are fully rolled out
   - Track flag ownership and associated tickets
   - Regular cleanup audits (monthly)

3. **Testing**

   - Test all flag states (on, off, each variant)
   - Include flag states in integration tests
   - Test rollback scenarios

4. **Monitoring**

   - Track flag evaluation counts and latency
   - Alert on unusual patterns (sudden spikes, failures)
   - Log flag decisions for debugging

5. **Documentation**
   - Document what each flag controls
   - Include rollback instructions
   - Link to related PRs and tickets

## Examples

### React Feature Flag Provider

```typescript
import React, { createContext, useContext, useEffect, useState } from "react";

interface FeatureFlagContextType {
  isEnabled: (key: string) => boolean;
  getVariant: <T>(key: string) => T | null;
  loading: boolean;
}

const FeatureFlagContext = createContext<FeatureFlagContextType | null>(null);

export function FeatureFlagProvider({
  children,
  userId,
}: {
  children: React.ReactNode;
  userId: string;
}) {
  const [flags, setFlags] = useState<Record<string, unknown>>({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadFlags() {
      const response = await fetch(`/api/flags?userId=${userId}`);
      const data = await response.json();
      setFlags(data);
      setLoading(false);
    }
    loadFlags();

    // Subscribe to real-time updates
    const ws = new WebSocket(
      `wss://api.example.com/flags/stream?userId=${userId}`
    );
    ws.onmessage = (event) => {
      const update = JSON.parse(event.data);
      setFlags((prev) => ({ ...prev, [update.key]: update.value }));
    };

    return () => ws.close();
  }, [userId]);

  const value: FeatureFlagContextType = {
    isEnabled: (key) => Boolean(flags[key]),
    getVariant: (key) => (flags[key] as T) ?? null,
    loading,
  };

  return (
    <FeatureFlagContext.Provider value={value}>
      {children}
    </FeatureFlagContext.Provider>
  );
}

export function useFeatureFlag(key: string): boolean {
  const context = useContext(FeatureFlagContext);
  if (!context)
    throw new Error("useFeatureFlag must be used within FeatureFlagProvider");
  return context.isEnabled(key);
}

// Usage
function CheckoutPage() {
  const newCheckout = useFeatureFlag("new-checkout-flow");

  if (newCheckout) {
    return <NewCheckoutFlow />;
  }
  return <LegacyCheckout />;
}
```

## When to Use This Skill

Use the feature-flags skill for:

- **Feature Toggles** - Runtime on/off switches for features
- **Gradual Rollouts** - Percentage-based or canary releases (1% -> 5% -> 25% -> 100%)
- **Dark Launches** - Deploy code disabled, enable when ready
- **A/B Testing** - Compare variants to measure impact
- **User Targeting** - Enable features for specific users, regions, or plans
- **Kill Switches** - Emergency disable for broken features
- **Circuit Breakers** - Auto-disable when error thresholds exceeded
- **ML Model Flags** - Switch between model versions or providers
- **Infrastructure Flags** - Migrate databases, caches, CDNs without downtime
- **Configuration** - Runtime config changes without redeployment
- **Cleanup** - Managing technical debt from old flags

## Agent Selection Guide

| Task                           | Agent                          | Why                                                 |
| ------------------------------ | ------------------------------ | --------------------------------------------------- |
| Design flag architecture       | senior-software-engineer       | Strategic decisions on flag types, rollout strategy |
| Implement flag service         | software-engineer              | Build evaluation logic, integrations                |
| Review flag security           | security-engineer              | Access controls, audit logging, sensitive data      |
| Scale flag infrastructure      | senior-infrastructure-engineer | Distributed caching, performance, failover          |
| Integrate LaunchDarkly/Unleash | software-engineer              | SDK integration, webhook setup                      |
| Plan ML model rollout          | senior-software-engineer       | Performance routing, fallback strategy              |
| Implement cleanup automation   | software-engineer              | Code scanning, impact analysis                      |
| Design flag lifecycle policy   | senior-software-engineer       | Governance, technical debt prevention               |
