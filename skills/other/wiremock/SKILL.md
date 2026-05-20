---
name: wiremock
description: Expert guidance for using WireMock in Java applications for HTTP API mocking and testing. Use this skill when the user asks to mock HTTP APIs, create API stubs, test REST clients, simulate network faults, verify HTTP requests, or integrate WireMock with Spring Boot. Trigger keywords include "wiremock", "mock http", "stub api", "http mock", "api testing", "rest mock", "simulate fault", "verify request", "spring boot wiremock".
---

You are an expert in using WireMock for HTTP API mocking in Java applications. You follow best practices for creating reliable, maintainable test mocks.

## Core concepts

WireMock enables you to stub HTTP responses for requests matching specific criteria. This allows testing of HTTP clients without depending on external services.

### Preferred configuration methods

The preferred approaches for configuring stubs are:

1. **JSON files** in the `mappings` directory (for test resources)
2. **Programmatic APIs** using the Java SDK (for dynamic test setup)

These methods work well with ephemeral WireMock instances in test contexts, avoiding the need for persistent WireMock servers.

## Stubbing basics

### Basic stub structure

Every stub requires:

- **Request matcher**: URL, method, headers, body patterns
- **Response definition**: Status code, headers, body content

```java
import static com.github.tomakehurst.wiremock.client.WireMock.*;

stubFor(get(urlEqualTo("/api/users"))
    .willReturn(aResponse()
        .withStatus(200)
        .withHeader("Content-Type", "application/json")
        .withBody("{\"users\": []}")));
```

### Java DSL shortcuts

WireMock provides convenient methods for common patterns:

```java
stubFor(get("/ping").willReturn(ok()));
stubFor(get("/users").willReturn(okJson("{\"users\": []}")));
stubFor(post("/redirect").willReturn(temporaryRedirect("/new/location")));
stubFor(get("/error").willReturn(serverError()));
stubFor(get("/not-found").willReturn(notFound()));
stubFor(get("/unauthorized").willReturn(unauthorized()));
```

### Response body options

**String literal:**

```java
.withBody("Hello, world!")
```

**JSON object:**

```java
.withBody("{\"message\": \"Hello\"}")
// Or use the convenience method:
.willReturn(okJson("{\"message\": \"Hello\"}"))
```

**File reference:**

```java
.withBodyFile("response.json")  // Relative to __files directory
```

**Binary data:**

```java
.withBody(binaryData)  // Base64-encoded in JSON
```

### Stub priority

When multiple stubs match a request, priority determines which responds. Lower numbers equal higher priority (1 is highest; default is 5).

```java
stubFor(get(urlEqualTo("/api/users/123"))
    .atPriority(1)
    .willReturn(aResponse().withStatus(200).withBody("Specific user")));

stubFor(get(urlMatching("/api/users/.*"))
    .atPriority(5)
    .willReturn(aResponse().withStatus(200).withBody("Any user")));
```

## JSON mapping files

JSON mapping files provide a declarative way to define stubs that can be version-controlled and reused across tests.

### Directory structure

Place mapping files in the test resources directory:

```
src/test/resources/
├── mappings/
│   ├── get-users.json
│   ├── create-user.json
│   └── error-scenarios.json
└── __files/
    ├── users-response.json
    └── user-created-response.json
```

### Basic mapping file structure

```json
{
    "request": {
        "method": "GET",
        "urlPath": "/api/users"
    },
    "response": {
        "status": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": "{\"users\": []}"
    }
}
```

### Using external body files

For larger responses, reference files from the `__files` directory:

```json
{
    "request": {
        "method": "GET",
        "urlPath": "/api/users"
    },
    "response": {
        "status": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "bodyFileName": "users-response.json"
    }
}
```

### Request matching in JSON

**URL path with query parameters:**

```json
{
    "request": {
        "method": "GET",
        "urlPath": "/api/search",
        "queryParameters": {
            "q": {
                "equalTo": "test"
            },
            "page": {
                "matches": "[0-9]+"
            }
        }
    },
    "response": {
        "status": 200
    }
}
```

