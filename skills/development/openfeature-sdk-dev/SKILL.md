---
name: openfeature-sdk-dev
description: Develop OpenFeature SDK implementations from the specification. Use when implementing the OpenFeature spec in a new language, extending existing SDKs with new features, building custom providers, or contributing to official SDK repositories.
---

# OpenFeature SDK Development

> **Note**: This skill extends patterns from `meta-sdk-patterns-eng`.
> See that skill for foundational SDK patterns (architecture, error handling,
> configuration, testing strategies, packaging).

Guide for implementing OpenFeature SDKs from the specification. This skill covers building SDK implementations, not using existing SDKs (see `openfeature-eng` for usage).

## When to Use This Skill

- Implementing OpenFeature in a new programming language
- Contributing to official OpenFeature SDK repositories
- Building custom providers from scratch
- Extending existing SDKs with new features
- Understanding SDK architecture and compliance requirements

## Specification Overview

OpenFeature uses RFC 2119 keywords (MUST, SHOULD, MAY) to define normative requirements. Implementations achieve compliance by satisfying all mandatory clauses.

### Stability Levels

| Level | Description | Breaking Change Policy |
|-------|-------------|------------------------|
| **Experimental** | Testing features, may change anytime | None |
| **Hardening** | Production-ready, TSC consensus for changes | Requires consensus |
| **Stable** | Battle-tested, major version protection | Major version only |

## Core Architecture

### Component Hierarchy

```
┌─────────────────────────────────────────────────────────────┐
│                     OpenFeature API                         │
│  (Global Singleton - manages providers, hooks, context)     │
├─────────────────────────────────────────────────────────────┤
│                        Client(s)                            │
│  (Domain-scoped flag evaluation interface)                  │
├─────────────────────────────────────────────────────────────┤
│                       Provider(s)                           │
│  (Translates evaluation to flag management system)          │
├─────────────────────────────────────────────────────────────┤
│                         Hooks                               │
│  (Lifecycle middleware: before/after/error/finally)         │
└─────────────────────────────────────────────────────────────┘
```

### SDK Paradigms

**Dynamic-Context (Server-Side)**
- Context passed per evaluation call
- Stateless evaluation
- Multi-tenant support

**Static-Context (Client-Side)**
- Context set once, cached
- Requires reconciliation on context change
- Single-user/device focus

## Type Definitions

### Flag Value Types

```typescript
// Core value types
type FlagValue = boolean | string | number | Structure;

// Structure: Language-idiomatic structured data (object, dict, map)
interface Structure {
  [key: string]: boolean | string | number | DateTime | Structure;
}
```

### Resolution Details

```typescript
interface ResolutionDetails<T extends FlagValue> {
  value: T;                    // Required: resolved flag value
  variant?: string;            // Optional: string identifier for value
  reason?: ResolutionReason;   // Optional: semantic cause
  errorCode?: ErrorCode;       // Optional: null/falsy on success
  errorMessage?: string;       // Optional: additional error detail
  flagMetadata?: FlagMetadata; // Optional: arbitrary metadata
}

type ResolutionReason =
  | 'STATIC'           // Statically configured value
  | 'DEFAULT'          // Default value returned
  | 'TARGETING_MATCH'  // Targeting rule matched
  | 'SPLIT'            // Percentage/split allocation
  | 'CACHED'           // Cached value returned
  | 'DISABLED'         // Flag disabled
  | 'UNKNOWN'          // Reason unknown
  | 'STALE'            // Stale cached value
  | 'ERROR'            // Error occurred
  | string;            // Custom reasons allowed
```

### Error Codes

```typescript
enum ErrorCode {
  PROVIDER_NOT_READY = 'PROVIDER_NOT_READY',
  FLAG_NOT_FOUND = 'FLAG_NOT_FOUND',
  PARSE_ERROR = 'PARSE_ERROR',
  TYPE_MISMATCH = 'TYPE_MISMATCH',
  TARGETING_KEY_MISSING = 'TARGETING_KEY_MISSING',
  INVALID_CONTEXT = 'INVALID_CONTEXT',
  PROVIDER_FATAL = 'PROVIDER_FATAL',
  GENERAL = 'GENERAL'
}
```

### Provider Status

```typescript
enum ProviderStatus {
  NOT_READY = 'NOT_READY',     // Initial state, not yet initialized
  READY = 'READY',             // Initialization complete
  ERROR = 'ERROR',             // Temporary error, may recover
  STALE = 'STALE',             // Using cached/stale data
  FATAL = 'FATAL',             // Unrecoverable error
  RECONCILING = 'RECONCILING'  // Static-context only: context change in progress
}
```

## API Implementation

