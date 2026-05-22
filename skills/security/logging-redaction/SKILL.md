---
name: Logging Redaction
description: Comprehensive guide to preventing PII and secrets from appearing in logs through redaction strategies, safe logging practices, and automated filtering.
---

# Logging Redaction

## Overview

Logging redaction is the practice of removing or masking sensitive information before it appears in logs. This is critical because:

- **PII in logs = Compliance violation** (GDPR, CCPA, HIPAA)
- **Secrets in logs = Security breach** (API keys, passwords, tokens)
- **Logs are long-lived** (often retained for months or years)
- **Logs are widely accessible** (developers, support, security teams)
- **Logs are often exported** (to third-party services like Datadog, Splunk)

**Golden Rule**: If you wouldn't want it in a public GitHub repo, don't log it.

## 1. Why Redaction Matters

### Compliance Violations

```
❌ BAD: Logging PII
2024-01-15 10:23:45 INFO User login: email=john.smith@example.com, ip=192.168.1.100

GDPR Article 32: "appropriate technical and organizational measures to ensure a level of security appropriate to the risk"
→ PII in logs = violation (logs are not encrypted, widely accessible)

Penalty: Up to €20 million or 4% of global revenue
```

### Security Breaches

```
❌ CRITICAL: Logging secrets
2024-01-15 10:23:45 INFO API request: Authorization=Bearer sk-1234567890abcdef

→ Anyone with log access now has your API key
→ If logs are exported to Datadog/Splunk, third parties have your secrets
→ If logs are in CloudWatch, anyone with AWS access can see them
```

### Real-World Incidents

1. **Uber (2016)**: Engineers logged AWS credentials, leading to breach of 57M records
2. **GitHub (2018)**: Passwords logged in plaintext in internal logs
3. **Facebook (2019)**: 600M passwords stored in plaintext in internal logs

## 2. What to Redact

### PII (Personally Identifiable Information)

```python
# ❌ DON'T LOG
logger.info(f"User {user.name} logged in from {user.email}")
logger.info(f"Processing order for {customer.phone}")
logger.info(f"Shipping to {address.street}, {address.city}")

# ✅ DO LOG (with redaction)
logger.info(f"User {user.id} logged in")  # Use ID, not name
logger.info(f"Processing order {order.id}")  # Use order ID
logger.info(f"Shipping to {address.country}")  # Only country, not full address
```

**PII to redact**:
- Names (first, last, full)
- Email addresses
- Phone numbers
- Physical addresses
- IP addresses (sometimes - depends on context)
- User agent strings (can fingerprint users)
- GPS coordinates
- Social Security Numbers
- Passport numbers
- Driver's license numbers

### Authentication & Secrets

```python
# ❌ NEVER LOG THESE
logger.info(f"Password: {password}")  # NEVER!
logger.info(f"API Key: {api_key}")  # NEVER!
logger.info(f"Token: {jwt_token}")  # NEVER!
logger.info(f"Session: {session_id}")  # NEVER!
logger.info(f"Authorization: {auth_header}")  # NEVER!

# ✅ DO LOG (without values)
logger.info("Password validation successful")
logger.info("API key validated")
logger.info("JWT token verified")
logger.info("Session created")
logger.info("Authorization header present")
```

**Secrets to redact**:
- Passwords (plaintext or hashed)
- API keys
- OAuth tokens
- JWT tokens
- Session IDs
- CSRF tokens
- Private keys
- Database credentials
- AWS access keys
- Encryption keys

### Financial Information

```python
# ❌ DON'T LOG
logger.info(f"Charging card {credit_card_number}")
logger.info(f"CVV: {cvv}")
logger.info(f"Bank account: {account_number}")

# ✅ DO LOG (masked)
logger.info(f"Charging card ending in {credit_card_number[-4:]}")
logger.info("CVV validated")
logger.info(f"Bank account ending in {account_number[-4:]}")
```

**Financial data to redact**:
- Credit card numbers (full PAN)
- CVV/CVC codes
- Bank account numbers
- Routing numbers
- IBAN
- Cryptocurrency private keys
- Transaction amounts (sometimes - depends on context)

### Healthcare Information (HIPAA PHI)

```python
# ❌ DON'T LOG
logger.info(f"Patient {patient.name} diagnosed with {diagnosis}")
logger.info(f"Prescription: {medication} for MRN {medical_record_number}")

# ✅ DO LOG (de-identified)
logger.info(f"Patient {patient.id} diagnosis recorded")
logger.info(f"Prescription created for patient {patient.id}")
```

**PHI to redact**:
- Patient names
- Medical record numbers
- Diagnoses
- Medications
- Lab results
- Insurance policy numbers

### Business Secrets

