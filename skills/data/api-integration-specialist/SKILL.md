---
name: api-integration-specialist
description: Expert guidance for designing, integrating, and maintaining third-party APIs with best practices for authentication, error handling, rate limiting, security, and data transformation. Use when integrating external APIs, troubleshooting API issues, implementing OAuth flows, handling webhooks, or building API wrappers and clients.
license: Apache-2.0
metadata:
  author: API Integration Team
  category: integration-patterns
  version: 1.0.0
---

# API Integration Specialist

Expert assistant for reliable, secure, and efficient API integrations.

## Core Integration Workflow

### 1. Discovery and Planning
Before integrating any API:
- Review official documentation thoroughly
- Identify required endpoints and authentication methods
- Map out data flow and transformation needs
- Check rate limits and quotas
- Plan error handling strategy
- Document dependencies

### 2. Authentication Setup
Choose and implement appropriate authentication:

**OAuth 2.0** (Recommended for user-delegated access):
```
1. Register application with provider
2. Obtain client_id and client_secret
3. Implement authorization flow:
   - Authorization Code Flow (web apps)
   - PKCE Flow (mobile/SPA)
   - Client Credentials (server-to-server)
4. Handle token refresh automatically
5. Store tokens securely (never in code)
```

**API Keys** (Simple public APIs):
```
- Store in environment variables
- Rotate keys regularly
- Use different keys per environment
- Monitor usage and revoke if compromised
```

**Bearer Tokens** (JWT-based):
```
- Validate token signature
- Check expiration (exp claim)
- Verify issuer and audience
- Implement token refresh logic
```

### 3. Request Construction
Build reliable API requests:

**Headers**:
```
- Content-Type: application/json (for JSON APIs)
- Authorization: Bearer {token} or API-Key {key}
- Accept: application/json
- User-Agent: YourApp/version
- X-Request-ID: {unique-id} (for tracking)
```

**Query Parameters**:
- URL encode all values
- Use consistent naming (camelCase or snake_case)
- Validate before sending
- Document required vs optional params

**Request Body**:
- Validate data structure before sending
- Use schema validation (JSON Schema, Zod, Joi)
- Handle nested objects correctly
- Respect payload size limits

### 4. Response Handling
Process API responses systematically:

**Status Code Patterns**:
```
2xx Success:
  200 OK - Request successful, data returned
  201 Created - Resource created successfully
  202 Accepted - Request accepted, processing async
  204 No Content - Success with no response body

4xx Client Errors:
  400 Bad Request - Invalid input data
  401 Unauthorized - Missing/invalid auth
  403 Forbidden - Valid auth but no permission
  404 Not Found - Resource doesn't exist
  422 Unprocessable Entity - Validation failed
  429 Too Many Requests - Rate limit exceeded

5xx Server Errors:
  500 Internal Server Error - Server issue
  502 Bad Gateway - Upstream server error
  503 Service Unavailable - Temporary outage
  504 Gateway Timeout - Request timeout
```

**Response Validation**:
```python
# Always validate response structure
def validate_response(response):
    # Check status code first
    if response.status_code >= 500:
        raise ServerError("API server error")
    
    # Validate JSON structure
    try:
        data = response.json()
    except ValueError:
        raise ParseError("Invalid JSON response")
    
    # Validate expected fields
    if 'data' not in data:
        raise ValidationError("Missing data field")
    
    return data['data']
```

## Error Handling Patterns

### Retry Strategy with Exponential Backoff
```python
import time
import random

def retry_with_backoff(func, max_retries=3, base_delay=1):
    """
    Retry failed requests with exponential backoff
    """
    for attempt in range(max_retries):
        try:
            return func()
        except (ConnectionError, TimeoutError, ServerError) as e:
            if attempt == max_retries - 1:
                raise
            
            # Calculate backoff: base_delay * 2^attempt + jitter
            delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
            
            print(f"Attempt {attempt + 1} failed: {e}")
            print(f"Retrying in {delay:.2f} seconds...")
            time.sleep(delay)
```

