---
name: kb-fediverse-http-signatures
description: >
  Background knowledge about how HTTP Signatures work in ActivityPub and the
  Fediverse, including the signing and verification process, the public key
  model, authorized fetch / secure mode, key rotation, instance actors, and
  known interoperability quirks across implementations. Load when the user
  asks about implementing HTTP signatures, debugging signature verification
  failures, the Digest header, the (request-target) pseudo-header, keyId
  resolution, the publicKey property on actors, hs2019, clock skew, or
  federation failing between specific implementations. Also load when
  reviewing or writing code that signs or verifies ActivityPub requests.
user-invocable: false
---

# Fediverse HTTP Signatures — Complete Reference

## Overview

ActivityPub does not specify an authentication mechanism in its core spec.
In practice, the Fediverse has converged on **HTTP Signatures** (draft-cavage-12,
formally `draft-cavage-http-signatures`) for server-to-server authentication.
When one server POSTs an activity to another server's inbox, it signs the
request so the receiving server can verify the sender's identity.

The spec being used is `draft-cavage-http-signatures-12` — an expired IETF
Internet Draft, not an RFC. It has been superseded by RFC 9421, but the
Fediverse has not yet migrated to RFC 9421 at any meaningful scale. Treat
cavage-12 as the working standard for all current implementations.

---

## 1. The Public Key Model

Each actor (user) has an asymmetric keypair. The private key stays on the
server; the public key is published in the actor document under the
`publicKey` property, using the LD Security Vocabulary v1:

```json
{
  "@context": [
    "https://www.w3.org/ns/activitystreams",
    "https://w3id.org/security/v1"
  ],
  "type": "Person",
  "id": "https://example.com/users/alice",
  "inbox": "https://example.com/users/alice/inbox",
  "publicKey": {
    "id": "https://example.com/users/alice#main-key",
    "owner": "https://example.com/users/alice",
    "publicKeyPem": "-----BEGIN PUBLIC KEY-----\nMIIB...\n-----END PUBLIC KEY-----"
  }
}
```

Key points:
- `publicKey` may be a single object, a single id string, or an array
- The key object's `id` is the `keyId` used in the `Signature` header
- `owner` (or `controller`) links back to the actor for verification
- The key is RSA by default; Ed25519 is more modern but not yet widely
  supported across the Fediverse
- Generate 2048-bit RSA minimum; 4096-bit is common
- The PEM encoding may be PKCS-1 (`-----BEGIN RSA PUBLIC KEY-----`) or
  PKCS-8/SPKI (`-----BEGIN PUBLIC KEY-----`); crypto libraries generally
  auto-detect the format

---

## 2. How to Sign a Request

The standard set of headers to sign for a POST (inbox delivery):

```
(request-target)
host
date
digest
content-type
```

For a GET request, omit `digest` and `content-type`.

### Step-by-step signing

**1. Generate the `Digest` header (POST only)**

```
SHA-256=<base64(sha256(request_body))>
```

For an empty body, the SHA-256 of an empty string is always:
```
SHA-256=47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU=
```

Use standard base64 with padding. Do NOT use URL-safe base64. Do NOT use
the variant that inserts newlines every 60 characters (e.g. Ruby's
`Base64.encode64` — use `Base64.strict_encode64` instead).

**2. Construct the signing string**

Each header becomes one line: `headername: value`.
Header names must be **lowercased**.
Lines are joined with `\n` (ASCII newline, `0x0A`).
There must be **NO trailing newline** after the last line.

The `(request-target)` pseudo-header is constructed as:
```
(request-target): post /users/alice/inbox
```
i.e. `method_lowercase + " " + path_and_query`.

Example signing string for a POST:
```
(request-target): post /users/alice/inbox
host: example.com
date: Mon, 01 Jan 2024 12:00:00 GMT
digest: SHA-256=47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU=
content-type: application/activity+json
```

**3. Sign the string**

Sign the signing string with the actor's RSA private key using
RSASSA-PKCS1-v1_5 with SHA-256 (i.e. `rsa-sha256`).
Base64-encode the resulting bytes (standard base64 with padding).

**4. Set the `Signature` header**

```
Signature: keyId="https://example.com/users/alice#main-key",
           algorithm="hs2019",
           headers="(request-target) host date digest content-type",
           signature="<base64-encoded-signature>"
```

Use `hs2019` as the `algorithm` value — it is a placeholder meaning
"determine the algorithm from the key metadata." Do **not** use
`rsa-sha256` as the algorithm string in new implementations (see quirks).

