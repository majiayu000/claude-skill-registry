---
name: implement-saga-orchestration
description: "Step-by-step guide for implementing orchestrated sagas with state machines and compensating actions."
---

# Skill: Implement Saga Orchestration

This skill teaches you how to implement the Saga pattern using orchestration for coordinating multi-step business transactions. You'll learn to design state machines with compensating actions that ensure eventual consistency without distributed transactions.

Sagas are essential when a business process spans multiple services and must maintain consistency. Unlike traditional transactions, sagas achieve this through compensation - if a step fails, you run compensating actions for all previously completed steps in reverse order.

## Prerequisites

- Understanding of Clean Architecture and domain-driven design
- Familiarity with state machines and workflow orchestration
- Knowledge of the Idempotency pattern
- A multi-step business process that spans multiple services

## Overview

In this skill, you will:
1. Identify saga steps and their compensations
2. Design the state machine definition
3. Implement forward step handlers
4. Implement compensation handlers
5. Wire error handling and catch blocks
6. Add idempotency to all handlers
7. Test the complete saga flow

## Step 1: Identify Saga Steps and Compensations

Before writing code, map each forward step to its compensating action. Every step that modifies state must have a compensation.

### Asset Registration Saga Example

This saga registers a new energy asset across multiple systems:

```text
Forward Steps:
  1. ValidateAsset         -> compensation: none (read-only, no state change)
  2. CreateAssetRecord     -> compensation: DeleteAssetRecord
  3. RegisterWithGrid      -> compensation: UnregisterFromGrid
  4. ActivateMonitoring    -> compensation: DeactivateMonitoring

If ActivateMonitoring fails:
  -> DeactivateMonitoring (if started)
  -> UnregisterFromGrid
  -> DeleteAssetRecord
```

Key principles:
- Read-only steps (validation) don't need compensation
- Compensation undoes the effect of the forward step
- Compensations run in reverse order
- All compensations must be idempotent

### Define Step Types

```pseudocode
// SagaStep defines a step in the saga with its compensation
TYPE SagaStep
    name: String
    forward: String             // Handler name for forward action
    compensation: String        // Handler name for compensation (empty if none)
    requiresUndo: Boolean       // Whether this step needs compensation on failure

// AssetRegistrationSaga defines the steps for asset registration
CONSTANT AssetRegistrationSaga = [
    SagaStep{name: "ValidateAsset", forward: "validate-asset", compensation: "", requiresUndo: false},
    SagaStep{name: "CreateAssetRecord", forward: "create-asset", compensation: "delete-asset", requiresUndo: true},
    SagaStep{name: "RegisterWithGrid", forward: "register-grid", compensation: "unregister-grid", requiresUndo: true},
    SagaStep{name: "ActivateMonitoring", forward: "activate-monitoring", compensation: "deactivate-monitoring", requiresUndo: true}
]

// SagaInput is the input to the saga state machine
TYPE SagaInput
    assetId: String
    facilityId: String
    assetType: String
    capacityKWh: Float
    gridZone: String
    correlationId: String

// SagaState tracks which steps have completed for compensation
TYPE SagaState
    input: SagaInput
    completedSteps: List<String>
    currentStep: String
    error: String
    gridRegistration: String
    monitoringId: String
```

## Step 2: Design the State Machine Definition

Create the state machine definition. The orchestrator owns the flow but delegates all business logic to step handlers.

