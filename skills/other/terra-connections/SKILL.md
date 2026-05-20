---
name: terra-connections
description: Terra API device and provider connections. Use when connecting users to wearables (Fitbit, Garmin, Apple Health, Oura, WHOOP), managing user sessions, or handling disconnections.
---

# Terra Connections

Connect users to 150+ wearable devices and health data providers.

## Supported Providers (150+)

### Wearables & Fitness Trackers
- **Garmin** - All models, full historical data
- **Fitbit** - All devices, nutrition support
- **Apple Health** - iOS SDK required
- **Oura Ring** - Sleep, readiness, activity
- **WHOOP** - Recovery, strain, sleep
- **Polar** - Training, sleep, activity
- **Withings** - Watches, scales, blood pressure
- **Samsung Health** - Android SDK required
- **Google Fit / Health Connect** - Android SDK required
- **Suunto, Coros, Biostrap, Zepp** - Full support

### Nutrition Apps
- **MyFitnessPal** - Food logging, macros
- **Cronometer** - Detailed nutrition
- **MacrosFirst, FatSecret** - Meal tracking

### Medical Devices
- **Freestyle Libre** - CGM glucose data
- **Dexcom** - CGM glucose (special process)
- **Omron** - Blood pressure monitors

## Connection Methods

### Method 1: Widget Flow (Recommended)

Pre-built UI, easiest integration:

```python
from terra import Terra

client = Terra(
    dev_id=os.environ["TERRA_DEV_ID"],
    api_key=os.environ["TERRA_API_KEY"]
)

# Generate widget session
response = client.authentication.generatewidgetsession(
    reference_id="user_12345",  # Your internal user ID
    auth_success_redirect_url="https://app.botaniqal.com/success",
    auth_failure_redirect_url="https://app.botaniqal.com/failure",
    providers=["FITBIT", "GARMIN", "OURA"]  # Optional: filter providers
)

widget_url = response.url
# Redirect user to widget_url
```

**User Flow**:
1. User visits widget URL
2. Selects provider (Fitbit, Garmin, etc.)
3. Completes OAuth with provider
4. Redirected to success URL
5. Webhook sent to your endpoint with `type: "auth"`

### Method 2: Custom UI Flow

Build your own provider selection UI:

```python
# Step 1: Get available integrations
integrations = client.integrations.fetch()
# Display provider list in your UI

# Step 2: User selects provider, generate auth URL
response = client.authentication.authenticateuser(
    resource="FITBIT",  # Provider selected by user
    reference_id="user_12345"
)

auth_url = response.auth_url
# Open auth_url in browser (NOT WebView/iFrame!)
```

**Important**: Always open auth URLs in a real browser, not WebView or iFrame (OAuth security requirement).

### Method 3: Mobile SDK (Required for Apple/Samsung/Health Connect)

These sources have no web API - mobile SDK required:

**iOS (Swift) - Apple Health**:
```swift
import TerraiOS

// 1. Get token from your backend
let token = await fetchTerraToken()

// 2. Initialize Terra
Terra.initTerra(devId: "botaniqalmedtech-testing-SjyfjtG33s", referenceId: "user_12345")

// 3. Connect to Apple Health
Terra.initConnection(
    type: Connections.APPLE_HEALTH,
    token: token,
    schedulerOn: true  // Enable background sync
) { success, error in
    if success {
        print("Connected to Apple Health!")
    }
}
```

**Android (Kotlin) - Samsung Health / Health Connect**:
```kotlin
import co.tryterra.terra.Terra

// 1. Get token from your backend
val token = fetchTerraToken()

// 2. Initialize Terra (minSDK 28 required)
Terra.initTerra(
    devId = "botaniqalmedtech-testing-SjyfjtG33s",
    referenceId = "user_12345",
    context = this
)

// 3. Connect to Samsung Health or Health Connect
Terra.initConnection(
    connection = Connections.SAMSUNG,  // or Connections.HEALTH_CONNECT
    token = token,
    context = this,
    schedulerOn = true
) { success ->
    if (success) {
        println("Connected to Samsung Health!")
    }
}
```

**React Native**:
```javascript
import { Terra, Connections } from "terra-react";

// Initialize
Terra.initTerra("botaniqalmedtech-testing-SjyfjtG33s", "user_12345");

// Connect (iOS: Apple Health, Android: Samsung/Health Connect)
await Terra.initConnection(
    Connections.APPLE_HEALTH,
    authToken,
    true  // schedulerOn for background sync
);
```

## Operations

### `connect-user`
Connect a user to a wearable provider.

```python
def connect_user(
    client: Terra,
    reference_id: str,
    provider: str = None,
    success_url: str = None,
    failure_url: str = None
) -> dict:
    """
    Connect user to wearable provider.

    Args:
        reference_id: Your internal user ID
        provider: Specific provider or None for widget with all
        success_url: Redirect URL on success
        failure_url: Redirect URL on failure

    Returns:
        dict with url and session_id
    """
    if provider:
        # Custom UI flow - specific provider
        response = client.authentication.authenticateuser(
            resource=provider,
            reference_id=reference_id
        )
        return {"url": response.auth_url, "type": "direct"}
    else:
        # Widget flow - user selects provider
        response = client.authentication.generatewidgetsession(
            reference_id=reference_id,
            auth_success_redirect_url=success_url,
            auth_failure_redirect_url=failure_url
        )
        return {
            "url": response.url,
            "session_id": response.session_id,
            "type": "widget"
        }
```

