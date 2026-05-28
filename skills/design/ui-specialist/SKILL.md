---
name: ui-specialist
description: PySide6 UI development with dark theme, signals/slots, and NodeGraphQt integration
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: ui
---

## What I do

- Create PySide6 widgets and UI components
- Implement dark theme styling with THEME constants
- Design proper signal/slot connections
- Integrate with NodeGraphQt visual nodes

## When to use me

Use this when you need to:
- Create custom node widgets
- Design property editors
- Implement dialogs and panels
- Style UI with dark theme

## MCP-First Workflow

Always use MCP servers in this order:

1. **codebase** - Search for UI patterns
   ```python
   search_codebase("PySide6 widget dark theme signals slots", top_k=10)
   ```

2. **filesystem** - view_file existing UI code
   ```python
   read_file("src/casare_rpa/presentation/canvas/graph/node_widgets.py")
   ```

3. **git** - Check UI changes
   ```python
   git_diff("HEAD~5..HEAD", path="src/casare_rpa/presentation/canvas/")
   ```

4. **ref** - PySide6 documentation
   ```python
   search_documentation("widget", library="PySide6")
   ```

## Widget Template

```python
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit
from PySide6.QtCore import Signal, Slot

class CustomNodeWidget(QWidget):
    value_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)

        self.label = QLabel("Input:")
        self.input = QLineEdit()
        self.input.textChanged.connect(self._on_value_changed)

        layout.addWidget(self.label)
        layout.addWidget(self.input)

    @Slot(str)
    def _on_value_changed(self, value: str):
        self.value_changed.emit(value)

    def get_value(self) -> str:
        return self.input.text()

    def set_value(self, value: str):
        self.input.setText(value)
```

## Dark Theme (Use THEME Constants!)

```python
from casare_rpa.presentation.canvas.ui.theme import THEME

self.setStyleSheet(f"""
    QLineEdit {{
        background: {THEME.bg_darker};
        color: {THEME.text_primary};
        border: 1px solid {THEME.border};
        border-radius: 4px;
        padding: 4px;
    }}
    QLineEdit:focus {{
        border-color: {THEME.accent};
    }}
""")
```

## Signal/Slot Best Practices

| Pattern | Do | Don't |
|---------|-----|-------|
| Parameters | Use `@Slot(type)` decorator | Use bare `connect()` |
| Lambdas | Avoid (captures!) | `value_changed.connect(lambda v: ...)` |
| Threading | Use `Qt.QueuedConnection` | Direct calls cross-thread |
| Disconnecting | Store connection | Let it GC |

```python
# CORRECT
from functools import partial

def _setup_connections(self):
    self.input.textChanged.connect(partial(self._on_value_changed, self))

@Slot(str)
def _on_value_changed(self, value: str):
    pass
```