### Global Singleton (Requirement 1.1.1)

The API SHOULD exist as a global singleton, even with multiple API versions present.

```typescript
// TypeScript example structure
class OpenFeatureAPI {
  private static instance: OpenFeatureAPI;
  private providers: Map<string, FeatureProvider> = new Map();
  private hooks: Hook[] = [];
  private globalContext: EvaluationContext = {};

  static getInstance(): OpenFeatureAPI {
    if (!OpenFeatureAPI.instance) {
      OpenFeatureAPI.instance = new OpenFeatureAPI();
    }
    return OpenFeatureAPI.instance;
  }
}
```

### Provider Management

```typescript
interface OpenFeatureAPI {
  // Requirement 1.1.2: Set default provider
  setProvider(provider: FeatureProvider): void;

  // Requirement 1.1.2: Set provider and await initialization
  setProviderAndWait(provider: FeatureProvider): Promise<void>;

  // Requirement 1.1.3: Bind provider to domain
  setProvider(domain: string, provider: FeatureProvider): void;

  // Requirement 1.1.5: Get provider metadata
  getProviderMetadata(domain?: string): ProviderMetadata;

  // Requirement 1.6.1: Shutdown all providers
  shutdown(): Promise<void>;
}
```

**Provider Lifecycle Rules:**
- MUST invoke `initialize` on newly registered provider before resolution
- MUST call `shutdown` on previously registered provider when replaced
- Requirement 1.6.2: Shutdown MUST reset all API state

### Hook Management

```typescript
interface OpenFeatureAPI {
  // Requirement 1.1.4: Add hooks (append to collection)
  addHooks(...hooks: Hook[]): void;

  // Clear hooks
  clearHooks(): void;
}
```

### Client Creation

```typescript
interface OpenFeatureAPI {
  // Requirement 1.1.6: Create client with optional domain
  getClient(domain?: string): Client;
}
```

**Requirement 1.1.7**: Client creation MUST NOT throw or abnormally terminate.

## Client Implementation

### Client Interface

```typescript
interface Client {
  // Requirement 1.2.2: Immutable domain field
  readonly domain?: string;

  // Client-level hooks
  addHooks(...hooks: Hook[]): void;

  // Client-level context (dynamic paradigm)
  setContext(context: EvaluationContext): void;
}
```

### Flag Evaluation Methods

**Dynamic-Context Paradigm (Requirement 1.3.1.1)**

```typescript
interface Client {
  getBooleanValue(
    flagKey: string,
    defaultValue: boolean,
    context?: EvaluationContext,
    options?: EvaluationOptions
  ): boolean;

  getStringValue(
    flagKey: string,
    defaultValue: string,
    context?: EvaluationContext,
    options?: EvaluationOptions
  ): string;

  getNumberValue(
    flagKey: string,
    defaultValue: number,
    context?: EvaluationContext,
    options?: EvaluationOptions
  ): number;

  getObjectValue<T extends Structure>(
    flagKey: string,
    defaultValue: T,
    context?: EvaluationContext,
    options?: EvaluationOptions
  ): T;
}
```

**Static-Context Paradigm (Requirement 1.3.2.1)**

Context parameter omitted; set at API/client level.

```typescript
interface StaticContextClient {
  getBooleanValue(
    flagKey: string,
    defaultValue: boolean,
    options?: EvaluationOptions
  ): boolean;
  // ... same pattern for other types
}
```

**Requirement 1.3.3.1**: Languages with separate integer/float types SHOULD provide distinct methods.

### Detailed Evaluation Methods

Return `EvaluationDetails` with supplementary metadata.

```typescript
interface EvaluationDetails<T extends FlagValue> extends ResolutionDetails<T> {
  flagKey: string;  // Requirement 1.4.5: Must contain passed flag key
}

interface Client {
  getBooleanDetails(
    flagKey: string,
    defaultValue: boolean,
    context?: EvaluationContext,
    options?: EvaluationOptions
  ): EvaluationDetails<boolean>;

  // ... same pattern for string, number, object
}
```

### Type Safety (Requirement 1.3.4)

If provider returns wrong type, return default value:

```typescript
function evaluateFlag<T>(flagKey: string, defaultValue: T): T {
  const result = provider.resolve(flagKey, defaultValue);

  // Type mismatch → return default
  if (typeof result.value !== typeof defaultValue) {
    return defaultValue;
  }

  return result.value as T;
}
```

### Error Handling (Requirement 1.4.10)

**CRITICAL**: Methods MUST NOT throw exceptions. Always return default value on error.

