---
name: frappe-testing-unit
description: >
  Use when writing unit tests, integration tests, creating test fixtures, or running tests with bench run-tests.
  Prevents flaky tests from missing fixtures, incorrect test isolation, and wrong test base classes.
  Covers frappe.tests.utils, IntegrationTestCase, UnitTestCase, test fixtures, bench run-tests flags, test naming conventions.
  Keywords: unit test, integration test, IntegrationTestCase, fixtures, bench run-tests, frappe.tests, test_*.py.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
metadata:
  author: OpenAEC-Foundation
  version: "2.0"
---

# Unit & Integration Testing

## Quick Reference

| Task | Command / Class |
|------|----------------|
| Run all tests | `bench --site test_site run-tests` |
| Run tests for app | `bench --site test_site run-tests --app myapp` |
| Run tests for doctype | `bench --site test_site run-tests --doctype "Sales Order"` |
| Run single test method | `bench --site test_site run-tests --doctype "Sales Order" --test test_submit` |
| Run tests for module | `bench --site test_site run-tests --module "myapp.mymodule.doctype.mydt.test_mydt"` |
| Run with profiler | `bench --site test_site run-tests --doctype "Task" --profile` |
| Run with failfast | `bench --site test_site run-tests --failfast` |
| Generate JUnit XML | `bench --site test_site run-tests --junit-xml-output /path/report.xml` |
| Skip fixture loading | `bench --site test_site run-tests --skip-test-records --skip-before-tests` |
| Base class (v14) | `from frappe.tests.utils import FrappeTestCase` |
| Unit test class (v15+) | `from frappe.tests.classes import UnitTestCase` |
| Integration test class (v15+) | `from frappe.tests.classes import IntegrationTestCase` |

## Decision Tree: Which Test Base Class?

```
Need to test a function or method in isolation?
├─ YES → Does it require database access?
│   ├─ NO → UnitTestCase (v15+) or FrappeTestCase (v14)
│   └─ YES → IntegrationTestCase (v15+) or FrappeTestCase (v14)
└─ NO → Need to test document lifecycle (create/submit/cancel)?
    ├─ YES → IntegrationTestCase (v15+) or FrappeTestCase (v14)
    └─ NO → Need to test permissions or user context?
        ├─ YES → IntegrationTestCase (v15+) or FrappeTestCase (v14)
        └─ NO → UnitTestCase (v15+) or FrappeTestCase (v14)
```

**Version note**: In v14, `FrappeTestCase` is the ONLY base class. In v15+, it still works (deprecated wrapper) but ALWAYS prefer `UnitTestCase` or `IntegrationTestCase` for new code.

## Test Base Classes

### FrappeTestCase (v14 — still works in v15+ as compatibility wrapper)

```python
from frappe.tests.utils import FrappeTestCase

class TestMyDoctype(FrappeTestCase):
    def test_something(self):
        doc = frappe.get_doc({"doctype": "My Doctype", "field": "value"})
        doc.insert()
        self.assertEqual(doc.field, "value")
```

**Behavior**: Resets `frappe.local.flags` after each test. Database transactions start before each test and rollback afterward. ALWAYS call `super().setUpClass()` if you override `setUpClass`.

### UnitTestCase (v15+) — No Database Access

```python
from frappe.tests.classes import UnitTestCase

class TestMyUtils(UnitTestCase):
    def test_calculation(self):
        result = my_calculation(10, 20)
        self.assertEqual(result, 30)

    def test_html_output(self):
        html = generate_html()
        self.assertEqual(self.normalize_html(html), self.normalize_html(expected))
```

**Behavior**: Sets `frappe.set_user("Administrator")` in `setUpClass`. Auto-detects doctype from module path. Provides `normalize_html()`, `normalize_sql()`, `assertDocumentEqual()`, `assertQueryEqual()`, `assertSequenceSubset()`.

### IntegrationTestCase (v15+) — Full Database Access

