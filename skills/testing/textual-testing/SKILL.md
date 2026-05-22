---
name: textual-testing
description: |
  Test Textual TUI applications using the built-in testing framework. Covers headless mode
  testing with App.run_test(), complete Pilot API (mouse, keyboard, timing, animations),
  widget querying, and worker management. Use when: writing tests for TUI widgets, testing
  user interactions (clicks, keypresses, hover), verifying widget state, testing event
  handling, or running integration tests. Primary skill for functional Textual testing.
---

# Textual Testing

Functional testing for Textual applications using `App.run_test()` and the `Pilot` class.

## Quick Start

```python
async def test_my_app():
    """Test a Textual application."""
    app = MyApp()
    async with app.run_test() as pilot:
        # Interact with app
        await pilot.press("enter")
        await pilot.pause()

        # Assert on state
        widget = pilot.app.query_one("#status")
        assert widget.renderable == "Done"
```

## pytest Configuration

```toml
# pyproject.toml
[tool.pytest.ini_options]
asyncio_mode = "auto"  # No @pytest.mark.asyncio needed
testpaths = ["tests"]
```

## App.run_test() Method

Run app in headless mode (no terminal output, all other behavior identical):

```python
async with app.run_test(size=(80, 24)) as pilot:
    # size: terminal dimensions (width, height), default (80, 24)
    ...
```

## Complete Pilot API

### Properties

```python
pilot.app  # Access the App instance being tested
```

### Mouse Operations

```python
# Click widget by selector, type, or instance
await pilot.click("#button")          # CSS selector
await pilot.click(Button)             # Widget type
await pilot.click(my_widget)          # Widget instance
await pilot.click(offset=(40, 12))    # Absolute coordinates

# Click with modifiers
await pilot.click("#item", shift=True)
await pilot.click("#item", control=True)
await pilot.click("#item", meta=True)

# Multiple clicks
await pilot.click("#item", times=2)   # Double-click
await pilot.click("#item", times=3)   # Triple-click
await pilot.double_click("#item")     # Alias
await pilot.triple_click("#item")     # Alias

# Click with offset from selector
await pilot.click("#widget", offset=(10, 5))

# Hover (for testing hover states, tooltips)
await pilot.hover("#menu-item")

# Raw mouse events (for drag-and-drop)
await pilot.mouse_down("#draggable")
await pilot.hover("#drop-target")
await pilot.mouse_up("#drop-target")
```

### Keyboard Operations

```python
# Press single key
await pilot.press("enter")

# Press multiple keys in sequence
await pilot.press("h", "e", "l", "l", "o")

# Type string (unpack into characters)
await pilot.press(*"hello world")

# Special keys
await pilot.press("tab", "enter", "escape", "backspace", "delete")
await pilot.press("up", "down", "left", "right")
await pilot.press("home", "end", "pageup", "pagedown")
await pilot.press("f1", "f2", "f12")

# Modifier combinations
await pilot.press("ctrl+c", "ctrl+s", "ctrl+shift+p")
await pilot.press("shift+tab", "alt+f4", "meta+s")
```

### Timing Control

```python
# Wait for message queue to drain
await pilot.pause()

# Wait for messages + additional delay
await pilot.pause(0.5)  # 0.5 seconds extra
```

### Animation Handling

```python
# Wait for current animations to complete
await pilot.wait_for_animation()

# Wait for all current AND scheduled animations
await pilot.wait_for_scheduled_animations()
```

### App Control

```python
# Exit app with return value
await pilot.exit(result={"status": "success"})

# Resize terminal during test
await pilot.resize_terminal(120, 40)
await pilot.pause()  # Let resize events propagate
```

### Worker Management

```python
# Wait for all background workers to complete
await pilot.app.workers.wait_for_complete()
```

## Widget Querying

```python
# Query single widget (raises if not found or multiple matches)
button = pilot.app.query_one("#submit")
button = pilot.app.query_one(Button)
button = pilot.app.query_one("#submit", Button)  # With type validation

# Query multiple widgets
buttons = pilot.app.query(Button)
buttons = pilot.app.query(".action-button")

# Query methods
first = pilot.app.query(Button).first()
last = pilot.app.query(Button).last()

# Iterate
for button in pilot.app.query(".action-button"):
    assert not button.disabled
```

## Common Test Patterns

### Test Button Click

```python
async def test_button_click():
    class MyApp(App):
        clicked = False

        def compose(self):
            yield Button("Click", id="btn")

        def on_button_pressed(self):
            self.clicked = True

    async with MyApp().run_test() as pilot:
        await pilot.click("#btn")
        await pilot.pause()
        assert pilot.app.clicked is True
```

### Test Text Input

```python
async def test_text_input():
    class MyApp(App):
        def compose(self):
            yield Input(id="input")

    async with MyApp().run_test() as pilot:
        await pilot.click("#input")
        await pilot.press(*"hello world")
        await pilot.pause()

        input_widget = pilot.app.query_one("#input", Input)
        assert input_widget.value == "hello world"
```

### Test Keyboard Binding

```python
async def test_keyboard_binding():
    class MyApp(App):
        BINDINGS = [("ctrl+s", "save", "Save")]
        saved = False

        def action_save(self):
            self.saved = True

    async with MyApp().run_test() as pilot:
        await pilot.press("ctrl+s")
        await pilot.pause()
        assert pilot.app.saved is True
```

### Test Background Worker

```python
async def test_background_worker():
    class MyApp(App):
        data = None

        @work
        async def fetch_data(self):
            await asyncio.sleep(0.1)
            self.data = {"loaded": True}

    async with MyApp().run_test() as pilot:
        pilot.app.fetch_data()
        await pilot.app.workers.wait_for_complete()
        assert pilot.app.data == {"loaded": True}
```

### Test Different Terminal Sizes

```python
async def test_responsive_layout():
    app = MyApp()

    # Test small terminal
    async with app.run_test(size=(40, 20)) as pilot:
        sidebar = pilot.app.query_one("#sidebar")
        assert not sidebar.is_visible  # Hidden on small screens

    # Test large terminal
    async with app.run_test(size=(120, 40)) as pilot:
        sidebar = pilot.app.query_one("#sidebar")
        assert sidebar.is_visible  # Visible on large screens
```

### Test with Terminal Resize

```python
async def test_resize_handling():
    async with MyApp().run_test(size=(80, 24)) as pilot:
        assert pilot.app.size == (80, 24)

        await pilot.resize_terminal(120, 40)
        await pilot.pause()

        assert pilot.app.size == (120, 40)
```

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Assertion fails before update | Add `await pilot.pause()` after interactions |
| Worker result not available | Use `await pilot.app.workers.wait_for_complete()` |
| Animation state varies | Use `await pilot.wait_for_animation()` |
| Missing `async def` | All test functions must be `async def` |
| Missing `await` | All pilot methods are async and need `await` |

## See Also

- [textual-snapshot-testing](../textual-snapshot-testing) - Visual regression testing
- [textual-test-fixtures](../textual-test-fixtures) - Pytest fixture patterns
- [textual-test-patterns](../textual-test-patterns) - Testing recipes by scenario
