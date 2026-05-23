---
name: python-code-review
description: Python code review guidelines (security, performance, bugs, style). Auto-loads when reviewing Python code or analyzing code quality.
user-invocable: false
---

# Python Code Review Patterns

This skill provides Python-specific code review guidelines. Use alongside `python-style` for comprehensive review.

## Critical Security Issues

### SQL Injection

```python
# VULNERABLE - string formatting in queries
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
User.objects.raw(f"SELECT * FROM users WHERE name = '{name}'")

# SAFE - parameterized queries
cursor.execute("SELECT * FROM users WHERE id = %s", [user_id])
User.objects.raw("SELECT * FROM users WHERE name = %s", [name])
```

### Command Injection

```python
# VULNERABLE - unsanitized input in shell commands
os.system(f"grep {user_input} /var/log/app.log")
subprocess.run(f"convert {filename} output.png", shell=True)

# SAFE - use list arguments, avoid shell=True
subprocess.run(["grep", user_input, "/var/log/app.log"])
subprocess.run(["convert", filename, "output.png"], check=True)
```

### Path Traversal

```python
# VULNERABLE - user input directly in path
file_path = f"/uploads/{filename}"
with open(file_path) as f:
    return f.read()

# SAFE - validate and sanitize paths
from pathlib import Path
base_path = Path("/uploads").resolve()
file_path = (base_path / filename).resolve()
if not file_path.is_relative_to(base_path):
    raise ValueError("Invalid path")
```

### Hardcoded Secrets

Flag any of these patterns:
```python
# VULNERABLE
API_KEY = "sk-abc123..."
password = "admin123"
SECRET_KEY = "hardcoded-secret"

# SAFE - use environment variables
API_KEY = os.environ["API_KEY"]
password = os.environ.get("DB_PASSWORD")
```

## High Priority Logic Bugs

### Mutable Default Arguments

```python
# BUG - shared mutable default
def add_item(item, items=[]):
    items.append(item)
    return items

# CORRECT
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

### Exception Swallowing

```python
# BUG - silently swallowing errors
try:
    process_data()
except Exception:
    pass

# CORRECT - handle or re-raise
try:
    process_data()
except SpecificError as e:
    logger.warning("Processing failed: %s", e)
    raise
```

### Bare Except Clauses

```python
# BUG - catches KeyboardInterrupt, SystemExit
try:
    risky_operation()
except:
    handle_error()

# CORRECT - be specific
try:
    risky_operation()
except (ValueError, TypeError) as e:
    handle_error(e)
```

### Late Binding in Closures

```python
# BUG - all functions use i=9
funcs = [lambda: i for i in range(10)]
[f() for f in funcs]  # [9, 9, 9, ...]

# CORRECT - capture value
funcs = [lambda i=i: i for i in range(10)]
```

### Boolean Comparison Mistakes

```python
# BUG - wrong comparison
if items == []:  # Use: if not items
if result == None:  # Use: if result is None
if flag == True:  # Use: if flag

# CORRECT
if not items:
if result is None:
if flag:
```

## Performance Anti-Patterns

### N+1 Query Problem (Django)

```python
# SLOW - N+1 queries
for order in Order.objects.all():
    print(order.customer.name)  # Query per order

# FAST - prefetch related
for order in Order.objects.select_related('customer'):
    print(order.customer.name)  # Single query

# For many-to-many
orders = Order.objects.prefetch_related('items')
```

### Inefficient List Operations

```python
# SLOW - O(n) for each 'in' check
if item in large_list:
    pass

# FAST - O(1) lookup
item_set = set(large_list)
if item in item_set:
    pass

# SLOW - string concatenation in loop
result = ""
for s in strings:
    result += s  # Creates new string each time

# FAST - use join
result = "".join(strings)
```

### Blocking I/O in Async Code

```python
# SLOW - blocks event loop
async def fetch_data():
    response = requests.get(url)  # Blocking!
    return response.json()

# FAST - use async client
async def fetch_data():
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()
```

### Loading All Records into Memory

```python
# MEMORY ISSUE - loads all into memory
all_users = list(User.objects.all())
for user in all_users:
    process(user)

# CORRECT - use iterator
for user in User.objects.iterator():
    process(user)

# Or batch processing
from django.core.paginator import Paginator
paginator = Paginator(User.objects.all(), 1000)
for page in paginator.page_range:
    for user in paginator.page(page):
        process(user)
