---
name: setup-contract-tests
description: "Step-by-step guide for setting up contract tests with OpenAPI, JSON Schema, and consumer-driven testing."
tools: []
context: []
---

# Skill: Setup Contract Tests

This skill teaches you how to set up comprehensive contract testing for  microservices. You'll implement consumer-driven contract tests, OpenAPI validation, event schema verification, and CI/CD integration to ensure producers and consumers stay compatible.

Contract testing is essential for microservice architectures. It verifies that service boundaries remain compatible without requiring full integration tests. By testing contracts independently, teams can develop services in parallel while maintaining confidence in their integrations.

Following  patterns, contracts are first-class artifacts stored in `/contracts/`. This includes OpenAPI specifications for HTTP APIs and JSON Schema definitions for domain events. Contract tests run in CI/CD pipelines to catch breaking changes before deployment.

## Prerequisites

- Understanding of OpenAPI 3.x specification format
- Familiarity with JSON Schema draft-07
- A microservice with defined API contracts
- CI/CD pipeline (GitHub Actions, GitLab CI, or similar)

## Overview

In this skill, you will:
1. Organize contract files (OpenAPI, JSON Schema)
2. Create consumer expectations and mock generators
3. Implement producer contract verification tests
4. Set up event schema validation
5. Configure schema registry for versioning
6. Integrate contract tests into CI/CD
7. Handle schema evolution with semantic versioning

## Step 1: Organize Contract Files

Structure your contracts directory to separate HTTP APIs from event schemas. This organization makes contracts discoverable and version-controllable.

### Directory Structure

```text
services/facility-context/
  contracts/
    api/
      openapi.yaml          # HTTP API contract
    events/
      facility.created.json # Event schemas
      facility.updated.json
      zone.added.json
    consumers/
      asset-context.pact.json  # Consumer expectations
  tests/
    contract/
      api_contract_test
      event_contract_test
      consumer_contract_test
```

### Contract Loader Utility

```pseudocode
// internal/contracts/loader

// OpenAPISpec holds a parsed OpenAPI specification.
TYPE OpenAPISpec
    doc: OpenAPIDocument
END TYPE

// LoadOpenAPISpec loads and parses an OpenAPI specification.
FUNCTION LoadOpenAPISpec(path: String) RETURNS Result<OpenAPISpec, Error>
    loader = NewOpenAPILoader()
    loader.AllowExternalRefs = TRUE

    doc = loader.LoadFromFile(path)
    IF doc.IsError() THEN
        RETURN Error("failed to load OpenAPI spec: " + doc.Error())
    END IF

    // Validate the spec itself
    validation = doc.Value().Validate(loader.Context)
    IF validation.IsError() THEN
        RETURN Error("invalid OpenAPI spec: " + validation.Error())
    END IF

    RETURN Ok(OpenAPISpec{doc: doc.Value()})
END FUNCTION

// EventSchema holds a compiled JSON Schema for event validation.
TYPE EventSchema
    schema: CompiledSchema
    name: String
END TYPE

// LoadEventSchema loads and compiles a JSON Schema for an event type.
FUNCTION LoadEventSchema(eventType: String) RETURNS Result<EventSchema, Error>
    schemaPath = "contracts/events/" + eventType + ".json"

    schemaLoader = NewJSONSchemaLoader(schemaPath)
    schema = schemaLoader.Compile()
    IF schema.IsError() THEN
        RETURN Error("failed to compile schema for " + eventType + ": " + schema.Error())
    END IF

    RETURN Ok(EventSchema{schema: schema.Value(), name: eventType})
END FUNCTION

// Validate validates a JSON document against the event schema.
METHOD EventSchema.Validate(jsonData: Bytes) RETURNS Result<Void, Error>
    documentLoader = NewBytesLoader(jsonData)
    result = this.schema.Validate(documentLoader)
    IF result.IsError() THEN
        RETURN Error("validation error: " + result.Error())
    END IF

    IF NOT result.Value().IsValid() THEN
        errMsg = ""
        FOR EACH desc IN result.Value().Errors() DO
            errMsg = errMsg + "- " + desc.Description() + "\n"
        END FOR
        RETURN Error("schema validation failed for " + this.name + ":\n" + errMsg)
    END IF

    RETURN Ok()
END METHOD
```

This loader provides utilities to work with both OpenAPI and JSON Schema contracts. The embedded filesystem allows tests to access contracts without external file dependencies.

## Step 2: Create Consumer Expectations

Consumer-driven contract testing puts consumers in charge. They define what they expect from producers, ensuring producers don't break consumer integrations.

