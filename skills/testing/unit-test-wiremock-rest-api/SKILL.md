---
name: unit-test-wiremock-rest-api
description: Unit tests for external REST APIs using WireMock to mock HTTP endpoints. Use when testing service integrations with external APIs.
category: testing
tags: [junit-5, wiremock, unit-testing, rest-api, mocking, http-stubbing]
version: 1.0.1
---

# Unit Testing REST APIs with WireMock

Test interactions with third-party REST APIs without making real network calls using WireMock. This skill focuses on pure unit tests (no Spring context) that stub HTTP responses and verify requests.

## When to Use This Skill

Use this skill when:
- Testing services that call external REST APIs
- Need to stub HTTP responses for predictable test behavior
- Want to test error scenarios (timeouts, 500 errors, malformed responses)
- Need to verify request details (headers, query params, request body)
- Integrating with third-party services (payment gateways, weather APIs, etc.)
- Testing without network dependencies or rate limits
- Building unit tests that run fast in CI/CD pipelines

## Core Dependencies

### Maven
```xml
<dependency>
  <groupId>org.wiremock</groupId>
  <artifactId>wiremock</artifactId>
  <version>3.4.1</version>
  <scope>test</scope>
</dependency>
<dependency>
  <groupId>org.junit.jupiter</groupId>
  <artifactId>junit-jupiter</artifactId>
  <scope>test</scope>
</dependency>
<dependency>
  <groupId>org.assertj</groupId>
  <artifactId>assertj-core</artifactId>
  <scope>test</scope>
</dependency>
```

### Gradle
```kotlin
dependencies {
  testImplementation("org.wiremock:wiremock:3.4.1")
  testImplementation("org.junit.jupiter:junit-jupiter")
  testImplementation("org.assertj:assertj-core")
}
```

## Basic Pattern: Stubbing and Verifying

### Simple Stub with WireMock Extension

```java
import com.github.tomakehurst.wiremock.junit5.WireMockExtension;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.RegisterExtension;
import static com.github.tomakehurst.wiremock.client.WireMock.*;
import static org.assertj.core.api.Assertions.assertThat;

class ExternalWeatherServiceTest {

  @RegisterExtension
  static WireMockExtension wireMock = WireMockExtension.newInstance()
    .options(wireMockConfig().dynamicPort())
    .build();

  @Test
  void shouldFetchWeatherDataFromExternalApi() {
    wireMock.stubFor(get(urlEqualTo("/weather?city=London"))
      .withHeader("Accept", containing("application/json"))
      .willReturn(aResponse()
        .withStatus(200)
        .withHeader("Content-Type", "application/json")
        .withBody("{\"city\":\"London\",\"temperature\":15,\"condition\":\"Cloudy\"}")));

    String baseUrl = wireMock.getRuntimeInfo().getHttpBaseUrl();
    WeatherApiClient client = new WeatherApiClient(baseUrl);
    WeatherData weather = client.getWeather("London");

    assertThat(weather.getCity()).isEqualTo("London");
    assertThat(weather.getTemperature()).isEqualTo(15);

    wireMock.verify(getRequestedFor(urlEqualTo("/weather?city=London"))
      .withHeader("Accept", containing("application/json")));
  }
}
```

## Testing Error Scenarios

### Test 4xx and 5xx Responses

```java
@Test
void shouldHandleNotFoundError() {
  wireMock.stubFor(get(urlEqualTo("/api/users/999"))
    .willReturn(aResponse()
      .withStatus(404)
      .withBody("{\"error\":\"User not found\"}")));

  WeatherApiClient client = new WeatherApiClient(wireMock.getRuntimeInfo().getHttpBaseUrl());
  
  assertThatThrownBy(() -> client.getUser(999))
    .isInstanceOf(UserNotFoundException.class)
    .hasMessageContaining("User not found");
}

@Test
void shouldRetryOnServerError() {
  wireMock.stubFor(get(urlEqualTo("/api/data"))
    .willReturn(aResponse()
      .withStatus(500)
      .withBody("{\"error\":\"Internal server error\"}")));

  ApiClient client = new ApiClient(wireMock.getRuntimeInfo().getHttpBaseUrl());
  
  assertThatThrownBy(() -> client.fetchData())
    .isInstanceOf(ServerErrorException.class);
}
```

## Request Verification

### Verify Request Details and Payload

```java
@Test
void shouldVerifyRequestBody() {
  wireMock.stubFor(post(urlEqualTo("/api/users"))
    .willReturn(aResponse()
      .withStatus(201)
      .withBody("{\"id\":123,\"name\":\"Alice\"}")));

  ApiClient client = new ApiClient(wireMock.getRuntimeInfo().getHttpBaseUrl());
  UserResponse response = client.createUser("Alice");

  assertThat(response.getId()).isEqualTo(123);
  
  wireMock.verify(postRequestedFor(urlEqualTo("/api/users"))
    .withRequestBody(matchingJsonPath("$.name", equalTo("Alice")))
    .withHeader("Content-Type", containing("application/json")));
}
```

## Best Practices

- **Use dynamic port** to avoid port conflicts in parallel test execution
- **Verify requests** to ensure correct API usage
- **Test error scenarios** thoroughly
- **Keep stubs focused** - one concern per test
- **Reset WireMock** between tests automatically via `@RegisterExtension`
- **Never call real APIs** - always stub third-party endpoints

## Troubleshooting

**WireMock not intercepting requests**: Ensure your HTTP client uses the stubbed URL from `wireMock.getRuntimeInfo().getHttpBaseUrl()`.

**Port conflicts**: Always use `wireMockConfig().dynamicPort()` to let WireMock choose available port.

## References

- [WireMock Official Documentation](https://wiremock.org/)
- [WireMock Stubs and Mocking](https://wiremock.org/docs/stubbing/)
- [JUnit 5 Extensions](https://junit.org/junit5/docs/current/user-guide/#extensions)
