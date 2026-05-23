---
name: quality-attributes-taxonomy
description: The "-ilities" framework for non-functional requirements. Use when defining NFRs, evaluating architecture trade-offs, or ensuring quality attributes are addressed in system design. Covers scalability, reliability, availability, performance, security, maintainability, and more.
allowed-tools: Read, Glob, Grep
---

# Quality Attributes Taxonomy

This skill provides a comprehensive framework for understanding and applying quality attributes (non-functional requirements) in system design.

## When to Use This Skill

**Keywords:** NFR, non-functional requirements, quality attributes, -ilities, scalability, reliability, availability, performance, security, maintainability, ISO 25010

**Use this skill when:**

- Defining non-functional requirements for a system
- Evaluating architectural trade-offs
- Conducting architecture reviews
- Preparing for system design interviews
- Ensuring all quality dimensions are considered
- Translating business needs to technical requirements

## What Are Quality Attributes?

Quality attributes (QAs) describe HOW a system performs, not WHAT it does. They're often called:

- Non-Functional Requirements (NFRs)
- The "-ilities" (scalability, reliability, etc.)
- Cross-cutting concerns
- System qualities

**Key insight:** Functional requirements define features; quality attributes define how well those features work.

## The Core Quality Attributes

### Primary Attributes (The Big 6)

| Attribute | Definition | Key Question |
| --------- | ---------- | ------------ |
| **Scalability** | Handle growing load | Can we grow 10x? 100x? |
| **Reliability** | Consistent correct operation | Does it work correctly every time? |
| **Availability** | System uptime | Is it running when needed? |
| **Performance** | Speed and throughput | How fast is it? |
| **Security** | Protection from threats | Is it safe from attacks? |
| **Maintainability** | Ease of change | Can we update it easily? |

### Secondary Attributes

| Attribute | Definition | Key Question |
| --------- | ---------- | ------------ |
| **Testability** | Ease of verification | Can we test it effectively? |
| **Observability** | System visibility | Can we see what's happening? |
| **Operability** | Ease of operation | Can we run it in production? |
| **Portability** | Platform independence | Can we move it? |
| **Interoperability** | System integration | Can it work with others? |
| **Cost Efficiency** | Resource optimization | Is it cost-effective? |

## Detailed Quality Attribute Definitions

### Scalability

**Definition:** The ability to handle increased load by adding resources.

| Type | Description | Example |
| ---- | ----------- | ------- |
| **Vertical** | Add more power to existing machines | Upgrade to larger instance |
| **Horizontal** | Add more machines | Add more servers behind load balancer |
| **Elastic** | Automatic scaling based on load | Auto-scaling groups |

**Measurement:**

```text
- Maximum concurrent users
- Requests per second at given latency
- Data volume supported
- Cost per transaction at scale
```

**Trade-offs:**

- Scalability often conflicts with consistency (CAP theorem)
- More scalability = more complexity
- Horizontal scaling requires stateless design

### Reliability

**Definition:** The probability of correct operation over time.

| Concept | Definition |
| ------- | ---------- |
| **MTBF** | Mean Time Between Failures |
| **MTTR** | Mean Time To Recovery |
| **Fault Tolerance** | Continue despite component failures |
| **Resilience** | Recover from failures gracefully |

**Measurement:**

```text
- Error rate (errors / total requests)
- Failure rate (failures / time period)
- Data accuracy percentage
- Successful transaction rate
```

**Trade-offs:**

- Higher reliability = higher cost (redundancy)
- Reliability vs performance (checksums, validation)
- Reliability vs complexity (more failure modes to handle)

### Availability

**Definition:** The proportion of time a system is operational.

| Level | Uptime | Downtime/Year | Downtime/Month |
| ----- | ------ | ------------- | -------------- |
| 99% | Two 9s | 3.65 days | 7.31 hours |
| 99.9% | Three 9s | 8.76 hours | 43.8 minutes |
| 99.99% | Four 9s | 52.6 minutes | 4.38 minutes |
| 99.999% | Five 9s | 5.26 minutes | 26.3 seconds |

