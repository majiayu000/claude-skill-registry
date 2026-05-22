---
name: a2a-testing
description: Test A2A implementations — unit tests, integration tests, mock agents, protocol conformance, and end-to-end multi-agent testing. Use when building test suites for A2A servers, clients, or multi-agent systems.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# A2A Testing

## Before writing code

**Fetch live docs**:
1. Fetch `https://a2a-protocol.org/latest/specification/` for protocol requirements to test against
2. Web-search `site:github.com a2aproject A2A testing conformance` for testing tools and guidance
3. Web-search `site:github.com a2aproject a2a-samples test` for test examples
4. Fetch SDK docs for test utilities, mock classes, and test helpers

## Conceptual Architecture

### Testing Levels

A2A implementations need testing at multiple levels:

#### 1. Unit Tests
Test individual components in isolation:
- Agent handler logic (given input message, verify output)
- Task state management (verify state transitions)
- Message/Part construction and parsing
- Agent Card validation
- Error code generation

#### 2. Integration Tests
Test the A2A server with a real HTTP stack:
- Send JSON-RPC requests, verify responses
- Test all supported methods (message/send, tasks/get, etc.)
- Verify Agent Card serving at `/.well-known/agent-card.json`
- Test authentication flows
- Test streaming with SSE client

#### 3. Protocol Conformance Tests
Verify compliance with the A2A specification:
- All required methods are implemented
- Request/response schemas match the spec
- Error codes are correct
- State transitions follow the rules
- Agent Card schema is valid

#### 4. End-to-End Tests
Test full multi-agent workflows:
- Client discovers agent via Agent Card
- Client sends task, agent processes, client receives result
- Multi-turn conversations complete successfully
- Error scenarios are handled gracefully
- Multiple agents collaborate on a complex task

### Mock Agents

For testing clients, create mock A2A servers that:
- Return predefined responses
- Simulate different task states
- Simulate errors and failures
- Simulate slow responses and timeouts
- Support streaming with controlled events

For testing servers, create mock A2A clients that:
- Send various message types and parts
- Exercise multi-turn flows
- Send invalid requests to test error handling
- Simulate disconnections during streaming

### What to Test

**Server tests:**
- Agent Card is valid and accessible
- All declared methods work correctly
- Task state transitions are correct
- Error codes are appropriate
- Streaming events are properly formatted
- Push notifications are delivered
- Authentication is enforced
- Concurrent requests are handled

**Client tests:**
- Agent Card discovery and parsing
- Request construction (correct JSON-RPC format)
- Response handling for all task states
- Error handling and retry logic
- Multi-turn conversation flow
- Streaming event processing
- Authentication credential handling

### Testing Patterns

**Stateful server tests**: Use an in-memory task store, send a sequence of requests, verify the accumulated state.

**Snapshot testing**: Capture JSON-RPC request/response pairs and verify they match expected schemas.

**Chaos testing**: Introduce random failures, slow responses, and disconnections to test resilience.

**Contract testing**: Verify that client and server agree on the message schemas (both sides validate against the spec).

### Best Practices

- Test all 9 task states, not just the happy path
- Test invalid state transitions (should return errors, not crash)
- Test with all Part types (TextPart, FilePart, DataPart)
- Test streaming with slow consumers and fast producers
- Test authentication with valid and invalid credentials
- Use deterministic agent logic in tests (not real LLMs) for reproducibility
- Validate all JSON-RPC responses against the schema
- Run tests in CI/CD pipelines
- Test Agent Card changes (schema validation)

Fetch any official conformance test suites or testing utilities from the A2A project before building custom test infrastructure.
