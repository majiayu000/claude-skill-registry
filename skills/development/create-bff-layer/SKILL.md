---
name: create-bff-layer
description: "Step-by-step guide for creating Backend for Frontend layers that aggregate multiple bounded contexts."
tools: []
context: []
---

# Skill: Create BFF Layer

This skill teaches you how to create a Backend for Frontend (BFF) layer following  architectural patterns. A BFF is a client-specific adapter that aggregates data from multiple bounded contexts and shapes responses for specific client surfaces.

A properly designed BFF enables clean separation between domain APIs and client needs. It aggregates calls, transforms responses, and handles client-specific concerns. The BFF remains stateless and never contains domain logic - it lives in Presentation and Adapter layers only.

## Prerequisites

- Understanding of Clean Architecture and DDD concepts
- Multiple bounded contexts already implemented with public APIs
- Clear understanding of what the client surface needs

## Overview

You will: define client requirements, create bounded context clients, implement BFF aggregation, add response shaping, implement caching, create error handling, and test independently.

## Step 1: Define Client Requirements

Create an OpenAPI contract that specifies the aggregated endpoints.

```yaml
# contracts/openapi.yaml
openapi: 3.0.3
info:
  title: Mobile Home BFF API
  version: 1.0.0
paths:
  /home/summary:
    get:
      summary: Get home energy summary
      operationId: getHomeSummary
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HomeSummaryResponse'
components:
  schemas:
    HomeSummaryResponse:
      type: object
      properties:
        facility_name:
          type: string
        total_assets:
          type: integer
        current_consumption_kw:
          type: number
```

The contract defines client-specific shapes that aggregate data from multiple bounded contexts.

## Step 2: Create Backend Service Clients

Create client interfaces for each bounded context your BFF will call.

```pseudocode
// clients/interfaces

// FacilityClient communicates with the Facility bounded context.
INTERFACE FacilityClient
    METHOD GetUserFacility(ctx: Context, userID: String) RETURNS Result<Facility, Error>
END INTERFACE

// AssetClient communicates with the Asset bounded context.
INTERFACE AssetClient
    METHOD GetFacilityAssets(ctx: Context, facilityID: String) RETURNS Result<List<Asset>, Error>
END INTERFACE

// IntelligenceClient communicates with the Intelligence bounded context.
INTERFACE IntelligenceClient
    METHOD GetCurrentSchedule(ctx: Context, facilityID: String) RETURNS Result<Schedule, Error>
END INTERFACE

TYPE Facility
    id: String
    name: String
    address: String
END TYPE

TYPE Asset
    id: String
    name: String
    state: String
    currentLoadKW: Float
END TYPE

TYPE Schedule
    nextActionTime: String
    nextActionDesc: String
    expectedSavingsKWh: Float
END TYPE
```

```pseudocode
// clients/facility_client

TYPE HTTPFacilityClient
    baseURL: String
    httpClient: HttpClient
END TYPE

CONSTRUCTOR NewHTTPFacilityClient(baseURL: String, client: HttpClient) RETURNS HTTPFacilityClient
    RETURN HTTPFacilityClient{baseURL: baseURL, httpClient: client}
END CONSTRUCTOR

METHOD HTTPFacilityClient.GetUserFacility(ctx: Context, userID: String) RETURNS Result<Facility, Error>
    url = this.baseURL + "/users/" + userID + "/facility"
    request = NewHttpRequest(ctx, "GET", url)

    response = this.httpClient.Do(request)
    IF response.IsError() THEN
        RETURN Error("failed to call facility service: " + response.Error())
    END IF
    DEFER response.Body.Close()

    IF response.StatusCode == 404 THEN
        RETURN Error(ErrFacilityNotFound)
    END IF

    facility = Deserialize<Facility>(response.Body)
    RETURN Ok(facility.Value())
END METHOD
```

Each client calls a single bounded context's public API. The BFF never accesses databases directly.

## Step 3: Implement BFF Handler with Aggregation

Create the BFF handler that orchestrates calls to multiple bounded contexts.

```pseudocode
// handlers/dto

// HomeSummaryResponse is the client-specific response shape.
TYPE HomeSummaryResponse
    facilityName: String
    totalAssets: Integer
    assetsOnline: Integer
    currentConsumptionKW: Float
    nextOptimization: OptimizationPreview  // Optional
    lastUpdated: DateTime
END TYPE

TYPE OptimizationPreview
    scheduledAt: DateTime
    action: String
    expectedSavingsKWh: Float
END TYPE
```

