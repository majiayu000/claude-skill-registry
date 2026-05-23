---
name: developing-openapi-specs
description: Guide for contributing to the OpenAPI layer using processor pattern, complexity management, and functional programming. Use when adding endpoint factories, processors, parameter descriptions, reducing cyclomatic complexity, or fixing OpenAPI validation errors. Covers architecture patterns from user-service repository.
---

# Developing OpenAPI Specs

**Guide for contributing to the OpenAPI layer** at `src/Shared/Application/OpenApi/`.

This skill covers architecture patterns, complexity management techniques, and best practices for maintaining OpenAPI specifications while keeping code quality high.

**Related Skills**:

- [implementing-ddd-architecture](../implementing-ddd-architecture/SKILL.md) - Domain layer must stay pure; OpenAPI code belongs in Application layer

## When to Use This Skill

- Adding new OpenAPI endpoint factories
- Creating processors for spec transformation
- Adding parameter descriptions or validation
- Modifying OpenAPI generation logic
- Fixing OpenAPI validation errors
- Reducing cyclomatic complexity in OpenAPI code

## Architecture Overview

The OpenAPI layer follows a **Processor Pattern** with clear separation of concerns:

```
src/Shared/Application/OpenApi/
├── Builder/              # Schema and parameter builders
├── Factory/
│   ├── Endpoint/         # Custom endpoint factories
│   ├── Request/          # Request body schemas
│   ├── Response/         # Response schemas
│   └── UriParameter/     # Path parameter factories
├── Processor/            # Spec transformation processors
└── OpenApiFactory.php    # Main coordinator
```

### Key Principles

1. **Single Responsibility**: Each processor/factory handles ONE concern
2. **Immutability**: Use `with*()` methods, never mutate directly
3. **Functional Programming**: Prefer `array_map`, `array_filter` over loops
4. **Match Expressions**: Use PHP 8 `match` instead of if-else chains
5. **Early Returns**: Guard clauses reduce nesting and complexity

## Quick Pattern Reference

### Pattern 1: OPERATIONS Constant

```php
private const OPERATIONS = ['Get', 'Post', 'Put', 'Patch', 'Delete'];

private function processPathItem(PathItem $pathItem): PathItem
{
    foreach (self::OPERATIONS as $operation) {
        $pathItem = $pathItem->{'with' . $operation}(
            $this->processOperation($pathItem->{'get' . $operation}())
        );
    }
    return $pathItem;
}
```

### Pattern 2: Match Expression (Lower Complexity)

```php
// ✅ Complexity: 3
private function processOperation(?Operation $operation): ?Operation
{
    return match (true) {
        $operation === null => null,
        $operation->getParameters() === [] => $operation,
        default => $operation->withParameters(...),
    };
}

// ❌ Complexity: 5
private function processOperation(?Operation $operation): ?Operation
{
    if ($operation === null) return null;
    if ($operation->getParameters() === []) return $operation;
    return $operation->withParameters(...);
}
```

### Pattern 3: Functional Array Operations

```php
// ✅ Functional (complexity: 2)
private function collectRequired(array $params): array
{
    return array_values(
        array_map(
            static fn (Parameter $p) => $p->name,
            array_filter($params, static fn (Parameter $p) => $p->isRequired())
        )
    );
}

// ❌ Procedural (complexity: 3+)
private function collectRequired(array $params): array
{
    $required = [];
    foreach ($params as $param) {
        if ($param->isRequired()) {
            $required[] = $param->name;
        }
    }
    return $required;
}
```

### Pattern 4: Extract Methods (Keep Under 20 Lines)

```php
// Split long methods into focused helpers
private function processContent(Operation $operation): Operation
{
    $content = $operation->getRequestBody()->getContent();
    $modified = false;

    foreach ($content as $mediaType => $mediaTypeObject) {
        $fixedProperties = $this->fixProperties($mediaTypeObject);  // Extracted!
        if ($fixedProperties !== null) {
            $content[$mediaType]['schema']['properties'] = $fixedProperties;
            $modified = true;
        }
    }

    return $modified ? $operation->withRequestBody(...) : $operation;
}

// Extracted method with single responsibility
private function fixProperties(array $mediaTypeObject): ?array
{
    if (!isset($mediaTypeObject['schema']['properties'])) {
        return null;
    }

    $properties = $mediaTypeObject['schema']['properties'];
    return array_map(
        static fn ($prop) => self::fixProperty($prop),
        $properties
    );
}
```

