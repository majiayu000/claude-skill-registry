---
name: selenium
description: "Selenium WebDriver for cross-browser web automation and testing. Automate Chrome, Firefox, Safari, and Edge browsers. Use for browser testing, cross-browser automation, or web application testing."
---

# Selenium Skill

Complete guide for Selenium - cross-browser automation.

## Quick Reference

### Supported Browsers
| Browser | Driver |
|---------|--------|
| **Chrome** | ChromeDriver |
| **Firefox** | GeckoDriver |
| **Safari** | SafariDriver |
| **Edge** | EdgeDriver |

### Key Components
```
- WebDriver: Browser control
- WebElement: Page elements
- Wait: Synchronization
- Actions: Complex interactions
```

---

## 1. Installation

### Python
```bash
pip install selenium webdriver-manager
```

### Java (Maven)
```xml
<dependency>
    <groupId>org.seleniumhq.selenium</groupId>
    <artifactId>selenium-java</artifactId>
    <version>4.18.1</version>
</dependency>
```

### JavaScript
```bash
npm install selenium-webdriver
```

---

## 2. Basic Setup (Python)

### Chrome
```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Auto-install driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Navigate
driver.get("https://example.com")

# Close
driver.quit()
```

### Firefox
```python
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
```

### Options
```python
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-gpu")
options.add_argument("user-agent=Custom User Agent")

driver = webdriver.Chrome(options=options)
```

---

## 3. Finding Elements

### Locator Strategies
```python
from selenium.webdriver.common.by import By

# By ID
element = driver.find_element(By.ID, "my-id")

# By class name
element = driver.find_element(By.CLASS_NAME, "my-class")

# By name
element = driver.find_element(By.NAME, "username")

# By tag name
element = driver.find_element(By.TAG_NAME, "input")

# By link text
element = driver.find_element(By.LINK_TEXT, "Click here")
element = driver.find_element(By.PARTIAL_LINK_TEXT, "Click")

# By CSS selector
element = driver.find_element(By.CSS_SELECTOR, "div.container > p")

# By XPath
element = driver.find_element(By.XPATH, "//button[@type='submit']")

# Find multiple elements
elements = driver.find_elements(By.CSS_SELECTOR, ".item")
```

### XPath Examples
```python
# By text content
driver.find_element(By.XPATH, "//button[text()='Submit']")

# Contains text
driver.find_element(By.XPATH, "//div[contains(text(), 'Hello')]")

# By attribute
driver.find_element(By.XPATH, "//input[@placeholder='Search']")

# Parent/child
driver.find_element(By.XPATH, "//div[@class='parent']//span")

# Following sibling
driver.find_element(By.XPATH, "//label[text()='Email']/following-sibling::input")

# Index
driver.find_element(By.XPATH, "(//div[@class='item'])[1]")
```

---

## 4. Interactions

### Basic Actions
```python
# Click
element.click()

# Type text
element.send_keys("Hello World")

# Clear input
element.clear()

# Submit form
element.submit()

# Get text
text = element.text

# Get attribute
value = element.get_attribute("href")
class_name = element.get_attribute("class")

# Check state
is_displayed = element.is_displayed()
is_enabled = element.is_enabled()
is_selected = element.is_selected()
```

### Keyboard Actions
```python
from selenium.webdriver.common.keys import Keys

# Special keys
element.send_keys(Keys.ENTER)
element.send_keys(Keys.TAB)
element.send_keys(Keys.ESCAPE)

# Key combinations
element.send_keys(Keys.CONTROL + "a")
element.send_keys(Keys.CONTROL + "c")

# Clear and type
element.send_keys(Keys.CONTROL + "a")
element.send_keys("new text")
```

### Select Dropdowns
```python
from selenium.webdriver.support.ui import Select

select = Select(driver.find_element(By.ID, "dropdown"))

# By visible text
select.select_by_visible_text("Option 1")

# By value attribute
select.select_by_value("opt1")

# By index
select.select_by_index(0)

# Get selected option
selected = select.first_selected_option.text

# Get all options
options = select.options
for option in options:
    print(option.text)
```

