---
name: node-template-generator
description: 'Generate boilerplate code for new CasareRPA automation nodes. See templates/
  for category-specific templates and references/ for the complete checklist. Use
  when: creating new nodes, adding node categ'
---

---
name: node-template-generator
description: Generate boilerplate code for new CasareRPA automation nodes. See templates/ for category-specific templates and references/ for the complete checklist. Use when: creating new nodes, adding node categories, implementing BaseNode patterns, @properties decorator, node registration, get_parameter usage.
---

# Node Template Generator

Generate complete boilerplate for new CasareRPA nodes following modern standards.

## Quick Start

```python
# Node implementation
@properties(
    PropertyDef("url", PropertyType.STRING, required=True),
    PropertyDef("timeout", PropertyType.INTEGER, default=30000),
)
@node(category="browser")
class MyNode(BaseNode):
    async def execute(self, context):
        url = self.get_parameter("url")  # required
        timeout = self.get_parameter("timeout", 30000)  # optional
```

## Templates by Category

| Category | Template | Color |
|----------|----------|-------|
| Browser | `templates/browser.py` | RGB(65, 105, 225) |
| Desktop | `templates/desktop.py` | RGB(139, 69, 19) |
| Data | `templates/data.py` | RGB(70, 130, 180) |
| Control Flow | `templates/control_flow.py` | RGB(255, 140, 0) |
| File System | `templates/file.py` | RGB(46, 139, 87) |

## Registration Checklist

See `references/checklist.md` for the complete 8-step registration process.

## Quick Reference

- Use `get_parameter()` for optional properties
- Use `add_exec_input()/add_exec_output()` for flow ports
- Use `add_input_port(name, DataType.X)` for data ports
- Always register in `NODE_REGISTRY` and `NODE_TYPE_MAP`
