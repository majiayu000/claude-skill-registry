---
name: feature-flag-system
description: Implement feature flags (toggles) for controlled feature rollouts, A/B testing, canary deployments, and kill switches. Use when deploying new features gradually, testing in production, or managing feature lifecycles.
---

# Feature Flag System

## Overview

Implement feature flags to decouple deployment from release, enable gradual rollouts, A/B testing, and provide emergency kill switches.

## When to Use

- Gradual feature rollouts
- A/B testing and experiments
- Canary deployments
- Beta features for specific users
- Emergency kill switches
- Trunk-based development
- Dark launching
- Operational flags (maintenance mode)
- User-specific features

## Implementation Examples

### 1. **Feature Flag Service (TypeScript)**

```typescript
interface FlagConfig {
  key: string;
  enabled: boolean;
  description: string;
  rules?: FlagRule[];
  variants?: FlagVariant[];
  createdAt: Date;
  updatedAt: Date;
}

interface FlagRule {
  type: 'user' | 'percentage' | 'attribute' | 'datetime';
  operator: 'in' | 'equals' | 'contains' | 'gt' | 'lt' | 'between';
  attribute?: string;
  values: any[];
}

interface FlagVariant {
  key: string;
  weight: number;
  value: any;
}

interface EvaluationContext {
  userId?: string;
  email?: string;
  attributes?: Record<string, any>;
  timestamp?: number;
}

class FeatureFlagService {
  private flags: Map<string, FlagConfig> = new Map();

  constructor() {
    this.loadFlags();
  }

  private loadFlags(): void {
    // Load from database or config
    this.flags.set('new-dashboard', {
      key: 'new-dashboard',
      enabled: true,
      description: 'New dashboard UI',
      rules: [
        {
          type: 'percentage',
          operator: 'lt',
          values: [25] // 25% rollout
        }
      ],
      createdAt: new Date(),
      updatedAt: new Date()
    });

    this.flags.set('premium-features', {
      key: 'premium-features',
      enabled: true,
      description: 'Premium features for paid users',
      rules: [
        {
          type: 'attribute',
          operator: 'equals',
          attribute: 'plan',
          values: ['premium', 'enterprise']
        }
      ],
      createdAt: new Date(),
      updatedAt: new Date()
    });

    this.flags.set('beta-feature', {
      key: 'beta-feature',
      enabled: true,
      description: 'Beta feature',
      rules: [
        {
          type: 'user',
          operator: 'in',
          values: ['user1', 'user2', 'user3']
        }
      ],
      createdAt: new Date(),
      updatedAt: new Date()
    });
  }

  isEnabled(flagKey: string, context: EvaluationContext = {}): boolean {
    const flag = this.flags.get(flagKey);

    if (!flag) {
      console.warn(`Flag not found: ${flagKey}`);
      return false;
    }

    if (!flag.enabled) {
      return false;
    }

    if (!flag.rules || flag.rules.length === 0) {
      return true;
    }

    return this.evaluateRules(flag.rules, context);
  }

  getVariant(flagKey: string, context: EvaluationContext = {}): any {
    const flag = this.flags.get(flagKey);

    if (!flag || !this.isEnabled(flagKey, context)) {
      return null;
    }

    if (!flag.variants || flag.variants.length === 0) {
      return true;
    }

    return this.selectVariant(flag.variants, context);
  }

  private evaluateRules(rules: FlagRule[], context: EvaluationContext): boolean {
    return rules.every(rule => this.evaluateRule(rule, context));
  }

  private evaluateRule(rule: FlagRule, context: EvaluationContext): boolean {
    switch (rule.type) {
      case 'user':
        return this.evaluateUserRule(rule, context);

      case 'percentage':
        return this.evaluatePercentageRule(rule, context);

      case 'attribute':
        return this.evaluateAttributeRule(rule, context);

      case 'datetime':
        return this.evaluateDateTimeRule(rule, context);

      default:
        return false;
    }
  }

  private evaluateUserRule(rule: FlagRule, context: EvaluationContext): boolean {
    if (!context.userId) return false;

    return rule.values.includes(context.userId);
  }

  private evaluatePercentageRule(rule: FlagRule, context: EvaluationContext): boolean {
    const hash = this.hashContext(context);
    const percentage = (hash % 100) + 1;

    return percentage <= rule.values[0];
  }

  private evaluateAttributeRule(rule: FlagRule, context: EvaluationContext): boolean {
    if (!rule.attribute || !context.attributes) return false;

    const value = context.attributes[rule.attribute];

    switch (rule.operator) {
      case 'equals':
        return rule.values.includes(value);

      case 'contains':
        return rule.values.some(v => String(value).includes(v));

      case 'gt':
        return value > rule.values[0];

      case 'lt':
        return value < rule.values[0];

      default:
        return false;
    }
  }

  private evaluateDateTimeRule(rule: FlagRule, context: EvaluationContext): boolean {
    const now = context.timestamp || Date.now();

    if (rule.operator === 'between') {
      return now >= rule.values[0] && now <= rule.values[1];
    }

    return false;
  }

  private selectVariant(variants: FlagVariant[], context: EvaluationContext): any {
    const hash = this.hashContext(context);
    const totalWeight = variants.reduce((sum, v) => sum + v.weight, 0);
    const position = hash % totalWeight;

    let cumulative = 0;
    for (const variant of variants) {
      cumulative += variant.weight;
      if (position < cumulative) {
        return variant.value;
      }
    }

    return variants[0].value;
  }

  private hashContext(context: EvaluationContext): number {
    const str = context.userId || context.email || 'anonymous';
    let hash = 0;

    for (let i = 0; i < str.length; i++) {
      const char = str.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash;
    }

    return Math.abs(hash);
  }

  async createFlag(config: Omit<FlagConfig, 'createdAt' | 'updatedAt'>): Promise<void> {
    this.flags.set(config.key, {
      ...config,
      createdAt: new Date(),
      updatedAt: new Date()
    });
  }

  async updateFlag(key: string, updates: Partial<FlagConfig>): Promise<void> {
    const flag = this.flags.get(key);
    if (!flag) {
      throw new Error(`Flag not found: ${key}`);
    }

    this.flags.set(key, {
      ...flag,
      ...updates,
      updatedAt: new Date()
    });
  }

  async deleteFlag(key: string): Promise<void> {
    this.flags.delete(key);
  }

  getAllFlags(): FlagConfig[] {
    return Array.from(this.flags.values());
  }
}

// Usage
const featureFlags = new FeatureFlagService();

// Simple boolean check
if (featureFlags.isEnabled('new-dashboard', { userId: 'user123' })) {
  console.log('Show new dashboard');
}

// With user attributes
const hasPremiumFeatures = featureFlags.isEnabled('premium-features', {
  userId: 'user123',
  attributes: { plan: 'premium' }
});

// Get variant for A/B testing
const buttonColor = featureFlags.getVariant('button-color-test', {
  userId: 'user123'
});
```

