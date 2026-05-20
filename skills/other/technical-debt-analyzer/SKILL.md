---
name: technical-debt-analyzer
description: Detect and analyze areas with high maintenance cost, poor design, or accumulated technical debt. Use this skill when reviewing codebases for quality issues, planning refactoring efforts, conducting code audits, assessing project health, identifying maintenance hotspots, or prioritizing technical improvements. Analyzes code smells, architectural issues, dependency problems, test quality, documentation gaps, and provides actionable recommendations with priority rankings.
---

# Technical Debt Analyzer

Systematically identify, categorize, and prioritize technical debt across codebases. Provides actionable insights into code quality, architectural issues, and maintenance risks.

## Core Capabilities

### 1. Code Quality Analysis

Identify code-level technical debt:
- **Code smells** - Long methods, large classes, duplicated code
- **Complexity metrics** - Cyclomatic complexity, nesting depth
- **Naming issues** - Poor variable/function names, inconsistent conventions
- **Dead code** - Unused functions, unreachable code, commented code
- **Magic numbers** - Hard-coded values without explanation
- **Anti-patterns** - Common design mistakes and bad practices

### 2. Architectural Debt

Detect structural and design issues:
- **Tight coupling** - Excessive dependencies between modules
- **Missing abstractions** - Duplicated logic that should be extracted
- **Layer violations** - Breaking architectural boundaries
- **God objects** - Classes/modules with too many responsibilities
- **Circular dependencies** - Modules depending on each other
- **Inconsistent patterns** - Mixed architectural styles

### 3. Maintenance Risk Assessment

Identify high-maintenance areas:
- **Change frequency** - Files modified frequently (hotspots)
- **Bug density** - Areas with recurring bugs
- **Test coverage gaps** - Critical code without tests
- **Complexity + change** - Complex code that changes often (highest risk)
- **Knowledge concentration** - Code only one person understands
- **Outdated dependencies** - Old libraries with security issues

### 4. Documentation Debt

Find documentation gaps:
- **Missing documentation** - Undocumented public APIs
- **Outdated comments** - Comments contradicting code
- **Poor commit messages** - Unclear change history
- **Incomplete README** - Setup/usage not documented
- **Missing architecture docs** - No design documentation

### 5. Test Debt

Assess test quality issues:
- **Low coverage** - Critical paths untested
- **Flaky tests** - Tests that fail intermittently
- **Slow tests** - Tests that slow down CI/CD
- **Test duplication** - Redundant test logic
- **Missing test types** - No integration/E2E tests
- **Brittle tests** - Tests that break with minor changes

## Technical Debt Analysis Workflow

### Step 1: Scan the Codebase

Gather evidence of technical debt:

**Examine file structure:**
```
# Look for:
- Large files (>500 lines)
- Deep nesting (>5 levels)
- Many files in single directory
- Inconsistent naming patterns
```

**Analyze code metrics:**
- Lines of code per file/function
- Cyclomatic complexity
- Code duplication percentage
- Dependency count
- Test coverage percentage

**Review version control:**
```bash
# Find frequently changed files (hotspots)
git log --format=format: --name-only | grep -v '^$' | sort | uniq -c | sort -rn | head -20

# Find files with many authors (knowledge spread)
git log --format='%an' --name-only | grep -v '^$' | sort | uniq -c

# Find large commits (risky changes)
git log --all --numstat --format="%H" | awk '
```

### Step 2: Categorize Technical Debt

Classify findings into debt categories:

**Code-level debt:**
```python
# Example: Long method
def process_order(order):  # 150 lines!
    # Validation
    # Price calculation
    # Inventory check
    # Payment processing
    # Email notification
    # Logging
    # Analytics
    # ...

# Debt: Violates Single Responsibility Principle
# Impact: Hard to test, modify, understand
# Priority: Medium
```

**Architectural debt:**
```python
# Example: Tight coupling
from payment_processor import PaymentProcessor
from email_service import EmailService
from analytics import Analytics

class OrderService:
    def __init__(self):
        self.payment = PaymentProcessor()  # Direct dependency
        self.email = EmailService()        # Direct dependency
        self.analytics = Analytics()        # Direct dependency

# Debt: No dependency injection, hard to test
# Impact: Cannot mock dependencies, tightly coupled
# Priority: High
```

**Test debt:**
```python
# Example: No tests for critical function
def calculate_refund(order, reason):
    # Complex refund logic...
    # No tests exist!

# Debt: Critical business logic untested
# Impact: High risk of bugs in refunds
# Priority: Critical
```