### Consumer Contract Definition

```pseudocode
// tests/contract/consumer_expectations

// ConsumerExpectation defines what a consumer expects from a producer.
TYPE ConsumerExpectation
    consumer: String
    provider: String
    interactions: List<InteractionDef>
END TYPE

// InteractionDef describes a single request/response expectation.
TYPE InteractionDef
    description: String
    request: RequestDef
    response: ResponseDef
END TYPE

// RequestDef defines expected request parameters.
TYPE RequestDef
    method: String
    path: String
    headers: Map<String, String>
    body: JSON
END TYPE

// ResponseDef defines expected response structure.
TYPE ResponseDef
    status: Integer
    headers: Map<String, String>
    body: JSON
END TYPE

// AssetContextExpectations defines what Asset Context expects from Facility API.
FUNCTION AssetContextExpectations() RETURNS ConsumerExpectation
    RETURN ConsumerExpectation{
        consumer: "asset-context",
        provider: "facility-context",
        interactions: [
            InteractionDef{
                description: "Get facility by ID returns facility details",
                request: RequestDef{
                    method: "GET",
                    path: "/v1/facilities/fac-abc123",
                    headers: {"Accept": "application/json"}
                },
                response: ResponseDef{
                    status: 200,
                    headers: {"Content-Type": "application/json"},
                    body: {
                        "id": "fac-abc123",
                        "name": "Solar Farm Alpha",
                        "status": "active"
                    }
                }
            },
            InteractionDef{
                description: "Get non-existent facility returns 404",
                request: RequestDef{
                    method: "GET",
                    path: "/v1/facilities/fac-notfound",
                    headers: {"Accept": "application/json"}
                },
                response: ResponseDef{
                    status: 404,
                    body: {
                        "code": "NOT_FOUND",
                        "message": "Facility not found"
                    }
                }
            }
        ]
    }
END FUNCTION

// SaveExpectations writes consumer expectations to a contract file.
FUNCTION SaveExpectations(exp: ConsumerExpectation, path: String) RETURNS Result<Void, Error>
    data = SerializeJSON(exp)
    IF data.IsError() THEN
        RETURN Error("failed to marshal expectations: " + data.Error())
    END IF
    RETURN WriteFile(path, data.Value())
END FUNCTION
```

### Consumer Contract Test

```pseudocode
// tests/contract/consumer_contract_test

// MockProvider creates an HTTP handler from consumer expectations.
TYPE MockProvider
    expectations: ConsumerExpectation
END TYPE

CONSTRUCTOR NewMockProvider(exp: ConsumerExpectation) RETURNS MockProvider
    RETURN MockProvider{expectations: exp}
END CONSTRUCTOR

METHOD MockProvider.ServeHTTP(writer: ResponseWriter, request: HttpRequest)
    FOR EACH interaction IN this.expectations.interactions DO
        IF request.Method == interaction.request.method AND
           request.URL.Path == interaction.request.path THEN
            FOR EACH key, value IN interaction.response.headers DO
                writer.Header().Set(key, value)
            END FOR
            writer.WriteHeader(interaction.response.status)
            writer.Write(interaction.response.body)
            RETURN
        END IF
    END FOR
    writer.WriteHeader(501)
END METHOD


// TestAssetContext_ConsumerExpectations verifies the consumer's expectations.
// This test runs in the CONSUMER's repository to generate the contract.
TEST AssetContext_ConsumerExpectations
    expectations = AssetContextExpectations()

    // Create a mock provider based on expectations
    mock = NewMockProvider(expectations)
    server = NewTestServer(mock)
    DEFER server.Close()

    // Test each interaction from consumer's perspective
    FOR EACH interaction IN expectations.interactions DO
        TEST interaction.description
            // Make request as consumer would
            request = NewHttpRequest(
                interaction.request.method,
                server.URL + interaction.request.path,
                NULL
            )

            FOR EACH key, value IN interaction.request.headers DO
                request.Header.Set(key, value)
            END FOR

            response = HttpClient.Do(request)
            DEFER response.Body.Close()

            // Verify response matches expectation
            ASSERT response.StatusCode == interaction.response.status

            body = ReadAll(response.Body)

            // Compare JSON structures (ignoring field order)
            ASSERT JSONEquals(interaction.response.body, body)
        END TEST
    END FOR
END TEST
```

Consumer expectations define the minimum contract. Producers must satisfy these expectations but may provide additional fields or endpoints.

## Step 3: Generate Mocks from Contracts

Generate type-safe mocks from OpenAPI specifications to ensure test doubles match the actual contract.

### Mock Generator

