---
name: pii-redaction
description: Automatically applies when logging sensitive data. Ensures PII (phone numbers, emails, IDs, payment data) is redacted in all logs and outputs for compliance.
---

# PII Redaction Enforcer

When you are writing code that logs or outputs:
- Phone numbers (mobile, landline)
- Email addresses
- User IDs / Subscriber IDs
- Payment tokens / Credit card numbers
- Social Security Numbers / Tax IDs
- Physical addresses
- Names (in sensitive contexts)
- IP addresses (in some jurisdictions)
- Any other personally identifiable information

**Always redact PII in logs, error messages, and debug output.**

## ✅ Correct Pattern

```python
import logging
import re

logger = logging.getLogger(__name__)

def redact_pii(value: str, show_last: int = 4) -> str:
    """
    Redact PII showing only last N characters.

    Args:
        value: String to redact
        show_last: Number of characters to show (default: 4)

    Returns:
        Redacted string (e.g., "***5678")
    """
    if not value or len(value) <= show_last:
        return "***"
    return f"***{value[-show_last:]}"

def redact_email(email: str) -> str:
    """
    Redact email preserving domain.

    Args:
        email: Email address to redact

    Returns:
        Redacted email (e.g., "u***r@example.com")
    """
    if not email or '@' not in email:
        return "***"

    local, domain = email.split('@', 1)
    if len(local) <= 2:
        return f"***@{domain}"

    return f"{local[0]}***{local[-1]}@{domain}"

# Usage in logging
logger.info(f"Processing user | subscriber_id={redact_pii(subscriber_id)}")
logger.info(f"Payment received | token={redact_pii(payment_token)} | user={redact_email(email)}")
logger.info(f"Order created | phone={redact_pii(phone_number)}")
```

**Output:**
```
Processing user | subscriber_id=***5678
Payment received | token=***2344 | user=u***r@example.com
Order created | phone=***1234
```

## ❌ Incorrect Pattern (PII Leak)

```python
# ❌ Full PII exposed
logger.info(f"Processing subscriber_id: {subscriber_id}")
logger.info(f"User email: {email}")
logger.info(f"Phone: {phone_number}")

# ❌ PII in error messages
raise ValueError(f"Invalid subscriber ID: {subscriber_id}")

# ❌ PII in API responses (should only redact in logs)
return {"error": f"User {email} not found"}  # OK in response, but log should redact

# ❌ Insufficient redaction
logger.info(f"Phone: {phone_number[:3]}****")  # Shows area code - still PII!
```

## Redaction Helper Functions

```python
import re
from typing import Optional

class PIIRedactor:
    """Helper class for consistent PII redaction."""

    @staticmethod
    def phone(phone: str, show_last: int = 4) -> str:
        """Redact phone number."""
        digits = re.sub(r'\D', '', phone)
        if len(digits) <= show_last:
            return "***"
        return f"***{digits[-show_last:]}"

    @staticmethod
    def email(email: str) -> str:
        """Redact email preserving domain."""
        if not email or '@' not in email:
            return "***"

        local, domain = email.split('@', 1)
        if len(local) <= 2:
            return f"***@{domain}"

        return f"{local[0]}***{local[-1]}@{domain}"

    @staticmethod
    def card_number(card: str, show_last: int = 4) -> str:
        """Redact credit card number."""
        digits = re.sub(r'\D', '', card)
        if len(digits) <= show_last:
            return "***"
        return f"***{digits[-show_last:]}"

    @staticmethod
    def ssn(ssn: str) -> str:
        """Redact SSN completely."""
        return "***-**-****"

    @staticmethod
    def address(address: str) -> str:
        """Redact street address, keep city/state."""
        # Example: "123 Main St, Boston, MA" -> "*** Main St, Boston, MA"
        parts = address.split(',')
        if parts:
            street = parts[0]
            # Redact house number but keep street name
            street_redacted = re.sub(r'^\d+', '***', street)
            parts[0] = street_redacted
        return ','.join(parts)

    @staticmethod
    def generic(value: str, show_last: int = 4) -> str:
        """Generic redaction for any string."""
        if not value or len(value) <= show_last:
            return "***"
        return f"***{value[-show_last:]}"

# Usage
redactor = PIIRedactor()
logger.info(f"User phone: {redactor.phone('555-123-4567')}")
logger.info(f"User email: {redactor.email('john.doe@example.com')}")
logger.info(f"Card: {redactor.card_number('4111-1111-1111-1111')}")
```

## When to Redact

**Always redact in:**
- ✅ Log statements (`logger.info`, `logger.debug`, `logger.error`)
- ✅ Audit logs
- ✅ Error messages (logs)
- ✅ Monitoring/observability data (OTEL, metrics)
- ✅ Debug output
- ✅ Stack traces (if they contain PII)

**Don't redact in:**
- ❌ Actual API calls (need full data)
- ❌ Database queries (need full data)
- ❌ Function parameters (internal use)
- ❌ Return values to authorized clients
- ❌ Encrypted storage
- ❌ Secure internal processing

