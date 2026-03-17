---
name: continuous-learning-v2
description: Instinct-based pattern learning with confidence scoring and auto-evolution
argument-hint: "[status|export|import|evolve]"
tags: [learning, patterns, instincts, evolution, meta]
---

# Continuous Learning v2

## Overview
Captures atomic behavioral patterns (instincts) from session activity via hooks.
Each instinct has a confidence score (0.3-0.9) that increases with repetition and decays when contradicted.

## Commands
-  - View learned patterns with confidence scores
-  - Export instincts as JSON for team sharing
-  - Import instincts from teammate
-  - Cluster related instincts into reusable skills/commands

## How It Works

### Capture Pipeline


### Instinct Format


### Confidence Scoring
| Score | Meaning | Action |
|-------|---------|--------|
| 0.3-0.4 | Weak signal | Observe only |
| 0.5-0.6 | Emerging pattern | Suggest in context |
| 0.7-0.8 | Strong pattern | Auto-apply |
| 0.9+ | Established behavior | Promote to skill |

### Evolution Pipeline
When 3+ related instincts reach 0.7+ confidence:
1. Cluster by category/domain
2. Generate skill draft from instinct descriptions
3. Present for human review
4. If approved, create skill .md file in skills/ directory

## Stack Context
- .NET 8: Watch for CosmosDB patterns, GDPR anonymization, French HR terms
- React 18: Watch for Redux Toolkit patterns, Ant Design usage, French labels
- Azure: Watch for AKS deployment patterns, Key Vault usage
