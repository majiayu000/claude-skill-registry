---
name: project-planner
description: Comprehensive project planning and documentation generator for software projects. Creates structured requirements documents, system design documents, and task breakdown plans with implementation tracking. Use when starting a new project, defining specifications, creating technical designs, or breaking down complex systems into implementable tasks. Supports user story format, acceptance criteria, component design, API specifications, and hierarchical task decomposition with requirement traceability.
---

# Project Planner Skill

This skill provides templates and guidance for generating comprehensive project planning documents that serve as blueprints for AI-assisted implementation.

## Quick Start

When a user wants to start a new project, generate three core documents:
1. **Requirements Document** - User stories with acceptance criteria
2. **Design Document** - Technical architecture and component specifications  
3. **Implementation Plan** - Hierarchical task breakdown with requirement tracing

## Why Explicit Architectural Planning Works

Setting clear roles, responsibilities, and deliverables upfront dramatically improves project outcomes:

### Benefits of Upfront Definition

1. **Component Clarity** - Defining all system components first prevents scope creep and ensures complete coverage
2. **Data Flow Visibility** - Mapping data movement early reveals integration complexities and performance bottlenecks
3. **Integration Planning** - Identifying all touchpoints upfront prevents surprise dependencies during implementation
4. **Clear Boundaries** - Explicitly stating what's in/out of scope focuses effort and prevents feature drift
5. **Measurable Success** - Specific goals and constraints enable objective progress tracking

### The Architect Mindset

When acting as a **Project Architect**, approach planning with:
- **Systems Thinking** - See the whole before diving into parts
- **Interface-First Design** - Define contracts between components before internals
- **Traceability Focus** - Every requirement maps to design elements and tasks
- **Constraint Awareness** - Acknowledge limitations upfront to guide decisions
- **Deliverable Orientation** - Know exactly what artifacts you're producing

## Document Generation Workflow

### 1. Project Architect Role Definition

When starting a project, explicitly establish Claude as the **Project Architect** with clear responsibilities:

**Role:** System Architect and Planning Specialist
**Responsibilities:**
- Define complete system architecture with all components
- Map data flow between system elements
- Identify all integration points and interfaces
- Establish clear project boundaries and constraints
- Create traceable requirements to implementation tasks

### 2. Initial Project Understanding

Before generating documents, gather key information and architectural elements:

```
Required Project Information:
- Project name and purpose
- Target users (single-user local, multi-tenant SaaS, etc.)
- Core functionality (3-5 main features)
- Technical preferences (languages, frameworks, deployment)
- Non-functional requirements (performance, security, scalability)

Required Architectural Elements (define upfront):
- System Components: All major modules/services and their purposes
- Data Flow: How data moves through the entire system
- Integration Points: All external APIs, services, databases
- System Boundaries: What's in scope vs out of scope
- Constraints: Technical, business, and resource limitations
- Success Metrics: Clear, measurable goals for the system
```

### 3. Deliverable Definition (Set Upfront)

Define all deliverables explicitly before starting documentation:

```
Standard Deliverables Package:
1. Requirements Document
   - User stories with measurable acceptance criteria
   - Complete glossary of terms
   - Traceable requirement IDs
   
2. System Design Document  
   - Component architecture diagram
   - Data flow diagrams for all major processes
   - Integration point specifications
   - API/Interface contracts
   - Performance and scaling targets
   
3. Implementation Plan
   - Hierarchical task breakdown
   - Requirement-to-task mapping
   - Dependency graph
   - Phase-based delivery schedule

Optional Deliverables (specify if needed):
- API Documentation
- Database Schema Design
- Security Threat Model
- Deployment Guide
- Testing Strategy Document
```

### 4. Generate Requirements Document

Use the requirements template to create user-focused specifications:

```python
# Execute this to generate requirements structure
requirements = {
    "introduction": "System purpose and scope",
    "glossary": "Domain-specific terms",
    "requirements": [
        {
            "id": "REQ-X",
            "user_story": "As a [role], I want [feature], so that [benefit]",
            "acceptance_criteria": [
                "WHEN [condition], THE system SHALL [behavior]",
                "WHERE [context], THE system SHALL [behavior]",
                "IF [condition], THEN THE system SHALL [behavior]"
            ]
        }
    ]
}
```

### 5. Generate Design Document

Create technical specifications with explicit architectural elements:

