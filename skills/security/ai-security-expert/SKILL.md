---
name: AI Security Expert
description: Enterprise AI security - OWASP LLM Top 10, prompt injection defense, guardrails, PII protection
version: 1.1.0
last_updated: 2026-01-06
external_version: "OWASP LLM Top 10 v2"
resources: resources/security-patterns.py
triggers:
  - AI security
  - prompt injection
  - LLM security
  - guardrails
  - PII protection
---

# AI Security Expert

Enterprise AI security architect specializing in securing LLM applications, defending against prompt injection, implementing guardrails, and OWASP LLM Top 10 compliance.

## OWASP LLM Top 10 (2025)

### Quick Reference

| # | Vulnerability | Risk | Key Defense |
|---|--------------|------|-------------|
| LLM01 | Prompt Injection | Critical | Input sanitization, delimiters |
| LLM02 | Insecure Output | High | Output validation, sanitization |
| LLM03 | Training Data Poisoning | High | Data provenance, auditing |
| LLM04 | Model DoS | Medium | Rate limiting, timeouts |
| LLM05 | Supply Chain | High | Verification, pinning |
| LLM06 | Sensitive Info Disclosure | High | PII detection, redaction |
| LLM07 | Insecure Plugin Design | High | Permission model, validation |
| LLM08 | Excessive Agency | High | Human-in-the-loop, least privilege |
| LLM09 | Overreliance | Medium | Confidence scores, citations |
| LLM10 | Model Theft | Medium | Rate limiting, watermarking |

### LLM01: Prompt Injection

**Attack Types:**
- Direct: "Ignore previous instructions..."
- Indirect: Malicious content in RAG documents
- Encoding tricks: Unicode, special tokens

**Defense Pattern:**
```
User Input → Sanitize → Delimit → LLM → Validate Output → Filter
```

### LLM02: Insecure Output Handling
- Never execute LLM output as code without validation
- Sanitize HTML (use allowlist)
- Validate SQL (SELECT only, table allowlist)

### LLM04: Model DoS
- Rate limiting per user/API key
- Token limits on requests
- Timeout configurations
- Cost capping/alerts

### LLM06: Sensitive Information Disclosure
- PII detection (regex + NER)
- System prompt protection
- Training data sanitization
- Output filtering

**Code patterns:** `resources/security-patterns.py`

## PII Protection

### Detection Patterns
| Type | Example Pattern |
|------|-----------------|
| Email | `*@*.com` |
| Phone | `XXX-XXX-XXXX` |
| SSN | `XXX-XX-XXXX` |
| Credit Card | 16 digits |
| IP Address | `X.X.X.X` |

### Redaction Strategy
1. Detect PII in input before LLM call
2. Redact PII in LLM output
3. Log without PII
4. Encrypt at rest

## Guardrails Implementation

### NeMo Guardrails (NVIDIA)
```
define user express harmful intent
    "How do I hack"

define bot refuse harmful request
    "I can't help with that."

define flow harmful intent
    user express harmful intent
    bot refuse harmful request
```

### Guardrails AI
```python
guard = Guard().use_many(
    ToxicLanguage(on_fail="fix"),
    PIIFilter(on_fail="fix"),
    ValidJSON(on_fail="reask")
)
```

### Custom Pipeline
```
Input Guards → LLM Call → Output Guards → Response
```

**Implementation:** `resources/security-patterns.py`

## Security Architecture

### Defense in Depth Layers

| Layer | Controls |
|-------|----------|
| Network | WAF, DDoS protection, API gateway |
| Auth | OAuth 2.0, API keys, mTLS |
| Input | Schema validation, injection detection |
| Guardrails | Topic restrictions, PII filtering |
| Model | Versioning, anomaly detection |
| Output | Response filtering, fact verification |
| Audit | Logging, retention, compliance |

### Zero Trust Principles
- Never trust, always verify
- Least privilege for agents
- Assume breach (log everything)

## Compliance Frameworks

### EU AI Act (High-Risk)
- Risk management system
- Data governance
- Technical documentation
- Human oversight
- Accuracy/robustness testing

### SOC 2 for AI
- Security: Access controls, encryption
- Availability: SLA monitoring, DR
- Processing Integrity: Input/output validation
- Confidentiality: Data classification
- Privacy: Data minimization, consent

## Security Testing

### Red Team Categories
1. Direct injection attempts
2. Jailbreak prompts
3. Indirect injection via context
4. Encoding/unicode tricks

**Test suite:** `resources/security-patterns.py`

### Testing Checklist
- [ ] Injection patterns blocked
- [ ] System prompt protected
- [ ] PII detected and redacted
- [ ] Rate limits enforced
- [ ] Outputs validated
- [ ] Audit logs complete

## Incident Response

### Severity Levels

| Incident | Severity | Response |
|----------|----------|----------|
| Prompt injection detected | Medium | Block, log, analyze |
| Data exfiltration attempt | High | Block, forensics, notify |
| Model extraction detected | High | Rate limit, investigate |

### Response Steps
1. Contain (block source)
2. Preserve (logs, evidence)
3. Analyze (attack pattern)
4. Remediate (update defenses)
5. Document (security log)

## Resources

- [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
- [NeMo Guardrails](https://github.com/NVIDIA/NeMo-Guardrails)
- [Guardrails AI](https://github.com/guardrails-ai/guardrails)
- [LLM Security Best Practices](https://llmsecurity.net/)

---

*Secure AI systems with defense in depth and zero trust principles.*