```python
# ❌ DON'T LOG
logger.info(f"Pricing algorithm: {algorithm_details}")
logger.info(f"Customer acquisition cost: ${cac}")
logger.info(f"Proprietary formula: {formula}")

# ✅ DO LOG (without details)
logger.info("Pricing calculated")
logger.info("CAC metrics updated")
logger.info("Formula applied")
```

## 3. Redaction Strategies

### Complete Removal

Replace sensitive data with a placeholder:

```python
# Before: "My email is john@example.com"
# After:  "My email is [REDACTED]"

def redact_email(text):
    return re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[REDACTED]', text)
```

**Pros**: Maximum privacy
**Cons**: Loses all information, can't correlate events

### Partial Masking

Show part of the data for debugging:

```python
# Before: "Card: 4532-1234-5678-9010"
# After:  "Card: ****-****-****-9010"

def mask_credit_card(card_number):
    return f"****-****-****-{card_number[-4:]}"

# Before: "Email: john.smith@example.com"
# After:  "Email: j***@example.com"

def mask_email(email):
    local, domain = email.split('@')
    return f"{local[0]}***@{domain}"
```

**Pros**: Retains some information for debugging
**Cons**: Still reveals partial data

### Hashing

Replace with consistent hash for correlation:

```python
import hashlib

def hash_pii(value, salt="your-secret-salt"):
    """Hash PII for consistent redaction."""
    return hashlib.sha256(f"{value}{salt}".encode()).hexdigest()[:16]

# Before: "User: john@example.com"
# After:  "User: a1b2c3d4e5f6g7h8"

# Same email always produces same hash
# Can correlate events for same user
# Cannot reverse hash to get original email
```

**Pros**: Allows correlation, irreversible
**Cons**: Rainbow table attacks possible without strong salt

### Tokenization

Replace with placeholder tokens:

```python
class Tokenizer:
    def __init__(self):
        self.token_map = {}
        self.reverse_map = {}
        self.counter = 0
    
    def tokenize(self, value):
        if value in self.token_map:
            return self.token_map[value]
        
        token = f"TOKEN_{self.counter}"
        self.counter += 1
        
        self.token_map[value] = token
        self.reverse_map[token] = value
        
        return token
    
    def detokenize(self, token):
        return self.reverse_map.get(token)

# Before: "Email: john@example.com"
# After:  "Email: TOKEN_0"

# Can reverse if needed (for authorized users)
```

**Pros**: Reversible (if needed), consistent
**Cons**: Must secure token map

## 4. Redaction Patterns

### Before Logging (Preferred)

Redact data before it reaches the logger:

```python
import logging

def safe_log_user_action(user, action):
    """Log user action with redacted PII."""
    logger.info(
        "User action",
        extra={
            'user_id': user.id,  # ✅ ID, not email
            'action': action,
            'timestamp': datetime.now().isoformat()
        }
    )
    # Email, name, phone are never logged

# Usage
safe_log_user_action(user, "login")
```

**Pros**: PII never enters logs
**Cons**: Requires discipline from all developers

### At Logging Time (Middleware)

Use logging filters to redact automatically:

```python
import logging
import re

class PIIRedactionFilter(logging.Filter):
    """Redact PII from log records."""
    
    EMAIL_PATTERN = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    PHONE_PATTERN = re.compile(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b')
    SSN_PATTERN = re.compile(r'\b\d{3}-\d{2}-\d{4}\b')
    CC_PATTERN = re.compile(r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b')
    
    def filter(self, record):
        # Redact message
        if isinstance(record.msg, str):
            record.msg = self.redact(record.msg)
        
        # Redact args
        if record.args:
            record.args = tuple(
                self.redact(str(arg)) if isinstance(arg, str) else arg
                for arg in record.args
            )
        
        return True
    
    def redact(self, text):
        text = self.EMAIL_PATTERN.sub('[EMAIL_REDACTED]', text)
        text = self.PHONE_PATTERN.sub('[PHONE_REDACTED]', text)
        text = self.SSN_PATTERN.sub('[SSN_REDACTED]', text)
        text = self.CC_PATTERN.sub('[CC_REDACTED]', text)
        return text

# Setup
logger = logging.getLogger(__name__)
logger.addFilter(PIIRedactionFilter())

# Usage
logger.info("User email: john@example.com")  # Logged as "User email: [EMAIL_REDACTED]"
```

**Pros**: Automatic, catches mistakes
**Cons**: Performance overhead, may miss context

### After Logging (Log Processors)

Process logs after they're written:

```python
# Logstash filter (ELK stack)
filter {
  mutate {
    gsub => [
      "message", "\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "[EMAIL_REDACTED]",
      "message", "\b\d{3}-\d{2}-\d{4}\b", "[SSN_REDACTED]"
    ]
  }
}
```