### Step 3: Assess Impact and Priority

Rank technical debt by impact:

**Priority scoring factors:**
1. **Business criticality** - How important is this code?
2. **Change frequency** - How often does it change?
3. **Current quality** - How bad is it?
4. **Risk level** - What could go wrong?
5. **Effort to fix** - How hard to improve?

**Priority matrix:**
```
High Impact + Low Effort = Critical (fix first)
High Impact + High Effort = Important (plan carefully)
Low Impact + Low Effort = Nice-to-have (quick wins)
Low Impact + High Effort = Defer (don't bother)
```

**Example scoring:**
```
Technical Debt: Missing error handling in payment processing
- Business criticality: 10/10 (payments are critical)
- Change frequency: 8/10 (changes often)
- Current quality: 3/10 (poor)
- Risk level: 10/10 (could lose money)
- Effort to fix: 4/10 (moderate)

Overall Priority: CRITICAL
Recommended action: Fix immediately
```

### Step 4: Generate Recommendations

Provide specific, actionable fixes:

**Format:**
```markdown
## Technical Debt Item: [Name]

**Category:** [Code Quality/Architecture/Test/Documentation]
**Location:** [file:line or component]
**Severity:** [Critical/High/Medium/Low]
**Effort:** [Hours or Days estimate]

### Problem
[Clear description of the issue]

### Impact
[Why this matters - business/technical impact]

### Recommendation
[Specific steps to fix]

### Example Fix
[Code example if applicable]

### Benefits
[What improves after fixing]
```

**Example:**
```markdown
## Technical Debt Item: God Class in OrderService

**Category:** Architectural Debt
**Location:** src/services/OrderService.java
**Severity:** High
**Effort:** 2-3 days

### Problem
OrderService class has 1,200 lines and handles 15 different responsibilities:
validation, pricing, inventory, payment, shipping, notifications, analytics,
logging, caching, etc.

### Impact
- Hard to test (requires mocking 15 dependencies)
- Changes risky (touches many concerns)
- Team bottleneck (everyone modifies this file)
- Poor reusability (can't use parts independently)

### Recommendation
1. Extract responsibilities into separate services:
   - ValidationService
   - PricingService
   - InventoryService
   - PaymentService
   - NotificationService

2. Use dependency injection for loose coupling

3. Introduce OrderOrchestrator to coordinate services

### Example Fix
```java
// Before: God class
class OrderService {
    void processOrder() {
        validate();
        calculatePrice();
        checkInventory();
        processPayment();
        sendEmail();
        logAnalytics();
        // ...
    }
}

// After: Separated concerns
class OrderOrchestrator {
    private ValidationService validator;
    private PricingService pricer;
    private PaymentService payment;

    OrderOrchestrator(ValidationService v, PricingService p, PaymentService pm) {
        this.validator = v;
        this.pricer = p;
        this.payment = pm;
    }

    void processOrder(Order order) {
        validator.validate(order);
        Price price = pricer.calculate(order);
        payment.process(order, price);
    }
}
```

### Benefits
- Each service independently testable
- Clear separation of concerns
- Easier to maintain and extend
- Better code reuse
- Parallel development possible
```

### Step 5: Create Action Plan

Prioritize and sequence fixes:

**Suggested format:**
```
## Technical Debt Remediation Plan

### Immediate Actions (This Sprint)
1. [Critical item 1] - [effort estimate]
2. [Critical item 2] - [effort estimate]

### Short Term (Next 1-2 Months)
1. [High priority item 1]
2. [High priority item 2]

### Long Term (3-6 Months)
1. [Strategic improvements]
2. [Architectural changes]

### Quick Wins (Can do anytime)
1. [Low effort improvements]

### Monitoring
- Track technical debt metrics monthly
- Review hotspots after each release
- Code review checklist to prevent new debt
```

## Technical Debt Patterns

### Pattern 1: Code Smell - Long Method

**Detection:**
```python
# File: order_processor.py
def process_order(order_id):  # 250 lines long!
    # Get order from database
    order = db.query(f"SELECT * FROM orders WHERE id = {order_id}")

    # Validate customer
    if not order.customer_id:
        raise ValueError("No customer")
    customer = db.query(f"SELECT * FROM customers WHERE id = {order.customer_id}")

    # Check inventory for each item
    for item in order.items:
        inventory = db.query(f"SELECT * FROM inventory WHERE sku = {item.sku}")
        if inventory.quantity < item.quantity:
            # Send email to supplier
            # Log shortage
            # Update backorder
            # ...

    # Calculate pricing with discounts
    # Process payment
    # Update inventory
    # Send confirmation email
    # Update analytics
    # ... (200+ more lines)
```

