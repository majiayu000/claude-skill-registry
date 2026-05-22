---
name: gauge
description: |
    Use when writing markdown-based test specifications with the Gauge framework (ThoughtWorks). Covers specification files, scenarios, steps, concepts, data tables, tags, step implementations, data-driven testing, and reporting.
    USE FOR: markdown test specifications, free-form acceptance tests, Gauge spec files, concept-based test abstraction, data-driven test specs, cross-language test automation with Gauge runners
    DO NOT USE FOR: structured Given/When/Then specs (use gherkin), requirements documentation (use prd or trd), architecture diagrams (use diagramming sub-skills)
license: MIT
metadata:
  displayName: "Gauge"
  author: "Tyler-R-Kendrick"
compatibility: claude, copilot, cursor
references:
  - title: "Gauge Official Documentation"
    url: "https://docs.gauge.org/"
  - title: "Gauge — GitHub Repository"
    url: "https://github.com/getgauge/gauge"
---

# Gauge

## Overview
Gauge is an open-source test automation framework created by ThoughtWorks that uses Markdown as its specification language. Unlike Gherkin's rigid `Given/When/Then` structure, Gauge allows free-form, natural-language specifications written as plain Markdown files (`.spec`). This makes specifications more readable for non-technical stakeholders while remaining fully executable.

Gauge separates the *specification layer* (Markdown) from the *implementation layer* (code in any supported language), enabling teams to write test specs that read like documentation.

## Core Concepts

### Specification Files (.spec)
A specification is a Markdown file containing a heading (the spec name) and one or more scenarios.

```markdown
# User Authentication

This specification covers the login and logout flows
for registered users of the application.

## Successful Login

* Navigate to the login page
* Enter username "alice@example.com"
* Enter password "Str0ng!Pass"
* Click the login button
* Verify the dashboard is displayed
* Verify the welcome message shows "Hello, Alice"

## Failed Login with Wrong Password

* Navigate to the login page
* Enter username "alice@example.com"
* Enter password "wrong-password"
* Click the login button
* Verify the error message "Invalid credentials" is displayed
```

- The `#` heading is the **specification name**.
- The `##` headings are **scenario names**.
- Lines beginning with `*` are **steps**.
- Free-form text between headings is documentation (not executed).

### Steps
Steps are the executable units in Gauge. Each step in the spec maps to a step implementation in code.

Steps can contain **parameters** in quotes or angle brackets:
- Static parameters: `* Enter username "alice@example.com"`
- Dynamic parameters: `* Enter username <username>`
- Table parameters (passed as data tables)
- File parameters: `* Upload file <file:data/sample.csv>`

### Concepts
Concepts are reusable groups of steps -- like macros or subroutines for specifications. They are defined in `.cpt` files.

**File: `specs/concepts/login.cpt`**
```markdown
# Login as user <username> with password <password>

* Navigate to the login page
* Enter username <username>
* Enter password <password>
* Click the login button
```

**Using the concept in a spec:**
```markdown
## Successful Login

* Login as user "alice@example.com" with password "Str0ng!Pass"
* Verify the dashboard is displayed
```

Concepts reduce duplication and create a higher-level vocabulary for specs.

### Tags
Tags categorize specifications and scenarios for filtered execution.

```markdown
# User Authentication

Tags: authentication, smoke

## Successful Login

Tags: happy-path, critical

* Login as user "alice@example.com" with password "Str0ng!Pass"
* Verify the dashboard is displayed
```

Run filtered: `gauge run --tags "smoke & !wip" specs/`

### Data Tables
Tabular data can be embedded directly in specifications for data-driven scenarios.

```markdown
## Create users with different roles

   | username | role   | permissions        |
   |----------|--------|--------------------|
   | alice    | admin  | read,write,delete  |
   | bob      | editor | read,write         |
   | charlie  | viewer | read               |

* Create user <username> with role <role>
* Verify user <username> has permissions <permissions>
```

The scenario runs once per row with the column values substituted into the dynamic parameters.

### Data-Driven Testing with External Sources
Gauge supports CSV and other external data sources for large data sets.

**Using a CSV data source:**
```markdown
## Validate product pricing

Tags: data-driven

table: data/products.csv

* Search for product <name>
* Verify the displayed price is <expected_price>
* Verify the stock status is <stock_status>
```