```

## Django-Specific Patterns

### Missing Database Indexes

```python
# Flag fields used in filters without db_index
class Order(models.Model):
    # If frequently filtered by status, needs index
    status = models.CharField(max_length=20)  # Missing: db_index=True
    created_at = models.DateTimeField()  # Missing: db_index=True

    # CORRECT
    status = models.CharField(max_length=20, db_index=True)
```

### Unsafe Model Deletion

```python
# DANGEROUS - cascade delete without protection
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

# SAFER - for important relationships
customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
# or
customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
```

### Raw SQL Without Proper Escaping

```python
# VULNERABLE
Model.objects.raw(f"SELECT * FROM table WHERE col = '{value}'")

# SAFE
Model.objects.raw("SELECT * FROM table WHERE col = %s", [value])
```

### Unvalidated Form Data

```python
# VULNERABLE - using request data directly
def view(request):
    user_id = request.POST['user_id']
    User.objects.filter(id=user_id).delete()

# SAFE - validate with forms
def view(request):
    form = DeleteUserForm(request.POST)
    if form.is_valid():
        User.objects.filter(id=form.cleaned_data['user_id']).delete()
```

## FastAPI-Specific Patterns

### Missing Response Model

```python
# WEAK - no response validation
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return {"id": user_id, "name": "John"}

# STRONG - typed response
@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int) -> UserResponse:
    return UserResponse(id=user_id, name="John")
```

### Sync Operations in Async Endpoints

```python
# BLOCKS - sync database call in async
@app.get("/data")
async def get_data():
    return db.query(Model).all()  # SQLAlchemy sync!

# CORRECT - use async ORM or run_in_executor
@app.get("/data")
async def get_data(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Model))
    return result.scalars().all()
```

### Missing Dependency Injection

```python
# TIGHT COUPLING
@app.get("/items")
async def get_items():
    db = Database()  # Hard to test
    return db.get_items()

# LOOSE COUPLING - use Depends
@app.get("/items")
async def get_items(db: Database = Depends(get_database)):
    return db.get_items()
```

## Celery-Specific Patterns

### Passing Large Objects to Tasks

```python
# BAD - serializes entire object
@celery_app.task
def process_order(order):  # Order object serialized!
    order.process()

# GOOD - pass ID, fetch in task
@celery_app.task
def process_order(order_id: int):
    order = Order.objects.get(id=order_id)
    order.process()
```

### Missing Task Retry Configuration

```python
# FRAGILE - no retry on failure
@celery_app.task
def send_email(email_id):
    send(email_id)  # Network errors = lost task

# ROBUST - with retry
@celery_app.task(
    bind=True,
    autoretry_for=(ConnectionError, TimeoutError),
    retry_backoff=True,
    max_retries=3
)
def send_email(self, email_id):
    send(email_id)
```

### Long-Running Tasks Without Heartbeat

```python
# DANGEROUS - worker might be killed
@celery_app.task(time_limit=3600)
def long_task():
    for item in huge_list:
        process(item)

# SAFER - use soft_time_limit and handle
@celery_app.task(soft_time_limit=300, time_limit=360)
def long_task():
    try:
        for item in huge_list:
            process(item)
    except SoftTimeLimitExceeded:
        save_progress()
        long_task.delay()  # Re-queue
```

## Test Coverage Gaps

Flag missing tests for:

1. **Error paths**: Functions with try/except need tests that trigger exceptions
2. **Edge cases**: Empty lists, None values, boundary conditions
3. **Auth-protected endpoints**: Unauthenticated and unauthorized access
4. **Database operations**: Creation, updates, deletions
5. **Async code**: Test both success and timeout scenarios

```python
# Missing test coverage examples
def test_create_user_duplicate_email():  # Error case
    pass

def test_get_items_empty_list():  # Edge case
    pass

def test_delete_order_unauthorized():  # Auth check
    pass
```

## Code Review Checklist

### Security
- [ ] No SQL injection vectors
- [ ] No command injection vectors
- [ ] No hardcoded credentials
- [ ] Proper input validation
- [ ] Safe file path handling

### Logic
- [ ] No mutable default arguments
- [ ] Exceptions properly handled (not swallowed)
- [ ] No bare except clauses
- [ ] Boolean comparisons use `is` for None
- [ ] Closures capture correct values

### Performance
- [ ] No N+1 query patterns
- [ ] Efficient data structures (sets for lookups)
- [ ] No blocking calls in async code
- [ ] Large datasets use iterators/pagination

### Framework
- [ ] Django: select_related/prefetch_related used
- [ ] Django: Indexed fields for common queries
- [ ] FastAPI: Response models defined
- [ ] FastAPI: Async operations properly awaited
- [ ] Celery: Pass IDs not objects, retry configured
