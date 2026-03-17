---
name: Load Balancing Strategies
description: Comprehensive guide to load balancing algorithms, health checks, and high-availability patterns.
---

# Load Balancing Strategies

## Overview

Load balancing distributes traffic across multiple targets to improve
availability, performance, and resilience. This guide covers algorithms,
health checks, and operational best practices.

## Table of Contents

1. [Fundamentals](#fundamentals)
2. [Layer 4 vs Layer 7](#layer-4-vs-layer-7)
3. [Algorithms](#algorithms)
4. [Health Checks](#health-checks)
5. [Session Persistence](#session-persistence)
6. [TLS Termination](#tls-termination)
7. [Connection Draining](#connection-draining)
8. [Global Load Balancing](#global-load-balancing)
9. [Cloud Load Balancers](#cloud-load-balancers)
10. [Software Load Balancers](#software-load-balancers)
11. [Service Mesh Load Balancing](#service-mesh-load-balancing)
12. [Autoscaling Integration](#autoscaling-integration)
13. [Monitoring](#monitoring)
14. [Troubleshooting](#troubleshooting)

---

## Fundamentals

Core goals:
- Spread traffic evenly
- Avoid single points of failure
- Improve latency by routing to healthy targets

## Layer 4 vs Layer 7

- **Layer 4 (TCP/UDP)**: Fast, protocol-agnostic, no HTTP awareness.
- **Layer 7 (HTTP/HTTPS)**: Route by path/host/headers, supports TLS termination.

## Algorithms

Common strategies:
- **Round Robin**: Simple rotation.
- **Weighted Round Robin**: Bias to stronger nodes.
- **Least Connections**: Route to least busy.
- **Weighted Least Connections**: Combine weight + load.
- **IP Hash**: Sticky routing by client IP.
- **Random**: Low overhead.
- **Least Response Time**: Prefer lowest latency target.

## Health Checks

Types:
- **Active**: Probes at intervals.
- **Passive**: Detect failures from live traffic.

Use both for best detection and recovery.

## Session Persistence

Sticky sessions route a client to the same target:
- Cookie-based affinity
- IP hash

Use only when state cannot be externalized.

## TLS Termination

Terminate TLS at the load balancer for:
- Centralized cert management
- Better performance
- Easier observability

Optionally re-encrypt to backend for end-to-end security.

## Connection Draining

Allow in-flight requests to finish during scale-down or deploy:
- Set drain timeout
- Stop new connections

## Global Load Balancing

GSLB routes across regions:
- Geo-based routing
- Latency-based routing
- Failover routing

## Cloud Load Balancers

- **AWS**: ALB (L7), NLB (L4)
- **GCP**: HTTP(S) Load Balancer, TCP/UDP LB
- **Azure**: Application Gateway, Azure Load Balancer

## Software Load Balancers

- **NGINX**: Popular L7 proxy with health checks.
- **HAProxy**: High performance L4/L7.
- **Envoy**: Modern proxy with rich telemetry.

## Service Mesh Load Balancing

Service meshes (Istio, Linkerd) provide client-side load balancing with
retry policies, circuit breaking, and telemetry.

## Autoscaling Integration

Combine with autoscaling:
- Scale on CPU, latency, or queue depth
- Pre-warm nodes to reduce cold starts

## Monitoring

Track:
- Request rate and latency
- Backend error rates
- Health check failures
- Uneven traffic distribution

## Troubleshooting

Common issues:
- Misconfigured health checks (false negatives)
- Sticky sessions causing hot spots
- TLS mismatch or SNI routing errors
- Draining too short for long requests

## Related Skills
- `09-microservices/api-gateway`
- `09-microservices/service-mesh`
- `15-devops-infrastructure/kubernetes-helm`