**Measurement:**

```text
Availability = Uptime / (Uptime + Downtime)
            = MTBF / (MTBF + MTTR)
```

**Trade-offs:**

- Each additional "9" is exponentially more expensive
- Availability vs consistency (CAP theorem)
- Planned maintenance affects availability

### Performance

**Definition:** How fast and efficient the system operates.

| Metric | Definition |
| ------ | ---------- |
| **Latency** | Time to complete one request |
| **Throughput** | Requests processed per unit time |
| **Response Time** | Total time user waits |
| **Utilization** | Resource usage percentage |

**Common Targets:**

```text
- Web page load: < 2 seconds
- API response: < 100 ms (p99)
- Database query: < 10 ms
- Batch job: < scheduled window
```

**Trade-offs:**

- Performance vs cost (faster hardware costs more)
- Latency vs throughput (batching improves throughput, hurts latency)
- Performance vs consistency (caching improves speed, may serve stale data)

### Security

**Definition:** Protection of data and systems from unauthorized access.

| Principle | Description |
| --------- | ----------- |
| **Confidentiality** | Data accessible only to authorized |
| **Integrity** | Data is accurate and unaltered |
| **Availability** | Systems accessible when needed |
| **Non-repudiation** | Actions are attributable |

**Measurement:**

```text
- Time to detect breaches
- Number of vulnerabilities
- Compliance audit results
- Mean time to patch
```

**Trade-offs:**

- Security vs usability (more security = more friction)
- Security vs performance (encryption adds latency)
- Security vs cost (security tools and expertise are expensive)

### Maintainability

**Definition:** Ease of modifying the system over time.

| Aspect | Description |
| ------ | ----------- |
| **Modularity** | Components can change independently |
| **Reusability** | Components can be repurposed |
| **Analyzability** | Easy to understand the system |
| **Modifiability** | Easy to make changes |
| **Testability** | Easy to verify changes |

**Measurement:**

```text
- Time to implement typical change
- Defect injection rate per change
- Code complexity metrics
- Documentation coverage
```

**Trade-offs:**

- Maintainability vs performance (abstractions add overhead)
- Maintainability vs time-to-market (good design takes time)
- Maintainability vs specialization (generic = slower)

## Quality Attribute Scenarios

### How to Specify Quality Attributes

Use this template to make QAs measurable:

```text
Source:     [Who or what generates the stimulus?]
Stimulus:   [What event occurs?]
Artifact:   [What part of the system is affected?]
Environment:[Under what conditions?]
Response:   [How should the system respond?]
Measure:    [How do we know it succeeded?]
```

### Example Scenarios

**Scalability Scenario:**

```text
Source:     Marketing campaign
Stimulus:   10x traffic spike
Artifact:   Web application
Environment:Normal operation
Response:   Auto-scale to handle load
Measure:    Latency stays under 200ms at p99
```

**Availability Scenario:**

```text
Source:     Hardware failure
Stimulus:   Database server dies
Artifact:   Order processing system
Environment:Peak business hours
Response:   Failover to replica
Measure:    Recovery in < 30 seconds, no data loss
```

**Security Scenario:**

```text
Source:     External attacker
Stimulus:   SQL injection attempt
Artifact:   User authentication
Environment:Production
Response:   Block attack, alert security team
Measure:    Zero successful injections, alert within 5 minutes
```

## ISO 25010 Quality Model

The ISO 25010 standard defines 8 quality characteristics:

| Characteristic | Sub-characteristics |
| -------------- | ------------------- |
| **Functional Suitability** | Completeness, correctness, appropriateness |
| **Performance Efficiency** | Time behavior, resource utilization, capacity |
| **Compatibility** | Co-existence, interoperability |
| **Usability** | Learnability, operability, accessibility |
| **Reliability** | Maturity, availability, fault tolerance, recoverability |
| **Security** | Confidentiality, integrity, non-repudiation, accountability |
| **Maintainability** | Modularity, reusability, analyzability, modifiability, testability |
| **Portability** | Adaptability, installability, replaceability |

## Quality Attributes in System Design Interviews