```python
from frappe.tests.classes import IntegrationTestCase

class TestSalesOrder(IntegrationTestCase):
    def test_submit_order(self):
        so = frappe.get_doc({
            "doctype": "Sales Order",
            "customer": "_Test Customer",
            "items": [{"item_code": "_Test Item", "qty": 1, "rate": 100}]
        }).insert()
        so.submit()
        self.assertEqual(so.docstatus, 1)
```

**Behavior**: Extends `UnitTestCase`. Calls `frappe.init()` and sets up site connection. Loads test record dependencies via `make_test_records()`. Provides `primary_connection()` and `secondary_connection()` context managers. `maxDiff = 10_000`.

## Test File Structure

ALWAYS place test files in the doctype directory following this naming convention:

```
myapp/
└── mymodule/
    └── doctype/
        └── my_doctype/
            ├── my_doctype.py          # DocType controller
            ├── my_doctype.json        # DocType definition
            ├── test_my_doctype.py     # Test file (MUST start with test_)
            └── test_records.json      # Optional: test fixtures
```

**Rules**:
- ALWAYS prefix test files with `test_` — the test runner ignores files without this prefix
- ALWAYS use `test_{doctype_in_snake_case}.py` for doctype tests
- NEVER place test files outside the doctype directory for doctype-specific tests
- Non-doctype tests can live in any module, but MUST follow the `test_*.py` naming

## Test Fixtures

### Method 1: test_records.json (Static Fixtures)

Create a `test_records.json` file in the doctype directory:

```json
[
    {
        "doctype": "My Doctype",
        "field1": "_Test Value 1",
        "field2": 100
    },
    {
        "doctype": "My Doctype",
        "field1": "_Test Value 2",
        "field2": 200
    }
]
```

**Rules**:
- ALWAYS prefix test data values with `_Test` to distinguish from production data
- The test runner auto-loads these before running tests for the doctype
- Link field dependencies are resolved automatically — the runner builds records for linked DocTypes first

### Method 2: _test_records List (In-Module Fixtures)

```python
_test_records = [
    {"doctype": "My Doctype", "field1": "_Test Value 1"},
    {"doctype": "My Doctype", "field1": "_Test Value 2"},
]
```

### Method 3: Programmatic Fixtures (Recommended for Complex Data)

```python
def create_test_data():
    if frappe.flags.test_data_created:
        return
    frappe.set_user("Administrator")
    frappe.get_doc({
        "doctype": "My Doctype",
        "field1": "_Test Value",
    }).insert()
    frappe.flags.test_data_created = True

class TestMyDoctype(IntegrationTestCase):
    def setUp(self):
        create_test_data()
```

ALWAYS use `frappe.flags` to prevent duplicate fixture creation across test methods.

## Testing Patterns

### Testing Document Lifecycle

```python
class TestInvoice(IntegrationTestCase):
    def test_full_lifecycle(self):
        # Create
        doc = frappe.get_doc({"doctype": "Sales Invoice", ...}).insert()
        self.assertEqual(doc.docstatus, 0)  # Draft

        # Submit
        doc.submit()
        self.assertEqual(doc.docstatus, 1)  # Submitted

        # Cancel
        doc.cancel()
        self.assertEqual(doc.docstatus, 2)  # Cancelled
```

### Testing Permissions

```python
class TestPermissions(IntegrationTestCase):
    def test_user_cannot_read_private(self):
        frappe.set_user("test1@example.com")
        doc = frappe.get_doc("Event", {"subject": "_Test Private Event"})
        self.assertFalse(frappe.has_permission("Event", doc=doc))

    def tearDown(self):
        # ALWAYS reset user in tearDown
        frappe.set_user("Administrator")
```

### Testing with User Context (v15+ Context Manager)

```python
class TestAccess(IntegrationTestCase):
    def test_restricted_access(self):
        with self.set_user("test1@example.com"):
            self.assertRaises(
                frappe.PermissionError,
                frappe.get_doc, "Salary Slip", "SAL-001"
            )
        # User automatically restored after context manager exits
```

### Testing Whitelisted Methods

```python
class TestAPI(IntegrationTestCase):
    def test_whitelisted_method(self):
        frappe.set_user("test1@example.com")
        result = frappe.call("myapp.api.get_dashboard_data", filters={})
        self.assertIsInstance(result, dict)
        self.assertIn("total", result)
```