**Pros**: Centralized, can update rules without code changes
**Cons**: PII still written to disk initially

### At Query Time (Least Preferred)

Redact when viewing logs:

```python
# CloudWatch Insights query
fields @timestamp, @message
| filter @message like /ERROR/
| replace @message, /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/, "[EMAIL_REDACTED]"
```

**Pros**: Original data preserved (if needed)
**Cons**: PII still stored, accessible to anyone with log access

## 5. Application-Level Redaction

### Structured Logging with Redaction

```python
import logging
import json

class RedactingJSONFormatter(logging.Formatter):
    """JSON formatter with automatic PII redaction."""
    
    SENSITIVE_KEYS = {
        'password', 'token', 'api_key', 'secret', 'authorization',
        'ssn', 'credit_card', 'cvv', 'pin'
    }
    
    def format(self, record):
        log_data = {
            'timestamp': self.formatTime(record),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
        }
        
        # Add extra fields
        if hasattr(record, 'extra'):
            log_data.update(self.redact_dict(record.extra))
        
        return json.dumps(log_data)
    
    def redact_dict(self, data):
        """Recursively redact sensitive keys."""
        if isinstance(data, dict):
            return {
                k: '[REDACTED]' if k.lower() in self.SENSITIVE_KEYS else self.redact_dict(v)
                for k, v in data.items()
            }
        elif isinstance(data, list):
            return [self.redact_dict(item) for item in data]
        else:
            return data

# Setup
handler = logging.StreamHandler()
handler.setFormatter(RedactingJSONFormatter())

logger = logging.getLogger(__name__)
logger.addHandler(handler)

# Usage
logger.info("User login", extra={
    'user_id': 123,
    'email': 'john@example.com',  # Will be redacted if in SENSITIVE_KEYS
    'password': 'secret123'  # Will be redacted
})
```

### Safe-by-Default Logging

```python
from typing import Any, Dict
import logging

class SafeLogger:
    """Logger that redacts PII by default."""
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
    
    def info(self, message: str, **kwargs):
        """Log info with automatic redaction."""
        safe_kwargs = self._redact_kwargs(kwargs)
        self.logger.info(message, extra=safe_kwargs)
    
    def error(self, message: str, exc_info=None, **kwargs):
        """Log error with automatic redaction."""
        safe_kwargs = self._redact_kwargs(kwargs)
        
        # Redact exception messages
        if exc_info:
            exc_info = self._redact_exception(exc_info)
        
        self.logger.error(message, exc_info=exc_info, extra=safe_kwargs)
    
    def _redact_kwargs(self, kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """Redact sensitive data from kwargs."""
        redacted = {}
        
        for key, value in kwargs.items():
            # Redact based on key name
            if any(sensitive in key.lower() for sensitive in ['password', 'token', 'secret', 'key']):
                redacted[key] = '[REDACTED]'
            # Redact based on value pattern
            elif isinstance(value, str):
                redacted[key] = self._redact_string(value)
            else:
                redacted[key] = value
        
        return redacted
    
    def _redact_string(self, value: str) -> str:
        """Redact PII patterns from string."""
        # Email
        value = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', value)
        # Phone
        value = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[PHONE]', value)
        # SSN
        value = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[SSN]', value)
        return value
    
    def _redact_exception(self, exc_info):
        """Redact PII from exception messages."""
        # This is complex - exceptions can contain PII in messages
        # For now, just return as-is, but in production you'd want to redact
        return exc_info

# Usage
logger = SafeLogger(__name__)
logger.info("User action", user_id=123, email="john@example.com")  # email redacted
```

## 6. Redaction Libraries

### Python: pino-redaction (for Node.js)

```javascript
const pino = require('pino');

const logger = pino({
  redact: {
    paths: [
      'req.headers.authorization',
      'req.headers.cookie',
      'req.body.password',
      'req.body.email',
      'res.headers["set-cookie"]'
    ],
    censor: '[REDACTED]'
  }
});

// Usage
logger.info({
  req: {
    headers: {
      authorization: 'Bearer secret-token'  // Will be redacted
    },
    body: {
      email: 'john@example.com',  // Will be redacted
      name: 'John'  // Not redacted
    }
  }
});
```

### Node.js: winston-redact

```javascript
const winston = require('winston');
const redact = require('winston-redact');

const logger = winston.createLogger({
  format: winston.format.combine(
    redact({
      paths: ['password', 'email', 'ssn', '*.token'],
      censor: '[REDACTED]'
    }),
    winston.format.json()
  ),
  transports: [new winston.transports.Console()]
});

// Usage
logger.info({
  user: 'john',
  password: 'secret123',  // Will be redacted
  email: 'john@example.com'  // Will be redacted
});
```

