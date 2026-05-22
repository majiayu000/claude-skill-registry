---
name: unit-test-controller-layer
description: Unit tests for REST controllers using MockMvc and @WebMvcTest. Test request/response mapping, validation, and exception handling. Use when testing web layer endpoints in isolation.
category: testing
tags: [junit-5, mockito, unit-testing, controller, rest, mockmvc]
version: 1.0.1
---

# Unit Testing REST Controllers with MockMvc

Test @RestController and @Controller classes by mocking service dependencies and verifying HTTP responses, status codes, and serialization. Use MockMvc for lightweight controller testing without loading the full Spring context.

## When to Use This Skill

Use this skill when:
- Testing REST controller request/response handling
- Verifying HTTP status codes and response formats
- Testing request parameter binding and validation
- Mocking service layer for isolated controller tests
- Testing content negotiation and response headers
- Want fast controller tests without integration test overhead

## Setup: MockMvc + Mockito

### Maven
```xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-test</artifactId>
  <scope>test</scope>
</dependency>
<dependency>
  <groupId>org.mockito</groupId>
  <artifactId>mockito-core</artifactId>
  <scope>test</scope>
</dependency>
```

### Gradle
```kotlin
dependencies {
  testImplementation("org.springframework.boot:spring-boot-starter-test")
  testImplementation("org.mockito:mockito-core")
}
```

## Basic Pattern: Testing GET Endpoint

### Simple GET Endpoint Test

```java
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;
import static org.mockito.Mockito.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@ExtendWith(MockitoExtension.class)
class UserControllerTest {

  @Mock
  private UserService userService;

  @InjectMocks
  private UserController userController;

  private MockMvc mockMvc;

  void setUp() {
    mockMvc = MockMvcBuilders.standaloneSetup(userController).build();
  }

  @Test
  void shouldReturnAllUsers() throws Exception {
    List<UserDto> users = List.of(
      new UserDto(1L, "Alice"),
      new UserDto(2L, "Bob")
    );
    when(userService.getAllUsers()).thenReturn(users);

    mockMvc.perform(get("/api/users"))
      .andExpect(status().isOk())
      .andExpect(jsonPath("$").isArray())
      .andExpect(jsonPath("$[0].id").value(1))
      .andExpect(jsonPath("$[0].name").value("Alice"))
      .andExpect(jsonPath("$[1].id").value(2));

    verify(userService, times(1)).getAllUsers();
  }

  @Test
  void shouldReturnUserById() throws Exception {
    UserDto user = new UserDto(1L, "Alice");
    when(userService.getUserById(1L)).thenReturn(user);

    mockMvc.perform(get("/api/users/1"))
      .andExpect(status().isOk())
      .andExpect(jsonPath("$.id").value(1))
      .andExpect(jsonPath("$.name").value("Alice"));

    verify(userService).getUserById(1L);
  }
}
```

## Testing POST Endpoint

### Create Resource with Request Body

```java
@Test
void shouldCreateUserAndReturn201() throws Exception {
  UserCreateRequest request = new UserCreateRequest("Alice", "alice@example.com");
  UserDto createdUser = new UserDto(1L, "Alice", "alice@example.com");
  
  when(userService.createUser(any(UserCreateRequest.class)))
    .thenReturn(createdUser);

  mockMvc.perform(post("/api/users")
      .contentType("application/json")
      .content("{\"name\":\"Alice\",\"email\":\"alice@example.com\"}"))
    .andExpect(status().isCreated())
    .andExpect(jsonPath("$.id").value(1))
    .andExpect(jsonPath("$.name").value("Alice"))
    .andExpect(jsonPath("$.email").value("alice@example.com"));

  verify(userService).createUser(any(UserCreateRequest.class));
}
```

## Testing Error Scenarios

### Handle 404 Not Found

```java
@Test
void shouldReturn404WhenUserNotFound() throws Exception {
  when(userService.getUserById(999L))
    .thenThrow(new UserNotFoundException("User not found"));

  mockMvc.perform(get("/api/users/999"))
    .andExpect(status().isNotFound())
    .andExpect(jsonPath("$.error").value("User not found"));

  verify(userService).getUserById(999L);
}
```

### Handle 400 Bad Request

```java
@Test
void shouldReturn400WhenRequestBodyInvalid() throws Exception {
  mockMvc.perform(post("/api/users")
      .contentType("application/json")
      .content("{\"name\":\"\"}")) // Empty name
    .andExpect(status().isBadRequest())
    .andExpect(jsonPath("$.errors").isArray());
}
```

## Testing PUT/PATCH Endpoints

### Update Resource

```java
@Test
void shouldUpdateUserAndReturn200() throws Exception {
  UserUpdateRequest request = new UserUpdateRequest("Alice Updated");
  UserDto updatedUser = new UserDto(1L, "Alice Updated");
  
  when(userService.updateUser(eq(1L), any(UserUpdateRequest.class)))
    .thenReturn(updatedUser);

  mockMvc.perform(put("/api/users/1")
      .contentType("application/json")
      .content("{\"name\":\"Alice Updated\"}"))
    .andExpect(status().isOk())
    .andExpect(jsonPath("$.id").value(1))
    .andExpect(jsonPath("$.name").value("Alice Updated"));

  verify(userService).updateUser(eq(1L), any(UserUpdateRequest.class));
}
```

