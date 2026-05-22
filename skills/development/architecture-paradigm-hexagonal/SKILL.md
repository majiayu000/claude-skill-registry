---
name: architecture-paradigm-hexagonal
description: |

Triggers: hexagonal, architecture, ports-adapters, testability, infrastructure-independence
  Decouple domain logic from infrastructure using Hexagonal (Ports & Adapters) pattern.

  Triggers: hexagonal, ports-adapters, infrastructure-independence, domain-isolation

  Use when: business logic separation, infrastructure changes needed, testability critical
  DO NOT use when: selecting paradigms (use architecture-paradigms first), simple CRUD
version: 1.0.0
category: architectural-pattern
tags: [architecture, hexagonal, ports-adapters, infrastructure-independence, testability]
dependencies: []
tools: [boundary-validator, adapter-generator, contract-tester]
usage_patterns:
  - paradigm-implementation
  - refactoring-guidance
  - adr-support
  - infrastructure-migration
complexity: intermediate
estimated_tokens: 1200
---

# The Hexagonal (Ports & Adapters) Paradigm

## When to Employ This Paradigm
- When you anticipate frequent changes to databases, frameworks, or user interfaces and need the core domain logic to remain stable.
- When testing the core application requires mocking complex or slow infrastructure components.
- When the development team needs to provide clear inbound and outbound interfaces for third-party integrations.

## Adoption Steps
1. **Define Domain Ports**: Identify all interactions with the core domain. Define inbound "driver ports" for actors that initiate actions (e.g., UI, CLI, automated jobs) and outbound "driven ports" for services the application consumes (e.g., database, message bus, external APIs). Express these ports as formal interfaces.
2. **Implement Adapters at the Edge**: For each external technology, create an "adapter" that implements a port's interface. Keep the core domain entirely ignorant of the specific frameworks or libraries used in the adapters.
3. **Aggregate Use Cases**: Organize the application's functionality into services that are built around business capabilities. These services orchestrate calls to the domain through the defined ports.
4. **Implement Contract Testing**: validate that each adapter correctly honors the expectations of the port it implements. Use contract tests or consumer-driven contract tests to validate this behavior.
5. **Enforce Dependency Rules**: The most critical rule is that only adapters may have dependencies on external frameworks. Enforce this with automated architecture tests or static analysis rules.

## Key Deliverables
- An Architecture Decision Record (ADR) that formally names the ports, their corresponding adapters, and the dependency policies.
- A set of port interface definitions, stored with the core domain module.
- A suite of contract tests for each adapter, alongside unit tests for the domain and application services.
- Architectural diagrams showing the inbound and outbound data flows, for use by operations teams and architecture reviewers.

## Risks & Mitigations
- **Port/Interface Bloat**:
  - **Mitigation**: An excessive number of ports can increase maintenance overhead. Group related operations into more cohesive, higher-level ports, often organized around domain aggregates.
- **Leaky Abstractions**:
  - **Mitigation**: If a port's interface exposes details about the transport layer (e.g., HTTP headers), it is a "leaky abstraction." Refactor these interfaces to use domain-centric Data Transfer Objects (DTOs) instead.
- **Adapter Drift**:
  - **Mitigation**: An adapter can become out-of-sync with the external technology it represents (e.g., database schema changes). Schedule regular, automated validation of adapters, such as verifying that SQL migrations still align with the expectations of the persistence port.
## Troubleshooting

### Common Issues

**Command not found**
Ensure all dependencies are installed and in PATH

**Permission errors**
Check file permissions and run with appropriate privileges

**Unexpected behavior**
Enable verbose logging with `--verbose` flag
