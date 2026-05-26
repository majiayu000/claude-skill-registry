---
name: arch
description: Load architecture patterns from the Claude Code Optimization Framework. Supports hybrid, mono, ms (microservices), and sls (serverless) patterns.
argument-hint: "<pattern> - Choose: hybrid, mono, ms, sls"
---

# Architecture Pattern Loader

When invoked with `/arch <pattern>`, load the corresponding architecture configuration.

## Supported Patterns

### @arch:hybrid (or /arch hybrid)
**File**: `C:\.claude\architectures\hybrid.yaml`
Use for: Legacy modernization, brownfield projects, multi-tier enterprise systems

### @arch:mono (or /arch mono)
**File**: `C:\.claude\architectures\monolith.yaml`
Use for: Small-medium applications, rapid prototyping, single-team projects

**Variants**:
- `@mono:3tier` - Classic 3-tier (Presentation, Business, Data)
- `@mono:clean` - Clean Architecture (Domain-centric)
- `@mono:hex` - Hexagonal/Ports & Adapters
- `@mono:vertical` - Vertical Slice Architecture
- `@mono:modular` - Modular Monolith (pre-microservices)

### @arch:ms (or /arch ms)
**File**: `C:\.claude\architectures\microservices.yaml`
Use for: Large-scale distributed systems, multi-team development, independent deployability

**Includes**:
- Saga patterns (Choreography/Orchestration)
- Circuit breakers
- Service mesh configuration
- Event-driven communication

### @arch:sls (or /arch sls)
**File**: `C:\.claude\architectures\serverless.yaml`
Use for: Event-driven workloads, variable traffic, cost optimization

**Includes**:
- AWS Lambda / Azure Functions patterns
- Step Functions / Durable Functions
- API Gateway integration
- Cold start optimization

## How to Use

1. Load pattern: `/arch ms`
2. The configuration will be applied to code generation
3. Use with other shortcuts: `@arch:ms @dotnet @deploy:k8s`

## Behavior
When loaded, the architecture pattern guides:
- Project structure recommendations
- Code organization patterns
- Communication patterns
- Data management strategies
- Deployment considerations
