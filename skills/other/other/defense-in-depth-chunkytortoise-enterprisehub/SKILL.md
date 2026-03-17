---
name: Defense in Depth
description: This skill should be used when implementing "multi-layer validation", "comprehensive error handling", "input sanitization", "security testing", "data validation layers", "fault tolerance", or when building robust systems with multiple validation checkpoints.
version: 2.0.0
---

# Defense in Depth: Multi-Layer Validation and Security

## Overview

This skill implements comprehensive defense-in-depth strategies for robust applications. It provides multiple layers of validation, security checks, and error handling to ensure system resilience against various failure modes and attack vectors.

**Progressive Disclosure**: This file contains core concepts and quick reference patterns. For complete implementations, see `reference/` directory.

## When to Use This Skill

Use this skill when implementing:
- **Multi-layer input validation**
- **Comprehensive error handling strategies**
- **Security hardening with multiple checkpoints**
- **Data integrity validation across system layers**
- **Fault-tolerant system architectures**
- **API security with multiple validation stages**
- **Database security and data protection**

## Core Architecture: 5 Layers of Defense

```
┌─────────────────────────────────────────────────────┐
│  Layer 5: Application Security                      │
│  - Monitoring, anomaly detection, logging           │
├─────────────────────────────────────────────────────┤
│  Layer 4: API Security                              │
│  - JWT validation, rate limiting, permissions       │
├─────────────────────────────────────────────────────┤
│  Layer 3: Database Security                         │
│  - SQL injection prevention, safe queries           │
├─────────────────────────────────────────────────────┤
│  Layer 2: Business Logic Validation                 │
│  - Workflow validation, business rules              │
├─────────────────────────────────────────────────────┤
│  Layer 1: Input Validation                          │
│  - Type checking, sanitization, format validation   │
└─────────────────────────────────────────────────────┘
```

## Quick Reference: Validation Patterns

### Layer 1: Input Validation

**Core Classes** (see `reference/input-validation-layer.md` for complete implementation):

```python
from dataclasses import dataclass
from enum import Enum
from typing import Any, List, Optional


class ValidationSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class ValidationResult:
    """Standard validation result structure."""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    sanitized_data: Optional[Any] = None
    severity: ValidationSeverity = ValidationSeverity.INFO
```

**Common Patterns**:

```python
# Email validation pattern
validator = InputValidator(strict_mode=True)
result = validator.validate_email(user_input)
if not result.is_valid:
    return handle_validation_error(result.errors)

# Numeric validation with bounds
result = validator.validate_numeric_input(
    value=user_input,
    min_value=0,
    max_value=1000000,
    allow_decimal=True
)

# HTML sanitization
result = validator.sanitize_html_input(user_content)
sanitized_html = result.sanitized_data
```

**📖 Complete Implementation**: `reference/input-validation-layer.md`

### Layer 2: Business Logic Validation

**Core Patterns** (see `reference/business-logic-validation.md`):

```python
# Registration workflow validation
business_validator = BusinessLogicValidator(config={
    'max_registration_attempts': 5,
    'registration_window_minutes': 60
})

result = business_validator.validate_registration_workflow(
    email=email,
    user_data=user_data,
    existing_attempts=attempts
)

# Transaction validation
result = business_validator.validate_transaction(
    transaction_type='withdrawal',
    amount=500.00,
    user_context=user_context,
    account_balance=1000.00
)
```

**Key Features**:
- Rate limiting
- Workflow state validation
- Domain-specific business rules
- Fraud detection patterns

**📖 Complete Implementation**: `reference/business-logic-validation.md`

### Layer 3: Database Security

**Core Patterns** (see `reference/database-security-layer.md`):

```python
from sqlalchemy.orm import Session

# Safe parameterized queries
db_security = DatabaseSecurityLayer(session)

result = db_security.safe_query(
    model=Lead,
    filters={'email': user_email, 'status': 'active'},
    order_by='created_at',
    limit=100
)

# Safe insert with validation
result = db_security.safe_insert(
    model=Lead,
    data={'email': email, 'name': name}
)

# Safe update with filters
result = db_security.safe_update(
    model=Lead,
    filters={'id': lead_id},
    updates={'status': 'qualified'}
)
```

**Key Features**:
- SQL injection prevention
- Parameterized queries only
- Filter validation
- Query logging for audit

**📖 Complete Implementation**: `reference/database-security-layer.md`

### Layer 4: API Security

