---
name: hash-calculator
description: Calculate cryptographic hashes (MD5, SHA1, SHA256, SHA512) for text and files. Compare hashes, verify integrity, and batch process directories.
---

# Hash Calculator

Calculate cryptographic hash values for text strings and files. Supports multiple algorithms, file verification, and batch processing.

## Quick Start

```python
from scripts.hash_calc import HashCalculator

# Hash text
calc = HashCalculator()
result = calc.hash_text("Hello, World!")
print(result['sha256'])

# Hash file
result = calc.hash_file("document.pdf")
print(result['md5'])

# Verify file integrity
is_valid = calc.verify_file("file.zip", "expected_hash", algorithm="sha256")
```

## Features

- **Multiple Algorithms**: MD5, SHA1, SHA256, SHA384, SHA512, BLAKE2
- **Text Hashing**: Hash strings directly
- **File Hashing**: Efficient streaming for large files
- **Verification**: Compare against expected hash
- **Batch Processing**: Hash multiple files
- **Checksum Files**: Generate/verify checksum files

## API Reference

### Text Hashing

```python
calc = HashCalculator()

# Single algorithm
md5 = calc.hash_text("Hello", algorithm="md5")

# All algorithms
results = calc.hash_text("Hello")
# {'md5': '...', 'sha1': '...', 'sha256': '...', ...}

# Specific algorithms
results = calc.hash_text("Hello", algorithms=["md5", "sha256"])
```

### File Hashing

```python
# Single file
result = calc.hash_file("document.pdf")
print(result['sha256'])

# Specific algorithm
sha256 = calc.hash_file("file.zip", algorithm="sha256")
```

### Verification

```python
# Verify file against expected hash
is_valid = calc.verify_file(
    "download.iso",
    "a1b2c3d4e5...",
    algorithm="sha256"
)

# Verify text
is_valid = calc.verify_text("password", "5f4dcc3b...", algorithm="md5")
```

### Batch Processing

```python
# Hash all files in directory
results = calc.hash_directory("./files", algorithm="sha256")
# {'file1.txt': 'abc...', 'file2.pdf': 'def...'}

# With recursive option
results = calc.hash_directory("./files", recursive=True)
```

### Checksum Files

```python
# Generate checksum file
calc.generate_checksums("./release", "checksums.sha256", algorithm="sha256")

# Verify against checksum file
results = calc.verify_checksums("checksums.sha256")
# {'file1.zip': True, 'file2.zip': True, 'file3.zip': False}
```

## CLI Usage

```bash
# Hash text
python hash_calc.py --text "Hello, World!"

# Hash file
python hash_calc.py --file document.pdf

# Specific algorithm
python hash_calc.py --file document.pdf --algorithm sha256

# Verify file
python hash_calc.py --file download.iso --verify "expected_hash"

# Hash directory
python hash_calc.py --directory ./files --output checksums.txt

# Verify checksums file
python hash_calc.py --verify-checksums checksums.sha256
```

### CLI Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--text` | Text to hash | - |
| `--file` | File to hash | - |
| `--directory` | Directory to hash | - |
| `--algorithm` | Hash algorithm | all |
| `--verify` | Expected hash to verify | - |
| `--output` | Output file | - |
| `--recursive` | Recursive directory | False |
| `--verify-checksums` | Verify checksum file | - |

## Supported Algorithms

| Algorithm | Output Length | Use Case |
|-----------|---------------|----------|
| `md5` | 128 bits (32 hex) | Legacy, checksums (not secure) |
| `sha1` | 160 bits (40 hex) | Legacy (not secure) |
| `sha256` | 256 bits (64 hex) | General purpose, secure |
| `sha384` | 384 bits (96 hex) | High security |
| `sha512` | 512 bits (128 hex) | Maximum security |
| `blake2b` | 512 bits | Modern, fast |
| `blake2s` | 256 bits | Modern, fast, small |

## Examples

### Verify Download Integrity

```python
calc = HashCalculator()

# Downloaded file and expected hash from website
expected = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
is_valid = calc.verify_file("ubuntu.iso", expected, algorithm="sha256")

if is_valid:
    print("Download verified successfully!")
else:
    print("WARNING: Hash mismatch - file may be corrupted!")
```

### Generate Release Checksums

```python
calc = HashCalculator()

# Generate checksums for release files
calc.generate_checksums(
    "./release",
    "SHA256SUMS",
    algorithm="sha256"
)

# Output: SHA256SUMS
# e3b0c44298fc1c14...  release-v1.0.zip
# a1b2c3d4e5f6g7h8...  release-v1.0.tar.gz
```

### Password Storage (Example)

```python
calc = HashCalculator()
import os

# Note: In production, use bcrypt/argon2 instead
salt = os.urandom(16).hex()
password = "user_password"
hashed = calc.hash_text(salt + password, algorithm="sha256")

# Store: salt + ":" + hashed
stored = f"{salt}:{hashed}"
```

### Compare Two Files

```python
calc = HashCalculator()

hash1 = calc.hash_file("file1.txt", algorithm="sha256")
hash2 = calc.hash_file("file2.txt", algorithm="sha256")

if hash1 == hash2:
    print("Files are identical")
else:
    print("Files are different")
```

## Output Formats

### Text Output
```
MD5:    5d41402abc4b2a76b9719d911017c592
SHA1:   aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d
SHA256: 2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824
```

### JSON Output
```json
{
  "input": "hello",
  "md5": "5d41402abc4b2a76b9719d911017c592",
  "sha256": "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
}
```

## Dependencies

```
(No external dependencies - uses Python standard library)
```

## Security Notes

- MD5 and SHA1 are not collision-resistant (don't use for security)
- Use SHA256 or higher for security applications
- For password hashing, use dedicated libraries (bcrypt, argon2)
- File hashing uses streaming to handle large files efficiently
