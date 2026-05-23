---
name: fail-fast-no-hedging
description: Eliminate component hedging anti-patterns that mask infrastructure failures. Build systems that fail loudly when broken instead of limping along in degraded states. Critical for production reliability and operational visibility.
---

# Fail-Fast Engineering: Architectural Honesty Over Silent Degradation

## 🚨 Core Principle

**Hedging** is treating **required** infrastructure as optional through defensive try/except blocks that mask failures as normal operation.

**The Critical Question:** Is this component required for the system to work correctly, or is it a genuine optional enhancement?

When **required** infrastructure fails, the system MUST fail loudly. When **optional** features fail, logging and continuing may be appropriate.

## 📋 Assessment Output Format (REQUIRED)

When analyzing a codebase, conclude with this structured list of all hedging issues found:

```markdown
## Hedging Anti-Patterns Found in [directory/module name]

**N files with component hedging violations:**

1. **filename.py** (SEVERITY)
   - Location: `function_name()` lines X-Y
   - Issue: Brief description of what's wrong
   - Hedging: Explanation of how it's treating required infrastructure as optional
   - Impact: What happens in production when infrastructure fails

2. **filename.py** (SEVERITY)
   - Location: `function_name()` lines X-Y
   - Issue: Brief description of what's wrong
   - Hedging: Explanation of how it's treating required infrastructure as optional
   - Impact: What happens in production when infrastructure fails
```

**Example (from lt_memory/ audit):**

```markdown
## Hedging Anti-Patterns Found in lt_memory/

**3 files with component hedging violations:**

1. **db_access.py** (HIGH SEVERITY)
   - Location: `get_or_create_entity()` lines 916-933
   - Issue: Returns `None` when database INSERT...RETURNING fails, masking query failure as "entity not found"
   - Hedging: Docstring declares return type as `Entity`, implementation silently returns `None` on infrastructure failure
   - Impact: Caller cannot distinguish between "entity doesn't exist" (legitimate) vs "database query failed" (infrastructure down)

2. **extraction.py** (HIGH SEVERITY)
   - Location: `_parse_extraction_response()` lines 396-397 and 430
   - Issue: Returns `[]` (empty list) when JSON parsing fails, instead of raising as docstring declares
   - Hedging: Docstring says "Raises: ValueError" but code returns `[]` on parse failures
   - Impact: Caller sees empty list and treats it as "no memories extracted" when actually LLM returned invalid JSON
```

This format makes all issues immediately scannable before remediation work begins.

---

## 🎯 Quick-Start Guide

When analyzing a new codebase:

1. **Identify Infrastructure Dependencies**
   - Database connections
   - Cache/session stores
   - External APIs
   - Message queues
   - File systems

2. **Apply Three Diagnostic Tests**
   - **Semantic Distinction Test**: Can you distinguish "no data" from "infrastructure down"?
   - **Never Executes Test**: Will this fallback realistically run during normal operation?
   - **Contract Match Test**: Does behavior match the docstring/type hints?

3. **Look for These Red Flags**
   ```
   except Exception: return []     # Infrastructure failure → empty data
   except Exception: return False  # Connection error → "not allowed"
   except Exception: return None   # Database down → "not found"
   ```

## 🌍 Real-World Patterns from Production Codebases

Based on systematic removal of 40+ hedging anti-patterns across production systems, these specific patterns emerge repeatedly:

### 1. Infrastructure Failures Converted to Client Errors (CRITICAL)

**Pattern**: Catching database/service failures and raising ValidationError (400) instead of letting them propagate as 500s.

```python
# REAL EXAMPLE: CNS API Layer
def execute_action(self, action: str, data: Dict) -> Dict:
    try:
        session_manager = get_shared_session_manager()
        lt_db = LTMemoryDB(session_manager)
    except Exception as e:
        # Database down converted to "your input is invalid"!
        if "connection" in str(e) or "database" in str(e):
            raise ValidationError(f"Database connection failed: {e}")
```

**Impact**: Users see "Bad Request" when database is down. Monitoring doesn't alert (watches 500s, not 400s). Operators think users are sending bad data while infrastructure burns.

**Fix**: Remove business-layer exception translation. Let infrastructure exceptions bubble to API boundary where proper HTTP status translation happens.

### 2. The Availability Flag Plague (PERVASIVE)

**Pattern**: Setting `self.component_available = False` during init, then checking it hundreds of times throughout the codebase.

