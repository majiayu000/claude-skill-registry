---
name: acceptance-testing
description: |
    Use for verifying business requirements with executable specifications using BDD frameworks. Covers Cucumber (Java, JS, Ruby), SpecFlow/Reqnroll (C#), Behave (Python), Gauge (ThoughtWorks), and Godog (Go). Includes Gherkin feature files, step definitions, BDD workflow, and cross-language examples.
    USE FOR: Cucumber, SpecFlow, Reqnroll, Behave, Gauge, Godog, BDD test automation, step definitions, acceptance criteria verification, Given-When-Then execution, executable specifications, living documentation
    DO NOT USE FOR: writing Gherkin specification syntax (use specs/documentation/gherkin), writing Gauge specification syntax (use specs/documentation/gauge), unit testing (use unit-testing), API testing (use api-testing)
license: MIT
metadata:
  displayName: "Acceptance Testing (BDD)"
  author: "Tyler-R-Kendrick"
compatibility: claude, copilot, cursor
references:
  - title: "Cucumber Documentation"
    url: "https://cucumber.io/docs"
  - title: "SpecFlow Documentation"
    url: "https://docs.specflow.org"
  - title: "Gauge Documentation (ThoughtWorks)"
    url: "https://docs.gauge.org"
---

# Acceptance Testing (BDD)

## Overview
Acceptance testing verifies that software meets business requirements by executing human-readable specifications. Behavior-Driven Development (BDD) bridges the gap between business stakeholders and developers through a collaborative workflow: business rules are written as executable specifications (feature files), automated with step definitions, and run as part of the CI pipeline.

> For Gherkin specification syntax (Given/When/Then), see **specs/documentation/gherkin**.
> For Gauge specification syntax (Markdown specs), see **specs/documentation/gauge**.

## BDD Workflow

```
  Collaborate          Specify            Automate           Validate
 ┌──────────┐     ┌──────────────┐    ┌──────────────┐   ┌──────────────┐
 │ Business  │────►│   Feature    │───►│    Step      │──►│  CI Pipeline │
 │ + Dev +   │     │   Files      │    │  Definitions │   │  Execution   │
 │ QA discuss│     │ (Gherkin/    │    │ (code that   │   │  + Reports   │
 │ examples  │     │  Gauge spec) │    │  runs specs) │   │              │
 └──────────┘     └──────────────┘    └──────────────┘   └──────────────┘
```

1. **Collaborate** — Business, dev, and QA discuss requirements using concrete examples (Example Mapping, Three Amigos).
2. **Specify** — Write executable specifications in Gherkin or Gauge Markdown format.
3. **Automate** — Implement step definitions that translate specification steps into code.
4. **Validate** — Run specifications as automated tests in CI; generate living documentation.

---

## Cross-Platform Tools

| Tool | Languages | Spec Format | Strengths |
|------|-----------|-------------|-----------|
| **Cucumber** | Java, JS/TS, Ruby | Gherkin (.feature) | Industry standard, largest ecosystem |
| **SpecFlow / Reqnroll** | C# (.NET) | Gherkin (.feature) | .NET-native, context injection, parallel execution |
| **Behave** | Python | Gherkin (.feature) | Pythonic, fixtures, environment hooks |
| **Gauge** | Java, JS, C#, Python, Ruby, Go | Markdown (.spec) | Markdown specs, concept reuse, data tables |
| **Godog** | Go | Gherkin (.feature) | Go-native, godog.Suite, step definitions |

---

## Gherkin Feature File Example

```gherkin
# features/user-registration.feature
Feature: User Registration
  As a new visitor
  I want to create an account
  So that I can access personalized features

  Background:
    Given the registration page is displayed

  Scenario: Successful registration with valid details
    When I fill in the registration form with:
      | field    | value              |
      | name     | Jane Doe           |
      | email    | jane@example.com   |
      | password | SecurePass123!     |
    And I accept the terms of service
    And I click the "Register" button
    Then I should see a welcome message "Welcome, Jane Doe!"
    And a confirmation email should be sent to "jane@example.com"

  Scenario: Registration fails with duplicate email
    Given a user exists with email "jane@example.com"
    When I fill in the registration form with:
      | field    | value              |
      | name     | Jane Doe           |
      | email    | jane@example.com   |
      | password | SecurePass123!     |
    And I click the "Register" button
    Then I should see an error "An account with this email already exists"

  Scenario Outline: Registration fails with invalid input
    When I fill in "<field>" with "<value>"
    And I click the "Register" button
    Then I should see an error "<error>"

    Examples:
      | field    | value        | error                              |
      | name     |              | Name is required                   |
      | email    | not-an-email | Please enter a valid email address |
      | password | short        | Password must be at least 8 chars  |
```

---

## Step Definitions by Language

### JavaScript / TypeScript (Cucumber.js)

```javascript
// features/step-definitions/registration.steps.js
const { Given, When, Then } = require("@cucumber/cucumber");
const { expect } = require("@playwright/test");

Given("the registration page is displayed", async function () {
    await this.page.goto("/register");
    await expect(this.page.locator("h1")).toHaveText("Create Account");
});

Given("a user exists with email {string}", async function (email) {
    // Seed the database or call an API to create the user
    await this.api.post("/test/seed-user", { email });
});

When("I fill in the registration form with:", async function (dataTable) {
    const rows = dataTable.rowsHash();
    for (const [field, value] of Object.entries(rows)) {
        await this.page.fill(`[name="${field}"]`, value);
    }
});

When("I fill in {string} with {string}", async function (field, value) {
    await this.page.fill(`[name="${field}"]`, value);
});

When("I accept the terms of service", async function () {
    await this.page.check("#terms-checkbox");
});

When("I click the {string} button", async function (buttonText) {
    await this.page.click(`button:has-text("${buttonText}")`);
});

Then("I should see a welcome message {string}", async function (message) {
    await expect(this.page.locator(".welcome-message")).toHaveText(message);
});

Then(
    "a confirmation email should be sent to {string}",
    async function (email) {
        // Verify via test email service (e.g., Mailhog, Mailtrap)
        const emails = await this.mailService.getEmails(email);
        expect(emails.length).toBeGreaterThan(0);
        expect(emails[0].subject).toContain("Confirm your account");
    }
);

Then("I should see an error {string}", async function (errorMessage) {
    await expect(this.page.locator(".error-message")).toHaveText(errorMessage);
});
```

```javascript
// features/support/world.js
const { setWorldConstructor, Before, After } = require("@cucumber/cucumber");
const { chromium } = require("@playwright/test");

class CustomWorld {
    constructor() {
        this.page = null;
        this.browser = null;
        this.api = null;
    }
}

setWorldConstructor(CustomWorld);

Before(async function () {
    this.browser = await chromium.launch();
    const context = await this.browser.newContext();
    this.page = await context.newPage();
});

After(async function () {
    await this.browser?.close();
});
```

### C# (SpecFlow / Reqnroll)

```csharp
// Features/StepDefinitions/RegistrationSteps.cs
using Reqnroll;               // or TechTalk.SpecFlow for SpecFlow
using Microsoft.Playwright;
using Xunit;

[Binding]
public class RegistrationSteps
{
    private readonly IPage _page;
    private readonly ApiClient _api;

    // Context injection — Reqnroll/SpecFlow injects shared state automatically
    public RegistrationSteps(BrowserContext context, ApiClient api)
    {
        _page = context.Page;
        _api = api;
    }

    [Given("the registration page is displayed")]
    public async Task GivenTheRegistrationPageIsDisplayed()
    {
        await _page.GotoAsync("/register");
        var heading = await _page.TextContentAsync("h1");
        Assert.Equal("Create Account", heading);
    }

    [Given("a user exists with email {string}")]
    public async Task GivenAUserExistsWithEmail(string email)
    {
        await _api.PostAsync("/test/seed-user", new { Email = email });
    }

    [When("I fill in the registration form with:")]
    public async Task WhenIFillInTheRegistrationFormWith(Table table)
    {
        foreach (var row in table.Rows)
        {
            var field = row["field"];
            var value = row["value"];
            await _page.FillAsync($"[name=\"{field}\"]", value);
        }
    }

    [When("I accept the terms of service")]
    public async Task WhenIAcceptTheTermsOfService()
    {
        await _page.CheckAsync("#terms-checkbox");
    }

    [When("I click the {string} button")]
    public async Task WhenIClickTheButton(string buttonText)
    {
        await _page.ClickAsync($"button:has-text(\"{buttonText}\")");
    }

    [Then("I should see a welcome message {string}")]
    public async Task ThenIShouldSeeAWelcomeMessage(string message)
    {
        var text = await _page.TextContentAsync(".welcome-message");
        Assert.Equal(message, text);
    }

    [Then("a confirmation email should be sent to {string}")]
    public async Task ThenAConfirmationEmailShouldBeSentTo(string email)
    {
        var emails = await _api.GetAsync<List<Email>>($"/test/emails?to={email}");
        Assert.NotEmpty(emails);
        Assert.Contains("Confirm your account", emails[0].Subject);
    }

    [Then("I should see an error {string}")]
    public async Task ThenIShouldSeeAnError(string errorMessage)
    {
        var text = await _page.TextContentAsync(".error-message");
        Assert.Equal(errorMessage, text);
    }
}
```

### Python (Behave)

```python
# features/steps/registration_steps.py
from behave import given, when, then
from playwright.sync_api import expect


@given("the registration page is displayed")
def step_registration_page(context):
    context.page.goto("/register")
    expect(context.page.locator("h1")).to_have_text("Create Account")


@given('a user exists with email "{email}"')
def step_user_exists(context, email):
    context.api.post("/test/seed-user", json={"email": email})


@when("I fill in the registration form with")
def step_fill_form(context):
    for row in context.table:
        field = row["field"]
        value = row["value"]
        context.page.fill(f'[name="{field}"]', value)


@when('I fill in "{field}" with "{value}"')
def step_fill_field(context, field, value):
    context.page.fill(f'[name="{field}"]', value)


@when("I accept the terms of service")
def step_accept_terms(context):
    context.page.check("#terms-checkbox")


@when('I click the "{button_text}" button')
def step_click_button(context, button_text):
    context.page.click(f'button:has-text("{button_text}")')


@then('I should see a welcome message "{message}"')
def step_welcome_message(context, message):
    expect(context.page.locator(".welcome-message")).to_have_text(message)


@then('a confirmation email should be sent to "{email}"')
def step_confirmation_email(context, email):
    emails = context.mail_service.get_emails(email)
    assert len(emails) > 0
    assert "Confirm your account" in emails[0]["subject"]


@then('I should see an error "{error_message}"')
def step_error_message(context, error_message):
    expect(context.page.locator(".error-message")).to_have_text(error_message)
```

```python
# features/environment.py
from playwright.sync_api import sync_playwright
import requests


def before_all(context):
    context.playwright = sync_playwright().start()
    context.browser = context.playwright.chromium.launch()


def before_scenario(context, scenario):
    context.browser_context = context.browser.new_context()
    context.page = context.browser_context.new_page()
    context.api = requests.Session()
    context.api.base_url = "http://localhost:3000"


def after_scenario(context, scenario):
    context.browser_context.close()


def after_all(context):
    context.browser.close()
    context.playwright.stop()
```

---

## Gauge

### Overview
Gauge (by ThoughtWorks) uses Markdown-based specification files instead of Gherkin. Specifications are written as natural-language steps in `.spec` files, with reusable abstractions called "concepts".

> For Gauge specification syntax details, see **specs/documentation/gauge**.

### Gauge Spec Example

```markdown
# User Registration

## Successful registration with valid details
Tags: registration, smoke

* Navigate to the registration page
* Fill in registration form with name "Jane Doe" and email "jane@example.com" and password "SecurePass123!"
* Accept terms of service
* Click the "Register" button
* Verify welcome message "Welcome, Jane Doe!" is displayed
* Verify confirmation email sent to "jane@example.com"

## Registration fails with duplicate email
Tags: registration, negative

* Ensure user exists with email "jane@example.com"
* Navigate to the registration page
* Fill in registration form with name "Jane Doe" and email "jane@example.com" and password "SecurePass123!"
* Click the "Register" button
* Verify error message "An account with this email already exists" is displayed
```

### Gauge Concept (Reusable Step Group)

```markdown
# Register a new user with <name> and <email>
* Navigate to the registration page
* Fill in registration form with name <name> and email <email> and password "DefaultPass123!"
* Accept terms of service
* Click the "Register" button
```

### Gauge Step Implementation (JavaScript)

```javascript
// tests/step_implementations/registration.js
const { Step, BeforeSuite, AfterSuite } = require("gauge-ts");
const { openBrowser, closeBrowser, goto, write, click, into, textBox, text, checkBox } = require("taiko");

Step("Navigate to the registration page", async () => {
    await goto("http://localhost:3000/register");
});

Step(
    "Fill in registration form with name <name> and email <email> and password <password>",
    async (name, email, password) => {
        await write(name, into(textBox({ name: "name" })));
        await write(email, into(textBox({ name: "email" })));
        await write(password, into(textBox({ name: "password" })));
    }
);

Step("Accept terms of service", async () => {
    await checkBox({ id: "terms-checkbox" }).check();
});

Step("Click the <buttonText> button", async (buttonText) => {
    await click(buttonText);
});

Step("Verify welcome message <message> is displayed", async (message) => {
    assert(await text(message).exists());
});

Step("Verify error message <message> is displayed", async (message) => {
    assert(await text(message).exists());
});
```

---

## Godog (Go)

### Overview
Godog is the official Cucumber BDD framework for Go. It uses standard Gherkin feature files with step definitions written in Go.

### Step Definitions

```go
// features/registration_test.go
package features

import (
    "context"
    "fmt"
    "net/http"
    "testing"

    "github.com/cucumber/godog"
    "github.com/playwright-community/playwright-go"
)

type registrationContext struct {
    page    playwright.Page
    browser playwright.Browser
}

func (rc *registrationContext) theRegistrationPageIsDisplayed() error {
    _, err := rc.page.Goto("http://localhost:3000/register")
    if err != nil {
        return err
    }
    heading, err := rc.page.TextContent("h1")
    if err != nil {
        return err
    }
    if heading != "Create Account" {
        return fmt.Errorf("expected 'Create Account', got '%s'", heading)
    }
    return nil
}

func (rc *registrationContext) aUserExistsWithEmail(email string) error {
    resp, err := http.Post(
        "http://localhost:3000/test/seed-user",
        "application/json",
        strings.NewReader(fmt.Sprintf(`{"email":"%s"}`, email)),
    )
    if err != nil {
        return err
    }
    defer resp.Body.Close()
    return nil
}

func (rc *registrationContext) iFillInWithValue(field, value string) error {
    return rc.page.Fill(fmt.Sprintf(`[name="%s"]`, field), value)
}

func (rc *registrationContext) iClickTheButton(buttonText string) error {
    return rc.page.Click(fmt.Sprintf(`button:has-text("%s")`, buttonText))
}

func (rc *registrationContext) iShouldSeeAnError(message string) error {
    text, err := rc.page.TextContent(".error-message")
    if err != nil {
        return err
    }
    if text != message {
        return fmt.Errorf("expected error '%s', got '%s'", message, text)
    }
    return nil
}

func InitializeScenario(ctx *godog.ScenarioContext) {
    rc := &registrationContext{}

    ctx.Before(func(ctx context.Context, sc *godog.Scenario) (context.Context, error) {
        pw, _ := playwright.Run()
        browser, _ := pw.Chromium.Launch()
        page, _ := browser.NewPage()
        rc.browser = browser
        rc.page = page
        return ctx, nil
    })

    ctx.After(func(ctx context.Context, sc *godog.Scenario, err error) (context.Context, error) {
        rc.browser.Close()
        return ctx, nil
    })

    ctx.Step(`^the registration page is displayed$`, rc.theRegistrationPageIsDisplayed)
    ctx.Step(`^a user exists with email "([^"]*)"$`, rc.aUserExistsWithEmail)
    ctx.Step(`^I fill in "([^"]*)" with "([^"]*)"$`, rc.iFillInWithValue)
    ctx.Step(`^I click the "([^"]*)" button$`, rc.iClickTheButton)
    ctx.Step(`^I should see an error "([^"]*)"$`, rc.iShouldSeeAnError)
}

