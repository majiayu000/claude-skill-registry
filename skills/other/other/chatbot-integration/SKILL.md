---
id: SKL-chatbot-CHATBOTINTEGRATION
name: Chatbot Integration
description: AI-powered chatbots use language models to provide conversational interfaces
  for customer support, information retrieval, and task automation. They combine natural
  language understanding, context mana
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

# Chatbot Integration

## Skill Profile
*(Select at least one profile to enable specific modules)*
- [ ] **DevOps**
- [x] **Backend**
- [ ] **Frontend**
- [ ] **AI-RAG**
- [ ] **Security Critical**

## Overview
AI-powered chatbots use language models to provide conversational interfaces for customer support, information retrieval, and task automation. They combine natural language understanding, context management, and integration with business systems to deliver intelligent, personalized conversations.

## Why This Matters
- **Reduces Support Burden**: Automate common inquiries, reducing response time and support ticket volume
- **Increases Operational Efficiency**: 24/7 availability reduces downtime and ensures consistent customer service
- **Lowers Support Costs**: Automated workflows reduce need for large support teams
- **Improves Customer Experience**: Instant responses and natural conversations enhance user satisfaction
- **Enables Scalability**: Handle increasing customer volume without proportional team growth
- **Provides Data Insights**: Conversation data helps identify pain points and improvement opportunities

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
  - User messages (text, voice transcripts)
  - User context (session ID, user profile, conversation history)
  - Business data (product info, support tickets, user accounts)
* **Entry Conditions**:
  - LLM API configured with valid credentials
  - Chatbot intents and entities defined
  - Business system APIs accessible
  - Database for conversation storage initialized
* **Outputs**:
  - Chatbot responses (text, rich messages)
  - Conversation state updates
  - Escalation requests to human agents
  - Analytics events
* **Artifacts Required (Deliverables)**:
  - Chatbot implementation code
  - Intent classification model
  - Conversation memory system
  - Tool integration layer
  - Analytics tracking
* **Acceptance Evidence**:
  - Test conversation logs
  - Intent classification accuracy metrics
  - Response time benchmarks
  - User satisfaction scores
* **Success Criteria**:
  - Intent classification accuracy > 85%
  - Average response time < 2 seconds
  - User satisfaction score > 4.0/5.0
  - Human handoff rate < 10%

## Skill Composition
* **Depends on**: [llm-integration](../06-ai-ml-production/llm-integration/SKILL.md), [ai-agents](./ai-agents/SKILL.md), [ai-search](./ai-search/SKILL.md)
* **Compatible with**: [conversational-ui](./conversational-ui/SKILL.md), [line-platform-integration](./line-platform-integration/SKILL.md), [customer-support](../29-customer-support/)
* **Conflicts with**: Static FAQ pages (limited functionality)
* **Related Skills**: [llm-function-calling](../06-ai-ml-production/llm-function-calling/SKILL.md), [langchain-patterns](../06-ai-ml-production/langchain-patterns/SKILL.md), [agent-patterns](../06-ai-ml-production/agent-patterns/SKILL.md)

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

