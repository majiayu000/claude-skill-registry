---
name: terra-sdk
description: Terra SDK integration for Python, JavaScript, iOS, Android, React Native, and Flutter. Use when implementing Terra in applications, choosing SDKs, or integrating mobile health sources.
---

# Terra SDK Integration

Complete SDK reference for Terra API integration across all platforms.

## SDK Overview

| SDK | Platform | Package | Use Case |
|-----|----------|---------|----------|
| **Python** | Backend | `terra-python` | Server-side API calls |
| **JavaScript** | Backend/Node | `terra-api` | Node.js, Deno, Bun |
| **iOS** | Mobile | `TerraiOS` | Apple Health integration |
| **Android** | Mobile | `terra-android` | Samsung Health, Health Connect |
| **React Native** | Mobile | `terra-react` | Cross-platform mobile |
| **Flutter** | Mobile | `terra_flutter` | Cross-platform mobile |

## Python SDK

### Installation
```bash
pip install terra-python
```

### Setup
```python
from terra import Terra, AsyncTerra

# Synchronous client
client = Terra(
    dev_id=os.environ["TERRA_DEV_ID"],
    api_key=os.environ["TERRA_API_KEY"]
)

# Async client
async_client = AsyncTerra(
    dev_id=os.environ["TERRA_DEV_ID"],
    api_key=os.environ["TERRA_API_KEY"]
)
```

### Configuration Options
```python
from terra import Terra

client = Terra(
    dev_id="...",
    api_key="...",
    timeout=60.0,           # Request timeout in seconds
    max_retries=2,          # Automatic retries (default: 2)
)
```

### Complete Method Reference

```python
# Authentication
client.authentication.generatewidgetsession(reference_id=..., auth_success_redirect_url=..., ...)
client.authentication.generateauthtoken()  # No params, generates for account
client.authentication.authenticateuser(resource=..., reference_id=...)
client.authentication.deauthenticateuser(user_id=...)

# User Management
client.user.getinfoforuserid(user_id=None, reference_id=None)  # Get single user
client.user.getalluserids(page=None, per_page=None)  # List all connected users
client.user.getinfoformultipleuserids(user_ids=...)  # Bulk user info
client.user.modifyuser(user_id=..., ...)  # Update user

# Data Retrieval (use .fetch() method)
client.activity.fetch(user_id=..., start_date=..., end_date=..., to_webhook=False)
client.sleep.fetch(user_id=..., start_date=..., end_date=..., to_webhook=False)
client.daily.fetch(user_id=..., start_date=..., end_date=..., to_webhook=False)
client.body.fetch(user_id=..., start_date=..., end_date=..., to_webhook=False)
client.nutrition.fetch(user_id=..., start_date=..., end_date=..., to_webhook=False)
client.menstruation.fetch(user_id=..., start_date=..., end_date=..., to_webhook=False)
client.athlete.fetch(user_id=...)

# Integrations
client.integrations.fetch()  # Basic list
client.integrations.detailedfetch()  # With detailed info

# Data Writing (limited providers)
client.activity.write(user_id=..., data=...)
client.nutrition.write(user_id=..., data=...)
client.body.write(user_id=..., data=...)
```

### Async Usage
```python
import asyncio
from terra import AsyncTerra

async def main():
    client = AsyncTerra(dev_id="...", api_key="...")

    # Concurrent requests
    activity, sleep, daily = await asyncio.gather(
        client.activity.get(user_id, start, end),
        client.sleep.get(user_id, start, end),
        client.daily.get(user_id, start, end)
    )

    return activity.data, sleep.data, daily.data

asyncio.run(main())
```

### Error Handling
```python
from terra import Terra
from terra.core.api_error import ApiError

client = Terra(dev_id="...", api_key="...")

try:
    data = client.activity.get(user_id="invalid", start_date=start, end_date=end)
except ApiError as e:
    print(f"Status: {e.status_code}")
    print(f"Message: {e.message}")
    print(f"Body: {e.body}")
```

## JavaScript/Node.js SDK

### Installation
```bash
npm install terra-api
# or
yarn add terra-api
```

### Setup
```javascript
import { TerraClient } from "terra-api";

const client = new TerraClient({
    apiKey: process.env.TERRA_API_KEY,
    devId: process.env.TERRA_DEV_ID
});
```

### TypeScript Support
```typescript
import { TerraClient, TerraError } from "terra-api";

const client = new TerraClient({
    apiKey: string,
    devId: string,
    timeout?: number,
    maxRetries?: number
});
```