```pseudocode
// internal/contracts/mockgen

// ContractMock creates a test server that validates requests against OpenAPI spec.
TYPE ContractMock
    spec: OpenAPIDocument
    router: OpenAPIRouter
    responses: Map<String, MockResponse>
END TYPE

// MockResponse defines a canned response for an operation.
TYPE MockResponse
    status: Integer
    headers: Map<String, String>
    body: Any
END TYPE

// NewContractMock creates a mock server from an OpenAPI spec.
CONSTRUCTOR NewContractMock(specPath: String) RETURNS Result<ContractMock, Error>
    loader = NewOpenAPILoader()
    spec = loader.LoadFromFile(specPath)
    IF spec.IsError() THEN
        RETURN Error("failed to load spec: " + spec.Error())
    END IF

    router = NewOpenAPIRouter(spec.Value())
    IF router.IsError() THEN
        RETURN Error("failed to create router: " + router.Error())
    END IF

    RETURN Ok(ContractMock{
        spec: spec.Value(),
        router: router.Value(),
        responses: NEW Map<String, MockResponse>()
    })
END CONSTRUCTOR

// SetResponse configures the response for an operation.
METHOD ContractMock.SetResponse(operationID: String, resp: MockResponse)
    this.responses[operationID] = resp
END METHOD

// Handler returns an HTTP handler that validates against the contract.
METHOD ContractMock.Handler() RETURNS HttpHandler
    RETURN FUNCTION(writer: ResponseWriter, request: HttpRequest)
        // Find matching operation
        route = this.router.FindRoute(request)
        IF route.IsError() THEN
            HttpError(writer, "Route not found in contract", 404)
            RETURN
        END IF

        // Validate request against contract
        requestValidation = ValidateRequest(request, route.Value())
        IF requestValidation.IsError() THEN
            HttpError(writer, "Request violates contract: " + requestValidation.Error(), 400)
            RETURN
        END IF

        // Return configured response
        operationID = route.Value().Operation.OperationID
        resp = this.responses[operationID]
        IF resp == NULL THEN
            HttpError(writer, "No mock response configured for " + operationID, 501)
            RETURN
        END IF

        FOR EACH key, value IN resp.headers DO
            writer.Header().Set(key, value)
        END FOR
        writer.Header().Set("Content-Type", "application/json")
        writer.WriteHeader(resp.status)

        IF resp.body != NULL THEN
            WriteJSON(writer, resp.body)
        END IF
    END FUNCTION
END METHOD

// Server creates a test server with contract validation.
METHOD ContractMock.Server() RETURNS TestServer
    RETURN NewTestServer(this.Handler())
END METHOD
```

### Using Contract Mocks in Tests

```pseudocode
// tests/service/facility_client_test

TEST FacilityClient_GetFacility
    // Create contract-validated mock
    mock = NewContractMock("../../contracts/api/openapi.yaml")
    ASSERT mock.IsOk()

    // Configure expected response
    mock.Value().SetResponse("getFacility", MockResponse{
        status: 200,
        body: {
            "id": "fac-abc123",
            "name": "Solar Farm Alpha",
            "status": "active",
            "zoneCount": 5
        }
    })

    server = mock.Value().Server()
    DEFER server.Close()

    // Test client against contract-validated mock
    client = NewFacilityClient(server.URL)
    facility = client.GetFacility(NewContext(), "fac-abc123")

    ASSERT facility.IsOk()
    ASSERT facility.Value().ID == "fac-abc123"
    ASSERT facility.Value().Name == "Solar Farm Alpha"
    ASSERT facility.Value().Status == "active"
END TEST


TEST FacilityClient_InvalidRequest_RejectedByContract
    mock = NewContractMock("../../contracts/api/openapi.yaml")
    ASSERT mock.IsOk()

    server = mock.Value().Server()
    DEFER server.Close()

    client = NewFacilityClient(server.URL)

    // Request with invalid facility ID format should be rejected
    result = client.GetFacility(NewContext(), "invalid-format")

    // Contract mock rejects requests that don't match path pattern
    ASSERT result.IsError()
END TEST
```

Contract mocks validate both requests and responses against the OpenAPI specification, catching contract violations during development.

## Step 4: Implement Producer Verification

Producers must verify they actually fulfill the contract. This runs in the producer's CI pipeline.

### OpenAPI Response Validator

