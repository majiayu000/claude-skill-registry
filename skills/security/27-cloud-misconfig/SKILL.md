---
name: cloud-misconfig
description: Hunt cloud misconfigurations exposed externally — open S3/GCS buckets, exposed IAM-tied EC2 metadata, Cognito misconfig, GitHub Actions secret leakage, exposed Kubernetes API, public Elastic / Kibana / Mongo, Firebase RTDB rules, weak AWS access keys discovered in JS/mobile. Use when leveraging leaked credentials or hunting cloud surface in scope.
metadata:
  type: skill
  phase: hunt
  vuln_class: cloud
  tools: [aws-cli, prowler, ScoutSuite, cloudsplaining, enumerate-iam, s3scanner]
---

# Cloud Misconfig

> Leaked AWS keys + missing IAM check = full account take.

## When to invoke

**Trigger phrases:**
- "S3 bucket"
- "exposed cloud"
- "AWS key found"
- "Firebase config"
- "Kubernetes exposed"

## In-scope check FIRST

Cloud assets belong to the target — confirm scope:
- `*.s3.amazonaws.com` — usually OOS unless explicitly in-scope OR you confirm bucket ownership via DNS/branding
- Subdomains pointing to cloud services — see `[[subdomain-takeover]]`
- Leaked credentials in code/apps belonging to target — usually in-scope as info disclosure

## The 10 cloud attack surfaces

### 1. Public S3 / GCS / Azure Blob buckets

Common naming guesses:
```
{target}
{target}-backup
{target}-prod
{target}-staging
{target}-dev
{target}-uploads
{target}-assets
{target}-logs
{target}-private
{target}-internal
{target}-data
{target}-media
{target}-images
{target}-cdn
{target}-config
{target}-test
{target}.com.{everything-above}
```

Tools:
```bash
# s3scanner
pip install s3scanner
echo "target" | s3scanner scan --bucket-targets -

# Or with bucket-list
s3scanner scan --buckets-file buckets.txt

# CloudEnum (multi-cloud)
git clone https://github.com/initstring/cloud_enum
python3 cloud_enum.py -k target
```

For found buckets, test access:
```bash
# Anonymous list
aws s3 ls s3://bucket-name/ --no-sign-request

# Anonymous read of specific object
aws s3 cp s3://bucket-name/file.txt - --no-sign-request

# Anonymous write (the high-severity one)
echo "ccs-canary" | aws s3 cp - s3://bucket-name/canary-claude-cybersecurity-skills --no-sign-request

# ACL inspection
aws s3api get-bucket-acl --bucket bucket-name --no-sign-request
```

### 2. Cognito Identity Pool misconfig

```bash
# Find Cognito Identity Pool IDs (usually in JS bundles, mobile apps)
grep -roE 'us-east-1:[a-f0-9-]{36}|us-west-[0-9]:[a-f0-9-]{36}' loot/target/js/

# Once you have an Identity Pool ID, test for unauthenticated access:
aws cognito-identity get-id --identity-pool-id us-east-1:abc-123 --region us-east-1
aws cognito-identity get-credentials-for-identity --identity-id us-east-1:xxx --region us-east-1
# If credentials returned → unauth Cognito → potentially access to other AWS services
```

If credentials work, enumerate permissions:
```bash
# What can this identity do?
enumerate-iam --access-key X --secret-key Y --session-token Z --region us-east-1
```

### 3. AWS access keys in code

Already covered in `[[js-analysis]]` and `[[mobile-recon-android]]`. Once you have keys:

```bash
export AWS_ACCESS_KEY_ID=AKIA...
export AWS_SECRET_ACCESS_KEY=...
[ export AWS_SESSION_TOKEN=... ]   # if temp creds

# Identify the user/role
aws sts get-caller-identity

# Enumerate permissions
enumerate-iam --access-key $AWS_ACCESS_KEY_ID --secret-key $AWS_SECRET_ACCESS_KEY

# Or with pacu (interactive)
pacu
> set_keys
> run iam__enum_users_roles_policies
> run aws__enum_account
> run s3__enum
```

### 4. Firebase Realtime Database / Firestore

