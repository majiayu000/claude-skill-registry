---
name: chain-tester
description: Node chain testing templates for quality agent. WorkflowBuilder patterns and tier-based testing. Use when: testing node chains, WorkflowBuilder patterns, tier-based testing, chain execution tests, simple/complex/full chain tiers.
---

# Chain Tester

Templates for testing node chains with real nodes.

## Testing Tiers

| Tier | Nodes | Complexity | Marker |
|------|-------|------------|--------|
| Simple | 2-3 | Linear | (none) |
| Complex | 5-10 | Branching | (none) |
| Full | 10+ | Multi-branch | `@pytest.mark.slow` |

## WorkflowBuilder API

```python
from tests.nodes.chain.conftest import WorkflowBuilder

chain = WorkflowBuilder() \
    .add(StartNode(), id="start") \
    .add(SomeNode(param="value"), id="action") \
    .add(EndNode(), id="end") \
    .connect_sequential() \
    .build()
```

## Simple Chain Template

```python
@pytest.mark.asyncio
async def test_basic_linear_chain(chain_executor):
    chain = WorkflowBuilder() \
        .add(StartNode(), id="start") \
        .add(SetVariableNode(name="x", value=42), id="set") \
        .add(EndNode(), id="end") \
        .connect_sequential() \
        .build()

    result = await chain_executor.execute(chain)

    assert result.status == ExecutionStatus.COMPLETED
    assert result.context.variables["x"] == 42
```

## Assertion Patterns

```python
# Status assertions
assert result.success is True

# Variable assertions
assert result.final_variables["output"] == expected_value

# Execution assertions
assert "node_id" in result.nodes_executed

# Error assertions
assert len(result.errors) > 0
```
