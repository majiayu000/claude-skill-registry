---
name: load-balancing-patterns
description: When distributing traffic across multiple servers or regions, use this skill to select and configure the appropriate load balancing solution (L4/L7, cloud-managed, self-managed, or Kubernetes ingress) with proper health checks and session management.
---

# Load Balancing Patterns

Distribute traffic across infrastructure using the appropriate load balancing approach, from simple round-robin to global multi-region failover.

## When to Use This Skill

Use load-balancing-patterns when:
- Distributing traffic across multiple application servers
- Implementing high availability and failover
- Routing traffic based on URLs, headers, or geographic location
- Managing session persistence across stateless backends
- Deploying applications to Kubernetes clusters
- Configuring global traffic management across regions
- Implementing zero-downtime deployments (blue-green, canary)
- Selecting between cloud-managed and self-managed load balancers

## Core Load Balancing Concepts

### Layer 4 vs Layer 7

**Layer 4 (L4) - Transport Layer:**
- Routes based on IP address and port (TCP/UDP packets)
- No application data inspection, lower latency, higher throughput
- Protocol agnostic, preserves client IP addresses
- Use for: Database connections, video streaming, gaming, financial transactions, non-HTTP protocols

**Layer 7 (L7) - Application Layer:**
- Routes based on HTTP URLs, headers, cookies, request body
- Full application data visibility, SSL/TLS termination, caching, WAF integration
- Content-based routing capabilities
- Use for: Web applications, REST APIs, microservices, GraphQL endpoints, complex routing logic

For detailed comparison including performance benchmarks and hybrid approaches, see `references/l4-vs-l7-comparison.md`.

### Load Balancing Algorithms

| Algorithm | Distribution Method | Use Case |
|-----------|-------------------|----------|
| **Round Robin** | Sequential | Stateless, similar servers |
| **Weighted Round Robin** | Capacity-based | Different server specs |
| **Least Connections** | Fewest active connections | Long-lived connections |
| **Least Response Time** | Fastest server | Performance-sensitive |
| **IP Hash** | Client IP-based | Session persistence |
| **Resource-Based** | CPU/memory metrics | Varying workloads |

### Health Check Types

**Shallow (Liveness):** Is the process alive?
- Endpoint: `/health/live` or `/live`
- Returns: 200 if process running
- Use for: Process monitoring, container health

**Deep (Readiness):** Can the service handle requests?
- Endpoint: `/health/ready` or `/ready`
- Validates: Database, cache, external API connectivity
- Use for: Load balancer routing decisions

**Health Check Hysteresis:** Different thresholds for marking up vs down to prevent flapping
- Example: 3 failures to mark down, 2 successes to mark up

For complete health check implementation patterns, see `references/health-check-strategies.md`.

## Cloud Load Balancers

### AWS Load Balancing

**Application Load Balancer (ALB) - Layer 7:**
- Use for: HTTP/HTTPS applications, microservices, WebSocket
- Features: Path/host/header routing, AWS WAF integration, Lambda targets
- Choose when: Content-based routing needed

**Network Load Balancer (NLB) - Layer 4:**
- Use for: Ultra-low latency (<1ms), TCP/UDP, static IPs, millions RPS
- Features: Preserves source IP, TLS termination
- Choose when: Non-HTTP protocols, performance critical

**Global Accelerator - Layer 4 Global:**
- Use for: Multi-region applications, global users, DDoS protection
- Features: Anycast IPs, automatic regional failover

### GCP Load Balancing

**Application LB (L7):** Global HTTPS LB, Cloud CDN integration, Cloud Armor (WAF/DDoS)
**Network LB (L4):** Regional TCP/UDP, pass-through balancing, session affinity
**Cloud Load Balancing:** Single anycast IP, global distribution, backend buckets

### Azure Load Balancing

**Application Gateway (L7):** WAF integration, URL-based routing, SSL termination, autoscaling
**Load Balancer (L4):** Basic and Standard SKUs, health probes, HA ports
**Traffic Manager (Global):** DNS-based routing (priority, weighted, performance, geographic)

For complete cloud provider configurations and Terraform examples, see `references/cloud-load-balancers.md`.

## Self-Managed Load Balancers

### NGINX

**Best for:** General-purpose HTTP/HTTPS load balancing, web application stacks

**Capabilities:**
- HTTP reverse proxy with multiple algorithms
- TCP/UDP stream load balancing
- SSL/TLS termination
- Passive health checks (open source), active health checks (NGINX Plus)
- Cookie-based sticky sessions (NGINX Plus)