```python
# REAL EXAMPLE: ValkeyClient with 200+ defensive checks
class ValkeyClient:
    def __init__(self):
        try:
            self._init_connections()
            self.valkey_available = True
        except Exception:
            self.valkey_available = False

    def get(self, key: str) -> Optional[Any]:
        if not self.valkey_available:  # One of 200+ checks!
            return None
        return self.valkey.get(key)
```

**Impact**:
- Every operation has defensive check overhead
- Infrastructure failures silently masked as "feature disabled"
- Dead code paths when component is actually required
- False sense of "graceful degradation"

**Fix**: Remove availability tracking entirely. If component is required, fail at initialization. The "graceful degradation" never actually helps - it just delays the inevitable failure.

### 3. Silent Success Claims on Failure (DECEPTIVE)

**Pattern**: Returning `{"success": True, "value": None}` when infrastructure fails.

```python
# REAL EXAMPLE: Calendar configuration endpoint
def get_calendar_config(self, user_id: str) -> Dict:
    try:
        config = credential_service.get_credential(user_id, "calendar_url")
        return {"success": True, "calendar_url": config}
    except Exception:
        # Vault down? Claim success anyway!
        return {"success": True, "calendar_url": None, "message": "Not configured"}
```

**Impact**: Client cannot distinguish "user hasn't configured calendar" from "credential service is down". UI shows "not configured" while Vault burns.

### 4. Job Registration Boolean Swallowing (TIME BOMB)

**Pattern**: Critical scheduled jobs return `False` on registration failure instead of raising.

```python
# REAL EXAMPLE: Token renewal that fails silently
def register_jobs(self) -> bool:
    try:
        scheduler = get_scheduler()
        success = scheduler.register_job(
            job_id="vault-token-renewer",
            func=self.renew_token,
            trigger="interval",
            days=7
        )
        return success  # False if registration failed
    except Exception:
        return False  # Import error? Scheduler down? Who knows!
```

**Impact**: Token renewal silently fails to register. System runs fine for 32 days, then authentication mysteriously breaks when token expires. No errors logged at startup.

### 5. Lazy Loading Creating False Optionality

**Pattern**: Deferring initialization with lazy loading, making required components appear optional.

```python
# REAL EXAMPLE: Email service that's actually required
class Service:
    def __init__(self):
        self._email_service = None  # Lazy loaded

    def send_welcome_email(self, user_id: str):
        if hasattr(self, '_email_service') and self._email_service:
            self._email_service.send(...)  # Silently skip if not loaded!
```

**Impact**: Required functionality (welcome emails) silently skipped when service fails to initialize. Users don't get onboarding emails, no errors logged.

### 6. Multi-Layer Exception Masking (DIAGNOSTIC HELL)

**Pattern**: Base class catches exceptions, subclass adds another layer, framework adds third layer.

```python
# REAL EXAMPLE: Working memory trinket system
# Layer 1: Base trinket class
class BaseTrinket:
    def handle_update_request(self):
        try:
            return self._generate_content()
        except Exception:
            return None  # Mask all errors

# Layer 2: Event handler
def _handle_update_trinket(self, event):
    try:
        content = trinket.handle_update_request()
    except Exception as e:
        logger.warning(f"Trinket failed: {e}")  # Second mask

# Layer 3: Individual trinket
class ReminderTrinket(BaseTrinket):
    def _generate_content(self):
        try:
            reminders = self.get_reminders()
        except Exception:
            return []  # Third mask!
```

**Impact**: Database failure → returns [] → caught and returns None → caught and logged as warning. Original DatabaseError completely lost. Operators see "Trinket failed: 'NoneType' has no attribute 'format'" instead of "Database connection lost".

### 7. Data Corruption Hidden as Empty State

**Pattern**: JSON decode errors returning None instead of raising.

```python
# REAL EXAMPLE: Database JSON columns
def fetch_as_dict(self, query: str) -> Optional[Dict]:
    result = self.execute(query)
    if result and result[0]:
        try:
            return json.loads(result[0])
        except json.JSONDecodeError:
            logger.warning("Failed to parse JSON")
            return None  # Corrupted data = no data!
```

**Impact**: Data corruption indistinguishable from NULL values. Corrupted user preferences silently become "no preferences". Data quality issues invisible until user complaints.

### 8. The hasattr() Vestigial Pattern

**Pattern**: Checking for attributes that are never set anywhere in the codebase.