**Analysis:**
```
Category: Code Quality Debt
Severity: Medium
Issues:
- 250 lines in single function
- Multiple responsibilities (SRP violation)
- High cyclomatic complexity (15+)
- Hard to test
- SQL injection vulnerability
- Poor error handling
```

**Recommendation:**
```python
# Extract into smaller, focused functions

def process_order(order_id):
    """Main orchestration - now only 20 lines."""
    order = get_order(order_id)
    validate_order(order)
    check_inventory(order)
    price = calculate_total(order)
    process_payment(order, price)
    fulfill_order(order)
    send_confirmation(order)
    return order

def get_order(order_id):
    """Single responsibility: fetch order."""
    return Order.query.get(order_id)

def validate_order(order):
    """Single responsibility: validation."""
    if not order.customer_id:
        raise ValidationError("Order has no customer")
    if not order.items:
        raise ValidationError("Order has no items")

def check_inventory(order):
    """Single responsibility: inventory check."""
    for item in order.items:
        inventory = Inventory.query.filter_by(sku=item.sku).first()
        if inventory.quantity < item.quantity:
            handle_shortage(item, inventory)
```

**Benefits:**
- Each function testable in isolation
- Clear single responsibility
- Easier to understand and modify
- Better error handling
- Reusable components

### Pattern 2: Architectural Debt - Circular Dependency

**Detection:**
```python
# services/order_service.py
from services.customer_service import CustomerService

class OrderService:
    def get_customer_orders(self, customer_id):
        customer = CustomerService().get_customer(customer_id)
        return self.filter_by_customer(customer)

# services/customer_service.py
from services.order_service import OrderService

class CustomerService:
    def get_customer_with_orders(self, customer_id):
        orders = OrderService().get_orders_by_customer(customer_id)
        customer = self.get_customer(customer_id)
        customer.orders = orders
        return customer
```

**Analysis:**
```
Category: Architectural Debt
Severity: High
Issues:
- Circular dependency (OrderService ↔ CustomerService)
- Import errors possible
- Hard to test in isolation
- Tight coupling
- Poor separation of concerns
```

**Recommendation:**
```python
# Option 1: Introduce repository pattern
# repositories/order_repository.py
class OrderRepository:
    def get_by_customer(self, customer_id):
        return Order.query.filter_by(customer_id=customer_id).all()

# services/customer_service.py
from repositories.order_repository import OrderRepository

class CustomerService:
    def __init__(self, order_repo):
        self.order_repo = order_repo

    def get_customer_with_orders(self, customer_id):
        customer = self.get_customer(customer_id)
        customer.orders = self.order_repo.get_by_customer(customer_id)
        return customer

# Option 2: Use dependency injection
# Break the cycle by injecting dependencies
class CustomerService:
    def __init__(self, order_service=None):
        self.order_service = order_service

    def get_customer_with_orders(self, customer_id):
        if self.order_service:
            orders = self.order_service.get_orders(customer_id)
        else:
            orders = []
        # ...
```

**Benefits:**
- No circular dependencies
- Services testable independently
- Clear dependency direction
- Easier to understand flow

### Pattern 3: Test Debt - Missing Critical Tests

**Detection:**
```python
# payment_processor.py - NO TESTS!
def process_refund(order, amount, reason):
    """Process refund to customer's payment method."""
    if amount > order.total:
        # What happens here? Not tested!
        pass

    payment_method = get_payment_method(order.payment_id)

    if payment_method.type == "credit_card":
        result = refund_to_card(payment_method, amount)
    elif payment_method.type == "paypal":
        result = refund_to_paypal(payment_method, amount)
    else:
        # Edge case - not tested!
        result = manual_refund_process(payment_method, amount)

    # What if refund fails? Not tested!
    return result
```

**Analysis:**
```
Category: Test Debt
Severity: Critical
Issues:
- No tests for critical payment function
- Multiple edge cases untested
- Error handling not verified
- Business logic unvalidated
- High risk of bugs
Coverage: 0%
```

