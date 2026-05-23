---
name: node-creator
description: Create or update CasareRPA nodes using schema-driven patterns and registry updates. Use when: adding new nodes, modifying node properties or ports, registering visual nodes, writing node tests.
---

# Node Creator

Build nodes with the modern schema-driven pattern and keep registry/visual nodes in sync.

## Start Here

- `docs/agent/nodes.md`
- `docs/agent/node-templates.md`
- `docs/agent/node-registration.md`
- `.brain/docs/node-checklist.md`
- `.brain/docs/node-templates-core.md`
- `.brain/docs/node-templates-data.md`

## Core Rules (Non-Negotiable)

- Always use `@properties(...)` (even empty).
- Use `get_parameter()` for optional properties (never `self.config.get()`).
- Data ports use `add_input_port(name, DataType.X)` and `add_output_port(...)`.
- Exec ports use `add_exec_input()` and `add_exec_output()`.
- Register in `src/casare_rpa/nodes/registry_data.py` (NODE_REGISTRY + NODE_TYPE_MAP).

## Minimal Template

```python
from casare_rpa.domain.decorators import node, properties
from casare_rpa.domain.entities.base_node import BaseNode
from casare_rpa.domain.schemas import PropertyDef, PropertyType
from casare_rpa.domain.value_objects.types import DataType

@properties(
    PropertyDef("timeout", PropertyType.INTEGER, default=30000),
)
@node(category="browser")
class ExampleNode(BaseNode):
    def _define_ports(self):
        self.add_exec_input("exec_in")
        self.add_exec_output("exec_out")
        self.add_input_port("url", DataType.STRING)
        self.add_output_port("result", DataType.STRING)

    async def execute(self, context):
        timeout = self.get_parameter("timeout", 30000)
        url = self.get_input_value("url")
        # ... logic ...
        self.set_output_value("result", "ok")
        return {"success": True, "next_nodes": ["exec_out"]}
```

## Typical File Touches

- Node implementation: `src/casare_rpa/nodes/...`
- Visual node: `src/casare_rpa/presentation/canvas/visual_nodes/...`
- Registry: `src/casare_rpa/nodes/registry_data.py`
- Exports: category `__init__.py`
- Tests: `tests/domain/` or `tests/nodes/`

## Validation

- Run: `python scripts/audit_node_modernization.py` (if auditing non-@properties nodes).
