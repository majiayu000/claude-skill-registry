---
name: terra-troubleshooting
description: Terra API troubleshooting and debugging. Use when experiencing connection issues, data sync problems, webhook failures, SDK errors, or provider-specific issues.
---

# Terra Troubleshooting

Diagnose and resolve common Terra API issues.

## Quick Diagnostics

```python
from terra import Terra

def check_terra_health(client: Terra) -> dict:
    """Run basic health checks."""
    results = {}

    # 1. API connectivity
    try:
        integrations = client.integrations.fetch()
        results["api_connection"] = f"OK - {len(integrations.integrations)} providers"
    except Exception as e:
        results["api_connection"] = f"FAILED - {e}"

    # 2. List connected users
    try:
        users = client.user.getsubscriptions()
        results["connected_users"] = f"OK - {len(users.users)} users"
    except Exception as e:
        results["connected_users"] = f"FAILED - {e}"

    return results

# Usage
client = Terra(dev_id="...", api_key="...")
print(check_terra_health(client))
```

## Common Issues

### Authentication Issues

#### "Invalid API key or dev-id"
**Cause**: Incorrect credentials or wrong environment.

**Solution**:
```python
# Check you're using correct environment credentials
ENVIRONMENTS = {
    "testing": {
        "dev_id": os.environ.get("TERRA_DEV_ID_TESTING"),
        "api_key": os.environ.get("TERRA_API_KEY_TESTING")
    },
    "staging": {
        "dev_id": os.environ.get("TERRA_DEV_ID_STAGING"),
        "api_key": os.environ.get("TERRA_API_KEY_STAGING")
    },
    "production": {
        "dev_id": os.environ.get("TERRA_DEV_ID_PRODUCTION"),
        "api_key": os.environ.get("TERRA_API_KEY_PRODUCTION")
    }
}

# Verify connection
from terra import Terra
client = Terra(**ENVIRONMENTS["testing"])
print(client.integrations.fetch())
```

#### Widget session expired
**Cause**: Session URLs expire after 15 minutes.

**Solution**: Generate a new widget session:
```python
response = client.authentication.generatewidgetsession(
    reference_id="user_123",
    auth_success_redirect_url="https://app.example.com/success",
    auth_failure_redirect_url="https://app.example.com/failure"
)
# Redirect user to response.url immediately
```

#### Mobile SDK token invalid
**Cause**: Token expired (3 min) or already used.

**Solution**: Generate fresh token for each connection attempt:
```python
# Backend generates new token each time
token = client.authentication.generateauthtoken(reference_id="user_123")
# Send token.token to mobile app
# Token is one-time use - generate new one if connection fails
```

### Connection Issues

#### User stuck on "connecting"
**Cause**: OAuth flow interrupted or WebView used.

**Solution**:
1. **Never use WebView/iFrame** for OAuth
2. Open auth URL in real browser
3. Handle redirects properly:

```javascript
// Wrong - WebView blocks OAuth
<WebView source={{ uri: authUrl }} />

// Correct - Open in browser
import { Linking } from 'react-native';
Linking.openURL(authUrl);

// Or use InAppBrowser
import { InAppBrowser } from 'react-native-inappbrowser-reborn';
InAppBrowser.open(authUrl);
```

#### Provider returns "Access Denied"
**Cause**: Provider-side issue or insufficient permissions.

**Solution**:
```python
# Check user's granted scopes
user = client.user.getuser(user_id="terra_abc123")
print(f"Scopes: {user.user.scopes}")

# If missing scopes, user needs to reconnect and grant all permissions
```

#### WHOOP / Dexcom connection fails
**Cause**: These require special activation.

**Solution**: Contact Terra support at [email protected] for:
- WHOOP access activation
- Dexcom (CGM) access activation
- Freestyle Libre EU dedicated API keys
- Strava dedicated API keys

### Data Sync Issues

#### No data received
**Causes**:
1. User just connected (data takes time to sync)
2. User has no data in that date range
3. Provider is "polled" type (5-min delay)

**Solution**:
```python
from datetime import datetime, timedelta

def check_user_data(client: Terra, user_id: str) -> dict:
    """Check if user has any data."""
    end = datetime.now()
    start = end - timedelta(days=7)

    results = {}

    # Check each data type
    for data_type in ["daily", "activity", "sleep", "body"]:
        try:
            method = getattr(client, data_type)
            response = method.get(user_id=user_id, start_date=start, end_date=end)
            results[data_type] = len(response.data)
        except Exception as e:
            results[data_type] = f"Error: {e}"

    return results

print(check_user_data(client, "terra_abc123"))
```

