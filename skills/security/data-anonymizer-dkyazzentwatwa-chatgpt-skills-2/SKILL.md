---
name: data-anonymizer
description: Detect and mask PII (names, emails, phones, SSN, addresses) in text and CSV files. Multiple masking strategies with reversible tokenization option.
---

# Data Anonymizer

Detect and mask personally identifiable information (PII) in text documents and structured data. Supports multiple masking strategies and can process CSV files at scale.

## Quick Start

```python
from scripts.data_anonymizer import DataAnonymizer

# Anonymize text
anonymizer = DataAnonymizer()
result = anonymizer.anonymize("Contact John Smith at john@email.com or 555-123-4567")
print(result)
# "Contact [NAME] at [EMAIL] or [PHONE]"

# Anonymize CSV
anonymizer.anonymize_csv("customers.csv", "customers_anon.csv")
```

## Features

- **PII Detection**: Names, emails, phones, SSN, addresses, credit cards, dates
- **Multiple Strategies**: Mask, redact, hash, fake data replacement
- **CSV Processing**: Anonymize specific columns or auto-detect
- **Reversible Tokens**: Optional mapping for de-anonymization
- **Custom Patterns**: Add your own PII patterns
- **Audit Report**: List all detected PII with locations

## API Reference

### Initialization

```python
anonymizer = DataAnonymizer(
    strategy="mask",      # mask, redact, hash, fake
    reversible=False      # Enable token mapping
)
```

### Text Anonymization

```python
# Basic anonymization
result = anonymizer.anonymize(text)

# With specific PII types
result = anonymizer.anonymize(text, pii_types=["email", "phone"])

# Get detected PII report
result, report = anonymizer.anonymize(text, return_report=True)
```

### Masking Strategies

```python
text = "Email john@test.com, call 555-1234"

# Mask (default) - replace with type labels
anonymizer.strategy = "mask"
# "Email [EMAIL], call [PHONE]"

# Redact - replace with asterisks
anonymizer.strategy = "redact"
# "Email ***************, call ********"

# Hash - replace with hash
anonymizer.strategy = "hash"
# "Email a1b2c3d4, call e5f6g7h8"

# Fake - replace with realistic fake data
anonymizer.strategy = "fake"
# "Email jane@example.org, call 555-9876"
```

### CSV Processing

```python
# Auto-detect PII columns
anonymizer.anonymize_csv("input.csv", "output.csv")

# Specify columns
anonymizer.anonymize_csv(
    "input.csv",
    "output.csv",
    columns=["name", "email", "phone"]
)

# Different strategies per column
anonymizer.anonymize_csv(
    "input.csv",
    "output.csv",
    column_strategies={
        "name": "fake",
        "email": "hash",
        "ssn": "redact"
    }
)
```

### Reversible Anonymization

```python
anonymizer = DataAnonymizer(reversible=True)

# Anonymize with token mapping
result = anonymizer.anonymize("John Smith: john@test.com")
mapping = anonymizer.get_mapping()

# Save mapping securely
anonymizer.save_mapping("mapping.json", encrypt=True, password="secret")

# Later, de-anonymize
anonymizer.load_mapping("mapping.json", password="secret")
original = anonymizer.deanonymize(result)
```

### Custom Patterns

```python
# Add custom PII pattern
anonymizer.add_pattern(
    name="employee_id",
    pattern=r"EMP-\d{6}",
    label="[EMPLOYEE_ID]"
)
```

## CLI Usage

```bash
# Anonymize text file
python data_anonymizer.py --input document.txt --output document_anon.txt

# Anonymize CSV
python data_anonymizer.py --input customers.csv --output customers_anon.csv

# Specific strategy
python data_anonymizer.py --input data.csv --output anon.csv --strategy fake

# Generate audit report
python data_anonymizer.py --input document.txt --report audit.json

# Specific PII types only
python data_anonymizer.py --input doc.txt --types email phone ssn
```

### CLI Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--input` | Input file | Required |
| `--output` | Output file | Required |
| `--strategy` | Masking strategy | mask |
| `--types` | PII types to detect | all |
| `--columns` | CSV columns to process | auto |
| `--report` | Generate audit report | - |
| `--reversible` | Enable token mapping | False |

## Supported PII Types

| Type | Examples | Pattern |
|------|----------|---------|
| `name` | John Smith, Mary Johnson | NLP-based |
| `email` | user@domain.com | Regex |
| `phone` | 555-123-4567, (555) 123-4567 | Regex |
| `ssn` | 123-45-6789 | Regex |
| `credit_card` | 4111-1111-1111-1111 | Regex + Luhn |
| `address` | 123 Main St, City, ST 12345 | NLP + Regex |
| `date_of_birth` | 01/15/1990, January 15, 1990 | Regex |
| `ip_address` | 192.168.1.1 | Regex |

## Examples

### Anonymize Customer Support Logs

```python
anonymizer = DataAnonymizer(strategy="mask")

log = """
Ticket #1234: Customer John Doe (john.doe@company.com) called about
billing issue. SSN on file: 123-45-6789. Callback number: 555-867-5309.
Address: 123 Oak Street, Springfield, IL 62701.
"""

result = anonymizer.anonymize(log)
print(result)
# Ticket #1234: Customer [NAME] ([EMAIL]) called about
# billing issue. SSN on file: [SSN]. Callback number: [PHONE].
# Address: [ADDRESS].
```

### GDPR Compliance for Database Export

```python
anonymizer = DataAnonymizer(strategy="hash")

# Consistent hashing for joins
anonymizer.anonymize_csv(
    "users.csv",
    "users_anon.csv",
    columns=["email", "name", "phone"]
)

anonymizer.anonymize_csv(
    "orders.csv",
    "orders_anon.csv",
    columns=["customer_email"]  # Same hash as users.email
)
```

### Generate Test Data from Production

```python
anonymizer = DataAnonymizer(strategy="fake")

# Replace real PII with realistic fake data
anonymizer.anonymize_csv(
    "production_data.csv",
    "test_data.csv"
)

# Test data has same structure but fake PII
```

## Dependencies

```
pandas>=2.0.0
faker>=18.0.0
```

## Limitations

- Name detection may miss unusual names
- Address detection works best for US formats
- Custom patterns may be needed for domain-specific PII
- Fake data replacement doesn't preserve exact format