func TestFeatures(t *testing.T) {
    suite := godog.TestSuite{
        ScenarioInitializer: InitializeScenario,
        Options: &godog.Options{
            Format:   "pretty",
            Paths:    []string{"features"},
            TestingT: t,
        },
    }
    if suite.Run() != 0 {
        t.Fatal("non-zero exit code from godog")
    }
}
```

---

## CI Integration

### Cucumber.js CI Pipeline

```yaml
# .github/workflows/acceptance.yml
name: Acceptance Tests
on: [push, pull_request]

jobs:
  acceptance-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - run: npx playwright install --with-deps
      - run: npm start &
      - run: npx wait-on http://localhost:3000
      - run: npx cucumber-js --format json:results/cucumber.json --format html:results/report.html
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: acceptance-results
          path: results/
```

### Reqnroll / SpecFlow CI Pipeline

```yaml
# .github/workflows/acceptance-dotnet.yml
name: Acceptance Tests (.NET)
on: [push, pull_request]

jobs:
  acceptance-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-dotnet@v4
        with:
          dotnet-version: 8.0.x
      - run: dotnet restore
      - run: dotnet build --no-restore
      - run: dotnet test --no-build --logger "trx;LogFileName=results.trx"
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: acceptance-results
          path: "**/*.trx"