**Core Patterns** (see `reference/api-security-layer.md`):

```python
# JWT token validation
api_security = APISecurityLayer(secret_key=settings.JWT_SECRET)

result = api_security.validate_jwt_token(token)
if result.is_valid:
    user_data = result.sanitized_data

# Rate limiting
result = api_security.check_rate_limit(
    identifier=f"{user_id}:{ip_address}",
    max_requests=100,
    window_seconds=60
)

# Complete request validation
result = api_security.validate_api_request(
    request=request,
    required_permissions=['leads:read', 'properties:read']
)
```

**FastAPI Integration**:

```python
from fastapi import Depends

@app.get("/api/leads")
async def get_leads(
    user = Depends(api_security.require_auth),
    _rate_limit = Depends(api_security.rate_limit(100, 60))
):
    # Protected endpoint with auth and rate limiting
    pass
```

**📖 Complete Implementation**: `reference/api-security-layer.md`

### Layer 5: Application Security

**Core Patterns** (see `reference/application-security-layer.md`):

```python
# Security event logging
app_security = ApplicationSecurityLayer()

app_security.log_security_event(SecurityEvent(
    event_type=SecurityEventType.AUTH_FAILURE,
    severity=ValidationSeverity.WARNING,
    user_id=user_id,
    ip_address=ip_address,
    details={'reason': 'invalid_credentials'}
))

# Permission checking
result = app_security.check_user_permissions(
    user_id=user_id,
    resource='leads',
    action='delete',
    user_permissions=user.permissions
)

# Anomaly detection
result = app_security.detect_anomalous_behavior(
    user_id=user_id,
    current_behavior={
        'requests_per_minute': 150,
        'resources': ['leads', 'contacts', 'admin'],
        'location': 'RU'
    }
)
```

**📖 Complete Implementation**: `reference/application-security-layer.md`

## GHL Real Estate Platform Integration

**Project-Specific Implementation** (see `reference/ghl-real-estate-implementation.md`):

### Lead Registration with Full Defense-in-Depth

```python
class LeadRegistrationSecurity:
    """Complete 5-layer validation for lead registration."""

    async def validate_and_register_lead(
        self,
        lead_data: Dict[str, Any],
        ghl_location_id: str,
        ip_address: str
    ) -> ValidationResult:
        # Layer 1: Input validation (email, phone, data)
        email_result = self.input_validator.validate_email(lead_data['email'])
        if not email_result.is_valid:
            return email_result

        # Layer 2: Business logic (rate limiting, domain checks)
        business_result = self.business_validator.validate_registration_workflow(
            email_result.sanitized_data,
            lead_data,
            existing_attempts
        )

        # Layer 3: Database security (safe insert)
        lead_id = await self._safe_insert_lead(lead_data, ghl_location_id)

        # Layer 4: API security (GHL webhook signature)
        await self._sync_to_ghl(lead_id, lead_data, ghl_location_id)

        # Layer 5: Application security (logging, monitoring)
        self.security_layer.log_security_event(...)

        return ValidationResult(True, [], [], {'lead_id': lead_id})
```

**📖 Complete Implementation**: `reference/ghl-real-estate-implementation.md`

## Implementation Checklist

Use this checklist when implementing defense-in-depth:

### Layer 1: Input Validation
- [ ] Validate all string inputs (email, phone, text)
- [ ] Sanitize HTML inputs with whitelist
- [ ] Validate numeric inputs with bounds
- [ ] Check input lengths to prevent buffer issues
- [ ] Detect and reject dangerous patterns

### Layer 2: Business Logic
- [ ] Implement rate limiting for sensitive operations
- [ ] Validate workflow states and transitions
- [ ] Check domain-specific business rules
- [ ] Validate time-based constraints
- [ ] Implement fraud detection patterns

### Layer 3: Database Security
- [ ] Use parameterized queries exclusively
- [ ] Validate filter inputs for SQL injection
- [ ] Implement query logging for audit
- [ ] Use transactions for consistency
- [ ] Limit query result sizes

### Layer 4: API Security
- [ ] Validate JWT tokens on all protected endpoints
- [ ] Implement rate limiting per user/IP
- [ ] Check permissions for every operation
- [ ] Validate request sizes and content types
- [ ] Log authentication failures

### Layer 5: Application Security
- [ ] Log all security events with severity
- [ ] Monitor for attack patterns
- [ ] Implement anomaly detection
- [ ] Validate sessions on every request
- [ ] Maintain audit trail for compliance