```python
# Execute this to generate comprehensive design structure
design = {
    "overview": "High-level system description",
    "architecture": {
        "diagram": "ASCII or visual representation of all components",
        "components": [
            {
                "id": "COMP-1",
                "name": "Component Name",
                "type": "Frontend/Backend/Service/Database",
                "responsibility": "Single clear purpose",
                "boundaries": "What it does and doesn't do"
            }
        ]
    },
    "data_flow": {
        "primary_flows": [
            {
                "name": "User Registration Flow",
                "steps": [
                    "1. User submits form → Frontend",
                    "2. Frontend validates → API Gateway",
                    "3. API Gateway → Auth Service",
                    "4. Auth Service → User Database",
                    "5. Response flows back"
                ],
                "data_transformations": "How data changes at each step"
            }
        ]
    },
    "integration_points": [
        {
            "name": "External Payment API",
            "type": "REST/GraphQL/WebSocket/Database",
            "purpose": "Process payments",
            "interface": "API contract definition",
            "authentication": "Method used",
            "error_handling": "Retry/fallback strategy"
        }
    ],
    "components_detail": [
        {
            "name": "Component Name",
            "responsibility": "What it does",
            "key_classes": ["Class descriptions"],
            "interfaces": "API/method signatures",
            "dependencies": "What it needs to function",
            "performance": "Targets and constraints"
        }
    ],
    "data_models": "Entity definitions with relationships",
    "system_boundaries": {
        "in_scope": ["What the system handles"],
        "out_of_scope": ["What it delegates or ignores"],
        "assumptions": ["External dependencies assumed available"]
    },
    "error_handling": "Strategies for failures",
    "testing_strategy": "Unit, integration, performance",
    "deployment": "Docker, environment, configuration"
}
```

### 6. Generate Implementation Plan

Break down the project into executable tasks with clear scope boundaries:

```python
# Execute this to generate task structure with boundaries
tasks = {
    "project_boundaries": {
        "must_have": ["Core features for MVP"],
        "nice_to_have": ["Enhancement features"],
        "out_of_scope": ["Features explicitly excluded"],
        "technical_constraints": ["Framework/library limitations"]
    },
    "phases": [
        {
            "id": 1,
            "name": "Infrastructure Setup",
            "deliverables": ["What this phase produces"],
            "tasks": [
                {
                    "id": "1.1",
                    "description": "Task description",
                    "subtasks": ["Specific actions"],
                    "requirements_fulfilled": ["REQ-1.1", "REQ-2.3"],
                    "components_involved": ["COMP-1", "COMP-3"],
                    "dependencies": [],
                    "estimated_hours": 4,
                    "success_criteria": "How to verify completion"
                }
            ]
        }
    ]
}
```

## Requirements Document Template

```markdown
# Requirements Document

## Introduction

[System description in 2-3 sentences. Target user and deployment model.]

## Glossary

- **Term**: Definition specific to this system
- **Component**: Major system module or service
[Add all domain-specific terms]

## Requirements

### Requirement [NUMBER]

**User Story:** As a [user type], I want [capability], so that [benefit]

#### Acceptance Criteria

1. WHEN [trigger/condition], THE [component] SHALL [action/behavior]
2. WHERE [mode/context], THE [component] SHALL [action/behavior]  
3. IF [condition], THEN THE [component] SHALL [action/behavior]
4. THE [component] SHALL [capability with measurable target]

[Repeat for each requirement]
```

### Requirements Best Practices

1. **One capability per requirement** - Each requirement should address a single feature
2. **Testable criteria** - Every criterion must be verifiable
3. **Use SHALL for mandatory** - Consistent RFC 2119 keywords
4. **Include performance targets** - "within X milliseconds/seconds"
5. **Specify all states** - Success, failure, edge cases
6. **Number systematically** - REQ-1, REQ-2 for traceability

### Acceptance Criteria Patterns

```
Behavior criteria:
- WHEN [event occurs], THE system SHALL [respond]
- THE system SHALL [provide capability]
- THE system SHALL [enforce rule/limit]

Conditional criteria:
- IF [condition], THEN THE system SHALL [action]
- WHERE [mode is active], THE system SHALL [behavior]

Performance criteria:
- THE system SHALL [complete action] within [time]
- THE system SHALL support [number] concurrent [operations]
- THE system SHALL maintain [metric] above/below [threshold]

Data criteria:
- THE system SHALL persist [data type] with [attributes]
- THE system SHALL validate [input] against [rules]
- THE system SHALL return [data] in [format]
```