```python
# REAL EXAMPLE: Cache updater that doesn't exist
def _update_cache_if_pooled(self) -> None:
    if hasattr(self, '_cache_updater') and self._cache_updater:
        # This attribute is NEVER set anywhere!
        try:
            self._cache_updater(self.user_id, self._message_cache)
        except Exception:
            logger.warning("Cache update failed")
```

**Impact**: Dead code creating false architectural impressions. Future developers think "cache updates must be optional" when they're actually handled elsewhere entirely.

### 9. Partial Success Masquerading as Complete Success

**Pattern**: Continuing after required sub-operations fail.

```python
# REAL EXAMPLE: User creation with broken setup
def create_user(email: str) -> str:
    user_id = db.insert_user(email)

    try:
        initialize_user_preferences(user_id)
        create_welcome_reminders(user_id)
        send_welcome_email(user_id)
    except Exception as e:
        logger.error(f"User setup failed: {e}")
        # Continue - user exists but broken!

    return user_id  # "Success!"
```

**Impact**: Users created in broken state. Can log in but missing preferences, reminders, welcome email. Support tickets: "Features don't work for some users."

### 10. Rate Limiter Fail-Closed Masquerade

**Pattern**: Security-motivated hedging that creates operational blindness.

```python
# REAL EXAMPLE: Rate limiter "failing closed"
def is_allowed(self, identifier: str) -> Tuple[bool, int]:
    try:
        count = valkey.increment(f"rate:{identifier}")
        return count <= self.limit, 0
    except Exception:
        # "Fail closed for security" - but identical to rate limited!
        return False, self.window_seconds
```

**Impact**: Valkey outage = all users rate limited. Support flooded with "I can't log in" while ops thinks "high traffic day". Security theater creating availability problems.

## 📐 Pattern Library

### Pattern 1: Infrastructure Masquerading

<pattern name="infrastructure-masquerade">
<anti_pattern>
def operation([PARAMS]) -> [RETURN_TYPE]:
    try:
        result = [REQUIRED_INFRASTRUCTURE].query()
        return result
    except Exception:
        return [SAFE_DEFAULT]  # Infrastructure failure looks like [NORMAL_STATE]
</anti_pattern>

<fail_fast>
def operation([PARAMS]) -> [RETURN_TYPE]:
    result = [REQUIRED_INFRASTRUCTURE].query()  # Raises on infrastructure failure
    return result  # Only returns actual data or legitimate empty state
</fail_fast>

<diagnostic>
Can caller distinguish between "[NO_DATA]" and "[INFRASTRUCTURE_DOWN]"?
</diagnostic>
</pattern>

**Examples of [SAFE_DEFAULT]**: `[]`, `None`, `False`, `0`, `{}`
**Examples of [REQUIRED_INFRASTRUCTURE]**: `database`, `cache`, `auth_service`, `message_queue`

### Pattern 2: False Optionality

<pattern name="false-optionality">
<anti_pattern>
class Service:
    def __init__(self):
        self._component = None  # Lazy loading creates false impression

    @property
    def component(self):
        if self._component is None:
            self._component = initialize_component()
        return self._component

    def operation(self):
        if hasattr(self, '_component') and self._component:  # Defensive checks
            return self._component.do_work()
        return [DEGRADED_RESULT]
</anti_pattern>

<fail_fast>
class Service:
    def __init__(self):
        self.component = initialize_component()  # Fail at startup if broken

    def operation(self):
        return self.component.do_work()  # No defensive checks needed
</fail_fast>

<diagnostic>
Is the component truly optional, or are we just afraid of startup failures?
</diagnostic>
</pattern>

### Pattern 3: Partial Success Masking

<pattern name="partial-success">
<anti_pattern>
def create_resource([PARAMS]) -> [ID_TYPE]:
    resource_id = database.insert([DATA])

    try:
        initialize_related([resource_id])  # Required setup
    except Exception:
        logger.error("Setup failed")
        # Continue - resource exists but broken

    return resource_id  # Partial success returned as complete
</anti_pattern>

<fail_fast>
def create_resource([PARAMS]) -> [ID_TYPE]:
    resource_id = database.insert([DATA])
    initialize_related([resource_id])  # Fails → transaction rolls back
    return resource_id  # Only returns if fully initialized
</fail_fast>

<diagnostic>
Are we creating broken/incomplete entities that will fail later?
</diagnostic>
</pattern>

### Pattern 4: Safe Defaults on Error

