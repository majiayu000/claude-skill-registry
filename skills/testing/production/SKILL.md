---
name: production
description: Unit testing, performance optimization, security implementation, Play Store deployment.
version: "2.0.0"
sasmp_version: "1.3.0"

# Agent Binding
bonded_agent: 07-production
bond_type: PRIMARY_BOND

# Skill Configuration
atomic: true
single_responsibility: Production quality & deployment

# Parameter Validation
parameters:
  concern:
    type: string
    enum: [testing, performance, security, deployment]
    required: false
  urgency:
    type: string
    enum: [low, medium, high, critical]
    default: medium

# Retry Configuration
retry:
  max_attempts: 3
  backoff: exponential
  on_failure: escalate_to_human

# Observability
logging:
  level: warn
  include: [concern_type, security_level, test_coverage]
---

# Production Quality Skill

## Quick Start

### Unit Testing
```kotlin
@Test
fun loadUser_updates_state() = runTest {
    val user = User(1, "John")
    val mockRepo = mockk<UserRepository>()
    coEvery { mockRepo.getUser(1) } returns user
    
    val viewModel = UserViewModel(mockRepo)
    viewModel.loadUser(1)
    
    assertEquals(user, viewModel.state.value)
}
```

### Security
```kotlin
// Encrypted storage
val prefs = EncryptedSharedPreferences.create(context, "secret",
    MasterKey.Builder(context).build(), AES256_SIV, AES256_GCM)

// SSL pinning
CertificatePinner.Builder()
    .add("api.example.com", "sha256/...").build()
```

### Play Store Deployment
```bash
./gradlew bundleRelease
# Upload to Google Play Console
# Monitor crashes and ratings
```

## Key Concepts

### Testing
- Unit tests (70-80% coverage)
- Integration tests
- UI tests with Espresso
- Mock external dependencies

### Performance
- ANR prevention
- Memory leak detection
- 60 FPS target
- Battery optimization

### Security
- Data encryption
- HTTPS/SSL pinning
- Permission handling
- OWASP Top 10

### Deployment
- Internal → Closed → Open → Production
- Staged rollout strategy
- Crash analytics monitoring
- User rating management

## Best Practices

✅ Write comprehensive tests
✅ Profile regularly
✅ Implement security features
✅ Monitor production apps
✅ Use staged rollouts

## Resources

- [Testing Guide](https://developer.android.com/training/testing)
- [Security & Privacy](https://developer.android.com/privacy-and-security)
- [Play Console Help](https://support.google.com/googleplay)