```typescript
function getBooleanValue(flagKey: string, defaultValue: boolean): boolean {
  try {
    const details = provider.resolveBooleanValue(flagKey, defaultValue, context);
    return details.value;
  } catch (error) {
    // Log via hooks, not direct logging (Requirement 1.4.11)
    return defaultValue;
  }
}
```

### Evaluation Options

```typescript
interface EvaluationOptions {
  // Requirement 1.5.1: Additional hooks for this evaluation
  hooks?: Hook[];

  // Hook hints passed to all hooks
  hookHints?: HookHints;
}
```

## Provider Implementation

### Provider Interface

```typescript
interface FeatureProvider {
  // Requirement 2.1.1: Metadata with name field
  readonly metadata: ProviderMetadata;

  // Requirement 2.4.1: Optional initialization
  initialize?(context: EvaluationContext): Promise<void>;

  // Requirement 2.5.1: Optional shutdown
  shutdown?(): Promise<void>;

  // Requirement 2.6.1: Optional context change handler (static paradigm)
  onContextChange?(
    oldContext: EvaluationContext,
    newContext: EvaluationContext
  ): Promise<void>;

  // Requirement 2.3.1: Optional provider hooks
  hooks?: Hook[];

  // Requirement 2.2.1: Resolution methods
  resolveBooleanValue(
    flagKey: string,
    defaultValue: boolean,
    context: EvaluationContext
  ): ResolutionDetails<boolean>;

  resolveStringValue(
    flagKey: string,
    defaultValue: string,
    context: EvaluationContext
  ): ResolutionDetails<string>;

  resolveNumberValue(
    flagKey: string,
    defaultValue: number,
    context: EvaluationContext
  ): ResolutionDetails<number>;

  resolveObjectValue<T extends Structure>(
    flagKey: string,
    defaultValue: T,
    context: EvaluationContext
  ): ResolutionDetails<T>;
}

interface ProviderMetadata {
  name: string;
}
```

### Provider Lifecycle States

```
                    ┌──────────────────┐
                    │    NOT_READY     │
                    │  (Initial State) │
                    └────────┬─────────┘
                             │ initialize()
                    ┌────────┴─────────┐
          success   │                  │ failure
        ┌───────────┤                  ├───────────┐
        ▼           │                  │           ▼
┌───────────┐       │                  │    ┌───────────┐
│   READY   │◄──────┘                  └────│   ERROR   │
└─────┬─────┘                               └─────┬─────┘
      │                                           │
      │ config change / recovery                  │ recovery
      │ ┌─────────┐                               │
      ├─┤  STALE  │◄──────────────────────────────┘
      │ └─────────┘
      │
      │ shutdown()
      ▼
┌───────────┐
│ NOT_READY │
└───────────┘

┌───────────┐
│   FATAL   │  (Unrecoverable - no transitions out)
└───────────┘
```

### Resolution Details Requirements

```typescript
function resolveValue<T>(flagKey: string, defaultValue: T): ResolutionDetails<T> {
  // Requirement 2.2.3: Value field MUST contain resolved value
  // Requirement 2.2.4: Variant SHOULD be set if available
  // Requirement 2.2.5: Reason SHOULD indicate semantic cause
  // Requirement 2.2.6: Error code MUST be null/falsy on success
  // Requirement 2.2.9: Flag metadata SHOULD be populated

  return {
    value: resolvedValue,
    variant: 'variant-a',
    reason: 'TARGETING_MATCH',
    errorCode: undefined,
    flagMetadata: { version: '1.0.0' }
  };
}
```

### Error Handling in Providers

```typescript
function resolveValue(flagKey: string): ResolutionDetails {
  try {
    // Normal resolution
    return { value: resolved, reason: 'TARGETING_MATCH' };
  } catch (error) {
    // Requirement 2.2.7: Indicate errors with error codes
    // Requirement 2.3.3: May include error message
    return {
      value: defaultValue,
      reason: 'ERROR',
      errorCode: 'GENERAL',
      errorMessage: error.message
    };
  }
}
```

### Provider Shutdown (Requirement 2.5.2-2.5.3)

```typescript
class MyProvider implements FeatureProvider {
  private initialized = false;

  async shutdown(): Promise<void> {
    if (!this.initialized) return; // Idempotent

    // Clean up resources
    await this.connection?.close();
    this.initialized = false;

    // Requirement 2.5.2: Revert to uninitialized state
  }
}
```

## Evaluation Context

### Context Structure

```typescript
interface EvaluationContext {
  // Requirement 3.1.1: Optional targeting key
  targetingKey?: string;

  // Requirement 3.1.2: Custom fields
  [key: string]: boolean | string | number | DateTime | Structure | undefined;
}
```

### Context Merging (Requirement 3.2.3)