### Complete Method Reference
```javascript
// Authentication
await client.authentication.generateWidgetSession({ referenceId, authSuccessRedirectUrl, ... });
await client.authentication.generateAuthToken({ referenceId });
await client.authentication.authenticateUser({ resource, referenceId });
await client.authentication.deauthenticateUser({ userId });

// User Management
await client.user.getUser({ userId });
await client.user.getSubscriptions();

// Data Retrieval
await client.activity.get({ userId, startDate, endDate, toWebhook });
await client.sleep.get({ userId, startDate, endDate, toWebhook });
await client.daily.get({ userId, startDate, endDate, toWebhook });
await client.body.get({ userId, startDate, endDate, toWebhook });
await client.nutrition.get({ userId, startDate, endDate, toWebhook });

// Integrations
await client.integrations.fetch();
```

### Error Handling
```javascript
import { TerraClient, TerraError } from "terra-api";

try {
    const data = await client.activity.get({ userId: "...", startDate, endDate });
} catch (error) {
    if (error instanceof TerraError) {
        console.log(error.statusCode);
        console.log(error.message);
        console.log(error.body);
    }
}
```

### Abort Requests
```javascript
const controller = new AbortController();

const promise = client.activity.get(
    { userId, startDate, endDate },
    { abortSignal: controller.signal }
);

// Cancel if needed
controller.abort();
```

## iOS SDK (Swift)

### Installation

**Swift Package Manager**:
```
https://github.com/tryterra/TerraiOS
```

**CocoaPods**:
```ruby
pod 'TerraiOS'
```

### Setup
```swift
import TerraiOS

class HealthManager {

    func initialize() {
        Terra.initTerra(
            devId: "botaniqalmedtech-testing-SjyfjtG33s",
            referenceId: getCurrentUserId()
        )
    }

    func connectAppleHealth(token: String) {
        Terra.initConnection(
            type: Connections.APPLE_HEALTH,
            token: token,
            schedulerOn: true  // Enable background sync
        ) { success, error in
            if success {
                print("Connected to Apple Health!")
            } else {
                print("Connection failed: \(error?.localizedDescription ?? "Unknown")")
            }
        }
    }
}
```

### Reading Data
```swift
import TerraiOS

// Get activity data
Terra.getActivity(
    startDate: Calendar.current.date(byAdding: .day, value: -7, to: Date())!,
    endDate: Date()
) { success, data, error in
    if success, let activities = data {
        for activity in activities {
            print("Activity: \(activity.metadata.type)")
            print("Calories: \(activity.calories_data.total_burned_calories)")
        }
    }
}

// Get sleep data
Terra.getSleep(startDate: startDate, endDate: endDate) { success, data, error in
    // Handle sleep data
}

// Get daily data
Terra.getDaily(startDate: startDate, endDate: endDate) { success, data, error in
    // Handle daily summaries
}
```

### Writing Data (Apple Health)
```swift
// Post activity
Terra.postActivity(data: activityData) { success, error in
    if success {
        print("Activity posted to Apple Health")
    }
}

// Post planned workout (appears in Workout app)
let workout = PlannedWorkout(
    name: "Morning Run",
    type: "running",
    phases: [
        WorkoutPhase(type: "warmup", duration: 300),
        WorkoutPhase(type: "active", duration: 1800),
        WorkoutPhase(type: "cooldown", duration: 300)
    ]
)
Terra.postPlannedWorkout(data: workout) { success, error in
    // Workout now available on Apple Watch
}
```

### Background Delivery
```swift
// Enable background delivery in AppDelegate
func application(_ application: UIApplication, didFinishLaunchingWithOptions...) {
    Terra.setUpBackgroundDelivery()
}

// Data syncs automatically in background when schedulerOn: true
```

## Android SDK (Kotlin)

### Installation

**build.gradle**:
```gradle
dependencies {
    implementation 'co.tryterra:terra-android:VERSION'
}
```

**Requirements**: minSDK 28 (Android 9.0+)

### Setup
```kotlin
import co.tryterra.terra.Terra
import co.tryterra.terra.Connections

class HealthManager(private val context: Context) {

    fun initialize() {
        Terra.initTerra(
            devId = "botaniqalmedtech-testing-SjyfjtG33s",
            referenceId = getCurrentUserId(),
            context = context
        )
    }

    fun connectSamsungHealth(token: String) {
        Terra.initConnection(
            connection = Connections.SAMSUNG,
            token = token,
            context = context,
            schedulerOn = true
        ) { success ->
            if (success) {
                println("Connected to Samsung Health!")
            }
        }
    }

    fun connectHealthConnect(token: String) {
        Terra.initConnection(
            connection = Connections.HEALTH_CONNECT,
            token = token,
            context = context,
            schedulerOn = true
        ) { success ->
            if (success) {
                println("Connected to Health Connect!")
            }
        }
    }
}
```

