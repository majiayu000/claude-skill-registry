---
name: document-api
description: Generate comprehensive API documentation in Markdown format for Swift classes and structs. Use this when creating API documentation, documenting public interfaces, or preparing developer documentation for iOS components.
---

# API Documentation Generator

Generate user-friendly API documentation in Markdown format for Swift source files, focusing on public and internal members only.

## Instructions

When asked to document a Swift component's API:

1. **Analyze the Source**: Identify the main class/struct, its purpose, and public-facing API (properties, initializers, methods). Use DocC-style comments (`///`) as primary source.

2. **Generate Documentation** with this structure:

### Structure
```markdown
# API Documentation: [ClassName]

## Overview
[Brief 1-2 sentence summary of component's purpose]

## Properties
* **propertyName** (`type`): Description of property's purpose and usage

## Initializers
### `init(param1:type1, param2:type2)`
Description of what this initializer does
- **param1**: Description of parameter
- **param2**: Description of parameter

## Methods
### `methodName(param1:type1) -> ReturnType`
Description of what the method does
- **param1**: Description of parameter
- **Returns**: Description of return value
```

## Scope Rules
- **Include**: `public` and `internal` members only
- **Exclude**: All `private` and `fileprivate` implementation details

## Example

**Input:**
```swift
/// Converts temperature between different units.
class TemperatureConverter {
    /// The current temperature in degrees Celsius.
    public private(set) var celsius: Double

    /// Creates a converter with an initial Celsius value.
    public init(celsius: Double) {
        self.celsius = celsius
    }

    /// Updates the temperature from a Kelvin value.
    public func set(kelvin: Double) {
        guard kelvin >= 0 else { return }
        self.celsius = kelvin - 273.15
    }
}
```

**Output:**
```markdown
# API Documentation: TemperatureConverter

## Overview
A utility class that converts and stores temperature in Celsius.

## Properties
* **celsius** (`Double`): The current temperature in degrees Celsius. This property is read-only from outside the class.

## Initializers
### `init(celsius: Double)`
Creates a new instance of the converter with a specified initial temperature.
- **celsius**: The starting temperature in degrees Celsius.

## Methods
### `set(kelvin: Double)`
Updates the stored temperature from a Kelvin value. It ignores negative Kelvin values.
- **kelvin**: The new temperature in Kelvin.
```
