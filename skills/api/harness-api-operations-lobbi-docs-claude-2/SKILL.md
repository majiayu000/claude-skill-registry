---
name: Harness API Operations
description: Comprehensive guide for Harness Platform API authentication, rate limiting, error handling, and endpoint operations
version: 1.0.0
trigger_phrases:
  - "harness api"
  - "harness authentication"
  - "harness rate limit"
  - "harness error handling"
  - "harness endpoints"
  - "harness api key"
  - "harness bearer token"
  - "harness rest api"
categories: ["harness", "api", "authentication", "error-handling"]
---

# Harness API Operations Skill

## When to Use This Skill

Use this skill when you need to:

- **Authenticate with Harness APIs** using API keys or service account tokens
- **Handle API rate limits** and implement exponential backoff strategies
- **Process API errors** with proper retry logic and graceful degradation
- **Interact with Harness endpoints** for pipelines, templates, services, environments
- **Implement API clients** with best practices for production systems
- **Debug API integration issues** and understand error responses
- **Build automation** around Harness Platform APIs

Perfect for:
- Building CI/CD automation with Harness
- Creating infrastructure templates programmatically
- Implementing GitOps workflows
- Building custom Harness integrations
- Automating pipeline and service management
- Creating monitoring and reporting tools
- Troubleshooting API connectivity issues

## Core Capabilities

### 1. API Authentication Methods

Master three authentication approaches:
- **API Key Authentication**: Header-based authentication using `x-api-key`
- **Service Account Tokens**: OAuth 2.0 bearer tokens for service accounts
- **Personal Access Tokens**: User-scoped tokens for personal automation
- **Environment Variables**: Secure credential storage patterns
- **Token Rotation**: Implementing credential refresh strategies
- **Multi-Account Management**: Handling multiple Harness accounts

### 2. Rate Limit Management

Implement robust rate limit handling:
- **Read Operations**: 1000 requests per minute
- **Write Operations**: 300 requests per minute
- **Exponential Backoff**: Progressive retry delays with jitter
- **Rate Limit Headers**: Parsing `X-RateLimit-*` headers
- **Request Queuing**: Managing request bursts
- **Concurrent Request Limits**: Throttling parallel operations

### 3. Error Handling Strategies

Comprehensive error management:
- **HTTP Status Codes**: Understanding 4xx and 5xx responses
- **Retry Logic**: Implementing smart retry with circuit breakers
- **Error Correlation**: Using correlation IDs for debugging
- **Graceful Degradation**: Fallback strategies for partial failures
- **Error Logging**: Structured error logging for observability
- **Timeout Management**: Request and connection timeout strategies

### 4. Harness API Endpoints

Complete endpoint reference:
- **Pipeline API**: Create, update, execute, and monitor pipelines
- **Template API**: Manage pipeline and step templates
- **Service API**: CRUD operations for services
- **Environment API**: Environment and infrastructure management
- **IaCM API**: Infrastructure as Code Management workspace operations
- **Connector API**: Managing cloud provider and tool connectors
- **Secrets API**: Secret management operations
- **Project API**: Project and organization management

### 5. Request/Response Patterns

API communication patterns:
- **YAML Body Formatting**: Proper YAML serialization for Harness objects
- **Pagination Handling**: Managing large result sets
- **Filtering and Sorting**: Query parameter patterns
- **Bulk Operations**: Batch processing strategies
- **Webhook Integration**: Event-driven patterns
- **Streaming Responses**: Handling long-running operations

## Authentication Patterns

### Authentication Matrix

| Method | Use Case | Header Format | Scope | Rotation |
|--------|----------|---------------|-------|----------|
| **API Key** | Service automation | `x-api-key: {key}` | Account/Org/Project | Manual |
| **Service Account Token** | CI/CD integration | `Authorization: Bearer {token}` | Configurable RBAC | Automatic |
| **Personal Access Token** | User automation | `x-api-key: {token}` | User permissions | Manual |
| **OAuth 2.0 Client** | Third-party apps | `Authorization: Bearer {token}` | Delegated | Automatic |

### Authentication Code Examples

#### Example 1: API Key Authentication (Python)

```python
import requests
import os
from typing import Optional, Dict, Any

class HarnessClient:
    """Harness API client with API key authentication."""

    def __init__(
        self,
        account_id: str,
        api_key: Optional[str] = None,
        base_url: str = "https://app.harness.io"
    ):
        """
        Initialize Harness API client.

        Args:
            account_id: Harness account identifier
            api_key: API key (defaults to HARNESS_API_KEY env var)
            base_url: Harness API base URL
        """
        self.account_id = account_id
        self.api_key = api_key or os.getenv("HARNESS_API_KEY")
        self.base_url = base_url

        if not self.api_key:
            raise ValueError("API key must be provided or set in HARNESS_API_KEY")

    def _get_headers(self) -> Dict[str, str]:
        """Generate request headers with authentication."""
        return {
            "x-api-key": self.api_key,
            "Content-Type": "application/yaml",
            "Accept": "application/json"
        }

    def _make_request(
        self,
        method: str,
        endpoint: str,
        **kwargs
    ) -> requests.Response:
        """
        Make authenticated API request.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint path
            **kwargs: Additional requests arguments

        Returns:
            Response object
        """
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers()

        # Add account identifier to query params
        params = kwargs.get("params", {})
        params["accountIdentifier"] = self.account_id
        kwargs["params"] = params

        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            **kwargs
        )

        return response

    def get_pipeline(
        self,
        org_id: str,
        project_id: str,
        pipeline_id: str
    ) -> Dict[str, Any]:
        """
        Retrieve pipeline by identifier.

        Args:
            org_id: Organization identifier
            project_id: Project identifier
            pipeline_id: Pipeline identifier

        Returns:
            Pipeline configuration dictionary
        """
        endpoint = f"/pipeline/api/pipelines/v2/{pipeline_id}"
        params = {
            "orgIdentifier": org_id,
            "projectIdentifier": project_id
        }

        response = self._make_request("GET", endpoint, params=params)
        response.raise_for_status()

        return response.json()

# Usage
client = HarnessClient(
    account_id="your_account_id",
    api_key=os.getenv("HARNESS_API_KEY")
)

pipeline = client.get_pipeline(
    org_id="default",
    project_id="my_project",
    pipeline_id="my_pipeline"
)
print(f"Pipeline: {pipeline['data']['name']}")
```

