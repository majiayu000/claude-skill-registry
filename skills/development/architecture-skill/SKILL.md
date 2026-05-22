---
name: architecture
description: Comprehensive system architecture design and implementation workflow that orchestrates expert analysis, technical decision-making, and architectural pattern selection using the integrated toolset. Handles everything from initial system analysis to implementation-ready technical specifications.
license: Apache 2.0
tools: []
---

# Architecture Master - Complete System Architecture Design Workflow

## Overview

This skill provides end-to-end architecture design and implementation guidance by orchestrating multiple expert systems and tools available in this repository. It bridges business requirements with technical implementation, ensuring robust, scalable, and maintainable system architectures.

**Key Capabilities:**
- 🏗️ **Multi-Expert Architecture Analysis** - Coordinates system, backend, frontend, DevOps, and security architects
- 🎯 **Intelligent Pattern Selection** - Automatically selects appropriate architectural patterns based on requirements
- 📊 **Scalability Planning** - Designs for 10x growth with bottleneck analysis
- 🔒 **Security-First Design** - Integrates security considerations at every layer
- 📋 **Implementation Guidance** - Provides detailed implementation roadmaps and best practices

## When to Use This Skill

**Perfect for:**
- New system architecture design and planning
- Legacy system modernization and migration strategies
- Microservices decomposition and service boundary definition
- API design and integration architecture
- Performance optimization and scalability planning
- DevOps and infrastructure architecture design
- Security architecture and compliance requirements

**Triggers:**
- "Help me design the architecture for..."
- "I need to refactor/upgrade our system architecture"
- "Design a microservices architecture for..."
- "Create an API architecture for..."
- "Plan the DevOps infrastructure for..."
- "Design a scalable system architecture..."

## Architecture Expert Panel

The skill orchestrates multiple architectural perspectives:

### **System Architect** (Holistic Design)
- **Focus**: System boundaries, scalability, long-term maintainability
- **Patterns**: Microservices, DDD, Event Sourcing, CQRS
- **Considerations**: 10x growth, component coupling, technology evolution

### **Backend Architect** (Data & Services)
- **Focus**: API design, data integrity, fault tolerance
- **Patterns**: RESTful APIs, GraphQL, Database Architecture
- **Considerations**: ACID compliance, security, performance

### **Frontend Architect** (User Experience)
- **Focus**: Component architecture, state management, performance
- **Patterns**: SPA, Micro-Frontends, Progressive Web Apps
- **Considerations**: User experience, performance optimization

### **DevOps Architect** (Infrastructure & Reliability)
- **Focus**: CI/CD, observability, deployment strategies
- **Patterns**: IaC, Container Orchestration, Cloud Native
- **Considerations**: Reliability, monitoring, disaster recovery

### **Security Architect** (Protection & Compliance)
- **Focus**: Security by design, threat modeling, compliance
- **Patterns**: Zero Trust, Defense in Depth, Security Controls
- **Considerations**: Data protection, regulatory compliance

## Architecture Design Workflow

### Phase 1: Requirements Analysis & Context Understanding
**Use when**: Starting any architecture project

**Tools Used:**
```bash
/sc:analyze existing-system/requirements
/speckit.specify architecture-requirements
BMAD Architect Agent: *research {domain}
```

**Activities:**
- Analyze business requirements and technical constraints
- Evaluate existing system landscape and integration points
- Identify scalability and performance requirements
- Assess security and compliance requirements
- Map stakeholder concerns and success criteria

### Phase 2: System Analysis & Architecture Strategy
**Use when**: Understanding current state and defining approach

**Tools Used:**
```bash
/sc:analyze system-landscape
/sc:business-panel "system-analysis-and-approach"
System Architect Agent: holistic analysis
```

**Activities:**
- Map current system dependencies and interactions
- Identify architectural debt and technical constraints
- Evaluate technology stack and infrastructure capabilities
- Assess team skills and development processes
- Define architectural principles and constraints

### Phase 3: Pattern Selection & Design Decisions
**Use when**: Making key architectural choices

**Tools Used:**
```bash
/sc:spec-panel --experts "martin-fowler,sam-newman,michael-nygard" --focus architecture
/sc:design --type architecture system-components
OpenSpec: Architecture change proposal
```

**Activities:**
- Select appropriate architectural patterns (microservices, monolith, serverless)
- Define service boundaries and interaction patterns
- Design data architecture and persistence strategies
- Choose integration patterns and communication protocols
- Document architectural decisions with trade-off analysis

### Phase 4: Detailed Architecture Design
**Use when**: Creating comprehensive specifications

