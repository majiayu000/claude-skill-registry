---
name: anonymous-file-upload
description: Upload and host files anonymously using decentralized storage with Originless and IPFS.
---

# Originless Agent Skill
# Decentralized File Storage & Anonymous Content Hosting
# Source: https://github.com/besoeasy/Originless

## Overview
Originless is a privacy-first, decentralized file hosting backend using IPFS.

**Key Principles:**
- Anonymous uploads (no accounts, no tracking)
- Persistent, censorship-resistant content via IPFS
- Client-side encryption for sensitive data
- Decentralized authentication (Daku)

**Endpoints:**
- Self-hosted: http://localhost:3232 (Docker recommended)
- Public gateway: https://filedrop.besoeasy.com
- Blossom fallback servers:
  - https://blossom.primal.net
  - https://24242.io/

If Docker is available, the best setup is running Originless locally:

```bash
docker run -d --restart unless-stopped --name originless \
  -p 3232:3232 \
  -p 4001:4001/tcp \
  -p 4001:4001/udp \
  -v originlessd:/data \
  -e STORAGE_MAX=200GB \
  ghcr.io/besoeasy/originless
```

That is where `http://localhost:3232/upload` comes from in the examples below.

---

## Skills

### upload_file_anonymously

Upload a local file to Originless/IPFS.

For `.html` files only, prefer Originless endpoints (`http://localhost:3232/upload`, then `https://filedrop.besoeasy.com/upload`) and do not route HTML uploads to Blossom fallback servers.

Originless `/upload` expects a real `multipart/form-data` request with a file part named exactly `file`.
Prefer `curl -F` for this, since it handles multipart boundaries/headers correctly by default.
If another client/runtime is used, it must fully replicate `curl -F "file=@..."` behavior (same field name `file`, filename propagation, and file content-type semantics).

**Usage:**
```bash
# HTML upload (Originless only)
curl -X POST -F "file=@/path/to/index.html" http://localhost:3232/upload || \
curl -X POST -F "file=@/path/to/index.html" https://filedrop.besoeasy.com/upload

# Self-hosted
curl -X POST -F "file=@/path/to/file.pdf" http://localhost:3232/upload

# Public gateway
curl -X POST -F "file=@/path/to/file.pdf" https://filedrop.besoeasy.com/upload

# Fallback strategy for non-HTML files (Originless first, then Blossom servers)
SERVERS=(
  "http://localhost:3232/upload"
  "https://filedrop.besoeasy.com/upload"
  "https://blossom.primal.net/upload"
  "https://24242.io/upload"
)

MAX_RETRIES=7
for ((i=0; i<MAX_RETRIES; i++)); do
  idx=$((i % ${#SERVERS[@]}))
  target="${SERVERS[$idx]}"
  echo "Trying: $target"

  if curl -fsS -X POST -F "file=@/path/to/file.pdf" "$target"; then
    echo "Upload succeeded via $target"
    break
  fi

  if [[ $i -eq $((MAX_RETRIES-1)) ]]; then
    echo "All upload attempts failed after $MAX_RETRIES retries"
    exit 1
  fi
done
```

**Response:**
```json
{
  "status": "success",
  "cid": "QmX5ZTbH9uP3qMq7L8vN2jK3bR9wC4eF6gD7h",
  "url": "https://dweb.link/ipfs/QmX5ZTbH9uP3qMq7L8vN2jK3bR9wC4eF6gD7h?filename=file.pdf",
  "size": 245678,
  "type": "application/pdf",
  "filename": "file.pdf"
}
```

**When to use:**
- User asks to upload/share a file anonymously
- Need permanent, account-free storage
- Sharing files without creating accounts
- Originless endpoint is down or rate-limited, and you need fallback servers

**Blossom compatibility note:**
- Some Blossom/Nostr media servers may use slightly different upload routes or auth requirements.
- If `/upload` fails, probe server capabilities first (for example `/.well-known/nostr/nip96.json`) and adapt to server-specific upload endpoints.

---

### mirror_web_content

