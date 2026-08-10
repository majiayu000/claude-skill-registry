---
name: api-integration
description: Integrate with external APIs using REST clients, webhook consumers, SDK wrappers, and polling patterns with proper authentication, error handling, and retry logic. Use when the user requests api integration or provides relevant inputs for this workflow.
license: MIT
metadata:
  author: awesome-ai-agent-skills
  version: 1.0.0
---

# API Integration

This skill enables an AI agent to integrate applications with external APIs reliably. The agent selects the right integration pattern (REST client, webhook consumer, polling, SDK wrapper), implements authentication (API keys, OAuth, JWT), handles errors with retries and circuit breakers, and respects rate limits. The result is production-grade integration code that handles real-world failure modes.

## Workflow

1. **Analyze the target API:** Review the API documentation, OpenAPI spec, or SDK reference to understand available endpoints, authentication requirements, rate limits, and response formats. Identify whether the API supports webhooks for push-based updates or requires polling. Note any idiosyncrasies like non-standard error formats or pagination schemes.

2. **Choose an integration pattern:** Select the appropriate pattern based on the use case. Use a REST client for on-demand request/response interactions. Use webhook consumers for real-time event-driven data. Use polling when the API has no webhook support but you need near-real-time updates. Wrap official SDKs when they exist to add retry logic, logging, and a consistent interface.

3. **Implement authentication:** Configure the correct authentication method—API key in headers, OAuth 2.0 bearer tokens, JWT-based service auth, or basic auth. Store credentials securely using environment variables or a secrets manager. For OAuth flows, implement token refresh logic so long-running integrations don't break when access tokens expire.