**Header matching:**

```json
{
    "request": {
        "method": "POST",
        "urlPath": "/api/users",
        "headers": {
            "Content-Type": {
                "equalTo": "application/json"
            },
            "Authorization": {
                "matches": "Bearer .*"
            }
        }
    },
    "response": {
        "status": 201
    }
}
```

**Request body matching:**

```json
{
    "request": {
        "method": "POST",
        "urlPath": "/api/users",
        "bodyPatterns": [
            {
                "matchesJsonPath": "$.name"
            },
            {
                "matchesJsonPath": "$.email",
                "equalTo": "user@example.com"
            }
        ]
    },
    "response": {
        "status": 201
    }
}
```

### Priority in JSON mappings

```json
{
    "priority": 1,
    "request": {
        "method": "GET",
        "urlPath": "/api/users/123"
    },
    "response": {
        "status": 200,
        "body": "Specific user"
    }
}
```

### Loading mappings in tests

**Spring Boot integration:**

```java
@EnableWireMock({
    @ConfigureWireMock(
        name = "api-service",
        filesUnderClasspath = "wiremock"
    )
})
```

This loads mappings from `src/test/resources/wiremock/mappings/`.

**Programmatic loading:**

```java
WireMockServer wireMockServer = new WireMockServer(
    options()
        .usingFilesUnderClasspath("wiremock")
        .port(8080)
);
wireMockServer.start();
```

### Combining JSON and programmatic stubs

JSON mappings provide baseline stubs, while programmatic stubs handle test-specific scenarios:

```java
@Test
void testSpecificScenario() {
    // JSON mappings already loaded from src/test/resources/mappings/

    // Override or add test-specific stub
    stubFor(get("/api/users/999")
        .willReturn(notFound()));

    // Run test
    assertThrows(UserNotFoundException.class, () -> {
        apiClient.getUser(999);
    });
}
```

## Request matching

### URL matching strategies

**Exact URL match (including query parameters):**

```java
stubFor(get(urlEqualTo("/api/users?page=1"))
    .willReturn(ok()));
```

**URL regex:**

```java
stubFor(get(urlMatching("/api/users/[0-9]+"))
    .willReturn(ok()));
```

**Path-only equality (preferred for query parameters):**

```java
stubFor(get(urlPathEqualTo("/api/users"))
    .willReturn(ok()));
```

**Path-only regex:**

```java
stubFor(get(urlPathMatching("/api/users/.*"))
    .willReturn(ok()));
```

**Path templates (RFC 6570 compliant):**

```java
stubFor(get(urlPathTemplate("/contacts/{contactId}/addresses/{addressId}"))
    .willReturn(ok()));
```

### Query parameter matching

```java
stubFor(get(urlPathEqualTo("/api/users"))
    .withQueryParam("page", equalTo("1"))
    .withQueryParam("size", matching("[0-9]+"))
    .willReturn(ok()));
```

### Header matching

```java
stubFor(get(urlEqualTo("/api/users"))
    .withHeader("Accept", equalTo("application/json"))
    .withHeader("Authorization", matching("Bearer .*"))
    .willReturn(ok()));
```

### Header absence

```java
stubFor(get(urlEqualTo("/api/users"))
    .withHeader("X-Custom-Header", absent())
    .willReturn(ok()));
```

### Request body matching

**Exact match:**

```java
stubFor(post(urlEqualTo("/api/users"))
    .withRequestBody(equalTo("{\"name\": \"John\"}"))
    .willReturn(created()));
```

**Contains:**

```java
stubFor(post(urlEqualTo("/api/users"))
    .withRequestBody(containing("John"))
    .willReturn(created()));
```

**Regex:**

```java
stubFor(post(urlEqualTo("/api/users"))
    .withRequestBody(matching(".*\"name\"\\s*:\\s*\"[A-Z][a-z]+\".*"))
    .willReturn(created()));
```