### Go: zap with custom encoders

```go
package main

import (
    "go.uber.org/zap"
    "go.uber.org/zap/zapcore"
    "regexp"
)

func redactString(s string) string {
    emailRegex := regexp.MustCompile(`\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b`)
    return emailRegex.ReplaceAllString(s, "[EMAIL_REDACTED]")
}

type redactingEncoder struct {
    zapcore.Encoder
}

func (e *redactingEncoder) EncodeEntry(entry zapcore.Entry, fields []zapcore.Field) (*buffer.Buffer, error) {
    // Redact entry message
    entry.Message = redactString(entry.Message)
    
    // Redact fields
    for i := range fields {
        if fields[i].Type == zapcore.StringType {
            fields[i].String = redactString(fields[i].String)
        }
    }
    
    return e.Encoder.EncodeEntry(entry, fields)
}

func main() {
    config := zap.NewProductionConfig()
    logger, _ := config.Build()
    
    logger.Info("User email: john@example.com")  // Will be redacted
}
```

## 7. Log Aggregation Redaction

### Datadog: Sensitive Data Scanner

```yaml
# Datadog sensitive data scanner rules
rules:
  - name: "Redact Email Addresses"
    pattern: '\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    replacement: "[EMAIL_REDACTED]"
    
  - name: "Redact Credit Cards"
    pattern: '\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b'
    replacement: "[CC_REDACTED]"
    
  - name: "Redact API Keys"
    pattern: 'sk-[a-zA-Z0-9]{32}'
    replacement: "[API_KEY_REDACTED]"
```

### Splunk: Data Anonymization

```conf
# props.conf
[source::*/application.log]
SEDCMD-redact_email = s/\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/[EMAIL_REDACTED]/g
SEDCMD-redact_ssn = s/\b\d{3}-\d{2}-\d{4}\b/[SSN_REDACTED]/g
SEDCMD-redact_cc = s/\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b/[CC_REDACTED]/g
```

### ELK: Logstash Filters

```ruby
# logstash.conf
filter {
  # Redact emails
  mutate {
    gsub => [
      "message", "\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "[EMAIL_REDACTED]"
    ]
  }
  
  # Redact credit cards
  mutate {
    gsub => [
      "message", "\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b", "[CC_REDACTED]"
    ]
  }
  
  # Redact SSN
  mutate {
    gsub => [
      "message", "\b\d{3}-\d{2}-\d{4}\b", "[SSN_REDACTED]"
    ]
  }
  
  # Remove sensitive fields entirely
  mutate {
    remove_field => ["password", "api_key", "token"]
  }
}
```

### CloudWatch: Logs Insights Redaction

```sql
-- Query with redaction
fields @timestamp, @message
| filter @message like /ERROR/
| replace @message, /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/, "[EMAIL_REDACTED]"
| replace @message, /\b\d{3}-\d{2}-\d{4}\b/, "[SSN_REDACTED]"
```

## 8. Configuration-Driven Redaction

### JSON Path Redaction

```python
import json
from jsonpath_ng import parse

class JSONPathRedactor:
    """Redact specific JSON paths."""
    
    def __init__(self, paths_to_redact):
        self.paths = [parse(path) for path in paths_to_redact]
    
    def redact(self, data):
        """Redact specified paths in JSON data."""
        data_copy = json.loads(json.dumps(data))  # Deep copy
        
        for path in self.paths:
            for match in path.find(data_copy):
                # Replace value with [REDACTED]
                self._set_value(data_copy, match.full_path, '[REDACTED]')
        
        return data_copy
    
    def _set_value(self, data, path, value):
        """Set value at path."""
        # Implementation depends on jsonpath library
        pass

# Configuration
redactor = JSONPathRedactor([
    '$.user.email',
    '$.user.phone',
    '$.payment.card_number',
    '$.headers.authorization'
])

# Usage
log_data = {
    'user': {
        'id': 123,
        'email': 'john@example.com',  # Will be redacted
        'phone': '555-1234'  # Will be redacted
    },
    'payment': {
        'amount': 100,
        'card_number': '4532-1234-5678-9010'  # Will be redacted
    }
}

redacted = redactor.redact(log_data)
logger.info(json.dumps(redacted))
```

### Field Name Patterns