### 2. **React Hook for Feature Flags**

```typescript
import { createContext, useContext, ReactNode } from 'react';

interface FeatureFlagContextType {
  isEnabled: (key: string) => boolean;
  getVariant: (key: string) => any;
}

const FeatureFlagContext = createContext<FeatureFlagContextType | null>(null);

export function FeatureFlagProvider({
  children,
  userId,
  attributes
}: {
  children: ReactNode;
  userId?: string;
  attributes?: Record<string, any>;
}) {
  const flagService = new FeatureFlagService();

  const context: FeatureFlagContextType = {
    isEnabled: (key: string) => {
      return flagService.isEnabled(key, { userId, attributes });
    },
    getVariant: (key: string) => {
      return flagService.getVariant(key, { userId, attributes });
    }
  };

  return (
    <FeatureFlagContext.Provider value={context}>
      {children}
    </FeatureFlagContext.Provider>
  );
}

export function useFeatureFlag(key: string): boolean {
  const context = useContext(FeatureFlagContext);
  if (!context) {
    throw new Error('useFeatureFlag must be used within FeatureFlagProvider');
  }
  return context.isEnabled(key);
}

export function useFeatureVariant(key: string): any {
  const context = useContext(FeatureFlagContext);
  if (!context) {
    throw new Error('useFeatureVariant must be used within FeatureFlagProvider');
  }
  return context.getVariant(key);
}

// Feature component wrapper
export function Feature({
  flag,
  fallback = null,
  children
}: {
  flag: string;
  fallback?: ReactNode;
  children: ReactNode;
}) {
  const isEnabled = useFeatureFlag(flag);

  return isEnabled ? <>{children}</> : <>{fallback}</>;
}

// Usage in components
function Dashboard() {
  const hasNewDashboard = useFeatureFlag('new-dashboard');
  const theme = useFeatureVariant('theme-experiment');

  return (
    <div>
      {hasNewDashboard ? <NewDashboard /> : <OldDashboard />}

      <Feature flag="premium-features" fallback={<UpgradePrompt />}>
        <PremiumContent />
      </Feature>

      <div style={{ backgroundColor: theme?.backgroundColor }}>
        Content with experiment theme
      </div>
    </div>
  );
}
```