Use the `Signature` header, **not** `Authorization: Signature ...`.

---

## 3. How to Verify a Signature

**1. Extract the `Signature` header**

Parse the `keyId`, `headers`, `algorithm`, and `signature` parameters.

**2. Resolve the public key** (see Section 4 below)

**3. Reconstruct the signing string**

Using the same `headers` list from the signature and the actual request
values, rebuild the signing string using the same rules as signing:
lowercased header names, `\n`-separated, no trailing newline.

**4. Verify the Digest** (if present and it was in the signed headers)

Compute SHA-256 of the request body and compare to the `Digest` header.
If they don't match, reject — the body was tampered with.

**5. Check the `Date` header**

Compare to current time. Reject if the skew is too large. A window of
approximately ±1 hour is the community consensus (see quirks for
implementation-specific values).

**6. Verify the cryptographic signature**

Use the public key and the reconstructed signing string to verify the
base64-decoded `signature` value. If verification fails with a cached key,
re-fetch the key from the origin (the actor may have rotated their key)
and try once more before rejecting.

**7. Return 401 if verification fails** (when a signature is required).

---

## 4. Resolving a `keyId` to a Public Key

The `keyId` is a URL. Resolving it to an actual public key requires care
because two patterns exist in the wild:

**Pattern A — Fragment URI (Mastodon style)**

`keyId = "https://example.com/users/alice#main-key"`

- Strip the fragment: fetch `https://example.com/users/alice`
- The response is the actor document
- Find `publicKey` in the actor; if it's an array, find the entry whose
  `id` matches the full `keyId` including the fragment
- Verify the key's `id` matches the original `keyId` exactly

**Pattern B — Path URI (GoToSocial style)**

`keyId = "https://example.com/users/alice/main-key"`

- Fetch the URL directly
- The response is a raw Key object (not a full actor), containing
  `publicKeyPem` and an `owner` (or `controller`) property
- Follow `owner` to fetch the full actor and verify the key is authorized

In both cases: always verify that the key's `id` matches the `keyId` from
the `Signature` header, and that the key's `owner`/`controller` matches
the expected actor. Never trust a key that doesn't pass this check.

---

## 5. Authorized Fetch (Secure Mode)

Some servers require HTTP Signatures on **GET requests** as well as POST
requests. This is called "authorized fetch" or "secure mode" (Mastodon's
term). In this mode:

- Fetching an actor, object, or collection requires a signed GET
- The signing actor is typically the instance actor (see Section 6)
- Servers use this to block data access from defederated instances
- GoToSocial requires signed GETs in all modes
- Mastodon only requires them when secure mode is explicitly enabled

If you're building an implementation and encounter 401 responses to unsigned
GETs, the remote server has authorized fetch enabled.

---

## 6. Instance Actors

Most servers maintain a special **instance-level actor** (separate from any
user) used to sign GET requests on behalf of the server itself. This is
used for fetching remote objects without attributing the fetch to a
specific user.

The instance actor typically has a well-known URL such as:
- `https://example.com/actor`
- `https://example.com/users/instanceactor`

When fetching a remote object to verify it (e.g. during signature verification
of an incoming activity), you should use the instance actor's key to sign
the outbound GET. Remote servers generally do not attempt to verify the
signature on requests made to resolve a `keyId` for the first time.

---

## 7. Key Rotation

If an actor rotates their keypair, the old public key is no longer valid.
Implementations must handle this:

1. Verification fails with the cached key
2. Re-fetch the actor document from the source (bypass cache)
3. Retry verification with the new key
4. If it succeeds, update your local cache

Without this retry logic, federation will break every time a user's key is
rotated.

---

## 8. Interoperability Quirks

This section documents known bugs, deviations, and incompatibilities across
Fediverse implementations. These are real-world issues that have caused
federation failures.

### 8.1 Query String in `(request-target)`

Mastodon historically omitted query strings from `(request-target)`, signing
only the path. GoToSocial included query parameters, which broke paged
Collection fetches.

Both now use a **double-attempt strategy**:
- Signing: sign with query params; if remote returns 401, retry without
- Verification: verify with query params; if it fails, retry without

If implementing signature verification for paged collections, support both.

### 8.2 `hs2019` Algorithm Interpretation

`hs2019` is a placeholder meaning "determine algorithm from key metadata."
Different implementations interpret it inconsistently:

| Implementation | Interpretation of `hs2019` |
|---|---|
| Mastodon | RSA-SHA256 |
| PeerTube | RSA-SHA512 |
| GoToSocial | Signs as RSA-SHA256; verifies RSA-SHA256, RSA-SHA512, Ed25519 in order |
| Lemmy | Sends `hs2019` string |

**Recommendation:** When verifying `hs2019`, try RSA-SHA256 first, then
RSA-SHA512, then Ed25519. When signing, use RSA-SHA256.

### 8.3 `(created)` and `(expires)` Pseudo-Headers

Mastodon **rejects** `(created)` and `(expires)` unless the algorithm is
`hs2019`. Sending `algorithm="rsa-sha256"` with `(created)` in the headers
list produces:

> "Invalid pseudo-header (created) for rsa-sha256"

Older Pleroma versions do not support `(created)` at all. GoToSocial
v0.16.0-rc1 temporarily switched to `(created)` instead of `Date`, breaking
federation with Akkoma/Pleroma and Bookwyrm — it was reverted.

**Recommendation:** Use `Date` rather than `(created)` for maximum
compatibility.

### 8.4 URL Encoding in `(request-target)`

Pleroma does **not** URL-decode the request-target path before constructing
the signing string. Mastodon **does** URL-decode it. If an inbox path
contains percent-encoded characters (e.g. `%40`), one side signs the encoded
form and the other verifies against the decoded form — silent failure.

**Security note:** Percent-encoded newlines (`%0A`) in a path could inject
fake header lines into the signing string if the path is decoded before
signing string construction.

**Recommendation:** Use the path as-is on the wire without decoding. Be
aware that web frameworks (Rails, ASP.NET) may auto-decode before your
application sees the path.

### 8.5 `Signature` Header vs `Authorization` Header

Both are defined in cavage. In practice, virtually all Fediverse
implementations use only the `Signature` header. Mastodon does not fall
back to `Authorization: Signature ...`.

**Recommendation:** Always use the `Signature` header.

### 8.6 Clock Skew Tolerance

Tolerance windows vary widely across implementations:

| Implementation | Tolerance window |
|---|---|
| Mastodon | ±1 hour (CLOCK_SKEW_MARGIN), max 12 hours (EXPIRATION_WINDOW_LIMIT) |
| Pleroma/Akkoma | Up to 2 hours old, max 40 minutes in the future |
| SWICG recommendation | ~1 hour plus a few minutes buffer |
| Some implementations | As tight as 30 seconds |

If your server's clock is significantly wrong, or a remote server's clock
is wrong, signatures will fail. NTP synchronisation is essential.

### 8.7 `keyId` Format Divergence

| Implementation | `keyId` format | Dereferencing |
|---|---|---|
| Mastodon | Fragment URI: `…/users/alice#main-key` | Returns full actor; key identified by fragment |
| GoToSocial | Path URI: `…/users/alice/main-key` | Returns key stub with `owner` back-link |

Receivers must handle both. When the `keyId` contains a fragment, strip it
before fetching. When the fetched document is a raw Key (not an actor),
follow `owner`/`controller` to the actor.

If `publicKey` is an array in the actor, match `keyId` against each key's
`id` to find the right one.

### 8.8 `Digest` Header

**Mastodon only accepts SHA-256.** Sending `SHA-512=...` alone will be
rejected. Mastodon validates that the decoded digest is exactly 32 bytes.

**Case sensitivity:** Mastodon lowercases the algorithm name when parsing
and checks for `sha-256`. The canonical format in the wild is uppercase
`SHA-256=`. Mixed case is accepted by Mastodon but may not be by others.

**Empty body:** A POST with an empty body MUST include a Digest of the empty
string: `SHA-256=47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU=`

**RFC 9530 rename:** RFC 9530 renames `Digest` to `Content-Digest`. Mastodon
4.5+ accepts both. Most implementations still send the old `Digest` header.
Send `Digest` for compatibility; accept both.

### 8.9 Base64 Encoding

Use **standard base64 with padding** — not URL-safe base64.

In Ruby, use `Base64.strict_encode64`, NOT `Base64.encode64` — the latter
inserts newlines every 60 characters per RFC 2045, which breaks verification
on the receiving side.

### 8.10 Multi-Value Header Concatenation

The spec requires multiple values for the same header to be concatenated
with `, ` (comma-space). Pixelfed historically did not comma-separate values,
causing verification failures against GoToSocial and Mastodon in secure mode.
Fixed in Pixelfed PR #4504.

