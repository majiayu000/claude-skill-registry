---
# ═══════════════════════════════════════════════════════════════════════════
# SKILL: Languages & Frameworks
# Version: 2.0.0 | Updated: 2025-01
# ═══════════════════════════════════════════════════════════════════════════
name: languages-frameworks
description: Expert guidance on 9 programming languages and 10+ frameworks. Compare, select, and master language ecosystems.

# ACTIVATION TRIGGERS
triggers:
  - python
  - javascript
  - typescript
  - java
  - go
  - rust
  - language comparison
  - framework selection

# SKILL PARAMETERS
parameters:
  use_case:
    type: string
    required: true
    description: Primary use case (web, data, systems, mobile)
  constraints:
    type: array
    required: false
    description: Constraints (team skills, performance, ecosystem)

# OUTPUT SPECIFICATION
outputs:
  recommendation:
    type: object
    description: Primary and alternative recommendations
  learning_path:
    type: array
    description: Steps to proficiency
  ecosystem_tools:
    type: array
    description: Essential ecosystem tools

# RELIABILITY
retry:
  max_attempts: 3
  backoff: exponential

# OBSERVABILITY
observability:
  log_level: info
  metrics: [recommendation_accuracy]

level: intermediate-to-advanced

sasmp_version: "1.3.0"
bonded_agent: 01-core-paths
bond_type: PRIMARY_BOND
---

# Languages & Frameworks Skill

## Quick Reference

| Goal | Primary | Alternative | Learning Time |
|------|---------|-------------|---------------|
| Web Backend | Python | JavaScript | 2-3 months |
| AI/ML | Python | - | 3-6 months |
| Systems | Go | Rust | 2-4 months |
| Enterprise | Java | C# | 4-6 months |
| Android | Kotlin | - | 3-4 months |
| iOS | Swift | - | 3-4 months |

---

## 2025 Language Rankings

### Tier 1: Highest Demand
| Language | TIOBE | Use Cases | Ecosystem |
|----------|-------|-----------|-----------|
| **Python** | #1 | AI/ML, Web, Automation | Excellent |
| **JavaScript** | #6 | Full-stack Web | Excellent |
| **TypeScript** | #7 | Large-scale Apps | Excellent |
| **Java** | #4 | Enterprise | Excellent |

### Tier 2: Growing Demand
| Language | TIOBE | Use Cases | Ecosystem |
|----------|-------|-----------|-----------|
| **Go** | #8 | Cloud, DevOps | Good |
| **Rust** | #14 | Systems, WASM | Growing |
| **Kotlin** | #18 | Android, Server | Good |

---

## Framework Selection

### Frontend (2025)
| Framework | Best For | Learning | Bundle |
|-----------|----------|----------|--------|
| **React 19** | Large apps | Medium | 42kb |
| **Vue 3** | Simplicity | Easy | 34kb |
| **Svelte 5** | Performance | Easy | 2kb |
| **Angular 18** | Enterprise | Hard | 90kb |

### Backend (2025)
| Framework | Language | Best For | Perf |
|-----------|----------|----------|------|
| **FastAPI** | Python | ML APIs | Good |
| **NestJS** | TypeScript | Enterprise | Good |
| **Gin** | Go | Performance | Excellent |
| **Spring Boot** | Java | Enterprise | Good |

---

## Decision Flowchart

```
What are you building?
│
├─► Web app (startup)
│   └─► Python + FastAPI OR TypeScript + NestJS
│
├─► Web app (enterprise)
│   └─► Java + Spring Boot OR TypeScript + NestJS
│
├─► AI/ML application
│   └─► Python (no alternatives match ecosystem)
│
├─► High-performance API
│   └─► Go + Gin OR Rust + Actix
│
├─► Mobile app
│   ├─► iOS only → Swift
│   ├─► Android only → Kotlin
│   └─► Cross-platform → Flutter (Dart)
│
└─► CLI/Systems tool
    └─► Go (simpler) OR Rust (safer)
```

---

## Ecosystem Essentials

| Language | Package Mgr | Formatter | Linter | Testing |
|----------|-------------|-----------|--------|---------|
| **Python** | uv, pip | ruff | ruff | pytest |
| **JavaScript** | pnpm | prettier | eslint | vitest |
| **Go** | go mod | gofmt | golangci-lint | go test |
| **Rust** | cargo | rustfmt | clippy | cargo test |
| **Java** | maven | google-java-format | spotbugs | junit |

---

## Learning Timelines

| Language | Basics | Productive | Expert |
|----------|--------|------------|--------|
| Python | 2 wk | 2 mo | 1+ yr |
| JavaScript | 3 wk | 3 mo | 1+ yr |
| TypeScript | 2 wk* | 1 mo* | 6+ mo* |
| Go | 2 wk | 2 mo | 6 mo |
| Rust | 2 mo | 6 mo | 2+ yr |
| Java | 1 mo | 4 mo | 1+ yr |

*Assumes JavaScript knowledge

---

## Troubleshooting

```
Can't decide between languages?
├─► Define end goal first (not "learn programming")
├─► Check team/company constraints
├─► Default: Python (most versatile) or TypeScript (web)
└─► Don't spend >1 day deciding

"Is X language dying?"
├─► PHP: NO - 77% of web, Laravel thriving
├─► Java: NO - #4 TIOBE, enterprise standard
├─► Ruby: Stable niche, not growing
└─► Perl: Legacy only, avoid for new projects

Learning multiple languages?
├─► Master ONE language first (6+ months)
├─► Then learn opposite paradigm
├─► Max 2 deeply before broadening
└─► Breadth without depth = unemployable
```

---

## Common Failure Modes

| Symptom | Root Cause | Recovery |
|---------|------------|----------|
| Analysis paralysis | Too many options | Apply constraints, decide today |
| Chasing new frameworks | FOMO | Stick with 2+ year old tools |
| Wrong tool for job | Ignoring requirements | Revisit decision flowchart |
| Framework lock-in | Learned framework, not language | Go back to fundamentals |

---

## Next Actions

Describe your use case to get a personalized recommendation.
