---
name: test
description: Test writing, reviewing, and running for Kagenti - smart router for test workflows
---

```mermaid
flowchart TD
    START([Need Tests]) --> TEST{"/test"}
    TEST -->|Write new tests| WRITE["test:write"]:::test
    TEST -->|Review quality| REVIEW["test:review"]:::test
    TEST -->|Run on Kind| RUNKIND["test:run-kind"]:::test
    TEST -->|Run on HyperShift| RUNHS["test:run-hypershift"]:::test
    TEST -->|Playwright| PW["test:playwright"]:::test
    TEST -->|Full TDD loop| TDD["tdd/*"]:::tdd

    WRITE --> REVIEW
    REVIEW -->|Issues found| WRITE
    REVIEW -->|Clean| RUN{Run where?}
    RUN -->|Kind| RUNKIND
    RUN -->|HyperShift| RUNHS

    classDef tdd fill:#4CAF50,stroke:#333,color:white
    classDef test fill:#9C27B0,stroke:#333,color:white
```

> Follow this diagram as the workflow.

# Test Skills

Test management for Kagenti: write, review, and run tests.

## Auto-Select Sub-Skill

```
What do you need?
    │
    ├─ Write pytest E2E/unit tests
    │   → test:write
    │
    ├─ Write Playwright demo tests
    │   → test:playwright
    │
    ├─ Review existing tests for quality
    │   → test:review
    │
    ├─ Run tests on Kind cluster
    │   → test:run-kind
    │
    ├─ Run tests on HyperShift cluster
    │   → test:run-hypershift
    │
    └─ Full TDD loop (write + run + iterate)
        → tdd (which links back here for test quality)
```

## Available Skills

| Skill | Purpose | Framework |
|-------|---------|-----------|
| `test:write` | Write pytest E2E/unit tests | pytest |
| `test:playwright` | Write Playwright demo tests (markStep, assertions, narration) | Playwright |
| `test:review` | Review test quality, catch bad patterns | Any |
| `test:run-kind` | Run tests on Kind cluster | pytest |
| `test:run-hypershift` | Run tests on HyperShift cluster | pytest |

## Test Workflow in TDD

```
tdd:* → Write/fix code → test:write (if new tests needed)
                        → test:review (verify test quality)
                        → test:run-kind or test:run-hypershift
                        → Pass? → git:commit → git:rebase → Push
```

## Related Skills

- `tdd:ci` - CI-driven TDD loop
- `tdd:kind` - TDD on Kind
- `tdd:hypershift` - TDD on HyperShift
- `git:commit` - Commit after tests pass
