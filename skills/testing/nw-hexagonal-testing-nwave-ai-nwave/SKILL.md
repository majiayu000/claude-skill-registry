---
name: nw-hexagonal-testing
description: 5-layer agent output validation, I/O contract specification, vertical slice development, and test doubles policy with per-layer examples
user-invocable: false
disable-model-invocation: true
---

# Hexagonal Testing and Output Validation

## 5-Layer Output Validation Framework

Validates agent OUTPUTS, not TDD testing methodology.

### Layer 1: Unit Testing (Output Validation)

Validate individual software-crafter outputs.

```yaml
structural_checks:
  - required_elements_present: true
  - format_compliance: true
  - quality_standards_met: true

quality_checks:
  - completeness: "All required components present"
  - clarity: "Unambiguous and understandable"
  - testability: "Can be validated"

test_data_quality:
  real_data: "Use real API responses as golden masters"
  edge_cases: "Test null, empty, malformed, boundary conditions"
  assertions: "Assert expected counts, not just 'any results'"
```

### Layer 2: Integration Testing (Handoff Validation)

Validate handoffs to next agent. Next agent must consume outputs without clarification.
- Deliverables complete: all expected artifacts present
- Validation status clear: quality gates passed/failed explicit
- Context sufficient: next agent can proceed without re-elicitation

### Layer 3: Adversarial Output Validation

Challenge output quality through adversarial scrutiny of generated code:
- SQL injection vulnerabilities? | XSS vulnerabilities? | Null/undefined/empty input handling?
- Integer overflow/underflow? | Graceful failure vs crash? | Exception handling appropriateness?

Pass criteria: all critical challenges addressed, edge cases documented and handled.

For peer review and escalation protocols, load the review-dimensions skill.

## Input/Output Contract

### Inputs
- **Required**: user_request (non-empty command string) | context_files (existing readable file paths)
- **Optional**: configuration (YAML/JSON) | previous_artifacts (outputs from prior wave for handoff)

### Outputs
- **Primary**: code artifacts (src/**/*, strictly necessary only) | documentation (docs/develop/, minimal essential)
- **Secondary**: validation_results (gate pass/fail status) | handoff_package (deliverables, next_agent, validation_status)
- **Policy**: any document beyond code/test files requires explicit user approval before creation

### Side Effects
- **Allowed**: file creation (src/**, tests/** only) | file modification with audit trail | log entries
- **Forbidden**: unsolicited documentation | deletion without approval | external API calls | credential access
- **Requires permission**: documentation beyond code/test files | summary reports | analysis documents

### Error Handling
- Invalid input: validate first, clear error, do not proceed with partial inputs
- Processing error: log context, return to safe state, actionable user message
- Validation failure: report failed gates, withhold artifacts, suggest remediation

## Vertical Slice Development

Complete business capability per slice: UI -> Application -> Domain -> Infrastructure for a specific feature. Slices developed and deployed independently. Focus on business capability over technical layer.

For test doubles policy and violation examples, load the tdd-methodology skill.

## Testing Boundaries per Architectural Layer

| Layer | Test Strategy | Adapter Selection | Rationale |
|-------|--------------|------------------|-----------|
| Domain | Pure unit test, zero I/O | N/A (no adapters) | Domain is pure functions — test with pure inputs |
| Application | InMemory ports for focused scenarios | InMemory doubles | Application orchestrates — test logic, not I/O |
| Adapter | REAL I/O ALWAYS* | Real system (tmp_path, subprocess, DB) | Adapter IS the I/O boundary — testing with InMemory defeats the purpose |

*Exception: costly subprocesses (claude -p, LLM) and paid external APIs use contract smoke tests tagged `@requires_external` instead of real I/O. See nw-tdd-methodology Mandate 6 for the full adapter type → test type table.
| WS/E2E | Per declared strategy (A/B/C/D) | Real for local, fake for costly | WS proves wiring — InMemory proves nothing about wiring |

### Key Insight

A pure function stub at a driven port boundary models the port's CONTRACT, not the external system's BEHAVIOR. For every driven port stub, verify that an adapter integration test with real I/O covers the behavioral gap.

### Integration Surface Ratio Heuristic

If the system's primary job is coordinating external processes (orchestrators, ETL, deployment scripts), invest MORE in WS and adapter integration tests than unit tests. If the system's primary job is domain computation (pricing, validation, parsing), the traditional pyramid applies.

### Strategy D Fixture Template

```python
# conftest.py
import os
import pytest

@pytest.fixture
def subprocess_runner():
    """Returns real or fake subprocess runner based on E2E mode."""
    if os.getenv("NWAVE_E2E_REAL_SUBPROCESS") == "1":
        from myapp.adapters.real_subprocess_runner import RealSubprocessRunner
        return RealSubprocessRunner()
    from tests.doubles.fake_subprocess_runner import FakeSubprocessRunner
    return FakeSubprocessRunner(exit_code=0, stdout="OK")
```

Naming convention for multi-port Strategy D: `NWAVE_E2E_REAL_{PORT_NAME}` per driven port (e.g., `NWAVE_E2E_REAL_SUBPROCESS`, `NWAVE_E2E_REAL_DATABASE`). Use `NWAVE_E2E_MODE=real` as composite flag to enable ALL real adapters at once for full E2E.
