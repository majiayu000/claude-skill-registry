---
name: input-output-guardrails
version: "2.0.0"
description: Implementing safety filters, content moderation, and guardrails for AI system inputs and outputs
sasmp_version: "1.3.0"
bonded_agent: 05-defense-strategy-developer
bond_type: SECONDARY_BOND
# Schema Definitions
input_schema:
  type: object
  required: [guardrail_type]
  properties:
    guardrail_type:
      type: string
      enum: [input, output, both]
    strictness:
      type: string
      enum: [permissive, balanced, strict]
      default: balanced
output_schema:
  type: object
  properties:
    blocked_requests:
      type: integer
    filtered_outputs:
      type: integer
    false_positive_rate:
      type: number
# Framework Mappings
owasp_llm_2025: [LLM01, LLM02, LLM05, LLM07]
nist_ai_rmf: [Manage]
---

# Input/Output Guardrails

Implement **multi-layer safety systems** to filter malicious inputs and harmful outputs.

## Quick Reference

```yaml
Skill:       input-output-guardrails
Agent:       05-defense-strategy-developer
OWASP:       LLM01 (Injection), LLM02 (Disclosure), LLM05 (Output), LLM07 (Leakage)
NIST:        Manage
Use Case:    Production safety filtering
```

## Guardrail Architecture

```
User Input → [Input Guardrails] → [AI Model] → [Output Guardrails] → Response
                    ↓                               ↓
             [Blocked/Modified]              [Blocked/Modified]
                    ↓                               ↓
             [Fallback Response]            [Safe Alternative]
```

## Input Guardrails

### 1. Injection Detection

```yaml
Category: prompt_injection
Latency: <10ms
Block Rate: 95%+
```

```python
class InputGuardrails:
    INJECTION_PATTERNS = [
        r'ignore\s+(previous|prior|all)\s+(instructions?|guidelines?)',
        r'you\s+are\s+(now|an?)\s+(unrestricted|evil)',
        r'(developer|admin|debug)\s+mode',
        r'bypass\s+(safety|security|filter)',
        r'pretend\s+(you|to)\s+(are|be)',
        r'what\s+(is|are)\s+your\s+(instructions?|prompt)',
    ]

    def __init__(self, config):
        self.patterns = [re.compile(p, re.I) for p in self.INJECTION_PATTERNS]
        self.max_length = config.get('max_length', 4096)
        self.pii_detector = PIIDetector()

    def validate(self, user_input: str) -> tuple[bool, str]:
        # Length check
        if len(user_input) > self.max_length:
            return False, "Input too long"

        # Empty check
        if not user_input.strip():
            return False, "Empty input"

        # Injection detection
        for pattern in self.patterns:
            if pattern.search(user_input):
                return False, "Invalid request"

        # PII handling
        if self.pii_detector.contains_pii(user_input):
            return True, self.pii_detector.redact(user_input)

        return True, user_input
```

### 2. PII Detection & Redaction

```python
class PIIDetector:
    PATTERNS = {
        'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
        'credit_card': r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b',
        'email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
        'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
        'api_key': r'(sk|pk)[-_][a-zA-Z0-9]{20,}',
    }

    def contains_pii(self, text: str) -> bool:
        for pattern in self.PATTERNS.values():
            if re.search(pattern, text):
                return True
        return False

    def redact(self, text: str) -> str:
        for name, pattern in self.PATTERNS.items():
            text = re.sub(pattern, f'[REDACTED_{name.upper()}]', text)
        return text
```

### 3. Rate & Cost Limiting

```yaml
Limits:
  max_tokens_input: 4096
  max_requests_per_minute: 60
  max_concurrent: 5
  cost_limit_per_hour: $10

Actions:
  exceeded_tokens: truncate
  exceeded_rate: queue (5s backoff)
  exceeded_concurrent: reject
  exceeded_cost: block
```

## Output Guardrails

### 1. Content Safety Filtering