#### Example 2: Service Account Token Authentication (Node.js)

```javascript
const axios = require('axios');

class HarnessClient {
  /**
   * Harness API client with service account token authentication.
   */
  constructor(accountId, options = {}) {
    this.accountId = accountId;
    this.baseURL = options.baseURL || 'https://app.harness.io';
    this.token = options.token || process.env.HARNESS_TOKEN;

    if (!this.token) {
      throw new Error('Service account token must be provided or set in HARNESS_TOKEN');
    }

    this.client = axios.create({
      baseURL: this.baseURL,
      headers: {
        'Authorization': `Bearer ${this.token}`,
        'Content-Type': 'application/yaml',
        'Accept': 'application/json'
      }
    });
  }

  /**
   * Add account identifier to request params.
   */
  _addAccountParam(params = {}) {
    return {
      ...params,
      accountIdentifier: this.accountId
    };
  }

  /**
   * Get pipeline by identifier.
   */
  async getPipeline(orgId, projectId, pipelineId) {
    const endpoint = `/pipeline/api/pipelines/v2/${pipelineId}`;
    const params = this._addAccountParam({
      orgIdentifier: orgId,
      projectIdentifier: projectId
    });

    try {
      const response = await this.client.get(endpoint, { params });
      return response.data;
    } catch (error) {
      console.error('Failed to fetch pipeline:', error.message);
      throw error;
    }
  }

  /**
   * Execute pipeline with runtime inputs.
   */
  async executePipeline(orgId, projectId, pipelineId, runtimeInputs = {}) {
    const endpoint = `/pipeline/api/pipelines/v2/execute/${pipelineId}`;
    const params = this._addAccountParam({
      orgIdentifier: orgId,
      projectIdentifier: projectId
    });

    try {
      const response = await this.client.post(
        endpoint,
        { runtimeInputYaml: runtimeInputs },
        { params }
      );
      return response.data;
    } catch (error) {
      console.error('Failed to execute pipeline:', error.message);
      throw error;
    }
  }
}

// Usage
const client = new HarnessClient('your_account_id', {
  token: process.env.HARNESS_TOKEN
});

(async () => {
  try {
    const pipeline = await client.getPipeline('default', 'my_project', 'my_pipeline');
    console.log(`Pipeline: ${pipeline.data.name}`);

    const execution = await client.executePipeline('default', 'my_project', 'my_pipeline', {
      environment: 'production'
    });
    console.log(`Execution ID: ${execution.data.planExecution.uuid}`);
  } catch (error) {
    console.error('Error:', error);
  }
})();
```

#### Example 3: Environment Variable Best Practices

```bash
# .env file (never commit to version control)
HARNESS_ACCOUNT_ID=your_account_id
HARNESS_API_KEY=pat.your_account_id.your_token
HARNESS_BASE_URL=https://app.harness.io

# For service account tokens
HARNESS_TOKEN=your_service_account_token

# Organization and project defaults
HARNESS_ORG_ID=default
HARNESS_PROJECT_ID=my_project

# Optional: Multiple environments
HARNESS_API_KEY_DEV=pat.dev_account.dev_token
HARNESS_API_KEY_STAGING=pat.staging_account.staging_token
HARNESS_API_KEY_PROD=pat.prod_account.prod_token
```

```python
# Loading environment variables securely
from dotenv import load_dotenv
import os
from typing import Optional

load_dotenv()  # Load .env file

class HarnessConfig:
    """Centralized Harness configuration from environment variables."""

    def __init__(self, environment: str = "prod"):
        self.environment = environment
        self.account_id = self._get_required("HARNESS_ACCOUNT_ID")
        self.base_url = os.getenv("HARNESS_BASE_URL", "https://app.harness.io")
        self.org_id = os.getenv("HARNESS_ORG_ID", "default")
        self.project_id = os.getenv("HARNESS_PROJECT_ID")

        # Environment-specific API key
        env_key = f"HARNESS_API_KEY_{environment.upper()}"
        self.api_key = os.getenv(env_key) or self._get_required("HARNESS_API_KEY")

    def _get_required(self, key: str) -> str:
        """Get required environment variable or raise error."""
        value = os.getenv(key)
        if not value:
            raise ValueError(f"Required environment variable {key} is not set")
        return value

# Usage
config = HarnessConfig(environment="prod")
client = HarnessClient(
    account_id=config.account_id,
    api_key=config.api_key,
    base_url=config.base_url
)
```

## Rate Limit Management

### Rate Limit Rules

| Operation Type | Limit | Window | Reset Behavior |
|----------------|-------|--------|----------------|
| **Read Operations** | 1000 requests | 1 minute | Rolling window |
| **Write Operations** | 300 requests | 1 minute | Rolling window |
| **Template Operations** | 100 requests | 1 minute | Rolling window |
| **Webhook Triggers** | 500 requests | 1 minute | Rolling window |

