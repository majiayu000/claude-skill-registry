---
name: cobuilder:tdd-pipeline
description: This skill should be used when System 3 or Guardian needs to "generate a TDD pipeline", "create a worker pipeline", "instantiate the tdd-validated template", "set up TDD execution pipeline", or when creating DOT pipeline files for test-driven worker execution. Documents the tdd-validated template and worker powers configuration.
version: 1.0.0
title: "TDD Pipeline Template"
status: active
type: skill
last_verified: 2026-03-21
grade: authoritative
---

# TDD Pipeline Template

The `tdd-validated` template generates DOT pipeline files with explicit RED → GREEN → REFACTOR nodes per worker. Each worker receives superpowers for TDD, debugging, and verification.

---

## Template Location

`.cobuilder/templates/tdd-validated/`

---

## Instantiation

```bash
python3 cobuilder/templates/instantiator.py tdd-validated \
  --param prd_ref=PRD-AUTH-001 \
  --param sd_path=docs/sds/SD-AUTH-001.md \
  --param-file workers.yaml \
  --output .pipelines/pipelines/auth-tdd.dot
```

### Workers YAML Format

```yaml
workers:
  - label: "User Login"
    worker_type: backend-solutions-engineer
    bead_id: AUTH-LOGIN
    acceptance: "Login endpoint returns JWT token for valid credentials"
    scope: "src/auth/login.py,tests/test_login.py"
    test_command: "pytest tests/test_login.py -v"
  - label: "Login Form"
    worker_type: frontend-dev-expert
    bead_id: AUTH-FORM
    acceptance: "Login form submits credentials and stores JWT"
    scope: "src/components/LoginForm.tsx,tests/LoginForm.test.tsx"
    test_command: "npm test -- --testPathPattern=LoginForm"
```

---

## Pipeline Structure Per Worker

Each worker gets three codergen nodes in sequence:

```
RED (write failing tests) → GREEN (minimal implementation) → REFACTOR (clean up)
    → Validation Gate → Decision (pass → next | fail → retry from RED)
```

Color coding: RED nodes = `#ffcccc`, GREEN nodes = `#ccffcc`, REFACTOR nodes = `#ccccff`

---

## Worker Powers Configuration

All codergen nodes in the TDD template receive `worker_powers` attribute:

| Power Key | Sub-Skills Available | Default |
|-----------|---------------------|---------|
| `tdd` | `cobuilder:tdd`, `cobuilder:verification-before-completion` | Yes |
| `systematic-debugging` | `cobuilder:systematic-debugging` | Yes |
| `verification` | `cobuilder:verification-before-completion` | Yes |
| `brainstorming` | `cobuilder:brainstorming` | No |
| `all` | All cobuilder sub-skills | No |

Default: `tdd,systematic-debugging,verification`

Override per-worker:
```yaml
workers:
  - label: "Complex UI"
    worker_powers: "all"  # Full power mode for complex tasks
```

---

## Template Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `prd_ref` | Yes | — | PRD identifier |
| `sd_path` | Yes | — | Path to Solution Design |
| `workers` | Yes | — | List of worker definitions |
| `include_research` | No | `false` | Prepend research node |
| `include_e2e` | No | `true` | Append E2E integration test node |
| `default_worker_powers` | No | `tdd,systematic-debugging,verification` | Power set for all workers |
| `llm_profile_test` | No | `anthropic-fast` | LLM for RED phase (test writing) |
| `llm_profile_impl` | No | `anthropic-smart` | LLM for GREEN phase (implementation) |
| `llm_profile_refactor` | No | `anthropic-fast` | LLM for REFACTOR phase |

---

## Validation

After generating a pipeline, validate it:

```bash
python3 cobuilder/engine/cli.py validate .pipelines/pipelines/auth-tdd.dot
```

Then launch:

```bash
python3 cobuilder/engine/pipeline_runner.py --dot-file .pipelines/pipelines/auth-tdd.dot
```
