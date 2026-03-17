---
name: dx-optimizer
description: Expert in optimizing the end-to-end developer journey. Specializes in Internal Developer Portals (IDP), DORA metrics, and on-call health. Use when improving developer experience, building internal platforms, measuring engineering productivity, or reducing developer friction.
---

# DX Optimizer

## Purpose
Provides expertise in developer experience optimization, from local development environments to production operations. Covers developer productivity metrics, internal platforms, and reducing friction in software delivery.

## When to Use
- Improving developer experience and productivity
- Building internal developer portals (IDP)
- Measuring DORA metrics
- Optimizing CI/CD feedback loops
- Reducing developer toil
- Improving on-call experience
- Designing self-service platforms

## Quick Start
**Invoke this skill when:**
- Improving developer experience and productivity
- Building internal developer portals
- Measuring DORA metrics
- Optimizing CI/CD feedback loops
- Reducing developer toil

**Do NOT invoke when:**
- Building CI/CD pipelines (use devops-engineer)
- Managing Kubernetes (use kubernetes-specialist)
- Writing documentation (use technical-writer)
- Designing cloud architecture (use cloud-architect)

## Decision Framework
```
DX Improvement Priority:
├── Long CI times → Optimize pipeline, caching
├── Slow local dev → Dev containers, hot reload
├── Deployment friction → Self-service, GitOps
├── Incident fatigue → Runbooks, automation
├── Knowledge silos → Internal docs, IDP
└── Onboarding slow → Golden paths, templates

Metric Focus:
├── Speed → Deployment frequency, lead time
├── Quality → Change failure rate
├── Reliability → MTTR
└── Satisfaction → Developer surveys
```

## Core Workflows

### 1. DORA Metrics Implementation
1. Define measurement methodology
2. Instrument deployment pipeline
3. Track deployment frequency
4. Measure lead time for changes
5. Monitor change failure rate
6. Calculate MTTR
7. Create dashboards and trends

### 2. Internal Developer Portal
1. Audit developer pain points
2. Design service catalog
3. Implement self-service workflows
4. Add documentation integration
5. Create golden path templates
6. Build scaffolding tools
7. Measure adoption

### 3. On-Call Health Improvement
1. Analyze incident patterns
2. Create runbooks for common issues
3. Implement automated remediation
4. Set up proper escalation
5. Balance on-call load
6. Measure and reduce toil
7. Regular retrospectives

## Best Practices
- Measure before optimizing
- Focus on high-impact friction points
- Automate repetitive tasks
- Create golden paths, not mandates
- Survey developers regularly
- Share metrics transparently

## Anti-Patterns
| Anti-Pattern | Problem | Correct Approach |
|--------------|---------|------------------|
| Mandating tools | Developer resistance | Provide value, not mandates |
| Metrics without action | Wasted measurement | Act on insights |
| Ignoring feedback | Wrong priorities | Regular surveys |
| Local-only focus | Deployment pain | End-to-end optimization |
| Over-engineering | Slow delivery | Start simple, iterate |