### Rate Limit Response Headers

```
X-RateLimit-Limit: 1000           # Total limit for the window
X-RateLimit-Remaining: 847        # Remaining requests
X-RateLimit-Reset: 1642694400     # Unix timestamp when limit resets
Retry-After: 30                   # Seconds to wait before retry (429 response)
```

### Rate Limit Handling Examples

#### Example 1: Exponential Backoff with Jitter (Python)

```python
import time
import random
from typing import Callable, Any, Optional
import requests
from functools import wraps

class RateLimitError(Exception):
    """Rate limit exceeded error."""
    pass

def exponential_backoff_retry(
    max_retries: int = 5,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    jitter: bool = True
):
    """
    Decorator for exponential backoff retry with jitter.

    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Initial delay in seconds
        max_delay: Maximum delay between retries
        jitter: Add random jitter to prevent thundering herd
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            retries = 0

            while retries <= max_retries:
                try:
                    return func(*args, **kwargs)

                except requests.exceptions.HTTPError as e:
                    if e.response.status_code == 429:  # Rate limit exceeded
                        if retries == max_retries:
                            raise RateLimitError(
                                f"Rate limit exceeded after {max_retries} retries"
                            )

                        # Calculate delay with exponential backoff
                        delay = min(base_delay * (2 ** retries), max_delay)

                        # Add jitter to prevent synchronized retries
                        if jitter:
                            delay = delay * (0.5 + random.random())

                        # Check if server provided Retry-After header
                        retry_after = e.response.headers.get('Retry-After')
                        if retry_after:
                            try:
                                delay = float(retry_after)
                            except ValueError:
                                pass  # Use calculated delay

                        print(f"Rate limited. Retrying in {delay:.2f} seconds...")
                        time.sleep(delay)
                        retries += 1
                    else:
                        raise  # Re-raise non-rate-limit errors

            raise RateLimitError(f"Max retries ({max_retries}) exceeded")

        return wrapper
    return decorator

class HarnessClientWithRetry(HarnessClient):
    """Harness client with automatic retry logic."""

    @exponential_backoff_retry(max_retries=5, base_delay=2.0)
    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Make request with automatic retry on rate limit."""
        response = super()._make_request(method, endpoint, **kwargs)

        # Log rate limit status
        if 'X-RateLimit-Remaining' in response.headers:
            remaining = int(response.headers['X-RateLimit-Remaining'])
            limit = int(response.headers['X-RateLimit-Limit'])

            if remaining < limit * 0.1:  # Less than 10% remaining
                print(f"Warning: Rate limit low ({remaining}/{limit} remaining)")

        response.raise_for_status()
        return response

# Usage
client = HarnessClientWithRetry(
    account_id="your_account_id",
    api_key=os.getenv("HARNESS_API_KEY")
)

# Automatic retry on rate limit
pipeline = client.get_pipeline("default", "my_project", "my_pipeline")
```

#### Example 2: Request Queue with Rate Limiting (Node.js)

```javascript
const pQueue = require('p-queue').default;

class RateLimitedHarnessClient extends HarnessClient {
  /**
   * Harness client with request queuing and rate limiting.
   */
  constructor(accountId, options = {}) {
    super(accountId, options);

    // Create separate queues for read and write operations
    this.readQueue = new pQueue({
      concurrency: 10,              // Max concurrent read requests
      interval: 60000,              // 1 minute window
      intervalCap: 900              // Max 900 requests per minute (leaving buffer)
    });

    this.writeQueue = new pQueue({
      concurrency: 5,               // Max concurrent write requests
      interval: 60000,              // 1 minute window
      intervalCap: 270              // Max 270 requests per minute (leaving buffer)
    });
  }

  /**
   * Make rate-limited request using appropriate queue.
   */
  async _makeRateLimitedRequest(method, endpoint, options = {}) {
    const isWriteOperation = ['POST', 'PUT', 'PATCH', 'DELETE'].includes(method.toUpperCase());
    const queue = isWriteOperation ? this.writeQueue : this.readQueue;

    return queue.add(async () => {
      try {
        const response = await this.client.request({
          method,
          url: endpoint,
          ...options
        });

        // Log rate limit status
        const remaining = response.headers['x-ratelimit-remaining'];
        const limit = response.headers['x-ratelimit-limit'];

        if (remaining && limit) {
          const percentRemaining = (remaining / limit) * 100;
          if (percentRemaining < 10) {
            console.warn(`Rate limit warning: ${remaining}/${limit} remaining (${percentRemaining.toFixed(1)}%)`);
          }
        }

        return response;
      } catch (error) {
        if (error.response?.status === 429) {
          const retryAfter = error.response.headers['retry-after'] || 30;
          console.log(`Rate limited. Waiting ${retryAfter}s before retry...`);

          // Wait and retry
          await new Promise(resolve => setTimeout(resolve, retryAfter * 1000));
          return this._makeRateLimitedRequest(method, endpoint, options);
        }
        throw error;
      }
    });
  }

  /**
   * Get pipeline with rate limiting.
   */
  async getPipeline(orgId, projectId, pipelineId) {
    const endpoint = `/pipeline/api/pipelines/v2/${pipelineId}`;
    const params = this._addAccountParam({
      orgIdentifier: orgId,
      projectIdentifier: projectId
    });

    const response = await this._makeRateLimitedRequest('GET', endpoint, { params });
    return response.data;
  }

  /**
   * Batch get multiple pipelines with rate limiting.
   */
  async getPipelines(orgId, projectId, pipelineIds) {
    const promises = pipelineIds.map(pipelineId =>
      this.getPipeline(orgId, projectId, pipelineId)
    );

    return Promise.all(promises);
  }
}

// Usage
const client = new RateLimitedHarnessClient('your_account_id', {
  token: process.env.HARNESS_TOKEN
});

(async () => {
  // Fetch 100 pipelines - automatically queued and rate-limited
  const pipelineIds = Array.from({ length: 100 }, (_, i) => `pipeline_${i}`);
  const pipelines = await client.getPipelines('default', 'my_project', pipelineIds);
  console.log(`Fetched ${pipelines.length} pipelines`);
})();
```