**Tools Used:**
```bash
/sc:design --type api --format spec rest-api-design
/sc:design --type database --format diagram data-architecture
BMAD Architect Agent: create-architecture-document
```

**Activities:**
- Design system components and their interfaces
- Define API specifications and data contracts
- Design database schemas and data models
- Plan caching, messaging, and integration strategies
- Create deployment and infrastructure architecture

### Phase 5: Security & Compliance Architecture
**Use when**: Ensuring robust security posture

**Tools Used:**
```bash
Security Architect Agent: comprehensive security analysis
/sc:troubleshoot "security-vulnerability-assessment"
Compliance Checklist validation
```

**Activities:**
- Conduct threat modeling and security assessment
- Design authentication, authorization, and encryption strategies
- Implement logging, monitoring, and audit capabilities
- Ensure compliance with relevant regulations (GDPR, SOC2, etc.)
- Define security controls and incident response procedures

### Phase 6: Implementation Planning & Roadmap
**Use when**: Creating implementation strategy

**Tools Used:**
```bash
/speckit.tasks architecture-implementation
/sc:spawn "architecture-implementation-coordination"
BMAD DevOps Agent: deployment-strategy
```

**Activities:**
- Create phased implementation roadmap
- Define migration strategies and rollback procedures
- Plan testing strategies and quality gates
- Design monitoring and observability architecture
- Generate team training and documentation plans

## Integration Patterns

### **SuperClaude Command Integration**

| Command | Use Case | Output |
|---------|---------|--------|
| `/sc:design` | Core architecture design | System diagrams, API specs |
| `/sc:spec-panel` | Expert review and validation | Quality-assured architecture |
| `/sc:analyze` | System analysis and assessment | Current state analysis |
| `/sc:business-panel` | Strategic alignment | Business-technical bridge |
| `/sc:spawn` | Complex implementation coordination | Cross-domain task management |

### **BMAD Agent Orchestration**

| Agent | Role | Capabilities |
|-------|------|------------|
| **Winston (Architect)** | Lead architect | Holistic system design, technology selection |
| **Backend Architect** | Service design | API design, database architecture |
| **Frontend Architect** | UI/UX architecture | Component design, performance |
| **DevOps Architect** | Infrastructure | CI/CD, deployment, monitoring |
| **Security Architect** | Security | Threat modeling, compliance |

### **Specialized MCP Agents**

| Agent | Expertise | Focus |
|-------|----------|-------|
| **System Architect** | Large-scale systems | Scalability, boundaries |
| **Backend Architect** | Data systems | Reliability, performance |
| **DevOps Architect** | Operations | Automation, reliability |
| **Cloud Architect** | Cloud infrastructure | Multi-cloud, optimization |

## Usage Examples

### Example 1: New Microservices System
```
User: "Help me design the architecture for an e-commerce platform with microservices"

Workflow:
1. Phase 1: Analyze e-commerce requirements and patterns
2. Phase 2: Evaluate monolith vs microservices approach
3. Phase 3: Service boundary definition and API contracts
4. Phase 4: Detailed service architecture and data flow
5. Phase 5: Payment processing security architecture
6. Phase 6: Implementation roadmap with migration strategy
```

### Example 2: Legacy System Modernization
```
User: "I need to modernize our 10-year-old monolithic application"

Workflow:
1. Phase 1: Comprehensive system analysis and assessment
2. Phase 2: Strangler Fig pattern planning and execution
3. Phase 3: Microservice decomposition strategy
4. Phase 4: API gateway and service mesh design
5. Phase 5: Data migration and modernization planning
6. Phase 6: Phased rollout and risk mitigation
```

### Example 3: High-Performance API System
```
User: "Design architecture for a high-performance API that handles millions of requests"

Workflow:
1. Phase 1: Performance requirements and load analysis
2. Phase 2: Scalability architecture and technology selection
3. Phase 3: API design with caching and optimization
4. Phase 4: Database architecture for high throughput
5. Phase 5: Monitoring and observability design
6. Phase 6: Performance testing and optimization roadmap
```

## Quality Assurance Mechanisms

### **Multi-Expert Validation**
- **Spec Panel**: Martin Fowler, Sam Newman, Michael Nygard review
- **Architectural Reviews**: Multiple architect perspectives and cross-validation
- **Pattern Compliance**: Ensure architectural patterns are correctly implemented
- **Security Validation**: Comprehensive security review and threat modeling

