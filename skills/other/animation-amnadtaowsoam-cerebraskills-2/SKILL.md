---
id: SKL-animation-ANIMATION
name: Animation
description: Creating efficient and beautiful animations is crucial for creating impressive
  user experiences in digital transformation era where users expect smooth, immediate,
  and responsive interactions. Animati
version: 1.0.0
status: active
owner: '@cerebra-team'
last_updated: '2026-02-22'
category: Backend
tags:
- api
- backend
- server
- database
stack:
- Python
- Node.js
- REST API
- GraphQL
difficulty: Intermediate
---

# Animation

## Skill Profile
*(Select at least one profile to enable specific modules)*
- [ ] **DevOps**
- [x] **Backend**
- [ ] **Frontend**
- [ ] **AI-RAG**
- [ ] **Security Critical**

## Overview
Creating efficient and beautiful animations is crucial for creating impressive user experiences in digital transformation era where users expect smooth, immediate, and responsive interactions. Animations are not just decoration; they are essential for communicating system status, guiding actions, and creating emotional connections with users. This skill covers use of major Animation Libraries in React ecosystem, including CSS Animations, Framer Motion, GSAP, and React Spring, with code examples and best practices for creating animations that are efficient, performant, and accessible.

## Why This Matters
- **Increases Conversion Rate**: Good animations help guide users to desired actions (Call-to-Action); studies show good animations can increase conversion rates by 15-20%
- **Reduces Bounce Rate**: Good loading animations and micro-interactions reduce perception that system is slow, keeping users on website longer
- **Enhances Brand Differentiation**: Unique animations create differentiation from competitors and build strong brand recall
- **Improves User Retention**: Good animations create satisfaction in usage, making users return to use application again
- **Reduces Support Costs**: Animations that guide usage (Onboarding Animations) can reduce questions and usage problems
- **Builds Trust**: Smooth, professional animations create positive perception of quality and reliability

---

## Core Concepts & Rules

### 1. Core Principles
- Follow established patterns and conventions
- Maintain consistency across codebase
- Document decisions and trade-offs

### 2. Implementation Guidelines
- Start with the simplest viable solution
- Iterate based on feedback and requirements
- Test thoroughly before deployment


## Inputs / Outputs / Contracts
* **Inputs**:
  - Design specifications and animations
  - User interaction requirements
  - Performance requirements
  - Accessibility guidelines
* **Entry Conditions**:
  - Animation library is installed
  - Design system is established
  - Performance baseline is measured
* **Outputs**:
  - Animated components
  - Animation configurations
  - Performance-optimized code
  - Accessible implementations
* **Artifacts Required (Deliverables)**:
  - Reusable animation components
  - Animation hooks and utilities
  - Performance monitoring setup
  - Accessibility testing results
* **Acceptance Evidence**:
  - Animations run smoothly at 60 FPS
  - CLS score < 0.1
  - Accessibility passes WCAG 2.1
  - Bundle size impact is minimal
* **Success Criteria**:
  - Animations are smooth and performant
  - Accessibility requirements are met
  - Performance targets are achieved
  - User feedback is positive

## Skill Composition
* **Depends on**: [nextjs-patterns](../nextjs-patterns/SKILL.md), [react-best-practices](../react-best-practices/SKILL.md)
* **Compatible with**: [error-boundaries-react](../error-boundaries-react/SKILL.md), [state-management](../state-management/SKILL.md)
* **Conflicts with**: None
* **Related Skills**: [tailwind-patterns](../tailwind-patterns/SKILL.md), [mui-material](../mui-material/SKILL.md)

---

## Quick Start / Implementation Example

1. Review requirements and constraints
2. Set up development environment
3. Implement core functionality following patterns
4. Write tests for critical paths
5. Run tests and fix issues
6. Document any deviations or decisions

```python
# Example implementation following best practices
def example_function():
    # Your implementation here
    pass
```


## Assumptions / Constraints / Non-goals

* **Assumptions**:
  - Development environment is properly configured
  - Required dependencies are available
  - Team has basic understanding of domain