### Circuit Breaker Pattern
```python
class CircuitBreaker:
    """
    Prevent cascading failures by breaking circuit after threshold
    """
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = 'CLOSED'  # CLOSED, OPEN, HALF_OPEN
    
    def call(self, func):
        if self.state == 'OPEN':
            if time.time() - self.last_failure_time > self.timeout:
                self.state = 'HALF_OPEN'
            else:
                raise CircuitOpenError("Circuit breaker is OPEN")
        
        try:
            result = func()
            self.on_success()
            return result
        except Exception as e:
            self.on_failure()
            raise
    
    def on_success(self):
        self.failure_count = 0
        self.state = 'CLOSED'
    
    def on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            self.state = 'OPEN'
```

### Error Response Format
Always return structured errors:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email format",
    "details": [
      {
        "field": "email",
        "issue": "Must be valid email address"
      }
    ],
    "correlation_id": "req-abc-123",
    "timestamp": "2025-11-03T10:30:00Z",
    "documentation_url": "https://docs.api.com/errors/validation"
  }
}
```

## Rate Limiting and Throttling

### Respect Rate Limits
```python
import time
from collections import deque

class RateLimiter:
    """
    Token bucket algorithm for rate limiting
    """
    def __init__(self, max_requests, time_window):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = deque()
    
    def allow_request(self):
        now = time.time()
        
        # Remove expired requests
        while self.requests and self.requests[0] < now - self.time_window:
            self.requests.popleft()
        
        # Check if we can make request
        if len(self.requests) < self.max_requests:
            self.requests.append(now)
            return True
        
        return False
    
    def wait_time(self):
        """Calculate wait time until next request allowed"""
        if not self.requests:
            return 0
        
        oldest = self.requests[0]
        wait = (oldest + self.time_window) - time.time()
        return max(0, wait)
```

### Handle 429 Responses
```python
def handle_rate_limit(response):
    """
    Handle rate limit using Retry-After header
    """
    if response.status_code == 429:
        # Check for Retry-After header
        retry_after = response.headers.get('Retry-After')
        
        if retry_after:
            # Can be seconds or HTTP date
            try:
                wait_seconds = int(retry_after)
            except ValueError:
                # Parse HTTP date
                retry_time = parse_http_date(retry_after)
                wait_seconds = (retry_time - datetime.now()).total_seconds()
            
            print(f"Rate limited. Waiting {wait_seconds} seconds...")
            time.sleep(wait_seconds)
            return True
        
        # No Retry-After, use exponential backoff
        return False
    
    return False
```

## Security Best Practices

### Secret Management
**NEVER** hardcode secrets:
```python
# ❌ WRONG - Never do this
API_KEY = "sk-1234567890abcdef"
API_SECRET = "secret_abc123"

# ✅ CORRECT - Use environment variables
import os
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')

# Validate secrets are present
if not API_KEY or not API_SECRET:
    raise ValueError("Missing required API credentials")
```

### Input Validation
Always validate and sanitize:
```python
def validate_api_input(data):
    """
    Validate data before sending to API
    """
    # Check required fields
    required = ['email', 'name']
    for field in required:
        if field not in data:
            raise ValidationError(f"Missing required field: {field}")
    
    # Sanitize strings
    data['name'] = data['name'].strip()
    data['email'] = data['email'].lower().strip()
    
    # Validate email format
    if not is_valid_email(data['email']):
        raise ValidationError("Invalid email format")
    
    # Remove unexpected fields
    allowed_fields = ['email', 'name', 'age']
    data = {k: v for k, v in data.items() if k in allowed_fields}
    
    return data
```

### HTTPS Only
```python
# Always use HTTPS
BASE_URL = "https://api.example.com"  # ✅ Secure
BASE_URL = "http://api.example.com"   # ❌ Insecure