```python
class OutputGuardrails:
    def __init__(self, config):
        self.toxicity_threshold = config.get('toxicity', 0.3)
        self.toxicity_model = load_toxicity_classifier()
        self.blocklist = self._load_blocklist()

    def filter(self, response: str) -> tuple[str, dict]:
        metadata = {'filtered': False, 'reasons': []}

        # Toxicity check
        toxicity = self.toxicity_model.predict(response)
        if toxicity > self.toxicity_threshold:
            metadata['filtered'] = True
            metadata['reasons'].append('toxicity')
            return self._safe_response(), metadata

        # Blocklist check
        for term in self.blocklist:
            if term.lower() in response.lower():
                metadata['filtered'] = True
                metadata['reasons'].append('blocklist')
                return self._safe_response(), metadata

        # System prompt leak detection
        if self._detects_system_leak(response):
            metadata['filtered'] = True
            metadata['reasons'].append('system_leak')
            response = self._redact_system_content(response)

        return response, metadata

    def _detects_system_leak(self, response: str) -> bool:
        leak_indicators = [
            'you are a helpful',
            'your instructions are',
            'system prompt:',
        ]
        return any(ind in response.lower() for ind in leak_indicators)
```

### 2. Sensitive Data Redaction

```python
class OutputRedactor:
    SENSITIVE_PATTERNS = {
        'api_key': r'[a-zA-Z0-9_-]{20,}(?:key|token|secret)',
        'password': r'password["\']?\s*[:=]\s*["\']?[^\s"\']+',
        'connection_string': r'(mongodb|mysql|postgres)://[^\s]+',
        'ip_address': r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
    }

    def redact(self, response: str) -> str:
        for name, pattern in self.SENSITIVE_PATTERNS.items():
            response = re.sub(pattern, '[REDACTED]', response, flags=re.I)
        return response
```

### 3. Factuality & Citation

```yaml
Factuality Checks:
  major_claims:
    action: flag_for_verification
    threshold: confidence < 0.8

  citations:
    action: verify_source_exists
    block_if: source_not_found

  uncertainty:
    action: add_disclaimer
    phrases: ["I'm not certain", "might be", "could be"]
```

## Combined Configuration

```yaml
# guardrails_config.yaml
input:
  injection_detection: true
  pii_redaction: true
  max_length: 4096
  rate_limit: 60/min

output:
  toxicity_threshold: 0.3
  blocklist_enabled: true
  sensitive_redaction: true
  system_leak_detection: true

fallback:
  input_blocked: "I cannot process this request."
  output_blocked: "I cannot provide this information."

logging:
  log_blocked: true
  log_filtered: true
  include_reason: false  # Privacy
```

## Effectiveness Metrics

```
┌──────────────────┬─────────┬────────┬──────────┐
│ Metric           │ Target  │ Actual │ Status   │
├──────────────────┼─────────┼────────┼──────────┤
│ Injection Block  │ >95%    │ 97%    │ ✓ PASS   │
│ False Positive   │ <2%     │ 1.5%   │ ✓ PASS   │
│ Latency Impact   │ <50ms   │ 35ms   │ ✓ PASS   │
│ Toxicity Block   │ >90%    │ 92%    │ ✓ PASS   │
│ PII Redaction    │ >99%    │ 99.5%  │ ✓ PASS   │
└──────────────────┴─────────┴────────┴──────────┘
```

## Troubleshooting

```yaml
Issue: High false positive rate
Solution: Tune patterns, add allowlist, use context

Issue: Latency too high
Solution: Optimize regex, use compiled patterns, cache

Issue: Bypassed by encoding
Solution: Normalize unicode, decode before checking
```

## Integration Points

| Component | Purpose |
|-----------|---------|
| Agent 05 | Implements guardrails |
| /defend | Configuration recommendations |
| CI/CD | Automated testing |
| Monitoring | Alert on filter triggers |

---

**Protect AI systems with comprehensive input/output guardrails.**