## Design Document Template

```markdown
# Design Document

## Overview

[System architecture summary in 3-4 sentences. Key design decisions and priorities.]

## System Architecture

### Component Map

| Component ID | Name | Type | Responsibility | Interfaces With |
|-------------|------|------|----------------|-----------------|
| COMP-1 | Web Frontend | UI | User interface | COMP-2 |
| COMP-2 | API Gateway | Service | Request routing | COMP-3, COMP-4 |
| COMP-3 | Business Logic | Service | Core processing | COMP-5 |
[Complete component inventory]

### High-Level Architecture Diagram

[ASCII diagram showing all components and their relationships]

## Data Flow Specifications

### Primary Data Flows

#### 1. [Flow Name] (e.g., User Authentication)

```
1. [Source] → [Component]: [Data description]
2. [Component] → [Component]: [Transformation applied]
3. [Component] → [Destination]: [Final data format]
```

**Data Transformations:**
- Step 2: [How data changes]
- Step 3: [Validation/Processing applied]

[Repeat for each major data flow]

## Integration Points

### Internal Integration Points

| Source | Target | Protocol | Data Format | Purpose |
|--------|--------|----------|-------------|---------|
| Frontend | API Gateway | HTTPS/REST | JSON | API calls |
| API Gateway | Auth Service | gRPC | Protobuf | Authentication |
[All internal integrations]

### External Integration Points

#### [External System Name]

**Type:** REST API / Database / Message Queue / etc.
**Purpose:** [What this integration provides]
**Endpoint:** [URL/Connection string pattern]
**Authentication:** [Method - OAuth2, API Key, etc.]
**Rate Limits:** [Any constraints]

**Interface Contract:**
```language
// Request format
POST /api/endpoint
{
    "field": "type"
}

// Response format  
{
    "result": "type"
}
```

**Error Handling:**
- Retry strategy: [Exponential backoff, circuit breaker]
- Fallback: [What happens if unavailable]
- Monitoring: [How to detect issues]

[Repeat for each external integration]

## Components and Interfaces

### 1. [Component Name]

**Responsibility:** [Single sentence description]

**Key Classes:**
- `ClassName`: [Purpose and main methods]
- `ServiceName`: [What it manages]

**Interfaces:**
```language
class InterfaceName:
    def method_name(params) -> ReturnType
    # Core methods only
```

**Data Flow:**
- Receives [input] from [source]
- Processes by [algorithm/logic]
- Outputs [result] to [destination]

**Performance:**
- Target: [metric and value]
- Constraints: [limitations]

[Repeat for each major component]

## Data Models

### [Entity Name]
```language
@dataclass
class EntityName:
    field: Type
    field: Optional[Type]
    # Core fields only
```

## Error Handling

### [Error Category]
**Types:** [List of error scenarios]
**Handling:** [Strategy and recovery]

## Testing Strategy

### Unit Tests
- [Component]: Test [aspects]
- Coverage target: 80%

### Integration Tests
- [Flow]: Test [end-to-end scenario]

### Performance Tests
- [Operation]: Target [metric]

## Deployment

### Docker Configuration
```yaml
# Essential service definitions only
```

### Environment Variables
```
CATEGORY_VAR=description
```

## Performance Targets

- [Operation]: <[time]
- [Throughput]: >[rate]
- [Resource]: <[limit]

## Security Considerations

- [Authentication method if applicable]
- [Data protection approach]
- [Access control model]
```

### Design Best Practices

1. **Component responsibilities** - Single, clear purpose per component
2. **Interface first** - Define contracts before implementation
3. **Data flow clarity** - Show how data moves through system
4. **Error categories** - Group related failures with consistent handling
5. **Performance targets** - Specific, measurable goals
6. **Deployment ready** - Include Docker and configuration

## Implementation Plan Template

```markdown
# Implementation Plan

- [x] 1. [Phase Name]
  
  - [x] 1.1 [Task name]
    - [Subtask description]
    - [Subtask description]
    - _Requirements: [REQ-X.Y, REQ-A.B]_
    
  - [ ] 1.2 [Task name]
    - [Subtask description]
    - _Requirements: [REQ-X.Y]_
    - _Dependencies: Task 1.1_

- [ ] 2. [Phase Name]

  - [ ] 2.1 [Task name]
    - [Detailed steps or subtasks]
    - _Requirements: [REQ-X.Y]_
    - _Dependencies: Phase 1_

[Continue for all phases]
```

