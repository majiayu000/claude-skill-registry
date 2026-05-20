---
name: pulse-mantine
description: Python bindings for Mantine React components. Wraps all @mantine/core components plus forms, dates, and charts packages. Use when building UI with Pulse Mantine components, adapting Mantine docs to Python, or working with MantineForm validation.
---

# Pulse Mantine

Python bindings for [Mantine](https://mantine.dev/) React library. All components from `@mantine/core`, `@mantine/form`, `@mantine/dates`, and `@mantine/charts` are wrapped.

## Quick Reference

```python
from pulse_mantine import MantineProvider, Button, TextInput, Stack, Select
```

## Adapting Mantine Docs to Pulse

Mantine docs use JSX. Convert to Pulse Python:

| JSX | Pulse Python |
|-----|--------------|
| `<Button variant="outline">Click</Button>` | `Button("Click", variant="outline")` |
| `<Stack gap="md"><Item /></Stack>` | `Stack(gap="md")[Item()]` |
| `onClick={() => fn()}` | `onClick=fn` or `onClick=lambda: fn()` |
| `<Tabs.Tab value="x">` | `TabsTab("label", value="x")` |

**Key rules:**
- Children as first args: `Button("text")`, `Title("heading")`
- Props use camelCase: `withAsterisk`, `onClick`, `defaultValue`
- Bracket syntax for nesting: `Stack()[child1, child2]`
- Compound components flatten: `Tabs.Tab` → `TabsTab`, `Modal.Body` → `ModalBody`

## Packages

### Core (`@mantine/core`)
100+ UI components. All props from Mantine docs work directly.

**Layout:** Stack, Group, Grid, GridCol, Flex, Container, Center, AppShell
**Inputs:** TextInput, Select, Checkbox, Switch, Slider, NumberInput, Textarea, PasswordInput, FileInput, ColorInput
**Buttons:** Button, ActionIcon, CloseButton, CopyButton, FileButton
**Overlays:** Modal, Drawer, Menu, Popover, Tooltip, HoverCard, Dialog
**Feedback:** Alert, Notification, Progress, Loader, Skeleton
**Data Display:** Card, Table, Accordion, Badge, Avatar, Timeline, Spoiler
**Navigation:** Tabs, NavLink, Breadcrumbs, Pagination, Stepper
**Typography:** Text, Title, Code, Highlight, List, Blockquote

### Forms (`@mantine/form`)
Form state + client/server validation. See `references/forms.md`.

```python
form = MantineForm(
    initialValues={"email": ""},
    validate={"email": IsEmail("Invalid email")},
)
return form.render(onSubmit=handle)[TextInput(name="email")]
```

### Dates (`@mantine/dates`)
Date/time pickers. See `references/dates.md`.

```python
DatePickerInput(name="date", label="Pick date")
DateTimePicker(name="datetime", label="Pick datetime")
TimeInput(name="time", label="Pick time")
```

### Charts (`@mantine/charts`)
Recharts wrappers. See `references/charts.md`.

```python
LineChart(h=300, data=data, dataKey="date", series=[{"name": "value", "color": "blue"}])
```

## Common Patterns

**Wrap app with provider:**
```python
@ps.component
def App():
    return MantineProvider()[YourContent()]
```

**Form with validation:**
```python
form = MantineForm(
    initialValues={"name": "", "email": ""},
    validate={
        "name": IsNotEmpty("Required"),
        "email": [IsNotEmpty("Required"), IsEmail("Invalid")],
    },
    validateInputOnBlur=True,
)
```

**Modal/Drawer state:**
```python
with ps.init():
    opened = ps.use_state(False)

Modal(opened=opened.value, onClose=lambda: opened.set(False))[content]
```

**Notifications:**
```python
from pulse_mantine import Notifications, notifications
# Add <Notifications /> to layout
notifications.show(title="Success", message="Done", color="green")
```

## Reference Files

For detailed API docs:
- `references/core.md` - All core components by category
- `references/forms.md` - MantineForm, validators, form actions
- `references/dates.md` - Date/time picker components
- `references/charts.md` - Chart components and data format
