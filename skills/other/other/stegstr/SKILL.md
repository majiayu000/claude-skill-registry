---
name: stegstr
summary: Embed and decode hidden messages in PNG images. Steganographic Nostr client for hiding data in images—works offline, no registration.
description: Decode and embed Stegstr payloads in PNG images. Use when the user needs to extract hidden Nostr data from a Stegstr image, encode a payload into a cover PNG, or work with steganographic social networking (Nostr-in-images). Supports CLI (stegstr-cli decode, detect, embed, post) for scripts and AI agents.
license: MIT
tags: steganography, nostr, images, crypto, integration, file-management, automation, cli
install:
  requirements: |
    - Rust (latest stable) - https://rustup.rs
    - Git
  steps: |
    1. git clone https://github.com/brunkstr/Stegstr.git
    2. cd Stegstr/src-tauri && cargo build --release --bin stegstr-cli
    3. Binary: target/release/stegstr-cli (Windows: stegstr-cli.exe)
permissions:
  - filesystem
metadata:
  homepage: https://stegstr.com
  for-agents: https://www.stegstr.com/wiki/for-agents.html
  repo: https://github.com/brunkstr/Stegstr
---

# Stegstr

Stegstr hides Nostr messages and arbitrary payloads inside PNG images using steganography. Users embed their feed (posts, DMs, JSON) into images and share them; recipients use Detect to load the hidden content. No registration, works offline.

## When to use this skill

- User wants to **decode** (extract) hidden data from a PNG that contains Stegstr data.
- User wants to **embed** a payload into a cover PNG (e.g. Nostr bundle, JSON, text).
- User mentions steganography, Nostr-in-images, Stegstr, hiding data in images, or secret messages in photos.
- User needs programmatic access for automation, scripts, or AI agents.

## CLI (headless)

Build the CLI from the Stegstr repo:

```bash
git clone https://github.com/brunkstr/Stegstr.git
cd Stegstr/src-tauri
cargo build --release --bin stegstr-cli
```

Binary: `target/release/stegstr-cli` (or `stegstr-cli.exe` on Windows).

### Decode (extract payload)

```bash
stegstr-cli decode image.png
```

Writes raw payload to stdout. Valid UTF-8 JSON is printed as text; otherwise `base64:<data>`. Exit 0 on success.

### Detect (decode + decrypt app bundle)

```bash
stegstr-cli detect image.png
```

Decodes and decrypts; prints Nostr bundle JSON `{ "version": 1, "events": [...] }`.

### Embed (hide payload in image)

```bash
stegstr-cli embed cover.png -o out.png --payload "text or JSON"
stegstr-cli embed cover.png -o out.png --payload @bundle.json
stegstr-cli embed cover.png -o out.png --payload @bundle.json --encrypt
```

Use `--payload @file` to load from file. Use `--encrypt` so any Stegstr user can detect. Use `--payload-base64 <base64>` for binary payloads.

### Post (create kind 1 note bundle)

```bash
stegstr-cli post "Your message here" --output bundle.json
stegstr-cli post "Message" --privkey-hex <64-char-hex> --output bundle.json
```

Creates a Nostr bundle; use `stegstr-cli embed` to hide it in an image.

## Example workflow

```bash
# Create a post bundle
stegstr-cli post "Hello from OpenClaw" --output bundle.json

# Embed into a cover image (encrypted for any Stegstr user)
stegstr-cli embed cover.png -o stego.png --payload @bundle.json --encrypt

# Recipient detects and extracts
stegstr-cli detect stego.png
```

## Image format

PNG only (lossless). JPEG or other lossy formats will corrupt the hidden data.

## Payload format

- **Magic:** `STEGSTR` (7 bytes ASCII)
- **Length:** 4 bytes, big-endian
- **Payload:** UTF-8 JSON or raw bytes (desktop app encrypts; CLI can embed raw or `--encrypt`)

Decrypted bundle: `{ "version": 1, "events": [ ... Nostr events ... ] }`. Schema: [bundle.schema.json](https://raw.githubusercontent.com/brunkstr/Stegstr/main/schema/bundle.schema.json).

## Links

- **agents.txt:** https://www.stegstr.com/agents.txt
- **For agents:** https://www.stegstr.com/wiki/for-agents.html
- **CLI docs:** https://www.stegstr.com/wiki/cli.html
- **Downloads:** https://github.com/brunkstr/Stegstr/releases/latest
