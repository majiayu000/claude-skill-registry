---
name: cloud-payments
description: Flow Nexus credit management and billing operations. Use for checking balances, purchasing credits, configuring auto-refill, and tracking transactions.
version: 1.0.0
category: cloud
type: skill
capabilities:
  - balance_checking
  - credit_purchasing
  - auto_refill_configuration
  - transaction_history
  - tier_management
  - usage_analytics
tools:
  - mcp__flow-nexus__check_balance
  - mcp__flow-nexus__ruv_balance
  - mcp__flow-nexus__ruv_history
  - mcp__flow-nexus__create_payment_link
  - mcp__flow-nexus__configure_auto_refill
  - mcp__flow-nexus__get_payment_history
  - mcp__flow-nexus__user_upgrade
  - mcp__flow-nexus__user_stats
  - mcp__flow-nexus__app_store_earn_ruv
related_skills:
  - cloud-auth
  - cloud-challenges
  - cloud-app-store
---

# Cloud Payments

> Manage rUv credits, billing, and financial operations within the Flow Nexus ecosystem.

## Quick Start

```javascript
// Check current balance
const balance = await mcp__flow-nexus__check_balance();
console.log(`Credits: ${balance.credits}, Auto-refill: ${balance.auto_refill}`);

// Purchase credits
const paymentLink = await mcp__flow-nexus__create_payment_link({
  amount: 50  // USD minimum $10
});

// Configure auto-refill
await mcp__flow-nexus__configure_auto_refill({
  enabled: true,
  threshold: 100,
  amount: 50
});

// View transaction history
const history = await mcp__flow-nexus__ruv_history({
  user_id: "user_id",
  limit: 20
});
```

## When to Use

- Checking current credit balance before operations
- Purchasing credits for platform usage
- Setting up automatic credit refill
- Tracking spending and transaction history
- Managing subscription tiers
- Understanding cost optimization strategies
- Tracking earnings from published apps

## Prerequisites

- Flow Nexus account with active session
- Payment method for credit purchases
- User authentication completed

## Core Concepts

### rUv Credits

rUv credits are the platform currency used for:
- Sandbox execution time
- Neural network training
- Agent deployment
- Template deployments
- API calls

### Pricing Tiers

| Tier | Monthly Credits | Price | Features |
|------|-----------------|-------|----------|
| **Free** | 100 | $0 | Basic features, community support |
| **Pro** | 1,000 | $29/month | Priority access, email support |
| **Enterprise** | Unlimited | Custom | Dedicated resources, SLA |

### Credit Earning Opportunities

| Activity | Credits |
|----------|---------|
| Challenge completion (beginner) | 10-50 |
| Challenge completion (advanced) | 100-500 |
| Template publishing (per use) | Revenue share |
| Referrals | Bonus credits |
| Daily engagement | Small bonuses |
| Achievements | Milestone rewards |

## MCP Tools Reference

### Balance Checking

```javascript
// Quick balance check
mcp__flow-nexus__check_balance()
// Returns: { credits, auto_refill, threshold, tier }

// Detailed balance for user
mcp__flow-nexus__ruv_balance({
  user_id: "user_id"
})
// Returns: { credits, pending, earned_total, spent_total }
```

### Credit Purchase

```javascript
mcp__flow-nexus__create_payment_link({
  amount: 50                 // USD (minimum $10, max $10,000)
})
// Returns: { payment_url, expires_at, credits_amount }
```

### Auto-Refill Configuration

```javascript
mcp__flow-nexus__configure_auto_refill({
  enabled: true,             // Enable/disable
  threshold: 100,            // Trigger when credits fall below
  amount: 50                 // Amount in USD to refill
})
// Returns: { enabled, threshold, amount, next_charge }
```

### Transaction History