```

### Gauge CI Pipeline

```yaml
# .github/workflows/gauge.yml
name: Gauge Acceptance Tests
on: [push, pull_request]

jobs:
  gauge-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm install -g @getgauge/cli
      - run: gauge install js
      - run: gauge install html-report
      - run: npm ci
      - run: gauge run specs/ --env staging
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: gauge-report
          path: reports/
```

---

## Project Structure Patterns

### Cucumber / SpecFlow / Behave (Gherkin-based)

```
project/
  features/
    user-registration.feature
    checkout.feature
    step-definitions/          # or step_definitions/ or StepDefinitions/
      registration.steps.js    # JS
      RegistrationSteps.cs     # C#
      registration_steps.py    # Python
    support/
      world.js                 # JS — World/context setup
      hooks.js                 # JS — Before/After hooks
    environment.py             # Python — Behave hooks
  cucumber.js                  # Cucumber.js config
  reqnroll.json                # Reqnroll config
```

### Gauge

```
project/
  specs/
    user-registration.spec
    checkout.spec
  concepts/
    register-user.cpt
    login.cpt
  tests/
    step_implementations/
      registration.js
      checkout.js
  env/
    default/
      default.properties
    staging/
      staging.properties
```

---

## Best Practices

### Specification Writing
- Write specifications before code — they are requirements, not afterthoughts.
- Use concrete examples with real data, not abstract placeholders.
- Keep scenarios independent — each scenario should set up its own state (Background for shared setup).
- Limit scenarios to 3-8 steps; if longer, consider splitting or using higher-level steps.
- Use Scenario Outlines / data tables for testing multiple input variations of the same behavior.
- Write specifications in domain language, not UI implementation language ("I register an account" not "I fill in #field-23").

### Step Definitions
- Keep step definitions thin — delegate to page objects, API clients, or service layers.
- Reuse step definitions across features; avoid duplicating similar steps.
- Use parameterized steps with Cucumber Expressions or regex for flexible matching.
- Use hooks (Before/After) for setup and teardown, not step definitions.

### BDD Workflow
- Hold Three Amigos sessions (business, dev, QA) before writing specifications.
- Use Example Mapping to discover acceptance criteria, rules, and edge cases.
- Treat feature files as living documentation — keep them up to date with the codebase.
- Generate HTML reports for stakeholder review (Cucumber HTML, Gauge HTML Report, SpecFlow+ LivingDoc).

### Automation
- Run acceptance tests in CI on every PR for critical flows.
- Use dedicated test environments with seeded data for reliable execution.
- Tag scenarios (@smoke, @regression, @wip) to run subsets in different pipeline stages.
- Parallelize scenario execution where frameworks support it (Reqnroll, Cucumber with parallel profiles).
- Separate fast API-level acceptance tests from slow browser-level acceptance tests.

### Anti-Patterns to Avoid
- **Incidental details** — Don't include UI selectors or technical steps in feature files.
- **Imperative style** — Prefer declarative steps ("I register an account") over imperative steps ("I type 'Jane' into the name field, then I type...").
- **Coupled scenarios** — Don't rely on scenario execution order; each scenario must be independent.
- **Testing implementation** — Test business behavior, not internal code structure.
- **Too many scenarios** — If a feature has 50+ scenarios, the feature is too broad; split it.