* **Constraints**:
  - Must follow existing codebase conventions
  - Time and resource limitations
  - Compatibility requirements
* **Non-goals**:
  - This skill does not cover edge cases outside scope
  - Not a replacement for formal training


## Compatibility & Prerequisites

* **Supported Versions**:
  - Python 3.8+
  - Node.js 16+
  - Modern browsers (Chrome, Firefox, Safari, Edge)
* **Required AI Tools**:
  - Code editor (VS Code recommended)
  - Testing framework appropriate for language
  - Version control (Git)
* **Dependencies**:
  - Language-specific package manager
  - Build tools
  - Testing libraries
* **Environment Setup**:
  - `.env.example` keys: `API_KEY`, `DATABASE_URL` (no values)


## Test Scenario Matrix (QA Strategy)

| Type | Focus Area | Required Scenarios / Mocks |
| :--- | :--- | :--- |
| **Unit** | Core Logic | Must cover primary logic and at least 3 edge/error cases. Target minimum 80% coverage |
| **Integration** | DB / API | All external API calls or database connections must be mocked during unit tests |
| **E2E** | User Journey | Critical user flows to test |
| **Performance** | Latency / Load | Benchmark requirements |
| **Security** | Vuln / Auth | SAST/DAST or dependency audit |
| **Frontend** | UX / A11y | Accessibility checklist (WCAG), Performance Budget (Lighthouse score) |


## Technical Guardrails & Security Threat Model

### 1. Security & Privacy (Threat Model)
* **Top Threats**: Injection attacks, authentication bypass, data exposure
- [ ] **Data Handling**: Sanitize all user inputs to prevent Injection attacks. Never log raw PII
- [ ] **Secrets Management**: No hardcoded API keys. Use Env Vars/Secrets Manager
- [ ] **Authorization**: Validate user permissions before state changes

### 2. Performance & Resources
- [ ] **Execution Efficiency**: Consider time complexity for algorithms
- [ ] **Memory Management**: Use streams/pagination for large data
- [ ] **Resource Cleanup**: Close DB connections/file handlers in finally blocks

### 3. Architecture & Scalability
- [ ] **Design Pattern**: Follow SOLID principles, use Dependency Injection
- [ ] **Modularity**: Decouple logic from UI/Frameworks

### 4. Observability & Reliability
- [ ] **Logging Standards**: Structured JSON, include trace IDs `request_id`
- [ ] **Metrics**: Track `error_rate`, `latency`, `queue_depth`
- [ ] **Error Handling**: Standardized error codes, no bare except
- [ ] **Observability Artifacts**:
    - **Log Fields**: timestamp, level, message, request_id
    - **Metrics**: request_count, error_count, response_time
    - **Dashboards/Alerts**: High Error Rate > 5%


## Agent Directives & Error Recovery
*(ข้อกำหนดสำหรับ AI Agent ในการคิดและแก้ปัญหาเมื่อเกิดข้อผิดพลาด)*

- **Thinking Process**: Analyze root cause before fixing. Do not brute-force.
- **Fallback Strategy**: Stop after 3 failed test attempts. Output root cause and ask for human intervention/clarification.
- **Self-Review**: Check against Guardrails & Anti-patterns before finalizing.
- **Output Constraints**: Output ONLY the modified code block. Do not explain unless asked.


## Definition of Done (DoD) Checklist

- [ ] Tests passed + coverage met
- [ ] Lint/Typecheck passed
- [ ] Logging/Metrics/Trace implemented
- [ ] Security checks passed
- [ ] Documentation/Changelog updated
- [ ] Accessibility/Performance requirements met (if frontend)


## Anti-patterns / Pitfalls

* ⛔ **Don't**: Log PII, catch-all exception, N+1 queries
* ⚠️ **Watch out for**: Common symptoms and quick fixes
* 💡 **Instead**: Use proper error handling, pagination, and logging


## Reference Links & Examples

* Internal documentation and examples
* Official documentation and best practices
* Community resources and discussions


## Versioning & Changelog

* **Version**: 1.0.0
* **Changelog**:
  - 2026-02-22: Initial version with complete template structure