```pseudocode
// State machine definition in declarative format
TYPE StateMachineDefinition
    comment: String
    startAt: String
    states: Map<String, State>

TYPE State
    type: String                // "Task", "Fail", "Succeed", "Choice"
    resource: String            // Handler reference
    next: String                // Next state
    catch: List<CatchBlock>     // Error handling
    resultPath: String          // Where to store result

TYPE CatchBlock
    errorEquals: List<String>   // Error types to catch
    resultPath: String          // Where to store error
    next: String                // State to transition to

// Asset Registration State Machine
CONSTANT AssetRegistrationStateMachine = StateMachineDefinition{
    comment: "Asset Registration Saga - orchestrates registration with compensation",
    startAt: "ValidateAsset",
    states: {
        "ValidateAsset": State{
            type: "Task",
            resource: "validate-asset",
            next: "CreateAssetRecord",
            catch: [
                CatchBlock{errorEquals: ["ValidationError"], next: "ValidationFailed"},
                CatchBlock{errorEquals: ["ALL"], next: "HandleUnexpectedError"}
            ],
            resultPath: "$.validation"
        },
        "CreateAssetRecord": State{
            type: "Task",
            resource: "create-asset",
            next: "RegisterWithGrid",
            catch: [
                CatchBlock{errorEquals: ["ALL"], resultPath: "$.error", next: "HandleUnexpectedError"}
            ],
            resultPath: "$.asset_record"
        },
        "RegisterWithGrid": State{
            type: "Task",
            resource: "register-grid",
            next: "ActivateMonitoring",
            catch: [
                CatchBlock{errorEquals: ["GridRegistrationError"], resultPath: "$.error", next: "CompensateCreateAssetRecord"},
                CatchBlock{errorEquals: ["ALL"], resultPath: "$.error", next: "CompensateCreateAssetRecord"}
            ],
            resultPath: "$.grid_registration"
        },
        "ActivateMonitoring": State{
            type: "Task",
            resource: "activate-monitoring",
            next: "SagaSuccess",
            catch: [
                CatchBlock{errorEquals: ["ALL"], resultPath: "$.error", next: "CompensateRegisterWithGrid"}
            ],
            resultPath: "$.monitoring"
        },
        "CompensateRegisterWithGrid": State{
            type: "Task",
            resource: "unregister-grid",
            next: "CompensateCreateAssetRecord",
            catch: [
                CatchBlock{errorEquals: ["ALL"], resultPath: "$.compensation_error", next: "CompensateCreateAssetRecord"}
            ],
            resultPath: "$.compensation.grid"
        },
        "CompensateCreateAssetRecord": State{
            type: "Task",
            resource: "delete-asset",
            next: "SagaFailed",
            catch: [
                CatchBlock{errorEquals: ["ALL"], resultPath: "$.compensation_error", next: "SagaFailed"}
            ],
            resultPath: "$.compensation.asset"
        },
        "ValidationFailed": State{
            type: "Fail",
            error: "ValidationError",
            cause: "Asset validation failed - no compensation needed"
        },
        "HandleUnexpectedError": State{
            type: "Fail",
            error: "UnexpectedError",
            cause: "Unexpected error during saga execution"
        },
        "SagaFailed": State{
            type: "Fail",
            error: "SagaFailed",
            cause: "Saga failed after compensation"
        },
        "SagaSuccess": State{
            type: "Succeed"
        }
    }
}
```

The state machine demonstrates key patterns:
- Each forward step catches errors and routes to appropriate compensation
- Compensation steps form a reverse chain
- Compensation errors don't stop the compensation chain
- Clear terminal states for success and failure

## Step 3: Implement Forward Step Handlers

Each handler performs one step of the saga. They receive the saga state and return updated state.

### ValidateAsset Handler

```pseudocode
// ValidationError is returned for invalid assets
TYPE ValidationError
    field: String
    message: String

METHOD ValidationError.Error() RETURNS String
    RETURN "validation failed: " + this.field + " - " + this.message
END METHOD

// ValidationResult is the output of validation
TYPE ValidationResult
    valid: Boolean
    assetId: String
    validatedAt: String

// Validate asset handler
FUNCTION HandleValidateAsset(ctx: Context, input: SagaInput) RETURNS Result<ValidationResult, Error>
    // Generate asset ID if not provided
    IF input.assetId == "" THEN
        input.assetId = GenerateUUID()
    END IF

    // Validate required fields
    IF input.facilityId == "" THEN
        RETURN Error(ValidationError{field: "facility_id", message: "facility ID is required"})
    END IF

    IF input.assetType == "" THEN
        RETURN Error(ValidationError{field: "asset_type", message: "asset type is required"})
    END IF

    validTypes = ["battery", "solar", "wind", "ev_charger"]
    IF NOT validTypes.Contains(input.assetType) THEN
        RETURN Error(ValidationError{field: "asset_type", message: "invalid asset type"})
    END IF

    IF input.capacityKWh <= 0 THEN
        RETURN Error(ValidationError{field: "capacity_kwh", message: "capacity must be positive"})
    END IF

    IF input.gridZone == "" THEN
        RETURN Error(ValidationError{field: "grid_zone", message: "grid zone is required"})
    END IF

    // Validation passed - no state changed, no compensation needed
    RETURN Ok(ValidationResult{
        valid: true,
        assetId: input.assetId,
        validatedAt: FormatTimestamp(CurrentTimestamp())
    })
END FUNCTION
```