**Recommendation:**
```python
# Add comprehensive test suite
def test_process_refund_success():
    """Test successful refund."""
    order = create_test_order(total=100)
    result = process_refund(order, 50, "Customer request")
    assert result.success is True
    assert result.amount == 50

def test_process_refund_exceeds_total():
    """Test that refund cannot exceed order total."""
    order = create_test_order(total=100)
    with pytest.raises(ValueError, match="exceeds order total"):
        process_refund(order, 150, "Invalid amount")

def test_process_refund_credit_card():
    """Test refund to credit card."""
    order = create_test_order(payment_type="credit_card")
    result = process_refund(order, 50, "Test")
    assert result.method == "credit_card"

def test_process_refund_paypal():
    """Test refund to PayPal."""
    order = create_test_order(payment_type="paypal")
    result = process_refund(order, 50, "Test")
    assert result.method == "paypal"

def test_process_refund_unknown_payment_type():
    """Test handling of unknown payment type."""
    order = create_test_order(payment_type="bitcoin")
    result = process_refund(order, 50, "Test")
    assert result.requires_manual_processing is True

def test_process_refund_payment_failure():
    """Test handling of payment gateway failure."""
    order = create_test_order()
    with patch('payment_gateway.refund') as mock:
        mock.side_effect = PaymentGatewayError("Network error")
        with pytest.raises(RefundFailedError):
            process_refund(order, 50, "Test")
```

**Benefits:**
- Critical payment logic validated
- Edge cases covered
- Error handling verified
- Safer to modify/refactor
- Documentation through tests

### Pattern 4: Dependency Debt - Outdated Libraries

**Detection:**
```json
// package.json
{
  "dependencies": {
    "express": "3.21.2",        // Latest: 4.18.2 (security issues in 3.x)
    "lodash": "4.17.20",        // Latest: 4.17.21 (CVE-2020-8203)
    "moment": "2.24.0",         // Latest: 2.29.4 (deprecated, use day.js)
    "request": "2.88.0"         // Deprecated! Use axios or node-fetch
  }
}
```

**Analysis:**
```
Category: Maintenance Risk
Severity: High
Issues:
- 3 packages with known security vulnerabilities
- 1 deprecated package still in use
- Missing critical security patches
- Outdated major versions
- Technical debt accumulating
```

**Recommendation:**
```json
// Updated package.json
{
  "dependencies": {
    "express": "^4.18.2",       // Updated to latest
    "lodash": "^4.17.21",       // Security patch applied
    "dayjs": "^1.11.7",         // Replaced moment (lighter, maintained)
    "axios": "^1.3.0"           // Replaced deprecated request
  }
}

// Migration notes:
// 1. express 3→4: Update middleware syntax
// 2. moment→dayjs: Update date formatting calls
// 3. request→axios: Update HTTP client calls
// 4. lodash: No breaking changes, just update

// Estimated effort: 1-2 days
// Risk: Medium (requires testing)
// Priority: High (security vulnerabilities)
```

**Migration example:**
```javascript
// Before (deprecated request)
const request = require('request');
request('https://api.example.com', (error, response, body) => {
  console.log(body);
});

// After (axios)
const axios = require('axios');
const response = await axios.get('https://api.example.com');
console.log(response.data);
```

**Benefits:**
- Security vulnerabilities patched
- Access to new features
- Better performance (dayjs vs moment)
- Continued maintenance support

### Pattern 5: Documentation Debt - Undocumented API

**Detection:**
```python
# api/user_controller.py - No documentation!
@app.route('/api/users/<id>/settings', methods=['PUT'])
def update_user_settings(id):
    # What fields are accepted? Unknown!
    # What's the response format? Unknown!
    # What errors can occur? Unknown!
    data = request.json
    user = User.query.get(id)
    user.settings = data
    db.session.commit()
    return jsonify(user.to_dict())
```

**Analysis:**
```
Category: Documentation Debt
Severity: Medium
Issues:
- No API documentation
- Request/response format unclear
- Validation rules unknown
- Error handling undocumented
- Hard for other developers to use
```

**Recommendation:**
```python
@app.route('/api/users/<id>/settings', methods=['PUT'])
def update_user_settings(id):
    """
    Update user settings.

    Args:
        id (str): User ID

    Request Body:
        {
            "theme": "dark" | "light",
            "notifications": boolean,
            "language": str (ISO 639-1 code)
        }

    Returns:
        200 OK:
            {
                "id": str,
                "settings": {
                    "theme": str,
                    "notifications": bool,
                    "language": str
                }
            }

        404 Not Found:
            {"error": "User not found"}

        400 Bad Request:
            {"error": "Invalid theme value"}

    Example:
        PUT /api/users/123/settings
        {
            "theme": "dark",
            "notifications": true,
            "language": "en"
        }
    """
    try:
        data = request.json
        validate_settings(data)  # Validate input

        user = User.query.get_or_404(id)
        user.update_settings(data)
        db.session.commit()

        return jsonify({
            "id": user.id,
            "settings": user.settings
        }), 200

    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
```

