---
name: playwright-e2e-testing
description: Write end-to-end tests with Playwright for web applications. Includes fixtures, page objects, test templates, visual regression testing, and accessibility audits.
---

# Playwright E2E Testing Skill

## When to Use

Use this skill when:
- Testing user workflows (sign up, login, checkout)
- Verifying form submission and validation
- Testing responsive design across devices
- Running visual regression tests
- Checking accessibility (WCAG AA)
- Testing dynamic content and API interactions
- Creating smoke tests for CI/CD

## Setup

### Install Playwright

```bash
pip install pytest-playwright
playwright install  # Download browsers (chromium, firefox, webkit)
```

### Project Structure

```
tests/
  ├── conftest.py              # Pytest fixtures
  ├── e2e/
  │   ├── test_homepage.py
  │   ├── test_product_search.py
  │   └── test_checkout.py
  └── pages/
      ├── base_page.py
      ├── homepage.py
      ├── product_page.py
      └── checkout_page.py
```

## Code Patterns

### 1. Page Object Model (POM)

```python
# tests/pages/base_page.py
from playwright.async_api import Page, expect

class BasePage:
    """Base page class with common methods"""
    
    def __init__(self, page: Page):
        self.page = page
    
    async def goto(self, url: str):
        """Navigate to URL"""
        await self.page.goto(url)
    
    async def wait_for_element(self, selector: str, timeout: int = 5000):
        """Wait for element to appear"""
        await self.page.locator(selector).wait_for(timeout=timeout)
    
    async def click(self, selector: str):
        """Click element"""
        await self.page.locator(selector).click()
    
    async def fill(self, selector: str, text: str):
        """Fill input field"""
        await self.page.locator(selector).fill(text)
    
    async def get_text(self, selector: str) -> str:
        """Get element text"""
        return await self.page.locator(selector).text_content()
    
    async def expect_visible(self, selector: str):
        """Assert element is visible"""
        await expect(self.page.locator(selector)).to_be_visible()
    
    async def expect_text(self, selector: str, text: str):
        """Assert element contains text"""
        await expect(self.page.locator(selector)).to_contain_text(text)
    
    async def screenshot(self, name: str):
        """Take screenshot for visual regression"""
        await self.page.screenshot(path=f"tests/screenshots/{name}.png")
```

### 2. Page Object for Product Search

```python
# tests/pages/product_page.py
from playwright.async_api import Page
from tests.pages.base_page import BasePage

class ProductPage(BasePage):
    """Product search and listing page"""
    
    # Selectors
    SEARCH_INPUT = 'input[placeholder="Buscar ofertas"]'
    SEARCH_BUTTON = 'button[type="submit"]'
    PRODUCT_CARD = '.product-card'
    PRODUCT_TITLE = '.product-title'
    PRODUCT_PRICE = '.product-price'
    PRODUCT_RATING = '.rating'
    SORT_DROPDOWN = 'select[name="sort"]'
    CATEGORY_FILTER = 'input[name="category"]'
    
    async def search(self, query: str):
        """Search for products"""
        await self.fill(self.SEARCH_INPUT, query)
        await self.click(self.SEARCH_BUTTON)
        await self.page.wait_for_load_state("networkidle")
    
    async def get_product_count(self) -> int:
        """Count visible products"""
        return await self.page.locator(self.PRODUCT_CARD).count()
    
    async def get_first_product_title(self) -> str:
        """Get first product title"""
        return await self.get_text(f"{self.PRODUCT_CARD}:first-child {self.PRODUCT_TITLE}")
    
    async def click_product(self, index: int = 0):
        """Click product by index"""
        products = self.page.locator(self.PRODUCT_CARD)
        await products.nth(index).click()
    
    async def filter_by_category(self, category: str):
        """Filter products by category"""
        await self.click(f'{self.CATEGORY_FILTER}[value="{category}"]')
        await self.page.wait_for_load_state("networkidle")
    
    async def sort_by(self, sort_type: str):
        """Sort products"""
        # sort_type: 'price-low-high', 'rating', 'newest'
        await self.page.select_option(self.SORT_DROPDOWN, sort_type)
        await self.page.wait_for_load_state("networkidle")
    
    async def get_price_range(self) -> tuple:
        """Get min/max price from current results"""
        prices = []
        price_elements = await self.page.locator(self.PRODUCT_PRICE).all()
        
        for element in price_elements:
            text = await element.text_content()
            # Parse "R$ 99,99" → 99.99
            price = float(text.replace("R$", "").replace(",", ".").strip())
            prices.append(price)
        
        return (min(prices), max(prices)) if prices else (0, 0)
```

