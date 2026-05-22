---
name: spring-boot-security-jwt
description: JWT authentication and authorization patterns for Spring Boot 3.5.x covering token generation with JJWT, Bearer/cookie authentication, database/OAuth2 integration, and RBAC/permission-based access control using Spring Security 6.x.
allowed-tools: Read, Write, Bash
category: backend
tags: [spring-boot, spring-security, jwt, authentication, authorization, rbac, oauth2, jjwt]
version: 1.0.0
---

# Spring Boot JWT Security

Comprehensive JWT (JSON Web Token) authentication and authorization patterns for Spring Boot 3.5.x applications using Spring Security 6.x and the JJWT library. This skill provides production-ready implementations for stateless authentication, role-based access control, and integration with modern authentication providers.

## Overview

JWT authentication enables stateless, scalable security for Spring Boot applications. This skill covers complete JWT lifecycle management including token generation, validation, refresh strategies, and integration patterns with database-backed and OAuth2 authentication providers. Implementations follow Spring Security 6.x best practices with modern SecurityFilterChain configuration.

## When to Use

Use this skill when:
- Implementing stateless authentication for REST APIs
- Building SPA (Single Page Application) backends with JWT
- Securing microservices with token-based authentication
- Integrating with OAuth2 providers (Google, GitHub, etc.)
- Implementing role-based or permission-based access control
- Setting up JWT refresh token strategies
- Migrating from session-based to token-based authentication
- Building mobile API backends
- Implementing cross-origin authentication with CORS

## Prerequisites

- Java 17+ (for records and pattern matching)
- Spring Boot 3.5.x (for Spring Security 6.x integration)
- JJWT library (io.jsonwebtoken) for JWT operations
- Maven or Gradle build system
- Basic understanding of Spring Security concepts

## Dependencies

### Maven

```xml
<dependencies>
    <!-- Spring Security -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-security</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-data-jpa</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-validation</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-oauth2-resource-server</artifactId>
    </dependency>

    <!-- JWT Library -->
    <dependency>
        <groupId>io.jsonwebtoken</groupId>
        <artifactId>jjwt-api</artifactId>
        <version>0.12.6</version>
    </dependency>
    <dependency>
        <groupId>io.jsonwebtoken</groupId>
        <artifactId>jjwt-impl</artifactId>
        <version>0.12.6</version>
        <scope>runtime</scope>
    </dependency>
    <dependency>
        <groupId>io.jsonwebtoken</groupId>
        <artifactId>jjwt-jackson</artifactId>
        <version>0.12.6</version>
        <scope>runtime</scope>
    </dependency>

    <!-- Database -->
    <dependency>
        <groupId>com.h2database</groupId>
        <artifactId>h2</artifactId>
        <scope>runtime</scope>
    </dependency>
    <dependency>
        <groupId>org.postgresql</groupId>
        <artifactId>postgresql</artifactId>
        <scope>runtime</scope>
    </dependency>

    <!-- Testing -->
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
    <dependency>
        <groupId>org.testcontainers</groupId>
        <artifactId>junit-jupiter</artifactId>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.springframework.security</groupId>
        <artifactId>spring-security-test</artifactId>
        <scope>test</scope>
    </dependency>
</dependencies>
```

### Gradle

```kotlin
dependencies {
    // Spring Security
    implementation("org.springframework.boot:spring-boot-starter-security")
    implementation("org.springframework.boot:spring-boot-starter-web")
    implementation("org.springframework.boot:spring-boot-starter-data-jpa")
    implementation("org.springframework.boot:spring-boot-starter-validation")
    implementation("org.springframework.boot:spring-boot-starter-oauth2-resource-server")

    // JWT Library
    implementation("io.jsonwebtoken:jjwt-api:0.12.6")
    implementation("io.jsonwebtoken:jjwt-impl:0.12.6")
    implementation("io.jsonwebtoken:jjwt-jackson:0.12.6")

    // Database
    runtimeOnly("com.h2database:h2")
    runtimeOnly("org.postgresql:postgresql")

    // Testing
    testImplementation("org.springframework.boot:spring-boot-starter-test")
    testImplementation("org.springframework.security:spring-security-test")
    testImplementation("org.testcontainers:junit-jupiter")
}
```