```python
class FieldPatternRedactor:
    """Redact fields based on name patterns."""
    
    SENSITIVE_PATTERNS = [
        r'.*password.*',
        r'.*token.*',
        r'.*secret.*',
        r'.*api[_-]?key.*',
        r'.*auth.*',
        r'.*ssn.*',
        r'.*credit[_-]?card.*',
    ]
    
    def should_redact(self, field_name):
        """Check if field should be redacted."""
        field_lower = field_name.lower()
        return any(
            re.match(pattern, field_lower)
            for pattern in self.SENSITIVE_PATTERNS
        )
    
    def redact_dict(self, data):
        """Recursively redact sensitive fields."""
        if isinstance(data, dict):
            return {
                k: '[REDACTED]' if self.should_redact(k) else self.redact_dict(v)
                for k, v in data.items()
            }
        elif isinstance(data, list):
            return [self.redact_dict(item) for item in data]
        else:
            return data

# Usage
redactor = FieldPatternRedactor()
log_data = {
    'user_id': 123,
    'user_password': 'secret',  # Redacted
    'api_key': 'sk-123',  # Redacted
    'email': 'john@example.com'  # Not redacted (add pattern if needed)
}

redacted = redactor.redact_dict(log_data)
```

### Regex Patterns Configuration

```yaml
# redaction-config.yaml
redaction_rules:
  - name: email
    pattern: '\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    replacement: '[EMAIL_REDACTED]'
    
  - name: phone
    pattern: '\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
    replacement: '[PHONE_REDACTED]'
    
  - name: ssn
    pattern: '\b\d{3}-\d{2}-\d{4}\b'
    replacement: '[SSN_REDACTED]'
    
  - name: credit_card
    pattern: '\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b'
    replacement: '[CC_REDACTED]'
    
  - name: api_key
    pattern: 'sk-[a-zA-Z0-9]{32}'
    replacement: '[API_KEY_REDACTED]'
```

```python
import yaml
import re

class ConfigurableRedactor:
    """Redactor with configurable rules."""
    
    def __init__(self, config_path):
        with open(config_path) as f:
            config = yaml.safe_load(f)
        
        self.rules = [
            {
                'name': rule['name'],
                'pattern': re.compile(rule['pattern']),
                'replacement': rule['replacement']
            }
            for rule in config['redaction_rules']
        ]
    
    def redact(self, text):
        """Apply all redaction rules."""
        for rule in self.rules:
            text = rule['pattern'].sub(rule['replacement'], text)
        return text

# Usage
redactor = ConfigurableRedactor('redaction-config.yaml')
text = "Email john@example.com, phone 555-1234, SSN 123-45-6789"
redacted = redactor.redact(text)
# "Email [EMAIL_REDACTED], phone [PHONE_REDACTED], SSN [SSN_REDACTED]"
```

## 9. Performance Considerations

### Redaction Overhead

```python
import time

def benchmark_redaction():
    """Benchmark redaction performance."""
    text = "User john@example.com called from 555-1234" * 1000
    
    # No redaction
    start = time.time()
    for _ in range(1000):
        logger.info(text)
    no_redaction_time = time.time() - start
    
    # With redaction
    start = time.time()
    for _ in range(1000):
        redacted = redactor.redact(text)
        logger.info(redacted)
    redaction_time = time.time() - start
    
    overhead = ((redaction_time - no_redaction_time) / no_redaction_time) * 100
    print(f"Redaction overhead: {overhead:.2f}%")

# Typical overhead: 5-20% depending on complexity
```

### Caching Redaction Decisions

```python
from functools import lru_cache

class CachedRedactor:
    """Redactor with caching for performance."""
    
    @lru_cache(maxsize=10000)
    def redact(self, text):
        """Redact with caching."""
        # Expensive regex operations
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', text)
        text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[PHONE]', text)
        return text

# For repeated log messages, cache hit avoids regex
```

### Sampling vs Full Redaction

```python
import random

class SamplingRedactor:
    """Redact only a sample of logs for performance."""
    
    def __init__(self, sample_rate=0.1):
        self.sample_rate = sample_rate
        self.full_redactor = FullRedactor()
    
    def should_redact(self):
        """Decide if this log should be redacted."""
        return random.random() < self.sample_rate
    
    def redact(self, text):
        """Redact based on sampling."""
        if self.should_redact():
            return self.full_redactor.redact(text)
        else:
            # Skip redaction for performance
            # WARNING: Some PII may leak!
            return text

# Trade-off: Performance vs completeness
# Only use if you can tolerate some PII leakage
```

## 10. Testing Redaction

### Unit Tests with PII Samples

