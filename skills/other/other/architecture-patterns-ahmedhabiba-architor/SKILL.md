---
name: architecture-patterns
description: Knowledge base for architecture patterns, trade-offs, and selection criteria. Activates when recommending or evaluating architecture patterns like microservices, monolith, serverless, event-driven, CQRS, or hybrid approaches.
---

# Architecture Patterns Knowledge

## Pattern Selection Framework

When recommending a pattern, evaluate against these criteria:

### Team Fit
- Team size < 5 → Strongly favor monolith or modular monolith
- Team size 5-15 → Modular monolith or bounded microservices
- Team size 15+ → Microservices viable if org supports it
- No DevOps/Platform team → Avoid Kubernetes-heavy architectures
- Junior-heavy team → Favor simpler patterns with clear boundaries

### Operational Reality
- 1 DevOps engineer → Cannot sustain >3 independently deployed services
- No dedicated DBA → Avoid polyglot persistence
- Limited monitoring experience → Start with monolith + good observability
- Budget constrained → Serverless for spiky loads, monolith for steady

### Requirement Signals
- Independent scaling needs → Microservices or serverless
- Strong consistency requirements → Monolith or synchronous microservices
- Event-heavy domain → Event-driven architecture
- Read/write asymmetry → CQRS
- Rapid experimentation needed → Modular monolith (fastest to change)
- Regulatory isolation → Service per compliance boundary

## Pattern Comparison Quick Reference

### Monolith
- **Best for:** Small teams, rapid development, strong consistency needs
- **Risks:** Scaling bottleneck, deployment coupling, team scaling limits
- **Migrate to:** Modular monolith → microservices (progressive)

### Modular Monolith
- **Best for:** Teams 3-10, need clear boundaries without operational overhead
- **Risks:** Module coupling creep, single deployment unit
- **Migrate to:** Extract modules to services as needed

### Microservices
- **Best for:** Large teams, independent scaling, polyglot needs
- **Risks:** Distributed system complexity, data consistency, operational overhead
- **Prerequisite:** CI/CD maturity, monitoring, team autonomy

### Event-Driven
- **Best for:** Async workflows, decoupled services, audit trails
- **Risks:** Eventual consistency complexity, debugging difficulty, event schema evolution
- **Prerequisite:** Team comfort with async patterns, good monitoring

### Serverless-First
- **Best for:** Spiky workloads, cost optimization at low scale, rapid prototyping
- **Risks:** Cold starts, vendor lock-in, debugging difficulty, cost at scale
- **Prerequisite:** Cloud-native comfort, stateless design skills

### CQRS
- **Best for:** Read-heavy systems, different read/write models, event sourcing
- **Risks:** Complexity, eventual consistency, increased codebase size
- **Prerequisite:** Strong domain modeling skills

## Red Flags by Pattern

- Microservices with shared database → "You have a distributed monolith"
- Event sourcing without replay testing → "You'll lose data"
- Serverless with persistent connections → "Wrong pattern for this workload"
- CQRS for simple CRUD → "Over-engineered"
- Monolith with 50+ developers → "Deployment bottleneck incoming"
