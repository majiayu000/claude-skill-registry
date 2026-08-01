---
name: implementing-code-signing
description: <!-- Copyright (c) 2026 defconxt. All rights reserved. -->
---

<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: implementing-code-signing
description: >-
  Implement code signing for software integrity verification including GPG
  signing, Authenticode (Windows), codesign (macOS), sigstore/cosign for
  containers, and CI/CD pipeline integration for automated signing workflows.
domain: cybersecurity
subdomain: cryptography
tags:
  - code-signing
  - authenticode
  - gpg
  - sigstore
  - cosign
  - software-integrity
  - supply-chain
  - notarization
version: "1.0"
author: defconxt
license: AGPL-3.0
metadata:
  mitre-attack: ["T1553.002"]
---

# Implementing Code Signing

## Overview

Code signing cryptographically binds identity to software artifacts, ensuring
integrity and authenticity. This skill covers signing executables, scripts,
container images, and git commits across platforms, with CI/CD automation
for supply chain security.

## Prerequisites

| Requirement | Install |
|---|---|
| GnuPG 2.x | `apt install gnupg2` |
| cosign (sigstore) | `go install github.com/sigstore/cosign/v2/cmd/cosign@latest` |
| osslsigncode | `apt install osslsigncode` |
| Python 3.10+ | For agent tooling |

## Key Concepts

### GPG Signing

```bash
# Generate a signing key
gpg --full-generate-key --expert
# Select: ECC (sign only), Curve 25519, 2y expiry

# List signing keys
gpg --list-secret-keys --keyid-format=long

# Sign a file (detached signature)
gpg --armor --detach-sign --output file.sig file.tar.gz

# Verify a signature
gpg --verify file.sig file.tar.gz

# Sign a git commit
git commit -S -m "Signed commit"

# Sign a git tag
git tag -s v1.0.0 -m "Release v1.0.0"

# Verify git signatures
git log --show-signature -1
git tag -v v1.0.0
```

### Windows Authenticode

```bash
# Sign with osslsigncode (cross-platform)
osslsigncode sign -certs cert.pem -key key.pem \
  -n "Application Name" -i https://example.com \
  -ts http://timestamp.digicert.com \
  -h sha256 -in app.exe -out app-signed.exe

# Verify Authenticode signature
osslsigncode verify -in app-signed.exe

# PowerShell (on Windows)
# Set-AuthenticodeSignature -FilePath app.exe -Certificate $cert -TimestampServer "http://timestamp.digicert.com"

# Verify with signtool (Windows SDK)
# signtool verify /pa /v app-signed.exe
```

### macOS Code Signing

```bash
# Sign with codesign
codesign --sign "Developer ID Application: Name (TEAMID)" \
  --timestamp --options runtime app.app

# Verify signature
codesign --verify --verbose=2 app.app

# Notarize with Apple
xcrun notarytool submit app.zip --apple-id dev@example.com \
  --team-id TEAMID --password "@keychain:AC_PASSWORD" --wait

# Staple notarization ticket
xcrun stapler staple app.app
```

### Container Image Signing (cosign)

```bash
# Generate a cosign keypair
cosign generate-key-pair

# Sign a container image
cosign sign --key cosign.key registry.example.com/app:v1.0

# Verify a container image
cosign verify --key cosign.pub registry.example.com/app:v1.0

# Keyless signing with OIDC (sigstore)
cosign sign registry.example.com/app:v1.0

# Verify keyless signature
cosign verify --certificate-identity dev@example.com \
  --certificate-oidc-issuer https://accounts.google.com \
  registry.example.com/app:v1.0

# Sign with SBOM attachment
cosign attest --predicate sbom.json --key cosign.key \
  registry.example.com/app:v1.0
```

### CI/CD Integration

```yaml
# GitHub Actions — sign container on push
- name: Sign container image
  run: |
    cosign sign --key env://COSIGN_KEY \
      ${{ env.REGISTRY }}/${{ env.IMAGE }}:${{ github.sha }}
  env:
    COSIGN_KEY: ${{ secrets.COSIGN_PRIVATE_KEY }}
    COSIGN_PASSWORD: ${{ secrets.COSIGN_PASSWORD }}
```

## Workflow

1. **Generate** — Create signing keys with appropriate algorithm
2. **Secure** — Store private keys in HSM, KMS, or CI secret store
3. **Integrate** — Add signing step to build pipeline
4. **Timestamp** — Always use a timestamp server for long-term validity
5. **Verify** — Add verification gates in deployment pipeline
6. **Rotate** — Plan key rotation with overlapping validity periods

## Verification

| Check | Method |
|---|---|
| GPG signature valid | `gpg --verify file.sig file.tar.gz` returns "Good signature" |
| Git commits signed | `git log --show-signature` shows valid signatures |
| Container signed | `cosign verify` succeeds against registry image |
| Timestamp present | Signature includes TSA timestamp for long-term validity |
| Key in secure storage | Private key not in repository or filesystem |

## References

- [Sigstore Documentation](https://docs.sigstore.dev/)
- [GnuPG Manual](https://www.gnupg.org/documentation/manuals/gnupg/)
- [Apple Code Signing Guide](https://developer.apple.com/documentation/security/code_signing_services)
- [Microsoft Authenticode](https://learn.microsoft.com/en-us/windows/win32/seccrypto/cryptography-tools)