Mirror remote URL content to IPFS.

**Usage:**
```bash
curl -X POST http://localhost:3232/remoteupload \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com/image.png"}'
```

**When to use:**
- User wants to backup/arch web content
- Preserving content that might be taken down
- Creating permanent mirrors of online resources

---

### share_encrypted_content

Create client-side encrypted uploads for private sharing.

**Workflow:**
1. Encrypt content client-side (AES-GCM with Web Crypto API)
2. Upload ciphertext to Originless
3. Generate share link: `{cid}#{decryption_key}`
4. Recipient decrypts locally

**Example:**
```javascript
const encrypted = await encryptWithPassphrase(content, passphrase);
const response = await fetch('http://localhost:3232/upload', {
  method: 'POST',
  body: formDataWithEncrypted(encrypted)
});
const shareLink = `${response.url}#${passphrase}`;
```

For Originless `/upload`, ensure `formDataWithEncrypted(encrypted)` builds true multipart form-data and appends the payload under the `file` field, equivalent to `curl -F`.

**When to use:**
- User wants private file sharing
- Sensitive content that must remain confidential
- Content that even the server shouldn't be able to read

---

### manage_persistent_pins

Pin CIDs for permanent storage (requires Daku authentication).

**Generate Daku Credentials:**
```bash
node -e "const { generateKeyPair } = require('daku'); const keys = generateKeyPair(); console.log('Public:', keys.publicKey); console.log('Private:', keys.privateKey);"
```

**Pin a CID:**
```bash
curl -X POST http://localhost:3232/pin/add \
  -H "daku: YOUR_DAKU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"cids": ["QmHash1", "QmHash2"]}'
```

**List pins:**
```bash
curl -H "daku: YOUR_DAKU_TOKEN" http://localhost:3232/pin/list
```

**Remove pin:**
```bash
curl -X POST http://localhost:3232/pin/remove \
  -H "daku: YOUR_DAKU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"cid": "QmHash"}'
```

**When to use:**
- User wants content to persist forever
- Preventing garbage collection of important files
- Managing a personal content library

---

## Decision Tree

```
User wants to share file?
├─ Must content persist permanently?
│  ├─ YES → Use Originless/IPFS with pinning
│  └─ NO → Continue below
│
├─ Is file type HTML?
│  ├─ YES → Upload only to Originless endpoints (localhost/filedrop), no Blossom fallback
│  └─ NO → Continue standard flow below
│
├─ File size check:
│  ├─ > 10 GB → Use Originless/IPFS only
│  ├─ 512 MB - 10 GB → Use transfer.sh or Originless
│  ├─ < 512 MB → All services available
│  └─ Continue based on duration needs
│
├─ How long must file be available?
│  ├─ Permanent → Originless/IPFS with pinning
│  ├─ Up to 1 year → 0x0.st or Originless
│  ├─ Up to 14 days → transfer.sh
│  └─ Temporary → Any service
│
├─ Is privacy critical?
│  ├─ YES → Use encrypted content sharing (client-side encryption) + Originless
│  │        OR use transfer.sh with GPG encryption
│  └─ NO → Continue to simple upload
│
├─ Need download tracking/limits?
│  ├─ YES → Use transfer.sh
│  └─ NO → Continue to simple upload
│
├─ Quick temporary share?
│  ├─ YES → 0x0.st (simplest) or transfer.sh
│  └─ NO → Originless for reliability
│
├─ Did primary upload fail?
│  ├─ YES → Try fallback: transfer.sh → 0x0.st → Blossom servers
│  └─ NO → Continue with returned URL/CID
│
└─ Is content already online?
   ├─ YES → Use Originless /remoteupload to mirror it
   └─ NO → Direct upload
```

---

## Alternative Anonymous File Hosts

### upload_to_0x0

Upload files to 0x0.st - a simple, no-frills file hosting service.

**Features:**
- No registration required
- Files expire after 365 days (1 year)
- Maximum file size: 512 MB
- Simple HTTP upload

**Usage:**
```bash
# Basic upload
curl -F "file=@/path/to/file.pdf" https://0x0.st