## Quick Start

### 1. Application Configuration

```yaml
# application.yml
spring:
  security:
    oauth2:
      client:
        registration:
          google:
            client-id: ${GOOGLE_CLIENT_ID}
            client-secret: ${GOOGLE_CLIENT_SECRET}
            scope: openid, profile, email

jwt:
  secret: ${JWT_SECRET:my-very-secret-key-that-is-at-least-256-bits-long}
  access-token-expiration: 86400000    # 24 hours in milliseconds
  refresh-token-expiration: 604800000 # 7 days in milliseconds
  issuer: spring-boot-jwt-example
  cookie-name: jwt-token
  cookie-secure: false                 # Set to true in production with HTTPS
  cookie-http-only: true
  cookie-same-site: lax
```

### 2. Modern Spring Security 6.x Configuration

```java
@Configuration
@EnableWebSecurity
@EnableMethodSecurity
@RequiredArgsConstructor
public class SecurityConfig {

    private final JwtAuthenticationFilter jwtAuthFilter;
    private final AuthenticationProvider authenticationProvider;
    private final LogoutHandler logoutHandler;

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
            .csrf(csrf -> csrf.disable())
            .cors(cors -> cors.configurationSource(corsConfigurationSource()))
            .sessionManagement(session -> session.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .authorizeHttpRequests(authz -> authz
                .requestMatchers("/api/auth/**").permitAll()
                .requestMatchers("/api/public/**").permitAll()
                .requestMatchers(HttpMethod.GET, "/api-docs/**").permitAll()
                .requestMatchers(HttpMethod.GET, "/swagger-ui/**").permitAll()
                .anyRequest().authenticated()
            )
            .authenticationProvider(authenticationProvider)
            .addFilterBefore(jwtAuthFilter, UsernamePasswordAuthenticationFilter.class)
            .logout(logout -> logout
                .logoutUrl("/api/auth/logout")
                .addLogoutHandler(logoutHandler)
                .logoutSuccessHandler((request, response, authentication) ->
                    SecurityContextHolder.clearContext())
            );

        return http.build();
    }

    @Bean
    public CorsConfigurationSource corsConfigurationSource() {
        CorsConfiguration configuration = new CorsConfiguration();
        configuration.setAllowedOriginPatterns(List.of("*"));
        configuration.setAllowedMethods(List.of("GET", "POST", "PUT", "DELETE", "OPTIONS"));
        configuration.setAllowedHeaders(List.of("*"));
        configuration.setAllowCredentials(true);

        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", configuration);
        return source;
    }
}
```

### 3. JWT Service Implementation