**`data/products.csv`:**
```csv
name,expected_price,stock_status
Wireless Mouse,$29.99,In Stock
Mechanical KB,$89.99,In Stock
USB-C Hub,$49.99,Out of Stock
```

### Teardown Steps
Steps that run after every scenario in a specification, used for cleanup.

```markdown
# Shopping Cart

## Add item to cart

* Login as user "shopper@example.com" with password "Pass123"
* Add product "Wireless Mouse" to cart
* Verify cart contains 1 item

## Remove item from cart

* Login as user "shopper@example.com" with password "Pass123"
* Add product "Wireless Mouse" to cart
* Remove product "Wireless Mouse" from cart
* Verify cart is empty

___
* Clear the shopping cart
* Logout the current user
```

The `___` (three or more underscores) marks the beginning of teardown steps.

### Context Steps
Steps that run before every scenario in a specification, similar to Gherkin's `Background`.

```markdown
# Shopping Cart

* Login as user "shopper@example.com" with password "Pass123"
* Navigate to the product catalog

## Add item to cart

* Add product "Wireless Mouse" to cart
* Verify cart contains 1 item

## View empty cart

* Navigate to the cart page
* Verify the cart is empty
```

Steps placed between the specification heading and the first scenario heading are context steps.

## Step Implementations

### JavaScript / TypeScript
```javascript
const { Step, BeforeSuite, AfterSuite } = require('gauge-ts');
const { openBrowser, closeBrowser, goto, click, write, into, textBox, text } = require('taiko');

Step('Navigate to the login page', async () => {
    await goto('https://app.example.com/login');
});

Step('Enter username <username>', async (username) => {
    await write(username, into(textBox({ id: 'email' })));
});

Step('Enter password <password>', async (password) => {
    await write(password, into(textBox({ id: 'password' })));
});

Step('Click the login button', async () => {
    await click('Login');
});

Step('Verify the dashboard is displayed', async () => {
    assert.ok(await text('Dashboard').exists());
});
```

### C# (.NET)
```csharp
using Gauge.CSharp.Lib.Attribute;
using FluentAssertions;

public class LoginSteps
{
    [Step("Navigate to the login page")]
    public void NavigateToLogin()
    {
        // navigate to login page
    }

    [Step("Enter username <username>")]
    public void EnterUsername(string username)
    {
        // type username into field
    }

    [Step("Enter password <password>")]
    public void EnterPassword(string password)
    {
        // type password into field
    }

    [Step("Verify the error message <message> is displayed")]
    public void VerifyErrorMessage(string message)
    {
        // assert error message
    }
}
```

### Python
```python
from getgauge.python import step, before_suite, after_suite

@step("Navigate to the login page")
def navigate_to_login():
    # navigate to login page
    pass

@step("Enter username <username>")
def enter_username(username):
    # type username into field
    pass

@step("Enter password <password>")
def enter_password(password):
    # type password into field
    pass

@step("Verify the dashboard is displayed")
def verify_dashboard():
    # assert dashboard is visible
    pass
```

### Java
```java
import com.thoughtworks.gauge.Step;

public class LoginSteps {
    @Step("Navigate to the login page")
    public void navigateToLogin() {
        // navigate to login page
    }

    @Step("Enter username <username>")
    public void enterUsername(String username) {
        // type username into field
    }

    @Step("Enter password <password>")
    public void enterPassword(String password) {
        // type password into field
    }

    @Step("Verify the dashboard is displayed")
    public void verifyDashboard() {
        // assert dashboard is visible
    }
}
```

## Complete Specification Example

```markdown
# E-Commerce Checkout

Tags: checkout, e2e

This specification covers the end-to-end checkout process
including cart review, shipping, payment, and order confirmation.

* Login as user "shopper@example.com" with password "Shop!Pass1"
* Navigate to the product catalog

## Purchase a single item

Tags: happy-path, smoke

* Add product "Wireless Mouse" to the cart
* Navigate to the cart page
* Verify the cart total is "$29.99"
* Proceed to checkout
* Enter shipping address:

   | field       | value              |
   |-------------|--------------------|
   | name        | Alice Smith        |
   | street      | 123 Main St        |
   | city        | Springfield        |
   | state       | IL                 |
   | zip         | 62701              |

* Select shipping method "Standard (5-7 days)"
* Enter payment card "4111111111111111" expiry "12/27" cvv "123"
* Place the order
* Verify order confirmation is displayed
* Verify confirmation email is sent to "shopper@example.com"

## Apply discount code during checkout

Tags: discounts

* Add product "Mechanical KB" to the cart
* Navigate to the cart page
* Apply discount code "SAVE10"
* Verify the discount of "10%" is applied
* Verify the cart total is "$80.99"
* Proceed to checkout
* Place the order with saved shipping and payment
* Verify order confirmation is displayed

## Checkout with empty cart

Tags: negative

* Navigate to the cart page
* Verify the cart is empty
* Verify the checkout button is disabled
* Verify the message "Add items to your cart to proceed" is displayed

___
* Clear the shopping cart
* Logout the current user
```

