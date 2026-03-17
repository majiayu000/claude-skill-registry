---
name: unit-test-security-authorization
description: Provides patterns for unit testing Spring Security with @PreAuthorize, @Secured, @RolesAllowed. Validates role-based access control and authorization policies. Use when testing security configurations and access control logic.
allowed-tools: Read, Write, Bash, Glob, Grep
---

# Unit Testing Security and Authorization

## Overview

This skill provides patterns for unit testing Spring Security authorization logic using @PreAuthorize, @Secured, @RolesAllowed, and custom permission evaluators. It covers testing role-based access control (RBAC), expression-based authorization, custom permission evaluators, and verifying access denied scenarios without full Spring Security context.

## When to Use

Use this skill when:
- Testing @PreAuthorize and @Secured method-level security
- Testing role-based access control (RBAC)
- Testing custom permission evaluators
- Verifying access denied scenarios
- Testing authorization with authenticated principals
- Want fast authorization tests without full Spring Security context

## Instructions

Follow these steps to test Spring Security authorization:

### 1. Set Up Security Testing Dependencies

Add spring-security-test to your test dependencies along with JUnit 5 and AssertJ.

### 2. Enable Method Security in Configuration

Use @EnableGlobalMethodSecurity(prePostEnabled = true) to activate @PreAuthorize annotations.

### 3. Create Test with @WithMockUser

Apply @WithMockUser annotation to simulate authenticated users with specific roles and authorities.

### 4. Test Both Allow and Deny Scenarios

For each security rule, test that authorized users can access the method and unauthorized users receive AccessDeniedException.

### 5. Test Expression-Based Authorization

Verify complex expressions like authentication.principal.username == #owner work correctly.

### 6. Test Custom Permission Evaluators

Unit test custom PermissionEvaluator implementations by creating Authentication objects and calling hasPermission directly.

### 7. Verify Method Interactions

Mock external dependencies and verify that security checks don't interfere with business logic.

## Examples

## Setup: Security Testing

### Maven
```xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-security</artifactId>
</dependency>
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-test</artifactId>
  <scope>test</scope>
</dependency>
<dependency>
  <groupId>org.springframework.security</groupId>
  <artifactId>spring-security-test</artifactId>
  <scope>test</scope>
</dependency>
```

### Gradle
```kotlin
dependencies {
  implementation("org.springframework.boot:spring-boot-starter-security")
  testImplementation("org.springframework.boot:spring-boot-starter-test")
  testImplementation("org.springframework.security:spring-security-test")
}
```

## Basic Pattern: Testing @PreAuthorize

### Simple Role-Based Access Control

```java
// Service with security annotations
@Service
public class UserService {

  @PreAuthorize("hasRole('ADMIN')")
  public void deleteUser(Long userId) {
    // delete logic
  }

  @PreAuthorize("hasRole('USER')")
  public User getCurrentUser() {
    // get user logic
  }

  @PreAuthorize("hasAnyRole('ADMIN', 'MANAGER')")
  public List<User> listAllUsers() {
    // list logic
  }
}

// Unit test
import org.junit.jupiter.api.Test;
import org.springframework.security.test.context.support.WithMockUser;
import static org.assertj.core.api.Assertions.*;

class UserServiceSecurityTest {

  @Test
  @WithMockUser(roles = "ADMIN")
  void shouldAllowAdminToDeleteUser() {
    UserService service = new UserService();
    
    assertThatCode(() -> service.deleteUser(1L))
      .doesNotThrowAnyException();
  }

  @Test
  @WithMockUser(roles = "USER")
  void shouldDenyUserFromDeletingUser() {
    UserService service = new UserService();
    
    assertThatThrownBy(() -> service.deleteUser(1L))
      .isInstanceOf(AccessDeniedException.class);
  }

  @Test
  @WithMockUser(roles = "ADMIN")
  void shouldAllowAdminAndManagerToListUsers() {
    UserService service = new UserService();
    
    assertThatCode(() -> service.listAllUsers())
      .doesNotThrowAnyException();
  }

  @Test
  void shouldDenyAnonymousUserAccess() {
    UserService service = new UserService();
    
    assertThatThrownBy(() -> service.deleteUser(1L))
      .isInstanceOf(AccessDeniedException.class);
  }
}
```