```javascript
// rUv credit transactions
mcp__flow-nexus__ruv_history({
  user_id: "user_id",
  limit: 50                  // Max 100
})
// Returns: { transactions: [{ date, amount, type, description }] }

// Payment history
mcp__flow-nexus__get_payment_history({
  limit: 10                  // Max 100
})
// Returns: { payments: [{ date, amount, status, invoice_url }] }
```

### Tier Management

```javascript
mcp__flow-nexus__user_upgrade({
  user_id: "user_id",
  tier: "pro"                // pro or enterprise
})
// Returns: { new_tier, monthly_credits, effective_date }
```

### Credit Earning

```javascript
// Award credits (for app creators, challenge completion, etc.)
mcp__flow-nexus__app_store_earn_ruv({
  user_id: "user_id",
  amount: 100,
  reason: "Challenge completion: Advanced Algorithm",
  source: "challenge"        // challenge, app_usage, referral
})
```

### Usage Statistics

```javascript
mcp__flow-nexus__user_stats({
  user_id: "user_id"
})
// Returns: { credits_earned, credits_spent, apps_published, challenges_completed }
```

## Usage Examples

### Example 1: Balance Management

```javascript
// Check current balance
const balance = await mcp__flow-nexus__check_balance();

console.log(`
Current Balance: ${balance.credits} credits
Tier: ${balance.tier}
Auto-refill: ${balance.auto_refill ? 'Enabled' : 'Disabled'}
`);

// If balance is low, show warning
if (balance.credits < 100) {
  console.log("Warning: Low balance! Consider adding credits.");

  // Create payment link
  const payment = await mcp__flow-nexus__create_payment_link({
    amount: 50
  });

  console.log(`Purchase credits: ${payment.payment_url}`);
  console.log(`This will add ${payment.credits_amount} credits`);
}
```

### Example 2: Setting Up Auto-Refill

```javascript
// Check current auto-refill status
const balance = await mcp__flow-nexus__check_balance();

if (!balance.auto_refill) {
  // Configure auto-refill to prevent service interruption
  await mcp__flow-nexus__configure_auto_refill({
    enabled: true,
    threshold: 100,          // Refill when below 100 credits
    amount: 50               // Add $50 worth of credits
  });

  console.log("Auto-refill configured:");
  console.log("- Trigger: When balance falls below 100 credits");
  console.log("- Amount: $50 (~500 credits)");
}

// To disable auto-refill
// await mcp__flow-nexus__configure_auto_refill({ enabled: false });
```

### Example 3: Tracking Usage and Spending

```javascript
// Get user statistics
const stats = await mcp__flow-nexus__user_stats({
  user_id: "your_user_id"
});

console.log(`
=== Usage Summary ===
Credits Earned: ${stats.credits_earned}
Credits Spent: ${stats.credits_spent}
Net Balance Change: ${stats.credits_earned - stats.credits_spent}
`);

// Get detailed transaction history
const history = await mcp__flow-nexus__ruv_history({
  user_id: "your_user_id",
  limit: 20
});

console.log("\nRecent Transactions:");
for (const tx of history.transactions) {
  const sign = tx.amount > 0 ? '+' : '';
  console.log(`${tx.date}: ${sign}${tx.amount} - ${tx.description}`);
}

// Get payment history
const payments = await mcp__flow-nexus__get_payment_history({
  limit: 10
});

console.log("\nRecent Payments:");
for (const payment of payments.payments) {
  console.log(`${payment.date}: $${payment.amount} - ${payment.status}`);
}
```

### Example 4: Tier Upgrade

```javascript
// Check current tier and credits
const balance = await mcp__flow-nexus__check_balance();

console.log(`Current tier: ${balance.tier}`);

// Compare tiers
const tierComparison = {
  free: { credits: 100, price: 0 },
  pro: { credits: 1000, price: 29 },
  enterprise: { credits: "Unlimited", price: "Custom" }
};

if (balance.tier === "free") {
  console.log("\nUpgrade Benefits:");
  console.log("- Pro: 10x more credits (1000/month) for $29/month");
  console.log("- Priority access to new features");
  console.log("- Email support");

  // Upgrade to Pro
  const upgrade = await mcp__flow-nexus__user_upgrade({
    user_id: "your_user_id",
    tier: "pro"
  });

  console.log(`\nUpgraded to ${upgrade.new_tier}!`);
  console.log(`Monthly credits: ${upgrade.monthly_credits}`);
}
```

