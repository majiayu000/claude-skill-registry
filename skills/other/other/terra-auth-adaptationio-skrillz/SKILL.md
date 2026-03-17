---
name: terra-auth
description: Terra API authentication, credentials management, and environment configuration. Use when setting up Terra integration, managing API keys, generating widget sessions, or configuring testing/staging/production environments.
---

# Terra Authentication & Credentials

Manage Terra API authentication across testing, staging, and production environments.

## Credential Files

Credentials are stored in environment-specific `.env` files:

| Environment | File |
|-------------|------|
| Testing | `.env.terra.testing` |
| Staging | `.env.terra.staging` |
| Production | `.env.terra.production` |

**Load credentials**:
```python
from dotenv import load_dotenv
import os

# Load specific environment
load_dotenv(".env.terra.testing")

dev_id = os.getenv("TERRA_DEV_ID")
api_key = os.getenv("TERRA_API_KEY")
```

**Or use the helper**:
```python
from scripts.terra_client import get_terra_client

client = get_terra_client("testing")  # or "staging", "production"
```

## Quick Start

### Python SDK Setup
```python
from terra import Terra

# Testing environment
client = Terra(
    dev_id="botaniqalmedtech-testing-SjyfjtG33s",
    api_key="_W7Pm-kAaIf1GA_Se21NnzCaFZjg3Izc"
)

# Verify connection
integrations = client.integrations.fetch()
print(f"Connected! {len(integrations.integrations)} providers available")
```

### Environment Variables
```bash
# .env.testing
TERRA_DEV_ID=botaniqalmedtech-testing-SjyfjtG33s
TERRA_API_KEY=_W7Pm-kAaIf1GA_Se21NnzCaFZjg3Izc

# .env.staging
TERRA_DEV_ID=botaniqalmedtech-staging-uGKHOPRCi1
TERRA_API_KEY=fJia30spa-EqB_CMqZBzzrkMWZ_u2pv_

# .env.production
TERRA_DEV_ID=botaniqalmedtech-prod-yrc99AwsT2
TERRA_API_KEY=Il4YUTc-e00EcvKGUx63j7YE3MJ-7QIz
```

## Operations

### `setup-environment`
Configure Terra credentials for specific environment.

**Python**:
```python
import os
from terra import Terra

def get_terra_client(env: str = "testing") -> Terra:
    """Get Terra client for specified environment."""
    configs = {
        "testing": {
            "dev_id": "botaniqalmedtech-testing-SjyfjtG33s",
            "api_key": "_W7Pm-kAaIf1GA_Se21NnzCaFZjg3Izc"
        },
        "staging": {
            "dev_id": "botaniqalmedtech-staging-uGKHOPRCi1",
            "api_key": "fJia30spa-EqB_CMqZBzzrkMWZ_u2pv_"
        },
        "production": {
            "dev_id": "botaniqalmedtech-prod-yrc99AwsT2",
            "api_key": "Il4YUTc-e00EcvKGUx63j7YE3MJ-7QIz"
        }
    }

    config = configs.get(env)
    if not config:
        raise ValueError(f"Unknown environment: {env}")

    return Terra(dev_id=config["dev_id"], api_key=config["api_key"])

# Usage
client = get_terra_client("testing")
```

### `generate-widget-session`
Create authentication widget URL for end users.

**Python**:
```python
def generate_widget_session(
    client: Terra,
    reference_id: str,
    success_url: str,
    failure_url: str,
    providers: list[str] = None
) -> str:
    """Generate widget session URL for user authentication."""

    response = client.authentication.generatewidgetsession(
        reference_id=reference_id,
        auth_success_redirect_url=success_url,
        auth_failure_redirect_url=failure_url,
        providers=providers  # Optional: filter providers ["FITBIT", "GARMIN"]
    )

    return response.url

# Usage
widget_url = generate_widget_session(
    client=client,
    reference_id="user_12345",  # Your internal user ID
    success_url="https://app.botaniqal.com/terra/success",
    failure_url="https://app.botaniqal.com/terra/failure"
)
print(f"Redirect user to: {widget_url}")
```