---

## 5. Waits

### Implicit Wait
```python
# Apply to all find_element calls
driver.implicitly_wait(10)  # seconds
```

### Explicit Wait
```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 10)

# Wait for element present
element = wait.until(
    EC.presence_of_element_located((By.ID, "my-id"))
)

# Wait for element visible
element = wait.until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, ".visible"))
)

# Wait for element clickable
element = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button"))
)

# Wait for text
wait.until(
    EC.text_to_be_present_in_element((By.ID, "status"), "Complete")
)

# Wait for URL
wait.until(EC.url_contains("dashboard"))
wait.until(EC.url_to_be("https://example.com/dashboard"))

# Wait for title
wait.until(EC.title_contains("Dashboard"))
```

### Common Expected Conditions
```python
EC.presence_of_element_located()
EC.visibility_of_element_located()
EC.element_to_be_clickable()
EC.invisibility_of_element_located()
EC.staleness_of()
EC.frame_to_be_available_and_switch_to_it()
EC.alert_is_present()
EC.number_of_windows_to_be()
```

### Custom Wait
```python
def custom_condition(driver):
    element = driver.find_element(By.ID, "status")
    return element.text == "Ready"

wait.until(custom_condition)
```

---

## 6. Advanced Actions

### Action Chains
```python
from selenium.webdriver.common.action_chains import ActionChains

actions = ActionChains(driver)

# Hover
actions.move_to_element(element).perform()

# Double click
actions.double_click(element).perform()

# Right click
actions.context_click(element).perform()

# Drag and drop
actions.drag_and_drop(source, target).perform()

# Click and hold
actions.click_and_hold(element).perform()
actions.release().perform()

# Chain multiple actions
actions.move_to_element(menu).click().perform()
actions.move_to_element(submenu).click().perform()
```

### Scroll
```python
# Scroll to element
driver.execute_script("arguments[0].scrollIntoView();", element)

# Scroll by amount
driver.execute_script("window.scrollBy(0, 500);")

# Scroll to bottom
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# Scroll to top
driver.execute_script("window.scrollTo(0, 0);")
```

### JavaScript Execution
```python
# Execute script
driver.execute_script("alert('Hello');")

# Return value
title = driver.execute_script("return document.title;")

# With arguments
driver.execute_script("arguments[0].click();", element)

# Modify element
driver.execute_script(
    "arguments[0].setAttribute('style', 'background: red');",
    element
)
```

---

## 7. Frames and Windows

### Frames/iFrames
```python
# Switch to frame by element
frame = driver.find_element(By.TAG_NAME, "iframe")
driver.switch_to.frame(frame)

# Switch by name or ID
driver.switch_to.frame("frame-name")

# Switch by index
driver.switch_to.frame(0)

# Switch back to main content
driver.switch_to.default_content()

# Switch to parent frame
driver.switch_to.parent_frame()
```

### Windows/Tabs
```python
# Get current window
main_window = driver.current_window_handle

# Get all windows
windows = driver.window_handles

# Open new tab
driver.execute_script("window.open('');")

# Switch to new window
driver.switch_to.window(windows[-1])

# Switch back
driver.switch_to.window(main_window)

# Close current window
driver.close()

# Quit all windows
driver.quit()
```

### Alerts
```python
# Switch to alert
alert = driver.switch_to.alert

# Get text
text = alert.text

# Accept (OK)
alert.accept()

# Dismiss (Cancel)
alert.dismiss()

# Send text to prompt
alert.send_keys("input text")
alert.accept()
```

---

## 8. Screenshots and Files

### Screenshots
```python
# Full page
driver.save_screenshot("page.png")

# Element screenshot
element.screenshot("element.png")

# As base64
screenshot = driver.get_screenshot_as_base64()

# As PNG bytes
screenshot = driver.get_screenshot_as_png()
```