<pattern name="safe-defaults">
<anti_pattern>
def get_metric([PARAMS]) -> [NUMERIC_TYPE]:
    try:
        result = metrics_service.query([PARAMS])
        return result.value
    except Exception:
        return 0  # Service down? Return zero!

def get_config([PARAMS]) -> Dict:
    try:
        return config_service.fetch([KEY])
    except Exception:
        return {"success": True, "value": None}  # Claim success on failure!
</anti_pattern>

<fail_fast>
def get_metric([PARAMS]) -> [NUMERIC_TYPE]:
    result = metrics_service.query([PARAMS])  # Raises on service failure
    return result.value  # Zero only when metric genuinely is zero

def get_config([PARAMS]) -> Dict:
    config = config_service.fetch([KEY])  # Raises on service failure
    return {"success": True, "value": config}
</fail_fast>

<diagnostic>
Does the "safe" default hide infrastructure problems from operators?
</diagnostic>
</pattern>

### Pattern 5: The "Never Executes" Fallback

<pattern name="never-executes">
<anti_pattern>
def get_or_create_resource([PARAMS]) -> [RESOURCE_TYPE]:
    result = database.insert_returning([DATA])

    if result:
        return [RESOURCE_TYPE](**result)

    # This fallback will NEVER execute in correct operation
    # INSERT...RETURNING should always return a result
    # If it doesn't, infrastructure is broken
    fetch_query = "SELECT * FROM [TABLE] WHERE ..."
    existing = database.query(fetch_query)
    return [RESOURCE_TYPE](**existing) if existing else None
</anti_pattern>

<fail_fast>
def get_or_create_resource([PARAMS]) -> [RESOURCE_TYPE]:
    result = database.insert_returning([DATA])

    if not result:
        raise RuntimeError(
            f"INSERT...RETURNING failed - database operation broken, "
            f"not a recoverable race condition"
        )

    return [RESOURCE_TYPE](**result)
</fail_fast>

<diagnostic>
Critical Question: "Will this fallback code realistically execute when the system is operating correctly?"
- YES → Legitimate defensive programming (real race conditions)
- NO → Hedging that masks the real error
</diagnostic>
</pattern>

## 🔍 Analysis Protocol

### Step-by-Step Failure Analysis

For each try/except block, perform this systematic analysis:

```
FAILURE SCENARIO ANALYSIS
=========================

1. What operations are in the try block?
   - Database calls?
   - External API calls?
   - Cache/session operations?

2. What can fail, and why?
   - Network timeout
   - Service unavailable
   - Invalid data format
   - Resource exhausted

3. Are these failures EXPECTED or UNEXPECTED?
   - Expected: Retry logic, validation errors, race conditions
   - Unexpected: Infrastructure down, OOM, disk full

4. What does the except block do?
   - Return safe default (None, [], False, 0)?
   - Log and re-raise?
   - Convert to different exception?
   - Continue with degraded state?

5. Can the caller handle this error?
   - Yes: Specific exception type (UserNotFoundError)
   - No: Infrastructure failure (DatabaseError, ConnectionError)
```

### Decision Framework

For each try/except block, ask:

1. **Is this infrastructure required?**
   - Required → Must fail-fast
   - Optional → May catch and continue

2. **What type of operation?**
   - Synchronous request → Fail-fast on infrastructure errors
   - Async event handler → May log and retry
   - Background job → Consider retry strategy

3. **What's the failure mode?**
   - Infrastructure down → Propagate immediately
   - Transient network → Retry with backoff
   - Invalid input → Return error response

4. **What does the catch block do?**
   - Returns safe default → Likely hedging
   - Adds context and re-raises → Appropriate
   - Logs and continues → Check if truly optional

### Severity Classification

**HIGH Severity**
- Silent data corruption (partial user creation, orphaned records)
- Security controls disabled on infrastructure failure
- Core business operations succeed in broken states
- Job registration failures that manifest weeks/months later
- User creation succeeds but required setup fails

**MEDIUM Severity**
- Infrastructure failures indistinguishable from normal operation
- Authentication/authorization degrades silently
- Resource management (locks, sessions) masks failures
- Rate limiting returns "limited" when infrastructure down
- Configuration failures return success with null values

**LOW Severity**
- Unnecessary exception re-wrapping
- Logging before re-raising
- Overly broad exception handling with proper re-raise
- JSON parsing errors masked as "not found" (when field is optional)

## ✅ When Try/Except IS Appropriate

### Rule 1: Translating Across Abstraction Boundaries