### CreateAssetRecord Handler

```pseudocode
TYPE SagaStateWithValidation
    input: SagaInput
    validation: ValidationResult

TYPE AssetRecord
    assetId: String
    createdAt: String
    recordToken: String         // For idempotency

FUNCTION HandleCreateAssetRecord(ctx: Context, state: SagaStateWithValidation) RETURNS Result<AssetRecord, Error>
    assetId = state.validation.assetId
    IF assetId == "" THEN
        assetId = GenerateUUID()
    END IF

    // Generate idempotency token based on correlation ID
    recordToken = state.input.correlationId + "-" + assetId

    // Check if already created (idempotency)
    existingResult = dataStore.GetItem(ctx, GetItemInput{
        tableName: tableName,
        key: {
            "PK": "ASSET#" + assetId,
            "SK": "METADATA"
        }
    })

    IF existingResult.IsOk() AND existingResult.Value().Item != NULL THEN
        // Already exists - return existing record (idempotent)
        RETURN Ok(AssetRecord{
            assetId: assetId,
            createdAt: existingResult.Value().Item.createdAt,
            recordToken: recordToken
        })
    END IF

    now = FormatTimestamp(CurrentTimestamp())

    // Create asset record
    item = {
        "PK": "ASSET#" + assetId,
        "SK": "METADATA",
        "facility_id": state.input.facilityId,
        "asset_type": state.input.assetType,
        "capacity_kwh": state.input.capacityKWh,
        "grid_zone": state.input.gridZone,
        "created_at": now,
        "record_token": recordToken,
        "status": "pending_registration"
    }

    result = dataStore.PutItem(ctx, PutItemInput{
        tableName: tableName,
        item: item,
        conditionExpression: "attribute_not_exists(PK)"
    })

    IF result.IsError() THEN
        RETURN Error("failed to create asset record: " + result.Error())
    END IF

    RETURN Ok(AssetRecord{
        assetId: assetId,
        createdAt: now,
        recordToken: recordToken
    })
END FUNCTION
```

### RegisterWithGrid Handler

```pseudocode
// GridRegistrationError indicates grid registration failure
TYPE GridRegistrationError
    code: String
    message: String

METHOD GridRegistrationError.Error() RETURNS String
    RETURN "grid registration failed: " + this.code + " - " + this.message
END METHOD

TYPE SagaStateWithAsset
    input: SagaInput
    assetRecord: AssetRecord

TYPE GridRegistration
    registrationId: String
    gridZone: String
    registeredAt: String
    status: String

FUNCTION HandleRegisterWithGrid(ctx: Context, state: SagaStateWithAsset) RETURNS Result<GridRegistration, Error>
    // Call external grid operator API
    reqBody = {
        "asset_id": state.assetRecord.assetId,
        "asset_type": state.input.assetType,
        "capacity_kwh": state.input.capacityKWh,
        "grid_zone": state.input.gridZone,
        "idempotency_key": state.assetRecord.recordToken
    }

    response = httpClient.POST(gridAPIURL + "/registrations", HTTPRequest{
        body: SerializeJSON(reqBody),
        headers: {
            "Content-Type": "application/json",
            "X-Idempotency-Key": state.assetRecord.recordToken
        }
    })

    IF response.IsError() THEN
        RETURN Error("grid API call failed: " + response.Error())
    END IF

    IF response.StatusCode == 409 THEN
        // Already registered - idempotent success
        result = DeserializeJSON<GridRegistration>(response.Body)
        RETURN Ok(result)
    END IF

    IF response.StatusCode != 201 AND response.StatusCode != 200 THEN
        RETURN Error(GridRegistrationError{
            code: "HTTP_" + ToString(response.StatusCode),
            message: "grid operator rejected registration"
        })
    END IF

    result = DeserializeJSON<GridRegistration>(response.Body)
    RETURN Ok(result)
END FUNCTION
```