```pseudocode
// handlers/home_bff

// HomeBFFHandler aggregates data from multiple bounded contexts.
// It contains NO domain logic - only orchestration and response shaping.
TYPE HomeBFFHandler
    facilityClient: FacilityClient
    assetClient: AssetClient
    intelligenceClient: IntelligenceClient
END TYPE

CONSTRUCTOR NewHomeBFFHandler(
    f: FacilityClient,
    a: AssetClient,
    i: IntelligenceClient
) RETURNS HomeBFFHandler
    RETURN HomeBFFHandler{
        facilityClient: f,
        assetClient: a,
        intelligenceClient: i
    }
END CONSTRUCTOR

// GetHomeSummary aggregates data - pure orchestration, no business rules.
METHOD HomeBFFHandler.GetHomeSummary(ctx: Context, userID: String) RETURNS Result<HomeSummaryResponse, Error>
    // Call Facility bounded context
    facility = this.facilityClient.GetUserFacility(ctx, userID)
    IF facility.IsError() THEN
        RETURN Error("failed to get facility: " + facility.Error())
    END IF

    // Call Asset bounded context
    assets = this.assetClient.GetFacilityAssets(ctx, facility.Value().id)
    IF assets.IsError() THEN
        RETURN Error("failed to get assets: " + assets.Error())
    END IF

    // Call Intelligence bounded context (optional - don't fail if unavailable)
    schedule = this.intelligenceClient.GetCurrentSchedule(ctx, facility.Value().id)
    // Ignore error for optional data

    // Aggregate and shape response - NO business logic here
    RETURN Ok(this.shapeResponse(facility.Value(), assets.Value(), schedule.ValueOrNil()))
END METHOD

METHOD HomeBFFHandler.shapeResponse(
    facility: Facility,
    assets: List<Asset>,
    schedule: Schedule
) RETURNS HomeSummaryResponse
    assetsOnline = 0
    totalConsumption = 0.0

    FOR EACH asset IN assets DO
        IF asset.state == "online" THEN
            assetsOnline = assetsOnline + 1
        END IF
        totalConsumption = totalConsumption + asset.currentLoadKW
    END FOR

    response = HomeSummaryResponse{
        facilityName: facility.name,
        totalAssets: assets.Length(),
        assetsOnline: assetsOnline,
        currentConsumptionKW: totalConsumption,
        lastUpdated: DateTime.Now().ToUTC()
    }

    IF schedule != NULL THEN
        scheduledAt = DateTime.Parse(schedule.nextActionTime)
        response.nextOptimization = OptimizationPreview{
            scheduledAt: scheduledAt,
            action: schedule.nextActionDesc,
            expectedSavingsKWh: schedule.expectedSavingsKWh
        }
    END IF

    RETURN response
END METHOD
```

The handler only orchestrates and shapes. No `if asset.Load > threshold` style decisions.

## Step 4: Add Optional Caching

For performance, add caching. This is technical caching, not domain state storage.

```pseudocode
// cache/cache

TYPE Cache
    client: CacheClient
    ttl: Duration
END TYPE

CONSTRUCTOR NewCache(client: CacheClient, ttl: Duration) RETURNS Cache
    RETURN Cache{client: client, ttl: ttl}
END CONSTRUCTOR

METHOD Cache.Get(ctx: Context, key: String, dest: Any) RETURNS Result<Any, Error>
    val = this.client.Get(ctx, key)
    IF val.IsError() THEN
        RETURN val.Error()
    END IF
    RETURN Deserialize(val.Value(), dest)
END METHOD

METHOD Cache.Set(ctx: Context, key: String, value: Any) RETURNS Result<Void, Error>
    data = Serialize(value)
    RETURN this.client.Set(ctx, key, data, this.ttl)
END METHOD

FUNCTION HomeSummaryKey(userID: String) RETURNS String
    RETURN "bff:home:summary:" + userID
END FUNCTION
```

## Step 5: Implement Error Handling

Translate domain errors to client-friendly responses.

```pseudocode
// clients/errors

CONSTANT ErrFacilityNotFound = "facility not found"
CONSTANT ErrServiceUnavailable = "service unavailable"
CONSTANT ErrUnauthorized = "unauthorized"
```

```pseudocode
// handlers/errors

TYPE ErrorResponse
    error: String
    code: String
    message: String
END TYPE

FUNCTION MapErrorToHTTPStatus(err: Error) RETURNS Integer
    SWITCH err
        CASE ErrFacilityNotFound:
            RETURN 404
        CASE ErrUnauthorized:
            RETURN 401
        DEFAULT:
            RETURN 500
    END SWITCH
END FUNCTION

FUNCTION MapErrorToResponse(err: Error) RETURNS ErrorResponse
    SWITCH err
        CASE ErrFacilityNotFound:
            RETURN ErrorResponse{
                error: "not_found",
                code: "FACILITY_NOT_FOUND",
                message: "No facility associated with your account"
            }
        DEFAULT:
            RETURN ErrorResponse{
                error: "internal_error",
                code: "INTERNAL_ERROR",
                message: "Something went wrong"
            }
    END SWITCH
END FUNCTION
```

## Step 6: Create Entry Point

Set up dependency injection in the handler.