```python
import unittest

class TestRedaction(unittest.TestCase):
    def setUp(self):
        self.redactor = PIIRedactor()
    
    def test_email_redaction(self):
        text = "Contact john@example.com"
        redacted = self.redactor.redact(text)
        self.assertNotIn("john@example.com", redacted)
        self.assertIn("[EMAIL_REDACTED]", redacted)
    
    def test_phone_redaction(self):
        text = "Call 555-123-4567"
        redacted = self.redactor.redact(text)
        self.assertNotIn("555-123-4567", redacted)
        self.assertIn("[PHONE_REDACTED]", redacted)
    
    def test_ssn_redaction(self):
        text = "SSN: 123-45-6789"
        redacted = self.redactor.redact(text)
        self.assertNotIn("123-45-6789", redacted)
        self.assertIn("[SSN_REDACTED]", redacted)
    
    def test_credit_card_redaction(self):
        text = "Card: 4532-1234-5678-9010"
        redacted = self.redactor.redact(text)
        self.assertNotIn("4532-1234-5678-9010", redacted)
        self.assertIn("[CC_REDACTED]", redacted)
    
    def test_multiple_pii_types(self):
        text = "User john@example.com, phone 555-1234, SSN 123-45-6789"
        redacted = self.redactor.redact(text)
        self.assertNotIn("john@example.com", redacted)
        self.assertNotIn("555-1234", redacted)
        self.assertNotIn("123-45-6789", redacted)
    
    def test_no_false_positives(self):
        text = "The price is $123.45"
        redacted = self.redactor.redact(text)
        self.assertIn("$123.45", redacted)  # Should not be redacted
```

### Log Review Audits

```python
def audit_logs_for_pii(log_file):
    """Audit log file for PII leakage."""
    pii_detector = PIIDetector()
    findings = []
    
    with open(log_file) as f:
        for line_num, line in enumerate(f, 1):
            pii_found = pii_detector.detect(line)
            if pii_found:
                findings.append({
                    'line': line_num,
                    'pii_types': [p['type'] for p in pii_found],
                    'snippet': line[:100]
                })
    
    if findings:
        print(f"⚠️  PII FOUND IN LOGS!")
        for finding in findings:
            print(f"Line {finding['line']}: {finding['pii_types']}")
    else:
        print("✅ No PII found in logs")
    
    return findings

# Run as part of CI/CD
audit_logs_for_pii('/var/log/application.log')
```

### Automated PII Detection in Logs

```python
# Pre-commit hook to detect PII in code
#!/usr/bin/env python3

import sys
import re

def check_for_pii_in_logging():
    """Check if code logs PII."""
    pii_patterns = [
        (r'logger\..*\(.*email.*\)', 'Logging email'),
        (r'logger\..*\(.*password.*\)', 'Logging password'),
        (r'logger\..*\(.*ssn.*\)', 'Logging SSN'),
        (r'logger\..*\(.*credit.*card.*\)', 'Logging credit card'),
    ]
    
    errors = []
    
    for file in sys.argv[1:]:
        with open(file) as f:
            for line_num, line in enumerate(f, 1):
                for pattern, message in pii_patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        errors.append(f"{file}:{line_num} - {message}")
    
    if errors:
        print("❌ PII logging detected:")
        for error in errors:
            print(f"  {error}")
        sys.exit(1)
    
    sys.exit(0)

if __name__ == '__main__':
    check_for_pii_in_logging()
```

## 11. Redaction for Different Log Types

### Application Logs

```python
# ❌ DON'T
logger.info(f"User {user.email} performed {action}")

# ✅ DO
logger.info(f"User {user.id} performed {action}")
```

### Access Logs

```nginx
# nginx access log format (redact IP addresses?)
log_format redacted '$remote_addr_redacted - $remote_user [$time_local] '
                    '"$request" $status $body_bytes_sent '
                    '"$http_referer" "$http_user_agent"';

# Use nginx module to redact last octet of IP
map $remote_addr $remote_addr_redacted {
    ~(?P<ip>\d+\.\d+\.\d+)\.\d+ $ip.0;
    default 0.0.0.0;
}
```

### Database Query Logs

```python
# ❌ DON'T log full queries with parameters
logger.info(f"Query: SELECT * FROM users WHERE email = '{email}'")

# ✅ DO log parameterized queries
logger.info(f"Query: SELECT * FROM users WHERE email = ?", extra={'params': '[REDACTED]'})
```

### Audit Logs

```python
# Audit logs need selective redaction
# Keep: Who, what, when, where
# Redact: Sensitive values

def log_audit_event(user_id, action, resource, old_value, new_value):
    """Log audit event with selective redaction."""
    logger.info(
        "Audit event",
        extra={
            'user_id': user_id,  # Keep
            'action': action,  # Keep
            'resource': resource,  # Keep
            'old_value': redact_if_sensitive(old_value),  # Conditional
            'new_value': redact_if_sensitive(new_value),  # Conditional
            'timestamp': datetime.now().isoformat()  # Keep
        }
    )

def redact_if_sensitive(value):
    """Redact if value is sensitive."""
    if is_pii(value):
        return '[REDACTED]'
    return value
```

### Error Logs

