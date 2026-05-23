---
name: project-architecture
description: System architecture, service boundaries, and data flow patterns. Use when making cross-module changes, adding new features, or understanding how components connect.
---

# Project Architecture

<!-- CUSTOMIZE THIS ENTIRE FILE FOR YOUR PROJECT -->
<!-- This is a TEMPLATE — replace everything below with your actual architecture -->

## System Overview
<!-- One paragraph describing what the system does and its core value proposition -->
[Describe your system here]

## Service Map
<!-- Show how services connect. Use text diagrams or just describe the flow -->
```
[Client] → [API Gateway] → [Service A] → [Database A]
                         → [Service B] → [Database B]
                         → [Service C] → [Queue] → [Worker]
```

## Key Data Flows
<!-- Describe the 2-3 most important flows through the system -->

### Flow 1: [Name — e.g. "User Authentication"]
1. Client sends credentials to `/api/auth/login`
2. Auth service validates against [user DB]
3. JWT issued with [claims]
4. Subsequent requests use Bearer token

### Flow 2: [Name — e.g. "Order Processing"]
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Architecture Decisions (ADRs)

### Why [Decision 1 — e.g. "Event-driven over REST for inter-service"]
- **Chose**: [what you chose]
- **Over**: [what you rejected]
- **Because**: [the actual reason]

### Why [Decision 2]
- **Chose**: [what]
- **Over**: [what]
- **Because**: [why]

## Boundaries & Rules
<!-- What should NEVER cross service boundaries? -->
- Services communicate via [REST/gRPC/events] only
- No direct database access across services
- Shared types live in [packages/shared or similar]
- [Any other hard boundaries]

## Deployment
<!-- How does code get to production? -->
- CI: [GitHub Actions / GitLab CI / etc]
- Staging: [how deployed]
- Production: [how deployed]
- Rollback: [procedure]