**Response**:
```json
{
  "url": "https://widget.tryterra.co/session/abc123...",
  "session_id": "abc123...",
  "expires_at": "2025-12-05T12:15:00Z"
}
```

### `generate-mobile-token`
Generate authentication token for mobile SDK.

**Python**:
```python
def generate_mobile_token(client: Terra) -> str:
    """Generate token for mobile SDK initialization.

    Note: Token is generated for the account, not per-user.
    Use reference_id in the mobile SDK init to identify users.
    """
    response = client.authentication.generateauthtoken()
    return response.token

# Usage (backend endpoint)
@app.route("/api/terra/mobile-token", methods=["POST"])
@login_required
def get_mobile_token():
    token = generate_mobile_token(client=terra_client)
    # Pass reference_id to mobile SDK, not to token generation
    return jsonify({
        "token": token,
        "reference_id": str(current_user.id)  # For SDK init
    })
```

**Token Expiration**: 180 seconds (3 minutes), one-time use.

### `deauthenticate-user`
Remove user and revoke data access.

**Python**:
```python
def deauthenticate_user(client: Terra, user_id: str) -> bool:
    """Deauthenticate user and remove their data."""

    response = client.authentication.deauthenticateuser(user_id=user_id)
    return response.success

# Usage
success = deauthenticate_user(client, "terra_user_abc123")
if success:
    print("User deauthenticated successfully")
```

### `list-integrations`
Get all available provider integrations.

**Python**:
```python
def list_integrations(client: Terra) -> list:
    """List all available Terra integrations."""

    response = client.integrations.fetch()

    integrations = []
    for integration in response.integrations:
        integrations.append({
            "name": integration.name,
            "resource": integration.resource,
            "logo_url": integration.logo_url
        })

    return integrations

# Usage
providers = list_integrations(client)
for p in providers:
    print(f"{p['name']}: {p['resource']}")
```

## REST API Headers

All REST API calls require these headers:
```
dev-id: <YOUR_DEV_ID>
x-api-key: <YOUR_API_KEY>
Content-Type: application/json
```

**cURL Example**:
```bash
curl -X GET "https://api.tryterra.co/v2/integrations" \
  -H "dev-id: botaniqalmedtech-testing-SjyfjtG33s" \
  -H "x-api-key: _W7Pm-kAaIf1GA_Se21NnzCaFZjg3Izc"
```

## Security Best Practices

1. **Never expose API keys in frontend/mobile apps**
2. **Use environment variables** for credentials
3. **Generate mobile tokens on backend** only
4. **Use HTTPS** for all redirect URLs
5. **Rotate keys** if compromised (contact Terra support)
6. **Different keys per environment** (testing/staging/production)

## Webhook Signing Secret

Each environment has a unique signing secret for webhook verification:
- Found in Terra Dashboard → Destinations → Webhooks
- Used for HMAC-SHA256 signature verification
- See `terra-webhooks` skill for implementation

## Session Lifecycle

| Token Type | Expiration | Notes |
|------------|------------|-------|
| Widget Session | 15 minutes | URL valid until used or expired |
| Mobile SDK Token | 3 minutes | One-time use, generate per connection |
| OAuth Tokens | Auto-refresh | Terra manages automatically |
| API Keys | Never | Rotate manually if needed |

## API Base URLs

| Environment | Base URL |
|-------------|----------|
| Production API | `https://api.tryterra.co` |
| Widget | `https://widget.tryterra.co` |
| Streaming | `wss://streaming.tryterra.co` |

## Related Skills

- **terra-connections**: Connect users to wearables
- **terra-data**: Retrieve health data
- **terra-webhooks**: Handle real-time events
- **terra-sdk**: SDK integration patterns