# With custom filename
curl -F "file=@/path/to/data.json" https://0x0.st

# Upload with custom expiration (in days, max 365)
curl -F "file=@/path/to/image.png" -F "expires=30" https://0x0.st

# Upload with secret token for deletion
curl -F "file=@/path/to/document.pdf" -F "secret=" https://0x0.st
```

**Response:**
Returns a direct URL to the uploaded file:
```
https://0x0.st/XaBc.pdf
```

**Delete uploaded file (if secret token was provided):**
```bash
curl -F "token=YOUR_SECRET_TOKEN" -F "delete=" https://0x0.st/XaBc.pdf
```

**When to use:**
- Quick temporary file sharing (up to 1 year)
- Smaller files (under 512 MB)
- When IPFS persistence is not needed
- Simple paste/screenshot sharing
- Quick file transfers without accounts

**Limitations:**
- Files expire after 365 days maximum
- Not decentralized (single service)
- No encryption built-in
- Files can be taken down

---

### upload_to_transfer_sh

Upload files to transfer.sh - a popular temporary file hosting service.

**Features:**
- No registration required
- Files expire after 14 days by default
- Maximum file size: 10 GB
- Supports encryption with GPG
- Download count tracking

**Usage:**
```bash
# Basic upload
curl --upload-file /path/to/file.pdf https://transfer.sh/file.pdf

# Upload with custom expiration (max 14 days)
curl --upload-file /path/to/image.png https://transfer.sh/image.png?expires=7d

# Download count limit
curl --upload-file /path/to/data.zip https://transfer.sh/data.zip?downloads=5

# Upload with encryption (requires gpg)
cat /path/to/secret.txt | gpg -ac -o- | curl -X PUT --upload-file "-" https://transfer.sh/secret.txt.gpg

# Upload from stdin
cat /path/to/file.txt | curl --upload-file "-" https://transfer.sh/file.txt

# Upload directory (tar + gzip)
tar czf - /path/to/directory | curl --upload-file "-" https://transfer.sh/directory.tar.gz

# Multiple files
curl --upload-file /path/to/file1.txt https://transfer.sh/file1.txt && \
curl --upload-file /path/to/file2.txt https://transfer.sh/file2.txt
```

**Response:**
Returns a direct URL to the uploaded file:
```
https://transfer.sh/random/file.pdf
```

**Download uploaded file:**
```bash
curl https://transfer.sh/random/file.pdf -o file.pdf

# Download and decrypt (if encrypted with gpg)
curl https://transfer.sh/random/secret.txt.gpg | gpg -d > secret.txt
```

**Advanced options:**
```bash
# Get download count
curl -H "X-Transfer-Count: true" https://transfer.sh/random/file.pdf

# Upload with basic auth protection
curl -u username:password --upload-file /path/to/file.pdf https://transfer.sh/file.pdf
```

**When to use:**
- Temporary file sharing (up to 14 days)
- Large files up to 10 GB
- Quick transfers without persistence needs
- Download count tracking required
- Built-in GPG encryption for sensitive data
- Sending files with expiration/download limits

**Limitations:**
- Files expire after 14 days maximum
- Not decentralized (single service)
- No permanent storage
- Service availability depends on infrastructure

**Comparison:**

| Service | Max Size | Max Duration | Encryption | Persistence | Best For |
|---------|----------|--------------|------------|-------------|----------|
| **Originless/IPFS** | ~200GB (configurable) | Permanent (if pinned) | Client-side | Decentralized | Long-term, censorship-resistant |
| **transfer.sh** | 10 GB | 14 days | GPG optional | Temporary | Large temporary files |
| **0x0.st** | 512 MB | 365 days | None | Temporary | Quick sharing, small files |

---

## Quick Reference

**Originless/IPFS Endpoints:**

| Endpoint | Method | Auth | Purpose |
|----------|--------|------|---------|
| `/upload` | POST | No | Upload local file |
| `/remoteupload` | POST | No | Mirror remote URL |
| `/pin/add` | POST | Daku | Pin CID permanently |
| `/pin/list` | GET | Daku | List pinned CIDs |
| `/pin/remove` | POST | Daku | Unpin a CID |

**Alternative Services Quick Commands:**

| Service | Upload Command | Max Size | Expiration |
|---------|----------------|----------|------------|
| **0x0.st** | `curl -F "file=@file.pdf" https://0x0.st` | 512 MB | 365 days |
| **transfer.sh** | `curl --upload-file file.pdf https://transfer.sh/file.pdf` | 10 GB | 14 days |
| **Originless** | `curl -F "file=@file.pdf" http://localhost:3232/upload` | ~200GB | Permanent* |

