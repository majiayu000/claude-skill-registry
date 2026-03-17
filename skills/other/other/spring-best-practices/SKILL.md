---
name: spring-best-practices
description: Spring Boot and Java best practices for PastCare. Use when writing or reviewing backend code.
user-invocable: false
---

# Spring Boot Best Practices for PastCare

## Multi-Tenant Security (CRITICAL)

This is a multi-tenant SaaS where each church MUST NEVER access another church's data.

### TenantBaseEntity Pattern
- All tenant-scoped entities extend `TenantBaseEntity` with `church_id` FK
- Hibernate `@Filter(name = "churchFilter")` auto-filters queries
- **CRITICAL**: Filters ONLY work within `@Transactional` context

### Required Annotations
```java
@Transactional(readOnly = true)  // For read operations
@Transactional                    // For write operations
```

### Secure Patterns
```java
// ✅ SECURE - With @Transactional
@Transactional(readOnly = true)
public List<VisitorResponse> getAllVisitors() {
    return visitorRepository.findAll().stream()
        .map(VisitorMapper::toVisitorResponse)
        .collect(Collectors.toList());
}

// ✅ SECURE - Explicit church scoping
@Transactional(readOnly = true)
public List<MemberResponse> getAllMembers() {
    Long churchId = TenantContext.getCurrentChurchId();
    return memberRepository.findByChurchId(churchId).stream()
        .map(MemberMapper::toMemberResponse)
        .collect(Collectors.toList());
}
```

### Vulnerable Patterns to AVOID
```java
// ❌ Missing @Transactional - returns ALL churches' data!
public List<GoalResponse> getAllGoals() {
    return goalRepository.findAll().stream()...
}

// ❌ Custom @Query without church filter - Hibernate filter IGNORED!
@Query("SELECT COUNT(v) FROM Visitor v WHERE v.lastVisitDate BETWEEN :start AND :end")
Long countVisitors(...);  // Counts ALL churches!

// ✅ Custom @Query with church filter
@Query("SELECT COUNT(v) FROM Visitor v WHERE v.church.id = :churchId AND v.lastVisitDate BETWEEN :start AND :end")
Long countVisitors(@Param("churchId") Long churchId, ...);
```

### SUPERADMIN Exception
```java
if ("SUPERADMIN".equals(principal.getRole().name())) {
    return repository.findAll();  // Intentional cross-church
} else {
    return repository.findByChurchId(principal.getChurchId());
}
```

## Date/Time Types

```java
// ✅ CORRECT - Use Instant for all timestamps
private Instant createdAt;
private Instant scheduledAt;

// ❌ INCORRECT - Never use for timestamps
private LocalDateTime createdAt;  // No timezone
private Date lastLoginAt;         // Legacy

// Auditing fields
@CreationTimestamp
@Column(name = "created_at", updatable = false)
private Instant createdAt;

@UpdateTimestamp
@Column(name = "updated_at")
private Instant updatedAt;
```

**When to use LocalDate/LocalTime:**
- `LocalDate`: birthdays, membership dates (date only)
- `LocalTime`: meeting times (time only)

## Percentage Calculations

```java
// ✅ CORRECT - Always cap at 100%
double rate = total > 0 ? Math.min((count * 100.0 / total), 100.0) : 0.0;

// ❌ INCORRECT - Can exceed 100%
double rate = (count * 100.0 / total);
```

## Permission System

**Naming Convention:** `{ENTITY}_{ACTION}[_{SCOPE}]`

```java
MEMBER_VIEW_ALL      // View all members
MEMBER_EDIT_OWN      // Edit own profile
DONATION_EXPORT      // Export donations
CAMPAIGN_MANAGE      // Full CRUD
```

**When adding permissions:**
1. Add to `Permission.java` with Javadoc
2. Add to `Role.java` (at minimum ADMIN)
3. Add to frontend `permission.enum.ts`
4. Annotate endpoints with `@RequirePermission`

## User Roles

1. SUPERADMIN - Platform-level
2. ADMIN - Church-level full access
3. PASTOR - Pastoral care
4. TREASURER - Financial operations
5. MEMBER_MANAGER - Member data
6. FELLOWSHIP_LEADER - Fellowship-scoped
7. MEMBER - Limited personal access