Mobile / web apps may embed Firebase URLs. Test rules:

```bash
# Realtime DB
curl https://target-default-rtdb.firebaseio.com/.json
# If returns data → rules are wide-open

# Read specific path
curl https://target-default-rtdb.firebaseio.com/users.json
curl https://target-default-rtdb.firebaseio.com/admin.json

# Write
curl -X PUT https://target-default-rtdb.firebaseio.com/canary.json -d '"ccs-canary"'

# Firestore (REST API)
curl "https://firestore.googleapis.com/v1/projects/{project_id}/databases/(default)/documents/users"
```

Also test `.well-known/firebase`:
```bash
curl https://target.com/.well-known/firebase-config.json
curl https://target.com/__/firebase/init.json
```

### 5. Exposed Kubernetes API

```bash
# Common K8s API ports
curl -k https://target.com:6443/
curl -k https://target.com:6443/api/v1/namespaces
curl -k https://target.com:8443/

# If accessible without auth → enumerate
kubectl --insecure-skip-tls-verify --server=https://target.com:6443 get pods --all-namespaces

# Look for Kubernetes dashboards
curl -k https://target.com:30000   # NodePort often
curl -k https://target.com/api/v1/   # Maybe behind ingress

# Exposed kubelet (port 10250)
curl -k https://target.com:10250/pods
curl -k https://target.com:10250/runningpods
```

### 6. Elastic / Kibana / Mongo / Redis public

Find via shodan / port scan:
```bash
# Naabu / nmap of target IP ranges
naabu -host target.com -p 9200,5601,27017,6379,8086,5984,9000,15672

# Direct test
curl http://target.com:9200/_cat/indices?v       # Elastic
curl http://target.com:5601/api/status            # Kibana
echo "info" | redis-cli -h target.com -p 6379    # Redis
mongosh "mongodb://target.com:27017"             # MongoDB
```

If unauth access → potentially CRITICAL.

### 7. GitHub Actions secrets leakage

If target has public repos:
```bash
# Search for secret leaks across all repo history
trufflehog github --org target-inc --json

# Or for a specific repo
trufflehog github --repo https://github.com/target-inc/some-repo

# Check public Actions logs (sometimes leak via prints)
# Browse https://github.com/target-inc/repo/actions
```

### 8. CloudFront / Cloudflare origin IP disclosure

If they're behind CF but you can find origin IP, you can bypass WAF:
```bash
# Censys / Shodan for cert search
censys search "names: target.com" --index-type certificates

# SecurityTrails historical DNS
curl "https://api.securitytrails.com/v1/history/target.com/dns/a" -H "APIKEY: ..."

# Just try common origin IP patterns from dig
dig +short api-origin.target.com
dig +short api.internal.target.com
```

### 9. SSRF → cloud metadata (chain)

See `[[ssrf]]` — once you have SSRF, hit IMDS for IAM creds, then proceed here for exploitation.

### 10. Public CI/CD secrets

```bash
# Look for build artifacts, env files
grep -hroE 'STRIPE_SECRET|JWT_SECRET|AWS_SECRET|GH_TOKEN|DB_PASSWORD' .
grep -rE 'docker-compose\.yml|\.env|circleci/config\.yml' loot/

# Look for terraform.tfstate (gold)
# Look for serverless.yml (env vars)
```

## prowler — comprehensive AWS audit (if you have credentials)

```bash
pip install prowler-cloud
prowler aws --profile target-creds

# Output: pdf report of misconfigs across IAM, S3, EC2, RDS, etc.
```

## Output template

```markdown
## Critical: Public S3 bucket `target-uploads` exposing 12M user files (PII)

### Summary
The S3 bucket `target-uploads`, used by `app.target.com` to store user-uploaded receipts and ID documents, is configured with anonymous READ permission. Any internet user can list and download all 12M+ uploaded files without authentication.

### Steps to reproduce
1. Identified bucket via JS bundle on `https://app.target.com/static/main.js`:
   ```
   uploadEndpoint: "https://target-uploads.s3.amazonaws.com"
   ```
