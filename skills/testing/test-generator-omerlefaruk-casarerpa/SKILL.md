---
name: test-generator
description: Generate comprehensive pytest test suites for CasareRPA components, including nodes, controllers, use cases, and domain entities. Use when: creating new tests, testing nodes, controller tests, use case tests, domain entity tests, test coverage needed, pytest test generation.
---

# Test Generator

Generate pytest test suites following CasareRPA testing patterns.

## Quick Start

For node tests:
```python
# tests/nodes/{category}/test_{node_name}.py
@pytest.fixture
def node():
    return {NodeName}Node()

@pytest.mark.asyncio
async def test_execute_success(node, mock_context):
    result = await node.execute(mock_context)
    assert result.success is True
```

## Test Types

| Component | Reference | Location |
|-----------|-----------|----------|
| Nodes | `references/node-tests.md` | Detailed node testing patterns |
| Controllers | `references/controller-tests.md` | UI controller testing |
| Use Cases | `references/use-case-tests.md` | Application layer tests |
| Domain Entities | `references/domain-tests.md` | Pure logic tests |

## Coverage Checklist

- [ ] Initialization tests
- [ ] Happy path (success cases)
- [ ] Sad path (error cases)
- [ ] Edge cases (boundary conditions)
- [ ] External resource mocking
- [ ] Logging verification

## Running Tests

```bash
pytest tests/ -v                    # All tests
pytest tests/nodes/browser/ -v      # Category only
pytest tests/ --cov=casare_rpa      # With coverage
```

## Examples

See `examples/` for complete test file examples.