## Reporting

Gauge generates reports automatically after each run.

| Format | Command Flag | Output |
|--------|-------------|--------|
| HTML | `--env default` (default) | `reports/html-report/index.html` |
| XML (JUnit) | Plugin: `gauge-xml-report` | `reports/xml-report/` |
| JSON | Plugin: `gauge-json-report` | `reports/json-report/result.json` |
| Spectacle | Plugin: `spectacle` | Interactive HTML dashboard |

Generate HTML report: `gauge run specs/`
Generate XML for CI: `gauge install xml-report && gauge run specs/`

## Gauge vs Gherkin

| Aspect | Gauge | Gherkin |
|--------|-------|---------|
| **Syntax** | Free-form Markdown | Structured Given/When/Then keywords |
| **File format** | `.spec` (Markdown) | `.feature` |
| **Readability** | Reads like documentation | Reads like structured test cases |
| **Flexibility** | Any natural language phrasing | Must follow keyword grammar |
| **Abstraction** | Concepts (`.cpt` files) | No built-in macro system |
| **Data tables** | Markdown tables + external CSV | Inline Examples tables |
| **Context steps** | Steps before first scenario | `Background` keyword |
| **Teardown** | `___` separator section | Hooks in code |
| **Runners** | Java, C#, JS, Python, Ruby, Go | Cucumber (Java), Behave (Python), SpecFlow/Reqnroll (C#), etc. |
| **Best for** | Teams wanting documentation-first specs | Teams wanting structured BDD with strict grammar |

## CLI Reference

```bash
# Install Gauge
npm install -g @getgauge/cli
# or: brew install gauge

# Initialize a new project
gauge init js        # JavaScript
gauge init csharp    # C#
gauge init python    # Python
gauge init java      # Java

# Run all specs
gauge run specs/

# Run specific spec file
gauge run specs/checkout.spec

# Run by tags
gauge run --tags "smoke" specs/
gauge run --tags "checkout & !wip" specs/

# Run in parallel
gauge run --parallel -n 4 specs/

# Validate specs (check for unimplemented steps)
gauge validate specs/

# List unimplemented steps
gauge --unimplemented specs/

# Install plugins
gauge install html-report
gauge install xml-report
gauge install json-report
```

## Project Structure

```
project-root/
  env/
    default/
      default.properties
  specs/
    concepts/
      login.cpt
      navigation.cpt
    authentication/
      login.spec
      registration.spec
    checkout/
      checkout.spec
      payment.spec
    data/
      products.csv
      users.csv
  tests/           # Step implementations
    authentication_steps.js
    checkout_steps.js
    hooks.js
  manifest.json
```

## Best Practices

- **Write specs as documentation first** -- the specification should be readable and valuable even without the automation layer.
- **Use concepts to build a domain vocabulary** -- concepts create a high-level language specific to your application that makes specs concise and expressive.
- **Keep steps atomic** -- each step should do one thing. Compose complex behaviors using concepts.
- **Use context steps for shared setup** -- avoid duplicating login or navigation steps across every scenario.
- **Use teardown steps for cleanup** -- ensure each scenario leaves the system in a clean state.
- **Externalize large data sets** -- use CSV files for data-driven testing rather than embedding large tables in spec files.
- **Tag consistently** -- adopt a tagging convention (`smoke`, `regression`, `wip`, feature area tags) and document it for the team.
- **Run specs in parallel** -- Gauge supports parallel execution natively; structure specs to be independent so they run reliably in parallel.
- **Integrate with CI/CD** -- use XML or JSON reports for CI integration and HTML reports for human review.
- **Validate specs regularly** -- run `gauge validate` in CI to catch unimplemented steps early.
