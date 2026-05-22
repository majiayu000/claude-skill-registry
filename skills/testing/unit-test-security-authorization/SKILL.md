---
name: unit-test-security-authorization
description: Unit tests for Spring Security with @PreAuthorize, @Secured, @RolesAllowed. Test role-based access control and authorization policies. Use when validating security configurations and access control logic.
category: testing
tags: [junit-5, spring-security, authorization, roles, preauthorize, mockmvc]
version: 1.0.1
---

# Unit Testing Security and Authorization

Test Spring Security authorization logic using @PreAuthorize, @Secured, and custom permission evaluators. Verify access control decisions without full security infrastructure.

## When to Use This Skill

Use this skill when:
- Testing @PreAuthorize and @Secured method-level security
- Testing role-based access control (RBAC)
- Testing custom permission evaluators
- Verifying access denied scenarios
- Testing authorization with authenticated principals
- Want fast authorization tests without full Spring Security context

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

## Troubleshooting

**AccessDeniedException not thrown**: Ensure `@EnableGlobalMethodSecurity(prePostEnabled = true)` is configured.

**@WithMockUser not working**: Verify Spring Security test dependencies are on classpath.

**Custom PermissionEvaluator not invoked**: Check `@EnableGlobalMethodSecurity(securedEnabled = true, prePostEnabled = true)`.

## References

- [Spring Security Method Security](https://docs.spring.io/spring-security/site/docs/current/reference/html5/#jc-method)
- [Spring Security Testing](https://docs.spring.io/spring-security/site/docs/current/reference/html5/#test)
- [@WithMockUser Documentation](https://docs.spring.io/spring-security/site/docs/current/api/org/springframework/security/test/context/support/WithMockUser.html)
