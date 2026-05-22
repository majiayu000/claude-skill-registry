---
name: testability
description: Testability assessment criteria for code review. Apply when evaluating code for dependency injection, global state, pure functions, and test seams.
user-invocable: false
---

# Testability Assessment

Evaluate whether code can be effectively unit tested in isolation.

## Quick Reference

| Factor | Question | Severity if problematic |
|--------|----------|------------------------|
| Dependency injection | Are deps passed in? | High |
| Global state | Is shared state avoided? | High |
| Pure functions | Is logic separated from I/O? | Medium |
| Time/randomness | Are these injectable? | Medium |
| File system | Can it be abstracted? | Medium |
| Seams | Can behavior be substituted? | Medium-High |
| Observability | Can you assert on outputs? | Medium |

## Quick Heuristic

If testing a function requires:
- **0 mocks**: Excellent testability (pure function)
- **1-2 mocks**: Good testability (clear dependencies)
- **3-5 mocks**: Concerning (might need refactoring)
- **6+ mocks**: Likely design problem (too many responsibilities)

---

## Dependency Injection

### Check: Are dependencies passed in or created internally?

```python
# HARD TO TEST: Creates its own dependencies
class OrderService:
    def __init__(self):
        self.db = PostgresDatabase()  # hardcoded
        self.emailer = SmtpEmailer()  # hardcoded
        self.payment = StripeClient(os.environ['STRIPE_KEY'])  # hardcoded + env

    def process(self, order):
        self.db.save(order)
        self.payment.charge(order.total)
        self.emailer.send(order.user.email, "Confirmed")

# Testing requires:
# - Real database or complex mocking of PostgresDatabase constructor
# - Real SMTP or mocking SmtpEmailer constructor
# - Real Stripe or mocking StripeClient + env vars

# TESTABLE: Dependencies injected
class OrderService:
    def __init__(self, db: Database, emailer: Emailer, payment: PaymentProcessor):
        self.db = db
        self.emailer = emailer
        self.payment = payment

    def process(self, order):
        self.db.save(order)
        self.payment.charge(order.total)
        self.emailer.send(order.user.email, "Confirmed")

# Testing:
def test_process_order():
    db = FakeDatabase()
    emailer = FakeEmailer()
    payment = FakePayment()
    service = OrderService(db, emailer, payment)

    service.process(order)

    assert db.saved == [order]
    assert payment.charged == order.total
```

### Flag as:
- **High** if external services (DB, HTTP, files) created internally
- **Medium** if configuration created internally
- **Low** if only simple value objects created internally

---

## Global State

### Check: Does the code read from or write to global/module state?

```python
# HARD TO TEST: Global state
_cache = {}  # module-level
_current_user = None  # module-level

def get_cached_user(user_id):
    if user_id in _cache:
        return _cache[user_id]
    user = fetch_user(user_id)
    _cache[user_id] = user
    return user

def do_action():
    if _current_user.is_admin:  # where does this come from?
        ...

# Problems:
# - Tests pollute each other via shared _cache
# - Must set _current_user before testing do_action()
# - Order of test execution matters

# TESTABLE: Explicit state
class UserCache:
    def __init__(self, fetcher: UserFetcher):
        self._cache = {}
        self._fetcher = fetcher

    def get(self, user_id):
        if user_id not in self._cache:
            self._cache[user_id] = self._fetcher.fetch(user_id)
        return self._cache[user_id]

def do_action(user: User):  # explicit parameter
    if user.is_admin:
        ...
```

### Flag as:
- **High** if global state affects function behavior
- **Medium** if global state is read-only configuration
- **Low** if global state is truly constant (e.g., `PI = 3.14159`)

---

## Pure Functions vs Side Effects

### Check: Are side effects separated from logic?

```python
# HARD TO TEST: Logic and I/O mixed
def process_report(report_id):
    report = db.get(report_id)  # I/O

    # Business logic buried with I/O
    total = sum(item.amount for item in report.items)
    tax = total * 0.1 if report.taxable else 0
    final = total + tax

    report.final_amount = final
    db.save(report)  # I/O

    if final > 10000:
        emailer.send_alert(report)  # I/O

    return final

# Testing requires mocking db and emailer just to test calculation logic

# TESTABLE: Separate pure logic from I/O
def calculate_report_total(items: list[Item], taxable: bool) -> tuple[float, float]:
    """Pure function - easy to test"""
    total = sum(item.amount for item in items)
    tax = total * 0.1 if taxable else 0
    return total, tax

def process_report(report_id):
    """Orchestration - harder to test, but logic is simple"""
    report = db.get(report_id)
    total, tax = calculate_report_total(report.items, report.taxable)
    report.final_amount = total + tax
    db.save(report)
    if report.final_amount > 10000:
        emailer.send_alert(report)
    return report.final_amount

# Now calculation logic can be tested without any mocks:
def test_calculate_report_total():
    items = [Item(amount=100), Item(amount=200)]
    total, tax = calculate_report_total(items, taxable=True)
    assert total == 300
    assert tax == 30
```

