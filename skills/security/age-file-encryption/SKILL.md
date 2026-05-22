---
name: age-file-encryption
description: Encrypt and decrypt files or streams using age — a simple, modern, and secure encryption tool with small explicit keys, passphrase support, SSH key support, post-quantum hybrid keys, and UNIX-style composability. No config options, no footguns.
---

# age File Encryption

[age](https://github.com/FiloSottile/age) is a minimal, modern encryption tool. It replaces GPG for most file encryption needs with a much simpler design: small explicit keys, no config files, and clean composability with UNIX pipes.

## When to Use This Skill

- Encrypting files or directories before storing or sharing them
- Securely sending files to specific recipients by public key
- Encrypting secrets with a passphrase for backup or storage
- Encrypting to existing SSH public keys (ed25519 or RSA)
- Encrypting to multiple recipients at once
- Encrypting to a GitHub user's SSH keys
- Automating encryption/decryption in scripts

## Installation

```bash
# macOS / Linux (Homebrew)
brew install age

# Debian / Ubuntu 22.04+
apt install age

# Arch Linux
pacman -S age

# Alpine Linux
apk add age

# Fedora
dnf install age

# Windows
winget install --id FiloSottile.age

# From source (requires Go)
go install filippo.io/age/cmd/...@latest
```

Pre-built binaries:
```
https://dl.filippo.io/age/latest?for=linux/amd64
https://dl.filippo.io/age/latest?for=darwin/arm64
https://dl.filippo.io/age/latest?for=windows/amd64
```

## Core Concepts

| Term | Meaning |
|------|---------|
| **recipient** | Public key — who can decrypt the file |
| **identity** | Private key file — used to decrypt |
| **age public key** | Starts with `age1...` |
| **age private key** | Starts with `AGE-SECRET-KEY-1...`, stored in a key file |

## Key Generation

```bash
# Generate a key pair and save to key.txt
age-keygen -o key.txt
# Output: Public key: age1ql3z7hjy54pw3hyww5ayyfg7zqgvc7w3j2elw8zmrj2kg5sfn9aqmcac8p

# Print only the public key from an existing key file
age-keygen -y key.txt
```

## Encrypting Files

### With a recipient's public key

```bash
# Encrypt a file
age -r age1ql3z7hjy54pw3hyww5ayyfg7zqgvc7w3j2elw8zmrj2kg5sfn9aqmcac8p -o secret.txt.age secret.txt

# Using a pipe
cat secret.txt | age -r age1ql3z7hjy54... > secret.txt.age
```

### With a passphrase

```bash
# age will prompt for a passphrase (or autogenerate a secure one)
age -p secret.txt > secret.txt.age
```

### To multiple recipients

```bash
# Each recipient can independently decrypt the file
age -o file.age \
  -r age1ql3z7hjy54pw3hyww5ayyfg7zqgvc7w3j2elw8zmrj2kg5sfn9aqmcac8p \
  -r age1lggyhqrw2nlhcxprm67z43rta597azn8gknawjehu9d9dl0jq3yqqvfafg \
  file.txt
```

### With a recipients file

```bash
# recipients.txt — one public key per line, # for comments
cat recipients.txt
# Alice
age1ql3z7hjy54pw3hyww5ayyfg7zqgvc7w3j2elw8zmrj2kg5sfn9aqmcac8p
# Bob
age1lggyhqrw2nlhcxprm67z43rta597azn8gknawjehu9d9dl0jq3yqqvfafg

age -R recipients.txt file.txt > file.txt.age
```

### With SSH keys

```bash
# Encrypt using an SSH public key
age -R ~/.ssh/id_ed25519.pub secret.txt > secret.txt.age

# Encrypt to all SSH keys on a GitHub profile
curl https://github.com/username.keys | age -R - secret.txt > secret.txt.age
```

### With armor (PEM text output)

```bash
# Produces ASCII-safe output, safe to paste in email or config
age -a -r age1ql3z7... secret.txt > secret.txt.age
```

### Encrypting a directory (tar + age)

```bash
tar czf - ~/data | age -r age1ql3z7... > data.tar.gz.age
```

## Decrypting Files

### With an identity (key) file

```bash
age -d -i key.txt secret.txt.age > secret.txt
```

### With passphrase

```bash
# age auto-detects passphrase-encrypted files
age -d secret.txt.age > secret.txt
# Prompts: Enter passphrase:
```

### With an SSH private key

```bash
age -d -i ~/.ssh/id_ed25519 secret.txt.age > secret.txt
```

### Decrypting to stdout (piping)

```bash
age -d -i key.txt archive.tar.gz.age | tar xzf -
```

## Post-Quantum Keys (v1.3.0+)

Hybrid post-quantum keys protect against future quantum computer attacks.

```bash
# Generate a post-quantum key pair
age-keygen -pq -o key.txt

# Extract the public key (recipients start with age1pq1...)
age-keygen -y key.txt > recipient.txt

# Encrypt
age -R recipient.txt file.txt > file.txt.age

# Decrypt
age -d -i key.txt file.txt.age > file.txt
```

## Passphrase-Protected Identity Files

Store your private key encrypted with a passphrase:

```bash
# Generate key and immediately encrypt it with a passphrase
age-keygen | age -p > key.age
# Output: Public key: age1yhm4gctwfmrpz87tdslm550wrx6m79y9f2hdzt0lndjnehwj0ukqrjpyx5

# Encrypt a file using the public key
age -r age1yhm4gctwfmrpz87tdslm550wrx6m79y9f2hdzt0lndjnehwj0ukqrjpyx5 secrets.txt > secrets.txt.age

# Decrypt — age will prompt for the passphrase to unlock key.age first
age -d -i key.age secrets.txt.age > secrets.txt
```

## Inspect an Encrypted File

```bash
age-inspect secrets.age

# JSON output for scripting
age-inspect --json secrets.age
```

## CLI Reference

```
Usage:
    age [--encrypt] (-r RECIPIENT | -R PATH)... [--armor] [-o OUTPUT] [INPUT]
    age [--encrypt] --passphrase [--armor] [-o OUTPUT] [INPUT]
    age --decrypt [-i PATH]... [-o OUTPUT] [INPUT]

Options:
    -e, --encrypt               Encrypt (default if omitted)
    -d, --decrypt               Decrypt
    -o, --output OUTPUT         Write result to file
    -a, --armor                 Output PEM-encoded text
    -p, --passphrase            Encrypt with a passphrase
    -r, --recipient RECIPIENT   Encrypt to recipient (repeatable)
    -R, --recipients-file PATH  Encrypt to recipients from file (repeatable)
    -i, --identity PATH         Identity file for decryption (repeatable)
```

INPUT defaults to stdin, OUTPUT defaults to stdout.

## Tips

- Use `-a` / `--armor` when the output needs to be text-safe (email, config files)
- Multiple `-i` flags can be passed; unused identity files are silently ignored
- Pass `-` as a path to read recipients or identities from stdin
- Encrypted files have the `.age` extension by convention
- age is composable — pipe freely with `tar`, `gzip`, `ssh`, etc.
- For automation, store the public key in the repo and keep the private key secret

## Security Notes

- SSH key encryption embeds a public key tag in the file, making it possible to fingerprint which key was used
- Passphrase-protected identity files are useful for keys stored remotely, but usually unnecessary for local keys
- Post-quantum keys have ~2000-character public keys — use a recipients file for convenience

## Related Skills

- `anonymous-file-upload` — Upload the encrypted `.age` file anonymously after encrypting
- `send-email-programmatically` — Send encrypted files over email using armored output (`-a`)
- `nostr-logging-system` — Publish encrypted payloads to Nostr