```python
# ❌ DON'T log full exception with user input
try:
    process_payment(card_number, cvv)
except Exception as e:
    logger.error(f"Payment failed: {e}")  # May contain card_number!

# ✅ DO redact exception messages
try:
    process_payment(card_number, cvv)
except Exception as e:
    safe_message = redactor.redact(str(e))
    logger.error(f"Payment failed: {safe_message}")
```

## 12. Trade-offs

### Debugging vs Privacy

```
More Redaction = More Privacy, Less Debuggability
Less Redaction = Less Privacy, More Debuggability

Solution: Tiered logging
- Production: Heavy redaction
- Staging: Moderate redaction
- Development: Light redaction (but still redact secrets!)
```

### Correlation vs Security

```python
# Option 1: Complete redaction (no correlation)
logger.info("User logged in")  # Can't correlate with other events

# Option 2: Hashed PII (allows correlation)
user_hash = hash_pii(user.email)
logger.info(f"User {user_hash} logged in")  # Can correlate same user

# Option 3: User ID (best of both worlds)
logger.info(f"User {user.id} logged in")  # Can correlate, no PII
```

### Performance vs Completeness

```
Full redaction on every log = Slow
Sampling redaction = Fast but incomplete
Async redaction = Fast but complex

Solution: Async redaction with queue
- Log to queue immediately (fast)
- Redact in background worker (complete)
- Write redacted logs to storage
```

## 13. Redaction Policies

### What Gets Redacted

```yaml
# redaction-policy.yaml
always_redact:
  - passwords
  - api_keys
  - tokens
  - credit_cards
  - ssn
  - passport_numbers

conditionally_redact:
  - email: production_only
  - phone: production_only
  - ip_address: depends_on_use_case

never_redact:
  - user_id
  - timestamps
  - error_codes
  - http_status_codes
```

### What Stays (for Debugging)

```python
# Keep these for debugging
logger.info(
    "Payment failed",
    extra={
        'user_id': user.id,  # ✅ Keep
        'order_id': order.id,  # ✅ Keep
        'amount': amount,  # ✅ Keep (not PII)
        'currency': currency,  # ✅ Keep
        'error_code': error_code,  # ✅ Keep
        'card_last_4': card_number[-4:],  # ✅ Keep (partial)
        'card_full': '[REDACTED]',  # ❌ Redact
        'cvv': '[REDACTED]',  # ❌ Redact
    }
)
```

### Retention After Redaction

```
Original logs (with PII): Delete after 30 days
Redacted logs: Retain for 1 year
Aggregated metrics: Retain indefinitely
```

## 14. Common Mistakes

### Logging request.body Without Redaction

```python
# ❌ CRITICAL MISTAKE
@app.route('/api/login', methods=['POST'])
def login():
    logger.info(f"Login request: {request.json}")  # Contains password!
    # ...

# ✅ CORRECT
@app.route('/api/login', methods=['POST'])
def login():
    safe_body = {k: v for k, v in request.json.items() if k != 'password'}
    logger.info(f"Login request: {safe_body}")
    # ...
```

### Exception Messages with User Input

```python
# ❌ MISTAKE
def process_user(email):
    if not is_valid_email(email):
        raise ValueError(f"Invalid email: {email}")  # Email in exception!

# ✅ CORRECT
def process_user(email):
    if not is_valid_email(email):
        raise ValueError("Invalid email format")  # No PII
```

### SQL Queries with Parameters

```python
# ❌ MISTAKE
query = f"SELECT * FROM users WHERE email = '{email}'"
logger.info(f"Executing: {query}")  # Email in log!

# ✅ CORRECT
query = "SELECT * FROM users WHERE email = ?"
logger.info(f"Executing: {query}", extra={'params': '[REDACTED]'})
```

### API Responses with Full User Objects

```python
# ❌ MISTAKE
logger.info(f"API response: {json.dumps(user.__dict__)}")  # All PII!

# ✅ CORRECT
logger.info(f"API response for user {user.id}")  # Just ID
```

## 15. Implementation Examples

### Complete Python Implementation