```java
@Service
@RequiredArgsConstructor
@Slf4j
public class JwtService {

    @Value("${jwt.secret}")
    private String secret;

    @Value("${jwt.access-token-expiration}")
    private long accessTokenExpiration;

    @Value("${jwt.refresh-token-expiration}")
    private long refreshTokenExpiration;

    @Value("${jwt.issuer}")
    private String issuer;

    private final RefreshTokenService refreshTokenService;

    /**
     * Generate access token for user
     */
    public String generateAccessToken(UserDetails userDetails) {
        return generateToken(userDetails, accessTokenExpiration);
    }

    /**
     * Generate refresh token for user
     */
    public String generateRefreshToken(UserDetails userDetails) {
        return refreshTokenService.createRefreshToken(userDetails.getUsername());
    }

    /**
     * Extract username from JWT token
     */
    public String extractUsername(String token) {
        return extractClaims(token).getSubject();
    }

    /**
     * Extract claims from JWT token
     */
    private Claims extractClaims(String token) {
        return Jwts.parser()
                .verifyWith(getSigningKey())
                .build()
                .parseSignedClaims(token)
                .getPayload();
    }

    /**
     * Validate JWT token
     */
    public boolean isTokenValid(String token, UserDetails userDetails) {
        try {
            final String username = extractUsername(token);
            return (username.equals(userDetails.getUsername()) &&
                    !isTokenExpired(token) &&
                    extractClaims(token).getIssuer().equals(issuer));
        } catch (JwtException | IllegalArgumentException e) {
            log.debug("Invalid JWT token: {}", e.getMessage());
            return false;
        }
    }

    /**
     * Check if token is expired
     */
    private boolean isTokenExpired(String token) {
        return extractClaims(token).getExpiration().before(new Date());
    }

    /**
     * Generate token with expiration
     */
    private String generateToken(UserDetails userDetails, long expiration) {
        Date now = new Date();
        Date expiryDate = new Date(now.getTime() + expiration);

        return Jwts.builder()
                .setSubject(userDetails.getUsername())
                .setIssuer(issuer)
                .setIssuedAt(now)
                .setExpiration(expiryDate)
                .claim("authorities", getAuthorities(userDetails))
                .claim("type", "access")
                .signWith(getSigningKey())
                .compact();
    }

    /**
     * Get signing key from secret
     */
    private SecretKey getSigningKey() {
        byte[] keyBytes = secret.getBytes(StandardCharsets.UTF_8);
        return Keys.hmacShaKeyFor(keyBytes);
    }

    /**
     * Extract authorities from user details
     */
    private List<String> getAuthorities(UserDetails userDetails) {
        return userDetails.getAuthorities().stream()
                .map(GrantedAuthority::getAuthority)
                .collect(Collectors.toList());
    }
}
```

### 3. JWT Authentication Filter

```java
@Component
@RequiredArgsConstructor
public class JwtAuthenticationFilter extends OncePerRequestFilter {

    private final JwtService jwtService;
    private final UserDetailsService userDetailsService;

    @Override
    protected void doFilterInternal(
            @NonNull HttpServletRequest request,
            @NonNull HttpServletResponse response,
            @NonNull FilterChain filterChain) throws ServletException, IOException {

        final String authHeader = request.getHeader("Authorization");
        final String jwt;
        final String userEmail;

        // Check for Bearer token
        if (authHeader == null || !authHeader.startsWith("Bearer ")) {
            // Check for JWT cookie
            String jwtCookie = WebUtils.getCookie(request, "jwt-token") != null
                ? WebUtils.getCookie(request, "jwt-token").getValue()
                : null;

            if (jwtCookie != null) {
                jwt = jwtCookie;
                userEmail = jwtService.extractUsername(jwt);

                if (userEmail != null && SecurityContextHolder.getContext().getAuthentication() == null) {
                    UserDetails userDetails = userDetailsService.loadUserByUsername(userEmail);

                    if (jwtService.isTokenValid(jwt, userDetails)) {
                        UsernamePasswordAuthenticationToken authToken =
                            new UsernamePasswordAuthenticationToken(
                                userDetails,
                                null,
                                userDetails.getAuthorities()
                            );
                        authToken.setDetails(
                            new WebAuthenticationDetailsSource().buildDetails(request)
                        );
                        SecurityContextHolder.getContext().setAuthentication(authToken);
                    }
                }
            }

            filterChain.doFilter(request, response);
            return;
        }

        jwt = authHeader.substring(7);
        userEmail = jwtService.extractUsername(jwt);

        if (userEmail != null && SecurityContextHolder.getContext().getAuthentication() == null) {
            UserDetails userDetails = userDetailsService.loadUserByUsername(userEmail);

            if (jwtService.isTokenValid(jwt, userDetails)) {
                UsernamePasswordAuthenticationToken authToken =
                    new UsernamePasswordAuthenticationToken(
                        userDetails,
                        null,
                        userDetails.getAuthorities()
                    );
                authToken.setDetails(
                    new WebAuthenticationDetailsSource().buildDetails(request)
                );
                SecurityContextHolder.getContext().setAuthentication(authToken);
            }
        }

        filterChain.doFilter(request, response);
    }
}
```

### 4. Security Configuration