### 3. **Feature Flag with Analytics**

```typescript
interface FlagEvaluationEvent {
  flagKey: string;
  userId?: string;
  result: boolean;
  variant?: any;
  timestamp: number;
  duration: number;
}

class FeatureFlagServiceWithAnalytics extends FeatureFlagService {
  private analytics: Analytics;

  constructor(analytics: Analytics) {
    super();
    this.analytics = analytics;
  }

  isEnabled(flagKey: string, context: EvaluationContext = {}): boolean {
    const startTime = Date.now();
    const result = super.isEnabled(flagKey, context);
    const duration = Date.now() - startTime;

    this.trackEvaluation({
      flagKey,
      userId: context.userId,
      result,
      timestamp: Date.now(),
      duration
    });

    return result;
  }

  getVariant(flagKey: string, context: EvaluationContext = {}): any {
    const startTime = Date.now();
    const variant = super.getVariant(flagKey, context);
    const duration = Date.now() - startTime;

    this.trackEvaluation({
      flagKey,
      userId: context.userId,
      result: variant !== null,
      variant,
      timestamp: Date.now(),
      duration
    });

    return variant;
  }

  private trackEvaluation(event: FlagEvaluationEvent): void {
    this.analytics.track('feature_flag_evaluated', {
      flag_key: event.flagKey,
      user_id: event.userId,
      result: event.result,
      variant: event.variant,
      duration_ms: event.duration
    });
  }

  async getAnalytics(flagKey: string, timeRange: { start: Date; end: Date }): Promise<{
    evaluations: number;
    uniqueUsers: number;
    enabledRate: number;
    variantDistribution: Record<string, number>;
  }> {
    return this.analytics.getFlagAnalytics(flagKey, timeRange);
  }
}
```

### 4. **LaunchDarkly-Style SDK**