### 3. Test Fixtures

```python
# tests/conftest.py
import pytest
from playwright.async_api import async_playwright, Browser, BrowserContext, Page
from tests.pages.product_page import ProductPage

BASE_URL = "http://localhost:3000"

@pytest.fixture(scope="session")
async def browser() -> Browser:
    """Create browser session"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        yield browser
        await browser.close()

@pytest.fixture
async def context(browser: Browser) -> BrowserContext:
    """Create browser context"""
    context = await browser.new_context()
    yield context
    await context.close()

@pytest.fixture
async def page(context: BrowserContext) -> Page:
    """Create page object"""
    return await context.new_page()

@pytest.fixture
async def product_page(page: Page) -> ProductPage:
    """Instantiate ProductPage"""
    product_page = ProductPage(page)
    await product_page.goto(BASE_URL)
    return product_page

# Async test marker
def pytest_collection_modifyitems(items):
    for item in items:
        item.add_marker(pytest.mark.asyncio)
```

### 4. E2E Test Examples

```python
# tests/e2e/test_product_search.py
import pytest
from tests.pages.product_page import ProductPage

class TestProductSearch:
    """Test product search functionality"""
    
    @pytest.mark.asyncio
    async def test_search_returns_results(self, product_page: ProductPage):
        """Should return products for valid search"""
        await product_page.search("smartphone")
        
        count = await product_page.get_product_count()
        assert count > 0, "Should return at least one product"
        
        title = await product_page.get_first_product_title()
        assert "smartphone" in title.lower(), "Product should match search query"
    
    @pytest.mark.asyncio
    async def test_search_no_results(self, product_page: ProductPage):
        """Should handle empty results"""
        await product_page.search("xyzabc123nonexistent")
        
        count = await product_page.get_product_count()
        assert count == 0, "Should return no products"
        
        # Verify "no results" message
        await product_page.expect_text('.no-results', "Nenhum produto encontrado")
    
    @pytest.mark.asyncio
    async def test_filter_by_category(self, product_page: ProductPage):
        """Should filter products by category"""
        await product_page.filter_by_category("electronics")
        
        count = await product_page.get_product_count()
        assert count > 0, "Should return electronics products"
    
    @pytest.mark.asyncio
    async def test_sort_by_price(self, product_page: ProductPage):
        """Should sort products by price (low to high)"""
        await product_page.search("smartphone")
        await product_page.sort_by("price-low-high")
        
        min_price, max_price = await product_page.get_price_range()
        assert min_price <= max_price, "Prices should be in ascending order"
    
    @pytest.mark.asyncio
    async def test_pagination(self, product_page: ProductPage):
        """Should paginate results"""
        await product_page.search("teclado")
        
        # Get products on page 1
        count_page1 = await product_page.get_product_count()
        
        # Go to page 2
        await product_page.click('a[aria-label="Next page"]')
        await product_page.page.wait_for_load_state("networkidle")
        
        count_page2 = await product_page.get_product_count()
        assert count_page1 > 0 and count_page2 > 0, "Both pages should have products"
```

### 5. Visual Regression Testing