## Complexity Target Metrics

- **Min Complexity**: 94%
- **Max Cyclomatic Complexity/Method**: 10
- **Max Method Length**: 20 lines
- **Max Class Complexity**: ≤ 8

## Quick Start Guide

### Adding a Processor

1. Create class in `src/Shared/Application/OpenApi/Processor/`
2. Implement `process(OpenApi $openApi): OpenApi`
3. Use OPERATIONS constant, match expressions, functional style
4. Inject into `OpenApiFactory` constructor
5. Call in `OpenApiFactory::__invoke()`

See [REFERENCE.md - Adding Processors](REFERENCE.md#adding-a-new-processor) for complete examples.

### Adding an Endpoint Factory

1. Implement `EndpointFactoryInterface`
2. Tag with `app.openapi_endpoint_factory` in services.yaml
3. Auto-discovered by `OpenApiFactory`

See [REFERENCE.md - Adding Endpoint Factories](REFERENCE.md#adding-a-new-endpoint-factory) for step-by-step guide.

### Adding Parameter Descriptions

Add to `ParameterDescriptionAugmenter::getParameterDescriptions()`:

```php
private function getYourFilterDescriptions(): array
{
    return [
        'yourParam' => 'Description of parameter',
        'yourParam[]' => 'Array variant description',
    ];
}

private function getParameterDescriptions(): array
{
    return array_merge(
        $this->getOrderDescriptions(),
        $this->getYourFilterDescriptions(),  // Add here
    );
}
```

## Anti-Patterns to Avoid

1. ❌ **Don't Mutate**: Use `withX()` methods, not direct assignment
2. ❌ **Don't Use empty()**: Explicitly check `$array === []` or `$string === ''`
3. ❌ **Don't Create God Classes**: Split into focused processors
4. ❌ **Don't Repeat HTTP Methods**: Use OPERATIONS constant
5. ❌ **Don't Use If-Else Chains**: Use match expressions

## Testing Your Changes

```bash
make generate-openapi-spec       # Generate spec
make validate-openapi-spec        # Validate with Spectral
make phpinsights                 # Check quality scores
make unit-tests                  # Run tests
```

**Expected Results**:

- OpenAPI validation: "No results with severity 'hint' or higher"
- PHPInsights: Code 100%, Complexity ≥94%, Architecture 100%, Style 100%
- Unit tests: 100% coverage

## Architecture Layer (DDD)

OpenAPI code belongs in the **Application layer**:

- ✅ **Application Layer**: `src/Shared/Application/OpenApi/`
- ❌ **Never in Domain**: Domain must have zero framework dependencies
- See [implementing-ddd-architecture](../implementing-ddd-architecture/SKILL.md) for layer rules

OpenAPI components can depend on:

- Domain entities (for type information)
- Symfony/API Platform components
- DTOs and transformers

## Detailed Documentation

For comprehensive patterns, step-by-step guides, and examples:

- **[REFERENCE.md](REFERENCE.md)** - Full directory structure, all patterns with examples, troubleshooting guide
- **Codebase Examples**:
  - `ParameterDescriptionAugmenter.php` - All key patterns
  - `IriReferenceTypeFixer.php` - Complexity reduction journey
  - `PathParametersSanitizer.php` - Delegation pattern

## Quick Checklist

Before committing OpenAPI changes:

- [ ] Used OPERATIONS constant for HTTP methods
- [ ] Used match expressions (not if-else)
- [ ] Methods under 20 lines
- [ ] Cyclomatic complexity under 10 per method
- [ ] Used functional array operations
- [ ] Pure functions are static
- [ ] No `empty()` - explicit type checks
- [ ] Early returns and guard clauses
- [ ] Delegated to specialized classes
- [ ] `make validate-openapi-spec` passes
- [ ] `make phpinsights` meets thresholds
- [ ] `make unit-tests` pass with 100% coverage

---

**Remember**: Low complexity and high quality go hand-in-hand. Use functional programming, match expressions, and method extraction to keep code maintainable.
