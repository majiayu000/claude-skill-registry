---
name: openfeature-eng
description: Implement OpenFeature feature flags in software projects. Use when adding feature flags with OpenFeature SDKs, configuring providers, setting up evaluation context, or integrating the OpenFeature MCP Server.
---

# OpenFeature Implementation

Guide for implementing OpenFeature - the open standard for feature flag management - across server and client applications.

## When to Use This Skill

- Adding feature flags to a new or existing project
- Implementing OpenFeature Server SDKs (Go, Java, .NET, Node.js, PHP, Python, Ruby, Rust, Dart)
- Implementing OpenFeature Client SDKs (JavaScript, React, Angular, Kotlin, iOS/Swift)
- Configuring feature flag providers (flagd, LaunchDarkly, Split, etc.)
- Setting up evaluation context for targeting
- Using the OpenFeature MCP Server

**This skill does NOT cover:**
- Creating custom OpenFeature providers (see provider development docs)
- Vendor-specific flag management UIs
- Feature flag strategy/design patterns

## Core Concepts

### OpenFeature Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Application Code                         │
│  client.getBooleanValue("feature-x", false, context)        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    OpenFeature SDK                           │
│  - Evaluation API                                            │
│  - Hooks (before/after/error/finally)                       │
│  - Event handling                                            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Provider                                │
│  flagd | LaunchDarkly | Split | CloudBees | In-Memory       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Flag Management                            │
│  Flag definitions, rules, segments, rollouts                │
└─────────────────────────────────────────────────────────────┘
```

### Key Terms

| Term | Description |
|------|-------------|
| **Provider** | Backend that evaluates flags (flagd, LaunchDarkly, etc.) |
| **Client** | SDK instance for evaluating flags |
| **Context** | User/request attributes for targeting |
| **Hook** | Lifecycle callbacks for logging, metrics |
| **Flag** | Feature toggle with key, type, and default value |

## Server SDK Implementations

### Go

```bash
go get github.com/open-feature/go-sdk
```

```go
package main

import (
    "context"
    "github.com/open-feature/go-sdk/openfeature"
    "github.com/open-feature/go-sdk-contrib/providers/flagd/pkg"
)

func main() {
    // Set up provider
    provider := flagd.NewProvider()
    openfeature.SetProvider(provider)

    // Get client
    client := openfeature.NewClient("my-app")

    // Evaluation context
    ctx := openfeature.NewEvaluationContext(
        "user-123",
        map[string]interface{}{
            "email": "user@example.com",
            "tier":  "premium",
        },
    )

    // Evaluate flags
    enabled, _ := client.BooleanValue(
        context.Background(),
        "new-feature",
        false,
        ctx,
    )

    if enabled {
        // New feature code
    }
}
```

### Java

```xml
<dependency>
    <groupId>dev.openfeature</groupId>
    <artifactId>sdk</artifactId>
    <version>1.7.0</version>
</dependency>
```

```java
import dev.openfeature.sdk.*;
import dev.openfeature.contrib.providers.flagd.FlagdProvider;

public class FeatureFlags {
    public static void main(String[] args) {
        // Set provider
        OpenFeatureAPI api = OpenFeatureAPI.getInstance();
        api.setProvider(new FlagdProvider());

        // Get client
        Client client = api.getClient("my-app");

        // Evaluation context
        EvaluationContext ctx = new ImmutableContext("user-123",
            Map.of(
                "email", new Value("user@example.com"),
                "tier", new Value("premium")
            )
        );

        // Evaluate flags
        boolean enabled = client.getBooleanValue("new-feature", false, ctx);

        if (enabled) {
            // New feature code
        }
    }
}
```

### .NET

```bash
dotnet add package OpenFeature
dotnet add package OpenFeature.Contrib.Providers.Flagd
```

```csharp
using OpenFeature;
using OpenFeature.Contrib.Providers.Flagd;

// Set provider
var provider = new FlagdProvider();
await Api.Instance.SetProviderAsync(provider);

// Get client
var client = Api.Instance.GetClient("my-app");

// Evaluation context
var context = EvaluationContext.Builder()
    .SetTargetingKey("user-123")
    .Set("email", "user@example.com")
    .Set("tier", "premium")
    .Build();

// Evaluate flags
var enabled = await client.GetBooleanValueAsync("new-feature", false, context);