#### Example 3: Circuit Breaker Pattern

```python
from enum import Enum
from datetime import datetime, timedelta
from typing import Callable, Any
import requests

class CircuitState(Enum):
    """Circuit breaker states."""
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing if service recovered

class CircuitBreaker:
    """
    Circuit breaker for API calls to prevent cascade failures.
    """

    def __init__(
        self,
        failure_threshold: int = 5,
        timeout: int = 60,
        expected_exception: type = requests.exceptions.HTTPError
    ):
        """
        Initialize circuit breaker.

        Args:
            failure_threshold: Number of failures before opening circuit
            timeout: Seconds to wait before attempting recovery
            expected_exception: Exception type to catch
        """
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.expected_exception = expected_exception

        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED

    def call(self, func: Callable, *args, **kwargs) -> Any:
        """
        Execute function with circuit breaker protection.

        Args:
            func: Function to execute
            *args: Function arguments
            **kwargs: Function keyword arguments

        Returns:
            Function result

        Raises:
            Exception: If circuit is open or function fails
        """
        if self.state == CircuitState.OPEN:
            if datetime.now() - self.last_failure_time > timedelta(seconds=self.timeout):
                # Try to recover
                self.state = CircuitState.HALF_OPEN
                print("Circuit breaker: Attempting recovery (HALF_OPEN)")
            else:
                raise Exception(
                    f"Circuit breaker OPEN. Service unavailable. "
                    f"Retry after {self.timeout}s"
                )

        try:
            result = func(*args, **kwargs)

            # Success - reset failure count
            if self.state == CircuitState.HALF_OPEN:
                print("Circuit breaker: Recovery successful (CLOSED)")

            self.failure_count = 0
            self.state = CircuitState.CLOSED
            return result

        except self.expected_exception as e:
            self.failure_count += 1
            self.last_failure_time = datetime.now()

            if self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
                print(
                    f"Circuit breaker: Threshold reached ({self.failure_count} failures). "
                    f"Circuit OPEN"
                )

            raise

class HarnessClientWithCircuitBreaker(HarnessClientWithRetry):
    """Harness client with circuit breaker pattern."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.circuit_breaker = CircuitBreaker(
            failure_threshold=5,
            timeout=60
        )

    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Make request with circuit breaker protection."""
        return self.circuit_breaker.call(
            super()._make_request,
            method,
            endpoint,
            **kwargs
        )

# Usage
client = HarnessClientWithCircuitBreaker(
    account_id="your_account_id",
    api_key=os.getenv("HARNESS_API_KEY")
)

# Protected by circuit breaker
try:
    pipeline = client.get_pipeline("default", "my_project", "my_pipeline")
except Exception as e:
    print(f"Request failed: {e}")
```

## Error Handling

### HTTP Status Code Reference

| Status Code | Meaning | Retry Strategy | Common Causes |
|-------------|---------|----------------|---------------|
| **400 Bad Request** | Invalid request format | Do not retry | Malformed YAML, missing required fields |
| **401 Unauthorized** | Authentication failed | Do not retry | Invalid or expired API key/token |
| **403 Forbidden** | Insufficient permissions | Do not retry | Missing RBAC permissions |
| **404 Not Found** | Resource doesn't exist | Do not retry | Wrong identifier or deleted resource |
| **409 Conflict** | Resource conflict | Retry after resolution | Concurrent modification |
| **422 Unprocessable Entity** | Validation failed | Do not retry | Invalid field values |
| **429 Too Many Requests** | Rate limit exceeded | Retry with backoff | Too many requests |
| **500 Internal Server Error** | Server error | Retry with backoff | Temporary server issue |
| **502 Bad Gateway** | Gateway error | Retry with backoff | Proxy or load balancer issue |
| **503 Service Unavailable** | Service overloaded | Retry with backoff | Temporary unavailability |
| **504 Gateway Timeout** | Request timeout | Retry with backoff | Long-running operation |

### Error Response Format

```json
{
  "status": "ERROR",
  "code": "INVALID_REQUEST",
  "message": "Pipeline with identifier 'invalid_pipeline' does not exist",
  "correlationId": "abc123-def456-ghi789",
  "detailedMessage": "The requested pipeline 'invalid_pipeline' was not found in project 'my_project' under organization 'default'",
  "responseMessages": [
    {
      "code": "RESOURCE_NOT_FOUND",
      "level": "ERROR",
      "message": "Pipeline not found",
      "failureTypes": ["APPLICATION_ERROR"]
    }
  ]
}
```

### Error Handling Examples

#### Example 1: Comprehensive Error Handler (Python)

