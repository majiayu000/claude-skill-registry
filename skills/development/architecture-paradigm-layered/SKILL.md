---
name: architecture-paradigm-layered
description: |

Triggers: monolith, separation-of-concerns, n-tier, architecture, layered
  Use a Layered (N-Tier) architecture to separate presentation, domain logic, and
  data access responsibilities within a system.

  Triggers: layered architecture, n-tier, separation of concerns, presentation layer,
  data access layer, service layer, traditional architecture, monolith structure,
  layer enforcement, dependency direction

  Use when: building traditional applications with clear boundaries, working with
  moderate-sized teams, needing familiar and well-understood patterns, compliance
  requirements demand clear separation

  DO NOT use when: selecting from multiple paradigms - use architecture-paradigms first.
  DO NOT use when: high scalability needs independent component scaling.
  DO NOT use when: teams need independent deployment cycles - use microservices.

  Consult this skill when implementing layered patterns or enforcing layer boundaries.
version: 1.0.0
category: architectural-pattern
tags: [architecture, layered, n-tier, separation-of-concerns, monolith]
dependencies: []
tools: [dependency-validator, layer-enforcer, architecture-compliance-checker]
usage_patterns:
  - paradigm-implementation
  - legacy-system-modernization
  - team-structure-alignment
  - compliance-requirements
complexity: low
estimated_tokens: 700
---

# The Layered (N-Tier) Architecture Paradigm

## When to Employ This Paradigm
- When teams need clear architectural boundaries and a familiar structure for moderate-sized systems.
- When compliance or operations teams require clear separation of concerns (e.g., UI vs. domain logic vs. persistence).
- When the deployment artifact remains a monolith, but code clarity and separation are degrading.

## When NOT to Use This Paradigm
- When high scalability demands require independent scaling of components
- When multiple teams need independent deployment cycles
- When complex business logic requires frequent cross-layer communication
- When microservices architecture is already planned or in place
- When real-time processing requirements make layered communication too slow

## Adoption Steps
1. **Define the Layers**: Establish a clear set of layers. A common stack includes: Presentation -> Application/Service -> Domain -> Data Access.
2. **Enforce Dependency Direction**: Code in a given layer may only depend on the layer immediately below it. Forbid any "upward" dependencies or imports.
3. **Centralize Cross-Cutting Concerns**: Implement concerns like logging, authentication, and validation as centralized middleware or policies, rather than duplicating this logic in each layer.
4. **Test Each Layer Appropriately**: Apply testing strategies suitable for each layer, such as unit tests for the domain layer, service-layer tests for orchestration logic, and integration tests for persistence adapters.
5. **Document and Enforce Interactions**: Maintain up-to-date dependency diagrams and use automated architecture tests to prevent developers from creating "shortcut" dependencies that violate the layering rules.

## Key Deliverables
- An Architecture Decision Record (ADR) that captures the responsibilities of each layer, the allowed dependencies between them, and the policy for any exceptions.
- A formal dependency diagram stored with the project documentation.
- Automated architectural checks (e.g., using ArchUnit, dep-cruise, or custom scripts) to prevent rule violations from being merged.

## Technology Guidance

**Layer Implementation Patterns**:
- **Presentation Layer**: React/Vue/Angular (Frontend), MVC Controllers (Backend)
- **Application Layer**: Service classes, Application services, Use case orchestrators
- **Domain Layer**: Business entities, Domain services, Business rules validation
- **Data Access Layer**: Repository pattern, ORM mappers, Data access objects (DAO)

**Architecture Enforcement Tools**:
- **Java**: ArchUnit for dependency rule testing
- **JavaScript/TypeScript**: ESLint rules with dependency tracking
- **C#**: NDepend for architectural analysis
- **Python**: Custom decorators and import analysis tools

**Common Layer Stacks**:
- **3-Layer**: Presentation → Business Logic → Data Access
- **4-Layer**: Presentation → Application → Domain → Infrastructure
- **5-Layer**: UI → Controller → Service → Domain → Persistence

## Real-World Examples

**Enterprise ERP Systems**: SAP and Oracle ERP use layered architecture to separate user interfaces from business logic and database operations, enabling different frontend applications to share the same business rules.

**Banking Applications**: Financial institutions employ layered architecture to maintain strict separation between customer-facing interfaces, transaction processing, and secure data storage for regulatory compliance.

**E-commerce Platforms**: Traditional e-commerce sites use layered architecture to separate product catalogs, shopping cart logic, order processing, and payment handling into distinct layers.

## Risks & Mitigations
- **Excessive Rigidity and Latency**:
  - **Mitigation**: For features that span multiple layers, strict adherence can lead to excessive "pass-through" code and increased latency. In such cases, consider using a Façade pattern to provide a more direct interface where appropriate.
- **"Leaky" Layers**:
  - **Mitigation**: Developers may be tempted to bypass architectural rules for expediency, which degrades the architecture. Treat all architectural violations as build-breaking failures or critical issues in code review.
## Troubleshooting

### Common Issues

**Command not found**
Ensure all dependencies are installed and in PATH

**Permission errors**
Check file permissions and run with appropriate privileges

**Unexpected behavior**
Enable verbose logging with `--verbose` flag