### Reading Data
```kotlin
// Get activity
Terra.getActivity(startDate, endDate) { success, data ->
    if (success) {
        data?.forEach { activity ->
            println("Activity: ${activity.metadata.type}")
            println("Calories: ${activity.caloriesData.totalBurnedCalories}")
        }
    }
}

// Get sleep
Terra.getSleep(startDate, endDate) { success, data ->
    // Handle sleep data
}

// Get daily
Terra.getDaily(startDate, endDate) { success, data ->
    // Handle daily summaries
}
```

### Permissions
```xml
<!-- AndroidManifest.xml -->
<uses-permission android:name="android.permission.ACTIVITY_RECOGNITION"/>
<uses-permission android:name="android.permission.BODY_SENSORS"/>
```

## React Native SDK

### Installation
```bash
npm install terra-react
# or
yarn add terra-react

# iOS: pod install
cd ios && pod install
```

### Setup
```javascript
import { Terra, Connections } from "terra-react";

// Initialize
Terra.initTerra(
    "botaniqalmedtech-testing-SjyfjtG33s",
    getCurrentUserId()
);
```

### Connecting Sources
```javascript
// Get auth token from your backend
const token = await fetchTerraToken();

// Connect (auto-detects platform)
const connection = Platform.OS === 'ios'
    ? Connections.APPLE_HEALTH
    : Connections.HEALTH_CONNECT;

await Terra.initConnection(
    connection,
    token,
    true  // schedulerOn for background sync
);
```

### Reading Data
```javascript
import { Terra } from "terra-react";

// Get activity
const activities = await Terra.getActivity(startDate, endDate);
activities.forEach(activity => {
    console.log(`Type: ${activity.metadata.type}`);
    console.log(`Calories: ${activity.calories_data.total_burned_calories}`);
});

// Get sleep
const sleepData = await Terra.getSleep(startDate, endDate);

// Get daily
const dailyData = await Terra.getDaily(startDate, endDate);

// Get body
const bodyData = await Terra.getBody(startDate, endDate);
```

### Writing Data
```javascript
// Post activity
await Terra.postActivity(activityData);

// Post nutrition
await Terra.postNutrition(nutritionData);

// Post body metrics
await Terra.postBody(bodyData);
```

## Flutter SDK

### Installation

**pubspec.yaml**:
```yaml
dependencies:
  terra_flutter: ^VERSION
```

### Setup
```dart
import 'package:terra_flutter/terra_flutter.dart';

class HealthManager {
  late Terra terra;

  void initialize() {
    terra = Terra(
      "botaniqalmedtech-testing-SjyfjtG33s",
      getCurrentUserId()
    );
  }

  Future<void> connectAppleHealth(String token) async {
    await terra.initConnection(
      Connections.APPLE_HEALTH,
      token,
      schedulerOn: true
    );
  }
}
```

### Reading Data
```dart
// Get activity
final activities = await terra.getActivity(startDate, endDate);
for (var activity in activities) {
  print("Type: ${activity.metadata.type}");
  print("Calories: ${activity.caloriesData.totalBurnedCalories}");
}

// Get sleep
final sleepData = await terra.getSleep(startDate, endDate);

// Get daily
final dailyData = await terra.getDaily(startDate, endDate);
```

### Writing Data
```dart
// Post activity
await terra.postActivity(activityData);

// Post nutrition
await terra.postNutrition(nutritionData);
```

## Backend Token Generation

Mobile SDKs require backend token generation:

```python
# Flask example
from flask import Flask, jsonify
from flask_login import login_required, current_user
from terra import Terra

app = Flask(__name__)
terra = Terra(dev_id="...", api_key="...")

@app.route("/api/terra/token", methods=["POST"])
@login_required
def get_terra_token():
    """Generate auth token for mobile SDK."""
    response = terra.authentication.generateauthtoken(
        reference_id=str(current_user.id)
    )
    return jsonify({"token": response.token})
```

**Token Expiration**: 180 seconds (3 minutes), one-time use.

## SDK Comparison

| Feature | Python | JavaScript | iOS | Android | React Native | Flutter |
|---------|--------|------------|-----|---------|--------------|---------|
| Async support | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Auto retries | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Type safety | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ |
| Background sync | N/A | N/A | ✅ | ✅ | ✅ | ✅ |
| Write data | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

## When to Use Each SDK

| Scenario | Recommended SDK |
|----------|-----------------|
| Backend API calls | Python or JavaScript |
| iOS app with Apple Health | iOS SDK (Swift) |
| Android app | Android SDK (Kotlin) |
| Cross-platform mobile | React Native or Flutter |
| Serverless (Lambda, etc.) | JavaScript |
| Data processing | Python (with async) |

## Related Skills

- **terra-auth**: Credential management
- **terra-connections**: Connection flows
- **terra-data**: Data retrieval details
- **terra-webhooks**: Event handling