## Testing DELETE Endpoint

### Delete Resource

```java
@Test
void shouldDeleteUserAndReturn204() throws Exception {
  doNothing().when(userService).deleteUser(1L);

  mockMvc.perform(delete("/api/users/1"))
    .andExpect(status().isNoContent());

  verify(userService).deleteUser(1L);
}

@Test
void shouldReturn404WhenDeletingNonExistentUser() throws Exception {
  doThrow(new UserNotFoundException("User not found"))
    .when(userService).deleteUser(999L);

  mockMvc.perform(delete("/api/users/999"))
    .andExpect(status().isNotFound());
}
```

## Testing Request Parameters

### Query Parameters

```java
@Test
void shouldFilterUsersByName() throws Exception {
  List<UserDto> users = List.of(new UserDto(1L, "Alice"));
  when(userService.searchUsers("Alice")).thenReturn(users);

  mockMvc.perform(get("/api/users/search?name=Alice"))
    .andExpect(status().isOk())
    .andExpect(jsonPath("$").isArray())
    .andExpect(jsonPath("$[0].name").value("Alice"));

  verify(userService).searchUsers("Alice");
}
```

### Path Variables

```java
@Test
void shouldGetUserByIdFromPath() throws Exception {
  UserDto user = new UserDto(123L, "Alice");
  when(userService.getUserById(123L)).thenReturn(user);

  mockMvc.perform(get("/api/users/{id}", 123L))
    .andExpect(status().isOk())
    .andExpect(jsonPath("$.id").value(123));
}
```

## Testing Response Headers

### Verify Response Headers

```java
@Test
void shouldReturnCustomHeaders() throws Exception {
  when(userService.getAllUsers()).thenReturn(List.of());

  mockMvc.perform(get("/api/users"))
    .andExpect(status().isOk())
    .andExpect(header().exists("X-Total-Count"))
    .andExpect(header().string("X-Total-Count", "0"))
    .andExpect(header().string("Content-Type", containsString("application/json")));
}
```

## Testing Request Headers

### Send Request Headers

```java
@Test
void shouldRequireAuthorizationHeader() throws Exception {
  mockMvc.perform(get("/api/users"))
    .andExpect(status().isUnauthorized());

  mockMvc.perform(get("/api/users")
      .header("Authorization", "Bearer token123"))
    .andExpect(status().isOk());
}
```

## Content Negotiation

### Test Different Accept Headers

```java
@Test
void shouldReturnJsonWhenAcceptHeaderIsJson() throws Exception {
  UserDto user = new UserDto(1L, "Alice");
  when(userService.getUserById(1L)).thenReturn(user);

  mockMvc.perform(get("/api/users/1")
      .accept("application/json"))
    .andExpect(status().isOk())
    .andExpect(content().contentType("application/json"));
}
```

## Advanced: Testing Multiple Status Codes

```java
@Test
void shouldReturnDifferentStatusCodesForDifferentScenarios() throws Exception {
  // Successful response
  when(userService.getUserById(1L)).thenReturn(new UserDto(1L, "Alice"));
  mockMvc.perform(get("/api/users/1"))
    .andExpect(status().isOk());

  // Not found
  when(userService.getUserById(999L))
    .thenThrow(new UserNotFoundException("Not found"));
  mockMvc.perform(get("/api/users/999"))
    .andExpect(status().isNotFound());

  // Unauthorized
  mockMvc.perform(get("/api/admin/users"))
    .andExpect(status().isUnauthorized());
}
```

## Best Practices

- **Use standalone setup** when testing single controller: `MockMvcBuilders.standaloneSetup()`
- **Mock service layer** - controllers should focus on HTTP handling
- **Test happy path and error paths** thoroughly
- **Verify service method calls** to ensure controller delegates correctly
- **Use content() matchers** for response body validation
- **Keep tests focused** on one endpoint behavior per test
- **Use JsonPath** for fluent JSON response assertions

## Common Pitfalls

- **Testing business logic in controller**: Move to service tests
- **Not mocking service layer**: Always mock service dependencies
- **Testing framework behavior**: Focus on your code, not Spring code
- **Hardcoding URLs**: Use MockMvcRequestBuilders helpers
- **Not verifying mock interactions**: Always verify service was called correctly

## Troubleshooting

**Content type mismatch**: Ensure `contentType()` matches controller's `@PostMapping(consumes=...)` or use default.

**JsonPath not matching**: Use `mockMvc.perform(...).andDo(print())` to see actual response content.

**Status code assertions fail**: Check controller `@RequestMapping`, `@PostMapping` status codes and error handling.

## References

- [Spring MockMvc Documentation](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/test/web/servlet/MockMvc.html)
- [JsonPath for REST Assertions](https://goessner.net/articles/JsonPath/)
- [Spring Testing Best Practices](https://docs.spring.io/spring-boot/docs/current/reference/html/features.html#features.testing)