## Best Practices

### 1. Fail Secure
```python
# ❌ BAD: Default to allowing access
def check_permission(user, resource):
    if user.is_admin():
        return True
    # Forgot to handle other cases - defaults to allowing!

# ✅ GOOD: Default to denying access
def check_permission(user, resource):
    if user.is_admin():
        return True
    if f"{resource}:read" in user.permissions:
        return True
    return False  # Explicit deny
```

### 2. Defense in Depth
Never rely on a single layer of validation:

```python
# ✅ GOOD: Multiple validation layers
async def create_lead(lead_data: Dict):
    # Layer 1: Input validation
    if not validate_email(lead_data['email']):
        raise ValueError("Invalid email")

    # Layer 2: Business logic
    if not check_rate_limit(lead_data['email']):
        raise RateLimitError()

    # Layer 3: Database security
    await safe_insert(lead_data)

    # Layer 4: Application logging
    log_security_event('lead_created', lead_data['email'])
```

### 3. Structured Error Handling
Always return `ValidationResult` for consistent error handling:

```python
# ✅ GOOD: Structured validation results
result = validator.validate_email(email)
if not result.is_valid:
    log_errors(result.errors, result.severity)
    return {'status': 'error', 'errors': result.errors}

# Use sanitized data only if valid
if result.is_valid:
    email = result.sanitized_data
```

### 4. Logging and Monitoring
```python
# Log all security-relevant events
security_layer.log_security_event(SecurityEvent(
    event_type=SecurityEventType.AUTH_FAILURE,
    severity=ValidationSeverity.WARNING,
    user_id=user_id,
    details={'reason': error_message}
))
```

## Testing Defense-in-Depth

### Unit Tests for Each Layer

```python
# Test Layer 1: Input validation
def test_email_validation():
    validator = InputValidator()

    # Valid email
    result = validator.validate_email("user@example.com")
    assert result.is_valid
    assert result.sanitized_data == "user@example.com"

    # Invalid email
    result = validator.validate_email("invalid")
    assert not result.is_valid
    assert "Invalid email format" in result.errors

    # SQL injection attempt
    result = validator.validate_email("'; DROP TABLE users--")
    assert not result.is_valid
    assert "dangerous characters" in str(result.errors)
```

### Integration Tests

```python
# Test complete validation pipeline
async def test_lead_registration_pipeline():
    security = LeadRegistrationSecurity()

    # Valid registration
    result = await security.validate_and_register_lead(
        lead_data={'email': 'test@example.com', 'name': 'Test'},
        ghl_location_id='loc_123',
        ip_address='192.168.1.1'
    )
    assert result.is_valid

    # Rate limit test
    for _ in range(6):
        await security.validate_and_register_lead(...)

    result = await security.validate_and_register_lead(...)
    assert not result.is_valid
    assert "Too many registration attempts" in str(result.errors)
```

## Reference Files

Load these files for complete implementation details:

| Layer | Reference File | Description |
|-------|----------------|-------------|
| Layer 1 | `reference/input-validation-layer.md` | Email, password, numeric, HTML validation |
| Layer 2 | `reference/business-logic-validation.md` | Registration, transactions, business rules |
| Layer 3 | `reference/database-security-layer.md` | SQL injection prevention, safe queries |
| Layer 4 | `reference/api-security-layer.md` | JWT validation, rate limiting, API security |
| Layer 5 | `reference/application-security-layer.md` | Monitoring, anomaly detection, logging |
| GHL Integration | `reference/ghl-real-estate-implementation.md` | Project-specific implementations |

## Summary

Defense-in-depth provides **five layers of validation and security**:

1. **Input Validation**: First line of defense against malicious input
2. **Business Logic**: Domain-specific rules and workflow validation
3. **Database Security**: SQL injection prevention and safe queries
4. **API Security**: Authentication, authorization, and rate limiting
5. **Application Security**: Monitoring, logging, and anomaly detection

**Core Principle**: Never rely on a single validation layer. Each layer should operate independently and provide its own protection.

**Token Optimization**: Core concepts in SKILL.md (~400 lines), detailed implementations in reference files (loaded on-demand).

---

**Version**: 2.0.0 (Token-Optimized with Progressive Disclosure)
**Token Count**: ~600 tokens (was ~2,600 tokens)
**Savings**: ~2,000 tokens (77% reduction)