```python
import logging
from typing import Optional, Dict, Any
from enum import Enum
import requests

class ErrorSeverity(Enum):
    """Error severity levels."""
    TRANSIENT = "transient"      # Temporary, retry
    PERMANENT = "permanent"      # Permanent, do not retry
    FATAL = "fatal"              # Fatal, terminate

class HarnessAPIError(Exception):
    """Base exception for Harness API errors."""

    def __init__(
        self,
        message: str,
        status_code: int,
        response: Optional[Dict[str, Any]] = None,
        correlation_id: Optional[str] = None
    ):
        self.message = message
        self.status_code = status_code
        self.response = response or {}
        self.correlation_id = correlation_id
        super().__init__(self.message)

    @property
    def severity(self) -> ErrorSeverity:
        """Determine error severity based on status code."""
        if self.status_code in [429, 500, 502, 503, 504]:
            return ErrorSeverity.TRANSIENT
        elif self.status_code in [400, 401, 403, 404, 422]:
            return ErrorSeverity.PERMANENT
        else:
            return ErrorSeverity.FATAL

    @property
    def should_retry(self) -> bool:
        """Determine if error should be retried."""
        return self.severity == ErrorSeverity.TRANSIENT

class HarnessErrorHandler:
    """Centralized error handling for Harness API operations."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """
        Handle API response and raise appropriate errors.

        Args:
            response: Requests response object

        Returns:
            Response data dictionary

        Raises:
            HarnessAPIError: For any error responses
        """
        try:
            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError as e:
            error_data = self._extract_error_data(response)
            correlation_id = response.headers.get('X-Correlation-Id')

            # Log error with context
            self.logger.error(
                f"Harness API error: {error_data['message']} "
                f"(Status: {response.status_code}, "
                f"Correlation ID: {correlation_id})"
            )

            raise HarnessAPIError(
                message=error_data['message'],
                status_code=response.status_code,
                response=error_data,
                correlation_id=correlation_id
            ) from e

    def _extract_error_data(self, response: requests.Response) -> Dict[str, Any]:
        """Extract error information from response."""
        try:
            data = response.json()

            # Handle different error response formats
            if isinstance(data, dict):
                return {
                    'message': data.get('message', 'Unknown error'),
                    'code': data.get('code', 'UNKNOWN'),
                    'detailed_message': data.get('detailedMessage'),
                    'response_messages': data.get('responseMessages', [])
                }
        except ValueError:
            pass

        # Fallback to status code message
        return {
            'message': response.reason,
            'code': str(response.status_code),
            'detailed_message': response.text[:500] if response.text else None,
            'response_messages': []
        }

class RobustHarnessClient(HarnessClientWithRetry):
    """Harness client with comprehensive error handling."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_handler = HarnessErrorHandler()

        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Make request with error handling."""
        try:
            response = super()._make_request(method, endpoint, **kwargs)
            return self.error_handler.handle_response(response)

        except HarnessAPIError as e:
            if e.status_code == 404:
                # Handle specific error cases
                self.logger.warning(f"Resource not found: {endpoint}")
                raise
            elif e.status_code == 401:
                self.logger.error("Authentication failed. Check API key/token.")
                raise
            elif e.status_code == 403:
                self.logger.error(
                    f"Insufficient permissions for {method} {endpoint}. "
                    f"Check RBAC settings."
                )
                raise
            else:
                raise

# Usage with error handling
client = RobustHarnessClient(
    account_id="your_account_id",
    api_key=os.getenv("HARNESS_API_KEY")
)

try:
    pipeline = client.get_pipeline("default", "my_project", "my_pipeline")
    print(f"Successfully fetched pipeline: {pipeline['data']['name']}")

except HarnessAPIError as e:
    if e.severity == ErrorSeverity.PERMANENT:
        print(f"Permanent error (do not retry): {e.message}")
        print(f"Correlation ID: {e.correlation_id}")
    elif e.severity == ErrorSeverity.TRANSIENT:
        print(f"Transient error (safe to retry): {e.message}")
    else:
        print(f"Fatal error: {e.message}")
        raise
```

#### Example 2: Graceful Degradation Pattern