Precedence order (highest wins):
1. Before hooks (highest)
2. Invocation context
3. Client context
4. Transaction context
5. API (global) context (lowest)

```typescript
function mergeContext(...contexts: EvaluationContext[]): EvaluationContext {
  // Later contexts override earlier ones
  return contexts.reduce((merged, ctx) => ({
    ...merged,
    ...ctx
  }), {});
}

// Usage in evaluation
const finalContext = mergeContext(
  api.getContext(),           // Lowest precedence
  transactionContext,
  client.getContext(),
  invocationContext,
  beforeHookContext           // Highest precedence
);
```

## Hooks Implementation

### Hook Interface

```typescript
interface Hook {
  // At least one stage required
  before?(context: HookContext, hints: HookHints): EvaluationContext | void;
  after?(context: HookContext, details: EvaluationDetails, hints: HookHints): void;
  error?(context: HookContext, error: Error, hints: HookHints): void;
  finally?(context: HookContext, hints: HookHints): void;
}

interface HookContext {
  readonly flagKey: string;
  readonly flagValueType: FlagValueType;
  readonly defaultValue: FlagValue;
  readonly evaluationContext: EvaluationContext;
  readonly clientMetadata: ClientMetadata;
  readonly providerMetadata: ProviderMetadata;

  // Mutable: allows inter-stage communication
  hookData: Record<string, unknown>;
}

interface HookHints {
  readonly [key: string]: boolean | string | number | DateTime | Structure;
}
```

### Hook Execution Order

```
API Hooks ──┬── before() ────────────────────────────────────┐
            │                                                 │
Client Hooks┼── before() ───────────────────────────────────┐│
            │                                                ││
Invocation ─┼── before() ──────────────────────────────────┐││
Hooks       │                                               │││
            │                                               │││
Provider ───┼── before() ─────────────────────────────────┐││││
Hooks       │                                              │││││
            │          ┌─────────────────┐                 │││││
            │          │  FLAG RESOLVE   │                 │││││
            │          └─────────────────┘                 │││││
            │                                              │││││
Provider ───┼── after() ──────────────────────────────────┘││││
Hooks       │                                               ││││
            │                                               ││││
Invocation ─┼── after() ───────────────────────────────────┘│││
Hooks       │                                                │││
            │                                                │││
Client Hooks┼── after() ────────────────────────────────────┘││
            │                                                 ││
API Hooks ──┴── after() ─────────────────────────────────────┘│
                                                               │
            finally() executes in same reverse order ◄─────────┘
```

### Hook Error Handling

```typescript
async function executeHooks(hooks: Hook[], stage: string): Promise<void> {
  for (const hook of hooks) {
    try {
      await hook[stage]?.();
    } catch (error) {
      // Hooks MUST NOT propagate exceptions
      // Error hooks still execute
      // Finally hooks always execute
      if (stage !== 'error' && stage !== 'finally') {
        await executeErrorHooks(hooks, error);
      }
    }
  }
}
```

### Before Hook Context Modification

```typescript
// Dynamic-context paradigm only
function beforeHook(context: HookContext): EvaluationContext {
  // Can return modified context (merged with highest precedence)
  return {
    ...context.evaluationContext,
    additionalKey: 'added-by-hook'
  };
}
```

## Events Implementation

### Event Types

```typescript
enum ProviderEvent {
  PROVIDER_READY = 'PROVIDER_READY',
  PROVIDER_ERROR = 'PROVIDER_ERROR',
  PROVIDER_FATAL = 'PROVIDER_FATAL',
  PROVIDER_STALE = 'PROVIDER_STALE',
  PROVIDER_CONFIGURATION_CHANGED = 'PROVIDER_CONFIGURATION_CHANGED',
  PROVIDER_RECONCILING = 'PROVIDER_RECONCILING',        // Static-context only
  PROVIDER_CONTEXT_CHANGED = 'PROVIDER_CONTEXT_CHANGED' // Static-context only
}

interface EventDetails {
  providerName: string;
  errorCode?: ErrorCode;
  errorMessage?: string;
  flagsChanged?: string[];
  metadata?: Record<string, unknown>;
}

type EventHandler = (details: EventDetails) => void;
```

### Event Handler Registration

```typescript
interface EventEmitter {
  // Requirement 5.2.1: API-level handlers
  addHandler(event: ProviderEvent, handler: EventHandler): void;

  // Requirement 5.2.2: Client-level handlers
  addHandler(event: ProviderEvent, handler: EventHandler): void;

  // Requirement 5.2.7: Handler removal
  removeHandler(event: ProviderEvent, handler: EventHandler): void;
}
```

### Event Emission Rules