**JSON equality:**

```java
stubFor(post(urlEqualTo("/api/users"))
    .withRequestBody(equalToJson("{\"name\": \"John\", \"age\": 30}", true, true))
    .willReturn(created()));
```

**JSON path matching:**

```java
stubFor(post(urlEqualTo("/api/users"))
    .withRequestBody(matchingJsonPath("$.name"))
    .withRequestBody(matchingJsonPath("$.age", equalTo("30")))
    .willReturn(created()));
```

**JSON schema validation:**

```java
stubFor(post(urlEqualTo("/api/users"))
    .withRequestBody(matchingJsonSchema(schemaJson))
    .willReturn(created()));
```

**XML equality:**

```java
stubFor(post(urlEqualTo("/api/users"))
    .withRequestBody(equalToXml("<user><name>John</name></user>"))
    .willReturn(created()));
```

**XPath matching:**

```java
stubFor(post(urlEqualTo("/api/users"))
    .withRequestBody(matchingXPath("//name[text()='John']"))
    .willReturn(created()));
```

### Basic authentication

```java
stubFor(get(urlEqualTo("/api/protected"))
    .withBasicAuth("username", "password")
    .willReturn(ok()));
```

### Cookie matching

```java
stubFor(get(urlEqualTo("/api/users"))
    .withCookie("session", matching("[A-Z0-9]+"))
    .willReturn(ok()));
```

### Logical operators

**AND combination:**

```java
stubFor(post(urlEqualTo("/api/users"))
    .withRequestBody(matching("[a-z]+").and(containing("magic")))
    .willReturn(ok()));
```

**OR combination:**

```java
stubFor(get(urlEqualTo("/api/users"))
    .withHeader("Accept", matching("application/json").or(matching("application/xml")))
    .willReturn(ok()));
```

**NOT negation:**

```java
stubFor(get(urlEqualTo("/api/users"))
    .withHeader("X-Internal", not(matching("true")))
    .willReturn(ok()));
```

## Simulating faults

### Fixed delays

Add delays to individual stubs:

```java
stubFor(get(urlEqualTo("/api/slow"))
    .willReturn(aResponse()
        .withStatus(200)
        .withFixedDelay(2000)));  // 2 second delay
```

### Random delays

**Lognormal distribution (realistic long-tail latencies):**

```java
stubFor(get(urlEqualTo("/api/variable"))
    .willReturn(aResponse()
        .withStatus(200)
        .withLogNormalRandomDelay(90, 0.1)));  // Median 90ms, sigma 0.1
```

**Uniform distribution (stable latency with jitter):**

```java
stubFor(get(urlEqualTo("/api/jitter"))
    .willReturn(aResponse()
        .withStatus(200)
        .withUniformRandomDelay(15, 25)));  // Between 15-25ms
```

### Chunked dribble delays

Simulate slow network connections by fragmenting responses:

```java
stubFor(get(urlEqualTo("/api/slow-download"))
    .willReturn(aResponse()
        .withBody("Large response body...")
        .withChunkedDribbleDelay(5, 1000)));  // 5 chunks over 1000ms
```

### Fault injection

Simulate corrupted or failed responses:

```java
import static com.github.tomakehurst.wiremock.http.Fault.*;

stubFor(get(urlEqualTo("/api/fault"))
    .willReturn(aResponse().withFault(MALFORMED_RESPONSE_CHUNK)));
```

**Available fault types:**

- `EMPTY_RESPONSE`: No response data
- `MALFORMED_RESPONSE_CHUNK`: Valid status, then corrupted data
- `RANDOM_DATA_THEN_CLOSE`: Garbage followed by connection closure
- `CONNECTION_RESET_BY_PEER`: Immediate disconnection

## Request verification

### Basic verification

Verify a request was made:

```java
import static com.github.tomakehurst.wiremock.client.WireMock.*;

verify(getRequestedFor(urlEqualTo("/api/users")));
verify(postRequestedFor(urlEqualTo("/api/users"))
    .withHeader("Content-Type", equalTo("application/json")));
```

### Count verification

Verify exact request counts:

```java
verify(exactly(3), postRequestedFor(urlEqualTo("/api/users")));
verify(lessThan(5), getRequestedFor(urlMatching("/api/.*")));
verify(moreThanOrExactly(1), deleteRequestedFor(urlEqualTo("/api/users/123")));
```

**Available count operators:**

- `exactly(n)`
- `lessThan(n)`
- `lessThanOrExactly(n)`
- `moreThan(n)`
- `moreThanOrExactly(n)`

### Retrieving all requests

```java
List<ServeEvent> allEvents = getAllServeEvents();
List<LoggedRequest> allRequests = findAll(anyRequestedFor(anyUrl()));
```

### Filtering requests

```java
List<LoggedRequest> userRequests = findAll(
    putRequestedFor(urlMatching("/api/users/.*")));
```

### Finding unmatched requests

```java
List<LoggedRequest> unmatchedRequests = findUnmatchedRequests();
```

### Near misses

Identify stub mappings that almost matched (useful for debugging):

```java
List<NearMiss> nearMisses = findNearMissesForAllUnmatchedRequests();
```

### Resetting request journal

```java
resetAllRequests();  // Clear request log only
reset();  // Clear both stubs and request log
```

## Spring Boot integration

### Setup

Add the dependency:

**Maven:**

```xml
<dependency>
    <groupId>org.wiremock.integrations</groupId>
    <artifactId>wiremock-spring-boot</artifactId>
    <version>3.10.0</version>
    <scope>test</scope>
</dependency>
```

**Gradle:**

```gradle
testImplementation 'org.wiremock.integrations:wiremock-spring-boot:3.10.0'
```

### Basic usage

```java
import org.springframework.boot.test.context.SpringBootTest;
import org.wiremock.spring.EnableWireMock;
import org.wiremock.spring.ConfigureWireMock;
import org.springframework.beans.factory.annotation.Value;
import static com.github.tomakehurst.wiremock.client.WireMock.*;

@SpringBootTest
@EnableWireMock
class ApiClientTest {

    @Value("${wiremock.server.baseUrl}")
    private String wireMockUrl;

    @Test
    void testApiClient() {
        stubFor(get("/api/users")
            .willReturn(okJson("[{\"id\": 1, \"name\": \"John\"}]")));

        // Test your API client
        List<User> users = apiClient.getUsers();

        assertThat(users).hasSize(1);
        verify(getRequestedFor(urlEqualTo("/api/users")));
    }
}
```

### Injected properties

The integration automatically provides:

- `wiremock.server.baseUrl` — Server base URL
- `wiremock.server.port` — HTTP port number

### Declarative configuration

```java
@SpringBootTest
@EnableWireMock({
    @ConfigureWireMock(
        name = "user-service",
        port = 8888,
        baseUrlProperties = "user-service.url"
    )
})
class ApiClientTest {
    @Value("${user-service.url}")
    private String userServiceUrl;
}
```

**Configuration options:**

- `port` — HTTP port (default: random)
- `httpsPort` — HTTPS port (default: random)
- `name` — Instance identifier (default: "wiremock")
- `baseUrlProperties` — Custom property name for base URL
- `portProperties` — Custom property name for port
- `filesUnderClasspath` — Classpath resource root for mappings
- `filesUnderDirectory` — Directory root for mappings

### Injecting WireMock instances

```java
import org.wiremock.spring.InjectWireMock;
import com.github.tomakehurst.wiremock.WireMockServer;

@SpringBootTest
@EnableWireMock
class ApiClientTest {

    @InjectWireMock
    private WireMockServer wireMock;

    @Test
    void testWithDirectAccess() {
        wireMock.stubFor(get("/api/users").willReturn(ok()));
        // Test code
    }
}
```

### Multiple WireMock instances

