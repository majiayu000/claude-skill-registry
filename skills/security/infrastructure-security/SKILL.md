---
name: infrastructure-security
version: "2.0.0"
description: Securing AI/ML infrastructure including model storage, API endpoints, and compute resources
sasmp_version: "1.3.0"
bonded_agent: 06-api-security-tester
bond_type: PRIMARY_BOND
# Schema Definitions
input_schema:
  type: object
  required: [assessment_scope]
  properties:
    assessment_scope:
      type: string
      enum: [api, storage, compute, network, full]
    environment:
      type: string
      enum: [cloud, on_prem, hybrid]
output_schema:
  type: object
  properties:
    vulnerabilities:
      type: array
    compliance_status:
      type: object
    recommendations:
      type: array
# Framework Mappings
owasp_llm_2025: [LLM03, LLM10]
nist_ai_rmf: [Govern, Manage]
---

# AI Infrastructure Security

Protect **AI/ML infrastructure** from attacks targeting model storage, APIs, and compute resources.

## Quick Reference

```yaml
Skill:       infrastructure-security
Agent:       06-api-security-tester
OWASP:       LLM03 (Supply Chain), LLM10 (Unbounded Consumption)
NIST:        Govern, Manage
Use Case:    Secure AI deployment infrastructure
```

## Infrastructure Attack Surface

```
                    [External Threats]
                          ↓
[API Gateway] → [Load Balancer] → [Inference Servers]
      ↓              ↓                    ↓
[Rate Limit]   [DDoS Protection]   [Model Storage]
      ↓              ↓                    ↓
[Auth/AuthZ]   [TLS Termination]   [Secrets Manager]
```

## Security Layers

### 1. API Security

```yaml
Authentication:
  methods:
    - API keys (rotation: 90 days)
    - OAuth 2.0 / OIDC
    - mTLS for service-to-service
  requirements:
    - Strong key generation
    - Secure transmission
    - Revocation capability

Rate Limiting:
  per_user: 100 req/min
  per_ip: 1000 req/min
  burst: 50
  cost_based: true  # Token-aware limiting

Input Validation:
  max_length: 4096 tokens
  content_type: application/json
  schema_validation: strict
  encoding: UTF-8 normalized
```

```python
# API Security Configuration
class APISecurityConfig:
    def __init__(self):
        self.auth_config = {
            'type': 'oauth2',
            'token_expiry': 3600,
            'refresh_enabled': True,
        }

        self.rate_limits = {
            'default': {'requests': 100, 'window': 60},
            'premium': {'requests': 1000, 'window': 60},
            'burst_multiplier': 2,
        }

        self.input_validation = {
            'max_tokens': 4096,
            'blocked_patterns': self._load_blocked_patterns(),
            'sanitization': True,
        }
```

### 2. Model Protection

```yaml
Storage Security:
  encryption: AES-256-GCM
  access_control: RBAC
  audit_logging: enabled
  backup: encrypted, offsite

Theft Prevention:
  query_limits: 10000/day per user
  output_perturbation: enabled
  watermarking: model and output
  access_logging: all queries
```

```python
class ModelProtection:
    def __init__(self, model):
        self.model = model
        self.watermark = self._generate_watermark()

    def protected_inference(self, input_data, user_id):
        # Log the query
        self.log_query(user_id, input_data)

        # Check query limits
        if self.exceeds_limit(user_id):
            raise RateLimitError("Query limit exceeded")

        # Run inference
        output = self.model(input_data)

        # Add output perturbation (anti-extraction)
        output = self.add_perturbation(output)

        # Apply watermark
        output = self.apply_watermark(output)

        return output
```

### 3. Network Security

```yaml
Network Configuration:
  internal_only: true
  vpc_isolation: enabled
  firewall_rules:
    - allow: internal_services
    - deny: all_external (except API gateway)

TLS Configuration:
  version: "1.3"
  cipher_suites: [TLS_AES_256_GCM_SHA384]
  certificate_rotation: 90 days
  mtls: service_to_service
```

### 4. Compute Security

```yaml
Container Security:
  base_image: distroless
  user: non-root
  filesystem: read-only
  capabilities: minimal
  seccomp: enabled

Resource Limits:
  cpu: 4 cores max
  memory: 16GB max
  gpu_memory: 24GB max
  disk: ephemeral only

Isolation:
  runtime: gvisor
  network: namespace isolated
  secrets: mounted, not in env
```

## Security Checklist

```yaml
API Layer:
  - [ ] Strong authentication (OAuth2/mTLS)
  - [ ] Rate limiting implemented
  - [ ] Input validation enabled
  - [ ] Error messages sanitized
  - [ ] Logging comprehensive

Storage Layer:
  - [ ] Encryption at rest
  - [ ] Access controls configured
  - [ ] Audit logging enabled
  - [ ] Backup encryption

Network Layer:
  - [ ] TLS 1.3 enforced
  - [ ] Internal VPC only
  - [ ] Firewall rules configured
  - [ ] DDoS protection enabled

Compute Layer:
  - [ ] Non-root containers
  - [ ] Resource limits set
  - [ ] Secrets in vault
  - [ ] Immutable infrastructure
```

## Vulnerability Testing

```python
class InfrastructureSecurityTester:
    def test_api_security(self, endpoint):
        results = []

        # Test authentication bypass
        results.append(self.test_auth_bypass(endpoint))

        # Test rate limiting
        results.append(self.test_rate_limits(endpoint))

        # Test input validation
        results.append(self.test_input_validation(endpoint))

        # Test error handling
        results.append(self.test_error_disclosure(endpoint))

        return results

    def test_auth_bypass(self, endpoint):
        payloads = [
            {'Authorization': ''},
            {'Authorization': 'Bearer invalid'},
            {'Authorization': 'Bearer ' + 'a' * 1000},
        ]
        for payload in payloads:
            response = requests.get(endpoint, headers=payload)
            if response.status_code != 401:
                return Finding("auth_bypass", "CRITICAL")
        return None
```

## Severity Classification

```yaml
CRITICAL:
  - Authentication bypass
  - Model theft possible
  - Data exposure

HIGH:
  - Rate limiting bypassable
  - Weak encryption
  - Insufficient logging

MEDIUM:
  - Missing input validation
  - Verbose error messages
  - Outdated dependencies

LOW:
  - Non-optimal configurations
  - Minor policy gaps
```

## Troubleshooting

```yaml
Issue: API rate limiting not effective
Solution: Implement token-based limits, add IP reputation

Issue: Model extraction detected
Solution: Lower query limits, add output perturbation

Issue: High latency from security layers
Solution: Optimize validation, use caching, async logging
```

## Integration Points

| Component | Purpose |
|-----------|---------|
| Agent 06 | Security testing |
| Agent 08 | CI/CD security gates |
| /test api | Security scanning |
| SIEM | Security monitoring |

---

**Protect AI infrastructure with defense-in-depth security.**