```python
from typing import Dict, Any, Optional
import hashlib
import json

class FeatureFlagClient:
    def __init__(self, sdk_key: str, config: Optional[Dict] = None):
        self.sdk_key = sdk_key
        self.config = config or {}
        self.flags: Dict[str, Dict] = {}
        self.initialize()

    def initialize(self):
        """Load flags from API or cache."""
        # In production, fetch from API
        self.flags = {
            'new-feature': {
                'enabled': True,
                'rollout': {
                    'percentage': 50
                }
            },
            'premium-feature': {
                'enabled': True,
                'targeting': {
                    'attribute': 'plan',
                    'values': ['premium', 'enterprise']
                }
            }
        }

    def variation(
        self,
        flag_key: str,
        user: Dict[str, Any],
        default: bool = False
    ) -> bool:
        """Evaluate flag for user."""
        flag = self.flags.get(flag_key)

        if not flag or not flag.get('enabled'):
            return default

        # Check targeting rules
        if 'targeting' in flag:
            if not self._evaluate_targeting(flag['targeting'], user):
                return False

        # Check percentage rollout
        if 'rollout' in flag:
            return self._evaluate_rollout(flag['rollout'], user, flag_key)

        return True

    def variation_detail(
        self,
        flag_key: str,
        user: Dict[str, Any],
        default: Any = None
    ) -> Dict[str, Any]:
        """Get flag variation with details."""
        value = self.variation(flag_key, user, default)

        return {
            'value': value,
            'variation_index': 0 if value else 1,
            'reason': {
                'kind': 'RULE_MATCH' if value else 'OFF'
            }
        }

    def _evaluate_targeting(self, targeting: Dict, user: Dict) -> bool:
        """Evaluate targeting rules."""
        attribute = targeting.get('attribute')
        values = targeting.get('values', [])

        user_value = user.get(attribute)
        return user_value in values

    def _evaluate_rollout(
        self,
        rollout: Dict,
        user: Dict,
        flag_key: str
    ) -> bool:
        """Evaluate percentage rollout."""
        percentage = rollout.get('percentage', 0)
        user_id = user.get('id', user.get('email', 'anonymous'))

        # Consistent hashing for stable rollout
        hash_value = self._hash_user(user_id, flag_key)
        bucket = hash_value % 100

        return bucket < percentage

    def _hash_user(self, user_id: str, flag_key: str) -> int:
        """Hash user ID for consistent bucketing."""
        combined = f"{flag_key}:{user_id}"
        hash_bytes = hashlib.sha256(combined.encode()).digest()
        return int.from_bytes(hash_bytes[:4], byteorder='big')

    def track(self, event_name: str, user: Dict, data: Optional[Dict] = None):
        """Track custom event."""
        # Send to analytics
        pass

    def identify(self, user: Dict):
        """Identify user."""
        # Update user context
        pass

    def flush(self):
        """Flush events."""
        pass

    def close(self):
        """Close client."""
        pass


# Usage
client = FeatureFlagClient(sdk_key='your-sdk-key')

user = {
    'id': 'user-123',
    'email': 'user@example.com',
    'plan': 'premium'
}

# Check if feature is enabled
if client.variation('new-feature', user):
    print("New feature enabled!")

# Get detailed information
detail = client.variation_detail('premium-feature', user)
print(f"Value: {detail['value']}, Reason: {detail['reason']}")

# Track event
client.track('feature-used', user, {'feature': 'new-feature'})
```

### 5. **Admin UI for Feature Flags**

```typescript
interface FlagFormData {
  key: string;
  description: string;
  enabled: boolean;
  rolloutPercentage?: number;
  targetUsers?: string[];
  targetAttributes?: Record<string, any>;
}

function FeatureFlagDashboard() {
  const [flags, setFlags] = useState<FlagConfig[]>([]);
  const flagService = new FeatureFlagService();

  useEffect(() => {
    loadFlags();
  }, []);

  const loadFlags = async () => {
    const allFlags = flagService.getAllFlags();
    setFlags(allFlags);
  };

  const toggleFlag = async (key: string) => {
    const flag = flags.find(f => f.key === key);
    if (flag) {
      await flagService.updateFlag(key, { enabled: !flag.enabled });
      await loadFlags();
    }
  };

  return (
    <div className="dashboard">
      <h1>Feature Flags</h1>

      <table>
        <thead>
          <tr>
            <th>Flag</th>
            <th>Description</th>
            <th>Status</th>
            <th>Rollout</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {flags.map(flag => (
            <tr key={flag.key}>
              <td>{flag.key}</td>
              <td>{flag.description}</td>
              <td>
                <Switch
                  checked={flag.enabled}
                  onChange={() => toggleFlag(flag.key)}
                />
              </td>
              <td>{getRolloutPercentage(flag)}%</td>
              <td>
                <button onClick={() => editFlag(flag)}>Edit</button>
                <button onClick={() => deleteFlag(flag.key)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
```

## Best Practices

### ✅ DO
- Use descriptive flag names
- Document flag purpose and lifecycle
- Implement gradual rollouts
- Track flag evaluations
- Clean up old flags regularly
- Use feature flags for experiments
- Implement kill switches for critical features
- Test both enabled and disabled states
- Use consistent hashing for stable rollouts
- Provide admin UI for non-technical users

### ❌ DON'T
- Use flags for permanent configuration
- Accumulate technical debt with old flags
- Skip flag cleanup
- Make flags too granular
- Hard-code flag checks everywhere
- Skip analytics and monitoring

## Resources

- [LaunchDarkly](https://launchdarkly.com/)
- [Split.io](https://www.split.io/)
- [Flagsmith](https://flagsmith.com/)
- [Unleash](https://www.getunleash.io/)