### `disconnect-user`
Disconnect user and remove their data.

```python
def disconnect_user(client: Terra, terra_user_id: str) -> bool:
    """
    Disconnect user from Terra (revokes access, removes data).

    Args:
        terra_user_id: Terra's user ID (not your reference_id)

    Returns:
        bool: Success status
    """
    response = client.authentication.deauthenticateuser(user_id=terra_user_id)
    return response.success
```

### `get-user-info`
Get user's connection status and details.

```python
def get_user_info(client: Terra, terra_user_id: str) -> dict:
    """Get information about a connected user."""

    response = client.user.getuser(user_id=terra_user_id)

    return {
        "user_id": response.user.user_id,
        "provider": response.user.provider,
        "reference_id": response.user.reference_id,
        "scopes": response.user.scopes,
        "last_webhook_update": response.user.last_webhook_update
    }
```

### `list-connected-users`
Get all users connected to your app.

```python
def list_connected_users(client: Terra) -> list:
    """List all connected Terra users."""

    response = client.user.getsubscriptions()

    users = []
    for user in response.users:
        users.append({
            "user_id": user.user_id,
            "provider": user.provider,
            "reference_id": user.reference_id,
            "last_update": user.last_webhook_update
        })

    return users
```

### `get-users-by-reference`
Find Terra users by your internal reference ID.

```python
def get_users_by_reference(client: Terra, reference_id: str) -> list:
    """
    Get all Terra users for a reference_id.
    (One person can have multiple providers connected)
    """

    response = client.user.getuser(reference_id=reference_id)

    return response.users  # List of TerraUser objects
```

## Multi-Device Setup

One user can connect multiple wearables:

```python
# User connects Fitbit
connect_user(client, "user_123", provider="FITBIT")

# Same user connects Oura Ring
connect_user(client, "user_123", provider="OURA")

# Get all connections for user
users = get_users_by_reference(client, "user_123")
# Returns: [TerraUser(provider="FITBIT"), TerraUser(provider="OURA")]
```

**Each provider creates a separate Terra User ID**, but all share the same `reference_id`.

## Provider-Specific Notes

### Apple Health (iOS)
- **Requires**: Mobile SDK, iOS 13+
- **No web API**: Must use native app
- **Background sync**: Enable `schedulerOn: true`
- **Permissions**: Request during connection

### Samsung Health / Health Connect (Android)
- **Requires**: Mobile SDK, minSDK 28
- **Health Connect**: Google's unified health API
- **Samsung specific**: Uses Samsung Health SDK

### WHOOP
- **Special process**: Contact Terra for activation
- **Data**: Recovery, strain, sleep, HRV

### Dexcom (CGM)
- **Special process**: Contact Terra for activation
- **Data**: Continuous glucose monitoring

### Freestyle Libre (EU)
- **Dedicated API keys**: Required for EU
- **Data**: CGM glucose readings

### Strava
- **Dedicated API keys**: Required
- **Data**: Activities, routes

## Webhook Events for Connections

When user connects/disconnects, you receive webhooks:

**Connection Success** (`type: "auth"`):
```json
{
  "type": "auth",
  "user": {
    "user_id": "terra_abc123",
    "provider": "FITBIT",
    "reference_id": "user_12345"
  },
  "status": "authenticated"
}
```

**Disconnection** (`type: "deauth"`):
```json
{
  "type": "deauth",
  "user": {
    "user_id": "terra_abc123",
    "provider": "FITBIT"
  },
  "status": "deauthenticated"
}
```

**Connection Error** (`type: "connection_error"`):
```json
{
  "type": "connection_error",
  "user": {
    "user_id": "terra_abc123",
    "provider": "FITBIT"
  },
  "message": "Token refresh failed"
}
```

## Database Schema Recommendation

```sql
CREATE TABLE terra_connections (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),  -- Your user
    terra_user_id VARCHAR(255) UNIQUE,     -- Terra's user ID
    provider VARCHAR(50),                   -- FITBIT, GARMIN, etc.
    reference_id VARCHAR(255),              -- Your reference ID
    connected_at TIMESTAMP DEFAULT NOW(),
    last_sync TIMESTAMP,
    status VARCHAR(20) DEFAULT 'active',    -- active, disconnected
    scopes TEXT[]                           -- Granted permissions
);

CREATE INDEX idx_terra_user ON terra_connections(user_id);
CREATE INDEX idx_terra_reference ON terra_connections(reference_id);
```

## Related Skills

- **terra-auth**: Authentication and credentials
- **terra-data**: Retrieve health data
- **terra-webhooks**: Handle connection events
- **terra-sdk**: Mobile SDK integration
