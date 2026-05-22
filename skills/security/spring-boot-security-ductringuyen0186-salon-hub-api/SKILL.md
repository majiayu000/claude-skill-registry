---
name: spring-boot-security
description: Guide for implementing Spring Security with JWT authentication and role-based access control. Use this when adding security to endpoints or implementing authentication features.
---

# Spring Security Best Practices

Follow these practices for securing Spring Boot applications.

## Security Configuration

```java
@Configuration
@EnableWebSecurity
@EnableMethodSecurity(prePostEnabled = true)
public class SecurityConfiguration {

    private final JwtAuthenticationFilter jwtAuthFilter;

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        return http
            .csrf(csrf -> csrf.disable())  // Disable for stateless REST APIs
            .sessionManagement(session -> 
                session.sessionCreationPolicy(SessionCreationPolicy.STATELESS)
            )
            .authorizeHttpRequests(authz -> authz
                // Public endpoints
                .requestMatchers("/api/auth/**").permitAll()
                .requestMatchers("/api/checkin").permitAll()
                .requestMatchers("/actuator/health").permitAll()
                .requestMatchers("/v3/api-docs/**", "/swagger-ui/**").permitAll()
                // All other requests require authentication
                .anyRequest().authenticated()
            )
            .addFilterBefore(jwtAuthFilter, UsernamePasswordAuthenticationFilter.class)
            .build();
    }
}
```

## Role-Based Access Control

### Role Hierarchy

```
ADMIN > MANAGER > FRONT_DESK > TECHNICIAN
```

### Method-Level Security

```java
// Admin only
@PreAuthorize("hasRole('ADMIN')")
@DeleteMapping("/users/{id}")
public ResponseEntity<Void> deleteUser(@PathVariable Long id) { }

// Manager and above
@PreAuthorize("hasRole('MANAGER')")
@PostMapping("/employees")
public EmployeeDTO createEmployee(@RequestBody EmployeeRequest request) { }

// Front desk and above
@PreAuthorize("hasRole('FRONT_DESK')")
@PostMapping("/appointments")
public AppointmentDTO createAppointment(@RequestBody AppointmentRequest request) { }

// All authenticated users
@PreAuthorize("hasRole('TECHNICIAN')")
@GetMapping("/appointments")
public List<AppointmentDTO> getAppointments() { }

// Self-access patterns
@PreAuthorize("hasRole('ADMIN') or #id == authentication.principal.employeeId")
@GetMapping("/employees/{id}")
public EmployeeDTO getEmployee(@PathVariable Long id) { }
```

## Input Validation

**Always validate user input to prevent injection attacks:**

```java
public class UserRequest {
    @NotBlank
    @Size(min = 3, max = 50)
    private String username;

    @NotBlank
    @Email
    private String email;

    @NotBlank
    @Pattern(regexp = "^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z]).{8,}$",
             message = "Password must contain at least 8 characters, one digit, one lowercase and one uppercase letter")
    private String password;
}

@PostMapping("/register")
public ResponseEntity<UserDTO> register(@Valid @RequestBody UserRequest request) {
    // Process validated input
}
```

## Password Security

```java
@Configuration
public class SecurityConfig {
    
    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }
}

@Service
public class AuthService {
    private final PasswordEncoder passwordEncoder;
    
    public void registerUser(UserRequest request) {
        User user = new User();
        user.setPassword(passwordEncoder.encode(request.getPassword()));
        // Never store plain text passwords
    }
}
```

## JWT Token Handling

```java
@Component
public class JwtTokenProvider {
    
    @Value("${jwt.secret}")
    private String jwtSecret;
    
    @Value("${jwt.expiration}")
    private long jwtExpiration;
    
    public String generateToken(UserDetails userDetails) {
        return Jwts.builder()
            .setSubject(userDetails.getUsername())
            .claim("roles", userDetails.getAuthorities())
            .setIssuedAt(new Date())
            .setExpiration(new Date(System.currentTimeMillis() + jwtExpiration))
            .signWith(getSigningKey(), SignatureAlgorithm.HS256)
            .compact();
    }
    
    public boolean validateToken(String token) {
        try {
            Jwts.parserBuilder()
                .setSigningKey(getSigningKey())
                .build()
                .parseClaimsJws(token);
            return true;
        } catch (JwtException | IllegalArgumentException e) {
            return false;
        }
    }
}
```

## Security Headers

```java
@Bean
public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
    http
        .headers(headers -> headers
            .contentSecurityPolicy(csp -> csp.policyDirectives("default-src 'self'"))
            .frameOptions(frame -> frame.deny())
            .xssProtection(xss -> xss.block(true))
            .httpStrictTransportSecurity(hsts -> hsts
                .includeSubDomains(true)
                .maxAgeInSeconds(31536000)
            )
        );
    return http.build();
}
```

## Security Testing

```java
@WebMvcTest(controllers = UserController.class)
@Import(TestSecurityConfig.class)
class UserControllerSecurityTest {

    @Test
    void endpoint_withoutAuth_shouldReturn403() throws Exception {
        mockMvc.perform(get("/api/users/1"))
            .andExpect(status().isForbidden());
    }

    @Test
    @WithMockUser(roles = {"TECHNICIAN"})
    void endpoint_withInsufficientRole_shouldReturn403() throws Exception {
        mockMvc.perform(delete("/api/users/1"))
            .andExpect(status().isForbidden());
    }

    @Test
    @WithMockUser(roles = {"ADMIN"})
    void endpoint_withAdminRole_shouldReturn200() throws Exception {
        when(userService.findById(1L)).thenReturn(mockUser);
        
        mockMvc.perform(get("/api/users/1"))
            .andExpect(status().isOk());
    }
}
```

## Common Security Pitfalls to Avoid

1. **Never log passwords or tokens**
2. **Never return sensitive data in error messages**
3. **Always use parameterized queries (JPA does this by default)**
4. **Never disable CSRF without stateless authentication**
5. **Always validate and sanitize user input**
6. **Use HTTPS in production**
7. **Implement rate limiting for authentication endpoints**

## Security Checklist for New Endpoints

- [ ] Add appropriate `@PreAuthorize` annotation
- [ ] Validate all input with `@Valid`
- [ ] Write security tests (unauthenticated, wrong role, correct role)
- [ ] Ensure no sensitive data in logs or responses
- [ ] Document security requirements in API docs
