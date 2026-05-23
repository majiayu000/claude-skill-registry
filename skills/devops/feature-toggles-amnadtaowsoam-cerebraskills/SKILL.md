---
name: Feature Toggles (Feature Flags)
description: Using runtime switches to enable or disable features without deploying new code, decoupling deployment from release and enabling gradual rollouts, A/B testing, and emergency feature disabling.
---

# Feature Toggles (Feature Flags)

> **Current Level:** Intermediate  
> **Domain:** DevOps / Feature Management

---

## Overview

Feature toggles are runtime switches that enable or disable features without deploying new code. They decouple deployment from release, enabling gradual rollouts, A/B testing, and emergency feature disabling without code changes.

## What are Feature Toggles

### Core Concept

```
┌─────────────────────────────────────────────────────────────────┐
│  Feature Toggle Concept                                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │  Code Deployed ──▶ Feature Toggle OFF ──▶ Feature Hidden │     │
│  └─────────────────────────────────────────────────────────┘     │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │  Code Deployed ──▶ Feature Toggle ON ──▶ Feature Visible│     │
│  └─────────────────────────────────────────────────────────┘     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Why Feature Toggles

| Benefit | Impact |
|---------|---------|
| **Trunk-Based Development** | No long-lived branches |
| **Dark Launches** | Deploy without activating |
| **Gradual Rollout** | Enable for 5%, 50%, 100% |
| **Kill Switch** | Disable if issues |
| **A/B Testing** | Test variants |

## Types of Feature Toggles

### Release Toggles

```javascript
// Release toggle (temporary)
function showNewCheckout() {
    if (featureEnabled('new-checkout')) {
        return <NewCheckout />;
    } else {
        return <OldCheckout />;
    }
}

// Usage
const checkout = showNewCheckout();
```

### Experiment Toggles

```javascript
// Experiment toggle (A/B testing)
function showCheckoutVariant() {
    const variant = getExperimentVariant('checkout-test');
    
    if (variant === 'A') {
        return <CheckoutVariantA />;
    } else {
        return <CheckoutVariantB />;
    }
}

// Usage
const checkout = showCheckoutVariant();
```

### Ops Toggles

```javascript
// Ops toggle (circuit breaker)
function makePayment() {
    if (featureEnabled('payments-enabled')) {
        return processPayment();
    } else {
        return showMaintenanceMessage();
    }
}

// Usage
const payment = makePayment();
```

### Permission Toggles

```javascript
// Permission toggle (user-based)
function showPremiumFeature() {
    if (userHasPermission('premium')) {
        return <PremiumFeature />;
    } else {
        return <UpgradePrompt />;
    }
}

// Usage
const feature = showPremiumFeature();
```

## Feature Toggle Implementation

### Simple Boolean Flag

```javascript
// Simple boolean flag
const featureFlags = {
    newCheckout: false,
    premiumFeature: true,
    paymentsEnabled: true
};

function featureEnabled(flag) {
    return featureFlags[flag] || false;
}

// Usage
if (featureEnabled('newCheckout')) {
    showNewCheckout();
}
```

### Config File

```json
// config/feature-flags.json
{
    "newCheckout": false,
    "premiumFeature": true,
    "paymentsEnabled": true
}
```

```javascript
// Load config file
const fs = require('fs');
const featureFlags = JSON.parse(fs.readFileSync('config/feature-flags.json'));

function featureEnabled(flag) {
    return featureFlags[flag] || false;
}

