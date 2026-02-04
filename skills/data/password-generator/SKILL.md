---
name: password-generator
description: Generate secure passwords and passphrases with customizable rules. Check password strength, generate bulk passwords, and create memorable passphrases.
---

# Password Generator

Generate cryptographically secure passwords and memorable passphrases. Customize character sets, length, and rules. Includes strength checking and bulk generation.

## Quick Start

```python
from scripts.password_gen import PasswordGenerator

# Generate password
gen = PasswordGenerator()
password = gen.generate(length=16)
print(password)  # "K#9mPx$vL2nQ@8wR"

# Generate passphrase
passphrase = gen.passphrase(words=4)
print(passphrase)  # "correct-horse-battery-staple"
```

## Features

- **Secure Generation**: Uses cryptographically secure random
- **Custom Rules**: Character sets, required types, exclusions
- **Passphrases**: Word-based memorable passwords
- **Strength Check**: Evaluate password strength
- **Bulk Generation**: Generate multiple passwords
- **Pronounceable**: Generate easier-to-type passwords

## API Reference

### Basic Generation

```python
gen = PasswordGenerator()

# Default (16 chars, mixed)
password = gen.generate()

# Custom length
password = gen.generate(length=24)
```

### Character Options

```python
# Include/exclude character types
password = gen.generate(
    length=16,
    uppercase=True,
    lowercase=True,
    digits=True,
    symbols=True
)

# Exclude ambiguous characters (0, O, l, 1, etc.)
password = gen.generate(length=16, exclude_ambiguous=True)

# Custom character set
password = gen.generate(length=16, charset="abc123!@#")

# Exclude specific characters
password = gen.generate(length=16, exclude="{}[]")
```

### Requirements

```python
# Require at least N of each type
password = gen.generate(
    length=16,
    min_uppercase=2,
    min_lowercase=2,
    min_digits=2,
    min_symbols=2
)
```

### Passphrases

```python
# Word-based passphrase
passphrase = gen.passphrase(words=4)
# "correct-horse-battery-staple"

# Custom separator
passphrase = gen.passphrase(words=4, separator="_")
# "correct_horse_battery_staple"

# With number
passphrase = gen.passphrase(words=3, include_number=True)
# "correct-horse-42-battery"

# Capitalize words
passphrase = gen.passphrase(words=4, capitalize=True)
# "Correct-Horse-Battery-Staple"
```

### Strength Check

```python
strength = gen.check_strength("MyP@ssw0rd!")
# {
#     'score': 3,           # 0-4 scale
#     'label': 'Strong',    # Weak, Fair, Good, Strong, Very Strong
#     'entropy': 65.2,      # Bits of entropy
#     'feedback': ['Good length', 'Has symbols']
# }
```

### Bulk Generation

```python
# Generate multiple passwords
passwords = gen.generate_bulk(count=10, length=16)

# To CSV
gen.generate_to_csv("passwords.csv", count=100, length=20)
```

## CLI Usage

```bash
# Generate single password
python password_gen.py --length 16

# Generate passphrase
python password_gen.py --passphrase --words 4

# Custom options
python password_gen.py --length 20 --no-symbols --exclude-ambiguous

# Bulk generate
python password_gen.py --count 10 --length 16

# Check strength
python password_gen.py --check "MyPassword123!"

# Generate to file
python password_gen.py --count 100 --output passwords.txt
```

### CLI Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--length` | Password length | 16 |
| `--count` | Number to generate | 1 |
| `--passphrase` | Generate passphrase | False |
| `--words` | Words in passphrase | 4 |
| `--no-uppercase` | Exclude uppercase | False |
| `--no-lowercase` | Exclude lowercase | False |
| `--no-digits` | Exclude digits | False |
| `--no-symbols` | Exclude symbols | False |
| `--exclude-ambiguous` | Exclude 0, O, l, 1 | False |
| `--check` | Check password strength | - |
| `--output` | Output file | - |

## Examples

### Strong Random Password

```python
gen = PasswordGenerator()
password = gen.generate(
    length=20,
    min_uppercase=2,
    min_lowercase=2,
    min_digits=2,
    min_symbols=2
)
print(f"Password: {password}")
print(f"Strength: {gen.check_strength(password)['label']}")
```

### Memorable Passphrase

```python
gen = PasswordGenerator()
passphrase = gen.passphrase(
    words=4,
    capitalize=True,
    include_number=True,
    separator="-"
)
print(passphrase)
# "Tiger-Mountain-42-Sunset-Lake"
```

### PIN Generation

```python
gen = PasswordGenerator()
pin = gen.generate(
    length=6,
    uppercase=False,
    lowercase=False,
    digits=True,
    symbols=False
)
print(f"PIN: {pin}")  # "847291"
```

### Batch for Team

```python
gen = PasswordGenerator()

# Generate passwords for new team members
team = ["alice", "bob", "charlie"]
for member in team:
    password = gen.generate(length=16)
    print(f"{member}: {password}")
```

## Strength Scoring

| Score | Label | Description |
|-------|-------|-------------|
| 0 | Very Weak | < 28 bits entropy |
| 1 | Weak | 28-35 bits |
| 2 | Fair | 36-59 bits |
| 3 | Strong | 60-127 bits |
| 4 | Very Strong | 128+ bits |

## Dependencies

```
(No external dependencies - uses Python standard library)
```

## Security Notes

- Uses `secrets` module for cryptographic randomness
- Never logs or stores generated passwords
- Passphrase wordlist is embedded (no external calls)
- Strength check is local (no external API)
