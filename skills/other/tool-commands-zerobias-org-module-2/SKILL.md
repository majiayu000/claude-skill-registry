---
name: tool-commands
description: Development tool commands and usage patterns
---

# Tool Requirements and Commands

Essential tools and commands for module development.

## Required Tools

### Node.js
- **Version**: >= 16.0.0
- **Check**: `node --version`
- **Install**: https://nodejs.org/

### npm
- **Version**: >= 8.0.0
- **Check**: `npm --version`
- **Comes with**: Node.js installation

### Yeoman
- **Version**: >= 4.0.0
- **Check**: `yo --version`
- **Install**: `npm install -g yo`
- **Purpose**: Module scaffolding with generator

### Java
- **Version**: >= 11.0.0
- **Check**: `java -version`
- **Install**: https://adoptium.net/
- **Purpose**: OpenAPI code generation

### yq (YAML Processor)
- **Check**: `yq --version`
- **Install (Mac)**: `brew install yq`
- **Install (Linux)**: Download from https://github.com/mikefarah/yq
- **Purpose**: API specification validation and transformation

### swagger-cli
- **Check**: `swagger-cli --version`
- **Install**: `npm install -g swagger-cli`
- **Purpose**: OpenAPI specification validation

### jq (JSON Processor)
- **Check**: `jq --version`
- **Install (Mac)**: `brew install jq`
- **Install (Linux)**: `apt-get install jq` or `yum install jq`
- **Purpose**: JSON processing in scripts

## Essential Module Commands

### Discovery and Scaffolding

```bash
# List available product packages
npm view @zerobias-org/product-bundle --json

# Create module with Yeoman generator
yo @auditmation/hub-module
# Follow prompts to configure module

# Sync package metadata
npm run sync-meta
```

### Type Generation and Building

```bash
# Generate TypeScript types from API specification
npm run clean && npm run generate

# Transpile TypeScript (compile without linting)
npm run transpile

# Full build (lint + compile + bundle)
npm run build

# Clean build artifacts
npm run clean
```

### API Specification Validation

```bash
# Validate OpenAPI specification
npx swagger-cli validate api.yml

# Check for common API spec issues
grep -E "describe[A-Z]" api.yml  # Should return nothing
grep "nullable:" api.yml          # Should return nothing
grep -E "'40[0-9]'|'50[0-9]'" api.yml  # Should return nothing

# Lint API specification (if configured)
npm run lint:api
```

### Testing

```bash
# Run all tests
npm test

# Run only unit tests
npm test -- test/unit

# Run only integration tests
npm run test:integration

# Run with coverage
npm test -- --coverage
```

### Code Quality

```bash
# Lint source code
npm run lint:src

# Auto-fix linting issues
npm run lint:src -- --fix

# Type check without building
npx tsc --noEmit
```

### Dependency Management

```bash
# Install dependencies
npm install

# Lock dependencies for npm package
npm run shrinkwrap

# Check for outdated packages
npm outdated

# Audit for security issues
npm audit
```

### Validation Scripts

```bash
# Check for generated inline types (should be none)
grep -r "InlineResponse\|InlineRequestBody" generated/

# Verify no Promise<any> in source
grep "Promise<any>" src/*.ts

# Check for environment variables in source (forbidden)
grep "process.env" src/*.ts  # Should only be in test/Common.ts

# Validate connectionState has expiresIn
grep "expiresIn:" connectionState.yml || grep "baseConnectionState" connectionState.yml
```

## Module-Specific Scripts

These commands are available in generated modules:

```bash
# Module commands (from package.json)
npm run build         # Full build pipeline
npm run clean         # Remove build artifacts
npm run generate      # Generate types from API spec
npm run transpile     # Compile TypeScript only
npm run lint:src      # Lint source files
npm run lint:api      # Lint API specification
npm run test          # Run tests
npm run shrinkwrap    # Lock dependencies
npm run sync-meta     # Sync package metadata
```

## yq Validation Patterns

### Check for envelope/wrapper responses
```bash
yq eval '.paths.*.*.responses.*.content.*.schema | select(has("properties"))' api.yml
# Should only return business object schemas, not wrapper schemas
```

### Find schemas used in nested contexts
```bash
nested_schemas=$(yq eval '.components.schemas[] | .. | select(type == "string" and test("#/components/schemas/")) | capture("#/components/schemas/(?<schema>.+)").schema' api.yml | sort -u)
```

### Find schemas with their own endpoints
```bash
endpoint_schemas=$(yq eval '.paths.*.*.responses.*.content.*.schema["$ref"]' api.yml | grep -o '[^/]*$' | sort -u)
```

### Count properties in a schema
```bash
prop_count=$(yq eval ".components.schemas.User.properties | length" api.yml)
```

## Tool Installation Validation

Before starting module development, verify all tools are installed:

```bash
#!/bin/bash
# check-tools.sh

echo "Checking required tools..."

command -v node >/dev/null 2>&1 || { echo "❌ Node.js not installed"; exit 1; }
command -v npm >/dev/null 2>&1 || { echo "❌ npm not installed"; exit 1; }
command -v yo >/dev/null 2>&1 || { echo "❌ Yeoman not installed"; exit 1; }
command -v java >/dev/null 2>&1 || { echo "❌ Java not installed"; exit 1; }
command -v yq >/dev/null 2>&1 || { echo "❌ yq not installed"; exit 1; }
command -v jq >/dev/null 2>&1 || { echo "❌ jq not installed"; exit 1; }

echo "✅ All required tools installed"
```

## Common Issues

### "swagger-cli: command not found"
```bash
npm install -g swagger-cli
```

### "yq: command not found"
```bash
# Mac
brew install yq

# Linux
wget https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64 -O /usr/local/bin/yq
chmod +x /usr/local/bin/yq
```

### "yo: command not found"
```bash
npm install -g yo
```

### Java version too old
```bash
# Install Java 11 or newer from https://adoptium.net/
# Verify: java -version
```

## Agent Usage

Agents should reference specific commands from this file:

```markdown
## Prerequisites

Verify tools are available:
- See tool-requirements skill for installation

## Validation

Run validation commands:
- See tool-requirements skill for validation scripts
```