```pseudocode
// internal/contracts/validator

// ResponseValidator validates HTTP responses against OpenAPI spec.
TYPE ResponseValidator
    spec: OpenAPIDocument
    router: OpenAPIRouter
END TYPE

// NewResponseValidator creates a validator from an OpenAPI spec.
CONSTRUCTOR NewResponseValidator(specPath: String) RETURNS Result<ResponseValidator, Error>
    loader = NewOpenAPILoader()
    spec = loader.LoadFromFile(specPath)
    IF spec.IsError() THEN
        RETURN Error(spec.Error())
    END IF

    router = NewOpenAPIRouter(spec.Value())
    IF router.IsError() THEN
        RETURN Error(router.Error())
    END IF

    RETURN Ok(ResponseValidator{spec: spec.Value(), router: router.Value()})
END CONSTRUCTOR

// ValidateResponse checks if a response matches the contract.
METHOD ResponseValidator.ValidateResponse(
    request: HttpRequest,
    response: HttpResponse
) RETURNS Result<Void, Error>
    route = this.router.FindRoute(request)
    IF route.IsError() THEN
        RETURN Error(route.Error())
    END IF

    // Read response body
    bodyBytes = ReadAll(response.Body)
    response.Body = NewBufferReader(bodyBytes)

    // Create validation input
    responseValidation = ValidateOpenAPIResponse(
        request,
        route.Value(),
        response.StatusCode,
        response.Header,
        bodyBytes
    )

    RETURN responseValidation
END METHOD
```

### Producer Contract Test

```pseudocode
// tests/contract/api_contract_test

TEST FacilityAPI_CreateFacility_MatchesContract
    // Load the OpenAPI contract
    validator = NewResponseValidator("../../contracts/api/openapi.yaml")
    ASSERT validator.IsOk()

    // Create the actual handler (with mocked dependencies)
    handler = setupTestHandler()
    server = NewTestServer(handler)
    DEFER server.Close()

    // Create valid request according to contract
    reqBody = '{
        "name": "Test Facility",
        "latitude": 59.3293,
        "longitude": 18.0686,
        "maxZones": 10
    }'

    request = NewHttpRequest("POST", server.URL + "/v1/facilities", reqBody)
    request.Header.Set("Content-Type", "application/json")

    // Make request
    response = HttpClient.Do(request)
    DEFER response.Body.Close()

    // Verify response matches contract
    err = validator.Value().ValidateResponse(request, response)
    ASSERT err == NULL  // "Response should match OpenAPI contract"

    // Also verify expected status
    ASSERT response.StatusCode == 201
END TEST


TEST FacilityAPI_ValidationError_MatchesContract
    validator = NewResponseValidator("../../contracts/api/openapi.yaml")
    ASSERT validator.IsOk()

    handler = setupTestHandler()
    server = NewTestServer(handler)
    DEFER server.Close()

    // Invalid request (latitude out of range)
    reqBody = '{
        "name": "Test",
        "latitude": 999.0,
        "longitude": 18.0686
    }'

    request = NewHttpRequest("POST", server.URL + "/v1/facilities", reqBody)
    request.Header.Set("Content-Type", "application/json")

    response = HttpClient.Do(request)
    DEFER response.Body.Close()

    // Verify 400 response matches error schema
    ASSERT response.StatusCode == 400
    err = validator.Value().ValidateResponse(request, response)
    ASSERT err == NULL  // "Error response should match contract schema"
END TEST


TEST FacilityAPI_AllOperations_MatchContract
    validator = NewResponseValidator("../../contracts/api/openapi.yaml")
    ASSERT validator.IsOk()

    handler = setupTestHandler()
    server = NewTestServer(handler)
    DEFER server.Close()

    testCases = [
        {name: "Create facility", method: "POST", path: "/v1/facilities",
         body: '{"name":"Test","latitude":59.32,"longitude":18.06}', expectedStatus: 201},
        {name: "Get facility", method: "GET", path: "/v1/facilities/fac-test123",
         expectedStatus: 200},
        {name: "Get non-existent facility", method: "GET", path: "/v1/facilities/fac-notfound",
         expectedStatus: 404}
    ]

    FOR EACH tc IN testCases DO
        TEST tc.name
            request = NewHttpRequest(tc.method, server.URL + tc.path, tc.body)

            IF tc.body != "" THEN
                request.Header.Set("Content-Type", "application/json")
            END IF

            response = HttpClient.Do(request)
            DEFER response.Body.Close()

            ASSERT response.StatusCode == tc.expectedStatus
            err = validator.Value().ValidateResponse(request, response)
            ASSERT err == NULL  // "Response should match contract"
        END TEST
    END FOR
END TEST


FUNCTION setupTestHandler() RETURNS HttpHandler
    // Setup handler with mocked repositories
    // In real tests, inject test doubles for database, event publisher, etc.
    repo = NewMockFacilityRepository()
    publisher = NewMockEventPublisher()

    RETURN NewAPIHandler(repo, publisher)
END FUNCTION
```

