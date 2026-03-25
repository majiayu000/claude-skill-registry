---
name: magento-di
description: Configure Magento 2 dependency injection — di.xml, types, virtual types, preferences, argument replacement, and Object Manager. Use when wiring dependencies, creating class variations, or configuring module integrations.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# Magento 2 Dependency Injection

## Before writing code

**Fetch live docs**:
1. Web-search `site:developer.adobe.com commerce php development components dependency-injection` for the DI guide
2. Fetch `https://developer.adobe.com/commerce/php/development/` and navigate to DI documentation
3. Web-search `site:developer.adobe.com commerce php development build di-xml` for di.xml reference

## Conceptual Architecture

### How DI Works in Magento

Magento's Object Manager reads `di.xml` configurations and automatically injects dependencies into class constructors. You declare what you need; the framework provides it.

**Constructor injection** is the primary pattern — declare dependencies as constructor parameters with type hints.

### di.xml Scope

di.xml files are area-scoped:
- `etc/di.xml` — global (all areas)
- `etc/frontend/di.xml` — storefront only
- `etc/adminhtml/di.xml` — admin panel only
- `etc/webapi_rest/di.xml` — REST API only
- `etc/webapi_soap/di.xml` — SOAP API only

### Types

Configure constructor arguments for a specific class:
- Override default values
- Inject different implementations per area
- Argument types: `string`, `boolean`, `number`, `const`, `null`, `object`, `array`, `init_parameter`

### Virtual Types

Create class variations **without writing new PHP files**:
- Same base class with different constructor arguments
- Only exists in DI configuration
- Cannot be injected by classname directly (use as a `type` attribute value)
- Reduces code duplication significantly

### Preferences

Map an interface to a concrete implementation:
- `<preference for="InterfaceName" type="ConcreteClassName" />`
- Global preference applies everywhere unless overridden by area-specific di.xml
- Foundation of Magento's interface-based programming

### Argument Types

| Type | Description |
|------|-------------|
| `string` | String value |
| `boolean` | `true` or `false` |
| `number` | Integer or float |
| `const` | PHP constant value |
| `null` | Null value |
| `object` | Another class instance (injected) |
| `array` | Array of mixed argument types |
| `init_parameter` | Value from `Magento\Framework\App\DeploymentConfig` |

### Shared vs Non-Shared

- By default, Object Manager creates **shared** instances (singleton behavior)
- Set `shared="false"` on a type to get a new instance each time
- Factories (`SomeClassFactory`) always create new instances

### Sensitive/Environment Config

`init_parameter` type reads from `app/etc/env.php` — use for environment-specific values that shouldn't be in di.xml.

## Common Patterns

- **Interface → Implementation mapping**: preference for repository, data, and service interfaces
- **Logger customization**: virtual type with custom handler arguments
- **Collection modification**: type with different filter arguments per area
- **Plugin declaration**: type with plugin child element (covered in plugins skill)

## Best Practices

- Always inject interfaces, not concrete classes
- Use virtual types to avoid unnecessary PHP files
- Scope di.xml to the smallest applicable area
- Never call Object Manager directly in application code (only in factories and framework)
- Use `shared="false"` sparingly — most dependencies should be shared

Fetch the DI documentation for exact XML schema, element attributes, and current best practices before configuring.
