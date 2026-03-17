---
name: cui-testing-http
description: CUI MockWebServer standards for HTTP client testing with JUnit 5 integration
user-invocable: false
allowed-tools: Read, Grep, Glob
---

# CUI Testing HTTP Skill

**REFERENCE MODE**: This skill provides reference material. Load specific standards on-demand based on current task.

CUI-specific HTTP testing standards for projects using cui-test-mockwebserver-junit5. This skill covers MockWebServer configuration, HTTPS testing, and request verification patterns.

## Prerequisites

This skill requires CUI test library dependencies:
- `de.cuioss.test:cui-test-mockwebserver-junit5` (EnableMockWebServer, MockResponseConfig)

## Workflow

### Step 1: Load MockWebServer Standards

**CRITICAL**: Load this standard for any HTTP client testing work.

```
Read: standards/testing-mockwebserver.md
```

This provides the foundational rules:
- `@EnableMockWebServer` annotation for test classes
- `@MockResponseConfig` for declarative response mocking
- `@ModuleDispatcher` for complex routing scenarios
- HTTPS support with automatic certificate generation

## Key Rules Summary

### Basic MockWebServer Setup
```java
// CORRECT - Use annotation-based configuration
@EnableMockWebServer
@MockResponseConfig(
    path = "/api/users",
    method = HttpMethodMapper.GET,
    status = 200,
    jsonContentKeyValue = "users=[]"
)
class SimpleMockWebServerTest {

    @Test
    @DisplayName("Should fetch users from API")
    void shouldFetchUsers(URIBuilder uriBuilder) throws Exception {
        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
            .uri(uriBuilder.addPathSegments("api", "users").build())
            .GET()
            .build();

        HttpResponse<String> response = client.send(request,
            HttpResponse.BodyHandlers.ofString());

        assertEquals(200, response.statusCode());
    }
}
```

### HTTPS Testing
```java
// CORRECT - Enable HTTPS with auto-generated certificates
@EnableMockWebServer(useHttps = true)
class HttpsTest {

    @Test
    void shouldConnectViaHttps(URIBuilder uriBuilder, SSLContext sslContext) {
        assertEquals("https", uriBuilder.build().getScheme());

        HttpClient client = HttpClient.newBuilder()
            .sslContext(sslContext)
            .build();
        // Test with HTTPS...
    }
}
```

### Request Verification
```java
// CORRECT - Verify request details with MockWebServer parameter
@Test
void shouldVerifyRequest(MockWebServer server, URIBuilder uriBuilder) throws Exception {
    client.fetchSecureResource(uriBuilder.addPathSegments("api", "users").build(), "token");

    RecordedRequest request = server.takeRequest();
    assertEquals("Bearer token", request.getHeader("Authorization"));
    assertEquals("GET", request.getMethod());
}
```

### Complex Routing with ModuleDispatcher
```java
// CORRECT - Use @ModuleDispatcher for dynamic responses
@EnableMockWebServer
@ModuleDispatcher
class ComplexRoutingTest {

    ModuleDispatcherElement getModuleDispatcher() {
        return new ModuleDispatcherElement() {
            @Override
            public String getBaseUrl() { return "/api"; }

            @Override
            public Optional<MockResponse> handleGet(RecordedRequest request) {
                if (request.getPath().endsWith("/api/users/active")) {
                    return Optional.of(new MockResponse.Builder()
                        .code(200)
                        .body("{\"users\":[]}")
                        .build());
                }
                return Optional.empty();
            }

            @Override
            public Set<HttpMethodMapper> supportedMethods() {
                return Set.of(HttpMethodMapper.GET);
            }
        };
    }
}
```

## Related Skills

- `pm-dev-java-cui:cui-http` - CUI HTTP client patterns
- `pm-dev-java-cui:cui-testing` - CUI test generator framework
- `pm-dev-java:junit-core` - General JUnit 5 patterns

## Standards Reference

| Standard | Purpose |
|----------|---------|
| testing-mockwebserver.md | MockWebServer configuration and patterns |