### How to Address QAs

1. **Ask about requirements:** "What's the expected latency? Availability target?"
2. **State assumptions:** "I'll assume we need 99.9% availability"
3. **Justify decisions:** "I'm adding a cache here for performance"
4. **Acknowledge trade-offs:** "This improves scalability but complicates consistency"

### Common QA Trade-offs in Interviews

| Decision | Improves | Hurts |
| -------- | -------- | ----- |
| Add caching | Performance | Consistency, complexity |
| Add replication | Availability | Consistency, cost |
| Use async processing | Throughput | Latency, complexity |
| Shard database | Scalability | Cross-shard queries |
| Add encryption | Security | Performance |
| Use microservices | Maintainability, scalability | Latency, complexity |

### QA Checklist for Design Reviews

Before finalizing a design, verify:

- [ ] **Scalability:** Can handle 10x growth?
- [ ] **Reliability:** Handles component failures?
- [ ] **Availability:** Meets uptime target?
- [ ] **Performance:** Meets latency/throughput targets?
- [ ] **Security:** Protects data and access?
- [ ] **Maintainability:** Easy to update and debug?
- [ ] **Cost:** Within budget at scale?
- [ ] **Observability:** Can monitor and troubleshoot?

## Architectural Tactics by Quality Attribute

### Scalability Tactics

| Tactic | Description |
| ------ | ----------- |
| Horizontal scaling | Add more instances |
| Load balancing | Distribute traffic |
| Sharding | Partition data |
| Caching | Reduce repeated work |
| Async processing | Decouple components |

### Availability Tactics

| Tactic | Description |
| ------ | ----------- |
| Redundancy | Multiple instances of components |
| Failover | Automatic switch to backup |
| Health checks | Detect failures early |
| Graceful degradation | Reduce functionality vs complete failure |
| Geographic distribution | Survive datacenter failures |

### Performance Tactics

| Tactic | Description |
| ------ | ----------- |
| Caching | Reduce computation/IO |
| CDN | Serve content closer to users |
| Connection pooling | Reuse expensive connections |
| Compression | Reduce data transfer |
| Indexing | Speed up queries |

### Security Tactics

| Tactic | Description |
| ------ | ----------- |
| Encryption | Protect data at rest and in transit |
| Authentication | Verify identity |
| Authorization | Control access |
| Audit logging | Track actions |
| Input validation | Prevent injection attacks |

## From Business Requirements to Quality Attributes

### Translation Guide

| Business Requirement | Quality Attribute | Technical Implication |
| -------------------- | ----------------- | --------------------- |
| "Must handle Black Friday traffic" | Scalability | Auto-scaling, elastic capacity |
| "Cannot lose orders" | Reliability, durability | Replication, backups, transactions |
| "Always available" | Availability | Redundancy, failover, monitoring |
| "Fast checkout" | Performance | Caching, optimization, CDN |
| "Protect customer data" | Security | Encryption, access control, auditing |
| "Easy to add features" | Maintainability | Modular design, clean architecture |
| "Regulatory compliance" | Security, auditability | Logging, encryption, access control |
| "Global users" | Performance, availability | CDN, geographic distribution |

## Related Skills

- `design-interview-methodology` - Overall interview framework
- `estimation-techniques` - Quantify capacity requirements
- `cap-theorem` - Consistency/availability trade-offs (Phase 2)
- `trade-off-analysis` - ATAM and decision frameworks (Phase 5)
- `architectural-tactics` - Detailed tactics per attribute (Phase 5)

## Related Commands

- `/sd:analyze-nfrs [scope]` - Analyze quality attributes in code (Phase 5)
- `/sd:explain <concept>` - Explain any quality attribute

## Related Agents

- `trade-off-analyzer` - Evaluate design trade-offs (Phase 2)
- `sre-persona` - Reliability/observability perspective (Phase 5)
- `security-architect` - Security implications (Phase 5)

---

## Version History

- **v1.0.0** (2025-12-26): Initial release

---

## Last Updated

**Date:** 2025-12-26
**Model:** claude-opus-4-5-20251101