**Basic configuration:**
```nginx
upstream backend {
    least_conn;
    server backend1.example.com:8080 weight=3;
    server backend2.example.com:8080 weight=2;
    keepalive 32;
}

server {
    listen 80;
    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

For complete NGINX patterns and advanced configurations, see `references/nginx-patterns.md`.

### HAProxy

**Best for:** Maximum performance, database load balancing, resource efficiency

**Capabilities:**
- Highest raw throughput, lowest memory footprint
- 10+ load balancing algorithms
- Sophisticated health checks (HTTP, TCP, Redis, MySQL, etc.)
- Cookie or IP-based persistence

**Basic configuration:**
```haproxy
frontend http_front
    bind *:80
    default_backend web_servers

backend web_servers
    balance roundrobin
    option httpchk GET /health
    server web1 192.168.1.101:8080 check
    server web2 192.168.1.102:8080 check
```

For complete HAProxy patterns, see `references/haproxy-patterns.md`.

### Envoy

**Best for:** Microservices, Kubernetes, service mesh integration

**Capabilities:**
- Cloud-native design with dynamic configuration (xDS APIs)
- Circuit breakers, retries, timeouts
- Advanced health checks (TCP, HTTP, gRPC)
- Excellent observability

For complete Envoy patterns, see `references/envoy-patterns.md`.

### Traefik

**Best for:** Docker/Kubernetes environments, dynamic configuration, ease of use

**Capabilities:**
- Automatic service discovery
- Native Kubernetes integration
- Built-in Let's Encrypt support
- Middleware system (auth, rate limiting)

For complete Traefik patterns, see `references/traefik-patterns.md`.

## Kubernetes Ingress Controllers

### Selection Guide

| Controller | Best For | Strengths |
|------------|----------|-----------|
| **NGINX Ingress** (F5) | General purpose | Stability, wide adoption, mature features |
| **Traefik** | Dynamic environments | Easy configuration, service discovery |
| **HAProxy Ingress** | High performance | Advanced L7 routing, reliability |
| **Envoy** (Contour/Gateway) | Service mesh | Rich L7 features, extensibility |
| **Kong** | API-heavy apps | JWT auth, rate limiting, plugins |
| **Cloud Provider** | Single-cloud | Native cloud integration |

### Basic Ingress Example

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/affinity: "cookie"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - app.example.com
    secretName: app-tls
  rules:
  - host: app.example.com
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: api-service
            port:
              number: 80
      - path: /
        pathType: Prefix
        backend:
          service:
            name: web-service
            port:
              number: 80
```

For complete Kubernetes ingress examples and Gateway API patterns, see `references/kubernetes-ingress.md`.

## Session Persistence

### Sticky Sessions (Use Sparingly)

**Cookie-Based:** Load balancer sets cookie to track server affinity
- Accurate routing, works with NAT/proxies
- HTTP only, adds cookie overhead

**IP Hash:** Hash client IP to select backend server
- No cookie required, works for non-HTTP
- Poor distribution with NAT/proxies

**Drawbacks:** Uneven load distribution, session lost on server failure, complicates scaling

### Shared Session Store (Recommended)

Architecture: Stateless application servers + centralized session storage (Redis, Memcached)

**Benefits:**
- No sticky sessions needed
- True load balancing
- Server failures don't lose sessions
- Horizontal scaling trivial

### Client-Side Tokens (Best for APIs)

JWT (JSON Web Tokens): Server generates signed token, client stores and sends with requests

**Benefits:**
- Fully stateless servers
- Perfect load balancing
- No session storage needed

For complete session management patterns and code examples, see `references/session-persistence.md`.

## Global Load Balancing

### GeoDNS Routing

Route users to nearest server based on geographic location:
- DNS returns different IPs based on client location
- Reduces latency, supports compliance and regional content
- Implementation: AWS Route 53, GCP Cloud DNS, Azure Traffic Manager

### Multi-Region Failover

Primary/secondary region configuration:
- Health checks determine primary region health
- Automatic DNS failover to secondary
- Transparent to clients

### CDN Integration

Combine load balancing with CDN:
- GeoDNS routes to closest CDN PoP
- CDN caches content globally
- Origin load balancing for cache misses

For complete global load balancing examples with Terraform, see `references/global-load-balancing.md`.

## Decision Frameworks

### L4 vs L7 Selection

Choose **L4** when:
- Protocol is TCP/UDP (not HTTP)
- Ultra-low latency critical (<1ms)
- High throughput required (millions RPS)
- Client source IP preservation needed

Choose **L7** when:
- Protocol is HTTP/HTTPS
- Content-based routing needed (URL, headers)
- SSL termination required
- WAF integration needed
- Microservices architecture

### Cloud vs Self-Managed

Choose **Cloud-Managed** when:
- Single cloud deployment
- Auto-scaling required
- Team lacks load balancer expertise
- Managed service preferred

Choose **Self-Managed** when:
- Multi-cloud or hybrid deployment
- Advanced routing requirements
- Cost optimization important
- Full control needed
- Vendor lock-in avoidance

### Self-Managed Selection