### Example 5: Cost Optimization Analysis

```javascript
// Analyze spending patterns
const history = await mcp__flow-nexus__ruv_history({
  user_id: "your_user_id",
  limit: 100
});

// Group by category
const spending = {};
for (const tx of history.transactions) {
  if (tx.amount < 0) {
    const category = tx.type || 'other';
    spending[category] = (spending[category] || 0) + Math.abs(tx.amount);
  }
}

console.log("Spending by Category:");
for (const [category, amount] of Object.entries(spending)) {
  console.log(`- ${category}: ${amount} credits`);
}

// Optimization recommendations
console.log("\nOptimization Tips:");
console.log("1. Use appropriate sandbox sizes (don't over-provision)");
console.log("2. Batch operations to reduce overhead");
console.log("3. Leverage templates instead of rebuilding");
console.log("4. Schedule non-urgent tasks for off-peak times");
console.log("5. Clean up unused sandboxes promptly");
```

## Execution Checklist

- [ ] Check current balance before operations
- [ ] Set up auto-refill to prevent interruptions
- [ ] Review spending patterns regularly
- [ ] Consider tier upgrade if usage is high
- [ ] Track earnings from published content
- [ ] Optimize resource usage for cost efficiency

## Best Practices

1. **Monitor Balance**: Check balance before heavy operations
2. **Auto-Refill**: Enable to prevent service interruption
3. **Right-Size Resources**: Don't over-provision sandboxes
4. **Batch Operations**: Group related tasks to minimize overhead
5. **Template Reuse**: Leverage existing templates
6. **Resource Cleanup**: Delete unused sandboxes promptly

## Cost Optimization Strategies

| Strategy | Savings | Effort |
|----------|---------|--------|
| Right-size sandboxes | 20-40% | Low |
| Batch operations | 10-20% | Medium |
| Template reuse | 30-50% | Low |
| Off-peak scheduling | 5-15% | Low |
| Resource cleanup | 15-30% | Low |
| Tier optimization | Variable | Medium |

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `insufficient_credits` | Balance too low | Add credits or enable auto-refill |
| `payment_failed` | Payment method issue | Update payment method |
| `invalid_amount` | Amount below minimum | Use $10 minimum |
| `auto_refill_failed` | Payment method expired | Update payment method |
| `tier_upgrade_failed` | Payment required | Complete payment first |

## Metrics & Success Criteria

- **Credit Utilization**: Track credits used vs available
- **Cost per Operation**: Monitor average cost by type
- **Auto-Refill Success**: >99% successful refills
- **Revenue (publishers)**: Track earnings from apps/templates

## Integration Points

### With Challenges

```javascript
// Credits earned from challenges
await mcp__flow-nexus__app_store_earn_ruv({
  user_id: "user_id",
  amount: 100,
  reason: "Completed Advanced Algorithm Challenge",
  source: "challenge"
});
```

### With App Store

```javascript
// Revenue from published apps
const stats = await mcp__flow-nexus__user_stats({
  user_id: "publisher_id"
});
console.log(`Earned from apps: ${stats.app_revenue} credits`);
```

### Related Skills

- [cloud-auth](../cloud-auth/SKILL.md) - User authentication
- [cloud-challenges](../cloud-challenges/SKILL.md) - Earn credits
- [cloud-app-store](../cloud-app-store/SKILL.md) - Publish and earn

## References

- [Flow Nexus Pricing](https://flow-nexus.ruv.io/pricing)
- [Credit Guide](https://flow-nexus.ruv.io/docs/credits)

## Version History

- **1.0.0** (2026-01-02): Initial release - converted from flow-nexus-payments agent
