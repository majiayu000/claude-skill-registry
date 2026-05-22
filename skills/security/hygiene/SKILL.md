---
name: hygiene
description: |
    Use when enforcing defensive coding practices that treat all data as untrusted — regardless of source. Covers sanitization, canonicalization, encoding, and validation of inputs AND outputs at every component boundary, including internal databases, caches, message queues, and inter-service calls.
    USE FOR: data hygiene, sanitization, canonicalization, normalization, output encoding, trust boundaries, defense in depth, zero trust data handling, internal data validation, component boundary security
    DO NOT USE FOR: specific injection attack patterns (use input-validation or owasp), cryptographic controls (use cryptography), API-level security headers (use api-security)
license: MIT
metadata:
  displayName: "Hygiene"
  author: "Tyler-R-Kendrick"
compatibility: claude, copilot, cursor
references:
  - title: "OWASP Input Validation Cheat Sheet"
    url: "https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html"
  - title: "OWASP Cheat Sheet Series"
    url: "https://cheatsheetseries.owasp.org"
---

# Hygiene — Trust No Data

## Overview

Security hygiene is the discipline of treating **all data as untrusted** at every component boundary — not just data from end users. Internal databases, caches, message queues, partner APIs, configuration stores, and even your own microservices can deliver data that is malformed, stale, tampered with, or injected. A compromised internal system, a poisoned cache entry, or a corrupted database row can be just as dangerous as a malicious HTTP request.

The core principle: **sanitize, validate, and encode at the boundary of every component**, not just at the perimeter.

> "The Jenga tower of trust collapses when any single block is compromised. Don't assume the block below you is sound — verify it."

## The Trust Boundary Model

Every component has boundaries where data enters and exits. Each boundary is a point where hygiene must be enforced.

```
                    ┌─────────────────────┐
  User Input ──────►│                     │──────► Database
                    │    Your Component   │
  Database ────────►│                     │──────► API Response
                    │   SANITIZE HERE     │
  Message Queue ───►│   ON EVERY EDGE     │──────► Message Queue
                    │                     │
  Cache ───────────►│                     │──────► Logs
                    │                     │
  Partner API ─────►│                     │──────► Downstream Service
                    └─────────────────────┘
```

### Why Internal Sources Are Untrusted

| Source | Why It Can't Be Trusted | Example Threat |
|--------|------------------------|----------------|
| **Database** | Rows may have been inserted by a compromised service, SQL injection, or legacy code without validation | Stored XSS: HTML in a database field rendered without encoding |
| **Cache (Redis, Memcached)** | Cache poisoning, stale data, no authentication by default | Attacker writes malicious payload to shared cache key |
| **Message Queue** | Any producer can publish; messages may be replayed or tampered | Deserialization attack via crafted message payload |
| **Internal API / Microservice** | Service may be compromised, misconfigured, or returning unexpected data | Downstream service returns user-controlled data without sanitization |
| **Configuration Store** | Config values may be modified by operators or injected via environment | Command injection through a config value used in a shell call |
| **File System** | Files may be written by other processes, users, or symlink attacks | Path traversal via a filename read from a temp directory |
| **Logs (when read back)** | Log entries may contain injected content | Log injection leading to SIEM manipulation or log4shell-style attacks |

## Sanitization

Sanitization removes or neutralizes dangerous content from data. It should happen **on input to your component**, before the data is processed or stored.

### Strategies

| Strategy | What It Does | When to Use |
|----------|-------------|-------------|
| **Stripping** | Removes disallowed characters or tags entirely | HTML tags from plain-text fields, control characters from strings |
| **Escaping** | Replaces special characters with safe equivalents | HTML entities, SQL parameterization, shell escaping |
| **Allowlisting** | Accepts only values matching a known-good pattern | Enum fields, expected formats (UUID, ISO date, email) |
| **Type coercion** | Converts data to the expected type | Parse string to integer, parse to date object |

### Sanitize Both Directions

- **Inbound**: Validate and sanitize data entering your component from any source.
- **Outbound**: Encode data leaving your component for the target context (HTML, SQL, shell, URL, JSON, XML).

```
  Inbound                           Outbound
  ────────                          ────────
  Validate type/format              Encode for HTML context
  Enforce allowlist                 Encode for SQL (parameterize)
  Strip/escape dangerous chars      Encode for shell (avoid shell if possible)
  Normalize/canonicalize            Encode for URL
  Reject if invalid                 Encode for JSON/XML
```

## Canonicalization

Canonicalization (C14N) converts data to its simplest, standard form **before** validation. Without canonicalization, attackers bypass validation by using alternate representations of the same value.

### Common Bypass Techniques Prevented by Canonicalization

| Technique | Example | What Canonicalization Does |
|-----------|---------|--------------------------|
| **Unicode normalization** | `\uFF41` (fullwidth 'a') vs `a` | Normalize to NFC/NFD before comparing |
| **URL encoding** | `%2e%2e%2f` = `../` | Decode URL encoding before path validation |
| **Double encoding** | `%252e` → `%2e` → `.` | Decode iteratively until stable |
| **Case variation** | `SELECT` vs `SeLeCt` | Lowercase before matching keywords |
| **Path normalization** | `/app/../etc/passwd` | Resolve to canonical absolute path (`/etc/passwd`) |
| **Null bytes** | `file.php%00.jpg` | Strip null bytes before extension check |
| **Homoglyph substitution** | `pаypal.com` (Cyrillic 'а') | Normalize to ASCII or punycode |
| **Whitespace injection** | `admin\t` vs `admin` | Trim and normalize whitespace |

### Canonicalization Order

Always canonicalize **before** validation:

```
Raw Input → Decode → Normalize → Canonicalize → Validate → Process
```