```java
@SpringBootTest
@EnableWireMock({
    @ConfigureWireMock(
        name = "user-service",
        baseUrlProperties = "user-service.url"
    ),
    @ConfigureWireMock(
        name = "order-service",
        baseUrlProperties = "order-service.url"
    )
})
class MultiServiceTest {

    @InjectWireMock("user-service")
    private WireMockServer userService;

    @InjectWireMock("order-service")
    private WireMockServer orderService;

    @Test
    void testMultipleServices() {
        userService.stubFor(get("/users/1").willReturn(okJson("{\"id\": 1}")));
        orderService.stubFor(get("/orders").willReturn(okJson("[]")));

        // Test code that calls both services
    }
}
```

### Programmatic configuration

For advanced control, implement `WireMockConfigurationCustomizer`:

```java
import org.wiremock.spring.WireMockConfigurationCustomizer;
import com.github.tomakehurst.wiremock.core.WireMockConfiguration;

@SpringBootTest
@EnableWireMock({
    @ConfigureWireMock(
        configurationCustomizers = CustomizerTest.Customizer.class
    )
})
class CustomizerTest {

    static class Customizer implements WireMockConfigurationCustomizer {
        @Override
        public void customize(
            WireMockConfiguration configuration,
            ConfigureWireMock options
        ) {
            configuration
                .notifier(new CustomNotifier())
                .extensions(new CustomTransformer());
        }
    }
}
```

## Stub management

### Listing stubs

```java
List<StubMapping> allStubs = WireMock.listAllStubMappings().getMappings();
```

### Editing stubs

```java
StubMapping stub = stubFor(get("/api/users").willReturn(ok()));
stub.setResponse(aResponse().withStatus(404));
editStub(stub);
```

### Removing stubs

```java
// Remove by ID
removeStub(stubId);

// Remove by metadata
removeStubsByMetadata(matchingJsonPath("$.tag", equalTo("temporary")));

// Remove all
WireMock.resetMappings();
```

### Finding unused stubs

```java
List<StubMapping> unusedStubs = findUnmatchedStubs();
```

## Best practices

### Use path-only matching for query parameters

Prefer `urlPathEqualTo()` over `urlEqualTo()` when matching query parameters separately to achieve order-invariant matching:

```java
// Good: Order-independent query parameter matching
stubFor(get(urlPathEqualTo("/api/search"))
    .withQueryParam("q", equalTo("test"))
    .withQueryParam("page", equalTo("1"))
    .willReturn(ok()));

// Avoid: Query parameter order matters
stubFor(get(urlEqualTo("/api/search?q=test&page=1"))
    .willReturn(ok()));
```

### Use appropriate matchers

Choose the most specific matcher for your use case:

- Use `equalTo()` for exact matches
- Use `matching()` for regex patterns
- Use `containing()` for substring checks
- Use `matchingJsonPath()` for JSON field matching
- Use `matchingJsonSchema()` for structural validation

### Organise stubs by priority

Use priority to create layered stub configurations:

- High priority (1-2): Specific test cases
- Medium priority (3-5): General cases
- Low priority (6+): Catch-all fallbacks

### Reset between tests

Always reset WireMock state between tests:

```java
@BeforeEach
void setUp() {
    WireMock.reset();  // Clears both stubs and request log
}
```

Or reset selectively:

```java
@BeforeEach
void setUp() {
    WireMock.resetAllRequests();  // Keep stubs, clear request log
}
```

### Use realistic delays

When simulating latency, use lognormal distribution for realistic long-tail behaviour:

```java
stubFor(get("/api/users")
    .willReturn(aResponse()
        .withStatus(200)
        .withLogNormalRandomDelay(100, 0.1)));
```

### Verify important interactions

Always verify that critical requests were made:

```java
@Test
void shouldCreateUser() {
    // Stub the response
    stubFor(post("/api/users").willReturn(created()));

    // Execute test
    apiClient.createUser(new User("John"));

    // Verify the request
    verify(postRequestedFor(urlEqualTo("/api/users"))
        .withRequestBody(matchingJsonPath("$.name", equalTo("John"))));
}
```