Producer tests run the actual handler and validate responses against the contract. This ensures the implementation matches what was documented.

## Step 5: Set Up Event Schema Validation

Event schemas ensure producers and consumers agree on event structure. Validate events at publish and consume time.

### Event Validator

```pseudocode
// internal/events/validator

// SchemaValidator validates events against JSON schemas.
TYPE SchemaValidator
    schemaDir: String
    cache: Map<String, CompiledSchema>
    mutex: Mutex
END TYPE

// NewSchemaValidator creates a validator with schema directory.
CONSTRUCTOR NewSchemaValidator(schemaDir: String) RETURNS SchemaValidator
    RETURN SchemaValidator{
        schemaDir: schemaDir,
        cache: NEW Map<String, CompiledSchema>(),
        mutex: NEW Mutex()
    }
END CONSTRUCTOR

// Validate validates an event against its schema.
METHOD SchemaValidator.Validate(eventType: String, event: Any) RETURNS Result<Void, Error>
    schema = this.getSchema(eventType)
    IF schema.IsError() THEN
        RETURN Error("failed to load schema: " + schema.Error())
    END IF

    eventJSON = SerializeJSON(event)
    IF eventJSON.IsError() THEN
        RETURN Error("failed to marshal event: " + eventJSON.Error())
    END IF

    documentLoader = NewBytesLoader(eventJSON.Value())
    result = schema.Value().Validate(documentLoader)
    IF result.IsError() THEN
        RETURN Error("validation error: " + result.Error())
    END IF

    IF NOT result.Value().IsValid() THEN
        RETURN this.formatErrors(eventType, result.Value().Errors())
    END IF

    RETURN Ok()
END METHOD

METHOD SchemaValidator.getSchema(eventType: String) RETURNS Result<CompiledSchema, Error>
    this.mutex.RLock()
    IF this.cache.Contains(eventType) THEN
        schema = this.cache[eventType]
        this.mutex.RUnlock()
        RETURN Ok(schema)
    END IF
    this.mutex.RUnlock()

    this.mutex.Lock()
    DEFER this.mutex.Unlock()

    // Double-check after acquiring write lock
    IF this.cache.Contains(eventType) THEN
        RETURN Ok(this.cache[eventType])
    END IF

    schemaPath = this.schemaDir + "/" + eventType + ".json"
    schemaLoader = NewJSONSchemaLoader(schemaPath)

    schema = schemaLoader.Compile()
    IF schema.IsError() THEN
        RETURN Error(schema.Error())
    END IF

    this.cache[eventType] = schema.Value()
    RETURN Ok(schema.Value())
END METHOD

METHOD SchemaValidator.formatErrors(eventType: String, errors: List<ValidationError>) RETURNS Error
    msg = "event " + eventType + " failed validation:\n"
    FOR EACH e IN errors DO
        msg = msg + "  - " + e.Field() + ": " + e.Description() + "\n"
    END FOR
    RETURN Error(msg)
END METHOD
```

### Event Contract Test

```pseudocode
// tests/contract/event_contract_test

TEST FacilityCreatedEvent_MatchesSchema
    validator = NewSchemaValidator("../../contracts/events")

    // Create event as domain would
    event = FacilityCreatedEvent{
        eventID: NewUUID(),
        eventType: "facility.created",
        schemaVersion: "1.0.0",
        occurredAt: DateTime.Now().ToRFC3339(),
        aggregateID: "fac-abc123",
        correlationID: "corr-xyz789",
        payload: FacilityCreatedPayload{
            facilityID: "fac-abc123",
            name: "Solar Farm Alpha",
            location: Location{
                latitude: 59.3293,
                longitude: 18.0686,
                country: "SE",
                timezone: "Europe/Stockholm"
            },
            ownerID: "tenant-001",
            maxZones: 10
        }
    }

    err = validator.Validate("facility.created", event)
    ASSERT err == NULL
END TEST


TEST FacilityCreatedEvent_MissingRequired_FailsValidation
    validator = NewSchemaValidator("../../contracts/events")

    // Event missing required fields
    event = {
        "event_id": NewUUID(),
        "event_type": "facility.created"
        // Missing: schema_version, occurred_at, aggregate_id, correlation_id, payload
    }

    err = validator.Validate("facility.created", event)
    ASSERT err != NULL
    ASSERT err.Message().Contains("schema_version")
END TEST


TEST AllDomainEvents_MatchSchemas
    validator = NewSchemaValidator("../../contracts/events")

    testCases = [
        {name: "FacilityCreated", eventType: "facility.created",
         event: createValidFacilityCreatedEvent()},
        {name: "FacilityUpdated", eventType: "facility.updated",
         event: createValidFacilityUpdatedEvent()},
        {name: "ZoneAdded", eventType: "zone.added",
         event: createValidZoneAddedEvent()}
    ]

    FOR EACH tc IN testCases DO
        TEST tc.name
            err = validator.Validate(tc.eventType, tc.event)
            ASSERT err == NULL  // "Event should match schema"
        END TEST
    END FOR
END TEST


FUNCTION createValidFacilityCreatedEvent() RETURNS FacilityCreatedEvent
    RETURN FacilityCreatedEvent{
        eventID: NewUUID(),
        eventType: "facility.created",
        schemaVersion: "1.0.0",
        occurredAt: DateTime.Now().ToRFC3339(),
        aggregateID: "fac-test123",
        correlationID: "corr-test456",
        payload: FacilityCreatedPayload{
            facilityID: "fac-test123",
            name: "Test Facility",
            location: Location{latitude: 59.0, longitude: 18.0},
            ownerID: "tenant-test"
        }
    }
END FUNCTION
```