If you validate before canonicalizing, an attacker can encode their payload to pass validation and then have it decoded into a malicious form later.

### Language Examples

**Path Canonicalization**
```csharp
// C# — Resolve to absolute path and verify it's within the allowed directory
string basePath = Path.GetFullPath("/app/uploads");
string requested = Path.GetFullPath(Path.Combine(basePath, userInput));
if (!requested.StartsWith(basePath + Path.DirectorySeparatorChar))
    throw new SecurityException("Path traversal detected");
```

```python
# Python — Resolve symlinks and relative segments
import os
base = os.path.realpath("/app/uploads")
requested = os.path.realpath(os.path.join(base, user_input))
if not requested.startswith(base + os.sep):
    raise ValueError("Path traversal detected")
```

**Unicode Normalization**
```python
import unicodedata

# Normalize to NFC before comparing or validating
clean = unicodedata.normalize("NFC", user_input)
```

```csharp
// C# — Normalize to FormC (NFC)
string clean = userInput.Normalize(NormalizationForm.FormC);
```

**URL Canonicalization**
```python
from urllib.parse import unquote

def canonicalize_url(url: str) -> str:
    prev = None
    while prev != url:
        prev = url
        url = unquote(url)
    return url
```

## Output Encoding

Output encoding ensures data is safe for the **specific context** it is being rendered or transmitted into. This applies to ALL outputs, not just HTTP responses.

### Context-Specific Encoding

| Output Context | Encoding Required | Why |
|---------------|-------------------|-----|
| **HTML body** | HTML entity encoding (`<` → `&lt;`) | Prevents XSS |
| **HTML attributes** | Attribute encoding (quote special chars) | Prevents attribute injection |
| **JavaScript** | JS string encoding or `JSON.stringify()` | Prevents script injection |
| **SQL** | Parameterized queries (never string concat) | Prevents SQL injection |
| **Shell commands** | Avoid shell entirely; if unavoidable, use library escaping | Prevents command injection |
| **URLs** | URL-encode query parameters and path segments | Prevents parameter injection |
| **XML** | XML entity encoding | Prevents XXE and injection |
| **JSON** | Proper serialization (not string concatenation) | Prevents JSON injection |
| **Log entries** | Strip newlines and control characters | Prevents log injection |
| **Email headers** | Strip newlines from header values | Prevents header injection |

### Encoding Data From Internal Sources

```
Database row → render in HTML?    → HTML-encode the value
Cache value  → insert into SQL?   → use parameterized query
Queue msg    → pass to shell?     → use subprocess array (no shell)
Config value → embed in template? → encode for template context
API response → return to client?  → serialize properly, set Content-Type
```

The encoding must match the **destination context**, regardless of where the data came from.

## Component Boundary Checklist

For every component boundary (inbound or outbound), verify:

| # | Check | Applies To |
|---|-------|-----------|
| 1 | **Type validation** — Is the data the expected type? | All inputs |
| 2 | **Format validation** — Does it match the expected pattern? | Strings, IDs, dates, emails |
| 3 | **Range validation** — Is it within acceptable bounds? | Numbers, dates, string lengths |
| 4 | **Canonicalization** — Is the data in its simplest canonical form? | Paths, URLs, Unicode strings |
| 5 | **Allowlist check** — Is the value in the set of permitted values? | Enums, status codes, roles |
| 6 | **Sanitization** — Have dangerous characters been removed or escaped? | All text inputs |
| 7 | **Output encoding** — Is data encoded for the destination context? | All outputs |
| 8 | **Size limits** — Is the data within acceptable size bounds? | Files, payloads, strings |

## Anti-Patterns

| Anti-Pattern | Why It's Dangerous | Correct Approach |
|-------------|-------------------|-----------------|
| "It's from our database, so it's safe" | Database can contain injected content from any entry point | Encode database values for the output context |
| "We validated it on the way in, so it's clean" | Output context may differ from input context; data may be modified in transit | Encode for the specific output context at point of use |
| "It's an internal API, so we trust it" | Internal services can be compromised or misconfigured | Validate response schema and sanitize values |
| "We use an ORM, so SQL injection is impossible" | Raw queries, dynamic column names, and ORDER BY bypass ORM protections | Always parameterize; review ORM escape hatches |
| "The cache just stores what we put in" | Cache can be poisoned via shared keys, race conditions, or unauthenticated access | Validate and encode cache values on read |
| "Config values are set by operators" | Environment variables and config stores can be compromised | Validate config values at startup; never pass raw to shell or template |

## Best Practices

- **Treat all data as untrusted** regardless of source — user input, databases, caches, queues, APIs, config, and files all deserve the same scrutiny.
- **Canonicalize before validating** — decode, normalize, and resolve data to its simplest form before applying security checks.
- **Encode at the point of use**, not at the point of storage — the correct encoding depends on where the data is going, not where it came from.
- **Validate on both sides of every boundary** — the producer should validate what it sends and the consumer should validate what it receives.
- **Use allowlists over denylists** — it is safer to define what is permitted than to try to enumerate everything that is dangerous.
- **Fail closed** — if data fails validation, reject it entirely rather than attempting to "fix" it and proceeding.
- **Apply the same rigor to outbound data** — log injection, email header injection, and downstream API injection are just as real as XSS.
- **Automate hygiene checks** — use linters, SAST rules (Semgrep, CodeQL), and code review checklists to catch missing validation and encoding at component boundaries.
- **Document trust boundaries** — make them explicit in architecture diagrams and threat models so every developer knows where hygiene enforcement is required.
- **Review ORM and framework escape hatches** — `dangerouslySetInnerHTML`, raw SQL, `HtmlString`, `@Html.Raw()`, `mark_safe()`, and similar constructs bypass built-in protections and require manual encoding.