### ActivateMonitoring Handler

```pseudocode
TYPE SagaStateWithGrid
    input: SagaInput
    assetRecord: AssetRecord
    gridRegistration: GridRegistration

TYPE MonitoringActivation
    monitoringId: String
    assetId: String
    activatedAt: String
    status: String

FUNCTION HandleActivateMonitoring(ctx: Context, state: SagaStateWithGrid) RETURNS Result<MonitoringActivation, Error>
    assetId = state.assetRecord.assetId
    monitoringId = "MON-" + GenerateUUID()[0:8]
    now = FormatTimestamp(CurrentTimestamp())

    // Create monitoring record
    monitoringItem = {
        "PK": "MONITORING#" + monitoringId,
        "SK": "CONFIG",
        "asset_id": assetId,
        "registration_id": state.gridRegistration.registrationId,
        "activated_at": now,
        "status": "active",
        "idempotency_key": state.assetRecord.recordToken
    }

    result = dataStore.PutItem(ctx, PutItemInput{
        tableName: monitoringTable,
        item: monitoringItem
    })

    IF result.IsError() THEN
        RETURN Error("failed to create monitoring: " + result.Error())
    END IF

    // Update asset status to active
    updateResult = dataStore.UpdateItem(ctx, UpdateItemInput{
        tableName: assetTable,
        key: {
            "PK": "ASSET#" + assetId,
            "SK": "METADATA"
        },
        updateExpression: "SET #status = :status, monitoring_id = :mid",
        expressionAttributeNames: {"#status": "status"},
        expressionAttributeValues: {
            ":status": "active",
            ":mid": monitoringId
        }
    })

    IF updateResult.IsError() THEN
        RETURN Error("failed to update asset status: " + updateResult.Error())
    END IF

    RETURN Ok(MonitoringActivation{
        monitoringId: monitoringId,
        assetId: assetId,
        activatedAt: now,
        status: "active"
    })
END FUNCTION
```

## Step 4: Implement Compensation Handlers

Compensation handlers undo the effects of forward steps. They must be idempotent - running them multiple times should have the same effect as running once.

### DeleteAssetRecord (Compensates CreateAssetRecord)

```pseudocode
TYPE CompensationInput
    assetRecord: AssetRecord
    error: ErrorInfo

TYPE ErrorInfo
    cause: String

TYPE CompensationResult
    compensated: Boolean
    assetId: String
    compensatedAt: String

FUNCTION HandleDeleteAssetRecord(ctx: Context, input: CompensationInput) RETURNS Result<CompensationResult, Error>
    assetId = input.assetRecord.assetId

    // Check if record exists (idempotency - might already be deleted)
    existingResult = dataStore.GetItem(ctx, GetItemInput{
        tableName: assetTable,
        key: {
            "PK": "ASSET#" + assetId,
            "SK": "METADATA"
        }
    })

    IF existingResult.IsError() THEN
        RETURN Error("failed to check asset: " + existingResult.Error())
    END IF

    IF existingResult.Value().Item == NULL THEN
        // Already deleted - idempotent success
        RETURN Ok(CompensationResult{
            compensated: true,
            assetId: assetId,
            compensatedAt: FormatTimestamp(CurrentTimestamp())
        })
    END IF

    // Soft delete - mark as compensated rather than hard delete
    result = dataStore.UpdateItem(ctx, UpdateItemInput{
        tableName: assetTable,
        key: {
            "PK": "ASSET#" + assetId,
            "SK": "METADATA"
        },
        updateExpression: "SET #status = :status, compensated_at = :cat, compensation_reason = :reason",
        expressionAttributeNames: {"#status": "status"},
        expressionAttributeValues: {
            ":status": "compensated",
            ":cat": FormatTimestamp(CurrentTimestamp()),
            ":reason": input.error.cause
        }
    })

    IF result.IsError() THEN
        RETURN Error("failed to compensate asset: " + result.Error())
    END IF

    RETURN Ok(CompensationResult{
        compensated: true,
        assetId: assetId,
        compensatedAt: FormatTimestamp(CurrentTimestamp())
    })
END FUNCTION
```

