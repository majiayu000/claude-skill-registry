---
name: quota-management
description: 'Quota tracking, threshold monitoring, and graceful degradation for rate-limited
  API services.


  quota, rate limiting, usage limits, thresholds.'
category: infrastructure
tags:
- quota
- rate-limiting
- resource-management
- cost-tracking
- thresholds
dependencies: []
tools:
- quota-tracker
provides:
  infrastructure:
  - quota-tracking
  - threshold-monitoring
  - usage-estimation
  patterns:
  - graceful-degradation
  - quota-enforcement
  - cost-optimization
usage_patterns:
- service-integration
- rate-limit-management
- cost-tracking
- resource-monitoring
complexity: intermediate
estimated_tokens: 500
progressive_loading: true
modules:
- modules/threshold-strategies.md
- modules/estimation-patterns.md
---
## Table of Contents

- [Overview](#overview)
- [When to Use](#when-to-use)
- [Core Concepts](#core-concepts)
- [Quota Thresholds](#quota-thresholds)
- [Quota Types](#quota-types)
- [Quick Start](#quick-start)
- [Check Quota Status](#check-quota-status)
- [Record Usage](#record-usage)
- [Estimate Before Execution](#estimate-before-execution)
- [Integration Pattern](#integration-pattern)
- [Detailed Resources](#detailed-resources)
- [Exit Criteria](#exit-criteria)


# Quota Management

## Overview

Patterns for tracking and enforcing resource quotas across rate-limited services. This skill provides the infrastructure that other plugins use for consistent quota handling.

## When To Use

- Building integrations with rate-limited APIs
- Need to track usage across sessions
- Want graceful degradation when limits approached
- Require cost estimation before operations

## When NOT To Use

- Project doesn't use the leyline infrastructure patterns
- Simple scripts without service architecture needs

## Core Concepts

### Quota Thresholds

Three-tier threshold system for proactive management:

| Level | Usage | Action |
|-------|-------|--------|
| **Healthy** | <80% | Proceed normally |
| **Warning** | 80-95% | Alert, consider batching |
| **Critical** | >95% | Defer non-urgent, use secondary services |

### Quota Types

```python
@dataclass
class QuotaConfig:
    requests_per_minute: int = 60
    requests_per_day: int = 1000
    tokens_per_minute: int = 100000
    tokens_per_day: int = 1000000
```

## Quick Start

### Check Quota Status
```python
from leyline.quota_tracker import QuotaTracker

tracker = QuotaTracker(service="my-service")
status, warnings = tracker.get_quota_status()

if status == "CRITICAL":
    # Defer or use secondary service
    pass
```

### Record Usage
```python
tracker.record_request(
    tokens=estimated_tokens,
    success=True,
    duration=elapsed_seconds
)
```

### Estimate Before Execution
```python
can_proceed, issues = tracker.can_handle_task(estimated_tokens)
if not can_proceed:
    print(f"Quota issues: {issues}")
```

## Integration Pattern

Other plugins reference this skill:

```yaml
# In your skill's frontmatter
dependencies: [leyline:quota-management]
```

Then use the shared patterns:
1. Initialize tracker for your service
2. Check quota before operations
3. Record usage after operations
4. Handle threshold warnings gracefully

## Detailed Resources

- **Threshold Strategies**: See `modules/threshold-strategies.md` for degradation patterns
- **Estimation Patterns**: See `modules/estimation-patterns.md` for token/cost estimation

## Exit Criteria

- Quota status checked before operation
- Usage recorded after operation
- Threshold warnings handled appropriately
## Troubleshooting

### Common Issues

**Command not found**
Ensure all dependencies are installed and in PATH

**Permission errors**
Check file permissions and run with appropriate privileges

**Unexpected behavior**
Enable verbose logging with `--verbose` flag
