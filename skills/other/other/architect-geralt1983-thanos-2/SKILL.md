---
name: System Architect
description: Software architecture, system design, and technical planning. USE WHEN user mentions architecture, design systems, refactor, restructure, scalability, patterns, tech debt, dependencies, or asks about how to structure or organize code.
---

# System Architect Skill

AI-powered system architecture guidance for designing, planning, and improving software systems with focus on maintainability, scalability, and clean code principles.

## What This Skill Does

This skill provides expert-level architectural guidance including system design, code organization, dependency management, pattern selection, and technical debt reduction. It combines software engineering best practices with practical, actionable recommendations.

**Key Capabilities:**
- **System Design**: Architecture diagrams, component design, API planning
- **Code Organization**: Module structure, separation of concerns, layered architectures
- **Pattern Selection**: Design patterns, architectural patterns, anti-pattern detection
- **Dependency Management**: Coupling analysis, interface design, dependency injection
- **Tech Debt Assessment**: Code health metrics, refactoring priorities, migration strategies
- **Scalability Planning**: Performance considerations, caching strategies, distributed systems

## Core Principles

### The SOLID Foundation
- **S**ingle Responsibility: Each module/class has one reason to change
- **O**pen/Closed: Open for extension, closed for modification
- **L**iskov Substitution: Subtypes must be substitutable for base types
- **I**nterface Segregation: Many specific interfaces > one general interface
- **D**ependency Inversion: Depend on abstractions, not concretions

### Architectural Qualities
1. **Maintainability** - Code that's easy to understand and modify
2. **Testability** - Components that can be tested in isolation
3. **Scalability** - Systems that grow gracefully with load
4. **Resilience** - Graceful degradation under failure
5. **Evolvability** - Ability to adapt to changing requirements

## Architecture Assessment Workflow

### 1. Initial Analysis
```
Analyze the current system:
├── Structure (directories, modules, packages)
├── Dependencies (internal and external)
├── Data Flow (how information moves)
├── Integration Points (APIs, databases, services)
└── Pain Points (what causes friction)
```

### 2. Architecture Metrics
- **Coupling Score**: How tightly connected are components?
- **Cohesion Score**: How focused are individual modules?
- **Complexity Index**: Cyclomatic and cognitive complexity
- **Dependency Depth**: How deep is the import chain?
- **Change Risk**: Which areas are most frequently modified?

### 3. Recommendations
Generate prioritized recommendations based on:
- Impact (how much improvement)
- Effort (how much work)
- Risk (what could break)
- Dependencies (what needs to happen first)

## Common Architectural Patterns

### Layered Architecture
```
┌─────────────────────────────────────┐
│           Presentation              │
├─────────────────────────────────────┤
│            Application              │
├─────────────────────────────────────┤
│             Domain                  │
├─────────────────────────────────────┤
│          Infrastructure             │
└─────────────────────────────────────┘
```
**Use When:** Traditional business applications, clear separation needed

### Hexagonal (Ports & Adapters)
```
              ┌───────────────────┐
   Adapters   │                   │   Adapters
 ┌──────────┐ │      Domain       │ ┌──────────┐
 │   API    │←│       Core        │→│    DB    │
 │   CLI    │ │                   │ │ External │
 └──────────┘ └───────────────────┘ └──────────┘
              Ports (Interfaces)
```
**Use When:** Core logic must be isolated from infrastructure

### Event-Driven
```
┌──────────┐     ┌──────────────┐     ┌──────────┐
│ Producer │────►│  Event Bus   │────►│ Consumer │
└──────────┘     └──────────────┘     └──────────┘
```
**Use When:** Loose coupling, async processing, scalable systems

### Microservices
```
┌─────────┐  ┌─────────┐  ┌─────────┐
│Service A│  │Service B│  │Service C│
└────┬────┘  └────┬────┘  └────┬────┘
     │            │            │
     └────────────┼────────────┘
            API Gateway
```
**Use When:** Independent deployment, team autonomy, scale by component

## Refactoring Strategies