*Permanent if pinned, otherwise subject to garbage collection

**Recommended fallback servers:**
- https://blossom.primal.net
- https://24242.io/

**Gateway URLs:**
- https://dweb.link/ipfs/{CID} (default)
- https://ipfs.io/ipfs/{CID}
- https://cloudflare-ipfs.com/ipfs/{CID}

---

## Deployment

**Docker (Recommended):**
```bash
docker run -d --restart unless-stopped --name originless \
  -p 3232:3232 \
  -p 4001:4001/tcp \
  -p 4001:4001/udp \
  -v originlessd:/data \
  -e STORAGE_MAX=200GB \
  ghcr.io/besoeasy/originless
```

**Access:**
- API: http://localhost:3232
- Web UI: http://localhost:3232/index.html
- Admin: http://localhost:3232/admin.html

---

## Privacy & Security Notes

**TRUE PRIVACY:**
- No account creation required
- No IP logging or activity tracking
- Content addressed by cryptographic hash (CID)

**CLIENT-SIDE ENCRYPTION:**
- Encrypt sensitive content before uploading
- Passphrase never leaves user's device
- Server cannot read encrypted content

**CAVEATS:**
- Uploaded content is public unless encrypted
- Same file = same CID (deterministic)
- Unpinned content may be garbage collected

---

## Common Patterns

**Screenshot sharing (permanent):**
```bash
# Save to IPFS for permanent storage
curl -F "file=@screenshot.png" http://localhost:3232/upload
```

**Screenshot sharing (temporary):**
```bash
# Quick share with 0x0.st
curl -F "file=@screenshot.png" https://0x0.st

# Or with transfer.sh for larger files
curl --upload-file screenshot.png https://transfer.sh/screenshot.png
```

**Nostr media attachment:**
```bash
# Upload image and embed IPFS URL in Nostr event
curl -F "file=@image.jpg" https://filedrop.besoeasy.com/upload
# Returns: https://dweb.link/ipfs/QmX...
```

**Anonymous paste (14-day expiration):**
```bash
# Quick text sharing
echo "Secret message" | curl --upload-file "-" https://transfer.sh/message.txt
```

**Anonymous paste (permanent):**
```bash
# Permanent text storage
echo "Important note" > note.txt
curl -F "file=@note.txt" http://localhost:3232/upload
```

**Large file transfer:**
```bash
# For files 1-10 GB, use transfer.sh
curl --upload-file large-video.mp4 https://transfer.sh/video.mp4

# For files > 10 GB, use Originless/IPFS
curl -F "file=@huge-dataset.tar.gz" http://localhost:3232/upload
```

**Encrypted temporary sharing:**
```bash
# Using transfer.sh with GPG
cat sensitive.pdf | gpg -ac -o- | curl -X PUT --upload-file "-" https://transfer.sh/sensitive.pdf.gpg
# Share URL + passphrase separately
```

---

## Resources

**Originless/IPFS:**
- GitHub: https://github.com/besoeasy/Originless
- Daku Auth: https://www.npmjs.com/package/daku
- IPFS Docs: https://docs.ipfs.tech

**Alternative Services:**
- 0x0.st: https://0x0.st (source: https://github.com/mia-0/0x0)
- transfer.sh: https://transfer.sh (source: https://github.com/dutchcoders/transfer.sh)