```typescript
class ProviderWrapper {
  private handlers: Map<ProviderEvent, EventHandler[]> = new Map();

  async initialize(): Promise<void> {
    try {
      await this.provider.initialize?.(this.context);
      // Requirement 5.3.1: Emit READY on success
      this.emit(ProviderEvent.PROVIDER_READY);
    } catch (error) {
      // Requirement 5.3.2: Emit ERROR on failure
      this.emit(ProviderEvent.PROVIDER_ERROR, {
        errorCode: 'GENERAL',
        errorMessage: error.message
      });
    }
  }

  private emit(event: ProviderEvent, details?: Partial<EventDetails>): void {
    const handlers = this.handlers.get(event) ?? [];
    for (const handler of handlers) {
      try {
        handler({ providerName: this.provider.metadata.name, ...details });
      } catch {
        // Requirement 5.2.5: Handler errors don't prevent other handlers
      }
    }
  }
}
```

### Deferred Handler Execution (Requirement 5.3.3)

```typescript
function addHandler(event: ProviderEvent, handler: EventHandler): void {
  this.handlers.get(event)?.push(handler);

  // If provider already in target state, execute immediately
  if (event === ProviderEvent.PROVIDER_READY && this.status === 'READY') {
    handler({ providerName: this.provider.metadata.name });
  }
}
```

## Provider Status Management

### Status Tracking (Requirement 1.7.1)

```typescript
class ProviderManager {
  private status: ProviderStatus = ProviderStatus.NOT_READY;

  getStatus(): ProviderStatus {
    return this.status;
  }

  async initialize(): Promise<void> {
    try {
      await this.provider.initialize?.(this.context);
      // Requirement 1.7.3: READY on normal initialization
      this.status = ProviderStatus.READY;
    } catch (error) {
      if (error.code === 'PROVIDER_FATAL') {
        // Requirement 1.7.5: FATAL on fatal error
        this.status = ProviderStatus.FATAL;
      } else {
        // Requirement 1.7.4: ERROR on abnormal termination
        this.status = ProviderStatus.ERROR;
      }
    }
  }
}
```

### Evaluation During Non-Ready States

```typescript
function evaluate(flagKey: string, defaultValue: boolean): EvaluationDetails<boolean> {
  // Requirement 1.7.6: Return error code if NOT_READY
  if (this.status === ProviderStatus.NOT_READY) {
    return {
      value: defaultValue,
      flagKey,
      reason: 'ERROR',
      errorCode: ErrorCode.PROVIDER_NOT_READY
    };
  }

  // Requirement 1.7.7: Return error code if FATAL
  if (this.status === ProviderStatus.FATAL) {
    return {
      value: defaultValue,
      flagKey,
      reason: 'ERROR',
      errorCode: ErrorCode.PROVIDER_FATAL
    };
  }

  // Normal evaluation
  return this.provider.resolveBooleanValue(flagKey, defaultValue, this.context);
}
```

## Testing Requirements

### Gherkin Test Suites

The specification includes Gherkin test suites for compliance testing:

```gherkin
Feature: Flag Evaluation

Scenario: Boolean flag evaluation returns expected value
  Given a provider is registered
  When a boolean flag "my-flag" is evaluated with default "false"
  Then the returned value should be "true"
  And the variant should be "on"
  And the reason should be "TARGETING_MATCH"

Scenario: Evaluation returns default on provider error
  Given a provider is registered that throws errors
  When a boolean flag "error-flag" is evaluated with default "false"
  Then the returned value should be "false"
  And the error code should be "GENERAL"
```

### Compliance Testing Structure

```typescript
// Test categories to implement
describe('Flag Evaluation API', () => {
  describe('Singleton behavior', () => {
    it('should return same instance', () => {
      expect(OpenFeature.getInstance()).toBe(OpenFeature.getInstance());
    });
  });

  describe('Provider management', () => {
    it('should call initialize on provider registration');
    it('should call shutdown on previous provider when replaced');
  });

  describe('Flag evaluation', () => {
    it('should return correct type for boolean flags');
    it('should return default value on type mismatch');
    it('should never throw exceptions');
  });

  describe('Hooks', () => {
    it('should execute in correct order');
    it('should not propagate hook errors');
  });

  describe('Events', () => {
    it('should emit PROVIDER_READY on successful initialization');
    it('should execute deferred handlers immediately');
  });
});
```

## SDK Implementation Checklist

### Phase 1: Core Types

- [ ] Define FlagValue union type
- [ ] Define ResolutionDetails structure
- [ ] Define EvaluationDetails structure
- [ ] Implement ErrorCode enum
- [ ] Implement ProviderStatus enum
- [ ] Implement ResolutionReason type
- [ ] Define EvaluationContext interface
- [ ] Define FlagMetadata type

