---
name: playwright-testing
description: RPA workflow testing with Playwright browser automation. Covers page object model, wait strategies, screenshot testing, and browser node testing patterns. Use when: testing browser nodes, page object model, wait strategies, screenshot testing, visual regression, browser automation tests.
---

## Playwright Testing for CasareRPA

When testing browser automation workflows in CasareRPA, use these patterns for robust, maintainable tests.

## Core Patterns

### 1. Mock Page Fixture (Fastest)
```python
from tests.conftest import mock_page, mock_context

async def test_browser_node(mock_context, mock_page):
    mock_page.evaluate.return_value = {"title": "Test"}
    mock_context.get_active_page.return_value = mock_page

    node = MyNode("test")
    result = await node.execute(mock_context)

    assert result["success"] is True
```

### 2. Wait Strategies

```python
# Wait for selector (Playwright built-in)
await page.wait_for_selector("#button", timeout=5000)

# Wait for load state
await page.wait_for_load_state("networkidle")

# Wait for navigation
await page.wait_for_url("**/success")

# Custom wait with predicate
await page.wait_for_function("() => document.readyState === 'complete'")
```

### 3. Page Object Model

```python
class LoginPage:
    """Page object for login page."""

    def __init__(self, page):
        self.page = page
        self.username_input = "#username"
        self.password_input = "#password"
        self.login_button = "button[type='submit']"

    async def login(self, username: str, password: str):
        await self.page.fill(self.username_input, username)
        await self.page.fill(self.password_input, password)
        await self.page.click(self.login_button)

    async def is_logged_in(self) -> bool:
        return await self.page.locator(".user-profile").count() > 0
```

### 4. Screenshot Testing

```python
async def take_screenshot(page, path: str, full_page: bool = False):
    await page.screenshot(path=path, full_page=full_page)

# Visual regression (basic)
async def assert_screenshot_matches(page, expected_path: str, threshold: float = 0.1):
    from PIL import Image
    import io

    actual_bytes = await page.screenshot()
    actual = Image.open(io.BytesIO(actual_bytes))
    expected = Image.open(expected_path)

    # Basic pixel comparison (use playwright-compare for advanced)
    diff = sum(abs(a - b) for a, b in zip(actual.tobytes(), expected.tobytes()))
    assert diff / len(actual.tobytes()) < threshold
```

## Browser Node Testing

### Test Structure

```python
import pytest
from unittest.mock import AsyncMock, MagicMock
from casare_rpa.nodes.browser.my_node import MyNode

@pytest.fixture
def node():
    return MyNode("test_node")

@pytest.fixture
def context_with_page(mock_context, mock_page):
    mock_context.get_active_page.return_value = mock_page
    return mock_context

class TestMyNode:
    @pytest.mark.asyncio
    async def test_success(self, context_with_page, mock_page):
        mock_page.click.return_value = None
        node = MyNode("test", config={"selector": "#button"})
        result = await node.execute(context_with_page)
        assert result["success"] is True

    @pytest.mark.asyncio
    async def test_no_page_error(self, mock_context):
        mock_context.get_active_page.return_value = None
        node = MyNode("test")
        result = await node.execute(mock_context)
        assert result["success"] is False
        assert "page" in result["error"].lower()
```

## Helpers

See `examples/helpers.py` and `scripts/playwright_test_helpers.py` for:
- `create_mock_page()` - Full page mock builder
- `wait_for_element()` - Robust element waiting
- `screenshot_comparison()` - Visual diff helpers
- `browser_test_session()` - Test context manager

## Running Tests

```bash
# Browser node tests only
pytest tests/nodes/browser/ -v

# With coverage
pytest tests/nodes/browser/ --cov=casare_rpa/nodes/browser

# Skip slow integration tests
pytest tests/nodes/browser/ -m "not slow" -v
```

## Examples

- `examples/test_click_node.py` - Click interaction tests
- `examples/test_navigation.py` - Page navigation tests
- `examples/test_form_filling.py` - Form interaction patterns
- `examples/test_element_healing.py` - Selector healing tests
