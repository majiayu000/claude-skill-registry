---
name: setup-feature-flags
description: "Step-by-step guide for implementing feature flags to decouple deployment from release with safe rollouts and kill switches using cloud-agnostic patterns."
---

# Skill: Setup Feature Flags

This skill teaches you how to implement feature flags in services following  patterns. You'll learn to decouple deployment from release, enable gradual rollouts, implement kill switches, and create cleanup processes.

## Prerequisites

- Understanding of Clean Architecture principles
- Cloud configuration service access (AppConfig, GCP Runtime Config, Azure App Configuration)
- Service structured with Clean Architecture layers

## Step 1: Define Flag Structure

```pseudocode
TYPE FlagKey
    NEW_BILLING_ENGINE = "new-billing-engine"
    ASYNC_PROCESSING = "async-processing"
    ENHANCED_VALIDATION = "enhanced-validation"
END TYPE

TYPE FlagState
    ENABLED = "enabled"
    DISABLED = "disabled"
    ROLLOUT = "rollout"
END TYPE

TYPE FlagConfig
    key: FlagKey
    description: String
    defaultValue: Boolean
    state: FlagState
    rolloutPercentage: Int
    expiresAt: DateTime (optional)
    owner: String
    cleanupTicket: String (optional)
END TYPE

TYPE EvaluationContext
    userId: String
    tenantId: String
    environment: String

CONSTRUCTOR NewEvaluationContext(userId: String, tenantId: String, env: String) RETURNS EvaluationContext
    RETURN EvaluationContext{userId: userId, tenantId: tenantId, environment: env}
END CONSTRUCTOR
```

### Flag Registry

```pseudocode
TYPE FlagRegistry
    flags: Map<FlagKey, FlagConfig>

CONSTRUCTOR NewFlagRegistry() RETURNS FlagRegistry
    now = CurrentTime()
    RETURN FlagRegistry{
        flags: {
            FlagKey.NEW_BILLING_ENGINE: FlagConfig{
                key: FlagKey.NEW_BILLING_ENGINE,
                description: "Enables the new billing calculation engine",
                defaultValue: FALSE,
                state: FlagState.DISABLED,
                expiresAt: now.AddMonths(3),
                owner: "billing-team",
                cleanupTicket: "JIRA-1234"
            }
        }
    }
END CONSTRUCTOR

METHOD FlagRegistry.Get(key: FlagKey) RETURNS Result<FlagConfig, Error>
    config = this.flags[key]
    IF config IS NULL THEN
        RETURN Error("unknown flag: " + key)
    END IF
    RETURN Ok(config)
END METHOD

METHOD FlagRegistry.ExpiredFlags() RETURNS List<FlagConfig>
    expired = NewList()
    now = CurrentTime()
    FOR EACH config IN this.flags.Values() DO
        IF config.expiresAt IS NOT NULL AND config.expiresAt.Before(now) THEN
            expired.Add(config)
        END IF
    END FOR
    RETURN expired
END METHOD
```

## Step 2: Implement Flag Client

```pseudocode
INTERFACE FeatureFlagClient
    METHOD IsEnabled(ctx: Context, key: FlagKey, evalCtx: EvaluationContext) RETURNS Boolean
    METHOD Close() RETURNS Result<Void, Error>
END INTERFACE
```

### In-Memory Implementation

```pseudocode
TYPE InMemoryClient IMPLEMENTS FeatureFlagClient
    registry: FlagRegistry
    overrides: Map<FlagKey, Boolean>
    mutex: Mutex

CONSTRUCTOR NewInMemoryClient(registry: FlagRegistry) RETURNS InMemoryClient
    RETURN InMemoryClient{
        registry: registry,
        overrides: NewMap()
    }
END CONSTRUCTOR

METHOD InMemoryClient.IsEnabled(ctx: Context, key: FlagKey, evalCtx: EvaluationContext) RETURNS Boolean
    this.mutex.RLock()
    override, hasOverride = this.overrides[key]
    this.mutex.RUnlock()

    IF hasOverride THEN
        RETURN override
    END IF

    configResult = this.registry.Get(key)
    IF configResult.IsError() THEN
        RETURN FALSE
    END IF

    config = configResult.Value()

    SWITCH config.state
        CASE FlagState.ENABLED:
            RETURN TRUE
        CASE FlagState.DISABLED:
            RETURN FALSE
        CASE FlagState.ROLLOUT:
            hash = FNVHash32(evalCtx.userId)
            RETURN (hash MOD 100) < config.rolloutPercentage
    END SWITCH

    RETURN config.defaultValue
END METHOD

METHOD InMemoryClient.SetOverride(key: FlagKey, enabled: Boolean)
    this.mutex.Lock()
    this.overrides[key] = enabled
    this.mutex.Unlock()
END METHOD

METHOD InMemoryClient.Close() RETURNS Result<Void, Error>
    RETURN Ok(Void)
END METHOD
```

## Step 3: Add Flag Middleware