### Phase 2: Provider Interface

- [ ] Define FeatureProvider interface
- [ ] Define ProviderMetadata interface
- [ ] Implement NoOpProvider (for testing/defaults)
- [ ] Support initialize lifecycle method
- [ ] Support shutdown lifecycle method
- [ ] Support onContextChange (static paradigm)

### Phase 3: API Implementation

- [ ] Implement global singleton
- [ ] Implement provider registration
- [ ] Implement domain-scoped providers
- [ ] Implement hook registration
- [ ] Implement context management
- [ ] Implement shutdown

### Phase 4: Client Implementation

- [ ] Implement client creation (non-throwing)
- [ ] Implement value methods (boolean, string, number, object)
- [ ] Implement details methods
- [ ] Implement client-level hooks
- [ ] Implement client-level context
- [ ] Ensure type safety

### Phase 5: Hooks

- [ ] Define Hook interface
- [ ] Define HookContext interface
- [ ] Define HookHints interface
- [ ] Implement hook execution order
- [ ] Implement error isolation
- [ ] Implement finally stage guarantee
- [ ] Support context modification (dynamic)

### Phase 6: Events

- [ ] Define ProviderEvent enum
- [ ] Define EventDetails interface
- [ ] Implement event emitter
- [ ] Implement handler registration
- [ ] Implement deferred execution
- [ ] Ensure handler error isolation

### Phase 7: Testing

- [ ] Unit tests for all components
- [ ] Integration tests with providers
- [ ] Gherkin compliance tests
- [ ] Edge case coverage
- [ ] Concurrency testing (if applicable)

---

## Server SDK Implementation

Server SDKs use the **dynamic-context paradigm** where evaluation context is passed per request. This is the most common pattern for backend services.

### Key Characteristics

| Aspect | Server SDK Behavior |
|--------|---------------------|
| Context | Passed per evaluation call |
| State | Stateless between evaluations |
| Concurrency | Multi-threaded, concurrent evaluations |
| Users | Multi-tenant (many users per instance) |
| Lifecycle | Long-running process |

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Server Application                        │
├─────────────────────────────────────────────────────────────┤
│  Request 1          Request 2          Request 3            │
│  ┌─────────┐        ┌─────────┐        ┌─────────┐          │
│  │Context A│        │Context B│        │Context C│          │
│  └────┬────┘        └────┬────┘        └────┬────┘          │
│       │                  │                  │                │
│       └──────────────────┼──────────────────┘                │
│                          ▼                                   │
│                 ┌─────────────────┐                          │
│                 │ OpenFeature API │ (Singleton)              │
│                 └────────┬────────┘                          │
│                          ▼                                   │
│                 ┌─────────────────┐                          │
│                 │    Provider     │ (Shared, thread-safe)    │
│                 └─────────────────┘                          │
└─────────────────────────────────────────────────────────────┘
```

### Server SDK Requirements

```typescript
// Dynamic-context evaluation signature
interface ServerClient {
  getBooleanValue(
    flagKey: string,
    defaultValue: boolean,
    context: EvaluationContext,  // Required per-call
    options?: EvaluationOptions
  ): boolean;
}

// Context passed with each request
app.get('/api/feature', (req, res) => {
  const context: EvaluationContext = {
    targetingKey: req.user.id,
    email: req.user.email,
    plan: req.user.subscription,
    // Request-specific context
  };

  const enabled = client.getBooleanValue('new-feature', false, context);
  res.json({ enabled });
});
```

### Server-Specific Considerations

**Thread Safety**
```typescript
// Provider must be thread-safe
class ThreadSafeProvider implements FeatureProvider {
  private cache: Map<string, FlagValue> = new Map();
  private mutex = new Mutex();

  async resolveBooleanValue(
    flagKey: string,
    defaultValue: boolean,
    context: EvaluationContext
  ): Promise<ResolutionDetails<boolean>> {
    // Use mutex for cache access in multi-threaded environments
    return this.mutex.runExclusive(async () => {
      // Resolution logic
    });
  }
}
```

**Connection Pooling**
```go
// Go - Reuse HTTP connections
type Provider struct {
    client *http.Client
}

func NewProvider() *Provider {
    return &Provider{
        client: &http.Client{
            Transport: &http.Transport{
                MaxIdleConns:        100,
                MaxIdleConnsPerHost: 100,
                IdleConnTimeout:     90 * time.Second,
            },
        },
    }
}
```

**Request-Scoped Context Propagation**
```python
# Python - Using contextvars for request context
from contextvars import ContextVar

request_context: ContextVar[EvaluationContext] = ContextVar('request_context')