## Testing @Secured Annotation

### Legacy Security Configuration

```java
@Service
public class OrderService {

  @Secured("ROLE_ADMIN")
  public Order approveOrder(Long orderId) {
    // approval logic
  }

  @Secured({"ROLE_ADMIN", "ROLE_MANAGER"})
  public List<Order> getOrders() {
    // get orders
  }
}

class OrderSecurityTest {

  @Test
  @WithMockUser(roles = "ADMIN")
  void shouldAllowAdminToApproveOrder() {
    OrderService service = new OrderService();
    
    assertThatCode(() -> service.approveOrder(1L))
      .doesNotThrowAnyException();
  }

  @Test
  @WithMockUser(roles = "USER")
  void shouldDenyUserFromApprovingOrder() {
    OrderService service = new OrderService();
    
    assertThatThrownBy(() -> service.approveOrder(1L))
      .isInstanceOf(AccessDeniedException.class);
  }
}
```

## Testing Controller Security with MockMvc

### Secure REST Endpoints

```java
@RestController
@RequestMapping("/api/admin")
public class AdminController {

  @GetMapping("/users")
  @PreAuthorize("hasRole('ADMIN')")
  public List<UserDto> listAllUsers() {
    // logic
  }

  @DeleteMapping("/users/{id}")
  @PreAuthorize("hasRole('ADMIN')")
  public void deleteUser(@PathVariable Long id) {
    // delete logic
  }
}

// Testing with MockMvc
import org.springframework.security.test.context.support.WithMockUser;
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

class AdminControllerSecurityTest {

  private MockMvc mockMvc;

  @BeforeEach
  void setUp() {
    mockMvc = MockMvcBuilders
      .standaloneSetup(new AdminController())
      .apply(springSecurity())
      .build();
  }

  @Test
  @WithMockUser(roles = "ADMIN")
  void shouldAllowAdminToListUsers() throws Exception {
    mockMvc.perform(get("/api/admin/users"))
      .andExpect(status().isOk());
  }

  @Test
  @WithMockUser(roles = "USER")
  void shouldDenyUserFromListingUsers() throws Exception {
    mockMvc.perform(get("/api/admin/users"))
      .andExpect(status().isForbidden());
  }

  @Test
  void shouldDenyAnonymousAccessToAdminEndpoint() throws Exception {
    mockMvc.perform(get("/api/admin/users"))
      .andExpect(status().isUnauthorized());
  }

  @Test
  @WithMockUser(roles = "ADMIN")
  void shouldAllowAdminToDeleteUser() throws Exception {
    mockMvc.perform(delete("/api/admin/users/1"))
      .andExpect(status().isOk());
  }
}
```

## Testing Expression-Based Authorization

### Complex Permission Expressions

```java
@Service
public class DocumentService {

  @PreAuthorize("hasRole('ADMIN') or authentication.principal.username == #owner")
  public Document getDocument(String owner, Long docId) {
    // get document
  }

  @PreAuthorize("hasPermission(#docId, 'Document', 'WRITE')")
  public void updateDocument(Long docId, String content) {
    // update logic
  }

  @PreAuthorize("#userId == authentication.principal.id")
  public UserProfile getUserProfile(Long userId) {
    // get profile
  }
}

class ExpressionBasedSecurityTest {

  @Test
  @WithMockUser(username = "alice", roles = "ADMIN")
  void shouldAllowAdminToAccessAnyDocument() {
    DocumentService service = new DocumentService();
    
    assertThatCode(() -> service.getDocument("bob", 1L))
      .doesNotThrowAnyException();
  }

  @Test
  @WithMockUser(username = "alice")
  void shouldAllowOwnerToAccessOwnDocument() {
    DocumentService service = new DocumentService();
    
    assertThatCode(() -> service.getDocument("alice", 1L))
      .doesNotThrowAnyException();
  }

  @Test
  @WithMockUser(username = "alice")
  void shouldDenyUserAccessToOtherUserDocument() {
    DocumentService service = new DocumentService();
    
    assertThatThrownBy(() -> service.getDocument("bob", 1L))
      .isInstanceOf(AccessDeniedException.class);
  }

  @Test
  @WithMockUser(username = "alice", id = "1")
  void shouldAllowUserToAccessOwnProfile() {
    DocumentService service = new DocumentService();
    
    assertThatCode(() -> service.getUserProfile(1L))
      .doesNotThrowAnyException();
  }

  @Test
  @WithMockUser(username = "alice", id = "1")
  void shouldDenyUserAccessToOtherProfile() {
    DocumentService service = new DocumentService();
    
    assertThatThrownBy(() -> service.getUserProfile(999L))
      .isInstanceOf(AccessDeniedException.class);
  }
}
```

