---
name: ciphey
description: Automatic decryption and decoding tool using AI. Use when user says "解密", "decrypt", "decode", "crack", "破解密码", or provides encrypted/encoded text that needs to be deciphered. Supports 50+ encryption types including Base64, Caesar, Vigenere, XOR, Morse code, binary, hashes, and more.
---

# Ciphey

Automatic decryption/decoding tool that uses AI to detect and crack encryption.

## Usage

Run the decrypt script:

```bash
python3 ~/.claude/skills/ciphey/scripts/decrypt.py "<ciphertext>" [-q]
```

**Parameters:**
- `ciphertext`: The encrypted/encoded text to decrypt (required)
- `-q`: Quiet mode, suppress progress output (optional)

## Examples

Decrypt Base64:
```bash
python3 ~/.claude/skills/ciphey/scripts/decrypt.py "SGVsbG8gV29ybGQh"
# Output: Hello World!
```

Decrypt with quiet mode:
```bash
python3 ~/.claude/skills/ciphey/scripts/decrypt.py "Uryyb Jbeyq!" -q
# Output: Hello World! (Caesar/ROT13)
```

## Supported Encryptions

- **Encodings**: Base64, Base32, Base16, Binary, Hex, Octal, ASCII, URL encoding
- **Classical Ciphers**: Caesar, ROT13, Vigenere, Affine, Atbash, Playfair
- **Modern**: XOR, Repeating-key XOR
- **Hashes**: MD5, SHA1, SHA256, SHA512 (detection)
- **Other**: Morse code, NATO phonetic, Braille, and 40+ more

## Installation

The script auto-detects and uses available installation:

1. **Direct**: If `ciphey` command exists
2. **Docker**: Uses `remnux/ciphey` image (recommended)
3. **Homebrew**: `brew install ciphey`
4. **pipx**: `pipx install ciphey`

## Notes

- Uses AI to automatically detect encryption type
- Most decryptions complete in under 3 seconds
- Requires Python 3.7+