if (enabled)
{
    // New feature code
}
```

### Node.js / TypeScript

```bash
npm install @openfeature/server-sdk @openfeature/flagd-provider
```

```typescript
import { OpenFeature } from '@openfeature/server-sdk';
import { FlagdProvider } from '@openfeature/flagd-provider';

// Set provider
await OpenFeature.setProviderAndWait(new FlagdProvider());

// Get client
const client = OpenFeature.getClient('my-app');

// Evaluation context
const context = {
  targetingKey: 'user-123',
  email: 'user@example.com',
  tier: 'premium',
};

// Evaluate flags
const enabled = await client.getBooleanValue('new-feature', false, context);

if (enabled) {
  // New feature code
}
```

### NestJS Integration

```bash
npm install @openfeature/server-sdk @openfeature/nestjs-sdk @openfeature/flagd-provider
```

```typescript
// app.module.ts
import { Module } from '@nestjs/common';
import { OpenFeatureModule } from '@openfeature/nestjs-sdk';
import { FlagdProvider } from '@openfeature/flagd-provider';

@Module({
  imports: [
    OpenFeatureModule.forRoot({
      defaultProvider: new FlagdProvider(),
    }),
  ],
})
export class AppModule {}
```

```typescript
// feature.service.ts
import { Injectable } from '@nestjs/common';
import {
  OpenFeatureClient,
  BooleanFeatureFlag
} from '@openfeature/nestjs-sdk';
import { Client } from '@openfeature/server-sdk';

@Injectable()
export class FeatureService {
  constructor(
    @OpenFeatureClient() private client: Client,
  ) {}

  @BooleanFeatureFlag({
    flagKey: 'new-feature',
    defaultValue: false,
  })
  async isNewFeatureEnabled(): Promise<boolean> {
    return this.client.getBooleanValue('new-feature', false);
  }
}
```

### Python

```bash
pip install openfeature-sdk openfeature-provider-flagd
```

```python
from openfeature import api
from openfeature.evaluation_context import EvaluationContext
from openfeature.contrib.provider.flagd import FlagdProvider

# Set provider
api.set_provider(FlagdProvider())

# Get client
client = api.get_client("my-app")

# Evaluation context
context = EvaluationContext(
    targeting_key="user-123",
    attributes={
        "email": "user@example.com",
        "tier": "premium",
    }
)

# Evaluate flags
enabled = client.get_boolean_value("new-feature", False, context)

if enabled:
    # New feature code
    pass
```

### Ruby

```bash
gem install openfeature-sdk openfeature-flagd-provider
```

```ruby
require 'openfeature/sdk'
require 'openfeature/flagd/provider'

# Set provider
OpenFeature::SDK.configure do |config|
  config.set_provider(OpenFeature::Flagd::Provider.new)
end

# Get client
client = OpenFeature::SDK.build_client(name: 'my-app')

# Evaluation context
context = OpenFeature::SDK::EvaluationContext.new(
  targeting_key: 'user-123',
  email: 'user@example.com',
  tier: 'premium'
)

# Evaluate flags
enabled = client.fetch_boolean_value(
  flag_key: 'new-feature',
  default_value: false,
  evaluation_context: context
)

if enabled
  # New feature code
end
```

### Rust

```toml
[dependencies]
open-feature = "0.2"
```

```rust
use open_feature::{
    provider::NoOpProvider,
    EvaluationContext, OpenFeature,
};

#[tokio::main]
async fn main() {
    // Set provider
    let mut api = OpenFeature::singleton_mut().await;
    api.set_provider(NoOpProvider::default()).await;

    // Get client
    let client = api.create_client();

    // Evaluation context
    let context = EvaluationContext::default()
        .with_targeting_key("user-123")
        .with_custom_field("email", "user@example.com")
        .with_custom_field("tier", "premium");

    // Evaluate flags
    let enabled = client
        .get_bool_value("new-feature", Some(&context), None)
        .await
        .unwrap_or(false);

    if enabled {
        // New feature code
    }
}
```

### Dart

```yaml
dependencies:
  openfeature_dart_sdk: ^0.1.0
```

```dart
import 'package:openfeature_dart_sdk/openfeature_dart_sdk.dart';