@app.middleware("http")
async def add_context(request: Request, call_next):
    context = EvaluationContext(
        targeting_key=request.user.id,
        attributes={"path": request.url.path}
    )
    token = request_context.set(context)
    try:
        response = await call_next(request)
    finally:
        request_context.reset(token)
    return response
```

### Server SDK Checklist

- [ ] Thread-safe provider implementation
- [ ] Connection pooling for external calls
- [ ] Request context propagation
- [ ] Graceful shutdown with in-flight request handling
- [ ] Metrics/telemetry per evaluation
- [ ] Bulk evaluation support (optional)
- [ ] Caching strategy for high-throughput

---

## Client SDK Implementation

Client SDKs use the **static-context paradigm** where context is set once and cached. This pattern is used for mobile apps, browser applications, and edge devices.

### Key Characteristics

| Aspect | Client SDK Behavior |
|--------|---------------------|
| Context | Set once, cached until changed |
| State | Stateful, maintains flag cache |
| Concurrency | Single-threaded (usually) |
| Users | Single user/device per instance |
| Lifecycle | Application lifecycle (may be short-lived) |

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Client Application                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                  EvaluationContext                    │   │
│  │  (Set once: user ID, device, app version, etc.)      │   │
│  └──────────────────────┬───────────────────────────────┘   │
│                         │                                    │
│                         ▼                                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │               OpenFeature API                         │   │
│  │  ┌────────────────────────────────────────────────┐  │   │
│  │  │              Flag Cache                         │  │   │
│  │  │  (Evaluated flags stored locally)              │  │   │
│  │  └────────────────────────────────────────────────┘  │   │
│  └──────────────────────┬───────────────────────────────┘   │
│                         │                                    │
│                         ▼                                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                    Provider                           │   │
│  │  (Syncs with server, manages local cache)            │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Client SDK Requirements

```typescript
// Static-context evaluation signature (no context parameter)
interface ClientSdkClient {
  getBooleanValue(
    flagKey: string,
    defaultValue: boolean,
    options?: EvaluationOptions
  ): boolean;  // Synchronous - uses cached values
}

// Context set at initialization or on user change
OpenFeature.setContext({
  targetingKey: user.id,
  email: user.email,
  deviceType: 'mobile',
  appVersion: '2.1.0',
});

// Evaluations use cached context
const enabled = client.getBooleanValue('new-feature', false);
```

### Client-Specific Events

```typescript
// Additional events for client SDKs
enum ClientProviderEvent {
  // Standard events
  PROVIDER_READY = 'PROVIDER_READY',
  PROVIDER_ERROR = 'PROVIDER_ERROR',
  PROVIDER_STALE = 'PROVIDER_STALE',

  // Client-specific events
  PROVIDER_RECONCILING = 'PROVIDER_RECONCILING',      // Context change in progress
  PROVIDER_CONTEXT_CHANGED = 'PROVIDER_CONTEXT_CHANGED', // Context change complete
}

// Listen for context reconciliation
client.addHandler(ProviderEvent.PROVIDER_CONTEXT_CHANGED, () => {
  // Re-render UI with new flag values
  refreshUI();
});
```

### Context Reconciliation

When context changes, client SDKs must reconcile cached values:

```typescript
interface ClientProvider extends FeatureProvider {
  // Called when context changes
  onContextChange(
    oldContext: EvaluationContext,
    newContext: EvaluationContext
  ): Promise<void>;
}

class MyClientProvider implements ClientProvider {
  private cache: Map<string, ResolutionDetails<FlagValue>> = new Map();

  async onContextChange(
    oldContext: EvaluationContext,
    newContext: EvaluationContext
  ): Promise<void> {
    // Emit RECONCILING event
    this.emit(ProviderEvent.PROVIDER_RECONCILING);

    try {
      // Fetch new flag values for new context
      const newFlags = await this.fetchFlags(newContext);
      this.cache = new Map(newFlags);

      // Emit CONTEXT_CHANGED event
      this.emit(ProviderEvent.PROVIDER_CONTEXT_CHANGED);
    } catch (error) {
      this.emit(ProviderEvent.PROVIDER_ERROR, { error });
    }
  }
}
```

### Platform-Specific Patterns

**Mobile (iOS/Android)**
```swift
// Swift - iOS lifecycle handling
class OpenFeatureManager {
    func applicationDidBecomeActive() {
        // Refresh flags when app becomes active
        provider.refresh()
    }

    func applicationDidEnterBackground() {
        // Persist cache before backgrounding
        provider.persistCache()
    }
}
```

```kotlin
// Kotlin - Android lifecycle
class FeatureFlagViewModel : ViewModel() {
    private val client = OpenFeature.getClient()