```java
@Configuration
@EnableWebSecurity
@RequiredArgsConstructor
@EnableMethodSecurity(prePostEnabled = true)
public class SecurityConfig {

    private final JwtAuthenticationFilter jwtAuthFilter;
    private final AuthenticationProvider authenticationProvider;
    private final LogoutHandler logoutHandler;

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
            .csrf(AbstractHttpConfigurer::disable)
            .authorizeHttpRequests(auth -> auth
                // Public endpoints
                .requestMatchers("/api/v1/auth/**").permitAll()
                .requestMatchers("/api/v1/oauth2/**").permitAll()
                .requestMatchers("/swagger-ui/**", "/v3/api-docs/**").permitAll()
                .requestMatchers("/health").permitAll()

                // Admin endpoints
                .requestMatchers("/api/v1/admin/**").hasRole("ADMIN")

                // Protected endpoints
                .anyRequest().authenticated()
            )
            .sessionManagement(sess -> sess
                .sessionCreationPolicy(SessionCreationPolicy.STATELESS)
            )
            .authenticationProvider(authenticationProvider)
            .addFilterBefore(jwtAuthFilter, UsernamePasswordAuthenticationFilter.class)
            .oauth2Login(oauth2 -> oauth2
                .loginPage("/oauth2/authorization/google")
                .defaultSuccessUrl("/api/v1/auth/oauth2/success", true)
                .failureUrl("/api/v1/auth/oauth2/failure")
            )
            .logout(logout -> logout
                .logoutUrl("/api/v1/auth/logout")
                .addLogoutHandler(logoutHandler)
                .logoutSuccessHandler((request, response, authentication) ->
                    SecurityContextHolder.clearContext())
            );

        return http.build();
    }

    @Bean
    public AuthenticationProvider authenticationProvider(UserDetailsService userDetailsService, PasswordEncoder passwordEncoder) {
        DaoAuthenticationProvider authProvider = new DaoAuthenticationProvider();
        authProvider.setUserDetailsService(userDetailsService);
        authProvider.setPasswordEncoder(passwordEncoder);
        return authProvider;
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }

    @Bean
    public AuthenticationManager authenticationManager(AuthenticationConfiguration config) throws Exception {
        return config.getAuthenticationManager();
    }
}
```

## Authentication Controllers

```java
@RestController
@RequestMapping("/api/v1/auth")
@RequiredArgsConstructor
@Slf4j
public class AuthenticationController {

    private final AuthenticationService authenticationService;

    @PostMapping("/register")
    public ResponseEntity<AuthenticationResponse> register(
            @Valid @RequestBody RegisterRequest request) {
        log.info("Registering new user: {}", request.getEmail());
        return ResponseEntity.ok(authenticationService.register(request));
    }

    @PostMapping("/authenticate")
    public ResponseEntity<AuthenticationResponse> authenticate(
            @Valid @RequestBody AuthenticationRequest request) {
        log.info("Authenticating user: {}", request.getEmail());
        AuthenticationResponse response = authenticationService.authenticate(request);

        return ResponseEntity.ok()
                .header("Set-Cookie", createJwtCookie(response.getAccessToken()))
                .body(response);
    }

    @PostMapping("/refresh")
    public ResponseEntity<AuthenticationResponse> refreshToken(
            @RequestBody RefreshTokenRequest request) {
        log.info("Refreshing token for user");
        return ResponseEntity.ok(authenticationService.refreshToken(request));
    }

    @GetMapping("/me")
    public ResponseEntity<UserProfile> getCurrentUser() {
        return ResponseEntity.ok(authenticationService.getCurrentUser());
    }

    private String createJwtCookie(String token) {
        return String.format(
            "jwt-token=%s; Path=/; HttpOnly; SameSite=Lax; Max-Age=%d",
            token,
            86400 // 24 hours
        );
    }
}
```

## Authorization Patterns

### Role-Based Access Control (RBAC)

