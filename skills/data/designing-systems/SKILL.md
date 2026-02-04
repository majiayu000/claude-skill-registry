---
name: designing-systems
description: Design scalable, reliable software systems. Use when planning new systems, major features, or architecture changes. Covers C4 diagrams, trade-off analysis, and system decomposition.
allowed-tools: Read, Write, Glob, Grep
---

# Designing Systems

## Workflows

- [ ] **Requirements**: Gather functional and non-functional requirements
- [ ] **Diagrams**: Create C4 diagrams (Context, Container)
- [ ] **Data**: Define data model and storage strategy
- [ ] **API**: Define interfaces and contracts
- [ ] **Risks**: Identify single points of failure
- [ ] **Document**: Save to `./artifacts/adr_[topic].md`

## Feedback Loops

1. Draft design document
2. Review with stakeholders
3. Create POC for risky components
4. Refine design based on POC
5. Finalize ADR

## Blueprint Template

Every system design should include:

1. **High-Level Diagram**: Mermaid graph showing components
2. **Component Boundaries**: Clear responsibility definitions
3. **API Definitions**: OpenAPI or GraphQL specs
4. **Data Models**: Schema definitions
5. **Trade-off Analysis**: Rationale for key decisions

## C4 Model Levels

### Level 1: Context
Who uses the system? What external systems does it interact with?

### Level 2: Container
What are the major deployable units? (APIs, databases, queues)

### Level 3: Component
What are the major building blocks within each container?

### Level 4: Code
Class/function level (usually not needed in architecture docs)

## Trade-off Analysis

For major decisions, explicitly document:

| Decision | Option A | Option B |
|----------|----------|----------|
| Pros | ... | ... |
| Cons | ... | ... |
| When to Choose | ... | ... |

## Non-Functional Requirements

Always consider:
- **Scalability**: Expected load, growth rate
- **Availability**: SLA targets, failure modes
- **Latency**: P50, P95, P99 requirements
- **Security**: Authentication, authorization, data protection
- **Cost**: Infrastructure, operational overhead

## Resources

- [System Design Template](./resources/system-design.template.md)
- [ADR Template](./resources/adr.template.md)