# Verify SSL certificates
import requests
response = requests.get(url, verify=True)  # ✅ Verify SSL
response = requests.get(url, verify=False) # ❌ Dangerous
```

## Data Transformation

### Request Transformation
```python
def transform_for_api(internal_data):
    """
    Transform internal data format to API format
    """
    return {
        'firstName': internal_data['first_name'],
        'lastName': internal_data['last_name'],
        'emailAddress': internal_data['email'],
        'phoneNumber': format_phone(internal_data['phone']),
        'dateOfBirth': internal_data['dob'].isoformat(),
        'metadata': {
            'source': 'internal_system',
            'version': '1.0'
        }
    }
```

### Response Transformation
```python
def transform_from_api(api_response):
    """
    Transform API response to internal format
    """
    return {
        'id': api_response['userId'],
        'first_name': api_response['firstName'],
        'last_name': api_response['lastName'],
        'email': api_response['emailAddress'],
        'phone': parse_phone(api_response['phoneNumber']),
        'dob': datetime.fromisoformat(api_response['dateOfBirth']),
        'created_at': datetime.fromisoformat(api_response['createdAt'])
    }
```

## Pagination Patterns

### Offset-Based Pagination
```python
def fetch_all_pages_offset(base_url, limit=100):
    """
    Fetch all pages using offset pagination
    """
    all_data = []
    offset = 0
    
    while True:
        response = requests.get(
            base_url,
            params={'limit': limit, 'offset': offset}
        )
        response.raise_for_status()
        
        data = response.json()
        items = data['items']
        
        if not items:
            break
        
        all_data.extend(items)
        offset += limit
        
        # Check if we got all data
        if len(items) < limit:
            break
    
    return all_data
```

### Cursor-Based Pagination
```python
def fetch_all_pages_cursor(base_url):
    """
    Fetch all pages using cursor pagination
    """
    all_data = []
    cursor = None
    
    while True:
        params = {'cursor': cursor} if cursor else {}
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        
        data = response.json()
        all_data.extend(data['items'])
        
        # Check for next page
        cursor = data.get('next_cursor')
        if not cursor:
            break
    
    return all_data
```

## Webhook Integration

### Webhook Security
```python
import hmac
import hashlib