### File Upload
```python
upload = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
upload.send_keys("/path/to/file.pdf")
```

### File Download
```python
options = Options()
prefs = {
    "download.default_directory": "/path/to/download",
    "download.prompt_for_download": False,
    "download.directory_upgrade": True
}
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(options=options)
```

---

## 9. Cookies and Storage

### Cookies
```python
# Get all cookies
cookies = driver.get_cookies()

# Get specific cookie
cookie = driver.get_cookie("session_id")

# Add cookie
driver.add_cookie({
    "name": "auth",
    "value": "token123",
    "domain": "example.com"
})

# Delete cookie
driver.delete_cookie("auth")

# Delete all cookies
driver.delete_all_cookies()
```

### Local Storage
```python
# Set item
driver.execute_script("localStorage.setItem('key', 'value');")

# Get item
value = driver.execute_script("return localStorage.getItem('key');")

# Remove item
driver.execute_script("localStorage.removeItem('key');")

# Clear all
driver.execute_script("localStorage.clear();")
```

---

## 10. Page Object Model

### Base Page
```python
class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def find(self, locator):
        return self.wait.until(
            EC.presence_of_element_located(locator)
        )

    def click(self, locator):
        self.wait.until(
            EC.element_to_be_clickable(locator)
        ).click()

    def type(self, locator, text):
        element = self.find(locator)
        element.clear()
        element.send_keys(text)
```

### Page Class
```python
class LoginPage(BasePage):
    # Locators
    USERNAME = (By.ID, "username")
    PASSWORD = (By.ID, "password")
    SUBMIT = (By.CSS_SELECTOR, "button[type='submit']")
    ERROR = (By.CLASS_NAME, "error-message")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://example.com/login"

    def open(self):
        self.driver.get(self.url)
        return self

    def login(self, username, password):
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.click(self.SUBMIT)
        return DashboardPage(self.driver)

    def get_error(self):
        return self.find(self.ERROR).text
```

### Usage
```python
# In tests
login_page = LoginPage(driver).open()
dashboard = login_page.login("user", "pass")
assert dashboard.is_loaded()
```

---

## 11. Testing Integration

### pytest
```python
import pytest
from selenium import webdriver

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_login(driver):
    driver.get("https://example.com/login")
    driver.find_element(By.ID, "username").send_keys("user")
    driver.find_element(By.ID, "password").send_keys("pass")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    assert "dashboard" in driver.current_url
```

### unittest
```python
import unittest
from selenium import webdriver

class TestLogin(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()

    def test_valid_login(self):
        self.driver.get("https://example.com/login")
        # Test logic
        self.assertIn("dashboard", self.driver.current_url)

if __name__ == "__main__":
    unittest.main()
```

---

## 12. Troubleshooting

### Common Issues

**StaleElementReferenceException:**
```python
# Re-find element after page changes
try:
    element.click()
except StaleElementReferenceException:
    element = driver.find_element(By.ID, "my-id")
    element.click()
```

**TimeoutException:**
```python
from selenium.common.exceptions import TimeoutException

try:
    wait.until(EC.presence_of_element_located((By.ID, "slow")))
except TimeoutException:
    print("Element not found in time")
```

**ElementNotInteractableException:**
```python
# Wait for clickable
wait.until(EC.element_to_be_clickable((By.ID, "button")))

# Or scroll into view
driver.execute_script("arguments[0].scrollIntoView();", element)
```

---

## Best Practices

1. **Use explicit waits** - More reliable than implicit
2. **Page Object Model** - Maintainable test code
3. **Unique locators** - Prefer ID over XPath
4. **Handle exceptions** - Graceful error handling
5. **Close browsers** - Use quit() in finally/teardown
6. **Headless for CI** - Faster test execution
7. **Screenshots on failure** - Debug easier
8. **Avoid hardcoded waits** - Use conditions
9. **Parallel execution** - Faster test suites
10. **Clean test data** - Isolated tests