```python
from typing import Optional, List, Dict, Any
import logging

class PipelineService:
    """
    Service layer with graceful degradation for pipeline operations.
    """

    def __init__(self, client: RobustHarnessClient):
        self.client = client
        self.logger = logging.getLogger(__name__)
        self.cache = {}  # Simple in-memory cache

    def get_pipeline_with_fallback(
        self,
        org_id: str,
        project_id: str,
        pipeline_id: str,
        use_cache: bool = True
    ) -> Optional[Dict[str, Any]]:
        """
        Get pipeline with fallback to cached version on error.

        Args:
            org_id: Organization identifier
            project_id: Project identifier
            pipeline_id: Pipeline identifier
            use_cache: Whether to use cached fallback

        Returns:
            Pipeline data or None if unavailable
        """
        cache_key = f"{org_id}/{project_id}/{pipeline_id}"

        try:
            # Try to fetch from API
            pipeline = self.client.get_pipeline(org_id, project_id, pipeline_id)

            # Update cache on success
            if use_cache:
                self.cache[cache_key] = pipeline

            return pipeline

        except HarnessAPIError as e:
            if e.severity == ErrorSeverity.TRANSIENT and use_cache:
                # Fall back to cache for transient errors
                cached_pipeline = self.cache.get(cache_key)

                if cached_pipeline:
                    self.logger.warning(
                        f"API error, using cached pipeline data: {e.message}"
                    )
                    return cached_pipeline
                else:
                    self.logger.error(
                        f"API error and no cached data available: {e.message}"
                    )
                    return None
            else:
                # Permanent errors or cache disabled
                self.logger.error(f"Failed to fetch pipeline: {e.message}")
                return None

    def batch_get_pipelines(
        self,
        org_id: str,
        project_id: str,
        pipeline_ids: List[str],
        fail_fast: bool = False
    ) -> List[Optional[Dict[str, Any]]]:
        """
        Batch fetch pipelines with error isolation.

        Args:
            org_id: Organization identifier
            project_id: Project identifier
            pipeline_ids: List of pipeline identifiers
            fail_fast: Stop on first error if True

        Returns:
            List of pipeline data (None for failed fetches)
        """
        results = []
        errors = []

        for pipeline_id in pipeline_ids:
            try:
                pipeline = self.get_pipeline_with_fallback(
                    org_id, project_id, pipeline_id
                )
                results.append(pipeline)

            except Exception as e:
                errors.append({
                    'pipeline_id': pipeline_id,
                    'error': str(e)
                })

                if fail_fast:
                    raise
                else:
                    # Continue processing remaining pipelines
                    results.append(None)

        # Log summary
        success_count = sum(1 for r in results if r is not None)
        self.logger.info(
            f"Batch fetch complete: {success_count}/{len(pipeline_ids)} successful"
        )

        if errors:
            self.logger.warning(f"Errors encountered: {len(errors)}")
            for error in errors:
                self.logger.warning(
                    f"  - {error['pipeline_id']}: {error['error']}"
                )

        return results

# Usage
client = RobustHarnessClient(
    account_id="your_account_id",
    api_key=os.getenv("HARNESS_API_KEY")
)

service = PipelineService(client)

# Single pipeline with fallback
pipeline = service.get_pipeline_with_fallback("default", "my_project", "my_pipeline")
if pipeline:
    print(f"Pipeline: {pipeline['data']['name']}")
else:
    print("Pipeline unavailable")

# Batch fetch with error isolation
pipeline_ids = ["pipeline1", "pipeline2", "pipeline3"]
pipelines = service.batch_get_pipelines("default", "my_project", pipeline_ids)
print(f"Fetched {sum(1 for p in pipelines if p)} pipelines")
```

## Harness API Endpoints

### Complete Endpoint Reference

#### Pipeline API

```
Base: /pipeline/api/pipelines/v2
```

| Endpoint | Method | Description | Rate Limit |
|----------|--------|-------------|------------|
| `/{pipelineId}` | GET | Get pipeline by ID | Read |
| `/` | POST | Create pipeline | Write |
| `/{pipelineId}` | PUT | Update pipeline | Write |
| `/{pipelineId}` | DELETE | Delete pipeline | Write |
| `/execute/{pipelineId}` | POST | Execute pipeline | Write |
| `/execution/{executionId}` | GET | Get execution status | Read |
| `/list` | POST | List pipelines (with filters) | Read |
| `/{pipelineId}/summary` | GET | Get pipeline summary | Read |

#### Template API

```
Base: /template/api/templates
```

| Endpoint | Method | Description | Rate Limit |
|----------|--------|-------------|------------|
| `/{templateId}` | GET | Get template by ID | Read |
| `/` | POST | Create template | Write |
| `/{templateId}` | PUT | Update template | Write |
| `/{templateId}` | DELETE | Delete template | Write |
| `/list` | POST | List templates | Read |
| `/{templateId}/versions` | GET | Get template versions | Read |

#### Service API

```
Base: /ng/api/servicesV2
```

| Endpoint | Method | Description | Rate Limit |
|----------|--------|-------------|------------|
| `/{serviceId}` | GET | Get service by ID | Read |
| `/` | POST | Create service | Write |
| `/{serviceId}` | PUT | Update service | Write |
| `/{serviceId}` | DELETE | Delete service | Write |
| `/list` | GET | List services | Read |

#### Environment API

```
Base: /ng/api/environmentsV2
```

| Endpoint | Method | Description | Rate Limit |
|----------|--------|-------------|------------|
| `/{environmentId}` | GET | Get environment by ID | Read |
| `/` | POST | Create environment | Write |
| `/{environmentId}` | PUT | Update environment | Write |
| `/{environmentId}` | DELETE | Delete environment | Write |
| `/list` | GET | List environments | Read |

#### IaCM API

```
Base: /iacm/api/workspaces
```

| Endpoint | Method | Description | Rate Limit |
|----------|--------|-------------|------------|
| `/{workspaceId}` | GET | Get workspace by ID | Read |
| `/` | POST | Create workspace | Write |
| `/{workspaceId}` | PUT | Update workspace | Write |
| `/{workspaceId}` | DELETE | Delete workspace | Write |
| `/{workspaceId}/runs` | POST | Trigger workspace run | Write |
| `/{workspaceId}/runs/{runId}` | GET | Get run status | Read |

#### Connector API

```
Base: /ng/api/connectors
```

| Endpoint | Method | Description | Rate Limit |
|----------|--------|-------------|------------|
| `/{connectorId}` | GET | Get connector by ID | Read |
| `/` | POST | Create connector | Write |
| `/{connectorId}` | PUT | Update connector | Write |
| `/{connectorId}` | DELETE | Delete connector | Write |
| `/{connectorId}/test-connection` | POST | Test connector | Write |
| `/list` | GET | List connectors | Read |

### Endpoint Usage Examples

#### Example 1: Complete Pipeline CRUD Operations