- **NGINX:** General-purpose, web stacks, HTTP/3 support
- **HAProxy:** Maximum performance, database LB, lowest resource usage
- **Envoy:** Microservices, service mesh, dynamic configuration
- **Traefik:** Docker/Kubernetes, automatic discovery, easy configuration

## Configuration Examples

Complete working examples available in `examples/` directory:

**Cloud Providers:**
- `examples/aws/alb-terraform.tf` - AWS ALB with path-based routing
- `examples/aws/nlb-terraform.tf` - AWS NLB for TCP load balancing

**Self-Managed:**
- `examples/nginx/http-load-balancing.conf` - NGINX HTTP reverse proxy
- `examples/haproxy/http-lb.cfg` - HAProxy configuration
- `examples/envoy/basic-lb.yaml` - Envoy cluster configuration
- `examples/traefik/kubernetes-ingress.yaml` - Traefik IngressRoute

**Kubernetes:**
- `examples/kubernetes/nginx-ingress.yaml` - NGINX Ingress with TLS
- `examples/kubernetes/traefik-ingress.yaml` - Traefik IngressRoute
- `examples/kubernetes/gateway-api.yaml` - Gateway API configuration

## Monitoring and Observability

### Key Metrics

**Throughput:** Requests per second, bytes transferred, connection rate
**Latency:** Request duration (p50, p95, p99), backend response time, SSL handshake time
**Errors:** HTTP error rates (4xx, 5xx), backend connection failures, health check failures
**Resource Utilization:** CPU, memory, active connections, connection queue depth
**Health:** Healthy/unhealthy backend count, health check success rate

### Load Balancer Logs

Enable access logs for request/response details, client IPs, response times, error tracking
- **AWS ALB:** Store in S3, analyze with Athena
- **NGINX:** Custom log format, ship to centralized logging
- **HAProxy:** Syslog integration, structured logging

## Troubleshooting

### Uneven Load Distribution

**Symptoms:** One server receives disproportionate traffic
**Causes:** Sticky sessions with few clients, IP hash with NAT concentration, long-lived connections
**Solutions:** Switch to least connections, disable sticky sessions, implement connection draining

### Health Check Flapping

**Symptoms:** Servers rapidly transition between healthy/unhealthy
**Causes:** Health check timeout too short, threshold too low, network instability
**Solutions:** Increase interval and timeout, implement hysteresis, use deep health checks

### Session Loss After Failover

**Symptoms:** Users logged out when server fails
**Causes:** Sticky sessions without replication, in-memory sessions
**Solutions:** Implement shared session store (Redis), use client-side tokens (JWT)

## Integration Points

**Related Skills:**
- `infrastructure-as-code` - Deploy load balancers via Terraform/Pulumi
- `kubernetes-operations` - Ingress controllers for K8s traffic management
- `network-architecture` - Network design and topology for load balancing
- `deploying-applications` - Blue-green and canary deployments via load balancers
- `observability` - Load balancer metrics, access logs, distributed tracing
- `security-hardening` - WAF integration, rate limiting, DDoS protection
- `service-mesh` - Envoy as both ingress and service mesh proxy
- `implementing-tls` - TLS termination and certificate management

## Quick Reference

### Selection Matrix

| Use Case | Recommended Solution |
|----------|---------------------|
| HTTP web app (AWS) | ALB |
| Non-HTTP protocol (AWS) | NLB |
| Kubernetes HTTP ingress | NGINX Ingress or Traefik |
| Maximum performance | HAProxy |
| Service mesh | Envoy |
| Docker Swarm | Traefik |
| Multi-cloud portable | NGINX or HAProxy |
| Global distribution | CloudFlare, AWS Global Accelerator |

### Algorithm Selection

| Traffic Pattern | Algorithm |
|-----------------|-----------|
| Stateless, similar servers | Round Robin |
| Stateless, different capacity | Weighted Round Robin |
| Long-lived connections | Least Connections |
| Performance-sensitive | Least Response Time |
| Session persistence needed | IP Hash or Cookie |
| Varying server load | Resource-Based |

### Health Check Configuration

| Service Type | Check Type | Interval | Timeout |
|--------------|------------|----------|---------|
| Web app | HTTP /health | 10s | 3s |
| API | HTTP /health/ready | 10s | 5s |
| Database | TCP connect | 5s | 2s |
| Critical service | HTTP deep check | 5s | 3s |
| Background worker | HTTP /live | 30s | 5s |

## Summary

Load balancing is essential for distributing traffic, ensuring high availability, and enabling horizontal scaling. Choose L4 for raw performance and non-HTTP protocols, L7 for intelligent content-based routing. Prefer cloud-managed load balancers for simplicity and auto-scaling, self-managed for multi-cloud portability and advanced features. Implement proper health checks with hysteresis, avoid sticky sessions when possible, and monitor key metrics continuously.

For deployment patterns, see examples in `examples/aws/`, `examples/nginx/`, `examples/kubernetes/`, and other provider directories.
