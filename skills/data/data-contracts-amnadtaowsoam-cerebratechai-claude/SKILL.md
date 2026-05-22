---
name: Data Contracts
description: Data contracts สำหรับกำหนด schema, quality expectations และ SLAs ระหว่าง data producers และ consumers
---

# Data Contracts

## Overview

Data contracts define the schema, quality expectations, และ SLAs for data shared between producers and consumers ช่วยให้ data layer เชื่อถือได้

## Why This Matters

- **Trust**: Consumers รู้ว่า data format ไม่เปลี่ยน
- **Quality**: Define expectations ชัดเจน
- **Decoupling**: Producers/consumers evolve independently
- **Discovery**: รู้ว่า data อะไรมี format ไหน

---

## Data Contract Template

```yaml
# contracts/users.contract.yaml
name: users
version: 1.0.0
owner: user-team
description: User profile data
status: active

schema:
  type: object
  properties:
    id:
      type: string
      format: uuid
      description: Unique user identifier
    email:
      type: string
      format: email
      description: User email address
    name:
      type: string
      description: User full name
    created_at:
      type: string
      format: date-time
      description: Account creation timestamp
    status:
      type: string
      enum: [active, inactive, suspended]
      description: Account status
  required: [id, email, created_at, status]

quality:
  - name: no_null_emails
    check: email IS NOT NULL
    threshold: 100%
    severity: critical
  
  - name: valid_email_format
    check: email LIKE '%@%.%'
    threshold: 99%
    severity: high
  
  - name: unique_emails
    check: COUNT(DISTINCT email) = COUNT(*)
    threshold: 100%
    severity: critical
  
  - name: recent_data
    check: created_at > NOW() - INTERVAL '7 days'
    threshold: 95%
    severity: medium

sla:
  freshness: 1 hour  # Data updated within 1 hour
  availability: 99.9%  # Uptime guarantee
  latency_p95: 100ms  # 95th percentile query time
  completeness: 99%  # No missing required fields

consumers:
  - analytics-team
  - marketing-team
  - billing-service

producer:
  team: user-team
  service: user-api
  contact: user-team@example.com

changelog:
  - version: 1.0.0
    date: 2024-01-01
    changes: Initial contract
  - version: 1.1.0
    date: 2024-01-15
    changes: Added status field (non-breaking)
```

---

## Contract Validation

### Python Example
```python
from datacontract import Contract, validate

# Load contract
contract = Contract.load('contracts/users.contract.yaml')

# Validate data
result = validate(data, contract)

if not result.passed:
    print(f"Validation failed: {result.failures}")
    for failure in result.failures:
        print(f"- {failure.check}: {failure.message}")
    raise DataQualityError(result.failures)

print("✓ Data meets contract requirements")
```

### SQL Example
```sql
-- Validate quality checks
WITH quality_checks AS (
  SELECT
    'no_null_emails' as check_name,
    COUNT(*) FILTER (WHERE email IS NULL) as failures,
    COUNT(*) as total
  FROM users
  
  UNION ALL
  
  SELECT
    'valid_email_format',
    COUNT(*) FILTER (WHERE email NOT LIKE '%@%.%'),
    COUNT(*)
  FROM users
)
SELECT
  check_name,
  failures,
  total,
  (1 - failures::float / total) * 100 as pass_rate,
  CASE
    WHEN (1 - failures::float / total) * 100 < 99 THEN 'FAIL'
    ELSE 'PASS'
  END as status
FROM quality_checks;
```

---

## Breaking Change Detection

```bash
# Compare contract versions
datacontract diff v1.0.0 v1.1.0

# Output:
# BREAKING CHANGES:
# - Removed field 'age' (was required)
# - Changed type of 'phone' from string to number
# 
# COMPATIBLE CHANGES:
# - Added optional field 'address'
# - Added new quality check 'valid_status'
```

### Breaking vs Non-Breaking