4. **Build the client with error handling:** Write the integration code with structured error handling. Catch HTTP errors by status code category: 4xx for client errors (don't retry), 429 for rate limiting (retry with backoff), 5xx for server errors (retry with exponential backoff). Parse error response bodies for actionable messages. Log all requests and responses at debug level for troubleshooting.

5. **Add retry and circuit breaker logic:** Implement exponential backoff with jitter for transient failures. Set a maximum retry count (typically 3-5). Implement a circuit breaker that opens after consecutive failures and periodically allows a test request through. This prevents cascading failures when a downstream API is degraded.

6. **Test and monitor:** Write integration tests using recorded HTTP fixtures (VCR pattern) so tests don't hit live APIs. Monitor integration health with metrics for request latency, error rates, and rate limit headroom. Set up alerts for sustained error rates above threshold.

## Supported Technologies

- **HTTP clients:** requests (Python), httpx (Python async), axios (Node.js), fetch, HttpClient (.NET), OkHttp (Java)
- **Authentication:** API keys, OAuth 2.0, JWT, Basic Auth, HMAC signatures
- **Resilience:** tenacity (Python), retry (Node.js), Polly (.NET), resilience4j (Java)
- **Testing:** responses (Python), nock (Node.js), VCR.py, WireMock
- **GraphQL clients:** gql (Python), graphql-request (Node.js), Apollo Client

## Usage

Provide the agent with the target API name or documentation URL, the operations you need to perform, and the programming language. Specify authentication method and any constraints (rate limits, data volume). The agent will produce a complete integration module with error handling, retries, and usage examples.

## Examples

### Example 1: Stripe API Integration in Python

```python
import os
import time
import logging
from typing import Optional
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)

class StripeClient:
    """Production-ready Stripe API client with retries and error handling."""

    BASE_URL = "https://api.stripe.com/v1"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ["STRIPE_SECRET_KEY"]
        self.session = self._build_session()

    def _build_session(self) -> requests.Session:
        session = requests.Session()
        session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/x-www-form-urlencoded",
            "Stripe-Version": "2024-06-20",
        })
        retry_strategy = Retry(
            total=4,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST", "DELETE"],
            respect_retry_after_header=True,
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)
        return session

    def create_customer(self, email: str, name: str, metadata: Optional[dict] = None) -> dict:
        """Create a Stripe customer."""
        payload = {"email": email, "name": name}
        if metadata:
            for key, value in metadata.items():
                payload[f"metadata[{key}]"] = value
        response = self._request("POST", "/customers", data=payload)
        return response

    def create_payment_intent(self, amount_cents: int, currency: str = "usd",
                              customer_id: Optional[str] = None) -> dict:
        """Create a payment intent for a given amount."""
        payload = {"amount": amount_cents, "currency": currency}
        if customer_id:
            payload["customer"] = customer_id
        return self._request("POST", "/payment_intents", data=payload)

    def list_charges(self, customer_id: str, limit: int = 10) -> list:
        """List charges for a customer with automatic pagination."""
        charges = []
        params = {"customer": customer_id, "limit": limit}
        while True:
            data = self._request("GET", "/charges", params=params)
            charges.extend(data["data"])
            if not data["has_more"]:
                break
            params["starting_after"] = data["data"][-1]["id"]
        return charges

    def _request(self, method: str, path: str, **kwargs) -> dict:
        url = f"{self.BASE_URL}{path}"
        try:
            resp = self.session.request(method, url, **kwargs)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.HTTPError as e:
            error_body = e.response.json().get("error", {})
            logger.error(
                "Stripe API error: type=%s code=%s message=%s",
                error_body.get("type"),
                error_body.get("code"),
                error_body.get("message"),
            )
            if e.response.status_code == 429:
                retry_after = int(e.response.headers.get("Retry-After", 5))
                logger.warning("Rate limited. Retry after %ds", retry_after)
            raise
        except requests.exceptions.ConnectionError:
            logger.error("Connection failed to Stripe API")
            raise

# Usage
client = StripeClient()
customer = client.create_customer("alice@example.com", "Alice Smith")
payment = client.create_payment_intent(2500, customer_id=customer["id"])
print(f"Payment intent {payment['id']} for ${payment['amount']/100:.2f}")
```

### Example 2: GraphQL API Integration with requests

```python
import requests
from typing import Any, Optional

class GraphQLClient:
    """Lightweight GraphQL client with error handling and variable support."""

    def __init__(self, endpoint: str, headers: Optional[dict] = None):
        self.endpoint = endpoint
        self.session = requests.Session()
        if headers:
            self.session.headers.update(headers)

    def execute(self, query: str, variables: Optional[dict] = None) -> dict:
        """Execute a GraphQL query or mutation."""
        payload = {"query": query}
        if variables:
            payload["variables"] = variables

        response = self.session.post(self.endpoint, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()

        if "errors" in result:
            error_messages = [e["message"] for e in result["errors"]]
            raise GraphQLError(error_messages, result.get("data"))

        return result["data"]

class GraphQLError(Exception):
    def __init__(self, messages: list, partial_data: Any = None):
        self.messages = messages
        self.partial_data = partial_data
        super().__init__(f"GraphQL errors: {'; '.join(messages)}")

# Usage: Query a GitHub-style GraphQL API
client = GraphQLClient(
    endpoint="https://api.github.com/graphql",
    headers={"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}"},
)

# Fetch repositories with pagination
query = """
query($owner: String!, $cursor: String) {
  user(login: $owner) {
    repositories(first: 10, after: $cursor, orderBy: {field: UPDATED_AT, direction: DESC}) {
      pageInfo {
        hasNextPage
        endCursor
      }
      nodes {
        name
        description
        stargazerCount
        primaryLanguage { name }
      }
    }
  }
}
"""

repos = []
cursor = None
while True:
    data = client.execute(query, {"owner": "octocat", "cursor": cursor})
    page = data["user"]["repositories"]
    repos.extend(page["nodes"])
    if not page["pageInfo"]["hasNextPage"]:
        break
    cursor = page["pageInfo"]["endCursor"]

for repo in repos:
    lang = repo["primaryLanguage"]["name"] if repo["primaryLanguage"] else "N/A"
    print(f"{repo['name']} ({lang}) - {repo['stargazerCount']} stars")
```

## Best Practices

- **Never hardcode credentials.** Use environment variables or a secrets manager. Rotate API keys on a regular schedule and immediately on suspected compromise.
- **Respect rate limits proactively.** Parse `X-RateLimit-Remaining` headers and slow down before hitting the limit rather than reacting to 429 responses after the fact.
- **Use idempotency keys** for POST requests to payment and financial APIs. This prevents duplicate charges or operations when retrying after network failures.
- **Implement request/response logging** at debug level with sensitive fields (tokens, card numbers) redacted. This is invaluable for debugging integration issues in production.
- **Set explicit timeouts** on all HTTP requests (connect timeout of 5s, read timeout of 30s). Never use infinite timeouts—a hung connection will block your entire application.
- **Version-pin API integrations** by sending explicit API version headers (e.g., `Stripe-Version`). This prevents breaking changes from affecting your integration unexpectedly.

## Edge Cases

- **API deprecation:** Monitor for `Deprecation` and `Sunset` headers in responses. Log warnings when these appear so you can migrate before the endpoint is removed.
- **Partial responses:** Some APIs return `200 OK` with an `errors` array (common in GraphQL). Always check for error fields even on successful HTTP status codes.
- **Clock skew:** APIs that use timestamp-based signatures (HMAC, JWT) can reject requests if your server clock is skewed. Use NTP and allow a small tolerance window.
- **Large payloads:** When fetching large datasets, use streaming responses and pagination rather than loading everything into memory. Watch for APIs that silently truncate results.
- **Network partitions:** A request may succeed on the server but the response is lost. This is why idempotency keys matter—you can safely retry without causing duplicate side effects.
- **Webhook vs. polling race conditions:** If you use both webhooks and polling for the same data, implement deduplication to avoid processing the same event twice.