#### Duplicate data received
**Cause**: Daily/body data updates multiple times per day.

**Solution**: Use UPSERT pattern, not INSERT:
```python
# Wrong - creates duplicates
db.insert(data)

# Correct - overwrites existing
db.upsert(
    {"user_id": user_id, "date": date},
    {"$set": data}
)
```

#### Historical data missing
**Cause**: Provider limits historical access.

**Reference** - Maximum historical data per provider:

| Provider | Limit |
|----------|-------|
| Garmin | 5 years |
| Fitbit | 10 years |
| Oura | 3 years |
| WHOOP | 2 years |
| Polar | 30 days |
| COROS | 3 months |

### Webhook Issues

#### Webhooks not received
**Checklist**:

1. **Check webhook configured in dashboard**:
   - Terra Dashboard → Destinations → Webhooks
   - Verify URL is correct and HTTPS

2. **Check endpoint is accessible**:
   ```bash
   curl -X POST https://your-webhook-url.com/terra \
     -H "Content-Type: application/json" \
     -d '{"type": "test"}'
   ```

3. **Check server logs** for incoming requests

4. **Verify IP not blocked** - Terra IPs:
   ```
   18.133.218.210, 18.169.82.189, 18.132.162.19,
   18.130.218.186, 13.43.183.154, 3.11.208.36,
   35.214.201.105, 35.214.230.71, 35.214.252.53, 35.214.229.114
   ```

#### Signature verification failing
**Causes**:
1. Wrong signing secret
2. Body modified before verification
3. Incorrect signature algorithm

**Solution**:
```python
import hmac
import hashlib

def debug_signature(header: str, body: bytes, secret: str):
    """Debug signature verification."""

    # Parse header
    parts = dict(p.split("=") for p in header.split(","))
    print(f"Timestamp: {parts['t']}")
    print(f"Received signature: {parts['v1']}")

    # Compute expected
    message = f"{parts['t']}.{body.decode()}"
    expected = hmac.new(secret.encode(), message.encode(), hashlib.sha256).hexdigest()
    print(f"Expected signature: {expected}")

    # Compare
    match = hmac.compare_digest(expected, parts['v1'])
    print(f"Match: {match}")

    return match

# Use in webhook handler
@app.route("/webhook", methods=["POST"])
def webhook():
    header = request.headers.get("terra-signature")
    body = request.get_data()  # Must be raw bytes, not parsed JSON!

    if not debug_signature(header, body, SIGNING_SECRET):
        return "Invalid signature", 401

    # Now parse JSON
    payload = request.get_json()
```

**Critical**: Get raw body BEFORE parsing JSON.

#### Webhook timeouts
**Cause**: Processing takes too long (>5 seconds recommended).

**Solution**: Process asynchronously:
```python
from celery import Celery

celery = Celery()

@app.route("/webhook", methods=["POST"])
def webhook():
    # Verify signature
    # Queue for async processing
    process_webhook.delay(request.get_json())

    # Respond immediately
    return "OK", 200

@celery.task
def process_webhook(payload):
    # Do heavy processing here
    save_to_database(payload)
    send_notifications(payload)
```

### SDK Issues

#### iOS: Apple Health no data
**Causes**:
1. Permissions not granted
2. Background delivery not enabled
3. App not authorized in Health app

**Solution**:
```swift
// 1. Check permissions in code
Terra.checkPermissions { granted in
    if !granted {
        // Request permissions again
        Terra.requestPermissions()
    }
}

// 2. Enable background delivery
func application(_ app: UIApplication, didFinishLaunchingWithOptions...) {
    Terra.setUpBackgroundDelivery()
}

// 3. User must enable in Settings → Privacy → Health → Your App
```

#### Android: Samsung Health fails
**Causes**:
1. Samsung Health app not installed
2. minSDK < 28
3. Missing permissions

**Solution**:
```kotlin
// 1. Check Samsung Health installed
if (!Terra.isSamsungHealthAvailable(context)) {
    // Prompt user to install Samsung Health
    showInstallSamsungHealthDialog()
}

// 2. Verify minSDK in build.gradle
android {
    defaultConfig {
        minSdkVersion 28  // Required for Terra Android SDK
    }
}

// 3. Request permissions
<uses-permission android:name="android.permission.ACTIVITY_RECOGNITION"/>
<uses-permission android:name="android.permission.BODY_SENSORS"/>
```

