---
name: building-attack-trees
description: <!-- Copyright (c) 2026 defconxt. All rights reserved. -->
---

<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
<!-- CIPHER is a trademark of defconxt. -->
---
name: building-attack-trees
description: >-
  Construct hierarchical attack trees that decompose adversary goals into sub-goals, leaf nodes represent atomic attack steps, with AND/OR logic gates for comprehensive attack path enumeration and cost-benefit analysis.
domain: cybersecurity
subdomain: threat-modeling
tags:
  - attack-trees
  - attack-paths
  - goal-decomposition
  - risk-analysis
  - threat-enumeration
version: "1.0"
author: defconxt
license: AGPL-3.0
metadata:
  mitre-attack: ["T1078", "T1059", "T1053", "T1021"]
---

# Building Attack Trees

## Overview

Attack trees are hierarchical diagrams that model how an adversary achieves a goal by
decomposing it into sub-goals connected by AND/OR gates. This technique covers tree
construction, probability and cost annotation, path enumeration, and countermeasure mapping.

Mode: `[MODE: RED]` — Offensive attack path analysis and enumeration.

## Prerequisites

- Target system documentation or architecture diagrams
- Python 3.10+ for tree analysis scripts
- Graphviz for tree visualization: `apt install graphviz`
- Understanding of the adversary's capabilities and objectives

## Key Concepts

### Attack Tree Structure

- **Root node**: Adversary's ultimate goal (e.g., "Exfiltrate customer PII")
- **OR nodes**: Alternative attack paths (attacker needs ANY one)
- **AND nodes**: Required combined steps (attacker needs ALL)
- **Leaf nodes**: Atomic attack actions with cost/probability annotations

### Node Annotations

| Attribute | Description | Example |
|-----------|-------------|---------|
| Cost | Resources required | $500, 40 hours |
| Probability | Likelihood of success | 0.7 (70%) |
| Skill Level | Attacker expertise needed | Script kiddie / APT |
| Detection Risk | Chance of being caught | Low / Medium / High |
| Impact | Damage if successful | Critical data loss |

### Path Analysis

For each root-to-leaf path:
- **AND paths**: multiply probabilities, sum costs
- **OR paths**: take maximum probability, minimum cost
- **Optimal attack**: lowest cost path with highest success probability

## Workflow

### Step 1: Define Root Goal

```bash
# Initialize attack tree with root goal
node scripts/agent.js --action build --goal "Exfiltrate customer PII"
```

### Step 2: Decompose Into Sub-Goals

```bash
# Add nodes to the tree
node scripts/agent.js --action add-node --parent root --name "Compromise web app" --gate OR
node scripts/agent.js --action add-node --parent root --name "Insider threat" --gate OR
```

### Step 3: Annotate and Analyze

```bash
# Analyze all attack paths
node scripts/agent.js --action analyze --input tree.json --output analysis.json

# Export tree visualization
node scripts/agent.js --action export --input tree.json --format dot
```

### Step 4: Map Countermeasures

```bash
# Generate countermeasure report
node scripts/agent.js --action countermeasures --input tree.json --output mitigations.json
```

## Verification

- [ ] Root goal clearly defined from adversary perspective
- [ ] All leaf nodes represent atomic, actionable attack steps
- [ ] AND/OR gates correctly model dependency relationships
- [ ] Cost and probability annotations on all leaf nodes
- [ ] All viable attack paths enumerated and ranked
- [ ] Countermeasures mapped to highest-risk paths

## References

- [Bruce Schneier — Attack Trees](https://www.schneier.com/academic/archives/1999/12/attack_trees.html)
- [OWASP Attack Tree](https://owasp.org/www-community/Attack_Tree)
- [MITRE ATT&CK](https://attack.mitre.org/)
