---
name: cfn-hybrid-routing
description: Adaptive routing strategies for distributed systems with multi-channel communication
version: 1.0.0
tags: [routing, hybrid, failover, load-balancing]
status: production
---

# Hybrid Routing Skill

## Overview
Implements adaptive routing strategies for distributed systems with multi-channel communication.

## Purpose
- Dynamic route selection
- Fallback mechanism implementation
- Performance optimization
- Low-latency communication channels

## Routing Strategies
1. Primary-Secondary Channel Routing
2. Load-balanced Path Selection
3. Contextual Routing

## Configuration Parameters
- `primary_channel`: Main communication route
- `secondary_channel`: Backup communication path
- `routing_algorithm`: Routing selection method
- `latency_threshold`: Maximum acceptable delay

## Operational Modes
- Synchronous Routing
- Asynchronous Routing
- Failover Routing

## Dependencies
- Redis Pub/Sub
- Agent Coordination Framework
- Performance Monitoring

## Security Considerations
- Encrypted channel selection
- Authentication for route transitions
- Minimal exposure surface

## Performance Metrics
- Route success rate
- Channel switching latency
- Routing decision confidence

## Validation Criteria
- ≥0.85 routing accuracy
- <50ms channel transition time
- Minimal packet loss