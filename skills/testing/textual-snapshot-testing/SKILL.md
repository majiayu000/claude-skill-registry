---
name: textual-snapshot-testing
description: |
  Visual regression testing for Textual TUI applications using pytest-textual-snapshot.
  Captures SVG screenshots and compares across test runs to detect visual regressions.
  Use when: testing visual appearance, detecting layout regressions, testing responsive
  designs across terminal sizes, verifying CSS styling effects, or setting up CI/CD
  for visual testing. Covers snap_compare fixture, run_before callbacks, snapshot
  management, flaky test handling (animations, cursors, timestamps), and CI integration.

---

# Textual Snapshot Testing

Visual regression testing using pytest-textual-snapshot to capture and compare SVG screenshots.

## Quick Reference

```python
# Basic snapshot test
def test_app_visual(snap_compare):
    assert snap_compare(MyApp())

# With user interaction
def test_after_input(snap_compare):
    assert snap_compare(MyApp(), press=["tab", "enter"])

# With custom terminal size
def test_responsive(snap_compare):
    assert snap_compare(MyApp(), terminal_size=(120, 40))

# With pre-snapshot setup
def test_stable(snap_compare):
    async def run_before(pilot):
        pilot.app.query_one(Input).cursor_blink = False
    assert snap_compare(MyApp(), run_before=run_before)
```

## Setup

```bash
pip install pytest-textual-snapshot
```

The `snap_compare` fixture is automatically available after installation.

## snap_compare API

```python
def snap_compare(
    app: App | str | Path,           # App instance or path to app file
    *,
    press: list[str] | None = None,  # Keys to press before snapshot
    terminal_size: tuple[int, int] = (80, 24),  # Terminal dimensions
    run_before: Callable[[Pilot], Awaitable[None]] | None = None,  # Async setup
) -> bool
```

## Workflow

1. **First run**: Snapshot generated, test fails (by design)
2. **Review**: Check HTML report, validate visual output
3. **Approve**: Run `pytest --snapshot-update` to save baseline
4. **Subsequent runs**: Compare against baseline, fail on differences
5. **Regression**: Visual diff shown in HTML report

## Key Patterns

### Disable Animations (Prevents Flaky Tests)

```python
def test_stable_snapshot(snap_compare):
    async def run_before(pilot):
        for widget in pilot.app.query("*"):
            widget.can_animate = False
    assert snap_compare(MyApp(), run_before=run_before)
```

### Disable Cursor Blink

```python
def test_input_snapshot(snap_compare):
    async def run_before(pilot):
        pilot.app.query_one(Input).cursor_blink = False
    assert snap_compare(MyApp(), run_before=run_before)
```

### Wait for Workers Before Snapshot

```python
def test_data_loaded(snap_compare):
    async def run_before(pilot):
        await pilot.press("r")  # Trigger load
        await pilot.app.workers.wait_for_complete()
    assert snap_compare(DataApp(), run_before=run_before)
```

### Mock Time (Stable Timestamps)

```python
from unittest.mock import patch
from datetime import datetime

def test_timestamp(snap_compare):
    with patch("myapp.datetime") as mock_dt:
        mock_dt.now.return_value = datetime(2025, 1, 1, 12, 0, 0)
        assert snap_compare(TimestampApp())
```

### Complex Interaction Sequence

```python
def test_command_palette(snap_compare):
    async def run_before(pilot):
        await pilot.press("ctrl+p")
        await pilot.pause()
        await pilot.press(*"search term")
        await pilot.pause()
        pilot.app.query_one(Input).cursor_blink = False
    assert snap_compare(MyApp(), run_before=run_before)
```

## Snapshot Management

### Update Snapshots

```bash
# Update all snapshots
pytest --snapshot-update

# Update specific test
pytest tests/test_app.py::test_specific --snapshot-update
```

### Snapshot Storage

```
tests/
├── test_app.py
└── __snapshots__/
    └── test_app/
        └── test_my_feature.svg
```

**Important**: Commit `__snapshots__/` to version control.

### View Failure Reports

When tests fail, pytest generates HTML report with visual diff:
- **Left**: Current rendering
- **Right**: Historical baseline
- **Toggle**: Overlay mode for subtle differences

## CI/CD Integration

### GitHub Actions

```yaml
- name: Run snapshot tests
  run: pytest tests/snapshot -v

- name: Upload report on failure
  if: failure()
  uses: actions/upload-artifact@v4
  with:
    name: snapshot-report
    path: snapshot_report.html
```

### Manual Snapshot Update Workflow

```yaml
# .github/workflows/update-snapshots.yml
name: Update Snapshots
on: workflow_dispatch

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pytest tests/snapshot --snapshot-update
      - run: |
          git add tests/__snapshots__/
          git commit -m "Update snapshot baselines"
          git push
```

## Editor Integration

Open failed snapshots in your editor:

```bash
# VS Code
export TEXTUAL_SNAPSHOT_FILE_OPEN_PREFIX="code://file/"

# Cursor
export TEXTUAL_SNAPSHOT_FILE_OPEN_PREFIX="cursor://file/"

# PyCharm
export TEXTUAL_SNAPSHOT_FILE_OPEN_PREFIX="pycharm://"
```

## Common Pitfalls

| Problem | Solution |
|---------|----------|
| Flaky: Animation frame varies | Disable animations in `run_before` |
| Flaky: Cursor blink state varies | Set `cursor_blink = False` |
| Flaky: Timestamps change | Mock `datetime.now()` |
| Snapshots not in VCS | Add `__snapshots__/` to git |
| Different results in CI | Use explicit `terminal_size` |

## See Also

- [textual-testing](../textual-testing) - Functional testing with Pilot
- [textual-test-fixtures](../textual-test-fixtures) - Fixture patterns
