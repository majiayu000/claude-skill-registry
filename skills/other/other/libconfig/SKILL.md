---
name: libconfig
description: >
  libconfig - Configuration management library. serviceConfig, extensionConfig,
  and scriptConfig load settings from files and environment variables.
  Configuration class provides advanced features like namespacing and storage
  backend loading. Use for service initialization, environment-specific
  settings, and runtime configuration.
---

# libconfig Skill

## When to Use

- Loading configuration for services at startup
- Managing environment-specific settings (local, docker, production)
- Accessing configuration values with defaults
- Initializing applications with proper config hierarchy

## Key Concepts

**Namespace configs**: serviceConfig, extensionConfig, scriptConfig provide
scoped configuration for different component types.

**Configuration class**: Advanced configuration with storage backend support and
dynamic reloading.

## Usage Patterns

### Pattern 1: Service configuration

```javascript
import { serviceConfig } from "@copilot-ld/libconfig";

const config = serviceConfig("agent");
const host = config.get("HOST", "localhost");
const port = config.get("PORT", 50051);
```

### Pattern 2: Extension configuration

```javascript
import { extensionConfig } from "@copilot-ld/libconfig";

const config = extensionConfig("web");
const authEnabled = config.get("AUTH_ENABLED", "false") === "true";
```

## Integration

Used by all services and extensions at startup. Loads from .env files and
config/\*.yml.