## Testing Custom Permission Evaluator

### Create and Test Custom Permission Logic

```java
// Custom permission evaluator
@Component
public class DocumentPermissionEvaluator implements PermissionEvaluator {

  private final DocumentRepository documentRepository;

  public DocumentPermissionEvaluator(DocumentRepository documentRepository) {
    this.documentRepository = documentRepository;
  }

  @Override
  public boolean hasPermission(Authentication authentication, Object targetDomainObject, Object permission) {
    if (authentication == null) return false;
    
    Document document = (Document) targetDomainObject;
    String userUsername = authentication.getName();
    
    return document.getOwner().getUsername().equals(userUsername) ||
           userHasRole(authentication, "ADMIN");
  }

  @Override
  public boolean hasPermission(Authentication authentication, Serializable targetId, String targetType, Object permission) {
    if (authentication == null) return false;
    if (!"Document".equals(targetType)) return false;

    Document document = documentRepository.findById((Long) targetId).orElse(null);
    if (document == null) return false;

    return hasPermission(authentication, document, permission);
  }

  private boolean userHasRole(Authentication authentication, String role) {
    return authentication.getAuthorities().stream()
      .anyMatch(auth -> auth.getAuthority().equals("ROLE_" + role));
  }
}

// Unit test for custom evaluator
class DocumentPermissionEvaluatorTest {

  private DocumentPermissionEvaluator evaluator;
  private DocumentRepository documentRepository;
  private Authentication adminAuth;
  private Authentication userAuth;
  private Document document;

  @BeforeEach
  void setUp() {
    documentRepository = mock(DocumentRepository.class);
    evaluator = new DocumentPermissionEvaluator(documentRepository);

    document = new Document(1L, "Test Doc", new User("alice"));

    adminAuth = new UsernamePasswordAuthenticationToken(
      "admin",
      null,
      List.of(new SimpleGrantedAuthority("ROLE_ADMIN"))
    );

    userAuth = new UsernamePasswordAuthenticationToken(
      "alice",
      null,
      List.of(new SimpleGrantedAuthority("ROLE_USER"))
    );
  }

  @Test
  void shouldGrantPermissionToDocumentOwner() {
    boolean hasPermission = evaluator.hasPermission(userAuth, document, "WRITE");
    
    assertThat(hasPermission).isTrue();
  }

  @Test
  void shouldDenyPermissionToNonOwner() {
    Authentication otherUserAuth = new UsernamePasswordAuthenticationToken(
      "bob",
      null,
      List.of(new SimpleGrantedAuthority("ROLE_USER"))
    );

    boolean hasPermission = evaluator.hasPermission(otherUserAuth, document, "WRITE");
    
    assertThat(hasPermission).isFalse();
  }

  @Test
  void shouldGrantPermissionToAdmin() {
    boolean hasPermission = evaluator.hasPermission(adminAuth, document, "WRITE");
    
    assertThat(hasPermission).isTrue();
  }

  @Test
  void shouldDenyNullAuthentication() {
    boolean hasPermission = evaluator.hasPermission(null, document, "WRITE");
    
    assertThat(hasPermission).isFalse();
  }
}
```

## Testing Multiple Roles

### Parameterized Role Testing