### UnregisterFromGrid (Compensates RegisterWithGrid)

```pseudocode
TYPE GridCompensationInput
    gridRegistration: GridRegistration
    assetRecord: AssetRecord
    error: ErrorInfo

TYPE GridCompensationResult
    unregistered: Boolean
    registrationId: String
    unregisteredAt: String

FUNCTION HandleUnregisterFromGrid(ctx: Context, input: GridCompensationInput) RETURNS Result<GridCompensationResult, Error>
    registrationId = input.gridRegistration.registrationId

    IF registrationId == "" THEN
        // No registration to undo - idempotent success
        RETURN Ok(GridCompensationResult{
            unregistered: true,
            unregisteredAt: FormatTimestamp(CurrentTimestamp())
        })
    END IF

    // Call grid API to unregister
    reqBody = {
        "reason": "saga_compensation",
        "idempotency_key": input.assetRecord.recordToken + "-unregister"
    }

    url = gridAPIURL + "/registrations/" + registrationId
    response = httpClient.DELETE(url, HTTPRequest{
        body: SerializeJSON(reqBody),
        headers: {
            "Content-Type": "application/json",
            "X-Idempotency-Key": input.assetRecord.recordToken + "-unregister"
        }
    })

    IF response.IsError() THEN
        RETURN Error("grid API call failed: " + response.Error())
    END IF

    // 404 means already unregistered - idempotent success
    IF response.StatusCode == 404 OR response.StatusCode == 204 OR response.StatusCode == 200 THEN
        RETURN Ok(GridCompensationResult{
            unregistered: true,
            registrationId: registrationId,
            unregisteredAt: FormatTimestamp(CurrentTimestamp())
        })
    END IF

    RETURN Error("grid unregistration failed with status " + ToString(response.StatusCode))
END FUNCTION
```

### DeactivateMonitoring (Compensates ActivateMonitoring)

```pseudocode
TYPE MonitoringCompensationInput
    monitoring: MonitoringInfo
    assetRecord: AssetRecord
    error: ErrorInfo

TYPE MonitoringInfo
    monitoringId: String
    assetId: String

TYPE MonitoringCompensationResult
    deactivated: Boolean
    monitoringId: String
    deactivatedAt: String

FUNCTION HandleDeactivateMonitoring(ctx: Context, input: MonitoringCompensationInput) RETURNS Result<MonitoringCompensationResult, Error>
    monitoringId = input.monitoring.monitoringId

    IF monitoringId == "" THEN
        // No monitoring to deactivate - idempotent success
        RETURN Ok(MonitoringCompensationResult{
            deactivated: true,
            deactivatedAt: FormatTimestamp(CurrentTimestamp())
        })
    END IF

    // Update monitoring status to deactivated
    result = dataStore.UpdateItem(ctx, UpdateItemInput{
        tableName: monitoringTable,
        key: {
            "PK": "MONITORING#" + monitoringId,
            "SK": "CONFIG"
        },
        updateExpression: "SET #status = :status, deactivated_at = :dat, deactivation_reason = :reason",
        expressionAttributeNames: {"#status": "status"},
        expressionAttributeValues: {
            ":status": "deactivated",
            ":dat": FormatTimestamp(CurrentTimestamp()),
            ":reason": "saga_compensation: " + input.error.cause
        }
    })

    IF result.IsError() THEN
        RETURN Error("failed to deactivate monitoring: " + result.Error())
    END IF

    RETURN Ok(MonitoringCompensationResult{
        deactivated: true,
        monitoringId: monitoringId,
        deactivatedAt: FormatTimestamp(CurrentTimestamp())
    })
END FUNCTION
```

