---
id: SKL-llm-LLMFUNCTIONCALLING
name: Llm Function Calling
description: LLM function calling (also known as tool use) enables Large Language
  Models to interact with external systems by calling predefined functions. Instead
  of just generating text, LLM can request to execu
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

# Llm Function Calling

## Skill Profile
*(Select at least one profile to enable specific modules)*
- [ ] **DevOps**
- [x] **Backend**
- [ ] **Frontend**
- [ ] **AI-RAG**
- [ ] **Security Critical**

## Overview
LLM function calling (also known as tool use) enables Large Language Models to interact with external systems by calling predefined functions. Instead of just generating text, LLM can request to execute specific functions with structured parameters, receive results, and continue reasoning based on those results. This skill covers OpenAI and Anthropic function calling APIs, function definition schemas, structured output extraction, multi-function calls, streaming with function calls, error handling, validation, security considerations, rate limiting, caching, parallel execution, function routing, dynamic function loading, and production monitoring.

## Why This Matters
Function calling is critical for production AI applications because:
- **Structured Output**: Enables reliable data extraction from unstructured LLM responses
- **External Integration**: LLMs can safely interact with databases, APIs, and services
- **Validation**: Schema validation ensures data integrity and type safety
- **Orchestration**: LLMs can coordinate complex multi-step workflows
- **Security**: Controlled function execution prevents unauthorized access
- **Observability**: Function calls are logged and monitored for debugging

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
#

## Skill Composition
* **Depends on**: None
* **Compatible with**: None
* **Conflicts with**: None
* **Related Skills**: None

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


## Assumptions
- LLM supports function calling (GPT-4, Claude 3 Opus+)
- Functions are idempotent or handle retries appropriately
- Network connectivity for external services
- Sufficient memory for concurrent function execution

## Compatibility
- Python 3.8+
- OpenAI API 1.0+ (for function calling)
- Anthropic API 1.0+ (for tool use)
- Pydantic 2.0+ (for validation)
- Asyncio 3.7+ (for parallel execution)

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


## Anti-patterns
1. **No Validation**: Not validating function parameters
2. **No Error Handling**: Functions can fail - handle gracefully
3. **Hardcoded Schemas**: Not using proper schema definitions
4. **No Caching**: Re-executing same functions wastes resources
5. **No Rate Limiting**: Exceeding API limits
6. **Ignoring Context**: Not using previous function results
7. **No Streaming**: Not streaming long responses
8. **Insecure Code Execution**: Allowing arbitrary code execution

## Reference Links & Examples

* Internal documentation and examples
* Official documentation and best practices
* Community resources and discussions


## Versioning & Changelog

* **Version**: 1.0.0
* **Changelog**:
  - 2026-02-22: Initial version with complete template structure