```java
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

class RoleBasedAccessTest {

  private AdminService service;

  @BeforeEach
  void setUp() {
    service = new AdminService();
  }

  @ParameterizedTest
  @ValueSource(strings = {"ADMIN", "SUPER_ADMIN", "SYSTEM"})
  @WithMockUser(roles = "ADMIN")
  void shouldAllowPrivilegedRolesToDeleteUser(String role) {
    assertThatCode(() -> service.deleteUser(1L))
      .doesNotThrowAnyException();
  }

  @ParameterizedTest
  @ValueSource(strings = {"USER", "GUEST", "READONLY"})
  void shouldDenyUnprivilegedRolesToDeleteUser(String role) {
    assertThatThrownBy(() -> service.deleteUser(1L))
      .isInstanceOf(AccessDeniedException.class);
  }
}
```

## Best Practices

- **Use @WithMockUser** for setting authenticated user context
- **Test both allow and deny cases** for each security rule
- **Test with different roles** to verify role-based decisions
- **Test expression-based security** comprehensively
- **Mock external dependencies** (permission evaluators, etc.)
- **Test anonymous access separately** from authenticated access
- **Use @EnableGlobalMethodSecurity** in configuration for method-level security

## Common Pitfalls

- Forgetting to enable method security in test configuration
- Not testing both allow and deny scenarios
- Testing framework code instead of authorization logic
- Not handling null authentication in tests
- Mixing authentication and authorization tests unnecessarily

## Constraints and Warnings

- **Method security requires proxy**: @PreAuthorize works via proxies; direct method calls bypass security
- **@EnableGlobalMethodSecurity**: Must be enabled for @PreAuthorize, @Secured to work
- **Role prefix**: Spring adds "ROLE_" prefix automatically; use hasRole('ADMIN') not hasRole('ROLE_ADMIN')
- **Authentication context**: Security context is thread-local; be careful with async tests
- **@WithMockUser limitations**: Creates a simple Authentication; complex auth scenarios need custom setup
- **SpEL expressions**: Complex SpEL in @PreAuthorize can be difficult to debug; test thoroughly
- **Performance impact**: Method security adds overhead; consider security at layer boundaries

## Examples

### Input: Service Without Security Testing

```java
@Service
public class AdminService {
    public void deleteUser(Long userId) {
        // Delete logic without security check
    }
}
```

### Output: Service With Security Test Coverage

```java
@Service
public class AdminService {
    @PreAuthorize("hasRole('ADMIN')")
    public void deleteUser(Long userId) {
        // Delete logic
    }
}

// Test
@Test
@WithMockUser(roles = "ADMIN")
void shouldAllowAdminToDeleteUser() {
    assertThatCode(() -> adminService.deleteUser(1L))
        .doesNotThrowAnyException();
}

@Test
@WithMockUser(roles = "USER")
void shouldDenyUserFromDeletingUser() {
    assertThatThrownBy(() -> adminService.deleteUser(1L))
        .isInstanceOf(AccessDeniedException.class);
}
```

### Input: Manual Security Check (Anti-Pattern)

```java
if (user.hasRole("ADMIN")) {
    service.deleteUser(userId);
}
```

### Output: Declarative Security with Testing

```java
@PreAuthorize("hasRole('ADMIN')")
public void deleteUser(Long userId) {
    // Business logic only, security is declarative
}

// Test verifies security enforcement
@Test
@WithMockUser(roles = "ADMIN")
void shouldExecuteDelete() {
    service.deleteUser(1L);
    verify(repository).deleteById(1L);
}
```

## Constraints and Warnings

**AccessDeniedException not thrown**: Ensure `@EnableGlobalMethodSecurity(prePostEnabled = true)` is configured.

**@WithMockUser not working**: Verify Spring Security test dependencies are on classpath.

**Custom PermissionEvaluator not invoked**: Check `@EnableGlobalMethodSecurity(securedEnabled = true, prePostEnabled = true)`.

## References

- [Spring Security Method Security](https://docs.spring.io/spring-security/site/docs/current/reference/html5/#jc-method)
- [Spring Security Testing](https://docs.spring.io/spring-security/site/docs/current/reference/html5/#test)
- [@WithMockUser Documentation](https://docs.spring.io/spring-security/site/docs/current/api/org/springframework/security/test/context/support/WithMockUser.html)