**Benefits:**
- Clear API contract
- Easier for developers to use
- Self-documenting code
- Reduces support questions

### Pattern 6: Duplication Debt - Copy-Pasted Code

**Detection:**
```python
# analytics.py
def track_signup(user):
    event = {
        "type": "signup",
        "user_id": user.id,
        "timestamp": datetime.now(),
        "properties": {"email": user.email}
    }
    analytics_client.track(event)
    logger.info(f"Tracked signup: {user.id}")

# payments.py
def track_purchase(order):
    event = {
        "type": "purchase",
        "user_id": order.user_id,
        "timestamp": datetime.now(),
        "properties": {"amount": order.total}
    }
    analytics_client.track(event)
    logger.info(f"Tracked purchase: {order.id}")

# notifications.py
def track_notification(user, notification):
    event = {
        "type": "notification",
        "user_id": user.id,
        "timestamp": datetime.now(),
        "properties": {"message": notification.text}
    }
    analytics_client.track(event)
    logger.info(f"Tracked notification: {user.id}")
```

**Analysis:**
```
Category: Code Quality Debt
Severity: Medium
Issues:
- Same pattern duplicated 3+ times
- Violates DRY principle
- Hard to modify (must update all copies)
- Inconsistent implementations possible
- Maintenance burden
```

**Recommendation:**
```python
# Extract common pattern into reusable function
def track_event(event_type, user_id, properties=None):
    """
    Track analytics event.

    Args:
        event_type: Type of event (signup, purchase, etc.)
        user_id: User ID associated with event
        properties: Optional dict of event properties
    """
    event = {
        "type": event_type,
        "user_id": user_id,
        "timestamp": datetime.now(),
        "properties": properties or {}
    }
    analytics_client.track(event)
    logger.info(f"Tracked {event_type}: {user_id}")

# Now use the extracted function
def track_signup(user):
    track_event("signup", user.id, {"email": user.email})

def track_purchase(order):
    track_event("purchase", order.user_id, {"amount": order.total})

def track_notification(user, notification):
    track_event("notification", user.id, {"message": notification.text})
```

**Benefits:**
- Single source of truth
- Easier to maintain
- Consistent behavior
- Less code overall
- Easier to add features (e.g., add filtering to track_event)

## Code Quality Metrics

### Cyclomatic Complexity

Measure of code complexity based on decision points:

```
Complexity = edges - nodes + 2 * connected_components

Guidelines:
- 1-10: Simple, low risk
- 11-20: Moderate, medium risk
- 21-50: Complex, high risk
- 50+: Very complex, very high risk (refactor!)
```

**Example:**
```python
def calculate_discount(customer, order):  # Complexity: 8
    if customer.is_premium:        # +1
        if order.total > 1000:     # +1
            return 0.2
        else:                       # +1
            return 0.15
    elif customer.is_member:        # +1
        if order.total > 500:      # +1
            return 0.1
        else:                       # +1
            return 0.05
    else:                           # +1
        return 0
```

### Maintainability Index

Combined metric for maintainability:

```
MI = max(0, (171 - 5.2 * ln(HV) - 0.23 * CC - 16.2 * ln(LOC)) * 100 / 171)

Where:
- HV = Halstead Volume
- CC = Cyclomatic Complexity
- LOC = Lines of Code

Guidelines:
- 85-100: Highly maintainable
- 65-85: Moderately maintainable
- 0-65: Hard to maintain (technical debt!)
```

### Code Churn

Measure of code volatility:

```bash
# Files with highest churn (lines changed)
git log --all --numstat --format="%H" --since="3 months ago" | \
  awk '{if ($1 != "") files[$3] += $1 + $2} END {for (f in files) print files[f], f}' | \
  sort -rn | head -20
```

High churn + high complexity = **Highest maintenance risk**

## Technical Debt Report Template

