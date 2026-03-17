---
name: load-testing
description: Create and manage K6 load tests for REST and GraphQL APIs. Use when creating load tests, writing K6 scripts, testing API performance, debugging load test failures, or setting up performance monitoring. Covers REST endpoints, GraphQL operations, data generation, IRI handling, configuration patterns, and performance troubleshooting.
---

# Load Testing Skill

## Overview

This skill provides guidance for creating and managing K6 load tests for both REST and GraphQL APIs following VilnaCRM ecosystem patterns.

## Core Principles

### 1. Individual Endpoint Testing

- Create separate test scripts for each endpoint (REST) or operation (GraphQL)
- Follow the pattern: `createResource.js`, `getResource.js`, `updateResource.js`, `deleteResource.js`
- For GraphQL: `graphQLCreateResource.js`, `graphQLGetResource.js`, etc.
- Avoid composite/random operation scripts for better debugging and clarity

### 2. Deterministic Testing

- **NEVER use random operations** in load tests
- Use predictable, iteration-based patterns (`__ITER % N`)
- Ensure reproducible results for reliable performance analysis

### 3. Proper Resource Management

- Implement `setup()` function to create test dependencies
- Implement `teardown()` function to clean up test data
- Use proper IRI handling for REST APIs
- Use proper ID handling for GraphQL queries/mutations

### 4. Automatic Integration

- All test scripts are automatically discovered from `tests/Load/scripts/`
- No separate commands needed - GraphQL and REST tests run together
- Use existing Makefile commands

## Available Commands

```bash
# All load tests (REST + GraphQL)
make load-tests

# Specific load levels
make smoke-load-tests      # Minimal load (2-5 VUs, 10s)
make average-load-tests    # Normal load (10-20 VUs, 2-3 min)
make stress-load-tests     # High load (30-80 VUs, 5-15 min)
make spike-load-tests      # Extreme load (100-200 VUs, 1-3 min)

# Individual script
make execute-load-tests-script scenario=createCustomer
make execute-load-tests-script scenario=graphQLCreateCustomer

# List all available scenarios
./tests/Load/get-load-test-scenarios.sh
```

## Quick Start Guide

### 1. Choose Test Type

- **REST API**: Use for HTTP endpoint testing
- **GraphQL**: Use for GraphQL query/mutation testing

### 2. Create Test Script

```bash
# Create in tests/Load/scripts/
touch tests/Load/scripts/yourOperation.js         # REST
touch tests/Load/scripts/graphQLYourOperation.js  # GraphQL
```

### 3. Follow Script Structure

See **Supporting Files** below for detailed templates and examples.

### 4. Add Configuration

Update `tests/Load/config.json.dist` with script parameters.

### 5. Test and Verify

```bash
# Test with smoke load first
make smoke-load-tests

# Verify cleanup
# Check no test data remains in database
```

## Load Test Levels

| Level       | VUs     | Duration     | Success Rate | Purpose                           |
| ----------- | ------- | ------------ | ------------ | --------------------------------- |
| **Smoke**   | 2-5     | 10 seconds   | 100%         | Basic functionality verification  |
| **Average** | 10-20   | 2-3 minutes  | >99%         | Normal traffic simulation         |
| **Stress**  | 30-80   | 5-15 minutes | >95%         | Find breaking points              |
| **Spike**   | 100-200 | 1-3 minutes  | >90%         | Test resilience under sudden load |

## Common Pitfalls

### ❌ Don't Do This

```javascript
// Random operations - unpredictable results
const operation = Math.random();

// Hardcoded test data
const email = 'test@example.com'; // Will cause conflicts

// Missing cleanup in teardown()
```

### ✅ Do This Instead

```javascript
// Deterministic operations
const operationIndex = __ITER % 3;

// Dynamic test data
const email = `test_${Date.now()}_${randomString(6)}@example.com`;

// Proper cleanup
export function teardown(data) {
  // Clean up all created resources
}
```

## Checklist for New Load Tests

### Before Creating

- [ ] Identify the specific endpoint/operation to test
- [ ] Determine if REST or GraphQL (or both)
- [ ] Identify required dependencies (types, statuses, etc.)
- [ ] Plan realistic test data generation
- [ ] Choose appropriate load test parameters

### During Creation

- [ ] Follow the appropriate script structure template
- [ ] Implement proper setup/teardown functions
- [ ] Use deterministic operations (no random)
- [ ] Handle IRI/ID paths correctly
- [ ] Add configuration to `config.json.dist`
- [ ] Use proper naming: `graphQL` prefix for GraphQL tests

### After Creation

- [ ] Verify automatic discovery: `./tests/Load/get-load-test-scenarios.sh`
- [ ] Test with smoke load first
- [ ] Verify 100% success rate in controlled environment
- [ ] Check that cleanup works properly (no leftover data)
- [ ] Document any special requirements

## Performance Monitoring

### Success Criteria

- **Smoke Tests**: 100% success rate
- **Average Tests**: >99% success rate
- **Stress Tests**: >95% success rate
- **Response Times**: <threshold configured per endpoint

### Key Metrics

- HTTP status codes (201, 200, 204 for success)
- Response times (avg, p95, p99)
- Error rates and types
- Throughput (requests per second)

## Supporting Files

For detailed patterns, examples, and reference documentation:

- **[rest-api-patterns.md](rest-api-patterns.md)** - REST API script templates and patterns
- **[graphql-patterns.md](graphql-patterns.md)** - GraphQL script templates and patterns
- **[examples/](examples/)** - Complete working examples
- **[reference/configuration.md](reference/configuration.md)** - Configuration patterns and guidelines
- **[reference/utils-extensions.md](reference/utils-extensions.md)** - Extending the Utils class
- **[reference/troubleshooting.md](reference/troubleshooting.md)** - Common issues and solutions

## Quick Reference

### REST API Test Structure

1. Import required modules
2. Create Utils and ScenarioUtils instances
3. Export options from scenarioUtils
4. Implement setup() for dependencies
5. Implement default function for main test logic
6. Implement teardown() for cleanup
7. Use IRI format for resource references

### GraphQL Test Structure

1. Import required modules
2. Create Utils and ScenarioUtils instances
3. Export options from scenarioUtils
4. Use REST API in setup() for faster dependency creation
5. Use GraphQL in default function for actual testing
6. Use REST API in teardown() for faster cleanup
7. Handle full IRI format in queries/mutations
8. Validate response.data and check for errors

---

This skill ensures consistent, professional, and effective load testing for both REST and GraphQL APIs across all VilnaCRM projects.