```pseudocode
// cmd/api/main

GLOBAL bffHandler: HomeBFFHandler

FUNCTION init()
    httpClient = NewHttpClient(timeout: 10 seconds)

    bffHandler = NewHomeBFFHandler(
        NewHTTPFacilityClient(GetEnv("FACILITY_SERVICE_URL"), httpClient),
        NewHTTPAssetClient(GetEnv("ASSET_SERVICE_URL"), httpClient),
        NewHTTPIntelligenceClient(GetEnv("INTELLIGENCE_SERVICE_URL"), httpClient)
    )
END FUNCTION

FUNCTION main()
    StartServer(handle)
END FUNCTION

FUNCTION handle(ctx: Context, request: HttpRequest) RETURNS HttpResponse
    userID = request.Context.Authorizer["sub"]
    IF userID == NULL THEN
        RETURN HttpResponse{StatusCode: 401}
    END IF

    response = bffHandler.GetHomeSummary(ctx, userID)
    IF response.IsError() THEN
        RETURN HttpResponse{StatusCode: MapErrorToHTTPStatus(response.Error())}
    END IF

    RETURN JsonResponse(200, response.Value())
END FUNCTION
```

## Step 7: Test BFF Independently

Create tests that mock the bounded context clients.

```pseudocode
// handlers/home_bff_test

TYPE MockFacilityClient
    mock: Mock
END TYPE

METHOD MockFacilityClient.GetUserFacility(ctx: Context, userID: String) RETURNS Result<Facility, Error>
    args = this.mock.Called(ctx, userID)
    IF args.Get(0) == NULL THEN
        RETURN Error(args.Error(1))
    END IF
    RETURN Ok(args.Get(0) AS Facility)
END METHOD

TYPE MockAssetClient
    mock: Mock
END TYPE

METHOD MockAssetClient.GetFacilityAssets(ctx: Context, facilityID: String) RETURNS Result<List<Asset>, Error>
    args = this.mock.Called(ctx, facilityID)
    IF args.Get(0) == NULL THEN
        RETURN Error(args.Error(1))
    END IF
    RETURN Ok(args.Get(0) AS List<Asset>)
END METHOD

TYPE MockIntelligenceClient
    mock: Mock
END TYPE

METHOD MockIntelligenceClient.GetCurrentSchedule(ctx: Context, facilityID: String) RETURNS Result<Schedule, Error>
    args = this.mock.Called(ctx, facilityID)
    IF args.Get(0) == NULL THEN
        RETURN Error(args.Error(1))
    END IF
    RETURN Ok(args.Get(0) AS Schedule)
END METHOD


TEST GetHomeSummary_Success
    ctx = NewContext()
    facilityMock = NEW MockFacilityClient()
    assetMock = NEW MockAssetClient()
    intelligenceMock = NEW MockIntelligenceClient()

    facilityMock.mock.On("GetUserFacility", ctx, "user-123").Return(
        Facility{id: "f-1", name: "Home"},
        NULL
    )
    assetMock.mock.On("GetFacilityAssets", ctx, "f-1").Return(
        [
            Asset{id: "a-1", state: "online", currentLoadKW: 5.0},
            Asset{id: "a-2", state: "online", currentLoadKW: 7.5}
        ],
        NULL
    )
    intelligenceMock.mock.On("GetCurrentSchedule", ctx, "f-1").Return(
        Schedule{nextActionDesc: "Charge"},
        NULL
    )

    handler = NewHomeBFFHandler(facilityMock, assetMock, intelligenceMock)
    response = handler.GetHomeSummary(ctx, "user-123")

    ASSERT response.IsOk()
    ASSERT response.Value().facilityName == "Home"
    ASSERT response.Value().totalAssets == 2
    ASSERT response.Value().currentConsumptionKW == 12.5
END TEST


TEST GetHomeSummary_FacilityNotFound
    ctx = NewContext()
    facilityMock = NEW MockFacilityClient()
    assetMock = NEW MockAssetClient()
    intelligenceMock = NEW MockIntelligenceClient()

    facilityMock.mock.On("GetUserFacility", ctx, "unknown").Return(
        NULL,
        Error(ErrFacilityNotFound)
    )

    handler = NewHomeBFFHandler(facilityMock, assetMock, intelligenceMock)
    response = handler.GetHomeSummary(ctx, "unknown")

    ASSERT response.IsError()
    ASSERT response.Error().Contains(ErrFacilityNotFound)
END TEST
```

## Verification Checklist

After creating your BFF layer, verify:

- [ ] BFF has no domain logic (no business rules, no invariant checks)
- [ ] BFF only calls public bounded context APIs
- [ ] BFF does not access any database directly
- [ ] BFF is stateless (caching is for performance only)
- [ ] BFF does not emit domain events
- [ ] BFF does not own domain models (uses view DTOs only)
- [ ] Response shapes are client-specific, not domain shapes
- [ ] Error handling translates domain errors to client-friendly responses
- [ ] Each bounded context client is independently testable
- [ ] BFF handler can be tested with mocked clients
- [ ] OpenAPI contract matches implementation
- [ ] Caching has appropriate TTL and invalidation strategy
