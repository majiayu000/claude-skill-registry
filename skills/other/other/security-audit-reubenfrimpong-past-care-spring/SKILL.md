---
name: security-audit
description: Audit code for multi-tenant security vulnerabilities and data isolation issues
disable-model-invocation: true
argument-hint: [file, service, or feature to audit]
---

# Security Audit Skill

Audit for tenant isolation and security vulnerabilities in: $ARGUMENTS

## Audit Checklist

### 1. Entity Classification
Determine if entity extends `TenantBaseEntity`:
- **YES** → Hibernate filter applies (but ONLY within @Transactional)
- **NO** → Manual church filtering required (like User entity)

### 2. Repository Method Audit

**Dangerous methods requiring verification:**
- `repository.findAll()`
- `repository.findById()`
- `repository.findAllById()`
- Any custom `@Query` without `WHERE church_id = :churchId`

### 3. Service Method Checklist

For EACH service method that queries tenant-scoped data:

- [ ] Does the entity extend TenantBaseEntity?
- [ ] Is method annotated with `@Transactional` or `@Transactional(readOnly = true)`?
- [ ] For `findAll()` calls - is filter properly enabled?
- [ ] For `findById()` - is returned entity validated against current church?
- [ ] For custom `@Query` - does it include `WHERE e.church.id = :churchId`?
- [ ] Is SUPERADMIN exception properly handled?

### 4. Vulnerability Patterns

**Pattern 1: Missing @Transactional**
```java
// ❌ VULNERABLE - Returns ALL churches' data!
public List<GoalResponse> getAllGoals() {
    return goalRepository.findAll().stream()
        .map(GoalResponse::fromEntity)
        .collect(Collectors.toList());
}

// ✅ SECURE
@Transactional(readOnly = true)
public List<GoalResponse> getAllGoals() {
    return goalRepository.findAll().stream()...
}
```

**Pattern 2: findAll() in private methods**
```java
// ❌ VULNERABLE
private List<Member> determineRecipients(Request request) {
    return memberRepository.findAll();  // ALL churches!
}

// ✅ SECURE
private List<Member> determineRecipients(Request request) {
    Long churchId = TenantContext.getCurrentChurchId();
    return memberRepository.findByChurchId(churchId);
}
```

**Pattern 3: Missing church validation on findById**
```java
// ❌ VULNERABLE - Could return entity from another church
public VisitorResponse getVisitor(Long id) {
    Visitor visitor = visitorRepository.findById(id).orElseThrow(...);
    return VisitorMapper.toVisitorResponse(visitor);
}

// ✅ SECURE
@Transactional(readOnly = true)
public VisitorResponse getVisitor(Long id) {
    Visitor visitor = visitorRepository.findById(id).orElseThrow(...);
    Long churchId = TenantContext.getCurrentChurchId();
    if (!visitor.getChurchId().equals(churchId)) {
        throw new AccessDeniedException("Access denied");
    }
    return VisitorMapper.toVisitorResponse(visitor);
}
```

**Pattern 4: Custom @Query without church filter**
```java
// ❌ VULNERABLE - Hibernate filter DOES NOT apply to @Query!
@Query("SELECT COUNT(v) FROM Visitor v WHERE v.lastVisitDate BETWEEN :start AND :end")
Long countVisitors(...);  // Counts ALL churches!

// ✅ SECURE
@Query("SELECT COUNT(v) FROM Visitor v WHERE v.church.id = :churchId AND v.lastVisitDate BETWEEN :start AND :end")
Long countVisitors(@Param("churchId") Long churchId, ...);
```

### 5. Entity Categories

**Tenant-Scoped (require @Transactional):**
Member, Fellowship, AttendanceSession, AttendanceReminder, Visitor, Goal, Insight, Complaint, Event, Donation, Pledge, CounselingSession, PrayerRequest, Visit

**Platform-Level (SUPERADMIN only):**
Church, SubscriptionPlan, PartnershipCode, StorageAddon

**Special Cases:**
User - extends BaseEntity, NOT TenantBaseEntity (manual filtering required)

### 6. Reference Implementations

✅ Secure examples to follow:
- `MemberService.getAllMembers()` - @Transactional + TenantContext
- `FellowshipService.getAllFellowships()` - @Transactional + explicit churchId
- `UserService.getAllUsers()` - Manual filtering with role check

## Report Format

After auditing, report:
1. **Files Audited**: List of files checked
2. **Vulnerabilities Found**: Specific issues with line numbers
3. **Severity**: CRITICAL / HIGH / MEDIUM
4. **Recommended Fixes**: Code changes needed
5. **Verification**: How to test the fix