```java
@RestController
@RequestMapping("/api/v1/admin")
@RequiredArgsConstructor
@PreAuthorize("hasRole('ADMIN')")
public class AdminController {

    private final AdminService adminService;

    @GetMapping("/users")
    @PreAuthorize("hasAuthority('ADMIN_READ')")
    public ResponseEntity<Page<UserResponse>> getAllUsers(Pageable pageable) {
        return ResponseEntity.ok(adminService.getAllUsers(pageable));
    }

    @DeleteMapping("/users/{id}")
    @PreAuthorize("hasAuthority('ADMIN_DELETE')")
    public ResponseEntity<Void> deleteUser(@PathVariable Long id) {
        adminService.deleteUser(id);
        return ResponseEntity.noContent().build();
    }

    @PostMapping("/users/{id}/roles")
    @PreAuthorize("hasAuthority('ADMIN_MANAGE_ROLES')")
    public ResponseEntity<UserResponse> assignRole(
            @PathVariable Long id,
            @Valid @RequestBody AssignRoleRequest request) {
        return ResponseEntity.ok(adminService.assignRole(id, request));
    }
}
```

### Permission-Based Access Control

```java
@Service
@RequiredArgsConstructor
public class DocumentService {

    @PreAuthorize("hasPermission(#documentId, 'Document', 'READ')")
    public Document getDocument(Long documentId) {
        return documentRepository.findById(documentId)
                .orElseThrow(() -> new DocumentNotFoundException(documentId));
    }

    @PreAuthorize("hasPermission(#documentId, 'Document', 'WRITE') or hasRole('ADMIN')")
    public Document updateDocument(Long documentId, UpdateDocumentRequest request) {
        Document document = getDocument(documentId);
        document.setContent(request.content());
        return documentRepository.save(document);
    }

    @PreAuthorize("@documentSecurityService.canAccess(#userEmail, #documentId)")
    public Document shareDocument(String userEmail, Long documentId) {
        // Implementation
    }
}
```

### Custom Permission Evaluator

```java
@Component
@RequiredArgsConstructor
public class DocumentPermissionEvaluator implements PermissionEvaluator {

    private final DocumentRepository documentRepository;

    @Override
    public boolean hasPermission(
            Authentication authentication,
            Object targetDomainObject,
            Object permission) {

        if (authentication == null || !(targetDomainObject instanceof Document)) {
            return false;
        }

        Document document = (Document) targetDomainObject;
        String username = authentication.getName();
        String requiredPermission = (String) permission;

        // Admin can do anything
        if (hasRole(authentication, "ADMIN")) {
            return true;
        }

        // Owner can read and write
        if (document.getOwner().getUsername().equals(username)) {
            return "READ".equals(requiredPermission) || "WRITE".equals(requiredPermission);
        }

        // Check shared permissions
        return document.getSharedWith().stream()
                .anyMatch(share -> share.getUser().getUsername().equals(username)
                        && share.getPermission().name().equals(requiredPermission));
    }

    @Override
    public boolean hasPermission(
            Authentication authentication,
            Serializable targetId,
            String targetType,
            Object permission) {

        if (!"Document".equals(targetType)) {
            return false;
        }

        Document document = documentRepository.findById((Long) targetId).orElse(null);
        return document != null && hasPermission(authentication, document, permission);
    }

    private boolean hasRole(Authentication authentication, String role) {
        return authentication.getAuthorities().stream()
                .anyMatch(auth -> auth.getAuthority().equals("ROLE_" + role));
    }
}
```

## Database Entities

```java
@Entity
@Table(name = "users")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(unique = true, nullable = false)
    private String username;

    @Column(unique = true, nullable = false)
    private String email;

    @Column(nullable = false)
    private String password;

    @Builder.Default
    @Enumerated(EnumType.STRING)
    private Role role = Role.USER;

    @Builder.Default
    private boolean enabled = true;

    @Builder.Default
    private boolean accountNonExpired = true;

    @Builder.Default
    private boolean accountNonLocked = true;

    @Builder.Default
    private boolean credentialsNonExpired = true;

    @OneToMany(mappedBy = "user", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private Set<RefreshToken> refreshTokens = new HashSet<>();

    @CreationTimestamp
    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;
}

@Entity
@Table(name = "refresh_tokens")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class RefreshToken {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String token;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    @Builder.Default
    private boolean revoked = false;

    @Builder.Default
    private boolean expired = false;

    @Column(name = "expiry_date")
    private LocalDateTime expiryDate;

    @CreationTimestamp
    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;
}
```