**Context matters:**
```python
# ❌ Bad: Redacting in business logic
def send_email(email: str):
    send_to(redact_email(email))  # Wrong! Need real email to send!

# ✅ Good: Redacting in logs
def send_email(email: str):
    logger.info(f"Sending email to {redact_email(email)}")  # Log: redacted
    send_to(email)  # Actual operation: full email
```

## Structured Logging with Redaction

```python
import logging
import structlog

# Configure structlog with redaction
def redact_processor(logger, method_name, event_dict):
    """Processor to redact PII fields."""
    pii_fields = ['email', 'phone', 'ssn', 'card_number', 'subscriber_id']

    for field in pii_fields:
        if field in event_dict:
            if field == 'email':
                event_dict[field] = PIIRedactor.email(event_dict[field])
            else:
                event_dict[field] = PIIRedactor.generic(event_dict[field])

    return event_dict

structlog.configure(
    processors=[
        redact_processor,
        structlog.processors.JSONRenderer()
    ]
)

logger = structlog.get_logger()

# Usage - automatic redaction
logger.info("user_action", email="user@example.com", phone="555-1234")
# Output: {"event": "user_action", "email": "u***r@example.com", "phone": "***1234"}
```

## Compliance Considerations

**GDPR (EU):**
- Personal data must be protected
- Logs are considered data processing
- Must have legal basis for logging PII
- Right to be forgotten applies to logs

**CCPA (California):**
- Consumer personal information must be protected
- Includes identifiers, browsing history, biometric data

**PCI-DSS (Payment Cards):**
- Never log full card numbers (PAN)
- Never log CVV/CVV2
- Card holder name is sensitive too
- Mask PAN when displayed (show last 4 only)

**HIPAA (Healthcare):**
- PHI (Protected Health Information) must be secured
- Includes names, addresses, dates, phone numbers
- Medical record numbers, device identifiers

```python
# PCI-DSS compliant logging
def process_payment(card_number: str, cvv: str, amount: Decimal):
    """
    Process payment transaction.

    Security Note:
        PCI-DSS compliant. Never logs full card number or CVV.
    """
    # ✅ Redact card number in logs
    logger.info(
        f"Processing payment | "
        f"card={redact_pii(card_number, show_last=4)} | "
        f"amount={amount}"
        # ✅ NEVER log CVV
    )

    # Process with full data
    result = payment_gateway.charge(card_number, cvv, amount)

    # ✅ Redact in audit log
    logger.info(
        f"AUDIT: Payment processed | "
        f"card={redact_pii(card_number, show_last=4)} | "
        f"amount={amount} | "
        f"status={result.status}"
    )

    return result
```

## Testing Redaction

```python
import pytest

def test_redact_phone():
    """Test phone redaction."""
    assert redact_pii("5551234567") == "***4567"
    assert redact_pii("555-123-4567") == "***4567"

def test_redact_email():
    """Test email redaction."""
    assert redact_email("user@example.com") == "u***r@example.com"
    assert redact_email("a@example.com") == "***@example.com"

def test_redact_empty():
    """Test empty string handling."""
    assert redact_pii("") == "***"
    assert redact_pii(None) == "***"

def test_log_redaction(caplog):
    """Test that logs contain redacted PII."""
    with caplog.at_level(logging.INFO):
        user_id = "user_12345678"
        logger.info(f"Processing user={redact_pii(user_id)}")

    assert "***5678" in caplog.text
    assert "user_12345678" not in caplog.text
```

## ❌ Anti-Patterns

```python
# ❌ Not redacting at all
logger.info(f"User {user_id} logged in from {ip_address}")

# ❌ Inconsistent redaction
logger.info(f"User: ***{user_id[-4:]}")  # Different format each time
logger.debug(f"User: {user_id[:4]}****")

# ❌ Insufficient redaction
logger.info(f"Email: {email[0]}****")  # Just first letter isn't enough

# ❌ Redacting too much (lost debugability)
logger.info("User logged in")  # No identifier at all - can't debug!

# ✅ Better: Redact but keep debugability
logger.info(f"User logged in | user_id={redact_pii(user_id)}")

# ❌ Forgetting error messages
try:
    process_user(email)
except Exception as e:
    logger.error(f"Failed for {email}: {e}")  # PII in error log!

# ✅ Better
try:
    process_user(email)
except Exception as e:
    logger.error(f"Failed for {redact_email(email)}: {e}")
```

## Best Practices Checklist

- ✅ Create consistent redaction helper functions
- ✅ Redact all PII in logs automatically
- ✅ Show last 4 characters for debugging
- ✅ Preserve enough info for support/debugging
- ✅ Use structured logging with auto-redaction
- ✅ Document PII handling in Security Notes
- ✅ Test that redaction works correctly
- ✅ Train team on PII identification
- ✅ Regular audit of logs for PII leaks
- ✅ Consider legal requirements (GDPR, CCPA, PCI-DSS)

## Auto-Apply

When you see logging of PII, automatically:
1. Wrap with appropriate redaction function
2. Show last 4 characters for debugging
3. Add Security Note to docstring if handling PII
4. Use consistent redaction format
5. Test that PII is not in logs

## Related Skills

- structured-errors - Redact PII in error responses
- docstring-format - Document PII handling with Security Note
- tool-design-pattern - Redact PII in tool logs
- pytest-patterns - Test PII redaction