```python
# GOOD: Database layer translates SQLAlchemy exceptions to domain exceptions
def get_user(user_id: str) -> User:
    try:
        return session.query(User).filter_by(id=user_id).one()
    except NoResultFound:
        raise UserNotFoundError(f"User {user_id} not found")
    except SQLAlchemyError as e:
        raise DatabaseError(f"Database query failed: {e}")

# GOOD: API endpoint translates domain exceptions to HTTP status codes
@router.post("/actions")
def actions_endpoint(request_data: ActionRequest):
    try:
        response = handler.handle_request(request_data)
        return response.to_dict()
    except ValidationError as e:
        return JSONResponse(status_code=400, ...)  # Client error
    except Exception as e:
        logger.error(f"Actions endpoint error: {e}", exc_info=True)
        return JSONResponse(status_code=500, ...)  # Infrastructure error

# BAD: Business logic converting infrastructure failures to client errors
def execute_action(self, action: str) -> Dict:
    try:
        session_manager = get_session_manager()
        lt_db = LTMemoryDB(session_manager)
    except Exception as e:
        # WRONG: Makes infrastructure failure (500) look like client error (400)
        raise ValidationError(f"Database connection failed: {e}")
```

**Why**: Infrastructure exception handling belongs at architectural boundaries (API endpoints), not in business logic. Converting DatabaseError → ValidationError makes 500s appear as 400s.

### Rule 2: Recovering from Expected, Recoverable Errors

```python
# GOOD: Retry on transient failures with backoff
def fetch_with_retry(url: str, attempts: int = 3) -> Response:
    for attempt in range(attempts):
        try:
            return requests.get(url, timeout=5)
        except requests.Timeout:
            if attempt == attempts - 1:
                raise  # Final attempt failed
            logger.warning(f"Attempt {attempt+1} timed out, retrying...")
            time.sleep(2 ** attempt)  # Exponential backoff
```

**Why**: Transient network failures are expected and retrying can succeed. Each retry is logged for visibility.

### Rule 3: Adding Business Context Not in Stack Trace

```python
# GOOD: Add context that's not obvious from code
def process_batch(batch_id: str, items: List[Item]):
    try:
        for i, item in enumerate(items):
            process_item(item)
    except ProcessingError as e:
        # Stack trace shows WHERE but not WHICH batch/item
        logger.error(
            f"Batch {batch_id} failed at item {i+1}/{len(items)} "
            f"(item_id={item.id}): {e}"
        )
        raise ProcessingError(f"Batch {batch_id} processing failed") from e
```

**Why**: Adds business context (batch ID, item position) that's not in the stack trace but crucial for debugging.

### Rule 4: Handling Non-Fatal Failures

```python
# GOOD: Optional features can fail gracefully
def save_with_cache(data: Dict) -> None:
    # Critical: Save to database
    db.save(data)  # Must succeed, raises on failure

    # Optional: Update cache
    try:
        cache.set(data['id'], data)
    except CacheError as e:
        logger.warning(f"Cache update failed (non-critical): {e}")
        # Continue - cache miss is acceptable
```

**Why**: Cache failure shouldn't break the operation. Log because we're suppressing the error.

## ❌ When Try/Except is WRONG

1. **Converting infrastructure failures to None/False/[]**
2. **Catching broad exceptions without re-raising**
3. **Logging and re-raising (redundant)**
4. **Masking required service failures as optional**

## 🛠️ Refactoring Steps

1. **Write test for infrastructure failure propagation**
   ```python
   def test_propagates_database_failure():
       with mock.patch('db.query', side_effect=DatabaseError):
           with pytest.raises(DatabaseError):
               service.get_data()
   ```

2. **Remove defensive try/except**
3. **Update docstring/types if needed**
4. **Run test to verify failure propagates**
5. **Add monitoring for the new exception type**

## 🔬 Testing Fail-Fast Behavior

### Test Infrastructure Failures Propagate

```python
def test_infrastructure_failure_propagates():
    """Verify infrastructure failure raises, doesn't return safe default."""
    service = AuthService()

    with mock.patch('valkey.get', side_effect=ConnectionError("Valkey unreachable")):
        with pytest.raises(ConnectionError):
            service.validate_session("test-token")

    # NOT: assert service.validate_session(...) is None
```

### Test Legitimate Empty States

```python
def test_user_with_no_tokens_returns_empty_list():
    """Verify empty result is legitimate, not masked error."""
    service = AuthService()

    # User exists but has no tokens
    result = service.list_tokens(user_id="test-user")

    assert result == []  # Legitimately empty
    assert not isinstance(result, type(None))  # Not None from error
```