## Testing JWT Security

```java
@SpringBootTest
@AutoConfigureMockMvc
@TestPropertySource(properties = {
    "jwt.secret=test-secret-key-for-testing-only",
    "jwt.access-token-expiration=3600000"
})
class AuthenticationControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @Autowired
    private JwtService jwtService;

    @Test
    void shouldAuthenticateUser() throws Exception {
        AuthenticationRequest request = AuthenticationRequest.builder()
                .email("test@example.com")
                .password("password123")
                .build();

        mockMvc.perform(post("/api/v1/auth/authenticate")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.accessToken").exists())
                .andExpect(jsonPath("$.refreshToken").exists())
                .andExpect(jsonPath("$.user.email").value("test@example.com"));
    }

    @Test
    void shouldDenyAccessWithoutToken() throws Exception {
        mockMvc.perform(get("/api/v1/admin/users"))
                .andExpect(status().isUnauthorized());
    }

    @Test
    @WithMockUser(roles = "ADMIN")
    void shouldAllowAdminAccess() throws Exception {
        mockMvc.perform(get("/api/v1/admin/users"))
                .andExpect(status().isOk());
    }

    @Test
    void shouldValidateJwtToken() throws Exception {
        UserDetails userDetails = User.withUsername("test@example.com")
                .password("password")
                .roles("USER")
                .build();

        String token = jwtService.generateAccessToken(userDetails);

        mockMvc.perform(get("/api/v1/auth/me")
                .header("Authorization", "Bearer " + token))
                .andExpect(status().isOk());
    }
}
```

## Best Practices

### 1. Modern JWT Patterns

#### Key Rotation Strategy
```java
@Component
@RequiredArgsConstructor
public class JwtKeyRotationService {

    private final SecretKeyRepository keyRepository;
    private final CacheManager cacheManager;

    @Scheduled(cron = "0 0 0 * * ?") // Daily at midnight
    public void rotateKeys() {
        SecretKey newKey = Keys.secretKeyFor(SignatureAlgorithm.HS256);
        keyRepository.save(new SecretKeyEntity(newKey, LocalDateTime.now()));
        cacheManager.getCache("jwt-keys").clear();
    }
}
```

#### Token Blacklisting
```java
@Service
@RequiredArgsConstructor
public class TokenBlacklistService {

    private final RedisTemplate<string, string> redisTemplate;
    private static final String BLACKLIST_PREFIX = "blacklist:jwt:";

    public void blacklistToken(String token, long expirationTime) {
        String tokenId = extractTokenId(token);
        redisTemplate.opsForValue().set(
            BLACKLIST_PREFIX + tokenId,
            "1",
            expirationTime,
            TimeUnit.MILLISECONDS
        );
    }

    public boolean isBlacklisted(String token) {
        String tokenId = extractTokenId(token);
        return Boolean.TRUE.equals(redisTemplate.hasKey(BLACKLIST_PREFIX + tokenId));
    }
}
```

### 2. Security Configuration

- **Always use HTTPS** in production for JWT token transmission
- **Set appropriate cookie flags**: `HttpOnly`, `Secure`, `SameSite`
- **Use strong secret keys**: minimum 256 bits for HMAC algorithms
- **Implement token expiration**: Don't use tokens with infinite lifetime
- **Validate all inputs**: Never trust JWT claims without validation
- **Implement key rotation**: Regularly rotate signing keys
- **Use token blacklisting**: For logout and security incidents

### 2. Token Management

```java
// Implement refresh token rotation
public class RefreshTokenService {

    @Transactional
    public String rotateRefreshToken(String oldToken) {
        RefreshToken refreshToken = refreshTokenRepository.findByToken(oldToken)
                .orElseThrow(() -> new RefreshTokenException("Invalid refresh token"));

        // Revoke old token
        refreshToken.setRevoked(true);
        refreshTokenRepository.save(refreshToken);

        // Generate new token
        return createRefreshToken(refreshToken.getUser().getUsername());
    }
}
```