### 8.11 Trailing Newline in Signing String

The signing string must **not** include a trailing `\n` after the last line.
This is a common silent failure — the signature is generated with a trailing
newline, which doesn't match the signature generated without one during
verification. Multiple SocialHub discussions document this as one of the most
frequent implementation bugs.

### 8.12 Unsigned GET Requests

Pixelfed did not sign GET requests until 2021, breaking federation with any
server running authorized fetch / secure mode. GoToSocial requires signed
GETs in all modes.

**Recommendation:** Sign GET requests. Use the instance actor for GET
requests not attributable to a specific user.

### 8.13 PeerTube Signature Header Prefix Bug (Fixed)

PeerTube v2.1.1 prefixed the `Signature` header value with the literal
string `"Signature "`, producing `Signature: Signature keyId=...`. This
was caused by an older version of the `http-signature` npm library. Fixed
in PeerTube v2.2. Mentioned here because old PeerTube instances may still
be in the wild.

### 8.14 Misskey Digest/Host Validation Bug (Fixed — CVE-2023-49079)

Misskey prior to v2023.11.1 did **not** validate the `Digest` or `Host`
headers — only the cryptographic signature was checked. This allowed
attackers to craft requests with valid signatures but spoofed bodies,
impersonating any remote user. CVSS 9.3 Critical.

**Implication for implementors:** Always validate `Digest` and `Host` as
part of signature verification, not just the cryptographic signature itself.

### 8.15 Reverse Proxy / Host Header Issues

When a reverse proxy rewrites the `Host` header, the signed `host` value
won't match what the application sees. In nginx, use `proxy_set_header Host $host`.

A documented case: Ghost on AWS behind CloudFront had federation break
because CloudFront sends `CloudFront-Forwarded-Proto` instead of the
standard `X-Forwarded-Proto`, causing the app to generate HTTP URLs instead
of HTTPS, breaking actor ID matching and signature verification.

### 8.16 IDN / Punycode in Host Headers

Instances with non-ASCII domain names (e.g., Cyrillic) store the punycode
version internally but may receive the Unicode version in incoming requests.
If the local server compares against punycode and the incoming `host` header
is Unicode (or vice versa), signature verification of the `host` header fails.

**Recommendation:** Use ASCII/punycode in all URLs and `Host` headers.

### 8.17 HTTP/1.1 Line Folding

The cavage-12 canonicalization algorithm does not account for HTTP/1.1
obs-fold (continuation lines starting with whitespace). While line folding
is deprecated, it could still appear from legacy clients or proxies. Most
implementations do not handle it.

### 8.18 Shared Library Landscape

Very few implementations share HTTP signature code:

| Library | Used by |
|---|---|
| `@peertube/http-signature` (npm) | PeerTube, Misskey |
| `pleroma/http_signatures` (Elixir) | Pleroma, Mobilizon |
| Everyone else | Custom implementations |

This is why the same spec ambiguity can be interpreted differently by 10+
independent codebases — there is no shared reference implementation to
enforce consistency.

---

## 9. Debugging Checklist

When signatures fail, check in this order:

1. **Clock skew** — is the `Date` header within tolerance? Check NTP on both servers.
2. **Trailing newline** — is the signing string missing a trailing `\n`, or does it have one it shouldn't?
3. **Header name case** — are all header names lowercased in the signing string?
4. **`(request-target)` construction** — is it `method_lowercase + " " + path`? Does path include or exclude query string? (Try both.)
5. **Digest mismatch** — does the `Digest` header match the actual body? Empty body is not the same as no body.
6. **Base64 encoding** — is the signature standard base64 with padding and no embedded newlines?
7. **`keyId` resolution** — does the fetched key's `id` match the `keyId` exactly (including fragment)?
8. **Key rotation** — is the cached key stale? Try re-fetching the actor.
9. **Reverse proxy** — is the `Host` header being rewritten before the application sees it?
10. **Algorithm mismatch** — if remote is PeerTube, try RSA-SHA512 in addition to RSA-SHA256.

---

## 10. Minimum Required Headers (Consensus)

| Request type | Required in signed headers |
|---|---|
| POST (inbox delivery) | `(request-target)`, `host`, `date`, `digest`, `content-type` |
| GET (authorized fetch) | `(request-target)`, `host`, `date` |

Most Fediverse software will reject POST requests without a signed `Digest`,
and GET requests without a signed `(request-target)`, in order to prevent
replay attacks.
