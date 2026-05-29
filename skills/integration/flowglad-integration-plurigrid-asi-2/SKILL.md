---
name: flowglad-integration
description: Zero-webhook billing for AI agents
version: 1.0.0
trit: 1
---

# Flowglad Integration

> **Trit**: +1 (PLUS) - Generates billing flows

Zero-webhook billing platform for AI agent subscriptions.

## Overview

Resolves credit balance friction via polling-based checkout.

## GF(3) Triad

| Trit | Skill | Role |
|------|-------|------|
| -1 | amp-skill | Validates credit |
| 0 | unified-reafference | Coordinates state |
| +1 | flowglad-integration | Generates checkout |

## Patterns That Work

- Polling-based checkout (no webhooks)
- Usage metering via ledger
- Multi-tenant with RLS

## Patterns to Avoid

- Webhook-dependent flows
- Synchronous payment confirmation

## Related Skills

- amp-skill
- unified-reafference
- aptos-trading

## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 10. Adventure Game Example

**Concepts**: autonomous agent, game, synthesis

### GF(3) Balanced Triad

```
flowglad-integration (−) + SDF.Ch10 (+) + [balancer] (○) = 0
```

**Skill Trit**: -1 (MINUS - verification)

### Secondary Chapters

- Ch4: Pattern Matching

### Connection Pattern

Adventure games synthesize techniques. This skill integrates multiple patterns.