Event schema validation ensures domain events match their published contracts. Run these tests whenever event structures change.

## Step 6: Configure CI/CD Contract Validation

Integrate contract tests into CI/CD to catch breaking changes before merge.

### Makefile Targets

```makefile
# Makefile
.PHONY: test-contracts test-unit test-integration lint-contracts

# Run all contract tests
test-contracts:
	go test -v -tags=contract ./tests/contract/...

# Validate OpenAPI spec syntax
lint-contracts:
	@echo "Validating OpenAPI specification..."
	npx @redocly/cli lint contracts/api/openapi.yaml
	@echo "Validating event schemas..."
	@for schema in contracts/events/*.json; do \
		echo "Checking $$schema..."; \
		npx ajv validate -s $$schema -d /dev/null 2>/dev/null || \
		npx ajv compile -s $$schema; \
	done

# Check for breaking changes
check-breaking:
	@echo "Checking for breaking changes..."
	npx @redocly/cli diff contracts/api/openapi.yaml origin/main:contracts/api/openapi.yaml

# Full test suite
test: lint-contracts test-unit test-contracts test-integration
```

### GitHub Actions Workflow

```yaml
# .github/workflows/contracts.yaml
name: Contract Tests

on:
  pull_request:
    paths:
      - 'contracts/**'
      - 'tests/contract/**'
      - 'core/domain/**/events'
  push:
    branches: [main]

jobs:
  contract-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Need history for breaking change detection

      - name: Setup language environment
        # Configure your language runtime here

      - name: Install contract tools
        run: |
          npm install -g @redocly/cli ajv-cli

      - name: Validate contract syntax
        run: make lint-contracts

      - name: Check for breaking changes
        if: github.event_name == 'pull_request'
        run: |
          npx @redocly/cli diff \
            contracts/api/openapi.yaml \
            origin/${{ github.base_ref }}:contracts/api/openapi.yaml \
            --fail-on-incompatible-changes

      - name: Run contract tests
        run: make test-contracts

      - name: Upload contract artifacts
        uses: actions/upload-artifact@v4
        with:
          name: contracts
          path: contracts/
```

### Breaking Change Detection Script