```python
from typing import Dict, Any, Optional

class PipelineManager:
    """Manager for pipeline CRUD operations."""

    def __init__(self, client: RobustHarnessClient, org_id: str, project_id: str):
        self.client = client
        self.org_id = org_id
        self.project_id = project_id

    def create_pipeline(self, pipeline_yaml: str) -> Dict[str, Any]:
        """
        Create a new pipeline.

        Args:
            pipeline_yaml: Pipeline YAML definition

        Returns:
            Created pipeline data
        """
        endpoint = "/pipeline/api/pipelines/v2"
        params = {
            "orgIdentifier": self.org_id,
            "projectIdentifier": self.project_id
        }

        response = self.client._make_request(
            "POST",
            endpoint,
            params=params,
            data=pipeline_yaml,
            headers={"Content-Type": "application/yaml"}
        )

        return response

    def get_pipeline(self, pipeline_id: str) -> Dict[str, Any]:
        """
        Get pipeline by identifier.

        Args:
            pipeline_id: Pipeline identifier

        Returns:
            Pipeline data
        """
        endpoint = f"/pipeline/api/pipelines/v2/{pipeline_id}"
        params = {
            "orgIdentifier": self.org_id,
            "projectIdentifier": self.project_id
        }

        response = self.client._make_request("GET", endpoint, params=params)
        return response

    def update_pipeline(self, pipeline_id: str, pipeline_yaml: str) -> Dict[str, Any]:
        """
        Update existing pipeline.

        Args:
            pipeline_id: Pipeline identifier
            pipeline_yaml: Updated pipeline YAML

        Returns:
            Updated pipeline data
        """
        endpoint = f"/pipeline/api/pipelines/v2/{pipeline_id}"
        params = {
            "orgIdentifier": self.org_id,
            "projectIdentifier": self.project_id
        }

        response = self.client._make_request(
            "PUT",
            endpoint,
            params=params,
            data=pipeline_yaml,
            headers={"Content-Type": "application/yaml"}
        )

        return response

    def delete_pipeline(self, pipeline_id: str) -> bool:
        """
        Delete pipeline.

        Args:
            pipeline_id: Pipeline identifier

        Returns:
            True if deleted successfully
        """
        endpoint = f"/pipeline/api/pipelines/v2/{pipeline_id}"
        params = {
            "orgIdentifier": self.org_id,
            "projectIdentifier": self.project_id
        }

        self.client._make_request("DELETE", endpoint, params=params)
        return True

    def execute_pipeline(
        self,
        pipeline_id: str,
        runtime_inputs: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Execute pipeline with optional runtime inputs.

        Args:
            pipeline_id: Pipeline identifier
            runtime_inputs: Runtime input values

        Returns:
            Execution data with execution ID
        """
        endpoint = f"/pipeline/api/pipelines/v2/execute/{pipeline_id}"
        params = {
            "orgIdentifier": self.org_id,
            "projectIdentifier": self.project_id
        }

        body = {}
        if runtime_inputs:
            import yaml
            body["runtimeInputYaml"] = yaml.dump(runtime_inputs)

        response = self.client._make_request(
            "POST",
            endpoint,
            params=params,
            json=body
        )

        return response

    def get_execution_status(self, execution_id: str) -> Dict[str, Any]:
        """
        Get pipeline execution status.

        Args:
            execution_id: Execution identifier

        Returns:
            Execution status data
        """
        endpoint = f"/pipeline/api/pipelines/v2/execution/{execution_id}"
        params = {
            "orgIdentifier": self.org_id,
            "projectIdentifier": self.project_id
        }

        response = self.client._make_request("GET", endpoint, params=params)
        return response

    def list_pipelines(
        self,
        filters: Optional[Dict[str, Any]] = None,
        page: int = 0,
        size: int = 50
    ) -> Dict[str, Any]:
        """
        List pipelines with optional filters.

        Args:
            filters: Filter criteria
            page: Page number (0-indexed)
            size: Page size

        Returns:
            Paginated list of pipelines
        """
        endpoint = "/pipeline/api/pipelines/v2/list"
        params = {
            "orgIdentifier": self.org_id,
            "projectIdentifier": self.project_id,
            "page": page,
            "size": size
        }

        body = filters or {}

        response = self.client._make_request(
            "POST",
            endpoint,
            params=params,
            json=body
        )

        return response

# Usage
client = RobustHarnessClient(
    account_id="your_account_id",
    api_key=os.getenv("HARNESS_API_KEY")
)

manager = PipelineManager(client, "default", "my_project")

# Create pipeline
pipeline_yaml = """
pipeline:
  identifier: my_new_pipeline
  name: My New Pipeline
  projectIdentifier: my_project
  orgIdentifier: default
  stages:
    - stage:
        name: Deploy
        identifier: deploy
        type: Deployment
"""

created = manager.create_pipeline(pipeline_yaml)
print(f"Created pipeline: {created['data']['identifier']}")

# Execute pipeline
execution = manager.execute_pipeline("my_new_pipeline", {
    "environment": "production"
})
execution_id = execution['data']['planExecution']['uuid']
print(f"Started execution: {execution_id}")

# Monitor execution
status = manager.get_execution_status(execution_id)
print(f"Execution status: {status['data']['pipelineExecutionSummary']['status']}")

# List all pipelines
pipelines = manager.list_pipelines(page=0, size=100)
print(f"Found {len(pipelines['data']['content'])} pipelines")

# Update pipeline
updated_yaml = pipeline_yaml.replace("My New Pipeline", "My Updated Pipeline")
updated = manager.update_pipeline("my_new_pipeline", updated_yaml)
print(f"Updated pipeline: {updated['data']['name']}")

# Delete pipeline
deleted = manager.delete_pipeline("my_new_pipeline")
print(f"Deleted: {deleted}")
```

## Request/Response Patterns

### YAML Body Formatting

Harness APIs accept YAML for resource definitions. Proper formatting is critical.