### **Automated Checks**
- **Scalability Analysis**: Automated bottleneck identification
- **Dependency Analysis**: System dependency mapping and risk assessment
- **Compliance Validation**: Regulatory and industry standard compliance checks
- **Performance Validation**: Performance modeling and bottleneck prediction

### **Best Practice Integration**
- **Industry Standards**: Adherence to architectural best practices
- **Technology Alignment**: Consistent with technology stack and organizational capabilities
- **Maintainability**: Future-proof design and evolution planning
- **Documentation Standards**: Comprehensive architectural documentation

## Output Deliverables

### Primary Deliverable: Complete Architecture Package
```
architecture-package/
├── docs/
│   ├── architecture-overview.md          # Executive summary
│   ├── system-architecture.md           # Detailed system design
│   ├── api-architecture.md              # API specifications
│   ├── data-architecture.md             # Data and database design
│   ├── security-architecture.md          # Security design
│   ├── deployment-architecture.md        # Infrastructure design
│   └── migration-strategy.md             # Implementation roadmap
├── diagrams/
│   ├── system-overview.png             # High-level architecture diagram
│   ├── component-diagram.png            # Component interaction diagram
│   ├── data-flow.png                    # Data flow diagram
│   └── deployment-diagram.png           # Deployment architecture
├── decisions/
│   ├── architectural-decisions.md      # Decision log with rationale
│   ├── trade-offs.md                   # Trade-off analysis
│   └── technology-selection.md         # Technology evaluation
├── checklists/
│   ├── architecture-review.md          # Quality validation checklist
│   ├── security-checklist.md           # Security validation
│   ├── performance-checklist.md        # Performance validation
│   └── scalability-checklist.md         # Scalability validation
└── implementation/
    ├── implementation-roadmap.md       # Phased implementation plan
    ├── team-guidelines.md            # Development team guidelines
    ├── testing-strategy.md            # Testing and validation plan
    └── monitoring-strategy.md          # Observability plan
```

### Supporting Artifacts
- **OpenSpec Change Files**: Structured architectural change proposals
- **BMAD Template Outputs**: Standardized architecture documentation
- **SpeckIT Task Plans**: Detailed implementation task breakdowns
- **Expert Panel Reports**: Multi-expert validation and recommendations

## Advanced Features

### **Intelligent Pattern Matching**
- Automatically suggests appropriate architectural patterns based on requirements
- Pattern library with implementation guidance and best practices
- Pattern evolution planning and adaptation strategies

### **Technology Stack Analysis**
- Evaluates existing technology stack against requirements
- Recommends technology upgrades and migration paths
- Considers team skills, organizational context, and budget constraints

### **Risk Assessment**
- Identifies architectural risks and failure modes
- Provides mitigation strategies and contingency planning
- Includes business impact analysis and risk scoring

### **Cost Optimization**
- Analyzes total cost of ownership (TCO) for architectural decisions
- Optimizes infrastructure costs and licensing strategies
- Balances technical excellence with financial reality

## Troubleshooting

### Common Architectural Challenges
- **Monolith to Microservices Transition**: Use Strangler Fig pattern with gradual migration
- **Performance Bottlenecks**: Comprehensive performance analysis with optimization strategies
- **Security Compliance**: Layered security approach with defense-in-depth principles
- **Team Skills Gap**: Training recommendations and hiring strategies

### Architecture Decision Recovery
- **Pattern Selection Issues**: Re-evaluate requirements and match patterns appropriately
- **Technology Trade-offs**: Re-assess technical decisions with updated requirements
- **Integration Challenges**: Design adaptive integration patterns and APIs
- **Scalability Problems**: Identify scaling bottlenecks and redesign hot components

## Best Practices

### **For System Design**
- Start with clear system boundaries and interfaces
- Design for failure with fault isolation and recovery
- Implement observability from the beginning
- Plan for evolution and future changes

### **For Technology Selection**
- Choose boring technology when possible
- Consider team expertise and learning curves
- Evaluate long-term maintenance and support
- Balance technical excellence with practical constraints

### **For Security**
- Implement security by design, not as an afterthought
- Use multiple layers of security controls
- Regular security assessments and penetration testing
- Stay updated with security best practices and threat landscapes

### **For Scalability**
- Design for horizontal scaling from the start
- Identify and optimize performance bottlenecks
- Use caching and data partitioning strategies
- Plan for capacity growth and load distribution

---

This architecture skill transforms the complex process of system architecture design into a guided, expert-supported workflow that leverages the full power of your integrated development toolset. It ensures that architectural decisions are well-reasoned, thoroughly validated, and aligned with both business requirements and long-term technical strategy.