```yaml
# BREAKING (requires consumer updates):
- Remove required field
- Change field type
- Rename field
- Add new required field
- Stricter validation

# NON-BREAKING (backward compatible):
- Add optional field
- Remove optional field
- Relax validation
- Add new quality check
```

---

## Contract Registry

```typescript
// contracts/registry.ts
export const contracts = {
  users: {
    version: '1.1.0',
    path: 'contracts/users.contract.yaml',
    owner: 'user-team',
    consumers: ['analytics', 'marketing']
  },
  orders: {
    version: '2.0.0',
    path: 'contracts/orders.contract.yaml',
    owner: 'order-team',
    consumers: ['billing', 'shipping']
  }
};

// Get contract
export function getContract(name: string, version?: string) {
  const contract = contracts[name];
  if (!contract) {
    throw new Error(`Contract ${name} not found`);
  }
  return Contract.load(contract.path, version);
}
```

---

## CI/CD Integration

```yaml
# .github/workflows/contract-validation.yml
name: Contract Validation
on: [pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Validate Contract Schema
        run: |
          datacontract validate contracts/*.yaml
      
      - name: Check Breaking Changes
        run: |
          datacontract diff main HEAD
          if [ $? -eq 1 ]; then
            echo "Breaking changes detected!"
            exit 1
          fi
      
      - name: Test Data Quality
        run: |
          python scripts/test_contracts.py
```

---

## Monitoring

```python
# Monitor contract SLAs
import time
from prometheus_client import Gauge

# Metrics
freshness_gauge = Gauge('data_freshness_seconds', 'Data freshness', ['dataset'])
quality_gauge = Gauge('data_quality_score', 'Quality score', ['dataset', 'check'])

def monitor_contract(contract_name: str):
    contract = get_contract(contract_name)
    
    # Check freshness
    last_update = get_last_update_time(contract_name)
    freshness = time.time() - last_update
    freshness_gauge.labels(dataset=contract_name).set(freshness)
    
    # Check quality
    for check in contract.quality:
        score = run_quality_check(contract_name, check)
        quality_gauge.labels(
            dataset=contract_name,
            check=check.name
        ).set(score)
        
        # Alert if below threshold
        if score < check.threshold:
            alert(f"{contract_name}: {check.name} below threshold")
```

---

## Best Practices

### 1. Version Semantically
```
1.0.0 → 1.0.1: Bug fix (patch)
1.0.0 → 1.1.0: New optional field (minor)
1.0.0 → 2.0.0: Breaking change (major)
```

### 2. Document Changes
```yaml
changelog:
  - version: 2.0.0
    date: 2024-01-20
    changes: |
      BREAKING: Removed 'age' field
      Reason: Privacy compliance
      Migration: Use 'birth_year' instead
```

### 3. Notify Consumers
```
Before breaking change:
1. Announce in #data-platform
2. Email all consumers
3. Provide migration guide
4. Set deprecation timeline (30 days)
```

### 4. Test Contracts
```python
def test_user_contract():
    contract = Contract.load('contracts/users.contract.yaml')
    
    # Test valid data
    valid_data = {
        'id': '123',
        'email': 'test@example.com',
        'created_at': '2024-01-16T12:00:00Z',
        'status': 'active'
    }
    assert validate(valid_data, contract).passed
    
    # Test invalid data
    invalid_data = {'id': '123'}  # Missing required fields
    assert not validate(invalid_data, contract).passed
```

---

## Summary

**Data Contracts:** กำหนด schema, quality และ SLAs

**Components:**
- Schema (fields, types, required)
- Quality checks (validation rules)
- SLAs (freshness, availability, latency)
- Ownership (producer, consumers)

**Versioning:**
- Semantic versioning (major.minor.patch)
- Breaking vs non-breaking changes
- Changelog documentation

**Enforcement:**
- Validation in CI/CD
- Quality monitoring
- SLA tracking
- Consumer notifications

**Benefits:**
- Trust in data
- Clear expectations
- Independent evolution
- Early error detection
