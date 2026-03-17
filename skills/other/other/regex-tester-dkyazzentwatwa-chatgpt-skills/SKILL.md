---
name: regex-tester
description: Test, debug, and explain regular expressions. Visualize matches, generate patterns from examples, and convert between regex flavors.
---

# Regex Tester

Test and debug regular expressions with detailed match visualization, plain-English explanations, and pattern generation from examples.

## Quick Start

```python
from scripts.regex_tester import RegexTester

# Test pattern
tester = RegexTester()
result = tester.test(r"\d{3}-\d{4}", "Call 555-1234 today")
print(result['matches'])  # ['555-1234']

# Explain pattern
explanation = tester.explain(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")
print(explanation)

# Generate pattern from examples
pattern = tester.generate_pattern(["555-1234", "123-4567", "999-0000"])
print(pattern)  # r"\d{3}-\d{4}"
```

## Features

- **Pattern Testing**: Test against text with detailed results
- **Match Visualization**: See exactly what matched and where
- **Pattern Explanation**: Plain-English breakdown of regex
- **Pattern Generation**: Create patterns from example matches
- **Find & Replace**: Test substitution patterns
- **Common Patterns**: Library of pre-built patterns
- **Validation**: Check pattern syntax before use

## API Reference

### Testing

```python
tester = RegexTester()

# Basic test
result = tester.test(r"\d+", "There are 42 items")
# {
#     'pattern': r'\d+',
#     'text': 'There are 42 items',
#     'matches': ['42'],
#     'match_count': 1,
#     'positions': [(10, 12)],  # (start, end)
#     'groups': []
# }

# With flags
result = tester.test(r"hello", "Hello World", ignore_case=True)

# All matches with groups
result = tester.test(r"(\d{3})-(\d{4})", "555-1234 and 999-0000")
# matches: ['555-1234', '999-0000']
# groups: [('555', '1234'), ('999', '0000')]
```

### Explanation

```python
explanation = tester.explain(r"\b\w+@\w+\.\w{2,}\b")
# Returns:
# \b - Word boundary
# \w+ - One or more word characters
# @ - Literal '@'
# \w+ - One or more word characters
# \. - Literal '.'
# \w{2,} - Two or more word characters
# \b - Word boundary
```

### Pattern Generation

```python
# Generate pattern from examples
examples = ["user@test.com", "admin@site.org", "info@company.net"]
pattern = tester.generate_pattern(examples)
# Suggests: r"[a-z]+@[a-z]+\.(com|org|net)"

# With negative examples (what NOT to match)
pattern = tester.generate_pattern(
    positive=["555-1234", "999-0000"],
    negative=["555-12", "12345"]
)
```

### Find & Replace

```python
result = tester.replace(
    pattern=r"(\d{3})-(\d{4})",
    replacement=r"(\1) \2",
    text="Call 555-1234"
)
# "Call (555) 1234"
```

### Validation

```python
# Check if pattern is valid
is_valid, error = tester.validate(r"[invalid")
# is_valid: False
# error: "unterminated character set"
```

### Common Patterns

```python
# Get pre-built patterns
email = tester.patterns['email']
phone = tester.patterns['phone']
url = tester.patterns['url']
ip = tester.patterns['ipv4']
```

## CLI Usage

```bash
# Test pattern
python regex_tester.py --pattern "\d+" --text "There are 42 items"

# Test from file
python regex_tester.py --pattern "\w+@\w+\.\w+" --file emails.txt

# Explain pattern
python regex_tester.py --explain "\b[A-Z][a-z]+\b"

# Find and replace
python regex_tester.py --pattern "(\d+)" --replace "[$1]" --text "Item 42"

# Generate pattern
python regex_tester.py --generate "555-1234,999-0000,123-4567"

# Interactive mode
python regex_tester.py --interactive
```

### CLI Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--pattern` | Regex pattern | - |
| `--text` | Text to test against | - |
| `--file` | File to test against | - |
| `--explain` | Explain pattern | False |
| `--replace` | Replacement pattern | - |
| `--generate` | Generate from examples | - |
| `--ignore-case` | Case insensitive | False |
| `--multiline` | Multiline mode | False |
| `--interactive` | Interactive mode | False |

## Examples

### Email Validation

```python
tester = RegexTester()

email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

test_emails = [
    "user@example.com",
    "invalid.email",
    "user@domain",
    "test.user+tag@sub.domain.org"
]

for email in test_emails:
    result = tester.test(email_pattern, email)
    status = "Valid" if result['matches'] else "Invalid"
    print(f"{email}: {status}")
```

### Extract Data from Log

```python
tester = RegexTester()

log_line = '[2024-01-15 14:30:22] ERROR: Connection timeout (192.168.1.100)'
pattern = r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] (\w+): (.+) \((\d+\.\d+\.\d+\.\d+)\)'

result = tester.test(pattern, log_line)
if result['groups']:
    timestamp, level, message, ip = result['groups'][0]
    print(f"Time: {timestamp}")
    print(f"Level: {level}")
    print(f"Message: {message}")
    print(f"IP: {ip}")
```

### Phone Number Formatter

```python
tester = RegexTester()

# Normalize various phone formats
phones = ["5551234567", "(555) 123-4567", "555.123.4567"]
pattern = r"[\(\)\.\s-]?"

for phone in phones:
    # Remove all formatting
    clean = tester.replace(r"[\(\)\.\s-]", "", phone)
    # Format consistently
    formatted = tester.replace(
        r"(\d{3})(\d{3})(\d{4})",
        r"(\1) \2-\3",
        clean
    )
    print(f"{phone} -> {formatted}")
```

### Understand Complex Pattern

```python
tester = RegexTester()

# Explain a complex pattern
pattern = r"(?:https?://)?(?:www\.)?([a-zA-Z0-9-]+)\.([a-zA-Z]{2,})(?:/\S*)?"

explanation = tester.explain(pattern)
print(explanation)
# (?:https?://)? - Optional non-capturing group: 'http://' or 'https://'
# (?:www\.)? - Optional non-capturing group: 'www.'
# ([a-zA-Z0-9-]+) - Capturing group 1: domain name
# \. - Literal '.'
# ([a-zA-Z]{2,}) - Capturing group 2: TLD
# (?:/\S*)? - Optional non-capturing group: path
```

## Common Patterns Library

| Name | Pattern | Matches |
|------|---------|---------|
| `email` | Complex | user@domain.com |
| `phone_us` | `\d{3}[-.]?\d{3}[-.]?\d{4}` | 555-123-4567 |
| `url` | Complex | https://example.com |
| `ipv4` | `\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}` | 192.168.1.1 |
| `date_iso` | `\d{4}-\d{2}-\d{2}` | 2024-01-15 |
| `time_24h` | `\d{2}:\d{2}(:\d{2})?` | 14:30:00 |
| `hex_color` | `#[0-9A-Fa-f]{6}` | #FF5733 |
| `zipcode_us` | `\d{5}(-\d{4})?` | 12345-6789 |

## Dependencies

```
(No external dependencies - uses Python standard library re module)
```

## Limitations

- Pattern generation is heuristic (may not be optimal)
- Some advanced regex features are Python-specific
- Explanation works best with common patterns
- Very long patterns may have simplified explanations