## Step 5: Start Saga Execution

Create a service to start saga executions from your application.

```pseudocode
// SagaStarter starts saga executions
INTERFACE Orchestrator
    METHOD StartExecution(ctx: Context, input: StartExecutionInput) RETURNS Result<ExecutionOutput, Error>
    METHOD DescribeExecution(ctx: Context, input: DescribeExecutionInput) RETURNS Result<ExecutionDescription, Error>
END INTERFACE

TYPE SagaStarter
    orchestrator: Orchestrator
    stateMachineId: String

CONSTRUCTOR NewSagaStarter(orchestrator: Orchestrator, stateMachineId: String) RETURNS SagaStarter
    RETURN SagaStarter{
        orchestrator: orchestrator,
        stateMachineId: stateMachineId
    }
END CONSTRUCTOR

// StartAssetRegistration starts the asset registration saga
METHOD SagaStarter.StartAssetRegistration(ctx: Context, input: SagaInput) RETURNS Result<String, Error>
    // Generate correlation ID if not provided
    IF input.correlationId == "" THEN
        input.correlationId = GenerateUUID()
    END IF

    inputJSON = SerializeJSON(input)

    // Use correlation ID as execution name for idempotency
    executionName = "asset-reg-" + input.correlationId

    result = this.orchestrator.StartExecution(ctx, StartExecutionInput{
        stateMachineId: this.stateMachineId,
        name: executionName,
        input: inputJSON
    })

    IF result.IsError() THEN
        RETURN Error("failed to start saga: " + result.Error())
    END IF

    RETURN Ok(result.Value().ExecutionId)
END METHOD

// GetExecutionStatus retrieves the status of a saga execution
METHOD SagaStarter.GetExecutionStatus(ctx: Context, executionId: String) RETURNS Result<ExecutionStatus, Error>
    result = this.orchestrator.DescribeExecution(ctx, DescribeExecutionInput{
        executionId: executionId
    })

    IF result.IsError() THEN
        RETURN Error("failed to describe execution: " + result.Error())
    END IF

    RETURN Ok(ExecutionStatus{
        executionId: executionId,
        status: result.Value().Status,
        startDate: result.Value().StartDate,
        stopDate: result.Value().StopDate,
        output: result.Value().Output,
        error: result.Value().Error
    })
END METHOD

// ExecutionStatus represents saga execution status
TYPE ExecutionStatus
    executionId: String
    status: String
    startDate: String
    stopDate: String
    output: String
    error: String
```

## Step 6: Add Observability

Track saga execution with structured logging and metrics.

```pseudocode
// LogSagaEvent logs saga events with structured data
FUNCTION LogSagaEvent(ctx: Context, event: String, data: Map<String, Any>)
    attrs = ["event", event]

    FOR EACH key, value IN data DO
        attrs.append(key, value)
    END FOR

    Logger.Info(ctx, "saga_event", attrs)
END FUNCTION

// Example usage in handler:
// LogSagaEvent(ctx, "step_started", {
//     "saga_id": correlationID,
//     "step": "CreateAssetRecord",
//     "asset_id": assetID
// })
//
// LogSagaEvent(ctx, "compensation_triggered", {
//     "saga_id": correlationID,
//     "failed_step": "RegisterWithGrid",
//     "compensation_step": "DeleteAssetRecord",
//     "error": err.Error()
// })
```

## Verification Checklist

After implementing your saga, verify:

- [ ] Every forward step that modifies state has a compensation
- [ ] All compensations are idempotent (safe to run multiple times)
- [ ] State machine catches errors at each step and routes to correct compensation
- [ ] Compensation chain runs in reverse order
- [ ] Compensation errors don't stop the compensation chain
- [ ] Correlation ID flows through all steps for tracing
- [ ] Idempotency keys prevent duplicate operations
- [ ] Forward steps don't contain compensation logic
- [ ] Orchestrator coordinates but doesn't contain business logic
- [ ] All handlers have proper error types for routing
- [ ] Execution history provides visibility into saga progress
- [ ] Failed sagas are logged with full context for debugging