### Mocking External Services

```python
from unittest.mock import patch, MagicMock

class TestIntegration(IntegrationTestCase):
    @patch("myapp.integrations.stripe.requests.post")
    def test_payment_gateway(self, mock_post):
        mock_post.return_value = MagicMock(
            status_code=200,
            json=lambda: {"status": "success", "id": "ch_123"}
        )
        result = process_payment(amount=1000, currency="USD")
        self.assertEqual(result["status"], "success")
        mock_post.assert_called_once()
```

### Testing with Settings Changes

```python
class TestFeature(IntegrationTestCase):
    def test_with_modified_settings(self):
        with self.change_settings("Selling Settings", {"so_required": 1}):
            # Settings temporarily changed
            self.assertRaises(frappe.ValidationError, create_delivery_note)
        # Settings automatically reverted
```

### Testing with Hook Overrides

```python
class TestHooks(IntegrationTestCase):
    def test_custom_hook(self):
        with self.patch_hooks({"on_submit": ["myapp.hooks.custom_on_submit"]}):
            doc = create_and_submit_doc()
            # Verify hook was executed
```

## Context Managers Reference

| Context Manager | Available On | Purpose |
|----------------|-------------|---------|
| `set_user(user)` | UnitTestCase, IntegrationTestCase | Temporarily switch user context |
| `change_settings(dt, **kw)` | UnitTestCase, IntegrationTestCase | Temporarily modify settings |
| `patch_hooks(overrides)` | UnitTestCase, IntegrationTestCase | Temporarily override hooks |
| `freeze_time(time)` | UnitTestCase, IntegrationTestCase | Freeze time for deterministic tests |
| `debug_on(*exceptions)` | UnitTestCase, IntegrationTestCase | Drop into debugger on exception |
| `timeout(seconds)` | Decorator | Fail test if it exceeds time limit |
| `enable_safe_exec()` | IntegrationTestCase | Enable server scripts temporarily |
| `switch_site(site)` | IntegrationTestCase | Switch to a different site |
| `assertQueryCount(n)` | IntegrationTestCase | Assert exact SQL query count |
| `assertRedisCallCounts(**kw)` | IntegrationTestCase | Assert Redis command counts |
| `assertRowsRead(n)` | IntegrationTestCase | Assert row-level DB access limits |

## Database State Management

- **IntegrationTestCase**: ALWAYS rolls back database after each test — no cleanup needed
- **UnitTestCase**: No database connection — NEVER use `frappe.db` calls
- Each test gets a clean state: transactions start in `setUp` and rollback in `tearDown`
- NEVER call `frappe.db.commit()` in tests — this breaks test isolation
- Use `frappe.flags.in_test` to check if code is running under the test runner

## Detecting Test Mode

```python
if frappe.flags.in_test:
    # Skip external API calls, emails, etc.
    return mock_response()
```

NEVER use `frappe.flags.in_test` to skip validation logic — tests MUST exercise the same code paths as production.

## Common Pitfalls

1. **NEVER forget `super().setUpClass()`** — omitting this breaks fixture loading and user setup
2. **NEVER call `frappe.db.commit()`** in tests — this persists data across tests and breaks isolation
3. **ALWAYS reset user in `tearDown`** if you called `frappe.set_user()` directly (v14 pattern)
4. **ALWAYS prefix test data with `_Test`** — makes cleanup and identification easy
5. **NEVER rely on test execution order** — each test MUST be independent
6. **ALWAYS use `frappe.flags`** to guard fixture creation — prevents duplicate inserts

## See Also

- [references/examples.md](references/examples.md) — Complete test examples
- [references/anti-patterns.md](references/anti-patterns.md) — Common mistakes and fixes
- [references/fixtures.md](references/fixtures.md) — Fixture patterns in depth
- [references/api-reference.md](references/api-reference.md) — Full API reference for test utilities
- [frappe-testing-cicd](../frappe-testing-cicd/) — CI/CD pipeline setup