```pseudocode
TYPE ContextKey
    FLAG_CONTEXT = "feature_flags_context"
    FLAG_CLIENT = "feature_flags_client"
END TYPE

TYPE FlagMiddleware
    client: FeatureFlagClient
    next: APIHandlerFunc

CONSTRUCTOR NewFlagMiddleware(client: FeatureFlagClient, next: APIHandlerFunc) RETURNS FlagMiddleware
    RETURN FlagMiddleware{client: client, next: next}
END CONSTRUCTOR

METHOD FlagMiddleware.Handle(ctx: Context, request: APIRequest) RETURNS Result<APIResponse, Error>
    evalCtx = NewEvaluationContext(
        request.Headers["x-user-id"],
        request.Headers["x-tenant-id"],
        "production"
    )
    ctx = ctx.WithValue(ContextKey.FLAG_CONTEXT, evalCtx)
    ctx = ctx.WithValue(ContextKey.FLAG_CLIENT, this.client)
    RETURN this.next(ctx, request)
END METHOD

FUNCTION IsEnabled(ctx: Context, key: FlagKey) RETURNS Boolean
    client = ctx.Value(ContextKey.FLAG_CLIENT) AS FeatureFlagClient
    IF client IS NULL THEN
        RETURN FALSE
    END IF

    evalCtx = ctx.Value(ContextKey.FLAG_CONTEXT) AS EvaluationContext
    IF evalCtx IS NULL THEN
        evalCtx = NewEvaluationContext("", "", "production")
    END IF

    RETURN client.IsEnabled(ctx, key, evalCtx)
END FUNCTION
```

## Step 4: Use Flags in Application Code

```pseudocode
INTERFACE PaymentEngine
    METHOD Process(ctx: Context, amount: Decimal, currency: String) RETURNS Result<PaymentResult, Error>
END INTERFACE

TYPE ProcessPaymentUseCase
    flagClient: FeatureFlagClient
    oldEngine: PaymentEngine
    newEngine: PaymentEngine

METHOD ProcessPaymentUseCase.Execute(ctx: Context, cmd: ProcessPaymentCommand) RETURNS Result<ProcessPaymentResult, Error>
    evalCtx = ctx.Value(ContextKey.FLAG_CONTEXT) AS EvaluationContext
    IF evalCtx IS NULL THEN
        evalCtx = NewEvaluationContext("", "", "production")
    END IF

    engine: PaymentEngine
    IF this.flagClient.IsEnabled(ctx, FlagKey.NEW_BILLING_ENGINE, evalCtx) THEN
        engine = this.newEngine
    ELSE
        engine = this.oldEngine
    END IF

    result = engine.Process(ctx, cmd.Amount, cmd.Currency)
    IF result.IsError() THEN
        RETURN Error("payment processing failed: " + result.Error().Message())
    END IF

    RETURN Ok(ProcessPaymentResult{
        transactionId: result.Value().Id,
        status: result.Value().Status
    })
END METHOD
```

## Step 5: Test with Feature Flags

```pseudocode
FUNCTION TestProcessPayment_UsesCorrectEngine()
    registry = NewFlagRegistry()
    flagClient = NewInMemoryClient(registry)

    testCases = [
        {name: "new engine when enabled", flagEnabled: TRUE, expectNew: TRUE},
        {name: "old engine when disabled", flagEnabled: FALSE, expectNew: FALSE}
    ]

    FOR EACH tc IN testCases DO
        flagClient.SetOverride(FlagKey.NEW_BILLING_ENGINE, tc.flagEnabled)
        evalCtx = NewEvaluationContext("user-123", "tenant-1", "test")
        result = flagClient.IsEnabled(BackgroundContext(), FlagKey.NEW_BILLING_ENGINE, evalCtx)
        AssertEqual(tc.expectNew, result)
    END FOR
END FUNCTION

FUNCTION TestRollout_IsDeterministic()
    registry = NewFlagRegistry()
    flagClient = NewInMemoryClient(registry)
    evalCtx = NewEvaluationContext("user-123", "tenant-1", "test")

    result1 = flagClient.IsEnabled(BackgroundContext(), FlagKey.ASYNC_PROCESSING, evalCtx)
    result2 = flagClient.IsEnabled(BackgroundContext(), FlagKey.ASYNC_PROCESSING, evalCtx)

    AssertEqual(result1, result2, "same user should get consistent results")
END FUNCTION
```

## Step 6: Create Cleanup Process

```pseudocode
FUNCTION CleanupExpiredFlags()
    logger = NewJsonLogger(stdout)
    registry = NewFlagRegistry()

    expired = registry.ExpiredFlags()
    IF expired.IsEmpty() THEN
        logger.Info("no expired flags found")
        RETURN
    END IF

    FOR EACH flag IN expired DO
        logger.Warn("expired flag", {
            "key": flag.key,
            "owner": flag.owner
        })
        IF CurrentTime().Since(flag.expiresAt) > 30 * Day THEN
            Exit(1)  // Fail build if flags are way past expiration
        END IF
    END FOR
END FUNCTION
```

## Verification Checklist

- [ ] Flag keys are typed constants
- [ ] All flags have owners and cleanup tickets
- [ ] Expiration dates set for temporary flags
- [ ] Flag client abstraction allows swapping implementations
- [ ] Middleware extracts user context for targeting
- [ ] Rollout uses consistent hashing
- [ ] Kill switches return 503
- [ ] Tests verify enabled AND disabled states
- [ ] Cleanup process runs in CI
- [ ] Flag changes don't require redeployment