// Usage
if (featureEnabled('newCheckout')) {
    showNewCheckout();
}
```

### Database

```sql
-- Feature flags table
CREATE TABLE feature_flags (
    id SERIAL PRIMARY KEY,
    flag_name VARCHAR(255) NOT NULL UNIQUE,
    flag_value BOOLEAN NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Insert feature flags
INSERT INTO feature_flags (flag_name, flag_value)
VALUES ('newCheckout', false),
       ('premiumFeature', true),
       ('paymentsEnabled', true);
```

```javascript
// Load from database
async function loadFeatureFlags() {
    const result = await db.query('SELECT flag_name, flag_value FROM feature_flags');
    const featureFlags = {};
    
    result.rows.forEach(row => {
        featureFlags[row.flag_name] = row.flag_value;
    });
    
    return featureFlags;
}

async function featureEnabled(flag) {
    const featureFlags = await loadFeatureFlags();
    return featureFlags[flag] || false;
}

// Usage
if (await featureEnabled('newCheckout')) {
    showNewCheckout();
}
```

### Feature Flag Service

```javascript
// LaunchDarkly
const LaunchDarkly = require('ldclient-node');

const client = LaunchDarkly.init('sdk-key');

client.on('ready', () => {
    const flagValue = client.variation('new-checkout', false, {
        key: 'user-123'
    });
    
    if (flagValue) {
        showNewCheckout();
    } else {
        showOldCheckout();
    }
});
```

## Toggle Configuration

### Boolean Toggle

```javascript
// Boolean toggle (on/off)
const flagValue = client.variation('new-checkout', false, user);
```

### Percentage Rollout

```javascript
// Percentage rollout (20% of users)
const flagValue = client.variation('new-checkout', false, user, {
    percentage: 20
});
```

### User Targeting

```javascript
// User targeting (specific user IDs)
const flagValue = client.variation('new-checkout', false, user, {
    users: ['user-123', 'user-456']
});
```

### Segment Targeting

```javascript
// Segment targeting (beta users, paid users)
const flagValue = client.variation('new-checkout', false, user, {
    segments: ['beta', 'paid']
});
```

### Environment-Based

```javascript
// Environment-based (on in prod, off in staging)
const flagValue = client.variation('new-checkout', false, user, {
    environments: {
        production: true,
        staging: false
    }
});
```

## Toggle Evaluation

### Server-Side

```javascript
// Server-side evaluation
app.get('/checkout', (req, res) => {
    const flagValue = client.variation('new-checkout', false, req.user);
    
    if (flagValue) {
        res.send('<NewCheckout />');
    } else {
        res.send('<OldCheckout />');
    }
});
```

### Client-Side

```javascript
// Client-side evaluation
const flagValue = client.variation('new-checkout', false, user);

if (flagValue) {
    render(<NewCheckout />);
} else {
    render(<OldCheckout />);
}
```

### Hybrid

```javascript
// Hybrid evaluation (some server, some client)
app.get('/checkout', (req, res) => {
    const serverFlag = client.variation('payments-enabled', false, req.user);
    
    if (serverFlag) {
        res.send({
            checkout: 'new',
            payments: true
        });
    } else {
        res.send({
            checkout: 'old',
            payments: false
        });
    }
});
```

## Gradual Rollout with Toggles

### Dark Launch

```javascript
// Dark launch (code deployed but off)
function darkLaunch() {
    // Deploy code
    deployNewVersion();
    
    // Feature is off by default
    setFeatureFlag('new-checkout', false);
    
    // No users see new feature
    console.log('Dark launch: feature is off');
}

darkLaunch();
```

### Internal Users

```javascript
// Enable for internal users (dogfooding)
function enableForInternalUsers() {
    // Enable for internal users
    setFeatureFlag('new-checkout', true, {
        users: ['user-1@company.com', 'user-2@company.com']
    });
    
    console.log('Enabled for internal users');
}

enableForInternalUsers();
```

### Ramp to 5%

```javascript
// Ramp to 5% of users
function rampTo5Percent() {
    setFeatureFlag('new-checkout', true, {
        percentage: 5
    });
    
    console.log('Ramped to 5%');
}

rampTo5Percent();
```

### Ramp to 50%

```javascript
// Ramp to 50% of users
function rampTo50Percent() {
    setFeatureFlag('new-checkout', true, {
        percentage: 50
    });
    
    console.log('Ramped to 50%');
}

rampTo50Percent();
```

### Ramp to 100%

```javascript
// Ramp to 100% of users
function rampTo100Percent() {
    setFeatureFlag('new-checkout', true, {
        percentage: 100
    });
    
    console.log('Ramped to 100%');
}

rampTo100Percent();
```

### Remove Toggle

```javascript
// Remove toggle after full rollout
function removeToggle() {
    // Remove feature flag code
    // Always show new feature
    // Clean up old code
    
    console.log('Toggle removed');
}

removeToggle();
```

## A/B Testing with Toggles

### Variant A (50%)

```javascript
// Variant A (50% of users)
const variantA = client.variation('checkout-test', 'A', user);

if (variantA === 'A') {
    render(<CheckoutVariantA />);
}
```

### Variant B (50%)

```javascript
// Variant B (50% of users)
const variantB = client.variation('checkout-test', 'B', user);

if (variantB === 'B') {
    render(<CheckoutVariantB />);
}
```

### Measure Metrics

```javascript
// Track metrics for each variant
function trackCheckoutEvent(variant, event) {
    analytics.track({
        event: event,
        variant: variant,
        user: user.id
    });
}

// Usage
const variant = client.variation('checkout-test', 'A', user);
renderCheckout(variant);
trackCheckoutEvent(variant, 'checkout_viewed');
```

### Determine Winner

```javascript
// Determine winner based on metrics
function determineWinner() {
    const metrics = analytics.getMetrics('checkout-test');
    
    const conversionA = metrics.A.conversionRate;
    const conversionB = metrics.B.conversionRate;
    
    if (conversionA > conversionB) {
        return 'A';
    } else {
        return 'B';
    }
}

// Usage
const winner = determineWinner();
setFeatureFlag('checkout-test', winner);
```

## Kill Switch

### Disable Feature

```javascript
// Kill switch: disable feature if issues
function killSwitch() {
    setFeatureFlag('payments-enabled', false);
    
    console.log('Payments disabled');
}

killSwitch();
```

### No Redeployment

```javascript
// No redeployment needed
function disableFeatureWithoutRedeploy() {
    // Disable feature
    setFeatureFlag('new-checkout', false);
    
    // No code changes needed
    // No redeployment needed
    
    console.log('Feature disabled');
}

disableFeatureWithoutRedeploy();
```

## Toggle Lifecycle

### Create Toggle

```javascript
// Create toggle for new feature
function createToggle() {
    setFeatureFlag('new-checkout', false);
    
    console.log('Toggle created');
}

createToggle();
```

### Use During Development

```javascript
// Use toggle during development
function useDuringDevelopment() {
    // Toggle is off by default
    setFeatureFlag('new-checkout', false);
    
    // Developers can enable locally
    if (process.env.NODE_ENV === 'development') {
        setFeatureFlag('new-checkout', true);
    }
}

useDuringDevelopment();
```

### Enable Gradually

```javascript
// Enable gradually
function enableGradually() {
    // Enable for 5% of users
    setFeatureFlag('new-checkout', true, { percentage: 5 });
    
    // Wait and monitor
    setTimeout(() => {
        // Enable for 25% of users
        setFeatureFlag('new-checkout', true, { percentage: 25 });
        
        // Wait and monitor
        setTimeout(() => {
            // Enable for 50% of users
            setFeatureFlag('new-checkout', true, { percentage: 50 });
            
            // Wait and monitor
            setTimeout(() => {
                // Enable for 100% of users
                setFeatureFlag('new-checkout', true, { percentage: 100 });
            }, 3600000); // 1 hour
        }, 3600000); // 1 hour
    }, 3600000); // 1 hour
}

enableGradually();
```

### Feature Fully Released

```javascript
// Feature fully released
function featureFullyReleased() {
    // All users see new feature
    setFeatureFlag('new-checkout', true, { percentage: 100 });
    
    console.log('Feature fully released');
}

featureFullyReleased();
```

### Remove Toggle

```javascript
// Remove toggle after full rollout
function removeToggle() {
    // Remove feature flag code
    // Always show new feature
    // Clean up old code
    
    console.log('Toggle removed');
}

removeToggle();
```

## Toggle Debt

### Old Toggles

```javascript
// Old toggles = complexity
function oldToggles() {
    // Many old toggles in code
    if (featureEnabled('old-feature-1')) { /* ... */ }
    if (featureEnabled('old-feature-2')) { /* ... */ }
    if (featureEnabled('old-feature-3')) { /* ... */ }
    // ... many more
}

oldToggles();
```

### Regular Cleanup

```javascript
// Regular cleanup: remove old toggles
function cleanupOldToggles() {
    // Remove old feature flag code
    // Clean up old code
    
    console.log('Old toggles removed');
}

cleanupOldToggles();
```

### Expiration Dates

```javascript
// Set expiration dates on toggles
function setExpirationDate() {
    setFeatureFlag('new-checkout', true, {
        expirationDate: '2024-12-31'
    });
    
    console.log('Expiration date set');
}

setExpirationDate();
```

## Feature Flag Services

### LaunchDarkly

```javascript
// LaunchDarkly
const LaunchDarkly = require('ldclient-node');

const client = LaunchDarkly.init('sdk-key');

client.on('ready', () => {
    const flagValue = client.variation('new-checkout', false, {
        key: 'user-123'
    });
    
    if (flagValue) {
        showNewCheckout();
    } else {
        showOldCheckout();
    }
});
```

### Split.io

```javascript
// Split.io
const SplitFactory = require('@splitsoftware/splitio').SplitFactory;

const factory = SplitFactory({
    core: {
        authorizationKey: 'sdk-key'
    }
});

const client = factory.client();

client.on(client.Event.SDK_READY, () => {
    const treatment = client.getTreatment('new-checkout', 'user-123');
    
    if (treatment === 'on') {
        showNewCheckout();
    } else {
        showOldCheckout();
    }
});
```

### Unleash

```javascript
// Unleash
const unleash = require('unleash-client');

unleash.initialize({
    url: 'https://unleash.example.com/api',
    appName: 'my-app',
    instanceId: 'my-instance-id'
});

unleash.on('ready', () => {
    if (unleash.isEnabled('new-checkout')) {
        showNewCheckout();
    } else {
        showOldCheckout();
    }
});
```

### Flagsmith

```javascript
// Flagsmith
const Flagsmith = require('flagsmith-nodejs-sdk');

const flagsmith = new Flagsmith({
    environmentKey: 'env-key'
});

flagsmith.getEnvironmentFlags().then(flags => {
    const newCheckout = flags.isFeatureEnabled('new-checkout');
    
    if (newCheckout) {
        showNewCheckout();
    } else {
        showOldCheckout();
    }
});
```

### ConfigCat

```javascript
// ConfigCat
const ConfigCatClient = require('configcat-node');

const client = ConfigCatClient.get('sdk-key');

client.getValueAsync('new-checkout', false, user).then(value => {
    if (value) {
        showNewCheckout();
    } else {
        showOldCheckout();
    }
});
```

## DIY Feature Flags

### Config File

```javascript
// Config file (simple, requires redeploy)
const fs = require('fs');

function loadFeatureFlags() {
    const config = JSON.parse(fs.readFileSync('config/feature-flags.json'));
    return config;
}

function featureEnabled(flag) {
    const flags = loadFeatureFlags();
    return flags[flag] || false;
}

// Usage
if (featureEnabled('new-checkout')) {
    showNewCheckout();
}
```

### Database

```javascript
// Database table (dynamic, adds latency)
async function loadFeatureFlags() {
    const result = await db.query('SELECT flag_name, flag_value FROM feature_flags');
    const flags = {};
    
    result.rows.forEach(row => {
        flags[row.flag_name] = row.flag_value;
    });
    
    return flags;
}

async function featureEnabled(flag) {
    const flags = await loadFeatureFlags();
    return flags[flag] || false;
}

// Usage
if (await featureEnabled('new-checkout')) {
    showNewCheckout();
}
```

### Redis

```javascript
// Redis (fast, requires Redis)
const redis = require('redis');
const client = redis.createClient();

async function loadFeatureFlags() {
    const flags = await client.hgetall('feature-flags');
    return flags;
}

async function featureEnabled(flag) {
    const flags = await loadFeatureFlags();
    return flags[flag] === 'true';
}

// Usage
if (await featureEnabled('new-checkout')) {
    showNewCheckout();
}
```

## Performance Considerations

### Cache Flag Values

```javascript
// Cache flag values (don't query every request)
const flagCache = new Map();

async function featureEnabled(flag) {
    // Check cache first
    if (flagCache.has(flag)) {
        return flagCache.get(flag);
    }
    
    // Load from source
    const value = await loadFlagValue(flag);
    
    // Cache the value
    flagCache.set(flag, value);
    
    // Invalidate cache after 5 minutes
    setTimeout(() => {
        flagCache.delete(flag);
    }, 300000);
    
    return value;
}

// Usage
if (await featureEnabled('new-checkout')) {
    showNewCheckout();
}
```

### Evaluate Once Per Request

```javascript
// Evaluate flags once per request
app.use((req, res, next) => {
    req.flags = {};
    next();
});

app.get('/checkout', (req, res) => {
    // Evaluate flag once
    if (!req.flags.newCheckout) {
        req.flags.newCheckout = client.variation('new-checkout', false, req.user);
    }
    
    if (req.flags.newCheckout) {
        res.send('<NewCheckout />');
    } else {
        res.send('<OldCheckout />');
    }
});
```

### Minimal Overhead

```javascript
// Minimal overhead: use in-memory cache
const flagCache = new Map();

function featureEnabled(flag) {
    // In-memory cache (fastest)
    return flagCache.get(flag) || false;
}

// Load flags on startup
async function loadFlags() {
    const flags = await loadFeatureFlags();
    
    Object.entries(flags).forEach(([key, value]) => {
        flagCache.set(key, value);
    });
}

loadFlags();

// Usage
if (featureEnabled('new-checkout')) {
    showNewCheckout();
}
```

## Testing with Toggles

### Test Both Paths

```javascript
// Test both paths (on and off)
describe('New Checkout', () => {
    it('shows new checkout when flag is on', () => {
        setFeatureFlag('new-checkout', true);
        const checkout = showNewCheckout();
        expect(checkout).toBe('<NewCheckout />');
    });
    
    it('shows old checkout when flag is off', () => {
        setFeatureFlag('new-checkout', false);
        const checkout = showNewCheckout();
        expect(checkout).toBe('<OldCheckout />');
    });
});
```

### Integration Tests

```javascript
// Integration tests with toggles enabled/disabled
describe('Checkout Integration', () => {
    it('processes payment when flag is on', async () => {
        setFeatureFlag('payments-enabled', true);
        const result = await processPayment();
        expect(result.success).toBe(true);
    });
    
    it('shows maintenance message when flag is off', async () => {
        setFeatureFlag('payments-enabled', false);
        const result = await processPayment();
        expect(result.message).toBe('Maintenance mode');
    });
});
```

### Feature Branch Testing

```javascript
// Feature branch testing (toggle on)
describe('Feature Branch Tests', () => {
    beforeEach(() => {
        setFeatureFlag('new-checkout', true);
    });
    
    it('tests new checkout flow', () => {
        // Test new checkout flow
    });
});
```

## Multi-Variate Flags

### Multiple Variants

```javascript
// Multi-variate flags (not just on/off)
const variant = client.variation('new-ui', 'v1', user);

if (variant === 'v1') {
    render(<UIVariant1 />);
} else if (variant === 'v2') {
    render(<UIVariant2 />);
} else if (variant === 'v3') {
    render(<UIVariant3 />);
}
```

### A/B/C Testing

```javascript
// A/B/C testing
const variant = client.variation('checkout-test', 'A', user);

if (variant === 'A') {
    render(<CheckoutVariantA />);
} else if (variant === 'B') {
    render(<CheckoutVariantB />);
} else if (variant === 'C') {
    render(<CheckoutVariantC />);
}
```

## Toggle Best Practices

### Short-Lived Release Toggles

```javascript
// Short-lived release toggles (remove after rollout)
function shortLivedToggle() {
    // Create toggle
    setFeatureFlag('new-checkout', false);
    
    // Use during rollout
    // Remove after full rollout
    
    console.log('Toggle will be removed after rollout');
}

shortLivedToggle();
```

### Long-Lived Permission Toggles

```javascript
// Long-lived permission toggles (for plans)
function longLivedToggle() {
    // Permission toggles stay
    setFeatureFlag('premium-feature', true, {
        segments: ['premium']
    });
    
    console.log('Permission toggle stays for premium users');
}

longLivedToggle();
```

### Descriptive Names

```javascript
// Descriptive names (new-checkout, not flag-123)
function descriptiveNames() {
    setFeatureFlag('new-checkout', false); // Good
    setFeatureFlag('flag-123', false); // Bad
}

descriptiveNames();
```

### Default to Off

```javascript
// Default to off (safe default)
function defaultToOff() {
    setFeatureFlag('new-checkout', false); // Safe default
    
    console.log('Default to off (safe)');
}

defaultToOff();
```

## Toggle Anti-Patterns

### Toggle Everywhere

```javascript
// Toggle everywhere (overuse)
function toggleEverywhere() {
    // Too many toggles
    if (featureEnabled('flag-1')) { /* ... */ }
    if (featureEnabled('flag-2')) { /* ... */ }
    if (featureEnabled('flag-3')) { /* ... */ }
    // ... many more
}

toggleEverywhere();
```

### Not Removing Old Toggles

```javascript
// Not removing old toggles (debt)
function notRemovingOldToggles() {
    // Old toggles accumulate
    if (featureEnabled('old-feature-1')) { /* ... */ }
    if (featureEnabled('old-feature-2')) { /* ... */ }
    // ... many old toggles
}

notRemovingOldToggles();
```

### Complex Toggle Logic

```javascript
// Complex toggle logic (if A && B && !C...)
function complexToggleLogic() {
    // Too complex
    if (featureEnabled('flag-A') && featureEnabled('flag-B') && !featureEnabled('flag-C')) {
        // ...
    }
}

complexToggleLogic();
```

## Real Examples

### Feature Rollout with LaunchDarkly

```javascript
// Feature rollout with LaunchDarkly
const LaunchDarkly = require('ldclient-node');

const client = LaunchDarkly.init('sdk-key');

client.on('ready', () => {
    // Dark launch (off by default)
    const flagValue = client.variation('new-checkout', false, user);
    
    // Enable for internal users
    client.variation('new-checkout', false, {
        key: 'user-1@company.com'
    });
    
    // Ramp to 5%
    client.variation('new-checkout', false, user, {
        percentage: 5
    });
    
    // Ramp to 50%
    client.variation('new-checkout', false, user, {
        percentage: 50
    });
    
    // Ramp to 100%
    client.variation('new-checkout', false, user, {
        percentage: 100
    });
});
```

### A/B Test with Feature Flags

```javascript
// A/B test with feature flags
const variant = client.variation('checkout-test', 'A', user);

if (variant === 'A') {
    render(<CheckoutVariantA />);
    analytics.track('checkout_variant_A_viewed');
} else {
    render(<CheckoutVariantB />);
    analytics.track('checkout_variant_B_viewed');
}

// Determine winner
const metrics = analytics.getMetrics('checkout-test');
if (metrics.A.conversionRate > metrics.B.conversionRate) {
    setFeatureFlag('checkout-test', 'A');
} else {
    setFeatureFlag('checkout-test', 'B');
}
```

### Kill Switch for Critical Feature

```javascript
// Kill switch for critical feature
function killSwitch() {
    // Disable payments if issues
    if (paymentGatewayDown) {
        setFeatureFlag('payments-enabled', false);
        console.log('Payments disabled');
    }
}

// Monitor payment gateway
setInterval(() => {
    const status = checkPaymentGatewayStatus();
    if (status !== 'healthy') {
        killSwitch();
    }
}, 60000); // Check every minute
```

## Summary Checklist

### Planning

- [ ] Feature toggle strategy defined
- [ ] Toggle types identified
- [ ] Rollout plan documented
- [ ] Rollback plan documented
- [ ] Cleanup plan documented

### Implementation

- [ ] Toggle system chosen
- [ ] Toggle implementation complete
- [ ] Toggle configuration set up
- [ ] Toggle evaluation implemented
- [ ] Toggle caching implemented

### Rollout

- [ ] Dark launch (toggle off)
- [ ] Enable for internal users
- [ ] Ramp to 5%
- [ ] Ramp to 25%
- [ ] Ramp to 50%
- [ ] Ramp to 100%

### Testing

- [ ] Test both paths (on and off)
- [ ] Integration tests complete
- [ ] Feature branch tests complete
- [ ] Performance tests complete
```

---

## Quick Start

### LaunchDarkly Integration

```javascript
const LaunchDarkly = require('launchdarkly-node-server-sdk')

const client = LaunchDarkly.init(process.env.LAUNCHDARKLY_SDK_KEY)

// Check feature flag
const flagValue = await client.variation('new-checkout-flow', user, false)
if (flagValue) {
  // New checkout flow
} else {
  // Old checkout flow
}
```

### Custom Feature Toggle

```typescript
interface FeatureToggle {
  name: string
  enabled: boolean
  percentage?: number
  userIds?: string[]
}

class FeatureToggleService {
  async isEnabled(toggleName: string, userId: string): Promise<boolean> {
    const toggle = await db.featureToggles.findUnique({
      where: { name: toggleName }
    })
    
    if (!toggle || !toggle.enabled) return false
    
    // Percentage rollout
    if (toggle.percentage) {
      const hash = this.hashUserId(userId)
      return hash % 100 < toggle.percentage
    }
    
    // User list
    if (toggle.userIds?.includes(userId)) {
      return true
    }
    
    return false
  }
}
```

---

## Production Checklist

- [ ] **Toggle Service**: Set up feature toggle service
- [ ] **Toggle Management**: UI for managing toggles
- [ ] **Gradual Rollout**: Support percentage-based rollout
- [ ] **User Targeting**: Support user-specific toggles
- [ ] **Monitoring**: Monitor toggle usage and impact
- [ ] **Documentation**: Document each feature toggle
- [ ] **Cleanup**: Remove toggles after feature is stable
- [ ] **Testing**: Test with toggles on/off
- [ ] **Fallback**: Fallback behavior when toggle fails
- [ ] **Performance**: Minimal performance impact
- [ ] **Security**: Secure toggle configuration
- [ ] **Audit**: Audit log of toggle changes

---

## Anti-patterns

### ❌ Don't: Toggle Debt

```typescript
// ❌ Bad - Toggle never removed
if (featureToggle('old-feature')) {
  // Old code still here!
}
```

```typescript
// ✅ Good - Remove after feature stable
// Toggle removed after 2 weeks of 100% rollout
// Old code removed
```

### ❌ Don't: No Fallback

```typescript
// ❌ Bad - No fallback
const value = await getToggle('feature')
if (value) {
  newFeature()  // What if toggle service fails?
}
```

```typescript
// ✅ Good - Fallback to safe default
const value = await getToggle('feature').catch(() => false)  // Default: off
if (value) {
  newFeature()
} else {
  oldFeature()  // Safe fallback
}
```

---

## Integration Points

- **Canary Deployment** (`26-deployment-strategies/canary-deployment/`) - Gradual rollout
- **A/B Testing** (`23-business-analytics/ab-testing-analysis/`) - Feature testing
- **Monitoring** (`14-monitoring-observability/`) - Toggle monitoring

---

## Further Reading

- [Feature Toggles (Martin Fowler)](https://martinfowler.com/articles/feature-toggles.html)
- [LaunchDarkly Documentation](https://docs.launchdarkly.com/)
- [Unleash Feature Flags](https://www.getunleash.io/)

### Cleanup

- [ ] Remove old toggles
- [ ] Clean up old code
- [ ] Update documentation
- [ ] Archive toggle history