### Flag as:
- **Medium** if business logic is tangled with I/O
- **Low** if I/O is clearly separated but could be cleaner

---

## Time and Randomness

### Check: Are non-deterministic operations injectable?

```python
# HARD TO TEST: Hardcoded time
def is_expired(token):
    return token.expires_at < datetime.now()  # changes every call!

def create_token(user):
    return Token(
        user_id=user.id,
        created_at=datetime.now(),
        token=secrets.token_hex(32)  # random!
    )

# Tests are flaky or require freezegun/time mocking

# TESTABLE: Inject time and randomness
def is_expired(token, now: datetime = None):
    now = now or datetime.now()
    return token.expires_at < now

def create_token(user, now: datetime = None, token_generator=secrets.token_hex):
    return Token(
        user_id=user.id,
        created_at=now or datetime.now(),
        token=token_generator(32)
    )

# Tests are deterministic:
def test_is_expired():
    fixed_now = datetime(2024, 1, 15, 12, 0, 0)
    expired_token = Token(expires_at=datetime(2024, 1, 14))
    assert is_expired(expired_token, now=fixed_now)

def test_create_token():
    fixed_now = datetime(2024, 1, 15)
    token = create_token(user, now=fixed_now, token_generator=lambda n: "abc123")
    assert token.created_at == fixed_now
    assert token.token == "abc123"
```

### Flag as:
- **Medium** if time/random makes tests flaky or requires complex mocking
- **Low** if non-determinism is in test-unimportant code paths

---

## File System Access

### Check: Can file operations be abstracted?

```python
# HARD TO TEST: Direct file system access
def process_uploads(upload_dir):
    for filename in os.listdir(upload_dir):
        path = os.path.join(upload_dir, filename)
        with open(path) as f:
            content = f.read()
        result = transform(content)
        output_path = path + '.processed'
        with open(output_path, 'w') as f:
            f.write(result)

# Tests require actual files, temp directories, cleanup

# TESTABLE: Abstract file operations
from typing import Protocol

class FileSystem(Protocol):
    def list_files(self, directory: str) -> list[str]: ...
    def read(self, path: str) -> str: ...
    def write(self, path: str, content: str) -> None: ...

class RealFileSystem:
    def list_files(self, directory): return os.listdir(directory)
    def read(self, path): return Path(path).read_text()
    def write(self, path, content): Path(path).write_text(content)

class FakeFileSystem:
    def __init__(self):
        self.files = {}
    def list_files(self, directory): return list(self.files.keys())
    def read(self, path): return self.files[path]
    def write(self, path, content): self.files[path] = content

def process_uploads(upload_dir: str, fs: FileSystem):
    for filename in fs.list_files(upload_dir):
        content = fs.read(f"{upload_dir}/{filename}")
        result = transform(content)
        fs.write(f"{upload_dir}/{filename}.processed", result)
```

### Flag as:
- **Medium** if file operations are core to the functionality
- **Low** if file access is peripheral (e.g., config loading at startup)

---

## Test Seams

### Check: Are there clear points to substitute test doubles?

A **seam** is a place where you can alter behavior without editing the code.

```python
# FEW SEAMS: Everything hardwired
def send_notification(user_id, message):
    user = User.objects.get(id=user_id)  # Django ORM hardwired
    if user.preferences.email_enabled:
        smtp = smtplib.SMTP('mail.server.com')  # hardwired
        smtp.send(user.email, message)
    if user.preferences.sms_enabled:
        twilio = TwilioClient(os.environ['TWILIO_KEY'])  # hardwired
        twilio.send(user.phone, message)

# MANY SEAMS: Substitutable at multiple points
def send_notification(
    user: User,  # pass in, don't fetch
    message: str,
    email_sender: EmailSender,  # injectable
    sms_sender: SmsSender,  # injectable
):
    if user.preferences.email_enabled:
        email_sender.send(user.email, message)
    if user.preferences.sms_enabled:
        sms_sender.send(user.phone, message)
```

### Flag as:
- **High** if critical code paths have no seams
- **Medium** if some seams exist but major ones are missing

---

## Assertions and Observability

### Check: Is it clear what to assert in tests?

```python
# HARD TO OBSERVE: Side effects with no return/state to check
def process(item):
    # does stuff...
    # returns nothing
    # changes no observable state
    pass

# How do you test this? Mock everything and verify calls?

# OBSERVABLE: Clear outputs to assert
def process(item) -> ProcessResult:
    # does stuff...
    return ProcessResult(
        success=True,
        changes_made=["updated X", "created Y"],
        warnings=[]
    )

# Easy to test:
def test_process():
    result = process(item)
    assert result.success
    assert "updated X" in result.changes_made
```

### Flag as:
- **Medium** if testing requires verifying mock interactions instead of outputs
- **Low** if outputs exist but could be richer
