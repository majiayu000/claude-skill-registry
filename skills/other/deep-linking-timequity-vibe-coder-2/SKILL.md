---
name: deep-linking
description: Universal Links, App Links, and URL scheme configuration.
---

# Deep Linking

## URL Schemes

```json
// app.json
{
  "expo": {
    "scheme": "myapp"
  }
}
```

```typescript
// Handle myapp://path
import * as Linking from 'expo-linking';

const url = Linking.createURL('path/to/screen', {
  queryParams: { id: '123' },
});
// myapp://path/to/screen?id=123
```

## Universal Links (iOS)

```json
// app.json
{
  "expo": {
    "ios": {
      "associatedDomains": ["applinks:example.com"]
    }
  }
}
```

```json
// /.well-known/apple-app-site-association
{
  "applinks": {
    "apps": [],
    "details": [
      {
        "appID": "TEAM_ID.com.example.app",
        "paths": ["/product/*", "/user/*"]
      }
    ]
  }
}
```

## App Links (Android)

```json
// app.json
{
  "expo": {
    "android": {
      "intentFilters": [
        {
          "action": "VIEW",
          "autoVerify": true,
          "data": [
            {
              "scheme": "https",
              "host": "example.com",
              "pathPrefix": "/product"
            }
          ],
          "category": ["BROWSABLE", "DEFAULT"]
        }
      ]
    }
  }
}
```

```json
// /.well-known/assetlinks.json
[{
  "relation": ["delegate_permission/common.handle_all_urls"],
  "target": {
    "namespace": "android_app",
    "package_name": "com.example.app",
    "sha256_cert_fingerprints": ["..."]
  }
}]
```

## Expo Router

```typescript
// app/_layout.tsx
export default function Layout() {
  return (
    <Stack>
      <Stack.Screen name="product/[id]" />
    </Stack>
  );
}

// app/product/[id].tsx
export default function ProductScreen() {
  const { id } = useLocalSearchParams();
  // https://example.com/product/123 -> id = "123"
}
```

## Testing

```bash
# iOS Simulator
xcrun simctl openurl booted "myapp://product/123"

# Android Emulator
adb shell am start -a android.intent.action.VIEW -d "myapp://product/123"
```
