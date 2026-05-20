---
id: SKL-edge-EDGEMODELCOMPRESSION
name: Edge Model Compression
description: Edge Model Compression enables deployment of large, accurate machine
  learning models on resource-constrained edge devices through techniques like quantization,
  pruning, knowledge distillation, and neu
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

# Edge Model Compression

## Skill Profile
*(Select at least one profile to enable specific modules)*
- [ ] **DevOps**
- [x] **Backend**
- [ ] **Frontend**
- [ ] **AI-RAG**
- [ ] **Security Critical**

## Overview
Edge Model Compression enables deployment of large, accurate machine learning models on resource-constrained edge devices through techniques like quantization, pruning, knowledge distillation, and neural architecture search. This capability is essential for bringing AI capabilities to edge devices with limited memory, compute, and power while maintaining acceptable accuracy.

## Why This Matters
- **Resource Constraints**: Deploy models on devices with <512KB RAM, <2MB Flash
- **Cost Reduction**: Reduce hardware requirements and power consumption by 50-80%
- **Latency Improvement**: Faster inference on edge devices (2-10x speedup)
- **Bandwidth Savings**: Smaller models for faster OTA updates (80-95% size reduction)
- **Scalability**: Deploy AI to millions of edge devices cost-effectively

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
  - Original trained model (PyTorch/TensorFlow)
  - Training data for calibration and fine-tuning
  - Test data for validation
  - Compression configuration (quantization type, sparsity, temperature)
  - Target device constraints (RAM, Flash, latency, power)
* **Entry Conditions**:
  - Original model trained and validated
  - Training and test data available
  - Target device constraints documented
  - Compression pipeline configured
  - Representative calibration data available
* **Outputs**:
  - Compressed model (quantized, pruned, distilled)
  - Compression metrics (size reduction, accuracy drop, speedup)
  - Exported model format (TFLite, ONNX, TorchScript)
  - Deployment package (model file, metadata, documentation)
* **Artifacts Required (Deliverables)**:
  - Compressed model file
  - Compression pipeline code
  - Metrics and validation report
  - Deployment documentation
  - Model metadata (compression parameters, accuracy, size)
* **Acceptance Evidence**:
  - Compression ratio > 10x
  - Accuracy retention > 95%
  - Latency reduction > 50%
  - Model size fits target device
  - Power consumption within budget
* **Success Criteria**:
  - Model size < target (e.g., < 1MB)
  - Accuracy > 95% of original model
  - Inference latency < target (e.g., < 100ms)
  - Power consumption < target (e.g., < 10mW)
  - Compression ratio > 10x

## Skill Composition
* **Depends on**: [tinyml-microcontroller-ai](../tinyml-microcontroller-ai/SKILL.md) (Edge inference), [edge-ai-development-workflow](../edge-ai-development-workflow/SKILL.md) (End-to-end pipeline)
* **Compatible with**: [on-device-model-training](../on-device-model-training/SKILL.md), [hybrid-inference-architecture](../hybrid-inference-architecture/SKILL.md)
* **Conflicts with**: None
* **Related Skills**: [model-optimization-quantization](../../78-inference-model-serving/model-optimization-quantization/SKILL.md), [high-performance-inference](../../78-inference-model-serving/high-performance-inference/SKILL.md)

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