```pseudocode
// scripts/check_schema_compatibility

FUNCTION main()
    IF Arguments.Length() < 3 THEN
        Print("Usage: check_schema_compatibility <old_schema> <new_schema>")
        Exit(1)
    END IF

    oldPath = Arguments[1]
    newPath = Arguments[2]

    breaking = checkBreakingChanges(oldPath, newPath)
    IF breaking.IsError() THEN
        Print("Error checking compatibility: " + breaking.Error())
        Exit(1)
    END IF

    IF breaking.Value().Length() > 0 THEN
        Print("BREAKING CHANGES DETECTED:")
        FOR EACH change IN breaking.Value() DO
            Print("  - " + change)
        END FOR
        Exit(1)
    END IF

    Print("No breaking changes detected")
END FUNCTION


FUNCTION checkBreakingChanges(oldPath: String, newPath: String) RETURNS Result<List<String>, Error>
    breaking = NEW List<String>()

    oldSchema = loadSchema(oldPath)
    IF oldSchema.IsError() THEN
        RETURN Error(oldSchema.Error())
    END IF

    newSchema = loadSchema(newPath)
    IF newSchema.IsError() THEN
        RETURN Error(newSchema.Error())
    END IF

    // Check for removed required fields
    oldRequired = getRequired(oldSchema.Value())
    newRequired = getRequired(newSchema.Value())

    FOR EACH field IN oldRequired DO
        IF NOT newRequired.Contains(field) THEN
            // Check if field still exists as optional
            IF NOT fieldExists(newSchema.Value(), field) THEN
                breaking.Add("Required field '" + field + "' was removed")
            END IF
        END IF
    END FOR

    // Check for new required fields
    FOR EACH field IN newRequired DO
        IF NOT oldRequired.Contains(field) THEN
            breaking.Add("New required field '" + field + "' added")
        END IF
    END FOR

    RETURN Ok(breaking)
END FUNCTION


FUNCTION loadSchema(path: String) RETURNS Result<Map<String, Any>, Error>
    data = ReadFile(path)
    IF data.IsError() THEN
        RETURN Error(data.Error())
    END IF

    schema = DeserializeJSON<Map<String, Any>>(data.Value())
    RETURN schema
END FUNCTION


FUNCTION getRequired(schema: Map<String, Any>) RETURNS Set<String>
    required = NEW Set<String>()
    IF schema.Contains("required") THEN
        FOR EACH r IN schema["required"] DO
            required.Add(r)
        END FOR
    END IF
    RETURN required
END FUNCTION


FUNCTION fieldExists(schema: Map<String, Any>, field: String) RETURNS Boolean
    IF NOT schema.Contains("properties") THEN
        RETURN FALSE
    END IF
    props = schema["properties"]
    RETURN props.Contains(field)
END FUNCTION
```

CI/CD integration ensures contract tests run on every change, blocking merges that would break compatibility.

## Step 7: Handle Schema Versioning

Use semantic versioning to communicate compatibility. Maintain multiple schema versions when needed.

### Version Manager

```pseudocode
// internal/contracts/versioning

// SchemaVersion represents a parsed semantic version.
TYPE SchemaVersion
    major: Integer
    minor: Integer
    patch: Integer
    raw: String
END TYPE

// ParseVersion parses a semver string.
FUNCTION ParseVersion(v: String) RETURNS Result<SchemaVersion, Error>
    IF NOT v.StartsWith("v") THEN
        v = "v" + v
    END IF

    IF NOT IsValidSemver(v) THEN
        RETURN Error("invalid version: " + v)
    END IF

    major, minor, patch = ParseSemver(v)

    RETURN Ok(SchemaVersion{
        major: major,
        minor: minor,
        patch: patch,
        raw: v.TrimPrefix("v")
    })
END FUNCTION

// IsCompatible checks if consumer version is compatible with producer version.
// Compatible means: same major version, producer minor >= consumer minor.
METHOD SchemaVersion.IsCompatible(producer: SchemaVersion) RETURNS Boolean
    IF this.major != producer.major THEN
        RETURN FALSE  // Major version mismatch = breaking change
    END IF
    RETURN producer.minor >= this.minor
END METHOD

// SchemaRegistry tracks available schema versions.
TYPE SchemaRegistry
    schemas: Map<String, List<SchemaVersion>>  // eventType -> versions
END TYPE

// NewSchemaRegistry creates an empty registry.
CONSTRUCTOR NewSchemaRegistry() RETURNS SchemaRegistry
    RETURN SchemaRegistry{
        schemas: NEW Map<String, List<SchemaVersion>>()
    }
END CONSTRUCTOR

// Register adds a schema version.
METHOD SchemaRegistry.Register(eventType: String, version: String) RETURNS Result<Void, Error>
    v = ParseVersion(version)
    IF v.IsError() THEN
        RETURN Error(v.Error())
    END IF

    IF NOT this.schemas.Contains(eventType) THEN
        this.schemas[eventType] = NEW List<SchemaVersion>()
    END IF

    this.schemas[eventType].Add(v.Value())

    // Keep sorted by version
    this.schemas[eventType].Sort(FUNCTION(a, b)
        IF a.major != b.major THEN RETURN a.major < b.major END IF
        IF a.minor != b.minor THEN RETURN a.minor < b.minor END IF
        RETURN a.patch < b.patch
    END FUNCTION)

    RETURN Ok()
END METHOD

// LatestVersion returns the latest version for an event type.
METHOD SchemaRegistry.LatestVersion(eventType: String) RETURNS Result<SchemaVersion, Boolean>
    IF NOT this.schemas.Contains(eventType) OR this.schemas[eventType].IsEmpty() THEN
        RETURN NULL, FALSE
    END IF
    versions = this.schemas[eventType]
    RETURN versions[versions.Length() - 1], TRUE
END METHOD

// CompatibleVersions returns all versions compatible with the given version.
METHOD SchemaRegistry.CompatibleVersions(eventType: String, consumerVersion: SchemaVersion) RETURNS List<SchemaVersion>
    IF NOT this.schemas.Contains(eventType) THEN
        RETURN NEW List<SchemaVersion>()
    END IF

    compatible = NEW List<SchemaVersion>()
    FOR EACH v IN this.schemas[eventType] DO
        IF consumerVersion.IsCompatible(v) THEN
            compatible.Add(v)
        END IF
    END FOR
    RETURN compatible
END METHOD
```