### Use meaningful stub names

When using multiple WireMock instances in Spring Boot, use descriptive names:

```java
@EnableWireMock({
    @ConfigureWireMock(name = "user-service"),
    @ConfigureWireMock(name = "payment-gateway"),
    @ConfigureWireMock(name = "notification-service")
})
```

### Prefer JSON mappings for reusable stubs

Use JSON mapping files for stubs that are reused across multiple tests:

```
src/test/resources/mappings/
├── common-success-responses.json
├── common-error-responses.json
└── service-specific/
    ├── user-service-stubs.json
    └── order-service-stubs.json
```

Reference external files for large response bodies:

```json
{
    "request": {
        "method": "GET",
        "urlPath": "/api/users"
    },
    "response": {
        "status": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "bodyFileName": "users-response.json"
    }
}
```

### Use programmatic stubs for test-specific scenarios

Reserve programmatic stub creation for test-specific cases that require dynamic behaviour:

```java
@Test
void shouldHandleSpecificEdgeCase() {
    // JSON mappings provide baseline stubs

    // Add test-specific stub programmatically
    stubFor(get("/api/users/edge-case")
        .willReturn(aResponse()
            .withStatus(200)
            .withBody(generateDynamicResponse())));

    // Test code
}
```

### Test error scenarios

Always test how your code handles failures:

```java
@Test
void shouldHandleServerError() {
    stubFor(get("/api/users").willReturn(serverError()));

    assertThrows(ServiceException.class, () -> {
        apiClient.getUsers();
    });
}

@Test
void shouldHandleTimeout() {
    stubFor(get("/api/users")
        .willReturn(aResponse()
            .withStatus(200)
            .withFixedDelay(5000)));  // Longer than client timeout

    assertThrows(TimeoutException.class, () -> {
        apiClient.getUsers();
    });
}
```

## Common patterns

### Stateful behaviour

Simulate stateful interactions using scenarios:

```java
stubFor(post("/api/orders")
    .inScenario("Order Flow")
    .whenScenarioStateIs(STARTED)
    .willReturn(created())
    .willSetStateTo("Order Created"));

stubFor(get("/api/orders/123")
    .inScenario("Order Flow")
    .whenScenarioStateIs("Order Created")
    .willReturn(okJson("{\"id\": 123, \"status\": \"PENDING\"}")));
```

### Response templating

Use response templates for dynamic responses (requires extension):

```java
stubFor(get(urlPathMatching("/api/users/([0-9]+)"))
    .willReturn(aResponse()
        .withBody("{\"id\": {{request.pathSegments.[2]}}, \"name\": \"User\"}")
        .withTransformers("response-template")));
```

### Conditional responses based on request content

```java
stubFor(post("/api/users")
    .withRequestBody(matchingJsonPath("$.role", equalTo("admin")))
    .willReturn(aResponse()
        .withStatus(201)
        .withBody("{\"role\": \"admin\"}")));

stubFor(post("/api/users")
    .withRequestBody(matchingJsonPath("$.role", equalTo("user")))
    .willReturn(aResponse()
        .withStatus(201)
        .withBody("{\"role\": \"user\"}")));
```

### Simulating rate limiting

```java
stubFor(get("/api/data")
    .inScenario("Rate Limit")
    .whenScenarioStateIs(STARTED)
    .willReturn(ok())
    .willSetStateTo("Request 1"));

stubFor(get("/api/data")
    .inScenario("Rate Limit")
    .whenScenarioStateIs("Request 1")
    .willReturn(ok())
    .willSetStateTo("Request 2"));

stubFor(get("/api/data")
    .inScenario("Rate Limit")
    .whenScenarioStateIs("Request 2")
    .willReturn(aResponse()
        .withStatus(429)
        .withHeader("Retry-After", "60")));
```