```python
import logging
import re
import json
from typing import Any, Dict

class ProductionLogger:
    """Production-ready logger with comprehensive redaction."""
    
    # Regex patterns
    EMAIL_PATTERN = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    PHONE_PATTERN = re.compile(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b')
    SSN_PATTERN = re.compile(r'\b\d{3}-\d{2}-\d{4}\b')
    CC_PATTERN = re.compile(r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b')
    API_KEY_PATTERN = re.compile(r'sk-[a-zA-Z0-9]{32}')
    
    # Sensitive field names
    SENSITIVE_KEYS = {
        'password', 'token', 'api_key', 'secret', 'authorization',
        'ssn', 'credit_card', 'cvv', 'pin', 'private_key'
    }
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self._setup_logger()
    
    def _setup_logger(self):
        """Setup logger with JSON formatting."""
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
    
    def info(self, message: str, **kwargs):
        """Log info with redaction."""
        self._log('INFO', message, kwargs)
    
    def error(self, message: str, exc_info=None, **kwargs):
        """Log error with redaction."""
        if exc_info:
            kwargs['error'] = str(exc_info)
        self._log('ERROR', message, kwargs)
    
    def _log(self, level: str, message: str, extra: Dict[str, Any]):
        """Internal log method with redaction."""
        log_entry = {
            'level': level,
            'message': self._redact_string(message),
            'extra': self._redact_dict(extra)
        }
        
        self.logger.info(json.dumps(log_entry))
    
    def _redact_string(self, text: str) -> str:
        """Redact PII patterns from string."""
        if not isinstance(text, str):
            return text
        
        text = self.EMAIL_PATTERN.sub('[EMAIL]', text)
        text = self.PHONE_PATTERN.sub('[PHONE]', text)
        text = self.SSN_PATTERN.sub('[SSN]', text)
        text = self.CC_PATTERN.sub('[CC]', text)
        text = self.API_KEY_PATTERN.sub('[API_KEY]', text)
        
        return text
    
    def _redact_dict(self, data: Any) -> Any:
        """Recursively redact sensitive data."""
        if isinstance(data, dict):
            return {
                k: '[REDACTED]' if k.lower() in self.SENSITIVE_KEYS else self._redact_dict(v)
                for k, v in data.items()
            }
        elif isinstance(data, list):
            return [self._redact_dict(item) for item in data]
        elif isinstance(data, str):
            return self._redact_string(data)
        else:
            return data

# Usage
logger = ProductionLogger(__name__)

logger.info("User login", user_id=123, email="john@example.com")
# Output: {"level": "INFO", "message": "User login", "extra": {"user_id": 123, "email": "[EMAIL]"}}

logger.error("Payment failed", card_number="4532-1234-5678-9010", cvv="123")
# Output: {"level": "ERROR", "message": "Payment failed", "extra": {"card_number": "[CC]", "cvv": "[REDACTED]"}}
```

### Complete Node.js Implementation

```javascript
const pino = require('pino');

// Custom redaction function
function redactPII(value) {
  if (typeof value !== 'string') return value;
  
  // Email
  value = value.replace(/\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/g, '[EMAIL]');
  // Phone
  value = value.replace(/\b\d{3}[-.]?\d{3}[-.]?\d{4}\b/g, '[PHONE]');
  // SSN
  value = value.replace(/\b\d{3}-\d{2}-\d{4}\b/g, '[SSN]');
  // Credit card
  value = value.replace(/\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b/g, '[CC]');
  
  return value;
}

const logger = pino({
  redact: {
    paths: [
      'req.headers.authorization',
      'req.headers.cookie',
      'req.body.password',
      'req.body.api_key',
      'res.headers["set-cookie"]'
    ],
    censor: '[REDACTED]'
  },
  serializers: {
    req: (req) => ({
      method: req.method,
      url: req.url,
      headers: req.headers,
      body: redactPII(JSON.stringify(req.body))
    }),
    res: (res) => ({
      statusCode: res.statusCode,
      headers: res.headers
    })
  }
});

// Usage
logger.info({
  user_id: 123,
  email: 'john@example.com',  // Will be redacted
  action: 'login'
});

module.exports = logger;
```

## Best Practices

1. **Redact Before Logging**: Prevent PII from ever entering logs
2. **Use Structured Logging**: Easier to redact specific fields
3. **Automate Redaction**: Use filters/middleware, don't rely on developers
4. **Test Redaction**: Unit tests with PII samples
5. **Audit Logs Regularly**: Scan for PII leakage
6. **Use IDs, Not PII**: Log user_id instead of email
7. **Partial Masking**: Show last 4 digits of card for debugging
8. **Hash for Correlation**: Use consistent hashes to correlate events
9. **Tiered Redaction**: More redaction in production, less in dev
10. **Document Policies**: Clear guidelines on what to redact

## Common Pitfalls

- **Logging Full Request Bodies**: Often contain passwords, tokens
- **Exception Messages**: Can contain user input with PII
- **SQL Queries**: Parameters may contain PII
- **API Responses**: Full user objects contain PII
- **Not Redacting Logs in Third-Party Services**: Datadog, Splunk also need redaction
- **Forgetting About Backups**: Redact logs before backup
- **No Redaction in Development**: Secrets can still leak

## Summary

Logging redaction is essential for compliance and security. Implement multi-layered redaction (before logging, at logging time, after logging) to ensure PII and secrets never appear in logs. Use structured logging with automatic redaction, test thoroughly, and audit logs regularly for leakage.