### 3. Performance Optimization

```java
// Cache user details to avoid database hits
@Service
@RequiredArgsConstructor
public class CachedUserDetailsService implements UserDetailsService {

    private final UserRepository userRepository;
    private final CacheManager cacheManager;

    @Override
    @Cacheable(value = "users", key = "#username")
    public UserDetails loadUserByUsername(String username) {
        User user = userRepository.findByEmail(username)
                .orElseThrow(() -> new UsernameNotFoundException(username));
        return new CustomUserDetails(user);
    }
}
```

### 4. Monitoring and Audit

```java
@Component
@RequiredArgsConstructor
@Slf4j
public class SecurityAuditService {

    @EventListener
    public void handleAuthenticationSuccess(AuthenticationSuccessEvent event) {
        log.info("Authentication success for user: {}", event.getAuthentication().getName());
        // Store audit event
    }

    @EventListener
    public void handleAuthenticationFailure(AuthenticationFailureEvent event) {
        log.warn("Authentication failure for user: {}", event.getAuthentication().getName());
        // Store security event
    }

    @EventListener
    public void handleAuthorizationFailure(AuthorizationFailureEvent event) {
        log.warn("Authorization denied for user: {} on resource: {}",
                event.getAuthentication().getName(),
                event.getConfigAttributes());
    }
}
```

## Constraints

### 1. Token Size Limitations
- JWT tokens should stay under HTTP header size limits (typically 8KB)
- Avoid storing large amounts of data in JWT claims
- Use references instead of embedding complete objects

### 2. Security Considerations
- Never store sensitive information in JWT tokens
- Implement proper token revocation strategies
- Use different keys for different environments (dev, staging, prod)
- Regularly rotate signing keys

### 3. Rate Limiting
```java
@RestController
@RequestMapping("/api/v1/auth")
@RequiredArgsConstructor
public class AuthenticationController {

    @PostMapping("/authenticate")
    @RateLimiter(name = "auth", fallbackMethod = "authenticateFallback")
    public ResponseEntity<AuthenticationResponse> authenticate(@RequestBody AuthenticationRequest request) {
        // Implementation
    }

    public ResponseEntity<AuthenticationResponse> authenticateFallback(
            AuthenticationRequest request,
            CallNotPermittedException exception) {
        return ResponseEntity.status(HttpStatus.TOO_MANY_REQUESTS).build();
    }
}
```

### 4. CORS Configuration
```java
@Configuration
public class CorsConfig {

    @Bean
    public CorsConfigurationSource corsConfigurationSource() {
        CorsConfiguration configuration = new CorsConfiguration();
        configuration.setAllowedOriginPatterns(List.of("*"));
        configuration.setAllowedMethods(List.of("GET", "POST", "PUT", "DELETE", "OPTIONS"));
        configuration.setAllowedHeaders(List.of("*"));
        configuration.setAllowCredentials(true);

        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", configuration);
        return source;
    }
}
```

## Reference Materials

- [Complete JWT Configuration Guide](references/jwt-complete-configuration.md) - Consolidated configuration patterns for Spring Security 6.x
- [JWT Testing Guide](references/jwt-testing-guide.md) - Comprehensive testing strategies
- [JWT Quick Reference](references/jwt-quick-reference.md) - Common patterns and quick examples
- [Complete implementation examples](references/examples.md)
- [Security hardening checklist](references/security-hardening.md)
- [Migration guide for Spring Security 6.x](references/migration-spring-security-6x.md)

## Related Skills

- `spring-boot-dependency-injection` - Constructor injection patterns used throughout
- `spring-boot-rest-api-standards` - REST API security patterns and error handling
- `unit-test-security-authorization` - Testing Spring Security configurations
- `spring-data-jpa` - User entity and repository patterns
- `spring-boot-actuator` - Security monitoring and health endpoints