    init {
        // Observe provider events
        OpenFeature.addHandler(ProviderEvent.PROVIDER_READY) {
            refreshFlags()
        }
    }

    override fun onCleared() {
        // Cleanup when ViewModel is destroyed
        OpenFeature.shutdown()
    }
}
```

**Browser/Web**
```typescript
// Handle page visibility changes
document.addEventListener('visibilitychange', () => {
  if (document.visibilityState === 'visible') {
    // Refresh flags when tab becomes visible
    provider.refresh();
  }
});

// Handle online/offline
window.addEventListener('online', () => {
  provider.reconnect();
});

window.addEventListener('offline', () => {
  // Use cached values, emit STALE if needed
  provider.setStatus(ProviderStatus.STALE);
});
```

**Edge/Embedded**
```rust
// Rust - Resource-constrained environments
pub struct EdgeProvider {
    cache: HashMap<String, FlagValue>,
    max_cache_size: usize,
    storage: Box<dyn PersistentStorage>,
}

impl EdgeProvider {
    pub fn new(max_cache_size: usize) -> Self {
        Self {
            cache: HashMap::with_capacity(max_cache_size),
            max_cache_size,
            storage: Box::new(FileStorage::new("/data/flags")),
        }
    }

    // Load from persistent storage on init
    pub async fn initialize(&mut self) -> Result<(), Error> {
        self.cache = self.storage.load().await?;
        Ok(())
    }
}
```

### Offline Support

```typescript
interface OfflineCapableProvider extends ClientProvider {
  // Check if operating offline
  isOffline(): boolean;

  // Get cached value (works offline)
  getCachedValue<T>(flagKey: string): T | undefined;

  // Queue context changes for when online
  queueContextChange(context: EvaluationContext): void;
}

class OfflineProvider implements OfflineCapableProvider {
  private pendingContext: EvaluationContext | null = null;

  async onContextChange(old: EvaluationContext, new_: EvaluationContext) {
    if (this.isOffline()) {
      this.pendingContext = new_;
      return; // Will reconcile when back online
    }
    await this.reconcile(new_);
  }

  async onOnline() {
    if (this.pendingContext) {
      await this.reconcile(this.pendingContext);
      this.pendingContext = null;
    }
  }
}
```

### Client SDK Checklist

- [ ] Static-context evaluation methods (no context param)
- [ ] Context reconciliation (`onContextChange`)
- [ ] RECONCILING and CONTEXT_CHANGED events
- [ ] Local flag cache
- [ ] Persistent storage for offline support
- [ ] Application lifecycle handling
- [ ] Network state awareness (online/offline)
- [ ] Background refresh strategies
- [ ] Memory-efficient caching (size limits)
- [ ] Synchronous evaluation from cache

---

## Language-Specific Considerations

### Static vs Dynamic Typing

**Statically Typed (Go, Rust, Java, TypeScript)**
- Use generics for type-safe evaluation
- Compile-time type checking preferred
- Requirement 2.2.8.1: Support generic resolution details

**Dynamically Typed (Python, Ruby, JavaScript)**
- Runtime type checking in evaluation
- Duck typing for providers
- Clear documentation of expected types

### Concurrency Models

**Single-threaded (JavaScript/Browser)**
- Async/await for provider operations
- Event loop considerations
- Requirement 1.4.12: Provide async mechanisms

**Multi-threaded (Go, Rust, Java)**
- Thread-safe singleton implementation
- Concurrent provider access
- Lock-free where possible

### Error Handling Idioms

**Exceptions (Java, Python, C#)**
- Catch and suppress in evaluation
- Return defaults on any exception

**Result Types (Rust, Go)**
- Map errors to default values
- Error details in resolution structure

### Memory Management

**Garbage Collected (Java, Go, Python)**
- Standard cleanup in shutdown

**Manual/RAII (Rust, C++)**
- Implement Drop/destructor
- Consider Rc/Arc for shared providers

## References

- [OpenFeature Specification](https://openfeature.dev/specification/)
- [Flag Evaluation API](https://openfeature.dev/specification/sections/flag-evaluation)
- [Provider Interface](https://openfeature.dev/specification/sections/providers)
- [Hooks](https://openfeature.dev/specification/sections/hooks)
- [Evaluation Context](https://openfeature.dev/specification/sections/evaluation-context)
- [Events](https://openfeature.dev/specification/sections/events)
- [Types and Data Structures](https://openfeature.dev/specification/types)
- [Gherkin Test Suites](https://openfeature.dev/specification/appendix-b)
- [Official SDK Repositories](https://github.com/open-feature)