#### Android: Health Connect issues
**Cause**: Health Connect not installed or configured.

**Solution**:
```kotlin
// Check Health Connect availability
if (!Terra.isHealthConnectAvailable(context)) {
    // Prompt to install Health Connect
    val intent = Intent(Intent.ACTION_VIEW).apply {
        data = Uri.parse("https://play.google.com/store/apps/details?id=com.google.android.apps.healthdata")
    }
    startActivity(intent)
}
```

#### React Native: Build failures
**Common fixes**:

```bash
# iOS: Clean and rebuild
cd ios
pod deintegrate
pod install
cd ..
npx react-native run-ios

# Android: Clean build
cd android
./gradlew clean
cd ..
npx react-native run-android
```

### Provider-Specific Issues

#### MyFitnessPal: Gateway timeout
**Cause**: MyFitnessPal API is slow/unreliable.

**Solution**: Retry with exponential backoff:
```python
import time

def fetch_with_retry(client, user_id, start, end, max_retries=3):
    for attempt in range(max_retries):
        try:
            return client.nutrition.get(user_id, start, end)
        except Exception as e:
            if "timeout" in str(e).lower() and attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # 1, 2, 4 seconds
                continue
            raise
```

#### Garmin: Data delayed
**Cause**: Garmin is a "polled" provider (~5 min sync).

**Solution**: Wait for webhook rather than polling API:
```python
# Don't poll repeatedly
# Instead, wait for webhook notification
```

#### Fitbit: Token revoked
**Cause**: User revoked access in Fitbit app.

**Solution**: Handle `access_revoked` webhook:
```python
def handle_access_revoked(payload):
    user_id = payload["user"]["user_id"]

    # Mark user as disconnected
    db.terra_users.update_one(
        {"terra_user_id": user_id},
        {"$set": {"status": "access_revoked"}}
    )

    # Notify user to reconnect
    send_reconnect_notification(user_id)
```

## Debug Mode

Enable detailed logging:

```python
import logging

# Enable Terra SDK logging
logging.getLogger("terra").setLevel(logging.DEBUG)

# Or enable all HTTP logging
import http.client
http.client.HTTPConnection.debuglevel = 1
```

## Support Escalation

If issues persist:

1. **Check Terra Status**: https://status.tryterra.co
2. **Documentation**: https://docs.tryterra.co
3. **Email Support**: [email protected]
4. **Include in support request**:
   - Dev ID (not API key!)
   - User ID (if applicable)
   - Error message
   - Timestamp of issue
   - Provider affected

## Health Check Script

```python
#!/usr/bin/env python3
"""Terra API health check script."""

from terra import Terra
from datetime import datetime, timedelta

def run_health_check():
    print("=" * 50)
    print("Terra API Health Check")
    print("=" * 50)

    # Test each environment - credentials loaded from env vars
    envs = {
        "testing": (os.environ.get("TERRA_DEV_ID_TESTING"), os.environ.get("TERRA_API_KEY_TESTING")),
        "staging": (os.environ.get("TERRA_DEV_ID_STAGING"), os.environ.get("TERRA_API_KEY_STAGING")),
        "production": (os.environ.get("TERRA_DEV_ID_PRODUCTION"), os.environ.get("TERRA_API_KEY_PRODUCTION")),
    }

    for env_name, (dev_id, api_key) in envs.items():
        print(f"\n{env_name.upper()}:")
        try:
            client = Terra(dev_id=dev_id, api_key=api_key)

            # Check API
            integrations = client.integrations.fetch()
            print(f"  ✅ API Connected - {len(integrations.integrations)} providers")

            # Check users
            users = client.user.getsubscriptions()
            print(f"  ✅ Users: {len(users.users)} connected")

        except Exception as e:
            print(f"  ❌ Error: {e}")

    print("\n" + "=" * 50)
    print("Health check complete")

if __name__ == "__main__":
    run_health_check()
```

## Related Skills

- **terra-auth**: Credential management
- **terra-connections**: Connection flows
- **terra-webhooks**: Webhook handling
- **terra-data**: Data retrieval
- **terra-sdk**: SDK integration