void main() async {
  // Set provider
  final api = OpenFeatureAPI.instance;
  await api.setProvider(InMemoryProvider());

  // Get client
  final client = api.getClient('my-app');

  // Evaluation context
  final context = EvaluationContext(
    targetingKey: 'user-123',
    attributes: {
      'email': 'user@example.com',
      'tier': 'premium',
    },
  );

  // Evaluate flags
  final enabled = await client.getBooleanValue(
    'new-feature',
    defaultValue: false,
    context: context,
  );

  if (enabled) {
    // New feature code
  }
}
```

### PHP

```bash
composer require open-feature/sdk open-feature/flagd-provider
```

```php
<?php
use OpenFeature\OpenFeatureAPI;
use OpenFeature\Providers\Flagd\FlagdProvider;
use OpenFeature\implementation\flags\EvaluationContext;

// Set provider
$api = OpenFeatureAPI::getInstance();
$api->setProvider(new FlagdProvider());

// Get client
$client = $api->getClient('my-app');

// Evaluation context
$context = new EvaluationContext(
    'user-123',
    [
        'email' => 'user@example.com',
        'tier' => 'premium',
    ]
);

// Evaluate flags
$enabled = $client->getBooleanValue('new-feature', false, $context);

if ($enabled) {
    // New feature code
}
```

## Client SDK Implementations

### React

```bash
npm install @openfeature/react-sdk @openfeature/web-sdk @openfeature/flagd-web-provider
```

```tsx
// App.tsx
import { OpenFeatureProvider, useBooleanFlagValue } from '@openfeature/react-sdk';
import { FlagdWebProvider } from '@openfeature/flagd-web-provider';

const provider = new FlagdWebProvider({
  host: 'localhost',
  port: 8013,
});

function App() {
  return (
    <OpenFeatureProvider provider={provider}>
      <FeatureComponent />
    </OpenFeatureProvider>
  );
}

function FeatureComponent() {
  const enabled = useBooleanFlagValue('new-feature', false);

  return enabled ? <NewFeature /> : <OldFeature />;
}
```

```tsx
// With evaluation context
import { useOpenFeatureClient } from '@openfeature/react-sdk';

function UserFeature({ userId }: { userId: string }) {
  const client = useOpenFeatureClient();

  const enabled = useBooleanFlagValue('premium-feature', false, {
    targetingKey: userId,
    tier: 'premium',
  });

  return enabled ? <PremiumFeature /> : <StandardFeature />;
}
```

### Angular

```bash
npm install @openfeature/angular-sdk @openfeature/web-sdk
```

```typescript
// app.module.ts
import { NgModule } from '@angular/core';
import { OpenFeatureModule } from '@openfeature/angular-sdk';
import { InMemoryProvider } from '@openfeature/web-sdk';

@NgModule({
  imports: [
    OpenFeatureModule.forRoot({
      provider: new InMemoryProvider({
        'new-feature': {
          disabled: false,
          variants: { on: true, off: false },
          defaultVariant: 'on'
        },
      }),
    }),
  ],
})
export class AppModule {}
```

```typescript
// feature.component.ts
import { Component } from '@angular/core';
import { BooleanFeatureFlag } from '@openfeature/angular-sdk';

@Component({
  selector: 'app-feature',
  template: `
    <div *ngIf="isEnabled$ | async">
      New Feature Content
    </div>
  `,
})
export class FeatureComponent {
  @BooleanFeatureFlag({ flagKey: 'new-feature', defaultValue: false })
  isEnabled$!: Observable<boolean>;
}
```

### Kotlin (Android)

```kotlin
// build.gradle.kts
dependencies {
    implementation("dev.openfeature:android-sdk:0.3.0")
}
```

```kotlin
import dev.openfeature.sdk.OpenFeatureAPI
import dev.openfeature.sdk.EvaluationContext
import dev.openfeature.contrib.providers.flagd.FlagdProvider

class FeatureFlags(context: Context) {
    private val client: Client

    init {
        // Set provider
        val api = OpenFeatureAPI.getInstance()
        api.setProvider(FlagdProvider())

        client = api.getClient("my-app")
    }

    suspend fun isNewFeatureEnabled(userId: String): Boolean {
        val context = EvaluationContext(
            targetingKey = userId,
            attributes = mapOf(
                "platform" to "android",
                "version" to BuildConfig.VERSION_NAME
            )
        )

        return client.getBooleanValue("new-feature", false, context)
    }
}
```

### iOS / Swift

```swift
// Package.swift
dependencies: [
    .package(url: "https://github.com/open-feature/swift-sdk.git", from: "0.1.0")
]
```

```swift
import OpenFeature

class FeatureFlags {
    private let client: Client

    init() {
        // Set provider
        let api = OpenFeatureAPI.shared
        api.setProvider(provider: InMemoryProvider())

        client = api.getClient(name: "my-app")
    }