### Production Impact Scenarios

**Before Fail-Fast Refactoring (Valkey Down)**
```
User Experience:
- "Too many requests" errors (rate limiter returns False)
- "Invalid session" errors (session validation returns None)
- "Resource locked" timeouts (locks return False)

Operator Experience:
- No monitoring alerts
- Users complaining about "weird behavior"
- 2 hours to diagnose: "Oh, Valkey has been down since 3pm"
```

**After Fail-Fast Refactoring (Valkey Down)**
```
User Experience:
- "Service temporarily unavailable" (clear 500 errors)

Operator Experience:
- PagerDuty alert: "VALKEY_CONNECTION_ERROR" at 3:01pm
- Clear stack trace pointing to infrastructure
- Fixed in 5 minutes
```

## 🚩 Warning Signs in Code Reviews

When reviewing code, these patterns indicate likely hedging:

### Textual Clues
- Comments like "Fail closed for security", "Graceful degradation", "Continue anyway"
- Variable names: `component_available`, `is_enabled`, `has_feature`
- Return values: `{"success": True, "value": None}` when operations fail

### Structural Clues
- `try:` blocks wrapping infrastructure calls with `except Exception:`
- Methods returning both `bool` for success AND results
- `Optional[T]` return types for operations that should always succeed
- Multiple defensive checks: `if hasattr() and self.thing and self.thing.ready:`

### Behavioral Clues
- Init methods that set availability flags instead of failing
- Config/credential lookups that return defaults on failure
- Database queries returning `[]` in except blocks
- Scheduled job registration returning `False` instead of raising

### Architecture Smells
- Base classes with catch-all exception handlers
- Lazy loading of required components
- Services checking `if self.required_dependency:` before every operation
- Factory functions returning `None` when service creation fails

## 🎯 The Three Diagnostic Tests

### Test 1: Semantic Distinction
Can you distinguish between legitimate empty states and infrastructure failures?
- ✅ Raises `DatabaseError` when down, returns `[]` when no data
- ❌ Returns `[]` for both cases

### Test 2: Never Executes
Will this fallback code run during normal operation?
- ✅ Handles genuine race conditions or expected states
- ❌ "Defensive" code that never executes when system works

### Test 3: Contract Match
Does the implementation match documented behavior?
- ✅ Docstring says "raises X" and code raises X
- ❌ Docstring says "raises X" but code returns None

## 📝 Summary

**Goal**: Systems that crash obviously when broken are easier to operate than systems that limp along mysteriously.

**Remember**:
- Required dependencies must fail loudly
- Optional enhancements may fail quietly
- The distinction is an architectural decision, not an implementation detail
- When in doubt, fail fast and let operators decide

## 📊 Lessons from Production Refactoring

After removing 40+ hedging patterns across multiple systems, key insights emerge:

### 1. **Hedging Compounds Over Time**
- Starts with one "harmless" try/except
- Other developers add more defensive layers
- Eventually 3-4 layers of exception masking
- Original errors become completely untraceable

### 2. **The Availability Flag Anti-Pattern**
- `component_available` flags spread like a virus
- One component adds flag → dependent components check it
- Soon 200+ defensive checks throughout codebase
- Massive dead code when component is actually required

### 3. **API Layer Is The Only Translation Point**
- Business logic should NEVER convert infrastructure errors to ValidationError
- HTTP status translation happens ONCE at the API boundary
- Everything else just propagates exceptions naturally

### 4. **"Fail Closed" Security Theater**
- Rate limiting that returns `False` when infrastructure down
- Makes outages look like normal rate limiting
- Better: Let it fail with clear error so ops can fix infrastructure
- Real security comes from working infrastructure, not silent failures

### 5. **Test Suites Reveal Hidden Assumptions**
- Removing hedging often breaks tests that assumed silent degradation
- These test failures are GOOD - they reveal incorrect assumptions
- Tests checking for `None` when they should expect exceptions

### 6. **The Time Bomb Pattern**
- Scheduled job registration failures are the worst
- System appears to start fine
- Weeks/months later, mysterious failures when jobs never ran
- Always raise immediately on registration failure

### 7. **Startup Failures Are A Gift**
- Fail at startup > fail at first request > fail silently
- Operators can fix config/infrastructure before accepting traffic
- Silent degradation means discovering issues only after user complaints