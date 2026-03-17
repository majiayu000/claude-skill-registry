---
name: contract-test-v2
description: Generate API contract tests with Pact V4
argument-hint: "<consumer> <provider> [--broker-url=<url>]"
tags: [testing, contract, pact, api]
user-invocable: true
---

# Contract Testing with Pact V4

Generate consumer-driven contract tests between microservices.

## Consumer Side (.NET)
```bash
dotnet add package PactNet
```
Generate consumer test that defines expectations, then publish pact to broker.

## Provider Side (.NET)
```bash
dotnet add package PactNet.Verifier
```
Verify provider against published pact contracts.

## CI Integration
Run consumer tests first, publish pacts, then verify providers.

## Arguments
- `<consumer>`: Consumer service name
- `<provider>`: Provider service name
- `--broker-url=<url>`: Pact Broker URL