2. Test anonymous list:
   ```bash
   aws s3 ls s3://target-uploads/ --no-sign-request
   # Returns: ...
   # 2026-05-30 14:32:18    234234 12345-passport.jpg
   # 2026-05-30 14:32:19    192834 12345-id-card.jpg
   # ...
   ```
3. Test anonymous read of a single object:
   ```bash
   aws s3 cp s3://target-uploads/12345-passport.jpg /tmp/sample.jpg --no-sign-request
   # Successfully downloaded — file is a user's passport photo
   ```
4. ACL confirmation:
   ```bash
   aws s3api get-bucket-acl --bucket target-uploads --no-sign-request
   # Includes: "URI": "http://acs.amazonaws.com/groups/global/AllUsers" with READ permission
   ```

### Impact
- 12M+ files exposed, including:
  - Passport scans
  - ID cards
  - Driver licenses
  - Receipts (with payment card last-4 visible)
- Direct GDPR/CCPA breach
- Customer trust impact if exposed publicly
- Attackers can correlate filenames with user IDs (filenames include `{user_id}-{doctype}.{ext}`)

### Suggested fix
1. Set bucket ACL to private:
   ```
   aws s3api put-bucket-acl --bucket target-uploads --acl private
   ```
2. Use presigned URLs for downloads (5-minute TTL, scoped to user)
3. Block public access at the account level
4. Audit other buckets for the same issue (see attached list of suspected siblings)

### What we did
- Listed bucket via `--no-sign-request` (anonymous)
- Downloaded ONE sample file to confirm readability
- Deleted the sample locally
- Did NOT download additional files
- Did NOT redistribute
```

## Cross-references

- `[[ssrf]]` — SSRF → IMDS → IAM credentials → here
- `[[mobile-recon-android]]` — extract AWS keys from mobile
- `[[js-analysis]]` — extract AWS keys from JS
- `[[subdomain-takeover]]` — dangling cloud CNAMEs

## Common pitfalls

1. **Scope ambiguity.** Confirm cloud resource belongs to target — branding, DNS evidence, OR bucket name match.
2. **Causing impact.** Don't download large amounts of data. One file is proof.
3. **Treating "public" buckets as "vuln".** Some buckets are intentionally public (CDN). Verify content sensitivity.
4. **Old / cached results.** AWS access can change quickly. Re-verify before reporting.
5. **Using your real AWS account for keys with malware.** Spin up a fresh AWS account for forensics.

## Severity guide

| Finding | Severity |
|---|---|
| Public S3/GCS bucket with sensitive data (PII, secrets) | Critical |
| Public bucket with metadata only (no PII) | Medium |
| AWS Access Key with admin/broad IAM | Critical |
| AWS Access Key with read-only on non-sensitive | Medium |
| Firebase RTDB public read of user data | Critical |
| Firebase RTDB public write (data manipulation) | Critical |
| Public Elastic with internal logs | Critical |
| Public Kubernetes API (anonymous) | Critical |
| Cognito unauth identity → IAM access | High-Critical |
| GitHub Actions secret leak (active credential) | Critical |

## Always: snapshot your evidence

Don't rely on the bucket / endpoint staying open. Save:
- Screenshot of bucket listing
- `aws s3api get-bucket-acl` output saved to file
- Sample file (one, deleted after PoC)
- Timestamp of test

Reports without timestamps and evidence often face "we can't reproduce" → N/A.

## Quick recon one-liner

```bash
# Combine bucket guess + s3scanner + firebase test in one
TARGET="target"

# Buckets
echo "$TARGET" | s3scanner scan --bucket-targets -

# Firebase (try common subdomains)
for sub in "" "-default-rtdb" "-prod" "-staging"; do
    url="https://${TARGET}${sub}.firebaseio.com/.json"
    code=$(curl -s -o /dev/null -w "%{http_code}" "$url")
    [[ "$code" == "200" ]] && echo "[ACCESSIBLE] $url"
done

# Cloudfront leak via cert
curl -s "https://crt.sh/?q=${TARGET}&output=json" | jq -r '.[] | select(.name_value | test("cloudfront")) | .name_value' | sort -u
```