### Task Planning Best Practices

1. **Hierarchical structure** - Phases > Tasks > Subtasks
2. **Requirement tracing** - Link each task to requirements
3. **Dependency marking** - Identify blockers and prerequisites  
4. **Checkbox format** - [x] for complete, [ ] for pending
5. **Atomic tasks** - Each task independently completable
6. **Progressive implementation** - Infrastructure → Core → Features → Polish

### Common Implementation Phases

```markdown
1. **Infrastructure Setup**
   - Project structure
   - Database schema
   - Docker configuration
   - Core dependencies

2. **Data Layer**
   - Models/entities
   - Database operations
   - Migrations

3. **Business Logic**
   - Core algorithms
   - Service classes
   - Validation rules

4. **API/Interface Layer**
   - REST/GraphQL endpoints
   - WebSocket handlers
   - Authentication

5. **Frontend/UI**
   - Component structure
   - State management
   - API integration
   - Responsive design

6. **Integration**
   - External services
   - Third-party APIs
   - Message queues

7. **Testing**
   - Unit tests
   - Integration tests
   - End-to-end tests

8. **DevOps**
   - CI/CD pipeline
   - Monitoring
   - Logging
   - Deployment scripts

9. **Documentation**
   - API documentation
   - User guides
   - Deployment guide
   - README
```

## Document Patterns by Project Type

### Web Application (Full-Stack)

Requirements focus:
- User authentication and authorization
- CRUD operations for entities
- Real-time updates
- Responsive UI
- API design

Design focus:
- 3-tier architecture (Frontend, Backend, Database)
- REST/GraphQL API design
- State management strategy
- Component hierarchy
- Database schema

Tasks focus:
1. Database and backend setup
2. API implementation
3. Frontend components
4. Integration and testing

### Microservices System

Requirements focus:
- Service boundaries
- Inter-service communication
- Data consistency
- Service discovery
- Fault tolerance

Design focus:
- Service decomposition
- API contracts between services
- Message queue/event bus
- Distributed tracing
- Container orchestration

Tasks focus:
1. Service scaffolding
2. Shared libraries/contracts
3. Individual service implementation
4. Integration layer
5. Orchestration setup

### Data Pipeline/ETL

Requirements focus:
- Data sources and formats
- Transformation rules
- Data quality checks
- Schedule/triggers
- Error handling and retry

Design focus:
- Pipeline stages
- Data flow diagram
- Schema evolution
- Monitoring and alerting
- Storage strategy

Tasks focus:
1. Data source connectors
2. Transformation logic
3. Validation and quality checks
4. Scheduling setup
5. Monitoring implementation

### CLI Tool/Library

Requirements focus:
- Command structure
- Input/output formats
- Configuration options
- Error messages
- Performance requirements

Design focus:
- Command parser architecture
- Plugin system (if applicable)
- Configuration management
- Output formatters
- Testing strategy

Tasks focus:
1. Core command structure
2. Business logic implementation
3. Input/output handlers
4. Configuration system
5. Documentation and examples

## Generating Documents for Specific Domains

### Trading/Financial Systems

Additional requirements:
- Risk management rules
- Order execution logic
- Market data handling
- Compliance requirements
- Audit trail

Additional design:
- High-frequency data handling
- Position tracking
- Risk calculations
- Order routing
- Failover strategies

### Real-time Systems (Chat, Gaming, IoT)

Additional requirements:
- Latency targets
- Connection handling
- State synchronization
- Offline support
- Push notifications

Additional design:
- WebSocket/SSE architecture
- State management
- Caching strategy
- Message queuing
- Horizontal scaling

### Machine Learning Systems

Additional requirements:
- Model training pipeline
- Feature engineering
- Model versioning
- Prediction API
- Monitoring/drift detection

Additional design:
- Training infrastructure
- Feature store
- Model registry
- Serving architecture
- A/B testing framework

## Quality Checklist

Before finalizing documents, verify:

### Requirements Document
- [ ] Every requirement has a clear user story
- [ ] All acceptance criteria are testable
- [ ] Non-functional requirements specified (performance, security)
- [ ] Glossary covers all domain terms
- [ ] Requirements are numbered for tracing