```python
# tests/e2e/test_visual_regression.py
import pytest

class TestVisualRegression:
    """Test visual consistency across changes"""
    
    @pytest.mark.asyncio
    async def test_homepage_visual(self, product_page: ProductPage):
        """Compare homepage visual appearance"""
        await product_page.goto("http://localhost:3000")
        
        # Compare with baseline screenshot
        await product_page.page.expect_screenshot(
            name="homepage.png",
            mask_locator='[aria-label="Last updated"]'  # Ignore dynamic elements
        )
    
    @pytest.mark.asyncio
    async def test_product_card_visual(self, product_page: ProductPage):
        """Compare product card design"""
        await product_page.search("monitor")
        
        product_element = product_page.page.locator('.product-card').first
        
        await expect(product_element).to_have_screenshot("product-card.png")
```

### 6. Accessibility Testing

```python
# tests/e2e/test_accessibility.py
import pytest
from playwright.async_api import expect

class TestAccessibility:
    """Test WCAG AA compliance"""
    
    @pytest.mark.asyncio
    async def test_form_labels(self, page):
        """All inputs should have associated labels"""
        await page.goto("http://localhost:3000")
        
        inputs = await page.locator('input').all()
        
        for input_elem in inputs:
            # Check for associated label
            input_id = await input_elem.get_attribute("id")
            
            if input_id:
                label = page.locator(f'label[for="{input_id}"]')
                await expect(label).to_be_visible()
    
    @pytest.mark.asyncio
    async def test_button_contrast(self, page):
        """Buttons should have sufficient color contrast"""
        await page.goto("http://localhost:3000")
        
        buttons = await page.locator('button').all()
        
        for button in buttons:
            # This would require a contrast checking library
            # Example: check computed styles
            color = await button.evaluate("el => window.getComputedStyle(el).color")
            bg_color = await button.evaluate("el => window.getComputedStyle(el).backgroundColor")
            
            # Verify contrast ratio >= 4.5:1
            # Use contrast checking library for precise calculation
    
    @pytest.mark.asyncio
    async def test_keyboard_navigation(self, page):
        """Page should be navigable with keyboard"""
        await page.goto("http://localhost:3000")
        
        # Tab through interactive elements
        await page.keyboard.press("Tab")
        
        # Check focus is visible
        focused = await page.evaluate("document.activeElement")
        assert focused is not None, "Focus should be visible after Tab"
    
    @pytest.mark.asyncio
    async def test_mobile_responsive(self, browser):
        """Test on mobile viewport (375x667)"""
        context = await browser.new_context(
            viewport={"width": 375, "height": 667}
        )
        page = await context.new_page()
        
        await page.goto("http://localhost:3000")
        
        # Verify content is readable
        await expect(page.locator('h1')).to_be_visible()
        await expect(page.locator('nav')).to_be_visible()
        
        await context.close()
```

### 7. Running Tests

```bash
# Run all tests
pytest tests/e2e/

# Run specific test file
pytest tests/e2e/test_product_search.py

# Run with verbose output
pytest -v tests/e2e/

# Run in headed mode (see browser)
pytest tests/e2e/ --headed

# Run specific test
pytest tests/e2e/test_product_search.py::TestProductSearch::test_search_returns_results

# Generate HTML report
pytest tests/e2e/ --html=report.html

# Run with screenshots on failure
pytest tests/e2e/ --screenshot=only-on-failure
```

## Best Practices

✅ Use **Page Object Model** for maintainability  
✅ **Wait for elements** properly (not sleep)  
✅ **Test user flows**, not implementation details  
✅ **Mock external APIs** when possible  
✅ **Use fixtures** for setup/teardown  
✅ **Name tests clearly** (test_search_returns_results)  
✅ **Keep tests independent** (no test order dependency)  
✅ **Screenshot baselines** for visual regression  
✅ **Check accessibility** in every test  

## Related Files

- [page-factory.py](./page-factory.py) - Page object factory
- [test-templates.py](./test-templates.py) - Copy-paste test templates
- [ci-config.yml](./ci-config.yml) - GitHub Actions workflow

## References

- Playwright: https://playwright.dev/python/
- Pytest: https://docs.pytest.org/
- Playwright BDD: https://playwright.dev/python/docs/bdd