```markdown
# Technical Debt Analysis Report

**Project:** [Project Name]
**Date:** [Analysis Date]
**Analyzed By:** [Name/Tool]

## Executive Summary

**Overall Debt Level:** [High/Medium/Low]
**Total Items:** [Count]
**Critical Items:** [Count]
**Estimated Effort:** [Days/Weeks]

### Key Findings
1. [Most critical issue]
2. [Second critical issue]
3. [Third critical issue]

### Recommendations
1. [Top priority action]
2. [Second priority action]
3. [Third priority action]

## Debt Inventory

### Critical Priority (Fix Immediately)

#### 1. [Debt Item Name]
- **Category:** [Code Quality/Architecture/Test/etc.]
- **Location:** [file:line or component]
- **Impact:** [Description of business/technical impact]
- **Effort:** [Estimate]
- **Recommendation:** [Specific fix]

#### 2. [Next critical item...]

### High Priority (Next Sprint)

[Same format as critical]

### Medium Priority (Next 1-2 Months)

[Same format]

### Low Priority (Nice-to-Have)

[Same format]

## Metrics Summary

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Test Coverage | 65% | 80% | ⚠️ Below target |
| Cyclomatic Complexity (avg) | 15 | <10 | ⚠️ Too high |
| Code Duplication | 12% | <5% | ⚠️ Too high |
| Outdated Dependencies | 8 | 0 | ⚠️ Action needed |
| Documentation Coverage | 40% | 80% | ⚠️ Insufficient |

## Hotspot Analysis

### Top 10 Maintenance Hotspots
(High complexity + High change frequency)

1. **src/services/OrderService.java** - Complexity: 45, Changes: 87
2. **src/controllers/UserController.py** - Complexity: 38, Changes: 62
3. [Continue...]

## Action Plan

### Phase 1: Immediate (This Sprint)
- [ ] Fix critical security vulnerability in payment processing
- [ ] Add tests for refund logic
- [ ] Update vulnerable dependencies

**Estimated Effort:** 3-5 days

### Phase 2: Short Term (Next 1-2 Months)
- [ ] Refactor OrderService god class
- [ ] Eliminate circular dependencies
- [ ] Improve test coverage to 80%

**Estimated Effort:** 2-3 weeks

### Phase 3: Long Term (3-6 Months)
- [ ] Architectural improvements
- [ ] Documentation overhaul
- [ ] Performance optimization

**Estimated Effort:** 1-2 months

## Appendix

### Tools Used
- [Static analysis tools]
- [Coverage tools]
- [Complexity analyzers]

### Analysis Scope
- [Directories analyzed]
- [Exclusions]
- [Time period for git analysis]
```

## Best Practices

1. **Regular analysis** - Run technical debt analysis quarterly or before major releases
2. **Automate detection** - Use static analysis tools in CI/CD pipeline
3. **Track metrics** - Monitor trends over time, not just point-in-time snapshots
4. **Prioritize ruthlessly** - Focus on high-impact, high-risk debt first
5. **Budget time** - Allocate 10-20% of each sprint to debt reduction
6. **Prevent new debt** - Code review checklist, quality gates, linting
7. **Measure progress** - Track debt reduction metrics over time
8. **Communicate impact** - Translate technical debt to business risk
9. **Balance with features** - Don't stop all feature work, but don't ignore debt
10. **Make it visible** - Dashboard showing debt trends, hotspots, and priorities

## Common Anti-Patterns

### Anti-Pattern 1: The "Rewrite" Trap

**Problem:**
"This code is terrible, let's rewrite it from scratch!"

**Why it fails:**
- Underestimates effort (Netscape effect)
- Loses institutional knowledge
- Introduces new bugs
- Takes longer than incremental improvement

**Better approach:**
- Incremental refactoring
- Strangler fig pattern
- Add tests first, then refactor
- Preserve working functionality

### Anti-Pattern 2: Perfection Paralysis

**Problem:**
"We can't ship until we fix all technical debt!"

**Why it fails:**
- Infinite task (debt never goes to zero)
- Delays value delivery
- Business loses patience
- Team burnout

**Better approach:**
- Fix critical debt, ship with minor debt
- Continuous improvement
- Pragmatic prioritization

### Anti-Pattern 3: Ignore and Hope

**Problem:**
"We'll fix it later when we have time."

**Why it fails:**
- Later never comes
- Debt compounds (gets worse over time)
- Eventually forces painful emergency fixes
- Team morale suffers

**Better approach:**
- Schedule debt reduction in every sprint
- Boy Scout rule (leave code better than found)
- Track debt trend (going up or down?)