```python
import yaml
from typing import Dict, Any

def create_pipeline_yaml(config: Dict[str, Any]) -> str:
    """
    Generate properly formatted pipeline YAML.

    Args:
        config: Pipeline configuration dictionary

    Returns:
        YAML string
    """
    pipeline_dict = {
        "pipeline": {
            "identifier": config["identifier"],
            "name": config["name"],
            "projectIdentifier": config["project_id"],
            "orgIdentifier": config["org_id"],
            "stages": config.get("stages", [])
        }
    }

    # Use safe_dump with proper formatting
    return yaml.safe_dump(
        pipeline_dict,
        default_flow_style=False,
        sort_keys=False,
        indent=2
    )

# Usage
config = {
    "identifier": "my_pipeline",
    "name": "My Pipeline",
    "org_id": "default",
    "project_id": "my_project",
    "stages": [
        {
            "stage": {
                "name": "Build",
                "identifier": "build",
                "type": "CI"
            }
        }
    ]
}

pipeline_yaml = create_pipeline_yaml(config)
print(pipeline_yaml)
```

### Pagination Handling

```python
from typing import Iterator, Dict, Any

def paginate_pipelines(
    manager: PipelineManager,
    page_size: int = 100
) -> Iterator[Dict[str, Any]]:
    """
    Generator to iterate through all pipelines with pagination.

    Args:
        manager: PipelineManager instance
        page_size: Number of items per page

    Yields:
        Pipeline data dictionaries
    """
    page = 0

    while True:
        response = manager.list_pipelines(page=page, size=page_size)

        pipelines = response['data']['content']
        if not pipelines:
            break

        for pipeline in pipelines:
            yield pipeline

        # Check if there are more pages
        total_pages = response['data']['totalPages']
        if page >= total_pages - 1:
            break

        page += 1

# Usage
for pipeline in paginate_pipelines(manager, page_size=50):
    print(f"Pipeline: {pipeline['identifier']}")
```

## Best Practices

### 1. Secure Credential Management

**Do:**
- Store API keys in environment variables or secrets managers
- Rotate credentials regularly
- Use service accounts with minimal required permissions
- Implement credential refresh for long-running services

**Don't:**
- Commit credentials to version control
- Share credentials across environments
- Use overly permissive API keys
- Log credentials in error messages

### 2. Rate Limit Optimization

**Do:**
- Implement request queuing for batch operations
- Use exponential backoff with jitter
- Monitor rate limit headers proactively
- Cache frequently accessed data
- Use webhooks instead of polling when possible

**Don't:**
- Ignore rate limit headers
- Retry immediately after 429
- Make unnecessary duplicate requests
- Use fixed retry intervals

### 3. Error Handling Strategy

**Do:**
- Log errors with correlation IDs
- Implement circuit breakers for cascading failures
- Use structured error logging
- Provide fallback mechanisms
- Distinguish between transient and permanent errors

**Don't:**
- Swallow errors silently
- Retry on permanent errors (4xx)
- Expose internal error details to end users
- Assume all 5xx errors are retryable

### 4. API Request Optimization

**Do:**
- Use batch endpoints when available
- Request only needed fields
- Implement client-side caching
- Use conditional requests (ETags)
- Compress request/response bodies

**Don't:**
- Fetch entire resource graphs unnecessarily
- Poll for status updates too frequently
- Make sequential requests that could be parallel
- Ignore pagination for large result sets

### 5. Monitoring and Observability

**Do:**
- Track API latency and error rates
- Monitor rate limit usage
- Log correlation IDs for debugging
- Set up alerts for error thresholds
- Use structured logging

**Don't:**
- Rely on client-side logs alone
- Ignore slow API responses
- Skip correlation ID tracking
- Log sensitive data

## Related Skills

- **[[infrastructure-template-generator]]** - Generate Harness templates programmatically
- **[[harness-pipeline-builder]]** - Build pipelines using API
- **[[error-recovery-patterns]]** - Advanced error recovery strategies
- **[[api-client-design]]** - Design robust API clients
- **[[rate-limit-strategies]]** - Advanced rate limiting patterns
- **[[authentication-patterns]]** - Secure authentication implementations
- **[[observability-patterns]]** - Monitoring and logging best practices

## Troubleshooting

### Common Issues and Solutions

#### Issue: Authentication Failures

**Symptoms:**
- 401 Unauthorized responses
- "Invalid API key" errors

**Solutions:**
1. Verify API key format: `pat.{account_id}.{token}`
2. Check API key permissions and scope
3. Ensure account ID matches API key
4. Verify token hasn't expired
5. Check for leading/trailing whitespace in credentials

#### Issue: Rate Limit Exceeded

**Symptoms:**
- 429 Too Many Requests
- Retry-After headers in responses

**Solutions:**
1. Implement exponential backoff with jitter
2. Use request queuing
3. Cache frequently accessed data
4. Batch operations when possible
5. Monitor rate limit headers proactively

#### Issue: Intermittent 500/502/503 Errors

**Symptoms:**
- Occasional server errors
- Gateway timeout responses

**Solutions:**
1. Implement retry logic with backoff
2. Use circuit breaker pattern
3. Add request timeout configuration
4. Check Harness status page for incidents
5. Contact Harness support with correlation IDs

#### Issue: YAML Parsing Errors

**Symptoms:**
- 400 Bad Request
- "Invalid YAML" error messages

**Solutions:**
1. Validate YAML syntax before sending
2. Check for special characters needing escaping
3. Ensure proper indentation
4. Use YAML libraries instead of string concatenation
5. Validate against Harness schema

---

**Version:** 1.0.0
**Last Updated:** 2026-01-19
**Skill Type:** API Integration & Operations
**Complexity:** Intermediate to Advanced