### Strangler Fig Pattern
Gradually replace legacy system by routing new features to new code:
1. Identify a seam (boundary in the old system)
2. Build new functionality behind that seam
3. Route traffic to new implementation
4. Repeat until old system is gone

### Branch by Abstraction
Refactor in-place by introducing abstractions:
1. Create abstraction layer over existing code
2. Implement new version behind abstraction
3. Migrate consumers to abstraction
4. Switch implementation
5. Remove old code

### Parallel Run
Run old and new implementations simultaneously:
1. Route requests to both systems
2. Compare outputs
3. Verify correctness
4. Switch over when confident

## Code Organization Guidelines

### Directory Structure (Python Example)
```
project/
├── src/
│   ├── core/           # Domain logic, no external deps
│   │   ├── entities/
│   │   ├── services/
│   │   └── interfaces/
│   ├── adapters/       # External integrations
│   │   ├── database/
│   │   ├── api/
│   │   └── messaging/
│   ├── application/    # Use cases, coordination
│   │   ├── commands/
│   │   └── queries/
│   └── presentation/   # User-facing code
│       ├── cli/
│       └── web/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
└── config/
```

### Naming Conventions
- **Classes**: `UserService`, `PaymentProcessor` (noun + role)
- **Interfaces**: `IRepository`, `PaymentGateway` (capability)
- **Functions**: `calculate_total()`, `validate_input()` (verb + noun)
- **Modules**: `authentication`, `billing`, `notifications` (domain)

## Anti-Pattern Detection

### Common Anti-Patterns
| Anti-Pattern | Symptoms | Solution |
|--------------|----------|----------|
| **God Class** | Class with 1000+ lines, does everything | Extract cohesive responsibilities |
| **Spaghetti** | Deep nesting, unclear flow | Refactor to small functions |
| **Circular Deps** | A imports B imports A | Introduce interfaces |
| **Feature Envy** | Method uses other class's data more | Move method to data owner |
| **Shotgun Surgery** | One change touches many files | Group related code together |
| **Primitive Obsession** | Raw types everywhere | Create domain types |

## Dependency Analysis

### Healthy Dependencies
```
✓ Core → (nothing)
✓ Application → Core
✓ Adapters → Core
✓ Presentation → Application
```

### Unhealthy Dependencies
```
✗ Core → Database (infrastructure leak)
✗ Adapters → Adapters (coupling)
✗ Circular: A → B → A
```

### Analysis Commands
```bash
# Python dependency analysis
pipdeptree --graph-output png > deps.png
pydeps src/core --max-bacon 2

# TypeScript/JavaScript
npx madge --circular --extensions ts src/
npx depcruise --output-type dot src | dot -T svg > deps.svg
```

## When to Use This Skill

**Trigger Phrases:**
- "How should I structure..."
- "What's the best way to organize..."
- "This code is getting hard to maintain"
- "We need to refactor..."
- "How do I reduce coupling..."
- "What pattern should I use for..."
- "Help me design..."
- "Review the architecture of..."

**Example Requests:**
1. "How should I structure a new Python CLI app?"
2. "This file has grown to 2000 lines, help me break it up"
3. "We're adding a new feature, where should the code live?"
4. "Our tests are slow, is there an architectural issue?"
5. "Help me migrate from monolith to services"

## Architecture Review Checklist

Before implementing major changes:

- [ ] **Boundaries clear?** Can you draw boxes around components?
- [ ] **Dependencies one-way?** No circular imports?
- [ ] **Core isolated?** Domain logic has no infrastructure deps?
- [ ] **Testable?** Can you test components in isolation?
- [ ] **Scalable?** What happens with 10x load?
- [ ] **Evolvable?** How hard to add new features?
- [ ] **Observable?** Can you see what's happening?
- [ ] **Recoverable?** What happens when parts fail?

## Integration with Other Skills

- **Pair Programming**: Use architect mode for design phases
- **Code Review**: Architectural concerns in review process
- **Performance Analysis**: Architecture impacts performance
- **Testing**: Architecture determines test strategy

---

*Skill designed for Thanos + Antigravity integration*