def verify_webhook_signature(payload, signature, secret):
    """
    Verify webhook came from trusted source
    """
    # Compute expected signature
    expected = hmac.new(
        secret.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()
    
    # Compare signatures (timing-safe)
    return hmac.compare_digest(signature, expected)

# Usage in webhook handler
@app.route('/webhooks/payment', methods=['POST'])
def handle_payment_webhook():
    signature = request.headers.get('X-Webhook-Signature')
    payload = request.get_data(as_text=True)
    
    if not verify_webhook_signature(payload, signature, WEBHOOK_SECRET):
        return jsonify({'error': 'Invalid signature'}), 401
    
    # Process webhook
    data = request.json
    process_payment_event(data)
    
    return jsonify({'status': 'received'}), 200
```

## Testing Strategy

### Unit Tests
```python
def test_api_client():
    """Test API client with mocked responses"""
    with requests_mock.Mocker() as m:
        # Mock successful response
        m.get(
            'https://api.example.com/users/123',
            json={'id': 123, 'name': 'John'},
            status_code=200
        )
        
        client = APIClient()
        user = client.get_user(123)
        
        assert user['id'] == 123
        assert user['name'] == 'John'

def test_error_handling():
    """Test error handling"""
    with requests_mock.Mocker() as m:
        # Mock error response
        m.get(
            'https://api.example.com/users/999',
            status_code=404,
            json={'error': 'User not found'}
        )
        
        client = APIClient()
        with pytest.raises(NotFoundError):
            client.get_user(999)
```

### Integration Tests
Run against sandbox/test environments:
```python
def test_real_api_integration():
    """Test against sandbox environment"""
    client = APIClient(
        api_key=TEST_API_KEY,
        base_url='https://sandbox.api.example.com'
    )
    
    # Test create
    user = client.create_user({
        'name': 'Test User',
        'email': 'test@example.com'
    })
    assert user['id'] is not None
    
    # Test read
    fetched = client.get_user(user['id'])
    assert fetched['name'] == 'Test User'
    
    # Test cleanup
    client.delete_user(user['id'])
```

## Monitoring and Logging

### Request Logging
```python
import logging

def log_api_request(method, url, status_code, duration, error=None):
    """Log API request with relevant details"""
    log_data = {
        'method': method,
        'url': url,
        'status_code': status_code,
        'duration_ms': duration * 1000,
        'timestamp': datetime.utcnow().isoformat()
    }
    
    if error:
        log_data['error'] = str(error)
        logging.error(f"API request failed: {log_data}")
    else:
        logging.info(f"API request completed: {log_data}")
```

### Metrics to Track
Monitor these key metrics:
- Request success rate (%)
- Average response time (ms)
- Error rate by status code
- Rate limit hit frequency
- Circuit breaker state changes
- Retry attempts
- Timeout occurrences

## Common Integration Patterns

### 1. Idempotency
Use idempotency keys for retries:
```python
import uuid

def create_payment(amount, idempotency_key=None):
    """Create payment with idempotency support"""
    if not idempotency_key:
        idempotency_key = str(uuid.uuid4())
    
    response = requests.post(
        f'{BASE_URL}/payments',
        json={'amount': amount},
        headers={
            'Authorization': f'Bearer {API_KEY}',
            'Idempotency-Key': idempotency_key
        }
    )
    return response.json()
```

### 2. Batch Operations
Batch requests when supported:
```python
def batch_create_users(users, batch_size=100):
    """Create users in batches"""
    results = []
    
    for i in range(0, len(users), batch_size):
        batch = users[i:i + batch_size]
        
        response = requests.post(
            f'{BASE_URL}/users/batch',
            json={'users': batch}
        )
        response.raise_for_status()
        
        results.extend(response.json()['created'])
    
    return results
```

### 3. Caching
Implement smart caching:
```python
from functools import lru_cache
from datetime import datetime, timedelta

class CachedAPIClient:
    def __init__(self):
        self.cache = {}
        self.cache_ttl = timedelta(minutes=5)
    
    def get_user(self, user_id):
        cache_key = f'user:{user_id}'
        
        # Check cache
        if cache_key in self.cache:
            data, timestamp = self.cache[cache_key]
            if datetime.now() - timestamp < self.cache_ttl:
                return data
        
        # Fetch from API
        response = requests.get(f'{BASE_URL}/users/{user_id}')
        response.raise_for_status()
        data = response.json()
        
        # Update cache
        self.cache[cache_key] = (data, datetime.now())
        
        return data
```

## Resources

For detailed guidance, see:
- **references/ERROR_CODES.md** - Complete error code reference
- **references/AUTHENTICATION_PATTERNS.md** - Auth implementation details
- **references/RATE_LIMITING.md** - Advanced rate limiting strategies
- **scripts/validate_api_spec.py** - Validate OpenAPI specifications
- **scripts/test_api_health.py** - Health check automation

## Validation Tools

Run validation before deployment:
```bash
# Validate API specification
python scripts/validate_api_spec.py openapi.yaml

# Test API health
python scripts/test_api_health.py --base-url https://api.example.com
```

## Quick Reference

**Authentication Priority**:
1. OAuth 2.0 (user delegation)
2. JWT Bearer tokens
3. API Keys (public APIs only)

**Error Handling**:
- Implement retry with exponential backoff
- Use circuit breaker for cascading failures
- Log all errors with correlation IDs
- Return structured error responses

**Security Checklist**:
- ✅ Use HTTPS only
- ✅ Secrets in environment variables
- ✅ Validate all inputs
- ✅ Verify SSL certificates
- ✅ Implement rate limiting
- ✅ Use webhook signatures

**Testing Levels**:
1. Unit tests (mocked responses)
2. Integration tests (sandbox)
3. Load tests (performance)
4. Security tests (penetration)

---

**This skill provides comprehensive API integration guidance. For advanced topics and detailed examples, refer to the references directory.**