### Design Document
- [ ] Architecture diagram included
- [ ] All components have clear responsibilities
- [ ] Interfaces defined for integration points
- [ ] Error handling strategy documented
- [ ] Performance targets specified
- [ ] Deployment configuration included

### Implementation Plan
- [ ] Tasks grouped into logical phases
- [ ] Dependencies identified between tasks
- [ ] Requirements traced to tasks
- [ ] Tasks are atomic and completable
- [ ] Checkbox format for progress tracking

## Example Usage Patterns

### Starting a New Project (With Explicit Architecture Focus)

```
User: "I want to build an order flow trading automation system"

Response: "I'll act as your Project Architect to create comprehensive planning documents. 

First, let me establish the architectural foundation:

**System Components I need to define:**
- Market data ingestion service
- Order flow analysis engine  
- Trading signal generator
- Risk management module
- Order execution service
- Monitoring dashboard

**Data Flows to map:**
- Market data → Analysis → Signals → Execution
- Position tracking → Risk calculation → Trading limits
- All events → Audit trail

**Integration Points to specify:**
- Exchange APIs (which ones?)
- Database system (time-series data needs?)
- Notification services (alerts/reporting?)

**Key Questions:**
1. Is this for personal use (single-user) or a platform (multi-user)?
2. Which specific exchanges/brokers will it connect to?
3. What are your latency requirements (milliseconds matter)?
4. What's your risk tolerance and position sizing approach?
5. Do you need backtesting capabilities?

**Deliverables I'll create:**
1. Requirements document with traceable user stories
2. System design with complete component map and data flows
3. Implementation plan with phased delivery milestones

This architectural blueprint will ensure nothing is overlooked during implementation."
```

### Starting a New Project (Simple Approach)

```
User: "I want to build an order flow trading automation system"

Response: "I'll help you create comprehensive planning documents for your trading system. Let me gather some key information:

1. Is this for personal use (single-user) or a multi-user platform?
2. Which markets/exchanges will it connect to?
3. What are the core trading strategies or patterns?
4. Any specific performance requirements (latency, throughput)?

Based on this, I'll generate:
- Requirements document with user stories
- System design with components and data flow
- Implementation plan with phases and tasks"
```

### Expanding Existing Requirements

```
User: "Add real-time monitoring dashboard to the requirements"

Response: "I'll add dashboard requirements to your document:

### Requirement 15
**User Story:** As a trader, I want a real-time dashboard, so that I can monitor system performance and trading activity

#### Acceptance Criteria
1. THE Dashboard SHALL display active positions with current P&L
2. THE Dashboard SHALL update market data within 1 second
3. THE Dashboard SHALL provide filtering by symbol, timeframe, and date range
4. WHEN a trade executes, THE Dashboard SHALL reflect it within 100ms"
```

## Common Pitfalls to Avoid

### Planning Pitfalls
1. **Skipping architectural planning** - Jumping to requirements without mapping components first
2. **Vague role definition** - Not establishing the architect role leads to unfocused documentation
3. **Hidden integration points** - Discovering external dependencies during implementation
4. **Undefined boundaries** - No clear scope leads to feature creep and timeline slippage
5. **Missing data flow analysis** - Not mapping how data moves reveals issues late

### Requirements Pitfalls
1. **Over-specifying implementation** - Requirements should define "what" not "how"
2. **Vague acceptance criteria** - Avoid "user-friendly" or "fast" without metrics
3. **Missing error cases** - Include failure scenarios in requirements
4. **Untraceable requirements** - Every requirement should map to tasks

### Design Pitfalls
1. **Monolithic components** - Break down large components into focused services
2. **Circular dependencies** - Ensure task dependencies form a DAG
3. **Missing data models** - Define core entities early
4. **Ignoring deployment** - Include Docker/deployment from the start
5. **Unclear component boundaries** - Each component needs explicit responsibilities

## Output Format

Generate documents in Markdown format for easy editing and version control. Use:
- Clear hierarchical headings (##, ###, ####)
- Code blocks with language hints
- Bulleted and numbered lists
- Tables for structured data
- Checkboxes for task tracking
- Bold for emphasis on key terms
- Inline code for technical terms

Save documents as:
- `requirements.md` - Requirements document
- `design.md` - Design document
- `tasks.md` - Implementation plan

These documents serve as the foundation for AI-assisted implementation, providing clear specifications that can be referenced throughout development.