### Versioned Event Publisher

```pseudocode
// adapters/secondary/eventbus/versioned_publisher

// VersionedPublisher publishes events with schema validation.
TYPE VersionedPublisher
    client: EventBusClient
    busName: String
    validator: SchemaValidator
    registry: SchemaRegistry
END TYPE

// NewVersionedPublisher creates a publisher with validation.
CONSTRUCTOR NewVersionedPublisher(
    client: EventBusClient,
    busName: String,
    schemaDir: String
) RETURNS VersionedPublisher
    RETURN VersionedPublisher{
        client: client,
        busName: busName,
        validator: NewSchemaValidator(schemaDir),
        registry: loadRegistry(schemaDir)
    }
END CONSTRUCTOR

// Publish validates and publishes an event.
METHOD VersionedPublisher.Publish(ctx: Context, event: Any) RETURNS Result<Void, Error>
    // Extract event type and version
    eventType, version = extractEventMeta(event)
    IF eventType.IsError() THEN
        RETURN Error("failed to extract event metadata: " + eventType.Error())
    END IF

    // Validate against schema
    validation = this.validator.Validate(eventType.Value(), event)
    IF validation.IsError() THEN
        RETURN Error("event failed schema validation: " + validation.Error())
    END IF

    // Check version exists in registry
    registered = this.registry.LatestVersion(eventType.Value())
    IF NOT registered.found THEN
        RETURN Error("no schema registered for event type: " + eventType.Value())
    END IF

    eventVersion = ParseVersion(version.Value())
    IF NOT eventVersion.Value().IsCompatible(registered.version) THEN
        RETURN Error("event version " + version.Value() +
                     " incompatible with registered " + registered.version.raw)
    END IF

    // Marshal and publish
    eventJSON = SerializeJSON(event)
    IF eventJSON.IsError() THEN
        RETURN Error("failed to marshal event: " + eventJSON.Error())
    END IF

    RETURN this.client.PutEvent(ctx, EventEntry{
        eventBusName: this.busName,
        source: ".facility",
        detailType: eventType.Value(),
        detail: eventJSON.Value()
    })
END METHOD


FUNCTION extractEventMeta(event: Any) RETURNS Result<(String, String), Error>
    data = SerializeJSON(event)
    IF data.IsError() THEN
        RETURN Error(data.Error())
    END IF

    meta = DeserializeJSON<EventMeta>(data.Value())
    IF meta.IsError() THEN
        RETURN Error(meta.Error())
    END IF

    RETURN Ok((meta.Value().eventType, meta.Value().schemaVersion))
END FUNCTION


FUNCTION loadRegistry(schemaDir: String) RETURNS SchemaRegistry
    // Load from schema files - in production, this would scan the directory
    registry = NewSchemaRegistry()
    registry.Register("facility.created", "1.0.0")
    registry.Register("facility.updated", "1.0.0")
    registry.Register("zone.added", "1.0.0")
    RETURN registry
END FUNCTION
```

Semantic versioning with compatibility checking ensures consumers know which producer versions they can work with. Major version changes require consumer updates.

## Verification Checklist

After setting up contract tests, verify:

- [ ] OpenAPI specification exists in `/contracts/api/openapi.yaml`
- [ ] Event JSON schemas exist in `/contracts/events/`
- [ ] Contract loader can parse OpenAPI and JSON Schema files
- [ ] Consumer expectations define minimum required responses
- [ ] Mock generator validates requests against OpenAPI spec
- [ ] Producer tests validate actual responses against contract
- [ ] Event validator checks domain events against JSON schemas
- [ ] CI/CD runs `lint-contracts` to validate syntax
- [ ] CI/CD runs `test-contracts` on every PR
- [ ] Breaking change detection blocks incompatible changes
- [ ] Schema versioning follows semver rules
- [ ] New required fields trigger major version bump
- [ ] Compatible versions are documented in schema registry