    func isNewFeatureEnabled(userId: String) async -> Bool {
        let context = MutableContext(
            targetingKey: userId,
            structure: MutableStructure(
                attributes: [
                    "platform": .string("ios"),
                    "version": .string(Bundle.main.infoDictionary?["CFBundleShortVersionString"] as? String ?? "")
                ]
            )
        )

        return await client.getBooleanValue(
            key: "new-feature",
            defaultValue: false,
            context: context
        )
    }
}
```

## Provider Configuration

### flagd (Open Source)

```yaml
# flagd-config.yaml
flags:
  new-feature:
    state: ENABLED
    variants:
      "on": true
      "off": false
    defaultVariant: "off"
    targeting:
      if:
        - in:
            - var: tier
            - ["premium", "enterprise"]
        - "on"
        - "off"
```

```bash
# Run flagd
docker run -p 8013:8013 -v ./flagd-config.yaml:/config.yaml \
  ghcr.io/open-feature/flagd:latest start --uri file:/config.yaml
```

### In-Memory Provider (Testing)

```typescript
import { InMemoryProvider } from '@openfeature/server-sdk';

const flags = {
  'new-feature': {
    disabled: false,
    variants: { on: true, off: false },
    defaultVariant: 'on',
  },
  'feature-limit': {
    disabled: false,
    variants: { low: 10, medium: 50, high: 100 },
    defaultVariant: 'medium',
  },
};

await OpenFeature.setProviderAndWait(new InMemoryProvider(flags));
```

## OpenFeature MCP Server

The OpenFeature MCP Server enables flag evaluation through Claude.

### Installation

```bash
npx @openfeature/mcp-server
```

### Configuration

```json
{
  "mcpServers": {
    "openfeature": {
      "command": "npx",
      "args": ["@openfeature/mcp-server"],
      "env": {
        "FLAGD_HOST": "localhost",
        "FLAGD_PORT": "8013"
      }
    }
  }
}
```

### Usage

The MCP server provides tools for:
- Evaluating feature flags
- Listing available flags
- Getting flag metadata

## Hooks

### Logging Hook

```typescript
import { Hook, HookContext, EvaluationDetails } from '@openfeature/server-sdk';

const loggingHook: Hook = {
  before: (hookContext: HookContext) => {
    console.log(`Evaluating flag: ${hookContext.flagKey}`);
  },
  after: (hookContext: HookContext, details: EvaluationDetails<any>) => {
    console.log(`Flag ${hookContext.flagKey} = ${details.value}`);
  },
  error: (hookContext: HookContext, error: Error) => {
    console.error(`Error evaluating ${hookContext.flagKey}:`, error);
  },
};

client.addHooks(loggingHook);
```

### Metrics Hook

```typescript
const metricsHook: Hook = {
  after: (hookContext, details) => {
    metrics.increment('feature_flag.evaluation', {
      flag: hookContext.flagKey,
      variant: details.variant,
      reason: details.reason,
    });
  },
};
```

## Testing

### Unit Testing with Mocks

```typescript
import { OpenFeature, InMemoryProvider } from '@openfeature/server-sdk';

describe('Feature Tests', () => {
  beforeEach(async () => {
    await OpenFeature.setProviderAndWait(
      new InMemoryProvider({
        'new-feature': {
          disabled: false,
          variants: { on: true, off: false },
          defaultVariant: 'on',
        },
      })
    );
  });

  it('should show new feature when enabled', async () => {
    const client = OpenFeature.getClient();
    const enabled = await client.getBooleanValue('new-feature', false);
    expect(enabled).toBe(true);
  });
});
```

## Best Practices

1. **Set default values defensively** - Always provide sensible defaults
2. **Use targeting keys** - Enable user-level targeting and consistency
3. **Add evaluation context** - Include relevant attributes for targeting
4. **Implement hooks** - Add logging and metrics for observability
5. **Clean up flags** - Remove flags after features are fully rolled out
6. **Use typed values** - Prefer specific value types over strings
7. **Test both paths** - Test feature on and off states

## References

- [OpenFeature Specification](https://openfeature.dev/specification/)
- [OpenFeature SDK Documentation](https://openfeature.dev/docs/)
- [flagd Documentation](https://flagd.dev/)
- [Provider Catalog](https://openfeature.dev/ecosystem)
- [OpenFeature GitHub](https://github.com/open-feature)
